"""
Security Agent - Enterprise-Grade Security Auditing and Vulnerability Management.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum, auto
from datetime import datetime
import re


class ThreatLevel(Enum):
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    INFO = 1


class VulnerabilityType(Enum):
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


class FindingStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    ACCEPTED = "accepted"


@dataclass
class Vulnerability:
    id: str
    name: str
    type: VulnerabilityType
    severity: ThreatLevel
    location: str
    description: str
    impact: str
    remediation: str
    cvss_score: float
    discovered_at: datetime


class VulnerabilityScanner:
    def __init__(self):
        self.findings: List[Vulnerability] = []
    
    def scan_code(self, code: str) -> List[Vulnerability]:
        vulnerabilities = []
        lines = code.split('\n')
        
        patterns = [
            (r"os\.system\s*\(", "Command Injection", ThreatLevel.HIGH, 8.0),
            (r"subprocess.*shell\s*=\s*True", "Shell Injection", ThreatLevel.HIGH, 8.5),
            (r"eval\s*\(", "Eval Injection", ThreatLevel.CRITICAL, 9.0),
            (r"SELECT\s+\*.*WHERE.*\+", "SQL Injection", ThreatLevel.CRITICAL, 9.0),
            (r"md5\s*\(", "MD5 Hashing", ThreatLevel.HIGH, 7.0),
            (r"sha1\s*\(", "SHA1 Hashing", ThreatLevel.MEDIUM, 6.0),
            (r"api[_-]?key\s*=\s*['\"][^'\"]+", "Hardcoded API Key", ThreatLevel.CRITICAL, 9.0),
            (r"password\s*=\s*['\"][^'\"]+", "Hardcoded Password", ThreatLevel.CRITICAL, 9.5),
            (r"debug\s*=\s*True", "Debug Mode Enabled", ThreatLevel.HIGH, 7.5),
            (r"jwt\.decode.*verify\s*=\s*False", "JWT Verification Disabled", ThreatLevel.CRITICAL, 9.0),
        ]
        
        for pattern, name, severity, cvss in patterns:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    vuln = Vulnerability(
                        id=f"vuln_{len(self.findings) + len(vulnerabilities) + 1}",
                        name=name,
                        type=VulnerabilityType.INJECTION,
                        severity=severity,
                        location=f"Line {i}",
                        description=f"Potential {name} vulnerability found",
                        impact="Could allow attacker to exploit the system",
                        remediation=f"Implement secure coding practices",
                        cvss_score=cvss,
                        discovered_at=datetime.now()
                    )
                    vulnerabilities.append(vuln)
        
        self.findings.extend(vulnerabilities)
        return vulnerabilities
    
    def calculate_security_score(self, vulnerabilities: List[Vulnerability]) -> Dict:
        if not vulnerabilities:
            return {"score": 100, "grade": "A+"}
        
        weights = {ThreatLevel.CRITICAL: 40, ThreatLevel.HIGH: 25, ThreatLevel.MEDIUM: 15, ThreatLevel.LOW: 10}
        deductions = sum(weights.get(v.severity, 10) for v in vulnerabilities)
        score = max(0, 100 - deductions)
        grade = "A+" if score >= 95 else "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D"
        return {"score": score, "grade": grade}


class ThreatModeler:
    def __init__(self):
        self.components: Dict[str, Dict] = {}
        self.threats: List[Dict] = []
    
    def add_component(self, name: str, type: str, trust_level: str):
        self.components[name] = {"type": type, "trust_level": trust_level, "threats": []}
    
    def generate_threats(self) -> List[Dict]:
        stride = [
            ("Spoofing", "HIGH", "Implement strong authentication", ["T1190"]),
            ("Tampering", "HIGH", "Use integrity checks", ["T1056"]),
            ("Repudiation", "MEDIUM", "Implement audit logging", ["T1485"]),
            ("Information Disclosure", "HIGH", "Encrypt sensitive data", ["T1041"]),
            ("Denial of Service", "MEDIUM", "Implement rate limiting", ["T1498"]),
            ("Elevation of Privilege", "CRITICAL", "Implement RBAC", ["T1068"]),
        ]
        
        threats = []
        for comp, details in self.components.items():
            for threat_type, severity, mitigation, _ in stride:
                if details["trust_level"] == "untrusted" or threat_type in ["DoS", "EoP"]:
                    threat = {
                        "id": f"threat_{len(threats) + 1}",
                        "component": comp,
                        "threat_type": threat_type,
                        "severity": severity,
                        "mitigation": mitigation
                    }
                    details["threats"].append(threat)
                    threats.append(threat)
        
        self.threats = threats
        return threats


class SecurityAgent:
    def __init__(self):
        self.scanner = VulnerabilityScanner()
        self.threat_modeler = ThreatModeler()
    
    def scan_source(self, code: str) -> Dict:
        vulnerabilities = self.scanner.scan_code(code)
        by_severity = {}
        for v in vulnerabilities:
            by_severity.setdefault(v.severity.name, []).append({
                "id": v.id, "name": v.name, "location": v.location, "remediation": v.remediation
            })
        
        score = self.scanner.calculate_security_score(vulnerabilities)
        
        self.threat_modeler.add_component("API", "service", "untrusted")
        self.threat_modeler.add_component("Database", "storage", "trusted")
        threats = self.threat_modeler.generate_threats()
        
        return {
            "total_vulnerabilities": len(vulnerabilities),
            "by_severity": by_severity,
            "security_score": score,
            "threats": threats,
            "recommendations": self._generate_recommendations(vulnerabilities)
        }
    
    def _generate_recommendations(self, vulnerabilities: List[Vulnerability]) -> List[str]:
        recs = []
        if any(v.severity == ThreatLevel.CRITICAL for v in vulnerabilities):
            recs.append("CRITICAL: Fix critical vulnerabilities immediately")
        if any(v.severity == ThreatLevel.HIGH for v in vulnerabilities):
            recs.append("HIGH: Address high severity issues in current sprint")
        recs.extend([
            "Enable comprehensive audit logging",
            "Implement security headers (CSP, X-Frame-Options)",
            "Conduct regular penetration testing",
            "Automate security scanning in CI/CD"
        ])
        return recs
    
    def get_dashboard(self) -> Dict:
        return {
            "total_scans": len(self.scanner.findings),
            "open_findings": len([v for v in self.scanner.findings if v.id]),
            "threats": len(self.threat_modeler.threats)
        }


def main():
    print("\n" + "="*60)
    print("  Security Agent")
    print("  Enterprise-Grade Security Auditing")
    print("="*60 + "\n")
    
    agent = SecurityAgent()
    
    sample_code = '''
import os
import md5
password = "admin123"
api_key = "sk-1234567890"
query = "SELECT * FROM users WHERE name = '" + user + "'"
os.system("rm -rf /tmp/*")
app.config['DEBUG'] = True
'''
    
    report = agent.scan_source(sample_code)
    
    print(f"Total Vulnerabilities: {report['total_vulnerabilities']}")
    print(f"Security Score: {report['security_score']['score']}/{report['security_score']['grade']}")
    print(f"Threats Identified: {len(report['threats'])}")
    print()
    print("Top Recommendations:")
    for rec in report['recommendations'][:3]:
        print(f"  - {rec}")


if __name__ == "__main__":
    main()
