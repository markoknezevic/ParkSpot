"""Parking spot database model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint, and_, select
from sqlalchemy.orm import Mapped, aliased, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.parking_spot_status import ParkingSpotStatus

if TYPE_CHECKING:
    from app.models.parking_lot import ParkingLot
    from app.models.spot_status import SpotStatus


def _latest_history_join():
    history = aliased(ParkingSpotStatus)
    latest_id = (
        select(history.id)
        .where(history.parking_spot_id == ParkingSpot.id)
        .order_by(history.created_at.desc(), history.id.desc())
        .limit(1)
        .correlate(ParkingSpot)
        .scalar_subquery()
    )
    return and_(
        ParkingSpot.id == ParkingSpotStatus.parking_spot_id,
        ParkingSpotStatus.id == latest_id,
    )


class ParkingSpot(TimestampMixin, Base):
    """A numbered spot belonging to a parking lot."""

    __tablename__ = "parking_spots"
    __table_args__ = (
        UniqueConstraint("parking_lot_id", "number"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(nullable=False)
    level: Mapped[int | None] = mapped_column(nullable=True)
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

    latest_history: Mapped[ParkingSpotStatus | None] = relationship(
        primaryjoin=_latest_history_join, viewonly=True
    )

    @property
    def last_status(self) -> SpotStatus | None:
        """Return the status from the latest history row, if one exists."""

        return self.latest_history.status if self.latest_history else None
