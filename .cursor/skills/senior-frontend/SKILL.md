---
name: senior-frontend
description: Senior front-end engineering for this Nuxt 4 SPA — feature slices auth/resume/library, pages → features → shared, apiRequest HTTP, Pinia auth only, KK/RU/EN i18n. Use when building or reviewing frontend pages, components, composables, data fetching, state, routing, or accessibility.
---

# Senior Nuxt front-end (Resume AI)

SPA (`ssr: false`) in `frontend/`. OpenAPI lives on FastAPI `:8000`; Nuxt does not proxy it.

## Principles

- Vue 3 `<script setup lang="ts">`. Strict TypeScript. No `any`.
- `@nuxt/ui` (primary sky, dark slate). Do not mix in another CSS system.
- Follow existing feature files before inventing folders or stores.
- Access config only via `useRuntimeConfig()`. Never `process.env` in components. Do not read `.env`.

## Layout

```
frontend/app/
  pages/index.vue          # thin: sidebar + ResumeWizard
  features/auth/           # store, api, LoginModal, AuthBar
  features/resume/         # wizard, generate, export, preview
  features/library/        # saved list open/delete
  shared/api/http.ts       # apiRequest, apiBlob, Bearer
  shared/schemas/          # Zod; mirrors backend/schemas.py
```

**Dependency rule:** `pages → features → shared`. Features export only via `index.ts`. Shell widgets (`LangSwitch`, `WizardSteps`) stay in `app/components/`.

## HTTP and data

- HTTP only in `*.api.ts` + `shared/api/http.ts`. Never `$fetch` or raw `fetch` in Vue components.
- Parse responses with Zod schemas from `shared/schemas/`.
- Library: `useAsyncData('saved-resumes')` in `useResumeLibrary`. Keep that key.
- Generate and export are **user-triggered** `fetch` via `generateResume` / `exportResume`.
- Do **not** “fix” `ssr: false` by adding SSR or `useFetch` for the wizard.

## State

| Concern | Mechanism |
|---------|-----------|
| Auth + JWT (`resume_ai_token`) | Pinia `useAuthStore` only |
| Wizard step + form | `useState` in `useResumeWizard` |
| Preview result | `useState` in `useResumeResult` |

Home (`/`) stays public. Generate/export call `requireAuth()` and open `LoginModal` on 401. Middleware `auth.ts` is for future protected routes — do not put it on `/` unasked.

## i18n and a11y

- Locales `kk` / `ru` / `en`; default `kk`. Add the same key to all three JSON files.
- Semantic HTML, labels on inputs, keyboard access, visible focus. One `<h1>` on the wizard page.

## Workflow

1. Read the feature slice and `shared/` files you will touch.
2. Implement in the existing feature; export new public APIs from `index.ts`.
3. Run from `frontend/`: `pnpm lint`, `pnpm typecheck`, `pnpm test`.
4. Verify in the browser: loading, error, empty, and the happy path. See [checklist.md](checklist.md).

## Ask a human before

New dependencies, `nuxt.config.ts` modules, auth transport (cookies / HttpOnly / Nitro proxy), or anything needing secret values.
