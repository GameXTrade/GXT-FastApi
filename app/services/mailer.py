from .config import EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT, MailBody
from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP

def send_mail(data: dict | None = None):
    body = data.get("body", "")
    URL = f"http://localhost:5173/verify?token={body}"
    msg = f'''
        <div style="border: 2px solid #333; border-radius: 5px; padding: 10px; background-color: #f9f9f9; width: 300px;">
            <p style="font-size: 16px; font-weight: bold; color: #333;">Willkommen zur Registrierung!</p>
            <p style="font-size: 14px; color: #666;">Klicke unten, um dich zu registrieren:</p>
            <a href="{URL}" style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: #fff; text-decoration: none; border-radius: 5px; margin-top: 10px;">Registrieren</a>
            <p style="font-size: 12px; color: #999; margin-top: 10px;">Falls der Button nicht funktioniert, kopiere und füge den folgenden Link in deinen Browser ein: <br><br> {URL}</p>
        </div>
    '''
    message = MIMEText(msg, "html")
    message["From"] = EMAIL_HOST_USER
    message["To"] = ",".join(data["to"])
    message["Subject"] = data["subject"]

    ctx = create_default_context()

    try:
        with SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.send_message(message)
            server.quit()
        return {"status": 200, "errors": None}
    except Exception as e:
        return {"status": 500, "errors": e}