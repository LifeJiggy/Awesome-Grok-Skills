---
name: "Dynamic Analysis"
version: "2.0.0"
description: "Comprehensive dynamic analysis toolkit with runtime profiling, memory analysis, thread debugging, API tracing, and performance monitoring for production application debugging"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["debugger", "dynamic-analysis", "profiling", "tracing", "runtime", "performance"]
category: "debugger"
personality: "dynamic-analyst"
use_cases: ["runtime profiling", "memory analysis", "thread debugging", "API tracing", "performance monitoring"]
---

# Dynamic Analysis

> Production-grade dynamic analysis framework providing runtime profiling, memory analysis, thread debugging, API tracing, and performance monitoring for diagnosing issues in running applications.

## Overview

The Dynamic Analysis module provides tools for analyzing running applications without modifying source code. It implements CPU and memory profiling with flame graph generation, thread deadlock detection and race condition identification, HTTP/API request tracing with distributed context propagation, runtime behavior monitoring, and automated anomaly detection. Every analysis produces actionable reports with root cause hypotheses and remediation guidance.

## Core Capabilities

### 1. Runtime Profiling
- CPU profiling with function-level attribution
- Memory allocation tracking and leak detection
- I/O profiling (disk reads/writes, network)
- Goroutine/thread profiling
- Flame graph generation

### 2. Memory Analysis
- Heap dump analysis
- Object lifecycle tracking
- Memory leak detection
- Garbage collection profiling
- Memory allocation hotspots

### 3. Thread Debugging
- Deadlock detection and reporting
- Lock contention analysis
- Thread state profiling
- Race condition detection
- Thread pool utilization monitoring

### 4. API Tracing
- Distributed request tracing
- Span hierarchy visualization
- Latency breakdown analysis
- Error propagation tracking
- Dependency mapping

### 5. Runtime Monitoring
- Function call counting
- Execution time measurement
- Error rate tracking
- Resource usage monitoring
- Anomaly detection

### 6. Automated Diagnostics
- Root cause analysis
- Performance bottleneck identification
- Regression detection
- Recommendation engine

## Usage Examples

### CPU Profiling

```python
from dynamic_analysis import Profiler, ProfileMode

profiler = Profiler(mode=ProfileMode.CPU)

# Profile a code block
with profiler.profile("data_processing"):
    for i in range(100000):
        result = process_data(i)

# Get results
report = profiler.get_report()
print(f"Total time: {report.total_time_ms:.1f}ms")
print(f"Top functions:")
for func in report.top_functions[:5]:
    print(f"  {func.name}: {func.time_ms:.1f}ms ({func.percentage:.1f}%)")

# Generate flame graph
profiler.export_flame_graph("profile.svg")
```

### Memory Analysis

```python
from dynamic_analysis import MemoryAnalyzer

analyzer = MemoryAnalyzer()

# Take heap snapshot
analyzer.snapshot("before_processing")

# Run some code
process_large_dataset()

# Take another snapshot
analyzer.snapshot("after_processing")

# Compare snapshots
diff = analyzer.compare("before_processing", "after_processing")
print(f"Memory change: {diff.memory_delta_mb:.1f} MB")
print(f"Objects created: {diff.objects_created}")
print(f"Potential leaks:")
for leak in diff.potential_leaks:
    print(f"  {leak.type}: {leak.count} objects ({leak.size_mb:.1f} MB)")
```

### Thread Debugging

```python
from dynamic_analysis import ThreadDebugger

debugger = ThreadDebugger()

# Detect deadlocks
deadlocks = debugger.detect_deadlocks()
if deadlocks:
    print(f"Deadlocks found: {len(deadlocks)}")
    for deadlock in deadlocks:
        print(f"  Threads: {deadlock.thread_ids}")
        print(f"  Locks: {deadlock.locks}")
        print(f"  Wait graph: {deadlock.wait_graph}")

# Analyze lock contention
contention = debugger.analyze_lock_contention()
print(f"Lock contention: {contention.contention_pct:.1f}%")
print(f"Most contested locks:")
for lock in contention.top_locks[:3]:
    print(f"  {lock.name}: {lock.wait_time_ms:.1f}ms ({lock.contention_count} waits)")
```

### API Tracing

```python
from dynamic_analysis import Tracer, SpanKind

tracer = Tracer(service_name="payment-service")

# Start a trace
with tracer.start_span("process_payment", kind=SpanKind.INTERNAL) as span:
    span.set_attribute("order_id", "12345")
    span.set_attribute("amount", 99.99)

    # Child span for validation
    with tracer.start_span("validate_payment") as child:
        validate_payment(order_id)

    # Child span for processing
    with tracer.start_span("charge_card") as child:
        charge_card(card_token, amount)

# Get trace
trace = tracer.get_trace()
print(f"Trace ID: {trace.trace_id}")
print(f"Total duration: {trace.duration_ms:.1f}ms")
print(f"Spans: {len(trace.spans)}")
for span in trace.spans:
    print(f"  {span.name}: {span.duration_ms:.1f}ms ({span.status})")
```

## Best Practices

### Profiling
- Profile in production-like environments, not development
- Use sampling profiling for production (lower overhead)
- Profile at multiple points in the lifecycle
- Compare profiles before and after changes

### Memory Analysis
- Take snapshots at known stable points
- Compare snapshots to identify growth patterns
- Watch for objects accumulating without cleanup
- Monitor GC pressure in managed languages

### Thread Debugging
- Enable deadlock detection in testing and production
- Monitor lock contention as a key metric
- Use lock-free data structures when possible
- Implement timeout on lock acquisition

### API Tracing
- Propagate trace context across service boundaries
- Sample traces in production (1-10% rate)
- Capture both success and failure paths
- Set meaningful attributes on spans

## Related Modules

- **memory-profiling**: Detailed memory profiling and leak detection
- **network-debugging**: Network-level tracing and analysis
- **crash-analysis**: Crash dump analysis and post-mortem debugging
- **reverse-engineering**: Binary analysis and reverse engineering