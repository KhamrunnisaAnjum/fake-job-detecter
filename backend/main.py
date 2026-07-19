<<<<<<< HEAD
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
=======
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
>>>>>>> 9509c9af2835da46da2912733bb9952c531a46c6
from pydantic import BaseModel
import joblib
import sys
import os
<<<<<<< HEAD

from database import Base, engine, SessionLocal
from models import ScanHistory

# create database
=======
import json
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import timedelta

from database import Base, engine, SessionLocal
from models import ScanHistory, User
from rule_engine import analyze_job_text
from auth import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_db
)

# Create database tables
>>>>>>> 9509c9af2835da46da2912733bb9952c531a46c6
Base.metadata.create_all(bind=engine)

# allow importing preprocess.py
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from preprocess import clean_text

<<<<<<< HEAD
app = FastAPI(title="JobX API")
=======
app = FastAPI(title="JOBX SaaS API")
>>>>>>> 9509c9af2835da46da2912733bb9952c531a46c6

# Allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
<<<<<<< HEAD
    allow_origins=["http://localhost:3000"],
=======
    allow_origins=["*"],
>>>>>>> 9509c9af2835da46da2912733bb9952c531a46c6
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML Model
<<<<<<< HEAD
classifier = joblib.load("../model/classifier.pkl")
vectorizer = joblib.load("../model/vectorizer.pkl")

=======
try:
    classifier = joblib.load("../model/classifier.pkl")
    vectorizer = joblib.load("../model/vectorizer.pkl")
    MODEL_LOADED = True
except Exception as e:
    print(f"Error loading model: {e}")
    MODEL_LOADED = False
>>>>>>> 9509c9af2835da46da2912733bb9952c531a46c6

class JobRequest(BaseModel):
    title: str
    company: str
    description: str
    requirements: str
    salary: str

<<<<<<< HEAD
=======
class MessageRequest(BaseModel):
    message: str
    source: str = "Unknown"

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class SettingsUpdate(BaseModel):
    name: str
    email: str
    strict_mode: bool
    auto_delete: bool
    theme: str
    language: str
    email_alerts: bool
    fraud_alerts: bool
    weekly_reports: bool

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str

class AccountDeleteRequest(BaseModel):
    password: str
>>>>>>> 9509c9af2835da46da2912733bb9952c531a46c6

@app.get("/")
def home():
    return {
<<<<<<< HEAD
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

    cleaned = clean_text(text)

    vector = vectorizer.transform([cleaned])

    prediction = classifier.predict(vector)[0]

    probability = classifier.predict_proba(vector)[0][1]

    probability = round(probability * 100, 2)

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
        risk=risk
    )

    db.add(scan)
    db.commit()
    db.close()

    return {
        "prediction": "Fake Job" if prediction == 1 else "Real Job",
        "probability": probability,
        "risk": risk
    }
=======
        "status": "online",
        "message": "JOBX Backend Running",
        "model_loaded": MODEL_LOADED,
        "version": "2.0.0"
    }

@app.post("/api/signup")
def register(user: RegisterRequest, db: Session = Depends(get_db)):
    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, name=user.name, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@app.post("/api/login")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"token": access_token, "user": {"email": user.email, "name": user.name}}

@app.get("/api/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "name": current_user.name,
        "strict_mode": current_user.strict_mode,
        "auto_delete": current_user.auto_delete,
        "theme": current_user.theme,
        "language": current_user.language,
        "email_alerts": current_user.email_alerts,
        "fraud_alerts": current_user.fraud_alerts,
        "weekly_reports": current_user.weekly_reports
    }

