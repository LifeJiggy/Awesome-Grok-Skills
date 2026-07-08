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
  - "A/B testing"
  - "funnel analysis"
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
7. **Platform Respect**: Honor each platform's character limits and best practices
8. **Brand Consistency**: Maintain voice and messaging across all channels

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
# Returns: AudienceSegment(segment_id="seg_abc123", name="Urban Millennials", ...)

# Create behavioral segment
behavioral = manager.create_segment(
    name="Frequent Buyers",
    audience_type=AudienceType.BEHAVIORAL,
    criteria={"purchase_frequency": ">5/month", "avg_order": ">50"},
    estimated_size=25000,
    tags=["loyal", "high-frequency"]
)

# Combine segments via intersection
combined = manager.combine_segments(
    name="Urban Tech Buyers",
    segment_ids=[segment.segment_id, behavioral.segment_id],
    operation="intersect"
)
# Result: users in BOTH segments

# Combine via union
broad = manager.combine_segments(
    name="All High Value",
    segment_ids=[segment.segment_id, behavioral.segment_id],
    operation="union"
)
# Result: users in EITHER segment

# Score segment quality
scores = manager.score_segment(segment.segment_id)
# {
#   'size_score': 0.75,
#   'growth_score': 0.4,
#   'criteria_score': 0.6,
#   'overall': 0.583
# }

# Update segment
manager.update_segment(
    segment.segment_id,
    estimated_size=80000,
    tags=["high-value", "tech-savvy", "q1-target"]
)

# List segments with filters
segments = manager.list_segments(
    audience_type=AudienceType.DEMOGRAPHIC,
    tags=["high-value"]
)
```

**Segment Types**:
| Type | Use Case | Example Criteria |
|------|----------|-----------------|
| BEHAVIORAL | Purchase patterns, browsing | purchase_frequency > 3/month |
| DEMOGRAPHIC | Age, gender, income | age: 25-40, income: 50k+ |
| GEOGRAPHIC | Location-based | city: "San Francisco" |
| PSYCHOGRAPHIC | Interests, values | interests: ["tech", "sustainability"] |
| TECHNOGRAPHIC | Device, platform | device: "mobile", os: "iOS" |
| PREDICTIVE | ML-based scores | churn_risk < 0.3, ltv > 500 |

**Scoring Algorithm**:
```python
# Size Score: normalized to 100K audience
size_score = min(1.0, estimated_size / 100_000)

# Growth Score: monthly growth rate mapped to 0-1
growth_score = max(0, min(1.0, (growth_rate + 50) / 100))

# Criteria Depth: more criteria = better targeting
criteria_score = min(1.0, len(criteria) / 5.0)

# Overall: weighted average
overall = (size_score + growth_score + criteria_score) / 3.0
```

---

### 2. Campaign Management

Full lifecycle management from draft to completion.

```python
from agents.marketing.agent import CampaignManager, Channel, CampaignStatus

manager = CampaignManager()

# Create campaign
campaign = manager.create_campaign(
    name="Q1 Product Launch",
    channel=Channel.EMAIL,
    audience_segments=["seg_abc123"],
    content={
        "subject": "Introducing Our New Product",
        "body": "Discover how our new product can transform your workflow...",
        "cta": "Learn More"
    },
    budget=10000,
    tags=["product-launch", "q1"]
)
# Returns: Campaign(campaign_id="camp_xyz789", status=DRAFT, ...)

# Schedule for future launch
manager.schedule_campaign(campaign.campaign_id, launch_date="2025-02-01")

# Launch
manager.launch_campaign(campaign.campaign_id)
# Status: DRAFT → ACTIVE
# Hooks: on_launch fired

# Record touchpoints for attribution
from agents.marketing.agent import ConversionEvent
event = ConversionEvent(
    campaign_id=campaign.campaign_id,
    user_id="user_42",
    value=149.99,
    channel=Channel.EMAIL,
    conversion_type="purchase"
)
manager.record_conversion(event)

# Pause if needed
manager.pause_campaign(campaign.campaign_id)
# Status: ACTIVE → PAUSED

