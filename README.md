# CredLens AI

**Policy-Grounded Credit Decisioning System**

CredLens AI is an **AI-assisted credit decision engine** designed to simulate how modern fintech companies evaluate loan applications using machine learning, policy retrieval, and explainable AI.

The system combines:

* Machine Learning risk scoring
* Retrieval Augmented Generation (RAG)
* Policy grounded reasoning
* Evidence verification
* Audit logging
* Real-time monitoring dashboard

---

# 🚀 Live Demo

API Docs

```
[https://credlens-ai.onrender.com/docs](https://credlens-ai.onrender.com)
```

Dashboard

```
https://credlens-ai.onrender.com/dashboard/index.html
```

---

# 🧠 System Architecture

```
User Application
      │
      ▼
FastAPI Backend
      │
      ├── Risk Scoring Model (ML)
      │
      ├── RAG Policy Retrieval
      │      └── ChromaDB Vector Store
      │
      ├── Decision Agent (LLM)
      │
      ├── Evidence Verifier
      │
      └── Audit Log Database
              │
              ▼
      Real-time Dashboard
```

---

# ⚙️ Core Features

### 1️⃣ ML Risk Model

Calculates risk metrics including:

* Debt to Income Ratio
* Credit History
* Existing Loans
* Employment Stability

---

### 2️⃣ Retrieval Augmented Generation

Policies are retrieved using **semantic search** from:

```
ChromaDB Vector Database
```

Embedding model:

```
all-MiniLM-L6-v2
```

---

### 3️⃣ Deterministic Policy Engine

Hard rules run before any ML or LLM call. The decision label is irrevocable.

```python
# Example policy rules (simplified)
if dti_ratio > 0.50:
    return Decision.REJECT, "DTI_EXCEEDS_MAXIMUM"

if credit_score < 580:
    return Decision.REJECT, "CREDIT_SCORE_BELOW_MINIMUM"

if dti_ratio <= 0.35 and credit_score >= 700:
    return Decision.APPROVE, "STRONG_PROFILE"

return Decision.MANUAL_REVIEW, "BORDERLINE_CASE"
```

Every threshold maps to a named policy rule. When the policy changes, the rule changes — not the model.

### ML Risk Scoring

A Scikit-Learn classifier computes a continuous risk score (0.0 to 1.0) from:

- Debt-to-Income Ratio
- Credit Score
- Employment Stability
- Existing Loan Count
- Income vs Requested Loan Amount

The risk score is recorded in the audit log alongside the decision. It does not override the rules engine — it informs the explanation and the MANUAL_REVIEW threshold band.

### RAG Pipeline

Policy documents are embedded and stored in ChromaDB. At inference time:

```
Query: applicant profile + decision context
   |
   v
Embedding model: all-MiniLM-L6-v2 (runs locally)
   |
   v
ChromaDB semantic search -> top-k policy chunks
   |
   v
Context injection into LLM prompt
   |
   v
Structured explanation with policy citations
```

The embedding model runs locally — no external embedding API call, no additional latency.

### Evidence Verification

Prevents hallucinated policy citations by validating LLM outputs against retrieved policy chunks.

---

### 6️⃣ Audit Logging

Each decision is stored with:

* applicant data
* risk model output
* policy version
* explanation
* cryptographic hash chain

---

### 7️⃣ Real-time Dashboard

Displays:

* total decisions
* approvals
* rejections
* manual reviews

Auto-refresh every **2 seconds**.

---

# 🧪 Evaluation

Tested using **500 synthetic loan applications**.

Results:

```
Accuracy: 91.2%
Average Latency: 4.17s
```

---

# 🛠 Tech Stack

Backend

```
FastAPI
SQLModel
Python
```

Machine Learning

```
Scikit-Learn
Pandas
NumPy
```

Vector Database

```
ChromaDB
SentenceTransformers
```

LLM Integration

```
OpenAI API
```

Infrastructure

```
Docker
Render Deployment
```

---

## Quick Start

### Prerequisites

- Docker Desktop installed
- OpenAI API key

### Run with Docker

```bash
# Clone the repository
git clone https://github.com/mehakgoel20/credlens-ai.git
cd credlens-ai

# Build the image
docker build -t credlens-ai .

# Run the container
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key_here credlens-ai
```

### Access

| Interface            | URL                                              |
|----------------------|--------------------------------------------------|
| API Documentation    | http://localhost:8000/docs                       |
| Monitoring Dashboard | http://localhost:8000/dashboard/index.html       |
| Health Check         | http://localhost:8000/health                     |

---

## API Reference

### POST /evaluate

Evaluate a loan application.

**Request body:**

```json
{
  "case_id": 2,
  "case_hash": "65c7ee3e...",
  "prev_hash": "00166ddb...",
  "risk_output": {
    "risk_score": 0.38,
    "risk_bucket": "LOW",
    "dti": 0.167,
    "risk_engine": "rules"
  },
  "decision_output": {
    "decision": "APPROVE",
    "confidence": 0.85,
    "reasons": [
      {
        "reason_code": "FORCED_DECISION",
        "reason_text": "DTI <= 0.35 and credit history >= 12 months with low existing loans",
        "evidence": {
          "chunk_index": 0,
          "source": "LoanPolicy.pdf"
        }
      }
    ]
  }
}


Evaluation

Run automated regression tests:
python eval/run_eval.py


Expected output:

PASS/FAIL per test case
Final pass rate

### Limitations
ML risk model is baseline/demo unless trained on real-world repayment/default labels
PDF extraction quality depends on document formatting
Policy versioning and dedup improvements can be added for multi-policy environments
Production deployment would require DB migrations + RBAC + observability

### Future Improvements

Policy version control and dedup ingestion
Human review queue with role-based access control
Audit verification endpoint (/audit/verify)
Docker + CI/CD pipeline
Replace heuristic confidence with calibrated confidence model
Monitoring metrics (/metrics)

### Author

Built by Mehak Goel
Focus: Fintech-ready GenAI Engineering + Enterprise Systems