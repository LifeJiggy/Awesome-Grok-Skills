# Cloud Audit Agent

## Overview

The Cloud Audit Agent is an autonomous, intelligent agent that performs
end-to-end cloud security audits, compliance checks, cost analysis, and
risk assessments across AWS, Azure, GCP, Oracle Cloud, IBM Cloud, and Alibaba
Cloud. It is designed to be invoked programmatically or via a CLI to produce
actionable, structured reports for security teams, DevOps engineers, cloud
architects, compliance officers, and FinOps practitioners.

**Key capabilities:**
- Multi-cloud security posture assessment
- Regulatory and framework compliance evaluation (SOC 2, PCI DSS, HIPAA, GDPR, CIS, NIST, ISO 27001, FedRAMP, CCPA)
- Detailed cost analysis with dollar-value optimisation recommendations
- Quantitative risk scoring with automated prioritisation and mitigation guidance
- Pluggable notification channels (console, Slack, email)
- Cached, repeatable audit runs with TTL-based invalidation
- Multiple export formats: JSON, CSV, and human-readable text

---

## Capabilities

### 1. Cloud Security Audits

Perform comprehensive security audits across cloud providers and resource types.

**Supported resource types (AWS simulation):**
- S3 (Simple Storage Service)
- EC2 (Elastic Compute Cloud)
- RDS (Relational Database Service)
- IAM (Identity and Access Management)
- EKS (Elastic Kubernetes Service)

**Built-in security checks:**

| Resource | Check | Severity | Category |
|----------|-------|----------|----------|
| S3 | `block_public_acls` / `block_public_policy` disabled | HIGH | Network Exposure |
| S3 | `encryption` disabled | HIGH | Encryption |
| S3 | `logging` disabled | MEDIUM | Misconfiguration |
| RDS | `publicly_accessible` = True | HIGH | Network Exposure |
| RDS | `storage_encrypted` = False | HIGH | Encryption |
| EC2 | `public_ip` = True without restriction | HIGH | Network Exposure |
| EC2 | `encrypted_volumes` = False | HIGH | Encryption |
| EC2 | Security group misconfiguration | HIGH | Misconfiguration |
| IAM User | `mfa_enabled` = False | CRITICAL | Access Control |
| EKS | `endpoint_public_access` unrestricted | MEDIUM | Network Exposure |
| S3 | `versioning` disabled | LOW | Data Protection |
| EC2 | No monitoring / CloudWatch alarms | MEDIUM | Monitoring |
| IAM User | `access_keys_active` > 1 | HIGH | Access Control |
| IAM Role | `max_session_duration` > 12 hours | MEDIUM | Access Control |
| EKS | `authenticator` logging disabled | LOW | Monitoring |

**Example:**
```python
from agents.cloud_audit.agent import CloudAuditAgent, Config, CloudProvider, AuditScope

agent = CloudAuditAgent()
result = agent.audit_cloud(provider="aws", scope="security")
# => {
#   "provider": "aws",
#   "scope": "security",
#   "score": 85,
#   "findings_count": 4,
#   "findings": [...]
# }
```

Example finding output:
```json
{
  "finding_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Public access not blocked: block_public_acls",
  "description": "The s3 resource s3-bucket-prod-data has 'block_public_acls' disabled, exposing it to the public internet.",
  "severity": "high",
  "category": "network_exposure",
  "provider": "aws",
  "resource_id": "s3-bucket-prod-data",
  "resource_type": "s3",
  "region": "us-east-1",
  "account_id": "123456789012",
  "remediation": "Enable 'block_public_acls' in the S3 bucket's Public Access Block settings.",
  "compliance_frameworks": ["CIS", "PCI_DSS"],
  "evidence": {"control": "block_public_acls", "config_snapshot": {"block_public_acls": false}},
  "references": [
    "https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html",
    "https://docs.aws.amazon.com/security/latest/resources"
  ],
  "detected_at": "2024-01-15T06:00:00Z"
}
```

### 2. Compliance Checks

Evaluate a cloud environment against regulatory and industry frameworks.

**Supported frameworks:**

| Framework | Acronym | Focus |
|-----------|---------|-------|
| SOC 2 | SOC2 | Trust service criteria (security, availability, confidentiality) |
| PCI DSS | PCI_DSS | Payment card industry data security |
| HIPAA | HIPAA | Protected health information safeguards |
| General Data Protection Regulation | GDPR | EU data privacy regulation |
| CIS AWS Foundations Benchmark | CIS | AWS-specific security hardening controls |
| NIST Cybersecurity Framework | NIST_CSF | Identify, protect, detect, respond, recover |
| NIST SP 800-53 | NIST_800_53 | Security and privacy controls |
| FedRAMP | FedRAMP | US federal cloud authorisation |
| California Consumer Privacy Act | CCPA | California consumer privacy rights |
| AWS Well-Architected Framework | AWS_WELL_ARCHITECTED | Operational excellence, security, reliability, performance, cost |
| Azure Security Benchmark | AZURE_SECURITY_BENCHMARK | Azure security best practices |
| GCP Security Framework | CLOUD_SECURITY_FRAMEWORK | GCP security posture controls |