# Resume
manager.resume_campaign(campaign.campaign_id)
# Status: PAUSED → ACTIVE

# Complete campaign
manager.complete_campaign(campaign.campaign_id)
# Status: ACTIVE → COMPLETED
# Hooks: on_complete fired

# Get comprehensive metrics
metrics = manager.get_campaign_metrics(campaign.campaign_id)
# {
#   'conversions': 1,
#   'revenue': 149.99,
#   'cost': 10000,
#   'roi': -85.0,
#   'roas': 0.015,
#   'cpa': 10000.0,
#   'ctr': 2.5,
#   'open_rate': 22.0
# }

# List campaigns with filters
active = manager.list_campaigns(status=CampaignStatus.ACTIVE)
email_campaigns = manager.list_campaigns(channel=Channel.EMAIL)
```

**Campaign States**:
```
DRAFT → SCHEDULED → ACTIVE → COMPLETED
                  ↕
                PAUSED
                  ↓
              ARCHIVED
```

**State Transition Rules**:
| From | To | Trigger |
|------|-----|---------|
| DRAFT | SCHEDULED | schedule_campaign() |
| DRAFT | ACTIVE | launch_campaign() |
| SCHEDULED | ACTIVE | launch_campaign() |
| ACTIVE | PAUSED | pause_campaign() |
| PAUSED | ACTIVE | resume_campaign() |
| ACTIVE | COMPLETED | complete_campaign() |
| COMPLETED | ARCHIVED | archive_campaign() |
| DRAFT | ARCHIVED | archive_campaign() |

---

### 3. Budget Allocation

Distribute marketing spend using data-driven strategies.

```python
from agents.marketing.agent import BudgetAllocator, BudgetStrategy, ROIMetric

allocator = BudgetAllocator()

# Equal split across channels
split = allocator.equal_split(50000, ["email", "social", "search", "display"])
# {
#   'email': 12500,
#   'social': 12500,
#   'search': 12500,
#   'display': 12500
# }

# Performance-based split using historical ROI
roi_data = {
    "email": ROIMetric(channel="email", revenue=30000, cost=5000, roi=500),
    "social": ROIMetric(channel="social", revenue=15000, cost=8000, roi=87.5),
    "search": ROIMetric(channel="search", revenue=45000, cost=10000, roi=350)
}
perf_split = allocator.performance_based_split(50000, roi_data)
# Higher-performing channels get proportionally more budget

# Seasonal adjustment
seasonal_index = {
    1: 0.8, 2: 0.9, 3: 1.0, 4: 1.1, 5: 1.2, 6: 1.3,
    7: 1.2, 8: 1.1, 9: 1.0, 10: 1.1, 11: 1.4, 12: 1.5
}
seasonal_split = allocator.seasonal_adjust(50000, seasonal_index)

# Record performance for future decisions
allocator.record_performance("email", ROIMetric(
    channel="email",
    revenue=25000,
    cost=4000,
    roi=525,
    roas=6.25,
    cpa=35.0
))

# Get reallocation recommendations
recs = allocator.recommend_reallocation()
# {
#   'recommendations': [
#     {'channel': 'email', 'action': 'increase', 'reason': 'ROI 525% > avg 300%'},
#     {'channel': 'social', 'action': 'decrease', 'reason': 'ROI 87.5% < avg 300%'},
#   ],
#   'current_allocation': {...},
#   'suggested_allocation': {...}
# }

# Get performance history
history = allocator.get_performance_history("email")
# [ROIMetric(...), ROIMetric(...), ...]
```

**Strategies**:
| Strategy | When to Use | Formula |
|----------|------------|---------|
| `EQUAL_SPLIT` | Starting out, no data | total / num_channels |
| `PERFORMANCE_BASED` | Historical ROI available | weight = roi_ch / sum(roi_all) |
| `SEASONAL_ADJUST` | Cyclical demand | base * seasonal_index[month] |
| `CUSTOM` | Complex rules | user-defined function |

---

### 4. Multi-Touch Attribution

Understand channel contribution across the customer journey.

```python
from agents.marketing.agent import AttributionEngine, AttributionModel

