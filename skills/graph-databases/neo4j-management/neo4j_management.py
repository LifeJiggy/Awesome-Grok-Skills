"""
Neo4j Database Management Toolkit

Operational utilities for Neo4j administration: index management,
query optimization, cluster monitoring, backup orchestration, and
performance analysis.
"""

from __future__ import annotations

import json
import time
import logging
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Domain Enums
# ---------------------------------------------------------------------------

class IndexType(Enum):
    B_TREE = auto()
    FULL_TEXT = auto()
    RANGE = auto()
    POINT = auto()
    COMPOSITE = auto()

    def to_cypher_label(self) -> str:
        mapping = {
            IndexType.B_TREE: "btree",
            IndexType.FULL_TEXT: "fulltext",
            IndexType.RANGE: "range",
            IndexType.POINT: "point",
            IndexType.COMPOSITE: "composite",
        }
        return mapping[self]


class ClusterRole(Enum):
    LEADER = "leader"
    FOLLOWER = "follower"
    READ_REPLICA = "read_replica"
    CORE = "core"


class QueryStatus(Enum):
    RUNNING = auto()
    WAITING = auto()
    IDLE = auto()
    FAILED = auto()
    COMPLETED = auto()


class BackupStrategy(Enum):
    FULL = auto()
    INCREMENTAL = auto()
    DIFFERENTIAL = auto()


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class IndexDefinition:
    name: str
    label: str
    properties: list[str]
    index_type: IndexType
    created_at: datetime = field(default_factory=datetime.now)
    size_bytes: int = 0
    query_count: int = 0
    uniqueness: bool = False

    def to_cypher(self) -> str:
        props = ", ".join(self.properties)
        unique = "UNIQUE " if self.uniqueness else ""
        if self.index_type == IndexType.FULL_TEXT:
            return f"CREATE {self.index_type.to_cypher_label()} INDEX {self.name} FOR (n:{self.label}) ON EACH [{props}]"
        return f"CREATE {unique}{self.index_type.to_cypher_label()} INDEX {self.name} FOR (n:{self.label}) ON ({props})"


@dataclass
class QueryProfile:
    query: str
    execution_time_ms: float
    db_hits: int = 0
    rows_produced: int = 0
    status: QueryStatus = QueryStatus.RUNNING
    plan: dict[str, Any] = field(default_factory=dict)
    memory_bytes: int = 0

    @property
    def avg_cost_per_row(self) -> float:
        if self.rows_produced == 0:
            return 0.0
        return self.db_hits / self.rows_produced


@dataclass
class ClusterNode:
    id: str
    role: ClusterRole
    address: str
    bolt_port: int = 7687
    http_port: int = 7474
    uptime_seconds: int = 0
    is_alive: bool = True
    version: str = "5.x"
    used_memory_mb: float = 0
    committed_memory_mb: float = 0

    @property
    def uptime_human(self) -> str:
        delta = timedelta(seconds=self.uptime_seconds)
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        if days > 0:
            return f"{days}d {hours}h"
        return f"{hours}h {minutes}m"


@dataclass
class BackupRecord:
    backup_id: str
    strategy: BackupStrategy
    database: str
    path: str
    size_bytes: int
    created_at: datetime = field(default_factory=datetime.now)
    duration_seconds: float = 0
    verified: bool = False
    checksum: str = ""

    @property
    def size_human(self) -> str:
        gb = self.size_bytes / (1024 ** 3)
        if gb >= 1:
            return f"{gb:.1f} GB"
        mb = self.size_bytes / (1024 ** 2)
        return f"{mb:.1f} MB"


@dataclass
class ServerConfig:
    heap_initial_size: str = "4G"
    heap_max_size: str = "4G"
    pagecache_size: str = "8G"
    transaction_total_max: str = "4G"
    query_memory_limit: str = "2G"
    bolt_listen_address: str = "0.0.0.0:7687"
    http_listen_address: str = "0.0.0.0:7474"
    auth_enabled: bool = True
    metrics_enabled: bool = False
    prometheus_enabled: bool = False
    ssl_bolt_enabled: bool = False


