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

## Advanced Analysis Workflows

### STIX 2.1 Bundle Construction and Distribution

```python
from threat_intelligence import STIXBundleBuilder, STIXObject, TLPConfig

builder = STIXBundleBuilder(
    identity=IdentityConfig(
        name="ACME Threat Intelligence",
        identity_class="organization",
        sectors=["technology", "finance"]
    ),
    default_tlp=TLPConfig.AMBER
)

# Build comprehensive STIX bundle
bundle = builder.build(
    objects=[
        # Threat Actor
        STIXObject.threat_actor(
            name="APT-Example",
            aliases=["Cozy Cloud", "DarkByte"],
            description="State-sponsored threat actor targeting financial sector",
            primary_motivation="ideology",
            sophistication="advanced",
            resource_level="government",
            first_seen="2019-03-15",
            last_seen="2024-01-15",
            goals=["intellectual property theft", "financial gain"]
        ),

        # Campaign
        STIXObject.campaign(
            name="Operation Financial Storm",
            description="Targeting financial institutions via supply chain compromise",
            first_seen="2023-10-01",
            last_seen="2024-01-15",
            objective="compromise financial sector supply chain",
            campaign_goals=["access to SWIFT systems", "trading algorithm theft"]
        ),

        # Attack Patterns (MITRE ATT&CK)
        STIXObject.attack_pattern(
            technique_id="T1195.002",
            name="Supply Chain Compromise: Compromise Software Supply Chain",
            description="Adversary compromised a software update mechanism"
        ),
        STIXObject.attack_pattern(
            technique_id="T1059.001",
            name="Command and Scripting Interpreter: PowerShell",
            description="PowerShell used for post-exploitation activities"
        ),

        # Indicators
        STIXObject.indicator(type="ipv4-addr", value="198.51.100.42",
                             valid_from="2023-12-01", confidence=85,
                             labels=["c2"]),
        STIXObject.indicator(type="domain-name", value="malicious-example.com",
                             valid_from="2023-11-15", confidence=90,
                             labels=["c2", "phishing"]),
        STIXObject.indicator(type="file:hashes.MD5", value="d41d8cd98f00b204",
                             valid_from="2024-01-01", confidence=95,
                             labels=["malware"]),

        # Infrastructure
        STIXObject.infrastructure(
            name="C2 Infrastructure",
            infrastructure_types=["command-and-control"],
            first_seen="2023-11-01",
            last_seen="2024-01-15"
        ),
    ],
    relationships=[
        # Campaign uses attack patterns
        ("campaign--op-financial", "uses", "attack-pattern--T1195.002"),
        ("campaign--op-financial", "uses", "attack-pattern--T1059.001"),
        # Campaign attributed to threat actor
        ("threat-actor--apt-example", "attributed-to", "campaign--op-financial"),
        # Infrastructure attributed to campaign
        ("campaign--op-financial", "uses", "infrastructure--c2"),
        # Indicators on infrastructure
        ("indicator--ip-198", "communicates-with", "infrastructure--c2"),
        ("indicator--domain-evil", "resolves-to", "infrastructure--c2"),
    ]
)

# Validate and serialize
validation = bundle.validate()
print(f"STIX Bundle Validation:")
print(f"  Valid: {validation.is_valid}")
print(f"  Object count: {len(bundle.objects)}")
print(f"  Relationship count: {len(bundle.relationships)}")
print(f"  Errors: {validation.errors}")

# Export
bundle.serialize(
    output_path="/exports/stix_bundle.json",
    pretty=True,
    include_custom_properties=True
)
print(f"Bundle exported: {bundle.size_bytes} bytes")
```

### Threat Actor Profile Deep Dive

