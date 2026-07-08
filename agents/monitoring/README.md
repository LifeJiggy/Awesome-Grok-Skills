# Monitoring Agent

Infrastructure monitoring, alerting, APM, log aggregation, dashboards, and incident correlation.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

The Monitoring Agent provides complete infrastructure observability covering metrics collection, alerting, uptime monitoring, log aggregation, dashboard visualization, incident management, and SLO tracking.

### Key Capabilities

| Capability | Description |
|-----------|-------------|
| Metrics Collection | Prometheus-style counters, gauges, histograms |
| Alert Management | Rule definition, firing, acknowledgment, resolution |
| Uptime Monitoring | Endpoint availability and response time tracking |
| Log Monitoring | Ingestion, pattern matching, search, analysis |
| Dashboards | Multi-panel visualization with export |
| Incident Management | Full lifecycle with timeline and MTTR |
| SLO Tracking | Error budgets and burn rate monitoring |

---

## Features

### Metrics
- Counter, gauge, and histogram metric types
- Label-based metric dimensions
- Histogram bucket configuration
- Prometheus-compatible scrape output

### Alerting
- 5 severity levels with notification routing
- Alert lifecycle: firing → acknowledged → resolved
- Silence capability for maintenance windows
- Rule-based alert generation

### Uptime
- Configurable health checks (URL, method, expected status)
- Response time tracking
- Uptime percentage calculation
- Multi-hour window analysis

### Logs
- Regex-based pattern matching
- Multi-level log ingestion (debug to critical)
- Source-based filtering
- Error rate and volume analysis

### Dashboards
- 6 panel types (graph, singlestat, table, heatmap, bar, pie)
- Configurable refresh intervals
- JSON export for Grafana import
- Multi-panel composition

### Incidents
- 4 severity levels (SEV1-SEV4)
- Status workflow: open → investigating → identified → monitoring → resolved
- Full event timeline
- MTTR calculation

### SLOs
- Target-based objective definition
- Error budget tracking
- Burn rate calculation
- Multi-window analysis

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│           MonitoringAgent (Facade)               │
├─────────────────────────────────────────────────┤
│  PrometheusMetrics  │  AlertManager             │
│  UptimeMonitor      │  LogMonitor               │
│  DashboardGenerator │  IncidentManager          │
│  SLOManager                                 │
└─────────────────────────────────────────────────┘
```

---

## Quick Start

### Installation

```bash
pip install awesome-grok-skills
```

### Minimal Example

```python
from agents.monitoring.agent import MonitoringAgent, AlertSeverity

agent = MonitoringAgent()

# Define and record metrics
agent.metrics.define_counter("requests_total", "Total requests")
agent.metrics.inc_counter("requests_total")

# Add alert rule
rule = agent.alerts.add_rule("HighErrors", "errors > 10", AlertSeverity.HIGH)

# Check uptime
check = agent.uptime.add_check("API", "https://api.example.com/health")
agent.uptime.record_check(check.check_id, 200, 45, True)
```

---

## Usage

### Running the Agent

```bash
python agents/monitoring/agent.py
```

### Programmatic Access

```python
from agents.monitoring.agent import MonitoringAgent

agent = MonitoringAgent()

# Each component works independently
agent.metrics.define_gauge("cpu_usage", "CPU %")
agent.alerts.add_rule("HighCPU", "cpu > 90", AlertSeverity.HIGH)
agent.uptime.add_check("Web", "https://example.com")
agent.logs.add_pattern("Error", r"ERROR", AlertSeverity.HIGH)
```

---

## API Reference

### MonitoringAgent

| Method | Description |
|--------|-------------|
| `setup_full_monitoring(service, endpoints, rules)` | Complete monitoring setup |

### PrometheusMetrics

| Method | Description |
|--------|-------------|
| `define_counter(name, desc, labels)` | Define counter metric |
| `define_gauge(name, desc, labels)` | Define gauge metric |
| `define_histogram(name, desc, buckets)` | Define histogram metric |
| `inc_counter(name, value, labels)` | Increment counter |
| `set_gauge(name, value, labels)` | Set gauge value |
| `observe_histogram(name, value)` | Record histogram value |
| `scrape()` | Export all metrics |

### AlertManager

| Method | Description |
|--------|-------------|
| `add_rule(name, expr, severity)` | Create alert rule |
| `fire_alert(rule_id, message)` | Fire alert |
| `acknowledge_alert(alert_id, by)` | Acknowledge alert |
| `resolve_alert(alert_id)` | Resolve alert |
| `get_active_alerts()` | List active alerts |

### UptimeMonitor

| Method | Description |
|--------|-------------|
| `add_check(name, url, method, status)` | Add health check |
| `record_check(check_id, status, time, success)` | Record result |
| `get_uptime(check_id, hours)` | Get uptime stats |
| `get_status_summary()` | Overall status |

### LogMonitor

| Method | Description |
|--------|-------------|
| `add_pattern(name, regex, severity)` | Add log pattern |
| `ingest(message, source, level)` | Ingest log entry |
| `search(query, level, source, since)` | Search logs |
| `get_error_summary(hours)` | Error summary |

### DashboardGenerator

| Method | Description |
|--------|-------------|
| `create_dashboard(title, refresh)` | Create dashboard |
| `add_panel(dash_id, title, type, metrics)` | Add panel |
| `export_json(dash_id)` | Export as JSON |

### IncidentManager

| Method | Description |
|--------|-------------|
| `create_incident(title, severity, desc)` | Create incident |
| `update_status(inc_id, status, note)` | Update status |
| `resolve_incident(inc_id, resolution)` | Resolve |
| `get_mttr(inc_id)` | Get MTTR |

### SLOManager

| Method | Description |
|--------|-------------|
| `create_slo(service, metric, target, window)` | Create SLO |
| `update_slo(slo_id, current_value)` | Update value |
| `get_burn_rate(slo_id)` | Get burn rate |

---

## Examples

### Full Monitoring Setup

```python
agent = MonitoringAgent()

