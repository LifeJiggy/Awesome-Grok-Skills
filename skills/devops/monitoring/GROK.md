---
name: "Monitoring & Observability"
version: "2.0.0"
description: "Comprehensive monitoring and observability toolkit with metrics collection, log aggregation, distributed tracing, alerting, and dashboarding for production system visibility"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["devops", "monitoring", "observability", "metrics", "logging", "tracing"]
category: "devops"
personality: "sre-engineer"
use_cases: ["metrics collection", "log aggregation", "distributed tracing", "alerting", "dashboarding"]
---

# Monitoring & Observability

> Production-grade monitoring framework providing metrics collection, log aggregation, distributed tracing, alerting, and dashboarding for comprehensive production system visibility.

## Overview

The Monitoring & Observability module provides a complete observability stack for production systems. It implements metrics collection with Prometheus/StatsD integration, centralized log aggregation with Elasticsearch/Loki, distributed tracing with OpenTelemetry, multi-channel alerting, and customizable dashboards. Every component includes health self-monitoring and scaling guidance.

## Core Capabilities

### 1. Metrics Collection
- Prometheus metrics exposition
- StatsD metrics aggregation
- Custom metric definitions
- Metric aggregation and rollup
- High-cardinality metric management

### 2. Log Aggregation
- Structured logging standards
- Log shipping and collection
- Log parsing and enrichment
- Log-based alerting
- Log retention management

### 3. Distributed Tracing
- OpenTelemetry integration
- Span creation and propagation
- Trace context propagation
- Sampling strategies
- Trace analysis and visualization

### 4. Alerting
- Multi-channel notifications (Slack, PagerDuty, email)
- Alert grouping and deduplication
- Escalation policies
- Alert silencing and maintenance windows
- Runbook integration

### 5. Dashboarding
- Real-time metric visualization
- Custom dashboard creation
- Template-based dashboards
- Dashboard sharing and embedding
- Mobile-friendly views

### 6. SLO Management
- SLI definition and tracking
- Error budget calculation
- SLO burn rate alerting
- Reliability reporting

## Usage Examples

### Metrics Collection

```python
from monitoring import MetricsCollector, MetricType

collector = MetricsCollector(backend="prometheus")

# Define and record metrics
collector.counter("http_requests_total", labels={"method": "GET", "status": "200"})
collector.histogram("http_request_duration_seconds", value=0.15, labels={"path": "/api"})
collector.gauge("active_connections", value=42)

# Query metrics
query = collector.query('rate(http_requests_total[5m])')
print(f"Request rate: {query.value:.1f} req/s")
```

### Log Aggregation

```python
from monitoring import LogAggregator, LogLevel

aggregator = LogAggregator(backend="elasticsearch")

# Ship structured logs
aggregator.log(
    level=LogLevel.INFO,
    message="Request processed",
    service="api-gateway",
    trace_id="abc123",
    duration_ms=150,
    status_code=200,
)

# Search logs
results = aggregator.search(
    query="service:api-gateway AND level:ERROR",
    time_range="1h",
)
print(f"Errors found: {results.count}")
```

### Distributed Tracing

```python
from monitoring import Tracer, SpanKind

tracer = Tracer(service_name="api-gateway")

# Create trace spans
with tracer.start_span("handle_request", kind=SpanKind.SERVER) as span:
    span.set_attribute("http.method", "GET")
    span.set_attribute("http.url", "/api/users")

    with tracer.start_span("auth_middleware") as child:
        child.set_attribute("user.id", "12345")

    with tracer.start_span("database_query") as child:
        child.set_attribute("db.statement", "SELECT * FROM users")

# Get trace
trace = tracer.get_trace()
print(f"Trace: {trace.trace_id}")
print(f"Duration: {trace.duration_ms:.1f}ms")
print(f"Spans: {len(trace.spans)}")
```

### Alerting

```python
from monitoring import AlertManager, AlertRule, Severity

manager = AlertManager()

# Create alert rules
manager.add_rule(AlertRule(
    name="high_error_rate",
    condition="rate(http_errors_total[5m]) > 0.05",
    severity=Severity.CRITICAL,
    channels=["slack-ops", "pagerduty-oncall"],
    runbook_url="https://wiki/runbooks/high-error-rate",
))

# Check alerts
alerts = manager.check_alerts()
print(f"Active alerts: {len(alerts)}")
for alert in alerts:
    print(f"  [{alert.severity.value}] {alert.name}: {alert.message}")
```

