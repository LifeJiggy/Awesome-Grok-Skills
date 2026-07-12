---
name: "drift-detection"
category: "iac"
version: "2.0.0"
tags: ["iac", "drift", "compliance", "monitoring", "remediation"]
description: "Infrastructure configuration drift detection and remediation"
---

# Drift Detection

## Overview

The Drift Detection module monitors infrastructure configuration state to identify unauthorized or unexpected changes (drift) from the desired state defined in Infrastructure as Code. It compares actual infrastructure state against Terraform state, CloudFormation stacks, or Pulumi outputs, detects drift events, categorizes severity, and supports automated or manual remediation. This is essential for maintaining security, compliance, and operational consistency across cloud environments.

## Core Capabilities

- **Multi-Tool State Comparison**: Detect drift against Terraform, CloudFormation, and Pulumi state
- **Continuous Monitoring**: Schedule periodic drift checks across infrastructure
- **Drift Categorization**: Classify drift by type (configuration, security, compliance, cost)
- **Change Impact Analysis**: Assess the impact and risk of detected drift
- **Automated Remediation**: Auto-revert or auto-apply based on drift policies
- **Notification Integration**: Alert via Slack, email, PagerDuty on drift detection
- **Drift Reporting**: Generate compliance and drift status reports
- **Historical Tracking**: Maintain drift event history for audit purposes

## Usage Examples

### Terraform Drift Detection

```python
from drift_detection import DriftDetector, DriftCheckConfig

detector = DriftDetector(
    config=DriftCheckConfig(
        terraform_workspaces=["production", "staging"],
        state_backends={"production": "s3://tf-state-prod", "staging": "s3://tf-state-staging"},
        check_interval_minutes=30,
    )
)

# Run drift check
results = detector.check_terraform_drift(workspace="production")

print(f"Drift Check Results:")
print(f"  Resources Checked: {results.resources_checked}")
print(f"  Drifted Resources: {results.drifted_count}")
print(f"  In Sync: {results.in_sync_count}")

for drift in results.drifted_resources:
    print(f"\n  Drift Detected: {drift.resource_address}")
    print(f"    Type: {drift.drift_type.value}")
    print(f"    Severity: {drift.severity}")
    print(f"    Changes: {drift.changes}")
```

### Continuous Monitoring

```python
from drift_detection import DriftMonitor, MonitoringSchedule

monitor = DriftMonitor(
    schedule=MonitoringSchedule(
        interval_minutes=15,
        environments=["production", "staging"],
        check_types=["terraform", "cloudformation"],
    ),
    notifications={
        "slack": {"webhook": "https://hooks.slack.com/xxx"},
        "email": {"recipients": ["ops-team@company.com"]},
    },
)

# Start monitoring
monitor.start()

# Check status
status = monitor.get_status()
print(f"Monitor Status: {status.state}")
print(f"Last Check: {status.last_check}")
print(f"Total Drift Events: {status.total_drift_events}")
```

### Automated Remediation

```python
from drift_detection import RemediationEngine, RemediationPolicy

engine = RemediationEngine(
    policies=[
        RemediationPolicy(
            name="auto-revert-security",
            trigger="security_drift",
            action="terraform_apply",
            auto_approve=True,
            notification_required=False,
        ),
        RemediationPolicy(
            name="manual-review-config",
            trigger="config_drift",
            action="manual_review",
            auto_approve=False,
            approvers=["ops-lead"],
        ),
    ]
)

# Process drift event
remediation = engine.remediate(drift_event)
print(f"Remediation: {remediation.action}")
print(f"Status: {remediation.status}")
print(f"Auto-approved: {remediation.auto_approved}")
```

### Compliance Reporting

```python
from drift_detection import ComplianceReporter

reporter = ComplianceReporter()

# Generate compliance report
report = reporter.generate_report(
    time_range_days=30,
    environments=["production"],
)

print(f"Compliance Report:")
print(f"  Period: {report.period_start} to {report.period_end}")
print(f"  Total Checks: {report.total_checks}")
print(f"  Drift Events: {report.drift_events}")
print(f"  Compliance Rate: {report.compliance_rate:.1f}%")
print(f"  Remediated: {report.remediated_count}")
```

## Best Practices

- **Frequent Checks**: Run drift detection at least every 30 minutes for production
- **Immediate Alerts**: Configure real-time alerts for security and compliance drift
- **Automated Remediation**: Auto-revert low-risk drift; manual review for high-risk changes
- **Baseline Maintenance**: Keep IaC state files up to date with actual infrastructure
- **Change Correlation**: Correlate drift events with change management tickets
- **Exception Handling**: Document and approve legitimate configuration exceptions
- **Regular Audits**: Perform comprehensive drift audits weekly or monthly
- **State Locking**: Ensure state file locking to prevent concurrent modifications

## Related Modules

- **terraform-cloudformation**: State management for drift comparison
- **cloud-deployment**: Deployment validation and post-deploy drift checks
- **drift-detection**: Core drift detection capabilities
