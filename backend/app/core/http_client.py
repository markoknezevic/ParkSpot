"""Shared outbound HTTP client for the FastAPI application."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request


@asynccontextmanager
async def http_client_lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with httpx.AsyncClient(timeout=5.0) as client:
        app.state.http_client = client
        yield


async def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client
