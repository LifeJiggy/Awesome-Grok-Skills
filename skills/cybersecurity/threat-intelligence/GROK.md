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

---

## Advanced Configuration

### Threat Feed Configuration

Configure multiple threat intelligence feeds.

```python
feed_config = ThreatFeedConfig(
    feeds={
        "otx": {"api_key": "...", "update_interval": 3600},
        "misp": {"url": "https://misp.internal", "api_key": "..."},
        "virustotal": {"api_key": "...", "rate_limit": 4},
        "abuseipdb": {"api_key": "...", "confidence_threshold": 75},
    },
    normalization_rules={
        "ip_address": {"validate": True, "enrich": True},
        "domain": {"validate": True, "whois": True},
        "hash": {"validate": True, "sandbox": True},
    },
)
```

### IOC Scoring Configuration

Configure IOC confidence scoring.

```python
ioc_scoring = IOCScoringConfig(
    scoring_model="admiralty",
    source_reliability={
        "A": {"score": 1.0, "description": "Completely reliable"},
        "B": {"score": 0.8, "description": "Usually reliable"},
        "C": {"score": 0.6, "description": "Fairly reliable"},
        "D": {"score": 0.4, "description": "Not usually reliable"},
        "E": {"score": 0.2, "description": "Unreliable"},
        "F": {"score": 0.1, "description": "Cannot be judged"},
    },
    information_credibility={
        "1": {"score": 1.0, "description": "Confirmed"},
        "2": {"score": 0.8, "description": "Probably true"},
        "3": {"score": 0.6, "description": "Possibly true"},
        "4": {"score": 0.4, "description": "Doubtful"},
        "5": {"score": 0.2, "description": "Improbable"},
    },
)
```

### TLP Configuration

Configure Traffic Light Protocol settings.

```python
tlp_config = TLPConfig(
    levels={
        "WHITE": {"sharing": "unrestricted", "description": "Public disclosure"},
        "GREEN": {"sharing": "community", "description": "Community-wide sharing"},
        "AMBER": {"sharing": "organization", "description": "Limited disclosure"},
        "AMBER_STRICT": {"sharing": "need_to_know", "description": "Strict need-to-know"},
        "RED": {"sharing": "individual", "description": "Named recipients only"},
    },
    default_level="AMBER",
)
```

---

## Architecture Patterns

### Intelligence Cycle Pattern

```python
class IntelligenceCycle:
    phases = [
        "planning",
        "collection",
        "processing",
        "analysis",
        "dissemination",
        "feedback",
    ]

    def execute(self, requirement):
        context = {"requirement": requirement, "intelligence": []}
        for phase in self.phases:
            handler = self.get_phase_handler(phase)
            context = handler.execute(context)
        return context['intelligence']
```

### Diamond Model Pattern

```python
class DiamondModel:
    def __init__(self):
        self.adversary = None
        self.infrastructure = None
        self.capability = None
        self.victim = None

    def analyze(self, event):
        self.adversary = self.extract_adversary(event)
        self.infrastructure = self.extract_infrastructure(event)
        self.capability = self.extract_capability(event)
        self.victim = self.extract_victim(event)
        return self.generate_relationships()
```

### STIX/TAXII Pattern

```python
class STIXTAXIIClient:
    def __init__(self, taxii_server, username, password):
        self.client = TAXIIClient(taxii_server, username, password)

    def get_indicators(self, collection):
        stix_objects = self.client.get_collection_objects(collection)
        return [self.parse_stix_object(obj) for obj in stix_objects]

    def create_indicator(self, indicator):
        stix_object = self.to_stix(indicator)
        self.client.add_objects(stix_object)
```

---

## Integration Guide

### MISP Integration

```python
import pymisp

misp = pymisp.ExpandedPyMISP("https://misp.internal", "...")

# Get events
events = misp.search(controller="events", tags=["apt29"])

# Create indicator
indicator = pymisp.MISPAttribute()
indicator.type = "ip-dst"
indicator.value = "185.220.101.34"
misp.add_attribute(event_id, indicator)
```

### YARA Rule Integration

```python
import yara

rules = yara.compile(filepath="malware_rules.yar")

# Scan file
matches = rules.match("suspicious_file.exe")
for match in matches:
    print(f"Rule: {match.rule}, Tags: {match.tags}")
```

### Sigma Rule Integration

