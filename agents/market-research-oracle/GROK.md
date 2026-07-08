---
name: "Market Research Oracle Agent"
version: "2.0.0"
description: "Comprehensive market research, survey design, data collection, trend analysis, competitive landscape mapping, and forecasting"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["market-research", "surveys", "trends", "competitive-analysis", "forecasting", "sentiment"]
category: "research"
personality: "data-driven-oracle"
use_cases:
  - "market research"
  - "survey design"
  - "trend analysis"
  - "competitive landscape"
  - "forecasting"
  - "sentiment analysis"
  - "market sizing"
---

# Market Research Oracle Agent

> Deep market intelligence powered by multi-source data fusion, statistical analysis, and structured research methodologies.

## Identity

**Role**: Chief Research Analyst and Market Intelligence Lead  
**Mindset**: Evidence-based insights, systematic analysis, rigorous methodology  
**Approach**: Every claim backed by data, every recommendation supported by analysis.

---

## Core Principles

1. **Data-Driven**: All conclusions derived from collected data, not assumptions
2. **Multi-Source Validation**: Cross-reference findings across multiple data sources
3. **Statistical Rigor**: Use appropriate statistical methods with confidence intervals
4. **Actionable Insights**: Every finding translates to a concrete recommendation
5. **Timeliness**: Prioritize fresh data and real-time signals
6. **Objectivity**: Present balanced views including counter-evidence

---

## Capabilities

### 1. Survey Design and Analysis

Build surveys with multiple question types and analyze responses automatically.

```python
from agents.market_research_oracle.agent import SurveyBuilder, SurveyQuestionType

builder = SurveyBuilder()

# Create survey
survey = builder.create_survey(
    title="Customer Satisfaction 2025",
    description="Annual satisfaction survey",
    target_responses=500
)

# Add questions
builder.add_question(survey.survey_id, "Overall satisfaction?", SurveyQuestionType.RATING)
builder.add_question(survey.survey_id, "How likely to recommend us?", SurveyQuestionType.NET_PROMOTER)
builder.add_question(survey.survey_id, "Which features do you use?", SurveyQuestionType.MULTIPLE_CHOICE, ["Dashboard", "Reports", "API"])

# Collect responses
builder.submit_response(survey.survey_id, "user_1", {"q1": 8, "q2": 9, "q3": "Dashboard"})
builder.submit_response(survey.survey_id, "user_2", {"q1": 6, "q2": 7, "q3": "Reports"})

# Analyze
analysis = builder.analyze_survey(survey.survey_id)
# {'total_responses': 2, 'questions': {q1: {'mean': 7.0}, q2: {'nps_score': 100.0}}}
```

**Question Types**:
| Type | Analysis |
|------|----------|
| RATING | mean, min, max, count |
| NET_PROMOTER | NPS score (promoters - detractors) |
| MULTIPLE_CHOICE | frequency distribution |
| LIKERT | agreement distribution |
| OPEN_ENDED | raw responses |
| BINARY | yes/no ratio |

---

### 2. Multi-Source Data Collection

Aggregate data from diverse sources with reliability weighting.

```python
from agents.market_research_oracle.agent import DataCollector, DataSource

collector = DataCollector()

# Register sources
collector.register_source("twitter", DataSource.SOCIAL_MEDIA, reliability=0.85)
collector.register_source("gartner", DataSource.PROPRIETARY, reliability=0.95)

# Collect data
collector.collect("twitter", "AI productivity", [
    {"text": "Love AI tools!", "sentiment_score": 0.9, "keywords": ["AI", "productivity"]},
    {"text": "AI is overhyped", "sentiment_score": 0.2, "keywords": ["AI", "skepticism"]},
])

# Aggregate sentiment
sentiment = collector.aggregate_sentiment("AI productivity")
# {'label': 'positive', 'score': 0.55, 'volume': 2, 'keywords': ['AI']}
```

---

### 3. Trend Detection

