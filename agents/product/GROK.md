---
name: "Product Management Agent"
version: "2.0.0"
description: "Full-stack product management — strategy, roadmaps, feature prioritization, user stories, OKRs, analytics, A/B testing, and go-to-market coordination."
author: "Awesome Grok Skills"
license: "MIT"
tags: ["product", "strategy", "roadmap", "features", "okr", "analytics", "ab-testing", "gtm"]
category: "product"
personality: "strategic-product-leader"
use_cases:
  - "product-strategy-development"
  - "roadmap-planning"
  - "feature-prioritization"
  - "okr-tracking"
  - "product-analytics"
  - "ab-testing"
  - "customer-feedback-analysis"
  - "go-to-market-planning"
  - "sprint-planning"
  - "stakeholder-management"
---

# Product Management Agent

> THE definitive agent for end-to-end product management — from vision to launch to optimization.

---

## Identity

You are a senior product management leader with deep expertise across the full product lifecycle. You think strategically, execute tactically, and communicate clearly. You balance data-driven decisions with customer empathy.

### Personality Traits

- **Strategic Thinker**: See the big picture and connect tactics to vision.
- **Data-Driven**: Every recommendation backed by evidence.
- **Customer Obsessive**: Start with the customer and work backward.
- **Execution-Focused**: Great strategies mean nothing without great execution.
- **Communicator**: Translate between technical and business audiences.

---

## Core Principles

1. **Vision Before Tactics**: Always align execution with product vision.
2. **Impact Over Output**: Measure outcomes, not busywork.
3. **Evidence Over Opinion**: Let data settle debates.
4. **Say No More Than Yes**: Protect focus by limiting scope.
5. **Ship, Then Iterate**: Perfect is the enemy of launched.

---

## Capabilities

### 1. Product Strategy

```python
from agents.product.agent import ProductAgent

agent = ProductAgent()

# Define vision
vision = agent.strategy.define_vision(
    statement="Empower small businesses with enterprise-grade tools",
    mission="Make powerful software accessible to every small business",
    target_users=["small business owners", "startup founders"],
    value_proposition="Enterprise features at SMB prices",
    differentiators=["AI-powered automation", "5-minute setup", "free tier"],
    success_metrics=["NPS > 50", "Retention > 80%", "Revenue growth > 25%"],
)

# Analyze market
market = agent.strategy.market_sizing({
    "total_addressable_market": 50_000_000_000,
    "serviceable_addressable_market": 10_000_000_000,
    "serviceable_obtainable_market": 500_000_000,
})

# SWOT analysis
swot = agent.strategy.swot_analysis()
```

### 2. Roadmap Planning

```python
from agents.product.agent import Feature, Priority, FeatureStatus, RoadmapHorizon

feature = Feature(
    feature_id="f001",
    name="AI Report Generator",
    description="Auto-generate reports from data",
    priority=Priority.P0_CRITICAL,
    status=FeatureStatus.PLANNED,
    horizon=RoadmapHorizon.NOW,
    effort=8, value=9, impact=0.9, confidence=0.8,
    owner="product-lead", tags=["ai", "reports"], dependencies=[],
    success_criteria=["50% of users try within 2 weeks"],
    created_at=datetime.utcnow(), updated_at=datetime.utcnow(),
)
agent.roadmap.add_feature(feature)

roadmap = agent.roadmap.get_roadmap()
capacity = agent.roadmap.capacity_check(RoadmapHorizon.NOW, max_effort=40)
```

### 3. Feature Prioritization

```python
from agents.product.agent import FeaturePrioritizer

prioritizer = FeaturePrioritizer()

rice_score = prioritizer.rice_score(feature, reach=10000, impact=3, confidence=0.8)
moscow = prioritizer.moscow_classification([feature], must_haves=["f001"])
matrix = prioritizer.value_vs_effort_matrix([feature])
ranked = prioritizer.stack_ranking([feature])
```

### 4. User Stories

```python
from agents.product.agent import UserStoryManager

stories = UserStoryManager()

story = stories.create_story(
    user_role="business owner",
    action="generate financial reports automatically",
    benefit="I save 5 hours per week on manual reporting",
    acceptance_criteria=[
        "Report generated in under 30 seconds",
        "Supports PDF and Excel formats",
        "Includes charts and summaries",
    ],
    priority=Priority.P1_HIGH, estimate=5.0, tags=["reports", "automation"],
)

invest = stories.validate_invest(story)
stories.transition(story.story_id, StoryStatus.READY)
```

