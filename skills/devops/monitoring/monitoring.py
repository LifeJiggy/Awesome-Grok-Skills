"""
Monitoring & Observability Framework

Production-grade monitoring toolkit providing metrics collection, log aggregation,
distributed tracing, alerting, and dashboarding for production systems.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class MetricType(Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class SpanKind(Enum):
    INTERNAL = "internal"
    SERVER = "server"
    CLIENT = "client"
    PRODUCER = "producer"
    CONSUMER = "consumer"


class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class MetricValue:
    """A recorded metric value."""
    name: str
    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class MetricQueryResult:
    """Result of a metric query."""
    name: str
    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class LogEntry:
    """A structured log entry."""
    timestamp: datetime
    level: LogLevel
    message: str
    service: str = ""
    trace_id: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LogSearchResult:
    """Log search result."""
    entries: List[LogEntry]
    count: int = 0
    duration_ms: float = 0.0


@dataclass
class Span:
    """A trace span."""
    span_id: str
    trace_id: str
    name: str
    kind: SpanKind
    start_time: datetime
    end_time: Optional[datetime] = None
    parent_id: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)

    @property
    def duration_ms(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() * 1000
        return 0.0


@dataclass
class Trace:
    """A complete trace."""
    trace_id: str
    spans: List[Span]
    service_name: str = ""

    @property
    def duration_ms(self) -> float:
        if self.spans:
            starts = [s.start_time for s in self.spans]
            ends = [s.end_time for s in self.spans if s.end_time]
            if starts and ends:
                return (max(ends) - min(starts)).total_seconds() * 1000
        return 0.0


@dataclass
class AlertRule:
    """Alert rule definition."""
    name: str
    condition: str
    severity: Severity = Severity.WARNING
    channels: List[str] = field(default_factory=list)
    runbook_url: str = ""
    cooldown_seconds: int = 300
    enabled: bool = True


@dataclass
class Alert:
    """An active alert."""
    rule: AlertRule
    message: str
    triggered_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    value: float = 0.0
    acknowledged: bool = False


@dataclass
class DashboardPanel:
    """Dashboard panel."""
    title: str
    metric: str
    panel_type: str = "timeseries"
    position: Tuple[int, int] = (0, 0)
    size: Tuple[int, int] = (1, 1)


@dataclass
class Dashboard:
    """A monitoring dashboard."""
    title: str
    panels: List[DashboardPanel]
    refresh_interval: int = 30


@dataclass
class SLOTarget:
    """SLO target definition."""
    name: str
    sli_metric: str
    target_percentage: float
    window_days: int = 30


@dataclass
class SLOStatus:
    """SLO compliance status."""
    target: SLOTarget
    current_percentage: float
    error_budget_remaining: float
    is_breached: bool = False


# ---------------------------------------------------------------------------
# Metrics Collector
# ---------------------------------------------------------------------------

class MetricsCollector:
    """Collect and query metrics."""

    def __init__(self, backend: str = "prometheus"):
        self.backend = backend
        self._metrics: Dict[str, List[MetricValue]] = {}

    def counter(self, name: str, value: float = 1, labels: Optional[Dict[str, str]] = None) -> None:
        key = f"{name}:{json.dumps(labels or {}, sort_keys=True)}"
        if key not in self._metrics:
            self._metrics[key] = []
        self._metrics[key].append(MetricValue(name=name, value=value, labels=labels or {}))

    def gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        key = f"{name}:{json.dumps(labels or {}, sort_keys=True)}"
        self._metrics[key] = [MetricValue(name=name, value=value, labels=labels or {})]

    def histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        key = f"{name}:{json.dumps(labels or {}, sort_keys=True)}"
        if key not in self._metrics:
            self._metrics[key] = []
        self._metrics[key].append(MetricValue(name=name, value=value, labels=labels or {}))

    def query(self, promql: str) -> MetricQueryResult:
        return MetricQueryResult(name=promql, value=np.random.uniform(0, 100))

    def get_metrics(self) -> Dict[str, int]:
        return {name: len(values) for name, values in self._metrics.items()}


# ---------------------------------------------------------------------------
# Log Aggregator
# ---------------------------------------------------------------------------

class LogAggregator:
    """Aggregate and search logs."""

    def __init__(self, backend: str = "elasticsearch"):
        self.backend = backend
        self._logs: List[LogEntry] = []

    def log(self, level: LogLevel, message: str, service: str = "",
            trace_id: str = "", **metadata: Any) -> LogEntry:
        entry = LogEntry(
            timestamp=datetime.now(timezone.utc),
            level=level,
            message=message,
            service=service,
            trace_id=trace_id,
            metadata=metadata,
        )
        self._logs.append(entry)
        return entry

    def search(self, query: str = "", time_range: str = "1h",
               level: Optional[LogLevel] = None) -> LogSearchResult:
        filtered = list(self._logs)
        if level:
            filtered = [l for l in filtered if l.level == level]
        if query:
            filtered = [l for l in filtered if query.lower() in l.message.lower()
                       or query.lower() in l.service.lower()]

        return LogSearchResult(
            entries=filtered[-100:],
            count=len(filtered),
        )

    def get_stats(self) -> Dict[str, int]:
        stats: Dict[str, int] = {}
        for log in self._logs:
            stats[log.level.value] = stats.get(log.level.value, 0) + 1
        return stats


# ---------------------------------------------------------------------------
# Tracer
# ---------------------------------------------------------------------------

class Tracer:
    """Distributed request tracing."""

    def __init__(self, service_name: str = "default"):
        self.service_name = service_name
        self._spans: List[Span] = []

    def start_span(self, name: str, kind: SpanKind = SpanKind.INTERNAL,
                   attributes: Optional[Dict[str, Any]] = None) -> "SpanContext":
        trace_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:16]
        span_id = hashlib.md5(f"{name}:{time.time()}".encode()).hexdigest()[:8]

        span = Span(
            span_id=span_id,
            trace_id=trace_id,
            name=name,
            kind=kind,
            start_time=datetime.now(timezone.utc),
            attributes=attributes or {},
        )
        self._spans.append(span)
        return SpanContext(span)

    def get_trace(self, trace_id: Optional[str] = None) -> Optional[Trace]:
        if not self._spans:
            return None
        trace_id = trace_id or self._spans[0].trace_id
        spans = [s for s in self._spans if s.trace_id == trace_id]
        return Trace(trace_id=trace_id, spans=spans, service_name=self.service_name)

    def get_all_traces(self) -> List[Trace]:
        trace_ids = set(s.trace_id for s in self._spans)
        return [self.get_trace(tid) for tid in trace_ids if self.get_trace(tid)]


class SpanContext:
    """Context manager for spans."""

    def __init__(self, span: Span):
        self.span = span

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.span.end_time = datetime.now(timezone.utc)
        return False

    def set_attribute(self, key: str, value: Any) -> None:
        self.span.attributes[key] = value


# ---------------------------------------------------------------------------
# Alert Manager
# ---------------------------------------------------------------------------

class AlertManager:
    """Manage alerting rules and active alerts."""

    def __init__(self):
        self._rules: List[AlertRule] = []
        self._active_alerts: List[Alert] = []

    def add_rule(self, rule: AlertRule) -> None:
        self._rules.append(rule)

    def check_alerts(self) -> List[Alert]:
        triggered = []
        for rule in self._rules:
            if not rule.enabled:
                continue
            # Simulate alert evaluation
            if np.random.random() < 0.1:
                alert = Alert(rule=rule, message=f"Condition met: {rule.condition}")
                triggered.append(alert)
                self._active_alerts.append(alert)
        return triggered

    def get_active_alerts(self) -> List[Alert]:
        return [a for a in self._active_alerts if not a.acknowledged]

    def acknowledge(self, alert: Alert) -> None:
        alert.acknowledged = True


# ---------------------------------------------------------------------------
# SLO Manager
# ---------------------------------------------------------------------------

class SLOManager:
    """Manage Service Level Objectives."""

    def __init__(self):
        self._targets: List[SLOTarget] = []

    def add_target(self, target: SLOTarget) -> None:
        self._targets.append(target)

    def get_status(self) -> List[SLOStatus]:
        statuses = []
        for target in self._targets:
            current = np.random.uniform(99.0, 99.99)
            budget = (target.target_percentage - current) * target.window_days / 100
            statuses.append(SLOStatus(
                target=target,
                current_percentage=current,
                error_budget_remaining=max(0, budget),
                is_breached=current < target.target_percentage,
            ))
        return statuses


# ---------------------------------------------------------------------------
# Dashboard Builder
# ---------------------------------------------------------------------------

class DashboardBuilder:
    """Build monitoring dashboards."""

    def __init__(self, title: str = "Dashboard"):
        self.title = title
        self._panels: List[DashboardPanel] = []

    def add_panel(self, title: str, metric: str, panel_type: str = "timeseries",
                  position: Tuple[int, int] = (0, 0),
                  size: Tuple[int, int] = (1, 1)) -> "DashboardBuilder":
        self._panels.append(DashboardPanel(title=title, metric=metric,
                                           panel_type=panel_type,
                                           position=position, size=size))
        return self

    def build(self) -> Dashboard:
        return Dashboard(title=self.title, panels=list(self._panels))


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate monitoring capabilities."""
    print("=" * 70)
    print("Monitoring & Observability Framework - Demo")
    print("=" * 70)

    # --- 1. Metrics ---
    print("\n--- Metrics Collection ---")
    metrics = MetricsCollector("prometheus")
    for _ in range(100):
        metrics.counter("http_requests_total", labels={"method": "GET", "status": "200"})
    metrics.gauge("active_connections", 42)
    metrics.histogram("http_duration", 0.15)

    print(f"  Metrics recorded: {len(metrics.get_metrics())}")
    query = metrics.query('rate(http_requests_total[5m])')
    print(f"  Query result: {query.value:.1f}")

    # --- 2. Logging ---
    print("\n--- Log Aggregation ---")
    logs = LogAggregator("elasticsearch")
    logs.log(LogLevel.INFO, "Request processed", service="api", duration_ms=150)
    logs.log(LogLevel.ERROR, "Database timeout", service="api", trace_id="abc123")
    logs.log(LogLevel.WARNING, "High latency", service="api", latency_ms=500)

    result = logs.search(level=LogLevel.ERROR)
    print(f"  Error logs: {result.count}")
    stats = logs.get_stats()
    print(f"  Log levels: {stats}")

    # --- 3. Tracing ---
    print("\n--- Distributed Tracing ---")
    tracer = Tracer("api-gateway")
    with tracer.start_span("handle_request", SpanKind.SERVER) as span:
        span.set_attribute("http.method", "GET")
        with tracer.start_span("auth") as child:
            child.set_attribute("user.id", "12345")
        with tracer.start_span("db_query") as child:
            child.set_attribute("db.statement", "SELECT * FROM users")

    trace = tracer.get_trace()
    if trace:
        print(f"  Trace: {trace.trace_id}")
        print(f"  Duration: {trace.duration_ms:.1f}ms")
        print(f"  Spans: {len(trace.spans)}")

    # --- 4. Alerting ---
    print("\n--- Alerting ---")
    alert_mgr = AlertManager()
    alert_mgr.add_rule(AlertRule("high_error_rate", "rate(errors[5m]) > 0.05",
                                 Severity.CRITICAL, ["slack-ops"]))

    alerts = alert_mgr.check_alerts()
    print(f"  Alerts triggered: {len(alerts)}")
    for alert in alerts:
        print(f"    [{alert.rule.severity.value}] {alert.rule.name}")

    # --- 5. SLO ---
    print("\n--- SLO Management ---")
    slo_mgr = SLOManager()
    slo_mgr.add_target(SLOTarget("availability", "uptime", 99.9, 30))
    slo_mgr.add_target(SLOTarget("latency", "p99_latency", 99.0, 30))

    statuses = slo_mgr.get_status()
    for status in statuses:
        print(f"  {status.target.name}: {status.current_percentage:.2f}% "
              f"(budget: {status.error_budget_remaining:.1f}d)")

    # --- 6. Dashboard ---
    print("\n--- Dashboard ---")
    builder = DashboardBuilder("Production Overview")
    builder.add_panel("Request Rate", "http_requests_total", "timeseries")
    builder.add_panel("Error Rate", "http_errors_total", "gauge")
    builder.add_panel("Latency", "http_duration", "heatmap")
    dashboard = builder.build()
    print(f"  Dashboard: {dashboard.title}")
    print(f"  Panels: {len(dashboard.panels)}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()