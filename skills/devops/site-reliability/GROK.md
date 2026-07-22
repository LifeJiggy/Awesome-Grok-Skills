---
name: "Site Reliability Engineering"
version: "2.0.0"
description: "Comprehensive SRE toolkit with SLO management, error budgets, incident management, toil reduction, and reliability engineering practices for production systems"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["devops", "sre", "reliability", "incident-management", "toil", "slo"]
category: "devops"
personality: "sre-engineer"
use_cases: ["SLO management", "incident management", "toil reduction", "capacity planning", "reliability engineering"]
---

# Site Reliability Engineering

> Production-grade SRE framework providing SLO management, error budget tracking, incident management, toil reduction, and reliability engineering practices for building and operating reliable systems.

## Overview

The Site Reliability Engineering module provides tools for implementing SRE practices. It implements SLI/SLO/SLA definition and tracking, error budget management and burn rate alerting, incident management workflows, toil identification and reduction, capacity planning, and post-incident review automation. Every practice includes metrics, templates, and automation support.

## Core Capabilities

### 1. SLO Management
- SLI definition and measurement
- SLO target setting and tracking
- Error budget calculation and tracking
- SLO burn rate alerting
- Multi-window burn rate analysis

### 2. Incident Management
- Incident detection and classification
- On-call rotation management
- Escalation policies
- Incident commander workflows
- Status page management

### 3. Post-Incident Review
- Blameless postmortem templates
- Root cause analysis automation
- Action item tracking
- Lessons learned documentation
- Trend analysis across incidents

### 4. Toil Reduction
- Toil identification and measurement
- Automation opportunity detection
- Toil budget tracking
- Runbook automation
- Self-healing systems

### 5. Capacity Planning
- Resource utilization forecasting
- Growth trend analysis
- Capacity threshold alerting
- Cost optimization recommendations
- Scaling recommendations

### 6. Reliability Practices
- Chaos engineering support
- Game day planning
- Failure mode analysis
- Disaster recovery testing
- Reliability reviews

## Usage Examples

### SLO Management

```python
from site_reliability import SLOManager, SLIDefinition

manager = SLOManager()

# Define SLIs
availability_sli = SLIDefinition(
    name="availability",
    metric="successful_requests / total_requests",
    good_event="http_status != 5xx",
    total_event="all_requests",
)

# Set SLO target
slo = manager.create_slo(
    name="api_availability",
    sli=availability_sli,
    target=99.9,
    window_days=30,
)

# Check error budget
budget = manager.get_error_budget(slo)
print(f"Error budget: {budget.remaining_pct:.2f}%")
print(f"Budget consumed: {budget.consumed_pct:.2f}%")
print(f"Days remaining: {budget.days_remaining:.1f}")
```

### Incident Management

```python
from site_reliability import IncidentManager, Severity

incidents = IncidentManager()

# Create incident
incident = incidents.create_incident(
    title="API error rate spike",
    severity=Severity.P1,
    service="api-gateway",
    description="Error rate increased to 5% in the last 10 minutes",
)

print(f"Incident: {incident.id}")
print(f"Severity: {incident.severity.value}")
print(f"On-call: {incident.oncall_engineer}")

# Update incident
incidents.update(incident.id, update="Root cause identified: database connection pool exhausted")

# Resolve
incidents.resolve(incident.id, resolution="Increased connection pool size")
```

### Toil Reduction

```python
from site_reliability import ToilTracker

tracker = Trackilizer()

# Log toil activity
tracker.log_activity(
    task="Manual certificate renewal",
    duration_minutes=30,
    frequency="monthly",
    automation_opportunity="high",
)

# Get toil report
report = tracker.get_report()
print(f"Total toil hours/month: {report.total_hours:.1f}")
print(f"Automation opportunities: {len(report.opportunities)}")
print(f"Toil ratio: {report.toil_ratio:.1%}")
```

### Capacity Planning

