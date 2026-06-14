import re
from typing import Dict, Set
from dataclasses import dataclass

@dataclass
class Control:
    id: str
    title: str
    description: str
    family: str

class SSPParser:
    def __init__(self):
        self.controls: Dict[str, Control] = {}
        
    def parse_content(self, content: str) -> Dict[str, Control]:
        self.controls = {}
        
        # 1. Normalize line endings and strip BOM (Byte Order Mark)
        if content.startswith('\ufeff'):
            content = content[1:]
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        
        lines = content.split('\n')
        current_control = None
        description_lines = []
        
        # 2. Highly permissive regex
        header_pattern = re.compile(r'^##\s+([A-Z]{2}-\d{1,2}(?:\.\d+)?(?:\s*$$\d+$$)?)\s*-\s*(.*)')
        
        for line in lines:
            stripped = line.strip()
            match = header_pattern.search(stripped)
            
            if match:
                # Save previous control
                if current_control:
                    current_control.description = ' '.join(description_lines).strip()
                    self.controls[current_control.id] = current_control
                
                control_id = match.group(1).replace(' ', '')
                title = match.group(2).strip()
                
                current_control = Control(
                    id=control_id,
                    title=title,
                    description="",
                    family=control_id.split('-')[0]
                )
                description_lines = []
            elif current_control and stripped and not stripped.startswith('#'):
                description_lines.append(stripped)
                
        # Save the last control
        if current_control:
            current_control.description = ' '.join(description_lines).strip()
            self.controls[current_control.id] = current_control
            
        # DEBUG LOGS: Check your backend terminal for these!
        print(f"[SSP PARSER DEBUG] Content length: {len(content)} chars")
        print(f"[SSP PARSER DEBUG] Total controls found: {len(self.controls)}")
        if self.controls:
            print(f"[SSP PARSER DEBUG] Controls: {list(self.controls.keys())}")
        else:
            print(f"[SSP PARSER DEBUG] First 100 chars of file: {repr(content[:100])}")
            
        return self.controls

    def get_required_controls(self) -> Set[str]:
        return set(self.controls.keys())
        
    def get_control(self, control_id: str) -> Control:
        return self.controls.get(control_id)