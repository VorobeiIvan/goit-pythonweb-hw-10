from pydantic import BaseModel, EmailStr, constr, validator, Field
from datetime import date, datetime
from typing import Optional, List
from uuid import UUID
from enum import Enum
from src.validators.validate_phone_number import validate_phone_number
from src.validators.validate_birthday import validate_birthday


class ContactStatus(str, Enum):
    """
    Перелік можливих статусів контакту.
    """

    active = "active"  # Активний контакт
    inactive = "inactive"  # Неактивний контакт
    archived = "archived"  # Архівований контакт


class ContactGroup(str, Enum):
    """
    Перелік можливих груп, до яких може належати контакт.
    """

    friends = "friends"  # Друзі
    family = "family"  # Родина
    work = "work"  # Робота


class ContactBase(BaseModel):
    """
    Базова модель для представлення контакту.

    Атрибути:
        first_name (str): Ім'я контакту. Мінімум 1, максимум 100 символів.
        last_name (str): Прізвище контакту. Мінімум 1, максимум 100 символів.
        email (EmailStr): Електронна пошта контакту (автоматична перевірка валідності).
        phone_numbers (List[str]): Список телефонних номерів контакту (мінімум 1 номер).
        birthday (date): Дата народження контакту (перевіряється, щоб не була в майбутньому).
        additional_data (Optional[str]): Додаткова інформація (максимум 500 символів, необов'язкове поле).
        notes (Optional[str]): Довільні нотатки про контакт (необов'язкове поле).
        status (ContactStatus): Статус контакту (за замовчуванням "active").
        group (Optional[ContactGroup]): Група контакту (друзі, родина, робота — необов'язкове поле).
        address (Optional[str]): Адреса контакту (необов'язкове поле).
        city (Optional[str]): Місто контакту (необов'язкове поле).
        country (Optional[str]): Країна контакту (необов'язкове поле).
        created_at (datetime): Дата та час створення контакту (автоматично встановлюється при створенні).
        updated_at (datetime): Дата та час останнього оновлення контакту (автоматично оновлюється при зміні).
    """

    first_name: constr(min_length=1, max_length=100)
    last_name: constr(min_length=1, max_length=100)
    email: EmailStr
    phone_numbers: List[str]  # Список телефонних номерів
    birthday: date
    additional_data: Optional[constr(max_length=500)] = None
    notes: Optional[str] = None
    status: ContactStatus = ContactStatus.active
    group: Optional[ContactGroup] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("birthday")
    def birthday_validation(cls, value):
        """
        Валідатор для перевірки коректності дати народження.
        """
        return validate_birthday(value)

    @validator("phone_numbers", each_item=True)
    def phone_number_validation(cls, value):
        """
        Валідатор для перевірки кожного номера телефону у списку.
        """
        return validate_phone_number(value)


class ContactCreate(ContactBase):
    """
    Модель для створення нового контакту.
    Успадковує всі поля від ContactBase.
    """

    pass


class ContactResponse(ContactBase):
    """
    Розширена модель відповіді для контакту.
    """

    id: UUID  # Унікальний ідентифікатор контакту

    class Config:
        from_attributes = True  # Замість застарілого orm_mode
