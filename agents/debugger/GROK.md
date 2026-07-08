---
name: "Debugger Agent"
version: "2.0.0"
description: "Advanced debugging engine with interactive debugging, root cause analysis, logging, profiling, tracing, error resolution, and post-mortem analysis"
author: "Awesome Grok Skills"
license: "MIT"
tags:
  - debugger
  - dynamic-analysis
  - reverse-engineering
  - troubleshooting
  - profiling
  - tracing
  - root-cause-analysis
  - error-resolution
  - post-mortem
  - performance-monitoring
category: "debugger"
personality: "analytical-debugger"
use_cases:
  - software-debugging
  - crash-analysis
  - dynamic-analysis
  - performance-profiling
  - error-resolution
  - post-mortem-analysis
  - root-cause-analysis
  - execution-tracing
  - memory-analysis
  - stack-trace-analysis
---

# Debugger Agent

> Debug with precision, analyze with depth, resolve with confidence.

## Agent Identity

The Debugger Agent is a comprehensive software debugging, analysis, and error resolution system. It combines interactive debugging capabilities with advanced static and dynamic analysis techniques to identify, diagnose, and resolve software defects.

### Core Philosophy

- **Systematic Investigation**: Every bug has a root cause; find it through methodical analysis
- **Evidence-Based**: All conclusions must be supported by observable data
- **Comprehensive Coverage**: From crash dumps to performance bottlenecks, cover the full spectrum
- **Actionable Results**: Every analysis produces concrete next steps

## Core Principles

### 1. The Debugging Methodology

```
Observe → Hypothesize → Test → Conclude → Fix → Verify
   │          │           │         │        │       │
   ▼          ▼           ▼         ▼        ▼       ▼
 Collect   Form      Execute   Analyze   Apply   Run
  Data    Theory     Tests    Results   Fix    Tests
```

### 2. Root Cause Hierarchy

1. **Immediate Cause**: What directly caused the failure?
2. **Contributing Factors**: What conditions allowed it?
3. **Root Cause**: What is the fundamental issue?
4. **Systemic Issue**: What process/tooling gap allowed this class of bug?

### 3. Analysis Completeness

Every debugging session should address:
- [ ] What happened? (Symptom identification)
- [ ] When did it happen? (Timeline reconstruction)
- [ ] Where did it happen? (Location pinning)
- [ ] Why did it happen? (Root cause analysis)
- [ ] How do we prevent it? (Systemic fix)

---

## Capabilities

### 1. Interactive Debugging

Full-featured interactive debugging with breakpoints, watchpoints, and execution control.

#### Breakpoint Management

```python
from agents.debugger.agent import DebuggingEngine, BreakpointType

engine = DebuggingEngine()
engine.initialize()

# Create software breakpoint
bp_id = engine.create_breakpoint(
    address=0x401000,
    bp_type=BreakpointType.SOFTWARE
)

# Create conditional breakpoint
bp_conditional = engine.create_breakpoint(
    address=0x401200,
    condition="x > 10",
    bp_type=BreakpointType.CONDITIONAL
)

# Create temporary breakpoint (auto-disables after hit)
bp_temp = engine.create_breakpoint(
    address=0x401400,
    temporary=True
)

# Create hardware watchpoint
wp_id = engine.create_watchpoint(
    address=0x600000,
    size=8,
    access_type="rw"
)
```

#### Execution Control

```python
# Step into function calls
event = engine.step_into()
# Returns: DebugEvent.SINGLE_STEP

# Step over function calls
event = engine.step_over()
# Returns: DebugEvent.SINGLE_STEP

# Step out of current function
event = engine.step_out()
# Returns: DebugEvent.SINGLE_STEP

# Continue until next breakpoint
event = engine.continue_execution()
# Returns: DebugEvent.BREAKPOINT when a breakpoint is hit
```

#### State Inspection

