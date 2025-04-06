from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from slowapi.errors import RateLimitExceeded
from app.utils.limiter import limiter

# Створення тестового додатка
app = FastAPI()
app.state.limiter = limiter


@app.get("/test")
@limiter.limit("5/minute")
async def test_endpoint():
    return {"message": "Success"}


client = TestClient(app)


def test_rate_limiter():
    # Виконуємо 5 успішних запитів
    for _ in range(5):
        response = client.get("/test")
        assert response.status_code == 200
        assert response.json() == {"message": "Success"}

    # 6-й запит повинен викликати RateLimitExceeded
    response = client.get("/test")
    assert response.status_code == 429
    assert "Rate limit exceeded" in response.text
