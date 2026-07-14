# ================= auth.py =================

import streamlit as st


def login():

    st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
    }
    #MainMenu, footer, header {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        max-width:440px;
        margin:80px auto 0 auto;
        padding:48px 40px;
        border:1px solid #E5E7EB;
        border-radius:20px;
        background:#FFFFFF;
        text-align:center;
        box-shadow:0 1px 2px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.04);
    ">
        <div style="font-size:34px; margin-bottom:6px;">🛡️</div>
        <h1 style="
            font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            font-size:24px;
            font-weight:700;
            color:#111827;
            margin:0 0 6px 0;
            letter-spacing:-0.4px;
        ">JobShield AI</h1>
        <p style="color:#6B7280; font-size:14.5px; margin:0 0 4px 0;">
            AI-Powered Fake Job Detection Platform
        </p>
        <p style="color:#9CA3AF; font-size:13px; margin:0 0 28px 0;">
            Sign in to continue
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    div[data-testid="stTextInput"] input {
        border-radius:10px !important;
        border:1px solid #E5E7EB !important;
        padding:10px 14px !important;
        font-size:14px !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color:#111827 !important;
        box-shadow:0 0 0 3px rgba(17,24,39,0.08) !important;
    }
    div.stButton > button {
        background:#111827 !important;
        color:#FFFFFF !important;
        border:none !important;
        border-radius:10px !important;
        height:46px !important;
        font-weight:600 !important;
        font-size:14.5px !important;
        transition:background 0.15s ease;
    }
    div.stButton > button:hover {
        background:#000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.4, 1])

    with mid:
        username = st.text_input(
            "Email Address",
            placeholder="you@company.com"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="••••••••"
        )

        if st.button(
            "Sign In",
            use_container_width=True
        ):

            if (
                username == "admin@gmail.com"
                and password == "admin123"
            ):

                st.session_state.logged_in = True
                st.success("Login Successful!")
                st.rerun()

            else:
                st.error(
                    "Invalid username or password"
                )