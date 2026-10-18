"""Unit tests for GPT/BERT orchestration (OpenAI mocked; BERT offline)."""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))

# Ensure fallback-friendly settings before importing app modules.
os.environ.setdefault("AI_ALLOW_FALLBACK", "true")
os.environ["OPENAI_API_KEY"] = ""

from schemas import ExperienceItem, PersonalInfo, ResumeRequest  # noqa: E402
from services import bert_analyze, openai_generate, resume_logic  # noqa: E402


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

    def test_openai_fallback_label_when_no_key(self):
        text, label, used = openai_generate.generate_with_fallback(_sample_payload())
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

    def test_mocked_openai_success_label(self):
        fake_msg = MagicMock()
        fake_msg.content = "GPT Resume\nSkills: React"
        fake_choice = MagicMock()
        fake_choice.message = fake_msg
        fake_resp = MagicMock()
        fake_resp.choices = [fake_choice]

        with patch.object(openai_generate, "openai_configured", return_value=True), patch(
            "services.openai_generate.OpenAI"
        ) as client_cls:
            client_cls.return_value.chat.completions.create.return_value = fake_resp
            with patch("services.openai_generate.settings") as st:
                st.openai_api_key = "sk-test"
                st.openai_model = "gpt-3.5-turbo"
                st.ai_allow_fallback = True
                text, label, used = openai_generate.generate_with_fallback(_sample_payload())
        self.assertTrue(used)
        self.assertEqual(label, "gpt-3.5-turbo")
        self.assertTrue(text.startswith("GPT Resume"))


if __name__ == "__main__":
    unittest.main()