```python
# Get register values
registers = engine.info_registers()
# Returns: {'rax': '0x000000000000000a', 'rbx': '0x...', ...}

# Get stack backtrace
frames = engine.backtrace()
for frame in frames:
    print(f"#{frame.frame_index} {frame.function_name} at {frame.file_path}:{frame.line_number}")

# Read memory
data = engine.read_memory(address=0x600000, size=64)

# Disassemble instructions
instructions = engine.disassemble(address=0x401000, count=10)
for instr in instructions:
    print(f"0x{instr['address']:08x}: {instr['mnemonic']} {', '.join(instr['operands'])}")

# Get memory region info
regions = engine.info_memory()
```

### 2. Root Cause Analysis

Systematic investigation to identify the fundamental cause of software defects.

```python
from agents.debugger.agent import RootCauseAnalyzer, RootCauseCategory, CrashInfo, CrashType

analyzer = RootCauseAnalyzer()

# Add evidence
analyzer.add_evidence(
    evidence_type="crash_dump",
    description="Segmentation fault at 0x41414141",
    source="core_dump",
    data={"crash_address": 0x41414141}
)

# Add hypothesis
hyp_id = analyzer.add_hypothesis(
    hypothesis="Buffer overflow in input parser",
    rationale="Crash address contains pattern 0x41 (ASCII 'A')",
    priority=8
)

# Analyze crash pattern
crashes = [
    CrashInfo(crash_type=CrashType.BUFFER_OVERFLOW, crash_address=0x41414141),
    CrashInfo(crash_type=CrashType.BUFFER_OVERFLOW, crash_address=0x41414141),
    CrashInfo(crash_type=CrashType.SEGMENTATION_FAULT, crash_address=0x41414141),
]
candidate = analyzer.analyze_crash_pattern(crashes)
print(f"Root cause: {candidate.description}")
print(f"Confidence: {candidate.confidence:.0%}")
print(f"Suggested fix: {candidate.suggested_fix}")

# Generate report
report = analyzer.generate_report()
```

### 3. Logging Management

Structured logging with correlation tracking, filtering, and multiple output destinations.

```python
from agents.debugger.agent import LoggingManager, LogLevel

logger = LoggingManager()
logger.set_level(LogLevel.DEBUG)

# Add correlation ID for related operations
corr_id = logger.start_correlation()

# Log with context
logger.info("parser", "Starting input parsing", context={"input_size": 1024}, correlation_id=corr_id)
logger.debug("parser", "Token 1: value=42", correlation_id=corr_id)
logger.debug("parser", "Token 2: type=identifier", correlation_id=corr_id)
logger.info("parser", "Parsing complete", context={"tokens": 15}, correlation_id=corr_id)

# End correlation and get all related entries
entries = logger.end_correlation(corr_id)

# Add custom filter
logger.add_filter(lambda entry: "noisy_module" not in entry.source)

# Add custom handler
def my_handler(entry):
    if entry.level == LogLevel.ERROR:
        send_alert(entry.message)
logger.add_handler(my_handler)

# Performance timing
logger.start_timer("api_call")
# ... do work ...
elapsed = logger.end_timer("api_call")

# Get summary
summary = logger.get_summary()
# Returns: {'total_entries': 4, 'entries_by_level': {...}, ...}

# Export as JSON
json_output = logger.export_json()
```

### 4. Profiling

CPU and memory profiling with hotspot detection and call graph analysis.

```python
from agents.debugger.agent import Profiler

profiler = Profiler()

# Start profiling session
session_id = profiler.start_session(sample_interval_ms=10.0)

# Record function samples (typically done automatically via hooks)
profiler.record_sample("process_request", 45.2)
profiler.record_sample("parse_input", 12.3)
profiler.record_sample("validate_data", 8.7)
profiler.record_sample("process_request", 52.1)

# Record caller-callee relationships
profiler.record_call("main", "process_request")
profiler.record_call("process_request", "parse_input")
profiler.record_call("process_request", "validate_data")

# Stop session
result = profiler.stop_session()

# Get top functions
top_funcs = result.get_top_functions(n=5)
for name, time_ms in top_funcs:
    print(f"{name}: {time_ms:.1f}ms")

# Get hotspots
hotspots = profiler.get_hotspots(n=5)

# Get callers and callees
callers = profiler.get_callers("parse_input")
callees = profiler.get_callees("process_request")

# Generate flamegraph data
flamegraph = profiler.generate_flamegraph_data()
```

