# CloudAudit Agent Architecture

## Overview

The CloudAudit Agent is a modular, extensible auditing platform designed to
evaluate cloud environments for security posture, compliance adherence, cost
efficiency, and risk exposure. It supports AWS, Azure, GCP, Oracle Cloud,
IBM Cloud, and Alibaba Cloud, both individually and in multi/hybrid
configurations.

This document details the internal architecture, data flows, component
responsibilities, extension points, deployment profiles, and operational
considerations for the CloudAudit Agent.

---

## 1. Design Principles

| Principle | Description |
|-----------|-------------|
| **Modularity** | Each concern (security, compliance, cost, risk) is encapsulated in its own engine class. |
| **Extensibility** | New cloud providers are added by subclassing `BaseCloudClient`. New frameworks are added by extending framework evaluation methods. |
| **Testability** | Pure functions and injectable clients make unit-testing straightforward. |
| **Observability** | Structured logging, caching, and notification channels provide full visibility. |
| **Idempotency** | Cached report keys ensure repeated runs are fast and consistent. |
| **Separation of Concerns** | Data models, business logic, transport, and presentation are kept in distinct layers. |
| **Least Privilege** | The agent operates with minimal required permissions. |
| **Explicit over Implicit** | All configuration is explicit; no hidden defaults beyond safe fallbacks. |
| **Immutable Results** | Audit reports are read-only after creation to prevent tampering. |
| **Fail-Safe Defaults** | Unsafe defaults are avoided; strict mode enables CI gating. |

---

## 2. System Components

```
┌─────────────────────────────────────────────────────────────────────┐
│                      CloudAuditAgent (Orchestrator)                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────┐  ┌──────────────────┐  ┌───────────────────┐  │
│  │ SecurityCheck   │  │ ComplianceCheck  │  │ CostAnalysis      │  │
│  │ Engine          │  │ Engine           │  │ Engine            │  │
│  └────────┬────────┘  └────────┬─────────┘  └────────┬──────────┘  │
│           │                     │                      │              │
│           ▼                     ▼                      ▼              │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    BaseCloudClient (Abstraction)               │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │    │
│  │  │ AWS Client   │  │ Azure Client │  │ GCP Client (stub)│   │    │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────┘    │
│           │                     │                      │              │
│           ▼                     ▼                      ▼              │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  RiskAssessmentEngine   │   AuditCache   │   ReportFormatter │   │
│  │  NotificationChannels   │   Config       │   Data Models      │   │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.1 Core Layer

| Component | Responsibility |
|-----------|----------------|
| `CloudAuditAgent` | Top-level orchestrator. Accepts user requests, initialises engines, caches results, and dispatches notifications. |
| `Config` | Hierarchical data-class configuration (`ProviderConfig`, `ComplianceConfig`, `CostConfig`, `RiskConfig`). Validated at startup. |

### 2.2 Data Layer

| Model | Purpose |
|-------|---------|
| `AuditFinding` | A single security or operational defect discovered during an audit. |
| `ComplianceGap` | A control in a compliance framework that is not satisfied. |
| `CostRecommendation` | A concrete dollar-value recommendation for reducing cloud spend. |
| `RiskRecord` | An assessed risk derived from findings, with likelihood, impact, and mitigation. |
| `AuditReport` | The complete output of `run_full_audit`, aggregating findings, gaps, recommendations, and risks. |

### 2.3 Engine Layer

| Engine | Input | Output |
|--------|-------|--------|
| `SecurityCheckEngine` | `BaseCloudClient` + resource types | `List[AuditFinding]` |
| `ComplianceCheckEngine` | `BaseCloudClient` + framework | `List[ComplianceGap]` |
| `CostAnalysisEngine` | `BaseCloudClient` + `CostConfig` | `List[CostRecommendation]` |
| `RiskAssessmentEngine` | `List[AuditFinding]` + `RiskConfig` | `List[RiskRecord]` |

### 2.4 Client Layer

| Class | Role |
|-------|------|
| `BaseCloudClient` | Abstract interface defining `authenticate`, `list_resources`, `get_config`, `get_compliance_status`, `get_cost_data`. |
| `AWSSimulatedClient` | In-memory simulated AWS backend for testing and demos. |

### 2.5 Infrastructure Layer

| Component | Role |
|-----------|------|
| `AuditCache` | In-memory key/value store with TTL-based expiry for deduplication and speed. |
| `NotificationChannel` hierarchy | Pluggable notification dispatch (`ConsoleNotificationChannel`, `SlackNotificationChannel`, `EmailNotificationChannel`). |
| `ReportFormatter` | Converts `AuditReport` into JSON, CSV, or plain-text formats. |

---

## 3. Data Flow

### 3.1 Full Audit Flow

```
 User Request
      │
      ▼
 CloudAuditAgent.run_full_audit(provider, scope, account_id)
      │
      ├── Cache Key Generation  ─────────────────────┐
      │   key = "full_audit:{provider}:{scope}:{id}" │
      │                                               ▼
      │              ┌───────────────────┐   Cache Hit? ───► Return Cached Report
      │              │  AuditCache.get() │
      │              └────────┬──────────┘
      │                       │ Miss
      ▼                       ▼
 BaseCloudClient ──► list_resources(resource_types)
      │
      ├── SecurityCheckEngine.run() ──► List[AuditFinding]
      │
      ├── ComplianceCheckEngine.evaluate() ──► List[ComplianceGap] per framework
      │
      ├── CostAnalysisEngine.analyze() ──► List[CostRecommendation]
      │
      └── RiskAssessmentEngine.assess() ──► List[RiskRecord]
                │
                ▼
         AuditReport assembled
         score = compute_score(findings)
         completed_at = now
                │
                ▼
         AuditCache.set(key, report)
                │
                ▼
         NotificationChannels.send(subject, message)
                │
                ▼
         Return AuditReport