```python
from threat_intelligence import ThreatActorProfiler, ProfileDimension, EvidenceSource

profiler = ThreatActorProfiler(
    evidence_sources=[
        EvidenceSource.MISP,
        EvidenceSource.ALIENVAULT_OTX,
        EvidenceSource.CRIMETHINC,
        EvidenceSource.MANDIANT,
        EvidenceSource.PUBLIC_REPORTS,
    ],
    confidence_model="bayesian"
)

# Build comprehensive threat actor profile
profile = profiler.build_profile(
    actor_name="APT29",
    include_dimensions=[
        ProfileDimension.IDENTIFICATION,
        ProfileDimension.CAPABILITIES,
        ProfileDimension.INFRASTRUCTURE,
        ProfileDimension.TARGETING,
        ProfileDimension.TTPS,
        ProfileDimension.TIMELINE,
        ProfileDimension.ATTRIBUTION,
        ProfileDimension.INFRASTRUCTURE_KNOWLEDGE,
    ]
)

print(f"Threat Actor Profile: {profile.actor_name}")
print(f"  Aliases: {profile.aliases}")
print(f"  Attribution Confidence: {profile.attribution_confidence:.1%}")
print(f"  Attribution Sources: {profile.attribution_sources}")
print(f"\n  Identification:")
print(f"    Country: {profile.country}")
print(f"    Sponsorship: {profile.sponsorship}")
print(f"    Motivation: {profile.motivation}")
print(f"    Sophistication: {profile.sophistication}")
print(f"    Resource Level: {profile.resource_level}")
print(f"\n  Capabilities:")
print(f"    Tooling: {profile.tooling}")
print(f"    Zero-days used: {profile.zero_day_count}")
print(f"    Custom malware families: {profile.custom_malware}")
print(f"    Operational security: {profile.opsec_level}")
print(f"\n  Targeting:")
print(f"    Sectors: {profile.target_sectors}")
print(f"    Countries: {profile.target_countries}")
print(f"    User types: {profile.target_user_types}")
print(f"\n  Infrastructure:")
print(f"    Known C2 domains: {profile.c2_domains_count}")
print(f"    Known C2 IPs: {profile.c2_ip_count}")
print(f"    Hosting providers: {profile.hosting_providers}")
print(f"    Registrars used: {profile.registrars}")
print(f"\n  Timeline:")
print(f"    First activity: {profile.first_activity}")
print(f"    Last activity: {profile.last_activity}")
print(f"    Active campaigns: {profile.active_campaign_count}")
print(f"    Total campaigns: {profile.total_campaign_count}")

# Export profile as structured data
profile.export(
    format="json",
    output_path="/profiles/apt29_profile.json"
)
```

### MITRE ATT&CK Mapping and Gap Analysis

```python
from threat_intelligence import ATTCKMapper, ATTCKMatrix, CoverageGap

mapper = ATTCKMapper(matrix=ATTCKMatrix.ENTERPRISE)

# Map observed TTPs to ATT&CK
observed_ttps = [
    {"technique": "T1566.001", "tactic": "initial-access", "context": "spearphishing attachment"},
    {"technique": "T1059.001", "tactic": "execution", "context": "PowerShell encoded command"},
    {"technique": "T1053.005", "tactic": "persistence", "context": "scheduled task creation"},
    {"technique": "T1078", "tactic": "persistence", "context": "compromised credentials"},
    {"technique": "T1055", "tactic": "defense-evasion", "context": "process injection"},
    {"technique": "T1140", "tactic": "defense-evasion", "context": "deobfuscation of payloads"},
    {"technique": "T1071.001", "tactic": "command-and-control", "context": "HTTP C2"},
    {"technique": "T1041", "tactic": "exfiltration", "context": "C2 channel exfiltration"},
    {"technique": "T1486", "tactic": "impact", "context": "data encryption for ransom"},
]

# Map to ATT&CK
mapping_result = mapper.map_ttps(observed_ttps)

print("MITRE ATT&CK Mapping:")
for tactic, techniques in mapping_result.tactic_mapping.items():
    print(f"\n  {tactic}:")
    for tech in techniques:
        print(f"    [{tech.technique_id}] {tech.name}")
        print(f"      Context: {tech.context}")
        print(f"      Detection coverage: {tech.detection_coverage:.0%}")
        print(f"      Mitigation available: {tech.mitigation_available}")

# Identify coverage gaps
coverage = mapper.assess_coverage(
    observed_ttps=observed_ttps,
    existing_detection_rules=detection_rules,
    existing_mitigations=mitigations
)

print(f"\nCoverage Analysis:")
print(f"  Total techniques in observed attack: {coverage.total_techniques}")
print(f"  Techniques with detection: {coverage.detected_count}")
print(f"  Techniques with mitigation: {coverage.mitigated_count}")
print(f"  Overall detection coverage: {coverage.detection_coverage:.0%}")
print(f"  Overall mitigation coverage: {coverage.mitigation_coverage:.0%}")

print(f"\n  Coverage Gaps (Critical):")
for gap in coverage.critical_gaps:
    print(f"    [{gap.technique_id}] {gap.technique_name}")
    print(f"      Tactic: {gap.tactic}")
    print(f"      Impact: {gap.impact_assessment}")
    print(f"      Recommended detection: {gap.detection_recommendation}")
    print(f"      Recommended mitigation: {gap.mitigation_recommendation}")
```

## Intelligence Production

### Structured Intelligence Report Generation