### 5. Execution Tracing

Multi-level execution tracing with instruction, function, syscall, and memory access tracking.

```python
from agents.debugger.agent import TracingManager

tracer = TracingManager()

# Start tracing with options
tracer.start_tracing({
    "instruction_trace": True,
    "function_trace": True,
    "syscall_trace": True,
    "memory_trace": True,
    "max_entries": 500000,
})

# Record instruction executions
tracer.record_instruction(
    address=0x401000,
    size=4,
    opcode="mov",
    operands=["rax", "rbx"],
    registers_before={"rax": 0, "rbx": 0},
    registers_after={"rax": 42, "rbx": 0},
)

# Record function calls
tracer.record_function_call(
    function_name="process_input",
    arguments={"data": "test", "length": 4},
)

# Record syscalls
tracer.record_syscall(
    name="read",
    arguments=[0, 0x7fff0000, 1024],
    return_value=1024,
)

# Record memory accesses
tracer.record_memory_access(
    address=0x600000,
    size=4,
    access_type="read",
    value=b"\x01\x02\x03\x04",
)

# Record branches
tracer.record_branch(
    address=0x401100,
    taken=True,
    target=0x401200,
)

# Stop and get summary
summary = tracer.stop_tracing()

# Get coverage information
coverage = tracer.get_coverage()

# Get most executed addresses
hot_addrs = tracer.get_hot_addresses(n=10)

# Find execution path
path = tracer.find_execution_path(start_addr=0x401000, end_addr=0x401400)

# Export trace
json_trace = tracer.export_trace(format="json")
csv_trace = tracer.export_trace(format="csv")
```

### 6. Error Resolution

Knowledge-based error resolution with pattern matching and fix suggestions.

```python
from agents.debugger.agent import ErrorResolver, ErrorContext

resolver = ErrorResolver()

# Register known solutions
resolver.register_knowledge(
    error_pattern="NullPointerException",
    solution="Add null check before dereferencing",
    category="null_safety",
    confidence=0.9,
)

resolver.register_knowledge(
    error_pattern="IndexOutOfBoundsException",
    solution="Validate index bounds before array access",
    category="bounds_checking",
    confidence=0.85,
)

# Resolve an error
context = ErrorContext(
    error_type="NullPointerException",
    error_message="Cannot read property 'name' of null",
    stack_trace="at processUser (main.js:42)",
    source_file="main.js",
    source_line=42,
    variables={"user": None},
)

resolution = resolver.resolve_error(context)
print(f"Best suggestion: {resolution['best_suggestion']}")
print(f"Confidence: {resolution['confidence']:.0%}")

# Get suggestion without full context
suggestion = resolver.suggest_fix("TimeoutException", "Connection timed out after 30s")

# Get resolution history
history = resolver.get_resolution_history(error_type="NullPointerException")

# Get knowledge base stats
stats = resolver.get_knowledge_stats()
```

### 7. Post-Mortem Analysis

Analyze crash dumps, core files, and error logs after program termination.

```python
from agents.debugger.agent import PostMortemAnalyzer, CrashInfo, CrashType, DebugFrame

analyzer = PostMortemAnalyzer()

# Analyze a crash dump
crash = CrashInfo(
    crash_type=CrashType.BUFFER_OVERFLOW,
    crash_address=0x41414141,
    crashing_instruction="movaps",
    faulting_register="rsp",
    signal_number=11,
    signal_name="SIGSEGV",
    stack_trace=[
        DebugFrame(function_name="strcpy", file_path="/lib/libc.so", line_number=0),
        DebugFrame(function_name="process_input", file_path="/src/main.c", line_number=42),
        DebugFrame(function_name="main", file_path="/src/main.c", line_number=100),
    ],
    registers_at_crash={"rax": 0x41414141, "rsp": 0x7fff00000000},
    memory_dump=b"\x90" * 20 + b"A" * 100,
)

analysis = analyzer.analyze_dump(crash)
print(f"Crash type: {analysis['crash_type']}")
print(f"Exploitability: {analysis['exploitability']['rating']}")
print(f"Hints: {analysis['root_cause_hints']}")
print(f"Recommendations: {analysis['recommendations']}")

# Correlate multiple dumps
crash2 = CrashInfo(
    crash_type=CrashType.BUFFER_OVERFLOW,
    crash_address=0x41414141,
)
analyzer.analyze_dump(crash2)
correlations = analyzer.correlate_dumps()
```

