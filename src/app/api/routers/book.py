from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from src.app.models import User
from src.app.api.deps import get_book_service, get_current_active_user
from src.app.schemas.book_schemas import BookCreate, BookResponse, BookUpdate
from src.app.services.book_service import BookService

router = APIRouter(tags=["book"], prefix="/book")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(
    service: Annotated[BookService, Depends(get_book_service)],
    upload_data: BookCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> BookResponse:
    return await service.create_book(upload_data, current_user.id)


@router.get("/")
async def get_all(
    service: Annotated[BookService, Depends(get_book_service)],
    limit: int = Query(50, ge=1, le=50, description="Limit of count on one page"),
    page: int = Query(1, ge=1, description="Page number"),
    genre: str | None = Query(None, max_length=50, description="Genre filter"),
    author_id: int | None = Query(None, ge=1, description="Author filter"),
) -> list[BookResponse]:
    return await service.get_all(limit, page, genre, author_id)


@router.get("/{book_id}")
async def get_by_id(
    service: Annotated[BookService, Depends(get_book_service)],
    book_id: int = Path(..., ge=1, description="Book ID"),
) -> BookResponse:
    return await service.get_by_id(book_id)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    service: Annotated[BookService, Depends(get_book_service)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    book_id: int = Path(..., ge=1, description="Book ID"),
) -> None:
    return await service.delete(book_id, current_user.id)


@router.patch("/{book_id}")
async def update(
    service: Annotated[BookService, Depends(get_book_service)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    newbook_data: BookUpdate,
    book_id: int = Path(..., ge=1, description="Book ID"),
) -> BookResponse:
    return await service.update(
        user_id=current_user.id, id=book_id, newbook_data=newbook_data
    )
