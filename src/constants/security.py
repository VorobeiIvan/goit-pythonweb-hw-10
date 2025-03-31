from passlib.context import CryptContext

"""
Цей модуль налаштовує контекст для хешування паролів.

Контекст:
    pwd_context (CryptContext): Використовує алгоритм bcrypt для безпечного збереження паролів.
"""

# Контекст для роботи з паролями
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Функції для роботи з паролями
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Перевіряє, чи відповідає хеш паролю.

    :param plain_password: Звичайний текст пароля.
    :param hashed_password: Хешований пароль.
    :return: True, якщо паролі збігаються, інакше False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """
    Хешує пароль для збереження.

    :param password: Пароль у текстовому вигляді.
    :return: Хеш пароля.
    """
    return pwd_context.hash(password)