```python
from site_reliability import CapacityPlanner

planner = CapacityPlanner()

# Analyze capacity
analysis = planner.analyze(service="api-gateway")
print(f"Current utilization: {analysis.current_utilization:.1%}")
print(f"Projected 30-day: {analysis.projected_30day:.1%}")
print(f"Days until capacity: {analysis.days_until_capacity}")

# Get recommendations
recs = planner.get_recommendations()
for rec in recs:
    print(f"  {rec.action}: {rec.reason}")
```

## Best Practices

### SLOs
- Start with 99.9% availability SLOs
- Use multiple SLIs for comprehensive coverage
- Set SLOs based on user experience, not infrastructure
- Review and adjust SLOs quarterly

### Incident Management
- Always have an incident commander
- Use status pages for external communication
- Follow blameless postmortem principles
- Track action items to completion

### Toil Reduction
- Measure toil hours per engineer per month
- Set toil budget targets (e.g., < 30% of engineering time)
- Automate repetitive tasks
- Use runbooks for manual procedures

### Capacity Planning
- Monitor resource utilization continuously
- Forecast growth based on business metrics
- Set capacity alerts at 70% and 80%
- Review capacity monthly

## Related Modules

- **monitoring**: Metrics and observability for SRE
- **incident-response**: Incident management automation
- **chaos-engineering**: Reliability testing practices
- **cost-optimization**: Cost-aware reliability engineering

---

## Advanced Configuration

### Multi-Window Burn Rate Alerting

```python
from site_reliability import BurnRateAlert

burn_rate = BurnRateAlert(
    slo_target=99.9,
    short_window_minutes=5,
    long_window_minutes=60,
    burn_rate_threshold=14.4,  # 14.4x for 1-hour error budget consumption
)
```

### Error Budget Policy

```python
from site_reliability import ErrorBudgetPolicy

policy = ErrorBudgetPolicy(
    slo_name="api_availability",
    remaining_budget_thresholds={
        "warning": 50,     # Alert when 50% consumed
        "critical": 80,    # Alert when 80% consumed
        "exhausted": 100,  # Freeze deployments
    },
    deployment_freeze=True,
    notify_channels=["slack-sre", "pagerduty-oncall"],
)
```

## Architecture Patterns

### SRE Practice Framework

```
SLO Definition Ã¢â€ â€™ Error Budget Ã¢â€ â€™ Incident Response Ã¢â€ â€™ Postmortem Ã¢â€ â€™ Toil Reduction
```

### Error Budget Lifecycle

```
Budget Allocated Ã¢â€ â€™ Budget Consumed Ã¢â€ â€™ Alert Ã¢â€ â€™ Investigation Ã¢â€ â€™ Remediation Ã¢â€ â€™ Budget Recovery
```

## Integration Guide

### PagerDuty Integration

```python
from site_reliability import PagerDutyIntegration

pd = PagerDutyIntegration(routing_key="xxx")
pd.create_incident(
    title="API Error Budget Critical",
    severity="critical",
    description="Error budget below 20%",
)
```

### Status Page Integration

```python
from site_reliability import StatusPage

page = StatusPage(provider="opsgenie")
page.update_component("API Service", status="degraded")
page.create_incident(title="Elevated Error Rates", impact="major")
```

## Performance Optimization

| Optimization | Benefit |
|-------------|---------|
| SLI metric caching | Faster error budget calculation |
| Incident timeline automation | Reduced MTTR |
| Toil detection ML | Automated toil identification |
| Capacity forecasting | Proactive scaling |

## Security Considerations

- **Incident data confidentiality**: Restrict postmortem access
- **Status page auth**: Prevent unauthorized updates
- **Runbook access control**: Sensitive procedures restricted
- **Audit trail**: Log all SLO changes

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Error budget exhausts too fast | SLO too aggressive | Revisit SLO target |
| Burn rate alert flapping | Window too short | Increase window duration |
| Toil underreported | No time tracking | Add toil logging |
| Incident response slow | No runbooks | Create runbooks for common incidents |

## API Reference

### SLOManager

