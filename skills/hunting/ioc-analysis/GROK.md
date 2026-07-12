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

## Related Modules

- **threat-intelligence**: Core intelligence collection and management
- **behavioral-analysis**: Behavioral pattern analysis for advanced detection
- **forensic-analysis**: Forensic investigation for indicator validation
