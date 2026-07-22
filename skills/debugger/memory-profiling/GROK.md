---
name: "Memory Profiling"
version: "2.0.0"
description: "Comprehensive memory profiling toolkit with heap analysis, leak detection, allocation tracking, garbage collection monitoring, and memory optimization for production applications"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["debugger", "memory", "profiling", "leak-detection", "heap-analysis", "optimization"]
category: "debugger"
personality: "memory-engineer"
use_cases: ["heap analysis", "leak detection", "allocation tracking", "GC monitoring", "memory optimization"]
---

# Memory Profiling

> Production-grade memory profiling framework providing heap analysis, leak detection, allocation tracking, garbage collection monitoring, and memory optimization for diagnosing memory issues in production applications.

## Overview

The Memory Profiling module provides a complete toolkit for analyzing and optimizing memory usage. It implements heap snapshot analysis with object lifecycle tracking, memory leak detection with root cause analysis, allocation hotspot identification, garbage collection monitoring and tuning, and memory optimization recommendations. Every analysis produces actionable reports with object graphs, retention paths, and remediation steps.

## Core Capabilities

### 1. Heap Analysis
- Heap snapshot capture and comparison
- Object graph traversal and visualization
- Retained size calculation
- Dominator tree analysis
- Object distribution by type/size

### 2. Leak Detection
- Growing object detection
- Circular reference identification
- Closure capture analysis
- Event listener leak detection
- Connection pool leak detection

### 3. Allocation Tracking
- Allocation hotspot identification
- Allocation call stack tracking
- Temporary object detection
- Buffer reuse opportunities
- String interning candidates

### 4. GC Monitoring
- GC pause time tracking
- GC frequency analysis
- GC type classification (minor/major)
- GC pressure metrics
- GC tuning recommendations

### 5. Memory Optimization
- Object pooling recommendations
- Cache sizing optimization
- Memory layout improvements
- Data structure selection guidance
- Compression opportunities

## Usage Examples

### Heap Analysis

```python
from memory_profiling import HeapAnalyzer

analyzer = HeapAnalyzer()

# Capture heap snapshot
snapshot = analyzer.capture_snapshot("baseline")
print(f"Heap size: {snapshot.total_size_mb:.1f} MB")
print(f"Objects: {snapshot.total_objects:,}")

# Analyze object distribution
distribution = snapshot.object_distribution()
print("Object distribution:")
for obj_type, count, size in distribution[:10]:
    print(f"  {obj_type}: {count:,} objects ({size:.1f} MB)")

# Find largest objects
largest = snapshot.largest_objects(10)
for obj in largest:
    print(f"  {obj.type_name} @ {obj.address}: {obj.size_kb:.1f} KB")
```

### Leak Detection

```python
from memory_profiling import LeakDetector

detector = LeakDetector()

# Take multiple snapshots
detector.snapshot("t1")
process_requests(1000)
detector.snapshot("t2")
process_requests(1000)
detector.snapshot("t3")

# Detect leaks
leaks = detector.detect_growing_objects(threshold_pct=10)
print(f"Potential leaks: {len(leaks)}")
for leak in leaks:
    print(f"  {leak.type_name}: {leak.growth_pct:.1f}% growth")
    print(f"    Retained: {leak.retained_size_mb:.1f} MB")
    print(f"    Root: {leak.root_path}")
```

### Allocation Tracking

```python
from memory_profiling import AllocationTracker

tracker = AllocationTracker()

# Start tracking
tracker.start_tracking()

# Run workload
for _ in range(10000):
    process_request()

# Stop and analyze
tracker.stop_tracking()
report = tracker.get_report()

print(f"Total allocations: {report.total_allocations:,}")
print(f"Top allocation sites:")
for site in report.top_sites[:5]:
    print(f"  {site.function}: {site.allocations:,} ({site.total_bytes / 1024:.1f} KB)")
```

### GC Monitoring

```python
from memory_profiling import GCMonitor

monitor = GCMonitor()

# Monitor GC activity
monitor.start_monitoring()
run_application()
monitor.stop_monitoring()

stats = monitor.get_stats()
print(f"GC runs: {stats.total_collections}")
print(f"Total pause: {stats.total_pause_ms:.1f}ms")
print(f"Avg pause: {stats.avg_pause_ms:.2f}ms")
print(f"Max pause: {stats.max_pause_ms:.2f}ms")
print(f"Gen 0: {stats.gen0_collections}, Gen 1: {stats.gen1_collections}, Gen 2: {stats.gen2_collections}")
```

