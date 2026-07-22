---
name: "ioc-analysis"
category: "hunting"
version: "2.0.0"
tags: ["hunting", "ioc", "indicators", "correlation", "enrichment"]
description: "Advanced indicator of compromise analysis, correlation, and lifecycle management"
---

# IOC Analysis

## Overview

The IOC Analysis module provides deep analysis and correlation capabilities for Indicators of Compromise (IoCs). It goes beyond simple indicator storage to offer contextual enrichment, relationship mapping, false-positive scoring, and lifecycle management. The module supports automated enrichment from multiple OSINT sources, bulk correlation across indicator datasets, and temporal analysis to identify coordinated campaigns. This is essential for security teams that need to understand not just what indicators exist, but what they mean in the context of their threat landscape.

## Core Capabilities

- **Multi-Source Enrichment**: Query VirusTotal, Shodan, AbuseIPDB, OTX, and custom APIs for indicator context
- **Correlation Engine**: Identify relationships between indicators based on shared infrastructure, temporal proximity, and behavioral patterns
- **False Positive Scoring**: ML-assisted scoring to reduce alert fatigue by identifying likely false positives
- **Indicator Lifecycle Tracking**: Track indicators from creation through active use to retirement with full audit trail
- **Bulk Processing**: Efficiently analyze thousands of indicators with parallel processing and caching
- **Contextual Tagging**: Automatically apply contextual tags based on enrichment data (geo-location, ASN, hosting provider)
- **Overlap Analysis**: Identify indicator overlap between different threat actor profiles
- **Temporal Clustering**: Group indicators by time windows to identify campaign bursts

## Usage Examples

### Single Indicator Analysis

```python
from ioc_analysis import IOCAnalyzer, EnrichmentSource

analyzer = IOCAnalyzer(
    enrichment_sources=[
        EnrichmentSource(name="virustotal", api_key="your-vt-key"),
        EnrichmentSource(name="abuseipdb", api_key="your-abuseipdb-key"),
        EnrichmentSource(name="shodan", api_key="your-shodan-key"),
    ]
)

# Analyze a single IP address
result = analyzer.analyze("198.51.100.42")
print(f"Indicator: {result.indicator.value}")
print(f"Confidence: {result.confidence_score}%")
print(f"False positive rate: {result.false_positive_rate:.1%}")
print(f"Enrichment sources queried: {result.enrichment_count}")
print(f"Associated threat actors: {result.threat_actors}")
print(f"Geo-location: {result.geo_location}")
print(f"ASN: {result.asn_info}")
```

### Bulk Indicator Correlation

```python
from ioc_analysis import CorrelationEngine, TimeWindow

correlator = CorrelationEngine(time_window=TimeWindow.DAYS_30)

# Load indicator sets
correlator.load_dataset("dataset_a", indicators_set_a)
correlator.load_dataset("dataset_b", indicators_set_b)

# Find correlations
overlaps = correlator.find_overlaps()
print(f"Found {len(overlaps)} correlated indicator groups")

for group in overlaps:
    print(f"\nCorrelation Group ({len(group.indicators)} indicators):")
    print(f"  Shared between: {group.datasets}")
    print(f"  Time span: {group.first_seen} to {group.last_seen}")
    print(f"  Confidence: {group.correlation_confidence}%")
    print(f"  Indicators: {[i.value for i in group.indicators[:5]]}...")
```

### False Positive Analysis

```python
from ioc_analysis import FalsePositiveScorer

scorer = FalsePositiveScorer(model_path="fp_model.pkl")

# Score indicators
for indicator in indicators:
    fp_score = scorer.score(indicator)
    indicator.false_positive_rate = fp_score.rate

# Filter low-false-positive indicators
high_confidence = [i for i in indicators if i.false_positive_rate < 0.1]
print(f"High confidence indicators: {len(high_confidence)}/{len(indicators)}")
```

### Lifecycle Management

```python
from ioc_analysis import LifecycleManager, LifecyclePolicy

manager = LifecycleManager(
    policy=LifecyclePolicy(
        default_ttl_days=90,
        high_confidence_ttl_days=180,
        auto_retire=True,
        archive_after_days=365,
    )
)

# Check lifecycle status
for indicator in indicators:
    status = manager.get_status(indicator)
    print(f"{indicator.value}: {status.state} (expires: {status.expires})")

# Purge expired indicators
purged = manager.purge_expired()
print(f"Purged {purged} expired indicators")
```

## Best Practices

- **Enrich Before Actioning**: Always enrich indicators with contextual data before adding them to blocklists
- **Validate Against Your Environment**: Check if indicators appear in legitimate traffic before blocking
- **Use Temporal Windows**: Correlate indicators within reasonable time windows to reduce noise
- **Track False Positives**: Maintain a false-positive database to improve future scoring accuracy
- **Implement Lifecycle Policies**: Define and enforce TTL policies to keep indicator sets fresh
- **Audit Enrichment Sources**: Regularly assess the quality and freshness of enrichment data sources
- **Batch Processing**: Use batch operations for large indicator sets to optimize API usage
- **Document Correlation Logic**: Maintain clear documentation of how correlations are established

