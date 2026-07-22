---
name: "tracing"
category: "observability"
version: "1.0.0"
tags: ["observability", "tracing"]
---

# Tracing

## Overview

Comprehensive tracing capabilities within the observability domain. This module provides tools, frameworks, and best practices for tracing operations.

## Core Capabilities

- Configuration and setup
- Data processing and analysis
- Integration with related systems
- Monitoring and observability
- Best practices and patterns

## Usage

```python
from tracing import _module

engine = _module.Engine()
engine.configure()
results = engine.run()
print(results)
```

## Best Practices

- Follow security guidelines
- Implement proper error handling
- Use configuration management
- Monitor performance metrics
- Document API interfaces

## Related Modules

- Other modules in observability domain
- Integration points with external systems

## Advanced Configuration

### Sampling Strategies

- **Head-based sampling**: Decision made at trace creation. Lower overhead, may miss important traces.
- **Tail-based sampling**: Decision made after trace completion. Higher accuracy, requires buffering.
- **Adaptive sampling**: Rate adjusts based on error rate and latency. Balanced approach for production.

```yaml
sampling:
  default_rate: 0.01
  error_rate: 1.0
  slow_threshold_ms: 500
  slow_rate: 0.5
  rules:
    - match: "http.method == POST"
      rate: 0.1
    - match: "service == payment"
      rate: 0.5
```

### Propagation Formats

- **W3C TraceContext**: Standard format with traceparent and tracestate headers.
- **B3**: Zipkin format with X-B3-TraceId and X-B3-SpanId headers.
- **Jaeger**: Uber format with uber-trace-id header.
- **AWS X-Ray**: AWS-native format with X-Amzn-Trace-Id header.

### Context Propagation

```python
from tracing import TracerProvider, TraceContext

provider = TracerProvider(
    service_name="api-gateway",
    sampler=ParentBasedSampler(root=TraceIdRatioBased(0.01)),
    resource=Resource({"environment": "production"})
)

tracer = provider.get_tracer("http-handler")

with tracer.start_span("handle_request") as span:
    span.set_attribute("http.method", "GET")
    span.set_attribute("http.url", "/api/users")
    # Child spans automatically inherit context
    with tracer.start_span("database_query", parent=span) as child:
        result = db.query("SELECT * FROM users")
        child.set_attribute("db.statement", "SELECT * FROM users")
```

### Span Limits

```python
provider = TracerProvider(
    max_spans_per_trace=1000,
    max_events_per_span=128,
    max_attributes_per_span=128,
    max_links_per_span=128,
    max_attribute_value_length=4096,
    timeout_seconds=300
)
```

## Architecture Patterns

### Trace Collection Pipeline

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Application │────▶│  Agent       │────▶│   Collector   │
│   Instrumented│     │  (OTel/      │     │   (OTel       │
│              │     │   Jaeger)    │     │   Collector)  │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                     ┌──────────────┐     ┌──────▼───────┐
                     │    Query     │◀────│   Storage    │
                     │    (Jaeger/  │     │  (Cassandra/ │
                     │   Tempo)     │     │   Elasticsearch)│
                     └──────────────┘     └──────────────┘
```

### Auto-Instrumentation vs Manual

- **Auto-instrumentation**: Automatically captures spans from HTTP, gRPC, database, and message queue calls. Zero code changes, but less control over span attributes.
- **Manual instrumentation**: Explicit span creation with custom attributes. More control, but requires code changes.
- **Hybrid**: Auto-instrument for framework calls, manual for business logic. Best of both approaches.

### Distributed Context Propagation

```
Service A ──────▶ Service B ──────▶ Service C
   │                  │                  │
Span 1             Span 2             Span 3
(trace_id=abc)    (trace_id=abc)    (trace_id=abc)
(span_id=1)       (span_id=2)       (span_id=3)
(parent=none)     (parent=1)        (parent=2)
```

### Service Dependency Mapping

```
           ┌──────────┐
           │  API GW  │
           └────┬─────┘
        ┌───────┼───────┐
        │       │       │
   ┌────▼──┐ ┌──▼───┐ ┌▼──────┐
   │ Auth  │ │Order │ │Payment│
   │Service│ │Svc   │ │Service│
   └───┬───┘ └──┬───┘ └───┬───┘
       │        │         │
   ┌───▼───┐ ┌──▼───┐ ┌───▼───┐
   │ Redis │ │Postgres│ │ Stripe│
   └───────┘ └───────┘ └───────┘
