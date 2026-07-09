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
- Geographic presence analysis
- Market share estimation
- Technology stack profiling
- Patent portfolio tracking
- Customer segment overlap analysis
- Partnership and alliance mapping

### 2.2 SWOT Analyzer
- Performs structured Strengths/Weaknesses/Opportunities/Threats analysis
- Internal/external factor categorization
- Overall score calculation from factor balance
- Strategic priority determination (offensive, competitive, defensive, survival)
- Cross-competitor SWOT comparison
- SO/WO/ST/WT strategy generation
- Factor library for inference when data is sparse
- Confidence scoring based on evidence quality
- Historical SWOT tracking for trend analysis
- Competitive positioning matrix generation

### 2.3 Trend Monitor
- Ingests streaming data points with topic/source/sentiment
- Groups data by topic and analyzes sentiment distribution
- Detects trend direction (rising, stable, declining, emerging, disruptive)
- Calculates impact scores based on data point volume and sentiment delta
- Confidence levels based on data point count
- Multi-topic correlation analysis
- Anomaly detection for sudden shifts
- Industry-specific trend weighting
- Geographic trend variation tracking
- Time-series decomposition for seasonal patterns

### 2.4 Benchmark Engine
- Multi-metric competitive benchmarking
- Ranking calculation across competitor sets
- Overall competitive scoring (market_leader → laggard)
- Feature comparison matrix generation
- Pricing analysis with market positioning
- Performance metric normalization
- Industry benchmark integration
- Historical benchmark trend tracking
- Gap analysis with priority recommendations
- Competitive advantage identification

### 2.5 Intelligence Collector
- Multi-source intelligence ingestion (news, patents, filings, reviews)
- Full-text search with keyword, competitor, and category filters
- Confidence level tracking per report
- Source and freshness metadata
- Priority-based intelligence triage
- Duplicate detection and deduplication
- Source credibility scoring
- Relevance ranking algorithms
- Cross-reference validation
- Automated tagging and categorization

### 2.6 Market Research Engine
- TAM/SAM/SOM market sizing
- Entry barrier analysis
- Feasibility scoring
- Research report persistence
- Market segmentation analysis
- Customer persona development
- Competitive landscape mapping
- Industry trend correlation
- Geographic market analysis
- Regulatory environment assessment

### 2.7 Strategic Brief Generator
- Executive-level intelligence summaries
- Landscape overview with threat distribution
- Trend summary with direction counts
- Actionable recommendations from data patterns
- Risk assessment integration
- Opportunity identification
- Competitive advantage highlighting
- Time-sensitive alert generation
- Custom briefing templates
- Distribution list management

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
7. **Validation**: Cross-reference with multiple sources
8. **Archival**: Historical storage for trend analysis

### 3.2 Data Transformation Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                 Data Transformation Pipeline                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Raw Data                                                   │
│    │                                                        │
│    v                                                        │
│  ┌─────────────┐                                            │
│  │ Validation  │──> Schema check, dedup, normalization      │
│  └──────┬──────┘                                            │
│         v                                                   │
│  ┌─────────────┐                                            │
│  │ Enrichment  │──> Add metadata, source scoring, tagging   │
│  └──────┬──────┘                                            │
│         v                                                   │
│  ┌─────────────┐                                            │
│  │ Analysis    │──> SWOT, trends, benchmarks, scoring       │
│  └──────┬──────┘                                            │
│         v                                                   │
│  ┌─────────────┐                                            │
│  │ Synthesis   │──> Aggregate insights, generate briefs     │
│  └──────┬──────┘                                            │
│         v                                                   │
│  ┌─────────────┐                                            │
│  │ Distribution│──> Alerts, dashboards, reports              │
│  └─────────────┘                                            │
└─────────────────────────────────────────────────────────────┘
```

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

### 4.8 Template Method Pattern
Analysis workflows follow a common template with type-specific variations (e.g., SWOT vs. PESTEL vs. Five Forces).

### 4.9 Singleton Pattern
Configuration manager ensures single instance of system configuration across all components.

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

### 5.4 Intelligence Source Scoring

```
┌─────────────────────────────────────────────────┐
│           Source Credibility Scoring             │
├─────────────────────────────────────────────────┤
│                                                 │
│  Source Type          │ Score │ Weight           │
│  ─────────────────────┼───────┼────────          │
│  SEC Filing           │  10   │ 1.0              │
│  Earnings Call        │   9   │ 1.0              │
│  Patent Database      │   8   │ 0.9              │
│  Industry Report      │   8   │ 0.9              │
│  News Article         │   6   │ 0.7              │
│  Job Postings         │   5   │ 0.6              │
│  Social Media         │   4   │ 0.5              │
│  Customer Review      │   5   │ 0.6              │
│  Conference Talk      │   6   │ 0.7              │
│  Anonymous Tip        │   2   │ 0.3              │
│                                                 │
│  Final Score = Source Score × Confidence ×      │
│               Freshness Decay                   │
│                                                 │
│  Freshness Decay = exp(-days_since / 30)       │
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
| ID Generation | hashlib | Deterministic unique IDs |
| Date Handling | datetime | Timestamp management |
| Collections | defaultdict | Efficient aggregation |

## 7. Security Considerations

### 7.1 Data Sensitivity
- Competitive intelligence may contain sensitive market data
- No persistence to unencrypted storage
- Source attribution tracked for accountability
- Confidence levels indicate data reliability
- Access controls for sensitive reports
- Data classification levels (public, internal, confidential, restricted)

### 7.2 Source Verification
- Each intelligence report tagged with source type
- Verification status tracked (verified/unverified)
- Confidence levels guide decision-making weight
- Freshness metadata prevents stale data usage
- Cross-reference validation across multiple sources
- Source credibility scoring and tracking

