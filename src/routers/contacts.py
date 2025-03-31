from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import List
from src.utils.db.sessions import get_db
from src.utils.auth.auth_utils import get_current_user
from src.models.models import Contact, ContactCreate, ContactResponse, User

# Ініціалізація роутера для контактів
router = APIRouter(prefix="/contacts", tags=["Контакти"])


@router.post("/", response_model=ContactResponse)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Створює новий контакт для поточного користувача.
    """
    db_contact = Contact(**contact.dict(), owner_id=current_user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@router.get("/", response_model=List[ContactResponse])
def read_contacts(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Отримує список усіх контактів користувача.
    """
    return db.query(Contact).filter(Contact.owner_id == current_user.id).all()


@router.get("/upcoming_birthdays/", response_model=List[ContactResponse])
def get_upcoming_birthdays_for_user(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Повертає контакти з днями народження, які наближаються впродовж 7 днів.
    """
    today = date.today()
    next_week = today + timedelta(days=7)
    return (
        db.query(Contact)
        .filter(
            Contact.owner_id == current_user.id,
            Contact.birthday.between(today, next_week),
        )
        .all()
    )
