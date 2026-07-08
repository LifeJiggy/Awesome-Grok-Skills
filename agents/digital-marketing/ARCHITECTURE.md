# Digital Marketing Agent — System Architecture

## Overview

The Digital Marketing Agent is a modular, event-driven platform for managing
multi-channel marketing campaigns at scale. It provides campaign lifecycle
management, channel strategy optimization, performance analytics, multi-touch
attribution, email marketing, social media management, and SEO auditing — all
within a single cohesive agent framework.

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      DigitalMarketingAgent                              │
│  (Top-level Orchestrator)                                               │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐  ┌────────────────┐  ┌──────────────────────────────┐ │
│  │  Campaign     │  │  Channel       │  │  Performance                 │ │
│  │  Manager      │  │  Strategy      │  │  Analytics                   │ │
│  │              │  │  Engine        │  │                              │ │
│  │  - CRUD      │  │  - Recommend   │  │  - Touchpoint tracking       │ │
│  │  - Validate  │  │  - Allocate    │  │  - Dashboard snapshots       │ │
│  │  - Lifecycle │  │  - Optimize    │  │  - Trend analysis            │ │
│  └──────┬───────┘  └───────┬────────┘  └──────────────┬───────────────┘ │
│         │                  │                           │                  │
│  ┌──────┴───────┐  ┌──────┴────────┐  ┌──────────────┴───────────────┐ │
│  │  Attribution  │  │  Email        │  │  Social Media                │ │
│  │  Engine       │  │  Marketing    │  │  Manager                     │ │
│  │              │  │  Engine       │  │                              │ │
│  │  - 8 models  │  │  - Campaigns  │  │  - Multi-platform posting    │ │
│  │  - Journeys  │  │  - Events     │  │  - Engagement tracking       │ │
│  │  - Compare   │  │  - Segments   │  │  - Scheduling queue          │ │
│  └──────────────┘  └───────────────┘  └──────────────────────────────┘ │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │                     SEO Manager                                     │ │
│  │  - Keyword tracking & ranking changes                               │ │
│  │  - Site audits & scorecards                                         │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Component Deep Dives

### 1. CampaignManager

**Purpose**: Full lifecycle management for marketing campaigns — creation,
updates, activation, pausing, completion, duplication, and deletion.

```
┌─────────────────────────────────────────┐
│           CampaignManager               │
├─────────────────────────────────────────┤
│  _campaigns: Dict[str, Campaign]        │
│  _audit_log: List[Dict]                 │
├─────────────────────────────────────────┤
│  create_campaign()    → Campaign        │
│  update_campaign()    → Campaign        │
│  delete_campaign()    → bool            │
│  activate_campaign()  → bool            │
│  pause_campaign()     → bool            │
│  complete_campaign()  → bool            │
│  duplicate_campaign() → Campaign        │
│  add_ad_group()       → bool            │
│  list_campaigns()     → List[Campaign]  │
│  get_campaign_health() → Dict           │
└─────────────────────────────────────────┘
```

**Key Design Decisions**:
- Every state transition is logged to `_audit_log` for compliance and debugging.
- `validate()` is called before activation to catch missing creatives,
  invalid budgets, or incomplete ad groups.
- Campaign duplication creates a deep copy with a fresh ID and resets status
  to DRAFT.

### 2. ChannelStrategyEngine

**Purpose**: Develops multi-channel marketing strategies, allocates budgets
across channels, and optimizes allocation based on real performance data.

```
┌──────────────────────────────────────────────┐
│          ChannelStrategyEngine               │
├──────────────────────────────────────────────┤
│  CHANNEL_COST_BENCHMARKS                     │
│  _strategies: Dict[str, Dict]                │
├──────────────────────────────────────────────┤
│  develop_strategy()          → Dict          │
│  optimize_allocation()       → Dict          │
│  get_channel_recommendations() → List[Dict]  │
│  _recommend_channels()       → List[Channel] │
│  _allocate_budget()          → Dict          │
│  _recommend_bid_strategy()   → BidStrategy   │
│  _score_channel_fit()        → float         │
└──────────────────────────────────────────────┘
```

**Budget Allocation Algorithm**:
1. Start with equal weights across recommended channels.
2. Apply objective-specific multipliers (e.g., Video gets 2.0x for Awareness,
   Paid Search gets 2.5x for Conversion).
