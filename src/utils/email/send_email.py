import os
import smtplib
from email.message import EmailMessage

"""
Файл `send_email.py` містить утиліти для відправки email, включаючи верифікаційні листи.
"""


# Функція для відправки верифікаційного листа
def send_verification_email(email: str, token: str):
    """
    Відправляє верифікаційний email з токеном для підтвердження реєстрації.

    :param email: Email отримувача.
    :param token: Токен для верифікації.
    :raises RuntimeError: Якщо виникла помилка під час відправки листа.
    """
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not all([smtp_server, smtp_port, smtp_email, smtp_password]):
        raise ValueError("SMTP конфігурація відсутня у змінних середовища")

    msg = EmailMessage()
    msg["Subject"] = "Підтвердження електронної пошти"
    msg["From"] = smtp_email
    msg["To"] = email
    msg.set_content(
        f"Перейдіть за посиланням для підтвердження: http://127.0.0.1:8000/verify/{token}"
    )

    try:
        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.send_message(msg)
    except smtplib.SMTPException as e:
        raise RuntimeError(f"Не вдалося відправити верифікаційний лист: {e}")