# ---------------------------------------------------------------------------
# Index Manager
# ---------------------------------------------------------------------------

class IndexManager:
    """Manages Neo4j indexes: creation, monitoring, and cleanup."""

    def __init__(self) -> None:
        self._indexes: dict[str, IndexDefinition] = {}

    def create_btree_index(self, name: str, label: str,
                           properties: list[str], unique: bool = False) -> IndexDefinition:
        idx = IndexDefinition(
            name=name, label=label, properties=properties,
            index_type=IndexType.B_TREE, uniqueness=unique,
        )
        self._indexes[name] = idx
        logger.info("Created B-tree index: %s", name)
        return idx

    def create_fulltext_index(self, name: str, label: str,
                              properties: list[str]) -> IndexDefinition:
        idx = IndexDefinition(
            name=name, label=label, properties=properties,
            index_type=IndexType.FULL_TEXT,
        )
        self._indexes[name] = idx
        logger.info("Created fulltext index: %s", name)
        return idx

    def create_range_index(self, name: str, label: str,
                           properties: list[str]) -> IndexDefinition:
        idx = IndexDefinition(
            name=name, label=label, properties=properties,
            index_type=IndexType.RANGE,
        )
        self._indexes[name] = idx
        logger.info("Created range index: %s", name)
        return idx

    def drop_index(self, name: str) -> bool:
        if name in self._indexes:
            del self._indexes[name]
            logger.info("Dropped index: %s", name)
            return True
        logger.warning("Index not found: %s", name)
        return False

    def list_indexes(self) -> list[IndexDefinition]:
        return list(self._indexes.values())

    def find_unused(self, min_queries: int = 1) -> list[IndexDefinition]:
        return [i for i in self._indexes.values() if i.query_count < min_queries]

    def get_size_report(self) -> dict[str, int]:
        report: dict[str, int] = {}
        for idx in self._indexes.values():
            report[idx.name] = idx.size_bytes
        return report

    def generate_migration_statements(self, from_version: str, to_version: str) -> list[str]:
        statements: list[str] = []
        if from_version.startswith("4.") and to_version.startswith("5."):
            statements.append("CALL db.index.fulltext.awaitIndexes()")
            for idx in self._indexes.values():
                statements.append(f"CALL db.index.fulltext.drop('{idx.name}')")
                statements.append(idx.to_cypher())
        return statements


# ---------------------------------------------------------------------------
# Query Analyzer
# ---------------------------------------------------------------------------

class QueryAnalyzer:
    """Tracks and analyzes Neo4j query performance."""

    def __init__(self, slow_query_threshold_ms: float = 1000.0) -> None:
        self._slow_threshold_ms = slow_query_threshold_ms
        self._profiles: list[QueryProfile] = []
        self._query_stats: dict[str, dict[str, Any]] = defaultdict(
            lambda: {"count": 0, "total_ms": 0.0, "max_ms": 0.0}
        )

    def record(self, profile: QueryProfile) -> None:
        self._profiles.append(profile)
        stats = self._query_stats[profile.query[:100]]
        stats["count"] += 1
        stats["total_ms"] += profile.execution_time_ms
        stats["max_ms"] = max(stats["max_ms"], profile.execution_time_ms)

    def slow_queries(self, limit: int = 10) -> list[QueryProfile]:
        sorted_profiles = sorted(
            self._profiles, key=lambda p: p.execution_time_ms, reverse=True
        )
        return [p for p in sorted_profiles if p.execution_time_ms > self._slow_threshold_ms][:limit]

    def aggregate_stats(self) -> dict[str, dict[str, Any]]:
        result: dict[str, dict[str, Any]] = {}
        for query_prefix, stats in self._query_stats.items():
            count = stats["count"]
            result[query_prefix] = {
                "count": count,
                "avg_ms": stats["total_ms"] / count if count else 0,
                "max_ms": stats["max_ms"],
                "total_ms": stats["total_ms"],
            }
        return result

    def suggest_indexes(self) -> list[str]:
        suggestions: list[str] = []
        for profile in self._slow_queries(5):
            if "WHERE" in profile.query:
                suggestions.append(
                    f"Consider adding an index for query: {profile.query[:80]}..."
                )
        return suggestions

    def detect_cartesian_products(self, query: str) -> bool:
        match_count = query.upper().count("MATCH")
        return_count = query.upper().count("RETURN")
        where_clauses = query.upper().count("WHERE")
        return match_count > 1 and where_clauses == 0


