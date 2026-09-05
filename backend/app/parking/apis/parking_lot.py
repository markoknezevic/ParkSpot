"""HTTP routes for parking lots."""

from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.models import ParkingLot
from app.parking.schemas import ParkingLotSchema, ParkingLotSummarySchema
from app.parking.services import ParkingService

router = APIRouter(tags=["parking"])


@router.get("/parking-lots", response_model=list[ParkingLotSummarySchema])
def get_parking_lots(
    service: Annotated[ParkingService, Depends(ParkingService)],
) -> Sequence[ParkingLot]:
    """Get all parking lots with only their IDs and names."""

    return service.get_parking_lots()


@router.get(
    "/parking-lots/{parking_lot_id}",
    response_model=ParkingLotSchema,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Parking lot not found"}},
)
def get_parking_lot(
    parking_lot_id: int,
    service: Annotated[ParkingService, Depends(ParkingService)],
) -> ParkingLot:
    """Get a parking lot, all its spots, and each spot's latest status."""

    return service.get_parking_lot(parking_lot_id)
