"""Internal tool selection models; no HTTP serialization aliases."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ParkingQueryArgumentsDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    parking_lot_name: str | None = Field(
        min_length=1, max_length=120,
        description="Parking lot name explicitly mentioned by the user, or null for all lots. Never invent a name.",
    )
    level: int | None = Field(description="Specific level, or null for all levels. Independent of the lot filter.")


class ToolCallDTO(BaseModel):
    name: Literal["get_parking_availability", "list_free_spots"]
    arguments: ParkingQueryArgumentsDTO


class ToolSelectionDTO(BaseModel):
    tool_call: ToolCallDTO | None = None
    message: str | None = None
