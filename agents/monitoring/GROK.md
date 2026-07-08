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

---

## Capabilities

### 1. Prometheus Metrics

Collect counters, gauges, and histograms in Prometheus format.

```python
from agents.monitoring.agent import PrometheusMetrics, MetricType

metrics = PrometheusMetrics()

# Define metrics
metrics.define_counter("http_requests_total", "Total HTTP requests", ["method", "status"])
metrics.define_gauge("active_connections", "Current connections")
metrics.define_histogram("http_request_duration_seconds", "Request latency")

# Record
metrics.inc_counter("http_requests_total", labels={"method": "GET", "status": "200"})
metrics.set_gauge("active_connections", 42)
metrics.observe_histogram("http_request_duration_seconds", 0.25)

# Scrape
data = metrics.scrape()
# {'http_requests_total{method="GET",status="200"}': 1, 'active_connections': 42, ...}
```

**Metric Types**:
| Type | Use Case | Behavior |
|------|----------|----------|
| COUNTER | Request count, errors | Monotonically increasing |
| GAUGE | Connections, temperature | Can go up and down |
| HISTOGRAM | Latency, response size | Distribution tracking |

---

### 2. Alert Management

Define rules, fire alerts, and route notifications.

```python
from agents.monitoring.agent import AlertManager, AlertSeverity

manager = AlertManager()

# Add rule
rule = manager.add_rule(
    name="HighErrorRate",
    expression="rate(http_errors[5m]) > 0.05",
    severity=AlertSeverity.HIGH,
    for_duration="5m",
    labels={"service": "api"},
    annotations={"summary": "Error rate exceeded 5%"}
)

# Fire alert
alert = manager.fire_alert(rule.rule_id, "Error rate at 7.2%")

# Acknowledge and resolve
manager.acknowledge_alert(alert.alert_id, acknowledged_by="oncall")
manager.resolve_alert(alert.alert_id)

# Get active alerts
active = manager.get_active_alerts()
```

**Severity Routing**:
| Severity | Channels |
|----------|----------|
| CRITICAL | PagerDuty + Slack + Email |
| HIGH | Slack + Email |
| MEDIUM | Slack |
| LOW | Email |
| INFO | (none) |

---

### 3. Uptime Monitoring

Track endpoint availability and response times.

```python
from agents.monitoring.agent import UptimeMonitor

monitor = UptimeMonitor()

# Add check
check = monitor.add_check(
    name="API Health",
    url="https://api.example.com/health",
    method="GET",
    expected_status=200,
    timeout=10,
    interval=60
)

# Record result
monitor.record_check(check.check_id, status_code=200, response_time_ms=45, success=True)

# Get uptime
uptime = monitor.get_uptime(check.check_id, hours=24)
# {'uptime_percent': 99.95, 'total_checks': 1440, 'avg_response_ms': 42.3}

# Status summary
summary = monitor.get_status_summary()
# {'total_checks': 5, 'healthy': 4, 'unhealthy': 1}
```

---

### 4. Log Monitoring

Ingest, search, and analyze application logs.

```python
from agents.monitoring.agent import LogMonitor, AlertSeverity, LogLevel

monitor = LogMonitor()

# Add patterns
monitor.add_pattern("DBError", r"Database.*error", AlertSeverity.HIGH)
monitor.add_pattern("OOM", r"OutOfMemory", AlertSeverity.CRITICAL)

# Ingest logs
monitor.ingest("ERROR: Database connection timeout", source="api", level=LogLevel.ERROR)
monitor.ingest("INFO: Request processed", source="api", level=LogLevel.INFO)

# Search
results = monitor.search("Database", level=LogLevel.ERROR)

# Error summary
summary = monitor.get_error_summary(hours=1)
# {'total_errors': 1, 'by_pattern': {'pat_abc': 1}, 'error_rate': 50.0}
```

---

### 5. Dashboard Creation

Build monitoring dashboards with multiple panel types.

