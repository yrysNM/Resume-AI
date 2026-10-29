"""Seeker job board and applications."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from auth import require_seeker
from database import get_db
from models import Application, Company, Resume, User, Vacancy
from schemas import ApplyRequest, JobOut, SeekerApplicationOut
from services import rank as rank_service

router = APIRouter(tags=["jobs"])


@router.get("/api/jobs", response_model=list[JobOut])
def list_jobs(
    db: Session = Depends(get_db),
    _: User = Depends(require_seeker),
) -> list[JobOut]:
    rows = (
        db.query(Vacancy)
        .options(joinedload(Vacancy.company))
        .filter(Vacancy.status == "open")
        .order_by(Vacancy.created_at.desc())
        .all()
    )
    return [
        JobOut(
            id=v.id,
            title=v.title,
            description=v.description,
            company_id=v.company_id,
            company_name=v.company.name if v.company else "",
        )
        for v in rows
    ]


@router.post("/api/jobs/{vacancy_id}/apply", response_model=SeekerApplicationOut, status_code=201)
def apply_to_job(
    vacancy_id: int,
    payload: ApplyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_seeker),
) -> SeekerApplicationOut:
    vacancy = (
        db.query(Vacancy)
        .options(joinedload(Vacancy.company))
        .filter(Vacancy.id == vacancy_id)
        .first()
    )
    if vacancy is None:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    if vacancy.status != "open":
        raise HTTPException(status_code=409, detail="Vacancy is closed")

    resume = (
        db.query(Resume)
        .filter(Resume.id == payload.resume_id, Resume.user_id == current_user.id)
        .first()
    )
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")

    existing = (
        db.query(Application)
        .filter(
            Application.vacancy_id == vacancy_id,
            Application.seeker_id == current_user.id,
        )
        .first()
    )
    if existing is not None:
        raise HTTPException(status_code=409, detail="Already applied")

    try:
        score, labeled = rank_service.score_resume_against_vacancy(
            resume.resume_text, vacancy.title, vacancy.description
        )
    except rank_service.RankUnavailable as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Ranking unavailable",
        ) from exc

    app = Application(
        vacancy_id=vacancy_id,
        seeker_id=current_user.id,
        resume_id=resume.id,
        resume_text=resume.resume_text,
        match_score=score,
        ranked_by=labeled,
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return SeekerApplicationOut(
        id=app.id,
        vacancy_id=app.vacancy_id,
        vacancy_title=vacancy.title,
        resume_id=app.resume_id,
        match_score=app.match_score,
        ranked_by=app.ranked_by,
        created_at=app.created_at,
    )


@router.get("/api/applications", response_model=list[SeekerApplicationOut])
def list_my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_seeker),
) -> list[SeekerApplicationOut]:
    rows = (
        db.query(Application)
        .options(joinedload(Application.vacancy))
        .filter(Application.seeker_id == current_user.id)
        .order_by(Application.created_at.desc())
        .all()
    )
    return [
        SeekerApplicationOut(
            id=a.id,
            vacancy_id=a.vacancy_id,
            vacancy_title=a.vacancy.title if a.vacancy else "",
            resume_id=a.resume_id,
            match_score=a.match_score,
            ranked_by=a.ranked_by,
            created_at=a.created_at,
        )
        for a in rows
    ]
