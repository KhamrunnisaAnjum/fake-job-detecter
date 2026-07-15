# ================= auth.py =================

import streamlit as st


def login():
    # Inject Custom CSS for the premium split login page (covers all possible Streamlit column selectors)
    st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background-color: #FAFAFA !important;
}

#MainMenu, footer, header[data-testid="stHeader"] {
    visibility: hidden !important;
}

.block-container {
    padding-top: 4.5rem !important;
    padding-bottom: 4.5rem !important;
    max-width: 1060px !important;
}

/* Horizontal Block Container Override (Split Layout Card) */
div[data-testid="stHorizontalBlock"] {
    background: #FFFFFF !important;
    border: 1px solid #E4E4E7 !important;
    border-radius: 16px !important;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02) !important;
    overflow: hidden !important;
    margin: 0 auto !important;
    min-height: 560px !important;
    gap: 0px !important;
}

/* Left Column - Product Branding & Trust (Comprehensive Selectors) */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(1),
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-of-type(1),
div[data-testid="stHorizontalBlock"] > div[class*="stColumn"]:nth-of-type(1),
div[data-testid="stHorizontalBlock"] > div[class*="column"]:nth-of-type(1) {
    background: linear-gradient(135deg, #090D16 0%, #152238 100%) !important;
    padding: 56px 48px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    color: #FFFFFF !important;
    position: relative !important;
    min-height: 560px !important;
}

/* Left Column Radial Glowing Orb */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(1)::before,
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-of-type(1)::before {
    content: "" !important;
    position: absolute !important;
    top: -10% !important;
    right: -10% !important;
    width: 320px !important;
    height: 320px !important;
    background: radial-gradient(circle, rgba(59, 130, 246, 0.12) 0%, rgba(0,0,0,0) 70%) !important;
    pointer-events: none !important;
}

/* Right Column - Login Form Card (Comprehensive Selectors) */
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-of-type(2),
div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-of-type(2),
div[data-testid="stHorizontalBlock"] > div[class*="stColumn"]:nth-of-type(2),
div[data-testid="stHorizontalBlock"] > div[class*="column"]:nth-of-type(2) {
    background: #FFFFFF !important;
    padding: 56px 48px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    min-height: 560px !important;
}

/* Left Column Elements styling */
.branding-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 28px;
}
.branding-logo {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.14);
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
.branding-title {
    font-size: 18px;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #FFFFFF;
}

.hero-text-container {
    margin-top: auto;
    margin-bottom: auto;
    padding-bottom: 12px;
}
.left-title {
    font-size: 28px;
    font-weight: 700;
    color: #FFFFFF !important;
    line-height: 1.28;
    letter-spacing: -0.03em !important;
    margin-bottom: 16px !important;
}
.left-desc {
    font-size: 14.5px;
    color: #94A3B8;
    line-height: 1.6;
    margin: 0;
    font-weight: 400;
}

.trust-container {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    margin-top: 40px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    padding-top: 24px;
}
.trust-badge {
    font-size: 12.5px;
    color: #94A3B8;
    font-weight: 550;
    display: flex;
    align-items: center;
    gap: 6px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 6px 12px;
    border-radius: 6px;
}
.trust-badge span {
    font-size: 13px;
}

/* Right Column Elements styling */
.right-header {
    text-align: center;
    margin-bottom: 28px;
}
.right-title {
    font-size: 24px;
    font-weight: 700;
    color: #0F172A !important;
    letter-spacing: -0.03em !important;
    margin-bottom: 6px !important;
}
.right-subtitle {
    font-size: 14px;
    color: #52525B;
    margin: 0;
}

/* Google / Continue With Button */
.social-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    width: 100%;
    height: 40px;
    border-radius: 6px;
    border: 1px solid #E4E4E7;
    background: #FFFFFF;
    color: #18181B;
    font-size: 13.5px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}
.social-btn:hover {
    background: #FAFAFA;
    border-color: #D4D4D8;
}

