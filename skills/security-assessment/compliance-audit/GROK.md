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

## Detailed Workflow: End-to-End Compliance Audit

### Phase 1: Scope Definition and Framework Selection

```python
from security_assessment.compliance_audit import AuditWorkflow

workflow = AuditWorkflow(
    organization="Acme Corp",
    audit_type="annual",
    frameworks=["ISO27001", "SOC2", "PCI_DSS"]
)

# Define organizational scope
workflow.define_scope(
    business_units=["Engineering", "Finance", "Operations"],
    systems=["production-api", "customer-portal", "payment-gateway"],
    data_classes=["PII", "PCI", "financial", "internal"],
    locations=["us-east-1", "eu-west-1"],
    third_party_services=["aws", "cloudflare", "stripe"]
)

# Identify applicable frameworks and map overlapping requirements
applicable = workflow.identify_applicable_frameworks()
for framework in applicable:
    print(f"{framework.name} v{framework.version}: {framework.control_count} controls")
    print(f"  Estimated overlap with other frameworks: {framework.overlap_percent:.0f}%")
    print(f"  Estimated unique controls: {framework.unique_controls}")

# Generate cross-framework mapping
mapping = workflow.cross_framework_map()
print(f"\nTotal unique controls across all frameworks: {mapping.unique_count}")
print(f"Controls satisfying 2+ frameworks: {mapping.overlapping_count}")
print(f"Estimated audit effort reduction: {mapping.efficiency_gain:.0f}%")
```

### Phase 2: Evidence Collection Pipeline

```python
from security_assessment.compliance_audit import EvidencePipeline

pipeline = EvidencePipeline(
    frameworks=["ISO27001", "SOC2", "PCI_DSS"],
    evidence_store="./evidence-2025/"
)

# Configure evidence sources
pipeline.add_source(
    name="aws-config",
    type="cloud_api",
    provider="aws",
    config={
        "regions": ["us-east-1", "eu-west-1"],
        "rules": ["encrypted-volumes", "public-snapshots", "root-account-mfa"]
    }
)

pipeline.add_source(
    name="github-security",
    type="code_repository",
    provider="github",
    config={
        "org": "acme-corp",
        "repos": ["api-gateway", "customer-portal", "payment-service"],
        "checks": ["dependabot", "code-scanning", "secret-scanning"]
    }
)

pipeline.add_source(
    name="jira-compliance",
    type="ticketing",
    provider="jira",
    config={
        "project": "SEC",
        "issue_types": ["Security Finding", "Compliance Gap"],
        "fields": ["status", "priority", "assignee", "resolution"]
    }
)

pipeline.add_source(
    name="siem-logs",
    type="log_aggregation",
    provider="splunk",
    config={
        "index": "security",
        "queries": {
            "access_reviews": "index=iam action=access_review",
            "policy_violations": "index=security action=policy_violation",
            "incident_closures": "index=incident status=closed"
        }
    }
)

# Execute collection
collection_result = pipeline.collect(
    control_ids=["A.8.1", "A.8.9", "A.8.24", "CC6.1", "CC6.3", "Req 1", "Req 6"],
    date_range=("2025-01-01", "2025-12-31"),
    parallel=True
)

print(f"Evidence collected: {collection_result.total_artifacts}")
print(f"  Automated: {collection_result.automated_count}")
print(f"  Manual required: {collection_result.manual_count}")
print(f"  Missing evidence: {collection_result.missing_count}")

for missing in collection_result.missing:
    print(f"  MISSING: {missing.control_id} — {missing.evidence_type}")
    print(f"    Suggested collection: {missing.collection_method}")
```

### Phase 3: Gap Analysis and Remediation Planning

```python
from security_assessment.compliance_audit import GapAnalyzer, RemediationPlanner

# Run gap analysis
analyzer = GapAnalyzer(framework="ISO27001:2022")
gaps = analyzer.analyze(
    controls=organization_controls,
    evidence=collected_evidence,
    scope=["A.5", "A.6", "A.7", "A.8"]
)

# Generate remediation plan
planner = RemediationPlanner()
plan = planner.create_plan(
    gaps=gaps,
    constraints={
        "budget": 150000,
        "timeline_months": 6,
        "team_capacity": 3  # FTEs available
    }
)

print("Remediation Plan:")
for i, action in enumerate(plan.actions, 1):
    print(f"  {i}. [{action.priority}] {action.control_id}: {action.description}")
    print(f"     Effort: {action.estimated_hours}h | Cost: ${action.estimated_cost:,.0f}")
    print(f"     Owner: {action.owner} | Due: {action.due_date}")
    print(f"     Dependencies: {action.dependencies}")
```