### 7.3 Ethical Intelligence
- All data collection from public sources
- No industrial espionage or unauthorized access
- Compliance with fair competition regulations
- Transparent methodology documentation
- Regular ethics audits
- Whistleblower protection protocols

### 7.4 Data Protection
- Encryption at rest for sensitive intelligence
- Access logging for all data queries
- Retention policies based on data classification
- Secure deletion protocols
- Audit trails for compliance

## 8. Scalability

### 8.1 Current Architecture
- In-memory stores limit to ~10,000 intelligence reports
- Competitor profiles: ~500 concurrently
- Trend detection on ~100,000 data points
- Benchmark metrics: ~10,000 per category
- Search queries: ~1,000 concurrent

### 8.2 Scaling Strategies
- **Database backend**: PostgreSQL for persistent storage
- **Search engine**: Elasticsearch for full-text search at scale
- **Streaming pipeline**: Kafka for real-time data ingestion
- **ML integration**: NLP models for automated sentiment analysis
- **API layer**: REST API for external system integration
- **Caching layer**: Redis for frequently accessed intelligence
- **Microservices**: Decompose monolith into independent services
- **Load balancing**: Distribute analysis across multiple instances

### 8.3 Performance Targets

| Metric | Current | Scaled Target |
|--------|---------|---------------|
| Competitor add | < 20ms | < 10ms |
| SWOT analysis | < 50ms | < 20ms |
| Trend detection | < 200ms | < 50ms |
| Benchmark ranking | < 100ms | < 30ms |
| Intelligence search | < 100ms | < 20ms |
| Strategic brief | < 1s | < 200ms |

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

### 9.1 Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Integration Architecture                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐                                            │
│  │ External    │                                            │
│  │ APIs        │                                            │
│  └──────┬──────┘                                            │
│         v                                                   │
│  ┌─────────────┐                                            │
│  │ API Gateway │──> Rate limiting, authentication, logging  │
│  └──────┬──────┘                                            │
│         v                                                   │
│  ┌─────────────┐                                            │
│  │ Adapter     │──> Normalize external data formats         │
│  │ Layer       │                                            │
│  └──────┬──────┘                                            │
│         v                                                   │
│  ┌─────────────┐                                            │
│  │ Queue       │──> Async processing, retry logic           │
│  │ Manager     │                                            │
│  └──────┬──────┘                                            │
│         v                                                   │
│  ┌─────────────┐                                            │
│  │ Intelligence│──> Core processing and storage             │
│  │ Core        │                                            │
│  └─────────────┘                                            │
└─────────────────────────────────────────────────────────────┘
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
| Rate limit exceeded | Implement exponential backoff |
| Data validation error | Return detailed validation errors |
| Timeout error | Retry with reduced scope |

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
- Source credibility calculations
- Freshness decay algorithms

### Integration Tests
- Competitor → Analysis → Brief pipeline
- Trend detection from real data sequences
- Multi-competitor benchmark comparison
- Intelligence collection and retrieval cycle
- Cross-framework SWOT comparison
- Real-time trend monitoring

### Acceptance Tests
- End-to-end competitive analysis scenario
- Trend detection accuracy against known patterns
- Brief generation completeness validation
- Source credibility scoring accuracy
- Benchmark ranking consistency

### Performance Tests
- Load testing with 10K+ intelligence reports
- Concurrent search query handling
- Memory usage optimization
- Response time under load

## 13. Configuration

```python
config = {
    "competitor_limit": 500,
    "intelligence_limit": 10000,
    "trend_data_points": 100000,
    "benchmark_metrics": 10000,
    "search_index_size": 1000000,
    "cache_ttl": 3600,
    "source_weights": {
        "sec_filing": 1.0,
        "earnings_call": 1.0,
        "news_article": 0.7,
        "social_media": 0.5,
    },
    "freshness_decay_days": 30,
    "confidence_threshold": 0.7,
}
agent = CompetitiveIntelAgent(config)
```

## 14. Best Practices

1. **Data Quality Over Quantity** — Focus on high-quality, verified intelligence
2. **Regular Updates** — Refresh competitor profiles monthly at minimum
3. **Cross-Validation** — Verify critical intelligence across multiple sources
4. **Timeliness** — Prioritize recent intelligence for decision-making
5. **Documentation** — Maintain clear methodology documentation
6. **Ethical Standards** — Adhere to fair competition regulations
7. **Actionable Focus** — Every analysis should conclude with recommendations
8. **Continuous Monitoring** — Set up alerts for critical competitor activities
9. **Knowledge Sharing** — Distribute intelligence to relevant stakeholders
10. **Security Awareness** — Protect sensitive competitive intelligence

## 15. Troubleshooting

| Problem | Diagnosis | Solution |
|---------|-----------|----------|
| SWOT analysis too generic | Not enough context/data | Add company-specific data points, involve domain experts |
| Trend detection too noisy | Low-quality data points | Increase minimum data point threshold, filter by source quality |
| Benchmark rankings inaccurate | Outdated competitor data | Refresh competitor metrics, verify data freshness |
| Intelligence reports conflicting | Multiple unverified sources | Check confidence levels, prefer verified sources |
| Threat assessment wrong | Missing competitor context | Review recent moves, update profile with latest intel |
| Strategic brief lacks insight | Insufficient intelligence volume | Increase data collection, diversify sources |
| Search returns irrelevant results | Poor keyword matching | Refine search terms, use advanced filters |
| Source credibility issues | Unverified sources | Implement stricter source verification |
| Memory overflow | Too many data points | Archive old data, implement data retention policies |

---

*Competitive Intelligence Agent Architecture v3.0 — Part of the Awesome Grok Skills collection.*