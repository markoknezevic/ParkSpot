"""Parking spot database model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.parking_lot import ParkingLot


class ParkingSpot(TimestampMixin, Base):
    """A numbered spot belonging to a parking lot."""

    __tablename__ = "parking_spots"
    __table_args__ = (
        UniqueConstraint("parking_lot_id", "number"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(nullable=False)
    parking_lot_id: Mapped[int] = mapped_column(
        ForeignKey("parking_lots.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    parking_lot: Mapped[ParkingLot] = relationship(back_populates="parking_spots")
