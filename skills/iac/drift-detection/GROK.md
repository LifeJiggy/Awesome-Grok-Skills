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

---

## Advanced Configuration

### Multi-Cloud State Comparison

```python
drift_config = {
    "terraform": {
        "backend": "s3",
        "state_file": "terraform.tfstate",
    },
    "cloudformation": {
        "region": "us-east-1",
        "stacks": ["prod-vpc", "prod-app"],
    },
    "pulumi": {
        "backend": "pulumi-cloud",
        "stacks": ["prod/network", "prod/compute"],
    },
}
```

### Custom Drift Policies

```python
drift_policies = {
    "security_drift": {
        "severity": "critical",
        "auto_remediate": True,
        "notify": ["security-team", "ops-lead"],
        "max_remediate_time_minutes": 5,
    },
    "config_drift": {
        "severity": "medium",
        "auto_remediate": False,
        "notify": ["dev-lead"],
        "approval_required": True,
    },
    "cost_drift": {
        "severity": "low",
        "auto_remediate": False,
        "notify": ["finance-team"],
        "budget_threshold": 100,
    },
}
```

### Advanced Notification Configuration

```python
notification_config = {
    "slack": {
        "webhook": "https://hooks.slack.com/xxx",
        "channel": "#infrastructure-alerts",
        "severity_filter": ["critical", "high"],
    },
    "email": {
        "smtp_host": "smtp.company.com",
        "recipients": ["ops@company.com"],
        "frequency": "daily",
    },
    "pagerduty": {
        "service_key": "xxx",
        "severity": "critical",
    },
    "webhook": {
        "url": "https://api.company.com/alerts",
        "method": "POST",
        "headers": {"Authorization": "Bearer xxx"},
    },
}
```

### Scheduled Check Configuration

```python
schedule_config = {
    "production": {
        "interval_minutes": 15,
        "check_types": ["terraform", "cloudformation"],
        "priority": "high",
    },
    "staging": {
        "interval_minutes": 30,
        "check_types": ["terraform"],
        "priority": "medium",
    },
    "development": {
        "interval_minutes": 60,
        "check_types": ["terraform"],
        "priority": "low",
    },
}
```

### Remediation Configuration

```python
remediation_config = {
    "terraform_apply": {
        "auto_approve": False,
        "timeout_minutes": 30,
        "rollback_on_failure": True,
        "notification_after": True,
    },
    "cloudformation_update": {
        "auto_approve": False,
        "timeout_minutes": 60,
        "rollback_on_failure": True,
    },
    "manual_review": {
        "approvers": ["ops-lead"],
        "timeout_hours": 24,
        "escalation_hours": 12,
    },
}
```

### Compliance Framework Integration

```python
compliance_frameworks = {
    "soc2": {
        "drift_reporting": True,
        "retention_days": 365,
        "audit_trail": True,
    },
    "hipaa": {
        "drift_reporting": True,
        "retention_days": 2555,
        "encryption_required": True,
    },
    "pci_dss": {
        "drift_reporting": True,
        "retention_days": 365,
        "quarterly_audit": True,
    },
}
```

## Architecture Patterns

### Event-Driven Drift Detection

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Cloud API  │────▶│  Event Bus   │────▶│   Drift     │
│  Changes    │     │  (SQS/SNS)   │     │  Detector   │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │ Alert   │           │ Remediate │         │  Report   │
                    │ Manager │           │  Engine   │         │  Engine   │
                    └─────────┘           └───────────┘         └───────────┘
```

### Polling-Based Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Scheduler  │────▶│  Drift       │────▶│  State      │
│  (Cron)     │     │  Checker     │     │  Comparator │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  State  │           │   Cloud   │         │  Results  │
                    │  Store  │           │   APIs    │         │  Store    │
                    └─────────┘           └───────────┘         └───────────┘
```

### Hybrid Architecture

```python
hybrid_architecture = {
    "real_time": {
        "event_driven": True,
        "sources": ["cloudtrail", "config-rules"],
    },
    "periodic": {
        "polling": True,
        "interval_minutes": 15,
        "sources": ["terraform-state", "cloudformation"],
    },
    "on_demand": {
        "api_triggered": True,
        "manual_checks": True,
    },
}
```

### Multi-Tenant Architecture

```python
tenant_config = {
    "tenant_1": {
        "state_backends": ["s3://tf-state-tenant1"],
        "notification_channels": ["slack://tenant1-alerts"],
    },
    "tenant_2": {
        "state_backends": ["s3://tf-state-tenant2"],
        "notification_channels": ["email://tenant2-ops@company.com"],
    },
}
```

