from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    RESEND_API_KEY: str
    MAIL_TO: str
    MAIL_FROM_ANTONIOCLAUDIODEV: str
    MAIL_FROM_ARENAMANAGER: str
    FRONTEND_URL: str
    RABBITMQ_URL: str

    RABBITMQ_ARENA_MANAGER_QUEUE: str
    RABBITMQ_ARENA_MANAGER_EXCHANGE: str
    RABBITMQ_ARENA_MANAGER_ROUTING_KEY: str

    RABBITMQ_PORTFOLIO_QUEUE: str
    RABBITMQ_PORTFOLIO_EXCHANGE: str
    RABBITMQ_PORTFOLIO_ROUTING_KEY: str

    PORT: int = 10000

    class Config:
        env_file = ".env"


settings = Settings()
