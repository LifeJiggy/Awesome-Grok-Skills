# Security Agent

Enterprise-grade security operations platform for vulnerability management, threat modeling, incident response, compliance auditing, and penetration testing.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Vulnerability Scanning](#vulnerability-scanning)
  - [Threat Modeling](#threat-modeling)
  - [Compliance Assessment](#compliance-assessment)
  - [Incident Response](#incident-response)
  - [Penetration Testing](#penetration-testing)
  - [Security Dashboard](#security-dashboard)
- [API Reference](#api-reference)
  - [SecurityAgent](#securityagent)
  - [VulnerabilityScanner](#vulnerabilityscanner)
  - [ThreatModeler](#threatmodeler)
  - [ComplianceAuditor](#complianceauditor)
  - [IncidentResponder](#incidentresponder)
  - [PenetrationTester](#penetrationtester)
- [Configuration](#configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Security Agent provides a comprehensive, modular security operations framework. It orchestrates five specialized subsystems behind a unified `SecurityAgent` facade, enabling end-to-end security workflows from scanning through remediation tracking.

**Key Benefits:**
- Unified security operations across multiple domains
- Defense-in-depth architecture with separation of concerns
- Extensible plugin system for custom scan engines and compliance frameworks
- Automated incident response with playbook-driven workflows
- Comprehensive reporting and dashboarding

**Use Cases:**
- CI/CD security gates for automated vulnerability detection
- Quarterly compliance assessments (SOC2, ISO27001, PCI DSS)
- Incident response coordination and tracking
- Penetration test orchestration and reporting
- Security posture dashboards for executive visibility

## Features

| Feature | Description | Status |
|---------|-------------|--------|
| **Multi-Engine Scanning** | SAST, secrets detection, dependency analysis, container security | Stable |
| **STRIDE Threat Modeling** | Component-based threat generation with attack trees | Stable |
| **Multi-Framework Compliance** | SOC2, ISO27001, PCI DSS, HIPAA, NIST, GDPR assessment | Stable |
| **Incident Response** | Playbook-driven lifecycle with timeline tracking | Stable |
| **Penetration Testing** | Scope management, network/web scanning, finding reports | Stable |
| **Unified Dashboard** | Aggregated metrics across all security subsystems | Stable |
| **Security Scoring** | CVSS-based scoring with grade and risk level | Stable |
| **CVE Management** | Vulnerability database with CWE mapping | Stable |
| **IOC Tracking** | Indicators of compromise linked to incidents | Stable |
| **MTTR Calculation** | Mean Time to Respond/Resolve metrics | Stable |

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SecurityAgent (Facade)                            │
├─────────────┬─────────────┬─────────────┬──────────────┬────────────────────┤
│ Vulnerability│  Threat     │ Compliance  │  Incident    │  Penetration       │
│ Scanner     │  Modeler    │  Auditor    │  Responder   │  Tester            │
├─────────────┼─────────────┼─────────────┼──────────────┼────────────────────┤
│ SAST Engine │ STRIDE      │ SOC2        │ Playbooks    │ Network Scan       │
│ Secrets     │ Attack Tree │ ISO27001    │ Timeline     │ Web Scan           │
│ SCA         │ Trust Zone  │ PCI DSS     │ IOC Tracking │ Scope Management   │
│ Container   │ Data Flow   │ HIPAA       │ MTTR Calc    │ Finding Reports    │
└─────────────┴─────────────┴─────────────┴──────────────┴────────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for full technical details including data flow diagrams, design patterns, and scalability considerations.

## Quick Start

```python
from agents.security.agent import SecurityAgent

agent = SecurityAgent()

# Scan code for vulnerabilities
result = agent.scan_source("your_code_here", "python")
print(f"Score: {result['security_score']['score']}/100")
print(f"Grade: {result['security_score']['grade']}")

# Full security analysis (scan + threats + compliance)
analysis = agent.analyze_security("your_code_here", "python")
print(f"Threats: {analysis['threat_model']['total_threats']}")
print(f"Compliance: {analysis['compliance']}")

# Get unified dashboard
dashboard = agent.get_dashboard()
print(f"Overall Score: {dashboard['overall_score']['score']}/100")
```

Run the demo:

```bash
python agents/security/agent.py
```

## Installation

### Requirements

- Python 3.10+
- No external dependencies (standard library only)

### Setup

```bash
# Clone the repository
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills

# Install in development mode
pip install -e .
```

### Optional Dependencies

```bash
# For real penetration testing integration
pip install python-nmap requests

# For PDF report generation
pip install reportlab

# For email notifications
pip install sendgrid
```

## Usage

### Vulnerability Scanning

```python
from agents.security.agent import SecurityAgent, ScanType

agent = SecurityAgent()

# Scan with all engines
findings = agent.scanner.scan(code, "python")

# Targeted scan (secrets only)
findings = agent.scanner.scan(
    code, "python",
    scan_types=[ScanType.SECRETS]
)

# SAST + Secrets
findings = agent.scanner.scan(
    code, "python",
    scan_types=[ScanType.SAST, ScanType.SECRETS]
)

# Calculate security score
score = agent.scanner.calculate_security_score(findings)
# {
#   "score": 45,
#   "grade": "D",
#   "risk_level": "high",
#   "severity_distribution": {...}
# }

# Add custom detection pattern
agent.scanner.add_custom_pattern(
    name="Custom SQL Pattern",
    pattern=r"query.*\+.*request",
    severity=ThreatLevel.HIGH,
    cwe_id="CWE-89"
)

# Get scan statistics
stats = agent.scanner.get_statistics()
# {
#   "total_scans": 15,
#   "total_findings": 234,
#   "avg_score": 72.5,
#   "by_language": {"python": 10, "javascript": 5}
# }
```

**Supported Scan Types:**
| Engine | Description | Detection Patterns |
|--------|-------------|-------------------|
| SAST | Static Application Security Testing | Injection, XSS, SSRF, path traversal, eval/exec |
| Secrets | Credential Detection | API keys, passwords, tokens, cloud credentials |
| SCA | Software Composition Analysis | Vulnerable dependency versions |
| Container | Container Security | Dockerfile misconfigurations, privilege escalation |

### Threat Modeling

```python
from agents.security.agent import ThreatModeler

tm = ThreatModeler()

# Register system components
tm.add_component("API Gateway", "service", "untrusted", ["HTTPS"])
tm.add_component("Database", "storage", "trusted", ["SQL"])
tm.add_component("Cache", "storage", "trusted", ["Redis"])

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
# [
#   {
#     "component": "API Gateway",
#     "threat_type": "Spoofing",
#     "description": "Attacker impersonates user",
#     "mitigation": "Implement JWT validation",
#     "risk_level": "high"
#   }
# ]

# Build attack tree
tree = tm.build_attack_tree("Database Server")
# {
#   "target": "Database Server",
#   "attack_paths": [...],
#   "total_paths": 4
# }

# Get summary
summary = tm.get_summary()
# {
#   "total_threats": 12,
#   "by_stride": {"spoofing": 2, "tampering": 3, ...},
#   "mitigation_coverage": 0.75
# }
```

### Compliance Assessment

```python
from agents.security.agent import ComplianceAuditor, ComplianceFramework

auditor = ComplianceAuditor()

# Assess SOC2 compliance
result = auditor.assess(ComplianceFramework.SOC2, {
    "CC1.1": True, "CC1.2": True, "CC1.3": False,
    "CC6.1": True, "CC7.1": 0.5
})
# {"score": 62.5, "grade": "D", "implemented": 3, "not_implemented": 1}

# Generate report
report = auditor.generate_report(ComplianceFramework.SOC2, result)
# {
#   "framework": "SOC2",
#   "overall_score": 62.5,
#   "grade": "D",
#   "gaps": [...],
#   "remediation_roadmap": [...]
# }

# Compare multiple frameworks
results = auditor.compare_frameworks(
    [ComplianceFramework.SOC2, ComplianceFramework.ISO27001],
    evidence
)
```

**Supported Frameworks:**
| Framework | Controls | Categories |
|-----------|----------|------------|
| SOC2 | 64 | 9 Trust Service Criteria |
| ISO27001 | 114 | 14 Annex A domains |
| PCI DSS | 281 | 12 Requirements |
| HIPAA | 46 | 6 Safeguard categories |
| NIST CSF | 108 | 5 Functions |
| GDPR | 99 | 11 Chapters |
| CCPA | 23 | 7 Categories |

### Incident Response

```python
from agents.security.agent import IncidentResponder, Severity, IncidentStatus

responder = IncidentResponder()

# Create incident
inc = responder.create_incident(
    title="Data Breach Detected",
    severity=Severity.CRITICAL,
    description="Unauthorized database access",
    affected_systems=["db-primary", "db-replica"]
)
# {"id": "INC-20250101-0001", "status": "OPEN", ...}

# Progress through lifecycle
responder.update_status(inc["id"], IncidentStatus.INVESTIGATING)
responder.add_timeline_entry(inc["id"], "SOC team engaged")
responder.add_containment_action(inc["id"], "Isolated db-replica")
responder.update_status(inc["id"], IncidentStatus.CONTAINED)

# Add IOC
responder.add_ioc(inc["id"], "ip", "203.0.113.42", 0.95)

# Get playbook
playbook = responder.get_playbook("data_breach")
# {"name": "Data Breach Response", "phases": [...]}

# Calculate MTTR
mttr = responder.calculate_mttr()
# {"mttr_hours": 4.25, "mttd_hours": 0.5}
```

### Penetration Testing

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
    description="Unparameterized query",
    proof="GET /search?q=' OR 1=1--",
    impact="Full database compromise",
    remediation="Use parameterized queries",
    cwe_id="CWE-89"
)

# Generate report
report = pt.generate_report(scope["id"])
# {
#   "executive_summary": "Critical vulnerabilities found...",
#   "findings_summary": {"critical": 1, "high": 3, ...},
#   "remediation_roadmap": [...]
# }
```

### Security Dashboard

```python
agent = SecurityAgent()
dashboard = agent.get_dashboard()
# {
#   "overall_score": {"score": 72, "grade": "C", "risk_level": "medium"},
#   "vulnerability_stats": {"total": 156, "open": 45, ...},
#   "threat_model": {"total_threats": 24, "coverage": 0.75},
#   "compliance": {"SOC2": {"score": 85}, "ISO27001": {"score": 72}},
#   "incidents": {"active": 2, "mttr_hours": 4.25},
#   "pentest": {"findings": {"critical": 1, "high": 3}}
# }
```

## API Reference

### SecurityAgent

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `scan_source(code, language)` | code: str, language: str | Dict | Scan code for vulnerabilities |
| `analyze_security(code, language)` | code: str, language: str | Dict | Full analysis with threats + compliance |
| `assess_compliance(framework)` | framework: str | Dict | Compliance assessment |
| `create_incident(title, severity, desc, systems)` | all str/List[str] | Dict | Create security incident |
| `run_pentest(target, scope_type)` | target: str, scope_type: str | Dict | Run penetration test |
| `get_dashboard()` | none | Dict | Unified security dashboard |

### VulnerabilityScanner

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `scan(code, language, scan_types?)` | code, language, Optional[List] | List[Vulnerability] | Run configured scan engines |
| `calculate_security_score(findings)` | findings: List | Dict | Score from 0-100 with grade |
| `get_statistics()` | none | Dict | Aggregate scan metrics |
| `add_custom_pattern(name, pattern, severity, cwe_id)` | str, str, ThreatLevel, str | None | Add custom detection pattern |
| `get_scan_history()` | none | List[Dict] | Past scan results |

### ThreatModeler

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `add_component(name, type, trust, flows?)` | str, str, str, List[str] | Component | Register system component |
| `add_data_flow(name, src, dst, proto, enc, class)` | str, str, str, str, bool, str | DataFlow | Register data flow |
| `add_trust_zone(name, level, desc, reqs)` | str, int, str, List[str] | TrustZone | Define trust boundary |
| `generate_stride_threats()` | none | List[Dict] | STRIDE threat generation |
| `build_attack_tree(target)` | target: str | Dict | Construct attack tree |
| `get_summary()` | none | Dict | Threat model summary |
| `calculate_risk_score(threats)` | threats: List[Dict] | float | Calculate overall risk score |

### ComplianceAuditor

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `assess(framework, evidence)` | ComplianceFramework, Dict | Dict | Run compliance check |
| `generate_report(framework, assessment)` | ComplianceFramework, Dict | Dict | Produce compliance report |
| `get_frameworks()` | none | List | Available frameworks |
| `get_control_details(framework, control_id)` | ComplianceFramework, str | Dict | Get control details |
| `compare_frameworks(frameworks, evidence)` | List[ComplianceFramework], Dict | Dict | Compare multiple frameworks |

### IncidentResponder

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `create_incident(title, severity, desc, systems)` | str, Severity, str, List[str] | Dict | Create incident |
| `update_status(inc_id, status, note?)` | str, IncidentStatus, Optional[str] | Dict | Transition status |
| `add_timeline_entry(inc_id, action, user?)` | str, str, Optional[str] | Dict | Log timeline event |
| `add_containment_action(inc_id, action)` | str, str | Dict | Record containment |
| `add_ioc(inc_id, type, value, confidence)` | str, str, str, float | Dict | Add IOC |
| `get_playbook(type)` | type: str | Dict | Retrieve playbook |
| `get_summary()` | none | Dict | Incident metrics |
| `calculate_mttr()` | none | Dict | Mean Time to Resolve |

### PenetrationTester

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `create_scope(target, type, objectives, constraints, exclusions?)` | str, str, List[str], List[str], Optional[List[str]] | Dict | Define test scope |
| `run_network_scan(target)` | target: str | Dict | Network reconnaissance |
| `run_web_scan(target)` | target: str | Dict | Web application scan |
| `add_finding(title, severity, desc, proof, impact, remediation, ...)` | various | PentestFinding | Record finding |
| `generate_report(scope_id)` | scope_id: str | Dict | Produce pentest report |
| `get_findings(scope_id?)` | Optional[str] | List[PentestFinding] | Get findings |
| `get_scope(scope_id)` | scope_id: str | Dict | Get scope details |

## Configuration

```python
# Logging configuration
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# Custom scan engines
from agents.security.agent import ScanType
agent.scanner._scan_engines[ScanType.CUSTOM] = my_custom_scanner

# Custom compliance framework
from agents.security.agent import ComplianceAuditor, ComplianceFramework
ComplianceAuditor.FRAMEWORKS[ComplianceFramework.CUSTOM] = {
    "CTRL-1": ("Control Name", "Description", "category"),
    "CTRL-2": ("Another Control", "Description", "category"),
}

# Custom severity weights
agent.scanner.SEVERITY_WEIGHTS = {
    "critical": 15,  # Default: 10
    "high": 8,       # Default: 5
    "medium": 3,     # Default: 2
    "low": 1,        # Default: 1
    "info": 0,       # Default: 0
}

# Custom incident playbook
from agents.security.agent import IncidentResponder
IncidentResponder.PLAYBOOKS["custom_incident"] = {
    "name": "Custom Incident Response",
    "phases": [
        {"phase": "Detection", "actions": ["Verify", "Classify"]},
        {"phase": "Response", "actions": ["Contain", "Eradicate"]},
        {"phase": "Recovery", "actions": ["Restore", "Verify"]},
    ]
}
```

## Examples

### CI/CD Security Gate

```python
from agents.security.agent import SecurityAgent

agent = SecurityAgent()

def security_gate(code: str, language: str, max_score: int = 70) -> bool:
    """Security gate for CI/CD pipeline"""
    findings = agent.scanner.scan(code, language)
    score = agent.scanner.calculate_security_score(findings)
    
    if score["score"] < max_score:
        print(f"Security gate FAILED: Score {score['score']}/100")
        for f in findings:
            if f.severity.value >= 4:
                print(f"  - {f.name}: {f.file_path}:{f.line_number}")
        return False
    
    print(f"Security gate PASSED: Score {score['score']}/100")
    return True

# Usage in CI/CD
result = security_gate(source_code, "python")
assert result, "Security gate failed"
```

### Quarterly Compliance Report

```python
from agents.security.agent import ComplianceAuditor, ComplianceFramework

auditor = ComplianceAuditor()
frameworks = [ComplianceFramework.SOC2, ComplianceFramework.ISO27001]

evidence = {
    ComplianceFramework.SOC2: {
        "CC1.1": True, "CC1.2": True, "CC6.1": True, "CC7.1": True
    },
    ComplianceFramework.ISO27001: {
        "A.5.1.1": True, "A.5.1.2": True, "A.8.1.1": True
    }
}

for framework in frameworks:
    result = auditor.assess(framework, evidence[framework])
    report = auditor.generate_report(framework, result)
    print(f"{framework.value}: {report['grade']} ({report['overall_score']}%)")
```

### Incident Response Workflow

```python
from agents.security.agent import IncidentResponder, Severity, IncidentStatus

responder = IncidentResponder()

# Create and manage incident
inc = responder.create_incident(
    title="Ransomware Detection",
    severity=Severity.CRITICAL,
    description="Ransomware detected on file server",
    affected_systems=["fs-primary", "fs-backup"]
)

# Follow playbook
responder.update_status(inc["id"], IncidentStatus.INVESTIGATING)
responder.add_timeline_entry(inc["id"], "Isolated affected systems")
responder.add_containment_action(inc["id"], "Network segmentation applied")
responder.add_ioc(inc["id"], "hash", "abc123def456", 0.99)

# Track resolution
responder.update_status(inc["id"], IncidentStatus.CONTAINED)
responder.update_status(inc["id"], IncidentStatus.ERADICATED)
responder.update_status(inc["id"], IncidentStatus.RECOVERED)

# Post-incident
mttr = responder.calculate_mttr()
print(f"MTTR: {mttr['mttr_hours']} hours")
```

## Best Practices

1. **Always specify the language** when scanning - it affects which engines run
2. **Review findings manually** - regex-based detection has false positives
3. **Use playbooks** for incident response consistency
4. **Run compliance assessments quarterly** with fresh evidence
5. **Track findings to resolution** using the status lifecycle
6. **Maintain the CVE database** with current vulnerability data
7. **Scope penetration tests carefully** with explicit constraints
8. **Update custom patterns** based on new vulnerability disclosures
9. **Document incident timelines** thoroughly for post-incident review
10. **Calculate MTTR regularly** to identify process improvement opportunities
11. **Use the dashboard** for executive visibility into security posture
12. **Integrate with CI/CD** for automated security gates
13. **Train team on playbooks** before incidents occur
14. **Version control** all security configurations and custom patterns
15. **Encrypt sensitive findings** when sharing reports externally

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No findings detected | Verify language parameter; check engine registration |
| Compliance score unexpected | Validate evidence dict keys match framework control IDs |
| Incident ID not found | Format must be INC-YYYYMMDD-NNNN |
| Scan engine error | Check code input is a string; review engine logs |
| Dashboard shows 0 threats | Call `generate_stride_threats()` after adding components |
| Pentest report empty | Add findings before generating report |
| Security score = 100 with findings | Check severity weights and confidence scores |
| Incident timeline out of order | Timestamps must be in UTC and monotonically increasing |
| Compliance framework not found | Verify enum value exists in ComplianceFramework |
| MTTR calculation returns None | Ensure incidents have both created_at and resolved_at |
| Custom pattern not triggering | Verify regex syntax and test against sample code |
| Memory usage high | Reduce scan scope or implement streaming for large codebases |

## Files

| File | Description | Lines |
|------|-------------|-------|
| `agent.py` | Full implementation with all subsystems | ~2000+ |
| `ARCHITECTURE.md` | System architecture and design patterns | ~900 |
| `GROK.md` | Agent identity, capabilities, and API docs | ~900 |
| `README.md` | This file | ~900 |

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run linting
flake8 agents/security/

# Run type checking
mypy agents/security/
```

## License

MIT License - See [LICENSE](../../LICENSE) for details.

## Support

- **Documentation**: See [ARCHITECTURE.md](ARCHITECTURE.md) and [GROK.md](GROK.md)
- **Issues**: GitHub Issues for bug reports and feature requests
- **Discussions**: GitHub Discussions for questions and community support

---

*Security Agent v2.0 — Part of the Awesome Grok Skills collection.*
