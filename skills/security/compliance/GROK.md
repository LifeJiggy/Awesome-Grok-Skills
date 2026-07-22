---
name: "compliance"
category: "security"
version: "2.0.0"
tags: ["security", "compliance", "SOC2", "ISO27001", "PCI-DSS", "HIPAA", "GDPR", "NIST-800-53", "audit", "control-mapping"]
---

# Compliance

## Overview

Compliance is the practice of ensuring that security controls, policies, and processes meet regulatory, contractual, and industry standards. This module provides comprehensive tooling for mapping controls across frameworks (SOC 2, ISO 27001, PCI DSS, HIPAA, GDPR, NIST 800-53, CIS), generating audit evidence, tracking control effectiveness, and maintaining continuous compliance posture. Compliance is not the same as security — you can be compliant but insecure, or secure but non-compliant. The goal is to use compliance frameworks as structured minimum baselines that drive real security improvements, not as checkbox exercises.

The key challenge in compliance is the multiplier effect: a single control implementation often maps to multiple requirements across multiple frameworks. One SSH key rotation policy can satisfy SOC 2 CC6.1, PCI DSS 2.2, ISO 27001 A.9.4.3, NIST 800-53 IA-5(1), and HIPAA §164.312(a)(1). This module's control registry eliminates duplicated effort by maintaining a single source of truth for each control with automated multi-framework mapping. When a framework requirement changes, you immediately know which controls are affected.

This module bridges the gap between security engineering and GRC (Governance, Risk, and Compliance). Engineers implement controls; GRC teams need evidence that controls exist and are effective. The module automates evidence collection from infrastructure (configuration exports, access reviews, scan reports), generates audit-ready bundles, and provides real-time dashboards for compliance posture. It also tracks regulatory changes (PCI DSS 4.0, SOC 2 updates, new HIPAA guidance) and maps changes to existing controls, so you know exactly what needs updating when frameworks evolve.

## Core Capabilities

1. **Multi-Framework Control Registry** — Register a single control with mappings to multiple frameworks simultaneously. One well-documented control satisfies requirements across SOC 2, ISO 27001, PCI DSS, NIST 800-53, HIPAA, and GDPR. Track implementation status per framework.

2. **Gap Analysis** — Compare current controls against a target framework. Identify missing controls, partial implementations, and areas requiring new documentation. Generate prioritized remediation plans with effort estimates.

3. **Evidence Collection Automation** — Programmatically collect and organize audit evidence: configuration exports, access review exports, vulnerability scan reports, change logs, policy attestations, and deployment records. Schedule recurring evidence collection.

4. **Control Testing & Validation** — Schedule and execute control tests (access reviews, configuration audits, policy attestations, penetration test results). Track pass/fail status, generate findings, and maintain test history for audit evidence.

5. **Policy Management** — Version-control security policies, track employee policy acknowledgments, enforce annual review cycles, and map policies to framework controls. Template library for common policies (acceptable use, data classification, incident response).

6. **Audit Readiness Dashboard** — Real-time view of compliance posture across all frameworks. Highlight gaps, upcoming reviews, expired evidence, and overdue control tests. Executive-level summary with drill-down capability.

7. **Regulatory Change Monitoring** — Track framework updates (PCI DSS 4.0 changes, SOC 2 2024 updates, new HIPAA guidance, GDPR enforcement actions) and map changes to existing controls with impact assessment.

8. **Audit Evidence Bundling** — Generate audit-ready evidence packages organized by framework, control, and evidence type. Support for auditor portal upload, document management system integration, and evidence chain-of-custody tracking.

## Usage Examples

### Multi-Framework Control Registry

```python
from compliance import ControlRegistry, Framework, ControlStatus

registry = ControlRegistry()

# Register a control with multi-framework mappings
registry.register_control(
    control_id="SC-001",
    title="SSH Key Rotation",
    description="All SSH keys are rotated every 90 days and upon personnel departure",
    implementation="Automated via Ansible playbooks with Vault integration",
    owner="platform-team",
    review_frequency="quarterly",
    framework_mappings={
        Framework.SOC2: ["CC6.1", "CC6.3"],
        Framework.ISO27001: ["A.9.4.2", "A.9.4.3"],
        Framework.PCI_DSS: ["2.2", "8.2.4"],
        Framework.NIST_800_53: ["IA-5(1)", "AC-2(4)"],
        Framework.HIPAA: ["164.312(a)(1)"],
    },
    evidence_sources=["ansible_logs", "vault_audit", "hr_system"],
    test_procedure="Verify rotation logs show keys rotated within 90-day window"
)

# Query controls by framework
soc2_controls = registry.get_controls_for_framework(Framework.SOC2)
print(f"SOC 2 controls mapped: {len(soc2_controls)}")

# Query coverage for a specific framework
coverage = registry.get_framework_coverage(Framework.ISO27001)
print(f"ISO 27001 coverage: {coverage.implemented}/{coverage.total} "
      f"({coverage.percentage:.0f}%)")
print(f"  Fully implemented:  {coverage.fully_implemented}")
print(f"  Partially implemented: {coverage.partially_implemented}")
print(f"  Not implemented:    {coverage.not_implemented}")
```

### Gap Analysis

```python
from compliance import GapAnalyzer, TargetFramework, Priority

analyzer = GapAnalyzer(registry)

# Run gap analysis against target framework
gap_report = analyzer.analyze(
    target=TargetFramework.PCI_DSS,
    version="4.0",
    current_controls=registry.get_all_controls()
)

print(f"=== PCI DSS 4.0 Gap Analysis ===")
print(f"Fully implemented:    {gap_report.implemented}")
print(f"Partially implemented: {gap_report.partial}")
print(f"Missing:              {gap_report.missing}")
print(f"Compliance score:     {gap_report.score:.1%}")

# Print missing controls with priority
for gap in gap_report.missing_controls:
    print(f"\n  GAP: {gap.control_id} - {gap.title}")
    print(f"    Requirement: {gap.framework_requirement}")
    print(f"    Priority:    {gap.priority}")
    print(f"    Effort:      {gap.estimated_effort}")
    print(f"    Suggested:   {gap.suggested_control}")

# Generate remediation roadmap
roadmap = gap_report.generate_roadmap(target_date="2024-12-31")
print(f"\n=== Remediation Roadmap ===")
for phase in roadmap.phases:
    print(f"Phase {phase.number}: {phase.name} ({phase.timeline})")
    for item in phase.items:
        print(f"  - {item.control_id}: {item.title} ({item.effort})")
```