## Best Practices

### Metrics
- Use labels sparingly to avoid high cardinality
- Name metrics consistently (method, resource, unit)
- Record both counters and histograms
- Monitor metric collection health

### Logging
- Use structured logging (JSON format)
- Include trace context in logs
- Set appropriate log levels
- Implement log sampling for high-volume services

### Tracing
- Propagate trace context across service boundaries
- Sample traces in production (1-10%)
- Add meaningful attributes to spans
- Monitor trace completeness

### Alerting
- Alert on symptoms, not causes
- Use appropriate severity levels
- Include runbook links in alerts
- Test alert notifications regularly

## Related Modules

- **ci-cd-pipelines**: Pipeline monitoring integration
- **container-orchestration**: Kubernetes monitoring
- **site-reliability**: SRE metrics and practices
- **database-admin**: Database monitoring

---

## Advanced Configuration

### Custom Metric Definitions

```python
from monitoring import MetricDefinition, LabelConfig

MetricDefinition(
    name="http_request_duration_seconds",
    type="histogram",
    help="HTTP request latency",
    label_names=["method", "status", "path"],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0],
)
```

### Alert Rule Configuration

```python
from monitoring import AlertRule, Severity, Duration

rule = AlertRule(
    name="high_error_rate",
    condition="rate(http_errors_total[5m]) / rate(http_requests_total[5m]) > 0.05",
    severity=Severity.CRITICAL,
    for_duration=Duration(minutes=5),
    labels={"team": "backend"},
    annotations={"summary": "Error rate above 5%"},
    runbook_url="https://wiki/runbooks/high-error-rate",
)
```

## Architecture Patterns

### Three Pillars of Observability

```
Metrics (Prometheus)     Logs (Loki/ELK)      Traces (Jaeger/Tempo)
    Ã¢â€â€š                        Ã¢â€â€š                       Ã¢â€â€š
    Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€ËœÃ¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
                 Ã¢â€â€š
        Unified Dashboard (Grafana)
```

### Metric Types

```
Counter   Ã¢â€ â€™ Monotonically increasing (requests, errors)
Gauge     Ã¢â€ â€™ Can go up/down (connections, temperature)
Histogram Ã¢â€ â€™ Distribution of values (latency, size)
Summary    Ã¢â€ â€™ Pre-computed quantiles (p50, p95, p99)
```

## Integration Guide

### Grafana Dashboard

```python
from monitoring import GrafanaDashboard

dashboard = GrafanaDashboard(title="API Service")
dashboard.add_panel("Request Rate", 'rate(http_requests_total[5m])')
dashboard.add_panel("Error Rate", 'rate(http_errors_total[5m])')
dashboard.add_panel("Latency P99", 'histogram_quantile(0.99, http_request_duration_seconds_bucket)')
dashboard.upload("grafana-url", api_key="xxx")
```

### PagerDuty Integration

```python
from monitoring import PagerDutyIntegration

pd = PagerDutyIntegration(routing_key="your-routing-key")
pd.create_incident(title="High Error Rate", severity="critical", details={"error_rate": 0.08})
```

## Performance Optimization

| Optimization | Benefit |
|-------------|---------|
| Metric cardinality control | Prevents Prometheus OOM |
| Log sampling | Reduces log volume 90% |
| Trace sampling | 1-10% for cost control |
| Dashboard lazy loading | Faster UI rendering |
| Alert grouping | Reduces notification noise |

## Security Considerations

- **Metric endpoint auth**: Protect /metrics with authentication
- **Log redaction**: Remove PII from logs before shipping
- **Trace data sensitivity**: Scrub business data from spans
- **Alert routing encryption**: TLS for notification channels
- **Dashboard access control**: RBAC for Grafana dashboards

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Prometheus OOM | High cardinality labels | Reduce label combinations |
| Logs not appearing | Shipper misconfigured | Check agent configuration |
| Traces incomplete | Missing context propagation | Add trace headers middleware |
| Alert not firing | Wrong PromQL syntax | Test query in Prometheus UI |
| Dashboard slow | Too many panels | Reduce time range or panel count |

## API Reference

### MetricsCollector