### Phase 4: Continuous Compliance Monitoring

```python
from security_assessment.compliance_audit import ComplianceMonitor, AlertEngine

# Configure continuous monitoring
monitor = ComplianceMonitor(
    frameworks=["ISO27001", "SOC2", "PCI_DSS"],
    check_interval_minutes=15
)

# Define compliance drift rules
monitor.add_rule(
    name="encryption-at-rest-drift",
    control="A.8.24",
    description="Detect when encrypted volumes become unencrypted",
    check=lambda asset: asset.encryption_enabled == True,
    severity="critical",
    auto_ticket=True
)

monitor.add_rule(
    name="mfa-enforcement-drift",
    control="CC6.1",
    description="Detect when MFA is disabled for admin accounts",
    check=lambda user: user.mfa_enabled == True if user.is_admin else True,
    severity="high",
    auto_ticket=True
)

monitor.add_rule(
    name="access-review-overdue",
    control="A.5.18",
    description="Detect overdue access reviews (>90 days since last review)",
    check=lambda review: review.last_review_date > (today - timedelta(days=90)),
    severity="medium",
    auto_ticket=False
)

# Configure alerting
alert_engine = AlertEngine()
alert_engine.add_channel(
    type="slack",
    webhook_url="https://hooks.slack.com/services/T.../B...",
    severity_filter=["critical", "high"]
)
alert_engine.add_channel(
    type="email",
    recipients=["security@acme-corp.com", "compliance@acme-corp.com"],
    severity_filter=["critical", "high", "medium"]
)
alert_engine.add_channel(
    type="pagerduty",
    service_key="...",
    severity_filter=["critical"]
)

monitor.set_alert_engine(alert_engine)
monitor.start()
```

### Phase 5: Audit Readiness Assessment

```python
from security_assessment.compliance_audit import AuditReadinessChecker

checker = AuditReadinessChecker(framework="ISO27001:2022")
readiness = checker.check(
    controls=organization_controls,
    evidence=collected_evidence,
    policies=policy_documents,
    previous_findings=previous_audit_findings
)

print("Audit Readiness Report:")
print(f"  Overall score: {readiness.score:.0f}%")
print(f"  Ready: {readiness.ready_count}/{readiness.total_controls}")
print(f"  High-risk gaps: {readiness.high_risk_gaps}")
print(f"  Estimated findings: {readiness.estimated_findings}")

for category in readiness.categories:
    print(f"\n  {category.name}: {category.score:.0f}%")
    for gap in category.gaps:
        print(f"    [{gap.severity}] {gap.control_id}: {gap.description}")
        print(f"    Days to audit: {gap.days_until_audit}")
        print(f"    Remediation feasible: {gap.remediation_feasible}")
```

## Advanced Evidence Collection Techniques

### Automated Screenshot Evidence

```python
from security_assessment.compliance_audit.evidence import ScreenshotEvidence

screenshot_evidence = ScreenshotEvidence(
    browser="chromium",
    viewport={"width": 1920, "height": 1080},
    wait_for_selector=".dashboard-loaded"
)

# Capture configuration screens as evidence
screenshots = screenshot_evidence.capture_batch(
    urls=[
        "https://console.aws.amazon.com/iam/home#/security_credentials",
        "https://console.aws.amazon.com/config/home#/settings",
        "https://console.cloud.google.com/security-center"
    ],
    annotations=[
        {"url_pattern": "iam", "text": "Root account MFA enabled"},
        {"url_pattern": "config", "text": "AWS Config rules active"},
        {"url_pattern": "security-center", "text": "SCC findings reviewed"}
    ],
    output_dir="./evidence/screenshots/"
)
```

### Log-Based Evidence Collection