**Example:**
```python
result = agent.check_compliance(ComplianceFramework.SOC2)
# => {
#   "framework": "SOC2",
#   "compliant": false,
#   "gaps": [
#     {
#       "framework": "SOC2",
#       "control_id": "CC7.2",
#       "control_name": "Incident Detection and Monitoring",
#       "current_status": "non_compliant",
#       "recommended_action": "Enable CloudTrail...",
#       "priority": "high"
#     }
#   ],
#   "compliance_percentage": 93.75
# }
```

Example compliance gap output:
```json
{
  "gap_id": "660e8400-e29b-41d4-a716-446655440001",
  "framework": "CIS",
  "control_id": "1.4",
  "control_name": "Ensure no security groups allow ingress from 0.0.0.0/0 to port 22.",
  "description": "CIS Control 1.4 not satisfied.",
  "current_status": "non_compliant",
  "recommended_action": "Remove SSH unrestricted inbound rules from security groups.",
  "priority": "high",
  "owner": "security-team",
  "due_date": "2024-02-15T06:00:00Z",
  "evidence_url": ""
}
```

Compliance percentage calculation:
```python
compliance_percentage = (compliant_controls / total_controls) * 100
# For SOC2: (45 / 48) * 100 = 93.75%
```

### 3. Cost Analysis

Analyse cloud spend and generate actionable cost-optimisation recommendations.

**Analysis dimensions:**

| Category | Description | Typical Savings |
|----------|-------------|----------------|
| Idle Resources | EC2 instances / RDS clusters with low utilisation | ~20% of compute spend |
| Over-provisioned Resources | Right-sizing EC2/RDS based on actual utilisation | ~10.5% of compute spend |
| Reserved Instance Opportunities | Purchase RIs or Savings Plans for steady-state workloads | ~25% of annual compute |
| Storage Tiering | Move infrequent S3 objects to Standard-IA or Glacier | ~15% of storage spend |
| Network Egress | Reduce cross-region / cross-AZ data transfer | ~8% of networking spend |
| Unattached Volumes | Delete unattached EBS volumes | ~3-5% of storage spend |
| Orphaned Snapshots | Clean up orphaned RDS/EBS snapshots | ~2-4% of storage spend |
| License Optimisation | Use Bring-Your-Own-License (BYOL) where possible | ~10-15% of software spend |

**Example:**
```python
result = agent.analyze_costs(account="123456789012")
# => {
#   "account": "123456789012",
#   "spend": 36000.0,
#   "total_potential_savings": 7200.0,
#   "savings_percentage": 20.0,
#   "recommendations": [
#     {
#       "resource_id": "collection-ec2-idle",
#       "recommendation": "Identify and terminate idle EC2 instances...",
#       "projected_monthly_savings": 2160.0,
#       "confidence": "high"
#     }
#   ]
# }
```

Example cost recommendation output:
```json
{
  "reco_id": "770e8400-e29b-41d4-a716-446655440002",
  "resource_id": "collection-ec2-idle",
  "resource_type": "EC2-Instances",
  "current_monthly_cost": 10800.0,
  "projected_monthly_savings": 2160.0,
  "savings_percentage": 20.0,
  "recommendation": "Identify and terminate or stop idle EC2 instances with low CPU utilization.",
  "confidence": "high",
  "provider": "aws",
  "region": "us-east-1",
  "risk_level": "low"
}
```

### 4. Risk Assessment

Convert security findings into quantified risk records with likelihood, impact,
and mitigation guidance.

**Risk categories evaluated:**
- Data Breach
- Misconfiguration
- Access Control
- Encryption
- Network Exposure
- Compliance Violation
- Cost Overflow
- Availability
- Supply Chain
- Insider Threat

**Scoring model:**
```
risk_score = SEVERITY_WEIGHT(severity) × LIKELIHOOD(l) × IMPACT(i)
```

**Severity weights:** Critical=10, High=7, Medium=4, Low=2, Info=1  
**Likelihood / Impact weights:** High=3, Medium=2, Low=1  
**Max possible score:** 10 × 3 × 3 = 90

**Status thresholds:**

| Risk Score Range | Status | Action |
|-----------------|--------|--------|
| 0 - 4 | `accepted` | Document as tolerated residual risk |
| 5 - 9 | `open` | Remediate within current sprint |
| 10 - 14 | `high` | Escalate to stakeholder; plan within 7 days |
| 15+ | `critical` | Immediate action required; initiate incident response |

**Example:**
```python
risks = agent.assess_risks()
# => [
#   {
#     "risk_id": "...",
#     "title": "IAM user without MFA",
#     "severity": "critical",
#     "category": "access_control",
#     "likelihood": "high",
#     "impact": "high",
#     "mitigation": "Enforce MFA...",
#     "status": "critical",
#     "owner": "cloud-security-team"
#   }
# ]
```

Example risk record output:
```json
{
  "risk_id": "880e8400-e29b-41d4-a716-446655440003",
  "title": "IAM user without MFA",
  "description": "The IAM user 'admin-user' does not have multi-factor authentication enabled.",
  "category": "access_control",
  "severity": "critical",
  "likelihood": "high",
  "impact": "high",
  "mitigation": "Enforce least privilege; enable MFA; review IAM policies.",
  "residual_risk": "high",
  "owner": "cloud-security-team",
  "status": "critical",
  "detected_at": "2024-01-15T06:00:00Z"
}
```