```

### 3.2 Lightweight Audit Flow

```
 CloudAuditAgent.audit_cloud(provider, scope)
      │
      └── SecurityCheckEngine.run()
              │
              ▼
         score = compute_score(findings)
              │
              ▼
         return {
             "provider": ...,
             "scope": ...,
             "score": ...,
             "findings_count": ...,
             "findings": [...]
         }
```

### 3.3 Compliance Check Flow

```
 CloudAuditAgent.check_compliance(framework)
      │
      ├── client.get_compliance_status(framework)  ◄── Provider API
      │
      └── ComplianceCheckEngine.evaluate(framework)
              │
              ▼
         ComplianceGap list
              │
              ▼
         return {
             "framework": ...,
             "compliant": bool,
             "gaps": [...],
             "compliance_percentage": ...,
             "remediation_priority": [...]
         }
```

### 3.4 Cost Analysis Flow

```
 CloudAuditAgent.analyze_costs(account)
      │
      ├── client.get_cost_data(lookback_days)  ◄── Provider API
      │
      └── CostAnalysisEngine.analyze()
              │
              ├── _check_idle_resources()
              ├── _check_overprovisioned_resources()
              ├── _check_reserved_instance_opportunities()
              └── _check_storage_tier_optimization()
                      │
                      ▼
                 return {
                     "account": ...,
                     "spend": ...,
                     "recommendations": [...],
                     "total_potential_savings": ...,
                     "savings_percentage": ...
                 }
```

### 3.5 Risk Assessment Flow

```
 CloudAuditAgent.assess_risks(cloud_config)
      │
      ├── Source: cloud_config["findings"] OR last AuditReport
      │
      └── RiskAssessmentEngine.assess(findings)
              │
              ├── Filter by min_severity
              ├── Estimate likelihood and impact per finding
              ├── Compute risk_score = severity × likelihood × impact
              ├── Derive residual risk and status (open / accepted / critical)
              └── Sort descending if auto_prioritize
                      │
                      ▼
                 return List[RiskRecord dicts]
```

### 3.6 Notification Flow

```
 Audit Complete
      │
      ▼
 ComplianceConfig.notify_on_gap == True?
      │
      ├── No  ──► Skip notifications
      │
      └── Yes ──► For each NotificationChannel:
                      │
                      ├── ConsoleNotificationChannel.send() ──► logger.info()
                      ├── SlackNotificationChannel.send() ──► webhook POST (simulated)
                      └── EmailNotificationChannel.send() ──► SMTP send (simulated)
                              │
                              ├── Success ──► continue
                              └── Exception ──► logger.error(); continue
