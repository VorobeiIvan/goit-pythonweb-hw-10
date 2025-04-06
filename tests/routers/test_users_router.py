import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import MagicMock, patch
from app.models.user import User

client = TestClient(app)


@patch("app.routers.users.get_db")
def test_register_user_success(mock_get_db):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db

    mock_db.query.return_value.filter.return_value.first.return_value = None

    response = client.post(
        "/register/",
        json={
            "email": "test@example.com",
            "password": "Password123",
            "role": "user",
        },
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"


@patch("app.routers.users.get_db")
def test_register_user_already_exists(mock_get_db):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db

    mock_db.query.return_value.filter.return_value.first.return_value = User(
        email="test@example.com"
    )

    response = client.post(
        "/register/",
        json={
            "email": "test@example.com",
            "password": "Password123",
            "role": "user",
        },
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "User already exists"


@patch("app.routers.users.get_db")
def test_register_user_invalid_data(mock_get_db):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db

    response = client.post(
        "/register/",
        json={
            "email": "invalid_email",  # Некоректний email
            "password": "Password123",
            "role": "user",
        },
    )
    assert response.status_code == 422  # Unprocessable Entity


@patch("app.routers.users.get_current_user")
def test_get_current_user_info(mock_get_current_user):
    mock_user = MagicMock()
    mock_user.email = "test@example.com"
    mock_user.is_verified = True
    mock_user.id = 1
    mock_get_current_user.return_value = mock_user

    response = client.get("/me/")
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


@patch("app.routers.users.get_current_user")
def test_admin_access(mock_get_current_user):
    mock_user = MagicMock()
    mock_user.role = "admin"
    mock_get_current_user.return_value = mock_user

    response = client.get("/admin/dashboard")
    assert response.status_code == 200


@patch("app.routers.users.get_current_user")
def test_user_access_denied(mock_get_current_user):
    mock_user = MagicMock()
    mock_user.role = "user"
    mock_get_current_user.return_value = mock_user

    response = client.get("/admin/dashboard")
    assert response.status_code == 403
    assert response.json() == {"detail": "Access forbidden"}
