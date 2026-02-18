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
            "Seu cliente de email não suporta HTML. Use um cliente compatível."
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
                    style="background:#ffffff; border-radius:8px; padding:40px 30px;">

                <tr>
                    <td align="center" style="padding-bottom:20px;">
                    <h2 style="margin:0; color:#1f2937;">Arena Manager</h2>
                    </td>
                </tr>

                <tr>
                    <td style="color:#374151; font-size:16px; line-height:1.6;">
                    <p>Olá!</p>

                    <p>
                        Obrigado por criar sua conta no <strong>Arena Manager</strong>.
                    </p>

                    <p>
                        Para ativar sua conta, clique no botão abaixo:
                    </p>
                    </td>
                </tr>

                <tr>
                    <td align="center" style="padding:30px 0;">
                    <a href="{verify_url}"
                        style="background-color:#2563eb;
                                color:#ffffff;
                                text-decoration:none;
                                padding:14px 28px;
                                border-radius:6px;
                                font-weight:bold;
                                display:inline-block;">
                        Clique aqui para verificar seu e-mail
                    </a>
                    </td>
                </tr>

                <tr>
                    <td style="color:#6b7280; font-size:14px; line-height:1.6;">
                    <p>
                        Se você não criou essa conta, pode ignorar este e-mail.
                    </p>

                    <p style="margin-top:30px;">
                        © 2026 Arena Manager
                    </p>
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
