"""HTTP contracts for general parking documents and semantic search."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel

from app.parking_knowledge.constants import MAX_EMBEDDING_INPUT_BYTES


class RequestSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
        extra="forbid",
    )


class ParkingDocumentCreate(RequestSchema):
    title: str = Field(min_length=1, max_length=200, pattern=r"^[^\x00]*$")
    content: str = Field(min_length=1, max_length=MAX_EMBEDDING_INPUT_BYTES, pattern=r"^[^\x00]*$")

    @model_validator(mode="after")
    def validate_embedding_size(self) -> "ParkingDocumentCreate":
        if len(self.embedding_text.encode("utf-8")) > MAX_EMBEDDING_INPUT_BYTES:
            raise ValueError("Title and content together must not exceed 8000 UTF-8 bytes")
        return self

    @property
    def embedding_text(self) -> str:
        return f"{self.title}\n\n{self.content}"


class ResponseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)


class ParkingDocumentResponse(ResponseSchema):
    id: int
    title: str
    content: str
    embedding_model: str
    created_at: datetime
    updated_at: datetime


class ParkingKnowledgeSearch(RequestSchema):
    query: str = Field(min_length=1, max_length=2000, pattern=r"^[^\x00]*$")
    limit: int = Field(default=5, ge=1, le=20, strict=True)
    min_similarity: float = Field(default=0.3, ge=-1, le=1, allow_inf_nan=False)


class ParkingKnowledgeMatch(ResponseSchema):
    document_id: int
    title: str
    content: str
    similarity: float
