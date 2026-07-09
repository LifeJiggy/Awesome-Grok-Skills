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
- [Design Patterns](#design-patterns)
- [Security](#security)
- [Scalability](#scalability)
- [Configuration](#configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Checklists](#checklists)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Compliance Audit Agent is a Python-based system for managing the full compliance lifecycle from framework selection through assessment, audit execution, risk management, evidence collection, and remediation tracking. It supports multiple regulatory frameworks with built-in control libraries.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    COMPLIANCE AUDIT AGENT                                │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │  Framework   │  │    Risk      │  │ Remediation  │  │  Evidence  │  │
│  │   Manager    │  │  Assessment  │  │   Tracker    │  │  Manager   │  │
│  │              │  │    Engine    │  │              │  │            │  │
│  │ • SOC2       │  │ • Threat     │  │ • Findings   │  │ • Collect  │  │
│  │ • GDPR       │  │ • Vuln       │  │ • Owners     │  │ • Verify   │  │
│  │ • HIPAA      │  │ • Impact     │  │ • Deadlines  │  │ • Audit    │  │
│  │ • PCI DSS    │  │ • Mitigation │  │ • Status     │  │ • Hash     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘  │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────────┐   │
│  │    Audit     │  │   Policy     │  │       Dashboard              │   │
│  │   Manager    │  │   Manager    │  │       Generator              │   │
│  │              │  │              │  │                              │   │
│  │ • Scope      │  │ • Create     │  │ • Framework coverage         │   │
│  │ • Team       │  │ • Approve    │  │ • Risk heatmap               │   │
│  │ • Timeline   │  │ • Review     │  │ • Remediation status         │   │
│  │ • Findings   │  │ • Enforce    │  │ • Evidence completeness      │   │
│  └──────────────┘  └──────────────┘  └──────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    Data Layer                                     │   │
│  │  Controls │ Frameworks │ Findings │ Evidence │ Policies │ Audits  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

**Key Capabilities:**
- Multi-framework compliance assessment (SOC 2, GDPR, HIPAA, PCI DSS, ISO 27001)
- Policy lifecycle management with review scheduling
- Audit preparation and execution support
- Risk assessment with likelihood x impact scoring
- Evidence collection with integrity verification
- Finding lifecycle tracking with remediation management
- Unified compliance dashboard

**Ideal For:**
- Compliance officers managing multiple regulatory frameworks
- Security teams tracking audit readiness
- Risk managers assessing and mitigating compliance risks
- Organizations preparing for external audits

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
| Cross-Framework Mapping | Map controls between different frameworks |
| Compliance Scoring | Weighted scoring with configurable thresholds |
| Escalation Rules | Automatic escalation for overdue items |

## Architecture

### Component Interaction

```
                    ┌─────────────────┐
                    │ ComplianceAudit │
                    │     Agent       │
                    │   (Facade)      │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
    ┌───────▼──────┐ ┌──────▼──────┐ ┌───────▼──────┐
    │  Framework   │ │    Risk     │ │  Evidence    │
    │   Manager    │ │  Assessment │ │   Manager    │
    └───────┬──────┘ └──────┬──────┘ └───────┬──────┘
            │                │                │
    ┌───────▼──────┐ ┌──────▼──────┐ ┌───────▼──────┐
    │ Control      │ │ Risk        │ │ Evidence     │
    │ Library      │ │ Register    │ │ Store        │
    └──────────────┘ └─────────────┘ └──────────────┘
            │                │                │
            └────────────────┼────────────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
    ┌───────▼──────┐ ┌──────▼──────┐ ┌───────▼──────┐
    │   Audit      │ │   Policy    │ │ Remediation  │
    │   Manager    │ │   Manager   │ │   Tracker    │
    └──────────────┘ └─────────────┘ └──────────────┘
```

### Data Flow

```
Framework Selection ──▶ Control Mapping ──▶ Assessment ──▶ Gap Analysis
                                                          │
Evidence Collection ◀─────────────────────────────────────┘
       │
       ▼
Verification ──▶ Finding Creation ──▶ Remediation Plan ──▶ Tracking
       │
       ▼
Dashboard Update ──▶ Reporting ──▶ Executive Summary
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

# Risk score: 0.4 x 0.9 = 0.36 -> MEDIUM
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
| `get_compliance_dashboard()` | -- | Dashboard dict |
| `list_frameworks()` | -- | Frameworks dict |
| `list_audits()` | -- | List of audit dicts |
| `get_status()` | -- | Agent status dict |

### ComplianceFrameworkManager

```python
class ComplianceFrameworkManager:
    def get_controls(self, framework: str) -> List[Dict]:
        """Get all controls for a framework."""

    def get_control(self, framework: str, control_id: str) -> Dict:
        """Get a specific control."""

    def map_controls(self, source: str, target: str) -> Dict:
        """Map controls between frameworks."""

    def get_framework_summary(self, framework: str) -> Dict:
        """Get framework summary with control counts."""
```

### RiskAssessmentEngine

```python
class RiskAssessmentEngine:
    def assess_risk(self, asset: str, threat: str, vulnerability: str,
                    likelihood: float, impact: float,
                    existing_controls: List[str] = None,
                    mitigation_plan: str = "") -> Dict:
        """Full risk assessment with scoring."""

    def update_residual_risk(self, risk_id: str, new_residual: float,
                            mitigation_notes: str = "") -> Dict:
        """Update residual risk after controls."""

    def get_risk_register(self, level_filter: str = None) -> List[Dict]:
        """Get risk register, optionally filtered by level."""

    def risk_summary(self) -> Dict:
        """Summary of all risks by level."""

    def get_top_risks(self, limit: int = 10) -> List[Dict]:
        """Get highest-rated risks."""
```

### RemediationTracker

```python
class RemediationTracker:
    def add_finding(self, finding: Finding) -> str:
        """Add a finding, return finding_id."""

    def update_status(self, finding_id: str, new_status: FindingStatus,
                     notes: str = "", updated_by: str = "") -> Dict:
        """Update finding status."""

    def assign_remediation(self, finding_id: str, owner: str,
                          deadline_days: int, plan: str = "") -> Dict:
        """Assign remediation with deadline."""

    def get_overdue(self) -> List[Dict]:
        """Get all overdue findings."""

    def get_progress_report(self) -> Dict:
        """Completion rate, overdue count, by severity."""
```

### EvidenceManager

```python
class EvidenceManager:
    def collect(self, name: str, evidence_type: str, description: str,
               control_ids: List[str] = None, finding_ids: List[str] = None,
               collected_by: str = "") -> Dict:
        """Collect evidence with integrity hash."""

    def verify(self, evidence_id: str, verified_by: str) -> Dict:
        """Verify evidence integrity."""

    def get_for_control(self, control_id: str) -> List[Dict]:
        """Get all evidence for a control."""

    def get_for_finding(self, finding_id: str) -> List[Dict]:
        """Get all evidence for a finding."""

    def get_stats(self) -> Dict:
        """Verification rates, by type, total count."""
```

### PolicyManager

```python
class PolicyManager:
    def create_policy(self, title: str, description: str, category: str,
                     content: str = "", owner: str = "",
                     frameworks: List[str] = None) -> Dict:
        """Create a new policy."""

    def approve_policy(self, policy_id: str, approved_by: str) -> Dict:
        """Approve a policy."""

    def get_policies_due_for_review(self) -> List[Dict]:
        """Get policies needing review."""

    def archive_policy(self, policy_id: str) -> Dict:
        """Archive an obsolete policy."""

    def get_policy_status(self, policy_id: str) -> Dict:
        """Get policy lifecycle status."""
```

## Data Models

### Finding
Audit finding with severity, remediation status, owner, and deadline.

```python
@dataclass
class Finding:
    finding_id: str
    title: str
    description: str
    severity: Severity  # CRITICAL, HIGH, MEDIUM, LOW, INFO
    framework: ComplianceFramework
    control_ids: List[str]
    status: FindingStatus = FindingStatus.OPEN
    owner: str = ""
    deadline: Optional[datetime] = None
    remediation_plan: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
```

### RiskAssessment
Risk entry with threat, vulnerability, likelihood, impact, and mitigation plan.

### Evidence
Audit evidence with type, integrity hash, and verification status.

### Policy
Policy document with lifecycle status, owner, and review schedule.

### Audit
Audit record with scope, team, findings, and compliance rate.

## Supported Frameworks

| Framework | Controls | Focus | Key Areas |
|-----------|----------|-------|-----------|
| SOC 2 | 16 | Trust Service Criteria | Security, Availability, Processing Integrity, Confidentiality, Privacy |
| GDPR | 12 | Data Protection | Consent, Data Subject Rights, Breach Notification, DPO |
| HIPAA | 11 | ePHI Safeguards | Administrative, Physical, Technical |
| PCI DSS | 12 | Cardholder Data | Network Security, Access Control, Monitoring, Testing |
| ISO 27001 | 14 domains | ISMS | Risk Management, Controls, Continual Improvement |
| CCPA | 10 | Consumer Privacy | Right to Know, Delete, Opt-Out, Non-Discrimination |

### Framework Mapping

```
SOC 2 CC6.1 ◀──▶ ISO 27001 A.9.1 ◀──▶ HIPAA §164.312(a)
SOC 2 CC7.1 ◀──▶ ISO 27001 A.12.4 ◀──▶ PCI DSS 10.1
SOC 2 CC3.1 ◀──▶ ISO 27001 A.8.2  ◀──▶ GDPR Art. 32
```

## Design Patterns

| Pattern | Usage | Component |
|---------|-------|-----------|
| **Facade** | Unified compliance interface | ComplianceAuditAgent |
| **Strategy** | Different scoring algorithms per framework | ComplianceFrameworkManager |
| **Observer** | Notify on status changes | RemediationTracker |
| **Builder** | Construct complex audit objects | Audit Preparation |
| **Chain of Responsibility** | Escalation rules processing | Escalation Engine |
| **Decorator** | Add verification hashing to evidence | EvidenceManager |
| **State Machine** | Finding lifecycle transitions | RemediationTracker |
| **Template Method** | Framework-specific assessment flows | Assessment Engine |

## Security

- All evidence files hashed with SHA-256 for integrity verification
- Access controls on policy approval workflows
- Audit trail for all compliance actions
- Sensitive data encryption at rest
- Role-based access for different compliance operations
- Regular access reviews and privilege audits
- Evidence chain of custody tracking
- Tamper-evident logging for all assessments

```
┌──────────────────────────────────────────────────┐
│              Security Controls                    │
├──────────────────────────────────────────────────┤
│ Authentication ──▶ Authorization ──▶ Audit Log   │
│       │                  │                │       │
│  MFA Support      Role-Based        Immutable    │
│  SSO Integration  Permission Set    Tamper-proof │
│  API Keys         Resource Scope    Retention    │
└──────────────────────────────────────────────────┘
```

## Scalability

| Dimension | Strategy | Notes |
|-----------|----------|-------|
| Control Library | Lazy loading by framework | Load only active frameworks |
| Evidence Storage | File system with metadata DB | Hash-based deduplication |
| Risk Register | Indexed by severity and owner | Fast filtered queries |
| Audit History | Partitioned by year | Archive old audits |
| Concurrent Assessments | Async processing | Multiple framework assessments |
| Dashboard | Cached aggregation | Refresh on write |
| Policy Versioning | Append-only history | Full audit trail |

### Performance Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| Control lookup | < 1ms | Indexed by framework + ID |
| Assessment scoring | < 50ms | Per-framework calculation |
| Evidence verification | < 100ms | SHA-256 hash comparison |
| Risk register query | < 20ms | Indexed filtering |
| Dashboard generation | < 200ms | Cached aggregation |
| Policy search | < 10ms | Full-text indexed |

## Configuration

```python
config = {
    "user": "compliance_officer",
    "default_framework": "SOC2",
    "compliance_threshold": 0.9,
    "risk_review_days": 90,
    "evidence_retention_days": 365,
    "audit_retention_days": 2555,  # 7 years
    "max_concurrent_audits": 10,
    "evidence_hash_algorithm": "sha256",
    "auto_escalation_enabled": True,
    "escalation_threshold_days": 7,
}
agent = ComplianceAuditAgent(config)
```

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `default_framework` | `"SOC2"` | Default compliance framework |
| `compliance_threshold` | `0.9` | Minimum compliance score |
| `risk_review_days` | `90` | Risk assessment review frequency |
| `evidence_retention_days` | `365` | Evidence retention period |
| `audit_retention_days` | `2555` | Audit record retention (7 years) |
| `max_concurrent_audits` | `10` | Maximum simultaneous audits |
| `evidence_hash_algorithm` | `"sha256"` | Hash algorithm for evidence integrity |
| `auto_escalation_enabled` | `True` | Enable automatic escalation |
| `escalation_threshold_days` | `7` | Days before escalation |

## Examples

### Full Compliance Workflow

```python
from agents.compliance_audit.agent import ComplianceAuditAgent

agent = ComplianceAuditAgent()

# 1. Assess compliance
assessment = agent.assess_compliance(
    framework="SOC2",
    control_scores={
        "CC1.1": 0.9,
        "CC6.1": 0.3,
        "CC7.1": 0.7,
    },
)

# 2. Record risks
risk = agent.record_risk(
    asset="Customer Database",
    threat="Data Breach",
    vulnerability="Weak access controls",
    likelihood=0.4,
    impact=0.9,
)

# 3. Collect evidence
evidence = agent.collect_evidence(
    name="Access Control Policy",
    evidence_type="policy",
    control_ids=["CC6.1"],
)

# 4. Add finding
from agents.compliance_audit.agent import Finding, Severity
finding = Finding(
    title="Weak access controls",
    description="Customer database lacks RBAC",
    severity=Severity.HIGH,
)
finding_id = agent._remediation_tracker.add_finding(finding)

# 5. Track remediation
agent._remediation_tracker.assign_remediation(
    finding_id=finding_id,
    owner="Security Team",
    deadline_days=14,
)

# 6. Generate dashboard
dashboard = agent.get_compliance_dashboard()
print(f"Compliance Status: {dashboard['overall_status']}")
```

### Cross-Framework Mapping

```python
# Map SOC2 controls to ISO 27001
mapping = agent._framework_manager.map_controls("SOC2", "ISO27001")

for soc2_control, iso_control in mapping.items():
    print(f"{soc2_control} -> {iso_control}")

# Use mapping to avoid duplicate evidence
evidence = agent.collect_evidence(
    name="Access Control Evidence",
    evidence_type="technical",
    control_ids=["CC6.1", "A.9.1.1"],  # Both frameworks
)
```

## Best Practices

1. **Assess Regularly** -- Don't wait for audit season to check compliance
2. **Risk-Based Prioritization** -- Focus on critical and high risks first
3. **Evidence in Advance** -- Collect evidence continuously, not during audit crunch
4. **Accountable Remediation** -- Every finding needs an owner and a deadline
5. **Policy Lifecycle** -- Review and update policies on schedule
6. **Continuous Monitoring** -- Compliance is a process, not a point-in-time event
7. **Cross-Framework Mapping** -- Leverage control mappings to reduce duplication
8. **Automation First** -- Automate evidence collection and verification where possible
9. **Regular Training** -- Ensure all stakeholders understand compliance requirements
10. **Document Everything** -- Maintain comprehensive audit trails

## Checklists

### Pre-Audit Readiness

- [ ] All framework controls mapped and scored
- [ ] Evidence collected for every in-scope control
- [ ] Evidence integrity verified (SHA-256 hashes)
- [ ] All high/critical findings remediated or have approved plans
- [ ] Policies reviewed and approved within last 12 months
- [ ] Risk register updated within last 90 days
- [ ] Audit team assigned and briefed on scope
- [ ] Systems inventory current and accurate
- [ ] Previous audit findings closed
- [ ] Stakeholder communication plan ready

### Risk Assessment Checklist

- [ ] All assets inventoried and classified
- [ ] Threat landscape reviewed for each asset
- [ ] Vulnerabilities identified through scanning/assessment
- [ ] Likelihood scores assigned with justification
- [ ] Impact scores assigned with business context
- [ ] Existing controls documented
- [ ] Residual risk calculated after controls
- [ ] Mitigation plans created for high/critical risks
- [ ] Risk owners assigned
- [ ] Review schedule established

### Evidence Collection Checklist

- [ ] Evidence type classified (document, technical, interview)
- [ ] Evidence linked to specific controls
- [ ] Collection date and collector documented
- [ ] Integrity hash generated (SHA-256)
- [ ] Chain of custody maintained
- [ ] Storage location secure and accessible
- [ ] Retention period defined
- [ ] Verification status recorded
- [ ] Backup copies stored separately
- [ ] Access permissions restricted

## Troubleshooting

| Problem | Diagnosis | Solution |
|---------|-----------|----------|
| Low compliance score | Missing controls or weak implementations | Prioritize critical/high severity gaps first |
| Evidence not verifiable | Hash mismatch or corrupt file | Collect fresh evidence, verify chain of custody |
| Remediation overdue | Resource constraints or unclear ownership | Escalate to management, reassign resources |
| Finding keeps reopening | Root cause not addressed | Address root cause, not just symptoms |
| Framework mismatch | Controls don't align between frameworks | Use cross-framework mapping to find equivalents |
| Audit timeline slipping | Scope too broad or resources insufficient | Narrow scope, increase resources, negotiate timeline |
| Risk assessments outdated | No scheduled review process | Schedule quarterly risk assessments with reminders |
| Policy not enforced | No training or monitoring | Implement mandatory compliance training program |
| Dashboard shows stale data | Cache not refreshed | Clear cache, verify data pipeline |
| Control library incomplete | Framework update not applied | Update control library to latest version |
| Escalation not firing | Threshold not configured | Review escalation rules and thresholds |
| Finding severity incorrect | Misclassification | Reassess using CVSS or custom severity matrix |

## Files

- `agent.py` -- Main implementation (~900 lines)
- `ARCHITECTURE.md` -- System architecture with diagrams
- `GROK.md` -- Agent instructions and identity
- `README.md` -- This file

## Contributing

1. Add new compliance framework control libraries
2. Enhance risk scoring algorithms
3. Add integration with GRC platforms
4. Improve evidence management workflows
5. Add automated control testing capabilities
6. Update documentation for API changes

## License

Part of the Awesome Grok Skills collection. See project root for license details.
