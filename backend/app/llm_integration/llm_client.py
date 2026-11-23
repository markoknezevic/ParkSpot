"""HTTP client for LLM tool selection and final answers."""

from typing import Annotated

import httpx
from fastapi import Depends, HTTPException

from app.core import config
from app.core.http_client import get_http_client
from app.llm_integration.dtos import ToolSelectionDTO
from app.llm_integration.utils import build_answer_payload, build_tool_selection_payload


class LLMClient:
    def __init__(self, client: Annotated[httpx.AsyncClient, Depends(get_http_client)]) -> None:
        self._client = client

    async def select_tool(self, message: str) -> httpx.Response:
        """Ask the model which parking function to call."""
        return await self._post(build_tool_selection_payload(message, config.OPENAI_MODEL))

    async def generate_answer(
        self, message: str, selection: ToolSelectionDTO, data: dict[str, object],
    ) -> httpx.Response:
        """Send the database result to the model for a final answer."""
        return await self._post(build_answer_payload(message, selection, data, config.OPENAI_MODEL))

    async def _post(self, payload: dict[str, object]) -> httpx.Response:
        """Send a Responses API request and translate upstream HTTP errors."""
        if not config.OPENAI_API_KEY or not config.OPENAI_MODEL:
            raise HTTPException(status_code=503, detail="Configure OPENAI_API_KEY and OPENAI_MODEL")

        try:
            response = await self._client.post(
                "https://api.openai.com/v1/responses",
                headers={"Authorization": f"Bearer {config.OPENAI_API_KEY}"},
                json=payload,
                timeout=30.0,
            )
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise HTTPException(status_code=504, detail="LLM request timed out") from exc
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail="LLM request failed") from exc

        return response
