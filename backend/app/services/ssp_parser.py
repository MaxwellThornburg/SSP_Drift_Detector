# backend/app/services/ssp_parser.py

import re
from typing import Dict, List, Set
from dataclasses import dataclass


@dataclass
class Control:
    id: str
    title: str
    description: str
    implementation_status: str = "not_implemented"


class SSPParser:
    """Parser for System Security Plan (SSP) documents."""
    
    CONTROL_PATTERN = re.compile(r'([A-Z]{2}-\d{1,2}(?:\s*\(\d+\))?)')
    
    def __init__(self):
        self.controls: Dict[str, Control] = {}
    
    def parse_file(self, file_path: str) -> Dict[str, Control]:
        """Parse an SSP file and extract all controls."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return self.parse_content(content)
    
    def parse_content(self, content: str) -> Dict[str, Control]:
        """Parse SSP content string and extract controls."""
        self.controls = {}
        
        lines = content.split('\n')
        current_control = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for control ID patterns (e.g., AC-1, SC-7(1))
            match = self.CONTROL_PATTERN.match(line)
            if match:
                control_id = match.group(1).replace(' ', '')
                current_control = Control(
                    id=control_id,
                    title=line,
                    description=""
                )
                self.controls[control_id] = current_control
            
            elif current_control and line:
                current_control.description += line + " "
        
        return self.controls
    
    def get_required_controls(self) -> Set[str]:
        """Return set of required control IDs."""
        return set(self.controls.keys())
    
    def get_control(self, control_id: str) -> Control | None:
        """Get a specific control by ID."""
        return self.controls.get(control_id)