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


# ================= CUSTOM CSS =================

st.markdown("""
<style>

.stApp {
    background-color:#F8FAFC;
}

h1,h2,h3 {
    color:#0F172A;
    font-family:Arial;
}

section[data-testid="stSidebar"] {
    background:white;
}

.stButton button {
    background:#2563EB;
    color:white;
    border-radius:10px;
    font-weight:600;
    height:45px;
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
""", unsafe_allow_html=True)



# ================= LOAD MODEL =================

classifier = joblib.load(
    "model/classifier.pkl"
)

vectorizer = joblib.load(
    "model/vectorizer.pkl"
)



# ================= FILE =================

LOG_FILE = "checked_postings.csv"



# ================= SIDEBAR =================

with st.sidebar:

    st.title("🛡️ JobShield AI")

    st.write(
        "Fake Job Posting Detection System"
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
        "Built using Machine Learning + NLP"
    )



# ================= SAVE FUNCTION =================

def save_prediction(
        title,
        risk,
        score
):

    data = pd.DataFrame({

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

        data.to_csv(
            LOG_FILE,
            mode="a",
            header=False,
            index=False
        )

    else:

        data.to_csv(
            LOG_FILE,
            index=False
        )



# ================= ML FUNCTION =================

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


    cleaned = clean_text(text)


    vector = vectorizer.transform(
        [cleaned]
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
    