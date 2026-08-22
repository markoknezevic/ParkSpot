"""HTTP routes for the parking module."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.jobs.services import JobService
from app.parking.services import ParkingService

router = APIRouter(tags=["parking"])


@router.get("/")
def read_root(
    service: Annotated[ParkingService, Depends(ParkingService)],
    job_service: Annotated[JobService, Depends(JobService)],
) -> dict[str, str]:
    job_service.schedule_hello_world()
    return service.get_welcome_message()
