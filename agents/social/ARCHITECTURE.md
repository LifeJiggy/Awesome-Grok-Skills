# Social Agent Architecture

## 1. Overview

The Social Agent implements a modular social media management platform. It orchestrates six subsystems—content management, engagement tracking, audience analytics, social performance analytics, influencer management, and reputation monitoring—behind a unified `SocialAgent` facade. This architecture enables organizations to manage their social media presence across multiple platforms from a single, cohesive system.

The design follows the principle of separation of concerns: each subsystem handles its domain independently while sharing common data models. The facade layer provides a unified API that coordinates cross-subsystem operations like campaign management, cross-platform analytics, and automated response workflows.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                          SocialAgent (Facade)                                    │
├──────────────┬──────────────┬──────────────┬──────────────┬──────────────────────┤
│   Content    │  Engagement  │   Audience   │   Social     │   Influencer         │
│   Manager    │   Manager    │   Analyzer   │   Analytics  │   Manager            │
├──────────────┼──────────────┼──────────────┼──────────────┼──────────────────────┤
│ Post CRUD    │ Track Events │ Demographics │ KPI Calc     │ Discovery            │
│ Scheduling   │ Sentiment    │ Best Times   │ Top Posts    │ Tier Classification  │
│ Templates    │ Automations  │ Growth Rate  │ Platform     │ Collaboration ROI    │
│ Calendar     │ Response     │ Cross-Plat   │ Reports      │ Relevance Scoring    │
│ Platform     │ Top Engagers │ Overlap      │ Trends       │                      │
│ Rules        │ Trend        │              │              │                      │
├──────────────┴──────────────┴──────────────┴──────────────┴──────────────────────┤
│                          Reputation Monitor                                      │
├──────────────────────────────────────────────────────────────────────────────────┤
│ Keyword Monitoring │ Sentiment Assessment │ Alert Levels │ Crisis Detection      │
└──────────────────────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   Shared Models    │
                    │ SocialPost         │
                    │ Engagement         │
                    │ Campaign           │
                    │ AudienceInsight    │
                    │ InfluencerProfile  │
                    │ ReputationEvent    │
                    └───────────────────┘
