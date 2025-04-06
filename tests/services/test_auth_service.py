from app.services.auth import (
    verify_password,
    get_password_hash,
    authenticate_user,
    create_access_token,
)
from unittest.mock import MagicMock
from datetime import timedelta
from jose import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = "HS256"


def test_verify_password():
    password = "my_password"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password) is True
    assert verify_password("wrong_password", hashed_password) is False


def test_authenticate_user():
    mock_db = MagicMock()
    mock_user = MagicMock()
    mock_user.email = "test@example.com"
    mock_user.hashed_password = get_password_hash("my_password")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    user = authenticate_user(mock_db, "test@example.com", "my_password")
    assert user.email == "test@example.com"

    user = authenticate_user(mock_db, "test@example.com", "wrong_password")
    assert user is None

    user = authenticate_user(mock_db, "notfound@example.com", "my_password")
    assert user is None


def test_create_access_token():
    data = {"sub": "test@example.com"}
    token = create_access_token(data, expires_delta=timedelta(minutes=15))
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_data["sub"] == "test@example.com"
