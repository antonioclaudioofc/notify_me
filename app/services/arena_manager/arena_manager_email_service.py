import html
import datetime

import pytz

from app.core.config import settings
from app.core.smtp import send_email
from app.services.arena_manager.email_service import EmailService


class ArenaManagerEmailService(EmailService):

    def send_verification_email(self, data: dict):
        verify_url = f"{settings.FRONTEND_URL}/auth/verify-email?token={data['token']}"

        utc_zone = pytz.utc
        sp_zone = pytz.timezone('America/Sao_Paulo')
        utc_now = datetime.datetime.now(utc_zone)
        created_at = utc_now.astimezone(sp_zone)
        formatted_date = created_at.strftime("%d/%m/%Y %H:%M")

        safe_email = html.escape(data['email'])

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

                        <p><strong>Email:</strong> {safe_email}</p>
                        <p><strong>Solicitado em:</strong> {formatted_date}</p>
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
            </html>"""

        send_email(
            to=data['email'],
            subject="Confirme seu email - Arena Manager",
            html_content=html_content,
            from_addr=settings.MAIL_FROM_ARENAMANAGER,
        )

    def send_owner_promotion_email(self, user: dict, arena: dict):
        utc_zone = pytz.utc
        sp_zone = pytz.timezone('America/Sao_Paulo')
        utc_now = datetime.datetime.now(utc_zone)
        created_at = utc_now.astimezone(sp_zone)
        formatted_date = created_at.strftime("%d/%m/%Y %H:%M")

        safe_name = html.escape(user["name"])
        safe_arena = html.escape(arena["name"])

        html_content = f"""
            <!DOCTYPE html>
            <html>
            <body style="font-family:Arial, sans-serif; background:#f4f6f8; padding:20px;">
            <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                <td align="center">
                    <table width="600" style="background:#ffffff; padding:30px; border-radius:8px;">

                    <tr>
                        <td align="center">
                        <h2 style="color:#2563eb;">Arena Manager</h2>
                        </td>
                    </tr>

                    <tr>
                        <td>
                        <h3>🎉 Parabéns, {safe_name}!</h3>

                        <p>
                            Sua arena <strong>{safe_arena}</strong> foi criada com sucesso.
                        </p>

                        <p>
                            Agora você possui acesso completo para gerenciar:
                        </p>

                        <ul>
                            <li>Horários e reservas</li>
                            <li>Usuários</li>
                            <li>Pagamentos</li>
                            <li>Relatórios</li>
                        </ul>

                        <p>
                            Estamos felizes em ter você conosco 🚀
                        </p>

                        <p><strong>Data:</strong> {formatted_date}</p>
                        </td>
                    </tr>

                    <tr>
                        <td style="padding-top:20px; color:#6b7280; font-size:12px;">
                        © 2026 Arena Manager
                        </td>
                    </tr>

                    </table>
                </td>
                </tr>
            </table>
            </body>
            </html>"""

        send_email(
            to=user["email"],
            subject="Parabéns! Você agora é dono de uma arena",
            html_content=html_content,
            from_addr=settings.MAIL_FROM_ARENAMANAGER,
        )

    def send_new_court_email(self, user: dict, arena: dict, court: dict):
        utc_zone = pytz.utc
        sp_zone = pytz.timezone('America/Sao_Paulo')
        utc_now = datetime.datetime.now(utc_zone)
        created_at = utc_now.astimezone(sp_zone)
        formatted_date = created_at.strftime("%d/%m/%Y %H:%M")

        safe_name = html.escape(user["name"])
        safe_arena = html.escape(arena["name"])
        safe_court = html.escape(court["name"])

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family:Arial, sans-serif; background:#f4f6f8; padding:20px;">
        <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
            <td align="center">
                <table width="600" style="background:#ffffff; padding:30px; border-radius:8px;">

                <tr>
                    <td align="center">
                    <h2 style="color:#2563eb;">Arena Manager</h2>
                    </td>
                </tr>

                <tr>
                    <td>
                    <h3>🏟️ Nova quadra criada!</h3>

                    <p>
                        Olá <strong>{safe_name}</strong>,
                    </p>

                    <p>
                        A quadra <strong>{safe_court}</strong> foi adicionada com sucesso na sua arena 
                        <strong>{safe_arena}</strong>.
                    </p>

                    <p>
                        Ela já está disponível para reservas no sistema. Agora você pode:
                    </p>

                    <ul>
                        <li>Definir horários e disponibilidade</li>
                        <li>Configurar preços</li>
                        <li>Gerenciar reservas</li>
                        <li>Acompanhar o desempenho da quadra</li>
                    </ul>

                    <p>
                        Continue gerenciando sua arena e oferecendo a melhor experiência para seus clientes 🚀
                    </p>

                    <p><strong>Data:</strong> {formatted_date}</p>
                    </td>
                </tr>

                <tr>
                    <td style="padding-top:20px; color:#6b7280; font-size:12px;">
                    © 2026 Arena Manager
                    </td>
                </tr>

                </table>
            </td>
            </tr>
        </table>
        </body>
        </html>"""

        send_email(
            to=user["email"],
            subject=f"Nova quadra adicionada na arena {arena['name']}",
            html_content=html_content,
            from_addr=settings.MAIL_FROM_ARENAMANAGER,
        )

    def send_reservation_created_email(self, data: dict):
        print(
            f"Reservation created email not yet implemented. Data: {data}", flush=True
        )

    def send_reservation_cancelled_email(self, data: dict):
        print(
            f"Reservation cancelled email not yet implemented. Data: {data}", flush=True
        )
