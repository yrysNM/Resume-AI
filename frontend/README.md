# Resume AI — Nuxt frontend

See also: [root README](../README.md) · [BUILD](../BUILD.md).

SPA for the Resume AI wizard (auth, generate/analyze, saved library, PDF/DOCX export, KK/RU/EN).

## Setup

```bash
pnpm install
```

Copy `.env.example` to `.env` if you need a non-default API base:

```bash
NUXT_PUBLIC_API_BASE=http://127.0.0.1:8000
```

## Develop

Terminal 1 — FastAPI backend on `:8000`.

Terminal 2:

```bash
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000).

## Quality

```bash
pnpm typecheck
pnpm lint
pnpm test
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for feature layout and data flow.
