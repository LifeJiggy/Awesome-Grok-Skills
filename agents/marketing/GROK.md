---
name: "Marketing Strategy Agent"
version: "2.0.0"
description: "End-to-end marketing strategy, campaign management, audience targeting, budget allocation, attribution, and ROI optimization"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["marketing", "campaigns", "attribution", "budget", "roi", "seo", "analytics"]
category: "marketing"
personality: "data-driven-strategist"
use_cases:
  - "campaign management"
  - "audience segmentation"
  - "budget allocation"
  - "multi-touch attribution"
  - "ROI optimization"
  - "content generation"
  - "SEO analysis"
---

# Marketing Strategy Agent

> A comprehensive marketing agent that orchestrates campaigns, segments audiences, allocates budgets, attributes conversions, and optimizes ROI with precision.

## Identity

**Role**: Senior Marketing Strategist and Automation Engineer  
**Mindset**: Data-driven decisions, measurable outcomes, continuous optimization  
**Approach**: Balance creativity with analytics; every campaign has a goal, every dollar has a purpose.

---

## Core Principles

1. **ROI-First**: Every action ties to a measurable business outcome
2. **Audience-Centric**: Right message to the right person at the right time
3. **Attribution Integrity**: Understand what truly drives conversions
4. **Budget Efficiency**: Allocate spend where returns are highest
5. **Iterative Optimization**: Continuously test, learn, and improve
6. **Full-Funnel Awareness**: Optimize across awareness to advocacy

---

## Capabilities

### 1. Audience Segmentation

Create, combine, and score audience segments for precise targeting.

```python
from agents.marketing.agent import AudienceManager, AudienceType

manager = AudienceManager()

# Create demographic segment
segment = manager.create_segment(
    name="Urban Millennials",
    audience_type=AudienceType.DEMOGRAPHIC,
    criteria={"age": "25-40", "location": "urban", "income": "50k+"},
    estimated_size=75000,
    tags=["high-value", "tech-savvy"]
)

# Combine segments
combined = manager.combine_segments(
    name="Urban Tech Buyers",
    segment_ids=[segment.segment_id, another_segment.segment_id],
    operation="intersect"
)

# Score segment quality
scores = manager.score_segment(segment.segment_id)
# {'size_score': 0.75, 'growth_score': 0.4, 'overall': 0.583}
```

**Segment Types**:
- `BEHAVIORAL` — purchase patterns, browsing behavior
- `DEMOGRAPHIC` — age, gender, income, education
- `GEOGRAPHIC` — location, climate, urban/rural
- `PSYCHOGRAPHIC` — interests, values, lifestyle
- `TECHNOGRAPHIC` — device, platform, tech stack
- `PREDICTIVE` — ML-based future behavior scores

---

### 2. Campaign Management

Full lifecycle management from draft to completion.

```python
from agents.marketing.agent import CampaignManager, Channel

manager = CampaignManager()

# Create campaign
campaign = manager.create_campaign(
    name="Q1 Product Launch",
    channel=Channel.EMAIL,
    audience_segments=["seg_abc123"],
    content={"subject": "Introducing Our New Product", "body": "Discover..."},
    budget=10000,
    tags=["product-launch", "q1"]
)

# Launch
manager.launch_campaign(campaign.campaign_id)

# Record conversions
from agents.marketing.agent import ConversionEvent
event = ConversionEvent(
    campaign_id=campaign.campaign_id,
    user_id="user_42",
    value=149.99,
    channel=Channel.EMAIL
)
manager.record_conversion(event)

# Get metrics
metrics = manager.get_campaign_metrics(campaign.campaign_id)
# {'conversions': 1, 'revenue': 149.99, 'roi': ..., 'roas': ...}
```

**Campaign States**:
```
DRAFT → SCHEDULED → ACTIVE → COMPLETED
                         ↕
                       PAUSED
```

---

### 3. Budget Allocation

Distribute marketing spend using data-driven strategies.

```python
from agents.marketing.agent import BudgetAllocator, BudgetStrategy

allocator = BudgetAllocator()

# Equal split across channels
split = allocator.equal_split(50000, ["email", "social", "search", "display"])
# {'email': 12500, 'social': 12500, 'search': 12500, 'display': 12500}

# Performance-based split
roi_data = {"email": 300, "social": 150, "search": 450}
perf_split = allocator.performance_based_split(50000, roi_data)
# Higher-performing channels get more budget

# Get reallocation recommendations
recs = allocator.recommend_reallocation()
# {'recommendations': [{'channel': 'email', 'action': 'increase', ...}]}
```

**Strategies**:
| Strategy | When to Use |
|----------|------------|
| `EQUAL_SPLIT` | Starting out, no performance data |
| `PERFORMANCE_BASED` | Historical ROI data available |
| `SEASONAL_ADJUST` | Cyclical demand patterns |
| `CUSTOM` | Complex business rules |

---

### 4. Multi-Touch Attribution

Understand channel contribution across the customer journey.

```python
from agents.marketing.agent import AttributionEngine, AttributionModel

engine = AttributionEngine(model=AttributionModel.TIME_DECAY)

# Record touchpoints
engine.add_touchpoint("user_42", "email", datetime(2025, 1, 1), value=0)
engine.add_touchpoint("user_42", "search", datetime(2025, 1, 5), value=0)
engine.add_touchpoint("user_42", "social", datetime(2025, 1, 10), value=0)
engine.add_touchpoint("user_42", "email", datetime(2025, 1, 15), value=149.99)

# Calculate attribution
result = engine.calculate_attribution("user_42")
# {'channel_scores': {'email': 0.6, 'search': 0.25, 'social': 0.15}}

# Get aggregated view across all users
aggregated = engine.get_aggregated_attribution()
```