### Evidence Collection & Audit Bundling

```python
from compliance import EvidenceCollector, EvidenceType, AuditBundle

collector = EvidenceCollector(storage_path="./evidence/2024-Q1")

# Collect different types of evidence
evidence = []

# Access review evidence
evidence.append(collector.collect_access_review(
    system="AWS IAM",
    review_date="2024-01-15",
    reviewer="security-team",
    findings="No excessive permissions found. 3 stale roles removed.",
    evidence_file="iam_access_review_q1.xlsx"
))

# Configuration evidence
evidence.append(collector.collect_configuration_export(
    system="nginx",
    config_path="/etc/nginx/nginx.conf",
    compliance_check="TLS 1.2+ enforced, HSTS enabled, X-Frame-Options DENY",
    screenshot="nginx_tls_config.png"
))

# Vulnerability scan evidence
evidence.append(collector.collect_scan_report(
    scanner="trivy",
    target="web-prod-01",
    report_path="./scans/web-prod-01.json",
    summary="0 critical, 2 high, 15 medium",
    remediation_status="All high findings remediated within SLA"
))

# Policy attestation evidence
evidence.append(collector.collect_policy_attestation(
    policy="Acceptable Use Policy",
    version="3.2",
    acknowledgment_rate=0.98,
    non_acknowledgers=["new-hire-1", "new-hire-2"]
))

# Bundle for auditor
bundle = collector.create_audit_bundle(
    evidence_items=evidence,
    framework=Framework.SOC2,
    period="2024-Q1",
    auditor="Deloitte",
    include_executive_summary=True
)
print(f"Audit bundle created: {bundle.path} ({bundle.size_mb:.1f} MB)")
print(f"Evidence items: {len(bundle.evidence_items)}")
print(f"Controls covered: {len(bundle.controls_covered)}")
```

### Compliance Dashboard

```python
from compliance import ComplianceDashboard, Framework, PostureLevel

dashboard = ComplianceDashboard(registry)

# Generate executive summary for all frameworks
for fw in [Framework.SOC2, Framework.ISO27001, Framework.PCI_DSS]:
    status = dashboard.get_status(fw)
    print(f"\n{fw.value}:")
    print(f"  Overall Posture:  {status.overall_posture}")
    print(f"  Controls:         {status.implemented}/{status.total}")
    print(f"  Compliance Score: {status.compliance_score:.1%}")
    print(f"  Last Audit:       {status.last_audit_date}")
    print(f"  Next Review:      {status.next_review_date}")
    print(f"  Open Gaps:        {status.open_gaps}")
    print(f"  Expired Evidence: {status.expired_evidence}")
    print(f"  Avg Evidence Age: {status.avg_evidence_age_days:.0f} days")

# Generate trend report
print(f"\n=== Compliance Trend (12 Months) ===")
trend = dashboard.trend_report(months=12)
for month in trend.monthly:
    print(f"  {month.date}: {month.score:.1%} ({month.change:+.1%})")
```

## Architecture

The compliance module follows a control-centric architecture:

