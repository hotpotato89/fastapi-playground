from typing import Annotated

from fastapi import APIRouter, Depends
from src.app.routers.deps import get_service
from src.app.schemas.book_schemas import BookCreate, BookResponse
from src.app.services.book_service import BookService

router = APIRouter(tags=["book"], prefix="/book")


@router.post("/")
async def create_book(
    service: Annotated[BookService, Depends(get_service)], upload_data: BookCreate
) -> BookResponse:
    return await service.create_book(upload_data)
