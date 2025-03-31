from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.services.auth import register_user, login_user, verify_email
from src.utils.db.sessions import get_db
from pydantic import EmailStr
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Авторизація"])


@router.post("/register/", status_code=201)
def register(email: EmailStr, password: str, db: Session = Depends(get_db)):
    return register_user(email, password, db)


@router.get("/verify/{token}")
def verify(token: str, db: Session = Depends(get_db)):
    return verify_email(token, db)


@router.post("/login/")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    return login_user(form_data.username, form_data.password, db)
