"""Validate API access tokens and provision registered ParkSpot users."""

import os

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_plugin.fast_api_client import Auth0FastAPI
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import User


auth0 = Auth0FastAPI(
    domain=os.environ["AUTH0_DOMAIN"],
    audience=os.environ["AUTH0_AUDIENCE"],
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


def require_registered_user(
    claims: dict = Depends(validate_access_token),
    db: Session = Depends(get_db),
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

    user = User(auth_issuer=issuer, auth_subject=subject)
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
    db.refresh(user)
    return user
