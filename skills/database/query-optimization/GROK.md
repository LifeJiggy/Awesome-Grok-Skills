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

---

## Advanced Configuration

### Advanced Execution Plan Analysis

```python
from query_optimization import PlanAnalyzer, PlanNodeType, CostModel

analyzer = PlanAnalyzer(cost_model=CostModel.POSTGRESQL_15)

# Parse complex execution plan
plan = analyzer.parse_explain("""
Sort  (cost=12345.67..12345.72 rows=100 width=150) (actual time=123.456..123.480 rows=100 loops=1)
  Sort Key: o.created_at DESC
  ->  Hash Join  (cost=1000.00..12000.00 rows=100 width=150) (actual time=50.123..120.000 rows=100 loops=1)
        Hash Cond: (o.customer_id = c.id)
        ->  Bitmap Heap Scan on orders o  (cost=500.00..10000.00 rows=50000 width=80) (actual time=25.000..80.000 rows=50000 loops=1)
              Recheck Cond: (status = 'active')
              Rows Removed by Filter: 50000
              Heap Blocks: exact=1000
              ->  Bitmap Index Scan on idx_orders_status  (cost=0.00..487.50 rows=50000 width=0) (actual time=20.000..20.000 rows=50000 loops=1)
        ->  Hash  (cost=200.00..200.00 rows=10000 width=70) (actual time=20.000..20.000 rows=10000 loops=1)
              Buckets: 16384  Batches: 1  Memory Usage: 1234kB
              ->  Seq Scan on customers c  (cost=0.00..200.00 rows=10000 width=70) (actual time=0.010..10.000 rows=10000 loops=1)
Planning Time: 2.500 ms
Execution Time: 125.000 ms
""")

# Deep analysis
analysis = analyzer.analyze(plan, deep=True)
print(f"Total cost: {analysis.total_cost:.2f}")
print(f"Actual time: {analysis.actual_time_ms:.2f}ms")
print(f"Rows returned: {analysis.rows_returned}")
print(f"Memory usage: {analysis.memory_usage_kb:.0f} KB")
print(f"Issues found: {len(analysis.issues)}")

# Get cost breakdown
breakdown = analyzer.get_cost_breakdown(plan)
for node, cost in breakdown.items():
    print(f"  {node}: {cost:.2f} ({cost/analysis.total_cost*100:.1f}%)")
```

### Selectivity Estimation

```python
from query_optimization import SelectivityEstimator, Histogram

estimator = SelectivityEstimator()

# Build histogram for column
histogram = estimator.build_histogram(
    table="orders",
    column="total",
    num_buckets=100,
    sample_size=100000,
)

# Estimate selectivity for predicates
selectivity_eq = estimator.estimate_selectivity(
    histogram=histogram,
    predicate="total = 100.00",
)
print(f"Equality selectivity: {selectivity_eq:.6f}")

selectivity_range = estimator.estimate_selectivity(
    histogram=histogram,
    predicate="total BETWEEN 50.00 AND 150.00",
)
print(f"Range selectivity: {selectivity_range:.6f}")

# Multi-column selectivity
mc_selectivity = estimator.estimate_multi_column(
    columns=["status", "region"],
    predicates=[
        ("status", "=", "'active'"),
        ("region", "=", "'US'"),
    ],
)
print(f"Multi-column selectivity: {mc_selectivity:.6f}")
```

### Query Rewriting Engine

```python
from query_optimization import QueryRewriter, RewriteStrategy

rewriter = QueryRewriter(strategies=[
    RewriteStrategy.SUBQUERY_TO_JOIN,
    RewriteStrategy.IN_TO_EXISTS,
    RewriteStrategy.OR_TO_UNION_ALL,
    RewriteStrategy.LIMIT_PUSHDOWN,
    RewriteStrategy.PREDICATE_PUSHDOWN,
    RewriteStrategy.CTE_MATERIALIZATION,
])

# Rewrite complex query
original = """
SELECT * FROM orders o
WHERE o.customer_id IN (
    SELECT id FROM customers WHERE region = 'US'
)
AND o.status = 'active'
AND o.created_at > '2024-01-01'
ORDER BY o.total DESC
LIMIT 100
"""

result = rewriter.rewrite(original)
print(f"Original:\n{original}\n")
print(f"Optimized:\n{result.rewritten_query}\n")
print(f"Strategies applied: {result.strategies_applied}")
print(f"Estimated improvement: {result.estimated_improvement:.1f}%")

# Get rewrite details
for detail in result.details:
    print(f"  {detail.strategy}: {detail.explanation}")
```

