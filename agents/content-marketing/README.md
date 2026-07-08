# Content Marketing Agent

> Comprehensive content marketing management — strategy, calendars, SEO, distribution, and analytics.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.0.0-orange.svg)](CHANGELOG.md)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Strategy Development](#strategy-development)
  - [Editorial Calendar](#editorial-calendar)
  - [Content Briefs](#content-briefs)
  - [SEO Optimization](#seo-optimization)
  - [Keyword Research](#keyword-research)
  - [Topic Clusters](#topic-clusters)
  - [Content Distribution](#content-distribution)
  - [Performance Analytics](#performance-analytics)
  - [Content Repurposing](#content-repurposing)
  - [Gap Analysis](#gap-analysis)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Content Marketing Agent is a comprehensive system for managing the full content marketing lifecycle. It handles everything from high-level strategy development through tactical content creation, SEO optimization, multi-channel distribution, and performance analytics.

Built for marketing teams, content strategists, and digital marketing professionals who need a structured, data-driven approach to content marketing operations.

### What Makes This Agent Different

- **Strategy-First**: Every content decision traces back to a documented strategy
- **SEO Built-In**: Optimization is part of the workflow, not an afterthought
- **25+ Distribution Channels**: Comprehensive multi-channel support
- **Data-Driven**: All recommendations based on measurable metrics
- **Full Lifecycle**: From ideation through archival and repurposing
- **Structured Operations**: Every action logged and auditable

---

## Features

| Feature | Description |
|---------|-------------|
| Content Strategy | Create strategies with pillars, goals, audience targeting, SWOT analysis |
| Editorial Calendar | Multi-view calendar with daily/weekly/monthly/custom views |
| Content Briefs | Detailed briefs with keyword targeting, outlines, required sections |
| SEO Analysis | 4-dimension scoring (content, on-page, technical, off-page) |
| SEO Optimization | Actionable recommendations with priority and estimated impact |
| Keyword Research | Generate keywords with volume, difficulty, intent, opportunity scores |
| Topic Clusters | Build topical authority with pillar-cluster architecture |
| Distribution | 25+ channels with UTM tracking and timing optimization |
| Analytics | Performance tracking with comparison, anomalies, and reporting |
| Repurposing | Transform content into video, infographic, social, podcast formats |
| Gap Analysis | Identify content gaps based on strategy and existing library |
| Pipeline View | See content status across the entire production pipeline |
| Export | JSON, CSV, Markdown, PDF export formats |
| Caching | TTL-based in-memory cache for performance |
| Audit Trail | Full operation logging with timestamps |

---

## Quick Start

```python
from agents.content_marketing.agent import ContentMarketingAgent

# Initialize agent
agent = ContentMarketingAgent()

# Create a strategy
strategy = agent.create_content_strategy(
    name="My Content Strategy",
    target_market="B2B SaaS",
    pillars=["product growth", "customer success", "thought leadership"],
)

# Create editorial calendar
calendar = agent.create_editorial_calendar(strategy_id=strategy.strategy_id, months=3)

# Create content brief
brief = agent.create_content_brief(
    title="Complete Guide to SaaS Growth",
    primary_keyword="saas growth",
)

# Analyze SEO
seo_report = agent.analyze_seo(content_id="your-content-id")

# Get status
print(agent.get_status())
```

### Run the Demo

```bash
python agents/content-marketing/agent.py
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/LifeJiggy/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills

# No external dependencies required
# Python 3.10+ with standard library only
```

---

## Usage

### Strategy Development

```python
from agents.content_marketing.agent import ContentMarketingAgent, ContentGoal, AudienceSegment, ContentTone

agent = ContentMarketingAgent()

strategy = agent.create_content_strategy(
    name="Growth Marketing 2026",
    target_market="B2B SaaS startups",
    pillars=[
        "product-led growth",
        "developer experience",
        "customer success stories",
    ],
    goals=[ContentGoal.AWARENESS, ContentGoal.LEAD_GENERATION],
    audiences=[AudienceSegment.DEVELOPER, AudienceSegment.MANAGER],
    voice=ContentTone.AUTHORITATIVE,
    budget=120000.0,
)

# Access strategy data
print(strategy.content_pillars)
print(strategy.get_content_mix_summary())
```

### Editorial Calendar

```python
# Create 3-month calendar
calendar = agent.create_editorial_calendar(
    strategy_id=strategy.strategy_id,
    months=3,
)

# Get summary
print(calendar.get_summary())

# Get monthly view
view = agent.get_calendar_view(
    calendar_id=calendar.calendar_id,
    view=CalendarView.MONTHLY,
)

# Filter by author
entries = calendar.get_entries_by_author("content-writer-1")
```

### Content Briefs

```python
brief = agent.create_content_brief(
    title="The Complete Guide to Product-Led Growth",
    primary_keyword="product-led growth",
    secondary_keywords=["PLG strategy", "product-led growth framework"],
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
        "Case studies",
        "Getting started guide",
    ],
    deadline=datetime(2026, 7, 15),
)

# Generate content piece from brief
content = agent.generate_content_from_brief(brief.brief_id)
```

### SEO Optimization

```python
# Analyze content SEO
report = agent.analyze_seo(content_id=content.content_id)
print(f"Score: {report.overall_score}")
print(f"Issues: {len(report.issues)}")
print(f"Recommendations: {len(report.recommendations)}")

# Get optimization recommendations
optimization = agent.optimize_seo_content(
    content_id=content.content_id,
    target_keyword="product-led growth",
)
print(f"Estimated improvement: +{optimization['estimated_improvement']['estimated_score_increase']}")
```

### Keyword Research

```python
keywords = agent.generate_keyword_research(
    seed_keyword="conversion rate optimization",
    topic="marketing optimization",
    count=25,
)

# Analyze opportunities
for kw in sorted(keywords, key=lambda k: k.opportunity_score, reverse=True)[:5]:
    print(f"{kw.keyword}: vol={kw.search_volume}, diff={kw.keyword_difficulty}, score={kw.opportunity_score:.1f}")
```

### Topic Clusters

```python
cluster = agent.create_topic_cluster(
    pillar_topic="Conversion Rate Optimization",
    supporting_topics=[
        "A/B testing best practices",
        "Landing page design",
        "Call-to-action optimization",
        "User behavior analytics",
        "Form optimization",
    ],
    keywords=keywords[:5],
)

print(f"Cluster: {cluster.pillar_topic}")
print(f"Content needed: {cluster.total_content_count}")
```

### Content Distribution

```python
results = agent.distribute_content(
    content_id=content.content_id,
    channels=[
        DistributionChannel.ORGANIC_SEARCH,
        DistributionChannel.SOCIAL_MEDIA_LINKEDIN,
        DistributionChannel.EMAIL_MARKETING,
    ],
)

for result in results:
    print(f"{result.channel.value}: {result.status}")

# Get optimal posting times
times = agent.get_optimal_posting_times(
    channel=DistributionChannel.SOCIAL_MEDIA_LINKEDIN,
    audience=AudienceSegment.MANAGER,
)
```

### Performance Analytics

```python
# Record performance
agent.record_performance(
    content_id=content.content_id,
    metrics={
        "pageviews": 2500,
        "unique_visitors": 1800,
        "bounce_rate": 0.38,
        "conversion_rate": 0.042,
    },
)

# Get analytics
analytics = agent.get_content_analytics(timeframe=AnalyticsTimeframe.LAST_30_DAYS)
report = agent.generate_performance_report()
```

### Content Repurposing

```python
repurposed = agent.repurpose_content(
    content_id=content.content_id,
    target_formats=[
        ContentFormat.VIDEO_TUTORIAL,
        ContentFormat.INFOGRAPHIC_DATA,
        ContentFormat.SOCIAL_CAROUSEL,
        ContentFormat.PODCAST_EPISODE,
    ],
)

for brief in repurposed:
    print(f"Created: {brief.title}")
```

### Gap Analysis

```python
gaps = agent.get_content_gaps(strategy_id=strategy.strategy_id)

for gap in gaps:
    print(f"[{gap['priority']}] {gap['type']}: {gap.get('recommendation', 'N/A')}")
```

---

## API Reference

### ContentMarketingAgent

| Method | Description | Returns |
|--------|-------------|---------|
| `create_content_strategy()` | Create a new strategy | `ContentStrategy` |
| `update_content_strategy()` | Update existing strategy | `ContentStrategy` |
| `get_content_strategy()` | Get strategy by ID | `ContentStrategy` |
| `list_strategies()` | List all strategies | `List[ContentStrategy]` |
| `delete_content_strategy()` | Delete a strategy | `bool` |
| `create_editorial_calendar()` | Create editorial calendar | `EditorialCalendar` |
| `update_calendar_entry()` | Update calendar entry | `CalendarEntry` |
| `get_calendar()` | Get calendar by ID | `EditorialCalendar` |
| `list_calendars()` | List all calendars | `List[EditorialCalendar]` |
| `get_calendar_view()` | Get calendar view | `Dict` |
| `create_content_brief()` | Create content brief | `ContentBrief` |
| `update_content_brief()` | Update content brief | `ContentBrief` |
| `get_content_brief()` | Get brief by ID | `ContentBrief` |
| `list_briefs()` | List all briefs | `List[ContentBrief]` |
| `generate_content_from_brief()` | Generate content from brief | `ContentPiece` |
| `create_content_piece()` | Create content piece | `ContentPiece` |
| `update_content_status()` | Update content status | `ContentPiece` |
| `get_content()` | Get content by ID | `ContentPiece` |
| `list_content()` | List content with filters | `List[ContentPiece]` |
| `delete_content()` | Delete content piece | `bool` |
| `get_content_pipeline()` | Get pipeline status | `Dict[str, int]` |
| `analyze_seo()` | Analyze SEO | `SEOReport` |
| `optimize_seo_content()` | Get SEO recommendations | `Dict` |
| `generate_keyword_research()` | Generate keywords | `List[Keyword]` |
| `create_topic_cluster()` | Create topic cluster | `TopicCluster` |
| `distribute_content()` | Distribute to channels | `List[DistributionResult]` |
| `get_distribution_status()` | Get distribution status | `Dict` |
| `get_optimal_posting_times()` | Get posting times | `Dict` |
| `repurpose_content()` | Repurpose content | `List[ContentBrief]` |
| `record_performance()` | Record metrics | `PerformanceSnapshot` |
| `get_content_analytics()` | Get analytics | `Dict` |
| `get_performance_comparison()` | Compare performance | `Dict` |
| `generate_performance_report()` | Generate report | `Dict` |
| `get_content_gaps()` | Find content gaps | `List[Dict]` |
| `get_status()` | Get agent status | `Dict` |
| `get_operation_log()` | Get operation log | `List[Dict]` |
| `clear_cache()` | Clear cache | `int` |
| `export_data()` | Export all data | `str` |

### EditorialCalendar

| Method | Description | Returns |
|--------|-------------|---------|
| `add_entry()` | Add calendar entry | `None` |
| `get_entry()` | Get entry by ID | `Optional[CalendarEntry]` |
| `remove_entry()` | Remove entry | `bool` |
| `get_entries_by_date()` | Get entries for date | `List[CalendarEntry]` |
| `get_entries_by_status()` | Get entries by status | `List[CalendarEntry]` |
| `get_entries_by_type()` | Get entries by type | `List[CalendarEntry]` |
| `get_entries_by_channel()` | Get entries by channel | `List[CalendarEntry]` |
| `get_entries_by_author()` | Get entries by author | `List[CalendarEntry]` |
| `get_view()` | Get view by mode | `Dict` |
| `get_summary()` | Get calendar summary | `Dict` |

### ContentPiece

| Method | Description | Returns |
|--------|-------------|---------|
| `add_keyword()` | Add keyword | `None` |
| `update_status()` | Update status | `None` |
| `add_review_note()` | Add review note | `None` |
| `calculate_seo_score()` | Calculate SEO score | `float` |

### SEOReport

| Method | Description | Returns |
|--------|-------------|---------|
| `add_issue()` | Add issue | `None` |
| `add_recommendation()` | Add recommendation | `None` |
| `calculate_overall_score()` | Calculate score | `float` |

### Keyword

| Property | Description | Returns |
|----------|-------------|---------|
| `opportunity_score` | Computed opportunity score | `float` |

---

## Examples

### Example 1: Complete Content Strategy Workflow

```python
from agents.content_marketing.agent import ContentMarketingAgent, ContentGoal, AudienceSegment

agent = ContentMarketingAgent()

# 1. Define strategy
strategy = agent.create_content_strategy(
    name="Enterprise SaaS Marketing",
    target_market="Enterprise CTOs and VP Engineering",
    pillars=["technical deep-dives", "ROI analysis", "case studies"],
    goals=[ContentGoal.THOUGHT_LEADERSHIP, ContentGoal.LEAD_GENERATION],
    audiences=[AudienceSegment.EXECUTIVE, AudienceSegment.TECHNICAL],
    budget=200000.0,
)

# 2. Research keywords
keywords = agent.generate_keyword_research("enterprise saas", count=20)

# 3. Build topic cluster
cluster = agent.create_topic_cluster(
    pillar_topic="Enterprise SaaS Selection",
    supporting_topics=[k.keyword for k in keywords[:5]],
    keywords=keywords[:5],
)

# 4. Create brief
brief = agent.create_content_brief(
    title="Enterprise SaaS Selection Guide 2026",
    primary_keyword="enterprise saas selection",
    secondary_keywords=[k.keyword for k in keywords[1:5]],
    target_word_count=4000,
    audience="CTOs evaluating enterprise SaaS solutions",
)

# 5. Generate content
content = agent.generate_content_from_brief(brief.brief_id)

# 6. Optimize and distribute
seo = agent.analyze_seo(content.content_id)
results = agent.distribute_content(content.content_id)

print(f"Strategy: {strategy.name}")
print(f"SEO Score: {seo.overall_score}")
print(f"Distribution: {len(results)} channels")
```

### Example 2: Content Repurposing Pipeline

```python
# Find top performers
analytics = agent.generate_performance_report()
top_performers = analytics["top_performers"][:3]

for performer in top_performers:
    # Repurpose into multiple formats
    formats = [
        ContentFormat.VIDEO_TUTORIAL,
        ContentFormat.INFOGRAPHIC_DATA,
        ContentFormat.SOCIAL_CAROUSEL,
        ContentFormat.PODCAST_EPISODE,
        ContentFormat.CHECKLIST,
    ]
    repurposed = agent.repurpose_content(performer["content_id"], formats)
    print(f"'{performer['title']}' → {len(repurposed)} new pieces")
```

### Example 3: SEO-First Content Creation

```python
# Start with keyword research
keywords = agent.generate_keyword_research("content marketing", count=30)

# Sort by opportunity score
top_keywords = sorted(keywords, key=lambda k: k.opportunity_score, reverse=True)

# Create cluster around best keyword
best = top_keywords[0]
cluster = agent.create_topic_cluster(
    pillar_topic=best.keyword,
    supporting_topics=[k.keyword for k in top_keywords[1:7]],
)

# Create brief for pillar content
brief = agent.create_content_brief(
    title=f"Complete Guide to {best.keyword.title()}",
    primary_keyword=best.keyword,
    secondary_keywords=[k.keyword for k in top_keywords[1:5]],
    target_word_count=3500,
)

print(f"Best keyword: {best.keyword} (score: {best.opportunity_score:.1f})")
```

---

## Configuration

```python
from agents.content_marketing.agent import Config, SEOConfig, DistributionConfig, AnalyticsConfig

# Custom configuration
config = Config(
    agent_name="MyContentAgent",
    version="1.0.0",
    log_level="DEBUG",
    enable_caching=True,
    cache_ttl_seconds=1800,
    timezone="America/New_York",
    default_author="content-team",
    brand_voice=ContentTone.AUTHORITATIVE,
    content_review_required=True,
    auto_optimize_enabled=True,
    topic_cluster_enabled=True,
    content_scoring_enabled=True,
    seo=SEOConfig(
        target_keyword_density=0.02,
        max_keyword_density=0.04,
        min_word_count=300,
        ideal_word_count=2000,
        target_readability_score=70.0,
        max_title_length=60,
        max_meta_description_length=160,
        min_internal_links=3,
        target_images_per_1000_words=1.5,
    ),
    distribution=DistributionConfig(
        primary_channels=[
            DistributionChannel.ORGANIC_SEARCH,
            DistributionChannel.SOCIAL_MEDIA_LINKEDIN,
            DistributionChannel.EMAIL_MARKETING,
        ],
        cross_post_enabled=True,
        syndication_delay_days=7,
        paid_amplification_budget=5000.0,
    ),
    analytics=AnalyticsConfig(
        default_timeframe=AnalyticsTimeframe.LAST_30_DAYS,
        comparison_enabled=True,
        attribution_model="last_touch",
        alert_thresholds={
            "bounce_rate_high": 0.70,
            "conversion_rate_low": 0.01,
            "traffic_drop_percent": 0.20,
        },
    ),
)

agent = ContentMarketingAgent(config=config)
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `agent_name` | str | `"ContentMarketingAgent"` | Agent name |
| `version` | str | `"3.0.0"` | Agent version |
| `log_level` | str | `"INFO"` | Logging level |
| `enable_caching` | bool | `True` | Enable in-memory cache |
| `cache_ttl_seconds` | int | `3600` | Cache TTL in seconds |
| `timezone` | str | `"UTC"` | Default timezone |
| `default_author` | str | `"content-team"` | Default author |
| `brand_voice` | ContentTone | `PROFESSIONAL` | Default brand voice |
| `content_review_required` | bool | `True` | Require review before publish |
| `auto_optimize_enabled` | bool | `True` | Auto-optimize SEO |
| `topic_cluster_enabled` | bool | `True` | Enable topic clusters |
| `content_scoring_enabled` | bool | `True` | Enable content scoring |

---

## Best Practices

### Strategy

1. **Define 3-7 content pillars** — focused enough to be actionable, broad enough to cover your market
2. **Align goals to business objectives** — every content goal should map to a business outcome
3. **Document your audience** — create detailed personas for each segment
4. **Review quarterly** — update strategy based on performance data

### Content Creation

1. **Always start with a brief** — never write without a documented brief
2. **Target 1500+ words** for blog posts — longer content ranks better for competitive keywords
3. **Include primary keyword** in title, meta description, and first 100 words
4. **Add 3+ internal links** per content piece
5. **Include images** with descriptive alt text

### SEO

1. **Keyword density 1.5-3%** — avoid keyword stuffing
2. **Target readability score 70+** — write for humans first
3. **Add schema markup** — enable rich snippets in search results
4. **Optimize for mobile** — 60%+ of traffic is mobile
5. **Monitor Core Web Vitals** — LCP < 2.5s, FID < 100ms, CLS < 0.1

### Distribution

1. **Organic first** — optimize for search before paid promotion
2. **Channel-appropriate** — adapt content format for each channel
3. **UTM tracking** — always include UTM parameters
4. **Syndication delay** — wait 7+ days before syndicating
5. **Repurpose at 90 days** — refresh or repurpose content after 90 days

### Analytics

1. **Record metrics consistently** — track all channels and timeframes
2. **Compare periods** — always compare with previous period
3. **Focus on conversions** — traffic without conversions is vanity
4. **Review weekly** — check pipeline and performance weekly
5. **Act on gaps** — address content gaps immediately

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| SEO score low | Missing keywords in title/meta | Add primary keyword to title and meta description |
| Calendar empty | Strategy missing pillars | Add content pillars to strategy |
| Distribution errors | Channel not configured | Verify channel settings |
| Analytics zero | No performance recorded | Call `record_performance()` first |
| Brief incomplete | Missing required fields | Ensure title and keyword are provided |
| Keywords unrealistic | Estimated data | Integrate with real SEO tool APIs |

### Debug Mode

```python
config = Config(log_level="DEBUG")
agent = ContentMarketingAgent(config=config)

# Check operation log
log = agent.get_operation_log(limit=10)
for entry in log:
    print(f"{entry['timestamp']}: {entry['operation']}")

# Check cache
print(f"Cache size: {agent.clear_cache()}")

# Export data for inspection
data = agent.export_data(format="json")
print(data[:1000])
```

---

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
git clone https://github.com/LifeJiggy/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills
python agents/content-marketing/agent.py
```

### Running Tests

```bash
python -m pytest agents/content-marketing/ -v
```

---

## License

MIT License - see [LICENSE](../../LICENSE).

---

*Content Marketing Agent v3.0.0 — Part of the Awesome Grok Skills collection.*

*Last updated: 2026-07-06*
