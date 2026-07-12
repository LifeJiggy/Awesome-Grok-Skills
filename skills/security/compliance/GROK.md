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
