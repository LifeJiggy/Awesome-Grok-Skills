# Market Research Oracle Architecture

## Overview

The Market Research Oracle is a modular research intelligence system that combines survey design, multi-source data collection, sentiment analysis, trend detection, competitive landscape mapping, statistical forecasting, and market sizing into a unified platform. Each subsystem operates independently and exposes a clean API, while the top-level orchestrator coordinates cross-module workflows.

The system is designed for market researchers, product managers, and business analysts who need systematic, data-driven market intelligence. It supports both ad-hoc research queries and comprehensive market studies with full audit trails.

---

## System Context

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         External Data Sources                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐│
│  │ Social   │  │  News    │  │Financial │  │Government│  │  Survey  ││
│  │ Media    │  │  Feeds   │  │  APIs    │  │  Data    │  │ Platforms││
│  │ (Twitter,│  │ (RSS,    │  │ (Yahoo,  │  │ (Census, │  │ (Typeform││
│  │  Reddit) │  │  NewsAPI)│  │  Alpha)  │  │  BLS)    │  │  SurveyM)││
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘│
│       │             │             │             │             │        │
│  ┌────▼─────────────▼─────────────▼─────────────▼─────────────▼────┐  │
│  │                     Data Collector                               │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐  │  │
│  │  │  Source    │ │  Validate  │ │  Normalize │ │  Store     │  │  │
│  │  │  Registry │ │  & Clean   │ │  & Enrich  │ │  & Index   │  │  │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘  │  │
│  └─────────────────────────┬──────────────────────────────────────┘  │
│                            │                                           │
│  ┌─────────────────────────▼──────────────────────────────────────┐  │
│  │               Market Research Oracle Core                       │  │
│  │                                                                 │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │  │
│  │  │   Survey     │  │    Trend     │  │ Competitive  │         │  │
│  │  │   Builder    │  │   Analyzer   │  │  Landscape   │         │  │
│  │  │              │  │              │  │              │         │  │
│  │  │  Questions   │  │  Time Series │  │  SWOT        │         │  │
│  │  │  Responses   │  │  Regression  │  │  Positioning │         │  │
│  │  │  Analytics   │  │  Classification│ │  Threat Score│         │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘         │  │
│  │                                                                 │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │  │
│  │  │   Forecast   │  │   Market     │  │   Report     │         │  │
│  │  │   Engine     │  │ Size Est.    │  │  Generator   │         │  │
│  │  │              │  │              │  │              │         │  │
│  │  │  Moving Avg  │  │  TAM/SAM/SOM │  │  Sections    │         │  │
│  │  │  Exp. Smooth │  │  Forward     │  │  Findings    │         │  │
│  │  │  Lin. Regr.  │  │  Projection  │  │  Recs        │         │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘         │  │
│  └─────────────────────────┬──────────────────────────────────────┘  │
│                            │                                           │
│  ┌─────────────────────────▼──────────────────────────────────────┐  │
│  │                        Data Layer                                │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐               │  │
│  │  │  Survey    │  │   Time     │  │ Competitor │               │  │
│  │  │ Responses  │  │  Series    │  │  Profiles  │               │  │
│  │  │            │  │            │  │            │               │  │
│  │  │  per-survey│  │  per-metric│  │  per-company│              │  │
│  │  │  per-question│ │  per-time  │  │  SWOT data │               │  │
│  │  └────────────┘  └────────────┘  └────────────┘               │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐               │  │
│  │  │  Sentiment │  │  Forecast  │  │   Report   │               │  │
│  │  │   Store    │  │   Store    │  │   Store    │               │  │
│  │  └────────────┘  └────────────┘  └────────────┘               │  │
│  └────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. Survey Builder

**Purpose**: Design surveys, collect responses, and compute per-question analytics.

