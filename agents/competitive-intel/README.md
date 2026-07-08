# Competitive Intelligence Agent

Comprehensive competitive analysis, market intelligence, SWOT analysis, competitor tracking, trend monitoring, benchmarking, and strategic intelligence generation for data-driven competitive strategy.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
  - [Installation](#installation)
  - [Basic Setup](#basic-setup)
  - [First Analysis](#first-analysis)
  - [Running the CLI](#running-the-cli)
- [Usage](#usage)
  - [Competitor Tracking](#competitor-tracking)
  - [SWOT Analysis](#swot-analysis)
  - [Trend Monitoring](#trend-monitoring)
  - [Benchmarking](#benchmarking)
  - [Intelligence Collection](#intelligence-collection)
  - [Market Research](#market-research)
  - [Strategic Brief](#strategic-brief)
  - [Competitive Landscape Overview](#competitive-landscape-overview)
  - [Pricing Analysis](#pricing-analysis)
  - [Feature Comparison](#feature-comparison)
- [API Reference](#api-reference)
  - [CompetitiveIntelAgent](#competitiveintelagent)
  - [CompetitorProfiler](#competitorprofiler)
  - [SWOTAnalyzer](#swotanalyzer)
  - [TrendMonitor](#trendmonitor)
  - [BenchmarkEngine](#benchmarkengine)
  - [IntelligenceCollector](#intelligencecollector)
  - [PricingAnalyzer](#pricinganalyzer)
  - [MarketResearcher](#marketresearcher)
- [Data Models](#data-models)
  - [CompetitorProfile](#competitorprofile)
  - [MarketTrend](#markettrend)
  - [SWOTAnalysis](#swotanalysis)
  - [BenchmarkMetric](#benchmarkmetric)
  - [IntelReport](#intelreport)
  - [StrategicBrief](#strategicbrief)
  - [PricingModel](#pricingmodel)
- [Intelligence Sources](#intelligence-sources)
- [Intelligence Gathering Techniques](#intelligence-gathering-techniques)
- [Configuration](#configuration)
  - [Core Settings](#core-settings)
  - [Advanced Settings](#advanced-settings)
  - [Environment Variables](#environment-variables)
- [Examples](#examples)
  - [Startup Competitive Analysis](#startup-competitive-analysis)
  - [Enterprise Market Monitoring](#enterprise-market-monitoring)
  - [Product Launch Intelligence](#product-launch-intelligence)
  - [Pricing Strategy Optimization](#pricing-strategy-optimization)
  - [Competitive Threat Assessment](#competitive-threat-assessment)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Extending the Agent](#extending-the-agent)
  - [Adding New Analytical Frameworks](#adding-new-analytical-frameworks)
  - [Custom Intelligence Sources](#custom-intelligence-sources)
  - [Plugin Architecture](#plugin-architecture)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Competitive Intelligence Agent is a Python-based system for gathering, analyzing, and distributing actionable competitive intelligence. It combines structured analytical frameworks with data-driven trend detection and multi-metric benchmarking to give your organization a decisive strategic advantage.

**Key Capabilities:**
- Competitor profile management with threat assessment
- SWOT analysis with strategic priority determination
- Trend detection from streaming data points
- Multi-metric competitive benchmarking
- Intelligence collection and full-text search
- Market research and landscape analysis
- Executive strategic brief generation
- Pricing analysis and positioning intelligence
- Feature comparison matrices
- Automated competitive landscape monitoring

**Design Philosophy:**

The agent is designed around three core principles:

1. **Data-Driven Decisions** — Every strategic recommendation is backed by quantified metrics, sentiment analysis, and cross-referenced intelligence from multiple sources.
2. **Actionable Intelligence** — Raw data is transformed into structured insights with clear strategic implications, not just dashboards of numbers.
3. **Continuous Monitoring** — Competitive landscapes shift constantly; the agent provides streaming trend detection and real-time threat level adjustments.

---

## Prerequisites

Before using the Competitive Intelligence Agent, ensure your environment meets the following requirements:

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.9+ | Recommended 3.11+ for performance |
| pip | 21.0+ | For dependency management |
| OS | Linux, macOS, Windows | Cross-platform compatible |
| RAM | 512MB+ | Depends on intelligence volume |
| Disk | 100MB+ | For storing intelligence reports |

**Optional Dependencies:**

| Package | Purpose |
|---------|---------|
| `aiohttp` | Async HTTP for real-time intelligence feeds |
| `pandas` | Advanced data analysis and export |
| `matplotlib` | Trend visualization and charts |
| `rich` | Enhanced CLI output formatting |
| `sqlite3` | Persistent intelligence storage |

---

## Features

| Feature | Description | Complexity |
|---------|-------------|------------|
| Competitor Tracking | Maintain detailed profiles with threat levels, products, strengths, and weaknesses | Medium |
| SWOT Analysis | Structured internal/external factor analysis with strategic priority scoring | Medium |
| Trend Detection | Sentiment-based trend direction identification from streaming data points | High |
| Benchmarking | Multi-metric ranking and competitive scoring across industry dimensions | Medium |
| Intelligence Collection | Multi-source intelligence ingestion, categorization, and full-text search | High |
| Market Research | Competitive landscape analysis with market sizing and segment identification | High |
| Strategic Briefs | Executive-level intelligence summaries with actionable recommendations | Medium |
| Pricing Analysis | Competitive pricing intelligence with positioning recommendations | Medium |
| Feature Comparison | Side-by-side feature matrices against competitor products | Low |
| Threat Assessment | Automated competitor threat scoring with confidence intervals | Medium |
| Historical Tracking | Time-series analysis of competitor metrics and market position changes | Medium |
| Export & Reporting | Generate structured reports in JSON, Markdown, or CSV formats | Low |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Competitive Intelligence Agent                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────┐ │
│  │  Competitor   │  │    SWOT      │  │    Trend     │  │  Bench │ │
│  │   Profiler    │  │   Analyzer   │  │   Monitor    │  │ Engine │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └───┬────┘ │
│         │                 │                 │              │       │
│  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐  ┌───┴────┐ │
│  │   Intel      │  │   Market     │  │  Strategic   │  │Pricing │ │
│  │  Collector   │  │  Researcher  │  │   Brief Gen  │  │Analyzer│ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────┘ │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     Data Layer                              │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐            │   │
│  │  │ Competitor  │  │ Intelligence│  │  Trend     │            │   │
│  │  │   Store     │  │    Store    │  │   Store    │            │   │
│  │  └────────────┘  └────────────┘  └────────────┘            │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills

# Install dependencies
pip install -r requirements.txt
```

### Basic Setup

```python
from agents.competitive_intel.agent import CompetitiveIntelAgent

# Initialize with default configuration
agent = CompetitiveIntelAgent()

# Or with custom configuration
config = {
    "user": "analyst",
    "default_competitor_type": "direct",
    "trend_min_data_points": 5,
    "benchmark_threshold": 0.5,
}
agent = CompetitiveIntelAgent(config)
```

### First Analysis

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

### Running the CLI

```bash
# Start interactive mode
python agents/competitive-intel/agent.py

# Run specific analysis
python agents/competitive-intel/agent.py --competitor "TechCorp" --analyze

# Generate strategic brief
python agents/competitive-intel/agent.py --brief

# Export data
python agents/competitive-intel/agent.py --export json --output report.json
```

---

## Usage

### Competitor Tracking

```python
# Add competitors with detailed profiles
agent.add_competitor(
    name="InnovateTech",
    competitor_type="direct",
    website="https://innovatetech.com",
    employee_count=500,
    annual_revenue=50000000,
    products=["AI Platform", "Analytics Suite"],
    strengths=["Cutting-edge AI", "Developer community", "Strong brand"],
    weaknesses=["Limited enterprise sales", "No mobile offering"],
    threat_level="medium",
)

# Analyze a competitor
analysis = agent.analyze_competitor(comp["competitor_id"])
print(f"Positioning: {analysis['competitive_positioning']['position']}")
print(f"Threat Score: {analysis['threat_assessment']['threat_score']}")

# List all competitors
competitors = agent.list_competitors()
for comp in competitors:
    print(f"{comp['name']}: {comp['threat_level']} threat")
```

### SWOT Analysis

```python
# Perform SWOT analysis
swot = agent.perform_swot(
    subject="Our Product",
    strengths=["Best-in-class UX", "Fast performance", "Strong API"],
    weaknesses=["Limited integrations", "No mobile app", "Small team"],
    opportunities=["Enterprise adoption", "International expansion", "AI features"],
    threats=["Price competition", "Regulatory changes", "New entrants"],
)

print(f"Score: {swot['overall_score']}")
print(f"Priority: {swot['strategic_priority']}")

# Compare SWOT analyses
comparison = agent._swot_analyzer.compare_swot([swot1_id, swot2_id])
```

### Trend Monitoring

```python
# Add data points for trend detection
for _ in range(10):
    agent._trend_monitor.add_data_point(
        "AI Adoption", "news", "AI spending increases in enterprise", "positive"
    )

# Detect trends
trends = agent.monitor_trends(topics=["AI Adoption"])
for trend in trends["trends"]:
    print(f"{trend['name']}: {trend['direction']} (impact: {trend['impact_score']})")

# Get trend summary
summary = agent._trend_monitor.get_trend_summary()
print(f"Total topics tracked: {summary['total_topics']}")
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
print(f"Score: {rankings['competitive_score']['score']}")
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
    key_findings=["Targets enterprise", "Premium pricing", "Q2 launch date"],
)

# Search intelligence
results = agent.search_intelligence(competitor="TechCorp")
print(f"Found {len(results)} reports")

# Get latest intelligence
latest = agent._intel_collector.get_latest(limit=10)
```

### Market Research

```python
# Conduct market research
landscape = agent.conduct_market_research(
    market="Cloud Computing",
    segment="enterprise",
    competitors=[comp1_id, comp2_id],
)

print(f"Market size: ${landscape['market_size']}")
print(f"Competitors: {landscape['competitor_count']}")
print(f"Growth rate: {landscape['growth_rate']}%")
```

### Strategic Brief

```python
# Generate executive strategic brief
brief = agent.generate_strategic_brief()

print(f"Competitors tracked: {brief['executive_summary']['competitors_tracked']}")
print(f"Active trends: {brief['executive_summary']['active_trends']}")
print(f"\nRecommendations:")
for rec in brief["key_recommendations"]:
    print(f"  - {rec}")
```

### Competitive Landscape Overview

```python
# Get high-level competitive landscape
landscape = agent.get_competitive_landscape()

print(f"Total competitors: {landscape['total_competitors']}")
print(f"Direct competitors: {landscape['direct_competitors']}")
print(f"Average threat level: {landscape['average_threat']}")
```

### Pricing Analysis

```python
# Analyze pricing position
pricing = agent._pricing_analyzer.analyze_pricing(
    product_name="Pro Plan",
    our_price=99,
    competitor_prices={
        "TechCorp": 129,
        "InnovateTech": 79,
        "MarketLeader": 149,
    }
)

print(f"Position: {pricing['position']}")
print(f"Average competitor price: ${pricing['average_competitor']}")
```

### Feature Comparison

```python
# Compare features across competitors
comparison = agent._benchmark_engine.compare_features(
    product_name="Our Platform",
    features=["API Access", "SSO", "Analytics", "Custom Reports"],
    competitors={
        "TechCorp": [True, True, True, False],
        "InnovateTech": [True, False, True, True],
        "MarketLeader": [True, True, True, True],
    }
)

print(f"Feature parity: {comparison['feature_parity_score']}")
print(f"Unique features: {comparison['unique_features']}")
```

---

## API Reference

### CompetitiveIntelAgent

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `add_competitor()` | `name: str, competitor_type: str, website: str, employee_count: int, annual_revenue: float, products: list, strengths: list, weaknesses: list, threat_level: str` | `Competitor dict` | Add a new competitor profile |
| `analyze_competitor()` | `competitor_id: str, additional_data: dict` | `Analysis dict` | Perform deep analysis on a competitor |
| `conduct_market_research()` | `market: str, segment: str, competitors: list` | `Landscape dict` | Conduct market research analysis |
| `perform_swot()` | `subject: str, strengths: list, weaknesses: list, opportunities: list, threats: list` | `SWOT dict` | Perform SWOT analysis |
| `monitor_trends()` | `topics: list` | `Trends dict` | Detect trends in monitored topics |
| `add_intelligence()` | `title: str, summary: str, source: str, competitor_name: str, category: str, key_findings: list` | `Report dict` | Add intelligence report |
| `search_intelligence()` | `keyword: str, competitor: str, category: str` | `List of reports` | Search intelligence database |
| `add_benchmark_metric()` | `category: str, metric_name: str, our_value: float, competitor_values: dict, industry_average: float, unit: str, higher_is_better: bool` | `Metric dict` | Add benchmark metric |
| `get_benchmark_rankings()` | `category: str` | `Rankings dict` | Get rankings for a category |
| `generate_strategic_brief()` | `—` | `Brief dict` | Generate executive strategic brief |
| `get_competitive_landscape()` | `—` | `Landscape overview dict` | Get high-level landscape overview |
| `list_competitors()` | `—` | `List of competitor dicts` | List all tracked competitors |
| `get_status()` | `—` | `Agent status dict` | Get agent operational status |

### CompetitorProfiler

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `create_profile()` | `name, type, website, employees, revenue, products, strengths, weaknesses, threat_level` | `Profile dict` | Create detailed competitor profile |
| `update_profile()` | `competitor_id, updates: dict` | `Updated profile` | Update existing competitor data |
| `get_profile()` | `competitor_id: str` | `Profile dict` | Retrieve full competitor profile |
| `assess_threat()` | `competitor_id: str` | `Threat assessment` | Calculate threat score |

### SWOTAnalyzer

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `analyze()` | `subject: str, strengths: list, weaknesses: list, opportunities: list, threats: list` | `SWOT analysis` | Perform complete SWOT analysis |
| `compare_swot()` | `analysis_ids: list` | `Comparison dict` | Compare multiple SWOT analyses |
| `get_strategic_recommendations()` | `analysis_id: str` | `SO/WO/ST/WT strategies` | Generate strategic recommendations |

### TrendMonitor

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `add_data_point()` | `topic: str, source: str, content: str, sentiment: str` | `None` | Add data point for trend analysis |
| `detect_trends()` | `topics: list, min_data_points: int` | `List of trends` | Detect trends across topics |
| `get_trend_summary()` | `—` | `Summary dict` | Get summary of all tracked trends |

### BenchmarkEngine

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `add_metric()` | `category: str, metric_name: str, our_value: float, competitor_values: dict, industry_average: float, unit: str, higher_is_better: bool` | `Metric` | Add benchmark metric |
| `get_rankings()` | `category: str` | `Rankings list` | Get rankings for category |
| `competitive_score()` | `category: str` | `Score and position` | Calculate competitive score |
| `compare_features()` | `product_name: str, features: list, competitors: dict` | `Feature comparison` | Compare feature sets |
| `analyze_pricing()` | `product_name: str, our_price: float, competitor_prices: dict` | `Pricing analysis` | Analyze pricing position |

### IntelligenceCollector

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `collect()` | `title: str, summary: str, source: str, competitor_name: str, category: str, key_findings: list` | `Report` | Collect new intelligence |
| `search()` | `keyword: str, competitor: str, category: str, source: str, limit: int` | `List of reports` | Search collected intelligence |
| `get_latest()` | `competitor: str, limit: int` | `Latest reports` | Get most recent intelligence |
| `get_stats()` | `—` | `Collection statistics` | Get collection statistics |

### PricingAnalyzer

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `analyze_pricing()` | `product_name: str, our_price: float, competitor_prices: dict` | `Pricing analysis` | Analyze competitive pricing |
| `recommend_position()` | `product_name: str, market_data: dict` | `Position recommendation` | Recommend pricing position |

### MarketResearcher

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `analyze_market()` | `market: str, segment: str, competitors: list` | `Market analysis` | Analyze market landscape |
| `estimate_size()` | `market: str, methodology: str` | `Size estimate` | Estimate market size |

---

## Data Models

### CompetitorProfile

```python
{
    "competitor_id": "uuid",
    "name": "TechCorp",
    "competitor_type": "direct",  # direct | indirect | potential
    "website": "https://techcorp.com",
    "employee_count": 1200,
    "annual_revenue": 150000000,
    "products": ["Platform", "API", "Analytics"],
    "technologies": ["Python", "React", "AWS"],
    "strengths": ["Strong brand", "Enterprise relationships"],
    "weaknesses": ["Legacy architecture", "Slow innovation"],
    "threat_level": "high",  # low | medium | high | critical
    "threat_score": 85.5,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-06-20T14:45:00Z"
}
```

### MarketTrend

```python
{
    "trend_id": "uuid",
    "topic": "AI Adoption",
    "direction": "increasing",  # increasing | decreasing | stable | volatile
    "impact_score": 78.5,
    "confidence": 0.85,
    "data_points": [
        {"timestamp": "2024-01-01", "sentiment": "positive", "source": "news"},
        {"timestamp": "2024-01-15", "sentiment": "positive", "source": "report"}
    ],
    "drivers": ["Enterprise AI spending", "Cloud migration"],
    "first_detected": "2024-01-01T00:00:00Z",
    "last_updated": "2024-06-20T14:45:00Z"
}
```

### SWOTAnalysis

```python
{
    "analysis_id": "uuid",
    "subject": "Our Company",
    "strengths": ["Best UX", "Fast performance"],
    "weaknesses": ["Limited integrations"],
    "opportunities": ["Enterprise market"],
    "threats": ["Price competition"],
    "internal_score": 72.5,
    "external_score": 65.0,
    "overall_score": 68.75,
    "strategic_priority": "SO",  # SO | WO | ST | WT
    "created_at": "2024-01-15T10:30:00Z"
}
```

### BenchmarkMetric

```python
{
    "metric_id": "uuid",
    "category": "product",
    "metric_name": "API Response Time",
    "our_value": 45,
    "competitor_values": {"TechCorp": 60, "InnovateTech": 80},
    "industry_average": 75,
    "unit": "ms",
    "higher_is_better": False,
    "ranking": 1,
    "competitive_score": 92.5,
    "created_at": "2024-01-15T10:30:00Z"
}
```

### IntelReport

```python
{
    "report_id": "uuid",
    "title": "TechCorp announces new product",
    "summary": "Major product launch targeting enterprise",
    "source": "news_article",
    "competitor_name": "TechCorp",
    "category": "product_launch",
    "key_findings": ["Enterprise focus", "Premium pricing"],
    "confidence": 0.85,
    "strategic_implications": ["Need to accelerate enterprise roadmap"],
    "collected_at": "2024-06-20T14:45:00Z"
}
```

### StrategicBrief

```python
{
    "brief_id": "uuid",
    "executive_summary": {
        "competitors_tracked": 5,
        "active_trends": 8,
        "recent_intelligence": 12,
        "average_threat_level": "medium"
    },
    "key_recommendations": [
        "Accelerate enterprise features",
        "Monitor pricing changes",
        "Invest in AI capabilities"
    ],
    "threat_overview": {...},
    "trend_highlights": [...],
    "generated_at": "2024-06-20T14:45:00Z"
}
```

### PricingModel

```python
{
    "product_name": "Pro Plan",
    "our_price": 99,
    "competitor_prices": {
        "TechCorp": 129,
        "InnovateTech": 79,
        "MarketLeader": 149
    },
    "average_competitor": 119,
    "position": "below_average",  # premium | average | below_average | budget
    "price_advantage": 20.0,  # percentage below average
    "analyzed_at": "2024-06-20T14:45:00Z"
}
```

---

## Intelligence Sources

| Source | Reliability | Best For | Update Frequency |
|--------|-------------|----------|------------------|
| News Articles | Moderate | Recent events, product launches | Real-time |
| Earnings Calls | High | Financial performance, strategy | Quarterly |
| Patent Filings | High | Technology direction, innovation | Monthly |
| Job Postings | Moderate | Hiring priorities, skill gaps | Weekly |
| Customer Reviews | Moderate | Product feedback, satisfaction | Weekly |
| Industry Reports | High | Market sizing, trends | Quarterly |
| GitHub | High | Tech stack, development activity | Daily |
| Crunchbase | High | Funding, growth metrics | Monthly |
| LinkedIn | Moderate | Team changes, hiring signals | Daily |
| Glassdoor | Low-Moderate | Culture, employee satisfaction | Monthly |
| SEC Filings | High | Financial health, strategy | Quarterly |
| Social Media | Low-Moderate | Brand sentiment, announcements | Real-time |

---

## Intelligence Gathering Techniques

### Primary Research

1. **Competitive Product Analysis** — Purchase and evaluate competitor products directly. Document features, pricing, UX, and performance. Create comparison matrices.

2. **Customer Interviews** — Interview customers who switched from competitors. Understand their decision criteria, pain points, and what would make them switch back.

3. **Industry Expert Conversations** — Speak with industry analysts, consultants, and thought leaders. They often have insights not available in public sources.

4. **Trade Show Intelligence** — Attend industry events to observe competitor presentations, booth presence, and product demonstrations.

### Secondary Research

1. **SEC Filing Analysis** — Review 10-K, 10-Q, and 8-K filings for financial metrics, strategic initiatives, and risk disclosures.

2. **Patent Monitoring** — Track competitor patent applications to anticipate technology direction and innovation priorities.

3. **Job Posting Analysis** — Analyze competitor job listings to identify hiring priorities, technology choices, and strategic initiatives.

4. **Social Listening** — Monitor social media for competitor announcements, customer sentiment, and market trends.

### Digital Intelligence

1. **Website Monitoring** — Track changes to competitor websites for product updates, pricing changes, and messaging shifts.

2. **SEO Analysis** — Analyze competitor search rankings, keyword strategies, and content marketing efforts.

3. **Technology Stack Detection** — Use tools like BuiltWith or Wappalyzer to identify competitor technology choices.

4. **Traffic Analytics** — Estimate competitor website traffic using SimilarWeb or Alexa data.

---

## Configuration

### Core Settings

```python
config = {
    "user": "analyst",                    # Analyst identifier
    "default_competitor_type": "direct",  # direct | indirect | potential
    "trend_min_data_points": 5,           # Minimum points for trend detection
    "benchmark_threshold": 0.5,           # Minimum score threshold
}
agent = CompetitiveIntelAgent(config)
```

### Advanced Settings

```python
config = {
    # Core
    "user": "analyst",
    "default_competitor_type": "direct",
    
    # Trend Detection
    "trend_min_data_points": 5,
    "trend_sensitivity": 0.7,         # 0.0-1.0, higher = more sensitive
    "trend_decay_factor": 0.95,       # Exponential decay for older data
    
    # Benchmarking
    "benchmark_threshold": 0.5,
    "benchmark_weight_defaults": {     # Default weights for scoring
        "market_share": 0.25,
        "revenue": 0.20,
        "innovation": 0.20,
        "customer_satisfaction": 0.15,
        "brand_strength": 0.10,
        "operational_efficiency": 0.10
    },
    
    # Intelligence
    "intel_retention_days": 365,       # How long to keep intelligence
    "intel_confidence_threshold": 0.6, # Minimum confidence for reports
    "intel_max_sources": 10,           # Max sources per report
    
    # Output
    "export_format": "json",           # json | csv | markdown
    "report_language": "en",           # Report language
    
    # Storage
    "storage_backend": "memory",       # memory | sqlite | postgresql
    "storage_path": "./data",          # Path for file-based storage
}
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `COMPETITIVE_INTEL_USER` | Default analyst user | `analyst` |
| `COMPETITIVE_INTEL_STORAGE` | Storage backend | `memory` |
| `COMPETITIVE_INTEL_LOG_LEVEL` | Logging level | `INFO` |
| `COMPETITIVE_INTEL_EXPORT_DIR` | Export directory | `./exports` |

---

## Examples

### Startup Competitive Analysis

A complete competitive analysis workflow for a startup entering a new market.

```python
from agents.competitive_intel.agent import CompetitiveIntelAgent

# Initialize
agent = CompetitiveIntelAgent()

# Define competitors
competitors = [
    {
        "name": "EstablishedPlayer Inc",
        "competitor_type": "direct",
        "employee_count": 5000,
        "annual_revenue": 500000000,
        "products": ["Enterprise Suite", "API Platform"],
        "strengths": ["Market leader", "Strong brand", "Enterprise relationships"],
        "weaknesses": ["Legacy tech", "Slow innovation", "High prices"],
        "threat_level": "high",
    },
    {
        "name": "FastGrowth Startup",
        "competitor_type": "direct",
        "employee_count": 100,
        "annual_revenue": 10000000,
        "products": ["Modern Platform"],
        "strengths": ["Fast innovation", "Developer-friendly", "Low prices"],
        "weaknesses": ["Limited features", "No enterprise support"],
        "threat_level": "medium",
    },
]

# Add competitors
for comp in competitors:
    agent.add_competitor(**comp)

# Analyze each
for comp in agent.list_competitors():
    analysis = agent.analyze_competitor(comp["competitor_id"])
    print(f"\n{comp['name']}:")
    print(f"  Threat Score: {analysis['threat_assessment']['threat_score']}")
    print(f"  Position: {analysis['competitive_positioning']['position']}")

# SWOT for our startup
swot = agent.perform_swot(
    subject="Our Startup",
    strengths=["Modern tech stack", "Agile development", "Low overhead"],
    weaknesses=["No brand recognition", "Limited funding", "Small team"],
    opportunities=["Underserved mid-market", "API-first demand", "Remote work trend"],
    threats=["Established player response", "Funding drought", "Talent competition"],
)

print(f"\nSWOT Score: {swot['overall_score']}")
print(f"Strategic Priority: {swot['strategic_priority']}")

# Generate strategic brief
brief = agent.generate_strategic_brief()
print("\nStrategic Brief:")
for rec in brief["key_recommendations"]:
    print(f"  - {rec}")
```

### Enterprise Market Monitoring

Continuous monitoring of competitive landscape for an enterprise.

```python
from agents.competitive_intel.agent import CompetitiveIntelAgent

agent = CompetitiveIntelAgent({
    "trend_min_data_points": 3,
    "intel_confidence_threshold": 0.7,
})

# Track market trends
topics = ["Cloud Migration", "AI Adoption", "Remote Work", "Cybersecurity"]

# Simulate data collection over time
import random

for topic in topics:
    for _ in range(15):
        sentiment = random.choice(["positive", "neutral", "negative"])
        agent._trend_monitor.add_data_point(
            topic=topic,
            source=random.choice(["news", "report", "social"]),
            content=f"{topic} trend data point",
            sentiment=sentiment
        )

# Detect trends
trends = agent.monitor_trends(topics=topics)
print("Detected Trends:")
for trend in trends["trends"]:
    print(f"  {trend['name']}: {trend['direction']} "
          f"(impact: {trend['impact_score']:.1f}, "
          f"confidence: {trend['confidence']:.2f})")

# Collect intelligence
agent.add_intelligence(
    title="Major competitor announces AI-first strategy",
    summary="EstablishedPlayer shifts entire product line to AI",
    source="earnings_call",
    competitor_name="EstablishedPlayer Inc",
    category="strategic_shift",
    key_findings=["Full AI integration", "Increased R&D spend", "New partnerships"],
)

# Generate report
brief = agent.generate_strategic_brief()
print(f"\nMarket Intelligence:")
print(f"  Trends tracked: {brief['executive_summary']['active_trends']}")
print(f"  Intelligence items: {brief['executive_summary']['recent_intelligence']}")
```

### Product Launch Intelligence

Intelligence gathering around a competitor's product launch.

```python
from agents.competitive_intel.agent import CompetitiveIntelAgent

agent = CompetitiveIntelAgent()

# Add competitor launching product
comp = agent.add_competitor(
    name="InnovateTech",
    competitor_type="direct",
    products=["Existing Platform"],
    threat_level="medium",
)

# Collect launch intelligence
agent.add_intelligence(
    title="InnovateTech announces Product X launch",
    summary="New AI-powered analytics platform",
    source="press_release",
    competitor_name="InnovateTech",
    category="product_launch",
    key_findings=["AI-native architecture", "Real-time analytics", "API marketplace"],
    confidence=0.9,
)

agent.add_intelligence(
    title="InnovateTech pricing revealed",
    summary="Pricing starts at $99/mo for teams",
    source="blog_post",
    competitor_name="InnovateTech",
    category="pricing",
    key_findings=["Competitive pricing", "Freemium tier", "Enterprise discount"],
    confidence=0.85,
)

# Benchmark against launch
agent.add_benchmark_metric(
    category="product_features",
    metric_name="AI Capabilities",
    our_value=60,
    competitor_values={"InnovateTech": 85},
    industry_average=50,
    higher_is_better=True,
)

agent.add_benchmark_metric(
    category="product_features",
    metric_name="Pricing Competitiveness",
    our_value=75,
    competitor_values={"InnovateTech": 80},
    industry_average=70,
    higher_is_better=True,
)

# Analyze competitive impact
analysis = agent.analyze_competitor(comp["competitor_id"])
print(f"Post-Launch Threat Level: {analysis['threat_assessment']['threat_level']}")
print(f"Threat Score: {analysis['threat_assessment']['threat_score']}")

# Get strategic recommendations
swot = agent.perform_swot(
    subject="Our Response to Launch",
    strengths=["Established customer base", "Proven reliability"],
    weaknesses=["Slower AI development", "Legacy architecture"],
    opportunities=["Differentiate on support", "Acquire disappointed customers"],
    threats=["Market share loss", "Price war"],
)

print(f"\nStrategic Priority: {swot['strategic_priority']}")
```

### Pricing Strategy Optimization

Optimize pricing based on competitive intelligence.

```python
from agents.competitive_intel.agent import CompetitiveIntelAgent

agent = CompetitiveIntelAgent()

# Analyze pricing landscape
pricing_analysis = agent._pricing_analyzer.analyze_pricing(
    product_name="Pro Plan",
    our_price=99,
    competitor_prices={
        "MarketLeader": 149,
        "BudgetOption": 49,
        "PremiumProvider": 199,
        "MidRange": 89,
    }
)

print("Pricing Analysis:")
print(f"  Our Price: ${pricing_analysis['our_price']}")
print(f"  Market Average: ${pricing_analysis['average_competitor']}")
print(f"  Position: {pricing_analysis['position']}")
print(f"  Price Advantage: {pricing_analysis['price_advantage']:.1f}%")

# Add pricing benchmarks
agent.add_benchmark_metric(
    category="pricing",
    metric_name="Monthly Subscription",
    our_value=99,
    competitor_values={
        "MarketLeader": 149,
        "BudgetOption": 49,
        "PremiumProvider": 199,
    },
    industry_average=120,
    unit="USD",
    higher_is_better=False,  # Lower price is better for customers
)

# Get positioning recommendations
recommendation = agent._pricing_analyzer.recommend_position(
    product_name="Pro Plan",
    market_data={
        "market_growth": 0.15,
        "price_sensitivity": 0.7,
        "switching_cost": 0.3,
    }
)

print(f"\nRecommendation: {recommendation['position']}")
print(f"Rationale: {recommendation['rationale']}")
```

### Competitive Threat Assessment

Deep threat assessment of a specific competitor.

```python
from agents.competitive_intel.agent import CompetitiveIntelAgent

agent = CompetitiveIntelAgent()

# Add competitor
comp = agent.add_competitor(
    name="ThreatCorp",
    competitor_type="direct",
    employee_count=2000,
    annual_revenue=100000000,
    products=["Platform A", "Platform B", "API Service"],
    strengths=["Aggressive pricing", "Fast growth", "Strong VC backing"],
    weaknesses=["Customer support issues", "Limited enterprise features"],
    threat_level="high",
)

# Collect threat intelligence
threat_intel = [
    ("ThreatCorp raises $200M Series D", "funding", 0.9),
    ("ThreatCorp acquires analytics startup", "acquisition", 0.85),
    ("ThreatCorp launches enterprise tier", "product_launch", 0.8),
    ("ThreatCorp expands to European market", "expansion", 0.75),
]

for title, category, confidence in threat_intel:
    agent.add_intelligence(
        title=title,
        summary=f"Strategic move by ThreatCorp: {category}",
        source="news_article",
        competitor_name="ThreatCorp",
        category=category,
        key_findings=[f"Category: {category}", f"Impact: High"],
        confidence=confidence,
    )

# Analyze threat
analysis = agent.analyze_competitor(comp["competitor_id"])

print("Threat Assessment:")
print(f"  Threat Level: {analysis['threat_assessment']['threat_level']}")
print(f"  Threat Score: {analysis['threat_assessment']['threat_score']}")
print(f"  Positioning: {analysis['competitive_positioning']['position']}")

# Monitor threat trends
agent._trend_monitor.add_data_point("ThreatCorp Growth", "funding", 
    "Series D: $200M raised", "positive")
agent._trend_monitor.add_data_point("ThreatCorp Growth", "hiring", 
    "500 new positions posted", "positive")
agent._trend_monitor.add_data_point("ThreatCorp Growth", "product", 
    "Enterprise tier launched", "positive")

trends = agent.monitor_trends(topics=["ThreatCorp Growth"])
for trend in trends["trends"]:
    print(f"\nThreat Trend: {trend['direction']}")
    print(f"  Impact Score: {trend['impact_score']:.1f}")
    print(f"  Confidence: {trend['confidence']:.2f}")
```

---

## Best Practices

1. **Diversify Sources** — Don't rely on a single intelligence source. Cross-reference news with SEC filings, customer reviews, and analyst reports to build a complete picture.

2. **Verify Before Acting** — Always cross-reference findings across multiple sources before making strategic decisions. Single-source intelligence can be misleading.

3. **Keep Data Fresh** — Stale intelligence leads to stale strategy. Establish regular collection cadences based on source update frequency.

4. **Track Emerging Competitors** — Don't focus only on established players. Monitor startups and adjacent market entrants who could disrupt the landscape.

5. **Quantify Where Possible** — Metrics beat anecdotes for strategic decisions. Convert qualitative observations into quantified scores when possible.

6. **Act on Insights** — Intelligence without action is trivia. Every intelligence report should have clear strategic implications and recommended actions.

7. **Document Assumptions** — Track what you assumed vs what you verified. This prevents overconfidence in weakly-supported conclusions.

8. **Regular Review** — Schedule periodic competitive landscape reviews (monthly or quarterly) to ensure intelligence remains current and relevant.

9. **Maintain Objectivity** — Avoid confirmation bias. Actively seek disconfirming evidence for your strategic hypotheses.

10. **Respect Legal Boundaries** — Only gather intelligence from public and ethical sources. Avoid misrepresentation, hacking, or other illegal activities.

11. **Automate Collection** — Set up automated monitoring for critical intelligence sources to reduce manual effort and capture real-time changes.

12. **Context Matters** — Always consider the context behind competitor actions. A price cut could signal growth strategy or desperation depending on other signals.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| SWOT analysis too generic | Add more company-specific data points with concrete examples and metrics |
| Trend detection inaccurate | Increase minimum data point threshold or adjust sensitivity settings |
| Benchmark rankings outdated | Refresh competitor metrics by re-collecting latest data |
| Intelligence reports conflicting | Check confidence levels, prefer verified sources over unverified |
| Strategic brief lacks depth | Increase intelligence collection volume and diversify sources |
| Competitor profile incomplete | Fill in missing fields with latest intelligence reports |
| Trend direction fluctuating | Increase decay factor to reduce noise from older data points |
| Low confidence scores | Improve source diversity and cross-reference findings |
| No trends detected | Lower minimum data points threshold or increase data collection |
| Benchmark scores not updating | Verify metric values are being properly recorded |
| Export fails | Check file permissions and available disk space |
| Search returns no results | Verify data has been collected and search terms match content |
| Analysis seems biased | Add more competitor data to balance perspectives |
| High memory usage | Reduce data retention period or implement data archival |

---

## FAQ

**Q: How often should I update competitor profiles?**
A: Update profiles whenever significant intelligence is collected. For active competitors, aim for monthly reviews. For critical competitors, consider weekly updates.

**Q: Can I track indirect competitors?**
A: Yes, use the `competitor_type="indirect"` parameter. Indirect competitors are tracked separately but included in market landscape analysis.

**Q: How does trend detection handle contradictory signals?**
A: The trend monitor uses sentiment aggregation with configurable decay. Mixed signals typically result in a "stable" trend direction with lower confidence scores.

**Q: Is there a limit to how many competitors I can track?**
A: The agent supports unlimited competitors in memory mode. For production use with SQLite or PostgreSQL backends, performance scales well to hundreds of competitors.

**Q: Can I export data for external analysis?**
A: Yes, use the export functionality with formats: JSON, CSV, or Markdown. All data models are serializable.

**Q: How do I improve intelligence confidence scores?**
A: Cross-reference multiple sources, prefer primary sources over secondary, and verify key findings independently.

**Q: Can the agent integrate with external data sources?**
A: Yes, through the plugin architecture. See [Extending the Agent](#extending-the-agent) for custom source implementations.

**Q: What's the difference between threat_level and threat_score?**
A: `threat_level` is a categorical label (low/medium/high/critical). `threat_score` is a numeric value (0-100) for precise comparisons.

**Q: How do I handle competitors that span multiple markets?**
A: Create separate profiles for each market segment, or use the `competitor_type` field to distinguish market-specific competition.

**Q: Can I schedule automated intelligence collection?**
A: The agent provides collection methods that can be integrated with task schedulers (cron, Airflow, Celery) for automated workflows.

---

## Extending the Agent

### Adding New Analytical Frameworks

```python
# Example: Adding PESTEL Analysis

class PESTELAnalyzer:
    def __init__(self):
        self.factors = {
            "political": [],
            "economic": [],
            "social": [],
            "technological": [],
            "environmental": [],
            "legal": []
        }
    
    def analyze(self, subject, factors_by_category):
        """Perform PESTEL analysis."""
        for category, factors in factors_by_category.items():
            self.factors[category] = factors
        
        return {
            "subject": subject,
            "factors": self.factors,
            "risk_score": self._calculate_risk_score(),
            "opportunities": self._identify_opportunities()
        }
    
    def _calculate_risk_score(self):
        # Calculate overall risk from factors
        pass
    
    def _identify_opportunities(self):
        # Identify opportunities from PESTEL factors
        pass

# Register with agent
agent._pestel_analyzer = PESTELAnalyzer()
```

### Custom Intelligence Sources

```python
# Example: Custom news source handler

class CustomNewsHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.source_name = "custom_news"
    
    def fetch(self, query, limit=10):
        """Fetch news from custom source."""
        # Implementation specific to your news API
        pass
    
    def parse(self, raw_data):
        """Parse news into IntelReport format."""
        return [
            {
                "title": item["headline"],
                "summary": item["summary"],
                "source": self.source_name,
                "confidence": 0.8,
                "category": self._categorize(item)
            }
            for item in raw_data
        ]

# Register handler
agent._intel_collector.register_source("custom_news", CustomNewsHandler(api_key))
```

### Plugin Architecture

```python
# Example: Creating a plugin

class CompetitorAlertPlugin:
    def __init__(self, agent):
        self.agent = agent
        self.alerts = []
    
    def on_competitor_update(self, competitor_id, changes):
        """Called when competitor data changes."""
        if changes.get("threat_level") == "critical":
            self._send_alert(f"Critical threat detected: {competitor_id}")
    
    def on_intelligence_collected(self, report):
        """Called when new intelligence is collected."""
        if report.get("confidence", 0) > 0.9:
            self._send_alert(f"High-confidence intel: {report['title']}")
    
    def _send_alert(self, message):
        # Implement alert notification
        self.alerts.append({"message": message, "timestamp": datetime.now()})

# Register plugin
plugin = CompetitorAlertPlugin(agent)
agent.register_plugin(plugin)
```

---

## Contributing

1. Add new intelligence source handlers
2. Enhance trend detection algorithms
3. Add new analytical frameworks (Porter, PESTEL, Value Chain)
4. Improve benchmark metric calculations
5. Update documentation for API changes
6. Write tests for new features
7. Improve export formats and visualization

---

## Files

- `agent.py` — Main implementation (~900 lines)
- `ARCHITECTURE.md` — System architecture with diagrams
- `GROK.md` — Agent instructions and identity
- `README.md` — This file
- `plugins/` — Plugin directory for extensions
- `tests/` — Test suite
- `examples/` — Usage examples

---

## License

Part of the Awesome Grok Skills collection. See project root for license details.
