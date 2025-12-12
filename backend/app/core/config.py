# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr, AliasChoices, field_validator
from typing import Optional
import json

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
        default="postgresql://bakeaday_user:WD8qQS69uaEMtnxB9sBsMC9ZUevFu4jI@dpg-d4p7066uk2gs73d6i4b0-a/bakeaday",
        validation_alias=AliasChoices(
            "DATABASE_URL",
            "SQLALCHEMY_DATABASE_URL",
            "sqlalchemy.url",
        ),
    )

    # Admin auth (BakeADay requirement: validate against env)
    ADMIN_EMAIL: str = Field(
        default="abakeadayy@gmail.com",
        validation_alias=AliasChoices("ADMIN_EMAIL", "admin_email"),
    )
    # Either provide a raw password or a hash (hash preferred in prod)
    ADMIN_PASSWORD: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("ADMIN_PASSWORD", "admin_password"),
    )
    ADMIN_PASSWORD_HASH: Optional[SecretStr] = Field(
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
        default=SecretStr(""),  # require via env in prod
        validation_alias=AliasChoices("SMTP_PASSWORD", "smtp_password"),
    )

    # Clerk webhook signing secret (reuse SECRET_KEY if not set)
    CLERK_SIGNING_SECRET: Optional[SecretStr] = Field(
        default=None,
        validation_alias=AliasChoices("CLERK_SIGNING_SECRET", "clerk_signing_secret"),
    )

    # CORS (good sane default for local Next.js)
    # Can be set as JSON string in env var: ["https://bakeaday.vercel.app","http://localhost:3000"]
    CORS_ORIGINS: list[str] = Field(
        default_factory=lambda: ["https://bakeaday.vercel.app", "http://localhost:3000", "http://127.0.0.1:3000"],
        validation_alias=AliasChoices("CORS_ORIGINS", "cors_origins"),
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS_ORIGINS from JSON string if it's a string, otherwise return as-is."""
        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                # If it's not valid JSON, try splitting by comma
                return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

settings = Settings()