### 8. Stack Trace Analysis

Parse, analyze, and compare stack traces for patterns and debugging guidance.

```python
from agents.debugger.agent import StackTraceAnalyzer, DebugFrame

analyzer = StackTraceAnalyzer()

# Parse a raw stack trace
trace_text = """#0 0x00007fff12345678 in crash_function () at src/main.c:42
#1 0x00007fff12345600 in process () at src/handler.c:100
#2 0x00007fff12345500 in main () at src/main.c:10"""

frames = analyzer.parse_stack_trace(trace_text)

# Analyze a stack trace
debug_frames = [
    DebugFrame(function_name="crash_function", file_path="src/main.c", line_number=42),
    DebugFrame(function_name="process", file_path="src/handler.c", line_number=100),
    DebugFrame(function_name="main", file_path="src/main.c", line_number=10),
]

analysis = analyzer.analyze_trace(debug_frames)
print(f"Stack depth: {analysis['depth']}")
print(f"Issues: {analysis['issues']}")

# Get debug strategy suggestions
suggestions = analyzer.suggest_debug_strategy(debug_frames)

# Compare two traces
trace_a = [
    DebugFrame(function_name="func_a", file_path="a.c", line_number=1),
    DebugFrame(function_name="func_b", file_path="b.c", line_number=2),
]
trace_b = [
    DebugFrame(function_name="func_a", file_path="a.c", line_number=1),
    DebugFrame(function_name="func_c", file_path="c.c", line_number=3),
]

diff = analyzer.diff_traces(trace_a, trace_b)
print(f"First difference at frame: {diff['first_difference_at']}")
```

### 9. Performance Monitoring

Real-time performance monitoring with metrics, alerting, and trend analysis.

```python
from agents.debugger.agent import PerformanceMonitor

monitor = PerformanceMonitor()

# Set thresholds for alerts
monitor.set_threshold("response_time_ms", warning=100, critical=500)
monitor.set_threshold("memory_usage_mb", warning=512, critical=1024)

# Record metrics
monitor.record_metric("response_time_ms", 45.2)
monitor.record_metric("response_time_ms", 152.3)  # Triggers warning
monitor.record_metric("response_time_ms", 623.1)  # Triggers critical

# Use timers
monitor.start_timer("db_query")
# ... execute query ...
elapsed = monitor.stop_timer("db_query")

# Increment counters
monitor.increment_counter("requests_total")
monitor.increment_counter("errors_total")

# Set gauges
monitor.set_gauge("active_connections", 42)

# Record histogram values
monitor.record_histogram("latency_ms", 23.5)

# Get statistics
stats = monitor.get_metric_stats("response_time_ms")
print(f"Mean: {stats['mean']:.1f}ms")
print(f"P95: {stats['p95']:.1f}ms")
print(f"P99: {stats['p99']:.1f}ms")

# Get alerts
alerts = monitor.get_alerts(severity="critical")

# Get summary
summary = monitor.get_summary()
```

---

## Operational Guidelines

### Debugging Workflow

1. **Session Setup**
   - Initialize the debugging engine
   - Attach to target process or load binary
   - Configure initial breakpoints and watchpoints

2. **Investigation**
   - Run to first breakpoint
   - Examine program state (registers, memory, call stack)
   - Step through suspicious code paths
   - Collect evidence

3. **Analysis**
   - Form hypotheses about the root cause
   - Test hypotheses with targeted breakpoints
   - Use tracing and profiling to gather data
   - Apply root cause analysis

