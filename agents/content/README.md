# Content Agent

Content management, creation workflows, editorial processes, publishing pipelines, analytics tracking, and content moderation across multiple platforms and formats.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Content Generation](#content-generation)
  - [SEO Optimization](#seo-optimization)
  - [Content Moderation](#content-moderation)
  - [Content Calendar](#content-calendar)
  - [Social Media](#social-media)
  - [Performance Tracking](#performance-tracking)
- [API Reference](#api-reference)
- [Content Types](#content-types)
- [Data Models](#data-models)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Content Agent is a Python-based system for managing the full content lifecycle from ideation through publishing and performance tracking. It combines content generation, SEO optimization, calendar management, social media publishing, moderation, and analytics.

**Key Capabilities:**
- Multi-format content generation (blog, article, social, email, etc.)
- SEO analysis with keyword density, readability, and structure scoring
- Content moderation with quality assurance
- Content calendar management with topic suggestions
- Platform-optimized social media content
- Performance tracking with engagement metrics

## Features

| Feature | Description |
|---------|-------------|
| Content Generation | Create titles, bodies, meta descriptions, CTAs |
| SEO Optimization | Keyword analysis, readability scoring, recommendations |
| Content Moderation | Quality scoring, flagged term detection, brand compliance |
| Content Calendar | Scheduling, topic suggestions, publishing management |
| Social Media | Platform-optimized posts, thread creation, hashtags |
| Performance Tracking | Views, engagement, CTR, conversion monitoring |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Content Agent                            │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │ Content  │ │   SEO    │ │Calendar  │ │ Social   │     │
│  │Generator │ │Optimizer │ │ Manager  │ │ Manager  │     │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘     │
│       │            │            │            │             │
│  ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐     │
│  │Content   │ │Perform-  │ │ Content  │ │ Report   │     │
│  │Moderator │ │ance Track│ │  Store   │ │Generator │     │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

```python
from agents.content.agent import ContentAgent

agent = ContentAgent()

# Generate content
content = agent.generate_content(
    topic="AI in Marketing",
    content_type="blog_post",
    tone="professional",
    target_audience="marketers",
)

# Analyze SEO
seo = agent.analyze_seo(content["id"])
print(f"SEO Score: {seo['overall_score']}")

# Moderate
mod = agent.moderate_content(content["id"])
print(f"Approved: {mod['approved']}")
```

```bash
python agents/content/agent.py
```

## Usage

### Content Generation

```python
content = agent.generate_content(
    topic="AI in Content Marketing",
    content_type="blog_post",
    tone="professional",
    target_audience="marketers",
    keywords=["AI content", "content marketing"],
)

print(f"Title: {content['title']}")
print(f"Words: {content['word_count']}")
print(f"Reading time: {content['reading_time_minutes']} min")
```

### SEO Optimization

```python
seo = agent.analyze_seo(content["id"])

print(f"SEO Score: {seo['overall_score']}")
print(f"Readability: {seo['readability_score']}")
print(f"Grade level: {seo['grade_level']}")

for rec in seo["recommendations"]:
    print(f"  - {rec}")
```

### Content Moderation

```python
result = agent.moderate_content(content["id"])

print(f"Approved: {result['approved']}")
print(f"Score: {result['score']}")
for flag in result["flags"]:
    print(f"  Flag: {flag}")
for suggestion in result["suggestions"]:
    print(f"  Suggestion: {suggestion}")
```

### Content Calendar

```python
# Add entry
agent.add_calendar_entry(
    title="AI Content Trends",
    content_type="blog_post",
    platform="website",
    scheduled_date="2024-02-01",
    author="Content Team",
)

# Suggest topics
topics = agent.suggest_topics("AI Marketing", 10)
for topic in topics:
    print(f"  {topic['title']}")

# Get calendar
calendar = agent.get_calendar(start_date="2024-01-01")
```

### Social Media

```python
# Generate post
post = agent.generate_social_post("twitter", "AI is transforming content marketing...")
print(f"Characters: {post['character_count']}")
print(f"Hashtags: {post['hashtags']}")

# Generate thread
thread = agent.generate_social_thread("AI Content Marketing", tweet_count=5)
```

### Performance Tracking

```python
# Record metrics
agent.record_performance(
    content_id="abc123",
    views=1500,
    clicks=120,
    shares=45,
    comments=20,
)

# Get performance
perf = agent.get_content_performance("abc123")
print(f"Engagement: {perf['latest']['engagement_rate']}")

# Top performers
top = agent.get_top_performing(limit=5)
```

## API Reference

### ContentAgent

| Method | Parameters | Returns |
|--------|-----------|---------|
| `generate_content()` | topic, content_type, tone, target_audience, keywords | Content dict |
| `analyze_seo()` | content_id, keywords | SEO metrics dict |
| `moderate_content()` | content_id | Moderation result dict |
| `add_calendar_entry()` | title, content_type, platform, scheduled_date, author | Calendar entry dict |
| `suggest_topics()` | niche, count | List of topic suggestions |
| `generate_social_post()` | platform, content | Social post dict |
| `generate_social_thread()` | topic, tweet_count | List of tweet dicts |
| `record_performance()` | content_id, views, clicks, shares, comments, likes | Performance dict |
| `get_content_performance()` | content_id | Performance summary dict |
| `get_top_performing()` | limit | List of top performers |
| `get_calendar()` | start_date, end_date | List of calendar entries |
| `get_calendar_summary()` | — | Calendar summary dict |
| `list_content()` | — | List of content pieces |
| `get_status()` | — | Agent status dict |

## Content Types

| Type | Description | Best For |
|------|-------------|----------|
| `blog_post` | Long-form educational | SEO, thought leadership |
| `article` | News or analysis | Industry updates |
| `social_media` | Short-form engagement | Brand awareness |
| `email` | Direct communication | Nurturing, conversion |
| `landing_page` | Conversion-focused | Lead generation |
| `video_script` | Video outline | YouTube, social video |
| `whitepaper` | In-depth research | Gated content |
| `case_study` | Success story | Social proof |
| `documentation` | Technical reference | Product support |
| `newsletter` | Regular digest | Subscriber engagement |

## Data Models

### ContentPiece
Complete content with title, body, SEO metadata, status, and performance tracking.

### SEOMetrics
SEO analysis with keyword density, readability, structure, and recommendations.

### ContentPerformance
Performance metrics including views, engagement, CTR, and conversion rates.

### ModerationResult
Quality check results with approval status, flags, and suggestions.

## Configuration

```python
config = {
    "default_tone": "professional",
    "default_audience": "general",
    "min_word_count": 300,
    "seo_target_score": 70,
}
agent = ContentAgent(config)
```

## Best Practices

1. **Know Your Audience** — Research and understand your target audience deeply
2. **Provide Value** — Every piece of content should offer genuine value
3. **Optimize for SEO** — Balance SEO with natural, engaging writing
4. **Be Authentic** — Maintain a consistent, authentic brand voice
5. **Test and Iterate** — Continuously refine based on performance data
6. **Plan Ahead** — Use the calendar to maintain consistent publishing
7. **Repurpose Content** — Adapt content for multiple platforms

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Content too generic | Add specific audience pain points and examples |
| SEO score low | Follow SEO recommendations, add keywords naturally |
| Content flagged | Review flagged terms and remove or replace |
| Low engagement | Adjust tone for platform, add stronger CTAs |
| Calendar gaps | Use topic suggestion engine for fresh ideas |

## Files

- `agent.py` — Main implementation (~900 lines)
- `ARCHITECTURE.md` — System architecture with diagrams
- `GROK.md` — Agent instructions and identity
- `README.md` — This file

## Contributing

1. Add new content type templates
2. Enhance SEO analysis algorithms
3. Add new platform integrations
4. Improve moderation rules
5. Update documentation for API changes

## License

Part of the Awesome Grok Skills collection. See project root for license details.
