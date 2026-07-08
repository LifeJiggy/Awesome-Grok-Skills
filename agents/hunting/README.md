# Threat Hunting Agent

> Proactive threat hunting platform for IOC analysis, hypothesis-driven hunting, log analysis, network forensics, APT detection, and MITRE ATT&CK mapping.

---

## Overview

The Hunting Agent provides a complete threat hunting toolkit:

- **IOC Management**: Indicator lifecycle, STIX export, correlation
- **Log Analysis**: Anomaly detection, volume analysis, source tracking
- **Network Forensics**: Flow analysis, JA3 fingerprinting, lateral detection
- **Detection Engineering**: Sigma rule creation, matching, effectiveness tracking
- **Hunt Orchestration**: Hypothesis management, phase tracking, reporting
- **Alert Management**: Triage, assignment, resolution, metrics
- **Threat Intelligence**: Actor profiles, IOC correlation, active tracking

---

## Quick Start

```python
from agents.hunting.agent import IOCManager, IOCType, ThreatLevel

ioc_mgr = IOCManager()
ioc_mgr.add_ioc("198.51.100.23", IOCType.IP_ADDRESS, ThreatLevel.HIGH, 85)
active = ioc_mgr.get_active()
```

### Run the Agent

```bash
python agents/hunting/agent.py
```

---

## Usage

See [GROK.md](GROK.md) for detailed API documentation and examples.

---

## API Reference

| Class | Description |
|-------|-------------|
| `IOCManager` | IOC lifecycle management |
| `LogAnalyzer` | Log analysis and anomaly detection |
| `NetworkAnalyzer` | Network flow analysis |
| `DetectionEngine` | Sigma rule management |
| `HuntOrchestrator` | Hunt lifecycle management |
| `AlertManager` | Alert triage and resolution |
| `ThreatIntelCorrelator` | Threat actor correlation |

---

## Files

- `agent.py` — Full implementation
- `ARCHITECTURE.md` — System architecture
- `GROK.md` — Agent identity and patterns
- `README.md` — This file

---

*Hunt proactively, detect early, respond decisively.*
