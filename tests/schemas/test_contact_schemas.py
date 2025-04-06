import pytest
from pydantic import ValidationError
from app.schemas.contact import ContactCreate
from datetime import date, timedelta
from unittest.mock import patch


def test_contact_create_valid():
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "123456789",
        "birthday": "1990-01-01",
        "additional_info": "Friend from work",
    }
    contact = ContactCreate(**data)
    assert contact.first_name == "John"
    assert contact.birthday == date(1990, 1, 1)


def test_contact_create_invalid_birthday_future():
    future_date = (date.today() + timedelta(days=1)).isoformat()
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "123456789",
        "birthday": future_date,
    }
    with pytest.raises(ValidationError) as excinfo:
        ContactCreate(**data)
    assert "Birthday cannot be in the future." in str(excinfo.value)


def test_contact_create_invalid_phone():
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "abc123",  # Invalid phone
        "birthday": "1990-01-01",
    }
    with pytest.raises(ValidationError) as excinfo:
        ContactCreate(**data)
    assert "Phone number must contain only digits and be 7-15 characters long." in str(
        excinfo.value
    )


@patch("app.schemas.contact.logger")
def test_contact_create_logging_birthday(mock_logger):
    future_date = (date.today() + timedelta(days=1)).isoformat()
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "123456789",
        "birthday": future_date,
    }
    with pytest.raises(ValidationError):
        ContactCreate(**data)
    mock_logger.warning.assert_called_once_with(
        f"Invalid birthday: {future_date} (in the future)"
    )


@patch("app.schemas.contact.logger")
def test_contact_create_logging_phone(mock_logger):
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "abc123",  # Invalid phone
        "birthday": "1990-01-01",
    }
    with pytest.raises(ValidationError):
        ContactCreate(**data)
    mock_logger.warning.assert_called_once_with("Invalid phone number: abc123")
