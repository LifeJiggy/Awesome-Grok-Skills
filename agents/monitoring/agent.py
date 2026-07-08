"""
Monitoring Agent
Infrastructure monitoring, alerting, APM, log aggregation, dashboards, and incident correlation.
"""

import logging
import math
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple
from uuid import uuid4

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────

class AlertSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AlertStatus(Enum):
    FIRING = "firing"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    SILENCED = "silenced"


class MetricType(Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class IncidentSeverity(Enum):
    SEV1 = "sev1"
    SEV2 = "sev2"
    SEV3 = "sev3"
    SEV4 = "sev4"


class IncidentStatus(Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    IDENTIFIED = "identified"
    MONITORING = "monitoring"
    RESOLVED = "closed"


class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class DashboardPanelType(Enum):
    GRAPH = "graph"
    SINGLESTAT = "singlestat"
    TABLE = "table"
    HEATMAP = "heatmap"
    BAR = "bar"
    PIE = "pie"
    TEXT = "text"


# ──────────────────────────────────────────────
# Data Classes
# ──────────────────────────────────────────────

@dataclass
class MetricPoint:
    name: str = ""
    value: float = 0.0
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class MetricDefinition:
    name: str = ""
    metric_type: MetricType = MetricType.GAUGE
    description: str = ""
    labels: List[str] = field(default_factory=list)
    buckets: List[float] = field(default_factory=list)


@dataclass
class AlertRule:
    rule_id: str = field(default_factory=lambda: f"rule_{str(uuid4())[:8]}")
    name: str = ""
    expression: str = ""
    severity: AlertSeverity = AlertSeverity.MEDIUM
    for_duration: str = "5m"
    labels: Dict[str, str] = field(default_factory=dict)
    annotations: Dict[str, str] = field(default_factory=dict)
    enabled: bool = True


@dataclass
class Alert:
    alert_id: str = field(default_factory=lambda: f"alert_{str(uuid4())[:8]}")
    rule_id: str = ""
    name: str = ""
    severity: AlertSeverity = AlertSeverity.MEDIUM
    status: AlertStatus = AlertStatus.FIRING
    message: str = ""
    labels: Dict[str, str] = field(default_factory=dict)
    starts_at: datetime = field(default_factory=datetime.now)
    ends_at: Optional[datetime] = None
    acknowledged_by: Optional[str] = None


@dataclass
class UptimeCheck:
    check_id: str = field(default_factory=lambda: f"check_{str(uuid4())[:8]}")
    name: str = ""
    url: str = ""
    method: str = "GET"
    expected_status: int = 200
    timeout_seconds: int = 10
    interval_seconds: int = 60
    status: HealthStatus = HealthStatus.UNKNOWN
    last_check: Optional[datetime] = None
    response_time_ms: float = 0.0


@dataclass
class LogEntry:
    entry_id: str = field(default_factory=lambda: str(uuid4())[:8])
    timestamp: datetime = field(default_factory=datetime.now)
    level: LogLevel = LogLevel.INFO
    source: str = ""
    message: str = ""
    fields: Dict[str, Any] = field(default_factory=dict)
    matched_rules: List[str] = field(default_factory=list)


@dataclass
class LogPattern:
    pattern_id: str = field(default_factory=lambda: f"pat_{str(uuid4())[:8]}")
    name: str = ""
    regex: str = ""
    severity: AlertSeverity = AlertSeverity.MEDIUM
    description: str = ""
    match_count: int = 0


@dataclass
class Incident:
    incident_id: str = field(default_factory=lambda: f"inc_{str(uuid4())[:8]}")
    title: str = ""
    severity: IncidentSeverity = IncidentSeverity.SEV3
    status: IncidentStatus = IncidentStatus.OPEN
    description: str = ""
    affected_services: List[str] = field(default_factory=list)
    related_alerts: List[str] = field(default_factory=list)
    timeline: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None


@dataclass
class DashboardPanel:
    panel_id: str = field(default_factory=lambda: f"panel_{str(uuid4())[:8]}")
    title: str = ""
    panel_type: DashboardPanelType = DashboardPanelType.GRAPH
    metrics: List[str] = field(default_factory=list)
    visualization: str = "graph"
    position: Dict[str, int] = field(default_factory=dict)


@dataclass
class Dashboard:
    dashboard_id: str = field(default_factory=lambda: f"dash_{str(uuid4())[:8]}")
    title: str = ""
    panels: List[DashboardPanel] = field(default_factory=list)
    refresh_interval: int = 30
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ServiceHealth:
    service_name: str = ""
    status: HealthStatus = HealthStatus.UNKNOWN
    uptime_percent: float = 100.0
    avg_response_ms: float = 0.0
    error_rate: float = 0.0
    last_incident: Optional[datetime] = None


@dataclass
class SLO:
    slo_id: str = field(default_factory=lambda: f"slo_{str(uuid4())[:8]}")
    service: str = ""
    metric: str = ""
    target: float = 99.9
    window_days: int = 30
    current_value: float = 100.0
    error_budget_remaining: float = 100.0


# ──────────────────────────────────────────────
# Exceptions
# ──────────────────────────────────────────────

class MonitoringError(Exception):
    """Base monitoring error."""


class AlertRuleNotFoundError(MonitoringError):
    """Alert rule not found."""


class DashboardNotFoundError(MonitoringError):
    """Dashboard not found."""


class IncidentNotFoundError(MonitoringError):
    """Incident not found."""


# ──────────────────────────────────────────────
# Prometheus Metrics Collector
# ──────────────────────────────────────────────

class PrometheusMetrics:
    """Prometheus-style metrics collection."""

    def __init__(self) -> None:
        self._definitions: Dict[str, MetricDefinition] = {}
        self._counters: Dict[str, float] = {}
        self._gauges: Dict[str, float] = {}
        self._histograms: Dict[str, List[float]] = {}
        self._timestamps: Dict[str, datetime] = {}

    def define_counter(self, name: str, description: str = "", labels: Optional[List[str]] = None) -> None:
        self._definitions[name] = MetricDefinition(name=name, metric_type=MetricType.COUNTER, description=description, labels=labels or [])

    def define_gauge(self, name: str, description: str = "", labels: Optional[List[str]] = None) -> None:
        self._definitions[name] = MetricDefinition(name=name, metric_type=MetricType.GAUGE, description=description, labels=labels or [])

    def define_histogram(self, name: str, description: str = "", buckets: Optional[List[float]] = None) -> None:
        self._definitions[name] = MetricDefinition(name=name, metric_type=MetricType.HISTOGRAM, description=description, buckets=buckets or [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0])

    def inc_counter(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        key = self._make_key(name, labels)
        self._counters[key] = self._counters.get(key, 0) + value
        self._timestamps[key] = datetime.now()

    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        key = self._make_key(name, labels)
        self._gauges[key] = value
        self._timestamps[key] = datetime.now()

    def observe_histogram(self, name: str, value: float) -> None:
        self._histograms.setdefault(name, []).append(value)
        self._timestamps[name] = datetime.now()

    def get_counter(self, name: str) -> float:
        return self._counters.get(name, 0.0)

    def get_gauge(self, name: str) -> float:
        return self._gauges.get(name, 0.0)

    def get_histogram_stats(self, name: str) -> Dict[str, float]:
        values = self._histograms.get(name, [])
        if not values:
            return {"count": 0, "sum": 0, "avg": 0, "min": 0, "max": 0}
        return {
            "count": len(values),
            "sum": round(sum(values), 4),
            "avg": round(sum(values) / len(values), 4),
            "min": min(values),
            "max": max(values),
        }

    def scrape(self) -> Dict[str, Any]:
        metrics: Dict[str, Any] = {}
        for key, value in self._counters.items():
            metrics[f"{key}_total"] = value
        for key, value in self._gauges.items():
            metrics[key] = value
        for name, values in self._histograms.items():
            stats = self.get_histogram_stats(name)
            metrics[f"{name}_count"] = stats["count"]
            metrics[f"{name}_sum"] = stats["sum"]
            metrics[f"{name}_avg"] = stats["avg"]
        return metrics

    def _make_key(self, name: str, labels: Optional[Dict[str, str]] = None) -> str:
        if labels:
            label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
            return f"{name}{{{label_str}}}"
        return name


# ──────────────────────────────────────────────
# Alert Manager
# ──────────────────────────────────────────────

class AlertManager:
    """Create, manage, and evaluate alert rules."""

    def __init__(self) -> None:
        self._rules: Dict[str, AlertRule] = {}
        self._alerts: Dict[str, Alert] = {}
        self._notification_channels: Dict[AlertSeverity, List[str]] = {
            AlertSeverity.CRITICAL: ["pager", "slack", "email"],
            AlertSeverity.HIGH: ["slack", "email"],
            AlertSeverity.MEDIUM: ["slack"],
            AlertSeverity.LOW: ["email"],
            AlertSeverity.INFO: [],
        }

    def add_rule(
        self,
        name: str,
        expression: str,
        severity: AlertSeverity,
        for_duration: str = "5m",
        labels: Optional[Dict[str, str]] = None,
        annotations: Optional[Dict[str, str]] = None,
    ) -> AlertRule:
        rule = AlertRule(
            name=name,
            expression=expression,
            severity=severity,
            for_duration=for_duration,
            labels=labels or {},
            annotations=annotations or {},
        )
        self._rules[rule.rule_id] = rule
        logger.info("Added alert rule %s (%s)", rule.rule_id, name)
        return rule

    def fire_alert(
        self,
        rule_id: str,
        message: str = "",
        labels: Optional[Dict[str, str]] = None,
    ) -> Alert:
        rule = self._get_rule(rule_id)
        alert = Alert(
            rule_id=rule_id,
            name=rule.name,
            severity=rule.severity,
            message=message or rule.annotations.get("summary", "Alert fired"),
            labels={**rule.labels, **(labels or {})},
        )
        self._alerts[alert.alert_id] = alert
        self._send_notification(alert)
        logger.warning("Alert fired: %s (severity: %s)", rule.name, rule.severity.value)
        return alert

    def acknowledge_alert(self, alert_id: str, acknowledged_by: str = "system") -> Alert:
        alert = self._get_alert(alert_id)
        alert.status = AlertStatus.ACKNOWLEDGED
        alert.acknowledged_by = acknowledged_by
        return alert

    def resolve_alert(self, alert_id: str) -> Alert:
        alert = self._get_alert(alert_id)
        alert.status = AlertStatus.RESOLVED
        alert.ends_at = datetime.now()
        return alert

    def silence_alert(self, alert_id: str) -> Alert:
        alert = self._get_alert(alert_id)
        alert.status = AlertStatus.SILENCED
        return alert

    def get_active_alerts(self) -> List[Alert]:
        return [
            a for a in self._alerts.values()
            if a.status in (AlertStatus.FIRING, AlertStatus.ACKNOWLEDGED)
        ]

    def get_alerts_by_severity(self, severity: AlertSeverity) -> List[Alert]:
        return [a for a in self._alerts.values() if a.severity == severity]

    def get_rule(self, rule_id: str) -> AlertRule:
        return self._get_rule(rule_id)

    def list_rules(self) -> List[AlertRule]:
        return list(self._rules.values())

    def list_alerts(self) -> List[Alert]:
        return list(self._alerts.values())

    def _send_notification(self, alert: Alert) -> None:
        channels = self._notification_channels.get(alert.severity, [])
        logger.info("Sending %s notification to %s for alert %s", alert.severity.value, channels, alert.alert_id)

    def _get_rule(self, rule_id: str) -> AlertRule:
        if rule_id not in self._rules:
            raise AlertRuleNotFoundError(f"Rule {rule_id} not found")
        return self._rules[rule_id]

    def _get_alert(self, alert_id: str) -> Alert:
        if alert_id not in self._alerts:
            raise MonitoringError(f"Alert {alert_id} not found")
        return self._alerts[alert_id]


# ──────────────────────────────────────────────
# Uptime Monitor
# ──────────────────────────────────────────────

class UptimeMonitor:
    """Monitor endpoint availability and response times."""

    def __init__(self) -> None:
        self._checks: Dict[str, UptimeCheck] = {}
        self._history: Dict[str, List[Dict[str, Any]]] = {}

    def add_check(
        self,
        name: str,
        url: str,
        method: str = "GET",
        expected_status: int = 200,
        timeout: int = 10,
        interval: int = 60,
    ) -> UptimeCheck:
        check = UptimeCheck(
            name=name,
            url=url,
            method=method,
            expected_status=expected_status,
            timeout_seconds=timeout,
            interval_seconds=interval,
        )
        self._checks[check.check_id] = check
        logger.info("Added uptime check %s for %s", check.check_id, url)
        return check

    def record_check(self, check_id: str, status_code: int, response_time_ms: float, success: bool) -> Dict[str, Any]:
        check = self._get_check(check_id)
        check.status = HealthStatus.HEALTHY if success else HealthStatus.UNHEALTHY
        check.last_check = datetime.now()
        check.response_time_ms = response_time_ms
        result = {
            "check_id": check_id,
            "status_code": status_code,
            "response_time_ms": response_time_ms,
            "success": success,
            "timestamp": datetime.now(),
        }
        self._history.setdefault(check_id, []).append(result)
        return result

    def get_uptime(self, check_id: str, hours: int = 24) -> Dict[str, Any]:
        check = self._get_check(check_id)
        history = self._history.get(check_id, [])
        since = datetime.now() - timedelta(hours=hours)
        recent = [h for h in history if h["timestamp"] >= since]
        total = len(recent)
        successful = sum(1 for h in recent if h["success"])
        uptime = (successful / total * 100) if total > 0 else 100.0
        avg_response = sum(h["response_time_ms"] for h in recent) / total if total > 0 else 0
        return {
            "check_id": check_id,
            "name": check.name,
            "uptime_percent": round(uptime, 3),
            "total_checks": total,
            "successful": successful,
            "failed": total - successful,
            "avg_response_ms": round(avg_response, 2),
        }

    def get_status_summary(self) -> Dict[str, Any]:
        total = len(self._checks)
        healthy = sum(1 for c in self._checks.values() if c.status == HealthStatus.HEALTHY)
        unhealthy = sum(1 for c in self._checks.values() if c.status == HealthStatus.UNHEALTHY)
        return {
            "total_checks": total,
            "healthy": healthy,
            "unhealthy": unhealthy,
            "unknown": total - healthy - unhealthy,
        }

    def get_check(self, check_id: str) -> UptimeCheck:
        return self._get_check(check_id)

    def list_checks(self) -> List[UptimeCheck]:
        return list(self._checks.values())

    def _get_check(self, check_id: str) -> UptimeCheck:
        if check_id not in self._checks:
            raise MonitoringError(f"Check {check_id} not found")
        return self._checks[check_id]


# ──────────────────────────────────────────────
# Log Monitor
# ──────────────────────────────────────────────

class LogMonitor:
    """Ingest, search, and analyze logs."""

    def __init__(self) -> None:
        self._logs: List[LogEntry] = []
        self._patterns: Dict[str, LogPattern] = {}

    def add_pattern(self, name: str, regex: str, severity: AlertSeverity, description: str = "") -> LogPattern:
        pattern = LogPattern(name=name, regex=regex, severity=severity, description=description)
        self._patterns[pattern.pattern_id] = pattern
        return pattern

    def ingest(self, message: str, source: str = "app", level: LogLevel = LogLevel.INFO, fields: Optional[Dict[str, Any]] = None) -> LogEntry:
        entry = LogEntry(message=message, source=source, level=level, fields=fields or {})
        for pattern in self._patterns.values():
            if re.search(pattern.regex, message):
                entry.matched_rules.append(pattern.pattern_id)
                pattern.match_count += 1
        self._logs.append(entry)
        if entry.matched_rules:
            logger.warning("Log matched pattern(s): %s", entry.matched_rules)
        return entry

    def search(self, query: str, level: Optional[LogLevel] = None, source: Optional[str] = None, since: Optional[datetime] = None) -> List[LogEntry]:
        results = self._logs
        if level:
            results = [l for l in results if l.level == level]
        if source:
            results = [l for l in results if l.source == source]
        if since:
            results = [l for l in results if l.timestamp >= since]
        if query:
            results = [l for l in results if query.lower() in l.message.lower()]
        return results

    def get_error_summary(self, hours: int = 1) -> Dict[str, Any]:
        since = datetime.now() - timedelta(hours=hours)
        errors = [l for l in self._logs if l.level in (LogLevel.ERROR, LogLevel.CRITICAL) and l.timestamp >= since]
        by_pattern: Dict[str, int] = {}
        for e in errors:
            for pid in e.matched_rules:
                by_pattern[pid] = by_pattern.get(pid, 0) + 1
        return {
            "total_errors": len(errors),
            "by_pattern": by_pattern,
            "error_rate": round(len(errors) / max(1, len(self._logs)) * 100, 2),
        }

    def get_log_volume(self, hours: int = 1) -> Dict[str, Any]:
        since = datetime.now() - timedelta(hours=hours)
        recent = [l for l in self._logs if l.timestamp >= since]
        by_level: Dict[str, int] = {}
        by_source: Dict[str, int] = {}
        for l in recent:
            by_level[l.level.value] = by_level.get(l.level.value, 0) + 1
            by_source[l.source] = by_source.get(l.source, 0) + 1
        return {"total": len(recent), "by_level": by_level, "by_source": by_source}

    def list_patterns(self) -> List[LogPattern]:
        return list(self._patterns.values())


# ──────────────────────────────────────────────
# Dashboard Generator
# ──────────────────────────────────────────────

class DashboardGenerator:
    """Create and manage monitoring dashboards."""

    def __init__(self) -> None:
        self._dashboards: Dict[str, Dashboard] = {}

    def create_dashboard(self, title: str, refresh_interval: int = 30) -> Dashboard:
        dashboard = Dashboard(title=title, refresh_interval=refresh_interval)
        self._dashboards[dashboard.dashboard_id] = dashboard
        return dashboard

    def add_panel(
        self,
        dashboard_id: str,
        title: str,
        panel_type: DashboardPanelType,
        metrics: List[str],
        position: Optional[Dict[str, int]] = None,
    ) -> DashboardPanel:
        dashboard = self._get_dashboard(dashboard_id)
        panel = DashboardPanel(title=title, panel_type=panel_type, metrics=metrics, position=position or {})
        dashboard.panels.append(panel)
        return panel

    def get_dashboard(self, dashboard_id: str) -> Dashboard:
        return self._get_dashboard(dashboard_id)

    def export_json(self, dashboard_id: str) -> Dict[str, Any]:
        dashboard = self._get_dashboard(dashboard_id)
        return {
            "title": dashboard.title,
            "refresh_interval": dashboard.refresh_interval,
            "panels": [
                {
                    "title": p.title,
                    "type": p.panel_type.value,
                    "metrics": p.metrics,
                    "position": p.position,
                }
                for p in dashboard.panels
            ],
            "created_at": dashboard.created_at.isoformat(),
        }

    def list_dashboards(self) -> List[Dashboard]:
        return list(self._dashboards.values())

    def _get_dashboard(self, dashboard_id: str) -> Dashboard:
        if dashboard_id not in self._dashboards:
            raise DashboardNotFoundError(f"Dashboard {dashboard_id} not found")
        return self._dashboards[dashboard_id]


# ──────────────────────────────────────────────
# Incident Manager
# ──────────────────────────────────────────────

class IncidentManager:
    """Create, manage, and resolve incidents."""

    def __init__(self) -> None:
        self._incidents: Dict[str, Incident] = {}

    def create_incident(
        self,
        title: str,
        severity: IncidentSeverity,
        description: str = "",
        affected_services: Optional[List[str]] = None,
        related_alerts: Optional[List[str]] = None,
    ) -> Incident:
        incident = Incident(
            title=title,
            severity=severity,
            description=description,
            affected_services=affected_services or [],
            related_alerts=related_alerts or [],
        )
        incident.timeline.append({
            "event": "created",
            "timestamp": datetime.now().isoformat(),
            "description": f"Incident created: {title}",
        })
        self._incidents[incident.incident_id] = incident
        logger.warning("Incident created: %s (%s)", title, severity.value)
        return incident

    def update_status(self, incident_id: str, status: IncidentStatus, note: str = "") -> Incident:
        incident = self._get_incident(incident_id)
        incident.status = status
        incident.timeline.append({
            "event": "status_change",
            "new_status": status.value,
            "timestamp": datetime.now().isoformat(),
            "note": note,
        })
        return incident

    def resolve_incident(self, incident_id: str, resolution: str = "") -> Incident:
        incident = self._get_incident(incident_id)
        incident.status = IncidentStatus.RESOLVED
        incident.resolved_at = datetime.now()
        incident.timeline.append({
            "event": "resolved",
            "timestamp": datetime.now().isoformat(),
            "resolution": resolution,
        })
        return incident

    def get_mttr(self, incident_id: str) -> Optional[float]:
        incident = self._get_incident(incident_id)
        if incident.resolved_at:
            delta = incident.resolved_at - incident.created_at
            return round(delta.total_seconds() / 60, 2)
        return None

    def get_incident(self, incident_id: str) -> Incident:
        return self._get_incident(incident_id)

    def list_incidents(self, status: Optional[IncidentStatus] = None) -> List[Incident]:
        incidents = list(self._incidents.values())
        if status:
            incidents = [i for i in incidents if i.status == status]
        return incidents

    def _get_incident(self, incident_id: str) -> Incident:
        if incident_id not in self._incidents:
            raise IncidentNotFoundError(f"Incident {incident_id} not found")
        return self._incidents[incident_id]


# ──────────────────────────────────────────────
# SLO Manager
# ──────────────────────────────────────────────

class SLOManager:
    """Track Service Level Objectives and error budgets."""

    def __init__(self) -> None:
        self._slos: Dict[str, SLO] = {}

    def create_slo(self, service: str, metric: str, target: float, window_days: int = 30) -> SLO:
        slo = SLO(service=service, metric=metric, target=target, window_days=window_days)
        self._slos[slo.slo_id] = slo
        return slo

    def update_slo(self, slo_id: str, current_value: float) -> SLO:
        slo = self._get_slo(slo_id)
        slo.current_value = current_value
        error_budget = 100 - slo.target
        consumed = max(0, slo.target - current_value)
        slo.error_budget_remaining = round(max(0, error_budget - consumed) / error_budget * 100, 2) if error_budget > 0 else 100.0
        return slo

    def get_burn_rate(self, slo_id: str) -> float:
        slo = self._get_slo(slo_id)
        error_budget = 100 - slo.target
        if error_budget <= 0:
            return 0.0
        consumed_rate = (slo.target - slo.current_value) / error_budget * 100
        return round(consumed_rate / slo.window_days, 4) if slo.window_days > 0 else 0.0

    def get_slo(self, slo_id: str) -> SLO:
        return self._get_slo(slo_id)

    def list_slos(self) -> List[SLO]:
        return list(self._slos.values())

    def _get_slo(self, slo_id: str) -> SLO:
        if slo_id not in self._slos:
            raise MonitoringError(f"SLO {slo_id} not found")
        return self._slos[slo_id]


# ──────────────────────────────────────────────
# Monitoring Agent (orchestrator)
# ──────────────────────────────────────────────

class MonitoringAgent:
    """Top-level orchestrator for all monitoring operations."""

    def __init__(self) -> None:
        self.metrics = PrometheusMetrics()
        self.alerts = AlertManager()
        self.uptime = UptimeMonitor()
        self.logs = LogMonitor()
        self.dashboards = DashboardGenerator()
        self.incidents = IncidentManager()
        self.slos = SLOManager()
        logger.info("MonitoringAgent initialized")

    def setup_full_monitoring(
        self,
        service_name: str,
        endpoints: List[Dict[str, str]],
        alert_rules: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        results: Dict[str, Any] = {"service": service_name, "endpoints": [], "rules": []}
        for ep in endpoints:
            check = self.uptime.add_check(
                name=ep.get("name", service_name),
                url=ep["url"],
                method=ep.get("method", "GET"),
            )
            results["endpoints"].append(check.check_id)
        for rule in alert_rules:
            alert_rule = self.alerts.add_rule(
                name=rule["name"],
                expression=rule.get("expression", ""),
                severity=AlertSeverity(rule.get("severity", "medium")),
            )
            results["rules"].append(alert_rule.rule_id)
        dashboard = self.dashboards.create_dashboard(f"{service_name} Overview")
        self.dashboards.add_panel(dashboard.dashboard_id, "Request Rate", DashboardPanelType.GRAPH, [f"{service_name}_requests_total"])
        self.dashboards.add_panel(dashboard.dashboard_id, "Error Rate", DashboardPanelType.GRAPH, [f"{service_name}_errors_total"])
        self.dashboards.add_panel(dashboard.dashboard_id, "Latency", DashboardPanelType.GRAPH, [f"{service_name}_latency_seconds"])
        results["dashboard_id"] = dashboard.dashboard_id
        return results


# ──────────────────────────────────────────────
# CLI entry point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    agent = MonitoringAgent()

    agent.metrics.define_counter("http_requests_total", "Total HTTP requests")
    agent.metrics.define_gauge("active_connections", "Current connections")
    agent.metrics.define_histogram("http_request_duration_seconds", "Request latency")
    agent.metrics.inc_counter("http_requests_total", labels={"method": "GET", "status": "200"})
    agent.metrics.set_gauge("active_connections", 42)
    agent.metrics.observe_histogram("http_request_duration_seconds", 0.25)
    print(f"Metrics: {agent.metrics.scrape()}")

    rule = agent.alerts.add_rule("HighErrorRate", "rate(errors[5m]) > 0.05", AlertSeverity.HIGH)
    alert = agent.alerts.fire_alert(rule.rule_id, "Error rate exceeded 5%")
    print(f"Active alerts: {len(agent.alerts.get_active_alerts())}")

    check = agent.uptime.add_check("API", "https://api.example.com/health")
    agent.uptime.record_check(check.check_id, 200, 45, True)
    uptime = agent.uptime.get_uptime(check.check_id)
    print(f"Uptime: {uptime['uptime_percent']}%")

    agent.logs.add_pattern("DBError", r"Database.*error", AlertSeverity.HIGH)
    agent.logs.ingest("ERROR: Database connection timeout", source="api", level=LogLevel.ERROR)
    errors = agent.logs.get_error_summary()
    print(f"Errors: {errors['total_errors']}")

    dashboard = agent.dashboards.create_dashboard("Production Overview")
    agent.dashboards.add_panel(dashboard.dashboard_id, "Requests", DashboardPanelType.GRAPH, ["http_requests_total"])
    exported = agent.dashboards.export_json(dashboard.dashboard_id)
    print(f"Dashboard panels: {len(exported['panels'])}")

    incident = agent.incidents.create_incident("Database Outage", IncidentSeverity.SEV1, "Primary DB unreachable", ["database"], [alert.alert_id])
    agent.incidents.update_status(incident.incident_id, IncidentStatus.INVESTIGATING, "Looking into connection pool")
    agent.incidents.resolve_incident(incident.incident_id, "Connection pool resized")
    mttr = agent.incidents.get_mttr(incident.incident_id)
    print(f"MTTR: {mttr} minutes")

    slo = agent.slos.create_slo("api", "availability", 99.9, 30)
    agent.slos.update_slo(slo.slo_id, 99.95)
    burn = agent.slos.get_burn_rate(slo.slo_id)
    print(f"SLO burn rate: {burn}")
