---
name: "Crash Analysis"
version: "2.0.0"
description: "Comprehensive crash analysis toolkit with core dump analysis, stack trace processing, symbolication, crash clustering, and root cause identification for production application debugging"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["debugger", "crash-analysis", "core-dump", "stack-trace", "symbolication", "root-cause"]
category: "debugger"
personality: "crash-analyst"
use_cases: ["core dump analysis", "stack trace processing", "crash clustering", "root cause identification", "symbolication"]
---

# Crash Analysis

> Production-grade crash analysis framework providing core dump analysis, stack trace processing, symbolication, crash clustering, and automated root cause identification for diagnosing application crashes in production.

## Overview

The Crash Analysis module provides a complete toolkit for analyzing application crashes at scale. It implements core dump parsing and analysis, stack trace processing with symbolication, crash grouping and clustering, root cause identification, regression detection, and automated remediation suggestion. Every analysis produces actionable reports with reproduction steps and fix recommendations.

## Core Capabilities

### 1. Core Dump Analysis
- Core dump file parsing (ELF, Mach-O, minidump)
- Register state extraction
- Stack unwinding
- Memory state inspection
- Thread analysis

### 2. Stack Trace Processing
- Multi-frame stack trace parsing
- Symbolication with debug symbols
- Inlined function resolution
- Source location mapping
- Cross-platform stack traces

### 3. Crash Clustering
- Similar crash grouping
- Frequency analysis
- Impact assessment
- Trend detection
- Priority scoring

### 4. Root Cause Analysis
- Exception type classification
- Memory error detection (null pointer, buffer overflow, use-after-free)
- Race condition identification
- Resource exhaustion detection
- Dependency failure analysis

### 5. Regression Detection
- Crash rate monitoring
- New crash detection
- Regression correlation
- Deployment impact analysis

### 6. Automated Remediation
- Fix suggestion generation
- Similar issue lookup
- Patch recommendation
- Workaround identification

## Usage Examples

### Core Dump Analysis

```python
from crash_analysis import CoreDumpAnalyzer

analyzer = CoreDumpAnalyzer()

# Analyze a core dump
analysis = analyzer.analyze("/var/crash/app.core")
print(f"Signal: {analysis.signal}")
print(f"Fault address: 0x{analysis.fault_address:X}")
print(f"Thread count: {analysis.thread_count}")
print(f"Crashed in: {analysis.crashed_function}")

print("\nStack trace:")
for frame in analysis.stack_trace[:10]:
    print(f"  {frame.function} ({frame.file}:{frame.line})")
```

### Stack Trace Processing

```python
from crash_analysis import StackTraceProcessor

processor = StackTraceProcessor(symbol_path="/symbols")

# Process a stack trace
processed = processor.process("""
Signal: SIGSEGV (Segmentation fault)
Thread 0 (crashed):
  #0  0x00007f8b2c001234 in process_data (data.c:42)
  #1  0x00007f8b2c005678 in handle_request (server.c:156)
  #2  0x00007f8b2c009abc in worker_thread (worker.c:89)
  #3  0x00007f8b2c012345 in start_thread (pthread.c:123)
""")

print(f"Exception: {processed.exception_type}")
print(f"Function: {processed.top_frame.function}")
print(f"Source: {processed.top_frame.file}:{processed.top_frame.line}")
print(f"Root cause: {processed.root_cause}")
```

### Crash Clustering

```python
from crash_analysis import CrashClusterer

clusterer = CrashClusterer()

# Cluster crashes
clusters = clusterer.cluster(crash_reports)
print(f"Total crashes: {sum(c.count for c in clusters)}")
print(f"Unique clusters: {len(clusters)}")

for cluster in clusters[:5]:
    print(f"\n  Cluster: {cluster.signature}")
    print(f"  Count: {cluster.count}")
    print(f"  Impact: {cluster.affected_users} users")
    print(f"  First seen: {cluster.first_seen}")
    print(f"  Top frame: {cluster.top_frame.function}")
```

### Root Cause Analysis

```python
from crash_analysis import RootCauseAnalyzer

analyzer = RootCauseAnalyzer()

# Analyze crash root cause
result = analyzer.analyze(analysis)
print(f"Root cause category: {result.category}")
print(f"Confidence: {result.confidence:.1%}")
print(f"Description: {result.description}")

print("Evidence:")
for evidence in result.evidence:
    print(f"  - {evidence}")

print("Recommendations:")
for rec in result.recommendations:
    print(f"  - {rec}")
```

