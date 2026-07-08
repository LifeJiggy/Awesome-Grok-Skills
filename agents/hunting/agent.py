"""
Hunting Agent — Threat hunting, IOC analysis, hypothesis-driven hunting,
log analysis, network forensics, and APT detection.
"""

from __future__ import annotations
import hashlib
import logging
import re
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

class IOCType(Enum):
    IP_ADDRESS = "ip_address"
    DOMAIN = "domain"
    URL = "url"
    FILE_HASH_MD5 = "file_hash_md5"
    FILE_HASH_SHA1 = "file_hash_sha1"
    FILE_HASH_SHA256 = "file_hash_sha256"
    EMAIL = "email"
    MUTEX = "mutex"
    REGISTRY_KEY = "registry_key"
    FILE_PATH = "file_path"
    USER_AGENT = "user_agent"
    CVE = "cve"
    JA3_HASH = "ja3_hash"
    CIDR_BLOCK = "cidr_block"

class ThreatLevel(Enum):
    UNKNOWN = "unknown"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IOCStatus(Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    FALSE_POSITIVE = "false_positive"
    UNDER_REVIEW = "under_review"
    ARCHIVED = "archived"

class HuntPhase(Enum):
    PLANNING = "planning"
    DATA_COLLECTION = "data_collection"
    ANALYSIS = "analysis"
    INVESTIGATION = "investigation"
    REMEDIATION = "remediation"
    REPORTING = "reporting"

class LogSource(Enum):
    FIREWALL = "firewall"
    IDS_IPS = "ids_ips"
    PROXY = "proxy"
    DNS = "dns"
    ENDPOINT = "endpoint"
    EMAIL = "email"
    AUTH = "auth"
    CLOUD = "cloud"
    APPLICATION = "application"
    DATABASE = "database"

class AnomalyType(Enum):
    VOLUME_SPIKE = "volume_spike"
    NEW_CONNECTION = "new_connection"
    UNUSUAL_TIME = "unusual_time"
    UNUSUAL_PROTOCOL = "unusual_protocol"
    DATA_EXFIL = "data_exfil"
    LATERAL_MOVEMENT = "lateral_movement"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    C2_COMMUNICATION = "c2_communication"
    BRUTE_FORCE = "brute_force"
    DNS_TUNNEL = "dns_tunnel"

class Severity(IntEnum):
    INFO = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class HuntStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

class DetectionStatus(Enum):
    DRAFT = "draft"
    TESTED = "tested"
    DEPLOYED = "deployed"
    TUNING = "tuning"
    RETIRED = "retired"

class AlertStatus(Enum):
    NEW = "new"
    INVESTIGATING = "investigating"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"

class NetworkDirection(Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"
    LATERAL = "lateral"
    INTERNAL = "internal"

class MITRETactic(Enum):
    RECONNAISSANCE = "reconnaissance"
    INITIAL_ACCESS = "initial_access"
    EXECUTION = "execution"
    PERSISTENCE = "persistence"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    DEFENSE_EVASION = "defense_evasion"
    CREDENTIAL_ACCESS = "credential_access"
    DISCOVERY = "discovery"
    LATERAL_MOVEMENT = "lateral_movement"
    COLLECTION = "collection"
    COMMAND_AND_CONTROL = "command_and_control"
    EXFILTRATION = "exfiltration"
    IMPACT = "impact"

# Data Classes

@dataclass
class IOC:
    ioc_id: str
    value: str
    ioc_type: IOCType
    threat_level: ThreatLevel = ThreatLevel.UNKNOWN
    status: IOCStatus = IOCStatus.ACTIVE
    confidence: float = 0.0
    source: str = ""
    tags: List[str] = field(default_factory=list)
    description: str = ""
    first_seen: datetime = field(default_factory=datetime.utcnow)
    last_seen: datetime = field(default_factory=datetime.utcnow)
    expiry: Optional[datetime] = None
    mitre_techniques: List[str] = field(default_factory=list)
    false_positive_count: int = 0

    @property
    def is_expired(self) -> bool:
        return self.expiry is not None and datetime.utcnow() > self.expiry

    @property
    def days_active(self) -> int:
        return (datetime.utcnow() - self.first_seen).days

    def to_dict(self) -> Dict[str, Any]:
        return {"ioc_id": self.ioc_id, "value": self.value, "type": self.ioc_type.value,
                "threat_level": self.threat_level.value, "confidence": self.confidence}

@dataclass
class ThreatHunt:
    hunt_id: str
    title: str
    hypothesis: str
    description: str = ""
    phase: HuntPhase = HuntPhase.PLANNING
    status: HuntStatus = HuntStatus.NOT_STARTED
    analyst: str = ""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    mitre_tactic: Optional[MITRETactic] = None
    data_sources: List[LogSource] = field(default_factory=list)
    queries: List[str] = field(default_factory=list)
    iocs_found: List[str] = field(default_factory=list)
    findings: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    is_confirmed_threat: bool = False

    @property
    def duration_days(self) -> Optional[int]:
        if not self.start_date:
            return None
        return (self.end_date or datetime.utcnow() - self.start_date).days

@dataclass
class LogEntry:
    timestamp: datetime
    source: LogSource
    source_ip: str = ""
    destination_ip: str = ""
    source_port: int = 0
    destination_port: int = 0
    protocol: str = ""
    action: str = ""
    bytes_sent: int = 0
    bytes_received: int = 0
    user_agent: str = ""
    url: str = ""
    domain: str = ""
    query: str = ""
    response_code: int = 0
    process_name: str = ""
    user: str = ""
    anomalies: List[AnomalyType] = field(default_factory=list)

    @property
    def is_suspicious_port(self) -> bool:
        return self.destination_port in {4444, 5555, 6666, 7777, 8888, 9999, 1234, 31337, 1337}

@dataclass
class NetworkFlow:
    flow_id: str
    timestamp: datetime
    source_ip: str
    destination_ip: str
    source_port: int
    destination_port: int
    protocol: str
    bytes_sent: int = 0
    bytes_received: int = 0
    duration_seconds: float = 0.0
    direction: NetworkDirection = NetworkDirection.OUTBOUND
    is_encrypted: bool = False
    ja3_hash: str = ""
    anomalies: List[AnomalyType] = field(default_factory=list)

    @property
    def total_bytes(self) -> int:
        return self.bytes_sent + self.bytes_received

@dataclass
class SigmaRule:
    rule_id: str
    title: str
    description: str = ""
    status: DetectionStatus = DetectionStatus.DRAFT
    severity: Severity = Severity.MEDIUM
    author: str = ""
    logsource: str = ""
    detection_logic: str = ""
    references: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    matches: int = 0
    last_match: Optional[datetime] = None

@dataclass
class Alert:
    alert_id: str
    title: str
    description: str = ""
    severity: Severity = Severity.MEDIUM
    status: AlertStatus = AlertStatus.NEW
    source: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    source_ip: str = ""
    destination_ip: str = ""
    iocs: List[str] = field(default_factory=list)
    mitre_techniques: List[str] = field(default_factory=list)
    analyst_notes: str = ""
    assigned_to: str = ""
    resolved_at: Optional[datetime] = None

    @property
    def is_open(self) -> bool:
        return self.status in (AlertStatus.NEW, AlertStatus.INVESTIGATING, AlertStatus.ESCALATED)

    @property
    def age_hours(self) -> float:
        return (datetime.utcnow() - self.timestamp).total_seconds() / 3600

@dataclass
class ThreatActor:
    actor_id: str
    name: str
    aliases: List[str] = field(default_factory=list)
    motivation: str = ""
    sophistication: str = ""
    target_sectors: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    techniques: List[str] = field(default_factory=list)
    iocs: List[str] = field(default_factory=list)
    first_observed: Optional[datetime] = None
    last_observed: Optional[datetime] = None
    description: str = ""

    @property
    def is_active(self) -> bool:
        if not self.last_observed:
            return True
        return (datetime.utcnow() - self.last_observed).days < 90

@dataclass
class HuntReport:
    report_id: str
    hunt_id: str
    title: str
    executive_summary: str = ""
    findings: List[Dict[str, Any]] = field(default_factory=list)
    iocs: List[str] = field(default_factory=list)
    mitre_mapping: Dict[str, List[str]] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

# IOC Manager

class IOCManager:
    def __init__(self) -> None:
        self.iocs: Dict[str, IOC] = {}
        self._counter = 0

    def add_ioc(self, value: str, ioc_type: IOCType, threat_level: ThreatLevel = ThreatLevel.UNKNOWN,
                confidence: float = 0.0, source: str = "", tags: List[str] = None) -> IOC:
        self._counter += 1
        ioc = IOC(ioc_id=f"IOC-{self._counter:05d}", value=value, ioc_type=ioc_type,
                  threat_level=threat_level, confidence=confidence, source=source, tags=tags or [])
        self.iocs[ioc.ioc_id] = ioc
        return ioc

    def search(self, query: str) -> List[IOC]:
        q = query.lower()
        return [i for i in self.iocs.values() if q in i.value.lower() or q in " ".join(i.tags).lower()]

    def get_by_type(self, ioc_type: IOCType) -> List[IOC]:
        return [i for i in self.iocs.values() if i.ioc_type == ioc_type]

    def get_active(self) -> List[IOC]:
        return [i for i in self.iocs.values() if i.status == IOCStatus.ACTIVE and not i.is_expired]

    def get_high_threat(self) -> List[IOC]:
        return [i for i in self.iocs.values() if i.threat_level in (ThreatLevel.HIGH, ThreatLevel.CRITICAL)]

    def mark_false_positive(self, ioc_id: str) -> bool:
        if ioc_id not in self.iocs:
            return False
        self.iocs[ioc_id].status = IOCStatus.FALSE_POSITIVE
        self.iocs[ioc_id].false_positive_count += 1
        return True

    def export_stix(self, ioc_ids: List[str] = None) -> List[Dict[str, Any]]:
        to_export = [self.iocs[iid] for iid in (ioc_ids or self.iocs.keys()) if iid in self.iocs]
        return [{"type": "indicator", "spec_version": "2.1", "id": f"indicator--{i.ioc_id}",
                 "pattern": f"[{i.ioc_type.value}:value = '{i.value}']",
                 "valid_from": i.first_seen.isoformat(), "confidence": i.confidence} for i in to_export]

    def stats(self) -> Dict[str, Any]:
        by_type = defaultdict(int)
        by_level = defaultdict(int)
        for ioc in self.iocs.values():
            by_type[ioc.ioc_type.value] += 1
            by_level[ioc.threat_level.value] += 1
        return {"total": len(self.iocs), "active": len(self.get_active()),
                "by_type": dict(by_type), "by_level": dict(by_level)}

# Log Analyzer

class LogAnalyzer:
    def __init__(self) -> None:
        self.logs: List[LogEntry] = []
        self.baselines: Dict[str, Any] = {}

    def add_log(self, entry: LogEntry) -> None:
        self.logs.append(entry)

    def detect_anomalies(self) -> List[LogEntry]:
        flagged = []
        for log in self.logs:
            anomalies = []
            if log.is_suspicious_port:
                anomalies.append(AnomalyType.C2_COMMUNICATION)
            if log.bytes_sent > 10_000_000:
                anomalies.append(AnomalyType.DATA_EXFIL)
            if log.destination_port == 53 and len(log.query) > 50:
                anomalies.append(AnomalyType.DNS_TUNNEL)
            if log.timestamp.hour < 5 or log.timestamp.hour > 23:
                anomalies.append(AnomalyType.UNUSUAL_TIME)
            if anomalies:
                log.anomalies = anomalies
                flagged.append(log)
        return flagged

    def get_connections_by_ip(self, ip: str) -> List[LogEntry]:
        return [l for l in self.logs if l.source_ip == ip or l.destination_ip == ip]

    def get_volume_by_domain(self) -> Dict[str, int]:
        vol: Dict[str, int] = defaultdict(int)
        for log in self.logs:
            if log.domain:
                vol[log.domain] += log.bytes_sent
        return dict(sorted(vol.items(), key=lambda x: x[1], reverse=True))

    def get_unique_sources(self) -> List[str]:
        return list(set(l.source_ip for l in self.logs if l.source_ip))

    def summary(self) -> Dict[str, Any]:
        total = len(self.logs)
        flagged = sum(1 for l in self.logs if l.anomalies)
        return {"total_entries": total, "flagged": flagged, "unique_sources": len(self.get_unique_sources()),
                "unique_domains": len(set(l.domain for l in self.logs if l.domain))}

# Network Analyzer

class NetworkAnalyzer:
    def __init__(self) -> None:
        self.flows: List[NetworkFlow] = []

    def add_flow(self, flow: NetworkFlow) -> None:
        self.flows.append(flow)

    def detect_anomalies(self) -> List[NetworkFlow]:
        flagged = []
        for flow in self.flows:
            anomalies = []
            if flow.bytes_per_second > 1_000_000:
                anomalies.append(AnomalyType.DATA_EXFIL)
            if flow.destination_port in {4444, 5555, 6666}:
                anomalies.append(AnomalyType.C2_COMMUNICATION)
            if flow.direction == NetworkDirection.LATERAL:
                anomalies.append(AnomalyType.LATERAL_MOVEMENT)
            if anomalies:
                flow.anomalies = anomalies
                flagged.append(flow)
        return flagged

    def get_top_talkers(self, n: int = 10) -> List[Tuple[str, int]]:
        vol: Dict[str, int] = defaultdict(int)
        for f in self.flows:
            vol[f.source_ip] += f.total_bytes
        return sorted(vol.items(), key=lambda x: x[1], reverse=True)[:n]

    def get_external_connections(self) -> List[NetworkFlow]:
        return [f for f in self.flows if f.direction == NetworkDirection.OUTBOUND]

    def get_ja3_duplicates(self) -> Dict[str, List[str]]:
        ja3_map: Dict[str, List[str]] = defaultdict(list)
        for f in self.flows:
            if f.ja3_hash:
                ja3_map[f.ja3_hash].append(f.source_ip)
        return {k: v for k, v in ja3_map.items() if len(set(v)) > 1}

    def stats(self) -> Dict[str, Any]:
        total_bytes = sum(f.total_bytes for f in self.flows)
        encrypted = sum(1 for f in self.flows if f.is_encrypted)
        return {"total_flows": len(self.flows), "total_bytes": total_bytes,
                "encrypted_pct": encrypted / len(self.flows) * 100 if self.flows else 0,
                "unique_sources": len(set(f.source_ip for f in self.flows))}

# Detection Engine

class DetectionEngine:
    def __init__(self) -> None:
        self.rules: Dict[str, SigmaRule] = {}
        self._counter = 0

    def add_rule(self, title: str, logsource: str, detection_logic: str,
                 severity: Severity = Severity.MEDIUM, **kwargs: Any) -> SigmaRule:
        self._counter += 1
        rule = SigmaRule(rule_id=f"SIGMA-{self._counter:04d}", title=title,
                         logsource=logsource, detection_logic=detection_logic, severity=severity, **kwargs)
        self.rules[rule.rule_id] = rule
        return rule

    def match_logs(self, rule_id: str, logs: List[LogEntry]) -> List[LogEntry]:
        if rule_id not in self.rules:
            return []
        rule = self.rules[rule_id]
        matches = []
        for log in logs:
            if self._evaluate_rule(rule, log):
                matches.append(log)
                rule.matches += 1
                rule.last_match = datetime.utcnow()
        return matches

    def _evaluate_rule(self, rule: SigmaRule, log: LogEntry) -> bool:
        logic = rule.detection_logic.lower()
        if "source_ip" in logic:
            return bool(log.source_ip)
        if "suspicious_port" in logic:
            return log.is_suspicious_port
        if "high_bytes" in logic:
            return log.bytes_sent > 5_000_000
        if "dns_tunnel" in logic:
            return log.destination_port == 53 and len(log.query) > 50
        return False

    def get_deployed_rules(self) -> List[SigmaRule]:
        return [r for r in self.rules.values() if r.status == DetectionStatus.DPLOYED]

    def rules_stats(self) -> Dict[str, Any]:
        by_status = defaultdict(int)
        for r in self.rules.values():
            by_status[r.status.value] += 1
        return {"total": len(self.rules), "by_status": dict(by_status),
                "total_matches": sum(r.matches for r in self.rules.values())}

# Hunt Orchestrator

class HuntOrchestrator:
    def __init__(self) -> None:
        self.hunts: Dict[str, ThreatHunt] = {}
        self.reports: Dict[str, HuntReport] = {}
        self._counter = 0

    def create_hunt(self, title: str, hypothesis: str, analyst: str = "",
                    tactic: MITRETactic = None, sources: List[LogSource] = None) -> ThreatHunt:
        self._counter += 1
        hunt = ThreatHunt(hunt_id=f"HUNT-{self._counter:04d}", title=title,
                          hypothesis=hypothesis, analyst=analyst,
                          mitre_tactic=tactic, data_sources=sources or [])
        self.hunts[hunt.hunt_id] = hunt
        return hunt

    def start_hunt(self, hunt_id: str) -> bool:
        if hunt_id not in self.hunts:
            return False
        self.hunts[hunt_id].status = HuntStatus.IN_PROGRESS
        self.hunts[hunt_id].phase = HuntPhase.DATA_COLLECTION
        self.hunts[hunt_id].start_date = datetime.utcnow()
        return True

    def complete_hunt(self, hunt_id: str, findings: List[Dict[str, Any]], confirmed: bool = False) -> bool:
        if hunt_id not in self.hunts:
            return False
        hunt = self.hunts[hunt_id]
        hunt.status = HuntStatus.COMPLETED
        hunt.phase = HuntPhase.REPORTING
        hunt.end_date = datetime.utcnow()
        hunt.findings = findings
        hunt.is_confirmed_threat = confirmed
        return True

    def generate_report(self, hunt_id: str) -> Optional[HuntReport]:
        if hunt_id not in self.hunts:
            return None
        hunt = self.hunts[hunt_id]
        self._counter += 1
        report = HuntReport(report_id=f"RPT-{self._counter:04d}", hunt_id=hunt_id,
                            title=f"Report: {hunt.title}", executive_summary=hunt.hypothesis,
                            findings=hunt.findings, iocs=hunt.iocs_found,
                            recommendations=hunt.recommendations)
        self.reports[report.report_id] = report
        return report

    def get_active_hunts(self) -> List[ThreatHunt]:
        return [h for h in self.hunts.values() if h.status == HuntStatus.IN_PROGRESS]

    def hunt_stats(self) -> Dict[str, Any]:
        by_status = defaultdict(int)
        for h in self.hunts.values():
            by_status[h.status.value] += 1
        confirmed = sum(1 for h in self.hunts.values() if h.is_confirmed_threat)
        return {"total": len(self.hunts), "by_status": dict(by_status), "confirmed_threats": confirmed}

# Alert Manager

class AlertManager:
    def __init__(self) -> None:
        self.alerts: Dict[str, Alert] = {}
        self._counter = 0

    def create_alert(self, title: str, severity: Severity = Severity.MEDIUM, **kwargs: Any) -> Alert:
        self._counter += 1
        alert = Alert(alert_id=f"ALR-{self._counter:05d}", title=title, severity=severity, **kwargs)
        self.alerts[alert.alert_id] = alert
        return alert

    def assign(self, alert_id: str, analyst: str) -> bool:
        if alert_id not in self.alerts:
            return False
        self.alerts[alert_id].assigned_to = analyst
        self.alerts[alert_id].status = AlertStatus.INVESTIGATING
        return True

    def resolve(self, alert_id: str, notes: str = "", false_positive: bool = False) -> bool:
        if alert_id not in self.alerts:
            return False
        alert = self.alerts[alert_id]
        alert.status = AlertStatus.FALSE_POSITIVE if false_positive else AlertStatus.RESOLVED
        alert.analyst_notes = notes
        alert.resolved_at = datetime.utcnow()
        return True

    def get_open_alerts(self) -> List[Alert]:
        return [a for a in self.alerts.values() if a.is_open]

    def get_critical_alerts(self) -> List[Alert]:
        return [a for a in self.alerts.values() if a.severity == Severity.CRITICAL and a.is_open]

    def stats(self) -> Dict[str, Any]:
        by_status = defaultdict(int)
        by_severity = defaultdict(int)
        for a in self.alerts.values():
            by_status[a.status.value] += 1
            by_severity[a.severity.name] += 1
        return {"total": len(self.alerts), "open": len(self.get_open_alerts()),
                "by_status": dict(by_status), "by_severity": dict(by_severity)}

# Threat Intel Correlator

class ThreatIntelCorrelator:
    def __init__(self) -> None:
        self.actors: Dict[str, ThreatActor] = {}

    def add_actor(self, name: str, **kwargs: Any) -> ThreatActor:
        actor_id = f"TA-{len(self.actors) + 1:04d}"
        actor = ThreatActor(actor_id=actor_id, name=name, **kwargs)
        self.actors[actor_id] = actor
        return actor

    def correlate_iocs(self, iocs: List[str]) -> List[ThreatActor]:
        matches = []
        for actor in self.actors.values():
            overlap = set(iocs) & set(actor.iocs)
            if overlap:
                matches.append(actor)
        return matches

    def get_active_actors(self) -> List[ThreatActor]:
        return [a for a in self.actors.values() if a.is_active]

    def get_by_sophistication(self, level: str) -> List[ThreatActor]:
        return [a for a in self.actors.values() if a.sophistication == level]

# Main demo

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("=" * 60)
    print("Hunting Agent - Comprehensive Demo")
    print("=" * 60)

    # IOC Management
    ioc_mgr = IOCManager()
    ioc_mgr.add_ioc("198.51.100.23", IOCType.IP_ADDRESS, ThreatLevel.HIGH, 85, "osint", ["apt28"])
    ioc_mgr.add_ioc("evil-domain.com", IOCType.DOMAIN, ThreatLevel.CRITICAL, 95, "internal", ["c2"])
    ioc_mgr.add_ioc("d41d8cd98f00b204e9800998ecf8427e", IOCType.FILE_HASH_MD5, ThreatLevel.HIGH, 90, "sandbox")
    print(f"\nIOCs: {ioc_mgr.stats()}")

    # Log Analysis
    log_analyzer = LogAnalyzer()
    now = datetime.utcnow()
    log_analyzer.add_log(LogEntry(now, LogSource.FIREWALL, "10.0.0.5", "198.51.100.23", 49321, 4444, "TCP", "allow", 5000000))
    log_analyzer.add_log(LogEntry(now, LogSource.DNS, "10.0.0.5", "8.8.8.8", 0, 53, "UDP", "query", 0, query="a" * 100))
    log_analyzer.add_log(LogEntry(now, LogSource.PROXY, "10.0.0.10", "104.21.1.1", 44382, 80, "HTTP", "allow", 15000000))
    flagged = log_analyzer.detect_anomalies()
    print(f"\nLog Analysis: {log_analyzer.summary()}, Flagged: {len(flagged)}")

    # Network Analysis
    net = NetworkAnalyzer()
    net.add_flow(NetworkFlow("F1", now, "10.0.0.5", "198.51.100.23", 49321, 4444, "TCP", 100000, 50000, 60, NetworkDirection.OUTBOUND, True, "abc123"))
    net.add_flow(NetworkFlow("F2", now, "10.0.0.5", "10.0.0.10", 445, 445, "SMB", 5000, 2000, 5, NetworkDirection.LATERAL))
    net_flagged = net.detect_anomalies()
    print(f"\nNetwork: {net.stats()}, Flagged flows: {len(net_flagged)}")

    # Detection Rules
    detection = DetectionEngine()
    detection.add_rule("Suspicious Outbound Connection", "firewall", "suspicious_port", Severity.HIGH)
    detection.add_rule("DNS Tunneling", "dns", "dns_tunnel", Severity.HIGH)
    detection.add_rule("Large Data Transfer", "proxy", "high_bytes", Severity.MEDIUM)
    matches = detection.match_logs("SIGMA-0001", log_analyzer.logs)
    print(f"\nDetection: {detection.rules_stats()}, Matches on rule 1: {len(matches)}")

    # Threat Hunt
    orchestrator = HuntOrchestrator()
    hunt = orchestrator.create_hunt("APT Lateral Movement", "Adversary moving laterally via SMB", "analyst1", MITRETactic.LATERAL_MOVEMENT)
    orchestrator.start_hunt(hunt.hunt_id)
    orchestrator.complete_hunt(hunt.hunt_id, [{"finding": "SMB connections between workstations", "severity": "high"}], confirmed=True)
    print(f"\nHunts: {orchestrator.hunt_stats()}")

    # Alerts
    alerts = AlertManager()
    alerts.create_alert("C2 Communication Detected", Severity.CRITICAL, source_ip="10.0.0.5", destination_ip="198.51.100.23")
    alerts.create_alert("DNS Tunnel Attempt", Severity.HIGH, source_ip="10.0.0.5")
    alerts.assign("ALR-00001", "analyst1")
    print(f"\nAlerts: {alerts.stats()}")

    # Threat Intel
    ti = ThreatIntelCorrelator()
    ti.add_actor("APT28", aliases=["Fancy Bear"], sophistication="advanced",
                 techniques=["T1566", "T1059", "T1071"], iocs=["198.51.100.23", "evil-domain.com"])
    matches = ti.correlate_iocs(["198.51.100.23", "evil-domain.com"])
    print(f"\nThreat Intel: {len(matches)} actor matches")
    for actor in matches:
        print(f"  Matched: {actor.name} ({actor.sophistication})")

    print("\n" + "=" * 60)
    print("Hunting Agent demo complete.")
    print("=" * 60)
