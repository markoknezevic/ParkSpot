"""Helpers for building LLM requests."""

from app.llm_integration.tools import PARKING_TOOLS


def build_tool_selection_payload(message: str, model: str) -> dict[str, object]:
    """Build the request body for selecting a parking tool."""
    return {
        "model": model,
        "instructions": (
            "You are ParkSpot's parking tool selector. Use independent parking_lot_name and level filters. "
            "If no lot is mentioned, use parking_lot_name=null (all lots). "
            "If no level is mentioned, use level=null (all levels). "
            "Copy an explicitly mentioned lot name without inventing an ID or name. "
            "Select the appropriate tool for parking data. Never invent availability "
            "or claim a tool was executed. If the request is unclear, ask for clarification "
            "in the user's language. For unrelated questions, explain your parking scope. "
            "No previous conversation is available; ask for clarification if needed."
        ),
        "input": message,
        "tools": PARKING_TOOLS,
        "tool_choice": "auto",
        "parallel_tool_calls": False,
        "store": False,
    }