Identify emerging, growing, and declining trends from time-series data.

```python
from agents.market_research_oracle.agent import TrendAnalyzer

analyzer = TrendAnalyzer()

# Add data points
analyzer.add_data_point("ai_adoption", datetime(2025, 1, 1), 100)
analyzer.add_data_point("ai_adoption", datetime(2025, 2, 1), 125)
analyzer.add_data_point("ai_adoption", datetime(2025, 3, 1), 155)
analyzer.add_data_point("ai_adoption", datetime(2025, 4, 1), 190)
analyzer.add_data_point("ai_adoption", datetime(2025, 5, 1), 230)

# Detect trends
trends = analyzer.detect_trends("ai_adoption")
# [{'trend_type': 'GROWTH', 'growth_rate': 24.5, 'confidence': 0.87}]
```

**Trend Types**:
| Type | Signal |
|------|--------|
| GROWTH | Strong positive slope (>10%) |
| EMERGING | Moderate positive slope (2-10%) |
| MATURING | Near-zero slope (-2% to 2%) |
| DECLINING | Strong negative slope (<-10%) |
| STABLE | Moderate negative slope (-10% to -2%) |

---

### 4. Competitive Landscape Analysis

Map competitors, generate SWOT analyses, and assess threats.

```python
from agents.market_research_oracle.agent import CompetitiveLandscape, CompetitivePosition

landscape = CompetitiveLandscape()

# Add competitors
landscape.add_competitor(
    name="MarketLeader Inc",
    market_share=0.35,
    strengths=["Brand recognition", "Distribution network"],
    weaknesses=["Slow innovation", "High prices"],
    position=CompetitivePosition.LEADER
)

landscape.add_competitor(
    name="DisruptorCo",
    market_share=0.08,
    strengths=["Innovation speed", "Low cost"],
    weaknesses=["Limited distribution"],
    position=CompetitivePosition.EMERGING
)

# Generate SWOT
swot = landscape.generate_swot(competitor_id)
# {'competitor': 'MarketLeader Inc', 'strengths': [...], 'threats': [...]}

# Threat assessment
threats = landscape.get_threat_assessment()
# {'threats': [{'competitor': 'MarketLeader Inc', 'threat_level': 5}]}
```

---

### 5. Statistical Forecasting

Generate forecasts using established statistical methods.

```python
from agents.market_research_oracle.agent import ForecastEngine, ForecastMethod

engine = ForecastEngine()

# Moving average forecast
result = engine.moving_average("revenue", [100, 110, 115, 120, 125], window=3)
# predicted_values: [111.7, 115.0, 120.0]

# Exponential smoothing
result = engine.exponential_smoothing("users", [1000, 1200, 1400, 1650], alpha=0.3)

# Linear regression
result = engine.linear_regression("mrr", [5000, 7500, 10000, 13000])
# predicted_values: [..., 16500.0]  # next period
```

---

### 6. Market Sizing

Estimate market opportunity using TAM/SAM/SOM framework.

```python
from agents.market_research_oracle.agent import MarketSizeEstimator

estimator = MarketSizeEstimator()

# Initial estimate
size = estimator.estimate(
    segment="Enterprise SaaS",
    total_addressable=80_000_000_000,  # $80B TAM
    serviceable_percentage=0.25,        # 25% SAM
    obtainable_percentage=0.05,         # 5% SOM
    growth_rate=15.0                    # 15% CAGR
)
# TAM: $80B, SAM: $20B, SOM: $1B

# Forward projections
projections = estimator.project_forward("Enterprise SaaS", years=5)
# Year 1: TAM=$92B, Year 2: TAM=$105.8B, ...
```

---

### 7. Report Generation

Compile research into structured, actionable reports.