```python
class MetricsCollector:
    def __init__(self, backend: str)
    def counter(self, name: str, value: float = 1, labels: dict = None) -> None
    def gauge(self, name: str, value: float, labels: dict = None) -> None
    def histogram(self, name: str, value: float, labels: dict = None) -> None
    def query(self, promql: str) -> QueryResult
```

### Tracer

```python
class Tracer:
    def __init__(self, service_name: str)
    def start_span(self, name: str, kind: SpanKind = None) -> Span
    def get_trace(self) -> Trace
    def inject_context(self, carrier: dict) -> dict
```

## Data Models

```python
from dataclasses import dataclass
from enum import Enum

class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

@dataclass
class Alert:
    name: str
    severity: Severity
    message: str
    fired_at: float
    resolved_at: float = None

@dataclass
class TraceSpan:
    name: str
    start_time: float
    end_time: float
    attributes: dict
    parent_id: str = None
```

## Deployment Guide

### Installation

```bash
pip install monitoring
# With Prometheus backend
pip install monitoring[prometheus]
```

### Stack Setup

```bash
# Prometheus
docker run -d -p 9090:9090 prom/prometheus

# Grafana
docker run -d -p 3000:3000 grafana/grafana

# Loki
docker run -d -p 3100:3100 grafana/loki
```

## Monitoring & Observability

```python
from monitoring import MetricsCollector

collector = MetricsCollector(backend="prometheus")
collector.counter("monitoring.health_check", 1)
collector.gauge("monitoring.active_alerts", count)
```

## Testing Strategy

```python
import pytest
from monitoring import MetricsCollector

def test_counter_increment():
    collector = MetricsCollector(backend="memory")
    collector.counter("test.counter")
    collector.counter("test.counter")
    assert collector.get_value("test.counter") == 2
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added OpenTelemetry | Configure OTLP exporter |
| 2.0.0 | New alert engine | Migrate alert rules |

## Glossary

| Term | Definition |
|------|-----------|
| **SLI** | Service Level Indicator Ã¢â‚¬â€ metric measuring service behavior |
| **SLO** | Service Level Objective Ã¢â‚¬â€ target for SLI |
| **PromQL** | Prometheus Query Language |
| **Span** | Unit of work in distributed tracing |
| **Cardinality** | Number of unique label combinations |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with Prometheus/StatsD
- Log aggregation with Elasticsearch/Loki
- OpenTelemetry distributed tracing
- Multi-channel alerting

## Contributing Guidelines

```bash
git clone https://github.com/example/monitoring.git
pip install -e ".[dev]"
pytest tests/
```

## Advanced Observability Patterns

### OpenTelemetry Integration

```python
from monitoring import OpenTelemetryExporter

exporter = OpenTelemetryExporter(
    endpoint="http://otel-collector:4317",
    service_name="api-gateway",
    resource_attributes={
        "deployment.environment": "production",
        "service.version": "2.1.0",
    },
    trace_sample_rate=0.1,
    metric_export_interval_ms=30000,
)

# Auto-instrument FastAPI
exporter.instrument_fastapi(app)

# Custom span creation
with exporter.start_span("process_payment") as span:
    span.set_attribute("payment.amount", 99.99)
    span.set_attribute("payment.currency", "USD")
    payment = payment_service.charge(amount=99.99)
    span.set_attribute("payment.id", payment.id)
```

### SLO-Driven Alerting

```python
from monitoring import SLOBasedAlerting

slo_alerting = SLOBasedAlerting(
    slo_targets=[
        {"name": "api_availability", "target": 99.9, "window_days": 30},
        {"name": "api_latency", "target": 99.5, "window_days": 30, "metric": "latency_p99_ms", "threshold": 500},
    ],
    burn_rate_thresholds=[
        {"window": "1h", "threshold": 14.4, "severity": "critical"},
        {"window": "6h", "threshold": 6.0, "severity": "warning"},
        {"window": "1d", "threshold": 3.0, "severity": "info"},
    ],
    notification_channels=["slack-sre", "pagerduty-oncall"],
)

# Check SLO status
status = slo_alerting.check()
for slo in status:
    print(f"  {slo.name}: {slo.error_budget_remaining_pct:.1f}% remaining")
    print(f"    Burn rate (1h): {slo.burn_rate_1h:.2f}x")
    print(f"    Status: {slo.status}")
