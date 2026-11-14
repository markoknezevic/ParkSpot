"""Populate the database with example parking lots and spot statuses."""

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models import ParkingLot, ParkingSpot, ParkingSpotStatus, SpotStatus


LOTS = (("Main Parking Lot", 10), ("Central Garage", 18), ("Riverside Lot", 12))


def seed(session: Session) -> None:
    if session.get_bind().dialect.name == "postgresql":
        # Serialize concurrent seed runs because lot names are not unique.
        session.execute(text("SELECT pg_advisory_xact_lock(hashtext('parkspot.seed'))"))

    statuses = []
    for name in ("Free", "Pending", "Taken"):
        status = session.scalar(select(SpotStatus).where(SpotStatus.name == name))
        if status is None:
            status = SpotStatus(name=name)
            session.add(status)
        statuses.append(status)

    for name, capacity in LOTS:
        lot = session.scalar(
            select(ParkingLot).where(ParkingLot.name == name).order_by(ParkingLot.id).limit(1)
        )
        if lot is None:
            lot = ParkingLot(name=name)
            session.add(lot)
        spots = {spot.number: spot for spot in lot.parking_spots}
        for number in range(1, capacity + 1):
            spot = spots.get(number)
            if spot is None:
                spot = ParkingSpot(parking_lot=lot, number=number)
                session.add(spot)
            if spot.level is None:
                spot.level = (number - 1) // 6
            status = statuses[(number - 1) % len(statuses)]
            if spot.last_status is not status:
                session.add(ParkingSpotStatus(parking_spot=spot, status=status))


if __name__ == "__main__":
    with SessionLocal.begin() as session:
        seed(session)
