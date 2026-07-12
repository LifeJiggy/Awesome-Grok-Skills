"""
Penetration Testing Module

Structured offensive security testing framework covering reconnaissance,
exploitation, privilege escalation, lateral movement, and evidence collection.
For authorized security testing only.
"""

from __future__ import annotations

import os
import re
import time
import hashlib
import logging
from enum import Enum
from datetime import datetime
from typing import Optional, Any
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


# ──────────────────────────── Enums ────────────────────────────

class ReconPhase(str, Enum):
    PASSIVE = "passive"
    ACTIVE = "active"
    TARGETED = "targeted"


class ExploitResult(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    VERIFIED = "verified"
    NOT_EXPLOITABLE = "not_exploitable"
    BLOCKED = "blocked"


class Platform(str, Enum):
    LINUX = "linux"
    WINDOWS = "windows"
    MACOS = "macos"
    CONTAINER = "container"


class SessionType(str, Enum):
    METERPRETER = "meterpreter"
    SHELL = "shell"
    PowerShell = "powershell"
    SSH = "ssh"
    WINRM = "winrm"


class PrivEscTechnique(str, Enum):
    SUID_BINARY = "suid_binary"
    SUDO_MISCONFIG = "sudo_misconfig"
    KERNEL_EXPLOIT = "kernel_exploit"
    CAPABILITIES = "capabilities"
    CRON_JOB = "cron_job"
    WRITABLE_SERVICE = "writable_service"
    TOKEN_IMPERSONATION = "token_impersonation"
    UNQUOTED_SERVICE_PATH = "unquoted_service_path"


class PivotTechnique(str, Enum):
    SSH_KEY = "ssh_key"
    PASS_THE_HASH = "pass_the_hash"
    WINRM = "winrm"
    WMI = "wmi"
    PSExec = "psexec"
    SOCKS_PROXY = "socks_proxy"
    TUNNEL = "tunnel"


class WebVulnType(str, Enum):
    SQLI = "sqli"
    XSS = "xss"
    SSRF = "ssrf"
    XXE = "xxe"
    SSTI = "ssti"
    IDOR = "idor"
    AUTH_BYPASS = "auth_bypass"
    FILE_UPLOAD = "file_upload"


# ──────────────────────────── Dataclasses ─────────────────────

@dataclass
class Host:
    ip: str
    hostname: str = ""
    os: str = ""
    ports: list[int] = field(default_factory=list)
    services: dict[int, str] = field(default_factory=dict)
    technologies: list[str] = field(default_factory=list)
    is_alive: bool = True


@dataclass
class Port:
    number: int
    protocol: str = "tcp"
    state: str = "open"
    service: str = ""
    version: str = ""
    banner: str = ""


@dataclass
class WebEndpoint:
    url: str
    method: str = "GET"
    status_code: int = 0
    parameters: list[str] = field(default_factory=list)
    technologies: list[str] = field(default_factory=list)
    auth_required: bool = False


@dataclass
class ExploitFinding:
    endpoint: str
    vuln_type: WebVulnType
    technique: str
    payload: str
    impact: str
    severity: str = "HIGH"
    request_log: str = ""
    response_log: str = ""
    verified: bool = False


@dataclass
class PrivescVector:
    technique: PrivEscTechnique
    severity: str
    requirements: str
    reliability: str
    description: str
    command: str = ""


@dataclass
class PivotPath:
    source: str
    target: str
    technique: PivotTechnique
    credentials_needed: bool = True
    stealth_rating: str = "medium"


@dataclass
class Credential:
    username: str
    password: str = ""
    hash: str = ""
    source: str = ""
    domain: str = ""
    credential_type: str = "password"


@dataclass
class ReconReport:
    hosts: list[Host] = field(default_factory=list)
    web_endpoints: list[WebEndpoint] = field(default_factory=list)
    tech_stack: list[str] = field(default_factory=list)
    total_hosts: int = 0
    total_ports: int = 0
    total_endpoints: int = 0
    scan_time: datetime = field(default_factory=datetime.utcnow)


@dataclass
class SessionInfo:
    session_id: str
    target: str
    session_type: SessionType
    user: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True
    commands_executed: int = 0


# ──────────────────────────── Helper Classes ──────────────────

class WebExploiter:
    """Web application exploitation toolkit for authorized testing."""

    def __init__(self, target: str, scope: list[str] | None = None,
                 auth_tokens: dict[str, str] | None = None):
        self.target = target.rstrip("/")
        self.scope = scope or ["/"]
        self.auth_tokens = auth_tokens or {}
        self._endpoints: list[WebEndpoint] = []
        self._findings: list[ExploitFinding] = []

    def test_sqli(self, params: list[str] | None = None,
                  techniques: list[str] | None = None,
                  dbms: list[str] | None = None) -> list[ExploitFinding]:
        techniques = techniques or ["union", "blind", "time_based"]
        params = params or ["id", "search"]
        dbms = dbms or ["mysql"]

        for param in params:
            for tech in techniques:
                payload = self._generate_sqli_payload(tech, dbms[0])
                finding = ExploitFinding(
                    endpoint=f"{self.target}?{param}={payload[:30]}",
                    vuln_type=WebVulnType.SQLI,
                    technique=tech, payload=payload,
                    impact="Database data extraction possible",
                    verified=False,
                )
                self._findings.append(finding)
        return self._findings

    def test_xss(self, params: list[str] | None = None,
                  context: str = "reflected") -> list[ExploitFinding]:
        params = params or ["q", "name"]
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert(document.cookie)",
        ]
        for param in params:
            for payload in payloads:
                finding = ExploitFinding(
                    endpoint=f"{self.target}?{param}=PAYLOAD",
                    vuln_type=WebVulnType.XSS,
                    technique=context, payload=payload,
                    impact="Client-side code execution in victim browser",
                )
                self._findings.append(finding)
        return self._findings

    def test_idor(self, endpoints: list[str] | None = None) -> list[ExploitFinding]:
        endpoints = endpoints or ["/api/v1/users/{id}", "/api/v1/documents/{id}"]
        for ep in endpoints:
            finding = ExploitFinding(
                endpoint=f"{self.target}{ep}",
                vuln_type=WebVulnType.IDOR,
                technique="parameter_manipulation",
                payload="ID manipulation (1 → 2)",
                impact="Unauthorized access to other users' data",
            )
            self._findings.append(finding)
        return self._findings

    def _generate_sqli_payload(self, technique: str, dbms: str) -> str:
        payloads = {
            "union": "' UNION SELECT NULL,NULL,NULL--",
            "blind": "' AND 1=1--",
            "time_based": "' AND SLEEP(5)--",
        }
        return payloads.get(technique, "' OR '1'='1")


