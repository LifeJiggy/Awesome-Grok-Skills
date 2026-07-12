---
name: "compliance-audit"
category: "security-assessment"
version: "2.0.0"
tags: ["security-assessment", "compliance-audit", "ISO27001", "SOC2", "PCI-DSS", "GDPR", "NIST-CSF"]
---

# Compliance Audit Module

## Overview

The Compliance Audit module automates evidence collection, control mapping, gap analysis, and audit preparation across major regulatory and industry frameworks. It maps technical controls to framework requirements, tracks compliance posture over time, generates audit-ready evidence packages, and identifies gaps requiring remediation. Supports ISO 27001, SOC 2 Type II, PCI DSS v4.0, HIPAA, GDPR, NIST CSF 2.0, and CIS Controls with framework cross-mapping for multi-framework compliance programs.

Built for organizations managing multiple compliance obligations simultaneously, the module eliminates redundant control assessments by identifying common controls that satisfy multiple framework requirements. This cross-framework mapping reduces audit burden by up to 40% while maintaining comprehensive coverage across all applicable regulations.

The module's continuous monitoring capability transforms compliance from a periodic point-in-time exercise into an ongoing operational practice. Real-time drift detection alerts teams when controls fail or configurations change, enabling rapid remediation before compliance posture degrades. This proactive approach significantly reduces the risk of audit findings and regulatory penalties.

## Core Capabilities

1. **Framework Mapping** — Automatically map existing security controls to framework-specific requirements (e.g., NIST CSF → ISO 27001 Annex A → PCI DSS Requirement 6) with confidence scoring and gap identification.

2. **Gap Analysis** — Compare current control coverage against target framework requirements. Identify missing controls, partially implemented controls, and evidence gaps with severity classification.

3. **Evidence Collection** — Automate evidence gathering from cloud APIs (AWS Config, Azure Policy, GCP SCC), ticketing systems (Jira, ServiceNow), and configuration management tools with scheduled collection.

4. **Continuous Compliance Monitoring** — Real-time compliance posture dashboards with drift detection, alerting on control failures or configuration changes via email, Slack, or webhook integration.

5. **Audit Readiness Scoring** — Score readiness for upcoming audits by framework, identifying high-risk gaps that could result in findings or non-conformities with remediation priority ranking.

6. **Cross-Framework Correlation** — Map controls across frameworks to reduce duplicate effort (one control satisfying multiple framework requirements) with overlap analysis and optimization recommendations.

7. **Non-Conformity Management** — Track non-conformities from discovery through remediation with root cause analysis, corrective action plans, and verification workflows.

8. **Audit Trail Integrity** — Maintain immutable, timestamped audit trails for all control assessments and evidence artifacts with cryptographic verification.

## Usage Examples

### Framework Gap Analysis

```python
from security_assessment.compliance_audit import ComplianceAnalyzer

analyzer = ComplianceAnalyzer(framework="ISO27001:2022")
gaps = analyzer.gap_analysis(
    current_controls=loaded_controls,
    target_scope=["A.5-A.8"],
    evidence_repository="./evidence/"
)

print(f"Total controls: {gaps.total}")
print(f"  Compliant: {gaps.compliant}")
print(f"  Partial: {gaps.partial}")
print(f"  Non-compliant: {gaps.non_compliant}")
print(f"  No evidence: {gaps.no_evidence}")

for gap in gaps.findings:
    print(f"  [{gap.status}] {gap.control_id}: {gap.requirement}")
    print(f"    Remediation priority: {gap.priority}")
```

### SOC 2 Type II Readiness

```python
from security_assessment.compliance_audit import SOC2Analyzer

soc2 = SOC2Analyzer(trust_service_criteria=["CC", "A", "C", "PI", "R"])
readiness = soc2.assess(
    controls=organization_controls,
    evidence_store=evidence_store,
    review_period="2025-01-01 to 2025-12-31"
)

for criteria in readiness.criteria_scores:
    print(f"{criteria.code} ({criteria.name}): {criteria.score}% ready")
    if criteria.gaps:
        for gap in criteria.gaps:
            print(f"  GAP: {gap.description}")
            print(f"    Impact: {gap.audit_risk}")
            print(f"    Remediation: {gap.recommendation}")
```

