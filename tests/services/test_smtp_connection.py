from unittest.mock import patch, MagicMock
from app.services.email import send_verification_email, send_password_reset_email


@patch("smtplib.SMTP")
def test_send_verification_email(mock_smtp):
    mock_server = MagicMock()
    mock_smtp.return_value = mock_server

    email = "test@example.com"
    token = "test_token"
    send_verification_email(email, token)

    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once()
    mock_server.send_message.assert_called_once()


@patch("smtplib.SMTP")
def test_send_password_reset_email(mock_smtp):
    mock_server = MagicMock()
    mock_smtp.return_value = mock_server

    email = "test@example.com"
    token = "reset_token"
    send_password_reset_email(email, token)

    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once()
    mock_server.send_message.assert_called_once()
