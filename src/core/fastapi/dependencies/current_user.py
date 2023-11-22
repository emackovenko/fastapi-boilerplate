from fastapi import Depends, Request

from app.services.user import UserService
from core.factory import Factory


async def get_current_user(
    request: Request,
    user_service: UserService = Depends(Factory().get_user_service),
):
    return await user_service.get_by_id(request.user.id)
