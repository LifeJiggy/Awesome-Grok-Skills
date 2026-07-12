---
name: "Query Optimization"
version: "2.0.0"
description: "Comprehensive query optimization toolkit with plan analysis, index recommendations, query rewriting, execution plan visualization, and performance benchmarking for database query performance"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["database", "query-optimization", "execution-plans", "indexing", "performance", "profiling"]
category: "database"
personality: "query-optimizer"
use_cases: ["query plan analysis", "index optimization", "query rewriting", "performance benchmarking", "slow query detection"]
---

# Query Optimization

> Production-grade query optimization framework providing execution plan analysis, index recommendations, query rewriting, performance benchmarking, and slow query detection for database query performance tuning.

## Overview

The Query Optimization module provides tools for analyzing, diagnosing, and improving database query performance. It implements execution plan parsing and visualization, index usage analysis with automated recommendations, query rewriting for better performance, histogram-based selectivity estimation, join order optimization, and comprehensive performance benchmarking. Every analysis returns actionable recommendations with estimated performance improvements.

## Core Capabilities

### 1. Execution Plan Analysis
- Parse and visualize EXPLAIN/EXPLAIN ANALYZE output
- Identify full table scans, key lookups, and file sorts
- Calculate estimated vs actual row counts
- Detect plan regressions between versions
- Nested loop, hash join, and merge join analysis

### 2. Index Optimization
- Missing index detection from query patterns
- Duplicate and overlapping index identification
- Composite index order optimization
- Index-only scan opportunities
- Covering index recommendations

### 3. Query Rewriting
- Subquery to JOIN conversion
- IN to EXISTS rewriting
- OR to UNION ALL rewriting
- LIMIT pushdown optimization
- Predicate pushdown through joins

### 4. Selectivity Estimation
- Histogram-based selectivity calculation
- Correlated column estimation
- NULL selectivity handling
- Multi-column predicate estimation
- Join selectivity estimation

### 5. Performance Benchmarking
- Query throughput measurement (QPS)
- Latency distribution analysis (p50, p95, p99)
- Concurrent query performance testing
- Plan stability monitoring
- Regression detection between releases

### 6. Slow Query Detection
- Real-time slow query logging
- Query fingerprinting and grouping
- Resource consumption tracking
- I/O and CPU usage attribution
- Query complexity scoring

## Usage Examples

### Execution Plan Analysis

```python
from query_optimization import PlanAnalyzer, ExplainFormat

analyzer = PlanAnalyzer()

# Parse EXPLAIN ANALYZE output
plan = analyzer.parse_explain("""
Sort  (cost=1000.00..1000.05 rows=20 width=100) (actual time=15.000..15.010 rows=18 loops=1)
  Sort Key: orders.created_at DESC
  ->  Hash Join  (cost=500.00..999.00 rows=20 width=100) (actual time=10.000..14.900 rows=18 loops=1)
        Hash Cond: (orders.customer_id = customers.id)
        ->  Seq Scan on orders  (cost=0.00..800.00 rows=10000 width=50) (actual time=0.010..8.000 rows=10000 loops=1)
              Filter: (status = 'active')
        ->  Hash  (cost=100.00..100.00 rows=5000 width=50) (actual time=1.500..1.500 rows=5000 loops=1)
              ->  Seq Scan on customers  (cost=0.00..100.00 rows=5000 width=50) (actual time=0.005..1.000 rows=5000 loops=1)
Planning Time: 0.500 ms
Execution Time: 15.500 ms
""")

# Analyze the plan
analysis = analyzer.analyze(plan)
print(f"Total cost:     {analysis.total_cost:.2f}")
print(f"Actual time:    {analysis.actual_time_ms:.2f}ms")
print(f"Rows returned:  {analysis.rows_returned}")
print(f"Issues found:   {len(analysis.issues)}")

for issue in analysis.issues:
    print(f"  [{issue.severity}] {issue.description}")
    print(f"    Suggestion: {issue.suggestion}")
```

### Index Recommendations

```python
from query_optimization import IndexRecommender

recommender = IndexRecommender()

# Analyze queries and recommend indexes
queries = [
    "SELECT * FROM orders WHERE customer_id = ? AND status = 'active'",
    "SELECT * FROM orders WHERE created_at > ? ORDER BY total DESC",
    "SELECT * FROM customers WHERE email = ?",
]

recommendations = recommender.analyze(queries)

for rec in recommendations:
    print(f"  Index: {rec.index_definition}")
    print(f"  Impact: {rec.estimated_improvement}")
    print(f"  Queries helped: {len(rec.queries_affected)}")
    print(f"  Size estimate: {rec.size_estimate_mb:.1f} MB")
```

### Query Rewriting

```python
from query_optimization import QueryRewriter

rewriter = QueryRewriter()

# Rewrite for better performance
original = """
SELECT * FROM orders
WHERE customer_id IN (SELECT id FROM customers WHERE region = 'US')
AND status = 'active'
"""

optimized = rewriter.rewrite(original)
print(f"Original:  {original.strip()}")
print(f"Optimized: {optimized.rewritten_query.strip()}")
print(f"Strategy:  {optimized.strategy}")
print(f"Estimated improvement: {optimized.estimated_improvement}")
```

### Performance Benchmarking

```python
from query_optimization import QueryBenchmark

benchmark = QueryBenchmark(database="production")

# Benchmark a query
result = benchmark.run(
    query="SELECT * FROM orders WHERE status = ? AND created_at > ?",
    params=["active", "2024-01-01"],
    iterations=1000,
    concurrency=10,
)

print(f"Throughput:   {result.qps:.1f} QPS")
print(f"Latency p50:  {result.latency_p50_ms:.2f}ms")
print(f"Latency p95:  {result.latency_p95_ms:.2f}ms")
print(f"Latency p99:  {result.latency_p99_ms:.2f}ms")
print(f"Error rate:   {result.error_rate:.4f}")

# Compare with baseline
regression = benchmark.compare(result, baseline)
if regression:
    print(f"Regression detected: {regression.description}")
```

## Best Practices

### Execution Plan Analysis
- Always use EXPLAIN ANALYZE for actual execution times, not just EXPLAIN
- Focus on high-cost nodes — they dominate total query time
- Watch for nested loops with high row estimates — hash joins may be better
- Compare estimated vs actual rows — large discrepancies indicate stale statistics

### Index Design
- Create indexes that match your WHERE clause column order
- Include SELECT columns in composite indexes for covering (index-only) scans
- Limit composite indexes to 3-4 columns — more columns have diminishing returns
- Monitor index size — large indexes slow down writes and consume memory

### Query Rewriting
- Replace correlated subqueries with JOINs — they're almost always faster
- Use EXISTS instead of IN for subqueries with potential NULLs
- Push predicates as close to the data source as possible
- Avoid SELECT * — fetch only the columns you need

### Benchmarking
- Run benchmarks during off-peak hours to avoid interference
- Use realistic data volumes and distributions
- Warm the cache before measuring — cold cache results are misleading
- Measure at multiple concurrency levels — performance may degrade non-linearly

## Related Modules

- **database-administration**: Database connection management and monitoring
- **mongodb**: MongoDB-specific query optimization
- **data-modeling**: Schema design that supports efficient querying
- **statistical-analysis**: Statistical methods for selectivity estimation