```

### Log Analysis Pipeline

```python
from monitoring import LogAnalysisPipeline

pipeline = LogAnalysisPipeline(
    source="loki",
    rules=[
        {"name": "error_pattern", "query": '{level="ERROR"} | json', "alert": True},
        {"name": "slow_requests", "query": '{duration_ms > 5000}', "alert": True},
        {"name": "auth_failures", "query": '{message=~".*authentication.*failed.*"}', "alert": True},
    ],
    enrichment=[
        {"field": "service", "lookup": {"api": "API Gateway", "db": "Database"}},
        {"field": "severity", "map": {"ERROR": "critical", "WARN": "warning"}},
    ],
)

# Run analysis
results = pipeline.analyze(time_range="1h")
print(f"Total matches: {results.total}")
for rule in results.rule_results:
    print(f"  {rule.name}: {rule.match_count} matches")
```

### Anomaly Detection

```python
from monitoring import AnomalyDetector

detector = AnomalyDetector(
    algorithm="prophet",
    sensitivity=0.95,
    seasonality="daily",
)

# Train baseline
baseline = detector.train(
    metric="http_requests_total",
    lookback_days=30,
    resolution="5m",
)

# Detect anomalies
anomalies = detector.detect(
    metric="http_requests_total",
    time_range="1h",
)
for anomaly in anomalies:
    print(f"  [{anomaly.severity}] {anomaly.timestamp}")
    print(f"    Expected: {anomaly.expected:.0f}")
    print(f"    Actual: {anomaly.actual:.0f}")
    print(f"    Deviation: {anomaly.deviation:.2f} std dev")
```

### Distributed Tracing Visualization

```
Trace: abc123def456
Duration: 245.3ms
Spans: 8

[245ms] api-gateway (SERVER)
  Ã¢â€Å“Ã¢â€â‚¬[245ms] auth-middleware (INTERNAL)
  Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬[45ms] jwt-validation (INTERNAL)
  Ã¢â€Å“Ã¢â€â‚¬[180ms] route-handler (INTERNAL)
  Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬[120ms] database-query (CLIENT)
  Ã¢â€â€š   Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬[115ms] postgres-execute (DB)
  Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬[50ms] cache-get (CLIENT)
  Ã¢â€â€š       Ã¢â€â€Ã¢â€â‚¬[2ms] redis-get (DB)
  Ã¢â€â€Ã¢â€â‚¬[5ms] response-serialization (INTERNAL)
```

### Metrics Cardinality Management

```python
from monitoring import CardinalityManager

manager = CardinalityManager(
    max_cardinality=10000,
    tracking_window_hours=24,
)

# Monitor label cardinality
cardinality = manager.check("http_requests_total")
print(f"Current cardinality: {cardinality.current}")
print(f"Max allowed: {cardinality.max_allowed}")
print(f"Top labels by cardinality:")
for label in cardinality.top_labels:
    print(f"  {label.name}: {label.cardinality}")

# Auto-drop high-cardinality labels
manager.auto_drop(
    metric="http_requests_total",
    threshold=5000,
    protected_labels=["method", "status"],
)
```

### Alert Fatigue Reduction

```python
from monitoring import AlertManagerV2

manager = AlertManagerV2(
    grouping_rules=[
        {"match": {"service": "api-gateway"}, "group_wait_s": 30, "group_interval_s": 300},
        {"match": {"severity": "critical"}, "group_wait_s": 10, "group_interval_s": 60},
    ],
    inhibition_rules=[
        {"source": {"severity": "critical"}, "target": {"severity": "warning"}, "equal": ["service"]},
    ],
    silencing_rules=[
        {"match": {"maintenance_window": "true"}, "duration_s": 3600},
    ],
)

# Get alert fatigue metrics
fatigue = manager.get_fatigue_metrics(window_days=7)
print(f"Total alerts: {fatigue.total_alerts}")
print(f"Actions taken: {fatigue.actions_taken}")
print(f"Noise ratio: {fatigue.noise_ratio:.2%}")
print(f"Mean time to acknowledge: {fatigue.mtta_minutes:.1f}min")
```

### Prometheus Recording Rules

```python
from monitoring import RecordingRules

rules = RecordingRules(group="api_service")

rules.add(
    name="api_request_rate",
    expression="sum(rate(http_requests_total[5m])) by (method, status)",
    interval="30s",
)

