import json
import random

cases = []

def make_case(i, income, emi, expected):
    return {
        "name": f"AutoCase_{i}",
        "input": {
            "monthly_income": income,
            "monthly_emi": emi,
            "credit_history_years": random.uniform(0.5, 10),
            "existing_loans": random.randint(0, 4),
            "employment_years": random.uniform(0.5, 10)
        },
        "expected_decision": expected
    }

i = 0

# APPROVE
for _ in range(40):
    income = random.randint(50000, 150000)
    emi = int(income * random.uniform(0.05, 0.30))
    cases.append(make_case(i, income, emi, "APPROVE"))
    i += 1

# MANUAL
for _ in range(40):
    income = random.randint(50000, 150000)
    emi = int(income * random.uniform(0.36, 0.49))
    cases.append(make_case(i, income, emi, "MANUAL_REVIEW"))
    i += 1

# REJECT
for _ in range(40):
    income = random.randint(50000, 150000)
    emi = int(income * random.uniform(0.51, 0.80))
    cases.append(make_case(i, income, emi, "REJECT"))
    i += 1

with open("eval/test_cases.json", "w") as f:
    json.dump(cases, f, indent=2)

print("Generated", len(cases), "test cases")