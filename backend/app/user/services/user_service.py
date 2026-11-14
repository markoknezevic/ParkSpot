from typing import Annotated

from fastapi import Depends

from app.models import User
from app.user.repositories.user_repository import UserRepository
from app.user.schemas import UserProfileUpdate


class UserService:
    def __init__(
        self,
        repository: Annotated[UserRepository, Depends(UserRepository)],
    ) -> None:
        self._repository = repository

    def update_profile(self, current_user: User, changes: UserProfileUpdate) -> User:
        return self._repository.update(current_user, changes)
