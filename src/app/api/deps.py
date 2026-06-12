from typing import Annotated, Any, AsyncGenerator
from src.app.core import SessionLocal
from src.app.exceptions import InvalidTokenError, UserUnactiveError
from src.app.models import User
from src.app.repositories import BookRepository
from src.app.repositories.refresh_token_repository import RefreshTokenRepository
from src.app.repositories.user_repository import UserRepository
from src.app.services import BookService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.app.services.user_service import UserService
from src.app.utils.jwt import decode_jwt


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with SessionLocal() as session:
        yield session


async def get_book_repo(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> BookRepository:
    return BookRepository(session)


async def get_book_service(
    repo: Annotated[BookRepository, Depends(get_book_repo)],
) -> BookService:
    return BookService(repo)


async def get_user_repo(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRepository:
    return UserRepository(session)


async def get_refresh_token_repo(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> RefreshTokenRepository:
    return RefreshTokenRepository(session)


async def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repo)],
    refresh_token_repo: Annotated[
        RefreshTokenRepository, Depends(get_refresh_token_repo)
    ],
) -> UserService:
    return UserService(repo, refresh_token_repo)


async def get_token_payload(
    token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
) -> dict[str, Any]:
    return decode_jwt(token.credentials)


async def get_current_user(
    data: Annotated[dict[str, Any], Depends(get_token_payload)],
    repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> User:
    if data['type'] != 'access':
        raise InvalidTokenError('Required access token')

    user_id = data.get("user_id")
    if not user_id:
        raise InvalidTokenError("Token has no user_id")
    return await repo.get_by_id_for_auth(user_id)


async def get_current_active_user(
    user_model: Annotated[User, Depends(get_current_user)],
) -> User:
    if not user_model.is_active:
        raise UserUnactiveError("User is banned or deleted")
    return user_model
