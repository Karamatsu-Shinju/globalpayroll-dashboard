# GlobalPayroll Dashboard

A **multi-country payroll management dashboard** built as a case study project. It demonstrates product design thinking, full-stack development skills (Python + React), and deep domain knowledge in global employment compliance.

Built for the Remote Senior Product Designer application — showcasing systems thinking, cross-functional collaboration, and data-driven design for complex B2B SaaS.

---

## What This Demonstrates

| Skill | Evidence |
|-------|----------|
| **Systems thinking** | Multi-country payroll architecture with tax, compliance, and currency normalization |
| **Cross-functional collaboration** | Full-stack build bridging design (Figma-worthy UI) + engineering (Python API) |
| **Data-driven decisions** | KPIs, breakdowns, and trends derived from real payroll calculations |
| **Accessibility** | WCAG-compliant color contrast, keyboard-navigable UI, semantic HTML |
| **B2B SaaS design** | Dashboard for HR/Finance professionals managing global teams |
| **Technical depth** | Python FastAPI backend + React frontend — no no-code tools |

---

## Stack

**Backend:** Python 3.10+, FastAPI, SQLAlchemy, SQLite  
**Frontend:** React 19, TypeScript, Tailwind CSS, Vite  
**Charts:** Custom SVG (no charting library dependency)

---

## Quick Start

### Prerequisites
- Python 3.10+ with pip
- Node.js 20+ with npm

### 1. Clone / Download
```bash
cd case-study/
```

### 2. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
cd ..
```

### 3. Install Frontend Dependencies
```bash
npm install
```

### 4. Start Both Servers
```bash
python start.py
```

This will:
- Seed the SQLite database with realistic payroll data for 12 countries
- Start the FastAPI backend on `http://localhost:8000`
- Start the React dev server on `http://localhost:5173`
- Open your browser to `http://localhost:5173`

### Manual Start (if `start.py` doesn't work)

**Terminal 1 — Backend:**
```bash
cd backend
PYTHONPATH=. uvicorn app.main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
npm run dev
```

---

## Data Model

The database includes:
- **12 countries** with realistic tax rates, social security contributions, exchange rates, and compliance data
- **60 employees** across all countries with varied roles, departments, and salaries
- **3 payroll runs** (October, November, December 2024) with full calculation breakdowns

### Countries Covered
United States, United Kingdom, Germany, France, Portugal, Spain, Netherlands, Ireland, Canada, Brazil, India, Australia

### Tax Data Sources
All tax rates, social security contributions, and compliance data are sourced from OECD Taxing Wages 2024-2025, Trading Economics, and country-specific tax authority publications.

---

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/health` | Health check |
| `GET /api/dashboard/` | Full dashboard analytics (KPIs, breakdowns, trends) |
| `GET /api/countries/` | List all countries with payroll summary |
| `GET /api/countries/{id}` | Country detail with employees |
| `GET /api/employees/` | List employees with filters |
| `GET /api/payroll/runs` | List payroll runs |
| `GET /api/payroll/runs/{id}` | Payroll run detail with entries |

---

## Project Structure

```
case-study/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── database.py          # SQLite connection
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── seed.py              # Realistic seed data
│   │   └── routers/
│   │       ├── dashboard.py     # Dashboard analytics
│   │       ├── countries.py     # Country endpoints
│   │       ├── employees.py     # Employee endpoints
│   │       └── payroll.py       # Payroll endpoints
│   └── requirements.txt
├── src/
│   ├── lib/api.ts               # API client
│   ├── components/              # React components
│   ├── pages/                   # Page views
│   ├── App.tsx                  # Root component
│   └── main.tsx                 # Entry point
├── index.html
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── start.py                     # One-command launcher
```

---

## Screenshots

### Dashboard Overview
- **KPI Cards:** Total employees, monthly payroll, compliance rate, payroll growth
- **Payroll by Country:** Horizontal bar chart showing spend distribution
- **Tax Breakdown:** Stacked bar chart (income tax + employee SS + employer SS)
- **Department Distribution:** Donut chart with department breakdown
- **Compliance Status:** Per-country compliance indicators with tax burden

### Country Detail
- Full country profile with tax rates, exchange rates, mandatory benefits
- Side-by-side country comparison support

### Employee Directory
- Searchable, filterable table
- Multi-currency salary display (local + USD)
- Department and status filters

### Payroll Runs
- Processing history with status indicators
- Gross/net/deductions summary per run

---

## Why This Project?


1. **"Demonstrating maturity across the end-to-end design process"** — The project includes research (real tax data), problem definition (multi-country payroll complexity), solution design (dashboard UI), and validation (functional prototype).

2. **"Systems thinker who champions holistic thinking"** — The architecture models the entire global payroll ecosystem: countries, currencies, taxes, compliance, employees, and payroll runs as an interconnected system.

3. **"Effective cross-functional collaborator"** — Building both backend (Python) and frontend (React) demonstrates the ability to work across engineering boundaries.

4. **"Preference for B2B SaaS, HR Tech"** — Global payroll management is squarely in the HR Tech domain that Remote operates in.

5. **"Persuasive communication, storytelling narratives"** — The README and project structure tell a clear story of problem → research → solution → impact.
