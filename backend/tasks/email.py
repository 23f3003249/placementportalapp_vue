import smtplib
import os 

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = "sandbox.smtp.mailtrap.io"
SMTP_PORT = 2525

SMTP_USERNAME = os.getenv("MAILTRAP_USERNAME")
SMTP_PASSWORD = os.getenv("MAILTRAP_PASSWORD")

# print("HOST:", SMTP_HOST)
# print("PORT:", SMTP_PORT)
# print("PASS:", SMTP_PASSWORD)

def send_email(to_email, subject, body, attachment=None):


    message = MIMEMultipart()

    message['From'] = SMTP_USERNAME
    message['To'] = to_email
    message['Subject'] = subject


    message.attach(MIMEText(body, 'html'))

    if attachment:
        with open(attachment,"rb") as file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file.read())

            encoders.encode_base64(part)
            part.add_header("Content-Disposition",f'attachment; filename={os.path.basename(attachment)}')
            message.attach(part)
    try: 
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(
        SMTP_USERNAME,      # sender
        [to_email],           # receiver
        message.as_string() # email content
        )
    except Exception as e:
        print(f"Error sending email: {e}")