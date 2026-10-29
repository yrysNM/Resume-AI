"""HR vacancy CRUD, applications list, and re-rank."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from auth import require_hr
from database import get_db
from models import Application, Company, Resume, User, Vacancy
from schemas import (
    HrApplicationOut,
    VacancyCreate,
    VacancyOut,
    VacancyUpdate,
)
from services import rank as rank_service

router = APIRouter(tags=["vacancies"])


def _owned_company(db: Session, company_id: int, user: User) -> Company:
    row = (
        db.query(Company)
        .filter(Company.id == company_id, Company.user_id == user.id)
        .first()
    )
    if row is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return row


def _owned_vacancy(db: Session, vacancy_id: int, user: User) -> Vacancy:
    row = (
        db.query(Vacancy)
        .join(Company)
        .filter(Vacancy.id == vacancy_id, Company.user_id == user.id)
        .first()
    )
    if row is None:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return row


@router.get("/api/companies/{company_id}/vacancies", response_model=list[VacancyOut])
def list_company_vacancies(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr),
) -> list[Vacancy]:
    _owned_company(db, company_id, current_user)
    return (
        db.query(Vacancy)
        .filter(Vacancy.company_id == company_id)
        .order_by(Vacancy.created_at.desc())
        .all()
    )


@router.post(
    "/api/companies/{company_id}/vacancies",
    response_model=VacancyOut,
    status_code=status.HTTP_201_CREATED,
)
def create_company_vacancy(
    company_id: int,
    payload: VacancyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr),
) -> Vacancy:
    _owned_company(db, company_id, current_user)
    row = Vacancy(
        company_id=company_id,
        title=payload.title.strip(),
        description=payload.description or "",
        status=payload.status,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get(
    "/api/companies/{company_id}/vacancies/{vacancy_id}",
    response_model=VacancyOut,
)
def get_company_vacancy(
    company_id: int,
    vacancy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr),
) -> Vacancy:
    _owned_company(db, company_id, current_user)
    row = (
        db.query(Vacancy)
        .filter(Vacancy.id == vacancy_id, Vacancy.company_id == company_id)
        .first()
    )
    if row is None:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return row


@router.put(
    "/api/companies/{company_id}/vacancies/{vacancy_id}",
    response_model=VacancyOut,
)
def update_company_vacancy(
    company_id: int,
    vacancy_id: int,
    payload: VacancyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr),
) -> Vacancy:
    _owned_company(db, company_id, current_user)
    row = (
        db.query(Vacancy)
        .filter(Vacancy.id == vacancy_id, Vacancy.company_id == company_id)
        .first()
    )
    if row is None:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    if payload.title is not None:
        row.title = payload.title.strip()
    if payload.description is not None:
        row.description = payload.description
    if payload.status is not None:
        row.status = payload.status
    db.commit()
    db.refresh(row)
    return row


@router.delete(
    "/api/companies/{company_id}/vacancies/{vacancy_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_company_vacancy(
    company_id: int,
    vacancy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr),
) -> None:
    _owned_company(db, company_id, current_user)
    row = (
        db.query(Vacancy)
        .filter(Vacancy.id == vacancy_id, Vacancy.company_id == company_id)
        .first()
    )
    if row is None:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    db.delete(row)
    db.commit()


@router.get("/api/vacancies/{vacancy_id}", response_model=VacancyOut)
def get_vacancy(
    vacancy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr),
) -> Vacancy:
    return _owned_vacancy(db, vacancy_id, current_user)


@router.get(
    "/api/vacancies/{vacancy_id}/applications",
    response_model=list[HrApplicationOut],
)
def list_vacancy_applications(
    vacancy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr),
) -> list[HrApplicationOut]:
    _owned_vacancy(db, vacancy_id, current_user)
    rows = (
        db.query(Application)
        .options(joinedload(Application.resume))
        .filter(Application.vacancy_id == vacancy_id)
        .order_by(Application.match_score.desc())
        .all()
    )
    return [
        HrApplicationOut(
            id=a.id,
            vacancy_id=a.vacancy_id,
            seeker_id=a.seeker_id,
            resume_id=a.resume_id,
            resume_text=a.resume_text,
            match_score=a.match_score,
            ranked_by=a.ranked_by,
            created_at=a.created_at,
        )
        for a in rows
    ]


@router.post(
    "/api/vacancies/{vacancy_id}/rank",
    response_model=list[HrApplicationOut],
)
def rank_vacancy_applications(
    vacancy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr),
) -> list[HrApplicationOut]:
    vacancy = _owned_vacancy(db, vacancy_id, current_user)
    rows = (
        db.query(Application)
        .filter(Application.vacancy_id == vacancy_id)
        .all()
    )
    try:
        for app in rows:
            text = app.resume_text
            if app.resume_id is not None:
                resume = db.query(Resume).filter(Resume.id == app.resume_id).first()
                if resume is not None:
                    text = resume.resume_text
            score, labeled = rank_service.score_resume_against_vacancy(
                text, vacancy.title, vacancy.description
            )
            app.match_score = score
            app.ranked_by = labeled
            app.resume_text = text
    except rank_service.RankUnavailable as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Ranking unavailable",
        ) from exc
    db.commit()
    return list_vacancy_applications(vacancy_id, db, current_user)