### 5. Optimisation Recommendations

The agent provides direct, actionable recommendations with confidence levels and
quantified savings potential.

Each `CostRecommendation` includes:
- `resource_id` / `resource_type`: Target resource
- `current_monthly_cost`: Baseline spend
- `projected_monthly_savings`: Expected savings
- `savings_percentage`: Relative savings
- `confidence`: `high` / `medium` / `low`
- `risk_level`: Impact of applying the recommendation

**Confidence levels explained:**

| Confidence | Meaning |
|-----------|---------|
| `high` | Strong signal from data; low effort to implement |
| `medium` | Good signal; some manual validation required |
| `low` | Pattern-based; requires investigation before implementation |

### 6. Report Generation

Audit results are packaged into `AuditReport` objects and can be exported in
three formats.

| Format | Method | Use case |
|--------|--------|----------|
| JSON | `to_json()` | Programmatic consumption, archiving, API responses |
| CSV | `to_csv_findings()` | Spreadsheet tracking, ticker import into Jira |
| Text | `to_summary_text()` | Console output, email summaries, Slack posts |

**AuditReport schema:**
```json
{
  "report_id": "<uuid>",
  "provider": "aws",
  "scope": "full",
  "account_id": "123456789012",
  "regions": ["us-east-1", "us-west-2"],
  "started_at": "2024-01-15T06:00:00Z",
  "completed_at": "2024-01-15T06:00:12Z",
  "overall_score": 85,
  "findings": [...],
  "compliance_results": {
    "CIS": [...],
    "SOC2": [...]
  },
  "cost_recommendations": [...],
  "risks": [...],
  "metadata": {...}
}
```

---

## Usage

### Quick Start

```python
from agents.cloud_audit.agent import CloudAuditAgent

agent = CloudAuditAgent()

# Lightweight security audit
result = agent.audit_cloud(provider="aws", scope="security")
print(f"Score: {result['score']}/100  Findings: {result['findings_count']}")

# Full audit with compliance and cost analysis
from agents.cloud_audit.agent import (
    Config, CloudProvider, AuditScope, ComplianceFramework,
    ProviderConfig, ComplianceConfig, CostConfig, RiskConfig,
)

config = Config(
    providers=[
        ProviderConfig(provider=CloudProvider.AWS, regions=["us-east-1"])
    ],
    compliance=ComplianceConfig(
        enabled_frameworks=[ComplianceFramework.CIS, ComplianceFramework.SOC2]
    ),
)
agent = CloudAuditAgent(config=config)
report = agent.run_full_audit(
    provider=CloudProvider.AWS,
    scope=AuditScope.FULL,
    account_id="123456789012",
)
print(report.to_summary_text())
```

### CLI Usage

```bash
# Demo mode (simulated data)
python agents/cloud-audit/agent.py --demo

# Full audit
python agents/cloud-audit/agent.py \
  --provider aws \
  --scope full \
  --account 123456789012

# Compliance check only
python agents/cloud-audit/agent.py \
  --check-compliance \
  --framework CIS \
  --account 123456789012

# Cost analysis only
python agents/cloud-audit/agent.py \
  --analyze-costs \
  --account 123456789012

# Export full audit to JSON
python agents/cloud-audit/agent.py \
  --provider aws \
  --scope full \
  --account 123456789012 \
  --export ./reports/audit_2024.json

# Export findings to CSV
python agents/cloud-audit/agent.py \
  --provider aws \
  --scope security \
  --export ./reports/security_findings.csv \
  --export-format csv
```

### Configuration-Driven Usage

```python
from dataclasses import asdict
import json

config = _build_sample_config()

# Inspect configuration
print(json.dumps(asdict(config), indent=2, default=str))

# Validate before use
errors = config.validate()
if errors:
    raise ValueError(f"Configuration errors: {errors}")

agent = CloudAuditAgent(config=config)
```

### Custom Provider Integration

To integrate with a real cloud provider, subclass `BaseCloudClient`:

