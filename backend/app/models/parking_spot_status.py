"""Parking spot status history model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.parking_spot import ParkingSpot
    from app.models.spot_status import SpotStatus


class ParkingSpotStatus(TimestampMixin, Base):
    """A status change in a parking spot's history."""

    __tablename__ = "parking_spot_status"

    id: Mapped[int] = mapped_column(primary_key=True)
    parking_spot_id: Mapped[int] = mapped_column(
        ForeignKey("parking_spots.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    spot_status_id: Mapped[int] = mapped_column(
        ForeignKey("spot_status.id"),
        nullable=False,
        index=True,
    )
    parking_spot: Mapped[ParkingSpot] = relationship(back_populates="status_history")
    status: Mapped[SpotStatus] = relationship(back_populates="parking_spot_statuses")
