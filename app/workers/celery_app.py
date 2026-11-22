import smtplib
import ssl
from celery import Celery
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from core.config import settings
from fastapi import Jinja2Templates

SENDER = settings.SENDER
SMTP_URL = settings.SMTP_URL
EMAIL = settings.EMAIL
PASSWORD = settings.PASSWORD
REDIS_URL = settings.REDIS_URL

back_redis = "redis://localhost:6379/1"

celery = Celery("testing_kod",
                broker=REDIS_URL,
                backend=back_redis,
                
                )

message = MIMEMultipart("alternative")

templates = Jinja2Templates(directory = "app/templates")
@celery.task(
        bind=True,
        max_retries = 3,
        default_retry_delay = 10
)
def send_message(self,email,username, code, body, template_name):
    """Таск для отправки сообщения"""
    
    try:
        template = templates.get_template(template_name)
        message = MIMEMultipart("alternative")
        message["Subject"] = body
        message["From"] = SENDER
        message["To"] = email

        html_content = template.render(code = code, username = username,body=body, expire_minutes = 5)
        message.attach(MIMEText(html_content, "html","utf-8"))
        
        with smtplib.SMTP_SSL(SMTP_URL,465, context = ssl.create_default_context()) as server:
            server.login(EMAIL,PASSWORD)
            server.send_message(message)
    
    except Exception as ex:
        raise self.retry(exc=ex)
    
    return {"message":"Сообщение для регистрации отправлено"}