```python
from threat_intelligence import IntelProduction, ACHMatrix, KeyAssumptionsCheck

production = IntelProduction(
    title="APT29 Targeting of Financial Sector - Intelligence Assessment",
    classification="TLP:AMBER",
    confidence_level="moderate"
)

# Analysis of Competing Hypotheses (ACH)
ach = ACHMatrix(
    hypotheses=[
        "APT29 is actively targeting financial sector SWIFT systems",
        "APT29 is collecting intelligence for future operations",
        "APT29 is establishing long-term access for strategic purposes",
    ],
    evidence=[
        {"source": "Mandiant Report 2024-01", "reliability": "A", "credibility": "1"},
        {"source": "Internal IR findings", "reliability": "B", "credibility": "2"},
        {"source": "Social media intelligence", "reliability": "F", "credibility": "5"},
        {"source": "Partner intelligence sharing", "reliability": "B", "credibility": "2"},
    ]
)

# Score evidence against hypotheses
ach.score_evidence(
    scores={
        "Mandiant Report 2024-01": [2, 1, 1],      # Strongly supports H1
        "Internal IR findings": [1, 2, 2],           # Moderately supports H1
        "Social media intelligence": [0, 1, 0],      # Slightly supports H2
        "Partner intelligence sharing": [1, 2, 2],   # Moderately supports H1
    }
)

# Identify key assumptions
assumptions = KeyAssumptionsCheck(
    assumptions=[
        "Mandiant's attribution to APT29 is accurate",
        "Internal findings are not influenced by confirmation bias",
        "Partner intelligence is timely and relevant",
    ],
    impacts=[
        "If attribution is wrong, entire assessment is invalid",
        "If bias exists, findings may be overstated",
        "If partner intel is stale, assessment may be outdated",
    ]
)

# Build intelligence assessment
assessment = production.build_assessment(
    ach_analysis=ach,
    assumptions_check=assumptions,
    key_judgments=[
        {"judgment": "APT29 is actively targeting financial sector SWIFT systems",
         "confidence": "moderate", "basis": "Mandiant report + internal findings"},
        {"judgment": "The threat will likely increase in the next 30-60 days",
         "confidence": "low", "basis": "Historical patterns + campaign timeline"},
    ],
    recommended_actions=[
        "Enhance monitoring of SWIFT-related infrastructure",
        "Share indicators with financial sector ISAC",
        "Conduct targeted threat hunting for APT29 TTPs",
        "Brief executive leadership on potential impact",
    ]
)

# Generate final report
report = assessment.generate_report(format="markdown")
print(report)
assessment.export("apt29_financial_assessment.pdf")
```

### Intelligence Requirements Planning

```python
from threat_intelligence import IntelRequirements, PriorityIntelligenceRequirement, PIR

requirements = IntelRequirements(
    organization="ACME Corp",
    planning_cycle="quarterly"
)

# Define Priority Intelligence Requirements (PIRs)
pirs = [
    PIR(
        id="PIR-001",
        question="What threat actors are targeting our industry sector?",
        priority="high",
        collection_sources=["osint", "isac_sharing", "commercial_feeds"],
        consumers=["soc", "executive_leadership", "risk_management"],
        review_frequency="monthly"
    ),
    PIR(
        id="PIR-002",
        question="What vulnerabilities are being actively exploited against our technology stack?",
        priority="critical",
        collection_sources=["cve_feeds", "exploit_db", "dark_web_monitoring"],
        consumers=["vulnerability_management", "soc", "engineering"],
        review_frequency="weekly"
    ),
    PIR(
        id="PIR-003",
        question="Are there indicators of compromise relevant to our infrastructure?",
        priority="high",
        collection_sources=["threat_feeds", "isac", "internal_ir"],
        consumers=["soc", "threat_hunting", "ir_team"],
        review_frequency="daily"
    ),
    PIR(
        id="PIR-004",
        question="What is the current ransomware threat landscape?",
        priority="medium",
        collection_sources=["osint", "isac", "vendor_reports"],
        consumers=["executive_leadership", "risk_management", "soc"],
        review_frequency="monthly"
    ),
]

for pir in pirs:
    requirements.add_pir(pir)

# Generate collection plan
collection_plan = requirements.generate_collection_plan()

print("Intelligence Collection Plan:")
for pir in collection_plan.pirs:
    print(f"\n  {pir.id}: {pir.question}")
    print(f"    Priority: {pir.priority}")
    print(f"    Collection sources: {pir.collection_sources}")
    print(f"    Consumers: {pir.consumers}")
    print(f"    Review frequency: {pir.review_frequency}")
    print(f"    Status: {pir.status}")
    print(f"    Next review: {pir.next_review}")
```

## Feed Management

### Multi-Feed Aggregation with Deduplication

