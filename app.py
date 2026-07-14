import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="JobShield AI | Fake Job Posting Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------------------------
PRIMARY = "#2563EB"
PRIMARY_DARK = "#1D4ED8"
BG = "#F8FAFC"
CARD = "#FFFFFF"
TEXT_DARK = "#0F172A"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
DANGER = "#EF4444"
BORDER = "#E2E8F0"
RADIUS = "18px"

MENU_ITEMS = [
    ("Dashboard", "📊"),
    ("Scan New Job", "🔍"),
    ("Scan History", "🕒"),
    ("Analytics", "📈"),
    ("Risk Factors", "⚠️"),
    ("Reports", "📁"),
    ("Settings", "⚙️"),
    ("About Project", "ℹ️"),
]

# ----------------------------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------------------------
if "active_page" not in st.session_state:
    st.session_state.active_page = "Dashboard"

if "scan_history" not in st.session_state:
    demo_titles = [
        ("Senior Data Analyst", "Nexora Analytics Pvt Ltd", "Low Risk"),
        ("Work From Home Data Entry", "QuickCash Global LLC", "High Risk"),
        ("Frontend Developer (React)", "Bluewave Softworks", "Low Risk"),
        ("Immediate Hiring - Earn $500/day", "HomeProfit Ventures", "High Risk"),
        ("HR Executive", "Meridian Consulting Group", "Medium Risk"),
        ("Customer Support Associate", "TalkPoint Solutions", "Medium Risk"),
        ("Payment Processing Agent", "FastFundz Inc", "High Risk"),
        ("Product Manager", "Orbital Systems", "Low Risk"),
        ("Content Writer (Remote)", "WordCraft Media", "Low Risk"),
        ("Mystery Shopper Needed Urgently", "ShopSecret Rewards", "High Risk"),
    ]
    rows = []
    for i, (title, company, risk) in enumerate(demo_titles):
        rows.append({
            "Job Title": title,
            "Company": company,
            "Risk Level": risk,
            "Date": (datetime.now() - timedelta(hours=i * 7 + random.randint(1, 5))).strftime("%d %b %Y, %I:%M %p"),
        })
    st.session_state.scan_history = rows

if "last_result" not in st.session_state:
    st.session_state.last_result = None

