---
name: resume-ai-domain
description: Resume AI domain rules for the four-step wizard, ResumeRequest shape, honest generated_by labels, PDF/DOCX export, Kazakh section titles, and the three-title heuristic keyword map. Use when changing generate, analyze, export, i18n copy, or the auth/API contract.
---

# Resume AI domain

Product: KK / RU / EN wizard that generates a CV, scores it, saves a private library, and exports files.

## Wizard (steps 1–4)

| Step | UI | Payload fields |
|------|-----|----------------|
| 1 | Personal | `personal` (`full_name`, `email`, `phone`, `position`), plus `target_job`, `education` |
| 2 | Experience | `experience[]` (`company`, `role`, `period`, `description`) |
| 3 | Skills | `skills[]` (comma-split tags in the form) |
| 4 | Preview | generate + analysis; `language` + `template`; export when `id` exists |

Home is public. Generate, analyze, library, and export require Bearer JWT (`resume_ai_token`).

## `ResumeRequest`

Pydantic (`backend/schemas.py`) and Zod (`frontend/app/shared/schemas/resume.ts`) must match:

- `personal`, `skills`, `experience`, `education`, `target_job`, `language` (`kk` \| `ru` \| `en`), `template` (`classic` \| `modern` \| `minimal`)

Do not add fields on one side only. Auth contract: `UserRegister` (password 8–128, optional `role` `seeker` \| `hr` default `seeker`), `UserLogin`, `TokenResponse`, `UserOut` (`id`, `email`, `full_name`, `role`, `created_at`).

## `generated_by`

A **label** of engines that actually ran (`{generator} + {analyzer}`), not a provider name to hide.

- Generator: Ollama model id, `template(ollama-…)`, or `template`
- Analyzer: BERT model id, or `heuristic-keywords`

Never rewrite fallback as if Ollama/BERT succeeded. UI copy uses the `generated_by` i18n key (“Pipeline”).

Application `ranked_by` follows the same honesty rule: `BERT_MODEL_NAME`, or `heuristic-keywords` when BERT is down and `AI_ALLOW_FALLBACK` is true. Apply/re-rank return HTTP 503 if BERT is down and fallback is off.

## Export

`format=pdf|docx` query on `GET /api/resumes/{id}/export`. Optional `template=classic|modern|minimal` overrides the stored layout. Owner-scoped 404. PDF needs DejaVu fonts; DOCX does not.

## Generated text

Write section titles **and** body in `language` (`kk` / `ru` / `en`). Use these exact headings:

| Lang | Experience | Skills | Education | Target |
|------|------------|--------|-----------|--------|
| kk | ҚЫЗМЕТ ТӘЖІРИБЕСІ | ДАҒДЫЛАР | БІЛІМ | Мақсатты лауазым |
| ru | ОПЫТ РАБОТЫ | НАВЫКИ | ОБРАЗОВАНИЕ | Целевая должность |
| en | EXPERIENCE | SKILLS | EDUCATION | Target role |

Do not invent employers, degrees, or skills absent from the payload. `template` is layout only (preview + PDF/DOCX); it does not change the LLM path.

## Heuristic keyword map

Only three titles in `services/heuristic.py` `SKILL_KEYWORDS`:

- `frontend developer`
- `backend developer`
- `data scientist`

Unknown titles use the default list `react`, `python`, `api`, `sql`. **Do not silently expand** the map unless the task is to expand it.

## i18n

Same message key in `kk.json`, `ru.json`, and `en.json`. Default locale `kk`.
