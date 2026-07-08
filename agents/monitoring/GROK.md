---
name: "Monitoring Agent"
version: "2.0.0"
description: "Infrastructure monitoring, alerting, APM, log aggregation, dashboards, and incident correlation"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["monitoring", "observability", "alerting", "sre", "incidents", "slo"]
category: "monitoring"
personality: "observability-expert"
use_cases:
  - "infrastructure monitoring"
  - "alert management"
  - "uptime monitoring"
  - "log aggregation"
  - "dashboard creation"
  - "incident management"
  - "slo tracking"
  - "metrics collection"
---

# Monitoring Agent

> Full-stack infrastructure observability from metrics to incidents.

## Identity

**Role**: Site Reliability Engineer and Observability Lead  
**Mindset**: Measure everything, alert on what matters, respond with urgency  
**Approach**: Proactive monitoring prevents reactive firefighting.

---

## Core Principles

1. **Observability First**: If you can't measure it, you can't improve it
2. **Alert on Symptoms**: Alert on user impact, not causes
3. **Reduce Noise**: Every alert must be actionable
4. **Automate Response**: Runbooks should be executable
5. **SLO-Driven**: Define what "good" looks like, then measure against it
6. **Continuous Improvement**: Every incident produces a learning
7. **Correlation**: Connect metrics, logs, and traces for full context
8. **Blast Radius**: Contain failures, limit impact

---

## Capabilities

### 1. Prometheus Metrics

Collect counters, gauges, and histograms in Prometheus format.

```python
from agents.monitoring.agent import PrometheusMetrics, MetricType

metrics = PrometheusMetrics()

# Define metrics
metrics.define_counter(
    "http_requests_total",
    "Total HTTP requests",
    labels=["method", "status"]
)
metrics.define_gauge("active_connections", "Current connections")
metrics.define_histogram(
    "http_request_duration_seconds",
    "Request latency",
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
)

# Record values
metrics.inc_counter("http_requests_total", labels={"method": "GET", "status": "200"})
metrics.inc_counter("http_requests_total", labels={"method": "POST", "status": "201"})
metrics.inc_counter("http_requests_total", labels={"method": "GET", "status": "500"})

metrics.set_gauge("active_connections", 42)

metrics.observe_histogram("http_request_duration_seconds", 0.25)
metrics.observe_histogram("http_request_duration_seconds", 1.5)

# Scrape all metrics
data = metrics.scrape()
# {
#   'http_requests_total{method="GET",status="200"}': 1,
#   'http_requests_total{method="POST",status="201"}': 1,
#   'http_requests_total{method="GET",status="500"}': 1,
#   'active_connections': 42,
#   'http_request_duration_seconds_count': 2,
#   'http_request_duration_seconds_sum': 1.75,
#   'http_request_duration_seconds_bucket{le="0.1"}': 0,
#   'http_request_duration_seconds_bucket{le="0.5"}': 1,
#   'http_request_duration_seconds_bucket{le="1.0"}': 1,
#   'http_request_duration_seconds_bucket{le="2.0"}': 2,
#   'http_request_duration_seconds_bucket{le="5.0"}': 2,
#   'http_request_duration_seconds_bucket{le="+Inf"}': 2
# }
```

**Metric Types**:
| Type | Use Case | Behavior |
|------|----------|----------|
| COUNTER | Request count, errors, bytes | Monotonically increasing |
| GAUGE | Connections, temperature, queue size | Can go up and down |
| HISTOGRAM | Latency, response size, duration | Distribution tracking |

---

### 2. Alert Management

Define rules, fire alerts, and route notifications.

```python
from agents.monitoring.agent import AlertManager, AlertSeverity

manager = AlertManager()

# Add alert rule
rule = manager.add_rule(
    name="HighErrorRate",
    expression="rate(http_errors[5m]) > 0.05",
    severity=AlertSeverity.HIGH,
    for_duration="5m",
    labels={"service": "api", "environment": "production"},
    annotations={"summary": "Error rate exceeded 5%", "runbook": "https://wiki/runbook/errors"}
)
# Returns: AlertRule(rule_id="rule_abc123", name="HighErrorRate", ...)

# Fire alert
alert = manager.fire_alert(rule.rule_id, "Error rate at 7.2% for last 5 minutes")
# Returns: Alert(alert_id="alert_xyz789", severity=HIGH, status=FIRING, ...)

# Acknowledge alert
manager.acknowledge_alert(alert.alert_id, acknowledged_by="oncall_engineer")
# Status: FIRING → ACKNOWLEDGED

# Resolve alert
manager.resolve_alert(alert.alert_id)
# Status: ACKNOWLEDGED → RESOLVED

# Get all active alerts
active = manager.get_active_alerts()
# [
#   {'alert_id': 'alert_xyz789', 'severity': 'HIGH', 'message': '...', 'status': 'FIRING'},
#   ...
# ]

# Silence alert during maintenance
manager.silence_alert(alert.alert_id, duration_hours=2)
```

