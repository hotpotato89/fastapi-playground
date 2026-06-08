from src.app.repositories import BookRepository
from src.app.schemas import BookCreate, BookResponse

class BookService:
    def __init__(self, repo: BookRepository) -> None:
        self.repo = repo

    async def create_book(self, book_data: BookCreate) -> BookResponse:
        return await self.repo.create(book_data)