## Advanced Analysis Workflows

### Multi-Source IOC Enrichment Pipeline

```python
from ioc_analysis import EnrichmentPipeline, EnrichmentConfig, SourcePriority

pipeline = EnrichmentPipeline(
    config=EnrichmentConfig(
        max_concurrent_sources=6,
        timeout_per_source=30,
        retry_count=2,
        cache_ttl_hours=24,
        dedup_enabled=True
    )
)

# Register enrichment sources with priority ordering
pipeline.register_source(
    name="virustotal",
    api_key="your-vt-key",
    priority=SourcePriority.HIGH,
    rate_limit=4,  # requests per minute
    capabilities=["hash_lookup", "ip_lookup", "domain_lookup", "url_lookup"]
)

pipeline.register_source(
    name="abuseipdb",
    api_key="your-abuseipdb-key",
    priority=SourcePriority.HIGH,
    rate_limit=60,
    capabilities=["ip_lookup"]
)

pipeline.register_source(
    name="shodan",
    api_key="your-shodan-key",
    priority=SourcePriority.MEDIUM,
    rate_limit=1,
    capabilities=["ip_lookup", "domain_lookup"]
)

pipeline.register_source(
    name="otx",
    api_key="your-otx-key",
    priority=SourcePriority.MEDIUM,
    rate_limit=100,
    capabilities=["hash_lookup", "ip_lookup", "domain_lookup", "url_lookup"]
)

pipeline.register_source(
    name="greynoise",
    api_key="your-greynoise-key",
    priority=SourcePriority.MEDIUM,
    rate_limit=30,
    capabilities=["ip_lookup"]
)

pipeline.register_source(
    name="urlhaus",
    priority=SourcePriority.LOW,
    rate_limit=10,
    capabilities=["url_lookup", "domain_lookup"]
)

# Enrich a batch of indicators
indicators = [
    {"type": "ip", "value": "198.51.100.42"},
    {"type": "domain", "value": "malicious-example.com"},
    {"type": "hash", "value": "d41d8cd98f00b204e9800998ecf8427e"},
    {"type": "url", "value": "http://malicious-example.com/payload.exe"},
    {"type": "ip", "value": "203.0.113.55"},
]

results = pipeline.enrich_batch(indicators)

print("Enrichment Results:")
for result in results:
    print(f"\n  {result.indicator_type}: {result.indicator_value}")
    print(f"    Sources queried: {result.sources_queried}")
    print(f"    Sources responded: {result.sources_responded}")
    print(f"    Confidence score: {result.confidence_score:.1%}")
    print(f"    Malicious: {result.is_malicious}")
    print(f"    Threat score: {result.threat_score:.2f}")
    print(f"    Tags: {result.tags}")
    print(f"    First seen: {result.first_seen}")
    print(f"    Last seen: {result.last_seen}")

    if result.geolocation:
        print(f"    Geo: {result.geolocation.country}, {result.geolocation.city}")
    if result.asn:
        print(f"    ASN: {result.asn.number} ({result.asn.organization})")
    if result.whois:
        print(f"    Registrant: {result.whois.registrant}")
```

### IOC Relationship Graph Builder

