"""HR company CRUD."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth import require_hr
from database import get_db
from models import Company, User
from schemas import CompanyCreate, CompanyOut, CompanyUpdate

router = APIRouter(prefix="/api/companies", tags=["companies"])


def _owned_company(db: Session, company_id: int, user: User) -> Company:
    row = (
        db.query(Company)
        .filter(Company.id == company_id, Company.user_id == user.id)
        .first()
    )
    if row is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return row


@router.get("", response_model=list[CompanyOut])
def list_companies(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr),
) -> list[Company]:
    return (
        db.query(Company)
        .filter(Company.user_id == current_user.id)
        .order_by(Company.created_at.desc())
        .all()
    )


@router.post("", response_model=CompanyOut, status_code=status.HTTP_201_CREATED)
def create_company(
    payload: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr),
) -> Company:
    row = Company(
        user_id=current_user.id,
        name=payload.name.strip(),
        description=payload.description or "",
        website=payload.website,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get("/{company_id}", response_model=CompanyOut)
def get_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr),
) -> Company:
    return _owned_company(db, company_id, current_user)


@router.put("/{company_id}", response_model=CompanyOut)
def update_company(
    company_id: int,
    payload: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr),
) -> Company:
    row = _owned_company(db, company_id, current_user)
    if payload.name is not None:
        row.name = payload.name.strip()
    if payload.description is not None:
        row.description = payload.description
    if payload.website is not None:
        row.website = payload.website
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_hr),
) -> None:
    row = _owned_company(db, company_id, current_user)
    db.delete(row)
    db.commit()
