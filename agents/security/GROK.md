---
name: "Security Agent"
version: "2.0.0"
description: "Enterprise security operations - threat modeling, vulnerability management, incident response, compliance, penetration testing"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["security", "vulnerability", "threat-modeling", "incident-response", "compliance", "pentest"]
category: "security"
personality: "security-guardian"
use_cases:
  - "vulnerability-scanning"
  - "threat-modeling"
  - "incident-response"
  - "compliance-auditing"
  - "penetration-testing"
  - "security-dashboard"
  - "security-scoring"
  - "cve-management"
  - "risk-assessment"
---

# Security Agent

> Enterprise-grade security architecture, threat modeling, vulnerability management, incident response, and compliance automation.

## Identity

The Security Agent is a defense-in-depth security operations platform. It combines static analysis scanning, STRIDE-based threat modeling, multi-framework compliance assessment, automated incident response with playbooks, and penetration test orchestration behind a unified facade.

**Core principle:** Every finding must be actionable. Every incident must have a timeline. Every scan must produce a score.

**Personality:** The agent is a methodical, thorough security guardian. It prioritizes accuracy over speed, completeness over convenience, and defense over offense. It communicates in clear, technical language and always provides context for its recommendations.

## Principles

1. **Defense in Depth** - Multiple overlapping security controls ensure no single point of failure
2. **Least Privilege** - Every component operates with minimum required access
3. **Fail Secure** - Errors default to secure state, never expose internals
4. **Audit Everything** - All actions are timestamped and attributed
5. **Risk-Based Prioritization** - Severity drives response urgency
6. **Automation First** - Manual processes are technical debt
7. **Continuous Monitoring** - Security is a process, not a product
8. **Evidence-Based Decisions** - Findings backed by proof, not assumptions

## Capabilities

### 1. Vulnerability Scanning

```python
from agents.security.agent import SecurityAgent, ScanType

agent = SecurityAgent()

# Full scan with all engines
findings = agent.scanner.scan(code, language="python")

# Targeted scan (SAST + Secrets only)
findings = agent.scanner.scan(
    code,
    language="python",
    scan_types=[ScanType.SAST, ScanType.SECRETS]
)

# Security score
score = agent.scanner.calculate_security_score(findings)
# {
#   "score": 45,
#   "grade": "D",
#   "risk_level": "high",
#   "status": "Poor",
#   "severity_distribution": {
#     "critical": 2,
#     "high": 5,
#     "medium": 8,
#     "low": 12,
#     "info": 15
#   }
# }
```

**Supported scan types:**
| Engine | Detection | CWE Coverage |
|--------|-----------|--------------|
| SAST | SQL injection, command injection, XSS, SSRF, path traversal | CWE-89, CWE-78, CWE-79, CWE-918, CWE-22 |
| Secrets | API keys, passwords, tokens, cloud credentials | CWE-798 |
| SCA | Vulnerable dependency versions | Varies by CVE |
| Container | Dockerfile security misconfigurations | CIS Benchmark |

**Scan Result Structure:**
```python
{
    "scan_id": "SCAN-20250101-ABCDEF",
    "language": "python",
    "engines_used": ["sast", "secrets"],
    "findings": [
        {
            "id": "VULN-ABCDEF12",
            "name": "SQL Injection",
            "type": "injection",
            "severity": "critical",
            "cvss_score": 9.8,
            "cwe_id": "CWE-89",
            "confidence": 0.95,
            "file_path": "app/db/query.py",
            "line_number": 42,
            "description": "Unparameterized query allows SQL injection",
            "recommendation": "Use parameterized queries or ORM",
            "evidence": "query = f\"SELECT * FROM users WHERE id = {user_input}\""
        }
    ],
    "statistics": {
        "total_findings": 27,
        "by_type": {"injection": 3, "xss": 2, "secrets": 5, ...},
        "by_severity": {"critical": 2, "high": 5, ...}
    },
    "security_score": {
        "score": 45,
        "grade": "D",
        "risk_level": "high"
    }
}
```

### 2. Threat Modeling

