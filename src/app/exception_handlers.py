from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from src.app.exceptions import (
    BookAlreadyExistsError,
    BookNotFoundError,
    InvalidTokenError,
    ServerError,
    UserAlreadyExistsError,
    UserUnactiveError,
)
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

    @app.exception_handler(UserAlreadyExistsError)
    async def user_exists_error_handler(
        request: Request, exc: UserAlreadyExistsError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)}
        )

    @app.exception_handler(InvalidTokenError)
    async def token_error_handler(
        request: Request, exc: InvalidTokenError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(UserUnactiveError)
    async def user_unactive_error_handler(
        request: Request, exc: UserUnactiveError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN, content={"detail": str(exc)}
        )

    # Database errors

    @app.exception_handler(OperationalError)
    async def operationalerror_handler(
        request: Request, exc: OperationalError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": str(exc)},
        )

    # Server errors

    @app.exception_handler(ServerError)
    async def servererror_handler(request: Request, exc: ServerError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": str(exc)},
        )
