# Compliance Agent

Regulatory compliance management, policy tracking, audit trail generation, privacy management, security auditing, risk assessment, and remediation planning across multiple compliance frameworks.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Compliance Checking](#compliance-checking)
  - [Audit Trail](#audit-trail)
  - [Privacy Management](#privacy-management)
  - [Security Auditing](#security-auditing)
  - [Risk Assessment](#risk-assessment)
  - [Policy Management](#policy-management)
- [API Reference](#api-reference)
- [Compliance Frameworks](#compliance-frameworks)
- [Data Models](#data-models)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Compliance Agent is a Python-based system for managing regulatory compliance across multiple frameworks including GDPR, HIPAA, SOC 2, PCI DSS, ISO 27001, CCPA, SOX, and NIST 800-53. It provides compliance checking, audit trail management, privacy request handling, security finding tracking, risk assessment, and policy management.

**Key Capabilities:**
- Multi-framework compliance requirement tracking
- Evidence-based compliance checking with scoring
- Complete audit trail with query and export
- GDPR data subject request handling
- Security vulnerability tracking and remediation
- Risk assessment with severity matrices
- Policy creation, approval, and version tracking

## Features

| Feature | Description |
|---------|-------------|
| Compliance Checking | Track requirements, evaluate evidence, score compliance |
| Audit Trail | Immutable logging with query and export capabilities |
| Privacy Management | Data subject registration, consent, GDPR requests |
| Security Auditing | Vulnerability tracking with severity and remediation |
| Risk Assessment | Likelihood x Impact scoring with mitigation tracking |
| Policy Management | Policy creation, approval, version control |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Compliance Agent                         │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │Compliance│ │  Audit   │ │ Privacy  │ │ Security │     │
│  │ Checker  │ │  Logger  │ │ Manager  │ │ Auditor  │     │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘     │
│       │            │            │            │             │
│  ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐     │
│  │  Risk    │ │  Policy  │ │  Data    │ │  Report  │     │
│  │Assessor  │ │ Manager  │ │Subjects  │ │Generator │     │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

```python
from agents.compliance.agent import ComplianceAgent

agent = ComplianceAgent()

# Add a requirement
req = agent.add_requirement(
    framework="gdpr",
    control_id="GDPR-001",
    requirement="Data Consent",
    severity="high",
)

# Check compliance
result = agent.check_compliance(req["id"], {"data_consent": True})
print(f"Status: {result['status']}")

# Generate report
report = agent.generate_compliance_report("gdpr")
print(f"Score: {report['compliance_score']}%")
```

```bash
python agents/compliance/agent.py
```

## Usage

### Compliance Checking

```python
# Add requirements
agent.add_requirement("gdpr", "GDPR-001", "Data Consent", severity="high")
agent.add_requirement("gdpr", "GDPR-002", "Data Retention", severity="medium")

# Check each requirement
agent.check_compliance(req1_id, {"data_consent": True})
agent.check_compliance(req2_id, {"retention_policy": True})

# Generate report
report = agent.generate_compliance_report("gdpr")
print(f"Compliant: {report['compliant']}, Score: {report['compliance_score']}%")
```

### Audit Trail

```python
# Log events
agent.log_audit_event("CREATE", "admin@company.com", "user:123")
agent.log_audit_event("ACCESS", "user@company.com", "doc:456")
agent.log_audit_event("DELETE", "admin@company.com", "user:789")

# Query logs
logs = agent.query_audit_logs(actor="admin@company.com")
logs = agent.query_audit_logs(action="DELETE")

# Export for audit
export = agent._audit_logger.export_for_compliance("2024-01-01", "2024-12-31")
```

### Privacy Management

```python
# Register data subject
subject = agent.register_data_subject(
    email="john@example.com",
    name="John Doe",
    data_categories=["personal", "behavioral"],
)

# Record consent
agent.record_consent(subject["id"], "marketing", True)

# Handle GDPR requests
agent.handle_data_request(subject["id"], "access")       # Export data
agent.handle_data_request(subject["id"], "deletion")     # Delete data
agent.handle_data_request(subject["id"], "portability")  # Export JSON

# Privacy report
report = agent.get_privacy_report()
print(f"Consent rate: {report['consent_rate']}%")
```

### Security Auditing

```python
# Run scan
scan = agent.run_security_scan("api.example.com")

# Add findings
agent.add_security_finding(scan["scan_id"], "SQL Injection", "critical")
agent.add_security_finding(scan["scan_id"], "XSS", "high")

# Update finding status
agent._security_auditor.update_finding_status(finding_id, "remediated")

# Security report
report = agent.get_security_report(days=30)
print(f"Open findings: {report['open_findings']}")
```

### Risk Assessment

```python
# Create assessment
risk = agent.create_risk_assessment(
    asset="Customer Database",
    threat="Data Breach",
    vulnerability="Weak access controls",
    likelihood="medium",
    impact="critical",
    mitigation="Implement RBAC",
)

# Risk summary
summary = agent.get_risk_summary()
print(f"Critical risks: {summary['critical_risks']}")
```

### Policy Management

```python
# Create policy
policy = agent.create_policy(
    title="Data Protection Policy",
    framework="gdpr",
    content="All personal data must be processed lawfully...",
    owner="DPO",
)

# Approve
agent.approve_policy(policy["id"], "CISO")

# Summary
summary = agent.get_policy_summary()
print(f"Policies: {summary['total_policies']}")
```

## API Reference

### ComplianceAgent

| Method | Parameters | Returns |
|--------|-----------|---------|
| `add_requirement()` | framework, control_id, requirement, description, severity, owner | Requirement dict |
| `check_compliance()` | requirement_id, evidence, passed | Check result dict |
| `generate_compliance_report()` | framework | Report dict |
| `log_audit_event()` | action, actor, resource, details | Log entry dict |
| `query_audit_logs()` | actor, action, resource | List of log entries |
| `register_data_subject()` | email, name, data_categories | Subject dict |
| `record_consent()` | subject_id, purpose, granted | Consent record dict |
| `handle_data_request()` | subject_id, request_type | Request result dict |
| `get_privacy_report()` | — | Privacy report dict |
| `run_security_scan()` | target, scan_type | Scan dict |
| `add_security_finding()` | scan_id, title, severity, description | Finding dict |
| `get_security_report()` | days | Security report dict |
| `create_risk_assessment()` | asset, threat, vulnerability, likelihood, impact, mitigation | Assessment dict |
| `get_risk_summary()` | — | Risk summary dict |
| `create_policy()` | title, framework, content, owner | Policy dict |
| `approve_policy()` | policy_id, approved_by | Approval dict |
| `get_policy_summary()` | — | Policy summary dict |
| `get_status()` | — | Agent status dict |

## Compliance Frameworks

| Framework | Focus Area | Key Controls |
|-----------|-----------|--------------|
| GDPR | EU data protection | Consent, data rights, breach notification |
| HIPAA | Health data privacy | Access controls, audit trails, encryption |
| SOC 2 | Service organization controls | Security, availability, confidentiality |
| PCI DSS | Payment card data | Network security, access control, monitoring |
| ISO 27001 | Information security | Risk management, controls, continuous improvement |
| CCPA | California consumer privacy | Consumer rights, data disclosure, opt-out |

## Data Models

### ComplianceRequirement
Tracks framework requirements with status, severity, evidence, and verification.

### AuditLogEntry
Immutable audit trail entries with actor, action, resource, timestamp, and context.

### DataSubject
Data subject records with consent tracking and data category management.

### SecurityFinding
Security vulnerabilities with severity, status, CVSS scores, and remediation plans.

### RiskAssessment
Risk evaluations with likelihood, impact, risk level, and mitigation plans.

## Configuration

```python
config = {
    "frameworks": ["gdpr", "soc2", "hipaa"],
    "default_severity": "high",
    "audit_retention_days": 365,
}
agent = ComplianceAgent(config)
```

## Best Practices

1. **Document Everything** — If it's not documented, it didn't happen
2. **Review Regularly** — Schedule quarterly compliance reviews
3. **Train Teams** — Ensure all teams understand compliance requirements
4. **Automate Where Possible** — Use the agent for routine compliance checks
5. **Maintain Evidence** — Keep evidence current and accessible
6. **Act on Findings** — Address non-compliance promptly
7. **Test Incident Response** — Practice breach notification procedures

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Compliance score low | Gather evidence for non-compliant requirements |
| Audit logs missing | Add logging to all critical operations |
| Privacy request failing | Verify data subject ID and registration |
| Security findings stale | Schedule regular vulnerability scans |
| Risk assessments outdated | Review and update quarterly |
| Policy not approved | Route to appropriate approver |

## Files

- `agent.py` — Main implementation (~900 lines)
- `ARCHITECTURE.md` — System architecture with diagrams
- `GROK.md` — Agent instructions and identity
- `README.md` — This file

## Contributing

1. Add new compliance framework support
2. Enhance evidence evaluation logic
3. Add automated scanning integrations
4. Improve reporting and dashboards
5. Update documentation for API changes

## License

Part of the Awesome Grok Skills collection. See project root for license details.
