# SSP Drift Detector

A Windows desktop application that detects compliance drift between your System Security Plan (SSP) and actual infrastructure configuration.

## Prerequisites

Before you begin, ensure you have the following installed:

| Tool | Version | Purpose | Download |
|------|---------|---------|----------|
| **Python** | 3.11+ | Backend runtime | [python.org](https://www.python.org/downloads/) |
| **Node.js** | 18+ | Frontend runtime | [nodejs.org](https://nodejs.org/) |
| **npm** | 9+ | Package manager | Included with Node.js |

### Verify Installations

```bash
python --version      # Should show 3.11+
node --version        # Should show v18+
npm --version         # Should show 9+
```

## Architecture

- **Backend**: Python (FastAPI) — parses SSP documents, analyzes infrastructure YAML, and detects drift using a rule engine.
- **Frontend**: React + Vite + TypeScript + Tailwind CSS — UI for uploading SSPs and infrastructure configs, and viewing compliance results.
- **Desktop Shell**: pywebview + PyInstaller — packages everything as a single Windows desktop executable.

## Project Structure

```text
SSP_Drift_Detector/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI route definitions
│   │   ├── services/     # Business logic (SSP parsing, YAML analysis, drift detection)
│   │   └── models/       # Pydantic schemas
│   ├── requirements.txt
│   └── run_desktop.py    # Entry point for pywebview desktop app
├── frontend/
│   ├── src/
│   │   ├── components/   # React components (FileUpload, ComplianceChart)
│   │   ├── hooks/        # Custom React hooks (API calls)
│   │   └── styles/       # Tailwind CSS
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
├── build.bat             # Windows build script
└── README.md
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/MaxwellThornburg/SSP_Drift_Detector.git
cd SSP_Drift_Detector
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API server runs at `http://localhost:8000`.

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The dev server runs at `http://localhost:5173`.

### 4. Docker (Backend)

```bash
cd backend
docker build -t ssp-drift-backend .
docker run -p 8000:8000 ssp-drift-backend
```

### 5. Build Desktop App

To build the Windows desktop application:

```bash
# From project root
build.bat
```

The single executable `SSP_Drift_Detector.exe` will be created in the project root.

## Development Dependencies

### Python Packages

Key packages from `requirements.txt`:

| Package | Purpose |
|---------|---------|
| fastapi | Web framework |
| uvicorn | ASGI server |
| pydantic | Data validation |
| PyYAML | Infrastructure YAML parsing |
| python-multipart | File upload handling |
| pyinstaller | Build executable |
| pywebview | Native window for desktop app |

Install all with:
```bash
pip install -r backend/requirements.txt
```

### Node.js Packages

Key packages from `package.json`:

| Package | Purpose |
|---------|---------|
| react | UI framework |
| recharts | Data visualization / charting |
| vite | Build tool |
| tailwindcss | Styling |
| typescript | Type safety |

Install all with:
```bash
cd frontend
npm install
```

## How It Works

1. **Upload SSP** — Upload your System Security Plan document (Markdown `.md` or text `.txt` format). The parser extracts control headers and descriptions.
2. **Upload Infrastructure Configuration** — Upload your infrastructure state as a YAML file. The analyzer extracts security posture attributes (Identity, Network, Compute, Logging, Storage, Crypto, Monitoring, Config Mgmt).
3. **Detect Drift** — The rule engine evaluates each SSP control against the infrastructure posture.
4. **View Results** — See a compliance chart and a detailed list of control evaluations showing **PASS**, **FAIL**, or **INDETERMINATE** statuses with evidence and gap descriptions.

## Troubleshooting

### "npm not found"
Install Node.js: https://nodejs.org/

### "python not found"
Install Python: https://www.python.org/downloads/

### Frontend crashes or goes blank after analyzing
This usually happens if the backend returns an unexpected JSON format. Open your browser's Developer Tools (F12), go to the **Console** tab, and look for the `Backend response:` log to verify the API payload. Ensure your backend server is running the latest code.

## License

GPL-3.0