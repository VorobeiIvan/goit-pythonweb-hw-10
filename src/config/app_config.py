import os
from dotenv import load_dotenv, find_dotenv

# Завантаження змінних середовища
load_dotenv(find_dotenv())

# Перелік необхідних змінних середовища
required_env_vars = [
    "SECRET_KEY",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "POSTGRES_DB",
    "CLOUDINARY_URL",
    "SMTP_SERVER",
    "SMTP_PORT",
]
for var in required_env_vars:
    if not os.getenv(var):
        raise EnvironmentError(
            f"❌ Змінна {var} не встановлена! Перевірте файл .env або змінні середовища."
        )

# Динамічне створення `DATABASE_URL`
DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

# Логування успішного завантаження
print(f"✅ DATABASE_URL сформовано: {DATABASE_URL}")

# Інші конфігураційні параметри
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
