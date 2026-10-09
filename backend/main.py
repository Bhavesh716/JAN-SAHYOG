"""
Minimal FastAPI starting point for JAN SAHYOG.

This API currently exposes a health check and a safe placeholder assistance
endpoint. It does not yet call an LLM or retrieve government documents.
"""

from __future__ import annotations

import os
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

APP_NAME = os.getenv("APP_NAME", "JAN SAHYOG")
APP_ENV = os.getenv("APP_ENV", "development")

app = FastAPI(
    title=APP_NAME,
    description="Multilingual rural assistance platform — development starter API.",
    version="0.1.0",
)

origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS", "http://localhost:3000,http://localhost:5173"
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


class AssistanceRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    language: str = Field(default="en", min_length=2, max_length=12)
    channel: Literal["kiosk", "phone", "mobile", "web"] = "web"


class AssistanceResponse(BaseModel):
    status: str
    message: str
    answer: str
    sources: list[str] = []
    next_steps: list[str] = []


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": APP_NAME,
        "status": "running",
        "environment": APP_ENV,
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "jan-sahyog-api"}


@app.post("/api/v1/assistance", response_model=AssistanceResponse)
def request_assistance(payload: AssistanceRequest) -> AssistanceResponse:
    """
    Placeholder endpoint.

    Replace this response with the real pipeline:
    input normalization -> intent routing -> RAG retrieval -> LLM generation
    -> evidence/safety checks -> response.
    """
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    return AssistanceResponse(
        status="not_implemented",
        message=(
            "The assistance pipeline is not connected yet. No scheme or legal "
            "answer has been generated or verified."
        ),
        answer=(
            "JAN SAHYOG is still being configured. Please consult the relevant "
            "official government source for current eligibility, deadlines, "
            "and application requirements."
        ),
        sources=[],
        next_steps=[
            "Connect the document ingestion and retrieval pipeline.",
            "Configure a language model and response validation.",
            "Add verified official sources before answering scheme-specific questions.",
        ],
    )
