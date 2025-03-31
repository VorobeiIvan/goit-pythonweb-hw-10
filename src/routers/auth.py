from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from pydantic import EmailStr
from src.utils.auth.tokens import create_access_token
from src.utils.auth.auth_utils import authenticate_user
from src.utils.email.send_email import send_verification_email
from src.utils.db.sessions import get_db
from src.models.models import User
from src.constants.consts import SECRET_KEY, ALGORITHM, pwd_context

# Ініціалізація роутера для авторизації
router = APIRouter(prefix="/auth", tags=["Авторизація"])


@router.post("/register/")
def register_user(email: EmailStr, password: str, db: Session = Depends(get_db)):
    """
    Реєстрація нового користувача.
    Перевіряє унікальність email та надсилає верифікаційний лист.
    """
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=409, detail="Користувач вже існує")
    hashed_password = pwd_context.hash(password)
    user = User(email=email, hashed_password=hashed_password, is_verified=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    verification_token = create_access_token({"sub": email})
    send_verification_email(email, verification_token)
    return {
        "message": "Користувач успішно зареєстрований. Перевірте пошту для підтвердження."
    }


@router.get("/verify/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    """
    Підтверджує електронну пошту користувача за допомогою токена.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=400, detail="Недійсний токен")
        user.is_verified = True
        db.commit()
        return {"message": "Електронна пошта підтверджена"}
    except JWTError:
        raise HTTPException(status_code=400, detail="Недійсний токен")


@router.post("/login/")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Авторизує користувача та повертає токен доступу.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Недійсні облікові дані")
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
