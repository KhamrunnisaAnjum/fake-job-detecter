# ================= app.py =================
# JobShield AI — Fake Job Posting Detector
# Frontend redesigned to a premium SaaS dashboard style.
# ML / auth / risk-rule logic is untouched — see "DO NOT MODIFY" section below.

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


# =====================================================================
# ===========================  CUSTOM CSS  ===========================
# =====================================================================
# All styling lives here so the page-rendering code below stays clean.

CUSTOM_CSS = """
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
    padding-top: 1.4rem;
    padding-bottom: 3rem;
    max-width: 1360px;
}

h1, h2, h3 {
    color: #111827;
    letter-spacing: -0.3px;
}

hr { border-color: #E5E7EB; }

/* ---------------- SIDEBAR ---------------- */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #EEF0F3;
}
section[data-testid="stSidebar"] > div {
    padding-top: 1.1rem;
}
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 2px 6px 18px 6px;
    border-bottom: 1px solid #EEF0F3;
    margin-bottom: 14px;
}
.sidebar-brand .brand-icon {
    width: 38px;
    height: 38px;
    min-width: 38px;
    border-radius: 11px;
    background: linear-gradient(135deg, #2563EB, #1D4ED8);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 18px;
    box-shadow: 0 4px 10px rgba(37,99,235,0.28);
}
.sidebar-brand h1 {
    font-size: 17px;
    font-weight: 700;
    color: #111827;
    margin: 0;
    line-height: 1.2;
}
.sidebar-brand p {
    font-size: 11.5px;
    color: #9CA3AF;
    margin: 1px 0 0 0;
}

.sidebar-note {
    background: #F8FAFC;
    border: 1px solid #EEF0F3;
    border-radius: 12px;
    padding: 12px 14px;
    margin-top: 16px;
}
.sidebar-note p {
    margin: 0;
    font-size: 12px;
    color: #6B7280;
    line-height: 1.5;
}

/* option_menu already themed via the `styles=` dict passed in Python */

/* ---------------- TOP BAR ---------------- */
.top-bar-wrap {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 14px;
    margin-bottom: 6px;
    border-bottom: 1px solid #F1F2F4;
}
div[data-testid="stTextInput"] input.search-input,
.top-search input {
    border-radius: 12px !important;
    background: #F8FAFC !important;
    border: 1px solid #EEF0F3 !important;
    font-size: 13.5px !important;
    height: 42px !important;
}
.icon-btn {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: #F8FAFC;
    border: 1px solid #EEF0F3;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    color: #4B5563;
    font-size: 17px;
}
.notif-badge {
    position: absolute;
    top: -6px;
    right: -6px;
    background: #EF4444;
    color: white;
    font-size: 10px;
    font-weight: 700;
    min-width: 17px;
    height: 17px;
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
    gap: 10px;
    padding: 4px 12px 4px 4px;
    border-radius: 999px;
    background: #F8FAFC;
    border: 1px solid #EEF0F3;
}
.user-chip .avatar {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: linear-gradient(135deg, #2563EB, #1D4ED8);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 700;
}
.user-chip .u-name {
    font-size: 13px;
    font-weight: 600;
    color: #111827;
    line-height: 1.1;
}
.user-chip .u-role {
    font-size: 11px;
    color: #9CA3AF;
    line-height: 1.1;
}

/* ---------------- HERO ---------------- */
.hero-card {
    display: flex;
    align-items: center;
    gap: 16px;
    border: 1px solid #EEF0F3;
    border-radius: 20px;
    background: linear-gradient(180deg, #F8FAFC 0%, #FFFFFF 100%);
    padding: 26px 30px;
    margin: 18px 0 26px 0;
}
.hero-card .hero-icon {
    width: 52px;
    height: 52px;
    min-width: 52px;
    border-radius: 14px;
    background: #EFF4FF;
    color: #2563EB;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
}
.hero-card h1 {
    font-size: 24px;
    font-weight: 800;
    margin: 0 0 4px 0;
}
.hero-card p {
    font-size: 14px;
    color: #6B7280;
    margin: 0;
}
.info-badge {
    display: inline-block;
    background: #EFF4FF;
    color: #2563EB;
    border: 1px solid #DBE6FE;
    border-radius: 999px;
    padding: 6px 13px;
    margin: 10px 6px 0 0;
    font-size: 12.5px;
    font-weight: 600;
}

/* ---------------- GENERIC CARD ---------------- */
.js-card {
    border: 1px solid #EEF0F3;
    border-radius: 18px;
    background: #FFFFFF;
    padding: 24px 26px;
    margin-bottom: 22px;
    box-shadow: 0 1px 2px rgba(16,24,40,0.03);
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.js-card:hover {
    box-shadow: 0 10px 24px rgba(16,24,40,0.07);
    transform: translateY(-2px);
}

/* ---------------- SECTION TITLES ---------------- */
.section-title {
    font-size: 16px;
    font-weight: 700;
    color: #111827;
    margin: 0 0 3px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-subtitle {
    font-size: 12.5px;
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
    border-color: #2563EB !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.10) !important;
}
label, .stCheckbox label p {
    font-weight: 600 !important;
    color: #374151 !important;
    font-size: 13px !important;
}

/* ---------------- BUTTONS ---------------- */
div.stButton > button {
    background: #2563EB !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 11px !important;
    height: 46px !important;
    font-weight: 600 !important;
    font-size: 14.5px !important;
    transition: background 0.15s ease, transform 0.15s ease;
}
div.stButton > button:hover {
    background: #1D4ED8 !important;
    transform: translateY(-1px);
}
div[data-testid="stDownloadButton"] > button {
    background: #FFFFFF !important;
    color: #2563EB !important;
    border: 1px solid #DBE6FE !important;
    border-radius: 11px !important;
    height: 46px !important;
    font-weight: 600 !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: #EFF4FF !important;
}

/* ---------------- METRIC CARDS ---------------- */
.metric-card {
    background: white;
    border: 1px solid #EEF0F3;
    border-radius: 18px;
    padding: 20px 22px;
    text-align: left;
    min-height: 128px;
    box-shadow: 0 1px 2px rgba(16,24,40,0.03);
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.metric-card:hover {
    box-shadow: 0 10px 24px rgba(16,24,40,0.07);
    transform: translateY(-3px);
}
.icon-circle {
    width: 46px;
    height: 46px;
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 19px;
    margin-bottom: 12px;
}
.icon-circle-blue   { background: #EFF4FF; color: #2563EB; }
.icon-circle-red    { background: #FEF2F2; color: #DC2626; }
.icon-circle-orange { background: #FFF7ED; color: #D97706; }
.icon-circle-green  { background: #ECFDF5; color: #059669; }

.metric-title {
    font-size: 12.5px;
    color: #6B7280;
    font-weight: 600;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}
.metric-value {
    font-size: 30px;
    font-weight: 800;
    color: #111827;
    line-height: 1.15;
}
.metric-trend {
    font-size: 12px;
    font-weight: 600;
    margin-top: 6px;
}
.trend-up { color: #059669; }
.trend-down { color: #DC2626; }
.trend-neutral { color: #9CA3AF; }

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

/* ---------------- RISK CHIPS ---------------- */
.flag-chip {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: #FEF2F2;
    color: #B91C1C;
    border: 1px solid #FECACA;
    border-radius: 12px;
    padding: 10px 14px;
    margin: 0 8px 8px 0;
    font-size: 13px;
    font-weight: 600;
}
.flag-chip-safe {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: #ECFDF5;
    color: #047857;
    border: 1px solid #A7F3D0;
    border-radius: 12px;
    padding: 10px 14px;
    margin-top: 6px;
    font-size: 13px;
    font-weight: 600;
}

.reco-box {
    border-radius: 14px;
    padding: 16px 18px;
    font-size: 13.5px;
    font-weight: 500;
    margin-top: 14px;
    border: 1px solid #EEF0F3;
    background: #F8FAFC;
    color: #111827;
}
.reco-box b { color: #111827; }

/* ---------------- RESULT / GAUGE CARD ---------------- */
.result-risk-line {
    display: flex;
    align-items: center;
    gap: 10px;
    justify-content: center;
    margin-top: -10px;
}
.result-risk-line .rlabel {
    font-size: 22px;
    font-weight: 800;
}
.rlabel-high { color: #DC2626; }
.rlabel-medium { color: #B45309; }
.rlabel-low { color: #15803D; }

.analysis-placeholder {
    text-align: center;
    padding: 40px 10px;
    color: #9CA3AF;
    font-size: 13.5px;
}
.analysis-placeholder .ph-icon {
    font-size: 30px;
    margin-bottom: 10px;
    color: #C7D2FE;
}

/* ---------------- TABLES ---------------- */
div[data-testid="stDataFrame"] {
    border: 1px solid #EEF0F3;
    border-radius: 14px;
    overflow: hidden;
}

/* ---------------- RECENT SCANS LIST ---------------- */
.scan-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 11px 2px;
    border-bottom: 1px solid #F4F5F7;
}
.scan-row:last-child { border-bottom: none; }
.scan-row .s-title {
    font-size: 13.5px;
    font-weight: 600;
    color: #111827;
}
.scan-row .s-time {
    font-size: 11.5px;
    color: #9CA3AF;
    margin-top: 1px;
}
.scan-row .s-right {
    text-align: right;
}

/* ---------------- RISK FACTOR INFO CARDS ---------------- */
.rf-card {
    border: 1px solid #EEF0F3;
    border-radius: 16px;
    padding: 18px 20px;
    background: #FFFFFF;
    height: 100%;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.rf-card:hover {
    box-shadow: 0 10px 24px rgba(16,24,40,0.07);
    transform: translateY(-2px);
}
.rf-card .rf-icon {
    width: 40px;
    height: 40px;
    border-radius: 11px;
    background: #FEF2F2;
    color: #DC2626;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 17px;
    margin-bottom: 10px;
}
.rf-card h4 {
    font-size: 14px;
    font-weight: 700;
    color: #111827;
    margin: 0 0 6px 0;
}
.rf-card p {
    font-size: 12.5px;
    color: #6B7280;
    line-height: 1.6;
    margin: 0;
}

</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Bootstrap Icons (used for crisp glyph icons throughout the dashboard)
st.markdown(
    '<link rel="stylesheet" '
    'href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">',
    unsafe_allow_html=True
)


# =====================================================================
# ==================  BACKEND — DO NOT MODIFY BELOW  ==================
# =====================================================================
# Model loading, prediction, risk-flag detection, CSV logging and
# recommendation thresholds are identical to the original, working
# backend. Only presentation code around these was changed.

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
# ====================  END OF PROTECTED BACKEND  ======================
# =====================================================================


# =====================================================================
# ========================  FRONTEND HELPERS  =========================
# =====================================================================
# Everything below is presentation-only: layout, charts, and small
# data aggregations over the existing CSV log. No ML/risk logic here.

RISK_COLORS = {
    "High Risk": "#EF4444",
    "Medium Risk": "#F59E0B",
    "Low Risk": "#10B981",
}

RISK_BADGE_CLASS = {
    "High Risk": "badge-high",
    "Medium Risk": "badge-medium",
    "Low Risk": "badge-low",
}

# Presentational icon mapping for the fixed set of strings returned by
# risk_rules.get_risk_flags() — purely cosmetic, does not touch the flags.
FLAG_ICON_MAP = {
    "No salary range provided": "bi-cash-coin",
    "Very little or no company information given": "bi-building",
    "Uses urgency-pressure language": "bi-alarm",
    "Asks for payment from applicant (major red flag)": "bi-credit-card",
    "Job description is unusually short": "bi-file-earmark-text",
}


def load_history():
    """Read the prediction log written by save_prediction(). Read-only."""
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.sort_values("timestamp")
        return df
    return pd.DataFrame(columns=["timestamp", "title", "risk", "score"])


def week_over_week(df, mask=None):
    """Compare row counts in the last 7 days vs the 7 days before that.
    Returns (label, direction) using only real data — no fabricated numbers."""
    if df.empty or "timestamp" not in df.columns:
        return "No data yet", "neutral"

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
        return f"{cur_n} new this week", "up"

    pct = round(((cur_n - prev_n) / prev_n) * 100, 1)
    if pct > 0:
        return f"↑ {pct}% from last week", "up"
    elif pct < 0:
        return f"↓ {abs(pct)}% from last week", "down"
    return "No change from last week", "neutral"


def time_ago(ts):
    """Human friendly relative time, e.g. '5 mins ago'."""
    if pd.isna(ts):
        return ""
    delta = pd.Timestamp.now() - ts
    seconds = delta.total_seconds()
    if seconds < 60:
        return "just now"
    if seconds < 3600:
        return f"{int(seconds // 60)} mins ago"
    if seconds < 86400:
        return f"{int(seconds // 3600)} hours ago"
    return f"{int(seconds // 86400)} days ago"


def metric_card(icon_class, color, title, value, trend_label=None, trend_dir="neutral"):
    trend_html = ""
    if trend_label:
        trend_html = f'<div class="metric-trend trend-{trend_dir}">{trend_label}</div>'

    st.markdown(f"""
    <div class="metric-card">
        <div class="icon-circle icon-circle-{color}"><i class="bi {icon_class}"></i></div>
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        {trend_html}
    </div>
    """, unsafe_allow_html=True)


def render_hero(icon_class, title, subtitle, badges=None):
    badges_html = ""
    if badges:
        badges_html = "".join(f'<span class="info-badge">{b}</span>' for b in badges)
        badges_html = f'<div>{badges_html}</div>'

    st.markdown(f"""
    <div class="hero-card">
        <div class="hero-icon"><i class="bi {icon_class}"></i></div>
        <div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
            {badges_html}
        </div>
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
        st.text_input(
            "Search",
            placeholder="🔍  Search scanned job titles...",
            label_visibility="collapsed",
            key="top_search"
        )

    with bell_col:
        badge = f'<span class="notif-badge">{high_today}</span>' if high_today > 0 else ""
        st.markdown(f"""
        <div class="icon-btn"><i class="bi bi-bell"></i>{badge}</div>
        """, unsafe_allow_html=True)

    with user_col:
        st.markdown("""
        <div class="user-chip">
            <div class="avatar">U</div>
            <div>
                <div class="u-name">User</div>
                <div class="u-role">Admin</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def risk_donut_chart(risk_count):
    labels = list(risk_count.index)
    values = list(risk_count.values)
    colors = [RISK_COLORS.get(r, "#9CA3AF") for r in labels]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.62,
        marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
        textinfo="none",
        sort=False,
    )])

    fig.update_layout(
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=230,
        annotations=[dict(
            text=f"<b>{sum(values)}</b><br><span style='font-size:11px;color:#9CA3AF'>Total</span>",
            x=0.5, y=0.5, showarrow=False, font=dict(size=20, color="#111827")
        )]
    )
    return fig


def fraud_score_chart(df):
    recent = df.dropna(subset=["timestamp"]).tail(30)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=recent["timestamp"],
        y=recent["score"],
        mode="lines+markers",
        line=dict(color="#2563EB", width=3, shape="spline"),
        marker=dict(size=6, color="#2563EB"),
        fill="tozeroy",
        fillcolor="rgba(37,99,235,0.08)",
    ))

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=230,
        xaxis=dict(showgrid=False),
        yaxis=dict(title="Fraud Score", showgrid=True, gridcolor="#F1F2F4", range=[0, 100]),
    )
    return fig


def fraud_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={'suffix': "%", 'font': {'size': 42, 'color': '#111827'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#E5E7EB'},
            'bar': {'color': "#2563EB"},
            'bgcolor': "white",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 30], 'color': "#DCFCE7"},
                {'range': [30, 60], 'color': "#FEF3C7"},
                {'range': [60, 100], 'color': "#FEE2E2"}
            ],
            'threshold': {
                'line': {'color': "#111827", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))

    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#111827")
    )
    return fig


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand">
            <div class="brand-icon"><i class="bi bi-shield-check"></i></div>
            <div>
                <h1>JobShield AI</h1>
                <p>Fake Job Detector</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        selected = option_menu(
            menu_title=None,
            options=[
                "Dashboard",
                "Scan New Job",
                "History",
                "Analytics",
                "Risk Factors",
                "Reports",
                "Settings",
                "About",
            ],
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
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#FFFFFF"},
                "icon": {"color": "#6B7280", "font-size": "15px"},
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "2px 0",
                    "padding": "10px 14px",
                    "border-radius": "10px",
                    "color": "#374151",
                    "--hover-color": "#F3F4F6",
                },
                "nav-link-selected": {
                    "background-color": "#2563EB",
                    "color": "white",
                    "font-weight": "600",
                },
            },
        )

        st.markdown("""
        <div class="sidebar-note">
            <p>🤖 Machine Learning + NLP based fraud detection system.</p>
        </div>
        """, unsafe_allow_html=True)

        return selected


# =====================================================================
# ============================  PAGES  ================================
# =====================================================================

def page_dashboard(df):
    render_hero(
        "bi-shield-check",
        "AI-Powered Fake Job Posting Detector",
        "Protecting job seekers from employment fraud using Machine Learning.",
    )

    if df.empty:
        st.markdown('<div class="js-card">', unsafe_allow_html=True)
        st.info("No predictions available yet. Run a scan from **Scan New Job** to populate the dashboard.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    total_jobs = len(df)
    high_n = len(df[df["risk"] == "High Risk"])
    medium_n = len(df[df["risk"] == "Medium Risk"])
    low_n = len(df[df["risk"] == "Low Risk"])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        label, direction = week_over_week(df)
        metric_card("bi-briefcase", "blue", "Total Jobs Scanned", total_jobs, label, direction)
    with c2:
        label, direction = week_over_week(df, df["risk"] == "High Risk")
        metric_card("bi-exclamation-triangle", "red", "High Risk Jobs", high_n, label, direction)
    with c3:
        label, direction = week_over_week(df, df["risk"] == "Medium Risk")
        metric_card("bi-shield-plus", "orange", "Medium Risk Jobs", medium_n, label, direction)
    with c4:
        label, direction = week_over_week(df, df["risk"] == "Low Risk")
        metric_card("bi-patch-check", "green", "Low Risk Jobs", low_n, label, direction)

    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        st.markdown('<div class="js-card">', unsafe_allow_html=True)
        st.markdown(
            '<p class="section-title"><i class="bi bi-pie-chart"></i> Risk Distribution</p>',
            unsafe_allow_html=True
        )
        risk_count = df["risk"].value_counts()
        st.plotly_chart(risk_donut_chart(risk_count), use_container_width=True, config={"displayModeBar": False})

        legend = ""
        for r in ["High Risk", "Medium Risk", "Low Risk"]:
            n = int(risk_count.get(r, 0))
            pct = round(n / total_jobs * 100, 1) if total_jobs else 0
            legend += (
                f'<div style="display:flex;align-items:center;gap:8px;margin-top:6px;font-size:13px;color:#374151;">'
                f'<span style="width:10px;height:10px;border-radius:50%;background:{RISK_COLORS[r]};display:inline-block;"></span>'
                f'{r} — {n} ({pct}%)</div>'
            )
        st.markdown(legend, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="js-card">', unsafe_allow_html=True)
        st.markdown(
            '<p class="section-title"><i class="bi bi-graph-up"></i> Fraud Score Trend</p>',
            unsafe_allow_html=True
        )
        st.plotly_chart(fraud_score_chart(df), use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="js-card">', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-title"><i class="bi bi-list-check"></i> Recent Scans</p>',
        unsafe_allow_html=True
    )
    for _, row in df.tail(6).iloc[::-1].iterrows():
        badge = RISK_BADGE_CLASS.get(row["risk"], "badge-low")
        st.markdown(f"""
        <div class="scan-row">
            <div>
                <div class="s-title">{row['title'] if str(row['title']).strip() else '(untitled posting)'}</div>
                <div class="s-time">{time_ago(row['timestamp'])}</div>
            </div>
            <div class="s-right">
                <span class="risk-badge {badge}">{row['risk']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def page_scan():
    render_hero(
        "bi-search",
        "Scan New Job Posting",
        "Analyze a job posting instantly and identify fraud risk before applying.",
        badges=["🤖 AI Powered", "⚡ Real-Time Analysis", "🛡️ ML + NLP"],
    )

    form_col, result_col = st.columns([1.15, 1])

    with form_col:
        st.markdown('<div class="js-card">', unsafe_allow_html=True)
        st.markdown(
            '<p class="section-title">Scan New Job Posting</p>'
            '<p class="section-subtitle">Fill in the job details below to analyze fraud risk</p>',
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2)
        with c1:
            title = st.text_input("Job Title *", placeholder="e.g. Python Developer")
        with c2:
            company = st.text_input("Company Name", placeholder="e.g. Microsoft")

        company_profile = st.text_area(
            "Company Profile", placeholder="Tell us about the company...", height=90
        )
        description = st.text_area(
            "Job Description *", placeholder="Paste the full job description here...", height=160
        )

        c3, c4 = st.columns(2)
        with c3:
            requirements = st.text_input("Requirements", placeholder="e.g. Python, SQL, Django...")
        with c4:
            salary = st.text_input("Salary Range", placeholder="e.g. 30000 - 50000")

        remote = st.checkbox("Is this a remote job?")

        analyze_clicked = st.button("✨ Analyze Job Posting", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with result_col:
        st.markdown('<div class="js-card">', unsafe_allow_html=True)
        st.markdown(
            '<p class="section-title"><i class="bi bi-clipboard-data"></i> AI Analysis Result</p>'
            '<p class="section-subtitle">Fraud probability score and detected risk factors</p>',
            unsafe_allow_html=True
        )

        if not analyze_clicked:
            st.markdown("""
            <div class="analysis-placeholder">
                <div class="ph-icon"><i class="bi bi-shield-lock"></i></div>
                Fill in the job details and click <b>Analyze Job Posting</b><br>to see the AI fraud analysis here.
            </div>
            """, unsafe_allow_html=True)

        elif description.strip() == "":
            st.warning("Please enter a job description before analyzing.")

        else:
            # ---- unchanged backend call ----
            result, probability = predict_job(
                title, company, description, requirements, salary
            )
            score = round(probability * 100, 2)

            if score >= 60:
                risk = "High Risk"
                badge_class = "badge-high"
                rlabel_class = "rlabel-high"
                recommendation = "Avoid applying until company legitimacy is verified."
            elif score >= 30:
                risk = "Medium Risk"
                badge_class = "badge-medium"
                rlabel_class = "rlabel-medium"
                recommendation = "Verify company details before applying."
            else:
                risk = "Low Risk"
                badge_class = "badge-low"
                rlabel_class = "rlabel-low"
                recommendation = "Appears safe but always verify independently."

            flags = get_risk_flags(
                title, description, salary, company_profile, remote
            )
            # ---- end unchanged backend call ----

            st.plotly_chart(fraud_gauge(score), use_container_width=True, config={"displayModeBar": False})

            st.markdown(f"""
            <div class="result-risk-line">
                <span class="rlabel {rlabel_class}">{risk.upper()}</span>
                <span class="risk-badge {badge_class}">{score}% Fraud Score</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                f'<div class="reco-box"><b>AI Recommendation:</b> {recommendation}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<p style="font-weight:700; margin-top:20px; margin-bottom:8px; color:#111827; font-size:13.5px;">Risk Factors Detected</p>',
                unsafe_allow_html=True
            )

            if flags:
                chips = ""
                for flag in flags:
                    icon = FLAG_ICON_MAP.get(flag, "bi-exclamation-circle")
                    chips += f'<span class="flag-chip"><i class="bi {icon}"></i> {flag}</span>'
                st.markdown(chips, unsafe_allow_html=True)
            else:
                st.markdown(
                    '<span class="flag-chip-safe"><i class="bi bi-check-circle"></i> No suspicious factors found</span>',
                    unsafe_allow_html=True
                )

            save_prediction(title, risk, score)

        st.markdown('</div>', unsafe_allow_html=True)


def page_history(df):
    render_hero(
        "bi-clock-history",
        "Prediction History",
        "Search and review all past predictions.",
    )

    st.markdown('<div class="js-card">', unsafe_allow_html=True)

    if df.empty:
        st.info("No prediction history found yet.")
    else:
        search_col, download_col = st.columns([3, 1])
        with search_col:
            search_term = st.text_input(
                "Search", placeholder="🔍  Search by job title", label_visibility="collapsed"
            )
        with download_col:
            st.download_button(
                label="⬇️ Download CSV",
                data=df.to_csv(index=False),
                file_name="jobshield_history.csv",
                mime="text/csv",
                use_container_width=True,
            )

        filtered = df
        if search_term:
            filtered = df[df["title"].astype(str).str.contains(search_term, case=False, na=False)]

        st.dataframe(filtered.sort_values("timestamp", ascending=False), use_container_width=True, hide_index=True)

    st.markdown('</div>', unsafe_allow_html=True)


def page_analytics(df):
    render_hero(
        "bi-bar-chart-line",
        "Analytics",
        "Deeper trends across every job posting scanned so far.",
    )

    if df.empty:
        st.markdown('<div class="js-card">', unsafe_allow_html=True)
        st.info("No data to analyze yet. Scan a few job postings first.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    valid = df.dropna(subset=["timestamp"]).copy()
    valid["date"] = valid["timestamp"].dt.date

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("bi-clipboard-data", "blue", "Total Scans", len(df))
    with c2:
        metric_card("bi-percent", "orange", "Average Fraud Score", f"{round(df['score'].mean(), 1)}%")
    with c3:
        metric_card("bi-graph-up-arrow", "red", "Highest Score", f"{round(df['score'].max(), 1)}%")
    with c4:
        metric_card("bi-graph-down-arrow", "green", "Lowest Score", f"{round(df['score'].min(), 1)}%")

    left, right = st.columns(2)
    with left:
        st.markdown('<div class="js-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-title"><i class="bi bi-calendar3"></i> Scans Per Day</p>', unsafe_allow_html=True)
        daily = valid.groupby("date").size()
        fig = go.Figure(go.Bar(
            x=[str(d) for d in daily.index], y=daily.values,
            marker_color="#2563EB", marker_line_width=0,
        ))
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10), height=260,
            yaxis=dict(gridcolor="#F1F2F4"),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="js-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-title"><i class="bi bi-bar-chart-steps"></i> Average Score by Risk Level</p>', unsafe_allow_html=True)
        avg_by_risk = df.groupby("risk")["score"].mean().reindex(["Low Risk", "Medium Risk", "High Risk"]).dropna()
        fig = go.Figure(go.Bar(
            x=avg_by_risk.index, y=avg_by_risk.values,
            marker_color=[RISK_COLORS.get(r, "#9CA3AF") for r in avg_by_risk.index],
            text=[f"{v:.1f}%" for v in avg_by_risk.values], textposition="outside",
        ))
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10), height=260,
            yaxis=dict(gridcolor="#F1F2F4", range=[0, 100]), showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)


def page_risk_factors():
    render_hero(
        "bi-shield-exclamation",
        "Risk Factors",
        "The signals JobShield AI's heuristic engine checks on every job posting.",
    )

    cards = [
        ("bi-cash-coin", "Missing Salary Range",
         "Postings that don't specify a salary range can be hiding unrealistic or exploitative pay."),
        ("bi-building", "Insufficient Company Information",
         "Legitimate employers usually provide a real company profile. Vague or missing details are a common scam signal."),
        ("bi-alarm", "Urgency-Pressure Language",
         "Phrases like 'urgent', 'immediate joining' or 'act now' are used to rush applicants into a decision."),
        ("bi-credit-card", "Requests Payment From Applicant",
         "Genuine employers never ask candidates to pay a registration, processing, or deposit fee."),
        ("bi-file-earmark-text", "Unusually Short Description",
         "Fraudulent postings are often short on detail, because the job doesn't actually exist."),
    ]

    st.markdown('<div class="js-card">', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-title">How Scans Are Scored</p>'
        '<p class="section-subtitle" style="margin-bottom:0;">'
        'Every posting is scored by the ML classifier (fraud probability) and cross-checked against these '
        'rule-based signals, which appear as risk factor chips in your analysis results.</p>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    for i, (icon, name, desc) in enumerate(cards):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="rf-card">
                <div class="rf-icon"><i class="bi {icon}"></i></div>
                <h4>{name}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)


def page_reports(df):
    render_hero(
        "bi-file-earmark-text",
        "Reports",
        "Summary statistics and exportable data across all scans.",
    )

    if df.empty:
        st.markdown('<div class="js-card">', unsafe_allow_html=True)
        st.info("No data available yet to build a report.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    total_jobs = len(df)
    high_n = len(df[df["risk"] == "High Risk"])
    medium_n = len(df[df["risk"] == "Medium Risk"])
    low_n = len(df[df["risk"] == "Low Risk"])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("bi-briefcase", "blue", "Total Jobs Scanned", total_jobs)
    with c2:
        metric_card("bi-exclamation-triangle", "red", "High Risk", high_n)
    with c3:
        metric_card("bi-shield-plus", "orange", "Medium Risk", medium_n)
    with c4:
        metric_card("bi-patch-check", "green", "Low Risk", low_n)

    st.markdown('<div class="js-card">', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-title"><i class="bi bi-table"></i> Full Scan Log</p>'
        '<p class="section-subtitle">Export the complete history for offline reporting.</p>',
        unsafe_allow_html=True
    )
    st.download_button(
        label="⬇️ Download Full Report (CSV)",
        data=df.to_csv(index=False),
        file_name="jobshield_full_report.csv",
        mime="text/csv",
        use_container_width=True,
    )
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)


def page_settings():
    render_hero(
        "bi-gear",
        "Settings",
        "Customize your JobShield AI experience.",
    )
    st.markdown('<div class="js-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-title">More settings coming soon</p>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#6B7280; font-size:13.5px;">This section is reserved for future preferences '
        '(notification thresholds, export defaults, and account management).</p>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)


def page_about():
    render_hero(
        "bi-info-circle",
        "About This Project",
        "Machine Learning powered fake job posting detection using NLP and Logistic Regression.",
    )

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


# =====================================================================
# ===========================  MAIN ROUTER  ============================
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