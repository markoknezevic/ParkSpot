"""Business logic for the parking module."""

from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.models import ParkingLot
from app.parking.repositories import ParkingRepository


class ParkingService:
    def __init__(
        self,
        repository: Annotated[ParkingRepository, Depends(ParkingRepository)],
    ) -> None:
        self._repository = repository

    def get_parking_lots(self) -> Sequence[ParkingLot]:
        return self._repository.get_parking_lots()

    def get_parking_lot(self, parking_lot_id: int) -> ParkingLot:
        parking_lot = self._repository.get_parking_lot(parking_lot_id)
        if parking_lot is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parking lot not found",
            )

        return parking_lot