3. Normalize weights to sum to 1.0, then multiply by total budget.

**Optimization Loop**:
```
Input: current allocation + ChannelPerformance data
  ↓
For each channel with data:
  Compute weight = channel ROAS / total ROAS
  New allocation = total_budget × weight
  ↓
Return updated allocation
```

### 3. PerformanceAnalytics

**Purpose**: Central touchpoint recording, channel-level aggregation, dashboard
snapshots, trend analysis, and conversion goal tracking.

```
┌──────────────────────────────────────────────┐
│         PerformanceAnalytics                 │
├──────────────────────────────────────────────┤
│  _touchpoints: List[Touchpoint]              │
│  _channel_performance: Dict[Channel, Perf]   │
│  _conversion_goals: Dict[str, ConvGoal]      │
├──────────────────────────────────────────────┤
│  record_touchpoint()         → None          │
│  get_channel_performance()   → Perf | Dict   │
│  get_total_metrics()         → Dict          │
│  create_dashboard()          → DashSnapshot  │
│  get_performance_trend()     → List[Dict]    │
│  register_conversion_goal()  → None          │
│  get_conversion_summary()    → Dict          │
│  _generate_alerts()          → List[Dict]    │
└──────────────────────────────────────────────┘
```

**Alert Generation Rules**:
| Condition | Severity | Message |
|-----------|----------|---------|
| ROAS < 1.0 and cost > $0 | Critical | "ROAS below 1.0 for {channel}" |
| CPC > $5.0 and clicks > 0 | Warning | "High CPC for {channel}" |
| Impressions > 10K and CTR < 0.5% | Warning | "Low CTR for {channel}" |

### 4. AttributionEngine

**Purpose**: Multi-touch attribution modeling across 8 different models with
customer journey grouping and cross-model comparison.

```
┌──────────────────────────────────────────────┐
│          AttributionEngine                   │
├──────────────────────────────────────────────┤
│  _touchpoint_store: List[Touchpoint]         │
│  _results_cache: Dict[Model, AttrResult]     │
├──────────────────────────────────────────────┤
│  add_touchpoints()       → None              │
│  compute_attribution()   → AttributionResult │
│  compare_models()        → Dict[Model,Res]   │
│  get_channel_attribution() → Dict            │
│  _group_journeys()       → Dict[vid, List]   │
│  _compute_journey_credits() → Dict           │
└──────────────────────────────────────────────┘
```

**Attribution Model Comparison Matrix**:

| Model | Credit Distribution | Best For |
|-------|-------------------|----------|
| First Touch | 100% to first | Top-of-funnel analysis |
| Last Touch | 100% to last | Conversion-focused |
| Linear | Equal across all | Balanced view |
| Time Decay | More to recent | Long sales cycles |
| Position-Based | 40/20/40 split | Balanced first+last |
| Data Driven | Algorithmic | High-volume datasets |
| Markov Chain | Removal effect | Path analysis |
| Shapley Value | Game theory | Fair credit assignment |

### 5. EmailMarketingEngine

**Purpose**: Email campaign creation, sending, event tracking, segmentation,
and ROI calculation.

```
┌──────────────────────────────────────────────┐
│         EmailMarketingEngine                 │
├──────────────────────────────────────────────┤
│  _campaigns: Dict[str, EmailCampaign]        │
│  _metrics: Dict[str, EmailMetrics]           │
│  _event_log: List[Dict]                      │
├──────────────────────────────────────────────┤
│  create_campaign()       → EmailCampaign     │
│  send_campaign()         → Dict              │
│  record_event()          → None              │
│  get_campaign_metrics()  → EmailMetrics      │
│  calculate_roi()         → Dict              │
│  get_segment_performance() → Dict            │
└──────────────────────────────────────────────┘
```

**Email Metrics Pipeline**:
```
Sent → Delivered (97% delivery rate) → Opened → Clicked → Converted
       ↓                              ↓
    Bounced (3%)                   Unsubscribed / Complained
```

### 6. SocialMediaManager

**Purpose**: Multi-platform social post creation, publishing, engagement
tracking, scheduling, and analytics.