```python
from security_assessment.compliance_audit.evidence import LogEvidence

log_evidence = LogEvidence(source="splunk")

# Collect access review evidence
access_reviews = log_evidence.query(
    search='index=iam action=access_review status=completed',
    time_range="last_90_days",
    fields=["reviewer", "review_date", "systems_reviewed", "findings_count"],
    output_format="evidence_package"
)

# Collect incident response evidence
incident_evidence = log_evidence.query(
    search='index=incident type="security_incident" status=closed',
    time_range="last_365_days",
    fields=["incident_id", "detection_time", "response_time", "resolution_time", "root_cause"],
    output_format="evidence_package"
)

# Package with metadata
access_reviews.package(
    control_ids=["A.5.18", "CC6.1", "CC6.3"],
    framework="ISO27001",
    reviewer="compliance-team",
    output_path="./evidence/access-reviews/"
)
```

### API-Based Evidence Collection

```python
from security_assessment.compliance_audit.evidence import APIEvidence

# Collect evidence from GitHub security features
github_evidence = APIEvidence(
    provider="github",
    token=os.environ["GITHUB_TOKEN"]
)

dependabot_evidence = github_evidence.collect(
    endpoint="/repos/{org}/{repo}/vulnerability-alerts",
    params={"state": "enabled"},
    transform=lambda data: {
        "control": "A.8.8",
        "evidence_type": "technical_control",
        "description": f"Dependabot enabled for {repo}",
        "data": data,
        "collected_at": datetime.utcnow().isoformat()
    }
)

# Collect evidence from AWS Config
aws_evidence = APIEvidence(
    provider="aws",
    profile="security-audit"
)

config_rules = aws_evidence.collect(
    service="config",
    action="DescribeConfigRules",
    params={"ConfigRuleNames": ["encrypted-volumes", "root-account-mfa-enabled"]},
    transform=lambda rule: {
        "control": "A.8.24" if "encrypted" in rule["ConfigRuleName"] else "A.5.16",
        "evidence_type": "automated_check",
        "rule_name": rule["ConfigRuleName"],
        "compliance": rule["Compliance"]["ComplianceStatus"],
        "evaluation_time": rule["LastSuccessfulInvocationTime"]
    }
)
```

## Non-Conformity Management

### Tracking Non-Conformities

```python
from security_assessment.compliance_audit import NonConformityTracker

tracker = NonConformityTracker()

# Log a non-conformity
nc = tracker.create(
    id="NC-2025-001",
    control_id="A.8.9",
    framework="ISO27001",
    severity="major",
    description="Cryptographic keys not rotated within 12-month policy period",
    evidence_package="evidence/nc-2025-001/",
    root_cause="No automated key rotation configured in AWS KMS",
    detected_date="2025-06-15",
    auditor="external-audit-team"
)

# Create corrective action plan
cap = tracker.create_cap(
    nc_id="NC-2025-001",
    actions=[
        {
            "description": "Enable automatic key rotation for all KMS keys",
            "owner": "cloud-engineering",
            "due_date": "2025-07-15",
            "evidence_required": ["kms-rotation-config-screenshot", "rotation-log"]
        },
        {
            "description": "Implement monitoring for key rotation compliance",
            "owner": "security-operations",
            "due_date": "2025-07-30",
            "evidence_required": ["monitoring-dashboard-screenshot", "alert-config"]
        }
    ],
    verification_method="automated-check + manual-review",
    target_closure_date="2025-08-15"
)

# Track progress
status = tracker.get_status("NC-2025-001")
print(f"NC Status: {status.current_status}")
print(f"Actions completed: {status.actions_completed}/{status.total_actions}")
print(f"Days remaining: {status.days_remaining}")
print(f"Risk of overdue: {status.overdue_risk}")
```

### Non-Conformity Dashboard

```python
from security_assessment.compliance_audit import NCDashboard

dashboard = NCDashboard(data_source=tracker)
summary = dashboard.generate_summary(
    time_range="last_12_months",
    group_by=["framework", "severity", "status"]
)

print("Non-Conformity Summary:")
print(f"  Total open NCs: {summary.total_open}")
print(f"  Critical: {summary.critical}")
print(f"  Major: {summary.major}")
print(f"  Minor: {summary.minor}")
print(f"  Average time to closure: {summary.avg_closure_days} days")
print(f"  NCs overdue: {summary.overdue_count}")

for trend in summary.monthly_trend:
    print(f"  {trend.month}: Opened={trend.opened}, Closed={trend.closed}")
```

## Database Schema for Compliance Data

### PostgreSQL Schema

