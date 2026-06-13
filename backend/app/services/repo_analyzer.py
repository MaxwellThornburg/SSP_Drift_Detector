# backend/app/services/repo_analyzer.py

import os
import re
from typing import Dict, List, Set
from pathlib import Path


class RepoAnalyzer:
    """Analyzes repository for implemented security controls."""
    
    CONTROL_KEYWORDS = {
        'AC': ['access', 'authentication', 'authorization', 'login', 'permission'],
        'AU': ['audit', 'log', 'logging', 'monitor', 'event'],
        'CM': ['config', 'configuration', 'baseline', 'change control'],
        'CP': ['contingency', 'backup', 'recovery', 'disaster'],
        'IA': ['identification', 'authentication', 'credential', 'mfa', '2fa'],
        'IR': ['incident', 'response', 'breach', 'detection'],
        'MA': ['maintenance', 'patch', 'update'],
        'MP': ['media', 'encryption', 'sanitize', 'wipe'],
        'PE': ['physical', 'facility', 'environment'],
        'PL': ['planning', 'policy', 'procedure'],
        'PS': ['personnel', 'background', 'screening'],
        'RA': ['risk', 'assessment', 'vulnerability', 'threat'],
        'SA': ['system', 'acquisition', 'development', 'sdlc'],
        'SC': ['security', 'cryptographic', 'encryption', 'tls', 'ssl', 'cipher'],
        'SI': ['system', 'integrity', 'malware', 'antivirus', 'scan'],
        'ST': ['storage', 'encryption', 'data at rest'],
    }
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.implemented_controls: Set[str] = set()
        self.control_evidence: Dict[str, List[str]] = {}
    
    def analyze(self) -> Dict[str, List[str]]:
        """Analyze repository and return implemented controls with evidence."""
        self._scan_code_files()
        self._scan_config_files()
        self._scan_documentation()
        return self.control_evidence
    
    def _scan_code_files(self):
        """Scan source code files for control implementations."""
        code_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs', '.c', '.cpp'}
        
        for ext in code_extensions:
            for file_path in self.repo_path.rglob(f'*{ext}'):
                if self._should_skip(file_path):
                    continue
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        self._extract_controls_from_content(content, str(file_path))
                except Exception:
                    continue
    
    def _scan_config_files(self):
        """Scan configuration files for control evidence."""
        config_files = ['dockerfile', 'docker-compose.yml', 'kubernetes.yaml', 
                       '.github/workflows', 'terraform', 'ansible', 'policy']
        
        for pattern in config_files:
            for file_path in self.repo_path.rglob(f'*{pattern}*'):
                if self._should_skip(file_path):
                    continue
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        self._extract_controls_from_content(content, str(file_path))
                except Exception:
                    continue
    
    def _scan_documentation(self):
        """Scan documentation for control references."""
        doc_files = ['README.md', 'SECURITY.md', 'COMPLIANCE.md', 'POLICY.md']
        
        for doc in doc_files:
            doc_path = self.repo_path / doc
            if doc_path.exists():
                try:
                    with open(doc_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self._extract_controls_from_content(content, str(doc_path))
                except Exception:
                    continue
    
    def _extract_controls_from_content(self, content: str, file_path: str):
        """Extract control references from file content."""
        content_lower = content.lower()
        
        for family, keywords in self.CONTROL_KEYWORDS.items():
            for keyword in keywords:
                if keyword in content_lower:
                    # Map to specific control IDs based on context
                    control_ids = self._map_to_control_ids(family, content)
                    for cid in control_ids:
                        if cid not in self.control_evidence:
                            self.control_evidence[cid] = []
                        if file_path not in self.control_evidence[cid]:
                            self.control_evidence[cid].append(file_path)
                        self.implemented_controls.add(cid)
    
    def _map_to_control_ids(self, family: str, content: str) -> List[str]:
        """Map content to specific control IDs within a family."""
        control_ids = []
        
        # Pattern to find specific control numbers
        pattern = rf'{family}-(\d+)'
        matches = re.findall(pattern, content, re.IGNORECASE)
        
        for num in matches:
            control_ids.append(f"{family}-{num}")
        
        # If no specific ID found, add base controls for the family
        if not control_ids:
            base_controls = {
                'AC': ['AC-2', 'AC-3', 'AC-17'],
                'AU': ['AU-3', 'AU-6', 'AU-12'],
                'CM': ['CM-2', 'CM-6', 'CM-7'],
                'CP': ['CP-2', 'CP-9'],
                'IA': ['IA-2', 'IA-5'],
                'IR': ['IR-4', 'IR-5'],
                'MA': ['MA-2'],
                'MP': ['MP-2', 'MP-5'],
                'PE': ['PE-3'],
                'PL': ['PL-4'],
                'PS': ['PS-3'],
                'RA': ['RA-3', 'RA-5'],
                'SA': ['SA-3', 'SA-11'],
                'SC': ['SC-8', 'SC-13', 'SC-28'],
                'SI': ['SI-3', 'SI-4'],
                'ST': ['ST-8'],
            }
            control_ids.extend(base_controls.get(family, []))
        
        return control_ids
    
    def _should_skip(self, path: Path) -> bool:
        """Check if path should be skipped."""
        skip_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}
        return any(part in skip_dirs for part in path.parts)
    
    def get_implemented_controls(self) -> Set[str]:
        """Return set of implemented control IDs."""
        return self.implemented_controls