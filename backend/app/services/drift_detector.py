# backend/app/services/drift_detector.py

from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from .ssp_parser import SSPParser, Control
from .repo_analyzer import RepoAnalyzer


@dataclass
class DriftResult:
    control_id: str
    status: str  # 'compliant', 'non_compliant', 'not_implemented'
    evidence: List[str]
    gap_description: str


class DriftDetector:
    """Detects drift between SSP requirements and repository implementation."""
    
    def __init__(self, ssp_parser: SSPParser, repo_analyzer: RepoAnalyzer):
        self.ssp_parser = ssp_parser
        self.repo_analyzer = repo_analyzer
        self.results: List[DriftResult] = []
    
    def detect(self) -> Dict:
        """
        Compare SSP requirements against repository implementation.
        Returns compliance report with drift analysis.
        """
        required = self.ssp_parser.get_required_controls()
        implemented = self.repo_analyzer.get_implemented_controls()
        evidence = self.repo_analyzer.control_evidence
        
        self.results = []
        
        for control_id in required:
            control = self.ssp_parser.get_control(control_id)
            
            if control_id in implemented:
                # Control is required and implemented
                result = DriftResult(
                    control_id=control_id,
                    status='compliant',
                    evidence=evidence.get(control_id, []),
                    gap_description="Control is implemented as required."
                )
            else:
                # Control is required but not implemented - DRIFT DETECTED
                result = DriftResult(
                    control_id=control_id,
                    status='non_compliant',
                    evidence=[],
                    gap_description=f"Control {control_id} is required by SSP but not found in repository."
                )
            
            self.results.append(result)
        
        # Check for controls implemented but not in SSP (shadow IT)
        for control_id in implemented:
            if control_id not in required:
                result = DriftResult(
                    control_id=control_id,
                    status='not_implemented',
                    evidence=evidence.get(control_id, []),
                    gap_description=f"Control {control_id} is implemented but not documented in SSP."
                )
                self.results.append(result)
        
        return self._generate_report()
    
    def _generate_report(self) -> Dict:
        """Generate compliance report from results."""
        total = len(self.results)
        compliant = sum(1 for r in self.results if r.status == 'compliant')
        non_compliant = sum(1 for r in self.results if r.status == 'non_compliant')
        not_implemented = sum(1 for r in self.results if r.status == 'not_implemented')
        
        compliance_percentage = (compliant / total * 100) if total > 0 else 0
        
        return {
            'summary': {
                'total_controls': total,
                'compliant': compliant,
                'non_compliant': non_compliant,
                'not_implemented': not_implemented,
                'compliance_percentage': round(compliance_percentage, 2)
            },
            'drift_detected': non_compliant > 0,
            'results': [
                {
                    'control_id': r.control_id,
                    'status': r.status,
                    'evidence': r.evidence,
                    'gap_description': r.gap_description
                }
                for r in self.results
            ]
        }
    
    def get_non_compliant_controls(self) -> List[DriftResult]:
        """Return list of non-compliant controls."""
        return [r for r in self.results if r.status == 'non_compliant']
    
    def get_compliance_by_family(self) -> Dict[str, Dict]:
        """Group compliance results by control family."""
        families = {}
        
        for result in self.results:
            family = result.control_id.split('-')[0] if '-' in result.control_id else 'UNKNOWN'
            
            if family not in families:
                families[family] = {
                    'total': 0,
                    'compliant': 0,
                    'non_compliant': 0
                }
            
            families[family]['total'] += 1
            if result.status == 'compliant':
                families[family]['compliant'] += 1
            elif result.status == 'non_compliant':
                families[family]['non_compliant'] += 1
        
        # Calculate percentages
        for family in families:
            total = families[family]['total']
            families[family]['compliance_percentage'] = round(
                families[family]['compliant'] / total * 100, 2
            ) if total > 0 else 0
        
        return families