```
┌──────────────────────────────────────────────────────────────┐
│                    FRAMEWORK LAYER                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │  SOC 2   │  │  ISO     │  │  PCI     │  │  HIPAA / │    │
│  │  Type II │  │  27001   │  │  DSS 4.0 │  │  GDPR    │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       └──────────────┼───────────┼──────────────┘           │
│                      │           │                          │
└──────────────────────┼───────────┼──────────────────────────┘
                       │           │
┌──────────────────────▼───────────▼──────────────────────────┐
│                    CONTROL LAYER                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Multi-Framework Control Registry          │   │
│  │    SC-001 ──→ SOC2:CC6.1, ISO:A.9.4.2, PCI:2.2     │   │
│  │    SC-002 ──→ SOC2:CC6.3, NIST:AC-2, HIPAA:164.312  │   │
│  │    SC-003 ──→ PCI:8.2.4, ISO:A.9.4.3, SOC2:CC6.1    │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                   │
└─────────────────────────┼───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    EVIDENCE LAYER                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │  Config  │  │  Access  │  │  Scan    │  │  Policy  │    │
│  │  Exports │  │  Reviews │  │  Reports │  │Attestation│   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       └──────────────┼───────────┼──────────────┘           │
│                      │           │                          │
└──────────────────────┼───────────┼──────────────────────────┘
                       │           │
┌──────────────────────▼───────────▼──────────────────────────┐
│                    REPORTING LAYER                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │  Gap     │  │  Audit   │  │Dashboard │  │Regulatory│    │
│  │ Analysis │  │ Bundles  │  │          │  │Monitoring│    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices

1. **Map controls across frameworks** — One well-documented control can satisfy multiple frameworks. Avoid duplicating effort by maintaining a single control registry with multi-framework mappings.

2. **Automate evidence collection** — Manual evidence gathering doesn't scale and introduces human error. Script exports, screenshots, log collection, and access review generation. Schedule recurring evidence collection.

3. **Continuous compliance over point-in-time** — Annual audits are snapshots that can be gamed. Build automated checks that run weekly or daily to maintain continuous compliance posture.

4. **Treat compliance as a floor, not a ceiling** — PCI DSS minimums prevent catastrophic breaches but don't guarantee security. ISO 27001 is a management system, not a technical standard. Exceed the baseline based on your risk profile.

5. **Involve engineering in compliance** — Compliance is not just a GRC team function. Engineers must understand why controls exist and how to implement them. Embed compliance checks in CI/CD pipelines.

6. **Version control everything** — Policies, procedures, evidence, and control definitions should all be in version control with change tracking. Auditors expect to see historical evidence of control changes.

7. **Prepare for auditor questions** — Maintain a mapping from every control to its evidence source, owner, last review date, and known exceptions. Respond to auditor requests within hours, not days.

8. **Track regulatory changes** — Subscribe to framework update feeds. PCI DSS 4.0, SOC 2 updates, and new HIPAA guidance affect your control set. Map changes to existing controls immediately.

## Performance Considerations

- **Control registry queries**: Multi-framework control lookups complete in milliseconds with proper indexing. Large registries (>10,000 controls) may benefit from partitioning by framework.
- **Evidence collection**: Automated evidence collection from infrastructure APIs (AWS Config, GCP Cloud Asset) takes minutes. Manual evidence collection takes hours per control.
- **Gap analysis**: Gap analysis against large frameworks (NIST 800-53 has 1,000+ controls) completes in seconds with pre-indexed control mappings.
- **Audit bundling**: Generating large audit bundles (>100 evidence items) takes 1-5 minutes. Use incremental bundling for ongoing auditor access.
- **Dashboard rendering**: Real-time dashboards with compliance scoring complete in seconds. Historical trend reports with 12+ months of data may take longer.

## Security Considerations

- **Evidence sensitivity**: Audit evidence may contain sensitive information (access reviews, configuration details, vulnerability reports). Protect evidence storage with access controls and encryption.
- **Policy availability**: Security policies must be accessible to all employees but protected from unauthorized modification. Use version control with branch protection for policy documents.
- **Audit scope creep**: Auditors may request evidence outside the agreed scope. Define and document audit scope boundaries to prevent unauthorized access to sensitive systems.
- **Compliance ≠ security**: Don't assume compliance equals security. Regularly test controls independently of audit cycles. Many breaches occur at compliant organizations.
- **Regulatory penalties**: Non-compliance can result in significant fines (GDPR: up to 4% of global revenue, PCI DSS: $5,000-$100,000/month). Prioritize compliance based on regulatory risk.

## Related Modules

- **threat-modeling** — Document risk assessments for auditors
- **secure-coding** — Implement controls that satisfy compliance requirements
- **security-architecture** — Design systems that are compliant by construction
- **vulnerability-management** — Prove vulnerability management controls to auditors (PCI DSS 6.1, SOC 2 CC6.1)
- **evidence-hygiene** — Proper evidence capture and redaction for audit submissions
- **hunt-sharepoint** — SharePoint-specific compliance testing for on-prem environments

## References

- SOC 2 Trust Services Criteria: https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/aicpasoc2report
- ISO/IEC 27001:2022: https://www.iso.org/standard/27001
- PCI DSS v4.0: https://www.pcisecuritystandards.org/document_library/
- NIST SP 800-53 Rev. 5: https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final
- HIPAA Security Rule: https://www.hhs.gov/hipaa/for-professionals/security/index.html
- GDPR (General Data Protection Regulation): https://gdpr.eu/
- NIST Cybersecurity Framework (CSF) 2.0: https://www.nist.gov/cyberframework
- CIS Controls v8: https://www.cisecurity.org/controls
- OWASP ASVS (Application Security Verification Standard): https://owasp.org/www-project-application-security-verification-standard/
- Cloud Security Alliance (CSA) CCM: https://cloudsecurityalliance.org/research/cloud-controls-matrix/

---

## GDPR Compliance Implementation

The General Data Protection Regulation (GDPR) imposes strict requirements on organizations that process personal data of EU residents. Non-compliance carries fines up to 4% of annual global revenue or EUR 20 million, whichever is higher. GDPR compliance requires technical and organizational measures that protect personal data throughout its lifecycle.

### GDPR Data Processing Principles

```python
from compliance import GDPRCompliance, DataProcessingRecord, lawful_basis

# Register a data processing activity (Article 30 record)
processing = DataProcessingRecord(
    activity_id="DPA-001",
    purpose="Customer account management",
    data_categories=["name", "email", "phone", "ip_address"],
    data_subjects=["customers", "website_visitors"],
    lawful_basis=lawful_basis.CONTRACT,  # Art. 6(1)(b)
    retention_period="7 years after account closure",
    recipients=["payment_processor", "email_service"],
    transfers=["US (SCCs in place)"],
    technical_measures=["encryption_at_rest", "access_controls", "pseudonymization"],
    dpo_contact="dpo@company.com",
    last_review="2024-01-15"
)

# Data Protection Impact Assessment (DPIA) for high-risk processing
dpia = gdpr.dpia(
    processing=processing,
    necessity_and_proportionality=True,
    risk_to_data_subjects=["unauthorized_access", "data_breach", "discrimination"],
    mitigation_measures=["encryption", "access_logging", "anonymization"],
    dpo_sign_off=True,
    review_date="2024-07-15"
)
print(f"DPIA Status: {dpia.status}")
print(f"Risk Level: {dpia.risk_level}")
print(f"DPO Approval: {dpia.dpo_approved}")
```

### Data Subject Rights Implementation

```python
from compliance import GDPRDataRights, SubjectRequest, RequestType

rights_handler = GDPRDataRights(storage_backend="postgresql")

# Handle right of access (Article 15)
request = SubjectRequest(
    subject_id="user-12345",
    request_type=RequestType.ACCESS,
    identity_verified=True,
    verification_method="email_plus_id",
    deadline_days=30
)

response = rights_handler.process(request)
print(f"Request ID: {response.request_id}")
print(f"Data found: {response.data_categories}")
print(f"Third parties notified: {response.third_parties_notified}")
print(f"Response due: {response.deadline}")

# Handle right to erasure (Article 17 - Right to be forgotten)
erasure_request = SubjectRequest(
    subject_id="user-67890",
    request_type=RequestType.ERASURE,
    identity_verified=True,
    verification_method="email_plus_id",
    exemptions=["legal_obligation", "active_contract"]
)