```python
import boto3
from botocore.exceptions import ClientError
from typing import List, Dict, Any
from agents.cloud_audit.agent import (
    BaseCloudClient, ProviderConfig, CloudProvider, ComplianceFramework
)

class AWSBoto3Client(BaseCloudClient):
    def __init__(self, config: ProviderConfig):
        super().__init__(config)
        self._session = boto3.Session(profile_name=config.profile)
        self._s3 = self._session.client("s3")
        self._ec2 = self._session.client("ec2")
        self._rds = self._session.client("rds")

    def authenticate(self) -> bool:
        try:
            self._session.client("sts").get_caller_identity()
            return True
        except ClientError:
            return False

    def list_resources(self, resource_type: str, region: str) -> List[Dict[str, Any]]:
        if resource_type == "s3":
            response = self._s3.list_buckets()
            return [{"resource_id": b["Name"], "resource_type": "s3", "region": region} for b in response.get("Buckets", [])]
        elif resource_type == "ec2":
            response = self._ec2.describe_instances()
            instances = []
            for reservation in response.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    instances.append({
                        "resource_id": instance["InstanceId"],
                        "resource_type": "ec2_instance",
                        "region": instance.get("Placement", {}).get("AvailabilityZone", region),
                    })
            return instances
        return []

    def get_config(self, resource_id: str) -> Dict[str, Any]:
        return {"resource_id": resource_id, "detail": "boto3_impl_needed"}

    def get_compliance_status(self, framework: ComplianceFramework) -> Dict[str, Any]:
        return {
            "framework": framework.value,
            "compliant_controls": 45,
            "non_compliant_controls": 3,
            "total_controls": 48,
            "compliance_percentage": 93.75,
        }

    def get_cost_data(self, lookback_days: int) -> Dict[str, Any]:
        ce = self._session.client("ce")
        end = datetime.datetime.utcnow().date()
        start = end - datetime.timedelta(days=lookback_days)
        response = ce.get_cost_and_usage(
            TimePeriod={"Start": start.isoformat(), "End": end.isoformat()},
            Granularity="DAILY",
            Metrics=["UnblendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
        )
        # Transform response...
        return {"total_cost": 0.0, "services": {}, "lookback_days": lookback_days}
```

### Adding Custom Security Checks

```python
class CustomSecurityCheckEngine(SecurityCheckEngine):
    def _check_tagging_compliance(self, resource: Dict[str, Any]) -> None:
        tags = resource.get("tags", {})
        required = {"env", "owner", "cost-center", "data-classification"}
        missing = required - set(tags.keys())
        if missing:
            self._add_finding(
                title="Non-compliant resource tags",
                description=f"Resource {resource.get('resource_id')} is missing required tags: {missing}",
                severity=SeverityLevel.MEDIUM,
                category=RiskCategory.MISCONFIGURATION,
                resource=resource,
                control="tagging",
            )

    def run(self, resource_types: List[str]) -> List[AuditFinding]:
        findings = super().run(resource_types)
        for resource_type in resource_types:
            resources = self._client.list_resources(resource_type, "us-east-1")
            for resource in resources:
                self._check_tagging_compliance(resource)
                self._check_backup_retention(resource)
        return findings
```

### Exporting Reports

```python
from agents.cloud_audit.agent import CloudAuditAgent, ReportFormatter

agent = CloudAuditAgent()
report = agent.run_full_audit()

# JSON (default)
agent.export_report(report, "./audit.json", fmt="json")

# CSV (findings only)
agent.export_report(report, "./findings.csv", fmt="csv")

# Human-readable text
agent.export_report(report, "./summary.txt", fmt="text")

# Or use formatter directly
formatter = ReportFormatter(report)
json_str = formatter.to_json()
text_summary = formatter.to_summary_text()
csv_data = formatter.to_csv_findings()
```

---

## Agent Instructions

When invoked, the Cloud Audit Agent must:

1. **Parse intent** from the user request or CLI arguments.
2. **Normalise inputs** (provider, scope, framework) to their enum types.
3. **Authenticate** the relevant cloud client.
4. **Execute the appropriate engine(s)** based on the requested action:
   - `audit_cloud` → `SecurityCheckEngine`
   - `check_compliance` → `ComplianceCheckEngine` + `get_compliance_status`
   - `analyze_costs` → `CostAnalysisEngine` + `get_cost_data`
   - `assess_risks` → `RiskAssessmentEngine`
   - `run_full_audit` → all engines in sequence
5. **Cache the result** if caching is enabled.
6. **Dispatch notifications** if `notify_on_gap` is enabled.
7. **Return structured data** (dict for lightweight methods; `AuditReport` for full audit).
8. **Handle errors gracefully**: log failures, continue with partial data where safe, and raise on unrecoverable errors (missing client, invalid input).

**Expected behaviour on common inputs:**

| Input | Expected Behaviour |
|-------|-------------------|
| `provider="aws", scope="full"` | Run full AWS audit; return `AuditReport` with score |
| `provider="azure", scope="security"` | Run Azure security scan (when stubbed) |
| `framework="CIS"` (string) | Normalise to `ComplianceFramework.CIS`; evaluate CIS |
| `framework="nonexistent"` | `ValueError: Unsupported compliance framework` |
| No providers in config | Use default: single AWS `us-east-1` |
| `--demo` flag | Print banner, run sample audit, export to `./audit_report.txt` |

**Failure modes:**
- Missing provider → `ValueError`
- Unknown framework → `ValueError`
- Client auth failure → `ValueError`
- Notification failure → log error, do not abort audit

**Output format:**
- Structured dictionaries or `AuditReport` objects only.
- No side effects unless `export_report` is explicitly called.
- All timestamps are UTC ISO-8601.
- All monetary values are in the configured currency (default USD).

---

## Supported Cloud Providers

