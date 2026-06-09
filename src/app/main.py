from fastapi import FastAPI

from src.app.exception_handlers import register_exception_handlers
from src.app.routers import root_router
from src.app.core import lifespan
from src.app.main_router import main_router

app = FastAPI(title="FastAPI playground", lifespan=lifespan)
register_exception_handlers(app)

app.include_router(root_router)
app.include_router(main_router)
