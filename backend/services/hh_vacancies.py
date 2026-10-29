"""HeadHunter public vacancy search (HR market watch). Stdlib urllib only."""

from __future__ import annotations

import json
import logging
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from config import settings
from schemas import HhVacancyList, HhVacancyOut

logger = logging.getLogger(__name__)

# Category 12 — Управление персоналом, тренинги (HR / training roles)
_HH_HR_ROLES = ("17", "38", "69", "117", "118", "153", "171", "181")
_HIGHLIGHT_RE = re.compile(r"</?highlighttext>", re.IGNORECASE)
_TIMEOUT_S = 10


class HhUnavailable(Exception):
    """Raised when HeadHunter cannot be reached or returns a non-200."""


def fetch_hr_vacancies(page: int = 0) -> HhVacancyList:
    page = max(0, int(page))
    per_page = max(1, min(100, int(settings.hh_per_page)))

    query: list[tuple[str, str]] = [
        ("area", str(settings.hh_area)),
        ("per_page", str(per_page)),
        ("page", str(page)),
        ("order_by", "publication_time"),
    ]
    for role in _HH_HR_ROLES:
        query.append(("professional_role", role))

    base = settings.hh_api_base.rstrip("/")
    url = f"{base}/vacancies?{urllib.parse.urlencode(query)}"
    headers = {
        "User-Agent": settings.hh_user_agent,
        "HH-User-Agent": settings.hh_user_agent,
        "Accept": "application/json",
    }
    req = urllib.request.Request(url, headers=headers, method="GET")

    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT_S) as resp:  # noqa: S310 — configured base URL
            raw = resp.read().decode("utf-8")
            status = getattr(resp, "status", 200)
    except urllib.error.HTTPError as exc:
        logger.warning("HH HTTP %s", exc.code)
        raise HhUnavailable(f"HeadHunter HTTP {exc.code}") from exc
    except Exception as exc:  # noqa: BLE001
        logger.warning("HH request failed: %s", type(exc).__name__)
        raise HhUnavailable("HeadHunter unavailable") from exc

    if status != 200:
        raise HhUnavailable(f"HeadHunter HTTP {status}")

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise HhUnavailable("HeadHunter returned invalid JSON") from exc

    items = [_map_item(item) for item in (payload.get("items") or [])]
    return HhVacancyList(
        found=int(payload.get("found") or 0),
        page=int(payload.get("page") or page),
        pages=int(payload.get("pages") or 0),
        per_page=int(payload.get("per_page") or per_page),
        items=items,
    )


def _strip_highlight(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = _HIGHLIGHT_RE.sub("", value).strip()
    return cleaned or None


def _map_item(item: dict[str, Any]) -> HhVacancyOut:
    salary = item.get("salary") or {}
    snippet = item.get("snippet") or {}
    experience = item.get("experience") or {}
    schedule = item.get("schedule") or {}
    employer = item.get("employer") or {}
    area = item.get("area") or {}

    return HhVacancyOut(
        id=str(item.get("id") or ""),
        title=str(item.get("name") or ""),
        employer_name=str(employer.get("name") or ""),
        area_name=(str(area["name"]) if area.get("name") else None),
        salary_from=salary.get("from"),
        salary_to=salary.get("to"),
        salary_currency=(str(salary["currency"]) if salary.get("currency") else None),
        published_at=str(item.get("published_at") or ""),
        requirement=_strip_highlight(snippet.get("requirement")),
        responsibility=_strip_highlight(snippet.get("responsibility")),
        experience=(str(experience["name"]) if experience.get("name") else None),
        schedule=(str(schedule["name"]) if schedule.get("name") else None),
        url=str(item.get("alternate_url") or item.get("url") or ""),
    )
