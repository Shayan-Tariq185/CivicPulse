"""
SQLAlchemy database repository for complaints.

Phase 4: Uses PostgreSQL database to persist data.
"""
from __future__ import annotations

import uuid
from typing import Optional

from schemas.complaint import ComplaintCreate, ComplaintStatus
from database import SessionLocal
from models.complaint import ComplaintModel


def create(data: ComplaintCreate) -> ComplaintModel:
    db = SessionLocal()
    try:
        complaint_id = f"CMP-{uuid.uuid4().hex[:8].upper()}"
        record = ComplaintModel(
            id=complaint_id,
            title=data.title,
            description=data.description,
            category=data.category,
            location=data.location,
            status=ComplaintStatus.open,
            upvotes=0
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    finally:
        db.close()


def get_by_id(complaint_id: str) -> Optional[ComplaintModel]:
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


def update_status(complaint_id: str, new_status: ComplaintStatus) -> Optional[ComplaintModel]:
    db = SessionLocal()
    try:
        record = db.query(ComplaintModel).filter(ComplaintModel.id == complaint_id).first()
        if not record:
            return None
        record.status = new_status
        db.commit()
        db.refresh(record)
        return record
    finally:
        db.close()
