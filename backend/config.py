"""Application settings loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str = "Resume AI API"
    database_url: str = "sqlite:///./resume_ai.db"
    secret_key: str = "change-me-in-production-resume-ai-demo-secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24 hours
    cors_origins: tuple[str, ...] = ("*",)

    # OpenAI (GPT resume generation)
    openai_api_key: str = ""
    openai_model: str = "gpt-3.5-turbo"

    # BERT / sentence-transformers (analysis)
    bert_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    bert_keyword_threshold: float = 0.35
    bert_retry_load: bool = False

    # When true, missing keys / model load failures use local heuristics.
    # When false, generate/analyze return HTTP 503 with a clear error.
    ai_allow_fallback: bool = True


def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv("DATABASE_URL", Settings.database_url),
        secret_key=os.getenv("SECRET_KEY", Settings.secret_key),
        algorithm=os.getenv("JWT_ALGORITHM", Settings.algorithm),
        access_token_expire_minutes=int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", str(Settings.access_token_expire_minutes))
        ),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", Settings.openai_model),
        bert_model_name=os.getenv("BERT_MODEL_NAME", Settings.bert_model_name),
        bert_keyword_threshold=float(
            os.getenv("BERT_KEYWORD_THRESHOLD", str(Settings.bert_keyword_threshold))
        ),
        bert_retry_load=_env_bool("BERT_RETRY_LOAD", Settings.bert_retry_load),
        ai_allow_fallback=_env_bool("AI_ALLOW_FALLBACK", Settings.ai_allow_fallback),
    )


settings = get_settings()
