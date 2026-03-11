import datetime
import html

import pytz

from app.core.config import settings
from app.core.smtp import send_email
from app.schemas.contact import RequestContact
from app.services.antonio_claudio_dev.email_service import EmailService


class AntonioClaudioDevEmailService(EmailService):

    def send_message_from_payload(self, payload: dict):
        contact = RequestContact.model_validate(payload)
        self.send_message(contact)

    def send_message(self, contact: RequestContact):
        safe_message = html.escape(contact.message)

        utc_zone = pytz.utc
        sp_zone = pytz.timezone('America/Sao_Paulo')
        utc_now = datetime.datetime.now(utc_zone)

        created_at = utc_now.astimezone(sp_zone)
        formatted_date = created_at.strftime("%d/%m/%Y %H:%M")

        html_content = f"""
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
                        Novo contato pelo portfolio
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
                    Este e-mail foi enviado automaticamente pelo formulario do seu portfolio.
                    </td>
                </tr>

                </table>
            </td>
            </tr>
        </table>
        </body>
        </html>"""

        send_email(
            to=settings.MAIL_TO,
            subject=f"Novo contato de {contact.name}",
            html_content=html_content,
            from_addr=settings.MAIL_FROM_ANTONIOCLAUDIODEV,
        )
