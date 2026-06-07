from fastapi import FastAPI, APIRouter

from src.app.routers import health_router, root_router
from src.app.core import lifespan

app = FastAPI(title="FastAPI playground", lifespan=lifespan)
main_router = APIRouter(prefix="/api")

main_router.include_router(health_router)
app.include_router(root_router)
app.include_router(main_router)
