# 🚀 PROVA - Enterprise AI Automated Testing & Quality Assurance Platform

PROVA is an enterprise-grade AI-powered test automation, repository discovery, business requirement synthesis, and test execution engine. It dynamically analyzes legacy and modern software repositories, extracts business domains & entities, generates comprehensive Business Requirement Documents (BRD), formulates right-sized UI & API test suites, and executes automated Playwright and Selenium tests with enterprise-grade state lifecycle tracking and visual evidence capture.

---

## 🌟 Key Features

- **🔍 Dynamic Repository Discovery Engine**:
  - Automatically scans repository source code, HTML/JSP/Thymeleaf templates, React components, and REST controllers.
  - Extracts pages, routes, interactive elements, form fields, and validation annotations without relying on hardcoded module names.
- **📄 Business Requirement Document (BRD) Synthesis**:
  - Generates comprehensive enterprise BRD reports (HTML & PDF formats) detailing Executive Summaries, Business Domains, System Architecture, UI Workflows, and Functional Rules.
- **🤖 Intelligent Test Coverage & Right-Sizing**:
  - Predicts UI and API test scenario counts scaled directly to discovered codebase complexity.
  - Eliminates test redundancy while ensuring full structural coverage.
- **🎭 Dual UI Test Automation (Playwright & Selenium)**:
  - Generates robust, executable Playwright (TypeScript/JavaScript) and Selenium (Java/TestNG) test suites.
  - Automatic base URL and port discovery (auto-scanning ports `8081`, `8080`, `8082`, etc.).
  - Captures full visual evidence (video recordings, step-by-step screenshots, trace zips).
- **⏳ Enterprise Test Lifecycle & State Management**:
  - Tracks test states: `Queued` $\rightarrow$ `Running` $\rightarrow$ `Retrying (Attempt N/3)` $\rightarrow$ `Passed` / `Failed` / `Skipped`.
  - Retries transient locator/timeout errors before finalizing failure counts.
- **📊 Interactive Analytics & Live Logs**:
  - Live execution log streaming and pass rate donut charts.
  - Downloadable raw HTML reports, test scripts, and execution packages.

---

## 🛠️ Architecture & Tech Stack

### Frontend
- **Framework**: React 18 (Vite)
- **Styling**: Vanilla CSS3, Tailwind CSS, Framer Motion
- **Icons**: Lucide React
- **Visualizations**: Recharts, Circular Progressbar, SyntaxHighlighter

### Backend
- **Framework**: Python 3.10+, FastAPI, Uvicorn
- **AI Synthesis**: Google Gemini 1.5 Pro / Flash
- **Task Queue**: Celery with Redis broker
- **Database**: SQLite / SQLAlchemy / Alembic migrations
- **Test Executors**: Playwright Node/Python API, Selenium WebDriver, JUnit/TestNG

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Node.js (v18+) & npm
- Docker / Redis (Optional, for Celery background tasks)

---

### 1. Automated Launcher (Windows PowerShell)

Run the included automated setup script:
```powershell
.\run_project.ps1
```

---

### 2. Manual Installation & Launch

#### Step 1: Start Python Backend (FastAPI)
```bash
cd python_backend
python -m venv venv

# On Windows
.\venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Launch FastAPI Server
python main.py
```
- **Backend API**: `http://localhost:8000`
- **Swagger Documentation**: `http://localhost:8000/docs`

#### Step 2: Start Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev
```
- **Web UI**: `http://localhost:5173`

---

## 📁 Repository Structure

```text
PROVA/
├── frontend/                     # React Vite Web Interface
│   ├── src/
│   │   ├── pages/                # Discovery, Strategy, Execution, Reports, Settings
│   │   ├── components/           # ChatbotWidget, TechIcons, UI elements
│   │   └── App.jsx               # Navigation, Workflow routing & Scroll Reset
│   ├── package.json
│   └── vite.config.js
├── python_backend/               # FastAPI Backend Service
│   ├── app/
│   │   ├── routers/              # API Endpoints (api.py, report_api.py, etc.)
│   │   ├── services/             # Analysis, BRD, Playwright, Selenium Services
│   │   ├── templates/            # BRD and Test Case HTML Templates
│   │   └── config.py             # Path allocation and active port resolution
│   ├── main.py                   # FastAPI Server Entrypoint
│   └── requirements.txt
├── run_project.ps1               # Automated PowerShell Launcher
├── start.sh                      # Shell Launcher
├── README.md                     # Main Project Documentation
└── EXPLANATION.md                # Comprehensive Architecture & Technical Explanation
```

---

## 📜 License
Internal Enterprise License - All Rights Reserved.
