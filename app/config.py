from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Configuration settings for the application.

    Attributes:
        database_url (str): The database connection URL.
        mail_username (str): The username for the mail server.
        mail_password (str): The password for the mail server.
        mail_server (str): The mail server address.
        mail_port (int): The mail server port.
        mail_from (str): The email address for outgoing mails.
        secret_key (str): The secret key for JWT.
        algorithm (str): The algorithm for JWT.
        access_token_expire_minutes (int): Expiry time for access tokens.
        refresh_token_expire_days (int): Expiry time for refresh tokens.
        mail_starttls (bool): Whether to use STARTTLS for the mail server.
        mail_ssl_tls (bool): Whether to use SSL/TLS for the mail server.
    """
    database_url: str = Field(..., json_schema_extra={"env": "DATABASE_URL"})
    mail_username: str = Field(..., json_schema_extra={"env": "MAIL_USERNAME"})
    mail_password: str = Field(..., json_schema_extra={"env": "MAIL_PASSWORD"})
    mail_server: str = Field(..., json_schema_extra={"env": "MAIL_SERVER"})
    mail_port: int = Field(..., json_schema_extra={"env": "MAIL_PORT"})
    mail_from: str = Field(..., json_schema_extra={"env": "MAIL_FROM"})
    secret_key: str = Field(..., json_schema_extra={"env": "SECRET_KEY"})
    algorithm: str = Field(..., json_schema_extra={"env": "ALGORITHM"})
    access_token_expire_minutes: int = Field(..., json_schema_extra={"env": "ACCESS_TOKEN_EXPIRE_MINUTES"})
    refresh_token_expire_days: int = Field(..., json_schema_extra={"env": "REFRESH_TOKEN_EXPIRE_DAYS"})
    mail_starttls: bool = Field(..., json_schema_extra={"env": "MAIL_STARTTLS"})
    mail_ssl_tls: bool = Field(..., json_schema_extra={"env": "MAIL_SSL_TLS"})

    class Config:
        env_file = ".env"
        extra = "forbid"

# Initialize the settings object
settings = Settings()

# Print the loaded settings for verification
print("Settings loaded:", settings.model_dump())
