import streamlit as st
import random
import pandas as pd
import os
from datetime import datetime

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Fake Job Posting Detector",
    layout="wide"
)

LOG_FILE = "checked_postings.csv"

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("JobShield AI")

st.sidebar.info(
    "Built for Employment Fraud Detection Project"
)

st.sidebar.write(
    "Uses Machine Learning and Risk Analysis "
    "to identify suspicious job postings."
)

# -------------------------------
# MAIN TITLE
# -------------------------------
st.title("🕵️ Fake Job Posting Detector")

st.write(
    "Paste job details below and check whether the posting appears suspicious."
)

# -------------------------------
# TEMPORARY FAKE PREDICTOR
# -------------------------------
def fake_predict(title, description, salary_range, company_profile):
    return round(random.uniform(0, 1), 2)

# -------------------------------
# INPUT FORM
# -------------------------------
st.header("Enter Job Posting Details")

title = st.text_input("Job Title")

company_profile = st.text_area(
    "Company Profile / About the Company",
    height=100
)

description = st.text_area(
    "Job Description",
    height=150
)

requirements = st.text_area(
    "Requirements",
    height=100
)

salary_range = st.text_input("Salary Range")

telecommuting = st.checkbox(
    "Remote / Telecommuting Job"
)

# -------------------------------
# PREDICTION BUTTON
# -------------------------------
if st.button("Check This Posting"):

    if description.strip() == "":
        st.warning("Please enter a job description.")

    else:

        score = fake_predict(
            title,
            description,
            salary_range,
            company_profile
        )

        if score > 0.6:
            risk_level = "High"
            st.error(
                f"⚠️ High Risk Job Posting\n\nFraud Score: {score}"
            )

        elif score > 0.3:
            risk_level = "Medium"
            st.warning(
                f"⚠️ Medium Risk Job Posting\n\nFraud Score: {score}"
            )

        else:
            risk_level = "Low"
            st.success(
                f"✅ Low Risk Job Posting\n\nFraud Score: {score}"
            )

        # Progress Bar
        st.write("### Fraud Probability")
        st.progress(score)

        # Risk Factors Placeholder
        placeholder_flags = [
            "Feature coming soon: detailed risk reasons"
        ]

        st.write("### Risk Factors Detected")

        for flag in placeholder_flags:
            st.write(f"- {flag}")

        # Save Result
        new_row = pd.DataFrame([{
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "title": title,
            "fraud_score": score,
            "risk_level": risk_level
        }])

        if os.path.exists(LOG_FILE):
            new_row.to_csv(
                LOG_FILE,
                mode="a",
                header=False,
                index=False
            )
        else:
            new_row.to_csv(
                LOG_FILE,
                mode="w",
                header=True,
                index=False
            )

        st.success("Prediction saved successfully!")

# -------------------------------
# DASHBOARD
# -------------------------------
st.markdown("---")

st.header("📊 Checked Postings Dashboard")

if os.path.exists(LOG_FILE):

    log_df = pd.read_csv(LOG_FILE)

    st.subheader("Prediction History")

    st.dataframe(
        log_df,
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Risk Level Count")

        st.bar_chart(
            log_df["risk_level"].value_counts()
        )

    with col2:
        st.subheader("Fraud Score Trend")

        st.line_chart(
            log_df["fraud_score"]
        )

else:
    st.info("No postings checked yet.")