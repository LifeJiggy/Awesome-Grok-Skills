# Site Reliability Engineering

## Overview

Site Reliability Engineering (SRE) combines software engineering and operations to build and run reliable, scalable systems. This skill covers SLO definition, error budget management, incident response, and reliability engineering practices. SRE focuses on reliability as a feature and balances feature development with operational stability.

## Core Capabilities

Service Level Objectives define reliability targets based on user needs. Service Level Indicators measure actual performance against SLOs. Error budgets quantify how much unreliability is acceptable. Error budget burn rate guides feature vs. reliability work decisions.

Incident management provides structured response to outages. Runbooks document operational procedures. Post-mortems extract learning from incidents without blame. Capacity planning ensures systems can handle growth.

## Usage Examples

```python
from site_reliability import SiteReliability

sre = SiteReliability()

availability_sli = sre.create_sli(
    name="api_availability",
    category="availability",
    indicator="successful_requests / total_requests",
    measurement_method="percentage over 1 minute windows"
)

api_availability_slo = sre.create_availability_slo(
    name="API 99.9% Availability",
    target=0.999,
    window="30d"
)

latency_slo = sre.create_latency_slo(
    name="API P99 Latency",
    threshold_ms=200,
    target_percent=0.99,
    window="30d"
)

error_budget = sre.calculate_error_budget(
    slo=api_availability_slo,
    actual_performance=0.998
)

runbook = sre.create_runbook(
    name="Database High CPU Runbook",
    steps=[
        {"step": 1, "action": "Check current connections", "command": "SHOW PROCESSLIST"},
        {"step": 2, "action": "Identify slow queries", "command": "EXPLAIN SELECT..."},
        {"step": 3, "action": "Kill blocking queries if needed"},
        {"step": 4, "action": "Restart database if unresponsive"}
    ],
    escalation_path=["on_call", "dba_team", "manager"]
)

incident_response = sre.create_incident_response(
    severity_levels=[
        {"level": 1, "name": "SEV-1", "response_time_min": 15, "description": "Critical - Full outage"},
        {"level": 2, "name": "SEV-2", "response_time_min": 30, "description": "High - Major degradation"},
        {"level": 3, "name": "SEV-3", "response_time_min": 60, "description": "Medium - Minor impact"}
    ]
)

post_mortem = sre.create_post_mortem_template(
    sections=["summary", "timeline", "impact", "root_cause", "resolution", "action_items"]
)

on_call = sre.create_on_call_schedule(
    rotation_type="weekly",
    handoff_day="Friday",
    handoff_hour="12:00"
)

capacity_plan = sre.create_capacity_plan(
    current_capacity={"rps": 1000, "instances": 10},
    growth_rate=0.15,
    headroom_percent=20
)

health_check = sre.create_health_check_endpoint(
    path="/health",
    checks=[
        {"name": "database", "type": "readiness"},
        {"name": "cache", "type": "readiness"}
    ]
)

synthetic = sre.create_synthetic_monitoring(
    name="API Health Check",
    url="https://api.example.com/health",
    frequency_minutes=5,
    locations=["us-east-1", "us-west-2", "eu-west-1"]
)

canary = sre.create_canary_analysis(
    baseline_deployment="v1.0",
    canary_deployment="v1.1",
    metrics=["latency", "error_rate", "throughput"],
    success_criteria={"threshold": 0.95, "metric": "success_rate"}
)

dr_plan = sre.create_disaster_recovery_plan(
    rpo_hours=4,
    rto_hours=24,
    test_frequency="quarterly"
)

dashboard = sre.create_sre_dashboard(
    panels=[
        {"name": "Service Health", "type": "status"},
        {"name": "SLO Status", "type": "slo"},
        {"name": "Error Budget", "type": "budget"},
        {"name": "Incident Rate", "type": "incident"}
    ]
)
```

## Best Practices

Define SLOs based on user experience, not internal metrics. Monitor error budget burn rate to balance features and reliability. Create runbooks for all common operational tasks. Automate incident response where possible.

Conduct blameless post-mortems to learn from failures. Test disaster recovery procedures regularly. Reduce toil through automation. Involve SREs in architectural decisions.

## Related Skills

- Incident Management (incident response)
- Chaos Engineering (reliability testing)
- Observability (monitoring)
- Site Reliability Engineering (engineering practices)

## Use Cases

SaaS platform reliability ensures high availability for customers. E-commerce platforms maintain uptime during peak shopping periods. Financial systems meet strict availability requirements. Cloud services provide SLAs to customers.
