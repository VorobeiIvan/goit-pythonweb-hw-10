from app.core.startup import initialize_database
from unittest.mock import patch


@patch("app.core.startup.Base.metadata.create_all")
def test_initialize_database_success(mock_create_all):
    """
    Test successful database initialization.
    """
    initialize_database()
    mock_create_all.assert_called_once()


@patch("app.core.startup.Base.metadata.create_all")
def test_initialize_database_failure(mock_create_all):
    """
    Test database initialization failure.
    """
    mock_create_all.side_effect = Exception("Test exception")
    try:
        initialize_database()
    except Exception as e:
        assert str(e) == "Test exception"
