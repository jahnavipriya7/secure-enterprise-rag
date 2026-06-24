# 🔐 Secure Enterprise RAG System

> Zero Trust · Defense in Depth · Local LLM · Role-Based Access Control

A production-grade, enterprise-secure RAG (Retrieval-Augmented Generation) system with a 10-stage security pipeline. The LLM is **never trusted** — every query and every response is validated through multiple independent security layers.

---

## 🚀 Quick Start (Double-Click)

**Just double-click `START.bat`** — it automatically starts both servers and opens the browser.

---

## 🛠 Manual Start

### Backend (FastAPI)
```bash
# From CIS/ directory
python -m uvicorn backend.main:app --reload --port 8000
```

### Frontend (React + Vite)
```bash
# From CIS/frontend/ directory
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## 🔑 Test Accounts

| Username      | Password        | Role     | Access Level              |
|---------------|-----------------|----------|---------------------------|
| `admin_user`  | `adminpassword` | admin    | All 5 documents           |
| `hr_user`     | `hrpassword`    | hr       | HR + Employee + Onboarding|
| `emp_user`    | `emppassword`   | employee | Employee + Onboarding     |
| `intern_user` | `internpassword`| intern   | Onboarding only           |

---

## 🔄 The 10-Stage Security Pipeline

```
User Query
    ↓
[1] Injection Detector     ← Regex + ML classifier
    ↓
[2] Role Validation        ← JWT verification
    ↓
[3] Metadata Filtering     ← Pre-retrieval RBAC
    ↓
[4] Semantic Retrieval     ← FAISS vector search
    ↓
[5] PII Redaction          ← Aadhaar / PAN / Email scrub
    ↓
[6] Secure Prompt Build    ← System prompt assembly
    ↓
[7] Local LLM              ← Phi-3 / Fallback engine
    ↓
[8] Response Guard         ← Output PII scan
    ↓
[9] Audit Logging          ← JSON compliance log
    ↓
Secure Response
```

---

## 📁 Project Structure

```
CIS/
├── START.bat                        ← Double-click to run everything
├── backend/
│   ├── main.py                      ← FastAPI app + 10-stage pipeline
│   ├── auth.py                      ← JWT authentication
│   ├── generate_pdf.py              ← PDF guide generator
│   ├── Secure_Enterprise_RAG_Guide.pdf
│   ├── security/
│   │   ├── injection_detector.py   ← Regex + ML classifier
│   │   ├── metadata_filter.py      ← Role-based pre-filtering
│   │   ├── redactor.py             ← PII scrubbing engine
│   │   └── response_guard.py       ← Output validation
│   ├── db/
│   │   └── vector_store.py         ← FAISS + SentenceTransformers
│   ├── llm/
│   │   └── local_llm.py            ← Ollama + local fallback
│   └── utils/
│       └── logger.py               ← Audit logging
└── frontend/
    ├── src/
    │   ├── App.jsx                  ← Full 4-tab React UI
    │   └── App.css                  ← Premium dark glassmorphism CSS
    └── index.html
```

---

## 🌐 API Endpoints

| Method | Endpoint               | Auth     | Description                    |
|--------|------------------------|----------|--------------------------------|
| POST   | `/api/auth/login`      | None     | Get JWT token                  |
| POST   | `/api/rag/query`       | Required | Run full security pipeline     |
| GET    | `/api/documents`       | Required | List all documents             |
| GET    | `/api/admin/logs`      | Admin    | View audit logs                |
| GET    | `/api/pdf/download`    | None     | Download beginner's guide PDF  |
| GET    | `/docs`                | None     | Swagger interactive API docs   |

---

## 📄 Beginner's Guide PDF

A comprehensive 6-chapter PDF guide is auto-generated at `backend/Secure_Enterprise_RAG_Guide.pdf`.  
It is also downloadable via the **"Download Guide"** button in the app.

---

## 🛡️ Security Features

- **Prompt Injection Detection**: Regex scanner + TF-IDF/LogisticRegression ML classifier
- **Zero Trust**: Every input is assumed malicious until verified
- **Role-Based Access Control**: JWT + metadata pre-filtering
- **PII Protection**: Aadhaar, PAN, Email, Phone redaction before LLM
- **Local LLM**: No cloud API calls — Ollama (Phi-3) or built-in fallback
- **Response Guard**: Output validation before user sees it
- **Audit Trail**: Every event logged to `backend/logs/audit.log`

---

## 📦 Tech Stack

| Layer          | Technology                          |
|----------------|-------------------------------------|
| Frontend       | React 18 + Vite                     |
| Backend        | FastAPI + Uvicorn                   |
| Auth           | JWT (PyJWT)                         |
| Vector DB      | FAISS (faiss-cpu)                   |
| Embeddings     | all-MiniLM-L6-v2 (SentenceTransformers) |
| ML Classifier  | TF-IDF + Logistic Regression (scikit-learn) |
| LLM            | Phi-3 via Ollama / Local Fallback   |
| PDF            | ReportLab                           |