## Architecture Patterns

### Query Optimization Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                   Query Optimization Pipeline               │
├─────────────────────────────────────────────────────────────┤
│  1. Parse Query                                             │
│     └─► AST Generation                                      │
│  2. Validate Query                                          │
│     └─► Syntax & Semantics Check                            │
│  3. Generate Execution Plans                                │
│     └─► Plan Enumeration (NLJ, Hash, Merge)                 │
│  4. Estimate Costs                                          │
│     └─► Statistics-based Cost Model                         │
│  5. Select Best Plan                                        │
│     └─► Plan Optimization                                   │
│  6. Execute Plan                                            │
│     └─► Runtime Execution                                   │
│  7. Collect Statistics                                      │
│     └─► Update Histograms                                   │
└─────────────────────────────────────────────────────────────┘
```

### Index Selection Algorithm

```
┌─────────────────────────────────────────────────────────────┐
│                   Index Selection Algorithm                 │
├─────────────────────────────────────────────────────────────┤
│  Input: Query workload, available statistics                │
│                                                             │
│  1. Extract predicates from WHERE clauses                   │
│  2. Find matching indexes (exact, prefix, range)            │
│  3. Estimate selectivity for each predicate                 │
│  4. Calculate index benefit (I/O reduction)                 │
│  5. Calculate index cost (storage, maintenance)             │
│  6. Rank indexes by benefit/cost ratio                      │
│  7. Return top-K recommendations                            │
│                                                             │
│  Output: Recommended indexes with expected improvement      │
└─────────────────────────────────────────────────────────────┘
```

### Join Order Optimization

```
┌─────────────────────────────────────────────────────────────┐
│                   Join Order Optimization                   │
├─────────────────────────────────────────────────────────────┤
│  Input: Tables to join, join predicates, statistics         │
│                                                             │
│  1. Build join graph                                        │
│  2. Estimate cardinalities for single tables                │
│  3. Enumerate possible join orders                          │
│  4. For each order:                                         │
│     a. Choose join type (NLJ, Hash, Merge)                  │
│     b. Estimate cost                                        │
│  5. Select minimum cost order                               │
│  6. Apply predicate pushdown                                │
│  7. Apply projection pushdown                               │
│                                                             │
│  Output: Optimized join order with join types               │
└─────────────────────────────────────────────────────────────┘
```

## Integration Guide

### Application Integration

```python
# Integration with SQLAlchemy
from sqlalchemy import event
from query_optimization import QueryAnalyzer

analyzer = QueryAnalyzer()

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    duration = time.time() - context._query_start_time
    if duration > 1.0:  # Slow query threshold
        analyzer.log_slow_query(statement, parameters, duration)
```

### Monitoring Integration

```python
# Integration with Prometheus
from prometheus_client import Counter, Histogram, Gauge

QUERY_COUNT = Counter('db_query_total', 'Total queries', ['status', 'type'])
QUERY_DURATION = Histogram('db_query_duration_seconds', 'Query duration')
SLOW_QUERY_COUNT = Counter('db_slow_query_total', 'Slow queries')
INDEX_HIT_RATIO = Gauge('db_index_hit_ratio', 'Index hit ratio')

class QueryMetricsCollector:
    def record_query(self, query_type, duration, success):
        status = 'success' if success else 'error'
        QUERY_COUNT.labels(status=status, type=query_type).inc()
        QUERY_DURATION.observe(duration)
        
        if duration > 1.0:
            SLOW_QUERY_COUNT.inc()
    
    def update_index_hit_ratio(self, ratio):
        INDEX_HIT_RATIO.set(ratio)
```

### Caching Integration

```python
# Integration with Redis cache
from query_optimization import QueryCache, CacheStrategy

cache = QueryCache(
    redis_url="redis://localhost:6379",
    strategy=CacheStrategy.ADAPTIVE,
    ttl_seconds=300,
    max_size_mb=1024,
)

@cache.memoize(key_prefix="query")
async def execute_query(conn, query, params=None):
    return await conn.execute(query, params)

# Cache-aware query execution
result = await execute_query(
    conn,
    "SELECT * FROM users WHERE region = $1",
    params=["US"]
)
```

## Performance Optimization

### Query Performance Tuning

| Technique | Description | Impact |
|-----------|-------------|--------|
| Index-only scan | Fetch data from index only | High |
| Predicate pushdown | Filter data at source | High |
| Join reordering | Optimize join order | Medium-High |
| Parallel query | Use multiple workers | Medium |
| JIT compilation | Compile queries at runtime | Medium |
| Materialized CTE | Pre-compute CTE results | Low-Medium |

### Index Optimization Strategies

```python
from query_optimization import IndexOptimizer