# ----------------------------------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}

    .stApp {{ background-color: {BG}; }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header[data-testid="stHeader"] {{ background-color: transparent; height: 0px; }}

    .block-container {{
        padding-top: 1.6rem;
        padding-bottom: 3.5rem;
        max-width: 1440px;
    }}

    /* ---------------- SIDEBAR ---------------- */
    section[data-testid="stSidebar"] {{
        background-color: #FFFFFF;
        border-right: 1px solid {BORDER};
        min-width: 280px !important;
        box-shadow: 2px 0 12px rgba(15,23,42,0.03);
    }}
    section[data-testid="stSidebar"] > div {{ padding-top: 1.2rem; }}

    .sidebar-logo {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 6px 22px 6px;
        border-bottom: 1px solid {BORDER};
        margin-bottom: 22px;
    }}
    .sidebar-logo-icon {{
        font-size: 32px;
        line-height: 1;
        background: linear-gradient(135deg, #EFF6FF, #DBEAFE);
        border-radius: 14px;
        width: 52px;
        height: 52px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 10px rgba(37,99,235,0.15);
    }}
    .sidebar-logo-text h1 {{
        font-size: 18.5px;
        font-weight: 800;
        color: {TEXT_DARK};
        margin: 0;
        letter-spacing: -0.3px;
    }}
    .sidebar-logo-text p {{
        font-size: 12px;
        color: #64748B;
        margin: 2px 0 0 0;
        font-weight: 500;
    }}

    div[data-testid="stSidebar"] .stButton > button {{
        width: 100%;
        text-align: left;
        background-color: transparent;
        border: none;
        border-radius: 12px;
        padding: 11px 16px;
        margin-bottom: 5px;
        color: #475569;
        font-weight: 500;
        font-size: 14.5px;
        transition: all 0.18s ease-in-out;
        box-shadow: none;
    }}
    div[data-testid="stSidebar"] .stButton > button:hover {{
        background-color: #EFF6FF;
        color: {PRIMARY};
        transform: translateX(3px);
    }}
    div[data-testid="stSidebar"] .stButton > button:focus {{ box-shadow: none !important; }}
    div[data-testid="stSidebar"] .stButton > button:active {{ background-color: #DBEAFE; }}

    .nav-active > button {{
        background: linear-gradient(135deg, {PRIMARY}, {PRIMARY_DARK}) !important;
        color: white !important;
        font-weight: 600 !important;
        box-shadow: 0 6px 16px rgba(37,99,235,0.35) !important;
    }}
    .nav-active > button:hover {{
        background: linear-gradient(135deg, {PRIMARY_DARK}, {PRIMARY}) !important;
        color: white !important;
        transform: none;
    }}

    /* ---------------- TOP HEADER ---------------- */
    .header-left h2 {{ margin: 0; font-size: 22px; font-weight: 700; color: {TEXT_DARK}; }}
    .header-left p {{ margin: 2px 0 0 0; font-size: 13px; color: #64748B; }}

    .notif-icon {{
        position: relative;
        background: #F1F5F9;
        border-radius: 50%;
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        transition: all 0.15s ease;
    }}
    .notif-icon:hover {{ background:#E2E8F0; transform: scale(1.05); }}
    .notif-dot {{
        position: absolute; top: 6px; right: 7px;
        width: 8px; height: 8px; background: {DANGER};
        border-radius: 50%; border: 2px solid white;
    }}
    .user-chip {{
        display: flex; align-items: center; gap: 10px;
        background: #F8FAFC; border: 1px solid {BORDER};
        padding: 7px 16px 7px 8px; border-radius: 30px;
        box-shadow: 0 1px 2px rgba(15,23,42,0.03);
    }}
    .user-avatar {{
        width: 34px; height: 34px; border-radius: 50%;
        background: linear-gradient(135deg, {PRIMARY}, #7C3AED);
        display: flex; align-items: center; justify-content: center;
        color: white; font-weight: 700; font-size: 13px;
    }}
    .user-chip-text p {{ margin: 0; line-height: 1.15; }}
    .user-chip-name {{ font-size: 13px; font-weight: 600; color: {TEXT_DARK}; }}
    .user-chip-role {{ font-size: 11px; color: #94A3B8; }}

    /* ---------------- GENERIC CARD ---------------- */
    .jsa-card {{
        background-color: {CARD};
        border: 1px solid {BORDER};
        border-radius: {RADIUS};
        padding: 28px 30px;
        box-shadow: 0 4px 14px rgba(15,23,42,0.05), 0 1px 3px rgba(15,23,42,0.04);
        margin-bottom: 26px;
        transition: box-shadow 0.25s ease, transform 0.25s ease;
    }}
    .jsa-card:hover {{
        box-shadow: 0 14px 32px rgba(15,23,42,0.09);
    }}

    /* ---------------- HERO ---------------- */
    .hero-card {{
        background: linear-gradient(120deg, #EFF6FF 0%, #F8FAFC 55%, #EEF2FF 100%);
        border: 1px solid {BORDER};
        border-radius: {RADIUS};
        padding: 38px 44px;
        margin-bottom: 28px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 24px;
        flex-wrap: wrap;
        box-shadow: 0 6px 20px rgba(37,99,235,0.06);
    }}
    .hero-left h1 {{
        font-size: 29px; font-weight: 800; color: {TEXT_DARK};
        margin: 0 0 10px 0; letter-spacing: -0.6px; max-width: 620px;
    }}
    .hero-left p {{
        font-size: 15px; color: #475569; max-width: 560px; margin: 0; line-height: 1.65;
    }}
    .hero-badge {{
        display: inline-block; background: #DBEAFE; color: {PRIMARY};
        font-size: 12px; font-weight: 700; padding: 6px 14px; border-radius: 20px;
        margin-bottom: 14px; letter-spacing: 0.4px;
    }}
    .hero-icon-wrap {{
        background: white; border: 1px solid {BORDER}; border-radius: {RADIUS};
        width: 110px; height: 110px; display: flex; align-items: center; justify-content: center;
        font-size: 52px; box-shadow: 0 12px 30px rgba(37,99,235,0.18); flex-shrink: 0;
    }}

    /* ---------------- METRIC / KPI CARDS ---------------- */
    .metric-card {{
        background-color: {CARD};
        border: 1px solid {BORDER};
        border-radius: {RADIUS};
        padding: 24px 24px;
        box-shadow: 0 3px 10px rgba(15,23,42,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
    }}
    .metric-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 16px 30px rgba(15,23,42,0.10);
    }}
    .metric-icon {{
        width: 52px; height: 52px; border-radius: 14px;
        display: flex; align-items: center; justify-content: center;
        font-size: 24px; margin-bottom: 16px;
    }}
    .metric-title {{ font-size: 13px; color: #64748B; font-weight: 600; margin: 0 0 6px 0; }}
    .metric-value {{ font-size: 32px; font-weight: 800; color: {TEXT_DARK}; margin: 0 0 8px 0; letter-spacing: -0.6px; }}
    .metric-trend {{ font-size: 12.5px; font-weight: 700; }}

    /* ---------------- SECTION TITLES ---------------- */
    .section-title {{ font-size: 19px; font-weight: 700; color: {TEXT_DARK}; margin: 4px 0 4px 0; }}
    .section-subtitle {{ font-size: 13px; color: #64748B; margin: 0 0 18px 0; }}

    /* ---------------- FORM INPUTS ---------------- */
    .stTextInput > div > div > input,
    .stTextArea textarea,
    .stSelectbox > div > div,
    .stNumberInput input {{
        border-radius: 12px !important;
        border: 1.5px solid {BORDER} !important;
        background-color: #F8FAFC !important;
        font-size: 14px !important;
    }}
    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus {{
        border-color: {PRIMARY} !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
    }}
    label {{ font-weight: 600 !important; color: {TEXT_DARK} !important; font-size: 13.5px !important; }}

    div.stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, {PRIMARY}, {PRIMARY_DARK});
        color: white; border: none; border-radius: 12px; padding: 13px 0;
        font-weight: 700; font-size: 15.5px;
        box-shadow: 0 8px 20px rgba(37,99,235,0.32);
        transition: all 0.18s ease; width: 100%;
    }}
    div.stButton > button[kind="primary"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 14px 28px rgba(37,99,235,0.42);
    }}

    /* ---------------- BADGES / PILLS ---------------- */
    .badge {{
        display: inline-flex; align-items: center; gap: 8px;
        padding: 9px 16px; border-radius: 12px; font-size: 13.5px; font-weight: 600;
        margin: 5px 6px 5px 0; border: 1px solid;
    }}
    .badge-danger {{ background-color: #FEF2F2; color: {DANGER}; border-color: #FECACA; }}
    .badge-warning {{ background-color: #FFFBEB; color: #B45309; border-color: #FDE68A; }}
    .badge-success {{ background-color: #ECFDF5; color: #047857; border-color: #A7F3D0; }}

    .risk-pill {{
        display: inline-block; padding: 5px 14px; border-radius: 20px;
        font-size: 11.5px; font-weight: 700; letter-spacing: 0.3px;
    }}
    .pill-high {{ background:#FEF2F2; color:{DANGER}; }}
    .pill-medium {{ background:#FFFBEB; color:#B45309; }}
    .pill-low {{ background:#ECFDF5; color:#047857; }}

    .reco-box {{
        border-radius: 14px; padding: 16px 20px; font-size: 14.5px;
        font-weight: 600; margin-top: 10px; border-left: 5px solid;
    }}

    /* ---------------- ANIMATED GAUGE ---------------- */
    .gauge-wrap {{
        position: relative; display: flex; align-items: center; justify-content: center;
        margin: 6px auto 4px auto;
    }}
    .gauge-circle {{ animation: gaugeFill 1.4s cubic-bezier(0.22, 1, 0.36, 1) forwards; }}
    @keyframes gaugeFill {{
        from {{ stroke-dashoffset: var(--circumference); }}
        to {{ stroke-dashoffset: var(--target-offset); }}
    }}
    .gauge-label {{ position: absolute; text-align: center; }}
    .gauge-score {{
        font-size: 32px; font-weight: 800; color: {TEXT_DARK};
        animation: fadeIn 1s ease 0.4s both;
    }}
    .gauge-caption {{ font-size: 12.5px; color: #64748B; font-weight: 600; }}
    @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: translateY(0); }} }}

    /* ---------------- RECENT SCANS TABLE ---------------- */
    .scan-table {{ width: 100%; border-collapse: collapse; }}
    .scan-table th {{
        text-align: left; font-size: 12px; color: #64748B; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.4px;
        padding: 10px 14px; border-bottom: 2px solid {BORDER};
    }}
    .scan-table td {{
        padding: 14px; font-size: 13.5px; color: {TEXT_DARK};
        border-bottom: 1px solid {BORDER};
    }}
    .scan-table tr:hover td {{ background-color: #F8FAFC; }}
    .scan-table tr:last-child td {{ border-bottom: none; }}

    hr {{ border-color: {BORDER}; }}
    .stCheckbox {{ padding-top: 6px; }}
    div[data-testid="column"] {{ padding: 8px; }}

    /* ---------------- RESPONSIVE ---------------- */
    @media (max-width: 900px) {{
        .hero-card {{ flex-direction: column; text-align: center; padding: 28px; }}
        .hero-left p {{ max-width: 100%; }}
        .metric-card {{ margin-bottom: 14px; }}
    }}
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">🛡️</div>
        <div class="sidebar-logo-text">
            <h1>JobShield AI</h1>
            <p>Fake Job Detector</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for label, icon in MENU_ITEMS:
        is_active = st.session_state.active_page == label
        wrapper_class = "nav-active" if is_active else "nav-inactive"
        st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
        if st.button(f"{icon}    {label}", key=f"nav_{label}", use_container_width=True):
            st.session_state.active_page = label
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:#F0F9FF; border:1px solid #BAE6FD; border-radius:14px; padding:14px 16px; margin-top:10px;">
        <p style="margin:0; font-size:12px; color:#0369A1; font-weight:600;">🎓 Final Year Project</p>
        <p style="margin:4px 0 0 0; font-size:11.5px; color:#0284C7;">ML + NLP based fraud detection system for academic exhibition.</p>
    </div>
    """, unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# TOP HEADER
# ----------------------------------------------------------------------------
def top_header(title, subtitle):
    c1, c2, c3, c4 = st.columns([3.2, 2.4, 0.6, 1.6])
    with c1:
        st.markdown(f"""
        <div style="padding-top:6px;">
            <h2 style="margin:0;font-size:20px;font-weight:700;color:{TEXT_DARK};">{title}</h2>
            <p style="margin:0;font-size:13px;color:#64748B;">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.text_input("Search", placeholder="🔍  Search jobs, companies, reports...", label_visibility="collapsed")
    with c3:
        st.markdown('<div class="notif-icon">🔔<div class="notif-dot"></div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="user-chip">
            <div class="user-avatar">SA</div>
            <div class="user-chip-text">
                <p class="user-chip-name">Sneha Agarwal</p>
                <p class="user-chip-role">Fraud Analyst</p>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# RULE BASED FRAUD SCORING ENGINE
# ----------------------------------------------------------------------------
URGENCY_WORDS = ["urgent", "immediate", "asap", "act now", "hurry", "limited slots", "instant hire"]
PAYMENT_WORDS = ["registration fee", "processing fee", "deposit", "pay to apply", "training fee", "refundable deposit"]
VAGUE_WORDS = ["easy money", "no experience needed", "work from home guaranteed", "earn daily", "be your own boss"]

def analyze_job(title, company, description, requirements, benefits, salary, remote):
    text = " ".join([title or "", company or "", description or "", requirements or "", benefits or "", salary or ""]).lower()
    score = 10
    factors = []

    if not company or len(company.strip()) < 3:
        score += 20
        factors.append(("Missing company information", "danger"))

    if any(w in text for w in URGENCY_WORDS):
        score += 15
        factors.append(("Uses urgency language", "warning"))

    if any(w in text for w in PAYMENT_WORDS):
        score += 30
        factors.append(("Requests payment from applicants", "danger"))

    if any(w in text for w in VAGUE_WORDS):
        score += 15
        factors.append(("Uses vague / too-good-to-be-true phrasing", "warning"))

    if salary:
        digits = "".join(c for c in salary if c.isdigit())
        if digits and len(digits) >= 6 and ("hour" in salary.lower() or "day" in salary.lower()):
            score += 20
            factors.append(("Unrealistic salary offered", "danger"))
        elif digits and int(digits[:7] or 0) > 5000000:
            score += 15
            factors.append(("Unrealistic salary offered", "danger"))

    if not description or len(description.strip()) < 40:
        score += 10
        factors.append(("Very short / generic job description", "warning"))

    if not requirements or len(requirements.strip()) < 15:
        score += 8
        factors.append(("No clear requirements specified", "warning"))

    if "@gmail.com" in text or "@yahoo.com" in text or "whatsapp" in text:
        score += 12
        factors.append(("Uses personal email / messaging app for contact", "warning"))

    if not factors:
        factors.append(("No major red flags detected", "success"))

    score = min(score, 97)
    score = max(score, 4)

    if score >= 65:
        risk_level = "HIGH RISK"
        risk_color = DANGER
        recommendation = "Do not apply for this job. It may be a scam. Verify the company independently before sharing any personal or financial information."
    elif score >= 35:
        risk_level = "MEDIUM RISK"
        risk_color = WARNING
        recommendation = "Proceed with caution. Verify company details, recruiter identity, and never pay any fee to apply or get hired."
    else:
        risk_level = "LOW RISK"
        risk_color = SUCCESS
        recommendation = "This posting looks reasonably legitimate. Still verify the company and recruiter before sharing sensitive documents."

    return {
        "score": score,
        "risk_level": risk_level,
        "risk_color": risk_color,
        "recommendation": recommendation,
        "factors": factors,
    }


# ----------------------------------------------------------------------------
# ANIMATED HTML/CSS FRAUD SCORE GAUGE
# ----------------------------------------------------------------------------
def render_animated_gauge(score, color, size=190, stroke=14):
    radius = (size / 2) - (stroke * 1.4)
    circumference = 2 * 3.14159265 * radius
    offset = circumference - (score / 100) * circumference
    center = size / 2

    html = (
        f'<div class="gauge-wrap" style="width:{size}px; height:{size}px;">'
        f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
        f'<circle cx="{center}" cy="{center}" r="{radius}" fill="none" stroke="#F1F5F9" stroke-width="{stroke}"/>'
        f'<circle cx="{center}" cy="{center}" r="{radius}" fill="none" stroke="{color}" stroke-width="{stroke}" '
        f'stroke-linecap="round" stroke-dasharray="{circumference}" stroke-dashoffset="{circumference}" '
        f'transform="rotate(-90 {center} {center})" class="gauge-circle" '
        f'style="--target-offset:{offset}px; --circumference:{circumference}px;"/>'
        f'</svg>'
        f'<div class="gauge-label">'
        f'<div class="gauge-score">{score}%</div>'
        f'<div class="gauge-caption">Fraud Score</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# RECENT SCANS TABLE WITH COLORED RISK BADGES
# (fixed: no leading indentation / blank lines so Markdown doesn't treat
#  this as an indented code block)
# ----------------------------------------------------------------------------
def render_scan_table(rows):
    pill_map = {"High Risk": "pill-high", "Medium Risk": "pill-medium", "Low Risk": "pill-low"}
    body_rows = ""
    for r in rows:
        pill_cls = pill_map.get(r["Risk Level"], "pill-medium")
        body_rows += (
            f'<tr>'
            f'<td>{r["Job Title"]}</td>'
            f'<td>{r["Company"]}</td>'
            f'<td><span class="risk-pill {pill_cls}">{r["Risk Level"]}</span></td>'
            f'<td style="color:#64748B;">{r["Date"]}</td>'
            f'</tr>'
        )
    table_html = (
        '<table class="scan-table">'
        '<thead><tr>'
        '<th>Job Title</th><th>Company</th><th>Risk Level</th><th>Date</th>'
        '</tr></thead>'
        f'<tbody>{body_rows}</tbody>'
        '</table>'
    )
    st.markdown(table_html, unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# MAIN PAGE CONTENT
# ----------------------------------------------------------------------------
top_header("Dashboard", "AI-powered fraud analysis for job postings")

# HERO SECTION
st.markdown(f"""
<div class="hero-card">
    <div class="hero-left">
        <div class="hero-badge">MACHINE LEARNING · NLP</div>
        <h1>AI Powered Fake Job Posting Detector</h1>
        <p>Protecting job seekers from employment fraud using Machine Learning and Natural Language Processing.</p>
    </div>
    <div class="hero-icon-wrap">🛡️</div>
</div>
""", unsafe_allow_html=True)

# STATISTICS CARDS
metrics = [
    ("Total Jobs Scanned", "1,250", "📄", PRIMARY, "#EFF6FF", "▲ 8.2% this week", SUCCESS),
    ("High Risk Jobs", "152", "🚫", DANGER, "#FEF2F2", "▲ 3.1% this week", DANGER),
    ("Medium Risk Jobs", "287", "⚠️", WARNING, "#FFFBEB", "▼ 1.4% this week", SUCCESS),
    ("Low Risk Jobs", "811", "✅", SUCCESS, "#ECFDF5", "▲ 5.6% this week", SUCCESS),
]
cols = st.columns(4)
for col, (title, value, icon, color, bg, trend, trend_color) in zip(cols, metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon" style="background:{bg}; color:{color};">{icon}</div>
            <p class="metric-title">{title}</p>
            <p class="metric-value">{value}</p>
            <p class="metric-trend" style="color:{trend_color};">{trend}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# SCAN JOB FORM (left) + AI RESULT PANEL (right)
left_col, right_col = st.columns([1.5, 1])

with left_col:
    st.markdown("""<div class="jsa-card">""", unsafe_allow_html=True)
    st.markdown('<p class="section-title">Scan New Job Posting</p><p class="section-subtitle">Fill in as much detail as possible for a more accurate fraud score</p>', unsafe_allow_html=True)

    title = st.text_input("Job Title", placeholder="e.g. Senior Data Analyst")
    company = st.text_input("Company Name", placeholder="e.g. Nexora Analytics Pvt Ltd")
    description = st.text_area("Job Description", placeholder="Paste the full job description here...", height=120)
    requirements = st.text_area("Requirements", placeholder="e.g. Bachelor's degree, 2+ years experience...", height=100)
    benefits = st.text_area("Benefits", placeholder="e.g. Health insurance, paid leave, flexible hours...", height=100)
    salary = st.text_input("Salary Range", placeholder="e.g. ₹6,00,000 - ₹9,00,000 / year")
    remote = st.checkbox("This is a Remote Job")

    analyze_clicked = st.button("🔎  Analyze Job Posting", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if analyze_clicked:
        if not title:
            st.warning("Please enter at least a job title before analyzing.")
        else:
            result = analyze_job(title, company, description, requirements, benefits, salary, remote)
            st.session_state.last_result = result
            st.session_state.scan_history.insert(0, {
                "Job Title": title,
                "Company": company or "Not specified",
                "Risk Level": result["risk_level"].replace(" RISK", "").title() + " Risk",
                "Date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
            })
            st.rerun()

with right_col:
    st.markdown("""<div class="jsa-card">""", unsafe_allow_html=True)
    st.markdown('<p class="section-title">AI Analysis Result</p><p class="section-subtitle">Fraud Score · Risk Level · Recommendation</p>', unsafe_allow_html=True)

    if st.session_state.last_result:
        result = st.session_state.last_result
        render_animated_gauge(result["score"], result["risk_color"])

        pill_class = "pill-high" if "HIGH" in result["risk_level"] else ("pill-medium" if "MEDIUM" in result["risk_level"] else "pill-low")
        st.markdown(f"""
        <div style="text-align:center; margin-top:8px; margin-bottom:14px;">
            <span class="risk-pill {pill_class}">{result['risk_level']}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="reco-box" style="background:{result['risk_color']}12; border-left-color:{result['risk_color']}; color:{TEXT_DARK};">
            <strong>Recommendation:</strong> {result['recommendation']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"<p style='font-weight:700; margin-top:16px; margin-bottom:6px; color:{TEXT_DARK};'>Detected Risk Factors</p>", unsafe_allow_html=True)
        badges_html = ""
        for factor, kind in result["factors"]:
            cls = f"badge-{kind}"
            icon = "🚫" if kind == "danger" else ("⚠️" if kind == "warning" else "✅")
            badges_html += f'<span class="badge {cls}">{icon} {factor}</span>'
        st.markdown(f"<div>{badges_html}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align:center; padding:44px 10px; color:#94A3B8;">
            <div style="font-size:42px; margin-bottom:12px;">🛡️</div>
            <p style="font-size:14px;">Submit a job posting on the left to see the AI fraud score, risk level, and recommendation here.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# CHARTS: RISK DISTRIBUTION PIE + FRAUD TREND LINE
b1, b2 = st.columns([1, 1.3])

with b1:
    st.markdown("""<div class="jsa-card">""", unsafe_allow_html=True)
    st.markdown('<p class="section-title">Risk Distribution</p><p class="section-subtitle">Share of postings by risk category</p>', unsafe_allow_html=True)
    total_scanned = 152 + 287 + 811
    fig_pie = px.pie(
        names=["High Risk", "Medium Risk", "Low Risk"],
        values=[152, 287, 811],
        hole=0.62,
        color=["High Risk", "Medium Risk", "Low Risk"],
        color_discrete_map={"High Risk": DANGER, "Medium Risk": WARNING, "Low Risk": SUCCESS},
    )
    fig_pie.update_traces(textinfo="percent", textfont_size=12, marker=dict(line=dict(color="white", width=2)))
    fig_pie.update_layout(
        margin=dict(l=10, r=10, t=10, b=10), height=290,
        legend=dict(orientation="h", y=-0.15),
        annotations=[dict(text=f"<b>{total_scanned}</b><br><span style='font-size:11px;color:#64748B'>Total Scanned</span>",
                           x=0.5, y=0.5, showarrow=False, font_size=20)]
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with b2:
    st.markdown("""<div class="jsa-card">""", unsafe_allow_html=True)
    st.markdown('<p class="section-title">Fraud Trend</p><p class="section-subtitle">Detected high-risk postings — last 7 days</p>', unsafe_allow_html=True)
    days = [(datetime.now() - timedelta(days=i)).strftime("%a") for i in range(6, -1, -1)]
    values = [12, 18, 9, 22, 15, 27, 19]
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=days, y=values, mode="lines+markers",
        line=dict(color=PRIMARY, width=3, shape="spline"),
        marker=dict(size=8, color=PRIMARY, line=dict(color="white", width=2)),
        fill="tozeroy", fillcolor="rgba(37,99,235,0.08)"
    ))
    fig_trend.update_layout(
        margin=dict(l=10, r=10, t=10, b=10), height=290,
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor=BORDER),
        plot_bgcolor="white", paper_bgcolor="white"
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# RECENT SCANS TABLE
st.markdown("""<div class="jsa-card">""", unsafe_allow_html=True)
st.markdown('<p class="section-title">Recent Scans</p><p class="section-subtitle">Latest job postings analyzed by the engine</p>', unsafe_allow_html=True)
render_scan_table(st.session_state.scan_history)
st.markdown("</div>", unsafe_allow_html=True)