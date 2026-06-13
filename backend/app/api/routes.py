# backend/app/api/routes.py

import os
import tempfile
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from git import Repo
from app.models.schemas import DriftReport, AnalysisRequest, DriftItem
from app.services.ssp_parser import SSPParser
from app.services.repo_analyzer import RepoAnalyzer
from app.services.drift_detector import DriftDetector

router = APIRouter()


@router.post("/upload-ssp", response_model=dict)
async def upload_ssp(file: UploadFile = File(...)):
    """Upload an SSP document for parsing."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Save uploaded file to temporary location
    temp_dir = tempfile.mkdtemp()
    file_path = Path(temp_dir) / file.filename
    
    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Parse the SSP to verify it's valid
        parser = SSPParser()
        controls = parser.parse_file(str(file_path))
        
        return {
            "filename": file.filename,
            "status": "uploaded",
            "controls_found": len(controls),
            "temp_path": str(file_path),
            "temp_dir": temp_dir
        }
    except Exception as e:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise HTTPException(status_code=400, detail=f"Failed to parse SSP: {str(e)}")


@router.post("/analyze", response_model=DriftReport)
async def analyze_repo(
    repo_url: str = Form(...),
    branch: str = Form("main"),
    ssp_path: str = Form(...),
    ssp_filename: str = Form(...)
):
    """Analyze a remote repository against the uploaded SSP."""
    repo_temp_dir = None
    
    try:
        # Validate SSP file exists
        ssp_file = Path(ssp_path)
        if not ssp_file.exists():
            raise HTTPException(status_code=400, detail="SSP file not found. Upload it first.")
        
        # Clone the remote repository
        repo_temp_dir = tempfile.mkdtemp()
        try:
            repo = Repo.clone_from(repo_url, repo_temp_dir, branch=branch, depth=1)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to clone repository: {str(e)}")
        
        # Parse the SSP
        ssp_parser = SSPParser()
        ssp_parser.parse_file(str(ssp_file))
        
        # Analyze the repository
        repo_analyzer = RepoAnalyzer(repo_temp_dir)
        repo_analyzer.analyze()
        
        # Detect drift
        drift_detector = DriftDetector(ssp_parser, repo_analyzer)
        report = drift_detector.detect()
        
        # Convert results to DriftReport schema
        drift_items = []
        for result in report["results"]:
            if result["status"] == "non_compliant":
                control = ssp_parser.get_control(result["control_id"])
                drift_items.append(DriftItem(
                    control_id=result["control_id"],
                    control_name=control.title if control else result["control_id"],
                    ssp_description=control.description if control else "",
                    actual_implementation=None,
                    severity="high",
                    details=result["gap_description"]
                ))
        
        return DriftReport(
            repo_url=repo_url,
            total_controls=report["summary"]["total_controls"],
            compliant=report["summary"]["compliant"],
            non_compliant=report["summary"]["non_compliant"],
            drift_items=drift_items
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    finally:
        # Clean up cloned repository
        if repo_temp_dir:
            shutil.rmtree(repo_temp_dir, ignore_errors=True)


@router.get("/results/{session_id}", response_model=DriftReport)
async def get_results(session_id: str):
    """Retrieve cached analysis results."""
    # Since the app is stateless, this endpoint is not fully implemented.
    # For now, return a 404 indicating results are not cached.
    raise HTTPException(
        status_code=404, 
        detail="Results not found. The application is stateless - results are not cached. "
               "Please run the analysis again."
    )