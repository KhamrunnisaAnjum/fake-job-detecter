# ================= app.py =================

from auth import login
import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime

from preprocess import clean_text
from risk_rules import get_risk_flags


# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="JobShield AI | Fake Job Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()


# ================= CUSTOM UI (Notion / Linear / Vercel style) =================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.stApp {
    background-color: #FFFFFF;
}

#MainMenu, footer, header[data-testid="stHeader"] {
    visibility: hidden;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1300px;
}

h1, h2, h3 {
    color: #111827;
    letter-spacing: -0.3px;
}

/* ---------------- SIDEBAR ---------------- */
section[data-testid="stSidebar"] {
    background-color: #FAFAFA;
    border-right: 1px solid #E5E7EB;
}
section[data-testid="stSidebar"] > div {
    padding-top: 1.2rem;
}
.sidebar-brand {
    padding: 4px 4px 18px 4px;
    border-bottom: 1px solid #E5E7EB;
    margin-bottom: 16px;
}
.sidebar-brand h1 {
    font-size: 19px;
    font-weight: 700;
    color: #111827;
    margin: 0;
}
.sidebar-brand p {
    font-size: 12.5px;
    color: #9CA3AF;
    margin: 4px 0 0 0;
}

div[data-testid="stSidebar"] .stRadio > label {
    font-size: 12px;
    font-weight: 600;
    color: #9CA3AF;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
div[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
    padding: 9px 12px;
    border-radius: 10px;
    margin-bottom: 2px;
    font-size: 14px;
    color: #374151;
    transition: background 0.15s ease;
}
div[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
    background: #F3F4F6;
}

.sidebar-note {
    background: #F9FAFB;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 12px 14px;
    margin-top: 14px;
}
.sidebar-note p {
    margin: 0;
    font-size: 12px;
    color: #6B7280;
    line-height: 1.5;
}

/* ---------------- GENERIC CARD ---------------- */
.js-card {
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    background: #FFFFFF;
    padding: 26px 28px;
    margin-bottom: 22px;
}

/* ---------------- HERO ---------------- */
.hero-card {
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    background: #FAFAFA;
    padding: 32px 34px;
    margin-bottom: 24px;
}
.hero-card h1 {
    font-size: 26px;
    font-weight: 700;
    margin: 0 0 8px 0;
}
.hero-card p {
    font-size: 14.5px;
    color: #6B7280;
    margin: 0;
}

/* ---------------- SECTION TITLES ---------------- */
.section-title {
    font-size: 17px;
    font-weight: 700;
    color: #111827;
    margin: 0 0 4px 0;
}
.section-subtitle {
    font-size: 13px;
    color: #9CA3AF;
    margin: 0 0 16px 0;
}

/* ---------------- INPUTS ---------------- */
.stTextInput input,
.stTextArea textarea,
.stSelectbox > div > div {
    border-radius: 10px !important;
    border: 1px solid #E5E7EB !important;
    background: #FFFFFF !important;
    font-size: 14px !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #111827 !important;
    box-shadow: 0 0 0 3px rgba(17,24,39,0.06) !important;
}
label {
    font-weight: 600 !important;
    color: #374151 !important;
    font-size: 13px !important;
}

/* ---------------- BUTTONS ---------------- */
div.stButton > button {
    background: #111827 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    height: 46px !important;
    font-weight: 600 !important;
    font-size: 14.5px !important;
    transition: background 0.15s ease;
}
div.stButton > button:hover {
    background: #000000 !important;
}

/* ---------------- METRICS ---------------- */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 16px;
    padding: 18px 20px;
}
div[data-testid="stMetricLabel"] {
    color: #9CA3AF !important;
    font-size: 12.5px !important;
    font-weight: 600 !important;
}
div[data-testid="stMetricValue"] {
    color: #111827 !important;
    font-weight: 700 !important;
}

