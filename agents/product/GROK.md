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
# Result: {'capture_rate': 0.01, 'sam_to_tam_ratio': 0.2, ...}

# SWOT analysis
swot = agent.strategy.swot_analysis()
# Result: {'strengths': [...], 'weaknesses': [...], 'opportunities': [...], 'threats': [...]}
```

### 2. Roadmap Planning

```python
from agents.product.agent import Feature, Priority, FeatureStatus, RoadmapHorizon

# Add features to roadmap
feature = Feature(
    feature_id="f001",
    name="AI Report Generator",
    description="Auto-generate reports from data",
    priority=Priority.P0_CRITICAL,
    status=FeatureStatus.PLANNED,
    horizon=RoadmapHorizon.NOW,
    effort=8,
    value=9,
    impact=0.9,
    confidence=0.8,
    owner="product-lead",
    tags=["ai", "reports"],
    dependencies=[],
    success_criteria=["50% of users try within 2 weeks"],
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow(),
)
agent.roadmap.add_feature(feature)

# Get roadmap
roadmap = agent.roadmap.get_roadmap()
# Result: {'now': [Feature], 'next': [], 'later': [], 'future': []}

# Check capacity
capacity = agent.roadmap.capacity_check(RoadmapHorizon.NOW, max_effort=40)
# Result: {'is_overloaded': False, 'utilization': 0.2, ...}
```

### 3. Feature Prioritization

```python
from agents.product.agent import FeaturePrioritizer

prioritizer = FeaturePrioritizer()

# RICE scoring
rice_score = prioritizer.rice_score(feature, reach=10000, impact=3, confidence=0.8)
# Result: 3000.0

# MoSCoW classification
moscow = prioritizer.moscow_classification([feature], must_haves=["f001"])
# Result: {'must_have': [feature], 'should_have': [], 'could_have': [], 'wont_have': []}

# Value vs Effort matrix
matrix = prioritizer.value_vs_effort_matrix([feature])
# Result: {'quick_wins': [feature], 'big_bets': [], 'fill_ins': [], 'money_pits': []}

# Stack ranking
ranked = prioritizer.stack_ranking([feature])
```

### 4. User Stories

```python
from agents.product.agent import UserStoryManager

stories = UserStoryManager()

# Create story
story = stories.create_story(
    user_role="business owner",
    action="generate financial reports automatically",
    benefit="I save 5 hours per week on manual reporting",
    acceptance_criteria=[
        "Report generated in under 30 seconds",
        "Supports PDF and Excel formats",
        "Includes charts and summaries",
    ],
    priority=Priority.P1_HIGH,
    estimate=5.0,
    tags=["reports", "automation"],
)

# Validate INVEST
invest = stories.validate_invest(story)
# Result: {'independent': True, 'negotiable': True, 'valuable': True, 'estimable': True, 'small': True, 'testable': True}

# Transition status
stories.transition(story.story_id, StoryStatus.READY)
```

### 5. OKR Tracking

```python
from agents.product.agent import OKRManager

okr = OKRManager()

# Create objective
objective = okr.create_objective(
    statement="Increase product adoption by 50%",
    owner="vp-product",
    quarter="Q1 2024",
    key_results=[
        {"statement": "Reach 10K MAU", "metric": "mau", "start_value": 5000, "target_value": 10000},
        {"statement": "Achieve NPS > 50", "metric": "nps", "start_value": 35, "target_value": 50},
        {"statement": "Reduce churn to < 5%", "metric": "churn", "start_value": 8, "target_value": 5},
    ],
)

# Check in
okr.check_in(
    objective_id=objective.objective_id,
    kr_updates={"kr001": 7500, "kr002": 45, "kr003": 6},
    confidence=0.7,
    notes="Strong growth from new onboarding flow",
)

# Get progress
progress = okr.progress(objective.objective_id)
# Result: {'overall_progress': 58.3, 'confidence': 0.7, 'status': 'on_track', ...}
```

### 6. Product Analytics

```python
from agents.product.agent import ProductAnalytics, MetricType

analytics = ProductAnalytics()

# Track metrics
analytics.track_metric("daily_active_users", 1250, MetricType.GAUGE)
analytics.track_metric("signup_count", 45, MetricType.COUNTER)

# Define and analyze funnel
analytics.define_funnel("activation", ["visit", "signup", "first_action", "activated"])
analytics.record_event({"event_type": "visit", "user_id": "u1"})
analytics.record_event({"event_type": "signup", "user_id": "u1"})
analytics.record_event({"event_type": "first_action", "user_id": "u1"})

funnel = analytics.analyze_funnel("activation")
# Result: {'overall_conversion': 33.3, 'steps': [...]}
```

### 7. A/B Testing

```python
from agents.product.agent import ABTestManager

ab = ABTestManager()

# Create experiment
exp = ab.create_experiment(
    name="New Onboarding Flow",
    hypothesis="Simplified onboarding increases activation by 15%",
    metric="activation_rate",
    control={"description": "Current flow", "traffic": 50},
    treatments=[{"name": "new_flow", "description": "Simplified 3-step", "traffic": 50}],
    sample_size=5000,
    confidence_level=0.95,
)

# Start and analyze
ab.start_experiment(exp.experiment_id)
results = ab.analyze_results(
    exp.experiment_id,
    control_data=[0.32, 0.35, 0.33, 0.34],
    treatment_data={"new_flow": [0.42, 0.45, 0.43, 0.44]},
)
# Result: {'winner': 'new_flow', 'recommendation': 'Deploy winner: new_flow', ...}
```

### 8. Go-to-Market

```python
from agents.product.agent import GTMManager, GTMPhase

gtm = GTMManager()

plan = gtm.create_plan(
    feature_id="f001",
    phase=GTMPhase.PREPARE,
    activities=[
        {"name": "Write blog post", "owner": "marketing"},
        {"name": "Create demo video", "owner": "product"},
        {"name": "Update docs", "owner": "engineering"},
    ],
    timeline={"launch": datetime(2024, 3, 1)},
    budget=50000,
    owner="gtm-lead",
    success_metrics=["1000 signups in first week", "Press coverage in 3 outlets"],
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
# Get today's priorities
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

*Powered by the Product Management Agent — strategic precision meets execution excellence.*