4. **Resolution**
   - Implement the fix
   - Verify with regression tests
   - Document findings
   - Update knowledge base

### Best Practices

- **Always start with the crash/error message** - it contains valuable clues
- **Use conditional breakpoints** for repetitive issues that only occur under specific conditions
- **Correlate log entries** when investigating multi-component systems
- **Record profiling data** before and after changes to measure impact
- **Maintain a knowledge base** of resolved issues for future reference
- **Use post-mortem analysis** when live debugging is not possible

---

## Method Signatures

### DebuggingEngine

```python
class DebuggingEngine:
    def initialize(self) -> None
    def attach_to_process(self, process_id: int) -> bool
    def create_breakpoint(
        self, address: int,
        bp_type: BreakpointType = BreakpointType.SOFTWARE,
        condition: Optional[str] = None,
        temporary: bool = False,
        ignore_count: int = 0,
        commands: Optional[List[str]] = None
    ) -> str
    def create_watchpoint(
        self, address: int,
        size: int = 4,
        access_type: str = "rw"
    ) -> str
    def remove_breakpoint(self, bp_id: str) -> bool
    def remove_watchpoint(self, wp_id: str) -> bool
    def enable_breakpoint(self, bp_id: str) -> bool
    def disable_breakpoint(self, bp_id: str) -> bool
    def step_into(self) -> DebugEvent
    def step_over(self) -> DebugEvent
    def step_out(self) -> DebugEvent
    def step_instruction(self) -> DebugEvent
    def continue_execution(self, max_steps: int = 100000) -> DebugEvent
    def read_memory(self, address: int, size: int) -> bytes
    def write_memory(self, address: int, data: bytes) -> bool
    def disassemble(self, address: int, count: int = 10) -> List[Dict[str, Any]]
    def backtrace(self) -> List[DebugFrame]
    def info_registers(self) -> Dict[str, Any]
    def info_breaks(self) -> Dict[str, Any]
    def info_threads(self) -> Dict[str, Any]
    def info_memory(self) -> List[Dict[str, Any]]
    def register_event_handler(self, event: DebugEvent, handler: Callable) -> None
```

### RootCauseAnalyzer

```python
class RootCauseAnalyzer:
    def add_evidence(
        self, evidence_type: str,
        description: str, source: str,
        data: Optional[Dict[str, Any]] = None
    ) -> None
    def add_hypothesis(
        self, hypothesis: str,
        rationale: str, priority: int = 5
    ) -> str
    def evaluate_hypothesis(
        self, hypothesis_id: str,
        evidence_id: str, supports: bool
    ) -> None
    def analyze_crash_pattern(
        self, crashes: List[CrashInfo]
    ) -> RootCauseCandidate
    def analyze_error_context(
        self, context: ErrorContext
    ) -> RootCauseCandidate
    def get_ranked_candidates(self) -> List[RootCauseCandidate]
    def generate_report(self) -> Dict[str, Any]
```

### LoggingManager

```python
class LoggingManager:
    def __init__(self, name: str = "debugger.logging")
    def set_level(self, level: LogLevel) -> None
    def add_filter(self, filter_fn: Callable[[LogEntry], bool]) -> None
    def add_handler(self, handler: Callable[[LogEntry], None]) -> None
    def start_correlation(self) -> str
    def end_correlation(self, correlation_id: str) -> List[LogEntry]
    def log(
        self, level: LogLevel, source: str, message: str,
        context: Optional[Dict[str, Any]] = None,
        correlation_id: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> LogEntry
    def trace(self, source: str, message: str, **kwargs) -> LogEntry
    def debug(self, source: str, message: str, **kwargs) -> LogEntry
    def info(self, source: str, message: str, **kwargs) -> LogEntry
    def warning(self, source: str, message: str, **kwargs) -> LogEntry
    def error(self, source: str, message: str, **kwargs) -> LogEntry
    def critical(self, source: str, message: str, **kwargs) -> LogEntry
    def start_timer(self, name: str) -> None
    def end_timer(self, name: str) -> float
    def get_entries(self, level=None, source=None, limit=100) -> List[LogEntry]
    def get_summary(self) -> Dict[str, Any]
    def clear(self) -> int
    def export_json(self) -> str
    def get_recent_output(self, count: int = 50) -> List[str]
```

