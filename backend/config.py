"""Application settings loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "Resume AI API"
    database_url: str = "sqlite:///./resume_ai.db"
    secret_key: str = "change-me-in-production-resume-ai-demo-secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24 hours
    cors_origins: tuple[str, ...] = ("*",)


def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv("DATABASE_URL", Settings.database_url),
        secret_key=os.getenv("SECRET_KEY", Settings.secret_key),
        algorithm=os.getenv("JWT_ALGORITHM", Settings.algorithm),
        access_token_expire_minutes=int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", str(Settings.access_token_expire_minutes))
        ),
    )


settings = get_settings()
