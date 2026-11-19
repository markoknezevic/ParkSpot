"""Business logic for the parking module."""

from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.engine import RowMapping

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

    def get_parking_availability(self, level: int | None = None, parking_lot_name: str | None = None) -> Sequence[RowMapping]:
        """Return status counts by lot and level across all parking lots."""
        return self._repository.get_parking_availability(level, self._resolve_lot_id(parking_lot_name))

    def list_free_spots(self, level: int | None = None, parking_lot_name: str | None = None) -> Sequence[RowMapping]:
        """Return individual free spots across all parking lots."""
        return self._repository.list_free_spots(level, self._resolve_lot_id(parking_lot_name))

    def _resolve_lot_id(self, name: str | None) -> int | None:
        if name is None:
            return None
        lots = self._repository.find_parking_lots_by_name(name)
        if not lots:
            raise HTTPException(status_code=404, detail="Parking lot not found")
        if len(lots) > 1:
            raise HTTPException(status_code=409, detail="Parking lot name is ambiguous")
        return lots[0].id
