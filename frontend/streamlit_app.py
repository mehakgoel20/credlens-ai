import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8002"

st.set_page_config(page_title="CredLens AI", layout="centered")

st.title("CredLens AI — Credit Risk & Compliance Decision Platform")

st.subheader("1) Upload Policy Document (PDF)")
uploaded = st.file_uploader("Upload Loan Policy PDF", type=["pdf"])

if uploaded:
    files = {"file": (uploaded.name, uploaded, "application/pdf")}
    res = requests.post(f"{API_BASE}/docs/upload", files=files)
    if res.status_code == 200:
        st.success("Policy uploaded and indexed ✅")
        st.json(res.json())
    else:
        st.error("Upload failed")
        st.text(res.text)

st.divider()

st.subheader("2) Enter Applicant Data")
monthly_income = st.number_input("Monthly Income", min_value=0.0, value=50000.0)
monthly_emi = st.number_input("Monthly EMI", min_value=0.0, value=20000.0)
credit_history_years = st.number_input("Credit History (Years)", min_value=0.0, value=1.0)
existing_loans = st.number_input("Existing Loans", min_value=0, value=1, step=1)
employment_years = st.number_input("Employment Years", min_value=0.0, value=1.0)

if st.button("Make Decision"):
    payload = {
        "monthly_income": monthly_income,
        "monthly_emi": monthly_emi,
        "credit_history_years": credit_history_years,
        "existing_loans": existing_loans,
        "employment_years": employment_years
    }

    res = requests.post(f"{API_BASE}/decision/", json=payload)
    if res.status_code == 200:
        data = res.json()
        st.success("Decision Generated ✅")

        st.subheader("Decision Output")
        st.json(data)

        case_id = data.get("case_id")
        if case_id:
            st.subheader("Download Compliance Report")
            report_url = f"{API_BASE}/report/{case_id}"
            st.write("Report URL:", report_url)

            pdf_res = requests.get(report_url)
            if pdf_res.status_code == 200:
                st.download_button(
                    label="Download Report PDF",
                    data=pdf_res.content,
                    file_name=f"CredLens_Case_{case_id}_Report.pdf",
                    mime="application/pdf"
                )
    else:
        st.error("Decision API failed")
        st.text(res.text)