```

## Integration Guide

### Jaeger Integration

```python
from tracing import JaegerExporter

exporter = JaegerExporter(
    agent_host_name="jaeger-agent",
    agent_port=6831,
    collector_endpoint="http://jaeger-collector:14268/api/traces"
)
```

### Zipkin Integration

```python
from tracing import ZipkinExporter

exporter = ZipkinExporter(
    endpoint="http://zipkin:9411/api/v2/spans",
    local_endpoint={"serviceName": "my-service"}
)
```

### OpenTelemetry Integration

```python
from tracing import OTLPExporter

exporter = OTLPExporter(
    endpoint="http://otel-collector:4317",
    insecure=False,
    timeout=10
)
```

## Performance Optimization

### Sampling Overhead

- Head-based sampling: <1ms per trace creation.
- Tail-based sampling: 1-10ms per trace for buffering and evaluation.
- Adaptive sampling: Variable overhead based on traffic patterns.

### Span Attributes

- Use semantic conventions for standard attributes (http.method, db.system).
- Limit attribute values to 4096 bytes.
- Avoid high-cardinality attribute values (user IDs, request IDs).

### Batch Export

```python
from tracing import BatchSpanProcessor

processor = BatchSpanProcessor(
    max_queue_size=2048,
    max_export_batch_size=512,
    schedule_delay_millis=5000,
    export_timeout_millis=30000
)
```

### Storage Optimization

- **Compression**: Gzip spans before storage (70-90% reduction).
- **TTL**: Automatically delete traces after retention period.
- **Indexing**: Index by service, operation, and duration for fast queries.
- **Sharding**: Partition traces by time or service for horizontal scaling.

## Security Considerations

- **PII in spans**: Never log PII (user IDs, emails, credit cards) in span attributes.
- **Trace context injection**: Validate trace context headers to prevent injection attacks.
- **TLS transport**: Use TLS for all trace export. Verify certificates.
- **Access control**: Restrict trace query access to authorized personnel.
- **Audit logging**: Log all trace query and export operations.
- **Data retention**: Implement automated trace lifecycle management.
- **Sampling sensitivity**: Avoid sampling decisions based on sensitive request attributes.

## Troubleshooting Guide

### Common Issues

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| Missing traces | Sampling rate too low | Increase sampling rate for affected services |
| Broken traces | Context not propagated | Verify propagation format configuration |
| High latency | Batch export delay | Reduce batch size or export interval |
| Storage full | Retention too long | Verify TTL, check storage capacity |
| Incomplete traces | Span timeout | Increase span timeout configuration |
| Duplicate traces | Multiple exporters | Check exporter deduplication config |

### Debug Mode

```python
from tracing import enable_debug

enable_debug(
    log_level="trace",
    include_all_spans=True,
    include_context_propagation=True,
    output_file="/tmp/tracing-debug.log"
)
```

### Trace Validation Checklist

1. Verify trace IDs are valid 128-bit hex strings.
2. Check span parent-child relationships form valid DAGs.
3. Confirm span timestamps are monotonically increasing within a trace.
4. Validate service dependency graph for unexpected edges.
5. Ensure all external calls are captured as spans.

## API Reference

### Core Classes

#### `Tracer`

```python
class Tracer:
    def start_span(self, name: str, parent: Optional[Span] = None) -> Span
    def start_active_span(self, name: str) -> ContextManager[Span]
    def get_current_span(self) -> Optional[Span]
```

#### `Span`

```python
class Span:
    def set_attribute(self, key: str, value: Any) -> None
    def add_event(self, name: str, attributes: Optional[Dict] = None) -> None
    def set_status(self, status: SpanStatus) -> None
    def end(self) -> None
```

#### `TracerProvider`

```python
class TracerProvider:
    def __init__(self, config: ProviderConfig)
    def get_tracer(self, name: str, version: str = "1.0.0") -> Tracer
    def add_processor(self, processor: SpanProcessor) -> None
    def shutdown(self) -> None
