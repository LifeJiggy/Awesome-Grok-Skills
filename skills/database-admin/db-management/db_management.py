"""
Database Management Module

Core database management operations providing lifecycle management, resource
allocation, space management, configuration tuning, and maintenance scheduling
for production databases.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class LifecycleAction(Enum):
    CREATE = "create"
    CLONE = "clone"
    RESIZE = "resize"
    ARCHIVE = "archive"
    DROP = "drop"
    BACKUP = "backup"
    RESTORE = "restore"


class MaintenanceTask(Enum):
    VACUUM = "vacuum"
    VACUUM_FULL = "vacuum_full"
    ANALYZE = "analyze"
    REINDEX = "reindex"
    CLUSTER = "cluster"
    CHECK = "check"
    REFRESH_MATERIALIZED = "refresh_materialized"


class DatabaseState(Enum):
    ACTIVE = "active"
    CREATING = "creating"
    CLONING = "cloning"
    ARCHIVING = "archiving"
    DROPPING = "dropping"
    MAINTENANCE = "maintenance"
    INACTIVE = "inactive"


class ConfigContext(Enum):
    POSTMASTER = "postmaster"  # requires restart
    SIGHUP = "sighup"  # reload
    SUPERUSER = "superuser"
    USER = "user"


class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class DatabaseInfo:
    """Information about a database."""
    name: str
    owner: str
    encoding: str = "UTF-8"
    locale: str = "en_US.UTF-8"
    size_bytes: int = 0
    state: DatabaseState = DatabaseState.ACTIVE
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_vacuum: Optional[datetime] = None
    last_analyze: Optional[datetime] = None
    connection_count: int = 0
    max_connections: int = 100

    @property
    def size_mb(self) -> float:
        return self.size_bytes / (1024 * 1024)

    @property
    def size_gb(self) -> float:
        return self.size_bytes / (1024 ** 3)


@dataclass
class DatabaseSize:
    """Size breakdown of a database."""
    total_bytes: int = 0
    tables_bytes: int = 0
    indexes_bytes: int = 0
    toast_bytes: int = 0
    free_bytes: int = 0

    @property
    def total_mb(self) -> float:
        return self.total_bytes / (1024 * 1024)

    @property
    def tables_mb(self) -> float:
        return self.tables_bytes / (1024 * 1024)

    @property
    def indexes_mb(self) -> float:
        return self.indexes_bytes / (1024 * 1024)

    @property
    def free_mb(self) -> float:
        return self.free_bytes / (1024 * 1024)


@dataclass
class TableBloat:
    """Table bloat information."""
    name: str
    schema: str = "public"
    size_bytes: int = 0
    dead_bytes: int = 0
    bloat_pct: float = 0.0
    wasted_bytes: int = 0
    fill_factor: int = 100
    last_vacuum: Optional[datetime] = None

    @property
    def wasted_mb(self) -> float:
        return self.wasted_bytes / (1024 * 1024)


@dataclass
class VacuumResult:
    """Result of a VACUUM operation."""
    table: str
    duration_seconds: float
    rows_scanned: int
    rows_removed: int
    pages_removed: int
    space_reclaimed_bytes: int
    new_live_tuples: int
    new_dead_tuples: int
    analyze_performed: bool = False

    @property
    def space_reclaimed_mb(self) -> float:
        return self.space_reclaimed_bytes / (1024 * 1024)


@dataclass
class ConfigParameter:
    """Database configuration parameter."""
    name: str
    value: str
    unit: str = ""
    category: str = ""
    context: ConfigContext = ConfigContext.SIGHUP
    description: str = ""
    min_value: Optional[str] = None
    max_value: Optional[str] = None
    default_value: Optional[str] = None
    is_reloadable: bool = True

    @property
    def requires_restart(self) -> bool:
        return self.context == ConfigContext.POSTMASTER


@dataclass
class ConfigChange:
    """Record of a configuration change."""
    parameter: str
    old_value: str
    new_value: str
    context: ConfigContext
    changed_by: str = "system"
    changed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    reason: str = ""


@dataclass
class ConfigDiff:
    """Configuration difference between environments."""
    parameter: str
    production_value: str
    staging_value: str
    environment_a: str = "production"
    environment_b: str = "staging"


@dataclass
class ArchiveResult:
    """Result of a data archival operation."""
    table: str
    rows_archived: int
    size_bytes: int
    archive_location: str
    duration_seconds: float
    archived_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def size_mb(self) -> float:
        return self.size_bytes / (1024 * 1024)


@dataclass
class MaintenanceSchedule:
    """Scheduled maintenance task."""
    task: MaintenanceTask
    schedule: str  # cron expression
    targets: List[str]
    options: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None


@dataclass
class MaintenanceResult:
    """Result of a maintenance window."""
    tasks_completed: int
    tasks_failed: int
    duration_seconds: float
    details: List[Dict[str, Any]] = field(default_factory=list)
    completed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ResourceMetrics:
    """Database resource metrics."""
    active_connections: int = 0
    idle_connections: int = 0
    waiting_connections: int = 0
    locks_held: int = 0
    locks_waiting: int = 0
    deadlocks: int = 0
    temp_files: int = 0
    temp_bytes: int = 0
    cache_hit_ratio: float = 0.0
    index_usage_ratio: float = 0.0
    tuple_statistics: Dict[str, int] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Database Manager
# ---------------------------------------------------------------------------

class DatabaseManager:
    """Manage database lifecycle operations."""

    def __init__(self, connection_string: str = ""):
        self.connection_string = connection_string
        self._databases: Dict[str, DatabaseInfo] = {}
        self._history: List[Dict[str, Any]] = []

    def create_database(
        self,
        name: str,
        template: str = "template0",
        encoding: str = "UTF-8",
        locale: str = "en_US.UTF-8",
        owner: str = "postgres",
        tablespace: Optional[str] = None,
    ) -> DatabaseInfo:
        db = DatabaseInfo(
            name=name, owner=owner, encoding=encoding, locale=locale,
            state=DatabaseState.CREATING,
        )
        logger.info("Creating database: %s (owner=%s, encoding=%s)", name, owner, encoding)

        # Simulate creation
        db.state = DatabaseState.ACTIVE
        db.size_bytes = np.random.randint(1_000_000, 10_000_000)
        self._databases[name] = db

        self._log_action("CREATE", name, {"template": template, "tablespace": tablespace})
        return db

    def clone_database(
        self,
        source: str,
        target: str,
        copy_data: bool = True,
        copy_privileges: bool = True,
    ) -> DatabaseInfo:
        if source not in self._databases:
            raise ValueError(f"Source database '{source}' not found")

        source_db = self._databases[source]
        clone = DatabaseInfo(
            name=target, owner=source_db.owner,
            encoding=source_db.encoding, locale=source_db.locale,
            state=DatabaseState.CLONING,
        )

        logger.info("Cloning database: %s → %s", source, target)
        clone.state = DatabaseState.ACTIVE
        clone.size_bytes = source_db.size_bytes if copy_data else 1_000_000
        self._databases[target] = clone

        self._log_action("CLONE", target, {"source": source, "copy_data": copy_data})
        return clone

    def archive_data(
        self,
        database: str,
        table: str,
        older_than_days: int = 90,
        archive_to: str = "/archive/",
    ) -> ArchiveResult:
        start = time.time()
        rows_archived = np.random.randint(10000, 1000000)
        size_bytes = rows_archived * 100  # avg row size

        logger.info("Archiving %d rows from %s.%s", rows_archived, database, table)

        result = ArchiveResult(
            table=table,
            rows_archived=rows_archived,
            size_bytes=size_bytes,
            archive_location=archive_to,
            duration_seconds=time.time() - start,
        )

        self._log_action("ARCHIVE", f"{database}.{table}", {
            "rows": rows_archived, "older_than_days": older_than_days,
        })
        return result

    def drop_database(self, name: str, force: bool = False) -> bool:
        if name not in self._databases:
            raise ValueError(f"Database '{name}' not found")

        db = self._databases[name]
        db.state = DatabaseState.DROPPING
        logger.info("Dropping database: %s", name)

        del self._databases[name]
        self._log_action("DROP", name, {"force": force})
        return True

    def list_databases(self) -> List[DatabaseInfo]:
        return list(self._databases.values())

    def get_database(self, name: str) -> Optional[DatabaseInfo]:
        return self._databases.get(name)

    def _log_action(self, action: str, target: str, details: Dict[str, Any]) -> None:
        self._history.append({
            "action": action,
            "target": target,
            "details": details,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })


# ---------------------------------------------------------------------------
# Space Manager
# ---------------------------------------------------------------------------

class SpaceManager:
    """Manage database space and storage."""

    def __init__(self, connection_string: str = ""):
        self.connection_string = connection_string

    def get_database_size(self, database: str = "default") -> DatabaseSize:
        total = np.random.randint(1_000_000_000, 100_000_000_000)
        tables = int(total * 0.6)
        indexes = int(total * 0.25)
        toast = int(total * 0.05)
        free = total - tables - indexes - toast

        return DatabaseSize(
            total_bytes=total,
            tables_bytes=tables,
            indexes_bytes=indexes,
            toast_bytes=toast,
            free_bytes=free,
        )

    def detect_bloat(self, schema: str = "public") -> List[TableBloat]:
        tables = ["orders", "events", "sessions", "users", "products", "audit_log"]
        bloat_list = []

        for table in tables:
            size = np.random.randint(10_000_000, 5_000_000_000)
            bloat_pct = np.random.uniform(5, 60)
            wasted = int(size * bloat_pct / 100)

            bloat_list.append(TableBloat(
                name=table,
                schema=schema,
                size_bytes=size,
                dead_bytes=int(size * 0.02),
                bloat_pct=bloat_pct,
                wasted_bytes=wasted,
                fill_factor=np.random.choice([70, 80, 90, 100]),
            ))

        return sorted(bloat_list, key=lambda b: b.wasted_bytes, reverse=True)

    def vacuum(
        self,
        table: str,
        full: bool = False,
        analyze: bool = True,
        verbose: bool = False,
    ) -> VacuumResult:
        start = time.time()
        logger.info("Running VACUUM on %s (full=%s, analyze=%s)", table, full, analyze)

        rows_scanned = np.random.randint(100000, 10000000)
        pages_removed = np.random.randint(100, 10000)
        space_reclaimed = pages_removed * 8192  # 8KB pages

        return VacuumResult(
            table=table,
            duration_seconds=time.time() - start,
            rows_scanned=rows_scanned,
            rows_removed=int(rows_scanned * 0.01),
            pages_removed=pages_removed,
            space_reclaimed_bytes=space_reclaimed,
            new_live_tuples=rows_scanned - int(rows_scanned * 0.01),
            new_dead_tuples=0,
            analyze_performed=analyze,
        )

    def get_index_usage(self) -> List[Dict[str, Any]]:
        return [
            {"index": "orders_pkey", "table": "orders", "scans": 50000, "size_mb": 12.5},
            {"index": "orders_customer_idx", "table": "orders", "scans": 30000, "size_mb": 8.2},
            {"index": "events_created_idx", "table": "events", "scans": 15000, "size_mb": 45.0},
            {"index": "sessions_user_idx", "table": "sessions", "scans": 5000, "size_mb": 3.1},
            {"index": "users_email_idx", "table": "users", "scans": 80000, "size_mb": 5.5},
        ]


# ---------------------------------------------------------------------------
# Config Manager
# ---------------------------------------------------------------------------

class ConfigManager:
    """Manage database configuration parameters."""

    def __init__(self, connection_string: str = ""):
        self.connection_string = connection_string
        self._config_history: List[ConfigChange] = []
        self._parameters: Dict[str, ConfigParameter] = self._load_defaults()

    def _load_defaults(self) -> Dict[str, ConfigParameter]:
        defaults = [
            ConfigParameter("shared_buffers", "128MB", unit="MB", category="memory",
                          context=ConfigContext.POSTMASTER, description="Sets the number of shared memory buffers."),
            ConfigParameter("effective_cache_size", "4GB", unit="MB", category="memory",
                          context=ConfigContext.SIGHUP, description="Sets the planner's assumption about total cache size."),
            ConfigParameter("work_mem", "4MB", unit="MB", category="memory",
                          context=ConfigContext.SIGHUP, description="Sets the maximum memory for query operations."),
            ConfigParameter("maintenance_work_mem", "64MB", unit="MB", category="memory",
                          context=ConfigContext.SIGHUP, description="Sets the maximum memory for maintenance operations."),
            ConfigParameter("max_connections", "100", category="connections",
                          context=ConfigContext.POSTMASTER, description="Sets the maximum number of concurrent connections."),
            ConfigParameter("wal_buffers", "-1", category="wal",
                          context=ConfigContext.POSTMASTER, description="Sets the number of WAL buffers."),
            ConfigParameter("checkpoint_completion_target", "0.9", category="checkpoint",
                          context=ConfigContext.SIGHUP, description="Time spent flushing dirty buffers during checkpoint."),
            ConfigParameter("random_page_cost", "4.0", category="query",
                          context=ConfigContext.SIGHUP, description="Sets the planner's estimate of random page cost."),
            ConfigParameter("log_min_duration_statement", "1000", unit="ms", category="logging",
                          context=ConfigContext.SIGHUP, description="Sets the minimum execution time above which statements are logged."),
            ConfigParameter("deadlock_timeout", "1000", unit="ms", category="locks",
                          context=ConfigContext.SIGHUP, description="Sets the time to wait on a lock before checking for deadlock."),
        ]
        return {p.name: p for p in defaults}

    def get_parameters(self, category: Optional[str] = None) -> List[ConfigParameter]:
        params = list(self._parameters.values())
        if category:
            params = [p for p in params if p.category == category]
        return params

    def get_parameter(self, name: str) -> Optional[ConfigParameter]:
        return self._parameters.get(name)

    def set_parameter(
        self,
        name: str,
        value: str,
        context: Optional[ConfigContext] = None,
        reload: bool = True,
    ) -> ConfigChange:
        old_value = self._parameters[name].value if name in self._parameters else ""
        if name in self._parameters:
            self._parameters[name].value = value

        change = ConfigChange(
            parameter=name,
            old_value=old_value,
            new_value=value,
            context=context or ConfigContext.SIGHUP,
        )
        self._config_history.append(change)
        logger.info("Configuration changed: %s = %s (was %s)", name, value, old_value)
        return change

    def diff_configurations(
        self,
        env_a: str = "production",
        env_b: str = "staging",
    ) -> List[ConfigDiff]:
        diffs = []
        for name, param in self._parameters.items():
            val_a = param.value
            val_b = param.default_value or param.value
            if val_a != val_b:
                diffs.append(ConfigDiff(
                    parameter=name,
                    production_value=val_a,
                    staging_value=val_b,
                    environment_a=env_a,
                    environment_b=env_b,
                ))
        return diffs

    def get_history(self, limit: int = 20) -> List[ConfigChange]:
        return self._config_history[-limit:]


# ---------------------------------------------------------------------------
# Maintenance Scheduler
# ---------------------------------------------------------------------------

class MaintenanceScheduler:
    """Schedule and run database maintenance tasks."""

    def __init__(self, connection_string: str = ""):
        self.connection_string = connection_string
        self._schedules: List[MaintenanceSchedule] = []
        self._history: List[MaintenanceResult] = []

    def schedule(
        self,
        task: MaintenanceTask,
        schedule: str,
        targets: List[str],
        options: Optional[Dict[str, Any]] = None,
    ) -> MaintenanceSchedule:
        ms = MaintenanceSchedule(
            task=task, schedule=schedule, targets=targets,
            options=options or {},
        )
        self._schedules.append(ms)
        logger.info("Scheduled maintenance: %s on %s (cron: %s)", task.value, targets, schedule)
        return ms

    def run_maintenance_window(
        self,
        start_hour: int = 2,
        end_hour: int = 6,
        tasks: Optional[List[MaintenanceTask]] = None,
    ) -> MaintenanceResult:
        if tasks is None:
            tasks = [MaintenanceTask.VACUUM, MaintenanceTask.ANALYZE]

        start_time = time.time()
        completed = 0
        failed = 0
        details = []

        for task in tasks:
            for schedule in self._schedules:
                if schedule.task == task and schedule.enabled:
                    try:
                        # Simulate task execution
                        time.sleep(0.01)
                        completed += 1
                        details.append({
                            "task": task.value,
                            "targets": schedule.targets,
                            "status": "completed",
                            "duration_seconds": 0.01,
                        })
                        schedule.last_run = datetime.now(timezone.utc)
                    except Exception as e:
                        failed += 1
                        details.append({
                            "task": task.value,
                            "targets": schedule.targets,
                            "status": "failed",
                            "error": str(e),
                        })

        result = MaintenanceResult(
            tasks_completed=completed,
            tasks_failed=failed,
            duration_seconds=time.time() - start_time,
            details=details,
        )
        self._history.append(result)
        return result

    def get_schedules(self) -> List[MaintenanceSchedule]:
        return self._schedules

    def get_history(self, limit: int = 10) -> List[MaintenanceResult]:
        return self._history[-limit:]


# ---------------------------------------------------------------------------
# Resource Monitor
# ---------------------------------------------------------------------------

class ResourceMonitor:
    """Monitor database resource usage."""

    def __init__(self, connection_string: str = ""):
        self.connection_string = connection_string

    def get_metrics(self) -> ResourceMetrics:
        return ResourceMetrics(
            active_connections=np.random.randint(10, 50),
            idle_connections=np.random.randint(5, 20),
            waiting_connections=np.random.randint(0, 5),
            locks_held=np.random.randint(0, 100),
            locks_waiting=np.random.randint(0, 10),
            deadlocks=np.random.randint(0, 3),
            temp_files=np.random.randint(0, 50),
            temp_bytes=np.random.randint(0, 10_000_000),
            cache_hit_ratio=np.random.uniform(0.95, 0.999),
            index_usage_ratio=np.random.uniform(0.80, 0.99),
        )

    def get_slow_queries(self, threshold_ms: int = 1000) -> List[Dict[str, Any]]:
        queries = []
        for i in range(5):
            queries.append({
                "query": f"SELECT * FROM orders WHERE status = '{['pending', 'active', 'completed'][i % 3]}'",
                "duration_ms": np.random.uniform(threshold_ms, threshold_ms * 10),
                "calls": np.random.randint(100, 10000),
                "rows": np.random.randint(1, 10000),
            })
        return sorted(queries, key=lambda q: q["duration_ms"], reverse=True)

    def get_lock_info(self) -> List[Dict[str, Any]]:
        return [
            {"lock_type": "relation", "mode": "AccessShareLock", "granted": True, "pid": 1234},
            {"lock_type": "tuple", "mode": "RowExclusiveLock", "granted": True, "pid": 1235},
            {"lock_type": "relation", "mode": "RowShareLock", "granted": False, "pid": 1236},
        ]


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate database management capabilities."""
    print("=" * 70)
    print("Database Management Module - Demo")
    print("=" * 70)

    # --- 1. Database Lifecycle ---
    print("\n--- Database Lifecycle ---")
    manager = DatabaseManager()
    db = manager.create_database("analytics_prod", owner="app_user")
    print(f"Created: {db.name} ({db.size_mb:.1f} MB)")

    clone = manager.clone_database("analytics_prod", "analytics_staging", copy_data=True)
    print(f"Cloned: {clone.name} ({clone.size_mb:.1f} MB)")

    archive = manager.archive_data("analytics_prod", "events", older_than_days=90)
    print(f"Archived: {archive.rows_archived:,} rows ({archive.size_mb:.1f} MB)")

    print(f"Databases: {[d.name for d in manager.list_databases()]}")

    # --- 2. Space Management ---
    print("\n--- Space Management ---")
    space = SpaceManager()
    db_size = space.get_database_size()
    print(f"Database size: {db_size.total_mb:.1f} MB")
    print(f"  Tables: {db_size.tables_mb:.1f} MB")
    print(f"  Indexes: {db_size.indexes_mb:.1f} MB")

    bloat = space.detect_bloat()
    for b in bloat[:3]:
        print(f"  {b.name}: {b.bloat_pct:.1f}% bloat ({b.wasted_mb:.1f} MB wasted)")

    vacuum_result = space.vacuum("orders", analyze=True)
    print(f"Vacuum: reclaimed {vacuum_result.space_reclaimed_mb:.1f} MB in {vacuum_result.duration_seconds:.2f}s")

    # --- 3. Configuration ---
    print("\n--- Configuration ---")
    config = ConfigManager()
    params = config.get_parameters(category="memory")
    for p in params:
        print(f"  {p.name}: {p.value} ({'restart' if p.requires_restart else 'reload'})")

    change = config.set_parameter("shared_buffers", "4GB")
    print(f"Changed: {change.parameter} = {change.new_value} (was {change.old_value})")

    # --- 4. Maintenance ---
    print("\n--- Maintenance ---")
    scheduler = MaintenanceScheduler()
    scheduler.schedule(MaintenanceTask.VACUUM, "0 2 * * *", ["orders", "events"])
    scheduler.schedule(MaintenanceTask.ANALYZE, "0 3 * * *", ["orders", "events"])
    scheduler.schedule(MaintenanceTask.REINDEX, "0 4 * * 0", ["orders_idx"])

    result = scheduler.run_maintenance_window()
    print(f"Maintenance: {result.tasks_completed} completed, {result.tasks_failed} failed "
          f"in {result.duration_seconds:.2f}s")

    # --- 5. Resource Monitoring ---
    print("\n--- Resource Monitoring ---")
    monitor = ResourceMonitor()
    metrics = monitor.get_metrics()
    print(f"  Connections: {metrics.active_connections} active, {metrics.idle_connections} idle")
    print(f"  Locks: {metrics.locks_held} held, {metrics.locks_waiting} waiting")
    print(f"  Cache hit ratio: {metrics.cache_hit_ratio:.3f}")
    print(f"  Index usage: {metrics.index_usage_ratio:.3f}")

    slow = monitor.get_slow_queries(threshold_ms=500)
    print(f"  Slow queries: {len(slow)}")
    for q in slow[:2]:
        print(f"    {q['duration_ms']:.0f}ms: {q['query'][:60]}...")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()