```
┌───────────────────────────────────────────────────────────────────────┐
│                          Survey Builder                                │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Public API:                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ create_survey(title, description, target_responses)             │  │
│  │ add_question(survey_id, text, type, options)                    │  │
│  │ submit_response(survey_id, respondent_id, answers)              │  │
│  │ analyze_survey(survey_id) → SurveyAnalysis                      │  │
│  │ list_surveys() → List[Survey]                                   │  │
│  │ get_survey(survey_id) → Survey                                  │  │
│  │ get_response_count(survey_id) → int                             │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Question Types:                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ RATING         → numeric scale (1-5, 1-10)                     │  │
│  │ MULTIPLE_CHOICE → single selection from options                 │  │
│  │ NET_PROMOTER   → NPS score (0-10)                              │  │
│  │ LIKERT         → agreement scale (1-5)                          │  │
│  │ OPEN_ENDED     → free text response                             │  │
│  │ BINARY         → yes/no                                         │  │
│  │ RANKING        → ordered preference list                        │  │
│  │ DEMOGRAPHIC    → age, gender, income, etc.                      │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Analysis per Question Type:                                          │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ RATING        → mean, median, min, max, std_dev, count         │  │
│  │ MULTIPLE_CHOICE → frequency distribution, percentages           │  │
│  │ NET_PROMOTER  → NPS = %Promoters - %Detractors                 │  │
│  │ LIKERT        → agreement distribution, mean score             │  │
│  │ OPEN_ENDED    → raw responses, word_count, common_words        │  │
│  │ BINARY        → yes_ratio, no_ratio, total                     │  │
│  │ RANKING       → average rank per option                         │  │
│  │ DEMOGRAPHIC   → distribution by category                        │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Internal State:                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ _surveys: Dict[str, Survey]                                     │  │
│  │ _responses: Dict[str, List[SurveyResponse]]                     │  │
│  │ _questions: Dict[str, List[SurveyQuestion]]                     │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────┘
```

**Data Flow**:
```
Survey Creation:
  User Input → Title/Desc Validation → Survey Object → Store

Question Addition:
  Survey ID → Type Validation → Options Check → Question Object → Append to Survey

Response Submission:
  Survey ID → Respondent ID → Answer Validation → Response Object → Store

Analysis:
  Survey ID → Load Responses → Per-Question Aggregation → SurveyAnalysis → Return
```

**NPS Calculation**:
```python
# NPS = % Promoters (9-10) - % Detractors (0-6)
promoters = count(score >= 9) / total * 100
detractors = count(score <= 6) / total * 100
nps_score = promoters - detractors
# Range: -100 to +100
```

---

### 2. Data Collector

**Purpose**: Aggregate data from multiple sources and compute cross-source sentiment.

```
┌───────────────────────────────────────────────────────────────────────┐
│                         Data Collector                                 │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Source Types:                                                        │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                 │
│  │ SOCIAL_MEDIA │ │ NEWS         │ │ PROPRIETARY  │                 │
│  │ (Twitter,    │ │ (RSS, API)   │ │ (Internal,   │                 │
│  │  Reddit)     │ │              │ │  Survey)     │                 │
│  └──────────────┘ └──────────────┘ └──────────────┘                 │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                 │
│  │ FINANCIAL    │ │ GOVERNMENT   │ │ WEB_SCRAPE   │                 │
│  │ (Stock,      │ │ (Census,     │ │ (Competitor  │                 │
│  │  Earnings)   │ │  BLS, SEC)   │ │  websites)   │                 │
│  └──────────────┘ └──────────────┘ └──────────────┘                 │
│                                                                       │
│  Data Flow:                                                          │
│  ┌──────────┐    ┌────────────┐    ┌────────────┐    ┌──────────┐   │
│  │ Sources  │───→│ Validation │───→│  Storage   │───→│Aggregatn │   │
│  │ Registerd│    │ & Cleaning │    │ & Indexing │    │& Sentimnt│   │
│  └──────────┘    └────────────┘    └────────────┘    └──────────┘   │
│                                                                       │
│  Sentiment Scoring:                                                   │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ score >= 0.75  → VERY_POSITIVE                                  │  │
│  │ score >= 0.55  → POSITIVE                                       │  │
│  │ score >= 0.45  → NEUTRAL                                        │  │
│  │ score >= 0.25  → NEGATIVE                                       │  │
│  │ score <  0.25  → VERY_NEGATIVE                                  │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Source Reliability:                                                  │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ Each source carries a reliability weight (0.0-1.0)              │  │
│  │ Used to weight aggregation when combining sources               │  │
│  │ Higher reliability = more influence on final sentiment          │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Public API:                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ register_source(name, type, reliability)                        │  │
│  │ collect(source_name, topic, data_records)                       │  │
│  │ get_data(source_name, topic) → List[DataRecord]                 │  │
│  │ aggregate_sentiment(topic) → SentimentResult                    │  │
│  │ get_source_stats() → Dict[str, SourceStats]                     │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────┘
```