# Initialize with preferred model
engine = AttributionEngine(model=AttributionModel.TIME_DECAY)

# Record touchpoints along customer journey
engine.add_touchpoint("user_42", "email", datetime(2025, 1, 1), value=0)
engine.add_touchpoint("user_42", "search", datetime(2025, 1, 5), value=0)
engine.add_touchpoint("user_42", "social", datetime(2025, 1, 10), value=0)
engine.add_touchpoint("user_42", "email", datetime(2025, 1, 15), value=149.99)

# Calculate attribution for specific user
result = engine.calculate_attribution("user_42")
# {
#   'user_id': 'user_42',
#   'model': 'TIME_DECAY',
#   'channel_scores': {
#     'email': 0.60,
#     'search': 0.25,
#     'social': 0.15
#   },
#   'confidence': 1.0,
#   'total_touchpoints': 4,
#   'unique_channels': 3,
#   'conversion_value': 149.99
# }

# Get aggregated view across all users
aggregated = engine.get_aggregated_attribution()
# {
#   'model': 'TIME_DECAY',
#   'total_users': 1000,
#   'avg_channel_scores': {
#     'email': 0.45,
#     'search': 0.30,
#     'social': 0.25
#   },
#   'total_conversions': 150,
#   'total_revenue': 22500.00
# }

# Switch models for comparison
engine.set_model(AttributionModel.POSITION_BASED)
result_position = engine.calculate_attribution("user_42")
# Compare with time-decay result
```

**Models**:
| Model | Logic | Best For |
|-------|-------|----------|
| `FIRST_TOUCH` | 100% to first interaction | Awareness campaigns |
| `LAST_TOUCH` | 100% to last interaction | Direct response |
| `LINEAR` | Equal credit across all | Balanced view |
| `TIME_DECAY` | Recent weighted higher | Fast-moving B2C |
| `POSITION_BASED` | 40% first, 40% last, 20% middle | B2B consideration |

**Time Decay Formula**:
```python
# Weight decreases by half every half_life_days
weight = 2 ** (-days_before_conversion / half_life_days)
# Default half_life_days = 7
```

---

### 5. Content Generation

Create marketing content with brand voice consistency.

```python
from agents.marketing.agent import ContentGenerator

gen = ContentGenerator()

# Configure brand voice
gen.set_brand_voice(
    tone="professional",
    keywords=["innovation", "growth", "efficiency"],
    excluded_words=["cheap", "basic", "simple"]
)

# Register custom template
gen.add_template(
    template_id="product_launch",
    template="Introducing {{PRODUCT}}: {{TAGLINE}}. {{DESCRIPTION}}",
    content_type="EMAIL"
)

# Generate email
email = gen.generate_email(
    subject="Hello {{NAME}}",
    body="Welcome to {{PRODUCT}}. Explore our features today.",
    variables={"NAME": "Sarah", "PRODUCT": "Analytics Pro"}
)
# {
#   'subject': 'Hello Sarah',
#   'body': 'Welcome to Analytics Pro. Explore our features today.',
#   'word_count': 10,
#   'char_count': 52
# }

# Generate social post with platform-specific limits
twitter_post = gen.generate_social_post(
    platform="twitter",
    message="Big news coming soon! We're excited to announce our latest innovation in analytics technology.",
    include_cta=True
)
# Auto-truncated to 280 chars for Twitter

linkedin_post = gen.generate_social_post(
    platform="linkedin",
    message="Big news coming soon! We're excited to announce our latest innovation in analytics technology.",
    include_cta=True
)
# Respects 3000 char limit for LinkedIn

# Render template with variables
rendered = gen.render("product_launch", {
    "PRODUCT": "Analytics Pro",
    "TAGLINE": "Data-driven decisions, simplified",
    "DESCRIPTION": "Transform your data into actionable insights."
})