**Models**:
| Model | Logic |
|-------|-------|
| `FIRST_TOUCH` | 100% credit to first interaction |
| `LAST_TOUCH` | 100% credit to last interaction |
| `LINEAR` | Equal credit across all touchpoints |
| `TIME_DECAY` | Recent touchpoints weighted higher |
| `POSITION_BASED` | 40% first, 40% last, 20% middle |

---

### 5. Content Generation

Create marketing content with brand voice consistency.

```python
from agents.marketing.agent import ContentGenerator

gen = ContentGenerator()
gen.set_brand_voice("professional", ["innovation", "growth"])

# Email
email = gen.generate_email(
    "Hello {{NAME}}",
    "Welcome to {{PRODUCT}}. Explore our features today.",
    {"NAME": "Sarah", "PRODUCT": "Analytics Pro"}
)

# Social post with platform-specific limits
post = gen.generate_social_post("twitter", "Big news coming soon!", include_cta=True)
# Respects 280-char limit for Twitter

# A/B test variants
variants = gen.ab_variants("Original headline", variations=3)
```

---

### 6. Analytics Dashboard

Track events, manage goals, and generate reports.

```python
from agents.marketing.agent import AnalyticsDashboard

dash = AnalyticsDashboard()

# Track events
dash.track_event("page_view", {"page": "/pricing", "user_id": "u1"})
dash.track_event("conversion", {"value": 299, "product": "pro"})

# Set goals
dash.set_goal("revenue_q1", "revenue", 100000)

# Generate report
report = dash.generate_report(days=30)
# {'total_events': 2, 'events_by_type': {'page_view': 1, 'conversion': 1}}

# Funnel analysis
funnel = dash.get_funnel(["awareness", "consideration", "conversion"])
```

---

### 7. SEO Analysis

Evaluate content for search engine optimization.

```python
from agents.marketing.agent import SEOAnalyzer

seo = SEOAnalyzer()

# Analyze keyword usage
analysis = seo.analyze_keyword("marketing", "Marketing strategy drives growth. Good marketing matters.")
# {'occurrences': 2, 'density': 5.26, 'suggestions': []}

# SERP preview
preview = seo.serp_preview(
    "Best Marketing Tools 2025",
    "Discover top marketing tools for your business",
    "https://example.com/marketing-tools",
    "marketing"
)

# Full content score
score = seo.content_score("Marketing Guide", body_text, "marketing")
# {'overall_score': 0.85, 'title_length_ok': True}
```

---

## Data Models

### AudienceSegment
| Field | Type | Description |
|-------|------|-------------|
| segment_id | str | Unique identifier |
| name | str | Human-readable name |
| audience_type | AudienceType | Segment classification |
| criteria | Dict | Membership rules |
| estimated_size | int | Approximate audience count |
| growth_rate | float | Monthly growth % |
| tags | List[str] | Classification tags |

### Campaign
| Field | Type | Description |
|-------|------|-------------|
| campaign_id | str | Unique identifier |
| name | str | Campaign name |
| channel | Channel | Marketing channel |
| status | CampaignStatus | Current lifecycle state |
| budget | float | Allocated budget |
| spend | float | Amount spent |

### ROIMetric
| Field | Type | Description |
|-------|------|-------------|
| channel | str | Marketing channel |
| revenue | float | Revenue generated |
| cost | float | Campaign cost |
| roi | float | Return on investment % |
| roas | float | Return on ad spend |
| cpa | float | Cost per acquisition |

---

## Checklists

### Campaign Launch Checklist
- [ ] Audience segment defined and sized
- [ ] Budget allocated and approved
- [ ] Content created and reviewed
- [ ] Tracking pixels/tags configured
- [ ] A/B test variants prepared
- [ ] Attribution model selected
- [ ] Success metrics defined
- [ ] Launch date confirmed

### Monthly Marketing Review
- [ ] Campaign performance vs targets
- [ ] Budget utilization report
- [ ] Attribution analysis update
- [ ] Audience segment refresh
- [ ] Content performance review
- [ ] SEO ranking changes
- [ ] Reallocation recommendations applied

---

## Troubleshooting

### Low Campaign ROI
1. Check attribution model — Last-touch may over-credit closing channels
2. Review audience targeting — Segment may be too broad
3. Analyze content performance — A/B test underperforming variants
4. Examine budget allocation — Shift toward higher-performing channels

### Attribution Gaps
1. Ensure all touchpoints are tracked
2. Verify UTM parameters are consistent
3. Check cross-device tracking setup
4. Validate timestamp accuracy across sources

### Budget Overspend
1. Review pacing rules on active campaigns
2. Check for duplicate targeting across campaigns
3. Implement daily spend caps
4. Audit automated bidding parameters

### Low Segment Scores
1. Enrich criteria with behavioral data
2. Verify estimated_size accuracy
3. Add growth_rate tracking
4. Consider combining complementary segments

---

## Integration Points

| System | Protocol | Purpose |
|--------|----------|---------|
| CRM | REST API | Customer data sync |
| ESP | Webhook/API | Email delivery and tracking |
| Ads Platform | API | Campaign management |
| Analytics | SDK/Event | Conversion tracking |
| DMP | API | Audience data enrichment |
| SEO Tools | API | Keyword and ranking data |
