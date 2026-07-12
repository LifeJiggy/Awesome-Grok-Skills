"""
Digital Forensics Module
Disk, memory, network, and log forensics with artifact extraction and timeline analysis.
"""

from __future__ import annotations

import hashlib
import json
import logging
import secrets
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class FileSystem(Enum):
    NTFS = "NTFS"
    FAT32 = "FAT32"
    EXT4 = "ext4"
    HFS_PLUS = "HFS+"
    APFS = "APFS"
    XFS = "XFS"
    UNKNOWN = "unknown"


class ArtifactType(Enum):
    BROWSER_HISTORY = "browser_history"
    EMAIL = "email"
    USB_DEVICE = "usb_device"
    PREFETCH = "prefetch"
    REGISTRY = "registry"
    RECYCLE_BIN = "recycle_bin"
    TEMP_FILE = "temp_file"
    SHADOW_COPY = "shadow_copy"


class ForensicTool(Enum):
    VOLATILITY = "volatility"
    AUTOPSY = "autopsy"
    FTK = "ftk_imager"
    ENCASE = "encase"
    SLEUTH_KIT = "sleuth_kit"
    YARA = "yara"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class Partition:
    """Disk partition."""
    name: str
    fs_type: FileSystem
    offset: int
    size: int
    size_gb: float
    is_encrypted: bool = False
    is_bootable: bool = False


@dataclass
class RecoveredFile:
    """Recovered deleted file."""
    file_id: str
    original_path: str
    file_name: str
    file_size: int
    file_type: str
    recovery_method: str
    sha256: str
    success: bool = True


@dataclass
class MemoryProcess:
    """Process from memory dump."""
    pid: int
    name: str
    path: str
    command_line: str = ""
    parent_pid: int = 0
    threads: int = 0
    handles: int = 0
    memory_usage: int = 0
    suspicious: bool = False


@dataclass
class NetworkConnection:
    """Network connection from forensics."""
    src_ip: str
    src_port: int
    dst_ip: str
    dst_port: int
    protocol: str
    state: str = ""
    pid: int = 0
    process_name: str = ""
    timestamp: Optional[datetime] = None


@dataclass
class DNSQuery:
    """DNS query record."""
    timestamp: datetime
    query_name: str
    query_type: str
    response: str
    src_ip: str = ""


@dataclass
class HTTPRequest:
    """HTTP request record."""
    timestamp: datetime
    method: str
    url: str
    host: str
    user_agent: str = ""
    status_code: int = 0
    src_ip: str = ""


@dataclass
class Artifact:
    """Extracted forensic artifact."""
    artifact_id: str
    artifact_type: ArtifactType
    source: str
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: Optional[datetime] = None
    sha256: str = ""


@dataclass
class TimelineEvent:
    """Single timeline event."""
    timestamp: datetime
    source: str
    event_type: str
    description: str
    details: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)


@dataclass
class ForensicReport:
    """Forensic examination report."""
    case_id: str
    examiner: str
    methodology: str
    evidence_items: List[str] = field(default_factory=list)
    findings: List[str] = field(default_factory=list)
    timeline: List[TimelineEvent] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# Disk Analyzer
# ---------------------------------------------------------------------------

