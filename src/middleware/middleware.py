import os
import logging
import time
from dotenv import load_dotenv
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request

"""
Файл middleware.py

Цей файл забезпечує функціонал Middleware для додатку FastAPI, включаючи перевірку змінних середовища,
логування HTTP-запитів та відповідей, а також моніторинг продуктивності.

Функціонал:
1. Перевірка ключових змінних середовища, необхідних для роботи додатку.
2. Логування вхідних HTTP-запитів із прихованими чутливими заголовками (authorization, cookie).
3. Логування статусу відповідей та часу обробки кожного запиту.
4. Гнучкість налаштувань через файл `.env` (з використанням `dotenv`).

Компоненти:
- ConfigValidationMiddleware: Middleware для перевірки конфігурацій та моніторингу запитів.
- sanitize_headers(): Допоміжна функція для приховування чутливих заголовків.
"""

# Завантаження змінних середовища з файлу .env
load_dotenv()

# Налаштування логування: рівень INFO, формат повідомлень
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def sanitize_headers(headers: dict):
    """
    Приховує чутливі заголовки у логах, щоб уникнути витоку конфіденційних даних.

    :param headers: Заголовки HTTP-запиту у вигляді словника.
    :return: Словник із прихованими значеннями для чутливих заголовків.
    """
    sensitive_keys = {"authorization", "cookie"}
    return {
        k: ("***" if k.lower() in sensitive_keys else v) for k, v in headers.items()
    }


class ConfigValidationMiddleware(BaseHTTPMiddleware):
    """
    Middleware для перевірки змінних середовища та логування запитів і відповідей.

    Цей клас забезпечує:
    1. Перевірку ключових змінних середовища, включаючи SECRET_KEY, ALGORITHM та ACCESS_TOKEN_EXPIRE_MINUTES.
    2. Логування кожного запиту та відповіді з інформацією про час обробки.
    """

    def __init__(self, app: FastAPI):
        """
        Ініціалізація Middleware.

        :param app: Екземпляр FastAPI додатку.
        """
        super().__init__(app)
        self.validate_env_variables()

    def validate_env_variables(self):
        """
        Перевіряє ключові змінні середовища на наявність і правильність.

        Перевірка включає:
        - Наявність SECRET_KEY.
        - Довжину SECRET_KEY (не менше 32 символів).
        - Валідність ALGORITHM (входить до дозволеного списку алгоритмів).
        - Валідність ACCESS_TOKEN_EXPIRE_MINUTES (додатне ціле число).

        :raises ValueError: У разі відсутності або некоректності змінних середовища.
        """
        # Отримання значень змінних середовища
        SECRET_KEY = os.getenv("SECRET_KEY")  # Секретний ключ для токенів
        ALGORITHM = os.getenv("ALGORITHM")  # Алгоритм шифрування
        ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES", "30"
        )  # Час життя токену

        # Читаємо дозволені алгоритми зі змінної середовища
        allowed_algorithms = set(
            os.getenv("ALLOWED_ALGORITHMS", "HS256,RS256").split(",")
        )

        # Перевірка SECRET_KEY
        if not SECRET_KEY:
            logging.error("❌ SECRET_KEY обов'язковий")
            raise ValueError("❌ SECRET_KEY обов'язковий")

        # Довжина SECRET_KEY
        if len(SECRET_KEY) < 32:
            logging.error("❌ SECRET_KEY має бути не менше 32 символів")
            raise ValueError("❌ SECRET_KEY має бути не менше 32 символів для безпеки")

        # Валідність ALGORITHM
        if ALGORITHM not in allowed_algorithms:
            logging.error(
                f"❌ ALGORITHM має бути одним із {allowed_algorithms}, отримано: {ALGORITHM}"
            )
            raise ValueError(f"❌ ALGORITHM має бути одним із {allowed_algorithms}")

        # Валідність ACCESS_TOKEN_EXPIRE_MINUTES
        try:
            ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)
            if ACCESS_TOKEN_EXPIRE_MINUTES <= 0:
                raise ValueError("❌ ACCESS_TOKEN_EXPIRE_MINUTES має бути більше 0")
        except ValueError:
            raise ValueError("❌ ACCESS_TOKEN_EXPIRE_MINUTES має бути цілим числом")

        # Логування успішного завантаження змінних середовища
        logging.info(
            f"✅ Завантажено змінні: ALGORITHM={ALGORITHM}, TOKEN_EXPIRATION={ACCESS_TOKEN_EXPIRE_MINUTES} хвилин"
        )

    async def dispatch(self, request: Request, call_next):
        """
        Перехоплює кожен HTTP-запит, виконує логування запиту та відповіді.

        :param request: Об'єкт HTTP-запиту.
        :param call_next: Функція для передачі запиту наступному обробнику.
        :return: HTTP-відповідь.
        """
        start_time = time.time()  # Початковий час обробки запиту

        # Логування вхідного запиту з прихованими чутливими заголовками
        logging.info(
            f"📥 Запит: {request.method} {request.url} - Headers: {sanitize_headers(dict(request.headers))}"
        )

        # Виклик наступного обробника
        response = await call_next(request)

        # Логування відповіді та часу обробки
        process_time = time.time() - start_time
        logging.info(f"📤 Відповідь: {response.status_code} (⏱ {process_time:.2f}s)")

        return response