```python
from threat_intelligence import FeedAggregator, FeedConfig, DeduplicationStrategy

aggregator = FeedAggregator(
    dedup_strategy=DeduplicationStrategy.HASH_BASED,
    normalization_enabled=True,
    conflict_resolution="highest_confidence"
)

# Configure feeds
feeds = [
    FeedConfig(
        name="AlienVault OTX",
        url="https://otx.alienvault.com/api/v1/pulses",
        api_key="your-otx-key",
        poll_interval_minutes=30,
        format="otx",
        enabled=True,
        priority=1
    ),
    FeedConfig(
        name="Abuse.ch URLhaus",
        url="https://urlhaus-api.abuse.ch/v1/urls/recent",
        poll_interval_minutes=15,
        format="json",
        enabled=True,
        priority=2
    ),
    FeedConfig(
        name="PhishTank",
        url="https://data.phishtank.com/data/online-valid.csv",
        poll_interval_minutes=60,
        format="csv",
        enabled=True,
        priority=3
    ),
    FeedConfig(
        name="CIRCL Hashdd",
        url="https://hashdd.com/api/v1/lookup",
        poll_interval_minutes=60,
        format="json",
        enabled=True,
        priority=3
    ),
    FeedConfig(
        name="MISP Community",
        url="https://misp.example.com",
        api_key="your-misp-key",
        poll_interval_minutes=30,
        format="misp",
        enabled=True,
        priority=2,
        filters={"tags": ["ransomware", "apt", "financial-sector"]}
    ),
    FeedConfig(
        name="Internal IR IoCs",
        path="/data/internal/iocs_export.json",
        poll_interval_minutes=5,
        format="json",
        enabled=True,
        priority=1
    ),
]

for feed in feeds:
    aggregator.add_feed(feed)

# Poll all feeds and aggregate
result = aggregator.poll_and_aggregate(
    time_window_hours=24,
    generate_report=True
)

print("Feed Aggregation Results:")
print(f"  Feeds polled: {result.feeds_polled}")
print(f"  Total indicators ingested: {result.total_ingested}")
print(f"  Duplicates removed: {result.duplicates_removed}")
print(f"  New indicators: {result.new_indicators}")
print(f"  Updated indicators: {result.updated_indicators}")
print(f"  Conflicts resolved: {result.conflicts_resolved}")
print(f"  Duration: {result.duration_seconds:.1f}s")

print(f"\n  Per-Feed Breakdown:")
for feed, stats in result.feed_stats.items():
    print(f"    {feed}:")
    print(f"      Indicators: {stats.indicators_count}")
    print(f"      New: {stats.new_count}")
    print(f"      Updated: {stats.updated_count}")
    print(f"      Errors: {stats.error_count}")
    print(f"      Avg response time: {stats.avg_response_ms:.0f}ms")
```

### Feed Health Monitoring

```python
from threat_intelligence import FeedHealthMonitor, HealthMetric, AlertRule

monitor = FeedHealthMonitor(
    check_interval_minutes=5,
    alert_channels=["email", "slack"]
)

# Define health metrics
metrics = [
    HealthMetric(
        name="freshest_indicator_age",
        description="Age of most recent indicator from feed",
        threshold_hours=24,
        severity="warning"
    ),
    HealthMetric(
        name="indicator_volume",
        description="Number of indicators in last poll",
        min_count=10,
        max_count=100000,
        severity="critical"
    ),
    HealthMetric(
        name="poll_success_rate",
        description="Percentage of successful polls in last 24h",
        threshold_percent=95,
        severity="critical"
    ),
    HealthMetric(
        name="response_time",
        description="Average API response time",
        threshold_ms=5000,
        severity="warning"
    ),
    HealthMetric(
        name="duplicate_rate",
        description="Percentage of duplicates in feed",
        threshold_percent=50,
        severity="info"
    ),
]

for metric in metrics:
    monitor.add_metric(metric)

# Check feed health
health_report = monitor.check_all_feeds()

print("Feed Health Report:")
for feed_name, health in health_report.feeds.items():
    status = "HEALTHY" if health.is_healthy else "DEGRADED"
    print(f"\n  {feed_name}: {status}")
    print(f"    Last poll: {health.last_poll_time}")
    print(f"    Indicator count: {health.indicator_count}")
    print(f"    Freshness: {health.freshness_hours:.1f}h")
    print(f"    Success rate: {health.success_rate:.1%}")
    print(f"    Avg response time: {health.avg_response_ms:.0f}ms")
    print(f"    Duplicate rate: {health.duplicate_rate:.1%}")

    if health.alerts:
        for alert in health.alerts:
            print(f"    ALERT [{alert.severity}]: {alert.message}")
```

## Database Schema for Threat Intelligence