erasure_response = rights_handler.process_erasure(erasure_request)
print(f"Records deleted: {erasure_response.records_deleted}")
print(f"Records retained (exemptions): {erasure_response.records_retained}")
print(f"Third parties notified: {erasure_response.third_parties_notified}")
print(f"Backup purged: {erasure_response.backup_purge_scheduled}")

# Handle right to portability (Article 20)
portability = rights_handler.export_data(
    subject_id="user-12345",
    format="json",  # machine-readable format
    include_metadata=True
)
print(f"Export size: {portability.size_bytes} bytes")
print(f"Format: {portability.format}")
print(f"Encryption: {portability.export_encrypted}")
```

### GDPR Breach Notification

```python
from compliance import GDPRBreachNotification, BreachSeverity

# Record a data breach
breach = GDPRBreachNotification(
    breach_id="BREACH-2024-001",
    detected_date="2024-03-15T10:30:00Z",
    breach_type="confidentiality",  # confidentiality, integrity, or availability
    data_categories=["email", "password_hashes"],
    estimated_subjects=5000,
    severity=BreachSeverity.HIGH,  # risk to rights and freedoms
    cause="compromised API key",
    containment_date="2024-03-15T11:00:00Z",
    forensic_status="investigating"
)

# GDPR 72-hour notification to supervisory authority
notification = breach.prepare_authority_notification(
    authority="Commission Nationale de l'Informatique et des Libert\u00e9s (CNIL)",
    include_containment_measures=True,
    include_dpo_contact=True,
    include_likely_consequences=True,
    include_mitigation_measures=True
)
print(f"Notification deadline: {notification.deadline_72h}")
print(f"Deadline status: {notification.status}")

# Prepare data subject notification (Article 34)
# Required when high risk to rights and freedoms
subject_notification = breach.prepare_subject_notification(
    template="breach_notification_v3",
    include_contact_dpo=True,
    include_measures_taken=True,
    include_recommendations=True
)
print(f"Subject notification required: {subject_notification.required}")
print(f"Notification channels: {subject_notification.channels}")
```

## HIPAA Compliance Implementation

The Health Insurance Portability and Accountability Act (HIPAA) requires covered entities and business associates to implement administrative, physical, and technical safeguards for Protected Health Information (PHI). Penalties range from $100 to $50,000 per violation, with an annual maximum of $1.5 million per violation category.

### HIPAA Security Rule Implementation

```python
from compliance import HIPAACompliance, SecuritySafeguard, safeguard_type

# Map technical safeguards (§164.312)
technical_safeguards = [
    SecuritySafeguard(
        ref="§164.312(a)(1)",
        title="Access Control",
        requirement="Implement technical policies to allow access only to authorized persons",
        implementation_status="implemented",
        controls=[
            "RBAC with role-based access to EHR systems",
            "Unique user identification (no shared accounts)",
            "Automatic session timeout (15 minutes)",
            "Emergency access procedure documented and tested",
            "Encryption of PHI at rest (AES-256) and in transit (TLS 1.3)",
        ],
        evidence=["rbac_policy.pdf", "session_timeout_config.png", "encryption_audit.json"],
        last_tested="2024-01-15"
    ),
    SecuritySafeguard(
        ref="§164.312(b)",
        title="Audit Controls",
        requirement="Implement hardware, software, and/or procedural mechanisms to record and examine access",
        implementation_status="implemented",
        controls=[
            "Centralized audit logging (ELK stack)",
            "Access logs retained for 6 years",
            "Automated alerting on anomalous access patterns",
            "Monthly access review by compliance team",
        ],
        evidence=["audit_log_config.json", "monthly_review_report.pdf"],
        last_tested="2024-01-15"
    ),
    SecuritySafeguard(
        ref="§164.312(c)(1)",
        title="Integrity",
        requirement="Implement policies to protect PHI from improper alteration or destruction",
        implementation_status="implemented",
        controls=[
            "Database write-ahead logging (WAL)",
            "Cryptographic integrity verification (SHA-256)",
            "Immutable audit trail for PHI modifications",
            "Automated backup integrity checks",
        ],
        evidence=["integrity_check_config.json", "backup_verification_log.csv"],
        last_tested="2024-01-15"
    ),
    SecuritySafeguard(
        ref="§164.312(d)",
        title="Person or Entity Authentication",
        requirement="Implement procedures to verify identity of persons seeking access to PHI",
        implementation_status="implemented",
        controls=[
            "Multi-factor authentication (MFA) for all PHI access",
            "Certificate-based authentication for service accounts",
            "Biometric authentication for physical access to data centers",
            "Annual credential review and rotation",
        ],
        evidence=["mfa_policy.pdf", "auth_config.json", "credential_review_2024.pdf"],
        last_tested="2024-01-15"
    ),
    SecuritySafeguard(
        ref="§164.312(e)(1)",
        title="Transmission Security",
        requirement="Implement technical security measures to guard against unauthorized access during transmission",
        implementation_status="implemented",
        controls=[
            "TLS 1.3 for all PHI transmissions",
            "mTLS for system-to-system communication",
            "VPN for remote access to PHI systems",
            "Encryption key rotation every 90 days",
        ],
        evidence=["tls_config.json", "mtls_config.json", "vpn_config.json"],
        last_tested="2024-01-15"
    ),
]

