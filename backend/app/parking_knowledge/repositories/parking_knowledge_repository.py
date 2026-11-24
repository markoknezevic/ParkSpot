"""Persistence and exact cosine retrieval for parking documents."""

from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends
from sqlalchemy import and_, case, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, defer

from app.core.database import get_db
from app.models import ParkingDocument


class ParkingKnowledgeRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db)]) -> None:
        self._session = session

    def create(self, title: str, content: str, embedding_model: str, embedding: list[float]) -> ParkingDocument:
        document = ParkingDocument(title=title, content=content, embedding_model=embedding_model, embedding=embedding)
        self._session.add(document)
        try:
            self._session.commit()
        except SQLAlchemyError:
            self._session.rollback()
            raise
        return document

    def list_documents(self, limit: int, offset: int) -> Sequence[ParkingDocument]:
        statement = (
            select(ParkingDocument)
            .options(defer(ParkingDocument.embedding))
            .order_by(ParkingDocument.id)
            .limit(limit)
            .offset(offset)
        )
        return self._session.scalars(statement).all()

    def get_document(self, document_id: int) -> ParkingDocument | None:
        statement = (
            select(ParkingDocument)
            .options(defer(ParkingDocument.embedding))
            .where(ParkingDocument.id == document_id)
        )
        return self._session.scalar(statement)

    def search(self, embedding: list[float], embedding_model: str, limit: int, min_similarity: float) -> list[dict]:
        # CASE prevents PostgreSQL from evaluating cosine distance on legacy
        # vectors of a different dimension, regardless of predicate ordering.
        distance = case((
            and_(
                ParkingDocument.embedding_model == embedding_model,
                func.vector_dims(ParkingDocument.embedding) == len(embedding),
            ),
            ParkingDocument.embedding.cosine_distance(embedding),
        ))
        statement = (
            select(
                ParkingDocument.id.label("document_id"),
                ParkingDocument.title,
                ParkingDocument.content,
                (1 - distance).label("similarity"),
            )
            .where(distance <= 1 - min_similarity)
            .order_by(distance, ParkingDocument.id)
            .limit(limit)
        )
        return [dict(row) for row in self._session.execute(statement).mappings()]
