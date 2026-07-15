# ================= app.py =================
# JobShield AI — Fake Job Posting Detector
# Frontend redesigned to a premium SaaS dashboard style.
# ML / auth / risk-rule logic is untouched — see "BACKEND" section below.

from streamlit_option_menu import option_menu
from auth import login
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
import os
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

# Initialize Session States
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "menu_selection" not in st.session_state:
    st.session_state.menu_selection = "Dashboard"

if not st.session_state.logged_in:
    login()
    st.stop()


# =====================================================================
# ===========================  GLOBAL CSS  ===========================
# =====================================================================
# Modern visual tokens and layouts matching Vercel/Stripe/Linear aesthetics.

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background-color: #FFFFFF !important;
}

#MainMenu, footer, header[data-testid="stHeader"] {
    visibility: hidden !important;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 4rem !important;
    max-width: 1200px !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #0F172A !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em !important;
}

hr {
    border-color: #F4F4F5 !important;
}

/* ---------------- COMPACT SIDEBAR ---------------- */
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

/* Workspace Selector */
.workspace-selector {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    border-radius: 6px;
    background: #F4F4F5;
    border: 1px solid #E4E4E7;
    margin-bottom: 16px;
    cursor: pointer;
    transition: all 0.15s ease;
}
.workspace-selector:hover {
    background: #E4E4E7;
    border-color: #D4D4D8;
}
.workspace-avatar {
    width: 28px;
    height: 28px;
    border-radius: 5px;
    background: #0F172A;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 12px;
}
.workspace-info {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    gap: 1px;
}
.workspace-name {
    font-size: 13px;
    font-weight: 600;
    color: #0F172A;
    line-height: 1.2;
    letter-spacing: -0.01em;
}
.workspace-plan {
    font-size: 10px;
    color: #71717A;
    font-weight: 500;
    line-height: 1;
}
.workspace-chevron {
    color: #71717A;
    font-size: 12px;
}

/* Sidebar Search */
.sidebar-search {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 10px;
    border-radius: 6px;
    border: 1px solid #E4E4E7;
    background: #FFFFFF;
    color: #A1A1AA;
    font-size: 12.5px;
    margin-bottom: 16px;
    cursor: pointer;
}
.sidebar-search span {
    flex-grow: 1;
    font-weight: 400;
}
.sidebar-search kbd {
    background: #F4F4F5;
    border: 1px solid #E4E4E7;
    border-radius: 4px;
    padding: 1px 4px;
    font-size: 9.5px;
    font-family: monospace;
    color: #71717A;
}

/* Sidebar footer note */
.sidebar-note {
    background: #FAFAFA;
    border: 1px solid #E4E4E7;
    border-radius: 6px;
    padding: 10px 12px;
    margin-top: 20px;
}
.sidebar-note p {
    margin: 0;
    font-size: 11.5px;
    color: #71717A;
    line-height: 1.45;
    font-weight: 450;
}

/* Option Menu Item Selected Left Line */
.nav-link-selected {
    border-left: 2.5px solid #0F172A !important;
    border-radius: 0px 6px 6px 0px !important;
}

/* ---------------- TOP BAR ---------------- */
.top-bar-wrap {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 14px;
    margin-bottom: 18px;
    border-bottom: 1px solid #F4F4F5;
}
.breadcrumbs {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    font-weight: 500;
}
.bc-parent {
    color: #71717A;
}
.bc-separator {
    color: #D4D4D8;
}
.bc-active {
    color: #0F172A;
    font-weight: 600;
}

.icon-btn {
    width: 34px;
    height: 34px;
    border-radius: 6px;
    background: #FFFFFF;
    border: 1px solid #E4E4E7;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    color: #52525B;
    font-size: 15px;
    cursor: pointer;
    transition: all 0.15s ease;
}
.icon-btn:hover {
    background: #F4F4F5;
    border-color: #D4D4D8;
    color: #0F172A;
}
.notif-badge {
    position: absolute;
    top: -4px;
    right: -4px;
    background: #EF4444;
    color: white;
    font-size: 8.5px;
    font-weight: 700;
    min-width: 14px;
    height: 14px;
    border-radius: 999px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 3px;
    border: 2px solid white;
}

.user-chip {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 3px 10px 3px 3px;
    border-radius: 999px;
    background: #F4F4F5;
    border: 1px solid #E4E4E7;
}
.user-chip .avatar {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    background: #0F172A;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 700;
}
.user-chip .u-info {
    display: flex;
    flex-direction: column;
    gap: 0px;
}
.user-chip .u-name {
    font-size: 11px;
    font-weight: 600;
    color: #0F172A;
    line-height: 1.1;
}
.user-chip .u-role {
    font-size: 9.5px;
    color: #71717A;
    line-height: 1.1;
}

/* ---------------- HERO LANDING (DASHBOARD) ---------------- */
.dashboard-hero {
    padding: 32px 0 24px 0;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    background: #EFF6FF;
    color: #1D4ED8;
    border: 1px solid #DBEAFE;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.05em;
    margin-bottom: 16px;
}
.hero-title {
    font-size: 36px !important;
    font-weight: 850 !important;
    color: #0F172A !important;
    letter-spacing: -0.035em !important;
    line-height: 1.15 !important;
    margin-bottom: 14px !important;
    max-width: 720px;
}
.hero-desc {
    font-size: 15.5px;
    color: #52525B;
    line-height: 1.6;
    max-width: 680px;
    margin-bottom: 24px;
    font-weight: 400;
}
.trust-indicator-row {
    display: flex;
    gap: 24px;
    margin-top: 28px;
    padding-top: 24px;
    border-top: 1px solid #F4F4F5;
}
.trust-item {
    font-size: 12px;
    color: #71717A;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 6px;
}
.trust-item i {
    color: #A1A1AA;
    font-size: 13.5px;
}

