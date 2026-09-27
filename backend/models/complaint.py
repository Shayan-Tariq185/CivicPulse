from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, Float
from database import Base

class ComplaintModel(Base):
    __tablename__ = "complaints"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    status = Column(String, nullable=False, default="open")
    location = Column(String, nullable=False)
    upvotes = Column(Integer, default=0)
    submitted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    priority = Column(String(10), nullable=False, default="normal")
    ai_summary = Column(String(140), nullable=False, default="")
    triaged_by = Column(String(50), nullable=False, default="rules")
    triage_latency_ms = Column(Integer, nullable=False, default=0)
    triage_confidence = Column(Float, nullable=False, default=0.0)
