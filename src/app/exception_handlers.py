from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from src.app.exceptions import BookAlreadyExistsError, BookNotFoundError
from sqlalchemy.exc import OperationalError


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(BookAlreadyExistsError)
    async def conflict_handler(
        request: Request, exc: BookAlreadyExistsError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)}
        )

    @app.exception_handler(BookNotFoundError)
    async def not_found_error_handler(
        request: Request, exc: BookNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
        )

    # Database errors

    @app.exception_handler(OperationalError)
    async def database_error_handler(
        request: Request, exc: OperationalError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": str(exc)},
        )
