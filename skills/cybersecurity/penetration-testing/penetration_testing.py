"""
Penetration Testing Module
Recon, scanning, exploitation, privilege escalation, and reporting.
"""

from __future__ import annotations

import hashlib
import logging
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

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


class ScanType(Enum):
    PORT = "port"
    SERVICE = "service"
    VULNERABILITY = "vulnerability"
    WEB = "web"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class ReconResult:
    """Reconnaissance result."""
    target: str
    subdomains: List[str] = field(default_factory=list)
    ip_addresses: List[str] = field(default_factory=list)
    emails: List[str] = field(default_factory=list)
    technologies: List[str] = field(default_factory=list)
    open_ports: List[int] = field(default_factory=list)


@dataclass
class ScanResult:
    """Scan result."""
    target: str
    hosts_up: int = 0
    open_ports: List[Dict[str, Any]] = field(default_factory=list)
    vulnerabilities: List[Dict[str, Any]] = field(default_factory=list)
    services: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ExploitResult:
    """Exploitation result."""
    success: bool
    target: str
    exploit: str
    shell_type: str = ""
    session_id: str = ""
    output: str = ""


@dataclass
class PrivEscVuln:
    """Privilege escalation vulnerability."""
    technique: str
    severity: Severity
    description: str
    remediation: str = ""
    cve: str = ""


@dataclass
class PentestFinding:
    """Penetration test finding."""
    title: str
    severity: Severity
    description: str
    impact: str
    remediation: str
    evidence: List[str] = field(default_factory=list)
    cvss_score: float = 0.0


@dataclass
class PentestReport:
    """Penetration test report."""
    title: str
    scope: str
    methodology: str
    executive_summary: str
    findings: List[PentestFinding] = field(default_factory=list)
    total_findings: int = 0
    start_date: str = ""
    end_date: str = ""


# ---------------------------------------------------------------------------
# Recon Engine
# ---------------------------------------------------------------------------

class ReconEngine:
    """Reconnaissance and information gathering."""

    def passive_recon(self, target: str) -> ReconResult:
        return ReconResult(
            target=target,
            subdomains=[f"www.{target}", f"mail.{target}", f"api.{target}", f"dev.{target}"],
            ip_addresses=["93.184.216.34", "93.184.216.35"],
            emails=[f"admin@{target}", f"info@{target}", f"security@{target}"],
            technologies=["nginx", "react", "postgresql", "redis"],
        )

    def active_recon(self, target: str) -> ReconResult:
        result = self.passive_recon(target)
        result.open_ports = [22, 80, 443, 8080, 5432]
        return result


# ---------------------------------------------------------------------------
# Vuln Scanner
# ---------------------------------------------------------------------------

class VulnScanner:
    """Vulnerability scanning."""

    def scan(
        self, target: str, scan_type: str = "service", ports: str = "1-1000"
    ) -> ScanResult:
        vulns = [
            {"name": "CVE-2023-1234", "severity": "high", "service": "ssh", "port": 22},
            {"name": "CVE-2023-5678", "severity": "medium", "service": "http", "port": 80},
            {"name": "Weak Credentials", "severity": "critical", "service": "postgresql", "port": 5432},
        ]
        services = [
            {"port": 22, "service": "ssh", "version": "OpenSSH 8.2"},
            {"port": 80, "service": "http", "version": "nginx/1.18"},
            {"port": 443, "service": "https", "version": "nginx/1.18"},
            {"port": 5432, "service": "postgresql", "version": "13.4"},
        ]
        return ScanResult(
            target=target,
            hosts_up=1,
            open_ports=[{"port": s["port"], "service": s["service"]} for s in services],
            vulnerabilities=vulns,
            services=services,
        )


# ---------------------------------------------------------------------------
# Exploit Framework
# ---------------------------------------------------------------------------

class ExploitFramework:
    """Exploitation framework."""

    KNOWN_EXPLOITS = {
        "ms17_010": {"name": "EternalBlue", "severity": "critical", "target": "Windows SMB"},
        "log4shell": {"name": "Log4Shell", "severity": "critical", "target": "Log4j"},
        "spring4shell": {"name": "Spring4Shell", "severity": "critical", "target": "Spring Framework"},
    }

    def run_exploit(
        self,
        target: str,
        exploit: str,
        payload: str = "reverse_shell",
        lhost: str = "127.0.0.1",
        lport: int = 4444,
    ) -> ExploitResult:
        exploit_info = self.KNOWN_EXPLOITS.get(exploit, {"name": exploit})
        session_id = secrets.token_hex(8)
        return ExploitResult(
            success=True,
            target=target,
            exploit=exploit_info.get("name", exploit),
            shell_type="meterpreter" if payload == "reverse_shell" else payload,
            session_id=session_id,
            output=f"Session {session_id} established with {target}",
        )

    def list_exploits(self) -> List[Dict[str, str]]:
        return [
            {"id": k, "name": v["name"], "severity": v["severity"]}
            for k, v in self.KNOWN_EXPLOITS.items()
        ]