```
┌──────────────────────────────────────────────┐
│         SocialMediaManager                   │
├──────────────────────────────────────────────┤
│  _posts: Dict[str, SocialPost]               │
│  _metrics: Dict[str, SocialMetrics]          │
│  _scheduling_queue: List[str]                │
├──────────────────────────────────────────────┤
│  create_post()          → SocialPost         │
│  publish_post()         → bool               │
│  record_engagement()    → None               │
│  get_post_metrics()     → SocialMetrics      │
│  get_platform_summary() → Dict               │
│  get_top_posts()        → List[Dict]         │
└──────────────────────────────────────────────┘
```

### 7. SEOManager

**Purpose**: SEO keyword tracking, ranking change detection, site auditing,
and scorecard generation.

```
┌──────────────────────────────────────────────┐
│              SEOManager                      │
├──────────────────────────────────────────────┤
│  _keywords: Dict[str, SEOKeyword]            │
│  _audit_history: List[SEOAuditResult]        │
│  _site_urls: List[str]                       │
├──────────────────────────────────────────────┤
│  add_keyword()              → SEOKeyword     │
│  update_keyword_position()  → SEOKeyword     │
│  get_keyword_rankings()     → List[SEOKey]   │
│  get_ranking_changes()      → List[Dict]     │
│  run_site_audit()           → SEOAuditResult │
│  get_seo_scorecard()        → Dict           │
└──────────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### Campaign Creation Flow

```
User Request
     │
     ▼
┌─────────────────────────────────────────┐
│  DigitalMarketingAgent                  │
│  .create_full_campaign()                │
└────────────────┬────────────────────────┘
                 │
     ┌───────────┼───────────┐
     ▼           ▼           ▼
┌──────────┐ ┌────────┐ ┌──────────┐
│ Campaign │ │Channel │ │ Audience │
│ Manager  │ │Strategy│ │ Definitn │
│ .create()│ │.develop│ │          │
└────┬─────┘ └───┬────┘ └──────────┘
     │           │
     ▼           ▼
  Campaign    Strategy
  Object      Dict
     │           │
     └─────┬─────┘
           ▼
     Return Dict
  {campaign, strategy}
```

### Attribution Analysis Flow

```
Touchpoints (from all channels)
     │
     ▼
┌─────────────────────────────────┐
│  AttributionEngine              │
│  .add_touchpoints()             │
│  .compute_attribution(model)    │
└────────────┬────────────────────┘
             │
             ▼
     Group by visitor_id
     Sort by timestamp
             │
     ┌───────┼───────────────┐
     ▼       ▼               ▼
  First    Linear        Time Decay
  Touch    (equal)       (half-life)
     │       │               │
     └───────┼───────────────┘
             ▼
     Channel Credits
     (normalized)
             │
             ▼
     AttributionResult
```

### Dashboard Generation Flow

```
All Touchpoints
     │
     ▼
┌────────────────────┐
│ PerformanceAnalytics│
│ .create_dashboard() │
└────────┬───────────┘
         │
    ┌────┼────┬─────────┐
    ▼    ▼    ▼         ▼
 Channel  Alert  Trend  Conversion
 Totals  Gen    Data    Summary
    │    │      │         │
    └────┼──────┼─────────┘
         ▼
  DashboardSnapshot
         │
         ▼
  + SEO Scorecard
  + Email Summary
  + Social Summary
         │
         ▼
  Full Dashboard Dict
