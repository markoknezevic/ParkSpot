"""User database model."""

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class User(TimestampMixin, Base):
    """A user and their contact information."""

    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint(
            "auth_issuer", "auth_subject", name="uq_users_auth_identity"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False)

    auth_issuer: Mapped[str | None] = mapped_column(String(255), nullable=True)
    auth_subject: Mapped[str | None] = mapped_column(String(255), nullable=True)
