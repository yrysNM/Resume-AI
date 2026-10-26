"""Deterministic template generation and keyword scoring (offline fallback)."""

from __future__ import annotations

from schemas import AnalysisIssue, AnalysisResponse, ResumeRequest
from services.resume_i18n import headings_for, issue_copy_for

SKILL_KEYWORDS = {
    "frontend developer": ["react", "javascript", "typescript", "html", "css", "api"],
    "backend developer": ["python", "fastapi", "sql", "rest", "docker"],
    "data scientist": ["python", "ml", "pandas", "nlp", "scikit-learn"],
}


def detect_keywords(text: str, target: str) -> tuple[list[str], list[str]]:
    target_lower = target.lower()
    expected = SKILL_KEYWORDS.get(target_lower, ["react", "python", "api", "sql"])
    text_lower = text.lower()
    found = [kw for kw in expected if kw in text_lower]
    missing = [kw for kw in expected if kw not in text_lower]
    return found, missing


def expected_keywords(target: str) -> list[str]:
    return list(SKILL_KEYWORDS.get(target.lower(), ["react", "python", "api", "sql"]))


def build_resume_text(payload: ResumeRequest) -> str:
    p = payload.personal
    headings = headings_for(payload.language)
    skills_line = ", ".join(payload.skills) if payload.skills else "—"
    exp_blocks = []
    for item in payload.experience:
        exp_blocks.append(
            f"• {item.role} — {item.company} ({item.period})\n  {item.description}"
        )
    experience_text = "\n".join(exp_blocks) if exp_blocks else "—"

    resume_text = f"""{p.full_name}
{p.position} | {p.email} | {p.phone}

{headings.experience}
{experience_text}

{headings.skills}
{skills_line}

{headings.education}
{payload.education or '—'}

{headings.target}: {payload.target_job or p.position}
"""
    return resume_text.strip()


def analyze_resume(payload: ResumeRequest) -> AnalysisResponse:
    full_text = " ".join(
        [
            payload.personal.position,
            payload.education,
            " ".join(payload.skills),
            " ".join(e.description for e in payload.experience),
            payload.target_job,
        ]
    )
    found, missing = detect_keywords(full_text, payload.target_job or payload.personal.position)
    issues = base_issues(payload, missing)

    completeness = min(100.0, 40 + len(payload.skills) * 8 + len(payload.experience) * 15)
    match_score = min(100.0, 50 + len(found) * 10 - len(missing) * 5)
    expected = expected_keywords(payload.target_job or payload.personal.position)
    precision = round(len(found) / max(len(found) + len(missing), 1), 2)
    recall = round(len(found) / max(len(expected), 1), 2)

    return AnalysisResponse(
        completeness_score=round(completeness, 1),
        match_score=round(match_score, 1),
        precision=precision,
        recall=recall,
        issues=issues,
        keywords_found=found,
        keywords_missing=missing,
    )


def base_issues(payload: ResumeRequest, missing: list[str]) -> list[AnalysisIssue]:
    copy = issue_copy_for(payload.language)
    issues: list[AnalysisIssue] = []
    if len(payload.experience) < 1:
        issues.append(
            AnalysisIssue(
                section=copy.experience_section,
                severity="high",
                message=copy.experience_message,
                suggestion=copy.experience_suggestion,
            )
        )
    if len(payload.skills) < 3:
        issues.append(
            AnalysisIssue(
                section=copy.skills_section,
                severity="medium",
                message=copy.skills_message,
                suggestion=copy.skills_suggestion,
            )
        )
    for kw in missing[:2]:
        issues.append(
            AnalysisIssue(
                section=copy.keywords_section,
                severity="medium",
                message=copy.keywords_message.format(kw=kw),
                suggestion=copy.keywords_suggestion.format(kw=kw),
            )
        )
    return issues