```python
class SLOManager:
    def __init__(self)
    def create_slo(self, name: str, sli: SLIDefinition, target: float, window_days: int) -> SLO
    def get_error_budget(self, slo: SLO) -> ErrorBudget
    def get_burn_rate(self, slo: SLO, window_minutes: int) -> float
```

### IncidentManager

```python
class IncidentManager:
    def __init__(self)
    def create_incident(self, title: str, severity: Severity, service: str, description: str) -> Incident
    def update(self, incident_id: str, update: str) -> None
    def resolve(self, incident_id: str, resolution: str) -> None
```

## Data Models

```python
from dataclasses import dataclass
from enum import Enum

class Severity(Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"

@dataclass
class SLO:
    name: str
    sli: SLIDefinition
    target: float
    window_days: int

@dataclass
class ErrorBudget:
    slo: SLO
    remaining_pct: float
    consumed_pct: float
    days_remaining: float

@dataclass
class Incident:
    id: str
    title: str
    severity: Severity
    status: str
    oncall_engineer: str
    created_at: float
```

## Deployment Guide

### Installation

```bash
pip install site-reliability
```

### SRE Practice Setup

1. Define SLIs for all services
2. Set SLO targets (start with 99.9%)
3. Configure error budget alerting
4. Create incident response runbooks
5. Establish postmortem process
6. Track and reduce toil

## Monitoring & Observability

```python
from site_reliability import MetricsCollector

collector = MetricsCollector()
collector.gauge("sre.slo.error_budget_remaining_pct", budget.remaining_pct, tags={"slo": slo.name})
collector.counter("sre.incidents.total", count, tags={"severity": sev})
collector.gauge("sre.toil.hours_per_month", hours)
collector.histogram("sre.mttr.minutes", mttr)
```

## Testing Strategy

```python
import pytest
from site_reliability import SLOManager, SLIDefinition

def test_error_budget():
    manager = SLOManager()
    sli = SLIDefinition(name="availability", metric="success/total", good_event="status != 5xx", total_event="all")
    slo = manager.create_slo("api_avail", sli, 99.9, 30)
    budget = manager.get_error_budget(slo)
    assert budget.remaining_pct == 100.0
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added burn rate alerting | Configure alert windows |
| 2.0.0 | New incident workflow | Migrate to new API |

## Glossary

| Term | Definition |
|------|-----------|
| **SLI** | Service Level Indicator |
| **SLO** | Service Level Objective |
| **SLA** | Service Level Agreement |
| **Error Budget** | Allowed unreliability within SLO |
| **MTTR** | Mean Time To Recovery |
| **Toil** | Manual, repetitive, automatable work |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with SLO management
- Error budget tracking and burn rate alerting
- Incident management workflows
- Toil reduction tracking

## Contributing Guidelines

```bash
git clone https://github.com/example/site-reliability.git
pip install -e ".[dev]"
pytest tests/
```

## Advanced SRE Practices

### Error Budget Policy Automation

```python
from site_reliability import ErrorBudgetAutomation

automation = ErrorBudgetAutomation(
    slo_targets=[
        {"name": "api_availability", "target": 99.9, "window_days": 30},
        {"name": "api_latency", "target": 99.5, "window_days": 30},
    ],
    policies=[
        {"budget_consumed_pct": 50, "action": "notify", "channels": ["slack-sre"]},
        {"budget_consumed_pct": 75, "action": "restrict_deployments", "scope": "non-critical"},
        {"budget_consumed_pct": 90, "action": "freeze_deployments", "scope": "all"},
        {"budget_consumed_pct": 100, "action": "escalate", "channels": ["pagerduty-oncall"]},
    ],
)

# Check and enforce policies
result = automation.check_and_enforce()
print(f"Budget status: {result.budget_status}")
print(f"Action taken: {result.action_taken}")
print(f"Deployments restricted: {result.deployments_restricted}")
```

### Incident Commander Workflow

```python
from site_reliability import IncidentCommander

ic = IncidentCommander()

# Start incident
incident = ic.start_incident(
    title="Payment processing degraded",
    severity=Severity.P1,
    service="payment-service",
    description="Payment success rate dropped to 85%",
)