```sql
-- Framework definitions
CREATE TABLE frameworks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    version VARCHAR(20) NOT NULL,
    description TEXT,
    control_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, version)
);

-- Control definitions
CREATE TABLE controls (
    id SERIAL PRIMARY KEY,
    framework_id INTEGER REFERENCES frameworks(id),
    control_id VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    control_type VARCHAR(50), -- preventive, detective, corrective
    implementation_status VARCHAR(50), -- implemented, partial, not_implemented
    last_assessed_at TIMESTAMP,
    next_assessment_due TIMESTAMP,
    UNIQUE(framework_id, control_id)
);

-- Cross-framework mapping
CREATE TABLE control_mappings (
    id SERIAL PRIMARY KEY,
    source_control_id INTEGER REFERENCES controls(id),
    target_control_id INTEGER REFERENCES controls(id),
    mapping_confidence FLOAT, -- 0.0 to 1.0
    mapping_type VARCHAR(50), -- exact, partial, related
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_control_id, target_control_id)
);

-- Evidence artifacts
CREATE TABLE evidence (
    id SERIAL PRIMARY KEY,
    control_id INTEGER REFERENCES controls(id),
    evidence_type VARCHAR(50), -- screenshot, log, document, api_response, manual
    title VARCHAR(200) NOT NULL,
    description TEXT,
    file_path VARCHAR(500),
    file_hash VARCHAR(64), -- SHA-256
    collected_by VARCHAR(100),
    collected_at TIMESTAMP NOT NULL,
    valid_until TIMESTAMP,
    framework_specific JSONB, -- framework-specific metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit trail
CREATE TABLE audit_trail (
    id BIGSERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INTEGER NOT NULL,
    action VARCHAR(50) NOT NULL,
    actor VARCHAR(100) NOT NULL,
    old_value JSONB,
    new_value JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    user_agent TEXT
);

-- Non-conformities
CREATE TABLE non_conformities (
    id SERIAL PRIMARY KEY,
    nc_number VARCHAR(50) UNIQUE NOT NULL,
    control_id INTEGER REFERENCES controls(id),
    severity VARCHAR(20) NOT NULL, -- critical, major, minor
    description TEXT NOT NULL,
    root_cause TEXT,
    detected_date DATE NOT NULL,
    target_closure_date DATE,
    actual_closure_date DATE,
    status VARCHAR(50) DEFAULT 'open',
    auditor VARCHAR(100),
    evidence_package_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Corrective action plans
CREATE TABLE corrective_actions (
    id SERIAL PRIMARY KEY,
    nc_id INTEGER REFERENCES non_conformities(id),
    action_description TEXT NOT NULL,
    owner VARCHAR(100) NOT NULL,
    due_date DATE NOT NULL,
    completed_date DATE,
    status VARCHAR(50) DEFAULT 'pending',
    evidence_required JSONB,
    verification_method TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Compliance snapshots (periodic)
CREATE TABLE compliance_snapshots (
    id SERIAL PRIMARY KEY,
    framework_id INTEGER REFERENCES frameworks(id),
    snapshot_date DATE NOT NULL,
    overall_score FLOAT,
    controls_compliant INTEGER,
    controls_partial INTEGER,
    controls_non_compliant INTEGER,
    controls_no_evidence INTEGER,
    risk_score FLOAT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_controls_framework ON controls(framework_id);
CREATE INDEX idx_controls_status ON controls(implementation_status);
CREATE INDEX idx_evidence_control ON evidence(control_id);
CREATE INDEX idx_evidence_collected ON evidence(collected_at);
CREATE INDEX idx_audit_trail_entity ON audit_trail(entity_type, entity_id);
CREATE INDEX idx_audit_trail_timestamp ON audit_trail(timestamp);
CREATE INDEX idx_nc_status ON non_conformities(status);
CREATE INDEX idx_nc_severity ON non_conformities(severity);
CREATE INDEX idx_snapshots_framework_date ON compliance_snapshots(framework_id, snapshot_date);
```

## Compliance Reporting API

### REST API Endpoints

