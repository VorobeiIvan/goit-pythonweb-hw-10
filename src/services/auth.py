from sqlalchemy.orm import Session
from fastapi import HTTPException
from jose import jwt
from src.models.models import User
from src.utils.auth.tokens import create_access_token
from src.utils.auth.auth_utils import authenticate_user
from src.utils.email.send_email import send_verification_email
from src.constants.consts import SECRET_KEY, ALGORITHM
from passlib.context import CryptContext
import os

# Ініціалізація контексту для хешування паролів
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def register_user(email: str, password: str, db: Session):
    """
    Реєструє нового користувача в системі.

    Ця функція перевіряє, чи існує користувач із заданою електронною поштою в базі даних.
    Якщо користувач вже існує, викликається виключення HTTPException зі статусом 409.
    Якщо користувач не існує, створюється новий запис у базі даних із хешованим паролем
    та статусом верифікації "не верифікований". Також генерується токен для верифікації
    електронної пошти та надсилається лист із посиланням для підтвердження.

    Параметри:
        email (str): Електронна пошта користувача.
        password (str): Пароль користувача.
        db (Session): Сесія бази даних для виконання операцій.

    Повертає:
        dict: Повідомлення про успішну реєстрацію користувача.

    Виключення:
        HTTPException: Якщо користувач із заданою електронною поштою вже існує.

    Додатково:
        - Хешування пароля виконується за допомогою `pwd_context.hash`.
        - Токен для верифікації створюється функцією `create_access_token`.
        - Лист із посиланням для верифікації надсилається функцією `send_verification_email`.
        - Базова URL-адреса береться з середовища або використовується значення за замовчуванням "http://localhost:8000".
    """
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=409, detail="Користувач вже існує")

    hashed_password = pwd_context.hash(password)
    user = User(email=email, hashed_password=hashed_password, is_verified=False)
    db.add(user)
    db.commit()
    db.refresh(user)

    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    verification_token = create_access_token({"sub": email})
    verification_url = f"{base_url}/verify/{verification_token}"

    send_verification_email(email, verification_url)

    return {"message": "Користувач успішно зареєстрований"}


def verify_email(token: str, db: Session):
    """
    Підтверджує email користувача на основі отриманого токена.

    :param token: JWT токен для підтвердження.
    :param db: Сесія бази даних.
    :return: Повідомлення про успішне підтвердження.
    """
    try:
        # Декодування токена
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if not email:
            raise HTTPException(status_code=400, detail="Недійсний токен")

        # Перевірка існування користувача
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=400, detail="Недійсний токен")

        # Підтвердження email
        user.is_verified = True
        db.commit()

        return {"message": "Електронна пошта підтверджена"}
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Недійсний токен")


def login_user(username: str, password: str, db: Session):
    """
    Авторизує користувача та повертає токен доступу.

    :param username: Email користувача.
    :param password: Пароль користувача.
    :param db: Сесія бази даних.
    :return: Токен доступу (JWT).
    """
    # Перевірка аутентифікації користувача
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Недійсні облікові дані. Перевірте email або пароль.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Генерація токена доступу
    access_token = create_access_token({"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
