from passlib.context import CryptContext

"""
Модуль для хешування паролів за допомогою bcrypt.

Цей модуль:
1. Створює контекст для роботи з паролями.
2. Надає функції для хешування паролів та перевірки їхнього хешу.
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
