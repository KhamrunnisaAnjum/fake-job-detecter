from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from database import Base


class ScanHistory(Base):
    __tablename__ = "scan_history"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    company = Column(String)

    prediction = Column(String)

    probability = Column(Float)

    risk = Column(String)
    
    warnings = Column(String, default="[]")
    source = Column(String, default="Scan")

    created_at = Column(DateTime, default=datetime.utcnow)