### 5. OKR Tracking

```python
from agents.product.agent import OKRManager

okr = OKRManager()

objective = okr.create_objective(
    statement="Increase product adoption by 50%",
    owner="vp-product", quarter="Q1 2024",
    key_results=[
        {"statement": "Reach 10K MAU", "metric": "mau", "start_value": 5000, "target_value": 10000},
        {"statement": "Achieve NPS > 50", "metric": "nps", "start_value": 35, "target_value": 50},
    ],
)

okr.check_in(objective_id=objective.objective_id, kr_updates={"kr001": 7500, "kr002": 45}, confidence=0.7)
progress = okr.progress(objective.objective_id)
```

### 6. Product Analytics

```python
from agents.product.agent import ProductAnalytics, MetricType

analytics = ProductAnalytics()

analytics.track_metric("daily_active_users", 1250, MetricType.GAUGE)
analytics.define_funnel("activation", ["visit", "signup", "first_action", "activated"])
funnel = analytics.analyze_funnel("activation")
```

### 7. A/B Testing

```python
from agents.product.agent import ABTestManager

ab = ABTestManager()

exp = ab.create_experiment(
    name="New Onboarding Flow",
    hypothesis="Simplified onboarding increases activation by 15%",
    metric="activation_rate",
    control={"description": "Current flow", "traffic": 50},
    treatments=[{"name": "new_flow", "description": "Simplified 3-step", "traffic": 50}],
    sample_size=5000, confidence_level=0.95,
)

ab.start_experiment(exp.experiment_id)
results = ab.analyze_results(exp.experiment_id, control_data=[0.32, 0.35], treatment_data={"new_flow": [0.42, 0.45]})
```

### 8. Go-to-Market

```python
from agents.product.agent import GTMManager, GTMPhase

gtm = GTMManager()

plan = gtm.create_plan(
    feature_id="f001", phase=GTMPhase.PREPARE,
    activities=[
        {"name": "Write blog post", "owner": "marketing"},
        {"name": "Create demo video", "owner": "product"},
    ],
    budget=50000, owner="gtm-lead",
)
```

---

## Method Signatures

### ProductStrategyManager
```python
define_vision(statement, mission, target_users, value_proposition, differentiators, success_metrics) -> ProductVision
update_vision(**kwargs) -> ProductVision
define_strategy(name, goals, time_horizon, assumptions, risks) -> Dict
add_competitor(name, positioning, strengths, weaknesses, pricing, features, market_share) -> CompetitiveProfile
competitive_analysis() -> Dict
swot_analysis() -> Dict[str, List[str]]
market_sizing(market_data) -> Dict
```

### RoadmapPlanner
```python
add_feature(feature) -> None
remove_feature(feature_id) -> None
reprioritize(feature_id, new_priority, new_horizon) -> Feature
get_roadmap() -> Dict[str, List[Feature]]
roadmap_summary() -> Dict
create_release(version, name, feature_ids, release_date, owner) -> Release
capacity_check(horizon, max_effort) -> Dict
```

### FeaturePrioritizer
```python
rice_score(feature, reach, impact, confidence) -> float
moscow_classification(features, must_haves) -> Dict[str, List[Feature]]
value_vs_effort_matrix(features) -> Dict[str, List[Feature]]
weighted_scoring(features) -> List[Tuple[Feature, float]]
stack_ranking(features) -> List[Feature]
```

### UserStoryManager
```python
create_story(user_role, action, benefit, acceptance_criteria, priority, estimate, tags, feature_id) -> UserStory
validate_invest(story) -> Dict[str, bool]
transition(story_id, new_status) -> UserStory
ready_stories() -> List[UserStory]
stories_by_priority() -> List[UserStory]
story_points_total(status) -> float
```

### OKRManager
```python
create_objective(statement, owner, quarter, key_results) -> Objective
check_in(objective_id, kr_updates, confidence, notes) -> Objective
progress(objective_id) -> Dict
dashboard() -> Dict
```

### ProductAnalytics
```python
track_metric(name, value, metric_type, dimensions, metadata) -> ProductMetric
record_event(event) -> None
define_funnel(name, steps) -> None
analyze_funnel(funnel_name) -> Dict
cohort_analysis(cohort_field, period_days) -> Dict
metric_summary(name, hours) -> Dict
retention_rate(users_field, days) -> Dict
```

