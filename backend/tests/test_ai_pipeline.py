"""Unit tests for Ollama/BERT orchestration (Ollama mocked; BERT offline)."""

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
from services import bert_analyze, ollama_generate, resume_logic  # noqa: E402


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

    def test_ollama_fallback_when_connection_fails(self):
        from openai import APIConnectionError

        with patch.object(ollama_generate, "ollama_configured", return_value=True), patch(
            "services.ollama_generate.OpenAI"
        ) as client_cls:
            client_cls.return_value.chat.completions.create.side_effect = APIConnectionError(
                request=MagicMock()
            )
            with patch("services.ollama_generate.settings") as st:
                st.ollama_api_key = "ollama"
                st.ollama_model = "llama3.2"
                st.ollama_base_url = "http://127.0.0.1:11434/v1"
                st.ai_allow_fallback = True
                text, label, used = ollama_generate.generate_with_fallback(_sample_payload())
        self.assertFalse(used)
        self.assertEqual(label, "template(ollama-connection-failed)")
        self.assertIn("Test User", text)

    def test_generate_and_analyze_honest_label(self):
        # Force connection failure so we don't need a live Ollama for this unit test.
        from openai import APIConnectionError

        with patch("services.ollama_generate.OpenAI") as client_cls:
            client_cls.return_value.chat.completions.create.side_effect = APIConnectionError(
                request=MagicMock()
            )
            text, analysis, generated_by = resume_logic.generate_and_analyze(_sample_payload())
        self.assertIn("Test User", text)
        self.assertIn("template", generated_by)
        self.assertIn("sentence-transformers", generated_by)
        self.assertNotIn("(demo)", generated_by)
        self.assertIsNotNone(analysis.match_score)

    def test_mocked_ollama_success_label(self):
        fake_msg = MagicMock()
        fake_msg.content = "Ollama Resume\nSkills: React"
        fake_choice = MagicMock()
        fake_choice.message = fake_msg
        fake_resp = MagicMock()
        fake_resp.choices = [fake_choice]

        with patch.object(ollama_generate, "ollama_configured", return_value=True), patch(
            "services.ollama_generate.OpenAI"
        ) as client_cls:
            client_cls.return_value.chat.completions.create.return_value = fake_resp
            with patch("services.ollama_generate.settings") as st:
                st.ollama_api_key = "ollama"
                st.ollama_model = "llama3.2"
                st.ollama_base_url = "http://127.0.0.1:11434/v1"
                st.ai_allow_fallback = True
                text, label, used = ollama_generate.generate_with_fallback(_sample_payload())
        self.assertTrue(used)
        self.assertEqual(label, "llama3.2")
        self.assertTrue(text.startswith("Ollama Resume"))

    def test_rate_limit_fallback_label(self):
        from openai import RateLimitError

        err = RateLimitError(
            message="Error code: 429 - rate_limit_exceeded",
            response=MagicMock(status_code=429, headers={}),
            body={"error": {"code": "rate_limit_exceeded"}},
        )
        with patch.object(ollama_generate, "ollama_configured", return_value=True), patch(
            "services.ollama_generate.OpenAI"
        ) as client_cls:
            client_cls.return_value.chat.completions.create.side_effect = err
            with patch("services.ollama_generate.settings") as st:
                st.ollama_api_key = "ollama"
                st.ollama_model = "llama3.2"
                st.ollama_base_url = "http://127.0.0.1:11434/v1"
                st.ai_allow_fallback = True
                text, label, used = ollama_generate.generate_with_fallback(_sample_payload())
        self.assertFalse(used)
        self.assertEqual(label, "template(ollama-rate-limited)")
        self.assertIn("Test User", text)

    def test_heuristic_english_headings(self):
        from services.heuristic import build_resume_text
        from services.resume_layout import layout_from_input_json, parse_resume_text

        payload = _sample_payload().model_copy(update={"language": "en"})
        text = build_resume_text(payload)
        self.assertIn("EXPERIENCE", text)
        self.assertIn("SKILLS", text)
        self.assertIn("EDUCATION", text)
        self.assertNotIn("ҚЫЗМЕТ ТӘЖІРИБЕСІ", text)
        self.assertNotIn("ДАҒДЫЛАР", text)
        parsed = parse_resume_text(text)
        self.assertEqual(parsed.name, "Test User")
        self.assertTrue(parsed.has_sections)
        self.assertIn("React", parsed.skills)
        language, template = layout_from_input_json(
            '{"language":"ru","template":"modern"}'
        )
        self.assertEqual(language, "ru")
        self.assertEqual(template, "modern")


class RankTests(unittest.TestCase):
    def test_heuristic_fallback_when_bert_offline(self):
        from services import rank

        resume = "python fastapi sql rest docker services"
        with patch.object(
            bert_analyze, "_load_model", side_effect=bert_analyze.BertUnavailable("offline")
        ):
            score, label = rank.rank_resume_against_vacancy(
                resume, "backend developer", "Build REST APIs in Python"
            )
        self.assertEqual(label, "heuristic-keywords")
        self.assertGreater(score, 50)
        self.assertLessEqual(score, 100)

    def test_raises_when_bert_offline_and_fallback_disabled(self):
        from services import rank

        with patch.object(
            bert_analyze, "_load_model", side_effect=bert_analyze.BertUnavailable("offline")
        ), patch("services.rank.settings") as st:
            st.ai_allow_fallback = False
            with self.assertRaises(bert_analyze.BertUnavailable):
                rank.rank_resume_against_vacancy("resume text", "title", "description")

    def test_unknown_title_uses_default_keywords(self):
        from services import heuristic, rank

        self.assertEqual(
            heuristic.expected_keywords("quantum plumber"),
            ["react", "python", "api", "sql"],
        )
        with patch.object(
            bert_analyze, "_load_model", side_effect=bert_analyze.BertUnavailable("offline")
        ):
            score, label = rank.rank_resume_against_vacancy(
                "python api sql react", "quantum plumber", "Pipe the qubits"
            )
        self.assertEqual(label, "heuristic-keywords")
        self.assertGreater(score, 50)

    def test_bert_rank_uses_vacancy_jd(self):
        from services import rank

        score, label = rank.rank_resume_against_vacancy(
            "Frontend developer with React TypeScript HTML CSS and API work",
            "frontend developer",
            "We need React and TypeScript for our UI team.",
        )
        self.assertIn("MiniLM", label)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        self.assertNotEqual(label, "heuristic-keywords")


if __name__ == "__main__":
    unittest.main()
