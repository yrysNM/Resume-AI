"""Locale headings and analysis copy for generated resumes."""

from __future__ import annotations

from dataclasses import dataclass

from schemas import ResumeLanguage

_LANGUAGE_NAMES: dict[ResumeLanguage, str] = {
    "kk": "Kazakh",
    "ru": "Russian",
    "en": "English",
}


@dataclass(frozen=True)
class ResumeHeadings:
    experience: str
    skills: str
    education: str
    target: str


@dataclass(frozen=True)
class IssueCopy:
    experience_section: str
    experience_message: str
    experience_suggestion: str
    skills_section: str
    skills_message: str
    skills_suggestion: str
    keywords_section: str
    keywords_message: str
    keywords_suggestion: str
    match_section: str
    match_message: str
    match_suggestion: str


_HEADINGS: dict[ResumeLanguage, ResumeHeadings] = {
    "kk": ResumeHeadings(
        experience="ҚЫЗМЕТ ТӘЖІРИБЕСІ",
        skills="ДАҒДЫЛАР",
        education="БІЛІМ",
        target="Мақсатты лауазым",
    ),
    "ru": ResumeHeadings(
        experience="ОПЫТ РАБОТЫ",
        skills="НАВЫКИ",
        education="ОБРАЗОВАНИЕ",
        target="Целевая должность",
    ),
    "en": ResumeHeadings(
        experience="EXPERIENCE",
        skills="SKILLS",
        education="EDUCATION",
        target="Target role",
    ),
}

_ISSUE_COPY: dict[ResumeLanguage, IssueCopy] = {
    "kk": IssueCopy(
        experience_section="Қызмет тәжірибесі",
        experience_message="Тәжірибе бөлімі толтырылмаған",
        experience_suggestion="Кемінде бір жұмыс орнын қосыңыз",
        skills_section="Дағдылар",
        skills_message="Дағдылар тізімі тым қысқа",
        skills_suggestion="Кемінде 3 дағды қосыңыз",
        keywords_section="Кілт сөздер",
        keywords_message="«{kw}» кілт сөзі жоқ",
        keywords_suggestion="Түйіндемеге «{kw}» қосыңыз",
        match_section="Сәйкестік",
        match_message="Мақсатты лауазыммен сәйкестік төмен",
        match_suggestion="Дағдылар мен тәжірибені мақсатты рөлге жақындатыңыз",
    ),
    "ru": IssueCopy(
        experience_section="Опыт работы",
        experience_message="Раздел опыта пуст",
        experience_suggestion="Добавьте хотя бы одно место работы",
        skills_section="Навыки",
        skills_message="Список навыков слишком короткий",
        skills_suggestion="Добавьте минимум 3 навыка",
        keywords_section="Ключевые слова",
        keywords_message="Нет ключевого слова «{kw}»",
        keywords_suggestion="Добавьте «{kw}» в резюме",
        match_section="Соответствие",
        match_message="Низкое соответствие целевой должности",
        match_suggestion="Приблизьте навыки и опыт к целевой роли",
    ),
    "en": IssueCopy(
        experience_section="Experience",
        experience_message="Experience section is empty",
        experience_suggestion="Add at least one role",
        skills_section="Skills",
        skills_message="Skills list is too short",
        skills_suggestion="Add at least 3 skills",
        keywords_section="Keywords",
        keywords_message="Missing keyword “{kw}”",
        keywords_suggestion="Include “{kw}” in the resume",
        match_section="Match",
        match_message="Low match to the target role",
        match_suggestion="Align skills and experience with the target role",
    ),
}


def language_name(language: ResumeLanguage | str) -> str:
    key: ResumeLanguage = language if language in _LANGUAGE_NAMES else "en"  # type: ignore[assignment]
    return _LANGUAGE_NAMES[key]


def headings_for(language: ResumeLanguage | str) -> ResumeHeadings:
    key: ResumeLanguage = language if language in _HEADINGS else "en"  # type: ignore[assignment]
    return _HEADINGS[key]


def issue_copy_for(language: ResumeLanguage | str) -> IssueCopy:
    key: ResumeLanguage = language if language in _ISSUE_COPY else "en"  # type: ignore[assignment]
    return _ISSUE_COPY[key]
