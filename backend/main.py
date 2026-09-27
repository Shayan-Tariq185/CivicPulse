"""
CivicPulse — FastAPI application entry point.

Responsibilities:
- Create the FastAPI app instance
- Mount routers
- Configure CORS (permissive in dev; tightened in Phase 8)
- No business logic here
"""
from __future__ import annotations

import json
import logging
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from metrics import record_request
from redis_client import redis_db
from routers import complaints, meta, operations, stats


logger = logging.getLogger("civicpulse.request")


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        })


if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    redis_db.close()
    engine.dispose()

app = FastAPI(
    title="CivicPulse API",
    description="Complaint management API for CivicPulse — CS4032 Assignment 01",
    version="0.2.0",  # Phase 2: in-memory store
    lifespan=lifespan,
)

# ── Rate Limiting ────────────────────────────────────────────────────────────
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "127.0.0.1"
    current_minute = int(time.time() // 60)
    key = f"civicpulse:ratelimit:{client_ip}:{current_minute}"
    
    current_count = redis_db.incr(key)
    if current_count == 1:
        redis_db.expire(key, 60)
        
    if current_count > 100:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too Many Requests"},
            headers={"Retry-After": "60"},
        )

    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    started_at = time.perf_counter()
    response = await call_next(request)
    latency_ms = (time.perf_counter() - started_at) * 1000
    response.headers["X-Request-ID"] = request_id
    record_request(request.method, request.url.path, response.status_code, latency_ms)
    logger.info(json.dumps({
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "latency_ms": round(latency_ms, 2),
    }))
    return response

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
app.include_router(operations.router)


# ── Root ──────────────────────────────────────────────────────────────────────
@app.get("/", tags=["meta"], summary="API root / health ping")
def root():
    return {"service": "civicpulse-api", "version": "0.2.0", "status": "ok"}
