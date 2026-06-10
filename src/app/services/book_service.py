from src.app.exceptions import PermissionDeniedError
from src.app.repositories import BookRepository
from src.app.schemas import BookCreate, BookResponse
from src.app.schemas.book_schemas import BookUpdate


class BookService:
    def __init__(self, repo: BookRepository) -> None:
        self.repo = repo

    async def create_book(self, book_data: BookCreate, author_id: int) -> BookResponse:
        return await self.repo.create(book_data, author_id)

    async def get_all(
        self,
        limit: int = 50,
        page: int = 1,
        genre: str | None = None,
        author_id: int | None = None,
    ) -> list[BookResponse]:
        return await self.repo.get_all(limit, page, genre, author_id)

    async def get_by_id(self, id: int) -> BookResponse:
        return await self.repo.get_by_id(id)

    async def delete(self, id: int, user_id: int) -> None:
        book = await self.repo.get_by_id(id)
        if book.author_id != user_id:
            raise PermissionDeniedError("You cannot delete another's book")
        return await self.repo.delete(id)

    async def update(
        self, user_id: int, id: int, newbook_data: BookUpdate
    ) -> BookResponse:
        book = await self.repo.get_by_id(id)
        if book.author_id != user_id:
            raise PermissionDeniedError("You cannot edit another's book")
        return await self.repo.update(id, newbook_data)
