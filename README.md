# Resume AI

A KK / RU / EN resume wizard: sign in with JWT, generate a CV with Ollama, score it with BERT, save a private library, and export PDF or DOCX.

**Stack:** FastAPI (app version 1.3.0) in [`backend/`](backend/) on `:8000`; Nuxt 4 SPA (`ssr: false`) in [`frontend/`](frontend/) on `:3000`. The browser talks to FastAPI over CORS with a Bearer token in `localStorage` (`resume_ai_token`). Nuxt does **not** proxy the API through Nitro.

- [ARCHITECTURE.md](ARCHITECTURE.md) — full-stack layout, API, and AI pipeline
- [BUILD.md](BUILD.md) — how to run, lint, typecheck, and test
- [AGENTS.md](AGENTS.md) — conventions for coding agents

## Quick start

Copy [`.env.example`](.env.example) to `.env` at the repo root. A human must set `SECRET_KEY`. Resume text comes from a local Ollama server (`OLLAMA_BASE_URL`, default model `llama3.2`). Copy [`frontend/.env.example`](frontend/.env.example) to `frontend/.env` only if you need a non-default `NUXT_PUBLIC_API_BASE`. Never open or print `.env`.

Two terminals:

```bash
# Terminal 1 — cwd must be backend/ so SQLite ./resume_ai.db lands there
cd backend
python -m venv .venv
# activate .venv, then:
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

```bash
# Terminal 2
cd frontend
pnpm install
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000). API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

This repo has no Docker or CI.
