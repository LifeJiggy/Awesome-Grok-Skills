---
name: "Indie Hacker Agent"
version: "2.0.0"
description: "Comprehensive AI-powered platform for solo entrepreneurs to build, launch, grow, and monetize software products with advanced business tools and automation"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["indie-hacker", "startup", "solo-entrepreneur", "saas", "mvp", "growth", "marketing", "analytics", "revenue", "customer-acquisition"]
category: "indie-hacker"
personality: "indie-entrepreneur"
use_cases: ["saas-development", "marketing-automation", "growth-hacking", "revenue-optimization", "customer-retention", "project-management"]
complexity: "advanced"
dependencies: ["python>=3.8"]
---

# Indie Hacker Agent

> Empowering Solo Founders with AI-Driven Startup Excellence

## Core Principles

1. **Ship Fast, Iterate Faster** — Done is better than perfect. Get to market quickly.
2. **Data Over Intuition** — Every decision backed by metrics, not gut feelings.
3. **Customer-Centric** — Build what customers need, not what you think they need.
4. **Sustainable Growth** — Profitable growth beats vanity metrics every time.
5. **Focus is Power** — Say no to everything except your core value proposition.

## Capabilities

### SaaS Financial Metrics

Calculate and project all key SaaS metrics:

```python
from agents.indie_hacker.agent import IndieHackerAgent

agent = IndieHackerAgent()

# Calculate MRR
mrr = agent.metrics.calculate_mrr(
    customers_by_tier={"starter": 100, "pro": 50, "enterprise": 10},
    pricing={"starter": 29, "pro": 79, "enterprise": 199}
)
# → 2900 + 3950 + 1990 = $8,840

# Calculate LTV
ltv = agent.metrics.calculate_ltv(
    mrr=8840, churn_rate=5.0, gross_margin=0.80, cac=200
)

# Calculate runway
runway = agent.metrics.calculate_runway(
    cash_balance=50000, monthly_burn=8000, monthly_revenue=8840
)
# → {"runway_months": 120.0, "is_profitable": True}

# Project growth
projections = agent.metrics.project_growth(
    current_mrr=8840, growth_rate_percent=15, churn_rate_percent=5, months=12
)
```

**Key Metrics:**
| Metric | Formula | Target |
|--------|---------|--------|
| MRR | Σ (customers × price) | Growing 10-20% MoM |
| ARR | MRR × 12 | — |
| LTV | (ARPU × Margin) / Churn | > 3x CAC |
| CAC | Spend / New Customers | < LTV/3 |
| Payback | CAC / (ARPU × Margin) | < 12 months |
| Quick Ratio | (New + Expansion) / (Contraction + Churn) | > 4 |
| Burn Rate | Cash / Months of Runway | Decreasing |

### Marketing Automation

```python
# Create campaign
campaign = agent.marketing_engine.create_campaign(
    name="Welcome Series",
    subject="Welcome to {product}!",
    segment="new_signups",
)

# Launch
result = agent.marketing_engine.launch_campaign(
    "Welcome Series",
    ["user1@example.com", "user2@example.com"]
)

# Create automation
automation = agent.marketing_engine.create_automation(
    name="Onboarding Flow",
    trigger="user_signup",
    actions=["send_welcome", "wait_2_days", "send_features", "wait_7_days", "send_check_in"],
)
```

### Customer Intelligence

```python
# Segment customers
active = agent.segmenter.segment_by_behavior(customers, "active")
at_risk = agent.segmenter.segment_by_behavior(customers, "at_risk")
power_users = agent.segmenter.segment_by_behavior(customers, "power_user")

# Predict churn
risk = agent.churn_predictor.predict_churn_risk(
    customer=customer,
    recent_metrics={"support_tickets": 3, "login_count": 2}
)
# → {"risk_level": "high", "recommendations": [...]}

# Analyze churn reasons
analysis = agent.churn_predictor.analyze_churn_reasons(churned_customers)
```

### Pricing Optimization

```python
# Add tiers
agent.pricing.add_tier("Starter", 29, features=["5 projects", "Basic analytics"])
agent.pricing.add_tier("Pro", 79, features=["Unlimited projects", "Advanced analytics", "API access"])
agent.pricing.add_tier("Enterprise", 199, features=["Everything in Pro", "Priority support", "Custom integrations"])
agent.pricing.set_popular_tier("Pro")

# Price elasticity analysis
elasticity = agent.pricing.calculate_price_elasticity(
    current_price=29, new_price=39, current_demand=100
)

# Competitive analysis
comparison = agent.pricing.compare_competitor_pricing([
    {"name": "Competitor A", "price": 35},
    {"name": "Competitor B", "price": 49},
    {"name": "Competitor C", "price": 25},
])
```

### Growth Experiments

```python
# Create experiment
experiment = agent.experiment_manager.create_experiment(
    name="CTA Button Test",
    hypothesis="Green buttons will increase clicks by 20%",
    metric="click_through_rate",
    sample_size=500,
    duration_days=14,
)

# Start and record results
agent.experiment_manager.start_experiment("CTA Button Test")
agent.experiment_manager.record_result("CTA Button Test", "control", 3.2)
agent.experiment_manager.record_result("CTA Button Test", "variant", 4.1)

# Analyze
result = agent.experiment_manager.complete_experiment("CTA Button Test")
# → {"winner": "variant", "lift": "+28.1%", "significant": true}
```

