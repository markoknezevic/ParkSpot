"""Parking lot database model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.parking_spot import ParkingSpot


class ParkingLot(TimestampMixin, Base):
    """A physical parking lot and its space capacity."""

    __tablename__ = "parking_lots"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    parking_spots: Mapped[list[ParkingSpot]] = relationship(
        back_populates="parking_lot",
        cascade="all, delete-orphan",
    )
