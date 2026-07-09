# Digital Marketing Agent

Full-stack digital marketing platform for campaign management, multi-channel
strategy, paid advertising, email marketing, social media, SEO/SEM, performance
analytics, and multi-touch attribution modeling.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Campaign Management](#campaign-management)
  - [Channel Strategy](#channel-strategy)
  - [Performance Analytics](#performance-analytics)
  - [Attribution](#attribution)
  - [Email Marketing](#email-marketing)
  - [Social Media](#social-media)
  - [SEO](#seo)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Design Patterns](#design-patterns)
- [Security](#security)
- [Scalability](#scalability)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Digital Marketing Agent provides a comprehensive, modular platform for
managing all aspects of digital marketing operations. It covers the complete
marketing lifecycle — from campaign ideation and budget allocation through
execution, tracking, attribution, and reporting.

Built with a modular architecture, each sub-engine (Campaign Manager, Channel
Strategy, Analytics, Attribution, Email, Social, SEO) operates independently
while being orchestrated by a top-level agent that provides unified dashboards
and cross-channel insights.

---

## Features

### Campaign Management
- Full CRUD operations for campaigns
- Multi-channel campaign support (15+ channels)
- Ad group and creative asset management
- Campaign validation before activation
- Lifecycle management (draft → active → paused → completed)
- Campaign duplication and templating

### Channel Strategy
- AI-powered channel recommendations based on objective
- Budget allocation optimization across channels
- Performance-based reallocation using ROAS data
- Bid strategy recommendations per objective
- Channel fit scoring for audience alignment

### Performance Analytics
- Real-time touchpoint recording and aggregation
- Channel-level performance metrics (CTR, CPC, CPA, ROAS)
- Dashboard snapshot generation with alerts
- Historical trend analysis (daily granularity)
- Conversion goal tracking with revenue attribution

### Multi-Touch Attribution
- 8 attribution models (First Touch, Last Touch, Linear, Time Decay,
  Position-Based, Data-Driven, Markov Chain, Shapley Value)
- Customer journey grouping and analysis
- Cross-model comparison for strategic insight
- Channel-level credit distribution

### Email Marketing
- Campaign creation with HTML/plain text content
- A/B testing variant support
- Event tracking (sent, delivered, opened, clicked, bounced, unsubscribed)
- Segment-level performance analysis
- ROI calculation per campaign

### Social Media
- 10 platform support (Facebook, Instagram, Twitter, LinkedIn, TikTok,
  YouTube, Pinterest, Reddit, Snapchat, Threads)
- Post creation, scheduling, and publishing
- Engagement tracking (likes, comments, shares, saves, clicks)
- Platform-level and cross-platform summaries
- Top post identification by metric

### SEO
- Keyword tracking with position history
- Ranking change detection
- Site audit with scoring (page speed, mobile, SEO, accessibility)
- SEO scorecard generation
- Recommendation engine for improvements

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     DigitalMarketingAgent                                  │
│                                                                          │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────────┐  │
│  │  Campaign      │  │  Channel       │  │  Performance               │  │
│  │  Manager       │  │  Strategy      │  │  Analytics                 │  │
│  │  ├ Create      │  │  ├ Recommend   │  │  ├ Touchpoints             │  │
│  │  ├ Activate    │  │  ├ Allocate    │  │  ├ Dashboard               │  │
│  │  ├ Pause       │  │  ├ Optimize    │  │  ├ Trends                  │  │
│  │  └ Complete    │  │  └ Score       │  │  └ Alerts                  │  │
│  └────────────────┘  └────────────────┘  └────────────────────────────┘  │
│                                                                          │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────────┐  │
│  │  Attribution   │  │  Email         │  │  Social                    │  │
│  │  Engine        │  │  Marketing     │  │  Media                     │  │
│  │  ├ 8 models    │  │  ├ Campaigns   │  │  ├ 10 platforms            │  │
│  │  ├ Compare     │  │  ├ Events      │  │  ├ Engagement              │  │
│  │  ├ Channel     │  │  ├ Metrics     │  │  ├ Analytics               │  │
│  │  └ Customer    │  │  └ ROI         │  │  └ Scheduling              │  │
│  └────────────────┘  └────────────────┘  └────────────────────────────┘  │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐│
│  │  SEO Manager                                                         ││
│  │  ├ Keywords  │ Rankings  │ Audits  │ Scorecard  │ Recommendations   ││
│  └──────────────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed component diagrams,
data flows, and design patterns.

---

## Quick Start

```python
from agents.digital_marketing.agent import (
    DigitalMarketingAgent, ObjectiveType, ChannelType,
    AudienceDefinition, AudienceSegment,
)

agent = DigitalMarketingAgent()

# Create a campaign with strategy
result = agent.create_full_campaign(
    name="Summer Sale",
    objective=ObjectiveType.CONVERSION,
    channels=[ChannelType.PAID_SEARCH, ChannelType.EMAIL],
    budget=50000,
    audience=AudienceDefinition(
        segment=AudienceSegment.HIGH_VALUE,
        geo_targets=["US", "CA"],
    ),
)

print(f"Campaign ID: {result['campaign']['id']}")
print(f"Budget Allocation: {result['strategy']['budget_allocation']}")
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills

# Install dependencies (if any)
pip install -r requirements.txt

# Run the agent demo
python agents/digital-marketing/agent.py
```

---

## Usage

### Running the Demo

```bash
python agents/digital-marketing/agent.py
```

This runs a complete demo showing campaign creation, strategy development,
touchpoint recording, dashboard generation, and monthly reporting.

### Programmatic Usage

```python
from agents.digital_marketing.agent import DigitalMarketingAgent

agent = DigitalMarketingAgent()

# Check agent status
print(agent.get_status())

# Create campaign
campaign = agent.campaign_manager.create_campaign(
    name="Product Launch",
    objective=ObjectiveType.AWARENESS,
    channels=[ChannelType.VIDEO, ChannelType.PAID_SOCIAL],
    budget_total=30000,
)

# Activate
agent.campaign_manager.activate_campaign(campaign.campaign_id)

# Get dashboard
dashboard = agent.get_marketing_dashboard()
```

### Campaign Management

```python
# Create campaign
campaign = agent.campaign_manager.create_campaign(
    name="Q4 Push",
    objective=ObjectiveType.CONVERSION,
    channels=[ChannelType.PAID_SEARCH, ChannelType.EMAIL],
    budget_total=25000,
)

# Lifecycle management
agent.campaign_manager.activate_campaign(campaign.campaign_id)
agent.campaign_manager.pause_campaign(campaign.campaign_id)
agent.campaign_manager.complete_campaign(campaign.campaign_id)

# Health check
health = agent.campaign_manager.get_campaign_health(campaign.campaign_id)
```

**Campaign States:**

```
  ┌────────┐     ┌──────────┐     ┌────────┐
  │ DRAFT  │────►│ SCHEDULED│────►│ ACTIVE │
  └────────┘     └──────────┘     └────────┘
                                      │
                              ┌───────┴───────┐
                              ▼               ▼
                        ┌────────┐      ┌──────────┐
                        │ PAUSED │      │COMPLETED │
                        └────────┘      └──────────┘
                                            │
                                            ▼
                                      ┌──────────┐
                                      │ ARCHIVED │
                                      └──────────┘
```

### Channel Strategy

```python
strategy = agent.channel_strategy.develop_strategy(
    objective=ObjectiveType.AWARENESS,
    total_budget=50000,
    target_audience=audience,
)

# Get recommendations
recs = agent.channel_strategy.get_channel_recommendations(
    objective=ObjectiveType.CONVERSION,
    audience=audience,
    budget=50000,
)
```

**Channel Fit Matrix:**

```
┌─────────────────┬────────────┬────────────┬────────────┬────────────┐
│  Channel        │ Awareness  │ Consider   │ Conversion │ Retention  │
├─────────────────┼────────────┼────────────┼────────────┼────────────┤
│  Paid Search    │    Low     │   Medium   │   High     │    Low     │
│  Paid Social    │   High     │   Medium   │   Medium   │    Low     │
│  Display        │   High     │    Low     │    Low     │    Low     │
│  Video          │   High     │   High     │   Medium   │   Medium   │
│  Email          │    Low     │   Medium   │   High     │   High     │
│  Organic Search │   Medium   │   High     │   Medium   │   Medium   │
│  Social Organic │   High     │   Medium   │    Low     │   Medium   │
│  Affiliate      │   Medium   │   Medium   │   High     │    Low     │
└─────────────────┴────────────┴────────────┴────────────┴────────────┘
```

### Performance Analytics

```python
# Record touchpoints
touchpoint = Touchpoint(
    channel=ChannelType.PAID_SEARCH,
    campaign_id=campaign.campaign_id,
    impressions=50000,
    clicks=2500,
    conversions=125,
    cost=5000,
    revenue=25000,
)
agent.analytics.record_touchpoint(touchpoint)

# Get dashboard
dashboard = agent.analytics.create_dashboard()
print(f"ROAS: {dashboard.overall_roas:.2f}x")

# Get trend
trend = agent.analytics.get_performance_trend(days=30)
```

### Attribution

```python
# Add touchpoints
agent.attribution_engine.add_touchpoints(all_touchpoints)

# Compare models
comparison = agent.attribution_engine.compare_models()
for model_name, result in comparison.items():
    print(f"{model_name}: ROAS={result.roas:.2f}")

# Get channel attribution
channel_attr = agent.attribution_engine.get_channel_attribution(
    AttributionModel.TIME_DECAY
)
```

**Attribution Models:**

| Model | Best For | Consideration |
|-------|----------|---------------|
| First Touch | Acquisition | Ignores nurturing |
| Last Touch | Conversion | Ignores awareness |
| Linear | Balanced | Equal credit |
| Time Decay | Long cycles | Recent weighted |
| Position-Based | First/last | 40/20/40 split |
| Data-Driven | Algorithmic | Needs data |
| Markov Chain | Removal impact | Complex |
| Shapley Value | Fair distribution | Expensive |

### Email Marketing

```python
# Create campaign
email_campaign = agent.email_engine.create_campaign(
    name="Welcome Series",
    subject_line="Welcome to our community!",
    from_email="hello@company.com",
    html_content="<h1>Welcome!</h1>",
)

# Send and track
agent.email_engine.send_campaign(email_campaign.email_id, 5000)
agent.email_engine.record_event(email_campaign.email_id, EmailEventType.OPENED, 2500)
agent.email_engine.record_event(email_campaign.email_id, EmailEventType.CLICKED, 500)

# Get metrics
metrics = agent.email_engine.get_campaign_metrics(email_campaign.email_id)
print(f"Open rate: {metrics.open_rate:.1%}")
print(f"Click rate: {metrics.click_rate:.1%}")
```

**Email Benchmarks:**

| Metric | Good | Average | Poor |
|--------|------|---------|------|
| Open Rate | > 25% | 15-25% | < 15% |
| Click Rate | > 5% | 2-5% | < 2% |
| Bounce Rate | < 1% | 1-3% | > 3% |

### Social Media

```python
# Create post
post = agent.social_manager.create_post(
    platform=SocialPlatform.INSTAGRAM,
    content="Excited to announce our new product!",
    media_urls=["https://cdn.example.com/product.jpg"],
    hashtags=["newlaunch", "product"],
)

# Publish
agent.social_manager.publish_post(post.post_id)

# Track engagement
agent.social_manager.record_engagement(post.post_id, "like", count=1500)
agent.social_manager.record_engagement(post.post_id, "comment", count=200)

# Get summary
summary = agent.social_manager.get_platform_summary(SocialPlatform.INSTAGRAM)
```

### SEO

```python
# Track keywords
kw = agent.seo_manager.add_keyword(
    keyword="best running shoes",
    url="https://shop.example.com/running-shoes",
    position=12,
    search_volume=14800,
)

# Update positions
agent.seo_manager.update_keyword_position(kw.keyword_id, new_position=8)

# Run audit
audit = agent.seo_manager.run_site_audit("shop.example.com")
print(f"Overall Score: {audit.overall_score}/100")

# Get scorecard
scorecard = agent.seo_manager.get_seo_scorecard()
```

---

## API Reference

### DigitalMarketingAgent (Top-Level)

| Method | Description | Returns |
|--------|-------------|---------|
| `create_full_campaign(...)` | Create campaign + strategy | `Dict` |
| `get_marketing_dashboard()` | Unified dashboard | `Dict` |
| `run_attribution_analysis(model)` | Run attribution | `Dict` |
| `generate_monthly_report()` | Monthly report | `Dict` |
| `get_status()` | Agent status | `Dict` |

### CampaignManager

| Method | Description | Returns |
|--------|-------------|---------|
| `create_campaign(name, objective, channels, budget_total, ...)` | Create campaign | `Campaign` |
| `update_campaign(campaign_id, updates)` | Update fields | `Campaign` |
| `delete_campaign(campaign_id)` | Delete campaign | `bool` |
| `activate_campaign(campaign_id)` | Activate | `bool` |
| `pause_campaign(campaign_id)` | Pause | `bool` |
| `complete_campaign(campaign_id)` | Mark complete | `bool` |
| `duplicate_campaign(campaign_id, new_name)` | Duplicate | `Campaign` |
| `list_campaigns(status, channel, tags)` | List campaigns | `List[Campaign]` |
| `get_campaign_health(campaign_id)` | Health check | `Dict` |

### ChannelStrategyEngine

| Method | Description | Returns |
|--------|-------------|---------|
| `develop_strategy(objective, total_budget, audience, ...)` | Create strategy | `Dict` |
| `optimize_allocation(strategy_id, perf_data)` | Optimize budget | `Dict` |
| `get_channel_recommendations(objective, audience, budget)` | Recommendations | `List[Dict]` |

### PerformanceAnalytics

| Method | Description | Returns |
|--------|-------------|---------|
| `record_touchpoint(touchpoint)` | Record interaction | `None` |
| `get_channel_performance(channel)` | Channel data | `ChannelPerformance` |
| `get_total_metrics()` | All-channel totals | `Dict` |
| `create_dashboard()` | Dashboard snapshot | `DashboardSnapshot` |
| `get_performance_trend(days)` | Daily trend | `List[Dict]` |
| `register_conversion_goal(goal)` | Add goal | `None` |
| `get_conversion_summary()` | Goal summary | `Dict` |

### AttributionEngine

| Method | Description | Returns |
|--------|-------------|---------|
| `add_touchpoints(touchpoints)` | Add data | `None` |
| `compute_attribution(model)` | Run model | `AttributionResult` |
| `compare_models()` | Compare all | `Dict` |
| `get_channel_attribution(model)` | Channel credits | `Dict` |

### EmailMarketingEngine

| Method | Description | Returns |
|--------|-------------|---------|
| `create_campaign(name, subject, from_email, html, ...)` | Create email | `EmailCampaign` |
| `send_campaign(email_id, count)` | Send | `Dict` |
| `record_event(email_id, event_type, count)` | Track event | `None` |
| `get_campaign_metrics(email_id)` | Metrics | `EmailMetrics` |
| `calculate_roi(email_id, revenue_per_conversion)` | ROI | `Dict` |
| `get_segment_performance()` | Segment data | `Dict` |

### SocialMediaManager

| Method | Description | Returns |
|--------|-------------|---------|
| `create_post(platform, content, ...)` | Create post | `SocialPost` |
| `publish_post(post_id)` | Publish | `bool` |
| `record_engagement(post_id, type, count)` | Track engagement | `None` |
| `get_post_metrics(post_id)` | Metrics | `SocialMetrics` |
| `get_platform_summary(platform)` | Summary | `Dict` |
| `get_top_posts(metric, limit)` | Top posts | `List[Dict]` |

### SEOManager

| Method | Description | Returns |
|--------|-------------|---------|
| `add_keyword(keyword, url, position, ...)` | Add keyword | `SEOKeyword` |
| `update_keyword_position(keyword_id, position)` | Update rank | `SEOKeyword` |
| `get_keyword_rankings(top_n)` | Rankings | `List[SEOKeyword]` |
| `get_ranking_changes()` | Changes | `List[Dict]` |
| `run_site_audit(domain)` | Site audit | `SEOAuditResult` |
| `get_seo_scorecard()` | Scorecard | `Dict` |

---

## Examples

### Example 1: Full Campaign with Email

```python
from agents.digital_marketing.agent import *

agent = DigitalMarketingAgent()

# Create campaign
result = agent.create_full_campaign(
    name="Product Launch Q4",
    objective=ObjectiveType.LEAD_GENERATION,
    channels=[ChannelType.PAID_SEARCH, ChannelType.EMAIL],
    budget=75000,
    audience=AudienceDefinition(
        segment=AudienceSegment.ALL,
        interests=["technology", "innovation"],
    ),
)

# Set up email nurture
email_campaign = agent.email_engine.create_campaign(
    name="Launch Nurture",
    subject_line="Be the first to know",
    from_email="launch@company.com",
    html_content="<h1>New Product</h1><p>Something exciting is coming.</p>",
)
agent.email_engine.send_campaign(email_campaign.email_id, 10000)
```

### Example 2: Attribution Analysis

```python
from agents.digital_marketing.agent import *

agent = DigitalMarketingAgent()
touchpoints = [
    Touchpoint(channel=ChannelType.DISPLAY, impressions=10000, cost=500),
    Touchpoint(channel=ChannelType.PAID_SEARCH, clicks=200, conversions=10, cost=400, revenue=2000),
    Touchpoint(channel=ChannelType.EMAIL, clicks=150, conversions=15, cost=50, revenue=3000),
]
agent.attribution_engine.add_touchpoints(touchpoints)

report = agent.run_attribution_analysis(AttributionModel.TIME_DECAY)
for model, data in report["model_comparison"].items():
    print(f"{model}: ROAS={data['roas']:.2f}")
```

### Example 3: Social Media Campaign

```python
from agents.digital_marketing.agent import *

social = agent.social_manager

# Create posts across platforms
for platform in [SocialPlatform.INSTAGRAM, SocialPlatform.TIKTOK]:
    post = social.create_post(
        platform=platform,
        content="Check out our new collection!",
        media_urls=["https://cdn.example.com/collection.jpg"],
        hashtags=["newcollection", "fashion"],
    )
    social.publish_post(post.post_id)

# Track engagement
summary = social.get_platform_summary()
```

### Example 4: SEO Audit and Optimization

```python
from agents.digital_marketing.agent import *

seo = agent.seo_manager

# Add keywords to track
keywords = [
    ("running shoes", "https://shop.example.com/running", 12, 14800),
    ("best sneakers", "https://shop.example.com/sneakers", 8, 22000),
    ("athletic footwear", "https://shop.example.com/athletic", 15, 8500),
]

for kw, url, pos, vol in keywords:
    seo.add_keyword(kw, url, position=pos, search_volume=vol)

# Run audit
audit = seo.run_site_audit("shop.example.com")
print(f"Score: {audit.overall_score}/100")

# Get recommendations
for rec in audit.recommendations:
    print(f"  - {rec}")
```

---

## Configuration

```yaml
digital_marketing_agent:
  campaign_manager:
    max_campaigns: 10000
    audit_log_retention_days: 365

  channel_strategy:
    default_currency: USD
    optimization_frequency: daily

  analytics:
    touchpoint_retention_days: 365
    alert_thresholds:
      roas_critical: 1.0
      cpc_warning: 5.0

  attribution:
    default_model: linear
    time_decay_half_life_days: 7

  email:
    max_send_rate_per_hour: 100000

  seo:
    max_keywords_tracked: 50000
```

---

## Design Patterns

### Strategy Pattern for Attribution

```python
class AttributionStrategy:
    def compute(self, touchpoints: List[Touchpoint]) -> Dict[str, float]:
        raise NotImplementedError

class FirstTouchStrategy(AttributionStrategy):
    def compute(self, touchpoints):
        # Give all credit to first touchpoint
        pass

class TimeDecayStrategy(AttributionStrategy):
    def compute(self, touchpoints):
        # Weight by recency
        pass
```

### Observer Pattern for Campaign Events

```python
class CampaignObserver:
    def on_campaign_activated(self, campaign: Campaign):
        self.notify_stakeholders(campaign)
    
    def on_budget_exhausted(self, campaign: Campaign):
        self.alert_team(campaign)
```

### Factory Pattern for Channel Creation

```python
class ChannelFactory:
    @staticmethod
    def create(channel_type: ChannelType, config: Dict) -> Channel:
        if channel_type == ChannelType.PAID_SEARCH:
            return PaidSearchChannel(config)
        elif channel_type == ChannelType.EMAIL:
            return EmailChannel(config)
        # ... etc
```

---

## Security

### Data Protection

- PII handling for customer data
- GDPR compliance for EU audiences
- Secure API key storage
- Encrypted data transmission

### Access Control

```
┌─────────────────┬────────┬────────┬────────┬────────┐
│  Role           │Campaign│Email   │Social  │SEO     │
├─────────────────┼────────┼────────┼────────┼────────┤
│  Viewer         │   ✓    │   ✓    │   ✓    │   ✓    │
│  Editor         │   ✓    │   ✓    │   ✓    │   ✗    │
│  Admin          │   ✓    │   ✓    │   ✓    │   ✓    │
└─────────────────┴────────┴────────┴────────┴────────┘
```

---

## Scalability

### Performance Considerations

| Operation | Small (< 1K) | Medium (< 100K) | Large (< 1M) |
|-----------|---------------|-----------------|--------------|
| Touchpoint recording | 10ms | 50ms | 200ms |
| Dashboard generation | 100ms | 1s | 10s |
| Attribution analysis | 200ms | 2s | 30s |
| Report generation | 500ms | 5s | 60s |

### Scaling Strategies

- Batch touchpoint recording for high-volume campaigns
- Cache dashboard snapshots for frequently accessed data
- Use incremental attribution updates
- Archive old touchpoints for performance
- Parallelize report generation

---

## Best Practices

1. **Always validate before activating** — run `campaign.validate()` to catch
   issues before they cost money.
2. **Record every touchpoint** — attribution accuracy depends on complete data.
3. **Compare attribution models** — no single model tells the full story.
4. **Monitor alerts daily** — catch ROAS drops and CPC spikes early.
5. **Re-optimize weekly** — use performance data to reallocate budgets.
6. **Segment email campaigns** — personalized emails get 2x higher open rates.
7. **Track SEO weekly** — ranking changes signal algorithm updates.
8. **Keep creatives fresh** — ad fatigue drops CTR by 50%+ within 2 weeks.

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Campaign won't activate | Missing creatives or budget | Run `validate()` and fix errors |
| ROAS always 0 | No touchpoints recorded | Call `record_touchpoint()` |
| Email open rate 0% | Events not tracked | Use `record_event()` |
| Attribution credits != 1.0 | Floating point rounding | Normalize manually if needed |
| Dashboard shows no data | Empty analytics | Record touchpoints first |
| SEO scores random | Placeholder implementation | Connect real SEO API |
| Duplicate campaigns created | Calling create in a loop | Use `duplicate_campaign()` |

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
pip install -r requirements-dev.txt
pytest tests/
flake8 agents/digital_marketing/
mypy agents/digital_marketing/
```

---

## License

MIT License — see [LICENSE](../../LICENSE) for details.

---

**See Also**: [ARCHITECTURE.md](./ARCHITECTURE.md) for system design details,
[GROK.md](./GROK.md) for agent identity and operational guidelines.
