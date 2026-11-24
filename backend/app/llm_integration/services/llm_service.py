"""Answer parking questions using database results and the LLM."""

from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import ValidationError

from app.llm_integration.dtos import ToolSelectionDTO
from app.llm_integration.llm_client import LLMClient
from app.llm_integration.utils import validate_tool_selection_payload
from app.parking.services import ParkingService


class LLMService:
    def __init__(
        self,
        client: Annotated[LLMClient, Depends(LLMClient)],
        parking_service: Annotated[ParkingService, Depends(ParkingService)],
    ) -> None:
        self._client = client
        self._parking_service = parking_service

    async def answer_message(self, message: str) -> str:
        """Select a tool, fetch parking data, and return the model's final answer."""
        selection = await self.select_tool(message)
        if selection.name is None:
            if selection.message is None:
                raise HTTPException(status_code=502, detail="Invalid LLM response")
            return selection.message

        rows = await run_in_threadpool(
            self._parking_service.get_parking_availability,
            parking_lot_name=selection.parking_lot_name,
            level=selection.level,
        )
        data = {"rows": [dict(row) for row in rows]}
        return await self.generate_answer(message, selection, data)

    async def select_tool(self, message: str) -> ToolSelectionDTO:
        """Make one model request and return its proposed tool call or text reply."""
        response = await self._client.select_tool(message)

        try:
            payload = response.json()
            calls, texts = validate_tool_selection_payload(payload)
            if calls:
                call = calls[0]
                return ToolSelectionDTO(
                    name=call["name"],
                    parking_lot_name=call["arguments"]["parking_lot_name"],
                    level=call["arguments"]["level"],
                    call_id=call["call_id"],
                    response_output=payload["output"],
                )
            return ToolSelectionDTO(message="\n".join(texts).strip())
        except (ValueError, TypeError, KeyError, AttributeError, ValidationError) as exc:
            raise HTTPException(status_code=502, detail="Invalid LLM response") from exc

    async def generate_answer(
        self, message: str, selection: ToolSelectionDTO, data: dict[str, object],
    ) -> str:
        """Call the LLM with parking data and extract the final text reply."""
        response = await self._client.generate_answer(message, selection, data)
        try:
            calls, texts = validate_tool_selection_payload(response.json())
            if calls:
                raise ValueError("Expected a final answer, not another tool call")
            return "\n".join(texts).strip()
        except (ValueError, TypeError, KeyError, AttributeError, ValidationError) as exc:
            raise HTTPException(status_code=502, detail="Invalid LLM response") from exc
