import smtplib
import ssl
from email.message import EmailMessage
from flask import current_app


def send_email(to_email: str, subject: str, body_text: str, body_html: str | None = None) -> bool:
    cfg = current_app.config

    if not cfg.get('EMAIL_ENABLED'):
        current_app.logger.info("EMAIL_ENABLED is false; skipping email send to %s. Subject: %s", to_email, subject)
        return False

    host = cfg.get('EMAIL_SERVER')
    port = cfg.get('EMAIL_PORT')
    user = cfg.get('EMAIL_USERNAME')
    password = cfg.get('EMAIL_PASSWORD')
    sender = cfg.get('EMAIL_SENDER') or user

    if not host or not port or not user or not password or not sender:
        current_app.logger.error("Email not configured correctly; missing server/credentials")
        return False

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to_email
    if body_html:
        msg.set_content(body_text or '')
        msg.add_alternative(body_html, subtype='html')
    else:
        msg.set_content(body_text or '')

    try:
        if cfg.get('EMAIL_USE_SSL'):
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(host, port, context=context) as server:
                server.login(user, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(host, port) as server:
                if cfg.get('EMAIL_USE_TLS'):
                    server.starttls(context=ssl.create_default_context())
                server.login(user, password)
                server.send_message(msg)
        current_app.logger.info("Sent email to %s: %s", to_email, subject)
        return True
    except Exception as e:
        current_app.logger.exception("Failed to send email to %s: %s", to_email, e)
        return False
