from fastapi import APIRouter, UploadFile, File, Form
from app.models.schemas import DriftReport, AnalysisRequest

router = APIRouter()


@router.post("/upload-ssp", response_model=dict)
async def upload_ssp(file: UploadFile = File(...)):
    """Upload an SSP document for parsing."""
    # TODO: pass file to ssp_parser service
    return {"filename": file.filename, "status": "uploaded"}


@router.post("/analyze", response_model=DriftReport)
async def analyze_repo(request: AnalysisRequest):
    """Analyze a repository against the uploaded SSP."""
    # TODO: invoke repo_analyzer and drift_detector services
    return DriftReport(
        repo_url=request.repo_url,
        total_controls=0,
        compliant=0,
        non_compliant=0,
        drift_items=[],
    )


@router.get("/results/{session_id}", response_model=DriftReport)
async def get_results(session_id: str):
    """Retrieve cached analysis results."""
    # TODO: fetch from storage/cache
    pass