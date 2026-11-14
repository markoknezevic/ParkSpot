"""Parking spot status lookup model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.slug import SlugMixin

if TYPE_CHECKING:
    from app.models.parking_spot_status import ParkingSpotStatus


class SpotStatus(SlugMixin, TimestampMixin, Base):
    """A status that can be assigned to a parking spot."""

    __tablename__ = "spot_status"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )
    parking_spot_statuses: Mapped[list[ParkingSpotStatus]] = relationship(
        back_populates="status"
    )
