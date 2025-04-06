import pytest
import json
from unittest.mock import MagicMock, patch
from app.services.redis_cache import cache_user, get_cached_user


@patch("app.services.cache.redis_cache")
def test_cache_user(mock_redis_cache):
    email = "test@example.com"
    user_data = {"name": "Test User", "email": email}

    # Виклик функції
    cache_user(email, user_data, expiration_minutes=30)

    # Перевірка, що setex викликано з правильними аргументами
    mock_redis_cache.setex.assert_called_once_with(
        f"user:{email}", 30 * 60, json.dumps(user_data)  # 30 хвилин у секундах
    )


@patch("app.services.cache.redis_cache")
def test_get_cached_user_hit(mock_redis_cache):
    email = "test@example.com"
    user_data = {"name": "Test User", "email": email}
    mock_redis_cache.get.return_value = json.dumps(user_data)

    # Виклик функції
    result = get_cached_user(email)

    # Перевірка результату
    assert result == user_data
    mock_redis_cache.get.assert_called_once_with(f"user:{email}")


@patch("app.services.cache.redis_cache")
def test_get_cached_user_miss(mock_redis_cache):
    email = "test@example.com"
    mock_redis_cache.get.return_value = None

    # Виклик функції
    result = get_cached_user(email)

    # Перевірка результату
    assert result is None
    mock_redis_cache.get.assert_called_once_with(f"user:{email}")


@patch("app.services.cache.redis_cache")
def test_cache_user_invalid_data(mock_redis_cache):
    # Некоректні дані
    email = None
    user_data = None

    # Виклик функції
    with pytest.raises(ValueError):
        cache_user(email, user_data, expiration_minutes=30)


@patch("app.services.cache.redis_cache")
def test_get_cached_user_redis_error(mock_redis_cache):
    email = "test@example.com"
    mock_redis_cache.get.side_effect = Exception("Redis connection error")

    # Виклик функції
    result = get_cached_user(email)

    # Перевірка, що результат None при помилці Redis
    assert result is None
    mock_redis_cache.get.assert_called_once_with(f"user:{email}")