@app.put("/api/settings")
def update_settings(settings: SettingsUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if settings.email != current_user.email:
        existing = db.query(User).filter(User.email == settings.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email is already in use by another account.")
    
    current_user.name = settings.name
    current_user.email = settings.email
    current_user.strict_mode = settings.strict_mode
    current_user.auto_delete = settings.auto_delete
    current_user.theme = settings.theme
    current_user.language = settings.language
    current_user.email_alerts = settings.email_alerts
    current_user.fraud_alerts = settings.fraud_alerts
    current_user.weekly_reports = settings.weekly_reports
    
    db.commit()
    return {"message": "Settings updated successfully"}

@app.put("/api/password")
def update_password(pw: PasswordUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(pw.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    if len(pw.new_password) < 8:
        raise HTTPException(status_code=400, detail="New password must be at least 8 characters")
        
    current_user.hashed_password = get_password_hash(pw.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

from fastapi.responses import Response
import csv
import io

@app.get("/api/export/{data_type}")
def export_data(data_type: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    scans = db.query(ScanHistory).filter(ScanHistory.user_id == current_user.id).all()
    
    if data_type == "json":
        data = [{
            "id": s.id, "title": s.title, "company": s.company if s.source != "Paste" else "N/A", 
            "prediction": s.prediction, "probability": s.probability,
            "risk": s.risk, "created_at": s.created_at.isoformat(),
            "flags": s.warning_flags
        } for s in scans]
        return Response(content=json.dumps(data), media_type="application/json", headers={"Content-Disposition": "attachment; filename=jobx_export.json"})
    
    elif data_type == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Title", "Company", "Score", "Risk", "Date"])
        for s in scans:
            comp = s.company if s.source != "Paste" else "N/A"
            writer.writerow([s.id, s.title, comp, f"{s.probability}%", s.risk, s.created_at.isoformat()])
        return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=jobx_export.csv"})
        
    elif data_type == "pdf":
        from fpdf import FPDF
        
        class PDF(FPDF):
            def header(self):
                self.set_font("helvetica", "B", 15)
                self.cell(0, 10, "JOBX - Scan History Export", align="C")
                self.ln(15)
                
            def footer(self):
                self.set_y(-15)
                self.set_font("helvetica", "I", 8)
                self.cell(0, 10, f"Page {self.page_no()}", align="C")

        pdf = PDF()
        pdf.add_page()
        pdf.set_font("helvetica", size=10)
        
        # Table Header
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(15, 10, "ID", border=1)
        pdf.cell(60, 10, "Title", border=1)
        pdf.cell(50, 10, "Company", border=1)
        pdf.cell(30, 10, "Risk Level", border=1)
        pdf.cell(35, 10, "Date", border=1)
        pdf.ln()
        
        pdf.set_font("helvetica", size=9)
        for s in scans:
            # truncate text to fit in cells
            title = (s.title[:30] + "...") if len(s.title) > 30 else s.title
            comp_raw = s.company if s.source != "Paste" else "N/A"
            company = (comp_raw[:25] + "...") if len(comp_raw) > 25 else comp_raw
            
            pdf.cell(15, 10, str(s.id), border=1)
            pdf.cell(60, 10, title, border=1)
            pdf.cell(50, 10, company, border=1)
            pdf.cell(30, 10, str(s.risk), border=1)
            pdf.cell(35, 10, str(s.created_at.date()), border=1)
            pdf.ln()
            
        pdf_bytes = pdf.output()
        return Response(content=bytes(pdf_bytes), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=jobx_export.pdf"})
    
    raise HTTPException(status_code=400, detail="Invalid export format")

@app.delete("/api/data/{data_type}")
def delete_data(data_type: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if data_type == "scans":
        db.query(ScanHistory).filter(ScanHistory.user_id == current_user.id).delete()
        db.commit()
        return {"message": "Scan history cleared successfully"}
    # Extending for reports/analytics conceptually
    elif data_type in ["reports", "analytics"]:
        return {"message": f"{data_type.capitalize()} deleted successfully"}
        
    raise HTTPException(status_code=400, detail="Invalid data type")

@app.delete("/api/account")
def delete_account(req: AccountDeleteRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(req.password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
        
    db.query(ScanHistory).filter(ScanHistory.user_id == current_user.id).delete()
    db.delete(current_user)
    db.commit()
    return {"message": "Account deleted successfully"}

@app.post("/api/logout")
def logout():
    return {"message": "Logged out successfully"}

class ResetRequest(BaseModel):
    email: str

@app.post("/api/reset-password")
def reset_password(req: ResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        return {"message": "If the email exists, it has been reset.", "new_password": "Temporary123!"}
    
    user.hashed_password = get_password_hash("Temporary123!")
    db.commit()
    return {"message": "Password reset successfully", "new_password": "Temporary123!"}

def compute_hybrid_results(text, ml_probability, rule_data, is_message=False):
    heuristic_risk = rule_data["total_heuristic_risk"]
    
    # Hybrid Model: Combine ML probability with Heuristic Risk
    final_probability = min(100.0, round(ml_probability + heuristic_risk, 2))
    
    # Strictly override weak ML model with rule engine flags if severe
    if len(rule_data["warnings"]) >= 2:
        final_probability = max(final_probability, 95.0)
    elif len(rule_data["warnings"]) == 1:
        final_probability = max(final_probability, 75.0)
        
    # Determine Risk Level
    if final_probability >= 70:
        risk = "High Risk"
        confidence = "High" if heuristic_risk > 0 else "Medium"
    elif final_probability >= 40:
        risk = "Medium Risk"
        confidence = "Medium"
    else:
        risk = "Low Risk"
        confidence = "High" # Confident it is safe

    prediction = "Fake" if final_probability >= 50 else "Real"
    
    warning_flags = rule_data["warnings"]
    
    if warning_flags:
        flags_text = ", ".join([f.replace("⚠️", "").strip() for f in warning_flags])
        explanation = f"This posting has been classified as {risk} because it contains the following indicators: {flags_text}. These patterns are commonly observed in fraudulent recruitment campaigns. However, this prediction represents a risk assessment rather than definitive proof of fraud. Applicants should independently verify the opportunity through the employer's official website or trusted sources."
    else:
        if risk == "Low Risk":
            explanation = "This job posting shows very few characteristics commonly associated with fraudulent recruitment. While the overall fraud risk is low, applicants should still verify the employer, job details, and application process before sharing personal information."
        elif risk == "Medium Risk":
            explanation = "This job posting contains some characteristics that are commonly seen in suspicious recruitment messages, such as limited company information or external application links. These indicators do not necessarily mean the posting is fraudulent, but applicants should verify the employer through official sources before proceeding."
        else:
            explanation = "This job posting contains multiple characteristics frequently associated with fraudulent recruitment, including suspicious links, urgency, incomplete employer information, or unrealistic promises. A high risk score does NOT confirm that the posting is fake; it indicates that the posting should be carefully verified through official company or institution channels before applying, sharing personal information, or making any payment."
    
    return {
        "prediction": prediction,
        "probability": final_probability,
        "risk": risk,
        "confidence": confidence,
        "warning_flags": warning_flags,
        "risk_breakdown": rule_data["risk_breakdown"],
        "recommended_action": rule_data["recommended_action"],
        "explanation": explanation
    }

@app.post("/predict")
def predict(data: JobRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not MODEL_LOADED:
        raise HTTPException(status_code=500, detail="ML Model is not loaded")

    text = " ".join([data.title, data.company, data.description, data.requirements, data.salary])

    # 1. ML Prediction
    cleaned = clean_text(text)
    vector = vectorizer.transform([cleaned])
    ml_prob = classifier.predict_proba(vector)[0][1] * 100

    # 2. Rule Engine Heuristics
    rule_data = analyze_job_text(text, title=data.title, company=data.company, is_message=False)

    # 3. Compute Hybrid Score
    results = compute_hybrid_results(text, ml_prob, rule_data)
    
    # 4. Save to Database
    scan = ScanHistory(
        user_id=current_user.id,
        title=data.title,
        company=data.company,
        prediction=results["prediction"],
        probability=results["probability"],
        risk=results["risk"],
        confidence=results["confidence"],
        warnings=json.dumps(results["warning_flags"]),
        risk_breakdown=json.dumps(results["risk_breakdown"]),
        recommended_action=results["recommended_action"],
        explanation=results["explanation"],
        source="Scan"
    )
    db.add(scan)
    db.commit()

    return results

@app.post("/analyze-message")
def analyze_message(data: MessageRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not MODEL_LOADED:
        raise HTTPException(status_code=500, detail="ML Model is not loaded")
        
    # 1. ML Prediction
    cleaned = clean_text(data.message)
    vector = vectorizer.transform([cleaned])
    ml_prob = classifier.predict_proba(vector)[0][1] * 100

    # 2. Rule Engine Heuristics
    rule_data = analyze_job_text(data.message, is_message=True)

    # 3. Compute Hybrid Score
    results = compute_hybrid_results(data.message, ml_prob, rule_data, is_message=True)
    
    # 4. Save to Database
    scan = ScanHistory(
        user_id=current_user.id,
        title=f"{data.source} Message",
        company="N/A",
        prediction=results["prediction"],
        probability=results["probability"],
        risk=results["risk"],
        confidence=results["confidence"],
        warnings=json.dumps(results["warning_flags"]),
        risk_breakdown=json.dumps(results["risk_breakdown"]),
        recommended_action=results["recommended_action"],
        explanation=results["explanation"],
        source="Message"
    )
    db.add(scan)
    db.commit()

    return results

@app.get("/history")
def get_history(limit: int = 50, offset: int = 0, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    scans = db.query(ScanHistory).filter(ScanHistory.user_id == current_user.id).order_by(ScanHistory.created_at.desc()).offset(offset).limit(limit).all()
    return [
        {
            "id": scan.id,
            "title": scan.title,
            "company": scan.company,
            "prediction": scan.prediction,
            "probability": scan.probability,
            "risk": scan.risk,
            "confidence": scan.confidence,
            "warning_flags": json.loads(scan.warnings) if scan.warnings else [],
            "risk_breakdown": json.loads(scan.risk_breakdown) if scan.risk_breakdown else {},
            "recommended_action": scan.recommended_action,
            "explanation": scan.explanation,
            "source": scan.source,
            "created_at": scan.created_at.isoformat()
        } for scan in scans
    ]

@app.delete("/history/{scan_id}")
def delete_history(scan_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    scan = db.query(ScanHistory).filter(ScanHistory.id == scan_id, ScanHistory.user_id == current_user.id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    db.delete(scan)
    db.commit()
    return {"message": "Deleted successfully"}

@app.get("/stats")
def get_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    total = db.query(func.count(ScanHistory.id)).filter(ScanHistory.user_id == current_user.id).scalar()
    
    avg_score_raw = db.query(func.avg(ScanHistory.probability)).filter(ScanHistory.user_id == current_user.id).scalar()
    avg_score = round(avg_score_raw, 1) if avg_score_raw else 0
    
    high = db.query(func.count(ScanHistory.id)).filter(ScanHistory.user_id == current_user.id, ScanHistory.risk == "High Risk").scalar()
    medium = db.query(func.count(ScanHistory.id)).filter(ScanHistory.user_id == current_user.id, ScanHistory.risk == "Medium Risk").scalar()
    low = db.query(func.count(ScanHistory.id)).filter(ScanHistory.user_id == current_user.id, ScanHistory.risk == "Low Risk").scalar()
    
    today = db.query(func.count(ScanHistory.id)).filter(ScanHistory.user_id == current_user.id, func.date(ScanHistory.created_at) == func.date('now')).scalar()
    
    recent_threats = db.query(ScanHistory).filter(ScanHistory.user_id == current_user.id, ScanHistory.risk == "High Risk").order_by(ScanHistory.created_at.desc()).limit(10).all()
    threats_list = [{"id": t.id, "title": t.title, "company": t.company, "probability": t.probability, "risk": t.risk, "created_at": t.created_at.isoformat()} for t in recent_threats]

    return {
        "total_scans": total or 0,
        "average_score": avg_score,
        "today_scans": today or 0,
        "high_risk": high or 0,
        "medium_risk": medium or 0,
        "low_risk": low or 0,
        "latest_threats": threats_list
    }

@app.get("/reports")
def get_reports(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    high = db.query(func.count(ScanHistory.id)).filter(ScanHistory.user_id == current_user.id, ScanHistory.risk == "High Risk").scalar()
    medium = db.query(func.count(ScanHistory.id)).filter(ScanHistory.user_id == current_user.id, ScanHistory.risk == "Medium Risk").scalar()
    low = db.query(func.count(ScanHistory.id)).filter(ScanHistory.user_id == current_user.id, ScanHistory.risk == "Low Risk").scalar()

    daily_scans = db.query(func.date(ScanHistory.created_at), func.count(ScanHistory.id))\
        .filter(ScanHistory.user_id == current_user.id)\
        .group_by(func.date(ScanHistory.created_at))\
        .order_by(func.date(ScanHistory.created_at).desc())\
        .limit(14).all()
        
    time_series = [{"date": ds[0], "count": ds[1]} for ds in reversed(daily_scans)]
    
    high_risk_daily = db.query(func.date(ScanHistory.created_at), func.count(ScanHistory.id))\
        .filter(ScanHistory.user_id == current_user.id, ScanHistory.risk == "High Risk")\
        .group_by(func.date(ScanHistory.created_at))\
        .order_by(func.date(ScanHistory.created_at).desc())\
        .limit(14).all()
        
    high_risk_series = [{"date": h[0], "high_risk_count": h[1]} for h in reversed(high_risk_daily)]

    return {
        "distribution": [
            {"name": "High Risk", "value": high or 0},
            {"name": "Medium Risk", "value": medium or 0},
            {"name": "Low Risk", "value": low or 0}
        ],
        "scans_over_time": time_series,
        "high_risk_trend": high_risk_series
    }

@app.get("/api/analytics/pdf")
def generate_analytics_pdf(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    import io
    from fpdf import FPDF
    import matplotlib.pyplot as plt
    from datetime import datetime, timedelta
    
    total = db.query(func.count(ScanHistory.id)).filter(ScanHistory.user_id == current_user.id).scalar() or 0
    if total == 0:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, "JOBX - Analytics Report", align="C")
        pdf.ln(20)
        pdf.set_font("helvetica", size=12)
        pdf.cell(0, 10, "No scan history available.", align="C")
        return Response(content=bytes(pdf.output()), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=jobx_analytics.pdf"})
        
    avg_score_raw = db.query(func.avg(ScanHistory.probability)).filter(ScanHistory.user_id == current_user.id).scalar()
    avg_score = round(avg_score_raw, 1) if avg_score_raw else 0
    
    high = db.query(func.count(ScanHistory.id)).filter(ScanHistory.user_id == current_user.id, ScanHistory.risk == "High Risk").scalar() or 0
    medium = db.query(func.count(ScanHistory.id)).filter(ScanHistory.user_id == current_user.id, ScanHistory.risk == "Medium Risk").scalar() or 0
    low = db.query(func.count(ScanHistory.id)).filter(ScanHistory.user_id == current_user.id, ScanHistory.risk == "Low Risk").scalar() or 0
    
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    monthly_scans = db.query(func.count(ScanHistory.id)).filter(ScanHistory.user_id == current_user.id, ScanHistory.created_at >= thirty_days_ago).scalar() or 0
    
    # Generate Charts
    plt.style.use('bmh')
    
    # 1. Pie Chart
    fig1, ax1 = plt.subplots(figsize=(4, 4))
    ax1.pie([high, medium, low], labels=['High', 'Medium', 'Low'], colors=['#DC2626', '#F59E0B', '#16A34A'], autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    plt.title('Risk Distribution')
    buf_pie = io.BytesIO()
    plt.savefig(buf_pie, format='png', bbox_inches='tight')
    buf_pie.seek(0)
    plt.close(fig1)
    
    # 2. Line Chart (Fraud Trend)
    daily_scans = db.query(func.date(ScanHistory.created_at), func.count(ScanHistory.id))\
        .filter(ScanHistory.user_id == current_user.id, ScanHistory.risk == "High Risk")\
        .group_by(func.date(ScanHistory.created_at))\
        .order_by(func.date(ScanHistory.created_at).desc())\
        .limit(14).all()
    
    dates = [d[0] for d in reversed(daily_scans)]
    counts = [d[1] for d in reversed(daily_scans)]
    
    fig2, ax2 = plt.subplots(figsize=(6, 3))
    ax2.plot(dates, counts, marker='o', color='#DC2626')
    ax2.set_title('Fraud Trend (High Risk, Last 14 Days)')
    ax2.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    buf_line = io.BytesIO()
    plt.savefig(buf_line, format='png')
    buf_line.seek(0)
    plt.close(fig2)

    class AnalyticsPDF(FPDF):
        def header(self):
            self.set_font("helvetica", "B", 24)
            self.set_text_color(17, 17, 17)
            self.cell(0, 10, "JOBX", align="L")
            self.set_font("helvetica", "", 12)
            self.cell(0, 10, "Analytics Report", align="R")
            self.ln(15)
            self.set_font("helvetica", "", 10)
            self.set_text_color(107, 114, 128)
            self.cell(0, 5, f"User: {current_user.name} ({current_user.email})", align="L")
            self.ln(5)
            self.cell(0, 5, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", align="L")
            self.ln(10)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(5)
            
        def footer(self):
            self.set_y(-15)
            self.set_font("helvetica", "I", 8)
            self.set_text_color(107, 114, 128)
            self.cell(0, 10, f"Page {self.page_no()}", align="C")

    pdf = AnalyticsPDF()
    pdf.add_page()
    
    # Dashboard Summary
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(17, 17, 17)
    pdf.cell(0, 10, "Dashboard Summary")
    pdf.ln(10)
    
    pdf.set_font("helvetica", "", 10)
    pdf.cell(50, 8, f"Total Detections: {total}")
    pdf.cell(50, 8, f"Average Fraud Score: {avg_score}%")
    pdf.cell(50, 8, f"Monthly Scans (30d): {monthly_scans}")
    pdf.ln(8)
    pdf.cell(50, 8, f"High Risk: {high} ({round((high/total)*100, 1) if total > 0 else 0}%)")
    pdf.cell(50, 8, f"Medium Risk: {medium} ({round((medium/total)*100, 1) if total > 0 else 0}%)")
    pdf.cell(50, 8, f"Low Risk: {low} ({round((low/total)*100, 1) if total > 0 else 0}%)")
    pdf.ln(15)
    
    # Charts
    pdf.image(buf_pie, x=15, y=pdf.get_y(), w=70)
    pdf.image(buf_line, x=100, y=pdf.get_y(), w=100)
    
    return Response(content=bytes(pdf.output()), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=jobx_analytics.pdf"})

@app.get("/api/reports/pdf")
def generate_reports_pdf_v2(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    import io
    from fpdf import FPDF
    import matplotlib.pyplot as plt
    from datetime import datetime
    
    total = db.query(func.count(ScanHistory.id)).filter(ScanHistory.user_id == current_user.id).scalar() or 0
    if total == 0:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, "JOBX - Reports", align="C")
        pdf.ln(20)
        pdf.set_font("helvetica", size=12)
        pdf.cell(0, 10, "No scan history available.", align="C")
        return Response(content=bytes(pdf.output()), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=jobx_reports.pdf"})
        
    avg_score_raw = db.query(func.avg(ScanHistory.probability)).filter(ScanHistory.user_id == current_user.id).scalar()
    avg_score = round(avg_score_raw, 1) if avg_score_raw else 0
    
    high = db.query(func.count(ScanHistory.id)).filter(ScanHistory.user_id == current_user.id, ScanHistory.risk == "High Risk").scalar() or 0
    medium = db.query(func.count(ScanHistory.id)).filter(ScanHistory.user_id == current_user.id, ScanHistory.risk == "Medium Risk").scalar() or 0
    low = db.query(func.count(ScanHistory.id)).filter(ScanHistory.user_id == current_user.id, ScanHistory.risk == "Low Risk").scalar() or 0
    
    # Generate Chart
    plt.style.use('bmh')
    fig1, ax1 = plt.subplots(figsize=(4, 4))
    ax1.pie([high, medium, low], labels=['High', 'Medium', 'Low'], colors=['#DC2626', '#F59E0B', '#16A34A'], autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    plt.title('Risk Distribution')
    buf_pie = io.BytesIO()
    plt.savefig(buf_pie, format='png', bbox_inches='tight')
    buf_pie.seek(0)
    plt.close(fig1)
    
    class ReportsPDF(FPDF):
        def header(self):
            self.set_font("helvetica", "B", 24)
            self.set_text_color(17, 17, 17)
            self.cell(0, 10, "JOBX Logo", align="L")
            self.set_font("helvetica", "", 12)
            self.cell(0, 10, "Scan Reports", align="R")
            self.ln(15)
            self.set_font("helvetica", "", 10)
            self.set_text_color(107, 114, 128)
            self.cell(0, 5, f"Username: {current_user.name} ({current_user.email})", align="L")
            self.ln(5)
            self.cell(0, 5, f"Date & Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", align="L")
            self.ln(10)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(5)
            
        def footer(self):
            self.set_y(-15)
            self.set_font("helvetica", "I", 8)
            self.set_text_color(107, 114, 128)
            self.cell(0, 10, f"Page {self.page_no()}", align="C")

    pdf = ReportsPDF()
    pdf.add_page()
    
    # Summary
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(17, 17, 17)
    pdf.cell(0, 10, "Overall Summary")
    pdf.ln(10)
    
    pdf.set_font("helvetica", "", 10)
    pdf.cell(40, 8, f"Total Scans: {total}")
    pdf.cell(50, 8, f"Average Fraud Score: {avg_score}%")
    pdf.ln(8)
    pdf.cell(40, 8, f"High Risk: {high}")
    pdf.cell(40, 8, f"Medium Risk: {medium}")
    pdf.cell(40, 8, f"Low Risk: {low}")
    pdf.ln(15)
    
    # Charts
    pdf.image(buf_pie, x=15, y=pdf.get_y(), w=70)
    
    pdf.ln(80)
    
    # Scan History Summary & AI Recommendations
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "Scan History Summary & AI Recommendations")
    pdf.ln(10)
    
    recent_scans = db.query(ScanHistory).filter(ScanHistory.user_id == current_user.id).order_by(ScanHistory.created_at.desc()).limit(15).all()
    for s in recent_scans:
        pdf.set_font("helvetica", "B", 10)
        title = (s.title[:60] + "..") if len(s.title) > 60 else s.title
        pdf.cell(0, 6, f"{title} [{s.risk} - {s.probability}%]", ln=1)
        pdf.set_font("helvetica", "", 9)
        pdf.cell(0, 6, f"Date: {s.created_at.strftime('%Y-%m-%d')} | Flags: {s.warning_flags or 'None'}", ln=1)
        
        pdf.set_font("helvetica", "I", 9)
        pdf.set_text_color(75, 85, 99)
        explanation = (s.explanation[:120] + "..") if s.explanation and len(s.explanation) > 120 else (s.explanation or "No explanation available.")
        pdf.cell(0, 6, f"AI Explanation: {explanation}", ln=1)
        
        pdf.set_font("helvetica", "B", 9)
        pdf.set_text_color(17, 17, 17)
        if s.risk == "High Risk":
            rec = "AI Recommendation: Do NOT engage. This is highly likely a scam."
        elif s.risk == "Medium Risk":
            rec = "AI Recommendation: Proceed with caution. Verify the company and avoid sharing personal data."
        else:
            rec = "AI Recommendation: Safe to proceed based on current data."
        pdf.cell(0, 6, rec, ln=1)
        pdf.ln(4)
        
    return Response(content=bytes(pdf.output()), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=jobx_reports.pdf"})
>>>>>>> 9509c9af2835da46da2912733bb9952c531a46c6
