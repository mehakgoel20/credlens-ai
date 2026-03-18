# CredLens AI — Enterprise Credit Decisioning Platform (GenAI + RAG + Guardrails)

CredLens AI is an **AI-assisted credit decision engine** designed to simulate how modern fintech companies evaluate loan applications using machine learning, policy retrieval, and explainable AI.

The system combines:

* Machine Learning risk scoring
* Retrieval Augmented Generation (RAG)
* Policy grounded reasoning
* Evidence verification
* Audit logging
* Real-time monitoring dashboard

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

Hard decision rules ensure regulatory compliance.

Example:

```
DTI > 0.50 → Reject
DTI ≤ 0.35 → Approve
Else → Manual Review
```

---

### 4️⃣ Explainable AI

Each decision contains:

* reason codes
* evidence references
* policy citations

---

### 5️⃣ Evidence Verification

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
```

---

# 📂 Project Structure

```text
credlens-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes_decision.py
│   │   │   ├── routes_docs.py
│   │   │   ├── routes_audit.py
│   │   │   ├── routes_report.py
│   │   │   └── routes_manual_review.py  (optional)
│   │   ├── services/
│   │   │   ├── rag_pipeline.py
│   │   │   ├── risk_model.py
│   │   │   ├── decision_agent.py
│   │   │   ├── evidence_verifier.py
│   │   │   └── report_generator.py
│   │   ├── db/
│   │   │   ├── session.py
│   │   │   └── models.py
│   │   ├── core/
│   │   │   └── security.py
│   │   ├── utils/
│   │   │   ├── audit_hash.py
│   │   │   └── doc_hash.py  (optional)
│   │   └── main.py
│   └── .env
│
├── frontend/
│   └── streamlit_app.py
│
├── eval/
│   ├── test_cases.json
│   └── run_eval.py
│
└── ml/
    ├── train.py
    └── artifacts/
        └── risk_model.pkl


## Setup Instructions

### 1) Clone Repo
```bash
git clone <your_repo_url>
cd credlens-ai

### 2) Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

### Create .env inside backend/
OPENAI_API_KEY=your_openai_key_here
APP_API_KEY=credlens-secret-key

### Run Backend
uvicorn app.main:app --reload --port 8002

### Swagger UI
http://127.0.0.1:8002/docs

### 3) Frontend Setup (Streamlit)
cd ../frontend
pip install streamlit requests
streamlit run streamlit_app.py


## Open:

http://localhost:8501

## Authentication

All secured endpoints require the following header:
X-API-KEY: credlens-secret-key

## Main API Endpoints
Upload Policy PDF
-> POST /docs/upload

Retrieve Policy Chunks (RAG)
-> POST /retrieve

Make Underwriting Decision
-> POST /decision/

List Audit Cases
-> GET /audit/cases?limit=10

Get Case by ID
-> GET /audit/cases/{case_id}

Download Compliance Report PDF
-> GET /report/{case_id}

Example Decision Output
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
