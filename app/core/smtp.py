import smtplib
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr

from app.core.config import settings


def send_email(
    to: str,
    subject: str,
    html_content: str,
    from_addr: str
):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to

    msg.attach(MIMEText(html_content, "html"))

    _, sender_email = parseaddr(from_addr)

    try:
        print(f"Sending email to {to} via SMTP...", flush=True)

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.sendmail(sender_email, [to], msg.as_string())

        print(f"Email sent successfully to {to}", flush=True)
    except Exception as e:
        print(
            f"Failed to send email to {to}: {e}\n{traceback.format_exc()}",
            flush=True,
        )
        raise
