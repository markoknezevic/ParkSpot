"""HTTP routes for the parking module."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.parking.services import ParkingService

router = APIRouter(tags=["parking"])


@router.get("/")
async def read_root(
    service: Annotated[ParkingService, Depends(ParkingService)],
) -> dict[str, str]:
    return service.get_welcome_message()