**Aggregation Algorithm**:
```python
def aggregate_sentiment(topic):
    records = get_all_records(topic)
    if not records:
        return SentimentResult(label=NEUTRAL, score=0.5, volume=0)

    weighted_sum = 0
    total_weight = 0
    keywords = set()

    for record in records:
        source_reliability = sources[record.source].reliability
        weight = source_reliability
        weighted_sum += record.sentiment_score * weight
        total_weight += weight
        keywords.update(record.keywords)

    avg_score = weighted_sum / total_weight if total_weight > 0 else 0.5
    label = classify_sentiment(avg_score)

    return SentimentResult(
        label=label,
        score=avg_score,
        volume=len(records),
        keywords=list(keywords)
    )
```

---

### 3. Trend Analyzer

**Purpose**: Detect trends from time-series data using statistical methods.

```
┌───────────────────────────────────────────────────────────────────────┐
│                          Trend Analyzer                                │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Public API:                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ add_data_point(metric_name, timestamp, value)                   │  │
│  │ detect_trends(metric_name) → List[Trend]                        │  │
│  │ get_trend_summary() → Dict[str, TrendSummary]                   │  │
│  │ list_trends() → List[Trend]                                     │  │
│  │ get_data_points(metric_name) → List[DataPoint]                  │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Trend Classification:                                                │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ slope > 0.10   → GROWTH      (strong positive)                 │  │
│  │ slope > 0.02   → EMERGING    (moderate positive)                │  │
│  │ slope < -0.10  → DECLINING   (strong negative)                  │  │
│  │ slope < -0.02  → STABLE      (moderate negative)                │  │
│  │ otherwise      → MATURING    (flat / plateau)                   │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Trend Detection Algorithm:                                            │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ 1. Sort time series chronologically by timestamp                │  │
│  │ 2. Compute linear regression slope (least squares)              │  │
│  │ 3. Normalize slope relative to average value                    │  │
│  │ 4. Calculate volatility via standard deviation of returns       │  │
│  │ 5. Compute growth rate: (last - first) / first * 100           │  │
│  │ 6. Confidence = min(1, n/20) * (1 - volatility)               │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Internal State:                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ _data_points: Dict[str, List[DataPoint]]                        │  │
│  │ _trends: Dict[str, List[Trend]]                                 │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────┘
```

**Linear Regression Algorithm**:
```python
def linear_regression(timestamps, values):
    n = len(values)
    x = [(t - timestamps[0]).total_seconds() for t in timestamps]
    y = values

    x_mean = sum(x) / n
    y_mean = sum(y) / n

    numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    denominator = sum((x[i] - x_mean) ** 2 for i in range(n))

    slope = numerator / denominator if denominator != 0 else 0
    intercept = y_mean - slope * x_mean

    # Normalize slope
    avg_value = y_mean if y_mean != 0 else 1
    normalized_slope = slope / avg_value

    return normalized_slope, intercept
```

---

### 4. Competitive Landscape

**Purpose**: Map competitors, generate SWOT analyses, and assess market threats.

```
┌───────────────────────────────────────────────────────────────────────┐
│                     Competitive Landscape                              │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Position Types:                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ LEADER     (>25% share, strong brand, market definer)           │  │
│  │ CHALLENGER (>15% share, growing fast, taking share)             │  │
│  │ FOLLOWER   (<10% share, stable, copying leaders)                │  │
│  │ NICHE      (<5% share, specialized, loyal base)                 │  │
│  │ EMERGING   (<2% share, new entrant, disruptive potential)       │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Threat Scoring:                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ threat_level = 0                                                │  │
│  │ + 3 if market_share > 0.20                                      │  │
│  │ + 2 if market_share > 0.10                                      │  │
│  │ + 1 if market_share > 0.05                                      │  │
│  │ + 2 if growth_rate > 15%                                        │  │
│  │ + 1 if growth_rate > 5%                                         │  │
│  │ + 1 if sentiment_score > 0.7                                    │  │
│  │ → min(5, total)                                                 │  │
│  │                                                                 │  │
│  │ Threat Levels:                                                  │  │
│  │ 5 = Critical (direct competitor, high share, growing)           │  │
│  │ 4 = High                                                         │  │
│  │ 3 = Medium                                                       │  │
│  │ 2 = Low                                                          │  │
│  │ 1 = Minimal                                                      │  │
│  │ 0 = None                                                         │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Public API:                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ add_competitor(name, market_share, strengths, weaknesses, pos)  │  │
│  │ generate_swot(competitor_id) → Dict                             │  │
│  │ competitive_matrix() → List[Dict]                               │  │
│  │ get_threat_assessment() → List[Threat]                          │  │
│  │ list_competitors() → List[Competitor]                           │  │
│  │ update_competitor(competitor_id, **kwargs)                      │  │
│  │ remove_competitor(competitor_id)                                │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Internal State:                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ _competitors: Dict[str, Competitor]                             │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────┘
```