### PCI DSS v4.0 Assessment

```python
from security_assessment.compliance_audit import PCIDSSAssessor

assessor = PCIDSSAssessor(version="4.0", cardholder_data_env="production")
result = assessor.assess_scope(
    requirements=["Req 1-12"],
    assets=["network-diagrams", "firewall-configs", "access-logs"]
)

print(f"PCI DSS v4.0 Compliance: {result.overall_score}%")
for req in result.requirement_results:
    status = "PASS" if req.is_compliant else "FAIL"
    print(f"  [{status}] Requirement {req.number}: {req.title}")
    if req.findings:
        for f in req.findings:
            print(f"    → {f.description} (Priority: {f.priority})")
```

### GDPR Data Protection Assessment

```python
from security_assessment.compliance_audit import GDPRAssessment

gdpr = GDPRAssessment()
assessment = gdpr.assess(
    data_processing_activities=dpas,
    technical_measures=technical_controls,
    organizational_measures=org_controls
)

print(f"GDPR Compliance Score: {assessment.score}%")
for article in assessment.article_coverage:
    if article.status != "compliant":
        print(f"  [{article.status.upper()}] Article {article.number}: {article.title}")
        print(f"    Risk: {article.risk_level}")
        print(f"    Fine exposure: {article.max_fine}")
```

### Automated Evidence Collection

```python
from security_assessment.compliance_audit import EvidenceCollector

collector = EvidenceCollector(
    sources=[
        {"type": "aws_config", "region": "us-east-1"},
        {"type": "github", "org": "myorg"},
        {"type": "jira", "project": "SEC"}
    ]
)

evidence = collector.collect(
    control_ids=["A.8.1", "A.8.9", "A.8.24"],
    date_range=("2025-01-01", "2025-12-31")
)

evidence.package(
    framework="ISO27001",
    output_path="./audit-evidence-2025/",
    include_metadata=True
)
```

### Cross-Framework Control Mapping

```python
from security_assessment.compliance_audit import CrossFrameworkMapper

mapper = CrossFrameworkMapper()
mapper.load_frameworks(["ISO27001", "SOC2", "PCI_DSS", "NIST_CSF", "HIPAA"])

mapping = mapper.map_control(
    control_description="Multi-factor authentication for administrative access"
)

print("Controls mapped to this requirement:")
for mapped in mapping.matches:
    print(f"  {mapped.framework}: {mapped.control_id} — {mapped.requirement}")
    print(f"    Confidence: {mapped.confidence:.0%}")
    print(f"    Evidence required: {mapped.evidence_types}")
```

## Architecture

```
┌────────────────────────────────────────────────────┐
│              Compliance Audit Module                │
├──────────────┬──────────────┬──────────────────────┤
│  Framework   │    Gap       │    Evidence          │
│  Engine      │  Analysis    │    Collection        │
├──────────────┼──────────────┼──────────────────────┤
│ ISO 27001   │ Control      │ Cloud APIs           │
│ SOC 2       │ Coverage     │ Ticketing Systems    │
│ PCI DSS     │ Risk Scoring │ Config Management    │
│ HIPAA       │ Remediation  │ Log Aggregation      │
│ GDPR        │ Priorities   │ Manual Uploads       │
│ NIST CSF    │              │                      │
├──────────────┴──────────────┴──────────────────────┤
│         Cross-Framework Mapping Engine              │
├────────────────────────────────────────────────────┤
│  Continuous   │  Audit Trail  │  Reporting          │
│  Monitoring   │  & Integrity  │  Dashboard          │
└────────────────────────────────────────────────────┘
```

The module operates on a four-layer architecture: framework definitions, gap analysis engine, evidence collection pipeline, and cross-framework mapping. The continuous monitoring layer runs independently, detecting drift and triggering alerts when control posture changes.

## Best Practices

