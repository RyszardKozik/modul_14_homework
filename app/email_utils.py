from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic_settings import BaseSettings
from pydantic import BaseModel, EmailStr
from fastapi_mail import ConnectionConfig
from app.config import settings

class EmailSchema(BaseModel):
    email: EmailStr

class EmailSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_FROM: str

    class Config:
        env_file = ".env"
        extra = "ignore"  

email_settings = EmailSettings()

# Configure email settings using settings from .env file
conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=settings.mail_starttls,
    MAIL_SSL_TLS=settings.mail_ssl_tls,
    USE_CREDENTIALS=True
    # TLS and SSL are managed by FastMail based on the MAIL_PORT
)

def send_reset_password_email(email_to: str, reset_link: str, background_tasks: BackgroundTasks):
    """
    Sends a password reset email.

    Args:
        email_to (str): The recipient's email address.
        reset_link (str): The password reset link.
        background_tasks (BackgroundTasks): Background tasks to handle async email sending.
    """
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email_to],
        body=f"To reset your password, click the following link: {reset_link}",
        subtype="html"
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)
