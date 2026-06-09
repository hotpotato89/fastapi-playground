from fastapi import FastAPI, APIRouter

from src.app.exception_hendlers import register_exception_handlers
from src.app.routers import health_router, root_router, book_router
from src.app.core import lifespan

app = FastAPI(title="FastAPI playground", lifespan=lifespan)
register_exception_handlers(app)
main_router = APIRouter(prefix="/api")

main_router.include_router(health_router)
main_router.include_router(book_router)
app.include_router(root_router)
app.include_router(main_router)
