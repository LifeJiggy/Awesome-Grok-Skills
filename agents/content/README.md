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
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Content Agent is a Python-based system for managing the full content lifecycle from ideation through publishing and performance tracking. It combines content generation, SEO optimization, calendar management, social media publishing, moderation, and analytics into a single, cohesive platform.

**Key Capabilities:**
- Multi-format content generation (blog, article, social, email, landing page, etc.)
- SEO analysis with keyword density, readability scoring, and structure optimization
- Content moderation with quality assurance and brand compliance
- Content calendar management with topic suggestions and scheduling
- Platform-optimized social media content with hashtag generation
- Performance tracking with engagement metrics, CTR, and trend analysis

**Ideal For:**
- Content marketing teams managing multiple channels
- Solo creators optimizing for SEO and engagement
- Marketing agencies handling client content
- Product teams creating documentation and guides

## Features

| Feature | Description |
|---------|-------------|
| Content Generation | Create titles, bodies, meta descriptions, CTAs for 10+ content types |
| SEO Optimization | Keyword analysis, readability scoring, structure analysis, recommendations |
| Content Moderation | Quality scoring, flagged term detection, brand compliance checking |
| Content Calendar | Scheduling, topic suggestions, status tracking, conflict detection |
| Social Media | Platform-optimized posts, thread creation, hashtag generation |
| Performance Tracking | Views, engagement rate, CTR, conversion monitoring, trend analysis |
| Multi-Platform | Twitter, LinkedIn, Instagram, Facebook, Medium, Substack support |
| Topic Suggestions | AI-powered topic generation based on niche and keywords |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Content Agent                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Content  │  │   SEO    │  │Calendar  │  │ Social   │   │
│  │Generator │  │Optimizer │  │ Manager  │  │ Manager  │   │
│  │          │  │          │  │          │  │          │   │
│  │• Titles  │  │• Keywords│  │• Schedule│  │• Posts   │   │
│  │• Bodies  │  │• Readab. │  │• Topics  │  │• Threads │   │
│  │• Meta    │  │• Struct. │  │• Status  │  │• Tags    │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │             │             │           │
│  ┌────┴─────┐  ┌────┴─────┐  ┌────┴─────┐  ┌────┴─────┐   │
│  │Content   │  │Perform-  │  │ Topic    │  │ Report   │   │
│  │Moderator │  │ance Track│  │ Suggest  │  │Generator │   │
│  │          │  │          │  │ Engine   │  │          │   │
│  │• Quality │  │• Views   │  │• Ideas   │  │• Summary │   │
│  │• Flags   │  │• Clicks  │  │• Keywords│  │• Trends  │   │
│  │• Brand   │  │• CTR     │  │• Niche   │  │• Top 10  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   Data Layer                         │   │
│  │  ContentStore │ CalendarStore │ SocialStore │ Metrics│   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### Installation

```bash
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e .
```

### Basic Usage

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

# Record performance
agent.record_performance(content["id"], views=1000, clicks=50, shares=10)

# Get top performers
top = agent.get_top_performing(limit=5)
```

### Command Line

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
    keywords=["AI content", "content marketing", "AI tools"],
)

print(f"Title: {content['title']}")
print(f"Words: {content['word_count']}")
print(f"Reading time: {content['reading_time_minutes']} min")
print(f"Meta: {content['meta_description']}")
print(f"CTA: {content['cta']}")
```

### SEO Optimization

```python
seo = agent.analyze_seo(content["id"])

print(f"SEO Score: {seo['overall_score']}")
print(f"Readability: {seo['readability_score']}")
print(f"Flesch Score: {seo['flesch_score']}")
print(f"Grade Level: {seo['grade_level']}")
print(f"Headings: {seo['heading_count']}")
print(f"Paragraphs: {seo['paragraph_count']}")

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
    keywords=["AI trends", "marketing"],
)

# Suggest topics
topics = agent.suggest_topics("AI Marketing", 10)
for topic in topics:
    print(f"  {topic['title']} — {topic['difficulty']}")

# Get calendar
calendar = agent.get_calendar(start_date="2024-01-01", end_date="2024-03-31")
print(f"Total entries: {len(calendar)}")

# Get summary
summary = agent.get_calendar_summary()
print(f"Scheduled: {summary['scheduled']}, Published: {summary['published']}")
```

### Social Media

```python
# Generate post
post = agent.generate_social_post("twitter", "AI is transforming content marketing...")
print(f"Characters: {post['character_count']}")
print(f"Hashtags: {post['hashtags']}")
print(f"Text: {post['text']}")

# Generate thread
thread = agent.generate_social_thread("AI Content Marketing", tweet_count=5)
for i, tweet in enumerate(thread):
    print(f"Tweet {i+1}/{len(thread)}: {tweet['text'][:60]}...")
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
    likes=80,
)

# Get performance
perf = agent.get_content_performance("abc123")
print(f"Engagement: {perf['latest']['engagement_rate']:.1%}")
print(f"CTR: {perf['latest']['ctr']:.1%}")

# Top performers
top = agent.get_top_performing(limit=5)
for item in top:
    print(f"  {item['title']}: {item['engagement_rate']:.1%} engagement")
```

## API Reference

### ContentAgent

| Method | Parameters | Returns |
|--------|-----------|---------|
| `generate_content()` | topic, content_type, tone, target_audience, keywords | Content dict |
| `analyze_seo()` | content_id, keywords | SEO metrics dict |
| `moderate_content()` | content_id | Moderation result dict |
| `add_calendar_entry()` | title, content_type, platform, scheduled_date, author, keywords | Calendar entry dict |
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

