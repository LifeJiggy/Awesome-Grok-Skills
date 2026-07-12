"""
Penetration Testing Framework Module

Provides structured methodology and tooling for authorized security assessments.
Covers the full lifecycle of a professional penetration test from scope
reconnaissance through exploitation, post-exploitation, and reporting.

This module is designed for authorized red team operators conducting
engagements against defined scopes with proper documentation.
"""

from __future__ import annotations

import hashlib
import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from pathlib import Path
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Severity(Enum):
    """Vulnerability severity levels aligned with CVSS."""
    INFO = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class PhaseStatus(Enum):
    """Status of a penetration testing phase."""
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    BLOCKED = auto()
    FAILED = auto()


class AccessLevel(Enum):
    """Access level achieved during exploitation."""
    NONE = auto()
    LOW_USER = auto()
    STANDARD_USER = auto()
    PRIVILEGED_USER = auto()
    LOCAL_ADMIN = auto()
    DOMAIN_ADMIN = auto()
    SYSTEM = auto()


class AttackSurface(Enum):
    """Categories of attack surface."""
    NETWORK = auto()
    WEB_APPLICATION = auto()
    MOBILE = auto()
    CLOUD = auto()
    PHYSICAL = auto()
    SOCIAL = auto()


class ScanProfile(Enum):
    """Predefined scanning profiles."""
    QUICK = "quick"
    MODERATE = "moderate"
    THOROUGH = "thorough"
    AGGRESSIVE = "aggressive"


class ExploitStrategy(Enum):
    """Exploitation strategy levels."""
    SAFE = "safe"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Scope:
    """Defines the authorized scope for a penetration test."""
    target_domains: list[str]
    excluded_hosts: list[str] = field(default_factory=list)
    ip_ranges: list[str] = field(default_factory=list)
    ports: str = "1-65535"
    rules_of_engagement: dict[str, Any] = field(default_factory=dict)

    def is_in_scope(self, target: str) -> bool:
        """Check if a target is within the authorized scope."""
        for excluded in self.excluded_hosts:
            if target == excluded or target.endswith(f".{excluded}"):
                return False
        for domain in self.target_domains:
            if domain.startswith("*."):
                base = domain[2:]
                if target == base or target.endswith(f".{base}"):
                    return True
            elif target == domain:
                return True
        return False

    def validate_authorization(self) -> bool:
        """Validate that scope has required authorization fields."""
        roe = self.rules_of_engagement
        required = ["testing_window", "emergency_contact"]
        return all(field in roe for field in required)


@dataclass
class Engagement:
    """Represents a complete penetration test engagement."""
    name: str
    client: str
    authorizer: str
    scope: Scope
    start_date: str
    end_date: str
    engagement_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: PhaseStatus = PhaseStatus.NOT_STARTED

    @property
    def duration_days(self) -> int:
        start = datetime.strptime(self.start_date, "%Y-%m-%d")
        end = datetime.strptime(self.end_date, "%Y-%m-%d")
        return (end - start).days

    def is_active(self) -> bool:
        now = datetime.utcnow()
        start = datetime.strptime(self.start_date, "%Y-%m-%d")
        end = datetime.strptime(self.end_date, "%Y-%m-%d")
        return start <= now <= end


@dataclass
class Vulnerability:
    """Represents a discovered vulnerability."""
    title: str
    description: str
    target: str
    severity: Severity
    cvss_score: float
    cwe_id: str
    cve_id: Optional[str] = None
    evidence_path: Optional[str] = None
    remediation: Optional[str] = None
    found_at: datetime = field(default_factory=datetime.utcnow)
    vuln_id: str = field(default_factory=lambda: f"VULN-{uuid.uuid4().hex[:6].upper()}")
    verified: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.vuln_id,
            "title": self.title,
            "severity": self.severity.name,
            "cvss": self.cvss_score,
            "cwe": self.cwe_id,
            "target": self.target,
            "verified": self.verified,
        }


@dataclass
class ExploitResult:
    """Result of an exploitation attempt."""
    vulnerability: Vulnerability
    success: bool
    access_level: AccessLevel = AccessLevel.NONE
    session_id: Optional[str] = None
    evidence_path: Optional[str] = None
    error_message: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Session:
    """Active exploitation session for post-exploitation."""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    compromised_host: str = ""
    current_user: str = ""
    access_level: AccessLevel = AccessLevel.NONE
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True


