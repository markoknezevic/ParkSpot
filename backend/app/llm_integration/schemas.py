"""Request schemas for the chat API."""

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Literal


class ChatMessageRequest(BaseModel):
    """A question across parking lots, with optional conversation context."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        str_strip_whitespace=True,
        extra="forbid",
    )

    message: str = Field(min_length=1, max_length=4000)
    conversation_id: str | None = Field(
        default=None, min_length=1, max_length=128,
        description="Reserved for future conversation history; currently requests are stateless.",
    )


class ParkingQueryArgumentsResponse(BaseModel):
    parking_lot_name: str | None
    level: int | None


class ToolCallResponse(BaseModel):
    name: Literal["get_parking_availability"]
    arguments: ParkingQueryArgumentsResponse


class ChatMessageResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    tool_call: ToolCallResponse | None = None
    message: str | None = None
