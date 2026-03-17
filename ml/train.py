import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

def generate_data(n=2000, seed=42):
    np.random.seed(seed)

    monthly_income = np.random.randint(20000, 120000, n)
    monthly_emi = (monthly_income * np.random.uniform(0.05, 0.7, n)).astype(int)
    credit_history_years = np.random.uniform(0, 10, n)
    existing_loans = np.random.randint(0, 6, n)
    employment_years = np.random.uniform(0, 10, n)

    dti = monthly_emi / monthly_income

    # Label generation (default risk) - synthetic logic
    risk_prob = (
        0.5 * (dti > 0.5) +
        0.25 * (credit_history_years < 1) +
        0.15 * (existing_loans >= 3) +
        0.10 * (employment_years < 1)
    )

    # Convert probability into 0/1 labels
    y = (risk_prob + np.random.uniform(0, 0.2, n) > 0.6).astype(int)

    df = pd.DataFrame({
        "monthly_income": monthly_income,
        "monthly_emi": monthly_emi,
        "credit_history_years": credit_history_years,
        "existing_loans": existing_loans,
        "employment_years": employment_years,
        "label": y
    })
    return df

def main():
    df = generate_data()

    X = df.drop(columns=["label"])
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print(classification_report(y_test, preds))

    os.makedirs("ml/artifacts", exist_ok=True)
    joblib.dump(model, "ml/artifacts/risk_model.pkl")
    print("✅ Model saved to ml/artifacts/risk_model.pkl")

if __name__ == "__main__":
    main()