```

---

## 4. Key Component Details

### 4.1 SecurityCheckEngine

Responsible for inspecting cloud resource configurations and producing
`AuditFinding` objects.

**Built-in checks:**

| Category | Resources | Checks |
|----------|-----------|--------|
| Public Access | S3, RDS, EKS | `block_public_acls`, `block_public_policy`, `ignore_public_acls`, `restrict_public_buckets`, `publicly_accessible`, `endpoint_public_access` |
| Encryption | S3, RDS, EC2 | `encryption`, `storage_encrypted`, `encrypted_volumes` |
| Logging | S3, EKS | `logging`, API/audit/authenticator logs |
| IAM Exposure | IAM User | `mfa_enabled`, active access key count |
| Versioning | S3 | `versioning` |

**Severity mapping for security checks:**

| Condition | Severity |
|-----------|----------|
| Public access open | HIGH |
| Encryption disabled | HIGH |
| MFA disabled | CRITICAL |
| Logging disabled | MEDIUM |
| Versioning disabled | MEDIUM |

**Extensibility:** Add new resource types by extending `PUBLIC_ACCESS_CHECKS`
or `ENCRYPTION_CHECKS` dictionaries, or by adding new `_check_*` methods.

### 4.2 ComplianceCheckEngine

Evaluates resource configurations against regulatory and industry standards.

**Supported frameworks (built-in):**

| Framework | Controls Simulated |
|-----------|-------------------|
| CIS AWS Foundations | 11 controls (1.1, 1.2, 1.4, 1.5, 1.10, 2.1.1–2.1.3, 2.1.5, 4.1, 5.1) |
| SOC 2 | CC6.1 (Logical Access), CC6.6 (Network Boundary), CC7.2 (Monitoring) |
| PCI DSS 4.0 | 3.4 (PAN Encryption), 6.5 (Vulnerability Management) |
| HIPAA | 164.312 (Access Controls), 164.312(a)(2)(i) (Unique User ID) |
| GDPR | Art. 5 (Data Minimisation), Art. 32 (Security of Processing) |

**Remediation Map:** Each CIS control ID maps to a specific remediation string
stored in `_remediation_for_cis`.

**Framework evaluation priority order:**
1. CIS (fastest, AWS-specific)
2. SOC 2 (industry-standard trust criteria)
3. PCI DSS (payment card specific)
4. HIPAA (healthcare specific)
5. GDPR (EU data privacy)

### 4.3 CostAnalysisEngine

Runs heuristic and pattern-based cost checks against the provider's cost API.

| Check | Logic | Potential Savings |
|-------|-------|------------------|
| Idle Resources | Flag resources with low utilisation (simulated) | ~20% of EC2 spend |
| Over-provisioned | CPU/memory headroom exceeds 60% | ~10.5% of EC2 spend |
| Reserved Instances | Steady-state workloads >30 days | ~25% of annual compute |
| Storage Tiering | Objects not modified >90 days | ~15% of S3 spend |

**Cost analysis output fields per recommendation:**

| Field | Description |
|-------|-------------|
| `resource_id` | Identifier of the target collection |
| `resource_type` | EC2 / RDS / S3 / Reserved-Instances |
| `current_monthly_cost` | Baseline monthly spend |
| `projected_monthly_savings` | Expected savings after implementation |
| `savings_percentage` | Calculated: `savings / current × 100` |
| `recommendation` | Human-readable action description |
| `confidence` | `high` / `medium` / `low` |
| `risk_level` | Implementation risk |
| `provider` | Cloud provider |
| `region` | Target region |

### 4.4 RiskAssessmentEngine

Transforms raw findings into `RiskRecord` objects with quantitative scoring.

**Scoring formula:**
```
risk_score = SEVERITY_WEIGHT(severity) * LIKELIHOOD_WEIGHT(likelihood) * IMPACT_WEIGHT(impact)
```

**Severity weights:** Critical=10, High=7, Medium=4, Low=2, Info=1  
**Likelihood / Impact weights:** High=3, Medium=2, Low=1

**Status derivation:**

| Residual Score | Status |
|---------------|--------|
| <= 4 | `accepted` (residual risk is tolerable) |
| 5 to 14 | `open` (requires remediation) |
| >= 15 | `critical` (immediate action required) |

**Default mitigation strategies by category:**
- Data Breach: Enable encryption at rest and in transit; review access controls.
- Misconfiguration: Apply recommended configuration change and validate with re-scan.
- Access Control: Enforce least privilege; enable MFA; review IAM policies.
- Encryption: Enable encryption; rotate keys; enforce TLS 1.2+.
- Network Exposure: Restrict inbound/outbound rules; use private subnets.
- Compliance Violation: Remediate the specific control gap and document evidence.
- Cost Overflow: Set up budgets and alerts; right-size resources.
- Availability: Enable multi-AZ; implement monitoring and auto-scaling.
- Supply Chain: Scan container images; validate artifacts; pin versions.
- Insider Threat: Enable audit logging; implement separation of duties; use JIT access.

### 4.5 ReportFormatter

Transforms `AuditReport` into machine-readable or human-readable formats.

| Format | Method | Use Case |
|--------|--------|----------|
| JSON | `to_json()` | API responses, persisted archives |
| CSV | `to_csv_findings()` | Spreadsheet imports, tracking tickers |
| Text | `to_summary_text()` | Console output, email summaries |

**Text report layout:**
```
═══════════════════════════════════════════════════════════════
CLOUD AUDIT REPORT SUMMARY
═══════════════════════════════════════════════════════════════
Report ID   : <uuid>
Provider    : aws
Scope       : FULL
Account     : 123456789012
Regions     : us-east-1, us-west-2
Started     : 2024-01-15T06:00:00Z
Completed   : 2024-01-15T06:00:12Z
Score       : 85/100

Total Findings : 12
  CRITICAL : 2
  HIGH     : 4
  MEDIUM   : 4
  LOW      : 2
  INFO     : 0

Compliance Gaps:
  CIS: 5 gaps
  SOC2: 1 gap

Cost Recommendations:
  Total potential savings: $3,240.00/month

Risk Summary:
  Open risks: 8
  Critical risks: 2