| Provider | Enum | Status | Client Class |
|----------|------|--------|--------------|
| Amazon Web Services | `CloudProvider.AWS` | Simulated | `AWSSimulatedClient` |
| Microsoft Azure | `CloudProvider.AZURE` | Stub | Not yet implemented |
| Google Cloud Platform | `CloudProvider.GCP` | Stub | Not yet implemented |
| Oracle Cloud Infrastructure | `CloudProvider.ORACLE` | Stub | Not yet implemented |
| IBM Cloud | `CloudProvider.IBM_CLOUD` | Stub | Not yet implemented |
| Alibaba Cloud | `CloudProvider.ALIBABA` | Stub | Not yet implemented |
| Multi-Cloud | `CloudProvider.MULTI_CLOUD` | Aggregates across configured providers | Uses first available |
| Hybrid | `CloudProvider.HYBRID` | On-prem + cloud hybrid mode | Uses first available |

### Provider Enum Reference

```python
class CloudProvider(Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    ORACLE = "oracle"
    IBM_CLOUD = "ibm_cloud"
    ALIBABA = "alibaba"
    MULTI_CLOUD = "multi_cloud"
    HYBRID = "hybrid"
```

### Resource Types per Provider

| Provider | Supported Resources |
|----------|-------------------|
| AWS | s3, ec2, rds, iam, eks |
| Azure | (planned: storage, vm, keyvault, nsg) |
| GCP | (planned: gcs, gce, gke, iam) |
| Oracle | (planned: object_storage, compute, vcn) |
| IBM | (planned: cos, vpc, kubernetes) |
| Alibaba | (planned: oss, ecs, rds) |

---

## Supported Compliance Frameworks

| Framework | Acronym | Built-in Controls | Regulation Type |
|-----------|---------|-------------------|----------------|
| CIS AWS Foundations | CIS | 11 controls | Hardening |
| SOC 2 | SOC2 | CC6.1, CC6.6, CC7.2 | Trust Services |
| PCI DSS 4.0 | PCI_DSS | 3.4, 6.5 | Payment Card |
| HIPAA | HIPAA | 164.312 | Healthcare |
| GDPR | GDPR | Art. 5, Art. 32 | EU Data Privacy |
| NIST CSF | NIST_CSF | Framework skeleton | Cybersecurity |
| NIST SP 800-53 | NIST_800_53 | Framework skeleton | Security Controls |
| FedRAMP | FEDRAMP | Framework skeleton | US Federal |
| CCPA | CCPA | Framework skeleton | California Privacy |
| AWS Well-Architected | AWS_WELL_ARCHITECTED | Framework skeleton | Cloud Best Practices |
| Azure Security Benchmark | AZURE_SECURITY_BENCHMARK | Framework skeleton | Cloud Security |
| GCP Security Framework | CLOUD_SECURITY_FRAMEWORK | Framework skeleton | Cloud Security |

### Framework Evaluation Details

**CIS AWS Foundations:**
- 1.1: Avoid the use of the root account
- 1.2: Ensure MFA is enabled for root account
- 1.4: Ensure no security groups allow ingress from 0.0.0.0/0 to port 22
- 1.5: Ensure no security groups allow ingress from 0.0.0.0/0 to port 3389
- 1.10: Ensure no security groups allow ingress from 0.0.0.0/0 to port 443
- 2.1.1: Ensure S3 bucket policy denies insecure (HTTP) requests
- 2.1.2: Ensure S3 buckets are encrypted with AWS-KMS
- 2.1.3: Ensure S3 bucket versioning is enabled
- 2.1.5: Ensure S3 bucket policy requires encryption at minimum TLS 1.2
- 4.1: Ensure no security groups allow ingress from 0.0.0.0/0
- 5.1: Ensure no Network ACLs allow ingress from 0.0.0.0/0

**SOC 2 (CC6.1, CC6.6, CC7.2):**
- CC6.1: Logical Access Controls - IAM policies should restrict access to least privilege
- CC6.6: System Boundary Protection - Network controls at boundaries
- CC7.2: Incident Detection and Monitoring - CloudTrail and Config logging enabled in all regions

**PCI DSS 4.0 (3.4, 6.5):**
- 3.4: PAN Storage Encryption - Encryption of cardholder data at rest
- 6.5: Vulnerability Management - Address vulnerabilities in payment applications

**HIPAA (164.312):**
- 164.312: Access Controls - PHI access controls enforced via RBAC
- 164.312(a)(2)(i): Unique User Identification - Distinct user identification for PHI access

**GDPR (Art. 5, Art. 32):**
- Art. 5: Data Minimisation - Personal data collection limited to what is necessary
- Art. 32: Security of Processing - Appropriate technical and organisational measures

---

## Error Handling

| Scenario | Agent Behaviour | User-Facing Message |
|----------|-----------------|-------------------|
| No providers configured | Uses default AWS single-region config | N/A (silent fallback) |
| Invalid provider string | `ValueError` | `"Unsupported cloud provider: {provider}"` |
| Invalid scope string | `ValueError` | `"Unsupported audit scope: {scope}"` |
| Invalid framework string | `ValueError` | `"Unsupported compliance framework: {framework}"` |
| Unknown alias for framework | Resolves via alias map; raises if no match | Same as above |
| No client for provider | `ValueError` | `"No client configured for provider {provider.value}."` |
| Cache miss | Proceed normally | None (logged at INFO) |
| Cache failure | Log warning; degrade gracefully | None (logged at WARNING) |
| Notification failure | Log error per channel; audit succeeds | None (logged at ERROR) |
| Export format unsupported | `ValueError` | `"Unsupported export format: {fmt}"` |
| File write permission error | `OSError` propagates | OS-level error message |

