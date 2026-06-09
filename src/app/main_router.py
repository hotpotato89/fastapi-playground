from src.app.routers import book_router, health_router, user_router
from fastapi import APIRouter


main_router = APIRouter(prefix="/api")

main_router.include_router(health_router)
main_router.include_router(book_router)
main_router.include_router(user_router)