class PrivEscChecker:
    """Local privilege escalation detection for multiple platforms."""

    def __init__(self, platform: Platform | str = Platform.LINUX):
        if isinstance(platform, str):
            self.platform = Platform(platform)
        else:
            self.platform = platform

    def enumerate(self, current_user: str = "",
                  kernel_version: str = "",
                  installed_packages: list[str] | None = None,
                  sudo_permissions: str = "",
                  file_permissions: list[str] | None = None,
                  **kwargs) -> list[PrivescVector]:
        vectors: list[PrivescVector] = []
        if self.platform == Platform.LINUX:
            vectors.extend(self._enumerate_linux(
                current_user, kernel_version, sudo_permissions))
        elif self.platform == Platform.WINDOWS:
            vectors.extend(self._enumerate_windows(**kwargs))
        return vectors

    def _enumerate_linux(self, user: str, kernel: str,
                         sudo: str) -> list[PrivescVector]:
        vectors = []
        if "NOPASSWD" in sudo:
            vectors.append(PrivescVector(
                technique=PrivEscTechnique.SUDO_MISCONFIG,
                severity="HIGH",
                requirements="Current user has NOPASSWD sudo",
                reliability="high",
                description="User can run commands as root without password",
                command="sudo -l",
            ))
        if kernel and any(v in kernel for v in ["5.4", "4.15"]):
            vectors.append(PrivescVector(
                technique=PrivEscTechnique.KERNEL_EXPLOIT,
                severity="CRITICAL",
                requirements=f"Kernel {kernel} with known CVEs",
                reliability="medium",
                description=f"Kernel {kernel} may be vulnerable to local privilege escalation",
            ))
        vectors.append(PrivescVector(
            technique=PrivEscTechnique.SUID_BINARY,
            severity="MEDIUM",
            requirements="Writable SUID binaries",
            reliability="medium",
            description="Check for misconfigured SUID binaries via find / -perm -4000",
            command="find / -perm -4000 2>/dev/null",
        ))
        return vectors

    def _enumerate_windows(self, **kwargs) -> list[PrivescVector]:
        return [
            PrivescVector(
                technique=PrivEscTechnique.TOKEN_IMPERSONATION,
                severity="HIGH",
                requirements="SeImpersonatePrivilege enabled",
                reliability="high",
                description="Service accounts with SeImpersonatePrivilege can be exploited via Potato attacks",
                command="whoami /priv",
            ),
            PrivescVector(
                technique=PrivEscTechnique.UNQUOTED_SERVICE_PATH,
                severity="MEDIUM",
                requirements="Unquoted service path with spaces",
                reliability="medium",
                description="Services with unquoted paths may be hijacked",
                command="wmic service get name,pathname",
            ),
        ]


