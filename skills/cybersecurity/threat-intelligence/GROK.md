---
name: "threat-intelligence"
category: "cybersecurity"
version: "2.0.0"
tags: ["cybersecurity", "threat-intelligence", "CTI", "MITRE-ATT&CK", "IOCs"]
---

# Threat Intelligence

## Overview

The Threat Intelligence module provides tools for collecting, analyzing, and operationalizing threat intelligence data. It covers IOC management, threat actor profiling, MITRE ATT&CK mapping, threat feed integration, and intelligence-driven defense. The module supports both strategic and tactical intelligence workflows.

This skill is essential for threat intelligence analysts, SOC teams, and security operations centers consuming and producing actionable threat intelligence.

## Core Capabilities

- **IOC Management**: Create, enrich, deduplicate, and share indicators of compromise
- **Threat Actor Profiling**: Actor TTPs, infrastructure, targets, and attribution analysis
- **ATT&CK Mapping**: Map observed behaviors to MITRE ATT&CK techniques and procedures
- **Threat Feeds**: Integrate and normalize threat intelligence feeds (STIX/TAXII, MISP, OTX)
- **Intelligence Analysis**: diamond model analysis, kill chain mapping, and intelligence cycle
- **Detection Rules**: Generate detection rules from threat intelligence (Sigma, YARA, Snort)
- **Sharing**: TLP marking, sharing communities, and intelligence exchange patterns
- **Scoring**: IOC confidence scoring, source reliability, and intelligence quality assessment

## Usage Examples

```python
from threat_intelligence import (
    IOCManager,
    ThreatActorProfiler,
    ATTCKMapper,
    IntelAnalyzer,
    DetectionRuleGenerator,
)

# --- IOC Management ---
ioc_mgr = IOCManager()
ioc = ioc_mgr.create_ioc(
    indicator="185.220.101.34",
    ioc_type="ip_address",
    confidence=85,
    source="internal_analysis",
    tags=["c2", "apt29"],
    tlp="amber",
)
print(f"IOC: {ioc.indicator}")
print(f"Confidence: {ioc.confidence}%")
print(f"Enrichment: {ioc.enrichment}")

# --- Threat Actor Profiling ---
profiler = ThreatActorProfiler()
profile = profiler.profile("APT29")
print(f"Actor: {profile.name}")
print(f"Aliases: {profile.aliases}")
print(f"Attribution: {profile.attribution}")
print(f"Target sectors: {profile.target_sectors}")

# --- ATT&CK Mapping ---
mapper = ATTCKMapper()
techniques = mapper.map_observations([
    "PowerShell execution",
    "Scheduled task creation",
    "Lateral movement via SMB",
])
for t in techniques:
    print(f"  {t.technique_id}: {t.technique_name}")
    print(f"    Tactic: {t.tactic}")
    print(f"    Detection: {t.detection}")

# --- Intel Analysis ---
analyzer = IntelAnalyzer()
analysis = analyzer.diamond_model(
    adversary="APT29",
    capability="Cobalt Strike",
    infrastructure="185.220.101.34",
    victim="government",
)
print(f"Relationships: {len(analysis.relationships)}")

# --- Detection Rules ---
rule_gen = DetectionRuleGenerator()
sigma = rule_gen.generate_sigma(
    technique="T1059.001",
    description="Suspicious PowerShell execution",
    logsource="windows",
)
print(f"Sigma rule: {sigma.rule_name}")
print(f"Detection: {sigma.detection_query[:100]}...")
```

## Best Practices

- Always evaluate source reliability using the Admiralty scale (A-F)
- Mark intelligence with appropriate TLP (Traffic Light Protocol) for sharing
- Focus on actionable intelligence — not all IOCs are equally useful
- Map all observations to MITRE ATT&CK for consistent categorization
- Use multiple sources to corroborate intelligence before acting on it
- Operationalize intelligence by generating detection rules automatically
- Track intelligence lifecycle — IOCs expire and require validation
- Share intelligence with trusted communities to improve collective defense
- Use confidence scoring to prioritize response to highest-confidence threats
- Review and update threat profiles quarterly as actor TTPs evolve

## Related Modules

- **penetration-testing**: Red team validation of threat intelligence
- **security-audit**: Compliance assessment of intelligence programs
- **incident-response**: Intelligence-driven incident response
- **zero-trust-security**: Intelligence-informed zero trust policies
