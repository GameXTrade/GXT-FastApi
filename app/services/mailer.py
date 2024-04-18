from .config import EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT, MailBody
from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP

def send_mail(data: dict, template="register"):
    body = data.get("body", "")

    URL = f"http://localhost:5173/verify"
    if template=="login":   
        URL += f"?token={body}"

    message_subject = "Willkommen zur Registrierung!" if template == "register" else "Logge dich jetzt ein."
    button_text = "Registrieren" if template == "register" else "Einloggen"
    msg = f'''
        <div style="border: 2px solid #333; border-radius: 5px; padding: 10px; background-color: #f9f9f9; width: 300px;">
            <p style="font-size: 16px; font-weight: bold; color: #333;">{message_subject}</p>
            <a href="{URL}" style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: #fff; text-decoration: none; border-radius: 5px; margin-top: 10px;">{button_text}</a>
            <p style="font-size: 12px; color: #999; margin-top: 10px;">Falls der Knopf nicht funktioniert, kopiere und füge den folgenden Link in deinen Browser ein: <br><br> {URL}</p>
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