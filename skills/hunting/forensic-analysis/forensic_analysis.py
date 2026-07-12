"""
Forensic Analysis Module
Digital forensic analysis for incident investigation and evidence collection
"""

from __future__ import annotations

import hashlib
import json
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
import uuid

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class EvidenceType(Enum):
    DISK_IMAGE = "disk_image"
    MEMORY_DUMP = "memory_dump"
    NETWORK_CAPTURE = "network_capture"
    LOG_FILE = "log_file"
    REGISTRY_HIVE = "registry_hive"
    EMAIL_ARCHIVE = "email_archive"
    MOBILE_IMAGE = "mobile_image"
    CLOUD_SNAPSHOT = "cloud_snapshot"


class HashAlgorithm(Enum):
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    SHA512 = "sha512"


class SeverityLevel(Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CustodyAction(Enum):
    COLLECTED = "collected"
    TRANSFERRED = "transferred"
    ANALYZED = "analyzed"
    STORED = "stored"
    DISPOSED = "disposed"


class InjectionType(Enum):
    DLL_INJECTION = "dll_injection"
    CODE_INJECTION = "code_injection"
    PROCESS_HOLLOWING = "process_hollowing"
    ATOMIC_INJECTION = "atomic_injection"
    THREAD_HIJACKING = "thread_hijacking"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class HashValue:
    """Cryptographic hash value."""
    algorithm: HashAlgorithm
    value: str

    def verify(self, data: bytes) -> bool:
        computed = self._compute(data)
        return computed.lower() == self.value.lower()

    def _compute(self, data: bytes) -> str:
        if self.algorithm == HashAlgorithm.MD5:
            return hashlib.md5(data).hexdigest()
        elif self.algorithm == HashAlgorithm.SHA1:
            return hashlib.sha1(data).hexdigest()
        elif self.algorithm == HashAlgorithm.SHA256:
            return hashlib.sha256(data).hexdigest()
        elif self.algorithm == HashAlgorithm.SHA512:
            return hashlib.sha512(data).hexdigest()
        return ""


@dataclass
class CustodyEntry:
    """Single chain of custody entry."""
    action: CustodyAction
    timestamp: datetime = field(default_factory=datetime.utcnow)
    custodian: str = ""
    notes: str = ""
    location: str = ""
    verified: bool = False


@dataclass
class ChainOfCustody:
    """Complete chain of custody for an evidence item."""
    entries: List[CustodyEntry] = field(default_factory=list)

    @property
    def current_custodian(self) -> str:
        if self.entries:
            return self.entries[-1].custodian
        return "unknown"

    def add_entry(self, action: CustodyAction, custodian: str, notes: str = "", location: str = "") -> None:
        self.entries.append(CustodyEntry(
            action=action,
            custodian=custodian,
            notes=notes,
            location=location,
            verified=True,
        ))

    def to_dict(self) -> List[Dict[str, Any]]:
        return [
            {
                "action": e.action.value,
                "timestamp": e.timestamp.isoformat(),
                "custodian": e.custodian,
                "notes": e.notes,
                "verified": e.verified,
            }
            for e in self.entries
        ]


@dataclass
class EvidenceItem:
    """A piece of digital evidence."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    case_id: str = ""
    evidence_type: EvidenceType = EvidenceType.DISK_IMAGE
    description: str = ""
    source: str = ""
    destination: str = ""
    collected_at: datetime = field(default_factory=datetime.utcnow)
    collected_by: str = ""
    size_bytes: int = 0
    hashes: List[HashValue] = field(default_factory=list)
    chain_of_custody: ChainOfCustody = field(default_factory=ChainOfCustody)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def sha256_hash(self) -> Optional[str]:
        for h in self.hashes:
            if h.algorithm == HashAlgorithm.SHA256:
                return h.value
        return None

    @property
    def md5_hash(self) -> Optional[str]:
        for h in self.hashes:
            if h.algorithm == HashAlgorithm.MD5:
                return h.value
        return None

    def add_hash(self, algorithm: HashAlgorithm, value: str) -> None:
        self.hashes.append(HashValue(algorithm=algorithm, value=value))

    def verify_integrity(self, data: bytes) -> bool:
        return all(h.verify(data) for h in self.hashes)


@dataclass
class TimelineEvent:
    """Single event in an investigation timeline."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    source: str = ""
    description: str = ""
    severity: SeverityLevel = SeverityLevel.INFO
    category: str = ""
    indicators: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Timeline:
    """Investigation timeline."""
    case_id: str = ""
    events: List[TimelineEvent] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def duration(self) -> Optional[timedelta]:
        if not self.events:
            return None
        timestamps = [e.timestamp for e in self.events]
        return max(timestamps) - min(timestamps)

    def to_dict(self) -> List[Dict[str, Any]]:
        return [
            {
                "timestamp": e.timestamp.isoformat(),
                "source": e.source,
                "description": e.description,
                "severity": e.severity.value,
            }
            for e in sorted(self.events, key=lambda x: x.timestamp)
        ]


@dataclass
class ProcessInfo:
    """Process information from memory analysis."""
    name: str = ""
    pid: int = 0
    parent_name: str = ""
    parent_pid: int = 0
    path: str = ""
    command_line: str = ""
    user: str = ""
    creation_time: Optional[datetime] = None
    risk_score: int = 0
    indicators: List[str] = field(default_factory=list)
    modules: List[str] = field(default_factory=list)
    handles: int = 0
    threads: int = 0


@dataclass
class MemoryInjection:
    """Detected code injection."""
    process_name: str = ""
    pid: int = 0
    injection_type: InjectionType = InjectionType.DLL_INJECTION
    address: str = ""
    size: int = 0
    target_module: str = ""
    risk_score: int = 0


@dataclass
class MemoryAnalysisResults:
    """Results from memory dump analysis."""
    file_path: str = ""
    total_processes: int = 0
    suspicious_processes: List[ProcessInfo] = field(default_factory=list)
    network_connections: List[Dict[str, Any]] = field(default_factory=list)
    injected_code: List[MemoryInjection] = field(default_factory=list)
    registry_modifications: List[Dict[str, Any]] = field(default_factory=list)
    analysis_time_seconds: float = 0.0


@dataclass
class LogEntry:
    """Single log entry."""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    source: str = ""
    message: str = ""
    severity: SeverityLevel = SeverityLevel.INFO
    fields: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LogCorrelation:
    """Correlated log events."""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    source: str = ""
    message: str = ""
    related_events: List[LogEntry] = field(default_factory=list)
    correlation_score: float = 0.0


@dataclass
class LogSource:
    """Configuration for a log source."""
    name: str = ""
    path: str = ""
    parser: str = "auto"
    enabled: bool = True


@dataclass
class ForensicReport:
    """Comprehensive forensic investigation report."""
    case_id: str = ""
    title: str = ""
    investigator: str = ""
    executive_summary: str = ""
    timeline: Optional[Timeline] = None
    evidence_items: List[EvidenceItem] = field(default_factory=list)
    findings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Evidence Collector
# ---------------------------------------------------------------------------

class EvidenceCollector:
    """Collects and preserves digital evidence."""

    def __init__(self, investigator: str, case_id: str) -> None:
        self.investigator = investigator
        self.case_id = case_id
        self._evidence_items: List[EvidenceItem] = []

    def collect_disk_image(
        self,
        source: str,
        destination: str,
        format: str = "ewf",
        compression: bool = True,
    ) -> EvidenceItem:
        evidence = EvidenceItem(
            case_id=self.case_id,
            evidence_type=EvidenceType.DISK_IMAGE,
            description=f"Disk image from {source}",
            source=source,
            destination=destination,
            collected_by=self.investigator,
            metadata={"format": format, "compression": compression},
        )
        evidence.chain_of_custody.add_entry(
            action=CustodyAction.COLLECTED,
            custodian=self.investigator,
            notes=f"Disk image collected from {source}",
        )
        # Simulate hash computation
        evidence.add_hash(HashAlgorithm.SHA256, hashlib.sha256(source.encode()).hexdigest())
        evidence.add_hash(HashAlgorithm.MD5, hashlib.md5(source.encode()).hexdigest())
        self._evidence_items.append(evidence)
        return evidence

    def collect_memory_dump(self, target: str, output: str) -> EvidenceItem:
        evidence = EvidenceItem(
            case_id=self.case_id,
            evidence_type=EvidenceType.MEMORY_DUMP,
            description=f"Memory dump from {target}",
            source=target,
            destination=output,
            collected_by=self.investigator,
            size_bytes=4 * 1024 * 1024 * 1024,  # 4GB simulated
        )
        evidence.chain_of_custody.add_entry(
            action=CustodyAction.COLLECTED,
            custodian=self.investigator,
            notes=f"Memory dump collected from {target}",
        )
        evidence.add_hash(HashAlgorithm.SHA256, hashlib.sha256(target.encode()).hexdigest())
        self._evidence_items.append(evidence)
        return evidence

    def collect_network_capture(self, interface: str, duration_seconds: int, output: str) -> EvidenceItem:
        evidence = EvidenceItem(
            case_id=self.case_id,
            evidence_type=EvidenceType.NETWORK_CAPTURE,
            description=f"Network capture on {interface} for {duration_seconds}s",
            source=interface,
            destination=output,
            collected_by=self.investigator,
            metadata={"duration_seconds": duration_seconds},
        )
        evidence.chain_of_custody.add_entry(
            action=CustodyAction.COLLECTED,
            custodian=self.investigator,
            notes=f"Network capture on {interface}",
        )
        self._evidence_items.append(evidence)
        return evidence

    def get_all_evidence(self) -> List[EvidenceItem]:
        return self._evidence_items


# ---------------------------------------------------------------------------
# Timeline Analyzer
# ---------------------------------------------------------------------------

class TimelineAnalyzer:
    """Analyzes and correlates events into a timeline."""

    def __init__(self) -> None:
        self._events: List[TimelineEvent] = []

    def add_event(self, event: TimelineEvent) -> None:
        self._events.append(event)

    def generate_timeline(self, severity_filter: Optional[SeverityLevel] = None) -> List[TimelineEvent]:
        filtered = self._events
        if severity_filter:
            severity_order = {
                SeverityLevel.INFO: 0,
                SeverityLevel.LOW: 1,
                SeverityLevel.MEDIUM: 2,
                SeverityLevel.HIGH: 3,
                SeverityLevel.CRITICAL: 4,
            }
            min_severity = severity_order.get(severity_filter, 0)
            filtered = [e for e in filtered if severity_order.get(e.severity, 0) >= min_severity]

        return sorted(filtered, key=lambda e: e.timestamp)

    def find_gaps(self, max_gap_minutes: int = 30) -> List[Tuple[datetime, datetime]]:
        sorted_events = sorted(self._events, key=lambda e: e.timestamp)
        gaps = []
        for i in range(len(sorted_events) - 1):
            diff = sorted_events[i + 1].timestamp - sorted_events[i].timestamp
            if diff > timedelta(minutes=max_gap_minutes):
                gaps.append((sorted_events[i].timestamp, sorted_events[i + 1].timestamp))
        return gaps

    def get_statistics(self) -> Dict[str, Any]:
        if not self._events:
            return {"total_events": 0}

        severity_counts = defaultdict(int)
        source_counts = defaultdict(int)
        for event in self._events:
            severity_counts[event.severity.value] += 1
            source_counts[event.source] += 1

        return {
            "total_events": len(self._events),
            "by_severity": dict(severity_counts),
            "by_source": dict(source_counts),
            "earliest": min(e.timestamp for e in self._events).isoformat(),
            "latest": max(e.timestamp for e in self._events).isoformat(),
        }


# ---------------------------------------------------------------------------
# Memory Analyzer
# ---------------------------------------------------------------------------

class MemoryAnalyzer:
    """Analyzes memory dumps for forensic artifacts."""

    def __init__(self) -> None:
        self._suspicious_patterns = [
            "mimikatz", "lazagne", "procdump", "psexec", "nc.exe",
            "metasploit", "cobalt strike", "meterpreter", "empire",
        ]

    def analyze(self, memory_dump_path: str) -> MemoryAnalysisResults:
        results = MemoryAnalysisResults(file_path=memory_dump_path)

        # Simulate process enumeration
        simulated_processes = [
            ProcessInfo(name="lsass.exe", pid=556, parent_name="wininit.exe", parent_pid=476,
                       risk_score=80, indicators=["credential access target"]),
            ProcessInfo(name="svchost.exe", pid=1234, parent_name="services.exe", parent_pid=700,
                       risk_score=10),
            ProcessInfo(name="powershell.exe", pid=4532, parent_name="wsmprovhost.exe", parent_pid=3800,
                       command_line="powershell -enc ABC...", risk_score=75,
                       indicators=["encoded command", "suspicious parent"]),
        ]

        results.total_processes = len(simulated_processes)
        results.suspicious_processes = [p for p in simulated_processes if p.risk_score >= 50]

        # Simulate network connections
        results.network_connections = [
            {"local": "10.0.1.100:49152", "remote": "198.51.100.42:443", "state": "ESTABLISHED"},
            {"local": "10.0.1.100:49153", "remote": "203.0.113.50:8080", "state": "ESTABLISHED"},
        ]

        return results

    def detect_code_injection(self, results: MemoryAnalysisResults) -> List[MemoryInjection]:
        injections = []
        for proc in results.suspicious_processes:
            if proc.risk_score > 70:
                injections.append(MemoryInjection(
                    process_name=proc.name,
                    pid=proc.pid,
                    injection_type=InjectionType.DLL_INJECTION,
                    address="0x7FFE0000",
                    size=4096,
                    risk_score=proc.risk_score,
                ))
        return injections


# ---------------------------------------------------------------------------
# Log Correlator
# ---------------------------------------------------------------------------

class LogCorrelator:
    """Correlates events across multiple log sources."""

    def __init__(self) -> None:
        self._sources: Dict[str, LogSource] = {}
        self._entries: Dict[str, List[LogEntry]] = defaultdict(list)

    def add_source(self, source: LogSource) -> None:
        self._sources[source.name] = source

    def add_entries(self, source_name: str, entries: List[LogEntry]) -> None:
        self._entries[source_name].extend(entries)

    def correlate(
        self,
        time_window_seconds: int = 300,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[LogCorrelation]:
        correlations = []
        all_entries = []
        for source_name, entries in self._entries.items():
            for entry in entries:
                entry.source = source_name
                all_entries.append(entry)

        all_entries.sort(key=lambda e: e.timestamp)

        # Group entries within time windows
        window = timedelta(seconds=time_window_seconds)
        i = 0
        while i < len(all_entries):
            group = [all_entries[i]]
            j = i + 1
            while j < len(all_entries):
                if (all_entries[j].timestamp - all_entries[i].timestamp) <= window:
                    if self._matches_filters(all_entries[j], filters):
                        group.append(all_entries[j])
                j += 1

            if len(group) > 1:
                sources = list(set(e.source for e in group))
                correlations.append(LogCorrelation(
                    timestamp=group[0].timestamp,
                    source=",".join(sources),
                    message=f"Correlated {len(group)} events from {len(sources)} sources",
                    related_events=group,
                    correlation_score=min(len(group) * 20, 100),
                ))
            i += 1

        return correlations

    def _matches_filters(self, entry: LogEntry, filters: Optional[Dict[str, Any]]) -> bool:
        if filters is None:
            return True
        for key, value in filters.items():
            entry_value = entry.fields.get(key)
            if entry_value is None:
                return False
            if isinstance(value, str) and value.lower() not in str(entry_value).lower():
                return False
        return True


# ---------------------------------------------------------------------------
# Forensic Report Generator
# ---------------------------------------------------------------------------

class ForensicReportGenerator:
    """Generates forensic investigation reports."""

    def generate(self, report: ForensicReport) -> str:
        lines = [
            f"# Forensic Investigation Report",
            f"\n**Case ID:** {report.case_id}",
            f"**Title:** {report.title}",
            f"**Investigator:** {report.investigator}",
            f"**Date:** {report.created_at.strftime('%Y-%m-%d')}",
            f"\n## Executive Summary\n\n{report.executive_summary}",
        ]

        if report.evidence_items:
            lines.append("\n## Evidence Collected\n")
            lines.append("| Type | Source | SHA256 | Collected By |")
            lines.append("|------|--------|--------|--------------|")
            for ev in report.evidence_items:
                lines.append(f"| {ev.evidence_type.value} | `{ev.source}` | `{ev.sha256_hash or 'N/A'}` | {ev.collected_by} |")

        if report.timeline and report.timeline.events:
            lines.append("\n## Timeline\n")
            for event in sorted(report.timeline.events, key=lambda e: e.timestamp):
                lines.append(f"- **{event.timestamp.isoformat()}** [{event.severity.value}] {event.source}: {event.description}")

        if report.findings:
            lines.append("\n## Findings\n")
            for finding in report.findings:
                lines.append(f"- {finding}")

        if report.recommendations:
            lines.append("\n## Recommendations\n")
            for rec in report.recommendations:
                lines.append(f"- {rec}")

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the forensic analysis module."""
    print("=" * 60)
    print("  Forensic Analysis Module — Demo")
    print("=" * 60)

    # Initialize collector
    collector = EvidenceCollector(investigator="jsmith", case_id="IR-2024-042")

    # Collect evidence
    disk_evidence = collector.collect_disk_image(
        source="/dev/sda1",
        destination="/evidence/case-042/disk_image.E01",
    )
    print(f"\n[+] Disk Evidence Collected:")
    print(f"    SHA256: {disk_evidence.sha256_hash}")
    print(f"    Custodian: {disk_evidence.chain_of_custody.current_custodian}")

    memory_evidence = collector.collect_memory_dump(
        target="10.0.1.100",
        output="/evidence/case-042/memory.dmp",
    )
    print(f"\n[+] Memory Evidence Collected:")
    print(f"    Size: {memory_evidence.size_bytes / 1024 / 1024:.0f} MB")
    print(f"    MD5: {memory_evidence.md5_hash}")

    # Timeline analysis
    timeline_analyzer = TimelineAnalyzer()
    events = [
        TimelineEvent(
            timestamp=datetime(2024, 1, 15, 8, 30),
            source="auth_log",
            description="Failed login from 198.51.100.42",
            severity=SeverityLevel.MEDIUM,
        ),
        TimelineEvent(
            timestamp=datetime(2024, 1, 15, 8, 31),
            source="auth_log",
            description="Successful login from 198.51.100.42",
            severity=SeverityLevel.HIGH,
        ),
        TimelineEvent(
            timestamp=datetime(2024, 1, 15, 8, 45),
            source="process_log",
            description="powershell.exe with encoded command",
            severity=SeverityLevel.HIGH,
        ),
    ]
    for event in events:
        timeline_analyzer.add_event(event)

    timeline = timeline_analyzer.generate_timeline()
    print(f"\n[+] Timeline ({len(timeline)} events):")
    for event in timeline:
        print(f"    [{event.timestamp}] {event.description}")

    # Memory analysis
    memory_analyzer = MemoryAnalyzer()
    mem_results = memory_analyzer.analyze("memory.dmp")
    print(f"\n[+] Memory Analysis:")
    print(f"    Total Processes: {mem_results.total_processes}")
    print(f"    Suspicious: {len(mem_results.suspicious_processes)}")
    for proc in mem_results.suspicious_processes:
        print(f"      - {proc.name} (PID {proc.pid}): risk {proc.risk_score}")

    injections = memory_analyzer.detect_code_injection(mem_results)
    print(f"    Code Injections: {len(injections)}")

    # Log correlation
    log_correlator = LogCorrelator()
    log_correlator.add_source(LogSource(name="auth", path="/var/log/auth.log"))
    log_correlator.add_entries("auth", [
        LogEntry(timestamp=datetime(2024, 1, 15, 8, 30), message="Login failed", fields={"src_ip": "198.51.100.42"}),
        LogEntry(timestamp=datetime(2024, 1, 15, 8, 31), message="Login success", fields={"src_ip": "198.51.100.42"}),
    ])
    correlations = log_correlator.correlate(time_window_seconds=120)
    print(f"\n[+] Log Correlations: {len(correlations)}")

    # Generate report
    report_gen = ForensicReportGenerator()
    report = ForensicReport(
        case_id="IR-2024-042",
        title="APT29 Investigation",
        investigator="jsmith",
        executive_summary="Investigation identified unauthorized access and data exfiltration.",
        evidence_items=collector.get_all_evidence(),
        findings=["Unauthorized login detected", "Encoded PowerShell execution observed"],
        recommendations=["Reset compromised credentials", "Implement network segmentation"],
    )
    report.timeline = Timeline(events=timeline)
    report_md = report_gen.generate(report)
    print(f"\n[+] Report Generated ({len(report_md)} chars)")
    print(report_md[:300] + "...")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
