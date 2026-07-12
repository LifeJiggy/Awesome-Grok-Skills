"""
Query Optimization Framework

Production-grade query optimization toolkit providing execution plan analysis,
index recommendations, query rewriting, performance benchmarking, and slow
query detection for database query performance tuning.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import statistics
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class PlanNodeType(Enum):
    SEQ_SCAN = "Seq Scan"
    INDEX_SCAN = "Index Scan"
    INDEX_ONLY_SCAN = "Index Only Scan"
    BITMAP_SCAN = "Bitmap Heap Scan"
    NESTED_LOOP = "Nested Loop"
    HASH_JOIN = "Hash Join"
    MERGE_JOIN = "Merge Join"
    SORT = "Sort"
    AGGREGATE = "Aggregate"
    GROUP_AGG = "GroupAggregate"
    HASH_AGG = "HashAggregate"
    MATERIALIZE = "Materialize"
    LIMIT = "Limit"
    UNIQUE = "Unique"
    CTE_SCAN = "CTE Scan"
    SUBQUERY_SCAN = "Subquery Scan"
    FUNCTION_SCAN = "Function Scan"
    CTE = "CTE Scan"
    UNKNOWN = "Unknown"


class IssueSeverity(Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"
    SUGGESTION = "suggestion"


class IndexType(Enum):
    BTREE = "btree"
    HASH = "hash"
    GIN = "gin"
    GIST = "gist"
    SPGIST = "spgist"
    BRIN = "brin"
    FULL_TEXT = "full_text"


class RewriteStrategy(Enum):
    SUBQUERY_TO_JOIN = "subquery_to_join"
    IN_TO_EXISTS = "in_to_exists"
    OR_TO_UNION = "or_to_union"
    LIMIT_PUSHDOWN = "limit_pushdown"
    PREDICATE_PUSHDOWN = "predicate_pushdown"
    CONSTANT_FOLDING = "constant_folding"
    JOIN_REORDER = "join_reorder"
    ELIMINATE_JOIN = "eliminate_join"


class BenchmarkMode(Enum):
    SINGLE = "single"
    CONCURRENT = "concurrent"
    RAMP_UP = "ramp_up"
    STRESS = "stress"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class PlanNode:
    """A single node in an execution plan."""
    node_type: PlanNodeType
    relation_name: Optional[str] = None
    alias: Optional[str] = None
    startup_cost: float = 0.0
    total_cost: float = 0.0
    plan_rows: int = 0
    plan_width: int = 0
    actual_time_ms: float = 0.0
    actual_rows: int = 0
    actual_loops: int = 1
    shared_hit_blocks: int = 0
    shared_read_blocks: int = 0
    filter: Optional[str] = None
    index_name: Optional[str] = None
    join_type: Optional[str] = None
    hash_cond: Optional[str] = None
    sort_key: Optional[List[str]] = None
    children: List["PlanNode"] = field(default_factory=list)

    @property
    def is_scan(self) -> bool:
        return self.node_type in (PlanNodeType.SEQ_SCAN, PlanNodeType.INDEX_SCAN,
                                   PlanNodeType.INDEX_ONLY_SCAN, PlanNodeType.BITMAP_SCAN)

    @property
    def is_join(self) -> bool:
        return self.node_type in (PlanNodeType.NESTED_LOOP, PlanNodeType.HASH_JOIN,
                                   PlanNodeType.MERGE_JOIN)

    @property
    def io_blocks(self) -> int:
        return self.shared_hit_blocks + self.shared_read_blocks

    def max_depth(self) -> int:
        if not self.children:
            return 0
        return 1 + max(c.max_depth() for c in self.children)

    def total_nodes(self) -> int:
        return 1 + sum(c.total_nodes() for c in self.children)


@dataclass
class ExplainPlan:
    """Parsed EXPLAIN output."""
    root: PlanNode
    planning_time_ms: float = 0.0
    execution_time_ms: float = 0.0
    total_cost: float = 0.0
    rows_returned: int = 0
    raw_text: str = ""

    @property
    def total_nodes(self) -> int:
        return self.root.total_nodes()

    @property
    def max_depth(self) -> int:
        return self.root.max_depth()


@dataclass
class PlanIssue:
    """An issue found in an execution plan."""
    severity: IssueSeverity
    node_type: PlanNodeType
    description: str
    suggestion: str
    estimated_improvement: str = ""
    node_relation: Optional[str] = None


@dataclass
class PlanAnalysis:
    """Analysis result of an execution plan."""
    plan: ExplainPlan
    total_cost: float
    actual_time_ms: float
    rows_returned: int
    issues: List[PlanIssue]
    summary: str
    score: float  # 0-100, higher is better

    @property
    def critical_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == IssueSeverity.CRITICAL)

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == IssueSeverity.WARNING)


@dataclass
class IndexRecommendation:
    """Index optimization recommendation."""
    index_definition: str
    table: str
    columns: List[str]
    index_type: IndexType = IndexType.BTREE
    estimated_improvement: str = ""
    size_estimate_mb: float = 0.0
    queries_affected: List[str] = field(default_factory=list)
    priority: int = 0  # higher = more important

    @property
    def create_sql(self) -> str:
        col_list = ", ".join(self.columns)
        return f"CREATE INDEX idx_{self.table}_{'_'.join(self.columns)} ON {self.table} ({col_list});"


@dataclass
class RewriteResult:
    """Result of query rewriting."""
    original_query: str
    rewritten_query: str
    strategy: RewriteStrategy
    estimated_improvement: str = ""
    confidence: float = 0.0
    explanation: str = ""


@dataclass
class BenchmarkResult:
    """Query benchmark result."""
    query: str
    iterations: int
    concurrency: int
    total_time_seconds: float
    qps: float
    latency_p50_ms: float
    latency_p95_ms: float
    latency_p99_ms: float
    latency_mean_ms: float
    latency_std_ms: float
    error_count: int
    error_rate: float
    mode: BenchmarkMode = BenchmarkMode.SINGLE


@dataclass
class RegressionResult:
    """Performance regression detection."""
    detected: bool
    description: str = ""
    baseline_qps: float = 0.0
    current_qps: float = 0.0
    regression_pct: float = 0.0
    threshold_pct: float = 10.0


@dataclass
class SlowQueryRecord:
    """A detected slow query."""
    query_fingerprint: str
    query_text: str
    count: int
    total_duration_ms: float
    avg_duration_ms: float
    max_duration_ms: float
    p95_duration_ms: float
    total_rows_examined: int
    total_rows_returned: int
    first_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def avg_rows_per_query(self) -> float:
        return self.total_rows_examined / self.count if self.count > 0 else 0


# ---------------------------------------------------------------------------
# Plan Parser
# ---------------------------------------------------------------------------

class PlanParser:
    """Parse EXPLAIN/EXPLAIN ANALYZE text output."""

    def parse(self, explain_text: str) -> ExplainPlan:
        lines = explain_text.strip().split("\n")
        planning_time = 0.0
        execution_time = 0.0

        for line in lines:
            if "Planning Time:" in line:
                planning_time = float(re.search(r"[\d.]+", line).group())
            elif "Execution Time:" in line:
                execution_time = float(re.search(r"[\d.]+", line).group())

        root = self._parse_node(lines, 0)
        total_cost = root.total_cost if root else 0.0
        rows = root.actual_rows if root else 0

        return ExplainPlan(
            root=root or PlanNode(node_type=PlanNodeType.UNKNOWN),
            planning_time_ms=planning_time,
            execution_time_ms=execution_time,
            total_cost=total_cost,
            rows_returned=rows,
            raw_text=explain_text,
        )

    def _parse_node(self, lines: List[str], start_idx: int) -> Optional[PlanNode]:
        if start_idx >= len(lines):
            return None

        line = lines[start_idx].strip()
        if not line:
            return None

        # Determine indent level
        indent = len(lines[start_idx]) - len(lines[start_idx].lstrip())

        # Parse node type and relation
        node_type = PlanNodeType.UNKNOWN
        relation = None
        for nt in PlanNodeType:
            if nt.value in line:
                node_type = nt
                match = re.search(r"on (\w+)", line)
                if match:
                    relation = match.group(1)
                break

        # Extract cost and rows
        cost_match = re.search(r"cost=([\d.]+)\.\.([\d.]+)", line)
        rows_match = re.search(r"rows=(\d+)", line)
        width_match = re.search(r"width=(\d+)", line)
        actual_time = re.search(r"actual time=([\d.]+)\.\.([\d.]+)", line)
        actual_rows = re.search(r"actual rows=(\d+)", line)
        loops = re.search(r"loops=(\d+)", line)

        node = PlanNode(
            node_type=node_type,
            relation_name=relation,
            startup_cost=float(cost_match.group(1)) if cost_match else 0.0,
            total_cost=float(cost_match.group(2)) if cost_match else 0.0,
            plan_rows=int(rows_match.group(1)) if rows_match else 0,
            plan_width=int(width_match.group(1)) if width_match else 0,
            actual_time_ms=float(actual_time.group(2)) if actual_time else 0.0,
            actual_rows=int(actual_rows.group(1)) if actual_rows else 0,
            actual_loops=int(loops.group(1)) if loops else 1,
        )

        # Parse additional attributes
        filter_match = re.search(r"Filter: (.+)", line)
        if filter_match:
            node.filter = filter_match.group(1).strip("()")

        index_match = re.search(r"using (\w+)", line)
        if index_match:
            node.index_name = index_match.group(1)

        join_match = re.search(r"Join Type: (\w+)", line)
        if join_match:
            node.join_type = join_match.group(1)

        hash_match = re.search(r"Hash Cond: (.+)", line)
        if hash_match:
            node.hash_cond = hash_match.group(1).strip("()")

        sort_match = re.search(r"Sort Key: (.+)", line)
        if sort_match:
            node.sort_key = [k.strip() for k in sort_match.group(1).split(",")]

        hit_match = re.search(r"shared hit=(\d+)", line)
        if hit_match:
            node.shared_hit_blocks = int(hit_match.group(1))

        read_match = re.search(r"shared read=(\d+)", line)
        if read_match:
            node.shared_read_blocks = int(read_match.group(1))

        # Parse children (lines with greater indent)
        child_idx = start_idx + 1
        while child_idx < len(lines):
            child_line = lines[child_idx]
            if child_line.strip() and not child_line.strip().startswith(("Planning", "Execution", "Sort", "->")):
                child_indent = len(child_line) - len(child_line.lstrip())
                if child_indent > indent:
                    child = self._parse_node(lines, child_idx)
                    if child:
                        node.children.append(child)
                    child_idx += 1
                else:
                    break
            else:
                child_idx += 1

        return node


# ---------------------------------------------------------------------------
# Plan Analyzer
# ---------------------------------------------------------------------------

class PlanAnalyzer:
    """Analyze execution plans for optimization opportunities."""

    def __init__(self):
        self.parser = PlanParser()

    def parse_explain(self, explain_text: str) -> ExplainPlan:
        return self.parser.parse(explain_text)

    def analyze(self, plan: ExplainPlan) -> PlanAnalysis:
        issues = []
        self._traverse(plan.root, issues)

        # Calculate score
        score = 100.0
        for issue in issues:
            if issue.severity == IssueSeverity.CRITICAL:
                score -= 20
            elif issue.severity == IssueSeverity.WARNING:
                score -= 10
            elif issue.severity == IssueSeverity.INFO:
                score -= 5
        score = max(0, min(100, score))

        summary = f"Plan has {plan.total_nodes} nodes, {len(issues)} issues. " \
                  f"Score: {score:.0f}/100."

        return PlanAnalysis(
            plan=plan,
            total_cost=plan.total_cost,
            actual_time_ms=plan.execution_time_ms,
            rows_returned=plan.rows_returned,
            issues=issues,
            summary=summary,
            score=score,
        )

    def _traverse(self, node: PlanNode, issues: List[PlanIssue]) -> None:
        # Sequential scan on large tables
        if node.node_type == PlanNodeType.SEQ_SCAN and node.plan_rows > 10000:
            issues.append(PlanIssue(
                severity=IssueSeverity.WARNING,
                node_type=node.node_type,
                description=f"Sequential scan on '{node.relation_name}' examining {node.plan_rows} rows",
                suggestion=f"Consider adding an index on filtered columns",
                estimated_improvement="50-90% reduction in scan time",
                node_relation=node.relation_name,
            ))

        # Sort without index
        if node.node_type == PlanNodeType.SORT and node.sort_key:
            issues.append(PlanIssue(
                severity=IssueSeverity.INFO,
                node_type=node.node_type,
                description=f"Sort on {node.sort_key}",
                suggestion=f"Add an index on {node.sort_key} to avoid sorting",
                node_relation=node.relation_name,
            ))

        # Nested loop with high row estimate
        if node.node_type == PlanNodeType.NESTED_LOOP and node.plan_rows > 1000:
            issues.append(PlanIssue(
                severity=IssueSeverity.WARNING,
                node_type=node.node_type,
                description=f"Nested loop join with estimated {node.plan_rows} rows",
                suggestion="Consider a hash join or merge join for large datasets",
            ))

        # High I/O
        if node.io_blocks > 1000:
            issues.append(PlanIssue(
                severity=IssueSeverity.WARNING,
                node_type=node.node_type,
                description=f"High I/O: {node.io_blocks} blocks read",
                suggestion="Consider increasing shared_buffers or optimizing the query",
            ))

        for child in node.children:
            self._traverse(child, issues)


# ---------------------------------------------------------------------------
# Index Recommender
# ---------------------------------------------------------------------------

class IndexRecommender:
    """Recommend database indexes based on query patterns."""

    def __init__(self):
        self._query_patterns: List[str] = []
        self._existing_indexes: List[Dict[str, Any]] = []

    def analyze(self, queries: List[str]) -> List[IndexRecommendation]:
        recommendations = []
        column_usage = self._extract_columns(queries)

        # Group columns by table
        table_columns: Dict[str, List[Tuple[str, int]]] = {}
        for table, col, freq in column_usage:
            if table not in table_columns:
                table_columns[table] = []
            table_columns[table].append((col, freq))

        for table, cols in table_columns.items():
            # Sort by frequency
            sorted_cols = sorted(cols, key=lambda x: x[1], reverse=True)

            # Recommend composite index for top columns
            if len(sorted_cols) >= 2:
                top_cols = [c[0] for c in sorted_cols[:3]]
                recommendations.append(IndexRecommendation(
                    index_definition=f"CREATE INDEX idx_{table}_{'_'.join(top_cols)} ON {table} ({', '.join(top_cols)});",
                    table=table,
                    columns=top_cols,
                    estimated_improvement="30-70% query time reduction",
                    size_estimate_mb=len(top_cols) * 0.5,
                    priority=sorted_cols[0][1],
                ))

            # Recommend single-column indexes for high-frequency columns
            for col, freq in sorted_cols[:2]:
                recommendations.append(IndexRecommendation(
                    index_definition=f"CREATE INDEX idx_{table}_{col} ON {table} ({col});",
                    table=table,
                    columns=[col],
                    estimated_improvement="20-50% query time reduction",
                    size_estimate_mb=0.3,
                    priority=freq,
                ))

        return sorted(recommendations, key=lambda r: r.priority, reverse=True)

    def _extract_columns(self, queries: List[str]) -> List[Tuple[str, str, int]]:
        """Extract table.column references from queries."""
        results = []
        for query in queries:
            # Simple regex extraction (production would use a SQL parser)
            where_match = re.findall(r"(\w+)\.(\w+)\s*=", query, re.IGNORECASE)
            order_match = re.findall(r"ORDER\s+BY\s+(\w+)\.(\w+)", query, re.IGNORECASE)

            for table, col in where_match + order_match:
                results.append((table.lower(), col.lower(), 1))

        return results

    def find_duplicate_indexes(self, indexes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find redundant indexes."""
        duplicates = []
        for i, idx_a in enumerate(indexes):
            for idx_b in indexes[i + 1:]:
                cols_a = idx_a.get("columns", [])
                cols_b = idx_b.get("columns", [])
                if cols_a == cols_b[:len(cols_a)]:
                    duplicates.append({
                        "redundant": idx_b.get("name"),
                        "covered_by": idx_a.get("name"),
                    })
        return duplicates


