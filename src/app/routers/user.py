from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from src.app.models import User
from src.app.routers.deps import get_current_active_user, get_user_service
from src.app.schemas.user_schemas import UserLogin, UserRegister, UserResponse
from src.app.services.user_service import UserService


router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    service: Annotated[UserService, Depends(get_user_service)], userdata: UserRegister
) -> UserResponse:
    return await service.register_user(userdata)


@router.post("/login")
async def login_user(
    service: Annotated[UserService, Depends(get_user_service)], userdata: UserLogin
) -> dict[str, Any]:
    return await service.login_user(userdata)


@router.get("/me")
async def get_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    return await service.get_me(current_user)
