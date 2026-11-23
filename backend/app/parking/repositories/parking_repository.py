"""Data access for the parking module."""

from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends
from sqlalchemy import case, func, select
from sqlalchemy.engine import RowMapping
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.models import ParkingLot, ParkingSpot, ParkingSpotStatus, SpotStatus


class ParkingRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db)]) -> None:
        self._session = session

    def get_parking_lots(self) -> Sequence[ParkingLot]:
        """Return all parking lots in a stable order."""

        statement = select(ParkingLot).order_by(ParkingLot.id)
        return self._session.scalars(statement).all()

    def get_parking_lot(self, parking_lot_id: int) -> ParkingLot | None:
        """Return a parking lot with the relationships needed by the response."""

        statement = (
            select(ParkingLot)
            .options(
                joinedload(ParkingLot.parking_spots)
                .joinedload(ParkingSpot.latest_history)
                .joinedload(ParkingSpotStatus.status)
            )
            .where(ParkingLot.id == parking_lot_id)
        )
        return self._session.execute(statement).unique().scalar_one_or_none()

    def get_parking_availability(self, level: int | None = None, parking_lot_id: int | None = None) -> Sequence[RowMapping]:
        """Count latest statuses by lot and level. Groups without spots are omitted."""
        free = func.count(case((SpotStatus.slug == "free", 1)))
        taken = func.count(case((SpotStatus.slug == "taken", 1)))
        pending = func.count(case((SpotStatus.slug == "pending", 1)))
        statement = (
            select(
                ParkingLot.id.label("parking_lot_id"),
                ParkingLot.name.label("parking_lot_name"),
                ParkingSpot.level,
                free.label("free"),
                taken.label("taken"),
                pending.label("pending"),
            )
            .select_from(ParkingSpot)
            .join(ParkingSpot.parking_lot)
            .outerjoin(ParkingSpot.latest_history)
            .outerjoin(ParkingSpotStatus.status)
            .group_by(ParkingLot.id, ParkingLot.name, ParkingSpot.level)
            .order_by(ParkingLot.id, ParkingSpot.level.asc().nulls_last())
        )
        if parking_lot_id is not None:
            statement = statement.where(ParkingLot.id == parking_lot_id)
        if level is not None:
            statement = statement.where(ParkingSpot.level == level)
        return self._session.execute(statement).mappings().all()

    def find_parking_lots_by_name(self, name: str) -> Sequence[ParkingLot]:
        """Match a full lot name case-insensitively without interpreting wildcards."""
        statement = select(ParkingLot).where(func.lower(ParkingLot.name) == name.strip().lower())
        return self._session.scalars(statement).all()
