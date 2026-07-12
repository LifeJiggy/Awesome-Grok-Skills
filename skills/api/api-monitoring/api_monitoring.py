"""
API Monitoring Module — Metrics collection, distributed tracing, structured logging,
SLA tracking, alerting, and dashboard generation for API observability.
"""

from __future__ import annotations

import json
import math
import statistics
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class MetricType(Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class AlertStatus(Enum):
    PENDING = "pending"
    FIRING = "firing"
    RESOLVED = "resolved"
    SILENCED = "silenced"


class TraceSpanStatus(Enum):
    OK = "ok"
    ERROR = "error"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class RequestMetric:
    """A single API request metric."""
    method: str
    path: str
    status_code: int
    latency_ms: float
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    consumer_id: str = ""
    request_size_bytes: int = 0
    response_size_bytes: int = 0
    user_agent: str = ""
    trace_id: str = ""

    @property
    def endpoint_key(self) -> str:
        return f"{self.method} {self.path}"

    @property
    def is_error(self) -> bool:
        return self.status_code >= 400

    def to_dict(self) -> Dict[str, Any]:
        return {
            "method": self.method,
            "path": self.path,
            "status": self.status_code,
            "latency_ms": round(self.latency_ms, 2),
            "consumer": self.consumer_id,
        }


@dataclass
class EndpointSummary:
    """Summary metrics for an endpoint."""
    endpoint: str
    total_requests: int = 0
    error_count: int = 0
    avg_latency_ms: float = 0.0
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    min_latency_ms: float = 0.0
    max_latency_ms: float = 0.0
    requests_per_second: float = 0.0
    error_rate: float = 0.0
    time_window_s: float = 300

    def to_dict(self) -> Dict[str, Any]:
        return {
            "endpoint": self.endpoint,
            "total_requests": self.total_requests,
            "error_rate": round(self.error_rate, 4),
            "avg_latency": round(self.avg_latency_ms, 2),
            "p50": round(self.p50_latency_ms, 2),
            "p95": round(self.p95_latency_ms, 2),
            "p99": round(self.p99_latency_ms, 2),
            "rps": round(self.requests_per_second, 1),
        }


@dataclass
class TraceSpan:
    """A distributed tracing span."""
    span_id: str
    trace_id: str
    parent_span_id: Optional[str]
    name: str
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    status: TraceSpanStatus = TraceSpanStatus.OK
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def duration_ms(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time) * 1000
        return 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "span_id": self.span_id,
            "trace_id": self.trace_id,
            "parent": self.parent_span_id,
            "name": self.name,
            "duration_ms": round(self.duration_ms, 2),
            "status": self.status.value,
        }


@dataclass
class LogEntry:
    """A structured API log entry."""
    timestamp: str
    level: str
    method: str
    path: str
    status_code: int
    latency_ms: float
    correlation_id: str
    user_id: str = ""
    consumer_id: str = ""
    message: str = ""
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps({
            "timestamp": self.timestamp,
            "level": self.level,
            "method": self.method,
            "path": self.path,
            "status": self.status_code,
            "latency_ms": round(self.latency_ms, 2),
            "correlation_id": self.correlation_id,
            "user_id": self.user_id,
            "message": self.message,
        })


@dataclass
class AlertRule:
    """An alert rule definition."""
    rule_id: str
    name: str
    metric: str
    condition: str
    threshold: float
    window_minutes: int = 5
    severity: AlertSeverity = AlertSeverity.WARNING
    notify: List[str] = field(default_factory=list)
    enabled: bool = True
    cooldown_minutes: int = 15
    last_fired: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "metric": self.metric,
            "condition": self.condition,
            "threshold": self.threshold,
            "severity": self.severity.value,
        }


@dataclass
class Alert:
    """A fired alert."""
    alert_id: str
    rule_id: str
    severity: AlertSeverity
    status: AlertStatus
    message: str
    metric_value: float
    threshold: float
    fired_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    resolved_at: Optional[str] = None
    acknowledged_by: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "rule": self.rule_id,
            "severity": self.severity.value,
            "status": self.status.value,
            "message": self.message,
        }