# Generate A/B test variants
variants = gen.ab_variants(
    original="Discover the future of analytics",
    variations=3
)
# [
#   {'variant_id': 'A', 'content': 'Discover the future of analytics'},
#   {'variant_id': 'B', 'content': 'Experience next-gen analytics today'},
#   {'variant_id': 'C', 'content': 'Unlock analytics innovation now'}
# ]
```

**Platform Limits**:
| Platform | Character Limit | Recommended |
|----------|----------------|-------------|
| Twitter | 280 | 240 (with media) |
| LinkedIn | 3000 | 1500 |
| Instagram | 2200 | 1250 |
| Facebook | 63206 | 40-80 (short) |
| Email | unlimited | Subject: 60 |

---

### 6. Analytics Dashboard

Track events, manage goals, and generate reports.

```python
from agents.marketing.agent import AnalyticsDashboard

dash = AnalyticsDashboard()

# Track events with custom properties
dash.track_event("page_view", {
    "page": "/pricing",
    "user_id": "u1",
    "session_id": "sess_abc",
    "referrer": "google.com"
})

dash.track_event("conversion", {
    "value": 299,
    "product": "pro_plan",
    "user_id": "u1",
    "campaign_id": "camp_xyz"
})

dash.track_event("email_open", {
    "user_id": "u1",
    "campaign_id": "camp_xyz",
    "email_id": "email_123"
})

# Set performance goals
dash.set_goal("revenue_q1", "revenue", 100000)
dash.set_goal("signups_q1", "conversions", 5000)

# Check goal progress
goal_progress = dash.get_goal_progress("revenue_q1")
# {
#   'goal_id': 'revenue_q1',
#   'metric': 'revenue',
#   'target': 100000,
#   'current': 45000,
#   'progress_percent': 45.0,
#   'on_track': True
# }

# Generate comprehensive report
report = dash.generate_report(days=30)
# {
#   'period': '2025-01-01 to 2025-01-30',
#   'total_events': 15420,
#   'events_by_type': {
#     'page_view': 12000,
#     'conversion': 420,
#     'email_open': 3000
#   },
#   'unique_users': 8500,
#   'total_revenue': 125000.00,
#   'conversion_rate': 3.48
# }

# Funnel analysis
funnel = dash.get_funnel([
    "page_view",
    "signup",
    "trial_start",
    "conversion"
])
# {
#   'stages': [
#     {'event': 'page_view', 'count': 10000, 'rate': 100.0},
#     {'event': 'signup', 'count': 2500, 'rate': 25.0},
#     {'event': 'trial_start', 'count': 1000, 'rate': 10.0},
#     {'event': 'conversion', 'count': 250, 'rate': 2.5}
#   ],
#   'biggest_dropoff': 'signup → trial_start'
# }
```

---

### 7. SEO Analysis

Evaluate content for search engine optimization.

```python
from agents.marketing.agent import SEOAnalyzer

seo = SEOAnalyzer()

# Analyze keyword usage
analysis = seo.analyze_keyword(
    keyword="marketing",
    content="Marketing strategy drives growth. Good marketing matters. Marketing is essential."
)
# {
#   'keyword': 'marketing',
#   'occurrences': 3,
#   'total_words': 10,
#   'density': 30.0,
#   'suggestions': ['Keyword density too high, reduce usage']
# }

# Generate SERP preview
preview = seo.serp_preview(
    title="Best Marketing Tools 2025 | Your Brand",
    description="Discover top marketing tools for your business. Compare features, pricing, and reviews.",
    url="https://example.com/marketing-tools",
    keyword="marketing"
)
# {
#   'title': 'Best Marketing Tools 2025 | Your Brand',
#   'title_length': 38,
#   'title_optimal': True,
#   'description': 'Discover top marketing tools...',
#   'desc_length': 75,
#   'desc_optimal': True,
#   'url': 'https://example.com/marketing-tools',
#   'keyword_in_title': True,
#   'keyword_in_desc': True
# }

