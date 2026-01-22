---
name: "Threat Intelligence"
version: "1.0.0"
description: "Advanced threat intelligence collection and analysis"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["threat-intelligence", "ioc", "apt", "adversary"]
category: "hunting"
personality: "intel-analyst"
use_cases: ["ioc-collection", "threat-mapping", "adversary-tracking"]
---

# Threat Intelligence 🔍

> Collect and analyze threat intelligence with Grok's analytical precision

## Overview

This skill provides comprehensive threat intelligence capabilities for hunting and analysis.

## Resources

| Resource | Type | Description |
|----------|------|-------------|
| `threat_intel.py` | Module | Threat intelligence collection and analysis |
| `indicators.yaml` | Data | IOC database and mappings |
| `ttps.json` | Data | MITRE ATT&CK TTPs mapping |

## Quick Start

```python
from threat_intel import ThreatIntelligence

intel = ThreatIntelligence()

# Collect IOCs
indicators = intel.collect_from_feed("https://feed.example.com/iocs")

# Enrich with context
enriched = intel.enrich_indicators(indicators)

# Map to TTPs
ttps_mapped = intel.map_to_attack(enriched)
```
