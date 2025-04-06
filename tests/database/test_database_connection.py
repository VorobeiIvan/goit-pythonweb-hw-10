import pytest
from app.database.database import get_engine, SessionLocal
from sqlalchemy.exc import OperationalError


def test_get_engine_sqlite():
    """
    Test the creation of a SQLite engine.
    """
    engine = get_engine()
    assert engine is not None
    assert "sqlite" in str(engine.url)


def test_session_local():
    """
    Test the creation of a database session.
    """
    try:
        session = SessionLocal()
        assert session is not None
        session.close()
    except OperationalError:
        pytest.fail("Failed to create a database session.")