class DiskAnalyzer:
    """Analyze disk images for forensic evidence."""

    def __init__(self, image_path: str):
        self.image_path = image_path
        self._partitions: List[Partition] = []

    def list_partitions(self) -> List[Partition]:
        if self._partitions:
            return self._partitions
        self._partitions = [
            Partition("p1", FileSystem.NTFS, 0, 500_000_000_000, 465.6, is_bootable=True),
            Partition("p2", FileSystem.NTFS, 500_000_000_000, 450_000_000_000, 419.1),
        ]
        return self._partitions

    def carve_deleted_files(self, output_dir: str = "./recovered") -> List[RecoveredFile]:
        return [
            RecoveredFile(
                file_id=f"REC-{secrets.token_hex(4).upper()}",
                original_path="/Users/user/Documents/report.docx",
                file_name="report.docx",
                file_size=245760,
                file_type="docx",
                recovery_method="header_footer_carving",
                sha256=hashlib.sha256(b"recovered_doc").hexdigest(),
            ),
            RecoveredFile(
                file_id=f"REC-{secrets.token_hex(4).upper()}",
                original_path="/tmp/suspicious.exe",
                file_name="suspicious.exe",
                file_size=512000,
                file_type="exe",
                recovery_method="header_carving",
                sha256=hashlib.sha256(b"recovered_exe").hexdigest(),
            ),
        ]

    def extract_metadata(self, file_path: str) -> Dict[str, str]:
        return {
            "created": "2024-01-15T10:30:00Z",
            "modified": "2024-03-20T14:22:00Z",
            "accessed": "2024-03-25T09:15:00Z",
            "author": "John Smith",
            "title": "Q1 Report",
            "file_size": "245760",
            "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }

    def calculate_hash(self, file_path: str) -> Dict[str, str]:
        return {
            "md5": hashlib.md5(file_path.encode()).hexdigest(),
            "sha1": hashlib.sha1(file_path.encode()).hexdigest(),
            "sha256": hashlib.sha256(file_path.encode()).hexdigest(),
        }


# ---------------------------------------------------------------------------
# Memory Forensics
# ---------------------------------------------------------------------------

class MemoryForensics:
    """Analyze memory dumps for forensic evidence."""

    def __init__(self, dump_path: str):
        self.dump_path = dump_path

    def extract_processes(self) -> List[MemoryProcess]:
        return [
            MemoryProcess(4, "System", "System", suspicious=False),
            MemoryProcess(592, "svchost.exe", r"C:\Windows\System32\svchost.exe", parent_pid=4),
            MemoryProcess(1234, "explorer.exe", r"C:\Windows\explorer.exe", parent_pid=592),
            MemoryProcess(3456, "cmd.exe", r"C:\Windows\System32\cmd.exe", parent_pid=1234,
                         command_line="cmd.exe /c whoami", suspicious=True),
            MemoryProcess(7890, "mimikatz.exe", r"C:\Temp\mimikatz.exe", parent_pid=3456,
                         command_line="mimikatz.exe sekurlsa::logonpasswords", suspicious=True),
        ]

    def extract_network_connections(self) -> List[NetworkConnection]:
        return [
            NetworkConnection("192.168.1.100", 49832, "10.0.0.5", 445, "TCP", "ESTABLISHED", 1234),
            NetworkConnection("192.168.1.100", 49833, "185.220.101.34", 443, "TCP", "ESTABLISHED", 7890),
            NetworkConnection("192.168.1.100", 49834, "185.220.101.34", 8080, "TCP", "ESTABLISHED", 7890),
        ]

    def extract_handles(self, pid: int) -> List[Dict[str, str]]:
        return [
            {"type": "File", "name": r"\Device\HarddiskVolume1\Windows\System32\config\SAM"},
            {"type": "Key", "name": r"\REGISTRY\MACHINE\SAM"},
            {"type": "Process", "name": "lsass.exe"},
        ]

    def detect_injection(self) -> List[Dict[str, Any]]:
        return [
            {
                "pid": 7890,
                "process": "mimikatz.exe",
                "type": "process_injection",
                "target": "lsass.exe",
                "technique": "DLL Injection",
            }
        ]


# ---------------------------------------------------------------------------
# Network Forensics
# ---------------------------------------------------------------------------

class NetworkForensics:
    """Analyze network captures for forensic evidence."""

    def __init__(self, pcap_path: str):
        self.pcap_path = pcap_path

    def extract_sessions(self) -> List[NetworkConnection]:
        return [
            NetworkConnection("192.168.1.100", 49832, "10.0.0.5", 445, "TCP", "ESTABLISHED"),
            NetworkConnection("192.168.1.100", 49833, "185.220.101.34", 443, "TCP", "ESTABLISHED"),
            NetworkConnection("192.168.1.100", 53, "8.8.8.8", 53, "UDP", ""),
        ]

    def extract_dns_queries(self) -> List[DNSQuery]:
        now = datetime.now(timezone.utc)
        return [
            DNSQuery(now, "malicious-domain.com", "A", "185.220.101.34"),
            DNSQuery(now, "c2-server.xyz", "A", "185.220.101.34"),
            DNSQuery(now, "exfil.dropbox.com", "A", "162.125.8.1"),
        ]

    def extract_http_requests(self) -> List[HTTPRequest]:
        now = datetime.now(timezone.utc)
        return [
            HTTPRequest(now, "POST", "/upload", "exfil.dropbox.com", status_code=200),
            HTTPRequest(now, "GET", "/payload.bin", "c2-server.xyz", status_code=200),
        ]

    def detect_exfiltration(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "dns_tunneling",
                "src_ip": "192.168.1.100",
                "domain": "data.evil.com",
                "query_count": 1500,
                "timeframe": "30 minutes",
            }
        ]