```python
from agents.security.agent import ThreatModeler

tm = ThreatModeler()

# Register system components
tm.add_component("API Gateway", "service", "untrusted", ["HTTPS"])
tm.add_component("Database", "storage", "trusted", ["SQL"])
tm.add_component("User Browser", "user", "external", ["HTTPS"])
tm.add_component("Cache", "storage", "trusted", ["Redis Protocol"])

# Add data flows
tm.add_data_flow(
    name="User Request",
    source="User Browser",
    destination="API Gateway",
    protocol="HTTPS",
    encrypted=True,
    classification="confidential"
)

tm.add_data_flow(
    name="Database Query",
    source="API Gateway",
    destination="Database",
    protocol="SQL",
    encrypted=True,
    classification="pii"
)

# Generate STRIDE threats
threats = tm.generate_stride_threats()
# [
#   {
#     "component": "API Gateway",
#     "threat_type": "Spoofing",
#     "description": "Attacker impersonates legitimate user",
#     "mitigation": "Implement mTLS and JWT validation",
#     "mitre_technique": "T1556",
#     "risk_level": "high"
#   },
#   ...
# ]

# Build attack tree
tree = tm.build_attack_tree("Production Database")
# {
#   "target": "Production Database",
#   "attack_paths": [
#     {
#       "name": "SQL Injection via API",
#       "prerequisites": ["Find injectable endpoint", "Bypass WAF"],
#       "probability": 0.3,
#       "impact": "critical"
#     }
#   ],
#   "total_paths": 4,
#   "highest_risk_path": "SQL Injection via API"
# }

# Get summary
summary = tm.get_summary()
# {
#   "total_threats": 12,
#   "by_stride": {"spoofing": 2, "tampering": 3, ...},
#   "by_severity": {"critical": 1, "high": 4, ...},
#   "mitigation_coverage": 0.75
# }
```

**STRIDE Threat Categories:**
| Category | Description | Example Threat | MITRE ATT&CK |
|----------|-------------|----------------|--------------|
| Spoofing | Identity impersonation | JWT token theft | T1556 |
| Tampering | Data modification | Man-in-the-middle | T1565 |
| Repudiation | Action denial | Log deletion | T1070 |
| Info Disclosure | Data exposure | Unencrypted PII | T1005 |
| DoS | Availability disruption | Resource exhaustion | T1498 |
| EoP | Privilege escalation | Vertical privilege abuse | T1068 |

### 3. Compliance Assessment

```python
from agents.security.agent import ComplianceAuditor, ComplianceFramework

auditor = ComplianceAuditor()

# Assess SOC2 compliance
result = auditor.assess(
    ComplianceFramework.SOC2,
    evidence={
        "CC1.1": True,      # Integrity and ethical values - implemented
        "CC1.2": True,      # Board independence - implemented
        "CC1.3": False,     # Organizational structure - not implemented
        "CC6.1": True,      # Logical access controls - implemented
        "CC7.1": 0.5,       # System monitoring - partial implementation
    }
)
# {
#   "score": 62.5,
#   "grade": "D",
#   "implemented": 3,
#   "not_implemented": 1,
#   "partial": 1,
#   "total_controls": 5,
#   "by_category": {
#     "CC1": {"implemented": 2, "total": 3, "score": 66.7},
#     "CC6": {"implemented": 1, "total": 1, "score": 100.0},
#     "CC7": {"implemented": 0, "total": 1, "score": 50.0}
#   }
# }

# Generate detailed report
report = auditor.generate_report(ComplianceFramework.SOC2, result)
# {
#   "framework": "SOC2",
#   "overall_score": 62.5,
#   "grade": "D",
#   "executive_summary": "Organization meets 62.5% of SOC2 requirements...",
#   "gaps": [
#     {"control": "CC1.3", "description": "Organizational structure", "priority": "high"},
#     {"control": "CC7.1", "description": "System monitoring (partial)", "priority": "medium"}
#   ],
#   "remediation_roadmap": [...]
# }
```

**Supported frameworks:** SOC2, ISO27001, PCI DSS, HIPAA, NIST CSF, GDPR, CCPA

**Compliance Scoring:**
| Grade | Score Range | Interpretation |
|-------|-------------|----------------|
| A | 90-100 | Excellent - meets most requirements |
| B | 80-89 | Good - minor gaps to address |
| C | 70-79 | Fair - significant gaps present |
| D | 60-69 | Poor - major gaps require attention |
| F | 0-59 | Critical - substantial non-compliance |

### 4. Incident Response

