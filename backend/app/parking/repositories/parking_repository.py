"""Data access for the parking module."""

from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

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

        latest_status = ParkingSpotStatus.__table__.alias("latest_parking_spot_status")
        latest_status_id = (
            select(latest_status.c.id)
            .where(
                latest_status.c.parking_spot_id
                == ParkingSpotStatus.parking_spot_id
            )
            .order_by(latest_status.c.created_at.desc(), latest_status.c.id.desc())
            .limit(1)
            .correlate(ParkingSpotStatus)
            .scalar_subquery()
        )

        statement = (
            select(ParkingLot)
            .options(
                selectinload(ParkingLot.parking_spots)
                .selectinload(
                    ParkingSpot.status_history.and_(
                        ParkingSpotStatus.id == latest_status_id
                    )
                )
                .joinedload(ParkingSpotStatus.status)
            )
            .where(ParkingLot.id == parking_lot_id)
        )
        return self._session.scalar(statement)
