---
name: "api-monitoring"
category: "api"
version: "2.0.0"
tags: ["api", "monitoring", "analytics", "observability", "tracing", "metrics", "logging"]
---

# API Monitoring

## Overview

Comprehensive API monitoring and observability platform providing real-time metrics, distributed tracing, structured logging, error tracking, performance analytics, and SLA compliance monitoring. This module tracks request rates, latency percentiles (p50/p95/p99), error rates, throughput, and availability across all API endpoints with alerting, anomaly detection, and automated incident response. Supports OpenTelemetry, Prometheus, Grafana, Datadog, and custom monitoring backends.

## Core Capabilities

- **Request Metrics**: Track request count, rate, latency distribution, and throughput per endpoint, method, status code, and consumer
- **Distributed Tracing**: End-to-end request tracing across microservices with span hierarchy and bottleneck identification
- **Structured Logging**: JSON-structured API access logs with correlation IDs, user context, and performance data
- **Error Tracking**: Aggregate and categorize errors by type, endpoint, frequency, and impact with stack trace analysis
- **SLA Monitoring**: Track availability, latency, and error rate SLAs with automated compliance reporting
- **Anomaly Detection**: Statistical anomaly detection for traffic spikes, latency degradation, and error bursts
- **Alerting**: Configurable alerts on metrics thresholds with escalation policies and notification channels
- **Dashboard Generation**: Auto-generated monitoring dashboards with key API health indicators

## Usage

```python
from api_monitoring import (
    MetricsCollector, TraceCollector, AlertManager, SLATracker, DashboardGenerator
)

# Collect metrics
metrics = MetricsCollector()
metrics.record_request(
    method="GET", path="/api/users",
    status_code=200, latency_ms=45.2,
    consumer_id="client-app-1",
)
metrics.record_request(
    method="POST", path="/api/users",
    status_code=201, latency_ms=120.5,
    consumer_id="client-app-1",
)
metrics.record_request(
    method="GET", path="/api/users/123",
    status_code=404, latency_ms=12.1,
)

# Query metrics
summary = metrics.get_endpoint_summary("GET /api/users")
print(f"Requests: {summary['total_requests']}")
print(f"Avg latency: {summary['avg_latency_ms']:.1f}ms")
print(f"p99 latency: {summary['p99_latency_ms']:.1f}ms")
print(f"Error rate: {summary['error_rate']:.2%}")

# Distributed tracing
tracer = TraceCollector()
span = tracer.start_span("GET /api/users")
child = tracer.start_span("db.query", parent=span.span_id)
tracer.end_span(child)
tracer.end_span(span, attributes={"http.status_code": 200})

# SLA tracking
sla = SLATracker()
sla.define_sla(
    name="user-api-availability",
    metric="availability",
    target=99.9,
    window="30d",
)
status = sla.check("user-api-availability")
print(f"\nSLA: {status['name']} = {status['current']:.2f}% (target: {status['target']}%)")
print(f"Compliant: {status['compliant']}")

# Alerting
alerts = AlertManager()
alerts.add_rule(
    name="high-error-rate",
    metric="error_rate",
    condition="> 0.05",
    window_minutes=5,
    severity="critical",
    notify=["slack:#api-alerts", "email:ops@example.com"],
)
```

## Best Practices

- Monitor the four golden signals: latency, traffic, errors, and saturation
- Use structured JSON logs for machine parsing — include correlation IDs in every request
- Track p99 latency, not just averages — tail latency drives user experience
- Set SLAs at the 99th percentile, not the 50th — most users experience the tail
- Implement distributed tracing across all microservices for end-to-end visibility
- Create runbooks for every alert to reduce mean time to resolution (MTTR)
- Monitor API consumer behavior to detect anomalies early
- Use anomaly detection rather than static thresholds for dynamic traffic patterns
- Export metrics in Prometheus format for integration with Grafana dashboards
- Track both server-side and client-side latency for complete picture

## Related Modules

- **api-design** — Design patterns that affect monitoring (correlation IDs, status codes)
- **api-versioning** — Version-specific monitoring and consumer migration tracking
- **api-security** — Security event monitoring and threat detection
- **api-gateway** → **api-management** — Gateway-level metrics aggregation
- **backend** → **background-jobs** — Background job monitoring and metrics
