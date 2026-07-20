from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Preferences
    strict_mode = Column(Boolean, default=False)
    auto_delete = Column(Boolean, default=False)
    theme = Column(String, default="system")
    language = Column(String, default="en")
    email_alerts = Column(Boolean, default=True)
    fraud_alerts = Column(Boolean, default=True)
    weekly_reports = Column(Boolean, default=False)

    scans = relationship("ScanHistory", back_populates="owner")


class ScanHistory(Base):
    __tablename__ = "scan_history"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="scans")

    title = Column(String)
    company = Column(String)

    prediction = Column(String)


    probability = Column(Float)
    risk = Column(String)

    # Advanced Tracking Fields
    confidence = Column(String, default="Low")
    warnings = Column(Text, default="[]")
    risk_breakdown = Column(Text, default="{}")
    recommended_action = Column(Text, default="")
    explanation = Column(Text, default="")

    source = Column(String, default="Scan")

    created_at = Column(DateTime, default=datetime.utcnow)