## Best Practices

### Core Dump Analysis
- Collect core dumps with debug symbols for accurate analysis
- Analyze core dumps promptly — system state may change
- Preserve core dumps with metadata (build version, environment)
- Use automated collection to ensure consistency

### Stack Trace Processing
- Use source maps or debug symbols for symbolication
- Include relevant context (variables, registers) in analysis
- Process stack traces in bulk for pattern detection
- Handle optimized code (inlining, tail calls) correctly

### Crash Clustering
- Use crash signatures for grouping (function + line + type)
- Consider both stack trace and error message similarity
- Track cluster trends over time
- Prioritize by impact (affected users, frequency)

### Root Cause Analysis
- Combine automated analysis with manual review
- Look for common patterns (null deref, buffer overflow, etc.)
- Consider environmental factors (memory pressure, disk space)
- Document findings for future reference

## Related Modules

- **memory-profiling**: Memory-related crash analysis
- **dynamic-analysis**: Runtime behavior during crashes
- **reverse-engineering**: Binary crash analysis
- **network-debugging**: Network-related crash analysis

---

## Advanced Configuration

### Advanced Core Dump Analysis

```python
from crash_analysis import CoreDumpAnalyzer, AnalysisConfig

analyzer = CoreDumpAnalyzer(
    config=AnalysisConfig(
        symbol_path="/symbols",
        source_path="/source",
        extract_all_threads=True,
        analyze_memory=True,
        analyze_handles=True,
        analyze_network=True,
        generate_report=True,
    ),
)

# Comprehensive core dump analysis
analysis = analyzer.analyze_comprehensive("/var/crash/app.core")
print(f"Signal: {analysis.signal}")
print(f"Fault address: 0x{analysis.fault_address:X}")
print(f"Thread count: {analysis.thread_count}")
print(f"Crashed in: {analysis.crashed_function}")

print("\nStack trace:")
for frame in analysis.stack_trace[:15]:
    print(f"  {frame.function} ({frame.file}:{frame.line})")
    if frame.variables:
        print(f"    Variables:")
        for var in frame.variables:
            print(f"      {var.name}: {var.value}")

print("\nMemory state:")
print(f"  Heap size: {analysis.memory.heap_size_mb:.1f} MB")
print(f"  Free memory: {analysis.memory.free_memory_mb:.1f} MB")
print(f"  Memory map entries: {analysis.memory.map_entries}")

print("\nOpen handles:")
for handle in analysis.handles[:10]:
    print(f"  {handle.type}: {handle.name}")
```

### Advanced Stack Trace Processing

```python
from crash_analysis import StackTraceProcessor, ProcessingConfig

processor = StackTraceProcessor(
    config=ProcessingConfig(
        symbol_path="/symbols",
        source_path="/source",
        inline_functions=True,
        optimize_frames=True,
        group_similar=True,
        max_frames=100,
    ),
)

# Process multiple stack traces
traces = processor.process_batch(crash_reports)

# Cluster similar crashes
clusters = processor.cluster_traces(
    traces,
    similarity_threshold=0.8,
    min_cluster_size=3,
)

print(f"Total crashes: {len(traces)}")
print(f"Unique clusters: {len(clusters)}")

for cluster in clusters[:5]:
    print(f"\n  Cluster: {cluster.signature}")
    print(f"  Count: {cluster.count}")
    print(f"  Top frame: {cluster.top_frame.function}")
    print(f"  Root cause: {cluster.root_cause}")
```

### Advanced Root Cause Analysis

```python
from crash_analysis import RootCauseAnalyzer, AnalysisConfig

analyzer = RootCauseAnalyzer(
    config=AnalysisConfig(
        use_machine_learning=True,
        check_common_patterns=True,
        analyze_environment=True,
        suggest_fixes=True,
        similar_issue_lookup=True,
    ),
)

# Comprehensive root cause analysis
result = analyzer.analyze_comprehensive(analysis)
print(f"Root cause: {result.root_cause}")
print(f"Category: {result.category}")
print(f"Confidence: {result.confidence:.1%}")

print("\nEvidence:")
for evidence in result.evidence:
    print(f"  - {evidence.type}: {evidence.description}")
    print(f"    Source: {evidence.source}")

print("\nRecommendations:")
for rec in result.recommendations:
    print(f"  [{rec.priority}] {rec.description}")
    print(f"    Fix: {rec.fix_suggestion}")
    print(f"    Similar issues: {rec.similar_issues_count}")
```