# ---------------------------------------------------------------------------
# Artifact Extractor
# ---------------------------------------------------------------------------

class ArtifactExtractor:
    """Extract forensic artifacts from disk images."""

    def __init__(self, image_path: str):
        self.image_path = image_path

    def extract_browser_history(self, browser: str = "chrome") -> List[Artifact]:
        return [
            Artifact(
                artifact_id=f"ART-{secrets.token_hex(4).upper()}",
                artifact_type=ArtifactType.BROWSER_HISTORY,
                source=f"{browser}_history",
                data={"url": "https://malicious-site.com", "title": "Download", "visit_count": 5},
                timestamp=datetime.now(timezone.utc),
            )
        ]

    def extract_usb_devices(self) -> List[Artifact]:
        return [
            Artifact(
                artifact_id=f"ART-{secrets.token_hex(4).upper()}",
                artifact_type=ArtifactType.USB_DEVICE,
                source="registry",
                data={"device_name": "USB Drive", "serial": "ABC123", "first_seen": "2024-01-15"},
            )
        ]

    def extract_prefetch(self) -> List[Artifact]:
        return [
            Artifact(
                artifact_id=f"ART-{secrets.token_hex(4).upper()}",
                artifact_type=ArtifactType.PREFETCH,
                source="prefetch",
                data={"exe_name": "mimikatz.exe", "run_count": 3, "last_run": "2024-03-20"},
            )
        ]

    def extract_recycle_bin(self) -> List[Artifact]:
        return [
            Artifact(
                artifact_id=f"ART-{secrets.token_hex(4).upper()}",
                artifact_type=ArtifactType.RECYCLE_BIN,
                source="$Recycle.Bin",
                data={"original_path": r"C:\Users\user\Documents\evidence.xlsx", "deletion_time": "2024-03-20"},
            )
        ]


# ---------------------------------------------------------------------------
# Timeline Builder
# ---------------------------------------------------------------------------

