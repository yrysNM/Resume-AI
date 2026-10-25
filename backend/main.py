"""Resume AI API — FastAPI backend with JWT auth, SQLite, Ollama + BERT."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import init_db
from routers import auth_router, resumes


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    description="Түйіндеме құру және AI талдау микросервисі (JWT + SQLite + Ollama/BERT)",
    version="1.3.0",
    lifespan=lifespan,
)

# Explicit origins for Nuxt (:3000). Auth uses Bearer JWT in Authorization —
# allow_credentials is not required.
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    from services import ollama_generate

    return {
        "status": "ok",
        "service": "resume-ai-backend",
        "ollama_configured": ollama_generate.ollama_configured(),
        "ollama_model": settings.ollama_model,
        "ollama_base_url": settings.ollama_base_url,
        "bert_model": settings.bert_model_name,
        "ai_allow_fallback": settings.ai_allow_fallback,
    }


app.include_router(auth_router.router)
app.include_router(resumes.router)
