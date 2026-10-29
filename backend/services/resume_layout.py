"""Parse plain-text resumes into named sections for PDF/DOCX export."""

from __future__ import annotations

import json
from dataclasses import dataclass

from schemas import ResumeLanguage, ResumeTemplate
from services.resume_i18n import headings_for


@dataclass
class ParsedResume:
    raw: str
    name: str = ""
    headline: str = ""
    target: str = ""
    experience: str = ""
    skills: str = ""
    education: str = ""
    has_sections: bool = False


def parse_resume_text(resume_text: str) -> ParsedResume:
    text = (resume_text or "").strip()
    parsed = ParsedResume(raw=text)
    if not text:
        return parsed

    lines = text.splitlines()
    parsed.name = lines[0].strip()
    if len(lines) > 1 and lines[1].strip() and not _is_heading(lines[1]):
        parsed.headline = lines[1].strip()

    # Collect known headings across locales so exports work for kk/ru/en text.
    heading_map: dict[str, str] = {}
    for lang in ("kk", "ru", "en"):
        h = headings_for(lang)
        heading_map[h.experience.upper()] = "experience"
        heading_map[h.skills.upper()] = "skills"
        heading_map[h.education.upper()] = "education"
        heading_map[h.target.upper()] = "target"
        heading_map[f"{h.target.upper()}:"] = "target"

    current: str | None = None
    buckets: dict[str, list[str]] = {
        "experience": [],
        "skills": [],
        "education": [],
        "target": [],
    }

    start = 2 if parsed.headline else 1
    for line in lines[start:]:
        stripped = line.strip()
        key = heading_map.get(stripped.upper())
        if key is None and stripped.upper().endswith(":"):
            key = heading_map.get(stripped.upper())
        if key is not None:
            current = key
            parsed.has_sections = True
            # Inline "Target: value" style
            if key == "target" and ":" in stripped:
                after = stripped.split(":", 1)[1].strip()
                if after:
                    buckets["target"].append(after)
                    current = None
            continue
        if current is None:
            continue
        buckets[current].append(line)

    parsed.experience = "\n".join(buckets["experience"]).strip()
    parsed.skills = "\n".join(buckets["skills"]).strip()
    parsed.education = "\n".join(buckets["education"]).strip()
    parsed.target = "\n".join(buckets["target"]).strip()
    return parsed


def _is_heading(line: str) -> bool:
    upper = line.strip().upper()
    for lang in ("kk", "ru", "en"):
        h = headings_for(lang)
        if upper in {
            h.experience.upper(),
            h.skills.upper(),
            h.education.upper(),
            h.target.upper(),
        }:
            return True
    return False


def layout_from_input_json(raw: str | None) -> tuple[ResumeLanguage, ResumeTemplate]:
    """Read language/template from a stored Resume.input_json payload."""
    language: ResumeLanguage = "kk"
    template: ResumeTemplate = "classic"
    if not raw:
        return language, template
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return language, template
    lang = data.get("language")
    tmpl = data.get("template")
    if lang in ("kk", "ru", "en"):
        language = lang
    if tmpl in ("classic", "modern", "minimal"):
        template = tmpl
    return language, template
