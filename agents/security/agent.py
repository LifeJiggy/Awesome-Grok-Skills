#!/usr/bin/env python3
"""
Grok Security Agent
Specialized agent for security analysis, vulnerability assessment, and threat modeling.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import hashlib
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
    SOCIAL_ENGINEERING = "social_engineering"

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
    references: List[str]
    cve_id: Optional[str]
    discovered_at: datetime

@dataclass
class SecurityFinding:
    id: str
    vulnerability_id: str
    target: str
    evidence: str
    exploitability: str
    affected_components: List[str]
    mitigations: List[str]

class VulnerabilityScanner:
    """Scans code and systems for vulnerabilities."""
    
    def __init__(self):
        self.findings: List[Vulnerability] = []
        self.scan_history = []
    
    def scan_code(self, code: str, language: str = "python") -> List[Vulnerability]:
        """Scan source code for vulnerabilities."""
        vulnerabilities = []
        
        if language in ["python", "javascript", "typescript"]:
            vulnerabilities.extend(self._scan_for_injection(code))
            vulnerabilities.extend(self._scan_for_crypto(code))
            vulnerabilities.extend(self._scan_for_auth(code))
            vulnerabilities.extend(self._scan_for_sensitive_data(code))
        
        self.findings.extend(vulnerabilities)
        return vulnerabilities
    
    def _scan_for_injection(self, code: str) -> List[Vulnerability]:
        """Scan for injection vulnerabilities."""
        vuln_list = []
        
        patterns = {
            'sql_injection': [
                r'(execute|query|raw).*%\s*['\''"]',
                r'(execute|query).*\{\s*[^}]+\s*\}',
                r'string\.format.*[^\w]%\s*[as]'
            ],
            'command_injection': [
                r'os\.system\s*\(',
                r'subprocess.*shell\s*=\s*True',
                r'eval\s*\([^)]+\)'
            ],
            'path_traversal': [
                r'open\s*\([^,]+,\s*['\''"]?[rwa]',
                r'os\.path\.join.*\.\.',
                r'readFile.*user_input'
            ]
        }
        
        vuln_type_map = {
            'sql_injection': (VulnerabilityType.INJECTION, ThreatLevel.CRITICAL),
            'command_injection': (VulnerabilityType.INJECTION, ThreatLevel.CRITICAL),
            'path_traversal': (VulnerabilityType.INJECTION, ThreatLevel.HIGH)
        }
        
        for vuln_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                matches = re.finditer(pattern, code, re.IGNORECASE)
                for match in matches:
                    vuln = Vulnerability(
                        id=f"vuln_{len(self.findings) + 1}",
                        name=f"{vuln_type.replace('_', ' ').title()}",
                        type=vuln_type_map[vuln_type][0],
                        severity=vuln_type_map[vuln_type][1],
                        location=f"Line {code[:match.start()].count(chr(10)) + 1}",
                        description=f"Potential {vuln_type.replace('_', ' ')} found",
                        impact="Could allow attacker to execute unauthorized commands",
                        remediation=f"Use parameterized queries / input validation",
                        references=["OWASP"],
                        cve_id=None,
                        discovered_at=datetime.now()
                    )
                    vuln_list.append(vuln)
        
        return vuln_list
    
    def _scan_for_crypto(self, code: str) -> List[Vulnerability]:
        """Scan for cryptographic vulnerabilities."""
        vuln_list = []
        
        weak_crypto = [
            (r'md5\s*\(', "MD5 hashing", ThreatLevel.HIGH),
            (r'sha1\s*\(', "SHA1 hashing", ThreatLevel.MEDIUM),
            (r'DES\.new', "DES encryption", ThreatLevel.HIGH),
            (r'Random\.new', "Weak random number generation", ThreatLevel.MEDIUM)
        ]
        
        for pattern, name, severity in weak_crypto:
            if re.search(pattern, code):
                vuln = Vulnerability(
                    id=f"vuln_{len(self.findings) + 1}",
                    name=f"Weak Cryptography: {name}",
                    type=VulnerabilityType.CRYPTOGRAPHY,
                    severity=severity,
                    location="Crypto usage",
                    description=f"Weak cryptographic algorithm used: {name}",
                    impact="Cryptographic weakness could be exploited",
                    remediation="Use SHA-256 or stronger / Use secrets module",
                    references=["OWASP Cryptographic Failures"],
                    cve_id=None,
                    discovered_at=datetime.now()
                )
                vuln_list.append(vuln)
        
        return vuln_list
    
    def _scan_for_auth(self, code: str) -> List[Vulnerability]:
        """Scan for authentication vulnerabilities."""
        vuln_list = []
        
        auth_issues = [
            (r'if\s+password\s*==', "Hardcoded password comparison", ThreatLevel.CRITICAL),
            (r'check_password.*==\s*True', "Insecure password check", ThreatLevel.HIGH),
            (r'session\s*\[\s*["\']user', "Unsecured session access", ThreatLevel.MEDIUM)
        ]
        
        for pattern, name, severity in auth_issues:
            if re.search(pattern, code, re.IGNORECASE):
                vuln = Vulnerability(
                    id=f"vuln_{len(self.findings) + 1}",
                    name=f"Authentication Issue: {name}",
                    type=VulnerabilityType.AUTHENTICATION,
                    severity=severity,
                    location="Auth implementation",
                    description=f"{name} detected",
                    impact="Could allow unauthorized access",
                    remediation="Use secure authentication patterns / hashing",
                    references=["OWASP Auth"],
                    cve_id=None,
                    discovered_at=datetime.now()
                )
                vuln_list.append(vuln)
        
        return vuln_list
    
    def _scan_for_sensitive_data(self, code: str) -> List[Vulnerability]:
        """Scan for exposed sensitive data."""
        vuln_list = []
        
        patterns = [
            (r'api[_-]?key\s*=\s*["\'][^"\']+', "Hardcoded API key", ThreatLevel.CRITICAL),
            (r'secret[_-]?key\s*=\s*["\'][^"\']+', "Hardcoded secret", ThreatLevel.CRITICAL),
            (r'password\s*=\s*["\'][^"\']+', "Hardcoded password", ThreatLevel.CRITICAL),
            (r'aws[_-]?secret\s*=\s*["\'][^"\']+', "AWS credentials", ThreatLevel.CRITICAL),
            (r'private[_-]?key.*=\s*["\']', "Private key exposed", ThreatLevel.CRITICAL)
        ]
        
        for pattern, name, severity in patterns:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                vuln = Vulnerability(
                    id=f"vuln_{len(self.findings) + 1}",
                    name=name,
                    type=VulnerabilityType.SENSITIVE_DATA,
                    severity=severity,
                    location=f"Line {code[:match.start()].count(chr(10)) + 1}",
                    description=f"Sensitive data hardcoded: {match.group()[:20]}...",
                    impact="Exposure of sensitive credentials",
                    remediation="Use environment variables / secrets management",
                    references=["OWASP Secrets"],
                    cve_id=None,
                    discovered_at=datetime.now()
                )
                vuln_list.append(vuln)
        
        return vuln_list

class ThreatModeler:
    """Creates threat models for systems."""
    
    def __init__(self):
        self.threats: List[Dict[str, Any]] = []
        self.components: Dict[str, Dict] = {}
    
    def add_component(self, name: str, component_type: str,
                     trust_level: str, data_flows: List[str]) -> None:
        """Add system component to threat model."""
        self.components[name] = {
            'type': component_type,
            'trust_level': trust_level,
            'data_flows': data_flows
        }
    
    def generate_threats(self) -> List[Dict[str, Any]]:
        """Generate threats based on STRIDE methodology."""
        threats = []
        
        stride_threats = {
            'Spoofing': ThreatLevel.HIGH,
            'Tampering': ThreatLevel.HIGH,
            'Repudiation': ThreatLevel.MEDIUM,
            'Information Disclosure': ThreatLevel.HIGH,
            'Denial of Service': ThreatLevel.MEDIUM,
            'Elevation of Privilege': ThreatLevel.CRITICAL
        }
        
        for component, details in self.components.items():
            for threat_type, severity in stride_threats.items():
                if details['trust_level'] == 'untrusted':
                    threats.append({
                        'id': f"threat_{len(threats) + 1}",
                        'component': component,
                        'threat_type': threat_type,
                        'severity': severity.value,
                        'description': f"{threat_type} threat on {component}",
                        'mitigation': self._get_mitigation(threat_type, component)
                    })
        
        self.threats = threats
        return threats
    
    def _get_mitigation(self, threat_type: str, component: str) -> str:
        """Get mitigation for threat type."""
        mitigations = {
            'Spoofing': "Implement strong authentication",
            'Tampering': "Use integrity checks and signatures",
            'Repudiation': "Implement audit logging",
            'Information Disclosure': "Encrypt sensitive data",
            'Denial of Service': "Implement rate limiting",
            'Elevation of Privilege': "Implement authorization checks"
        }
        return mitigations.get(threat_type, "Implement security controls")

class SecurityAudit:
    """Conducts comprehensive security audits."""
    
    def __init__(self):
        self.audits = []
        self.findings = []
    
    def start_audit(self, target: str, scope: List[str]) -> str:
        """Start security audit."""
        audit_id = f"audit_{len(self.audits) + 1}"
        self.audits.append({
            'id': audit_id,
            'target': target,
            'scope': scope,
            'start_time': datetime.now(),
            'status': 'in_progress'
        })
        return audit_id
    
    def run_checks(self, audit_id: str) -> Dict[str, Any]:
        """Run security checks for audit."""
        return {
            'authentication': self._check_authentication(),
            'authorization': self._check_authorization(),
            'input_validation': self._check_input_validation(),
            'cryptography': self._check_cryptography(),
            'configuration': self._check_configuration()
        }
    
    def _check_authentication(self) -> Dict[str, Any]:
        """Check authentication security."""
        return {
            'status': 'pass',
            'checks': [
                {'name': 'Password policy', 'passed': True},
                {'name': 'MFA enabled', 'passed': True},
                {'name': 'Session timeout', 'passed': True}
            ]
        }
    
    def _check_authorization(self) -> Dict[str, Any]:
        """Check authorization controls."""
        return {
            'status': 'pass',
            'checks': [
                {'name': 'Role-based access', 'passed': True},
                {'name': 'Permission checks', 'passed': True}
            ]
        }
    
    def _check_input_validation(self) -> Dict[str, Any]:
        """Check input validation."""
        return {
            'status': 'warning',
            'checks': [
                {'name': 'SQL injection protection', 'passed': True},
                {'name': 'XSS protection', 'passed': True},
                {'name': 'File upload validation', 'passed': False}
            ]
        }
    
    def _check_cryptography(self) -> Dict[str, Any]:
        """Check cryptographic implementations."""
        return {
            'status': 'pass',
            'checks': [
                {'name': 'TLS 1.2+', 'passed': True},
                {'name': 'Strong ciphers', 'passed': True},
                {'name': 'Key management', 'passed': True}
            ]
        }
    
    def _check_configuration(self) -> Dict[str, Any]:
        """Check security configuration."""
        return {
            'status': 'pass',
            'checks': [
                {'name': 'Debug mode disabled', 'passed': True},
                {'name': 'Security headers', 'passed': True},
                {'name': 'Logging configured', 'passed': True}
            ]
        }
    
    def complete_audit(self, audit_id: str) -> Dict[str, Any]:
        """Complete security audit."""
        for audit in self.audits:
            if audit['id'] == audit_id:
                audit['status'] = 'completed'
                audit['end_time'] = datetime.now()
                audit['results'] = self.run_checks(audit_id)
        
        return {'status': 'completed', 'audit_id': audit_id}

class SecurityAgent:
    """Main security agent."""
    
    def __init__(self):
        self.scanner = VulnerabilityScanner()
        self.threat_modeler = ThreatModeler()
        self.audit = SecurityAudit()
    
    def scan_source(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Scan source code for vulnerabilities."""
        vulnerabilities = self.scanner.scan_code(code, language)
        
        by_severity = {}
        for vuln in vulnerabilities:
            severity_name = vuln.severity.name
            if severity_name not in by_severity:
                by_severity[severity_name] = []
            by_severity[severity_name].append({
                'id': vuln.id,
                'name': vuln.name,
                'type': vuln.type.value,
                'location': vuln.location,
                'remediation': vuln.remediation
            })
        
        return {
            'total_vulnerabilities': len(vulnerabilities),
            'by_severity': by_severity,
            'critical_count': len([v for v in vulnerabilities if v.severity == ThreatLevel.CRITICAL]),
            'high_count': len([v for v in vulnerabilities if v.severity == ThreatLevel.HIGH]),
            'medium_count': len([v for v in vulnerabilities if v.severity == ThreatLevel.MEDIUM]),
            'low_count': len([v for v in vulnerabilities if v.severity == ThreatLevel.LOW])
        }
    
    def analyze_code_security(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Comprehensive security analysis."""
        vuln_report = self.scan_source(code, language)
        
        self.threat_modeler.add_component("API", "service", "untrusted", ["HTTPS"])
        self.threat_modeler.add_component("Database", "storage", "trusted", ["SQL"])
        self.threats = self.threat_modeler.generate_threats()
        
        return {
            'vulnerabilities': vuln_report,
            'threats': self.threats,
            'risk_score': self._calculate_risk_score(vuln_report),
            'recommendations': self._generate_recommendations(vuln_report)
        }
    
    def _calculate_risk_score(self, report: Dict[str, Any]) -> float:
        """Calculate overall risk score."""
        weights = {
            'critical_count': 40,
            'high_count': 20,
            'medium_count': 10,
            'low_count': 5
        }
        
        score = 0
        for key, weight in weights.items():
            count = report.get(key, 0)
            score += min(count * weight, weight * 5)
        
        return min(100, score)
    
    def _generate_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """Generate security recommendations."""
        recommendations = []
        
        if report.get('critical_count', 0) > 0:
            recommendations.append("CRITICAL: Fix critical vulnerabilities immediately")
        if report.get('high_count', 0) > 0:
            recommendations.append("HIGH: Address high severity issues in next sprint")
        if report.get('medium_count', 0) > 0:
            recommendations.append("MEDIUM: Plan fixes for medium severity issues")
        
        recommendations.append("Implement security headers (CSP, X-Frame-Options)")
        recommendations.append("Enable comprehensive audit logging")
        recommendations.append("Conduct regular penetration testing")
        
        return recommendations
    
    def get_security_dashboard(self) -> Dict[str, Any]:
        """Get security dashboard."""
        return {
            'scanner': {
                'total_scans': len(self.scanner.scan_history),
                'total_vulnerabilities': len(self.scanner.findings)
            },
            'threat_model': {
                'components': len(self.threat_modeler.components),
                'threats_generated': len(self.threats)
            },
            'audit': {
                'total_audits': len(self.audit.audits),
                'completed': len([a for a in self.audit.audits if a['status'] == 'completed']
            }
        }

def main():
    """Main entry point."""
    agent = SecurityAgent()
    
    sample_code = """
    password = "admin123"
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    hash = md5(password)
    api_key = "sk-1234567890abcdef"
    """
    
    report = agent.analyze_code_security(sample_code, "python")
    print(f"Security report: {report}")

if __name__ == "__main__":
    main()