```python
from fastapi import FastAPI, Query, Depends
from security_assessment.compliance_audit import ComplianceAPI

app = FastAPI(title="Compliance Audit API", version="1.0.0")
api = ComplianceAPI(data_store=postgresql_store)

@app.get("/api/v1/frameworks")
async def list_frameworks(
    organization_id: str = Depends(get_org_id)
):
    """List all applicable frameworks for the organization."""
    frameworks = await api.list_frameworks(organization_id)
    return {
        "frameworks": [
            {
                "name": f.name,
                "version": f.version,
                "control_count": f.control_count,
                "compliance_score": f.compliance_score,
                "last_assessed": f.last_assessed
            }
            for f in frameworks
        ]
    }

@app.get("/api/v1/frameworks/{framework}/controls")
async def list_controls(
    framework: str,
    status: str = Query(None, enum=["compliant", "partial", "non_compliant", "no_evidence"]),
    category: str = None
):
    """List controls for a framework with optional filtering."""
    controls = await api.list_controls(framework, status=status, category=category)
    return {"controls": controls, "total": len(controls)}

@app.get("/api/v1/controls/{control_id}/evidence")
async def list_evidence(control_id: str):
    """List evidence artifacts for a specific control."""
    evidence = await api.list_evidence(control_id)
    return {
        "control_id": control_id,
        "evidence": evidence,
        "coverage_score": api.calculate_evidence_coverage(control_id)
    }

@app.post("/api/v1/gap-analysis")
async def run_gap_analysis(request: GapAnalysisRequest):
    """Run gap analysis for a framework."""
    result = await api.run_gap_analysis(
        framework=request.framework,
        scope=request.scope,
        date_range=request.date_range
    )
    return result

@app.get("/api/v1/compliance-dashboard")
async def compliance_dashboard(
    frameworks: List[str] = Query(...),
    time_range: str = Query("30d")
):
    """Get compliance dashboard data."""
    dashboard = await api.get_dashboard(frameworks, time_range)
    return {
        "overall_score": dashboard.overall_score,
        "framework_scores": dashboard.framework_scores,
        "trend_data": dashboard.trend_data,
        "recent_findings": dashboard.recent_findings,
        "upcoming_audits": dashboard.upcoming_audits
    }

@app.post("/api/v1/non-conformities")
async def create_nc(request: CreateNCRequest):
    """Create a new non-conformity."""
    nc = await api.create_non_conformity(request)
    return {"nc_id": nc.id, "nc_number": nc.number}

@app.put("/api/v1/non-conformities/{nc_id}/status")
async def update_nc_status(nc_id: str, request: UpdateNCStatusRequest):
    """Update non-conformity status."""
    nc = await api.update_nc_status(nc_id, request)
    return {"nc_id": nc.id, "status": nc.status, "updated_at": nc.updated_at}
```

## Deployment Configuration

### Kubernetes Deployment

```yaml
# compliance-audit-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: compliance-audit-service
  namespace: security-tools
  labels:
    app: compliance-audit
    version: v2.0.0
spec:
  replicas: 3
  selector:
    matchLabels:
      app: compliance-audit
  template:
    metadata:
      labels:
        app: compliance-audit
    spec:
      serviceAccountName: compliance-audit-sa
      containers:
        - name: compliance-audit
          image: acme-corp/compliance-audit:2.0.0
          ports:
            - containerPort: 8080
              name: http
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: compliance-db-credentials
                  key: url
            - name: AWS_ACCESS_KEY_ID
              valueFrom:
                secretKeyRef:
                  name: aws-credentials
                  key: access-key-id
            - name: AWS_SECRET_ACCESS_KEY
              valueFrom:
                secretKeyRef:
                  name: aws-credentials
                  key: secret-access-key
            - name: SLACK_WEBHOOK_URL
              valueFrom:
                secretKeyRef:
                  name: alerting-credentials
                  key: slack-webhook
          resources:
            requests:
              cpu: "500m"
              memory: "512Mi"
            limits:
              cpu: "1000m"
              memory: "1Gi"
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
          volumeMounts:
            - name: evidence-storage
              mountPath: /app/evidence
      volumes:
        - name: evidence-storage
          persistentVolumeClaim:
            claimName: compliance-evidence-pvc
---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: compliance-evidence-collection
  namespace: security-tools
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: compliance-audit-sa
          containers:
            - name: evidence-collector
              image: acme-corp/compliance-audit:2.0.0
              command: ["python", "-m", "compliance_audit.collect_evidence"]
              env:
                - name: DATABASE_URL
                  valueFrom:
                    secretKeyRef:
                      name: compliance-db-credentials
                      key: url
          restartPolicy: OnFailure
      backoffLimit: 3
```

