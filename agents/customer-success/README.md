# Customer Success Agent

A comprehensive customer success management platform with onboarding workflows, health scoring, expansion revenue tracking, QBR management, advocacy programs, success plans, renewal tracking, risk assessment, milestone management, value realization, workload management, feedback collection, and adoption journey tracking.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Onboarding](#onboarding)
  - [Health Scoring](#health-scoring)
  - [Expansion Revenue](#expansion-revenue)
  - [QBR Management](#qbr-management)
  - [Advocacy Programs](#advocacy-programs)
  - [Success Plans](#success-plans)
  - [Usage Tracking](#usage-tracking)
  - [Renewal Tracking](#renewal-tracking)
  - [Risk Assessment](#risk-assessment)
  - [Milestone Tracking](#milestone-tracking)
  - [Value Realization](#value-realization)
  - [CSM Workload](#csm-workload)
  - [Customer Feedback](#customer-feedback)
  - [Adoption Journey](#adoption-journey)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

The Customer Success Agent provides tools for managing the entire customer success lifecycle from onboarding through expansion and advocacy. It helps teams proactively manage customer health, identify growth opportunities, manage renewals, assess risks, track adoption journeys, and build lasting customer relationships.

The agent uses an orchestrator pattern with 14 independent subsystems, each managing its own data and thread-safe locking strategy. This architecture allows parallel operations across subsystems while maintaining data consistency.

## Features

- **Onboarding Workflows**: Milestone-based onboarding with progress tracking and velocity reports
- **Health Scoring**: Weighted multi-metric health calculation with trend analysis
- **Expansion Revenue**: Pipeline tracking for upsell and cross-sell with win-rate analytics
- **QBR Management**: Quarterly Business Review scheduling, execution, and completion tracking
- **Advocacy Programs**: Referral codes, case studies, testimonials, and top-advocate ranking
- **Success Plans**: Goal-oriented plans with milestone tracking and at-risk detection
- **Usage Tracking**: Product adoption metrics, scoring, and trend analysis
- **Renewal Tracking**: Renewal lifecycle management with risk scoring
- **Risk Assessment**: Customer risk evaluation with mitigation action plans
- **Milestone Tracking**: Customer milestones across onboarding, product, relationship, and contract types
- **Value Realization**: Value progression tracking from initial adoption to maximum value
- **CSM Workload Management**: Balanced task assignment across customer success managers
- **Customer Feedback**: Multi-source feedback collection with sentiment analysis and NPS
- **Adoption Journey**: Phase-based adoption tracking with blocker identification

## Quick Start

```python
from agents.customer_success.agent import CustomerSuccessAgent, Config

agent = CustomerSuccessAgent(Config())
agent.initialize()

# Add customer
agent.add_customer("cust_001", name="Acme Corp", plan="professional", mrr=2000)

# Start onboarding
agent.start_onboarding("cust_001")

# Track health
agent.record_health_metric("cust_001", "product_usage", 85)
agent.record_health_metric("cust_001", "engagement", 70)

# Get health score
health = agent.get_health_score("cust_001")
print(f"Health: {health['health_status']} ({health['health_score']})")

# Record adoption phase
agent.record_adoption("cust_001", AdoptionPhase.REGULAR_USE, 65.0)

# Record feedback
agent.record_feedback("cust_001", FeedbackSource.NPS, 9.0, "Excellent product")

# Get full report
report = agent.get_full_report()

agent.shutdown()
```

## Usage

### Onboarding

```python
# Start onboarding (creates 6 milestone tasks)
agent.start_onboarding("cust_001")

# Check progress
progress = agent.get_onboarding_progress("cust_001")
# {'current_stage': 'TRAINING', 'progress_percent': 50.0, 'days_since_start': 14}

# Complete tasks
tasks = agent._onboarding_manager.get_all_tasks("cust_001")
agent.complete_onboarding_task("cust_001", tasks[0].task_id, "Kickoff done")

# Check overdue
overdue = agent._onboarding_manager.get_overdue_tasks()

# Get velocity report
velocity = agent._onboarding_manager.get_velocity_report("cust_001")
# {'avg_days_per_stage': 7.5, 'total_days': 45, 'stages_completed': 4}

# Reassign task
agent._onboarding_manager.reassign_task(task_id, "cust_001", "new_csm_id")

# Get tasks by stage
setup_tasks = agent._onboarding_manager.get_tasks_by_stage("cust_001", OnboardingStage.SETUP)
```

### Health Scoring

```python
# Record metrics
agent.record_health_metric("cust_001", "product_usage", 85)
agent.record_health_metric("cust_001", "engagement", 70)
agent.record_health_metric("cust_001", "support_tickets", 60)
agent.record_health_metric("cust_001", "nps_score", 90)
agent.record_health_metric("cust_001", "payment_health", 95)
agent.record_health_metric("cust_001", "relationship", 80)

# Get comprehensive health report
health = agent.get_health_score("cust_001")
# {'health_score': 78.5, 'health_status': 'HEALTHY', 'metrics': {...}}

# Health distribution across all customers
dist = agent.get_health_distribution()
# {'CRITICAL': 2, 'POOR': 5, 'AT_RISK': 12, 'STABLE': 45, 'HEALTHY': 80, 'EXCELLENT': 30}

# Get health trend
trend = agent._health_scorer.get_health_trend("cust_001", days=30)
# {'trend': 'improving', 'change': 5.2}

# Find top risk customers
risks = agent._health_scorer.get_top_risk_customers(limit=10)

# Custom weights
agent._health_scorer.set_weight("product_usage", 0.40)
```

### Expansion Revenue

```python
# Identify opportunities
agent.identify_expansion("cust_001", ExpansionType.UPGRADE,
                         "Ready for enterprise plan", 24000)

agent.identify_expansion("cust_001", ExpansionType.ADD_ON,
                         "Analytics module interest", 5000)

# Track pipeline
pipeline = agent.get_expansion_pipeline()
# {'pipeline_value': 22500.0, 'closed_value': 0, 'identified_count': 2}

# By type breakdown
by_type = agent._expansion_manager.get_expansion_by_type()

# Win rate analytics
win_rate = agent._expansion_manager.get_win_rate()
# {'win_rate': 66.7, 'total_deals': 12, 'avg_deal_size': 18000, 'total_revenue': 216000}

# Close an opportunity
agent._expansion_manager.close_opportunity(opp_id, 24000)
```

### QBR Management

```python
# Schedule QBR
qbr = agent.schedule_qbr("cust_001", "Q1-2024", datetime(2024, 3, 15))

# Complete QBR
agent.complete_qbr(qbr["qbr_id"],
                   metrics={"health_score": 78, "nps": 42, "usage": "high"},
                   action_items=[{"action": "Schedule follow-up", "owner": "CSM"}])

# Get upcoming
upcoming = agent.get_upcoming_qbrs(30)

# Get completion rate
rate = agent._qbr_manager.get_qbr_completion_rate()
# {'total': 24, 'completed': 20, 'cancelled': 2, 'completion_rate': 83.3}

# Find overdue QBRs
overdue = agent._qbr_manager.get_overdue_qbrs()

# Get customer QBR history
history = agent._qbr_manager.get_customer_qbrs("cust_001")
```

### Advocacy Programs

```python
# Create advocacy entries
agent.create_advocacy_entry("cust_001", AdvocacyType.CASE_STUDY,
                            "Published: Acme 3x ROI story")

agent.create_advocacy_entry("cust_001", AdvocacyType.REFERRAL,
                            "Referred BetaCorp")

# Generate referral code
ref = agent.generate_referral_code("cust_001")
# {'referral_code': 'REF_cust_001_A1B2C3'}

# View stats
stats = agent.get_advocacy_stats()

# Find top advocates
top = agent._advocacy_manager.get_top_advocates(limit=5)
```

### Success Plans

```python
# Create plan with goals
plan = agent.create_success_plan("cust_001", "Q1 Growth Plan",
    goals=[{"objective": "Increase feature adoption", "target": "80%"}])

# Activate
agent.activate_success_plan(plan["plan_id"])

# Track
progress = agent.get_success_plan_progress(plan["plan_id"])
# {'completion_rate': 25.0, 'status': 'ACTIVE'}

# Find at-risk plans
at_risk = agent._success_plan_manager.get_at_risk_plans()

# Add goals dynamically
agent._success_plan_manager.add_goal(plan_id, "Improve NPS", "target: 50+")

# Add milestones
agent._success_plan_manager.add_milestone(plan_id, "Complete integration", datetime(2024, 6, 1))
```

### Usage Tracking

```python
# Record usage data
agent.record_usage("cust_001",
    logins_30d=45, active_users=8,
    features_used=12, total_features=20,
    avg_session_minutes=15.5, integrations_active=3,
    api_calls=1500)

# Get report
report = agent.get_usage_report("cust_001")
# {'logins_30d': 45, 'feature_adoption': '12/20', 'adoption_score': 65.0}

# Get usage trend
trend = agent._usage_tracker.get_usage_trend("cust_001")
# {'trend': 'growing', 'change_percent': 15.0}

# Find low usage customers
low = agent._usage_tracker.get_low_usage_customers(threshold=20.0)
```

### Renewal Tracking

```python
# Create renewal record
renewal = agent.create_renewal("cust_001", 24000.0, renewal_date=datetime(2024, 12, 1))

# Get upcoming renewals
upcoming = agent.get_upcoming_renewals(days=90)

# Get at-risk renewals
at_risk = agent._renewal_tracker.get_at_risk_renewals()

# Get summary
summary = agent._renewal_tracker.get_renewal_summary()
# {'total_renewals': 50, 'total_value': 1200000, 'at_risk_value': 180000}

# Update risk score
agent._renewal_tracker.update_risk_score(renewal_id, 0.65)
```

### Risk Assessment

```python
# Assess risk
assessment = agent.assess_risk("cust_001", "churn_risk",
                                factors=["low_usage", "missed_qbr"])

# Get customer risks
risks = agent._risk_assessment.get_customer_risks("cust_001")

# Get high-risk customers
high_risk = agent._risk_assessment.get_high_risk_customers()

# Get summary
summary = agent._risk_assessment.get_risk_summary()
```

### Milestone Tracking

```python
# Create milestone
milestone = agent.create_milestone("cust_001", MilestoneType.PRODUCT,
                                    "First API Integration",
                                    target_date=datetime(2024, 3, 1))

# Get progress
progress = agent.get_milestone_progress("cust_001")
# {'total': 12, 'achieved': 8, 'overdue': 1, 'completion_rate': 66.7}

# Get upcoming milestones
upcoming = agent._milestone_tracker.get_upcoming_milestones(days=30)

# Achieve milestone
agent._milestone_tracker.achieve_milestone(milestone_id)
```

### Value Realization

```python
# Record value
value = agent.record_value("cust_001", ValueStage.CORE_VALUE,
                            realized=15000, potential=24000)

# Get progress
progress = agent.get_value_progress("cust_001")
# {'stage': 'CORE_VALUE', 'realized_value': 15000, 'realization_rate': 62.5}

# Get summary
summary = agent._value_realization.get_value_summary()
```

### CSM Workload

```python
# Assign task
task = agent.assign_csm_task("csm_001", "cust_001", "check_in", priority="high")

# Get workload
workload = agent.get_csm_workload("csm_001")
# {'pending_tasks': 8, 'total_estimated_minutes': 360, 'customers_served': 5}

# Get balanced assignment
recommendation = agent._csm_workload.get_balanced_assignment()
# {'recommended_csm': 'csm_002', 'current_minutes': 120}
```

### Customer Feedback

```python
# Record feedback
feedback = agent.record_feedback("cust_001", FeedbackSource.NPS, 9.0, "Great product")

# Get sentiment summary
summary = agent.get_feedback_summary("cust_001")
# {'total': 15, 'avg_rating': 7.8, 'positive': 10, 'negative': 2, 'neutral': 3}

# Get NPS score
nps = agent._feedback_manager.get_nps_score()
# {'nps_score': 53.3, 'promoters': 8, 'detractors': 2, 'total': 15}

# Get negative feedback
negatives = agent._feedback_manager.get_negative_feedback()
```

### Adoption Journey

```python
# Record adoption phase
adoption = agent.record_adoption("cust_001", AdoptionPhase.DEEP_ADOPTION, 78.0)

# Get phase
phase = agent.get_adoption_phase("cust_001")
# {'phase': 'DEEP_ADOPTION', 'adoption_score': 78.0, 'blockers': []}

# Get journey progress
journey = agent._adoption_tracker.get_journey_progress("cust_001")
# {'phases_completed': ['AWARENESS', 'EXPLORATION', 'REGULAR_USE', 'DEEP_ADOPTION']}

# Get distribution
dist = agent._adoption_tracker.get_adoption_distribution()

# Get blocked customers
blocked = agent._adoption_tracker.get_blocked_customers()
```

## API Reference

### Core Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `add_customer()` | id, name, company, plan, mrr | Dict | Add customer |
| `initialize()` | - | Dict | Initialize agent |
| `shutdown()` | - | Dict | Shutdown agent |
| `get_status()` | - | Dict | Agent status |
| `get_full_report()` | - | Dict | Full report |

### Onboarding Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `start_onboarding()` | customer_id | Dict | Start onboarding |
| `complete_onboarding_task()` | customer_id, task_id, notes | Dict | Complete task |
| `get_onboarding_progress()` | customer_id | Dict | Get progress |

### Health Scoring Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `record_health_metric()` | customer_id, type, value | Dict | Record metric |
| `get_health_score()` | customer_id | Dict | Get health |
| `get_health_distribution()` | - | Dict | Distribution |

### Expansion Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `identify_expansion()` | customer_id, type, desc, value | Dict | Identify opp |
| `get_expansion_pipeline()` | - | Dict | Pipeline value |

### QBR Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `schedule_qbr()` | customer_id, quarter, date | Dict | Schedule QBR |
| `complete_qbr()` | qbr_id, metrics, actions | Dict | Complete QBR |
| `get_upcoming_qbrs()` | days | List | Upcoming QBRs |

### Advocacy Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `create_advocacy_entry()` | customer_id, type, desc | Dict | Create entry |
| `generate_referral_code()` | customer_id | Dict | Get code |
| `get_advocacy_stats()` | - | Dict | Stats |

### Success Plan Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `create_success_plan()` | customer_id, name, goals | Dict | Create plan |
| `activate_success_plan()` | plan_id | Dict | Activate |
| `get_success_plan_progress()` | plan_id | Dict | Progress |

### Usage Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `record_usage()` | customer_id, **metrics | Dict | Record usage |
| `get_usage_report()` | customer_id | Dict | Usage report |

### Renewal Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `create_renewal()` | customer_id, value, date | Dict | Create renewal |
| `get_upcoming_renewals()` | days | List | Upcoming renewals |

### Risk Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `assess_risk()` | customer_id, type, factors | Dict | Assess risk |

### Milestone Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `create_milestone()` | customer_id, type, name, date | Dict | Create milestone |
| `get_milestone_progress()` | customer_id | Dict | Progress |

### Value Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `record_value()` | customer_id, stage, realized, potential | Dict | Record value |
| `get_value_progress()` | customer_id | Dict | Progress |

### Workload Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `assign_csm_task()` | csm_id, customer_id, type, priority | Dict | Assign task |
| `get_csm_workload()` | csm_id | Dict | Workload |

### Feedback Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `record_feedback()` | customer_id, source, rating, comment | Dict | Record feedback |
| `get_feedback_summary()` | customer_id | Dict | Sentiment summary |

### Adoption Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `record_adoption()` | customer_id, phase, score | Dict | Record phase |
| `get_adoption_phase()` | customer_id | Dict | Current phase |

## Configuration

```yaml
agent:
  health_score_threshold: 50.0
  qbr_frequency_months: 3
  auto_intervention_enabled: true
  renewal_warning_days: 90
  max_csm_workload_minutes: 2400
  feedback_follow_up_days: 7

health_weights:
  product_usage: 0.30
  engagement: 0.20
  support_tickets: 0.15
  nps_score: 0.15
  payment_health: 0.10
  relationship: 0.10

renewal_risk_thresholds:
  NONE: [0.0, 0.1]
  LOW: [0.1, 0.3]
  MEDIUM: [0.3, 0.5]
  HIGH: [0.5, 0.75]
  CRITICAL: [0.75, 1.0]

adoption_phases:
  AWARENESS: [0, 15]
  EXPLORATION: [15, 30]
  FIRST_VALUE: [30, 50]
  REGULAR_USE: [50, 70]
  DEEP_ADOPTION: [70, 85]
  CHAMPION: [85, 100]

onboarding_milestones:
  - stage: KICKOFF
    name: "Kickoff Meeting"
    days: 0
  - stage: SETUP
    name: "Account Setup"
    days: 3
  - stage: TRAINING
    name: "Training Complete"
    days: 14
  - stage: GO_LIVE
    name: "Go Live"
    days: 30
  - stage: ADOPTION
    name: "Full Adoption"
    days: 60
  - stage: COMPLETED
    name: "Onboarding Complete"
    days: 90
```

## Best Practices

### Onboarding
1. Start with a clear kickoff meeting
2. Set expectations for each milestone
3. Track progress and address delays
4. Celebrate go-live achievements
5. Monitor velocity to identify bottlenecks
6. Reassign tasks when team capacity changes
7. Review overdue tasks weekly

### Health Scoring
1. Update metrics at least monthly
2. Focus on actionable metric categories
3. Set alerts for score drops
4. Review weights quarterly
5. Analyze trends over 30-day windows
6. Identify top risk customers proactively
7. Use health distribution for portfolio management

### Expansion
1. Identify opportunities during QBRs
2. Track probability and value
3. Document close reasons
4. Report pipeline monthly
5. Calculate win rates by type
6. Focus on highest-probability deals
7. Link expansion to health score improvements

### QBRs
1. Prepare metrics in advance
2. Share agenda beforehand
3. Document action items with owners
4. Follow up within 1 week
5. Track completion rates
6. Flag overdue QBRs immediately
7. Review customer QBR history before meetings

### Renewals
1. Create renewal records early (90+ days out)
2. Calculate risk scores based on health and usage
3. Flag at-risk renewals for immediate action
4. Review renewal summary weekly
5. Link renewal risk to expansion opportunities
6. Monitor upcoming renewals by value

### Risk Assessment
1. Assess risks regularly, not just reactively
2. Document factors and mitigation actions
3. Review high-risk customers in team meetings
4. Track risk level changes over time
5. Use risk data to prioritize interventions
6. Group risks by type for pattern analysis

### Milestones
1. Create milestones for all customer types
2. Set realistic target dates
3. Mark milestones achieved promptly
4. Review overdue milestones weekly
5. Use milestone progress in QBRs
6. Track milestones across all types

### Value Realization
1. Record value stages at key checkpoints
2. Track realized vs potential value
3. Use realization rate to demonstrate ROI
4. Share value progress in QBRs
5. Identify customers stuck at partial value
6. Review value summary monthly

### CSM Workload
1. Assign tasks with priority levels
2. Monitor total workload per CSM
3. Use balanced assignment to distribute work
4. Track completion rates by CSM
5. Adjust workload before burnout occurs
6. Review workload distribution weekly

### Customer Feedback
1. Collect feedback from multiple sources
2. Classify sentiment automatically
3. Calculate NPS regularly
4. Follow up on negative feedback within 7 days
5. Track feedback trends over time
6. Use negative feedback for process improvement

### Adoption Journey
1. Record adoption phases at key milestones
2. Identify blockers early
3. Track phase progression over time
4. Use distribution data to spot patterns
5. Focus intervention on blocked customers
6. Review adoption distribution in team meetings

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Health score always 50.0 | No metrics recorded | Call `record_health_metric()` for each dimension |
| Onboarding shows 0% | No tasks created | Call `start_onboarding()` first |
| Adoption score is 0.0 | No usage data | Call `record_usage()` with metrics |
| Renewal risk always NONE | Risk score not updated | Call `_renewal_tracker.update_risk_score()` |
| Feedback sentiment always neutral | Ratings out of range | Use 0-10 scale for ratings |
| CSM workload shows 0 | No tasks assigned | Call `assign_csm_task()` |
| Value rate is 0% | No value entries | Call `record_value()` with non-zero potential |
| Milestone progress 0% | Not marked achieved | Call `_milestone_tracker.achieve_milestone()` |
| NPS always 0 | No NPS feedback | Record feedback with `FeedbackSource.NPS` |
| Top risk customers empty | No health metrics | Record metrics for customers first |
| Win rate 0% | No closed opportunities | Close some with `close_opportunity()` |
| Adoption distribution all zero | No adoption entries | Call `record_adoption()` for customers |
| CSM balanced assignment empty | No workload entries | Assign tasks with `assign_csm_task()` first |
| Upcoming renewals empty | No future renewals | Create renewals with future `renewal_date` |
| QBR completion rate 0% | No completed QBRs | Complete QBRs with `complete_qbr()` |

## Examples

### Full Customer Lifecycle

```python
from agents.customer_success.agent import (
    CustomerSuccessAgent, Config, CustomerHealth, OnboardingStage,
    ExpansionType, AdvocacyType, ValueStage, AdoptionPhase, FeedbackSource
)

agent = CustomerSuccessAgent(Config())
agent.initialize()

# 1. Add customer
agent.add_customer("cust_001", name="Acme Corp", company="Acme Inc",
                   plan="professional", mrr=2000, csm="csm_001")

# 2. Start onboarding
agent.start_onboarding("cust_001")
tasks = agent._onboarding_manager.get_all_tasks("cust_001")
for task in tasks:
    agent.complete_onboarding_task("cust_001", task.task_id)

# 3. Record health metrics
agent.record_health_metric("cust_001", "product_usage", 85)
agent.record_health_metric("cust_001", "engagement", 75)
agent.record_health_metric("cust_001", "support_tickets", 70)
agent.record_health_metric("cust_001", "nps_score", 90)
agent.record_health_metric("cust_001", "payment_health", 95)
agent.record_health_metric("cust_001", "relationship", 80)

# 4. Track usage
agent.record_usage("cust_001", logins_30d=45, active_users=8,
                   features_used=12, total_features=20)

# 5. Record adoption phase
agent.record_adoption("cust_001", AdoptionPhase.DEEP_ADOPTION, 78.0)

# 6. Identify expansion opportunity
agent.identify_expansion("cust_001", ExpansionType.UPGRADE,
                         "Ready for enterprise plan", 24000)

# 7. Schedule QBR
qbr = agent.schedule_qbr("cust_001", "Q1-2024", datetime(2024, 3, 15))

# 8. Create success plan
plan = agent.create_success_plan("cust_001", "Q1 Growth Plan",
    goals=[{"objective": "Increase adoption", "target": "90%"}])
agent.activate_success_plan(plan["plan_id"])

# 9. Track renewal
agent.create_renewal("cust_001", 24000.0, renewal_date=datetime(2024, 12, 1))

# 10. Record feedback
agent.record_feedback("cust_001", FeedbackSource.NPS, 9.0, "Excellent product")

# 11. Record value realization
agent.record_value("cust_001", ValueStage.FULL_VALUE, realized=20000, potential=24000)

# 12. Get full report
report = agent.get_full_report()
print(report)
```

### Bulk Customer Processing

```python
import random

agent = CustomerSuccessAgent(Config())
agent.initialize()

# Add 100 customers
for i in range(100):
    agent.add_customer(f"cust_{i:03d}", name=f"Customer {i}",
                       company=f"Company {i}", plan="professional",
                       mrr=random.uniform(500, 5000))

# Health distribution analysis
for cid in [f"cust_{i:03d}" for i in range(100)]:
    agent.record_health_metric(cid, "product_usage", random.uniform(30, 100))
    agent.record_health_metric(cid, "engagement", random.uniform(20, 100))

dist = agent.get_health_distribution()
print(f"Health Distribution: {dist}")

# Find at-risk customers
at_risk = agent._health_scorer.get_customers_by_health(CustomerHealth.AT_RISK)
print(f"At-risk customers: {len(at_risk)}")

# Get top risk
top_risk = agent._health_scorer.get_top_risk_customers(limit=5)
for r in top_risk:
    print(f"  {r['customer_id']}: {r['health_score']} ({r['status']})")
```

### CSM Workload Balancing

```python
agent = CustomerSuccessAgent(Config())
agent.initialize()

# Assign tasks to CSMs
csms = ["csm_001", "csm_002", "csm_003"]
for i, cid in enumerate([f"cust_{j:03d}" for j in range(20)]):
    csm = csms[i % 3]
    agent.assign_csm_task(csm, cid, "check_in", priority="normal")

# Check workloads
for csm in csms:
    workload = agent.get_csm_workload(csm)
    print(f"{csm}: {workload['pending_tasks']} tasks, {workload['total_estimated_minutes']} min")

# Get balanced assignment
rec = agent._csm_workload.get_balanced_assignment()
print(f"Next task should go to: {rec['recommended_csm']}")
```

### NPS Analysis

```python
agent = CustomerSuccessAgent(Config())
agent.initialize()

# Record NPS responses
responses = [
    ("cust_001", 9, "Great product"),
    ("cust_002", 10, "Love it"),
    ("cust_003", 3, "Poor support"),
    ("cust_004", 8, "Good value"),
    ("cust_005", 2, "Too expensive"),
]

for cid, score, comment in responses:
    agent.record_feedback(cid, FeedbackSource.NPS, score, comment)

# Get NPS
nps = agent._feedback_manager.get_nps_score()
print(f"NPS: {nps['nps_score']}")
print(f"Promoters: {nps['promoters']}, Detractors: {nps['detractors']}")

# Get negative feedback for follow-up
negatives = agent._feedback_manager.get_negative_feedback()
for n in negatives:
    print(f"  {n['customer_id']}: {n['rating']} - {n['comment']}")
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation including:

- System architecture diagrams
- Component deep dives
- Data flow diagrams
- Design patterns
- Thread safety model
- Performance targets
- Configuration reference
- Error handling hierarchy
- Data storage model

## Agent Identity

See [GROK.md](GROK.md) for agent identity documentation including:

- Core principles
- Capabilities with code examples
- Method signatures reference
- Data models
- Enums reference
- Checklists
- Troubleshooting guide
- Error handling patterns
- Thread safety details
- Performance characteristics
- Integration patterns
- Deployment considerations

## Data Models Reference

### Core Models

```python
# Customer - the central entity
@dataclass
class Customer:
    customer_id: str
    name: str = ""
    company: str = ""
    plan: str = "starter"
    mrr: float = 0.0
    arr: float = 0.0
    health_score: float = 50.0
    health_status: CustomerHealth = CustomerHealth.STABLE
    onboarding_stage: OnboardingStage = OnboardingStage.NOT_STARTED
    csm_assigned: str = ""
    renewal_date: Optional[datetime] = None
    segment: str = "standard"
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
```

### Health and Usage Models

```python
# HealthMetric - individual health dimension
@dataclass
class HealthMetric:
    customer_id: str
    metric_type: str
    value: float
    weight: float = 0.0
    calculated_at: datetime = field(default_factory=datetime.now)
    trend: str = "stable"
    details: Dict[str, Any] = field(default_factory=dict)

# UsageMetrics - product usage snapshot
@dataclass
class UsageMetrics:
    customer_id: str
    logins_30d: int = 0
    active_users: int = 0
    features_used: int = 0
    total_features: int = 0
    avg_session_minutes: float = 0.0
    tasks_completed: int = 0
    integrations_active: int = 0
    api_calls: int = 0
    last_calculated: datetime = field(default_factory=datetime.now)
```

### Lifecycle Models

```python
# OnboardingTask - individual onboarding task
@dataclass
class OnboardingTask:
    task_id: str
    customer_id: str
    stage: OnboardingStage
    name: str
    description: str = ""
    assignee: str = ""
    due_date: Optional[datetime] = None
    completed: bool = False
    completed_at: Optional[datetime] = None
    notes: str = ""

# SuccessPlan - customer success plan
@dataclass
class SuccessPlan:
    plan_id: str
    customer_id: str
    name: str
    goals: List[Dict[str, Any]] = field(default_factory=list)
    milestones: List[Dict[str, Any]] = field(default_factory=list)
    status: SuccessPlanStatus = SuccessPlanStatus.DRAFT
    owner: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    target_date: Optional[datetime] = None
```

### Revenue Models

```python
# ExpansionOpportunity - upsell/cross-sell opportunity
@dataclass
class ExpansionOpportunity:
    opportunity_id: str
    customer_id: str
    expansion_type: ExpansionType
    description: str = ""
    estimated_value: float = 0.0
    probability: float = 0.0
    status: str = "identified"
    identified_at: datetime = field(default_factory=datetime.now)
    closed_at: Optional[datetime] = None
    closed_value: float = 0.0

# RenewalRecord - contract renewal tracking
@dataclass
class RenewalRecord:
    renewal_id: str
    customer_id: str
    current_value: float = 0.0
    proposed_value: float = 0.0
    renewal_date: Optional[datetime] = None
    risk_score: float = 0.0
    risk_level: RenewalRisk = RenewalRisk.NONE
    status: str = "pending"
    notes: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
```

### Risk and Assessment Models

```python
# RiskAssessmentEntry - risk evaluation
@dataclass
class RiskAssessmentEntry:
    assessment_id: str
    customer_id: str
    risk_type: str = ""
    risk_level: RiskLevel = RiskLevel.NONE
    risk_score: float = 0.0
    factors: List[str] = field(default_factory=list)
    mitigation_actions: List[str] = field(default_factory=list)
    assessed_at: datetime = field(default_factory=datetime.now)
    reviewed: bool = False

# MilestoneRecord - customer milestone
@dataclass
class MilestoneRecord:
    milestone_id: str
    customer_id: str
    milestone_type: MilestoneType
    name: str
    description: str = ""
    target_date: Optional[datetime] = None
    achieved: bool = False
    achieved_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
```

### Value and Adoption Models

```python
# ValueEntry - value realization tracking
@dataclass
class ValueEntry:
    entry_id: str
    customer_id: str
    value_stage: ValueStage = ValueStage.NOT_STARTED
    realized_value: float = 0.0
    potential_value: float = 0.0
    metrics: Dict[str, Any] = field(default_factory=dict)
    recorded_at: datetime = field(default_factory=datetime.now)
    notes: str = ""

# AdoptionEntry - adoption journey tracking
@dataclass
class AdoptionEntry:
    entry_id: str
    customer_id: str
    phase: AdoptionPhase = AdoptionPhase.AWARENESS
    adoption_score: float = 0.0
    key_actions_completed: List[str] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)
    recorded_at: datetime = field(default_factory=datetime.now)
```

### Feedback and Workload Models

```python
# FeedbackRecord - customer feedback
@dataclass
class FeedbackRecord:
    feedback_id: str
    customer_id: str
    source: FeedbackSource = FeedbackSource.DIRECT_CONVERSATION
    rating: float = 0.0
    comment: str = ""
    tags: List[str] = field(default_factory=list)
    sentiment: str = "neutral"
    created_at: datetime = field(default_factory=datetime.now)
    follow_up_needed: bool = False

# WorkloadEntry - CSM workload tracking
@dataclass
class WorkloadEntry:
    entry_id: str
    csm_id: str
    customer_id: str
    task_type: str = ""
    priority: str = "normal"
    estimated_minutes: int = 0
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
```

## Health Score Calculation

The health score is calculated as a weighted average across 6 dimensions:

```
Score = Σ(metric_value × weight) / Σ(weights)

Where:
- product_usage: 30% weight
- engagement: 20% weight
- support_tickets: 15% weight
- nps_score: 15% weight
- payment_health: 10% weight
- relationship: 10% weight

Health Status Thresholds:
- CRITICAL: 0-20
- POOR: 20-40
- AT_RISK: 40-55
- STABLE: 55-70
- HEALTHY: 70-85
- EXCELLENT: 85-100
```

## Adoption Phase Thresholds

```
Phase Score Ranges:
- AWARENESS: 0-15%
- EXPLORATION: 15-30%
- FIRST_VALUE: 30-50%
- REGULAR_USE: 50-70%
- DEEP_ADOPTION: 70-85%
- CHAMPION: 85-100%
```

## Renewal Risk Thresholds

```
Risk Level Score Ranges:
- NONE: 0.0-0.1
- LOW: 0.1-0.3
- MEDIUM: 0.3-0.5
- HIGH: 0.5-0.75
- CRITICAL: 0.75-1.0
```

## NPS Calculation

```
NPS = (Promoters - Detractors) / Total × 100

Where:
- Promoters: rating >= 9
- Passives: rating 7-8
- Detractors: rating <= 6

NPS Score Interpretation:
- 70+: World-class
- 50-69: Excellent
- 30-49: Good
- 0-29: Needs improvement
- Below 0: Critical
```

## Thread Safety

The agent uses a per-manager locking strategy:

- Each of the 14 subsystems owns its own `threading.Lock()`
- Lock scope is limited to internal data structures
- No cross-manager locking required
- Copy-on-read pattern for safe data retrieval
- Atomic updates within lock scope

This design prevents deadlocks and allows parallel operations across independent subsystems.

## Performance Targets

| Operation | Target Latency |
|-----------|---------------|
| Health Score Calc | < 50ms |
| Onboarding Progress | < 100ms |
| Expansion Pipeline | < 200ms |
| Usage Adoption Score | < 100ms |
| Renewal Summary | < 150ms |
| Risk Assessment | < 100ms |
| Milestone Progress | < 100ms |
| Value Summary | < 150ms |
| CSM Workload | < 100ms |
| Feedback Sentiment | < 100ms |
| Adoption Distribution | < 100ms |
| Full Report | < 500ms |

## Error Handling

```python
# The agent uses a hierarchy of exceptions:
#
# CustomerSuccessError (base)
# ├── OnboardingError
# ├── HealthScoreError
# ├── QBRError
# ├── RenewalError
# ├── RiskAssessmentError
# ├── WorkloadError
# ├── FeedbackError
# ├── AdoptionError
# └── ValueRealizationError
#
# All public methods return Dict with status information
# Errors are logged with context for debugging
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Development Setup

```bash
# Clone the repository
git clone <repository-url>

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Run the demo
python -m agents.customer_success.agent
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all public methods
- Add docstrings for new classes and methods
- Keep methods focused and under 50 lines
- Use meaningful variable and method names

## License

MIT License - see LICENSE file for details.