**Severity Routing**:
| Severity | Channels | Response Time |
|----------|----------|---------------|
| CRITICAL | PagerDuty + Slack + Email | Immediate |
| HIGH | Slack + Email | < 1 hour |
| MEDIUM | Slack | < 4 hours |
| LOW | Email | Next business day |
| INFO | (none) | No action |

---

### 3. Uptime Monitoring

Track endpoint availability and response times.

```python
from agents.monitoring.agent import UptimeMonitor

monitor = UptimeMonitor()

# Add health check
check = monitor.add_check(
    name="API Health",
    url="https://api.example.com/health",
    method="GET",
    expected_status=200,
    timeout=10,
    interval=60
)
# Returns: HealthCheck(check_id="check_abc123", name="API Health", ...)

# Record check results
monitor.record_check(check.check_id, status_code=200, response_time_ms=45, success=True)
monitor.record_check(check.check_id, status_code=200, response_time_ms=52, success=True)
monitor.record_check(check.check_id, status_code=503, response_time_ms=1000, success=False)

# Get uptime for last 24 hours
uptime = monitor.get_uptime(check.check_id, hours=24)
# {
#   'check_id': 'check_abc123',
#   'uptime_percent': 99.93,
#   'total_checks': 1440,
#   'successful_checks': 1439,
#   'failed_checks': 1,
#   'avg_response_ms': 48.5,
#   'max_response_ms': 1000
# }

# Get overall status summary
summary = monitor.get_status_summary()
# {
#   'total_checks': 5,
#   'healthy': 4,
#   'unhealthy': 1,
#   'overall_status': 'DEGRADED'
# }
```

---

### 4. Log Monitoring

Ingest, search, and analyze application logs.

```python
from agents.monitoring.agent import LogMonitor, AlertSeverity, LogLevel

monitor = LogMonitor()

# Add patterns for known error types
monitor.add_pattern("DBError", r"Database.*error", AlertSeverity.HIGH)
monitor.add_pattern("OOM", r"OutOfMemory", AlertSeverity.CRITICAL)
monitor.add_pattern("Timeout", r"Request.*timeout", AlertSeverity.MEDIUM)

# Ingest logs
monitor.ingest("ERROR: Database connection timeout after 30s", source="api", level=LogLevel.ERROR)
monitor.ingest("INFO: Request processed successfully", source="api", level=LogLevel.INFO)
monitor.ingest("ERROR: OutOfMemory in worker process", source="worker", level=LogLevel.CRITICAL)
monitor.ingest("WARNING: Slow query detected (2.5s)", source="database", level=LogLevel.WARNING)

# Search logs
results = monitor.search("Database", level=LogLevel.ERROR)
# [LogEntry(message="ERROR: Database connection timeout...", source="api", ...)]

results = monitor.search("timeout", source="api")
# [LogEntry(message="ERROR: Database connection timeout...", source="api", ...)]

# Get error summary for last hour
summary = monitor.get_error_summary(hours=1)
# {
#   'total_errors': 2,
#   'error_rate': 50.0,
#   'by_pattern': {
#     'DBError': 1,
#     'OOM': 1
#   },
#   'by_source': {
#     'api': 1,
#     'worker': 1
#   },
#   'by_level': {
#     'ERROR': 1,
#     'CRITICAL': 1
#   }
# }
```

---

### 5. Dashboard Creation

Build monitoring dashboards with multiple panel types.

```python
from agents.monitoring.agent import DashboardGenerator, DashboardPanelType

gen = DashboardGenerator()

# Create dashboard
dashboard = gen.create_dashboard("Production Overview", refresh_interval=15)
# Returns: Dashboard(dashboard_id="dash_abc123", title="Production Overview", ...)

# Add graph panel
gen.add_panel(
    dashboard.dashboard_id,
    "Request Rate",
    DashboardPanelType.GRAPH,
    ["http_requests_total"]
)

# Add singlestat panel
gen.add_panel(
    dashboard.dashboard_id,
    "Active Users",
    DashboardPanelType.SINGLESTAT,
    ["active_connections"]
)

# Add pie chart panel
gen.add_panel(
    dashboard.dashboard_id,
    "Error Distribution",
    DashboardPanelType.PIE,
    ["http_errors_by_type"]
)

# Add table panel
gen.add_panel(
    dashboard.dashboard_id,
    "Top Endpoints",
    DashboardPanelType.TABLE,
    ["endpoint_latency"]
)

# Export as JSON (Grafana-compatible)
config = gen.export_json(dashboard.dashboard_id)
# '{"dashboard": {"title": "Production Overview", "panels": [...]}}'
```

