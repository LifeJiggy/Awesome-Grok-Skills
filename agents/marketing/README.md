# Marketing Strategy Agent

End-to-end marketing strategy, campaign management, audience targeting, budget allocation, attribution, and ROI optimization.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

The Marketing Strategy Agent provides a complete marketing automation platform covering the full campaign lifecycle. From audience segmentation and campaign creation to multi-touch attribution and ROI analysis, this agent enables data-driven marketing decisions with measurable outcomes.

### Key Capabilities

| Capability | Description |
|-----------|-------------|
| Audience Segmentation | Create, combine, and score customer segments |
| Campaign Management | Full lifecycle from draft to completion |
| Budget Allocation | Data-driven spend distribution across channels |
| Multi-Touch Attribution | 6 attribution models for conversion credit |
| Content Generation | Template-based content with brand voice |
| Analytics Dashboard | Event tracking, goals, and reporting |
| SEO Analysis | Keyword density, SERP preview, content scoring |

---

## Features

### Audience Management
- Support for 6 segment types: behavioral, demographic, geographic, psychographic, technographic, predictive
- Segment combination via intersect, union, or exclude operations
- Automated segment scoring based on size, growth, and criteria depth

### Campaign Lifecycle
- State machine with validated transitions: draft, scheduled, active, paused, completed, archived
- Event hooks for on_launch, on_pause, and on_complete callbacks
- Conversion event recording with per-campaign attribution

### Budget Optimization
- Equal split, performance-based, and custom allocation strategies
- Historical ROI tracking per channel
- Reallocation recommendations based on performance thresholds

### Attribution Models
- First Touch, Last Touch, Linear, Time Decay, Position-Based, Data-Driven
- Per-user and aggregated attribution views
- Confidence scoring based on touchpoint diversity

### Content Creation
- Template rendering with variable substitution
- Platform-aware content with character limits
- A/B variant generation

### Analytics
- Event tracking with custom properties
- Goal setting and progress monitoring
- Funnel conversion analysis
- Configurable reporting periods

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│              MarketingAgent (Facade)             │
├─────────────────────────────────────────────────┤
│  AudienceManager  │  CampaignManager            │
│  BudgetAllocator  │  AttributionEngine          │
│  ContentGenerator │  AnalyticsDashboard         │
│  SEOAnalyzer                                    │
└─────────────────────────────────────────────────┘
```

Each component operates independently with its own state and can be used standalone or through the `MarketingAgent` orchestrator.

---

## Quick Start

### Installation

```bash
pip install awesome-grok-skills
```

### Minimal Example

```python
from agents.marketing.agent import MarketingAgent, Channel, AudienceType

# Initialize
agent = MarketingAgent()

# Create audience
seg = agent.audience.create_segment(
    name="Target Users",
    audience_type=AudienceType.DEMOGRAPHIC,
    criteria={"age": "25-45"},
    estimated_size=50000
)

# Create and launch campaign
campaign = agent.campaigns.create_campaign(
    name="Spring Launch",
    channel=Channel.EMAIL,
    audience_segments=[seg.segment_id],
    content={"subject": "New Arrivals", "body": "Check them out"},
    budget=5000
)
agent.campaigns.launch_campaign(campaign.campaign_id)

# Get metrics
metrics = agent.campaigns.get_campaign_metrics(campaign.campaign_id)
print(f"ROI: {metrics['roi']:.1f}%")
```

---

## Usage

### Running the Agent

```bash
python agents/marketing/agent.py
```

### Programmatic Access

```python
from agents.marketing.agent import MarketingAgent

agent = MarketingAgent()

# Each component can be used independently
segments = agent.audience.list_segments()
campaigns = agent.campaigns.list_campaigns()
report = agent.analytics.generate_report()
```

---

## API Reference

### MarketingAgent

| Method | Description |
|--------|-------------|
| `full_campaign_lifecycle(name, channel, segments, budget, content)` | End-to-end campaign execution |
| `run_attribution_analysis()` | Get aggregated channel attribution |
| `optimize_budget()` | Get reallocation recommendations |
| `generate_dashboard_report()` | Generate analytics report |

### AudienceManager

| Method | Description |
|--------|-------------|
| `create_segment(name, type, criteria, size, tags)` | Create new segment |
| `combine_segments(name, ids, operation)` | Combine multiple segments |
| `score_segment(segment_id)` | Score segment quality |
| `update_segment(segment_id, **kwargs)` | Update segment fields |
| `delete_segment(segment_id)` | Remove segment |

### CampaignManager

| Method | Description |
|--------|-------------|
| `create_campaign(name, channel, segments, content, budget)` | Create campaign |
| `launch_campaign(campaign_id)` | Start campaign |
| `pause_campaign(campaign_id)` | Pause active campaign |
| `resume_campaign(campaign_id)` | Resume paused campaign |
| `complete_campaign(campaign_id)` | Mark campaign complete |
| `get_campaign_metrics(campaign_id)` | Get performance metrics |
| `record_conversion(event)` | Record conversion event |

### BudgetAllocator

| Method | Description |
|--------|-------------|
| `create_allocation(total, channel_budgets, strategy)` | Create allocation |
| `equal_split(budget, channels)` | Equal distribution |
| `performance_based_split(budget, channel_rois)` | ROI-weighted split |
| `recommend_reallocation()` | Get optimization suggestions |

### AttributionEngine

| Method | Description |
|--------|-------------|
| `add_touchpoint(user, channel, timestamp, value)` | Record touchpoint |
| `calculate_attribution(user_id)` | Calculate per-user attribution |
| `get_aggregated_attribution()` | Get cross-user attribution |

### ContentGenerator

| Method | Description |
|--------|-------------|
| `set_brand_voice(tone, keywords)` | Configure brand voice |
| `add_template(id, template)` | Register template |
| `render(template_id, variables)` | Render template |
| `generate_email(subject, body, vars)` | Create email |
| `generate_social_post(platform, message)` | Create social post |

### AnalyticsDashboard

| Method | Description |
|--------|-------------|
| `track_event(type, properties)` | Track custom event |
| `set_goal(id, metric, target)` | Set performance goal |
| `generate_report(days)` | Generate report |
| `get_funnel(stages)` | Analyze conversion funnel |

### SEOAnalyzer

| Method | Description |
|--------|-------------|
| `analyze_keyword(keyword, content)` | Analyze keyword usage |
| `serp_preview(title, desc, url, keyword)` | Generate SERP preview |
| `content_score(title, body, keyword)` | Score content SEO |

---

## Examples

### Multi-Channel Campaign

```python
agent = MarketingAgent()

