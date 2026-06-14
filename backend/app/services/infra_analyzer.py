import yaml
from typing import Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime, date

@dataclass
class SecurityPosture:
    # Identity
    human_auth_mfa: bool = False
    human_auth_cac_piv: bool = False
    account_review_cadence_days: int = None
    iam_users: List[Dict] = field(default_factory=list)
    
    # Network
    ingress_configs: List[Dict] = field(default_factory=list)
    egress_mode: str = None
    vpn_required_for_admin: bool = False
    
    # Compute
    k8s_stig_hardened: bool = False
    nodes_os: str = None
    nodes_stig_hardened: bool = False
    
    # Logging
    log_retention_online_days: int = None
    log_retention_archive_days: int = None
    event_types_logged: List[str] = field(default_factory=list)
    log_tamper_protection: str = None
    log_readers: List[str] = field(default_factory=list)
    
    # Storage
    db_encryption_at_rest: bool = False
    db_kms_rotation: bool = False
    db_backup_cadence: str = None
    db_backup_region: str = None
    db_last_restore_test: date = None
    obj_encryption_at_rest: bool = False
    obj_encryption_algo: str = None
    
    # Crypto
    fips_mode_enabled: bool = False
    legacy_crypto_exceptions: List[Dict] = field(default_factory=list)
    
    # Monitoring
    siem: str = None
    edr: str = None
    automated_response: str = None
    
    # Config Mgmt
    iac_tool: str = None
    drift_detection_enabled: bool = False
    drift_detection_cadence: str = None

class InfraAnalyzer:
    def __init__(self, yaml_content: str):
        self.yaml_content = yaml_content
        self.infra_data: Dict[str, Any] = {}
        self.posture = SecurityPosture()
        
    def analyze(self) -> SecurityPosture:
        try:
            self.infra_data = yaml.safe_load(self.yaml_content)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML format: {str(e)}")
            
        if not self.infra_data:
            raise ValueError("YAML file is empty")
            
        self._extract_posture()
        return self.posture
        
    def _parse_date(self, date_val) -> date:
        if not date_val: return None
        if isinstance(date_val, date): return date_val
        if isinstance(date_val, datetime): return date_val.date()
        try:
            return datetime.strptime(str(date_val), "%Y-%m-%d").date()
        except ValueError:
            return None

    def _extract_posture(self):
        data = self.infra_data
        
        # Identity
        identity = data.get('identity', {})
        human_auth = identity.get('human_auth', {})
        self.posture.human_auth_mfa = human_auth.get('mfa_required', False)
        self.posture.human_auth_cac_piv = human_auth.get('cac_piv_integration', False)
        self.posture.account_review_cadence_days = identity.get('account_review_cadence_days')
        
        # Network
        network = data.get('network', {})
        self.posture.ingress_configs = network.get('ingress', [])
        self.posture.egress_mode = network.get('egress', {}).get('mode')
        self.posture.vpn_required_for_admin = network.get('vpn', {}).get('required_for_admin', False)
        
        # Compute
        compute = data.get('compute', {})
        self.posture.k8s_stig_hardened = compute.get('kubernetes', {}).get('stig_hardened', False)
        nodes = compute.get('nodes', {})
        self.posture.nodes_os = nodes.get('os')
        self.posture.nodes_stig_hardened = nodes.get('stig_hardened', False)
        
        # Logging
        logging = data.get('logging', {})
        self.posture.log_retention_online_days = logging.get('retention_online_days')
        self.posture.log_retention_archive_days = logging.get('retention_archive_days')
        self.posture.event_types_logged = logging.get('event_types_logged', [])
        self.posture.log_tamper_protection = logging.get('tamper_protection')
        readers = logging.get('access_controls', {}).get('readers', [])
        self.posture.log_readers = [r.get('role') for r in readers if isinstance(r, dict)]
        
        # Storage
        storage = data.get('storage', {})
        db = storage.get('database', {})
        self.posture.db_encryption_at_rest = db.get('encryption_at_rest', False)
        self.posture.db_kms_rotation = db.get('kms_key_rotation') == 'enabled'
        self.posture.db_backup_cadence = db.get('backup_cadence')
        self.posture.db_backup_region = db.get('backup_region')
        self.posture.db_last_restore_test = self._parse_date(db.get('last_restore_test'))
        
        obj = storage.get('object_storage', {})
        self.posture.obj_encryption_at_rest = obj.get('encryption_at_rest', False)
        self.posture.obj_encryption_algo = obj.get('encryption_algorithm')
        
        # Crypto
        crypto = data.get('crypto', {})
        self.posture.fips_mode_enabled = crypto.get('fips_mode') == 'enabled'
        self.posture.legacy_crypto_exceptions = crypto.get('legacy_exceptions', [])
        
        # Monitoring
        monitoring = data.get('monitoring', {})
        self.posture.siem = monitoring.get('siem')
        self.posture.edr = monitoring.get('edr')
        self.posture.automated_response = monitoring.get('automated_response')
        
        # Config Mgmt
        config_mgmt = data.get('config_management', {})
        self.posture.iac_tool = config_mgmt.get('iac_tool')
        drift = config_mgmt.get('drift_detection', {})
        self.posture.drift_detection_enabled = drift.get('enabled', False)
        self.posture.drift_detection_cadence = drift.get('cadence')