---
name: "security-audit"
category: "cybersecurity"
version: "2.0.0"
tags: ["cybersecurity", "security-audit", "compliance", "assessment", "governance"]
---

# Security Audit

## Overview

The Security Audit module provides systematic frameworks for evaluating security posture, compliance adherence, and control effectiveness across IT environments. It covers audit planning, control assessment, risk evaluation, compliance checking (ISO 27001, SOC 2, NIST CSF, PCI DSS), and audit reporting.

This skill is essential for security auditors, compliance officers, and GRC teams conducting internal and external security assessments.

## Core Capabilities

- **Audit Planning**: Scope definition, audit scheduling, and resource allocation
- **Control Assessment**: Technical and administrative control testing and evaluation
- **Compliance Mapping**: Mapping controls to frameworks (NIST, ISO, SOC 2, PCI DSS, HIPAA)
- **Risk Assessment**: Risk identification, scoring, and treatment recommendation
- **Gap Analysis**: Current state vs desired state gap identification
- **Audit Evidence**: Evidence collection, documentation, and chain of custody
- **Reporting**: Executive summaries, detailed findings, and remediation roadmaps
- **Continuous Monitoring**: Ongoing compliance monitoring and drift detection

## Usage Examples

```python
from security_audit import (
    AuditPlanner,
    ControlAssessor,
    ComplianceMapper,
    RiskEvaluator,
    AuditReport,
)

# --- Audit Planning ---
planner = AuditPlanner()
plan = planner.create_plan(
    title="Annual Security Audit 2024",
    scope=["IT infrastructure", "applications", "data protection"],
    frameworks=["ISO 27001", "SOC 2"],
    duration_days=30,
    team_size=4,
)
print(f"Audit: {plan.audit_id}")
print(f"Controls: {plan.total_controls}")
print(f"Duration: {plan.duration_days} days")

# --- Control Assessment ---
assessor = ControlAssessor()
results = assessor.assess_controls(
    control_ids=["A.8.1.1", "A.8.1.2", "A.9.1.1"],
    evidence=[
        {"control": "A.8.1.1", "status": "pass", "evidence": "Inventory maintained"},
        {"control": "A.8.1.2", "status": "fail", "evidence": "No media policy"},
    ],
)
for r in results:
    print(f"  {r.control_id}: {r.status} ({r.score}/100)")

# --- Compliance Mapping ---
mapper = ComplianceMapper()
mapping = mapper.map_controls(
    source="internal_controls",
    target_framework="SOC 2",
)
print(f"Mapped: {mapping.mapped_count}/{mapping.total_count}")
print(f"Gaps: {len(mapping.gaps)}")

# --- Risk Evaluation ---
evaluator = RiskEvaluator()
risks = evaluator.evaluate(
    findings=[
        {"title": "Missing MFA", "likelihood": "high", "impact": "high"},
        {"title": "Unencrypted data", "likelihood": "medium", "impact": "critical"},
    ],
)
for risk in risks:
    print(f"  [{risk.risk_level}] {risk.title}: {risk.score}")

# --- Audit Report ---
report = AuditReport()
report.generate(
    audit_plan=plan,
    control_results=results,
    risk_assessment=risks,
)
print(f"Report generated: {report.title}")
print(f"Overall score: {report.overall_score}")
```

## Best Practices

- Define clear audit scope and objectives before starting any assessment
- Use risk-based approach to prioritize controls for deep assessment
- Map all findings to specific control frameworks for compliance evidence
- Collect evidence with proper chain of custody for audit trail
- Provide actionable remediation steps with priority and timeline
- Conduct follow-up audits to verify remediation effectiveness
- Maintain independence — auditors should not assess their own work
- Use automated compliance monitoring for continuous assurance
- Document all assumptions, limitations, and scope exclusions
- Present findings in both technical detail and executive summary formats

## Related Modules

- **penetration-testing**: Technical security testing for audit evidence
- **threat-intelligence**: Threat context for risk assessments
- **incident-response**: Incident history review for audit findings
- **zero-trust-security**: Zero trust architecture compliance assessment

---

## Advanced Configuration

### Audit Framework Configuration

Configure audit frameworks and standards.

```python
audit_framework = AuditFrameworkConfig(
    frameworks={
        "iso27001": {"version": "2022", "controls": 93},
        "soc2": {"type": "type_ii", "trust_service_criteria": ["security", "availability", "confidentiality"]},
        "nist_csf": {"version": "1.1", "functions": ["identify", "protect", "detect", "respond", "recover"]},
        "pci_dss": {"version": "4.0", "requirements": 12},
    },
    selected_frameworks=["iso27001", "soc2"],
)
```

### Risk Scoring Configuration

Configure risk scoring methodology.

```python
risk_config = RiskScoringConfig(
    methodology="qualitative",
    scales={
        "likelihood": {"low": 1, "medium": 2, "high": 3, "very_high": 4},
        "impact": {"negligible": 1, "minor": 2, "moderate": 3, "major": 4, "critical": 5},
    },
    risk_matrix={
        (1, 1): "low", (1, 2): "low", (1, 3): "medium", (1, 4): "high",
        (2, 1): "low", (2, 2): "medium", (2, 3): "high", (2, 4): "very_high",
        (3, 1): "medium", (3, 2): "high", (3, 3): "very_high", (3, 4): "very_high",
    },
)
```

### Evidence Collection Configuration

Configure audit evidence requirements.

```python
evidence_config = AuditEvidenceConfig(
    evidence_types={
        "technical": ["screenshots", "config_exports", "logs", "scan_results"],
        "administrative": ["policies", "procedures", "training_records"],
        "physical": ["access_logs", "badge_records", "visitor_logs"],
    },
    retention_period_years=7,
    chain_of_custody_required=True,
)
```