/* ---------------- RISK BADGES ---------------- */
.risk-badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12.5px;
    font-weight: 600;
    letter-spacing: 0.2px;
}
.badge-high { background:#FEF2F2; color:#DC2626; border:1px solid #FECACA; }
.badge-medium { background:#FFFBEB; color:#B45309; border:1px solid #FDE68A; }
.badge-low { background:#F0FDF4; color:#15803D; border:1px solid #BBF7D0; }

.flag-card {
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 8px;
    background: #FAFAFA;
    font-size: 13.5px;
    color: #374151;
}

.reco-box {
    border-radius: 12px;
    padding: 16px 18px;
    font-size: 14px;
    font-weight: 500;
    margin-top: 12px;
    border: 1px solid #E5E7EB;
    background: #FAFAFA;
    color: #111827;
}

/* ---------------- TABLES ---------------- */
div[data-testid="stDataFrame"] {
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    overflow: hidden;
}

hr { border-color: #E5E7EB; }

</style>
""", unsafe_allow_html=True)


# ================= LOAD MODEL =================

classifier = joblib.load(
    "model/classifier.pkl"
)

vectorizer = joblib.load(
    "model/vectorizer.pkl"
)


# ================= CONSTANT =================

LOG_FILE = "checked_postings.csv"


# ================= SIDEBAR =================

with st.sidebar:

    st.markdown("""
    <div class="sidebar-brand">
        <h1>🛡️ JobShield AI</h1>
        <p>Fraud Detection Workspace</p>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "Menu",
        [
            "Dashboard",
            "Scan New Job",
            "History",
            "About"
        ],
        label_visibility="collapsed"
    )

    st.markdown("""
    <div class="sidebar-note">
        <p>Machine Learning + NLP Based System</p>
    </div>
    """, unsafe_allow_html=True)


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


# ================= SCAN NEW JOB PAGE =================

if menu == "Scan New Job":

    st.markdown("""
    <div class="hero-card">
        <h1>🛡️ JobShield AI</h1>
        <p>Protecting job seekers using Machine Learning and NLP.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="js-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">Scan New Job Posting</p><p class="section-subtitle">Fill in the job details below to analyze fraud risk</p>', unsafe_allow_html=True)

    with st.container():

        col1, col2 = st.columns(2)

        with col1:

            title = st.text_input(
                "Job Title",
                placeholder="Example: Software Engineer"
            )

            company = st.text_input(
                "Company Name",
                placeholder="Example: Microsoft"
            )

            salary = st.text_input(
                "Salary Range",
                placeholder="Example: ₹8 LPA"
            )

        with col2:

            remote = st.checkbox(
                "🏠 Remote / Work From Home"
            )

            requirements = st.text_area(
                "Requirements",
                height=120
            )

    company_profile = st.text_area(
        "Company Profile",
        height=100
    )

    description = st.text_area(
        "Job Description",
        height=180
    )

    analyze_clicked = st.button(
        "🚀 Analyze with AI",
        use_container_width=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

    if analyze_clicked:

        if description.strip() == "":
            st.warning("Please enter job description.")

        else:

            result, probability = predict_job(
                title,
                company,
                description,
                requirements,
                salary
            )

            score = round(probability * 100, 2)

            if score >= 60:
                risk = "High Risk"
                badge_class = "badge-high"
                recommendation = "Avoid applying until company legitimacy is verified."

            elif score >= 30:
                risk = "Medium Risk"
                badge_class = "badge-medium"
                recommendation = "Verify company details before applying."

            else:
                risk = "Low Risk"
                badge_class = "badge-low"
                recommendation = "Appears safe but always verify independently."

            flags = get_risk_flags(
                title,
                description,
                salary,
                company_profile,
                remote
            )

            st.markdown('<div class="js-card">', unsafe_allow_html=True)
            st.markdown('<p class="section-title">AI Analysis Result</p><p class="section-subtitle">Fraud probability score and detected risk factors</p>', unsafe_allow_html=True)

            m1, m2 = st.columns(2)

            with m1:
                st.metric("Fraud Probability", f"{score}%")

            with m2:
                st.markdown(
                    f'<div style="padding-top:8px;">'
                    f'<span class="risk-badge {badge_class}">{risk}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            st.markdown(
                f'<div class="reco-box"><strong>Recommendation:</strong> {recommendation}</div>',
                unsafe_allow_html=True
            )

            st.markdown('<p style="font-weight:600; margin-top:20px; margin-bottom:8px; color:#111827;">Risk Factors</p>', unsafe_allow_html=True)

            if flags:
                for flag in flags:
                    st.markdown(f'<div class="flag-card">⚠️ {flag}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="flag-card">✅ No suspicious factors found.</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

            save_prediction(
                title,
                risk,
                score
            )


# ================= DASHBOARD PAGE =================

elif menu == "Dashboard":

    st.markdown("""
    <div class="hero-card">
        <h1>📊 JobShield AI Dashboard</h1>
        <p>Protecting job seekers using Machine Learning and NLP.</p>
    </div>
    """, unsafe_allow_html=True)

    if os.path.exists(LOG_FILE):

        df = pd.read_csv(LOG_FILE)

        total_jobs = len(df)

        fake_jobs = len(
            df[df["risk"] == "High Risk"]
        )

        real_jobs = total_jobs - fake_jobs

        avg_score = round(
            df["score"].mean(),
            2
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📄 Total Scans", total_jobs)

        with col2:
            st.metric("🚫 High Risk Jobs", fake_jobs)

        with col3:
            st.metric("✅ Low Risk Jobs", real_jobs)

        with col4:
            st.metric("📊 Average Fraud Score", f"{avg_score}%")

        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

        left, right = st.columns(2)

        with left:
            st.markdown('<div class="js-card">', unsafe_allow_html=True)
            st.markdown('<p class="section-title">📌 Risk Distribution</p>', unsafe_allow_html=True)

            risk_count = df["risk"].value_counts()

            st.bar_chart(risk_count)
            st.markdown('</div>', unsafe_allow_html=True)

        with right:
            st.markdown('<div class="js-card">', unsafe_allow_html=True)
            st.markdown('<p class="section-title">📈 Fraud Score Trend</p>', unsafe_allow_html=True)

            st.line_chart(df["score"])
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="js-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-title">📋 Recent Predictions</p>', unsafe_allow_html=True)

        st.dataframe(
            df.tail(10),
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    else:

        st.markdown('<div class="js-card">', unsafe_allow_html=True)
        st.info("No predictions available yet.")
        st.markdown('</div>', unsafe_allow_html=True)


# ================= HISTORY PAGE =================

elif menu == "History":

    st.markdown("""
    <div class="hero-card">
        <h1>🕒 Prediction History</h1>
        <p>Search and review all past predictions.</p>
    </div>
    """, unsafe_allow_html=True)

    if os.path.exists(LOG_FILE):

        history = pd.read_csv(LOG_FILE)

        st.markdown('<div class="js-card">', unsafe_allow_html=True)

        search_col, download_col = st.columns([3, 1])

        with search_col:
            search_term = st.text_input(
                "Search",
                placeholder="🔍 Search by job title",
                label_visibility="collapsed"
            )

        with download_col:
            st.download_button(
                label="⬇️ Download CSV",
                data=history.to_csv(index=False),
                file_name="jobshield_history.csv",
                mime="text/csv",
                use_container_width=True
            )

        filtered = history

        if search_term:
            filtered = history[
                history["title"].astype(str).str.contains(search_term, case=False, na=False)
            ]

        st.dataframe(
            filtered,
            use_container_width=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

    else:

        st.markdown('<div class="js-card">', unsafe_allow_html=True)
        st.info("No prediction history found.")
        st.markdown('</div>', unsafe_allow_html=True)


# ================= ABOUT PAGE =================

elif menu == "About":

    st.markdown("""
    <div class="hero-card">
        <h1>ℹ️ About JobShield AI</h1>
        <p>Fake Job Posting Detection System</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="js-card">
        <p class="section-title">About JobShield AI</p>
        <p style="color:#374151; font-size:14px; line-height:1.7;">
            JobShield AI is a Machine Learning and Natural Language Processing
            based application that detects suspicious job postings before
            job seekers apply or share personal information.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="js-card">
            <p class="section-title">Features</p>
            <p style="color:#374151; font-size:14px; line-height:2;">
                ✅ AI based fake job detection<br>
                ✅ Fraud probability score<br>
                ✅ Risk factor explanation<br>
                ✅ Prediction history<br>
                ✅ Dashboard analytics
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="js-card">
            <p class="section-title">Technology Stack</p>
            <p style="color:#374151; font-size:14px; line-height:2;">
                • Python<br>
                • Streamlit<br>
                • Machine Learning<br>
                • NLP<br>
                • TF-IDF<br>
                • Scikit-learn
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="js-card">
        <p class="section-title">Purpose</p>
        <p style="color:#374151; font-size:14px; line-height:1.7;">
            To help job seekers identify possible employment scams
            before sharing personal information or paying money.
        </p>
    </div>
    """, unsafe_allow_html=True)