### Remediation Workflow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Drift      │────▶│  Severity    │────▶│  Policy     │
│  Detected   │     │  Classifier  │     │  Engine     │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │ Auto    │           │  Manual   │         │  Ticket   │
                    │ Fix     │           │  Review   │         │  System   │
                    └─────────┘           └───────────┘         └───────────┘
```

## Integration Guide

### Terraform Cloud Integration

```python
tf_cloud_integration = {
    "api_endpoint": "https://app.terraform.io/api/v2",
    "organization": "my-org",
    "workspaces": ["prod-vpc", "prod-app"],
    "auto_apply": False,
    "notification_triggers": ["drift_detected"],
}
```

### AWS Config Integration

```python
aws_config = {
    "config_rules": [
        {
            "name": "terraform-drift",
            "source": {
                "owner": "CUSTOM_LAMBDA",
                "source_identifier": "arn:aws:lambda:us-east-1:123456789:function:check-drift",
            },
        },
    ],
    "delivery_channels": ["s3", "sns"],
}
```

### GitHub Actions Integration

```yaml
name: Drift Detection
on:
  schedule:
    - cron: '*/15 * * * *'
  workflow_dispatch:

jobs:
  detect-drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check for drift
        run: terraform plan -detailed-exitcode
        continue-on-error: true
      - name: Notify on drift
        if: steps.check.outputs.exitcode == 2
        uses: slackapi/slack-github-action@v1
        with:
          payload: '{"text": "Drift detected!"}'
```

### Jira Integration

```python
jira_config = {
    "server": "https://company.atlassian.net",
    "project": "INFRA",
    "issue_type": "Task",
    "priority_mapping": {
        "critical": "Highest",
        "high": "High",
        "medium": "Medium",
        "low": "Low",
    },
}
```

### ServiceNow Integration

```python
servicenow_config = {
    "instance": "company.service-now.com",
    "table": "incident",
    "auto_create": True,
    "assignment_group": "Infrastructure Operations",
    "severity_mapping": {
        "critical": "1",
        "high": "2",
        "medium": "3",
        "low": "4",
    },
}
```

### PagerDuty Integration

```python
pagerduty_config = {
    "service_key": "xxx",
    "api_key": "xxx",
    "escalation_policy": "Infrastructure Team",
    "severity_mapping": {
        "security_drift": "critical",
        "config_drift": "warning",
        "cost_drift": "info",
    },
}
```

## Performance Optimization

### Parallel Drift Checks

```python
parallel_config = {
    "max_concurrent_checks": 10,
    "batch_size": 5,
    "timeout_per_check_seconds": 60,
    "retry_count": 3,
}
```

### Caching Strategy

```python
cache_config = {
    "state_cache_ttl": 300,
    "resource_cache_ttl": 60,
    "api_call_cache_ttl": 30,
    "enable_distributed_cache": True,
    "cache_backend": "redis",
}
```

### Incremental Drift Detection

```python
incremental_config = {
    "track_changes": True,
    "last_check_timestamp": True,
    "delta_detection": True,
    "full_scan_interval_hours": 24,
}
```

### Resource Filtering

```python
filter_config = {
    "include_types": ["aws_instance", "aws_s3_bucket", "aws_vpc"],
    "exclude_types": ["aws_cloudwatch_log_group"],
    "include_tags": {"Environment": "production"},
    "exclude_names": ["temp-*", "test-*"],
}
```

### API Rate Limiting

```python
rate_limit_config = {
    "aws_api_calls_per_second": 100,
    "terraform_state_refresh_per_minute": 30,
    "backoff_strategy": "exponential",
    "max_retries": 5,
}
```

## Security Considerations

### State File Security

```python
state_security = {
    "encryption_at_rest": True,
    "encryption_in_transit": True,
    "kms_key_arn": "arn:aws:kms:us-east-1:123456789:key/abc-123",
    "access_logging": True,
    "versioning": True,
    "backup_enabled": True,
}
```

### Access Control

```python
access_control = {
    "rbac_enabled": True,
    "roles": {
        "drift-viewer": ["read"],
        "drift-operator": ["read", "remediate"],
        "drift-admin": ["read", "remediate", "configure"],
    },
    "mfa_required": True,
    "ip_whitelist": ["10.0.0.0/8"],
}
```

### Audit Logging

```python
audit_config = {
    "enabled": True,
    "log_level": "INFO",
    "retention_days": 365,
    "events": [
        "drift_detected",
        "remediation_started",
        "remediation_completed",
        "configuration_changed",
    ],
    "export_to_s3": True,
}
```

### Secret Management

```python
secret_config = {
    "vault_enabled": True,
    "vault_path": "secret/data/drift-detection",
    "rotation_enabled": True,
    "rotation_interval_days": 30,
}
```

### Network Security

```python
network_security = {
    "tls_required": True,
    "min_tls_version": "1.2",
    "mtls_enabled": False,
    "vpn_required": True,
    "firewall_rules": [
        {"port": 443, "protocol": "tcp", "source": "10.0.0.0/8"},
    ],
}
```

### Compliance Requirements

```python
compliance_config = {
    "data_residency": "us-east-1",
    "encryption_standard": "AES-256",
    "access_logging": True,
    "retention_policy": "7_years",
    "audit_trail": True,
}
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| State lock timeout | Concurrent access | Use state locking with DynamoDB |
| False positive drift | Provider bug | Update provider version |
| API rate limiting | Too many calls | Implement backoff strategy |
| State file corruption | Interrupted operation | Restore from backup |
| Notification failure | Webhook misconfiguration | Verify webhook URL and credentials |
| Remediation timeout | Slow resource update | Increase timeout, check resource health |
| Memory exhaustion | Large state file | Split state into smaller files |

