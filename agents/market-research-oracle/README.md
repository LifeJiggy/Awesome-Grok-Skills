# Market Research Oracle Agent

Comprehensive market research, survey design, data collection, trend analysis, competitive landscape mapping, and forecasting.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

The Market Research Oracle provides a complete research intelligence platform combining survey design, multi-source data collection, sentiment analysis, trend detection, competitive landscape mapping, statistical forecasting, and market sizing into a unified system.

### Key Capabilities

| Capability | Description |
|-----------|-------------|
| Survey Builder | Design, distribute, and analyze surveys |
| Data Collection | Multi-source aggregation with reliability weighting |
| Sentiment Analysis | Cross-source sentiment scoring and classification |
| Trend Detection | Statistical trend identification from time-series data |
| Competitive Landscape | SWOT analysis, threat assessment, market mapping |
| Forecasting | Moving average, exponential smoothing, linear regression |
| Market Sizing | TAM/SAM/SOM estimation with forward projection |

---

## Features

### Survey System
- 8 question types: rating, NPS, multiple choice, ranking, likert, binary, open-ended, demographic
- Per-question analytics (mean, distribution, NPS score)
- Response tracking with completion rates
- Configurable target response counts

### Data Collection
- Support for 10 data source types
- Reliability-weighted aggregation
- Cross-source sentiment fusion
- Source statistics and metadata

### Trend Analysis
- Linear regression slope analysis
- Automatic trend classification (growth, emerging, maturing, declining)
- Volatility-adjusted confidence scoring
- Time-series data point management

### Competitive Intelligence
- Competitor profiling with market share
- Position classification (leader, challenger, follower, niche, emerging)
- SWOT generation with automated opportunity/threat identification
- Threat level scoring (0-5 scale)

### Forecasting
- Moving average with configurable window
- Exponential smoothing with alpha parameter
- Linear regression with OLS fitting
- Confidence intervals and accuracy scoring

### Market Sizing
- TAM/SAM/SOM framework
- Forward projection with compound growth
- Segment-specific estimates

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│        MarketResearchOracle (Facade)             │
├─────────────────────────────────────────────────┤
│  SurveyBuilder      │  DataCollector            │
│  TrendAnalyzer      │  CompetitiveLandscape     │
│  ForecastEngine     │  MarketSizeEstimator      │
│  ReportGenerator                             │
└─────────────────────────────────────────────────┘
```

---

## Quick Start

### Installation

```bash
pip install awesome-grok-skills
```

### Minimal Example

```python
from agents.market_research_oracle.agent import MarketResearchOracle

oracle = MarketResearchOracle()

# Estimate market
size = oracle.market_size.estimate("SaaS", 50_000_000_000, 0.3, 0.1)
print(f"Market: TAM=${size.tam:,.0f}")

# Add competitors
oracle.competitive.add_competitor("AlphaCorp", 0.25, ["Brand"], ["Innovation"])

# Generate report
report = oracle.reports.generate_report(
    "Market Analysis",
    "Strong growth identified.",
    ["Growth 15%"],
    ["Invest in R&D"]
)
```

---

## Usage

### Running the Agent

```bash
python agents/market-research-oracle/agent.py
```

### Programmatic Access

```python
from agents.market_research_oracle.agent import MarketResearchOracle

oracle = MarketResearchOracle()

# Each component can be used independently
survey = oracle.surveys.create_survey("Feedback Survey")
oracle.trends.add_data_point("revenue", datetime.now(), 1000)
oracle.forecast.linear_regression("revenue", [800, 900, 1000])
```

---

## API Reference

### MarketResearchOracle

| Method | Description |
|--------|-------------|
| `full_research_cycle(topic, competitors, data)` | End-to-end research workflow |

### SurveyBuilder

| Method | Description |
|--------|-------------|
| `create_survey(title, desc, target)` | Create new survey |
| `add_question(survey_id, text, type, options)` | Add question |
| `submit_response(survey_id, respondent, answers)` | Record response |
| `analyze_survey(survey_id)` | Analyze all responses |
| `list_surveys()` | List all surveys |

### DataCollector

| Method | Description |
|--------|-------------|
| `register_source(name, type, reliability)` | Register data source |
| `collect(source, topic, data)` | Collect data records |
| `get_data(source, topic)` | Retrieve collected data |
| `aggregate_sentiment(topic)` | Cross-source sentiment |
| `get_source_stats()` | Source statistics |

### TrendAnalyzer

| Method | Description |
|--------|-------------|
| `add_data_point(metric, timestamp, value)` | Add time-series point |
| `detect_trends(metric)` | Detect trends |
| `get_trend_summary()` | Summary by type |
| `list_trends()` | All detected trends |

### CompetitiveLandscape

| Method | Description |
|--------|-------------|
| `add_competitor(name, share, strengths, weaknesses)` | Add competitor |
| `generate_swot(competitor_id)` | Generate SWOT |
| `competitive_matrix()` | Full competitive matrix |
| `get_threat_assessment()` | Threat scoring |
| `list_competitors()` | All competitors |

### ForecastEngine

| Method | Description |
|--------|-------------|
| `moving_average(metric, values, window)` | Moving average forecast |
| `exponential_smoothing(metric, values, alpha)` | Exponential smoothing |
| `linear_regression(metric, values)` | Linear regression |
| `get_forecast(metric)` | Retrieve forecast |
| `list_forecasts()` | All forecasts |

### MarketSizeEstimator

| Method | Description |
|--------|-------------|
| `estimate(segment, tam, sam_pct, som_pct, growth)` | Initial estimate |
| `project_forward(segment, years)` | Multi-year projection |
| `get_estimate(segment)` | Retrieve estimate |
| `list_estimates()` | All estimates |

### ReportGenerator

| Method | Description |
|--------|-------------|
| `generate_report(title, summary, findings, recs)` | Create report |
| `add_section(report_id, title, content)` | Add section |
| `get_report(report_id)` | Retrieve report |
| `list_reports()` | All reports |

---

## Examples

### Complete Market Research Cycle

```python
oracle = MarketResearchOracle()

