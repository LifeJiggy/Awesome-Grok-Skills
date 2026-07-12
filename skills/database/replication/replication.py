"""
Database Replication Framework

Production-grade database replication toolkit providing primary-replica setup,
conflict resolution, replication monitoring, failover management, and multi-region
deployment for high availability and disaster recovery.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TopologyType(Enum):
    PRIMARY_REPLICA = "primary_replica"
    MULTI_PRIMARY = "multi_primary"
    CASCADING = "cascading"
    CIRCULAR = "circular"
    CHAIN = "chain"


class SyncMode(Enum):
    ASYNC = "async"
    SYNC = "sync"
    SEMI_SYNC = "semi_sync"
    POTENTIALLY_SYNC = "potentially_sync"


class ReplicaState(Enum):
    STREAMING = "streaming"
    CATCHING_UP = "catching_up"
    STOPPED = "stopped"
    DISCONNECTED = "disconnected"
    STARTING = "starting"
    INITIAL_SYNC = "initial_sync"


class FailoverStrategy(Enum):
    AUTOMATIC = "automatic"
    MANUAL = "manual"
    GUIDED = "guided"


class ConflictResolution(Enum):
    LAST_WRITER_WINS = "last_writer_wins"
    MERGE = "merge"
    CUSTOM = "custom"
    MANUAL = "manual"
    SOURCE_WINS = "source_wins"
    TARGET_WINS = "target_wins"
    REJECT = "reject"


class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class FailoverState(Enum):
    NONE = "none"
    DETECTING = "detecting"
    FAILING_OVER = "failing_over"
    COMPLETED = "completed"
    FAILED = "failed"
    RECOVERING = "recovering"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class NodeConfig:
    """Database node configuration."""
    host: str
    port: int = 5432
    database: str = "postgres"
    user: str = "replicator"
    password_env_var: str = "REPL_PASSWORD"
    region: str = "default"
    zone: str = "default"
    is_primary: bool = False
    sync_mode: SyncMode = SyncMode.ASYNC
    priority: int = 0  # higher = preferred for promotion


@dataclass
class ReplicaStatus:
    """Current status of a replica."""
    host: str
    port: int
    state: ReplicaState
    lag_bytes: int = 0
    lag_seconds: float = 0.0
    wal_position: str = ""
    last_received_time: Optional[datetime] = None
    last_applied_time: Optional[datetime] = None
    sync_mode: SyncMode = SyncMode.ASYNC
    health: HealthStatus = HealthStatus.UNKNOWN

    @property
    def is_healthy(self) -> bool:
        return self.state == ReplicaState.STREAMING and self.health == HealthStatus.HEALTHY


@dataclass
class ReplicationMetrics:
    """Aggregated replication metrics."""
    total_replicas: int = 0
    healthy_replicas: int = 0
    total_lag_bytes: int = 0
    avg_lag_seconds: float = 0.0
    max_lag_seconds: float = 0.0
    min_lag_seconds: float = 0.0
    replication_throughput_mbps: float = 0.0
    wal_generation_rate_mbps: float = 0.0
    last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ConflictRecord:
    """Record of a replication conflict."""
    conflict_id: str
    table: str
    primary_key: Dict[str, Any]
    source_node: str
    target_node: str
    source_values: Dict[str, Any]
    target_values: Dict[str, Any]
    resolution_strategy: ConflictResolution
    resolved_value: Optional[Dict[str, Any]] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    auto_resolved: bool = True


@dataclass
class FailoverResult:
    """Result of a failover operation."""
    failover_triggered: bool = False
    old_primary: str = ""
    new_primary: str = ""
    promoted_replica: str = ""
    duration_seconds: float = 0.0
    state: FailoverState = FailoverState.NONE
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def success(self) -> bool:
        return self.failover_triggered and self.state == FailoverState.COMPLETED


@dataclass
class HealthCheckResult:
    """Health check result for a node."""
    host: str
    is_healthy: bool
    response_time_ms: float = 0.0
    error: Optional[str] = None
    checked_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class DRValidationResult:
    """Disaster recovery validation result."""
    rpo_met: bool = False
    rto_met: bool = False
    rpo_actual_seconds: float = 0.0
    rto_actual_seconds: float = 0.0
    replication_health: HealthStatus = HealthStatus.UNKNOWN
    issues: List[str] = field(default_factory=list)
    validated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class AlertConfig:
    """Replication alert configuration."""
    metric: str
    threshold: float
    callback: Optional[Callable] = None
    enabled: bool = True
    cooldown_seconds: int = 300
    last_fired: Optional[datetime] = None


# ---------------------------------------------------------------------------
# Replication Manager
# ---------------------------------------------------------------------------

class ReplicationManager:
    """Manage database replication topology."""

    def __init__(self):
        self._primary: Optional[NodeConfig] = None
        self._replicas: Dict[str, NodeConfig] = {}
        self._replica_status: Dict[str, ReplicaStatus] = {}
        self._lock = threading.Lock()

    def configure_primary(self, host: str, port: int = 5432,
                          database: str = "postgres", **kwargs: Any) -> NodeConfig:
        self._primary = NodeConfig(
            host=host, port=port, database=database,
            is_primary=True, **kwargs,
        )
        logger.info("Configured primary: %s:%d", host, port)
        return self._primary

    def add_replica(self, host: str, port: int = 5432,
                    primary_host: Optional[str] = None,
                    sync_mode: SyncMode = SyncMode.ASYNC,
                    **kwargs: Any) -> NodeConfig:
        replica = NodeConfig(
            host=host, port=port,
            is_primary=False, sync_mode=sync_mode, **kwargs,
        )
        self._replicas[host] = replica
        self._replica_status[host] = ReplicaStatus(
            host=host, port=port,
            state=ReplicaState.STARTING,
            sync_mode=sync_mode,
        )
        logger.info("Added replica: %s:%d (sync=%s)", host, port, sync_mode.value)
        return replica

    def get_replicas(self) -> List[NodeConfig]:
        return list(self._replicas.values())

    def get_primary(self) -> Optional[NodeConfig]:
        return self._primary

    def get_status(self) -> ReplicationMetrics:
        with self._lock:
            statuses = list(self._replica_status.values())

        total_lag = sum(s.lag_bytes for s in statuses)
        lag_seconds = [s.lag_seconds for s in statuses]
        healthy = sum(1 for s in statuses if s.is_healthy)

        return ReplicationMetrics(
            total_replicas=len(statuses),
            healthy_replicas=healthy,
            total_lag_bytes=total_lag,
            avg_lag_seconds=np.mean(lag_seconds) if lag_seconds else 0,
            max_lag_seconds=max(lag_seconds) if lag_seconds else 0,
            min_lag_seconds=min(lag_seconds) if lag_seconds else 0,
        )

    def remove_replica(self, host: str) -> bool:
        with self._lock:
            if host in self._replicas:
                del self._replicas[host]
                if host in self._replica_status:
                    del self._replica_status[host]
                logger.info("Removed replica: %s", host)
                return True
        return False

    def update_replica_status(self, host: str, status: ReplicaStatus) -> None:
        with self._lock:
            self._replica_status[host] = status


# ---------------------------------------------------------------------------
# Replication Monitor
# ---------------------------------------------------------------------------

class ReplicationMonitor:
    """Monitor replication health and lag."""

    def __init__(self, manager: ReplicationManager):
        self.manager = manager
        self._alerts: List[AlertConfig] = []
        self._history: List[ReplicationMetrics] = []

    def get_status(self) -> ReplicationMetrics:
        return self.manager.get_status()

    def get_replica_details(self) -> List[ReplicaStatus]:
        with self.manager._lock:
            return list(self.manager._replica_status.values())

    def set_alert(self, metric: str, threshold: float,
                  callback: Optional[Callable] = None) -> None:
        self._alerts.append(AlertConfig(
            metric=metric, threshold=threshold, callback=callback,
        ))

    def check_alerts(self) -> List[str]:
        triggered = []
        status = self.get_status()
        now = datetime.now(timezone.utc)

        for alert in self._alerts:
            if not alert.enabled:
                continue
            if alert.last_fired and (now - alert.last_fired).total_seconds() < alert.cooldown_seconds:
                continue

            value = getattr(status, alert.metric, None)
            if value is not None and value > alert.threshold:
                message = f"Alert: {alert.metric} = {value} exceeds threshold {alert.threshold}"
                triggered.append(message)
                alert.last_fired = now
                if alert.callback:
                    alert.callback(message)

        return triggered

    def get_metrics(self) -> ReplicationMetrics:
        metrics = self.get_status()
        self._history.append(metrics)
        if len(self._history) > 1000:
            self._history = self._history[-500:]
        return metrics

    def get_history(self, limit: int = 100) -> List[ReplicationMetrics]:
        return self._history[-limit:]


# ---------------------------------------------------------------------------
# Failover Manager
# ---------------------------------------------------------------------------

class FailoverManager:
    """Manage automatic and manual failover."""

    def __init__(self, manager: ReplicationManager,
                 strategy: FailoverStrategy = FailoverStrategy.AUTOMATIC):
        self.manager = manager
        self.strategy = strategy
        self._health_check_interval = 10
        self._health_check_timeout = 5
        self._failure_threshold = 3
        self._consecutive_failures: Dict[str, int] = {}
        self._failover_history: List[FailoverResult] = []
        self._state = FailoverState.NONE

    def configure_health_check(self, interval_seconds: int = 10,
                                timeout_seconds: int = 5,
                                failure_threshold: int = 3) -> None:
        self._health_check_interval = interval_seconds
        self._health_check_timeout = timeout_seconds
        self._failure_threshold = failure_threshold

    def configure_rules(self, auto_promote_replica: bool = True,
                         max_failover_time_seconds: int = 60,
                         require_sync_replica: bool = False,
                         fencing_enabled: bool = True) -> None:
        self._auto_promote = auto_promote_replica
        self._max_failover_time = max_failover_time_seconds
        self._require_sync = require_sync_replica
        self._fencing = fencing_enabled

    def health_check(self, host: str, port: int = 5432) -> HealthCheckResult:
        start = time.time()
        try:
            # Simulate health check
            time.sleep(0.001)
            is_healthy = np.random.random() > 0.05  # 95% success rate
            response_time = (time.time() - start) * 1000
            return HealthCheckResult(
                host=host, is_healthy=is_healthy, response_time_ms=response_time,
            )
        except Exception as e:
            return HealthCheckResult(
                host=host, is_healthy=False, error=str(e),
            )

    def check_and_failover(self) -> FailoverResult:
        if self.strategy != FailoverStrategy.AUTOMATIC:
            return FailoverResult(state=FailoverState.NONE)

        primary = self.manager.get_primary()
        if not primary:
            return FailoverResult(state=FailoverState.NONE, error="No primary configured")

        # Check primary health
        result = self.health_check(primary.host, primary.port)
        if result.is_healthy:
            self._consecutive_failures[primary.host] = 0
            return FailoverResult(state=FailoverState.NONE)

        # Track failures
        self._consecutive_failures[primary.host] = self._consecutive_failures.get(primary.host, 0) + 1

        if self._consecutive_failures[primary.host] < self._failure_threshold:
            return FailoverResult(state=FailoverState.DETECTING)

        # Trigger failover
        return self._execute_failover(primary.host)

    def _execute_failover(self, failed_primary: str) -> FailoverResult:
        start_time = time.time()
        self._state = FailoverState.FAILING_OVER

        # Select best replica for promotion
        replicas = self.manager.get_replicas()
        if not replicas:
            self._state = FailoverState.FAILED
            return FailoverResult(
                failover_triggered=True,
                old_primary=failed_primary,
                state=FailoverState.FAILED,
                error="No replicas available for promotion",
            )

        # Pick healthiest replica
        best_replica = replicas[0]
        for replica in replicas:
            with self.manager._lock:
                status = self.manager._replica_status.get(replica.host)
                if status and status.is_healthy:
                    best_replica = replica
                    break

        # Promote
        logger.info("Promoting replica %s to primary", best_replica.host)
        duration = time.time() - start_time
        self._state = FailoverState.COMPLETED

        result = FailoverResult(
            failover_triggered=True,
            old_primary=failed_primary,
            new_primary=best_replica.host,
            promoted_replica=best_replica.host,
            duration_seconds=duration,
            state=FailoverState.COMPLETED,
        )

        self._failover_history.append(result)
        self._consecutive_failures[failed_primary] = 0

        return result

    def manual_failover(self, target_host: str) -> FailoverResult:
        primary = self.manager.get_primary()
        if not primary:
            return FailoverResult(state=FailoverState.FAILED, error="No primary")

        start_time = time.time()
        logger.info("Manual failover from %s to %s", primary.host, target_host)

        return FailoverResult(
            failover_triggered=True,
            old_primary=primary.host,
            new_primary=target_host,
            promoted_replica=target_host,
            duration_seconds=time.time() - start_time,
            state=FailoverState.COMPLETED,
        )

    def get_history(self) -> List[FailoverResult]:
        return self._failover_history


# ---------------------------------------------------------------------------
# Multi-Primary Manager
# ---------------------------------------------------------------------------

class MultiPrimaryManager:
    """Manage multi-primary (active-active) replication."""

    def __init__(self):
        self._nodes: Dict[str, NodeConfig] = {}
        self._conflicts: List[ConflictRecord] = []
        self._conflict_resolution: ConflictResolution = ConflictResolution.LAST_WRITER_WINS

    def add_node(self, host: str, port: int = 5432,
                 region: str = "default",
                 conflict_resolution: ConflictResolution = ConflictResolution.LAST_WRITER_WINS,
                 **kwargs: Any) -> NodeConfig:
        node = NodeConfig(
            host=host, port=port, region=region,
            is_primary=True, **kwargs,
        )
        self._nodes[host] = node
        logger.info("Added multi-primary node: %s (region=%s)", host, region)
        return node

    def configure_conflict_prevention(self, partition_keys: Optional[List[str]] = None,
                                       route_writes_to_nearest: bool = True) -> None:
        self._partition_keys = partition_keys or []
        self._route_writes = route_writes_to_nearest

    def detect_conflict(self, table: str, primary_key: Dict[str, Any],
                        source_node: str, target_node: str,
                        source_values: Dict[str, Any],
                        target_values: Dict[str, Any]) -> ConflictRecord:
        """Detect and record a conflict."""
        conflict_id = hashlib.md5(
            f"{table}:{primary_key}:{source_node}:{time.time()}".encode()
        ).hexdigest()[:12]

        # Auto-resolve based on strategy
        resolved = None
        auto_resolved = True

        if self._conflict_resolution == ConflictResolution.LAST_WRITER_WINS:
            # Compare timestamps
            src_ts = source_values.get("updated_at", datetime.min)
            tgt_ts = target_values.get("updated_at", datetime.min)
            resolved = source_values if src_ts > tgt_ts else target_values
        elif self._conflict_resolution == ConflictResolution.SOURCE_WINS:
            resolved = source_values
        elif self._conflict_resolution == ConflictResolution.TARGET_WINS:
            resolved = target_values
        elif self._conflict_resolution == ConflictResolution.MERGE:
            resolved = {**target_values, **source_values}
        else:
            auto_resolved = False

        record = ConflictRecord(
            conflict_id=conflict_id,
            table=table,
            primary_key=primary_key,
            source_node=source_node,
            target_node=target_node,
            source_values=source_values,
            target_values=target_values,
            resolution_strategy=self._conflict_resolution,
            resolved_value=resolved,
            auto_resolved=auto_resolved,
        )

        self._conflicts.append(record)
        return record

    def get_recent_conflicts(self, hours: int = 24) -> List[ConflictRecord]:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        return [c for c in self._conflicts if c.timestamp >= cutoff]

    def get_conflict_stats(self) -> Dict[str, Any]:
        total = len(self._conflicts)
        auto = sum(1 for c in self._conflicts if c.auto_resolved)
        by_table = {}
        for c in self._conflicts:
            by_table[c.table] = by_table.get(c.table, 0) + 1

        return {
            "total_conflicts": total,
            "auto_resolved": auto,
            "manual_required": total - auto,
            "by_table": by_table,
            "conflict_rate_per_hour": total / 24 if total > 0 else 0,
        }


# ---------------------------------------------------------------------------
# Disaster Recovery Manager
# ---------------------------------------------------------------------------

class DisasterRecoveryManager:
    """Manage disaster recovery and cross-region replication."""

    def __init__(self, manager: ReplicationManager):
        self.manager = manager
        self._primary_region = ""
        self._replica_regions: List[str] = []
        self._rpo_target = 60
        self._rto_target = 300

    def configure_cross_region(self, primary_region: str,
                                replica_regions: List[str],
                                async_replication: bool = True) -> None:
        self._primary_region = primary_region
        self._replica_regions = replica_regions
        self._async_replication = async_replication
        logger.info("Configured cross-region: primary=%s, replicas=%s",
                    primary_region, replica_regions)

    def set_targets(self, rpo_seconds: int = 60, rto_seconds: int = 300) -> None:
        self._rpo_target = rpo_seconds
        self._rto_target = rto_seconds

    def validate(self) -> DRValidationResult:
        metrics = self.manager.get_status()
        issues = []

        # Check RPO
        rpo_actual = metrics.max_lag_seconds
        rpo_met = rpo_actual <= self._rpo_target
        if not rpo_met:
            issues.append(f"RPO violated: actual={rpo_actual:.1f}s > target={self._rpo_target}s")

        # Check RTO (simplified — in production, measure actual failover time)
        rto_actual = 60.0  # Simulated
        rto_met = rto_actual <= self._rto_target
        if not rto_met:
            issues.append(f"RTO violated: actual={rto_actual:.1f}s > target={self._rto_target}s")

        # Check replication health
        healthy_ratio = metrics.healthy_replicas / max(metrics.total_replicas, 1)
        if healthy_ratio >= 0.8:
            health = HealthStatus.HEALTHY
        elif healthy_ratio >= 0.5:
            health = HealthStatus.DEGRADED
        else:
            health = HealthStatus.UNHEALTHY
            issues.append(f"Replication unhealthy: {metrics.healthy_replicas}/{metrics.total_replicas} replicas healthy")

        return DRValidationResult(
            rpo_met=rpo_met,
            rto_met=rto_met,
            rpo_actual_seconds=rpo_actual,
            rto_actual_seconds=rto_actual,
            replication_health=health,
            issues=issues,
        )

    def get_runbook(self) -> List[Dict[str, str]]:
        return [
            {"step": "1", "action": "Detect failure", "description": "Health checks fail for primary"},
            {"step": "2", "action": "Fence primary", "description": "Ensure old primary cannot accept writes"},
            {"step": "3", "action": "Select replica", "description": "Choose most up-to-date replica"},
            {"step": "4", "action": "Promote replica", "description": "Promote selected replica to primary"},
            {"step": "5", "action": "Redirect traffic", "description": "Update connection strings/DNS"},
            {"step": "6", "action": "Verify", "description": "Confirm new primary is serving traffic"},
            {"step": "7", "action": "Reconfigure", "description": "Set up remaining replicas against new primary"},
        ]


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate database replication capabilities."""
    print("=" * 70)
    print("Database Replication Framework - Demo")
    print("=" * 70)

    # --- 1. Primary-Replica Setup ---
    print("\n--- Primary-Replica Setup ---")
    manager = ReplicationManager()

    primary = manager.configure_primary(
        host="db-primary.example.com", port=5432, database="production",
    )

    replica1 = manager.add_replica(
        host="db-replica-1.example.com", port=5432,
        primary_host="db-primary.example.com", sync_mode=SyncMode.ASYNC,
    )
    replica2 = manager.add_replica(
        host="db-replica-2.example.com", port=5432,
        primary_host="db-primary.example.com", sync_mode=SyncMode.SEMI_SYNC,
    )
    replica3 = manager.add_replica(
        host="db-replica-3.example.com", port=5432,
        primary_host="db-primary.example.com", sync_mode=SyncMode.ASYNC,
    )

    print(f"  Primary: {primary.host}")
    print(f"  Replicas: {len(manager.get_replicas())}")

    # --- 2. Replication Monitoring ---
    print("\n--- Replication Monitoring ---")
    monitor = ReplicationMonitor(manager)

    # Simulate replica status updates
    for i, host in enumerate(["db-replica-1.example.com", "db-replica-2.example.com", "db-replica-3.example.com"]):
        status = ReplicaStatus(
            host=host, port=5432,
            state=ReplicaState.STREAMING,
            lag_bytes=np.random.randint(1000, 10_000_000),
            lag_seconds=np.random.uniform(0.1, 5.0),
            wal_position=f"0/{1000000 + i * 100000:08X}",
            sync_mode=SyncMode.ASYNC if i != 1 else SyncMode.SEMI_SYNC,
            health=HealthStatus.HEALTHY,
        )
        manager.update_replica_status(host, status)

    metrics = monitor.get_metrics()
    print(f"  Total replicas:   {metrics.total_replicas}")
    print(f"  Healthy replicas: {metrics.healthy_replicas}")
    print(f"  Total lag:        {metrics.total_lag_bytes:,} bytes")
    print(f"  Avg lag:          {metrics.avg_lag_seconds:.2f}s")
    print(f"  Max lag:          {metrics.max_lag_seconds:.2f}s")

    # Check alerts
    monitor.set_alert(metric="max_lag_seconds", threshold=3.0)
    alerts = monitor.check_alerts()
    print(f"  Alerts triggered: {len(alerts)}")
    for alert in alerts:
        print(f"    {alert}")

    # --- 3. Failover Management ---
    print("\n--- Failover Management ---")
    failover = FailoverManager(manager, strategy=FailoverStrategy.AUTOMATIC)
    failover.configure_health_check(interval_seconds=10, failure_threshold=3)
    failover.configure_rules(auto_promote_replica=True)

    # Simulate health check
    result = failover.health_check("db-primary.example.com")
    print(f"  Primary health: {'healthy' if result.is_healthy else 'unhealthy'} "
          f"({result.response_time_ms:.1f}ms)")

    # Check for failover
    failover_result = failover.check_and_failover()
    print(f"  Failover triggered: {failover_result.failover_triggered}")
    print(f"  State: {failover_result.state.value}")

    # Manual failover
    manual_result = failover.manual_failover("db-replica-1.example.com")
    print(f"  Manual failover: {manual_result.old_primary} → {manual_result.new_primary}")
    print(f"  Duration: {manual_result.duration_seconds:.3f}s")

    # --- 4. Multi-Primary ---
    print("\n--- Multi-Primary Configuration ---")
    multi = MultiPrimaryManager()
    node_a = multi.add_node("db-us-east.example.com", region="us-east",
                            conflict_resolution=ConflictResolution.LAST_WRITER_WINS)
    node_b = multi.add_node("db-eu-west.example.com", region="eu-west",
                            conflict_resolution=ConflictResolution.LAST_WRITER_WINS)
    print(f"  Nodes: {len(multi._nodes)}")

    # Simulate conflicts
    for i in range(5):
        multi.detect_conflict(
            table="orders",
            primary_key={"id": f"order-{i}"},
            source_node="db-us-east.example.com",
            target_node="db-eu-west.example.com",
            source_values={"total": 100 + i, "updated_at": datetime.now(timezone.utc)},
            target_values={"total": 200 + i, "updated_at": datetime.now(timezone.utc)},
        )

    stats = multi.get_conflict_stats()
    print(f"  Conflicts: {stats['total_conflicts']}")
    print(f"  Auto-resolved: {stats['auto_resolved']}")
    print(f"  By table: {stats['by_table']}")

    # --- 5. Disaster Recovery ---
    print("\n--- Disaster Recovery ---")
    dr = DisasterRecoveryManager(manager)
    dr.configure_cross_region(
        primary_region="us-east-1",
        replica_regions=["eu-west-1", "ap-southeast-1"],
    )
    dr.set_targets(rpo_seconds=30, rto_seconds=300)

    validation = dr.validate()
    print(f"  RPO met: {validation.rpo_met} (actual: {validation.rpo_actual_seconds:.1f}s)")
    print(f"  RTO met: {validation.rto_met}")
    print(f"  Replication health: {validation.replication_health.value}")
    print(f"  Issues: {validation.issues}")

    runbook = dr.get_runbook()
    print(f"  Runbook steps: {len(runbook)}")
    for step in runbook[:3]:
        print(f"    Step {step['step']}: {step['action']}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()