1. **Continuous Over Point-in-Time** — Implement continuous compliance monitoring rather than annual audit-driven assessments. Drift detection catches issues early.

2. **Automated Evidence Collection** — Reduce audit burden by automating evidence collection from cloud APIs, logs, and configuration management systems.

3. **Control Rationalization** — Use cross-framework mapping to identify control overlap and reduce redundant control implementations.

4. **Risk-Based Scoping** — Scope compliance efforts based on risk assessment outputs. Not every framework requirement applies equally.

5. **Audit Trail Integrity** — Maintain immutable, timestamped audit trails for all control assessments and evidence artifacts.

6. **Remediation SLAs by Severity** — Non-conformities need aggressive timelines: Critical (24h), Major (30d), Minor (90d).

7. **Third-Party Validation** — Where possible, use independent validation for critical controls to strengthen audit posture.

8. **Framework Update Tracking** — Monitor framework revision cycles and update control mappings when standards change.

9. **Evidence Expiration Management** — Track evidence validity periods and schedule re-collection before expiration.

## Performance Considerations

- Cross-framework mapping with 5+ frameworks completes in under 10 seconds for typical control sets (<500 controls).
- Evidence collection from cloud APIs may be rate-limited; schedule collection during off-peak hours.
- Gap analysis on large frameworks (ISO 27001 with 93 controls) completes in 2-5 seconds with proper indexing.
- Continuous monitoring requires lightweight polling intervals (5-15 minutes) to balance freshness with API costs.
- Report generation for multi-framework assessments benefits from template caching for repeated generation.

## Security Considerations

- Compliance evidence contains sensitive security information; restrict access based on role and audit scope.
- Evidence collection APIs require privileged access; use dedicated service accounts with minimal permissions.
- Audit trails must be tamper-proof to maintain integrity for regulatory examinations.
- Cross-framework mappings reveal control implementation details; protect from external disclosure.
- Evidence packages may contain configuration snapshots; redact sensitive values before external sharing.

## Related Modules

- `risk-assessment` — Risk-based prioritization for compliance investments and gap remediation
- `vulnerability-assessment` — Technical control effectiveness verification and vulnerability correlation
- `security-review` — Control design and implementation review with secure design patterns
- `penetration-testing` — Control validation through adversarial testing and attack simulation

## Configuration Reference

```yaml
# compliance_audit_config.yaml
frameworks:
  - name: ISO27001
    version: "2022"
    scope: ["A.5-A.8"]
  - name: SOC2
    criteria: ["CC", "A", "C", "PI", "R"]
  - name: PCIDSS
    version: "4.0"

evidence_collection:
  sources:
    - type: aws_config
      region: us-east-1
    - type: github
      org: myorg
    - type: jira
      project: SEC
  schedule: daily
  retention_days: 365

monitoring:
  enabled: true
  alert_channels: ["email", "slack"]
  drift_threshold: 5  # percent

reporting:
  formats: ["html", "json", "pdf"]
  include_evidence: true
  executive_summary: true
```

## Integration Guide

The module integrates with common compliance and governance tools:

- **Cloud Platforms** — Connect to AWS Config, Azure Policy, GCP Security Command Center for automated evidence collection.
- **Ticketing Systems** — Integrate with Jira, ServiceNow for non-conformity tracking and remediation workflows.
- **SIEM Integration** — Forward compliance alerts to SIEM platforms for correlation with security events.
- **GRC Platforms** — Export compliance reports to governance, risk, and compliance platforms for enterprise visibility.

## References

- ISO 27001:2022 — Information Security Management Systems
- SOC 2 Type II — AICPA Trust Service Criteria
- PCI DSS v4.0 — Payment Card Industry Data Security Standard
- HIPAA Security Rule — 45 CFR Part 160 and Part 164
- GDPR — General Data Protection Regulation (EU) 2016/679
- NIST CSF 2.0 — Cybersecurity Framework
- CIS Controls v8 — Center for Internet Security Critical Security Controls
- COBIT 2019 — Control Objectives for Information and Related Technologies