## Best Practices

### Heap Analysis
- Capture snapshots at known stable points
- Compare snapshots to identify growth patterns
- Focus on retained size, not just shallow size
- Use dominator tree to find true memory owners

### Leak Detection
- Take at least 3 snapshots to identify trends
- Focus on objects that grow continuously
- Check for common leak patterns (event listeners, closures, caches)
- Monitor in production, not just development

### Allocation Tracking
- Profile during realistic workloads
- Focus on hot paths with high allocation rates
- Look for temporary objects in loops
- Consider object pooling for frequently allocated objects

### GC Monitoring
- Monitor GC pause times as a key metric
- Tune heap size based on allocation patterns
- Avoid premature optimization — measure first
- Consider generational GC tuning

## Related Modules

- **dynamic-analysis**: Runtime profiling and tracing
- **crash-analysis**: Memory-related crash analysis
- **network-debugging**: Network memory usage monitoring
- **performance-tuning**: Memory configuration optimization

---

## Advanced Configuration

### Advanced Heap Analysis

```python
from memory_profiling import HeapAnalyzer, HeapConfig

analyzer = HeapAnalyzer(
    config=HeapConfig(
        capture_interval_seconds=60,
        max_snapshots=100,
        include_weak_references=True,
        include_finalizers=True,
        track_object_graph=True,
        calculate_retained_sizes=True,
    ),
)

# Capture with filters
snapshot = analyzer.capture_snapshot(
    name="baseline",
    filters={
        "min_size_bytes": 1024,
        "include_types": ["dict", "list", "str", "bytes"],
        "exclude_types": ["int", "float", "bool"],
    },
)

# Analyze dominator tree
dominators = snapshot.dominator_tree()
for node in dominators.top_nodes(10):
    print(f"  {node.type_name}: {node.retained_size_mb:.1f} MB ({node.percentage:.1f}%)")
    print(f"    Dominates: {node.dominated_count} objects")
```

### Advanced Leak Detection

```python
from memory_profiling import LeakDetector, LeakConfig

detector = LeakDetector(
    config=LeakConfig(
        growth_threshold_pct=5,
        min_samples=5,
        time_window_seconds=300,
        track_growth_rate=True,
        predict_leak_trajectory=True,
    ),
)

# Monitor over time
detector.start_monitoring(interval_seconds=30)

# Simulate workload
for _ in range(100):
    process_requests()
    time.sleep(1)

# Get leak analysis
analysis = detector.analyze()
print(f"Potential leaks: {len(analysis.leaks)}")
for leak in analysis.leaks:
    print(f"  {leak.type_name}:")
    print(f"    Growth: {leak.growth_pct:.1f}% over {leak.duration_seconds:.0f}s")
    print(f"    Rate: {leak.growth_rate_objects_per_second:.1f} objects/s")
    print(f"    Retained: {leak.retained_size_mb:.1f} MB")
    print(f"    Root path: {leak.root_path}")
    print(f"    Prediction: {leak.predicted_exhaustion_hours:.1f} hours")
```

### Advanced Allocation Tracking

```python
from memory_profiling import AllocationTracker, AllocationConfig

tracker = AllocationTracker(
    config=AllocationConfig(
        sampling_rate=0.1,  # 10% sampling
        max_call_stack_depth=32,
        track_temporary_objects=True,
        track_large_allocations_threshold=10240,  # 10KB
        group_by="module",
    ),
)

# Track allocations
tracker.start_tracking()

# Run workload
for _ in range(10000):
    process_request()

# Get detailed report
report = tracker.get_report()
print(f"Total allocations: {report.total_allocations:,}")
print(f"Total bytes: {report.total_bytes / 1024 / 1024:.1f} MB")
print(f"Temporary objects: {report.temporary_objects:,}")
print(f"Large allocations: {report.large_allocations:,}")

print("\nTop allocation sites by module:")
for module in report.by_module[:5]:
    print(f"  {module.name}: {module.allocations:,} ({module.bytes / 1024:.1f} KB)")
```

