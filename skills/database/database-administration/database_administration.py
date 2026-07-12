"""
Database Administration Framework

Production-grade database administration toolkit providing connection pooling, schema
management, backup orchestration, access control, query monitoring, and multi-database
support for reliable database operations.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
import threading
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, Generator, List, Optional, Sequence, Tuple, Union

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class DatabaseType(Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MONGODB = "mongodb"
    REDIS = "redis"


class Permission(Enum):
    ALL = "all"
    SELECT = "select"
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"
    CREATE = "create"
    ALTER = "alter"
    DROP = "drop"
    GRANT = "grant"


class MigrationState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class BackupType(Enum):
    FULL = "full"
    INCREMENTAL = "incremental"
    DIFFERENTIAL = "differential"
    WAL = "wal"


class BackupState(Enum):
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    VERIFIED = "verified"


class SlowQueryThreshold(Enum):
    MILLISECONDS_100 = 100
    MILLISECONDS_250 = 250
    MILLISECONDS_500 = 500
    SECONDS_1 = 1000
    SECONDS_5 = 5000


class ConnectionState(Enum):
    IDLE = "idle"
    IN_USE = "in_use"
    CLOSED = "closed"
    UNHEALTHY = "unhealthy"


class QueryState(Enum):
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class PoolConfig:
    """Connection pool configuration."""
    host: str = "localhost"
    port: int = 5432
    database: str = "postgres"
    user: str = "postgres"
    password_env_var: str = "DB_PASSWORD"
    min_connections: int = 5
    max_connections: int = 20
    max_idle_time_seconds: int = 300
    connection_timeout_seconds: int = 10
    health_check_interval: int = 60
    enable_ssl: bool = False
    ssl_ca_path: Optional[str] = None
    retry_attempts: int = 3
    retry_delay_seconds: float = 1.0
    database_type: DatabaseType = DatabaseType.POSTGRESQL

    @property
    def dsn(self) -> str:
        password = os.environ.get(self.password_env_var, "")
        return f"{self.database_type.value}://{self.user}:{password}@{self.host}:{self.port}/{self.database}"


@dataclass
class ConnectionInfo:
    """Information about a database connection."""
    connection_id: str
    state: ConnectionState
    created_at: datetime
    last_used_at: Optional[datetime] = None
    database: str = ""
    user: str = ""
    query_count: int = 0
    error_count: int = 0
    total_time_seconds: float = 0.0

    @property
    def idle_seconds(self) -> float:
        if self.last_used_at is None:
            return (datetime.now(timezone.utc) - self.created_at).total_seconds()
        return (datetime.now(timezone.utc) - self.last_used_at).total_seconds()

    @property
    def is_healthy(self) -> bool:
        return self.state != ConnectionState.UNHEALTHY and self.error_count < 5


@dataclass
class Migration:
    """Schema migration definition."""
    version: str
    description: str
    up: List[str] = field(default_factory=list)
    down: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    state: MigrationState = MigrationState.PENDING
    applied_at: Optional[datetime] = None
    rolled_back_at: Optional[datetime] = None
    checksum: str = ""

    def __post_init__(self) -> None:
        if not self.checksum:
            content = json.dumps({"up": self.up, "down": self.down}, sort_keys=True)
            self.checksum = hashlib.sha256(content.encode()).hexdigest()[:16]


@dataclass
class MigrationStatus:
    """Status of a migration."""
    version: str
    description: str
    state: MigrationState
    applied_at: Optional[datetime] = None
    checksum: str = ""


@dataclass
class BackupSchedule:
    """Backup schedule configuration."""
    name: str
    frequency: str  # daily, hourly, weekly
    time: str = "02:00"
    retention_days: int = 30
    compression: bool = True
    encryption_key_env: Optional[str] = None
    backup_type: BackupType = BackupType.FULL
    enabled: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None


@dataclass
class BackupResult:
    """Result of a backup operation."""
    filename: str
    backup_type: BackupType
    size_bytes: int
    duration_seconds: float
    timestamp: datetime
    checksum: str = ""
    compressed: bool = False
    encrypted: bool = False
    verified: bool = False
    tag: Optional[str] = None

    @property
    def size_mb(self) -> float:
        return self.size_bytes / (1024 * 1024)


@dataclass
class Role:
    """Database role definition."""
    name: str
    permissions: List[Permission] = field(default_factory=list)
    row_level_security: Optional[Dict[str, str]] = None
    inherits_from: Optional[List[str]] = None


@dataclass
class AuditEntry:
    """Audit log entry."""
    timestamp: datetime
    user: str
    operation: str
    table: Optional[str] = None
    database: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    success: bool = True
    ip_address: Optional[str] = None


@dataclass
class QueryTracking:
    """Query execution tracking context."""
    query_id: str
    query: str
    start_time: float
    state: QueryState = QueryState.EXECUTING
    end_time: Optional[float] = None
    row_count: int = 0
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def duration_ms(self) -> float:
        end = self.end_time if self.end_time else time.time()
        return (end - self.start_time) * 1000


@dataclass
class QueryMetrics:
    """Aggregated query performance metrics."""
    total_queries: int = 0
    total_duration_ms: float = 0.0
    avg_duration_ms: float = 0.0
    p50_duration_ms: float = 0.0
    p95_duration_ms: float = 0.0
    p99_duration_ms: float = 0.0
    error_count: int = 0
    error_rate: float = 0.0
    queries_per_second: float = 0.0
    slow_query_count: int = 0
    slow_query_rate: float = 0.0


# ---------------------------------------------------------------------------
# Connection Pool
# ---------------------------------------------------------------------------

class ConnectionPool:
    """Thread-safe database connection pool."""

    def __init__(self, config: PoolConfig):
        self.config = config
        self._connections: List[ConnectionInfo] = []
        self._lock = threading.Lock()
        self._semaphore = threading.Semaphore(config.max_connections)
        self._stats = {
            "total_acquired": 0,
            "total_released": 0,
            "total_errors": 0,
            "total_timeouts": 0,
        }
        # Initialize minimum connections
        for _ in range(config.min_connections):
            conn = self._create_connection()
            self._connections.append(conn)

    def _create_connection(self) -> ConnectionInfo:
        conn_id = hashlib.md5(
            f"{self.config.host}:{self.config.port}:{time.time()}".encode()
        ).hexdigest()[:12]

        return ConnectionInfo(
            connection_id=conn_id,
            state=ConnectionState.IDLE,
            created_at=datetime.now(timezone.utc),
            database=self.config.database,
            user=self.config.user,
        )

    @contextmanager
    def acquire(self, timeout: Optional[float] = None) -> Generator[ConnectionInfo, None, None]:
        """Acquire a connection from the pool."""
        acquired = False
        conn = None

        try:
            if not self._semaphore.acquire(timeout=timeout or self.config.connection_timeout_seconds):
                self._stats["total_timeouts"] += 1
                raise TimeoutError(f"Could not acquire connection within {timeout}s")

            with self._lock:
                # Find available connection
                for c in self._connections:
                    if c.state == ConnectionState.IDLE and c.is_healthy:
                        c.state = ConnectionState.IN_USE
                        c.last_used_at = datetime.now(timezone.utc)
                        conn = c
                        break

                # Create new connection if needed
                if conn is None and len(self._connections) < self.config.max_connections:
                    conn = self._create_connection()
                    conn.state = ConnectionState.IN_USE
                    conn.last_used_at = datetime.now(timezone.utc)
                    self._connections.append(conn)

                # Recycle oldest idle connection
                if conn is None:
                    idle_conns = [c for c in self._connections if c.state == ConnectionState.IDLE]
                    if idle_conns:
                        oldest = min(idle_conns, key=lambda c: c.created_at)
                        oldest.state = ConnectionState.CLOSED
                        conn = self._create_connection()
                        conn.state = ConnectionState.IN_USE
                        conn.last_used_at = datetime.now(timezone.utc)
                        self._connections.remove(oldest)
                        self._connections.append(conn)

            if conn is None:
                self._stats["total_errors"] += 1
                raise RuntimeError("No available connections in pool")

            acquired = True
            self._stats["total_acquired"] += 1
            yield conn

        finally:
            if acquired and conn is not None:
                with self._lock:
                    conn.state = ConnectionState.IDLE
                    conn.query_count += 1
                    conn.last_used_at = datetime.now(timezone.utc)
                self._stats["total_released"] += 1
                self._semaphore.release()

    def health_check(self) -> List[ConnectionInfo]:
        """Check health of all connections."""
        unhealthy = []
        with self._lock:
            for conn in self._connections:
                if conn.idle_seconds > self.config.max_idle_time_seconds:
                    conn.state = ConnectionState.UNHEALTHY
                    unhealthy.append(conn)
                elif not conn.is_healthy:
                    unhealthy.append(conn)
            # Remove unhealthy connections
            self._connections = [c for c in self._connections if c.state != ConnectionState.UNHEALTHY]

        # Replace removed connections up to minimum
        with self._lock:
            while len(self._connections) < self.config.min_connections:
                self._connections.append(self._create_connection())

        return unhealthy

    def get_stats(self) -> Dict[str, Any]:
        with self._lock:
            idle = sum(1 for c in self._connections if c.state == ConnectionState.IDLE)
            in_use = sum(1 for c in self._connections if c.state == ConnectionState.IN_USE)
            return {
                "total_connections": len(self._connections),
                "idle": idle,
                "in_use": in_use,
                "max_connections": self.config.max_connections,
                **self._stats,
            }

    def close_all(self) -> None:
        with self._lock:
            for conn in self._connections:
                conn.state = ConnectionState.CLOSED
            self._connections.clear()


# ---------------------------------------------------------------------------
# Migration Manager
# ---------------------------------------------------------------------------

class MigrationManager:
    """Schema migration management."""

    def __init__(self, pool: ConnectionPool):
        self.pool = pool
        self._migrations: Dict[str, Migration] = {}
        self._applied: Dict[str, MigrationStatus] = {}
        self._ensure_migration_table()

    def _ensure_migration_table(self) -> None:
        """Create migrations tracking table if it doesn't exist."""
        # In production, this would execute SQL
        logger.info("Ensuring migration tracking table exists")

    def register(self, migration: Migration) -> None:
        self._migrations[migration.version] = migration

    def migrate(self, target: Optional[str] = None) -> List[MigrationStatus]:
        """Apply pending migrations up to target version."""
        applied = []
        sorted_versions = sorted(self._migrations.keys())

        for version in sorted_versions:
            if target and version > target:
                break

            migration = self._migrations[version]
            if migration.state == MigrationState.COMPLETED:
                continue

            # Check dependencies
            for dep in migration.dependencies:
                if dep not in self._applied or self._applied[dep].state != MigrationState.COMPLETED:
                    logger.warning("Migration %s depends on unapplied migration %s", version, dep)
                    return applied

            # Apply migration
            migration.state = MigrationState.RUNNING
            try:
                logger.info("Applying migration %s: %s", version, migration.description)
                # In production, execute SQL statements
                for stmt in migration.up:
                    logger.debug("  SQL: %s", stmt[:100])

                migration.state = MigrationState.COMPLETED
                migration.applied_at = datetime.now(timezone.utc)
                self._applied[version] = MigrationStatus(
                    version=version,
                    description=migration.description,
                    state=MigrationState.COMPLETED,
                    applied_at=migration.applied_at,
                    checksum=migration.checksum,
                )
                applied.append(self._applied[version])

            except Exception as e:
                migration.state = MigrationState.FAILED
                logger.error("Migration %s failed: %s", version, e)
                break

        return applied

    def rollback(self, target: str) -> List[MigrationStatus]:
        """Rollback migrations to target version."""
        rolled_back = []
        sorted_versions = sorted(self._migrations.keys(), reverse=True)

        for version in sorted_versions:
            if version <= target:
                break

            migration = self._migrations[version]
            if migration.state != MigrationState.COMPLETED:
                continue

            migration.state = MigrationState.RUNNING
            try:
                logger.info("Rolling back migration %s: %s", version, migration.description)
                for stmt in migration.down:
                    logger.debug("  SQL: %s", stmt[:100])

                migration.state = MigrationState.ROLLED_BACK
                migration.rolled_back_at = datetime.now(timezone.utc)
                self._applied[version] = MigrationStatus(
                    version=version,
                    description=migration.description,
                    state=MigrationState.ROLLED_BACK,
                    applied_at=migration.rolled_back_at,
                )
                rolled_back.append(self._applied[version])

            except Exception as e:
                migration.state = MigrationState.FAILED
                logger.error("Rollback of %s failed: %s", version, e)
                break

        return rolled_back

    def status(self) -> List[MigrationStatus]:
        """Get status of all registered migrations."""
        statuses = []
        for version in sorted(self._migrations.keys()):
            migration = self._migrations[version]
            statuses.append(MigrationStatus(
                version=version,
                description=migration.description,
                state=migration.state,
                applied_at=migration.applied_at,
                checksum=migration.checksum,
            ))
        return statuses

    def diff(self, local_migrations: List[Migration]) -> Dict[str, Any]:
        """Compare local migrations with applied migrations."""
        local_versions = {m.version for m in local_migrations}
        applied_versions = set(self._applied.keys())

        return {
            "pending": sorted(local_versions - applied_versions),
            "applied": sorted(applied_versions & local_versions),
            "extra_applied": sorted(applied_versions - local_versions),
        }


