# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr, AliasChoices
from typing import Optional

class Settings(BaseSettings):
    # Pydantic Settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="forbid",            # keep strict to catch mistakes
        case_sensitive=False,      # be forgiving with env key case
    )

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/postgres",
        validation_alias=AliasChoices(
            "DATABASE_URL",
            "SQLALCHEMY_DATABASE_URL",
            "sqlalchemy.url",          # your current key with a dot
        ),
    )

    # Admin auth (BakeADay requirement: validate against env)
    ADMIN_EMAIL: str = Field(
        default="abakeadayy@gmail.com",
        validation_alias=AliasChoices("ADMIN_EMAIL", "admin_email"),
    )
    # Either provide a raw password or a hash (hash preferred in prod)
    ADMIN_PASSWORD: Optional[SecretStr] = Field(
        default=None,
        validation_alias=AliasChoices("ADMIN_PASSWORD", "admin_password"),
    )
    ADMIN_PASSWORD_HASH: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("ADMIN_PASSWORD_HASH", "admin_password_hash"),
    )

        # JWT/session secret
    SECRET_KEY: SecretStr = Field(
        default=SecretStr("43db080680993b2c7d521c87002d85e8c24ef928635c74c60bb1e87b9cdc69c1"),
        validation_alias=AliasChoices("SECRET_KEY", "secret_key"),
    )

    # Email / SMTP
    ADMIN_RECEIVER_EMAIL: str = Field(
        default="abakeadayy@gmail.com",
        validation_alias=AliasChoices("ADMIN_RECEIVER_EMAIL", "admin_receiver_email"),
    )
    SMTP_HOST: str = Field(
        default="smtp.gmail.com",
        validation_alias=AliasChoices("SMTP_HOST", "smtp_host"),
    )
    SMTP_PORT: int = Field(
        default=587,
        validation_alias=AliasChoices("SMTP_PORT", "smtp_port"),
    )
    SMTP_USER: str = Field(
        default="",
        validation_alias=AliasChoices("SMTP_USER", "smtp_user"),
    )
    SMTP_PASSWORD: SecretStr = Field(
        default=SecretStr("bpqg gezs fcct tcpe"),
        validation_alias=AliasChoices("SMTP_PASSWORD", "smtp_password"),
    )

    # CORS (good sane default for local Next.js)
    CORS_ORIGINS: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://127.0.0.1:3000"],
        validation_alias=AliasChoices("CORS_ORIGINS", "cors_origins"),
    )

settings = Settings()
