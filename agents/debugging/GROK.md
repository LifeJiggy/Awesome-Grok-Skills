---
name: debugging
version: 2.0.0
description: Systematic debugging agent for error analysis, root cause investigation, performance profiling, distributed tracing, log analysis, and automated fix suggestions
author: Awesome Grok Skills
tags:
  - debugging
  - error-analysis
  - root-cause-analysis
  - profiling
  - tracing
  - logging
  - performance
  - troubleshooting
  - observability
  - fix-suggestions
category: development-tools
personality: methodical, analytical, systematic, patient
use_cases:
  - Error classification and stack trace analysis
  - Root cause investigation with structured methodology
  - Performance profiling (CPU, memory, I/O, database)
  - Distributed trace analysis and bottleneck detection
  - Log pattern analysis and correlation detection
  - Logging strategy optimization
  - Automated fix suggestion generation
  - Debug session management and reporting
---

# Debugging Agent

## Agent Identity

The Debugging Agent is a systematic debugging platform that helps developers diagnose and resolve software issues through structured error analysis, root cause investigation, performance profiling, distributed tracing, and log analysis. It follows a proven 7-phase debugging methodology and generates actionable fix suggestions.

## Core Principles

1. **Reproduce first** — Never fix what you can't reproduce
2. **Isolate systematically** — Narrow down to the smallest possible scope
3. **Hypothesize then verify** — Form theories, then gather evidence
4. **Root causes, not symptoms** — Fix the underlying issue, not the surface error
5. **Document everything** — Build knowledge base from every debugging session
6. **Prevent recurrence** — Every fix should include monitoring and tests

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        DebuggingAgent                                      │
│                                                                          │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────────┐  │
│  │  Error         │  │  Root Cause    │  │  Profiler                  │  │
│  │  Analyzer      │  │  Analysis      │  │  ├ CPU                     │  │
│  │  ├ Classify    │  │  ├ Evidence    │  │  ├ Memory                  │  │
│  │  ├ Patterns    │  │  ├ Hypothesis  │  │  ├ I/O                     │  │
│  │  ├ History     │  │  ├ Confirm     │  │  └ Database                │  │
│  │  └ Severity    │  │  └ Fix Suggest │  │                            │  │
│  └────────────────┘  └────────────────┘  └────────────────────────────┘  │
│                                                                          │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────────┐  │
│  │  Distributed   │  │  Log           │  │  Session                   │  │
│  │  Tracer        │  │  Analyzer      │  │  Manager                   │  │
│  │  ├ Spans       │  │  ├ Patterns    │  │  ├ Create                  │  │
│  │  ├ Timeline    │  │  ├ Correlation │  │  ├ Track phases            │  │
│  │  ├ Bottleneck  │  │  ├ Anomalies   │  │  ├ Artifacts               │  │
│  │  └ Analysis    │  │  └ Strategy    │  │  └ Report                  │  │
│  └────────────────┘  └────────────────┘  └────────────────────────────┘  │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐│
│  │  Fix Suggestion Engine                                               ││
│  │  ├ Code fixes  │ Config changes  │ Dependency updates  │ Arch changes││
│  └──────────────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────────────┘
```

## Capabilities

### 1. Error Analysis

```python
agent = DebuggingAgent()

# Analyze an error
error = agent.analyze_error(
    error_message="TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'",
    error_type="TypeError",
    stack_trace='File "app/user.py", line 42, in get_balance\n    return self.balance + bonus',
    context={"user_id": 12345},
)
print(f"Category: {error.category.value}")  # type_error
print(f"Severity: {error.severity.value}")  # medium
print(f"Source: {error.source_file}:{error.source_line}")

# Check for recurring patterns
patterns = agent.get_error_patterns()
for p in patterns:
    print(f"{p['error_type']}: {p['count']} occurrences")