optimizer = IndexOptimizer()

# Analyze workload and recommend indexes
workload = [
    {"query": "SELECT * FROM orders WHERE status = ? AND region = ?", "frequency": 1000},
    {"query": "SELECT * FROM orders WHERE customer_id = ?", "frequency": 500},
    {"query": "SELECT * FROM orders WHERE created_at > ? ORDER BY total DESC", "frequency": 200},
]

recommendations = optimizer.analyze_workload(workload)
for rec in recommendations:
    print(f"Index: {rec.definition}")
    print(f"  Impact: {rec.estimated_improvement:.1f}%")
    print(f"  Size: {rec.size_estimate_mb:.1f} MB")
    print(f"  Maintenance cost: {rec.maintenance_cost}")
    print()
```

### Query Plan Stability

```python
from query_optimization import PlanStabilityMonitor

monitor = PlanStabilityMonitor()

# Monitor plan stability
stability = monitor.check_stability(
    query="SELECT * FROM orders WHERE status = ?",
    sample_size=1000,
)

print(f"Plan stable: {stability.is_stable}")
print(f"Plan variations: {len(stability.variations)}")
for variation in stability.variations:
    print(f"  {variation.plan_hash}: {variation.frequency}% ({variation.avg_cost:.2f})")

# Get recommendations for unstable plans
if not stability.is_stable:
    recommendations = monitor.get_stability_recommendations(stability)
    for rec in recommendations:
        print(f"Recommendation: {rec}")
```

## Security Considerations

### Query Injection Prevention

```python
from query_optimization import QueryValidator, InjectionDetector

validator = QueryValidator()
detector = InjectionDetector()

# Validate query before execution
query = "SELECT * FROM users WHERE id = ?"
is_valid = validator.validate(query)
print(f"Query valid: {is_valid}")

# Detect injection attempts
suspicious_query = "SELECT * FROM users WHERE id = 1; DROP TABLE users;--"
is_injection = detector.detect(suspicious_query)
print(f"Injection detected: {is_injection}")

# Sanitize query
clean_query = validator.sanitize(suspicious_query)
print(f"Sanitized: {clean_query}")
```

### Query Audit Logging

```python
from query_optimization import QueryAuditor

auditor = QueryAuditor()

# Log query execution
auditor.log(
    query="SELECT * FROM sensitive_data WHERE user_id = ?",
    params=["123"],
    user="app_user",
    duration_ms=150,
    rows_returned=10,
    client_ip="10.0.0.1",
)

# Generate audit report
report = auditor.generate_report(
    start_date="2024-01-01",
    end_date="2024-01-31",
    filter_by_user="app_user",
)

print(f"Total queries: {report.total_queries}")
print(f"Slow queries: {report.slow_queries}")
print(f"Failed queries: {report.failed_queries}")
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Full table scans | Sequential Scan in plan | Add appropriate indexes |
| Hash join spill | High memory usage | Increase work_mem, optimize join |
| Nested loop inefficiency | High row estimates | Consider hash join, add indexes |
| Stale statistics | Inaccurate row estimates | Run ANALYZE on table |
| Plan regression | Performance degradation | Use plan hints, check statistics |

### Diagnostic Queries

```sql
-- Find queries with high I/O
SELECT
    query,
    calls,
    total_exec_time,
    shared_blks_read,
    shared_blks_hit,
    ROUND(shared_blks_hit::float / NULLIF(shared_blks_hit + shared_blks_read, 0) * 100, 2) AS hit_ratio
FROM pg_stat_statements
ORDER BY shared_blks_read DESC
LIMIT 10;

-- Find queries with high CPU usage
SELECT
    query,
    calls,
    total_exec_time,
    ROUND(total_exec_time / calls, 2) AS avg_time
FROM pg_stat_statements
WHERE calls > 100
ORDER BY total_exec_time DESC
LIMIT 10;

-- Check index usage
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;

-- Check table bloat
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS total_size,
    n_dead_tup,
    n_live_tup,
    ROUND(n_dead_tup::float / NULLIF(n_live_tup, 0) * 100, 2) AS dead_ratio
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

## API Reference

### PlanAnalyzer

```python
class PlanAnalyzer:
    def __init__(self, cost_model: CostModel = CostModel.POSTGRESQL_15)
    def parse_explain(self, explain_output: str) -> ExecutionPlan
    def analyze(self, plan: ExecutionPlan, deep: bool = False) -> PlanAnalysis
    def get_cost_breakdown(self, plan: ExecutionPlan) -> dict[str, float]
    def compare_plans(self, plan1: ExecutionPlan, plan2: ExecutionPlan) -> PlanComparison
    def suggest_indexes(self, plan: ExecutionPlan) -> list[IndexRecommendation]
    def visualize(self, plan: ExecutionPlan) -> str
