import joblib
import os
import numpy as np

# ✅ Absolute path so it works no matter where uvicorn is run from
# backend/app/services/risk_model.py  -> go up 3 levels -> project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "ml", "artifacts", "risk_model.pkl")

_model = None


def load_model():
    """
    Loads the trained ML risk model from disk (if present).
    If the model file does not exist, returns None.
    """
    global _model

    if _model is None:
        if not os.path.exists(MODEL_PATH):
            return None
        _model = joblib.load(MODEL_PATH)

    return _model


def simple_risk_score(features: dict):
    """
    Rule-based risk scoring (baseline).
    Output matches the same JSON structure as ML scoring.
    """
    income = features["monthly_income"]
    emi = features["monthly_emi"]
    credit_years = features["credit_history_years"]
    loans = features["existing_loans"]
    emp_years = features["employment_years"]

    dti = emi / income

    risk = 0.0

    if dti > 0.5:
        risk += 0.45
    elif dti > 0.35:
        risk += 0.25
    else:
        risk += 0.10

    if credit_years < 1:
        risk += 0.25
    elif credit_years < 3:
        risk += 0.15
    else:
        risk += 0.05

    if loans >= 3:
        risk += 0.20
    elif loans == 2:
        risk += 0.12
    else:
        risk += 0.05

    if emp_years < 1:
        risk += 0.15
    elif emp_years < 3:
        risk += 0.08
    else:
        risk += 0.03

    risk_score = min(round(risk, 3), 1.0)

    if risk_score >= 0.7:
        bucket = "HIGH"
    elif risk_score >= 0.4:
        bucket = "MEDIUM"
    else:
        bucket = "LOW"

    reasons = []
    if dti > 0.35:
        reasons.append("HIGH_DTI")
    if credit_years < 3:
        reasons.append("LOW_CREDIT_HISTORY")
    if loans >= 2:
        reasons.append("MULTIPLE_EXISTING_LOANS")
    if emp_years < 3:
        reasons.append("LOW_EMPLOYMENT_STABILITY")

    return {
        "risk_score": risk_score,
        "risk_bucket": bucket,
        "dti": round(dti, 3),
        "reason_codes": reasons,
        "risk_engine": "rules"
    }


def ml_risk_score(features: dict):
    """
    ML-based risk scoring (primary).
    If ML model is missing, it automatically falls back to rule-based scoring.
    """
    model = load_model()

    # ✅ fallback if model isn't trained yet
    if model is None:
        return simple_risk_score(features)

    X = np.array([[
        features["monthly_income"],
        features["monthly_emi"],
        features["credit_history_years"],
        features["existing_loans"],
        features["employment_years"]
    ]])

    # Probability of class 1 (high-risk)
    prob = float(model.predict_proba(X)[0][1])

    if prob >= 0.7:
        bucket = "HIGH"
    elif prob >= 0.4:
        bucket = "MEDIUM"
    else:
        bucket = "LOW"

    dti = features["monthly_emi"] / features["monthly_income"]

    return {
        "risk_score": round(prob, 3),
        "risk_bucket": bucket,
        "dti": round(dti, 3),
        "reason_codes": [],  # keep empty OR add rules-based reason codes if you want
        "risk_engine": "ml"
    }