```

**Error Classification Matrix:**

| Error Type | Category | Severity | Common Cause |
|-----------|----------|----------|--------------|
| TypeError | TYPE_ERROR | Medium | Wrong data type |
| NullReference | REFERENCE_ERROR | High | Uninitialized variable |
| ValueError | DATA | Medium | Invalid input |
| KeyError | DATA | Medium | Missing dictionary key |
| Timeout | TIMEOUT | High | Slow external service |
| ConnectionError | NETWORK | High | Network failure |
| MemoryError | MEMORY | Critical | Resource exhaustion |
| ImportError | DEPENDENCY | Medium | Missing package |
| PermissionError | PERMISSION | High | Access denied |

**Error Analysis Flow:**

```
  ┌──────────────┐
  │  Error       │
  │  Input       │
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
  │  Classify    │───►│  Pattern     │───►│  Severity    │
  │  (20+ types) │    │  Detection   │    │  Assessment  │
  └──────────────┘    └──────────────┘    └──────┬───────┘
                                                 │
                                                 ▼
                                          ┌──────────────┐
                                          │  Fix         │
                                          │  Suggestions │
                                          └──────────────┘
```

### 2. Root Cause Analysis

```python
# Start a structured investigation
rca = agent.start_root_cause_analysis("Database connection timeout in production")

# Add evidence
agent.add_rca_evidence(rca, "logs", "Connection pool exhausted", {"pool_size": 100, "active": 100})
agent.add_rca_evidence(rca, "metrics", "Request rate doubled", {"rpm_before": 1000, "rpm_after": 2000})

# Form hypothesis
agent.form_hypothesis(
    rca,
    "Connection pool size insufficient for traffic spike",
    RootCauseCategory.RESOURCE_LIMIT,
)

# Confirm root cause
agent.confirm_root_cause(
    rca,
    root_cause="Pool size of 100 too small for 2000 RPM peak",
    confidence=0.95,
    contributing_factors=["No auto-scaling configured", "No connection pooling tuning"],
    recommendations=["Increase pool to 200", "Add connection pool monitoring", "Implement auto-scaling"],
)

# Generate fixes
fixes = agent.generate_fix_suggestions(rca)
```

**Root Cause Categories:**

| Category | Example | Detection |
|----------|---------|-----------|
| CODE_DEFECT | Null pointer, off-by-one | Stack trace, unit test |
| DESIGN_FLAW | N+1 queries, missing indexes | Profiling, code review |
| CONFIGURATION_ERROR | Wrong env var, missing config | Config diff, audit |
| DEPENDENCY_FAILURE | Library bug, API change | Version check, logs |
| RESOURCE_LIMIT | OOM, disk full, pool exhaustion | Monitoring, metrics |
| CONCURRENCY_ISSUE | Race condition, deadlock | Profiling, stress test |
| DATA_CORRUPTION | Invalid data, missing records | Data validation |
| SECURITY_VULNERABILITY | SQL injection, XSS | Security scan |

**RCA Investigation Flow:**

```
  ┌──────────────┐
  │  Issue       │
  │  Reported    │
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │  Reproduce   │
  │  Issue       │
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
  │  Gather      │───►│  Form        │───►│  Test        │
  │  Evidence    │    │  Hypotheses  │    │  Hypotheses  │
  └──────────────┘    └──────────────┘    └──────┬───────┘
                                                 │
                                                 ▼
                                          ┌──────────────┐
                                          │  Confirm     │
                                          │  Root Cause  │
                                          └──────┬───────┘
                                                 │
                                                 ▼
                                          ┌──────────────┐
                                          │  Generate    │
                                          │  Fixes       │
                                          └──────────────┘
```

### 3. Performance Profiling

```python
# CPU profiling
cpu_profile = agent.create_profile(
    profiling_type=ProfilingType.CPU,
    duration_seconds=5.0,
    samples=10000,
    top_functions=[
        {"name": "process_data", "percentage": 42.5, "calls": 5000},
        {"name": "serialize", "percentage": 28.1, "calls": 5000},
        {"name": "validate", "percentage": 12.3, "calls": 5000},
    ],
    summary={"total_time_ms": 5000, "function_count": 200},
)
# Returns targeted recommendations:
# "Function 'process_data' consumes 42.5% of CPU time. Consider optimization or caching."

# Memory profiling
mem_profile = agent.create_profile(
    profiling_type=ProfilingType.MEMORY,
    duration_seconds=10.0,
    samples=1000,
    summary={"peak_memory_mb": 750, "allocation_count": 250000},
)
# Returns: "Peak memory usage (750.0MB) exceeds warning threshold."

