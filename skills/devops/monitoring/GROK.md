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