```

## 2. Component Descriptions

### 2.1 ContentManager

Handles post creation, template rendering, scheduling, and platform-specific rules. The content manager ensures that each post adheres to the target platform's constraints while maintaining brand consistency through templates and scheduling.

The template system supports variable substitution, allowing dynamic content generation. The calendar system tracks scheduled posts, prevents conflicts, and optimizes posting times based on audience activity data.

```
┌───────────────────────────────────────────────────────────────────────────────┐
│              ContentManager                                                   │
├───────────────────────────────────────────────────────────────────────────────┤
│  Post Store (Dict[str, SocialPost])                                           │
│  - Key: post_id                                                               │
│  - Value: full post record with content, metrics, and status                  │
│                                                                              │
│  Template Registry (Dict[str, Dict])                                          │
│  - template_name → {template, platform, variables, category}                 │
│  - Supports {{variable}} substitution syntax                                  │
│                                                                              │
│  Calendar (Dict[str, List[CalendarEntry]])                                    │
│  - date_string → [scheduled posts for that date]                             │
│  - Prevents double-booking and conflict detection                            │
│                                                                              │
│  Platform Rules (Dict[Platform, Rules])                                       │
│  - Per-platform constraints (length, hashtags, features)                     │
│  - Validation rules for content compliance                                   │
│                                                                              │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐                    │
│  │ create_post  │  │ render_tmpl  │  │ validate_content│                    │
│  │ create_thread│  │ get_calendar │  │ check_conflicts │                    │
│  │ update_post  │  │ schedule     │  │ optimize_time   │                    │
│  │ delete_post  │  │ unschedule   │  │                 │                    │
│  └─────────────┘  └──────────────┘  └─────────────────┘                    │
└───────────────────────────────────────────────────────────────────────────────┘
```

**Platform Rules:**
| Platform | Max Length | Max Hashtags | Max Mentions | Special Features |
|----------|-----------|--------------|--------------|------------------|
| Twitter | 280 | 5 | 10 | Threads, Polls, Spaces |
| LinkedIn | 3,000 | 5 | 10 | Articles, Newsletters |
| Instagram | 2,200 | 30 | 20 | Reels, Carousels, Stories |
| YouTube | 5,000 | 15 | 10 | Shorts, Premieres |
| TikTok | 2,200 | 10 | 10 | Duet, Stitch, LIVE |
| Facebook | 63,206 | 30 | 20 | Groups, Marketplace |

**Content Types:**
| Type | Platforms | Character Limits | Media Support |
|------|-----------|------------------|---------------|
| POST | All | Per platform | Image, Video, GIF |
| THREAD | Twitter | 280 per tweet | Image per tweet |
| STORY | Instagram, Facebook | 2,200 | Image, Video, Poll |
| REEL | Instagram, TikTok | 2,200 | Video (15-90s) |
| ARTICLE | LinkedIn | 100,000+ | Rich text, images |
| SHORT | YouTube, TikTok | 100 | Video (≤60s) |

### 2.2 EngagementManager

Tracks user interactions, analyzes sentiment, and manages automated responses. The engagement manager processes incoming interactions (likes, comments, shares, mentions), classifies sentiment, and triggers appropriate responses based on configurable automation rules.

The sentiment analysis engine uses a lexicon-based approach with support for custom domain-specific terms. The automation system enables immediate responses to common interactions while flagging complex cases for human review.

```
┌───────────────────────────────────────────────────────────────────────────────┐
│            EngagementManager                                                   │
├───────────────────────────────────────────────────────────────────────────────┤
│  Engagement Store (List[Engagement])                                          │
│  - All interactions tracked with timestamps                                  │
│  - Linked to posts and users                                                 │
│                                                                              │
│  Response Registry (Dict[str, str])                                           │
│  - trigger_keyword → response_template                                       │
│  - Supports {{variable}} substitution                                        │
│                                                                              │
│  Automation Rules (List[Dict])                                                │
│  - trigger: engagement_type + conditions                                     │
│  - action: respond, escalate, tag                                            │
│  - priority: determines execution order                                      │
│                                                                              │
│  Sentiment Lexicon (Dict[str, List[str]])                                     │
│  - positive: [love, great, amazing, ...]                                     │
│  - negative: [hate, terrible, awful, ...]                                    │
│  - very_positive: [obsessed, perfect, ...]                                   │
│  - very_negative: [worst, scam, ...]                                         │
│                                                                              │
│  ┌──────────────┐  ┌──────────────────┐  ┌─────────────────┐               │
│  │track_engage   │  │_analyze_sentiment│  │create_automation│               │
│  │respond        │  │get_sentiment_trend│ │check_automations│               │
│  │get_metrics    │  │get_top_engagers  │  │escalate         │               │
│  └──────────────┘  └──────────────────┘  └─────────────────┘               │
└───────────────────────────────────────────────────────────────────────────────┘
```

**Engagement Types:**
| Type | Value | Typical Response |
|------|-------|------------------|
| LIKE | 1 | No action required |
| COMMENT | 5 | Reply if question/complaint |
| SHARE | 3 | Thank for advocacy |
| MENTION | 2 | Acknowledge if positive |
| SAVE | 2 | No action required |
| CLICK | 1 | Track for analytics |
| REPLY | 4 | Continue conversation |

### 2.3 AudienceAnalyzer

Manages audience demographics, behavior patterns, and growth tracking. The analyzer maintains per-platform audience profiles and calculates optimal posting times, growth rates, and cross-platform overlap.

The growth tracking system monitors follower changes over time, calculates velocity, and generates recommendations based on performance patterns. Cross-platform overlap analysis helps identify unique vs. duplicate audience segments.

```
┌───────────────────────────────────────────────────────────────────────────────┐
│           AudienceAnalyzer                                                     │
├───────────────────────────────────────────────────────────────────────────────┤
│  Audience Store (Dict[Platform, AudienceInsight])                             │
│  - Per-platform audience profile with demographics                           │
│  - Engagement rates and active hours                                         │
│                                                                              │
│  Follower History (List[Dict])                                                │
│  - Timestamped follower counts for trend analysis                            │
│  - Enables growth rate calculation                                           │
│                                                                              │
│  ┌────────────────┐  ┌──────────────────┐  ┌──────────────────┐             │
│  │add_audience_data│  │optimal_post_times│  │growth_recommend. │             │
│  │cross_platform   │  │analyze_overlap   │  │get_demographics  │             │
│  │total_reach      │  │calculate_growth  │  │                  │             │
│  └────────────────┘  └──────────────────┘  └──────────────────┘             │
└───────────────────────────────────────────────────────────────────────────────┘
```

**Audience Metrics:**
| Metric | Formula | Description |
|--------|---------|-------------|
| Growth Rate | (current - previous) / previous × 100 | Follower growth percentage |
| Engagement Rate | (likes + comments + shares) / followers × 100 | Audience activity level |
| Reach Rate | impressions / followers × 100 | Content visibility |
| Active Hours | hour with highest engagement | Optimal posting times |
| Demographics | age/gender/location breakdown | Audience composition |

### 2.4 SocialAnalytics

Calculates KPIs, identifies top content, and generates performance reports. The analytics engine aggregates data from content, engagement, and audience subsystems to produce comprehensive performance metrics.

The KPI calculator computes standard social media metrics including engagement rate, reach, impressions, and conversion metrics. The reporting system generates period-over-period comparisons and trend analysis.

```
┌───────────────────────────────────────────────────────────────────────────────┐
│            SocialAnalytics                                                     │
├───────────────────────────────────────────────────────────────────────────────┤
│  References: ContentManager, EngagementManager, AudienceAnalyzer             │
│                                                                              │
│  ┌───────────────┐  ┌──────────────────┐  ┌──────────────────┐             │
│  │calculate_kpis  │  │get_top_posts     │  │platform_breakdown│             │
│  │generate_report │  │get_trends        │  │compare_periods   │             │
│  └───────────────┘  └──────────────────┘  └──────────────────┘             │
│                                                                              │
│  KPI Metrics:                                                                │
│  ┌──────────────────────────────────────────────────────────┐               │
│  │ Total Posts    │ Total Engagements │ Engagement Rate      │               │
│  │ Total Reach    │ Total Impressions │ Click-Through Rate   │               │
│  │ Follower Growth│ Share of Voice     │ Sentiment Score      │               │
│  └──────────────────────────────────────────────────────────┘               │
└───────────────────────────────────────────────────────────────────────────────┘
```

**KPI Definitions:**
| KPI | Formula | Target |
|-----|---------|--------|
| Engagement Rate | engagements / impressions × 100 | > 3% |
| Click-Through Rate | clicks / impressions × 100 | > 2% |
| Share of Voice | brand_mentions / total_mentions × 100 | > 20% |
| Sentiment Score | positive / (positive + negative) × 100 | > 70% |
| Follower Growth Rate | (new_followers / total_followers) × 100 | > 2% monthly |

### 2.5 InfluencerManager

Discovers, classifies, and tracks influencer collaborations. The manager maintains influencer profiles, calculates ROI for collaborations, and identifies top influencers by niche and engagement metrics.

The tier classification system automatically categorizes influencers based on follower count and engagement rates. The collaboration tracking system records campaign performance and calculates return on investment.

```
┌───────────────────────────────────────────────────────────────────────────────┐
│           InfluencerManager                                                   │
├───────────────────────────────────────────────────────────────────────────────┤
│  Profile Store (Dict[str, InfluencerProfile])                                │
│  - Full influencer profiles with metrics                                     │
│  - Classification by tier and niche                                          │
│                                                                              │
│  Collaboration Log (List[Dict])                                               │
│  - Campaign history with performance data                                    │
│  - ROI calculations                                                          │
│                                                                              │
│  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐              │
│  │add_influencer │  │find_top_by_niche │  │calculate_roi     │              │
│  │record_collab  │  │get_summary       │  │compare_influencers│             │
│  │update_profile │  │find_by_tier      │  │                  │              │
│  └──────────────┘  └──────────────────┘  └──────────────────┘              │
└───────────────────────────────────────────────────────────────────────────────┘
```

**Influencer Tiers:**
| Tier | Followers | Engagement Rate | Typical Cost | Use Case |
|------|-----------|-----------------|--------------|----------|
| Nano | 1K-10K | 5-10% | $50-500 | Niche communities, high trust |
| Micro | 10K-100K | 3-5% | $500-5,000 | Targeted reach, authentic voices |
| Macro | 100K-1M | 1-3% | $5,000-50,000 | Broad awareness, brand campaigns |
| Mega | 1M+ | 0.5-2% | $50,000+ | Mass reach, celebrity endorsements |

**ROI Calculation:**
```
ROI = (Revenue Generated - Collaboration Cost) / Collaboration Cost × 100