```python
from ioc_analysis import RelationshipGraph, GraphNode, GraphEdge, RelationshipType

graph = RelationshipGraph()

# Build relationship graph from enriched indicators
indicators_to_graph = [
    GraphNode(id="ip-198.51.100.42", type="ip", attributes={"country": "RU"}),
    GraphNode(id="domain-evil.com", type="domain", attributes={"registrar": "GoDaddy"}),
    GraphNode(id="hash-abc123", type="hash_md5", attributes={"file_name": "malware.exe"}),
    GraphNode(id="hash-def456", type="hash_sha256", attributes={"file_name": "dropper.dll"}),
    GraphNode(id="actor-apt28", type="threat_actor", attributes={"aliases": ["Fancy Bear"]}),
    GraphNode(id="campaign-op1", type="campaign", attributes={"name": "Operation Shadow"}),
    GraphNode(id="tool-mimikatz", type="tool", attributes={"category": "credential_harvest"}),
    GraphNode(id="cve-2023-1234", type="vulnerability", attributes={"cvss": 9.8}),
    GraphNode(id="email-admin@corp.com", type="email", attributes={"role": "sysadmin"}),
]

edges = [
    GraphEdge(src="ip-198.51.100.42", dst="domain-evil.com", type=RelationshipType.RESOLVES_TO),
    GraphEdge(src="ip-198.51.100.42", dst="hash-abc123", type=RelationshipType.HOSTS),
    GraphEdge(src="domain-evil.com", dst="hash-def456", type=RelationshipType.DISTRIBUTES),
    GraphEdge(src="actor-apt28", dst="campaign-op1", type=RelationshipType.PARTICIPATES_IN),
    GraphEdge(src="campaign-op1", dst="hash-abc123", type=RelationshipType.USES),
    GraphEdge(src="campaign-op1", dst="tool-mimikatz", type=RelationshipType.USES),
    GraphEdge(src="campaign-op1", dst="cve-2023-1234", type=RelationshipType.EXPLOITS),
    GraphEdge(src="campaign-op1", dst="email-admin@corp.com", type=RelationshipType.TARGETS),
    GraphEdge(src="ip-198.51.100.42", dst="campaign-op1", type=RelationshipType.ASSOCIATED_WITH),
]

for node in indicators_to_graph:
    graph.add_node(node)
for edge in edges:
    graph.add_edge(edge)

# Analyze graph properties
centrality = graph.compute_centrality()
print("Node Centrality (Top 5):")
for node_id, score in sorted(centrality.items(), key=lambda x: -x[1])[:5]:
    node = graph.get_node(node_id)
    print(f"  {node_id} ({node.type}): centrality={score:.4f}")

# Find shortest paths between indicators
paths = graph.find_paths("ip-198.51.100.42", "email-admin@corp.com")
print(f"\nPaths from IP to target email: {len(paths)}")
for path in paths:
    print(f"  {' -> '.join(path.nodes)}")
    print(f"    Length: {path.length}, Confidence: {path.confidence:.2f}")

# Detect communities / clusters
communities = graph.detect_communities()
print(f"\nDetected Communities: {len(communities)}")
for i, community in enumerate(communities):
    print(f"  Community {i+1}: {len(community.nodes)} nodes")
    for node_id in community.nodes[:5]:
        node = graph.get_node(node_id)
        print(f"    - {node_id} ({node.type})")
```

### Campaign Identification Through Temporal Clustering

```python
from ioc_analysis import CampaignIdentifier, TemporalCluster, ClusterAlgorithm

identifier = CampaignIdentifier(
    algorithm=ClusterAlgorithm.DBSCAN,
    eps_hours=24,
    min_samples=3,
    similarity_threshold=0.7
)

# Group indicators into campaigns based on temporal and attribute similarity
campaigns = identifier.identify_campaigns(
    indicators=enriched_indicators,
    attributes_for_similarity=[
        "infrastructure_overlap",
        "malware_family",
        "target_sector",
        "geographic_targeting",
        "ttp_overlap"
    ]
)

print(f"Campaign Identification Results:")
print(f"  Total indicators analyzed: {len(enriched_indicators)}")
print(f"  Campaigns identified: {len(campaigns)}")

for campaign in campaigns:
    print(f"\n  Campaign: {campaign.campaign_id}")
    print(f"    Indicator count: {len(campaign.indicators)}")
    print(f"    Time span: {campaign.first_indicator_seen} to {campaign.last_indicator_seen}")
    print(f"    Confidence: {campaign.confidence:.1%}")
    print(f"    Infrastructure overlap: {campaign.infrastructure_overlap:.1%}")
    print(f"    Primary malware: {campaign.primary_malware}")
    print(f"    Target sectors: {campaign.target_sectors}")
    print(f"    Threat actors: {campaign.associated_actors}")

    # Show top indicators
    print(f"    Top indicators:")
    for ioc in campaign.top_indicators(n=5):
        print(f"      {ioc.type}: {ioc.value} (score: {ioc.threat_score:.2f})")
```

## Advanced Detection Techniques

### Domain Generation Algorithm (DGA) Detection

```python
from ioc_analysis import DGADetector, DGAAlgorithm, DetectionResult

detector = DGADetector(
    algorithms=[
        DGAAlgorithm.ENTROPY_ANALYSIS,
        DGAAlgorithm.NGRAM_FREQUENCY,
        DGAAlgorithm.LEVENSHTEIN_DISTANCE,
        DGAAlgorithm.MARKOV_CHAIN,
        DGAAlgorithm.NEURAL_NETWORK,
    ],
    confidence_threshold=0.8
)

# Analyze domains for DGA patterns
domains_to_analyze = [
    "google.com",
    "xkjrmqwlke.com",
    "microsoft.com",
    "aopkrmvzq.net",
    "github.com",
    "bwmqlexkr.org",
]

for domain in domains_to_analyze:
    result = detector.analyze(domain)
    label = "DGA" if result.is_dga else "LEGITIMATE"
    print(f"{domain}: {label} (confidence: {result.confidence:.1%})")
    print(f"  Algorithms: {result.algorithm_scores}")
    print(f"  Entropy: {result.entropy:.4f}")
    print(f"  Character frequency score: {result.char_freq_score:.4f}")
    print(f"  N-gram score: {result.ngram_score:.4f}")
    print(f"  Language model score: {result.language_model_score:.4f}")
    if result.is_dga:
        print(f"  Likely DGA family: {result.likely_dga_family}")
        print(f"  Recommended action: block domain and sinkhole")
    print()
```

