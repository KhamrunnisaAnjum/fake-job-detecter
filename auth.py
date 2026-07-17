# auth.py — Premium Center-Card Login UI matching target design
import streamlit as st
import base64
import os
from db import register_user, login_user

def login():
    if "auth_view" not in st.session_state:
        st.session_state.auth_view = "login"

    AUTH_CSS = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif !important;
    }}
    
    /* Overall background */
    .stApp {{
        background: #F1F5F9 !important;
    }}
    
    #MainMenu, footer, header {{ visibility: hidden !important; }}
    
    .block-container {{
        max-width: 950px !important;
        padding-top: 8vh !important;
        padding-bottom: 8vh !important;
    }}
    
    /* Main Card Container */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: #FFFFFF !important;
        border-radius: 32px !important;
        border: none !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15) !important;
        overflow: hidden !important;
    }}
    
    /* Remove padding inside the container */
    div[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"] {{
        padding: 0 !important;
        gap: 0 !important;
    }}
    
    /* Remove gap between columns */
    [data-testid="stHorizontalBlock"] {{
        gap: 0 !important;
    }}
    
    /* Left column (Image) */
    [data-testid="column"]:nth-child(1) {{
        /* You can replace this URL with your own image URL */
        background-image: linear-gradient(rgba(15, 23, 42, 0.3), rgba(15, 23, 42, 0.7)), url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1200&auto=format&fit=crop');
        background-size: cover !important;
        background-position: center !important;
        padding: 40px !important;
        min-height: 720px !important;
        border-top-left-radius: 32px !important;
        border-bottom-left-radius: 32px !important;
    }}
    
    /* Right column (Form) */
    [data-testid="column"]:nth-child(2) {{
        padding: 60px 80px !important;
        background: #FFFFFF !important;
        border-top-right-radius: 32px !important;
        border-bottom-right-radius: 32px !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    
    /* Input Fields */
    [data-testid="stTextInput"] input {{
        height: 52px !important;
        border-radius: 12px !important;
        border: 1px solid #E2E8F0 !important;
        padding: 0 16px !important;
        font-size: 14px !important;
        background: #FFFFFF !important;
        color: #0F172A !important;
        margin-bottom: 2px !important;
    }}
    [data-testid="stTextInput"] input:focus {{
        border-color: #EF4444 !important;
        box-shadow: 0 0 0 1px #EF4444 !important;
    }}
    
    /* Primary Button (Red) */
    button[kind="primary"] {{
        background-color: #EF4444 !important;
        color: white !important;
        height: 52px !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        margin-top: 15px !important;
        width: 100% !important;
        transition: all 0.2s ease;
    }}
    button[kind="primary"]:hover {{
        background-color: #DC2626 !important;
    }}
    
    /* Secondary Button (Google style) */
    button[kind="secondary"] {{
        background-color: #FFFFFF !important;
        color: #334155 !important;
        height: 52px !important;
        border-radius: 12px !important;
        border: 1px solid #E2E8F0 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        width: 100% !important;
        transition: all 0.2s ease;
    }}
    button[kind="secondary"]:hover {{
        border-color: #CBD5E1 !important;
        color: #0F172A !important;
    }}
    
    /* Tertiary Button (Text link) */
    button[kind="tertiary"] {{
        color: #EF4444 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        padding: 0 !important;
        height: auto !important;
        min-height: 0 !important;
    }}
    button[kind="tertiary"]:hover {{
        color: #DC2626 !important;
    }}
    
    .social-icons {{
        text-align: center;
        margin-top: 40px;
        color: #94A3B8;
        font-size: 18px;
        letter-spacing: 15px;
    }}
    
    /* Hide the form labels */
    div[data-testid="stTextInput"] label {{
        display: none !important;
    }}
    </style>
    """
    st.markdown(AUTH_CSS, unsafe_allow_html=True)
    st.markdown('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">', unsafe_allow_html=True)

    with st.container(border=True):
        col1, col2 = st.columns([1, 1.25])
        
        with col1:
            st.markdown("""
            <div style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                <div style="display:flex; justify-content: space-between; align-items: center;">
                    <div style="font-weight: 700; color: white; font-size: 16px;">Selected Works</div>
                    <div style="display:flex; align-items: center;">
                        <span style="color:white; font-size: 12px; margin-right: 15px; font-weight:500;">Sign Up</span>
                        <span style="border: 1px solid rgba(255,255,255,0.6); border-radius: 20px; padding: 6px 16px; color: white; font-size: 12px; font-weight:500;">Join Us</span>
                    </div>
                </div>
                <div style="display:flex; justify-content: space-between; align-items: flex-end; margin-top: auto;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <img src="https://ui-avatars.com/api/?name=Andrew+UI&background=0284C7&color=fff&size=80" style="width: 44px; height: 44px; border-radius: 50%;">
                        <div style="color: white; line-height: 1.3;">
                            <div style="font-weight: 700; font-size: 14px;">Andrew.ui</div>
                            <div style="font-size: 12px; color: rgba(255,255,255,0.7); font-weight:500;">UI & Illustration</div>
                        </div>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <div style="width: 32px; height: 32px; border: 1px solid rgba(255,255,255,0.3); border-radius: 50%; display: flex; align-items:center; justify-content:center; color: white; font-size:12px;">←</div>
                        <div style="width: 32px; height: 32px; border: 1px solid rgba(255,255,255,0.3); border-radius: 50%; display: flex; align-items:center; justify-content:center; color: white; font-size:12px;">→</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div style="display:flex; justify-content: space-between; align-items: center; margin-bottom: 60px;">
                <div style="font-weight: 900; font-size: 18px; color: #0F172A; letter-spacing: -0.5px;">JOB SHIELD</div>
                <div style="border: 1px solid #E2E8F0; border-radius: 20px; padding: 4px 12px; font-size: 11px; color: #475569; font-weight:600;">
                    🇬🇧 EN <i class="bi bi-chevron-down" style="font-size: 9px; margin-left: 2px;"></i>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.auth_view == "login":
                st.markdown('<h1 style="font-size: 44px; font-weight: 800; color: #0F172A; margin:0; line-height: 1.1; letter-spacing: -1px; text-align: center;">Welcome Back</h1>', unsafe_allow_html=True)
                st.markdown('<p style="font-size: 14px; color: #64748B; text-align: center; margin-top: 8px; margin-bottom: 35px; font-weight: 500;">Sign in to Job Shield Console</p>', unsafe_allow_html=True)
                
                email = st.text_input("Email", placeholder="Email", label_visibility="collapsed", key="li_email")
                st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
                password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed", key="li_pass")
                
                st.markdown("<p style='text-align:right; color:#EF4444; font-size:11px; margin-top:-6px; margin-bottom: 25px; font-weight:500; cursor:pointer;'>Forgot password ?</p>", unsafe_allow_html=True)
                
                st.markdown("""
                <div style="display: flex; align-items: center; text-align: center; margin: 15px 0 20px 0;">
                    <div style="flex: 1; border-bottom: 1px solid #E2E8F0;"></div>
                    <span style="padding: 0 15px; color: #94A3B8; font-size: 12px; font-weight: 500;">or</span>
                    <div style="flex: 1; border-bottom: 1px solid #E2E8F0;"></div>
                </div>
                """, unsafe_allow_html=True)
                
                st.button("Login with Google", use_container_width=True, key="btn_google")
                
                if st.button("Login", type="primary", use_container_width=True, key="signin_btn"):
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
                            st.rerun()
                
                st.markdown("<div style='text-align:center; font-size: 12px; color: #64748B; font-weight:500; margin-top: 20px;'>Don't have an account?</div>", unsafe_allow_html=True)
                if st.button("Sign up", type="tertiary", use_container_width=True, key="toggle_reg"):
                    st.session_state.auth_view = "register"
                    st.rerun()
                        
            else:
                st.markdown('<h1 style="font-size: 44px; font-weight: 800; color: #0F172A; margin:0; line-height: 1.1; letter-spacing: -1px; text-align: center;">Join Us</h1>', unsafe_allow_html=True)
                st.markdown('<p style="font-size: 14px; color: #64748B; text-align: center; margin-top: 8px; margin-bottom: 35px; font-weight: 500;">Create your Job Shield account</p>', unsafe_allow_html=True)
                
                r_name = st.text_input("Full Name", placeholder="Full Name", label_visibility="collapsed", key="reg_name")
                r_email= st.text_input("Email Address", placeholder="Email", label_visibility="collapsed", key="reg_email")
                r_pass = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed", key="reg_pass")
                r_conf = st.text_input("Confirm Password", type="password", placeholder="Confirm Password", label_visibility="collapsed", key="reg_conf")
                
                if st.button("Create Account", type="primary", use_container_width=True, key="register_btn"):
                    if r_pass != r_conf:
                        st.error("❌ Passwords do not match.")
                    else:
                        ok, err = register_user(r_name, r_email, r_pass)
                        if err:
                            st.error(f"❌ {err}")
                        else:
                            st.success("✅ Account created! Please log in.")
                            st.session_state.auth_view = "login"
                            st.rerun()
                
                st.markdown("<div style='text-align:center; font-size: 12px; color: #64748B; font-weight:500; margin-top: 20px;'>Already have an account?</div>", unsafe_allow_html=True)
                if st.button("Log in", type="tertiary", use_container_width=True, key="toggle_login"):
                    st.session_state.auth_view = "login"
                    st.rerun()

            st.markdown("""
            <div class="social-icons">
                <i class="bi bi-facebook"></i>
                <i class="bi bi-twitter"></i>
                <i class="bi bi-linkedin"></i>
                <i class="bi bi-instagram"></i>
            </div>
            """, unsafe_allow_html=True)