═══════════════════════════════════════════════════════════════
```

### 4.6 AuditCache

Provides a TTL-based in-memory cache keyed by a deterministic string.

**Cache key format:**
```
full_audit:{provider}:{scope}:{account_id}
```

**Operations:**
- `get(key) -> Optional[Any]` - Retrieve and validate TTL
- `set(key, value)` - Store with current timestamp
- `invalidate(key)` - Remove single entry
- `clear()` - Remove all entries

**Invalidation triggers:**
- Manual: `agent.clear_cache()`
- TTL expiry: automatic on next `get()` call
- New audit: old keys remain until TTL expires

### 4.7 Notification Channels

```
Abstract: NotificationChannel.send(subject, message) -> bool
   ├── ConsoleNotificationChannel   (logs to stdout via logger)
   ├── SlackNotificationChannel     (simulates webhook POST)
   └── EmailNotificationChannel     (simulates SMTP send)
```

Notificatio are dispatched after every `run_full_audit` completes, provided
`ComplianceConfig.notify_on_gap` is `True`.

**Notification payload structure:**
```python
{
    "subject": "Cloud Audit Completed: aws - Score 85",
    "message": "Report ID: <uuid>\nFindings: 12\nCompliance Gaps: 6\nCost Recommendations: 4\n",
    "timestamp": "2024-01-15T06:00:12Z",
    "agent_version": "2.0.0"
}
```

---

## 5. Configuration Reference

### 5.1 Top-level Config

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `providers` | `List[ProviderConfig]` | `[]` | Cloud providers to audit. |
| `compliance` | `ComplianceConfig` | — | Compliance framework settings. |
| `cost` | `CostConfig` | — | Cost analysis settings. |
| `risk` | `RiskConfig` | — | Risk assessment settings. |
| `output_format` | `str` | `"json"` | Preferred export format. |
| `output_path` | `str` | `"./reports"` | Directory for exported reports. |
| `log_level` | `str` | `"INFO"` | Python log level. |
| `parallel_checks` | `int` | `4` | Concurrent check worker count (future parallelism). |
| `cache_enabled` | `bool` | `True` | Enable/disable result caching. |
| `cache_ttl_seconds` | `int` | `3600` | Cache entry time-to-live. |

### 5.2 ProviderConfig

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `provider` | `CloudProvider` | required | Cloud provider enum value. |
| `enabled` | `bool` | `True` | Whether this provider is active. |
| `regions` | `List[str]` | `[]` | Regions to audit. |
| `credentials_file` | `str` | `""` | Path to provider credentials. |
| `profile` | `str` | `"default"` | Named credential profile. |
| `max_retries` | `int` | `3` | API retry limit. |
| `timeout_seconds` | `int` | `30` | Per-request timeout. |

### 5.3 ComplianceConfig

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled_frameworks` | `List[ComplianceFramework]` | `[]` | Frameworks to evaluate. |
| `strict_mode` | `bool` | `False` | Fail on any gap (for CI gates). |
| `auto_remediate` | `bool` | `False` | Attempt automatic remediation (future). |
| `notify_on_gap` | `bool` | `True` | Send notifications after audit. |
| `gap_owner_default` | `str` | `""` | Default owner for gaps. |

### 5.4 CostConfig

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `lookback_days` | `int` | `30` | Historical period for cost data. |
| `currency` | `str` | `"USD"` | Reporting currency. |
| `include_forecast` | `bool` | `True` | Include 3-month cost forecast. |
| `threshold_monthly` | `float` | `1000.0` | Monthly spend threshold for alerts. |
| `anomaly_detection` | `bool` | `True` | Enable statistical anomaly detection. |
| `group_by` | `List[str]` | `["service", "region", "account"]` | Dimensions to group cost data. |

### 5.5 RiskConfig

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled_categories` | `List[RiskCategory]` | `[]` | Risk categories to evaluate. |
| `min_severity` | `SeverityLevel` | `LOW` | Minimum severity to include in report. |
| `max_results` | `int` | `100` | Maximum risk records returned. |
| `auto_prioritize` | `bool` | `True` | Sort risks by severity descending. |
| `mitigation_suggestions` | `bool` | `True` | Include mitigation text in risk records. |

---

## 6. Extension Points

### 6.1 Adding a New Cloud Provider

1. Add a new member to `CloudProvider` enum.
2. Create a subclass of `BaseCloudClient` implementing all abstract methods.
3. Register it in `CloudAuditAgent._build_clients`.

```python
class MyCloudClient(BaseCloudClient):
    def authenticate(self) -> bool: ...
    def list_resources(self, resource_type: str, region: str) -> List[Dict[str, Any]]: ...
    def get_config(self, resource_id: str) -> Dict[str, Any]: ...
    def get_compliance_status(self, framework: ComplianceFramework) -> Dict[str, Any]: ...
    def get_cost_data(self, lookback_days: int) -> Dict[str, Any]: ...
