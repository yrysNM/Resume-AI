"""Resume generate/analyze endpoints and persisted resume CRUD."""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import Resume, User
from schemas import (
    AnalysisResponse,
    GenerateResponse,
    ResumeDetail,
    ResumeRequest,
    ResumeSummary,
    ResumeTemplate,
)
from services import bert_analyze, export as export_service, ollama_generate, resume_logic
from services.resume_layout import layout_from_input_json

router = APIRouter(tags=["resumes"])


def _analysis_from_row(row: Resume) -> AnalysisResponse | None:
    if not row.analysis_json:
        return None
    return AnalysisResponse.model_validate_json(row.analysis_json)


def _ai_http_error(exc: Exception) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=str(exc) or "AI service unavailable",
    )


@router.post("/api/resume/generate", response_model=GenerateResponse)
def generate_resume(
    payload: ResumeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> GenerateResponse:
    try:
        resume_text, analysis, generated_by = resume_logic.generate_and_analyze(payload)
    except (ollama_generate.OllamaUnavailable, bert_analyze.BertUnavailable) as exc:
        raise _ai_http_error(exc) from exc

    title = payload.target_job or payload.personal.position or "Untitled resume"
    row = Resume(
        user_id=current_user.id,
        title=title,
        target_job=payload.target_job or payload.personal.position,
        resume_text=resume_text,
        input_json=payload.model_dump_json(),
        analysis_json=analysis.model_dump_json(),
        generated_by=generated_by,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return GenerateResponse(
        id=row.id,
        resume_text=resume_text,
        format="plain",
        generated_by=generated_by,
        language=payload.language,
        template=payload.template,
        analysis=analysis,
    )


@router.post("/api/resume/analyze", response_model=AnalysisResponse)
def analyze_resume_endpoint(
    payload: ResumeRequest,
    current_user: User = Depends(get_current_user),
) -> AnalysisResponse:
    _ = current_user
    try:
        analysis, _analyzer = resume_logic.analyze_resume(payload)
    except bert_analyze.BertUnavailable as exc:
        raise _ai_http_error(exc) from exc
    return analysis


@router.get("/api/resumes", response_model=list[ResumeSummary])
def list_resumes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Resume]:
    return (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
        .all()
    )


@router.get("/api/resumes/{resume_id}", response_model=ResumeDetail)
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ResumeDetail:
    row = (
        db.query(Resume)
        .filter(Resume.id == resume_id, Resume.user_id == current_user.id)
        .first()
    )
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    language, template = layout_from_input_json(row.input_json)
    return ResumeDetail(
        id=row.id,
        title=row.title,
        target_job=row.target_job,
        generated_by=row.generated_by,
        created_at=row.created_at,
        updated_at=row.updated_at,
        resume_text=row.resume_text,
        language=language,
        template=template,
        analysis=_analysis_from_row(row),
    )


@router.delete("/api/resumes/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    row = (
        db.query(Resume)
        .filter(Resume.id == resume_id, Resume.user_id == current_user.id)
        .first()
    )
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    db.delete(row)
    db.commit()


@router.get("/api/resumes/{resume_id}/export")
def export_resume(
    resume_id: int,
    fmt: Literal["pdf", "docx"] = Query(..., alias="format"),
    template: ResumeTemplate | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    row = (
        db.query(Resume)
        .filter(Resume.id == resume_id, Resume.user_id == current_user.id)
        .first()
    )
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    stored_language, stored_template = layout_from_input_json(row.input_json)
    try:
        body, media_type, _ = export_service.export_bytes(
            row.resume_text,
            fmt,
            template=template or stored_template,
            language=stored_language,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    title = row.title or "resume"
    safe = "".join(c if c.isalnum() or c in " -_" else "_" for c in title).strip() or "resume"
    filename = f"{safe[:80]}.{fmt}"
    return Response(
        content=body,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