## Testing Examples

### Unit Tests for Compliance Analyzer

```python
import pytest
from unittest.mock import Mock, patch
from security_assessment.compliance_audit import ComplianceAnalyzer, GapAnalyzer

class TestComplianceAnalyzer:
    def setup_method(self):
        self.analyzer = ComplianceAnalyzer(framework="ISO27001:2022")

    def test_gap_analysis_all_compliant(self):
        controls = [
            {"id": "A.8.1", "status": "compliant", "evidence": ["doc1", "doc2"]},
            {"id": "A.8.2", "status": "compliant", "evidence": ["doc3"]},
        ]
        gaps = self.analyzer.gap_analysis(
            current_controls=controls,
            target_scope=["A.8"]
        )
        assert gaps.compliant == 2
        assert gaps.non_compliant == 0
        assert gaps.no_evidence == 0

    def test_gap_analysis_with_gaps(self):
        controls = [
            {"id": "A.8.1", "status": "compliant", "evidence": ["doc1"]},
            {"id": "A.8.2", "status": "partial", "evidence": []},
            {"id": "A.8.3", "status": "non_compliant", "evidence": ["doc2"]},
        ]
        gaps = self.analyzer.gap_analysis(
            current_controls=controls,
            target_scope=["A.8"]
        )
        assert gaps.compliant == 1
        assert gaps.partial == 1
        assert gaps.non_compliant == 1

    def test_gap_analysis_priority_scoring(self):
        controls = [
            {"id": "A.8.1", "status": "non_compliant", "criticality": "high"},
            {"id": "A.8.2", "status": "non_compliant", "criticality": "low"},
        ]
        gaps = self.analyzer.gap_analysis(
            current_controls=controls,
            target_scope=["A.8"]
        )
        high_priority = [g for g in gaps.findings if g.priority == "critical"]
        assert len(high_priority) == 1

    @patch("security_assessment.compliance_audit.evidence.Collector")
    def test_evidence_collection_mock(self, mock_collector):
        mock_collector.return_value.collect.return_value = [
            {"control": "A.8.1", "evidence": "config-screenshot.png"}
        ]
        result = self.analyzer.collect_evidence(
            control_ids=["A.8.1"],
            sources=["aws_config"]
        )
        assert len(result) > 0


class TestSOC2Analyzer:
    def setup_method(self):
        self.analyzer = SOC2Analyzer(
            trust_service_criteria=["CC", "A", "C"]
        )

    def test_readiness_assessment(self):
        controls = [
            {"criteria": "CC6.1", "status": "effective", "evidence": ["doc1"]},
            {"criteria": "CC6.2", "status": "partial", "evidence": []},
        ]
        readiness = self.analyzer.assess(
            controls=controls,
            evidence_store={},
            review_period="2025-01-01 to 2025-12-31"
        )
        assert readiness.criteria_scores[0].score > 0

    def test_trust_service_criteria_coverage(self):
        criteria_coverage = self.analyzer.get_criteria_coverage()
        assert "CC" in criteria_coverage
        assert "A" in criteria_coverage


class TestCrossFrameworkMapper:
    def setup_method(self):
        self.mapper = CrossFrameworkMapper()
        self.mapper.load_frameworks(["ISO27001", "SOC2", "PCI_DSS"])

    def test_control_mapping(self):
        mapping = self.mapper.map_control(
            control_description="Multi-factor authentication for administrative access"
        )
        assert len(mapping.matches) > 0
        assert all(m.confidence > 0 for m in mapping.matches)

    def test_overlap_analysis(self):
        overlap = self.mapper.analyze_overlap()
        assert overlap.total_unique_controls > 0
        assert overlap.overlapping_percentage >= 0
```

## Monitoring and Alerting Setup

### Prometheus Metrics