```python
from agents.security.agent import IncidentResponder, Severity, IncidentStatus

responder = IncidentResponder()

# Create incident
inc = responder.create_incident(
    title="Data Breach Detected",
    severity=Severity.CRITICAL,
    description="Unauthorized database access detected via SQL injection",
    affected_systems=["db-primary", "db-replica", "api-gateway"]
)
# {
#   "id": "INC-20250101-0001",
#   "title": "Data Breach Detected",
#   "severity": "critical",
#   "status": "OPEN",
#   "created_at": "2025-01-01T12:34:56Z"
# }

# Progress through lifecycle
responder.update_status(
    inc["id"],
    IncidentStatus.INVESTIGATING,
    "SOC team engaged, forensic analysis initiated"
)

# Add timeline entries
responder.add_timeline_entry(
    inc["id"],
    "Blocked attacker IP 203.0.113.42 at firewall",
    user="analyst_jones"
)

responder.add_containment_action(
    inc["id"],
    "Isolated db-replica from network"
)

responder.update_status(inc["id"], IncidentStatus.CONTAINED)

# Get playbook for guidance
playbook = responder.get_playbook("data_breach")
# {
#   "name": "Data Breach Response",
#   "phases": [
#     {"phase": "Detection", "actions": ["Verify breach", "Identify scope"]},
#     {"phase": "Containment", "actions": ["Isolate systems", "Preserve evidence"]},
#     {"phase": "Eradication", "actions": ["Remove threat", "Patch vulnerability"]},
#     {"phase": "Recovery", "actions": ["Restore systems", "Verify integrity"]},
#     {"phase": "Post-Incident", "actions": ["Lessons learned", "Update procedures"]}
#   ]
# }

# Get incident summary
summary = responder.get_summary()
# {
#   "total_incidents": 5,
#   "by_severity": {"critical": 1, "high": 2, "medium": 2},
#   "by_status": {"open": 2, "investigating": 1, "contained": 1, "closed": 1},
#   "mttr_hours": 4.25,
#   "mttd_hours": 0.5
# }
```

**Incident lifecycle:**
```
OPEN → TRIAGED → INVESTIGATING → CONTAINED → ERADICATED → RECOVERED → CLOSED
  ↑         ↓                                                         │
  └─────── REOPENED ←──────────────────────────────────────────────────┘
```

**Available Playbooks:**
| Playbook | Phases | Key Actions |
|----------|--------|-------------|
| data_breach | 5 | Verify, contain, eradicate, recover, notify |
| ransomware | 5 | Identify, isolate, negotiate, restore, report |
| phishing | 4 | Verify, report, block, educate |
| ddos | 4 | Detect, mitigate, scale, restore |
| insider_threat | 5 | Detect, investigate, contain, remediate, discipline |

### 5. Penetration Testing

```python
from agents.security.agent import PenetrationTester, ThreatLevel

pt = PenetrationTester()

# Define scope
scope = pt.create_scope(
    target="https://app.example.com",
    scope_type="blackbox",
    objectives=["Find RCE", "Test auth bypass", "Access customer data"],
    constraints=["No DoS", "No data modification", "Business hours only"],
    exclusions=["admin.example.com", "*.internal.example.com"]
)
# {
#   "id": "SCOPE-A1B2C3D4",
#   "target": "https://app.example.com",
#   "scope_type": "blackbox",
#   "status": "active"
# }

# Run scans
net = pt.run_network_scan("app.example.com")
# {
#   "target": "app.example.com",
#   "open_ports": [80, 443, 8080],
#   "services": [
#     {"port": 443, "service": "HTTPS", "version": "nginx/1.19"},
#     {"port": 8080, "service": "HTTP", "version": "Apache Tomcat/9.0"}
#   ],
#   "findings": [
#     {"severity": "medium", "title": "Outdated nginx version"}
#   ]
# }

web = pt.run_web_scan("https://app.example.com")
# {
#   "target": "https://app.example.com",
#   "pages_crawled": 145,
#   "forms_found": 23,
#   "findings": [
#     {"severity": "critical", "title": "SQL Injection in search"},
#     {"severity": "high", "title": "XSS in comment form"}
#   ]
# }

# Record finding
pt.add_finding(
    title="SQL Injection in Search Endpoint",
    severity=ThreatLevel.CRITICAL,
    description="Unparameterized query in search endpoint allows SQL injection",
    proof="GET /search?q=' OR 1=1-- returns all users",
    impact="Full database compromise, customer data exfiltration",
    remediation="Use parameterized queries or ORM",
    cvss_vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
    cwe_id="CWE-89"
)

# Generate report
report = pt.generate_report(scope["id"])
# {
#   "scope_id": "SCOPE-A1B2C3D4",
#   "executive_summary": "Critical vulnerabilities found...",
#   "methodology": "OWASP Testing Guide v4",
#   "findings_summary": {
#     "critical": 1,
#     "high": 2,
#     "medium": 5,
#     "low": 8
#   },
#   "findings": [...],
#   "remediation_roadmap": [...],
#   "tools_used": ["nmap", "burpsuite", "sqlmap"]
# }
```

