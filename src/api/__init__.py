from fastapi import APIRouter

from .monitoring import monitoring_router
from .auth import auth_router

router = APIRouter()

router.include_router(monitoring_router, prefix="/monitoring", tags=["Мониторинг"])
router.include_router(auth_router, prefix="/auth", tags=["Аутентификация"])


__all__ = ["router"]
