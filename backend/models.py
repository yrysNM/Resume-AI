"""ORM models for users, saved resumes, companies, vacancies, and applications."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="uq_users_email"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    role: Mapped[str] = mapped_column(
        String(16), nullable=False, default="seeker", server_default="seeker"
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    resumes: Mapped[list[Resume]] = relationship(
        "Resume", back_populates="owner", cascade="all, delete-orphan"
    )
    companies: Mapped[list[Company]] = relationship(
        "Company", back_populates="owner", cascade="all, delete-orphan"
    )
    applications: Mapped[list[Application]] = relationship(
        "Application",
        back_populates="seeker",
        cascade="all, delete-orphan",
        foreign_keys="Application.seeker_id",
    )


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, default="Untitled resume")
    target_job: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    resume_text: Mapped[str] = mapped_column(Text, nullable=False)
    input_json: Mapped[str] = mapped_column(Text, nullable=False)  # original form payload
    analysis_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    generated_by: Mapped[str] = mapped_column(
        String(255), nullable=False, default="pending"
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow
    )

    owner: Mapped[User] = relationship("User", back_populates="resumes")


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    website: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    owner: Mapped[User] = relationship("User", back_populates="companies")
    vacancies: Mapped[list[Vacancy]] = relationship(
        "Vacancy", back_populates="company", cascade="all, delete-orphan"
    )


class Vacancy(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="open", server_default="open"
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    company: Mapped[Company] = relationship("Company", back_populates="vacancies")
    applications: Mapped[list[Application]] = relationship(
        "Application", back_populates="vacancy", cascade="all, delete-orphan"
    )


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("vacancy_id", "seeker_id", name="uq_applications_vacancy_seeker"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancies.id", ondelete="CASCADE"), index=True
    )
    seeker_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    resume_id: Mapped[int | None] = mapped_column(
        ForeignKey("resumes.id", ondelete="SET NULL"), nullable=True, index=True
    )
    resume_text: Mapped[str] = mapped_column(Text, nullable=False)
    match_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    ranked_by: Mapped[str] = mapped_column(String(255), nullable=False, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    vacancy: Mapped[Vacancy] = relationship("Vacancy", back_populates="applications")
    seeker: Mapped[User] = relationship(
        "User", back_populates="applications", foreign_keys=[seeker_id]
    )
    resume: Mapped[Resume | None] = relationship("Resume")