### 6. Security Dashboard

```python
agent = SecurityAgent()
dashboard = agent.get_dashboard()
# {
#   "overall_score": {
#     "score": 72,
#     "grade": "C",
#     "risk_level": "medium",
#     "trend": "improving"
#   },
#   "vulnerability_stats": {
#     "total": 156,
#     "open": 45,
#     "in_progress": 12,
#     "resolved": 99,
#     "by_severity": {"critical": 3, "high": 15, "medium": 22, "low": 5}
#   },
#   "threat_model": {
#     "total_threats": 24,
#     "mitigated": 18,
#     "coverage": 0.75
#   },
#   "compliance": {
#     "SOC2": {"score": 85, "grade": "B"},
#     "ISO27001": {"score": 72, "grade": "C"},
#     "PCI_DSS": {"score": 91, "grade": "A"}
#   },
#   "incidents": {
#     "active": 2,
#     "resolved_this_month": 8,
#     "mttr_hours": 4.25,
#     "mttd_hours": 0.5
#   },
#   "pentest": {
#     "last_scan": "2025-01-01",
#     "findings": {"critical": 1, "high": 3, "medium": 7},
#     "remediation_rate": 0.85
#   }
# }
```

## Method Signatures

```python
class SecurityAgent:
    def scan_source(self, code: str, language: str = "python") -> Dict[str, Any]
    def analyze_security(self, code: str, language: str = "python") -> Dict[str, Any]
    def assess_compliance(self, framework: str) -> Dict[str, Any]
    def create_incident(self, title: str, severity: str, description: str, systems: List[str]) -> Dict[str, Any]
    def run_pentest(self, target: str, scope_type: str = "blackbox") -> Dict[str, Any]
    def get_dashboard(self) -> Dict[str, Any]

class VulnerabilityScanner:
    def scan(self, code: str, language: str, scan_types: Optional[List[ScanType]] = None) -> List[Vulnerability]
    def calculate_security_score(self, findings: List[Vulnerability]) -> Dict[str, Any]
    def get_statistics(self) -> Dict[str, Any]
    def add_custom_pattern(self, name: str, pattern: str, severity: ThreatLevel, cwe_id: str) -> None
    def get_scan_history(self) -> List[Dict]

class ThreatModeler:
    def add_component(self, name: str, type: str, trust_level: str, protocols: List[str]) -> Component
    def add_data_flow(self, name: str, source: str, destination: str, protocol: str, encrypted: bool, classification: str) -> DataFlow
    def add_trust_zone(self, name: str, level: int, description: str, requirements: List[str]) -> TrustZone
    def generate_stride_threats(self) -> List[Dict]
    def build_attack_tree(self, target: str) -> Dict
    def get_summary(self) -> Dict
    def calculate_risk_score(self, threats: List[Dict]) -> float

class ComplianceAuditor:
    def assess(self, framework: ComplianceFramework, evidence: Dict[str, Any]) -> Dict
    def generate_report(self, framework: ComplianceFramework, assessment: Dict) -> Dict
    def get_frameworks(self) -> List[ComplianceFramework]
    def get_control_details(self, framework: ComplianceFramework, control_id: str) -> Dict
    def compare_frameworks(self, frameworks: List[ComplianceFramework], evidence: Dict) -> Dict

class IncidentResponder:
    def create_incident(self, title: str, severity: Severity, description: str, affected_systems: List[str]) -> Dict
    def update_status(self, incident_id: str, status: IncidentStatus, notes: Optional[str] = None) -> Dict
    def add_timeline_entry(self, incident_id: str, action: str, user: Optional[str] = None) -> Dict
    def add_containment_action(self, incident_id: str, action: str) -> Dict
    def get_playbook(self, incident_type: str) -> Dict
    def get_summary(self) -> Dict
    def calculate_mttr(self) -> Dict
    def add_ioc(self, incident_id: str, ioc_type: str, value: str, confidence: float) -> Dict

class PenetrationTester:
    def create_scope(self, target: str, scope_type: str, objectives: List[str], constraints: List[str], exclusions: Optional[List[str]] = None) -> Dict
    def run_network_scan(self, target: str) -> Dict
    def run_web_scan(self, target: str) -> Dict
    def add_finding(self, title: str, severity: ThreatLevel, description: str, proof: str, impact: str, remediation: str, cvss_vector: Optional[str] = None, cwe_id: Optional[str] = None) -> PentestFinding
    def generate_report(self, scope_id: str) -> Dict
    def get_findings(self, scope_id: Optional[str] = None) -> List[PentestFinding]
    def get_scope(self, scope_id: str) -> Dict
```

