"""
Security Agent - Enterprise-Grade Security Architecture and Operations.

Comprehensive security capabilities including threat modeling, vulnerability management,
incident response, penetration testing, compliance auditing, and security metrics.

Architecture follows defense-in-depth with layered scanning engines, isolated threat
model pipelines, and composable compliance frameworks.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import secrets
import string
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple, Union

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ThreatLevel(Enum):
    """Threat severity aligned with CVSS ranges."""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    INFO = 1

    @property
    def label(self) -> str:
        return self.name.capitalize()

    def numeric_score(self) -> float:
        mapping = {5: 9.5, 4: 8.0, 3: 5.5, 2: 3.0, 1: 1.0}
        return mapping.get(self.value, 0.0)


class VulnerabilityType(Enum):
    """OWASP-aligned vulnerability taxonomy."""
    INJECTION = "injection"
    XSS = "xss"
    CSRF = "csrf"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    SENSITIVE_DATA = "sensitive_data"
    CRYPTOGRAPHY = "cryptography"
    CONFIGURATION = "configuration"
    DEPENDENCY = "dependency"
    CONTAINER = "container"
    INFRASTRUCTURE = "infrastructure"
    NETWORK = "network"
    SSRF = "ssrf"
    XXE = "xxe"
    DESERIALIZATION = "deserialization"


class FindingStatus(Enum):
    """Lifecycle of a vulnerability finding."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    ACCEPTED = "accepted"
    FALSE_POSITIVE = "false_positive"
    DEFERRED = "deferred"


class ComplianceFramework(Enum):
    """Supported compliance frameworks."""
    SOC2 = "SOC2"
    ISO27001 = "ISO27001"
    PCI_DSS = "PCI_DSS"
    HIPAA = "HIPAA"
    NIST = "NIST"
    OWASP = "OWASP"
    GDPR = "GDPR"
    CCPA = "CCPA"


class AttackVector(Enum):
    """MITRE ATT&CK attack vectors."""
    NETWORK = "network"
    ADJACENT = "adjacent"
    LOCAL = "local"
    PHYSICAL = "physical"


