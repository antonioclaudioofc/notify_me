from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    MAIL_FROM: str
    MAIL_TO: str
    MAIL_FROM_EMAIL: str
    FRONTEND_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