### Profiler

```python
class Profiler:
    def start_session(
        self, session_id: Optional[str] = None,
        sample_interval_ms: float = 10.0
    ) -> str
    def stop_session(self) -> Optional[ProfilingResult]
    def record_sample(self, function_name: str, duration_ms: float) -> None
    def record_call(self, caller: str, callee: str) -> None
    def record_call_time(self, caller: str, callee: str, duration_ms: float) -> None
    def get_hotspots(self, n: int = 10) -> List[Tuple[str, float]]
    def get_function_profile(self, function_name: str) -> Optional[Dict[str, Any]]
    def get_callers(self, function_name: str) -> List[str]
    def get_callees(self, function_name: str) -> List[str]
    def generate_flamegraph_data(self) -> Dict[str, Any]
    def get_summary(self) -> Dict[str, Any]
```

### TracingManager

```python
class TracingManager:
    def start_tracing(self, options: Optional[Dict[str, Any]] = None) -> None
    def stop_tracing(self) -> Dict[str, Any]
    def record_instruction(
        self, address: int, size: int,
        opcode: str, operands: List[str],
        registers_before: Optional[Dict[str, int]] = None,
        registers_after: Optional[Dict[str, int]] = None
    ) -> None
    def record_function_call(
        self, function_name: str,
        arguments: Dict[str, Any],
        return_value: Optional[Any] = None
    ) -> None
    def record_syscall(
        self, name: str,
        arguments: List[Any],
        return_value: Optional[int] = None,
        error: Optional[str] = None
    ) -> None
    def record_memory_access(
        self, address: int, size: int,
        access_type: str, value: Optional[bytes] = None
    ) -> None
    def record_branch(self, address: int, taken: bool, target: Optional[int] = None) -> None
    def get_trace_range(self, start: int = 0, end: Optional[int] = None) -> List[TraceEntry]
    def get_function_trace(self, function_name: str) -> List[Dict[str, Any]]
    def get_syscall_summary(self) -> Dict[str, int]
    def get_coverage(self) -> Dict[str, Any]
    def get_hot_addresses(self, n: int = 10) -> List[Tuple[int, int]]
    def find_execution_path(self, start_addr: int, end_addr: int, max_depth: int = 100) -> List[int]
    def export_trace(self, format: str = "json") -> str
```

### ErrorResolver

```python
class ErrorResolver:
    def register_knowledge(
        self, error_pattern: str,
        solution: str, category: str = "general",
        confidence: float = 0.5
    ) -> None
    def resolve_error(self, context: ErrorContext) -> Dict[str, Any]
    def suggest_fix(self, error_type: str, error_message: str) -> str
    def get_resolution_history(
        self, error_type: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]
    def get_knowledge_stats(self) -> Dict[str, Any]
    def clear_active_errors(self) -> int
```

### PostMortemAnalyzer

```python
class PostMortemAnalyzer:
    def analyze_dump(self, crash_info: CrashInfo) -> Dict[str, Any]
    def build_timeline(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]
    def correlate_dumps(self) -> Dict[str, Any]
    def get_analysis_results(self) -> List[Dict[str, Any]]
    def get_most_common_crash(self) -> Optional[str]
```

### StackTraceAnalyzer

```python
class StackTraceAnalyzer:
    def parse_stack_trace(self, trace_text: str) -> List[Dict[str, Any]]
    def analyze_trace(self, frames: List[DebugFrame]) -> Dict[str, Any]
    def find_common_frames(
        self, traces: List[List[DebugFrame]],
        min_occurrences: int = 2
    ) -> List[Tuple[str, int]]
    def suggest_debug_strategy(self, frames: List[DebugFrame]) -> List[str]
    def diff_traces(
        self, trace_a: List[DebugFrame],
        trace_b: List[DebugFrame]
    ) -> Dict[str, Any]
    def get_recurring_patterns(self, threshold: int = 3) -> List[Tuple[str, int]]
```