```python
# Convert Sigma to Splunk query
sigma_cli = SigmaCLI()
splunk_query = sigma_cli.convert(
    rule="suspicious_powershell.yml",
    backend="splunk",
)
```

---

## Performance Optimization

### IOC Cache

```python
# Cache IOC lookups
ioc_cache = IOCCache(
    backend="redis",
    ttl_seconds=3600,
    max_entries=100000,
)
```

### Batch Processing

```python
# Process IOCs in batch
def batch_process_iocs(iocs, batch_size=1000):
    for i in range(0, len(iocs), batch_size):
        batch = iocs[i:i+batch_size]
        process_batch(batch)
```

---

## Security Considerations

### Intelligence Sharing Security

```python
# Secure intelligence sharing
class IntelShareSecurity:
    def __init__(self):
        self.encryption = EncryptionManager()
        self.access_control = AccessControl()

    def share(self, intelligence, recipients, tlp_level):
        if not self.access_control.can_share(tlp_level, recipients):
            raise SharingViolation("TLP violation")
        encrypted = self.encryption.encrypt(intelligence)
        return self.send(recipients, encrypted)
```

---

## Troubleshooting Guide

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Stale IOCs | Feed not updating | Check feed connectivity |
| False positives | Low confidence IOCs | Increase confidence threshold |
| Duplicate IOCs | Multiple feeds | Deduplicate across feeds |

---

## API Reference

### IOCManager

```python
class IOCManager:
    def create_ioc(indicator, ioc_type, confidence, source, tags, tlp) -> IOC
    def enrich_ioc(ioc) -> EnrichedIOC
    def deduplicate(iocs) -> List[IOC]
    def share_ioc(ioc, recipients, tlp) -> ShareResult
```

### ThreatActorProfiler

```python
class ThreatActorProfiler:
    def profile(actor_name) -> ThreatActorProfile
    def map_techniques(actor_name) -> List[Technique]
    def predict_targets(actor_name) -> List[Target]
```

### DetectionRuleGenerator

```python
class DetectionRuleGenerator:
    def generate_sigma(technique, description, logsource) -> SigmaRule
    def generate_yara(pattern, description) -> YARARule
    def generate_snort(rule_content) -> SnortRule
```

---

## Data Models

### IOC

```python
@dataclass
class IOC:
    indicator: str
    ioc_type: str
    confidence: int
    source: str
    tags: List[str]
    tlp: str
    first_seen: datetime
    last_seen: datetime
    enrichment: dict
```

### ThreatActorProfile

```python
@dataclass
class ThreatActorProfile:
    name: str
    aliases: List[str]
    attribution: str
    target_sectors: List[str]
    techniques: List[Technique]
    infrastructure: List[str]
    motivations: List[str]
```

---

## Deployment Guide

### Threat Intelligence Platform

```yaml
services:
  misp:
    image: misp/misp
    ports:
      - "443:443"
    environment:
      - HOSTNAME=misp.internal
    volumes:
      - misp-data:/var/www/MISP/app/files

  taxii:
    image: taxii2-server
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://...
```

---

## Monitoring & Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `ti.ioc.count` | Total IOCs | Track |
| `ti.feed.update` | Feed update success | < 0.95 |
| `ti.detection.match` | Detection matches | Spike |

---

## Testing Strategy

### Intelligence Tests

```python
def test_ioc_creation():
    mgr = IOCManager()
    ioc = mgr.create_ioc("185.220.101.34", "ip_address", 85, "analysis", ["c2"], "amber")
    assert ioc.confidence == 85
    assert ioc.tlp == "amber"
```

---

## Versioning & Migration

### Intelligence Schema Versioning

Track STIX/TAXII schema versions.

---

## Glossary

| Term | Definition |
|------|-----------|
| **IOC** | Indicator of Compromise |
| **TLP** | Traffic Light Protocol |
| **TTP** | Tactics, Techniques, and Procedures |
| **MITRE ATT&CK** | Adversary tactics and techniques knowledge base |
| **Diamond Model** | Threat analysis framework |

---

## Changelog

### v2.0.0
- Added STIX/TAXII support
- YARA/Sigma rule generation
- Multi-source IOC enrichment

### v1.0.0
- Initial release with basic IOC management

---

## Contributing Guidelines

- Validate IOC confidence
- Follow TLP guidelines
- Document intelligence sources

---

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills
