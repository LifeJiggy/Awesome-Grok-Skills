---
name: "performance-tuning"
category: "core"
version: "2.0.0"
tags: ["core", "performance", "profiling", "optimization", "benchmarks"]
---

# Performance Tuning

## Overview

The Performance Tuning module provides systematic approaches to identifying and resolving performance bottlenecks in software systems. It covers profiling methodologies, benchmarking frameworks, database query optimization, caching strategies, and runtime performance analysis across languages and platforms.

This skill is essential for performance engineers, backend developers, and SREs optimizing application performance and resource utilization.

## Core Capabilities

- **Profiling**: CPU profiling, memory profiling, I/O profiling, and flame graph generation
- **Benchmarking**: Micro-benchmarking, load testing, and comparative benchmarking frameworks
- **Database Optimization**: Query plan analysis, index optimization, N+1 detection, and connection pooling
- **Caching**: Multi-level caching strategies, cache invalidation patterns, and cache warming
- **Runtime Optimization**: JIT compilation awareness, garbage collection tuning, and memory layout optimization
- **Network Optimization**: Connection pooling, keep-alive, compression, and protocol optimization
- **Load Testing**: Stress testing, endurance testing, and capacity planning methodologies

## Usage Examples

```python
from performance_tuning import (
    Profiler,
    BenchmarkRunner,
    DBOptimizer,
    CacheStrategy,
    LoadTester,
)

# --- Profiling ---
profiler = Profiler()
profile = profiler.profile_function(
    target=my_function,
    args=(large_dataset,),
    profiler_type="memory",
)
print(f"Peak memory: {profile.peak_memory_mb:.1f} MB")
print(f"Allocations: {profile.allocations:,}")
print(f"Hotspots: {len(profile.hotspots)}")

# --- Benchmarking ---
runner = BenchmarkRunner()
result = runner.benchmark(
    functions=[solution_a, solution_b],
    input_sizes=[100, 1000, 10000],
    iterations=100,
)
for name, timings in result.results.items():
    print(f"  {name}: {timings['mean_ms']:.2f}ms (std: {timings['std_ms']:.2f}ms)")

# --- DB Optimization ---
db_opt = DBOptimizer()
analysis = db_opt.analyze_query(
    query="SELECT * FROM users WHERE email = ?",
    execution_plan=mock_plan,
)
print(f"Suggestions: {analysis.suggestions}")
print(f"Missing indexes: {analysis.missing_indexes}")

# --- Caching ---
cache = CacheStrategy()
strategy = cache.recommend(
    access_pattern="read_heavy",
    data_freshness="eventual",
    hit_rate_target=0.95,
)
print(f"Strategy: {strategy.level}")
print(f"Invalidation: {strategy.invalidation}")

# --- Load Testing ---
tester = LoadTester()
result = tester.run(
    target="https://api.example.com/health",
    concurrent_users=100,
    duration_seconds=60,
)
print(f"Throughput: {result.requests_per_second:.0f} req/s")
print(f"P99 latency: {result.p99_ms:.0f}ms")
print(f"Error rate: {result.error_rate:.2%}")
```

## Best Practices

- Always profile before optimizing — measure, don't guess
- Use statistical benchmarks with multiple iterations and warm-up
- Focus on the hottest code paths — 80/20 rule applies to performance
- Consider the full stack: code, database, network, and disk I/O
- Use flame graphs to identify optimization opportunities quickly
- Test with production-like data volumes and access patterns
- Monitor performance in production, not just in benchmarks
- Consider the cost/complexity vs. performance gain tradeoff
- Use A/B testing for performance optimizations in production
- Document performance baselines and regressions

## Related Modules

- **efficient-code**: Writing clean and efficient code
- **code-golf**: Extreme code minimization
- **algorithmic-art**: Algorithmic art and visualization
- **meme-code-hybrids**: Fun with code optimization
