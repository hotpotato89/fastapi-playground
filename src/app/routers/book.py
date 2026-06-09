from typing import Annotated

from fastapi import APIRouter, Depends, Query
from src.app.routers.deps import get_service
from src.app.schemas.book_schemas import BookCreate, BookResponse
from src.app.services.book_service import BookService

router = APIRouter(tags=["book"], prefix="/book")


@router.post("/")
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
