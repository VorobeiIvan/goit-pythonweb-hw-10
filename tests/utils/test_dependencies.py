import pytest
from fastapi import HTTPException
from jose import jwt
from sqlalchemy.orm import Session
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.services.auth import SECRET_KEY, ALGORITHM


# Мок для бази даних
class MockDBSession:
    def __init__(self, users):
        self.users = users

    def query(self, model):
        return self

    def filter(self, condition):
        email = condition.right.value
        return [user for user in self.users if user.email == email]

    def first(self):
        return self.users[0] if self.users else None


# Тести
def test_get_current_user_valid_token():
    user = User(email="test@example.com")
    db = MockDBSession([user])
    token = jwt.encode({"sub": "test@example.com"}, SECRET_KEY, algorithm=ALGORITHM)

    result = get_current_user(token, db)
    assert result.email == "test@example.com"


def test_get_current_user_invalid_token():
    db = MockDBSession([])
    token = "invalid_token"

    with pytest.raises(HTTPException) as excinfo:
        get_current_user(token, db)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Invalid token"


def test_get_current_user_user_not_found():
    db = MockDBSession([])
    token = jwt.encode({"sub": "notfound@example.com"}, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        get_current_user(token, db)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Invalid token"
