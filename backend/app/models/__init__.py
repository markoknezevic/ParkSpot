"""Database models."""

from app.models.base import Base, TimestampMixin
from app.models.parking_lot import ParkingLot
from app.models.parking_spot import ParkingSpot
from app.models.parking_spot_status import ParkingSpotStatus
from app.models.slug import SlugMixin
from app.models.spot_status import SpotStatus
from app.models.user import User

__all__ = [
    "Base",
    "ParkingLot",
    "ParkingSpot",
    "ParkingSpotStatus",
    "SlugMixin",
    "SpotStatus",
    "TimestampMixin",
    "User",
]
