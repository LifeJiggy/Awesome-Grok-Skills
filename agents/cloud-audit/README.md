# CloudAudit Agent

Cloud Audit Agent - Cloud Security and Compliance Audits.

A production-grade, extensible agent for auditing cloud environments across
multiple providers (AWS, Azure, GCP, Oracle, IBM Cloud, Alibaba Cloud).
Performs security scans, regulatory compliance checks, cost-optimisation
analysis, and quantitative risk assessment.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Run the Agent](#run-the-agent)
6. [CLI Reference](#cli-reference)
7. [API Reference](#api-reference)
8. [Configuration Guide](#configuration-guide)
9. [Provider Setup](#provider-setup)
10. [Compliance Frameworks](#compliance-frameworks)
11. [Export Formats](#export-formats)
12. [Examples](#examples)
13. [Troubleshooting](#troubleshooting)
14. [Contributing](#contributing)
15. [License](#license)
16. [Files](#files)

---

## Overview

CloudAudit Agent automates the repetitive, tedious, and error-prone parts of cloud
governance. Instead of manually clicking through cloud consoles, RunCasting IAM
policies, and cross-referencing spreadsheet checklists, security teams can invoke
the agent to produce structured, repeatable, and auditable outputs.

**What it does:**
- Scans cloud resources for misconfigurations and security weaknesses
- Evaluates compliance against SOC 2, PCI DSS, HIPAA, GDPR, CIS, NIST, ISO 27001, and more
- Analyses cloud spend and recommends cost optimisations worth thousands of dollars
- Prioritises risks with a quantitative scoring model
- Notifies stakeholders via console, Slack, or email
- Exports reports in JSON, CSV, or human-readable text

**Who it is for:**
- Cloud Security Engineers
- DevSecOps Engineers
- Compliance Officers (SOC 2, PCI, HIPAA, GDPR)
- FinOps / Cloud Finance Practitioners
- DevOps Engineers and Platform Teams
- CISOs and Security Architects

**What's New in v2.0:**
- Multi-engine architecture: Security, Compliance, Cost, Risk in one run
- `AuditFinding`, `ComplianceGap`, `CostRecommendation`, `RiskRecord` data models
- `AuditCache` with TTL-based expiry for fast repeated runs
- Pluggable notification channels
- `ReportFormatter` with JSON, CSV, and Text output
- CLI with `argparse` for full scriptability
- Simulated AWS client for zero-credential demos and testing

---

## Features

| Feature | Description | Output |
|---------|-------------|--------|
| Security Audits | Multi-resource, multi-region security scans | `List[AuditFinding]` |
| Compliance Checks | Automated evaluation of regulatory frameworks | `List[ComplianceGap]` |
| Cost Analysis | Spend analysis with RI / Right-sizing / Tiering recs | `List[CostRecommendation]` |
| Risk Assessment | Likelihood × Impact scoring with prioritised risks | `List[RiskRecord]` |
| Caching | TTL-based in-memory cache to avoid redundant scans | `AuditCache` |
| Notifications | Console, Slack, and email channels | `NotificationChannel` |
| Exports | JSON, CSV, Text | `ReportFormatter` |
| Multi-cloud | Single agent for AWS, Azure, GCP, Oracle, IBM, Alibaba | `CloudProvider` enum |
| CLI | Full-featured command-line interface | `argparse` |

---

## Installation

### Prerequisites

- Python 3.9+
- `pip` or `pipx` for installation
- (Optional) Cloud provider credentials configured locally

### Install from Source

```bash
git clone <repository-url>
cd awsome-grok-skills
pip install -e agents/cloud-audit
```

### Install Dependencies

```bash
pip install -r agents/cloud-audit/requirements.txt
```

### Encrypted Backups with Duplicati

CloudAudit reports should be backed up to a secure, encrypted off-site location.
[Duplicati](https://www.duplicati.com/) is a free, open-source backup client that
stores encrypted, incremental, compressed backups on cloud storage (local disk,
FTP, SSH, WebDAV, cloud object storage, and more). **Duplicati provides AES-256
encryption**, so your backups are confidential. Passwords and keys are never
sent to storage targets.

Set up a Duplicati backup job:
- Choose the reports directory (e.g. `./reports` or Duplicati's "Add files" path).
- Under "General", set a **strong passphrase** and choose **AES-256 encryption**.
- Configure your storage destination (local path, FTP, SFTP, cloud, etc.).
- Schedule and enable "Run directly" or schedule as you prefer.

> **Important:** Store your Duplicati passphrase securely (e.g. in a secrets manager
> or offline). Duplicati support can reset it for you if needed, but encrypted
> backups remain safe as long as the passphrase is not exposed.

### No Additional Dependencies (Standalone)

The `agent.py` file is self-contained and uses only the Python standard library.
You can run it immediately without installing third-party packages:

```bash
python agents/cloud-audit/agent.py --demo
```

---

## Quick Start

### 30-Second Demo

```bash
# Clone repository, then:
python agents/cloud-audit/agent.py --demo
```

This runs a full simulated audit using `AWSSimulatedClient` and prints a
complete summary to stdout, including findings, compliance gaps, cost
recommendations, and risks.

### Python Quick Start

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
        enabled_frameworks=[
            ComplianceFramework.CIS,
            ComplianceFramework.SOC2,
        ]
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

---

## Run the Agent

### As a Script

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

### As a Library

```python
import asyncio
from agents.cloud_audit.agent import CloudAuditAgent, Config

async def main():
    config = Config(
        providers=[
            ProviderConfig(
                provider=CloudProvider.AWS,
                regions=["us-east-1", "eu-west-1"],
            )
        ],
        compliance=ComplianceConfig(
            enabled_frameworks=[ComplianceFramework.CIS]
        ),
        cache_enabled=True,
    )
    agent = CloudAuditAgent(config=config)
    report = agent.run_full_audit(scope=AuditScope.FULL)
    
    # Export to JSON
    agent.export_report(report, "./report.json")
    
    # List previous audits in this session
    audits = agent.list_audits()
    print(audits)
    
    # Clear cache
    agent.clear_cache()

if __name__ == "__main__":
    asyncio.run(main())
```

### Encrypted Backups with Duplicati

After exporting reports, back them up to an encrypted off-site location with
Duplicati (as described in the [installation section](#encrypted-backups-with-duplicati)). Set up a Duplicati backup job
that includes your export directory (for example `./reports`), schedule regular
runs, and keep your passphrase secure.

---

## CLI Reference

```
usage: agent.py [-h] [--demo] [--provider {aws,azure,gcp,oracle,ibm_cloud,alibaba,multi_cloud,hybrid}]
                [--scope {full,security,compliance,cost,network,identity,storage,compute,database,serverless,containers,iam}]
                [--framework {SOC2,PCI_DSS,HIPAA,GDPR,ISO27001,CIS,NIST_CSF,NIST_800_53,FEDRAMP,CCPA,AWS_WELL_ARCHITECTED,AZURE_SECURITY_BENCHMARK,GCP_SECURITY_FRAMEWORK}]
                [--account ACCOUNT] [--check-compliance] [--analyze-costs]
                [--export PATH] [--export-format {json,csv,text}]
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--demo` | `False` | Run the built-in demonstration audit. |
| `--provider` | `aws` | Cloud provider to audit. Choices: `aws`, `azure`, `gcp`, `oracle`, `ibm_cloud`, `alibaba`, `multi_cloud`, `hybrid`. |
| `--scope` | `full` | Audit scope. Choices include `full`, `security`, `compliance`, `cost`, `network`, `identity`, `storage`, `compute`, `database`, `serverless`, `containers`, `iam`. |
| `--framework` | `CIS` | Compliance framework for `--check-compliance`. Choices: `SOC2`, `PCI_DSS`, `HIPAA`, `GDPR`, `ISO27001`, `CIS`, `NIST_CSF`, `NIST_800_53`, `FEDRAMP`, `CCPA`, `AWS_WELL_ARCHITECTED`, `AZURE_SECURITY_BENCHMARK`, `GCP_SECURITY_FRAMEWORK`. |
| `--account` | `""` | Cloud account ID to target. |
| `--check-compliance` | `False` | Run a single compliance framework check. |
| `--analyze-costs` | `False` | Run cost analysis instead of security audit. |
| `--export PATH` | `None` | Export report to a file at `PATH`. |
| `--export-format` | `json` | Export format: `json`, `csv`, or `text`. |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (no critical issues, or no gaps in strict mode) |
| 1 | Failure (invalid input, client error, or compliance gaps in strict mode) |
| 2 | Usage error (missing required arguments) |

---

## API Reference

### CloudAuditAgent

#### `__init__(config: Optional[Config] = None)`

Initialise the agent. If `config` is `None`, a default single-AWS-provider
configuration is used.

**Parameters:**
- `config` (Optional[Config]): Hierarchical agent configuration.

**Raises:**
- `ValueError`: If configuration validation fails after init.

**Returns:** None

#### `get_status() -> Dict[str, Any]`

Return current agent status including version, configured providers, and number
of completed audits.

**Returns:**
```python
{
    "agent": "CloudAuditAgent",
    "version": "2.0.0",
    "configured_providers": ["aws"],
    "initialized_clients": ["<CloudProvider.AWS: 'aws'>"],
    "audits_completed": 0,
    "cache_enabled": True,
    "parallel_checks": 4
}
```

#### `run_full_audit(provider, scope, account_id, regions) -> AuditReport`

Execute a complete audit: security + compliance + cost + risk.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `provider` | `CloudProvider` or `str` | No | First configured provider | Target cloud provider. |
| `scope` | `AuditScope` or `str` | No | `FULL` | Audit scope. |
| `account_id` | `str` | No | `""` | Cloud account identifier. |
| `regions` | `List[str]` | No | From config | Regions to audit. |

**Returns:** `AuditReport` with populated findings, compliance gaps, cost
recommendations, risks, and an overall score.

**Raises:**
- `ValueError`: No client configured for the given provider.

**Side Effects:**
- Writes to cache (if enabled)
- Sends notifications (if `notify_on_gap`)

#### `audit_cloud(provider, scope) -> Dict[str, Any]`

Execute a lightweight security scan.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `provider` | `CloudProvider` or `str` | No | `AWS` | Target cloud provider. |
| `scope` | `AuditScope` or `str` | No | `FULL` | Audit scope. |

**Returns:** Dictionary with `provider`, `scope`, `score`, `findings_count`, and
`findings`.

**Raises:**
- `ValueError`: No client configured.

#### `check_compliance(framework) -> Dict[str, Any]`

Evaluate a single compliance framework.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `framework` | `ComplianceFramework` or `str` | Yes | Framework to evaluate. Accepts enum or string alias. |

**Returns:** Dictionary with `framework`, `compliant`, `gaps`, `compliance_percentage`,
`compliant_controls`, `total_controls`, `remediation_priority`.

**Raises:**
- `ValueError`: Unsupported framework string.

#### `analyze_costs(account) -> Dict[str, Any]`

Run cost analysis.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `account` | `str` | No | `"default"` | Account identifier. |

**Returns:** Dictionary with `account`, `spend`, `currency`, `services`,
`total_current_monthly`, `total_potential_savings`, `savings_percentage`,
`recommendations`.

**Raises:**
- `ValueError`: No cloud client configured.

#### `assess_risks(cloud_config) -> List[Dict]`

Assess risks from provided findings dict or the last completed audit.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `cloud_config` | `Optional[Dict]` | No | `None` | Optional findings dict. If omitted, uses last audit. |

**Returns:** List of `RiskRecord` dicts.

#### `export_report(report, path, fmt) -> str`

Export a report to a file.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `report` | `AuditReport` | required | Report to export. |
| `path` | `str` | required | Destination file path. |
| `fmt` | `str` | `"json"` | Format: `json`, `csv`, or `text`. |

**Returns:** The path to the written file.

**Raises:**
- `OSError`: If the report directory does not exist or is not writable.
- `ValueError`: If fmt is not one of `json`, `csv`, `text`.

**Side Effects:** Creates parent directories if they do not exist.

#### `list_audits() -> List[Dict[str, Any]]`

List summaries of all audits completed in this session.

**Returns:** List of dictionaries with `report_id`, `provider`, `scope`, `score`,
`findings`, `completed_at`.

#### `clear_cache() -> None`

Clear the audit result cache.

**Side Effects:** Removes all cached entries. Subsequent audits will be re-run.

---

## Configuration Guide

The agent is configured using `dataclass`-based configuration objects. A full
configuration example:

```python
from dataclasses import asdict
import json

config = Config(
    providers=[
        ProviderConfig(
            provider=CloudProvider.AWS,
            enabled=True,
            regions=["us-east-1", "us-west-2", "eu-west-1"],
            credentials_file="~/.aws/credentials",
            profile="production",
            max_retries=3,
            timeout_seconds=30,
        ),
        ProviderConfig(
            provider=CloudProvider.AZURE,
            enabled=False,  # enable when Azure client is ready
            regions=["eastus", "westeurope"],
        ),
    ],
    compliance=ComplianceConfig(
        enabled_frameworks=[
            ComplianceFramework.CIS,
            ComplianceFramework.SOC2,
            ComplianceFramework.PCI_DSS,
            ComplianceFramework.HIPAA,
            ComplianceFramework.GDPR,
        ],
        strict_mode=False,
        auto_remediate=False,
        notify_on_gap=True,
        gap_owner_default="cloud-security@example.com",
    ),
    cost=CostConfig(
        lookback_days=30,
        currency="USD",
        include_forecast=True,
        threshold_monthly=1000.0,
        anomaly_detection=True,
        group_by=["service", "region", "account"],
    ),
    risk=RiskConfig(
        enabled_categories=list(RiskCategory),
        min_severity=SeverityLevel.LOW,
        max_results=100,
        auto_prioritize=True,
        mitigation_suggestions=True,
    ),
    output_format="json",
    output_path="./reports",
    log_level="INFO",
    parallel_checks=4,
    cache_enabled=True,
    cache_ttl_seconds=3600,
)

# Validate
errors = config.validate()
if errors:
    raise ValueError(f"Config errors: {errors}")

print(json.dumps(asdict(config), indent=2, default=str))
```

**Configuration fields at a glance:**

| Path | Type | Default | Description |
|------|------|---------|-------------|
| `providers[].provider` | `CloudProvider` | required | Cloud provider enum |
| `providers[].regions` | `List[str]` | `[]` | Regions to audit |
| `compliance.enabled_frameworks` | `List[ComplianceFramework]` | `[]` | Frameworks to evaluate |
| `cost.lookback_days` | `int` | `30` | Cost data lookback window |
| `risk.min_severity` | `SeverityLevel` | `LOW` | Minimum severity to include |
| `cache_ttl_seconds` | `int` | `3600` | Cache time-to-live |

### Configuration Validation Rules

- At least one provider must be configured (or default will be applied).
- Each enabled provider must have at least one region.
- `parallel_checks` must be >= 1.
- `cache_ttl_seconds` must be >= 60.
- `lookback_days` must be between 1 and 365.

---

## Provider Setup

### AWS (Simulated - Ready Now)

No credentials needed for simulated mode. `AWSSimulatedClient` returns
realistic in-memory data structures for S3, EC2, RDS, IAM, and EKS.

```python
from agents.cloud_audit.agent import CloudAuditAgent, CloudProvider

agent = CloudAuditAgent()
result = agent.audit_cloud(provider=CloudProvider.AWS, scope=AuditScope.FULL)
```

#### Simulated AWS Resources Generated

| Resource Type | Count | Notable Configurations |
|---------------|-------|------------------------|
| S3 | 2 | One fully compliant, one with public access disabled |
| EC2 | 2 | One with public IP and unencrypted volumes, one hardened |
| RDS | 1 | Aurora cluster with encryption and multi-AZ |
| IAM | 2 | User without MFA, role with permissions boundary |
| EKS | 1 | Cluster with public/private endpoints and partial logging |

### AWS (Real - Planned v2.1)

```python
# Future: use boto3
class AWSBoto3Client(BaseCloudClient):
    def __init__(self, config: ProviderConfig):
        super().__init__(config)
        import boto3
        self._session = boto3.Session(
            profile_name=config.profile,
            region_name=config.regions[0] if config.regions else "us-east-1",
        )
        self._s3 = self._session.client("s3")
        self._ec2 = self._session.client("ec2")

    def list_resources(self, resource_type, region):
        # Map resource_type to boto3 call
        ...
```

### Azure, GCP, Oracle, IBM, Alibaba

Stub clients are included in the enum. To enable, subclass `BaseCloudClient`
following the AWS pattern and register it in `_build_clients`.

---

## Compliance Frameworks

### CIS AWS Foundations Benchmark

The most widely adopted AWS security benchmark. 11 core controls evaluated:

| Control | Description | Remediation |
|---------|-------------|-------------|
| 1.1 | Avoid root account use | Enforce MFA; delete root access keys |
| 1.2 | MFA enabled for root | Enable virtual MFA |
| 1.4 | No SSH (22) open to 0.0.0.0/0 | Remove unrestricted SG ingress |
| 1.5 | No RDP (3389) open to 0.0.0.0/0 | Remove unrestricted SG ingress |
| 1.10 | No unrestricted HTTPS to 0.0.0.0/0 | Apply WAF / restrict CIDRs |
| 2.1.1 | S3 bucket policy denies HTTP | Enforce HTTPS |
| 2.1.2 | S3 encryption enabled | Enable AES-256 or KMS |
| 2.1.3 | S3 versioning enabled | Enable versioning |
| 2.1.5 | S3 TLS 1.2+ required | Add SSL condition |
| 4.1 | No SG open to 0.0.0.0/0 | Restrict to known IPs |
| 5.1 | No NACL open to 0.0.0.0/0 | Restrict to known IPs |

### SOC 2

Trust service criteria mapped to cloud controls:

| Control | Title | Status Field |
|---------|-------|--------------|
| CC6.1 | Logical Access Controls | Partial → tighten IAM policies |
| CC6.6 | System Boundary Protection | Review network boundary |
| CC7.2 | Incident detection & monitoring | Enable CloudTrail + SIEM |

### PCI DSS 4.0

| Control | Title |
|---------|-------|
| 3.4 | PAN Storage Encryption |
| 6.5 | Vulnerability Management |

### HIPAA

| Control | Title |
|---------|-------|
| 164.312 | Access Controls |
| 164.312(a)(2)(i) | Unique User Identification |

### GDPR

| Article | Principle |
|---------|-----------|
| Art. 5 | Data Minimisation |
| Art. 32 | Security of Processing |

---

## Export Formats

### JSON Export

Best for: APIs, archives, programmatic processing, integration with analytics.

```bash
agent.export_report(report, "./audit.json", fmt="json")
```

### CSV Export

Best for: spreadsheets, ticket tracking, importing into Jira / ServiceNow / Excel.

Includes columns:
`finding_id`, `severity`, `title`, `resource_id`, `resource_type`, `region`,
`account_id`, `remediation`

```bash
agent.export_report(report, "./audit_findings.csv", fmt="csv")
```

### Text Export

Best for: console output, email notifications, quick summaries.

```bash
agent.export_report(report, "./audit_summary.txt", fmt="text")
```

Text report includes:
- Report metadata (ID, provider, scope, account, regions, score)
- Finding breakdown by severity
- Compliance gap counts per framework
- Cost summary (total + savings)
- Risk summary (open / critical counts)

---

## Examples

### Example 1: Daily Security Audit Cron Job

```bash
#!/bin/bash
# /etc/cron.d/cloud-audit-daily
0 6 * * *  cd /opt/cloud-audit && /usr/bin/python agent.py \
  --provider aws \
  --scope security \
  --account 123456789012 \
  --export /var/reports/security_$(date +\%F).json \
  >> /var/log/cloud-audit/cron.log 2>&1
```

### Example 2: CI/CD Compliance Gate

```yaml
# .github/workflows/compliance-gate.yml
name: Compliance Gate
on: [pull_request]

jobs:
  cloud-compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -e agents/cloud-audit
      - run: |
          python agents/cloud-audit/agent.py \
            --check-compliance \
            --framework CIS \
            --framework SOC2 \
            --account ${{ secrets.AWS_ACCOUNT_ID }} \
            > compliance_report.json
      - run: |
          python -c "
            import json, sys
            data = json.load(open('compliance_report.json'))
            non_compliant = sum(len(v) for v in data.values())
            if non_compliant > 0:
                print(f'FAIL: {non_compliant} compliance gaps found')
                sys.exit(1)
            print('PASS: All checks compliant')
          "
```

### Example 3: Multi-Cloud Consolidated Report

```python
config = Config(
    providers=[
        ProviderConfig(provider=CloudProvider.AWS, regions=["us-east-1", "eu-west-1"]),
        ProviderConfig(provider=CloudProvider.AZURE, regions=["eastus"], enabled=False),
        ProviderConfig(provider=CloudProvider.GCP, regions=["us-central1"], enabled=False),
    ],
    compliance=ComplianceConfig(
        enabled_frameworks=[
            ComplianceFramework.CIS,
            ComplianceFramework.SOC2,
            ComplianceFramework.ISO27001,
        ]
    ),
)

agent = CloudAuditAgent(config=config)

aws_report = agent.run_full_audit(provider=CloudProvider.AWS, scope=AuditScope.FULL)
azure_report = agent.run_full_audit(provider=CloudProvider.AZURE, scope=AuditScope.FULL)

combined_findings = aws_report.findings + azure_report.findings
print(f"Total findings across clouds: {len(combined_findings)}")
```

### Example 4: Custom Notification to PagerDuty

```python
class PagerDutyChannel(NotificationChannel):
    def __init__(self, integration_key: str):
        self._url = f"https://events.pagerduty.com/v2/enqueue/{integration_key}"

    def send(self, subject: str, message: str) -> bool:
        import urllib.request
        payload = json.dumps({
            "routing_key": self._url.split("/")[-1],
            "event_action": "trigger",
            "dedup_key": "cloud-audit-daily",
            "payload": {"summary": subject, "source": "CloudAuditAgent", "severity": "warning"},
        }).encode()
        req = urllib.request.Request(
            self._url, data=payload, headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status == 202
        except Exception as exc:
            logger.error("PagerDuty notification failed: %s", exc)
            return False

agent._notification_channels.append(PagerDutyChannel(integration_key="YOUR_KEY"))
```

### Example 5: Programme-Check Dot-Plot of Findings by Severity

```python
import collections

report = agent.run_full_audit(scope=AuditScope.SECURITY)
severities = [f.severity.value for f in report.findings]
counts = collections.Counter(severities)

for sev in ["critical", "high", "medium", "low", "info"]:
    bar = "█" * counts.get(sev, 0)
    print(f"{sev.upper():<10} {bar}")
```

Output example:
```
CRITICAL   ██
HIGH       █████
MEDIUM     ████
LOW        ██
INFO       
```

### Example 6: Scheduled FinOps Review

```python
def weekly_finops_review():
    config = Config(
        providers=[ProviderConfig(provider=CloudProvider.AWS, regions=["us-east-1"])],
        cost=CostConfig(lookback_days=7, include_forecast=True),
        risk=RiskConfig(min_severity=SeverityLevel.LOW, max_results=20),
    )
    agent = CloudAuditAgent(config=config)
    report = agent.run_full_audit(scope=AuditScope.COST)
    
    top_savers = sorted(
        report.cost_recommendations,
        key=lambda r: r.projected_monthly_savings,
        reverse=True,
    )[:5]
    
    print("Top 5 Cost-Saving Opportunities")
    for rec in top_savers:
        print(f"${rec.projected_monthly_savings:,.2f}/month - {rec.recommendation}")
```

---

## Troubleshooting

### No providers configured

**Symptom:** `ValueError: At least one provider must be configured.`

**Fix:** Pass a `Config` with at least one `ProviderConfig`.

### Cache returning stale data

**Symptom:** Report data looks outdated after changes in the cloud.

**Fix:** Reduce `Config.cache_ttl_seconds` or call `agent.clear_cache()` after
making cloud changes.

### Import errors

**Symptom:** `ModuleNotFoundError: No module named 'agents.cloud_audit'`

**Fix:** Ensure the package is installed or `PYTHONPATH` includes the repository root:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python agents/cloud-audit/agent.py --demo
```

### Slow full audit

**Symptom:** Audit takes longer than expected.

**Fix:**
- Reduce the number of `regions` in `ProviderConfig`
- Narrow the `scope` (e.g. `security` instead of `full`)
- Increase `parallel_checks` (future async support)
- Enable caching to avoid re-running unchanged environments
- Use `--check-compliance` or `--analyze-costs` for targeted runs

### Notification channel fails silently

**Symptom:** No Slack/email messages after audit.

**Fix:** Check `ComplianceConfig.notify_on_gap` is `True`. Verify webhook URLs
and SMTP settings in the notification channel constructor. Check agent logs for
`[NOTIFICATION]` or `[SLACK]` / `[EMAIL]` entries.

### Configuration validation errors

**Symptom:** `ValueError: Config errors: [...]`

**Fix:** Review the error list. Common issues:
- Empty `providers` list (will use default if not explicitly set)
- Missing `regions` for a provider
- `parallel_checks` < 1
- `cache_ttl_seconds` < 60

### Report export permission denied

**Symptom:** `OSError: [Errno 13] Permission denied: './reports/audit.json'`

**Fix:**
- Ensure the parent directory exists or is creatable
- Check write permissions on the target directory
- Use an absolute path if relative path resolution is ambiguous

---

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch: `git checkout -b feat/new-provider-gcp`
3. Follow the existing code style (type hints, dataclasses, no comments unless requested).
4. Add unit tests in `tests/agents/test_cloud_audit.py`.
5. Run linting: `ruff check agents/cloud-audit/agent.py`
6. Submit a pull request.

### Coding Conventions

- Use `PascalCase` for classes and enums; `snake_case` for functions and variables.
- All public methods must have type hints.
- Use `dataclass` for all data models.
- Enum members must be `UPPER_SNAKE_CASE`.
- Log via the module-level `logger`; never `print` in library code.
- No print statements in engine classes (use `logger.info/debug/warning/error`).
- Add docstrings to all public classes and methods (Google style).

### Commit Message Format

```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`

Examples:
```
feat(agent): add GCP simulated client stub
fix(cache): handle TTL expiry race condition
docs(architecture): add deployment profile section
```

---

## Security Policy

Please report security vulnerabilities to `security@example.com` (replace with
actual contact). Do not open public issues for security bugs.

**Security review checklist for contributors:**
- [ ] No plaintext credentials added
- [ ] No secrets or tokens committed
- [ ] Input validation added for new user-facing parameters
- [ ] Error messages do not leak sensitive system information
- [ ] New notification channels use TLS / secure protocols

---

## License

MIT License - see `LICENSE` for details.

---

## Files

| File | Description |
|------|-------------|
| `agent.py` | Main implementation: models, engines, agent, CLI (~1823 lines) |
| `GROK.md` | Agent instructions, capabilities, and API documentation |
| `ARCHITECTURE.md` | System design, data flow, component reference, deployment profiles, testing strategy |
| `README.md` | This file - quick start, guides, and examples |

---

## Support

- **Documentation:** See `GROK.md` and `ARCHITECTURE.md`
- **Issues:** Report bugs and feature requests via GitHub Issues
- **Discussions:** Use GitHub Discussions for questions and design proposals
- **Security:** Report security vulnerabilities to `security@example.com`

---

## Appendix: Agent Behaviour Reference

### Intended Behaviour on Common Inputs

| Command / Method | Expected Behaviour |
|-----------------|--------------------|
| `agent.audit_cloud(provider="aws", scope="security")` | Returns dict with provider, scope, score, findings |
| `agent.audit_cloud(provider="aws", scope="full")` | Returns dict with provider, scope, score, findings |
| `agent.run_full_audit(provider=AWS, scope=FULL, account_id="123")` | Returns AuditReport with score, findings, gaps, recommendations, risks |
| `agent.run_full_audit(provider="aws", scope="compliance")` | Runs security and compliance engines; cost engine may still run |
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
| Cache miss | First run or expired key | Proceed normally (log INFO) |
| Cache failure | Memory full | Log warning; degrade gracefully |
| Notification failure | Slack down, SMTP unreachable | Log error; audit still succeeds |
| File write error | No permissions on export path | `OSError` propagates |
| Missing regions | Empty `ProviderConfig.regions` | Applies safe defaults |

---

## Appendix: Version History

| Version | Date | Notable Changes |
|---------|------|-----------------|
| 2.0.0 | 2024-01 | Multi-engine architecture, data models, CLI, cache, notifications |
| 1.0.0 | 2023-06 | Initial release: basic security checks for AWS |

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