# Collect data from multiple sources
oracle.data_collector.collect("twitter", "AI tools", [
    {"sentiment_score": 0.8, "keywords": ["AI", "automation"]},
    {"sentiment_score": 0.6, "keywords": ["AI", "productivity"]},
])

# Analyze sentiment
sentiment = oracle.data_collector.aggregate_sentiment("AI tools")
print(f"Sentiment: {sentiment.label.value} ({sentiment.score})")

# Detect trends
oracle.trends.add_data_point("ai_market", datetime(2025, 1, 1), 100)
oracle.trends.add_data_point("ai_market", datetime(2025, 6, 1), 180)
oracle.trends.add_data_point("ai_market", datetime(2025, 12, 1), 300)
trends = oracle.trends.detect_trends("ai_market")

# Size market
oracle.market_size.estimate("AI Tools", 30_000_000_000, 0.2, 0.05, 25)
```

### Competitive SWOT Analysis

```python
oracle = MarketResearchOracle()

oracle.competitive.add_competitor("LeaderCorp", 0.30, ["Brand", "Distribution"], ["High prices"])
oracle.competitive.add_competitor("ChallengerAI", 0.15, ["Innovation", "Price"], ["Scale"])

for comp in oracle.competitive.list_competitors():
    swot = oracle.competitive.generate_swot(comp.competitor_id)
    print(f"\n{swot['competitor']}:")
    print(f"  Strengths: {swot['strengths']}")
    print(f"  Threats: {swot['threats']}")
```

### Multi-Method Forecasting

```python
values = [100, 112, 125, 140, 158, 179]

oracle.forecast.moving_average("revenue", values, window=3)
oracle.forecast.exponential_smoothing("revenue", values, alpha=0.3)
oracle.forecast.linear_regression("revenue", values)

for f in oracle.forecast.list_forecasts():
    print(f"{f.method.value}: next={f.predicted_values[-1]:.1f}, accuracy={f.accuracy_score}")
```

---

## Configuration

### Data Source Reliability

| Source Type | Default Reliability |
|------------|-------------------|
| Government | 0.95 |
| Financial API | 0.92 |
| Proprietary | 0.90 |
| News | 0.85 |
| Social Media | 0.80 |
| Web Scrape | 0.70 |

### Trend Detection Thresholds

| Slope Range | Classification |
|------------|---------------|
| > 10% | GROWTH |
| 2-10% | EMERGING |
| -2% to 2% | MATURING |
| -10% to -2% | STABLE |
| < -10% | DECLINING |

---

## Best Practices

### Survey Design
- Keep surveys under 10 minutes completion time
- Mix question types for engagement
- Always include at least one NPS question
- Pilot test before full distribution
- Set realistic response targets

### Data Collection
- Register sources with accurate reliability scores
- Collect from at least 3 sources for cross-validation
- Track source freshness and update regularly
- Anonymize respondent data before analysis

### Trend Detection
- Use at least 5 data points for reliable detection
- Update data regularly (weekly minimum)
- Compare detected trends across multiple metrics
- Document external factors that may influence trends

### Competitive Analysis
- Update competitor profiles quarterly
- Monitor for new entrants regularly
- Track pricing changes and product launches
- Include indirect competitors in analysis

### Forecasting
- Validate model accuracy before relying on predictions
- Use multiple methods and compare results
- Document assumptions and limitations
- Update forecasts as new data arrives

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Survey analysis returns empty | No responses submitted | Collect responses first |
| Trend detection fails | Too few data points | Add at least 3 data points |
| Forecast accuracy is low | Outliers in data | Clean data, try different method |
| SWOT returns error | Invalid competitor ID | Use `list_competitors()` to get IDs |
| Market size seems wrong | Check percentage inputs | SAM% and SOM% should be < 1.0 |
| Sentiment is always neutral | Insufficient data volume | Collect more records |
| Competitor threat level wrong | Missing market share data | Provide accurate market_share values |

---

## License

MIT License - see [LICENSE](../../LICENSE) for details.