# Map administrative safeguards (§164.308)
administrative_safeguards = [
    SecuritySafeguard(
        ref="§164.308(a)(1)",
        title="Security Management Process",
        requirement="Implement policies and procedures to prevent, detect, contain, and correct security violations",
        implementation_status="implemented",
        controls=[
            "Risk analysis conducted annually",
            "Risk management plan with assigned responsibilities",
            "Sanction policy for workforce members",
            "Information system activity review procedures",
        ],
        evidence=["risk_analysis_2024.pdf", "risk_management_plan.pdf", "sanction_policy.pdf"],
        last_tested="2024-01-15"
    ),
    SecuritySafeguard(
        ref="§164.308(a)(5)",
        title="Security Awareness and Training",
        requirement="Implement security awareness and training program for all workforce members",
        implementation_status="implemented",
        controls=[
            "Annual HIPAA security training for all staff",
            "Role-based training for new hires",
            "Phishing simulation quarterly",
            "Security awareness newsletter monthly",
        ],
        evidence=["training_completion_report.pdf", "phishing_simulation_results.csv"],
        last_tested="2024-01-15"
    ),
]

# Assess HIPAA compliance
hipaa = HIPAACompliance()
assessment = hipaa.assess(
    technical_safeguards=technical_safeguards,
    administrative_safeguards=administrative_safeguards,
    physical_safeguards=[],  # Not shown for brevity
)
print(f"HIPAA Compliance Score: {assessment.score:.1%}")
print(f"Technical Safeguards: {assessment.technical_score:.1%}")
print(f"Administrative Safeguards: {assessment.administrative_score:.1%}")
print(f"Findings: {assessment.findings_count}")
```

### Business Associate Agreement Tracking

```python
from compliance import BAATracker, BusinessAssociate

tracker = BAATracker()

# Register a business associate
ba = tracker.register(
    name="Cloud Health Systems",
    service="EHR hosting",
    data_access=["PHI", "ePHI"],
    baa_signed_date="2023-06-15",
    baa_expiry_date="2025-06-14",
    security_assessment_date="2023-06-01",
    last_audit_date="2024-01-15",
    breach_notification_required=True,
    subcontractors=["AWS", "CloudFlare"],
    compliance_requirements=["HIPAA", "SOC2"]
)

# Check BAA status
status = tracker.check_status(ba)
print(f"BAA Status: {status.status}")
print(f"Days until expiry: {status.days_until_expiry}")
print(f"Security assessment current: {status.assessment_current}")
print(f"Audit current: {status.audit_current}")

# Generate compliance report
report = tracker.compliance_report(
    include_expired=True,
    include_expiring_90_days=True
)
print(f"\nTotal BAAs: {report.total}")
print(f"Active: {report.active}")
print(f"Expiring in 90 days: {report.expiring_90_days}")
print(f"Expired: {report.expired}")
```

## PCI DSS 4.0 Implementation

Payment Card Industry Data Security Standard (PCI DSS) version 4.0 introduces 12 requirements organized into 6 goals, with new requirements for enhanced authentication, encryption, and continuous monitoring. Non-compliance can result in fines of $5,000 to $100,000 per month and loss of card processing privileges.

### PCI DSS Requirement Mapping

```python
from compliance import PCIDSSCompliance, Requirement, SAQType

pci = PCIDSSCompliance(version="4.0")

# Define requirement mappings for each of the 12 PCI DSS goals
requirements = [
    Requirement(
        goal=1,
        title="Install and Maintain Network Security Controls",
        sub_requirements=[
            "1.2.1 - Restrict inbound and outbound traffic",
            "1.3.1 - Restrict inbound traffic to cardholder data environment (CDE)",
            "1.3.2 - Restrict outbound traffic from CDE",
            "1.4.1 - Install network security controls between CDE and untrusted networks",
            "1.5.1 - Document roles and responsibilities for network security",
        ],
        implementation_status="implemented",
        evidence=["network_diagram.pdf", "firewall_rules.json", "access_control_lists.csv"],
        automated_check=True
    ),
    Requirement(
        goal=2,
        title="Apply Secure Configurations to All System Components",
        sub_requirements=[
            "2.2.1 - Develop configuration standards for all system components",
            "2.2.2 - System configuration standards address all known vulnerabilities",
            "2.2.3 - Configuration standards are reviewed at least annually",
            "2.2.4 - Changes to system components managed securely",
        ],
        implementation_status="implemented",
        evidence=["config_standards.pdf", "baseline_configs.json", "review_schedule.csv"],
        automated_check=True
    ),
    Requirement(
        goal=6,
        title="Develop and Maintain Secure Systems and Software",
        sub_requirements=[
            "6.2.1 - Bespoke and custom software are developed securely",
            "6.2.2 - Bespoke software is protected against common vulnerabilities",
            "6.3.1 - Identify and manage security vulnerabilities",
            "6.4.1 - Public-facing web applications protected against attacks",
            "6.4.2 - Automated technical solutions for web-based attacks on public systems",
        ],
        implementation_status="partially_implemented",
        evidence=["secure_coding_policy.pdf", "sast_config.json", "dast_results.csv"],
        automated_check=True
    ),
    Requirement(
        goal=8,
        title="Identify Users and Authenticate Access",
        sub_requirements=[
            "8.2.1 - Identify and authenticate users accessing system components",
            "8.3.1 - MFA for all non-console access to CDE",
            "8.3.2 - MFA implemented via hardware or software mechanisms",
            "8.3.6 - Password/passphrase complexity requirements",
            "8.3.7 - Password/passphrase history requirements",
        ],
        implementation_status="implemented",
        evidence=["mfa_policy.pdf", "auth_config.json", "password_policy.json"],
        automated_check=True
    ),
    Requirement(
        goal=10,
        title="Log and Monitor All Access",
        sub_requirements=[
            "10.2.1 - Audit logs capture specified events",
            "10.2.2 - Audit logs record all individual access to cardholder data",
            "10.3.1 - Audit logs are protected from modifications",
            "10.4.1 - Audit logs reviewed at least daily",
            "10.4.2 - Anomalies and exceptions identified and addressed",
        ],
        implementation_status="implemented",
        evidence=["logging_config.json", "siem_alerts.json", "review_schedule.csv"],
        automated_check=True
    ),
]

