from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from src.app.routers.deps import get_service
from src.app.schemas.book_schemas import BookCreate, BookResponse, BookUpdate
from src.app.services.book_service import BookService

router = APIRouter(tags=["book"], prefix="/book")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(
    service: Annotated[BookService, Depends(get_service)], upload_data: BookCreate
) -> BookResponse:
    return await service.create_book(upload_data)


@router.get("/")
async def get_all(
    service: Annotated[BookService, Depends(get_service)],
    limit: int = Query(50, ge=1, le=50, description="Limit of count on one page"),
    page: int = Query(1, ge=1, description="Page number"),
) -> list[BookResponse]:
    return await service.get_all(limit, page)


@router.get("/{book_id}")
async def get_by_id(
    service: Annotated[BookService, Depends(get_service)],
    book_id: int = Path(..., ge=1, description="Book ID"),
) -> BookResponse:
    return await service.get_by_id(book_id)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    service: Annotated[BookService, Depends(get_service)],
    book_id: int = Path(..., ge=1, description="Book ID"),
) -> None:
    return await service.delete(book_id)


@router.patch('/{book_id}')
async def update(
        service: Annotated[BookService, Depends(get_service)],
        newbook_data: BookUpdate,
        book_id: int = Path(..., ge=1, description='Book ID')
) -> BookResponse:
    return await service.update(book_id, newbook_data)
