---
name: "distributed-tracing"
category: "microservices"
version: "2.0.0"
tags: ["microservices", "tracing", "observability", "jaeger", "opentelemetry"]
description: "Distributed tracing and observability for microservices"
---

# Distributed Tracing

## Overview

The Distributed Tracing module provides tools for implementing and managing distributed tracing across microservices. It supports trace context propagation, span creation, trace analysis, and integration with tracing systems like Jaeger, Zipkin, and OpenTelemetry.

## Core Capabilities

- **Trace Context Propagation**: Propagate trace context across services
- **Span Management**: Create and manage spans within traces
- **Trace Collection**: Collect traces from distributed services
- **Trace Analysis**: Analyze traces for performance issues
- **Sampling Strategies**: Configure trace sampling
- **Integration**: Jaeger, Zipkin, OpenTelemetry support
- **Service Dependencies**: Map service dependencies from traces
- **Alerting**: Alert on slow or failed traces

## Usage Examples

### Trace Context

```python
from distributed_tracing import Tracer, SpanContext

tracer = Tracer(service_name="order-service")

# Start a trace
span = tracer.start_span(
    operation="process_order",
    context=SpanContext(
        trace_id="abc123",
        span_id="span001",
    ),
)

# Add tags and logs
span.set_tag("order.id", "ORD-001")
span.log("Processing order items")

# Finish span
span.finish()
```

### Trace Analysis

```python
from distributed_tracing import TraceAnalyzer, TraceQuery

analyzer = TraceAnalyzer()

# Analyze slow traces
slow_traces = analyzer.find_slow_traces(
    service="order-service",
    threshold_ms=1000,
    time_range="1h",
)

print(f"Slow Traces ({len(slow_traces)}):")
for trace in slow_traces[:5]:
    print(f"  Trace: {trace.trace_id}")
    print(f"    Duration: {trace.duration_ms:.0f}ms")
    print(f"    Spans: {trace.span_count}")
    print(f"    Services: {trace.services}")
```

### Sampling Configuration

```python
from distributed_tracing import SamplingConfig, SamplingStrategy

config = SamplingConfig(
    strategy=SamplingStrategy.ADAPTIVE,
    default_rate=0.01,
    service_rates={
        "order-service": 0.1,
        "payment-service": 0.1,
    },
    max_traces_per_second=100,
)

tracer.configure_sampling(config)
```

### Service Dependency Map

```python
from distributed_tracing import DependencyMapper

mapper = DependencyMapper()

# Generate dependency map
dependencies = mapper.generate(
    time_range="24h",
    min_requests=100,
)

print(f"Service Dependencies:")
for dep in dependencies:
    print(f"  {dep.source} -> {dep.target}")
    print(f"    Requests: {dep.request_count}")
    print(f"    Avg Latency: {dep.avg_latency_ms:.0f}ms")
```

## Best Practices

- **Trace Everything**: Instrument all service interactions
- **Context Propagation**: Always propagate trace context
- **Meaningful Names**: Use descriptive span operation names
- **Tagging**: Add relevant tags for filtering
- **Sampling**: Use appropriate sampling strategies
- **Performance**: Minimize tracing overhead
- **Security**: Protect sensitive trace data
- **Alerting**: Set up alerts for latency issues

## Related Modules

- **service-mesh**: Mesh integration for tracing
- **api-gateway**: Gateway trace propagation
- **service-architecture**: Service design for tracing
