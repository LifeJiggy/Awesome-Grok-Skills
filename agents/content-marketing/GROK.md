---
name: content-marketing
version: 3.0.0
description: Comprehensive content marketing management agent — strategy development, editorial calendars, SEO optimization, multi-channel distribution, content analytics, topic clusters, and performance reporting.
author: Awesome Grok Skills Team
tags:
  - content-marketing
  - seo
  - editorial-calendar
  - content-strategy
  - distribution
  - analytics
  - topic-clusters
  - keyword-research
  - performance-reporting
  - content-operations
category: Marketing & Content
personality: Strategic, data-driven, organized, creative yet methodical, focused on measurable outcomes
use_cases:
  - Developing content marketing strategies
  - Creating and managing editorial calendars
  - Performing SEO content optimization
  - Distributing content across multiple channels
  - Tracking and analyzing content performance
  - Building topic clusters for topical authority
  - Conducting keyword research
  - Generating content briefs for writers
  - Repurposing content across formats
  - Identifying content gaps and opportunities
---

# Content Marketing Agent

> THE definitive agent for content marketing strategy, editorial calendar management,
> SEO optimization, multi-channel distribution, performance analytics, and content operations.
> Enterprise-grade, auditable, and deeply structured.

---

## Table of Contents

1. [Agent Identity](#agent-identity)
2. [Core Principles](#core-principles)
3. [Capabilities](#capabilities)
4. [Operational Guidelines](#operational-guidelines)
5. [Method Signatures](#method-signatures)
6. [Usage Patterns](#usage-patterns)
7. [Data Models](#data-models)
8. [Checklists](#checklists)
9. [Troubleshooting](#troubleshooting)

---

## Agent Identity

The Content Marketing Agent is a comprehensive system for managing the full content marketing lifecycle. It handles everything from high-level strategy development through tactical content creation, SEO optimization, multi-channel distribution, and performance analytics.

### What It Does

- Creates and manages content marketing strategies with pillars, goals, and audience targeting
- Builds editorial calendars with multiple view modes and entry management
- Generates detailed content briefs for writers with SEO guidance
- Performs comprehensive SEO analysis with scoring and recommendations
- Distributes content across 25+ channels with UTM tracking and timing optimization
- Tracks performance metrics with comparison, anomaly detection, and reporting
- Builds topic clusters for topical authority and content architecture
- Identifies content gaps based on strategy and existing content library

### What It Does NOT Do

- Does not generate actual content (creates briefs and structures for writers)
- Does not directly publish to external platforms (manages scheduling and tracking)
- Does not replace analytics tools (provides aggregation and reporting layer)
- Does not handle paid media buying (tracks distribution and ROI)

---

## Core Principles

### 1. Strategy-First Approach
Every content decision should trace back to a documented strategy. The agent enforces strategy alignment through pillars, goals, and audience targeting.

### 2. Data-Driven Decisions
All recommendations are based on measurable data — SEO scores, performance metrics, keyword research, and competitive analysis. No guessing.

### 3. Content Lifecycle Thinking
Content is not a one-time event. Every piece has a lifecycle from ideation through publication, promotion, and eventual archival or repurposing.

### 4. SEO as Foundation
Search engine optimization is not an afterthought — it's built into every stage from brief creation through performance analysis.

### 5. Multi-Channel Distribution
Great content deserves great distribution. The agent ensures content reaches audiences through optimal channels at optimal times.

### 6. Continuous Improvement
Performance data feeds back into strategy. Content gaps are identified, underperforming content is flagged, and opportunities are surfaced.

### 7. Structured Operations
Every operation is logged, every change is tracked, and every output is structured for downstream consumption.

---

## Capabilities

### 1. Content Strategy Management

Create, update, and manage content marketing strategies with full lifecycle support.

```python
from agents.content_marketing.agent import ContentMarketingAgent, ContentGoal, AudienceSegment, ContentTone

agent = ContentMarketingAgent()

# Create a comprehensive strategy
strategy = agent.create_content_strategy(
    name="B2B SaaS Growth 2026",
    target_market="B2B SaaS startups Series A-C",
    pillars=[
        "product-led growth",
        "developer experience",
        "customer success stories",
        "industry thought leadership",
    ],
    goals=[ContentGoal.AWARENESS, ContentGoal.LEAD_GENERATION, ContentGoal.THOUGHT_LEADERSHIP],
    audiences=[AudienceSegment.DEVELOPER, AudienceSegment.MANAGER, AudienceSegment.ENTERPRISE],
    voice=ContentTone.AUTHORITATIVE,
    budget=150000.0,
)

# Access strategy details
print(strategy.strategy_id)       # "a1b2c3d4"
print(strategy.content_pillars)   # ["product-led growth", ...]
print(strategy.get_content_mix_summary())  # {"blog_post": 35.0, ...}
```

**Strategy Features:**
- Content pillars (3-7 strategic themes recommended)
- Topic clusters for each pillar
- Content mix ratios by type
- Channel mix ratios
- Publishing frequency by content type
- SWOT analysis
- Competitor landscape tracking
- Budget allocation

### 2. Editorial Calendar Management

Build and manage editorial calendars with multiple view modes.

```python
# Create a 3-month calendar
calendar = agent.create_editorial_calendar(
    strategy_id=strategy.strategy_id,
    months=3,
)

# Get calendar summary
summary = calendar.get_summary()
print(summary["total_entries"])    # 45
print(summary["by_type"])         # {"blog_post": 25, "social_post": 15, ...}
print(summary["by_status"])       # {"planned": 45}

# Get monthly view
monthly = agent.get_calendar_view(
    calendar_id=calendar.calendar_id,
    view=CalendarView.MONTHLY,
)

# Get entries by author
entries = calendar.get_entries_by_author("content-writer-1")
```

**Calendar Views:**
- Daily, Weekly, Monthly, Quarterly, Yearly
- By Content Type, Channel, Author, Topic

### 3. Content Brief Generation

Create detailed briefs that guide content creation.

```python
brief = agent.create_content_brief(
    title="The Complete Guide to Product-Led Growth",
    primary_keyword="product-led growth",
    secondary_keywords=["PLG strategy", "product-led growth framework", "SaaS growth"],
    target_word_count=3000,
    audience="Marketing leaders at B2B SaaS companies",
    intent=KeywordIntent.INFORMATIONAL,
    tone=ContentTone.AUTHORITATIVE,
    goals=[ContentGoal.EDUCATION, ContentGoal.LEAD_GENERATION],
    outline=[
        "What is Product-Led Growth?",
        "Why PLG matters in 2026",
        "PLG framework components",
        "Implementation steps",
        "Case studies from top SaaS companies",
        "Common pitfalls and how to avoid them",
        "Measuring PLG success",
        "Getting started guide",
    ],
    deadline=datetime(2026, 7, 15),
)

# Generate content piece from brief
content = agent.generate_content_from_brief(brief.brief_id)
print(content.content_id)  # Pre-populated content piece
```

**Brief Includes:**
- Target word count and keyword targeting
- Search intent classification
- Tone and voice guidance
- Structured outline
- Required sections based on content type
- Deadline tracking
- Special instructions

### 4. SEO Content Optimization

Comprehensive SEO analysis with scoring, issues, and recommendations.

```python
# Analyze existing content
seo_report = agent.analyze_seo(content_id=content.content_id)
print(f"Overall Score: {seo_report.overall_score}")  # 72.5
print(f"Issues Found: {len(seo_report.issues)}")     # 4
print(f"Recommendations: {len(seo_report.recommendations)}")  # 6

# Get specific recommendations
optimization = agent.optimize_seo_content(
    content_id=content.content_id,
    target_keyword="product-led growth",
)
print(f"Estimated Improvement: +{optimization['estimated_improvement']['estimated_score_increase']}")
```

**SEO Analysis Dimensions:**
- Content Score (35%): Word count, keyword density, images, links
- On-Page Score (30%): Title, meta description, canonical, schema
- Technical Score (25%): OG tags, URL structure, mobile readiness
- Off-Page Score (10%): Backlinks, domain authority

### 5. Keyword Research

Generate keyword research from seed terms with metrics and classification.

```python
keywords = agent.generate_keyword_research(
    seed_keyword="product-led growth",
    topic="SaaS growth strategy",
    count=25,
)

# Analyze keywords
for kw in keywords[:5]:
    print(f"{kw.keyword}: vol={kw.search_volume}, diff={kw.keyword_difficulty}, intent={kw.intent.value}")
    print(f"  Opportunity Score: {kw.opportunity_score:.1f}")
```

**Keyword Data:**
- Search volume estimates
- Keyword difficulty scores
- Cost per click data
- Search intent classification
- Competition level
- Opportunity score (computed)

### 6. Topic Cluster Creation

Build topic clusters for topical authority.

```python
cluster = agent.create_topic_cluster(
    pillar_topic="Product-Led Growth",
    supporting_topics=[
        "PLG metrics and KPIs",
        "Onboarding optimization",
        "Freemium vs free trial",
        "PLG sales motion",
        "Customer-led growth",
        "Product-qualified leads",
        "Usage-based pricing",
    ],
    keywords=keywords[:5],
)

print(f"Cluster: {cluster.pillar_topic}")
print(f"Supporting topics: {len(cluster.supporting_topics)}")
print(f"Total content needed: {cluster.total_content_count}")
```

### 7. Multi-Channel Distribution

Distribute content across 25+ channels with tracking.

```python
# Distribute to multiple channels
results = agent.distribute_content(
    content_id=content.content_id,
    channels=[
        DistributionChannel.ORGANIC_SEARCH,
        DistributionChannel.SOCIAL_MEDIA_LINKEDIN,
        DistributionChannel.EMAIL_MARKETING,
        DistributionChannel.SOCIAL_MEDIA_TWITTER,
    ],
)

for result in results:
    print(f"{result.channel.value}: {result.status}")
    print(f"  UTM: {result.utm_parameters}")

# Get optimal posting times
times = agent.get_optimal_posting_times(
    channel=DistributionChannel.SOCIAL_MEDIA_LINKEDIN,
    audience=AudienceSegment.MANAGER,
)
print(f"Best days: {times['schedule']['best_days']}")
print(f"Best times: {times['schedule']['best_times']}")
```

**Distribution Channels (25+):**
- Organic: Search, AMP, RSS
- Social: Facebook, Twitter, LinkedIn, Instagram, TikTok, Pinterest
- Paid: Search, Social
- Email: Marketing campaigns
- Syndication: Medium, Microsoft Start, News Google
- Community: Forums, GitHub
- Video/Audio: YouTube, Podcasts
- Partners: Influencer, Partner network
- PR: Press wire, SlideShare

### 8. Content Repurposing

Transform content into multiple formats.

```python
repurposed = agent.repurpose_content(
    content_id=content.content_id,
    target_formats=[
        ContentFormat.VIDEO_TUTORIAL,
        ContentFormat.INFOGRAPHIC_DATA,
        ContentFormat.SOCIAL_CAROUSEL,
        ContentFormat.PODCAST_EPISODE,
        ContentFormat.CHECKLIST,
    ],
)

for brief in repurposed:
    print(f"Created: {brief.title}")
    print(f"  Format: {brief.content_type.value}")
```

**Repurposing Options:**
- Blog → Video Tutorial / Interview
- Blog → Infographic (Data / Process)
- Blog → Social Carousel / Thread
- Blog → Podcast Episode
- Blog → Email Sequence
- Blog → Ebook / Guide
- Blog → Checklist / Cheat Sheet
- Blog → Webinar

### 9. Performance Analytics

Track, compare, and report on content performance.

```python
# Record performance data
agent.record_performance(
    content_id=content.content_id,
    metrics={
        "pageviews": 2500,
        "unique_visitors": 1800,
        "bounce_rate": 0.38,
        "time_on_page": 420,
        "social_shares": 89,
        "backlinks": 24,
        "conversion_rate": 0.042,
    },
    channel_breakdown={
        "organic_search": {"pageviews": 1500, "conversions": 65},
        "social_media": {"pageviews": 600, "conversions": 12},
        "email": {"pageviews": 400, "conversions": 28},
    },
)

# Get analytics
analytics = agent.get_content_analytics(timeframe=AnalyticsTimeframe.LAST_30_DAYS)
print(f"Total content: {analytics['content_count']}")
print(f"Pipeline: {analytics['pipeline_status']}")

# Compare performance
comparison = agent.get_performance_comparison(content.content_id)
print(f"Changes: {comparison['changes']}")

# Generate report
report = agent.generate_performance_report()
print(f"Top performers: {len(report['top_performers'])}")
```

### 10. Content Gap Analysis

Identify missing or underrepresented content areas.

```python
gaps = agent.get_content_gaps(strategy_id=strategy.strategy_id)

for gap in gaps:
    print(f"[{gap['priority']}] {gap['type']}")
    print(f"  {gap.get('recommendation', 'N/A')}")
```

**Gap Types:**
- Pillar underrepresented (not enough content for a pillar)
- Cluster gap (missing supporting content in a cluster)
- Funnel gap (no content targeting a funnel stage)

---

## Operational Guidelines

### Content Lifecycle Management

Follow the proper status transitions:

```
IDEATION → PLANNED → IN_PROGRESS → DRAFT → REVIEW → APPROVED → SCHEDULED → PUBLISHED
                                                                            ↓
                                                                    PROMOTING → ARCHIVED
                                                                            ↓
                                                                    REPURPOSED
```

### SEO Best Practices

1. **Always include primary keyword** in title, meta description, and first 100 words
2. **Target 1.5-3% keyword density** for primary keyword
3. **Minimum 1 internal link** per 500 words (3+ minimum)
4. **Add images** with descriptive alt text (1+ per 1000 words)
5. **Include schema markup** for rich snippets
6. **Optimize for mobile** with responsive design
7. **Target Core Web Vitals**: LCP < 2.5s, FID < 100ms, CLS < 0.1

### Distribution Strategy

1. **Organic first**: Optimize for search before paid promotion
2. **Channel-appropriate**: Adapt content format for each channel
3. **Timing matters**: Use optimal posting times for each channel
4. **UTM tracking**: Always include UTM parameters for attribution
5. **Repurpose at 90 days**: Refresh or repurpose content after 90 days

### Calendar Planning

1. **Plan 3 months ahead** minimum
2. **Balance content types**: Follow your content mix ratios
3. **Avoid conflicts**: Check for overlapping topics or authors
4. **Buffer time**: Leave 2-3 days between draft and publish
5. **Review cycle**: Weekly calendar review meetings

---

## Method Signatures

### Strategy Methods

```python
def create_content_strategy(
    self,
    name: str,
    target_market: str,
    pillars: List[str],
    goals: Optional[List[ContentGoal]] = None,
    audiences: Optional[List[AudienceSegment]] = None,
    voice: ContentTone = ContentTone.PROFESSIONAL,
    budget: float = 0.0,
) -> ContentStrategy

def update_content_strategy(self, strategy_id: str, **kwargs: Any) -> ContentStrategy
def get_content_strategy(self, strategy_id: str) -> ContentStrategy
def list_strategies(self) -> List[ContentStrategy]
def delete_content_strategy(self, strategy_id: str) -> bool
```

### Calendar Methods

```python
def create_editorial_calendar(
    self,
    strategy_id: str,
    months: int = 3,
    start_date: Optional[datetime] = None,
) -> EditorialCalendar

def update_calendar_entry(self, calendar_id: str, entry_id: str, **kwargs: Any) -> CalendarEntry
def get_calendar(self, calendar_id: str) -> EditorialCalendar
def list_calendars(self) -> List[EditorialCalendar]
def get_calendar_view(self, calendar_id: str, view: CalendarView, date: Optional[datetime] = None) -> Dict
```

### Content Methods

```python
def create_content_brief(
    self,
    title: str,
    primary_keyword: str,
    target_word_count: int = 1500,
    secondary_keywords: Optional[List[str]] = None,
    audience: str = "",
    intent: KeywordIntent = KeywordIntent.INFORMATIONAL,
    tone: ContentTone = ContentTone.PROFESSIONAL,
    goals: Optional[List[ContentGoal]] = None,
    outline: Optional[List[str]] = None,
    deadline: Optional[datetime] = None,
) -> ContentBrief

def generate_content_from_brief(self, brief_id: str) -> ContentPiece
def create_content_piece(self, title: str, content_type: ContentType = ContentType.BLOG_POST, ...) -> ContentPiece
def update_content_status(self, content_id: str, new_status: ContentStatus) -> ContentPiece
def get_content(self, content_id: str) -> ContentPiece
def list_content(self, status: Optional[ContentStatus] = None, ...) -> List[ContentPiece]
def delete_content(self, content_id: str) -> bool
def get_content_pipeline(self) -> Dict[str, int]
```

### SEO Methods

```python
def analyze_seo(self, content_id: str, check_competitors: bool = False) -> SEOReport
def optimize_seo_content(self, content_id: str, target_keyword: Optional[str] = None) -> Dict
def generate_keyword_research(self, seed_keyword: str, topic: str = "", count: int = 20) -> List[Keyword]
def create_topic_cluster(self, pillar_topic: str, supporting_topics: List[str], ...) -> TopicCluster
```

### Distribution Methods

```python
def distribute_content(
    self,
    content_id: str,
    channels: Optional[List[DistributionChannel]] = None,
    schedule: Optional[Dict[DistributionChannel, datetime]] = None,
) -> List[DistributionResult]

def get_distribution_status(self, content_id: str) -> Dict
def get_optimal_posting_times(self, channel: DistributionChannel, audience: AudienceSegment = AudienceSegment.ALL) -> Dict
def repurpose_content(self, content_id: str, target_formats: List[ContentFormat]) -> List[ContentBrief]
```

### Analytics Methods

```python
def record_performance(
    self,
    content_id: str,
    metrics: Dict[str, float],
    timeframe: AnalyticsTimeframe = AnalyticsTimeframe.LAST_30_DAYS,
    ...
) -> PerformanceSnapshot

def get_content_analytics(self, content_id: Optional[str] = None, timeframe: AnalyticsTimeframe = ..., ...) -> Dict
def get_performance_comparison(self, content_id: str, ...) -> Dict
def generate_performance_report(self, content_ids: Optional[List[str]] = None, ...) -> Dict
def get_content_gaps(self, strategy_id: Optional[str] = None) -> List[Dict]
```

### Status & Export

```python
def get_status(self) -> Dict[str, Any]
def get_operation_log(self, limit: int = 50) -> List[Dict[str, Any]]
def clear_cache(self) -> int
def export_data(self, format: str = "json") -> str
```

---

## Usage Patterns

### Pattern 1: Full Content Marketing Workflow

```python
agent = ContentMarketingAgent()

# 1. Create strategy
strategy = agent.create_content_strategy(
    name="Growth Marketing 2026",
    target_market="B2B SaaS",
    pillars=["product growth", "customer success", "industry insights"],
)

# 2. Build calendar
calendar = agent.create_editorial_calendar(strategy_id=strategy.strategy_id, months=3)

# 3. Create brief
brief = agent.create_content_brief(
    title="Ultimate Guide to PLG",
    primary_keyword="product-led growth",
)

# 4. Generate content piece
content = agent.generate_content_from_brief(brief.brief_id)

# 5. Optimize SEO
seo_report = agent.analyze_seo(content.content_id)
optimization = agent.optimize_seo_content(content.content_id, "product-led growth")

# 6. Distribute
results = agent.distribute_content(content.content_id)

# 7. Track performance
agent.record_performance(content.content_id, {"pageviews": 5000, "conversions": 210})

# 8. Analyze and report
analytics = agent.get_content_analytics()
report = agent.generate_performance_report()
```

### Pattern 2: SEO-First Content Creation

```python
# Start with keyword research
keywords = agent.generate_keyword_research("conversion rate optimization", count=15)

# Identify high-opportunity keywords
top_keywords = sorted(keywords, key=lambda k: k.opportunity_score, reverse=True)[:5]

# Create brief targeting top keyword
brief = agent.create_content_brief(
    title=f"Complete Guide to {top_keywords[0].keyword.title()}",
    primary_keyword=top_keywords[0].keyword,
    secondary_keywords=[k.keyword for k in top_keywords[1:]],
)

# Build topic cluster
cluster = agent.create_topic_cluster(
    pillar_topic=top_keywords[0].keyword,
    supporting_topics=[k.keyword for k in top_keywords[1:]],
    keywords=top_keywords,
)
```

### Pattern 3: Content Repurposing Pipeline

```python
# Identify high-performing content
analytics = agent.get_content_analytics()
top_performers = analytics["top_performers"][:3]

# Repurpose each into multiple formats
for performer in top_performers:
    repurposed = agent.repurpose_content(
        content_id=performer["content_id"],
        target_formats=[
            ContentFormat.VIDEO_TUTORIAL,
            ContentFormat.INFOGRAPHIC_DATA,
            ContentFormat.SOCIAL_CAROUSEL,
            ContentFormat.PODCAST_EPISODE,
        ],
    )
    print(f"Repurposed '{performer['title']}' into {len(repurposed)} formats")
```

### Pattern 4: Content Gap Analysis & Planning

```python
# Analyze gaps
gaps = agent.get_content_gaps(strategy_id=strategy.strategy_id)

# Prioritize and plan
high_priority = [g for g in gaps if g["priority"] == "high"]
for gap in high_priority:
    brief = agent.create_content_brief(
        title=gap.get("recommendation", "New content piece"),
        primary_keyword=gap.get("pillar", "topic"),
    )
    print(f"Created brief for gap: {gap['type']}")
```

---

## Data Models

### ContentPiece

| Field | Type | Description |
|-------|------|-------------|
| content_id | str | Unique 12-char ID |
| title | str | Content title |
| slug | str | URL-friendly slug |
| content_type | ContentType | Type of content |
| status | ContentStatus | Current lifecycle status |
| stage | ContentStage | Funnel stage |
| format | ContentFormat | Detailed format |
| author | str | Content author |
| topic | str | Content topic |
| keywords | List[Keyword] | Target keywords |
| word_count | int | Word count |
| seo_score | float | SEO score 0-100 |
| performance | Dict | Tracked metrics |

### Keyword

| Field | Type | Description |
|-------|------|-------------|
| keyword | str | The keyword phrase |
| search_volume | int | Monthly search volume |
| keyword_difficulty | float | Difficulty 0-100 |
| cost_per_click | float | CPC in dollars |
| intent | KeywordIntent | Search intent |
| competition | CompetitionLevel | Competition level |
| opportunity_score | float | Computed opportunity |

### CalendarEntry

| Field | Type | Description |
|-------|------|-------------|
| entry_id | str | Unique 8-char ID |
| date | datetime | Scheduled date |
| content_type | ContentType | Content type |
| channel | DistributionChannel | Target channel |
| author | str | Assigned author |
| status | ContentStatus | Entry status |
| priority | int | Priority level |

### PerformanceSnapshot

| Field | Type | Description |
|-------|------|-------------|
| snapshot_id | str | Unique ID |
| content_id | str | Content reference |
| timeframe | AnalyticsTimeframe | Time period |
| metrics | Dict[str, float] | Metric values |
| channel_breakdown | Dict | Per-channel metrics |
| anomalies | List[Dict] | Detected anomalies |

---

## Checklists

### Content Brief Checklist

- [ ] Title includes primary keyword
- [ ] Target word count specified (1500+ for blog)
- [ ] Primary keyword identified
- [ ] 3-5 secondary keywords included
- [ ] Target audience defined
- [ ] Search intent classified
- [ ] Content goals specified
- [ ] Outline with 5+ sections
- [ ] Required sections included
- [ ] Deadline set
- [ ] Special instructions documented

### SEO Optimization Checklist

- [ ] Primary keyword in title
- [ ] Primary keyword in meta description
- [ ] Primary keyword in first 100 words
- [ ] Keyword density 1.5-3%
- [ ] 3+ internal links
- [ ] 1+ images per 1000 words
- [ ] Alt text on all images
- [ ] Meta title < 60 characters
- [ ] Meta description < 160 characters
- [ ] Canonical URL set
- [ ] Schema markup included
- [ ] Open Graph tags present
- [ ] Mobile-friendly formatting
- [ ] Clear headings structure (H1 > H2 > H3)

### Distribution Checklist

- [ ] UTM parameters configured
- [ ] Channel-appropriate format
- [ ] Optimal posting time selected
- [ ] Cross-posting configured
- [ ] Hashtag strategy defined (social)
- [ ] Email subject line optimized
- [ ] Paid amplification budget set (if applicable)
- [ ] Syndication delay configured (7+ days)
- [ ] Influencer outreach planned (if applicable)

### Performance Review Checklist

- [ ] Metrics recorded for all channels
- [ ] Channel breakdown documented
- [ ] Audience breakdown documented
- [ ] Comparison with previous period
- [ ] Anomalies identified
- [ ] Top performers highlighted
- [ ] Underperformers flagged
- [ ] Recommendations generated
- [ ] Action items assigned

---

## Troubleshooting

### Problem: SEO score is low

**Symptoms:** `seo_report.overall_score < 50`

**Diagnosis:**
```python
report = agent.analyze_seo(content_id)
for issue in report.issues:
    if issue["severity"] == "high":
        print(f"HIGH: {issue['category']}: {issue['message']}")
```

**Common Fixes:**
1. Add primary keyword to title and meta description
2. Increase word count to meet minimum (300+ words)
3. Add internal links (3+ minimum)
4. Include images with alt text
5. Add schema markup

### Problem: Calendar entries not appearing

**Symptoms:** Calendar has 0 entries after creation

**Diagnosis:**
```python
calendar = agent.get_calendar(calendar_id)
print(f"Entries: {len(calendar.entries)}")
print(f"Period: {calendar.start_date} to {calendar.end_date}")
```

**Common Fixes:**
1. Check that strategy has content pillars defined
2. Verify start_date is not in the future
3. Ensure months parameter is > 0

### Problem: Distribution results show errors

**Symptoms:** `result.error_message` is not empty

**Diagnosis:**
```python
results = agent.distribute_content(content_id)
for result in results:
    if result.error_message:
        print(f"{result.channel.value}: {result.error_message}")
```

**Common Fixes:**
1. Verify channel is properly configured
2. Check UTM parameter generation
3. Ensure content has required fields (title, slug)

### Problem: Analytics showing zero metrics

**Symptoms:** `get_content_analytics()` returns empty metrics

**Diagnosis:**
```python
analytics = agent.get_content_analytics(content_id)
print(f"Content count: {analytics['content_count']}")
print(f"Total metrics: {analytics['total_metrics']}")
```

**Common Fixes:**
1. Record performance data with `record_performance()`
2. Check content_id is correct
3. Verify timeframe parameter matches recorded data

### Problem: Keyword research returning unrealistic data

**Symptoms:** Keywords have very high/low volumes

**Note:** The agent generates estimated keyword data for demonstration. In production, integrate with actual SEO tool APIs (Ahrefs, SEMrush, Google Keyword Planner) for real data.

### Problem: Content gaps not identifying issues

**Symptoms:** `get_content_gaps()` returns empty list

**Diagnosis:**
```python
gaps = agent.get_content_gaps(strategy_id=strategy.strategy_id)
print(f"Strategy pillars: {strategy.content_pillars}")
print(f"Content topics: {[c.topic for c in agent.list_content()]}")
```

**Common Fixes:**
1. Ensure strategy has content pillars defined
2. Verify content pieces have topics set
3. Check that topic clusters are created

---

*Content Marketing Agent v3.0.0 — Part of the Awesome Grok Skills collection.*
*Last updated: 2026-07-06*
