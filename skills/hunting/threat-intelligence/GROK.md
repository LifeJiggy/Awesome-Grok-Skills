---
name: "threat-intelligence"
category: "hunting"
version: "2.0.0"
tags: ["hunting", "threat-intelligence", "cti", "stix", "taxii", "mitre"]
description: "Comprehensive threat intelligence collection, analysis, and dissemination framework"
---

# Threat Intelligence

## Overview

The Threat Intelligence module provides a complete framework for collecting, processing, analyzing, and disseminating cyber threat intelligence (CTI). It supports multiple intelligence standards (STIX 2.1, OpenIOC, MISP), integrates with threat feeds, and enables structured analysis of threat actor behaviors, tactics, techniques, and procedures (TTPs). This module is designed for security operations centers (SOC), threat hunting teams, and incident response professionals who need actionable intelligence to proactively defend against adversaries.

## Core Capabilities

- **Multi-Format Intelligence Ingestion**: Parse and normalize intelligence from STIX 2.1 bundles, OpenIOC indicators, MISP events, CSV feeds, and custom JSON formats
- **Indicator Management**: Create, deduplicate, enrich, and correlate Indicators of Compromise (IoCs) including IP addresses, domains, URLs, file hashes, and email addresses
- **Threat Actor Profiling**: Build and maintain threat actor profiles with aliases, motivations, targeting patterns, and known infrastructure
- **MITRE ATT&CK Mapping**: Automatically map observed behaviors to MITRE ATT&CK techniques and procedures
- **Intelligence Scoring**: Apply confidence scores, relevance ratings, and timeliness assessments to intelligence products
- **Feed Aggregation**: Aggregate intelligence from multiple OSINT and commercial feeds with configurable polling and deduplication
- **Relationship Graph Construction**: Build relationship graphs connecting actors, campaigns, tools, vulnerabilities, and targets
- **Automated Reporting**: Generate structured intelligence reports in markdown, HTML, or PDF formats

## Usage Examples

### Basic Indicator Enrichment

```python
from threat_intelligence import ThreatIntelEngine, IndicatorFactory, IntelSource

# Initialize the engine with configuration
engine = ThreatIntelEngine(
    feeds=[
        IntelSource(name="alienvault-otx", url="https://otx.alienvault.com/api/v1/pulses", api_key="your-key"),
        IntelSource(name="abuse-ch", url="https://urlhaus-api.abuse.ch/v1/"),
    ],
    confidence_threshold=70,
    enable_enrichment=True
)

# Create indicators from raw data
factory = IndicatorFactory()
ip_indicator = factory.create_indicator(
    indicator_type="ipv4",
    value="198.51.100.42",
    tlp="amber",
    confidence=85,
    source="internal-ir",
    tags=["c2", "emotet"]
)

# Enrich the indicator with contextual data
enriched = engine.enrich_indicator(ip_indicator)
print(f"Enriched indicator: {enriched.value}")
print(f"Associated threat actors: {[a.name for a in enriched.threat_actors]}")
print(f"MITRE techniques: {[t.technique_id for t in enriched.mitre_techniques]}")
```

### Threat Actor Profile Construction

```python
from threat_intelligence import ThreatActor, Campaign, AttackPattern

actor = ThreatActor(
    name="APT29",
    aliases=["Cozy Bear", "The Dukes", "YTTRIUM"],
    motivation="espionage",
    sophistication="advanced",
    targeting=["government", "think-tanks", "healthcare"],
    first_seen="2008-01-01",
    country="RU"
)

# Add known campaigns
campaign = Campaign(
    name="SolarWinds Supply Chain",
    objective="compromise software supply chain for widespread access",
    start_date="2019-10-01",
    end_date="2020-12-01",
    targets=["us-government", "technology-sector"],
    attack_patterns=[
        AttackPattern(technique_id="T1195.002", name="Supply Chain Compromise: Compromise Software Supply Chain"),
        AttackPattern(technique_id="T1071.001", name="Application Layer Protocol: Web Protocols"),
    ]
)
actor.add_campaign(campaign)

# Export as STIX 2.1 bundle
stix_bundle = actor.to_stix_bundle()
print(stix_bundle.serialize(pretty=True))
```

### Intelligence Report Generation

```python
from threat_intelligence import IntelReport, ReportSection, SeverityLevel

report = IntelReport(
    title="Q4 2024 Threat Landscape Overview",
    classification="TLP:AMBER",
    executive_summary="Elevated activity from ransomware operators targeting critical infrastructure..."
)

report.add_section(ReportSection(
    heading="Key Findings",
    content="Analysis identified 47 unique threat actor groups with active campaigns...",
    severity=SeverityLevel.HIGH
))

report.add_section(ReportSection(
    heading="Indicators of Compromise",
    content="284 unique IoCs identified across 12 campaigns",
    indicators=engine.get_recent_indicators(days=90)
))

# Generate the report
report_html = report.render(format="html")
report.export("q4_threat_report.html")
```

### Feed Management and Polling

```python
from threat_intelligence import FeedManager, PollConfig

manager = FeedManager()

# Add feeds with polling configuration
manager.add_feed(
    name="MISP Community",
    url="https://misp.example.com",
    poll_config=PollConfig(interval_minutes=30, full_sync=False),
    filters={"tags": ["ransomware", "apt"], "confidence": [">=", 60]}
)

manager.add_feed(
    name="PhishTank",
    url="https://data.phishtank.com/data/online-valid.csv",
    poll_config=PollConfig(interval_minutes=60)
)

# Start continuous polling
manager.start_polling(callback=lambda event: process_intel_event(event))
```

## Best Practices

- **Validate Intelligence Quality**: Always assess the reliability of intelligence sources using the Admiralty Scale (source reliability + information credibility)
- **Apply TLP Correctly**: Respect Traffic Light Protocol (TLP) markings when sharing intelligence; never share TLP:RED intelligence outside your organization
- **Maintain Timeliness**: Stale intelligence is dangerous intelligence; regularly review and expire outdated indicators
- **Correlate Before Acting**: Single indicators rarely provide sufficient confidence; correlate multiple intelligence sources before taking blocking actions
- **Document Analytical Judgments**: Use structured analytical techniques (ACH, key assumptions checks) and document your reasoning
- **Feed Diversification**: Avoid single-source dependency; aggregate intelligence from multiple commercial, open-source, and government feeds
- **Automate Response Where Possible**: Integrate with SOAR platforms to automate blocking of high-confidence indicators
- **Regular Review Cycles**: Establish daily, weekly, and monthly review cadences for different intelligence types

## Related Modules

- **ioc-analysis**: Deep analysis and correlation of indicators of compromise
- **behavioral-analysis**: Behavioral pattern analysis for threat detection
- **apt-detection**: Advanced persistent threat identification and tracking
- **forensic-analysis**: Digital forensics for intelligence validation
