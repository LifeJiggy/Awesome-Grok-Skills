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
- [Security Considerations](#security-considerations)
- [Performance](#performance)
- [Design Patterns](#design-patterns)
- [Scalability](#scalability)
- [Files](#files)
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

### When to Use

| Scenario | Component |
|----------|-----------|
| Investigating suspicious network traffic | NetworkAnalyzer + LogAnalyzer |
| Correlating IOCs across data sources | IOCManager + ThreatIntelCorrelator |
| Building detection rules | DetectionEngine |
| Managing a threat hunt from hypothesis to report | HuntOrchestrator |
| Triaging incoming security alerts | AlertManager |
| Analyzing anomalous log patterns | LogAnalyzer |

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
│  │                   │  │                   │  │               │  │
│  │ • Add/Remove IOCs │  │ • Ingest logs     │  │ • Flow track  │  │
│  │ • Search/Filter   │  │ • Anomaly detect  │  │ • JA3 match   │  │
│  │ • STIX export     │  │ • Volume analysis │  │ • Lateral move│  │
│  │ • Stats           │  │ • Source tracking │  │ • Top talkers │  │
│  └──────────────────┘  └──────────────────┘  └───────────────┘  │
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐  │
│  │DetectionEngine    │  │HuntOrchestrator   │  │ AlertManager  │  │
│  │                   │  │                   │  │               │  │
│  │ • Sigma rules     │  │ • Hypotheses      │  │ • Triage      │  │
│  │ • Log matching    │  │ • Phase tracking  │  │ • Assignment  │  │
│  │ • Rule stats      │  │ • Report gen      │  │ • Resolution  │  │
│  │ • Effectiveness   │  │ • MITRE mapping   │  │ • SLA track   │  │
│  └──────────────────┘  └──────────────────┘  └───────────────┘  │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │              ThreatIntelCorrelator                         │   │
│  │  • Actor profiles  • IOC correlation  • Active tracking   │   │
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
| STIX export errors | Verify IOC format matches STIX specification |
| JA3 hash mismatch | Check TLS version and cipher suite compatibility |
| Network flow data missing | Ensure pcap capture covers full time range |
| Duplicate alerts | Check dedup window settings; increase if needed |
| Actor correlation fails | Verify IOC format matches actor profile IOCs |
| Rule match rate low | Review log source coverage; adjust pattern matching |

---

## Security Considerations

- IOCs may contain sensitive infrastructure details — handle with care
- Hunt reports may contain classified detection capabilities
- Threat actor profiles should not reveal sources
- STIX exports should be encrypted in transit
- Access to hunt data should be role-based
- Audit trail for all IOC additions and modifications
- Sensitive IOCs (internal IPs) should not be exported to external STIX feeds

---

## Performance

| Operation | Target |
|-----------|--------|
| IOC search | < 10ms for 10K IOCs |
| Anomaly detection | < 100ms per 1K log entries |
| JA3 fingerprint lookup | < 5ms per flow |
| Rule matching | < 50ms per log entry |
| Hunt report generation | < 200ms |
| Alert triage | < 10ms per alert |
| Threat intel correlation | < 50ms per IOC batch |

---

## Design Patterns

| Pattern | Usage | Component |
|---------|-------|-----------|
| **Repository** | IOC storage and retrieval | IOCManager |
| **Strategy** | Multiple anomaly detection algorithms | LogAnalyzer |
| **Observer** | Alert generation on anomaly detection | AlertManager |
| **State Machine** | Hunt lifecycle management | HuntOrchestrator |
| **Template Method** | Report generation | HuntOrchestrator |
| **Facade** | Unified API surface | All components via orchestrator |
| **Chain of Responsibility** | Detection rule matching pipeline | DetectionEngine |

---

## Scalability

| Dimension | Strategy |
|-----------|----------|
| IOC volume | Hash-based indexing for O(1) lookup |
| Log volume | Stream processing with batch aggregation |
| Flow volume | Time-bucketed storage with sampling |
| Rule count | Compiled rule cache for fast matching |
| Alert volume | Severity-based batching and dedup |
| Hunt count | Independent hunt sessions |
| Actor profiles | Indexed by technique and IOC |

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

---

## MITRE ATT&CK Mapping

### Tactic Coverage

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MITRE ATT&CK Coverage Matrix                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Reconnaissance          Resource Development       Initial Access           │
│  ├── T1595 Active Scan   ├── T1583 Acquire Infra   ├── T1190 Exploit Pub   │
│  ├── T1592 Gather Host   ├── T1586 Compromise Acct ├── T1566 Phishing      │
│  └── T1589 Gather Identities                       └── T1133 External Rem   │
│                                                                              │
│  Execution               Persistence               Privilege Escalation     │
│  ├── T1059 Cmd/Script   ├── T1053 Scheduled Task  ├── T1068 Exploitation  │
│  ├── T1203 Exploitation ├── T1547 Boot/Logon      └── T1548 Abuse Elevation│
│  └── T1204 User Exec    └── T1136 Create Account                         │
│                                                                              │
│  Defense Evasion         Credential Access         Discovery                │
│  ├── T1027 Obfuscation  ├── T1003 OS Cred Dump    ├── T1087 Account Disc  │
│  ├── T1070 Indicator    ├── T1110 Brute Force     ├── T1082 System Info   │
│  └── T1562 Impair Defs  └── T1557 Adversary-in-   └── T1046 Network Scan  │
│                              Middle                                        │
│                                                                              │
│  Lateral Movement        Collection                Command and Control      │
│  ├── T1021 Remote Svc   ├── T1005 Data from Local ├── T1071 App Layer P   │
│  ├── T1550 Use Alt Auth ├── T1114 Email Collect   ├── T1572 Protocol Tun  │
│  └── T1570 Lateral Tool ├── T1560 Archive Collected└── T1090 Proxy         │
│                                                                              │
│  Exfiltration            Impact                                                   │
│  ├── T1041 Exfil Over C2├── T1486 Data Encrypted for Impact              │
│  ├── T1567 Exfil Over WS├── T1489 Service Stop                           │
│  └── T1048 Exfil Over Alt└── T1490 Inhibit System Recovery                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Technique-to-Component Mapping

| MITRE Technique | Hunting Component | Detection Method |
|-----------------|-------------------|------------------|
| T1566 Phishing | LogAnalyzer + IOCManager | Email header analysis, URL reputation |
| T1071 C2 | NetworkAnalyzer + LogAnalyzer | JA3 fingerprint, unusual ports |
| T1053 Scheduled Task | DetectionEngine | Registry key monitoring |
| T1003 Credential Dump | DetectionEngine | Process monitoring, file access |
| T1021 Remote Services | NetworkAnalyzer | Lateral movement detection |
| T1046 Network Scan | LogAnalyzer | Port scan detection, volume spikes |
| T1110 Brute Force | LogAnalyzer + AlertManager | Auth failure aggregation |
| T1059 Command Execution | DetectionEngine | Process creation monitoring |
| T1070 Indicator Removal | LogAnalyzer | Log gap detection |
| T1048 Exfiltration | NetworkAnalyzer | Data volume anomaly |

---

## IOC Types Reference

### Supported IOC Formats

| Type | Format Example | Use Case |
|------|----------------|----------|
| IP Address | `198.51.100.23` | C2 server, scanner |
| Domain | `evil-domain.com` | Phishing, C2 |
| URL | `https://evil.com/payload` | Malware download |
| MD5 Hash | `d41d8cd98f00b204e9800998ecf8427e` | File identification |
| SHA1 Hash | `da39a3ee5e6b4b0d3255bfef95601890afd80709` | File identification |
| SHA256 Hash | `e3b0c44298fc1c149afbf4c8996fb924...` | File identification |
| Email | `attacker@evil.com` | Phishing sender |
| CVE | `CVE-2024-12345` | Vulnerability reference |
| JA3 Hash | `e7d705a3286e19ea42f587b344ee6865` | TLS fingerprint |
| CIDR Block | `198.51.100.0/24` | Network range |
| Mutex | `Global\my_mutex` | Malware artifact |
| Registry Key | `HKLM\Software\ Evil` | Persistence mechanism |
| File Path | `C:\Users\Public\svchost.exe` | Malware location |
| User Agent | `Mozilla/4.0 (compatible; evil)` | C2 communication |

### IOC Confidence Scoring

```
Confidence Score = Source_Weight × Age_Decay × Corroboration_Factor

Source Weights:
  Internal detection:     1.0
  Threat intel feed:      0.9
  OSINT research:         0.7
  User reported:          0.5
  Automated scan:         0.6

Age Decay:
  < 24 hours:             1.0
  < 7 days:               0.9
  < 30 days:              0.7
  < 90 days:              0.5
  > 90 days:              0.3

Corroboration:
  Single source:          1.0
  Two sources:            1.2
  Three+ sources:         1.5
```

---

## Sigma Rule Template

```yaml
title: Suspicious Outbound Connection to Known C2 Port
id: a1b2c3d4-e5f6-7890-abcd-ef1234567890
status: stable
description: Detects outbound connections to commonly used C2 ports
author: Threat Hunting Team
date: 2024/01/15
modified: 2024/01/20
tags:
  - attack.command_and_control
  - attack.t1071
logsource:
  category: firewall
  product: network
detection:
  selection:
    action: allow
    dst_port:
      - 4444
      - 5555
      - 6666
      - 8443
      - 443
    direction: outbound
  filter:
    dst_ip:
      - 10.0.0.0/8
      - 172.16.0.0/12
      - 192.168.0.0/16
  condition: selection and not filter
falsepositives:
  - Legitimate admin tools using these ports
  - Development environments
level: high
```

---

## Network Forensics Deep Dive

### JA3 Fingerprint Analysis

```
JA3 Hash = MD5(TLSVersion,Ciphers,Extensions,EllipticCurves,EllipticCurvePointFormats)

Example JA3 Calculation:
  Client Hello:
    TLS Version: 769 (TLS 1.2)
    Ciphers: 4865-4866-4867-49195-49199
    Extensions: 0-23-65281-10-11-35-16-5-13-18-51-45-43-27-21
    Curves: 29-23-24
    Point Formats: 0

  JA3 String: 769,4865-4866-4867-49195-49199,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-21,29-23-24,0
  JA3 Hash: a0e9f5d64349fb13191bc781f81f42e1
```

### Common JA3 Signatures

| JA3 Hash | Application | Risk Level |
|----------|-------------|------------|
| `a0e9f5d64349fb13191bc781f81f42e1` | Chrome | Low |
| `b32309a26951912be7dba376398abc3b` | Firefox | Low |
| `e7d705a3286e19ea42f587b344ee6865` | Cobalt Strike | Critical |
| `72a589da586844d7f0818ce684948eea` | Metasploit | Critical |
| `3b5074b1b5d032e5620f69f9f700ff0e` | Empire | High |
| `未知` | Unknown TLS stack | Investigate |

### Lateral Movement Detection

```
Detection Signals:
  1. Internal host → multiple internal hosts on same port
  2. Unusual service connections (SMB, RDP, WMI between non-admin hosts)
  3. New internal connection pairs not seen in baseline
  4. Connections during unusual hours
  5. Failed authentication followed by successful connection

Scoring:
  score = Σ (signal_weight × signal_confidence)

  Signal Weights:
    New internal pair:        +30
    Unusual hours:            +20
    Failed auth + success:    +25
    High-privilege port:      +15
    Multiple targets:         +20

  Threshold:
    score >= 60 → ALERT (lateral movement suspected)
    score >= 40 → INVESTIGATE
    score < 40  → MONITOR
```

---

## Threat Intelligence Integration

### STIX 2.1 Export Format

```json
{
  "type": "bundle",
  "id": "bundle--a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "objects": [
    {
      "type": "indicator",
      "spec_version": "2.1",
      "id": "indicator--12345678-1234-1234-1234-123456789abc",
      "created": "2024-01-15T10:00:00.000Z",
      "modified": "2024-01-15T10:00:00.000Z",
      "name": "C2 IP Address",
      "description": "Known Cobalt Strike C2 server",
      "pattern": "[ipv4-addr:value = '198.51.100.23']",
      "pattern_type": "stix",
      "valid_from": "2024-01-15T10:00:00.000Z",
      "indicator_types": ["malicious-activity"],
      "confidence": 85,
      "labels": ["c2", "cobalt-strike"]
    }
  ]
}
```

### IOC Enrichment Sources

| Source | Data Type | Refresh Rate | Confidence |
|--------|-----------|--------------|------------|
| Internal Logs | Network flows, auth events | Real-time | High |
| OSINT Feeds | IP/domain reputation | Hourly | Medium |
| Commercial TI | Advanced threat data | Daily | High |
| Industry ISACs | Sector-specific intel | Daily | High |
| DNS Intelligence | Domain resolution history | Hourly | Medium |
| Certificate Transparency | TLS certificate data | Daily | Medium |

### Threat Actor Profile Template

```yaml
actor_profile:
  name: "APT28"
  aliases: ["Fancy Bear", "Sofacy", "Pawn Storm", "Sednit"]
  country: "Russia"
  sophistication: "advanced"
  motivation: "espionage"
  first_seen: "2004"
  last_active: "2024"
  targets:
    - sectors: ["government", "defense", "media"]
    - regions: ["eastern-europe", "central-asia"]
  techniques:
    - tactic: "initial-access"
      technique: "T1566"
      subtechnique: "T1566.001"
      description: "Spearphishing with malicious attachments"
    - tactic: "execution"
      technique: "T1204"
      subtechnique: "T1204.002"
      description: "User execution of malicious document"
  infrastructure:
    - type: "c2"
      indicators: ["198.51.100.0/24"]
    - type: "phishing"
      indicators: ["*.targeted-org.com"]
    tools_used:
      - "X-Agent"
      - "X-Tunnel"
      - "Koadic"
      - "Mimikatz"
```

---

## Log Analysis Deep Dive

### Anomaly Detection Algorithms

```python
# Volume spike detection
def detect_volume_spike(log_counts, baseline_window=24, spike_threshold=3.0):
    """
    Detect volume spikes using z-score method.

    Args:
        log_counts: List of hourly log counts
        baseline_window: Hours to use for baseline calculation
        spike_threshold: Number of standard deviations for spike detection

    Returns:
        List of flagged hours with spike details
    """
    import statistics

    flagged = []
    for i in range(baseline_window, len(log_counts)):
        window = log_counts[i-baseline_window:i]
        mean = statistics.mean(window)
        stdev = statistics.stdev(window) if len(window) > 1 else 0

        if stdev > 0:
            z_score = (log_counts[i] - mean) / stdev
            if z_score > spike_threshold:
                flagged.append({
                    "hour": i,
                    "count": log_counts[i],
                    "baseline_mean": mean,
                    "z_score": round(z_score, 2),
                    "severity": "high" if z_score > 5 else "medium",
                })

    return flagged

# Example usage
hourly_counts = [100, 120, 110, 95, 105, 500, 110, 100]  # Spike at hour 5
spikes = detect_volume_spike(hourly_counts)
```

### DNS Tunnel Detection

```python
# Detect DNS tunneling based on query characteristics
def detect_dns_tunnel(dns_queries):
    """
    Detect DNS tunneling based on:
    - Query length (longer than normal)
    - Subdomain entropy (random characters)
    - Query frequency (high volume to single domain)
    """
    suspicious = []
    for query in dns_queries:
        domain = query["query"]
        subdomain = domain.split(".")[0]

        # Check query length
        if len(domain) > 50:
            suspicious.append({
                "domain": domain,
                "reason": "excessive_length",
                "length": len(domain),
                "risk": "high",
            })

        # Check entropy (random characters)
        entropy = calculate_entropy(subdomain)
        if entropy > 3.5:  # High entropy indicates random data
            suspicious.append({
                "domain": domain,
                "reason": "high_entropy",
                "entropy": round(entropy, 2),
                "risk": "high",
            })

        # Check for encoded data patterns
        if re.match(r'^[a-z0-9]{30,}\.[a-z]+$', domain):
            suspicious.append({
                "domain": domain,
                "reason": "encoded_data_pattern",
                "risk": "medium",
            })

    return suspicious
```
