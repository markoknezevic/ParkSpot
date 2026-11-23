"""Parking service tool contracts for answering chat questions."""

from app.llm_integration.dtos import ParkingQueryArgumentsDTO

PARKING_TOOLS = [
    {
        "type": "function",
        "name": "get_parking_availability",
        "description": (
            "Get free, taken and pending spot counts grouped by parking lot and level "
            "optionally filtered by parking lot name and/or level. Use for counts, availability comparisons or finding "
            "the lot/level with the most free spaces. Set parking_lot_name to null for all lots and level to null for all levels. These filters are independent."
        ),
        "parameters": ParkingQueryArgumentsDTO.model_json_schema(),
        "strict": True,
    },
]