class LateralMover:
    """Network lateral movement toolkit."""

    def __init__(self, session: SessionInfo | None = None):
        self.session = session
        self._credentials: list[Credential] = []
        self._pivot_paths: list[PivotPath] = []

    def harvest_credentials(self, sources: list[str] | None = None) -> list[Credential]:
        sources = sources or ["config_files", "environment_vars"]
        creds = []
        for source in sources:
            creds.append(Credential(
                username="harvested_user", password="",
                source=source, credential_type="discovered",
            ))
        self._credentials.extend(creds)
        return creds

    def find_pivot_paths(self, target_network: str = "",
                         techniques: list[str] | None = None) -> list[PivotPath]:
        techniques = techniques or ["ssh_key", "winrm"]
        paths = []
        for tech_str in techniques:
            tech = PivotTechnique(tech_str) if tech_str in [t.value for t in PivotTechnique] else PivotTechnique.SSH_KEY
            paths.append(PivotPath(
                source=self.session.target if self.session else "current",
                target=target_network,
                technique=tech,
            ))
        self._pivot_paths.extend(paths)
        return paths


class SessionManager:
    """Penetration testing session management."""

    def __init__(self):
        self._sessions: dict[str, SessionInfo] = {}
        self._command_log: list[dict] = []

    def create(self, target: str, session_type: str = "shell",
               persistent: bool = False) -> SessionInfo:
        sid = hashlib.md5(f"{target}{time.time()}".encode()).hexdigest()[:12]
        session = SessionInfo(
            session_id=sid, target=target,
            session_type=SessionType(session_type),
        )
        self._sessions[sid] = session
        return session

    def execute(self, session_id: str, command: str) -> dict:
        session = self._sessions.get(session_id)
        if not session or not session.is_active:
            return {"error": "Session not found or inactive"}
        session.commands_executed += 1
        result = {"command": command, "output": f"Simulated output for: {command}",
                  "timestamp": datetime.utcnow().isoformat()}
        self._command_log.append(result)
        return result

    def cleanup(self, session_id: str, remove_artifacts: bool = True,
                restore_config: bool = True) -> dict:
        session = self._sessions.get(session_id)
        if session:
            session.is_active = False
        return {"cleaned": True, "artifacts_removed": remove_artifacts,
                "config_restored": restore_config}


# ──────────────────────────── Main Engine ─────────────────────

class ReconEngine:
    """Reconnaissance automation engine."""

    def __init__(self, target: str = ""):
        self.target = target
        self._hosts: list[Host] = []
        self._endpoints: list[WebEndpoint] = []
        self._tech_stack: list[str] = []
        self._is_configured = False

    def configure(self, config: dict) -> None:
        self.target = config.get("target", self.target)
        self._is_configured = True

    def run(self) -> ReconReport:
        if not self._is_configured:
            raise RuntimeError("Not configured.")
        return self.get_results()

    def validate(self) -> bool:
        return self._is_configured and bool(self.target)

    def get_status(self) -> dict:
        return {"configured": self._is_configured, "target": self.target,
                "hosts": len(self._hosts), "endpoints": len(self._endpoints)}

    def passive_recon(self, osint_sources: list[str] | None = None,
                      dns_enumeration: bool = True,
                      certificate_transparency: bool = True) -> ReconReport:
        logger.info("Running passive recon on %s", self.target)
        self._hosts.append(Host(ip="0.0.0.0", hostname=self.target,
                                technologies=["nginx", "python"]))
        return self.get_results()

    def active_recon(self, port_scan: str = "top_1000",
                     service_enum: bool = True,
                     web_crawl: bool = True,
                     tech_fingerprint: bool = True) -> ReconReport:
        logger.info("Running active recon on %s", self.target)
        if self._hosts:
            self._hosts[0].ports = [80, 443, 8080]
            self._hosts[0].services = {80: "http", 443: "https", 8080: "http-alt"}
        return self.get_results()

    def get_results(self) -> ReconReport:
        total_ports = sum(len(h.ports) for h in self._hosts)
        return ReconReport(
            hosts=self._hosts, web_endpoints=self._endpoints,
            tech_stack=self._tech_stack,
            total_hosts=len(self._hosts),
            total_ports=total_ports,
            total_endpoints=len(self._endpoints),
        )