### Debug Commands

```bash
# Check Terraform state
terraform state list
terraform state show aws_instance.web

# Verify drift
terraform plan -detailed-exitcode

# Check drift logs
tail -f /var/log/drift-detection.log

# Verify API connectivity
aws sts get-caller-identity
```

### State Recovery

```bash
# List state backups
aws s3 ls s3://tf-state-backups/

# Restore state
aws s3 cp s3://tf-state-backups/terraform.tfstate.backup terraform.tfstate

# Import drifted resource
terraform import aws_instance.web i-1234567890abcdef0
```

### Performance Issues

```bash
# Check API response time
time terraform plan

# Monitor resource count
terraform state list | wc -l

# Check cache hit rate
grep "cache_hit" /var/log/drift-detection.log
```

## API Reference

### DriftDetector

```python
class DriftDetector:
    def __init__(self, config: DriftCheckConfig):
        """Initialize drift detector."""

    def check_terraform_drift(self, workspace: str) -> DriftResult:
        """Check Terraform workspace for drift."""

    def check_cloudformation_drift(self, stack_name: str) -> DriftResult:
        """Check CloudFormation stack for drift."""

    def check_pulumi_drift(self, stack_name: str) -> DriftResult:
        """Check Pulumi stack for drift."""

    def get_drift_summary(self, time_range_days: int = 30) -> DriftSummary:
        """Get drift summary for time range."""
```

### DriftMonitor

```python
class DriftMonitor:
    def __init__(self, schedule: MonitoringSchedule, notifications: dict):
        """Initialize drift monitor."""

    def start(self) -> None:
        """Start monitoring."""

    def stop(self) -> None:
        """Stop monitoring."""

    def get_status(self) -> MonitorStatus:
        """Get monitor status."""

    def add_notification_channel(self, channel: str, config: dict) -> None:
        """Add notification channel."""
```

### RemediationEngine

```python
class RemediationEngine:
    def __init__(self, policies: List[RemediationPolicy]):
        """Initialize remediation engine."""

    def remediate(self, drift_event: DriftEvent) -> RemediationResult:
        """Remediate drift event."""

    def get_pending_reviews(self) -> List[DriftEvent]:
        """Get events pending manual review."""

    def approve_remediation(self, event_id: str, approver: str) -> ApprovalResult:
        """Approve manual remediation."""
```

### ComplianceReporter

```python
class ComplianceReporter:
    def __init__(self):
        """Initialize compliance reporter."""

    def generate_report(self, time_range_days: int, environments: List[str]) -> ComplianceReport:
        """Generate compliance report."""

    def get_drift_trend(self, time_range_days: int) -> DriftTrend:
        """Get drift trend analysis."""

    def export_report(self, report: ComplianceReport, format: str) -> str:
        """Export report to file."""
```

### DriftResult

```python
@dataclass
class DriftResult:
    resources_checked: int
    drifted_count: int
    in_sync_count: int
    drifted_resources: List[DriftedResource]
    check_duration_seconds: float
    timestamp: datetime
```

## Data Models

### DriftEvent

```python
@dataclass
class DriftEvent:
    event_id: str
    resource_address: str
    drift_type: DriftType
    severity: str
    changes: List[AttributeChange]
    detected_at: datetime
    remediation_status: str
    remediated_at: datetime = None
    remediated_by: str = None
```

### DriftType

```python
class DriftType(Enum):
    CONFIGURATION = "configuration"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    COST = "cost"
    TAG = "tag"
```

### AttributeChange

```python
@dataclass
class AttributeChange:
    attribute: str
    previous_value: Any
    current_value: Any
    change_type: str
```

### DriftedResource

```python
@dataclass
class DriftedResource:
    resource_address: str
    resource_type: str
    drift_type: DriftType
    severity: str
    changes: List[AttributeChange]
```

