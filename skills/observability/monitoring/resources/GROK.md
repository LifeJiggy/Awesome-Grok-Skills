# Observability Agent

## Overview

The **Observability Agent** provides comprehensive monitoring and observability capabilities including metrics collection, distributed tracing, log aggregation, and SLO management. This agent enables understanding of system behavior and rapid issue detection.

## Core Capabilities

### 1. Metrics Collection
Collect and analyze system metrics:
- **Counter Metrics**: Cumulative counts (requests, errors)
- **Gauge Metrics**: Point-in-time values (memory, CPU)
- **Histogram Metrics**: Distribution of values (latency)
- **Summary Metrics**: Quantile calculations
- **Custom Metrics**: Application-specific metrics

### 2. Distributed Tracing
Track requests across services:
- **Span Management**: Create, annotate, close spans
- **Trace Context**: Propagate across services
- **Trace Analysis**: Identify bottlenecks
- **Error Tracing**: Root cause identification
- **Service Maps**: Visualize dependencies

### 3. Log Management
Centralize and analyze logs:
- **Log Collection**: Agent-based, API-based
- **Log Aggregation**: Centralized storage
- **Log Parsing**: Structured extraction
- **Log Search**: Full-text and structured queries
- **Log Alerting**: Anomaly detection

### 4. SLO Management
Define and monitor service levels:
- **SLO Definition**: Service level objectives
- **SLI Selection**: Key metrics selection
- **Error Budget**: Risk management
- **SLO Reporting**: Compliance tracking
- **Burn Rate Alerts**: Proactive monitoring

### 5. OpenTelemetry Integration
Standardized observability:
- **Auto-instrumentation**: Zero-code tracing
- **Manual Instrumentation**: Custom spans
- **Exporters**: Multiple backend support
- **Context Propagation**: Trace context headers
- **Sampling**: Trace sampling strategies

## Usage Examples

### Collect Metrics

```python
from observability import MetricsCollector

metrics = MetricsCollector()
metrics.record_metric('http_requests_total', 100, {'endpoint': '/api'})
metrics.increment_counter('user_logins', 1, {'method': 'oauth'})
metrics.observe_histogram('request_duration_ms', 150, {'endpoint': '/api'})
alert = metrics.create_alert('high_error_rate', 'error_rate > 0.05', 'critical')
```

### Distributed Tracing

```python
from observability import DistributedTracing

tracing = DistributedTracing()
span = tracing.start_span('trace_123', 'process_order', parent_span_id=None)
tracing.add_span_event(span['span_id'], 'order_received', {'order_id': '123'})
tracing.end_span(span['span_id'], 'ok')
analysis = tracing.analyze_trace('trace_123')
```

### Manage Logs

```python
from observability import LogManagement

logs = LogManagement()
structured = logs.structure_log('INFO', 'Order processed', 'api', {'order_id': '123'})
results = logs.search_logs('error OR failed', time_range='1h', limit=100)
anomalies = logs.detect_anomaly(log_stream)
```

### OpenTelemetry

```python
from observability import OpenTelemetryCollector

otel = OpenTelemetryCollector()
instrumented = otel.instrument_python_app('myapp')
exporter = otel.configure_exporter('otlp', 'localhost:4317')
sampling = otel.sample_traces(sample_rate=0.1)
```

### Dashboard and SLOs

```python
from observability import DashboardManager, SLOManagement

dashboard = DashboardManager()
dash = dashboard.create_dashboard('My Dashboard', [
    {'type': 'timeseries', 'title': 'Requests', 'query': 'http_requests_total'}
])
slo = SLOManagement()
slo.create_slo('availability_99', 'http_requests_success', 0.99, '30d')
budget = slo.calculate_error_budget('availability_99')
```

## Observability Stack

### Data Collection
- **Prometheus**: Metrics collection
- **OpenTelemetry**: Unified instrumentation
- **Fluentd/Fluent Bit**: Log collection
- **Jaeger/Zipkin**: Distributed tracing

### Data Storage
- **Prometheus TSDB**: Metrics storage
- **Elasticsearch**: Log storage
- **Tempo**: Trace storage
- **VictoriaMetrics**: Long-term metrics

### Visualization
- **Grafana**: Dashboards
- **Kibana**: Log visualization
- **Jaeger UI**: Trace exploration
- **Prometheus UI**: Metrics exploration

### Alerting
- **Alertmanager**: Alert routing
- **Grafana Alerts**: Visual alerts
- **PagerDuty**: Incident management
- **OpsGenie**: On-call management

## Key Metrics

### Application Metrics
- **Request Rate**: Requests per second
- **Error Rate**: Percentage of errors
- **Latency**: Response time (p50, p95, p99)
- **Saturation**: Resource utilization

### Infrastructure Metrics
- **CPU Usage**: Processor utilization
- **Memory Usage**: RAM consumption
- **Disk I/O**: Read/write operations
- **Network**: Bandwidth, packets

### Business Metrics
- **Conversion Rate**: User actions
- **Revenue**: Transaction value
- **Active Users**: DAU/MAU
- **Error Budget**: SLO burn rate

## Distributed Tracing Concepts

### Spans
```
┌──────────────────────────────────────────────────────┐
│                    Trace ID                          │
│  ┌─────────────┐                                     │
│  │ Span: order │ Duration: 150ms                     │
│  ├─────────────┤                                     │
│  │ Span: user  │ Duration: 50ms                      │
│  ├─────────────┤                                     │
│  │ Span: payment │ Duration: 100ms                   │
│  └─────────────┘                                     │
└──────────────────────────────────────────────────────┘
```

### Trace Components
- **Trace ID**: Unique request identifier
- **Span ID**: Individual operation
- **Parent Span**: Hierarchical relationship
- **Span Context**: Propagation data

## SLO/SLI Framework

### SLO Structure
```yaml
service: api
slo:
  name: availability
  sli: http_requests_success / http_requests_total
  target: 0.999  # 99.9%
  window: 30d
  error_budget: 7.2 hours per month
```

### Common SLOs
| SLO | SLI | Target |
|-----|-----|--------|
| Availability | Success rate | 99.9% |
| Latency | p95 response time | <200ms |
| Freshness | Data age | <5min |
| Correctness | Error-free responses | 99.99% |

## Alerting Strategies

### Alert Types
- **Critical**: Immediate action required
- **Warning**: Monitor closely
- **Info**: Informational only

### Best Practices
1. **Signal-to-Noise Ratio**: Avoid alert fatigue
2. **Runbooks**: Documented responses
3. **Escalation**: Clear escalation paths
4. **SLO-Based**: Alert on error budget

## Use Cases

### 1. Incident Response
- Rapid detection
- Root cause analysis
- Impact assessment
- Recovery tracking

### 2. Performance Optimization
- Bottleneck identification
- Capacity planning
- Trend analysis
- Resource allocation

### 3. User Experience
- Real user monitoring
- Performance tracking
- Error monitoring
- Feature adoption

### 4. Compliance
- Audit trails
- Security monitoring
- Data lineage
- Access logging

## Related Skills

- [Infrastructure as Code](../iac/terraform-cloudformation/README.md) - Deployment
- [Microservices Architecture](../microservices/service-architecture/README.md) - Architecture
- [Security Operations](../blue-team/soc-operations/README.md) - Security monitoring

---

**File Path**: `skills/observability/monitoring/resources/observability.py`
