"""ParkSpot application entry point."""

from fastapi import FastAPI

from app.parking.apis import router as parking_router

app = FastAPI(title="ParkSpot API")
app.include_router(parking_router)
