from typing import Annotated, AsyncGenerator
from src.app.core import SessionLocal
from src.app.repositories import BookRepository
from src.app.repositories.user_repository import UserRepository
from src.app.services import BookService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.app.services.user_service import UserService


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


async def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> UserService:
    return UserService(repo)
