from fastapi import FastAPI
from fastapi.testclient import TestClient
from slowapi.errors import RateLimitExceeded
from app.core.exception_handlers import add_exception_handlers


def test_rate_limit_exceeded_handler():
    """
    Test the RateLimitExceeded exception handler.
    """
    app = FastAPI()
    add_exception_handlers(app)

    @app.get("/test")
    async def test_endpoint():
        raise RateLimitExceeded("Rate limit exceeded")

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 429
    assert response.json() == {"detail": "Rate limit exceeded. Please try again later."}
