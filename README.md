# JOBX – Fake Job Posting Detector

JOBX is a web application that helps users assess potentially fraudulent job postings and suspicious recruitment messages. It combines a machine-learning classifier with rule-based checks to highlight warning signs and provide a risk assessment.

> **Note:** JOBX is an educational project. Its results are not a guarantee that a job is genuine or fraudulent. Always verify employers independently.

## Features

- **Job Posting Analysis:** Submit job details for a fake-job prediction.
- **Suspicious Message Analysis:** Check recruitment messages for common scam indicators.
- **Hybrid Risk Assessment:** Combines machine-learning predictions with rule-based checks.
- **Warning Explanations:** Highlights suspicious payment requests, messaging platforms, artificial urgency, and unrealistic promises.
- **User Authentication:** Sign-up and login functionality.
- **Scan History:** Access saved scan information.
- **Data Export:** Export available scan data in supported formats.
- **Account Settings:** Manage account preferences and security-related settings.

## Technology Stack

### Backend
- Python
- FastAPI
- Scikit-learn
- Joblib
- SQLAlchemy
- SQLite
- JWT Authentication
- Pandas

### Frontend
- Next.js
- React
- TypeScript
- Tailwind CSS
- Framer Motion

## Project Structure

```text
fake-job-detecter/
├── backend/       # FastAPI backend
├── frontend/      # Next.js frontend
├── model/         # Machine learning model files
├── preprocess.py  # Text preprocessing
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or later
- Node.js and npm
- Trained model files:
  - `model/classifier.pkl`
  - `model/vectorizer.pkl`

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/KhamrunnisaAnjum/fake-job-detecter.git
cd fake-job-detecter
```

### 2. Set up the backend

```bash
cd backend
python -m pip install -r requirements.txt
```

Create a `.env` file inside the `backend` folder:

```env
SECRET_KEY=your_generated_secret_key
```

Replace the example with a securely generated random secret. Never upload your `.env` file to GitHub.

Start the backend:

```bash
python -m uvicorn main:app --reload --port 8080
```

Backend API: http://127.0.0.1:8080

Interactive API documentation: http://127.0.0.1:8080/docs

### 3. Set up the frontend

Open a second terminal in the project root:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 in your browser.

## Project Status

JOBX is an ongoing development project. Frontend and backend integration, security-sensitive features, and deployment configuration require further testing and review before public production use.

## Disclaimer

JOBX is designed for educational purposes and job-scam awareness. Its predictions may not always be accurate. Always independently verify job offers and employers before sharing personal information or making decisions.
