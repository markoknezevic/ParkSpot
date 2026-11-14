from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import User
from app.user.schemas import UserProfileUpdate


class UserRepository:
    def __init__(self, session: Annotated[Session, Depends(get_db)]) -> None:
        self._session = session

    def update(self, user: User, changes: UserProfileUpdate) -> User:
        if "first_name" in changes.model_fields_set:
            user.first_name = changes.first_name
        if "last_name" in changes.model_fields_set:
            user.last_name = changes.last_name
        self._session.commit()
        return user
