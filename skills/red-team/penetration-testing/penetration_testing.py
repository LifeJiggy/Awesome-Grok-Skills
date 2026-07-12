"""
Penetration Testing Framework
A comprehensive framework for conducting authorized security assessments
of systems, networks, and applications.
"""

import asyncio
import logging
import hashlib
import json
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Set
from abc import ABC, abstractmethod
import ipaddress
import re
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScanType(Enum):
    """Enumeration of available scan types."""
    PASSIVE = "passive"
    ACTIVE = "active"
    AGGRESSIVE = "aggressive"
    STEALTH = "stealth"


class Severity(Enum):
    """Vulnerability severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class TestStatus(Enum):
    """Status of testing operations."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TestingMethodology(Enum):
    """Testing methodology types."""
    BLACK_BOX = "black_box"
    WHITE_BOX = "white_box"
    GRAY_BOX = "gray_box"


@dataclass
class Target:
    """Represents a testing target."""
    host: str
    port_range: str = "1-65535"
    description: str = ""
    excluded_ports: List[int] = field(default_factory=list)
    credentials: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate target after initialization."""
        if not self.host:
            raise ValueError("Target host cannot be empty")
        
        # Validate IP or hostname
        try:
            ipaddress.ip_address(self.host)
        except ValueError:
            # Check if it's a valid hostname
            if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*$', self.host):
                raise ValueError(f"Invalid target host: {self.host}")


@dataclass
class Vulnerability:
    """Represents a discovered vulnerability."""
    id: str
    title: str
    description: str
    severity: Severity
    cvss_score: float
    cve_id: Optional[str] = None
    affected_component: str = ""
    proof_of_concept: str = ""
    remediation: str = ""
    references: List[str] = field(default_factory=list)
    discovered_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Validate vulnerability data."""
        if not 0 <= self.cvss_score <= 10:
            raise ValueError(f"CVSS score must be between 0 and 10, got {self.cvss_score}")


@dataclass
class ScanResult:
    """Results from a scanning operation."""
    target: Target
    scan_type: ScanType
    start_time: datetime
    end_time: Optional[datetime] = None
    status: TestStatus = TestStatus.PENDING
    open_ports: List[int] = field(default_factory=list)
    services: Dict[int, Dict[str, str]] = field(default_factory=dict)
    vulnerabilities: List[Vulnerability] = field(default_factory=list)
    raw_output: str = ""
    
    @property
    def duration(self) -> Optional[timedelta]:
        """Calculate scan duration."""
        if self.end_time and self.start_time:
            return self.end_time - self.start_time
        return None
    
    @property
    def vulnerability_count(self) -> Dict[Severity, int]:
        """Count vulnerabilities by severity."""
        counts = {severity: 0 for severity in Severity}
        for vuln in self.vulnerabilities:
            counts[vuln.severity] += 1
        return counts


class Scanner(ABC):
    """Abstract base class for scanners."""
    
    @abstractmethod
    async def scan(self, target: Target) -> ScanResult:
        """Perform scanning operation."""
        pass
    
    @abstractmethod
    def validate_target(self, target: Target) -> bool:
        """Validate target before scanning."""
        pass


