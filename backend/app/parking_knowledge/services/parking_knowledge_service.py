"""Index and retrieve general parking documentation."""

from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.concurrency import run_in_threadpool

from app.models import ParkingDocument
from app.parking_knowledge.embedding_client import EmbeddingClient
from app.parking_knowledge.repositories import ParkingKnowledgeRepository
from app.parking_knowledge.schemas import ParkingDocumentCreate, ParkingKnowledgeMatch, ParkingKnowledgeSearch


class ParkingKnowledgeService:
    def __init__(
        self,
        repository: Annotated[ParkingKnowledgeRepository, Depends(ParkingKnowledgeRepository)],
        embeddings: Annotated[EmbeddingClient, Depends(EmbeddingClient)],
    ) -> None:
        self._repository = repository
        self._embeddings = embeddings

    async def create_document(self, data: ParkingDocumentCreate) -> ParkingDocument:
        embedding = await self._embeddings.embed(data.embedding_text)
        return await run_in_threadpool(
            self._repository.create,
            title=data.title,
            content=data.content,
            embedding_model=self._embeddings.model,
            embedding=embedding,
        )

    def list_documents(self, limit: int, offset: int) -> Sequence[ParkingDocument]:
        return self._repository.list_documents(limit, offset)

    def get_document(self, document_id: int) -> ParkingDocument:
        document = self._repository.get_document(document_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Parking document not found")
        return document

    async def search_knowledge(self, data: ParkingKnowledgeSearch) -> list[ParkingKnowledgeMatch]:
        embedding = await self._embeddings.embed(data.query, is_query=True)
        matches = await run_in_threadpool(
            self._repository.search,
            embedding=embedding,
            embedding_model=self._embeddings.model,
            limit=data.limit,
            min_similarity=data.min_similarity,
        )
        return [ParkingKnowledgeMatch.model_validate(match) for match in matches]