# Assign roles
ic.assign_role(incident.id, role="scribe", engineer="bob")
ic.assign_role(incident.id, role="subject_matter_expert", engineer="alice")

# Post updates
ic.update(incident.id, update="Identified root cause: payment gateway rate limiting")
ic.update(incident.id, update="Implementing circuit breaker fallback")

# Communicate
ic.announce(
    incident.id,
    channel="status-page",
    message="Payment processing degraded. Some transactions may fail. Working on resolution.",
)

# Resolve
ic.resolve(
    incident.id,
    resolution="Enabled circuit breaker fallback to secondary payment gateway",
    root_cause="Primary payment gateway rate limiting due to upstream issue",
    duration_minutes=45,
)
```

### Postmortem Automation

```python
from site_reliability import PostmortemGenerator

generator = PostmortemGenerator()

# Generate postmortem from incident data
postmortem = generator.generate(
    incident_id="INC-1234",
    template="blameless",
    sections=[
        "summary",
        "impact",
        "timeline",
        "root_cause",
        "action_items",
        "lessons_learned",
    ],
)

# Generate timeline from alerts and updates
timeline = generator.build_timeline(incident_id="INC-1234")
for event in timeline:
    print(f"  [{event.timestamp}] {event.source}: {event.description}")

# Export to Confluence
generator.export_confluence(postmortem, space_key="SRE", parent_page="Postmortems")
```

### Toil Measurement Framework

```python
from site_reliability import ToilFramework

framework = ToilFramework(
    categories=[
        {"name": "manual_operations", "weight": 1.0},
        {"name": "repetitive_tasks", "weight": 0.8},
        {"name": "automatable_work", "weight": 0.9},
        {"name": "interrupt_driven", "weight": 0.7},
    ],
)

# Log toil activities
framework.log(
    task="Manual certificate renewal",
    category="repetitive_tasks",
    duration_minutes=30,
    frequency="monthly",
    engineer="alice",
    automation_difficulty="low",
)

# Generate toil report
report = framework.report(engineering_team_size=10)
print(f"Total toil hours/month: {report.total_hours:.1f}")
print(f"Toil ratio: {report.toil_ratio:.1%}")
print(f"Target toil ratio: {report.target_ratio:.1%}")
print(f"Toil reduction needed: {report.reduction_needed_hours:.1f}h/month")
print(f"Top toil tasks:")
for task in report.top_tasks:
    print(f"  {task.name}: {task.hours_per_month:.1f}h/month ({task.automation_difficulty})")
```

### Capacity Planning Models

```python
from site_reliability import CapacityModel

model = CapacityModel(service="api-gateway")

# Add resource metrics
model.add_resource(
    name="cpu",
    current_utilization=0.65,
    peak_utilization=0.85,
    growth_rate_daily=0.02,
)

model.add_resource(
    name="memory",
    current_utilization=0.70,
    peak_utilization=0.90,
    growth_rate_daily=0.01,
)

model.add_resource(
    name="disk",
    current_utilization=0.45,
    peak_utilization=0.60,
    growth_rate_daily=0.05,
)

# Generate forecast
forecast = model.forecast(days=90)
print(f"CPU capacity reached: {forecast.cpu_days_until_capacity}")
print(f"Memory capacity reached: {forecast.memory_days_until_capacity}")
print(f"Disk capacity reached: {forecast.disk_days_until_capacity}")

# Get recommendations
recs = model.recommendations()
for rec in recs:
    print(f"  [{rec.priority}] {rec.action}")
    print(f"    Resource: {rec.resource}")
    print(f"    Deadline: {rec.deadline}")
    print(f"    Cost impact: {rec.cost_impact}")
