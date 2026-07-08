# Competitive Intelligence Agent — Architecture

## 1. Overview

The Competitive Intelligence Agent is a market analysis and competitor tracking system designed to gather, analyze, and distribute actionable intelligence for strategic decision-making. It combines structured SWOT analysis, trend detection from streaming data, multi-metric benchmarking, and intelligence collection into a unified competitive intelligence platform.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                  COMPETITIVE INTELLIGENCE AGENT v3.0                    │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                      ANALYTICS LAYER                              │  │
│  │  ┌──────────┐ ┌──────────────┐ ┌──────────┐ ┌────────────────┐  │  │
│  │  │ Competitor│ │    SWOT      │ │  Trend   │ │  Benchmark     │  │  │
│  │  │ Profiler  │ │   Analyzer   │ │ Monitor  │ │   Engine       │  │  │
│  │  └────┬─────┘ └──────┬───────┘ └────┬─────┘ └───────┬────────┘  │  │
│  │       │              │              │               │             │  │
│  │  ┌────┴─────┐ ┌──────┴───────┐ ┌────┴─────┐ ┌──────┴────────┐  │  │
│  │  │  Intel   │ │   Market     │ │ Strategic│ │  Pricing      │  │  │
│  │  │Collector │ │  Research    │ │  Brief   │ │  Analyzer     │  │  │
│  │  └──────────┘ └──────────────┘ └──────────┘ └───────────────┘  │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                    │                                    │
│  ┌─────────────────────────────────┴──────────────────────────────────┐  │
│  │                         DATA LAYER                                 │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │  │
│  │  │Competitor│ │  Intel   │ │  Trend   │ │Benchmark │            │  │
│  │  │Profiles  │ │ Reports  │ │  Store   │ │ Metrics  │            │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
```

## 2. System Components

### 2.1 Competitor Profiler
- Maintains detailed competitor profiles (revenue, products, technologies, people)
- Tracks competitor types (direct, indirect, emerging, substitute)
- Monitors threat levels and recent strategic moves
- Supports tagging and categorization
- Revenue and valuation tracking
- Executive team mapping

### 2.2 SWOT Analyzer
- Performs structured Strengths/Weaknesses/Opportunities/Threats analysis
- Internal/external factor categorization
- Overall score calculation from factor balance
- Strategic priority determination (offensive, competitive, defensive, survival)
- Cross-competitor SWOT comparison
- SO/WO/ST/WT strategy generation
- Factor library for inference when data is sparse

### 2.3 Trend Monitor
- Ingests streaming data points with topic/source/sentiment
- Groups data by topic and analyzes sentiment distribution
- Detects trend direction (rising, stable, declining, emerging, disruptive)
- Calculates impact scores based on data point volume and sentiment delta
- Confidence levels based on data point count

### 2.4 Benchmark Engine
- Multi-metric competitive benchmarking
- Ranking calculation across competitor sets
- Overall competitive scoring (market_leader → laggard)
- Feature comparison matrix generation
- Pricing analysis with market positioning

### 2.5 Intelligence Collector
- Multi-source intelligence ingestion (news, patents, filings, reviews)
- Full-text search with keyword, competitor, and category filters
- Confidence level tracking per report
- Source and freshness metadata
- Priority-based intelligence triage

### 2.6 Market Research Engine
- TAM/SAM/SOM market sizing
- Entry barrier analysis
- Feasibility scoring
- Research report persistence

### 2.7 Strategic Brief Generator
- Executive-level intelligence summaries
- Landscape overview with threat distribution
- Trend summary with direction counts
- Actionable recommendations from data patterns

## 3. Data Flow

```
┌─────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ External │───>│Intelligence│───>│   SWOT   │───>│Strategic │
│ Sources  │    │ Collector │    │ Analyzer │    │  Brief   │
└─────────┘    └────┬─────┘    └──────────┘    └──────────┘
                    │
                    v
             ┌──────────┐    ┌──────────┐
             │  Trend   │───>│Benchmark │
             │ Monitor  │    │  Engine  │
             └──────────┘    └────┬─────┘
                                  │
                                  v
                           ┌──────────┐
                           │ Market   │
                           │ Research │
                           └──────────┘
