# app/utils/email.py
from email.message import EmailMessage
from aiosmtplib import send
from pydantic import EmailStr
from app.core.config import settings

SMTP_HOST = settings.SMTP_HOST
SMTP_PORT = settings.SMTP_PORT
SMTP_USER = settings.SMTP_USER
SMTP_PASSWORD = settings.SMTP_PASSWORD.get_secret_value()
ADMIN_RECEIVER_EMAIL = settings.ADMIN_RECEIVER_EMAIL

async def send_contact_email(sender_email: EmailStr, message: str):
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = ADMIN_RECEIVER_EMAIL
    msg["Subject"] = "New Contact Message from BakeADay"
    msg.set_content(f"From: {sender_email}\n\n{message}")

    await send(
        msg,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        username=SMTP_USER,
        password=SMTP_PASSWORD,
        start_tls=True,
    )
