"""
Complaint business logic.

All rules live here — not in routers, not in repositories.
Route handlers call service functions only.
"""
from __future__ import annotations

from fastapi import HTTPException, status

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
    )


def create_complaint(data: ComplaintCreate) -> ComplaintOut:
    record = complaint_repo.create(data)
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

    allowed = _ALLOWED_TRANSITIONS[record.status]
    if body.status not in allowed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Cannot transition from '{record.status}' to '{body.status}'. "
                f"Allowed transitions: {[s.value for s in allowed] or 'none (terminal state)'}."
            ),
        )

    updated = complaint_repo.update_status(complaint_id, body.status)
    return _to_out(updated)
