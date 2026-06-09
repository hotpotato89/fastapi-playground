from sqlalchemy import desc, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.exceptions import BookAlreadyExistsError, BookNotFoundError, ServerError
from src.app.schemas import BookCreate, BookResponse
from src.app.models import Book

from logging import getLogger

from src.app.schemas.book_schemas import BookUpdate

logger = getLogger(__name__)


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
            raise BookAlreadyExistsError(f"Book with title {book_data.title} already exists")

    async def get_all(self, limit: int = 50, page: int = 1) -> list[BookResponse]:
        offset = (page - 1) * limit
        query = select(Book).order_by(desc(Book.created_at)).limit(limit).offset(offset)
        result = await self.session.execute(query)
        books = result.scalars().all()
        return [BookResponse.model_validate(book) for book in books]

    async def get_by_id(self, id: int) -> BookResponse:
        result = await self.session.execute(select(Book).where(Book.id == id))
        book = result.scalar_one_or_none()
        if not book:
            raise BookNotFoundError(f"Book with id {id} does not exist")
        return BookResponse.model_validate(book)

    async def delete(self, id: int) -> None:
        book = await self.session.get(Book, id)
        if not book:
            raise BookNotFoundError(f"Book with ID {id} does not exist")
        try:
            await self.session.delete(book)
            await self.session.commit()
        except Exception as e:
            logger.error("Database error", exc_info=e)
            raise ServerError("Database error")

    async def update(self, id: int, newbook_data: BookUpdate) -> BookResponse:
        book = await self.session.get(Book, id)
        if not book:
            raise BookNotFoundError(f'Book with ID {id} does not exist')
        
        update_data = newbook_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(book, key, value)
        
        try:
            await self.session.commit()
            await self.session.refresh(book)
            return BookResponse.model_validate(book)
        except IntegrityError:
            await self.session.rollback()
            raise BookAlreadyExistsError(f"Book with title {newbook_data.title} already exists")
