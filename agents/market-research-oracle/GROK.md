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
  - "report generation"
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
7. **Reproducibility**: Document methodology for audit and replication
8. **Privacy First**: Anonymize respondent data, respect source terms

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
    description="Annual satisfaction survey for product feedback",
    target_responses=500
)
# Returns: Survey(survey_id="sur_abc123", title="Customer Satisfaction 2025", ...)

# Add rating question
q1 = builder.add_question(
    survey.survey_id,
    "How satisfied are you with our product?",
    SurveyQuestionType.RATING
)

# Add NPS question
q2 = builder.add_question(
    survey.survey_id,
    "How likely are you to recommend us to a friend?",
    SurveyQuestionType.NET_PROMOTER
)

# Add multiple choice
q3 = builder.add_question(
    survey.survey_id,
    "Which features do you use most?",
    SurveyQuestionType.MULTIPLE_CHOICE,
    options=["Dashboard", "Reports", "API", "Integrations"]
)

# Add Likert scale
q4 = builder.add_question(
    survey.survey_id,
    "The product is easy to use.",
    SurveyQuestionType.LIKERT
)

# Add open-ended
q5 = builder.add_question(
    survey.survey_id,
    "What improvements would you suggest?",
    SurveyQuestionType.OPEN_ENDED
)

# Add binary
q6 = builder.add_question(
    survey.survey_id,
    "Would you renew your subscription?",
    SurveyQuestionType.BINARY
)

# Submit responses
builder.submit_response(survey.survey_id, "user_1", {
    "q1": 8, "q2": 9, "q3": "Dashboard",
    "q4": 4, "q5": "More integrations", "q6": "Yes"
})
builder.submit_response(survey.survey_id, "user_2", {
    "q1": 6, "q2": 7, "q3": "Reports",
    "q4": 3, "q5": "Better mobile app", "q6": "Yes"
})
builder.submit_response(survey.survey_id, "user_3", {
    "q1": 9, "q2": 10, "q3": "API",
    "q5": "Love it!", "q6": "Yes"
})

# Analyze all responses
analysis = builder.analyze_survey(survey.survey_id)
# {
#   'survey_id': 'sur_abc123',
#   'total_responses': 3,
#   'completion_rate': 100.0,
#   'questions': {
#     'q1': {
#       'type': 'RATING',
#       'mean': 7.67,
#       'median': 8,
#       'min': 6,
#       'max': 9,
#       'count': 3
#     },
#     'q2': {
#       'type': 'NET_PROMOTER',
#       'nps_score': 100.0,
#       'promoters': 2,
#       'passives': 1,
#       'detractors': 0
#     },
#     'q3': {
#       'type': 'MULTIPLE_CHOICE',
#       'distribution': {'Dashboard': 1, 'Reports': 1, 'API': 1}
#     },
#     'q6': {
#       'type': 'BINARY',
#       'yes_ratio': 1.0,
#       'no_ratio': 0.0
#     }
#   }
# }

# List all surveys
surveys = builder.list_surveys()
```

**Question Types**:
| Type | Analysis Output |
|------|----------------|
| RATING | mean, median, min, max, std_dev, count |
| NET_PROMOTER | NPS score, promoter/passive/detractor counts |
| MULTIPLE_CHOICE | frequency distribution, percentages |
| LIKERT | agreement distribution, mean score |
| OPEN_ENDED | raw responses, word counts |
| BINARY | yes/no ratio |
| RANKING | average rank per option |
| DEMOGRAPHIC | distribution by category |

---

### 2. Multi-Source Data Collection

Aggregate data from diverse sources with reliability weighting.

```python
from agents.market_research_oracle.agent import DataCollector, DataSource

collector = DataCollector()

# Register sources with reliability scores
collector.register_source("twitter", DataSource.SOCIAL_MEDIA, reliability=0.85)
collector.register_source("gartner", DataSource.PROPRIETARY, reliability=0.95)
collector.register_source("reuters", DataSource.NEWS, reliability=0.90)
collector.register_source("sec_filings", DataSource.GOVERNMENT, reliability=0.98)

# Collect data from sources
collector.collect("twitter", "AI productivity", [
    {
        "text": "AI tools are transforming how we work!",
        "sentiment_score": 0.9,
        "keywords": ["AI", "productivity", "transformation"]
    },
    {
        "text": "AI is overhyped, not ready for prime time",
        "sentiment_score": 0.2,
        "keywords": ["AI", "skepticism", "overhyped"]
    },
    {
        "text": "Using AI for code reviews has been great",
        "sentiment_score": 0.8,
        "keywords": ["AI", "code", "reviews", "productivity"]
    }
])

