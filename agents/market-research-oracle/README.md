# Market Research Oracle Agent

Comprehensive market research, survey design, data collection, trend analysis, competitive landscape mapping, and forecasting.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Contributing](#contributing)
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
| Report Generation | Structured research reports with findings and recommendations |

### System Requirements

- Python 3.10 or higher
- 512 MB RAM minimum
- 100 MB disk space
- Network access for external data sources (optional)

---

## Features

### Survey System
- 8 question types: rating, NPS, multiple choice, ranking, likert, binary, open-ended, demographic
- Per-question analytics (mean, distribution, NPS score)
- Response tracking with completion rates
- Configurable target response counts
- Survey templates for common research types
- Response validation and required field enforcement

### Data Collection
- Support for 10 data source types
- Reliability-weighted aggregation
- Cross-source sentiment fusion
- Source statistics and metadata
- Data cleaning and normalization
- Keyword extraction from text

### Trend Analysis
- Linear regression slope analysis
- Automatic trend classification (growth, emerging, maturing, declining)
- Volatility-adjusted confidence scoring
- Time-series data point management
- Multiple metric tracking
- Historical trend comparison

### Competitive Intelligence
- Competitor profiling with market share
- Position classification (leader, challenger, follower, niche, emerging)
- SWOT generation with automated opportunity/threat identification
- Threat level scoring (0-5 scale)
- Competitive matrix comparison
- Growth rate tracking

### Forecasting
- Moving average with configurable window
- Exponential smoothing with alpha parameter
- Linear regression with OLS fitting
- Confidence intervals and accuracy scoring
- Multiple method comparison
- Forecast persistence and retrieval

### Market Sizing
- TAM/SAM/SOM framework
- Forward projection with compound growth
- Segment-specific estimates
- Growth rate modeling
- Multi-year projections

### Report Generation
- Structured report format with sections
- Executive summary, findings, recommendations
- Data source documentation
- Report templates for common types
- Section-based assembly
- Timestamp and version tracking

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│        MarketResearchOracle (Facade)                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │ SurveyBuilder  │  │ DataCollector  │  │ TrendAnalyzer  │    │
│  │                │  │                │  │                │    │
│  │ Questions      │  │ Sources        │  │ Time Series    │    │
│  │ Responses      │  │ Sentiment      │  │ Regression     │    │
│  │ Analytics      │  │ Aggregation    │  │ Classification │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │CompetitiveLndsc│  │ ForecastEngine │  │MarketSizeEst.  │    │
│  │                │  │                │  │                │    │
│  │ SWOT           │  │ Moving Average │  │ TAM/SAM/SOM   │    │
│  │ Positioning    │  │ Exp. Smoothing │  │ Projection     │    │
│  │ Threat Score   │  │ Linear Regr.   │  │ Growth Model  │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
│                                                                  │
│  ┌────────────────┐                                             │
│  │ ReportGenerator│                                             │
│  │                │                                             │
│  │ Sections       │                                             │
│  │ Findings       │                                             │
│  │ Recommendations│                                             │
│  └────────────────┘                                             │
└─────────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

```
Research Request
     │
     ▼
MarketResearchOracle (facade)
     │
     ├──→ DataCollector.collect()
     │         │
     │         ▼
     │    Data Records
     │
     ├──→ DataCollector.aggregate_sentiment()
     │         │
     │         ▼
     │    Sentiment Result
     │
     ├──→ TrendAnalyzer.detect_trends()
     │         │
     │         ▼
     │    Trend Classifications
     │
     ├──→ CompetitiveLandscape.add_competitor()
     │         │
     │         ▼
     │    SWOT + Threat Scores
     │
     ├──→ ForecastEngine.linear_regression()
     │         │
     │         ▼
     │    Forecast Results
     │
     ├──→ MarketSizeEstimator.estimate()
     │         │
     │         ▼
     │    TAM/SAM/SOM
     │
     └──→ ReportGenerator.generate_report()
               │
               ▼
          Structured Report
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

# Estimate market size
size = oracle.market_size.estimate("SaaS", 50_000_000_000, 0.3, 0.1)
print(f"TAM: ${size.tam:,.0f}")
print(f"SAM: ${size.sam:,.0f}")
print(f"SOM: ${size.som:,.0f}")

# Add competitor
oracle.competitive.add_competitor("AlphaCorp", 0.25, ["Brand"], ["Innovation"])

# Generate report
report = oracle.reports.generate_report(
    "Market Analysis",
    "Strong growth identified.",
    ["Growth 15%", "Market expanding"],
    ["Invest in R&D", "Target new segments"]
)
print(f"Report: {report.title}")
```

### 60-Second Setup

```python
from agents.market_research_oracle.agent import MarketResearchOracle

oracle = MarketResearchOracle()

# Quick market sizing
oracle.market_size.estimate("AI Tools", 30_000_000_000, 0.2, 0.05, 25)

# Quick trend detection
from datetime import datetime
oracle.trends.add_data_point("revenue", datetime(2025, 1, 1), 100)
oracle.trends.add_data_point("revenue", datetime(2025, 6, 1), 180)
trends = oracle.trends.detect_trends("revenue")
print(f"Trend: {trends[0]['trend_type']}")
```

---

## Installation

### From PyPI

```bash
pip install awesome-grok-skills
```

### From Source

```bash
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e .
```

### Development Install

```bash
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e ".[dev]"
pytest  # Run tests
```

### Requirements

```
Python >= 3.10
No external dependencies (stdlib only)
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

### Component Independence

```python
from agents.market_research_oracle.agent import SurveyBuilder, TrendAnalyzer

# Use components directly without the facade
surveys = SurveyBuilder()
trends = TrendAnalyzer()

survey = surveys.create_survey("Direct Survey")
trends.add_data_point("metric", datetime.now(), 100)
```

### CLI Usage

```bash
# Run full research cycle
python agents/market-research-oracle/agent.py --research "AI market"

# Generate report
python agents/market-research-oracle/agent.py --report --title "Q2 Analysis"

# Export data
python agents/market-research-oracle/agent.py --export --format json
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
| `get_survey(survey_id)` | Get survey details |
| `get_response_count(survey_id)` | Get response count |

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
| `get_data_points(metric)` | Get raw data points |

### CompetitiveLandscape

| Method | Description |
|--------|-------------|
| `add_competitor(name, share, strengths, weaknesses)` | Add competitor |
| `generate_swot(competitor_id)` | Generate SWOT |
| `competitive_matrix()` | Full competitive matrix |
| `get_threat_assessment()` | Threat scoring |
| `list_competitors()` | All competitors |
| `update_competitor(id, **kwargs)` | Update competitor |
| `remove_competitor(id)` | Remove competitor |

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
from agents.market_research_oracle.agent import MarketResearchOracle
from datetime import datetime

oracle = MarketResearchOracle()

# Collect data from multiple sources
oracle.data_collector.collect("twitter", "AI tools", [
    {"sentiment_score": 0.8, "keywords": ["AI", "automation"]},
    {"sentiment_score": 0.6, "keywords": ["AI", "productivity"]},
])
oracle.data_collector.collect("news", "AI tools", [
    {"sentiment_score": 0.9, "keywords": ["AI", "growth"]},
])

# Analyze sentiment
sentiment = oracle.data_collector.aggregate_sentiment("AI tools")
print(f"Sentiment: {sentiment.label.value} ({sentiment.score})")

# Detect trends
oracle.trends.add_data_point("ai_market", datetime(2025, 1, 1), 100)
oracle.trends.add_data_point("ai_market", datetime(2025, 6, 1), 180)
oracle.trends.add_data_point("ai_market", datetime(2025, 12, 1), 300)
trends = oracle.trends.detect_trends("ai_market")
print(f"Trend: {trends[0]['trend_type']}, Growth: {trends[0]['growth_rate']:.1f}%")

# Size market
oracle.market_size.estimate("AI Tools", 30_000_000_000, 0.2, 0.05, 25)
```

### Competitive SWOT Analysis

```python
oracle = MarketResearchOracle()

oracle.competitive.add_competitor("LeaderCorp", 0.30, ["Brand", "Distribution"], ["High prices"])
oracle.competitive.add_competitor("ChallengerAI", 0.15, ["Innovation", "Price"], ["Scale"])
oracle.competitive.add_competitor("NichePlayer", 0.05, ["Specialization"], ["Limited reach"])

for comp in oracle.competitive.list_competitors():
    swot = oracle.competitive.generate_swot(comp.competitor_id)
    print(f"\n{swot['competitor']}:")
    print(f"  Strengths: {swot['strengths']}")
    print(f"  Threats: {swot['threats']}")
    print(f"  Position: {swot['position']}")

threats = oracle.competitive.get_threat_assessment()
for t in threats['threats']:
    print(f"Threat Level {t['threat_level']}: {t['competitor']}")
```

### Multi-Method Forecasting

```python
from agents.market_research_oracle.agent import ForecastEngine

engine = ForecastEngine()
values = [100, 112, 125, 140, 158, 179]

# Run all methods
ma = engine.moving_average("revenue", values, window=3)
es = engine.exponential_smoothing("revenue", values, alpha=0.3)
lr = engine.linear_regression("revenue", values)

# Compare results
for f in engine.list_forecasts():
    print(f"{f.method.value}: next={f.predicted_values[-1]:.1f}, accuracy={f.accuracy_score:.2f}")
```

### Survey Analysis

```python
from agents.market_research_oracle.agent import SurveyBuilder, SurveyQuestionType

builder = SurveyBuilder()

survey = builder.create_survey("Product Feedback", "Annual survey", target_responses=500)

builder.add_question(survey.survey_id, "Satisfaction?", SurveyQuestionType.RATING)
builder.add_question(survey.survey_id, "Recommend us?", SurveyQuestionType.NET_PROMOTER)
builder.add_question(survey.survey_id, "Features used?", SurveyQuestionType.MULTIPLE_CHOICE, ["A", "B", "C"])

# Submit sample responses
for i in range(10):
    builder.submit_response(survey.survey_id, f"user_{i}", {
        "q1": 7 + (i % 3),
        "q2": 8 + (i % 2),
        "q3": ["A", "B", "C"][i % 3]
    })

analysis = builder.analyze_survey(survey.survey_id)
print(f"Responses: {analysis['total_responses']}")
print(f"Satisfaction: {analysis['questions']['q1']['mean']:.1f}")
```

---

## Configuration

### Data Source Reliability

| Source Type | Default Reliability | Description |
|------------|-------------------|-------------|
| GOVERNMENT | 0.95 | Census, BLS, SEC |
| FINANCIAL_API | 0.92 | Yahoo Finance, Alpha Vantage |
| PROPRIETARY | 0.90 | Gartner, Forrester |
| NEWS | 0.85 | NewsAPI, RSS feeds |
| SOCIAL_MEDIA | 0.80 | Twitter, Reddit |
| WEB_SCRAPE | 0.70 | Competitor websites |

### Trend Detection Thresholds

| Slope Range | Classification | Growth Rate |
|------------|---------------|-------------|
| > 0.10 | GROWTH | > 10% |
| 0.02 to 0.10 | EMERGING | 2% to 10% |
| -0.02 to 0.02 | MATURING | -2% to 2% |
| -0.10 to -0.02 | STABLE | -10% to -2% |
| < -0.10 | DECLINING | < -10% |

### Forecast Method Selection

| Scenario | Recommended Method |
|----------|-------------------|
| Stable, low volatility | MOVING_AVERAGE |
| Recent trends important | EXPONENTIAL_SMOOTHING |
| Consistent growth/decline | LINEAR_REGRESSION |
| Short time series (< 5 points) | MOVING_AVERAGE |
| Long time series (> 10 points) | LINEAR_REGRESSION |

### Competitive Position Thresholds

| Position | Market Share | Growth Rate |
|----------|-------------|-------------|
| LEADER | > 25% | Stable |
| CHALLENGER | > 15% | > 10% |
| FOLLOWER | < 10% | Stable |
| NICHE | < 5% | Stable |
| EMERGING | < 2% | > 20% |

---

## Best Practices

### Survey Design
- Keep surveys under 10 minutes completion time
- Mix question types for engagement
- Always include at least one NPS question
- Pilot test before full distribution
- Set realistic response targets
- Use clear, non-leading language
- Ensure answer options are exhaustive

### Data Collection
- Register sources with accurate reliability scores
- Collect from at least 3 sources for cross-validation
- Track source freshness and update regularly
- Anonymize respondent data before analysis
- Validate data quality before aggregation
- Document data collection methodology

### Trend Detection
- Use at least 5 data points for reliable detection
- Update data regularly (weekly minimum)
- Compare detected trends across multiple metrics
- Document external factors that may influence trends
- Validate trends against domain knowledge
- Monitor for false positives

### Competitive Analysis
- Update competitor profiles quarterly
- Monitor for new entrants regularly
- Track pricing changes and product launches
- Include indirect competitors in analysis
- Validate market share data from multiple sources
- Document assumptions in SWOT analysis

### Forecasting
- Validate model accuracy before relying on predictions
- Use multiple methods and compare results
- Document assumptions and limitations
- Update forecasts as new data arrives
- Include confidence intervals in reports
- Review and recalibrate quarterly

### Reporting
- Lead with executive summary
- Support findings with data
- Make recommendations actionable
- Document data sources
- Include methodology section
- Version reports for tracking

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
| Report generation fails | Empty sections | Ensure sections have content |
| Data collection fails | Source not registered | Call `register_source` first |
| Forecast returns NaN | Division by zero | Check input values are non-zero |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

oracle = MarketResearchOracle()
# Now all operations will log detailed debug information
```

### Common Error Messages

| Error | Meaning | Fix |
|-------|---------|-----|
| `SurveyNotFoundError` | Survey ID doesn't exist | Verify survey_id |
| `InsufficientDataError` | Not enough data for analysis | Add more data points |
| `InvalidForecastError` | Data incompatible with method | Try different method |
| `CompetitorNotFoundError` | Competitor ID doesn't exist | Verify competitor_id |
| `DataSourceError` | Source unavailable | Check source registration |

---

## FAQ

### Q: Can I use components independently?
A: Yes, each component (SurveyBuilder, TrendAnalyzer, etc.) can be used standalone without the MarketResearchOracle facade.

### Q: How many data points are needed for trend detection?
A: Minimum 3 data points, but 5+ recommended for reliable detection.

### Q: What's the minimum for forecasting?
A: At least 3 data points for moving average, 4+ for linear regression.

### Q: Can I customize reliability scores?
A: Yes, when registering sources, provide your own reliability score (0.0-1.0).

### Q: How do I handle missing data?
A: The system skips missing values in calculations. Document gaps in reports.

### Q: Can I export data?
A: Yes, all data classes have `to_dict()` methods for serialization.

---

## Contributing

We welcome contributions! Please see our [Contributing Guide](../../CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e ".[dev]"
pre-commit install
```

### Running Tests

```bash
pytest tests/market_research_oracle/
pytest --cov=agents.market_research_oracle
```

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for public methods
- Add tests for new functionality

---

## License

MIT License - see [LICENSE](../../LICENSE) for details.

---

## Support

- Documentation: [docs.example.com](https://docs.example.com)
- Issues: [GitHub Issues](https://github.com/awesome-grok-skills/awesome-grok-skills/issues)
- Discussions: [GitHub Discussions](https://github.com/awesome-grok-skills/awesome-grok-skills/discussions)