rules.add(
    name="api_error_rate",
    expression="sum(rate(http_errors_total[5m])) / sum(rate(http_requests_total[5m]))",
    interval="30s",
)

rules.add(
    name="api_latency_p99",
    expression="histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
    interval="30s",
)

# Export rules
rules.export("recording_rules.yml")
```

### Grafana Dashboard Templates

```python
from monitoring import DashboardTemplate

template = DashboardTemplate(
    title="API Service Overview",
    templating=[
        {"name": "datasource", "type": "datasource", "query": "prometheus"},
        {"name": "service", "type": "query", "query": "label_values(http_requests_total, service)"},
    ],
    panels=[
        {"title": "Request Rate", "type": "graph", "query": 'sum(rate(http_requests_total{service="$service"}[5m]))'},
        {"title": "Error Rate", "type": "graph", "query": 'sum(rate(http_errors_total{service="$service"}[5m]))'},
        {"title": "Latency P99", "type": "graph", "query": 'histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{service="$service"}[5m])) by (le))'},
        {"title": "Active Connections", "type": "stat", "query": 'active_connections{service="$service"}'},
    ],
)

# Export to Grafana
template.export grafana_url="http://grafana:3000", api_key="xxx")
```

### Log Retention Policy

```python
from monitoring import LogRetentionPolicy

policy = LogRetentionPolicy(
    rules=[
        {"level": "ERROR", "retention_days": 90, "index": True},
        {"level": "WARN", "retention_days": 30, "index": True},
        {"level": "INFO", "retention_days": 14, "index": False},
        {"level": "DEBUG", "retention_days": 7, "index": False},
    ],
    storage_tiers=[
        {"tier": "hot", "days": 7, "storage": "ssd"},
        {"tier": "warm", "days": 30, "storage": "hdd"},
        {"tier": "cold", "days": 90, "storage": "s3"},
    ],
)

# Apply policy
policy.apply()
print(f"Logs archived: {policy.archived_count}")
print(f"Storage saved: {policy.storage_saved_gb:.1f}GB")
```

### Log Retention Policy

```python
from monitoring import LogRetentionPolicy

policy = LogRetentionPolicy(
    rules=[
        {"level": "ERROR", "retention_days": 90, "index": True},
        {"level": "WARN", "retention_days": 30, "index": True},
        {"level": "INFO", "retention_days": 14, "index": False},
        {"level": "DEBUG", "retention_days": 7, "index": False},
    ],
    storage_tiers=[
        {"tier": "hot", "days": 7, "storage": "ssd"},
        {"tier": "warm", "days": 30, "storage": "hdd"},
        {"tier": "cold", "days": 90, "storage": "s3"},
    ],
)

# Apply policy
policy.apply()
print(f"Logs archived: {policy.archived_count}")
print(f"Storage saved: {policy.storage_saved_gb:.1f}GB")
```

### Observability Cost Optimization

| Strategy | Savings | Implementation |
|----------|---------|----------------|
| Metric downsampling | 60-80% | Aggregate older metrics |
| Log level filtering | 70-90% | Drop DEBUG in production |
| Trace sampling | 80-95% | Head-based sampling |
| Dashboard optimization | 20-30% | Reduce panel queries |
| Alert deduplication | 40-60% | Group related alerts |
| Retention tiering | 50-70% | Cold storage for old data |

### Monitoring Stack Sizing Guide

| Component | Small (<10 services) | Medium (10-100) | Large (100+) |
|-----------|---------------------|-----------------|--------------|
| Prometheus | 2 CPU, 4GB RAM | 8 CPU, 32GB RAM | 16 CPU, 64GB RAM |
| Grafana | 1 CPU, 2GB RAM | 2 CPU, 4GB RAM | 4 CPU, 8GB RAM |
| Loki | 2 CPU, 4GB RAM | 8 CPU, 16GB RAM | 16 CPU, 32GB RAM |
| Tempo | 1 CPU, 2GB RAM | 4 CPU, 8GB RAM | 8 CPU, 16GB RAM |
| Alertmanager | 1 CPU, 1GB RAM | 2 CPU, 2GB RAM | 4 CPU, 4GB RAM |
| OTel Collector | 1 CPU, 1GB RAM | 4 CPU, 4GB RAM | 8 CPU, 8GB RAM |

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
