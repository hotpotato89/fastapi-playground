from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["root"])


@router.get("/")
async def root() -> RedirectResponse:
    return RedirectResponse("/docs", status_code=status.HTTP_301_MOVED_PERMANENTLY)
