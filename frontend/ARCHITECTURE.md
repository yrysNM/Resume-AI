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
│   ├── layouts/default.vue     # role-aware nav
│   ├── middleware/             # auth.ts, hr.ts
│   ├── pages/
│   │   ├── index.vue           # wizard; logged-in HR → /hr
│   │   ├── jobs.vue
│   │   ├── dashboard.vue
│   │   └── hr/                 # companies, vacancies, ranking, hh.kz market-watch
│   ├── plugins/                # auth + locale bootstrap
│   ├── features/
│   │   ├── auth/               # store, api, LoginModal, AuthBar
│   │   ├── resume/             # wizard form/state, generate, export, preview
│   │   ├── library/            # saved list open/delete
│   │   ├── hr/                 # companies, vacancies, ranked applicants, hh.kz market-watch
│   │   ├── jobs/               # open vacancies + apply
│   │   ├── dashboard/          # role stats cards
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
| Auth user + JWT + role | Pinia `useAuthStore` (`resume_ai_token` in `localStorage`) |
| Wizard step + form | `useState` in `useResumeWizard` |
| Generate/preview result | `useState` in `useResumeResult` |
| Saved resumes | `useAsyncData('saved-resumes')` in `useResumeLibrary` |

Roles: `seeker` (default) or `hr`. `isHr` / `isSeeker` come from `user.role`. After register, HR goes to `/hr` and seekers to `/`.

## Data flow

1. User fills wizard (`useResumeWizard` form).
2. Generate calls `resume.api` → `shared/api/http` with Bearer token.
3. Result lands in `useResumeResult`; library list refreshes.
4. Open/delete saved resumes updates result + step via library composable.

Seekers apply from `/jobs` with a library resume. HR manages companies → vacancies → ranked applications.

## Auth

- Public home wizard; generate / export call `requireAuth()` and open `LoginModal` on 401.
- Logged-in HR on `/` is redirected to `/hr`. Generate and library stay available on the API for any authenticated user.
- Plugin `auth.client.ts` refreshes `/api/auth/me` on startup.
- Middleware `auth.ts` on `/jobs`, `/dashboard`, `/hr/**`. Middleware `hr.ts` keeps `/hr` HR-only.
- Nav: seeker Resume / Jobs / Dashboard; HR Companies / Dashboard.

## API surface (client)

| Method | Path | Feature |
|--------|------|---------|
| POST | `/api/auth/login`, `/api/auth/register` | auth (`role` on register) |
| GET | `/api/auth/me` | auth (`UserOut.role`) |
| POST | `/api/resume/generate`, `/api/resume/analyze` | resume |
| GET/DELETE | `/api/resumes`, `/api/resumes/:id` | library |
| GET | `/api/resumes/:id/export?format=` | resume export (`template=` optional) |
| CRUD | `/api/companies`, `/api/companies/:id/vacancies` | hr |
| GET/PUT/DELETE | `/api/companies/:id/vacancies/:vacancy_id` | hr nested vacancy |
| GET | `/api/vacancies/:id` | hr vacancy (ranking page) |
| GET | `/api/vacancies/:id/applications` | hr ranking |
| POST | `/api/vacancies/:id/rank` | hr re-rank |
| GET | `/api/hh/vacancies` | hh.kz search for any auth user (`?page=&text=&category=`; 503 if HH down) |
| GET | `/api/hh/categories` | category ids |
| GET | `/api/jobs` | jobs (seeker) |
| POST | `/api/jobs/:id/apply` | jobs (`{ resume_id }`; 409 closed/duplicate) |
| GET | `/api/applications` | seeker applications |
| GET | `/api/dashboard` | `HrDashboard` \| `SeekerDashboard` (`role`) |

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
