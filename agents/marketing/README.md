# Marketing Strategy Agent

End-to-end marketing strategy, campaign management, audience targeting, budget allocation, attribution, and ROI optimization.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Contributing](#contributing)
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
| Multi-Touch Attribution | 5 attribution models for conversion credit |
| Content Generation | Template-based content with brand voice |
| Analytics Dashboard | Event tracking, goals, and reporting |
| SEO Analysis | Keyword density, SERP preview, content scoring |

### System Requirements

- Python 3.10 or higher
- 512 MB RAM minimum
- 100 MB disk space
- Network access for API integrations (optional)

---

## Features

### Audience Management
- Support for 6 segment types: behavioral, demographic, geographic, psychographic, technographic, predictive
- Segment combination via intersect, union, or exclude operations
- Automated segment scoring based on size, growth, and criteria depth
- Real-time segment updates with change tracking
- Tag-based segment organization

### Campaign Lifecycle
- State machine with validated transitions: draft, scheduled, active, paused, completed, archived
- Event hooks for on_launch, on_pause, on_complete, and on_archive callbacks
- Conversion event recording with per-campaign attribution
- Multi-channel support (email, social, search, display, video, affiliate)
- A/B testing with automatic variant generation

### Budget Optimization
- Equal split, performance-based, and custom allocation strategies
- Historical ROI tracking per channel
- Reallocation recommendations based on performance thresholds
- Seasonal adjustment with monthly indices
- Reserve budget for testing (configurable percentage)

### Attribution Models
- First Touch, Last Touch, Linear, Time Decay, Position-Based
- Per-user and aggregated attribution views
- Confidence scoring based on touchpoint diversity
- Model switching for comparison analysis
- Half-life configurable for time-decay model

### Content Creation
- Template rendering with variable substitution
- Platform-aware content with character limits
- A/B variant generation for testing
- Brand voice configuration (tone, keywords, excluded words)
- Content type support (email, social, ad, landing page)

### Analytics
- Event tracking with custom properties
- Goal setting and progress monitoring
- Funnel conversion analysis
- Configurable reporting periods (daily, weekly, monthly)
- Executive, campaign, channel, and audience report types

### SEO
- Keyword density analysis with optimal range (1-3%)
- SERP preview generation
- Content scoring with actionable suggestions
- Keyword opportunity identification
- Title and description length validation

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│              MarketingAgent (Facade)                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │ AudienceManager│  │CampaignManager │  │BudgetAllocator │    │
│  │                │  │                │  │                │    │
│  │ Segments       │  │ Lifecycle      │  │ Strategies     │    │
│  │ Combine        │  │ Hooks          │  │ ROI Track      │    │
│  │ Score          │  │ Metrics        │  │ Recommend      │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │AttributionEng. │  │ContentGeneratr │  │AnalyticsDashbd │    │
│  │                │  │                │  │                │    │
│  │ Models         │  │ Templates      │  │ Events         │    │
│  │ Scoring        │  │ Brand Voice    │  │ Goals          │    │
│  │ Aggregation    │  │ Platform       │  │ Reports        │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
│                                                                  │
│  ┌────────────────┐                                             │
│  │  SEOAnalyzer   │                                             │
│  │                │                                             │
│  │  Keywords      │                                             │
│  │  SERP Preview  │                                             │
│  │  Content Score │                                             │
│  └────────────────┘                                             │
└─────────────────────────────────────────────────────────────────┘
```

Each component operates independently with its own state and can be used standalone or through the `MarketingAgent` orchestrator.

### Component Interaction Flow

```
User Request
     │
     ▼
MarketingAgent (facade)
     │
     ├──→ AudienceManager.create_segment()
     │         │
     │         ▼
     │    Segment ID
     │
     ├──→ BudgetAllocator.equal_split()
     │         │
     │         ▼
     │    Channel Budgets
     │
     ├──→ CampaignManager.create_campaign()
     │         │
     │         ▼
     │    Campaign (DRAFT)
     │
     ├──→ CampaignManager.launch_campaign()
     │         │
     │         ▼
     │    Campaign (ACTIVE)
     │         │
     │         ├──→ AttributionEngine.add_touchpoint()
     │         │
     │         └──→ AnalyticsDashboard.track_event()
     │
     ├──→ CampaignManager.complete_campaign()
     │         │
     │         ▼
     │    Campaign (COMPLETED)
     │
     ├──→ AttributionEngine.calculate_attribution()
     │         │
     │         ▼
     │    Channel Scores
     │
     ├──→ AnalyticsDashboard.generate_report()
     │         │
     │         ▼
     │    Report
     │
     └──→ BudgetAllocator.recommend_reallocation()
               │
               ▼
          Recommendations
```

---

## Quick Start

### Installation

```bash
pip install awesome-grok-skills
```

### Minimal Example

```python
from agents.marketing.agent import MarketingAgent, Channel, AudienceType

# Initialize the agent
agent = MarketingAgent()

# Create audience segment
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

# Record a conversion
from agents.marketing.agent import ConversionEvent
agent.campaigns.record_conversion(ConversionEvent(
    campaign_id=campaign.campaign_id,
    user_id="user_123",
    value=99.99,
    channel=Channel.EMAIL
))

# Get metrics
metrics = agent.campaigns.get_campaign_metrics(campaign.campaign_id)
print(f"ROI: {metrics['roi']:.1f}%")
print(f"Revenue: ${metrics['revenue']:.2f}")
```

### 60-Second Setup

```python
from agents.marketing.agent import MarketingAgent

agent = MarketingAgent()

# One-liner campaign lifecycle
result = agent.full_campaign_lifecycle(
    name="Quick Campaign",
    channel="email",
    segments=["seg_001"],
    budget=1000,
    content={"subject": "Hello", "body": "World"}
)
print(result)
```

---

## Installation

### From PyPI

```bash
pip install awesome-grok-skills
```

### From Source

```bash
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e .
```

### Development Install

```bash
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e ".[dev]"
pytest  # Run tests
```

### Requirements

```
Python >= 3.10
No external dependencies (stdlib only)
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

### Component Independence

```python
from agents.marketing.agent import AudienceManager, CampaignManager

# Use components directly without the facade
audience = AudienceManager()
campaigns = CampaignManager()

seg = audience.create_segment("Direct Segment", AudienceType.BEHAVIORAL, {"opt_in": True}, 10000)
camp = campaigns.create_campaign("Direct Campaign", Channel.EMAIL, [seg.segment_id], {}, 5000)
```

### CLI Usage

```bash
# List all campaigns
python agents/marketing/agent.py --list-campaigns

# Generate report for last 30 days
python agents/marketing/agent.py --report-days 30

# Export analytics
python agents/marketing/agent.py --export-analytics --format json
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
| `get_segment(segment_id)` | Retrieve segment |
| `update_segment(segment_id, **kwargs)` | Update segment fields |
| `delete_segment(segment_id)` | Remove segment |
| `combine_segments(name, ids, operation)` | Combine multiple segments |
| `score_segment(segment_id)` | Score segment quality |
| `list_segments(type, tags)` | List segments with filters |

### CampaignManager

| Method | Description |
|--------|-------------|
| `create_campaign(name, channel, segments, content, budget)` | Create campaign |
| `launch_campaign(campaign_id)` | Start campaign |
| `pause_campaign(campaign_id)` | Pause active campaign |
| `resume_campaign(campaign_id)` | Resume paused campaign |
| `complete_campaign(campaign_id)` | Mark campaign complete |
| `archive_campaign(campaign_id)` | Archive completed campaign |
| `get_campaign(campaign_id)` | Get campaign details |
| `list_campaigns(status, channel)` | List campaigns with filters |
| `get_campaign_metrics(campaign_id)` | Get performance metrics |
| `record_conversion(event)` | Record conversion event |
| `add_hook(event_type, callback)` | Register event hook |

### BudgetAllocator

| Method | Description |
|--------|-------------|
| `create_allocation(total, channel_budgets, strategy)` | Create allocation |
| `equal_split(budget, channels)` | Equal distribution |
| `performance_based_split(budget, channel_rois)` | ROI-weighted split |
| `seasonal_adjust(base_alloc, seasonal_index)` | Seasonal adjustment |
| `record_performance(channel, ROIMetric)` | Record channel performance |
| `get_performance_history(channel)` | Get performance history |
| `recommend_reallocation()` | Get optimization suggestions |

### AttributionEngine

| Method | Description |
|--------|-------------|
| `set_model(model)` | Set attribution model |
| `add_touchpoint(user, channel, timestamp, value)` | Record touchpoint |
| `calculate_attribution(user_id)` | Calculate per-user attribution |
| `get_aggregated_attribution()` | Get cross-user attribution |
| `list_models()` | List available models |

### ContentGenerator

| Method | Description |
|--------|-------------|
| `set_brand_voice(tone, keywords, excluded)` | Configure brand voice |
| `add_template(id, template, type)` | Register template |
| `render(template_id, variables)` | Render template |
| `generate_email(subject, body, vars)` | Create email |
| `generate_social_post(platform, message)` | Create social post |
| `ab_variants(content, variations)` | Generate A/B variants |

### AnalyticsDashboard

| Method | Description |
|--------|-------------|
| `track_event(type, properties)` | Track custom event |
| `set_goal(id, metric, target)` | Set performance goal |
| `get_goal_progress(goal_id)` | Check goal progress |
| `generate_report(days)` | Generate report |
| `get_funnel(stages)` | Analyze conversion funnel |

### SEOAnalyzer

| Method | Description |
|--------|-------------|
| `analyze_keyword(keyword, content)` | Analyze keyword usage |
| `serp_preview(title, desc, url, keyword)` | Generate SERP preview |
| `content_score(title, body, keyword)` | Score content SEO |
| `get_keyword_suggestions(topic)` | Get keyword suggestions |

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

# Launch both
agent.campaigns.launch_campaign(email.campaign_id)
agent.campaigns.launch_campaign(social.campaign_id)
```

### Attribution Analysis

```python
from agents.marketing.agent import AttributionEngine, AttributionModel
from datetime import datetime

engine = AttributionEngine(model=AttributionModel.TIME_DECAY)

# Record a customer journey
engine.add_touchpoint("u1", "social", datetime(2025, 1, 1))
engine.add_touchpoint("u1", "email", datetime(2025, 1, 5))
engine.add_touchpoint("u1", "search", datetime(2025, 1, 8))
engine.add_touchpoint("u1", "email", datetime(2025, 1, 10), value=199.99)

result = engine.calculate_attribution("u1")
print(f"Email: {result.channel_scores['email']:.2%}")
print(f"Search: {result.channel_scores['search']:.2%}")
print(f"Social: {result.channel_scores['social']:.2%}")
print(f"Confidence: {result.confidence:.2%}")
```

### Budget Optimization

```python
from agents.marketing.agent import BudgetAllocator, ROIMetric

allocator = BudgetAllocator()

# Record historical performance
allocator.record_performance("email", ROIMetric(channel="email", revenue=15000, cost=3000, roi=400))
allocator.record_performance("social", ROIMetric(channel="social", revenue=8000, cost=4000, roi=100))
allocator.record_performance("search", ROIMetric(channel="search", revenue=20000, cost=5000, roi=300))

# Get recommendations
recs = allocator.recommend_reallocation()
for rec in recs['recommendations']:
    print(f"{rec['channel']}: {rec['action']} - {rec['reason']}")
```

### Content Generation with A/B Testing

```python
from agents.marketing.agent import ContentGenerator

gen = ContentGenerator()
gen.set_brand_voice("professional", ["innovation", "growth"])

# Generate email
email = gen.generate_email(
    subject="Hello {{NAME}}",
    body="Welcome to {{PRODUCT}}. Discover our features.",
    variables={"NAME": "Sarah", "PRODUCT": "Analytics Pro"}
)

# Generate A/B variants
variants = gen.ab_variants(email['subject'], variations=3)
for v in variants:
    print(f"Variant {v['variant_id']}: {v['content']}")
```

### SEO Content Optimization

```python
from agents.marketing.agent import SEOAnalyzer

seo = SEOAnalyzer()

# Analyze content
score = seo.content_score(
    title="Marketing Guide 2025",
    body="Marketing is essential for business growth. " * 50,
    keyword="marketing"
)

print(f"Score: {score['overall_score']:.2f}")
print(f"Title OK: {score['title_length_ok']}")
print(f"Keyword in Title: {score['title_has_keyword']}")
print(f"Suggestions: {score['suggestions']}")
```

### Complete Campaign Lifecycle

```python
from agents.marketing.agent import MarketingAgent

agent = MarketingAgent()

# Run full lifecycle
result = agent.full_campaign_lifecycle(
    name="Q1 Product Launch",
    channel="email",
    segments=["seg_target"],
    budget=10000,
    content={
        "subject": "Introducing Our New Product",
        "body": "Discover how our new product can help you..."
    }
)

# Access results
print(f"Campaign: {result['campaign_id']}")
print(f"Metrics: {result['metrics']}")
print(f"Attribution: {result['attribution']}")
print(f"Report: {result['report']}")
```

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MARKETING_LOG_LEVEL` | Logging verbosity | `INFO` |
| `MARKETING_DEFAULT_MODEL` | Attribution model | `linear` |
| `MARKETING_BUDGET_THRESHOLD` | ROI alert threshold | `50` |
| `MARKETING_CACHE_TTL` | Template cache TTL (seconds) | `3600` |
| `MARKETING_ATTRIBUTION_HALF_LIFE` | Time decay half-life (days) | `7` |
| `MARKETING_REALLOCATION_THRESHOLD` | ROI multiplier for recommendations | `1.5` |

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

### Attribution Model Selection

| Scenario | Recommended Model |
|----------|------------------|
| New brand, no data | LINEAR |
| Direct response focus | LAST_TOUCH |
| Brand awareness | FIRST_TOUCH |
| B2B with long sales cycle | POSITION_BASED |
| Fast-moving B2C | TIME_DECAY |

### Platform Configuration

```python
# Configure platform-specific settings
PLATFORM_LIMITS = {
    "twitter": {"max_chars": 280, "recommended": 240},
    "linkedin": {"max_chars": 3000, "recommended": 1500},
    "instagram": {"max_chars": 2200, "recommended": 1250},
    "facebook": {"max_chars": 63206, "recommended": 80},
    "email": {"max_chars": None, "subject_recommended": 60}
}
```

---

## Best Practices

### Audience Segmentation
- Start with broad segments and narrow based on performance data
- Use intersect operations to create high-intent micro-segments
- Review and refresh segments monthly
- Track segment growth rates to identify expanding opportunities
- Tag segments for easy filtering and organization
- Use behavioral data to supplement demographic criteria

### Campaign Management
- Always define success metrics before launch
- Use A/B testing for subject lines, content, and CTAs
- Set up conversion tracking from day one
- Complete campaigns promptly to keep metrics accurate
- Register hooks for automated notifications
- Document campaign objectives in tags

### Budget Allocation
- Never allocate 100% of budget — reserve 10-15% for testing
- Review performance weekly and reallocate monthly
- Use performance-based allocation once you have 30+ days of data
- Track CPA alongside ROI to avoid profitable-but-expensive channels
- Consider seasonal patterns for cyclical businesses
- Set up overspend alerts

### Attribution
- Start with linear attribution and iterate toward data-driven
- Ensure consistent UTM parameter naming across channels
- Account for cross-device journeys in attribution logic
- Use time-decay for fast-moving B2C, position-based for B2B
- Review and validate attribution results quarterly
- Compare multiple models to understand sensitivity

### Content
- Maintain brand voice consistency across all channels
- Respect platform character limits automatically
- Always generate A/B variants for testing
- Track content performance by engagement metrics
- Refresh templates quarterly to avoid fatigue
- Use personalization variables for higher engagement

### SEO
- Target keyword density between 1-3%
- Keep titles under 60 characters
- Keep meta descriptions under 160 characters
- Ensure content length exceeds 300 words
- Update content regularly to maintain freshness
- Research keywords before writing

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
| Hook not firing | Wrong event type | Check hook registration and event_type |
| Report shows no data | No events tracked | Verify analytics tracking setup |
| Segment scoring is low | Insufficient criteria | Add more criteria or increase size |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

agent = MarketingAgent()
# Now all operations will log detailed debug information
```

### Common Error Messages

| Error | Meaning | Fix |
|-------|---------|-----|
| `CampaignNotFoundError` | Campaign ID doesn't exist | Verify campaign_id |
| `InvalidStateTransitionError` | Can't move to requested state | Check current state |
| `InvalidBudgetError` | Budget exceeds allocation | Verify budget amounts |
| `SegmentNotFoundError` | Segment ID doesn't exist | Verify segment_id |
| `TemplateNotFoundError` | Template ID not registered | Add template first |

---

## FAQ

### Q: Can I use components independently?
A: Yes, each component (AudienceManager, CampaignManager, etc.) can be used standalone without the MarketingAgent facade.

### Q: How many touchpoints are needed for attribution?
A: Minimum 1 touchpoint with a conversion. More touchpoints increase attribution confidence.

### Q: What's the maximum number of segments I can combine?
A: No hard limit, but performance degrades with many segments. Keep combinations under 10 for optimal performance.

### Q: Can I customize the scoring algorithm?
A: The scoring algorithm is built-in, but you can subclass and override the `score_segment` method.

### Q: How do I handle cross-device attribution?
A: Use consistent user IDs across devices. The attribution engine aggregates by user_id.

### Q: Can I export data to other tools?
A: Yes, all data classes have `to_dict()` methods for easy serialization.

---

## Contributing

We welcome contributions! Please see our [Contributing Guide](../../CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e ".[dev]"
pre-commit install
```

### Running Tests

```bash
pytest tests/marketing/
pytest --cov=agents.marketing
```

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for public methods
- Add tests for new functionality

---

## License

MIT License - see [LICENSE](../../LICENSE) for details.

---

## Support

- Documentation: [docs.example.com](https://docs.example.com)
- Issues: [GitHub Issues](https://github.com/awesome-grok-skills/awesome-grok-skills/issues)
- Discussions: [GitHub Discussions](https://github.com/awesome-grok-skills/awesome-grok-skills/discussions)