Where:
  Revenue Generated = tracking_link_conversions × average_order_value
  Collaboration Cost = fee + product_costs + management_overhead
  
Example:
  Fee: $2,000
  Product Costs: $500
  Conversions: 50
  Average Order: $100
  
  Revenue = 50 × $100 = $5,000
  Cost = $2,000 + $500 = $2,500
  ROI = ($5,000 - $2,500) / $2,500 × 100 = 100%
```

### 2.6 ReputationMonitor

Monitors brand mentions, sentiment, and crisis signals. The monitor tracks keywords, assesses sentiment trends, and generates alerts based on configurable thresholds.

The crisis detection system identifies sudden negative sentiment spikes and generates escalation alerts. The alert level system provides clear escalation paths from monitoring to immediate action.

```
┌───────────────────────────────────────────────────────────────────────────────┐
│          ReputationMonitor                                                    │
├───────────────────────────────────────────────────────────────────────────────┤
│  Event Store (List[ReputationEvent])                                          │
│  - All brand mentions with sentiment scores                                  │
│  - Timestamped for trend analysis                                            │
│                                                                              │
│  Alert Queue (List[Dict])                                                     │
│  - Pending alerts requiring attention                                        │
│  - Priority-sorted for efficient processing                                  │
│                                                                              │
│  Keyword Watchlist (List[str])                                                │
│  - Brand names, product names, key phrases                                   │
│  - Case-insensitive matching                                                 │
│                                                                              │
│  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐              │
│  │record_event   │  │get_rep_score     │  │assess_crisis     │              │
│  │assess_alert   │  │get_recent_events │  │escalate          │              │
│  │add_keywords   │  │get_trend         │  │                  │              │
│  └──────────────┘  └──────────────────┘  └──────────────────┘              │
└───────────────────────────────────────────────────────────────────────────────┘
```

**Alert Levels:**
| Level | Condition | Response Time | Action |
|-------|-----------|---------------|--------|
| GREEN | Positive/neutral sentiment | Monitor | Log for trends |
| YELLOW | Slight negative trend | 24 hours | Track and analyze |
| ORANGE | Very negative sentiment | 4 hours | Investigate and respond |
| RED | Crisis keywords detected | 15 minutes | Escalate immediately |

**Crisis Keywords:**
| Category | Examples | Alert Level |
|----------|----------|-------------|
| Data Breach | "hacked", "data leak", "stolen data" | RED |
| Service Outage | "down", "broken", "not working" | ORANGE |
| Product Issue | "bug", "defective", "doesn't work" | YELLOW |
| Negative Review | "terrible", "worst", "scam" | YELLOW |
| Legal Issue | "lawsuit", "sue", "legal action" | RED |

## 3. Data Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         Social Agent Data Flow                                  │
│                                                                                 │
│  User Content                                                                   │
│       │                                                                         │
│       ▼                                                                         │
│  ┌───────────────────┐                                                         │
│  │ ContentManager    │──── Create/Update/Schedule ──── Calendar                 │
│  │                   │                                      │                   │
│  └───────────────────┘                                      │                   │
│                                                             ▼                   │
│  Platform APIs ◄──► EngagementManager ──► Sentiment Analysis                   │
│       │                   │                                                  │   │
│       │                   ▼                                                  │   │
│       │           ┌───────────────┐                                          │   │
│       │           │ Sentiment     │                                          │   │
│       │           │ Classification│                                          │   │
│       │           └───────────────┘                                          │   │
│       │                   │                                                  │   │
│       │                   ▼                                                  │   │
│       │           Automation Rules ──► Auto-Response / Escalation           │   │
│       │                                                                         │
│       ▼                                                                         │
│  AudienceAnalyzer ──► Growth Metrics ──► Recommendations                      │
│       │                                                                         │
│       ▼                                                                         │
│  SocialAnalytics ──► KPI Dashboard ──► Reports                                │
│       │                                                                         │
│  InfluencerManager ──► Collaboration ROI ──► Top Influencers                  │
│       │                                                                         │
│  ReputationMonitor ──► Alert System ──► Crisis Response                       │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 4. Design Patterns

| Pattern | Application | Implementation |
|---------|-------------|----------------|
| **Facade** | `SocialAgent` unifies six subsystems | Single entry point, delegates to subsystems |
| **Strategy** | Platform-specific content rules | `Dict[Platform, Rules]` with validation |
| **Observer** | Reputation monitoring triggers alerts | Event-driven alert generation |
| **Template Method** | Content templates with variable substitution | `{{variable}}` syntax, render function |
| **Registry** | Platform rules and influencer profiles stored as dicts | Class-level configuration |
| **Composite** | Campaigns compose multiple posts | Campaign → Posts → Engagements |
| **Chain of Responsibility** | Automation rules evaluated in sequence | Rules checked by priority |
| **State Machine** | Content status follows defined transitions | DRAFT → SCHEDULED → PUBLISHED |
| **Repository** | Content and engagement data persistence | In-memory store with export |

## 5. Data Models

### Core Entities

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  Entity Relationships                                                          │
│                                                                                 │
│  SocialPost ──1:N──► Engagement                                                 │
│  Campaign ──1:N──► SocialPost                                                   │
│  AudienceInsight ──1:1──► Platform                                              │
│  InfluencerProfile ──N:M──► Campaign (via Collaborations)                       │
│  ReputationEvent ──1:1──► AlertLevel                                            │
│                                                                                 │
│  SocialPost                                                                     │
│  ├── id: str                                                                    │
│  ├── platform: Platform                                                         │
│  ├── content: str                                                               │
│  ├── content_type: ContentType                                                  │
│  ├── status: ContentStatus                                                      │
│  ├── metrics: Dict                                                              │
│  └── engagement_rate: float                                                     │
│                                                                                 │
│  Engagement                                                                     │
│  ├── id: str                                                                    │
│  ├── post_id: str                                                               │
│  ├── user_id: str                                                               │
│  ├── engagement_type: EngagementType                                           │
│  ├── sentiment: SentimentType                                                   │
│  └── timestamp: datetime                                                        │
│                                                                                 │
│  Campaign                                                                       │
│  ├── id: str                                                                    │
│  ├── name: str                                                                  │
│  ├── platforms: List[Platform]                                                  │
│  ├── status: CampaignStatus                                                     │
│  ├── budget: float                                                              │
│  └── posts: List[str] (post_ids)                                               │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Engagement Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  Engagement Processing Pipeline                                                │
│                                                                                 │
│  User Action (like, comment, share, mention)                                    │
│       │                                                                         │
│       ▼                                                                         │
│  track_engagement()                                                             │
│       │                                                                         │
│       ├──► Store Engagement Record                                              │
│       │                                                                         │
│       ├──► Sentiment Analysis                                                   │
│       │    ├── Positive: 0.0 - 0.3                                             │
│       │    ├── Neutral: 0.3 - 0.7                                              │
│       │    └── Negative: 0.7 - 1.0                                             │
│       │                                                                         │
│       ├──► Automation Check                                                     │
│       │    ├── Match Trigger → Execute Action                                   │
│       │    └── No Match → Log for Analytics                                     │
│       │                                                                         │
│       └──► Metrics Update                                                       │
│            ├── Post engagement_count += 1                                       │
│            ├── User engagement_score += weight                                  │
│            └── Platform totals updated                                          │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 6. Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Language | Python 3.10+ | Core runtime |
| Type System | dataclasses, Enum, typing | Type safety and documentation |
| Logging | Python logging | Audit trail and debugging |
| Hashing | hashlib, uuid | Secure ID generation |
| Date/Time | datetime, timedelta | Scheduling and timestamps |
| Data | JSON-compatible dicts | Serialization and API |
| Sentiment | Lexicon-based classification | Text analysis |
| Pattern Matching | re (regex) | Content validation |
| Math | Standard library | Metrics calculations |

## 7. Scalability Considerations

| Dimension | Strategy | Implementation |
|-----------|----------|----------------|
| Post Volume | In-memory store; migrate to DB | Dict-based storage with export |
| Platform Addition | Add to Platform enum + rules dict | Declarative platform configuration |
| Engagement Volume | Batch processing for analytics | Aggregation on-demand |
| Real-time | Event-driven architecture | Pub/sub pattern for production |
| Multi-tenant | Add tenant_id to all models | Partition by tenant |
| Analytics Scale | Pre-compute aggregations | Cache frequently accessed metrics |
| Influencer Scale | Search indexing | Tag-based search optimization |
| Reputation Scale | Stream processing | Real-time sentiment analysis |

## 8. Extension Points

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  Extension Points                                                              │
│                                                                                 │
│  1. New Platform                                                                │
│     - Add to Platform enum                                                      │
│     - Define rules in _init_platform_rules()                                   │
│     - Add content type support                                                  │
│     - Implement API integration                                                 │
│                                                                                 │
│  2. New Content Type                                                            │
│     - Add to ContentType enum                                                   │
│     - Define validation rules                                                   │
│     - Add to platform-specific rules                                            │
│                                                                                 │
│  3. Custom Sentiment Analysis                                                   │
│     - Override _analyze_sentiment() with ML model                               │
│     - Integrate with external NLP services                                      │
│     - Add domain-specific lexicons                                              │
│                                                                                 │
│  4. API Integration                                                             │
│     - Add platform-specific publish methods in ContentManager                   │
│     - Implement OAuth flows for platform authentication                         │
│     - Handle rate limiting and retry logic                                      │
│                                                                                 │
│  5. Analytics Engine                                                            │
│     - Replace SocialAnalytics with external BI tool connector                   │
│     - Add custom KPI calculations                                               │
│     - Integrate with data warehouses                                            │
│                                                                                 │
│  6. Automation Rules                                                            │
│     - Add new trigger types                                                     │
│     - Implement complex conditions (AND/OR logic)                               │
│     - Add webhook integrations                                                  │
│                                                                                 │
│  7. Reporting                                                                   │
│     - Add PDF/HTML report generation                                            │
│     - Integrate with email delivery services                                    │
│     - Add scheduled report delivery                                             │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 9. Performance Characteristics

| Metric | Target | Optimization |
|--------|--------|--------------|
| Post creation | < 10ms | In-memory storage |
| Sentiment analysis | < 5ms per text | Pre-compiled lexicon |
| Dashboard generation | < 100ms | Cached aggregations |
| Calendar query | < 50ms | Date-indexed storage |
| Reputation assessment | < 20ms | Keyword pre-filtering |
| Memory per 10K posts | < 20MB | Efficient dataclass storage |
| Engagement tracking | < 5ms | Batch writes |
| Influencer search | < 30ms | Tag-based indexing |

## Appendix A: Content Validation Rules

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  Content Validation Matrix                                                      │
│                                                                                 │
│  Twitter:                                                                       │
│  ├── Length ≤ 280 characters                                                    │
│  ├── Hashtags ≤ 5                                                               │
│  ├── Mentions ≤ 10                                                              │
│  └── Media: 1 image, 4 images, 1 GIF, or 1 video                              │
│                                                                                 │
│  LinkedIn:                                                                      │
│  ├── Length ≤ 3,000 characters                                                  │
│  ├── Hashtags ≤ 5                                                               │
│  ├── No external links in first 3 lines (algorithm penalty)                    │
│  └── Media: 1 document, 1 video, or 1 image carousel                          │
│                                                                                 │
│  Instagram:                                                                     │
│  ├── Caption ≤ 2,200 characters                                                │
│  ├── Hashtags ≤ 30 (recommended: 11-15)                                        │
│  ├── First line is hook (shows in feed)                                        │
│  └── Media: 1 image, 10-image carousel, 1 video (60s), or 1 Reel (90s)       │
│                                                                                 │
│  YouTube:                                                                       │
│  ├── Title ≤ 100 characters                                                    │
│  ├── Description ≤ 5,000 characters                                            │
│  ├── Tags ≤ 15                                                                  │
│  └── Thumbnail: 1280×720, ≤ 2MB                                               │
│                                                                                 │
│  TikTok:                                                                        │
│  ├── Caption ≤ 2,200 characters                                                │
│  ├── Hashtags ≤ 10                                                              │
│  ├── Video: 15s, 60s, or 3 minutes                                             │
│  └── Audio: original or trending sound                                         │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Appendix B: Sentiment Scoring Algorithm

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  Sentiment Analysis Algorithm                                                   │
│                                                                                 │
│  1. Tokenize text into words                                                   │
│  2. Remove stop words (the, a, is, ...)                                        │
│  3. For each token:                                                             │
│     - Check positive lexicon → score += 1                                      │
│     - Check negative lexicon → score -= 1                                      │
│     - Check very_positive → score += 2                                         │
│     - Check very_negative → score -= 2                                         │
│  4. Normalize score: score / max(abs(score), 1)                               │
│  5. Apply intensity scaling:                                                   │
│     - Exclamation marks → multiply by 1.1 per mark (max 1.5)                  │
│     - ALL CAPS → multiply by 1.2                                               │
│     - Emojis → check emoji sentiment dictionary                               │
│  6. Map to SentimentType:                                                      │
│     - score > 0.5: VERY_POSITIVE                                               │
│     - 0.1 < score ≤ 0.5: POSITIVE                                              │
│     - -0.1 ≤ score ≤ 0.1: NEUTRAL                                              │
│     - -0.5 ≤ score < -0.1: NEGATIVE                                            │
│     - score < -0.5: VERY_NEGATIVE                                              │
│                                                                                 │
│  Confidence = min(1.0, matched_words / total_words × 2)                       │
└─────────────────────────────────────────────────────────────────────────────────┘
```
