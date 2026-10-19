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
)
from services import export as export_service
from services import resume_logic

router = APIRouter(tags=["resumes"])


def _analysis_from_row(row: Resume) -> AnalysisResponse | None:
    if not row.analysis_json:
        return None
    return AnalysisResponse.model_validate_json(row.analysis_json)


@router.post("/api/resume/generate", response_model=GenerateResponse)
def generate_resume(
    payload: ResumeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> GenerateResponse:
    resume_text = resume_logic.build_resume_text(payload)
    analysis = resume_logic.analyze_resume(payload)
    title = payload.target_job or payload.personal.position or "Untitled resume"

    row = Resume(
        user_id=current_user.id,
        title=title,
        target_job=payload.target_job or payload.personal.position,
        resume_text=resume_text,
        input_json=payload.model_dump_json(),
        analysis_json=analysis.model_dump_json(),
        generated_by=resume_logic.GENERATED_BY_LABEL,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return GenerateResponse(
        id=row.id,
        resume_text=resume_text,
        format="plain",
        generated_by=resume_logic.GENERATED_BY_LABEL,
        analysis=analysis,
    )


@router.post("/api/resume/analyze", response_model=AnalysisResponse)
def analyze_resume_endpoint(
    payload: ResumeRequest,
    current_user: User = Depends(get_current_user),
) -> AnalysisResponse:
    _ = current_user  # auth required; analysis itself is rule-based
    return resume_logic.analyze_resume(payload)


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
    return ResumeDetail(
        id=row.id,
        title=row.title,
        target_job=row.target_job,
        generated_by=row.generated_by,
        created_at=row.created_at,
        updated_at=row.updated_at,
        resume_text=row.resume_text,
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
    try:
        body, media_type, _ = export_service.export_bytes(row.resume_text, fmt)
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