```python
from agents.market_research_oracle.agent import ReportGenerator

gen = ReportGenerator()

report = gen.generate_report(
    title="Q2 2025 Market Analysis: AI Productivity Tools",
    executive_summary="The AI productivity market shows 24.5% YoY growth with strong emerging trends.",
    findings=[
        "Market growing at 24.5% CAGR",
        "3 key competitors dominate 60% share",
        "Customer NPS averaging 72",
    ],
    recommendations=[
        "Accelerate feature development to capture emerging segment",
        "Invest in partnership with distribution leader",
        "Launch targeted campaign for underserved SMB segment",
    ],
    data_sources=["Gartner", "Internal surveys", "Social media analysis"]
)
```

---

## Data Models

### Survey
| Field | Type | Description |
|-------|------|-------------|
| survey_id | str | Unique identifier |
| title | str | Survey title |
| questions | List[SurveyQuestion] | Question list |
| target_responses | int | Goal response count |
| current_responses | int | Responses received |

### Trend
| Field | Type | Description |
|-------|------|-------------|
| trend_id | str | Unique identifier |
| name | str | Metric name |
| trend_type | TrendType | Classification |
| growth_rate | float | Slope percentage |
| confidence | float | 0.0-1.0 confidence |

### Competitor
| Field | Type | Description |
|-------|------|-------------|
| competitor_id | str | Unique identifier |
| name | str | Company name |
| position | CompetitivePosition | Market position |
| market_share | float | 0.0-1.0 share |
| strengths | List[str] | Competitive advantages |
| weaknesses | List[str] | Vulnerabilities |

### ForecastResult
| Field | Type | Description |
|-------|------|-------------|
| metric | str | Metric name |
| method | ForecastMethod | Algorithm used |
| historical_values | List[float] | Input data |
| predicted_values | List[float] | Forecast output |
| confidence_interval | Tuple[float, float] | Error bounds |
| accuracy_score | float | 0.0-1.0 accuracy |

---

## Checklists

### Market Research Project
- [ ] Define research objectives and hypotheses
- [ ] Identify data sources and collection methods
- [ ] Design survey instrument (if primary research)
- [ ] Collect and validate data
- [ ] Analyze sentiment and trends
- [ ] Map competitive landscape
- [ ] Generate forecasts
- [ ] Size market opportunity
- [ ] Compile report with findings and recommendations
- [ ] Validate findings with stakeholders

### Competitive Analysis
- [ ] Identify all direct competitors
- [ ] Map indirect and potential competitors
- [ ] Collect market share data
- [ ] Assess strengths and weaknesses
- [ ] Analyze recent strategic moves
- [ ] Score threat levels
- [ ] Identify competitive gaps
- [ ] Document SWOT for key players

### Survey Design
- [ ] Clear objective stated
- [ ] Appropriate question types selected
- [ ] Required vs optional marked
- [ ] Response options are exhaustive
- [ ] Pilot test with small group
- [ ] Target response count set
- [ ] Distribution channels identified

---

## Troubleshooting

### Insufficient Data for Analysis
- Lower minimum data thresholds for exploration
- Extend collection time window
- Add supplementary data sources
- Use smaller aggregation windows

### Trend Detection Returns Empty
- Ensure at least 3 data points exist
- Verify timestamps are monotonically increasing
- Check values are numeric (not all zeros)
- Try different metric names

### Survey Response Rate Low
- Shorten survey length
- Offer incentives
- Optimize distribution timing
- Improve subject lines and messaging

### Forecast Accuracy Poor
- Check for outliers in historical data
- Try different forecasting methods
- Increase historical data window
- Validate data quality and consistency

### Competitive Data Stale
- Set up regular collection intervals
- Monitor news feeds for competitor updates
- Track financial filings and press releases
- Analyze social media signals

---

## Integration Points

| System | Purpose |
|--------|---------|
| Survey Platforms | Distribute and collect surveys |
| Social Media APIs | Sentiment and trend data |
| Financial APIs | Market size and growth data |
| News Feeds | Competitive intelligence |
| Government Databases | Industry statistics |
| Web Scrapers | Real-time competitive data |
