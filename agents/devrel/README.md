# DevRel Agent

Developer relations management — community building, content strategy, event management, documentation assessment, developer experience metrics, and feedback analysis.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Community Management](#community-management)
  - [Content Strategy](#content-strategy)
  - [Event Management](#event-management)
  - [Feedback Analysis](#feedback-analysis)
  - [Documentation Assessment](#documentation-assessment)
  - [DX Metrics](#dx-metrics)
  - [Developer Journey](#developer-journey)
  - [Reporting](#reporting)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The DevRel Agent provides a comprehensive platform for managing developer relations — from community growth and content performance to event impact, feedback analysis, documentation quality, and developer experience measurement. It tracks the full developer journey from first contact to advocacy, providing data-driven insights to optimize engagement and product adoption.

**Key capabilities:**
- Multi-platform community management (Discord, GitHub, Slack, Stack Overflow, etc.)
- Content lifecycle management with engagement analytics
- Event planning, execution, and post-event analysis
- Automated feedback categorization and sentiment analysis
- Documentation quality assessment with actionable issues
- Developer experience (DX) scoring against targets
- Developer journey mapping through adoption stages
- Comprehensive reporting with highlights, concerns, and recommendations

---

## Features

| Feature | Description |
|---------|-------------|
| **Community Management** | Track members across 12+ platforms with engagement metrics |
| **Content Strategy** | Content lifecycle, cross-posting, engagement tracking |
| **Event Management** | Full event lifecycle with attendance and satisfaction metrics |
| **Feedback Analysis** | Auto-categorization, sentiment analysis, priority assignment |
| **Documentation Assessment** | Quality scoring across 6 dimensions with issue tracking |
| **DX Metrics** | Score against targets for key developer experience indicators |
| **Developer Journey** | Map developers through 9 adoption stages |
| **Reporting** | Aggregate insights with highlights, concerns, recommendations |

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                      DEVREL AGENT                         │
├──────────────────────────────────────────────────────────┤
│  Community → Content → Events → Feedback                 │
│  → Documentation → DX Metrics → Journey → Reporting      │
└──────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for full system architecture.

---

## Quick Start

```python
from agents.devrel.agent import (
    DevRelAgent, Platform, ContentType, EventType,
    ContentStatus, EventStatus, JourneyStage,
)

agent = DevRelAgent()

# Add a community member
member = agent.add_member("Alice", Platform.DISCORD, tags=["python"])

# Create content
content = agent.create_content(
    "Quickstart Guide", ContentType.QUICKSTART,
    author="Alice", word_count=1000,
)

# Collect feedback
feedback = agent.add_feedback("Love the API! Very intuitive.")

# Generate report
report = agent.generate_report()
print(report.recommendations)
```

---

## Installation

```bash
cd Awesome-Grok-Skills
pip install -e .
```

Or run directly:

```bash
python agents/devrel/agent.py
```

**Requirements:** Python 3.10+, no external dependencies.

---

## Usage

### Community Management

```python
agent = DevRelAgent()

# Add members across platforms
agent.add_member("Alice", Platform.DISCORD, tags=["python", "api"])
agent.add_member("Bob", Platform.GITHUB, tags=["go", "cli"])
agent.add_member("Charlie", Platform.STACK_OVERFLOW, tags=["rust"])

# Track journey progression
agent.track_journey("alice-id", JourneyStage.REGULAR_USAGE)
agent.track_journey("bob-id", JourneyStage.ADVOCACY)

# Compute metrics
metrics = agent.compute_community_metrics()
print(f"Total: {metrics.total_members}")
print(f"Active: {metrics.active_members}")
print(f"Retention: {metrics.retention_rate:.0%}")
print(f"NPS: {metrics.nps_score}")
print(f"Top contributors: {metrics.top_contributors}")
print(f"By platform: {metrics.platform_breakdown}")
```

### Content Strategy

```python
# Create content
tutorial = agent.create_content(
    title="Building Your First App",
    content_type=ContentType.TUTORIAL,
    author="Alice",
    platforms=[Platform.BLOG, Platform.DEV_TO, Platform.MEDIUM],
    tags=["tutorial", "beginner", "app"],
    word_count=2500,
)

quickstart = agent.create_content(
    title="5-Minute Quickstart",
    content_type=ContentType.QUICKSTART,
    author="Bob",
    word_count=800,
)

# Track engagement
agent.record_content_engagement(tutorial.content_id, views=8000, likes=400, shares=120, comments=45)
agent.record_content_engagement(quickstart.content_id, views=12000, likes=600, shares=200, comments=60)

# Publish
agent.update_content_status(tutorial.content_id, ContentStatus.PUBLISHED)
agent.update_content_status(quickstart.content_id, ContentStatus.PUBLISHED)

# Analyze
analytics = agent.compute_content_analytics()
print(f"Published: {analytics['published']}")
print(f"Total views: {analytics['total_views']}")
print(f"Engagement rate: {analytics['engagement_rate']:.2%}")
for ctype, data in analytics['by_type'].items():
    print(f"  {ctype}: {data['count']} posts, {data['total_views']} views")
```

### Event Management

```python
# Create events
workshop = agent.create_event(
    name="Advanced API Workshop",
    event_type=EventType.WORKSHOP,
    speakers=["Alice", "Bob"],
    topics=["API", "REST", "Authentication"],
    is_virtual=True,
    max_attendees=100,
)

meetup = agent.create_event(
    name="Monthly Community Meetup",
    event_type=EventType.MEETUP,
    topics=["Community", "Roadmap"],
    is_virtual=True,
)

# Complete events with feedback
agent.update_event_status(workshop.event_id, EventStatus.COMPLETED)
agent.record_event_feedback(workshop.event_id, attended_count=78, satisfaction_score=4.6, nps_score=75)

agent.update_event_status(meetup.event_id, EventStatus.COMPLETED)
agent.record_event_feedback(meetup.event_id, attended_count=45, satisfaction_score=4.2, nps_score=60)

# Analyze
analytics = agent.compute_event_analytics()
print(f"Completed: {analytics['completed']}")
print(f"Attendance rate: {analytics['attendance_rate']:.0%}")
print(f"Satisfaction: {analytics['avg_satisfaction']}/5.0")
print(f"NPS: {analytics['avg_nps']}")
```

### Feedback Analysis

```python
# Add feedback (auto-categorized and sentiment-analyzed)
f1 = agent.add_feedback("This SDK is amazing! Best DX I've seen.", author="Charlie")
f2 = agent.add_feedback("Bug: crash when importing with Python 3.12", author="Diana")
f3 = agent.add_feedback("Please add GraphQL support", author="Eve")
f4 = agent.add_feedback("The docs are confusing for beginners", author="Frank")

# Review classifications
for f in [f1, f2, f3, f4]:
    print(f"[{f.feedback_type.value}] {f.sentiment.value}: {f.message[:40]}...")

# Analytics
analytics = agent.compute_feedback_analytics()
print(f"Total: {analytics['total_feedback']}")
print(f"By type: {analytics['by_type']}")
print(f"By sentiment: {analytics['by_sentiment']}")
print(f"Positive ratio: {analytics['positive_ratio']:.0%}")
print(f"Resolution rate: {analytics['resolution_rate']:.0%}")

# Resolve feedback
agent.resolve_feedback(f2.feedback_id)
```

### Documentation Assessment

```python
# Add pages for assessment
agent.add_documentation_page(
    "Getting Started", "/docs/quickstart",
    section="getting-started", word_count=1200,
    has_code_examples=True, has_tutorial=True,
    has_troubleshooting=True, has_changelog=True,
)

agent.add_documentation_page(
    "API Reference", "/docs/api",
    section="api", word_count=5000,
    has_code_examples=True, has_api_reference=True,
)

agent.add_documentation_page(
    "Authentication", "/docs/auth",
    section="security", word_count=800,
    has_code_examples=False, has_tutorial=False,
    has_troubleshooting=False,
)

# Assess all
assessment = agent.assess_documentation()
print(f"Total pages: {assessment['total_pages']}")
print(f"Quality: {assessment['quality_distribution']}")
print(f"Pages needing update: {assessment['pages_needing_update']}")
for page in assessment['worst_pages']:
    print(f"  {page.title}: {page.quality.value} - {page.issues[:2]}")
```

### DX Metrics

```python
# Record metrics against targets
agent.record_dx_metric("time_to_first_hello_world", 4.2, "minutes", target=5.0)
agent.record_dx_metric("api_adoption_rate", 0.32, "ratio", target=0.30)
agent.record_dx_metric("community_growth_rate", 0.15, "ratio", target=0.10)
agent.record_dx_metric("docs_coverage", 0.88, "ratio", target=0.90)
agent.record_dx_metric("support_response_time", 3.5, "hours", target=4.0)

# Compute DX score
dx = agent.compute_dx_score()
print(f"Overall DX Score: {dx['overall_score']}")
print(f"On target: {dx['on_target']}/{dx['metrics_count']}")
for m in dx['metrics']:
    status = "PASS" if m['target'] and (
        (m['name'] == 'time_to_first_hello_world' and m['value'] <= m['target']) or
        (m['name'] != 'time_to_first_hello_world' and m['value'] >= m['target'])
    ) else "MISS"
    print(f"  {m['name']}: {m['value']} {m['unit']} (target: {m['target']}) [{status}]")
```

### Developer Journey

```python
# Track a developer's progression
dev_id = "dev-456"
agent.track_journey(dev_id, JourneyStage.AWARENESS)
agent.track_journey(dev_id, JourneyStage.INTEREST)
agent.track_journey(dev_id, JourneyStage.EVALUATION)
agent.track_journey(dev_id, JourneyStage.ONBOARDING)
agent.track_journey(dev_id, JourneyStage.FIRST_SUCCESS)
agent.track_journey(dev_id, JourneyStage.REGULAR_USAGE)

journey = agent.get_journey(dev_id)
print(f"Stage: {journey.current_stage.value}")
print(f"Completed: {[s.value for s in journey.stages_completed]}")

# Analytics across all developers
analytics = agent.compute_journey_analytics()
print(f"Total developers: {analytics['total_developers']}")
print(f"Stage distribution: {analytics['stage_distribution']}")
print(f"At advocacy: {analytics['at_advocacy']}")
```

### Reporting

```python
# Generate comprehensive report
report = agent.generate_report(period="monthly")

print(f"Report ID: {report.report_id}")
print(f"\nHighlights:")
for h in report.highlights:
    print(f"  + {h}")
print(f"\nConcerns:")
for c in report.concerns:
    print(f"  - {c}")
print(f"\nRecommendations:")
for r in report.recommendations:
    print(f"  * {r}")
```

---

## API Reference

### DevRelAgent

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `add_member` | name, platform, email?, tags?, journey_stage? | CommunityMember | Add community member |
| `get_member` | member_id | CommunityMember | Get member by ID |
| `list_members` | platform?, stage?, limit? | List[CommunityMember] | List with filters |
| `compute_community_metrics` | period? | CommunityMetrics | Aggregate metrics |
| `create_content` | title, type, author, platforms, tags, word_count? | ContentItem | Create content |
| `get_content` | content_id | ContentItem | Get content by ID |
| `update_content_status` | content_id, status | ContentItem | Update status |
| `record_content_engagement` | content_id, views, likes, shares, comments, bookmarks | ContentItem | Record engagement |
| `list_content` | type?, status?, platform?, limit? | List[ContentItem] | List with filters |
| `compute_content_analytics` | - | Dict | Content performance |
| `create_event` | name, type, date?, is_virtual, **kwargs | DeveloperEvent | Create event |
| `get_event` | event_id | DeveloperEvent | Get event by ID |
| `update_event_status` | event_id, status | DeveloperEvent | Update status |
| `record_event_feedback` | event_id, attended, satisfaction, nps? | DeveloperEvent | Post-event feedback |
| `list_events` | type?, status?, limit? | List[DeveloperEvent] | List with filters |
| `compute_event_analytics` | - | Dict | Event performance |
| `add_feedback` | message, source, author, type? | FeedbackItem | Add feedback |
| `list_feedback` | type?, sentiment?, priority?, status?, limit? | List[FeedbackItem] | List with filters |
| `resolve_feedback` | feedback_id | FeedbackItem | Mark resolved |
| `compute_feedback_analytics` | - | Dict | Feedback analytics |
| `add_documentation_page` | title, url, section, **kwargs | DocumentationPage | Add doc page |
| `assess_documentation` | - | Dict | Quality assessment |
| `record_dx_metric` | name, value, unit, category, target | DXMetric | Record metric |
| `compute_dx_score` | - | Dict | Overall DX score |
| `track_journey` | developer_id, stage | DeveloperJourney | Track progression |
| `get_journey` | developer_id | DeveloperJourney? | Get journey |
| `compute_journey_analytics` | - | Dict | Journey analytics |
| `generate_report` | period? | DevRelReport | Full report |
| `get_status` | - | Dict | Agent status |

---

## Examples

### Example 1: Launch Campaign

```python
agent = DevRelAgent()

# Build community
for name, platform in [("Alice", Platform.DISCORD), ("Bob", Platform.GITHUB)]:
    agent.add_member(name, platform)

# Create launch content
agent.create_content("Introducing v2.0", ContentType.RELEASE_ANNOUNCEMENT,
                     platforms=[Platform.BLOG, Platform.TWITTER])
agent.create_content("Migration Guide v1 to v2", ContentType.HOW_TO,
                     word_count=3000)
agent.create_content("5-Minute Quickstart v2", ContentType.QUICKSTART,
                     word_count=800)

# Plan launch event
agent.create_event("v2.0 Launch Webinar", EventType.WEBINAR,
                   topics=["v2.0", "New Features", "Migration"])

# Generate report
report = agent.generate_report()
print(report.recommendations)
```

### Example 2: Quarterly Review

```python
report = agent.generate_report(period="quarterly")
print(f"Community: {report.community_metrics.total_members} members "
      f"({report.community_metrics.new_members} new)")
print(f"Content: {report.content_summary['published']} published, "
      f"{report.content_summary['total_views']} views")
print(f"Events: {report.event_summary['completed']} completed, "
      f"satisfaction: {report.event_summary['avg_satisfaction']}")
print(f"Feedback: {report.feedback_summary['total_feedback']} items, "
      f"positive: {report.feedback_summary['positive_ratio']:.0%}")
```

---

## Configuration

```python
config = DevRelConfig(
    min_response_time_hours=4.0,
    target_retention_rate=0.70,
    target_nps=50.0,
    target_posts_per_week=3,
    target_satisfaction_score=4.0,
    response_sla_hours=24.0,
    freshness_days=90,
    target_time_to_first_hello_world=5.0,
    target_api_adoption_rate=0.30,
    target_community_growth_rate=0.10,
)
agent = DevRelAgent(config)
```

---

## Best Practices

1. **Track everything** — Community growth, content engagement, event impact
2. **Respond fast** — Meet your SLA for feedback response
3. **Measure sentiment** — Track developer happiness trends
4. **Update documentation** — Keep it fresh within 90 days
5. **Mix content types** — Tutorials, how-tos, quickstarts, videos
6. **Run regular events** — Monthly meetups, quarterly workshops
7. **Empower advocates** — Recognize top contributors publicly
8. **Close the feedback loop** — Tell developers when their feedback leads to changes
9. **Review monthly** — Use reports to guide strategy
10. **Track the journey** — Understand where developers drop off

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Low retention rate | Check response times, review content quality, analyze feedback |
| Negative sentiment trending | Analyze feedback categories, check recent changes, communicate roadmap |
| Low content engagement | Review titles for SEO, check distribution, analyze format preferences |
| Documentation quality declining | Set freshness alerts, add code examples, include troubleshooting |
| Low event attendance | Promote earlier, choose better times, offer recordings |
| DX score below target | Review individual metrics, prioritize lowest-scoring areas |

---

## Contributing

Guidelines:
1. Add new platforms via `Platform` enum
2. Add new content types via `ContentType` enum
3. Add new event types via `EventType` enum
4. Extend sentiment lexicon for better accuracy
5. Add new DX metric categories
6. Include type hints for all public methods
7. Test edge cases: empty communities, no events, new feedback

---

## License

MIT License — See [LICENSE](../../LICENSE) for details.
