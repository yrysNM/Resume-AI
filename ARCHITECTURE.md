# Architecture

Source of truth for the FastAPI + Nuxt split. Frontend-only layout also lives in [frontend/ARCHITECTURE.md](frontend/ARCHITECTURE.md).

## Split

The Nuxt SPA on `:3000` calls FastAPI on `:8000` directly. There is no Nitro server route or `$fetch` proxy.

- CORS origins: `http://localhost:3000`, `http://127.0.0.1:3000` (override with `CORS_ORIGINS`)
- Auth: `Authorization: Bearer <jwt>`. Token is stored in `localStorage` under `resume_ai_token`
- `allow_credentials` is false; this is not cookie auth

Do **not** “fix” unasked: SQLite + `create_all` (no Alembic), SPA `ssr: false`, no HttpOnly cookies, no pagination on the library.

## Backend (`backend/`)

| File | Role |
|------|------|
| [`main.py`](backend/main.py) | FastAPI app, CORS, `/api/health`, router mount |
| [`config.py`](backend/config.py) | Settings from env names in [`.env.example`](.env.example) |
| [`auth.py`](backend/auth.py) | bcrypt, JWT, `get_current_user` |
| [`database.py`](backend/database.py) | SQLAlchemy engine, `init_db` → `create_all` plus SQLite `users.role` ALTER |
| [`models.py`](backend/models.py) | `User` (`role` seeker\|hr), `Resume`, `Company`, `Vacancy`, `Application` |
| [`schemas.py`](backend/schemas.py) | Pydantic request/response models |
| [`routers/`](backend/routers/) | Thin HTTP: `auth_router`, `resumes`, `companies`, `vacancies`, `jobs`, `dashboard` |
| [`services/`](backend/services/) | Ollama → BERT → heuristic fallback, export, vacancy rank |

Run uvicorn with cwd `backend/` so `DATABASE_URL=sqlite:///./resume_ai.db` creates `backend/resume_ai.db`.

## Frontend (`frontend/`)

Nuxt 4 SPA (`ssr: false`). Dependency rule: **pages → features → shared**. Features export only via `index.ts`.

Features: `auth`, `resume`, `library`. Shell UI (`LangSwitch`, `WizardSteps`) lives in `app/components/`.

| Concern | Mechanism |
|---------|-----------|
| Auth user + JWT | Pinia `useAuthStore` (`resume_ai_token`) |
| Wizard step + form | `useState` in `useResumeWizard` |
| Generate/preview result | `useState` in `useResumeResult` |
| Saved resumes | `useAsyncData('saved-resumes')` in `useResumeLibrary` |

Zod in [`frontend/app/shared/schemas/`](frontend/app/shared/schemas/) mirrors [`backend/schemas.py`](backend/schemas.py).

Locales: KK / RU / EN in `frontend/i18n/locales/`. Default locale `kk`, strategy `no_prefix`.

## Data flow

1. User fills the four-step wizard (`useResumeWizard`).
2. Generate calls `resume.api` → `shared/api/http.ts` (`apiRequest`) with Bearer token.
3. FastAPI generates, analyzes, and **persists** a `Resume` row owned by `current_user`.
4. Result lands in `useResumeResult`; the library list refreshes.
5. Analyze-only (`POST /api/resume/analyze`) does **not** write a row.
6. Export downloads a blob via `apiBlob` (`format=pdf|docx`).

## API

| Method | Path | Auth | Notes |
|--------|------|------|-------|
| GET | `/api/health` | no | Ollama/BERT flags |
| POST | `/api/auth/register` | no | 201 `TokenResponse` |
| POST | `/api/auth/login` | no | `TokenResponse` |
| GET | `/api/auth/me` | Bearer | `UserOut` |
| POST | `/api/resume/generate` | Bearer | Persists row; `GenerateResponse` |
| POST | `/api/resume/analyze` | Bearer | No persist |
| GET | `/api/resumes` | Bearer | Owner list, no pagination |
| GET | `/api/resumes/{id}` | Bearer | 404 if not owner |
| DELETE | `/api/resumes/{id}` | Bearer | 204; 404 if not owner |
| GET | `/api/resumes/{id}/export?format=` | Bearer | `pdf` or `docx`; optional `template=` |
| GET/POST | `/api/companies` | Bearer HR | list/create own companies; seeker → 403 |
| GET/PUT/DELETE | `/api/companies/{id}` | Bearer HR | owner-scoped; else 404 |
| GET/POST | `/api/companies/{id}/vacancies` | Bearer HR | vacancies under an owned company |
| GET/PUT/DELETE | `/api/companies/{id}/vacancies/{vacancy_id}` | Bearer HR | owner-scoped vacancy; else 404 |
| GET | `/api/vacancies/{id}` | Bearer HR | owner-scoped vacancy; else 404 |
| GET | `/api/vacancies/{id}/applications` | Bearer HR | applications by `match_score` desc |
| POST | `/api/vacancies/{id}/rank` | Bearer HR | recompute scores; 503 if BERT down and fallback off |
| GET | `/api/jobs` | Bearer seeker | open vacancies (title, company name, description) |
| POST | `/api/jobs/{id}/apply` | Bearer seeker | `{ resume_id }`; 404 if resume not owned; 409 if already applied or vacancy closed |
| GET | `/api/applications` | Bearer seeker | own applications + vacancy title + score |
| GET | `/api/dashboard` | Bearer | HR or seeker stats payload (`role` discriminator) |

Base URL for the SPA: `runtimeConfig.public.apiBase` ← `NUXT_PUBLIC_API_BASE` (default `http://127.0.0.1:8000`).

## AI pipeline

Orchestrated in [`services/resume_logic.py`](backend/services/resume_logic.py):

1. **Generate** — Ollama Chat Completions (OpenAI-compatible client, `OLLAMA_MODEL`).
2. **Analyze** — sentence-transformers BERT (`BERT_MODEL_NAME`) for JD similarity and keywords.
3. **Fallback** — local template + keyword heuristics when models fail **and** `AI_ALLOW_FALLBACK` is true. Otherwise generate/analyze/apply/rank return HTTP 503.
4. **Rank** — [`services/rank.py`](backend/services/rank.py): BERT cosine between stored `resume_text` and vacancy **title + description**, plus lexical overlap from `expected_keywords(title)` only. Persist `match_score` and honest `ranked_by` on apply; `POST /api/vacancies/{id}/rank` recomputes.

`generated_by` is an honest label of what actually ran, e.g. `{generator} + {analyzer}`:

- Generator: the Ollama model name, `template(ollama-…)`, or `template`
- Analyzer: the BERT model name, or `heuristic-keywords`
- Ranker (`ranked_by`): the BERT model name, or `heuristic-keywords`

Do not hide fallback behind a fake provider name.

`User.role` is `seeker` or `hr` (default `seeker`). `create_all` does not alter existing `users`; `init_db` runs a SQLite-only `ALTER TABLE users ADD COLUMN role` when the column is missing. Wrong-role calls return **403**. Missing/other-owner company, vacancy, or resume → **404**.

Heuristic keyword map is **three** job titles only (`frontend developer`, `backend developer`, `data scientist`). Do not silently expand it.

Generated text uses `language` (`kk` / `ru` / `en`) for section titles and body. `template` (`classic` / `modern` / `minimal`) is a layout for preview and PDF/DOCX export.