### Advanced GC Monitoring

```python
from memory_profiling import GCMonitor, GCConfig

monitor = GCMonitor(
    config=GCConfig(
        track_gc_pause=True,
        track_gc_type=True,
        track_heap_size=True,
        predict_gc_pressure=True,
        alert_on_long_pause_ms=100,
    ),
)

# Monitor GC activity
monitor.start_monitoring()

# Run workload
run_application()

# Get GC statistics
stats = monitor.get_stats()
print(f"GC runs: {stats.total_collections}")
print(f"Total pause: {stats.total_pause_ms:.1f}ms")
print(f"Avg pause: {stats.avg_pause_ms:.2f}ms")
print(f"Max pause: {stats.max_pause_ms:.2f}ms")
print(f"Gen 0: {stats.gen0_collections}")
print(f"Gen 1: {stats.gen1_collections}")
print(f"Gen 2: {stats.gen2_collections}")
print(f"GC pressure: {stats.gc_pressure_score:.1f}/10")

# Get GC recommendations
recommendations = monitor.get_recommendations()
for rec in recommendations:
    print(f"  {rec.parameter}: {rec.current_value} → {rec.recommended_value}")
    print(f"    Impact: {rec.expected_impact}")
```

## Architecture Patterns

### Memory Profiling Architecture

```
┌─────────────────────────────────────────────────────────────┐
│               Memory Profiling Architecture                 │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Collection Layer                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Heap       │  │  Allocation │  │  GC         │ │   │
│  │  │  Snapshots  │  │  Tracking   │  │  Monitoring │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Analysis Layer                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Dominator  │  │  Leak       │  │  Growth     │ │   │
│  │  │  Tree       │  │  Detection  │  │  Analysis   │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Optimization Layer                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Object     │  │  Cache      │  │  Data       │ │   │
│  │  │  Pooling    │  │  Sizing     │  │  Structure  │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Heap Snapshot Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   Heap Snapshot Flow                        │
├─────────────────────────────────────────────────────────────┤
│  1. Pause Application (optional, for consistency)           │
│     └─► Stop-the-world for accurate snapshot                │
│  2. Walk Object Graph                                       │
│     └─► Traverse all reachable objects                      │
│  3. Calculate Sizes                                         │
│     └─► Shallow size + retained size                        │
│  4. Build Dominator Tree                                    │
│     └─► Identify memory ownership                           │
│  5. Analyze Object Distribution                             │
│     └─► Group by type, size, location                       │
│  6. Compare Snapshots                                       │
│     └─► Identify growth patterns                            │
│  7. Generate Report                                         │
│     └─► Produce actionable findings                         │
└─────────────────────────────────────────────────────────────┘
```

## Integration Guide

### Application Integration

```python
# Integration with FastAPI
from fastapi import FastAPI, Request
from memory_profiling import HeapAnalyzer, LeakDetector

app = FastAPI()
analyzer = HeapAnalyzer()
detector = LeakDetector()

@app.on_event("startup")
async def startup():
    analyzer.start_monitoring(interval_seconds=300)
    detector.start_monitoring(interval_seconds=60)

@app.get("/admin/memory/snapshot")
async def take_snapshot():
    snapshot = analyzer.capture_snapshot()
    return {
        "total_size_mb": snapshot.total_size_mb,
        "objects": snapshot.total_objects,
    }

@app.get("/admin/memory/leaks")
async def check_leaks():
    analysis = detector.analyze()
    return {
        "leaks_found": len(analysis.leaks),
        "leaks": [l.__dict__ for l in analysis.leaks],
    }
```

### Prometheus Integration

