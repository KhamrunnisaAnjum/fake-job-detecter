import streamlit as st


def login():

    st.markdown("""
    <div style="
    max-width:500px;
    margin:auto;
    padding:40px;
    border:1px solid #e5e7eb;
    border-radius:20px;
    background:white;
    text-align:center;
    margin-top:60px;
    ">

    <h1>🛡️ JobShield AI</h1>

    <p style="color:#6b7280;">
    AI-Powered Fake Job Detection Platform
    </p>

    <p style="color:#9ca3af;font-size:14px;">
    Sign in to continue
    </p>

    </div>
    """, unsafe_allow_html=True)

    username = st.text_input(
        "Email Address"
    )

    password = st.text_input(
        "Password",
        type="password"
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