from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime
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
