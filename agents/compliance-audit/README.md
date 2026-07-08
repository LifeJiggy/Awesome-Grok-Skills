# Compliance Audit Agent

Comprehensive regulatory compliance assessment, audit management, policy enforcement, risk assessment, evidence management, and remediation tracking supporting SOC 2, GDPR, HIPAA, PCI DSS, ISO 27001, and CCPA.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Compliance Assessment](#compliance-assessment)
  - [Policy Management](#policy-management)
  - [Audit Preparation](#audit-preparation)
  - [Risk Assessment](#risk-assessment)
  - [Evidence Management](#evidence-management)
  - [Remediation Tracking](#remediation-tracking)
  - [Compliance Dashboard](#compliance-dashboard)
- [API Reference](#api-reference)
  - [ComplianceAuditAgent](#complianceauditagent)
  - [ComplianceFrameworkManager](#complianceframeworkmanager)
  - [RiskAssessmentEngine](#riskassessmentengine)
  - [RemediationTracker](#remediationtracker)
  - [EvidenceManager](#evidencemanager)
  - [PolicyManager](#policymanager)
- [Data Models](#data-models)
- [Supported Frameworks](#supported-frameworks)
- [Configuration](#configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Compliance Audit Agent is a Python-based system for managing the full compliance lifecycle from framework selection through assessment, audit execution, risk management, evidence collection, and remediation tracking. It supports multiple regulatory frameworks with built-in control libraries.

**Key Capabilities:**
- Multi-framework compliance assessment (SOC 2, GDPR, HIPAA, PCI DSS, ISO 27001)
- Policy lifecycle management with review scheduling
- Audit preparation and execution support
- Risk assessment with likelihood × impact scoring
- Evidence collection with integrity verification
- Finding lifecycle tracking with remediation management
- Unified compliance dashboard

## Features

| Feature | Description |
|---------|-------------|
| Compliance Assessment | Evaluate controls against framework requirements |
| Policy Management | Create, review, approve, and track policy lifecycle |
| Audit Preparation | Define scope, team, and timeline for audits |
| Risk Assessment | Threat-vulnerability-impact risk modeling |
| Evidence Management | Collect, verify, and track audit evidence |
| Remediation Tracking | Finding lifecycle with deadline management |
| Dashboard | Unified compliance status across all dimensions |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Compliance Audit Agent                      │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │Framework │ │   Risk   │ │Remediation│ │ Evidence │     │
│  │ Manager  │ │Assessment│ │ Tracker   │ │ Manager  │     │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘     │
│       │            │            │            │             │
│  ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐     │
│  │  Audit   │ │ Policy   │ │ Finding  │ │Dashboard │     │
│  │ Manager  │ │ Manager  │ │ Manager  │ │Generator │     │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

```python
from agents.compliance_audit.agent import ComplianceAuditAgent

# Initialize
agent = ComplianceAuditAgent()

# Assess compliance
assessment = agent.assess_compliance("SOC2")
print(f"Status: {assessment['overall_status']}")
print(f"Compliance rate: {assessment['compliance_rate']}")

# Get dashboard
dashboard = agent.get_compliance_dashboard()
print(f"Frameworks: {dashboard['frameworks_available']}")
```

```bash
python agents/compliance-audit/agent.py
```

## Usage

### Compliance Assessment

```python
assessment = agent.assess_compliance(
    framework="SOC2",
    control_scores={
        "CC1.1": 0.9,  # Strong
        "CC6.1": 0.3,  # Weak - needs work
        "CC7.1": 0.7,  # Partial
    },
    organization="Acme Corp",
)

# Result:
# - overall_status: partially_compliant
# - compliance_rate: 0.5 (if 2 of 4 controls pass)
# - gaps: List of non-compliant controls
```

### Policy Management

```python
# Create a policy
policy = agent.review_policy(
    policy_title="Information Security Policy",
    category="information_security",
    owner="CISO",
    frameworks=["SOC2", "ISO27001"],
)

# Approve the policy
agent._policy_manager.approve_policy(
    policy_id=policy["policy_id"],
    approved_by="Board of Directors",
)

# Check policies due for review
due = agent._policy_manager.get_policies_due_for_review()
print(f"Policies due: {len(due)}")
```

### Audit Preparation

```python
audit = agent.prepare_audit(
    title="Annual SOC2 Type 2 Audit",
    framework="SOC2",
    audit_type="external",
    lead_auditor="Jane Smith",
    systems=["Production", "Staging", "Development"],
    departments=["Engineering", "Security", "Operations"],
)

# Result:
# - audit_id: Unique identifier
# - controls_in_scope: 16 (SOC2 controls)
# - planned_start/end: Timeline
```

### Risk Assessment

```python
risk = agent.record_risk(
    asset="Customer Database",
    threat="Data Breach",
    vulnerability="SQL Injection",
    likelihood=0.4,
    impact=0.9,
    mitigation="WAF + Parameterized Queries",
    owner="Security Team",
)

# Risk score: 0.4 × 0.9 = 0.36 → MEDIUM
print(f"Risk level: {risk['risk_level']}")
print(f"Risk score: {risk['risk_score']}")

# Get risk register
register = agent._risk_engine.get_risk_register()
```

### Evidence Management

```python
# Collect evidence
evidence = agent.collect_evidence(
    name="Access Control Policy v2",
    evidence_type="policy",
    description="Current access control policy document",
    control_ids=["CC6.1", "CC6.2"],
    collected_by="Auditor",
)

# Verify evidence
agent._evidence_manager.verify(
    evidence_id=evidence["id"],
    verified_by="External Auditor",
)

# Get stats
stats = agent._evidence_manager.get_stats()
print(f"Verification rate: {stats['verification_rate']}")
```

### Remediation Tracking

```python
from agents.compliance_audit.agent import Finding, Severity

# Add a finding
finding = Finding(
    title="Unencrypted data at rest",
    description="Customer data not encrypted in backup storage",
    severity=Severity.HIGH,
    framework=ComplianceFramework.SOC2,
)
finding_id = agent._remediation_tracker.add_finding(finding)

# Assign remediation
agent._remediation_tracker.assign_remediation(
    finding_id=finding_id,
    owner="Infrastructure Team",
    deadline_days=14,
    plan="Enable encryption at rest for all backup volumes",
)

# Check progress
progress = agent._remediation_tracker.get_progress_report()
print(f"Completion rate: {progress['completion_rate']}")
print(f"Overdue: {progress['overdue_count']}")
```

### Compliance Dashboard

```python
dashboard = agent.get_compliance_dashboard()

print(f"Frameworks: {dashboard['frameworks_available']}")
print(f"Audits: {dashboard['audits']['total']}")
print(f"Risks: {dashboard['risks']['total_risks']}")
print(f"Remediation items: {dashboard['remediation']['total']}")
print(f"Evidence items: {dashboard['evidence']['total']}")
print(f"Policies: {dashboard['policies']['total']}")
```

## API Reference

### ComplianceAuditAgent

| Method | Parameters | Returns |
|--------|-----------|---------|
| `assess_compliance()` | framework, control_scores, organization | Assessment dict |
| `review_policy()` | policy_title, category, content, owner, frameworks | Policy dict |
| `prepare_audit()` | title, framework, audit_type, lead_auditor, systems, departments | Audit dict |
| `record_risk()` | asset, threat, vulnerability, likelihood, impact, mitigation, owner | Risk dict |
| `collect_evidence()` | name, evidence_type, description, control_ids, finding_ids, collected_by | Evidence dict |
| `plan_remediation()` | finding_id, owner, deadline_days, plan | Finding dict |
| `get_compliance_dashboard()` | — | Dashboard dict |
| `list_frameworks()` | — | Frameworks dict |
| `list_audits()` | — | List of audit dicts |
| `get_status()` | — | Agent status dict |

### ComplianceFrameworkManager

| Method | Parameters | Returns |
|--------|-----------|---------|
| `get_controls()` | framework | List of control dicts |
| `get_control()` | framework, control_id | Control dict |
| `map_controls()` | source_framework, target_framework | Mapping dict |

### RiskAssessmentEngine

| Method | Parameters | Returns |
|--------|-----------|---------|
| `assess_risk()` | asset, threat, vulnerability, likelihood, impact, existing_controls, mitigation_plan | Risk assessment |
| `update_residual_risk()` | risk_id, new_residual, mitigation_notes | Updated risk |
| `get_risk_register()` | level_filter | List of risks |
| `risk_summary()` | — | Summary dict |

### RemediationTracker

| Method | Parameters | Returns |
|--------|-----------|---------|
| `add_finding()` | finding | Finding ID |
| `update_status()` | finding_id, new_status, notes, updated_by | Finding dict |
| `assign_remediation()` | finding_id, owner, deadline_days, plan | Finding dict |
| `get_overdue()` | — | List of overdue findings |
| `get_progress_report()` | — | Progress dict |

### EvidenceManager

| Method | Parameters | Returns |
|--------|-----------|---------|
| `collect()` | name, evidence_type, description, control_ids, finding_ids, collected_by | Evidence |
| `verify()` | evidence_id, verified_by | Evidence dict |
| `get_for_control()` | control_id | List of evidence |
| `get_for_finding()` | finding_id | List of evidence |

### PolicyManager

| Method | Parameters | Returns |
|--------|-----------|---------|
| `create_policy()` | title, description, category, content, owner, frameworks | Policy |
| `approve_policy()` | policy_id, approved_by | Policy dict |
| `get_policies_due_for_review()` | — | List of policies |

## Data Models

### Finding
Audit finding with severity, remediation status, owner, and deadline.

### RiskAssessment
Risk entry with threat, vulnerability, likelihood, impact, and mitigation plan.

### Evidence
Audit evidence with type, integrity hash, and verification status.

### Policy
Policy document with lifecycle status, owner, and review schedule.

### Audit
Audit record with scope, team, findings, and compliance rate.

## Supported Frameworks

| Framework | Controls | Focus |
|-----------|----------|-------|
| SOC 2 | 16 | Trust Service Criteria |
| GDPR | 12 | Data Protection |
| HIPAA | 11 | ePHI Safeguards |
| PCI DSS | 12 | Cardholder Data |
| ISO 27001 | 14 domains | ISMS |

## Configuration

```python
config = {
    "user": "compliance_officer",
    "default_framework": "SOC2",
    "compliance_threshold": 0.9,
    "risk_review_days": 90,
}
agent = ComplianceAuditAgent(config)
```

## Best Practices

1. **Assess Regularly** — Don't wait for audit season to check compliance
2. **Risk-Based Prioritization** — Focus on critical and high risks first
3. **Evidence in Advance** — Collect evidence continuously, not during audit crunch
4. **Accountable Remediation** — Every finding needs an owner and a deadline
5. **Policy Lifecycle** — Review and update policies on schedule
6. **Continuous Monitoring** — Compliance is a process, not a point-in-time event

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Low compliance score | Prioritize critical/high severity gaps |
| Evidence not verifiable | Collect additional evidence, verify chain of custody |
| Remediation overdue | Escalate to management, reassign resources |
| Finding keeps reopening | Address root cause, not just symptoms |
| Framework mismatch | Use cross-framework mapping |
| Audit timeline slipping | Narrow scope, increase resources |

## Files

- `agent.py` — Main implementation (~900 lines)
- `ARCHITECTURE.md` — System architecture with diagrams
- `GROK.md` — Agent instructions and identity
- `README.md` — This file

## Contributing

1. Add new compliance framework control libraries
2. Enhance risk scoring algorithms
3. Add integration with GRC platforms
4. Improve evidence management workflows
5. Update documentation for API changes

## License

Part of the Awesome Grok Skills collection. See project root for license details.