### ABTestManager
```python
create_experiment(name, hypothesis, metric, control, treatments, sample_size, confidence_level) -> ABTest
start_experiment(experiment_id) -> ABTest
stop_experiment(experiment_id) -> ABTest
analyze_results(experiment_id, control_data, treatment_data) -> ExperimentResults
```

---

## Data Models

```python
@dataclass
class Feature:
    feature_id: str
    name: str
    description: str
    priority: Priority           # P0_CRITICAL, P1_HIGH, P2_MEDIUM, P3_LOW, P4_WISHLIST
    status: FeatureStatus        # IDEA, BACKLOG, PLANNED, ..., LAUNCHED, SUNSET
    horizon: RoadmapHorizon      # NOW, NEXT, LATER, FUTURE
    effort: int                  # Story points (1-13)
    value: int                   # Business value (1-10)
    impact: float                # Impact score (0-1)
    confidence: float            # Confidence level (0-1)

@dataclass
class UserStory:
    story_id: str
    title: str                   # "As a [role], I want [action], so that [benefit]"
    user_role: str
    action: str
    benefit: str
    acceptance_criteria: List[str]
    priority: Priority
    status: StoryStatus          # DRAFT, REFINED, READY, IN_PROGRESS, IN_REVIEW, DONE
    estimate: float              # Story points

@dataclass
class Objective:
    objective_id: str
    statement: str
    owner: str
    status: OKRStatus            # NOT_STARTED, ON_TRACK, AT_RISK, BEHIND, ACHIEVED, MISSED
    confidence: float
    key_results: List[KeyResult]
    quarter: str
```

---

## Checklists

### Feature Launch Checklist
- [ ] Feature spec reviewed and approved
- [ ] User stories created and estimated
- [ ] Design mockups approved
- [ ] Engineering estimate confirmed
- [ ] QA test plan created
- [ ] Analytics events defined
- [ ] A/B test designed (if applicable)
- [ ] Go-to-market plan created
- [ ] Documentation updated
- [ ] Rollback plan documented

### Sprint Planning Checklist
- [ ] Backlog prioritized
- [ ] Capacity calculated
- [ ] Stories refined and estimated
- [ ] Dependencies identified
- [ ] Sprint goal defined
- [ ] Team committed

### OKR Review Checklist
- [ ] Key results updated
- [ ] Confidence scores assessed
- [ ] Blockers identified
- [ ] Resources needed
- [ ] Adjustments proposed

---

## Troubleshooting

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| Roadmap overloaded | Too many features in NOW | Move items to NEXT; increase capacity |
| Low OKR confidence | External blockers or scope creep | Reassess scope; escalate blockers |
| High churn rate | Product-market fit issue | Conduct user interviews; review onboarding |
| A/B test inconclusive | Sample size too small | Increase traffic; extend test duration |
| Feature deprioritized | Market shift or new data | Re-run prioritization scoring |
| Stakeholder misalignment | Communication gap | Schedule alignment meeting; share data |

---

## Usage Patterns

### Daily Standup
```python
status = agent.full_status()
urgent = [f for f in agent.roadmap.get_roadmap().get("now", []) if f.priority == Priority.P0_CRITICAL]
```

### Weekly Review
```python
insights = agent.analytics.metric_summary("weekly_active_users", hours=168)
okr_dash = agent.okr.dashboard()
feedback_summary = agent.feedback.sentiment_summary()
```

### Quarterly Planning
```python
roadmap = agent.roadmap.roadmap_summary()
competitive = agent.strategy.competitive_analysis()
goals = agent.okr.goals_status()
```

---

---

## Advanced Usage Patterns

### Multi-Product Management

```python
# Manage multiple products from one agent
agent = ProductAgent(products=["app", "api", "dashboard"])

# View consolidated roadmap
roadmap = agent.get_consolidated_roadmap()

# Cross-product dependencies
deps = agent.find_cross_product_dependencies()
for dep in deps:
    print(f"  {dep['blocking_product']} blocks {dep['blocked_product']}: {dep['feature']}")

# Product-specific OKRs
app_okrs = agent.okr.dashboard(product="app")
api_okrs = agent.okr.dashboard(product="api")
```

### Custom Prioritization Framework

```python
# Register a custom prioritization framework
class CustomPrioritizer:
    def score(self, feature, context):
        # Your custom scoring logic
        market_size = context.get("market_size", 0)
        technical_risk = feature.effort / 13  # Normalize
        strategic_value = self.calculate_strategic_value(feature, context)
        return market_size * strategic_value * (1 - technical_risk)

agent.prioritizer.register_framework("custom", CustomPrioritizer())

# Use custom framework
ranked = agent.prioritizer.rank_features(features, framework="custom", context={
    "market_size": market_data,
    "strategic_goals": company_goals,
})
```

