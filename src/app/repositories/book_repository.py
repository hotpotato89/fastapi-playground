from sqlalchemy import desc, select
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
            raise BookAlreadyExistsError(
                f"Book with title {book_data.title} already exists"
            )

    async def get_all(self, limit: int = 50, page: int = 1) -> list[BookResponse]:
        offset = (page - 1) * limit
        query = select(Book).order_by(desc(Book.created_at)).limit(limit).offset(offset)
        result = await self.session.execute(query)
        books = result.scalars().all()
        return [BookResponse.model_validate(book) for book in books]
