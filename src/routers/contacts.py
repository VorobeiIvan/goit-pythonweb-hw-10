from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.services.contacts import create_contact, get_contacts, get_upcoming_birthdays
from src.utils.auth.auth_utils import get_current_user
from src.utils.db.sessions import get_db
from src.models.models import ContactCreate, ContactResponse
from typing import List

router = APIRouter(prefix="/contacts", tags=["Контакти"])


@router.post("/", response_model=ContactResponse, status_code=201)
def create(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_contact(contact, current_user, db)


@router.get("/", response_model=List[ContactResponse])
def read_all(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_contacts(current_user, db)


@router.get("/upcoming_birthdays/", response_model=List[ContactResponse])
def upcoming(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_upcoming_birthdays(current_user, db)