```

### IndexRecommender

```python
class IndexRecommender:
    def __init__(self)
    def analyze(self, queries: list[str]) -> list[IndexRecommendation]
    def analyze_workload(self, workload: list[dict]) -> list[IndexRecommendation]
    def check_duplicate_indexes(self, indexes: list[str]) -> list[DuplicateIndex]
    def estimate_size(self, index_def: str, table_stats: TableStats) -> float
    def validate_index(self, index_def: str) -> ValidationResult
```

### QueryRewriter

```python
class QueryRewriter:
    def __init__(self, strategies: list[RewriteStrategy] = None)
    def rewrite(self, query: str) -> RewriteResult
    def rewrite_with_stats(self, query: str, stats: QueryStats) -> RewriteResult
    def apply_strategy(self, query: str, strategy: RewriteStrategy) -> str
    def get_available_strategies(self) -> list[RewriteStrategy]
```

### QueryBenchmark

```python
class QueryBenchmark:
    def __init__(self, database: str)
    def run(self, query: str, params: list = None, iterations: int = 100, concurrency: int = 1) -> BenchmarkResult
    def compare(self, result1: BenchmarkResult, result2: BenchmarkResult) -> ComparisonResult
    def get_statistics(self, result: BenchmarkResult) -> BenchmarkStats
    def export_results(self, result: BenchmarkResult, format: str = "json") -> str
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum

class PlanNodeType(Enum):
    SEQ_SCAN = "Seq Scan"
    INDEX_SCAN = "Index Scan"
    INDEX_ONLY_SCAN = "Index Only Scan"
    BITMAP_HEAP_SCAN = "Bitmap Heap Scan"
    BITMAP_INDEX_SCAN = "Bitmap Index Scan"
    NESTED_LOOP = "Nested Loop"
    HASH_JOIN = "Hash Join"
    MERGE_JOIN = "Merge Join"
    HASH = "Hash"
    SORT = "Sort"
    AGGREGATE = "Aggregate"
    LIMIT = "Limit"

class JoinType(Enum):
    NESTED_LOOP = "Nested Loop"
    HASH_JOIN = "Hash Join"
    MERGE_JOIN = "Merge Join"

@dataclass
class ExecutionPlan:
    root_node: PlanNode
    planning_time_ms: float
    execution_time_ms: float
    total_cost: float
    actual_rows: int

@dataclass
class PlanNode:
    node_type: PlanNodeType
    relation_name: Optional[str]
    cost: float
    rows: int
    width: int
    actual_time_ms: float
    actual_rows: int
    loops: int
    children: List['PlanNode'] = field(default_factory=list)
    filters: List[str] = field(default_factory=list)

@dataclass
class IndexRecommendation:
    index_definition: str
    estimated_improvement: float
    size_estimate_mb: float
    queries_affected: List[str]
    maintenance_cost: str

@dataclass
class BenchmarkResult:
    query: str
    iterations: int
    qps: float
    latency_p50_ms: float
    latency_p95_ms: float
    latency_p99_ms: float
    error_rate: float
    total_time_ms: float
```

## Deployment Guide

### Installation

```bash
# Install via pip
pip install query-optimization

# Install with database support
pip install query-optimization[postgresql,mysql]

# Development installation
pip install -e ".[dev]"
```

### Configuration

```python
# query_optimization_config.py
from query_optimization import Config

config = Config(
    # Database connection
    database_url="postgresql://user:pass@localhost:5432/db",
    
    # Query thresholds
    slow_query_threshold_ms=1000,
    very_slow_query_threshold_ms=5000,
    
    # Analysis settings
    enable_deep_analysis=True,
    max_plan_nodes=1000,
    
    # Caching
    enable_plan_cache=True,
    plan_cache_ttl_seconds=300,
    
    # Logging
    log_level="INFO",
    log_slow_queries=True,
    log_plans=True,
)
```

## Monitoring & Observability

### Query Performance Metrics

```python
from query_optimization import MetricsCollector