### Error Handling Pattern in Engines

```python
try:
    result = engine.evaluate(framework)
except ValueError as e:
    logger.error("Evaluation failed for %s: %s", framework.value, e)
    raise
except Exception as e:
    logger.exception("Unexpected error during evaluation: %s", e)
    # Continue with partial results if safe
    return []
```

---

## Performance Targets

| Operation | Simulated Target | Production Target |
|-----------|------------------|-------------------|
| `audit_cloud` | <50 ms | <5 s |
| `check_compliance` (single framework) | <20 ms | <30 s |
| `analyze_costs` | <30 ms | <60 s |
| `run_full_audit` (AWS, 3 regions) | <200 ms | <5 min |

Cache round-trip: <1 ms in all environments.

### Performance Optimisation Tips

1. **Narrow the scope**: Use `security` instead of `full` when you only need security results.
2. **Limit regions**: Audit only active regions instead of all AWS regions.
3. **Enable caching**: Re-running on unchanged environments is instant.
4. **Batch requests**: Future async mode will parallelise all four engines.

---

## Testing

```bash
# Run with Python's unittest or pytest
pytest tests/agents/test_cloud_audit.py -v

# Run specific test
pytest tests/agents/test_cloud_audit.py::test_security_check_engine_s3_public_access -v

# Run with coverage
pytest tests/agents/test_cloud_audit.py --cov=agents.cloud_audit --cov-report=term-missing
```

**Recommended test coverage:**
- Unit tests for each engine with synthetic resource data.
- Integration test for `run_full_audit` end-to-end.
- CLI argument parsing via `subprocess` or `argparse.Namespace` injection.
- Cache TTL expiry tests using `time.sleep` or monkey-patched `time.time`.
- Error path tests: missing provider, bad framework, notification failure.
- Data class serialisation round-trip tests (dict → dataclass → JSON).
- Report export format validation (JSON parseable, CSV well-formed).

---

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `CLOUD_AUDIT_LOG_LEVEL` | Override agent log level | `INFO` |
| `CLOUD_AUDIT_OUTPUT_PATH` | Default export directory | `./reports` |
| `CLOUD_AUDIT_CACHE_TTL` | Override cache TTL (seconds) | `3600` |
| `CLOUD_AUDIT_CACHE_ENABLED` | Enable/disable caching | `true` |
| `SLACK_WEBHOOK_URL` | Slack channel webhook | `""` |
| `SMTP_SERVER` | Email relay hostname | `localhost` |
| `SMTP_PORT` | Email relay port | `25` |
| `AWS_PROFILE` | Default AWS credential profile | `default` |
| `AZURE_TENANT_ID` | Azure tenant identifier | `""` |

---

## Schema Version

Current agent schema: `2.0.0`

Compatibility:
- `AuditReport` and all dataclass models are backward-compatible within the major version.
- Enum additions are always backward-compatible.
- Engine method additions are additive only.

---

## Security Notes

When running the Cloud Audit Agent in production:

1. **Never commit credentials**: Use IAM roles, managed identities, or environment variables.
2. **Least privilege IAM**: Grant only read-only permissions (`ReadOnlyAccess`).
3. **Encrypt exports**: Reports may contain sensitive configuration data.
4. **Restrict access**: Limit who can read exported audit reports.
5. **Audit the auditor**: Log all agent invocations to your SIEM.
6. **Rotate regularly**: Review agent permissions and credentials quarterly.

---

## Common Patterns

### Pattern: Daily Compliance Dashboard

```python
from datetime import datetime, timedelta

def daily_compliance_dashboard():
    config = Config(
        providers=[ProviderConfig(provider=CloudProvider.AWS, regions=["us-east-1", "eu-west-1"])],
        compliance=ComplianceConfig(enabled_frameworks=[ComplianceFramework.CIS]),
        risk=RiskConfig(min_severity=SeverityLevel.LOW),
    )
    agent = CloudAuditAgent(config=config)
    report = agent.run_full_audit(scope=AuditScope.FULL)
    
    dashboard = {
        "date": datetime.utcnow().isoformat() + "Z",
        "score": report.overall_score,
        "findings_by_severity": {},
        "top_risks": [],
        "compliance_percentage": {},
    }
    
    from collections import Counter
    sev_counts = Counter(f.severity.value for f in report.findings)
    dashboard["findings_by_severity"] = dict(sev_counts)
    
    dashboard["top_risks"] = [
        {"title": r.title, "severity": r.severity.value, "status": r.status}
        for r in report.risks[:10]
    ]
    
    for fw, gaps in report.compliance_results.items():
        if gaps:
            total = gaps[0].framework.value
            dashboard["compliance_percentage"][fw] = max(
                0, 100 - len(gaps) * 5
            )
    
    return dashboard
```

### Pattern: CI/CD Pipeline Integration

