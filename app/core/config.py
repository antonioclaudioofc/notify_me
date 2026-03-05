from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    MAIL_TO: str
    MAIL_FROM_ANTONIOCLAUDIODEV: str
    MAIL_FROM_ARENAMANAGER: str
    FRONTEND_URL: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_QUEUE: str
    RABBITMQ_EXCHANGE: str

    class Config:
        env_file = ".env"


settings = Settings()
