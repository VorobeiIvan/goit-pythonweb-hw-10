import sys
import os
import pytest
from fastapi.testclient import TestClient
from main import app

# Додаємо кореневу папку проекту до sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from app.database.database import (
    SessionLocal,
    Base,
    engine,
)  # Імпорт після додавання шляху


@pytest.fixture(scope="function")
def db_session():
    """
    Фікстура для створення тестової сесії бази даних.
    """
    # Створення таблиць перед тестом
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Видалення таблиць після тесту
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def test_client():
    """
    Фікстура для створення тестового клієнта FastAPI.
    """
    with TestClient(app) as client:
        yield client