**SWOT Generation**:
```python
def generate_swot(competitor):
    return {
        "competitor": competitor.name,
        "strengths": competitor.strengths,
        "weaknesses": competitor.weaknesses,
        "opportunities": infer_opportunities(competitor),
        "threats": infer_threats(competitor),
        "position": competitor.position.value,
        "market_share": competitor.market_share
    }
```

---

### 5. Forecast Engine

**Purpose**: Generate forecasts using statistical methods.

```
┌───────────────────────────────────────────────────────────────────────┐
│                         Forecast Engine                                │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Methods:                                                             │
│  ┌────────────────┬───────────────────┬──────────────────────────┐   │
│  │ Method         │ Algorithm          │ Best For                 │   │
│  ├────────────────┼───────────────────┼──────────────────────────┤   │
│  │ Moving Average │ Windowed mean      │ Stable, low-volatility   │   │
│  │ Exp. Smoothing │ Weighted recursive │ Trends, recent emphasis  │   │
│  │ Linear Regr.   │ OLS line fitting   │ Consistent trends        │   │
│  └────────────────┴───────────────────┴──────────────────────────┘   │
│                                                                       │
│  Confidence Interval:                                                 │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ Based on average absolute error of fitted values                │  │
│  │ lower = predicted - error_margin                                │  │
│  │ upper = predicted + error_margin                                │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Accuracy Score:                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ accuracy = 1 - MAPE (Mean Absolute Percentage Error)            │  │
│  │ MAPE = mean(|actual - predicted| / actual) * 100               │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Public API:                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ moving_average(metric, values, window) → ForecastResult         │  │
│  │ exponential_smoothing(metric, values, alpha) → ForecastResult   │  │
│  │ linear_regression(metric, values) → ForecastResult              │  │
│  │ get_forecast(metric) → ForecastResult                           │  │
│  │ list_forecasts() → List[ForecastResult]                         │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────┘
```

**Moving Average**:
```python
def moving_average(values, window=3):
    predicted = []
    for i in range(window, len(values)):
        avg = sum(values[i-window:i]) / window
        predicted.append(avg)
    return predicted
```

**Exponential Smoothing**:
```python
def exponential_smoothing(values, alpha=0.3):
    result = [values[0]]
    for i in range(1, len(values)):
        smoothed = alpha * values[i] + (1 - alpha) * result[-1]
        result.append(smoothed)
    return result
```

---

### 6. Market Size Estimator

**Purpose**: Estimate market opportunity using TAM/SAM/SOM framework.

```
┌───────────────────────────────────────────────────────────────────────┐
│                      Market Size Estimator                             │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  TAM/SAM/SOM Framework:                                               │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                                                                 │  │
│  │  TAM (Total Addressable Market)                                 │  │
│  │  └── SAM (Serviceable Addressable Market)                       │  │
│  │       └── SOM (Serviceable Obtainable Market)                   │  │
│  │                                                                 │  │
│  │  Example:                                                       │  │
│  │  TAM = $50B (entire market)                                     │  │
│  │  SAM = $50B * 0.30 = $15B (addressable segment)                │  │
│  │  SOM = $15B * 0.10 = $1.5B (realistic capture)                 │  │
│  │                                                                 │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Forward Projection:                                                  │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ Compound growth over N years:                                    │  │
│  │ future_value = current_value * (1 + growth_rate/100) ^ years    │  │
│  │                                                                 │  │
│  │ Example (15% CAGR, 5 years):                                    │  │
│  │ Year 0: $1.5B                                                   │  │
│  │ Year 1: $1.73B                                                  │  │
│  │ Year 2: $1.98B                                                  │  │
│  │ Year 3: $2.28B                                                  │  │
│  │ Year 4: $2.62B                                                  │  │
│  │ Year 5: $3.02B                                                  │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Public API:                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ estimate(segment, tam, sam_pct, som_pct, growth) → MarketSize   │  │
│  │ project_forward(segment, years) → List[YearProjection]          │  │
│  │ get_estimate(segment) → MarketSize                              │  │
│  │ list_estimates() → List[MarketSize]                             │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────┘
```

