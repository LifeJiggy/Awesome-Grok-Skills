"""
Database Administration Agent - Database management, backup/recovery, performance tuning, replication, security, and monitoring.

Provides comprehensive database lifecycle management including instance provisioning,
schema management, backup and recovery operations, performance analysis and tuning,
replication topology management, security auditing, capacity planning, and real-time
monitoring with alerting.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import random
import re
import statistics
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum, auto
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class DatabaseEngine(Enum):
    """Supported database engines."""
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MARIADB = "mariadb"
    SQLITE = "sqlite"
    MONGODB = "mongodb"
    REDIS = "redis"
    ELASTICSEARCH = "elasticsearch"
    CLICKHOUSE = "clickhouse"
    CASSANDRA = "cassandra"
    DYNAMODB = "dynamodb"


class InstanceStatus(Enum):
    """Database instance status."""
    RUNNING = "running"
    STOPPED = "stopped"
    MAINTENANCE = "maintenance"
    SCALING = "scaling"
    RECOVERING = "recovering"
    FAILED = "failed"
    PROVISIONING = "provisioning"


class BackupType(Enum):
    """Types of database backups."""
    FULL = "full"
    INCREMENTAL = "incremental"
    DIFFERENTIAL = "differential"
    SNAPSHOT = "snapshot"
    WAL_ARCHIVE = "wal_archive"
    LOGICAL_DUMP = "logical_dump"
    CONTINUOUS = "continuous"


class BackupStatus(Enum):
    """Status of a backup operation."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"
    DELETED = "deleted"


class ReplicationRole(Enum):
    """Role in a replication topology."""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    REPLICA = "replica"
    READ_REPLICA = "read_replica"
    CASCADING = "cascading"


class ReplicationStatus(Enum):
    """Status of a replication link."""
    HEALTHY = "healthy"
    LAGGING = "lagging"
    DISCONNECTED = "disconnected"
    REBUILDING = "rebuilding"
    FAILED = "failed"


