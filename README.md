# CredLens AI — Enterprise Credit Decisioning Platform (GenAI + RAG + Guardrails)

CredLens AI is an enterprise-style fintech decisioning system that evaluates personal loan applications using **policy-grounded GenAI**, **Retrieval-Augmented Generation (RAG)**, and **deterministic guardrails**. It ingests official loan policy documents (PDFs), retrieves relevant rules using a vector database, generates structured credit decisions (**APPROVE / REJECT / MANUAL_REVIEW**) with evidence citations, logs every case with tamper-evident audit hashes, and produces downloadable compliance reports.

This project is designed to simulate how real underwriting decision systems work inside fintech/product-based companies, where explainability, policy compliance, auditability, and safe decision boundaries matter more than “just using an LLM.”

---

## Key Features

### 1) Policy Document Ingestion (PDF → Knowledge Base)
- Upload loan policy PDFs
- Extract and chunk text
- Store chunks in ChromaDB vector database

### 2) RAG Retrieval (Grounded Decisions)
- Retrieves the most relevant policy chunks for underwriting decisions
- Enables evidence-backed reasoning with `chunk_index` and `source` references

### 3) Credit Risk Scoring (Rules + ML-ready)
- Computes risk indicators including **DTI (Debt-to-Income Ratio)**
- Provides `risk_score`, `risk_bucket`, and structured `reason_codes`
- Supports ML scoring with fallback to deterministic rules

### 4) Deterministic Guardrails (Fintech-Safe Decisioning)
Final decision is never fully delegated to the LLM:
- **DTI > 0.50 → REJECT (hard rule)**
- **DTI ≤ 0.35 + good profile → APPROVE (hard rule)**
- Else → **MANUAL_REVIEW**

The LLM is used for explanation generation and structured output formatting.

### 5) Evidence Verifier (Anti-Hallucination Guard)
- Automatically re-verifies evidence citations using retrieval
- Ensures reason codes map to correct policy chunks

### 6) Audit Logging (Case Management)
- Every decision is stored as a unique `case_id`
- Stores full applicant input + risk output + decision output

### 7) Tamper-Evident Audit Trail (Hash Chaining)
- Implements `prev_hash → case_hash` chaining
- Makes logs tamper-evident (audit-grade)

### 8) Compliance Report Generator (PDF)
- Generates a downloadable decision report for each case
- Includes:
  - applicant summary
  - risk output
  - final decision
  - reasons with evidence citations
  - next steps

### 9) API Security (Tier-1)
- Request authentication via `X-API-KEY` header

### 10) Evaluation Suite
- Runs regression tests using predefined decision test cases
- Tracks decision correctness across scenarios

### 11) Streamlit Dashboard (Demo UI)
- Upload policy PDFs
- Enter applicant details
- Generate decision + download compliance report

---

## Tech Stack

**Backend**
- FastAPI (API layer)
- SQLModel + SQLite (audit case database)
- ChromaDB (vector database)
- OpenAI API (GenAI reasoning + embeddings)
- fpdf2 (PDF report generation)

**Frontend**
- Streamlit (demo dashboard)

---

## Project Structure

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