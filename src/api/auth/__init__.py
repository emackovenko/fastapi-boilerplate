from fastapi import APIRouter

from .users import user_router

auth_router = APIRouter()
auth_router.include_router(user_router, tags=["Users"])

__all__ = ["auth_router"]
