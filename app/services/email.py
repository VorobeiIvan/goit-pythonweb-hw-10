import smtplib
from email.message import EmailMessage
import os
import logging

# Налаштування логування
logger = logging.getLogger(__name__)

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


def send_verification_email(email: str, token: str):
    """
    Send a verification email to the user.

    Args:
        email (str): The recipient's email address.
        token (str): The verification token.
    """
    verification_url = f"{BASE_URL}/verify/{token}"
    msg = EmailMessage()
    msg["Subject"] = "Verify your email"
    msg["From"] = os.getenv("SMTP_EMAIL")
    msg["To"] = email
    msg.set_content(
        f"Please verify your email by clicking the link: {verification_url}"
    )

    try:
        with smtplib.SMTP(
            os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))
        ) as server:
            server.starttls()
            server.login(os.getenv("SMTP_EMAIL"), os.getenv("SMTP_PASSWORD"))
            server.send_message(msg)
        logger.info(f"Verification email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send verification email to {email}: {e}")


def send_password_reset_email(email: str, token: str):
    """
    Send a password reset email to the user.

    Args:
        email (str): The recipient's email address.
        token (str): The password reset token.
    """
    reset_url = f"{BASE_URL}/reset-password/{token}"
    msg = EmailMessage()
    msg["Subject"] = "Reset your password"
    msg["From"] = os.getenv("SMTP_EMAIL")
    msg["To"] = email
    msg.set_content(f"Click the link to reset your password: {reset_url}")

    try:
        with smtplib.SMTP(
            os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))
        ) as server:
            server.starttls()
            server.login(os.getenv("SMTP_EMAIL"), os.getenv("SMTP_PASSWORD"))
            server.send_message(msg)
        logger.info(f"Password reset email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send password reset email to {email}: {e}")