```

### 6.2 Adding a New Compliance Framework

1. Add a new member to `ComplianceFramework` enum.
2. Add an evaluation method in `ComplianceCheckEngine` (e.g. `_evaluate_framex`).
3. Call it from the polymorphic dispatch in `evaluate()`.

### 6.3 Adding a New Security Check

1. Add resource type entries to `PUBLIC_ACCESS_CHECKS` or `ENCRYPTION_CHECKS`.
2. Or add a new `_check_*` method and call it from `SecurityCheckEngine.run()`.

### 6.4 Adding a New Notification Channel

```python
class PagerDutyNotificationChannel(NotificationChannel):
    def send(self, subject: str, message: str) -> bool:
        # POST to PagerDuty Events API v2
        ...
        return True
```

### 6.5 Adding a New Report Export Format

1. Add a new method to `ReportFormatter` (e.g. `to_yaml()`).
2. Extend the `fmt` parameter handling in `CloudAuditAgent.export_report`.

### 6.6 Custom Risk Scoring

Subclass `RiskAssessmentEngine` and override `_estimate_likelihood_impact()`
and `_default_mitigation()` to implement organisation-specific risk models.

---

## 7. Deployment Profiles

### 7.1 Local Development

```
python agents/cloud-audit/agent.py --demo
```

Runs with `AWSSimulatedClient`. No cloud credentials required.

### 7.2 CI/CD Gate

```yaml
# Example GitHub Actions step
- name: Cloud Compliance Gate
  run: |
    python agents/cloud-audit/agent.py \
      --provider aws \
      --scope full \
      --check-compliance \
      --framework CIS \
      --account ${{ secrets.AWS_ACCOUNT_ID }}
```

Use `ComplianceConfig(strict_mode=True)` to fail on any gap.

### 7.3 Scheduled Production Run (cron / Airflow)

```
0 6 * * 1  cd /opt/cloud-audit && python agent.py --provider aws --scope full --account 123456789012 --export /var/reports/audit-$(date +\%F).json
```

### 7.4 Container Deployment

```dockerfile
FROM python:3.11-slim
COPY agents/cloud-audit/agent.py /app/agent.py
COPY agents/cloud-audit/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
WORKDIR /app
CMD ["python", "agent.py", "--demo"]
```

### 7.5 Kubernetes Deployment

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: cloud-audit-daily
spec:
  schedule: "0 6 * * 1-5"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: cloud-audit
              image: myrepo/cloud-audit:latest
              command: ["python", "agent.py", "--demo", "--export", "/reports/audit.json"]
              volumeMounts:
                - name: reports
                  mountPath: /reports
          restartPolicy: OnFailure
          volumes:
            - name: reports
              persistentVolumeClaim:
                claimName: audit-reports-pvc
```

### 7.6 Serverless (AWS Lambda)

```python
# lambda_handler.py
import json
from agents.cloud_audit.agent import CloudAuditAgent, Config

def lambda_handler(event, context):
    config = Config(
        providers=[ProviderConfig(provider=CloudProvider.AWS, regions=["us-east-1"])],
        compliance=ComplianceConfig(enabled_frameworks=[ComplianceFramework.CIS]),
    )
    agent = CloudAuditAgent(config=config)
    report = agent.run_full_audit()
    return {
        "statusCode": 200,
        "body": report.to_json(),
        "headers": {"Content-Type": "application/json"},
    }
```

---

## 8. Performance Considerations

| Metric | Current (Simulated) | Production Target |
|--------|---------------------|-------------------|
| Security scan (per region) | <50 ms | <5 s per 10k resources |
| Compliance evaluation (CIS) | <20 ms | <30 s |
| Cost analysis | <30 ms | <60 s (cost API latency) |
| Risk assessment | <10 ms | <1 s |
| End-to-end full audit | <200 ms | <5 min (large AWS org) |
| Cache round-trip | <1 ms | <1 ms |

**Optimisation techniques:**
- Simple rate limiter inside `BaseCloudClient` (`_respect_rate_limit`).
- In-memory `AuditCache` prevents redundant API calls.
- Future: async client layer using `httpx.AsyncClient` + `asyncio.Semaphore(parallel_checks)`.

### 8.1 Scalability Limits

| Factor | Simulated Limit | Practical Limit |
|--------|-----------------|-----------------|
| Regions per audit | Unlimited (memory) | ~20 per account |
| Resource types per scan | Unlimited | ~50 types |
| Concurrent audits | 1 (single-process) | N (multi-process) |
| Cache entries | Memory bounded | ~10k entries / ~100MB |
| Report size | ~400KB | ~10MB (large orgs) |

---

## 9. Security Considerations

- **Authentication:** Provider clients must authenticate before any data call.
  `AWSSimulatedClient.authenticate()` is called on init in production clients.
- **Authorization:** The agent should run with a least-privilege IAM role scoped to
  read-only access (`ReadOnlyAccess` or equivalent).
- **Secrets Management:** Credentials are loaded from files (`credentials_file`) or
  environment profiles. `Config.validate()` ensures paths are set before running.
- **Data Protection:** Reports may contain sensitive configuration data; export to
  encrypted storage and restrict access via ACLs.
- **Input Validation:** All string inputs are normalised through `_normalize_*`
  helpers before enum conversion to prevent injection attacks.