```python
from prometheus_client import Gauge, Histogram

HEAP_SIZE = Gauge('app_heap_size_bytes', 'Heap size')
OBJECT_COUNT = Gauge('app_object_count', 'Object count')
GC_PAUSE = Histogram('app_gc_pause_seconds', 'GC pause duration')
GC_COLLECTIONS = Gauge('app_gc_collections_total', 'GC collections', ['generation'])

class MemoryMetrics:
    def __init__(self, analyzer: HeapAnalyzer, gc_monitor: GCMonitor):
        self.analyzer = analyzer
        self.gc_monitor = gc_monitor
    
    def update(self):
        snapshot = self.analyzer.get_latest_snapshot()
        HEAP_SIZE.set(snapshot.total_size_bytes)
        OBJECT_COUNT.set(snapshot.total_objects)
        
        stats = self.gc_monitor.get_stats()
        GC_PAUSE.observe(stats.avg_pause_ms / 1000)
        GC_COLLECTIONS.labels(generation='0').set(stats.gen0_collections)
        GC_COLLECTIONS.labels(generation='1').set(stats.gen1_collections)
        GC_COLLECTIONS.labels(generation='2').set(stats.gen2_collections)
```

## Performance Optimization

### Memory Profiling Overhead

| Technique | CPU Overhead | Memory Overhead | Accuracy |
|-----------|--------------|-----------------|----------|
| Heap Snapshot | 5-20% | 10-50% | High |
| Allocation Tracking | 10-30% | 5-15% | High |
| GC Monitoring | 1-3% | < 1% | Medium |
| Sampling | 2-5% | 2-5% | Medium |

### Optimized Memory Profiling

```python
from memory_profiling import OptimizedProfiler

profiler = OptimizedProfiler()

# Configure for minimal overhead
profiler.configure(
    sampling_rate=0.01,  # 1% sampling
    max_snapshots=10,
    snapshot_interval_seconds=300,
    track_only_large_objects=True,
    large_object_threshold=10240,  # 10KB
)

# Profile with filtering
profiler.filter_types(
    include=["dict", "list", "bytes"],
    exclude=["int", "float", "bool", "NoneType"],
)
```

## Security Considerations

### Sensitive Data in Heap

```python
from memory_profiling import HeapSanitizer

sanitizer = HeapSanitizer()

# Configure sanitization
sanitizer.configure(
    # Redact sensitive strings
    redact_patterns=[
        r"password=.*",
        r"token=.*",
        r"secret=.*",
        r"api_key=.*",
        r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",  # Credit card
        r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
    ],
    
    # Redact sensitive keys
    redact_keys=["password", "token", "secret", "api_key", "ssn"],
)

# Sanitize snapshot
sanitized = sanitizer.sanitize(snapshot)
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| OOM during profiling | Process killed | Reduce snapshot frequency, use sampling |
| Inaccurate retained sizes | Wrong ownership attribution | Ensure consistent snapshots |
| Missing objects | Incomplete object graph | Check for weak references |
| High GC pressure | Frequent GC pauses | Tune heap size, reduce allocations |
| Memory fragmentation | High memory usage, low utilization | Consider heap compaction |

### Diagnostic Queries

```python
# Check memory health
from memory_profiling import MemoryHealth

health = MemoryHealth()
status = health.check()
print(f"Memory health: {status.status}")
print(f"Heap usage: {status.heap_usage_pct:.1f}%")
print(f"GC pressure: {status.gc_pressure:.1f}/10")
print(f"Fragmentation: {status.fragmentation_pct:.1f}%")
```

## API Reference

### HeapAnalyzer

```python
class HeapAnalyzer:
    def __init__(self, config: HeapConfig = None)
    def capture_snapshot(self, name: str = None, filters: dict = None) -> HeapSnapshot
    def compare(self, snapshot1: str, snapshot2: str) -> SnapshotDiff
    def get_latest_snapshot(self) -> HeapSnapshot
    def list_snapshots(self) -> list[HeapSnapshot]
    def export_snapshot(self, name: str, format: str = "json")
```

### LeakDetector

```python
class LeakDetector:
    def __init__(self, config: LeakConfig = None)
    def start_monitoring(self, interval_seconds: int = 60)
    def stop_monitoring(self)
    def analyze(self) -> LeakAnalysis
    def get_growing_objects(self, threshold_pct: float = 10) -> list[GrowingObject]
    def get_leak_prediction(self) -> LeakPrediction
```

### AllocationTracker

```python
class AllocationTracker:
    def __init__(self, config: AllocationConfig = None)
    def start_tracking(self, sampling_rate: float = 0.1)
    def stop_tracking(self) -> AllocationReport
    def get_top_sites(self, n: int = 10) -> list[AllocationSite]
    def get_temporary_objects(self) -> list[TemporaryObject]
    def get_large_allocations(self, threshold: int = 10240) -> list[LargeAllocation]