collector.collect("gartner", "AI productivity", [
    {
        "text": "Enterprise AI adoption growing 45% YoY",
        "sentiment_score": 0.85,
        "keywords": ["AI", "enterprise", "adoption"]
    }
])

# Aggregate sentiment across sources
sentiment = collector.aggregate_sentiment("AI productivity")
# {
#   'topic': 'AI productivity',
#   'label': 'positive',
#   'score': 0.72,
#   'volume': 4,
#   'keywords': ['AI', 'productivity', 'transformation', 'enterprise'],
#   'sources': ['twitter', 'gartner']
# }

# Get source statistics
stats = collector.get_source_stats()
# {
#   'twitter': {'records': 3, 'reliability': 0.85},
#   'gartner': {'records': 1, 'reliability': 0.95}
# }

# Get data from specific source
data = collector.get_data("twitter", "AI productivity")
# [DataRecord(...), DataRecord(...), ...]
```

---

### 3. Trend Detection

Identify emerging, growing, and declining trends from time-series data.

```python
from agents.market_research_oracle.agent import TrendAnalyzer
from datetime import datetime

analyzer = TrendAnalyzer()

# Add data points over time
analyzer.add_data_point("ai_adoption", datetime(2025, 1, 1), 100)
analyzer.add_data_point("ai_adoption", datetime(2025, 2, 1), 125)
analyzer.add_data_point("ai_adoption", datetime(2025, 3, 1), 155)
analyzer.add_data_point("ai_adoption", datetime(2025, 4, 1), 190)
analyzer.add_data_point("ai_adoption", datetime(2025, 5, 1), 230)
analyzer.add_data_point("ai_adoption", datetime(2025, 6, 1), 280)

# Detect trends
trends = analyzer.detect_trends("ai_adoption")
# [
#   {
#     'trend_id': 'trend_abc123',
#     'name': 'ai_adoption',
#     'trend_type': 'GROWTH',
#     'growth_rate': 24.5,
#     'confidence': 0.87,
#     'slope': 0.0245,
#     'data_points': 6,
#     'volatility': 0.12
#   }
# ]

# Get trend summary by type
summary = analyzer.get_trend_summary()
# {
#   'GROWTH': ['ai_adoption'],
#   'EMERGING': [],
#   'MATURING': [],
#   'DECLINING': [],
#   'STABLE': []
# }

# Add another metric with different pattern
analyzer.add_data_point("legacy_system", datetime(2025, 1, 1), 500)
analyzer.add_data_point("legacy_system", datetime(2025, 3, 1), 480)
analyzer.add_data_point("legacy_system", datetime(2025, 6, 1), 450)

# This will show as DECLINING
trends = analyzer.detect_trends("legacy_system")
# [{'trend_type': 'DECLINING', 'growth_rate': -10.0, ...}]
```

**Trend Types**:
| Type | Slope Signal | Growth Rate |
|------|-------------|-------------|
| GROWTH | > 0.10 | > 10% |
| EMERGING | > 0.02 | 2-10% |
| MATURING | -0.02 to 0.02 | -2% to 2% |
| DECLINING | < -0.10 | < -10% |
| STABLE | -0.10 to -0.02 | -10% to -2% |

---

### 4. Competitive Landscape Analysis

Map competitors, generate SWOT analyses, and assess threats.

```python
from agents.market_research_oracle.agent import CompetitiveLandscape, CompetitivePosition

landscape = CompetitiveLandscape()

# Add competitors
leader = landscape.add_competitor(
    name="MarketLeader Inc",
    market_share=0.35,
    strengths=["Brand recognition", "Distribution network", "Large customer base"],
    weaknesses=["Slow innovation", "High prices", "Legacy tech stack"],
    position=CompetitivePosition.LEADER
)

challenger = landscape.add_competitor(
    name="ChallengerAI",
    market_share=0.15,
    strengths=["Innovation speed", "Competitive pricing", "Strong engineering"],
    weaknesses=["Limited distribution", "Small brand", "Narrow focus"],
    position=CompetitivePosition.CHALLENGER
)

emerging = landscape.add_competitor(
    name="DisruptorCo",
    market_share=0.03,
    strengths=["Novel approach", "Viral marketing", "Low cost"],
    weaknesses=["No enterprise sales", "Limited features", "Early stage"],
    position=CompetitivePosition.EMERGING
)

