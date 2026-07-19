from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import sys
import os

from database import Base, engine, SessionLocal
from models import ScanHistory

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