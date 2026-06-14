from logging import getLogger
import time
from typing import Callable

from fastapi import FastAPI, Request, Response

logger = getLogger(__name__)


def register_middlewares(app: FastAPI) -> None:

    @app.middleware("http")
    async def slow_request_logging(request: Request, call_next: Callable) -> Response:
        start = time.perf_counter()

        response = await call_next(request)

        duration = time.perf_counter() - start

        if duration > 0.7:
            logger.warning(
                "Slow request: %s %s | status=%s | duration=%.3fs",
                request.method,
                request.url.path,
                response.status_code,
                duration,
            )

        return response
