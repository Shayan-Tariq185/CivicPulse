from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ComplaintCategory(str, Enum):
    roads = "Roads & Infrastructure"
    water = "Water & Sanitation"
    electricity = "Electricity"
    waste = "Waste Management"
    safety = "Public Safety"
    parks = "Parks & Recreation"
    noise = "Noise Pollution"
    other = "Other"


class ComplaintStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    rejected = "rejected"


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

    model_config = {"from_attributes": True}