### Advanced Crash Clustering

```python
from crash_analysis import CrashClusterer, ClusteringConfig

clusterer = CrashClusterer(
    config=ClusteringConfig(
        algorithm="hierarchical",
        similarity_metric="stack_trace",
        min_cluster_size=3,
        max_clusters=100,
        include_metadata=True,
    ),
)

# Cluster crashes from multiple sources
clusters = clusterer.cluster_comprehensive(
    crashes=crash_reports,
    group_by=["version", "platform", "environment"],
)

print(f"Total crashes: {sum(c.count for c in clusters)}")
print(f"Unique clusters: {len(clusters)}")

for cluster in clusters[:10]:
    print(f"\n  Cluster: {cluster.signature}")
    print(f"  Count: {cluster.count}")
    print(f"  Impact: {cluster.affected_users} users")
    print(f"  First seen: {cluster.first_seen}")
    print(f"  Last seen: {cluster.last_seen}")
    print(f"  Trend: {cluster.trend}")
    print(f"  Top frame: {cluster.top_frame.function}")
    print(f"  Root cause: {cluster.root_cause}")
```

## Architecture Patterns

### Crash Analysis Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                Crash Analysis Architecture                  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Collection Layer                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Core Dump  │  │  Crash      │  │  Minidump   │ │   │
│  │  │  Collection │  │  Reports    │  │  Collection  │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Processing Layer                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Symboli-   │  │  Stack      │  │  Memory     │ │   │
│  │  │  cation     │  │  Unwinding  │  │  Analysis   │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Analysis Layer                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Root Cause │  │  Clustering │  │  Regression │ │   │
│  │  │  Analysis   │  │             │  │  Detection  │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Reporting Layer                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Crash      │  │  Regression │  │  Fix        │ │   │
│  │  │  Dashboards │  │  Reports    │  │  Suggestions│ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Crash Analysis Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                  Crash Analysis Pipeline                    │
├─────────────────────────────────────────────────────────────┤
│  1. Crash Collection                                        │
│     └─► Collect core dumps, minidumps, crash reports        │
│  2. Symbolication                                           │
│     └─► Resolve addresses to function names                 │
│  3. Stack Unwinding                                         │
│     └─► Reconstruct call stack                              │
│  4. Memory Analysis                                         │
│     └─► Analyze memory state at crash                       │
│  5. Root Cause Analysis                                     │
│     └─► Identify crash cause                                │
│  6. Clustering                                              │
│     └─► Group similar crashes                               │
│  7. Regression Detection                                    │
│     └─► Detect new crash types                              │
│  8. Reporting                                               │
│     └─► Generate actionable reports                         │
└─────────────────────────────────────────────────────────────┘
```

## Integration Guide

### Application Integration

```python
# Integration with CI/CD
from crash_analysis import CrashAnalyzer, CrashReporter

analyzer = CrashAnalyzer()
reporter = CrashReporter()

def post_deployment_check():
    # Monitor for new crashes
    new_crashes = reporter.get_new_crashes(since_deployment=True)
    
    if new_crashes:
        # Analyze crashes
        analysis = analyzer.analyze_batch(new_crashes)
        
        # Check for regressions
        if analysis.has_regressions:
            alert_team(analysis.regressions)
            return False
    
    return True

# Automated crash collection
def collect_crash(crash_path: str):
    reporter.collect(
        crash_path=crash_path,
        build_version=get_build_version(),
        environment=get_environment(),
        user_id=get_user_id(),
    )
```

### Prometheus Integration

```python
from prometheus_client import Counter, Gauge, Histogram

CRASH_COUNT = Counter('app_crashes_total', 'Total crashes', ['type', 'version'])
CRASH_RATE = Gauge('app_crash_rate', 'Crash rate per hour')
CLUSTER_SIZE = Gauge('crash_cluster_size', 'Cluster size', ['signature'])

class CrashMetrics:
    def __init__(self, reporter: CrashReporter):
        self.reporter = reporter
    
    def record_crash(self, crash_type: str, version: str):
        CRASH_COUNT.labels(type=crash_type, version=version).inc()
    
    def update_crash_rate(self):
        rate = self.reporter.get_crash_rate(hours=1)
        CRASH_RATE.set(rate)
    
    def update_clusters(self, clusters):
        for cluster in clusters:
            CLUSTER_SIZE.labels(signature=cluster.signature).set(cluster.count)
