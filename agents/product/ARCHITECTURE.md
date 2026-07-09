# Product Agent Architecture

> Comprehensive architecture for the Product Management Agent — strategy, roadmaps, OKRs, analytics, A/B testing, and go-to-market coordination.

---

## Table of Contents

1. [Overview](#overview)
2. [System Components](#system-components)
3. [Data Flow](#data-flow)
4. [Key Components](#key-components)
5. [Design Patterns](#design-patterns)
6. [Tech Stack](#tech-stack)
7. [Configuration](#configuration)
8. [Performance](#performance)
9. [Security](#security)
10. [Scalability](#scalability)
11. [Extension Points](#extension-points)
12. [Monitoring & Observability](#monitoring--observability)
13. [Glossary](#glossary)
14. [Appendix: Design Decisions](#appendix-design-decisions)

---

## Overview

The Product Agent is a comprehensive product management platform designed as a modular, extensible system. It integrates strategy formulation, roadmap planning, feature prioritization, user story management, OKR tracking, product analytics, A/B testing, feedback processing, and go-to-market coordination into a single orchestrated platform.

### Design Principles

- **Separation of Concerns**: Each subsystem is an independent module with well-defined interfaces.
- **Event-Driven Architecture**: Components communicate via events for loose coupling.
- **Data-Driven Decisions**: Every recommendation is backed by quantitative analysis.
- **Extensibility**: Plugin architecture for custom prioritization frameworks, analytics pipelines, and integrations.
- **Immutability Where Possible**: Audit trail for strategy changes and feature decisions.

---

## System Components

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           Product Agent (Orchestrator)                          │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────────┐  │
│  │ ProductStrategy  │  │  RoadmapPlanner   │  │    FeaturePrioritizer        │  │
│  │    Manager       │  │                   │  │  (RICE / MoSCoW / Weighted)  │  │
│  │                  │  │  ┌─────────────┐  │  └──────────────────────────────┘  │
│  │ • Vision         │  │  │  Horizon    │  │                                   │
│  │ • Strategy       │  │  │  Management │  │  ┌──────────────────────────────┐  │
│  │ • SWOT           │  │  └─────────────┘  │  │    UserStoryManager          │  │
│  │ • Competitive    │  │  ┌─────────────┐  │  │  • INVEST validation         │  │
│  │   Analysis       │  │  │  Releases   │  │  │  • Template engine           │  │
│  │ • Market Sizing  │  │  └─────────────┘  │  │  • Status transitions        │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────────────────┘  │
│                                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────────┐  │
│  │   OKRManager     │  │ ProductAnalytics  │  │     ABTestManager            │  │
│  │                  │  │                   │  │                              │  │
│  │ • Objectives     │  │ • Metrics         │  │ • Experiment lifecycle       │  │
│  │ • Key Results    │  │ • Funnels         │  │ • Statistical analysis       │  │
│  │ • Check-ins      │  │ • Cohorts         │  │ • Welch t-test               │  │
│  │ • Dashboard      │  │ • Retention       │  │ • Power analysis             │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────────────────┘  │
│                                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────────┐  │
│  │ FeedbackProcessor│  │   GTMManager     │  │  StakeholderManager          │  │
│  │                  │  │                  │  │                              │  │
│  │ • Categorization │  │ • Plans          │  │ • Engagement matrix          │  │
│  │ • Sentiment      │  │ • Activities     │  │ • Communication tracking     │  │
│  │ • Voting         │  │ • Budget         │  │ • Due reminders              │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────────────────┘  │
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐   │
│  │                         SprintManager                                    │   │
│  │  • Sprint creation  • Velocity tracking  • Health monitoring            │   │
│  └──────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

```
                         ┌─────────────────┐
                         │  Customer Input  │
                         │  Market Data     │
                         │  Team Feedback   │
                         └────────┬────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │    ProductStrategyManager   │
                    │  (Vision → Strategy → SWOT) │
                    └─────────────┬─────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
    ┌─────────▼─────────┐ ┌──────▼──────┐ ┌─────────▼─────────┐
    │  RoadmapPlanner    │ │  OKRManager │ │ FeedbackProcessor  │
    │  (Features →      │ │  (Goals →   │ │ (Feedback →        │
    │   Horizons →      │ │   KRs →     │ │  Categorize →      │
    │   Releases)       │ │   Progress) │ │  Prioritize)       │
    └─────────┬─────────┘ └──────┬──────┘ └─────────┬─────────┘
              │                   │                   │
              └───────────────────┼───────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │   FeaturePrioritizer        │
                    │   (RICE / MoSCoW / Weighted │
                    │    Scoring / Stack Rank)    │
                    └─────────────┬─────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
    ┌─────────▼─────────┐ ┌──────▼──────┐ ┌─────────▼─────────┐
    │ UserStoryManager   │ │ ABTestManager│ │   GTMManager      │
    │ (Stories →         │ │ (Design →   │ │ (Plan →           │
    │  INVEST →          │ │  Run →      │ │  Activities →     │
    │  Sprint Assign)    │ │  Analyze)   │ │  Execute)         │
    └─────────┬─────────┘ └──────┬──────┘ └─────────┬─────────┘
              │                   │                   │
              └───────────────────┼───────────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │     ProductAnalytics       │
                    │  (Metrics → Insights →     │
                    │   Dashboard → Decisions)   │
                    └────────────────────────────┘
```

### Data Contracts Between Components

| Source | Destination | Data Format | Frequency |
|--------|-------------|-------------|-----------|
| StrategyManager | RoadmapPlanner | Vision + Goals | On change |
| RoadmapPlanner | FeaturePrioritizer | Feature list | On update |
| FeaturePrioritizer | UserStoryManager | Ranked features | Per sprint |
| FeedbackProcessor | OKRManager | Feedback themes | Weekly |
| ABTestManager | ProductAnalytics | Experiment results | On completion |
| All Components | ProductAgent | Status snapshots | On demand |

---

## Key Components

### 1. ProductStrategyManager

The strategy layer defines vision, mission, competitive positioning, and market analysis.

**Data Model:**
```python
ProductVision:
  vision_id: str
  statement: str
  mission: str
  target_users: List[str]
  value_proposition: str
  key_differentiators: List[str]
  success_metrics: List[str]
  version: int

CompetitiveProfile:
  competitor_id: str
  name: str
  positioning: str
  strengths: List[str]
  weaknesses: List[str]
  pricing: Dict[str, Any]
  market_share: float
```

### 2. RoadmapPlanner

Manages feature roadmap with four planning horizons.

**Horizon Model:**
```
NOW (0-3 months)     → Features in development/testing
NEXT (3-6 months)    → Features planned for next quarter
LATER (6-12 months)  → Features on the radar
FUTURE (12+ months)  → Aspirational features
```

### 3. FeaturePrioritizer

Supports multiple prioritization frameworks:
- **RICE**: (Reach × Impact × Confidence) / Effort
- **MoSCoW**: Must Have, Should Have, Could Have, Won't Have
- **Value vs Effort Matrix**: Quick Wins, Big Bets, Fill-ins, Money Pits
- **Weighted Scoring**: Customizable weighted criteria
- **Stack Ranking**: Composite score ordering

### 4. UserStoryManager

**Story Lifecycle:**
```
DRAFT → REFINED → READY → IN_PROGRESS → IN_REVIEW → DONE
```

### 5. OKRManager

**Progress Formula:**
```
KR Progress = (current_value - start_value) / (target_value - start_value) × 100
Objective Status = weighted average of KR statuses + confidence score
```

### 6. ProductAnalytics

**Funnel Analysis:**
```
Step 1 (Visit) → Step 2 (Signup) → Step 3 (Activation) → Step 4 (Revenue)
     1000            400 (60%↓)        200 (50%↓)           80 (60%↓)
     Overall conversion: 8%
```

### 7. ABTestManager

**Statistical Methods:**
- Welch's t-test for unequal variances
- Beta incomplete function for t-distribution CDF
- Cohen's d effect size for power analysis
- Confidence interval computation

### 8. FeedbackProcessor

**Sentiment Algorithm:**
```
Score = (positive_words_matched - negative_words_matched) / total_matched_words
Range: -1.0 (very negative) to +1.0 (very positive)
```

### 9. GTMManager

Manages go-to-market plans across five phases: Discovery → Validation → Prepare → Launch → Post-Launch.

### 10. StakeholderManager

Manages stakeholder engagement using the Influence/Interest matrix.

### 11. SprintManager

Agile sprint management with velocity tracking and capacity planning.

---

## Design Patterns

| Pattern | Usage | Component |
|---------|-------|-----------|
| **Facade** | ProductAgent orchestrates all sub-components | Orchestrator |
| **Strategy** | Pluggable prioritization algorithms | FeaturePrioritizer |
| **Observer** | Status snapshots across components | Analytics |
| **Command** | Reversible strategy updates | StrategyManager |
| **Factory** | User story creation from templates | UserStoryManager |
| **Chain of Responsibility** | Quality gate evaluations | Gates |
| **Memento** | Strategy version history | StrategyManager |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| Data Structures | dataclasses, Enum |
| Statistics | statistics, math (beta incomplete, normal CDF) |
| Persistence | SQLite (optional), JSON serialization |
| Testing | pytest, hypothesis |
| Logging | Python logging module |

---

## Configuration

```python
ProductConfig(
    default_currency="USD",
    roadmap_horizons=3,
    okr_quarter="Q1 2024",
    confidence_threshold=0.7,
    min_sample_size=1000,
    significance_level=0.05,
    max_sprint_stories=10,
    feedback_vote_threshold=10,
    metric_retention_days=90,
)
```

---

## Performance

| Metric | Target | Notes |
|--------|--------|-------|
| Strategy query | < 5ms | In-memory dictionary |
| Roadmap rendering | < 10ms | O(n) sort |
| Prioritization scoring | < 50ms | For 1000 features |
| Statistical analysis | < 100ms | For 10K samples |
| Feedback sentiment | < 1ms per item | Dictionary lookup |
| Full status snapshot | < 20ms | Aggregated from all components |

---

## Security

- **Input Validation**: All public methods validate inputs before processing.
- **Audit Trail**: Strategy changes are logged with timestamps.
- **Access Control**: Method-level permission checks for sensitive operations.
- **Data Isolation**: Each experiment and OKR tracked independently.
- **No Secrets in Code**: Configuration via external config objects.

---

## Scalability

| Dimension | Strategy |
|-----------|----------|
| Feature volume | Sharded by horizon; index by tag |
| Metric volume | Time-bucketed storage with configurable retention |
| Experiment volume | Independent experiment lifecycle |
| Team size | Stakeholder engagement matrix scales O(n) |
| Multi-product | Extend with product_id dimension |

---

## Extension Points

1. **Custom Prioritization Frameworks**: Subclass or register new scoring algorithms.
2. **Analytics Plugins**: Custom data sources and metric calculators.
3. **Integration Hooks**: Webhook-based integrations for external tools.
4. **Report Formats**: Pluggable report generators (HTML, PDF, CSV).
5. **Notification Channels**: Email, Slack, webhook alerting.

---

## Monitoring & Observability

| Signal | Method |
|--------|--------|
| Component health | `full_status()` on ProductAgent |
| Strategy changes | Audit trail in `_history` |
| Experiment status | `ABTestManager.experiments` state |
| Feedback volume | `FeedbackProcessor.sentiment_summary()` |
| Sprint velocity | `SprintManager._velocity_history` |

---

## Glossary

| Term | Definition |
|------|-----------|
| RICE | Reach, Impact, Confidence, Effort prioritization |
| MoSCoW | Must, Should, Could, Won't prioritization |
| OKR | Objective and Key Result |
| TAM | Total Addressable Market |
| SAM | Serviceable Addressable Market |
| SOM | Serviceable Obtainable Market |
| GTM | Go-to-Market |
| INVEST | Independent, Negotiable, Valuable, Estimable, Small, Testable |

---

## Appendix: Design Decisions

| Decision | Rationale |
|----------|-----------|
| In-memory storage | Simplicity; persistence layer optional |
| Four roadmap horizons | Industry standard (Now/Next/Later/Future) |
| Welch's t-test over Student's | More robust for unequal sample sizes |
| Sentiment via word lists | No ML dependency; deterministic; fast |
| Audit trail as list | Simple append-only; query via list comprehension |
| Beta incomplete for p-values | Avoids scipy dependency for statistical tests |

---

## Sprint Management

### Sprint Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Sprint Lifecycle                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │  Planning   │───►│  Active     │───►│  Review     │───►│  Retro      │ │
│  │             │    │             │    │             │    │             │ │
│  │ • Backlog   │    │ • Daily     │    │ • Demo      │    │ • What went │ │
│  │   grooming  │    │   standup   │    │ • Metrics   │    │   well      │ │
│  │ • Capacity  │    │ • Task      │    │ • Stake-    │    │ • What to   │ │
│  │   planning  │    │   tracking  │    │   holder    │    │   improve   │ │
│  │ • Sprint    │    │ • Blocker   │    │   feedback  │    │ • Action    │ │
│  │   goal      │    │   resolution│    │             │    │   items     │ │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Velocity Tracking

```python
# Track sprint velocity over time
velocity_history = agent.sprint.velocity_history(last_n_sprints=6)

print("Sprint Velocity History:")
for sprint in velocity_history:
    print(f"  {sprint['name']}: {sprint['points_completed']} points")
    print(f"    Planned: {sprint['points_planned']}")
    print(f"    Completed: {sprint['points_completed']}")
    print(f"    Carry Over: {sprint['carry_over']}")
    print(f"    Completion Rate: {sprint['completion_rate']:.1f}%")

avg_velocity = sum(s['points_completed'] for s in velocity_history) / len(velocity_history)
print(f"\nAverage Velocity: {avg_velocity:.1f} points/sprint")
```

---

## Stakeholder Communication

### Stakeholder Matrix

```
┌─────────────────────────────────────────────────────────────┐
│              Influence/Interest Matrix                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  High Influence                                             │
│       │                                                      │
│       │  ┌─────────────┐    ┌─────────────┐                │
│       │  │  KEEP       │    │  MANAGE     │                │
│       │  │  SATISFIED  │    │  CLOSELY    │                │
│       │  │             │    │             │                │
│       │  │ Board       │    │ CEO         │                │
│       │  │ Investors   │    │ VP Product  │                │
│       │  │ Legal       │    │ VP Eng      │                │
│       │  └─────────────┘    └─────────────┘                │
│       │                                                      │
│       │  ┌─────────────┐    ┌─────────────┐                │
│       │  │  MONITOR    │    │  KEEP       │                │
│       │  │  (MINIMAL   │    │  INFORMED   │                │
│       │  │   EFFORT)   │    │             │                │
│       │  │             │    │             │                │
│       │  │ End users   │    │ Marketing   │                │
│       │  │ Community   │    │ Sales       │                │
│       │  │ Support     │    │ Customer    │                │
│       │  └─────────────┘    │ Success     │                │
│       │                      └─────────────┘                │
│  Low Influence                                              │
│       │                                                      │
│       └──────────────────────────────────────────────────────│
│              Low Interest          High Interest             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Communication Cadence

| Stakeholder | Frequency | Format | Content |
|-------------|-----------|--------|---------|
| CEO/VP | Weekly | 1:1 meeting | Strategic updates, blockers, decisions needed |
| Engineering | Daily | Standup | Sprint progress, blockers, coordination |
| Marketing | Bi-weekly | Email + meeting | Feature timeline, launch plans |
| Sales | Monthly | Demo | New features, roadmap preview |
| Customer Success | Weekly | Slack + meeting | User feedback, churn signals |
| Support | Weekly | Slack | Bug trends, feature requests |

---

## A/B Testing Framework

### Statistical Methods

```python
# Welch's t-test implementation
def welch_t_test(control_data, treatment_data):
    """
    Perform Welch's t-test for unequal variances.
    More robust than Student's t-test for real-world data.
    """
    n1, n2 = len(control_data), len(treatment_data)
    mean1, mean2 = sum(control_data)/n1, sum(treatment_data)/n2
    var1 = sum((x - mean1)**2 for x in control_data) / (n1 - 1)
    var2 = sum((x - mean2)**2 for x in treatment_data) / (n2 - 1)

    # Standard error
    se = math.sqrt(var1/n1 + var2/n2)

    # t-statistic
    t_stat = (mean2 - mean1) / se

    # Degrees of freedom (Welch-Satterthwaite)
    df = (var1/n1 + var2/n2)**2 / ((var1/n1)**2/(n1-1) + (var2/n2)**2/(n2-1))

    # p-value approximation
    p_value = 2 * (1 - t_cdf(abs(t_stat), df))

    return {
        "t_statistic": t_stat,
        "p_value": p_value,
        "significant": p_value < 0.05,
        "control_mean": mean1,
        "treatment_mean": mean2,
        "lift": (mean2 - mean1) / mean1 * 100,
    }
```

### Experiment Design Template

```python
# Create a well-designed experiment
experiment = agent.ab_test.create_experiment(
    name="New Pricing Page",
    hypothesis="Redesigned pricing page will increase conversion by 15%",
    metric="pricing_page_conversion",
    unit_of_analysis="user",
    unit_of_randomization="user_id",

    # Sample size calculation
    baseline_rate=0.12,  # 12% current conversion
    minimum_detectable_effect=0.15,  # 15% relative improvement
    statistical_power=0.80,
    significance_level=0.05,

    # Variants
    control={
        "name": "Current Design",
        "traffic_percentage": 50,
    },
    treatments=[
        {
            "name": "New Design A",
            "description": "Simplified pricing with social proof",
            "traffic_percentage": 50,
        },
    ],
)
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

## Testing Strategy

### Unit Test Coverage

```python
# Test Product Strategy Manager
class TestProductStrategy:
    def test_define_vision(self):
        strategy = ProductStrategyManager()
        vision = strategy.define_vision(
            statement="Empower small businesses",
            mission="Make powerful software accessible",
            target_users=["small business owners"],
            value_proposition="Enterprise features at SMB prices",
            differentiators=["AI-powered automation"],
            success_metrics=["NPS > 50"],
        )
        assert vision.statement == "Empower small businesses"

    def test_swot_analysis(self):
        strategy = ProductStrategyManager()
        strategy.define_vision(statement="Test", mission="Test", target_users=[], value_proposition="Test", differentiators=[], success_metrics=[])
        swot = strategy.swot_analysis()
        assert "strengths" in swot
        assert "weaknesses" in swot
        assert "opportunities" in swot
        assert "threats" in swot

# Test Feature Prioritizer
class TestFeaturePrioritizer:
    def test_rice_score(self):
        prioritizer = FeaturePrioritizer()
        feature = Feature("f1", "Test", "Desc", Priority.P1_HIGH, FeatureStatus.PLANNED, RoadmapHorizon.NOW, 5, 8, 0.8, 0.9)
        score = prioritizer.rice_score(feature, reach=10000, impact=3, confidence=0.9)
        assert score > 0

    def test_moscow_classification(self):
        prioritizer = FeaturePrioritizer()
        features = [
            Feature("f1", "Must", "Desc", Priority.P0_CRITICAL, FeatureStatus.PLANNED, RoadmapHorizon.NOW, 5, 8, 0.8, 0.9),
            Feature("f2", "Should", "Desc", Priority.P1_HIGH, FeatureStatus.PLANNED, RoadmapHorizon.NOW, 5, 8, 0.8, 0.9),
        ]
        result = prioritizer.moscow_classification(features, must_haves=["f1"])
        assert "f1" in result["must_have"]
        assert "f2" in result["should_have"]
```

### Integration Tests

```python
class TestProductIntegration:
    def test_full_feature_lifecycle(self):
        agent = ProductAgent()

        # Define vision
        agent.strategy.define_vision(statement="Test", mission="Test", target_users=[], value_proposition="Test", differentiators=[], success_metrics=[])

        # Add feature to roadmap
        feature = Feature("f1", "AI Reports", "Auto-generate reports", Priority.P0_CRITICAL, FeatureStatus.PLANNED, RoadmapHorizon.NOW, 8, 9, 0.9, 0.8)
        agent.roadmap.add_feature(feature)

        # Create user story
        story = agent.stories.create_story(
            user_role="business owner",
            action="generate reports automatically",
            benefit="save 5 hours per week",
            acceptance_criteria=["Report in 30 seconds"],
            priority=Priority.P1_HIGH,
            estimate=5.0,
        )

        # Create OKR
        objective = agent.okr.create_objective(
            statement="Increase adoption by 50%",
            owner="vp-product",
            quarter="Q1 2024",
            key_results=[{"statement": "Reach 10K MAU", "metric": "mau", "start_value": 5000, "target_value": 10000}],
        )

        # Get status
        status = agent.full_status()
        assert "roadmap" in status
        assert "okr" in status
```

---

## Testing Strategy

### Unit Test Coverage

```python
# Test Product Strategy Manager
class TestProductStrategy:
    def test_define_vision(self):
        strategy = ProductStrategyManager()
        vision = strategy.define_vision(
            statement="Empower small businesses",
            mission="Make powerful software accessible",
            target_users=["small business owners"],
            value_proposition="Enterprise features at SMB prices",
            differentiators=["AI-powered automation"],
            success_metrics=["NPS > 50"],
        )
        assert vision.statement == "Empower small businesses"

    def test_swot_analysis(self):
        strategy = ProductStrategyManager()
        strategy.define_vision(statement="Test", mission="Test", target_users=[], value_proposition="Test", differentiators=[], success_metrics=[])
        swot = strategy.swot_analysis()
        assert "strengths" in swot
        assert "weaknesses" in swot
        assert "opportunities" in swot
        assert "threats" in swot

# Test Feature Prioritizer
class TestFeaturePrioritizer:
    def test_rice_score(self):
        prioritizer = FeaturePrioritizer()
        feature = Feature("f1", "Test", "Desc", Priority.P1_HIGH, FeatureStatus.PLANNED, RoadmapHorizon.NOW, 5, 8, 0.8, 0.9)
        score = prioritizer.rice_score(feature, reach=10000, impact=3, confidence=0.9)
        assert score > 0

    def test_moscow_classification(self):
        prioritizer = FeaturePrioritizer()
        features = [
            Feature("f1", "Must", "Desc", Priority.P0_CRITICAL, FeatureStatus.PLANNED, RoadmapHorizon.NOW, 5, 8, 0.8, 0.9),
            Feature("f2", "Should", "Desc", Priority.P1_HIGH, FeatureStatus.PLANNED, RoadmapHorizon.NOW, 5, 8, 0.8, 0.9),
        ]
        result = prioritizer.moscow_classification(features, must_haves=["f1"])
        assert "f1" in result["must_have"]
        assert "f2" in result["should_have"]
```

### Integration Tests

```python
class TestProductIntegration:
    def test_full_feature_lifecycle(self):
        agent = ProductAgent()

        # Define vision
        agent.strategy.define_vision(statement="Test", mission="Test", target_users=[], value_proposition="Test", differentiators=[], success_metrics=[])

        # Add feature to roadmap
        feature = Feature("f1", "AI Reports", "Auto-generate reports", Priority.P0_CRITICAL, FeatureStatus.PLANNED, RoadmapHorizon.NOW, 8, 9, 0.9, 0.8)
        agent.roadmap.add_feature(feature)

        # Create user story
        story = agent.stories.create_story(
            user_role="business owner",
            action="generate reports automatically",
            benefit="save 5 hours per week",
            acceptance_criteria=["Report in 30 seconds"],
            priority=Priority.P1_HIGH,
            estimate=5.0,
        )

        # Create OKR
        objective = agent.okr.create_objective(
            statement="Increase adoption by 50%",
            owner="vp-product",
            quarter="Q1 2024",
            key_results=[{"statement": "Reach 10K MAU", "metric": "mau", "start_value": 5000, "target_value": 10000}],
        )

        # Get status
        status = agent.full_status()
        assert "roadmap" in status
        assert "okr" in status
```
