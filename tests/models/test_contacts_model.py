from app.models.contacts import Contact
from datetime import datetime


def test_contact_model_defaults():
    contact = Contact(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="123456789",
        birthday=datetime(1990, 1, 1),
        owner_id=1,
    )
    assert contact.created_at is not None
    assert contact.updated_at is not None
    assert contact.owner_id == 1