### Fast Flux Detection

```python
from ioc_analysis import FastFluxDetector, FluxType

detector = FastFluxDetector(
    detection_window_hours=24,
    min_unique_ips=10,
    min_ttl_changes=5
)

# Analyze domain DNS history for fast flux indicators
flux_results = detector.analyze_domain(
    domain="malicious-example.com",
    dns_history=dns_lookup_history,
    whois_data=whois_info
)

print(f"Fast Flux Analysis for {flux_results.domain}:")
print(f"  Is Fast Flux: {flux_results.is_fast_flux}")
print(f"  Flux Type: {flux_results.flux_type.value if flux_results.is_fast_flux else 'N/A'}")
print(f"  Confidence: {flux_results.confidence:.1%}")
print(f"  Unique IPs (24h): {flux_results.unique_ip_count}")
print(f"  TTL range: {flux_results.ttl_min}s - {flux_results.ttl_max}s")
print(f"  DNS rotation frequency: {flux_results.rotation_frequency:.2f} changes/hour")
print(f"  Geographic distribution: {flux_results.geo_distribution}")
print(f"  ASN diversity: {flux_results.asn_count} unique ASNs")
print(f"  Name server diversity: {flux_results.ns_diversity}")

if flux_results.is_fast_flux:
    print(f"\n  Fast Flux Indicators:")
    for indicator in flux_results.indicators:
        print(f"    - {indicator.name}: {indicator.description}")
        print(f"      Weight: {indicator.weight:.2f}")
```

### IP Reputation Scoring Engine

```python
from ioc_analysis import ReputationScorer, ReputationDimension, ScoringModel

scorer = ReputationScorer(
    model=ScoringModel.WEIGHTED_ENSEMBLE,
    dimensions=[
        ReputationDimension.VIRUSTOTAL_DETECTION,
        ReputationDimension.ABUSEIPDB_CONFIDENCE,
        ReputationDimension.BLACKLIST_PRESENCE,
        ReputationDimension.GEOLOCATION_RISK,
        ReputationDimension.ASN_REPUTATION,
        ReputationDimension.DOMAIN_AGE,
        ReputationDimension.SSL_CERTIFICATE_VALIDITY,
        ReputationDimension.OPEN_PORTS,
        ReputationDimension.HISTORY_LENGTH,
    ]
)

# Score an IP address across all dimensions
ip_scores = scorer.score_ip(
    ip_address="198.51.100.42",
    enrichment_data=vt_result,
    abuseipdb_data=abuse_result,
    shodan_data=shodan_result
)

print(f"IP Reputation Score: {ip_scores.overall_score:.2f}/100")
print(f"Risk Level: {ip_scores.risk_level}")
print(f"Confidence: {ip_scores.confidence:.1%}")
print(f"\nDimension Breakdown:")
for dimension, score in ip_scores.dimension_scores.items():
    print(f"  {dimension.value}: {score:.2f}/100 (weight: {score.weight:.2f})")
    if score.details:
        print(f"    Details: {score.details}")

# Score a domain
domain_scores = scorer.score_domain(
    domain="malicious-example.com",
    whois_data=whois_data,
    dns_data=dns_data,
    web_data=web_scrape_data
)

print(f"\nDomain Reputation Score: {domain_scores.overall_score:.2f}/100")
print(f"Risk Level: {domain_scores.risk_level}")
```

### File Hash Threat Assessment

```python
from ioc_analysis import HashThreatAssessor, HashType, ThreatAssessment

assessor = HashThreatAssessor(
    lookup_sources=["virustotal", "hybrid-analysis", "malwarebazaar", "fileScan"],
    behavioral_sandbox="any.run"
)

# Assess a file hash
hash_result = assessor.assess(
    hash_value="d41d8cd98f00b204e9800998ecf8427e",
    hash_type=HashType.MD5,
    include_behavioral=True
)

print(f"Hash Threat Assessment:")
print(f"  Hash: {hash_result.hash_value}")
print(f"  Threat Level: {hash_result.threat_level}")
print(f"  Detection Ratio: {hash_result.detection_ratio}")
print(f"  First Submitted: {hash_result.first_submission}")
print(f"  Last Analysis: {hash_result.last_analysis}")

print(f"\n  AV Detections:")
for detection in hash_result.av_detections:
    print(f"    {detection.engine}: {detection.result}")

print(f"\n  File Properties:")
props = hash_result.file_properties
print(f"    Name: {props.file_name}")
print(f"    Type: {props.file_type}")
print(f"    Size: {props.file_size} bytes")
print(f"    Imp hash: {props.imphash}")
print(f"    SSDEEP: {props.ssdeep}")

if hash_result.behavioral_analysis:
    print(f"\n  Behavioral Analysis (from sandbox):")
    beh = hash_result.behavioral_analysis
    print(f"    Network connections: {len(beh.network_connections)}")
    for conn in beh.network_connections[:5]:
        print(f"      {conn.protocol} -> {conn.dst_ip}:{conn.dst_port}")
    print(f"    Registry modifications: {len(beh.registry_modifications)}")
    print(f"    File operations: {len(beh.file_operations)}")
    print(f"    Process injections: {len(beh.process_injections)}")

# Generate IOC from the assessment
ioc = hash_result.to_ioc(tlp="amber", confidence=hash_result.detection_ratio)
print(f"\n  Generated IOC:")
print(f"    Type: {ioc.type}")
print(f"    Value: {ioc.value}")
print(f"    TLP: {ioc.tlp}")
print(f"    Confidence: {ioc.confidence:.1%}")
print(f"    Tags: {ioc.tags}")
```