@dataclass
class ReconResult:
    """Results from reconnaissance phase."""
    subdomains: list[str] = field(default_factory=list)
    services: list[dict[str, Any]] = field(default_factory=list)
    technologies: list[str] = field(default_factory=list)
    live_hosts: list[str] = field(default_factory=list)
    email_addresses: list[str] = field(default_factory=list)
    credentials: list[dict[str, str]] = field(default_factory=list)


@dataclass
class Finding:
    """Consolidated finding for reporting."""
    finding_id: str = field(default_factory=lambda: f"FIND-{uuid.uuid4().hex[:6].upper()}")
    title: str = ""
    severity: Severity = Severity.INFO
    description: str = ""
    impact: str = ""
    remediation: str = ""
    evidence: list[str] = field(default_factory=list)
    cvss_score: float = 0.0
    cwe_id: str = ""
    affected_assets: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Core Engine Classes
# ---------------------------------------------------------------------------

class PenetrationTestEngine:
    """Main engine orchestrating the penetration test lifecycle."""

    def __init__(self, engagement: Engagement):
        self.engagement = engagement
        self.phases: dict[str, PhaseStatus] = {
            "reconnaissance": PhaseStatus.NOT_STARTED,
            "scanning": PhaseStatus.NOT_STARTED,
            "exploitation": PhaseStatus.NOT_STARTED,
            "post_exploitation": PhaseStatus.NOT_STARTED,
            "reporting": PhaseStatus.NOT_STARTED,
        }
        self.vulnerabilities: list[Vulnerability] = []
        self.findings: list[Finding] = []
        self.sessions: list[Session] = []
        self.evidence_dir: Path = Path("./evidence")
        self.logger = logging.getLogger("pentest_engine")
        self._config: dict[str, Any] = {}

    def configure(self, aggressiveness: str = "moderate",
                  max_concurrent_tasks: int = 10,
                  evidence_storage: str = "./evidence",
                  log_level: str = "verbose") -> None:
        """Configure the penetration test engine."""
        self._config = {
            "aggressiveness": aggressiveness,
            "max_concurrent_tasks": max_concurrent_tasks,
            "evidence_storage": evidence_storage,
            "log_level": log_level,
        }
        self.evidence_dir = Path(evidence_storage)
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        level = getattr(logging, log_level.upper(), logging.INFO)
        logging.basicConfig(level=level)
        self.logger.info("Engine configured: %s", self._config)

    def validate_scope(self, target: str) -> bool:
        """Validate that a target is within the authorized scope."""
        if not self.engagement.scope.is_in_scope(target):
            self.logger.warning("OUT OF SCOPE: %s", target)
            return False
        if not self.engagement.is_active():
            self.logger.warning("Engagement is not currently active")
            return False
        return True

    def start_phase(self, phase_name: str) -> None:
        """Mark a phase as in progress."""
        if phase_name not in self.phases:
            raise ValueError(f"Unknown phase: {phase_name}")
        self.phases[phase_name] = PhaseStatus.IN_PROGRESS
        self.logger.info("Phase '%s' started", phase_name)

    def complete_phase(self, phase_name: str) -> None:
        """Mark a phase as completed."""
        if phase_name not in self.phases:
            raise ValueError(f"Unknown phase: {phase_name}")
        self.phases[phase_name] = PhaseStatus.COMPLETED
        self.logger.info("Phase '%s' completed", phase_name)

    def add_vulnerability(self, vuln: Vulnerability) -> None:
        """Add a discovered vulnerability."""
        self.vulnerabilities.append(vuln)
        self.logger.info("Vulnerability added: %s [%s]", vuln.title, vuln.severity.name)

    def add_finding(self, finding: Finding) -> None:
        """Add a consolidated finding."""
        self.findings.append(finding)

    def get_status(self) -> dict[str, Any]:
        """Get current status of the penetration test."""
        return {
            "engagement": self.engagement.name,
            "client": self.engagement.client,
            "phases": {k: v.name for k, v in self.phases.items()},
            "vulnerabilities_found": len(self.vulnerabilities),
            "findings": len(self.findings),
            "active_sessions": sum(1 for s in self.sessions if s.is_active),
            "severity_breakdown": self._severity_breakdown(),
        }

    def _severity_breakdown(self) -> dict[str, int]:
        breakdown = {s.name: 0 for s in Severity}
        for vuln in self.vulnerabilities:
            breakdown[vuln.severity.name] += 1
        return breakdown

    def generate_report(self, format: str = "markdown") -> str:
        """Generate a penetration test report."""
        lines = [
            f"# Penetration Test Report",
            f"## Engagement: {self.engagement.name}",
            f"**Client:** {self.engagement.client}",
            f"**Authorizer:** {self.engagement.authorizer}",
            f"**Period:** {self.engagement.start_date} to {self.engagement.end_date}",
            "",
            "## Executive Summary",
            f"This assessment identified **{len(self.vulnerabilities)} vulnerabilities** "
            f"across the following severity levels:",
            "",
        ]
        for sev, count in self._severity_breakdown().items():
            if count > 0:
                lines.append(f"- **{sev}:** {count}")
        lines.extend(["", "## Findings", ""])
        for finding in self.findings:
            lines.extend([
                f"### {finding.finding_id}: {finding.title}",
                f"**Severity:** {finding.severity.name} (CVSS: {finding.cvss_score})",
                f"**CWE:** {finding.cwe_id}",
                f"**Description:** {finding.description}",
                f"**Impact:** {finding.impact}",
                f"**Remediation:** {finding.remediation}",
                "",
            ])
        return "\n".join(lines)


