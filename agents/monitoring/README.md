# Monitoring Agent

Infrastructure monitoring, alerting, APM, log aggregation, dashboards, and incident correlation.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Contributing](#contributing)
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
| Dashboards | Multi-panel visualization with Grafana export |
| Incident Management | Full lifecycle with timeline and MTTR |
| SLO Tracking | Error budgets and burn rate monitoring |

### System Requirements

- Python 3.10 or higher
- 512 MB RAM minimum
- 200 MB disk space (for log storage)
- Network access for external notifications (optional)

---

## Features

### Metrics
- Counter, gauge, and histogram metric types
- Label-based metric dimensions
- Histogram bucket configuration
- Prometheus-compatible scrape output
- Multi-label support for complex metrics
- Incremental counter updates

### Alerting
- 5 severity levels with notification routing
- Alert lifecycle: firing → acknowledged → resolved
- Silence capability for maintenance windows
- Rule-based alert generation with PromQL-like expressions
- Configurable `for` duration to prevent flapping
- Runbook links in alert annotations

### Uptime
- Configurable health checks (URL, method, expected status)
- Response time tracking per check
- Uptime percentage calculation
- Multi-hour window analysis
- Overall status summary

### Logs
- Regex-based pattern matching
- Multi-level log ingestion (debug to critical)
- Source-based filtering
- Error rate and volume analysis
- Pattern-based severity mapping
- Time-range search

### Dashboards
- 6 panel types (graph, singlestat, table, heatmap, bar, pie)
- Configurable refresh intervals
- JSON export for Grafana import
- Multi-panel composition
- Metric-based panel data

### Incidents
- 4 severity levels (SEV1-SEV4)
- Status workflow: open → investigating → identified → monitoring → resolved
- Full event timeline with timestamps
- MTTR calculation
- Related alert linking
- Affected services tracking

### SLOs
- Target-based objective definition
- Error budget tracking (total, consumed, remaining)
- Burn rate calculation
- Multi-window analysis support
- Service-level granularity

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│           MonitoringAgent (Facade)                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │PrometheusMetrics│  │ AlertManager   │  │ UptimeMonitor  │    │
│  │                │  │                │  │                │    │
│  │ Counters       │  │ Rules          │  │ Health Checks  │    │
│  │ Gauges         │  │ Firing         │  │ Response Time  │    │
│  │ Histograms     │  │ Routing        │  │ Uptime %       │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │  LogMonitor    │  │DashboardGeneratr│  │IncidentManager │    │
│  │                │  │                │  │                │    │
│  │ Patterns       │  │ Panels         │  │ Lifecycle      │    │
│  │ Search         │  │ Layout         │  │ Timeline       │    │
│  │ Analysis       │  │ Export         │  │ MTTR           │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
│                                                                  │
│  ┌────────────────┐                                             │
│  │  SLOManager    │                                             │
│  │                │                                             │
│  │ Objectives     │                                             │
│  │ Error Budget   │                                             │
│  │ Burn Rate      │                                             │
│  └────────────────┘                                             │
└─────────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

```
Monitoring Request
     │
     ▼
MonitoringAgent (facade)
     │
     ├──→ PrometheusMetrics.define_counter()
     │         │
     │         ▼
     │    Counter defined
     │
     ├──→ PrometheusMetrics.inc_counter()
     │         │
     │         ▼
     │    Value recorded
     │
     ├──→ AlertManager.add_rule()
     │         │
     │         ▼
     │    Rule created
     │
     ├──→ AlertManager.fire_alert()
     │         │
     │         ▼
     │    Alert fired → Notification sent
     │
     ├──→ IncidentManager.create_incident()
     │         │
     │         ▼
     │    Incident (OPEN)
     │
     ├──→ IncidentManager.resolve_incident()
     │         │
     │         ▼
     │    Incident (RESOLVED)
     │
     └──→ SLOManager.create_slo()
               │
               ▼
          SLO defined
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

# Get status
summary = agent.uptime.get_status_summary()
print(f"Status: {summary['overall_status']}")
```

### 60-Second Setup

```python
from agents.monitoring.agent import MonitoringAgent, AlertSeverity

agent = MonitoringAgent()

# Quick metrics
agent.metrics.define_counter("hits", "Page hits")
agent.metrics.inc_counter("hits")

# Quick alert
agent.alerts.add_rule("TooManyHits", "hits > 1000", AlertSeverity.HIGH)

# Quick uptime check
agent.uptime.add_check("Web", "https://example.com")

print("Monitoring configured!")
```

---

## Installation

### From PyPI

```bash
pip install awesome-grok-skills
```

### From Source

```bash
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e .
```

### Requirements

```
Python >= 3.10
No external dependencies (stdlib only)
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

### CLI Usage

```bash
# List all alerts
python agents/monitoring/agent.py --list-alerts

# Check uptime
python agents/monitoring/agent.py --uptime api-health

# Generate dashboard
python agents/monitoring/agent.py --generate-dashboard "Production"
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
| `add_rule(name, expr, severity, for_duration, labels)` | Create alert rule |
| `fire_alert(rule_id, message)` | Fire alert |
| `acknowledge_alert(alert_id, by)` | Acknowledge alert |
| `resolve_alert(alert_id)` | Resolve alert |
| `silence_alert(alert_id, duration)` | Silence alert |
| `get_active_alerts()` | List active alerts |

### UptimeMonitor

| Method | Description |
|--------|-------------|
| `add_check(name, url, method, status, timeout, interval)` | Add health check |
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
| `create_incident(title, severity, desc, affected, alerts)` | Create incident |
| `update_status(inc_id, status, note)` | Update status |
| `resolve_incident(inc_id, resolution)` | Resolve |
| `get_mttr(inc_id)` | Get MTTR |
| `get_timeline(inc_id)` | Get timeline |

### SLOManager

| Method | Description |
|--------|-------------|
| `create_slo(service, metric, target, window)` | Create SLO |
| `update_slo(slo_id, current_value)` | Update value |
| `get_burn_rate(slo_id)` | Get burn rate |
| `get_slo(slo_id)` | Get SLO details |

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
    "Database Outage",
    IncidentSeverity.SEV1,
    "Primary database unreachable",
    affected_services=["api", "web"],
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

# Create SLO
slo = agent.slos.create_slo("api", "availability", 99.95, window_days=30)

# Update and check
agent.slos.update_slo(slo.slo_id, current_value=99.97)
slo = agent.slos.get_slo(slo.slo_id)

print(f"Error budget remaining: {slo.error_budget_remaining}%")
print(f"Burn rate: {agent.slos.get_burn_rate(slo.slo_id)}")

# Simulate degradation
agent.slos.update_slo(slo.slo_id, current_value=99.90)
slo = agent.slos.get_slo(slo.slo_id)
print(f"Budget consumed: {100 - slo.error_budget_remaining}%")
```

### Dashboard with Multiple Panels

```python
agent = MonitoringAgent()

# Create dashboard
dashboard = agent.dashboards.create_dashboard("API Overview", refresh_interval=15)

# Add panels
agent.dashboards.add_panel(dashboard.dashboard_id, "Request Rate", DashboardPanelType.GRAPH, ["http_requests"])
agent.dashboards.add_panel(dashboard.dashboard_id, "Error Rate", DashboardPanelType.GRAPH, ["http_errors"])
agent.dashboards.add_panel(dashboard.dashboard_id, "Active Connections", DashboardPanelType.SINGLESTAT, ["connections"])
agent.dashboards.add_panel(dashboard.dashboard_id, "Latency Distribution", DashboardPanelType.HEATMAP, ["latency"])
agent.dashboards.add_panel(dashboard.dashboard_id, "Status Codes", DashboardPanelType.PIE, ["status_codes"])

# Export for Grafana
json_config = agent.dashboards.export_json(dashboard.dashboard_id)
```

### Log Pattern Analysis

```python
agent = MonitoringAgent()

# Define patterns
agent.logs.add_pattern("DBError", r"Database.*error", AlertSeverity.HIGH)
agent.logs.add_pattern("AuthFailure", r"Authentication failed", AlertSeverity.MEDIUM)
agent.logs.add_pattern("RateLimit", r"Rate limit exceeded", AlertSeverity.LOW)

# Ingest logs
agent.logs.ingest("ERROR: Database connection timeout", source="api", level=LogLevel.ERROR)
agent.logs.ingest("WARNING: Authentication failed for user admin", source="auth", level=LogLevel.WARNING)

# Get error summary
summary = agent.logs.get_error_summary(hours=1)
print(f"Total errors: {summary['total_errors']}")
print(f"By pattern: {summary['by_pattern']}")
```

---

## Configuration

### Metric Types

| Type | Use Case | Example |
|------|----------|---------|
| COUNTER | Request count, errors, bytes transferred | `http_requests_total` |
| GAUGE | Current connections, temperature, queue depth | `active_connections` |
| HISTOGRAM | Request latency, response size, duration | `http_request_duration_seconds` |

### Alert Severity

| Level | Response | Channels | Example |
|-------|----------|----------|---------|
| CRITICAL | Immediate | PagerDuty + Slack + Email | Service down |
| HIGH | < 1 hour | Slack + Email | High error rate |
| MEDIUM | < 4 hours | Slack | Elevated latency |
| LOW | Next day | Email | Disk space warning |
| INFO | No action | None | Deployment completed |

### Incident Severity

| Level | Definition | Response | Example |
|-------|-----------|----------|---------|
| SEV1 | Business down | 15 min | Complete outage |
| SEV2 | Major degradation | 1 hour | Payment failures |
| SEV3 | Minor issue | 4 hours | UI bug |
| SEV4 | Cosmetic | Next day | Typo |

### Dashboard Panel Types

| Type | Best For | Data Format |
|------|----------|-------------|
| GRAPH | Time-series trends | List of values over time |
| SINGLESTAT | Current values | Single numeric value |
| TABLE | Detailed data | List of rows |
| HEATMAP | Distribution | 2D distribution |
| BAR | Category comparison | Categories + values |
| PIE | Proportion | Categories + percentages |

### Uptime Check Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| name | Check name | Required |
| url | URL to check | Required |
| method | HTTP method | GET |
| expected_status | Expected status code | 200 |
| timeout | Timeout in seconds | 10 |
| interval | Check interval in seconds | 60 |

---

## Best Practices

### Metrics
- Use consistent naming conventions (snake_case)
- Include meaningful labels for filtering
- Set appropriate histogram buckets
- Avoid high-cardinality labels
- Use counters for rates, gauges for current values
- Document metric purpose in description

### Alerting
- Alert on symptoms, not causes
- Use `for` duration to avoid flapping
- Include runbook links in annotations
- Review and tune thresholds monthly
- Set up escalation policies
- Test alerts regularly

### Uptime
- Monitor from multiple locations
- Set realistic timeout values
- Track both uptime and response time
- Alert before users notice
- Use different intervals per criticality
- Include error body in failure logs

### Logs
- Define patterns for known error types
- Keep log volume manageable
- Use structured logging when possible
- Redact PII before storage
- Set up log retention policies
- Index critical fields

### Dashboards
- Keep panels focused (one metric per panel)
- Use consistent time ranges
- Include text panels for context
- Share dashboards with team
- Use variable templates for flexibility
- Export and version control

### Incidents
- Create incidents for all SEV1/SEV2 alerts
- Update timeline at every step
- Link related alerts
- Conduct post-mortems for SEV1/SEV2
- Track action items to completion
- Share learnings with team

### SLOs
- Set realistic targets (99.9% not 99.99%)
- Use appropriate measurement windows
- Alert on burn rate, not just current value
- Review SLOs quarterly
- Align SLOs with business objectives
- Document exceptions

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
| Histogram buckets wrong | Incorrect bucket config | Review bucket boundaries |
| Burn rate negative | Value above target | Expected - budget not consumed |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

agent = MonitoringAgent()
# Now all operations will log detailed debug information
```

---

## FAQ

### Q: Can I use components independently?
A: Yes, each component (PrometheusMetrics, AlertManager, etc.) can be used standalone without the MonitoringAgent facade.

### Q: What's the difference between counter and gauge?
A: Counter only increases (e.g., total requests). Gauge can go up and down (e.g., current connections).

### Q: How do I prevent alert flapping?
A: Use the `for_duration` parameter to require sustained breach before firing.

### Q: Can I export dashboards to Grafana?
A: Yes, use `export_json()` to get Grafana-compatible JSON.

### Q: How do I calculate MTTR?
A: Resolve the incident first, then call `get_mttr()`.

### Q: What's a burn rate?
A: How fast you're consuming your error budget. 1.0 = normal, 2.0 = twice as fast.

---

## Contributing

We welcome contributions! Please see our [Contributing Guide](../../CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e ".[dev]"
pre-commit install
```

### Running Tests

```bash
pytest tests/monitoring/
pytest --cov=agents.monitoring
```

---

## License

MIT License - see [LICENSE](../../LICENSE) for details.

---

## Support

- Documentation: [docs.example.com](https://docs.example.com)
- Issues: [GitHub Issues](https://github.com/awesome-grok-skills/awesome-grok-skills/issues)
- Discussions: [GitHub Discussions](https://github.com/awesome-grok-skills/awesome-grok-skills/discussions)
