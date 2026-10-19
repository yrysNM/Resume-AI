"""Resume AI API — FastAPI backend with JWT auth, SQLite, Groq + BERT."""

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
    description="Түйіндеме құру және AI талдау микросервисі (JWT + SQLite + Groq/BERT)",
    version="1.2.0",
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
    from services import bert_analyze, groq_generate

    return {
        "status": "ok",
        "service": "resume-ai-backend",
        "groq_configured": groq_generate.groq_configured(),
        "groq_model": settings.groq_model,
        "bert_model": settings.bert_model_name,
        "ai_allow_fallback": settings.ai_allow_fallback,
    }


app.include_router(auth_router.router)
app.include_router(resumes.router)

# Static mount must be last so /api/* routes take precedence.
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