# Generate SWOT for specific competitor
swot = landscape.generate_swot(leader.competitor_id)
# {
#   'competitor': 'MarketLeader Inc',
#   'strengths': ['Brand recognition', 'Distribution network', 'Large customer base'],
#   'weaknesses': ['Slow innovation', 'High prices', 'Legacy tech stack'],
#   'opportunities': ['Expand into emerging markets', 'Acquire startups'],
#   'threats': ['Disruption from agile competitors', 'Price pressure'],
#   'position': 'LEADER',
#   'market_share': 0.35
# }

# Get competitive matrix
matrix = landscape.competitive_matrix()
# [
#   {'name': 'MarketLeader Inc', 'share': 0.35, 'position': 'LEADER', 'threat': 4},
#   {'name': 'ChallengerAI', 'share': 0.15, 'position': 'CHALLENGER', 'threat': 5},
#   {'name': 'DisruptorCo', 'share': 0.03, 'position': 'EMERGING', 'threat': 2}
# ]

# Get threat assessment
threats = landscape.get_threat_assessment()
# {
#   'threats': [
#     {'competitor': 'ChallengerAI', 'threat_level': 5, 'reasons': ['Growing fast', 'Strong innovation']},
#     {'competitor': 'MarketLeader Inc', 'threat_level': 4, 'reasons': ['Large share']},
#     {'competitor': 'DisruptorCo', 'threat_level': 2, 'reasons': ['Small share']}
#   ]
# }

# List all competitors
competitors = landscape.list_competitors()
```

---

### 5. Statistical Forecasting

Generate forecasts using established statistical methods.

```python
from agents.market_research_oracle.agent import ForecastEngine, ForecastMethod

engine = ForecastEngine()

# Moving average forecast
ma_result = engine.moving_average(
    "revenue",
    [100, 110, 115, 120, 125],
    window=3
)
# {
#   'metric': 'revenue',
#   'method': 'MOVING_AVERAGE',
#   'historical_values': [100, 110, 115, 120, 125],
#   'predicted_values': [111.67, 115.0, 120.0],
#   'confidence_interval': (118.5, 121.5),
#   'accuracy_score': 0.94
# }

# Exponential smoothing
es_result = engine.exponential_smoothing(
    "users",
    [1000, 1200, 1400, 1650],
    alpha=0.3
)
# Predicted next: ~1825

# Linear regression
lr_result = engine.linear_regression(
    "mrr",
    [5000, 7500, 10000, 13000, 16000]
)
# Predicted next: ~19000

# Compare methods
for method in [ForecastMethod.MOVING_AVERAGE, ForecastMethod.EXPONENTIAL_SMOOTHING, ForecastMethod.LINEAR_REGRESSION]:
    result = engine.linear_regression("revenue", [100, 110, 125, 140, 160])
    print(f"{method.value}: accuracy={result.accuracy_score:.2f}")

# Get saved forecast
saved = engine.get_forecast("revenue")

# List all forecasts
all_forecasts = engine.list_forecasts()
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
# {
#   'segment': 'Enterprise SaaS',
#   'tam': 80000000000,
#   'sam': 20000000000,
#   'som': 1000000000,
#   'growth_rate': 15.0
# }

# Forward projections (5 years)
projections = estimator.project_forward("Enterprise SaaS", years=5)
# [
#   {'year': 1, 'tam': 92000000000, 'sam': 23000000000, 'som': 1150000000},
#   {'year': 2, 'tam': 105800000000, 'sam': 26450000000, 'som': 1322500000},
#   {'year': 3, 'tam': 121670000000, 'sam': 30417500000, 'som': 1520875000},
#   {'year': 4, 'tam': 139920500000, 'sam': 34980125000, 'som': 1749006250},
#   {'year': 5, 'tam': 160908575000, 'sam': 40227143750, 'som': 2011357188}
# ]

# Get specific estimate
estimate = estimator.get_estimate("Enterprise SaaS")

# List all estimates
all_estimates = estimator.list_estimates()
```

---

### 7. Report Generation

Compile research into structured, actionable reports.

```python
from agents.market_research_oracle.agent import ReportGenerator

gen = ReportGenerator()