# Database profiling
db_profile = agent.create_profile(
    profiling_type=ProfilingType.DATABASE,
    duration_seconds=30.0,
    samples=500,
    summary={"slow_queries": 12, "n_plus_one": True, "total_queries": 1500},
)
# Returns: "12 slow queries detected." and "N+1 query pattern detected."
```

**Profiling Types:**

| Type | Focus | Key Metrics | Tools |
|------|-------|-------------|-------|
| CPU | Processor usage | Time %, call count | cProfile, py-spy |
| MEMORY | RAM allocation | Peak, allocations | tracemalloc, memory_profiler |
| I/O | Disk/network | Read/write ops | iostat, strace |
| DATABASE | Query performance | Slow queries, N+1 | pg_stat, EXPLAIN |
| NETWORK | API latency | Response time, throughput | tcpdump, Wireshark |

### 4. Distributed Tracing

```python
trace_id = uuid.uuid4().hex[:16]

# Create trace spans
agent.create_trace_span(trace_id, "http_request", "api-gateway", duration_ms=350)
agent.create_trace_span(trace_id, "authenticate", "auth-service", duration_ms=45)
agent.create_trace_span(trace_id, "query_user", "user-service", duration_ms=180)
agent.create_trace_span(trace_id, "db_query", "postgres", duration_ms=140, status=TraceSpanStatus.ERROR, error="timeout")

# Analyze the trace
analysis = agent.analyze_trace(trace_id)
print(f"Total: {analysis.total_duration_ms}ms across {analysis.span_count} spans")
print(f"Bottleneck: {analysis.bottleneck_service}")
print(f"Error spans: {analysis.error_spans}")
print(f"Recommendations: {analysis.recommendations}")
```

**Trace Visualization:**

```
api-gateway     [████████████████████████████████████████] 350ms
  auth-service  [███████]                                   45ms
  user-service  [██████████████████████]                   180ms
    postgres    [████████████████████]                     140ms ← BOTTLENECK
  └──────────────────────────────────────────────────────────────┘
```

### 5. Log Analysis

```python
# Add log entries
agent.add_log_entries([
    LogEntry(level="ERROR", message="Connection timeout to db-primary", source="db.pool"),
    LogEntry(level="ERROR", message="Connection timeout to db-primary", source="db.pool"),
    LogEntry(level="WARN", message="Slow query detected (2.5s)", source="db.query"),
    LogEntry(level="INFO", message="Request processed successfully", source="api.handler"),
])

# Analyze patterns
analysis = agent.analyze_logs()
print(f"By level: {analysis.by_level}")
print(f"Error patterns: {len(analysis.error_patterns)}")
print(f"Correlated errors: {len(analysis.correlated_errors)}")
print(f"Recommendations: {analysis.recommendations}")
```

**Log Level Guidelines:**

```
┌──────────┬────────────────────────────────────────────────────────────┐
│  Level   │  When to Use                                               │
├──────────┼────────────────────────────────────────────────────────────┤
│  DEBUG   │  Detailed diagnostic info for developers                   │
│  INFO    │  General operational events (startup, shutdown)            │
│  WARN    │  Unexpected but handled situation (retry, fallback)        │
│  ERROR   │  Operation failed, needs attention                         │
│  CRITICAL│  System is unusable, immediate action required             │
└──────────┴────────────────────────────────────────────────────────────┘
```

### 6. Logging Strategy

```python
config = LoggingConfig(
    current_level="DEBUG",
    format="text",
    structured=False,
    correlation_ids=False,
)
analysis = agent.analyze_logging_strategy(config)
# Identifies: no structured logging, no correlation, no PII redaction

# Apply optimizations
optimized = agent.optimize_logging(config)
# Returns: structured=True, correlation_ids=True, sampling=0.1, redaction patterns
```

### 7. Comprehensive Debug Workflow

```python
# One-call comprehensive analysis
result = agent.debug_issue(
    error_message="ConnectionError: Unable to connect to database",
    error_type="ConnectionError",
    stack_trace='File "app/db/pool.py", line 88, in get_connection\n    return psycopg2.connect(dsn)',
)
print(result["session"])         # Session with all artifacts
print(result["error"])           # Classified error
print(result["root_cause_analysis"])  # Structured RCA
print(result["fix_suggestions"])      # Actionable fixes
```

## Operational Guidelines

### Debugging Methodology

```
Phase 1: REPRODUCE → Can you trigger the issue reliably?
Phase 2: ISOLATE → Which component/module/code path?
Phase 3: HYPOTHESIZE → What do you think is the cause?
Phase 4: INVESTIGATE → Gather evidence to confirm/deny
Phase 5: FIX → Apply the fix
Phase 6: VERIFY → Confirm the issue is resolved
Phase 7: PREVENT → Add monitoring, tests, documentation
```

**Methodology Flow:**

```
  ┌──────────────┐
  │  1. REPRODUCE│
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │  2. ISOLATE  │
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │  3. HYPOTHESIZE│
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │  4. INVESTIGATE│
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │  5. FIX      │
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │  6. VERIFY   │
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │  7. PREVENT  │
  └──────────────┘
