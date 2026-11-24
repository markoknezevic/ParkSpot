"""HTTP routes for chat messages."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.auth import require_registered_user
from app.llm_integration.schemas import (
    ChatMessageRequest,
    ChatMessageResponse,
)
from app.llm_integration.services import LLMService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post(
    "/messages",
    response_model=ChatMessageResponse,
    dependencies=[Depends(require_registered_user)],
    responses={
        404: {"description": "Parking lot not found"},
        409: {"description": "Parking lot name is ambiguous"},
        502: {"description": "LLM request failed or returned an invalid response"},
        503: {"description": "LLM is not configured"},
        504: {"description": "LLM request timed out"},
    },
)
async def send_message(
    message: ChatMessageRequest,
    service: Annotated[LLMService, Depends(LLMService)],
) -> ChatMessageResponse:
    """Answer a parking question using the database and the LLM."""

    answer = await service.answer_message(message.message)
    return ChatMessageResponse(message=answer)
