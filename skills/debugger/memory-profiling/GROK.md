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