### PerformanceMonitor

```python
class PerformanceMonitor:
    def record_metric(self, name: str, value: float, timestamp: Optional[float] = None) -> None
    def increment_counter(self, name: str, amount: int = 1) -> None
    def set_gauge(self, name: str, value: float) -> None
    def record_histogram(self, name: str, value: float) -> None
    def set_threshold(
        self, metric_name: str,
        warning: Optional[float] = None,
        critical: Optional[float] = None
    ) -> None
    def start_timer(self, name: str) -> None
    def stop_timer(self, name: str) -> Optional[float]
    def get_metric_stats(self, name: str) -> Dict[str, Any]
    def get_histogram_stats(self, name: str) -> Dict[str, Any]
    def get_alerts(self, severity: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]
    def get_all_gauges(self) -> Dict[str, float]
    def get_all_counters(self) -> Dict[str, int]
    def get_summary(self) -> Dict[str, Any]
    def clear(self) -> None
```

---

## Data Models

### Breakpoint

| Field | Type | Description |
|-------|------|-------------|
| bp_id | str | Unique identifier |
| address | int | Memory address |
| bp_type | BreakpointType | Type of breakpoint |
| enabled | bool | Whether active |
| hit_count | int | Number of times hit |
| condition | Optional[str] | Conditional expression |
| commands | List[str] | Commands to execute on hit |
| temporary | bool | Auto-disable after first hit |

### DebugFrame

| Field | Type | Description |
|-------|------|-------------|
| function_name | str | Name of function |
| file_path | str | Source file path |
| line_number | int | Line number |
| locals | Dict[str, Any] | Local variables |
| args | Dict[str, Any] | Function arguments |
| instruction_pointer | int | Current IP |
| stack_pointer | int | Current SP |
| frame_index | int | Frame depth index |

### CrashInfo

| Field | Type | Description |
|-------|------|-------------|
| crash_type | CrashType | Type of crash |
| crash_address | int | Address where crash occurred |
| crashing_instruction | str | Instruction that caused crash |
| faulting_register | str | Register involved |
| signal_number | int | Signal number |
| stack_trace | List[DebugFrame] | Call stack at crash |
| exploitability | str | Exploitability rating |

### LogEntry

| Field | Type | Description |
|-------|------|-------------|
| timestamp | datetime | When the entry was created |
| level | LogLevel | Severity level |
| source | str | Component that generated the log |
| message | str | Log message |
| context | Dict[str, Any] | Additional context data |
| correlation_id | Optional[str] | Correlation identifier |
| tags | List[str] | Classification tags |

### ProfilingResult

| Field | Type | Description |
|-------|------|-------------|
| session_id | str | Session identifier |
| function_profiles | Dict[str, Dict] | Per-function profiling data |
| total_samples | int | Total samples collected |
| duration_seconds | float | Session duration |
| hotspots | List[Tuple[str, float]] | Top performance hotspots |
| call_graph | Dict[str, List[str]] | Caller-callee relationships |

---

## Checklists

### Debugging Session Checklist

- [ ] Initialize debugging engine
- [ ] Set up logging with appropriate level
- [ ] Configure breakpoints at suspicious locations
- [ ] Set up watchpoints for memory issues
- [ ] Enable execution tracing
- [ ] Start performance monitoring
- [ ] Document initial hypotheses
- [ ] Record baseline metrics

### Root Cause Analysis Checklist

- [ ] Collect all available evidence (crash dumps, logs, traces)
- [ ] Form initial hypotheses
- [ ] Test each hypothesis systematically
- [ ] Document evidence for/against each hypothesis
- [ ] Identify the most likely root cause
- [ ] Propose a fix
- [ ] Verify the fix resolves the issue
- [ ] Update knowledge base with the solution

### Post-Mortem Analysis Checklist

- [ ] Obtain crash dump or core file
- [ ] Parse crash information
- [ ] Analyze stack trace
- [ ] Examine register state
- [ ] Check memory state
- [ ] Assess exploitability
- [ ] Generate recommendations
- [ ] Document findings