| Type | Description | Best For | Typical Length |
|------|-------------|----------|----------------|
| `blog_post` | Long-form educational | SEO, thought leadership | 800-2000 words |
| `article` | News or analysis | Industry updates | 600-1500 words |
| `social_media` | Short-form engagement | Brand awareness | 50-280 chars |
| `email` | Direct communication | Nurturing, conversion | 200-500 words |
| `landing_page` | Conversion-focused | Lead generation | 300-800 words |
| `video_script` | Video outline | YouTube, social video | 500-2000 words |
| `whitepaper` | In-depth research | Gated content | 2000-5000 words |
| `case_study` | Success story | Social proof | 800-1500 words |
| `documentation` | Technical reference | Product support | 500-5000 words |
| `newsletter` | Regular digest | Subscriber retention | 400-1200 words |

## Data Models

### ContentPiece
Complete content with title, body, SEO metadata, status, and performance tracking fields.

### SEOMetrics
SEO analysis with keyword density breakdown, readability score, structure analysis, and prioritized recommendations.

### ContentPerformance
Performance metrics including views, engagement rate, CTR, conversion rate, and historical data.

### CalendarEntry
Scheduled content with platform, author, keywords, and status tracking.

### SocialPost
Platform-optimized social media content with character count, hashtags, and thread support.

## Configuration

```python
config = {
    "default_tone": "professional",
    "default_audience": "general",
    "min_word_count": 300,
    "max_word_count": 5000,
    "seo_target_score": 70,
    "moderation_threshold": 0.7,
    "default_platform": "website",
    "enable_auto_moderation": True,
    "content_store_limit": 10000,
    "calendar_entry_limit": 5000,
    "performance_record_limit": 100000,
}
agent = ContentAgent(config)
```

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `default_tone` | `"professional"` | Default tone for content generation |
| `default_audience` | `"general"` | Default target audience |
| `min_word_count` | `300` | Minimum word count for content |
| `max_word_count` | `5000` | Maximum word count for content |
| `seo_target_score` | `70` | Target SEO score for recommendations |
| `moderation_threshold` | `0.7` | Minimum score to approve content |
| `default_platform` | `"website"` | Default platform for publishing |
| `enable_auto_moderation` | `True` | Auto-moderate on generation |
| `content_store_limit` | `10000` | Maximum content pieces in store |
| `calendar_entry_limit` | `5000` | Maximum calendar entries |
| `performance_record_limit` | `100000` | Maximum performance records |

## Examples

### Full Content Workflow

```python
from agents.content.agent import ContentAgent

agent = ContentAgent()

# 1. Generate content
content = agent.generate_content(
    topic="10 SEO Tips for 2024",
    content_type="blog_post",
    tone="professional",
    target_audience="small business owners",
    keywords=["SEO tips", "search engine optimization", "SEO 2024"],
)

# 2. Check SEO
seo = agent.analyze_seo(content["id"])
print(f"Initial SEO score: {seo['overall_score']}")

# 3. Moderate
mod = agent.moderate_content(content["id"])
if mod["approved"]:
    # 4. Schedule
    agent.add_calendar_entry(
        title=content["title"],
        content_type="blog_post",
        platform="website",
        scheduled_date="2024-02-01",
        author="Content Team",
    )

    # 5. Record initial metrics
    agent.record_performance(content["id"], views=0, clicks=0)

    print(f"Content scheduled: {content['title']}")
else:
    print(f"Content needs revision: {mod['suggestions']}")
```

### Multi-Platform Content

```python
# Generate base content
base = "AI is revolutionizing content marketing by enabling..."

# Adapt for each platform
twitter = agent.generate_social_post("twitter", base)
linkedin = agent.generate_social_post("linkedin", base)
instagram = agent.generate_social_post("instagram", base)

print(f"Twitter ({twitter['character_count']} chars): {twitter['text']}")
print(f"LinkedIn: {linkedin['text'][:100]}...")
print(f"Instagram: {instagram['text'][:100]}...")
```

## Best Practices

1. **Know Your Audience** — Research and understand your target audience deeply before writing
2. **Provide Value** — Every piece of content should offer genuine, actionable value
3. **Optimize for SEO** — Balance SEO keywords with natural, engaging writing
4. **Be Authentic** — Maintain a consistent, authentic brand voice across all content
5. **Test and Iterate** — Continuously refine based on performance data
6. **Plan Ahead** — Use the calendar to maintain consistent publishing cadence
7. **Repurpose Content** — Adapt high-performing content for multiple platforms
8. **Monitor Performance** — Track metrics weekly and adjust strategy monthly
9. **Quality Check** — Always run moderation before publishing
10. **Document Style** — Create and maintain a brand style guide

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Content too generic | Add specific audience pain points, examples, and data |
| SEO score low | Follow SEO recommendations, add keywords naturally in headings and body |
| Content flagged | Review flagged terms and remove or replace with alternatives |
| Low engagement | Adjust tone for platform, add stronger CTAs, test different headlines |
| Calendar gaps | Use topic suggestion engine, batch-create content monthly |
| Social post too long | Trim to platform limits or split into thread format |
| Reading time wrong | Verify word count calculation, check for special characters |
| Hashtag count off | Limit to 2-3 for Twitter, 5-10 for Instagram, 3-5 for LinkedIn |

## Files

- `agent.py` — Main implementation (~900 lines)
- `ARCHITECTURE.md` — System architecture with diagrams and component details
- `GROK.md` — Agent instructions, identity, and API reference
- `README.md` — This file

## Contributing

1. Add new content type templates with platform-specific rules
2. Enhance SEO analysis algorithms (semantic analysis, competitor comparison)
3. Add new platform integrations (TikTok, Pinterest, YouTube)
4. Improve moderation rules and brand compliance checking
5. Add A/B testing support for content variants
6. Update documentation for API changes

## License

Part of the Awesome Grok Skills collection. See project root for license details.