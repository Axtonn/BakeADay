from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ADMIN_EMAIL: str
    ADMIN_PASSWORD_HASH: str
    SECRET_KEY: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
