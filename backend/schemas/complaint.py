from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from schemas.enums import ComplaintCategory, ComplaintStatus, Priority

# ── Inbound ──────────────────────────────────────────────────────────────────

class ComplaintCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=120)
    description: str = Field(..., min_length=10)
    category: ComplaintCategory
    location: str = Field(..., min_length=2, max_length=200)


class StatusUpdate(BaseModel):
    status: ComplaintStatus


# ── Outbound ─────────────────────────────────────────────────────────────────

class ComplaintOut(BaseModel):
    id: str
    title: str
    description: str
    category: ComplaintCategory
    status: ComplaintStatus
    location: str
    upvotes: int
    submitted_at: datetime
    priority: Priority
    ai_summary: str
    triaged_by: str
    triage_latency_ms: int
    triage_confidence: float

    model_config = {"from_attributes": True}
