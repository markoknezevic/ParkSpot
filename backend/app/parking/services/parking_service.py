"""Business logic for the parking module."""

from typing import Annotated

from fastapi import Depends

from app.parking.repositories import ParkingRepository


class ParkingService:
    def __init__(
        self,
        repository: Annotated[ParkingRepository, Depends(ParkingRepository)],
    ) -> None:
        self._repository = repository

    def get_welcome_message(self) -> dict[str, str]:
        return self._repository.get_welcome_message()
