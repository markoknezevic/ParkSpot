"""Validate API access tokens and provision registered ParkSpot users."""

import httpx
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_plugin.fast_api_client import Auth0FastAPI
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import AUTH0_AUDIENCE, AUTH0_DOMAIN
from app.core.database import get_db
from app.core.http_client import get_http_client
from app.models import User


auth0 = Auth0FastAPI(
    domain=AUTH0_DOMAIN,
    audience=AUTH0_AUDIENCE,
    dpop_enabled=False,
)
_verify_token = auth0.require_auth()
_bearer = HTTPBearer(auto_error=False)


async def validate_access_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> dict:
    """Require a bearer token and delegate cryptographic validation to Auth0."""
    if credentials is None:
        raise HTTPException(
            status_code=401, detail="Bearer access token required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await _verify_token(request)


async def fetch_auth0_email(client: httpx.AsyncClient, access_token: str, subject: str) -> str | None:
    url = f"https://{AUTH0_DOMAIN}/userinfo"
    try:
        response = await client.get(url, headers={"Authorization": f"Bearer {access_token}"})
        response.raise_for_status()
        profile = response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(status_code=502, detail="Could not retrieve Auth0 profile") from exc

    if not isinstance(profile, dict):
        raise HTTPException(status_code=502, detail="Invalid Auth0 profile")
    if profile.get("sub") != subject:
        raise HTTPException(status_code=401, detail="Auth0 user identity mismatch")
    email = profile.get("email")
    if email is not None and (not isinstance(email, str) or len(email) > 254):
        raise HTTPException(status_code=502, detail="Invalid Auth0 email")
    return email


async def require_registered_user(
    claims: dict = Depends(validate_access_token),
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    db: Session = Depends(get_db),
    client: httpx.AsyncClient = Depends(get_http_client),
) -> User:
    """Require a validated user token, creating the local user on first access."""
    issuer = claims.get("iss")
    subject = claims.get("sub")
    if not isinstance(issuer, str) or not issuer or not isinstance(subject, str) or not subject:
        raise HTTPException(
            status_code=401, detail="Invalid user identity",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if claims.get("gty") == "client-credentials" or subject.endswith("@clients"):
        raise HTTPException(status_code=403, detail="A user account is required")

    query = select(User).where(
        User.auth_issuer == issuer, User.auth_subject == subject
    )
    user = db.scalar(query)
    if user is not None:
        return user

    email = await fetch_auth0_email(client, credentials.credentials, subject)
    user = User(auth_issuer=issuer, auth_subject=subject, email=email)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # A concurrent first request may have created the same identity.
        existing_user = db.scalar(query)
        if existing_user is not None:
            return existing_user
        raise
    return user