# Full content score
score = seo.content_score(
    title="Marketing Guide 2025",
    body="Marketing is the practice of promoting products and services. " * 50,
    keyword="marketing"
)
# {
#   'overall_score': 0.85,
#   'title_length_ok': True,
#   'title_has_keyword': True,
#   'desc_length_ok': True,
#   'keyword_density_ok': True,
#   'content_length_ok': True,
#   'suggestions': []
# }

# Get keyword suggestions
suggestions = seo.get_keyword_suggestions("marketing strategy")
# [
#   {'keyword': 'marketing strategy', 'difficulty': 'medium', 'opportunity': 'high'},
#   {'keyword': 'digital marketing', 'difficulty': 'high', 'opportunity': 'medium'},
#   {'keyword': 'marketing plan', 'difficulty': 'low', 'opportunity': 'high'}
# ]
```

---

## Data Models

### AudienceSegment
| Field | Type | Description |
|-------|------|-------------|
| segment_id | str | Unique identifier (UUID) |
| name | str | Human-readable segment name |
| audience_type | AudienceType | Classification type |
| criteria | Dict[str, str] | Membership rules |
| estimated_size | int | Approximate audience count |
| growth_rate | float | Monthly growth percentage |
| tags | List[str] | Classification tags |
| created_at | datetime | Creation timestamp |
| updated_at | datetime | Last modification timestamp |

### Campaign
| Field | Type | Description |
|-------|------|-------------|
| campaign_id | str | Unique identifier (UUID) |
| name | str | Campaign name |
| channel | Channel | Marketing channel |
| status | CampaignStatus | Current lifecycle state |
| audience_segments | List[str] | Target segment IDs |
| content | Dict | Campaign content |
| budget | float | Allocated budget |
| spend | float | Amount spent |
| conversions | int | Conversion count |
| revenue | float | Revenue generated |
| tags | List[str] | Campaign tags |
| created_at | datetime | Creation timestamp |
| launched_at | datetime | Launch timestamp |
| completed_at | datetime | Completion timestamp |

### ROIMetric
| Field | Type | Description |
|-------|------|-------------|
| channel | str | Marketing channel name |
| revenue | float | Revenue generated |
| cost | float | Campaign cost |
| roi | float | Return on investment percentage |
| roas | float | Return on ad spend |
| cpa | float | Cost per acquisition |
| impressions | int | Ad impressions |
| clicks | int | Ad clicks |
| conversions | int | Conversion count |

### ConversionEvent
| Field | Type | Description |
|-------|------|-------------|
| conversion_id | str | Unique identifier |
| campaign_id | str | Associated campaign |
| user_id | str | User identifier |
| value | float | Conversion value |
| channel | Channel | Attribution channel |
| conversion_type | str | Type of conversion |
| timestamp | datetime | Conversion time |

### AttributionResult
| Field | Type | Description |
|-------|------|-------------|
| user_id | str | User identifier |
| model | AttributionModel | Model used |
| channel_scores | Dict[str, float] | Channel contribution |
| confidence | float | Attribution confidence |
| total_touchpoints | int | Total interactions |
| unique_channels | int | Distinct channels |
| conversion_value | float | Total conversion value |

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
- [ ] Hook callbacks registered
- [ ] Emergency pause procedure documented

### Monthly Marketing Review
- [ ] Campaign performance vs targets
- [ ] Budget utilization report
- [ ] Attribution analysis update
- [ ] Audience segment refresh
- [ ] Content performance review
- [ ] SEO ranking changes
- [ ] Reallocation recommendations applied
- [ ] Competitor activity assessment
- [ ] Brand consistency audit
- [ ] Team capacity planning

### SEO Audit Checklist
- [ ] Title tags optimized (≤60 chars)
- [ ] Meta descriptions written (≤160 chars)
- [ ] Keyword density within 1-3%
- [ ] Content length > 300 words
- [ ] Internal links added
- [ ] Alt text on images
- [ ] URL structure clean
- [ ] Schema markup implemented

---

## Troubleshooting

### Low Campaign ROI
1. Check attribution model — Last-touch may over-credit closing channels
2. Review audience targeting — Segment may be too broad
3. Analyze content performance — A/B test underperforming variants
4. Examine budget allocation — Shift toward higher-performing channels
5. Verify tracking setup — Ensure conversions are captured correctly

### Attribution Gaps
1. Ensure all touchpoints are tracked
2. Verify UTM parameters are consistent
3. Check cross-device tracking setup
4. Validate timestamp accuracy across sources
5. Review attribution model settings

### Budget Overspend
1. Review pacing rules on active campaigns
2. Check for duplicate targeting across campaigns
3. Implement daily spend caps
4. Audit automated bidding parameters
5. Set up overspend alerts

### Low Segment Scores
1. Enrich criteria with behavioral data
2. Verify estimated_size accuracy
3. Add growth_rate tracking
4. Consider combining complementary segments
5. Review segment freshness

### Content Not Performing
1. Test different A/B variants
2. Review brand voice consistency
3. Check platform character limits
4. Analyze engagement metrics by segment
5. Refresh templates quarterly

### SEO Issues
1. Verify keyword density (1-3%)
2. Check title and description lengths
3. Review content word count
4. Analyze competitor rankings
5. Update content regularly

---

## Integration Points

| System | Protocol | Purpose |
|--------|----------|---------|
| CRM | REST API | Customer data sync |
| ESP | Webhook/API | Email delivery and tracking |
| Ads Platform | API | Campaign management (Google, Meta) |
| Analytics | SDK/Event | Conversion tracking (GA4, Mixpanel) |
| DMP | API | Audience data enrichment |
| SEO Tools | API | Keyword and ranking data (SEMrush, Ahrefs) |
| Social Media | API | Post scheduling and analytics |
| CMS | API | Content publishing |

---

## Advanced Usage

### Multi-Channel Campaign Orchestration
```python
agent = MarketingAgent()

