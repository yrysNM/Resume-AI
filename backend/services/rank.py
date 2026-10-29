"""Score applications against a vacancy (BERT cosine or heuristic keywords)."""

from __future__ import annotations

import logging
import re

from config import settings
from services.heuristic import expected_keywords

logger = logging.getLogger(__name__)


class RankUnavailable(Exception):
    """Raised when ranking engines are down and fallback is disabled."""


def rank_resume_against_vacancy(resume_text: str, title: str, description: str) -> tuple[float, str]:
    """Return (match_score 0–100, ranked_by label)."""
    jd = f"{title}\n{description}".strip()
    from services import bert_analyze

    try:
        sim = bert_analyze.cosine_similarity(resume_text or "", jd or title)
        score = max(0.0, min(100.0, round(sim * 100.0, 1)))
        return score, settings.bert_model_name
    except bert_analyze.BertUnavailable:
        if not settings.ai_allow_fallback:
            raise
        return _heuristic_score(resume_text, title), "heuristic-keywords"
    except Exception as exc:  # noqa: BLE001 — unexpected encoder failures
        logger.info("rank BERT failed: %s", type(exc).__name__)
        if not settings.ai_allow_fallback:
            raise RankUnavailable("BERT ranking unavailable") from exc
        return _heuristic_score(resume_text, title), "heuristic-keywords"


# Back-compat alias used by routers written against an earlier name.
score_resume_against_vacancy = rank_resume_against_vacancy


def _heuristic_score(resume_text: str, title: str) -> float:
    expected = expected_keywords(title)
    text = (resume_text or "").lower()
    found = sum(1 for kw in expected if kw.lower() in text)
    if not expected:
        return 50.0
    # Light lexical boost from shared tokens
    title_tokens = {t for t in re.findall(r"[a-zA-Zа-яА-ЯёЁәіңғүұқөһӘІҢҒҮҰҚӨҺ0-9]+", title.lower()) if len(t) > 2}
    overlap = sum(1 for t in title_tokens if t in text)
    raw = (found / len(expected)) * 70.0 + min(30.0, overlap * 5.0)
    return round(min(100.0, max(0.0, raw)), 1)
