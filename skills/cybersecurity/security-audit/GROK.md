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