/* ---------------- PAGE HEADER (GENERIC) ---------------- */
.page-header {
    margin-bottom: 24px;
    padding-bottom: 10px;
}
.page-header h1 {
    font-size: 24px;
    font-weight: 750;
    color: #0F172A;
    margin: 0 0 6px 0;
    letter-spacing: -0.025em;
}
.page-header p {
    font-size: 14px;
    color: #52525B;
    margin: 0;
    font-weight: 400;
    line-height: 1.5;
}

/* ---------------- CONTAINERS (CARDS) ---------------- */
.main div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF !important;
    border: 1px solid #E4E4E7 !important;
    border-radius: 8px !important;
    padding: 20px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    transition: all 0.15s ease-in-out !important;
}
.main div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #D4D4D8 !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04) !important;
}

.section-title {
    font-size: 14.5px;
    font-weight: 600;
    color: #0F172A;
    margin: 0 0 4px 0;
    display: flex;
    align-items: center;
    gap: 8px;
    letter-spacing: -0.01em;
}
.section-subtitle {
    font-size: 12px;
    color: #71717A;
    margin: 0 0 16px 0;
}

/* ---------------- INPUTS OVERRIDES ---------------- */
.stTextInput input,
.stTextArea textarea,
.stSelectbox > div > div {
    border-radius: 6px !important;
    border: 1px solid #E4E4E7 !important;
    background: #FFFFFF !important;
    font-size: 13.5px !important;
    color: #0F172A !important;
    transition: all 0.15s ease !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus,
.stSelectbox > div > div:focus-within {
    border-color: #0F172A !important;
    box-shadow: 0 0 0 2px rgba(15, 23, 42, 0.05) !important;
}
label, .stCheckbox label p {
    font-weight: 500 !important;
    color: #27272A !important;
    font-size: 12.5px !important;
    margin-bottom: 4px !important;
}

/* ---------------- BUTTONS OVERRIDES ---------------- */
div.stButton > button {
    border-radius: 6px !important;
    height: 38px !important;
    font-weight: 550 !important;
    font-size: 13.5px !important;
    letter-spacing: -0.01em !important;
    transition: all 0.15s ease !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
}
div.stButton > button:active {
    transform: translateY(0px) !important;
}

/* Primary buttons (Vercel dark slate style) */
div[data-testid="stBaseButton-primary"] {
    background-color: #0F172A !important;
    color: #FFFFFF !important;
    border: 1px solid #0F172A !important;
}
div[data-testid="stBaseButton-primary"]:hover {
    background-color: #1E293B !important;
    border-color: #1E293B !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08) !important;
}

/* Secondary buttons (Vercel outline style) */
div[data-testid="stBaseButton-secondary"] {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #E4E4E7 !important;
}
div[data-testid="stBaseButton-secondary"]:hover {
    background-color: #F4F4F5 !important;
    border-color: #D4D4D8 !important;
}

div[data-testid="stDownloadButton"] > button {
    background: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #E4E4E7 !important;
    border-radius: 6px !important;
    height: 38px !important;
    font-weight: 550 !important;
    font-size: 13.5px !important;
    transition: all 0.15s ease !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: #F4F4F5 !important;
    border-color: #D4D4D8 !important;
}

/* ---------------- STRIPE-STYLE METRICS ---------------- */
.metric-card {
    background: #FFFFFF;
    border: 1px solid #E4E4E7;
    border-radius: 8px;
    padding: 18px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    transition: all 0.15s ease-in-out;
    min-height: 110px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.metric-card:hover {
    border-color: #D4D4D8;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}
.metric-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
}
.metric-title {
    font-size: 11.5px;
    font-weight: 600;
    color: #71717A;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.metric-icon-wrap {
    width: 26px;
    height: 26px;
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
}
.metric-icon-blue   { background: #EFF6FF; color: #3B82F6; }
.metric-icon-red    { background: #FEF2F2; color: #EF4444; }
.metric-icon-orange { background: #FFF7ED; color: #F59E0B; }
.metric-icon-green  { background: #ECFDF5; color: #10B981; }

.metric-value {
    font-size: 24px;
    font-weight: 700;
    color: #0F172A;
    letter-spacing: -0.025em;
    line-height: 1.1;
    margin: 2px 0;
}
.metric-footer {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11.5px;
    font-weight: 500;
    margin-top: 4px;
}
.trend-up {
    color: #15803D;
    background: #DCFCE7;
    padding: 1px 5px;
    border-radius: 4px;
    display: inline-flex;
    align-items: center;
    gap: 3px;
}
.trend-down {
    color: #B91C1C;
    background: #FEE2E2;
    padding: 1px 5px;
    border-radius: 4px;
    display: inline-flex;
    align-items: center;
    gap: 3px;
}
.trend-neutral {
    color: #52525B;
    background: #F4F4F5;
    padding: 1px 5px;
    border-radius: 4px;
    display: inline-flex;
    align-items: center;
    gap: 3px;
}
.trend-text {
    color: #71717A;
}

/* ---------------- ACTIVITY STREAM ---------------- */
.scan-feed {
    display: flex;
    flex-direction: column;
}
.scan-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid #F4F4F5;
}
.scan-item:last-child {
    border-bottom: none;
}
.scan-avatar {
    width: 30px;
    height: 30px;
    border-radius: 5px;
    background: #F4F4F5;
    color: #0F172A;
    border: 1px solid #E4E4E7;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 12px;
}
.scan-details {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    gap: 1px;
}
.scan-title {
    font-size: 13px;
    font-weight: 600;
    color: #0F172A;
    letter-spacing: -0.01em;
}
.scan-meta {
    font-size: 11px;
    color: #71717A;
    display: flex;
    align-items: center;
    gap: 6px;
}
.scan-meta-bullet {
    color: #E4E4E7;
}

/* ---------------- RISK BADGES & CHIPS ---------------- */
.security-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 8px;
    border-radius: 9999px;
    font-size: 10.5px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    border: 1px solid transparent;
}
.security-badge.badge-high { background: #FEF2F2; color: #991B1B; border-color: #FEE2E2; }
.security-badge.badge-medium { background: #FFFBEB; color: #92400E; border-color: #FEF3C7; }
.security-badge.badge-low { background: #F0FDF4; color: #166534; border-color: #DCFCE7; }

.factor-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #F4F4F5;
    border: 1px solid #E4E4E7;
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 12px;
    font-weight: 500;
    color: #18181B;
    margin-right: 6px;
    margin-bottom: 6px;
    letter-spacing: -0.01em;
}
.factor-pill i {
    font-size: 12px;
}
.factor-pill.factor-critical {
    background: #FEF2F2;
    border-color: #FEE2E2;
    color: #991B1B;
}

.recommendation-box {
    background: #FAFAFA;
    border: 1px solid #E4E4E7;
    border-radius: 6px;
    padding: 14px 16px;
    margin-top: 14px;
    display: flex;
    gap: 10px;
    align-items: flex-start;
}
.reco-icon-wrap {
    color: #71717A;
    font-size: 15px;
    margin-top: 1px;
}
.reco-content {
    display: flex;
    flex-direction: column;
    gap: 2px;
}
.reco-title {
    font-size: 12.5px;
    font-weight: 600;
    color: #0F172A;
}
.reco-text {
    font-size: 12px;
    color: #52525B;
    line-height: 1.45;
}

/* ---------------- GAUGE / SECURITY RING ---------------- */
.security-indicator {
    text-align: center;
    padding: 10px 0;
}
.security-score-circle {
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: #FFFFFF;
    border: 7px solid #F4F4F5;
    margin-bottom: 12px;
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.02);
}
.security-score-circle.score-high { border-color: #FEE2E2; color: #EF4444; }
.security-score-circle.score-medium { border-color: #FEF3C7; color: #F59E0B; }
.security-score-circle.score-low { border-color: #DCFCE7; color: #10B981; }

.security-score-val {
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -0.03em;
}
.security-score-pct {
    font-size: 13px;
    font-weight: 600;
    color: #71717A;
}

.analysis-placeholder {
    text-align: center;
    padding: 50px 10px;
    color: #A1A1AA;
    font-size: 13px;
}
.analysis-placeholder .ph-icon {
    font-size: 30px;
    margin-bottom: 10px;
    color: #E4E4E7;
}

/* ---------------- DATA TABLE STYLING ---------------- */
div[data-testid="stDataFrame"] {
    border: 1px solid #E4E4E7 !important;
    border-radius: 6px !important;
    overflow: hidden !important;
}

/* ---------------- ABOUT PRODUCT WEBSITE LAYOUT ---------------- */
.about-hero {
    text-align: center;
    padding: 24px 0 32px 0;
    border-bottom: 1px solid #F4F4F5;
    margin-bottom: 24px;
}
.about-hero h2 {
    font-size: 28px;
    font-weight: 850;
    color: #0F172A;
    letter-spacing: -0.03em;
    margin-bottom: 8px;
}
.about-hero p {
    font-size: 15px;
    color: #52525B;
    max-width: 560px;
    margin: 0 auto;
    line-height: 1.55;
}

.grid-3col {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}
.about-card {
    background: #FFFFFF;
    border: 1px solid #E4E4E7;
    border-radius: 6px;
    padding: 20px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.01);
    transition: all 0.15s ease;
}
.about-card:hover {
    border-color: #D4D4D8;
    box-shadow: 0 4px 10px rgba(0,0,0,0.02);
}
.about-card-icon {
    width: 34px;
    height: 34px;
    border-radius: 5px;
    background: #F4F4F5;
    color: #0F172A;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    margin-bottom: 14px;
    border: 1px solid #E4E4E7;
}
.about-card h3 {
    font-size: 14.5px;
    font-weight: 600;
    color: #0F172A;
    margin: 0 0 6px 0;
    letter-spacing: -0.01em;
}
.about-card p {
    font-size: 12.5px;
    color: #52525B;
    line-height: 1.5;
    margin: 0;
}

.about-footer {
    text-align: center;
    padding-top: 20px;
    font-size: 12px;
    color: #71717A;
    border-top: 1px solid #F4F4F5;
}

</style>
"""

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# Bootstrap Icons (used for crisp glyph icons throughout the dashboard)
st.markdown(
    '<link rel="stylesheet" '
    'href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">',
    unsafe_allow_html=True
)


# =====================================================================
# ========================  BACKEND (UNTOUCHED) =======================
# =====================================================================

# ================= LOAD MODEL =================

classifier = joblib.load(
    "model/classifier.pkl"
)

vectorizer = joblib.load(
    "model/vectorizer.pkl"
)

# ================= CONSTANT =================

LOG_FILE = "checked_postings.csv"


# ================= SAVE HISTORY =================

def save_prediction(title, risk, score):
    new_data = pd.DataFrame({
        "timestamp": [
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        ],
        "title": [title],
        "risk": [risk],
        "score": [score]
    })

    if os.path.exists(LOG_FILE):
        new_data.to_csv(
            LOG_FILE,
            mode="a",
            header=False,
            index=False
        )
    else:
        new_data.to_csv(
            LOG_FILE,
            index=False
        )


# ================= ML PREDICTION =================

def predict_job(
        title,
        company,
        description,
        requirements,
        salary
):
    text = " ".join([
        title,
        company,
        description,
        requirements,
        salary
    ])

    cleaned_text = clean_text(
        text
    )

    vector = vectorizer.transform(
        [cleaned_text]
    )

    probability = classifier.predict_proba(
        vector
    )[0][1]

    prediction = classifier.predict(
        vector
    )[0]

    if prediction == 1:
        result = "Fake Job"
    else:
        result = "Real Job"

    return result, probability

# =====================================================================
# ====================  END OF BACKEND (UNTOUCHED) ====================
# =====================================================================


# =====================================================================
# ========================  FRONTEND HELPERS  =========================
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


def load_history():
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.sort_values("timestamp")
        return df
    return pd.DataFrame(columns=["timestamp", "title", "risk", "score"])


def week_over_week(df, mask=None):
    if df.empty or "timestamp" not in df.columns:
        return "No scans yet", "neutral"

    working = df[mask] if mask is not None else df
    working = working.dropna(subset=["timestamp"])

    now = pd.Timestamp.now()
    last_week_start = now - pd.Timedelta(days=7)
    prev_week_start = now - pd.Timedelta(days=14)

    current = working[working["timestamp"] >= last_week_start]
    previous = working[
        (working["timestamp"] >= prev_week_start)
        & (working["timestamp"] < last_week_start)
    ]

    cur_n, prev_n = len(current), len(previous)

    if prev_n == 0:
        if cur_n == 0:
            return "No data yet", "neutral"
        return f"{cur_n} new scans", "up"

    pct = round(((cur_n - prev_n) / prev_n) * 100, 1)
    if pct > 0:
        return f"↑ {pct}% this week", "up"
    elif pct < 0:
        return f"↓ {abs(pct)}% this week", "down"
    return "No change vs last week", "neutral"


def time_ago(ts):
    if pd.isna(ts):
        return ""
    delta = pd.Timestamp.now() - ts
    seconds = delta.total_seconds()
    if seconds < 60:
        return "just now"
    if seconds < 3600:
        return f"{int(seconds // 60)}m ago"
    if seconds < 86400:
        return f"{int(seconds // 3600)}h ago"
    return f"{int(seconds // 86400)}d ago"


def metric_card(icon_class, color, title, value, trend_label=None, trend_dir="neutral"):
    trend_html = ""
    if trend_label:
        trend_html = f'<div class="trend-{trend_dir}">{trend_label}</div>'
    else:
        trend_html = '<div class="trend-neutral">No change</div>'

    icon_color_map = {
        "blue": "metric-icon-blue",
        "red": "metric-icon-red",
        "orange": "metric-icon-orange",
        "green": "metric-icon-green",
    }
    icon_color_class = icon_color_map.get(color, "metric-icon-blue")

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">
            <span class="metric-title">{title}</span>
            <div class="metric-icon-wrap {icon_color_class}"><i class="bi {icon_class}"></i></div>
        </div>
        <div class="metric-value">{value}</div>
        <div class="metric-footer">
            {trend_html}
            <span class="trend-text">vs prev. period</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_hero(icon_class, title, subtitle, badges=None):
    badges_html = ""
    if badges:
        badges_html = "".join(f'<span class="info-badge">{b}</span>' for b in badges)
        badges_html = f'<div class="info-badge-row">{badges_html}</div>'

    st.markdown(f"""
    <div class="page-header">
        <h1 class="page-title">{title}</h1>
        <p class="page-desc">{subtitle}</p>
        {badges_html}
    </div>
    """, unsafe_allow_html=True)


def render_top_bar(page_label, df):
    high_today = 0
    if not df.empty:
        today = pd.Timestamp.now().normalize()
        recent = df.dropna(subset=["timestamp"])
        high_today = len(recent[
            (recent["timestamp"] >= today) & (recent["risk"] == "High Risk")
        ])

    search_col, bell_col, user_col = st.columns([5, 0.6, 1.6])

    with search_col:
        st.markdown(f"""
        <div class="breadcrumbs" style="margin-top: 6px;">
            <span class="bc-parent">Console</span>
            <span class="bc-separator">/</span>
            <span class="bc-active">{page_label}</span>
        </div>
        """, unsafe_allow_html=True)

    with bell_col:
        badge = f'<span class="notif-badge">{high_today}</span>' if high_today > 0 else ""
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin-top: 2px;">
            <div class="icon-btn"><i class="bi bi-bell"></i>{badge}</div>
        </div>
        """, unsafe_allow_html=True)

    with user_col:
        st.markdown("""
        <div style="display: flex; justify-content: flex-end;">
            <div class="user-chip">
                <div class="avatar">U</div>
                <div class="u-info">
                    <div class="u-name">Admin User</div>
                    <div class="u-role">Threat Auditor</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def risk_donut_chart(risk_count):
    labels = list(risk_count.index)
    values = list(risk_count.values)
    colors = [RISK_COLORS.get(r, "#71717A") for r in labels]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.72,
        marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
        textinfo="none",
        sort=False,
    )])

    fig.update_layout(
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=190,
        annotations=[dict(
            text=f"<b>{sum(values)}</b><br><span style='font-size:9.5px;color:#71717A'>Scans</span>",
            x=0.5, y=0.5, showarrow=False, font=dict(size=16, color="#0F172A")
        )]
    )
    return fig


def fraud_score_chart(df):
    recent = df.dropna(subset=["timestamp"]).tail(20)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=recent["timestamp"],
        y=recent["score"],
        mode="lines+markers",
        line=dict(color="#0F172A", width=2.5, shape="spline"),
        marker=dict(size=4.5, color="#0F172A"),
        fill="tozeroy",
        fillcolor="rgba(15,23,42,0.03)",
    ))

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=190,
        xaxis=dict(showgrid=False, linecolor="#E4E4E7"),
        yaxis=dict(showgrid=True, gridcolor="#F4F4F5", linecolor="#E4E4E7", range=[0, 105]),
    )
    return fig


def render_sidebar():
    with st.sidebar:
        # Notion-style Workspace Picker
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
        </div>
        """, unsafe_allow_html=True)

        menu_options = [
            "Dashboard",
            "Scan New Job",
            "History",
            "Analytics",
            "Risk Factors",
            "Reports",
            "Settings",
            "About"
        ]

        # Programmatically sync sidebar menu selection index
        default_idx = 0
        if st.session_state.menu_selection in menu_options:
            default_idx = menu_options.index(st.session_state.menu_selection)

        selected = option_menu(
            menu_title=None,
            options=menu_options,
            icons=[
                "grid-1x2",
                "search",
                "clock-history",
                "bar-chart-line",
                "shield-exclamation",
                "file-earmark-text",
                "gear",
                "info-circle",
            ],
            default_index=default_idx,
            key="sidebar_option_menu",
            styles={
                "container": {"padding": "0!important", "background-color": "#FFFFFF"},
                "icon": {"color": "#71717A", "font-size": "13.5px"},
                "nav-link": {
                    "font-size": "12.5px",
                    "text-align": "left",
                    "margin": "2px 0",
                    "padding": "7px 10px",
                    "border-radius": "5px",
                    "color": "#52525B",
                    "font-weight": "500",
                    "--hover-color": "#F4F4F5",
                },
                "nav-link-selected": {
                    "background-color": "#F4F4F5",
                    "color": "#0F172A",
                    "font-weight": "600",
                },
            },
        )

        st.markdown("""
        <div class="sidebar-note">
            <p>🤖 Zero-Trust threat classifier protecting recruitment pipelines.</p>
        </div>
        """, unsafe_allow_html=True)

        # Update the session state menu selection
        st.session_state.menu_selection = selected
        return selected


# =====================================================================
# ============================  PAGES  ================================
# =====================================================================

def page_dashboard(df):
    # Modern SaaS Hero landing section
    st.markdown("""
    <div class="dashboard-hero">
        <div class="hero-badge">🟢 HEURISTICS ACTIVE & SECURE</div>
        <h1 class="hero-title">Protect your applications with JobShield AI</h1>
        <p class="hero-desc">An AI-powered threat validation platform designed to detect fee scams and data harvesting posting networks in real time.</p>
    </div>
    """, unsafe_allow_html=True)

    # CTA Buttons (Primary and Secondary side by side)
    cta_col1, cta_col2, _ = st.columns([1.1, 1.2, 3])
    with cta_col1:
        if st.button("✨ Run New Scan", type="primary", use_container_width=True, key="dash_btn_scan"):
            st.session_state.menu_selection = "Scan New Job"
            st.rerun()
    with cta_col2:
        if st.button("📋 View Audit Logs", type="secondary", use_container_width=True, key="dash_btn_logs"):
            st.session_state.menu_selection = "History"
            st.rerun()

    # Trust Indicators Row
    st.markdown("""
    <div class="trust-indicator-row">
        <span class="trust-item"><i class="bi bi-cpu"></i> ML Model Inference Active</span>
        <span class="trust-item"><i class="bi bi-terminal"></i> NLP Text Vectorization</span>
        <span class="trust-item"><i class="bi bi-cloud-check"></i> Real-time CSV Audit Logs</span>
    </div>
    <div style="height: 32px;"></div>
    """, unsafe_allow_html=True)

    if df.empty:
        with st.container(border=True):
            st.info("No scanned data available in this workspace. Run your first threat scan to populate telemetry.")
        return

    total_jobs = len(df)
    high_n = len(df[df["risk"] == "High Risk"])
    medium_n = len(df[df["risk"] == "Medium Risk"])
    low_n = len(df[df["risk"] == "Low Risk"])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        label, direction = week_over_week(df)
        metric_card("bi-briefcase", "blue", "Total Audits", total_jobs, label, direction)
    with c2:
        label, direction = week_over_week(df, df["risk"] == "High Risk")
        metric_card("bi-exclamation-triangle", "red", "High Risk Alerts", high_n, label, direction)
    with c3:
        label, direction = week_over_week(df, df["risk"] == "Medium Risk")
        metric_card("bi-shield-plus", "orange", "Medium Risk Alerts", medium_n, label, direction)
    with c4:
        label, direction = week_over_week(df, df["risk"] == "Low Risk")
        metric_card("bi-patch-check", "green", "Safe Clearances", low_n, label, direction)

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown(
                '<p class="section-title"><i class="bi bi-pie-chart"></i> Risk Distribution</p>'
                '<p class="section-subtitle">Breakdown of scanned postings by alert level</p>',
                unsafe_allow_html=True
            )
            risk_count = df["risk"].value_counts()
            st.plotly_chart(risk_donut_chart(risk_count), use_container_width=True, config={"displayModeBar": False})

            # Custom Legend Layout
            legend = "<div style='display:flex; flex-direction:column; gap:6px; margin-top:12px; border-top:1px solid #F4F4F5; padding-top:12px;'>"
            for r in ["High Risk", "Medium Risk", "Low Risk"]:
                n = int(risk_count.get(r, 0))
                pct = round(n / total_jobs * 100, 1) if total_jobs else 0
                legend += (
                    f'<div style="display:flex;align-items:center;justify-content:space-between;font-size:12.5px;color:#52525B;">'
                    f'<div style="display:flex;align-items:center;gap:6px;">'
                    f'<span style="width:7px;height:7px;border-radius:50%;background:{RISK_COLORS[r]};display:inline-block;"></span>'
                    f'<span style="font-weight:550;color:#0F172A;">{r}</span>'
                    f'</div>'
                    f'<span style="color:#71717A;">{n} scans ({pct}%)</span>'
                    f'</div>'
                )
            legend += "</div>"
            st.markdown(legend, unsafe_allow_html=True)

    with right:
        with st.container(border=True):
            st.markdown(
                '<p class="section-title"><i class="bi bi-graph-up"></i> Threat Velocity</p>'
                '<p class="section-subtitle">Real-time threat percentage profile of historical scans</p>',
                unsafe_allow_html=True
            )
            st.plotly_chart(fraud_score_chart(df), use_container_width=True, config={"displayModeBar": False})

    # Recent Scans Table Activity List
    with st.container(border=True):
        st.markdown(
            '<p class="section-title"><i class="bi bi-clock-history"></i> Recent Scans Activity</p>'
            '<p class="section-subtitle">Real-time log of the latest analyzed job postings</p>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="scan-feed">', unsafe_allow_html=True)
        for _, row in df.tail(5).iloc[::-1].iterrows():
            badge_class = "badge-low" if row["risk"] == "Low Risk" else ("badge-medium" if row["risk"] == "Medium Risk" else "badge-high")
            title_str = row['title'] if str(row['title']).strip() else '(untitled posting)'
            company_initial = title_str[0].upper() if len(title_str) > 0 else 'J'
            time_str = time_ago(row['timestamp'])
            
            st.markdown(f"""
            <div class="scan-item">
                <div class="scan-avatar">{company_initial}</div>
                <div class="scan-details">
                    <div class="scan-title">{title_str}</div>
                    <div class="scan-meta">
                        <span>Threat Score: {row['score']}%</span>
                        <span class="scan-meta-bullet">•</span>
                        <span>{time_str}</span>
                    </div>
                </div>
                <div class="scan-badge-container">
                    <span class="security-badge {badge_class}">{row['risk']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


def page_scan():
    # Page-scoped CSS to stick-float the result column on desktop resolutions
    st.markdown("""
    <style>
    @media (min-width: 992px) {
        div[data-testid="column"]:nth-of-type(2) {
            position: -webkit-sticky !important;
            position: sticky !important;
            top: 24px !important;
            align-self: start !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    render_hero(
        "bi-search",
        "Threat Scanner Sandbox",
        "Execute NLP semantic scans and structural heuristic checks against arbitrary job postings.",
        badges=["🤖 TF-IDF Neural Model", "⚡ Dynamic Alerts", "🛡️ Sandboxed Environment"],
    )

    form_col, result_col = st.columns([1.2, 1])

    with form_col:
        # Panel 1: Job Information
        with st.container(border=True):
            st.markdown(
                '<p class="section-title"><i class="bi bi-briefcase"></i> Job Specifications</p>'
                '<p class="section-subtitle">Specify role headers and compensation details</p>',
                unsafe_allow_html=True
            )
            title = st.text_input("Job Title *", placeholder="e.g. Senior Product Designer")
            
            c1, c2 = st.columns(2)
            with c1:
                salary = st.text_input("Salary Range", placeholder="e.g. 90000 - 130000")
            with c2:
                st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
                remote = st.checkbox("This is a remote position")

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        # Panel 2: Company Information
        with st.container(border=True):
            st.markdown(
                '<p class="section-title"><i class="bi bi-building"></i> Company Profile</p>'
                '<p class="section-subtitle">Information detailing the employer</p>',
                unsafe_allow_html=True
            )
            company = st.text_input("Company Name", placeholder="e.g. Stripe Inc")
            company_profile = st.text_area(
                "Company Summary", placeholder="Brief summary of the company (sector, industry, founding etc)...", height=80
            )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        # Panel 3: Details & Requirements
        with st.container(border=True):
            st.markdown(
                '<p class="section-title"><i class="bi bi-file-earmark-text"></i> Listing Copy</p>'
                '<p class="section-subtitle">Paste the full description body and requirements</p>',
                unsafe_allow_html=True
            )
            description = st.text_area(
                "Job Description *", placeholder="Paste the job description body here...", height=140
            )
            requirements = st.text_input("Role Requirements", placeholder="e.g. React, Figma, SaaS layout")

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        analyze_clicked = st.button("✨ Execute AI Scan", type="primary", use_container_width=True)

    with result_col:
        with st.container(border=True):
            st.markdown(
                '<p class="section-title"><i class="bi bi-clipboard-data"></i> AI Analysis Console</p>'
                '<p class="section-subtitle">Threat score telemetry and warning flags</p>',
                unsafe_allow_html=True
            )

            if not analyze_clicked:
                st.markdown("""
                <div class="analysis-placeholder">
                    <div class="ph-icon"><i class="bi bi-shield-lock"></i></div>
                    Fill in the listing fields on the left and click <b>Execute AI Scan</b> to run threat analysis.
                </div>
                """, unsafe_allow_html=True)

            elif description.strip() == "":
                st.warning("Job Description is required to initiate the NLP semantic analysis.")

            else:
                # Backend prediction logic (preserved)
                result, probability = predict_job(
                    title, company, description, requirements, salary
                )
                score = round(probability * 100, 2)

                if score >= 60:
                    risk = "High Risk"
                    badge_class = "badge-high"
                    score_class = "score-high"
                    recommendation_title = "Threat Notice: High Scam Probability"
                    recommendation_text = "Severe listing anomalies detected. <b>We strongly advise against applying or sharing identity details.</b>"
                elif score >= 30:
                    risk = "Medium Risk"
                    badge_class = "badge-medium"
                    score_class = "score-medium"
                    recommendation_title = "Precautionary Notice: Mild Anomalies"
                    recommendation_text = "Minor suspicious signals flagged. Verify recruitment authenticity through the company's verified domain."
                else:
                    risk = "Low Risk"
                    badge_class = "badge-low"
                    score_class = "score-low"
                    recommendation_title = "Analysis Cleared: Low Risk"
                    recommendation_text = "No severe anomalies identified. Standard application protocols apply."

                flags = get_risk_flags(
                    title, description, salary, company_profile, remote
                )

                # Render HTML/CSS Progress Ring
                st.markdown(f"""
                <div class="security-indicator">
                    <div class="security-score-circle {score_class}">
                        <div>
                            <span class="security-score-val">{int(score)}</span>
                            <span class="security-score-pct">%</span>
                        </div>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <span class="security-badge {badge_class}">{risk}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Recommendation Alert Box
                reco_icon = "bi-shield-slash" if risk == "High Risk" else ("bi-shield-exclamation" if risk == "Medium Risk" else "bi-shield-check")
                st.markdown(f"""
                <div class="recommendation-box">
                    <div class="reco-icon-wrap"><i class="bi {reco_icon}"></i></div>
                    <div class="reco-content">
                        <span class="reco-title">{recommendation_title}</span>
                        <span class="reco-text">{recommendation_text}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(
                    '<p style="font-weight:600; margin-top:20px; margin-bottom:10px; color:#0F172A; font-size:13px; letter-spacing:-0.01em;">Heuristic Detections</p>',
                    unsafe_allow_html=True
                )

                if flags:
                    chips = ""
                    for flag in flags:
                        icon = FLAG_ICON_MAP.get(flag, "bi-exclamation-circle")
                        p_class = "factor-pill factor-critical" if "payment" in flag.lower() else "factor-pill"
                        chips += f'<span class="{p_class}"><i class="bi {icon}"></i> {flag}</span>'
                    st.markdown(chips, unsafe_allow_html=True)
                else:
                    st.markdown(
                        '<span class="factor-pill" style="background:#ECFDF5; border-color:#A7F3D0; color:#047857; margin-top:4px;">'
                        '<i class="bi bi-check-circle"></i> No vulnerabilities identified</span>',
                        unsafe_allow_html=True
                    )

                save_prediction(title, risk, score)


def page_history(df):
    render_hero(
        "bi-clock-history",
        "Scanned Logs Registry",
        "Audit log history and security classifications of previously inspected job listings.",
    )

    with st.container(border=True):
        if df.empty:
            st.info("No logs database found in this workspace.")
        else:
            st.markdown(
                '<p class="section-title"><i class="bi bi-search"></i> Query Registry</p>'
                '<p class="section-subtitle">Filter registry logs by keywords or risk classifications</p>',
                unsafe_allow_html=True
            )

            c1, c2, c3 = st.columns([2.5, 1.5, 1])
            with c1:
                search_term = st.text_input(
                    "Search", placeholder="🔍 Search scans by job title...", label_visibility="collapsed"
                )
            with c2:
                risk_filter = st.selectbox(
                    "Risk Filter", ["All Scan Alerts", "High Risk", "Medium Risk", "Low Risk"], label_visibility="collapsed"
                )
            with c3:
                st.download_button(
                    label="⬇️ Export Logs (CSV)",
                    data=df.to_csv(index=False),
                    file_name="jobshield_audit_logs.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            filtered = df
            if search_term:
                filtered = filtered[filtered["title"].astype(str).str.contains(search_term, case=False, na=False)]
            if risk_filter != "All Scan Alerts":
                filtered = filtered[filtered["risk"] == risk_filter]

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            st.dataframe(
                filtered.sort_values("timestamp", ascending=False),
                use_container_width=True,
                hide_index=True
            )


def page_analytics(df):
    render_hero(
        "bi-bar-chart-line",
        "Threat Analytics & Telemetry",
        "Aggregated scan frequencies, risk categories, and score metrics.",
    )

    if df.empty:
        with st.container(border=True):
            st.info("No logs database found. Run a few scans to populate telemetry analysis.")
        return

    valid = df.dropna(subset=["timestamp"]).copy()
    valid["date"] = valid["timestamp"].dt.date

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("bi-clipboard-data", "blue", "Total Audited", len(df))
    with c2:
        metric_card("bi-percent", "orange", "Average Threat Score", f"{round(df['score'].mean(), 1)}%")
    with c3:
        metric_card("bi-graph-up-arrow", "red", "Peak Threat Score", f"{round(df['score'].max(), 1)}%")
    with c4:
        metric_card("bi-graph-down-arrow", "green", "Min Threat Score", f"{round(df['score'].min(), 1)}%")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown('<p class="section-title"><i class="bi bi-calendar3"></i> Scan Frequency</p>'
                        '<p class="section-subtitle">Total volume of scans executed per day</p>', unsafe_allow_html=True)
            daily = valid.groupby("date").size()
            fig = go.Figure(go.Bar(
                x=[str(d) for d in daily.index], y=daily.values,
                marker_color="#0F172A", marker_line_width=0,
            ))
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=10, b=10), height=200,
                xaxis=dict(showgrid=False, linecolor="#E4E4E7"),
                yaxis=dict(gridcolor="#F4F4F5", linecolor="#E4E4E7"),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with right:
        with st.container(border=True):
            st.markdown('<p class="section-title"><i class="bi bi-bar-chart-steps"></i> Mean Risk Category Score</p>'
                        '<p class="section-subtitle">Average threat percentage matching alert levels</p>', unsafe_allow_html=True)
            avg_by_risk = df.groupby("risk")["score"].mean().reindex(["Low Risk", "Medium Risk", "High Risk"]).dropna()
            fig = go.Figure(go.Bar(
                x=avg_by_risk.index, y=avg_by_risk.values,
                marker_color=[RISK_COLORS.get(r, "#71717A") for r in avg_by_risk.index],
                text=[f"{v:.1f}%" for v in avg_by_risk.values], textposition="outside",
            ))
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=10, b=10), height=200,
                xaxis=dict(showgrid=False, linecolor="#E4E4E7"),
                yaxis=dict(gridcolor="#F4F4F5", range=[0, 115], linecolor="#E4E4E7"), showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def page_risk_factors():
    render_hero(
        "bi-shield-exclamation",
        "Heuristics Standards",
        "Vectors checked on listing inputs to identify common recruitment scam signals.",
    )

    with st.container(border=True):
        st.markdown(
            '<p class="section-title">Heuristic Alert Criteria</p>'
            '<p class="section-subtitle" style="margin-bottom:0;">'
            'Inspected listings undergo validation with both our NLP neural model and specific rule-based '
            'heuristics, flagging anomalies like applicant fees, shell descriptions, or missing corporate details.</p>',
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    cards = [
        ("bi-cash-coin", "Missing Compensation Range",
         "Omission of transparent compensation limits. Scammers frequently mask exploitative or unrealistic offers by keeping salary ranges completely undisclosed."),
        ("bi-building", "Vague Company Profiles",
         "Lack of verified corporate background. Legitimate enterprises publish clear company histories. Vague or brief corporate details point to spoofed operations."),
        ("bi-alarm", "Pressure & Urgency Tactics",
         "Keywords designed to prompt hasty decisions (e.g. 'immediate start', 'fees required now'). Scam operations rush candidates to bypass normal verification checks."),
        ("bi-credit-card", "Advanced Application Charges",
         "Demands for application, certification, or processing fees. Authentic recruiters never charge job applicants under any circumstances. This represents a critical risk."),
        ("bi-file-earmark-text", "Short Job Specifications",
         "Unusually brief job descriptions lacking structured role specifications. Short summaries usually imply shell listings created purely as recruitment clickbait."),
    ]

    cols = st.columns(3)
    for i, (icon, name, desc) in enumerate(cards):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"""
                <div class="about-card-icon" style="background:#EFF6FF; border-color:#DBEAFE; color:#2563EB;"><i class="bi {icon}"></i></div>
                <h4 style="font-size: 14.5px; font-weight:600; margin-bottom: 8px; color: #0F172A;">{name}</h4>
                <p style="font-size: 12.5px; color:#52525B; line-height: 1.6; margin:0;">{desc}</p>
                """, unsafe_allow_html=True)
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)


def page_reports(df):
    render_hero(
        "bi-file-earmark-text",
        "Compliance Logs Export",
        "Download workspace audit records, risk tallies, and threat database compliance files.",
    )

    if df.empty:
        with st.container(border=True):
            st.info("No audit logs found to generate compliance records.")
        return

    total_jobs = len(df)
    high_n = len(df[df["risk"] == "High Risk"])
    medium_n = len(df[df["risk"] == "Medium Risk"])
    low_n = len(df[df["risk"] == "Low Risk"])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("bi-briefcase", "blue", "Total Audited", total_jobs)
    with c2:
        metric_card("bi-exclamation-triangle", "red", "Critical Threats", high_n)
    with c3:
        metric_card("bi-shield-plus", "orange", "Alert Warnings", medium_n)
    with c4:
        metric_card("bi-patch-check", "green", "Normal Clearance", low_n)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(
            '<p class="section-title"><i class="bi bi-download"></i> Download Audit database</p>'
            '<p class="section-subtitle">Export full compliance logs in standard CSV layout for corporate archiving</p>',
            unsafe_allow_html=True
        )
        st.download_button(
            label="⬇_ Export Audit Log Database (CSV)",
            data=df.to_csv(index=False),
            file_name="jobshield_compliance_audit_logs.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.markdown("<div style='height: 18px; border-top:1px solid #F4F4F5; margin-top:18px;'></div>", unsafe_allow_html=True)
        st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True, hide_index=True)


def page_settings():
    render_hero(
        "bi-gear",
        "Console Preferences",
        "Configure custom threat parameters, score alerts, and audit preferences.",
    )
    
    with st.container(border=True):
        st.markdown('<p class="section-title"><i class="bi bi-sliders"></i> Security Thresholds</p>'
                    '<p class="section-subtitle">Adjust risk metrics and threshold defaults for scanning results</p>', unsafe_allow_html=True)
        
        st.slider("High Risk Score Threshold", 50, 90, 60, help="Minimum probability score to label a posting as High Risk.")
        st.slider("Medium Risk Score Threshold", 20, 50, 30, help="Minimum probability score to label a posting as Medium Risk.")
        
        st.markdown("<div style='height: 18px; border-top:1px solid #F4F4F5; margin-top: 18px;'></div>", unsafe_allow_html=True)
        st.markdown('<p class="section-title"><i class="bi bi-database-gear"></i> Log Retention</p>'
                    '<p class="section-subtitle">Configure retention period for CSV database scans</p>', unsafe_allow_html=True)
        st.selectbox("History Log Retention Limit", ["Keep indefinitely", "Last 100 scans", "Last 30 days", "Clear on session exit"])
        
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.button("Save Preferences Settings")


def page_about():
    render_hero(
        "bi-info-circle",
        "Platform Overview",
        "Technical documentation and architecture details of the JobShield AI Threat Engine.",
    )

    st.markdown("""
    <div class="about-hero">
        <h2>Shielding the Future of Work</h2>
        <p>JobShield AI is a commercial-grade threat detection engine designed to inspect, identify, and report suspicious employment listings before they compromise candidate safety.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="grid-3col">
        <div class="about-card">
            <div class="about-card-icon"><i class="bi bi-cpu"></i></div>
            <h3>ML Classifier</h3>
            <p>A natural language processing pipeline powered by Logistic Regression and TF-IDF feature mapping trained on verified employment fraud datasets.</p>
        </div>
        <div class="about-card">
            <div class="about-card-icon"><i class="bi bi-shield-lock"></i></div>
            <h3>Heuristic Engine</h3>
            <p>Rules check for advanced payment requests, insufficient profile summaries, and aggressive urgency copy designed to bypass traditional filters.</p>
        </div>
        <div class="about-card">
            <div class="about-card-icon"><i class="bi bi-activity"></i></div>
            <h3>Audit Console</h3>
            <p>Centralized logging database offering full scan compliance registry, relative timeline metrics, and security statistics exporting.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("""
            <p class="section-title"><i class="bi bi-rocket-takeoff"></i> Our Mission</p>
            <p style="color:#52525B; font-size:13.5px; line-height:1.7; margin:0;">
                Employment fraud has risen significantly with remote work adoption. Scammers impersonate established companies to harvest private candidate details or extract upfront fees. JobShield AI was built to put threat detection directly into the hands of job seekers and recruitment teams, ensuring every role is verified.
            </p>
            """, unsafe_allow_html=True)
    with col2:
        with st.container(border=True):
            st.markdown("""
            <p class="section-title"><i class="bi bi-layers"></i> Threat Tech Stack</p>
            <p style="color:#52525B; font-size:13.5px; line-height:1.8; margin:0;">
                • <b>Language</b>: Python 3.10+<br>
                • <b>Interface</b>: Streamlit Enterprise<br>
                • <b>Modeling</b>: Scikit-learn Logistic Regression<br>
                • <b>NLP Pipeline</b>: TF-IDF Text Vectorization<br>
                • <b>Visuals</b>: Plotly Graphing Engine & Vanilla CSS Tokens
            </p>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="height: 24px;"></div>
    <div class="about-footer">
        JobShield AI Security Suite • Version 2.1.0 • Released under Pro License
    </div>
    """, unsafe_allow_html=True)


# =====================================================================
# ===========================  MAIN ROUTER  ===========================
# =====================================================================

menu = render_sidebar()
history_df = load_history()

render_top_bar(menu, history_df)

if menu == "Dashboard":
    page_dashboard(history_df)
elif menu == "Scan New Job":
    page_scan()
elif menu == "History":
    page_history(history_df)
elif menu == "Analytics":
    page_analytics(history_df)
elif menu == "Risk Factors":
    page_risk_factors()
elif menu == "Reports":
    page_reports(history_df)
elif menu == "Settings":
    page_settings()
elif menu == "About":
    page_about()