```

## Performance Optimization

### Analysis Performance

| Technique | Time | Accuracy | Use Case |
|-----------|------|----------|----------|
| Stack trace parsing | Fast | High | Quick triage |
| Symbolication | Medium | High | Deep analysis |
| Memory analysis | Slow | High | Complex crashes |
| Root cause analysis | Slow | Medium | Automated triage |
| Clustering | Medium | High | Crash grouping |

### Optimized Analysis

```python
from crash_analysis import OptimizedAnalyzer

analyzer = OptimizedAnalyzer()

# Configure for speed
analyzer.configure(
    quick_analysis=True,
    skip_memory_analysis=False,
    parallel_processing=True,
    max_workers=4,
    cache_symbols=True,
)

# Batch analyze crashes
results = analyzer.batch_analyze(crash_paths)
```

## Security Considerations

### Sensitive Data in Crashes

```python
from crash_analysis import CrashSanitizer

sanitizer = CrashSanitizer()

# Configure sanitization
sanitizer.configure(
    # Redact sensitive memory regions
    redact_memory_regions=["stack", "heap"],
    
    # Redact sensitive variables
    redact_variables=["password", "token", "secret", "api_key"],
    
    # Redact file paths
    redact_paths=["/home/*", "/etc/*", "/Users/*"],
    
    # Redact environment variables
    redact_env_vars=["DATABASE_URL", "API_KEY", "SECRET"],
    
    # Mask memory addresses
    mask_addresses=True,
)

# Sanitize crash
sanitized = sanitizer.sanitize(crash)
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Missing symbols | Unresolved addresses | Ensure debug symbols available |
| Incomplete stack | Truncated frames | Check stack unwinding config |
| Large core dumps | Slow analysis | Use compressed dumps, limit analysis |
| False regressions | Incorrect detection | Tune similarity threshold |
| High memory usage | OOM during analysis | Process in batches, limit threads |

### Diagnostic Queries

```python
# Check analysis status
from crash_analysis import AnalysisStatus

status = AnalysisStatus()
check = status.check()
print(f"Symbol server: {check.symbol_server_status}")
print(f"Database: {check.database_status}")
print(f"Queue depth: {check.queue_depth}")
```

## API Reference

### CoreDumpAnalyzer

```python
class CoreDumpAnalyzer:
    def __init__(self, config: AnalysisConfig = None)
    def analyze(self, core_dump_path: str) -> CoreDumpAnalysis
    def analyze_comprehensive(self, core_dump_path: str) -> ComprehensiveAnalysis
    def extract_stack_trace(self, core_dump_path: str) -> list[StackFrame]
    def extract_memory_state(self, core_dump_path: str) -> MemoryState
    def extract_threads(self, core_dump_path: str) -> list[ThreadInfo]
```

### StackTraceProcessor

```python
class StackTraceProcessor:
    def __init__(self, config: ProcessingConfig = None)
    def process(self, stack_trace: str) -> ProcessedTrace
    def process_batch(self, stack_traces: list[str]) -> list[ProcessedTrace]
    def cluster_traces(self, traces: list[ProcessedTrace], **kwargs) -> list[CrashCluster]
    def symbolicate(self, addresses: list[int], binary: str) -> list[Symbol]
    def generate_signature(self, trace: ProcessedTrace) -> str
```

### RootCauseAnalyzer

```python
class RootCauseAnalyzer:
    def __init__(self, config: AnalysisConfig = None)
    def analyze(self, analysis: CoreDumpAnalysis) -> RootCauseResult
    def analyze_comprehensive(self, analysis: CoreDumpAnalysis) -> ComprehensiveResult
    def suggest_fix(self, root_cause: str) -> list[FixSuggestion]
    def find_similar(self, crash: CoreDumpAnalysis) -> list[SimilarCrash]
    def check_regression(self, crash: CoreDumpAnalysis, baseline: str) -> RegressionResult
```

### CrashClusterer

```python
class CrashClusterer:
    def __init__(self, config: ClusteringConfig = None)
    def cluster(self, crashes: list[CoreDumpAnalysis]) -> list[CrashCluster]
    def cluster_comprehensive(self, crashes: list, **kwargs) -> list[CrashCluster]
    def get_cluster_trend(self, cluster: CrashCluster) -> Trend
    def get_cluster_impact(self, cluster: CrashCluster) -> Impact
    def merge_clusters(self, cluster1: CrashCluster, cluster2: CrashCluster) -> CrashCluster
```

