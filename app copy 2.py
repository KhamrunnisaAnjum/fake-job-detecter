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
st.markdown("""
<style>

/* App */
.stApp{
    background:#ffffff;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#fafafa;
    border-right:1px solid #e5e7eb;
}

/* Inputs */
.stTextInput input,
.stTextArea textarea{
    border-radius:12px !important;
    border:1px solid #e5e7eb !important;
}

/* Buttons */
.stButton > button{
    background:#111827 !important;
    color:white !important;
    border-radius:12px !important;
    border:none !important;
    height:48px !important;
}

/* Metrics */
[data-testid="metric-container"]{
    border:1px solid #e5e7eb;
    border-radius:16px;
    padding:15px;
    background:white;
}

#MainMenu, footer, header{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# ================= CUSTOM UI =================

st.markdown("""
<style>

.stApp {
    background-color: #F8FAFC;
}

h1,h2,h3 {
    color:#0F172A;
    font-family:Arial;
}


section[data-testid="stSidebar"] {
    background-color:white;
}


.stButton button {

    background:#2563EB;
    color:white;
    border-radius:10px;
    height:45px;
    font-weight:600;

}


.stButton button:hover {

    background:#1D4ED8;

}


div[data-testid="stMetric"] {

    background:white;
    padding:20px;
    border-radius:15px;
    border:1px solid #E2E8F0;

}


</style>
""",
unsafe_allow_html=True)



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

    st.markdown("# 🛡️ JobShield AI")

    st.caption(
        "Fraud Detection Workspace"
    )

    st.divider()


    menu = st.radio(
        "Menu",
        [
            "Dashboard",
            "Scan New Job",
            "History",
            "About"
        ]
    )


    st.divider()


    st.info(
        "Machine Learning + NLP Based System"
    )



# ================= SAVE HISTORY =================


def save_prediction(title, risk, score):

    new_data = pd.DataFrame({

        "timestamp":[
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        ],

        "title":[title],

        "risk":[risk],

        "score":[score]

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


st.markdown("""
<div style="
padding:25px;
border:1px solid #e5e7eb;
border-radius:16px;
background:white;
margin-bottom:20px;
">

<h1>🛡️ JobShield AI</h1>

<p style="color:gray;">
Protecting job seekers using Machine Learning and NLP.
</p>

</div>
""", unsafe_allow_html=True)

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
if st.button(
    "🚀 Analyze Job Posting",
    use_container_width=True
):

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
            st.error("⚠️ Fake Job Detected")

        elif score >= 30:
            risk = "Medium Risk"
            st.warning("⚠️ Suspicious Job Posting")

        else:
            risk = "Low Risk"
            st.success("✅ Job Looks Legitimate")
            st.metric(
                "High Risk",
                fake_jobs 
                )
            st.metric(
                "Low Risk",
                real_jobs
                )
                


        flags = get_risk_flags(
            title,
            description,
            salary,
            company_profile,
            remote
        )


        st.subheader("⚠️ Risk Factors")

        if flags:
            for flag in flags:
                st.warning(flag)
        else:
            st.success("No suspicious factors found.")


        save_prediction(
            title,
            risk,
            score
        )



# ================= DASHBOARD PAGE =================


elif menu == "Dashboard":

    st.title("📊 JobShield AI Dashboard")

    st.write(
        "Monitor detected job postings and fraud analysis."
    )


    if os.path.exists(LOG_FILE):

        df = pd.read_csv(LOG_FILE)


        # Metrics

        total_jobs = len(df)

        fake_jobs = len(
            df[df["risk"]=="High Risk"]
        )

        real_jobs = total_jobs - fake_jobs

        avg_score = round(
            df["score"].mean(),
            2
        )


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Total Scans",
                total_jobs
            )


        with col2:

            st.metric(
                "Fake Jobs",
                fake_jobs
            )


        with col3:

            st.metric(
                "Real Jobs",
                real_jobs
            )


        with col4:

            st.metric(
                "Average Fraud Score",
                f"{avg_score}%"
            )


        st.divider()


        # Charts


        left, right = st.columns(2)


        with left:

            st.subheader(
                "📌 Risk Distribution"
            )


            risk_count = df["risk"].value_counts()


            st.bar_chart(
                risk_count
            )



        with right:

            st.subheader(
                "📈 Fraud Score Trend"
            )


            st.line_chart(
                df["score"]
            )



        st.divider()


        st.subheader(
            "📋 Recent Predictions"
        )


        st.dataframe(
            df.tail(10),
            use_container_width=True
        )


    else:

        st.info(
            "No predictions available yet."
        )
        # ================= HISTORY PAGE =================


elif menu == "History":

    st.title("🕒 Prediction History")


    if os.path.exists(LOG_FILE):

        history = pd.read_csv(
            LOG_FILE
        )


        st.dataframe(
            history,
            use_container_width=True
        )


        st.download_button(
            label="⬇️ Download History CSV",
            data=history.to_csv(index=False),
            file_name="jobshield_history.csv",
            mime="text/csv"
        )


    else:

        st.info(
            "No prediction history found."
        )



# ================= ABOUT PAGE =================


elif menu == "About":

    st.title(
        "ℹ️ About JobShield AI"
    )


    st.write(
        """
        ## Fake Job Posting Detection System 🛡️

        JobShield AI is a Machine Learning and 
        Natural Language Processing based application
        that detects suspicious job postings.

        ### Features:

        ✅ AI based fake job detection

        ✅ Fraud probability score

        ✅ Risk factor explanation

        ✅ Prediction history

        ✅ Dashboard analytics


        ### Technologies Used:

        - Python
        - Streamlit
        - Scikit-learn
        - NLP
        - TF-IDF
        - Logistic Regression


        ### Project Purpose:

        To help job seekers identify possible
        employment scams before sharing personal
        information or paying money.
        """
    )