class NetworkScanner(Scanner):
    """Network scanning and discovery."""
    
    def __init__(self, scan_type: ScanType = ScanType.ACTIVE):
        self.scan_type = scan_type
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 5432, 3306]
    
    def validate_target(self, target: Target) -> bool:
        """Validate target for network scanning."""
        try:
            ipaddress.ip_address(target.host)
            return True
        except ValueError:
            return False
    
    async def scan(self, target: Target) -> ScanResult:
        """Perform network scan."""
        result = ScanResult(
            target=target,
            scan_type=self.scan_type,
            start_time=datetime.now(),
            status=TestStatus.RUNNING
        )
        
        try:
            # Simulate network scanning
            logger.info(f"Starting {self.scan_type.value} scan on {target.host}")
            
            # Discover open ports
            open_ports = await self._discover_ports(target)
            result.open_ports = open_ports
            
            # Enumerate services
            services = await self._enumerate_services(target, open_ports)
            result.services = services
            
            result.status = TestStatus.COMPLETED
            result.end_time = datetime.now()
            
            logger.info(f"Scan completed: {len(open_ports)} open ports found")
            
        except Exception as e:
            result.status = TestStatus.FAILED
            result.raw_output = str(e)
            logger.error(f"Scan failed: {e}")
        
        return result
    
    async def _discover_ports(self, target: Target) -> List[int]:
        """Discover open ports on target."""
        # Simulate port discovery with common ports
        discovered_ports = []
        
        for port in self.common_ports:
            # Simulate port check (in real implementation, this would use socket)
            if await self._check_port(target.host, port):
                discovered_ports.append(port)
        
        return discovered_ports
    
    async def _check_port(self, host: str, port: int) -> bool:
        """Check if a specific port is open."""
        # Simulate port check with some randomness
        import random
        return random.random() > 0.7  # 30% chance port is open
    
    async def _enumerate_services(self, target: Target, ports: List[int]) -> Dict[int, Dict[str, str]]:
        """Enumerate services on open ports."""
        services = {}
        service_map = {
            21: {"service": "FTP", "version": "vsftpd 2.3.4"},
            22: {"service": "SSH", "version": "OpenSSH 7.6"},
            23: {"service": "Telnet", "version": "Linux telnetd"},
            25: {"service": "SMTP", "version": "Postfix smtpd"},
            53: {"service": "DNS", "version": "ISC BIND 9.11"},
            80: {"service": "HTTP", "version": "Apache/2.4.29"},
            110: {"service": "POP3", "version": "Dovecot pop3d"},
            143: {"service": "IMAP", "version": "Dovecot imapd"},
            443: {"service": "HTTPS", "version": "Apache/2.4.29"},
            993: {"service": "IMAPS", "version": "Dovecot imapd"},
            995: {"service": "POP3S", "version": "Dovecot pop3d"},
            3306: {"service": "MySQL", "version": "MySQL 5.7.25"},
            3389: {"service": "RDP", "version": "Microsoft Terminal Services"},
            5432: {"service": "PostgreSQL", "version": "PostgreSQL 10.6"}
        }
        
        for port in ports:
            if port in service_map:
                services[port] = service_map[port]
        
        return services