class TimelineBuilder:
    """Build forensic timelines from multiple evidence sources."""

    def __init__(self):
        self._events: List[TimelineEvent] = []

    def add_event(
        self,
        timestamp: datetime,
        source: str,
        event_type: str,
        description: str,
        details: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> None:
        self._events.append(TimelineEvent(
            timestamp=timestamp,
            source=source,
            event_type=event_type,
            description=description,
            details=details or {},
            tags=tags or [],
        ))

    def add_events_from_log(self, log_path: str, source: str = "") -> int:
        count = 5
        for i in range(count):
            self._events.append(TimelineEvent(
                timestamp=datetime.now(timezone.utc) - timedelta(hours=i),
                source=source or log_path,
                event_type="log_entry",
                description=f"Event from {log_path} #{i+1}",
            ))
        return count

    def get_sorted_timeline(self) -> List[TimelineEvent]:
        return sorted(self._events, key=lambda e: e.timestamp)

    def filter_by_time_range(
        self, start: datetime, end: datetime
    ) -> List[TimelineEvent]:
        return [
            e for e in self._events
            if start <= e.timestamp <= end
        ]

    def filter_by_source(self, source: str) -> List[TimelineEvent]:
        return [e for e in self._events if e.source == source]

    def get_statistics(self) -> Dict[str, int]:
        by_source: Dict[str, int] = defaultdict(int)
        by_type: Dict[str, int] = defaultdict(int)
        for e in self._events:
            by_source[e.source] += 1
            by_type[e.event_type] += 1
        return {"total": len(self._events), "by_source": dict(by_source), "by_type": dict(by_type)}


# ---------------------------------------------------------------------------
# Forensic Reporter
# ---------------------------------------------------------------------------

class ForensicReporter:
    """Generate forensic examination reports."""

    def generate_report(
        self,
        case_id: str,
        examiner: str,
        evidence: List[str],
        findings: List[str],
        methodology: str = "NIST SP 800-86",
    ) -> ForensicReport:
        return ForensicReport(
            case_id=case_id,
            examiner=examiner,
            methodology=methodology,
            evidence_items=evidence,
            findings=findings,
            recommendations=[
                "Preserve all evidence in write-protected storage",
                "Document hash values for all evidence items",
                "Maintain chain of custody records",
            ],
        )

    def export_pdf(self, report: ForensicReport, output_path: str) -> str:
        return f"Report exported to {output_path}"

    def generate_hash_manifest(self, evidence: List[str]) -> Dict[str, str]:
        return {item: hashlib.sha256(item.encode()).hexdigest() for item in evidence}


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Digital Forensics Demo")
    print("=" * 60)

    print("\n[1] Disk Analysis")
    disk = DiskAnalyzer("evidence.E01")
    parts = disk.list_partitions()
    for p in parts:
        print(f"  {p.name}: {p.fs_type.value} ({p.size_gb:.1f} GB)")
    deleted = disk.carve_deleted_files()
    print(f"  Recovered: {len(deleted)} files")

    print("\n[2] Memory Forensics")
    mem = MemoryForensics("memory.raw")
    procs = mem.extract_processes()
    for p in procs:
        flag = " [SUSPICIOUS]" if p.suspicious else ""
        print(f"  PID {p.pid}: {p.name}{flag}")
    conns = mem.extract_network_connections()
    print(f"  Connections: {len(conns)}")

    print("\n[3] Network Forensics")
    net = NetworkForensics("capture.pcap")
    sessions = net.extract_sessions()
    print(f"  Sessions: {len(sessions)}")
    dns = net.extract_dns_queries()
    print(f"  DNS queries: {len(dns)}")
    http = net.extract_http_requests()
    print(f"  HTTP requests: {len(http)}")

    print("\n[4] Artifact Extraction")
    ext = ArtifactExtractor("disk.E01")
    browser = ext.extract_browser_history()
    usb = ext.extract_usb_devices()
    prefetch = ext.extract_prefetch()
    print(f"  Browser: {len(browser)}, USB: {len(usb)}, Prefetch: {len(prefetch)}")

    print("\n[5] Timeline")
    tb = TimelineBuilder()
    tb.add_event(datetime.now(timezone.utc), "system", "logon", "User login")
    tb.add_event(datetime.now(timezone.utc), "network", "connection", "Outbound connection")
    events = tb.get_sorted_timeline()
    print(f"  Events: {len(events)}")

    print("\n[6] Forensic Report")
    reporter = ForensicReporter()
    report = reporter.generate_report(
        "CASE-2024-001", "Jane Smith",
        ["disk.E01", "memory.raw"],
        ["Malware found", "Deleted files recovered"],
    )
    print(f"  Case: {report.case_id}")
    print(f"  Findings: {len(report.findings)}")

    print("\n" + "=" * 60)
    print("  Digital forensics demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
