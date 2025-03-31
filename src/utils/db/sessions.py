from contextlib import contextmanager
from sqlalchemy.orm import Session
from src.database.database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError

"""
Файл `sessions.py` забезпечує утиліти для роботи з сесіями бази даних.
"""


# Контекстний менеджер для створення сесій бази даних
@contextmanager
def get_db() -> Session:
    """
    Контекстний менеджер для створення та закриття сесій бази даних.

    :return: Сесія бази даних.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Отримання користувача з бази даних
def get_user(db: Session, email: str):
    """
    Отримує користувача з бази даних за email.

    :param db: Сесія бази даних.
    :param email: Email користувача.
    :return: Користувач, якщо знайдений.
    """
    return db.query(User).filter(User.email == email).first()
