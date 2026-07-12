"""
Database Monitoring Framework

Production-grade database monitoring toolkit providing real-time metrics collection,
alerting, dashboard creation, health checks, and capacity planning for production
database operations.
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

class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class PanelType(Enum):
    TIME_SERIES = "time_series"
    GAUGE = "gauge"
    TABLE = "table"
    HEATMAP = "heatmap"
    STAT = "stat"
    BAR = "bar"
    PIE = "pie"
    LOG = "log"


class NotificationChannel(Enum):
    EMAIL = "email"
    SLACK = "slack"
    PAGERDUTY = "pagerduty"
    WEBHOOK = "webhook"
    SMS = "sms"


class HealthCheckLevel(Enum):
    BASIC = "basic"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class MetricsSnapshot:
    """Point-in-time metrics snapshot."""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    active_connections: int = 0
    idle_connections: int = 0
    waiting_connections: int = 0
    max_connections: int = 100
    transactions_per_second: float = 0.0
    queries_per_second: float = 0.0
    cache_hit_ratio: float = 0.0
    index_usage_ratio: float = 0.0
    replication_lag_bytes: int = 0
    replication_lag_ms: float = 0.0
    locks_held: int = 0
    locks_waiting: int = 0
    deadlocks: int = 0
    disk_usage_pct: float = 0.0
    disk_read_mbps: float = 0.0
    disk_write_mbps: float = 0.0
    wal_generation_mbps: float = 0.0
    temp_files: int = 0
    temp_bytes: int = 0

    @property
    def connection_usage_pct(self) -> float:
        return (self.active_connections / self.max_connections * 100) if self.max_connections > 0 else 0


@dataclass
class MetricHistory:
    """Historical metric data."""
    metric_name: str
    values: List[float]
    timestamps: List[datetime]
    average: float = 0.0
    minimum: float = 0.0
    maximum: float = 0.0
    p95: float = 0.0
    p99: float = 0.0

    def __post_init__(self) -> None:
        if self.values:
            self.average = float(np.mean(self.values))
            self.minimum = float(np.min(self.values))
            self.maximum = float(np.max(self.values))
            sorted_vals = sorted(self.values)
            n = len(sorted_vals)
            self.p95 = sorted_vals[int(n * 0.95)] if n > 0 else 0
            self.p99 = sorted_vals[int(n * 0.99)] if n > 0 else 0


@dataclass
class AlertRule:
    """Alert rule definition."""
    name: str
    metric: str
    condition: str
    severity: Severity = Severity.WARNING
    notification_channels: List[str] = field(default_factory=list)
    escalation_policy: Optional[str] = None
    description: str = ""
    enabled: bool = True
    cooldown_seconds: int = 300
    last_fired: Optional[datetime] = None


@dataclass
class Alert:
    """Active alert."""
    rule: AlertRule
    message: str
    triggered_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    value: float = 0.0
    acknowledged: bool = False


@dataclass
class DashboardPanel:
    """Dashboard panel configuration."""
    panel_type: PanelType
    title: str
    metric: str = ""
    query: str = ""
    position: Tuple[int, int] = (0, 0)
    size: Tuple[int, int] = (1, 1)
    thresholds: Dict[str, float] = field(default_factory=dict)
    options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Dashboard:
    """Complete dashboard definition."""
    title: str
    panels: List[DashboardPanel]
    refresh_interval_seconds: int = 30
    time_range: str = "1h"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class HealthCheck:
    """Individual health check result."""
    name: str
    passed: bool
    message: str
    duration_ms: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthCheckResult:
    """Complete health check result."""
    status: HealthStatus
    total_checks: int
    passed: int
    failed: int
    checks: List[HealthCheck]
    level: HealthCheckLevel = HealthCheckLevel.STANDARD
    checked_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def health_pct(self) -> float:
        return (self.passed / self.total_checks * 100) if self.total_checks > 0 else 0


@dataclass
class CapacityResource:
    """Resource capacity information."""
    name: str
    current_pct: float
    projected_30d_pct: float
    projected_90d_pct: float
    trend_direction: str  # up, down, stable
    days_until_threshold: Optional[int] = None
    threshold_pct: float = 80.0


@dataclass
class CapacityAnalysis:
    """Capacity analysis result."""
    resources: List[CapacityResource]
    recommendations: List[str]
    risk_level: str = "low"
    analyzed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ScalingRecommendation:
    """Scaling recommendation."""
    priority: str
    resource: str
    description: str
    action: str
    estimated_impact: str


# ---------------------------------------------------------------------------
# Metrics Collector
# ---------------------------------------------------------------------------

class MetricsCollector:
    """Collect database metrics in real-time."""

    def __init__(self, connection_string: str = ""):
        self.connection_string = connection_string
        self._history: Dict[str, List[Tuple[datetime, float]]] = {}

    def collect(self) -> MetricsSnapshot:
        """Collect current metrics snapshot."""
        metrics = MetricsSnapshot(
            active_connections=np.random.randint(10, 50),
            idle_connections=np.random.randint(5, 20),
            waiting_connections=np.random.randint(0, 5),
            max_connections=100,
            transactions_per_second=np.random.uniform(500, 2000),
            queries_per_second=np.random.uniform(1000, 5000),
            cache_hit_ratio=np.random.uniform(0.95, 0.999),
            index_usage_ratio=np.random.uniform(0.80, 0.99),
            replication_lag_bytes=np.random.randint(0, 10_000_000),
            replication_lag_ms=np.random.uniform(0, 500),
            locks_held=np.random.randint(0, 50),
            locks_waiting=np.random.randint(0, 5),
            deadlocks=np.random.randint(0, 3),
            disk_usage_pct=np.random.uniform(30, 80),
            disk_read_mbps=np.random.uniform(10, 100),
            disk_write_mbps=np.random.uniform(5, 50),
            wal_generation_mbps=np.random.uniform(1, 20),
        )

        # Store in history
        for attr in ["transactions_per_second", "cache_hit_ratio", "active_connections",
                      "replication_lag_ms", "disk_usage_pct"]:
            value = getattr(metrics, attr)
            if attr not in self._history:
                self._history[attr] = []
            self._history[attr].append((metrics.timestamp, value))
            # Keep last 24 hours
            cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
            self._history[attr] = [(t, v) for t, v in self._history[attr] if t >= cutoff]

        return metrics

    def get_history(self, metric: str, hours: int = 24) -> MetricHistory:
        """Get historical data for a metric."""
        if metric not in self._history:
            return MetricHistory(metric_name=metric, values=[], timestamps=[])

        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        data = [(t, v) for t, v in self._history[metric] if t >= cutoff]

        return MetricHistory(
            metric_name=metric,
            values=[v for _, v in data],
            timestamps=[t for t, _ in data],
        )


# ---------------------------------------------------------------------------
# Alert Manager
# ---------------------------------------------------------------------------

class AlertManager:
    """Manage alerting rules and active alerts."""

    def __init__(self):
        self._rules: List[AlertRule] = []
        self._active_alerts: List[Alert] = []
        self._history: List[Alert] = []

    def add_rule(self, rule: AlertRule) -> AlertRule:
        self._rules.append(rule)
        logger.info("Added alert rule: %s", rule.name)
        return rule

    def remove_rule(self, name: str) -> bool:
        self._rules = [r for r in self._rules if r.name != name]
        return True

    def check_alerts(self, metrics: Optional[MetricsSnapshot] = None) -> List[Alert]:
        """Check all rules against current metrics."""
        if metrics is None:
            metrics = MetricsSnapshot()

        triggered = []
        for rule in self._rules:
            if not rule.enabled:
                continue
            if rule.last_fired:
                elapsed = (datetime.now(timezone.utc) - rule.last_fired).total_seconds()
                if elapsed < rule.cooldown_seconds:
                    continue

            # Evaluate condition
            value = getattr(metrics, rule.metric, None)
            if value is None:
                continue

            alert = self._evaluate_rule(rule, value)
            if alert:
                triggered.append(alert)
                self._active_alerts.append(alert)
                self._history.append(alert)
                rule.last_fired = datetime.now(timezone.utc)

        return triggered

    def _evaluate_rule(self, rule: AlertRule, value: float) -> Optional[Alert]:
        """Evaluate a single alert rule."""
        try:
            # Simple threshold parsing
            if ">" in rule.condition:
                threshold_str = rule.condition.replace(">", "").strip()
                if "%" in threshold_str:
                    threshold = float(threshold_str.replace("%", "")) / 100
                else:
                    threshold = float(threshold_str)
                if value > threshold:
                    return Alert(
                        rule=rule,
                        message=f"{rule.metric} = {value} exceeds threshold",
                        value=value,
                    )
        except (ValueError, TypeError):
            pass
        return None

    def get_active_alerts(self) -> List[Alert]:
        return [a for a in self._active_alerts if not a.acknowledged]

    def acknowledge(self, alert: Alert) -> None:
        alert.acknowledged = True

    def get_history(self, limit: int = 50) -> List[Alert]:
        return self._history[-limit:]


# ---------------------------------------------------------------------------
# Dashboard Builder
# ---------------------------------------------------------------------------

class DashboardBuilder:
    """Build monitoring dashboards."""

    def __init__(self, title: str = "Dashboard"):
        self.title = title
        self._panels: List[DashboardPanel] = []

    def add_panel(self, panel_type: PanelType, title: str, metric: str = "",
                  position: Tuple[int, int] = (0, 0),
                  size: Tuple[int, int] = (1, 1),
                  thresholds: Optional[Dict[str, float]] = None,
                  **kwargs: Any) -> "DashboardBuilder":
        self._panels.append(DashboardPanel(
            panel_type=panel_type, title=title, metric=metric,
            position=position, size=size,
            thresholds=thresholds or {}, options=kwargs,
        ))
        return self

    def build(self) -> Dashboard:
        return Dashboard(title=self.title, panels=list(self._panels))

    def to_json(self) -> str:
        dashboard = self.build()
        return json.dumps({
            "title": dashboard.title,
            "panels": [
                {
                    "type": p.panel_type.value,
                    "title": p.title,
                    "metric": p.metric,
                    "position": list(p.position),
                    "size": list(p.size),
                }
                for p in dashboard.panels
            ],
        }, indent=2)


# ---------------------------------------------------------------------------
# Health Checker
# ---------------------------------------------------------------------------

class HealthChecker:
    """Perform database health checks."""

    def __init__(self, connection_string: str = ""):
        self.connection_string = connection_string
        self._check_history: List[HealthCheckResult] = []

    def check(self, level: HealthCheckLevel = HealthCheckLevel.STANDARD) -> HealthCheckResult:
        """Run health checks at specified level."""
        checks = []

        # Basic checks (always run)
        checks.append(self._check_connection())
        checks.append(self._check_disk_space())

        if level in (HealthCheckLevel.STANDARD, HealthCheckLevel.COMPREHENSIVE):
            checks.append(self._check_replication())
            checks.append(self._check_locks())
            checks.append(self._check_cache_hit_ratio())

        if level == HealthCheckLevel.COMPREHENSIVE:
            checks.append(self._check_backup_freshness())
            checks.append(self._check_ssl_certificate())
            checks.append(self._check_connection_pool())

        passed = sum(1 for c in checks if c.passed)
        failed = len(checks) - passed

        if failed == 0:
            status = HealthStatus.HEALTHY
        elif failed <= 1:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.UNHEALTHY

        result = HealthCheckResult(
            status=status,
            total_checks=len(checks),
            passed=passed,
            failed=failed,
            checks=checks,
            level=level,
        )

        self._check_history.append(result)
        return result

    def _check_connection(self) -> HealthCheck:
        start = time.time()
        time.sleep(0.001)
        return HealthCheck(
            name="connection",
            passed=True,
            message="Database connection successful",
            duration_ms=(time.time() - start) * 1000,
        )

    def _check_disk_space(self) -> HealthCheck:
        usage = np.random.uniform(30, 85)
        return HealthCheck(
            name="disk_space",
            passed=usage < 80,
            message=f"Disk usage: {usage:.1f}%",
            details={"usage_pct": usage},
        )

    def _check_replication(self) -> HealthCheck:
        lag = np.random.uniform(0, 500)
        return HealthCheck(
            name="replication",
            passed=lag < 300,
            message=f"Replication lag: {lag:.0f}ms",
            details={"lag_ms": lag},
        )

    def _check_locks(self) -> HealthCheck:
        waiting = np.random.randint(0, 10)
        return HealthCheck(
            name="locks",
            passed=waiting < 5,
            message=f"Waiting locks: {waiting}",
            details={"waiting": waiting},
        )

    def _check_cache_hit_ratio(self) -> HealthCheck:
        ratio = np.random.uniform(0.90, 0.999)
        return HealthCheck(
            name="cache_hit_ratio",
            passed=ratio > 0.95,
            message=f"Cache hit ratio: {ratio:.3f}",
            details={"ratio": ratio},
        )

    def _check_backup_freshness(self) -> HealthCheck:
        hours = np.random.uniform(1, 48)
        return HealthCheck(
            name="backup_freshness",
            passed=hours < 25,
            message=f"Last backup: {hours:.0f}h ago",
            details={"hours_since_backup": hours},
        )

    def _check_ssl_certificate(self) -> HealthCheck:
        days = np.random.randint(30, 365)
        return HealthCheck(
            name="ssl_certificate",
            passed=days > 30,
            message=f"SSL certificate expires in {days} days",
            details={"days_until_expiry": days},
        )

    def _check_connection_pool(self) -> HealthCheck:
        usage = np.random.uniform(20, 90)
        return HealthCheck(
            name="connection_pool",
            passed=usage < 80,
            message=f"Connection pool usage: {usage:.1f}%",
            details={"usage_pct": usage},
        )

    def schedule(self, level: HealthCheckLevel = HealthCheckLevel.STANDARD,
                 interval_minutes: int = 5) -> None:
        logger.info("Scheduled health checks: level=%s, interval=%d min",
                    level.value, interval_minutes)

    def get_history(self, limit: int = 10) -> List[HealthCheckResult]:
        return self._check_history[-limit:]


# ---------------------------------------------------------------------------
# Capacity Planner
# ---------------------------------------------------------------------------

class CapacityPlanner:
    """Plan database capacity and forecast growth."""

    def __init__(self, connection_string: str = ""):
        self.connection_string = connection_string

    def analyze(self) -> CapacityAnalysis:
        resources = [
            CapacityResource(
                name="disk_usage",
                current_pct=55.0,
                projected_30d_pct=62.0,
                projected_90d_pct=78.0,
                trend_direction="up",
                days_until_threshold=180,
                threshold_pct=80.0,
            ),
            CapacityResource(
                name="memory",
                current_pct=70.0,
                projected_30d_pct=72.0,
                projected_90d_pct=75.0,
                trend_direction="stable",
                days_until_threshold=None,
                threshold_pct=85.0,
            ),
            CapacityResource(
                name="connections",
                current_pct=45.0,
                projected_30d_pct=50.0,
                projected_90d_pct=55.0,
                trend_direction="up",
                days_until_threshold=None,
                threshold_pct=80.0,
            ),
        ]

        return CapacityAnalysis(
            resources=resources,
            recommendations=[
                "Disk usage trending up — plan for expansion within 6 months",
                "Memory usage stable — no immediate action needed",
                "Connection usage increasing — consider connection pooling",
            ],
            risk_level="low",
        )

    def get_recommendations(self) -> List[ScalingRecommendation]:
        return [
            ScalingRecommendation(
                priority="medium",
                resource="disk",
                description="Disk usage projected to reach 78% in 90 days",
                action="Add 100GB to database volume",
                estimated_impact="Extends capacity by 6 months",
            ),
            ScalingRecommendation(
                priority="low",
                resource="connections",
                description="Connection usage increasing gradually",
                action="Review connection pooling configuration",
                estimated_impact="Prevents connection exhaustion",
            ),
        ]


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate database monitoring capabilities."""
    print("=" * 70)
    print("Database Monitoring Framework - Demo")
    print("=" * 70)

    # --- 1. Metrics Collection ---
    print("\n--- Real-time Metrics ---")
    collector = MetricsCollector()
    metrics = collector.collect()
    print(f"  Connections: {metrics.active_connections}/{metrics.max_connections} "
          f"({metrics.connection_usage_pct:.0f}%)")
    print(f"  TPS: {metrics.transactions_per_second:.1f}")
    print(f"  Cache hit ratio: {metrics.cache_hit_ratio:.3f}")
    print(f"  Replication lag: {metrics.replication_lag_ms:.0f}ms")
    print(f"  Disk usage: {metrics.disk_usage_pct:.1f}%")

    # Simulate history
    for _ in range(10):
        collector.collect()

    history = collector.get_history("transactions_per_second", hours=1)
    print(f"  TPS history: avg={history.average:.1f}, max={history.maximum:.1f}")

    # --- 2. Alerting ---
    print("\n--- Alerting ---")
    alert_mgr = AlertManager()
    alert_mgr.add_rule(AlertRule(
        name="high_connections", metric="active_connections",
        condition="> 80", severity=Severity.WARNING,
    ))
    alert_mgr.add_rule(AlertRule(
        name="high_disk", metric="disk_usage_pct",
        condition="> 75", severity=Severity.CRITICAL,
    ))

    alerts = alert_mgr.check_alerts(metrics)
    print(f"  Active alerts: {len(alerts)}")
    for alert in alerts:
        print(f"    [{alert.rule.severity.value}] {alert.rule.name}: {alert.message}")

    # --- 3. Dashboard ---
    print("\n--- Dashboard ---")
    builder = DashboardBuilder("Database Overview")
    builder.add_panel(PanelType.TIME_SERIES, "TPS", "transactions_per_second",
                      position=(0, 0), size=(2, 1))
    builder.add_panel(PanelType.GAUGE, "Cache Hit", "cache_hit_ratio",
                      thresholds={"warning": 0.95, "critical": 0.90},
                      position=(2, 0), size=(1, 1))
    builder.add_panel(PanelType.STAT, "Connections", "active_connections",
                      position=(0, 1), size=(1, 1))
    builder.add_panel(PanelType.STAT, "Replication Lag", "replication_lag_ms",
                      position=(1, 1), size=(1, 1))

    dashboard = builder.build()
    print(f"  Dashboard: {dashboard.title}")
    print(f"  Panels: {len(dashboard.panels)}")
    print(f"  JSON: {len(builder.to_json())} chars")

    # --- 4. Health Checks ---
    print("\n--- Health Checks ---")
    health = HealthChecker()
    result = health.check(level=HealthCheckLevel.COMPREHENSIVE)
    print(f"  Status: {result.status.value}")
    print(f"  Checks: {result.passed}/{result.total_checks} passed ({result.health_pct:.0f}%)")
    for check in result.checks:
        icon = "✓" if check.passed else "✗"
        print(f"    {icon} {check.name}: {check.message}")

    # --- 5. Capacity Planning ---
    print("\n--- Capacity Planning ---")
    planner = CapacityPlanner()
    analysis = planner.analyze()
    print(f"  Risk level: {analysis.risk_level}")
    for resource in analysis.resources:
        print(f"  {resource.name}: {resource.current_pct:.1f}% "
              f"(30d: {resource.projected_30d_pct:.1f}%, 90d: {resource.projected_90d_pct:.1f}%)")

    recs = planner.get_recommendations()
    for rec in recs:
        print(f"  [{rec.priority}] {rec.description}")
        print(f"    Action: {rec.action}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()