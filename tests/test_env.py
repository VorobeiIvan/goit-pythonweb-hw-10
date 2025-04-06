import os
from dotenv import load_dotenv
import pytest

# Завантаження змінних середовища
load_dotenv()


def test_env_variables_exist():
    """
    Test that all required environment variables are set.
    """
    required_variables = [
        "SECRET_KEY",
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "DATABASE_URL",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_SERVER",
        "POSTGRES_PORT",
        "POSTGRES_DB",
        "ALGORITHM",
        "SMTP_SERVER",
        "SMTP_PORT",
        "SMTP_EMAIL",
        "SMTP_PASSWORD",
        "CLOUDINARY_CLOUD_NAME",
        "CLOUDINARY_API_KEY",
        "CLOUDINARY_API_SECRET",
        "REDIS_HOST",
        "REDIS_PORT",
        "REDIS_PASSWORD",
        "BASE_URL",
    ]

    for var in required_variables:
        assert os.getenv(var) is not None, f"Environment variable {var} is not set."


def test_env_variable_types():
    """
    Test that environment variables have the correct types.
    """
    assert isinstance(os.getenv("SECRET_KEY"), str)
    assert isinstance(int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")), int)
    assert isinstance(os.getenv("DATABASE_URL"), str)
    assert isinstance(os.getenv("POSTGRES_USER"), str)
    assert isinstance(os.getenv("POSTGRES_PASSWORD"), str)
    assert isinstance(os.getenv("POSTGRES_SERVER"), str)
    assert isinstance(int(os.getenv("POSTGRES_PORT")), int)
    assert isinstance(os.getenv("POSTGRES_DB"), str)
    assert isinstance(os.getenv("ALGORITHM"), str)
    assert isinstance(os.getenv("SMTP_SERVER"), str)
    assert isinstance(int(os.getenv("SMTP_PORT")), int)
    assert isinstance(os.getenv("SMTP_EMAIL"), str)
    assert isinstance(os.getenv("SMTP_PASSWORD"), str)
    assert isinstance(os.getenv("CLOUDINARY_CLOUD_NAME"), str)
    assert isinstance(os.getenv("CLOUDINARY_API_KEY"), str)
    assert isinstance(os.getenv("CLOUDINARY_API_SECRET"), str)
    assert isinstance(os.getenv("REDIS_HOST"), str)
    assert isinstance(int(os.getenv("REDIS_PORT")), int)
    assert isinstance(os.getenv("REDIS_PASSWORD"), str)
    assert isinstance(os.getenv("BASE_URL"), str)
