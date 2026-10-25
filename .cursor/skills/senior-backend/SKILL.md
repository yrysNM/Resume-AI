---
name: senior-backend
description: Senior FastAPI engineering for Resume AI — thin routers, Ollama/BERT/heuristic in services, JWT get_current_user, persist-on-generate only, owner-scoped CRUD. Use when changing backend routers, services, models, schemas, auth, export, or health.
---

# Senior FastAPI backend (Resume AI)

App version 1.3.0 in `backend/`. Uvicorn on `:8000`. SQLite via `create_all` — no Alembic unless the user asks.

## Layout

- `main.py` — CORS, `/api/health`, router include
- `routers/` — HTTP only (`auth_router`, `resumes`)
- `services/` — Ollama generate, BERT analyze, heuristic fallback, PDF/DOCX export
- `schemas.py` — Pydantic; mirror in `frontend/app/shared/schemas/`
- `auth.py` — `get_current_user` (HTTP Bearer)
- `models.py` — `User`, `Resume`

## Rules

- Routers stay thin. Ollama / BERT / heuristic stay in `services/`. Do not call the Ollama client or SentenceTransformer from a router.
- Persist a `Resume` row **only** on `POST /api/resume/generate`. `POST /api/resume/analyze` must not write.
- Filter every resume query by `current_user.id`. Missing or other-user ids → **404** (`Resume not found`), not 403.
- `AI_ALLOW_FALLBACK`: true → local template / `heuristic-keywords` and honest `generated_by`. false → HTTP **503** (`OllamaUnavailable` / `BertUnavailable`).
- Raise `HTTPException`. Never print `SECRET_KEY`, JWT, passwords, or API keys.
- Cwd for uvicorn is `backend/` so `sqlite:///./resume_ai.db` stays next to the app.

```python
# ❌ BAD — analyze writes a row
db.add(Resume(...))

# ✅ GOOD — generate commits; analyze returns AnalysisResponse only
```

## Export

`GET /api/resumes/{id}/export?format=pdf|docx`. PDF needs `backend/assets/fonts/DejaVuSans.ttf` (+ Bold). DOCX does not. Unsupported format → 400.

## Tests

No backend test suite yet. Do not add `pytest` / unittest files or mock Ollama unless the user asks. Never read `.env`.

## Ask a human before

Alembic, Postgres, extra LLM providers, rate limits, or any task that needs secret values.