@dataclass
class SLADefinition:
    """An SLA definition."""
    name: str
    metric: str
    target: float
    window: str = "30d"
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "metric": self.metric, "target": self.target, "window": self.window}


@dataclass
class SLAStatus:
    """Current SLA compliance status."""
    name: str
    current: float
    target: float
    compliant: bool
    budget_remaining_pct: float
    window: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "current": round(self.current, 2),
            "target": self.target,
            "compliant": self.compliant,
            "budget_remaining": round(self.budget_remaining_pct, 1),
        }


@dataclass
class DashboardPanel:
    """A dashboard panel configuration."""
    panel_id: str
    title: str
    panel_type: str  # "graph", "stat", "table", "heatmap"
    query: str
    position: Tuple[int, int] = (0, 0)
    size: Tuple[int, int] = (6, 4)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "panel_id": self.panel_id,
            "title": self.title,
            "type": self.panel_type,
            "query": self.query,
        }


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class MetricsCollector:
    """Collect and query API request metrics."""

    def __init__(self):
        self._requests: List[RequestMetric] = []
        self._counters: Dict[str, int] = defaultdict(int)
        self._latencies: Dict[str, List[float]] = defaultdict(list)

    def record_request(self, method: str, path: str, status_code: int,
                       latency_ms: float, consumer_id: str = "", **kwargs: Any) -> None:
        metric = RequestMetric(
            method=method, path=path, status_code=status_code,
            latency_ms=latency_ms, consumer_id=consumer_id, **kwargs,
        )
        self._requests.append(metric)
        key = metric.endpoint_key
        self._counters[key] += 1
        self._latencies[key].append(latency_ms)
        if status_code >= 400:
            self._counters[f"{key}:errors"] += 1

    def get_endpoint_summary(self, endpoint: str, window_s: float = 300) -> Dict[str, Any]:
        cutoff = time.time() - window_s
        recent = [r for r in self._requests if r.endpoint_key == endpoint
                  and datetime.fromisoformat(r.timestamp).timestamp() > cutoff]

        if not recent:
            return {"endpoint": endpoint, "total_requests": 0}

        latencies = sorted([r.latency_ms for r in recent])
        n = len(latencies)
        errors = sum(1 for r in recent if r.is_error)

        return {
            "endpoint": endpoint,
            "total_requests": n,
            "error_count": errors,
            "error_rate": errors / n if n > 0 else 0,
            "avg_latency_ms": statistics.mean(latencies) if latencies else 0,
            "p50_latency_ms": latencies[n // 2] if latencies else 0,
            "p95_latency_ms": latencies[int(n * 0.95)] if n > 20 else latencies[-1] if latencies else 0,
            "p99_latency_ms": latencies[int(n * 0.99)] if n > 100 else latencies[-1] if latencies else 0,
            "min_latency_ms": min(latencies) if latencies else 0,
            "max_latency_ms": max(latencies) if latencies else 0,
            "requests_per_second": n / window_s,
        }

    def get_global_summary(self) -> Dict[str, Any]:
        total = len(self._requests)
        errors = sum(1 for r in self._requests if r.is_error)
        all_latencies = [r.latency_ms for r in self._requests]
        return {
            "total_requests": total,
            "error_rate": errors / total if total > 0 else 0,
            "avg_latency_ms": statistics.mean(all_latencies) if all_latencies else 0,
            "unique_endpoints": len(set(r.endpoint_key for r in self._requests)),
            "unique_consumers": len(set(r.consumer_id for r in self._requests if r.consumer_id)),
        }

    def get_consumer_summary(self, consumer_id: str) -> Dict[str, Any]:
        consumer_reqs = [r for r in self._requests if r.consumer_id == consumer_id]
        return {
            "consumer_id": consumer_id,
            "total_requests": len(consumer_reqs),
            "endpoints_used": len(set(r.endpoint_key for r in consumer_reqs)),
        }


class TraceCollector:
    """Distributed tracing span collection and query."""

    def __init__(self):
        self._spans: Dict[str, TraceSpan] = {}

    def start_span(self, name: str, parent_span_id: Optional[str] = None,
                   trace_id: Optional[str] = None) -> TraceSpan:
        span = TraceSpan(
            span_id=uuid.uuid4().hex[:16],
            trace_id=trace_id or uuid.uuid4().hex,
            parent_span_id=parent_span_id,
            name=name,
        )
        self._spans[span.span_id] = span
        return span

    def end_span(self, span: TraceSpan, status: TraceSpanStatus = TraceSpanStatus.OK,
                 attributes: Optional[Dict[str, Any]] = None) -> None:
        span.end_time = time.time()
        span.status = status
        if attributes:
            span.attributes.update(attributes)

    def get_trace(self, trace_id: str) -> List[TraceSpan]:
        return [s for s in self._spans.values() if s.trace_id == trace_id]

    def get_slow_traces(self, threshold_ms: float = 1000) -> List[List[TraceSpan]]:
        trace_groups: Dict[str, List[TraceSpan]] = defaultdict(list)
        for span in self._spans.values():
            trace_groups[span.trace_id].append(span)

        slow_traces = []
        for trace_id, spans in trace_groups.items():
            root_spans = [s for s in spans if not s.parent_span_id]
            for root in root_spans:
                if root.duration_ms > threshold_ms:
                    slow_traces.append(spans)
        return slow_traces


class AlertManager:
    """Alert rule management and alert firing."""

    def __init__(self):
        self._rules: Dict[str, AlertRule] = {}
        self._alerts: List[Alert] = []

    def add_rule(self, name: str, metric: str, condition: str, threshold: float,
                 window_minutes: int = 5, severity: str = "warning",
                 notify: Optional[List[str]] = None) -> AlertRule:
        rule = AlertRule(
            rule_id=f"RULE-{uuid.uuid4().hex[:8].upper()}",
            name=name, metric=metric, condition=condition, threshold=threshold,
            window_minutes=window_minutes,
            severity=AlertSeverity(severity),
            notify=notify or [],
        )
        self._rules[rule.rule_id] = rule
        return rule

    def evaluate(self, metrics: Dict[str, float]) -> List[Alert]:
        fired = []
        for rule in self._rules.values():
            if not rule.enabled:
                continue
            value = metrics.get(rule.metric, 0)
            triggered = False
            if ">" in rule.condition and value > rule.threshold:
                triggered = True
            elif "<" in rule.condition and value < rule.threshold:
                triggered = True

            if triggered:
                alert = Alert(
                    alert_id=f"ALT-{uuid.uuid4().hex[:8].upper()}",
                    rule_id=rule.rule_id,
                    severity=rule.severity,
                    status=AlertStatus.FIRING,
                    message=f"{rule.name}: {rule.metric}={value} (threshold={rule.threshold})",
                    metric_value=value,
                    threshold=rule.threshold,
                )
                self._alerts.append(alert)
                rule.last_fired = datetime.now(timezone.utc).isoformat()
                fired.append(alert)
        return fired

    def get_active_alerts(self) -> List[Alert]:
        return [a for a in self._alerts if a.status == AlertStatus.FIRING]

    def acknowledge(self, alert_id: str, user: str) -> None:
        for alert in self._alerts:
            if alert.alert_id == alert_id:
                alert.acknowledged_by = user


class SLATracker:
    """Track and report on SLA compliance."""

    def __init__(self):
        self._slas: Dict[str, SLADefinition] = {}
        self._values: Dict[str, List[float]] = {}

    def define_sla(self, name: str, metric: str, target: float, window: str = "30d") -> None:
        self._slas[name] = SLADefinition(name=name, metric=metric, target=target, window=window)

    def record(self, sla_name: str, value: float) -> None:
        if sla_name not in self._values:
            self._values[sla_name] = []
        self._values[sla_name].append(value)

    def check(self, sla_name: str) -> Dict[str, Any]:
        sla = self._slas.get(sla_name)
        if not sla:
            return {"name": sla_name, "error": "SLA not found"}

        values = self._values.get(sla_name, [])
        current = statistics.mean(values) if values else sla.target
        compliant = current >= sla.target
        budget = ((current - sla.target) / sla.target * 100) if sla.target > 0 else 0

        return {
            "name": sla_name,
            "current": current,
            "target": sla.target,
            "compliant": compliant,
            "budget_remaining_pct": budget,
            "window": sla.window,
        }

    def get_all_status(self) -> List[Dict[str, Any]]:
        return [self.check(name) for name in self._slas]


class DashboardGenerator:
    """Auto-generate monitoring dashboards."""

    def generate_api_dashboard(self, endpoints: List[str]) -> Dict[str, Any]:
        panels = []
        for i, ep in enumerate(endpoints):
            panels.append(DashboardPanel(
                panel_id=f"panel-{i}",
                title=f"{ep} — Request Rate",
                panel_type="graph",
                query=f'rate(requests_total{{endpoint="{ep}"}}[5m])',
                position=(i * 6, 0),
            ))
            panels.append(DashboardPanel(
                panel_id=f"panel-latency-{i}",
                title=f"{ep} — Latency",
                panel_type="graph",
                query=f'histogram_quantile(0.99, request_latency_bucket{{endpoint="{ep}"}})',
                position=(i * 6, 4),
            ))

        panels.append(DashboardPanel(
            panel_id="global-errors",
            title="Global Error Rate",
            panel_type="stat",
            query='sum(rate(requests_total{status=~"5.."}[5m])) / sum(rate(requests_total[5m]))',
            position=(0, 8),
        ))

        return {
            "dashboard": {
                "title": "API Overview",
                "panels": [p.to_dict() for p in panels],
                "refresh": "30s",
            }
        }


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the API monitoring toolkit."""
    print("API Monitoring Toolkit")
    print("=" * 60)

    # Metrics
    metrics = MetricsCollector()
    import random
    for _ in range(100):
        metrics.record_request(
            method="GET", path="/api/users",
            status_code=random.choice([200, 200, 200, 404, 500]),
            latency_ms=random.uniform(10, 200),
            consumer_id=f"client-{random.randint(1,5)}",
        )

    summary = metrics.get_endpoint_summary("GET /api/users")
    print(f"\nEndpoint: GET /api/users")
    print(f"  Requests: {summary['total_requests']}")
    print(f"  Error rate: {summary['error_rate']:.1%}")
    print(f"  p50: {summary['p50_latency_ms']:.1f}ms, p95: {summary['p95_latency_ms']:.1f}ms, p99: {summary['p99_latency_ms']:.1f}ms")

    # Tracing
    tracer = TraceCollector()
    span = tracer.start_span("GET /api/users")
    child = tracer.start_span("db.query", parent_span_id=span.span_id)
    tracer.end_span(child, attributes={"db.statement": "SELECT * FROM users"})
    tracer.end_span(span, attributes={"http.status_code": 200})
    print(f"\nTrace: {span.duration_ms:.1f}ms total")

    # Alerting
    alerts = AlertManager()
    alerts.add_rule("high-error-rate", "error_rate", ">", 0.05, severity="critical")
    fired = alerts.evaluate({"error_rate": 0.08})
    print(f"\nAlerts fired: {len(fired)}")
    for a in fired:
        print(f"  [{a.severity.value}] {a.message}")

    # SLA
    sla = SLATracker()
    sla.define_sla("availability", "availability", 99.9, "30d")
    sla.record("availability", 99.95)
    status = sla.check("availability")
    print(f"\nSLA: {status['name']}={status['current']:.2f}% (compliant: {status['compliant']})")

    # Dashboard
    dash = DashboardGenerator()
    dashboard = dash.generate_api_dashboard(["GET /api/users", "POST /api/users"])
    print(f"\nDashboard: {len(dashboard['dashboard']['panels'])} panels")


if __name__ == "__main__":
    main()