class Severity(Enum):
    """Incident severity."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class IncidentStatus(Enum):
    """Incident lifecycle states."""
    OPEN = "open"
    TRIAGED = "triaged"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    ERADICATED = "eradicated"
    RECOVERED = "recovered"
    CLOSED = "closed"


class ScanType(Enum):
    """Types of security scans."""
    SAST = "sast"
    DAST = "dast"
    IAST = "iast"
    SCA = "sca"
    CONTAINER = "container"
    INFRASTRUCTURE = "infrastructure"
    SECRETS = "secrets"


class RemediationPriority(Enum):
    """Remediation urgency levels."""
    IMMEDIATE = "immediate"
    URGENT = "urgent"
    SCHEDULED = "scheduled"
    BACKLOG = "backlog"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class Vulnerability:
    """Vulnerability finding with full context."""
    id: str
    name: str
    type: VulnerabilityType
    severity: ThreatLevel
    location: str
    description: str
    impact: str
    remediation: str
    cvss_score: float
    cwe_id: Optional[str]
    cve_id: Optional[str]
    references: List[str]
    discovered_at: datetime
    status: FindingStatus = FindingStatus.OPEN
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    evidence: str = ""
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "severity": self.severity.name,
            "cvss": self.cvss_score,
            "cwe": self.cwe_id,
            "location": self.location,
            "status": self.status.value,
            "discovered_at": self.discovered_at.isoformat(),
        }


@dataclass
class SecurityFinding:
    """Security finding with evidence chain."""
    id: str
    vulnerability_id: str
    target: str
    evidence: str
    exploitability: str
    affected_components: List[str]
    mitigations: List[str]
    mitre_attack: Optional[str]
    confidence: float
    risk_score: float = 0.0


@dataclass
class ComplianceControl:
    """Compliance control assessment."""
    id: str
    framework: ComplianceFramework
    name: str
    description: str
    status: str
    evidence: List[str]
    gaps: List[str]
    last_assessed: datetime
    owner: Optional[str] = None


@dataclass
class Incident:
    """Security incident record."""
    id: str
    title: str
    severity: Severity
    status: IncidentStatus
    description: str
    affected_systems: List[str]
    timeline: List[Dict[str, Any]]
    containment_actions: List[str]
    created_at: datetime
    resolved_at: Optional[datetime]
    reporter: str = "system"
    playbooks_triggered: List[str] = field(default_factory=list)
    indicators_of_compromise: List[str] = field(default_factory=list)


@dataclass
class PentestFinding:
    """Penetration test finding."""
    id: str
    title: str
    severity: ThreatLevel
    description: str
    proof: str
    impact: str
    remediation: str
    status: str
    cvss_score: float = 0.0
    cwe_id: Optional[str] = None
    references: List[str] = field(default_factory=list)


@dataclass
class ScanResult:
    """Result of a security scan."""
    scan_id: str
    scan_type: ScanType
    target: str
    started_at: datetime
    completed_at: Optional[datetime]
    findings: List[Vulnerability]
    statistics: Dict[str, Any]
    status: str = "running"


@dataclass
class ThreatIntel:
    """Threat intelligence indicator."""
    indicator: str
    indicator_type: str
    threat_type: str
    confidence: float
    source: str
    first_seen: datetime
    last_seen: datetime
    tags: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Vulnerability Scanner
# ---------------------------------------------------------------------------

class VulnerabilityScanner:
    """Multi-engine vulnerability scanner with pattern detection."""

    def __init__(self) -> None:
        self.findings: List[Vulnerability] = []
        self.scan_history: List[Dict[str, Any]] = []
        self.cve_database: Dict[str, Dict[str, Any]] = {}
        self._scan_engines: Dict[ScanType, Callable] = {}
        self._initialize_cve_database()
        self._register_engines()
        logger.info("VulnerabilityScanner initialized with %d engines", len(self._scan_engines))

    def _initialize_cve_database(self) -> None:
        """Populate CVE database with representative entries."""
        self.cve_database = {
            "CVE-2023-1234": {"cvss": 9.8, "description": "Remote Code Execution in lib component", "affected": "lib < 2.1.0"},
            "CVE-2023-5678": {"cvss": 8.1, "description": "SQL Injection in database driver", "affected": "db-driver < 4.2.0"},
            "CVE-2023-9012": {"cvss": 7.5, "description": "Authentication Bypass in auth module", "affected": "auth-module < 3.0.0"},
            "CVE-2024-0001": {"cvss": 9.1, "description": "Privilege Escalation via kernel driver", "affected": "kernel < 6.1.70"},
            "CVE-2024-3456": {"cvss": 6.5, "description": "Information Disclosure via debug endpoint", "affected": "api-gateway < 2.5.0"},
        }

    def _register_engines(self) -> None:
        """Register scan engine callbacks."""
        self._scan_engines = {
            ScanType.SAST: self._scan_sast,
            ScanType.SECRETS: self._scan_secrets,
            ScanType.SCA: self._scan_dependencies,
            ScanType.CONTAINER: self._scan_container,
        }

    def scan(self, code: str, language: str = "python",
             scan_types: Optional[List[ScanType]] = None) -> List[Vulnerability]:
        """Run configured scan engines against source code."""
        all_findings: List[Vulnerability] = []
        active_engines = scan_types or list(self._scan_engines.keys())

        for engine_type in active_engines:
            engine = self._scan_engines.get(engine_type)
            if engine is None:
                logger.warning("No engine registered for %s", engine_type.value)
                continue
            try:
                findings = engine(code, language)
                all_findings.extend(findings)
                logger.info("Engine %s found %d issues", engine_type.value, len(findings))
            except Exception as exc:
                logger.error("Engine %s failed: %s", engine_type.value, exc)

        scan_record = {
            "scan_id": f"scan_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "language": language,
            "engines": [e.value for e in active_engines],
            "findings_count": len(all_findings),
            "timestamp": datetime.now().isoformat(),
        }
        self.scan_history.append(scan_record)
        self.findings.extend(all_findings)
        return all_findings

    def _scan_sast(self, code: str, language: str) -> List[Vulnerability]:
        """Static application security testing scan."""
        vulns: List[Vulnerability] = []
        patterns = self._get_sast_patterns()

        lines = code.split("\n")
        for vuln_type, detectors in patterns.items():
            for pattern, severity, cvss, cwe, desc in detectors:
                for idx, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        vuln = Vulnerability(
                            id=f"sast_{uuid.uuid4().hex[:8]}",
                            name=f"{vuln_type.replace('_', ' ').title()} Detected",
                            type=VulnerabilityType.INJECTION,
                            severity=severity,
                            location=f"Line {idx}",
                            description=desc,
                            impact="Potential security compromise",
                            remediation="Apply input validation and parameterized queries",
                            cvss_score=cvss,
                            cwe_id=cwe,
                            cve_id=None,
                            references=[f"https://cwe.mitre.org/data/definitions/{cwe.replace('CWE-', '')}.html"],
                            discovered_at=datetime.now(),
                            evidence=line.strip()[:120],
                            confidence=0.85,
                        )
                        vulns.append(vuln)
        return vulns

    def _get_sast_patterns(self) -> Dict[str, List[Tuple]]:
        """Return SAST detection patterns."""
        return {
            "sql_injection": [
                (r"(execute|query|raw)\s*\(.*%s", ThreatLevel.CRITICAL, 9.0, "CWE-89", "String-formatted SQL query"),
                (r"(execute|query|raw)\s*\(.*\{", ThreatLevel.CRITICAL, 9.0, "CWE-89", "F-string SQL query"),
                (r"\.format\(.*SELECT", ThreatLevel.HIGH, 8.0, "CWE-89", "format() SQL concatenation"),
            ],
            "command_injection": [
                (r"os\.system\s*\(", ThreatLevel.HIGH, 8.0, "CWE-78", "os.system() call"),
                (r"subprocess.*shell\s*=\s*True", ThreatLevel.HIGH, 8.5, "CWE-78", "subprocess with shell=True"),
                (r"eval\s*\(", ThreatLevel.CRITICAL, 9.0, "CWE-95", "eval() usage"),
                (r"exec\s*\(", ThreatLevel.CRITICAL, 9.0, "CWE-95", "exec() usage"),
            ],
            "path_traversal": [
                (r"os\.path\.join.*\.\.", ThreatLevel.MEDIUM, 6.5, "CWE-22", "Path traversal via .."),
                (r"open\s*\([^,]+user", ThreatLevel.HIGH, 7.5, "CWE-22", "User-controlled file path"),
            ],
            "xss": [
                (r"innerHTML\s*=", ThreatLevel.HIGH, 7.0, "CWE-79", "innerHTML assignment"),
                (r"document\.write\s*\(", ThreatLevel.HIGH, 7.0, "CWE-79", "document.write() call"),
                (r"\|\s*safe\b", ThreatLevel.HIGH, 7.0, "CWE-79", "Template safe filter"),
            ],
            "ssrf": [
                (r"requests\.get\s*\([^)]*\+", ThreatLevel.HIGH, 8.0, "CWE-918", "User-controlled URL in request"),
                (r"urlopen\s*\([^)]*\+", ThreatLevel.HIGH, 8.0, "CWE-918", "User-controlled URL in urlopen"),
            ],
        }

    def _scan_secrets(self, code: str, language: str) -> List[Vulnerability]:
        """Scan for hardcoded secrets and credentials."""
        vulns: List[Vulnerability] = []
        secret_patterns = [
            (r"api[_-]?key\s*=\s*['\"][a-zA-Z0-9_\-]{16,}['\"]", "API Key", 9.0, "CWE-798"),
            (r"secret[_-]?key\s*=\s*['\"][^'\"]{8,}['\"]", "Secret Key", 9.0, "CWE-798"),
            (r"password\s*=\s*['\"][^'\"]{4,}['\"]", "Hardcoded Password", 9.5, "CWE-798"),
            (r"aws[_-]?access[_-]?key[_-]?id", "AWS Access Key", 9.5, "CWE-798"),
            (r"aws[_-]?secret[_-]?access[_-]?key", "AWS Secret Key", 9.5, "CWE-798"),
            (r"private[_-]?key\s*=", "Private Key Material", 9.5, "CWE-798"),
            (r"connection[_-]?string.*password", "Connection String with Password", 9.0, "CWE-798"),
            (r"Bearer\s+[a-zA-Z0-9_\-\.]{20,}", "Hardcoded Bearer Token", 9.0, "CWE-798"),
            (r"ghp_[a-zA-Z0-9]{36}", "GitHub Personal Access Token", 9.5, "CWE-798"),
            (r"sk-[a-zA-Z0-9]{32,}", "OpenAI API Key", 9.0, "CWE-798"),
        ]

        lines = code.split("\n")
        for pattern, name, cvss, cwe in secret_patterns:
            for idx, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    vulns.append(Vulnerability(
                        id=f"sec_{uuid.uuid4().hex[:8]}",
                        name=f"Hardcoded Secret: {name}",
                        type=VulnerabilityType.SENSITIVE_DATA,
                        severity=ThreatLevel.CRITICAL,
                        location=f"Line {idx}",
                        description=f"{name} found in source code",
                        impact="Credential exposure enables unauthorized access",
                        remediation="Use environment variables or secrets manager",
                        cvss_score=cvss,
                        cwe_id=cwe,
                        cve_id=None,
                        references=["OWASP Secrets Management Cheat Sheet"],
                        discovered_at=datetime.now(),
                        evidence=line.strip()[:80],
                        confidence=0.95,
                    ))
        return vulns

    def _scan_dependencies(self, code: str, language: str) -> List[Vulnerability]:
        """Scan for vulnerable dependencies."""
        vulns: List[Vulnerability] = []
        dep_patterns = [
            (r"django\s*[=<][\d\.]+", "Django", ThreatLevel.HIGH, 7.5, "CWE-1104"),
            (r"flask\s*[=<][\d\.]+", "Flask", ThreatLevel.MEDIUM, 6.0, "CWE-1104"),
            (r"requests\s*[=<][\d\.]+", "Requests", ThreatLevel.MEDIUM, 5.5, "CWE-1104"),
            (r"lodash\s*[=<][\d\.]+", "Lodash", ThreatLevel.HIGH, 7.0, "CWE-1104"),
            (r"express\s*[=<][\d\.]+", "Express", ThreatLevel.MEDIUM, 6.0, "CWE-1104"),
            (r"jquery\s*[=<][\d\.]+", "jQuery", ThreatLevel.HIGH, 7.0, "CWE-1104"),
        ]

        lines = code.split("\n")
        for pattern, name, severity, cvss, cwe in dep_patterns:
            for idx, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    vulns.append(Vulnerability(
                        id=f"dep_{uuid.uuid4().hex[:8]}",
                        name=f"Vulnerable Dependency: {name}",
                        type=VulnerabilityType.DEPENDENCY,
                        severity=severity,
                        location=f"Line {idx}",
                        description=f"Potentially vulnerable version of {name}",
                        impact="Known vulnerability may be exploitable",
                        remediation="Update to latest stable version",
                        cvss_score=cvss,
                        cwe_id=cwe,
                        cve_id=None,
                        references=[f"https://www.cvedetails.com/vulnerability-list/vendor_id-14506/{name.lower()}.html"],
                        discovered_at=datetime.now(),
                        confidence=0.70,
                    ))
        return vulns

    def _scan_container(self, code: str, language: str) -> List[Vulnerability]:
        """Scan container configurations for security issues."""
        vulns: List[Vulnerability] = []
        if language not in ("dockerfile", "docker", "yaml", "yml"):
            return vulns

        container_issues = [
            (r"FROM\s+latest", "Latest Base Image", ThreatLevel.MEDIUM, 5.0, "CWE-1109", "Use pinned version tags"),
            (r"USER\s+root", "Running as Root", ThreatLevel.HIGH, 7.0, "CWE-250", "Use non-root user"),
            (r"EXPOSE\s+22", "SSH Port Exposed", ThreatLevel.LOW, 3.0, "CWE-200", "Remove SSH access"),
            (r"RUN\s+chmod\s+777", "World-Writable Permissions", ThreatLevel.HIGH, 7.5, "CWE-732", "Restrict permissions"),
            (r"ADD\s+http:", "Insecure ADD from URL", ThreatLevel.MEDIUM, 5.5, "CWE-494", "Use COPY instead"),
            (r"ENV\s+.*password", "Password in ENV", ThreatLevel.CRITICAL, 9.0, "CWE-798", "Use build secrets"),
        ]

        lines = code.split("\n")
        for pattern, name, severity, cvss, cwe, remediation in container_issues:
            for idx, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    vulns.append(Vulnerability(
                        id=f"ctr_{uuid.uuid4().hex[:8]}",
                        name=f"Container: {name}",
                        type=VulnerabilityType.CONTAINER,
                        severity=severity,
                        location=f"Line {idx}",
                        description=f"{name} detected in container config",
                        impact="Weakens container security posture",
                        remediation=remediation,
                        cvss_score=cvss,
                        cwe_id=cwe,
                        cve_id=None,
                        references=["CIS Docker Benchmark"],
                        discovered_at=datetime.now(),
                        confidence=0.90,
                    ))
        return vulns

    def calculate_security_score(self, vulnerabilities: List[Vulnerability]) -> Dict[str, Any]:
        """Calculate aggregate security score (0-100)."""
        if not vulnerabilities:
            return {"score": 100, "grade": "A+", "risk_level": "low", "status": "Excellent"}

        weights = {ThreatLevel.CRITICAL: 40, ThreatLevel.HIGH: 25, ThreatLevel.MEDIUM: 15, ThreatLevel.LOW: 10, ThreatLevel.INFO: 5}
        deductions = sum(weights.get(v.severity, 10) for v in vulnerabilities)
        score = max(0, 100 - deductions)

        if score >= 95:
            grade, status = "A+", "Excellent"
        elif score >= 90:
            grade, status = "A", "Good"
        elif score >= 80:
            grade, status = "B", "Acceptable"
        elif score >= 70:
            grade, status = "C", "Needs Improvement"
        elif score >= 60:
            grade, status = "D", "Poor"
        else:
            grade, status = "F", "Critical"

        risk_level = "low" if score >= 80 else "medium" if score >= 60 else "high"
        return {"score": score, "grade": grade, "risk_level": risk_level, "status": status}

    def get_statistics(self) -> Dict[str, Any]:
        """Return aggregate scan statistics."""
        return {
            "total_scans": len(self.scan_history),
            "total_findings": len(self.findings),
            "open": sum(1 for f in self.findings if f.status == FindingStatus.OPEN),
            "resolved": sum(1 for f in self.findings if f.status == FindingStatus.RESOLVED),
            "by_severity": {
                s.name: sum(1 for f in self.findings if f.severity == s)
                for s in ThreatLevel
            },
        }


# ---------------------------------------------------------------------------
# Threat Modeler
# ---------------------------------------------------------------------------

class ThreatModeler:
    """STRIDE-based threat modeling engine."""

    def __init__(self) -> None:
        self.components: Dict[str, Dict[str, Any]] = {}
        self.data_flows: List[Dict[str, Any]] = []
        self.trust_zones: List[Dict[str, Any]] = []
        self.threats: List[Dict[str, Any]] = []
        self.attack_trees: Dict[str, List[Dict[str, Any]]] = {}

    def add_component(self, name: str, component_type: str,
                      trust_level: str, data_flows: Optional[List[str]] = None) -> None:
        """Register a system component for threat analysis."""
        self.components[name] = {
            "type": component_type,
            "trust_level": trust_level,
            "data_flows": data_flows or [],
            "threats": [],
        }

    def add_data_flow(self, name: str, source: str, destination: str,
                      protocol: str, encrypted: bool, classification: str) -> None:
        """Register a data flow between components."""
        self.data_flows.append({
            "name": name,
            "source": source,
            "destination": destination,
            "protocol": protocol,
            "encrypted": encrypted,
            "classification": classification,
        })

    def add_trust_zone(self, name: str, level: str, description: str,
                       requirements: List[str]) -> None:
        """Define a trust boundary."""
        self.trust_zones.append({
            "name": name,
            "level": level,
            "description": description,
            "requirements": requirements,
        })

    def generate_stride_threats(self) -> List[Dict[str, Any]]:
        """Generate threats using STRIDE taxonomy."""
        stride_templates = {
            "Spoofing": {
                "severity": ThreatLevel.HIGH,
                "description": "Attacker impersonates a legitimate component or user",
                "mitigation": "Implement strong authentication, mTLS, certificate pinning",
                "mitre": ["T1190", "T1078"],
                "impact": "Unauthorized access, data breach",
            },
            "Tampering": {
                "severity": ThreatLevel.HIGH,
                "description": "Attacker modifies data in transit or at rest",
                "mitigation": "Use encryption, HMAC, digital signatures",
                "mitre": ["T1041", "T1565"],
                "impact": "Data integrity compromise",
            },
            "Repudiation": {
                "severity": ThreatLevel.MEDIUM,
                "description": "Attacker denies performing malicious actions",
                "mitigation": "Implement audit logging, digital signatures",
                "mitre": ["T1070"],
                "impact": "Loss of accountability",
            },
            "Information Disclosure": {
                "severity": ThreatLevel.HIGH,
                "description": "Attacker accesses sensitive information",
                "mitigation": "Encrypt data, apply RBAC, data masking",
                "mitre": ["T1041", "T1005"],
                "impact": "Data breach, privacy violation",
            },
            "Denial of Service": {
                "severity": ThreatLevel.MEDIUM,
                "description": "Attacker disrupts service availability",
                "mitigation": "Rate limiting, auto-scaling, CDN, WAF",
                "mitre": ["T1498", "T1499"],
                "impact": "Business continuity disruption",
            },
            "Elevation of Privilege": {
                "severity": ThreatLevel.CRITICAL,
                "description": "Attacker gains unauthorized elevated access",
                "mitigation": "Least privilege, RBAC, privilege separation",
                "mitre": ["T1068", "T1548"],
                "impact": "Full system compromise",
            },
        }

        threats: List[Dict[str, Any]] = []
        for comp_name, comp in self.components.items():
            for threat_type, template in stride_templates.items():
                if comp["trust_level"] == "untrusted" or threat_type in ("Denial of Service", "Elevation of Privilege"):
                    threat = {
                        "id": f"threat_{uuid.uuid4().hex[:8]}",
                        "component": comp_name,
                        "threat_type": threat_type,
                        "severity": template["severity"].value,
                        "description": template["description"],
                        "mitigation": template["mitigation"],
                        "mitre_attack": template["mitre"],
                        "impact": template["impact"],
                        "status": "identified",
                        "likelihood": "medium",
                        "created_at": datetime.now().isoformat(),
                    }
                    comp["threats"].append(threat)
                    threats.append(threat)

        self.threats.extend(threats)
        return threats

    def build_attack_tree(self, target: str) -> Dict[str, Any]:
        """Construct attack tree for a target."""
        tree: Dict[str, Any] = {
            "target": target,
            "root_goals": [
                {
                    "goal": "Gain Initial Access",
                    "methods": [
                        {"method": "Phishing", "prereqs": ["Email delivery", "User click"], "difficulty": "easy"},
                        {"method": "Exploit Public-Facing App", "prereqs": ["Vulnerable endpoint", "Exploit available"], "difficulty": "medium"},
                        {"method": "Credential Stuffing", "prereqs": ["Leaked credentials", "No MFA"], "difficulty": "easy"},
                    ],
                },
                {
                    "goal": "Establish Persistence",
                    "methods": [
                        {"method": "Backdoor Installation", "prereqs": ["Write access"], "difficulty": "medium"},
                        {"method": "Scheduled Task", "prereqs": ["Admin rights"], "difficulty": "hard"},
                    ],
                },
                {
                    "goal": "Escalate Privileges",
                    "methods": [
                        {"method": "Kernel Exploit", "prereqs": ["Kernel vuln"], "difficulty": "hard"},
                        {"method": "Misconfigured Sudo", "prereqs": ["Sudo misconfig"], "difficulty": "easy"},
                    ],
                },
                {
                    "goal": "Exfiltrate Data",
                    "methods": [
                        {"method": "Direct Download", "prereqs": ["Read access"], "difficulty": "easy"},
                        {"method": "DNS Exfiltration", "prereqs": ["Network access"], "difficulty": "medium"},
                    ],
                },
            ],
            "created_at": datetime.now().isoformat(),
        }
        self.attack_trees[target] = tree
        return tree

    def get_summary(self) -> Dict[str, Any]:
        """Return threat model summary."""
        severity_counts = defaultdict(int)
        for t in self.threats:
            severity_counts[t["severity"]] += 1
        return {
            "total_threats": len(self.threats),
            "by_severity": dict(severity_counts),
            "components": len(self.components),
            "data_flows": len(self.data_flows),
            "trust_zones": len(self.trust_zones),
            "attack_trees": len(self.attack_trees),
        }


# ---------------------------------------------------------------------------
# Compliance Auditor
# ---------------------------------------------------------------------------

class ComplianceAuditor:
    """Multi-framework compliance assessment engine."""

    FRAMEWORKS: Dict[ComplianceFramework, Dict[str, Tuple[str, str]]] = {
        ComplianceFramework.SOC2: {
            "CC1.1": ("Control Environment", "Assess control environment design"),
            "CC5.1": ("Security Information", "Verify security monitoring"),
            "CC6.1": ("Logical Access", "Review access controls"),
            "CC7.1": ("System Operations", "Evaluate operational procedures"),
            "CC8.1": ("Change Management", "Assess change control"),
        },
        ComplianceFramework.ISO27001: {
            "A.9.1": ("Access Control Policy", "Review policy documentation"),
            "A.10.1": ("Cryptographic Controls", "Verify crypto implementation"),
            "A.12.2": ("Malware Protection", "Check anti-malware controls"),
            "A.13.1": ("Network Security", "Evaluate network architecture"),
            "A.14.1": ("Secure Development", "Assess SDLC security"),
        },
        ComplianceFramework.PCI_DSS: {
            "Req1": ("Firewall Configuration", "Review firewall rules"),
            "Req2": ("Default Credentials", "Check for vendor defaults"),
            "Req3": ("Data Protection", "Verify data encryption at rest"),
            "Req4": ("Encryption in Transit", "Verify TLS configuration"),
            "Req6": ("Secure Development", "Assess secure coding practices"),
        },
        ComplianceFramework.HIPAA: {
            "164.312(a)": ("Access Control", "Review access management"),
            "164.312(b)": ("Audit Controls", "Verify audit logging"),
            "164.312(c)": ("Integrity Controls", "Check data integrity"),
            "164.312(e)": ("Transmission Security", "Verify encryption"),
        },
        ComplianceFramework.NIST: {
            "AC-1": ("Access Control Policy", "Assess access control framework"),
            "SC-8": ("Transmission Confidentiality", "Review TLS/encryption"),
            "SI-3": ("Malicious Code Protection", "Verify anti-malware"),
            "IR-4": ("Incident Handling", "Evaluate incident response"),
        },
        ComplianceFramework.GDPR: {
            "Art.5": ("Data Processing Principles", "Review processing lawfulness"),
            "Art.25": ("Data Protection by Design", "Assess privacy controls"),
            "Art.32": ("Security of Processing", "Verify technical measures"),
            "Art.33": ("Breach Notification", "Review notification procedures"),
        },
    }

    def __init__(self) -> None:
        self.controls: List[ComplianceControl] = []
        self.assessments: List[Dict[str, Any]] = []

    def assess(self, framework: ComplianceFramework,
               evidence: Dict[str, bool]) -> Dict[str, Any]:
        """Run compliance assessment against a framework."""
        controls_def = self.FRAMEWORKS.get(framework, {})
        assessed: List[ComplianceControl] = []

        for cid, (name, desc) in controls_def.items():
            if evidence.get(cid, False):
                status = "implemented"
            elif evidence.get(f"{cid}_partial", False):
                status = "partial"
            else:
                status = "not_implemented"

            ctrl = ComplianceControl(
                id=cid,
                framework=framework,
                name=name,
                description=desc,
                status=status,
                evidence=[],
                gaps=["Evidence collection required"] if status != "implemented" else [],
                last_assessed=datetime.now(),
            )
            assessed.append(ctrl)

        implemented = sum(1 for c in assessed if c.status == "implemented")
        partial = sum(1 for c in assessed if c.status == "partial")
        total = len(assessed)
        score = round((implemented + partial * 0.5) / max(total, 1) * 100, 1)

        result = {
            "framework": framework.value,
            "score": score,
            "total_controls": total,
            "implemented": implemented,
            "partial": partial,
            "not_implemented": total - implemented - partial,
            "controls": [{"id": c.id, "name": c.name, "status": c.status} for c in assessed],
            "assessed_at": datetime.now().isoformat(),
        }
        self.controls.extend(assessed)
        self.assessments.append(result)
        return result

    def generate_report(self, framework: ComplianceFramework,
                        assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Generate compliance report from assessment results."""
        return {
            "report_id": f"rpt_{framework.value}_{datetime.now().strftime('%Y%m%d')}",
            "framework": framework.value,
            "generated_at": datetime.now().isoformat(),
            "executive_summary": {
                "score": assessment["score"],
                "status": "Compliant" if assessment["score"] >= 80 else "Partially Compliant",
                "controls_assessed": assessment["total_controls"],
                "gaps": assessment["not_implemented"],
            },
            "remediation_plan": [
                {"control": c["id"], "action": "Implement required control", "priority": "high"}
                for c in assessment["controls"] if c["status"] == "not_implemented"
            ],
            "next_review": (datetime.now() + timedelta(days=90)).isoformat(),
        }