class ReconPhase:
    """Reconnaissance phase of a penetration test."""

    def __init__(self, engine: PenetrationTestEngine):
        self.engine = engine
        self.logger = logging.getLogger("recon_phase")

    def passive_recon(self, targets: list[dict[str, Any]],
                      tools: list[str] | None = None) -> ReconResult:
        """Execute passive reconnaissance against targets."""
        self.engine.start_phase("reconnaissance")
        result = ReconResult()
        self.logger.info("Starting passive recon with tools: %s", tools or [])
        for target in targets:
            domain = target.get("domain", "")
            result.subdomains.extend(self._enumerate_subdomains(domain))
            result.technologies.extend(self._detect_technologies(domain))
            result.email_addresses.extend(self._harvest_emails(domain))
        self.logger.info(
            "Passive recon complete: %d subdomains, %d technologies",
            len(result.subdomains), len(result.technologies),
        )
        return result

    def active_recon(self, targets: list[str],
                     techniques: list[str] | None = None) -> ReconResult:
        """Execute active reconnaissance against live targets."""
        result = ReconResult()
        self.logger.info("Starting active recon against %d targets", len(targets))
        for target in targets:
            if not self.engine.validate_scope(target):
                continue
            services = self._scan_services(target)
            result.services.extend(services)
            result.live_hosts.append(target)
        self.logger.info("Active recon complete: %d live hosts", len(result.live_hosts))
        return result

    def build_attack_surface(self, passive: ReconResult,
                             active: ReconResult,
                             output_format: str = "graph") -> dict[str, Any]:
        """Build consolidated attack surface map."""
        surface = {
            "total_subdomains": len(passive.subdomains),
            "live_hosts": len(active.live_hosts),
            "services": len(active.services),
            "technologies": passive.technologies,
            "attack_vectors": [],
        }
        for service in active.services:
            if service.get("port") in [80, 443, 8080, 8443]:
                surface["attack_vectors"].append("web_application")
            if service.get("port") in [22, 3389]:
                surface["attack_vectors"].append("remote_access")
            if service.get("port") in [445, 139]:
                surface["attack_vectors"].append("smb")
        return surface

    def _enumerate_subdomains(self, domain: str) -> list[str]:
        self.logger.info("Enumerating subdomains for %s", domain)
        return [f"sub{i}.{domain}" for i in range(1, 4)]

    def _detect_technologies(self, domain: str) -> list[str]:
        self.logger.info("Detecting technologies for %s", domain)
        return ["nginx/1.18", "PHP/8.1", "WordPress/6.4"]

    def _harvest_emails(self, domain: str) -> list[str]:
        self.logger.info("Harvesting emails for %s", domain)
        return [f"admin@{domain}", f"info@{domain}"]

    def _scan_services(self, target: str) -> list[dict[str, Any]]:
        self.logger.info("Scanning services on %s", target)
        return [
            {"port": 80, "service": "http", "version": "nginx/1.18"},
            {"port": 443, "service": "https", "version": "nginx/1.18"},
            {"port": 22, "service": "ssh", "version": "OpenSSH_8.9"},
        ]


