"""Resume generation and analysis orchestration (GPT-3.5 + BERT).

Primary path:
  - OpenAI chat model (default gpt-3.5-turbo) for resume text
  - sentence-transformers BERT-family embeddings for JD match / keywords

When models are unavailable and AI_ALLOW_FALLBACK=true, falls back to the
local template + keyword heuristics. `generated_by` always names the engines
that actually produced the response (never a fake “demo” label).
"""

from __future__ import annotations

from schemas import AnalysisResponse, ResumeRequest
from services import bert_analyze, openai_generate


def pipeline_label(generator: str, analyzer: str) -> str:
    return f"{generator} + {analyzer}"


def build_resume_text(payload: ResumeRequest) -> tuple[str, str]:
    """Return (resume_text, generator_label)."""
    text, generator, _ = openai_generate.generate_with_fallback(payload)
    return text, generator


def analyze_resume(payload: ResumeRequest) -> tuple[AnalysisResponse, str]:
    """Return (analysis, analyzer_label)."""
    analysis, analyzer, _ = bert_analyze.analyze_with_fallback(payload)
    return analysis, analyzer


def generate_and_analyze(payload: ResumeRequest) -> tuple[str, AnalysisResponse, str]:
    """Return (resume_text, analysis, generated_by)."""
    resume_text, generator = build_resume_text(payload)
    analysis, analyzer = analyze_resume(payload)
    return resume_text, analysis, pipeline_label(generator, analyzer)