```

### When to Use Each Capability

| Situation | Use |
|-----------|-----|
| New error in production | `analyze_error` → `debug_issue` |
| Intermittent failure | `analyze_error` with patterns → RCA |
| Slow endpoint | `create_profile` (CPU/DB) → recommendations |
| Cross-service latency | `create_trace_span` → `analyze_trace` |
| Too many logs | `analyze_logs` → pattern detection |
| Logging gaps | `analyze_logging_strategy` → optimize |

### Fix Suggestion Confidence

| Confidence | Action |
|------------|--------|
| >= 0.9 | High confidence — apply with standard testing |
| 0.7 - 0.9 | Medium confidence — apply with careful testing |
| < 0.7 | Low confidence — investigate more before applying |

## Method Signatures

```python
class DebuggingAgent:
    def __init__(self, config: Optional[DebuggingConfig] = None) -> None: ...

    # Sessions
    def create_session(self, issue_title: str) -> DebugSession: ...
    def get_session(self, session_id: str) -> DebugSession: ...
    def advance_phase(self, session_id: str, phase: DebugPhase) -> DebugSession: ...
    def end_session(self, session_id: str) -> DebugSession: ...
    def list_sessions(self, status: Optional[str] = None) -> List[DebugSession]: ...

    # Error Analysis
    def analyze_error(self, error_message, error_type="", stack_trace="", context=None) -> ErrorInfo: ...
    def get_error_history(self, category=None, severity=None, limit=50) -> List[ErrorInfo]: ...
    def get_error_patterns(self) -> List[Dict[str, Any]]: ...
    def resolve_error(self, error_id: str) -> bool: ...

    # Root Cause Analysis
    def start_root_cause_analysis(self, issue_description: str) -> RootCauseAnalysis: ...
    def add_rca_evidence(self, rca, evidence_type, description, data=None) -> RootCauseAnalysis: ...
    def form_hypothesis(self, rca, hypothesis, category=...) -> RootCauseAnalysis: ...
    def confirm_root_cause(self, rca, root_cause, confidence, contributing_factors=None, recommendations=None) -> RootCauseAnalysis: ...
    def generate_fix_suggestions(self, rca) -> List[FixSuggestion]: ...

    # Profiling
    def create_profile(self, profiling_type, duration_seconds, samples, top_functions=None, hotspots=None, summary=None) -> ProfileResult: ...
    def analyze_profiles(self) -> Dict[str, Any]: ...

    # Distributed Tracing
    def create_trace_span(self, trace_id, operation, service, parent_span_id=None, duration_ms=0, status=..., error=None, tags=None) -> TraceSpan: ...
    def analyze_trace(self, trace_id: str) -> TraceAnalysis: ...
    def get_trace_spans(self, trace_id: str) -> List[TraceSpan]: ...

    # Log Analysis
    def add_log_entry(self, entry: LogEntry) -> None: ...
    def add_log_entries(self, entries: List[LogEntry]) -> None: ...
    def analyze_logs(self) -> LogAnalysis: ...

    # Logging Strategy
    def analyze_logging_strategy(self, config: LoggingConfig) -> Dict[str, Any]: ...
    def optimize_logging(self, config: LoggingConfig) -> LoggingConfig: ...

    # Comprehensive
    def debug_issue(self, error_message, error_type="", stack_trace="", context=None) -> Dict[str, Any]: ...

    # Status
    def get_status(self) -> Dict[str, Any]: ...
    def generate_debug_report(self, session_id: str) -> str: ...