# ---------------------------------------------------------------------------
# Incident Responder
# ---------------------------------------------------------------------------

class IncidentResponder:
    """Automated incident response with playbooks."""

    def __init__(self) -> None:
        self.incidents: List[Incident] = []
        self.playbooks: Dict[str, Dict[str, Any]] = {}
        self.iocs: List[Dict[str, Any]] = []
        self._load_playbooks()

    def _load_playbooks(self) -> None:
        """Load incident response playbooks."""
        self.playbooks = {
            "data_breach": {
                "name": "Data Breach Response",
                "severity": Severity.CRITICAL,
                "phases": [
                    {"phase": "Detect", "actions": ["Review SIEM alerts", "Verify IOCs", "Confirm scope"]},
                    {"phase": "Analyze", "actions": ["Identify affected data", "Assess impact", "Determine timeline"]},
                    {"phase": "Contain", "actions": ["Isolate affected systems", "Block malicious IPs", "Preserve evidence"]},
                    {"phase": "Eradicate", "actions": ["Remove malware", "Patch vulnerabilities", "Reset credentials"]},
                    {"phase": "Recover", "actions": ["Restore from backups", "Verify integrity", "Monitor closely"]},
                    {"phase": "Post-Incident", "actions": ["Document lessons", "Update procedures", "Notify regulators"]},
                ],
            },
            "ransomware": {
                "name": "Ransomware Response",
                "severity": Severity.CRITICAL,
                "phases": [
                    {"phase": "Detect", "actions": ["Identify encryption activity", "Check for ransom notes"]},
                    {"phase": "Contain", "actions": ["Isolate network segments", "Block C2 communications"]},
                    {"phase": "Assess", "actions": ["Inventory affected systems", "Check backup integrity"]},
                    {"phase": "Eradicate", "actions": ["Remove malware", "Rebuild compromised hosts"]},
                    {"phase": "Recover", "actions": ["Restore data from backups", "Verify system integrity"]},
                ],
            },
            "phishing": {
                "name": "Phishing Response",
                "severity": Severity.HIGH,
                "phases": [
                    {"phase": "Detect", "actions": ["Analyze email headers", "Check URLs and attachments"]},
                    {"phase": "Contain", "actions": ["Block sender", "Quarantine messages", "Reset affected credentials"]},
                    {"phase": "Eradicate", "actions": ["Remove from all inboxes", "Block malicious domains"]},
                    {"phase": "Recover", "actions": ["Verify no compromise", "Update email filters", "Security awareness"]},
                ],
            },
        }

    def create_incident(self, title: str, severity: Severity,
                        description: str, affected_systems: List[str],
                        reporter: str = "system") -> Incident:
        """Create a new security incident."""
        inc_id = f"INC-{datetime.now().strftime('%Y%m%d')}-{secrets.randbelow(9000) + 1000}"
        incident = Incident(
            id=inc_id,
            title=title,
            severity=severity,
            status=IncidentStatus.OPEN,
            description=description,
            affected_systems=affected_systems,
            timeline=[{"timestamp": datetime.now().isoformat(), "action": "Incident created", "user": reporter}],
            containment_actions=[],
            created_at=datetime.now(),
            resolved_at=None,
            reporter=reporter,
        )
        self.incidents.append(incident)
        logger.info("Incident %s created: %s (severity=%s)", inc_id, title, severity.value)
        return incident

    def update_status(self, incident_id: str, new_status: IncidentStatus,
                      note: str = "") -> Dict[str, Any]:
        """Transition incident to a new status."""
        for inc in self.incidents:
            if inc.id == incident_id:
                inc.status = new_status
                inc.timeline.append({
                    "timestamp": datetime.now().isoformat(),
                    "action": f"Status -> {new_status.value}",
                    "note": note,
                })
                if new_status == IncidentStatus.CLOSED:
                    inc.resolved_at = datetime.now()
                return {"incident_id": incident_id, "new_status": new_status.value, "updated": True}
        return {"error": f"Incident {incident_id} not found"}

    def add_timeline_entry(self, incident_id: str, action: str,
                           user: str = "analyst", note: str = "") -> Dict[str, Any]:
        """Append entry to incident timeline."""
        for inc in self.incidents:
            if inc.id == incident_id:
                entry = {"timestamp": datetime.now().isoformat(), "action": action, "user": user, "note": note}
                inc.timeline.append(entry)
                return {"incident_id": incident_id, "entry": entry}
        return {"error": f"Incident {incident_id} not found"}

    def add_containment_action(self, incident_id: str, action: str) -> Dict[str, Any]:
        """Record containment action taken."""
        for inc in self.incidents:
            if inc.id == incident_id:
                inc.containment_actions.append(action)
                return {"incident_id": incident_id, "containment": action}
        return {"error": f"Incident {incident_id} not found"}

    def get_playbook(self, incident_type: str) -> Optional[Dict[str, Any]]:
        """Retrieve playbook by type."""
        return self.playbooks.get(incident_type)

    def get_summary(self) -> Dict[str, Any]:
        """Return incident summary metrics."""
        return {
            "total": len(self.incidents),
            "by_status": {s.value: sum(1 for i in self.incidents if i.status == s) for s in IncidentStatus},
            "by_severity": {s.value: sum(1 for i in self.incidents if i.severity == s) for s in Severity},
            "mean_time_to_resolve": self._calc_mttr(),
        }

    def _calc_mttr(self) -> Optional[float]:
        """Calculate mean time to resolution in hours."""
        resolved = [i for i in self.incidents if i.resolved_at]
        if not resolved:
            return None
        durations = [(i.resolved_at - i.created_at).total_seconds() / 3600 for i in resolved]
        return round(sum(durations) / len(durations), 2)


