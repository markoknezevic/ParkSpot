"""Parking lot database model."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ParkingLot(TimestampMixin, Base):
    """A physical parking lot and its space capacity."""

    __tablename__ = "parking_lots"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
