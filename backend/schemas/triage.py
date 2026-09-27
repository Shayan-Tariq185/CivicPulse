from __future__ import annotations

from pydantic import BaseModel, Field

from schemas.enums import ComplaintCategory, Priority


class TriageResult(BaseModel):
	"""Validated output shared by every triage provider."""

	category: ComplaintCategory
	priority: Priority
	summary: str = Field(min_length=1, max_length=140)
	confidence: float = Field(ge=0.0, le=1.0)
	triaged_by: str = "unknown"