collector = MetricsCollector()

# Collect query metrics
collector.gauge("query.optimization.plan_cache_hit_rate", hit_rate)
collector.histogram("query.optimization.analysis_duration_ms", duration)
collector.counter("query.optimization.slow_queries_total", count)

# Collect index metrics
collector.gauge("query.optimization.index_hit_ratio", index_ratio)
collector.gauge("query.optimization.index_size_mb", index_size)
collector.counter("query.optimization.index_recommendations_total", rec_count)
```

### Dashboard Configuration

```json
{
  "title": "Query Optimization Dashboard",
  "panels": [
    {
      "title": "Query Performance",
      "type": "graph",
      "targets": [
        "query_duration_p50",
        "query_duration_p95",
        "query_duration_p99"
      ]
    },
    {
      "title": "Index Hit Ratio",
      "type": "gauge",
      "targets": ["index_hit_ratio"],
      "thresholds": {
        "warning": 95,
        "critical": 90
      }
    },
    {
      "title": "Slow Queries",
      "type": "timeseries",
      "targets": ["rate(slow_queries_total[5m])"]
    }
  ]
}
```

## Testing Strategy

### Unit Tests

```python
import pytest
from query_optimization import PlanAnalyzer, QueryRewriter

@pytest.fixture
def analyzer():
    return PlanAnalyzer()

def test_parse_explain(analyzer):
    explain = """
    Seq Scan on users  (cost=0.00..10.00 rows=1000 width=50)
      Filter: (active = true)
    """
    plan = analyzer.parse_explain(explain)
    assert plan.root_node.node_type == PlanNodeType.SEQ_SCAN
    assert plan.root_node.rows == 1000

def test_rewrite_subquery():
    rewriter = QueryRewriter()
    query = "SELECT * FROM orders WHERE customer_id IN (SELECT id FROM customers WHERE region = 'US')"
    result = rewriter.rewrite(query)
    assert "JOIN" in result.rewritten_query.upper()
```

### Integration Tests

```python
@pytest.mark.integration
def test_query_analysis():
    analyzer = PlanAnalyzer(database_url="postgresql://localhost/test")
    
    # Run query and get plan
    plan = analyzer.get_plan("SELECT * FROM users WHERE active = true")
    
    # Analyze plan
    analysis = analyzer.analyze(plan)
    
    assert analysis.total_cost > 0
    assert analysis.actual_time_ms > 0
```

## Versioning & Migration

### Version Compatibility

| Version | PostgreSQL | MySQL | SQLite |
|---------|------------|-------|--------|
| 3.0.x | 12+ | 8.0+ | 3.35+ |
| 2.5.x | 11+ | 5.7+ | 3.25+ |
| 2.0.x | 10+ | 5.6+ | 3.20+ |

### Migration Path

```python
from query_optimization import MigrationManager

migration = MigrationManager()

# Check current version
current = migration.current_version()
print(f"Current version: {current}")

# Get migration path
path = migration.get_migration_path(
    from_version="2.5.0",
    to_version="3.0.0"
)

for step in path:
    print(f"Step: {step.description}")
    print(f"  Breaking changes: {step.breaking_changes}")
    print(f"  Migration script: {step.script_path}")
```

## Glossary

| Term | Definition |
|------|------------|
| **Execution Plan** | Database's strategy for executing a query |
| **Seq Scan** | Sequential scan of entire table |
| **Index Scan** | Scan using an index to find rows |
| **Nested Loop** | Join algorithm using nested iteration |
| **Hash Join** | Join algorithm using hash table |
| **Merge Join** | Join algorithm using sorted inputs |
| **Selectivity** | Fraction of rows matching a predicate |
| **Cardinality** | Estimated number of rows |
| **Cost** | Estimated resource consumption |
| **QPS** | Queries Per Second |

## Changelog

### Version 3.0.0 (2024-01-15)
- Added deep execution plan analysis
- New selectivity estimation engine
- Improved query rewriting strategies
- Added plan stability monitoring

### Version 2.5.0 (2023-12-01)
- Added MySQL support
- New index recommendation algorithm
- Improved benchmarking tools
- Added query caching integration

### Version 2.0.0 (2023-09-15)
- Major API redesign
- Added PostgreSQL 15 support
- New cost model implementations
- Improved visualization tools

## Contributing Guidelines

### Development Setup

```bash
# Clone the repository
git clone https://github.com/awesome-grok/query-optimization.git
cd query-optimization

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run type checking
mypy .
```

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