- **Audit Trail:** `detected_at` and `completed_at` timestamps are UTC ISO-8601.

### 9.1 IAM Policy for Production AWS Deployment

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "CloudAuditReadOnly",
            "Effect": "Allow",
            "Action": [
                "s3:GetBucketLocation", "s3:GetBucketPolicy", "s3:GetBucketAcl",
                "s3:GetBucketLogging", "s3:GetBucketVersioning",
                "s3:GetEncryptionConfiguration",
                "ec2:Describe*",
                "rds:Describe*",
                "iam:Get*", "iam:List*",
                "eks:Describe*", "eks:List*",
                "ce:Get*"
            ],
            "Resource": "*"
        }
    ]
}
```

### 9.2 Credential Rotation

- Use IAM roles with automatic rotation (AWS IAM Role, Azure Managed Identity).
- Avoid embedding credentials in `ProviderConfig.credentials_file` in production.
- Rotate `credentials_file` credentials every 90 days minimum.

### 9.3 Network Isolation

- Run the agent in a dedicated security audit VPC or subnet.
- Restrict outbound traffic to provider API endpoints only.
- Use VPC endpoints (AWS PrivateLink, Azure Private Link) where available.

---

## 10. Error Handling & Resilience

```text
run_full_audit
   ├── ValueError ──► No client / unsupported provider / scope
   │        └──► Propagate to caller with descriptive message
   ├── Client failures
   │        └──► Log via logger.error; continue with partial data if possible
   ├── Cache failures
   │        └──► Log warning; proceed without cache (degraded performance)
   └── Notification failures
            └──► Caught per-channel; does not fail the audit
```

### 10.1 Retry Strategy

| Scenario | Strategy |
|----------|----------|
| Transient API error (5xx) | Exponential backoff, up to `max_retries` |
| Rate limit (429) | Respect `Retry-After` header; delay by 2× |
| Auth failure (401/403) | No retry; alert operator immediately |
| Timeout | Retry once; if persistent, skip resource and log |

### 10.2 Circuit Breaker Pattern (Future)

```
CLOSED (normal) ──► N failures ──► OPEN (skip)
OPEN ──► cooldown period ──► HALF-OPEN (test)
HALF-OPEN ──► success ──► CLOSED
HALF-OPEN ──► failure ──► OPEN
```

---

## 11. Testing Strategy

### 11.1 Unit Tests

- `SecurityCheckEngine` → feed synthetic resources, assert finding count.
- `ComplianceCheckEngine` → assert gap count per framework.
- `CostAnalysisEngine` → inject mock cost data, assert recommendations.
- `RiskAssessmentEngine` → inject findings, assert risk ordering.
- `CloudAuditAgent._normalize_*` → boundary cases and invalid inputs.
- `AuditCache` → TTL expiry, `get`/`set`/`invalidate`/`clear`.

### 11.2 Integration Tests

- `CloudAuditAgent.run_full_audit` end-to-end with `AWSSimulatedClient`.
- Report export round-trip: `export_report` → read file → parse JSON.
- Notification channel dispatch.

### 11.3 Example Unit Test

```python
def test_security_check_engine_s3_public_access():
    client = AWSSimulatedClient(ProviderConfig(provider=CloudProvider.AWS, regions=["us-east-1"]))
    client.authenticate()
    engine = SecurityCheckEngine(client)
    findings = engine.run(["s3"])
    public_findings = [f for f in findings if "public" in f.title.lower()]
    assert len(public_findings) >= 1