### CrashReporter

```python
class CrashReporter:
    def __init__(self, api_url: str = None)
    def collect(self, crash_path: str, **kwargs) -> CollectionResult
    def get_crashes(self, limit: int = 100, **kwargs) -> list[CrashReport]
    def get_new_crashes(self, since_deployment: bool = False) -> list[CrashReport]
    def get_crash_rate(self, hours: int = 24) -> float
    def get_regression_status(self) -> RegressionStatus
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum
from datetime import datetime

class CrashType(Enum):
    SEGFAULT = "segfault"
    ABORT = "abort"
    STACK_OVERFLOW = "stack_overflow"
    OOM = "oom"
    UNHANDLED_EXCEPTION = "unhandled_exception"
    ASSERTION_FAILURE = "assertion_failure"

class Severity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class CoreDumpAnalysis:
    path: str
    signal: str
    fault_address: int
    crashed_function: str
    stack_trace: List['StackFrame']
    thread_count: int
    memory: 'MemoryState'
    handles: List['Handle']
    timestamp: datetime

@dataclass
class StackFrame:
    function: str
    file: str
    line: int
    address: int
    variables: List['Variable']
    inlined: bool

@dataclass
class CrashCluster:
    signature: str
    count: int
    affected_users: int
    first_seen: datetime
    last_seen: datetime
    top_frame: StackFrame
    root_cause: str
    trend: str
    severity: Severity

@dataclass
class RootCauseResult:
    root_cause: str
    category: str
    confidence: float
    evidence: List['Evidence']
    recommendations: List['Recommendation']
    similar_issues: List[str]
```

## Deployment Guide

### Docker Deployment

```yaml
version: '3.8'
services:
  crash-analyzer:
    image: crash-analyzer:latest
    volumes:
      - ./crashes:/crashes
      - ./symbols:/symbols
      - ./reports:/reports
    environment:
      SYMBOL_SERVER: https://symbols.example.com
      API_URL: https://crash-api.example.com
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '4'
```

## Monitoring & Observability

### Metrics Collection

```python
from crash_analysis import MetricsCollector

collector = MetricsCollector()

# Collect crash metrics
collector.counter("crash.total", count, tags={"type": crash_type, "version": version})
collector.gauge("crash.rate", rate)
collector.gauge("crash.cluster.size", size, tags=["signature": signature])
collector.histogram("crash.analysis.duration.seconds", duration)
```

### Alerting Rules

```yaml
groups:
  - name: crash_alerts
    rules:
      - alert: HighCrashRate
        expr: app_crash_rate > 10
        for: 1h
        labels:
          severity: critical
        annotations:
          summary: "High crash rate detected"
          
      - alert: NewCrashType
        expr: increase(app_crashes_total[1h]) > 0
        for: 0m
        labels:
          severity: warning
        annotations:
          summary: "New crash type detected"
```

## Testing Strategy

### Unit Tests

```python
import pytest
from crash_analysis import CoreDumpAnalyzer, StackTraceProcessor

@pytest.fixture
def analyzer():
    return CoreDumpAnalyzer()

def test_core_dump_analysis(analyzer):
    analysis = analyzer.analyze("test.core")
    assert analysis.signal is not None

def test_stack_trace_processing():
    processor = StackTraceProcessor()
    trace = processor.process("test stack trace")
    assert trace.frames is not None
```

## Versioning & Migration

### Version Compatibility

| Component | Minimum Version | Recommended |
|-----------|-----------------|-------------|
| Python | 3.8 | 3.11+ |
| GDB | 10.0 | 12.0+ |
| LLDB | 12.0 | 16.0+ |

## Glossary

| Term | Definition |
|------|------------|
| **Core Dump** | Memory dump at time of crash |
| **Minidump** | Compact crash dump (Windows) |
| **Symbolication** | Converting addresses to names |
| **Stack Unwinding** | Reconstructing call stack |
| **Regression** | New crash type not seen before |

## Changelog

### Version 3.0.0 (2024-01-15)
- Added regression detection
- New crash clustering
- Improved root cause analysis
- Added fix suggestions

## Contributing Guidelines

```bash
git clone https://github.com/awesome-grok/crash-analysis.git
cd crash-analysis
pip install -e ".[dev]"
pytest
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills