"""Data access for the parking module."""

from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.models import ParkingLot, ParkingSpot, ParkingSpotStatus


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