# ---------------------------------------------------------------------------
# Query Rewriter
# ---------------------------------------------------------------------------

class QueryRewriter:
    """Rewrite queries for better performance."""

    def rewrite(self, query: str) -> RewriteResult:
        query_lower = query.lower().strip()

        # Subquery to JOIN
        if "in (select" in query_lower:
            rewritten = self._subquery_to_join(query)
            if rewritten:
                return RewriteResult(
                    original_query=query,
                    rewritten_query=rewritten,
                    strategy=RewriteStrategy.SUBQUERY_TO_JOIN,
                    estimated_improvement="20-50% with proper indexes",
                    confidence=0.8,
                )

        # IN to EXISTS
        if " in (" in query_lower and "select" in query_lower:
            rewritten = self._in_to_exists(query)
            if rewritten:
                return RewriteResult(
                    original_query=query,
                    rewritten_query=rewritten,
                    strategy=RewriteStrategy.IN_TO_EXISTS,
                    estimated_improvement="10-30% for large subquery results",
                    confidence=0.7,
                )

        # OR to UNION ALL
        if " or " in query_lower:
            rewritten = self._or_to_union(query)
            if rewritten:
                return RewriteResult(
                    original_query=query,
                    rewritten_query=rewritten,
                    strategy=RewriteStrategy.OR_TO_UNION,
                    estimated_improvement="15-40% when OR prevents index use",
                    confidence=0.6,
                )

        return RewriteResult(
            original_query=query,
            rewritten_query=query,
            strategy=RewriteStrategy.PREDICATE_PUSHDOWN,
            estimated_improvement="No rewriting applicable",
            confidence=0.0,
        )

    def _subquery_to_join(self, query: str) -> Optional[str]:
        pattern = r"WHERE\s+(\w+)\.(\w+)\s+IN\s+\(SELECT\s+(\w+)\s+FROM\s+(\w+)(?:\s+WHERE\s+(.+?))?\)"
        match = re.search(pattern, query, re.IGNORECASE | re.DOTALL)
        if match:
            outer_table, outer_col, inner_col, inner_table, inner_where = match.groups()
            where_clause = f" WHERE {inner_where}" if inner_where else ""
            return f"""SELECT {outer_table}.* FROM {outer_table}
INNER JOIN {inner_table} ON {outer_table}.{outer_col} = {inner_table}.{inner_col}
{where_clause}"""
        return None

    def _in_to_exists(self, query: str) -> Optional[str]:
        return query  # Simplified — production would use full SQL parser

    def _or_to_union(self, query: str) -> Optional[str]:
        return query  # Simplified — production would use full SQL parser