```sql
-- Threat actors
CREATE TABLE threat_actors (
    actor_id            BIGINT AUTO_INCREMENT PRIMARY KEY,
    actor_uid           VARCHAR(64) UNIQUE NOT NULL,
    name                VARCHAR(256) NOT NULL,
    aliases             JSON,
    description         TEXT,
    motivation          VARCHAR(128),
    sophistication      ENUM('minimal', 'intermediate', 'advanced', 'expert', 'innovator', 'strategic'),
    resource_level      ENUM('individual', 'club', 'contest', 'team', 'organization', 'government'),
    country             VARCHAR(4),
    first_seen          DATE,
    last_seen           DATE,
    targeting_sectors   JSON,
    targeting_countries JSON,
    known_tools         JSON,
    known_malware       JSON,
    mitre_techniques    JSON,
    confidence          DOUBLE DEFAULT 0.5,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_country (country),
    INDEX idx_confidence (confidence DESC)
);

-- Campaigns
CREATE TABLE campaigns (
    campaign_id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    campaign_uid        VARCHAR(64) UNIQUE NOT NULL,
    name                VARCHAR(256) NOT NULL,
    description         TEXT,
    objective           TEXT,
    first_seen          DATE,
    last_seen           DATE,
    target_sectors      JSON,
    target_countries    JSON,
    associated_actors   JSON,
    mitre_techniques    JSON,
    confidence          DOUBLE DEFAULT 0.5,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_time_range (first_seen, last_seen)
);

-- Intelligence reports
CREATE TABLE intel_reports (
    report_id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    report_uid          VARCHAR(64) UNIQUE NOT NULL,
    title               VARCHAR(512) NOT NULL,
    classification      ENUM('TLP:WHITE', 'TLP:GREEN', 'TLP:AMBER', 'TLP:RED') DEFAULT 'TLP:GREEN',
    report_type         ENUM('strategic', 'tactical', 'operational', 'technical') NOT NULL,
    executive_summary   TEXT,
    key_findings        JSON,
    recommendations     JSON,
    mitre_techniques    JSON,
    associated_actors   JSON,
    associated_campaigns JSON,
    source_reliability  ENUM('A', 'B', 'C', 'D', 'E', 'F'),
    information_credibility ENUM('1', '2', '3', '4', '5', '6'),
    published_date      DATE,
    author              VARCHAR(128),
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_type (report_type),
    INDEX idx_classification (classification),
    INDEX idx_published (published_date)
);

-- Intelligence feeds
CREATE TABLE intel_feeds (
    feed_id             BIGINT AUTO_INCREMENT PRIMARY KEY,
    feed_name           VARCHAR(256) NOT NULL,
    feed_url            VARCHAR(2048),
    feed_format         ENUM('stix', 'csv', 'json', 'misp', 'otx', 'text') NOT NULL,
    poll_interval_minutes INT DEFAULT 60,
    enabled             BOOLEAN DEFAULT TRUE,
    last_polled_at      TIMESTAMP NULL,
    last_success_at     TIMESTAMP NULL,
    last_error          TEXT,
    indicator_count     INT DEFAULT 0,
    reliability_score   DOUBLE DEFAULT 0.5,
    api_key_required    BOOLEAN DEFAULT FALSE,
    auth_type           ENUM('none', 'api_key', 'basic', 'bearer', 'oauth2') DEFAULT 'none',
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_enabled (enabled),
    INDEX idx_last_polled (last_polled_at)
);

-- Intelligence requirements (PIRs)
CREATE TABLE intel_requirements (
    requirement_id      BIGINT AUTO_INCREMENT PRIMARY KEY,
    pir_id              VARCHAR(32) UNIQUE NOT NULL,
    question            TEXT NOT NULL,
    priority            ENUM('critical', 'high', 'medium', 'low') NOT NULL,
    status              ENUM('active', 'fulfilled', 'deferred', 'retired') DEFAULT 'active',
    collection_sources  JSON,
    consumers           JSON,
    review_frequency    VARCHAR(32),
    last_reviewed_at    TIMESTAMP NULL,
    next_review_at      TIMESTAMP NULL,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_priority (priority),
    INDEX idx_status (status)
);

-- Analytical products
CREATE TABLE analytical_products (
    product_id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    product_uid         VARCHAR(64) UNIQUE NOT NULL,
    title               VARCHAR(512) NOT NULL,
    product_type        ENUM('assessment', 'forecast', 'profile', 'gap_analysis', 'collection_plan') NOT NULL,
    assessment          TEXT,
    key_judgments       JSON,
    confidence_levels   JSON,
    assumptions         JSON,
    evidence_sources    JSON,
    ach_matrix          JSON,
    author              VARCHAR(128),
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_type (product_type)
);

-- Intelligence sharing agreements
CREATE TABLE sharing_agreements (
    agreement_id        BIGINT AUTO_INCREMENT PRIMARY KEY,
    partner_org         VARCHAR(256) NOT NULL,
    partner_contact     VARCHAR(256),
    tlp_allowed         JSON NOT NULL,
    sharing_scope       ENUM('bidirectional', 'outbound_only', 'inbound_only') DEFAULT 'bidirectional',
    data_types_shared   JSON,
    start_date          DATE,
    end_date            DATE,
    status              ENUM('active', 'expired', 'suspended') DEFAULT 'active',
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_partner (partner_org),
    INDEX idx_status (status)
);
```

## Integration Patterns

### Threat Intel Platform (TIP) Integration

