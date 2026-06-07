from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["root"])


@router.get("/")
async def root():
    return RedirectResponse("/docs")