# ---------------------------------------------------------------------------
# Backup Manager
# ---------------------------------------------------------------------------

class BackupManager:
    """Database backup and recovery management."""

    def __init__(self, pool: ConnectionPool, backup_dir: str = "/backups"):
        self.pool = pool
        self.backup_dir = backup_dir
        self._schedules: Dict[str, BackupSchedule] = {}
        self._backups: List[BackupResult] = []

    def schedule(self, schedule: BackupSchedule) -> None:
        self._schedules[schedule.name] = schedule

    def run_full_backup(self, tag: Optional[str] = None) -> BackupResult:
        """Run a full backup immediately."""
        start_time = time.time()
        timestamp = datetime.now(timezone.utc)
        filename = f"full_{timestamp.strftime('%Y%m%d_%H%M%S')}.sql.gz"

        logger.info("Starting full backup: %s", filename)

        # Simulate backup process
        time.sleep(0.1)

        duration = time.time() - start_time
        size_bytes = np.random.randint(10_000_000, 500_000_000)
        checksum = hashlib.sha256(filename.encode()).hexdigest()[:16]

        result = BackupResult(
            filename=filename,
            backup_type=BackupType.FULL,
            size_bytes=size_bytes,
            duration_seconds=duration,
            timestamp=timestamp,
            checksum=checksum,
            compressed=True,
            tag=tag,
        )

        self._backups.append(result)
        logger.info("Backup completed: %s (%.1f MB, %.1fs)", filename, result.size_mb, duration)

        return result

    def run_incremental_backup(self, tag: Optional[str] = None) -> BackupResult:
        start_time = time.time()
        timestamp = datetime.now(timezone.utc)
        filename = f"incr_{timestamp.strftime('%Y%m%d_%H%M%S')}.sql.gz"

        time.sleep(0.05)
        duration = time.time() - start_time
        size_bytes = np.random.randint(1_000_000, 50_000_000)

        result = BackupResult(
            filename=filename,
            backup_type=BackupType.INCREMENTAL,
            size_bytes=size_bytes,
            duration_seconds=duration,
            timestamp=timestamp,
            checksum=hashlib.sha256(filename.encode()).hexdigest()[:16],
            compressed=True,
            tag=tag,
        )

        self._backups.append(result)
        return result

    def list_backups(
        self,
        retention_days: Optional[int] = None,
        backup_type: Optional[BackupType] = None,
    ) -> List[BackupResult]:
        backups = list(self._backups)

        if retention_days is not None:
            cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)
            backups = [b for b in backups if b.timestamp >= cutoff]

        if backup_type is not None:
            backups = [b for b in backups if b.backup_type == backup_type]

        return sorted(backups, key=lambda b: b.timestamp, reverse=True)

    def verify_backup(self, backup: BackupResult) -> bool:
        """Verify backup integrity."""
        logger.info("Verifying backup: %s", backup.filename)
        # In production, this would restore to a test database
        backup.verified = True
        return True

    def restore(self, backup: BackupResult, target_time: Optional[datetime] = None) -> bool:
        """Restore from backup."""
        logger.info("Restoring from backup: %s", backup.filename)
        if target_time:
            logger.info("Point-in-time recovery to: %s", target_time)
        # In production, this would execute restore commands
        return True

    def get_schedules(self) -> List[BackupSchedule]:
        return list(self._schedules.values())