# Generate comprehensive report
report = gen.generate_report(
    title="Q2 2025 Market Analysis: AI Productivity Tools",
    executive_summary="The AI productivity market shows 24.5% YoY growth with strong emerging trends. MarketLeader Inc holds 35% share but faces disruption from ChallengerAI.",
    findings=[
        "Market growing at 24.5% CAGR, reaching $30B by 2027",
        "3 key competitors dominate 60% of market share",
        "Customer NPS averaging 72, with room for improvement",
        "Enterprise adoption accelerating, SMB still untapped",
        "Regulatory changes may impact growth in EU markets"
    ],
    recommendations=[
        "Accelerate feature development to capture emerging segment",
        "Invest in partnership with distribution leader",
        "Launch targeted campaign for underserved SMB segment",
        "Prepare compliance framework for EU AI regulations",
        "Consider acquisition of smaller players for technology"
    ],
    data_sources=["Gartner", "Internal surveys", "Social media analysis", "SEC filings"]
)
# {
#   'report_id': 'rpt_xyz789',
#   'title': 'Q2 2025 Market Analysis: AI Productivity Tools',
#   'sections': [],
#   'findings': ['Market growing...', ...],
#   'recommendations': ['Accelerate...', ...],
#   'generated_at': datetime(2025, 7, 1, 12, 0)
# }

# Add detailed sections
gen.add_section(report.report_id, "Market Size Analysis", "The TAM for AI productivity tools...")
gen.add_section(report.report_id, "Competitive Landscape", "MarketLeader Inc dominates with...")
gen.add_section(report.report_id, "Customer Sentiment", "NPS of 72 indicates...")

# Retrieve report
full_report = gen.get_report(report.report_id)

# List all reports
reports = gen.list_reports()
```

---

## Data Models

### Survey
| Field | Type | Description |
|-------|------|-------------|
| survey_id | str | Unique identifier |
| title | str | Survey title |
| description | str | Survey description |
| questions | List[SurveyQuestion] | Question list |
| target_responses | int | Goal response count |
| current_responses | int | Responses received |
| created_at | datetime | Creation timestamp |

### SurveyQuestion
| Field | Type | Description |
|-------|------|-------------|
| question_id | str | Unique identifier |
| text | str | Question text |
| question_type | SurveyQuestionType | Question type |
| options | List[str] | Options (for multiple choice) |
| required | bool | Is required |

### Trend
| Field | Type | Description |
|-------|------|-------------|
| trend_id | str | Unique identifier |
| name | str | Metric name |
| trend_type | TrendType | Classification |
| growth_rate | float | Slope percentage |
| confidence | float | 0.0-1.0 confidence |
| slope | float | Regression slope |
| volatility | float | Data volatility |
| data_points | int | Number of data points |

### Competitor
| Field | Type | Description |
|-------|------|-------------|
| competitor_id | str | Unique identifier |
| name | str | Company name |
| position | CompetitivePosition | Market position |
| market_share | float | 0.0-1.0 share |
| growth_rate | float | Annual growth rate |
| strengths | List[str] | Competitive advantages |
| weaknesses | List[str] | Vulnerabilities |
| sentiment_score | float | Market sentiment 0.0-1.0 |

### ForecastResult
| Field | Type | Description |
|-------|------|-------------|
| metric | str | Metric name |
| method | ForecastMethod | Algorithm used |
| historical_values | List[float] | Input data |
| predicted_values | List[float] | Forecast output |
| confidence_interval | Tuple[float, float] | Error bounds |
| accuracy_score | float | 0.0-1.0 accuracy |

### MarketSize
| Field | Type | Description |
|-------|------|-------------|
| segment | str | Market segment |
| tam | float | Total Addressable Market |
| sam | float | Serviceable Addressable Market |
| som | float | Serviceable Obtainable Market |
| growth_rate | float | CAGR percentage |

### Report
| Field | Type | Description |
|-------|------|-------------|
| report_id | str | Unique identifier |
| title | str | Report title |
| executive_summary | str | Overview text |
| sections | List[ReportSection] | Content sections |
| findings | List[str] | Key insights |
| recommendations | List[str] | Actionable items |
| data_sources | List[str] | Sources used |
| generated_at | datetime | Generation timestamp |

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
- [ ] Document methodology for reproducibility
- [ ] Archive raw data and analysis

### Competitive Analysis
- [ ] Identify all direct competitors
- [ ] Map indirect and potential competitors
- [ ] Collect market share data
- [ ] Assess strengths and weaknesses
- [ ] Analyze recent strategic moves
- [ ] Score threat levels
- [ ] Identify competitive gaps
- [ ] Document SWOT for key players
- [ ] Update quarterly
- [ ] Track pricing changes

### Survey Design
- [ ] Clear objective stated
- [ ] Appropriate question types selected
- [ ] Required vs optional marked
- [ ] Response options are exhaustive
- [ ] Pilot test with small group
- [ ] Target response count set
- [ ] Distribution channels identified
- [ ] Anonymity assured
- [ ] Time estimate provided
- [ ] Thank you message configured

### Forecast Validation
- [ ] Minimum 5 data points used
- [ ] Multiple methods compared
- [ ] Accuracy score > 0.8
- [ ] Confidence intervals reasonable
- [ ] Assumptions documented
- [ ] Edge cases tested
- [ ] Results sanity-checked

---

## Troubleshooting

### Insufficient Data for Analysis
- Lower minimum data thresholds for exploration
- Extend collection time window
- Add supplementary data sources
- Use smaller aggregation windows
- Document data limitations in report

### Trend Detection Returns Empty
- Ensure at least 3 data points exist
- Verify timestamps are monotonically increasing
- Check values are numeric (not all zeros)
- Try different metric names
- Check for data entry errors

### Survey Response Rate Low
- Shorten survey length
- Offer incentives
- Optimize distribution timing
- Improve subject lines and messaging
- Follow up with non-respondents

### Forecast Accuracy Poor
- Check for outliers in historical data
- Try different forecasting methods
- Increase historical data window
- Validate data quality and consistency
- Consider external factors

### Competitive Data Stale
- Set up regular collection intervals
- Monitor news feeds for competitor updates
- Track financial filings and press releases
- Analyze social media signals
- Use web scraping for real-time data

### Report Generation Fails
- Verify all required sections have content
- Check for empty findings or recommendations
- Ensure data sources are documented
- Validate timestamp formats

---

## Integration Points

| System | Purpose |
|--------|---------|
| Survey Platforms | Distribute and collect surveys (Typeform, SurveyMonkey) |
| Social Media APIs | Sentiment and trend data (Twitter, Reddit) |
| Financial APIs | Market size and growth data (Yahoo Finance, Alpha Vantage) |
| News Feeds | Competitive intelligence (NewsAPI, RSS) |
| Government Databases | Industry statistics (Census, BLS, SEC) |
| Web Scrapers | Real-time competitive data |
| CRM Systems | Customer data integration |
| BI Tools | Data visualization (Tableau, PowerBI) |

---

## Advanced Usage

### Custom Trend Detection
```python
from agents.market_research_oracle.agent import TrendAnalyzer
from datetime import datetime, timedelta

