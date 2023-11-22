from functools import partial

from fastapi import Depends

from app.services import AuthService, UserService
from app.models import User
from app.repositories import UserRepository
from core.database import get_session


class Factory:
    """
    This is the factory container that will instantiate all the services and
    repositories which can be accessed by the rest of the application.
    """

    # Repositories
    user_repository = partial(UserRepository, User)

    def get_user_service(self, db_session=Depends(get_session)):
        return UserService(
            user_repository=self.user_repository(db_session=db_session)
        )

    def get_auth_service(self, db_session=Depends(get_session)):
        return AuthService(
            user_repository=self.user_repository(db_session=db_session),
        )