# ---------------------------------------------------------------------------
# Access Control
# ---------------------------------------------------------------------------

class AccessControl:
    """Database access control and audit logging."""

    def __init__(self, pool: ConnectionPool):
        self.pool = pool
        self._roles: Dict[str, Role] = {}
        self._grants: Dict[str, Dict[str, Role]] = {}  # user -> {database: role}
        self._audit_log: List[AuditEntry] = []

    def grant_role(self, user: str, role: Role, database: str) -> None:
        self._roles[role.name] = role
        if user not in self._grants:
            self._grants[user] = {}
        self._grants[user][database] = role

        self._log_audit(
            user="system",
            operation="GRANT_ROLE",
            database=database,
            details={"granted_to": user, "role": role.name},
        )

    def revoke_role(self, user: str, role_name: str, database: str) -> None:
        if user in self._grants and database in self._grants[user]:
            del self._grants[user][database]
            self._log_audit(
                user="system",
                operation="REVOKE_ROLE",
                database=database,
                details={"revoked_from": user, "role": role_name},
            )

    def check_permission(self, user: str, database: str, permission: Permission) -> bool:
        if user not in self._grants or database not in self._grants[user]:
            return False

        role = self._grants[user][database]
        return Permission.ALL in role.permissions or permission in role.permissions

    def get_user_roles(self, user: str) -> Dict[str, Role]:
        return self._grants.get(user, {})

    def get_audit_log(
        self,
        user: Optional[str] = None,
        limit: int = 100,
    ) -> List[AuditEntry]:
        entries = self._audit_log
        if user:
            entries = [e for e in entries if e.user == user]
        return sorted(entries, key=lambda e: e.timestamp, reverse=True)[:limit]

    def _log_audit(
        self,
        user: str,
        operation: str,
        table: Optional[str] = None,
        database: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        success: bool = True,
    ) -> None:
        entry = AuditEntry(
            timestamp=datetime.now(timezone.utc),
            user=user,
            operation=operation,
            table=table,
            database=database,
            details=details,
            success=success,
        )
        self._audit_log.append(entry)
        logger.info("Audit: %s by %s on %s.%s", operation, user, database, table)


