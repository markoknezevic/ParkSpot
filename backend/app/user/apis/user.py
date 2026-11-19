from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.auth import require_registered_user
from app.models import User
from app.user.schemas import UserProfile, UserProfileUpdate
from app.user.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserProfile)
def get_current_user(
    current_user: Annotated[User, Depends(require_registered_user)],
) -> User:
    return current_user


@router.patch("/me", response_model=UserProfile)
def update_current_user(
    changes: UserProfileUpdate,
    current_user: Annotated[User, Depends(require_registered_user)],
    service: Annotated[UserService, Depends(UserService)],
) -> User:
    return service.update_profile(current_user, changes)