## False Positive Analysis

### ML-Based False Positive Scoring

```python
from ioc_analysis import FalsePositiveMLScorer, FPFeatureSet, TrainingConfig

scorer = FalsePositiveMLScorer(
    feature_set=FPFeatureSet.COMPREHENSIVE,
    model_config=TrainingConfig(
        algorithm="random_forest",
        n_estimators=200,
        max_depth=10,
        class_weight="balanced",
        cross_validation_folds=5
    )
)

# Train on labeled dataset
training_data = scorer.load_training_data(
    true_positives_path="/data/labeled/true_positives.csv",
    false_positives_path="/data/labeled/false_positives.csv"
)

training_result = scorer.train(training_data)
print(f"Model Training Results:")
print(f"  Accuracy: {training_result.accuracy:.4f}")
print(f"  Precision: {training_result.precision:.4f}")
print(f"  Recall: {training_result.recall:.4f}")
print(f"  F1 Score: {training_result.f1_score:.4f}")
print(f"  AUC-ROC: {training_result.auc_roc:.4f}")

# Feature importance
print(f"\n  Top Features:")
for feature, importance in training_result.feature_importance[:10]:
    print(f"    {feature}: {importance:.4f}")

# Score new indicators
for indicator in indicators:
    fp_result = scorer.score(indicator)
    print(f"\n  {indicator.value}:")
    print(f"    FP probability: {fp_result.fp_probability:.1%}")
    print(f"    TP probability: {fp_result.tp_probability:.1%}")
    print(f"    Contributing factors:")
    for factor in fp_result.contributing_factors[:3]:
        print(f"      - {factor.name}: {factor.impact:.2f} ({factor.direction})")
```

### Whitelist Management

```python
from ioc_analysis import WhitelistManager, WhitelistRule, WhitelistScope

manager = WhitelistManager()

# Create whitelist rules
rules = [
    WhitelistRule(
        name="CDN Provider IPs",
        scope=WhitelistScope.GLOBAL,
        match_pattern="ip:204.79.197.0/24",  # Microsoft CDN
        reason="Microsoft CDN infrastructure",
        expires_days=365,
        added_by="soc_team"
    ),
    WhitelistRule(
        name="AWS S3 Buckets",
        scope=WhitelistScope.GLOBAL,
        match_pattern="ip:52.92.0.0/16",
        reason="AWS S3 US-West-2 range",
        expires_days=180,
        added_by="soc_team"
    ),
    WhitelistRule(
        name="Internal DNS Servers",
        scope=WhitelistScope.ORGANIZATION,
        match_pattern="ip:10.0.0.53",
        reason="Primary internal DNS",
        expires_days=365,
        added_by="admin"
    ),
    WhitelistRule(
        name="Approved SaaS Domains",
        scope=WhitelistScope.GLOBAL,
        match_pattern="domain:*.salesforce.com|*.office365.com|*.google.com",
        reason="Approved cloud services",
        expires_days=365,
        added_by="it_team"
    ),
]

for rule in rules:
    manager.add_rule(rule)

# Check if indicator is whitelisted
for indicator in indicators:
    wl_result = manager.check_whitelist(indicator)
    if wl_result.is_whitelisted:
        print(f"  WHITELISTED: {indicator.value}")
        print(f"    Rule: {wl_result.matched_rule.name}")
        print(f"    Reason: {wl_result.matched_rule.reason}")
    else:
        print(f"  NOT WHITELISTED: {indicator.value}")

# Export whitelist for SIEM/SOAR integration
whitelist_export = manager.export(format="stix", output_path="/exports/whitelist_stix.json")
print(f"\nWhitelist exported: {whitelist_export.item_count} rules")
```

## Database Schema for IOC Storage