```python
from prometheus_client import Counter, Gauge, Histogram
from security_assessment.compliance_audit import ComplianceMonitor

# Define metrics
controls_assessed_total = Counter(
    'compliance_controls_assessed_total',
    'Total number of controls assessed',
    ['framework', 'status']
)

compliance_score_gauge = Gauge(
    'compliance_score',
    'Current compliance score per framework',
    ['framework']
)

evidence_collection_duration = Histogram(
    'compliance_evidence_collection_duration_seconds',
    'Time taken to collect evidence',
    ['source_type'],
    buckets=[1, 5, 10, 30, 60, 120, 300]
)

non_conformities_open = Gauge(
    'compliance_non_conformities_open',
    'Number of open non-conformities',
    ['severity', 'framework']
)

gap_remediation_progress = Gauge(
    'compliance_gap_remediation_progress',
    'Percentage of gaps remediated',
    ['framework', 'category']
)

# Instrument the monitor
class MetricsCollector:
    def __init__(self, monitor: ComplianceMonitor):
        self.monitor = monitor

    def record_assessment(self, framework: str, control_id: str, status: str):
        controls_assessed_total.labels(framework=framework, status=status).inc()

    def update_score(self, framework: str, score: float):
        compliance_score_gauge.labels(framework=framework).set(score)

    def update_nc_count(self, framework: str, severity: str, count: int):
        non_conformities_open.labels(severity=severity, framework=framework).set(count)

    def update_remediation(self, framework: str, category: str, progress: float):
        gap_remediation_progress.labels(framework=framework, category=category).set(progress)
```

### Grafana Dashboard Configuration

```json
{
  "dashboard": {
    "title": "Compliance Audit Dashboard",
    "panels": [
      {
        "title": "Compliance Score by Framework",
        "type": "stat",
        "targets": [
          {
            "expr": "compliance_score",
            "legendFormat": "{{framework}}"
          }
        ]
      },
      {
        "title": "Controls Assessment Distribution",
        "type": "piechart",
        "targets": [
          {
            "expr": "compliance_controls_assessed_total",
            "legendFormat": "{{framework}} - {{status}}"
          }
        ]
      },
      {
        "title": "Open Non-Conformities",
        "type": "bargauge",
        "targets": [
          {
            "expr": "compliance_non_conformities_open",
            "legendFormat": "{{framework}} - {{severity}}"
          }
        ]
      },
      {
        "title": "Remediation Progress",
        "type": "gauge",
        "targets": [
          {
            "expr": "compliance_gap_remediation_progress",
            "legendFormat": "{{framework}} - {{category}}"
          }
        ],
        "thresholds": {
          "steps": [
            {"color": "red", "value": 0},
            {"color": "yellow", "value": 50},
            {"color": "green", "value": 80}
          ]
        }
      },
      {
        "title": "Evidence Collection Duration",
        "type": "heatmap",
        "targets": [
          {
            "expr": "rate(compliance_evidence_collection_duration_seconds_sum[5m])",
            "legendFormat": "{{source_type}}"
          }
        ]
      }
    ]
  }
}
```

### Alert Rules

```yaml
# compliance_alerts.yaml
groups:
  - name: compliance_alerts
    rules:
      - alert: ComplianceScoreDropped
        expr: compliance_score < 80
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Compliance score dropped below 80%"
          description: "Framework {{ $labels.framework }} score is {{ $value }}%"

      - alert: CriticalNonConformity
        expr: compliance_non_conformities_open{severity="critical"} > 0
        for: 0m
        labels:
          severity: critical
        annotations:
          summary: "Critical non-conformity detected"
          description: "{{ $value }} critical NCs open for {{ $labels.framework }}"

      - alert: EvidenceCollectionFailed
        expr: rate(compliance_evidence_collection_errors_total[5m]) > 0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Evidence collection failures detected"
          description: "Evidence collection failing for source {{ $labels.source }}"

      - alert: AuditDeadlineApproaching
        expr: days_until(compliance_next_audit_date) < 30 and compliance_score < 90
        for: 0m
        labels:
          severity: critical
        annotations:
          summary: "Audit deadline approaching with low compliance score"
          description: "Audit in {{ $value }} days with score {{ $labels.score }}%"
```

## References

- ISO 27001:2022 — Information Security Management Systems
- SOC 2 Type II — AICPA Trust Service Criteria
- PCI DSS v4.0 — Payment Card Industry Data Security Standard
- HIPAA Security Rule — 45 CFR Part 160 and Part 164
- GDPR — General Data Protection Regulation (EU) 2016/679
- NIST CSF 2.0 — Cybersecurity Framework
- CIS Controls v8 — Center for Internet Security Critical Security Controls
- COBIT 2019 — Control Objectives for Information and Related Technologies