```

---

## 12. Glossary

| Term | Definition |
|------|-----------|
| **Finding** | A specific security or operational issue discovered during an audit. |
| **Gap** | A compliance control that the environment does not satisfy. |
| **Recommendation** | A cost-optimisation suggestion with quantified savings. |
| **Risk** | A finding elevated to risk status with likelihood, impact, and mitigation. |
| **Scope** | The boundaries of the audit (full, security, cost, etc.). |
| **Engine** | A pluggable component that performs one dimension of analysis. |
| **Client** | An abstraction over a cloud provider's API surface. |
| **Cache Key** | A deterministic string used to store and retrieve cached reports. |
| **Report** | The consolidated output of an audit run (`AuditReport`). |
| **Remediation** | The suggested action to close a finding or compliance gap. |
| **Framework** | A named set of compliance controls (CIS, SOC2, PCI DSS, etc.). |

---

## 13. Future Roadmap

| Milestone | Feature | Status |
|-----------|---------|--------|
| v2.1 | Real AWS (boto3) and Azure SDK clients | Planned |
| v2.2 | Parallel async engine execution | Planned |
| v2.3 | Terraform / Pulumi configuration import | Planned |
| v2.4 | Open Policy Agent (OPA) integration | Planned |
| v2.5 | Multi-cloud consolidated reporting | Planned |
| v2.6 | Jira / ServiceNow ticket creation from gaps | Planned |
| v2.7 | ML-based anomaly detection for costs | Planned |
| v2.8 | REST API wrapper (FastAPI) | Planned |

---

## 14. Interface Contracts

### 14.1 BaseCloudClient Abstract Interface

Every cloud provider client MUST implement the following interface:

```python
class BaseCloudClient(ABC):
    @abstractmethod
    def authenticate(self) -> bool:
        """Authenticate with the cloud provider.
        Returns True on success, False on failure.
        Should be idempotent.
        """

    @abstractmethod
    def list_resources(self, resource_type: str, region: str) -> List[Dict[str, Any]]:
        """List all resources of the given type in the given region.
        Returns a list of dicts, each with at least:
            - resource_id: str
            - resource_type: str
            - region: str
            - account_id: str (if available)
            - configuration: Dict[str, Any]
        """

    @abstractmethod
    def get_config(self, resource_id: str) -> Dict[str, Any]:
        """Get the full configuration for a specific resource.
        Returns a dict of configuration key-value pairs.
        """

    @abstractmethod
    def get_compliance_status(
        self, framework: ComplianceFramework
    ) -> Dict[str, Any]:
        """Return compliance posture for a given framework.
        Must return at least:
            - framework: str (framework value)
            - compliant_controls: int
            - non_compliant_controls: int
            - total_controls: int
            - compliance_percentage: float
        """

    @abstractmethod
    def get_cost_data(self, lookback_days: int) -> Dict[str, Any]:
        """Return cost data for the lookback period.
        Must return at least:
            - total_cost: float
            - currency: str
            - lookback_days: int
            - services: Dict[str, Dict] (service_name -> {cost, trend})
        """
```

### 14.2 CloudAuditAgent Public Interface Contract

```python
class CloudAuditAgent:
    def __init__(self, config: Optional[Config] = None) -> None: ...

    def get_status(self) -> Dict[str, Any]: ...

    def run_full_audit(
        self,
        provider: Optional[Union[CloudProvider, str]] = None,
        scope: Optional[Union[AuditScope, str]] = None,
        account_id: str = "",
        regions: Optional[List[str]] = None,
    ) -> AuditReport: ...

    def audit_cloud(
        self,
        provider: Optional[Union[CloudProvider, str]] = None,
        scope: Optional[Union[AuditScope, str]] = None,
    ) -> Dict[str, Any]: ...

    def check_compliance(
        self, framework: Union[ComplianceFramework, str]
    ) -> Dict[str, Any]: ...

    def analyze_costs(self, account: str = "") -> Dict[str, Any]: ...

    def assess_risks(
        self, cloud_config: Optional[Dict] = None
    ) -> List[Dict]: ...

    def export_report(
        self, report: AuditReport, path: str, fmt: str = "json"
    ) -> str: ...

    def list_audits(self) -> List[Dict[str, Any]]: ...

    def clear_cache(self) -> None: ...
```

### 14.3 NotificationChannel Contract

```python
class NotificationChannel(ABC):
    @abstractmethod
    def send(self, subject: str, message: str) -> bool:
        """Send a notification.
        Parameters:
            subject: Short summary for the notification header.
            message: Full message body (may include report summary).
        Returns:
            True if the notification was sent successfully.
            False if sending failed (but should not raise).
        """
```

---

## 15. Operational Runbooks

### 15.1 Daily Audit Run

1. SSH or kubectl exec into the audit runner.
2. Verify the scheduler or cron job ran successfully.
3. Check `/var/log/cloud-audit/cron.log` for errors.
4. Review the exported report at `/var/reports/audit-YYYY-MM-DD.json`.
5. Verify Slack/email notifications were received.
6. If score dropped >10 points from previous day, escalate to SOC.

### 15.2 Compliance Quarterly Review

1. Schedule a 2-hour window with the compliance team.
2. Run `check_compliance` for each framework in scope.
3. Export CSVs for each framework.
4. Upload spreadsheets to the compliance management tool.
5. Assign gap owners based on `gap_owner_default`.
6. Set `due_date` for critical gaps to the next sprint.

### 15.3 Incident Response Trigger

If `run_full_audit` returns `overall_score < 50` or any finding has
`severity == critical`:

1. Immediately escalate to the on-call security engineer.
2. Freeze the report as evidence (`sha256sum` on the JSON file).
3. Open a PagerDuty incident via the PagerDuty notification channel.
4. Begin containment: restrict IAM permissions, bucket ACLs, SG rules.
5. Schedule a post-mortem within 24 hours.

### 15.4 Cost Spike Alert Response

If `analyze_costs` returns `savings_percentage < 5` or total spend exceeds
`CostConfig.threshold_monthly`:

1. Notify the FinOps team via Slack channel.
2. Pull the detailed service breakdown from the report.
3. Identify the top 3 cost drivers.
4. Schedule a right-sizing meeting with the owning team.
5. Set budgets and alerts in the cloud provider's cost management console.

---

## 16. Appendix: Complete enums.py Reference

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

## 17. Appendix: Complete Data Model DDL (Conceptual)

If the audit results were stored in a relational database, the schema would look like:

```sql
CREATE TABLE audit_reports (
    report_id VARCHAR(36) PRIMARY KEY,
    provider VARCHAR(32) NOT NULL,
    scope VARCHAR(32) NOT NULL,
    account_id VARCHAR(64),
    regions JSON,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    overall_score INTEGER,
    metadata JSON
);