### ComplianceReport

```python
@dataclass
class ComplianceReport:
    report_id: str
    period_start: datetime
    period_end: datetime
    total_checks: int
    drift_events: int
    compliance_rate: float
    remediated_count: int
    environments: List[str]
    findings: List[ComplianceFinding]
```

### RemediationPolicy

```python
@dataclass
class RemediationPolicy:
    name: str
    trigger: str
    action: str
    auto_approve: bool
    notification_required: bool
    approvers: List[str] = None
    timeout_minutes: int = 30
```

## Deployment Guide

### Initial Setup

```bash
# Deploy drift detection service
terraform init
terraform plan -out=tfplan
terraform apply tfplan

# Configure notification channels
python setup_notifications.py --slack-webhook "https://hooks.slack.com/xxx"
```

### Multi-Environment Deployment

```python
environments = ["dev", "staging", "production"]
for env in environments:
    deploy_drift_detection(env, config)
```

### Rollback Procedure

```bash
# Rollback to previous version
terraform apply -target=module.drift_detection -var="version=previous"

# Restore state
aws s3 cp s3://backups/drift-state/terraform.tfstate terraform.tfstate
```

## Monitoring & Observability

### Metrics

```python
metrics_config = {
    "drift_detection_count": "counter",
    "drift_detected": "counter",
    "remediation_success_rate": "gauge",
    "check_duration_seconds": "histogram",
    "api_call_latency": "histogram",
}
```

### Dashboards

```python
dashboard_config = {
    "title": "Drift Detection Dashboard",
    "panels": [
        "drift_events_over_time",
        "remediation_success_rate",
        "compliance_rate",
        "resource_drift_distribution",
    ],
    "refresh_interval": "5m",
}
```

### Alerting Rules

```python
alerting_rules = [
    {
        "name": "CriticalDrift",
        "condition": "drift_severity == 'critical'",
        "severity": "critical",
        "channels": ["pagerduty", "slack"],
    },
    {
        "name": "HighDriftRate",
        "condition": "drift_rate > 10",
        "severity": "warning",
        "channels": ["slack", "email"],
    },
]
```

## Testing Strategy

### Unit Tests

```python
def test_drift_detection():
    detector = DriftDetector(config)
    result = detector.check_terraform_drift("test-workspace")
    assert result.resources_checked > 0
    assert result.drifted_count >= 0
```

### Integration Tests

```python
def test_full_drift_workflow():
    # Simulate drift
    simulate_resource_change()

    # Detect drift
    detector = DriftDetector(config)
    result = detector.check_terraform_drift("test")

    # Verify detection
    assert result.drifted_count > 0

    # Remediate
    engine = RemediationEngine(policies)
    remediation = engine.remediate(result.drifted_resources[0])
    assert remediation.status == "completed"
```

### Performance Tests

```python
def test_large_scale_drift():
    detector = DriftDetector(config)
    start_time = time.time()
    result = detector.check_terraform_drift("large-workspace")
    duration = time.time() - start_time

    assert duration < 300  # Should complete within 5 minutes
    assert result.resources_checked > 1000
```

## Versioning & Migration

### Version Strategy

```python
version_config = {
    "strategy": "semver",
    "breaking_changes": "major",
    "new_features": "minor",
    "bug_fixes": "patch",
}
```

### Migration Guide

```python
migration_steps = {
    "1.x_to_2.x": [
        "Update configuration format",
        "Migrate state to new backend",
        "Update notification webhooks",
    ],
    "2.x_to_3.x": [
        "Migrate to new API",
        "Update custom policies",
        "Reconfigure compliance rules",
    ],
}
```

## Glossary

| Term | Definition |
|------|------------|
| **Drift** | Deviation from desired state |
| **Remediation** | Action to fix drift |
| **Compliance** | Adherence to policies |
| **State** | Desired infrastructure configuration |
| **Baseline** | Reference configuration |
| **Attribute Change** | Individual value modification |
| **Severity** | Impact level of drift |
| **Auto-Remediate** | Automatic drift correction |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01-15 | Major rewrite with multi-cloud support |
| 1.5.0 | 2024-11-01 | Added compliance reporting |
| 1.4.0 | 2024-09-15 | Enhanced remediation engine |
| 1.3.0 | 2024-07-20 | Multi-tenant support |
| 1.2.0 | 2024-05-10 | Advanced notification system |
| 1.1.0 | 2024-03-01 | Performance improvements |
| 1.0.0 | 2024-01-01 | Initial release |

## Contributing Guidelines

1. Follow code standards
2. Write unit tests for new features
3. Update documentation
4. Add changelog entries
5. Test with multiple cloud providers

## License

MIT License. See LICENSE file for full terms.