```python
from threat_intelligence import TIPIntegration, TIPPlatform, SyncConfig

# MISP integration
misp = TIPIntegration(
    platform=TIPPlatform.MISP,
    config=SyncConfig(
        server_url="https://misp.example.com",
        api_key="your-misp-key",
        sync_interval_minutes=30,
        auto_create_events=True,
        default_distribution=1,
        default_threat_level=2,
        default_analysis=2,
        tag_mapping={
            "apt": "threat-actor:apt",
            "ransomware": "malware:ransomware",
            "financial": "target-sector:financial",
        }
    )
)

# Sync indicators to MISP
sync_result = misp.sync_indicators(
    indicators=enriched_indicators,
    event_name="Automated IOC Sync - {date}",
    create_event=True,
    correlate_existing=True
)

print(f"MISP Sync Results:")
print(f"  Indicators pushed: {sync_result.pushed}")
print(f"  New events created: {sync_result.events_created}")
print(f"  Existing events updated: {sync_result.events_updated}")
print(f"  Duplicates skipped: {sync_result.duplicates_skipped}")
print(f"  Errors: {sync_result.errors}")

# AlienVault OTX integration
otx = TIPIntegration(
    platform=TIPPlatform.ALIENVAULT_OTX,
    config=SyncConfig(
        api_key="your-otx-key",
        pulse_prefix="ACME:",
        auto_create_pulses=True
    )
)

# Create OTX pulse from internal analysis
pulse = otx.create_pulse(
    name="ACME: Campaign Infrastructure Update",
    description="Updated campaign infrastructure indicators",
    indicators=indicators_for_sharing,
    tlp="green",
    tags=["campaign", "infrastructure", "automated"],
    references=["https://internal-wiki.example.com/ir-2024-102"]
)

print(f"OTX Pulse Created: {pulse.id}")
print(f"  Indicator count: {pulse.indicator_count}")
print(f"  Tags: {pulse.tags}")
```

### SOAR Integration for Automated Enrichment

```python
from threat_intelligence import SOARIntegration, EnrichmentPlaybook, PlaybookAction

soar = SOARIntegration(
    platform="Palo Alto XSOAR",
    base_url="https://soar.example.com",
    api_key="your-soar-key"
)

# Create automated enrichment playbook
playbook = EnrichmentPlaybook(
    name="Threat Intel Auto-Enrichment",
    trigger="new_ioc_detected",
    actions=[
        PlaybookAction(
            type="enrich_ip",
            parameters={"ip": "{{ioc_value}}"},
            enrichment_sources=["virustotal", "abuseipdb", "shodan", "greynoise"]
        ),
        PlaybookAction(
            type="check_whitelist",
            parameters={"indicator": "{{ioc_value}}"}
        ),
        PlaybookAction(
            type="conditional",
            condition="{{is_whitelisted}} == false AND {{threat_score}} > 0.7",
            then_actions=[
                PlaybookAction(type="lookup_threat_actor", parameters={"indicator": "{{ioc_value}}"}),
                PlaybookAction(type="map_to_attack", parameters={"indicator": "{{ioc_value}}"}),
                PlaybookAction(type="create_ticket", parameters={
                    "title": "High-Confidence IOC: {{ioc_value}}",
                    "severity": "P2",
                    "assignee": "threat_intel_team"
                }),
                PlaybookAction(type="block_indicator", parameters={
                    "indicator": "{{ioc_value}}",
                    "targets": ["firewall", "dns_sinkhole", "proxy"]
                }),
            ],
            else_actions=[
                PlaybookAction(type="log_indicator", parameters={
                    "indicator": "{{ioc_value}}",
                    "action": "monitor_only"
                }),
            ]
        ),
    ]
)

# Register playbook
result = soar.register_playbook(playbook)
print(f"Playbook registered: {result.playbook_id}")
print(f"  Trigger: {playbook.trigger}")
print(f"  Actions: {len(playbook.actions)}")
```

### REST API for Intelligence Consumption

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from threat_intelligence import ThreatIntelEngine, IndicatorQuery, IntelQuery

app = FastAPI(title="Threat Intelligence API", version="2.0.0")
engine = ThreatIntelEngine.load("production")

@app.get("/api/v2/indicators/{indicator_type}/{value}")
async def lookup_indicator(indicator_type: str, value: str):
    """Look up an indicator and return enriched intelligence."""
    result = engine.lookup_indicator(type=indicator_type, value=value)
    if not result:
        raise HTTPException(status_code=404, detail="Indicator not found")
    return {
        "indicator": result.indicator,
        "enrichment": result.enrichment,
        "threat_score": result.threat_score,
        "confidence": result.confidence,
        "associated_actors": result.threat_actors,
        "mitre_techniques": result.mitre_techniques,
        "first_seen": result.first_seen,
        "last_seen": result.last_seen,
    }

@app.post("/api/v2/indicators/batch-lookup")
async def batch_lookup(query: IndicatorQuery):
    """Batch lookup multiple indicators."""
    results = engine.batch_lookup(query.indicators)
    return {
        "total": len(results),
        "malicious": sum(1 for r in results if r.is_malicious),
        "results": results
    }

@app.get("/api/v2/actors/{actor_name}")
async def get_actor_profile(actor_name: str):
    """Get comprehensive threat actor profile."""
    profile = engine.get_actor_profile(actor_name)
    if not profile:
        raise HTTPException(status_code=404, detail="Actor not found")
    return profile

@app.get("/api/v2/campaigns")
async def list_campaigns(
    since_days: int = 30,
    sector: str = None,
    actor: str = None,
    limit: int = 50
):
    """List recent campaigns with optional filters."""
    campaigns = engine.query_campaigns(
        since_days=since_days,
        sector=sector,
        actor=actor,
        limit=limit
    )
    return {"count": len(campaigns), "campaigns": campaigns}

