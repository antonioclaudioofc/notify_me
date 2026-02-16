from email.message import EmailMessage
import smtplib

from app.core.config import settings


class EmailService:

    @staticmethod
    def send_verification_email(user_verification):
        verify_url = f"{settings.FRONTEND_URL}/auth/verify-email?token={user_verification.token}"

        message = EmailMessage()
        message["Subject"] = "Confirme seu email - Arena Manager"
        message["From"] = settings.MAIL_FROM_EMAIL
        message["To"] = user_verification.email

        message.set_content(
            f"""
            Olá!

            Obrigado por criar sua conta no Arena Manager.

            Clique no link abaixo para validar seu email:

            {verify_url}

            Se você não criou essa conta, ignore este email.
            """
        )

        if settings.SMTP_PORT == 465:
            with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.login(settings.SMTP_USER, settings.SMTP_PASS)
                server.send_message(message)
        else:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASS)
                server.send_message(message)