```python
import sys

def ci_gate():
    config = Config(
        providers=[ProviderConfig(provider=CloudProvider.AWS, regions=["us-east-1"])],
        compliance=ComplianceConfig(
            enabled_frameworks=[ComplianceFramework.CIS],
            strict_mode=True,
            notify_on_gap=False,
        ),
    )
    agent = CloudAuditAgent(config=config)
    
    cis_result = agent.check_compliance(ComplianceFramework.CIS)
    if not cis_result["compliant"]:
        print(f"FAIL: CIS compliance gate failed with {len(cis_result['gaps'])} gaps")
        for gap in cis_result["gaps"]:
            print(f"  - [{gap['priority'].upper()}] {gap['control_id']}: {gap['control_name']}")
        sys.exit(1)
    
    print("PASS: All CIS checks compliant")
    sys.exit(0)
```

---

## Related Documentation

- See `ARCHITECTURE.md` for detailed system design and data flow diagrams.
- See `README.md` for quick-start instructions.
- See `agent.py` for complete implementation, models, engines, and CLI.

---

## Appendix: Complete Enum Reference

All enums used in the Cloud Audit Agent are defined in `agent.py`.

```python
class CloudProvider(Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    ORACLE = "oracle"
    IBM_CLOUD = "ibm_cloud"
    ALIBABA = "alibaba"
    MULTI_CLOUD = "multi_cloud"
    HYBRID = "hybrid"

class AuditScope(Enum):
    FULL = "full"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    COST = "cost"
    NETWORK = "network"
    IDENTITY = "identity"
    STORAGE = "storage"
    COMPUTE = "compute"
    DATABASE = "database"
    SERVERLESS = "serverless"
    CONTAINERS = "containers"
    IAM = "iam"

class SeverityLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class ComplianceFramework(Enum):
    SOC2 = "SOC2"
    PCI_DSS = "PCI_DSS"
    HIPAA = "HIPAA"
    GDPR = "GDPR"
    ISO27001 = "ISO27001"
    CIS = "CIS"
    NIST_CSF = "NIST_CSF"
    NIST_800_53 = "NIST_800_53"
    FEDRAMP = "FedRAMP"
    CCPA = "CCPA"
    AWS_WELL_ARCHITECTED = "AWS_Well_Architected"
    AZURE_SECURITY_BENCHMARK = "Azure_Security_Benchmark"
    GCP_SECURITY_FRAMEWORK = "GCP_Security_Framework"

class RiskCategory(Enum):
    DATA_BREACH = "data_breach"
    MISCONFIGURATION = "misconfiguration"
    ACCESS_CONTROL = "access_control"
    ENCRYPTION = "encryption"
    NETWORK_EXPOSURE = "network_exposure"
    COMPLIANCE_VIOLATION = "compliance_violation"
    COST_OVERFLOW = "cost_overflow"
    AVAILABILITY = "availability"
    SUPPLY_CHAIN = "supply_chain"
    INSIDER_THREAT = "insider_threat"
```

---

## Appendix: Supported CLI Arguments

```
usage: agent.py [-h] [--demo] [--provider {aws,azure,gcp,oracle,ibm_cloud,alibaba,multi_cloud,hybrid}]
                [--scope {full,security,compliance,cost,network,identity,storage,compute,database,serverless,containers,iam}]
                [--framework {SOC2,PCI_DSS,HIPAA,GDPR,ISO27001,CIS,NIST_CSF,NIST_800_53,FEDRAMP,CCPA,AWS_WELL_ARCHITECTED,AZURE_SECURITY_BENCHMARK,GCP_SECURITY_FRAMEWORK}]
                [--account ACCOUNT] [--check-compliance] [--analyze-costs]
                [--export PATH] [--export-format {json,csv,text}]
```

| Argument | Description |
|----------|-------------|
| `--help` | Show this help message and exit |
| `--demo` | Run built-in demonstration audit |
| `--provider` | Cloud provider to audit (default: `aws`) |
| `--scope` | Audit scope (default: `full`) |
| `--framework` | Compliance framework for `--check-compliance` (default: `CIS`) |
| `--account` | Cloud account ID to target (default: empty string) |
| `--check-compliance` | Check a single compliance framework |
| `--analyze-costs` | Run cost analysis instead of full security audit |
| `--export PATH` | Export last report to a file at the given path |
| `--export-format` | Export format: `json`, `csv`, or `text` (default: `json`) |

---

## Appendix: Agent Behaviour Reference

### Intended Behaviour on Common Inputs

