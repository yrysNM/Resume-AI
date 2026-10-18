"""Pydantic request/response schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


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
    analysis: AnalysisResponse | None = None


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(default="", max_length=255)


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
    analysis: AnalysisResponse | None = None