# ---------------------------------------------------------------------------
# Cluster Monitor
# ---------------------------------------------------------------------------

class ClusterMonitor:
    """Monitors Neo4j cluster topology and health."""

    def __init__(self) -> None:
        self._nodes: dict[str, ClusterNode] = {}

    def register_node(self, node: ClusterNode) -> None:
        self._nodes[node.id] = node
        logger.info("Registered cluster node: %s (%s)", node.id, node.role.value)

    def get_leader(self) -> Optional[ClusterNode]:
        for node in self._nodes.values():
            if node.role == ClusterRole.LEADER and node.is_alive:
                return node
        return None

    def get_read_replicas(self) -> list[ClusterNode]:
        return [n for n in self._nodes.values()
                if n.role == ClusterRole.READ_REPLICA and n.is_alive]

    def health_check(self) -> dict[str, Any]:
        alive = sum(1 for n in self._nodes.values() if n.is_alive)
        total = len(self._nodes)
        return {
            "total_nodes": total,
            "alive_nodes": alive,
            "dead_nodes": total - alive,
            "has_quorum": alive > total / 2,
            "leader_elected": self.get_leader() is not None,
        }

    def memory_usage_report(self) -> dict[str, dict[str, float]]:
        report: dict[str, dict[str, float]] = {}
        for nid, node in self._nodes.items():
            report[nid] = {
                "used_mb": node.used_memory_mb,
                "committed_mb": node.committed_memory_mb,
                "utilization_pct": (
                    (node.used_memory_mb / node.committed_memory_mb * 100)
                    if node.committed_memory_mb > 0 else 0
                ),
            }
        return report

    def detect_split_brain(self) -> bool:
        leaders = [n for n in self._nodes.values()
                   if n.role == ClusterRole.LEADER and n.is_alive]
        return len(leaders) > 1

    def get_cluster_summary(self) -> dict[str, Any]:
        roles: dict[str, int] = defaultdict(int)
        for node in self._nodes.values():
            if node.is_alive:
                roles[node.role.value] += 1
        return dict(roles)


# ---------------------------------------------------------------------------
# Backup Manager
# ---------------------------------------------------------------------------

class BackupManager:
    """Orchestrates Neo4j backup and restore operations."""

    def __init__(self, backup_dir: str = "/backups/neo4j") -> None:
        self._backup_dir = backup_dir
        self._records: list[BackupRecord] = []
        self._counter = 0

    def create_backup_id(self) -> str:
        self._counter += 1
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"backup_{ts}_{self._counter:04d}"

    def record_backup(self, strategy: BackupStrategy, database: str,
                      size_bytes: int, duration: float) -> BackupRecord:
        record = BackupRecord(
            backup_id=self.create_backup_id(),
            strategy=strategy,
            database=database,
            path=f"{self._backup_dir}/{database}",
            size_bytes=size_bytes,
            duration_seconds=duration,
        )
        self._records.append(record)
        return record

    def latest_backup(self, database: str) -> Optional[BackupRecord]:
        db_backups = [r for r in self._records if r.database == database]
        if not db_backups:
            return None
        return max(db_backups, key=lambda r: r.created_at)

    def verify_backup(self, backup_id: str) -> bool:
        for record in self._records:
            if record.backup_id == backup_id:
                record.verified = True
                logger.info("Verified backup: %s", backup_id)
                return True
        return False

    def needs_backup(self, database: str, max_age_hours: int = 24) -> bool:
        latest = self.latest_backup(database)
        if latest is None:
            return True
        age = datetime.now() - latest.created_at
        return age.total_seconds() > max_age_hours * 3600

    def generate_restore_commands(self, backup_id: str) -> list[str]:
        for record in self._records:
            if record.backup_id == backup_id:
                return [
                    f"neo4j-admin database stop {record.database}",
                    f"neo4j-admin database restore --from={record.path} --to={record.database}",
                    f"neo4j-admin database start {record.database}",
                ]
        return []

    def cleanup_old_backups(self, keep_days: int = 30) -> list[str]:
        cutoff = datetime.now() - timedelta(days=keep_days)
        removed: list[str] = []
        remaining: list[BackupRecord] = []
        for record in self._records:
            if record.created_at < cutoff:
                removed.append(record.backup_id)
            else:
                remaining.append(record)
        self._records = remaining
        return removed


