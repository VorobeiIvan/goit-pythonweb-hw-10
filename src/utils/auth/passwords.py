from src.constants.consts import pwd_context

"""
Файл `passwords.py` містить утиліти для роботи з паролями, включаючи хешування та перевірку.
"""


# Функція для хешування пароля
def hash_password(password: str) -> str:
    """
    Хешує пароль перед збереженням у базі даних.

    :param password: Пароль у текстовому вигляді.
    :return: Хешований пароль.
    """
    return pwd_context.hash(password)


# Функція для перевірки коректності пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Перевіряє, чи відповідає хеш паролю.

    :param plain_password: Вхідний пароль користувача.
    :param hashed_password: Хешований пароль з бази даних.
    :return: True, якщо пароль коректний, інакше False.
    """
    return pwd_context.verify(plain_password, hashed_password)