analyzer = TrendAnalyzer()

# Simulate 12 months of data
base_date = datetime(2025, 1, 1)
for i in range(12):
    value = 100 * (1.15 ** i)  # 15% monthly growth
    analyzer.add_data_point("revenue", base_date + timedelta(days=30*i), value)

trends = analyzer.detect_trends("revenue")
print(f"Trend: {trends[0]['trend_type']}, Growth: {trends[0]['growth_rate']:.1f}%")
```

### Multi-Method Forecast Comparison
```python
engine = ForecastEngine()
values = [100, 112, 125, 140, 158, 179]

# Run all methods
ma = engine.moving_average("revenue", values, window=3)
es = engine.exponential_smoothing("revenue", values, alpha=0.3)
lr = engine.linear_regression("revenue", values)

# Compare accuracy
print(f"Moving Avg: {ma.accuracy_score:.2f}")
print(f"Exp Smooth: {es.accuracy_score:.2f}")
print(f"Linear Reg: {lr.accuracy_score:.2f}")
```

### Complete Market Study
```python
oracle = MarketResearchOracle()

# 1. Survey customers
survey = oracle.surveys.create_survey("Customer Needs", "Understanding market needs")
oracle.surveys.add_question(survey.survey_id, "What matters most?", SurveyQuestionType.RANKING)

# 2. Collect market data
oracle.data_collector.collect("twitter", "market_segment", [...])
oracle.data_collector.collect("news", "market_segment", [...])

# 3. Analyze sentiment
sentiment = oracle.data_collector.aggregate_sentiment("market_segment")

# 4. Detect trends
oracle.trends.add_data_point("market_growth", datetime.now(), 100)
trends = oracle.trends.detect_trends("market_growth")

# 5. Map competitors
oracle.competitive.add_competitor("Leader", 0.30, ["Brand"], ["Price"])

# 6. Generate forecast
oracle.forecast.linear_regression("market_growth", [100, 120, 145, 175])

# 7. Size market
oracle.market_size.estimate("Segment", 50_000_000_000, 0.3, 0.1, 20)

# 8. Generate report
report = oracle.reports.generate_report(
    "Market Study: Segment Analysis",
    "Comprehensive analysis of market opportunity.",
    ["Market growing 20% YoY", "Leader holds 30% share"],
    ["Invest in R&D", "Target underserved segment"]
)
```
