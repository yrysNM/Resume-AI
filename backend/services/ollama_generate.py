"""Ollama LLM resume text generation (OpenAI-compatible Chat Completions)."""

from __future__ import annotations

import logging

from openai import APIConnectionError, APIError, AuthenticationError, OpenAI, RateLimitError

from config import settings
from schemas import ResumeRequest
from services import heuristic
from services.resume_i18n import headings_for, language_name

logger = logging.getLogger(__name__)


class OllamaUnavailable(Exception):
    """Raised when Ollama generation cannot run (server down or API failure)."""

    def __init__(self, message: str, *, reason: str = "unavailable") -> None:
        super().__init__(message)
        self.reason = reason


def ollama_configured() -> bool:
    # Local Ollama needs no real API key; base URL defaults are enough.
    return bool(settings.ollama_base_url.strip())


def generate_resume_text(payload: ResumeRequest) -> str:
    if not ollama_configured():
        raise OllamaUnavailable("OLLAMA_BASE_URL is not set", reason="missing-base-url")

    client = OpenAI(
        api_key=settings.ollama_api_key or "ollama",
        base_url=settings.ollama_base_url,
    )
    target = payload.target_job or payload.personal.position
    skills = ", ".join(payload.skills) if payload.skills else "(none listed)"
    experience_lines = []
    for item in payload.experience:
        experience_lines.append(
            f"- {item.role} at {item.company} ({item.period}): {item.description}"
        )
    experience_block = "\n".join(experience_lines) if experience_lines else "(none listed)"

    headings = headings_for(payload.language)
    lang_label = language_name(payload.language)
    system = (
        f"You are a professional resume writer. Produce a concise plain-text CV "
        f"written entirely in {lang_label}. Keep the candidate's name, email, and "
        "phone unchanged. Use these exact section headings on their own lines: "
        f"{headings.experience}, {headings.skills}, {headings.education}. "
        f"End with a line '{headings.target}: ...' using the target job. "
        "Do not invent employers, degrees, or skills that are not supported by "
        "the provided facts. Return only the resume text."
    )
    user = f"""Candidate:
Name: {payload.personal.full_name}
Email: {payload.personal.email}
Phone: {payload.personal.phone}
Current/desired position: {payload.personal.position}
Target job: {target}
Education: {payload.education or '(not provided)'}
Skills: {skills}
Experience:
{experience_block}
"""

    try:
        response = client.chat.completions.create(
            model=settings.ollama_model,
            temperature=0.4,
            max_tokens=900,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
    except APIConnectionError as exc:
        raise OllamaUnavailable(
            "Cannot reach Ollama — is the server running?",
            reason="connection-failed",
        ) from exc
    except AuthenticationError as exc:
        raise OllamaUnavailable("Ollama authentication failed", reason="auth-failed") from exc
    except RateLimitError as exc:
        raise OllamaUnavailable("Ollama rate limit exceeded", reason="rate-limited") from exc
    except APIError as exc:
        raise OllamaUnavailable(f"Ollama API error: {exc}", reason="api-error") from exc

    text = (response.choices[0].message.content or "").strip()
    if not text:
        raise OllamaUnavailable("Ollama returned empty resume text", reason="empty-response")
    return text


def generate_with_fallback(payload: ResumeRequest) -> tuple[str, str, bool]:
    """Return (resume_text, generator_label, used_ollama)."""
    if ollama_configured():
        try:
            return generate_resume_text(payload), settings.ollama_model, True
        except OllamaUnavailable as exc:
            logger.warning("Ollama generate failed (%s): %s", exc.reason, exc)
            if not settings.ai_allow_fallback:
                raise
            label = f"template(ollama-{exc.reason})"
            return heuristic.build_resume_text(payload), label, False
    elif not settings.ai_allow_fallback:
        raise OllamaUnavailable("OLLAMA_BASE_URL is not set", reason="missing-base-url")

    return heuristic.build_resume_text(payload), "template", False
