---
name: "Indie Hacker Agent"
version: "2.0.0"
description: "Comprehensive AI-powered platform for solo entrepreneurs to build, launch, grow, and monetize software products with advanced business tools and automation"
author: "Awesome Grok Skills"
license: "MIT"
tags:
  - indie-hacker
  - startup
  - solo-entrepreneur
  - saas
  - mvp
  - growth
  - marketing
  - analytics
  - revenue
  - customer-acquisition
  - retention
  - pricing
category: "indie-hacker"
personality: "indie-entrepreneur"
use_cases:
  - "saas-development"
  - "marketing-automation"
  - "growth-hacking"
  - "revenue-optimization"
  - "customer-retention"
  - "project-management"
  - "content-strategy"
  - "pricing-optimization"
  - "funnel-analysis"
  - "a-b-testing"
complexity: "advanced"
dependencies: ["python>=3.8"]
---

# Indie Hacker Agent

> Empowering Solo Founders with AI-Driven Startup Excellence

## Core Principles

1. **Ship Fast, Iterate Faster** — Done is better than perfect. Get to market quickly, then improve based on real feedback.

2. **Data Over Intuition** — Every decision backed by metrics, not gut feelings. If you can't measure it, it doesn't matter.

3. **Customer-Centric** — Build what customers need, not what you think they need. Talk to users daily.

4. **Sustainable Growth** — Profitable growth beats vanity metrics every time. Focus on revenue, not pageviews.

5. **Focus is Power** — Say no to everything except your core value proposition. Distraction kills startups.

6. **Retention > Acquisition** — Reducing churn is 5x cheaper than acquiring new customers. Fix retention first.

7. **Ship Weekly** — Small, frequent releases beat big quarterly launches. Stay in front of users.

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

# Track performance
stats = agent.marketing_engine.get_campaign_stats("Welcome Series")
print(f"Open rate: {stats['open_rate']:.1%}")
print(f"Click rate: {stats['click_rate']:.1%}")
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
# → {"top_reasons": ["price", "missing_feature", "support"], ...}
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

# Get recommendations
recs = agent.funnel.get_recommendations("Signup Flow")
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
print(f"Velocity: {report['velocity']} tasks/week")
print(f"Hours logged: {report['total_hours']}")
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

---

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
| created_at | str | Signup date |
| last_active | str | Last activity date |

### Task
| Field | Type | Description |
|-------|------|-------------|
| id | str | Unique identifier |
| title | str | Task title |
| priority | TaskPriority | CRITICAL, HIGH, MEDIUM, LOW |
| status | TaskStatus | BACKLOG → IN_PROGRESS → REVIEW → DONE |
| estimated_hours | float | Time estimate |
| actual_hours | float | Time spent |
| tags | List[str] | Category tags |

### EmailCampaign
| Field | Type | Description |
|-------|------|-------------|
| name | str | Campaign name |
| subject | str | Email subject line |
| segment | str | Target segment |
| open_rate | float | Open rate (0-1) |
| click_rate | float | Click rate (0-1) |
| status | str | draft → scheduled → sent → completed |

### GrowthExperiment
| Field | Type | Description |
|-------|------|-------------|
| name | str | Experiment name |
| hypothesis | str | What you're testing |
| metric | str | Primary metric |
| control_conversion | float | Control group rate |
| variant_conversion | float | Variant group rate |
| significant | bool | Statistical significance |
| winner | str | control or variant |

---

## Checklists

### MVP Launch
- [ ] Domain configured and SSL installed
- [ ] User authentication working (email + password minimum)
- [ ] Core feature implemented and tested
- [ ] Payment integration live (Stripe recommended)
- [ ] Error monitoring active (Sentry or equivalent)
- [ ] Analytics configured (Mixpanel, Amplitude, or GA4)
- [ ] Terms of service ready
- [ ] Privacy policy ready (GDPR compliant)
- [ ] Support process defined (email minimum)
- [ ] Landing page converted (> 2% signup rate)
- [ ] Onboarding flow complete (time to first value < 5 min)
- [ ] Mobile responsive (test on 3+ devices)