```sql
-- IOC master table
CREATE TABLE ioc_indicators (
    ioc_id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    ioc_type        ENUM('ip', 'domain', 'url', 'hash_md5', 'hash_sha1',
                         'hash_sha256', 'email', 'mutex', 'file_name',
                         'registry_key', 'certificate_hash', 'cve') NOT NULL,
    ioc_value       VARCHAR(4096) NOT NULL,
    tlp             ENUM('white', 'green', 'amber', 'red') DEFAULT 'green',
    confidence      DOUBLE NOT NULL DEFAULT 0.0,
    threat_score    DOUBLE DEFAULT 0.0,
    false_positive_rate DOUBLE DEFAULT 0.0,
    is_whitelisted  BOOLEAN DEFAULT FALSE,
    lifecycle_state ENUM('new', 'active', 'aging', 'expired', 'retired') DEFAULT 'new',
    first_seen      TIMESTAMP NULL,
    last_seen       TIMESTAMP NULL,
    expires_at      TIMESTAMP NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by      VARCHAR(128),
    notes           TEXT,
    UNIQUE KEY uk_type_value (ioc_type, ioc_value(512)),
    INDEX idx_type (ioc_type),
    INDEX idx_confidence (confidence DESC),
    INDEX idx_threat_score (threat_score DESC),
    INDEX idx_lifecycle (lifecycle_state),
    INDEX idx_first_seen (first_seen),
    INDEX idx_last_seen (last_seen),
    INDEX idx_expires (expires_at)
);

-- IOC enrichment results
CREATE TABLE ioc_enrichment (
    enrichment_id       BIGINT AUTO_INCREMENT PRIMARY KEY,
    ioc_id              BIGINT NOT NULL,
    source_name         VARCHAR(128) NOT NULL,
    source_query_time   TIMESTAMP NOT NULL,
    raw_response        JSON,
    is_malicious        BOOLEAN,
    detection_count     INT,
    total_engines       INT,
    threat_score        DOUBLE,
    tags                JSON,
    geolocation_country VARCHAR(2),
    geolocation_city    VARCHAR(128),
    asn_number          INT,
    asn_organization    VARCHAR(256),
    whois_registrant    VARCHAR(512),
    whois_registration_date DATE,
    whois_expiration_date   DATE,
    ssl_issuer          VARCHAR(512),
    ssl_subject         VARCHAR(512),
    ssl_valid_from      TIMESTAMP,
    ssl_valid_to        TIMESTAMP,
    FOREIGN KEY (ioc_id) REFERENCES ioc_indicators(ioc_id),
    INDEX idx_ioc (ioc_id),
    INDEX idx_source (source_name),
    INDEX idx_malicious (is_malicious),
    INDEX idx_query_time (source_query_time)
);

-- IOC relationships
CREATE TABLE ioc_relationships (
    relationship_id     BIGINT AUTO_INCREMENT PRIMARY KEY,
    source_ioc_id       BIGINT NOT NULL,
    target_ioc_id       BIGINT NOT NULL,
    relationship_type   ENUM('resolves_to', 'hosts', 'distributes', 'communicates_with',
                             'drops', 'exploits', 'associated_with', 'variant_of',
                             'similar_to', 'subdomain_of') NOT NULL,
    confidence          DOUBLE DEFAULT 1.0,
    first_seen          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    evidence            TEXT,
    FOREIGN KEY (source_ioc_id) REFERENCES ioc_indicators(ioc_id),
    FOREIGN KEY (target_ioc_id) REFERENCES ioc_indicators(ioc_id),
    INDEX idx_source (source_ioc_id),
    INDEX idx_target (target_ioc_id),
    INDEX idx_type (relationship_type),
    UNIQUE KEY uk_relationship (source_ioc_id, target_ioc_id, relationship_type)
);

-- IOC campaigns
CREATE TABLE ioc_campaigns (
    campaign_id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    campaign_uid        VARCHAR(64) UNIQUE NOT NULL,
    campaign_name       VARCHAR(256),
    description         TEXT,
    first_seen          TIMESTAMP NOT NULL,
    last_seen           TIMESTAMP NOT NULL,
    confidence          DOUBLE,
    primary_malware     VARCHAR(128),
    target_sectors      JSON,
    target_countries    JSON,
    associated_actors   JSON,
    mitre_techniques    JSON,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_time_range (first_seen, last_seen),
    INDEX idx_confidence (confidence DESC)
);

-- IOC to campaign mapping
CREATE TABLE ioc_campaign_map (
    ioc_id          BIGINT NOT NULL,
    campaign_id     BIGINT NOT NULL,
    role            ENUM('infrastructure', 'payload', 'tool', 'credential', 'other') DEFAULT 'other',
    confidence      DOUBLE DEFAULT 1.0,
    first_associated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (ioc_id, campaign_id),
    FOREIGN KEY (ioc_id) REFERENCES ioc_indicators(ioc_id),
    FOREIGN KEY (campaign_id) REFERENCES ioc_campaigns(campaign_id)
);

-- False positive tracking
CREATE TABLE ioc_false_positives (
    fp_id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    ioc_id          BIGINT NOT NULL,
    reporter        VARCHAR(128) NOT NULL,
    report_reason   TEXT NOT NULL,
    report_date     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified        BOOLEAN DEFAULT FALSE,
    verified_by     VARCHAR(128),
    verified_date   TIMESTAMP,
    fp_category     ENUM('cdn', 'shared_hosting', 'dynamic_ip', 'popular_domain',
                         'internal_asset', 'whitelist_miss', 'data_error', 'other'),
    resolution      ENUM('pending', 'confirmed_fp', 'confirmed_tp', 'dismissed') DEFAULT 'pending',
    FOREIGN KEY (ioc_id) REFERENCES ioc_indicators(ioc_id),
    INDEX idx_ioc (ioc_id),
    INDEX idx_resolution (resolution),
    INDEX idx_report_date (report_date)
);

-- IOC lifecycle audit log
CREATE TABLE ioc_lifecycle_log (
    log_id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    ioc_id          BIGINT NOT NULL,
    action          ENUM('created', 'enriched', 'updated', 'whitelisted',
                         'blacklisted', 'expired', 'retired', 'reactivated') NOT NULL,
    old_state       VARCHAR(64),
    new_state       VARCHAR(64),
    performed_by    VARCHAR(128),
    performed_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reason          TEXT,
    FOREIGN KEY (ioc_id) REFERENCES ioc_indicators(ioc_id),
    INDEX idx_ioc (ioc_id),
    INDEX idx_action (action),
    INDEX idx_performed_at (performed_at)
);

-- Bulk import tracking
CREATE TABLE ioc_bulk_imports (
    import_id       BIGINT AUTO_INCREMENT PRIMARY KEY,
    import_batch_id VARCHAR(64) UNIQUE NOT NULL,
    source_file     VARCHAR(1024),
    source_format   ENUM('csv', 'stix', 'misp', 'json', 'text') NOT NULL,
    total_indicators INT,
    imported_count   INT,
    duplicate_count  INT,
    error_count      INT,
    imported_by      VARCHAR(128),
    imported_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration_seconds DOUBLE,
    errors_log       TEXT,
    INDEX idx_imported_at (imported_at)
);
```