@app.get("/api/v2/intel-report/{report_id}")
async def get_intel_report(report_id: str):
    """Retrieve a specific intelligence report."""
    report = engine.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@app.post("/api/v2/indicators/search")
async def search_indicators(query: IntelQuery):
    """Search indicators with complex queries."""
    results = engine.search_indicators(
        types=query.types,
        tags=query.tags,
        confidence_min=query.confidence_min,
        threat_score_min=query.threat_score_min,
        date_range=query.date_range,
        limit=query.limit
    )
    return {"count": len(results), "indicators": results}
```

## Performance Tuning Guide

### Intelligence Processing Optimization

```python
from threat_intelligence import IntelPerformanceConfig, ProcessingPipeline

config = IntelPerformanceConfig(
    # Feed polling
    max_concurrent_polls=8,
    poll_timeout_seconds=30,
    poll_retry_count=3,
    poll_backoff_multiplier=2.0,

    # Enrichment
    max_concurrent_enrichments=16,
    enrichment_timeout_seconds=15,
    enrichment_cache_ttl_hours=24,

    # Indicator processing
    indicator_batch_size=5000,
    indicator_dedup_threads=4,
    indicator_index_refresh_interval=300,

    # Report generation
    report_template_cache=True,
    report_async_rendering=True,

    # Database
    db_connection_pool_size=20,
    db_query_timeout_seconds=30,
    db_batch_insert_size=10000,

    # Memory
    max_memory_mb=4096,
    indicator_buffer_size=100000
)

pipeline = ProcessingPipeline(config=config)

# Benchmark processing
benchmark = pipeline.benchmark(
    test_indicators=100000,
    test_feeds=10,
    test_enrichments=50000
)

print("Intelligence Processing Benchmark:")
print(f"  Feed polling: {benchmark.feeds_per_minute:.1f} feeds/min")
print(f"  Indicator ingestion: {benchmark.indicators_per_second:.0f} indicators/s")
print(f"  Enrichment throughput: {benchmark.enrichments_per_second:.0f} enrichments/s")
print(f"  Deduplication: {benchmark.dedup_rate:.0f} indicators/s")
print(f"  Report generation: {benchmark.reports_per_minute:.1f} reports/min")
print(f"  Peak memory: {benchmark.peak_memory_mb:.1f} MB")
print(f"  Database I/O: {benchmark.db_ops_per_second:.0f} ops/s")
```

### Caching Strategy

```python
from threat_intelligence import CacheManager, CacheConfig, CacheStrategy

cache = CacheManager(
    config=CacheConfig(
        strategy=CacheStrategy.TIERED,
        l1_cache={"type": "memory", "max_size_mb": 512, "ttl_seconds": 300},
        l2_cache={"type": "redis", "host": "redis.example.com", "port": 6379, "ttl_seconds": 3600},
        l3_cache={"type": "disk", "path": "/cache/intel", "max_size_gb": 10, "ttl_seconds": 86400}
    )
)

# Cache indicator lookups
indicator_cache_key = f"indicator:{indicator_type}:{value}"
cached = cache.get(indicator_cache_key)
if not cached:
    # Query enrichment sources
    result = engine.enrich_indicator(indicator)
    cache.set(indicator_cache_key, result, ttl=3600)
else:
    result = cached

# Cache management
stats = cache.get_stats()
print(f"Cache Statistics:")
print(f"  L1 (Memory) - Hits: {stats.l1_hits}, Misses: {stats.l1_misses}, "
      f"Hit rate: {stats.l1_hit_rate:.1%}")
print(f"  L2 (Redis) - Hits: {stats.l2_hits}, Misses: {stats.l2_misses}, "
      f"Hit rate: {stats.l2_hit_rate:.1%}")
print(f"  L3 (Disk) - Hits: {stats.l3_hits}, Misses: {stats.l3_misses}, "
      f"Hit rate: {stats.l3_hit_rate:.1%}")
print(f"  Overall hit rate: {stats.overall_hit_rate:.1%}")
print(f"  Total entries: {stats.total_entries}")
print(f"  Memory usage: {stats.memory_usage_mb:.1f} MB")
```

## Reporting Templates

### Threat Intelligence Summary Report

```python
from threat_intelligence import IntelReport, ReportSection, SeverityLevel

report = IntelReport(
    title="Weekly Threat Intelligence Summary",
    classification="TLP:GREEN",
    date_range=("2024-01-15", "2024-01-21"),
    author="Threat Intelligence Team"
)

report.add_section(ReportSection(
    heading="Executive Summary",
    content="""
        This week's threat landscape analysis identified 847 new indicators across
        12 active campaigns. Ransomware activity remains elevated with 3 new families
        identified. APT29 showed increased activity targeting financial sector
        infrastructure. Supply chain compromises continue to be a significant vector.
    """
))

