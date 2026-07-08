# Threat Hunting Agent

> Proactive threat hunting platform for IOC analysis, hypothesis-driven hunting, log analysis, network forensics, APT detection, and MITRE ATT&CK mapping.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

The Hunting Agent provides a complete threat hunting toolkit for security operations centers (SOC) and threat hunting teams. It combines IOC management, hypothesis-driven hunting, log analysis with anomaly detection, network forensics with JA3 fingerprinting, detection engineering with Sigma rules, alert management with triage workflows, and threat intelligence correlation.

### Design Principles

- **Hypothesis-Driven**: Every hunt starts with a testable hypothesis
- **Data-Backed**: All findings supported by evidence
- **MITRE-Aligned**: Map activity to ATT&CK framework
- **Actionable**: Clear recommendations for every finding
- **Measurable**: Track hunt metrics for program improvement

---

## Features

| Feature | Description |
|---------|-------------|
| **IOC Management** | Lifecycle management, STIX export, correlation, search |
| **Log Analysis** | Anomaly detection, volume analysis, source tracking |
| **Network Forensics** | Flow analysis, JA3 fingerprinting, lateral movement detection |
| **Detection Engineering** | Sigma rule creation, matching, effectiveness tracking |
| **Hunt Orchestration** | Hypothesis management, phase tracking, reporting |
| **Alert Management** | Triage, assignment, resolution, SLA tracking |
| **Threat Intelligence** | Actor profiles, IOC correlation, active tracking |
| **MITRE ATT&CK** | Tactic and technique mapping for all activity |

---

## Quick Start

### Installation

```bash
# No external dependencies required
python agents/hunting/agent.py
```

### Basic Usage

```python
from agents.hunting.agent import IOCManager, IOCType, ThreatLevel

ioc_mgr = IOCManager()
ioc_mgr.add_ioc("198.51.100.23", IOCType.IP_ADDRESS, ThreatLevel.HIGH, 85)
active = ioc_mgr.get_active()
```

### First Threat Hunt

```python
from agents.hunting.agent import HuntOrchestrator, MITRETactic

orch = HuntOrchestrator()

# Create a hunt
hunt = orch.create_hunt(
    title="Suspicious Outbound Traffic",
    hypothesis="Internal host communicating with known C2 infrastructure",
    analyst="hunter-1",
    tactic=MITRETactic.COMMAND_AND_CONTROL
)

# Start the hunt
orch.start_hunt(hunt.hunt_id)

# Complete with findings
orch.complete_hunt(hunt.hunt_id, [
    {"finding": "Confirmed C2 communication to 198.51.100.23:4444", "severity": "critical"}
], confirmed=True)

# Generate report
report = orch.generate_report(hunt.hunt_id)
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Hunting Agent (Orchestrator)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐  │
│  │  IOCManager       │  │  LogAnalyzer      │  │NetworkAnalyzer│  │
│  └──────────────────┘  └──────────────────┘  └───────────────┘  │
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐  │
│  │DetectionEngine    │  │HuntOrchestrator   │  │ AlertManager  │  │
│  └──────────────────┘  └──────────────────┘  └───────────────┘  │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │              ThreatIntelCorrelator                         │   │
│  └───────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full system architecture.

---

## Usage

### IOC Management

```python
from agents.hunting.agent import IOCManager, IOCType, ThreatLevel

ioc_mgr = IOCManager()

# Add IOCs
ioc_mgr.add_ioc("198.51.100.23", IOCType.IP_ADDRESS, ThreatLevel.HIGH, 85, "osint")
ioc_mgr.add_ioc("evil-domain.com", IOCType.DOMAIN, ThreatLevel.CRITICAL, 95, "internal")

# Search
results = ioc_mgr.search("evil")

# Filter
high = ioc_mgr.get_high_threat()
active = ioc_mgr.get_active()

# Export STIX
stix = ioc_mgr.export_stix()

# Stats
stats = ioc_mgr.stats()
```

### Log Analysis

```python
from agents.hunting.agent import LogAnalyzer, LogSource, LogEntry

analyzer = LogAnalyzer()
analyzer.add_log(LogEntry(now, LogSource.FIREWALL, "10.0.0.5", "198.51.100.23", 49321, 4444, "TCP"))

# Detect anomalies
flagged = analyzer.detect_anomalies()

# Analyze
by_domain = analyzer.get_volume_by_domain()
summary = analyzer.summary()
```

### Network Forensics

```python
from agents.hunting.agent import NetworkAnalyzer, NetworkFlow, NetworkDirection

