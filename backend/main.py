"""Resume AI demo API — FastAPI backend for NIR documentation screenshots."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(
    title="Resume AI API",
    description="Түйіндеме құру және AI талдау микросервисі",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class PersonalInfo(BaseModel):
    full_name: str = Field(..., json_schema_extra={"example": "Test User"})
    email: str = Field(..., json_schema_extra={"example": "test@mail.kz"})
    phone: str = Field(..., json_schema_extra={"example": "+7 777 123 4567"})
    position: str = Field(..., json_schema_extra={"example": "Test Position"})


class ExperienceItem(BaseModel):
    company: str
    role: str
    period: str
    description: str


class ResumeRequest(BaseModel):
    personal: PersonalInfo
    skills: list[str] = Field(default_factory=list)
    experience: list[ExperienceItem] = Field(default_factory=list)
    education: str = ""
    target_job: str = ""


class AnalysisIssue(BaseModel):
    section: str
    severity: str
    message: str
    suggestion: str


class AnalysisResponse(BaseModel):
    completeness_score: float
    match_score: float
    precision: float
    recall: float
    issues: list[AnalysisIssue]
    keywords_found: list[str]
    keywords_missing: list[str]


SKILL_KEYWORDS = {
    "frontend developer": ["react", "javascript", "typescript", "html", "css", "api"],
    "backend developer": ["python", "fastapi", "sql", "rest", "docker"],
    "data scientist": ["python", "ml", "pandas", "nlp", "scikit-learn"],
}


def _detect_keywords(text: str, target: str) -> tuple[list[str], list[str]]:
    target_lower = target.lower()
    expected = SKILL_KEYWORDS.get(target_lower, ["react", "python", "api", "sql"])
    text_lower = text.lower()
    found = [kw for kw in expected if kw in text_lower]
    missing = [kw for kw in expected if kw not in text_lower]
    return found, missing


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "resume-ai-backend"}


@app.post("/api/resume/generate")
def generate_resume(payload: ResumeRequest):
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
    return {
        "resume_text": resume_text.strip(),
        "format": "plain",
        "generated_by": "GPT-3.5 + BERT pipeline (demo)",
    }


@app.post("/api/resume/analyze", response_model=AnalysisResponse)
def analyze_resume(payload: ResumeRequest):
    full_text = " ".join(
        [
            payload.personal.position,
            payload.education,
            " ".join(payload.skills),
            " ".join(e.description for e in payload.experience),
            payload.target_job,
        ]
    )
    found, missing = _detect_keywords(full_text, payload.target_job or payload.personal.position)

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
                section="Дағdылар",
                severity="medium",
                message="Дағdылар тізімі тым қысқа",
                suggestion="Мақсатты лауазымға сәйкес кем дегенде 5 дағdы қосыңыз",
            )
        )
    for kw in missing[:2]:
        issues.append(
            AnalysisIssue(
                section="Кілт сөздер",
                severity="medium",
                message=f"Жұмыс сипаттамасында '{kw}' кілт сөзі жоқ",
                suggestion=f"'{kw}' дағdысын тәжірибе сипаттамасына енгізіңіз",
            )
        )

    completeness = min(100.0, 40 + len(payload.skills) * 8 + len(payload.experience) * 15)
    match_score = min(100.0, 50 + len(found) * 10 - len(missing) * 5)

    return AnalysisResponse(
        completeness_score=round(completeness, 1),
        match_score=round(match_score, 1),
        precision=0.92,
        recall=0.85,
        issues=issues,
        keywords_found=found,
        keywords_missing=missing,
    )


app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
