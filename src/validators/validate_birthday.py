from datetime import date
from typing import Optional


def validate_birthday(value: Optional[date]) -> Optional[date]:
    """
    Перевіряє, чи дата народження не є майбутньою.

    Args:
        value (Optional[date]): Дата народження.

    Returns:
        Optional[date]: Валідована дата народження, або None, якщо дата не вказана.

    Raises:
        ValueError: Якщо дата народження є майбутньою.
    """
    if value is None:
        return None  # Якщо дата не вказана, повертаємо None

    if value > date.today():
        raise ValueError("Дата народження не може бути майбутньою")

    return value