CREATE TABLE audit_findings (
    finding_id VARCHAR(36) PRIMARY KEY,
    report_id VARCHAR(36) REFERENCES audit_reports(report_id),
    title TEXT NOT NULL,
    description TEXT,
    severity VARCHAR(16) NOT NULL,
    category VARCHAR(32) NOT NULL,
    provider VARCHAR(32),
    resource_id VARCHAR(256),
    resource_type VARCHAR(64),
    region VARCHAR(32),
    account_id VARCHAR(64),
    remediation TEXT,
    evidence JSON,
    references JSON,
    detected_at TIMESTAMP NOT NULL
);

CREATE TABLE compliance_gaps (
    gap_id VARCHAR(36) PRIMARY KEY,
    report_id VARCHAR(36) REFERENCES audit_reports(report_id),
    framework VARCHAR(64) NOT NULL,
    control_id VARCHAR(32),
    control_name TEXT,
    description TEXT,
    current_status VARCHAR(32),
    recommended_action TEXT,
    priority VARCHAR(16),
    owner VARCHAR(256),
    due_date TIMESTAMP,
    evidence_url TEXT
);

CREATE TABLE cost_recommendations (
    reco_id VARCHAR(36) PRIMARY KEY,
    report_id VARCHAR(36) REFERENCES audit_reports(report_id),
    resource_id VARCHAR(256),
    resource_type VARCHAR(64),
    current_monthly_cost DECIMAL(12,2),
    projected_monthly_savings DECIMAL(12,2),
    recommendation TEXT,
    confidence VARCHAR(16),
    provider VARCHAR(32),
    region VARCHAR(32),
    risk_level VARCHAR(16)
);

CREATE TABLE risk_records (
    risk_id VARCHAR(36) PRIMARY KEY,
    report_id VARCHAR(36) REFERENCES audit_reports(report_id),
    title TEXT NOT NULL,
    description TEXT,
    category VARCHAR(32),
    severity VARCHAR(16),
    likelihood VARCHAR(16),
    impact VARCHAR(16),
    mitigation TEXT,
    residual_risk VARCHAR(16),
    owner VARCHAR(256),
    status VARCHAR(32),
    detected_at TIMESTAMP NOT NULL
);
```

---

## 18. Appendix: Glossary

| Term | Definition |
|------|-----------|
| **Finding** | A specific security or operational issue discovered during an audit. |
| **Gap** | A compliance control that the environment does not satisfy. |
| **Recommendation** | A cost-optimisation suggestion with quantified savings. |
| **Risk** | A finding elevated to risk status with likelihood, impact, and mitigation. |
| **Scope** | The boundaries of the audit (full, security, cost, etc.). |
| **Engine** | A pluggable component that performs one dimension of analysis. |
| **Client** | An abstraction over a cloud provider's API surface. |
| **Cache Key** | A deterministic string used to store and retrieve cached reports. |
| **Report** | The consolidated output of an audit run (`AuditReport`). |
| **Remediation** | The suggested action to close a finding or compliance gap. |
| **Framework** | A named set of compliance controls (CIS, SOC2, PCI DSS, etc.). |
| **Scope** | An enum value defining the boundaries of the audit. |
| **TTL** | Time-to-live of a cached entry, in seconds. |
| **Risk Score** | Numerical score = severity × likelihood × impact. |
| **Residual Risk** | Risk remaining after planned mitigation is applied. |

---

## 19. Appendix: Change Log

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2024-01 | Multi-engine architecture, data models, CLI, cache, notifications |
| 1.0.0 | 2023-06 | Initial release: basic security and compliance checks |

---

## 20. Data Retention and Archival Policy

Audit reports and findings should be retained according to organizational data governance policies and regulatory requirements.

| Regulation | Minimum Retention | Recommended Storage |
|------------|-------------------|---------------------|
| SOC 2 | 1 year | Encrypted object storage |
| PCI DSS | 1 year | Immutable backup with checksums |
| HIPAA | 6 years | Encrypted, access-controlled archive |
| GDPR | Varies by article | Encrypted with right-to-erasure workflow |
| ISO 27001 | 3 years | Write-once-read-many (WORM) storage |

**Retention workflow:**
1. After each audit, the `export_report` method writes to the configured output path.
2. A scheduled archival job (e.g. cron) copies reports to long-term storage.
3. Reports are checksummed (SHA-256) on ingestion to detect tampering.
4. Old reports beyond the retention window are purged by the archival job.

**Archival command example:**
```bash
find /var/reports/ -name "audit-*.json" -mtime +30 -exec gpg --symmetric --cipher-algo AES256 -o /archive/{} \;
```
