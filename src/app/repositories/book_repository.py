from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.exceptions import BookAlreadyExistsError
from src.app.schemas import BookCreate, BookResponse
from src.app.models import Book


class BookRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, book_data: BookCreate) -> BookResponse:
        new_book = Book(**book_data.model_dump())
        self.session.add(new_book)
        try:
            await self.session.commit()
            await self.session.refresh(new_book)
            return BookResponse.model_validate(new_book)
        except IntegrityError:
            await self.session.rollback()
            raise BookAlreadyExistsError("Book already exists")