### Growth Experiment
- [ ] Clear hypothesis defined (testable statement)
- [ ] Primary metric identified (one metric that matters)
- [ ] Sample size calculated (statistical power > 80%)
- [ ] Control and variant designed (only one variable changed)
- [ ] Tracking implemented (verified with test data)
- [ ] Experiment started (minimum 7 days or 1000 users)
- [ ] Results recorded (no peeking at significance)
- [ ] Statistical significance checked (p < 0.05)
- [ ] Winner implemented (full rollout)
- [ ] Learnings documented (what worked, what didn't)

### Customer Retention
- [ ] Health scores configured (usage, support, payment signals)
- [ ] Churn prediction active (daily risk scoring)
- [ ] At-risk customers identified (score < 40)
- [ ] Outreach templates ready (personalized per risk reason)
- [ ] Win-back campaigns defined (email sequences)
- [ ] NPS survey configured (quarterly minimum)
- [ ] Feedback loop established (feature requests tracked)
- [ ] Success metrics tracked (retention rate, NRR)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| MRR seems wrong | Check tier prices and customer counts match; verify no double-counting |
| LTV is infinite | Churn rate is 0 — set a minimum churn assumption (0.5% minimum) |
| Experiment not significant | Increase sample size or extend duration; check for external factors |
| Funnel shows 0% conversion | Check visitor counts at each stage; verify tracking is working |
| Churn risk always low | Adjust thresholds and factor weights; add more behavioral signals |
| Runway shows infinity | Revenue exceeds burn — set realistic revenue estimate with growth rate |
| Quick ratio < 1 | You're losing more customers than gaining — focus on retention before acquisition |
| Payback > 12 months | Reduce CAC or increase ARPU; consider higher-tier pricing |

---

## Integration Points

The agent integrates with:
- **Stripe** — Payment and subscription data (MRR, churn, refunds)
- **SendGrid / Mailchimp** — Email campaign delivery and analytics
- **Google Analytics** — Traffic, conversion, and attribution data
- **Mixpanel / Amplitude** — Product analytics and user behavior
- **Slack** — Team notifications and alerts
- **GitHub** — Development tracking and release management
- **Intercom / Crisp** — Customer support data and satisfaction scores
- **Hotjar / FullStory** — User session recordings and heatmaps

---

## Best Practices

1. **Start with metrics** — Set up MRR tracking before anything else; you can't improve what you don't measure
2. **Automate early** — Use marketing automation from day one; manual follow-up doesn't scale
3. **Track everything** — Log time, track experiments, measure everything; data is your competitive advantage
4. **Focus on retention** — Reducing churn is 5x cheaper than acquiring new customers
5. **Ship weekly** — Small, frequent releases beat big quarterly launches; stay in front of users
6. **Listen to customers** — Health scores and churn predictions guide outreach; talk to users weekly
7. **Price for value** — Don't compete on price; compete on value; raise prices annually
8. **Build in public** — Share your journey; transparency builds trust and attracts early adopters
9. **Automate support** — FAQ, chatbots, and knowledge base reduce support burden by 60%
10. **Say no** — Feature requests will overwhelm you; focus on core value proposition

---

## Advanced Analytics

### Cohort Analysis

```python
# Analyze customer cohorts by signup month
cohort_analysis = agent.analytics.cohort_analysis(
    cohort_field="signup_month",
    metric="retention_rate",
    periods=12,
)
# Returns retention curves for each cohort

# Visualize cohort retention
for cohort, retention_data in cohort_analysis.items():
    print(f"Cohort {cohort}: {[f'{r:.1f}%' for r in retention_data]}")
```

### Revenue Forecasting

```python
# Forecast revenue based on current trends
forecast = agent.metrics.forecast_revenue(
    current_mrr=8840,
    growth_rate=0.15,
    churn_rate=0.05,
    months=12,
    scenarios={
        "optimistic": {"growth": 0.25, "churn": 0.03},
        "base": {"growth": 0.15, "churn": 0.05},
        "pessimistic": {"growth": 0.08, "churn": 0.08},
    },
}
```

---

## Advanced Analytics

### Cohort Analysis

```python
# Analyze customer cohorts by signup month
cohort_analysis = agent.analytics.cohort_analysis(
    cohort_field="signup_month",
    metric="retention_rate",
    periods=12,
)

# Visualize cohort retention
for cohort, retention_data in cohort_analysis.items():
    print(f"Cohort {cohort}: {[f'{r:.1f}%' for r in retention_data]}")
```

### Revenue Forecasting

```python
# Forecast revenue based on current trends
forecast = agent.metrics.forecast_revenue(
    current_mrr=8840,
    growth_rate=0.15,
    churn_rate=0.05,
    months=12,
    scenarios={
        "optimistic": {"growth": 0.25, "churn": 0.03},
        "base": {"growth": 0.15, "churn": 0.05},
        "pessimistic": {"growth": 0.08, "churn": 0.08},
    },
)

print(f"12-month forecast:")
print(f"  Optimistic: ${forecast['optimistic']['mrr']:,.0f}/mo")
print(f"  Base:       ${forecast['base']['mrr']:,.0f}/mo")
print(f"  Pessimistic: ${forecast['pessimistic']['mrr']:,.0f}/mo")
```

### Customer Segmentation Deep Dive

```python
# RFM Analysis (Recency, Frequency, Monetary)
rfm_segments = agent.segmenter.rfm_analysis(
    customers=active_customers,
    recency_bins=5,
    frequency_bins=5,
    monetary_bins=5,
)

# Segment definitions
segments = {
    "champions": {"recency": "5", "frequency": "5", "monetary": "5"},
    "loyal": {"recency": "4-5", "frequency": "4-5", "monetary": "3-5"},
    "at_risk": {"recency": "1-2", "frequency": "3-5", "monetary": "3-5"},
    "hibernating": {"recency": "1-2", "frequency": "1-2", "monetary": "1-2"},
    "new_customers": {"recency": "5", "frequency": "1", "monetary": "1"},
}
```

---

## Growth Playbooks

### Launch Playbook

```
Week -4: Pre-Launch
├── Set up analytics (Mixpanel/GA4)
├── Create landing page with email capture
├── Build waitlist of 100+ interested users
└── Prepare launch content (blog, social, email)

Week -2: Soft Launch
├── Invite beta testers (10-20 users)
├── Collect feedback and fix critical bugs
├── Optimize onboarding flow
└── Prepare support documentation

Week 0: Launch
├── Product Hunt launch (schedule for Tuesday)
├── Hacker News Show HN post
├── Email waitlist
├── Social media announcements
└── Reach out to press/influencers

Week +1: Post-Launch
├── Monitor metrics hourly
├── Respond to all feedback within 24 hours
├── Fix critical bugs immediately
├── Share launch results publicly
└── Follow up with early adopters
```

### Retention Playbook

```
Day 0: Welcome
├── Send welcome email with quick start guide
├── Trigger onboarding automation
└── Schedule 3-day check-in

Day 3: Engagement
├── Check if user completed first value action
├── If not, send helpful tips email
└── If yes, celebrate and suggest next feature

Day 7: Habit Formation
├── Review usage patterns
├── Send "Here's what you've accomplished" email
└── Introduce advanced features

Day 14: Value Reinforcement
├── Share ROI metrics (time saved, etc.)
├── Ask for feedback (NPS survey)
└── Offer help if usage is low

Day 30: Loyalty
├── Review monthly usage report
├── Offer upgrade if hitting limits
├── Invite to community/slack
└── Ask for testimonial/referral
```

---

## Monetization Strategies

### Pricing Model Comparison

```
┌─────────────────────────────────────────────────────────────┐
│              Pricing Model Decision Matrix                   │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ Model        │ Best For     │ Pros         │ Cons           │
├──────────────┼──────────────┼──────────────┼────────────────┤
│ Freemium     │ Viral growth │ Low CAC      │ Low conversion │
│ Free Trial   │ B2B SaaS     │ Quality leads│ High support   │
│ Usage-Based  │ API/Infra    │ Scales w/    │ Revenue unsure │
│              │              │ value        │                │
│ Seat-Based   │ Team tools   │ Predictable  │ Limits adoption│
│ Flat Rate    │ Simple tools │ Easy to sell │ Leaves money   │
│              │              │              │ on table       │
│ Tiered       │ Most SaaS    │ Captures all │ Complex to     │
│              │              │ segments     │ manage         │
└──────────────┴──────────────┴──────────────┴────────────────┘
```

### Price Optimization Framework

```python
def optimize_pricing(agent, current_tiers):
    """Run price optimization analysis."""

    # 1. Analyze current conversion rates by tier
    conversions = agent.pricing.get_conversion_rates()

    # 2. Survey willingness to pay
    wtp = agent.pricing.willingness_to_pay_survey(
        sample_size=100,
        questions=["How much would you pay for X?"],
    )

    # 3. Competitive analysis
    competitors = agent.pricing.compare_competitor_pricing([
        {"name": "Competitor A", "price": 29},
        {"name": "Competitor B", "price": 49},
        {"name": "Competitor C", "price": 99},
    ])

    # 4. Calculate price elasticity
    elasticity = agent.pricing.calculate_price_elasticity(
        current_price=current_tiers["pro"]["price"],
        new_price=current_tiers["pro"]["price"] * 1.2,
        current_demand=conversions["pro"]["count"],
    )

    # 5. Generate recommendations
    recommendations = agent.pricing.generate_recommendations(
        conversions=conversions,
        wtp=wtp,
        competitors=competitors,
        elasticity=elasticity,
    )

    return recommendations
```

---

## Technical Architecture

### Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Data Flow Architecture                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  External Sources                    Internal Processing                     │
│  ┌──────────────┐                   ┌──────────────────┐                    │
│  │ Stripe       │──── webhooks ────►│ Event Processor  │                    │
│  │ Analytics    │──── API ─────────►│                  │                    │
│  │ CRM          │──── sync ────────►│ ┌──────────────┐ │                    │
│  └──────────────┘                   │ │ Validation   │ │                    │
│                                     │ └──────┬───────┘ │                    │
│                                     │        │         │                    │
│                                     │ ┌──────▼───────┐ │                    │
│                                     │ │ Transform    │ │                    │
│                                     │ └──────┬───────┘ │                    │
│                                     │        │         │                    │
│                                     │ ┌──────▼───────┐ │                    │
│                                     │ │ Enrich       │ │                    │
│                                     │ └──────┬───────┘ │                    │
│                                     │        │         │                    │
│                                     │ ┌──────▼───────┐ │                    │
│                                     │ │ Store        │ │                    │
│                                     │ └──────────────┘ │                    │
│                                     └──────────────────┘                    │
│                                              │                              │
│                                     ┌────────▼────────┐                     │
│                                     │   Analytics     │                     │
│                                     │   Engine        │                     │
│                                     └────────┬────────┘                     │
│                                              │                              │
│                              ┌───────────────┼───────────────┐              │
│                              │               │               │              │
│                         ┌────▼────┐    ┌─────▼────┐   ┌─────▼────┐        │
│                         │ Dashboard│   │ Reports  │   │ Alerts   │        │
│                         └─────────┘    └──────────┘   └──────────┘        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Event-Driven Architecture

```python
# Event types and handlers
event_handlers = {
    "customer.signup": [
        "send_welcome_email",
        "create_trial_subscription",
        "add_to_onboarding_sequence",
        "update_metrics",
    ],
    "customer.churn": [
        "send_winback_email",
        "update_churn_metrics",
        "trigger_retention_analysis",
        "notify_success_team",
    ],
    "subscription.upgraded": [
        "send_upgrade_confirmation",
        "update_mrr",
        "track_conversion",
        "unlock_features",
    ],
    "experiment.completed": [
        "analyze_results",
        "notify_stakeholders",
        "update_recommendations",
        "archive_experiment",
    ],
}
```

---

## Scaling Strategies

### From $0 to $1K MRR

```
Focus: Product-Market Fit
├── Talk to 50+ potential customers
├── Build MVP in 2-4 weeks
├── Launch to small audience
├── Iterate based on feedback
└── Target: 10 paying customers

Key Metrics:
- Activation rate > 40%
- Day 7 retention > 30%
- NPS > 30
```

### From $1K to $10K MRR

```
Focus: Growth Channels
├── Double down on what works
├── Build content marketing machine
├── Implement referral program
├── Optimize conversion funnel
└── Target: 100 paying customers

Key Metrics:
- CAC < $100
- LTV > $300
- Payback < 3 months
```

### From $10K to $100K MRR

```
Focus: Scaling Operations
├── Hire first employees
├── Build customer success function
├── Implement advanced analytics
├── Expand to adjacent markets
└── Target: 1000 paying customers

Key Metrics:
- Quick Ratio > 4
- Net Revenue Retention > 110%
- Gross Margin > 70%
```

---

## Advanced Analytics

### Cohort Analysis

```python
# Analyze customer cohorts by signup month
cohort_analysis = agent.analytics.cohort_analysis(
    cohort_field="signup_month",
    metric="retention_rate",
    periods=12,
)

# Visualize cohort retention
for cohort, retention_data in cohort_analysis.items():
    print(f"Cohort {cohort}: {[f'{r:.1f}%' for r in retention_data]}")
```

### Revenue Forecasting

```python
# Forecast revenue based on current trends
forecast = agent.metrics.forecast_revenue(
    current_mrr=8840,
    growth_rate=0.15,
    churn_rate=0.05,
    months=12,
    scenarios={
        "optimistic": {"growth": 0.25, "churn": 0.03},
        "base": {"growth": 0.15, "churn": 0.05},
        "pessimistic": {"growth": 0.08, "churn": 0.08},
    },
)

print(f"12-month forecast:")
print(f"  Optimistic: ${forecast['optimistic']['mrr']:,.0f}/mo")
print(f"  Base:       ${forecast['base']['mrr']:,.0f}/mo")
print(f"  Pessimistic: ${forecast['pessimistic']['mrr']:,.0f}/mo")
```

### Customer Segmentation Deep Dive

```python
# RFM Analysis (Recency, Frequency, Monetary)
rfm_segments = agent.segmenter.rfm_analysis(
    customers=active_customers,
    recency_bins=5,
    frequency_bins=5,
    monetary_bins=5,
)

# Segment definitions
segments = {
    "champions": {"recency": "5", "frequency": "5", "monetary": "5"},
    "loyal": {"recency": "4-5", "frequency": "4-5", "monetary": "3-5"},
    "at_risk": {"recency": "1-2", "frequency": "3-5", "monetary": "3-5"},
    "hibernating": {"recency": "1-2", "frequency": "1-2", "monetary": "1-2"},
    "new_customers": {"recency": "5", "frequency": "1", "monetary": "1"},
}
```

---

*Empowering indie hackers to build better businesses, one decision at a time.*
