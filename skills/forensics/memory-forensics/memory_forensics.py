"""
Memory Forensics Module
Part of the forensics skill domain

Provides RAM dump analysis, process extraction, network connection
recovery, malware detection, credential extraction, and rootkit detection.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import uuid


class AnalysisProfile(Enum):
    WIN10_X64 = "win10_x64"
    WIN7_X86 = "win7_x86"
    LINUX_X64 = "linux_x64"
    LINUX_ARM = "linux_arm"
    MACOS_X64 = "macos_x64"


class ProcessRisk(Enum):
    CLEAN = "clean"
    SUSPICIOUS = "suspicious"
    MALICIOUS = "malicious"


class CredentialType(Enum):
    NTLM_HASH = "ntlm_hash"
    KERBEROS_TICKET = "kerberos_ticket"
    PLAINTEXT = "plaintext"
    BROWSER_SAVED = "browser_saved"
    LSASS_DUMP = "lsass_dump"


class MalwareSeverity(Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SocketState(Enum):
    LISTEN = "listen"
    ESTABLISHED = "established"
    TIME_WAIT = "time_wait"
    CLOSE_WAIT = "close_wait"
    SYN_SENT = "syn_sent"


@dataclass
class ProcessInfo:
    pid: int
    ppid: int
    name: str
    cmdline: str
    thread_count: int
    handle_count: int
    memory_usage_kb: int
    created_time: str
    is_suspicious: bool = False
    risk_level: ProcessRisk = ProcessRisk.CLEAN
    indicators: List[str] = field(default_factory=list)


@dataclass
class NetworkConnection:
    local_address: str
    local_port: int
    remote_address: str
    remote_port: int
    state: SocketState
    pid: int
    process_name: str
    protocol: str = "TCP"
    created_time: str = ""


@dataclass
class MalwareFinding:
    rule_name: str
    severity: MalwareSeverity
    process_name: str
    pid: int
    evidence_description: str
    yara_match: bool
    offset: int = 0
    length: int = 0


@dataclass
class Credential:
    credential_type: CredentialType
    username: str
    domain: str
    source_process: str
    hash_value: str = ""
    plaintext: str = ""
    url: str = ""  # for browser creds


@dataclass
class KernelModule:
    name: str
    base_address: int
    size: int
    driver_object: int
    is_signed: bool
    is_suspicious: bool = False


@dataclass
class DLLInfo:
    name: str
    base_address: int
    size: int
    path: str
    is_signed: bool
    pid: int


class MemoryAnalyzer:
    """Core memory image analysis using Volatility-style parsing."""

    SUSPICIOUS_PROCESSES = {"mimikatz", "procdump", "psexec", "nc", "ncat",
                            "meterpreter", "cobaltstrike", "powershell"}

    def __init__(self, profile: AnalysisProfile = AnalysisProfile.WIN10_X64,
                 volatility_path: str = "volatility3"):
        self.profile = profile
        self.vol_path = volatility_path

    def analyze_processes(self, memory_image: str) -> List[ProcessInfo]:
        # Simulated process list from memory analysis
        processes = [
            ProcessInfo(4, 0, "System", "", 125, 2847, 4096, "2026-07-01T08:00:00"),
            ProcessInfo(412, 4, "smss.exe", "", 3, 312, 1024, "2026-07-01T08:00:01"),
            ProcessInfo(624, 500, "csrss.exe", "", 12, 856, 5120, "2026-07-01T08:00:02"),
            ProcessInfo(700, 500, "wininit.exe", "", 5, 423, 2048, "2026-07-01T08:00:02"),
            ProcessInfo(1024, 700, "svchost.exe", "svchost -k netsvcs", 45, 1230, 15360, "2026-07-01T08:00:05"),
            ProcessInfo(2840, 1024, "powershell.exe", "powershell -enc <base64>", 8, 342, 8192, "2026-07-01T14:32:15",
                        is_suspicious=True, risk_level=ProcessRisk.SUSPICIOUS,
                        indicators=["encoded_command", "unusual_parent"]),
            ProcessInfo(3156, 2840, "cmd.exe", "cmd /c whoami", 2, 87, 1024, "2026-07-01T14:32:18",
                        is_suspicious=True, risk_level=ProcessRisk.SUSPICIOUS,
                        indicators=["child_of_suspicious_parent"]),
        ]
        return processes

    def analyze_dlls(self, memory_image: str, pid: int) -> List[DLLInfo]:
        return [
            DLLInfo("ntdll.dll", 0x7FFE0000, 2048000, "C:\\Windows\\System32\\ntdll.dll", True, pid),
            DLLInfo("kernel32.dll", 0x7FF80000, 1024000, "C:\\Windows\\System32\\kernel32.dll", True, pid),
            DLLInfo("unknown_module.dll", 0x10000000, 65536, "C:\\Temp\\unknown_module.dll", False, pid),
        ]


class NetworkAnalyzer:
    """Network connection extraction from memory."""

    def extract_connections(
        self, memory_image: str, include_closed: bool = False,
    ) -> List[NetworkConnection]:
        connections = [
            NetworkConnection("192.168.1.100", 49832, "10.0.0.5", 445,
                              SocketState.ESTABLISHED, 4, "System"),
            NetworkConnection("192.168.1.100", 49834, "185.220.101.34", 443,
                              SocketState.ESTABLISHED, 2840, "powershell.exe"),
            NetworkConnection("0.0.0.0", 4444, "0.0.0.0", 0,
                              SocketState.LISTEN, 3156, "nc.exe"),
            NetworkConnection("192.168.1.100", 49840, "8.8.8.8", 53,
                              SocketState.ESTABLISHED, 1024, "svchost.exe"),
        ]
        if not include_closed:
            connections = [c for c in connections if c.state != SocketState.TIME_WAIT]
        return connections


class MalwareDetector:
    """Memory-based malware detection with YARA and heuristics."""

    def __init__(self, yara_rules_dir: str = "rules/",
                 heuristics_enabled: bool = True):
        self.rules_dir = yara_rules_dir
        self.heuristics = heuristics_enabled

    def scan(self, memory_image: str,
             scan_type: str = "comprehensive") -> List[MalwareFinding]:
        findings = [
            MalwareFinding(
                rule_name="Encoded_PS_Command",
                severity=MalwareSeverity.HIGH,
                process_name="powershell.exe", pid=2840,
                evidence_description="PowerShell with encoded command detected",
                yara_match=True,
            ),
            MalwareFinding(
                rule_name="Suspicious_Network_Listen",
                severity=MalwareSeverity.CRITICAL,
                process_name="nc.exe", pid=3156,
                evidence_description="Netcat listener on port 4444 - potential reverse shell",
                yara_match=True,
            ),
        ]
        return findings


class CredentialExtractor:
    """Credential extraction from memory dumps."""

    def __init__(self, decrypt_browser_creds: bool = True,
                 extract_ntlm: bool = True):
        self.browser_creds = decrypt_browser_creds
        self.ntlm = extract_ntlm

    def extract(
        self, memory_image: str,
        target_processes: Optional[List[str]] = None,
    ) -> List[Credential]:
        creds = []
        targets = target_processes or ["lsass.exe"]

        if "lsass.exe" in targets:
            creds.extend([
                Credential(CredentialType.NTLM_HASH, "administrator", "ACME",
                           "lsass.exe", hash_value="aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0"),
                Credential(CredentialType.NTLM_HASH, "jsmith", "ACME",
                           "lsass.exe", hash_value="aad3b435b51404eeaad3b435b51404ee:a4f49c406510bdcab6824ee7c30fd852"),
            ])

        if "chrome.exe" in targets and self.browser_creds:
            creds.append(Credential(
                CredentialType.BROWSER_SAVED, "john@example.com", "",
                "chrome.exe", url="https://mail.example.com",
            ))

        return creds


class KernelAnalyzer:
    """Kernel-level rootkit and hook detection."""

    def analyze_kernel_modules(self, memory_image: str) -> List[KernelModule]:
        return [
            KernelModule("ntoskrnl.exe", 0xFFFFF80000000000, 16_000_000, 0xFFFFFA8000123456, True),
            KernelModule("NDIS.SYS", 0xFFFFF88002000000, 1_200_000, 0xFFFFFA8000234567, True),
            KernelModule("rootkit.sys", 0xFFFFF88003000000, 65536, 0xFFFFFA8000345678, False,
                         is_suspicious=True),
        ]


def main():
    print("=" * 60)
    print("  Memory Forensics Demo")
    print("=" * 60)

    # Process analysis
    print("\n--- Process Analysis ---")
    ma = MemoryAnalyzer(profile=AnalysisProfile.WIN10_X64)
    procs = ma.analyze_processes("evidence/memory.raw")
    print(f"  Processes: {len(procs)}")
    for p in procs:
        flag = " ***" if p.is_suspicious else ""
        print(f"    PID {p.pid}: {p.name} (PPID {p.ppid}){flag}")
        if p.indicators:
            print(f"      Indicators: {', '.join(p.indicators)}")

    # Network
    print("\n--- Network Connections ---")
    na = NetworkAnalyzer()
    conns = na.extract_connections("evidence/memory.raw")
    for c in conns:
        suspicious = " ***" if c.remote_address not in ("0.0.0.0", "127.0.0.1") and c.local_port > 40000 else ""
        print(f"    {c.local_address}:{c.local_port} -> {c.remote_address}:{c.remote_port} [{c.state.value}]{suspicious}")
        print(f"      PID {c.pid}: {c.process_name}")

    # Malware
    print("\n--- Malware Detection ---")
    md = MalwareDetector()
    findings = md.scan("evidence/memory.raw")
    for f in findings:
        print(f"  [{f.severity.value.upper()}] {f.rule_name}: {f.evidence_description}")
        print(f"    Process: {f.process_name} (PID {f.pid})")

    # Credentials
    print("\n--- Credential Extraction ---")
    ce = CredentialExtractor()
    creds = ce.extract("evidence/memory.raw", ["lsass.exe"])
    for c in creds:
        print(f"  {c.credential_type.value}: {c.domain}\\{c.username}")
        if c.hash_value:
            print(f"    Hash: {c.hash_value[:40]}...")

    # Kernel
    print("\n--- Kernel Analysis ---")
    ka = KernelAnalyzer()
    modules = ka.analyze_kernel_modules("evidence/memory.raw")
    for m in modules:
        flag = " *** ROOTKIT?" if m.is_suspicious else ""
        print(f"    {m.name}: base=0x{m.base_address:X}, signed={m.is_signed}{flag}")


if __name__ == "__main__":
    main()
