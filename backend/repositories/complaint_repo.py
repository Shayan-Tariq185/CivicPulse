"""
SQLAlchemy database repository for complaints.

Phase 4: Uses PostgreSQL database to persist data.
"""
from __future__ import annotations

import uuid

from database import SessionLocal
from models.complaint import ComplaintModel
from schemas.complaint import ComplaintCreate, ComplaintStatus
from schemas.triage import TriageResult


def create(data: ComplaintCreate, triage_result: TriageResult, latency_ms: int) -> ComplaintModel:
    db = SessionLocal()
    try:
        complaint_id = f"CMP-{uuid.uuid4().hex[:8].upper()}"
        record = ComplaintModel(
            id=complaint_id,
            title=data.title,
            description=data.description,
            category=data.category.value,
            location=data.location,
            status=ComplaintStatus.open.value,
            upvotes=0,
            priority=triage_result.priority,
            ai_summary=triage_result.summary,
            triaged_by=triage_result.triaged_by,
            triage_latency_ms=latency_ms,
            triage_confidence=triage_result.confidence,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    finally:
        db.close()


def get_by_id(complaint_id: str) -> ComplaintModel | None:
    db = SessionLocal()
    try:
        return db.query(ComplaintModel).filter(ComplaintModel.id == complaint_id).first()
    finally:
        db.close()


def list_all() -> list[ComplaintModel]:
    db = SessionLocal()
    try:
        return db.query(ComplaintModel).order_by(ComplaintModel.submitted_at.desc()).all()
    finally:
        db.close()


def update_status(complaint_id: str, new_status: ComplaintStatus) -> ComplaintModel | None:
    db = SessionLocal()
    try:
        record = db.query(ComplaintModel).filter(ComplaintModel.id == complaint_id).first()
        if not record:
            return None
        record.status = new_status.value  # type: ignore[assignment]
        db.commit()
        db.refresh(record)
        return record
    finally:
        db.close()
