"""HeadHunter vacancy search proxy for authenticated users (HR + employees)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from auth import get_current_user
from models import User
from schemas import HhVacancyList
from services import hh_vacancies

router = APIRouter(prefix="/api/hh", tags=["hh"])


@router.get("/vacancies", response_model=HhVacancyList)
def list_hh_vacancies(
    page: int = Query(0, ge=0),
    text: str = Query("", max_length=200),
    category: str = Query(hh_vacancies.DEFAULT_CATEGORY, max_length=32),
    _: User = Depends(get_current_user),
) -> HhVacancyList:
    category_key = (category or hh_vacancies.DEFAULT_CATEGORY).strip().lower()
    if category_key not in hh_vacancies.HH_CATEGORIES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown category. Allowed: {', '.join(hh_vacancies.list_categories())}",
        )
    try:
        return hh_vacancies.fetch_vacancies(page=page, text=text, category=category_key)
    except hh_vacancies.HhUnavailable as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="HeadHunter vacancies unavailable",
        ) from exc


@router.get("/categories", response_model=list[str])
def list_hh_categories(
    _: User = Depends(get_current_user),
) -> list[str]:
    return hh_vacancies.list_categories()