```

## Data Models

### Span Schema

```sql
CREATE TABLE spans (
    trace_id VARCHAR(64) NOT NULL,
    span_id VARCHAR(16) NOT NULL,
    parent_span_id VARCHAR(16),
    service_name VARCHAR(128) NOT NULL,
    operation_name VARCHAR(256) NOT NULL,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    duration_ms FLOAT NOT NULL,
    status VARCHAR(16) NOT NULL,
    attributes JSONB,
    events JSONB,
    links JSONB,
    PRIMARY KEY (trace_id, span_id)
);

CREATE INDEX idx_spans_trace ON spans (trace_id);
CREATE INDEX idx_spans_service ON spans (service_name, start_time DESC);
CREATE INDEX idx_spans_operation ON spans (operation_name, start_time DESC);
CREATE INDEX idx_spans_duration ON spans (duration_ms) WHERE duration_ms > 1000;
```

## Deployment Guide

### Docker Compose

```yaml
version: '3.8'
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"  # UI
      - "14268:14268"  # Collector
      - "6831:6831/udp"  # Agent
  otel-collector:
    image: otel/opentelemetry-collector-contrib:latest
    ports:
      - "4317:4317"  # OTLP gRPC
      - "4318:4318"  # OTLP HTTP
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tracing-stack
spec:
  replicas: 3
  selector:
    matchLabels:
      app: tracing
  template:
    spec:
      containers:
        - name: jaeger
          image: jaegertracing/all-in-one:latest
          ports:
            - containerPort: 16686
            - containerPort: 14268
```

## Monitoring & Observability

### Self-Monitoring Metrics

- `tracing_spans_exported_total` — total spans exported.
- `tracing_spans_dropped_total` — dropped spans due to queue overflow.
- `tracing_export_latency_seconds` — export latency distribution.
- `tracing_storage_writes_total` — storage write throughput.
- `tracing_query_latency_seconds` — query latency distribution.

### Health Checks

```python
from tracing import TracingHealthCheck

health = TracingHealthCheck(
    checks=[
        CollectorConnectivity(),
        StorageConnectivity(),
        ExportLatency(max_p99_ms=5000),
        QueueUtilization(max_percent=80)
    ]
)
```

## Testing Strategy

### Unit Testing

```python
def test_span_creation():
    tracer = Tracer(name="test")
    with tracer.start_span("test_operation") as span:
        span.set_attribute("key", "value")
        assert span.name == "test_operation"

def test_context_propagation():
    ctx = TraceContext(trace_id="abc123", span_id="456")
    carrier = {}
    ctx.inject(carrier)
    assert "traceparent" in carrier
```

### Integration Testing

- Verify end-to-end trace flow from instrumentation to storage.
- Test context propagation across service boundaries.
- Validate sampling behavior under different traffic patterns.
- Check trace completeness for multi-service transactions.

## Versioning & Migration

- **v1.0.0**: Initial release with W3C TraceContext support.
- **v1.1.0**: Added adaptive sampling and tail-based sampling.
- **v1.2.0**: Performance optimization and multi-format propagation.

## Glossary

| Term | Definition |
|------|-----------|
| Trace | Complete path of a request through the system |
| Span | Single unit of work within a trace |
| Trace ID | Unique identifier for a complete trace |
| Span ID | Unique identifier for a single span |
| Parent Span | The span that initiated a child span |
| Sampling | Process of selecting which traces to capture |

## Changelog

### v1.2.0
- Added adaptive sampling with error-based rate adjustment.
- Multi-format context propagation (W3C, B3, Jaeger, X-Ray).
- Performance optimization for high-throughput environments.

### v1.1.0
- Added tail-based sampling for post-hoc trace selection.
- Service dependency graph visualization.
- Enhanced troubleshooting tools.

### v1.0.0
- Initial release with W3C TraceContext support.
- Basic span creation and export.

## Contributing Guidelines

1. Fork the repository and create a feature branch.
2. Write tests for all new functionality.
3. Follow the existing code style and naming conventions.
4. Update documentation for any API changes.
5. Add entries to the changelog for user-facing changes.
6. Submit a pull request with a clear description of changes.

### Span Error Handling

```python
from tracing import ErrorSpanHandler

handler = ErrorSpanHandler(
    capture_stack_traces=True,
    max_stack_depth=50,
    exclude_patterns=["internal/", "vendor/"],
    enrich_with_logs=True
)
```

### Trace Context Validation

```python
from tracing import TraceContextValidator