.divider-row {
    display: flex;
    align-items: center;
    text-align: center;
    color: #A1A1AA;
    font-size: 11px;
    margin: 22px 0;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.divider-row::before, .divider-row::after {
    content: '';
    flex: 1;
    border-bottom: 1px solid #F4F4F5;
}
.divider-row:not(:empty)::before {
    margin-right: .6em;
}
.divider-row:not(:empty)::after {
    margin-left: .6em;
}

.input-label {
    font-size: 13px;
    font-weight: 500;
    color: #3F3F46;
    display: block;
    margin-bottom: 6px;
    margin-top: 16px;
    letter-spacing: -0.01em;
}

/* Input adjustments */
div[data-testid="stTextInput"] {
    margin-bottom: 0px !important;
}
div[data-testid="stTextInput"] input {
    border-radius: 6px !important;
    border: 1px solid #E4E4E7 !important;
    padding: 10px 14px !important;
    font-size: 14px !important;
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    transition: all 0.15s ease !important;
    height: 40px !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #0F172A !important;
    box-shadow: 0 0 0 2px rgba(15,23,42,0.06) !important;
}

/* Button Adjustments */
div.stButton > button {
    background: #0F172A !important;
    color: #FFFFFF !important;
    border: 1px solid #0F172A !important;
    border-radius: 6px !important;
    height: 40px !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    letter-spacing: -0.01em !important;
    transition: all 0.15s ease !important;
    margin-top: 24px !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
}
div.stButton > button:hover {
    background: #1E293B !important;
    border-color: #1E293B !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08) !important;
}

.right-footer {
    margin-top: 24px;
    font-size: 12px;
    color: #71717A;
    text-align: center;
    border-top: 1px solid #F4F4F5;
    padding-top: 18px;
}
.right-footer a {
    color: #52525B;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.15s ease;
}
.right-footer a:hover {
    color: #0F172A;
}
</style>""", unsafe_allow_html=True)

    # Render split columns layout
    c1, c2 = st.columns([1.25, 1])

    with c1:
        st.markdown("""<div class="branding-header"><div class="branding-logo"><span>🛡️</span></div><span class="branding-title" style="color:#FFFFFF !important; font-weight:700;">JobShield AI</span></div><div class="hero-text-container"><h2 class="left-title" style="color:#FFFFFF !important; font-weight:700; margin-top:0px;">Verify roles instantly.<br>Shield your search.</h2><p class="left-desc" style="color:#94A3B8 !important; margin:0;">Our NLP classifier identifies employment scams and compliance hazards in real time, protecting applicants from advanced fee fraud and data harvesting listing schemes.</p></div><div class="trust-container"><span class="trust-badge"><span>🛡️</span> &nbsp;NLP Classifier</span><span class="trust-badge"><span>🔒</span> &nbsp;Secure Vault</span><span class="trust-badge"><span>🟢</span> &nbsp;Heuristics Active</span></div>""", unsafe_allow_html=True)

    with c2:
        # ── Session state for Google flow ──
        if "google_flow" not in st.session_state:
            st.session_state.google_flow = False

        # ============================================================
        # STEP 2 — GOOGLE WORKSPACE EMAIL VERIFICATION
        # ============================================================
        if st.session_state.google_flow:
            st.markdown("""
<div style="text-align:center; margin-bottom:28px; padding-top:8px;">
    <svg width="40" height="40" viewBox="0 0 48 48" style="margin-bottom:14px;">
        <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
        <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
        <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
        <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.31-8.16 2.31-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
        <path fill="none" d="M0 0h48v48H0z"/>
    </svg>
    <h2 style="font-size:20px; font-weight:700; color:#0F172A; margin:0 0 6px 0; letter-spacing:-0.02em;">Sign in with Google</h2>
    <p style="font-size:13px; color:#52525B; margin:0; line-height:1.5;">Use your Google Workspace account<br>to continue to <b>JobShield AI</b></p>
</div>""", unsafe_allow_html=True)

            st.markdown('<label class="input-label">Google Workspace Email</label>', unsafe_allow_html=True)
            google_email = st.text_input(
                "Google Workspace Email",
                placeholder="you@gmail.com",
                label_visibility="collapsed",
                key="google_email_input"
            )

            # Next button — full width, no columns
            if st.button("Next →", use_container_width=True, type="primary", key="google_next"):
                email = google_email.strip().lower()
                if not email:
                    st.error("Please enter your email address.")
                elif not (email.endswith("@gmail.com") or email.endswith("@googleworkspace.com")):
                    st.error("⛔ Enter a valid Gmail or Google Workspace email.")
                elif email == "admin@gmail.com":
                    st.session_state.logged_in = True
                    st.session_state.google_flow = False
                    st.rerun()
                else:
                    st.error("🚫 Account not found in this workspace. Contact your admin.")

            # Back as a subtle text link — no columns needed
            st.markdown("""
<div style="text-align:center; margin-top:14px;">
    <form action="" method="get">
    </form>
</div>""", unsafe_allow_html=True)
            if st.button("← Use a different login method", use_container_width=True, type="secondary", key="google_back"):
                st.session_state.google_flow = False
                st.rerun()

            st.markdown("""
<div style="margin-top:18px; padding-top:14px; border-top:1px solid #F4F4F5; font-size:11.5px; color:#A1A1AA; text-align:center; letter-spacing:0.01em;">
    🔒 Secured by Google Identity Services
</div>""", unsafe_allow_html=True)



        # ============================================================
        # STEP 1 — MAIN LOGIN PANEL
        # ============================================================
        else:
            st.markdown("""<div class="right-header"><h1 class="right-title">Welcome back</h1><p class="right-subtitle">Sign in to access your threat console</p></div>""", unsafe_allow_html=True)

            st.markdown("""<style>
div[key="google_login_btn"] > button {
    background: #FFFFFF !important; color: #18181B !important;
    border: 1px solid #E4E4E7 !important; border-radius: 6px !important;
    height: 42px !important; font-size: 13.5px !important;
    font-weight: 500 !important; box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
    margin-top: 0 !important;
}
div[key="google_login_btn"] > button:hover {
    background: #FAFAFA !important; border-color: #D4D4D8 !important;
    transform: none !important;
}
</style>""", unsafe_allow_html=True)

            if st.button(
                "🔑  Continue with Google workspace",
                use_container_width=True,
                type="secondary",
                key="google_login_btn"
            ):
                st.session_state.google_flow = True
                st.rerun()

            st.markdown('<div class="divider-row">or use credentials</div>', unsafe_allow_html=True)

            st.markdown('<label class="input-label">Email Address</label>', unsafe_allow_html=True)
            username = st.text_input(
                "Email Address",
                placeholder="you@company.com",
                label_visibility="collapsed"
            )

            st.markdown('<label class="input-label">Password</label>', unsafe_allow_html=True)
            password = st.text_input(
                "Password",
                type="password",
                placeholder="••••••••",
                label_visibility="collapsed"
            )

            if st.button("Sign In", use_container_width=True, key="signin_btn"):
                if username == "admin@gmail.com" and password == "admin123":
                    st.session_state.logged_in = True
                    st.success("Authorized")
                    st.rerun()
                else:
                    st.error("Invalid email address or password")

            st.markdown("""<div class="right-footer"><a href="#">Forgot password?</a> &nbsp;•&nbsp; <a href="#">Contact support</a></div>""", unsafe_allow_html=True)