## Integration Patterns

### STIX 2.1 Bundle Export

```python
from ioc_analysis import STIXExporter, STIXBundle, IdentityConfig

exporter = STIXExporter(
    identity=IdentityConfig(
        name="ACME Security Team",
        identity_class="organization",
        sectors=["technology"],
        contact_info="soc@acme.com"
    ),
    tlp_default="amber"
)

# Export indicators as STIX 2.1 bundle
stix_bundle = exporter.export_indicators(
    indicators=enriched_indicators,
    include_relationships=True,
    include_campaigns=True,
    include_threat_actors=True,
    custom_properties={"x_data_source": "internal-hunting"}
)

# Validate STIX bundle
validation = stix_bundle.validate()
print(f"STIX Bundle Validation:")
print(f"  Valid: {validation.is_valid}")
print(f"  Objects: {len(stix_bundle.objects)}")
print(f"  SDOs: {validation.sdo_count}")
print(f"  SROs: {validation.sro_count}")
print(f"  SCO: {validation.sco_count}")

# Export to file
stix_bundle.serialize(
    output_path="/exports/ioc_stix_bundle.json",
    pretty=True
)
print(f"STIX bundle exported: {stix_bundle.object_count} objects")
```

### MISP Event Synchronization

```python
from ioc_analysis import MISPSync, MISPEvent, MISPAttribute

sync = MISPSync(
    server_url="https://misp.example.com",
    api_key="your-misp-key",
    verify_ssl=True
)

# Create MISP event from IOC analysis
event = MISPEvent(
    info="Campaign Infrastructure - Operation Shadow",
    distribution=1,  # This community
    threat_level_id=2,  # Medium
    analysis=2,  # Complete
    date="2024-01-20",
    tags=["campaign:operation-shadow", "tlp:amber", "apt:apt28"]
)

# Add indicators as MISP attributes
for indicator in enriched_indicators:
    attr = MISPAttribute(
        type=indicator.misp_type,
        value=indicator.value,
        comment=f"Confidence: {indicator.confidence:.0%}, Threat score: {indicator.threat_score:.2f}",
        to_ids=True,
        category="Network activity",
        disable_correlation=False
    )
    event.add_attribute(attr)

# Add relationships
for rel in relationships:
    event.add_relationship(
        source_uuid=rel.source_uuid,
        relationship_type=rel.type,
        target_uuid=rel.target_uuid
    )

# Push to MISP
result = sync.push_event(event)
print(f"MISP Event Pushed:")
print(f"  Event ID: {result.event_id}")
print(f"  UUID: {result.uuid}")
print(f"  Attributes: {result.attribute_count}")
print(f"  Warnings: {result.warning_count}")
```

### Automated Blocklist Generation