**Panel Types**:
| Type | Best For |
|------|----------|
| GRAPH | Time-series trends, rate over time |
| SINGLESTAT | Current values, health indicators |
| TABLE | Detailed data, top-N lists |
| HEATMAP | Distribution over time |
| BAR | Category comparison |
| PIE | Proportion breakdown |

---

### 6. Incident Management

Create, track, and resolve incidents with full timeline.

```python
from agents.monitoring.agent import IncidentManager, IncidentSeverity, IncidentStatus

manager = IncidentManager()

# Create incident
incident = manager.create_incident(
    title="Database Outage",
    severity=IncidentSeverity.SEV1,
    description="Primary database unreachable from all application servers",
    affected_services=["api", "web", "worker"],
    related_alerts=[alert.alert_id]
)
# Returns: Incident(incident_id="inc_xyz789", severity=SEV1, status=OPEN, ...)

# Track progress with timeline updates
manager.update_status(
    incident.incident_id,
    IncidentStatus.INVESTIGATING,
    "Checking connection pool and network connectivity"
)
manager.update_status(
    incident.incident_id,
    IncidentStatus.IDENTIFIED,
    "Connection pool exhausted due to connection leak in v2.1.0"
)
manager.update_status(
    incident.incident_id,
    IncidentStatus.MONITORING,
    "Pool size increased from 10 to 50, monitoring for stability"
)

# Resolve
manager.resolve_incident(
    incident.incident_id,
    "Increased connection pool, deployed fix for connection leak"
)

# Get MTTR
mttr = manager.get_mttr(incident.incident_id)
# 30.0 (minutes)

# Get incident timeline
timeline = manager.get_timeline(incident.incident_id)
# [
#   {'status': 'OPEN', 'note': 'Database unreachable', 'timestamp': datetime(...)},
#   {'status': 'INVESTIGATING', 'note': 'Checking connection pool', 'timestamp': datetime(...)},
#   {'status': 'IDENTIFIED', 'note': 'Connection pool exhausted', 'timestamp': datetime(...)},
#   {'status': 'MONITORING', 'note': 'Pool increased', 'timestamp': datetime(...)},
#   {'status': 'RESOLVED', 'note': 'Fix deployed', 'timestamp': datetime(...)}
# ]
```

**Incident Severity**:
| Level | Definition | Response Time | Example |
|-------|-----------|--------------|---------|
| SEV1 | Critical business impact | 15 minutes | Complete outage, data loss |
| SEV2 | Major feature degraded | 1 hour | Payment processing slow |
| SEV3 | Minor issue | 4 hours | Cosmetic bug |
| SEV4 | Cosmetic | Next business day | Typo in UI |

---

### 7. SLO Tracking

Define and track Service Level Objectives with error budgets.

```python
from agents.monitoring.agent import SLOManager

manager = SLOManager()

# Create SLO
slo = manager.create_slo(
    service="api",
    metric="availability",
    target=99.9,
    window_days=30
)
# Returns: SLO(slo_id="slo_abc123", target=99.9, ...)

# Update current value
manager.update_slo(slo.slo_id, current_value=99.95)

# Get burn rate (how fast we're consuming error budget)
burn_rate = manager.get_burn_rate(slo.slo_id)
# 0.0 (not consuming budget - we're above target)

# Check error budget
slo = manager.get_slo(slo.slo_id)
# {
#   'slo_id': 'slo_abc123',
#   'service': 'api',
#   'metric': 'availability',
#   'target': 99.9,
#   'current_value': 99.95,
#   'error_budget_total': 0.1,
#   'error_budget_consumed': 0.0,
#   'error_budget_remaining': 100.0,
#   'burn_rate': 0.0
# }

# Simulate degradation
manager.update_slo(slo.slo_id, current_value=99.85)
slo = manager.get_slo(slo.slo_id)
# error_budget_remaining: 50.0 (half budget consumed)
# burn_rate: 2.0 (consuming twice as fast as expected)
```

---

## Data Models