### Funnel Analysis

```python
# Create funnel
funnel = agent.funnel.create_funnel("Signup Flow", [
    {"name": "Landing Page", "visitors": 10000},
    {"name": "Sign Up Form", "visitors": 3000},
    {"name": "Email Verified", "visitors": 2500},
    {"name": "Onboarding Complete", "visitors": 1800},
    {"name": "First Value Action", "visitors": 1200},
])

# Analyze
analysis = agent.funnel.analyze_funnel("Signup Flow")
# → {"overall_conversion_rate": 12.0, "biggest_dropoff": {"stage": "Sign Up Form", "rate": 70.0}}
```

### Content Strategy

```python
# Create content
content = agent.content.create_content(
    title="How to Build a SaaS in 30 Days",
    content_type="blog",
    topic="saas-development",
)

# Track keywords
agent.content.add_keyword("build saas", volume=5000, difficulty=35, intent="informational")

# Plan editorial calendar
agent.content.plan_content([
    {"title": "SaaS Pricing Guide", "type": "blog", "date": "2026-08-01", "keywords": ["saas pricing"]},
    {"title": "Customer Retention Tips", "type": "blog", "date": "2026-08-15", "keywords": ["customer retention"]},
])

# SEO scoring
seo = agent.content.calculate_seo_score(content)
```

### Project Management

```python
# Create project
agent.project_manager.create_project("My SaaS", "A subscription analytics platform")

# Add tasks
task = agent.project_manager.add_task(
    "Implement authentication",
    priority=TaskPriority.CRITICAL,
    estimated_hours=8,
    tags=["backend", "auth"],
)

# Track time
agent.project_manager.log_time(task.id, "Implemented OAuth flow", hours=6.5)

# Get report
report = agent.project_manager.get_project_report("My SaaS")
```

### MVP Templates

```python
# Generate SaaS template
mvp = agent.mvp_engine.generate_saas_template(
    product_name="Analytics Dashboard",
    core_features=["Data visualization", "User reports", "Export"],
    tech_stack="modern",
)
# → {"timeline_weeks": 8, "tech_stack": {...}, "launch_checklist": [...]}
```

## Data Models

### Customer
| Field | Type | Description |
|-------|------|-------------|
| email | str | Customer email |
| name | str | Customer name |
| plan | str | Subscription tier |
| ltv | float | Lifetime value |
| health_score | int | Health score (0-100) |
| engagement_score | int | Engagement score (0-100) |

### Task
| Field | Type | Description |
|-------|------|-------------|
| id | str | Unique identifier |
| title | str | Task title |
| priority | TaskPriority | CRITICAL, HIGH, MEDIUM, LOW |
| status | TaskStatus | BACKLOG → DONE |
| estimated_hours | float | Time estimate |
| actual_hours | float | Time spent |

### EmailCampaign
| Field | Type | Description |
|-------|------|-------------|
| name | str | Campaign name |
| subject | str | Email subject |
| segment | str | Target segment |
| open_rate | float | Open rate (0-1) |
| click_rate | float | Click rate (0-1) |

### GrowthExperiment
| Field | Type | Description |
|-------|------|-------------|
| name | str | Experiment name |
| hypothesis | str | What you're testing |
| metric | str | Primary metric |
| control_conversion | float | Control group rate |
| variant_conversion | float | Variant group rate |

## Checklists

### MVP Launch
- [ ] Domain configured and SSL installed
- [ ] User authentication working
- [ ] Core feature implemented and tested
- [ ] Payment integration live
- [ ] Error monitoring active (Sentry)
- [ ] Analytics configured
- [ ] Terms of service ready
- [ ] Privacy policy ready
- [ ] Support process defined
- [ ] Landing page converted

### Growth Experiment
- [ ] Clear hypothesis defined
- [ ] Primary metric identified
- [ ] Sample size calculated
- [ ] Control and variant designed
- [ ] Tracking implemented
- [ ] Experiment started
- [ ] Results recorded
- [ ] Statistical significance checked
- [ ] Winner implemented
- [ ] Learnings documented

### Customer Retention
- [ ] Health scores configured
- [ ] Churn prediction active
- [ ] At-risk customers identified
- [ ] Outreach templates ready
- [ ] Win-back campaigns defined
- [ ] NPS survey configured
- [ ] Feedback loop established
- [ ] Success metrics tracked

## Troubleshooting

| Issue | Solution |
|-------|----------|
| MRR seems wrong | Check tier prices and customer counts match |
| LTV is infinite | Churn rate is 0 — set a minimum churn assumption |
| Experiment not significant | Increase sample size or extend duration |
| Funnel shows 0% conversion | Check visitor counts at each stage |
| Churn risk always low | Adjust thresholds and factor weights |
| Runway shows infinity | Revenue exceeds burn — set realistic revenue estimate |

## Integration Points

The agent integrates with:
- **Stripe** — Payment and subscription data
- **SendGrid / Mailchimp** — Email campaign delivery
- **Google Analytics** — Traffic and conversion data
- **Mixpanel / Amplitude** — Product analytics
- **Slack** — Team notifications
- **GitHub** — Development tracking
- **Intercom / Crisp** — Customer support data

---

*Empowering indie hackers to build better businesses, one decision at a time.*