```

## Data Models

### ErrorCategory

```python
class ErrorCategory(Enum):
    RUNTIME = "runtime"
    TYPE_ERROR = "type_error"
    REFERENCE_ERROR = "reference_error"
    SYNTAX_ERROR = "syntax_error"
    LOGIC_ERROR = "logic_error"
    PERFORMANCE = "performance"
    MEMORY = "memory"
    NETWORK = "network"
    CONCURRENCY = "concurrency"
    SECURITY = "security"
    CONFIGURATION = "configuration"
    DEPENDENCY = "dependency"
    DATA = "data"
    PERMISSION = "permission"
    TIMEOUT = "timeout"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    UNKNOWN = "unknown"
```

### DebugPhase

```python
class DebugPhase(Enum):
    REPRODUCE = "reproduce"
    ISOLATE = "isolate"
    HYPOTHESIZE = "hypothesize"
    INVESTIGATE = "investigate"
    FIX = "fix"
    VERIFY = "verify"
    PREVENT = "prevent"
```

### RootCauseCategory

```python
class RootCauseCategory(Enum):
    CODE_DEFECT = "code_defect"
    DESIGN_FLAW = "design_flaw"
    CONFIGURATION_ERROR = "configuration_error"
    DEPENDENCY_FAILURE = "dependency_failure"
    RESOURCE_LIMIT = "resource_limit"
    CONCURRENCY_ISSUE = "concurrency_issue"
    DATA_CORRUPTION = "data_corruption"
    SECURITY_VULNERABILITY = "security_vulnerability"
    EXTERNAL_DEPENDENCY = "external_dependency"
    HUMAN_ERROR = "human_error"
    UNKNOWN = "unknown"
```

### Key Data Classes

```python
@dataclass
class ErrorInfo:
    error_id: str
    message: str
    error_type: str
    category: ErrorCategory
    severity: str
    source_file: str
    source_line: int
    stack_trace: str
    context: Dict[str, Any]
    first_seen: datetime
    last_seen: datetime
    occurrence_count: int

@dataclass
class RootCauseAnalysis:
    rca_id: str
    issue_description: str
    status: str
    evidence: List[Dict[str, Any]]
    hypotheses: List[Dict[str, Any]]
    root_cause: Optional[str]
    confidence: float
    contributing_factors: List[str]
    recommendations: List[str]

@dataclass
class FixSuggestion:
    suggestion_id: str
    rca_id: str
    title: str
    description: str
    confidence: float
    fix_type: str  # code, config, dependency, architecture
    code_changes: Optional[str]
    testing_notes: str
```

## Security Considerations

### Sensitive Data in Errors

```
┌──────────────────────────────────────────────────────────────┐
│               Security Checklist for Debugging                 │
├──────────────────────────────────────────────────────────────┤
│  □ Redact passwords, tokens, API keys from stack traces      │
│  □ Mask PII in log entries                                   │
│  □ Sanitize error messages before logging                    │
│  □ Never include credentials in error context                │
│  □ Use structured logging with field-level redaction         │
│  □ Audit debug logs for sensitive data exposure              │
└──────────────────────────────────────────────────────────────┘
```

### Logging Best Practices

- Use correlation IDs for request tracing
- Implement log rotation to prevent disk exhaustion
- Set appropriate log levels per environment
- Use structured logging for machine parsing
- Implement log aggregation for centralized analysis

## Scalability

### Handling High-Volume Errors

| Error Volume | Strategy |
|-------------|----------|
| < 100/day | Individual analysis |
| 100-1000/day | Pattern detection, batch analysis |
| 1000-10000/day | Sampling, aggregation, alerting |
| > 10000/day | Deduplication, rate limiting, bulk RCA |

### Performance Considerations

- Profile data retention: 30 days default
- Log entry limit: 100K entries per analysis
- Trace span limit: 1000 spans per trace
- RCA evidence limit: 50 items per investigation

## Design Patterns

### Strategy Pattern for Error Classification

```python
class ErrorClassifier:
    def __init__(self):
        self._strategies = {}
    
    def register(self, error_type: str, strategy: ClassificationStrategy):
        self._strategies[error_type] = strategy
    
    def classify(self, error: ErrorInfo) -> ErrorCategory:
        strategy = self._strategies.get(error.error_type)
        if strategy:
            return strategy.classify(error)
        return ErrorCategory.UNKNOWN
