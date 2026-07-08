# Competitive Intelligence Agent

Comprehensive competitive analysis, market intelligence, SWOT analysis, competitor tracking, trend monitoring, benchmarking, and strategic intelligence generation for data-driven competitive strategy.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Competitor Tracking](#competitor-tracking)
  - [SWOT Analysis](#swot-analysis)
  - [Trend Monitoring](#trend-monitoring)
  - [Benchmarking](#benchmarking)
  - [Intelligence Collection](#intelligence-collection)
  - [Market Research](#market-research)
  - [Strategic Brief](#strategic-brief)
- [API Reference](#api-reference)
  - [CompetitiveIntelAgent](#competitiveintelagent)
  - [SWOTAnalyzer](#swotanalyzer)
  - [TrendMonitor](#trendmonitor)
  - [BenchmarkEngine](#benchmarkengine)
  - [IntelligenceCollector](#intelligencecollector)
- [Data Models](#data-models)
- [Intelligence Sources](#intelligence-sources)
- [Configuration](#configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Competitive Intelligence Agent is a Python-based system for gathering, analyzing, and distributing actionable competitive intelligence. It combines structured analytical frameworks with data-driven trend detection and multi-metric benchmarking.

**Key Capabilities:**
- Competitor profile management with threat assessment
- SWOT analysis with strategic priority determination
- Trend detection from streaming data points
- Multi-metric competitive benchmarking
- Intelligence collection and full-text search
- Market research and landscape analysis
- Executive strategic brief generation

## Features

| Feature | Description |
|---------|-------------|
| Competitor Tracking | Maintain detailed profiles with threat levels |
| SWOT Analysis | Structured internal/external factor analysis |
| Trend Detection | Sentiment-based trend direction identification |
| Benchmarking | Multi-metric ranking and competitive scoring |
| Intelligence Collection | Multi-source intelligence ingestion and search |
| Market Research | Competitive landscape analysis |
| Strategic Briefs | Executive-level intelligence summaries |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Competitive Intelligence Agent                 │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │Competitor│ │  SWOT    │ │  Trend   │ │Benchmark │     │
│  │ Profiler │ │ Analyzer │ │ Monitor  │ │  Engine  │     │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘     │
│       │            │            │            │             │
│  ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐     │
│  │  Intel   │ │  Market  │ │Strategic │ │ Pricing  │     │
│  │Collector │ │ Research │ │  Brief   │ │ Analyzer │     │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

```python
from agents.competitive_intel.agent import CompetitiveIntelAgent

# Initialize
agent = CompetitiveIntelAgent()

# Add a competitor
comp = agent.add_competitor(
    name="TechCorp Alpha",
    competitor_type="direct",
    threat_level="high",
)

# Analyze
analysis = agent.analyze_competitor(comp["competitor_id"])
print(f"Threat score: {analysis['threat_assessment']['threat_score']}")

# SWOT
swot = agent.perform_swot(
    subject="Our Company",
    strengths=["Innovation", "Team"],
    weaknesses=["Brand", "Scale"],
    opportunities=["Market growth"],
    threats=["New entrants"],
)
```

```bash
python agents/competitive-intel/agent.py
```

## Usage

### Competitor Tracking

```python
# Add competitors
agent.add_competitor(
    name="InnovateTech",
    competitor_type="direct",
    products=["AI Platform"],
    strengths=["Cutting-edge AI", "Developer community"],
    weaknesses=["Limited enterprise sales"],
    threat_level="medium",
)

# Analyze a competitor
analysis = agent.analyze_competitor(comp["competitor_id"])
print(f"Positioning: {analysis['competitive_positioning']['position']}")
```

### SWOT Analysis

```python
swot = agent.perform_swot(
    subject="Our Product",
    strengths=["Best-in-class UX", "Fast performance", "Strong API"],
    weaknesses=["Limited integrations", "No mobile app"],
    opportunities=["Enterprise adoption", "International expansion"],
    threats=["Price competition", "Regulatory changes"],
)

print(f"Score: {swot['overall_score']}")
print(f"Priority: {swot['strategic_priority']}")
```

### Trend Monitoring

```python
# Add data points
for _ in range(10):
    agent._trend_monitor.add_data_point(
        "AI Adoption", "news", "AI spending increases", "positive"
    )

# Detect trends
trends = agent.monitor_trends(topics=["AI Adoption"])
for trend in trends["trends"]:
    print(f"{trend['name']}: {trend['direction']} (impact: {trend['impact_score']})")
```

### Benchmarking

```python
# Add metrics
agent.add_benchmark_metric(
    category="product",
    metric_name="API Response Time",
    our_value=45,
    competitor_values={"TechCorp": 60, "InnovateTech": 80},
    industry_average=75,
    unit="ms",
    higher_is_better=False,
)

# Get rankings
rankings = agent.get_benchmark_rankings("product")
print(f"Position: {rankings['competitive_score']['position']}")
```

### Intelligence Collection

```python
# Collect intelligence
agent.add_intelligence(
    title="TechCorp announces new product",
    summary="Major product launch targeting enterprise market",
    source="news_article",
    competitor_name="TechCorp",
    category="product_launch",
    key_findings=["Targets enterprise", "Premium pricing"],
)

# Search intelligence
results = agent.search_intelligence(competitor="TechCorp")
print(f"Found {len(results)} reports")
```

### Market Research

```python
landscape = agent.conduct_market_research(
    market="Cloud Computing",
    segment="enterprise",
    competitors=[comp1_id, comp2_id],
)

print(f"Competitors: {landscape['competitor_count']}")
```

### Strategic Brief

```python
brief = agent.generate_strategic_brief()

print(f"Competitors tracked: {brief['executive_summary']['competitors_tracked']}")
print(f"Active trends: {brief['executive_summary']['active_trends']}")
print(f"Recommendations:")
for rec in brief["key_recommendations"]:
    print(f"  - {rec}")
```

## API Reference

### CompetitiveIntelAgent

| Method | Parameters | Returns |
|--------|-----------|---------|
| `add_competitor()` | name, competitor_type, website, employee_count, annual_revenue, products, strengths, weaknesses, threat_level | Competitor dict |
| `analyze_competitor()` | competitor_id, additional_data | Analysis dict |
| `conduct_market_research()` | market, segment, competitors | Landscape dict |
| `perform_swot()` | subject, strengths, weaknesses, opportunities, threats | SWOT dict |
| `monitor_trends()` | topics | Trends dict |
| `add_intelligence()` | title, summary, source, competitor_name, category, key_findings | Report dict |
| `search_intelligence()` | keyword, competitor, category | List of reports |
| `add_benchmark_metric()` | category, metric_name, our_value, competitor_values, industry_average | Metric dict |
| `get_benchmark_rankings()` | category | Rankings dict |
| `generate_strategic_brief()` | — | Brief dict |
| `get_competitive_landscape()` | — | Landscape overview dict |
| `list_competitors()` | — | List of competitor dicts |
| `get_status()` | — | Agent status dict |

### SWOTAnalyzer

| Method | Parameters | Returns |
|--------|-----------|---------|
| `analyze()` | subject, strengths, weaknesses, opportunities, threats | SWOT analysis |
| `compare_swot()` | analysis_ids | Comparison dict |
| `get_strategic_recommendations()` | analysis_id | SO/WO/ST/WT strategies |

### TrendMonitor

| Method | Parameters | Returns |
|--------|-----------|---------|
| `add_data_point()` | topic, source, content, sentiment | — |
| `detect_trends()` | topics, min_data_points | List of trends |
| `get_trend_summary()` | — | Summary dict |

### BenchmarkEngine

| Method | Parameters | Returns |
|--------|-----------|---------|
| `add_metric()` | category, metric_name, our_value, competitor_values, industry_average | Metric |
| `get_rankings()` | category | Rankings list |
| `competitive_score()` | category | Score and position |
| `compare_features()` | product_name, features, competitors | Feature comparison |
| `analyze_pricing()` | product_name, our_price, competitor_prices | Pricing analysis |

### IntelligenceCollector

| Method | Parameters | Returns |
|--------|-----------|---------|
| `collect()` | title, summary, source, competitor_name, category, key_findings | Report |
| `search()` | keyword, competitor, category, source, limit | List of reports |
| `get_latest()` | competitor, limit | Latest reports |
| `get_stats()` | — | Collection statistics |

## Data Models

### CompetitorProfile
Full competitor profile with revenue, products, technologies, strengths, weaknesses, and threat level.

### MarketTrend
Detected trend with direction, impact score, drivers, and confidence level.

### SWOTAnalysis
Structured SWOT with internal/external factors, overall score, and strategic priority.

### BenchmarkMetric
Metric comparison across competitors with ranking and competitive scoring.

### IntelReport
Intelligence report with source, findings, confidence, and strategic implications.

## Intelligence Sources

| Source | Reliability | Best For |
|--------|-------------|----------|
| News Articles | Moderate | Recent events |
| Earnings Calls | High | Financial performance |
| Patent Filings | High | Technology direction |
| Job Postings | Moderate | Hiring priorities |
| Customer Reviews | Moderate | Product feedback |
| Industry Reports | High | Market sizing |
| GitHub | High | Tech stack, activity |
| Crunchbase | High | Funding, growth |
| LinkedIn | Moderate | Team, hiring signals |
| Glassdoor | Low-Moderate | Culture, satisfaction |

## Configuration

```python
config = {
    "user": "analyst",
    "default_competitor_type": "direct",
    "trend_min_data_points": 5,
    "benchmark_threshold": 0.5,
}
agent = CompetitiveIntelAgent(config)
```

## Best Practices

1. **Diversify Sources** — Don't rely on a single intelligence source
2. **Verify Before Acting** — Cross-reference findings across multiple sources
3. **Keep Data Fresh** — Stale intelligence leads to stale strategy
4. **Track Emerging Competitors** — Don't focus only on established players
5. **Quantify Where Possible** — Metrics beat anecdotes for strategic decisions
6. **Act on Insights** — Intelligence without action is trivia
7. **Document Assumptions** — Track what you assumed vs what you verified
8. **Regular Review** — Schedule periodic competitive landscape reviews

## Troubleshooting

| Problem | Solution |
|---------|----------|
| SWOT analysis too generic | Add more company-specific data points |
| Trend detection inaccurate | Increase minimum data point threshold |
| Benchmark rankings outdated | Refresh competitor metrics |
| Intelligence reports conflicting | Check confidence levels, prefer verified sources |
| Strategic brief lacks depth | Increase intelligence collection volume |
| Competitor profile incomplete | Fill in missing fields with latest intelligence |

## Files

- `agent.py` — Main implementation (~900 lines)
- `ARCHITECTURE.md` — System architecture with diagrams
- `GROK.md` — Agent instructions and identity
- `README.md` — This file

## Contributing

1. Add new intelligence source handlers
2. Enhance trend detection algorithms
3. Add new analytical frameworks (Porter, PESTEL)
4. Improve benchmark metric calculations
5. Update documentation for API changes

## License

Part of the Awesome Grok Skills collection. See project root for license details.
