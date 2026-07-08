# Market Research Oracle Architecture

## Overview

The Market Research Oracle is a modular research intelligence system that combines survey design, multi-source data collection, sentiment analysis, trend detection, competitive landscape mapping, statistical forecasting, and market sizing into a unified platform. Each subsystem operates independently and exposes a clean API, while the top-level orchestrator coordinates cross-module workflows.

---

## System Context

```
┌──────────────────────────────────────────────────────────────────┐
│                       External Data Sources                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ Social   │ │  News    │ │Financial │ │Government│           │
│  │ Media    │ │  Feeds   │ │  APIs    │ │  Data    │           │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘           │
│       │            │            │            │                    │
│  ┌────▼────────────▼────────────▼────────────▼─────┐            │
│  │              Data Collector                      │            │
│  └──────────────────┬──────────────────────────────┘            │
│                     │                                            │
│  ┌──────────────────▼──────────────────────────────┐            │
│  │           Market Research Oracle Core            │            │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │            │
│  │  │ Survey   │ │  Trend   │ │Competitve│        │            │
│  │  │ Builder  │ │ Analyzer │ │Landscape │        │            │
│  │  └──────────┘ └──────────┘ └──────────┘        │            │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │            │
│  │  │Forecast  │ │Market    │ │ Report   │        │            │
│  │  │ Engine   │ │Size Est. │ │Generator │        │            │
│  │  └──────────┘ └──────────┘ └──────────┘        │            │
│  └─────────────────────────────────────────────────┘            │
│                     │                                            │
│  ┌──────────────────▼──────────────────────────────┐            │
│  │              Data Layer                          │            │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │            │
│  │  │ Survey   │ │ Time     │ │Competitor│        │            │
│  │  │ Responses│ │ Series   │ │ Profiles │        │            │
│  │  └──────────┘ └──────────┘ └──────────┘        │            │
│  └─────────────────────────────────────────────────┘            │
└──────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. Survey Builder

**Purpose**: Design surveys, collect responses, and compute per-question analytics.

```
┌─────────────────────────────────────┐
│          Survey Builder             │
├─────────────────────────────────────┤
│  create_survey(title, desc)         │
│  add_question(survey_id, text, type)│
│  submit_response(survey_id, answers)│
│  analyze_survey(survey_id)          │
│  list_surveys()                     │
├─────────────────────────────────────┤
│  Question Types:                    │
│  ┌──────────────────────────────┐   │
│  │ MULTIPLE_CHOICE | OPEN_ENDED │   │
│  │ RATING | RANKING | NPS       │   │
│  │ BINARY | LIKERT | DEMOGRAPHIC│   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
```

**Analysis per question type**:
- Rating: mean, min, max, count
- Multiple Choice: frequency distribution
- NPS: promoter/detractor split, NPS score
- Open-ended: raw response list

---

### 2. Data Collector

**Purpose**: Aggregate data from multiple sources and compute cross-source sentiment.

```
Sources → Validation → Storage → Aggregation → Sentiment
```

**Sentiment Scoring**:
```
score >= 0.75  → VERY_POSITIVE
score >= 0.55  → POSITIVE
score >= 0.45  → NEUTRAL
score >= 0.25  → NEGATIVE
score <  0.25  → VERY_NEGATIVE
```

**Source Reliability**: Each source carries a reliability weight (0.0-1.0) used to weight aggregation.

---

### 3. Trend Analyzer

**Purpose**: Detect trends from time-series data using statistical methods.

```
┌─────────────────────────────────────┐
│          Trend Analyzer             │
├─────────────────────────────────────┤
│  add_data_point(metric, time, val)  │
│  detect_trends(metric_name)         │
│  get_trend_summary()                │
├─────────────────────────────────────┤
│  Trend Classification:             │
│  ┌──────────────────────────────┐   │
│  │ slope > 0.1   → GROWTH      │   │
│  │ slope > 0.02  → EMERGING    │   │
│  │ slope < -0.1  → DECLINING   │   │
│  │ slope < -0.02 → STABLE      │   │
│  │ otherwise     → MATURING    │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
```

**Trend Detection Algorithm**:
1. Sort time series chronologically
2. Compute linear regression slope
3. Normalize slope relative to average value
4. Calculate volatility via standard deviation of returns
5. Confidence = min(1, n/20) * (1 - volatility)

---

### 4. Competitive Landscape

**Purpose**: Map competitors, generate SWOT analyses, and assess market threats.

```
┌─────────────────────────────────────────────────┐
│             Competitive Landscape               │
├─────────────────────────────────────────────────┤
│  add_competitor(name, share, strengths, weaks)  │
│  generate_swot(competitor_id)                   │
│  competitive_matrix()                           │
│  get_threat_assessment()                        │
├─────────────────────────────────────────────────┤
│  Position Types:                                │
│  LEADER    (>25% share, strong brand)           │
│  CHALLENGER (>15% share, growing fast)          │
│  FOLLOWER  (<10% share, stable)                 │
│  NICHE     (<5% share, specialized)             │
│  EMERGING  (<2% share, new entrant)             │
└─────────────────────────────────────────────────┘
```

**Threat Scoring**:
```
threat_level = 0
+ 3 if market_share > 0.20
+ 2 if market_share > 0.10
+ 1 if market_share > 0.05
+ 2 if growth_rate > 15%
+ 1 if growth_rate > 5%
+ 1 if sentiment_score > 0.7
→ min(5, total)
```

---

### 5. Forecast Engine

**Purpose**: Generate forecasts using statistical methods.

**Methods**:

| Method | Algorithm | Best For |
|--------|-----------|----------|
| Moving Average | Windowed mean | Stable, low-volatility data |
| Exponential Smoothing | Weighted recursive | Data with trends, recent emphasis |
| Linear Regression | OLS line fitting | Consistent upward/downward trends |

**Confidence Interval**: Based on average absolute error of fitted values.

**Accuracy Score**: 1 - MAPE (Mean Absolute Percentage Error).

---

### 6. Market Size Estimator

**Purpose**: Estimate market opportunity using TAM/SAM/SOM framework.

```
TAM (Total Addressable Market)
  └── SAM (Serviceable Addressable Market)
       └── SOM (Serviceable Obtainable Market)

