import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

"""
Модуль для налаштування бази даних за допомогою SQLAlchemy.

Цей модуль виконує такі функції:
1. Завантажує змінні середовища з файлу `.env`.
2. Отримує URL бази даних із середовища (змінна `DATABASE_URL`).
3. Створює двигун бази даних (`engine`) з обробкою помилок під час підключення.
4. Налаштовує фабрику сесій (`SessionLocal`) для взаємодії з базою даних.
5. Визначає базовий клас (`Base`) для створення моделей бази даних.
6. Логує успішні та помилкові операції для кращого моніторингу.
7. Додає функцію `create_engine_from_url`, що дозволяє створювати двигуни з різними параметрами.
8. Містить опціональне автоматичне створення таблиць у базі (для тестового середовища).

Залежності:
- `os` – для роботи зі змінними середовища.
- `logging` – для ведення журналу.
- `sqlalchemy` – для роботи з базою даних.
- `dotenv` – для завантаження змінних середовища з файлу `.env`.
"""

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Завантаження змінних середовища з файлу .env
load_dotenv()

# Динамічне формування DATABASE_URL
DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

# Перевірка наявності змінної DATABASE_URL
if not DATABASE_URL:
    logger.error("❌ Змінна DATABASE_URL не визначена у середовищі!")
    raise ValueError("Змінна DATABASE_URL відсутня у змінних середовища")

# Створення двигуна бази даних з обробкою помилок
try:
    # Параметр echo=False (можна змінити на True для відладки SQL-запитів)
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
    logger.info("✅ Підключення до бази даних встановлено успішно.")
except Exception as e:
    logger.error(f"❌ Помилка підключення до бази даних: {e}")
    raise RuntimeError(f"Помилка підключення до бази даних: {e}")

# Налаштування сесії SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовий клас для визначення моделей
Base = declarative_base()

# Опціональне автоматичне створення таблиць (для тестового середовища)
# Base.metadata.create_all(bind=engine)


def create_engine_from_url(database_url: str, echo: bool = False):
    """
    Створює двигун бази даних на основі наданого URL.

    :param database_url: URL для підключення до бази даних.
    :param echo: Відображати SQL-запити у логах (корисно для відладки).
    :return: Об'єкт двигуна SQLAlchemy.
    """
    if not database_url:
        logger.error("❌ Надано пустий URL бази даних.")
        raise ValueError("URL бази даних не може бути пустим")
    try:
        logger.info(f"🔄 Створення двигуна бази даних (echo={echo})...")
        return create_engine(database_url, pool_pre_ping=True, echo=echo)
    except Exception as e:
        logger.error(f"❌ Помилка створення двигуна бази даних: {e}")
        raise RuntimeError(f"Не вдалося створити двигун бази даних: {e}")
