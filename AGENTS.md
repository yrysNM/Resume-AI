# Agents

Operating manual for Cursor and other coding agents. Read this first, then the matching skill.

## Repo map

- [`backend/`](backend/) — FastAPI 1.2.0 on `:8000` (JWT, SQLite, Groq + BERT, export)
- [`frontend/`](frontend/) — Nuxt 4 SPA (`ssr: false`) on `:3000` (features `auth`, `resume`, `library`)
- Canonical docs: [ARCHITECTURE.md](ARCHITECTURE.md), [BUILD.md](BUILD.md), [README.md](README.md)
- Frontend-only pages: [frontend/README.md](frontend/README.md), [frontend/ARCHITECTURE.md](frontend/ARCHITECTURE.md)

**Read next:** ARCHITECTURE → BUILD → matching skill.

| Area | Skill |
|------|--------|
| `frontend/**` | [`.cursor/skills/senior-frontend/SKILL.md`](.cursor/skills/senior-frontend/SKILL.md) |
| `backend/**` | [`.cursor/skills/senior-backend/SKILL.md`](.cursor/skills/senior-backend/SKILL.md) |
| generate / analyze / export / i18n / auth contract | [`.cursor/skills/resume-ai-domain/SKILL.md`](.cursor/skills/resume-ai-domain/SKILL.md) |

Rules live in [`.cursor/rules/`](.cursor/rules/). Rule `#1` (secrets) always applies.

## Rule #1 — secrets

Do **not** open, read, search, or print `.env`, `.env.*`, `*.db`, dumps, tokens, or API keys. Use `.env.example` for **names** only. If a task needs a secret value, stop and ask a human.

## Hard conventions

- No `any`. Strict TypeScript on the frontend.
- No `$fetch` (or raw `fetch`) in Vue components. HTTP belongs in `*.api.ts` + [`frontend/app/shared/api/http.ts`](frontend/app/shared/api/http.ts).
- Zod in [`frontend/app/shared/schemas/`](frontend/app/shared/schemas/) must mirror [`backend/schemas.py`](backend/schemas.py). Change both together.
- KK + RU + EN together. Same key in `kk.json`, `ru.json`, and `en.json`. Default locale `kk`.
- Features export only via `index.ts`. Pages stay thin: **pages → features → shared**.
- Pinia is auth only. JWT key: `resume_ai_token`.
- Persist resumes on generate only. Analyze does not write. Scope CRUD to `current_user.id`.
- `generated_by` is an honest pipeline label, not a provider to hide.

## Ask a human before

- New dependencies
- `nuxt.config.ts` module changes
- Auth transport changes (cookies, HttpOnly, Nitro proxy)
- Alembic / Postgres
- Anything that needs secret values (`SECRET_KEY`, `GROQ_API_KEY`, …)

## Do not invent

Docker, Playwright CI, HttpOnly cookie auth, SSR for the wizard, vanilla `index.html` / `app.js`, or FastAPI `StaticFiles` for the SPA — unless the user asks.

## Verify

When changing frontend behavior or layout, exercise the flow in the browser (not only a screenshot). Run `pnpm lint`, `pnpm typecheck`, and `pnpm test` from `frontend/`.
