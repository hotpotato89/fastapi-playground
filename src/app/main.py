from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.exception_handlers import register_exception_handlers
from src.app.api.routers import root_router
from src.app.core import lifespan, settings
from src.app.main_router import main_router

app = FastAPI(title="FastAPI playground", lifespan=lifespan)
register_exception_handlers(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.deploy.allow_origins,
    allow_credentials=settings.deploy.allow_credentials,
    allow_headers=settings.deploy.allow_headers,
    allow_methods=settings.deploy.allow_methods,
)

app.include_router(root_router)
app.include_router(main_router)
