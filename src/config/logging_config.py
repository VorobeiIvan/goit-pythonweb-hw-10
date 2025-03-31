import logging
import os

"""
Модуль для налаштування логера.

Цей модуль:
1. Забезпечує налаштування рівня логування.
2. Забезпечує зручний доступ до логера для відстеження подій у програмі.
"""

# Налаштування рівня логування
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Базове налаштування логера
logging.basicConfig(
    filename="app.log",  # Збереження логів у файл
    level=LOG_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Повідомлення про успішну конфігурацію логера
logger.info(f"✅ Логер налаштовано на рівень {LOG_LEVEL}")