```python
from agents.monitoring.agent import DashboardGenerator, DashboardPanelType

gen = DashboardGenerator()

# Create dashboard
dashboard = gen.create_dashboard("Production Overview", refresh_interval=15)

# Add panels
gen.add_panel(dashboard.dashboard_id, "Request Rate", DashboardPanelType.GRAPH, ["http_requests_total"])
gen.add_panel(dashboard.dashboard_id, "Active Users", DashboardPanelType.SINGLESTAT, ["active_connections"])
gen.add_panel(dashboard.dashboard_id, "Error Distribution", DashboardPanelType.PIE, ["http_errors"])

# Export
config = gen.export_json(dashboard.dashboard_id)
```

**Panel Types**:
| Type | Best For |
|------|----------|
| GRAPH | Time-series trends |
| SINGLESTAT | Current values |
| TABLE | Detailed data |
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
    description="Primary database unreachable",
    affected_services=["api", "web"],
    related_alerts=[alert.alert_id]
)

# Track progress
manager.update_status(incident.incident_id, IncidentStatus.INVESTIGATING, "Checking connection pool")
manager.update_status(incident.incident_id, IncidentStatus.IDENTIFIED, "Connection pool exhausted")

# Resolve
manager.resolve_incident(incident.incident_id, "Pool size increased from 10 to 50")

# MTTR
mttr = manager.get_mttr(incident.incident_id)  # minutes
```

**Incident Severity**:
| Level | Definition | Response Time |
|-------|-----------|--------------|
| SEV1 | Critical business impact | 15 minutes |
| SEV2 | Major feature degraded | 1 hour |
| SEV3 | Minor issue | 4 hours |
| SEV4 | Cosmetic | Next business day |

---

### 7. SLO Tracking

Define and track Service Level Objectives with error budgets.

```python
from agents.monitoring.agent import SLOManager

manager = SLOManager()

# Create SLO
slo = manager.create_slo(service="api", metric="availability", target=99.9, window_days=30)

# Update current value
manager.update_slo(slo.slo_id, current_value=99.95)

# Get burn rate
burn_rate = manager.get_burn_rate(slo.slo_id)  # 0.0 = not consuming budget

# Check error budget
slo = manager.get_slo(slo.slo_id)
# error_budget_remaining: 100.0%
```

---

## Data Models

### Alert
| Field | Type | Description |
|-------|------|-------------|
| alert_id | str | Unique identifier |
| rule_id | str | Triggering rule |
| severity | AlertSeverity | Impact level |
| status | AlertStatus | Lifecycle state |
| message | str | Human-readable message |

### Incident
| Field | Type | Description |
|-------|------|-------------|
| incident_id | str | Unique identifier |
| severity | IncidentSeverity | SEV1-SEV4 |
| status | IncidentStatus | Current state |
| affected_services | List[str] | Impacted services |
| timeline | List[Dict] | Event history |

### SLO
| Field | Type | Description |
|-------|------|-------------|
| slo_id | str | Unique identifier |
| service | str | Service name |
| target | float | Target percentage |
| current_value | float | Current measurement |
| error_budget_remaining | float | Budget left % |

---

## Checklists

### Monitoring Setup
- [ ] Core metrics defined (request rate, error rate, latency)
- [ ] Alert rules configured for each metric
- [ ] Uptime checks added for all endpoints
- [ ] Log patterns defined for errors and warnings
- [ ] Dashboards created for each service
- [ ] Notification channels tested

### Incident Response
- [ ] Incident created with severity and description
- [ ] Affected services documented
- [ ] Related alerts linked
- [ ] Timeline updated at each step
- [ ] Resolution documented
- [ ] Post-mortem scheduled (for SEV1/SEV2)

### SLO Definition
- [ ] Service identified
- [ ] Metric chosen (availability, latency, error rate)
- [ ] Target percentage set
- [ ] Measurement window defined
- [ ] Error budget calculated
- [ ] Burn rate alert configured

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

---

## Integration Points

| System | Purpose |
|--------|---------|
| Prometheus | Metrics collection |
| Grafana | Dashboard visualization |
| PagerDuty | Incident alerting |
| Slack | Team notifications |
| ELK/Loki | Log aggregation |
| OpsGenie | On-call management |
| StatusPage | Public status |
