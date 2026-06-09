from src.app.repositories import BookRepository
from src.app.schemas import BookCreate, BookResponse
from src.app.schemas.book_schemas import BookUpdate


class BookService:
    def __init__(self, repo: BookRepository) -> None:
        self.repo = repo

    async def create_book(self, book_data: BookCreate) -> BookResponse:
        return await self.repo.create(book_data)

    async def get_all(
        self,
        limit: int = 50,
        page: int = 1,
        genre: str | None = None,
        author: str | None = None,
    ) -> list[BookResponse]:
        fomatted_author = author.capitalize() if author else None
        return await self.repo.get_all(limit, page, genre, fomatted_author)

    async def get_by_id(self, id: int) -> BookResponse:
        return await self.repo.get_by_id(id)

    async def delete(self, id: int) -> None:
        return await self.repo.delete(id)

    async def update(self, id: int, newbook_data: BookUpdate) -> BookResponse:
        return await self.repo.update(id, newbook_data)
