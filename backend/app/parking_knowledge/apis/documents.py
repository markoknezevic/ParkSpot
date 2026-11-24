"""HTTP routes for general parking documentation."""

from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status

from app.core.auth import require_registered_user
from app.models import ParkingDocument
from app.parking_knowledge.schemas import (
    ParkingDocumentCreate,
    ParkingDocumentResponse,
    ParkingKnowledgeMatch,
    ParkingKnowledgeSearch,
)
from app.parking_knowledge.services import ParkingKnowledgeService

router = APIRouter(
    prefix="/parking-knowledge",
    tags=["parking-knowledge"],
    dependencies=[Depends(require_registered_user)],
)

EMBEDDING_ERRORS = {
    503: {"description": "Local embedding model is unavailable or inference failed"},
}


@router.post(
    "/documents",
    response_model=ParkingDocumentResponse,
    status_code=status.HTTP_201_CREATED,
    responses=EMBEDDING_ERRORS,
)
async def create_document(
    data: ParkingDocumentCreate,
    service: Annotated[ParkingKnowledgeService, Depends(ParkingKnowledgeService)],
) -> ParkingDocument:
    """Let any registered user store a general rule and its embedding atomically."""
    return await service.create_document(data)


@router.get("/documents", response_model=list[ParkingDocumentResponse])
def list_documents(
    service: Annotated[ParkingKnowledgeService, Depends(ParkingKnowledgeService)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> Sequence[ParkingDocument]:
    return service.list_documents(limit, offset)


@router.get(
    "/documents/{document_id}",
    response_model=ParkingDocumentResponse,
    responses={404: {"description": "Parking document not found"}},
)
def get_document(
    document_id: Annotated[int, Path(gt=0)],
    service: Annotated[ParkingKnowledgeService, Depends(ParkingKnowledgeService)],
) -> ParkingDocument:
    return service.get_document(document_id)


@router.post("/search", response_model=list[ParkingKnowledgeMatch], responses=EMBEDDING_ERRORS)
async def search_knowledge(
    data: ParkingKnowledgeSearch,
    service: Annotated[ParkingKnowledgeService, Depends(ParkingKnowledgeService)],
) -> list[ParkingKnowledgeMatch]:
    """Retrieve relevant documents with source IDs and cosine similarity scores."""
    return await service.search_knowledge(data)
