import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreate, UserRole
from unittest.mock import patch


def test_user_create_valid():
    data = {
        "email": "test@example.com",
        "password": "Password123",
        "is_active": True,
        "is_verified": False,
        "role": UserRole.USER,
    }
    user = UserCreate(**data)
    assert user.email == "test@example.com"
    assert user.password == "Password123"
    assert user.role == UserRole.USER


def test_user_create_invalid_password_short():
    data = {
        "email": "test@example.com",
        "password": "short",
    }
    with pytest.raises(ValidationError) as excinfo:
        UserCreate(**data)
    assert "Password must be at least 8 characters long." in str(excinfo.value)


def test_user_create_invalid_password_no_digit():
    data = {
        "email": "test@example.com",
        "password": "Password",
    }
    with pytest.raises(ValidationError) as excinfo:
        UserCreate(**data)
    assert "Password must contain at least one digit." in str(excinfo.value)


def test_user_create_invalid_password_no_letter():
    data = {
        "email": "test@example.com",
        "password": "12345678",
    }
    with pytest.raises(ValidationError) as excinfo:
        UserCreate(**data)
    assert "Password must contain at least one letter." in str(excinfo.value)


@patch("app.schemas.user.logger")
def test_user_create_logging_password(mock_logger):
    data = {
        "email": "test@example.com",
        "password": "short",
    }
    with pytest.raises(ValidationError):
        UserCreate(**data)
    mock_logger.warning.assert_called_once_with(
        "Password validation failed: too short."
    )