# ---------------------------------------------------------------------------
# Performance Tuner
# ---------------------------------------------------------------------------

class PerformanceTuner:
    """Analyzes and suggests Neo4j performance optimizations."""

    def __init__(self, config: Optional[ServerConfig] = None) -> None:
        self._config = config or ServerConfig()

    def analyze_heap_size(self) -> str:
        return (
            f"Heap: {self._config.heap_initial_size} initial, "
            f"{self._config.heap_max_size} max. "
            "Set initial = max to avoid GC pauses during resize."
        )

    def analyze_pagecache(self) -> str:
        return (
            f"Page cache: {self._config.pagecache_size}. "
            "Should be >= 10% of graph size for working set to fit."
        )

    def connection_pool_advice(self, peak_concurrent: int) -> dict[str, Any]:
        recommended = max(peak_concurrent * 2, 100)
        return {
            "current_pool_size": peak_concurrent,
            "recommended_pool_size": recommended,
            "connection_timeout": "30s",
            "validation_query": "RETURN 1",
        }

    def transaction_advice(self, avg_query_count_per_tx: int) -> dict[str, Any]:
        if avg_query_count_per_tx > 50:
            return {
                "split_transactions": True,
                "reason": "Transaction too large; split into smaller transactions.",
            }
        return {
            "split_transactions": False,
            "reason": "Transaction size acceptable.",
        }

    def generate_config(self, workload_type: str = "mixed") -> ServerConfig:
        configs = {
            "read_heavy": ServerConfig(
                heap_initial_size="6G", heap_max_size="6G",
                pagecache_size="16G", transaction_total_max="4G",
                query_memory_limit="4G",
            ),
            "write_heavy": ServerConfig(
                heap_initial_size="8G", heap_max_size="8G",
                pagecache_size="8G", transaction_total_max="8G",
                query_memory_limit="2G",
            ),
            "mixed": ServerConfig(),
        }
        return configs.get(workload_type, ServerConfig())

    def memory_recommendation(self, graph_size_gb: float) -> dict[str, str]:
        pagecache = max(graph_size_gb * 1.1, 4)
        heap = max(graph_size_gb * 0.5, 2)
        return {
            "pagecache": f"{pagecache:.1f}G",
            "heap": f"{heap:.1f}G",
            "transaction_total_max": f"{heap:.1f}G",
            "note": "Page cache >= 110% of graph size for optimal performance.",
        }


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 70)
    print("NEO4J MANAGEMENT TOOLKIT DEMO")
    print("=" * 70)

    # Index Management
    print("\n--- Index Management ---")
    idx_mgr = IndexManager()
    idx_mgr.create_btree_index("person_email", "Person", ["email"], unique=True)
    idx_mgr.create_btree_index("person_age", "Person", ["age"])
    idx_mgr.create_fulltext_index("person_search", "Person", ["name", "bio"])
    idx_mgr.create_range_index("event_ts", "Event", ["timestamp"])

    for idx in idx_mgr.list_indexes():
        print(f"  {idx.name}: {idx.to_cypher()}")

    print("\n  Unused indexes:", [i.name for i in idx_mgr.find_unused()])

    # Query Analysis
    print("\n--- Query Analysis ---")
    analyzer = QueryAnalyzer(slow_query_threshold_ms=500)
    analyzer.record(QueryProfile("MATCH (n) RETURN n", 1200.0, db_hits=50000, rows_produced=10000))
    analyzer.record(QueryProfile("MATCH (n:Person) WHERE n.age > 25 RETURN n", 300.0, db_hits=1200, rows_produced=200))
    analyzer.record(QueryProfile("MATCH (a)-[*]->(b) RETURN a, b", 5000.0, db_hits=1000000, rows_produced=50000))
    analyzer.record(QueryProfile("MATCH (n) WHERE n.name = 'test' RETURN n", 800.0, db_hits=30000, rows_produced=5))

    print("  Slow queries:", len(analyzer.slow_queries()))
    for q in analyzer.slow_queries(3):
        print(f"    [{q.execution_time_ms:.0f}ms] {q.query[:60]}...")

    print("  Aggregate stats:")
    for query, stats in analyzer.aggregate_stats().items():
        print(f"    {query[:50]}: {stats['count']}x, avg={stats['avg_ms']:.0f}ms")

    has_cartesian = analyzer.detect_cartesian_products(
        "MATCH (a:Person), (b:Person) RETURN a, b"
    )
    print(f"  Cartesian product detected: {has_cartesian}")

    # Cluster Monitoring
    print("\n--- Cluster Monitoring ---")
    cluster = ClusterMonitor()
    cluster.register_node(ClusterNode("core-01", ClusterRole.LEADER, "10.0.0.1", uptime_seconds=86400, used_memory_mb=2048, committed_memory_mb=4096))
    cluster.register_node(ClusterNode("core-02", ClusterRole.FOLLOWER, "10.0.0.2", uptime_seconds=86000, used_memory_mb=1800, committed_memory_mb=4096))
    cluster.register_node(ClusterNode("core-03", ClusterRole.CORE, "10.0.0.3", uptime_seconds=85000, used_memory_mb=1600, committed_memory_mb=4096))
    cluster.register_node(ClusterNode("replica-01", ClusterRole.READ_REPLICA, "10.0.0.4", used_memory_mb=1200, committed_memory_mb=4096))
    cluster.register_node(ClusterNode("replica-02", ClusterRole.READ_REPLICA, "10.0.0.5", is_alive=False))

    health = cluster.health_check()
    print(f"  Health: {health}")
    leader = cluster.get_leader()
    print(f"  Leader: {leader.id if leader else 'NONE'}")
    print(f"  Read replicas: {len(cluster.get_read_replicas())}")
    print(f"  Split brain: {cluster.detect_split_brain()}")
    print(f"  Memory usage: {cluster.memory_usage_report()}")

    # Backup Management
    print("\n--- Backup Management ---")
    backup_mgr = BackupManager()
    backup_mgr.record_backup(BackupStrategy.FULL, "graph.db", 5368709120, 120.0)
    backup_mgr.record_backup(BackupStrategy.INCREMENTAL, "graph.db", 536870912, 25.0)
    backup_mgr.verify_backup("backup_20260101_120000_0001")
    backup_mgr.record_backup(BackupStrategy.FULL, "graph.db", 5905580032, 130.0)

    latest = backup_mgr.latest_backup("graph.db")
    if latest:
        print(f"  Latest backup: {latest.backup_id} ({latest.size_human}, verified={latest.verified})")

    needs = backup_mgr.needs_backup("graph.db", max_age_hours=24)
    print(f"  Needs backup: {needs}")

    restore_cmds = backup_mgr.generate_restore_commands("backup_20260101_120000_0001")
    print(f"  Restore commands: {restore_cmds}")

    removed = backup_mgr.cleanup_old_backups(keep_days=0)
    print(f"  Removed old backups: {removed}")

    # Performance Tuning
    print("\n--- Performance Tuning ---")
    tuner = PerformanceTuner()
    print(f"  {tuner.analyze_heap_size()}")
    print(f"  {tuner.analyze_pagecache()}")
    print(f"  Connection pool advice: {tuner.connection_pool_advice(200)}")
    print(f"  Transaction advice: {tuner.transaction_advice(60)}")

    config = tuner.generate_config("read_heavy")
    print(f"  Read-heavy config: heap={config.heap_initial_size}, pagecache={config.pagecache_size}")

    rec = tuner.memory_recommendation(graph_size_gb=20.0)
    print(f"  20GB graph recommendation: {rec}")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")


if __name__ == "__main__":
    main()
