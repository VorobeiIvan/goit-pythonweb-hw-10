import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import MagicMock, patch
from app.models.contacts import Contact

client = TestClient(app)


@patch("app.routers.contacts.get_db")
def test_create_contact(mock_get_db):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db

    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None

    response = client.post(
        "/contacts/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "123456789",
            "birthday": "1990-01-01",
        },
    )
    assert response.status_code == 201


@patch("app.routers.contacts.get_db")
def test_get_contacts(mock_get_db):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db

    mock_db.query.return_value.filter.return_value.all.return_value = [
        Contact(id=1, first_name="John", last_name="Doe", email="john.doe@example.com")
    ]

    response = client.get("/contacts/")
    assert response.status_code == 200
    assert len(response.json()) == 1


@patch("app.routers.contacts.get_db")
def test_get_contact_by_id(mock_get_db):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db

    mock_db.query.return_value.filter.return_value.first.return_value = Contact(
        id=1, first_name="John", last_name="Doe", email="john.doe@example.com"
    )

    response = client.get("/contacts/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import MagicMock, patch
from app.models.contacts import Contact

client = TestClient(app)


@patch("app.routers.contacts.get_db")
def test_search_contacts(mock_get_db):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db

    mock_db.query.return_value.filter.return_value.all.return_value = [
        Contact(id=1, first_name="John", last_name="Doe", email="john.doe@example.com")
    ]

    response = client.get("/contacts/search?query=John")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["first_name"] == "John"


@patch("app.routers.contacts.get_db")
def test_get_upcoming_birthdays(mock_get_db):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db

    mock_db.query.return_value.filter.return_value.all.return_value = [
        Contact(id=1, first_name="Jane", last_name="Doe", email="jane.doe@example.com")
    ]

    response = client.get("/contacts/birthdays")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["first_name"] == "Jane"