# Generate SAQ (Self-Assessment Questionnaire)
saq = pci.generate_saq(
    saq_type=SAQType.A,  # SAQ A for merchants who outsource all card processing
    requirements=requirements,
    signed_by="CISO",
    sign_date="2024-03-15",
    attestation_period="2024-Q1"
)
print(f"SAQ Type: {saq.saq_type}")
print(f"Requirements Met: {saq.requirements_met}/{saq.requirements_total}")
print(f"Compliance Status: {saq.compliance_status}")
print(f"Next Assessment Due: {saq.next_assessment_date}")
```

### Continuous Compliance Monitoring for PCI

```python
from compliance import PCIContinuousMonitor, ComplianceCheck

monitor = PCIContinuousMonitor()

# Define continuous checks
checks = [
    ComplianceCheck(
        check_id="PCI-CONT-001",
        requirement="1.2.1",
        title="Network segmentation verification",
        check_type="automated",
        frequency="daily",
        script="verify_network_segmentation.py",
        pass_criteria="No direct traffic from internet to CDE",
        alert_on_failure=True
    ),
    ComplianceCheck(
        check_id="PCI-CONT-002",
        requirement="8.3.1",
        title="MFA enforcement verification",
        check_type="automated",
        frequency="daily",
        script="verify_mfa_enforcement.py",
        pass_criteria="100% of CDE access requires MFA",
        alert_on_failure=True
    ),
    ComplianceCheck(
        check_id="PCI-CONT-003",
        requirement="10.4.1",
        title="Daily log review completion",
        check_type="manual",
        frequency="daily",
        script="check_log_review.py",
        pass_criteria="Log review completed by 09:00 UTC",
        alert_on_failure=True
    ),
    ComplianceCheck(
        check_id="PCI-CONT-004",
        requirement="6.4.1",
        title="WAF rule effectiveness",
        check_type="automated",
        frequency="weekly",
        script="verify_waf_rules.py",
        pass_criteria="All OWASP Top 10 rules active, no disabled critical rules",
        alert_on_failure=True
    ),
]

# Run compliance checks
results = monitor.run_checks(checks)
for result in results:
    status = "PASS" if result.passed else "FAIL"
    print(f"[{status}] {result.check_id}: {result.title}")
    if not result.passed:
        print(f"  Details: {result.failure_details}")
        print(f"  Alert sent: {result.alert_sent}")

# Generate compliance report
report = monitor.compliance_report(period="last_30_days")
print(f"\nPCI DSS 4.0 Continuous Compliance Report")
print(f"Checks Run: {report.checks_run}")
print(f"Pass Rate: {report.pass_rate:.1%}")
print(f"Failures: {report.failures}")
print(f"Alerts Sent: {report.alerts_sent}")
```

## SOC 2 Trust Services Criteria Implementation

SOC 2 Type II examines the effectiveness of controls over a period (typically 6-12 months). The five Trust Services Criteria — Security, Availability, Processing Integrity, Confidentiality, and Privacy — form the framework for evaluating controls.

### SOC 2 Control Implementation

```python
from compliance import SOC2Control, TrustServiceCriteria, ControlEffectiveness

# Define controls mapped to Trust Services Criteria
controls = [
    SOC2Control(
        control_id="CC6.1",
        title="Logical Access Security",
        criteria=TrustServiceCriteria.SECURITY,
        description="Entity implements logical access security to protect against threats",
        control_type="preventive",
        implementation=[
            "RBAC with least-privilege principles",
            "Unique user identification (no shared accounts)",
            "MFA for remote access",
            "Quarterly access reviews",
            "Automated deprovisioning on termination",
        ],
        evidence_sources=["iam_config.json", "access_reviews/", "offboarding_logs.csv"],
        test_procedure="Verify access controls enforce least privilege and MFA",
        expected_result="100% of access follows RBAC, MFA enforced for remote",
        review_frequency="quarterly",
        owner="platform-team"
    ),
    SOC2Control(
        control_id="CC6.2",
        title="User Registration and Authorization",
        criteria=TrustServiceCriteria.SECURITY,
        description="Entity registers new users through an authorization process",
        control_type="preventive",
        implementation=[
            "New user request via ticketing system",
            "Manager approval required",
            "Security team verifies role appropriateness",
            "Unique credentials issued per user",
        ],
        evidence_sources=["ticket_logs.csv", "approval_records.json"],
        test_procedure="Verify all users have documented approval",
        expected_result="100% of new users have manager and security approval",
        review_frequency="quarterly",
        owner="platform-team"
    ),
    SOC2Control(
        control_id="CC7.1",
        title="Detection of Unauthorized Activities",
        criteria=TrustServiceCriteria.SECURITY,
        description="Entity monitors system components for anomalies",
        control_type="detective",
        implementation=[
            "SIEM integration (Splunk)",
            "Anomaly detection rules for authentication",
            "Failed login alerting (>5 attempts)",
            "Privilege escalation alerting",
            "Network traffic anomaly detection",
        ],
        evidence_sources=["siem_config.json", "alert_rules.json", "incident_logs.csv"],
        test_procedure="Verify alerts fire on test anomalies",
        expected_result="All anomaly detection rules functional, alerts delivered",
        review_frequency="monthly",
        owner="security-ops"
    ),
    SOC2Control(
        control_id="CC8.1",
        title="Change Management",
        criteria=TrustServiceCriteria.SECURITY,
        description="Entity manages changes to infrastructure and software",
        control_type="preventive",
        implementation=[
            "All changes via pull request with review",
            "Automated CI/CD with security gates",
            "Change approval by designated approvers",
            "Rollback procedures documented",
            "Post-deployment verification",
        ],
        evidence_sources=["git_logs.json", "ci_results.json", "change_tickets.csv"],
        test_procedure="Verify all production changes follow change management",
        expected_result="100% of production changes have documented approval",
        review_frequency="quarterly",
        owner="engineering"
    ),
    SOC2Control(
        control_id="CC9.1",
        title="Risk Management",
        criteria=TrustServiceCriteria.SECURITY,
        description="Entity identifies, selects, and develops risk mitigation activities",
        control_type="preventive",
        implementation=[
            "Annual risk assessment",
            "Risk register maintained and reviewed quarterly",
            "Risk acceptance documented by management",
            "Vendor risk assessments for critical vendors",
        ],
        evidence_sources=["risk_assessment.pdf", "risk_register.xlsx", "vendor_assessments/"],
        test_procedure="Verify risk register is current and reviewed",
        expected_result="Risk register updated quarterly, all risks have owners",
        review_frequency="quarterly",
        owner="risk-management"
    ),
]

