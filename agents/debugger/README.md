# Debugger Agent

A comprehensive software debugging, analysis, and error resolution system with interactive debugging, root cause analysis, logging strategies, profiling, tracing, error resolution, and post-mortem analysis capabilities.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
  - [Basic Usage](#basic-usage)
  - [Interactive Debugging Session](#interactive-debugging-session)
  - [Error Analysis Workflow](#error-analysis-workflow)
  - [Performance Profiling](#performance-profiling)
  - [Execution Tracing](#execution-tracing)
- [Installation](#installation)
  - [From Source](#from-source)
  - [Dependencies](#dependencies)
- [Usage](#usage)
  - [Starting a Debugging Session](#starting-a-debugging-session)
  - [Managing Breakpoints](#managing-breakpoints)
  - [Execution Control](#execution-control)
  - [Logging](#logging)
  - [Profiling](#profiling)
  - [Tracing](#tracing)
  - [Error Resolution](#error-resolution)
  - [Post-Mortem Analysis](#post-mortem-analysis)
- [API Reference](#api-reference)
  - [Enums](#enums)
  - [Data Classes](#data-classes)
  - [DebuggingEngine](#debuggingengine)
  - [RootCauseAnalyzer](#rootcauseanalyzer)
  - [LoggingManager](#loggingmanager)
  - [Profiler](#profiler)
  - [TracingManager](#tracingmanager)
  - [ErrorResolver](#errorresolver)
  - [PostMortemAnalyzer](#postmortemanalyzer)
  - [Factory Function](#factory-function)
- [Configuration](#configuration)
  - [Logging Configuration](#logging-configuration)
  - [Tracing Configuration](#tracing-configuration)
  - [Profiling Configuration](#profiling-configuration)
  - [Knowledge Base Configuration](#knowledge-base-configuration)
- [Best Practices](#best-practices)
  - [Debugging Best Practices](#debugging-best-practices)
  - [Root Cause Analysis Best Practices](#root-cause-analysis-best-practices)
  - [Performance Best Practices](#performance-best-practices)
  - [Logging Best Practices](#logging-best-practices)
- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)
  - [Getting Help](#getting-help)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Debugger Agent provides a complete debugging toolkit for software developers and security researchers. It combines interactive debugging with advanced analysis techniques to help identify, diagnose, and resolve software defects efficiently.

### Key Capabilities

- **Interactive Debugging**: Full-featured debugging engine with breakpoints, watchpoints, and execution control
- **Root Cause Analysis**: Evidence-based investigation to identify fundamental defect origins
- **Logging Management**: Structured logging with correlation tracking and filtering
- **Profiling**: CPU and memory profiling with hotspot detection and call graph analysis
- **Execution Tracing**: Multi-level tracing including instruction, function, syscall, and memory access
- **Error Resolution**: Knowledge-based error resolution with pattern matching and fix suggestions
- **Post-Mortem Analysis**: Crash dump analysis with exploitability assessment

### Architecture

The agent is composed of seven core components that work independently or together:

```
+-------------------+     +-------------------+     +-------------------+
|  DebuggingEngine  |<--->|  RootCauseAnalyzer|<--->|  LoggingManager   |
|  (breakpoints,    |     |  (evidence-based  |     |  (structured      |
|   watchpoints,    |     |   investigation)  |     |   entries,        |
|   execution)      |     |                   |     |   correlation)    |
+-------------------+     +-------------------+     +-------------------+
         |                         |                         |
         v                         v                         v
+-------------------+     +-------------------+     +-------------------+
|  Profiler         |     |  TracingManager   |     |  ErrorResolver    |
|  (sampling,       |     |  (instruction,    |     |  (knowledge base, |
|   hotspots,       |     |   function,       |     |   pattern match,  |
|   call graphs)    |     |   syscall trace)  |     |   fix suggestions)|
+-------------------+     +-------------------+     +-------------------+
                                 |
                                 v
                        +-------------------+
                        | PostMortemAnalyzer|
                        | (crash dumps,     |
                        |  exploitability,  |
                        |  timeline)        |
                        +-------------------+
```

---

## Features

### Debugging Engine

| Feature | Description |
|---------|-------------|
| Breakpoints | Software, hardware, conditional, temporary, function entry/exit |
| Watchpoints | Memory read, write, execute monitoring |
| Execution Control | Step into, step over, step out, continue |
| State Inspection | Registers, memory regions, call stack, threads |
| Memory Operations | Read and write memory at arbitrary addresses |
| Disassembly | Instruction disassembly with operand decoding |

### Root Cause Analysis

| Feature | Description |
|---------|-------------|
| Evidence Collection | Structured evidence gathering with metadata and timestamps |
| Hypothesis Testing | Form, evaluate, and rank hypotheses systematically |
| Pattern Matching | Match crash patterns against known root cause categories |
| Candidate Ranking | Rank root cause candidates by confidence score |
| Report Generation | Generate comprehensive analysis reports |

### Logging System

| Feature | Description |
|---------|-------------|
| Structured Logging | Rich log entries with context, tags, and correlation IDs |
| Correlation Tracking | Group related log entries across components |
| Filtering | Level-based, source-based, and custom filter functions |
| Multiple Handlers | Pluggable output handlers for console, file, network |
| Performance Timers | Built-in timing measurement with ms precision |
| JSON Export | Export log entries as JSON for external analysis |

### Profiling

| Feature | Description |
|---------|-------------|
| Sampling | Configurable sample interval for CPU profiling |
| Call Graph | Caller-callee relationship tracking |
| Hotspot Detection | Identify top performance bottlenecks by time |
| Flamegraph Data | Export hierarchical data for visualization |
| Function Profiles | Detailed per-function time and call count stats |

### Execution Tracing

| Feature | Description |
|---------|-------------|
| Instruction Trace | Every instruction executed with register snapshots |
| Function Trace | Entry/exit with arguments and return values |
| Syscall Trace | System call interception with argument recording |
| Memory Trace | Memory access tracking with value snapshots |
| Branch Tracking | Branch execution counts and taken/not-taken ratios |
| Code Coverage | Unique address and branch coverage analysis |
| Trace Export | Export traces as JSON or CSV for external tools |

---

## Quick Start

### Basic Usage

```python
from agents.debugger.agent import create_debugging_agent

# Create a fully initialized debugging agent suite
agent = create_debugging_agent()

# Access individual components
engine = agent["engine"]
profiler = agent["profiler"]
logger = agent["logging_manager"]
```

### Interactive Debugging Session

```python
from agents.debugger.agent import create_debugging_agent

agent = create_debugging_agent()
engine = agent["engine"]

# Create a breakpoint
bp_id = engine.create_breakpoint(address=0x401000)

# Continue execution until breakpoint
event = engine.continue_execution()

# Inspect state
registers = engine.info_registers()
backtrace = engine.backtrace()

# Step through code
event = engine.step_into()
event = engine.step_over()
event = engine.step_out()
```

### Error Analysis Workflow

```python
from agents.debugger.agent import create_debugging_agent, ErrorContext

agent = create_debugging_agent()
resolver = agent["error_resolver"]

# Register known solutions
resolver.register_knowledge(
    error_pattern="NullPointerException",
    solution="Add null check before dereferencing",
    confidence=0.9,
)

# Resolve an error
context = ErrorContext(
    error_type="NullPointerException",
    error_message="Cannot read property of null",
    stack_trace="at process (main.js:42)",
)
resolution = resolver.resolve_error(context)
print(resolution["best_suggestion"])
```

### Performance Profiling

```python
from agents.debugger.agent import create_debugging_agent

agent = create_debugging_agent()
profiler = agent["profiler"]

# Start profiling session
session_id = profiler.start_session()

# Record function samples and call relationships
profiler.record_call("main", "process_data")
profiler.record_sample("process_data", 45.2)
profiler.record_call("process_data", "parse_input")
profiler.record_sample("parse_input", 12.3)

# Stop and analyze
result = profiler.stop_session()
top = result.get_top_functions(5)
for name, time_ms in top:
    print(f"{name}: {time_ms:.1f}ms")
```

### Execution Tracing

```python
from agents.debugger.agent import create_debugging_agent

agent = create_debugging_agent()
tracer = agent["tracing_manager"]

# Start tracing with specific options
tracer.start_tracing({"function_trace": True, "syscall_trace": True})

# Record events
tracer.record_function_call("main", {"argc": 2})
tracer.record_syscall("open", ["/etc/passwd", 0], return_value=3)
tracer.record_function_call("read", {"fd": 3, "size": 1024})

# Get summary
summary = tracer.stop_tracing()
print(f"Functions traced: {summary['total_functions']}")
print(f"Syscalls: {summary['total_syscalls']}")
```

---

## Installation

### From Source

```bash
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e .
```

### Dependencies

The Debugger Agent has minimal dependencies:

- **Python 3.10+** (required for modern type hints and dataclasses)
- **Standard library only** (no external dependencies required)
- Uses: `logging`, `threading`, `json`, `hashlib`, `dataclasses`, `enum`, `typing`

---

## Usage

### Starting a Debugging Session

```python
from agents.debugger.agent import create_debugging_agent

# Initialize the full agent suite
agent = create_debugging_agent()

# Attach to a process
engine = agent["engine"]
engine.attach_to_process(process_id=12345)

# Or initialize manually for simulation
engine.initialize()
```

### Managing Breakpoints

```python
# Create breakpoints
bp1 = engine.create_breakpoint(0x401000)
bp2 = engine.create_breakpoint(0x401200, condition="x > 10")
bp3 = engine.create_breakpoint(0x401400, temporary=True)

# Manage breakpoints
engine.disable_breakpoint(bp1)
engine.enable_breakpoint(bp1)
engine.remove_breakpoint(bp3)

# List all breakpoints
info = engine.info_breaks()
```

### Execution Control

```python
# Step through code
event = engine.step_into()
event = engine.step_over()
event = engine.step_out()
event = engine.step_instruction()

# Continue execution
event = engine.continue_execution()

# Check event type
if event.value == "breakpoint":
    print("Hit a breakpoint!")
elif event.value == "single_step":
    print("Stepped one instruction")
```

### Logging

```python
from agents.debugger.agent import LogLevel

logger = agent["logging_manager"]
logger.set_level(LogLevel.DEBUG)

# Log messages
logger.info("parser", "Starting parse", context={"input_size": 1024})
logger.error("network", "Connection failed", context={"host": "example.com"})

# Use correlation IDs to track related operations
corr = logger.start_correlation()
logger.info("request", "Request started", correlation_id=corr)
logger.info("request", "Processing", correlation_id=corr)
logger.info("request", "Request complete", correlation_id=corr)
entries = logger.end_correlation(corr)

# Get summary
summary = logger.get_summary()
```

### Profiling

```python
profiler = agent["profiler"]

# Start profiling session
session_id = profiler.start_session()

# Record samples
profiler.record_sample("process_data", 45.2)
profiler.record_call("main", "process_data")

# Stop and analyze
result = profiler.stop_session()
top = result.get_top_functions(5)

# Get flamegraph data
flamegraph = profiler.generate_flamegraph_data()
```

### Tracing

```python
tracer = agent["tracing_manager"]

# Configure and start tracing
tracer.start_tracing({
    "instruction_trace": False,
    "function_trace": True,
    "syscall_trace": True,
    "memory_trace": False,
    "max_entries": 500000,
})

# Record events during execution
tracer.record_function_call("main", {"argc": 2})
tracer.record_syscall("read", [0, 1024], return_value=1024)

# Get coverage information
coverage = tracer.get_coverage()
print(f"Unique addresses: {coverage['unique_addresses']}")

# Export trace data
json_trace = tracer.export_trace("json")
csv_trace = tracer.export_trace("csv")
```

### Error Resolution

```python
from agents.debugger.agent import ErrorContext

resolver = agent["error_resolver"]

# Register known solutions
resolver.register_knowledge("segfault", "Check null pointer", confidence=0.8)
resolver.register_knowledge("timeout", "Optimize slow query", confidence=0.7)

# Resolve an error
context = ErrorContext(
    error_type="SegmentationFault",
    error_message="null pointer dereference",
    stack_trace="at process (main.c:42)",
    source_file="main.c",
    source_line=42,
)
resolution = resolver.resolve_error(context)
print(f"Best suggestion: {resolution['best_suggestion']}")

# Get automatic fix suggestion
fix = resolver.suggest_fix("timeout", "operation timed out after 30s")

# Check knowledge base stats
stats = resolver.get_knowledge_stats()
```

### Post-Mortem Analysis

```python
from agents.debugger.agent import create_debugging_agent, CrashInfo, CrashType, DebugFrame

agent = create_debugging_agent()
analyzer = agent["postmortem_analyzer"]

# Analyze a crash dump
crash = CrashInfo(
    crash_type=CrashType.BUFFER_OVERFLOW,
    crash_address=0x41414141,
    crashing_instruction="movaps",
    faulting_register="rsp",
    stack_trace=[
        DebugFrame("strcpy", "/lib/libc.so", 0),
        DebugFrame("process_input", "/src/main.c", 42),
    ],
)

analysis = analyzer.analyze_dump(crash)
print(f"Crash Type: {analysis['crash_type']}")
print(f"Exploitability: {analysis['exploitability']['rating']}")
print(f"Recommendations: {analysis['recommendations']}")

# Correlate multiple dumps
correlation = analyzer.correlate_dumps()
```

---

## API Reference

### Enums

#### BreakpointType

| Value | Description |
|-------|-------------|
| `SOFTWARE` | Software breakpoint (INT3 trap) |
| `HARDWARE` | Hardware debug register breakpoint |
| `CONDITIONAL` | Breakpoint with condition expression |
| `TEMPORARY` | One-shot breakpoint that disables after first hit |
| `FUNCTION_ENTRY` | Breakpoint at function entry point |
| `EXCEPTION` | Breakpoint on specific exception type |

#### DebugEvent

| Value | Description |
|-------|-------------|
| `BREAKPOINT` | Breakpoint was hit |
| `WATCHPOINT` | Watchpoint was triggered |
| `SINGLE_STEP` | Single instruction step completed |
| `PROGRAM_EXIT` | Program terminated |
| `EXCEPTION` | Exception occurred |
| `THREAD_CREATED` | New thread created |
| `THREAD_EXITED` | Thread terminated |

#### CrashType

| Value | Description |
|-------|-------------|
| `SEGMENTATION_FAULT` | Invalid memory access |
| `STACK_OVERFLOW` | Stack exhaustion |
| `HEAP_CORRUPTION` | Heap metadata corruption |
| `USE_AFTER_FREE` | Accessing freed memory |
| `DOUBLE_FREE` | Freeing already freed memory |
| `BUFFER_OVERFLOW` | Buffer write beyond bounds |
| `INTEGER_OVERFLOW` | Arithmetic overflow |
| `DEADLOCK` | Circular lock dependency |
| `OUT_OF_MEMORY` | Memory allocation failure |
| `UNKNOWN` | Unclassified crash |

#### RootCauseCategory

| Value | Description |
|-------|-------------|
| `LOGIC_ERROR` | Incorrect program logic |
| `RACE_CONDITION` | Concurrency timing issue |
| `MEMORY_SAFETY` | Memory corruption or access violation |
| `RESOURCE_LEAK` | Unreleased resource |
| `INPUT_VALIDATION` | Missing or incorrect input validation |
| `ERROR_HANDLING` | Improper error handling |
| `CONFIGURATION` | Configuration or environment issue |
| `DEPENDENCY` | External dependency problem |
| `PERFORMANCE` | Performance-related defect |
| `SECURITY` | Security vulnerability |
| `UNKNOWN` | Unclassified root cause |

### Data Classes

#### Breakpoint

```python
@dataclass
class Breakpoint:
    bp_id: str                          # Unique breakpoint identifier
    address: int                        # Memory address
    bp_type: BreakpointType             # Breakpoint type
    enabled: bool                       # Whether breakpoint is active
    hit_count: int                      # Number of times hit
    condition: Optional[str]            # Condition expression
    temporary: bool                     # One-shot breakpoint
    ignore_count: int                   # Hits to ignore before stopping
    hit_timestamps: List[float]         # Timestamps of each hit
    created_at: float                   # Creation timestamp
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `increment_hit()` | `None` | Record a breakpoint hit and update state |
| `should_ignore()` | `bool` | Check if this hit should be skipped |
| `get_hit_rate()` | `float` | Calculate hits per second since creation |

#### DebugFrame

```python
@dataclass
class DebugFrame:
    function_name: str                  # Function name
    file_path: str                      # Source file path
    line_number: int                    # Source line number
    locals: Dict[str, Any]              # Local variables
    args: Dict[str, Any]               # Function arguments
    instruction_pointer: int            # Instruction pointer value
    stack_pointer: int                  # Stack pointer value
    frame_index: int                    # Frame depth index
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `get_variable(name)` | `Any` | Retrieve variable from locals or args |
| `set_variable(name, value, is_local)` | `None` | Set a variable value |

#### Watchpoint

```python
@dataclass
class Watchpoint:
    wp_id: str                          # Unique watchpoint identifier
    address: int                        # Memory address to watch
    size: int                           # Number of bytes to watch
    access_type: str                    # "r", "w", or "rw"
    enabled: bool                       # Whether watchpoint is active
    hit_count: int                      # Number of accesses detected
    last_access_value: Optional[bytes]  # Value at last access
```

#### CrashInfo

```python
@dataclass
class CrashInfo:
    crash_type: CrashType               # Type of crash
    crash_address: int                  # Address where crash occurred
    crashing_instruction: str           # Instruction that caused crash
    faulting_register: str              # Register that caused fault
    signal_number: int                  # Signal number
    signal_name: str                    # Signal name
    stack_trace: List[DebugFrame]       # Stack trace at crash
    registers_at_crash: Dict[str, int]  # Register state at crash
    memory_dump: Optional[bytes]        # Memory dump around crash
    timestamp: float                    # Crash timestamp
    thread_id: int                      # Thread that crashed
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `get_crash_hash()` | `str` | Generate unique hash for deduplication |

#### ProfilingResult

```python
@dataclass
class ProfilingResult:
    session_id: str                     # Profiling session identifier
    function_profiles: Dict[str, Dict]  # Per-function profile data
    total_samples: int                  # Total samples collected
    sample_interval_ms: float           # Sample interval in milliseconds
    duration_seconds: float             # Total profiling duration
    hotspots: List[Tuple[str, float]]   # Top functions by time percentage
    call_graph: Dict[str, List[str]]    # Caller-callee relationships
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `get_top_functions(n)` | `List[Tuple[str, float]]` | Get top N functions by total time |

#### LogEntry

```python
@dataclass
class LogEntry:
    timestamp: datetime                 # UTC timestamp
    level: LogLevel                     # Log level
    source: str                         # Source component name
    message: str                        # Log message
    context: Dict[str, Any]            # Additional context data
    correlation_id: Optional[str]       # Correlation ID for grouping
    duration_ms: Optional[float]        # Duration in milliseconds
    tags: List[str]                     # Categorization tags
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `to_dict()` | `Dict[str, Any]` | Convert to dictionary for serialization |

#### ErrorContext

```python
@dataclass
class ErrorContext:
    error_type: str                     # Error class name
    error_message: str                  # Error description
    stack_trace: str                    # Stack trace text
    timestamp: float                    # Error timestamp
    source_file: Optional[str]         # Source file where error occurred
    source_line: Optional[int]         # Line number where error occurred
    variables: Dict[str, Any]          # Variable values at error time
```

#### RootCauseCandidate

```python
@dataclass
class RootCauseCandidate:
    category: RootCauseCategory         # Root cause category
    confidence: float                   # Confidence score (0.0-1.0)
    description: str                    # Human-readable description
    evidence: List[str]                 # Supporting evidence
    suggested_fix: Optional[str]       # Recommended fix
    severity: str                       # "low", "medium", "high"
```

**Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `is_high_confidence(threshold)` | `bool` | Check if confidence meets threshold |

### DebuggingEngine

Interactive debugging engine with breakpoints, watchpoints, and execution control.

#### Constructor

```python
DebuggingEngine()
```

Initializes empty engine with no state. Call `initialize()` or `attach_to_process()` to set up.

#### Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `initialize()` | - | `None` | Initialize with x86-64 register layout and default memory regions |
| `attach_to_process(pid)` | `process_id: int` | `bool` | Attach to a running process by PID |
| `create_breakpoint(addr, type, cond, temp, ignore)` | `address: int, BreakpointType, str, bool, int` | `str` | Create breakpoint, returns ID |
| `create_watchpoint(addr, size, access)` | `address: int, int, str` | `str` | Create watchpoint, returns ID |
| `remove_breakpoint(bp_id)` | `bp_id: str` | `bool` | Remove breakpoint by ID |
| `remove_watchpoint(wp_id)` | `wp_id: str` | `bool` | Remove watchpoint by ID |
| `enable_breakpoint(bp_id)` | `bp_id: str` | `bool` | Enable a disabled breakpoint |
| `disable_breakpoint(bp_id)` | `bp_id: str` | `bool` | Disable an active breakpoint |
| `step_into()` | - | `DebugEvent` | Step into function call |
| `step_over()` | - | `DebugEvent` | Step over function call |
| `step_out()` | - | `DebugEvent` | Step out of current function |
| `step_instruction()` | - | `DebugEvent` | Single instruction step |
| `continue_execution(max_steps)` | `int` | `DebugEvent` | Continue until breakpoint or exit |
| `read_memory(addr, size)` | `address: int, int` | `bytes` | Read memory at address |
| `write_memory(addr, data)` | `address: int, bytes` | `bool` | Write data to memory |
| `disassemble(addr, count)` | `address: int, int` | `List[Dict]` | Disassemble N instructions |
| `backtrace()` | - | `List[DebugFrame]` | Get call stack backtrace |
| `info_registers()` | - | `Dict[str, str]` | Get all register values |
| `info_breaks()` | - | `Dict[str, Any]` | Get breakpoint/watchpoint summary |
| `info_memory()` | - | `List[Dict]` | Get memory region info |

### RootCauseAnalyzer

Evidence-based root cause analysis engine.

#### Constructor

```python
RootCauseAnalyzer()
```

Initializes analyzer with empty evidence, hypotheses, and pattern database.

#### Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `add_evidence(type, desc, source)` | `str, str, str` | `None` | Add a piece of evidence |
| `add_hypothesis(hyp, rationale, priority)` | `str, str, int` | `str` | Add hypothesis, returns ID |
| `evaluate_hypothesis(hyp_id, ev_id, supports)` | `str, str, bool` | `None` | Evaluate evidence against hypothesis |
| `analyze_crash_pattern(crashes)` | `List[CrashInfo]` | `RootCauseCandidate` | Analyze recurring crash pattern |
| `analyze_error_context(context)` | `ErrorContext` | `RootCauseCandidate` | Analyze error for root cause |
| `get_ranked_candidates()` | - | `List[RootCauseCandidate]` | Get candidates sorted by confidence |
| `generate_report()` | - | `Dict[str, Any]` | Generate comprehensive report |

### LoggingManager

Structured logging with correlation tracking.

#### Constructor

```python
LoggingManager(name: str = "debugger.logging")
```

#### Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `set_level(level)` | `LogLevel` | `None` | Set minimum log level |
| `add_filter(fn)` | `Callable[[LogEntry], bool]` | `None` | Add custom filter |
| `add_handler(handler)` | `Callable[[LogEntry], None]` | `None` | Add output handler |
| `start_correlation()` | - | `str` | Start correlation ID |
| `end_correlation(corr_id)` | `str` | `List[LogEntry]` | End correlation, return entries |
| `log(level, source, msg, ctx, corr)` | `LogLevel, str, str, Dict, str` | `LogEntry` | Log a message |
| `trace(source, msg, **kw)` | `str, str` | `LogEntry` | Log at TRACE level |
| `debug(source, msg, **kw)` | `str, str` | `LogEntry` | Log at DEBUG level |
| `info(source, msg, **kw)` | `str, str` | `LogEntry` | Log at INFO level |
| `warning(source, msg, **kw)` | `str, str` | `LogEntry` | Log at WARNING level |
| `error(source, msg, **kw)` | `str, str` | `LogEntry` | Log at ERROR level |
| `critical(source, msg, **kw)` | `str, str` | `LogEntry` | Log at CRITICAL level |
| `start_timer(name)` | `str` | `None` | Start a named timer |
| `end_timer(name)` | `str` | `float` | End timer, return elapsed ms |
| `get_entries(level, source, limit)` | `LogLevel, str, int` | `List[LogEntry]` | Get filtered entries |
| `get_summary()` | - | `Dict` | Get log statistics |
| `clear()` | - | `int` | Clear all entries |
| `export_json()` | - | `str` | Export as JSON |

### Profiler

CPU and memory profiling engine.

#### Constructor

```python
Profiler()
```

#### Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `start_session(id, interval)` | `str, float` | `str` | Start profiling session |
| `stop_session()` | - | `ProfilingResult` | Stop and return results |
| `record_sample(func, duration)` | `str, float` | `None` | Record function execution sample |
| `record_call(caller, callee)` | `str, str` | `None` | Record caller-callee relationship |
| `record_call_time(caller, callee, dur)` | `str, str, float` | `None` | Record timed call relationship |
| `get_hotspots(n)` | `int` | `List[Tuple]` | Get top N hotspots |
| `get_function_profile(name)` | `str` | `Optional[Dict]` | Get function profile data |
| `get_callers(name)` | `str` | `List[str]` | Get callers of a function |
| `get_callees(name)` | `str` | `List[str]` | Get callees of a function |
| `generate_flamegraph_data()` | - | `Dict` | Generate hierarchical flamegraph data |
| `get_summary()` | - | `Dict` | Get profiling summary |

### TracingManager

Multi-level execution tracing.

#### Constructor

```python
TracingManager()
```

#### Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `start_tracing(options)` | `Dict` | `None` | Start tracing with options |
| `stop_tracing()` | - | `Dict` | Stop and return summary |
| `record_instruction(addr, size, op, ops, reg_b, reg_a)` | Various | `None` | Record instruction execution |
| `record_function_call(name, args, ret)` | `str, Dict, Any` | `None` | Record function call/return |
| `record_syscall(name, args, ret, err)` | `str, List, int, str` | `None` | Record system call |
| `record_memory_access(addr, size, type, val)` | `int, int, str, bytes` | `None` | Record memory access |
| `record_branch(addr, taken, target)` | `int, bool, int` | `None` | Record branch execution |
| `get_trace_range(start, end)` | `int, int` | `List[TraceEntry]` | Get trace slice |
| `get_function_trace(name)` | `str` | `List[Dict]` | Get function-specific trace |
| `get_syscall_summary()` | - | `Dict[str, int]` | Get syscall counts |
| `get_coverage()` | - | `Dict` | Get code coverage stats |
| `get_hot_addresses(n)` | `int` | `List[Tuple]` | Get most executed addresses |
| `find_execution_path(start, end, depth)` | `int, int, int` | `List[int]` | Find path between addresses |
| `export_trace(format)` | `str` | `str` | Export trace as JSON or CSV |

### ErrorResolver

Knowledge-based error resolution.

#### Constructor

```python
ErrorResolver()
```

Initializes with built-in fix templates for common error categories.

#### Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `register_knowledge(pattern, solution, cat, conf)` | `str, str, str, float` | `None` | Register error-solution pair |
| `resolve_error(context)` | `ErrorContext` | `Dict` | Find best solution for error |
| `suggest_fix(type, msg)` | `str, str` | `str` | Get quick fix suggestion |
| `get_history(type, limit)` | `str, int` | `List[Dict]` | Get resolution history |
| `get_knowledge_stats()` | - | `Dict` | Get knowledge base statistics |
| `clear_active_errors()` | - | `int` | Clear tracked active errors |

### PostMortemAnalyzer

Crash dump and post-mortem analysis.

#### Constructor

```python
PostMortemAnalyzer()
```

#### Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `analyze_dump(crash_info)` | `CrashInfo` | `Dict` | Full crash dump analysis |
| `build_timeline(events)` | `List[Dict]` | `List[Dict]` | Build chronological timeline |
| `correlate_dumps()` | - | `Dict` | Find correlations between dumps |
| `get_analysis_results()` | - | `List[Dict]` | Get all analysis results |
| `get_most_common_crash()` | - | `Optional[str]` | Get most frequent crash type |

**Internal Methods:**

| Method | Description |
|--------|-------------|
| `_assess_exploitability(crash)` | Score crash exploitability (0-100) |
| `_generate_hints(crash)` | Generate root cause hints from crash type |
| `_analyze_memory(crash)` | Analyze memory dump for patterns |
| `_generate_recommendations(crash)` | Generate actionable fix recommendations |

### Factory Function

#### create_debugging_agent()

```python
def create_debugging_agent() -> Dict[str, Any]:
```

Creates a fully initialized debugging agent suite with all components wired together and pre-loaded with common error solutions.

**Returns:** Dictionary containing:
- `engine` — `DebuggingEngine` instance (initialized)
- `root_cause_analyzer` — `RootCauseAnalyzer` instance
- `logging_manager` — `LoggingManager` instance
- `profiler` — `Profiler` instance
- `tracing_manager` — `TracingManager` instance
- `error_resolver` — `ErrorResolver` instance (with pre-loaded knowledge)
- `postmortem_analyzer` — `PostMortemAnalyzer` instance

---

## Configuration

### Logging Configuration

```python
from agents.debugger.agent import LoggingManager, LogLevel

logger = LoggingManager()
logger.set_level(LogLevel.WARNING)  # Only warnings and above

# Add custom filter
logger.add_filter(lambda e: "noise" not in e.source)

# Add custom handler
def my_handler(entry):
    with open("debug.log", "a") as f:
        f.write(f"{entry.timestamp} {entry.message}\n")
logger.add_handler(my_handler)
```

### Tracing Configuration

```python
from agents.debugger.agent import TracingManager

tracer = TracingManager()
tracer.start_tracing({
    "instruction_trace": False,    # Disable for performance
    "function_trace": True,        # Keep function tracing
    "syscall_trace": True,         # Keep syscall tracing
    "memory_trace": False,         # Disable memory tracing
    "max_entries": 500000,         # Limit buffer size
})
```

### Profiling Configuration

```python
from agents.debugger.agent import Profiler

profiler = Profiler()
profiler.start_session(
    session_id="my_profile",       # Custom session ID
    sample_interval_ms=50.0,       # Sample every 50ms
)
```

### Knowledge Base Configuration

```python
from agents.debugger.agent import ErrorResolver

resolver = ErrorResolver()

# Register domain-specific solutions
resolver.register_knowledge(
    error_pattern="ConnectionTimeout",
    solution="Increase timeout and add retry with exponential backoff",
    category="networking",
    confidence=0.85,
)

# Check stats
stats = resolver.get_knowledge_stats()
print(f"Patterns: {stats['patterns']}, Solutions: {stats['total_solutions']}")
```

---

## Best Practices

### Debugging Best Practices

1. **Start with reproduction** — Ensure you can reliably reproduce the issue before debugging
2. **Use conditional breakpoints** for issues that occur under specific conditions
3. **Enable logging early** — Capture context before the issue occurs
4. **Minimize assumptions** — Let the data guide your investigation
5. **Document findings** — Record what you learned for future reference
6. **Use temporary breakpoints** for one-shot verification without cluttering state

### Root Cause Analysis Best Practices

1. **Gather evidence first** — Don't jump to conclusions; collect all available data
2. **Form multiple hypotheses** — Consider alternatives before committing to one
3. **Test systematically** — Change one variable at a time
4. **Verify the fix** — Ensure the root cause is addressed, not just symptoms
5. **Update the knowledge base** — Help future debugging efforts with your findings
6. **Use crash pattern analysis** — Multiple crashes of the same type indicate systematic issues

### Performance Best Practices

1. **Profile before optimizing** — Measure first, optimize second
2. **Use representative workloads** — Test with real-world scenarios
3. **Compare before and after** — Quantify improvements
4. **Watch for regressions** — Ensure optimizations don't break functionality
5. **Set up monitoring** — Track performance metrics over time
6. **Use appropriate sample intervals** — Too frequent wastes resources, too sparse misses hotspots

### Logging Best Practices

1. **Use appropriate levels** — Don't over-log; each level should mean something
2. **Include context** — Log relevant metadata (input sizes, IDs, durations)
3. **Use correlation IDs** — Track requests across components
4. **Filter noise** — Remove irrelevant entries before they clutter output
5. **Rotate logs** — Prevent unbounded memory growth with entry limits
6. **Export for analysis** — Use JSON export for external analysis tools

---

## Troubleshooting

### Common Issues

#### Breakpoint Not Hit

- Verify the address is correct (check for ASLR/PIE randomization)
- Ensure the code path is actually executed
- Try using function entry breakpoints instead of address-based ones
- Check if the breakpoint is enabled

#### High Memory Usage

- Reduce `max_entries` in tracing configuration
- Use filtering to reduce log volume
- Call `clear()` on logging manager and performance monitor periodically
- Limit profiling session duration

#### Slow Profiling

- Increase `sample_interval_ms` to reduce overhead
- Profile only specific functions using function-level tracing
- Disable instruction-level tracing when not needed
- Use call graph recording sparingly

#### Too Much Log Noise

- Set appropriate log level (WARNING or ERROR for production)
- Add source-based filters to focus on relevant components
- Use correlation IDs to trace specific operations
- Use the `clear()` method to reset log buffer

#### Root Cause Analysis Stuck

- Gather more evidence with targeted tracing
- Try alternative hypotheses
- Use binary search to narrow down the issue
- Add new pattern matches to the pattern database

#### Post-Mortem Analysis Incomplete

- Ensure core dumps are enabled before crash
- Include memory dumps in CrashInfo for better analysis
- Provide stack trace for hint generation
- Analyze multiple dumps for correlation patterns

### Getting Help

1. Check the [API Reference](#api-reference) for method documentation
2. Review the [Quick Start](#quick-start) examples for common patterns
3. Consult the [Configuration](#configuration) section for tuning options
4. Review the [Best Practices](#best-practices) for guidance

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Setup

```bash
# Clone the repository
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills

# Install in development mode
pip install -e .

# Run tests
python -m pytest agents/debugger/tests/
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all public APIs
- Write docstrings for all classes and methods
- Keep methods focused and under 50 lines
- Use meaningful variable and function names

### Adding New Features

- Add corresponding enums for new categories
- Use dataclasses for structured data
- Include logging for all significant operations
- Add type hints for all parameters and return values
- Write tests for new functionality

---

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

*Debugger Agent v2.0.0*
