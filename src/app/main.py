from fastapi import FastAPI, APIRouter

from src.app.routers import health_router

app = FastAPI(title="FastAPI playground")
main_router = APIRouter(prefix="/api")

main_router.include_router(health_router)

app.include_router(main_router)
