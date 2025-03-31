from datetime import datetime, timedelta
from jose import jwt
from src.constants.consts import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

"""
Файл `tokens.py` містить утиліти для роботи з JWT токенами, включаючи створення та налаштування строку життя.
"""


# Функція для створення JWT токена
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Створює новий JWT токен для аутентифікації.

    :param data: Дані, які повинні бути закодовані в токені (наприклад, email користувача).
    :param expires_delta: Час життя токену. Якщо не вказано, використовується значення за замовчуванням.
    :return: Закодований JWT токен.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
