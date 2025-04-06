from app.utils.security import (
    verify_password,
    get_password_hash,
    create_refresh_token,
    verify_refresh_token,
)
from datetime import datetime, timedelta
from jose import jwt
from app.config import settings


def test_get_password_hash():
    password = "my_password"
    hashed_password = get_password_hash(password)
    assert hashed_password != password
    assert hashed_password.startswith("$2b$")


def test_verify_password():
    password = "my_password"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password) is True
    assert verify_password("wrong_password", hashed_password) is False


def test_create_refresh_token():
    data = {"sub": "test@example.com"}
    token = create_refresh_token(data)
    assert token is not None
    assert isinstance(token, str)


def test_verify_refresh_token():
    data = {"sub": "test@example.com"}
    token = create_refresh_token(data)
    email = verify_refresh_token(token)
    assert email == "test@example.com"

    invalid_email = verify_refresh_token("invalid_token")
    assert invalid_email is None


def test_verify_expired_refresh_token():
    # Створюємо токен із закінченим терміном дії
    data = {"sub": "test@example.com", "exp": datetime.utcnow() - timedelta(seconds=1)}
    expired_token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    email = verify_refresh_token(expired_token)
    assert email is None  # Токен має бути недійсним


def test_verify_malformed_refresh_token():
    # Передаємо некоректний токен
    malformed_token = "this.is.not.a.valid.token"
    email = verify_refresh_token(malformed_token)
    assert email is None  # Токен має бути недійсним
