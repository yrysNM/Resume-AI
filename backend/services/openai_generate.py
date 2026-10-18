"""OpenAI GPT resume text generation."""

from __future__ import annotations

from openai import APIError, AuthenticationError, OpenAI, RateLimitError

from config import settings
from schemas import ResumeRequest
from services import heuristic


class OpenAIUnavailable(Exception):
    """Raised when GPT generation cannot run (missing key or API failure)."""


def openai_configured() -> bool:
    return bool(settings.openai_api_key.strip())


def generate_resume_text(payload: ResumeRequest) -> str:
    if not openai_configured():
        raise OpenAIUnavailable("OPENAI_API_KEY is not set")

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
        raise OpenAIUnavailable("OpenAI authentication failed") from exc
    except RateLimitError as exc:
        raise OpenAIUnavailable("OpenAI rate limit exceeded") from exc
    except APIError as exc:
        raise OpenAIUnavailable(f"OpenAI API error: {exc}") from exc

    text = (response.choices[0].message.content or "").strip()
    if not text:
        raise OpenAIUnavailable("OpenAI returned empty resume text")
    return text


def generate_with_fallback(payload: ResumeRequest) -> tuple[str, str, bool]:
    """Return (resume_text, generator_label, used_openai)."""
    if openai_configured():
        try:
            return generate_resume_text(payload), settings.openai_model, True
        except OpenAIUnavailable:
            if not settings.ai_allow_fallback:
                raise
    elif not settings.ai_allow_fallback:
        raise OpenAIUnavailable("OPENAI_API_KEY is not set")

    return heuristic.build_resume_text(payload), "template", False