# ---------------------------------------------------------------------------
# Privilege Escalation Detector
# ---------------------------------------------------------------------------

class PrivEscDetector:
    """Detect privilege escalation opportunities."""

    def check_linux(
        self,
        os_info: str = "",
        kernel_version: str = "",
        suid_binaries: Optional[List[str]] = None,
        sudo_permissions: str = "",
    ) -> List[PrivEscVuln]:
        vulns: List[PrivEscVuln] = []
        if sudo_permissions == "ALL":
            vulns.append(PrivEscVuln(
                technique="sudo ALL misconfiguration",
                severity=Severity.CRITICAL,
                description="User has unrestricted sudo access",
                remediation="Apply principle of least privilege to sudo configuration",
            ))
        dangerous_suids = ["/usr/bin/find", "/usr/bin/vim", "/usr/bin/python3", "/usr/bin/perl"]
        for binary in (suid_binaries or []):
            if binary in dangerous_suids:
                vulns.append(PrivEscVuln(
                    technique=f"SUID binary: {binary}",
                    severity=Severity.HIGH,
                    description=f" Dangerous SUID binary {binary} can be used for privilege escalation",
                    remediation=f"Remove SUID bit from {binary}",
                ))
        if kernel_version:
            vulns.append(PrivEscVuln(
                technique="Kernel version check",
                severity=Severity.MEDIUM,
                description=f"Kernel {kernel_version} may have known vulnerabilities",
                remediation="Update kernel to latest stable version",
            ))
        return vulns

    def check_windows(
        self,
        os_version: str = "",
        installed_patches: Optional[List[str]] = None,
    ) -> List[PrivEscVuln]:
        vulns: List[PrivEscVuln] = []
        vulns.append(PrivEscVuln(
            technique="Token impersonation",
            severity=Severity.MEDIUM,
            description="SeImpersonatePrivilege may allow potato attacks",
            remediation="Remove SeImpersonatePrivilege from non-admin accounts",
        ))
        return vulns


# ---------------------------------------------------------------------------
# Report Generator
# ---------------------------------------------------------------------------

class ReportGenerator:
    """Generate penetration test reports."""

    def generate(
        self,
        findings: Optional[List[PrivEscVuln]] = None,
        scope: str = "",
        methodology: str = "OWASP Testing Guide",
        executive_summary: str = "",
    ) -> PentestReport:
        pentest_findings = []
        for f in (findings or []):
            pentest_findings.append(PentestFinding(
                title=f.technique,
                severity=f.severity,
                description=f.description,
                impact="Privilege escalation to root/admin",
                remediation=f.remediation,
            ))
        return PentestReport(
            title=f"Penetration Test Report - {scope}",
            scope=scope,
            methodology=methodology,
            executive_summary=executive_summary,
            findings=pentest_findings,
            total_findings=len(pentest_findings),
            start_date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Penetration Testing Demo")
    print("=" * 60)

    print("\n[1] Reconnaissance")
    recon = ReconEngine()
    results = recon.passive_recon("example.com")
    print(f"  Subdomains: {results.subdomains}")
    print(f"  IPs: {results.ip_addresses}")
    print(f"  Technologies: {results.technologies}")

    print("\n[2] Scanning")
    scanner = VulnScanner()
    scan = scanner.scan("192.168.1.0/24")
    print(f"  Hosts: {scan.hosts_up}")
    print(f"  Open ports: {len(scan.open_ports)}")
    print(f"  Vulnerabilities: {len(scan.vulnerabilities)}")
    for v in scan.vulnerabilities:
        print(f"    [{v['severity']}] {v['name']}")

    print("\n[3] Exploitation")
    exploit = ExploitFramework()
    result = exploit.run_exploit("192.168.1.10", "ms17_010")
    print(f"  Success: {result.success}")
    print(f"  Shell: {result.shell_type}")
    print(f"  Session: {result.session_id}")

    print("\n[4] Privilege Escalation")
    privesc = PrivEscDetector()
    vulns = privesc.check_linux(
        kernel_version="5.4.0-42",
        suid_binaries=["/usr/bin/find", "/usr/bin/vim"],
        sudo_permissions="ALL",
    )
    for v in vulns:
        print(f"  [{v.severity.value}] {v.technique}")

    print("\n[5] Report Generation")
    reporter = ReportGenerator()
    report = reporter.generate(vulns, "192.168.1.0/24")
    print(f"  Title: {report.title}")
    print(f"  Findings: {report.total_findings}")
    print(f"  Methodology: {report.methodology}")

    print("\n" + "=" * 60)
    print("  Penetration testing demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
