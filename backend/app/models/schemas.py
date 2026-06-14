from pydantic import BaseModel
from typing import List, Optional


class AnalysisRequest(BaseModel):
    infra_filename: str
    session_id: Optional[str] = None


class DriftItem(BaseModel):
    control_id: str
    control_name: str
    ssp_description: str
    actual_implementation: Optional[str] = None
    severity: str = "medium"
    details: Optional[str] = None


class DriftReport(BaseModel):
    source_file: str
    total_controls: int
    compliant: int
    non_compliant: int
    drift_items: List[DriftItem]


class SSPDocument(BaseModel):
    filename: str
    controls: List[dict]
    parsed_at: Optional[str] = None