```python
from ioc_analysis import BlocklistGenerator, BlocklistFormat, BlocklistTarget

generator = BlocklistGenerator(
    min_confidence=0.8,
    min_threat_score=0.6,
    exclude_whitelisted=True,
    max_age_days=90
)

# Generate blocklists for different targets
blocklists = [
    BlocklistTarget(
        name="Firewall - External Block",
        format=BlocklistFormat.CSV,
        ioc_types=["ip", "domain", "url"],
        output_path="/exports/blocklist_firewall.csv",
        columns=["value", "type", "confidence", "first_seen", "description"]
    ),
    BlocklistTarget(
        name="DNS Sinkhole",
        format=BlocklistFormat.HOSTS,
        ioc_types=["domain"],
        output_path="/exports/blocklist_sinkhole.hosts",
        sinkhole_ip="198.51.100.1"
    ),
    BlocklistTarget(
        name="Email Gateway",
        format=BlocklistFormat.CSV,
        ioc_types=["domain", "email", "hash_sha256"],
        output_path="/exports/blocklist_email.csv"
    ),
    BlocklistTarget(
        name="EDR/AV Exclusion",
        format=BlocklistFormat.JSON,
        ioc_types=["hash_sha256", "hash_md5"],
        output_path="/exports/blocklist_edr.json",
        include_signatures=True
    ),
]

for target in blocklists:
    result = generator.generate(
        target=target,
        indicators=enriched_indicators,
        format=target.format
    )
    print(f"Generated {target.name}:")
    print(f"  Indicators: {result.indicator_count}")
    print(f"  File: {result.output_path}")
    print(f"  Size: {result.file_size_bytes} bytes")
    print(f"  Hash: {result.sha256}")
```

## Performance Tuning

### Batch Processing Optimization

```python
from ioc_analysis import BatchProcessor, ProcessingConfig

processor = BatchProcessor(
    config=ProcessingConfig(
        batch_size=1000,
        max_concurrent_batches=4,
        cache_enabled=True,
        cache_ttl_hours=24,
        rate_limit_per_source=100,
        retry_failed=True,
        max_retries=3
    )
)

# Process large indicator set efficiently
result = processor.process(
    indicators=large_indicator_set,  # 100,000+ indicators
    enrichment_sources=["virustotal", "abuseipdb", "shodan"],
    output_path="/results/batch_enrichment/"
)

print(f"Batch Processing Results:")
print(f"  Total indicators: {result.total_processed}")
print(f"  Successfully enriched: {result.success_count}")
print(f"  Failed: {result.failure_count}")
print(f"  Cached (skipped): {result.cached_count}")
print(f"  Duration: {result.duration_seconds:.1f}s")
print(f"  Throughput: {result.throughput_per_second:.0f} indicators/second")
print(f"  API calls made: {result.api_call_count}")
print(f"  API errors: {result.api_error_count}")

# Performance breakdown by source
print(f"\n  Source Performance:")
for source, stats in result.source_stats.items():
    print(f"    {source}:")
    print(f"      Queried: {stats.queried}")
    print(f"      Responded: {stats.responded}")
    print(f"      Rate limited: {stats.rate_limited}")
    print(f"      Avg response time: {stats.avg_response_ms:.0f}ms")
```

## Reporting Templates

### IOC Analysis Report

```python
from ioc_analysis import IOCReport, ReportSection, IndicatorTable

report = IOCReport(
    title="IOC Analysis Report - Campaign Infrastructure",
    classification="TLP:AMBER",
    date_range=("2024-01-01", "2024-01-20"),
    analyst="analyst-01"
)

report.add_section(ReportSection(
    heading="Executive Summary",
    content="""
        Analysis of 847 indicators identified 23 unique infrastructure clusters
        associated with an active APT campaign. Enrichment across 6 sources
        confirmed 312 indicators as malicious with high confidence. Three
        campaigns were identified through temporal and infrastructure overlap
        analysis.
    """
))

report.add_section(ReportSection(
    heading="Key Findings",
    template="findings",
    findings=[
        "Identified 3 distinct campaigns with shared infrastructure overlap",
        "23 IP addresses associated with known APT28 infrastructure",
        "12 domains registered within 48 hours of campaign start",
        "DGA-generated domains detected with 94% confidence",
        "Fast flux behavior observed on 7 domains",
    ]
))

report.add_section(ReportSection(
    heading="Indicator Summary",
    template=IndicatorTable,
    indicators=enriched_indicators,
    columns=["type", "value", "confidence", "threat_score", "first_seen", "tags"],
    sort_by="threat_score",
    sort_desc=True,
    limit=50
))

report.add_section(ReportSection(
    heading="Recommended Actions",
    content="""
        1. Block 312 high-confidence malicious indicators at perimeter
        2. Deploy YARA rules for identified malware families
        3. Configure SIEM alerts for remaining low-confidence indicators
        4. Share TLP:GREEN indicators with trusted partners
        5. Monitor for new infrastructure registration patterns
    """
))

report.export(
    output_path="/reports/ioc_analysis_report.pdf",
    formats=["pdf", "html", "json"]
)
```

## Related Modules

- **threat-intelligence**: Core intelligence collection and management
- **behavioral-analysis**: Behavioral pattern analysis for advanced detection
- **forensic-analysis**: Forensic investigation for indicator validation
