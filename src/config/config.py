import os
from dotenv import load_dotenv, find_dotenv

"""
Модуль для завантаження змінних середовища і конфігурацій застосунку.

Цей модуль:
1. Завантажує змінні середовища з `.env` файлу.
2. Перевіряє обов'язкові змінні середовища на наявність.
3. Забезпечує доступ до ключових параметрів, таких як SECRET_KEY, ALGORITHM тощо.
"""

# Завантаження змінних середовища
load_dotenv(find_dotenv())

# Перелік необхідних змінних середовища
required_env_vars = [
    "SECRET_KEY",
    "DATABASE_URL",
    "CLOUDINARY_URL",
    "SMTP_SERVER",
    "SMTP_PORT",
]
for var in required_env_vars:
    if not os.getenv(var):
        raise EnvironmentError(
            f"❌ Змінна {var} не встановлена! Перевірте файл .env або змінні середовища."
        )

# Конфігураційні параметри
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Перевірка ALGORITHM
allowed_algorithms = {"HS256", "RS256"}
if ALGORITHM not in allowed_algorithms:
    raise ValueError(
        f"❌ ALGORITHM має бути одним із {allowed_algorithms}, отримано: {ALGORITHM}"
    )

# Логування успішного завантаження
print(
    f"✅ Конфігурація завантажена: SECRET_KEY={SECRET_KEY}, ALGORITHM={ALGORITHM}, TOKEN_EXPIRATION={ACCESS_TOKEN_EXPIRE_MINUTES} хвилин"
)