validator = TraceContextValidator(
    validate_trace_id=True,
    validate_span_id=True,
    validate_parent_chain=True,
    max_trace_age_hours=24
)
```

### Service Map Configuration

```yaml
service_map:
  discovery:
    method: "automatic"
    refresh_interval: "60s"
  visualization:
    layout: "force_directed"
    show_dependency_versions: true
    highlight_error_paths: true
  alerting:
    on_new_dependency: true
    on_dependency_change: true
```

### Trace Analysis and Querying

```python
from tracing import TraceAnalyzer

analyzer = TraceAnalyzer(
    backend="jaeger",
    index_patterns=["traces-*"]
)

# Find slow traces
slow_traces = analyzer.find_slow_traces(
    service="api-gateway",
    operation="handle_request",
    threshold_ms=1000,
    time_range=("2024-01-15T10:00:00Z", "2024-01-15T11:00:00Z")
)

# Analyze error traces
error_traces = analyzer.find_error_traces(
    service="payment-service",
    error_type="timeout",
    time_range=("2024-01-15T10:00:00Z", "2024-01-15T11:00:00Z")
)

# Get service dependency graph
dependencies = analyzer.get_service_graph(
    time_range=("2024-01-15T00:00:00Z", "2024-01-15T23:59:59Z")
)
```

### Trace-Based Sampling Rules

```yaml
sampling_rules:
  - name: "error_traces"
    condition: "span.status == ERROR"
    rate: 1.0
    max_traces_per_second: 100
  - name: "slow_traces"
    condition: "span.duration > 1000ms"
    rate: 0.5
    max_traces_per_second: 50
  - name: "high_value_service"
    condition: "span.service == 'payment'"
    rate: 0.1
    max_traces_per_second: 20
  - name: "default"
    condition: "true"
    rate: 0.01
    max_traces_per_second: 10
```

### Trace Correlation with Logs

```python
from tracing import TraceLogCorrelator

correlator = TraceLogCorrelator(
    trace_id_field="trace_id",
    span_id_field="span_id",
    log_fields=["message", "level", "error"]
)

# Correlate traces with logs
correlated = correlator.correlate(
    trace_id="abc123def456",
    time_range=("2024-01-15T10:30:00Z", "2024-01-15T10:35:00Z")
)

print(f"Trace duration: {correlated.trace_duration_ms}ms")
print(f"Related logs: {len(correlated.logs)}")
for log in correlated.logs:
    print(f"  [{log.timestamp}] {log.level}: {log.message}")
```

### Trace Export Configuration

```python
from tracing import TraceExporter

exporter = TraceExporter(
    backends=[
        {"type": "jaeger", "endpoint": "http://jaeger:14268/api/traces"},
        {"type": "zipkin", "endpoint": "http://zipkin:9411/api/v2/spans"},
        {"type": "otlp", "endpoint": "http://otel:4317"}
    ],
    batch_config={
        "max_queue_size": 4096,
        "max_export_batch_size": 1024,
        "schedule_delay_millis": 5000
    }
)
```

### Trace-Based Debugging

```python
from tracing import TraceDebugger

debugger = TraceDebugger(
    auto_capture=True,
    capture_requests=True,
    capture_responses=True,
    max_capture_size=10240  # bytes
)

# Debug a specific trace
debug_session = debugger.debug(trace_id="abc123def456")

print(f"Trace timeline:")
for span in debug_session.spans:
    print(f"  {span.service}.{span.operation}: {span.duration_ms:.1f}ms")
    if span.error:
        print(f"    ERROR: {span.error.message}")
```

### Trace Aggregation and Analytics

```yaml
trace_analytics:
  aggregation:
    - name: "latency_by_service"
      metric: "histogram_quantile(0.99, span_duration)"
      group_by: ["service"]
      time_window: "5m"
    - name: "error_rate_by_service"
      metric: "rate(span_errors_total[5m])"
      group_by: ["service"]
      time_window: "5m"
    - name: "throughput_by_service"
      metric: "rate(span_total[5m])"
      group_by: ["service"]
      time_window: "5m"
  anomaly_detection:
    enabled: true
    method: "z_score"
    sensitivity: 2.0
    min_samples: 100
```

### Trace Retention and Archival

```python
from tracing import TraceRetention

retention = TraceRetention(
    hot_retention_days=7,
    warm_retention_days=30,
    cold_retention_days=365,
    archive_to="s3://traces-archive",
    compression="zstd"
)