report.add_section(ReportSection(
    heading="Key Threat Developments",
    template="threat_developments",
    developments=[
        {"severity": "critical", "summary": "New ransomware family 'LockBlack' targeting healthcare"},
        {"severity": "high", "summary": "APT29 campaign targeting SWIFT infrastructure"},
        {"severity": "high", "summary": "Critical vulnerability in widely-used VPN appliance"},
        {"severity": "medium", "summary": "Phishing campaign impersonating financial regulators"},
    ]
))

report.add_section(ReportSection(
    heading="Indicator Activity",
    template="indicator_summary",
    data={
        "new_indicators": 847,
        "malicious_confirmed": 312,
        "false_positives": 45,
        "by_type": {"ip": 234, "domain": 189, "hash": 278, "url": 146},
        "top_threats": ["LockBlack Ransomware", "APT29", "Emotet"]
    }
))

report.add_section(ReportSection(
    heading="MITRE ATT&CK Coverage",
    template="attack_coverage",
    data={
        "techniques_observed": 47,
        "techniques_detected": 38,
        "coverage_gaps": 9,
        "top_tactics": ["initial-access", "execution", "persistence", "exfiltration"]
    }
))

report.add_section(ReportSection(
    heading="Recommended Actions",
    content="""
        1. Deploy updated YARA rules for LockBlack ransomware detection
        2. Block 312 confirmed malicious indicators at perimeter
        3. Conduct targeted hunting for APT29 TTPs in financial systems
        4. Patch VPN appliance vulnerability CVE-2024-XXXXX immediately
        5. Update email security rules for regulator impersonation phishing
    """
))

report.export(
    output_path="/reports/weekly_ti_summary.pdf",
    formats=["pdf", "html", "markdown", "json"]
)
```

## Architecture

```
+================================================================+
|               THREAT INTELLIGENCE ARCHITECTURE                   |
+================================================================+

+---------------------+     +---------------------+     +---------------------+
|   COLLECTION LAYER  |     |   PROCESSING LAYER  |     |   DISTRIBUTION      |
|                     |     |                     |     |   LAYER             |
|  +--------------+   |     |  +--------------+   |     |  +--------------+   |
|  | OSINT Feeds  |---+--+  |  | Normalizer  |---+--+  |  | STIX Export |---+--+
|  +--------------+   |  |  |  +--------------+   |  |  |  +--------------+   |  |
|  +--------------+   |  |  |  +--------------+   |  |  |  +--------------+   |  |
|  | ISAC Sharing |---+  |  |  | Deduplicator|---+  |  |  | MISP Sync   |---+  |
|  +--------------+   |  |  |  +--------------+   |  |  |  +--------------+   |  |
|  +--------------+   |  |  |  +--------------+   |  |  |  +--------------+   |  |
|  | Dark Web     |---+  |  |  | Enrichment  |---+  |  |  | OTX Push    |---+  |
|  | Monitoring   |   |  |  |  +--------------+   |  |  |  +--------------+   |  |
|  +--------------+   |  |  |  +--------------+   |  |  |  +--------------+   |  |
|  +--------------+   |  |  |  | Correlation |---+  |  |  | API/SOAR    |---+  |
|  | Commercial   |---+  |  |  | Engine      |   |  |  |  | Integration |   |  |
|  | Feeds        |   |  |  |  +--------------+   |  |  |  +--------------+   |  |
|  +--------------+   |  |  +---------------------+  |  +---------------------+  |
+---------------------+  |                           |                           |
                          v                           v                           v
              +----------------------------------------------+
              |           INTELLIGENCE CORE                   |
              |                                              |
              |  +------------+  +------------+  +--------+ |
              |  | Threat     |  | Campaign   |  | MITRE  | |
              |  | Actor DB   |  | Tracker    |  | ATT&CK | |
              |  +------------+  +------------+  +--------+ |
              |  +------------+  +------------+  +--------+ |
              |  | Feed       |  | Intel      |  | Report | |
              |  | Manager    |  | Production |  | Engine | |
              |  +------------+  +------------+  +--------+ |
              +----------------------------------------------+
                    |                    |                    |
                    v                    v                    v
         +-------------+     +------------------+    +---------------+
         |  Indicator  |     |  Intelligence    |    |  Collection   |
         |  Store      |     |  Requirements    |    |  Planning     |
         |  (Elastic)  |     |  (PIRs)          |    |  (PIR/PDCERF) |
         +-------------+     +------------------+    +---------------+
                    |                    |                    |
                    v                    v                    v
              +----------------------------------------------+
              |           CONSUMPTION LAYER                  |
              |  +----------------------------------------+  |
              |  | SOC Dashboards | IR Enrichment | Hunt |  |
              |  +----------------------------------------+  |
              +----------------------------------------------+
```

## Related Modules

- **ioc-analysis**: Deep analysis and correlation of indicators of compromise
- **behavioral-analysis**: Behavioral pattern analysis for threat detection
- **apt-detection**: Advanced persistent threat identification and tracking
- **forensic-analysis**: Digital forensics for intelligence validation