---

### 7. Report Generator

**Purpose**: Compile research findings into structured reports.

```
┌───────────────────────────────────────────────────────────────────────┐
│                       Report Generator                                 │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Report Structure:                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ Report                                                          │  │
│  │ ├── Title                                                       │  │
│  │ ├── Executive Summary                                           │  │
│  │ ├── Sections[]                                                  │  │
│  │ │   ├── Section Title                                           │  │
│  │ │   ├── Content (text)                                          │  │
│  │ │   └── Data (charts, tables)                                   │  │
│  │ ├── Findings[]                                                  │  │
│  │ │   └── Key insight string                                      │  │
│  │ ├── Recommendations[]                                           │  │
│  │ │   └── Actionable item string                                  │  │
│  │ ├── Data Sources[]                                              │  │
│  │ │   └── Source name string                                      │  │
│  │ └── Generated Timestamp                                         │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Report Types:                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ MARKET_ANALYSIS  → market overview, size, trends, competitors   │  │
│  │ COMPETITIVE      → competitor deep-dive, SWOT, positioning      │  │
│  │ CUSTOMER         → survey results, sentiment, needs             │  │
│  │ PRODUCT_LAUNCH   → market fit, positioning, go-to-market        │  │
│  │ QUARTERLY        → KPIs, trends, competitive changes            │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
│  Public API:                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ generate_report(title, summary, findings, recs) → Report        │  │
│  │ add_section(report_id, title, content) → Section                │  │
│  │ get_report(report_id) → Report                                  │  │
│  │ list_reports() → List[Report]                                   │  │
│  │ export_report(report_id, format) → str                          │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow: Full Research Cycle

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Collect    │───→│   Analyze    │───→│   Compare    │───→│   Forecast   │
│    Data      │    │  Sentiment   │    │  Competitor  │    │    Future    │
│              │    │              │    │              │    │              │
│ - surveys    │    │ - sentiment  │    │ - SWOT       │    │ - moving avg │
│ - social     │    │ - keywords   │    │ - position   │    │ - exp smooth │
│ - news       │    │ - trends     │    │ - threats    │    │ - lin reg    │
│ - financial  │    │ - volume     │    │ - matrix     │    │ - confidence │
└──────────────┘    └──────────────┘    └──────────────┘    └──────┬───────┘
                                                                   │
┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  Optimize    │←───│   Generate   │←───│    Size      │←─────────┘
│  Strategy    │    │   Report     │    │   Market     │
│              │    │              │    │              │
│ - recs       │    │ - sections   │    │ - TAM/SAM   │
│ - insights   │    │ - findings   │    │ - SOM        │
│ - next steps │    │ - export     │    │ - projection │
└──────────────┘    └──────────────┘    └──────────────┘
```

**Complete Research Workflow**:
```python
oracle = MarketResearchOracle()

# 1. Collect data
oracle.data_collector.collect("twitter", "AI productivity", [...])
oracle.data_collector.collect("news", "AI productivity", [...])

# 2. Analyze sentiment
sentiment = oracle.data_collector.aggregate_sentiment("AI productivity")

# 3. Detect trends
oracle.trends.add_data_point("ai_market", datetime(2025, 1, 1), 100)
oracle.trends.add_data_point("ai_market", datetime(2025, 6, 1), 180)
trends = oracle.trends.detect_trends("ai_market")

# 4. Map competitors
oracle.competitive.add_competitor("LeaderCorp", 0.30, [...], [...])
oracle.competitive.add_competitor("ChallengerAI", 0.15, [...], [...])
threats = oracle.competitive.get_threat_assessment()

# 5. Generate forecasts
oracle.forecast.linear_regression("ai_market", [100, 130, 170, 220])

# 6. Size market
oracle.market_size.estimate("AI Tools", 30_000_000_000, 0.2, 0.05, 25)

# 7. Generate report
report = oracle.reports.generate_report(
    "AI Market Analysis Q2 2025",
    "Strong growth with emerging competition.",
    ["Market growing 24.5% YoY", "3 competitors dominate 60% share"],
    ["Invest in R&D", "Partner with distribution leader"]
)
```

