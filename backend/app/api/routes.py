# backend/app/api/routes.py

import json
import tempfile
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from git import Repo
from app.models.schemas import DriftReport, DriftItem
from app.services.ssp_parser import SSPParser, Control
from app.services.repo_analyzer import RepoAnalyzer
from app.services.drift_detector import DriftDetector

router = APIRouter()


@router.post("/upload-ssp", response_model=dict)
async def upload_ssp(file: UploadFile = File(...)):
    """Upload and parse an SSP document. Returns parsed controls - no file persistence."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    try:
        # Read file content directly into memory
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Parse SSP content
        parser = SSPParser()
        controls = parser.parse_content(content_str)
        
        if not controls:
            raise HTTPException(status_code=400, detail="No controls found in SSP file")
        
        # Convert controls to serializable format
        controls_data = {
            cid: {
                "id": c.id,
                "title": c.title,
                "description": c.description,
                "implementation_status": c.implementation_status
            }
            for cid, c in controls.items()
        }
        
        return {
            "filename": file.filename,
            "status": "parsed",
            "controls_count": len(controls),
            "controls": controls_data
        }
        
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be valid UTF-8 text")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse SSP: {str(e)}")


@router.post("/analyze", response_model=DriftReport)
async def analyze_repo(
    repo_url: str = Form(...),
    branch: str = Form("main"),
    controls_json: str = Form(...)
):
    """Clone remote repository and analyze against the provided SSP controls."""
    repo_temp_dir = None
    
    try:
        # Parse controls from JSON
        try:
            controls_data = json.loads(controls_json)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid controls JSON")
        
        if not controls_data:
            raise HTTPException(status_code=400, detail="No controls provided")
        
        # Reconstruct SSPParser with the controls
        ssp_parser = SSPParser()
        ssp_parser.controls = {
            cid: Control(
                id=c["id"],
                title=c["title"],
                description=c["description"],
                implementation_status=c.get("implementation_status", "not_implemented")
            )
            for cid, c in controls_data.items()
        }
        
        # Clone the remote repository
        repo_temp_dir = tempfile.mkdtemp()
        try:
            Repo.clone_from(repo_url, repo_temp_dir, branch=branch, depth=1)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to clone repository: {str(e)}"
            )
        
        # Analyze the cloned repository
        repo_analyzer = RepoAnalyzer(repo_temp_dir)
        repo_analyzer.analyze()
        
        # Detect drift
        drift_detector = DriftDetector(ssp_parser, repo_analyzer)
        report = drift_detector.detect()
        
        # Build drift items from non-compliant controls
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
    raise HTTPException(
        status_code=404,
        detail="Results not cached. This application is stateless - please run analysis again."
    )