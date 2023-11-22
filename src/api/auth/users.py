from typing import Callable

from fastapi import APIRouter, Depends

from app.services import AuthService, UserService
from app.models.user import User, UserPermission
from app.schemas.extras.token import Token
from app.schemas.requests.users import LoginUserRequest, RegisterUserRequest
from app.schemas.responses.users import UserResponse
from core.factory import Factory
from core.fastapi.dependencies import AuthenticationRequired
from core.fastapi.dependencies.current_user import get_current_user
from core.fastapi.dependencies.permissions import Permissions

user_router = APIRouter()


@user_router.get("/users", dependencies=[Depends(AuthenticationRequired)])
async def get_users(
    user_service: UserService = Depends(Factory().get_user_service),
    assert_access: Callable = Depends(Permissions(UserPermission.READ)),
) -> list[UserResponse]:
    users = await user_service.get_all()
    assert_access(resource=users)
    return users


@user_router.post("/signup", status_code=201)
async def register_user(
    register_user_request: RegisterUserRequest,
    auth_service: AuthService = Depends(Factory().get_auth_service),
) -> UserResponse:
    return await auth_service.register(
        email=register_user_request.email,
        phone=register_user_request.phone,
        password=register_user_request.password,
    )


@user_router.post("/signin", description="Регистрация пользователя")
async def login_user(
    login_user_request: LoginUserRequest,
    auth_service: AuthService = Depends(Factory().get_auth_service),
) -> Token:
    return await auth_service.login(
        email=login_user_request.email,
        phone=login_user_request.phone,
        password=login_user_request.password
    )


@user_router.get("/me", dependencies=[Depends(AuthenticationRequired)])
def get_user(
    user: User = Depends(get_current_user),
) -> UserResponse:
    return user