class VulnScanPhase:
    """Vulnerability scanning phase."""

    def __init__(self, engine: PenetrationTestEngine):
        self.engine = engine
        self.logger = logging.getLogger("vulnscan_phase")

    def run(self, profile: dict[str, Any]) -> ReconResult:
        """Run vulnerability scan with specified profile."""
        self.engine.start_phase("scanning")
        self.logger.info("Running vuln scan: %s", profile.get("name", "default"))
        result = ReconResult()
        self.logger.info("Scan complete")
        return result

    def add_vulnerability(self, title: str, target: str, severity: Severity,
                          cvss: float, cwe: str) -> Vulnerability:
        """Create and register a vulnerability."""
        vuln = Vulnerability(
            title=title,
            description=f"Automated scan finding: {title}",
            target=target,
            severity=severity,
            cvss_score=cvss,
            cwe_id=cwe,
        )
        self.engine.add_vulnerability(vuln)
        return vuln

    def generate_report(self, format: str = "markdown",
                        include_remediation: bool = True,
                        risk_matrix: bool = True) -> str:
        """Generate vulnerability scan report."""
        lines = ["# Vulnerability Scan Report", ""]
        for vuln in self.engine.vulnerabilities:
            lines.extend([
                f"## {vuln.vuln_id}: {vuln.title}",
                f"- **Severity:** {vuln.severity.name}",
                f"- **CVSS:** {vuln.cvss_score}",
                f"- **Target:** {vuln.target}",
                "",
            ])
        return "\n".join(lines)


class ExploitPhase:
    """Exploitation phase of a penetration test."""

    def __init__(self, engine: PenetrationTestEngine):
        self.engine = engine
        self.logger = logging.getLogger("exploit_phase")

    def validate_target(self, target: str,
                        scope_check: bool = True,
                        authorization_check: bool = True,
                        previous_findings_check: bool = True) -> bool:
        """Validate that a target is safe to exploit."""
        if scope_check and not self.engine.validate_scope(target):
            return False
        if authorization_check and not self.engine.engagement.scope.validate_authorization():
            self.logger.error("Authorization validation failed")
            return False
        return True

    def exploit(self, findings: list[Vulnerability],
                strategy: str = "safe",
                documentation: bool = True,
                evidence_capture: bool = True) -> list[ExploitResult]:
        """Attempt exploitation of discovered vulnerabilities."""
        self.engine.start_phase("exploitation")
        results = []
        for vuln in findings:
            self.logger.info("Attempting exploit: %s", vuln.title)
            result = ExploitResult(
                vulnerability=vuln,
                success=False,
                evidence_path=f"./evidence/{vuln.vuln_id}" if evidence_capture else None,
            )
            if strategy == ExploitStrategy.SAFE.value:
                result.success = vuln.severity.value >= Severity.HIGH.value
            elif strategy == ExploitStrategy.MODERATE.value:
                result.success = vuln.severity.value >= Severity.MEDIUM.value
            else:
                result.success = True
            if result.success:
                result.access_level = AccessLevel.STANDARD_USER
                result.session_id = str(uuid.uuid4())[:8]
                self.logger.info("Exploit succeeded: %s -> session %s",
                                 vuln.title, result.session_id)
            results.append(result)
        return results

    def create_session(self, result: ExploitResult) -> Session:
        """Create a post-exploitation session from a successful exploit."""
        session = Session(
            session_id=result.session_id or str(uuid.uuid4())[:8],
            compromised_host=result.vulnerability.target,
            current_user="user",
            access_level=result.access_level,
        )
        self.engine.sessions.append(session)
        return session


class PostExploitPhase:
    """Post-exploitation phase."""

    def __init__(self, engine: PenetrationTestEngine, session: Session | None = None):
        self.engine = engine
        self.session = session
        self.logger = logging.getLogger("postexploit_phase")

    def privesc_enumeration(self, techniques: list[str] | None = None) -> dict[str, Any]:
        """Enumerate privilege escalation vectors."""
        self.engine.start_phase("post_exploitation")
        self.logger.info("Enumerating privesc vectors: %s", techniques)
        return {
            "vectors": [
                {"type": "suid_binary", "path": "/usr/bin/find", "risk": "high"},
                {"type": "sudo_misconfig", "detail": "NOPASSWD ALL", "risk": "critical"},
            ],
            "total_vectors": 2,
        }

    def credential_harvest(self, methods: list[str] | None = None,
                           output_path: str = "./credentials/") -> list[dict[str, str]]:
        """Harvest credentials from compromised host."""
        self.logger.info("Harvesting credentials via: %s", methods)
        return [{"type": "password", "source": "config_file", "hash": "redacted"}]

    def lateral_movement(self, target_network: str,
                         methods: list[str] | None = None,
                         pivot_through: str = "") -> list[dict[str, Any]]:
        """Attempt lateral movement to other hosts."""
        self.logger.info("Lateral movement to %s via %s", target_network, methods)
        return [{"host": "10.0.0.5", "method": "pass_the_hash", "success": True}]

    def simulate_exfiltration(self, target_data: str,
                              method: str = "dns_tunneling",
                              size_limit_mb: int = 50,
                              stealth: bool = True) -> dict[str, Any]:
        """Simulate data exfiltration."""
        self.logger.info("Simulating exfiltration: %s via %s", target_data, method)
        return {
            "method": method,
            "data_simulated_mb": size_limit_mb,
            "stealth_mode": stealth,
            "detection_bypassed": True,
        }


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def calculate_cvss(vector: dict[str, str]) -> float:
    """Calculate CVSS score from vector components (simplified)."""
    base_scores = {
        "AV:N": 0.85, "AV:A": 0.62, "AV:L": 0.55, "AV:P": 0.20,
        "AC:L": 0.77, "AC:H": 0.44,
        "PR:N": 0.85, "PR:L": 0.62, "PR:H": 0.27,
        "UI:N": 0.85, "UI:R": 0.62,
    }
    score = sum(base_scores.get(v, 0.5) for v in vector.values())
    return round(min(score / max(len(vector), 1) * 10, 10.0), 1)