Example:
  TAM = $50B (entire market)
  SAM = $50B * 0.30 = $15B (addressable segment)
  SOM = $15B * 0.10 = $1.5B (realistic capture)
```

**Forward Projection**: Compound growth over N years.

---

### 7. Report Generator

**Purpose**: Compile research findings into structured reports.

```
Report Structure:
├── Title
├── Executive Summary
├── Sections (title + content + data)
├── Findings (list of key insights)
├── Recommendations (actionable items)
├── Data Sources
└── Generated Timestamp
```

---

## Data Flow: Full Research Cycle

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Collect  │───→│ Analyze  │───→│ Compare  │───→│ Forecast │
│   Data   │    │ Sentiment│    │Competitor│    │  Future  │
└──────────┘    └──────────┘    └──────────┘    └─────┬────┘
                                                       │
┌──────────┐    ┌──────────┐    ┌──────────┐          │
│ Optimize │←───│ Generate │←───│   Size   │←─────────┘
│ Strategy │    │ Report   │    │ Market   │
└──────────┘    └──────────┘    └──────────┘
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

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Data Classes | dataclasses, typing |
| Enums | enum.Enum |
| Math | math, statistics |
| Logging | logging module |
| ID Generation | uuid |
| Date/Time | datetime, timedelta |

---

## Scalability Considerations

| Dimension | Approach |
|-----------|---------|
| Survey Volume | In-memory with configurable persistence |
| Time Series | Append-only with windowed analysis |
| Competitor Profiles | Hash-based lookup, lazy SWOT computation |
| Forecast Computation | On-demand with result caching |
| Report Generation | Template-based with section assembly |

---

## Security

| Concern | Approach |
|---------|----------|
| Respondent Privacy | Anonymized IDs, no PII in analysis |
| Data Source Credentials | Environment variables |
| Competitor Data | Public sources only |
| Report Access | Role-based access control |

---

## Error Handling

```
ResearchError (base)
├── SurveyError
├── InsufficientDataError
└── InvalidForecastError
```

All public methods validate inputs before computation. Statistical methods require minimum data thresholds and raise `InsufficientDataError` or `InvalidForecastError` when constraints are not met.
