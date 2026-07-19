<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, Float, DateTime
=======
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
>>>>>>> 9509c9af2835da46da2912733bb9952c531a46c6
from datetime import datetime

from database import Base


<<<<<<< HEAD
=======
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


>>>>>>> 9509c9af2835da46da2912733bb9952c531a46c6
class ScanHistory(Base):
    __tablename__ = "scan_history"

    id = Column(Integer, primary_key=True, index=True)
<<<<<<< HEAD
=======
    
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="scans")
>>>>>>> 9509c9af2835da46da2912733bb9952c531a46c6

    title = Column(String)
    company = Column(String)

    prediction = Column(String)
<<<<<<< HEAD

    probability = Column(Float)

    risk = Column(String)
=======
    probability = Column(Float)
    risk = Column(String)
    
    # New Advanced Tracking Fields
    confidence = Column(String, default="Low")
    warnings = Column(Text, default="[]")
    risk_breakdown = Column(Text, default="{}")
    recommended_action = Column(Text, default="")
    explanation = Column(Text, default="")
    
    source = Column(String, default="Scan")
>>>>>>> 9509c9af2835da46da2912733bb9952c531a46c6

    created_at = Column(DateTime, default=datetime.utcnow)