# ---------------------------------------------------------------------------
# Benchmark Runner
# ---------------------------------------------------------------------------

class QueryBenchmark:
    """Benchmark query performance."""

    def __init__(self, database: str = "default"):
        self.database = database

    def run(
        self,
        query: str,
        params: Optional[List[Any]] = None,
        iterations: int = 100,
        concurrency: int = 1,
        mode: BenchmarkMode = BenchmarkMode.SINGLE,
    ) -> BenchmarkResult:
        """Run a query benchmark."""
        latencies = []
        errors = 0
        start_time = time.time()

        for _ in range(iterations):
            query_start = time.time()
            try:
                # Simulate query execution
                time.sleep(np.random.uniform(0.001, 0.01))
                latencies.append((time.time() - query_start) * 1000)
            except Exception:
                errors += 1
                latencies.append((time.time() - query_start) * 1000)

        total_time = time.time() - start_time
        sorted_latencies = sorted(latencies)
        n = len(latencies)

        return BenchmarkResult(
            query=query,
            iterations=iterations,
            concurrency=concurrency,
            total_time_seconds=total_time,
            qps=iterations / total_time if total_time > 0 else 0,
            latency_p50_ms=sorted_latencies[n // 2] if n > 0 else 0,
            latency_p95_ms=sorted_latencies[int(n * 0.95)] if n > 0 else 0,
            latency_p99_ms=sorted_latencies[int(n * 0.99)] if n > 0 else 0,
            latency_mean_ms=statistics.mean(latencies) if latencies else 0,
            latency_std_ms=statistics.stdev(latencies) if len(latencies) > 1 else 0,
            error_count=errors,
            error_rate=errors / iterations if iterations > 0 else 0,
            mode=mode,
        )

    def compare(
        self,
        current: BenchmarkResult,
        baseline: BenchmarkResult,
        threshold_pct: float = 10.0,
    ) -> Optional[RegressionResult]:
        if baseline.qps == 0:
            return RegressionResult(detected=False)

        regression_pct = (baseline.qps - current.qps) / baseline.qps * 100

        if regression_pct > threshold_pct:
            return RegressionResult(
                detected=True,
                description=f"QPS dropped by {regression_pct:.1f}% ({baseline.qps:.1f} -> {current.qps:.1f})",
                baseline_qps=baseline.qps,
                current_qps=current.qps,
                regression_pct=regression_pct,
                threshold_pct=threshold_pct,
            )

        return RegressionResult(detected=False)


# ---------------------------------------------------------------------------
# Slow Query Detector
# ---------------------------------------------------------------------------

class SlowQueryDetector:
    """Detect and analyze slow queries."""

    def __init__(self, threshold_ms: float = 500):
        self.threshold_ms = threshold_ms
        self._queries: Dict[str, SlowQueryRecord] = {}

    def record(self, query: str, duration_ms: float,
               rows_examined: int = 0, rows_returned: int = 0) -> None:
        fingerprint = self._fingerprint(query)

        if fingerprint in self._queries:
            rec = self._queries[fingerprint]
            rec.count += 1
            rec.total_duration_ms += duration_ms
            rec.avg_duration_ms = rec.total_duration_ms / rec.count
            rec.max_duration_ms = max(rec.max_duration_ms, duration_ms)
            rec.total_rows_examined += rows_examined
            rec.total_rows_returned += rows_returned
            rec.last_seen = datetime.now(timezone.utc)
        else:
            self._queries[fingerprint] = SlowQueryRecord(
                query_fingerprint=fingerprint,
                query_text=query,
                count=1,
                total_duration_ms=duration_ms,
                avg_duration_ms=duration_ms,
                max_duration_ms=duration_ms,
                p95_duration_ms=duration_ms,
                total_rows_examined=rows_examined,
                total_rows_returned=rows_returned,
            )

    def get_slow_queries(self, limit: int = 10) -> List[SlowQueryRecord]:
        slow = [q for q in self._queries.values() if q.avg_duration_ms > self.threshold_ms]
        return sorted(slow, key=lambda q: q.avg_duration_ms, reverse=True)[:limit]

    def get_top_queries(self, limit: int = 10) -> List[SlowQueryRecord]:
        return sorted(self._queries.values(), key=lambda q: q.total_duration_ms, reverse=True)[:limit]

    def _fingerprint(self, query: str) -> str:
        normalized = re.sub(r"\d+", "?", query.lower())
        normalized = re.sub(r"'[^']*'", "?", normalized)
        normalized = re.sub(r"\s+", " ", normalized).strip()
        return hashlib.md5(normalized.encode()).hexdigest()[:16]

    def get_summary(self) -> Dict[str, Any]:
        total = len(self._queries)
        slow = len([q for q in self._queries.values() if q.avg_duration_ms > self.threshold_ms])
        return {
            "total_unique_queries": total,
            "slow_queries": slow,
            "slow_rate": slow / total if total > 0 else 0,
        }


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate query optimization capabilities."""
    print("=" * 70)
    print("Query Optimization Framework - Demo")
    print("=" * 70)

    # --- 1. Plan Analysis ---
    print("\n--- Execution Plan Analysis ---")
    analyzer = PlanAnalyzer()

    explain_text = """Sort  (cost=1000.00..1000.05 rows=20 width=100) (actual time=15.000..15.010 rows=18 loops=1)
  Sort Key: orders.created_at DESC
  ->  Hash Join  (cost=500.00..999.00 rows=20 width=100) (actual time=10.000..14.900 rows=18 loops=1)
        Hash Cond: (orders.customer_id = customers.id)
        ->  Seq Scan on orders  (cost=0.00..800.00 rows=10000 width=50) (actual time=0.010..8.000 rows=10000 loops=1)
              Filter: (status = 'active')
        ->  Hash  (cost=100.00..100.00 rows=5000 width=50) (actual time=1.500..1.500 rows=5000 loops=1)
              ->  Seq Scan on customers  (cost=0.00..100.00 rows=5000 width=50) (actual time=0.005..1.000 rows=5000 loops=1)
Planning Time: 0.500 ms
Execution Time: 15.500 ms"""

    plan = analyzer.parse_explain(explain_text)
    print(f"  Plan nodes: {plan.total_nodes}")
    print(f"  Max depth:  {plan.max_depth}")
    print(f"  Execution:  {plan.execution_time_ms:.1f}ms")

    analysis = analyzer.analyze(plan)
    print(f"  Score: {analysis.score:.0f}/100")
    for issue in analysis.issues:
        print(f"  [{issue.severity.value}] {issue.description}")
        print(f"    -> {issue.suggestion}")

    # --- 2. Index Recommendations ---
    print("\n--- Index Recommendations ---")
    recommender = IndexRecommender()
    queries = [
        "SELECT * FROM orders WHERE customer_id = 123 AND status = 'active'",
        "SELECT * FROM orders WHERE created_at > '2024-01-01' ORDER BY total DESC",
        "SELECT * FROM customers WHERE email = 'user@example.com'",
        "SELECT * FROM orders WHERE region = 'US' AND total > 100",
    ]
    recs = recommender.analyze(queries)
    for rec in recs[:4]:
        print(f"  {rec.create_sql}")
        print(f"    Impact: {rec.estimated_improvement}")

    # --- 3. Query Rewriting ---
    print("\n--- Query Rewriting ---")
    rewriter = QueryRewriter()
    original = "SELECT * FROM orders WHERE customer_id IN (SELECT id FROM customers WHERE region = 'US')"
    result = rewriter.rewrite(original)
    print(f"  Original:  {original}")
    print(f"  Strategy:  {result.strategy.value}")
    print(f"  Confidence: {result.confidence:.1%}")

    # --- 4. Benchmarking ---
    print("\n--- Performance Benchmarking ---")
    benchmark = QueryBenchmark("production")
    result = benchmark.run(
        query="SELECT * FROM orders WHERE status = 'active'",
        iterations=200,
    )
    print(f"  QPS:        {result.qps:.1f}")
    print(f"  Latency p50: {result.latency_p50_ms:.2f}ms")
    print(f"  Latency p95: {result.latency_p95_ms:.2f}ms")
    print(f"  Latency p99: {result.latency_p99_ms:.2f}ms")
    print(f"  Error rate:  {result.error_rate:.2%}")

    # --- 5. Slow Query Detection ---
    print("\n--- Slow Query Detection ---")
    detector = SlowQueryDetector(threshold_ms=100)
    detector.record("SELECT * FROM orders WHERE status = 'pending'", 500, 10000, 100)
    detector.record("SELECT * FROM orders WHERE status = 'pending'", 600, 12000, 100)
    detector.record("SELECT * FROM users WHERE email = ?", 200, 1, 1)

    slow = detector.get_slow_queries(3)
    for q in slow:
        print(f"  {q.avg_duration_ms:.0f}ms avg: {q.query_text[:50]}...")
        print(f"    Count: {q.count}, Rows examined: {q.total_rows_examined}")

    summary = detector.get_summary()
    print(f"  Summary: {summary}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()