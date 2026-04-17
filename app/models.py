import uuid
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from datetime import datetime
from .database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(String, default="QUEUED")
    priority = Column(Integer, default=1)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    cancel_requested = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)