class NetworkExploiter:
    """Network service exploitation toolkit."""

    def __init__(self, target: str = ""):
        self.target = target
        self._services: list[dict] = []
        self._vulns: list[dict] = []

    def enumerate_services(self, timeout: int = 30) -> list[dict]:
        self._services = [
            {"port": 22, "service": "ssh", "version": "OpenSSH 8.2"},
            {"port": 80, "service": "http", "version": "Apache 2.4.41"},
            {"port": 445, "service": "smb", "version": "Samba 4.11"},
        ]
        return self._services

    def find_exploitable(self) -> list[dict]:
        self._vulns = [
            {"service": "smb", "port": 445, "cve_id": "CVE-2017-7494",
             "cvss": 9.8, "exploit_module": "samba_is_known_pipename"},
        ]
        return self._vulns

    def exploit(self, vuln: dict, verify_only: bool = True) -> dict:
        return {"success": True, "verified": verify_only,
                "vuln": vuln.get("cve_id", "unknown")}


class NetworkExploiterError(Exception):
    pass


# ──────────────────────────── Demo ────────────────────────────

def main() -> None:
    print("=" * 60)
    print("  Penetration Testing Module — Demo")
    print("=" * 60)

    # Recon
    print("\n[1] Reconnaissance Phase:")
    recon = ReconEngine()
    recon.configure({"target": "example.com"})
    recon.passive_recon(osint_sources=["crt_sh", "shodan"])
    recon.active_recon(port_scan="top_100", service_enum=True)
    report = recon.get_results()
    print(f"    Hosts: {report.total_hosts} | Ports: {report.total_ports}")
    for host in report.hosts:
        print(f"    {host.hostname} ({host.ip}): {host.ports}")

    # Web Exploitation
    print("\n[2] Web Application Testing:")
    web = WebExploiter(target="https://app.example.com", scope=["/api/*"])
    sqli_findings = web.test_sqli(params=["id", "search"])
    xss_findings = web.test_xss(params=["q"])
    print(f"    SQLi findings: {len(sqli_findings)}")
    print(f"    XSS findings: {len(xss_findings)}")
    for f in sqli_findings[:2]:
        print(f"      [{f.vuln_type.value}] {f.technique}: {f.endpoint[:60]}")

    # Privilege Escalation
    print("\n[3] Privilege Escalation Check:")
    checker = PrivEscChecker(platform="linux")
    vectors = checker.enumerate(
        current_user="www-data", kernel_version="5.4.0-91-generic",
        sudo_permissions="www-data ALL=(root) NOPASSWD: /usr/bin/vim",
    )
    for v in vectors:
        print(f"    [{v.severity}] {v.technique.value}: {v.description[:60]}")

    # Lateral Movement
    print("\n[4] Lateral Movement:")
    session = SessionInfo(session_id="demo1", target="10.0.0.5",
                          session_type=SessionType.SHELL)
    mover = LateralMover(session=session)
    creds = mover.harvest_credentials(sources=["config_files"])
    pivots = mover.find_pivot_paths(target_network="10.1.0.0/16",
                                     techniques=["ssh_key", "winrm"])
    print(f"    Credentials harvested: {len(creds)}")
    print(f"    Pivot paths found: {len(pivots)}")
    for p in pivots:
        print(f"      {p.source} → {p.target} via {p.technique.value}")

    # Session Management
    print("\n[5] Session Management:")
    mgr = SessionManager()
    sess = mgr.create(target="10.0.0.5", session_type="meterpreter")
    print(f"    Session created: {sess.session_id}")
    result = mgr.execute(sess.session_id, "sysinfo")
    print(f"    Command executed: {result['command']}")
    mgr.cleanup(sess.session_id)
    print(f"    Cleanup: complete")

    # Network Exploitation
    print("\n[6] Network Service Exploitation:")
    net = NetworkExploiter(target="10.0.0.0/24")
    services = net.enumerate_services()
    vulns = net.find_exploitable()
    print(f"    Services: {len(services)} | Exploitable: {len(vulns)}")
    for v in vulns:
        print(f"      [{v['cve_id']}] {v['service']}:{v['port']} (CVSS {v['cvss']})")

    print("\n" + "=" * 60)
    print("  Demo Complete — Authorized Testing Only")
    print("=" * 60)


if __name__ == "__main__":
    main()
