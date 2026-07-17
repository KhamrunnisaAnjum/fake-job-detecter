# ================= app.py =================
# JobShield AI — Privacy-First Personal Edition

from streamlit_option_menu import option_menu
from auth import login
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import joblib, os, re, csv, io
from datetime import datetime, date

from preprocess import clean_text          # UNCHANGED
from risk_rules import get_risk_flags      # UNCHANGED
from db import init_db, save_scan, get_user_scans, delete_scan, \
               get_user_by_id, update_password

# ── Page config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="JobShield AI | Personal Console",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── DB init ──────────────────────────────────────────────────────────
init_db()

# ── Session defaults ─────────────────────────────────────────────────
if "logged_in"  not in st.session_state: st.session_state.logged_in  = False
if "menu_selection" not in st.session_state: st.session_state.menu_selection = "Dashboard"
if "user_id"    not in st.session_state: st.session_state.user_id    = None
if "username"   not in st.session_state: st.session_state.username   = ""
if "email"      not in st.session_state: st.session_state.email      = ""

if not st.session_state.logged_in:
    login()
    st.stop()

# =====================================================================
# ===========================  GLOBAL CSS  ============================
# =====================================================================
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important; }
.stApp { background-color: #FFFFFF !important; }
#MainMenu, footer { visibility: hidden !important; }
header[data-testid="stHeader"] { background: transparent !important; }
header[data-testid="stHeader"] > div:first-child { visibility: hidden !important; }
button[data-testid="stSidebarCollapsedControl"],
div[data-testid="stSidebarCollapsedControl"] {
    visibility: visible !important; display: flex !important;
    opacity: 1 !important; z-index: 999999 !important;
}
.block-container { padding-top:1.5rem !important; padding-bottom:4rem !important; max-width:1200px !important; }
h1,h2,h3,h4,h5,h6 { color:#0F172A !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; letter-spacing:-.025em !important; }
hr { border-color:#F4F4F5 !important; }

/* SIDEBAR */
section[data-testid="stSidebar"] { width:240px !important; min-width:240px !important; max-width:240px !important; background-color:#FFFFFF !important; border-right:1px solid #E4E4E7 !important; }
section[data-testid="stSidebar"] > div { padding-top:1.25rem !important; padding-left:10px !important; padding-right:10px !important; }
.workspace-selector { display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:6px;background:#F4F4F5;border:1px solid #E4E4E7;margin-bottom:16px;cursor:pointer; }
.workspace-avatar { width:28px;height:28px;border-radius:5px;background:#0F172A;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px; }
.workspace-info { flex-grow:1;display:flex;flex-direction:column;gap:1px; }
.workspace-name { font-size:13px;font-weight:600;color:#0F172A;letter-spacing:-.01em; }
.workspace-plan { font-size:10px;color:#71717A;font-weight:500; }
.sidebar-note { background:#FAFAFA;border:1px solid #E4E4E7;border-radius:6px;padding:10px 12px;margin-top:20px; }
.sidebar-note p { margin:0;font-size:11.5px;color:#71717A;line-height:1.45; }

/* TOP BAR */
.breadcrumbs { display:flex;align-items:center;gap:8px;font-size:13px;font-weight:500; }
.bc-parent { color:#71717A; } .bc-separator { color:#D4D4D8; } .bc-active { color:#0F172A;font-weight:600; }
.icon-btn { width:34px;height:34px;border-radius:6px;background:#FFFFFF;border:1px solid #E4E4E7;display:flex;align-items:center;justify-content:center;position:relative;color:#52525B;font-size:15px; }
.notif-badge { position:absolute;top:-4px;right:-4px;background:#EF4444;color:white;font-size:8.5px;font-weight:700;min-width:14px;height:14px;border-radius:999px;display:flex;align-items:center;justify-content:center;padding:0 3px;border:2px solid white; }
.user-chip { display:flex;align-items:center;gap:8px;padding:3px 10px 3px 3px;border-radius:999px;background:#F4F4F5;border:1px solid #E4E4E7; }
.user-chip .avatar { width:26px;height:26px;border-radius:50%;background:#0F172A;color:white;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700; }
.user-chip .u-name { font-size:11px;font-weight:600;color:#0F172A;line-height:1.1; }
.user-chip .u-role { font-size:9.5px;color:#71717A;line-height:1.1; }

/* HERO */
.dashboard-hero { padding:32px 0 24px 0; }
.hero-badge { display:inline-flex;align-items:center;background:#EFF6FF;color:#1D4ED8;border:1px solid #DBEAFE;padding:4px 10px;border-radius:9999px;font-size:11px;font-weight:600;letter-spacing:.05em;margin-bottom:16px; }
.hero-title { font-size:36px !important;font-weight:850 !important;color:#0F172A !important;letter-spacing:-.035em !important;line-height:1.15 !important;margin-bottom:14px !important;max-width:720px; }
.hero-desc { font-size:15.5px;color:#52525B;line-height:1.6;max-width:680px;margin-bottom:24px;font-weight:400; }
.trust-indicator-row { display:flex;gap:24px;margin-top:28px;padding-top:24px;border-top:1px solid #F4F4F5; }
.trust-item { font-size:12px;color:#71717A;font-weight:500;display:flex;align-items:center;gap:6px; }

/* PAGE HEADER */
.page-header { margin-bottom:24px;padding-bottom:10px; }
.page-header h1 { font-size:24px;font-weight:750;color:#0F172A;margin:0 0 6px 0;letter-spacing:-.025em; }
.page-header p { font-size:14px;color:#52525B;margin:0;line-height:1.5; }

/* CARDS */
.main div[data-testid="stVerticalBlockBorderWrapper"] { background-color:#FFFFFF !important;border:1px solid #E4E4E7 !important;border-radius:8px !important;padding:20px !important;box-shadow:0 1px 3px rgba(0,0,0,0.04) !important;transition:all 0.15s ease-in-out !important; }
.section-title { font-size:14.5px;font-weight:600;color:#0F172A;margin:0 0 4px 0;display:flex;align-items:center;gap:8px; }
.section-subtitle { font-size:12px;color:#71717A;margin:0 0 16px 0; }

/* INPUTS */
.stTextInput input,.stTextArea textarea { border-radius:6px !important;border:1px solid #E4E4E7 !important;background:#FFFFFF !important;font-size:13.5px !important;color:#0F172A !important; }
.stTextInput input:focus,.stTextArea textarea:focus { border-color:#0F172A !important;box-shadow:0 0 0 2px rgba(15,23,42,0.05) !important; }
label,.stCheckbox label p { font-weight:500 !important;color:#27272A !important;font-size:12.5px !important;margin-bottom:4px !important; }

/* BUTTONS */
div.stButton > button { border-radius:6px !important;height:38px !important;font-weight:550 !important;font-size:13.5px !important;letter-spacing:-.01em !important;transition:all 0.15s ease !important;box-shadow:0 1px 2px rgba(0,0,0,0.05) !important; }
div[data-testid="stBaseButton-primary"] { background-color:#0F172A !important;color:#FFFFFF !important;border:1px solid #0F172A !important; }
div[data-testid="stBaseButton-primary"]:hover { background-color:#1E293B !important;transform:translateY(-1px) !important;box-shadow:0 4px 12px rgba(15,23,42,0.08) !important; }
div[data-testid="stBaseButton-secondary"] { background-color:#FFFFFF !important;color:#0F172A !important;border:1px solid #E4E4E7 !important; }
div[data-testid="stDownloadButton"]>button { background:#FFFFFF !important;color:#0F172A !important;border:1px solid #E4E4E7 !important;border-radius:6px !important;height:38px !important;font-weight:550 !important;font-size:13.5px !important; }

/* METRICS */
.metric-card { background:#FFFFFF;border:1px solid #E4E4E7;border-radius:8px;padding:18px;box-shadow:0 1px 3px rgba(0,0,0,0.04);transition:all 0.15s ease-in-out;min-height:110px;display:flex;flex-direction:column;justify-content:space-between; }
.metric-header { display:flex;align-items:center;justify-content:space-between;margin-bottom:6px; }
.metric-title { font-size:11.5px;font-weight:600;color:#71717A;text-transform:uppercase;letter-spacing:.05em; }
.metric-icon-wrap { width:26px;height:26px;border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:12px; }
.metric-icon-blue{background:#EFF6FF;color:#3B82F6;} .metric-icon-red{background:#FEF2F2;color:#EF4444;} .metric-icon-orange{background:#FFF7ED;color:#F59E0B;} .metric-icon-green{background:#ECFDF5;color:#10B981;}
.metric-value { font-size:24px;font-weight:700;color:#0F172A;letter-spacing:-.025em;line-height:1.1;margin:2px 0; }
.metric-footer { display:flex;align-items:center;gap:6px;font-size:11.5px;font-weight:500;margin-top:4px; }
.trend-up{color:#15803D;background:#DCFCE7;padding:1px 5px;border-radius:4px;} .trend-down{color:#B91C1C;background:#FEE2E2;padding:1px 5px;border-radius:4px;} .trend-neutral{color:#52525B;background:#F4F4F5;padding:1px 5px;border-radius:4px;} .trend-text{color:#71717A;}

/* SCAN FEED */
.scan-item{display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid #F4F4F5;}
.scan-item:last-child{border-bottom:none;}
.scan-avatar{width:30px;height:30px;border-radius:5px;background:#F4F4F5;color:#0F172A;border:1px solid #E4E4E7;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:12px;}
.scan-details{flex-grow:1;display:flex;flex-direction:column;gap:1px;}
.scan-title{font-size:13px;font-weight:600;color:#0F172A;}
.scan-meta{font-size:11px;color:#71717A;display:flex;align-items:center;gap:6px;}

/* RISK BADGES */
.security-badge{display:inline-flex;align-items:center;gap:6px;padding:3px 8px;border-radius:9999px;font-size:10.5px;font-weight:600;text-transform:uppercase;letter-spacing:.04em;border:1px solid transparent;}
.badge-high{background:#FEF2F2;color:#991B1B;border-color:#FEE2E2;}
.badge-medium{background:#FFFBEB;color:#92400E;border-color:#FEF3C7;}
.badge-low{background:#F0FDF4;color:#166534;border-color:#DCFCE7;}
.factor-pill{display:inline-flex;align-items:center;gap:6px;background:#F4F4F5;border:1px solid #E4E4E7;border-radius:6px;padding:5px 10px;font-size:12px;font-weight:500;color:#18181B;margin-right:6px;margin-bottom:6px;}
.factor-critical{background:#FEF2F2 !important;border-color:#FEE2E2 !important;color:#991B1B !important;}
.recommendation-box{background:#FAFAFA;border:1px solid #E4E4E7;border-radius:6px;padding:14px 16px;margin-top:14px;display:flex;gap:10px;align-items:flex-start;}
.reco-icon-wrap{color:#71717A;font-size:15px;margin-top:1px;}
.reco-content{display:flex;flex-direction:column;gap:2px;}
.reco-title{font-size:12.5px;font-weight:600;color:#0F172A;}
.reco-text{font-size:12px;color:#52525B;line-height:1.45;}

/* SCORE RING */
.security-indicator{text-align:center;padding:10px 0;}
.security-score-circle{position:relative;display:inline-flex;align-items:center;justify-content:center;width:130px;height:130px;border-radius:50%;background:#FFFFFF;border:8px solid #F4F4F5;margin-bottom:12px;box-shadow:inset 0 1px 3px rgba(0,0,0,0.02),0 4px 16px rgba(0,0,0,0.06);}
.score-high{border-color:#FEE2E2;color:#EF4444;} .score-medium{border-color:#FEF3C7;color:#F59E0B;} .score-low{border-color:#DCFCE7;color:#10B981;}
.security-score-val{font-size:34px;font-weight:800;letter-spacing:-.03em;}
.security-score-pct{font-size:14px;font-weight:600;color:#71717A;}
.analysis-placeholder{text-align:center;padding:60px 10px;color:#A1A1AA;font-size:13px;}
.analysis-placeholder .ph-icon{font-size:36px;margin-bottom:12px;color:#E4E4E7;}
.scan-source-chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px;}
.source-chip{display:inline-flex;align-items:center;gap:5px;background:#F4F4F5;border:1px solid #E4E4E7;border-radius:999px;padding:3px 10px;font-size:11.5px;font-weight:500;color:#52525B;}
.info-table{width:100%;border-collapse:collapse;margin-top:10px;}
.info-table td{padding:8px 10px;font-size:12.5px;border-bottom:1px solid #F4F4F5;vertical-align:top;}
.info-table td:first-child{font-weight:600;color:#52525B;white-space:nowrap;width:130px;}
.info-table td:last-child{color:#0F172A;word-break:break-word;}
.info-table tr:last-child td{border-bottom:none;}
div[data-testid="stDataFrame"]{border:1px solid #E4E4E7 !important;border-radius:6px !important;overflow:hidden !important;}

/* ABOUT */
.about-hero{text-align:center;padding:24px 0 32px 0;border-bottom:1px solid #F4F4F5;margin-bottom:24px;}
.about-hero h2{font-size:28px;font-weight:850;color:#0F172A;letter-spacing:-.03em;margin-bottom:8px;}
.about-hero p{font-size:15px;color:#52525B;max-width:560px;margin:0 auto;line-height:1.55;}
.grid-3col{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:24px;}
.about-card{background:#FFFFFF;border:1px solid #E4E4E7;border-radius:6px;padding:20px;}
.about-card-icon{width:34px;height:34px;border-radius:5px;background:#F4F4F5;color:#0F172A;display:flex;align-items:center;justify-content:center;font-size:14px;margin-bottom:14px;border:1px solid #E4E4E7;}
.about-card h3{font-size:14.5px;font-weight:600;color:#0F172A;margin:0 0 6px 0;}
.about-card p{font-size:12.5px;color:#52525B;line-height:1.5;margin:0;}
.about-footer{text-align:center;padding-top:20px;font-size:12px;color:#71717A;border-top:1px solid #F4F4F5;}

/* Premium Popover Styling for Notification Bell */
div[data-testid="column"]:nth-child(2) div[data-testid="stPopover"] > button {
    width: 34px !important;
    height: 34px !important;
    min-width: 34px !important;
    max-width: 34px !important;
    border-radius: 6px !important;
    background: #FFFFFF !important;
    border: 1px solid #E4E4E7 !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    color: #52525B !important;
    position: relative !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    cursor: pointer !important;
}
div[data-testid="column"]:nth-child(2) div[data-testid="stPopover"] > button::after {
    font-family: "bootstrap-icons" !important;
    content: "\\F18A" !important;
    font-size: 15px !important;
    font-style: normal !important;
    font-weight: normal !important;
    font-variant: normal !important;
    text-transform: none !important;
    line-height: 1 !important;
    -webkit-font-smoothing: antialiased !important;
}
div[data-testid="column"]:nth-child(2) div[data-testid="stPopover"] > button div[data-testid="stMarkdownContainer"] {
    display: none !important;
}
div[data-testid="column"]:nth-child(2) div[data-testid="stPopover"] > button svg {
    display: none !important;
}
div[data-testid="column"]:nth-child(2) div[data-testid="stPopover"] > button:hover {
    background: #F4F4F5 !important;
    border-color: #D4D4D8 !important;
}
</style>
"""

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">',
    unsafe_allow_html=True
)

# =====================================================================
# ===========================  BACKEND  ===============================
# =====================================================================

classifier = joblib.load("model/classifier.pkl")   # UNCHANGED
vectorizer = joblib.load("model/vectorizer.pkl")   # UNCHANGED

RISK_COLORS = {"High Risk": "#EF4444", "Medium Risk": "#F59E0B", "Low Risk": "#10B981"}

FLAG_ICON_MAP = {
    "No salary range provided": "bi-cash-coin",
    "Very little or no company information given": "bi-building",
    "Uses urgency-pressure language": "bi-alarm",
    "Asks for payment from applicant (major red flag)": "bi-credit-card",
    "Job description is unusually short": "bi-file-earmark-text",
}


def predict_job(title, company, description, requirements, salary):
    """Original ML prediction — completely unchanged."""
    text = " ".join([title, company, description, requirements, salary])
    cleaned = clean_text(text)
    vector = vectorizer.transform([cleaned])
    probability = classifier.predict_proba(vector)[0][1]
    prediction = classifier.predict(vector)[0]
    return ("Fake Job" if prediction == 1 else "Real Job"), probability


def analyze_message_rules(text):
    flags = []
    t = text.lower()
    if re.search(r'chat\.whatsapp\.com|wa\.me|whatsapp', t):
        flags.append(("bi-whatsapp", "Redirects users to WhatsApp group/link", True))
    if re.search(r't\.me/|telegram\.me|join.*telegram|telegram.*group', t):
        flags.append(("bi-telegram", "Redirects users to Telegram", True))
    if re.search(r'bit\.ly|tinyurl|goo\.gl|ow\.ly|t\.co|cutt\.ly|rb\.gy|shorturl', t):
        flags.append(("bi-link-45deg", "Uses suspicious shortened URLs", True))
    if re.search(r'@gmail\.com|@yahoo\.com|@hotmail\.com|@outlook\.com', t):
        flags.append(("bi-envelope-exclamation", "Uses personal email instead of company domain", True))
    urgency = [r'limited seats?',r'limited slots?',r'hurry',r'act now',r'apply immediately',r'urgent(ly)?',r'last (few|chance)',r"don'?t miss",r'register (now|today|fast)']
    if any(re.search(p, t) for p in urgency):
        flags.append(("bi-alarm", "Uses urgency / pressure language", False))
    payment = [r'registration fee',r'processing fee',r'security deposit',r'advance payment',r'pay to (apply|join|register)',r'deposit (required|needed)',r'qr code',r'upi id',r'send money',r'pay ₹',r'crypto(currency)?',r'bitcoin']
    if any(re.search(p, t) for p in payment):
        flags.append(("bi-credit-card-2-front", "Requests payment from applicant — major red flag", True))
    earn = [r'earn ₹\s*\d{4,}',r'₹\s*\d+[,\d]*\s*(per|/)\s*(week|day|month)',r'earn upto',r'unlimited (earning|income)',r'guaranteed (income|salary|pay)',r'100% (placement|job guarantee)']
    if any(re.search(p, t) for p in earn):
        flags.append(("bi-currency-rupee", "Promises unrealistic / guaranteed earnings", True))
    brands = ['ibm','microsoft','google','amazon','apple','facebook','meta','infosys','tcs','wipro','accenture','iit','iim','reliance','hdfc','icici','flipkart']
    found = [b for b in brands if re.search(r'\b'+b+r'\b', t)]
    if found:
        flags.append(("bi-building-exclamation", f"Mentions famous brands — possible impersonation: {', '.join(found[:3]).upper()}", True))
    salary_kw = [r'salary',r'stipend',r'pay',r'compensation',r'₹',r'lpa',r'ctc',r'per\s*(month|annum|year)']
    if not any(re.search(p, t) for p in salary_kw):
        flags.append(("bi-cash-stack", "No salary or compensation mentioned", False))
    if re.search(r'certif(icate|ication|ied)', t):
        flags.append(("bi-award", "Promises certificate — common in scam internship ads", False))
    if re.search(r'work\s*from\s*home|wfh|remote', t):
        if re.search(r'no\s*(experience|exp)|fresher(s)?|0\s*(years?|yrs?)', t):
            flags.append(("bi-house-exclamation", "WFH + no experience required — common scam pattern", False))
    if len(text.split()) < 40:
        flags.append(("bi-file-earmark-x", "Message is unusually short — very little information provided", False))
    return flags


def extract_info(text):
    info = {}
    emails = re.findall(r'[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}', text)
    info['email'] = ', '.join(emails[:3]) if emails else None
    phones = re.findall(r'(?:\+91[\-\s]?)?[6-9]\d{9}', text)
    info['phone'] = ', '.join(phones[:3]) if phones else None
    urls = re.findall(r'https?://[^\s\)\>]+', text)
    non_social = [u for u in urls if not any(x in u for x in ['whatsapp','t.me','telegram'])]
    info['website'] = non_social[0] if non_social else None
    wa = re.findall(r'https?://chat\.whatsapp\.com/[^\s\)\>]+', text)
    tg = re.findall(r'https?://t\.me/[^\s\)\>]+', text)
    parts = []
    if wa: parts.append(f"WhatsApp Group ({len(wa)})")
    if tg: parts.append(f"Telegram ({len(tg)})")
    info['contact'] = ', '.join(parts) if parts else None
    sal = re.search(r'(?:salary|stipend|pay|ctc)[:\s]*([₹\d,\.]+\s*(?:lpa|per\s*(?:month|annum|year|week)|k)?)', text, re.IGNORECASE)
    if not sal:
        sal = re.search(r'₹\s*[\d,]+(?:\s*-\s*₹?\s*[\d,]+)?(?:\s*(?:lpa|per\s*\w+))?', text)
    info['salary'] = sal.group(0).strip() if sal else None
    big_brands = ['IBM','Microsoft','Google','Amazon','Apple','Facebook','Meta','Infosys','TCS','Wipro','Accenture','IIT','IIM','Reliance','HDFC','ICICI','Flipkart']
    found_brands = [b for b in big_brands if re.search(r'\b'+b+r'\b', text, re.IGNORECASE)]
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
# ========================  HELPERS  ==================================
# =====================================================================

def week_over_week(df, mask=None):
    if df.empty or "created_at" not in df.columns: return "No scans yet", "neutral"
    working = df[mask] if mask is not None else df
    working = working.dropna(subset=["created_at"])
    now = pd.Timestamp.now()
    cur_n  = len(working[working["created_at"] >= now - pd.Timedelta(days=7)])
    prev_n = len(working[(working["created_at"] >= now - pd.Timedelta(days=14)) & (working["created_at"] < now - pd.Timedelta(days=7))])
    if prev_n == 0: return (f"{cur_n} new scans", "up") if cur_n else ("No data yet", "neutral")
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
    color_map = {"blue":"metric-icon-blue","red":"metric-icon-red","orange":"metric-icon-orange","green":"metric-icon-green"}
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
    st.markdown(f'<div class="page-header"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)


def render_top_bar(page_label, df):
    high_today = 0
    if not df.empty:
        today = pd.Timestamp.now().normalize()
        r = df.dropna(subset=["created_at"])
        high_today = len(r[(r["created_at"] >= today) & (r["risk"] == "High Risk")])
    c1, c2, c3 = st.columns([5, 0.6, 1.6])
    with c1:
        st.markdown(f'<div class="breadcrumbs" style="margin-top:6px;"><span class="bc-parent">Console</span><span class="bc-separator">/</span><span class="bc-active">{page_label}</span></div>', unsafe_allow_html=True)
    with c2:
        badge_style = ""
        if high_today > 0:
            badge_style = f"""
            <style>
            div[data-testid="column"]:nth-child(2) div[data-testid="stPopover"] > button::before {{
                content: '{high_today}';
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
                z-index: 10;
            }}
            </style>
            """
            st.markdown(badge_style, unsafe_allow_html=True)

        with st.popover("", help="Click to view notifications"):
            st.markdown("<p style='font-weight:700; font-size:14px; margin-bottom:8px; color:#0F172A;'>Threat Notifications</p>", unsafe_allow_html=True)
            if high_today == 0:
                st.markdown("<p style='font-size:12px; color:#71717A; margin: 10px 0;'>No critical threat alerts today.</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='font-size:12px; color:#EF4444; font-weight:600; margin-bottom:12px;'>⚠️ {high_today} High Risk scan(s) today</p>", unsafe_allow_html=True)
                today = pd.Timestamp.now().normalize()
                r = df.dropna(subset=["created_at"])
                today_scans = r[(r["created_at"] >= today) & (r["risk"] == "High Risk")].sort_values("created_at", ascending=False)
                for _, row in today_scans.iterrows():
                    ts = str(row["created_at"])[11:16]
                    st.markdown(f"""
                    <div style='padding:8px; border-radius:6px; background:#FEF2F2; border:1px solid #FEE2E2; margin-bottom:8px;'>
                        <div style='font-size:11px; font-weight:700; color:#991B1B;'>{row["title"][:35]}...</div>
                        <div style='font-size:10px; color:#B91C1C; margin-top:2px;'>Score: {row["score"]}% · Time: {ts}</div>
                    </div>
                    """, unsafe_allow_html=True)
    with c3:
        uname = st.session_state.get("username", "User")
        init = uname[0].upper() if uname else "U"
        st.markdown(f'<div style="display:flex;justify-content:flex-end;"><div class="user-chip"><div class="avatar">{init}</div><div><div class="u-name">{uname}</div><div class="u-role">Private Account</div></div></div></div>', unsafe_allow_html=True)


def risk_donut_chart(risk_count, total):
    labels = list(risk_count.index)
    values = list(risk_count.values)
    colors = [RISK_COLORS.get(r, "#71717A") for r in labels]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.72,
                                  marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
                                  textinfo="none", sort=False)])
    fig.update_layout(showlegend=False, margin=dict(l=10,r=10,t=10,b=10),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=190,
                      annotations=[dict(text=f"<b>{total}</b><br><span style='font-size:9.5px;color:#71717A'>Scans</span>",
                                        x=0.5, y=0.5, showarrow=False, font=dict(size=16, color="#0F172A"))])
    return fig


def fraud_score_chart(df):
    recent = df.dropna(subset=["created_at"]).tail(20)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=recent["created_at"], y=recent["score"],
                             mode="lines+markers",
                             line=dict(color="#0F172A", width=2.5, shape="spline"),
                             marker=dict(size=4.5, color="#0F172A"),
                             fill="tozeroy", fillcolor="rgba(15,23,42,0.03)"))
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                      margin=dict(l=10,r=10,t=10,b=10), height=190,
                      xaxis=dict(showgrid=False, linecolor="#E4E4E7"),
                      yaxis=dict(showgrid=True, gridcolor="#F4F4F5", linecolor="#E4E4E7", range=[0,105]))
    return fig


def _render_result_panel(score_raw, risk, badge_class, score_class, rec_title, rec_text, rule_flags):
    st.markdown(f"""
    <div class="security-indicator">
        <div style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:#71717A;margin-bottom:10px;">FRAUD SCORE</div>
        <div class="security-score-circle {score_class}">
            <div><span class="security-score-val">{int(score_raw)}</span><span class="security-score-pct">%</span></div>
        </div>
        <div style="margin-bottom:12px;"><span class="security-badge {badge_class}">{risk}</span></div>
    </div>""", unsafe_allow_html=True)
    
    if risk == "High Risk":
        card_color = "#FEF2F2"
        border_color = "#FCA5A5"
        icon = "🔴"
        action = "Do not pay any registration or processing fee. Do not share personal documents immediately. Verify the employer independently."
    elif risk == "Medium Risk":
        card_color = "#FFFBEB"
        border_color = "#FCD34D"
        icon = "🟡"
        action = "Research the company online. Verify recruiter email. Avoid sharing sensitive information until legitimacy is confirmed."
    else:
        card_color = "#F0FDF4"
        border_color = "#86EFAC"
        icon = "🟢"
        action = "Verify the company website before applying. Apply only through official channels."

    st.markdown(f"""
    <div style="background-color: {card_color}; border: 1px solid {border_color}; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
        <h4 style="margin-top: 0; color: #0F172A; font-size: 16px;">{icon} {risk}</h4>
        <p style="margin: 4px 0; font-size: 14px; color: #334155;"><b>Fraud Probability:</b> {int(score_raw)}%</p>
        <p style="margin: 4px 0; font-size: 14px; color: #334155;"><b>Explanation:</b> {rec_text}</p>
        <p style="margin: 4px 0; font-size: 14px; color: #334155;"><b>Recommended action:</b> {action}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-title" style="margin-top: 20px;"><i class="bi bi-question-circle"></i> Why this Risk Level?</p>', unsafe_allow_html=True)
    reasons = []
    if risk == "High Risk":
        reasons.append(f"Fraud Probability is above 60% ({int(score_raw)}%).")
    elif risk == "Medium Risk":
        reasons.append(f"Fraud Probability is between 30% and 60% ({int(score_raw)}%).")
    else:
        reasons.append(f"Fraud Probability is below 30% ({int(score_raw)}%).")
    
    for _, msg, _ in rule_flags:
        reasons.append(msg)
    
    if not rule_flags and risk == "Low Risk":
        reasons.append("Company profile is available.")
        reasons.append("Professional language is used.")
        reasons.append("No suspicious keywords detected.")
    
    bullets = "".join([f"<li style='color: #475569; font-size: 14px; margin-bottom: 4px;'>{r}</li>" for r in reasons])
    st.markdown(f"<ul style='margin-top: 8px;'>{bullets}</ul>", unsafe_allow_html=True)

    st.markdown('<p class="section-title" style="margin-top: 20px;"><i class="bi bi-bar-chart-steps"></i> Risk Breakdown</p>', unsafe_allow_html=True)
    if rule_flags:
        total_weight = sum(2.5 if is_crit else 1.0 for _, _, is_crit in rule_flags)
        breakdown_html = "<div style='font-family: monospace; background: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px; border-radius: 6px; font-size: 14px; color: #334155;'>"
        accum = 0
        for _, msg, is_crit in rule_flags:
            weight = 2.5 if is_crit else 1.0
            pts = int(round((weight / total_weight) * (score_raw - 5))) 
            pts = max(1, pts) # Give at least 1 point
            accum += pts
            breakdown_html += f"<div style='display:flex; justify-content:space-between; max-width: 450px;'><span>+{pts}</span> <span>{msg}</span></div>"
        
        base_pts = max(0, int(score_raw) - accum)
        if base_pts > 0:
            breakdown_html += f"<div style='display:flex; justify-content:space-between; max-width: 450px;'><span>+{base_pts}</span> <span>Base ML Risk Model</span></div>"
        
        breakdown_html += f"<hr style='margin: 8px 0; max-width: 450px; border-color: #CBD5E1;'/><div style='display:flex; justify-content:space-between; max-width: 450px; font-weight: bold;'><span>Total Risk Score:</span> <span>{int(score_raw)}/100</span></div>"
        breakdown_html += "</div>"
        st.markdown(breakdown_html, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='font-family: monospace; background: #F8FAFC; border: 1px solid #E2E8F0; padding: 12px; border-radius: 6px; font-size: 14px; color: #334155;'>
            <div style='display:flex; justify-content:space-between; max-width: 450px;'><span>+{int(score_raw)}</span> <span>Base ML Risk Model</span></div>
            <hr style='margin: 8px 0; max-width: 450px; border-color: #CBD5E1;'/>
            <div style='display:flex; justify-content:space-between; max-width: 450px; font-weight: bold;'><span>Total Risk Score:</span> <span>{int(score_raw)}/100</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<p class="section-title" style="margin-top: 20px;"><i class="bi bi-lightbulb"></i> Recommendations</p>', unsafe_allow_html=True)
    if risk == "High Risk":
        recs = [
            "Do not pay any registration or processing fee.",
            "Do not share personal documents immediately.",
            "Verify the employer independently.",
            "Report suspicious postings to the job platform if necessary."
        ]
    elif risk == "Medium Risk":
        recs = [
            "Research the company online.",
            "Verify recruiter email.",
            "Avoid sharing sensitive information until legitimacy is confirmed."
        ]
    else:
        recs = [
            "Verify the company website before applying.",
            "Apply only through official channels."
        ]
    
    rec_bullets = "".join([f"<li style='color: #475569; font-size: 14px; margin-bottom: 4px;'>{r}</li>" for r in recs])
    st.markdown(f"<ul style='margin-top: 8px;'>{rec_bullets}</ul>", unsafe_allow_html=True)


# =====================================================================
# ============================  SIDEBAR  ==============================
# =====================================================================

def render_sidebar():
    with st.sidebar:
        uname = st.session_state.get("username", "User")
        init = uname[0].upper() if uname else "U"
        st.markdown(f"""
        <div class="workspace-selector">
            <div class="workspace-avatar">{init}</div>
            <div class="workspace-info">
                <span class="workspace-name">{uname}</span>
                <span class="workspace-plan">Personal Console</span>
            </div>
        </div>""", unsafe_allow_html=True)

        menu_options = ["Dashboard","Scan New Job","Message Analyzer","My History",
                        "Risk Distribution","My Reports","Settings","About","Logout"]
        default_idx = menu_options.index(st.session_state.menu_selection) \
                      if st.session_state.menu_selection in menu_options else 0

        selected = option_menu(
            menu_title=None,
            options=menu_options,
            icons=["grid-1x2","search","chat-left-text","clock-history",
                   "pie-chart","file-earmark-bar-graph","gear","info-circle","box-arrow-right"],
            default_index=default_idx,
            key="sidebar_option_menu",
            styles={
                "container": {"padding":"0!important","background-color":"#FFFFFF"},
                "icon": {"color":"#71717A","font-size":"13.5px"},
                "nav-link": {"font-size":"12.5px","text-align":"left","margin":"2px 0",
                             "padding":"7px 10px","border-radius":"5px",
                             "color":"#52525B","font-weight":"500","--hover-color":"#F4F4F5"},
                "nav-link-selected": {"background-color":"#F4F4F5","color":"#0F172A","font-weight":"600"},
            },
        )
        st.markdown('<div class="sidebar-note"><p>🛡️ Your data is private — only you can see your history.</p></div>', unsafe_allow_html=True)
        st.session_state.menu_selection = selected
        return selected


# =====================================================================
# ==============================  PAGES  ==============================
# =====================================================================

# ── DASHBOARD ────────────────────────────────────────────────────────
def page_dashboard(df):
    uname = st.session_state.get("username", "User")
    st.markdown(f"""
    <div class="dashboard-hero">
        <div class="hero-badge">🟢 HEURISTICS ACTIVE &amp; SECURE</div>
        <h1 class="hero-title">Protect your applications with JobShield AI</h1>
        <p class="hero-desc">Your personal AI threat detector. Every scan is private — only you can see your history.</p>
    </div>""", unsafe_allow_html=True)

    c1, c2, _ = st.columns([1.1, 1.2, 3])
    with c1:
        if st.button("✨ Run New Scan", type="primary", use_container_width=True, key="dash_scan"):
            st.session_state.menu_selection = "Scan New Job"; st.rerun()
    with c2:
        if st.button("📋 View My History", type="secondary", use_container_width=True, key="dash_logs"):
            st.session_state.menu_selection = "My History"; st.rerun()

    st.markdown("""<div class="trust-indicator-row">
        <span class="trust-item"><i class="bi bi-cpu"></i> ML Model Inference Active</span>
        <span class="trust-item"><i class="bi bi-terminal"></i> NLP Text Vectorization</span>
        <span class="trust-item"><i class="bi bi-lock"></i> Private Data Isolation</span>
    </div><div style="height:32px;"></div>""", unsafe_allow_html=True)

    if df.empty:
        with st.container(border=True):
            st.info("No scans yet. Run your first threat scan to see your personal telemetry here.")
        return

    total  = len(df)
    high_n = len(df[df["risk"] == "High Risk"])
    med_n  = len(df[df["risk"] == "Medium Risk"])
    low_n  = len(df[df["risk"] == "Low Risk"])

    c1, c2, c3, c4 = st.columns(4)
    with c1: lbl,d = week_over_week(df);             metric_card("bi-briefcase","blue","Total Audits",total,lbl,d)
    with c2: lbl,d = week_over_week(df, df["risk"]=="High Risk");   metric_card("bi-exclamation-triangle","red","High Risk",high_n,lbl,d)
    with c3: lbl,d = week_over_week(df, df["risk"]=="Medium Risk"); metric_card("bi-shield-plus","orange","Medium Risk",med_n,lbl,d)
    with c4: lbl,d = week_over_week(df, df["risk"]=="Low Risk");    metric_card("bi-patch-check","green","Safe Clearances",low_n,lbl,d)

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown('<p class="section-title"><i class="bi bi-pie-chart"></i> Risk Distribution</p><p class="section-subtitle">Your scans by alert level</p>', unsafe_allow_html=True)
            risk_count = df["risk"].value_counts()
            st.plotly_chart(risk_donut_chart(risk_count, total), use_container_width=True, config={"displayModeBar":False})
            legend = "<div style='display:flex;flex-direction:column;gap:6px;margin-top:12px;border-top:1px solid #F4F4F5;padding-top:12px;'>"
            for r in ["High Risk","Medium Risk","Low Risk"]:
                n = int(risk_count.get(r,0)); pct = round(n/total*100,1) if total else 0
                legend += f'<div style="display:flex;align-items:center;justify-content:space-between;font-size:12.5px;"><div style="display:flex;align-items:center;gap:6px;"><span style="width:7px;height:7px;border-radius:50%;background:{RISK_COLORS[r]};display:inline-block;"></span><span style="font-weight:550;color:#0F172A;">{r}</span></div><span style="color:#71717A;">{n} scans ({pct}%)</span></div>'
            legend += "</div>"
            st.markdown(legend, unsafe_allow_html=True)
    with right:
        with st.container(border=True):
            st.markdown('<p class="section-title"><i class="bi bi-graph-up"></i> Threat Velocity</p><p class="section-subtitle">Your fraud score profile over time</p>', unsafe_allow_html=True)
            st.plotly_chart(fraud_score_chart(df), use_container_width=True, config={"displayModeBar":False})

    with st.container(border=True):
        st.markdown('<p class="section-title"><i class="bi bi-clock-history"></i> Recent Scans</p><p class="section-subtitle">Your latest analyzed job postings</p>', unsafe_allow_html=True)
        st.markdown('<div class="scan-feed">', unsafe_allow_html=True)
        for _, row in df.head(5).iterrows():
            bc = "badge-low" if row["risk"]=="Low Risk" else ("badge-medium" if row["risk"]=="Medium Risk" else "badge-high")
            ts = str(row['title']) if str(row['title']).strip() else '(untitled)'
            st.markdown(f"""<div class="scan-item">
                <div class="scan-avatar">{ts[0].upper()}</div>
                <div class="scan-details">
                    <div class="scan-title">{ts[:60]}</div>
                    <div class="scan-meta"><span>Score: {row['score']}%</span><span>•</span><span>{time_ago(row['created_at'])}</span></div>
                </div>
                <span class="security-badge {bc}">{row['risk']}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ── SCAN NEW JOB ─────────────────────────────────────────────────────
def page_scan(df):
    render_hero("Threat Scanner Sandbox", "Execute NLP semantic scans and heuristic checks against any job posting.")

    if "scan_mode" not in st.session_state:
        st.session_state.scan_mode = "Structured Form"

    st.markdown('<p style="font-size:13px;font-weight:600;color:#0F172A;margin-bottom:6px;">Input Method</p>', unsafe_allow_html=True)
    selected = st.segmented_control(
        "Input Method",
        options=["📋  Structured Form","📨  Paste Complete Job Message"],
        default="📋  Structured Form",
        key="scan_seg_ctrl",
        label_visibility="collapsed",
    )
    input_mode = "Paste Complete Job Message" if selected and "Paste" in selected else "Structured Form"
    st.session_state.scan_mode = input_mode
    st.markdown("<hr style='margin:12px 0 18px 0;border-color:#F4F4F5;'>", unsafe_allow_html=True)

    # ── MODE 1: Structured Form ──
    if input_mode == "Structured Form":
        form_col, result_col = st.columns([1.2, 1])
        with form_col:
            with st.container(border=True):
                st.markdown('<p class="section-title"><i class="bi bi-briefcase"></i> Job Specifications</p><p class="section-subtitle">Specify role headers and compensation details</p>', unsafe_allow_html=True)
                title = st.text_input("Job Title *", placeholder="e.g. Senior Product Designer", key="sf_title")
                c1, c2 = st.columns(2)
                with c1: salary = st.text_input("Salary Range", placeholder="e.g. 90000 - 130000", key="sf_salary")
                with c2:
                    st.markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)
                    remote = st.checkbox("Remote position", key="sf_remote")
            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown('<p class="section-title"><i class="bi bi-building"></i> Company Profile</p><p class="section-subtitle">Information detailing the employer</p>', unsafe_allow_html=True)
                company = st.text_input("Company Name", placeholder="e.g. Stripe Inc", key="sf_company")
                company_profile = st.text_area("Company Summary", placeholder="Brief summary of the company...", height=80, key="sf_profile")
            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown('<p class="section-title"><i class="bi bi-file-earmark-text"></i> Listing Copy</p><p class="section-subtitle">Paste the full description body and requirements</p>', unsafe_allow_html=True)
                description = st.text_area("Job Description *", placeholder="Paste the job description body here...", height=140, key="sf_desc")
                requirements = st.text_input("Role Requirements", placeholder="e.g. React, Figma, SaaS layout", key="sf_req")
            st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
            sf_clicked = st.button("✨ Execute AI Scan", type="primary", use_container_width=True, key="sf_btn")

        with result_col:
            with st.container(border=True):
                st.markdown('<p class="section-title"><i class="bi bi-clipboard-data"></i> AI Analysis Console</p><p class="section-subtitle">Threat score telemetry and warning flags</p>', unsafe_allow_html=True)
                if not sf_clicked:
                    st.markdown('<div class="analysis-placeholder"><div class="ph-icon"><i class="bi bi-shield-lock"></i></div>Fill in the fields and click <b>Execute AI Scan</b>.</div>', unsafe_allow_html=True)
                elif not title.strip() and not description.strip():
                    st.warning("⚠️ Please fill in at least a Job Title or Job Description.")
                else:
                    result, probability = predict_job(title, company, description, requirements, salary)
                    score = round(probability * 100, 2)
                    if score >= 60:
                        risk, badge_class, score_class = "High Risk","badge-high","score-high"
                        rec_title = "Threat Notice: High Scam Probability"
                        rec_text  = "Severe listing anomalies detected. <b>We strongly advise against applying or sharing identity details.</b>"
                    elif score >= 30:
                        risk, badge_class, score_class = "Medium Risk","badge-medium","score-medium"
                        rec_title = "Precautionary Notice: Mild Anomalies"
                        rec_text  = "Minor suspicious signals flagged. Verify recruitment authenticity through the company's verified domain."
                    else:
                        risk, badge_class, score_class = "Low Risk","badge-low","score-low"
                        rec_title = "Analysis Cleared: Low Risk"
                        rec_text  = "No severe anomalies identified. Standard application protocols apply."
                    flags = get_risk_flags(title, description, salary, company_profile, remote)
                    rule_flags = [(FLAG_ICON_MAP.get(f,"bi-exclamation-circle"), f, "payment" in f.lower()) for f in flags]
                    _render_result_panel(score, risk, badge_class, score_class, rec_title, rec_text, rule_flags)
                    log_title = title.strip() if title.strip() else description.strip()[:50]
                    save_scan(st.session_state.user_id, log_title, risk, score, input_mode="structured")

    # ── MODE 2: Paste Message ──
    else:
        st.markdown("""<div class="scan-source-chips">
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
                st.markdown('<p class="section-title"><i class="bi bi-chat-left-text"></i> Paste Job Advertisement</p><p class="section-subtitle">Paste any job message exactly as received</p>', unsafe_allow_html=True)
                message = st.text_area("Job Message", placeholder="Paste the complete message here...", height=310, label_visibility="collapsed", key="msg_text")
                wc = len(message.split()) if message.strip() else 0
                st.markdown(f'<div style="text-align:right;font-size:11px;color:#A1A1AA;margin-top:-8px;">{wc} words · {len(message)} characters</div>', unsafe_allow_html=True)
            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            msg_clicked = st.button("🔍 Analyze Message", type="primary", use_container_width=True, key="msg_btn")

        with result_col:
            with st.container(border=True):
                st.markdown('<p class="section-title"><i class="bi bi-clipboard-data"></i> Analysis Results</p><p class="section-subtitle">Fraud score, risk factors, and extracted information</p>', unsafe_allow_html=True)
                if not msg_clicked:
                    st.markdown('<div class="analysis-placeholder"><div class="ph-icon"><i class="bi bi-shield-lock"></i></div><div style="font-weight:600;color:#52525B;margin-bottom:6px;">Ready to Analyze</div>Paste a job message and click<br><b>🔍 Analyze Message</b>.</div>', unsafe_allow_html=True)
                elif not message.strip():
                    st.warning("⚠️ Please paste a job message before analyzing.")
                else:
                    cleaned = clean_text(message)
                    vector = vectorizer.transform([cleaned])
                    probability = classifier.predict_proba(vector)[0][1]
                    score = round(probability * 100, 2)
                    if score >= 60:
                        risk,badge_class,score_class = "High Risk","badge-high","score-high"
                        rec_title = "⚠️ High Fraud Probability Detected"
                        rec_text  = "Multiple severe anomalies found. <b>Avoid applying or sharing personal details.</b>"
                    elif score >= 30:
                        risk,badge_class,score_class = "Medium Risk","badge-medium","score-medium"
                        rec_title = "🔶 Suspicious Signals Detected"
                        rec_text  = "Some suspicious patterns found. Verify the company through official channels."
                    else:
                        risk,badge_class,score_class = "Low Risk","badge-low","score-low"
                        rec_title = "✅ Appears Relatively Safe"
                        rec_text  = "No severe anomalies identified. Still apply standard job-search caution."
                    rule_flags = analyze_message_rules(message)
                    critical_count = sum(1 for _,_,crit in rule_flags if crit)
                    boosted = min(score + critical_count * 6, 99.9)
                    if critical_count >= 2:
                        risk,badge_class,score_class = "High Risk","badge-high","score-high"
                        rec_title = "⚠️ High Fraud Probability Detected"
                        rec_text  = "Multiple severe anomalies found. <b>Avoid applying or sharing personal details.</b>"
                    _render_result_panel(boosted, risk, badge_class, score_class, rec_title, rec_text, rule_flags)
                    info = extract_info(message)
                    st.markdown('<p style="font-weight:600;margin-top:20px;margin-bottom:8px;color:#0F172A;font-size:13px;"><i class="bi bi-info-circle" style="color:#3B82F6;margin-right:4px;"></i>Extracted Information</p>', unsafe_allow_html=True)
                    def fmt(val, fallback="Not Found"):
                        if val is None or val=="" or val is False: return f'<span style="color:#A1A1AA;">{fallback}</span>'
                        if val is True: return '<span style="color:#10B981;font-weight:600;">Yes</span>'
                        return f'<span style="color:#0F172A;">{val}</span>'
                    rows = [("Company",fmt(info.get("company"),"Not Identified")),("Job Title",fmt(info.get("title"),"Not Identified")),
                            ("Salary",fmt(info.get("salary"),"Not Mentioned")),("Email",fmt(info.get("email"))),
                            ("Phone",fmt(info.get("phone"))),("Website",fmt(info.get("website"))),
                            ("Contact",fmt(info.get("contact"),"Not Specified")),("Remote/WFH",fmt(info.get("remote"))),("Certificate",fmt(info.get("certificate")))]
                    tbl = "".join(f"<tr><td>{lbl}</td><td>{val}</td></tr>" for lbl,val in rows)
                    st.markdown(f'<table class="info-table">{tbl}</table>', unsafe_allow_html=True)
                    log_title = message.strip()[:50].replace("\n"," ")
                    save_scan(st.session_state.user_id, log_title, risk, int(boosted), raw_message=message.strip(), input_mode="paste")


# ── MESSAGE ANALYZER ─────────────────────────────────────────────────
def page_message_analyzer(df):
    render_hero("Message Analyzer", "Paste recruiter emails, WhatsApp messages, or Telegram forwards for instant fraud analysis.")
    st.markdown("""<div class="scan-source-chips">
        <span class="source-chip"><i class="bi bi-whatsapp"></i> WhatsApp</span>
        <span class="source-chip"><i class="bi bi-telegram"></i> Telegram</span>
        <span class="source-chip"><i class="bi bi-envelope"></i> Email</span>
        <span class="source-chip"><i class="bi bi-linkedin"></i> LinkedIn DM</span>
    </div>""", unsafe_allow_html=True)

    form_col, result_col = st.columns([1.15, 1])
    with form_col:
        with st.container(border=True):
            st.markdown('<p class="section-title"><i class="bi bi-chat-square-text"></i> Recruiter Message</p><p class="section-subtitle">Paste the message exactly as you received it</p>', unsafe_allow_html=True)
            msg = st.text_area("Message", placeholder="Hi! We found your profile on LinkedIn. We are offering a WFH data entry role paying ₹25,000/month. Registration fee ₹500. Join: https://chat.whatsapp.com/...", height=320, label_visibility="collapsed", key="ma_msg")
            wc = len(msg.split()) if msg.strip() else 0
            st.markdown(f'<div style="text-align:right;font-size:11px;color:#A1A1AA;margin-top:-8px;">{wc} words</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        ma_clicked = st.button("🔍 Analyze Message", type="primary", use_container_width=True, key="ma_btn")

    with result_col:
        with st.container(border=True):
            st.markdown('<p class="section-title"><i class="bi bi-clipboard-data"></i> Analysis Results</p><p class="section-subtitle">Fraud score and detected patterns</p>', unsafe_allow_html=True)
            if not ma_clicked:
                st.markdown('<div class="analysis-placeholder"><div class="ph-icon"><i class="bi bi-shield-lock"></i></div>Paste a recruiter message and click<br><b>🔍 Analyze Message</b>.</div>', unsafe_allow_html=True)
            elif not msg.strip():
                st.warning("⚠️ Please paste a message to analyze.")
            else:
                cleaned = clean_text(msg)
                vector = vectorizer.transform([cleaned])
                probability = classifier.predict_proba(vector)[0][1]
                score = round(probability * 100, 2)
                if score >= 60:
                    risk,badge_class,score_class = "High Risk","badge-high","score-high"
                    rec_title,rec_text = "⚠️ High Fraud Probability","<b>Do not respond or share personal details.</b> Report this message."
                elif score >= 30:
                    risk,badge_class,score_class = "Medium Risk","badge-medium","score-medium"
                    rec_title,rec_text = "🔶 Suspicious Signals","Verify the sender and company through official channels before engaging."
                else:
                    risk,badge_class,score_class = "Low Risk","badge-low","score-low"
                    rec_title,rec_text = "✅ Appears Relatively Safe","No severe fraud patterns detected. Apply standard caution."
                rule_flags = analyze_message_rules(msg)
                critical_count = sum(1 for _,_,c in rule_flags if c)
                boosted = min(score + critical_count * 6, 99.9)
                if critical_count >= 2:
                    risk,badge_class,score_class = "High Risk","badge-high","score-high"
                    rec_title,rec_text = "⚠️ High Fraud Probability","<b>Do not respond or share personal details.</b> Report this message."
                _render_result_panel(boosted, risk, badge_class, score_class, rec_title, rec_text, rule_flags)
                log_title = msg.strip()[:50].replace("\n"," ")
                save_scan(st.session_state.user_id, log_title, risk, int(boosted), raw_message=msg.strip(), input_mode="message_analyzer")


# ── MY HISTORY ───────────────────────────────────────────────────────
def page_history(df):
    render_hero("My Scan History", "All your private job scan records — only visible to you.")
    with st.container(border=True):
        if df.empty:
            st.info("No scan history yet. Run a scan to see your history here.")
            return
        st.markdown('<p class="section-title"><i class="bi bi-search"></i> Search & Filter</p><p class="section-subtitle">Filter your personal scan logs</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([2.5, 1.5, 1])
        with c1: search = st.text_input("Search", placeholder="🔍 Search by title...", label_visibility="collapsed")
        with c2: rf = st.selectbox("Risk Filter", ["All Scan Alerts","High Risk","Medium Risk","Low Risk"], label_visibility="collapsed")
        with c3: st.download_button("⬇️ Export CSV", data=df.drop(columns=["user_id","raw_message","input_mode"],errors="ignore").to_csv(index=False), file_name="my_jobshield_history.csv", mime="text/csv", use_container_width=True)
        filtered = df.copy()
        if search: filtered = filtered[filtered["title"].astype(str).str.contains(search, case=False, na=False)]
        if rf != "All Scan Alerts": filtered = filtered[filtered["risk"] == rf]
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

        if filtered.empty:
            st.info("No records match your filter.")
        else:
            for _, row in filtered.iterrows():
                ts = str(row["created_at"])[:16] if pd.notna(row["created_at"]) else ""
                score = float(row["score"])
                
                # Recalculate risk to ensure it always matches score threshold (0-29 Low, 30-59 Med, 60-100 High)
                if score >= 60:
                    risk_label = "High Risk"
                    bg_color = "#FEE2E2"
                    text_color = "#DC2626"
                elif score >= 30:
                    risk_label = "Medium Risk"
                    bg_color = "#FEF3C7"
                    text_color = "#D97706"
                else:
                    risk_label = "Low Risk"
                    bg_color = "#DCFCE7"
                    text_color = "#15803D"
                
                with st.expander(f"**{str(row['title'])[:70]}** — {risk_label} · {score}% · {ts}"):
                    st.markdown(f"""
                    <style>
                    div[data-testid="stExpander"]:has(.marker-{row['id']}) {{
                        border-left: 4px solid {text_color} !important;
                        border-radius: 8px;
                    }}
                    </style>
                    <div class="marker-{row['id']}"></div>
                    """, unsafe_allow_html=True)
                    
                    dc1, dc2 = st.columns([2.5, 1])
                    with dc1:
                        st.markdown(f"""
                        <div style="margin-bottom: 10px;">
                            <b>Risk:</b> <span style="background-color: {bg_color}; color: {text_color}; padding: 3px 10px; border-radius: 12px; font-size: 13px; font-weight: 600;">{risk_label}</span>
                        </div>
                        <div style="margin-bottom: 10px;">
                            <b>Score:</b> {score}%
                            <div style="width: 100%; max-width: 300px; background-color: #E2E8F0; border-radius: 4px; height: 6px; margin-top: 6px;">
                                <div style="width: {score}%; background-color: {text_color}; height: 6px; border-radius: 4px;"></div>
                            </div>
                        </div>
                        <div style="margin-bottom: 12px;">
                            <b>Mode:</b> <code style="color: #64748B; background: #F1F5F9; padding: 2px 6px; border-radius: 4px;">{row.get('input_mode','—')}</code>
                        </div>
                        """, unsafe_allow_html=True)
                        if row.get("raw_message"):
                            st.markdown("**Original Message:**")
                            st.text(str(row["raw_message"])[:500])
                    with dc2:
                        if st.button("🗑 Delete", key=f"del_{row['id']}"):
                            delete_scan(row["id"], st.session_state.user_id)
                            st.success("Deleted.")
                            st.rerun()


# ── RISK DISTRIBUTION ────────────────────────────────────────────────
def page_risk_distribution(df):
    render_hero("Risk Distribution", "Visual breakdown of your personal scan history and fraud score analytics.")

    if df.empty:
        with st.container(border=True):
            st.info("No data yet. Run some scans to see your risk distribution charts here.")
        return

    total  = len(df)
    high_n = len(df[df["risk"]=="High Risk"])
    med_n  = len(df[df["risk"]=="Medium Risk"])
    low_n  = len(df[df["risk"]=="Low Risk"])
    avg_score = round(df["score"].mean(), 1)

    # ── Summary stats ──
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: metric_card("bi-clipboard-data","blue","Total Analyzed",total)
    with c2: metric_card("bi-patch-check","green","Low Risk",low_n)
    with c3: metric_card("bi-shield-plus","orange","Medium Risk",med_n)
    with c4: metric_card("bi-exclamation-triangle","red","High Risk",high_n)
    with c5: metric_card("bi-percent","orange","Avg Fraud Score",f"{avg_score}%")

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # ── Pie Chart + Bar Chart ──
    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown('<p class="section-title"><i class="bi bi-pie-chart"></i> Risk Level Breakdown</p><p class="section-subtitle">Distribution of your scans by risk level</p>', unsafe_allow_html=True)
            risk_count = df["risk"].value_counts()
            pie_fig = go.Figure(data=[go.Pie(
                labels=risk_count.index.tolist(),
                values=risk_count.values.tolist(),
                hole=0.55,
                marker=dict(colors=[RISK_COLORS.get(r,"#71717A") for r in risk_count.index],
                            line=dict(color="#FFFFFF",width=3)),
                textinfo="label+percent",
                textfont=dict(size=12),
            )])
            pie_fig.update_layout(showlegend=False, margin=dict(l=10,r=10,t=10,b=10),
                                  paper_bgcolor="rgba(0,0,0,0)", height=260)
            st.plotly_chart(pie_fig, use_container_width=True, config={"displayModeBar":False})

    with right:
        with st.container(border=True):
            st.markdown('<p class="section-title"><i class="bi bi-bar-chart"></i> Risk Level Bar Chart</p><p class="section-subtitle">Count of scans at each risk level</p>', unsafe_allow_html=True)
            risk_df = df["risk"].value_counts().reindex(["High Risk","Medium Risk","Low Risk"]).fillna(0).reset_index()
            risk_df.columns = ["Risk Level","Count"]
            bar_fig = go.Figure(go.Bar(
                x=risk_df["Risk Level"], y=risk_df["Count"],
                marker_color=[RISK_COLORS.get(r,"#71717A") for r in risk_df["Risk Level"]],
                text=risk_df["Count"].astype(int), textposition="outside",
            ))
            bar_fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                  margin=dict(l=10,r=10,t=10,b=10), height=260,
                                  xaxis=dict(showgrid=False,linecolor="#E4E4E7"),
                                  yaxis=dict(gridcolor="#F4F4F5",linecolor="#E4E4E7"),showlegend=False)
            st.plotly_chart(bar_fig, use_container_width=True, config={"displayModeBar":False})

    # ── Fraud score histogram ──
    with st.container(border=True):
        st.markdown('<p class="section-title"><i class="bi bi-graph-up"></i> Fraud Score History</p><p class="section-subtitle">Your fraud score trend over time</p>', unsafe_allow_html=True)
        valid = df.dropna(subset=["created_at"]).sort_values("created_at")
        line_fig = go.Figure()
        line_fig.add_trace(go.Scatter(
            x=valid["created_at"], y=valid["score"],
            mode="lines+markers",
            line=dict(color="#0F172A",width=2,shape="spline"),
            marker=dict(size=5, color=[RISK_COLORS.get(r,"#71717A") for r in valid["risk"]]),
            fill="tozeroy", fillcolor="rgba(15,23,42,0.04)"
        ))
        line_fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                               margin=dict(l=10,r=10,t=10,b=10), height=220,
                               xaxis=dict(showgrid=False,linecolor="#E4E4E7"),
                               yaxis=dict(gridcolor="#F4F4F5",range=[0,105],linecolor="#E4E4E7"))
        st.plotly_chart(line_fig, use_container_width=True, config={"displayModeBar":False})


# ── MY REPORTS ───────────────────────────────────────────────────────
def page_reports(df):
    render_hero("My Reports", "Download and export your personal scan history and analysis summaries.")

    if df.empty:
        with st.container(border=True):
            st.info("No scan data found. Run some scans first to generate your reports.")
        return

    # ── Date filter ──
    with st.container(border=True):
        st.markdown('<p class="section-title"><i class="bi bi-calendar-range"></i> Filter by Date Range</p><p class="section-subtitle">Select a date range for your report</p>', unsafe_allow_html=True)
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
        min_date = df["created_at"].min().date() if not df.empty else date.today()
        max_date = df["created_at"].max().date() if not df.empty else date.today()
        dc1, dc2 = st.columns(2)
        with dc1: start_date = st.date_input("From", value=min_date, min_value=min_date, max_value=max_date, key="rpt_start")
        with dc2: end_date   = st.date_input("To",   value=max_date, min_value=min_date, max_value=max_date, key="rpt_end")
        filtered = df[(df["created_at"].dt.date >= start_date) & (df["created_at"].dt.date <= end_date)]

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # ── Summary stats ──
    total  = len(filtered)
    high_n = len(filtered[filtered["risk"]=="High Risk"])
    med_n  = len(filtered[filtered["risk"]=="Medium Risk"])
    low_n  = len(filtered[filtered["risk"]=="Low Risk"])
    avg_sc = round(filtered["score"].mean(), 1) if total else 0

    c1,c2,c3,c4 = st.columns(4)
    with c1: metric_card("bi-briefcase","blue","Total Audited",total)
    with c2: metric_card("bi-exclamation-triangle","red","High Risk",high_n)
    with c3: metric_card("bi-shield-plus","orange","Medium Risk",med_n)
    with c4: metric_card("bi-patch-check","green","Low Risk",low_n)

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # ── Download buttons ──
    with st.container(border=True):
        st.markdown('<p class="section-title"><i class="bi bi-download"></i> Download Reports</p><p class="section-subtitle">Export your filtered data</p>', unsafe_allow_html=True)
        export_df = filtered.drop(columns=["user_id","raw_message","input_mode"], errors="ignore")

        bc1, bc2 = st.columns(2)
        with bc1:
            st.download_button(
                "⬇ Download History as CSV",
                data=export_df.to_csv(index=False),
                file_name=f"jobshield_history_{start_date}_{end_date}.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with bc2:
            # ── PDF Report using reportlab ──
            try:
                from reportlab.lib.pagesizes import letter
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib import colors
                from reportlab.lib.units import inch

                def build_pdf(filtered_df, uname, avg_score, start_d, end_d):
                    buf = io.BytesIO()
                    doc = SimpleDocTemplate(buf, pagesize=letter,
                                            rightMargin=0.75*inch, leftMargin=0.75*inch,
                                            topMargin=0.75*inch, bottomMargin=0.75*inch)
                    styles = getSampleStyleSheet()
                    story  = []

                    title_style = ParagraphStyle("Title2", parent=styles["Title"],
                                                 fontSize=20, spaceAfter=4)
                    sub_style   = ParagraphStyle("Sub",   parent=styles["Normal"],
                                                 fontSize=11, textColor=colors.gray, spaceAfter=16)
                    head_style  = ParagraphStyle("Head",  parent=styles["Heading2"],
                                                 fontSize=13, spaceBefore=14, spaceAfter=6)

                    story.append(Paragraph("🛡️ JobShield AI — Personal Report", title_style))
                    story.append(Paragraph(f"User: {uname} | Period: {start_d} → {end_d}", sub_style))
                    story.append(Paragraph("Analysis Summary", head_style))

                    t = len(filtered_df)
                    h = len(filtered_df[filtered_df["risk"]=="High Risk"])
                    m = len(filtered_df[filtered_df["risk"]=="Medium Risk"])
                    l = len(filtered_df[filtered_df["risk"]=="Low Risk"])
                    summary_data = [
                        ["Metric", "Value"],
                        ["Total Scans", str(t)],
                        ["High Risk", str(h)],
                        ["Medium Risk", str(m)],
                        ["Low Risk", str(l)],
                        ["Avg Fraud Score", f"{avg_score}%"],
                    ]
                    tbl = Table(summary_data, colWidths=[3*inch, 2*inch])
                    tbl.setStyle(TableStyle([
                        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0F172A")),
                        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
                        ("FONTSIZE",   (0,0), (-1,-1), 11),
                        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#F8FAFC"),colors.white]),
                        ("GRID",       (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
                        ("PADDING",    (0,0), (-1,-1), 8),
                    ]))
                    story.append(tbl)
                    story.append(Spacer(1, 0.25*inch))
                    story.append(Paragraph("Scan History", head_style))

                    hist_data = [["#","Title","Risk","Score","Date"]]
                    for i, row in filtered_df.head(50).iterrows():
                        hist_data.append([
                            str(i+1),
                            str(row.get("title",""))[:50],
                            str(row.get("risk","")),
                            f"{row.get('score',0):.1f}%",
                            str(row.get("created_at",""))[:16],
                        ])
                    hist_tbl = Table(hist_data, colWidths=[0.4*inch,3.2*inch,1.2*inch,0.8*inch,1.4*inch])
                    hist_tbl.setStyle(TableStyle([
                        ("BACKGROUND", (0,0),(-1,0), colors.HexColor("#0F172A")),
                        ("TEXTCOLOR",  (0,0),(-1,0), colors.white),
                        ("FONTSIZE",   (0,0),(-1,-1), 9),
                        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#F8FAFC"),colors.white]),
                        ("GRID",       (0,0),(-1,-1), 0.4, colors.HexColor("#E2E8F0")),
                        ("PADDING",    (0,0),(-1,-1), 6),
                    ]))
                    story.append(hist_tbl)
                    story.append(Spacer(1, 0.3*inch))
                    story.append(Paragraph(f"Generated by JobShield AI on {datetime.now().strftime('%Y-%m-%d %H:%M')} — Private & Confidential", styles["Normal"]))
                    doc.build(story)
                    return buf.getvalue()

                pdf_bytes = build_pdf(filtered, st.session_state.username, avg_sc, start_date, end_date)
                st.download_button(
                    "📄 Download Report as PDF",
                    data=pdf_bytes,
                    file_name=f"jobshield_report_{start_date}_{end_date}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            except ImportError:
                st.info("Install `reportlab` to enable PDF export: `pip install reportlab`")

    # ── Preview table ──
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<p class="section-title"><i class="bi bi-table"></i> Scan History Preview</p><p class="section-subtitle">First 100 records in the selected date range</p>', unsafe_allow_html=True)
        display = filtered.drop(columns=["user_id","raw_message","input_mode","id"], errors="ignore").head(100)
        st.dataframe(display.sort_values("created_at", ascending=False), use_container_width=True, hide_index=True)


# ── SETTINGS ─────────────────────────────────────────────────────────
def page_settings():
    render_hero("Account Settings", "Manage your account preferences and security settings.")
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown('<p class="section-title"><i class="bi bi-person-circle"></i> My Account</p>', unsafe_allow_html=True)
            st.markdown(f"**Name:** {st.session_state.get('username','—')}")
            st.markdown(f"**Email:** {st.session_state.get('email','—')}")
            st.markdown(f"**Role:** Personal User")
    with c2:
        with st.container(border=True):
            st.markdown('<p class="section-title"><i class="bi bi-key"></i> Change Password</p>', unsafe_allow_html=True)
            cur_pw  = st.text_input("Current Password", type="password", key="cp_cur")
            new_pw  = st.text_input("New Password", type="password", key="cp_new")
            conf_pw = st.text_input("Confirm New Password", type="password", key="cp_conf")
            if st.button("Update Password", type="primary", key="cp_btn"):
                from db import login_user
                _, err = login_user(st.session_state.email, cur_pw)
                if err:
                    st.error("❌ Current password is incorrect.")
                elif len(new_pw) < 6:
                    st.error("❌ New password must be at least 6 characters.")
                elif new_pw != conf_pw:
                    st.error("❌ Passwords do not match.")
                else:
                    update_password(st.session_state.user_id, new_pw)
                    st.success("✅ Password updated successfully!")

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<p class="section-title"><i class="bi bi-sliders"></i> Security Thresholds</p><p class="section-subtitle">Adjust risk threshold defaults</p>', unsafe_allow_html=True)
        st.slider("High Risk Score Threshold", 50, 90, 60)
        st.slider("Medium Risk Score Threshold", 20, 50, 30)


# ── ABOUT ─────────────────────────────────────────────────────────────
def page_about():
    render_hero("Platform Overview", "Technical documentation and architecture details of JobShield AI.")
    st.markdown("""
    <div class="about-hero">
        <h2>Shielding the Future of Work</h2>
        <p>JobShield AI is a personal threat detection engine designed to inspect, identify, and report suspicious employment listings before they compromise your safety — and all your data stays private.</p>
    </div>
    <div class="grid-3col">
        <div class="about-card"><div class="about-card-icon"><i class="bi bi-cpu"></i></div><h3>ML Classifier</h3><p>Logistic Regression + TF-IDF trained on verified employment fraud datasets.</p></div>
        <div class="about-card"><div class="about-card-icon"><i class="bi bi-shield-lock"></i></div><h3>Heuristic Engine</h3><p>Rules check WhatsApp links, payment requests, urgency language, brand impersonation, and more.</p></div>
        <div class="about-card"><div class="about-card-icon"><i class="bi bi-lock"></i></div><h3>Private by Design</h3><p>Every user has an isolated account. No one — not even the system — can see your history.</p></div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown('<p class="section-title"><i class="bi bi-rocket-takeoff"></i> Our Mission</p><p style="color:#52525B;font-size:13.5px;line-height:1.7;margin:0;">Employment fraud has risen significantly. JobShield AI puts threat detection directly in the hands of job seekers — for free, with full privacy.</p>', unsafe_allow_html=True)
    with c2:
        with st.container(border=True):
            st.markdown('<p class="section-title"><i class="bi bi-layers"></i> Tech Stack</p><p style="color:#52525B;font-size:13.5px;line-height:1.8;margin:0;">• <b>Language</b>: Python 3.10+<br>• <b>Interface</b>: Streamlit<br>• <b>Modeling</b>: Scikit-learn Logistic Regression<br>• <b>NLP</b>: TF-IDF Text Vectorization<br>• <b>Auth</b>: SQLite + BCrypt<br>• <b>Visuals</b>: Plotly + Vanilla CSS</p>', unsafe_allow_html=True)
    st.markdown('<div style="height:24px;"></div><div class="about-footer">JobShield AI — Personal Edition v4.0.0 · Private &amp; Secure</div>', unsafe_allow_html=True)


# =====================================================================
# ============================  ROUTER  ===============================
# =====================================================================

menu     = render_sidebar()
user_df  = get_user_scans(st.session_state.user_id)
render_top_bar(menu, user_df)

if   menu == "Logout":
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
elif menu == "Dashboard":           page_dashboard(user_df)
elif menu == "Scan New Job":        page_scan(user_df)
elif menu == "Message Analyzer":    page_message_analyzer(user_df)
elif menu == "My History":          page_history(user_df)
elif menu == "Risk Distribution":   page_risk_distribution(user_df)
elif menu == "My Reports":          page_reports(user_df)
elif menu == "Settings":            page_settings()
elif menu == "About":               page_about()