---

## Design Patterns

| Pattern | Where | Purpose |
|---------|-------|---------|
| Builder | SurveyBuilder | Step-by-step survey construction |
| Strategy | ForecastEngine | Pluggable forecasting methods |
| Observer | DataCollector | Source registration callbacks |
| Facade | MarketResearchOracle | Unified interface to subsystems |
| Repository | Internal stores | Data access abstraction |
| Value Object | Data classes | Immutable data transfer |
| Factory Method | Source registration | Create source-specific handlers |
| Composite | Report sections | Assemble report from parts |

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Language | Python 3.10+ | Core runtime |
| Data Classes | dataclasses, typing | Structured data models |
| Enums | enum.Enum | Type-safe constants |
| Math | math, statistics | Regression, std dev, sqrt |
| Logging | logging module | Audit trail and debugging |
| ID Generation | uuid4 | Unique identifiers |
| Date/Time | datetime, timedelta | Time-based operations |
| Regex | re | Pattern matching |
| JSON | json | Serialization |

---

## Scalability Considerations

| Dimension | Approach | Threshold |
|-----------|---------|-----------|
| Survey Volume | In-memory with configurable persistence | 1K surveys |
| Time Series | Append-only with windowed analysis | 1M data points |
| Competitor Profiles | Hash-based lookup, lazy SWOT | 500 competitors |
| Forecast Computation | On-demand with result caching | 100 forecasts/day |
| Report Generation | Template-based with section assembly | 50 reports/day |
| Sentiment Analysis | Batch processing with streaming | 100K records/hour |
| Data Source Scaling | Connection pooling, rate limiting | 50 sources |

**Performance Optimizations**:
1. **Lazy SWOT**: Computed on-demand, not on every competitor update
2. **Forecast Caching**: Results cached by metric + method + input hash
3. **Batch Sentiment**: Process records in batches for efficiency
4. **Incremental Reports**: Build from pre-analyzed sections
5. **Windowed Time Series**: Old data archived, recent data in memory

---

## Security

| Concern | Approach | Implementation |
|---------|----------|----------------|
| Respondent Privacy | Anonymized IDs, no PII in analysis | UUID-based respondent IDs |
| Data Source Credentials | Environment variables | os.environ.get() |
| Competitor Data | Public sources only | Source type validation |
| Report Access | Role-based access control | Permission checks |
| Survey Data | Encrypted at rest | AES-256 encryption |
| API Keys | Rotated quarterly | Key rotation policy |
| Data Export | Audit logging | Track all exports |

---

## Error Handling

```
ResearchError (base)
├── SurveyError
│   ├── SurveyNotFoundError
│   ├── QuestionNotFoundError
│   └── ResponseValidationError
├── InsufficientDataError
│   └── Raised when < minimum data threshold
├── InvalidForecastError
│   └── Raised when data incompatible with method
├── DataSourceError
│   └── Raised when source unavailable or invalid
├── CompetitorNotFoundError
│   └── Raised when competitor_id not found
└── ReportError
    └── Raised when report generation fails
```

**Error Handling Strategy**:
- All public methods validate inputs before computation
- Statistical methods require minimum data thresholds
- Descriptive error messages with suggested fixes
- Errors logged with context for debugging
- Graceful degradation when data is incomplete

---

## Testing Strategy

| Component | Approach | Coverage Target |
|-----------|---------|-----------------|
| Survey Builder | Question type coverage, response validation | 95% |
| Data Collector | Source registration, aggregation accuracy | 90% |
| Trend Analyzer | Known-curve detection, edge cases | 95% |
| Competitive Landscape | SWOT generation, threat scoring | 90% |
| Forecast Engine | Method accuracy on known data | 95% |
| Market Size Estimator | Formula validation, projection accuracy | 90% |
| Report Generator | Template rendering, section assembly | 90% |

**Test Data**:
- Synthetic time series with known trends for trend detection validation
- Pre-defined competitor data for SWOT accuracy testing
- Historical data with known forecasts for model validation
- Survey responses with known distributions for analytics testing
