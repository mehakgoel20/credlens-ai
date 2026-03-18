import pandas as pd
import json
from datetime import datetime

CURRENT_YEAR = datetime.now().year

df = pd.read_csv("eval/loans_full_schematic.csv")

cases = []

for i, row in df.iterrows():

    monthly_income = row["annual_income"] / 12

    monthly_emi = row["debt_to_income"] * monthly_income

    credit_history_years = CURRENT_YEAR - row["earliest_credit_line"]

    employment_years = row["emp_length"]

    existing_loans = row["open_credit_lines"]

    dti = monthly_emi / monthly_income if monthly_income > 0 else 0

    if dti > 0.50:
        decision = "REJECT"

    elif dti <= 0.35 and credit_history_years >= 1 and existing_loans < 3:
        decision = "APPROVE"

    else:
        decision = "MANUAL_REVIEW"

    case = {
        "name": f"RealCase_{i}",
        "input": {
            "monthly_income": float(monthly_income),
            "monthly_emi": float(monthly_emi),
            "credit_history_years": float(credit_history_years),
            "existing_loans": int(existing_loans),
            "employment_years": float(employment_years)
        },
        "expected_decision": decision
    }

    cases.append(case)

with open("eval/real_test_cases.json", "w") as f:
    json.dump(cases[:500], f, indent=2)

print("Generated 500 realistic test cases.")