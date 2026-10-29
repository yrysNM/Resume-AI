"""Role-aware dashboard stats."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import Application, Company, Resume, User, Vacancy
from schemas import DashboardOut, HrDashboard, SeekerDashboard

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardOut)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> HrDashboard | SeekerDashboard:
    role = current_user.role or "seeker"
    if role == "hr":
        company_ids = [
            c.id
            for c in db.query(Company.id).filter(Company.user_id == current_user.id).all()
        ]
        companies = len(company_ids)
        open_vacancies = 0
        applications = 0
        avg_score = None
        if company_ids:
            open_vacancies = (
                db.query(func.count(Vacancy.id))
                .filter(Vacancy.company_id.in_(company_ids), Vacancy.status == "open")
                .scalar()
                or 0
            )
            vacancy_ids = [
                v.id
                for v in db.query(Vacancy.id)
                .filter(Vacancy.company_id.in_(company_ids))
                .all()
            ]
            if vacancy_ids:
                applications = (
                    db.query(func.count(Application.id))
                    .filter(Application.vacancy_id.in_(vacancy_ids))
                    .scalar()
                    or 0
                )
                avg_score = (
                    db.query(func.avg(Application.match_score))
                    .filter(Application.vacancy_id.in_(vacancy_ids))
                    .scalar()
                )
                if avg_score is not None:
                    avg_score = round(float(avg_score), 1)
        return HrDashboard(
            companies=companies,
            open_vacancies=int(open_vacancies),
            applications=int(applications),
            average_match_score=avg_score,
        )

    saved = (
        db.query(func.count(Resume.id))
        .filter(Resume.user_id == current_user.id)
        .scalar()
        or 0
    )
    sent = (
        db.query(func.count(Application.id))
        .filter(Application.seeker_id == current_user.id)
        .scalar()
        or 0
    )
    best = (
        db.query(func.max(Application.match_score))
        .filter(Application.seeker_id == current_user.id)
        .scalar()
    )
    open_jobs = (
        db.query(func.count(Vacancy.id)).filter(Vacancy.status == "open").scalar() or 0
    )
    return SeekerDashboard(
        saved_resumes=int(saved),
        applications_sent=int(sent),
        best_match_score=round(float(best), 1) if best is not None else None,
        open_jobs=int(open_jobs),
    )
