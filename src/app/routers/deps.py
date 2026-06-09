from typing import Annotated, AsyncGenerator
from src.app.core import SessionLocal
from src.app.repositories import BookRepository
from src.app.services import BookService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with SessionLocal() as session:
        yield session


async def get_repo(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> BookRepository:
    return BookRepository(session)


async def get_service(
    repo: Annotated[BookRepository, Depends(get_repo)],
) -> BookService:
    return BookService(repo)