# Create segments for each channel
email_seg = agent.audience.create_segment("Email Subscribers", AudienceType.BEHAVIORAL, {"opt_in": True}, 30000)
social_seg = agent.audience.create_segment("Social Followers", AudienceType.BEHAVIORAL, {"followed": True}, 50000)

# Launch parallel campaigns
email = agent.campaigns.create_campaign("Email Blast", Channel.EMAIL, [email_seg.segment_id], {}, 3000)
social = agent.campaigns.create_campaign("Social Push", Channel.SOCIAL, [social_seg.segment_id], {}, 5000)

# Allocate budget
agent.budget.create_allocation(8000, {"email": 3000, "social": 5000})
```

### Attribution Analysis

```python
engine = AttributionEngine(model=AttributionModel.TIME_DECAY)

# Record a customer journey
engine.add_touchpoint("u1", "social", datetime(2025, 1, 1))
engine.add_touchpoint("u1", "email", datetime(2025, 1, 5))
engine.add_touchpoint("u1", "search", datetime(2025, 1, 8))
engine.add_touchpoint("u1", "email", datetime(2025, 1, 10), value=199.99)

result = engine.calculate_attribution("u1")
print(result.channel_scores)
```

### Budget Optimization

```python
allocator = BudgetAllocator()

# Record historical performance
allocator.record_performance("email", ROIMetric(channel="email", revenue=15000, cost=3000, roi=400))
allocator.record_performance("social", ROIMetric(channel="social", revenue=8000, cost=4000, roi=100))
allocator.record_performance("search", ROIMetric(channel="search", revenue=20000, cost=5000, roi=300))

# Get recommendations
recs = allocator.recommend_reallocation()
```

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MARKETING_LOG_LEVEL` | Logging verbosity | `INFO` |
| `MARKETING_DEFAULT_MODEL` | Attribution model | `linear` |
| `MARKETING_BUDGET_THRESHOLD` | ROI alert threshold | `50` |

### Strategy Selection

```python
from agents.marketing.agent import BudgetStrategy

# Choose strategy based on data availability
if has_historical_data:
    strategy = BudgetStrategy.PERFORMANCE_BASED
elif is_seasonal_business:
    strategy = BudgetStrategy.SEASONAL_ADJUST
else:
    strategy = BudgetStrategy.EQUAL_SPLIT
```

---

## Best Practices

### Audience Segmentation
- Start with broad segments and narrow based on performance data
- Use intersect operations to create high-intent micro-segments
- Review and refresh segments monthly
- Track segment growth rates to identify expanding opportunities

### Campaign Management
- Always define success metrics before launch
- Use A/B testing for subject lines, content, and CTAs
- Set up conversion tracking from day one
- Complete campaigns promptly to keep metrics accurate

### Budget Allocation
- Never allocate 100% of budget — reserve 10-15% for testing
- Review performance weekly and reallocate monthly
- Use performance-based allocation once you have 30+ days of data
- Track CPA alongside ROI to avoid profitable-but-expensive channels

### Attribution
- Start with linear attribution and iterate toward data-driven
- Ensure consistent UTM parameter naming across channels
- Account for cross-device journeys in attribution logic
- Use time-decay for fast-moving B2C, position-based for B2B

### Content
- Maintain brand voice consistency across all channels
- Respect platform character limits automatically
- Always generate A/B variants for testing
- Track content performance by engagement metrics

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Segment size is 0 | Criteria too restrictive | Broaden criteria or combine segments |
| Campaign won't launch | Invalid state transition | Check current status, resume if paused |
| ROI shows 0% | No conversions recorded | Verify conversion tracking setup |
| Attribution scores don't sum to 1 | Model rounding | Expected for time-decay; use aggregated view |
| Budget allocation fails | Allocated exceeds total | Ensure channel budgets sum to <= total |
| Content exceeds platform limit | Message too long | Use `generate_social_post` for auto-truncation |
| SEO density too high | Keyword stuffing | Rephrase to use natural language variations |

---

## License

MIT License - see [LICENSE](../../LICENSE) for details.
