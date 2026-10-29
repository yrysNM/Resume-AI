"""Pydantic request/response schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, EmailStr, Field

ResumeLanguage = Literal["kk", "ru", "en"]
ResumeTemplate = Literal["classic", "modern", "minimal"]
UserRole = Literal["seeker", "hr"]
VacancyStatus = Literal["open", "closed"]

LANGUAGE_VALUES: tuple[ResumeLanguage, ...] = ("kk", "ru", "en")
TEMPLATE_VALUES: tuple[ResumeTemplate, ...] = ("classic", "modern", "minimal")
USER_ROLE_VALUES: tuple[UserRole, ...] = ("seeker", "hr")
VACANCY_STATUS_VALUES: tuple[VacancyStatus, ...] = ("open", "closed")


class PersonalInfo(BaseModel):
    full_name: str = Field(..., json_schema_extra={"example": "Test User"})
    email: EmailStr = Field(..., json_schema_extra={"example": "test@mail.kz"})
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
    language: ResumeLanguage = "kk"
    template: ResumeTemplate = "classic"


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


class GenerateResponse(BaseModel):
    id: int
    resume_text: str
    format: str = "plain"
    generated_by: str
    language: ResumeLanguage = "kk"
    template: ResumeTemplate = "classic"
    analysis: AnalysisResponse | None = None


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(default="", max_length=255)
    role: UserRole = "seeker"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole = "seeker"
    created_at: datetime

    model_config = {"from_attributes": True}


class ResumeSummary(BaseModel):
    id: int
    title: str
    target_job: str
    generated_by: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ResumeDetail(ResumeSummary):
    resume_text: str
    language: ResumeLanguage = "kk"
    template: ResumeTemplate = "classic"
    analysis: AnalysisResponse | None = None


class CompanyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str = ""
    website: str | None = Field(default=None, max_length=512)


class CompanyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    website: str | None = Field(default=None, max_length=512)


class CompanyOut(BaseModel):
    id: int
    user_id: int
    name: str
    description: str
    website: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class VacancyCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = ""
    status: VacancyStatus = "open"


class VacancyUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    status: VacancyStatus | None = None


class VacancyOut(BaseModel):
    id: int
    company_id: int
    title: str
    description: str
    status: VacancyStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class JobOut(BaseModel):
    id: int
    title: str
    description: str
    company_id: int
    company_name: str


class ApplyRequest(BaseModel):
    resume_id: int


class SeekerApplicationOut(BaseModel):
    id: int
    vacancy_id: int
    vacancy_title: str
    resume_id: int | None
    match_score: float
    ranked_by: str
    created_at: datetime


class HrApplicationOut(BaseModel):
    id: int
    vacancy_id: int
    seeker_id: int
    resume_id: int | None
    resume_text: str
    match_score: float
    ranked_by: str
    created_at: datetime

    model_config = {"from_attributes": True}


class HrDashboard(BaseModel):
    role: Literal["hr"] = "hr"
    companies: int
    open_vacancies: int
    applications: int
    average_match_score: float | None = None


class SeekerDashboard(BaseModel):
    role: Literal["seeker"] = "seeker"
    saved_resumes: int
    applications_sent: int
    best_match_score: float | None = None
    open_jobs: int


DashboardOut = Annotated[HrDashboard | SeekerDashboard, Field(discriminator="role")]


class HhVacancyOut(BaseModel):
    id: str
    title: str
    employer_name: str
    area_name: str | None = None
    salary_from: int | None = None
    salary_to: int | None = None
    salary_currency: str | None = None
    published_at: str
    requirement: str | None = None
    responsibility: str | None = None
    experience: str | None = None
    schedule: str | None = None
    url: str  # HH alternate_url


class HhVacancyList(BaseModel):
    found: int
    page: int
    pages: int
    per_page: int
    items: list[HhVacancyOut]
