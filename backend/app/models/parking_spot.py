"""Parking spot database model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.parking_lot import ParkingLot
    from app.models.parking_spot_status import ParkingSpotStatus
    from app.models.spot_status import SpotStatus


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
    status_history: Mapped[list[ParkingSpotStatus]] = relationship(
        back_populates="parking_spot",
        cascade="all, delete-orphan",
        order_by="ParkingSpotStatus.created_at",
    )

    @property
    def last_status(self) -> SpotStatus | None:
        """Return the spot status from the latest history entry."""

        if not self.status_history:
            return None

        latest_history = max(
            self.status_history,
            key=lambda status: (status.created_at, status.id),
        )
        return latest_history.status