| Command / Method | Expected Behaviour |
|-----------------|--------------------|
| `agent.audit_cloud(provider="aws", scope="security")` | Returns dict with provider, scope, score, findings |
| `agent.audit_cloud(provider="aws", scope="full")` | Returns dict with provider, scope, score, findings |
| `agent.run_full_audit(provider=AWS, scope=FULL, account_id="123")` | Returns AuditReport with score, findings, gaps, recommendations, risks |
| `agent.run_full_audit(provider="aws", scope="compliance")` | Runs security and compliance engines cost engine may still run |
| `agent.check_compliance(framework="CIS")` | Returns dict with compliant status, gaps, percentage |
| `agent.check_compliance(framework="SOC2")` | Returns SOC2 compliance dict |
| `agent.analyze_costs(account="123")` | Returns cost dict with spend, savings, recommendations |
| `agent.assess_risks()` | Returns list of risk dicts from last audit |
| `agent.assess_risks({"findings": [...]})` | Returns risk dicts from provided findings |
| `agent.export_report(report, path, fmt="json")` | Writes file; returns path |
| `agent.list_audits()` | Returns list of audit summaries from this session |
| `agent.clear_cache()` | Clears in-memory cache |
| `agent.get_status()` | Returns dict with agent status info |
| `python agent.py --demo` | Prints demo banner, audit summary, exports to file |
| `python agent.py --provider gcp` | Runs audit (stub) for GCP |
| `python agent.py --provider nonexistent` | Raises ValueError |
| `python agent.py --scope invalid` | Raises ValueError |
| `python agent.py --check-compliance --framework BOGUS` | Raises ValueError |
| `python agent.py --export /tmp/r.json` | Exports to /tmp/r.json in JSON format |

### Failure Mode Reference

| Failure Mode | Trigger | Behaviour |
|-------------|---------|-----------|
| Missing provider | `--provider nonexistent` | `ValueError` |
| Invalid scope | `--scope invalid` | `ValueError` |
| Unknown framework | `--framework bogus` | `ValueError` |
| No client for provider | Provider stub not implemented | `ValueError` |
| Cache miss | First run or expired key | Proceed normally |
| Cache failure | Memory full | Log warning; degrade gracefully |
| Notification failure | Slack down, SMTP unreachable | Log error; audit still succeeds |
| File write error | No permissions on export path | `OSError` propagates |
| Missing regions | Empty `Config.providers[].regions` | Falls back to detectable default pattern |

---

## Appendix: Data Model Usage Guide

### AuditFinding

Use `AuditFinding.to_dict()` to serialise. Key fields:
- `finding_id`: UUID unique to this finding
- `severity`: One of `critical`, `high`, `medium`, `low`, `info`
- `category`: One of the `RiskCategory` values
- `evidence`: Dict containing the control name and config snapshot
- `references`: List of URLs for documentation

### ComplianceGap

Use `ComplianceGap.to_dict()` to serialise. Key fields:
- `framework`: String enum value (e.g. `"CIS"`)
- `control_id`: ID within the framework (e.g. `"1.4"`)
- `priority`: Severity for prioritisation
- `due_date`: When this gap should be closed

### CostRecommendation

Use `CostRecommendation.to_dict()` to serialise. Key fields:
- `savings_percentage`: Auto-calculated from current and projected costs
- `confidence`: `high`, `medium`, or `low`
- `risk_level`: Risk of implementing the recommendation

### RiskRecord

Use `RiskRecord.to_dict()` to serialise. Key fields:
- `risk_score`: Calculated as `SEVERITY_WEIGHT × LIKELIHOOD × IMPACT`
- `status`: `accepted`, `open`, or `critical`
- `residual_risk`: Risk level after mitigation

---

## Appendix: Agent Behaviour in Strict Mode

When `ComplianceConfig.strict_mode = True`:

- Any non-compliant control generates a `ComplianceGap` with `current_status="non_compliant"`.
- The agent does not automatically fail; strict mode is a signal to CI/CD pipelines.
- Consumers should interpret a non-empty `gaps` list as a failure condition.
- Example CI check:
  ```python
  if any(gap["priority"] == "critical" for gap in result["gaps"]):
      sys.exit(1)
  ```

---

## Appendix: Encrypted Backup Workflow Example

Back up audit reports using any encrypted backup tool. Duplicati is referenced
here as an example; any encrypted backup solution is appropriate.

1. After each audit, copy reports to the backup source directory.
2. Configure your backup tool to encrypt using AES-256 with a strong passphrase.
3. Store backup passphrase offline in a secrets manager or password manager.
4. Test restore procedures quarterly.

Example command using Duplicati's command-line backup (if installed):
```bash
# Placeholder: replace with actual Duplicati backup command if installed.
duplicati-cli backup <source-dir> <backup-target>/<hostname>_<date>.duplicati
```

---

## Appendix: Performance Tuning Parameters

| Parameter | Where Set | Recommended Value | Effect |
|-----------|-----------|-------------------|--------|
| `cache_ttl_seconds` | `Config.cache_ttl_seconds` | 3600 (1 hour) | Longer = fewer re-audits |
| `parallel_checks` | `Config.parallel_checks` | 4 | Future async parallelism |
| `cost.lookback_days` | `CostConfig.lookback_days` | 30 | Shorter = faster cost analysis |
| `risk.max_results` | `RiskConfig.max_results` | 50-100 | Smaller = faster risk assessment |
| `region` list | `ProviderConfig.regions` | Active regions only | Fewer regions = faster scan |

---

## Appendix: Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2024-01 | Multi-engine architecture, data models, CLI, cache, notifications |
| 1.0.0 | 2023-06 | Initial release: basic security checks for AWS |

---

## Appendix: License

MIT License

Copyright (c) 2024 Cloud Audit Agent Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