class VulnerabilityScanner(Scanner):
    """Vulnerability scanning and assessment."""
    
    def __init__(self, scan_profiles: List[str] = None):
        self.scan_profiles = scan_profiles or ["OWASP_Top_10"]
        self.vulnerability_database = self._load_vulnerability_database()
    
    def _load_vulnerability_database(self) -> Dict[str, List[Dict]]:
        """Load vulnerability database."""
        # Simulated vulnerability database
        return {
            "web": [
                {
                    "id": "VULN-001",
                    "title": "SQL Injection",
                    "severity": Severity.CRITICAL,
                    "cvss_score": 9.8,
                    "description": "SQL injection vulnerability in login form",
                    "remediation": "Use parameterized queries and input validation"
                },
                {
                    "id": "VULN-002",
                    "title": "Cross-Site Scripting (XSS)",
                    "severity": Severity.HIGH,
                    "cvss_score": 7.5,
                    "description": "Reflected XSS in search functionality",
                    "remediation": "Implement input sanitization and output encoding"
                }
            ],
            "network": [
                {
                    "id": "VULN-003",
                    "title": "Weak SSH Configuration",
                    "severity": Severity.MEDIUM,
                    "cvss_score": 5.3,
                    "description": "SSH server supports weak ciphers",
                    "remediation": "Disable weak ciphers and use strong encryption"
                }
            ]
        }
    
    def validate_target(self, target: Target) -> bool:
        """Validate target for vulnerability scanning."""
        return bool(target.host)
    
    async def scan(self, target: Target) -> ScanResult:
        """Perform vulnerability scan."""
        result = ScanResult(
            target=target,
            scan_type=ScanType.ACTIVE,
            start_time=datetime.now(),
            status=TestStatus.RUNNING
        )
        
        try:
            logger.info(f"Starting vulnerability scan on {target.host}")
            
            # Perform vulnerability assessment
            vulnerabilities = await self._assess_vulnerabilities(target)
            result.vulnerabilities = vulnerabilities
            
            result.status = TestStatus.COMPLETED
            result.end_time = datetime.now()
            
            logger.info(f"Vulnerability scan completed: {len(vulnerabilities)} vulnerabilities found")
            
        except Exception as e:
            result.status = TestStatus.FAILED
            result.raw_output = str(e)
            logger.error(f"Vulnerability scan failed: {e}")
        
        return result
    
    async def _assess_vulnerabilities(self, target: Target) -> List[Vulnerability]:
        """Assess vulnerabilities on target."""
        vulnerabilities = []
        
        # Check for web vulnerabilities if HTTP services are present
        if target.port_range and ("80" in target.port_range or "443" in target.port_range):
            web_vulns = await self._scan_web_vulnerabilities(target)
            vulnerabilities.extend(web_vulns)
        
        # Check for network vulnerabilities
        network_vulns = await self._scan_network_vulnerabilities(target)
        vulnerabilities.extend(network_vulns)
        
        return vulnerabilities
    
    async def _scan_web_vulnerabilities(self, target: Target) -> List[Vulnerability]:
        """Scan for web application vulnerabilities."""
        vulnerabilities = []
        
        # Simulate web vulnerability scanning
        for vuln_data in self.vulnerability_database.get("web", []):
            vulnerability = Vulnerability(
                id=vuln_data["id"],
                title=vuln_data["title"],
                description=vuln_data["description"],
                severity=vuln_data["severity"],
                cvss_score=vuln_data["cvss_score"],
                affected_component=f"http://{target.host}",
                remediation=vuln_data["remediation"]
            )
            vulnerabilities.append(vulnerability)
        
        return vulnerabilities
    
    async def _scan_network_vulnerabilities(self, target: Target) -> List[Vulnerability]:
        """Scan for network vulnerabilities."""
        vulnerabilities = []
        
        # Simulate network vulnerability scanning
        for vuln_data in self.vulnerability_database.get("network", []):
            vulnerability = Vulnerability(
                id=vuln_data["id"],
                title=vuln_data["title"],
                description=vuln_data["description"],
                severity=vuln_data["severity"],
                cvss_score=vuln_data["cvss_score"],
                affected_component=target.host,
                remediation=vuln_data["remediation"]
            )
            vulnerabilities.append(vulnerability)
        
        return vulnerabilities


