"""Pydantic response schemas for the parking API."""

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class ResponseSchema(BaseModel):
    """Base schema that reads ORM models and serializes keys as camelCase."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        from_attributes=True,
        populate_by_name=True,
        serialize_by_alias=True,
    )


class SpotStatusSchema(ResponseSchema):
    """Serialize a parking spot status."""

    id: int
    name: str
    slug: str


class ParkingSpotSchema(ResponseSchema):
    """Serialize a parking spot with its latest known status."""

    id: int
    number: int
    last_status: SpotStatusSchema | None


class ParkingLotSummarySchema(ResponseSchema):
    """Serialize the identifying fields of a parking lot."""

    id: int
    name: str


class ParkingLotSchema(ResponseSchema):
    """Serialize a parking lot with all of its parking spots."""

    id: int
    name: str
    parking_spots: list[ParkingSpotSchema] = Field(default_factory=list)
