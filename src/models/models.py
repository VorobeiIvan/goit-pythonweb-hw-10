from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import datetime

from src.database.database import Base


class User(Base):
    """
    Модель користувача.

    Атрибути:
        id (int): Унікальний ідентифікатор користувача.
        email (str): Унікальна електронна пошта користувача.
        hashed_password (str): Хешований пароль.
        is_verified (bool): Статус підтвердження електронної пошти (за замовчуванням False).
        contacts (list[Contact]): Зв'язок один-до-багатьох з контактами.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(
        String(255), unique=True, index=True, nullable=False
    )  # Максимум 255 символів для email
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)

    # Відношення "один-до-багатьох" (один користувач може мати багато контактів)
    contacts = relationship(
        "Contact", back_populates="owner", cascade="all, delete-orphan"
    )


class Contact(Base):
    """
    Модель Contact представляє контактну інформацію користувача.

    Атрибути:
        id (int): Унікальний ідентифікатор контакту.
        first_name (str): Ім'я контакту.
        last_name (str): Прізвище контакту.
        email (str): Унікальна електронна пошта контакту.
        phone (str): Номер телефону контакту.
        birthday (date): День народження контакту.
        additional_info (str, optional): Додаткова інформація.
        is_active (bool): Статус активності контакту (за замовчуванням True).
        owner_id (int): Ідентифікатор власника контакту (FK на users).
        owner (User): Відношення до власника контакту.
    """

    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(
        String(50), index=True, nullable=False
    )  # Обмеження до 50 символів
    last_name = Column(String(50), index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(
        String(15), index=True, nullable=False
    )  # 15 символів для міжнародного формату
    birthday = Column(Date, nullable=False)  # Використовуємо Date замість String
    additional_info = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)  # Статус контакту
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # Відношення "багато-до-одного" (кожен контакт має одного власника)
    owner = relationship("User", back_populates="contacts")


class BaseSchema(BaseModel):
    """
    Базова Pydantic-схема з налаштуванням ORM.
    """

    class Config:
        orm_mode = True


class ContactCreate(BaseSchema):
    """
    Схема для створення контакту (вхідні дані).
    """

    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: datetime.date
    additional_info: Optional[str] = None

    @validator("birthday")
    def validate_birthday(cls, value):
        """
        Перевіряє, чи дата народження не є майбутньою.

        :param value: Дата народження.
        :return: Валідована дата народження.
        :raises ValueError: Якщо дата є майбутньою.
        """
        if value > datetime.date.today():
            raise ValueError("Дата народження не може бути майбутньою")
        return value


class ContactResponse(ContactCreate):
    """
    Схема для відповіді з API (включає id контакту).
    """

    id: int


class ContactUpdate(BaseSchema):
    """
    Схема для оновлення контактів (вхідні дані).
    """

    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    birthday: Optional[datetime.date]
    additional_info: Optional[str]
