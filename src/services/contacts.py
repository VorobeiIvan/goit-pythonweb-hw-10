from sqlalchemy.orm import Session
from datetime import date, timedelta
from src.models.models import Contact, User


def create_contact(contact_data, current_user: User, db: Session):
    contact = Contact(**contact_data.dict(), owner_id=current_user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def get_contacts(current_user: User, db: Session):
    return db.query(Contact).filter(Contact.owner_id == current_user.id).all()


def get_upcoming_birthdays(current_user: User, db: Session):
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
