from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from app.models import User
from core.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    User repository provides all the database operations for the User model.
    """

    async def get_by_email(
        self, email: str
    ) -> User | None:
        """
        Get user by email.

        :param email: Email.
        :return: User.
        """
        return await self.get(
            email__iexact=email, limit=1
        )

    async def get_by_phone(
        self, phone: str
    ) -> User | None:
        """
        Get user by phone number.

        :param phone: Phone number.
        :return: User.
        """
        return await self.get(
            phone__iexact=phone, limit=1
        )
