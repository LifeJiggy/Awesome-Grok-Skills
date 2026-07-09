# Red Team Agent

A comprehensive offensive security operations framework for authorized penetration testing, adversary simulation, and security assessments. Built with the MITRE ATT&CK framework for tactical and technical mapping.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Reconnaissance](#reconnaissance)
  - [Exploitation](#exploitation)
  - [Post-Exploitation](#post-exploitation)
  - [Adversary Emulation](#adversary-emulation)
  - [C2 Framework](#c2-framework)
- [API Reference](#api-reference)
- [Data Models](#data-models)
- [Design Patterns](#design-patterns)
- [Security](#security)
- [Scalability](#scalability)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Checklists](#checklists)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

The Red Team Agent provides a complete offensive security operations framework that simulates real-world threat actors. It covers the entire attack lifecycle from reconnaissance through reporting, with built-in MITRE ATT&CK mapping and adversary emulation capabilities.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    RED TEAM OPERATION MANAGER                            │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────────┐  │
│  │Reconnaissance│  │   Exploit    │  │      Post-Exploitation       │  │
│  │   Engine     │  │  Development │  │          Engine              │  │
│  │              │  │    Engine     │  │                              │  │
│  │ • Passive    │  │ • RCE        │  │ • Credential harvest         │  │
│  │ • Active     │  │ • LPE        │  │ • Persistence (12+ methods)  │  │
│  │ • Web        │  │ • SQLi/XSS   │  │ • Lateral movement (13)      │  │
│  │ • OSINT      │  │ • Payloads   │  │ • Data exfiltration          │  │
│  └──────────────┘  └──────────────┘  └──────────────────────────────┘  │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────────┐  │
│  │  Adversary   │  │     C2       │  │         Reporting            │  │
│  │  Emulation   │  │  Framework   │  │         Engine               │  │
│  │              │  │              │  │                              │  │
│  │ • APT29/41   │  │ • Listeners  │  │ • Executive summary          │  │
│  │ • Lazarus    │  │ • Beacons    │  │ • MITRE ATT&CK mapping      │  │
│  │ • Custom     │  │ • Tasking    │  │ • Evidence & recommendations │  │
│  │ • MITRE Map  │  │ • Infra      │  │ • Remediation guidance       │  │
│  └──────────────┘  └──────────────┘  └──────────────────────────────┘  │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                 Operation Audit Trail                              │   │
│  │  All actions logged with timestamps for reporting                  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Capabilities

- **Reconnaissance**: Passive OSINT, active scanning, web recon, technology fingerprinting
- **Exploitation**: RCE, LPE, SQLi, XSS, SSRF, command injection, deserialization
- **Post-Exploitation**: Credential harvesting, persistence, lateral movement, data exfiltration
- **Adversary Emulation**: APT29, APT41, Lazarus profiles with MITRE ATT&CK mapping
- **C2 Framework**: Listener management, beacon generation, tasking, infrastructure summary
- **Reporting**: Comprehensive operation reports with findings, evidence, and recommendations

### Use Cases

- External and internal penetration testing
- Adversary simulation exercises
- Red team operations
- Security assessments
- Purple team exercises
- Compliance validation testing
- Incident response preparedness testing

## Features

### Reconnaissance Engine

| Feature | Description |
|---------|-------------|
| Passive Recon | WHOIS, DNS, subdomains, CT logs, OSINT |
| Active Recon | Host discovery, port scanning, service enumeration |
| Web Recon | Technology detection, header analysis, form discovery |
| OSINT | Social media, code repos, leaked credentials |

### Exploit Development

| Feature | Description |
|---------|-------------|
| RCE Exploits | Path traversal, CGI, deserialization |
| LPE Exploits | SUID abuse, kernel exploits, token manipulation |
| Web Exploits | SQLi, XSS, SSRF, command injection |
| Payload Generation | Reverse shells, shellcode, obfuscation |

### Post-Exploitation

| Feature | Description |
|---------|-------------|
| Credential Harvesting | Registry, memory, LSASS, files |
| Persistence | 12+ methods across Windows/Linux |
| Lateral Movement | 13 methods including Kerberos attacks |
| Data Exfiltration | DNS, HTTPS, ICMP, covert channels |

### Adversary Emulation

| Feature | Description |
|---------|-------------|
| Threat Actor Profiles | APT29, APT41, Lazarus + custom |
| MITRE ATT&CK Mapping | 14 tactics, 30+ techniques |
| Emulation Planning | Tactic sequencing, technique selection |
| Finding Correlation | Map findings to ATT&CK framework |

## Architecture

### Component Interaction

```
                    ┌─────────────────┐
                    │  RedTeamOp      │
                    │  Manager        │
                    │  (Facade)       │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
    ┌───────▼──────┐ ┌──────▼──────┐ ┌───────▼──────┐
    │Reconnaissance│ │   Exploit   │ │Post-Exploit  │
    │   Engine     │ │  Development│ │   Engine     │
    └───────┬──────┘ └──────┬──────┘ └───────┬──────┘
            │                │                │
            └────────────────┼────────────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
    ┌───────▼──────┐ ┌──────▼──────┐ ┌───────▼──────┐
    │  Adversary   │ │     C2      │ │  Reporting   │
    │  Emulation   │ │  Framework  │ │   Engine     │
    └──────────────┘ └─────────────┘ └──────────────┘
```

### Attack Lifecycle Flow

```
Reconnaissance ──▶ Weaponization ──▶ Delivery ──▶ Exploitation
                                                      │
Reporting ◀──── Cleanup ◀──── Post-Exploit ◀──── Installation
```

For detailed architecture documentation, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/awesome-grok-skills/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills

# Install dependencies (if any)
pip install -r requirements.txt
```

### Basic Usage

```python
from agents.redteam.agent import RedTeamOperationManager

# Initialize the manager
manager = RedTeamOperationManager()

# Start an operation
op_id = manager.start_operation(
    name="My Penetration Test",
    targets=["example.com"],
    objectives=["Gain initial access", "Access sensitive data"]
)

# Execute the operation
results = manager.execute_operation(op_id)

# Generate a report
report = manager.generate_report(op_id)

print(f"Findings: {len(report.findings)}")
print(f"Recommendations: {len(report.recommendations)}")
```

### Run the Agent

```bash
python agents/redteam/agent.py
```

## Usage

### Reconnaissance

```python
from agents.redteam.agent import ReconnaissanceEngine

recon = ReconnaissanceEngine()

# Passive recon
results = recon.passive_recon("example.com")
print(f"Subdomains found: {len(results['subdomains'])}")
print(f"Technologies: {results['technologies']}")

# Active recon
results = recon.active_recon("192.168.1.0/24")
print(f"Hosts discovered: {len(results['hosts_discovered'])}")

# Web recon
results = recon.web_recon("https://example.com")
print(f"API endpoints: {results['api_endpoints']}")
```

### Exploitation

```python
from agents.redteam.agent import ExploitDevelopmentEngine

engine = ExploitDevelopmentEngine()

# Develop an exploit
vulnerability = {"type": "rce", "cve": "CVE-2021-41773"}
target = {"url": "http://target.com", "lhost": "10.10.14.5", "lport": 4444}

result = engine.develop_exploit(vulnerability, target)
print(f"Exploit success: {result.success}")
print(f"Access gained: {result.access_gained}")

# Generate payload
payload = engine.generate_payload("reverse_shell_bash", {
    "lhost": "10.10.14.5",
    "lport": 4444
})
print(f"Payload: {payload}")
```

### Post-Exploitation

```python
from agents.redteam.agent import (
    PostExploitationEngine, SessionType,
    PersistenceMethod, LateralMovementMethod
)

post = PostExploitationEngine()

# Establish session
session_id = post.establish_session(
    target="192.168.1.10",
    session_type=SessionType.REVERSE_SHELL
)

# Harvest credentials
creds = post.gather_credentials(session_id)
for cred in creds:
    print(f"Found: {cred.username} from {cred.source}")

# Deploy persistence
post.establish_persistence(
    session_id=session_id,
    method=PersistenceMethod.SCHEDULED_TASK
)

# Lateral movement
pivot = post.lateral_movement(
    session_id=session_id,
    target="192.168.1.20",
    method=LateralMovementMethod.PS_EXEC
)
```

### Adversary Emulation

```python
from agents.redteam.agent import AdversaryEmulationEngine

emulation = AdversaryEmulationEngine()

# List available profiles
print(emulation.list_profiles())  # ['APT29', 'APT41', 'Lazarus']

# Get profile details
apt29 = emulation.get_profile("APT29")
print(f"Tactics: {[t.value for t in apt29['tactics']]}")

# Create emulation plan
plan = emulation.emulate("APT29", "target.com", ["data exfiltration"])
```

### C2 Framework

```python
from agents.redteam.agent import C2Framework

c2 = C2Framework()

# Create listener
listener_id = c2.create_listener("HTTPS", "10.10.14.5", 443, "https")

# Generate beacon
beacon_id = c2.generate_beacon(listener_id, {"sleep_time": 30})

# Task beacon
task_id = c2.task_beacon(beacon_id, "shell", ["cmd.exe"])

# Check status
status = c2.get_beacon_status(beacon_id)
```

## API Reference

### RedTeamOperationManager

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `start_operation()` | name, targets, objectives, threat_actor? | str (op_id) | Start a new operation |
| `execute_operation()` | op_id | Dict | Execute the full operation lifecycle |
| `generate_report()` | op_id | OperationReport | Generate comprehensive report |
| `cleanup_operation()` | op_id | Dict | Clean up all artifacts |

### ReconnaissanceEngine

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `passive_recon()` | target_domain | Dict | Passive reconnaissance |
| `active_recon()` | target_range | Dict | Active reconnaissance |
| `web_recon()` | target_url | Dict | Web application recon |
| `osint_gathering()` | organization | Dict | OSINT gathering |

### ExploitDevelopmentEngine

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `develop_exploit()` | vulnerability, target_info | ExploitResult | Develop an exploit |
| `generate_payload()` | payload_type, options | str | Generate payload |
| `generate_shellcode()` | arch, payload_type, options | bytes | Generate shellcode |
| `generate_obfuscated_payload()` | payload, technique | str | Obfuscate payload |

### PostExploitationEngine

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `establish_session()` | target, session_type, access_level? | str (session_id) | Create session |
| `kill_session()` | session_id | bool | Terminate session |
| `gather_credentials()` | session_id, methods? | List[Credential] | Harvest credentials |
| `establish_persistence()` | session_id, method, options? | PersistenceEntry | Deploy persistence |
| `lateral_movement()` | session_id, target, method, credential? | Pivot | Move laterally |
| `exfiltrate_data()` | session_id, files, method, destination? | Dict | Exfiltrate data |
| `cleanup_persistence()` | session_id | List[str] | Clean persistence |

## Data Models

### Operation
Core operation record with targets, objectives, status, and timeline.

### Finding
Security finding with severity, evidence, MITRE ATT&CK mapping, and remediation.

### Session
Active session with target, type, access level, and persistence status.

### Credential
Harvested credential with username, source, type, and hash.

### EmulationPlan
Adversary emulation plan with tactics, techniques, and sequencing.

## Design Patterns

| Pattern | Usage | Component |
|---------|-------|-----------|
| **Strategy** | Multiple recon methods | ReconnaissanceEngine |
| **State Machine** | Operation lifecycle | RedTeamOperationManager |
| **Facade** | Unified red team interface | RedTeamOperationManager |
| **Observer** | Notify on findings | ReportingEngine |
| **Builder** | Construct complex exploits | ExploitDevelopmentEngine |

## Security

- All operations require explicit authorization
- Scope restrictions enforced on all actions
- Audit trail for every operation action
- Credential handling follows best practices
- Cleanup verification before operation close
- Data handling compliance with engagement rules

## Scalability

| Dimension | Strategy | Notes |
|-----------|----------|-------|
| Operations | Indexed by status + date | Fast filtered queries |
| Findings | Indexed by severity + MITRE | Efficient triage |
| Sessions | Partitioned by operation | Isolation |
| Reports | Generated on demand | Configurable detail |

## Examples

### Full Penetration Test

```python
from agents.redteam.agent import RedTeamOperationManager

manager = RedTeamOperationManager()

# Phase 1: Recon
op_id = manager.start_operation(
    name="Full Pen Test",
    targets=["corp.example.com", "10.0.0.0/16"],
    objectives=["Domain admin", "Access customer database"]
)

results = manager.execute_operation(op_id)

# Phase 2: Report
report = manager.generate_report(op_id)

# Print executive summary
print(report.executive_summary)

# Print findings
for finding in report.findings:
    print(f"[{finding.severity.value}] {finding.title}")

# Phase 3: Cleanup
manager.cleanup_operation(op_id)
```

### Adversary Emulation Exercise

```python
from agents.redteam.agent import RedTeamOperationManager

manager = RedTeamOperationManager()

op_id = manager.start_operation(
    name="APT29 Emulation",
    targets=["target.com"],
    objectives=["Simulate APT29 TTPs"],
    threat_actor="APT29"
)

results = manager.execute_operation(op_id)

# Review MITRE ATT&CK mapping
report = manager.generate_report(op_id)
for technique, findings in report.mitre_mapping.items():
    print(f"{technique}: {len(findings)} findings")
```

### Custom Adversary Profile

```python
from agents.redteam.agent import (
    AdversaryEmulationEngine, TacticID, TechniqueID
)

emulation = AdversaryEmulationEngine()

# Add custom profile
emulation.profiles["CustomAPT"] = {
    "name": "Custom APT",
    "origin": "Unknown",
    "tactics": [TacticID.INITIAL_ACCESS, TacticID.EXECUTION],
    "techniques": [TechniqueID.PHISHING, TechniqueID.COMMAND_SCRIPT_INTERPRETER],
    "tools": ["custom_tool_1", "custom_tool_2"],
    "preferred_persistence": [],
}

plan = emulation.emulate("CustomAPT", "target.com", ["data theft"])
```

## Configuration

### Operation Settings

```yaml
operation:
  max_concurrent_sessions: 10
  session_timeout: 3600
  auto_cleanup: true
```

### Reconnaissance Settings

```yaml
reconnaissance:
  passive_timeout: 30
  active_scan_rate: 100  # packets per second
  port_range: "1-65535"
  common_ports_only: true
```

### Exploitation Settings

```yaml
exploitation:
  max_exploit_attempts: 3
  payload_timeout: 10
  obfuscation_level: "medium"
```

### C2 Settings

```yaml
c2:
  default_protocol: "https"
  beacon_sleep: 60
  jitter_percent: 30
  encryption: "aes256"
```

## Best Practices

### Before the Operation

1. **Define Clear Scope** -- Explicitly list all targets and boundaries
2. **Get Written Authorization** -- Ensure RoE is signed
3. **Prepare Infrastructure** -- Set up C2 and exfiltration channels
4. **Establish Communication** -- Set up out-of-band comms
5. **Test Your Tools** -- Verify all exploits and payloads work

### During the Operation

1. **Document Everything** -- Log every action and finding
2. **Maintain OPSEC** -- Use proper tradecraft
3. **Stay in Scope** -- Never test outside authorized boundaries
4. **Monitor for Detection** -- Watch for blue team activity
5. **Adapt Your Approach** -- Change TTPs if detected

### After the Operation

1. **Clean Up** -- Remove all persistence and artifacts
2. **Verify Cleanup** -- Double-check nothing was left behind
3. **Write the Report** -- Include all findings with evidence
4. **Brief Stakeholders** -- Present findings to leadership
5. **Track Remediation** -- Follow up on fix implementation

### Reporting Guidelines

- Start with the executive summary
- Group findings by severity
- Include reproduction steps for every finding
- Provide clear remediation recommendations
- Map findings to MITRE ATT&CK
- Include evidence (screenshots, logs, payloads)
- Suggest remediation timelines

## Checklists

### Pre-Engagement

- [ ] Rules of Engagement (RoE) signed
- [ ] Scope explicitly defined
- [ ] Emergency contacts established
- [ ] Infrastructure tested
- [ ] Communication channels set up
- [ ] Legal review completed
- [ ] Insurance verified

### During Engagement

- [ ] Every action logged with timestamp
- [ ] Findings documented immediately
- [ ] Scope respected at all times
- [ ] OPSEC maintained
- [ ] Regular status updates to stakeholders
- [ ] Evidence properly handled

### Post-Engagement

- [ ] All persistence removed
- [ ] All credentials rotated
- [ ] Cleanup verified independently
- [ ] Report delivered on time
- [ ] Remediation tracking initiated
- [ ] Lessons learned documented

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Session drops immediately | Firewall blocking | Use DNS/HTTPS covert channels |
| No credentials harvested | Insufficient privileges | Try LPE first |
| Persistence detected by AV | Known signatures | Use living-off-the-land techniques |
| Lateral movement fails | Network segmentation | Pivot through existing access |
| C2 beacon not checking in | Network filtering | Try alternative protocol |
| Report missing data | Findings not logged | Review operation logs |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Tuning

| Parameter | Default | Range | Impact |
|-----------|---------|-------|--------|
| Session timeout | 3600s | 300-7200 | Longer = more persistent |
| Beacon sleep | 60s | 30-300 | Shorter = faster response |
| Jitter | 30% | 10-50% | Higher = more stealth |
| Scan rate | 100 pps | 50-500 | Higher = faster recon |

## Files

- `agent.py` - Main implementation with all engines and operation management
- `ARCHITECTURE.md` - System architecture, data flow, and design patterns
- `GROK.md` - Agent instructions, capabilities, and workflow checklists
- `README.md` - This file

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see [LICENSE](../../LICENSE) for details.

## Disclaimer

This tool is provided for authorized security testing purposes only. Always obtain proper authorization before performing any security testing. The authors are not responsible for any misuse of this tool.
