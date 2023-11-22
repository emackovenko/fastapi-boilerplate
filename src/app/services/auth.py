from pydantic import EmailStr

from app.models import User
from app.repositories import UserRepository
from app.schemas.extras.token import Token
from core.service import BaseService
from core.exceptions import BadRequestException, UnauthorizedException
from core.security import JWTHandler, PasswordHandler


class AuthService(BaseService[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    async def register(self, password: str, email: EmailStr | None = None, phone: str | None = None) -> User:

        user: User = None

        if email:
            user = await self.user_repository.get_by_email(email)
        if phone:
            if not user:
                user = await self.user_repository.get_by_phone(phone)
        if user:
            raise BadRequestException(
                "Пользователь с такими данными уже существует"
            )

        password = PasswordHandler.hash(password)
        return await self.user_repository.create(
            email=email,
            phone=phone,
            password=password,
        )

    async def login(self, password: str, email: EmailStr | None = None, phone: str | None = None) -> Token:
        user = None
        if email:
            user = await self.user_repository.get_by_email(email)
        elif phone:
            user = await self.user_repository.get_by_phone(phone)

        if not user:
            raise BadRequestException("Пользователь с логином и паролем не найден")

        if not PasswordHandler.verify(user.password, password):
            raise BadRequestException("Пользователь с логином и паролем не найден")

        return Token(
            access_token=JWTHandler.encode(payload={"user_id": user.id}),
            refresh_token=JWTHandler.encode(payload={"sub": "refresh_token"}),
        )

    async def refresh_token(self, access_token: str, refresh_token: str) -> Token:
        token = JWTHandler.decode(access_token)
        refresh_token = JWTHandler.decode(refresh_token)
        if refresh_token.get("sub") != "refresh_token":
            raise UnauthorizedException("Invalid refresh token")

        return Token(
            access_token=JWTHandler.encode(payload={"user_id": token.get("user_id")}),
            refresh_token=JWTHandler.encode(payload={"sub": "refresh_token"}),
        )


class AuthBackendAdminService:
    """Not yet implemented"""