net = NetworkAnalyzer()
net.add_flow(NetworkFlow("F1", now, "10.0.0.5", "198.51.100.23", 49321, 4444, "TCP", 100000, 50000, direction=NetworkDirection.OUTBOUND))

# Analyze
top = net.get_top_talkers(10)
ja3 = net.get_ja3_duplicates()
stats = net.stats()
```

### Detection Engineering

```python
from agents.hunting.agent import DetectionEngine, Severity

engine = DetectionEngine()
engine.add_rule("Suspicious Outbound", "firewall", "suspicious_port", Severity.HIGH)
matches = engine.match_logs("SIGMA-0001", logs)
stats = engine.rules_stats()
```

### Alert Management

```python
from agents.hunting.agent import AlertManager, Severity

alerts = AlertManager()
alert = alerts.create_alert("C2 Detected", Severity.CRITICAL, source_ip="10.0.0.5")
alerts.assign(alert.alert_id, "analyst-1")
alerts.resolve(alert.alert_id, notes="Confirmed C2")
stats = alerts.stats()
```

### Threat Intelligence

```python
from agents.hunting.agent import ThreatIntelCorrelator

ti = ThreatIntelCorrelator()
ti.add_actor("APT28", sophistication="advanced", techniques=["T1566", "T1059"], iocs=["198.51.100.23"])
matches = ti.correlate_iocs(["198.51.100.23"])
```

---

## API Reference

| Class | Description |
|-------|-------------|
| `IOCManager` | IOC lifecycle management and STIX export |
| `LogAnalyzer` | Log analysis and anomaly detection |
| `NetworkAnalyzer` | Network flow analysis and JA3 fingerprinting |
| `DetectionEngine` | Sigma rule management and log matching |
| `HuntOrchestrator` | Hunt lifecycle management and reporting |
| `AlertManager` | Alert triage, assignment, and resolution |
| `ThreatIntelCorrelator` | Threat actor profiles and IOC correlation |

### Enums

| Enum | Values |
|------|--------|
| `IOCType` | IP_ADDRESS, DOMAIN, URL, FILE_HASH_MD5, FILE_HASH_SHA1, FILE_HASH_SHA256, EMAIL, MUTEX, REGISTRY_KEY, FILE_PATH, USER_AGENT, CVE, JA3_HASH, CIDR_BLOCK |
| `ThreatLevel` | UNKNOWN, LOW, MEDIUM, HIGH, CRITICAL |
| `IOCStatus` | ACTIVE, EXPIRED, FALSE_POSITIVE, UNDER_REVIEW, ARCHIVED |
| `LogSource` | FIREWALL, IDS_IPS, PROXY, DNS, ENDPOINT, EMAIL, AUTH, CLOUD, APPLICATION, DATABASE |
| `AnomalyType` | VOLUME_SPIKE, NEW_CONNECTION, UNUSUAL_TIME, UNUSUAL_PROTOCOL, DATA_EXFIL, LATERAL_MOVEMENT, PRIVILEGE_ESCALATION, C2_COMMUNICATION, BRUTE_FORCE, DNS_TUNNEL |
| `Severity` | INFO(0), LOW(1), MEDIUM(2), HIGH(3), CRITICAL(4) |
| `HuntPhase` | PLANNING, DATA_COLLECTION, ANALYSIS, INVESTIGATION, REMEDIATION, REPORTING |
| `HuntStatus` | NOT_STARTED, IN_PROGRESS, COMPLETED, BLOCKED, CANCELLED |
| `DetectionStatus` | DRAFT, TESTED, DEPLOYED, TUNING, RETIRED |
| `AlertStatus` | NEW, INVESTIGATING, ESCALATED, RESOLVED, FALSE_POSITIVE |
| `NetworkDirection` | INBOUND, OUTBOUND, LATERAL, INTERNAL |
| `MITRETactic` | RECONNAISSANCE, INITIAL_ACCESS, EXECUTION, PERSISTENCE, PRIVILEGE_ESCALATION, DEFENSE_EVASION, CREDENTIAL_ACCESS, DISCOVERY, LATERAL_MOVEMENT, COLLECTION, COMMAND_AND_CONTROL, EXFILTRATION, IMPACT |

---

## Examples

### Complete Threat Hunt Workflow

```python
from agents.hunting.agent import (
    HuntOrchestrator, IOCManager, LogAnalyzer, NetworkAnalyzer,
    DetectionEngine, AlertManager, ThreatIntelCorrelator,
    MITRETactic, IOCType, ThreatLevel, LogSource, Severity
)
from datetime import datetime

