from src.app.repositories import BookRepository
from src.app.schemas import BookCreate, BookResponse


class BookService:
    def __init__(self, repo: BookRepository) -> None:
        self.repo = repo

    async def create_book(self, book_data: BookCreate) -> BookResponse:
        return await self.repo.create(book_data)

    async def get_all(self, limit: int = 50, page: int = 1) -> list[BookResponse]:
        return await self.repo.get_all(limit, page)

    async def get_by_id(self, id: int) -> BookResponse:
        return await self.repo.get_by_id(id)

    async def delete(self, id: int) -> None:
        return await self.repo.delete(id)