# Test control effectiveness
for control in controls:
    effectiveness = control.test_effectiveness()
    print(f"{control.control_id}: {control.title}")
    print(f"  Status: {effectiveness.status}")
    print(f"  Operating Effectively: {effectiveness.operating_effectively}")
    print(f"  Evidence Gap: {effectiveness.evidence_gap}")
    print(f"  Findings: {effectiveness.findings}")
    print()
```

## Audit Preparation and Evidence Generation

### Automated Audit Evidence Collection

```python
from compliance import AuditEvidenceCollector, EvidenceCategory

collector = AuditEvidenceCollector(
    storage_path="./audit-evidence/2024",
    encryption_key="vault://audit-evidence-key"
)

# Collect evidence from multiple sources automatically
evidence_items = collector.collect_batch([
    # Access control evidence
    {
        "category": EvidenceCategory.ACCESS_CONTROL,
        "source": "aws_iam",
        "collection_script": "collect_iam_access.py",
        "output_format": "json",
        "include_timestamps": True,
    },
    # Configuration evidence
    {
        "category": EvidenceCategory.CONFIGURATION,
        "source": "terraform_state",
        "collection_script": "collect_infra_config.py",
        "output_format": "json",
        "include_diff": True,
    },
    # Vulnerability scan evidence
    {
        "category": EvidenceCategory.VULNERABILITY_SCAN,
        "source": "trivy_scanner",
        "collection_script": "collect_scan_results.py",
        "output_format": "json",
        "include_summary": True,
    },
    # Change management evidence
    {
        "category": EvidenceCategory.CHANGE_MANAGEMENT,
        "source": "github",
        "collection_script": "collect_change_logs.py",
        "output_format": "json",
        "include_approvals": True,
    },
    # Incident response evidence
    {
        "category": EvidenceCategory.INCIDENT_RESPONSE,
        "source": "pagerduty",
        "collection_script": "collect_incidents.py",
        "output_format": "json",
        "include_resolution": True,
    },
])

# Generate audit-ready bundle
bundle = collector.create_bundle(
    evidence_items=evidence_items,
    framework=Framework.SOC2,
    period="2024-Q1",
    auditor="PwC",
    include_index=True,
    include_executive_summary=True
)

print(f"Audit bundle ready: {bundle.path}")
print(f"Total evidence items: {len(bundle.evidence_items)}")
print(f"Categories covered: {bundle.categories_covered}")
print(f"Bundle integrity hash: {bundle.integrity_hash}")
```

## Regulatory Change Tracking

```python
from compliance import RegulatoryChangeTracker, FrameworkUpdate

tracker = RegulatoryChangeTracker()

# Track changes across multiple frameworks
tracker.track_framework(
    framework=Framework.PCI_DSS,
    version="4.0",
    change_feed="https://www.pcisecuritystandards.org/rss/updates",
    alert_channels=["slack-security", "email-compliance"],
)

tracker.track_framework(
    framework=Framework.HIPAA,
    version="current",
    change_feed="hhs.gov/hipaa/rules",
    alert_channels=["email-compliance"],
)

tracker.track_framework(
    framework=Framework.SOC2,
    version="2024",
    change_feed="aicpa.org/soc2-updates",
    alert_channels=["slack-security", "email-compliance"],
)

# Check for recent changes
changes = tracker.get_recent_changes(days=30)
for change in changes:
    print(f"Change: {change.title}")
    print(f"  Framework: {change.framework}")
    print(f"  Effective Date: {change.effective_date}")
    print(f"  Impact: {change.impact_assessment}")
    print(f"  Controls Affected: {change.controls_affected}")
    print(f"  Action Required: {change.action_required}")
    print(f"  Status: {change.status}")
    print()
```

## Compliance Policy Templates

### Acceptable Use Policy Template

```python
from compliance import PolicyTemplate, PolicyType

template = PolicyTemplate(
    policy_type=PolicyType.ACCEPTABLE_USE,
    version="4.0",
    effective_date="2024-01-01",
    review_cycle="annual",
    approver="CISO",
    applicable_frameworks=["SOC2:CC6.1", "ISO27001:A.7.1.2", "NIST:AC-11"]
)

# Generate policy document
policy = template.generate(
    company_name="Acme Corp",
    data_classification_levels=["Public", "Internal", "Confidential", "Restricted"],
    prohibited_activities=[
        "Unauthorized access to systems or data",
        "Sharing credentials with others",
        "Using company resources for personal financial gain",
        "Installing unauthorized software",
        "Bypassing security controls",
    ],
    acceptable_activities=[
        "Using company resources for authorized work tasks",
        "Reporting security incidents immediately",
        "Following data handling procedures",
        "Participating in security awareness training",
    ],
    enforcement_actions=[
        "Verbal warning for first offense",
        "Written warning for repeated offenses",
        "Suspension of access pending investigation",
        "Termination for willful violations",
    ],
    acknowledgment_required=True,
    acknowledgment_deadline_days=30,
    format="docx"
)
print(f"Policy generated: {policy.path}")
print(f"Acknowledgment required: {policy.acknowledgment_required}")
print(f"Deadline: {policy.acknowledgment_deadline}")
```

### Incident Response Policy Template

```python
from compliance import PolicyTemplate, PolicyType

template = PolicyTemplate(
    policy_type=PolicyType.INCIDENT_RESPONSE,
    version="3.0",
    effective_date="2024-01-01",
    review_cycle="annual",
    approver="CISO",
    applicable_frameworks=[
        "SOC2:CC7.3", "SOC2:CC7.4",
        "ISO27001:A.16.1", "ISO27001:A.16.1.1",
        "PCI_DSS:12.10",
        "NIST:IR-1", "NIST:IR-2"
    ]
)