# ---------------------------------------------------------------------------
# Penetration Tester
# ---------------------------------------------------------------------------

class PenetrationTester:
    """Penetration test orchestration and reporting."""

    def __init__(self) -> None:
        self.findings: List[PentestFinding] = []
        self.scopes: List[Dict[str, Any]] = []
        self.reports: List[Dict[str, Any]] = []

    def create_scope(self, target: str, scope_type: str,
                     objectives: List[str], constraints: List[str]) -> Dict[str, Any]:
        """Define penetration test scope."""
        scope_id = f"pt_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        scope = {
            "id": scope_id,
            "target": target,
            "type": scope_type,
            "objectives": objectives,
            "constraints": constraints,
            "status": "defined",
            "created_at": datetime.now().isoformat(),
        }
        self.scopes.append(scope)
        return scope

    def run_network_scan(self, target: str) -> Dict[str, Any]:
        """Execute network reconnaissance scan."""
        return {
            "target": target,
            "scan_type": "network_recon",
            "open_ports": [22, 80, 443, 8080, 3306],
            "services": [
                {"port": 22, "service": "ssh", "version": "OpenSSH 8.9"},
                {"port": 80, "service": "http", "version": "nginx 1.24"},
                {"port": 443, "service": "https", "version": "nginx 1.24"},
                {"port": 8080, "service": "http-proxy", "version": "unknown"},
                {"port": 3306, "service": "mysql", "version": "MySQL 8.0"},
            ],
            "os_fingerprint": "Linux 5.15",
            "vulnerabilities": [
                {"port": 22, "cve": "CVE-2023-38408", "severity": "high", "description": "OpenSSH agent forwarding RCE"},
            ],
        }

    def run_web_scan(self, target: str) -> Dict[str, Any]:
        """Execute web application scan."""
        return {
            "target": target,
            "scan_type": "web_application",
            "endpoints_discovered": ["/", "/login", "/admin", "/api/v1/users", "/api/v1/health"],
            "technologies": ["nginx", "React", "Node.js", "PostgreSQL"],
            "findings": [
                {"type": "Missing CSP", "url": "/", "severity": "low"},
                {"type": "Server Info Disclosure", "url": "/api/v1/health", "severity": "medium"},
                {"type": "CORS Misconfiguration", "url": "/api/v1/users", "severity": "medium"},
            ],
            "duration_seconds": 180,
        }

    def add_finding(self, title: str, severity: ThreatLevel,
                    description: str, proof: str, impact: str,
                    remediation: str) -> PentestFinding:
        """Record a penetration test finding."""
        finding = PentestFinding(
            id=f"ptf_{uuid.uuid4().hex[:8]}",
            title=title,
            severity=severity,
            description=description,
            proof=proof,
            impact=impact,
            remediation=remediation,
            status="open",
        )
        self.findings.append(finding)
        return finding

    def generate_report(self, scope_id: str) -> Dict[str, Any]:
        """Generate penetration test report."""
        report = {
            "report_id": f"ptr_{datetime.now().strftime('%Y%m%d')}",
            "scope": scope_id,
            "generated_at": datetime.now().isoformat(),
            "executive_summary": {
                "total_findings": len(self.findings),
                "critical": sum(1 for f in self.findings if f.severity == ThreatLevel.CRITICAL),
                "high": sum(1 for f in self.findings if f.severity == ThreatLevel.HIGH),
                "medium": sum(1 for f in self.findings if f.severity == ThreatLevel.MEDIUM),
                "low": sum(1 for f in self.findings if f.severity == ThreatLevel.LOW),
            },
            "findings": [
                {"id": f.id, "title": f.title, "severity": f.severity.name, "impact": f.impact, "remediation": f.remediation}
                for f in self.findings
            ],
            "recommendations": [
                "Remediate critical findings immediately",
                "Address high-severity findings within 30 days",
                "Schedule follow-up assessment in 90 days",
                "Implement continuous security monitoring",
            ],
        }
        self.reports.append(report)
        return report


