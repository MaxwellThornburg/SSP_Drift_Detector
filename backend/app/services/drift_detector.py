from typing import Dict, List
from dataclasses import dataclass
from datetime import date, datetime
from .ssp_parser import SSPParser
from .infra_analyzer import InfraAnalyzer, SecurityPosture

@dataclass
class DriftResult:
    control_id: str
    status: str  # 'compliant', 'non_compliant', 'indeterminate'
    evidence: List[str]
    gap_description: str

class DriftDetector:
    def __init__(self, ssp_parser: SSPParser, infra_analyzer: InfraAnalyzer):
        self.ssp_parser = ssp_parser
        self.infra_analyzer = infra_analyzer
        self.posture: SecurityPosture = None
        self.results: List[DriftResult] = []
        self.today = date.today()
        
    def detect(self) -> Dict:
        self.posture = self.infra_analyzer.analyze()
        required_controls = self.ssp_parser.get_required_controls()
        self.results = []
        
        for control_id in required_controls:
            result = self._evaluate_control(control_id)
            self.results.append(result)
            
        return self._generate_report()
        
    def _evaluate_control(self, control_id: str) -> DriftResult:
        # Dispatch to specific evaluation methods dynamically
        evaluator = getattr(self, f"_eval_{control_id.replace('-', '_')}", None)
        if evaluator:
            return evaluator()
            
        return DriftResult(
            control_id=control_id,
            status='indeterminate',
            evidence=[],
            gap_description=f"Evaluation logic for {control_id} is not yet implemented in the rule engine."
        )

    # --- Specific Control Evaluators ---

    def _eval_AC_2(self) -> DriftResult:
        evidence, gaps = [], []
        if self.posture.human_auth_cac_piv: evidence.append("CAC/PIV integration enabled.")
        else: gaps.append("CAC/PIV integration is not enabled.")
            
        if self.posture.account_review_cadence_days and self.posture.account_review_cadence_days <= 90:
            evidence.append(f"Account review cadence is {self.posture.account_review_cadence_days} days (<= 90).")
        else:
            gaps.append(f"Account review cadence is {self.posture.account_review_cadence_days} days, exceeding 90-day limit.")
            
        return self._build_result('AC-2', evidence, gaps)

    def _eval_AC_3(self) -> DriftResult:
        return DriftResult('AC-3', 'indeterminate', [], "YAML schema lacks application-layer RBAC role definitions.")

    def _eval_AC_17(self) -> DriftResult:
        evidence, gaps = [], []
        if self.posture.vpn_required_for_admin: evidence.append("VPN required for admin access.")
        else: gaps.append("VPN is not required for admin access.")
        gaps.append("Jump host traversal cannot be verified from the current YAML schema.")
        return DriftResult('AC-17', 'indeterminate', evidence, " ".join(gaps))

    def _eval_AU_2(self) -> DriftResult:
        evidence, gaps = [], []
        required_events = {'auth_success', 'auth_failure', 'config_change', 'cui_data_access', 'system_error'}
        logged_events = set(self.posture.event_types_logged)
        
        if logged_events.issuperset(required_events):
            evidence.append("All required event types are logged.")
        else:
            gaps.append(f"Missing required event types: {', '.join(required_events - logged_events)}")
            
        if self.posture.log_retention_online_days and self.posture.log_retention_online_days >= 365:
            evidence.append(f"Online retention is {self.posture.log_retention_online_days} days (>= 365).")
        else:
            gaps.append(f"Online retention is {self.posture.log_retention_online_days} days, failing 1-year requirement.")
            
        if self.posture.log_retention_archive_days and self.posture.log_retention_archive_days >= 1095:
            evidence.append(f"Archive retention is {self.posture.log_retention_archive_days} days (>= 1095).")
        else:
            gaps.append(f"Archive retention is {self.posture.log_retention_archive_days} days, failing 3-year requirement.")
            
        return self._build_result('AU-2', evidence, gaps)

    def _eval_AU_9(self) -> DriftResult:
        evidence, gaps = [], []
        if self.posture.log_tamper_protection:
            evidence.append(f"Tamper protection enabled: {self.posture.log_tamper_protection}.")
        else:
            gaps.append("Tamper protection is not configured.")
            
        allowed_roles = {'isso', 'soc-analyst'} # Mapping "SOC personnel" to YAML's "soc-analyst"
        actual_roles = set(self.posture.log_readers)
        unauthorized = actual_roles - allowed_roles
        
        if not unauthorized:
            evidence.append(f"Log access restricted to authorized roles.")
        else:
            gaps.append(f"Unauthorized roles have log access: {', '.join(unauthorized)}")
            
        return self._build_result('AU-9', evidence, gaps)

    def _eval_CM_2(self) -> DriftResult:
        evidence, gaps = [], []
        if self.posture.iac_tool: evidence.append(f"IaC tool configured: {self.posture.iac_tool}.")
        else: gaps.append("No IaC tool configured.")
            
        if self.posture.drift_detection_enabled:
            evidence.append(f"Drift detection enabled ({self.posture.drift_detection_cadence} cadence).")
        else:
            gaps.append("Drift detection is not enabled.")
            
        return self._build_result('CM-2', evidence, gaps)

    def _eval_CM_6(self) -> DriftResult:
        evidence, gaps = [], []
        if self.posture.nodes_stig_hardened: evidence.append(f"Nodes ({self.posture.nodes_os}) are STIG hardened.")
        else: gaps.append("Nodes are not STIG hardened.")
            
        if self.posture.k8s_stig_hardened: evidence.append("Kubernetes cluster is STIG hardened.")
        else: gaps.append("Kubernetes cluster is not STIG hardened.")
            
        gaps.append("Container image scanning against DoD Iron Bank cannot be verified from YAML.")
        return DriftResult('CM-6', 'indeterminate', evidence, " ".join(gaps))

    def _eval_CP_9(self) -> DriftResult:
        evidence, gaps = [], []
        if self.posture.db_backup_cadence == 'daily': evidence.append("Database backups configured daily.")
        else: gaps.append(f"Database backup cadence is '{self.posture.db_backup_cadence}', expected 'daily'.")
            
        if self.posture.db_last_restore_test:
            days_since_test = (self.today - self.posture.db_last_restore_test).days
            if days_since_test <= 90:
                evidence.append(f"Last restore test was {days_since_test} days ago (<= 90).")
            else:
                gaps.append(f"Last restore test was {days_since_test} days ago, exceeding quarterly (90 days) limit.")
        else:
            gaps.append("No record of a backup restore test.")
            
        return self._build_result('CP-9', evidence, gaps)

    def _eval_IA_2(self) -> DriftResult:
        evidence, gaps = [], []
        if self.posture.human_auth_cac_piv: evidence.append("Human users authenticate via CAC/PIV.")
        else: gaps.append("CAC/PIV authentication not enabled.")
            
        if self.posture.human_auth_mfa: evidence.append("MFA is required.")
        else: gaps.append("MFA is not required.")
            
        return self._build_result('IA-2', evidence, gaps)

    def _eval_IA_5(self) -> DriftResult:
        return DriftResult('IA-5', 'indeterminate', [], "Break-glass password policies are not defined in the YAML schema.")

    def _eval_SC_7(self) -> DriftResult:
        evidence, gaps = [], []
        all_waf = True
        for ing in self.posture.ingress_configs:
            if not ing.get('waf_attached'):
                all_waf = False
                gaps.append(f"WAF is not attached to {ing.get('type')} ingress.")
                
        if all_waf and self.posture.ingress_configs: evidence.append("WAF attached to all ingress points.")
            
        if self.posture.egress_mode == 'allowlist': evidence.append("Egress restricted to allowlist.")
        else: gaps.append("Egress is not restricted to an allowlist.")
            
        return self._build_result('SC-7', evidence, gaps)

    def _eval_SC_8(self) -> DriftResult:
        evidence, gaps = [], []
        for ing in self.posture.ingress_configs:
            tls = str(ing.get('tls_version_min', '0'))
            try:
                if float(tls) < 1.2:
                    gaps.append(f"{ing.get('type')} ingress allows TLS {tls}, below the 1.2 minimum.")
                else:
                    evidence.append(f"{ing.get('type')} ingress enforces TLS {tls} or higher.")
            except ValueError:
                gaps.append(f"Invalid TLS version format for {ing.get('type')}: {tls}")
                
        return self._build_result('SC-8', evidence, gaps)

    def _eval_SC_13(self) -> DriftResult:
        evidence, gaps = [], []
        if self.posture.fips_mode_enabled: evidence.append("FIPS mode is enabled globally.")
        else: gaps.append("FIPS mode is not enabled globally.")
            
        for exc in self.posture.legacy_crypto_exceptions:
            if not exc.get('fips_validated'):
                waiver_exp = exc.get('waiver_expires')
                if waiver_exp:
                    try:
                        exp_date = datetime.strptime(str(waiver_exp), "%Y-%m-%d").date()
                        if exp_date < self.today:
                            gaps.append(f"Legacy exception for {exc.get('service')} uses unvalidated crypto and waiver expired.")
                        else:
                            evidence.append(f"Legacy exception for {exc.get('service')} has active waiver.")
                    except ValueError:
                        gaps.append(f"Invalid waiver expiration date for {exc.get('service')}.")
                else:
                    gaps.append(f"Legacy exception for {exc.get('service')} uses unvalidated crypto with no waiver.")
                    
        return self._build_result('SC-13', evidence, gaps)

    def _eval_SC_28(self) -> DriftResult:
        evidence, gaps = [], []
        if self.posture.db_encryption_at_rest and self.posture.obj_encryption_at_rest:
            evidence.append("Encryption at rest enabled for database and object storage.")
        else:
            if not self.posture.db_encryption_at_rest: gaps.append("Database encryption at rest is disabled.")
            if not self.posture.obj_encryption_at_rest: gaps.append("Object storage encryption at rest is disabled.")
            
        if self.posture.obj_encryption_algo == 'AES256': evidence.append("Object storage uses AES-256.")
        else: gaps.append(f"Object storage uses {self.posture.obj_encryption_algo}, expected AES256.")
            
        if self.posture.db_kms_rotation: evidence.append("KMS key rotation is enabled.")
        else: gaps.append("KMS key rotation is not enabled.")
            
        return self._build_result('SC-28', evidence, gaps)

    def _eval_SI_4(self) -> DriftResult:
        evidence, gaps = [], []
        if self.posture.siem: evidence.append(f"SIEM configured: {self.posture.siem}")
        else: gaps.append("No SIEM configured.")
        
        if self.posture.edr: evidence.append(f"EDR configured: {self.posture.edr}")
        else: gaps.append("No EDR configured.")
        
        if self.posture.automated_response in ['full', True]:
            evidence.append("Automated incident response workflow is fully enabled.")
        elif self.posture.automated_response == 'partial':
            gaps.append("Automated incident response is only 'partial', SSP requires full automated workflow.")
        else:
            gaps.append("Automated incident response is not configured.")
            
        return self._build_result('SI-4', evidence, gaps)

    # --- Helper Methods ---

    def _build_result(self, control_id: str, evidence: List[str], gaps: List[str]) -> DriftResult:
        status = 'compliant' if not gaps else 'non_compliant'
        gap_desc = " ".join(gaps) if gaps else "Control is implemented as required."
        return DriftResult(control_id, status, evidence, gap_desc)

    def _generate_report(self) -> Dict:
        total = len(self.results)
        compliant = sum(1 for r in self.results if r.status == 'compliant')
        non_compliant = sum(1 for r in self.results if r.status == 'non_compliant')
        indeterminate = sum(1 for r in self.results if r.status == 'indeterminate')
        
        # Calculate percentage based ONLY on determined controls
        determined = compliant + non_compliant
        compliance_percentage = (compliant / determined * 100) if determined > 0 else 0
        
        return {
            'summary': {
                'total_controls': total,
                'compliant': compliant,
                'non_compliant': non_compliant,
                'indeterminate': indeterminate,
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