```

### GCMonitor

```python
class GCMonitor:
    def __init__(self, config: GCConfig = None)
    def start_monitoring(self)
    def stop_monitoring(self)
    def get_stats(self) -> GCStats
    def get_pause_histogram(self) -> PauseHistogram
    def get_recommendations(self) -> list[GCRecommendation]
    def get_gc_pressure(self) -> float
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum
from datetime import datetime

class ObjectType(Enum):
    DICT = "dict"
    LIST = "list"
    STR = "str"
    BYTES = "bytes"
    INT = "int"
    FLOAT = "float"
    TUPLE = "tuple"
    SET = "set"
    CUSTOM = "custom"

@dataclass
class HeapSnapshot:
    name: str
    timestamp: datetime
    total_size_bytes: int
    total_objects: int
    object_distribution: Dict[str, int]
    dominator_tree: Optional['DominatorNode']

@dataclass
class Leak:
    type_name: str
    growth_pct: float
    growth_rate_objects_per_second: float
    retained_size_mb: float
    root_path: str
    first_seen: datetime
    last_seen: datetime
    predicted_exhaustion_hours: Optional[float]

@dataclass
class AllocationSite:
    function: str
    file: str
    line: int
    count: int
    bytes: int
    percentage: float
    call_stack: Optional[List[str]]

@dataclass
class GCStats:
    total_collections: int
    total_pause_ms: float
    avg_pause_ms: float
    max_pause_ms: float
    gen0_collections: int
    gen1_collections: int
    gen2_collections: int
    gc_pressure_score: float
```

## Deployment Guide

### Docker Deployment

```yaml
version: '3.8'
services:
  app:
    image: app:latest
    environment:
      MEMORY_PROFILER_ENABLED: "true"
      MEMORY_PROFILER_INTERVAL: "60"
      MEMORY_PROFILER_SAMPLING_RATE: "0.01"
    volumes:
      - ./heap_dumps:/heap_dumps
    deploy:
      resources:
        limits:
          memory: 4G
```

## Monitoring & Observability

### Metrics Collection

```python
from memory_profiling import MetricsCollector

collector = MetricsCollector()

# Collect memory metrics
collector.gauge("memory.heap.size.bytes", heap_size)
collector.gauge("memory.objects.total", object_count)
collector.histogram("memory.gc.pause.seconds", gc_pause)
collector.counter("memory.gc.collections.total", gc_count, tags={"generation": gen})
collector.gauge("memory.leaks.detected", leak_count)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from memory_profiling import HeapAnalyzer, LeakDetector

@pytest.fixture
def analyzer():
    return HeapAnalyzer()

def test_heap_snapshot(analyzer):
    snapshot = analyzer.capture_snapshot()
    assert snapshot.total_objects > 0

def test_leak_detection():
    detector = LeakDetector()
    detector.start_monitoring()
    # Simulate leak
    leaky_list = []
    for _ in range(1000):
        leaky_list.append("x" * 1024)
    detector.stop_monitoring()
    analysis = detector.analyze()
    assert len(analysis.leaks) > 0
```

## Versioning & Migration

### Version Compatibility

| Component | Minimum Version | Recommended |
|-----------|-----------------|-------------|
| Python | 3.8 | 3.11+ |
| Go | 1.18 | 1.21+ |
| Node.js | 16 | 20+ |

## Glossary

| Term | Definition |
|------|------------|
| **Shallow Size** | Direct memory usage of an object |
| **Retained Size** | Memory freed if object is garbage collected |
| **Dominator** | Object that keeps other objects alive |
| **Weak Reference** | Reference that doesn't prevent garbage collection |
| **GC Pressure** | Frequency and duration of garbage collection |

## Changelog

### Version 3.0.0 (2024-01-15)
- Added dominator tree analysis
- New leak prediction
- Improved GC monitoring
- Added allocation tracking

## Contributing Guidelines

```bash
git clone https://github.com/awesome-grok/memory-profiling.git
cd memory-profiling
pip install -e ".[dev]"
pytest
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills