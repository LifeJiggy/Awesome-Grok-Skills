# Social Media Agent

Comprehensive social media management platform with content scheduling, engagement analytics, audience insights, influencer marketing, and reputation monitoring.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Content Management](#content-management)
  - [Engagement Tracking](#engagement-tracking)
  - [Audience Analytics](#audience-analytics)
  - [Performance Reports](#performance-reports)
  - [Influencer Marketing](#influencer-marketing)
  - [Reputation Monitoring](#reputation-monitoring)
  - [Campaign Management](#campaign-management)
  - [Dashboard](#dashboard)
- [API Reference](#api-reference)
- [Data Models](#data-models)
- [Design Patterns](#design-patterns)
- [Security](#security)
- [Scalability](#scalability)
- [Configuration](#configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Checklists](#checklists)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

The Social Agent provides end-to-end social media management across multiple platforms. It handles content lifecycle from creation through scheduling and publishing, tracks engagement with sentiment analysis, analyzes audience demographics, manages influencer collaborations, and monitors brand reputation with crisis detection.

```
┌─────────────────────────────────────────────────────────────────────┐
│                       SOCIAL MEDIA AGENT                              │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────┐  │
│  │   Content    │  │  Engagement  │  │   Audience   │  │ Social │  │
│  │   Manager    │  │   Manager    │  │   Analyzer   │  │Analytics│ │
│  │              │  │              │  │              │  │        │  │
│  │ * Posts      │  │ * Tracking   │  │ * Demographics│ │ * KPIs │  │
│  │ * Templates  │  │ * Sentiment  │  │ * Best times │  │*Reports│  │
│  │ * Calendar   │  │ * Automations│  │ * Growth     │  │*Trends │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────┘  │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐                                  │
│  │  Influencer  │  │ Reputation   │                                  │
│  │   Manager    │  │   Monitor    │                                  │
│  │              │  │              │                                  │
│  │ * Discovery  │  │ * Keywords   │                                  │
│  │ * Tiers      │  │ * Alerts     │                                  │
│  │ * ROI        │  │ * Crisis     │                                  │
│  └──────────────┘  └──────────────┘                                  │
└─────────────────────────────────────────────────────────────────────┘
```

## Features

| Feature | Description |
|---------|-------------|
| **Multi-Platform Content** | Create and schedule posts for Twitter, LinkedIn, Instagram, YouTube, TikTok, and more |
| **Thread Creation** | Build connected content threads with automatic numbering |
| **Template System** | Reusable content templates with variable substitution |
| **Sentiment Analysis** | Lexicon-based sentiment classification for engagement text |
| **Audience Analytics** | Demographics, active hours, growth tracking, cross-platform overlap |
| **Influencer Management** | Discovery, tier classification, collaboration ROI tracking |
| **Reputation Monitoring** | Brand mention tracking with crisis alert levels |
| **Campaign Management** | Multi-platform campaigns with KPI tracking |
| **Unified Dashboard** | Aggregated metrics across all social channels |

## Architecture

### Component Interaction

```
                    ┌─────────────────┐
                    │   SocialAgent   │
                    │    (Facade)     │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
    ┌───────▼──────┐ ┌──────▼──────┐ ┌───────▼──────┐
    │  Content     │ │ Engagement  │ │  Audience    │
    │  Manager     │ │  Manager    │ │  Analyzer    │
    └───────┬──────┘ └──────┬──────┘ └───────┬──────┘
            │                │                │
            └────────────────┼────────────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
    ┌───────▼──────┐ ┌──────▼──────┐ ┌───────▼──────┐
    │  Influencer  │ │ Reputation  │ │   Social     │
    │  Manager     │ │  Monitor    │ │  Analytics   │
    └──────────────┘ └─────────────┘ └──────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for full details.

## Quick Start

```python
from agents.social.agent import SocialAgent, Platform

agent = SocialAgent()

# Create and schedule a post
post = agent.content.create_post(
    platform=Platform.TWITTER,
    content="Hello world!",
    hashtags=["#hello"],
)

# Track engagement
agent.engagement.track_engagement(
    post_id=post.id,
    user_id="user_001",
    username="fan",
    engagement_type=EngagementType.LIKE,
)

# Get dashboard
dashboard = agent.get_social_dashboard()
```

Run directly:

```bash
python agents/social/agent.py
```

## Usage

### Content Management

```python
from agents.social.agent import SocialAgent, Platform, ContentType

agent = SocialAgent()

# Create post with scheduling
post = agent.content.create_post(
    platform=Platform.LINKEDIN,
    content="Excited to announce our new feature!",
    content_type=ContentType.POST,
    scheduled_at=datetime(2025, 2, 1, 10, 0),
    hashtags=["#product", "#launch"],
)

# Create thread
thread = agent.content.create_thread(
    platform=Platform.TWITTER,
    messages=["Step 1...", "Step 2...", "Step 3..."],
)

# Use templates
agent.content.add_template("tip", "Tip of the day: {{tip}}")
content = agent.content.render_template("tip", {"tip": "Enable MFA"})

# Content calendar
calendar = agent.content.get_calendar(start, end)
```

### Engagement Tracking

```python
from agents.social.agent import EngagementType

# Track engagement
eng = agent.engagement.track_engagement(
    post_id="post_001",
    user_id="user_123",
    username="fan",
    engagement_type=EngagementType.COMMENT,
    content="Great work!",
)

# Metrics per post
metrics = agent.engagement.get_engagement_metrics("post_001")

# Top engagers
top = agent.engagement.get_top_engagers(limit=10)

# Sentiment trend
trend = agent.engagement.get_sentiment_trend(days=30)
```

### Audience Analytics

```python
# Add audience data per platform
agent.audience.add_audience_data(Platform.TWITTER, {
    "followers": 25000,
    "growth_rate": 0.03,
    "engagement_rate": 0.045,
    "active_hours": [9, 12, 18],
})

# Optimal posting times
times = agent.audience.get_optimal_posting_times(Platform.TWITTER)

# Cross-platform overlap
overlap = agent.audience.analyze_cross_platform_overlap()

# Growth recommendations
recs = agent.audience.get_growth_recommendations()
```

### Performance Reports

```python
# KPIs
kpis = agent.analytics.calculate_kpis()

# Top posts
top = agent.analytics.get_top_performing_posts(limit=5)

# Platform breakdown
breakdown = agent.analytics.get_platform_breakdown()

# Full report
report = agent.analytics.generate_report()
```

### Influencer Marketing

```python
# Add influencer
inf = agent.influencer.add_influencer(
    username="expert",
    platform=Platform.TWITTER,
    followers=150000,
    engagement_rate=0.05,
    niche="security",
)

# Find by niche
top = agent.influencer.find_top_influencers("security")

# Record collaboration
collab = agent.influencer.record_collaboration(
    influencer_id=inf.id,
    campaign_id="camp_001",
    content_posts=3,
    total_reach=45000,
    cost=2500.0,
)

# Summary
summary = agent.influencer.get_influencer_summary()
```

### Reputation Monitoring

```python
from agents.social.agent import SentimentType

# Add keywords
agent.reputation.add_keywords(["brandname"])

# Record events
event = agent.reputation.record_event(
    platform=Platform.TWITTER,
    event_type="mention",
    content="Love brandname!",
    source="tweet",
    sentiment=SentimentType.POSITIVE,
)

# Reputation score
score = agent.reputation.get_reputation_score()

# Recent events
recent = agent.reputation.get_recent_events(days=7)
```

### Campaign Management

```python
from datetime import datetime

campaign = agent.create_campaign(
    name="Product Launch",
    description="Multi-platform launch",
    platforms=[Platform.TWITTER, Platform.LINKEDIN],
    start_date=datetime(2025, 1, 15),
    end_date=datetime(2025, 2, 15),
    budget=10000.0,
)

# Batch schedule
agent.schedule_content_batch([
    {"platform": "twitter", "content": "Launch!", "scheduled_at": "2025-01-15T09:00:00"},
])
```

### Dashboard

```python
dashboard = agent.get_social_dashboard()
# {
#   "kpis": {...},
#   "audience": {...},
#   "reputation": {...},
#   "influencers": {...},
#   "top_posts": [...],
#   "recommendations": [...]
# }
```

## API Reference

### SocialAgent

| Method | Returns |
|--------|---------|
| `create_campaign(name, desc, platforms, start, end?, budget?)` | Campaign |
| `schedule_content_batch(posts_data)` | Dict with scheduled_count |
| `respond_to_mentions(keyword)` | List of response actions |
| `get_social_dashboard()` | Full dashboard dict |

### ContentManager

| Method | Returns |
|--------|---------|
| `create_post(platform, content, ...)` | SocialPost |
| `create_thread(platform, messages, ...)` | List[SocialPost] |
| `add_template(name, template, ...)` | None |
| `render_template(name, variables)` | Optional[str] |
| `get_calendar(start, end, platform?)` | Dict[str, List] |
| `publish_post(post_id)` | Dict |

### EngagementManager

| Method | Returns |
|--------|---------|
| `track_engagement(...)` | Engagement |
| `respond_to_engagement(id, response)` | Dict |
| `create_automation(trigger, action, ...)` | Dict |
| `get_engagement_metrics(post_id)` | Dict |
| `get_top_engagers(limit?)` | List[Dict] |
| `get_sentiment_trend(days?)` | List[Dict] |

### AudienceAnalyzer

| Method | Returns |
|--------|---------|
| `add_audience_data(platform, data)` | AudienceInsight |
| `get_optimal_posting_times(platform, count?)` | List[Dict] |
| `analyze_cross_platform_overlap()` | Dict[str, float] |
| `calculate_total_reach()` | Dict |
| `get_growth_recommendations()` | List[str] |

### InfluencerManager

| Method | Returns |
|--------|---------|
| `add_influencer(username, platform, followers, ...)` | InfluencerProfile |
| `find_top_influencers(niche, limit?)` | List[InfluencerProfile] |
| `record_collaboration(...)` | Dict |
| `get_influencer_summary()` | Dict |

### ReputationMonitor

| Method | Returns |
|--------|---------|
| `add_keywords(keywords)` | None |
| `record_event(platform, type, content, source, sentiment)` | ReputationEvent |
| `get_reputation_score()` | Dict |
| `get_recent_events(days?)` | List[ReputationEvent] |

## Data Models

### SocialPost
Post record with platform, content, hashtags, and scheduling data.

### Engagement
Interaction record with type, user, sentiment, and timestamp.

### AudienceInsight
Platform audience data with demographics, growth, and activity patterns.

### InfluencerProfile
Influencer record with followers, engagement rate, niche, and collaboration history.

### ReputationEvent
Brand mention with sentiment, platform, and alert level.

## Design Patterns

| Pattern | Usage | Component |
|---------|-------|-----------|
| **Facade** | Unified social interface | SocialAgent |
| **Strategy** | Platform-specific formatting | ContentManager |
| **Observer** | Engagement tracking | EngagementManager |
| **Template Method** | Post creation per platform | ContentManager |
| **State Machine** | Campaign lifecycle | CampaignManager |

## Security

- Social account credentials encrypted
- Access controls on content modification
- Audit trail for all posts and campaigns
- Rate limiting on platform APIs
- Content moderation before publishing

## Scalability

| Dimension | Strategy | Notes |
|-----------|----------|-------|
| Posts | Indexed by platform + date | Fast calendar queries |
| Engagement | Time-series storage | Efficient trend analysis |
| Audiences | Partitioned by platform | Platform-specific analytics |
| Campaigns | Indexed by status | Active vs archived |

## Configuration

```python
import logging
logging.basicConfig(level=logging.INFO)

# Custom platform rules
agent.content._content_rules[Platform.CUSTOM] = {
    "max_length": 5000,
    "max_hashtags": 10,
}

# Custom sentiment lexicon
agent.engagement._sentiment_lexicon["positive"].append("industry_term")
```

## Examples

See `main()` in `agent.py` for a complete working example demonstrating:
- Post creation and scheduling
- Engagement tracking with sentiment
- Audience data ingestion
- Reputation event monitoring
- Dashboard generation

## Best Practices

1. **Add audience data first** - Analytics depend on it
2. **Use templates for consistency** - Maintain brand voice
3. **Monitor reputation actively** - Catch crises early
4. **Track influencer ROI** - Measure collaboration value
5. **Schedule during peak hours** - Use audience analytics
6. **Respond to negative sentiment quickly** - Prevent escalation
7. **Review sentiment trends weekly** - Spot patterns early

## Checklists

### Content Creation
- [ ] Platform-specific formatting applied
- [ ] Hashtags relevant and within limits
- [ ] Scheduled at optimal time
- [ ] Brand voice consistent

### Campaign Management
- [ ] Multi-platform strategy defined
- [ ] Budget allocated per platform
- [ ] KPIs established
- [ ] Content calendar populated

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Post truncated | Check platform max_length rules |
| Sentiment always neutral | Add domain-specific terms to lexicon |
| Calendar empty | Posts need scheduled_at set |
| Engagement rate = 0 | Only PUBLISHED posts count |
| Reputation score stuck | Add keywords and record events |
| Dashboard empty | Add audience data for platforms |

## Files

| File | Description |
|------|-------------|
| `agent.py` | Full implementation with all subsystems |
| `ARCHITECTURE.md` | System architecture and design patterns |
| `GROK.md` | Agent identity, capabilities, and API docs |
| `README.md` | This file |

## License

MIT License - See [LICENSE](../../LICENSE) for details.
