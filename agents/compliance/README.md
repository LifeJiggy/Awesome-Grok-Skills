# Compliance Agent

Regulatory compliance management, policy tracking, audit trail generation, privacy management, security auditing, risk assessment, and remediation planning across multiple compliance frameworks.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Compliance Checking](#compliance-checking)
  - [Audit Trail](#audit-trail)
  - [Privacy Management](#privacy-management)
  - [Security Auditing](#security-auditing)
  - [Risk Assessment](#risk-assessment)
  - [Policy Management](#policy-management)
  - [Reporting and Analytics](#reporting-and-analytics)
  - [Integration with External Systems](#integration-with-external-systems)
- [API Reference](#api-reference)
  - [ComplianceAgent Methods](#complianceagent-methods)
  - [Helper Classes](#helper-classes)
- [Compliance Frameworks](#compliance-frameworks)
  - [Framework Details](#framework-details)
  - [Mapping Controls](#mapping-controls)
- [Data Models](#data-models)
  - [ComplianceRequirement](#compliancerequirement)
  - [AuditLogEntry](#auditlogentry)
  - [DataSubject](#datasubject)
  - [SecurityFinding](#securityfinding)
  - [RiskAssessment](#riskassessment)
  - [Policy](#policy)
- [Configuration](#configuration)
  - [Basic Configuration](#basic-configuration)
  - [Advanced Configuration](#advanced-configuration)
  - [Environment Variables](#environment-variables)
- [Extending the Agent](#extending-the-agent)
  - [Adding New Frameworks](#adding-new-frameworks)
  - [Custom Evidence Evaluators](#custom-evidence-evaluators)
  - [Plugins and Hooks](#plugins-and-hooks)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Examples](#examples)
  - [Example 1: GDPR Compliance Check](#example-1-gdpr-compliance-check)
  - [Example 2: HIPAA Audit Trail](#example-2-hipaa-audit-trail)
  - [Example 3: SOC 2 Risk Assessment](#example-3-soc-2-risk-assessment)
  - [Example 4: PCI DSS Policy Management](#example-4-pci-dss-policy-management)
  - [Example 5: ISO 27001 Integration](#example-5-iso-27001-integration)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Compliance Agent is a comprehensive Python-based system designed for managing regulatory compliance across multiple frameworks including GDPR, HIPAA, SOC 2, PCI DSS, ISO 27001, CCPA, SOX, and NIST 800-53. It provides compliance checking, audit trail management, privacy request handling, security finding tracking, risk assessment, and policy management.

**Key Capabilities:**
- Multi-framework compliance requirement tracking with customizable controls
- Evidence-based compliance checking with automated scoring and validation
- Complete audit trail with immutable logging, query capabilities, and export formats
- GDPR data subject request handling including access, deletion, and portability
- Security vulnerability tracking with severity assessment and remediation planning
- Risk assessment with likelihood x impact scoring matrices and mitigation tracking
- Policy creation, approval workflows, version control, and lifecycle management
- Integration-ready APIs for external system connectivity
- Real-time compliance dashboards and reporting
- Automated compliance monitoring and alerting

**Use Cases:**
- Enterprise compliance teams managing multiple regulatory requirements
- Security teams conducting audits and vulnerability management
- Privacy officers handling GDPR/CCPA data subject requests
- Risk managers assessing and mitigating organizational risks
- Policy administrators creating and enforcing compliance policies
- External auditors requiring compliance evidence and reports
- DevOps teams integrating compliance checks into CI/CD pipelines

## Features

| Feature | Description | Benefits |
|---------|-------------|----------|
| Compliance Checking | Track requirements across frameworks, evaluate evidence, score compliance status | Automated compliance tracking with clear status indicators |
| Audit Trail | Immutable logging with query, filter, and export capabilities for audit readiness | Complete audit history for regulatory examinations |
| Privacy Management | Data subject registration, consent tracking, GDPR request handling | Streamlined privacy operations with automated workflows |
| Security Auditing | Vulnerability tracking with severity, CVSS scoring, and remediation plans | Centralized security finding management and tracking |
| Risk Assessment | Likelihood x Impact scoring with risk matrices and mitigation tracking | Proactive risk management with quantified risk scores |
| Policy Management | Policy creation, approval workflows, version control, and lifecycle management | Consistent policy enforcement with clear accountability |
| Reporting and Analytics | Real-time dashboards, compliance reports, and trend analysis | Data-driven compliance decisions with actionable insights |
| Framework Mapping | Cross-framework control mapping and requirement alignment | Reduced duplication and improved compliance efficiency |
| Automated Monitoring | Continuous compliance monitoring with alerting and notifications | Early detection of compliance drift and issues |
| Integration APIs | RESTful APIs for external system integration and data exchange | Seamless integration with existing compliance tools |
| Multi-tenant Support | Organization-level isolation with role-based access control | Scalable compliance management for multiple business units |
| Evidence Management | Centralized evidence repository with versioning and access controls | Organized evidence collection for audit examinations |

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
│       │            │            │            │             │
│  ┌────┴────────────┴────────────┴────────────┴────┐     │
│  │              Core Services Layer                │     │
│  │  • Event Bus    • Configuration Manager         │     │
│  │  • Validation   • Notification Service          │     │
│  │  • Caching      • Audit Trail Service           │     │
│  └────────────────────────────────────────────────────┘     │
│       │            │            │            │             │
│  ┌────┴────────────┴────────────┴────────────┴────┐     │
│  │              Data Persistence Layer             │     │
│  │  • SQLite/PostgreSQL   • File-based Storage     │     │
│  │  • Encryption at Rest  • Backup Management      │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

**Component Responsibilities:**
- **Compliance Checker**: Evaluates requirements against evidence, calculates compliance scores
- **Audit Logger**: Records all system activities with immutable logging
- **Privacy Manager**: Handles data subject requests and consent management
- **Security Auditor**: Tracks vulnerabilities and manages remediation workflows
- **Risk Assessor**: Performs risk assessments with quantified scoring matrices
- **Policy Manager**: Manages policy lifecycle from creation to archival
- **Report Generator**: Creates compliance reports and analytics dashboards

## Prerequisites

Before using the Compliance Agent, ensure you have the following:

**System Requirements:**
- Python 3.8 or higher
- SQLite 3.25+ (default) or PostgreSQL 12+ (for production)
- Minimum 2GB RAM for standard operations
- 10GB+ storage for audit logs and evidence

**Python Dependencies:**
```bash
pip install -r requirements.txt
```

Core dependencies include:
- `pydantic` for data validation
- `sqlalchemy` for database operations
- `cryptography` for encryption
- `jinja2` for report templating
- `pandas` for data analysis
- `celery` for background tasks (optional)

**Environment Setup:**
```bash
# Clone the repository
git clone https://github.com/your-org/compliance-agent.git
cd compliance-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings
```

**Database Setup:**
```bash
# Initialize database
python -m compliance_agent.db.init

# Run migrations
python -m compliance_agent.db.migrate

# Seed sample data (optional)
python -m compliance_agent.db.seed
```

**Access Requirements:**
- Administrative access for initial setup
- API keys for external integrations (if needed)
- Compliance framework documentation for custom controls
- Evidence repository access for compliance checking

## Quick Start

### Basic Setup

```python
from agents.compliance.agent import ComplianceAgent

# Initialize with default configuration
agent = ComplianceAgent()

# Or with custom configuration
config = {
    "frameworks": ["gdpr", "hipaa", "soc2"],
    "database_url": "sqlite:///compliance.db",
    "audit_retention_days": 365,
    "enable_notifications": True,
}
agent = ComplianceAgent(config)
```

### First Compliance Check

```python
# Add a GDPR requirement
requirement = agent.add_requirement(
    framework="gdpr",
    control_id="GDPR-001",
    requirement="Data Consent Management",
    description="Obtain explicit consent before processing personal data",
    severity="high",
    owner="DPO"
)

# Provide evidence
evidence = {
    "consent_form_url": "https://example.com/consent",
    "consent_timestamp": "2024-01-15T10:30:00Z",
    "consent_records": 1500,
    "opt_out_mechanism": True
}

# Check compliance
result = agent.check_compliance(requirement["id"], evidence)
print(f"Status: {result['status']}")
print(f"Score: {result['score']}%")
print(f"Issues: {result.get('issues', [])}")
```

### Generate Compliance Report

```python
# Generate comprehensive report
report = agent.generate_compliance_report("gdpr")

print(f"Overall Score: {report['compliance_score']}%")
print(f"Compliant Requirements: {report['compliant_count']}")
print(f"Non-compliant Requirements: {report['non_compliant_count']}")
print(f"Recommendations: {len(report['recommendations'])}")

# Export to different formats
agent.export_report(report, format="pdf", filename="gdpr_report.pdf")
agent.export_report(report, format="json", filename="gdpr_report.json")
agent.export_report(report, format="csv", filename="gdpr_report.csv")
```

## Usage

### Compliance Checking

The compliance checking module provides comprehensive requirement tracking and evidence evaluation.

#### Adding Requirements

```python
# Add multiple requirements for different frameworks
gdpr_req = agent.add_requirement(
    framework="gdpr",
    control_id="GDPR-001",
    requirement="Lawful Basis for Processing",
    description="Document lawful basis for each processing activity",
    severity="critical",
    owner="Legal Team",
    due_date="2024-03-01",
    tags=["legal", "data-processing"]
)

hipaa_req = agent.add_requirement(
    framework="hipaa",
    control_id="HIPAA-164.312",
    requirement="Access Control",
    description="Implement access controls for electronic PHI",
    severity="high",
    owner="Security Team",
    due_date="2024-06-30"
)

soc2_req = agent.add_requirement(
    framework="soc2",
    control_id="CC6.1",
    requirement="Logical Access Controls",
    description="Implement logical access security software, infrastructure, and architectures",
    severity="high",
    owner="IT Security",
    custom_fields={"audit_frequency": "quarterly"}
)
```

#### Evaluating Evidence

```python
# Check compliance with evidence
evidence_data = {
    "policy_url": "https://company.com/privacy-policy",
    "processing_records": 25,
    "consent_mechanism": "explicit",
    "retention_period": "24_months",
    "third_party_processors": ["AWS", "Google Cloud"],
    "data_protection_impact_assessment": True
}

result = agent.check_compliance(
    requirement_id=gdpr_req["id"],
    evidence=evidence_data,
    evaluator="default",  # or custom evaluator name
    notes="Evidence collected during Q1 audit"
)

# Analyze result
if result["status"] == "compliant":
    print("Requirement is compliant!")
elif result["status"] == "partially_compliant":
    print(f"Partially compliant: {result['gaps']}")
else:
    print(f"Non-compliant: {result['issues']}")
    print(f"Remediation: {result['remediation_steps']}")
```

#### Compliance Scoring

```python
# Get detailed scoring breakdown
scoring = agent.get_compliance_scoring("gdpr")

print(f"Overall Score: {scoring['overall_score']}%")
print("Breakdown by category:")
for category, score in scoring['category_scores'].items():
    print(f"  {category}: {score}%")

# Get trend analysis
trends = agent.get_compliance_trends("gdpr", months=12)
for month_data in trends:
    print(f"{month_data['month']}: {month_data['score']}%")
```

### Audit Trail

The audit trail system provides immutable logging of all system activities.

#### Logging Events

```python
# Log various types of events
agent.log_audit_event(
    action="CREATE",
    actor="admin@company.com",
    resource="requirement:GDPR-001",
    details={
        "framework": "gdpr",
        "control_id": "GDPR-001",
        "description": "Added new data consent requirement"
    },
    severity="info",
    category="compliance"
)

agent.log_audit_event(
    action="ACCESS",
    actor="user@company.com",
    resource="document:privacy-policy-v2",
    details={
        "ip_address": "192.168.1.100",
        "user_agent": "Mozilla/5.0",
        "access_type": "read"
    },
    severity="info",
    category="access"
)

agent.log_audit_event(
    action="UPDATE",
    actor="dpo@company.com",
    resource="consent:subject-123",
    details={
        "field": "marketing_consent",
        "old_value": False,
        "new_value": True,
        "reason": "User opted in via email"
    },
    severity="info",
    category="privacy"
)
```

#### Querying Logs

```python
# Query logs with various filters
admin_logs = agent.query_audit_logs(
    actor="admin@company.com",
    start_date="2024-01-01",
    end_date="2024-12-31"
)

delete_logs = agent.query_audit_logs(
    action="DELETE",
    resource_type="user",
    severity="warning"
)

security_logs = agent.query_audit_logs(
    category="security",
    limit=100,
    order_by="timestamp",
    order="desc"
)

# Complex queries
critical_events = agent.query_audit_logs(
    filters={
        "severity": ["critical", "high"],
        "category": ["security", "compliance"],
        "actor_domain": "company.com"
    }
)
```

#### Exporting Audit Data

```python
# Export for compliance audits
export_data = agent.export_audit_logs(
    start_date="2024-01-01",
    end_date="2024-12-31",
    format="json",
    include_metadata=True
)

# Generate audit report
audit_report = agent.generate_audit_report(
    period="2024-Q4",
    include_statistics=True,
    include_anomalies=True
)

# Save to file
with open("audit_export.json", "w") as f:
    json.dump(export_data, f, indent=2)
```

### Privacy Management

The privacy management module handles GDPR/CCPA data subject requests and consent management.

#### Registering Data Subjects

```python
# Register new data subject
subject = agent.register_data_subject(
    email="john.doe@example.com",
    name="John Doe",
    data_categories=["personal", "behavioral", "transactional"],
    processing_purposes=["marketing", "analytics", "service_delivery"],
    lawful_basis="consent",
    retention_period="36_months",
    source="website_registration",
    additional_data={
        "phone": "+1-555-0123",
        "location": "San Francisco, CA",
        "customer_id": "CUST-789"
    }
)

print(f"Subject ID: {subject['id']}")
print(f"Registration Date: {subject['created_at']}")
```

#### Managing Consent

```python
# Record consent grants
agent.record_consent(
    subject_id=subject["id"],
    purpose="marketing",
    granted=True,
    method="website_form",
    timestamp="2024-01-15T10:30:00Z",
    evidence_url="https://consent.example.com/records/123"
)

# Record consent withdrawals
agent.record_consent(
    subject_id=subject["id"],
    purpose="analytics",
    granted=False,
    method="email_request",
    timestamp="2024-02-20T14:45:00Z",
    reason="User preference change"
)

# Get consent summary
consent_summary = agent.get_consent_summary(subject["id"])
print(f"Active consents: {consent_summary['active_count']}")
print(f"Withdrawn consents: {consent_summary['withdrawn_count']}")
```

#### Handling GDPR Requests

```python
# Access request (Right of Access)
access_result = agent.handle_data_request(
    subject_id=subject["id"],
    request_type="access",
    details={
        "format": "json",
        "include_metadata": True,
        "delivery_method": "secure_email"
    }
)

# Deletion request (Right to Erasure)
deletion_result = agent.handle_data_request(
    subject_id=subject["id"],
    request_type="deletion",
    details={
        "reason": "User requested account deletion",
        "retain_legal": True,  # Retain data required by law
        "notify_partners": True
    }
)

# Portability request (Right to Data Portability)
portability_result = agent.handle_data_request(
    subject_id=subject["id"],
    request_type="portability",
    details={
        "format": "json",
        "include_metadata": True,
        "encoding": "utf-8"
    }
)

# Rectification request (Right to Rectification)
rectification_result = agent.handle_data_request(
    subject_id=subject["id"],
    request_type="rectification",
    details={
        "field": "email",
        "old_value": "john.doe@example.com",
        "new_value": "john.new@example.com",
        "evidence": "ID document provided"
    }
)
```

#### Privacy Reports

```python
# Generate privacy report
privacy_report = agent.get_privacy_report(
    period="2024-Q1",
    include_metrics=True,
    include_trends=True
)

print(f"Total data subjects: {privacy_report['total_subjects']}")
print(f"Consent rate: {privacy_report['consent_rate']}%")
print(f"Average request processing time: {privacy_report['avg_processing_days']} days")
print(f"Open requests: {privacy_report['open_requests']}")
```

### Security Auditing

The security auditing module tracks vulnerabilities and manages remediation workflows.

#### Running Security Scans

```python
# Run vulnerability scan
scan = agent.run_security_scan(
    target="api.example.com",
    scan_type="vulnerability",
    scan_profile="standard",
    include_dependencies=True,
    timeout_minutes=30
)

print(f"Scan ID: {scan['scan_id']}")
print(f"Status: {scan['status']}")
print(f"Duration: {scan['duration_seconds']} seconds")
print(f"Findings: {scan['findings_count']}")
```

#### Managing Security Findings

```python
# Add security findings
sql_injection = agent.add_security_finding(
    scan_id=scan["scan_id"],
    title="SQL Injection in User Search",
    severity="critical",
    cvss_score=9.8,
    description="Unvalidated input in user search endpoint allows SQL injection",
    affected_component="api.example.com/search",
    remediation="Use parameterized queries and input validation",
    references=[
        "https://owasp.org/www-community/attacks/SQL_Injection",
        "https://cwe.mitre.org/data/definitions/89.html"
    ],
    evidence={
        "request": "GET /api/users?search=' OR '1'='1",
        "response": "Database error message exposed",
        "screenshot_url": "https://evidence.example.com/sql-injection.png"
    }
)

xss_finding = agent.add_security_finding(
    scan_id=scan["scan_id"],
    title="Reflected XSS in Comment System",
    severity="high",
    cvss_score=7.5,
    description="User input reflected without sanitization in comment display",
    affected_component="api.example.com/comments",
    remediation="Implement Content Security Policy and input sanitization",
    status="new",
    assignee="security-team@company.com"
)
```

#### Tracking Remediation

```python
# Update finding status
agent.update_finding_status(
    finding_id=sql_injection["finding_id"],
    status="in_progress",
    assignee="dev-team@company.com",
    notes="Started implementing parameterized queries"
)

# Add remediation notes
agent.add_remediation_note(
    finding_id=sql_injection["finding_id"],
    note="Replaced string concatenation with SQLAlchemy ORM queries",
    author="developer@company.com",
    timestamp="2024-02-10T16:30:00Z"
)

# Verify remediation
agent.verify_remediation(
    finding_id=sql_injection["finding_id"],
    verified_by="security-team@company.com",
    verification_method="re-scan",
    notes="Re-scanned endpoint, vulnerability no longer present"
)
```

#### Security Reports

```python
# Generate security report
security_report = agent.get_security_report(
    period="2024-Q1",
    include_trends=True,
    include_remediation_metrics=True
)

print(f"Total findings: {security_report['total_findings']}")
print(f"Critical findings: {security_report['critical_count']}")
print(f"Remediated: {security_report['remediated_count']}")
print(f"Mean time to remediate: {security_report['mttr_days']} days")
print(f"Open findings: {security_report['open_count']}")
```

### Risk Assessment

The risk assessment module provides quantified risk evaluation with mitigation tracking.

#### Creating Risk Assessments

```python
# Create risk assessment
risk = agent.create_risk_assessment(
    asset="Customer Database",
    asset_owner="Data Team",
    threat="Unauthorized Access",
    vulnerability="Weak access controls",
    likelihood="high",
    impact="critical",
    risk_level="critical",
    existing_controls=["Firewall", "Basic authentication"],
    recommended_controls=[
        "Implement multi-factor authentication",
        "Deploy database activity monitoring",
        "Enable encryption at rest"
    ],
    mitigation_plan="Phase 1: Implement MFA (Q1), Phase 2: Deploy monitoring (Q2)",
    target_date="2024-06-30",
    review_frequency="quarterly"
)

# Create multiple risks
risks = [
    agent.create_risk_assessment(
        asset="Payment Processing System",
        threat="Data Breach",
        vulnerability="Outdated encryption",
        likelihood="medium",
        impact="critical",
        risk_level="high"
    ),
    agent.create_risk_assessment(
        asset="Employee Workstations",
        threat="Malware Infection",
        vulnerability="Missing endpoint protection",
        likelihood="high",
        impact="medium",
        risk_level="medium"
    )
]
```

#### Risk Analysis

```python
# Get risk summary
risk_summary = agent.get_risk_summary()
print(f"Critical risks: {risk_summary['critical_risks']}")
print(f"High risks: {risk_summary['high_risks']}")
print(f"Medium risks: {risk_summary['medium_risks']}")
print(f"Low risks: {risk_summary['low_risks']}")
print(f"Overall risk score: {risk_summary['overall_score']}")

# Get risk by category
risk_by_asset = agent.get_risks_by_asset("Customer Database")
for risk in risk_by_asset:
    print(f"{risk['threat']}: {risk['risk_level']}")

# Risk trend analysis
risk_trends = agent.get_risk_trends(months=12)
for month in risk_trends:
    print(f"{month['month']}: {month['critical_count']} critical, {month['high_count']} high")
```

#### Mitigation Tracking

```python
# Update mitigation status
agent.update_mitigation_status(
    risk_id=risk["risk_id"],
    mitigation_status="in_progress",
    progress_percentage=45,
    notes="MFA implementation 50% complete",
    updated_by="security-team@company.com"
)

# Add mitigation evidence
agent.add_mitigation_evidence(
    risk_id=risk["risk_id"],
    evidence_type="implementation",
    description="MFA deployed to 50% of users",
    evidence_url="https://jira.company.com/SEC-123",
    verified_by="security-team@company.com"
)

# Complete mitigation
agent.complete_mitigation(
    risk_id=risk["risk_id"],
    completion_date="2024-03-15",
    verification_method="penetration_test",
    residual_risk="low"
)
```

### Policy Management

The policy management module handles policy lifecycle from creation to archival.

#### Creating Policies

```python
# Create policy
policy = agent.create_policy(
    title="Data Protection Policy",
    framework="gdpr",
    content="""
# Data Protection Policy

## Purpose
This policy establishes guidelines for protecting personal data in accordance with GDPR requirements.

## Scope
Applies to all employees, contractors, and third parties processing personal data on behalf of the company.

## Responsibilities
- DPO: Overall policy ownership and compliance monitoring
- Department Heads: Implementation within their teams
- All Staff: Adherence to policy requirements

## Requirements
1. Lawful basis must be documented for all processing activities
2. Data subjects must be informed of processing purposes
3. Consent must be freely given, specific, informed, and unambiguous
4. Data minimization principles must be applied
5. Retention periods must be defined and enforced

## Enforcement
Violations may result in disciplinary action up to and including termination.
""",
    owner="DPO",
    version="1.0",
    effective_date="2024-01-01",
    review_date="2025-01-01",
    tags=["gdpr", "data-protection", "privacy"],
    required_acknowledgments=True,
    acknowledgment_deadline="2024-02-01"
)

# Create policy with approval workflow
security_policy = agent.create_policy(
    title="Information Security Policy",
    framework="iso27001",
    content="...",
    owner="CISO",
    approval_workflow={
        "approvers": ["ciso@company.com", "cto@company.com"],
        "required_approvals": 2,
        "auto_approve_after_days": 30
    }
)
```

#### Approving Policies

```python
# Approve policy
approval = agent.approve_policy(
    policy_id=policy["id"],
    approved_by="CISO",
    comments="Policy aligns with GDPR requirements and company standards",
    conditions=["Annual review required", "Training mandatory for all staff"]
)

# Reject policy with feedback
agent.approve_policy(
    policy_id=security_policy["id"],
    approved_by="CTO",
    decision="rejected",
    comments="Needs additional technical controls section",
    return_for_revision=True
)

# Track approval status
approval_status = agent.get_policy_approval_status(policy["id"])
print(f"Status: {approval_status['status']}")
print(f"Approvals: {approval_status['approval_count']}/{approval_status['required_approvals']}")
```

#### Policy Lifecycle

```python
# Get policy summary
policy_summary = agent.get_policy_summary()
print(f"Total policies: {policy_summary['total_policies']}")
print(f"Active policies: {policy_summary['active_policies']}")
print(f"Pending approval: {policy_summary['pending_approval']}")
print(f"Due for review: {policy_summary['due_for_review']}")

# Archive policy
agent.archive_policy(
    policy_id=old_policy["id"],
    reason="Superseded by new version",
    archive_date="2024-01-01",
    retention_period="7_years"
)

# Get policy history
history = agent.get_policy_history(policy["id"])
for version in history:
    print(f"Version {version['version']}: {version['effective_date']} - {version['status']}")
```

### Reporting and Analytics

The reporting module provides comprehensive compliance analytics and dashboards.

#### Generating Reports

```python
# Compliance report
compliance_report = agent.generate_compliance_report(
    framework="gdpr",
    period="2024-Q1",
    include_evidence=True,
    include_recommendations=True,
    format="detailed"
)

# Audit report
audit_report = agent.generate_audit_report(
    period="2024-Q1",
    include_statistics=True,
    include_anomalies=True,
    include_trends=True
)

# Security report
security_report = agent.get_security_report(
    period="2024-Q1",
    include_trends=True,
    include_remediation_metrics=True
)

# Risk report
risk_report = agent.generate_risk_report(
    period="2024-Q1",
    include_mitigation_status=True,
    include_trends=True
)
```

#### Dashboard Data

```python
# Get dashboard data
dashboard = agent.get_dashboard_data()

print("Compliance Overview:")
print(f"  Overall Score: {dashboard['compliance']['overall_score']}%")
print(f"  Active Requirements: {dashboard['compliance']['active_count']}")

print("\nSecurity Overview:")
print(f"  Open Findings: {dashboard['security']['open_count']}")
print(f"  Critical: {dashboard['security']['critical_count']}")

print("\nRisk Overview:")
print(f"  Critical Risks: {dashboard['risks']['critical_count']}")
print(f"  Overall Risk Score: {dashboard['risks']['overall_score']}")

print("\nPrivacy Overview:")
print(f"  Open Requests: {dashboard['privacy']['open_requests']}")
print(f"  Consent Rate: {dashboard['privacy']['consent_rate']}%")
```

### Integration with External Systems

#### Webhook Integration

```python
# Configure webhooks
agent.configure_webhook(
    name="slack-notifications",
    url="https://hooks.slack.com/services/xxx",
    events=["compliance.score_changed", "security.finding_critical"],
    headers={"Content-Type": "application/json"}
)

# Manual webhook trigger
agent.trigger_webhook(
    webhook_name="slack-notifications",
    event="compliance.alert",
    payload={
        "message": "Compliance score dropped below threshold",
        "score": 65,
        "threshold": 80,
        "framework": "gdpr"
    }
)
```

#### API Integration

```python
# REST API endpoints available
# GET /api/v1/compliance/score?framework=gdpr
# GET /api/v1/security/findings?severity=critical
# GET /api/v1/risks?status=open
# POST /api/v1/requirements (add new requirement)
# POST /api/v1/evidence (upload evidence)

# Example API call
import requests

response = requests.get(
    "https://compliance-api.example.com/api/v1/compliance/score",
    params={"framework": "gdpr"},
    headers={"Authorization": "Bearer YOUR_API_TOKEN"}
)

data = response.json()
print(f"GDPR Score: {data['score']}%")
```

#### SIEM Integration

```python
# Configure SIEM integration
agent.configure_siem(
    type="splunk",
    host="splunk.company.com",
    port="8088",
    token="your-hec-token",
    index="compliance",
    sourcetype="compliance:events"
)

# Send events to SIEM
agent.send_to_siem(
    event_type="compliance_change",
    data={
        "requirement_id": "GDPR-001",
        "status_change": "non_compliant to compliant",
        "score_change": 65,
        "timestamp": "2024-01-15T10:30:00Z"
    }
)
```

## API Reference

### ComplianceAgent Methods

#### Requirement Management

```python
def add_requirement(
    self,
    framework: str,
    control_id: str,
    requirement: str,
    description: str = "",
    severity: str = "medium",
    owner: str = "",
    due_date: str = None,
    tags: List[str] = None,
    custom_fields: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Add a new compliance requirement."""
    pass

def update_requirement(
    self,
    requirement_id: str,
    updates: Dict[str, Any]
) -> Dict[str, Any]:
    """Update an existing requirement."""
    pass

def delete_requirement(
    self,
    requirement_id: str,
    reason: str = ""
) -> bool:
    """Delete a requirement (soft delete)."""
    pass

def get_requirement(
    self,
    requirement_id: str
) -> Dict[str, Any]:
    """Get requirement details."""
    pass

def list_requirements(
    self,
    framework: str = None,
    severity: str = None,
    status: str = None,
    owner: str = None,
    tags: List[str] = None,
    limit: int = 100,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """List requirements with filters."""
    pass
```

#### Compliance Checking

```python
def check_compliance(
    self,
    requirement_id: str,
    evidence: Dict[str, Any],
    evaluator: str = "default",
    notes: str = ""
) -> Dict[str, Any]:
    """Check compliance for a requirement with evidence."""
    pass

def batch_check_compliance(
    self,
    checks: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Check compliance for multiple requirements."""
    pass

def get_compliance_scoring(
    self,
    framework: str
) -> Dict[str, Any]:
    """Get detailed compliance scoring breakdown."""
    pass

def get_compliance_trends(
    self,
    framework: str,
    months: int = 12
) -> List[Dict[str, Any]]:
    """Get compliance score trends over time."""
    pass
```

#### Audit Trail

```python
def log_audit_event(
    self,
    action: str,
    actor: str,
    resource: str,
    details: Dict[str, Any] = None,
    severity: str = "info",
    category: str = "general"
) -> Dict[str, Any]:
    """Log an audit event."""
    pass

def query_audit_logs(
    self,
    actor: str = None,
    action: str = None,
    resource: str = None,
    resource_type: str = None,
    category: str = None,
    severity: str = None,
    start_date: str = None,
    end_date: str = None,
    filters: Dict[str, Any] = None,
    limit: int = 1000,
    offset: int = 0,
    order_by: str = "timestamp",
    order: str = "desc"
) -> List[Dict[str, Any]]:
    """Query audit logs with filters."""
    pass

def export_audit_logs(
    self,
    start_date: str,
    end_date: str,
    format: str = "json",
    include_metadata: bool = True
) -> Dict[str, Any]:
    """Export audit logs for compliance."""
    pass

def generate_audit_report(
    self,
    period: str,
    include_statistics: bool = True,
    include_anomalies: bool = True,
    include_trends: bool = True
) -> Dict[str, Any]:
    """Generate audit report."""
    pass
```

#### Privacy Management

```python
def register_data_subject(
    self,
    email: str,
    name: str,
    data_categories: List[str],
    processing_purposes: List[str] = None,
    lawful_basis: str = "consent",
    retention_period: str = None,
    source: str = "",
    additional_data: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Register a new data subject."""
    pass

def record_consent(
    self,
    subject_id: str,
    purpose: str,
    granted: bool,
    method: str = "",
    timestamp: str = None,
    evidence_url: str = ""
) -> Dict[str, Any]:
    """Record consent grant or withdrawal."""
    pass

def handle_data_request(
    self,
    subject_id: str,
    request_type: str,
    details: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Handle GDPR data subject request."""
    pass

def get_privacy_report(
    self,
    period: str = None,
    include_metrics: bool = True,
    include_trends: bool = True
) -> Dict[str, Any]:
    """Generate privacy report."""
    pass

def get_consent_summary(
    self,
    subject_id: str
) -> Dict[str, Any]:
    """Get consent summary for a data subject."""
    pass
```

#### Security Auditing

```python
def run_security_scan(
    self,
    target: str,
    scan_type: str = "vulnerability",
    scan_profile: str = "standard",
    include_dependencies: bool = True,
    timeout_minutes: int = 30
) -> Dict[str, Any]:
    """Run security scan on target."""
    pass

def add_security_finding(
    self,
    scan_id: str,
    title: str,
    severity: str,
    cvss_score: float = None,
    description: str = "",
    affected_component: str = "",
    remediation: str = "",
    references: List[str] = None,
    evidence: Dict[str, Any] = None,
    status: str = "new",
    assignee: str = ""
) -> Dict[str, Any]:
    """Add security finding."""
    pass

def update_finding_status(
    self,
    finding_id: str,
    status: str,
    assignee: str = "",
    notes: str = ""
) -> Dict[str, Any]:
    """Update security finding status."""
    pass

def get_security_report(
    self,
    period: str = None,
    include_trends: bool = True,
    include_remediation_metrics: bool = True
) -> Dict[str, Any]:
    """Generate security report."""
    pass
```

#### Risk Assessment

```python
def create_risk_assessment(
    self,
    asset: str,
    threat: str,
    vulnerability: str,
    likelihood: str,
    impact: str,
    risk_level: str = None,
    asset_owner: str = "",
    existing_controls: List[str] = None,
    recommended_controls: List[str] = None,
    mitigation_plan: str = "",
    target_date: str = None,
    review_frequency: str = "quarterly"
) -> Dict[str, Any]:
    """Create risk assessment."""
    pass

def get_risk_summary(self) -> Dict[str, Any]:
    """Get risk summary."""
    pass

def update_mitigation_status(
    self,
    risk_id: str,
    mitigation_status: str,
    progress_percentage: int = None,
    notes: str = "",
    updated_by: str = ""
) -> Dict[str, Any]:
    """Update mitigation status."""
    pass

def generate_risk_report(
    self,
    period: str = None,
    include_mitigation_status: bool = True,
    include_trends: bool = True
) -> Dict[str, Any]:
    """Generate risk report."""
    pass
```

#### Policy Management

```python
def create_policy(
    self,
    title: str,
    framework: str,
    content: str,
    owner: str,
    version: str = "1.0",
    effective_date: str = None,
    review_date: str = None,
    tags: List[str] = None,
    required_acknowledgments: bool = False,
    acknowledgment_deadline: str = None,
    approval_workflow: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Create new policy."""
    pass

def approve_policy(
    self,
    policy_id: str,
    approved_by: str,
    decision: str = "approved",
    comments: str = "",
    conditions: List[str] = None,
    return_for_revision: bool = False
) -> Dict[str, Any]:
    """Approve or reject policy."""
    pass

def get_policy_summary(self) -> Dict[str, Any]:
    """Get policy summary."""
    pass

def archive_policy(
    self,
    policy_id: str,
    reason: str = "",
    archive_date: str = None,
    retention_period: str = "7_years"
) -> bool:
    """Archive policy."""
    pass
```

### Helper Classes

#### AuditLogger

```python
class AuditLogger:
    def __init__(self, db_connection: Any, config: Dict[str, Any]):
        """Initialize audit logger."""
        pass
    
    def log(
        self,
        action: str,
        actor: str,
        resource: str,
        details: Dict[str, Any] = None,
        severity: str = "info",
        category: str = "general"
    ) -> AuditLogEntry:
        """Log audit event."""
        pass
    
    def query(
        self,
        filters: Dict[str, Any] = None,
        limit: int = 1000
    ) -> List[AuditLogEntry]:
        """Query audit logs."""
        pass
    
    def export_for_compliance(
        self,
        start_date: str,
        end_date: str,
        format: str = "json"
    ) -> Dict[str, Any]:
        """Export logs for compliance audit."""
        pass
```

#### PrivacyManager

```python
class PrivacyManager:
    def __init__(self, db_connection: Any, config: Dict[str, Any]):
        """Initialize privacy manager."""
        pass
    
    def register_subject(
        self,
        email: str,
        name: str,
        data_categories: List[str]
    ) -> DataSubject:
        """Register data subject."""
        pass
    
    def handle_request(
        self,
        subject_id: str,
        request_type: str,
        details: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Handle data subject request."""
        pass
    
    def get_consent_status(
        self,
        subject_id: str
    ) -> Dict[str, Any]:
        """Get consent status."""
        pass
```

#### SecurityAuditor

```python
class SecurityAuditor:
    def __init__(self, db_connection: Any, config: Dict[str, Any]):
        """Initialize security auditor."""
        pass
    
    def run_scan(
        self,
        target: str,
        scan_type: str = "vulnerability"
    ) -> Dict[str, Any]:
        """Run security scan."""
        pass
    
    def add_finding(
        self,
        scan_id: str,
        title: str,
        severity: str,
        cvss_score: float = None
    ) -> SecurityFinding:
        """Add security finding."""
        pass
    
    def update_finding_status(
        self,
        finding_id: str,
        status: str,
        notes: str = ""
    ) -> SecurityFinding:
        """Update finding status."""
        pass
```

## Compliance Frameworks

### Framework Details

| Framework | Focus Area | Key Controls | Audit Frequency | Certification |
|-----------|-----------|--------------|-----------------|---------------|
| GDPR | EU data protection | Consent, data rights, breach notification | Annual | Self-assessment |
| HIPAA | Health data privacy | Access controls, audit trails, encryption | Annual | Third-party audit |
| SOC 2 | Service organization controls | Security, availability, confidentiality | Annual | Type I/II audit |
| PCI DSS | Payment card data | Network security, access control, monitoring | Quarterly | QSA assessment |
| ISO 27001 | Information security | Risk management, controls, continuous improvement | Annual | Certification body |
| CCPA | California consumer privacy | Consumer rights, data disclosure, opt-out | Annual | Self-assessment |
| SOX | Financial reporting | Internal controls, audit trails | Annual | External audit |
| NIST 800-53 | Federal information security | Security controls, privacy controls | Continuous | FedRAMP assessment |

### Mapping Controls

```python
# Map controls across frameworks
mapping = agent.map_controls(
    source_framework="gdpr",
    target_framework="iso27001",
    control_ids=["GDPR-001", "GDPR-002", "GDPR-003"]
)

for control in mapping:
    print(f"GDPR {control['source_control']} → ISO {control['target_control']}")
    print(f"  Description: {control['description']}")
    print(f"  Gap: {control.get('gap_analysis', 'None')}")

# Get framework coverage
coverage = agent.get_framework_coverage("gdpr")
print(f"Total controls: {coverage['total_controls']}")
print(f"Mapped controls: {coverage['mapped_controls']}")
print(f"Unmapped controls: {coverage['unmapped_controls']}")
```

## Data Models

### ComplianceRequirement

```python
class ComplianceRequirement:
    id: str                          # Unique identifier
    framework: str                   # Framework identifier (gdpr, hipaa, etc.)
    control_id: str                  # Control ID (GDPR-001, HIPAA-164.312)
    requirement: str                 # Requirement name
    description: str                 # Detailed description
    severity: str                    # critical, high, medium, low
    status: str                      # compliant, non_compliant, partially_compliant, not_assessed
    owner: str                       # Responsible person/team
    due_date: Optional[str]          # Due date for compliance
    created_at: str                  # Creation timestamp
    updated_at: str                  # Last update timestamp
    evidence: Dict[str, Any]         # Evidence provided
    assessment_history: List[Dict]   # History of assessments
    tags: List[str]                  # Categorization tags
    custom_fields: Dict[str, Any]    # Custom metadata
```

### AuditLogEntry

```python
class AuditLogEntry:
    id: str                          # Unique identifier
    timestamp: str                   # Event timestamp (ISO 8601)
    action: str                      # Action performed (CREATE, READ, UPDATE, DELETE)
    actor: str                       # User/system performing action
    resource: str                    # Resource affected
    resource_type: str               # Type of resource
    details: Dict[str, Any]          # Additional details
    severity: str                    # info, warning, error, critical
    category: str                    # Category (compliance, security, privacy)
    ip_address: Optional[str]        # IP address of actor
    user_agent: Optional[str]        # User agent string
    session_id: Optional[str]        # Session identifier
    immutable: bool                  # Cannot be modified
```

### DataSubject

```python
class DataSubject:
    id: str                          # Unique identifier
    email: str                       # Email address
    name: str                        # Full name
    data_categories: List[str]       # Categories of data held
    processing_purposes: List[str]   # Purposes for processing
    lawful_basis: str                # Legal basis for processing
    consent_records: List[Dict]      # Consent history
    retention_period: str            # Data retention period
    source: str                      # How data was collected
    registration_date: str           # When subject was registered
    last_updated: str                # Last update timestamp
    additional_data: Dict[str, Any]  # Additional metadata
    requests: List[Dict]             # Data subject requests
```

### SecurityFinding

```python
class SecurityFinding:
    finding_id: str                  # Unique identifier
    scan_id: str                     # Associated scan ID
    title: str                       # Finding title
    severity: str                    # critical, high, medium, low, informational
    cvss_score: Optional[float]      # CVSS score (0-10)
    description: str                 # Detailed description
    affected_component: str          # Component affected
    remediation: str                 # Remediation steps
    status: str                      # new, in_progress, remediated, verified, false_positive
    assignee: str                    # Assigned to
    references: List[str]            # External references
    evidence: Dict[str, Any]         # Evidence of finding
    created_at: str                  # Creation timestamp
    updated_at: str                  # Last update timestamp
    remediation_history: List[Dict]  # Remediation history
```

### RiskAssessment

```python
class RiskAssessment:
    risk_id: str                     # Unique identifier
    asset: str                       # Asset at risk
    asset_owner: str                 # Asset owner
    threat: str                      # Threat description
    vulnerability: str               # Vulnerability description
    likelihood: str                  # low, medium, high, very_high
    impact: str                      # low, medium, high, critical
    risk_level: str                  # low, medium, high, critical
    existing_controls: List[str]     # Current controls
    recommended_controls: List[str]  # Recommended controls
    mitigation_plan: str             # Mitigation plan
    mitigation_status: str           # not_started, in_progress, completed
    target_date: Optional[str]       # Target completion date
    review_frequency: str            # Review frequency
    created_at: str                  # Creation timestamp
    updated_at: str                  # Last update timestamp
    residual_risk: Optional[str]     # Risk after mitigation
```

### Policy

```python
class Policy:
    id: str                          # Unique identifier
    title: str                       # Policy title
    framework: str                   # Associated framework
    content: str                     # Policy content (Markdown)
    owner: str                       # Policy owner
    version: str                     # Version number
    status: str                      # draft, pending_approval, approved, archived
    effective_date: Optional[str]    # When policy takes effect
    review_date: Optional[str]       # Next review date
    tags: List[str]                  # Categorization tags
    approval_workflow: Dict          # Approval workflow config
    approvals: List[Dict]            # Approval history
    acknowledgments: List[Dict]      # Acknowledgment tracking
    created_at: str                  # Creation timestamp
    updated_at: str                  # Last update timestamp
    archived_at: Optional[str]       # Archive timestamp
```

## Configuration

### Basic Configuration

```python
config = {
    # Database configuration
    "database_url": "sqlite:///compliance.db",
    "database_echo": False,
    
    # Framework configuration
    "frameworks": ["gdpr", "hipaa", "soc2", "pci_dss", "iso27001"],
    "default_framework": "gdpr",
    
    # Compliance settings
    "default_severity": "high",
    "compliance_threshold": 80,  # Percentage for compliance
    "require_evidence": True,
    
    # Audit settings
    "audit_retention_days": 365,
    "audit_immutable": True,
    "audit_categories": ["compliance", "security", "privacy", "access"],
    
    # Privacy settings
    "data_retention_days": 730,
    "consent_expiry_days": 365,
    "request_processing_days": 30,
    
    # Security settings
    "security_scan_timeout": 1800,
    "cvss_threshold": 7.0,
    "auto_assign_findings": True,
    
    # Risk settings
    "risk_review_frequency": "quarterly",
    "risk_matrix_size": "5x5",
    
    # Notification settings
    "enable_notifications": True,
    "notification_channels": ["email", "slack"],
    "alert_thresholds": {
        "compliance_score": 70,
        "critical_findings": 1,
        "high_risks": 5
    }
}

agent = ComplianceAgent(config)
```

### Advanced Configuration

```python
advanced_config = {
    # Encryption settings
    "encryption_enabled": True,
    "encryption_key": "your-encryption-key",
    "encryption_algorithm": "AES-256-GCM",
    
    # Backup settings
    "backup_enabled": True,
    "backup_frequency": "daily",
    "backup_retention_days": 90,
    "backup_location": "/backups/compliance",
    
    # Integration settings
    "integrations": {
        "siem": {
            "enabled": True,
            "type": "splunk",
            "host": "splunk.company.com",
            "token": "your-hec-token"
        },
        "jira": {
            "enabled": True,
            "host": "jira.company.com",
            "project": "SEC"
        },
        "slack": {
            "enabled": True,
            "webhook_url": "https://hooks.slack.com/services/xxx"
        }
    },
    
    # Performance settings
    "cache_enabled": True,
    "cache_ttl": 300,
    "max_concurrent_scans": 5,
    "batch_size": 100,
    
    # Logging settings
    "log_level": "INFO",
    "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "log_file": "/var/log/compliance-agent.log",
    
    # Custom fields
    "custom_fields": {
        "compliance": ["audit_frequency", "control_owner", "review_cycle"],
        "risk": ["business_unit", "cost_center", "project_code"],
        "policy": ["department", "applicable_roles", "training_required"]
    }
}
```

### Environment Variables

```bash
# Database
COMPLIANCE_DB_URL=postgresql://user:pass@localhost/compliance
COMPLIANCE_DB_ECHO=false

# Encryption
COMPLIANCE_ENCRYPTION_KEY=your-encryption-key
COMPLIANCE_ENCRYPTION_ENABLED=true

# Notifications
COMPLIANCE_SLACK_WEBHOOK=https://hooks.slack.com/services/xxx
COMPLIANCE_EMAIL_SMTP=smtp.company.com
COMPLIANCE_EMAIL_FROM=compliance@company.com

# Integration
COMPLIANCE_SPLUNK_HOST=splunk.company.com
COMPLIANCE_SPLUNK_TOKEN=your-hec-token
COMPLIANCE_JIRA_HOST=jira.company.com

# Security
COMPLIANCE_API_KEY=your-api-key
COMPLIANCE_SECRET_KEY=your-secret-key

# Logging
COMPLIANCE_LOG_LEVEL=INFO
COMPLIANCE_LOG_FILE=/var/log/compliance-agent.log
```

## Extending the Agent

### Adding New Frameworks

```python
# Define custom framework
custom_framework = {
    "name": "custom_security",
    "display_name": "Custom Security Framework",
    "description": "Internal security requirements",
    "version": "1.0",
    "controls": [
        {
            "id": "CS-001",
            "name": "Access Control",
            "description": "Implement role-based access control",
            "severity": "high",
            "evaluation_criteria": {
                "min_score": 80,
                "required_evidence": ["access_matrix", "role_definitions"]
            }
        },
        {
            "id": "CS-002",
            "name": "Data Encryption",
            "description": "Encrypt sensitive data at rest and in transit",
            "severity": "critical",
            "evaluation_criteria": {
                "min_score": 90,
                "required_evidence": ["encryption_config", "certificate_info"]
            }
        }
    ],
    "evaluation_logic": "weighted_average",
    "weights": {
        "CS-001": 0.4,
        "CS-002": 0.6
    }
}

# Register framework
agent.register_framework(custom_framework)

# Add requirements
agent.add_requirement(
    framework="custom_security",
    control_id="CS-001",
    requirement="Role-Based Access Control",
    severity="high"
)
```

### Custom Evidence Evaluators

```python
from compliance_agent.evaluators import BaseEvaluator

class CustomEvaluator(BaseEvaluator):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.custom_threshold = config.get("threshold", 80)
    
    def evaluate(
        self,
        requirement: Dict[str, Any],
        evidence: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Custom evaluation logic."""
        score = 0
        issues = []
        
        # Custom evaluation logic
        if evidence.get("has_documentation"):
            score += 30
        else:
            issues.append("Missing documentation")
        
        if evidence.get("has_implementation"):
            score += 40
        else:
            issues.append("Implementation not verified")
        
        if evidence.get("has_testing"):
            score += 30
        else:
            issues.append("Testing evidence missing")
        
        # Determine status
        if score >= self.custom_threshold:
            status = "compliant"
        elif score >= self.custom_threshold - 20:
            status = "partially_compliant"
        else:
            status = "non_compliant"
        
        return {
            "status": status,
            "score": score,
            "issues": issues,
            "recommendations": self._generate_recommendations(issues)
        }
    
    def _generate_recommendations(self, issues: List[str]) -> List[str]:
        """Generate recommendations based on issues."""
        recommendations = []
        for issue in issues:
            if "documentation" in issue:
                recommendations.append("Create comprehensive documentation")
            elif "implementation" in issue:
                recommendations.append("Complete implementation and verify")
            elif "testing" in issue:
                recommendations.append("Conduct thorough testing and document results")
        return recommendations

# Register custom evaluator
agent.register_evaluator("custom", CustomEvaluator)
```

### Plugins and Hooks

```python
from compliance_agent.plugins import BasePlugin

class NotificationPlugin(BasePlugin):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.webhook_url = config["webhook_url"]
    
    def on_compliance_change(self, event: Dict[str, Any]):
        """Handle compliance score changes."""
        if event["new_score"] < event["threshold"]:
            self.send_notification(
                title="Compliance Alert",
                message=f"Score dropped to {event['new_score']}%",
                severity="warning"
            )
    
    def on_critical_finding(self, event: Dict[str, Any]):
        """Handle critical security findings."""
        self.send_notification(
            title="Critical Finding",
            message=f"New critical finding: {event['title']}",
            severity="critical"
        )
    
    def send_notification(self, title: str, message: str, severity: str):
        """Send notification via webhook."""
        import requests
        payload = {
            "title": title,
            "message": message,
            "severity": severity,
            "timestamp": datetime.now().isoformat()
        }
        requests.post(self.webhook_url, json=payload)

# Register plugin
agent.register_plugin("notifications", NotificationPlugin({
    "webhook_url": "https://hooks.slack.com/services/xxx"
}))

# Hook into events
agent.on("compliance.score_changed", plugin.on_compliance_change)
agent.on("security.finding_critical", plugin.on_critical_finding)
```

## Best Practices

1. **Document Everything** — If it's not documented, it didn't happen. Maintain comprehensive evidence for all compliance activities.

2. **Review Regularly** — Schedule quarterly compliance reviews to ensure ongoing adherence to requirements and identify gaps early.

3. **Train Teams** — Ensure all teams understand compliance requirements relevant to their roles. Conduct regular training sessions.

4. **Automate Where Possible** — Use the agent for routine compliance checks, evidence collection, and reporting to reduce manual effort.

5. **Maintain Evidence** — Keep evidence current and accessible. Update evidence when changes occur and ensure it's properly versioned.

6. **Act on Findings** — Address non-compliance promptly. Create remediation plans with clear owners and timelines.

7. **Test Incident Response** — Practice breach notification procedures regularly. Conduct tabletop exercises and update procedures based on lessons learned.

8. **Implement Defense in Depth** — Don't rely on single controls. Implement multiple layers of security and compliance measures.

9. **Monitor Continuously** — Set up continuous monitoring for critical compliance areas. Use automated alerts for compliance drift.

10. **Keep Frameworks Updated** — Stay informed about changes to compliance frameworks. Update requirements and controls when frameworks are updated.

11. **Establish Clear Ownership** — Assign clear owners for all compliance requirements, policies, and controls. Ensure accountability.

12. **Use Risk-Based Approach** — Prioritize compliance efforts based on risk. Focus resources on high-risk areas first.

13. **Integrate with Workflows** — Embed compliance checks into existing workflows (CI/CD, procurement, HR) rather than treating them as separate activities.

14. **Conduct Regular Audits** — Perform internal audits to verify compliance. Use external auditors for independent assessment.

15. **Maintain Audit Trails** — Ensure all actions are logged with sufficient detail for audit purposes. Protect audit logs from tampering.

## Troubleshooting

| Problem | Solution | Prevention |
|---------|----------|------------|
| Compliance score low | Gather evidence for non-compliant requirements, run gap analysis | Regular evidence updates, automated monitoring |
| Audit logs missing | Add logging to all critical operations, check log configuration | Implement comprehensive logging from start |
| Privacy request failing | Verify data subject ID and registration, check request processing pipeline | Validate data subject registration, test request flows |
| Security findings stale | Schedule regular vulnerability scans, assign findings to owners | Automated scanning schedules, clear ownership |
| Risk assessments outdated | Review and update quarterly, assign risk owners | Calendar reminders, automated review triggers |
| Policy not approved | Route to appropriate approver, provide additional context | Clear approval workflows, escalation paths |
| Database connection errors | Check database URL, verify credentials, test connectivity | Connection pooling, health checks, monitoring |
| Performance issues | Optimize queries, add indexes, enable caching | Regular performance testing, capacity planning |
| Integration failures | Verify API credentials, check network connectivity, review logs | Integration testing, circuit breakers, monitoring |
| Backup failures | Check backup location permissions, verify storage space | Backup monitoring, multiple backup locations |
| Encryption errors | Verify encryption key, check algorithm compatibility | Key rotation schedule, encryption testing |
| Notification delays | Check notification service status, verify webhook URLs | Redundant notification channels, queue monitoring |
| Report generation slow | Optimize report queries, schedule during off-peak hours | Incremental reports, caching, background processing |
| Memory issues | Increase memory allocation, optimize data structures | Memory monitoring, profiling, cleanup routines |
| Version conflicts | Check dependency versions, update as needed | Version pinning, compatibility testing |

## FAQ

**Q: How do I add a new compliance framework?**
A: Use the `register_framework()` method with a framework definition. See [Adding New Frameworks](#adding-new-frameworks) for detailed instructions.

**Q: Can I customize the compliance scoring algorithm?**
A: Yes, you can create custom evaluators by extending `BaseEvaluator` and registering them with `register_evaluator()`. See [Custom Evidence Evaluators](#custom-evidence-evaluators).

**Q: How do I integrate with our existing SIEM system?**
A: Use the `configure_siem()` method to set up SIEM integration. The agent supports Splunk, Elastic, and custom SIEM systems via webhooks.

**Q: What happens if I lose encryption keys?**
A: Data encrypted with lost keys cannot be recovered. Ensure you have secure key backup procedures. Consider using a key management system (KMS).

**Q: Can I run multiple compliance checks simultaneously?**
A: Yes, the agent supports concurrent compliance checks. Use `batch_check_compliance()` for multiple checks or run checks in separate threads.

**Q: How do I handle data subject requests across multiple systems?**
A: The agent can integrate with external systems via APIs. Configure integrations in the settings and the agent will coordinate requests across systems.

**Q: What's the recommended database for production?**
A: PostgreSQL is recommended for production deployments. SQLite is suitable for development and small-scale deployments.

**Q: How do I backup compliance data?**
A: Enable backup configuration in settings. The agent supports automated backups to local storage or cloud storage (S3, GCS).

**Q: Can I export data for external auditors?**
A: Yes, use `export_audit_logs()` and `generate_compliance_report()` with appropriate date ranges and formats (JSON, CSV, PDF).

**Q: How do I update the agent without losing data?**
A: Use the migration system. Run `python -m compliance_agent.db.migrate` after updates. Always backup before major updates.

**Q: Can I customize the audit log retention period?**
A: Yes, set `audit_retention_days` in configuration. Logs older than the retention period are automatically archived.

**Q: How do I handle compliance for multiple business units?**
A: Use the multi-tenant features. Configure organization-level isolation and role-based access control for each business unit.

**Q: What's the difference between compliance and security auditing?**
A: Compliance checking verifies adherence to regulatory requirements. Security auditing identifies vulnerabilities and security issues. Both are complementary.

**Q: Can I schedule automatic compliance checks?**
A: Yes, use the scheduling features or integrate with external schedulers (cron, Airflow) to run compliance checks automatically.

**Q: How do I handle false positive security findings?**
A: Update finding status to "false_positive" with documentation explaining why it's a false positive. This maintains audit trail while excluding from reports.

## Examples

### Example 1: GDPR Compliance Check

```python
from agents.compliance.agent import ComplianceAgent

# Initialize agent
agent = ComplianceAgent({"frameworks": ["gdpr"]})

# Add GDPR requirements
requirements = [
    agent.add_requirement("gdpr", "GDPR-001", "Lawful Basis", severity="critical"),
    agent.add_requirement("gdpr", "GDPR-002", "Data Subject Rights", severity="high"),
    agent.add_requirement("gdpr", "GDPR-003", "Data Protection Officer", severity="medium"),
]

# Evidence for each requirement
evidence_map = {
    "GDPR-001": {
        "processing_activities": 25,
        "lawful_basis_documented": True,
        "consent_mechanism": "explicit",
        "legitimate_interest_assessment": True
    },
    "GDPR-002": {
        "access_request_process": True,
        "deletion_process": True,
        "portability_format": "json",
        "response_time_days": 30
    },
    "GDPR-003": {
        "dpo_appointed": True,
        "dpo_contact_published": True,
        "dpo_independence": True
    }
}

# Check compliance
results = []
for req in requirements:
    result = agent.check_compliance(
        req["id"],
        evidence_map[req["control_id"]]
    )
    results.append(result)
    print(f"{req['control_id']}: {result['status']} ({result['score']}%)")

# Generate report
report = agent.generate_compliance_report("gdpr")
print(f"\nOverall GDPR Score: {report['compliance_score']}%")
print(f"Compliant: {report['compliant_count']}")
print(f"Non-compliant: {report['non_compliant_count']}")
```

### Example 2: HIPAA Audit Trail

```python
# Configure for HIPAA compliance
agent = ComplianceAgent({
    "frameworks": ["hipaa"],
    "audit_retention_days": 2190,  # 6 years for HIPAA
    "audit_immutable": True
})

# Log HIPAA-related events
agent.log_audit_event(
    action="ACCESS",
    actor="doctor@hospital.org",
    resource="patient:12345",
    details={
        "record_type": "medical_record",
        "access_purpose": "treatment",
        "minimum_necessary": True
    },
    category="hipaa"
)

agent.log_audit_event(
    action="DISCLOSE",
    actor="billing@hospital.org",
    resource="patient:12345",
    details={
        "disclosure_type": "payment",
        "recipient": "insurance_company",
        "data_elements": ["diagnosis", "procedure_codes"]
    },
    category="hipaa"
)

# Query audit logs for HIPAA review
hipaa_logs = agent.query_audit_logs(
    category="hipaa",
    start_date="2024-01-01",
    end_date="2024-12-31"
)

# Generate HIPAA audit report
audit_report = agent.generate_audit_report(
    period="2024-Q4",
    include_statistics=True,
    include_anomalies=True
)

print(f"Total HIPAA events: {audit_report['total_events']}")
print(f"Access events: {audit_report['access_events']}")
print(f"Disclosure events: {audit_report['disclosure_events']}")
```

### Example 3: SOC 2 Risk Assessment

```python
# SOC 2 risk assessment
agent = ComplianceAgent({"frameworks": ["soc2"]})

# Create risk assessments
risks = [
    agent.create_risk_assessment(
        asset="Cloud Infrastructure",
        threat="Unauthorized Access",
        vulnerability="Weak IAM policies",
        likelihood="high",
        impact="critical",
        existing_controls=["MFA", "Basic IAM"],
        recommended_controls=["Zero Trust", "Just-in-time access"],
        mitigation_plan="Implement zero trust architecture by Q3"
    ),
    agent.create_risk_assessment(
        asset="Customer Data",
        threat="Data Breach",
        vulnerability="Insufficient encryption",
        likelihood="medium",
        impact="critical",
        existing_controls=["TLS 1.2", "Basic encryption"],
        recommended_controls=["TLS 1.3", "End-to-end encryption", "Key rotation"],
        mitigation_plan="Upgrade encryption standards by Q2"
    )
]

# Get risk summary
risk_summary = agent.get_risk_summary()
print(f"Critical Risks: {risk_summary['critical_risks']}")
print(f"High Risks: {risk_summary['high_risks']}")
print(f"Overall Risk Score: {risk_summary['overall_score']}")

# Generate risk report
risk_report = agent.generate_risk_report(
    period="2024-Q1",
    include_mitigation_status=True
)
```

### Example 4: PCI DSS Policy Management

```python
# PCI DSS policy management
agent = ComplianceAgent({"frameworks": ["pci_dss"]})

# Create PCI DSS policies
policies = [
    agent.create_policy(
        title="Cardholder Data Environment Policy",
        framework="pci_dss",
        content="All systems processing cardholder data must...",
        owner="Security Team",
        version="2.0",
        required_acknowledgments=True
    ),
    agent.create_policy(
        title="Vulnerability Management Policy",
        framework="pci_dss",
        content="Vulnerabilities must be scanned quarterly...",
        owner="Security Team",
        version="1.5"
    )
]

# Approval workflow
for policy in policies:
    agent.approve_policy(
        policy_id=policy["id"],
        approved_by="CISO",
        comments="Approved for PCI DSS compliance"
    )

# Track acknowledgments
policy_summary = agent.get_policy_summary()
print(f"Total Policies: {policy_summary['total_policies']}")
print(f"Acknowledgment Rate: {policy_summary['acknowledgment_rate']}%")
```

### Example 5: ISO 27001 Integration

```python
# ISO 27001 integration example
agent = ComplianceAgent({
    "frameworks": ["iso27001"],
    "integrations": {
        "jira": {
            "enabled": True,
            "host": "jira.company.com",
            "project": "ISO27001"
        }
    }
})

# Add ISO 27001 controls
controls = [
    agent.add_requirement("iso27001", "A.8.1", "Asset Management", severity="high"),
    agent.add_requirement("iso27001", "A.9.1", "Access Control", severity="critical"),
    agent.add_requirement("iso27001", "A.12.6", "Technical Vulnerability Management", severity="high")
]

# Map to Jira issues
for control in controls:
    jira_issue = agent.create_jira_issue(
        summary=f"Implement {control['requirement']}",
        description=control['description'],
        issue_type="Task",
        assignee="security-team@company.com"
    )
    print(f"Created Jira issue: {jira_issue['key']}")

# Generate ISO 27001 compliance report
report = agent.generate_compliance_report("iso27001")
print(f"ISO 27001 Score: {report['compliance_score']}%")
```

## Files

- `agent.py` — Main implementation (~900 lines)
- `ARCHITECTURE.md` — System architecture with diagrams
- `GROK.md` — Agent instructions and identity
- `README.md` — This file
- `config.py` — Configuration management
- `evaluators.py` — Custom evidence evaluators
- `plugins.py` — Plugin system
- `integrations.py` — External system integrations
- `tests/` — Test suite
- `docs/` — Additional documentation

## Contributing

1. **Add New Compliance Framework Support** — Implement framework definitions, controls, and evaluation logic

2. **Enhance Evidence Evaluation Logic** — Create custom evaluators for specific compliance needs

3. **Add Automated Scanning Integrations** — Integrate with security scanning tools (Nessus, Qualys, etc.)

4. **Improve Reporting and Dashboards** — Enhance report templates and dashboard visualizations

5. **Update Documentation for API Changes** — Keep documentation current with API modifications

6. **Add Test Coverage** — Write unit and integration tests for new features

7. **Performance Optimization** — Identify and optimize performance bottlenecks

8. **Accessibility Improvements** — Ensure compliance reports are accessible

9. **Internationalization** — Add support for multiple languages in reports

10. **Mobile Support** — Develop mobile-friendly interfaces for compliance checking

## License

Part of the Awesome Grok Skills collection. See project root for license details.