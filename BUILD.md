# Build and run

Prerequisites: Python 3.12+ (local venv may be 3.14), Node.js, and **pnpm**. Two terminals. No Docker.

Copy [`.env.example`](.env.example) → `.env` and [`frontend/.env.example`](frontend/.env.example) → `frontend/.env` if needed. A human sets secret values. Never `cat` `.env`.

Env **names** only: `SECRET_KEY`, `DATABASE_URL`, `GROQ_API_KEY`, `GROQ_MODEL`, `BERT_MODEL_NAME`, `AI_ALLOW_FALLBACK`, `CORS_ORIGINS`, `NUXT_PUBLIC_API_BASE`. More names are listed in `.env.example`.

## Backend

Cwd **must** be `backend/` so SQLite `./resume_ai.db` lands there.

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

CPU-only Torch (see the comment in [`backend/requirements.txt`](backend/requirements.txt)):

```bash
pip install --index-url https://download.pytorch.org/whl/cpu torch
```

- API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- OpenAPI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- There is no backend test suite yet. Do not invent `pytest` / unittest files unless asked.

PDF export needs [`backend/assets/fonts/DejaVuSans.ttf`](backend/assets/fonts/DejaVuSans.ttf) and `DejaVuSans-Bold.ttf`. DOCX export does not.

## Frontend

```bash
cd frontend
pnpm install
pnpm dev          # http://localhost:3000
pnpm lint && pnpm typecheck && pnpm test
pnpm build
```

Quality scripts: `pnpm lint`, `pnpm typecheck`, `pnpm test` (Vitest). FastAPI must be running on `:8000` for generate / library / export in the browser.