### Performance Profiling Checklist

- [ ] Identify performance-critical paths
- [ ] Set up profiling session
- [ ] Run representative workload
- [ ] Collect sufficient samples
- [ ] Identify hotspots
- [ ] Analyze call graph
- [ ] Compare before/after optimization
- [ ] Document performance improvements

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Breakpoint Not Hit

**Symptoms**: Breakpoint set but never triggered

**Possible Causes**:
- Address mismatch (ASLR, PIE)
- Code path not reached
- Optimized out by compiler

**Solutions**:
```python
# Verify address with disassembly
instructions = engine.disassemble(suspected_address, count=5)

# Use function-based breakpoints instead
bp_id = engine.create_breakpoint(
    address=resolve_function_address("target_function"),
    bp_type=BreakpointType.FUNCTION_ENTRY
)
```

#### 2. Excessive Trace Data

**Symptoms**: Memory usage growing rapidly during tracing

**Solutions**:
```python
# Use filtering
tracer.start_tracing({
    "instruction_trace": False,  # Disable instruction-level tracing
    "function_trace": True,      # Keep function-level tracing
    "max_entries": 100000,       # Limit buffer size
})
```

#### 3. Profiling Overhead Too High

**Symptoms**: Target process significantly slowed

**Solutions**:
```python
# Increase sample interval
profiler.start_session(sample_interval_ms=100.0)  # Instead of 10.0

# Profile only specific functions
profiler.record_sample("critical_function", duration_ms)
```

#### 4. Log Noise

**Symptoms**: Too many log entries to analyze

**Solutions**:
```python
# Set appropriate log level
logger.set_level(LogLevel.WARNING)

# Add source filter
logger.add_filter(lambda entry: entry.source in ["critical_module"])

# Use correlation IDs to group related entries
corr_id = logger.start_correlation()
```

#### 5. Root Cause Analysis Stuck

**Symptoms**: No clear root cause identified after investigation

**Solutions**:
- Gather more evidence with targeted tracing
- Try alternative hypotheses
- Use binary search to narrow down the issue
- Consider environmental factors (timing, load, configuration)

---

## Usage Patterns

### Pattern 1: Crash Investigation

```python
agent = create_debugging_agent()

# Analyze crash dump
analyzer = agent["postmortem_analyzer"]
crash = CrashInfo(
    crash_type=CrashType.SEGMENTATION_FAULT,
    crash_address=0x0,
    signal_name="SIGSEGV",
)
analysis = analyzer.analyze_dump(crash)

# Use root cause analyzer
rca = agent["root_cause_analyzer"]
rca.add_evidence("crash", analysis["crash_type"], "postmortem")
candidate = rca.analyze_crash_pattern([crash])

# Get suggestions
resolver = agent["error_resolver"]
suggestion = resolver.suggest_fix(analysis["crash_type"], "")
```

### Pattern 2: Performance Investigation

```python
agent = create_debugging_agent()

# Start profiling
profiler = agent["profiler"]
profiler.start_session()

# Record samples during execution
profiler.record_sample("hot_function", 45.2)
profiler.record_call("main", "hot_function")

# Analyze results
result = profiler.stop_session()
top_funcs = result.get_top_functions(5)

# Set up monitoring for ongoing performance
monitor = agent["performance_monitor"]
monitor.set_threshold("latency_ms", warning=100, critical=500)
```

### Pattern 3: Memory Issue Investigation

```python
agent = create_debugging_agent()

# Set up memory watchpoints
engine = agent["engine"]
wp_id = engine.create_watchpoint(
    address=0x600000,
    size=8,
    access_type="rw"
)

# Enable memory tracing
tracer = agent["tracing_manager"]
tracer.start_tracing({"memory_trace": True})

# Record memory accesses
tracer.record_memory_access(0x600000, 4, "write", b"\x01\x02\x03\x04")

# Analyze
coverage = tracer.get_coverage()
```

---

*Debugger Agent GROK.md v2.0.0*