class WebAppTester:
    """Web application security testing."""
    
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.session = None
        self.test_results = []
    
    async def test_sql_injection(self) -> List[Vulnerability]:
        """Test for SQL injection vulnerabilities."""
        vulnerabilities = []
        
        # Common SQL injection payloads
        payloads = [
            "' OR '1'='1",
            "admin'--",
            "' UNION SELECT * FROM users--",
            "1; DROP TABLE users--"
        ]
        
        # Simulate SQL injection testing
        for payload in payloads:
            # In real implementation, this would send HTTP requests
            logger.info(f"Testing SQL injection payload: {payload}")
            
            # Simulate finding a vulnerability
            if "UNION" in payload:
                vulnerability = Vulnerability(
                    id=f"SQLI-{hashlib.md5(payload.encode()).hexdigest()[:8]}",
                    title="SQL Injection Vulnerability",
                    description=f"SQL injection found with payload: {payload}",
                    severity=Severity.CRITICAL,
                    cvss_score=9.8,
                    affected_component=self.target_url,
                    proof_of_concept=f"Payload: {payload}",
                    remediation="Use parameterized queries and input validation"
                )
                vulnerabilities.append(vulnerability)
        
        return vulnerabilities
    
    async def test_xss(self) -> List[Vulnerability]:
        """Test for cross-site scripting vulnerabilities."""
        vulnerabilities = []
        
        # Common XSS payloads
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')"
        ]
        
        # Simulate XSS testing
        for payload in payloads:
            logger.info(f"Testing XSS payload: {payload}")
            
            # Simulate finding a vulnerability
            if "onerror" in payload or "onload" in payload:
                vulnerability = Vulnerability(
                    id=f"XSS-{hashlib.md5(payload.encode()).hexdigest()[:8]}",
                    title="Cross-Site Scripting Vulnerability",
                    description=f"XSS found with payload: {payload}",
                    severity=Severity.HIGH,
                    cvss_score=7.5,
                    affected_component=self.target_url,
                    proof_of_concept=f"Payload: {payload}",
                    remediation="Implement input sanitization and output encoding"
                )
                vulnerabilities.append(vulnerability)
        
        return vulnerabilities
    
    async def test_csrf(self) -> List[Vulnerability]:
        """Test for CSRF vulnerabilities."""
        vulnerabilities = []
        
        # Simulate CSRF testing
        logger.info("Testing for CSRF vulnerabilities")
        
        # Check for anti-CSRF tokens
        has_csrf_token = False  # Simulate missing CSRF token
        
        if not has_csrf_token:
            vulnerability = Vulnerability(
                id="CSRF-001",
                title="Missing CSRF Protection",
                description="No anti-CSRF token found in forms",
                severity=Severity.MEDIUM,
                cvss_score=6.5,
                affected_component=self.target_url,
                remediation="Implement anti-CSRF tokens in all state-changing operations"
            )
            vulnerabilities.append(vulnerability)
        
        return vulnerabilities
    
    async def test_authentication_bypass(self) -> List[Vulnerability]:
        """Test for authentication bypass vulnerabilities."""
        vulnerabilities = []
        
        # Simulate authentication bypass testing
        logger.info("Testing for authentication bypass vulnerabilities")
        
        # Check for common authentication issues
        vulnerability = Vulnerability(
            id="AUTH-001",
            title="Weak Password Policy",
            description="Application accepts weak passwords",
            severity=Severity.MEDIUM,
            cvss_score=5.3,
            affected_component=self.target_url,
            remediation="Implement strong password policy and account lockout mechanisms"
        )
        vulnerabilities.append(vulnerability)
        
        return vulnerabilities


class PrivilegeEscalator:
    """Privilege escalation testing and exploitation."""
    
    @staticmethod
    def attempt_escalation(escalation_path: 'EscalationPath') -> 'EscalationResult':
        """Attempt privilege escalation along a path."""
        logger.info(f"Attempting escalation: {escalation_path.description}")
        
        # Simulate escalation attempt
        success = True  # Simulate successful escalation
        
        return EscalationResult(
            success=success,
            initial_privileges=escalation_path.required_privileges,
            new_privileges=["administrator", "system"] if success else [],
            technique_used=escalation_path.technique,
            timestamp=datetime.now()
        )


@dataclass
class EscalationPath:
    """Represents a privilege escalation path."""
    description: str
    technique: str
    required_privileges: List[str]
    auto_exploitable: bool = True
    risk_level: Severity = Severity.MEDIUM


@dataclass
class EscalationResult:
    """Result of a privilege escalation attempt."""
    success: bool
    initial_privileges: List[str]
    new_privileges: List[str]
    technique_used: str
    timestamp: datetime


class SystemAnalyzer:
    """System analysis for privilege escalation."""
    
    def __init__(self, host: str):
        self.host = host
        self.current_user = None
    
    def get_current_user(self) -> 'User':
        """Get current user information."""
        # Simulate getting current user
        return User(
            name="testuser",
            uid=1000,
            gid=1000,
            privileges=["user", "sudo"],
            groups=["users", "sudo"]
        )
    
    def find_escalation_paths(self) -> List[EscalationPath]:
        """Find potential privilege escalation paths."""
        paths = []
        
        # Simulate finding escalation paths
        paths.append(EscalationPath(
            description="Sudo misconfiguration",
            technique="Sudo privilege abuse",
            required_privileges=["user"],
            auto_exploitable=True,
            risk_level=Severity.HIGH
        ))
        
        paths.append(EscalationPath(
            description="Writable /etc/passwd",
            technique="Direct user creation",
            required_privileges=["user"],
            auto_exploitable=True,
            risk_level=Severity.CRITICAL
        ))
        
        return paths


