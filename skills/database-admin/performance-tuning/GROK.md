---
name: "Performance Tuning"
version: "2.0.0"
description: "Comprehensive database performance tuning toolkit with query optimization, index tuning, connection tuning, memory configuration, and workload analysis for maximizing database throughput and minimizing latency"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["database-admin", "performance", "tuning", "optimization", "indexing", "workload"]
category: "database-admin"
personality: "performance-engineer"
use_cases: ["query optimization", "index tuning", "memory tuning", "connection tuning", "workload analysis"]
---

# Performance Tuning

> Production-grade database performance tuning framework providing query optimization, index tuning, connection and memory configuration, workload analysis, and automated tuning recommendations for maximizing database throughput.

## Overview

The Performance Tuning module provides a comprehensive toolkit for analyzing and optimizing database performance. It implements query execution plan analysis, automated index recommendation, connection pool tuning, memory and I/O configuration optimization, workload pattern analysis, and regression detection. Every analysis produces actionable recommendations with estimated performance impact and implementation priority.

## Core Capabilities

### 1. Query Performance Analysis
- Slow query identification and ranking
- Execution plan analysis with issue detection
- Query fingerprinting for pattern grouping
- Resource consumption attribution (CPU, I/O, memory)
- Query regression detection over time

### 2. Index Tuning
- Missing index detection from query patterns
- Redundant index identification
- Index size and bloat analysis
- Covering index recommendations
- Index maintenance scheduling

### 3. Connection and Memory Tuning
- Connection pool sizing recommendations
- Memory allocation optimization (shared_buffers, work_mem)
- Effective cache size estimation
- WAL configuration tuning
- Checkpoint optimization

### 4. Workload Analysis
- Read/write ratio analysis
- Peak load pattern detection
- Concurrent connection profiling
- Transaction throughput measurement
- Lock contention analysis

### 5. Configuration Optimization
- Parameter impact modeling
- Automated configuration recommendations
- A/B testing for configuration changes
- Configuration drift detection
- Best practice compliance checking

### 6. Performance Regression Detection
- Baseline establishment and monitoring
- Automatic regression alerting
- Root cause analysis for regressions
- Before/after comparison reporting

## Usage Examples

### Query Performance Analysis

```python
from performance_tuning import QueryAnalyzer, PerformanceReport

analyzer = QueryAnalyzer(connection_string="postgresql://admin:pass@localhost/prod")

# Analyze slow queries
report = analyzer.analyze_slow_queries(
    threshold_ms=500,
    top_n=20,
    time_range_hours=24,
)

print(f"Slow queries found: {report.total_slow_queries}")
print(f"Total time consumed: {report.total_time_seconds:.1f}s")

for query in report.top_queries[:5]:
    print(f"  {query.avg_duration_ms:.0f}ms avg ({query.calls} calls): "
          f"{query.query_text[:60]}...")
    print(f"    Impact score: {query.impact_score:.1f}")
```

### Index Tuning

```python
from performance_tuning import IndexTuner

tuner = IndexTuner(connection_string="postgresql://admin:pass@localhost/prod")

# Get index recommendations
recommendations = tuner.recommend_indexes(
    analyze_queries=True,
    analyze_usage=True,
    min_impact_ms=100,
)

print(f"Recommendations: {len(recommendations)}")
for rec in recommendations[:5]:
    print(f"  [{rec.priority}] {rec.index_definition}")
    print(f"    Impact: {rec.estimated_improvement}")
    print(f"    Size: {rec.size_estimate_mb:.1f} MB")

# Find unused indexes
unused = tuner.find_unused_indexes(min_scans=0)
print(f"Unused indexes: {len(unused)}")
for idx in unused:
    print(f"  {idx.name}: {idx.size_mb:.1f} MB, {idx.scans} scans")
```

### Memory Tuning

```python
from performance_tuning import MemoryTuner

tuner = MemoryTuner(connection_string="postgresql://admin:pass@localhost/prod")

# Analyze memory usage
analysis = tuner.analyze_memory()

print("Current memory settings:")
for param in analysis.current_settings:
    print(f"  {param.name}: {param.value}")

# Get recommendations
recs = tuner.recommend_memory_settings(
    total_ram_gb=64,
    dedicated_server=True,
    workload_type="oltp",
)

print("\nRecommendations:")
for rec in recs:
    print(f"  {rec.parameter}: {rec.current_value} → {rec.recommended_value}")
    print(f"    Impact: {rec.estimated_impact}")
```

### Workload Analysis

```python
from performance_tuning import WorkloadAnalyzer

analyzer = WorkloadAnalyzer(connection_string="postgresql://admin:pass@localhost/prod")

# Analyze workload patterns
workload = analyzer.analyze(time_range_hours=168)  # 1 week

print(f"Read/Write ratio: {workload.read_write_ratio:.1f}")
print(f"Avg connections: {workload.avg_connections:.1f}")
print(f"Peak connections: {workload.peak_connections}")
print(f"Transactions/sec: {workload.tps:.1f}")

# Peak hours
print("\nPeak hours:")
for hour in workload.peak_hours:
    print(f"  {hour.hour}:00 - {hour.tps:.0f} TPS ({hour.connections} connections)")
```

## Best Practices

### Query Optimization
- Focus on the top 10 queries by total time — they account for 80% of load
- Use EXPLAIN ANALYZE for actual execution times, not just estimates
- Always check for missing indexes when queries use WHERE or JOIN clauses
- Avoid SELECT * — fetch only the columns you need

### Index Tuning
- Monitor index usage weekly — drop indexes with zero scans
- Use covering indexes for frequently accessed column combinations
- Keep composite index column count to 3-4 maximum
- Schedule REINDEX during maintenance windows

### Memory Configuration
- Set shared_buffers to 25% of total RAM on dedicated servers
- Set effective_cache_size to 75% of total RAM
- Increase work_mem for complex sorts and joins
- Monitor buffer cache hit ratio — target > 99%

### Workload Management
- Use connection pooling to limit concurrent connections
- Route read queries to replicas when possible
- Monitor lock contention during peak hours
- Implement query timeouts for long-running queries

## Related Modules

- **query-optimization**: Detailed query plan analysis and rewriting
- **db-management**: Database configuration and maintenance
- **monitoring**: Real-time performance monitoring
- **security-hardening**: Security configuration that may impact performance