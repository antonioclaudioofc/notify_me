import datetime 
from email.message import EmailMessage
import html
import smtplib
import pytz

from app.schemas.contact import RequestContact
from app.core.config import settings


class AntonioClaudioDevService:

    @staticmethod
    def send_message(contact: RequestContact):

        safe_message = html.escape(contact.message)

        utc_zone = pytz.utc
        sp_zone = pytz.timezone('America/Sao_Paulo')
        utc_now = datetime.datetime.now(utc_zone)

        created_at = utc_now.astimezone(sp_zone)

        formatted_date = created_at.strftime("%d/%m/%Y %H:%M")

        message = EmailMessage()
        message["Subject"] = f"Novo contato de {contact.name}"
        message["From"] = settings.MAIL_FROM_ANTONIOCLAUDIODEV
        message["To"] = settings.MAIL_TO

        message.set_content(
            f"Nome: {contact.name}\n"
            f"Email: {contact.email}\n"
            f"Recebido em: {formatted_date}\n\n"
            f"Mensagem:\n{contact.message}"
        )

        message.add_alternative(f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        </head>
        <body style="margin:0; padding:0; background-color:#f4f6f8; font-family:Arial, sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f6f8; padding:20px 0;">
            <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0"
                    style="background:#ffffff; border-radius:8px; padding:30px;">

                <tr>
                    <td align="center" style="padding-bottom:20px;">
                    <h2 style="margin:0; color:#111827;">
                        📩 Novo contato pelo portfólio
                    </h2>
                    </td>
                </tr>

                <tr>
                    <td style="font-size:15px; color:#374151; line-height:1.6;">
                    <p><strong>Nome:</strong> {contact.name}</p>

                    <p>
                        <strong>Email:</strong>
                        <a href="mailto:{contact.email}" style="color:#2563eb; text-decoration:none;">
                        {contact.email}
                        </a>
                    </p>

                    <p><strong>Recebido em:</strong> {formatted_date}</p>
                    </td>
                </tr>

                <tr>
                    <td style="padding-top:20px;">
                    <table width="100%" cellpadding="0" cellspacing="0"
                            style="background:#f9fafb; border-radius:6px; padding:20px;">
                        <tr>
                        <td style="font-size:14px; color:#374151; white-space:pre-line;">
                            <strong>Mensagem:</strong><br><br>
                            {safe_message}
                        </td>
                        </tr>
                    </table>
                    </td>
                </tr>

                <tr>
                    <td style="padding-top:30px; font-size:12px; color:#6b7280;">
                    Este e-mail foi enviado automaticamente pelo formulário do seu portfólio.
                    </td>
                </tr>

                </table>
            </td>
            </tr>
        </table>
        </body>
        </html>
        """, subtype="html")

        if settings.SMTP_PORT == 465:
            with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.login(settings.SMTP_USER, settings.SMTP_PASS)
                server.send_message(message)
        else:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASS)
                server.send_message(message)