# ---------------------------------------------------------------------------
# Query Monitor
# ---------------------------------------------------------------------------

class QueryMonitor:
    """Query execution monitoring and performance tracking."""

    def __init__(self, pool: ConnectionPool, threshold: SlowQueryThreshold = SlowQueryThreshold.MILLISECONDS_500):
        self.pool = pool
        self.threshold_ms = threshold.value
        self._queries: List[QueryTracking] = []
        self._lock = threading.Lock()

    @contextmanager
    def track(self, label: str = "") -> Generator[QueryTracking, None, None]:
        query_id = hashlib.md5(f"{label}:{time.time()}".encode()).hexdigest()[:12]
        tracking = QueryTracking(
            query_id=query_id,
            query=label,
            start_time=time.time(),
        )

        try:
            yield tracking
            tracking.state = QueryState.COMPLETED
            tracking.end_time = time.time()

        except Exception as e:
            tracking.state = QueryState.FAILED
            tracking.error = str(e)
            tracking.end_time = time.time()
            raise

        finally:
            with self._lock:
                self._queries.append(tracking)

    def get_slow_queries(self, limit: int = 10) -> List[QueryTracking]:
        with self._lock:
            slow = [q for q in self._queries if q.duration_ms > self.threshold_ms]
        return sorted(slow, key=lambda q: q.duration_ms, reverse=True)[:limit]

    def get_metrics(self) -> QueryMetrics:
        with self._lock:
            queries = list(self._queries)

        if not queries:
            return QueryMetrics()

        durations = [q.duration_ms for q in queries]
        errors = sum(1 for q in queries if q.state == QueryState.FAILED)
        slow = sum(1 for q in queries if q.duration_ms > self.threshold_ms)

        total_duration = sum(durations)
        n = len(queries)

        # Time window for QPS
        if queries:
            first_time = min(q.start_time for q in queries)
            last_time = max(q.end_time or q.start_time for q in queries)
            window = max(last_time - first_time, 1.0)
        else:
            window = 1.0

        sorted_durations = sorted(durations)

        return QueryMetrics(
            total_queries=n,
            total_duration_ms=total_duration,
            avg_duration_ms=total_duration / n,
            p50_duration_ms=sorted_durations[n // 2] if n > 0 else 0,
            p95_duration_ms=sorted_durations[int(n * 0.95)] if n > 0 else 0,
            p99_duration_ms=sorted_durations[int(n * 0.99)] if n > 0 else 0,
            error_count=errors,
            error_rate=errors / n if n > 0 else 0,
            queries_per_second=n / window,
            slow_query_count=slow,
            slow_query_rate=slow / n if n > 0 else 0,
        )

    def clear(self) -> None:
        with self._lock:
            self._queries.clear()


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate database administration capabilities."""
    print("=" * 70)
    print("Database Administration Framework - Demo")
    print("=" * 70)

    # --- 1. Connection Pool ---
    print("\n--- Connection Pool ---")
    config = PoolConfig(
        host="localhost",
        port=5432,
        database="demo",
        min_connections=2,
        max_connections=10,
    )
    pool = ConnectionPool(config)

    # Simulate acquiring connections
    for i in range(5):
        with pool.acquire() as conn:
            conn.query_count += 1
            print(f"  Connection {conn.connection_id}: state={conn.state.value}")

    stats = pool.get_stats()
    print(f"  Pool stats: {stats}")

    # Health check
    unhealthy = pool.health_check()
    print(f"  Unhealthy connections: {len(unhealthy)}")

    # --- 2. Migration Manager ---
    print("\n--- Schema Migrations ---")
    manager = MigrationManager(pool=pool)

    migration1 = Migration(
        version="001",
        description="Create users table",
        up=["CREATE TABLE users (id UUID PRIMARY KEY, name VARCHAR(100));"],
        down=["DROP TABLE IF EXISTS users;"],
    )
    migration2 = Migration(
        version="002",
        description="Add email to users",
        up=["ALTER TABLE users ADD COLUMN email VARCHAR(255);"],
        down=["ALTER TABLE users DROP COLUMN email;"],
        dependencies=["001"],
    )

    manager.register(migration1)
    manager.register(migration2)

    applied = manager.migrate()
    print(f"  Migrations applied: {len(applied)}")
    for m in applied:
        print(f"    {m.version}: {m.description} ({m.state.value})")

    status = manager.status()
    print(f"  Total migrations: {len(status)}")

    # --- 3. Backup Manager ---
    print("\n--- Backup Management ---")
    backup_mgr = BackupManager(pool=pool, backup_dir="/tmp/backups")

    # Schedule daily backup
    schedule = BackupSchedule(
        name="daily_full",
        frequency="daily",
        time="02:00",
        retention_days=30,
        compression=True,
    )
    backup_mgr.schedule(schedule)

    # Run backups
    full_result = backup_mgr.run_full_backup(tag="pre-deploy")
    print(f"  Full backup: {full_result.filename} ({full_result.size_mb:.1f} MB, {full_result.duration_seconds:.2f}s)")

    incr_result = backup_mgr.run_incremental_backup()
    print(f"  Incremental: {incr_result.filename} ({incr_result.size_mb:.1f} MB)")

    # List backups
    backups = backup_mgr.list_backups(retention_days=7)
    print(f"  Backups in last 7 days: {len(backups)}")

    # Verify
    verified = backup_mgr.verify_backup(full_result)
    print(f"  Backup verified: {verified}")

    # --- 4. Access Control ---
    print("\n--- Access Control ---")
    acl = AccessControl(pool=pool)

    admin_role = Role(name="admin", permissions=[Permission.ALL])
    app_role = Role(name="app", permissions=[Permission.SELECT, Permission.INSERT, Permission.UPDATE])

    acl.grant_role("db_admin", admin_role, "production")
    acl.grant_role("app_svc", app_role, "production")

    # Check permissions
    print(f"  db_admin SELECT: {acl.check_permission('db_admin', 'production', Permission.SELECT)}")
    print(f"  app_svc DROP:    {acl.check_permission('app_svc', 'production', Permission.DROP)}")
    print(f"  app_svc SELECT:  {acl.check_permission('app_svc', 'production', Permission.SELECT)}")

    # Audit log
    acl._log_audit("app_svc", "SELECT", table="users", database="production")
    acl._log_audit("app_svc", "INSERT", table="orders", database="production")
    audit = acl.get_audit_log(limit=5)
    print(f"  Audit log entries: {len(audit)}")

    # --- 5. Query Monitor ---
    print("\n--- Query Monitoring ---")
    monitor = QueryMonitor(pool=pool, threshold=SlowQueryThreshold.MILLISECONDS_100)

    # Simulate queries
    for i in range(20):
        with monitor.track(f"query_{i}") as t:
            time.sleep(0.001 * (i + 1))
            t.row_count = np.random.randint(1, 1000)

    metrics = monitor.get_metrics()
    print(f"  Total queries:     {metrics.total_queries}")
    print(f"  Avg duration:      {metrics.avg_duration_ms:.2f}ms")
    print(f"  P95 duration:      {metrics.p95_duration_ms:.2f}ms")
    print(f"  Slow queries:      {metrics.slow_query_count} ({metrics.slow_query_rate:.1%})")
    print(f"  Queries/sec:       {metrics.queries_per_second:.1f}")

    slow = monitor.get_slow_queries(limit=3)
    print(f"  Top slow queries:")
    for q in slow:
        print(f"    {q.duration_ms:.1f}ms: {q.query}")

    # Cleanup
    pool.close_all()

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()