policy = template.generate(
    company_name="Acme Corp",
    incident_severity_levels=[
        {"level": 1, "name": "Critical", "response_time": "15 minutes", "escalation": "CISO, CTO, Legal"},
        {"level": 2, "name": "High", "response_time": "1 hour", "escalation": "Security Manager, Engineering VP"},
        {"level": 3, "name": "Medium", "response_time": "4 hours", "escalation": "Security Team Lead"},
        {"level": 4, "name": "Low", "response_time": "24 hours", "escalation": "Security Team"},
    ],
    response_phases=[
        {"phase": "Preparation", "description": "Pre-incident planning and readiness"},
        {"phase": "Detection & Analysis", "description": "Identify and assess the incident"},
        {"phase": "Containment", "description": "Limit the impact of the incident"},
        {"phase": "Eradication", "description": "Remove the threat and restore systems"},
        {"phase": "Recovery", "description": "Return to normal operations"},
        {"phase": "Post-Incident", "description": "Lessons learned and improvements"},
    ],
    notification_requirements={
        "internal": {"timeline": "immediately", "channels": ["pagerduty", "slack-security"]},
        "customers": {"timeline": "within 72 hours", "channels": ["email", "status_page"]},
        "regulators": {"timeline": "within 72 hours (GDPR)", "channels": ["regulatory_portal"]},
        "law_enforcement": {"timeline": "as needed", "channels": ["direct_contact"]},
    },
    format="docx"
)
print(f"IR Policy generated: {policy.path}")
```

## Multi-Framework Compliance Matrix

```python
from compliance import ComplianceMatrix, FrameworkControl

# Generate a compliance matrix showing cross-framework coverage
matrix = ComplianceMatrix(registry)

# Get detailed mapping for a specific control family
access_controls = matrix.get_family(
    family="access_control",
    frameworks=[Framework.SOC2, Framework.ISO27001, Framework.PCI_DSS, Framework.NIST_800_53]
)

print("=== Cross-Framework Access Control Mapping ===")
for control in access_controls:
    print(f"\nControl: {control.id} - {control.title}")
    for fw, mappings in control.framework_mappings.items():
        print(f"  {fw.value}: {', '.join(mappings)}")
    print(f"  Implementation: {control.implementation_status}")
    print(f"  Evidence: {control.evidence_count} items")
    print(f"  Last Tested: {control.last_tested}")

# Export matrix for auditor
export = matrix.export_for_auditor(
    format="xlsx",
    include_evidence_links=True,
    include_test_results=True,
    include_owner_contact=True
)
print(f"\nExport: {export.path}")
```

## Compliance Automation in CI/CD

```yaml
# .github/workflows/compliance-check.yml
name: Compliance Check

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  compliance-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install compliance tools
        run: |
          pip install bandit semgrep safety pip-audit

      - name: Security linting (bandit)
        run: bandit -r src/ -f json -o bandit-results.json

      - name: SAST scanning (semgrep)
        run: semgrep scan --config auto --json -o semgrep-results.json src/

      - name: Dependency audit
        run: |
          pip-audit --format json --output pip-audit-results.json
          npm audit --json > npm-audit-results.json

      - name: Configuration compliance
        run: |
          python -m compliance check --framework SOC2 --config ./
          python -m compliance check --framework PCI_DSS --config ./

      - name: Policy compliance
        run: |
          python -m compliance verify-policies --acknowledgment-check

      - name: Upload compliance results
        uses: actions/upload-artifact@v4
        with:
          name: compliance-results
          path: |
            bandit-results.json
            semgrep-results.json
            pip-audit-results.json
            npm-audit-results.json

      - name: Compliance gate
        run: |
          python -m compliance gate --max-critical 0 --max-high 0 --fail-on-violation
```

## Compliance Risk Assessment Framework

```python
from compliance import ComplianceRiskAssessment, RiskFactor, ComplianceRisk

# Define risk factors for compliance assessment
risk_factors = [
    RiskFactor(
        name="Regulatory Exposure",
        weight=0.3,
        scoring={
            "critical_regulation": 10,  # GDPR, HIPAA
            "major_regulation": 7,      # PCI DSS
            "industry_standard": 4,     # SOC 2, ISO 27001
            "internal_policy": 1,
        }
    ),
    RiskFactor(
        name="Financial Impact",
        weight=0.25,
        scoring={
            "revenue_loss": 10,
            "regulatory_fine": 9,
            "litigation_cost": 8,
            "remediation_cost": 5,
        }
    ),
    RiskFactor(
        name="Data Sensitivity",
        weight=0.25,
        scoring={
            "pii": 8,
            "phi": 10,
            "pci_data": 9,
            "internal_data": 3,
            "public_data": 1,
        }
    ),
    RiskFactor(
        name="Breach Likelihood",
        weight=0.2,
        scoring={
            "actively_exploited": 10,
            "known_vulnerability": 7,
            "theoretical_vulnerability": 4,
            "no_known_vulnerability": 1,
        }
    ),
]

assessment = ComplianceRiskAssessment(risk_factors)

# Assess compliance risk for a specific control gap
risk = assessment.assess(
    gap="Missing encryption at rest for customer database",
    regulatory_context="GDPR Article 32, HIPAA §164.312(a)(2)(iv)",
    financial_context="Customer database contains PII for 100K users",
    breach_context="No known exploit, but encryption is baseline control"
)

print(f"Compliance Risk Score: {risk.score:.1f}/10")
print(f"Risk Level: {risk.risk_level}")
print(f"Priority: {risk.priority}")
print(f"Remediation Timeline: {risk.remediation_timeline}")
print(f"Risk Factors:")
for factor in risk.factor_breakdown:
    print(f"  {factor.name}: {factor.score:.1f} (weight: {factor.weight})")
```