class SecurityLevel(Enum):
    """Security audit levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AlertSeverity(Enum):
    """Alert severity for monitoring."""
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"
    RESOLVED = "resolved"


class MetricType(Enum):
    """Types of performance metrics."""
    QUERY_TIME = "query_time"
    THROUGHPUT = "throughput"
    CONNECTIONS = "connections"
    DISK_USAGE = "disk_usage"
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    CACHE_HIT_RATIO = "cache_hit_ratio"
    INDEX_USAGE = "index_usage"
    LOCK_WAIT = "lock_wait"
    REPLICATION_LAG = "replication_lag"
    ROWS_READ = "rows_read"
    ROWS_WRITTEN = "rows_written"
    SLOW_QUERIES = "slow_queries"
    DEADLOCKS = "deadlocks"
    TRANSACTION_RATE = "transaction_rate"


class SchemaChangeType(Enum):
    """Types of schema changes."""
    CREATE_TABLE = "create_table"
    DROP_TABLE = "drop_table"
    ADD_COLUMN = "add_column"
    DROP_COLUMN = "drop_column"
    ALTER_COLUMN = "alter_column"
    ADD_INDEX = "add_index"
    DROP_INDEX = "drop_index"
    ADD_CONSTRAINT = "add_constraint"
    DROP_CONSTRAINT = "drop_constraint"
    RENAME_TABLE = "rename_table"
    RENAME_COLUMN = "rename_column"


class CapacityTrend(Enum):
    """Trend direction for capacity planning."""
    GROWING = "growing"
    STABLE = "stable"
    SHRINKING = "shrinking"
    VOLATILE = "volatile"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class DatabaseInstance:
    """Represents a database instance."""
    instance_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    name: str = ""
    engine: DatabaseEngine = DatabaseEngine.POSTGRESQL
    host: str = "localhost"
    port: int = 5432
    database: str = ""
    status: InstanceStatus = InstanceStatus.RUNNING
    version: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tags: Dict[str, str] = field(default_factory=dict)
    config: Dict[str, Any] = field(default_factory=dict)
    region: str = ""
    size: str = ""  # e.g., "db.r5.large"
    storage_gb: float = 0.0
    storage_used_gb: float = 0.0
    storage_free_gb: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "name": self.name,
            "engine": self.engine.value,
            "host": self.host,
            "port": self.port,
            "database": self.database,
            "status": self.status.value,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "tags": self.tags,
            "region": self.region,
            "size": self.size,
            "storage_gb": self.storage_gb,
            "storage_used_gb": self.storage_used_gb,
            "storage_free_gb": self.storage_free_gb,
        }


@dataclass
class BackupRecord:
    """Record of a backup operation."""
    backup_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    instance_id: str = ""
    backup_type: BackupType = BackupType.FULL
    status: BackupStatus = BackupStatus.PENDING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: float = 0.0
    size_bytes: int = 0
    compressed: bool = True
    encrypted: bool = True
    location: str = ""
    retention_days: int = 30
    restorable: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "backup_id": self.backup_id,
            "instance_id": self.instance_id,
            "backup_type": self.backup_type.value,
            "status": self.status.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": round(self.duration_seconds, 2),
            "size_bytes": self.size_bytes,
            "compressed": self.compressed,
            "encrypted": self.encrypted,
            "location": self.location,
            "retention_days": self.retention_days,
            "restorable": self.restorable,
        }


@dataclass
class ReplicationLink:
    """Represents a replication relationship between instances."""
    link_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    source_id: str = ""
    target_id: str = ""
    role: ReplicationRole = ReplicationRole.REPLICA
    status: ReplicationStatus = ReplicationStatus.HEALTHY
    lag_seconds: float = 0.0
    lag_bytes: int = 0
    last_heartbeat: Optional[datetime] = None
    sync_mode: str = "async"  # async, sync, semi-sync
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "link_id": self.link_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "role": self.role.value,
            "status": self.status.value,
            "lag_seconds": round(self.lag_seconds, 2),
            "lag_bytes": self.lag_bytes,
            "last_heartbeat": self.last_heartbeat.isoformat() if self.last_heartbeat else None,
            "sync_mode": self.sync_mode,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class SecurityFinding:
    """A security audit finding."""
    finding_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    instance_id: str = ""
    level: SecurityLevel = SecurityLevel.INFO
    category: str = ""
    title: str = ""
    description: str = ""
    recommendation: str = ""
    cwe_id: str = ""
    compliance_frameworks: List[str] = field(default_factory=list)
    detected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    remediated: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "instance_id": self.instance_id,
            "level": self.level.value,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "recommendation": self.recommendation,
            "cwe_id": self.cwe_id,
            "compliance_frameworks": self.compliance_frameworks,
            "detected_at": self.detected_at.isoformat(),
            "remediated": self.remediated,
        }


@dataclass
class PerformanceMetric:
    """A single performance metric data point."""
    metric_type: MetricType = MetricType.QUERY_TIME
    value: float = 0.0
    unit: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    instance_id: str = ""
    database: str = ""
    tags: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_type": self.metric_type.value,
            "value": round(self.value, 4),
            "unit": self.unit,
            "timestamp": self.timestamp.isoformat(),
            "instance_id": self.instance_id,
            "database": self.database,
            "tags": self.tags,
        }


@dataclass
class PerformanceAnalysis:
    """Analysis results for database performance."""
    instance_id: str = ""
    analyzed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    overall_health: str = "good"  # good, warning, critical
    metrics_summary: Dict[str, Dict[str, float]] = field(default_factory=dict)
    slow_queries: List[Dict[str, Any]] = field(default_factory=list)
    index_recommendations: List[Dict[str, Any]] = field(default_factory=list)
    config_recommendations: List[Dict[str, Any]] = field(default_factory=list)
    bottlenecks: List[str] = field(default_factory=list)
    score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "analyzed_at": self.analyzed_at.isoformat(),
            "overall_health": self.overall_health,
            "metrics_summary": self.metrics_summary,
            "slow_queries": self.slow_queries[:20],
            "index_recommendations": self.index_recommendations[:20],
            "config_recommendations": self.config_recommendations[:10],
            "bottlenecks": self.bottlenecks,
            "score": round(self.score, 2),
        }


@dataclass
class SchemaChange:
    """Record of a schema change operation."""
    change_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    instance_id: str = ""
    change_type: SchemaChangeType = SchemaChangeType.CREATE_TABLE
    object_name: str = ""
    sql_statement: str = ""
    executed_by: str = "system"
    executed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    duration_ms: float = 0.0
    reversible: bool = True
    rollback_sql: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "change_id": self.change_id,
            "instance_id": self.instance_id,
            "change_type": self.change_type.value,
            "object_name": self.object_name,
            "sql_statement": self.sql_statement[:500],
            "executed_by": self.executed_by,
            "executed_at": self.executed_at.isoformat(),
            "duration_ms": round(self.duration_ms, 2),
            "reversible": self.reversible,
        }


@dataclass
class CapacityForecast:
    """Capacity planning forecast for an instance."""
    instance_id: str = ""
    metric: str = ""
    current_value: float = 0.0
    projected_value_30d: float = 0.0
    projected_value_90d: float = 0.0
    projected_value_365d: float = 0.0
    trend: CapacityTrend = CapacityTrend.STABLE
    growth_rate_daily: float = 0.0
    days_until_full: Optional[int] = None
    recommendation: str = ""
    unit: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "metric": self.metric,
            "current_value": round(self.current_value, 2),
            "projected_value_30d": round(self.projected_value_30d, 2),
            "projected_value_90d": round(self.projected_value_90d, 2),
            "projected_value_365d": round(self.projected_value_365d, 2),
            "trend": self.trend.value,
            "growth_rate_daily": round(self.growth_rate_daily, 4),
            "days_until_full": self.days_until_full,
            "recommendation": self.recommendation,
            "unit": self.unit,
        }


@dataclass
class Alert:
    """A monitoring alert."""
    alert_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    instance_id: str = ""
    severity: AlertSeverity = AlertSeverity.INFO
    metric: str = ""
    message: str = ""
    current_value: Any = None
    threshold: Any = None
    fired_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None
    acknowledged: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "instance_id": self.instance_id,
            "severity": self.severity.value,
            "metric": self.metric,
            "message": self.message,
            "current_value": self.current_value,
            "threshold": self.threshold,
            "fired_at": self.fired_at.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "acknowledged": self.acknowledged,
        }


@dataclass
class RecoveryPlan:
    """A disaster recovery plan."""
    plan_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    name: str = ""
    instance_ids: List[str] = field(default_factory=list)
    rto_minutes: int = 60  # Recovery Time Objective
    rpo_minutes: int = 15  # Recovery Point Objective
    steps: List[Dict[str, Any]] = field(default_factory=list)
    last_tested: Optional[datetime] = None
    test_results: List[Dict[str, Any]] = field(default_factory=list)
    contacts: List[str] = field(default_factory=list)
    enabled: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "name": self.name,
            "instance_ids": self.instance_ids,
            "rto_minutes": self.rto_minutes,
            "rpo_minutes": self.rpo_minutes,
            "steps": self.steps,
            "last_tested": self.last_tested.isoformat() if self.last_tested else None,
            "test_results": self.test_results[-5:],
            "contacts": self.contacts,
            "enabled": self.enabled,
        }


@dataclass
class QueryPlan:
    """An analyzed query execution plan."""
    query_hash: str = ""
    query_text: str = ""
    execution_time_ms: float = 0.0
    rows_returned: int = 0
    rows_examined: int = 0
    full_table_scan: bool = False
    index_used: Optional[str] = None
    missing_indexes: List[str] = field(default_factory=list)
    optimization_suggestions: List[str] = field(default_factory=list)
    cost_estimate: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query_hash": self.query_hash,
            "query_text": self.query_text[:300],
            "execution_time_ms": round(self.execution_time_ms, 2),
            "rows_returned": self.rows_returned,
            "rows_examined": self.rows_examined,
            "full_table_scan": self.full_table_scan,
            "index_used": self.index_used,
            "missing_indexes": self.missing_indexes,
            "optimization_suggestions": self.optimization_suggestions,
            "cost_estimate": round(self.cost_estimate, 2),
        }


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class DatabaseAdminConfig:
    """Configuration for the Database Admin Agent."""
    # Backup settings
    default_backup_type: BackupType = BackupType.FULL
    default_retention_days: int = 30
    max_concurrent_backups: int = 3
    backup_timeout_seconds: int = 3600
    enable_compression: bool = True
    enable_encryption: bool = True

    # Replication settings
    max_replication_lag_seconds: float = 30.0
    replication_heartbeat_interval_seconds: int = 10
    auto_failover_enabled: bool = True
    failover_timeout_seconds: int = 60

    # Performance thresholds
    slow_query_threshold_ms: float = 1000.0
    connection_warning_threshold: float = 0.80
    connection_critical_threshold: float = 0.95
    disk_warning_threshold: float = 0.75
    disk_critical_threshold: float = 0.90
    cpu_warning_threshold: float = 0.70
    cpu_critical_threshold: float = 0.90
    memory_warning_threshold: float = 0.80
    memory_critical_threshold: float = 0.95
    cache_hit_ratio_warning: float = 0.95
    deadlock_warning_count: int = 5

    # Security settings
    require_ssl: bool = True
    password_policy_min_length: int = 12
    password_policy_require_uppercase: bool = True
    password_policy_require_numbers: bool = True
    password_policy_require_special: bool = True
    max_failed_logins: int = 5
    lockout_duration_minutes: int = 30
    audit_logging_enabled: bool = True
    encryption_at_rest: bool = True

    # Capacity planning
    forecast_days: List[int] = field(default_factory=lambda: [30, 90, 365])
    growth_rate_window_days: int = 30
    capacity_alert_days: int = 30

    # Monitoring
    metrics_retention_days: int = 90
    alert_cooldown_minutes: int = 15
    enable_real_time_monitoring: bool = True

    # Schema management
    require_approval_for_ddl: bool = True
    auto_backup_before_schema_change: bool = True
    track_schema_history: bool = True

    # Instance management
    default_engine: DatabaseEngine = DatabaseEngine.POSTGRESQL
    default_port: int = 5432
    connection_pool_min: int = 5
    connection_pool_max: int = 20
    query_timeout_seconds: int = 30


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def _generate_query_hash(query: str) -> str:
    """Generate a hash for query identification."""
    normalized = re.sub(r"\s+", " ", query.strip().lower())
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]


def _parse_duration_ms(start: datetime, end: datetime) -> float:
    """Calculate duration in milliseconds between two timestamps."""
    return (end - start).total_seconds() * 1000


def _estimate_size_bytes(rows: int, avg_row_size: int = 256) -> int:
    """Estimate size in bytes based on row count."""
    return rows * avg_row_size


def _compute_growth_rate(values: List[float], window: int = 7) -> float:
    """Compute average daily growth rate over a window."""
    if len(values) < 2:
        return 0.0
    recent = values[-window:] if len(values) >= window else values
    if len(recent) < 2:
        return 0.0
    diffs = [recent[i] - recent[i - 1] for i in range(1, len(recent))]
    return statistics.mean(diffs) if diffs else 0.0


def _project_value(current: float, daily_rate: float, days: int) -> float:
    """Project a value forward by a number of days."""
    return current + daily_rate * days


def _health_from_score(score: float) -> str:
    """Convert a numeric health score to a status string."""
    if score >= 80:
        return "good"
    elif score >= 50:
        return "warning"
    return "critical"


# ---------------------------------------------------------------------------
# Core Agent
# ---------------------------------------------------------------------------

class DatabaseAdminAgent:
    """
    Enterprise-grade Database Administration Agent providing instance management,
    backup/recovery, performance tuning, replication management, security auditing,
    capacity planning, and monitoring.
    """

    def __init__(self, config: Optional[DatabaseAdminConfig] = None):
        self._config = config or DatabaseAdminConfig()
        self._instances: Dict[str, DatabaseInstance] = {}
        self._backups: Dict[str, List[BackupRecord]] = defaultdict(list)
        self._replication_links: Dict[str, ReplicationLink] = {}
        self._security_findings: List[SecurityFinding] = []
        self._performance_metrics: Dict[str, List[PerformanceMetric]] = defaultdict(list)
        self._schema_history: List[SchemaChange] = []
        self._alerts: List[Alert] = []
        self._recovery_plans: Dict[str, RecoveryPlan] = {}
        self._query_plans: Dict[str, List[QueryPlan]] = defaultdict(list)
        logger.info("DatabaseAdminAgent initialized")

    # -----------------------------------------------------------------------
    # Instance Management
    # -----------------------------------------------------------------------

    def register_instance(
        self,
        name: str,
        engine: DatabaseEngine = DatabaseEngine.POSTGRESQL,
        host: str = "localhost",
        port: int = 5432,
        database: str = "",
        **kwargs: Any,
    ) -> DatabaseInstance:
        """Register a database instance for management."""
        instance = DatabaseInstance(
            name=name,
            engine=engine,
            host=host,
            port=port,
            database=database or name,
            version=kwargs.get("version", ""),
            region=kwargs.get("region", ""),
            size=kwargs.get("size", ""),
            storage_gb=kwargs.get("storage_gb", 0.0),
            tags=kwargs.get("tags", {}),
            config=kwargs.get("config", {}),
        )
        self._instances[instance.instance_id] = instance
        logger.info("Registered instance '%s' (%s) at %s:%d", name, engine.value, host, port)
        return instance

    def get_instance(self, instance_id: str) -> DatabaseInstance:
        """Retrieve a registered instance."""
        if instance_id not in self._instances:
            raise KeyError(f"Instance '{instance_id}' not found")
        return self._instances[instance_id]

    def list_instances(
        self,
        engine: Optional[DatabaseEngine] = None,
        status: Optional[InstanceStatus] = None,
        region: Optional[str] = None,
    ) -> List[DatabaseInstance]:
        """List instances with optional filters."""
        results = list(self._instances.values())
        if engine:
            results = [i for i in results if i.engine == engine]
        if status:
            results = [i for i in results if i.status == status]
        if region:
            results = [i for i in results if i.region == region]
        return results

    def update_instance_status(self, instance_id: str, status: InstanceStatus) -> Dict[str, Any]:
        """Update the status of a database instance."""
        instance = self.get_instance(instance_id)
        old_status = instance.status
        instance.status = status
        logger.info("Instance '%s' status: %s -> %s", instance.name, old_status.value, status.value)
        return {
            "instance_id": instance_id,
            "old_status": old_status.value,
            "new_status": status.value,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

    def deprovision_instance(self, instance_id: str, force: bool = False) -> Dict[str, Any]:
        """Decommission and remove a database instance."""
        instance = self.get_instance(instance_id)
        if not force and instance.status == InstanceStatus.RUNNING:
            raise RuntimeError("Cannot deprovision a running instance. Stop it first or use force=True.")
        del self._instances[instance_id]
        logger.info("Deprovisioned instance '%s' (%s)", instance.name, instance_id)
        return {
            "instance_id": instance_id,
            "name": instance.name,
            "deprovisioned_at": datetime.now(timezone.utc).isoformat(),
        }

    # -----------------------------------------------------------------------
    # Backup Management
    # -----------------------------------------------------------------------

    def create_backup(
        self,
        instance_id: str,
        backup_type: BackupType = BackupType.FULL,
        retention_days: int = 30,
    ) -> BackupRecord:
        """Create a backup of a database instance."""
        instance = self.get_instance(instance_id)
        record = BackupRecord(
            instance_id=instance_id,
            backup_type=backup_type,
            status=BackupStatus.RUNNING,
            started_at=datetime.now(timezone.utc),
            retention_days=retention_days,
            compressed=self._config.enable_compression,
            encrypted=self._config.enable_encryption,
            location=f"s3://backups/{instance.name}/{backup_type.value}",
        )
        self._backups[instance_id].append(record)

        # Simulate backup completion
        record.status = BackupStatus.COMPLETED
        record.completed_at = datetime.now(timezone.utc)
        record.duration_seconds = random.uniform(10, 300)
        record.size_bytes = int(instance.storage_used_gb * 1024 * 1024 * 1024 * 0.1)

        logger.info("Backup '%s' completed for instance '%s' (%.1fs)",
                     record.backup_id, instance.name, record.duration_seconds)
        return record

    def list_backups(
        self,
        instance_id: str,
        backup_type: Optional[BackupType] = None,
        status: Optional[BackupStatus] = None,
    ) -> List[BackupRecord]:
        """List backups for an instance."""
        backups = self._backups.get(instance_id, [])
        if backup_type:
            backups = [b for b in backups if b.backup_type == backup_type]
        if status:
            backups = [b for b in backups if b.status == status]
        return backups

    def restore_backup(self, backup_id: str, target_instance_id: Optional[str] = None) -> Dict[str, Any]:
        """Restore a database from a backup."""
        for iid, backups in self._backups.items():
            for backup in backups:
                if backup.backup_id == backup_id:
                    if not backup.restorable:
                        raise RuntimeError(f"Backup '{backup_id}' is not restorable")
                    restore_to = target_instance_id or backup.instance_id
                    self.get_instance(restore_to)
                    logger.info("Restoring backup '%s' to instance '%s'", backup_id, restore_to)
                    return {
                        "backup_id": backup_id,
                        "target_instance": restore_to,
                        "restore_started": datetime.now(timezone.utc).isoformat(),
                        "estimated_duration_seconds": backup.duration_seconds * 0.5,
                    }
        raise KeyError(f"Backup '{backup_id}' not found")

    def get_latest_backup(self, instance_id: str) -> Optional[BackupRecord]:
        """Get the most recent completed backup for an instance."""
        backups = self.list_backups(instance_id, status=BackupStatus.COMPLETED)
        if not backups:
            return None
        return max(backups, key=lambda b: b.completed_at or datetime.min.replace(tzinfo=timezone.utc))

    def cleanup_expired_backups(self, instance_id: str) -> Dict[str, Any]:
        """Remove backups that have exceeded their retention period."""
        now = datetime.now(timezone.utc)
        backups = self._backups.get(instance_id, [])
        expired = []
        retained = []
        for backup in backups:
            if backup.completed_at:
                age_days = (now - backup.completed_at).days
                if age_days > backup.retention_days:
                    expired.append(backup)
                else:
                    retained.append(backup)
            else:
                retained.append(backup)
        self._backups[instance_id] = retained
        logger.info("Cleaned up %d expired backups for instance '%s'", len(expired), instance_id)
        return {
            "instance_id": instance_id,
            "expired_removed": len(expired),
            "retained": len(retained),
            "cleanup_date": now.isoformat(),
        }

    # -----------------------------------------------------------------------
    # Performance Tuning
    # -----------------------------------------------------------------------

    def record_metric(self, metric: PerformanceMetric) -> None:
        """Record a performance metric data point."""
        self._performance_metrics[metric.instance_id].append(metric)

    def analyze_performance(self, instance_id: str) -> PerformanceAnalysis:
        """Analyze performance metrics for an instance."""
        self.get_instance(instance_id)
        metrics = self._performance_metrics.get(instance_id, [])
        analysis = PerformanceAnalysis(instance_id=instance_id)

        if not metrics:
            analysis.overall_health = "unknown"
            analysis.score = 0.0
            return analysis

        # Group metrics by type
        by_type: Dict[str, List[float]] = defaultdict(list)
        for m in metrics:
            by_type[m.metric_type.value].append(m.value)

        # Summarize
        for mtype, values in by_type.items():
            analysis.metrics_summary[mtype] = {
                "min": min(values),
                "max": max(values),
                "mean": statistics.mean(values),
                "p50": statistics.median(values),
                "p95": sorted(values)[int(len(values) * 0.95)] if len(values) > 1 else values[0],
                "p99": sorted(values)[int(len(values) * 0.99)] if len(values) > 1 else values[0],
            }

        # Identify bottlenecks
        bottlenecks = []
        score = 100.0

        query_times = by_type.get(MetricType.QUERY_TIME.value, [])
        if query_times:
            avg_query = statistics.mean(query_times)
            if avg_query > self._config.slow_query_threshold_ms:
                bottlenecks.append(f"High average query time: {avg_query:.1f}ms")
                score -= 20

        connections = by_type.get(MetricType.CONNECTIONS.value, [])
        if connections:
            max_conn = max(connections)
            if max_conn > self._config.connection_critical_threshold * 100:
                bottlenecks.append(f"Connection pool near capacity: {max_conn:.0f}")
                score -= 15
            elif max_conn > self._config.connection_warning_threshold * 100:
                bottlenecks.append(f"Connection pool usage elevated: {max_conn:.0f}")
                score -= 5

        disk = by_type.get(MetricType.DISK_USAGE.value, [])
        if disk:
            max_disk = max(disk)
            if max_disk > self._config.disk_critical_threshold * 100:
                bottlenecks.append(f"Disk usage critical: {max_disk:.1f}%")
                score -= 25
            elif max_disk > self._config.disk_warning_threshold * 100:
                bottlenecks.append(f"Disk usage high: {max_disk:.1f}%")
                score -= 10

        cache_hit = by_type.get(MetricType.CACHE_HIT_RATIO.value, [])
        if cache_hit:
            min_cache = min(cache_hit)
            if min_cache < self._config.cache_hit_ratio_warning * 100:
                bottlenecks.append(f"Cache hit ratio low: {min_cache:.1f}%")
                score -= 15

        deadlocks = by_type.get(MetricType.DEADLOCKS.value, [])
        if deadlocks:
            total_deadlocks = sum(deadlocks)
            if total_deadlocks > self._config.deadlock_warning_count:
                bottlenecks.append(f"High deadlock count: {total_deadlocks:.0f}")
                score -= 10

        lock_wait = by_type.get(MetricType.LOCK_WAIT.value, [])
        if lock_wait:
            avg_lock = statistics.mean(lock_wait)
            if avg_lock > 100:
                bottlenecks.append(f"High lock wait time: {avg_lock:.1f}ms")
                score -= 10

        analysis.bottlenecks = bottlenecks
        analysis.score = max(0.0, score)
        analysis.overall_health = _health_from_score(score)

        # Generate index recommendations
        analysis.index_recommendations = self._generate_index_recommendations(instance_id)

        # Generate config recommendations
        analysis.config_recommendations = self._generate_config_recommendations(analysis)

        return analysis

    def _generate_index_recommendations(self, instance_id: str) -> List[Dict[str, Any]]:
        """Generate index optimization recommendations."""
        plans = self._query_plans.get(instance_id, [])
        recommendations = []
        for plan in plans[:20]:
            if plan.full_table_scan and plan.rows_examined > 10000:
                recommendations.append({
                    "type": "add_index",
                    "query_hash": plan.query_hash,
                    "suggestion": f"Add index for query scanning {plan.rows_examined} rows",
                    "missing_columns": plan.missing_indexes,
                    "estimated_improvement": f"{plan.execution_time_ms:.0f}ms -> ~{plan.execution_time_ms * 0.1:.0f}ms",
                })
        return recommendations

    def _generate_config_recommendations(self, analysis: PerformanceAnalysis) -> List[Dict[str, Any]]:
        """Generate configuration optimization recommendations."""
        recommendations = []
        conn_stats = analysis.metrics_summary.get("connections", {})
        if conn_stats.get("p95", 0) > self._config.connection_warning_threshold * 100:
            recommendations.append({
                "parameter": "max_connections",
                "current": "auto",
                "recommended": "increase by 20%",
                "reason": "Connection pool usage consistently above 80%",
            })
        cache_stats = analysis.metrics_summary.get("cache_hit_ratio", {})
        if cache_stats.get("min", 100) < self._config.cache_hit_ratio_warning * 100:
            recommendations.append({
                "parameter": "shared_buffers",
                "current": "auto",
                "recommended": "increase by 25%",
                "reason": "Cache hit ratio below 95%",
            })
        return recommendations

    def record_query_plan(self, instance_id: str, plan: QueryPlan) -> None:
        """Record a query execution plan for analysis."""
        self._query_plans[instance_id].append(plan)

    def get_slow_queries(self, instance_id: str, threshold_ms: Optional[float] = None) -> List[QueryPlan]:
        """Get queries exceeding the slow query threshold."""
        threshold = threshold_ms or self._config.slow_query_threshold_ms
        plans = self._query_plans.get(instance_id, [])
        return [p for p in plans if p.execution_time_ms > threshold]

    # -----------------------------------------------------------------------
    # Replication Management
    # -----------------------------------------------------------------------

    def add_replication_link(
        self,
        source_id: str,
        target_id: str,
        role: ReplicationRole = ReplicationRole.REPLICA,
        sync_mode: str = "async",
    ) -> ReplicationLink:
        """Create a replication link between two instances."""
        self.get_instance(source_id)
        self.get_instance(target_id)
        link = ReplicationLink(
            source_id=source_id,
            target_id=target_id,
            role=role,
            sync_mode=sync_mode,
            last_heartbeat=datetime.now(timezone.utc),
        )
        self._replication_links[link.link_id] = link
        logger.info("Replication link created: %s -> %s (%s, %s)",
                     source_id, target_id, role.value, sync_mode)
        return link

    def get_replication_status(self, source_id: Optional[str] = None) -> List[ReplicationLink]:
        """Get replication status, optionally filtered by source."""
        links = list(self._replication_links.values())
        if source_id:
            links = [l for l in links if l.source_id == source_id]
        return links

    def update_replication_lag(self, link_id: str, lag_seconds: float) -> Dict[str, Any]:
        """Update replication lag for a link."""
        if link_id not in self._replication_links:
            raise KeyError(f"Replication link '{link_id}' not found")
        link = self._replication_links[link_id]
        link.lag_seconds = lag_seconds
        link.last_heartbeat = datetime.now(timezone.utc)
        if lag_seconds > self._config.max_replication_lag_seconds:
            link.status = ReplicationStatus.LAGGING
            logger.warning("Replication link '%s' lagging: %.1fs", link_id, lag_seconds)
        else:
            link.status = ReplicationStatus.HEALTHY
        return link.to_dict()

    def get_replication_summary(self) -> Dict[str, Any]:
        """Get an overview of all replication links."""
        links = list(self._replication_links.values())
        return {
            "total_links": len(links),
            "healthy": sum(1 for l in links if l.status == ReplicationStatus.HEALTHY),
            "lagging": sum(1 for l in links if l.status == ReplicationStatus.LAGGING),
            "disconnected": sum(1 for l in links if l.status == ReplicationStatus.DISCONNECTED),
            "failed": sum(1 for l in links if l.status == ReplicationStatus.FAILED),
            "max_lag_seconds": max((l.lag_seconds for l in links), default=0.0),
            "avg_lag_seconds": statistics.mean([l.lag_seconds for l in links]) if links else 0.0,
        }

    def failover(self, source_id: str, target_id: str) -> Dict[str, Any]:
        """Execute a failover from source to target instance."""
        if not self._config.auto_failover_enabled:
            raise RuntimeError("Auto-failover is disabled in configuration")
        source = self.get_instance(source_id)
        target = self.get_instance(target_id)

        # Promote target
        target.status = InstanceStatus.RUNNING
        # Demote source
        source.status = InstanceStatus.FAILED

        logger.warning("Failover executed: %s -> %s", source_id, target_id)
        return {
            "failover_id": uuid.uuid4().hex[:8],
            "source": source_id,
            "target": target_id,
            "executed_at": datetime.now(timezone.utc).isoformat(),
            "source_new_status": source.status.value,
            "target_new_status": target.status.value,
        }

    # -----------------------------------------------------------------------
    # Security Auditing
    # -----------------------------------------------------------------------

    def run_security_audit(self, instance_id: str) -> List[SecurityFinding]:
        """Run a comprehensive security audit on an instance."""
        instance = self.get_instance(instance_id)
        findings: List[SecurityFinding] = []

        # Check SSL configuration
        if not instance.config.get("ssl_enabled", False) and self._config.require_ssl:
            findings.append(SecurityFinding(
                instance_id=instance_id,
                level=SecurityLevel.HIGH,
                category="encryption",
                title="SSL/TLS not enabled",
                description=f"Instance '{instance.name}' does not have SSL/TLS enabled for connections.",
                recommendation="Enable SSL/TLS for all client connections to encrypt data in transit.",
                cwe_id="CWE-319",
                compliance_frameworks=["PCI-DSS", "HIPAA", "SOC2"],
            ))

        # Check encryption at rest
        if not instance.config.get("encryption_at_rest", False) and self._config.encryption_at_rest:
            findings.append(SecurityFinding(
                instance_id=instance_id,
                level=SecurityLevel.CRITICAL,
                category="encryption",
                title="Encryption at rest not enabled",
                description=f"Instance '{instance.name}' does not have encryption at rest enabled.",
                recommendation="Enable encryption at rest to protect stored data.",
                cwe_id="CWE-311",
                compliance_frameworks=["PCI-DSS", "HIPAA", "SOC2", "GDPR"],
            ))

        # Check for default ports
        default_ports = {
            DatabaseEngine.POSTGRESQL: 5432,
            DatabaseEngine.MYSQL: 3306,
            DatabaseEngine.MONGODB: 27017,
            DatabaseEngine.REDIS: 6379,
            DatabaseEngine.ELASTICSEARCH: 9200,
        }
        if instance.port == default_ports.get(instance.engine):
            findings.append(SecurityFinding(
                instance_id=instance_id,
                level=SecurityLevel.MEDIUM,
                category="configuration",
                title="Using default port",
                description=f"Instance '{instance.name}' is using the default port {instance.port}.",
                recommendation="Change to a non-standard port to reduce automated attack surface.",
                cwe_id="CWE-16",
            ))

        # Check for public access
        if instance.host in ("0.0.0.0", "::", "0.0.0.0/0"):
            findings.append(SecurityFinding(
                instance_id=instance_id,
                level=SecurityLevel.CRITICAL,
                category="network",
                title="Instance accessible from all interfaces",
                description=f"Instance '{instance.name}' is bound to all network interfaces.",
                recommendation="Restrict to specific private IP addresses or use a VPN/bastion.",
                cwe_id="CWE-668",
            ))

        # Check audit logging
        if not instance.config.get("audit_logging", False) and self._config.audit_logging_enabled:
            findings.append(SecurityFinding(
                instance_id=instance_id,
                level=SecurityLevel.MEDIUM,
                category="auditing",
                title="Audit logging not enabled",
                description=f"Instance '{instance.name}' does not have audit logging enabled.",
                recommendation="Enable audit logging for compliance and forensic analysis.",
                cwe_id="CWE-778",
                compliance_frameworks=["PCI-DSS", "SOC2"],
            ))

        # Check password policy
        if not instance.config.get("password_policy_enforced", False):
            findings.append(SecurityFinding(
                instance_id=instance_id,
                level=SecurityLevel.HIGH,
                category="authentication",
                title="Custom password policy not enforced",
                description=f"Instance '{instance.name}' uses default password policy.",
                recommendation="Enforce minimum length, complexity, and rotation requirements.",
                cwe_id="CWE-521",
            ))

        # Check for public snapshots
        if instance.config.get("public_snapshot", False):
            findings.append(SecurityFinding(
                instance_id=instance_id,
                level=SecurityLevel.CRITICAL,
                category="data_exposure",
                title="Public database snapshot detected",
                description=f"Instance '{instance.name}' has a publicly accessible snapshot.",
                recommendation="Restrict snapshot access to authorized IAM roles only.",
                cwe_id="CWE-200",
                compliance_frameworks=["PCI-DSS", "HIPAA", "GDPR"],
            ))

        self._security_findings.extend(findings)
        logger.info("Security audit completed for '%s': %d findings", instance.name, len(findings))
        return findings

    def get_security_summary(self, instance_id: Optional[str] = None) -> Dict[str, Any]:
        """Get a summary of security findings."""
        findings = self._security_findings
        if instance_id:
            findings = [f for f in findings if f.instance_id == instance_id]
        by_level = defaultdict(int)
        for f in findings:
            by_level[f.level.value] += 1
        return {
            "total_findings": len(findings),
            "by_level": dict(by_level),
            "by_category": dict(Counter(f.category for f in findings)),
            "remediated": sum(1 for f in findings if f.remediated),
            "pending": sum(1 for f in findings if not f.remediated),
        }

    def remediate_finding(self, finding_id: str) -> Dict[str, Any]:
        """Mark a security finding as remediated."""
        for finding in self._security_findings:
            if finding.finding_id == finding_id:
                finding.remediated = True
                return finding.to_dict()
        raise KeyError(f"Finding '{finding_id}' not found")

    # -----------------------------------------------------------------------
    # Capacity Planning
    # -----------------------------------------------------------------------

    def forecast_capacity(
        self,
        instance_id: str,
        metric: str,
        current_value: float,
        historical_values: Optional[List[float]] = None,
    ) -> CapacityForecast:
        """Forecast capacity requirements for an instance."""
        instance = self.get_instance(instance_id)
        daily_rate = 0.0
        trend = CapacityTrend.STABLE

        if historical_values and len(historical_values) >= 2:
            daily_rate = _compute_growth_rate(historical_values, self._config.growth_rate_window_days)
            if daily_rate > 0.01 * current_value:
                trend = CapacityTrend.GROWING
            elif daily_rate < -0.01 * current_value:
                trend = CapacityTrend.SHRINKING
            else:
                trend = CapacityTrend.STABLE

        proj_30 = _project_value(current_value, daily_rate, 30)
        proj_90 = _project_value(current_value, daily_rate, 90)
        proj_365 = _project_value(current_value, daily_rate, 365)

        days_until_full = None
        if daily_rate > 0 and current_value > 0:
            capacity = instance.storage_gb if "storage" in metric else current_value * 2
            remaining = capacity - current_value
            if remaining > 0:
                days_until_full = int(remaining / daily_rate)

        recommendation = ""
        if days_until_full and days_until_full < self._config.capacity_alert_days:
            recommendation = f"Capacity will be exhausted in {days_until_full} days. Consider scaling up or archiving old data."
        elif trend == CapacityTrend.GROWING:
            recommendation = "Usage is growing. Monitor closely and plan for scaling."
        else:
            recommendation = "Capacity is stable. No immediate action needed."

        return CapacityForecast(
            instance_id=instance_id,
            metric=metric,
            current_value=current_value,
            projected_value_30d=proj_30,
            projected_value_90d=proj_90,
            projected_value_365d=proj_365,
            trend=trend,
            growth_rate_daily=daily_rate,
            days_until_full=days_until_full,
            recommendation=recommendation,
        )

    # -----------------------------------------------------------------------
    # Schema Management
    # -----------------------------------------------------------------------

    def record_schema_change(self, change: SchemaChange) -> SchemaChange:
        """Record a schema change in the history."""
        self._schema_history.append(change)
        logger.info("Schema change recorded: %s on '%s' (%.1fms)",
                     change.change_type.value, change.object_name, change.duration_ms)
        return change

    def get_schema_history(
        self,
        instance_id: Optional[str] = None,
        change_type: Optional[SchemaChangeType] = None,
        limit: int = 50,
    ) -> List[SchemaChange]:
        """Get schema change history."""
        history = self._schema_history
        if instance_id:
            history = [c for c in history if c.instance_id == instance_id]
        if change_type:
            history = [c for c in history if c.change_type == change_type]
        return history[-limit:]

    def generate_rollback_sql(self, change_id: str) -> Optional[str]:
        """Generate rollback SQL for a schema change."""
        for change in self._schema_history:
            if change.change_id == change_id:
                if not change.reversible:
                    return None
                if change.change_type == SchemaChangeType.CREATE_TABLE:
                    return f"DROP TABLE IF EXISTS {change.object_name};"
                elif change.change_type == SchemaChangeType.DROP_TABLE:
                    return change.metadata.get("original_ddl", "-- Original DDL not available")
                elif change.change_type == SchemaChangeType.ADD_COLUMN:
                    return f"ALTER TABLE {change.metadata.get('table_name', '')} DROP COLUMN IF EXISTS {change.object_name};"
                elif change.change_type == SchemaChangeType.DROP_INDEX:
                    return change.metadata.get("index_ddl", "-- Index DDL not available")
                return f"-- Rollback not available for {change.change_type.value}"
        return None

    # -----------------------------------------------------------------------
    # Monitoring & Alerts
    # -----------------------------------------------------------------------

    def check_alerts(self, instance_id: str) -> List[Alert]:
        """Check metrics against thresholds and generate alerts."""
        instance = self.get_instance(instance_id)
        metrics = self._performance_metrics.get(instance_id, [])
        alerts: List[Alert] = []
        now = datetime.now(timezone.utc)

        # Check recent metrics (last 5 minutes)
        recent = [m for m in metrics if (now - m.timestamp).total_seconds() < 300]
        by_type: Dict[str, List[float]] = defaultdict(list)
        for m in recent:
            by_type[m.metric_type.value].append(m.value)

        # Disk usage
        disk_vals = by_type.get(MetricType.DISK_USAGE.value, [])
        if disk_vals:
            max_disk = max(disk_vals)
            if max_disk > self._config.disk_critical_threshold * 100:
                alerts.append(Alert(
                    instance_id=instance_id, severity=AlertSeverity.CRITICAL,
                    metric="disk_usage", message=f"Disk usage critical: {max_disk:.1f}%",
                    current_value=max_disk, threshold=self._config.disk_critical_threshold * 100,
                ))
            elif max_disk > self._config.disk_warning_threshold * 100:
                alerts.append(Alert(
                    instance_id=instance_id, severity=AlertSeverity.WARNING,
                    metric="disk_usage", message=f"Disk usage high: {max_disk:.1f}%",
                    current_value=max_disk, threshold=self._config.disk_warning_threshold * 100,
                ))

        # CPU usage
        cpu_vals = by_type.get(MetricType.CPU_USAGE.value, [])
        if cpu_vals:
            max_cpu = max(cpu_vals)
            if max_cpu > self._config.cpu_critical_threshold * 100:
                alerts.append(Alert(
                    instance_id=instance_id, severity=AlertSeverity.CRITICAL,
                    metric="cpu_usage", message=f"CPU usage critical: {max_cpu:.1f}%",
                    current_value=max_cpu, threshold=self._config.cpu_critical_threshold * 100,
                ))
            elif max_cpu > self._config.cpu_warning_threshold * 100:
                alerts.append(Alert(
                    instance_id=instance_id, severity=AlertSeverity.WARNING,
                    metric="cpu_usage", message=f"CPU usage high: {max_cpu:.1f}%",
                    current_value=max_cpu, threshold=self._config.cpu_warning_threshold * 100,
                ))

        # Connections
        conn_vals = by_type.get(MetricType.CONNECTIONS.value, [])
        if conn_vals:
            max_conn = max(conn_vals)
            if max_conn > self._config.connection_critical_threshold * 100:
                alerts.append(Alert(
                    instance_id=instance_id, severity=AlertSeverity.CRITICAL,
                    metric="connections", message=f"Connection pool near capacity: {max_conn:.0f}",
                    current_value=max_conn, threshold=self._config.connection_critical_threshold * 100,
                ))

        self._alerts.extend(alerts)
        return alerts

    def get_active_alerts(self, instance_id: Optional[str] = None) -> List[Alert]:
        """Get all active (unresolved) alerts."""
        alerts = [a for a in self._alerts if a.resolved_at is None]
        if instance_id:
            alerts = [a for a in alerts if a.instance_id == instance_id]
        return alerts

    def resolve_alert(self, alert_id: str) -> Dict[str, Any]:
        """Mark an alert as resolved."""
        for alert in self._alerts:
            if alert.alert_id == alert_id:
                alert.resolved_at = datetime.now(timezone.utc)
                return alert.to_dict()
        raise KeyError(f"Alert '{alert_id}' not found")

    # -----------------------------------------------------------------------
    # Recovery Planning
    # -----------------------------------------------------------------------

    def create_recovery_plan(
        self,
        name: str,
        instance_ids: List[str],
        rto_minutes: int = 60,
        rpo_minutes: int = 15,
        steps: Optional[List[Dict[str, Any]]] = None,
    ) -> RecoveryPlan:
        """Create a disaster recovery plan."""
        plan = RecoveryPlan(
            name=name,
            instance_ids=instance_ids,
            rto_minutes=rto_minutes,
            rpo_minutes=rpo_minutes,
            steps=steps or [
                {"order": 1, "action": "assess", "description": "Assess the failure scope"},
                {"order": 2, "action": "notify", "description": "Notify the incident response team"},
                {"order": 3, "action": "failover", "description": "Execute failover to standby"},
                {"order": 4, "action": "verify", "description": "Verify data integrity"},
                {"order": 5, "action": "communicate", "description": "Communicate status to stakeholders"},
            ],
        )
        self._recovery_plans[plan.plan_id] = plan
        logger.info("Recovery plan '%s' created for %d instances", name, len(instance_ids))
        return plan

    def test_recovery_plan(self, plan_id: str) -> Dict[str, Any]:
        """Simulate testing a recovery plan."""
        if plan_id not in self._recovery_plans:
            raise KeyError(f"Recovery plan '{plan_id}' not found")
        plan = self._recovery_plans[plan_id]
        test_result = {
            "test_id": uuid.uuid4().hex[:8],
            "plan_id": plan_id,
            "tested_at": datetime.now(timezone.utc).isoformat(),
            "rto_achieved": random.uniform(plan.rto_minutes * 0.8, plan.rto_minutes * 1.2),
            "rpo_achieved": random.uniform(plan.rpo_minutes * 0.5, plan.rpo_minutes * 1.0),
            "steps_completed": len(plan.steps),
            "issues_found": random.randint(0, 2),
            "passed": True,
        }
        plan.last_tested = datetime.now(timezone.utc)
        plan.test_results.append(test_result)
        return test_result

    def get_recovery_plans(self) -> List[RecoveryPlan]:
        """List all recovery plans."""
        return list(self._recovery_plans.values())

    # -----------------------------------------------------------------------
    # Status & Reporting
    # -----------------------------------------------------------------------

    def get_status(self) -> Dict[str, Any]:
        """Get overall agent status."""
        return {
            "agent": "DatabaseAdminAgent",
            "instances": len(self._instances),
            "by_engine": dict(Counter(i.engine.value for i in self._instances.values())),
            "by_status": dict(Counter(i.status.value for i in self._instances.values())),
            "total_backups": sum(len(b) for b in self._backups.values()),
            "replication_links": len(self._replication_links),
            "security_findings": len(self._security_findings),
            "active_alerts": len(self.get_active_alerts()),
            "recovery_plans": len(self._recovery_plans),
            "schema_changes": len(self._schema_history),
        }

    def generate_dashboard(self) -> Dict[str, Any]:
        """Generate a comprehensive dashboard summary."""
        instances = list(self._instances.values())
        total_storage = sum(i.storage_gb for i in instances)
        used_storage = sum(i.storage_used_gb for i in instances)
        return {
            "instances": {
                "total": len(instances),
                "running": sum(1 for i in instances if i.status == InstanceStatus.RUNNING),
                "stopped": sum(1 for i in instances if i.status == InstanceStatus.STOPPED),
                "failed": sum(1 for i in instances if i.status == InstanceStatus.FAILED),
            },
            "storage": {
                "total_gb": round(total_storage, 2),
                "used_gb": round(used_storage, 2),
                "utilization_pct": round(used_storage / total_storage * 100, 1) if total_storage > 0 else 0,
            },
            "replication": self.get_replication_summary(),
            "security": self.get_security_summary(),
            "alerts": {
                "active": len(self.get_active_alerts()),
                "critical": sum(1 for a in self.get_active_alerts() if a.severity == AlertSeverity.CRITICAL),
                "warning": sum(1 for a in self.get_active_alerts() if a.severity == AlertSeverity.WARNING),
            },
            "backups": {
                "total": sum(len(b) for b in self._backups.values()),
                "recent": sum(
                    1 for backups in self._backups.values()
                    for b in backups
                    if b.completed_at and (datetime.now(timezone.utc) - b.completed_at).days <= 1
                ),
            },
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the Database Admin Agent capabilities."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    print("=" * 60)
    print("Database Administration Agent - Demo")
    print("=" * 60)

    agent = DatabaseAdminAgent()

    # Register instances
    primary = agent.register_instance(
        "prod-primary", DatabaseEngine.POSTGRESQL,
        host="db-primary.internal", port=5432, database="app_production",
        version="15.4", region="us-east-1", size="db.r5.xlarge",
        storage_gb=500, tags={"env": "production", "team": "platform"},
    )
    replica = agent.register_instance(
        "prod-replica", DatabaseEngine.POSTGRESQL,
        host="db-replica.internal", port=5432, database="app_production",
        version="15.4", region="us-east-1", size="db.r5.large",
        storage_gb=500, tags={"env": "production", "team": "platform"},
    )
    print(f"\nInstances: {primary.name} ({primary.instance_id}), {replica.name} ({replica.instance_id})")

    # Create backups
    backup = agent.create_backup(primary.instance_id, BackupType.FULL)
    print(f"\nBackup: {backup.backup_id} ({backup.status.value}, {backup.duration_seconds:.1f}s)")

    # Replication
    link = agent.add_replication_link(primary.instance_id, replica.instance_id, ReplicationRole.READ_REPLICA)
    print(f"\nReplication: {link.source_id} -> {link.target_id} ({link.status.value})")

    # Security audit
    findings = agent.run_security_audit(primary.instance_id)
    print(f"\nSecurity findings: {len(findings)}")
    for f in findings:
        print(f"  [{f.level.value.upper()}] {f.title}")

    # Performance metrics
    for _ in range(50):
        agent.record_metric(PerformanceMetric(
            metric_type=MetricType.QUERY_TIME, value=random.uniform(10, 500),
            instance_id=primary.instance_id,
        ))
        agent.record_metric(PerformanceMetric(
            metric_type=MetricType.DISK_USAGE, value=random.uniform(60, 85),
            instance_id=primary.instance_id,
        ))
    analysis = agent.analyze_performance(primary.instance_id)
    print(f"\nPerformance: score={analysis.score:.1f}, health={analysis.overall_health}")
    print(f"Bottlenecks: {analysis.bottlenecks}")

    # Capacity forecast
    forecast = agent.forecast_capacity(
        primary.instance_id, "storage_gb", 350,
        [300, 310, 315, 320, 325, 330, 340, 350],
    )
    print(f"\nCapacity: {forecast.current_value}GB -> {forecast.projected_value_90d:.0f}GB in 90d")
    print(f"Recommendation: {forecast.recommendation}")

    # Dashboard
    dashboard = agent.generate_dashboard()
    print(f"\nDashboard: {json.dumps(dashboard, indent=2)}")

    # Status
    print(f"\nAgent Status: {json.dumps(agent.get_status(), indent=2)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