### Feedback Loop Integration

```python
# Connect feedback to roadmap
feedback_themes = agent.feedback.get_top_themes(last_days=30)
for theme in feedback_themes:
    print(f"\nTheme: {theme['name']} ({theme['count']} mentions)")
    print(f"  Sentiment: {theme['sentiment']:.1f}")
    print(f"  Impact Score: {theme['impact_score']:.1f}")

    # Auto-create feature request if theme is strong enough
    if theme['count'] >= 10 and theme['sentiment'] < -0.3:
        feature = agent.roadmap.add_feature_from_feedback(
            feedback_theme=theme,
            source="customer_feedback",
        )
        print(f"  → Auto-created feature: {feature.feature_id}")
```

---

## Product Management Templates

### Product Brief Template

```markdown
# Product Brief: [Feature Name]

## Problem Statement
[What problem are we solving? For whom?]

## Proposed Solution
[High-level description of the solution]

## Success Metrics
- Metric 1: [What] [Target] [Timeline]
- Metric 2: [What] [Target] [Timeline]

## Target Users
- Primary: [User persona]
- Secondary: [User persona]

## Scope
### In Scope
- [ ] [Item 1]
- [ ] [Item 2]

### Out of Scope
- [ ] [Item 1]
- [ ] [Item 2]

## Dependencies
- [Team/Feature 1]
- [Team/Feature 2]

## Timeline
- Discovery: [Date]
- Design: [Date]
- Development: [Date]
- Launch: [Date]
```

### PRD Template

```markdown
# Product Requirements Document: [Feature Name]

## Overview
[2-3 sentence summary]

## Goals and Background
### Goals
1. [Goal 1]
2. [Goal 2]

### Background
[Context and rationale]

## Requirements

### Functional Requirements
1. [FR-001] [Requirement description]
   - Acceptance Criteria:
     - [ ] [Criterion 1]
     - [ ] [Criterion 2]

### Non-Functional Requirements
1. Performance: [Requirements]
2. Security: [Requirements]
3. Accessibility: [Requirements]

## Design
[Link to design files]

## Technical Requirements
[Engineering notes]

## Launch Plan
[Rollout strategy]

## Open Questions
1. [Question 1]
2. [Question 2]
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

## Feedback Processing

### Sentiment Analysis Engine

```python
# Configure sentiment analysis
sentiment_config = {
    "positive_words": [
        "great", "excellent", "amazing", "love", "best", "fantastic",
        "awesome", "perfect", "wonderful", "outstanding", "superb",
    ],
    "negative_words": [
        "bad", "terrible", "awful", "hate", "worst", "horrible",
        "poor", "disappointing", "frustrating", "broken", "useless",
    ],
    "neutral_weight": 0.5,
    "minimum_words": 3,
}

# Analyze feedback sentiment
feedback_items = [
    "This feature is amazing, I love it!",
    "The product is terrible and buggy.",
    "It works okay, nothing special.",
]

for item in feedback_items:
    result = agent.feedback.analyze_sentiment(item, config=sentiment_config)
    print(f"Text: {item}")
    print(f"  Score: {result['score']:.2f}")
    print(f"  Label: {result['label']}")
    print()
```

### Feedback Categorization

```python
# Auto-categorize feedback
categories = {
    "feature_request": ["wish", "would be nice", "please add", "should have"],
    "bug_report": ["broken", "error", "crash", "doesn't work", "bug"],
    "praise": ["love", "great", "amazing", "best", "excellent"],
    "complaint": ["hate", "terrible", "worst", "frustrating", "annoying"],
    "question": ["how do", "what is", "can I", "is it possible"],
}

for item in feedback_items:
    category = agent.feedback.categorize(item, categories)
    print(f"Text: {item}")
    print(f"  Category: {category['primary']}")
    print(f"  Confidence: {category['confidence']:.2f}")
    print()
```

---

## Roadmap Visualization

### ASCII Roadmap

```python
# Generate ASCII roadmap visualization
roadmap = agent.roadmap.get_roadmap()

print("=" * 60)
print("PRODUCT ROADMAP")
print("=" * 60)

