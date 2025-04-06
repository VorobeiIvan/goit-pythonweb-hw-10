from app.models.user import User, UserRole
from datetime import datetime


def test_user_model_defaults():
    user = User(
        email="test@example.com",
        hashed_password="hashed_password123",
    )
    assert user.is_active is True
    assert user.is_verified is False
    assert user.role == UserRole.USER
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)


def test_user_model_custom_role():
    user = User(
        email="admin@example.com",
        hashed_password="hashed_password123",
        role=UserRole.ADMIN,
    )
    assert user.role == UserRole.ADMIN
