"""Parking service tool contracts. Chat currently selects tools without executing them."""

from app.llm_integration.dtos import ParkingQueryArgumentsDTO

PARKING_TOOLS = [
    {
        "type": "function",
        "name": "get_parking_availability",
        "description": (
            "Get free, taken, pending and unknown counts grouped by parking lot and level "
            "optionally filtered by parking lot name and/or level. Use for counts, availability comparisons or finding "
            "the lot/level with the most free spaces. Set parking_lot_name to null for all lots and level to null for all levels. These filters are independent."
        ),
        "parameters": ParkingQueryArgumentsDTO.model_json_schema(),
        "strict": True,
    },
    {
        "type": "function",
        "name": "list_free_spots",
        "description": (
            "List individual free parking spots with their lot, number and level across "
            "the requested parking lots. Use when the user wants specific spots, rather than counts. "
            "Set parking_lot_name to null for all lots and level to null for all levels. These filters are independent."
        ),
        "parameters": ParkingQueryArgumentsDTO.model_json_schema(),
        "strict": True,
    },
]
