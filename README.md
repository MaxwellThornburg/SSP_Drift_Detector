# SSP Drift Detector

A Windows desktop application that detects compliance drift between your System Security Plan (SSP) and actual code implementation.

## Architecture

- **Backend**: Python (FastAPI) — parses SSP documents, analyzes repositories, and detects drift
- **Frontend**: React + Vite + Tailwind CSS — UI for uploading SSPs, entering repo info, and viewing compliance results

## Project Structure

```
SSP_Drift_Detector/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI route definitions
│   │   ├── services/     # Business logic (SSP parsing, repo analysis, drift detection)
│   │   └── models/       # Pydantic schemas
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── hooks/        # Custom React hooks (API calls)
│   │   └── styles/       # Tailwind CSS
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
├── .gitignore
└── README.md
```

## Getting Started

### Backend

```bash
cd backend
python -m venv venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API server runs at `http://localhost:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The dev server runs at `http://localhost:5173`.

### Docker (Backend)

```bash
cd backend
docker build -t ssp-drift-backend .
docker run -p 8000:8000 ssp-drift-backend
```

## How It Works

1. **Upload SSP** — Upload your System Security Plan document (DOCX format)
2. **Analyze Repository** — Provide a Git repository URL to analyze
3. **View Results** — See a compliance chart showing drift between documented controls and actual implementation