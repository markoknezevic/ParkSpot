"""Marshmallow response schemas for the parking API."""

from marshmallow import Schema, fields


class SpotStatusSchema(Schema):
    """Serialize a parking spot's latest status history entry."""

    id = fields.Integer(attribute="status.id")
    name = fields.String(attribute="status.name")
    slug = fields.String(attribute="status.slug")
    recorded_at = fields.DateTime(attribute="created_at")


class ParkingSpotSchema(Schema):
    """Serialize a parking spot with its latest known status."""

    id = fields.Integer()
    number = fields.Integer()
    last_status = fields.Nested(SpotStatusSchema, allow_none=True)


class ParkingLotSchema(Schema):
    """Serialize a parking lot with all of its parking spots."""

    id = fields.Integer()
    name = fields.String()
    parking_spots = fields.List(fields.Nested(ParkingSpotSchema))
