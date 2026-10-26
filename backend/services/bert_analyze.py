"""BERT-family embedding analysis via sentence-transformers."""

from __future__ import annotations

import logging
import threading
from typing import Any

import numpy as np

from config import settings
from schemas import AnalysisIssue, AnalysisResponse, ResumeRequest
from services import heuristic
from services.resume_i18n import issue_copy_for

logger = logging.getLogger(__name__)

_model_lock = threading.Lock()
_model: Any | None = None
_model_error: str | None = None


class BertUnavailable(Exception):
    """Raised when the embedding model cannot be used."""


def bert_model_name() -> str:
    return settings.bert_model_name


def _load_model() -> Any:
    global _model, _model_error
    if _model is not None:
        return _model
    if _model_error is not None and not settings.bert_retry_load:
        raise BertUnavailable(_model_error)

    with _model_lock:
        if _model is not None:
            return _model
        try:
            from sentence_transformers import SentenceTransformer

            _model = SentenceTransformer(settings.bert_model_name)
            _model_error = None
            return _model
        except Exception as exc:  # model download / import failures
            _model_error = f"Failed to load BERT model '{settings.bert_model_name}': {exc}"
            logger.exception("BERT model load failed")
            raise BertUnavailable(_model_error) from exc


def bert_available() -> bool:
    try:
        _load_model()
        return True
    except BertUnavailable:
        return False


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def cosine_similarity(text_a: str, text_b: str) -> float:
    """Return cosine similarity in [0, 1]. Raises BertUnavailable if the model cannot load."""
    model = _load_model()
    embeddings = model.encode(
        [text_a.strip() or "(empty)", text_b.strip() or "(empty)"],
        normalize_embeddings=True,
    )
    a = np.asarray(embeddings[0], dtype=np.float32)
    b = np.asarray(embeddings[1], dtype=np.float32)
    return max(0.0, min(1.0, _cosine(a, b)))


def _resume_corpus(payload: ResumeRequest) -> str:
    parts = [
        payload.personal.position,
        payload.education,
        " ".join(payload.skills),
        " ".join(f"{e.role} {e.company} {e.description}" for e in payload.experience),
        payload.target_job,
    ]
    return " ".join(p for p in parts if p).strip()


def _jd_text(payload: ResumeRequest) -> str:
    target = payload.target_job or payload.personal.position
    expected = heuristic.expected_keywords(target)
    return f"{target} role requiring {', '.join(expected)}"


def analyze_with_bert(payload: ResumeRequest) -> AnalysisResponse:
    model = _load_model()
    resume_text = _resume_corpus(payload)
    jd_text = _jd_text(payload)
    expected = heuristic.expected_keywords(payload.target_job or payload.personal.position)

    embeddings = model.encode(
        [resume_text or "(empty resume)", jd_text, *expected],
        normalize_embeddings=True,
    )
    resume_vec = np.asarray(embeddings[0], dtype=np.float32)
    jd_vec = np.asarray(embeddings[1], dtype=np.float32)
    keyword_vecs = [np.asarray(v, dtype=np.float32) for v in embeddings[2:]]

    # Cosine similarity in [0, 1] after normalization → match percentage.
    similarity = max(0.0, min(1.0, _cosine(resume_vec, jd_vec)))
    match_score = round(similarity * 100.0, 1)

    found: list[str] = []
    missing: list[str] = []
    resume_lower = resume_text.lower()
    threshold = settings.bert_keyword_threshold
    for kw, vec in zip(expected, keyword_vecs):
        # Prefer lexical hit; otherwise use embedding proximity to the keyword.
        if kw in resume_lower or _cosine(resume_vec, vec) >= threshold:
            found.append(kw)
        else:
            missing.append(kw)

    completeness = min(100.0, 40 + len(payload.skills) * 8 + len(payload.experience) * 15)
    precision = round(len(found) / max(len(found) + len(missing), 1), 2)
    recall = round(len(found) / max(len(expected), 1), 2)

    issues: list[AnalysisIssue] = heuristic.base_issues(payload, missing)
    if match_score < 55:
        copy = issue_copy_for(payload.language)
        issues.append(
            AnalysisIssue(
                section=copy.match_section,
                severity="high",
                message=copy.match_message,
                suggestion=copy.match_suggestion,
            )
        )

    return AnalysisResponse(
        completeness_score=round(completeness, 1),
        match_score=match_score,
        precision=precision,
        recall=recall,
        issues=issues,
        keywords_found=found,
        keywords_missing=missing,
    )


def analyze_with_fallback(payload: ResumeRequest) -> tuple[AnalysisResponse, str, bool]:
    """Return (analysis, analyzer_label, used_bert)."""
    try:
        return analyze_with_bert(payload), settings.bert_model_name, True
    except BertUnavailable:
        if not settings.ai_allow_fallback:
            raise
        return heuristic.analyze_resume(payload), "heuristic-keywords", False