@dataclass
class User:
    """Represents a system user."""
    name: str
    uid: int
    gid: int
    privileges: List[str]
    groups: List[str]


class PenetrationTestFramework:
    """Main framework for penetration testing operations."""
    
    def __init__(self, methodology: TestingMethodology = TestingMethodology.BLACK_BOX):
        self.methodology = methodology
        self.network_scanner = NetworkScanner()
        self.vulnerability_scanner = VulnerabilityScanner()
        self.web_tester = None
        self.test_results = []
        self.scan_history = []
    
    def configure(self, config: Dict[str, Any]) -> None:
        """Configure the penetration testing framework."""
        logger.info(f"Configuring framework with methodology: {self.methodology.value}")
        
        # Apply configuration
        if "scan_type" in config:
            self.network_scanner.scan_type = ScanType(config["scan_type"])
        
        if "scan_profiles" in config:
            self.vulnerability_scanner.scan_profiles = config["scan_profiles"]
    
    async def run_full_assessment(self, target: Target) -> Dict[str, Any]:
        """Run a complete penetration test assessment."""
        logger.info(f"Starting full assessment on {target.host}")
        
        assessment_results = {
            "target": target.host,
            "start_time": datetime.now(),
            "network_scan": None,
            "vulnerability_scan": None,
            "web_application_test": None,
            "summary": {}
        }
        
        try:
            # Phase 1: Network reconnaissance
            logger.info("Phase 1: Network reconnaissance")
            network_result = await self.network_scanner.scan(target)
            assessment_results["network_scan"] = network_result
            
            # Phase 2: Vulnerability scanning
            logger.info("Phase 2: Vulnerability scanning")
            vuln_result = await self.vulnerability_scanner.scan(target)
            assessment_results["vulnerability_scan"] = vuln_result
            
            # Phase 3: Web application testing (if applicable)
            if any(port in network_result.open_ports for port in [80, 443, 8080, 8443]):
                logger.info("Phase 3: Web application testing")
                self.web_tester = WebAppTester(f"http://{target.host}")
                
                web_vulnerabilities = []
                web_vulnerabilities.extend(await self.web_tester.test_sql_injection())
                web_vulnerabilities.extend(await self.web_tester.test_xss())
                web_vulnerabilities.extend(await self.web_tester.test_csrf())
                web_vulnerabilities.extend(await self.web_tester.test_authentication_bypass())
                
                assessment_results["web_application_test"] = web_vulnerabilities
            
            # Generate summary
            assessment_results["summary"] = self._generate_summary(assessment_results)
            assessment_results["end_time"] = datetime.now()
            
            # Store results
            self.scan_history.append(assessment_results)
            
            logger.info("Full assessment completed successfully")
            
        except Exception as e:
            logger.error(f"Assessment failed: {e}")
            assessment_results["error"] = str(e)
        
        return assessment_results
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate assessment summary."""
        all_vulnerabilities = []
        
        # Collect all vulnerabilities
        if results["vulnerability_scan"]:
            all_vulnerabilities.extend(results["vulnerability_scan"].vulnerabilities)
        
        if results["web_application_test"]:
            all_vulnerabilities.extend(results["web_application_test"])
        
        # Count by severity
        severity_counts = {severity: 0 for severity in Severity}
        for vuln in all_vulnerabilities:
            severity_counts[vuln.severity] += 1
        
        return {
            "total_vulnerabilities": len(all_vulnerabilities),
            "severity_breakdown": severity_counts,
            "critical_findings": severity_counts[Severity.CRITICAL],
            "high_findings": severity_counts[Severity.HIGH],
            "risk_score": self._calculate_risk_score(all_vulnerabilities)
        }
    
    def _calculate_risk_score(self, vulnerabilities: List[Vulnerability]) -> float:
        """Calculate overall risk score."""
        if not vulnerabilities:
            return 0.0
        
        total_score = sum(vuln.cvss_score for vuln in vulnerabilities)
        return round(total_score / len(vulnerabilities), 2)
    
    def validate(self, target: Target) -> bool:
        """Validate target before testing."""
        logger.info(f"Validating target: {target.host}")
        
        # Validate network target
        if not self.network_scanner.validate_target(target):
            logger.error("Invalid network target")
            return False
        
        # Validate vulnerability scanner target
        if not self.vulnerability_scanner.validate_target(target):
            logger.error("Invalid vulnerability scanner target")
            return False
        
        logger.info("Target validation successful")
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """Get current framework status."""
        return {
            "methodology": self.methodology.value,
            "scan_history_count": len(self.scan_history),
            "last_scan": self.scan_history[-1] if self.scan_history else None,
            "components": {
                "network_scanner": self.network_scanner.scan_type.value,
                "vulnerability_scanner": self.vulnerability_scanner.scan_profiles,
                "web_tester": self.web_tester is not None
            }
        }


async def main():
    """Main demonstration function."""
    print("=" * 60)
    print("Penetration Testing Framework Demonstration")
    print("=" * 60)
    
    # Create framework instance
    framework = PenetrationTestFramework(
        methodology=TestingMethodology.BLACK_BOX
    )
    
    # Configure framework
    framework.configure({
        "scan_type": "aggressive",
        "scan_profiles": ["OWASP_Top_10", "CIS_Benchmarks"]
    })
    
    # Create target
    target = Target(
        host="192.168.1.100",
        port_range="1-1000",
        description="Web application server",
        credentials={"username": "admin", "password": "password123"}
    )
    
    # Validate target
    if not framework.validate(target):
        print("Target validation failed!")
        return
    
    print(f"Target validated: {target.host}")
    print(f"Port range: {target.port_range}")
    print(f"Description: {target.description}")
    
    # Run full assessment
    print("\nStarting full penetration test assessment...")
    results = await framework.run_full_assessment(target)
    
    # Display results
    print("\n" + "=" * 60)
    print("Assessment Results")
    print("=" * 60)
    
    if "error" in results:
        print(f"Assessment failed: {results['error']}")
        return
    
    # Network scan results
    if results["network_scan"]:
        network_scan = results["network_scan"]
        print(f"\nNetwork Scan Results:")
        print(f"  Open Ports: {network_scan.open_ports}")
        print(f"  Services: {network_scan.services}")
        print(f"  Status: {network_scan.status.value}")
    
    # Vulnerability scan results
    if results["vulnerability_scan"]:
        vuln_scan = results["vulnerability_scan"]
        print(f"\nVulnerability Scan Results:")
        print(f"  Total Vulnerabilities: {len(vuln_scan.vulnerabilities)}")
        print(f"  Severity Breakdown: {vuln_scan.vulnerability_count}")
    
    # Web application test results
    if results["web_application_test"]:
        web_vulns = results["web_application_test"]
        print(f"\nWeb Application Test Results:")
        print(f"  Vulnerabilities Found: {len(web_vulns)}")
        for vuln in web_vulns:
            print(f"    - {vuln.title} ({vuln.severity.value})")
    
    # Summary
    if results["summary"]:
        summary = results["summary"]
        print(f"\nAssessment Summary:")
        print(f"  Total Vulnerabilities: {summary['total_vulnerabilities']}")
        print(f"  Risk Score: {summary['risk_score']}")
        print(f"  Critical Findings: {summary['critical_findings']}")
        print(f"  High Findings: {summary['high_findings']}")
    
    # Get framework status
    print("\n" + "=" * 60)
    print("Framework Status")
    print("=" * 60)
    status = framework.get_status()
    print(f"Methodology: {status['methodology']}")
    print(f"Scan History: {status['scan_history_count']} scans")
    print(f"Components: {status['components']}")
    
    print("\n" + "=" * 60)
    print("Demonstration completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())