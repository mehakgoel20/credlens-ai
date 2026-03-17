# CredLens AI

### Explainable Loan Decision System using RAG + ML

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
https://credlens-ai.onrender.com/docs
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
Render Deployment
```

---

# 📂 Project Structure

```
credlens-ai
│
├── backend
│   ├── api
│   ├── services
│   ├── db
│   └── models
│
├── dashboard
│   └── index.html
│
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

# 🔒 Security

* API Key Authentication
* Deterministic Policy Rules
* Audit Hash Chain
* Grounding Verification

---

# 📈 Future Improvements

* Human reviewer interface
* Bias detection
* Model monitoring
* Credit bureau integration
* Explainability dashboards

---

# 👩‍💻 Author

Mehak Goel

BTech Computer Science
Machine Learning / Generative AI Engineer
