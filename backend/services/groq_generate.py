"""Groq LLM resume text generation (OpenAI-compatible Chat Completions)."""

from __future__ import annotations

import logging

from openai import APIError, AuthenticationError, OpenAI, RateLimitError

from config import settings
from schemas import ResumeRequest
from services import heuristic

logger = logging.getLogger(__name__)


class GroqUnavailable(Exception):
    """Raised when Groq generation cannot run (missing key or API failure)."""

    def __init__(self, message: str, *, reason: str = "unavailable") -> None:
        super().__init__(message)
        self.reason = reason


def groq_configured() -> bool:
    return bool(settings.groq_api_key.strip())


def _classify_rate_limit(exc: RateLimitError) -> tuple[str, str]:
    body = str(exc).lower()
    if "insufficient_quota" in body or "credit" in body or "billing" in body:
        return "Groq quota exhausted", "quota-exhausted"
    return "Groq rate limit exceeded", "rate-limited"


def generate_resume_text(payload: ResumeRequest) -> str:
    if not groq_configured():
        raise GroqUnavailable("GROQ_API_KEY is not set", reason="missing-key")

    client = OpenAI(
        api_key=settings.groq_api_key,
        base_url=settings.groq_base_url,
    )
    target = payload.target_job or payload.personal.position
    skills = ", ".join(payload.skills) if payload.skills else "(none listed)"
    experience_lines = []
    for item in payload.experience:
        experience_lines.append(
            f"- {item.role} at {item.company} ({item.period}): {item.description}"
        )
    experience_block = "\n".join(experience_lines) if experience_lines else "(none listed)"

    system = (
        "You are a professional resume writer. Produce a concise plain-text CV. "
        "Use clear section headings. Prefer Kazakh section titles "
        "(ҚЫЗМЕТ ТӘЖІРИБЕСІ, ДАҒДЫЛАР, БІЛІМ) with English content when the "
        "candidate data is in English. Do not invent employers, degrees, or skills "
        "that are not supported by the provided facts. Return only the resume text."
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
            model=settings.groq_model,
            temperature=0.4,
            max_tokens=900,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
    except AuthenticationError as exc:
        raise GroqUnavailable("Groq authentication failed", reason="auth-failed") from exc
    except RateLimitError as exc:
        message, reason = _classify_rate_limit(exc)
        raise GroqUnavailable(message, reason=reason) from exc
    except APIError as exc:
        raise GroqUnavailable(f"Groq API error: {exc}", reason="api-error") from exc

    text = (response.choices[0].message.content or "").strip()
    if not text:
        raise GroqUnavailable("Groq returned empty resume text", reason="empty-response")
    return text


def generate_with_fallback(payload: ResumeRequest) -> tuple[str, str, bool]:
    """Return (resume_text, generator_label, used_groq)."""
    if groq_configured():
        try:
            return generate_resume_text(payload), settings.groq_model, True
        except GroqUnavailable as exc:
            logger.warning("Groq generate failed (%s): %s", exc.reason, exc)
            if not settings.ai_allow_fallback:
                raise
            label = f"template(groq-{exc.reason})"
            return heuristic.build_resume_text(payload), label, False
    elif not settings.ai_allow_fallback:
        raise GroqUnavailable("GROQ_API_KEY is not set", reason="missing-key")

    return heuristic.build_resume_text(payload), "template", False
