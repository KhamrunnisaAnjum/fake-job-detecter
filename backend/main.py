from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import sys
import os
import json
from sqlalchemy import func

from database import Base, engine, SessionLocal
from models import ScanHistory
from rule_engine import analyze_job_text

# create database
Base.metadata.create_all(bind=engine)

# allow importing preprocess.py
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from preprocess import clean_text

app = FastAPI(title="JobX API")

# Allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML Model
classifier = joblib.load("../model/classifier.pkl")
vectorizer = joblib.load("../model/vectorizer.pkl")


class JobRequest(BaseModel):
    title: str
    company: str
    description: str
    requirements: str
    salary: str

class MessageRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {
        "message": "JobX Backend Running"
    }

@app.post("/predict")
def predict(data: JobRequest):

    text = " ".join([
        data.title,
        data.company,
        data.description,
        data.requirements,
        data.salary
    ])

    # Get ML Prediction
    cleaned = clean_text(text)
    vector = vectorizer.transform([cleaned])
    prediction = classifier.predict(vector)[0]
    probability = classifier.predict_proba(vector)[0][1]
    probability = round(probability * 100, 2)

    # Get Rule Engine Warnings
    warnings = analyze_job_text(text, title=data.title, company=data.company, is_message=False)

    # Add artificial weight to risk based on rules if ML is uncertain
    if len(warnings) > 2 and probability < 50:
        probability = min(probability + 20, 99.0) # Boost probability if many rules triggered

    if probability >= 60:
        risk = "High Risk"
    elif probability >= 30:
        risk = "Medium Risk"
    else:
        risk = "Low Risk"

    db = SessionLocal()

    scan = ScanHistory(
        title=data.title,
        company=data.company,
        prediction="Fake Job" if prediction == 1 else "Real Job",
        probability=probability,
        risk=risk,
        warnings=json.dumps(warnings),
        source="Scan"
    )

    db.add(scan)
    db.commit()
    db.close()

    return {
        "prediction": "Fake Job" if prediction == 1 else "Real Job",
        "probability": probability,
        "risk": risk,
        "warnings": warnings
    }

@app.post("/analyze-message")
def analyze_message(data: MessageRequest):
    # Rule engine only for messages
    warnings = analyze_job_text(data.message, is_message=True)
    
    # We can also run the ML model on the message
    cleaned = clean_text(data.message)
    vector = vectorizer.transform([cleaned])
    prediction = classifier.predict(vector)[0]
    probability = classifier.predict_proba(vector)[0][1]
    probability = round(probability * 100, 2)
    
    if len(warnings) >= 3:
        probability = min(probability + 30, 99.0)
    elif len(warnings) >= 1:
        probability = min(probability + 15, 99.0)
        
    if probability >= 60:
        risk = "High Risk"
    elif probability >= 30:
        risk = "Medium Risk"
    else:
        risk = "Low Risk"
        
    db = SessionLocal()
    scan = ScanHistory(
        title="WhatsApp/Telegram Message",
        company="N/A",
        prediction="Fake Message" if prediction == 1 else "Real Message",
        probability=probability,
        risk=risk,
        warnings=json.dumps(warnings),
        source="Message"
    )
    db.add(scan)
    db.commit()
    db.close()

    return {
        "prediction": "Fake Message" if prediction == 1 else "Real Message",
        "probability": probability,
        "risk": risk,
        "warnings": warnings
    }

@app.get("/history")
def get_history(limit: int = 50, offset: int = 0):
    db = SessionLocal()
    try:
        scans = db.query(ScanHistory).order_by(ScanHistory.created_at.desc()).offset(offset).limit(limit).all()
        return [
            {
                "id": scan.id,
                "title": scan.title,
                "company": scan.company,
                "prediction": scan.prediction,
                "probability": scan.probability,
                "risk": scan.risk,
                "warnings": json.loads(scan.warnings) if scan.warnings else [],
                "source": scan.source,
                "created_at": scan.created_at.isoformat()
            } for scan in scans
        ]
    finally:
        db.close()

@app.delete("/history/{scan_id}")
def delete_history(scan_id: int):
    db = SessionLocal()
    try:
        scan = db.query(ScanHistory).filter(ScanHistory.id == scan_id).first()
        if not scan:
            raise HTTPException(status_code=404, detail="Scan not found")
        db.delete(scan)
        db.commit()
        return {"message": "Deleted successfully"}
    finally:
        db.close()

@app.get("/stats")
def get_stats():
    db = SessionLocal()
    try:
        total = db.query(func.count(ScanHistory.id)).scalar()
        high = db.query(func.count(ScanHistory.id)).filter(ScanHistory.risk == "High Risk").scalar()
        medium = db.query(func.count(ScanHistory.id)).filter(ScanHistory.risk == "Medium Risk").scalar()
        low = db.query(func.count(ScanHistory.id)).filter(ScanHistory.risk == "Low Risk").scalar()
        
        recent_threats = db.query(ScanHistory).order_by(ScanHistory.created_at.desc()).limit(10).all()
        threats_list = [{"title": t.title, "company": t.company, "probability": t.probability, "risk": t.risk, "created_at": t.created_at.isoformat()} for t in recent_threats]

        return {
            "total_scans": total,
            "high_risk": high,
            "medium_risk": medium,
            "low_risk": low,
            "latest_threats": threats_list
        }
    finally:
        db.close()

@app.get("/reports")
def get_reports():
    db = SessionLocal()
    try:
        # Distribution
        high = db.query(func.count(ScanHistory.id)).filter(ScanHistory.risk == "High Risk").scalar()
        medium = db.query(func.count(ScanHistory.id)).filter(ScanHistory.risk == "Medium Risk").scalar()
        low = db.query(func.count(ScanHistory.id)).filter(ScanHistory.risk == "Low Risk").scalar()

        # Scans over time (group by day) - SQLite func.date equivalent
        # For simplicity, we fetch all and aggregate in python if DB date func is complex in sqlite,
        # but func.date(ScanHistory.created_at) works in SQLite.
        daily_scans = db.query(func.date(ScanHistory.created_at), func.count(ScanHistory.id))\
            .group_by(func.date(ScanHistory.created_at))\
            .order_by(func.date(ScanHistory.created_at).desc())\
            .limit(14).all()
            
        time_series = [{"date": ds[0], "count": ds[1]} for ds in reversed(daily_scans)]
        
        # High Risk Trend over time
        high_risk_daily = db.query(func.date(ScanHistory.created_at), func.count(ScanHistory.id))\
            .filter(ScanHistory.risk == "High Risk")\
            .group_by(func.date(ScanHistory.created_at))\
            .order_by(func.date(ScanHistory.created_at).desc())\
            .limit(14).all()
            
        high_risk_series = [{"date": h[0], "high_risk_count": h[1]} for h in reversed(high_risk_daily)]

        return {
            "distribution": [
                {"name": "High Risk", "value": high},
                {"name": "Medium Risk", "value": medium},
                {"name": "Low Risk", "value": low}
            ],
            "scans_over_time": time_series,
            "high_risk_trend": high_risk_series
        }
    finally:
        db.close()