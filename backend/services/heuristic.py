"""Deterministic template generation and keyword scoring (offline fallback)."""

from __future__ import annotations

from schemas import AnalysisIssue, AnalysisResponse, ResumeRequest

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
    skills_line = ", ".join(payload.skills) if payload.skills else "—"
    exp_blocks = []
    for item in payload.experience:
        exp_blocks.append(
            f"• {item.role} — {item.company} ({item.period})\n  {item.description}"
        )
    experience_text = "\n".join(exp_blocks) if exp_blocks else "—"

    resume_text = f"""{p.full_name}
{p.position} | {p.email} | {p.phone}

ҚЫЗМЕТ ТӘЖІРИБЕСІ
{experience_text}

ДАҒДЫЛАР
{skills_line}

БІЛІМ
{payload.education or '—'}

Мақсатты лауазым: {payload.target_job or p.position}
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
    issues: list[AnalysisIssue] = []
    if len(payload.experience) < 1:
        issues.append(
            AnalysisIssue(
                section="Тәжірибе",
                severity="high",
                message="Жұмыс тәжірибесі бөлімі толтырылмаған",
                suggestion="Кем дегенде бір жұмыс орны мен міндеттерін қосыңыз",
            )
        )
    if len(payload.skills) < 3:
        issues.append(
            AnalysisIssue(
                section="Дағдылар",
                severity="medium",
                message="Дағдылар тізімі тым қысқа",
                suggestion="Мақсатты лауазымға сәйкес кем дегенде 5 дағды қосыңыз",
            )
        )
    for kw in missing[:2]:
        issues.append(
            AnalysisIssue(
                section="Кілт сөздер",
                severity="medium",
                message=f"Жұмыс сипаттамасында '{kw}' кілт сөзі жоқ",
                suggestion=f"'{kw}' дағдысын тәжірибе сипаттамасына енгізіңіз",
            )
        )
    return issues
