# ================= app.py =================
# JobShield AI — Fake Job Posting Detector

from streamlit_option_menu import option_menu
from auth import login
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
import os
import re
import csv
from datetime import datetime

from preprocess import clean_text
from risk_rules import get_risk_flags


# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="JobShield AI | Trust Console",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "menu_selection" not in st.session_state:
    st.session_state.menu_selection = "Dashboard"

if not st.session_state.logged_in:
    login()
    st.stop()


# =====================================================================
# ===========================  GLOBAL CSS  ============================
# =====================================================================

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
.stApp { background-color: #FFFFFF !important; }
#MainMenu, footer { visibility: hidden !important; }
/* Keep the sidebar toggle button visible — only hide Streamlit's deploy button */
header[data-testid="stHeader"] { background: transparent !important; }
header[data-testid="stHeader"] > div:first-child { visibility: hidden !important; }
/* Make sure the sidebar collapse arrow/toggle is always shown */
button[data-testid="stSidebarCollapsedControl"],
div[data-testid="stSidebarCollapsedControl"] {
    visibility: visible !important;
    display: flex !important;
    opacity: 1 !important;
    z-index: 999999 !important;
}
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 4rem !important;
    max-width: 1200px !important;
}
h1,h2,h3,h4,h5,h6 {
    color: #0F172A !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em !important;
}
hr { border-color: #F4F4F5 !important; }

/* SIDEBAR */
section[data-testid="stSidebar"] {
    width: 240px !important;
    min-width: 240px !important;
    max-width: 240px !important;
    background-color: #FFFFFF !important;
    border-right: 1px solid #E4E4E7 !important;
}
section[data-testid="stSidebar"] > div {
    padding-top: 1.25rem !important;
    padding-left: 10px !important;
    padding-right: 10px !important;
}
.workspace-selector {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 10px; border-radius: 6px;
    background: #F4F4F5; border: 1px solid #E4E4E7;
    margin-bottom: 16px; cursor: pointer;
}
.workspace-avatar {
    width: 28px; height: 28px; border-radius: 5px;
    background: #0F172A; color: #FFFFFF;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 12px;
}
.workspace-info { flex-grow: 1; display: flex; flex-direction: column; gap: 1px; }
.workspace-name { font-size: 13px; font-weight: 600; color: #0F172A; letter-spacing: -0.01em; }
.workspace-plan { font-size: 10px; color: #71717A; font-weight: 500; }
.workspace-chevron { color: #71717A; font-size: 12px; }
.sidebar-search {
    display: flex; align-items: center; gap: 8px;
    padding: 8px 10px; border-radius: 6px;
    border: 1px solid #E4E4E7; background: #FFFFFF;
    color: #A1A1AA; font-size: 12.5px; margin-bottom: 16px;
}
.sidebar-search span { flex-grow: 1; }
.sidebar-search kbd {
    background: #F4F4F5; border: 1px solid #E4E4E7;
    border-radius: 4px; padding: 1px 4px;
    font-size: 9.5px; font-family: monospace; color: #71717A;
}
.sidebar-note {
    background: #FAFAFA; border: 1px solid #E4E4E7;
    border-radius: 6px; padding: 10px 12px; margin-top: 20px;
}
.sidebar-note p { margin: 0; font-size: 11.5px; color: #71717A; line-height: 1.45; }

/* TOP BAR */
.breadcrumbs { display: flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 500; }
.bc-parent { color: #71717A; }
.bc-separator { color: #D4D4D8; }
.bc-active { color: #0F172A; font-weight: 600; }
.icon-btn {
    width: 34px; height: 34px; border-radius: 6px;
    background: #FFFFFF; border: 1px solid #E4E4E7;
    display: flex; align-items: center; justify-content: center;
    position: relative; color: #52525B; font-size: 15px;
}
.notif-badge {
    position: absolute; top: -4px; right: -4px;
    background: #EF4444; color: white; font-size: 8.5px; font-weight: 700;
    min-width: 14px; height: 14px; border-radius: 999px;
    display: flex; align-items: center; justify-content: center;
    padding: 0 3px; border: 2px solid white;
}
.user-chip {
    display: flex; align-items: center; gap: 8px;
    padding: 3px 10px 3px 3px; border-radius: 999px;
    background: #F4F4F5; border: 1px solid #E4E4E7;
}
.user-chip .avatar {
    width: 26px; height: 26px; border-radius: 50%;
    background: #0F172A; color: white;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 700;
}
.user-chip .u-name { font-size: 11px; font-weight: 600; color: #0F172A; line-height: 1.1; }
.user-chip .u-role { font-size: 9.5px; color: #71717A; line-height: 1.1; }

/* DASHBOARD HERO */
.dashboard-hero { padding: 32px 0 24px 0; }
.hero-badge {
    display: inline-flex; align-items: center;
    background: #EFF6FF; color: #1D4ED8; border: 1px solid #DBEAFE;
    padding: 4px 10px; border-radius: 9999px;
    font-size: 11px; font-weight: 600; letter-spacing: 0.05em; margin-bottom: 16px;
}
.hero-title {
    font-size: 36px !important; font-weight: 850 !important;
    color: #0F172A !important; letter-spacing: -0.035em !important;
    line-height: 1.15 !important; margin-bottom: 14px !important; max-width: 720px;
}
.hero-desc {
    font-size: 15.5px; color: #52525B; line-height: 1.6;
    max-width: 680px; margin-bottom: 24px; font-weight: 400;
}
.trust-indicator-row {
    display: flex; gap: 24px; margin-top: 28px;
    padding-top: 24px; border-top: 1px solid #F4F4F5;
}
.trust-item { font-size: 12px; color: #71717A; font-weight: 500; display: flex; align-items: center; gap: 6px; }

/* PAGE HEADER */
.page-header { margin-bottom: 24px; padding-bottom: 10px; }
.page-header h1 {
    font-size: 24px; font-weight: 750; color: #0F172A;
    margin: 0 0 6px 0; letter-spacing: -0.025em;
}
.page-header p { font-size: 14px; color: #52525B; margin: 0; line-height: 1.5; }

/* CARDS */
.main div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E4E4E7 !important;
    border-radius: 8px !important;
    padding: 20px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    transition: all 0.15s ease-in-out !important;
}
.main div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #D4D4D8 !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04) !important;
}
.section-title {
    font-size: 14.5px; font-weight: 600; color: #0F172A;
    margin: 0 0 4px 0; display: flex; align-items: center; gap: 8px;
}
.section-subtitle { font-size: 12px; color: #71717A; margin: 0 0 16px 0; }

/* INPUTS */
.stTextInput input, .stTextArea textarea, .stSelectbox > div > div {
    border-radius: 6px !important; border: 1px solid #E4E4E7 !important;
    background: #FFFFFF !important; font-size: 13.5px !important;
    color: #0F172A !important; transition: all 0.15s ease !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #0F172A !important;
    box-shadow: 0 0 0 2px rgba(15,23,42,0.05) !important;
}
label, .stCheckbox label p {
    font-weight: 500 !important; color: #27272A !important;
    font-size: 12.5px !important; margin-bottom: 4px !important;
}
.stTextArea textarea {
    font-size: 13.5px !important; line-height: 1.65 !important;
    font-family: 'Inter', sans-serif !important; resize: vertical !important;
}

/* INPUT MODE TAB SWITCHER — handled via st.button + session_state, no CSS needed */

/* BUTTONS */
div.stButton > button {
    border-radius: 6px !important; height: 38px !important;
    font-weight: 550 !important; font-size: 13.5px !important;
    letter-spacing: -0.01em !important; transition: all 0.15s ease !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
}
div[data-testid="stBaseButton-primary"] {
    background-color: #0F172A !important; color: #FFFFFF !important;
    border: 1px solid #0F172A !important;
}
div[data-testid="stBaseButton-primary"]:hover {
    background-color: #1E293B !important; border-color: #1E293B !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(15,23,42,0.08) !important;
}
div[data-testid="stBaseButton-secondary"] {
    background-color: #FFFFFF !important; color: #0F172A !important;
    border: 1px solid #E4E4E7 !important;
}
div[data-testid="stBaseButton-secondary"]:hover {
    background-color: #F4F4F5 !important; border-color: #D4D4D8 !important;
}
div[data-testid="stDownloadButton"] > button {
    background: #FFFFFF !important; color: #0F172A !important;
    border: 1px solid #E4E4E7 !important; border-radius: 6px !important;
    height: 38px !important; font-weight: 550 !important; font-size: 13.5px !important;
}

/* METRICS */
.metric-card {
    background: #FFFFFF; border: 1px solid #E4E4E7; border-radius: 8px;
    padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: all 0.15s ease-in-out; min-height: 110px;
    display: flex; flex-direction: column; justify-content: space-between;
}
.metric-card:hover { border-color: #D4D4D8; box-shadow: 0 4px 12px rgba(0,0,0,0.04); }
.metric-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px; }
.metric-title { font-size: 11.5px; font-weight: 600; color: #71717A; text-transform: uppercase; letter-spacing: 0.05em; }
.metric-icon-wrap { width: 26px; height: 26px; border-radius: 5px; display: flex; align-items: center; justify-content: center; font-size: 12px; }
.metric-icon-blue { background: #EFF6FF; color: #3B82F6; }
.metric-icon-red { background: #FEF2F2; color: #EF4444; }
.metric-icon-orange { background: #FFF7ED; color: #F59E0B; }
.metric-icon-green { background: #ECFDF5; color: #10B981; }
.metric-value { font-size: 24px; font-weight: 700; color: #0F172A; letter-spacing: -0.025em; line-height: 1.1; margin: 2px 0; }
.metric-footer { display: flex; align-items: center; gap: 6px; font-size: 11.5px; font-weight: 500; margin-top: 4px; }
.trend-up { color: #15803D; background: #DCFCE7; padding: 1px 5px; border-radius: 4px; }
.trend-down { color: #B91C1C; background: #FEE2E2; padding: 1px 5px; border-radius: 4px; }
.trend-neutral { color: #52525B; background: #F4F4F5; padding: 1px 5px; border-radius: 4px; }
.trend-text { color: #71717A; }

/* SCAN FEED */
.scan-feed { display: flex; flex-direction: column; }
.scan-item { display: flex; align-items: center; gap: 12px; padding: 10px 0; border-bottom: 1px solid #F4F4F5; }
.scan-item:last-child { border-bottom: none; }
.scan-avatar { width: 30px; height: 30px; border-radius: 5px; background: #F4F4F5; color: #0F172A; border: 1px solid #E4E4E7; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 12px; }
.scan-details { flex-grow: 1; display: flex; flex-direction: column; gap: 1px; }
.scan-title { font-size: 13px; font-weight: 600; color: #0F172A; }
.scan-meta { font-size: 11px; color: #71717A; display: flex; align-items: center; gap: 6px; }
.scan-meta-bullet { color: #E4E4E7; }

/* RISK BADGES */
.security-badge {
    display: inline-flex; align-items: center; gap: 6px; padding: 3px 8px;
    border-radius: 9999px; font-size: 10.5px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.04em; border: 1px solid transparent;
}
.badge-high { background: #FEF2F2; color: #991B1B; border-color: #FEE2E2; }
.badge-medium { background: #FFFBEB; color: #92400E; border-color: #FEF3C7; }
.badge-low { background: #F0FDF4; color: #166534; border-color: #DCFCE7; }

.factor-pill {
    display: inline-flex; align-items: center; gap: 6px;
    background: #F4F4F5; border: 1px solid #E4E4E7; border-radius: 6px;
    padding: 5px 10px; font-size: 12px; font-weight: 500; color: #18181B;
    margin-right: 6px; margin-bottom: 6px;
}
.factor-critical { background: #FEF2F2 !important; border-color: #FEE2E2 !important; color: #991B1B !important; }

.recommendation-box {
    background: #FAFAFA; border: 1px solid #E4E4E7; border-radius: 6px;
    padding: 14px 16px; margin-top: 14px; display: flex; gap: 10px; align-items: flex-start;
}
.reco-icon-wrap { color: #71717A; font-size: 15px; margin-top: 1px; }
.reco-content { display: flex; flex-direction: column; gap: 2px; }
.reco-title { font-size: 12.5px; font-weight: 600; color: #0F172A; }
.reco-text { font-size: 12px; color: #52525B; line-height: 1.45; }

/* SCORE RING */
.security-indicator { text-align: center; padding: 10px 0; }
.security-score-circle {
    position: relative; display: inline-flex; align-items: center; justify-content: center;
    width: 130px; height: 130px; border-radius: 50%;
    background: #FFFFFF; border: 8px solid #F4F4F5;
    margin-bottom: 12px; box-shadow: inset 0 1px 3px rgba(0,0,0,0.02), 0 4px 16px rgba(0,0,0,0.06);
}
.score-high { border-color: #FEE2E2; color: #EF4444; }
.score-medium { border-color: #FEF3C7; color: #F59E0B; }
.score-low { border-color: #DCFCE7; color: #10B981; }
.security-score-val { font-size: 34px; font-weight: 800; letter-spacing: -0.03em; }
.security-score-pct { font-size: 14px; font-weight: 600; color: #71717A; }
.analysis-placeholder { text-align: center; padding: 60px 10px; color: #A1A1AA; font-size: 13px; }
.analysis-placeholder .ph-icon { font-size: 36px; margin-bottom: 12px; color: #E4E4E7; }

/* SOURCE CHIPS */
.scan-source-chips { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; }
.source-chip {
    display: inline-flex; align-items: center; gap: 5px;
    background: #F4F4F5; border: 1px solid #E4E4E7; border-radius: 999px;
    padding: 3px 10px; font-size: 11.5px; font-weight: 500; color: #52525B;
}

/* EXTRACTED INFO TABLE */
.info-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
.info-table td { padding: 8px 10px; font-size: 12.5px; border-bottom: 1px solid #F4F4F5; vertical-align: top; }
.info-table td:first-child { font-weight: 600; color: #52525B; white-space: nowrap; width: 130px; }
.info-table td:last-child { color: #0F172A; word-break: break-word; }
.info-table tr:last-child td { border-bottom: none; }

/* DATA TABLE */
div[data-testid="stDataFrame"] { border: 1px solid #E4E4E7 !important; border-radius: 6px !important; overflow: hidden !important; }

/* ABOUT */
.about-hero { text-align: center; padding: 24px 0 32px 0; border-bottom: 1px solid #F4F4F5; margin-bottom: 24px; }
.about-hero h2 { font-size: 28px; font-weight: 850; color: #0F172A; letter-spacing: -0.03em; margin-bottom: 8px; }
.about-hero p { font-size: 15px; color: #52525B; max-width: 560px; margin: 0 auto; line-height: 1.55; }
.grid-3col { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }
.about-card { background: #FFFFFF; border: 1px solid #E4E4E7; border-radius: 6px; padding: 20px; }
.about-card:hover { border-color: #D4D4D8; box-shadow: 0 4px 10px rgba(0,0,0,0.02); }
.about-card-icon { width: 34px; height: 34px; border-radius: 5px; background: #F4F4F5; color: #0F172A; display: flex; align-items: center; justify-content: center; font-size: 14px; margin-bottom: 14px; border: 1px solid #E4E4E7; }
.about-card h3 { font-size: 14.5px; font-weight: 600; color: #0F172A; margin: 0 0 6px 0; }
.about-card p { font-size: 12.5px; color: #52525B; line-height: 1.5; margin: 0; }
.about-footer { text-align: center; padding-top: 20px; font-size: 12px; color: #71717A; border-top: 1px solid #F4F4F5; }
</style>
"""

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">',
    unsafe_allow_html=True
)


# =====================================================================
# ==========================  BACKEND  ================================
# =====================================================================

classifier = joblib.load("model/classifier.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

LOG_FILE = "checked_postings.csv"


def save_prediction(title, risk, score, raw_message=None):
    """Append one scan result row to the CSV log safely."""
    file_exists = os.path.exists(LOG_FILE)
    # Clean title — strip newlines so the CSV row stays on one line
    safe_title = str(title).replace("\n", " ").replace("\r", "")[:120]
    # Store raw_message on a single line (escaped)
    safe_msg = (raw_message or "").replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        if not file_exists:
            writer.writerow(["timestamp", "title", "risk", "score", "raw_message"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            safe_title,
            risk,
            score,
            safe_msg
        ])


def predict_job(title, company, description, requirements, salary):
    """Original ML prediction — completely unchanged."""
    text = " ".join([title, company, description, requirements, salary])
    cleaned_text = clean_text(text)
    vector = vectorizer.transform([cleaned_text])
    probability = classifier.predict_proba(vector)[0][1]
    prediction = classifier.predict(vector)[0]
    result = "Fake Job" if prediction == 1 else "Real Job"
    return result, probability


def load_history():
    if os.path.exists(LOG_FILE):
        try:
            df = pd.read_csv(
                LOG_FILE,
                quoting=csv.QUOTE_ALL,
                on_bad_lines="skip",
                encoding="utf-8"
            )
        except Exception:
            # Fallback: read without strict quoting
            try:
                df = pd.read_csv(LOG_FILE, on_bad_lines="skip", encoding="utf-8")
            except Exception:
                return pd.DataFrame(columns=["timestamp", "title", "risk", "score", "raw_message"])
        # Ensure required columns exist
        for col in ["timestamp", "title", "risk", "score", "raw_message"]:
            if col not in df.columns:
                df[col] = ""
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0)
        df = df.dropna(subset=["risk"]).sort_values("timestamp")
        return df
    return pd.DataFrame(columns=["timestamp", "title", "risk", "score", "raw_message"])


# =====================================================================
# ==============  ENHANCED RULE ENGINE (FRONTEND ONLY)  ==============
# =====================================================================

def analyze_message_rules(text):
    """
    Rule-based detection for real-world job messages.
    Returns list of (icon, message, is_critical) tuples.
    Does NOT modify risk_rules.py.
    """
    flags = []
    t = text.lower()

    # WhatsApp / Telegram links
    if re.search(r'chat\.whatsapp\.com|wa\.me|whatsapp', t):
        flags.append(("bi-whatsapp", "Redirects users to WhatsApp group/link", True))
    if re.search(r't\.me/|telegram\.me|join.*telegram|telegram.*group', t):
        flags.append(("bi-telegram", "Redirects users to Telegram", True))

    # URL shorteners
    if re.search(r'bit\.ly|tinyurl|goo\.gl|ow\.ly|t\.co|cutt\.ly|rb\.gy|shorturl', t):
        flags.append(("bi-link-45deg", "Uses suspicious shortened URLs", True))

    # Personal email (Gmail/Yahoo used as contact)
    if re.search(r'@gmail\.com|@yahoo\.com|@hotmail\.com|@outlook\.com', t):
        flags.append(("bi-envelope-exclamation", "Uses personal email instead of company domain", True))

    # Urgency language
    urgency = [r'limited seats?', r'limited slots?', r'hurry', r'act now', r'apply immediately',
                r'urgent(ly)?', r'last (few|chance)', r'deadline (today|tomorrow|soon)',
                r"don'?t miss", r'first come', r'closing soon', r'only \d+ (seats?|spots?|slots?) left',
                r'register (now|today|fast)', r'enrol+\s?(now|today|fast)']
    if any(re.search(p, t) for p in urgency):
        flags.append(("bi-alarm", "Uses urgency / pressure language", False))

    # Payment requests
    payment = [r'registration fee', r'processing fee', r'security deposit',
               r'advance payment', r'pay to (apply|join|register)',
               r'deposit (required|needed)', r'qr code', r'upi id', r'upi payment',
               r'send money', r'pay ₹', r'payment (required|needed)',
               r'crypto(currency)?', r'bitcoin', r'ethereum']
    if any(re.search(p, t) for p in payment):
        flags.append(("bi-credit-card-2-front", "Requests payment from applicant — major red flag", True))

    # Unrealistic salary
    earn = [r'earn ₹\s*\d{4,}', r'₹\s*\d+[,\d]*\s*(per|/)\s*(week|day|month)',
            r'earn upto', r'earn up to', r'\d+[,\d]*\s*per\s*week',
            r'high (salary|pay|income)', r'unlimited (earning|income)',
            r'guaranteed (income|salary|pay)', r'100% (placement|job guarantee)']
    if any(re.search(p, t) for p in earn):
        flags.append(("bi-currency-rupee", "Promises unrealistic / guaranteed earnings", True))

    # Famous brand impersonation
    brands = ['ibm', 'microsoft', 'google', 'amazon', 'apple', 'facebook', 'meta',
              'infosys', 'tcs', 'wipro', 'accenture', 'iit', 'iim', 'nasscom',
              'reliance', 'hdfc', 'icici', 'byju', 'flipkart', 'myntra']
    found = [b for b in brands if re.search(r'\b' + b + r'\b', t)]
    if found:
        flags.append(("bi-building-exclamation",
                      f"Mentions famous brands — possible impersonation: {', '.join(found[:3]).upper()}", True))

    # No salary mentioned
    salary_kw = [r'salary', r'stipend', r'pay', r'compensation', r'₹', r'lpa', r'ctc', r'per\s*(month|annum|year)']
    if not any(re.search(p, t) for p in salary_kw):
        flags.append(("bi-cash-stack", "No salary or compensation mentioned", False))

    # Certificate bait
    if re.search(r'certif(icate|ication|ied)', t):
        flags.append(("bi-award", "Promises certificate — common in scam internship ads", False))

    # WFH + no experience
    if re.search(r'work\s*from\s*home|wfh|remote', t):
        if re.search(r'no\s*(experience|exp)|fresher(s)?|0\s*(years?|yrs?)', t):
            flags.append(("bi-house-exclamation", "Work-from-home + no experience required — common scam pattern", False))
        else:
            flags.append(("bi-house", "Remote / work-from-home position", False))

    # Promotional language
    promo = [r'live projects?', r'industry (exposure|experience)',
             r'letter of (recommendation|reference)', r'internship (program|drive|fair)',
             r'batch of \d{4}', r'selected candidates?', r'top \d+ companies',
             r'partnered with', r'collaborated with']
    if any(re.search(p, t) for p in promo):
        flags.append(("bi-megaphone", "Uses promotional / marketing language typical of fake ads", False))

    # International opportunity
    if re.search(r'abroad|overseas|international (job|opportunity|placement)|visa (sponsorship|provided)', t):
        flags.append(("bi-globe", "Promises international opportunity", False))

    # Very short message
    if len(text.split()) < 40:
        flags.append(("bi-file-earmark-x", "Message is unusually short — very little information provided", False))

    return flags


# =====================================================================
# ==================  INFO EXTRACTOR (FRONTEND ONLY)  ================
# =====================================================================

def extract_info(text):
    info = {}

    emails = re.findall(r'[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}', text)
    info['email'] = ', '.join(emails[:3]) if emails else None

    phones = re.findall(r'(?:\+91[\-\s]?)?[6-9]\d{9}', text)
    info['phone'] = ', '.join(phones[:3]) if phones else None

    urls = re.findall(r'https?://[^\s\)\>]+', text)
    non_social = [u for u in urls if not any(x in u for x in ['whatsapp', 't.me', 'telegram'])]
    info['website'] = non_social[0] if non_social else None

    wa = re.findall(r'https?://chat\.whatsapp\.com/[^\s\)\>]+', text)
    tg = re.findall(r'https?://t\.me/[^\s\)\>]+', text)
    parts = []
    if wa: parts.append(f"WhatsApp Group ({len(wa)})")
    if tg: parts.append(f"Telegram ({len(tg)})")
    info['contact'] = ', '.join(parts) if parts else None

    sal = re.search(
        r'(?:salary|stipend|pay|ctc)[:\s]*([₹\d,\.]+\s*(?:lpa|per\s*(?:month|annum|year|week)|k)?)',
        text, re.IGNORECASE
    )
    if not sal:
        sal = re.search(r'₹\s*[\d,]+(?:\s*-\s*₹?\s*[\d,]+)?(?:\s*(?:lpa|per\s*\w+))?', text)
    info['salary'] = sal.group(0).strip() if sal else None

    big_brands = ['IBM', 'Microsoft', 'Google', 'Amazon', 'Apple', 'Facebook', 'Meta',
                  'Infosys', 'TCS', 'Wipro', 'Accenture', 'IIT', 'IIM',
                  'Reliance', 'HDFC', 'ICICI', 'Byju', 'Flipkart', 'Myntra']
    found_brands = [b for b in big_brands if re.search(r'\b' + b + r'\b', text, re.IGNORECASE)]
    info['company'] = ', '.join(found_brands[:4]) if found_brands else None

    lines = [l.strip() for l in text.split('\n') if l.strip()]
    if lines and 2 <= len(lines[0].split()) <= 8:
        info['title'] = lines[0]
    else:
        info['title'] = None

    info['remote'] = bool(re.search(r'work\s*from\s*home|wfh|remote\s*(work|job|position)', text, re.IGNORECASE))
    info['certificate'] = bool(re.search(r'certif(icate|ication|ied)', text, re.IGNORECASE))

    return info


# =====================================================================
# =======================  FRONTEND HELPERS  ==========================
# =====================================================================

RISK_COLORS = {
    "High Risk": "#EF4444",
    "Medium Risk": "#F59E0B",
    "Low Risk": "#10B981",
}

FLAG_ICON_MAP = {
    "No salary range provided": "bi-cash-coin",
    "Very little or no company information given": "bi-building",
    "Uses urgency-pressure language": "bi-alarm",
    "Asks for payment from applicant (major red flag)": "bi-credit-card",
    "Job description is unusually short": "bi-file-earmark-text",
}


def week_over_week(df, mask=None):
    if df.empty or "timestamp" not in df.columns:
        return "No scans yet", "neutral"
    working = df[mask] if mask is not None else df
    working = working.dropna(subset=["timestamp"])
    now = pd.Timestamp.now()
    last_week = now - pd.Timedelta(days=7)
    prev_week = now - pd.Timedelta(days=14)
    cur_n = len(working[working["timestamp"] >= last_week])
    prev_n = len(working[(working["timestamp"] >= prev_week) & (working["timestamp"] < last_week)])
    if prev_n == 0:
        return (f"{cur_n} new scans", "up") if cur_n else ("No data yet", "neutral")
    pct = round(((cur_n - prev_n) / prev_n) * 100, 1)
    if pct > 0: return f"↑ {pct}% this week", "up"
    if pct < 0: return f"↓ {abs(pct)}% this week", "down"
    return "No change vs last week", "neutral"


def time_ago(ts):
    if pd.isna(ts): return ""
    secs = (pd.Timestamp.now() - ts).total_seconds()
    if secs < 60: return "just now"
    if secs < 3600: return f"{int(secs//60)}m ago"
    if secs < 86400: return f"{int(secs//3600)}h ago"
    return f"{int(secs//86400)}d ago"


def metric_card(icon_class, color, title, value, trend_label=None, trend_dir="neutral"):
    color_map = {"blue": "metric-icon-blue", "red": "metric-icon-red",
                 "orange": "metric-icon-orange", "green": "metric-icon-green"}
    ic = color_map.get(color, "metric-icon-blue")
    trend_html = f'<div class="trend-{trend_dir}">{trend_label}</div>' if trend_label else '<div class="trend-neutral">No change</div>'
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">
            <span class="metric-title">{title}</span>
            <div class="metric-icon-wrap {ic}"><i class="bi {icon_class}"></i></div>
        </div>
        <div class="metric-value">{value}</div>
        <div class="metric-footer">{trend_html}<span class="trend-text">vs prev. period</span></div>
    </div>""", unsafe_allow_html=True)


def render_hero(title, subtitle):
    st.markdown(f"""
    <div class="page-header">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>""", unsafe_allow_html=True)


def render_top_bar(page_label, df):
    high_today = 0
    if not df.empty:
        today = pd.Timestamp.now().normalize()
        r = df.dropna(subset=["timestamp"])
        high_today = len(r[(r["timestamp"] >= today) & (r["risk"] == "High Risk")])

    c1, c2, c3 = st.columns([5, 0.6, 1.6])
    with c1:
        st.markdown(f"""<div class="breadcrumbs" style="margin-top:6px;">
            <span class="bc-parent">Console</span>
            <span class="bc-separator">/</span>
            <span class="bc-active">{page_label}</span>
        </div>""", unsafe_allow_html=True)
    with c2:
        badge = f'<span class="notif-badge">{high_today}</span>' if high_today else ""
        st.markdown(f'<div style="display:flex;justify-content:flex-end;margin-top:2px;"><div class="icon-btn"><i class="bi bi-bell"></i>{badge}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div style="display:flex;justify-content:flex-end;"><div class="user-chip"><div class="avatar">U</div><div><div class="u-name">Admin User</div><div class="u-role">Threat Auditor</div></div></div></div>', unsafe_allow_html=True)


def risk_donut_chart(risk_count):
    labels = list(risk_count.index)
    values = list(risk_count.values)
    colors = [RISK_COLORS.get(r, "#71717A") for r in labels]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.72,
                                  marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
                                  textinfo="none", sort=False)])
    fig.update_layout(showlegend=False, margin=dict(l=10,r=10,t=10,b=10),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=190,
                      annotations=[dict(text=f"<b>{sum(values)}</b><br><span style='font-size:9.5px;color:#71717A'>Scans</span>",
                                        x=0.5, y=0.5, showarrow=False, font=dict(size=16, color="#0F172A"))])
    return fig


def fraud_score_chart(df):
    recent = df.dropna(subset=["timestamp"]).tail(20)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=recent["timestamp"], y=recent["score"],
                             mode="lines+markers",
                             line=dict(color="#0F172A", width=2.5, shape="spline"),
                             marker=dict(size=4.5, color="#0F172A"),
                             fill="tozeroy", fillcolor="rgba(15,23,42,0.03)"))
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                      margin=dict(l=10,r=10,t=10,b=10), height=190,
                      xaxis=dict(showgrid=False, linecolor="#E4E4E7"),
                      yaxis=dict(showgrid=True, gridcolor="#F4F4F5", linecolor="#E4E4E7", range=[0,105]))
    return fig


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="workspace-selector">
            <div class="workspace-avatar">JS</div>
            <div class="workspace-info">
                <span class="workspace-name">JobShield Team</span>
                <span class="workspace-plan">Pro Console</span>
            </div>
            <i class="bi bi-chevron-expand workspace-chevron"></i>
        </div>
        <div class="sidebar-search">
            <i class="bi bi-search"></i>
            <span>Search console...</span>
            <kbd>⌘K</kbd>
        </div>""", unsafe_allow_html=True)

        menu_options = ["Dashboard", "Scan New Job", "History", "Analytics", "Risk Factors", "Reports", "Settings", "About"]
        default_idx = menu_options.index(st.session_state.menu_selection) if st.session_state.menu_selection in menu_options else 0

        selected = option_menu(
            menu_title=None,
            options=menu_options,
            icons=["grid-1x2", "search", "clock-history", "bar-chart-line",
                   "shield-exclamation", "file-earmark-text", "gear", "info-circle"],
            default_index=default_idx,
            key="sidebar_option_menu",
            styles={
                "container": {"padding": "0!important", "background-color": "#FFFFFF"},
                "icon": {"color": "#71717A", "font-size": "13.5px"},
                "nav-link": {"font-size": "12.5px", "text-align": "left", "margin": "2px 0",
                             "padding": "7px 10px", "border-radius": "5px",
                             "color": "#52525B", "font-weight": "500", "--hover-color": "#F4F4F5"},
                "nav-link-selected": {"background-color": "#F4F4F5", "color": "#0F172A", "font-weight": "600"},
            },
        )
        st.markdown('<div class="sidebar-note"><p>🤖 Zero-Trust threat classifier protecting recruitment pipelines.</p></div>', unsafe_allow_html=True)
        st.session_state.menu_selection = selected
        return selected


# =====================================================================
# ==============================  PAGES  ==============================
# =====================================================================

def page_dashboard(df):
    st.markdown("""
    <div class="dashboard-hero">
        <div class="hero-badge">🟢 HEURISTICS ACTIVE &amp; SECURE</div>
        <h1 class="hero-title">Protect your applications with JobShield AI</h1>
        <p class="hero-desc">An AI-powered threat validation platform designed to detect fee scams and data harvesting posting networks in real time.</p>
    </div>""", unsafe_allow_html=True)

    c1, c2, _ = st.columns([1.1, 1.2, 3])
    with c1:
        if st.button("✨ Run New Scan", type="primary", use_container_width=True, key="dash_scan"):
            st.session_state.menu_selection = "Scan New Job"; st.rerun()
    with c2:
        if st.button("📋 View Audit Logs", type="secondary", use_container_width=True, key="dash_logs"):
            st.session_state.menu_selection = "History"; st.rerun()

    st.markdown("""<div class="trust-indicator-row">
        <span class="trust-item"><i class="bi bi-cpu"></i> ML Model Inference Active</span>
        <span class="trust-item"><i class="bi bi-terminal"></i> NLP Text Vectorization</span>
        <span class="trust-item"><i class="bi bi-cloud-check"></i> Real-time CSV Audit Logs</span>
    </div><div style="height:32px;"></div>""", unsafe_allow_html=True)

    if df.empty:
        with st.container(border=True):
            st.info("No scanned data available. Run your first threat scan to populate telemetry.")
        return

    total = len(df)
    high_n = len(df[df["risk"] == "High Risk"])
    med_n = len(df[df["risk"] == "Medium Risk"])
    low_n = len(df[df["risk"] == "Low Risk"])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        lbl, d = week_over_week(df); metric_card("bi-briefcase", "blue", "Total Audits", total, lbl, d)
    with c2:
        lbl, d = week_over_week(df, df["risk"] == "High Risk"); metric_card("bi-exclamation-triangle", "red", "High Risk Alerts", high_n, lbl, d)
    with c3:
        lbl, d = week_over_week(df, df["risk"] == "Medium Risk"); metric_card("bi-shield-plus", "orange", "Medium Risk Alerts", med_n, lbl, d)
    with c4:
        lbl, d = week_over_week(df, df["risk"] == "Low Risk"); metric_card("bi-patch-check", "green", "Safe Clearances", low_n, lbl, d)

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown('<p class="section-title"><i class="bi bi-pie-chart"></i> Risk Distribution</p><p class="section-subtitle">Breakdown of scanned postings by alert level</p>', unsafe_allow_html=True)
            risk_count = df["risk"].value_counts()
            st.plotly_chart(risk_donut_chart(risk_count), use_container_width=True, config={"displayModeBar": False})
            legend = "<div style='display:flex;flex-direction:column;gap:6px;margin-top:12px;border-top:1px solid #F4F4F5;padding-top:12px;'>"
            for r in ["High Risk", "Medium Risk", "Low Risk"]:
                n = int(risk_count.get(r, 0)); pct = round(n/total*100,1) if total else 0
                legend += f'<div style="display:flex;align-items:center;justify-content:space-between;font-size:12.5px;"><div style="display:flex;align-items:center;gap:6px;"><span style="width:7px;height:7px;border-radius:50%;background:{RISK_COLORS[r]};display:inline-block;"></span><span style="font-weight:550;color:#0F172A;">{r}</span></div><span style="color:#71717A;">{n} scans ({pct}%)</span></div>'
            legend += "</div>"
            st.markdown(legend, unsafe_allow_html=True)
    with right:
        with st.container(border=True):
            st.markdown('<p class="section-title"><i class="bi bi-graph-up"></i> Threat Velocity</p><p class="section-subtitle">Real-time threat percentage profile of historical scans</p>', unsafe_allow_html=True)
            st.plotly_chart(fraud_score_chart(df), use_container_width=True, config={"displayModeBar": False})

    with st.container(border=True):
        st.markdown('<p class="section-title"><i class="bi bi-clock-history"></i> Recent Scans Activity</p><p class="section-subtitle">Latest analyzed job postings</p>', unsafe_allow_html=True)
        st.markdown('<div class="scan-feed">', unsafe_allow_html=True)
        for _, row in df.tail(5).iloc[::-1].iterrows():
            bc = "badge-low" if row["risk"] == "Low Risk" else ("badge-medium" if row["risk"] == "Medium Risk" else "badge-high")
            ts = str(row['title']) if str(row['title']).strip() else '(untitled)'
            st.markdown(f"""<div class="scan-item">
                <div class="scan-avatar">{ts[0].upper()}</div>
                <div class="scan-details">
                    <div class="scan-title">{ts[:60]}</div>
                    <div class="scan-meta"><span>Score: {row['score']}%</span><span class="scan-meta-bullet">•</span><span>{time_ago(row['timestamp'])}</span></div>
                </div>
                <span class="security-badge {bc}">{row['risk']}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------------------
# HELPER: render the result panel (shared by both scan modes)
# ------------------------------------------------------------------
def _render_result_panel(score_raw, risk, badge_class, score_class, recommendation_title,
                          recommendation_text, flags_source, rule_flags):
    """Render score ring, recommendation, risk flags. flags_source = 'structured' or 'message'."""

    # Score ring
    st.markdown(f"""
    <div class="security-indicator">
        <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#71717A;margin-bottom:10px;">
            FRAUD SCORE
        </div>
        <div class="security-score-circle {score_class}">
            <div>
                <span class="security-score-val">{int(score_raw)}</span>
                <span class="security-score-pct">%</span>
            </div>
        </div>
        <div style="margin-bottom:12px;">
            <span class="security-badge {badge_class}">{risk}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # Recommendation
    reco_icon = "bi-shield-slash" if risk == "High Risk" else ("bi-shield-exclamation" if risk == "Medium Risk" else "bi-shield-check")
    st.markdown(f"""
    <div class="recommendation-box">
        <div class="reco-icon-wrap"><i class="bi {reco_icon}"></i></div>
        <div class="reco-content">
            <span class="reco-title">{recommendation_title}</span>
            <span class="reco-text">{recommendation_text}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # Risk flags
    st.markdown('<p style="font-weight:600;margin-top:20px;margin-bottom:8px;color:#0F172A;font-size:13px;">'
                '<i class="bi bi-exclamation-triangle" style="color:#F59E0B;margin-right:4px;"></i>'
                'Detected Risk Factors</p>', unsafe_allow_html=True)

    if rule_flags:
        html = ""
        for icon, msg, is_crit in rule_flags:
            cls = "factor-pill factor-critical" if is_crit else "factor-pill"
            html += f'<span class="{cls}"><i class="bi {icon}"></i> {msg}</span>'
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.markdown('<span class="factor-pill" style="background:#ECFDF5;border-color:#A7F3D0;color:#047857;">'
                    '<i class="bi bi-check-circle"></i> No risk factors detected</span>', unsafe_allow_html=True)


def page_scan():
    render_hero("Threat Scanner Sandbox",
                "Execute NLP semantic scans and structural heuristic checks against arbitrary job postings.")

    # ── Input Mode Selector — uses segmented_control (no columns, no CSS conflict) ──
    if "scan_mode" not in st.session_state:
        st.session_state.scan_mode = "Structured Form"

    st.markdown('<p style="font-size:13px;font-weight:600;color:#0F172A;margin-bottom:6px;">Input Method</p>', unsafe_allow_html=True)

    selected = st.segmented_control(
        "Input Method",
        options=["📋  Structured Form", "📨  Paste Complete Job Message"],
        default="📋  Structured Form",
        key="scan_seg_ctrl",
        label_visibility="collapsed",
    )
    input_mode = "Paste Complete Job Message" if selected and "Paste" in selected else "Structured Form"
    st.session_state.scan_mode = input_mode

    st.markdown("<hr style='margin:12px 0 18px 0; border-color:#F4F4F5;'>", unsafe_allow_html=True)

    # ================================================================
    # MODE 1 — STRUCTURED FORM  (original, completely unchanged)
    # ================================================================
    if input_mode == "Structured Form":

        form_col, result_col = st.columns([1.2, 1])

        with form_col:
            with st.container(border=True):
                st.markdown('<p class="section-title"><i class="bi bi-briefcase"></i> Job Specifications</p>'
                            '<p class="section-subtitle">Specify role headers and compensation details</p>',
                            unsafe_allow_html=True)
                title = st.text_input("Job Title *", placeholder="e.g. Senior Product Designer", key="sf_title")
                c1, c2 = st.columns(2)
                with c1:
                    salary = st.text_input("Salary Range", placeholder="e.g. 90000 - 130000", key="sf_salary")
                with c2:
                    st.markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)
                    remote = st.checkbox("This is a remote position", key="sf_remote")

            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

            with st.container(border=True):
                st.markdown('<p class="section-title"><i class="bi bi-building"></i> Company Profile</p>'
                            '<p class="section-subtitle">Information detailing the employer</p>',
                            unsafe_allow_html=True)
                company = st.text_input("Company Name", placeholder="e.g. Stripe Inc", key="sf_company")
                company_profile = st.text_area("Company Summary",
                    placeholder="Brief summary of the company...", height=80, key="sf_profile")

            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

            with st.container(border=True):
                st.markdown('<p class="section-title"><i class="bi bi-file-earmark-text"></i> Listing Copy</p>'
                            '<p class="section-subtitle">Paste the full description body and requirements</p>',
                            unsafe_allow_html=True)
                description = st.text_area("Job Description *",
                    placeholder="Paste the job description body here...", height=140, key="sf_desc")
                requirements = st.text_input("Role Requirements",
                    placeholder="e.g. React, Figma, SaaS layout", key="sf_req")

            st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
            sf_clicked = st.button("✨ Execute AI Scan", type="primary", use_container_width=True, key="sf_btn")

        with result_col:
            with st.container(border=True):
                st.markdown('<p class="section-title"><i class="bi bi-clipboard-data"></i> AI Analysis Console</p>'
                            '<p class="section-subtitle">Threat score telemetry and warning flags</p>',
                            unsafe_allow_html=True)

                if not sf_clicked:
                    st.markdown("""<div class="analysis-placeholder">
                        <div class="ph-icon"><i class="bi bi-shield-lock"></i></div>
                        Fill in the listing fields on the left and click <b>Execute AI Scan</b>.
                    </div>""", unsafe_allow_html=True)

                elif not title.strip() and not description.strip():
                    st.warning("⚠️ Please fill in at least a Job Title or Job Description to run the scan.")

                else:
                    # ── Original backend prediction (UNCHANGED) ──
                    result, probability = predict_job(title, company, description, requirements, salary)
                    score = round(probability * 100, 2)

                    if score >= 60:
                        risk, badge_class, score_class = "High Risk", "badge-high", "score-high"
                        rec_title = "Threat Notice: High Scam Probability"
                        rec_text = "Severe listing anomalies detected. <b>We strongly advise against applying or sharing identity details.</b>"
                    elif score >= 30:
                        risk, badge_class, score_class = "Medium Risk", "badge-medium", "score-medium"
                        rec_title = "Precautionary Notice: Mild Anomalies"
                        rec_text = "Minor suspicious signals flagged. Verify recruitment authenticity through the company's verified domain."
                    else:
                        risk, badge_class, score_class = "Low Risk", "badge-low", "score-low"
                        rec_title = "Analysis Cleared: Low Risk"
                        rec_text = "No severe anomalies identified. Standard application protocols apply."

                    # Original rule flags
                    flags = get_risk_flags(title, description, salary, company_profile, remote)
                    rule_flags = [(FLAG_ICON_MAP.get(f, "bi-exclamation-circle"), f, "payment" in f.lower()) for f in flags]

                    _render_result_panel(score, risk, badge_class, score_class, rec_title, rec_text, "structured", rule_flags)

                    # Save — use the actual job title (no raw_message)
                    log_title = title.strip() if title.strip() else description.strip()[:50]
                    save_prediction(log_title, risk, score)


    # ================================================================
    # MODE 2 — PASTE COMPLETE JOB MESSAGE  (new single-textbox)
    # ================================================================
    else:
        st.markdown("""
        <div class="scan-source-chips">
            <span class="source-chip"><i class="bi bi-whatsapp"></i> WhatsApp</span>
            <span class="source-chip"><i class="bi bi-linkedin"></i> LinkedIn</span>
            <span class="source-chip"><i class="bi bi-telegram"></i> Telegram</span>
            <span class="source-chip"><i class="bi bi-envelope"></i> Email</span>
            <span class="source-chip"><i class="bi bi-briefcase"></i> Job Ad</span>
            <span class="source-chip"><i class="bi bi-mortarboard"></i> Internship</span>
        </div>""", unsafe_allow_html=True)

        form_col, result_col = st.columns([1.15, 1])

        with form_col:
            with st.container(border=True):
                st.markdown('<p class="section-title"><i class="bi bi-chat-left-text"></i> Paste Job Advertisement</p>'
                            '<p class="section-subtitle">Paste any job message exactly as received — no editing required</p>',
                            unsafe_allow_html=True)

                message = st.text_area(
                    "Job Message",
                    placeholder=(
                        "Paste the complete message here...\n\n"
                        "Example:\n"
                        "Internship Program 2026\n\n"
                        "We have partnered with IBM, Microsoft & IIT Kharagpur...\n\n"
                        "Join WhatsApp: https://chat.whatsapp.com/...\n\n"
                        "Limited Seats | Live Projects | Certificate"
                    ),
                    height=310,
                    label_visibility="collapsed",
                    key="msg_text",
                )
                wc = len(message.split()) if message.strip() else 0
                st.markdown(f'<div style="text-align:right;font-size:11px;color:#A1A1AA;margin-top:-8px;margin-bottom:4px;">'
                            f'{wc} words · {len(message)} characters</div>', unsafe_allow_html=True)

            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            msg_clicked = st.button("🔍 Analyze Message", type="primary", use_container_width=True, key="msg_btn")

            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown("""<p class="section-title"><i class="bi bi-lightbulb"></i> Quick Tips</p>
                <ul style="font-size:12.5px;color:#52525B;line-height:1.8;margin:0;padding-left:16px;">
                    <li>Paste the <b>complete</b> message as received — do not edit</li>
                    <li>Include all links, contact details, company names</li>
                    <li>Longer messages give more accurate results</li>
                    <li>Works with WhatsApp, Telegram, Email, LinkedIn posts</li>
                </ul>""", unsafe_allow_html=True)

        with result_col:
            with st.container(border=True):
                st.markdown('<p class="section-title"><i class="bi bi-clipboard-data"></i> Analysis Results</p>'
                            '<p class="section-subtitle">Fraud score, risk factors, and extracted information</p>',
                            unsafe_allow_html=True)

                if not msg_clicked:
                    st.markdown("""<div class="analysis-placeholder">
                        <div class="ph-icon"><i class="bi bi-shield-lock"></i></div>
                        <div style="font-weight:600;color:#52525B;margin-bottom:6px;">Ready to Analyze</div>
                        Paste a job message on the left and click<br><b>🔍 Analyze Message</b>.
                    </div>""", unsafe_allow_html=True)

                elif not message.strip():
                    st.warning("⚠️ Please paste a job message before analyzing.")

                else:
                    # ── ML Prediction ──
                    cleaned = clean_text(message)
                    vector = vectorizer.transform([cleaned])
                    probability = classifier.predict_proba(vector)[0][1]
                    score = round(probability * 100, 2)

                    # ── Risk level ──
                    if score >= 60:
                        risk, badge_class, score_class = "High Risk", "badge-high", "score-high"
                        rec_title = "⚠️ High Fraud Probability Detected"
                        rec_text = "Multiple severe anomalies found. <b>Avoid applying or sharing personal details until company legitimacy is independently verified.</b>"
                    elif score >= 30:
                        risk, badge_class, score_class = "Medium Risk", "badge-medium", "score-medium"
                        rec_title = "🔶 Suspicious Signals Detected"
                        rec_text = "Some suspicious patterns found. Verify the company through official channels. Do not pay any fees."
                    else:
                        risk, badge_class, score_class = "Low Risk", "badge-low", "score-low"
                        rec_title = "✅ Appears Relatively Safe"
                        rec_text = "No severe anomalies identified by the ML model. Still apply standard job-search caution."

                    # ── Enhanced rule engine ──
                    rule_flags = analyze_message_rules(message)
                    critical_count = sum(1 for _, _, crit in rule_flags if crit)
                    boosted = min(score + critical_count * 6, 99.9)
                    if critical_count >= 2:
                        risk, badge_class, score_class = "High Risk", "badge-high", "score-high"
                        rec_title = "⚠️ High Fraud Probability Detected"
                        rec_text = "Multiple severe anomalies found. <b>Avoid applying or sharing personal details until company legitimacy is independently verified.</b>"

                    _render_result_panel(boosted, risk, badge_class, score_class, rec_title, rec_text, "message", rule_flags)

                    # ── Extracted Information ──
                    info = extract_info(message)
                    st.markdown('<p style="font-weight:600;margin-top:20px;margin-bottom:8px;color:#0F172A;font-size:13px;">'
                                '<i class="bi bi-info-circle" style="color:#3B82F6;margin-right:4px;"></i>'
                                'Extracted Information</p>', unsafe_allow_html=True)

                    def fmt(val, fallback="Not Found"):
                        if val is None or val == "" or val is False:
                            return f'<span style="color:#A1A1AA;">{fallback}</span>'
                        if val is True:
                            return '<span style="color:#10B981;font-weight:600;">Yes</span>'
                        return f'<span style="color:#0F172A;">{val}</span>'

                    rows = [
                        ("Company",       fmt(info.get("company"),     "Not Identified")),
                        ("Job Title",     fmt(info.get("title"),       "Not Identified")),
                        ("Salary",        fmt(info.get("salary"),      "Not Mentioned")),
                        ("Email",         fmt(info.get("email"))),
                        ("Phone",         fmt(info.get("phone"))),
                        ("Website",       fmt(info.get("website"))),
                        ("Contact",       fmt(info.get("contact"),     "Not Specified")),
                        ("Remote / WFH",  fmt(info.get("remote"))),
                        ("Certificate",   fmt(info.get("certificate"))),
                    ]
                    tbl = "".join(f"<tr><td>{lbl}</td><td>{val}</td></tr>" for lbl, val in rows)
                    st.markdown(f'<table class="info-table">{tbl}</table>', unsafe_allow_html=True)

                    # ── Save to history ──
                    # Title = first 50 chars of pasted message; full message saved in raw_message
                    log_title = message.strip()[:50].replace("\n", " ")
                    save_prediction(log_title, risk, int(boosted), raw_message=message.strip())


def page_history(df):
    render_hero("Scanned Logs Registry",
                "Audit log history and security classifications of previously inspected job messages.")
    with st.container(border=True):
        if df.empty:
            st.info("No logs found in this workspace.")
        else:
            st.markdown('<p class="section-title"><i class="bi bi-search"></i> Query Registry</p>'
                        '<p class="section-subtitle">Filter registry logs by keywords or risk level</p>',
                        unsafe_allow_html=True)
            c1, c2, c3 = st.columns([2.5, 1.5, 1])
            with c1:
                search = st.text_input("Search", placeholder="🔍 Search by title or message...", label_visibility="collapsed")
            with c2:
                rf = st.selectbox("Risk Filter", ["All Scan Alerts", "High Risk", "Medium Risk", "Low Risk"], label_visibility="collapsed")
            with c3:
                st.download_button("⬇️ Export CSV", data=df.to_csv(index=False),
                                   file_name="jobshield_audit_logs.csv", mime="text/csv", use_container_width=True)
            filtered = df
            if search:
                filtered = filtered[filtered["title"].astype(str).str.contains(search, case=False, na=False)]
            if rf != "All Scan Alerts":
                filtered = filtered[filtered["risk"] == rf]
            st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
            # Show display columns only (exclude raw_message from table view)
            display_cols = [c for c in ["timestamp", "title", "risk", "score"] if c in filtered.columns]
            st.dataframe(filtered[display_cols].sort_values("timestamp", ascending=False),
                         use_container_width=True, hide_index=True)


def page_analytics(df):
    render_hero("Threat Analytics & Telemetry", "Aggregated scan frequencies, risk categories, and score metrics.")
    if df.empty:
        with st.container(border=True): st.info("No logs found. Run a few scans to populate telemetry.")
        return

    valid = df.dropna(subset=["timestamp"]).copy()
    valid["date"] = valid["timestamp"].dt.date

    c1,c2,c3,c4 = st.columns(4)
    with c1: metric_card("bi-clipboard-data","blue","Total Audited",len(df))
    with c2: metric_card("bi-percent","orange","Avg Threat Score",f"{round(df['score'].mean(),1)}%")
    with c3: metric_card("bi-graph-up-arrow","red","Peak Threat Score",f"{round(df['score'].max(),1)}%")
    with c4: metric_card("bi-graph-down-arrow","green","Min Threat Score",f"{round(df['score'].min(),1)}%")

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown('<p class="section-title"><i class="bi bi-calendar3"></i> Scan Frequency</p>'
                        '<p class="section-subtitle">Total scans per day</p>', unsafe_allow_html=True)
            daily = valid.groupby("date").size()
            fig = go.Figure(go.Bar(x=[str(d) for d in daily.index], y=daily.values, marker_color="#0F172A", marker_line_width=0))
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              margin=dict(l=10,r=10,t=10,b=10), height=200,
                              xaxis=dict(showgrid=False, linecolor="#E4E4E7"),
                              yaxis=dict(gridcolor="#F4F4F5", linecolor="#E4E4E7"))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with right:
        with st.container(border=True):
            st.markdown('<p class="section-title"><i class="bi bi-bar-chart-steps"></i> Mean Score by Risk Level</p>'
                        '<p class="section-subtitle">Average threat % per alert level</p>', unsafe_allow_html=True)
            avg = df.groupby("risk")["score"].mean().reindex(["Low Risk","Medium Risk","High Risk"]).dropna()
            fig = go.Figure(go.Bar(x=avg.index, y=avg.values,
                                   marker_color=[RISK_COLORS.get(r,"#71717A") for r in avg.index],
                                   text=[f"{v:.1f}%" for v in avg.values], textposition="outside"))
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              margin=dict(l=10,r=10,t=10,b=10), height=200,
                              xaxis=dict(showgrid=False,linecolor="#E4E4E7"),
                              yaxis=dict(gridcolor="#F4F4F5",range=[0,115],linecolor="#E4E4E7"), showlegend=False)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def page_risk_factors():
    render_hero("Heuristics Standards", "All vectors checked on job messages to identify common recruitment scam signals.")
    with st.container(border=True):
        st.markdown('<p class="section-title">Heuristic Alert Criteria</p>'
                    '<p class="section-subtitle" style="margin-bottom:0;">Inspected messages undergo validation with both our NLP model and specific rule-based heuristics.</p>',
                    unsafe_allow_html=True)
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    cards = [
        ("bi-whatsapp","WhatsApp / Telegram Links","Legitimate job postings never direct applicants to WhatsApp groups or Telegram channels as a primary contact method."),
        ("bi-credit-card","Payment Requests","Demands for registration fees, processing fees, or security deposits. Authentic recruiters never charge applicants."),
        ("bi-alarm","Urgency & Pressure Tactics","Keywords like 'Limited Seats', 'Apply Immediately' designed to prompt hasty decisions that bypass normal verification."),
        ("bi-currency-rupee","Unrealistic Salary Promises","Claims like 'Earn ₹50,000/week' or '100% placement guaranteed'. Real jobs do not promise guaranteed income."),
        ("bi-building-exclamation","Famous Brand Impersonation","Fraudulent ads mention IBM, Microsoft, IIT to appear legitimate. These mentions are often false claims."),
        ("bi-link-45deg","URL Shorteners","Use of bit.ly, tinyurl hides destination addresses. Legitimate companies use verifiable domain links."),
        ("bi-envelope-exclamation","Personal Email Addresses","Using Gmail/Yahoo instead of a company domain (hr@company.com) strongly suggests a fraudulent listing."),
        ("bi-award","Certificate Bait","Offering certificates is common in fake internship ads, often combined with hidden registration fees."),
        ("bi-cash-stack","Missing Compensation Details","Omission of any salary or stipend. Scammers hide exploitative or zero-pay offers by keeping compensation undisclosed."),
    ]
    cols = st.columns(3)
    for i, (icon, name, desc) in enumerate(cards):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f'<div class="about-card-icon" style="background:#EFF6FF;border-color:#DBEAFE;color:#2563EB;"><i class="bi {icon}"></i></div>'
                            f'<h4 style="font-size:14.5px;font-weight:600;margin-bottom:8px;color:#0F172A;">{name}</h4>'
                            f'<p style="font-size:12.5px;color:#52525B;line-height:1.6;margin:0;">{desc}</p>',
                            unsafe_allow_html=True)
                st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)


def page_reports(df):
    render_hero("Compliance Logs Export", "Download workspace audit records, risk tallies, and threat database compliance files.")
    if df.empty:
        with st.container(border=True): st.info("No audit logs found."); return

    c1,c2,c3,c4 = st.columns(4)
    with c1: metric_card("bi-briefcase","blue","Total Audited",len(df))
    with c2: metric_card("bi-exclamation-triangle","red","Critical Threats",len(df[df["risk"]=="High Risk"]))
    with c3: metric_card("bi-shield-plus","orange","Alert Warnings",len(df[df["risk"]=="Medium Risk"]))
    with c4: metric_card("bi-patch-check","green","Normal Clearance",len(df[df["risk"]=="Low Risk"]))

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<p class="section-title"><i class="bi bi-download"></i> Download Audit Database</p>'
                    '<p class="section-subtitle">Export full compliance logs in CSV format</p>', unsafe_allow_html=True)
        st.download_button("⬇ Export Audit Log Database (CSV)", data=df.to_csv(index=False),
                           file_name="jobshield_compliance_audit_logs.csv", mime="text/csv", use_container_width=True)
        st.markdown("<div style='height:18px;border-top:1px solid #F4F4F5;margin-top:18px;'></div>", unsafe_allow_html=True)
        display_cols = [c for c in ["timestamp", "title", "risk", "score"] if c in df.columns]
        st.dataframe(df[display_cols].sort_values("timestamp", ascending=False), use_container_width=True, hide_index=True)


def page_settings():
    render_hero("Console Preferences", "Configure custom threat parameters, score alerts, and audit preferences.")
    with st.container(border=True):
        st.markdown('<p class="section-title"><i class="bi bi-sliders"></i> Security Thresholds</p>'
                    '<p class="section-subtitle">Adjust risk threshold defaults</p>', unsafe_allow_html=True)
        st.slider("High Risk Score Threshold", 50, 90, 60)
        st.slider("Medium Risk Score Threshold", 20, 50, 30)
        st.markdown("<div style='height:18px;border-top:1px solid #F4F4F5;margin-top:18px;'></div>", unsafe_allow_html=True)
        st.markdown('<p class="section-title"><i class="bi bi-database-gear"></i> Log Retention</p>'
                    '<p class="section-subtitle">Configure retention period for CSV database scans</p>', unsafe_allow_html=True)
        st.selectbox("History Log Retention Limit", ["Keep indefinitely","Last 100 scans","Last 30 days","Clear on session exit"])
        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        st.button("Save Preferences Settings")


def page_about():
    render_hero("Platform Overview", "Technical documentation and architecture details of the JobShield AI Threat Engine.")
    st.markdown("""
    <div class="about-hero">
        <h2>Shielding the Future of Work</h2>
        <p>JobShield AI is a commercial-grade threat detection engine designed to inspect, identify, and report suspicious employment listings before they compromise candidate safety.</p>
    </div>
    <div class="grid-3col">
        <div class="about-card"><div class="about-card-icon"><i class="bi bi-cpu"></i></div><h3>ML Classifier</h3><p>Logistic Regression + TF-IDF feature mapping trained on verified employment fraud datasets.</p></div>
        <div class="about-card"><div class="about-card-icon"><i class="bi bi-shield-lock"></i></div><h3>Heuristic Engine</h3><p>Rules check WhatsApp links, payment requests, urgency language, brand impersonation, and more.</p></div>
        <div class="about-card"><div class="about-card-icon"><i class="bi bi-activity"></i></div><h3>Audit Console</h3><p>Centralized logging with full scan compliance registry, timeline metrics, and CSV exporting.</p></div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown('<p class="section-title"><i class="bi bi-rocket-takeoff"></i> Our Mission</p>'
                        '<p style="color:#52525B;font-size:13.5px;line-height:1.7;margin:0;">Employment fraud has risen significantly with remote work adoption. JobShield AI was built to put threat detection directly into the hands of job seekers and recruitment teams.</p>',
                        unsafe_allow_html=True)
    with c2:
        with st.container(border=True):
            st.markdown('<p class="section-title"><i class="bi bi-layers"></i> Threat Tech Stack</p>'
                        '<p style="color:#52525B;font-size:13.5px;line-height:1.8;margin:0;">'
                        '• <b>Language</b>: Python 3.10+<br>• <b>Interface</b>: Streamlit<br>'
                        '• <b>Modeling</b>: Scikit-learn Logistic Regression<br>'
                        '• <b>NLP</b>: TF-IDF Text Vectorization<br>'
                        '• <b>Visuals</b>: Plotly + Vanilla CSS</p>', unsafe_allow_html=True)

    st.markdown('<div style="height:24px;"></div><div class="about-footer">JobShield AI Security Suite • Version 3.0.0</div>', unsafe_allow_html=True)


# =====================================================================
# ============================  ROUTER  ===============================
# =====================================================================

menu = render_sidebar()
history_df = load_history()
render_top_bar(menu, history_df)

if menu == "Dashboard":       page_dashboard(history_df)
elif menu == "Scan New Job":  page_scan()
elif menu == "History":       page_history(history_df)
elif menu == "Analytics":     page_analytics(history_df)
elif menu == "Risk Factors":  page_risk_factors()
elif menu == "Reports":       page_reports(history_df)
elif menu == "Settings":      page_settings()
elif menu == "About":         page_about()