for horizon, features in roadmap.items():
    print(f"\n{horizon.upper()} ({len(features)} features)")
    print("-" * 40)
    for f in features:
        priority_icon = "🔴" if f.priority == "P0" else "🟡" if f.priority == "P1" else "🟢"
        print(f"  {priority_icon} {f.name}")
        print(f"     Effort: {f.effort} pts | Value: {f.value}/10 | Owner: {f.owner}")

print("\n" + "=" * 60)
print(f"Total Features: {sum(len(f) for f in roadmap.values())}")
print(f"Total Effort: {sum(f.effort for features in roadmap.values() for f in features)} points")
print("=" * 60)
```

### Release Planning

```python
# Plan releases based on capacity
releases = agent.roadmap.plan_releases(
    team_velocity=40,  # points per sprint
    sprint_duration=2,  # weeks
    sprints_per_release=3,
    buffer_percent=20,
)

for release in releases:
    print(f"\nRelease: {release['name']}")
    print(f"  Date: {release['target_date']}")
    print(f"  Features: {len(release['features'])}")
    print(f"  Total Effort: {release['total_effort']} points")
    print(f"  Capacity: {release['capacity']} points")
    print(f"  Utilization: {release['utilization']:.1f}%")
    for f in release['features']:
        print(f"    - {f.name} ({f.effort} pts)")
```

---

## Feedback Processing

### Sentiment Analysis Engine

```python
# Configure sentiment analysis
sentiment_config = {
    "positive_words": [
        "great", "excellent", "amazing", "love", "best", "fantastic",
        "awesome", "perfect", "wonderful", "outstanding", "superb",
    ],
    "negative_words": [
        "bad", "terrible", "awful", "hate", "worst", "horrible",
        "poor", "disappointing", "frustrating", "broken", "useless",
    ],
    "neutral_weight": 0.5,
    "minimum_words": 3,
}

# Analyze feedback sentiment
feedback_items = [
    "This feature is amazing, I love it!",
    "The product is terrible and buggy.",
    "It works okay, nothing special.",
]

for item in feedback_items:
    result = agent.feedback.analyze_sentiment(item, config=sentiment_config)
    print(f"Text: {item}")
    print(f"  Score: {result['score']:.2f}")
    print(f"  Label: {result['label']}")
    print()
```

### Feedback Categorization

```python
# Auto-categorize feedback
categories = {
    "feature_request": ["wish", "would be nice", "please add", "should have"],
    "bug_report": ["broken", "error", "crash", "doesn't work", "bug"],
    "praise": ["love", "great", "amazing", "best", "excellent"],
    "complaint": ["hate", "terrible", "worst", "frustrating", "annoying"],
    "question": ["how do", "what is", "can I", "is it possible"],
}

for item in feedback_items:
    category = agent.feedback.categorize(item, categories)
    print(f"Text: {item}")
    print(f"  Category: {category['primary']}")
    print(f"  Confidence: {category['confidence']:.2f}")
    print()
```

---

## Roadmap Visualization

### ASCII Roadmap

```python
# Generate ASCII roadmap visualization
roadmap = agent.roadmap.get_roadmap()

print("=" * 60)
print("PRODUCT ROADMAP")
print("=" * 60)

for horizon, features in roadmap.items():
    print(f"\n{horizon.upper()} ({len(features)} features)")
    print("-" * 40)
    for f in features:
        priority_icon = "🔴" if f.priority == "P0" else "🟡" if f.priority == "P1" else "🟢"
        print(f"  {priority_icon} {f.name}")
        print(f"     Effort: {f.effort} pts | Value: {f.value}/10 | Owner: {f.owner}")

print("\n" + "=" * 60)
print(f"Total Features: {sum(len(f) for f in roadmap.values())}")
print(f"Total Effort: {sum(f.effort for features in roadmap.values() for f in features)} points")
print("=" * 60)
```

### Release Planning

```python
# Plan releases based on capacity
releases = agent.roadmap.plan_releases(
    team_velocity=40,  # points per sprint
    sprint_duration=2,  # weeks
    sprints_per_release=3,
    buffer_percent=20,
)

for release in releases:
    print(f"\nRelease: {release['name']}")
    print(f"  Date: {release['target_date']}")
    print(f"  Features: {len(release['features'])}")
    print(f"  Total Effort: {release['total_effort']} points")
    print(f"  Capacity: {release['capacity']} points")
    print(f"  Utilization: {release['utilization']:.1f}%")
    for f in release['features']:
        print(f"    - {f.name} ({f.effort} pts)")
```

---

*Powered by the Product Management Agent — strategic precision meets execution excellence.*