## Data Models

### Vulnerability
| Field | Type | Description |
|-------|------|-------------|
| id | str | Unique identifier (VULN-XXXXXXXX) |
| name | str | Human-readable name |
| type | VulnerabilityType | OWASP category |
| severity | ThreatLevel | CRITICAL=5, HIGH=4, MEDIUM=3, LOW=2, INFO=1 |
| cvss_score | float | 0.0-10.0 (CVSS v3.1) |
| cwe_id | Optional[str] | CWE reference (e.g., CWE-89) |
| status | FindingStatus | OPEN, IN_PROGRESS, RESOLVED, ACCEPTED, FALSE_POSITIVE |
| confidence | float | Detection confidence 0.0-1.0 |
| file_path | Optional[str] | Source file location |
| line_number | Optional[int] | Line number in source |
| description | str | Detailed description |
| recommendation | str | Remediation guidance |
| references | List[str] | CVE, CWE, OWASP links |

### Incident
| Field | Type | Description |
|-------|------|-------------|
| id | str | Format: INC-YYYYMMDD-NNNN |
| title | str | Short description |
| severity | Severity | critical, high, medium, low |
| status | IncidentStatus | Lifecycle state |
| description | str | Detailed incident description |
| affected_systems | List[str] | Systems impacted |
| timeline | List[Dict] | Chronological action log |
| containment_actions | List[str] | Actions taken to contain |
| assigned_to | Optional[str] | Assigned responder |
| created_at | datetime | Detection timestamp |
| resolved_at | Optional[datetime] | Resolution timestamp |
| iocs | List[Dict] | Indicators of compromise |

### PentestFinding
| Field | Type | Description |
|-------|------|-------------|
| id | str | Unique identifier (PF-XXXXXXXX) |
| title | str | Finding title |
| severity | ThreatLevel | CVSS-based severity |
| description | str | Detailed description |
| proof | str | Proof-of-concept |
| impact | str | Business impact |
| remediation | str | Remediation steps |
| cvss_vector | Optional[str] | CVSS vector string |
| cwe_id | Optional[str] | CWE reference |

### ComplianceControl
| Field | Type | Description |
|-------|------|-------------|
| id | str | Control ID (e.g., CC1.1) |
| name | str | Control name |
| framework | ComplianceFramework | Parent framework |
| implemented | bool | Implementation status |
| score | float | 0.0-1.0 |

## Checklist

### Pre-Scan
- [ ] Source code is accessible and complete
- [ ] Language type is correctly specified
- [ ] Scan engines are registered and initialized
- [ ] CVE database is initialized with current data
- [ ] Scan scope is defined (full vs. targeted)
- [ ] Exclusions are configured (test files, vendored code)
- [ ] Output format is specified (JSON, report, dashboard)

### During Scan
- [ ] Each engine executes without errors
- [ ] Findings are deduplicated by (file, line, type)
- [ ] Confidence scores are assigned based on pattern strength
- [ ] Evidence is captured for each finding
- [ ] Progress is logged for long-running scans
- [ ] Memory usage is monitored (large codebases)