```

### 3.1 Detailed Intelligence Lifecycle

1. **Collection**: Raw intelligence gathered from multiple sources
2. **Categorization**: Tagged by competitor, category, source type
3. **Analysis**: SWOT evaluation, trend detection, benchmark comparison
4. **Synthesis**: Findings aggregated into strategic insights
5. **Distribution**: Briefs and dashboards delivered to stakeholders
6. **Feedback Loop**: New intelligence triggers re-analysis

## 4. Design Patterns

### 4.1 Observer Pattern
The `TrendMonitor` observes incoming data points, grouping by topic and detecting sentiment shifts. Multiple trend detection strategies can subscribe to the same data stream.

### 4.2 Strategy Pattern
SWOT analysis supports multiple analytical frameworks (basic SWOT, Porter's Five Forces, PESTEL) through interchangeable strategy objects.

### 4.3 Composite Pattern
Competitive landscapes are composed of individual competitor profiles, each containing products, technologies, and intelligence reports.

### 4.4 Chain of Responsibility
Intelligence reports flow through a chain: collection → categorization → analysis → synthesis, with each stage enriching the data.

### 4.5 Repository Pattern
`IntelligenceCollector` acts as a repository, providing search, filtering, and retrieval over collected intelligence reports.

### 4.6 Builder Pattern
Competitor profiles and benchmark configurations are built incrementally through separate method calls.

### 4.7 Facade Pattern
The `CompetitiveIntelAgent` orchestrator provides a simplified interface over the complex subsystem of analyzers, monitors, and collectors.

## 5. Component Deep Dive

### 5.1 SWOT Analysis Framework

```
┌─────────────────────────────────────────────────────┐
│                 SWOT Analysis Matrix                 │
├──────────────────────┬──────────────────────────────┤
│      POSITIVE        │        NEGATIVE              │
├──────────────────────┼──────────────────────────────┤
│                      │                              │
│   ┌──────────────┐   │   ┌──────────────┐          │
│   │  STRENGTHS   │   │   │  WEAKNESSES  │          │
│   │  (Internal)  │   │   │  (Internal)  │          │
│   │              │   │   │              │          │
│   │ • Tech adv.  │   │   │ • Legacy     │          │
│   │ • Brand      │   │   │ • Scale      │          │
│   │ • Team       │   │   │ • Costs      │          │
│   └──────────────┘   │   └──────────────┘          │
│                      │                              │
│   ┌──────────────┐   │   ┌──────────────┐          │
│   │OPPORTUNITIES │   │   │   THREATS    │          │
│   │  (External)  │   │   │  (External)  │          │
│   │              │   │   │              │          │
│   │ • Growth     │   │   │ • New entrant│          │
│   │ • Partners   │   │   │ • Regulation │          │
│   │ • Expansion  │   │   │ • Economy    │          │
│   └──────────────┘   │   └──────────────┘          │
│                      │                              │
└──────────────────────┴──────────────────────────────┘

Score = (Strengths + Opportunities) / Total Factors
```

### 5.2 Trend Detection Algorithm

```
Data Points by Topic
         │
         v
┌─────────────────────┐
│ Group by Topic      │
│ Count by Sentiment  │
├─────────────────────┤
│ positive: N_p       │
│ negative: N_n       │
│ neutral:  N_u       │
└──────────┬──────────┘
           │
           v
┌─────────────────────────────────┐
│ Calculate Ratios                │
│ R_pos = N_p / Total             │
│ R_neg = N_n / Total             │
└──────────┬──────────────────────┘
           │
           v
┌─────────────────────────────────┐
│ Determine Direction             │
│ R_pos > 0.6 → RISING           │
│ R_neg > 0.6 → DECLINING        │
│ R_pos > 0.4 & R_neg < 0.2     │
│                → EMERGING       │
│ Otherwise → STABLE              │
└──────────┬──────────────────────┘
           │
           v
