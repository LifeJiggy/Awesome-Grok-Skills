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