### Alert
| Field | Type | Description |
|-------|------|-------------|
| alert_id | str | Unique identifier |
| rule_id | str | Triggering rule |
| severity | AlertSeverity | Impact level (CRITICAL, HIGH, MEDIUM, LOW, INFO) |
| status | AlertStatus | Lifecycle state (FIRING, ACKNOWLEDGED, RESOLVED, SILENCED) |
| message | str | Human-readable message |
| created_at | datetime | Alert creation time |
| acknowledged_by | str | Acknowledged by user |
| resolved_at | datetime | Resolution time |

### Incident
| Field | Type | Description |
|-------|------|-------------|
| incident_id | str | Unique identifier |
| title | str | Incident title |
| severity | IncidentSeverity | SEV1-SEV4 |
| status | IncidentStatus | Current state |
| description | str | Detailed description |
| affected_services | List[str] | Impacted services |
| related_alerts | List[str] | Related alert IDs |
| timeline | List[Dict] | Event history |
| created_at | datetime | Creation time |
| resolved_at | datetime | Resolution time |

### SLO
| Field | Type | Description |
|-------|------|-------------|
| slo_id | str | Unique identifier |
| service | str | Service name |
| metric | str | Metric being tracked |
| target | float | Target percentage |
| current_value | float | Current measurement |
| window_days | int | Measurement window |
| error_budget_total | float | Total error budget |
| error_budget_consumed | float | Consumed budget |
| error_budget_remaining | float | Remaining budget |
| burn_rate | float | Current burn rate |

---

## Checklists

### Monitoring Setup
- [ ] Core metrics defined (request rate, error rate, latency)
- [ ] Alert rules configured for each metric
- [ ] Uptime checks added for all endpoints
- [ ] Log patterns defined for errors and warnings
- [ ] Dashboards created for each service
- [ ] Notification channels tested
- [ ] Escalation policies configured
- [ ] Runbooks linked in alert annotations

### Incident Response
- [ ] Incident created with severity and description
- [ ] Affected services documented
- [ ] Related alerts linked
- [ ] Timeline updated at each step
- [ ] Resolution documented
- [ ] Post-mortem scheduled (for SEV1/SEV2)
- [ ] Action items assigned
- [ ] Follow-up date set

### SLO Definition
- [ ] Service identified
- [ ] Metric chosen (availability, latency, error rate)
- [ ] Target percentage set (99.9% not 99.99%)
- [ ] Measurement window defined
- [ ] Error budget calculated
- [ ] Burn rate alert configured
- [ ] Review cadence established

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Alerts not firing | Rule expression invalid | Validate PromQL syntax |
| High alert noise | Thresholds too sensitive | Adjust thresholds, add `for` duration |
| Dashboard empty | Metrics not scraped | Check metric definitions and scrape config |
| Log patterns not matching | Regex too strict | Test regex against sample logs |
| SLO shows 100% when errors exist | Wrong metric name | Verify metric matches actual data |
| Incident MTTR is None | Not resolved yet | Resolve incident to calculate MTTR |
| Uptime shows 100% with outages | Checks not running | Verify check interval configuration |
| Notifications not sent | Channel not configured | Check notification routing |
| Burn rate negative | Current value above target | Expected - budget not being consumed |
| Dashboard export fails | No panels added | Add at least one panel before export |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

agent = MonitoringAgent()
# Now all operations will log detailed debug information
```

---

## Integration Points

| System | Purpose |
|--------|---------|
| Prometheus | Metrics collection and querying |
| Grafana | Dashboard visualization |
| PagerDuty | Critical incident alerting |
| Slack | Team notifications |
| ELK/Loki | Log aggregation and search |
| OpsGenie | On-call management |
| StatusPage | Public status communication |
| Jira | Incident tracking integration |
| Datadog | APM and infrastructure monitoring |

---

## Advanced Usage

### Custom Metric Labels
```python
metrics.define_counter("http_requests", "HTTP requests", ["method", "status", "endpoint"])

# Record with multiple labels
metrics.inc_counter("http_requests", labels={
    "method": "GET",
    "status": "200",
    "endpoint": "/api/users"
})
```

### Alert with Runbook
```python
rule = alerts.add_rule(
    "HighLatency",
    "histogram_quantile(0.99, rate(http_duration[5m])) > 1.0",
    AlertSeverity.HIGH,
    annotations={
        "summary": "p99 latency > 1s",
        "runbook": "https://wiki/runbook/latency",
        "dashboard": "https://grafana/d/abc123"
    }
)
```

### Multi-Window SLO
```python
# 30-day availability SLO
slo_30d = slos.create_slo("api", "availability", 99.9, window_days=30)

# 7-day availability SLO (for faster detection)
slo_7d = slos.create_slo("api", "availability", 99.9, window_days=7)
```
