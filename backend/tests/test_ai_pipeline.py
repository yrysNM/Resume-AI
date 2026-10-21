"""Unit tests for Groq/BERT orchestration (Groq mocked; BERT offline)."""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))

os.environ.setdefault("AI_ALLOW_FALLBACK", "true")
os.environ["GROQ_API_KEY"] = ""
os.environ["OPENAI_API_KEY"] = ""

from schemas import ExperienceItem, PersonalInfo, ResumeRequest  # noqa: E402
from services import bert_analyze, groq_generate, resume_logic  # noqa: E402


def _sample_payload() -> ResumeRequest:
    return ResumeRequest(
        personal=PersonalInfo(
            full_name="Test User",
            email="test@mail.kz",
            phone="+7 777",
            position="Frontend Dev",
        ),
        skills=["React", "TypeScript", "HTML", "CSS", "API"],
        experience=[
            ExperienceItem(
                company="Tech",
                role="Junior",
                period="2024",
                description="Built React TypeScript REST API UIs",
            )
        ],
        education="NU",
        target_job="frontend developer",
    )


class PipelineTests(unittest.TestCase):
    def test_bert_analysis_runs(self):
        analysis, label, used = bert_analyze.analyze_with_fallback(_sample_payload())
        self.assertTrue(used)
        self.assertIn("MiniLM", label)
        self.assertGreaterEqual(analysis.match_score, 0)
        self.assertLessEqual(analysis.match_score, 100)
        self.assertTrue(analysis.keywords_found)

    def test_groq_fallback_label_when_no_key(self):
        text, label, used = groq_generate.generate_with_fallback(_sample_payload())
        self.assertFalse(used)
        self.assertEqual(label, "template")
        self.assertIn("Test User", text)

    def test_generate_and_analyze_honest_label(self):
        text, analysis, generated_by = resume_logic.generate_and_analyze(_sample_payload())
        self.assertIn("Test User", text)
        self.assertIn("template", generated_by)
        self.assertIn("sentence-transformers", generated_by)
        self.assertNotIn("(demo)", generated_by)
        self.assertIsNotNone(analysis.match_score)

    def test_mocked_groq_success_label(self):
        fake_msg = MagicMock()
        fake_msg.content = "Groq Resume\nSkills: React"
        fake_choice = MagicMock()
        fake_choice.message = fake_msg
        fake_resp = MagicMock()
        fake_resp.choices = [fake_choice]

        with patch.object(groq_generate, "groq_configured", return_value=True), patch(
            "services.groq_generate.OpenAI"
        ) as client_cls:
            client_cls.return_value.chat.completions.create.return_value = fake_resp
            with patch("services.groq_generate.settings") as st:
                st.groq_api_key = "gsk-test"
                st.groq_model = "qwen/qwen3.8-27b"
                st.groq_base_url = "https://api.groq.com/openai/v1"
                st.ai_allow_fallback = True
                text, label, used = groq_generate.generate_with_fallback(_sample_payload())
        self.assertTrue(used)
        self.assertEqual(label, "qwen/qwen3.8-27b")
        self.assertTrue(text.startswith("Groq Resume"))

    def test_rate_limit_fallback_label(self):
        from openai import RateLimitError

        err = RateLimitError(
            message="Error code: 429 - rate_limit_exceeded",
            response=MagicMock(status_code=429, headers={}),
            body={"error": {"code": "rate_limit_exceeded"}},
        )
        with patch.object(groq_generate, "groq_configured", return_value=True), patch(
            "services.groq_generate.OpenAI"
        ) as client_cls:
            client_cls.return_value.chat.completions.create.side_effect = err
            with patch("services.groq_generate.settings") as st:
                st.groq_api_key = "gsk-test"
                st.groq_model = "qwen/qwen3.8-27b"
                st.groq_base_url = "https://api.groq.com/openai/v1"
                st.ai_allow_fallback = True
                text, label, used = groq_generate.generate_with_fallback(_sample_payload())
        self.assertFalse(used)
        self.assertEqual(label, "template(groq-rate-limited)")
        self.assertIn("Test User", text)


if __name__ == "__main__":
    unittest.main()
