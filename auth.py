# auth.py — Premium Center-Card Login & Registration UI
import streamlit as st
from db import register_user, login_user

AUTH_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* Deep slate radial gradient background */
.stApp {
    background: radial-gradient(circle at 80% 20%, #1E293B 0%, #0F172A 100%) !important;
}

#MainMenu, footer, header { visibility: hidden !important; }

/* Set container width for centered login card */
.block-container {
    max-width: 460px !important;
    padding-top: 6vh !important;
    padding-bottom: 6vh !important;
}

/* Style container with border=True to look like a premium card */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4) !important;
    padding: 32px !important;
}

.auth-header {
    text-align: center;
    margin-bottom: 24px;
}
.auth-logo {
    font-size: 44px;
    margin-bottom: 12px;
    display: inline-block;
}
.auth-title {
    font-size: 26px !important;
    font-weight: 900 !important;
    color: #0F172A !important;
    letter-spacing: -0.035em !important;
    margin-top: 0 !important;
    margin-bottom: 6px !important;
}
.auth-desc {
    font-size: 13.5px;
    color: #64748B;
    line-height: 1.5;
}

/* Premium Tabs styling */
div[data-testid="stTabs"] > div:first-child {
    border-bottom: 1px solid #E2E8F0 !important;
    margin-bottom: 20px !important;
}
button[data-baseweb="tab"] {
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #94A3B8 !important;
    background: transparent !important;
    border: none !important;
    padding: 10px 16px !important;
    transition: all 0.15s ease !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #0F172A !important;
    border-bottom: 2px solid #0F172A !important;
}

/* Sleek inputs */
div[data-testid="stTextInput"] input {
    border-radius: 8px !important;
    border: 1.5px solid #E2E8F0 !important;
    height: 42px !important;
    font-size: 14px !important;
    background: #F8FAFC !important;
    color: #0F172A !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #0F172A !important;
    background: #FFFFFF !important;
    box-shadow: 0 0 0 3px rgba(15, 23, 42, 0.08) !important;
}
div[data-testid="stTextInput"] label {
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #334155 !important;
    margin-bottom: 6px !important;
}

/* Primary buttons styling */
div.stButton > button {
    background: #0F172A !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    height: 44px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    width: 100% !important;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15) !important;
    transition: all 0.2s ease !important;
    margin-top: 10px !important;
}
div.stButton > button:hover {
    background: #1E293B !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.25) !important;
}

.auth-footer {
    text-align: center;
    font-size: 12px;
    color: #94A3B8;
    margin-top: 24px;
    padding-top: 16px;
    border-top: 1px solid #F1F5F9;
}
</style>
"""

def login():
    st.markdown(AUTH_CSS, unsafe_allow_html=True)
    st.markdown(
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">',
        unsafe_allow_html=True
    )

    with st.container(border=True):
        st.markdown("""
        <div class="auth-header">
            <div class="auth-logo">🛡️</div>
            <h1 class="auth-title">JobShield AI</h1>
            <div class="auth-desc">Privacy-focused recruitment threat protection. Every scan and analysis remains strictly private.</div>
        </div>
        """, unsafe_allow_html=True)

        tab_in, tab_reg = st.tabs(["Sign In", "Create Account"])

        # ── SIGN IN ──────────────────────────────────────────
        with tab_in:
            email    = st.text_input("Email Address", placeholder="you@example.com", key="li_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="li_pass")
            if st.button("Sign In →", key="signin_btn"):
                if not email.strip() or not password:
                    st.error("Please fill in all fields.")
                else:
                    user, err = login_user(email, password)
                    if err:
                        st.error(f"❌ {err}")
                    else:
                        st.session_state.logged_in = True
                        st.session_state.user_id   = user["id"]
                        st.session_state.username  = user["username"]
                        st.session_state.email     = user["email"]
                        st.success(f"✅ Welcome back, {user['username']}!")
                        st.rerun()
            st.markdown('<div class="auth-footer"><i class="bi bi-shield-fill-check"></i> Secured with BCrypt password hashing</div>', unsafe_allow_html=True)

        # ── REGISTER ─────────────────────────────────────────
        with tab_reg:
            r_name = st.text_input("Full Name", placeholder="e.g. Ayesha Khan", key="reg_name")
            r_email= st.text_input("Email Address", placeholder="you@example.com", key="reg_email")
            r_pass = st.text_input("Password", type="password", placeholder="At least 6 characters", key="reg_pass")
            r_conf = st.text_input("Confirm Password", type="password", placeholder="Re-enter password", key="reg_conf")
            if st.button("Create Account →", key="register_btn"):
                if r_pass != r_conf:
                    st.error("❌ Passwords do not match.")
                else:
                    ok, err = register_user(r_name, r_email, r_pass)
                    if err:
                        st.error(f"❌ {err}")
                    else:
                        st.success("✅ Account created! Switch to **Sign In** to log in.")
            st.markdown('<div class="auth-footer"><i class="bi bi-lock-fill"></i> Data is fully isolated and encrypted</div>', unsafe_allow_html=True)