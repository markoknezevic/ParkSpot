"""Database models."""

from app.models.base import Base, TimestampMixin
from app.models.parking_lot import ParkingLot

__all__ = ["Base", "ParkingLot", "TimestampMixin"]
