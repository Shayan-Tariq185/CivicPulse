"""
Complaint business logic.

All rules live here — not in routers, not in repositories.
Route handlers call service functions only.
"""
from __future__ import annotations

import time

from fastapi import HTTPException, status

from metrics import record_triage
from providers.factory import get_triage_provider
from providers.history import record_outcome
from providers.rules import RuleBasedTriage
from redis_client import redis_db
from repositories import complaint_repo
from schemas.complaint import (
    ComplaintCreate,
    ComplaintOut,
    ComplaintStatus,
    StatusUpdate,
)

# Valid status transitions: current → set of allowed next statuses
_ALLOWED_TRANSITIONS: dict[ComplaintStatus, set[ComplaintStatus]] = {
    ComplaintStatus.open:        {ComplaintStatus.in_progress, ComplaintStatus.rejected},
    ComplaintStatus.in_progress: {ComplaintStatus.resolved,    ComplaintStatus.rejected},
    ComplaintStatus.resolved:    set(),   # terminal
    ComplaintStatus.rejected:    set(),   # terminal
}


def _to_out(record) -> ComplaintOut:
    return ComplaintOut(
        id=record.id,
        title=record.title,
        description=record.description,
        category=record.category,
        status=record.status,
        location=record.location,
        upvotes=record.upvotes,
        submitted_at=record.submitted_at,
        priority=record.priority,
        ai_summary=record.ai_summary,
        triaged_by=record.triaged_by,
        triage_latency_ms=record.triage_latency_ms,
        triage_confidence=record.triage_confidence,
    )


async def create_complaint(data: ComplaintCreate) -> ComplaintOut:
    started_at = time.perf_counter()
    try:
        triage_provider = get_triage_provider()
        triage_result = await triage_provider.triage(data.description, data.location)
    except Exception:  # noqa: BLE001
        triage_result = await RuleBasedTriage().triage(data.description, data.location)
        triage_result = triage_result.model_copy(update={"triaged_by": "rules:fallback"})

    latency_ms = round((time.perf_counter() - started_at) * 1000)
    record_outcome(
        provider=triage_result.triaged_by,
        latency_ms=latency_ms,
        fallback=triage_result.triaged_by == "rules:fallback",
    )
    record_triage(
        latency_ms=latency_ms,
        fallback=triage_result.triaged_by == "rules:fallback",
    )
    triaged_data = data.model_copy(update={"category": triage_result.category})
    record = complaint_repo.create(triaged_data, triage_result, latency_ms)
    redis_db.delete("civicpulse:stats")
    return _to_out(record)


def get_complaint(complaint_id: str) -> ComplaintOut:
    record = complaint_repo.get_by_id(complaint_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Complaint '{complaint_id}' not found.",
        )
    return _to_out(record)


def list_complaints() -> list[ComplaintOut]:
    return [_to_out(r) for r in complaint_repo.list_all()]


def update_status(complaint_id: str, body: StatusUpdate) -> ComplaintOut:
    record = complaint_repo.get_by_id(complaint_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Complaint '{complaint_id}' not found.",
        )

    allowed = _ALLOWED_TRANSITIONS[ComplaintStatus(record.status)]
    if body.status not in allowed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Cannot transition from '{record.status}' to '{body.status}'. "
                f"Allowed transitions: {[s.value for s in allowed] or 'none (terminal state)'}."
            ),
        )

    updated = complaint_repo.update_status(complaint_id, body.status)
    redis_db.delete("civicpulse:stats")
    return _to_out(updated)