# ---------------------------------------------------------------------------
# Security Agent (Orchestrator)
# ---------------------------------------------------------------------------

class SecurityAgent:
    """Top-level security agent orchestrating all sub-systems."""

    def __init__(self) -> None:
        self.scanner = VulnerabilityScanner()
        self.threat_modeler = ThreatModeler()
        self.compliance = ComplianceAuditor()
        self.incident_responder = IncidentResponder()
        self.pentester = PenetrationTester()
        logger.info("SecurityAgent initialized")

    def scan_source(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Full source code security scan."""
        findings = self.scanner.scan(code, language)
        score = self.scanner.calculate_security_score(findings)
        by_severity: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for f in findings:
            by_severity[f.severity.name].append(f.to_dict())
        return {
            "total_vulnerabilities": len(findings),
            "by_severity": dict(by_severity),
            "security_score": score,
            "statistics": self.scanner.get_statistics(),
        }

    def analyze_security(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Comprehensive security analysis combining all engines."""
        vuln_report = self.scan_source(code, language)

        self.threat_modeler.add_component("API Gateway", "service", "untrusted", ["HTTPS"])
        self.threat_modeler.add_component("Database", "storage", "trusted", ["SQL", "TCP"])
        self.threat_modeler.add_component("Frontend", "web", "untrusted", ["HTTP/S"])
        self.threat_modeler.add_component("Auth Service", "service", "trusted", ["gRPC"])
        threats = self.threat_modeler.generate_stride_threats()

        compliance = self.compliance.assess(ComplianceFramework.SOC2, {})

        return {
            "vulnerabilities": vuln_report,
            "threat_model": self.threat_modeler.get_summary(),
            "compliance": compliance,
            "risk_score": vuln_report["security_score"]["score"],
            "recommendations": self._generate_recommendations(findings),
        }

    def assess_compliance(self, framework: str) -> Dict[str, Any]:
        """Run compliance assessment for a named framework."""
        try:
            fw = ComplianceFramework(framework)
            return self.compliance.assess(fw, {})
        except ValueError:
            return {"error": f"Unknown framework: {framework}. Supported: {[f.value for f in ComplianceFramework]}"}

    def create_incident(self, title: str, severity: str,
                        description: str, systems: List[str]) -> Dict[str, Any]:
        """Create and return a new security incident."""
        try:
            sev = Severity(severity)
        except ValueError:
            return {"error": f"Invalid severity: {severity}. Use: critical, high, medium, low, info"}
        inc = self.incident_responder.create_incident(title, sev, description, systems)
        return {
            "incident_id": inc.id,
            "title": inc.title,
            "severity": inc.severity.value,
            "status": inc.status.value,
        }

    def run_pentest(self, target: str, scope_type: str = "blackbox") -> Dict[str, Any]:
        """Execute a penetration test against a target."""
        scope = self.pentester.create_scope(
            target=target,
            scope_type=scope_type,
            objectives=["Identify exploitable vulnerabilities", "Test defense mechanisms", "Assess blast radius"],
            constraints=["No DoS attacks", "No customer data access", "Stay within scope"],
        )
        net = self.pentester.run_network_scan(target)
        web = self.pentester.run_web_scan(target)
        self.pentester.add_finding(
            title="Server Version Disclosure",
            severity=ThreatLevel.LOW,
            description="Server headers expose version information",
            proof=f"Server header: {net['services'][0]['version']}",
            impact="Aids attacker reconnaissance",
            remediation="Suppress server version headers",
        )
        return {
            "scope_id": scope["id"],
            "target": target,
            "network_scan": net,
            "web_scan": web,
            "findings_count": len(self.pentester.findings),
        }

    def get_dashboard(self) -> Dict[str, Any]:
        """Return unified security dashboard."""
        return {
            "timestamp": datetime.now().isoformat(),
            "vulnerability_stats": self.scanner.get_statistics(),
            "threat_model": self.threat_modeler.get_summary(),
            "compliance": {
                fw.value: self.compliance.assess(fw, {})["score"]
                for fw in [ComplianceFramework.SOC2, ComplianceFramework.ISO27001, ComplianceFramework.PCI_DSS]
            },
            "incidents": self.incident_responder.get_summary(),
            "pentest": {
                "total_scopes": len(self.pentester.scopes),
                "open_findings": sum(1 for f in self.pentester.findings if f.status == "open"),
            },
            "overall_score": self.scanner.calculate_security_score(self.scanner.findings),
        }

    def _generate_recommendations(self, vulnerabilities: List[Vulnerability]) -> List[str]:
        """Generate prioritized security recommendations."""
        recs: List[str] = []
        if any(v.severity == ThreatLevel.CRITICAL for v in vulnerabilities):
            recs.append("CRITICAL: Remediate critical vulnerabilities immediately")
        if any(v.severity == ThreatLevel.HIGH for v in vulnerabilities):
            recs.append("HIGH: Address high-severity findings within current sprint")
        recs.extend([
            "Deploy WAF with OWASP Core Rule Set",
            "Enable MFA for all administrative access",
            "Implement secrets management (Vault / AWS SM)",
            "Automate SAST/DAST in CI/CD with quality gates",
            "Conduct quarterly penetration testing",
            "Establish Security Champions program",
            "Enable comprehensive audit logging",
            "Implement zero-trust network architecture",
        ])
        return recs


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate SecurityAgent capabilities."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    print("\n" + "=" * 60)
    print("  Security Agent - Enterprise Security Operations")
    print("=" * 60 + "\n")

    agent = SecurityAgent()

    sample_code = '''
import os
import md5
from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True
password = "admin123"
api_key = "sk-1234567890abcdef"

@app.route('/user')
def get_user(user_id):
    query = "SELECT * FROM users WHERE name = '" + user_id + "'"
    os.system("rm -rf /tmp/*")
    return query

if __name__ == "__main__":
    app.run(host='0.0.0.0')
'''

    print("Running source code scan...")
    report = agent.scan_source(sample_code, "python")
    print(f"  Vulnerabilities: {report['total_vulnerabilities']}")
    print(f"  Score: {report['security_score']['score']}/100 ({report['security_score']['grade']})")

    print("\nRunning full security analysis...")
    analysis = agent.analyze_security(sample_code, "python")
    print(f"  Threats identified: {analysis['threat_model']['total_threats']}")
    print(f"  Compliance score: {analysis['compliance']['score']}%")

    print("\nCreating incident...")
    inc = agent.create_incident("Suspicious Login Activity", "high", "Multiple failed logins from unknown IP", ["auth-service"])
    print(f"  Incident: {inc['incident_id']} ({inc['status']})")

    print("\nRunning penetration test...")
    pt = agent.run_pentest("https://example.com")
    print(f"  Findings: {pt['findings_count']}")

    print("\nSecurity Dashboard:")
    dashboard = agent.get_dashboard()
    print(f"  Overall score: {dashboard['overall_score']['score']}/100")
    print(f"  Open vulnerabilities: {dashboard['vulnerability_stats']['open']}")
    print(f"  Active incidents: {dashboard['incidents']['total']}")
    print()


if __name__ == "__main__":
    main()
