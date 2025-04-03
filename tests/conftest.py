import os
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.database import Base
from main import app, get_db

# Mock environment variables for testing purposes
# These variables are used to configure the application during tests
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "test_secret_key"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"
os.environ["SMTP_SERVER"] = "localhost"
os.environ["SMTP_PORT"] = "587"
os.environ["SMTP_EMAIL"] = "test@example.com"
os.environ["SMTP_PASSWORD"] = "test_password"
os.environ["CLOUDINARY_CLOUD_NAME"] = "test_cloud"
os.environ["CLOUDINARY_API_KEY"] = "test_key"
os.environ["CLOUDINARY_API_SECRET"] = "test_secret"

# Create a test database in memory using SQLite
# This database is isolated and used only during tests
engine = create_engine(
    "sqlite://",  # In-memory SQLite database
    connect_args={"check_same_thread": False},  # Required for SQLite in-memory DB
    poolclass=StaticPool,  # Use a static pool to avoid connection issues
)
# Create a session factory for the test database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dictionary to store shared state for test fixtures
test_state = {}


@pytest.fixture(autouse=True)
def mock_smtp():
    """
    Fixture to mock the SMTP server.
    This prevents actual emails from being sent during tests.
    """
    with patch("smtplib.SMTP") as mock_smtp:
        mock_server = MagicMock()  # Create a mock SMTP server
        mock_smtp.return_value.__enter__.return_value = mock_server
        test_state["mock_smtp"] = mock_server  # Store the mock server in shared state
        yield mock_server  # Provide the mock server to tests


@pytest.fixture
def test_db():
    """
    Fixture to set up and tear down the test database.
    Creates all tables before the test and drops them after the test.
    """
    Base.metadata.create_all(bind=engine)  # Create tables in the test database
    try:
        db = TestingSessionLocal()  # Create a new database session
        yield db  # Provide the session to tests
    finally:
        db.close()  # Close the session
        Base.metadata.drop_all(bind=engine)  # Drop all tables after the test


@pytest.fixture
def client(test_db):
    """
    Fixture to provide a FastAPI TestClient with a mocked database dependency.
    """

    def override_get_db():
        """
        Override the `get_db` dependency to use the test database session.
        """
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db  # Override the dependency
    yield TestClient(app)  # Provide the TestClient to tests
    app.dependency_overrides.clear()  # Clear overrides after the test


@pytest.fixture
def test_user(client):
    """
    Fixture to create and verify a test user.
    Simulates the user registration and email verification process.
    """
    # User registration data
    user_data = {"email": "test@example.com", "password": "testpassword123"}
    response = client.post("/register/", params=user_data)  # Register the user
    assert response.status_code == 200  # Ensure registration was successful

    # Retrieve the verification token from the mock SMTP server
    mock_smtp = test_state["mock_smtp"]
    verification_token = (
        mock_smtp.send_message.call_args[0][0]  # Access the email message
        .get_content()  # Get the email content
        .split("/verify/")[1]  # Extract the verification token from the URL
        .strip()  # Remove any extra whitespace
    )

    # Verify the user using the extracted token
    response = client.get(f"/verify/{verification_token}")
    assert response.status_code == 200  # Ensure verification was successful

    return user_data  # Return the user data for use in tests


@pytest.fixture
def test_user_token(client, test_user):
    """
    Fixture to generate an access token for the test user.
    Simulates the login process to retrieve a valid token.
    """
    # Request an access token using the test user's credentials
    response = client.post(
        "/token",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    assert response.status_code == 200  # Ensure the token request was successful
    return response.json()["access_token"]  # Return the access token