# Apply retention policy
retention.apply(
    storage_backend="cassandra",
    index_backend="elasticsearch"
)
```

## Common Pitfalls

### High Cardinality Span Attributes

Adding unbounded values (user IDs, request IDs, SQL queries) as span attributes
explodes storage costs and degrades query performance.

```python
# BAD — high cardinality
span.set_attribute("user.id", user_id)  # millions of values
span.set_attribute("db.query", sql_string)  # unbounded

# GOOD — bounded, useful dimensions
span.set_attribute("user.tier", user.tier)  # free|pro|enterprise
span.set_attribute("db.operation", "SELECT")  # enum
span.set_attribute("db.table", "orders")  # bounded set
```

### Clock Skew in Distributed Traces

When hosts have unsynchronized clocks, span timestamps can appear out of order,
making waterfall views misleading. Ensure NTP is running on all hosts, and use
the collector's `adjust_downstream_timestamps` option when clock skew is detected.

```yaml
processors:
  - adjust_downstream_timestamps:
      max_skew: 200ms
      strategy: "shift_to_parent"
```

### Context Propagation Gaps

If one service in the chain doesn't propagate trace context, the trace splits
into disconnected fragments. Common causes:

- HTTP client libraries that don't inject headers
- Message queue consumers that don't extract context
- gRPC interceptors missing propagation setup

Validate propagation end-to-end with synthetic traces that traverse every
service in the critical path.

## Performance Tuning

### Span Batch Export

Batching reduces network overhead. Tune batch size and flush interval based on
throughput:

```python
BatchSpanProcessor(
    max_queue_size=8192,
    max_export_batch_size=2048,
    schedule_delay_millis=5000,
    export_timeout_millis=30000
)
```

Rule of thumb: `max_export_batch_size` should be ~25% of `max_queue_size` to
keep the queue draining under sustained load.

### Sampling at the Edge

Push sampling decisions to edge proxies to avoid generating spans that will be
dropped anyway. The `trace_id_ratio_based` sampler at the edge reduces overhead
by 90%+ while preserving a statistically valid sample.

```python
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

sampler = TraceIdRatioBased(0.01)  # 1% of traces
```

### Storage Retention

Tie retention to your debugging and compliance needs:

| Tier | Duration | Use Case |
|------|----------|----------|
| Hot | 7 days | Active debugging, incident response |
| Warm | 30 days | Trend analysis, SLO reporting |
| Cold | 90 days | Compliance, audit |
| Archive | 1 year+ | Regulatory hold |

## Testing Strategies

### Integration Testing with Trace Mocks

```python
from tracing import MockTracerProvider

def test_payment_flow():
    tracer = MockTracerProvider()

    with tracer.start_span("process_payment") as span:
        # your code under test
        result = payment_service.charge(order)

        # assert span attributes
        assert span.get_attribute("payment.amount") == 99.99
        assert span.get_attribute("payment.status") == "success"
        assert span.status == StatusCode.OK
```

### Chaos Testing Tracing Infrastructure

Kill tracing backends during peak traffic and verify that:
1. Applications continue serving (tracing is non-blocking)
2. Spans are buffered and exported once backends recover
3. No data loss for high-value traces (error traces, slow traces)

## Real-World Scenarios

### Debugging a Cascading Timeout

A 5-second timeout in service D propagates back through C → B → A:

1. Query traces for `span.duration > 5000 AND span.service = D`
2. Follow parent span IDs upward through the call chain
3. Identify the root cause span (the first one with `status = ERROR`)
4. Check span events for timeout details
5. Correlate with logs using `trace_id`

### Latency Regression After Deployment

Compare p99 latency before and after the deployment annotation:
1. Filter traces by `deployment.version = v2.3.0`
2. Group by `span.operation` and compute p50/p90/p99
3. Diff against the baseline (previous deployment version)
4. Drill into the operation with the largest delta
5. Examine span-level breakdowns for the new bottleneck

## Contributing Guidelines

1. Follow OpenTelemetry semantic conventions for attribute names.
2. Write integration tests for every new exporter or sampler.
3. Document performance impact of any new instrumentation.
4. Keep vendor-specific code behind adapter interfaces.
5. Benchmark before and after changes to span processing pipelines.

## License

MIT License. See the root LICENSE file for full terms.