def generate_evidence_hash(file_path: str) -> str:
    """Generate SHA-256 hash of evidence file for integrity."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return "file_not_found"


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the penetration testing framework."""
    print("=" * 60)
    print("  Penetration Testing Framework - Demo")
    print("=" * 60)

    # Create scope and engagement
    scope = Scope(
        target_domains=["example.com", "*.example.com"],
        excluded_hosts=["10.0.0.1"],
        ip_ranges=["192.168.1.0/24"],
        rules_of_engagement={
            "testing_window": "2024-01-15 to 2024-02-15",
            "emergency_contact": "+1-555-0199",
        },
    )

    engagement = Engagement(
        name="ACME Corp External Penetration Test",
        client="ACME Corporation",
        authorizer="Jane Smith, CISO",
        scope=scope,
        start_date="2024-01-15",
        end_date="2024-12-31",
    )

    # Initialize engine
    engine = PenetrationTestEngine(engagement)
    engine.configure(
        aggressiveness="moderate",
        evidence_storage="./demo_evidence",
        log_level="info",
    )

    # Recon phase
    recon = ReconPhase(engine)
    passive = recon.passive_recon(
        targets=[{"domain": "example.com"}],
        tools=["subfinder", "amass"],
    )
    active = recon.active_recon(targets=passive.subdomains[:2])
    surface = recon.build_attack_surface(passive, active)
    print(f"\nAttack surface: {json.dumps(surface, indent=2)}")

    # Vulnerability scanning
    scan = VulnScanPhase(engine)
    scan.add_vulnerability("SQL Injection in Login", "app.example.com",
                           Severity.CRITICAL, 9.8, "CWE-89")
    scan.add_vulnerability("Reflected XSS in Search", "app.example.com",
                           Severity.MEDIUM, 6.1, "CWE-79")

    # Exploitation
    exploit = ExploitPhase(engine)
    is_valid = exploit.validate_target("app.example.com")
    print(f"\nTarget validation: {'PASS' if is_valid else 'FAIL'}")

    results = exploit.exploit(
        findings=engine.vulnerabilities,
        strategy="safe",
    )
    for r in results:
        print(f"Exploit {r.vulnerability.title}: {'SUCCESS' if r.success else 'FAILED'}")

    # Post-exploitation
    successful = [r for r in results if r.success]
    if successful:
        session = exploit.create_session(successful[0])
        post = PostExploitPhase(engine, session)
        privesc = post.privesc_enumeration()
        creds = post.credential_harvest()
        lateral = post.lateral_movement("10.0.0.0/24")
        exfil = post.simulate_exfiltration("simulated_pii")
        print(f"\nPrivesc vectors: {privesc['total_vectors']}")
        print(f"Credentials harvested: {len(creds)}")
        print(f"Lateral movement targets: {len(lateral)}")
        print(f"Exfiltration: {exfil['method']} ({exfil['data_simulated_mb']}MB)")

    # Generate report
    engine.complete_phase("reconnaissance")
    engine.complete_phase("scanning")
    engine.complete_phase("exploitation")
    engine.complete_phase("post_exploitation")
    engine.complete_phase("reporting")

    report = engine.generate_report()
    print(f"\n{report}")

    # Status
    status = engine.get_status()
    print(f"\nFinal status: {json.dumps(status, indent=2)}")


if __name__ == "__main__":
    main()