# Create channel-specific segments
email_seg = agent.audience.create_segment("Email Subscribers", AudienceType.BEHAVIORAL, {"opt_in": True}, 30000)
social_seg = agent.audience.create_segment("Social Followers", AudienceType.BEHAVIORAL, {"followed": True}, 50000)
search_seg = agent.audience.create_segment("Search Visitors", AudienceType.BEHAVIORAL, {"visited": True}, 20000)

# Launch parallel campaigns with coordinated budget
budgets = agent.budget.equal_split(50000, ["email", "social", "search"])

email_campaign = agent.campaigns.create_campaign("Email Blast", Channel.EMAIL, [email_seg.segment_id], {}, budgets["email"])
social_campaign = agent.campaigns.create_campaign("Social Push", Channel.SOCIAL, [social_seg.segment_id], {}, budgets["social"])
search_campaign = agent.campaigns.create_campaign("Search Ads", Channel.SEARCH, [search_seg.segment_id], {}, budgets["search"])

# Launch all
for campaign in [email_campaign, social_campaign, search_campaign]:
    agent.campaigns.launch_campaign(campaign.campaign_id)

# Unified attribution
agent.attribution.set_model(AttributionModel.TIME_DECAY)
```

### Custom Content Pipeline
```python
gen = ContentGenerator()
gen.set_brand_voice("professional", ["innovation", "growth"])

# Multi-format content creation
email_content = gen.generate_email("Hello {{NAME}}", "Welcome to {{PRODUCT}}...", vars)
social_content = gen.generate_social_post("twitter", "Excited to announce...", include_cta=True)
ad_content = gen.render("ad_template", {"headline": "Try Free", "body": "No credit card required"})

# A/B testing
variants = gen.ab_variants(email_content["subject"], variations=5)
```

### Automated Reporting Pipeline
```python
dash = AnalyticsDashboard()

# Generate weekly reports
report = dash.generate_report(days=7)
funnel = dash.get_funnel(["visit", "signup", "purchase"])

# Export for stakeholders
print(f"Revenue: ${report['total_revenue']:,.2f}")
print(f"Conversion Rate: {report['conversion_rate']:.2f}%")
print(f"Biggest Drop-off: {funnel['biggest_dropoff']}")
```
