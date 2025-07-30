import os
from email.message import EmailMessage
from aiosmtplib import send
from pydantic import EmailStr
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
ADMIN_RECEIVER_EMAIL = os.getenv("ADMIN_RECEIVER_EMAIL")  # abakeadayy@gmail.com

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
