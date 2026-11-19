"""Ask an LLM to select a parking tool without executing it."""

import json
from typing import Annotated

import httpx
from fastapi import Depends, HTTPException
from pydantic import ValidationError

from app.core import config
from app.core.http_client import get_http_client
from app.llm_integration.dtos import ToolSelectionDTO, ToolCallDTO
from app.llm_integration.utils import build_tool_selection_payload


class LLMService:
    def __init__(self, client: Annotated[httpx.AsyncClient, Depends(get_http_client)]) -> None:
        self._client = client

    async def select_tool(self, message: str) -> ToolSelectionDTO:
        """Make one model request and return its proposed tool call or text reply."""
        if not config.OPENAI_API_KEY or not config.OPENAI_MODEL:
            raise HTTPException(status_code=503, detail="Configure OPENAI_API_KEY and OPENAI_MODEL")

        try:
            response = await self._client.post(
                "https://api.openai.com/v1/responses",
                headers={"Authorization": f"Bearer {config.OPENAI_API_KEY}"},
                json=build_tool_selection_payload(message, config.OPENAI_MODEL),
                timeout=30.0,
            )
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise HTTPException(status_code=504, detail="LLM request timed out") from exc
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail="LLM request failed") from exc

        try:
            payload = response.json()
            if payload.get("status") != "completed":
                raise ValueError("Incomplete model response")
            calls = []
            texts = []
            for item in payload["output"]:
                if item["type"] == "function_call":
                    calls.append(ToolCallDTO.model_validate({
                        "name": item["name"],
                        "arguments": json.loads(item["arguments"]),
                    }))
                elif item["type"] == "message":
                    for content in item["content"]:
                        if content["type"] == "output_text":
                            texts.append(content["text"])
                        elif content["type"] == "refusal":
                            texts.append(content["refusal"])
            if len(calls) > 1:
                raise ValueError("Expected at most one tool call")
            if calls:
                return ToolSelectionDTO(tool_call=calls[0])
            text = "\n".join(texts).strip()
            if not text:
                raise ValueError("Empty model response")
            return ToolSelectionDTO(message=text)
        except (ValueError, TypeError, KeyError, AttributeError, ValidationError) as exc:
            raise HTTPException(status_code=502, detail="Invalid LLM response") from exc
