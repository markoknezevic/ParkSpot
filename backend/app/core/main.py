"""ParkSpot application entry point."""

from fastapi import FastAPI

from app.core.http_client import http_client_lifespan
from app.parking.apis import router as parking_router
from app.user.apis.user import router as user_router

app = FastAPI(title="ParkSpot API", lifespan=http_client_lifespan)
app.include_router(parking_router)
app.include_router(user_router)
