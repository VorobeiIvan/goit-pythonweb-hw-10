from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from src.utils.db.sessions import get_user
from src.constants.consts import SECRET_KEY, ALGORITHM, oauth2_scheme

"""
Файл `auth_utils.py` містить утиліти для роботи з аутентифікацією, включаючи
функцію отримання поточного користувача за токеном.
"""


# Функція для отримання поточного користувача на основі токену
def get_current_user(
    db: Session = Depends(get_user), token: str = Depends(oauth2_scheme)
):
    """
    Отримує поточного користувача на основі токену.

    :param db: Сесія бази даних.
    :param token: JWT токен.
    :return: Поточний користувач (об'єкт User).
    :raises HTTPException: Якщо токен недійсний або користувач не знайдений.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )

        user = get_user(db, email)
        if not user:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )

        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
