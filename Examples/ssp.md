# AEGIS-LOG System Security Plan (Excerpts)

- Document version: 2.3
- Last reviewed: 2024-08-12
- Authoring office: PMO AEGIS-LOG
- System categorization: Moderate (per FIPS 199)

---

## AC-2 - Account Management

The AEGIS-LOG system uses centralized identity management via the DoD CAC/PIV
infrastructure for all human users. Service accounts are managed through AWS
IAM with quarterly access reviews. All accounts are reviewed by the ISSO
within 30 days of personnel changes.

## AC-3 - Access Enforcement

Role-based access control is enforced at the application layer. Three roles
are defined: read-only viewer, operator, and administrator. All access
decisions are logged.

## AC-17 - Remote Access

All remote access to AEGIS-LOG occurs over the DoDIN via approved VPN
endpoints. Direct internet exposure of any system component is prohibited.
Administrative access requires jump host traversal.

## AU-2 - Event Logging

The system logs the following event types: authentication attempts (success
and failure), privilege escalations, configuration changes, data access
events for records marked CUI, and system errors. Logs are retained for one
year online and three years archived.

## AU-9 - Protection of Audit Information

Audit logs are written to a tamper-evident store. Access to logs is
restricted to the ISSO and SOC personnel. Logs are encrypted at rest.

## CM-2 - Baseline Configuration

The system maintains a documented baseline configuration in version control.
All infrastructure is declared as code. Drift from baseline is reviewed
weekly by the engineering lead.

## CM-6 - Configuration Settings

All EC2 instances are hardened per the DISA STIG for Red Hat Enterprise
Linux 8. All Kubernetes clusters are configured per the Kubernetes STIG.
Container images are scanned against the DoD Iron Bank baseline before
deployment.

## CP-9 - System Backup

User data and system configuration are backed up daily. Backups are
encrypted and stored in a geographically separate AWS region. Backup
restoration is tested quarterly.

## IA-2 - Identification and Authentication

All human users authenticate via CAC/PIV. Multi-factor authentication is
required for all administrative actions. Service-to-service authentication
uses short-lived tokens issued by the platform identity broker.

## IA-5 - Authenticator Management

Passwords, where used for break-glass access, conform to DoD password
complexity requirements: minimum 15 characters, complexity requirements per
DoD policy, rotation every 60 days.

## SC-7 - Boundary Protection

The system enforces boundary protection through AWS security groups, a
managed WAF, and network ACLs. All ingress traffic is inspected. Egress is
restricted to an allowlist of approved external endpoints.

## SC-8 - Transmission Confidentiality and Integrity

All data in transit is protected using TLS 1.2 or higher. Mutual TLS is
used for service-to-service communication within the cluster.

## SC-13 - Cryptographic Protection

All cryptographic modules in use are FIPS 140-2 validated. The system does
not use any cryptographic primitive that has not been validated.

## SC-28 - Protection of Information at Rest

All data at rest is encrypted using AES-256. Encryption keys are managed in
AWS KMS with automatic annual rotation. Database storage volumes, object
storage, and backup volumes are all encrypted.

## SI-4 - System Monitoring

The system is monitored continuously for indicators of compromise. Alerts
are forwarded to the program SOC. Anomalous behavior triggers an automated
incident response workflow.`