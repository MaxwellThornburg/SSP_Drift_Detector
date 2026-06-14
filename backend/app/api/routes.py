# backend/app/api/routes.py

import json
import tempfile
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.schemas import DriftReport, DriftItem
from app.services.ssp_parser import SSPParser, Control
from app.services.infra_analyzer import InfraAnalyzer
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


# REMOVED response_model=DriftReport so it returns the raw dictionary
@router.post("/analyze")
async def analyze_infra(
    ssp_file: UploadFile = File(...),
    infra_file: UploadFile = File(...)
):
    """Analyze infrastructure YAML file against the provided SSP document."""
    try:
        # Read and parse SSP file
        ssp_content = await ssp_file.read()
        ssp_content_str = ssp_content.decode('utf-8')
        
        ssp_parser = SSPParser()
        controls = ssp_parser.parse_content(ssp_content_str)
        
        if not controls:
            raise HTTPException(status_code=400, detail="No controls found in SSP file")
        
        # Read and parse the infrastructure YAML file
        infra_content = await infra_file.read()
        infra_content_str = infra_content.decode('utf-8')
        
        infra_analyzer = InfraAnalyzer(infra_content_str)
        try:
            infra_analyzer.analyze()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        # Detect drift
        drift_detector = DriftDetector(ssp_parser, infra_analyzer)
        report = drift_detector.detect()
        
        # Return the raw report dictionary directly! 
        # It already contains 'summary', 'drift_detected', and 'results' 
        # which perfectly matches the React frontend's AnalysisResult interface.
        return report
        
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Files must be valid UTF-8 text")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/results/{session_id}", response_model=DriftReport)
async def get_results(session_id: str):
    """Retrieve cached analysis results."""
    raise HTTPException(
        status_code=404,
        detail="Results not cached. This application is stateless - please run analysis again."
    )