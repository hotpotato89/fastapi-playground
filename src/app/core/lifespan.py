from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.app.core import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.engine = engine

    yield

    await app.state.engine.dispose()
