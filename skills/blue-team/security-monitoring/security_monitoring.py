"""
Security Monitoring Module
Log parsing, correlation rules, alert management, dashboards, and SIEM integration.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import secrets
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Pattern, Set, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class AlertStatus(Enum):
    NEW = "new"
    TRIAGED = "triaged"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"
    ESCALATED = "escalated"


class LogSourceType(Enum):
    SYSLOG = "syslog"
    WINDOWS_EVENT = "windows_event"
    CLOUD_TRAIL = "cloudtrail"
    FIREWALL = "firewall"
    WEB_ACCESS = "web_access"
    DNS = "dns"
    APPLICATION = "application"
    AUTH = "auth"


class SIEMPlatform(Enum):
    SPLUNK = "splunk"
    ELASTIC = "elastic"
    SENTINEL = "sentinel"
    QRADAR = "qradar"
    CHRONICLE = "chronicle"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class ParsedLog:
    """Parsed log entry."""
    timestamp: datetime
    host: str
    service: str
    message: str
    source_type: LogSourceType = LogSourceType.APPLICATION
    raw: str = ""
    severity: Severity = Severity.INFORMATIONAL
    extracted_fields: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

    @property
    def age_seconds(self) -> float:
        return (datetime.now(timezone.utc) - self.timestamp).total_seconds()


@dataclass
class Alert:
    """Security alert."""
    alert_id: str
    rule_name: str
    severity: Severity
    status: AlertStatus
    source_ip: str = ""
    destination_ip: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    details: Dict[str, Any] = field(default_factory=dict)
    enriched: bool = False
    assigned_to: str = ""
    resolution_notes: str = ""
    mitre_techniques: List[str] = field(default_factory=list)

    @property
    def age_minutes(self) -> float:
        return (datetime.now(timezone.utc) - self.timestamp).total_seconds() / 60

    @property
    def is_escalated(self) -> bool:
        return self.status == AlertStatus.ESCALATED or self.severity == Severity.CRITICAL


@dataclass
class SigmaRule:
    """Sigma detection rule."""
    title: str
    status: str = "experimental"
    description: str = ""
    logsource: Dict[str, str] = field(default_factory=dict)
    detection: Dict[str, Any] = field(default_factory=dict)
    level: str = "medium"
    tags: List[str] = field(default_factory=list)
    falsepositives: List[str] = field(default_factory=list)
    author: str = ""
    date: str = ""


@dataclass
class CorrelationRule:
    """Compiled correlation rule."""
    name: str
    condition: Callable[[List[ParsedLog]], bool]
    severity: Severity = Severity.MEDIUM
    window_seconds: int = 300
    threshold: int = 10
    group_by: str = ""


@dataclass
class DashboardPanel:
    """Dashboard visualization panel."""
    title: str
    type: str  # "pie_chart", "bar_chart", "line_chart", "table", "stat"
    query: str = ""
    position: int = 0
    width: int = 6
    height: int = 4


@dataclass
class ThreatIntelMatch:
    """Threat intelligence match."""
    indicator: str
    indicator_type: str
    confidence: float
    source: str
    tags: List[str] = field(default_factory=list)
    expiry: Optional[datetime] = None


@dataclass
class MonitoringMetrics:
    """Monitoring system metrics."""
    total_logs: int = 0
    logs_per_second: float = 0.0
    alerts_today: int = 0
    alerts_critical: int = 0
    mean_time_to_detect: float = 0.0
    mean_time_to_respond: float = 0.0
    false_positive_rate: float = 0.0
    coverage_pct: float = 0.0
    uptime_pct: float = 99.9


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

IP_PATTERN = re.compile(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b')
EMAIL_PATTERN = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')
HASH_PATTERN = re.compile(r'\b[a-fA-F0-9]{32,64}\b')
CVE_PATTERN = re.compile(r'CVE-\d{4}-\d{4,}')


# ---------------------------------------------------------------------------
# Log Parser
# ---------------------------------------------------------------------------

class LogParser:
    """Parse and normalize log entries from various sources."""

    def parse_syslog(self, raw: str) -> ParsedLog:
        pattern = r'^(\w+\s+\d+\s+\d+:\d+:\d+)\s+(\S+)\s+(\S+?)(?:\[\d+\])?:\s+(.*)$'
        match = re.match(pattern, raw)
        if not match:
            return ParsedLog(
                timestamp=datetime.now(timezone.utc),
                host="unknown", service="unknown",
                message=raw, raw=raw,
            )
        ts_str, host, service, message = match.groups()
        ts = self._parse_syslog_timestamp(ts_str)
        fields = self._extract_fields(message)
        return ParsedLog(
            timestamp=ts, host=host, service=service,
            message=message, raw=raw,
            source_type=LogSourceType.SYSLOG,
            extracted_fields=fields,
            tags=self._auto_tag(message),
        )

    def parse_windows_event(self, raw: str) -> ParsedLog:
        try:
            data = json.loads(raw) if raw.startswith("{") else {}
        except json.JSONDecodeError:
            data = {}
        return ParsedLog(
            timestamp=datetime.now(timezone.utc),
            host=data.get("ComputerName", "unknown"),
            service="Windows Security",
            message=data.get("Message", raw),
            raw=raw,
            source_type=LogSourceType.WINDOWS_EVENT,
            extracted_fields={
                "event_id": data.get("EventID"),
                "channel": data.get("Channel"),
                "level": data.get("Level"),
            },
            tags=self._auto_tag(data.get("Message", "")),
        )

    def parse_cloudtrail(self, raw: str) -> ParsedLog:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            data = {"raw": raw}
        return ParsedLog(
            timestamp=self._parse_iso(data.get("eventTime", "")),
            host=data.get("eventSource", "aws"),
            service="CloudTrail",
            message=data.get("eventName", raw),
            raw=raw,
            source_type=LogSourceType.CLOUD_TRAIL,
            extracted_fields={
                "event_name": data.get("eventName"),
                "user_identity": data.get("userIdentity", {}).get("arn"),
                "source_ip": data.get("sourceIPAddress"),
            },
            tags=self._auto_tag(data.get("eventName", "")),
        )

    def parse_firewall(self, raw: str) -> ParsedLog:
        fields = self._extract_fields(raw)
        return ParsedLog(
            timestamp=datetime.now(timezone.utc),
            host=fields.get("host", "firewall"),
            service="firewall",
            message=raw,
            raw=raw,
            source_type=LogSourceType.FIREWALL,
            extracted_fields=fields,
            tags=self._auto_tag(raw),
        )

    def parse_batch(self, logs: List[str], source_type: str = "syslog") -> List[ParsedLog]:
        parsers = {
            "syslog": self.parse_syslog,
            "windows": self.parse_windows_event,
            "cloudtrail": self.parse_cloudtrail,
            "firewall": self.parse_firewall,
        }
        parser = parsers.get(source_type, self.parse_syslog)
        return [parser(line) for line in logs]

    def _extract_fields(self, message: str) -> Dict[str, Any]:
        fields: Dict[str, Any] = {}
        ips = IP_PATTERN.findall(message)
        if ips:
            fields["src_ip"] = ips[0]
            if len(ips) > 1:
                fields["dst_ip"] = ips[1]
        emails = EMAIL_PATTERN.findall(message)
        if emails:
            fields["email"] = emails[0]
        hashes = HASH_PATTERN.findall(message)
        if hashes:
            fields["hash"] = hashes[0]
        cves = CVE_PATTERN.findall(message)
        if cves:
            fields["cve"] = cves
        return fields

    def _auto_tag(self, message: str) -> List[str]:
        tags: List[str] = []
        lower = message.lower()
        if "failed" in lower or "failure" in lower:
            tags.append("failure")
        if "error" in lower or "exception" in lower:
            tags.append("error")
        if "warning" in lower or "warn" in lower:
            tags.append("warning")
        if "unauthorized" in lower or "denied" in lower:
            tags.append("unauthorized")
        if "login" in lower or "logon" in lower or "auth" in lower:
            tags.append("authentication")
        if "brute" in lower or "multiple failed" in lower:
            tags.append("brute_force")
        return tags

    def _parse_syslog_timestamp(self, ts_str: str) -> datetime:
        try:
            now = datetime.now(timezone.utc)
            dt = datetime.strptime(ts_str, "%b %d %H:%M:%S")
            return dt.replace(year=now.year, tzinfo=timezone.utc)
        except ValueError:
            return datetime.now(timezone.utc)

    def _parse_iso(self, ts_str: str) -> datetime:
        try:
            return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Correlation Engine
# ---------------------------------------------------------------------------

class CorrelationEngine:
    """Evaluate correlation rules against log streams."""

    def __init__(self):
        self._sigma_rules: List[SigmaRule] = []
        self._custom_rules: List[CorrelationRule] = []
        self._log_buffer: Dict[str, List[ParsedLog]] = defaultdict(list)

    def add_sigma_rule(self, rule_dict: Dict[str, Any]) -> None:
        rule = SigmaRule(
            title=rule_dict.get("title", "Unnamed"),
            status=rule_dict.get("status", "experimental"),
            description=rule_dict.get("description", ""),
            logsource=rule_dict.get("logsource", {}),
            detection=rule_dict.get("detection", {}),
            level=rule_dict.get("level", "medium"),
            tags=rule_dict.get("tags", []),
        )
        self._sigma_rules.append(rule)

    def add_custom_rule(self, rule: CorrelationRule) -> None:
        self._custom_rules.append(rule)

    def evaluate(self, logs: List[ParsedLog]) -> List[Alert]:
        alerts: List[Alert] = []
        for rule in self._custom_rules:
            matching = self._filter_by_rule(logs, rule)
            grouped: Dict[str, List[ParsedLog]] = defaultdict(list)
            for log in matching:
                key = getattr(log, rule.group_by, "default") if rule.group_by else "default"
                grouped[str(key)].append(log)
            for group_key, group_logs in grouped.items():
                window = rule.window_seconds
                recent = [l for l in group_logs if l.age_seconds <= window]
                if len(recent) >= rule.threshold:
                    alerts.append(Alert(
                        alert_id=f"alert_{secrets.token_hex(8)}",
                        rule_name=rule.name,
                        severity=rule.severity,
                        status=AlertStatus.NEW,
                        source_ip=group_key if rule.group_by == "src_ip" else "",
                        details={
                            "count": len(recent),
                            "window": window,
                            "group": group_key,
                        },
                    ))
        return alerts

    def _filter_by_rule(
        self, logs: List[ParsedLog], rule: CorrelationRule
    ) -> List[ParsedLog]:
        return [l for l in logs if rule.name.lower() in l.message.lower()]

    def generate_spl(self, sigma: SigmaRule) -> str:
        logsource = sigma.logsource.get("service", "*")
        selection = sigma.detection.get("selection", {})
        fields = list(selection.keys()) if isinstance(selection, dict) else []
        query = f'index={logsource} '
        for field_name, value in selection.items():
            query += f'{field_name}="{value}" '
        query += f'| stats count by src_ip | where count > {sigma.detection.get("condition", "10").split(">")[-1].strip()}'
        return query

    def generate_kql(self, sigma: SigmaRule) -> str:
        logsource = sigma.logsource.get("service", "*")
        return f'SecurityEvent | where EventSource contains "{logsource}" | summarize count() by Computer | where count_ > 10'


# ---------------------------------------------------------------------------
# Alert Manager
# ---------------------------------------------------------------------------

class AlertManager:
    """Manage security alert lifecycle."""

    def __init__(self):
        self._alerts: Dict[str, Alert] = {}
        self._enrichment_hooks: List[Callable[[Alert], Alert]] = []

    def create_alert(
        self,
        rule_name: str,
        severity: str,
        source_ip: str = "",
        destination_ip: str = "",
        details: Optional[Dict[str, Any]] = None,
        mitre_techniques: Optional[List[str]] = None,
    ) -> Alert:
        alert = Alert(
            alert_id=f"alert_{secrets.token_hex(8)}",
            rule_name=rule_name,
            severity=Severity(severity),
            status=AlertStatus.NEW,
            source_ip=source_ip,
            destination_ip=destination_ip,
            details=details or {},
            mitre_techniques=mitre_techniques or [],
        )
        self._alerts[alert.alert_id] = alert
        return alert

    def enrich(self, alert_id: str) -> Optional[Alert]:
        alert = self._alerts.get(alert_id)
        if not alert:
            return None
        for hook in self._enrichment_hooks:
            alert = hook(alert)
        alert.enriched = True
        return alert

    def add_enrichment_hook(self, hook: Callable[[Alert], Alert]) -> None:
        self._enrichment_hooks.append(hook)

    def triage(self, alert_id: str, notes: str = "") -> Optional[Alert]:
        alert = self._alerts.get(alert_id)
        if alert:
            alert.status = AlertStatus.TRIAGED
            alert.resolution_notes = notes
        return alert

    def escalate(self, alert_id: str) -> Optional[Alert]:
        alert = self._alerts.get(alert_id)
        if alert:
            alert.status = AlertStatus.ESCALATED
        return alert

    def resolve(self, alert_id: str, notes: str = "", is_false_positive: bool = False) -> Optional[Alert]:
        alert = self._alerts.get(alert_id)
        if alert:
            alert.status = AlertStatus.FALSE_POSITIVE if is_false_positive else AlertStatus.RESOLVED
            alert.resolution_notes = notes
        return alert

    def get_alerts(
        self,
        status: Optional[AlertStatus] = None,
        severity: Optional[Severity] = None,
        limit: int = 100,
    ) -> List[Alert]:
        alerts = list(self._alerts.values())
        if status:
            alerts = [a for a in alerts if a.status == status]
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        return sorted(alerts, key=lambda a: a.timestamp, reverse=True)[:limit]

    def get_metrics(self) -> MonitoringMetrics:
        alerts = list(self._alerts.values())
        total = len(alerts)
        crit = sum(1 for a in alerts if a.severity == Severity.CRITICAL)
        fp = sum(1 for a in alerts if a.status == AlertStatus.FALSE_POSITIVE)
        return MonitoringMetrics(
            alerts_today=total,
            alerts_critical=crit,
            false_positive_rate=fp / max(total, 1),
        )

    def deduplicate(self, window_seconds: int = 300) -> int:
        """Remove duplicate alerts within time window."""
        by_rule: Dict[str, List[Alert]] = defaultdict(list)
        for alert in self._alerts.values():
            by_rule[alert.rule_name].append(alert)
        removed = 0
        for rule_name, rule_alerts in by_rule.items():
            rule_alerts.sort(key=lambda a: a.timestamp)
            seen = set()
            for alert in rule_alerts:
                key = f"{alert.source_ip}:{alert.destination_ip}"
                if key in seen:
                    del self._alerts[alert.alert_id]
                    removed += 1
                seen.add(key)
        return removed


# ---------------------------------------------------------------------------
# Dashboard Builder
# ---------------------------------------------------------------------------

class DashboardBuilder:
    """Build security monitoring dashboards."""

    def __init__(self, title: str):
        self.title = title
        self.panels: List[DashboardPanel] = []
        self.refresh_interval_seconds: int = 30

    def add_panel(
        self,
        title: str,
        type: str = "bar_chart",
        query: str = "",
        position: Optional[int] = None,
        width: int = 6,
        height: int = 4,
    ) -> DashboardPanel:
        panel = DashboardPanel(
            title=title,
            type=type,
            query=query,
            position=position or len(self.panels),
            width=width,
            height=height,
        )
        self.panels.append(panel)
        return panel

    def to_json(self) -> str:
        return json.dumps({
            "title": self.title,
            "refresh_interval": self.refresh_interval_seconds,
            "panels": [
                {
                    "title": p.title,
                    "type": p.type,
                    "query": p.query,
                    "position": p.position,
                    "size": {"w": p.width, "h": p.height},
                }
                for p in self.panels
            ],
        }, indent=2)

    def export_grafana(self) -> Dict[str, Any]:
        return {
            "dashboard": {
                "title": self.title,
                "panels": [
                    {
                        "title": p.title,
                        "type": p.type,
                        "targets": [{"expr": p.query}],
                    }
                    for p in self.panels
                ],
            }
        }


# ---------------------------------------------------------------------------
# SIEM Connector
# ---------------------------------------------------------------------------

class SIEMConnector:
    """Connect to SIEM platforms."""

    def __init__(self, platform: str = "splunk"):
        self.platform = SIEMPlatform(platform)
        self._connected = False
        self._query_count = 0

    def connect(self, host: str, port: str = "8089", **kwargs) -> bool:
        self._connected = True
        return True

    def query(self, query: str, max_results: int = 1000) -> List[Dict[str, Any]]:
        self._query_count += 1
        return []

    def ingest(self, logs: List[Dict[str, Any]], index: str = "main") -> int:
        return len(logs)

    def get_query_language(self) -> str:
        mapping = {
            SIEMPlatform.SPLUNK: "SPL",
            SIEMPlatform.ELASTIC: "KQL/EQL",
            SIEMPlatform.SENTINEL: "KQL",
            SIEMPlatform.QRADAR: "AQL",
            SIEMPlatform.CHRONICLE: "YARA-L",
        }
        return mapping.get(self.platform, "unknown")


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Security Monitoring Demo")
    print("=" * 60)

    parser = LogParser()

    print("\n[1] Log Parsing")
    syslog = parser.parse_syslog(
        "Jul  6 12:34:56 server1 sshd[12345]: Failed password for root from 192.168.1.100 port 22 ssh2"
    )
    print(f"  Host: {syslog.host}  Service: {syslog.service}")
    print(f"  Source IP: {syslog.extracted_fields.get('src_ip')}")
    print(f"  Tags: {syslog.tags}")

    logs = parser.parse_batch([
        "Jul  6 12:34:56 server1 sshd[1]: Failed password for root from 192.168.1.100 port 22",
        "Jul  6 12:34:57 server1 sshd[2]: Failed password for root from 192.168.1.100 port 22",
        "Jul  6 12:34:58 server1 sshd[3]: Failed password for root from 192.168.1.100 port 22",
    ])
    print(f"  Parsed {len(logs)} log entries")

    print("\n[2] Alert Management")
    alert_mgr = AlertManager()
    for i in range(15):
        alert_mgr.create_alert(
            rule_name="SSH Brute Force",
            severity="high",
            source_ip="192.168.1.100",
            details={"attempts": i + 1},
        )
    alerts = alert_mgr.get_alerts(severity=Severity.HIGH)
    print(f"  High alerts: {len(alerts)}")
    metrics = alert_mgr.get_metrics()
    print(f"  Total alerts: {metrics.alerts_today}")

    print("\n[3] Correlation Rules")
    engine = CorrelationEngine()
    engine.add_custom_rule(CorrelationRule(
        name="SSH Brute Force",
        condition=lambda logs: True,
        severity=Severity.HIGH,
        window_seconds=300,
        threshold=10,
        group_by="src_ip",
    ))
    corr_alerts = engine.evaluate(logs)
    print(f"  Correlation alerts: {len(corr_alerts)}")

    print("\n[4] SIEM Integration")
    splunk = SIEMConnector(platform="splunk")
    splunk.connect("splunk.internal", "8089")
    print(f"  Platform: {splunk.platform.value}")
    print(f"  Query language: {splunk.get_query_language()}")

    print("\n[5] Dashboard")
    dash = DashboardBuilder("SOC Overview")
    dash.add_panel("Alerts by Severity", "pie_chart", "index=alerts | stats count by severity")
    dash.add_panel("Top Source IPs", "bar_chart", "index=alerts | top src_ip limit=20")
    dash.add_panel("Alert Trend", "line_chart", "index=alerts | timechart span=1h count")
    print(f"  Panels: {len(dash.panels)}")

    print("\n" + "=" * 60)
    print("  Security monitoring demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
