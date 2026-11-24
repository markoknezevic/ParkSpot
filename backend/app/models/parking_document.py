"""General parking documentation, stored with one embedding per document."""

from pgvector.sqlalchemy import VECTOR
from sqlalchemy import CheckConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ParkingDocument(TimestampMixin, Base):
    __tablename__ = "parking_documents"
    __table_args__ = (
        CheckConstraint(
            "embedding_model != 'BAAI/bge-small-en-v1.5' OR vector_dims(embedding) = 384",
            name="local_embedding_dimensions",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding_model: Mapped[str] = mapped_column(String(100), nullable=False)
    # Retain legacy vectors until they are regenerated with the local model.
    embedding: Mapped[list[float]] = mapped_column(VECTOR(), nullable=False)