---

## Architecture Patterns

### Audit Workflow Pattern

```python
class AuditWorkflow:
    phases = [
        "planning",
        "fieldwork",
        "analysis",
        "reporting",
        "follow_up",
    ]

    def execute(self, audit_plan):
        context = {"plan": audit_plan, "evidence": [], "findings": []}
        for phase in self.phases:
            handler = self.get_phase_handler(phase)
            context = handler.execute(context)
        return context
```

### Control Assessment Pattern

```python
class ControlAssessment:
    def __init__(self, control):
        self.control = control
        self.evidence = []
        self.tests = []

    def add_test(self, test):
        self.tests.append(test)

    def assess(self):
        results = []
        for test in self.tests:
            result = test.execute(self.control)
            results.append(result)
        return AssessmentResult(
            control=self.control,
            results=results,
            status=self.calculate_status(results),
        )
```

### Finding Management Pattern

```python
class FindingManager:
    def __init__(self):
        self.findings = []
        self.severity_map = {
            "critical": 4,
            "high": 3,
            "medium": 2,
            "low": 1,
            "informational": 0,
        }

    def add_finding(self, finding):
        self.findings.append(finding)
        self.findings.sort(key=lambda f: self.severity_map[f.severity], reverse=True)
```

---

## Integration Guide

### Compliance Automation

```python
# Automated compliance checking
compliance_checker = ComplianceChecker(
    framework="iso27001",
    controls=is27001_controls,
)

results = compliance_checker.check_all(
    evidence_store="/evidence",
    output_format="json",
)
```

### Audit Management Tools

```python
# Integration with audit management platforms
audit_tool = AuditManagementPlatform(
    platform="servicenow",
    instance="company.service-now.com",
    api_key="...",
)

# Create audit record
audit_record = audit_tool.create_audit(
    title="Annual Security Audit 2024",
    framework="ISO 27001",
    start_date="2024-01-15",
    end_date="2024-02-15",
)
```

---

## Performance Optimization

### Parallel Evidence Collection

```python
# Collect evidence from multiple sources in parallel
def collect_evidence_parallel(sources):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(collect, s) for s in sources]
        return [f.result() for f in futures]
```

### Finding Deduplication

```python
# Deduplicate findings across audits
class FindingDeduplicator:
    def deduplicate(self, findings):
        seen = {}
        unique = []
        for finding in findings:
            key = self.generate_key(finding)
            if key not in seen:
                seen[key] = finding
                unique.append(finding)
        return unique
```

---

## Security Considerations

### Audit Data Protection

```python
# Protect audit evidence
class AuditDataProtector:
    def __init__(self):
        self.encryption_key = get_encryption_key()

    def encrypt_evidence(self, evidence):
        return encrypt(evidence, self.encryption_key)

    def access_control(self, user, evidence):
        return user.role in ["auditor", "admin"]
```

---

## Troubleshooting Guide

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Evidence missing | Access denied | Request proper access |
| Control not applicable | Scope issue | Document rationale |
| Finding disputed | Insufficient evidence | Gather more evidence |

---

## API Reference

### AuditPlanner

```python
class AuditPlanner:
    def create_plan(title, scope, frameworks, duration_days, team_size) -> AuditPlan
    def create_checklist(plan) -> List[AuditTask]
    def assign_resources(plan, resources) -> None
```

### ControlAssessor

```python
class ControlAssessor:
    def assess_controls(control_ids, evidence) -> List[ControlResult]
    def test_control(control_id, test_procedure) -> TestResult
    def score_control(control_id, results) -> ControlScore
```

### ComplianceMapper

```python
class ComplianceMapper:
    def map_controls(source, target_framework) -> ComplianceMapping
    def find_gaps(mapping) -> List[Gap]
    def generate_remediation_plan(gaps) -> RemediationPlan
```

---

## Data Models

### AuditPlan

```python
@dataclass
class AuditPlan:
    audit_id: str
    title: str
    scope: List[str]
    frameworks: List[str]
    duration_days: int
    team_size: int
    total_controls: int
    status: str
```

### ControlResult

```python
@dataclass
class ControlResult:
    control_id: str
    status: str  # pass, fail, partial, not_applicable
    score: int
    evidence: List[Evidence]
    findings: List[Finding]
    recommendations: List[str]
```

---

## Deployment Guide

### Audit Management System

```yaml
services:
  audit-platform:
    image: audit-management:latest
    environment:
      - DATABASE_URL=postgresql://...
      - S3_BUCKET=audit-evidence
    volumes:
      - ./evidence:/evidence
```

---

## Monitoring & Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `audit.controls.assessed` | Controls assessed | Track |
| `audit.findings.open` | Open findings | Track |
| `audit.remediation.overdue` | Overdue remediations | > 0 |

---

## Testing Strategy

### Audit Tests

```python
def test_control_assessment():
    assessor = ControlAssessor()
    result = assessor.assess_control("A.8.1.1", evidence)
    assert result.status in ["pass", "fail", "partial"]
```

---

## Versioning & Migration

### Framework Versioning

Track framework versions for compliance.

---

## Glossary

| Term | Definition |
|------|-----------|
| **Control** | Security measure to mitigate risk |
| **Finding** | Identified security issue or gap |
| **Evidence** | Proof of control implementation |
| **Remediation** | Action to fix a finding |
| **Compliance** | Adherence to standards/frameworks |

---

## Changelog

### v2.0.0
- Added multi-framework support
- Automated evidence collection
- Risk scoring matrix

### v1.0.0
- Initial release with basic audit planning

---

## Contributing Guidelines

- Document all audit procedures
- Maintain evidence integrity
- Provide actionable recommendations

---

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills
