"""
In-memory complaint store.

Phase 2: plain dict — no DB, no persistence.
Phase 4 will replace this with SQLAlchemy + PostgreSQL.
No business logic lives here — only raw CRUD.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from schemas.complaint import ComplaintCategory, ComplaintCreate, ComplaintStatus


# Internal data model (not exposed outside this module)
class _ComplaintRecord:
    __slots__ = (
        "id", "title", "description", "category",
        "status", "location", "upvotes", "submitted_at",
    )

    def __init__(
        self,
        id: str,
        title: str,
        description: str,
        category: ComplaintCategory,
        location: str,
    ) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.status = ComplaintStatus.open
        self.location = location
        self.upvotes = 0
        self.submitted_at = datetime.now(timezone.utc)


# Single in-memory store — dict keyed by complaint id
_store: dict[str, _ComplaintRecord] = {}


def create(data: ComplaintCreate) -> _ComplaintRecord:
    complaint_id = f"CMP-{uuid.uuid4().hex[:8].upper()}"
    record = _ComplaintRecord(
        id=complaint_id,
        title=data.title,
        description=data.description,
        category=data.category,
        location=data.location,
    )
    _store[complaint_id] = record
    return record


def get_by_id(complaint_id: str) -> Optional[_ComplaintRecord]:
    return _store.get(complaint_id)


def list_all() -> list[_ComplaintRecord]:
    return list(_store.values())


def update_status(complaint_id: str, new_status: ComplaintStatus) -> Optional[_ComplaintRecord]:
    record = _store.get(complaint_id)
    if record is None:
        return None
    record.status = new_status
    return record
