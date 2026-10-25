# Resume-AI Frontend Architecture

Full-stack: see root [ARCHITECTURE.md](../ARCHITECTURE.md).

Nuxt 4 SPA (`ssr: false`) that talks to the FastAPI backend over JWT Bearer auth.

## Stack

- **Nuxt 4** + Vue 3 `<script setup lang="ts">` (strict TypeScript)
- **@nuxt/ui** (primary: sky, neutral: slate — dark slate + sky accent)
- **Pinia** for auth session
- **@nuxtjs/i18n** — KK / RU / EN (`i18n/locales/`)
- **Zod** schemas mirroring `backend/schemas.py`
- **Vitest** smoke tests for schemas, auth store, wizard

## Layout

```
frontend/
├── app/
│   ├── app.vue
│   ├── error.vue
│   ├── assets/css/main.css
│   ├── components/             # LangSwitch, WizardSteps (shell UI)
│   ├── layouts/default.vue
│   ├── middleware/auth.ts
│   ├── pages/index.vue         # thin: sidebar + ResumeWizard
│   ├── plugins/                # auth + locale bootstrap
│   ├── features/
│   │   ├── auth/               # store, api, LoginModal, AuthBar
│   │   ├── resume/             # wizard form/state, generate, export, preview
│   │   ├── library/            # saved list open/delete
│   │   └── i18n/               # locale feature marker
│   └── shared/
│       ├── api/http.ts         # fetch + Bearer + AppError + blob download
│       ├── schemas/            # Zod boundary types
│       ├── constants/
│       ├── types/
│       └── utils/
├── i18n/locales/{kk,ru,en}.json
├── nuxt.config.ts
├── .env.example                # NUXT_PUBLIC_API_BASE only
└── ARCHITECTURE.md
```

**Dependency rule:** `pages → features → shared`. Features export via `index.ts`. Components do not call `$fetch` directly.

## Shared client state

| Concern | Mechanism |
|---------|-----------|
| Auth user + JWT | Pinia `useAuthStore` (`resume_ai_token` in `localStorage`) |
| Wizard step + form | `useState` in `useResumeWizard` |
| Generate/preview result | `useState` in `useResumeResult` |
| Saved resumes | `useAsyncData('saved-resumes')` in `useResumeLibrary` |

## Data flow

1. User fills wizard (`useResumeWizard` form).
2. Generate calls `resume.api` → `shared/api/http` with Bearer token.
3. Result lands in `useResumeResult`; library list refreshes.
4. Open/delete saved resumes updates result + step via library composable.

## Auth

- Public home wizard; generate / export call `requireAuth()` and open `LoginModal` on 401.
- Plugin `auth.client.ts` refreshes `/api/auth/me` on startup.
- Middleware `auth.ts` available for future protected routes (not on `/`).

## API surface (client)

| Method | Path | Feature |
|--------|------|---------|
| POST | `/api/auth/login`, `/api/auth/register` | auth |
| GET | `/api/auth/me` | auth |
| POST | `/api/resume/generate`, `/api/resume/analyze` | resume |
| GET/DELETE | `/api/resumes`, `/api/resumes/:id` | library |
| GET | `/api/resumes/:id/export?format=` | resume export |

Base URL: `runtimeConfig.public.apiBase` ← `NUXT_PUBLIC_API_BASE` (default `http://127.0.0.1:8000`).

## Scripts

```bash
pnpm dev          # http://localhost:3000
pnpm lint
pnpm typecheck
pnpm test
pnpm build
```

Run FastAPI separately on `:8000` with CORS allowing `http://localhost:3000`.
