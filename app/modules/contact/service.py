from email.message import EmailMessage
import smtplib

from app.schemas.contact import RequestContact
from app.core.config import settings

class ContactService:
    async def send_message(contact: RequestContact):
        message = EmailMessage()
        message["Subject"] = f"Novo contato de {contact.name}"
        message["From"] = settings.MAIL_FROM
        message["To"] = settings.MAIL_TO

        message.set_content(f"Nome: {contact.name}\nEmail: {contact.email}\n\nMensagem:\n{contact.message}")

        if settings.SMTP_PORT == 465:
            with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.login(settings.SMTP_USER, settings.SMTP_PASS)
                server.send_message(message)
        else:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASS)
                server.send_message(message)