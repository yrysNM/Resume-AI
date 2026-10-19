"""Resume AI API — FastAPI backend with JWT auth and SQLite persistence.

AI generate/analyze endpoints remain rule-based (template + keyword heuristics).
The response field `generated_by` is a demo label only — not a live GPT/BERT call.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import settings
from database import init_db
from routers import auth_router, resumes


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    description="Түйіндеме құру және AI талдау микросервисі (JWT + SQLite)",
    version="1.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "resume-ai-backend"}


app.include_router(auth_router.router)
app.include_router(resumes.router)

# Static mount must be last so /api/* routes take precedence.
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
