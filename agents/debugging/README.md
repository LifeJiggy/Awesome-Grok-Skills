# Debugging Agent

Systematic debugging — error analysis, root cause investigation, performance profiling, distributed tracing, log analysis, and automated fix suggestions.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Error Analysis](#error-analysis)
  - [Root Cause Analysis](#root-cause-analysis)
  - [Performance Profiling](#performance-profiling)
  - [Distributed Tracing](#distributed-tracing)
  - [Log Analysis](#log-analysis)
  - [Logging Strategy](#logging-strategy)
  - [Debug Sessions](#debug-sessions)
  - [Comprehensive Debug](#comprehensive-debug)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Debugging Agent provides a structured, systematic approach to diagnosing and resolving software issues. It follows a proven 7-phase methodology (Reproduce → Isolate → Hypothesize → Investigate → Fix → Verify → Prevent) and combines error analysis, root cause investigation, performance profiling, distributed tracing, and log analysis into a unified debugging platform.

**Key capabilities:**
- Auto-classify 20+ error types with severity assessment
- Structured root cause analysis with evidence tracking and confidence scoring
- Multi-dimensional profiling (CPU, memory, I/O, database)
- Distributed trace analysis with bottleneck detection
- Log pattern detection, correlation analysis, and normalization
- Logging strategy audit and optimization
- Comprehensive debug reports with actionable fix suggestions

---

## Features

| Feature | Description |
|---------|-------------|
| **Error Analysis** | Auto-classify errors, parse stack tracks, detect patterns |
| **Root Cause Analysis** | 7-phase methodology with evidence tracking |
| **Performance Profiling** | CPU, memory, I/O, database profiling with recommendations |
| **Distributed Tracing** | Span tree analysis, bottleneck detection, critical path |
| **Log Analysis** | Pattern detection, frequency analysis, correlation |
| **Logging Strategy** | Configuration audit, gap analysis, optimization |
| **Fix Suggestions** | Targeted fixes based on root cause category |
| **Debug Sessions** | Full lifecycle tracking with phase management |

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                   DEBUGGING AGENT                         │
├──────────────────────────────────────────────────────────┤
│  Error Analysis → Root Cause Analysis → Fix Suggestions  │
│  → Performance Profiling → Distributed Tracing           │
│  → Log Analysis → Logging Strategy → Debug Sessions      │
└──────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for full system architecture.

---

## Quick Start

```python
from agents.debugging.agent import (
    DebuggingAgent, ErrorCategory, Severity,
    RootCauseCategory, ProfilingType, TraceSpanStatus,
)

agent = DebuggingAgent()

# Analyze an error
error = agent.analyze_error(
    error_message="ConnectionError: Timeout connecting to database",
    error_type="ConnectionError",
)
print(f"Category: {error.category.value}")
print(f"Severity: {error.severity.value}")

# Comprehensive debug in one call
result = agent.debug_issue(
    error_message="TypeError: argument of type 'NoneType' is not iterable",
    error_type="TypeError",
)
print(result["fix_suggestions"])
```

---

## Installation

```bash
cd Awesome-Grok-Skills
pip install -e .
```

Or run directly:

```bash
python agents/debugging/agent.py
```

**Requirements:** Python 3.10+, no external dependencies.

---

## Usage

### Error Analysis

```python
agent = DebuggingAgent()

# Analyze with full context
error = agent.analyze_error(
    error_message="KeyError: 'user_id'",
    error_type="KeyError",
    stack_trace='File "app/api/handler.py", line 67, in process\n    uid = data["user_id"]',
    context={"request_id": "req-abc123", "endpoint": "/api/users"},
)

print(f"Category: {error.category.value}")     # data
print(f"Severity: {error.severity.value}")      # medium
print(f"Source: {error.source_file}:{error.source_line}")
print(f"Function: {error.source_function}")
print(f"Stack frames: {len(error.stack_frames)}")

# Check for recurring errors
patterns = agent.get_error_patterns()
for p in patterns:
    print(f"  {p['error_type']}: {p['count']} times (last: {p['last_seen']})")

# Resolve when fixed
agent.resolve_error(error.error_id)
```

### Root Cause Analysis

```python
# Start investigation
rca = agent.start_root_cause_analysis("Production API returning 500 errors")

# Add evidence
agent.add_rca_evidence(rca, "error_logs", "NullPointerException at line 42", {
    "stack_trace": "...",
    "frequency": "every 10th request",
})
agent.add_rca_evidence(rca, "metrics", "Error rate spiked", {
    "error_rate_before": "0.1%",
    "error_rate_after": "5.2%",
    "correlated_change": "deploy v2.3.1",
})

# Form hypothesis
agent.form_hypothesis(
    rca,
    "v2.3.1 deployment introduced null-safety regression in user profile handler",
    RootCauseCategory.CODE_DEFECT,
)

# Confirm with confidence
agent.confirm_root_cause(
    rca,
    root_cause="Missing null check in UserProfile.get_display_name() after refactoring",
    confidence=0.92,
    contributing_factors=[
        "No null-safety tests for edge cases",
        "Code review missed the regression",
    ],
    recommendations=[
        "Add null check: if self.name is None: return 'Anonymous'",
        "Add unit test for null name case",
        "Add integration test for profile endpoint",
    ],
)

# Get fix suggestions
fixes = agent.generate_fix_suggestions(rca)
for fix in fixes:
    print(f"[{fix.fix_type.value}] {fix.title} (confidence: {fix.confidence:.0%})")
```

### Performance Profiling

```python
# CPU profiling
cpu = agent.create_profile(
    profiling_type=ProfilingType.CPU,
    duration_seconds=3.0,
    samples=5000,
    top_functions=[
        {"name": "render_template", "percentage": 38.2, "calls": 2000},
        {"name": "validate_input", "percentage": 22.5, "calls": 2000},
        {"name": "serialize_response", "percentage": 18.1, "calls": 2000},
    ],
    summary={"total_time_ms": 3000, "function_count": 150},
)
print(f"Recommendations: {cpu.recommendations}")

# Memory profiling
mem = agent.create_profile(
    profiling_type=ProfilingType.MEMORY,
    duration_seconds=10.0,
    samples=1000,
    summary={"peak_memory_mb": 680, "allocation_count": 300000},
)
print(f"Recommendations: {mem.recommendations}")

# Database profiling
db = agent.create_profile(
    profiling_type=ProfilingType.DATABASE,
    duration_seconds=30.0,
    samples=2000,
    summary={"slow_queries": 8, "n_plus_one": True, "total_queries": 3000},
)
print(f"Recommendations: {db.recommendations}")

# Analyze all profiles
analysis = agent.analyze_profiles()
```

### Distributed Tracing

```python
trace_id = uuid.uuid4().hex[:16]

# Record spans
agent.create_trace_span(trace_id, "http_request", "api-gateway", duration_ms=420)
agent.create_trace_span(trace_id, "authenticate", "auth-service", duration_ms=55)
agent.create_trace_span(trace_id, "get_user", "user-service", duration_ms=200)
agent.create_trace_span(trace_id, "db_query", "postgres", duration_ms=160,
                        status=TraceSpanStatus.ERROR, error="Deadlock detected")

# Analyze
analysis = agent.analyze_trace(trace_id)
print(f"Total duration: {analysis.total_duration_ms}ms")
print(f"Spans: {analysis.span_count} ({analysis.error_spans} errors)")
print(f"Bottleneck: {analysis.bottleneck_service}")
print(f"Critical path: {' -> '.join(analysis.critical_path)}")
for rec in analysis.recommendations:
    print(f"  {rec}")
```

### Log Analysis

```python
# Add entries
for i in range(200):
    agent.add_log_entry(LogEntry(
        level="INFO" if i % 15 != 0 else "ERROR",
        message=f"Processed request {i}" if i % 15 != 0
                else f"Failed to process: timeout connecting to service-{i % 3}",
        source="app.processor",
    ))

# Analyze
analysis = agent.analyze_logs()
print(f"Total: {analysis.total_entries}")
print(f"Levels: {analysis.by_level}")
print(f"Error patterns: {len(analysis.error_patterns)}")
for pattern in analysis.error_patterns[:3]:
    print(f"  {pattern['count']}x: {pattern['pattern'][:60]}")
print(f"Recommendations: {analysis.recommendations}")
```

### Logging Strategy

```python
config = LoggingConfig(
    current_level="DEBUG",
    format="text",
    structured=False,
    correlation_ids=False,
    sampling_rate=1.0,
)

# Audit
analysis = agent.analyze_logging_strategy(config)
for issue in analysis["issues"]:
    print(f"Issue: {issue}")
for rec in analysis["recommendations"]:
    print(f"Recommendation: {rec}")

# Optimize
optimized = agent.optimize_logging(config)
print(f"Optimized: structured={optimized.structured}, "
      f"correlation={optimized.correlation_ids}, "
      f"sampling={optimized.sampling_rate}")
```

### Debug Sessions

```python
# Create and manage sessions
session = agent.create_session("Login page throws 500 error")
agent.advance_phase(session.session_id, DebugPhase.REPRODUCE)
agent.advance_phase(session.session_id, DebugPhase.ISOLATE)
agent.advance_phase(session.session_id, DebugPhase.HYPOTHESIZE)

# Add notes
session.notes.append("Reproduced on Chrome 120, not on Firefox 121")
session.notes.append("Isolated to auth.js:processToken")

# End session
agent.end_session(session.session_id)

# Generate report
report = agent.generate_debug_report(session.session_id)
print(report)
```

### Comprehensive Debug

```python
# One-call comprehensive analysis
result = agent.debug_issue(
    error_message="DatabaseError: deadlock detected",
    error_type="DatabaseError",
    stack_trace='File "app/models/order.py", line 112, in create_order\n    with transaction.atomic():\n        ...',
)

print(f"Session: {result['session']['session_id']}")
print(f"Error category: {result['error']['category']}")
print(f"Root cause: {result['root_cause_analysis']['root_cause']}")
print(f"Confidence: {result['root_cause_analysis']['confidence']}")
print(f"Fixes: {len(result['fix_suggestions'])}")
for fix in result['fix_suggestions']:
    print(f"  [{fix['fix_type']}] {fix['title']}")
```

---

## API Reference

### DebuggingAgent

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `create_session` | issue_title | DebugSession | Start a debug session |
| `get_session` | session_id | DebugSession | Get session by ID |
| `advance_phase` | session_id, phase | DebugSession | Move to next phase |
| `end_session` | session_id | DebugSession | Complete session |
| `list_sessions` | status? | List[DebugSession] | List sessions |
| `analyze_error` | message, type?, stack?, context? | ErrorInfo | Classify error |
| `get_error_history` | category?, severity?, limit? | List[ErrorInfo] | Error history |
| `get_error_patterns` | - | List[Dict] | Recurring patterns |
| `resolve_error` | error_id | bool | Mark resolved |
| `start_root_cause_analysis` | description | RootCauseAnalysis | Begin RCA |
| `add_rca_evidence` | rca, type, desc, data? | RootCauseAnalysis | Add evidence |
| `form_hypothesis` | rca, hypothesis, category? | RootCauseAnalysis | Form hypothesis |
| `confirm_root_cause` | rca, cause, confidence, factors?, recs? | RootCauseAnalysis | Confirm cause |
| `generate_fix_suggestions` | rca | List[FixSuggestion] | Get fix ideas |
| `create_profile` | type, duration, samples, funcs?, hotspots?, summary? | ProfileResult | Create profile |
| `analyze_profiles` | - | Dict | Analyze all profiles |
| `create_trace_span` | trace_id, op, service, parent?, duration?, status?, error?, tags? | TraceSpan | Record span |
| `analyze_trace` | trace_id | TraceAnalysis | Analyze trace |
| `get_trace_spans` | trace_id | List[TraceSpan] | Get spans |
| `add_log_entry` | entry | None | Add log entry |
| `add_log_entries` | entries | None | Add multiple |
| `analyze_logs` | - | LogAnalysis | Analyze logs |
| `analyze_logging_strategy` | config | Dict | Audit logging |
| `optimize_logging` | config | LoggingConfig | Optimize config |
| `debug_issue` | message, type?, stack?, context? | Dict | Comprehensive debug |
| `get_status` | - | Dict | Agent status |
| `generate_debug_report` | session_id | str | Debug report |

---

## Examples

### Example 1: Production Incident Debugging

```python
agent = DebuggingAgent()

# Error starts appearing in production
error = agent.analyze_error(
    error_message="TimeoutError: Request timeout after 30s",
    error_type="TimeoutError",
    stack_trace='File "app/services/payment.py", line 45, in process\n    response = gateway.charge(amount)',
)

# Start investigation
rca = agent.start_root_cause_analysis("Payment processing timeouts")
agent.add_rca_evidence(rca, "monitoring", "Payment gateway response time increased", {
    "p50_before_ms": 200, "p50_after_ms": 5000,
})
agent.form_hypothesis(rca, "Payment gateway degraded, need fallback", RootCauseCategory.EXTERNAL_DEPENDENCY)
agent.confirm_root_cause(rca, "Payment gateway p99 latency increased 25x", 0.85,
                         recommendations=["Implement circuit breaker", "Add fallback provider"])
```

### Example 2: Memory Leak Investigation

```python
# Profile shows growing memory
mem = agent.create_profile(
    profiling_type=ProfilingType.MEMORY,
    duration_seconds=3600,
    samples=3600,
    summary={"peak_memory_mb": 2048, "allocation_count": 5000000, "leak_suspected": True},
)
print(f"Recommendations: {mem.recommendations}")
# Returns: "Peak memory usage (2048.0MB) exceeds critical threshold."
```

### Example 3: Microservice Latency

```python
trace_id = "abc123"
agent.create_trace_span(trace_id, "checkout", "gateway", duration_ms=2500)
agent.create_trace_span(trace_id, "validate_cart", "cart-service", duration_ms=100)
agent.create_trace_span(trace_id, "process_payment", "payment-service", duration_ms=2000)
agent.create_trace_span(trace_id, "charge", "stripe-api", duration_ms=1800)
agent.create_trace_span(trace_id, "send_confirmation", "email-service", duration_ms=350)

analysis = agent.analyze_trace(trace_id)
# Bottleneck: stripe-api (1800ms out of 2500ms total)
# Recommendation: Focus optimization on payment-service → stripe-api call
```

---

## Configuration

```python
config = DebuggingConfig(
    max_stack_frames=50,
    slow_threshold_ms=1000.0,
    very_slow_threshold_ms=5000.0,
    memory_warning_mb=512.0,
    memory_critical_mb=1024.0,
    cpu_warning_percent=70.0,
    cpu_critical_percent=90.0,
    confidence_threshold=0.7,
    enable_auto_categorization=True,
    enable_pattern_detection=True,
    enable_correlation=True,
)
agent = DebuggingAgent(config)
```

---

## Best Practices

1. **Always reproduce first** — Don't guess; confirm you can trigger the issue
2. **Isolate before fixing** — Narrow down to the smallest possible scope
3. **Add evidence systematically** — Each piece of evidence increases confidence
4. **Use the right profiling type** — CPU for speed, memory for leaks, DB for queries
5. **Trace across services** — Distributed issues need distributed traces
6. **Normalize log messages** — Remove IDs/numbers to find true patterns
7. **Optimize logging proactively** — Don't wait for production issues
8. **Document every session** — Build institutional knowledge
9. **Verify fixes** — Always confirm the issue is resolved
10. **Prevent recurrence** — Add monitoring and tests for every fix

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Error classified as UNKNOWN | Add custom patterns to `DebuggingConfig.known_error_patterns` |
| Low RCA confidence | Add more evidence; run profiling or tracing |
| No profile recommendations | Provide meaningful `summary` dict with metrics |
| Trace shows no bottleneck | Check `service_breakdown` for highest total time |
| Log patterns missed | Ensure `level` is set correctly and `source` is populated |
| Debug report incomplete | Run all phases: reproduce → isolate → hypothesize → investigate → fix → verify → prevent |

---

## Contributing

Guidelines:
1. Add new error patterns in `DebuggingConfig.known_error_patterns`
2. Add new profiling types via `ProfilingType` enum
3. Add new root cause categories with corresponding fix types
4. Extend stack trace parser for new languages
5. Add new logging strategy recommendations
6. Include type hints for all public methods
7. Test edge cases: empty inputs, missing data, malformed traces

---

## License

MIT License — See [LICENSE](../../LICENSE) for details.
