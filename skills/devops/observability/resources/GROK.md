# Observability

## Overview

Observability enables understanding of system behavior through external outputs to infer internal states. This skill covers metrics, logging, tracing, and their integration to provide comprehensive system visibility. Observability is essential for debugging distributed systems, understanding user impact, and maintaining reliability.

## Core Capabilities

Metrics provide quantitative measurements of system behavior over time. Logs capture discrete events with contextual information. Distributed tracing follows requests across service boundaries. Dashboards visualize key metrics and trends.

Alerting notifies teams of anomalies and incidents. Service maps visualize system topology and dependencies. Anomaly detection identifies unusual patterns automatically. SLO dashboards track reliability against targets.

## Usage Examples

```python
from observability import Observability

obs = Observability()

obs.configure_metrics(
    provider="prometheus",
    scrape_interval=15
)

request_counter = obs.create_counter_metric(
    name="http_requests_total",
    description="Total HTTP requests",
    labels=["method", "status", "endpoint"]
)

latency_histogram = obs.create_histogram_metric(
    name="http_request_duration_seconds",
    description="HTTP request latency",
    buckets=[0.1, 0.25, 0.5, 1, 2.5, 5, 10]
)

obs.configure_logging(
    provider="elk",
    level="INFO",
    format="json"
)

alert = obs.create_alert_rule(
    name="HighErrorRate",
    query="rate(http_requests_total{status=~'5..'}[5m]) / rate(http_requests_total[5m]) > 0.05",
    severity="critical",
    condition="for 5m",
    duration=300
)

obs.configure_tracing(
    provider="jaeger",
    sample_rate=0.01
)

span = obs.create_span(
    operation_name="process_order",
    span_type="internal",
    tags={"order_id": "12345"}
)

dashboard = obs.create_dashboard(
    title="API Dashboard",
    panels=[
        obs.create_dashboard_panel("graph", "Request Rate", "rate(http_requests_total[5m])"),
        obs.create_dashboard_panel("graph", "Error Rate", "rate(http_requests_total{status=~'5..'}[5m])"),
        obs.create_dashboard_panel("stat", "P99 Latency", "histogram_quantile(0.99, http_request_duration_seconds)")
    ]
)

service_map = obs.create_service_map(
    services=[
        {"name": "api-gateway", "health": "healthy"},
        {"name": "order-service", "health": "healthy"},
        {"name": "payment-service", "health": "degraded"},
        {"name": "inventory-service", "health": "healthy"}
    ],
    dependencies=[
        {"from": "api-gateway", "to": "order-service"},
        {"from": "order-service", "to": "payment-service"},
        {"from": "order-service", "to": "inventory-service"}
    ]
)

slo_dashboard = obs.configure_slo_dashboard(
    service_name="api-service",
    slo_targets={
        "availability": 0.999,
        "latency": 0.95,
        "error_budget": 0.1
    }
)

health_check = obs.create_health_check_endpoint(
    name="api-health",
    path="/health",
    checks=[
        {"type": "liveness", "timeout": "5s"},
        {"type": "readiness", "timeout": "10s", "dependencies": ["database", "cache"]}
    ]
)

anomaly = obs.configure_anomaly_detection(
    metric_name="http_request_duration_seconds",
    algorithm="isolation_forest",
    sensitivity=0.5
)

incident_dashboard = obs.create_incident_dashboard(service_name="api-service")

cost_dashboard = obs.create_cost_dashboard(
    service_name="api-service",
    cost_metrics=["compute", "storage", "network"]
)
```

## Best Practices

Instrument everything from the start, don't retrofit observability. Use three pillars together for complete understanding. Create dashboards for different audiences and use cases. Alert on symptoms, not causes.

Sample traces appropriately for high-volume systems. Keep logs structured and consistent. Use SLO-based alerting to reduce noise. Automate anomaly detection for early warning.

## Related Skills

- Site Reliability Engineering (reliability practices)
- Metrics Collection (metric systems)
- Log Management (logging infrastructure)
- Distributed Tracing (tracing systems)

## Use Cases

Production debugging identifies root causes of incidents quickly. Capacity planning uses trend analysis of resource utilization. User experience monitoring tracks real user impact. Cost optimization identifies resource waste.
