from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@patch("app.routers.auth.authenticate_user")
@patch("app.routers.auth.create_access_token")
def test_login_success(mock_create_access_token, mock_authenticate_user):
    mock_user = MagicMock()
    mock_user.email = "test@example.com"
    mock_authenticate_user.return_value = mock_user
    mock_create_access_token.return_value = "test_token"

    response = client.post(
        "/token",
        data={"username": "test@example.com", "password": "Password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert response.json()["refresh_token"] != ""


@patch("app.routers.auth.authenticate_user")
def test_login_invalid_credentials(mock_authenticate_user):
    mock_authenticate_user.return_value = None

    response = client.post(
        "/token",
        data={"username": "test@example.com", "password": "wrong_password"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


@patch("app.routers.auth.verify_email_token")
@patch("app.routers.auth.get_db")
def test_verify_email_success(mock_get_db, mock_verify_email_token):
    mock_verify_email_token.return_value = "test@example.com"
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db

    response = client.get("/auth/verify?token=test_token")
    assert response.status_code == 200
    assert response.json() == {"message": "Email verified successfully"}


@patch("app.routers.auth.verify_email_token")
def test_verify_email_invalid_token(mock_verify_email_token):
    mock_verify_email_token.return_value = None

    response = client.get("/auth/verify?token=invalid_token")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid or expired token"}


@patch("app.routers.users.get_current_user")
def test_rate_limiting(mock_get_current_user):
    mock_user = MagicMock()
    mock_user.email = "test@example.com"
    mock_get_current_user.return_value = mock_user

    for _ in range(5):  # Assuming the limit is 5 requests
        response = client.get("/me/")
        assert response.status_code == 200

    response = client.get("/me/")
    assert response.status_code == 429  # Too Many Requests


@patch("app.routers.users.upload_avatar_to_cloudinary")
@patch("app.routers.users.get_current_user")
def test_update_avatar(mock_get_current_user, mock_upload_avatar_to_cloudinary):
    mock_user = MagicMock()
    mock_user.email = "test@example.com"
    mock_get_current_user.return_value = mock_user
    mock_upload_avatar_to_cloudinary.return_value = "http://cloudinary.com/avatar.jpg"

    response = client.post(
        "/users/avatar",
        files={"file": ("avatar.jpg", b"fake_image_data", "image/jpeg")},
    )
    assert response.status_code == 200
    assert response.json() == {"avatar_url": "http://cloudinary.com/avatar.jpg"}


@patch("app.routers.auth.send_password_reset_email")
@patch("app.routers.auth.get_db")
def test_reset_password_request(mock_get_db, mock_send_password_reset_email):
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db
    mock_send_password_reset_email.return_value = None

    response = client.post("/auth/reset-password", json={"email": "test@example.com"})
    assert response.status_code == 200
    assert response.json() == {"message": "Password reset email sent"}
