# 🔐 Secure Enterprise RAG System

[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Security Pipeline](https://img.shields.io/badge/Security-10--Stage%20Zero%20Trust-red?style=for-the-badge&logo=shield)](https://github.com/jahnavipriya7/secure-enterprise-rag)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%2018%20%2B%20Vite-61DAFB?style=for-the-badge&logo=react)](https://react.dev/)
[![FAISS](https://img.shields.io/badge/Vector%20DB-FAISS-00599C?style=for-the-badge)](https://github.com/facebookresearch/faiss)
[![Local LLM](https://img.shields.io/badge/LLM-Local%20Phi--3%20%2F%20Ollama-purple?style=for-the-badge)](https://ollama.ai/)

> **Zero Trust AI Architecture · Defense in Depth · Role-Based Access Control (RBAC) · PII Redaction & Output Guard**

A production-grade, enterprise-secure **Retrieval-Augmented Generation (RAG)** system built with Python FastAPI and React 18. Every query and response passes through an automated **10-Stage Security Pipeline** where the LLM is never trusted implicitly, preventing prompt injection attacks, unauthorized access to restricted documents, and sensitive data leakage.

---

## 📌 Key Highlights

- **🛡️ 10-Stage Zero Trust Security Pipeline**: Pre-retrieval prompt injection classification, role-based metadata filtering, PII scrubbing (Aadhaar, PAN, Emails, Phone numbers), secure prompt construction, local LLM generation, output response guard, and audit logging.
- **⚡ FAISS Vector Search & SentenceTransformers**: Dense semantic retrieval powered by `all-MiniLM-L6-v2` embeddings with pre-retrieval role metadata filtering.
- **🔒 Role-Based Access Control (RBAC)**: Enforced via JWT tokens with strict document-level permissions (Admin, HR, Employee, Intern).
- **🤖 Local & Air-Gapped LLM Execution**: Runs locally via **Ollama (Phi-3)** or built-in deterministic fallback engine — zero external API data sharing.
- **📊 Real-time Security Audit Trail**: Detailed JSON audit logs tracking risk scores, flagged security issues, model decisions, and user queries.
- **📄 Auto-Generated Beginner's Guide PDF**: Includes an embedded ReportLab PDF generator compiling a 6-chapter security handbook.

---

## 🔄 The 10-Stage Security Pipeline

```
                       User Input Query
                              │
                              ▼
  Stage 1: User Query Validation & Context Capturing
                              │
                              ▼
  Stage 2: Prompt Injection Detector (Regex + ML Classifier)  ──► [BLOCKED if Risk > Threshold]
                              │
                              ▼
  Stage 3: Role Validation (JWT Token Authorization)
                              │
                              ▼
  Stage 4: Pre-Retrieval Metadata Filtering (Document RBAC)
                              │
                              ▼
  Stage 5: Semantic Vector Search (FAISS + SentenceTransformers)
                              │
                              ▼
  Stage 6: PII & Sensitive Data Redactor (Aadhaar / PAN / Email)
                              │
                              ▼
  Stage 7: Secure System Prompt Construction
                              │
                              ▼
  Stage 8: Local Air-Gapped LLM Inference (Phi-3 / Ollama)
                              │
                              ▼
  Stage 9: Response Guard & Sanitization Scan
                              │
                              ▼
  Stage 10: Immutable JSON Security Audit Logging
                              │
                              ▼
                    Safe Enterprise Response
```

---

## 🔑 Test Accounts & Access Permissions

| Username | Password | Role | Document Access Scope |
| :--- | :--- | :--- | :--- |
| `admin_user` | `adminpassword` | **admin** | All 5 Enterprise Documents (Full Access) |
| `hr_user` | `hrpassword` | **hr** | HR Policies, Employee Handbook, Onboarding Guide |
| `emp_user` | `emppassword` | **employee** | Employee Handbook, Onboarding Guide |
| `intern_user` | `internpassword` | **intern** | Onboarding Guide Only |

---

## 🛠️ Quick Start Guide

### Option 1: Double-Click Startup (Windows)
Simply double-click **`START.bat`** in the root directory. It automatically initializes the Python virtual environment, starts the FastAPI server, launches the React dev server, and opens **`http://localhost:5173`** in your default browser.

### Option 2: Manual Terminal Startup

#### 1. Backend Server Setup (FastAPI)
```bash
# Navigate to project root directory
cd secure-enterprise-rag

# Install Python dependencies
pip install -r backend/requirements.txt

# Start FastAPI server
python -m uvicorn backend.main:app --reload --port 8000
```
*Backend API will run on `http://localhost:8000` (Swagger UI at `http://localhost:8000/docs`)*

#### 2. Frontend Client Setup (React + Vite)
```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start React Vite server
npm run dev
```
*Frontend app will run on `http://localhost:5173`*

---

## 📡 API Endpoints Summary

| Method | Endpoint | Auth Required | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/login` | None | Authenticate user credentials & receive JWT token |
| `POST` | `/api/rag/query` | JWT Bearer | Execute full 10-stage security pipeline & LLM generation |
| `GET` | `/api/documents` | JWT Bearer | List available document metadata according to user role |
| `GET` | `/api/admin/logs` | Admin Only | Retrieve JSON audit logs for security compliance |
| `GET` | `/api/pdf/download` | None | Generate & download the 6-chapter PDF security guide |
| `GET` | `/docs` | None | Interactive OpenAPI / Swagger documentation |

---

## 🏗️ Repository Directory Structure

```
secure-enterprise-rag/
├── START.bat                            # Automatic 1-click startup script for Windows
├── README.md                            # Complete system documentation
├── backend/
│   ├── main.py                          # FastAPI application & 10-stage pipeline execution
│   ├── auth.py                          # JWT token creation & authentication rules
│   ├── generate_pdf.py                  # ReportLab PDF guide generation script
│   ├── requirements.txt                 # Backend Python package requirements
│   ├── Secure_Enterprise_RAG_Guide.pdf  # Auto-generated comprehensive PDF handbook
│   ├── security/
│   │   ├── injection_detector.py        # Dual Regex + ML Prompt Injection Detector
│   │   ├── metadata_filter.py           # Pre-retrieval role-based document filter
│   │   ├── redactor.py                  # PII Regex scrubber (Aadhaar, PAN, Email, Phone)
│   │   └── response_guard.py            # Post-generation LLM output validator
│   ├── db/
│   │   └── vector_store.py              # FAISS index + SentenceTransformers manager
│   ├── llm/
│   │   └── local_llm.py                 # Local Ollama Phi-3 & offline fallback engine
│   └── utils/
│       └── logger.py                    # Structured JSON audit logging utility
└── frontend/
    ├── src/
    │   ├── App.jsx                      # Modern 4-tab React UI (Chat, Pipeline, Audit, Docs)
    │   ├── App.css                      # Custom dark glassmorphism styling
    │   └── main.jsx                     # Vite React entrypoint
    ├── package.json                     # Frontend Node dependencies
    └── vite.config.js                   # Vite configuration
```

---

## 📄 Beginner's Guide PDF

The repository includes an auto-generated, comprehensive 6-chapter security handbook saved at `backend/Secure_Enterprise_RAG_Guide.pdf`. Users can also download it live from the application header by clicking **"Download Guide"**.

---

<p align="center">
  Developed by <b>Pala Jahnavi Priya</b> · <a href="https://github.com/jahnavipriya7">@jahnavipriya7</a>
</p>