result = agent.setup_full_monitoring(
    service_name="api",
    endpoints=[
        {"name": "API Health", "url": "https://api.example.com/health"},
        {"name": "API Docs", "url": "https://api.example.com/docs"},
    ],
    alert_rules=[
        {"name": "HighErrorRate", "expression": "rate(errors[5m]) > 0.05", "severity": "high"},
        {"name": "HighLatency", "expression": "p99_latency > 1.0", "severity": "medium"},
    ]
)
print(f"Dashboard: {result['dashboard_id']}")
```

### Incident Response Flow

```python
agent = MonitoringAgent()

# Alert fires
rule = agent.alerts.add_rule("DBDown", "db_up == 0", AlertSeverity.CRITICAL)
alert = agent.alerts.fire_alert(rule.rule_id, "Database unreachable")

# Create incident
incident = agent.incidents.create_incident(
    "Database Outage", IncidentSeverity.SEV1,
    "Primary database unreachable",
    related_alerts=[alert.alert_id]
)

# Track resolution
agent.incidents.update_status(incident.incident_id, IncidentStatus.INVESTIGATING)
agent.incidents.update_status(incident.incident_id, IncidentStatus.IDENTIFIED, "Replica failed over")
agent.incidents.resolve_incident(incident.incident_id, "Failover completed")

print(f"MTTR: {agent.incidents.get_mttr(incident.incident_id)} minutes")
```

### SLO Monitoring

```python
agent = MonitoringAgent()

slo = agent.slos.create_slo("api", "availability", 99.95, window_days=30)
agent.slos.update_slo(slo.slo_id, current_value=99.97)

slo = agent.slos.get_slo(slo.slo_id)
print(f"Error budget remaining: {slo.error_budget_remaining}%")
print(f"Burn rate: {agent.slos.get_burn_rate(slo.slo_id)}")
```

---

## Configuration

### Metric Types

| Type | Use Case | Example |
|------|----------|---------|
| COUNTER | Request count | `http_requests_total` |
| GAUGE | Current connections | `active_connections` |
| HISTOGRAM | Request latency | `http_request_duration_seconds` |

### Alert Severity

| Level | Response | Channels |
|-------|----------|----------|
| CRITICAL | Immediate | PagerDuty + Slack + Email |
| HIGH | < 1 hour | Slack + Email |
| MEDIUM | < 4 hours | Slack |
| LOW | Next day | Email |
| INFO | No action | None |

### Incident Severity

| Level | Definition | Response |
|-------|-----------|----------|
| SEV1 | Business down | 15 min |
| SEV2 | Major degradation | 1 hour |
| SEV3 | Minor issue | 4 hours |
| SEV4 | Cosmetic | Next day |

---

## Best Practices

### Metrics
- Use consistent naming conventions (snake_case)
- Include meaningful labels for filtering
- Set appropriate histogram buckets
- Avoid high-cardinality labels

### Alerting
- Alert on symptoms, not causes
- Use `for` duration to avoid flapping
- Include runbook links in annotations
- Review and tune thresholds monthly

### Uptime
- Monitor from multiple locations
- Set realistic timeout values
- Track both uptime and response time
- Alert before users notice

### Logs
- Define patterns for known error types
- Keep log volume manageable
- Use structured logging when possible
- Redact PII before storage

### Dashboards
- Keep panels focused (one metric per panel)
- Use consistent time ranges
- Include text panels for context
- Share dashboards with team

### Incidents
- Create incidents for all SEV1/SEV2 alerts
- Update timeline at every step
- Link related alerts
- Conduct post-mortems for SEV1/SEV2

### SLOs
- Set realistic targets (99.9% not 99.99%)
- Use appropriate measurement windows
- Alert on burn rate, not just current value
- Review SLOs quarterly

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Alerts not firing | Invalid expression | Validate PromQL syntax |
| Too many alerts | Thresholds too low | Adjust thresholds, add `for` duration |
| Dashboard shows no data | Metrics not defined | Call `define_*` before recording |
| Log patterns miss errors | Regex too strict | Test regex against sample logs |
| SLO shows 100% with errors | Wrong metric | Verify metric name matches data |
| Uptime shows 100% with outages | Checks not running | Verify interval configuration |
| Incident MTTR is None | Not resolved | Resolve incident to calculate |
| Notifications not sent | Channel not configured | Check notification routing |

---

## License

MIT License - see [LICENSE](../../LICENSE) for details.
