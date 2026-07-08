# Security Agent

Enterprise-grade security operations platform for vulnerability management, threat modeling, incident response, compliance auditing, and penetration testing.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Vulnerability Scanning](#vulnerability-scanning)
  - [Threat Modeling](#threat-modeling)
  - [Compliance Assessment](#compliance-assessment)
  - [Incident Response](#incident-response)
  - [Penetration Testing](#penetration-testing)
  - [Security Dashboard](#security-dashboard)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

The Security Agent provides a comprehensive, modular security operations framework. It orchestrates five specialized subsystems behind a unified `SecurityAgent` facade, enabling end-to-end security workflows from scanning through remediation tracking.

## Features

| Feature | Description |
|---------|-------------|
| **Multi-Engine Scanning** | SAST, secrets detection, dependency analysis, container security |
| **STRIDE Threat Modeling** | Component-based threat generation with attack trees |
| **Multi-Framework Compliance** | SOC2, ISO27001, PCI DSS, HIPAA, NIST, GDPR assessment |
| **Incident Response** | Playbook-driven lifecycle with timeline tracking |
| **Penetration Testing** | Scope management, network/web scanning, finding reports |
| **Unified Dashboard** | Aggregated metrics across all security subsystems |

## Architecture

```
SecurityAgent (Facade)
├── VulnerabilityScanner (SAST + Secrets + SCA + Container)
├── ThreatModeler (STRIDE + Attack Trees)
├── ComplianceAuditor (SOC2, ISO27001, PCI DSS, HIPAA, NIST, GDPR)
├── IncidentResponder (Playbooks + Timeline + IOC)
└── PenetrationTester (Scope + Network/Web Scan + Reports)
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for full details.

## Quick Start

```python
from agents.security.agent import SecurityAgent

agent = SecurityAgent()

# Scan code for vulnerabilities
result = agent.scan_source("your_code_here", "python")
print(f"Score: {result['security_score']['score']}/100")

# Full security analysis
analysis = agent.analyze_security("your_code_here", "python")
print(f"Threats: {analysis['threat_model']['total_threats']}")
```

Run directly:

```bash
python agents/security/agent.py
```

## Usage

### Vulnerability Scanning

```python
from agents.security.agent import SecurityAgent, ScanType

agent = SecurityAgent()

# Scan with all engines
findings = agent.scanner.scan(code, "python")

# Targeted scan (secrets only)
findings = agent.scanner.scan(code, "python", scan_types=[ScanType.SECRETS])

# Calculate security score
score = agent.scanner.calculate_security_score(findings)
# {"score": 45, "grade": "D", "risk_level": "high"}
```

### Threat Modeling

```python
from agents.security.agent import ThreatModeler

tm = ThreatModeler()
tm.add_component("API", "service", "untrusted")
tm.add_component("Database", "storage", "trusted")
tm.add_data_flow("Query", "API", "Database", "SQL", True, "confidential")

threats = tm.generate_stride_threats()
tree = tm.build_attack_tree("Database Server")
summary = tm.get_summary()
```

### Compliance Assessment

```python
from agents.security.agent import ComplianceAuditor, ComplianceFramework

auditor = ComplianceAuditor()
result = auditor.assess(ComplianceFramework.SOC2, {
    "CC1.1": True, "CC6.1": True, "CC7.1": False
})
report = auditor.generate_report(ComplianceFramework.SOC2, result)
```

### Incident Response

```python
from agents.security.agent import IncidentResponder, Severity, IncidentStatus

responder = IncidentResponder()
inc = responder.create_incident(
    "Data Breach", Severity.CRITICAL, "DB compromise", ["db-primary"]
)
responder.update_status(inc.id, IncidentStatus.INVESTIGATING)
responder.add_containment_action(inc.id, "Isolated affected systems")
responder.update_status(inc.id, IncidentStatus.CONTAINED)
```

### Penetration Testing

```python
from agents.security.agent import PenetrationTester, ThreatLevel

pt = PenetrationTester()
scope = pt.create_scope("app.example.com", "blackbox", ["Find RCE"], ["No DoS"])
net = pt.run_network_scan("app.example.com")
web = pt.run_web_scan("https://app.example.com")
pt.add_finding("SQL Injection", ThreatLevel.CRITICAL, "Unparameterized query", "PoC...", "DB compromise", "Use parameterized queries")
report = pt.generate_report(scope["id"])
```

### Security Dashboard

```python
agent = SecurityAgent()
dashboard = agent.get_dashboard()
# {
#   "vulnerability_stats": {...},
#   "threat_model": {...},
#   "compliance": {"SOC2": 85, "ISO27001": 70},
#   "incidents": {...},
#   "overall_score": {"score": 72, "grade": "C"}
# }
```

## API Reference

### SecurityAgent

| Method | Parameters | Returns |
|--------|-----------|---------|
| `scan_source(code, language)` | code: str, language: str | Dict with vulnerabilities and score |
| `analyze_security(code, language)` | code: str, language: str | Full analysis with threats, compliance |
| `assess_compliance(framework)` | framework: str | Compliance assessment result |
| `create_incident(title, severity, desc, systems)` | all str/List[str] | Incident details |
| `run_pentest(target, scope_type)` | target: str, scope_type: str | Pentest results |
| `get_dashboard()` | none | Unified dashboard |

### VulnerabilityScanner

| Method | Description |
|--------|-------------|
| `scan(code, language, scan_types?)` | Run configured scan engines |
| `calculate_security_score(findings)` | Score from 0-100 with grade |
| `get_statistics()` | Aggregate scan metrics |

### ThreatModeler

| Method | Description |
|--------|-------------|
| `add_component(name, type, trust, flows?)` | Register system component |
| `add_data_flow(name, src, dst, proto, enc, class)` | Register data flow |
| `add_trust_zone(name, level, desc, reqs)` | Define trust boundary |
| `generate_stride_threats()` | STRIDE threat generation |
| `build_attack_tree(target)` | Construct attack tree |

### ComplianceAuditor

| Method | Description |
|--------|-------------|
| `assess(framework, evidence)` | Run compliance check |
| `generate_report(framework, assessment)` | Produce compliance report |

### IncidentResponder

| Method | Description |
|--------|-------------|
| `create_incident(title, severity, desc, systems)` | Create incident |
| `update_status(inc_id, status, note?)` | Transition status |
| `add_timeline_entry(inc_id, action, user?)` | Log timeline event |
| `add_containment_action(inc_id, action)` | Record containment |
| `get_playbook(type)` | Retrieve playbook |
| `get_summary()` | Incident metrics |

### PenetrationTester

| Method | Description |
|--------|-------------|
| `create_scope(target, type, objectives, constraints)` | Define test scope |
| `run_network_scan(target)` | Network reconnaissance |
| `run_web_scan(target)` | Web application scan |
| `add_finding(title, severity, desc, proof, impact, remediation)` | Record finding |
| `generate_report(scope_id)` | Produce pentest report |

## Configuration

```python
# Logging configuration
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Custom scan engines
agent.scanner._scan_engines[ScanType.CUSTOM] = my_custom_scanner

# Custom compliance framework
ComplianceAuditor.FRAMEWORKS[ComplianceFramework.CUSTOM] = {
    "CTRL-1": ("Control Name", "Description"),
}
```

## Examples

See the `main()` function in `agent.py` for a complete working example that:
1. Scans vulnerable sample code
2. Runs full security analysis
3. Creates a security incident
4. Executes a penetration test
5. Displays the unified dashboard

## Best Practices

1. **Always specify the language** when scanning - it affects which engines run
2. **Review findings manually** - regex-based detection has false positives
3. **Use playbooks** for incident response consistency
4. **Run compliance assessments quarterly** with fresh evidence
5. **Track findings to resolution** using the status lifecycle
6. **Maintain the CVE database** with current vulnerability data
7. **Scope penetration tests carefully** with explicit constraints

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No findings detected | Verify language parameter; check engine registration |
| Compliance score unexpected | Validate evidence dict keys match framework control IDs |
| Incident ID not found | Format must be INC-YYYYMMDD-NNNN |
| Scan engine error | Check code input is a string; review engine logs |
| Dashboard shows 0 threats | Call `generate_stride_threats()` after adding components |
| Pentest report empty | Add findings before generating report |

## Files

| File | Description |
|------|-------------|
| `agent.py` | Full implementation with all subsystems |
| `ARCHITECTURE.md` | System architecture and design patterns |
| `GROK.md` | Agent identity, capabilities, and API docs |
| `README.md` | This file |

## License

MIT License - See [LICENSE](../../LICENSE) for details.