```

### Chain of Responsibility for Fix Suggestions

```python
class FixHandler:
    def __init__(self):
        self._next_handler = None
    
    def set_next(self, handler: 'FixHandler') -> 'FixHandler':
        self._next_handler = handler
        return handler
    
    def handle(self, rca: RootCauseAnalysis) -> Optional[FixSuggestion]:
        if self.can_handle(rca):
            return self.apply_fix(rca)
        if self._next_handler:
            return self._next_handler.handle(rca)
        return None
```

### Observer Pattern for Debug Events

```python
class DebugEventBus:
    def __init__(self):
        self._subscribers = defaultdict(list)
    
    def subscribe(self, event_type: str, callback: Callable):
        self._subscribers[event_type].append(callback)
    
    def publish(self, event_type: str, data: Any):
        for callback in self._subscribers[event_type]:
            callback(data)
```

## Checklists

### New Error Investigation

- [ ] Reproduce the error reliably
- [ ] Classify with `analyze_error`
- [ ] Check for recurring patterns
- [ ] Start root cause analysis
- [ ] Add evidence from logs, metrics, stack traces
- [ ] Form and test hypothesis
- [ ] Confirm root cause with confidence
- [ ] Generate fix suggestions
- [ ] Apply fix with testing
- [ ] Add monitoring for recurrence

### Performance Investigation

- [ ] Profile CPU usage
- [ ] Profile memory allocation
- [ ] Profile I/O operations
- [ ] Profile database queries
- [ ] Identify top consumers
- [ ] Generate optimization recommendations
- [ ] Apply optimizations
- [ ] Re-profile to verify improvement

### Distributed System Debugging

- [ ] Collect trace spans from all services
- [ ] Analyze trace for total duration
- [ ] Identify bottleneck service
- [ ] Check for error spans
- [ ] Review service breakdown
- [ ] Focus optimization on bottleneck
- [ ] Add tracing to uninstrumented code

### Logging Strategy Review

- [ ] Verify structured logging enabled
- [ ] Check correlation ID propagation
- [ ] Review log level appropriateness
- [ ] Validate PII redaction
- [ ] Assess log volume and retention
- [ ] Test log aggregation pipeline

## Troubleshooting

### Error Classification Returns UNKNOWN

- Check that `error_type` matches a known pattern in `config.known_error_patterns`
- Add custom patterns to the config if needed
- The message-based fallback may catch it

### Root Cause Confidence Low

- Add more evidence to the analysis
- Check if multiple root causes are contributing
- Consider running profiling or trace analysis for more data

### Profile Recommendations Empty

- Ensure `summary` contains meaningful metrics
- Check that hotspots or top_functions are provided
- Verify profiling_type matches the data collected

### Trace Analysis Shows No Bottleneck

- Spans may have similar durations — check service_breakdown for the highest total
- Ensure all relevant services have trace spans
- Consider adding more granular spans

### Log Analysis Misses Patterns

- Ensure `error` level is set correctly in LogEntry
- Check that source field is populated for correlation
- Verify log entries are within the analysis window

## Integration Points

### With Other Agents

- **debugging**: Core debugging capabilities
- **devops**: Deployment and infrastructure context
- **monitoring**: Metric and alert correlation
- **security**: Vulnerability-related errors

### External Tools

- APM: Datadog, New Relic, Dynatrace
- Logging: ELK Stack, Splunk, CloudWatch
- Tracing: Jaeger, Zipkin, OpenTelemetry
- Profiling: py-spy, cProfile, memory_profiler

## Performance Benchmarks

| Operation | Small (< 1K entries) | Medium (< 100K) | Large (< 1M) |
|-----------|---------------------|-----------------|--------------|
| Error analysis | 10ms | 100ms | 1s |
| Log pattern detection | 50ms | 500ms | 5s |
| Trace analysis | 20ms | 200ms | 2s |
| Profile analysis | 100ms | 1s | 10s |
| RCA generation | 50ms | 500ms | 5s |

## Future Enhancements

- AI-powered root cause prediction
- Automated fix application with rollback
- Real-time distributed tracing integration
- Natural language debugging queries
- Cross-language stack trace correlation
- Predictive error detection
- Automated regression test generation
- Integration with CI/CD for pre-deploy analysis
