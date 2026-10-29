"""HeadHunter market-watch proxy for HR users."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from auth import require_hr
from models import User
from schemas import HhVacancyList
from services import hh_vacancies

router = APIRouter(prefix="/api/hh", tags=["hh"])


@router.get("/vacancies", response_model=HhVacancyList)
def list_hh_vacancies(
    page: int = Query(0, ge=0),
    _: User = Depends(require_hr),
) -> HhVacancyList:
    try:
        return hh_vacancies.fetch_hr_vacancies(page=page)
    except hh_vacancies.HhUnavailable as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="HeadHunter vacancies unavailable",
        ) from exc