```

### SRE Maturity Model

| Level | Practice | Metrics | Tools |
|-------|----------|---------|-------|
| 1 Ã¢â‚¬â€ Initial | Manual incident response | MTTR, incident count | Ticketing system |
| 2 Ã¢â‚¬â€ Managed | Defined runbooks, basic SLOs | Error budget, MTTR | Monitoring stack |
| 3 Ã¢â‚¬â€ Defined | Automated SLO tracking, game days | SLO burn rate, toil ratio | Full observability |
| 4 Ã¢â‚¬â€ Quantitative | Predictive capacity, automated remediation | Forecast accuracy, automation rate | ML-based alerting |
| 5 Ã¢â‚¬â€ Optimizing | Self-healing, continuous improvement | Reliability score, engineering velocity | AI-driven operations |

### Reliability Scorecard

```python
from site_reliability import ReliabilityScorecard

scorecard = ReliabilityScorecard(service="api-gateway")

# Calculate score
score = scorecard.calculate(
    metrics={
        "availability_pct": 99.95,
        "mttr_minutes": 15,
        "error_budget_remaining_pct": 65,
        "toil_ratio": 0.25,
        "incident_count_per_month": 2,
        "postmortem_completion_rate": 1.0,
        "action_item_completion_rate": 0.85,
    },
)

print(f"Reliability score: {score.total:.1f}/100")
print(f"Breakdown:")
for category in score.categories:
    print(f"  {category.name}: {category.score:.1f}/100 (weight: {category.weight:.0%})")
print(f"Grade: {score.grade}")
```

### Runbook Automation

```python
from site_reliability import RunbookAutomation

runbook = RunbookAutomation(
    name="high-error-rate-response",
    triggers=[
        {"metric": "http_error_rate", "condition": "> 0.05", "duration_s": 300},
    ],
    steps=[
        {"action": "check_service_health", "command": "kubectl get pods -l app=api-service"},
        {"action": "check_dependencies", "command": "curl -s https://status.internal/health"},
        {"action": "collect_logs", "command": "kubectl logs -l app=api-service --tail=100"},
        {"action": "notify_oncall", "channel": "slack-sre", "message": "Automated investigation complete"},
    ],
    max_duration_s=600,
)

# Execute runbook
result = runbook.execute(trigger_data={"error_rate": 0.08})
print(f"Runbook: {result.runbook_name}")
print(f"Status: {result.status}")
print(f"Steps completed: {result.steps_completed}/{result.total_steps}")
for step in result.step_results:
    print(f"  [{step.status}] {step.action}: {step.output[:100]}")
```

### SLI Definitions Library

```python
from site_reliability import SLILibrary

library = SLILibrary()

# Availability SLI
library.register(
    name="availability",
    description="Percentage of successful requests",
    metric="sum(http_requests_total{status!~'5..'}) / sum(http_requests_total)",
    good_event="status != 5xx",
    total_event="all_requests",
    unit="percentage",
)

# Latency SLI
library.register(
    name="latency",
    description="Percentage of requests under latency threshold",
    metric="sum(http_request_duration_seconds < 0.5) / sum(http_request_duration_seconds)",
    good_event="duration < 0.5",
    total_event="all_requests",
    unit="percentage",
)

# Freshness SLI
library.register(
    name="freshness",
    description="Data freshness for batch jobs",
    metric="time() - max(last_successful_run_timestamp)",
    good_event="freshness < 3600",
    total_event="all_batch_jobs",
    unit="seconds",
)

# Get all SLIs
for sli in library.list():
    print(f"  {sli.name}: {sli.description}")
```

### Multi-Region SLO Aggregation

```python
from site_reliability import MultiRegionSLO

slo = MultiRegionSLO(
    name="global_availability",
    target=99.9,
    window_days=30,
    regions=[
        {"name": "us-east-1", "weight": 0.4, "sli": "availability"},
        {"name": "eu-west-1", "weight": 0.35, "sli": "availability"},
        {"name": "ap-south-1", "weight": 0.25, "sli": "availability"},
    ],
)

# Calculate global SLO
status = slo.get_status()
print(f"Global availability: {status.global_availability:.3f}%")
for region in status.regions:
    print(f"  {region.name}: {region.availability:.3f}% (weight: {region.weight:.0%})")
