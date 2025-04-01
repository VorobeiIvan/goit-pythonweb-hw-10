from src.config.app_config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from src.config.logging_config import logger
from .security import pwd_context
from .auth import oauth2_scheme

"""
Цей модуль об'єднує глобальні константи для застосунку.

Змінні:
    SECRET_KEY (str): Секретний ключ для шифрування.
    ALGORITHM (str): Алгоритм для шифрування JWT.
    ACCESS_TOKEN_EXPIRE_MINUTES (int): Тривалість життя токена.
    logger (Logger): Об'єкт для логування.
    pwd_context (CryptContext): Контекст для хешування паролів.
    oauth2_scheme (OAuth2PasswordBearer): Схема для роботи з OAuth2 токенами.
"""

# Перевірка змінних середовища
if not SECRET_KEY:
    logger.error("❌ SECRET_KEY відсутній у конфігурації!")
    raise ValueError("SECRET_KEY обов'язковий для безпеки")

logger.info(
    f"✅ Завантажено змінні: ALGORITHM={ALGORITHM}, TOKEN_EXPIRATION={ACCESS_TOKEN_EXPIRE_MINUTES}"
)
