"""Data access for the parking module."""


class ParkingRepository:
    def get_welcome_message(self) -> dict[str, str]:
        return {"message": "Hello World"}