# Initialize all components
ioc_mgr = IOCManager()
log_analyzer = LogAnalyzer()
net = NetworkAnalyzer()
detection = DetectionEngine()
alerts = AlertManager()
orch = HuntOrchestrator()
ti = ThreatIntelCorrelator()

# 1. Add known IOCs
ioc_mgr.add_ioc("198.51.100.23", IOCType.IP_ADDRESS, ThreatLevel.CRITICAL, 95, "threat-intel")
ioc_mgr.add_ioc("evil-domain.com", IOCType.DOMAIN, ThreatLevel.CRITICAL, 95, "threat-intel")

# 2. Ingest logs
now = datetime.utcnow()
log_analyzer.add_log(LogEntry(now, LogSource.FIREWALL, "10.0.0.5", "198.51.100.23", 49321, 4444, "TCP", "allow", 5000000))
log_analyzer.add_log(LogEntry(now, LogSource.DNS, "10.0.0.5", "8.8.8.8", 0, 53, "UDP", "query", 0, query="a" * 100))

# 3. Add network flows
net.add_flow(NetworkFlow("F1", now, "10.0.0.5", "198.51.100.23", 49321, 4444, "TCP", 100000, 50000, direction=NetworkDirection.OUTBOUND))

# 4. Detect anomalies
log_flagged = log_analyzer.detect_anomalies()
net_flagged = net.detect_anomalies()

# 5. Create detection rules
detection.add_rule("C2 Communication", "firewall", "suspicious_port", Severity.CRITICAL)
detection.add_rule("DNS Tunneling", "dns", "dns_tunnel", Severity.HIGH)

# 6. Start a hunt
hunt = orch.create_hunt("C2 Detection", "Internal host communicating with known C2", "analyst", MITRETactic.COMMAND_AND_CONTROL)
orch.start_hunt(hunt.hunt_id)

# 7. Investigate and complete
orch.complete_hunt(hunt.hunt_id, [{"finding": "Confirmed C2 to 198.51.100.23:4444", "severity": "critical"}], confirmed=True)

# 8. Generate report
report = orch.generate_report(hunt.hunt_id)

# 9. Get metrics
print(f"IOCs: {ioc_mgr.stats()}")
print(f"Logs: {log_analyzer.summary()}")
print(f"Network: {net.stats()}")
print(f"Hunts: {orch.hunt_stats()}")
print(f"Alerts: {alerts.stats()}")
```

---

## Configuration

The agent uses sensible defaults. Key configurable parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| Suspicious ports | 4444, 5555, 6666, etc. | Ports flagged as suspicious |
| Data exfil threshold | 10MB | Bytes sent threshold for exfil detection |
| DNS tunnel threshold | 50 chars | Query length for DNS tunnel detection |
| Unusual hours | < 5 or > 23 | Hours outside business operations |
| JA3 duplicate threshold | 2+ hosts | Hosts sharing same JA3 hash |

---

## Best Practices

### IOC Management
1. Always record the source and confidence for every IOC
2. Set expiration dates for time-sensitive IOCs
3. Regularly review and mark false positives
4. Export IOCs in STIX format for sharing

### Hunt Planning
1. Start with a clear, testable hypothesis
2. Identify all required data sources before beginning
3. Map your hypothesis to MITRE ATT&CK tactics
4. Set clear success criteria and timeline

### Detection Engineering
1. Start with high-confidence rules and expand
2. Test rules against known good and bad traffic
3. Monitor false positive rates and tune regularly
4. Document rule logic and expected behavior

### Alert Management
1. Triage alerts by severity and confidence
2. Assign critical alerts immediately
3. Document investigation steps and findings
4. Track mean time to detect and respond

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No IOCs found | Broaden search terms; check IOC format |
| Low anomaly detection | Lower detection thresholds |
| High false positives | Tune rules with exclusions and whitelists |
| Alert fatigue | Adjust severity thresholds; batch low-severity alerts |
| Hunt stalls | Add additional log sources; broaden data collection |
| Report incomplete | Review hunt documentation; ensure findings are recorded |

---

## Files

| File | Description |
|------|-------------|
| `agent.py` | Full implementation (all classes and logic) |
| `GROK.md` | Agent identity, capabilities, and code examples |
| `ARCHITECTURE.md` | System architecture with diagrams |
| `README.md` | This file — overview and quick start |

---

## License

MIT License — see [LICENSE](../../LICENSE) for details.

---

*Hunt proactively, detect early, respond decisively.*