```

---

## Design Patterns

### Strategy Pattern
Channel budget allocation uses a strategy pattern — different objective types
apply different weight multipliers to channels, allowing flexible allocation
without conditional spaghetti.

### Observer / Event Log Pattern
Every campaign state change is appended to `_audit_log`. This enables
compliance reporting, debugging, and future event replay.

### Cache Pattern
The AttributionEngine caches results per model. Since touchpoints rarely
change mid-session, recomputation is avoided for repeated calls.

### Composite Pattern
The agent composes seven sub-engines. Each sub-engine is independently
testable and can be replaced or extended without affecting others.

---

## Data Model Summary

| Entity | Key Fields | Relationships |
|--------|-----------|---------------|
| Campaign | id, name, objective, status, channels, budget, ad_groups | 1:N → AdGroup |
| AdGroup | id, name, channel, audience, creatives, bid_strategy | N:1 → Campaign, 1:N → CreativeAsset |
| CreativeAsset | id, name, format, headline, body, URLs | N:1 → AdGroup |
| Touchpoint | id, channel, campaign_id, cost, impressions, clicks, conversions | N:1 → Campaign |
| AttributionResult | model, channel_credits, total_conversions, roas | 1:N → channel_credits |
| EmailCampaign | id, name, subject, from_email, html_content, audience | 1:1 → EmailMetrics |
| SocialPost | id, platform, content, media_urls, hashtags | 1:1 → SocialMetrics |
| SEOKeyword | id, keyword, url, position, search_volume | Independent |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Type System | dataclasses + Enum |
| Logging | stdlib logging |
| Data Storage | In-memory dicts (pluggable) |
| Serialization | dataclass → dict (JSON-serializable) |
| Testing | pytest + hypothesis |
| Concurrency | asyncio (future) |
| External APIs | REST adapters (pluggable) |

---

## Security Considerations

1. **API Key Management**: All external API keys (Google Ads, Meta, etc.)
   should be stored in environment variables, never in source code.
2. **PII Handling**: Audience definitions may contain PII. All PII fields
   must be encrypted at rest and masked in logs.
3. **Rate Limiting**: API calls to ad platforms must respect rate limits.
   The agent implements exponential backoff for 429 responses.
4. **Access Control**: Campaign modifications require authorization checks
   before execution. The audit log records who made each change.
5. **Data Retention**: Touchpoint data older than the configured retention
   period should be purged or aggregated.

---

## Scalability Considerations

| Dimension | Current | Target |
|-----------|---------|--------|
| Concurrent campaigns | 100 | 10,000+ |
| Touchpoints per day | 10K | 10M+ |
| Attribution models | 8 | 8 (extensible) |
| Channels | 15 | 30+ |
| Email sends per hour | 1K | 1M+ |
| Social posts per day | 100 | 10,000+ |

**Scaling Strategy**:
- Move from in-memory to Redis/PostgreSQL for persistent storage.
- Use Celery/Redis for async touchpoint processing.
- Shard attribution computation by visitor_id.
- Use connection pooling for email/Social API calls.

---

## Extension Points

1. **New Channel Types**: Add to `ChannelType` enum and update
   `CHANNEL_COST_BENCHMARKS`.
2. **New Attribution Models**: Add to `AttributionModel` enum and implement
   `_compute_journey_credits` case.
3. **New Bid Strategies**: Add to `BidStrategy` enum and update
   `_recommend_bid_strategy`.
4. **Custom Reporting**: Subclass `DashboardSnapshot` and override
   `compute_derived()`.
5. **External Integrations**: Each sub-engine accepts pluggable storage
   backends for production deployment.

---

## Configuration

```yaml
digital_marketing_agent:
  campaign_manager:
    max_campaigns: 10000
    audit_log_retention_days: 365
    auto_archive_completed_days: 90

  channel_strategy:
    default_currency: USD
    benchmark_refresh_interval_hours: 24
    optimization_frequency: daily

  analytics:
    touchpoint_retention_days: 365
    dashboard_cache_ttl_seconds: 300
    alert_thresholds:
      roas_critical: 1.0
      cpc_warning: 5.0
      ctr_warning: 0.005

  attribution:
    default_model: linear
    time_decay_half_life_days: 7
    cache_enabled: true

  email:
    default_delivery_rate: 0.97
    max_send_rate_per_hour: 100000
    bounce_threshold: 0.05

  seo:
    audit_cache_days: 7
    ranking_check_frequency_hours: 24
    max_keywords_tracked: 50000
```

---

## Performance Benchmarks

| Operation | Latency (p99) | Throughput |
|-----------|---------------|------------|
| Create campaign | < 50ms | 1000/s |
| Record touchpoint | < 5ms | 100K/s |
| Compute attribution | < 500ms | 100/s |
| Generate dashboard | < 200ms | 50/s |
| SEO audit | < 5s | 10/s |
| Email send batch | < 2s | 50 batches/s |

---

## Testing Strategy

| Test Type | Coverage Target | Tools |
|-----------|----------------|-------|
| Unit tests | 90%+ | pytest |
| Integration tests | Key flows | pytest + fixtures |
| Performance tests | Throughput | locust |
| Property-based tests | Data invariants | hypothesis |
| Contract tests | API boundaries | schemathesis |
