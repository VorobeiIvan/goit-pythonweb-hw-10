from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime
from src.utils.db.sessions import get_user
from src.constants.consts import SECRET_KEY, ALGORITHM, oauth2_scheme
import logging

"""
Файл `auth_utils.py` містить утиліти для роботи з аутентифікацією, включаючи
функцію отримання поточного користувача за токеном.
"""

# Налаштування логера
logger = logging.getLogger(__name__)


def authenticate_user(username: str, password: str) -> bool:
    """
    Автентифікація користувача за іменем користувача та паролем.

    :param username: Ім'я користувача.
    :param password: Пароль.
    :return: True, якщо автентифікація успішна, інакше False.
    """
    # Реалізація логіки автентифікації
    pass


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

        # Перевірка терміну дії токену
        exp = payload.get("exp")
        if exp and datetime.utcnow() > datetime.utcfromtimestamp(exp):
            logger.warning("❌ Токен прострочений")
            raise HTTPException(status_code=401, detail="Token has expired")

        # Отримання email з токену
        email = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )

        # Отримання користувача з бази даних
        user = get_user(db, email)
        if not user:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )

        logger.info(f"✅ Користувач успішно автентифікований: {email}")
        return user

    except JWTError as e:
        logger.error(f"❌ Невірний токен: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