print(f"Global error budget remaining: {status.error_budget_remaining_pct:.1f}%")
```

### Incident Metrics Dashboard

| Metric | Last 7 Days | Last 30 Days | Target |
|--------|-------------|--------------|--------|
| Incidents | 3 | 8 | < 5 |
| MTTR (minutes) | 22 | 18 | < 30 |
| MTBF (hours) | 56 | 90 | > 100 |
| P1 Incidents | 0 | 1 | < 1 |
| Error Budget Used | 15% | 35% | < 50% |
| Postmortem Rate | 100% | 100% | 100% |
| Action Item Completion | 80% | 85% | > 80% |
| Toil Ratio | 20% | 25% | < 30% |

### Reliability Review Template

```python
from site_reliability import ReliabilityReview

review = ReliabilityReview(
    service="api-gateway",
    period="2024-Q1",
    attendees=["sre-team", "backend-team"],
)

# Generate review data
data = review.generate(
    metrics=[
        "availability_slo",
        "latency_slo",
        "error_budget",
        "incidents",
        "mttr",
        "toil_ratio",
        "capacity_utilization",
    ],
)

# Create review document
review.export_markdown("reliability_review_q1_2024.md")
review.export_pdf("reliability_review_q1_2024.pdf")
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

## Additional Resources

### Related Technologies

This module integrates with industry-standard tools and frameworks. Refer to the official documentation for the latest API references and configuration options.

### Community and Support

- Open source contributions welcome
- Issue tracking via GitHub Issues
- Documentation updated with each release
- Community forums for discussion and support

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-01 | Initial release |
| 1.1.0 | 2026-03-15 | Enhanced configuration options |
| 1.2.0 | 2026-06-01 | Performance improvements |
| 2.0.0 | 2026-07-01 | Major architecture update |

### License

MIT License - Copyright (c) 2026 Awesome Grok Skills


## Extended Reference

### Configuration Matrix

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enabled | bool | true | Enable the module |
| log_level | str | INFO | Logging verbosity |
| timeout | int | 30 | Operation timeout in seconds |
| max_retries | int | 3 | Maximum retry attempts |
| cache_ttl | int | 3600 | Cache time-to-live in seconds |
| batch_size | int | 100 | Records per batch |
| parallel_workers | int | 4 | Concurrent worker threads |
| memory_limit | str | 512MB | Maximum memory allocation |
| disk_threshold | float | 0.8 | Disk usage alert threshold |
| health_check_interval | int | 60 | Health check frequency seconds |

### Environment Variables

`ash
MODULE_ENABLED=true
MODULE_LOG_LEVEL=INFO
MODULE_TIMEOUT=30
MODULE_MAX_RETRIES=3
MODULE_CACHE_TTL=3600
MODULE_BATCH_SIZE=100
MODULE_PARALLEL_WORKERS=4
MODULE_MEMORY_LIMIT=512MB
MODULE_DISK_THRESHOLD=0.8
MODULE_HEALTH_CHECK_INTERVAL=60
```n
### Docker Configuration

`yaml
version: '3.8'
services:
  module:
    image: awesome-grok/module:latest
    environment:
      - MODULE_ENABLED=true
      - MODULE_LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    ports:
      - '8080:8080'
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8080/health']
      interval: 30s
      timeout: 10s
      retries: 3
```n
### Kubernetes Deployment

`yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: module-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: module
  template:
    metadata:
      labels:
        app: module
    spec:
      containers:
      - name: module
        image: awesome-grok/module:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: 256Mi
            cpu: 250m
          limits:
            memory: 512Mi
            cpu: 500m
```n
### Prometheus Metrics

`yaml
scrape_configs:
  - job_name: 'module'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: /metrics
    scrape_interval: 15s
```n
### Grafana Dashboard

Import dashboard ID 12345 from Grafana.com for pre-configured monitoring panels including request rate, error rate, latency percentiles, and resource utilization.

### Alert Rules

`yaml
groups:
  - name: module-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(module_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(module_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
```n
### CI/CD Pipeline

`yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v
      - run: python -m mypy src/
      - run: python -m ruff check src/
```n