┌─────────────────────────────────┐
│ Impact = |R_pos - R_neg|        │
│ Confidence = f(data_points)     │
└─────────────────────────────────┘
```

### 5.3 Benchmark Ranking System

```
┌─────────────────────────────────────────────────┐
│              Benchmark Ranking                   │
├─────────────────────────────────────────────────┤
│                                                 │
│  Metric: API Response Time (lower is better)    │
│                                                 │
│  Our Company:    45ms  ←──── Rank 1             │
│  Competitor A:   60ms  ←──── Rank 2             │
│  Industry Avg:   80ms  ←──── Rank 3             │
│  Competitor B:  120ms  ←──── Rank 4             │
│                                                 │
│  Score = 1 - (our_position / total_positions)  │
│        = 1 - (1 / 4) = 0.75                    │
│                                                 │
│  Position: market_leader (≥ 0.8)                │
│            strong_contender (≥ 0.6)             │
│            competitive (≥ 0.4)                  │
│            challenger (≥ 0.2)                   │
│            laggard (< 0.2)                      │
└─────────────────────────────────────────────────┘
```

## 6. Tech Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Language | Python 3.10+ | Data analysis, type hints |
| Data Models | dataclasses | Typed, serializable structures |
| Analysis | Custom algorithms | SWOT scoring, trend detection |
| Search | In-memory full-text | Fast keyword matching |
| Serialization | dict/to_dict | JSON-compatible output |
| Trend Detection | Statistical | Sentiment ratio analysis |
| Logging | Python logging | Structured observability |

## 7. Security Considerations

### 7.1 Data Sensitivity
- Competitive intelligence may contain sensitive market data
- No persistence to unencrypted storage
- Source attribution tracked for accountability
- Confidence levels indicate data reliability

### 7.2 Source Verification
- Each intelligence report tagged with source type
- Verification status tracked (verified/unverified)
- Confidence levels guide decision-making weight
- Freshness metadata prevents stale data usage

### 7.3 Ethical Intelligence
- All data collection from public sources
- No industrial espionage or unauthorized access
- Compliance with fair competition regulations
- Transparent methodology documentation

## 8. Scalability

### 8.1 Current Architecture
- In-memory stores limit to ~10,000 intelligence reports
- Competitor profiles: ~500 concurrently
- Trend detection on ~100,000 data points

### 8.2 Scaling Strategies
- **Database backend**: PostgreSQL for persistent storage
- **Search engine**: Elasticsearch for full-text search at scale
- **Streaming pipeline**: Kafka for real-time data ingestion
- **ML integration**: NLP models for automated sentiment analysis
- **API layer**: REST API for external system integration

## 9. Integration Points

```
┌─────────────────┐     ┌──────────────────┐
│ CI Agent        │────>│ News APIs        │
│                 │     │ (NewsAPI, GNews)  │
└────────┬────────┘     └──────────────────┘
         │
         ├────────────>┌──────────────────┐
         │             │ Financial Data   │
         │             │ (Crunchbase,     │
         │             │  PitchBook)      │
         │             └──────────────────┘
         │
         ├────────────>┌──────────────────┐
         │             │ Social Media     │
         │             │ (Twitter,        │
         │             │  LinkedIn API)   │
         │             └──────────────────┘
         │
         ├────────────>┌──────────────────┐
         │             │ Patent Databases │
         │             │ (Google Patents) │
         │             └──────────────────┘
         │
         └────────────>┌──────────────────┐
                       │ Industry Reports │
                       │ (Gartner, IDC)   │
                       └──────────────────┘
```

## 10. Error Handling

| Error Type | Handling Strategy |
|-----------|-------------------|
| Competitor not found | Return error with available IDs |
| Invalid framework | Return supported frameworks list |
| Insufficient data points | Return "insufficient_data" trend |
| Empty benchmark category | Return empty rankings with zero score |
| Source unreachable | Skip source, continue with others |
| Duplicate intelligence | Dedup by title + source + date |
| Invalid enum value | Fall back to default enum member |

## 11. Performance

| Metric | Target | Notes |
|--------|--------|-------|
| Competitor add | < 20ms | Profile creation |
| SWOT analysis | < 50ms | Single subject |
| Trend detection | < 200ms | 10K data points |
| Benchmark ranking | < 100ms | 10 metrics x 10 competitors |
| Intelligence search | < 100ms | 10K reports |
| Strategic brief | < 1s | Full dashboard generation |

## 12. Testing Strategy

### Unit Tests
- SWOT scoring accuracy and edge cases
- Trend direction detection correctness
- Benchmark ranking calculations
- Intelligence search filtering
- Threat assessment scoring

### Integration Tests
- Competitor → Analysis → Brief pipeline
- Trend detection from real data sequences
- Multi-competitor benchmark comparison
- Intelligence collection and retrieval cycle

### Acceptance Tests
- End-to-end competitive analysis scenario
- Trend detection accuracy against known patterns
- Brief generation completeness validation
