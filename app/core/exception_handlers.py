from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
import logging

# Налаштування логування
logger = logging.getLogger(__name__)


def add_exception_handlers(app: FastAPI):
    """
    Add custom exception handlers to the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
        """
        Handle RateLimitExceeded exceptions.

        Args:
            request (Request): The incoming HTTP request.
            exc (RateLimitExceeded): The exception instance.

        Returns:
            JSONResponse: A JSON response with a 429 status code.
        """
        logger.warning(f"Rate limit exceeded for request: {request.url}")
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded. Please try again later."},
        )
