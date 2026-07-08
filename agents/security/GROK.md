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
---

# Security Agent

> Enterprise-grade security architecture, threat modeling, vulnerability management, incident response, and compliance automation.

## Identity

The Security Agent is a defense-in-depth security operations platform. It combines static analysis scanning, STRIDE-based threat modeling, multi-framework compliance assessment, automated incident response with playbooks, and penetration test orchestration behind a unified facade.

**Core principle:** Every finding must be actionable. Every incident must have a timeline. Every scan must produce a score.

## Principles

1. **Defense in Depth** - Multiple overlapping security controls
2. **Least Privilege** - Every component operates with minimum required access
3. **Fail Secure** - Errors default to secure state, never expose internals
4. **Audit Everything** - All actions are timestamped and attributed
5. **Risk-Based Prioritization** - Severity drives response urgency
6. **Automation First** - Manual processes are technical debt

## Capabilities

### 1. Vulnerability Scanning

```python
from agents.security.agent import SecurityAgent, ScanType

agent = SecurityAgent()

# Full scan with all engines
findings = agent.scanner.scan(code, language="python")

# Targeted scan
findings = agent.scanner.scan(
    code,
    language="python",
    scan_types=[ScanType.SAST, ScanType.SECRETS]
)

# Security score
score = agent.scanner.calculate_security_score(findings)
# {"score": 45, "grade": "D", "risk_level": "high", "status": "Poor"}
```

**Supported scan types:**
| Engine | Detection |
|--------|-----------|
| SAST | SQL injection, command injection, XSS, SSRF, path traversal |
| Secrets | API keys, passwords, tokens, cloud credentials |
| SCA | Vulnerable dependency versions |
| Container | Dockerfile security misconfigurations |

### 2. Threat Modeling

```python
from agents.security.agent import ThreatModeler

tm = ThreatModeler()

# Register system components
tm.add_component("API Gateway", "service", "untrusted", ["HTTPS"])
tm.add_component("Database", "storage", "trusted", ["SQL"])

# Add data flows
tm.add_data_flow(
    name="User Request",
    source="Frontend",
    destination="API Gateway",
    protocol="HTTPS",
    encrypted=True,
    classification="confidential"
)

# Generate STRIDE threats
threats = tm.generate_stride_threats()

# Build attack tree
tree = tm.build_attack_tree("Production Database")
```

### 3. Compliance Assessment

```python
from agents.security.agent import ComplianceAuditor, ComplianceFramework

auditor = ComplianceAuditor()

# Assess SOC2 compliance
result = auditor.assess(
    ComplianceFramework.SOC2,
    evidence={"CC1.1": True, "CC6.1": True, "CC7.1": False}
)
# {"score": 50.0, "implemented": 2, "not_implemented": 1}

# Generate report
report = auditor.generate_report(ComplianceFramework.SOC2, result)
```

**Supported frameworks:** SOC2, ISO27001, PCI DSS, HIPAA, NIST, GDPR, CCPA

### 4. Incident Response

```python
from agents.security.agent import IncidentResponder, Severity, IncidentStatus

responder = IncidentResponder()

# Create incident
inc = responder.create_incident(
    title="Data Breach Detected",
    severity=Severity.CRITICAL,
    description="Unauthorized database access detected",
    affected_systems=["db-primary", "db-replica"]
)
# INC-20250101-1234

# Progress through lifecycle
responder.update_status(inc.id, IncidentStatus.INVESTIGATING, "SOC team engaged")
responder.add_timeline_entry(inc.id, "Blocked attacker IP", user="analyst")
responder.add_containment_action(inc.id, "Isolated db-replica from network")
responder.update_status(inc.id, IncidentStatus.CONTAINED)

# Get playbook
playbook = responder.get_playbook("data_breach")
```

**Incident lifecycle:**
```
OPEN → TRIAGED → INVESTIGATING → CONTAINED → ERADICATED → RECOVERED → CLOSED
```

### 5. Penetration Testing

```python
from agents.security.agent import PenetrationTester, ThreatLevel

pt = PenetrationTester()

# Define scope
scope = pt.create_scope(
    target="https://app.example.com",
    scope_type="blackbox",
    objectives=["Find RCE", "Test auth bypass"],
    constraints=["No DoS", "No data access"]
)

# Run scans
net = pt.run_network_scan("app.example.com")
web = pt.run_web_scan("https://app.example.com")

# Record finding
pt.add_finding(
    title="SQL Injection in Search",
    severity=ThreatLevel.CRITICAL,
    description="Unparameterized query in search endpoint",
    proof="GET /search?q=' OR 1=1-- returns all users",
    impact="Full database compromise",
    remediation="Use parameterized queries"
)

# Generate report
report = pt.generate_report(scope["id"])
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
```

## Data Models

### Vulnerability
| Field | Type | Description |
|-------|------|-------------|
| id | str | Unique identifier |
| name | str | Human-readable name |
| type | VulnerabilityType | OWASP category |
| severity | ThreatLevel | CRITICAL=5, HIGH=4, MEDIUM=3, LOW=2, INFO=1 |
| cvss_score | float | 0.0-10.0 |
| cwe_id | Optional[str] | CWE reference |
| status | FindingStatus | OPEN, IN_PROGRESS, RESOLVED, ACCEPTED, FALSE_POSITIVE |
| confidence | float | Detection confidence 0.0-1.0 |

### Incident
| Field | Type | Description |
|-------|------|-------------|
| id | str | Format: INC-YYYYMMDD-NNNN |
| severity | Severity | critical, high, medium, low |
| status | IncidentStatus | Lifecycle state |
| timeline | List[Dict] | Chronological action log |
| containment_actions | List[str] | Actions taken |

## Checklist

### Pre-Scan
- [ ] Source code is accessible and complete
- [ ] Language type is correctly specified
- [ ] Scan engines are registered
- [ ] CVE database is initialized

### During Scan
- [ ] Each engine executes without errors
- [ ] Findings are deduplicated
- [ ] Confidence scores are assigned
- [ ] Evidence is captured

### Post-Scan
- [ ] Security score is calculated
- [ ] Recommendations are generated
- [ ] Findings are categorized by severity
- [ ] Report is produced

### Incident Response
- [ ] Incident is created with correct severity
- [ ] Playbook is triggered
- [ ] Timeline is maintained
- [ ] Containment actions are recorded
- [ ] Status transitions are logged

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No findings detected | Verify scan engines are registered; check language parameter |
| Compliance score seems low | Ensure evidence dict maps control IDs correctly |
| Incident not found | Check ID format: INC-YYYYMMDD-NNNN |
| Scan engine fails | Check logs for engine-specific errors; verify code is string |
| CVE database empty | Call `_initialize_cve_database()` or add custom entries |

## Security Notes

- The scanner analyzes code as text; it does not execute it
- Secrets detection uses regex patterns; false positives are possible
- Compliance assessments require manual evidence collection
- Penetration test results are simulated; integrate with real tools for production
- All timestamps use UTC via `datetime.now()`
