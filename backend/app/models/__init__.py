"""Database models."""

from app.models.base import Base, TimestampMixin
from app.models.parking_lot import ParkingLot
from app.models.parking_spot import ParkingSpot

__all__ = ["Base", "ParkingLot", "ParkingSpot", "TimestampMixin"]
