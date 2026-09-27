"""
CivicPulse — FastAPI application entry point.

Responsibilities:
- Create the FastAPI app instance
- Mount routers
- Configure CORS (permissive in dev; tightened in Phase 8)
- No business logic here
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import complaints, meta, stats

app = FastAPI(
    title="CivicPulse API",
    description="Complaint management API for CivicPulse — CS4032 Assignment 01",
    version="0.2.0",  # Phase 2: in-memory store
)

# ── CORS ─────────────────────────────────────────────────────────────────────
# Allow the Vite dev server (port 5173) in development.
# Tightened to specific origins in Phase 8 (Docker Compose).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(complaints.router, prefix="/api/v1")
app.include_router(stats.router, prefix="/api/v1")
app.include_router(meta.router, prefix="/api/v1")


# ── Root ──────────────────────────────────────────────────────────────────────
@app.get("/", tags=["meta"], summary="API root / health ping")
def root():
    return {"service": "civicpulse-api", "version": "0.2.0", "status": "ok"}