### Post-Scan
- [ ] Security score is calculated with correct weights
- [ ] Recommendations are generated per finding
- [ ] Findings are categorized by severity and type
- [ ] Report is produced in requested format
- [ ] Findings are exported to issue tracker (optional)
- [ ] Scan metadata is logged for audit trail

### Incident Response
- [ ] Incident is created with correct severity
- [ ] Playbook is triggered based on incident type
- [ ] Timeline is maintained with timestamped entries
- [ ] Containment actions are recorded
- [ ] Status transitions are logged with before/after
- [ ] IOC are captured and shared with threat intel
- [ ] Post-incident review is scheduled
- [ ] Lessons learned are documented

### Compliance Assessment
- [ ] Evidence dict maps control IDs correctly
- [ ] Partial implementations are scored appropriately
- [ ] Gap analysis identifies high-priority controls
- [ ] Remediation roadmap includes effort estimates
- [ ] Report includes executive summary and technical details
- [ ] Assessment is dated and version-controlled

### Penetration Testing
- [ ] Scope is clearly defined with exclusions
- [ ] Authorization is documented
- [ ] Findings include proof-of-concept
- [ ] CVSS scores are calculated correctly
- [ ] Remediation steps are actionable
- [ ] Report includes executive summary
- [ ] Findings are tracked to remediation

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No findings detected | Verify scan engines are registered; check language parameter |
| Compliance score seems low | Ensure evidence dict maps control IDs correctly |
| Incident not found | Check ID format: INC-YYYYMMDD-NNNN |
| Scan engine fails | Check logs for engine-specific errors; verify code is string |
| CVE database empty | Call `_initialize_cve_database()` or add custom entries |
| Threat model incomplete | Ensure all components and data flows are registered |
| Pentest report empty | Add findings before generating report |
| Security score = 100 with findings | Check severity weights and confidence scores |
| Incident timeline out of order | Timestamps must be in UTC and monotonically increasing |
| Compliance framework not found | Verify enum value exists in ComplianceFramework |
| MTTR calculation returns None | Ensure incidents have both created_at and resolved_at |
| Attack tree too shallow | Add more data flows crossing trust boundaries |

## Security Notes

- The scanner analyzes code as text; it does not execute it
- Secrets detection uses regex patterns; false positives are possible
- Compliance assessments require manual evidence collection
- Penetration test results are simulated; integrate with real tools for production
- All timestamps use UTC via `datetime.now()`
- Incident data should be encrypted at rest in production
- Findings may contain sensitive code snippets; handle with care
- Vulnerability databases should be updated regularly
- Custom patterns may have false positives; validate before remediation
- Reports may be shared with external parties; redact as needed

## Performance Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| Single-file SAST scan | < 500ms | Pre-compiled regex patterns |
| Full security analysis | < 2s | Parallel engine execution |
| Compliance assessment | < 100ms | Cached framework definitions |
| Incident creation | < 50ms | In-memory state |
| Dashboard generation | < 200ms | Cached aggregations |
| Threat model generation | < 150ms | Pre-built templates |
| Pentest report generation | < 300ms | Template-based rendering |

## Integration Guide

```python
# CI/CD Integration
from agents.security.agent import SecurityAgent

agent = SecurityAgent()

def ci_security_gate(code: str, language: str) -> bool:
    """Security gate for CI/CD pipeline"""
    findings = agent.scanner.scan(code, language)
    score = agent.scanner.calculate_security_score(findings)
    
    # Fail build if critical findings
    if score["score"] < 70:
        print(f"Security gate FAILED: Score {score['score']}/100")
        for finding in findings:
            if finding.severity.value >= 4:  # HIGH or CRITICAL
                print(f"  - {finding.name}: {finding.file_path}:{finding.line_number}")
        return False
    
    return True

# Scheduled Compliance Check
def quarterly_compliance():
    """Run quarterly compliance assessments"""
    auditor = ComplianceAuditor()
    frameworks = [ComplianceFramework.SOC2, ComplianceFramework.ISO27001]
    
    results = {}
    for framework in frameworks:
        evidence = collect_evidence(framework)  # Your evidence collection
        result = auditor.assess(framework, evidence)
        results[framework.value] = result
    
    return results
```

---

*Security Agent v2.0 — Part of the Awesome Grok Skills collection.*
