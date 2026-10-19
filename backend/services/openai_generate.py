"""OpenAI GPT resume text generation."""

from __future__ import annotations

import logging

from openai import APIError, AuthenticationError, OpenAI, RateLimitError

from config import settings
from schemas import ResumeRequest
from services import heuristic

logger = logging.getLogger(__name__)


class OpenAIUnavailable(Exception):
    """Raised when GPT generation cannot run (missing key or API failure)."""

    def __init__(self, message: str, *, reason: str = "unavailable") -> None:
        super().__init__(message)
        self.reason = reason


def openai_configured() -> bool:
    return bool(settings.openai_api_key.strip())


def _classify_rate_limit(exc: RateLimitError) -> tuple[str, str]:
    body = str(exc).lower()
    if "insufficient_quota" in body or "credit_balance" in body or "no credits" in body:
        return "OpenAI quota exhausted — add billing credits", "quota-exhausted"
    return "OpenAI rate limit exceeded", "rate-limited"


def generate_resume_text(payload: ResumeRequest) -> str:
    if not openai_configured():
        raise OpenAIUnavailable("OPENAI_API_KEY is not set", reason="missing-key")

    client = OpenAI(api_key=settings.openai_api_key)
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
            model=settings.openai_model,
            temperature=0.4,
            max_tokens=900,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
    except AuthenticationError as exc:
        raise OpenAIUnavailable("OpenAI authentication failed", reason="auth-failed") from exc
    except RateLimitError as exc:
        message, reason = _classify_rate_limit(exc)
        raise OpenAIUnavailable(message, reason=reason) from exc
    except APIError as exc:
        raise OpenAIUnavailable(f"OpenAI API error: {exc}", reason="api-error") from exc

    text = (response.choices[0].message.content or "").strip()
    if not text:
        raise OpenAIUnavailable("OpenAI returned empty resume text", reason="empty-response")
    return text


def generate_with_fallback(payload: ResumeRequest) -> tuple[str, str, bool]:
    """Return (resume_text, generator_label, used_openai)."""
    if openai_configured():
        try:
            return generate_resume_text(payload), settings.openai_model, True
        except OpenAIUnavailable as exc:
            logger.warning("OpenAI generate failed (%s): %s", exc.reason, exc)
            if not settings.ai_allow_fallback:
                raise
            label = f"template(openai-{exc.reason})"
            return heuristic.build_resume_text(payload), label, False
    elif not settings.ai_allow_fallback:
        raise OpenAIUnavailable("OPENAI_API_KEY is not set", reason="missing-key")

    return heuristic.build_resume_text(payload), "template", False
