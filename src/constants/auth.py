from fastapi.security import OAuth2PasswordBearer

"""
Цей модуль визначає константи для автентифікації у FastAPI.

Схема:
    oauth2_scheme (OAuth2PasswordBearer): Використовується для перевірки токена із заголовка Authorization.
"""

# Ініціалізація схеми OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
