---
name: Customer Success Agent
version: "3.0.0"
description: "Customer onboarding, health scoring, expansion revenue, QBR processes, advocacy programs, success plan management, renewal tracking, risk assessment, milestone management, value realization, workload management, feedback collection, and adoption journey tracking"
author: "MiMoCode"
tags:
  - customer-success
  - onboarding
  - health-score
  - expansion
  - qbr
  - advocacy
  - success-plans
  - renewal-tracking
  - risk-assessment
  - adoption-journey
  - value-realization
  - feedback
category: "agents"
personality: "customer-success-manager"
use_cases:
  - "Manage customer onboarding workflows"
  - "Calculate and track customer health scores"
  - "Identify and track expansion revenue opportunities"
  - "Schedule and execute Quarterly Business Reviews"
  - "Run customer advocacy and referral programs"
  - "Create and manage success plans"
  - "Track product usage and adoption metrics"
  - "Manage renewal lifecycle and risk"
  - "Assess customer risk factors"
  - "Track customer milestones"
  - "Measure value realization"
  - "Balance CSM workloads"
  - "Collect and analyze customer feedback"
  - "Map adoption journey phases"
---

# Customer Success Agent

## Agent Identity

You are a customer success expert with deep knowledge of onboarding optimization, health scoring methodologies, expansion revenue strategies, customer lifecycle management, renewal risk analysis, value realization measurement, and adoption journey mapping. You help businesses maximize customer value and retention through proactive success management.

## Core Principles

1. **Proactive Engagement**: Identify and address issues before they impact the customer
2. **Data-Driven Success**: Use metrics to guide every customer interaction
3. **Value Realization**: Ensure customers achieve their desired outcomes
4. **Revenue Expansion**: Grow customer accounts through demonstrated value
5. **Relationship Building**: Build trust through consistent, helpful engagement
6. **Risk Mitigation**: Identify and act on renewal and churn risks early
7. **Adoption Acceleration**: Move customers through adoption phases systematically

## Architecture Summary

The agent uses an orchestrator pattern with 14 independent subsystems:

```
CustomerSuccessAgent (Orchestrator)
├── Core Subsystems
│   ├── OnboardingManager
│   ├── HealthScorer
│   ├── ExpansionManager
│   ├── QBRManager
│   ├── AdvocacyManager
│   ├── SuccessPlanManager
│   ├── UsageTracker
│   └── InterventionEngine
└── Extension Subsystems
    ├── RenewalTracker
    ├── RiskAssessment
    ├── CustomerMilestoneTracker
    ├── ValueRealization
    ├── CSMWorkloadManager
    ├── CustomerFeedbackManager
    └── AdoptionJourneyTracker
```

Each subsystem owns its data and uses a threading.Lock for thread safety. The orchestrator coordinates cross-subsystem operations.

## Capabilities

### Customer Onboarding

```python
# Start onboarding - creates 6 milestone tasks
agent.start_onboarding("cust_001")
# Returns: {"customer_id": "cust_001", "tasks_created": 6, "stage": "KICKOFF"}

# Track progress
progress = agent.get_onboarding_progress("cust_001")
# Returns: {
#   "current_stage": "TRAINING",
#   "progress_percent": 50.0,
#   "tasks_total": 6,
#   "tasks_completed": 3,
#   "milestones_reached": ["KICKOFF", "SETUP", "TRAINING"],
#   "days_since_start": 14
# }

# Complete tasks
tasks = agent._onboarding_manager.get_all_tasks("cust_001")
agent.complete_onboarding_task("cust_001", tasks[0].task_id, "Kickoff done")

# Check overdue tasks
overdue = agent._onboarding_manager.get_overdue_tasks()
# Returns: list of OnboardingTask past due_date

# Get velocity report
velocity = agent._onboarding_manager.get_velocity_report("cust_001")
# Returns: {
#   "avg_days_per_stage": 7.5,
#   "stages_completed": 4,
#   "total_days": 45
# }

# Reassign task to different CSM
agent._onboarding_manager.reassign_task(task_id, "cust_001", "new_csm_id")

# Get tasks by specific stage
setup_tasks = agent._onboarding_manager.get_tasks_by_stage("cust_001", OnboardingStage.SETUP)
```

### Health Scoring

```python
# Record health metrics across 6 dimensions
agent.record_health_metric("cust_001", "product_usage", 85.0)
agent.record_health_metric("cust_001", "engagement", 70.0)
agent.record_health_metric("cust_001", "support_tickets", 60.0)
agent.record_health_metric("cust_001", "nps_score", 90.0)
agent.record_health_metric("cust_001", "payment_health", 95.0)
agent.record_health_metric("cust_001", "relationship", 80.0)

# Get comprehensive health report
health = agent.get_health_score("cust_001")
# Returns: {
#   "health_score": 78.5,
#   "health_status": "HEALTHY",
#   "metrics": {
#     "product_usage": {"value": 85.0, "weight": 0.30},
#     "engagement": {"value": 70.0, "weight": 0.20},
#     ...
#   },
#   "calculated_at": "2024-01-15T10:30:00"
# }

# Health distribution across all customers
dist = agent.get_health_distribution()
# Returns: {"CRITICAL": 2, "POOR": 5, "AT_RISK": 12, "STABLE": 45, "HEALTHY": 80, "EXCELLENT": 30}

# Get health trend over time
trend = agent._health_scorer.get_health_trend("cust_001", days=30)
# Returns: {"trend": "improving", "change": 5.2}

# Find top risk customers
risks = agent._health_scorer.get_top_risk_customers(limit=10)
# Returns: [{"customer_id": "cust_003", "health_score": 22.0, "status": "POOR"}, ...]

# Custom health weights
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
# Returns: {
#   "pipeline_value": 22500.0,
#   "closed_value": 0,
#   "identified_count": 2,
#   "closed_count": 0
# }

# By type breakdown
by_type = agent._expansion_manager.get_expansion_by_type()
# Returns: {"UPGRADE": {"count": 5, "value": 120000}, "ADD_ON": {"count": 3, "value": 15000}}

# Win rate analytics
win_rate = agent._expansion_manager.get_win_rate()
# Returns: {
#   "win_rate": 66.7,
#   "total_deals": 12,
#   "avg_deal_size": 18000,
#   "total_revenue": 216000
# }

# Close an opportunity
agent._expansion_manager.close_opportunity(opp_id, 24000)
```

### QBR Management

```python
# Schedule QBR
qbr = agent.schedule_qbr("cust_001", "Q1-2024", datetime(2024, 3, 15))
# Returns: {"qbr_id": "uuid", "quarter": "Q1-2024", "date": "2024-03-15T00:00:00"}

# Complete QBR
agent.complete_qbr(qbr["qbr_id"],
                   metrics={"health_score": 78, "nps": 42, "usage": "high"},
                   action_items=[{"action": "Schedule follow-up", "owner": "CSM"}])

# Get upcoming QBRs
upcoming = agent.get_upcoming_qbrs(30)

# Get completion rate
rate = agent._qbr_manager.get_qbr_completion_rate()
# Returns: {"total": 24, "completed": 20, "cancelled": 2, "completion_rate": 83.3}

# Find overdue QBRs
overdue = agent._qbr_manager.get_overdue_qbrs()
# Returns: list of QBRs past scheduled_date with SCHEDULED status

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
# Returns: {"referral_code": "REF_cust_001_A1B2C3"}

# View stats
stats = agent.get_advocacy_stats()
# Returns: {
#   "total_entries": 45,
#   "by_type": {
#     "CASE_STUDY": {"count": 10, "completed": 8, "value": 5000},
#     "REFERRAL": {"count": 20, "completed": 15, "value": 30000}
#   },
#   "total_referral_codes": 25
# }

# Find top advocates
top = agent._advocacy_manager.get_top_advocates(limit=5)
# Returns: [{"customer_id": "cust_001", "count": 5, "value": 12000}, ...]
```

### Success Plans

```python
# Create plan with goals
plan = agent.create_success_plan("cust_001", "Q1 Growth Plan",
    goals=[{"objective": "Increase feature adoption", "target": "80%"}])
# Returns: {"plan_id": "uuid", "name": "Q1 Growth Plan", "status": "DRAFT"}

# Activate
agent.activate_success_plan(plan["plan_id"])

# Track progress
progress = agent.get_success_plan_progress(plan["plan_id"])
# Returns: {"completion_rate": 25.0, "status": "ACTIVE"}

# Find at-risk plans
at_risk = agent._success_plan_manager.get_at_risk_plans()
# Returns: plans with < 50% completion

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
# Returns: {
#   "logins_30d": 45,
#   "active_users": 8,
#   "feature_adoption": "12/20",
#   "adoption_score": 65.0,
#   "integrations": 3,
#   "api_calls": 1500
# }

# Get usage trend
trend = agent._usage_tracker.get_usage_trend("cust_001")
# Returns: {"trend": "growing", "change_percent": 15.0}

# Find low usage customers
low = agent._usage_tracker.get_low_usage_customers(threshold=20.0)
# Returns: [{"customer_id": "cust_005", "adoption_score": 12.5}, ...]
```

### Renewal Tracking

```python
# Create renewal record
renewal = agent.create_renewal("cust_001", 24000.0, renewal_date=datetime(2024, 12, 1))
# Returns: {"renewal_id": "uuid", "customer_id": "cust_001"}

# Get upcoming renewals
upcoming = agent.get_upcoming_renewals(days=90)
# Returns: [{"renewal_id": "uuid", "customer_id": "cust_001", "renewal_date": "2024-12-01", "current_value": 24000}]

# Get at-risk renewals
at_risk = agent._renewal_tracker.get_at_risk_renewals()
# Returns: [{"renewal_id": "uuid", "customer_id": "cust_002", "risk_level": "HIGH", "risk_score": 0.65}]

# Get summary
summary = agent._renewal_tracker.get_renewal_summary()
# Returns: {"total_renewals": 50, "total_value": 1200000, "at_risk_value": 180000, "at_risk_count": 8}

# Update risk score
agent._renewal_tracker.update_risk_score(renewal_id, 0.65)
```

### Risk Assessment

```python
# Assess risk
assessment = agent.assess_risk("cust_001", "churn_risk",
                                factors=["low_usage", "missed_qbr", "executive_sponsor_departed"])
# Returns: {"assessment_id": "uuid", "customer_id": "cust_001"}

# Get customer risks
risks = agent._risk_assessment.get_customer_risks("cust_001")
# Returns: list of RiskAssessmentEntry

# Get high-risk customers
high_risk = agent._risk_assessment.get_high_risk_customers()
# Returns: [{"customer_id": "cust_001", "risk_count": 3, "risk_types": ["churn_risk", "expansion_risk"]}]

# Get summary
summary = agent._risk_assessment.get_risk_summary()
# Returns: {"total_assessments": 120, "by_level": {"NONE": 50, "LOW": 30, "MEDIUM": 25, "HIGH": 12, "CRITICAL": 3}}
```

### Milestone Tracking

```python
# Create milestone
milestone = agent.create_milestone("cust_001", MilestoneType.PRODUCT,
                                    "First API Integration",
                                    target_date=datetime(2024, 3, 1))
# Returns: {"milestone_id": "uuid", "name": "First API Integration"}

# Get progress
progress = agent.get_milestone_progress("cust_001")
# Returns: {"total": 12, "achieved": 8, "overdue": 1, "completion_rate": 66.7}

# Get upcoming milestones
upcoming = agent._milestone_tracker.get_upcoming_milestones(days=30)
# Returns: list of MilestoneRecord with target_date in next 30 days

# Achieve milestone
agent._milestone_tracker.achieve_milestone(milestone_id)
```

### Value Realization

```python
# Record value
value = agent.record_value("cust_001", ValueStage.CORE_VALUE,
                            realized=15000, potential=24000)
# Returns: {"entry_id": "uuid", "stage": "CORE_VALUE"}

# Get progress
progress = agent.get_value_progress("cust_001")
# Returns: {
#   "stage": "CORE_VALUE",
#   "realized_value": 15000,
#   "potential_value": 24000,
#   "realization_rate": 62.5
# }

# Get summary
summary = agent._value_realization.get_value_summary()
# Returns: {"total_customers": 100, "total_realized": 1500000, "total_potential": 2400000, "overall_rate": 62.5}
```

### CSM Workload Management

```python
# Assign task
task = agent.assign_csm_task("csm_001", "cust_001", "check_in", priority="high")
# Returns: {"entry_id": "uuid", "csm_id": "csm_001"}

# Get workload
workload = agent.get_csm_workload("csm_001")
# Returns: {
#   "pending_tasks": 8,
#   "total_estimated_minutes": 360,
#   "customers_served": 5
# }

# Get balanced assignment
recommendation = agent._csm_workload.get_balanced_assignment()
# Returns: {"recommended_csm": "csm_002", "current_minutes": 120}
```

### Customer Feedback

```python
# Record feedback
feedback = agent.record_feedback("cust_001", FeedbackSource.NPS, 9.0, "Great product")
# Returns: {"feedback_id": "uuid", "sentiment": "positive"}

# Get sentiment summary
summary = agent.get_feedback_summary("cust_001")
# Returns: {
#   "total": 15,
#   "avg_rating": 7.8,
#   "positive": 10,
#   "negative": 2,
#   "neutral": 3,
#   "follow_up_needed": 2
# }

# Get NPS score
nps = agent._feedback_manager.get_nps_score()
# Returns: {"nps_score": 53.3, "promoters": 8, "detractors": 2, "total": 15}

# Get negative feedback
negatives = agent._feedback_manager.get_negative_feedback()
# Returns: [{"customer_id": "cust_003", "rating": 2.0, "comment": "Poor support"}, ...]
```

### Adoption Journey

```python
# Record adoption phase
adoption = agent.record_adoption("cust_001", AdoptionPhase.DEEP_ADOPTION, 78.0)
# Returns: {"entry_id": "uuid", "phase": "DEEP_ADOPTION"}

# Get phase
phase = agent.get_adoption_phase("cust_001")
# Returns: {"phase": "DEEP_ADOPTION", "adoption_score": 78.0, "blockers": []}

# Get journey progress
journey = agent._adoption_tracker.get_journey_progress("cust_001")
# Returns: {
#   "phases_completed": ["AWARENESS", "EXPLORATION", "REGULAR_USE", "DEEP_ADOPTION"],
#   "current_phase": "DEEP_ADOPTION",
#   "total_records": 8
# }

# Get distribution
dist = agent._adoption_tracker.get_adoption_distribution()
# Returns: {"AWARENESS": 5, "EXPLORATION": 10, "FIRST_VALUE": 15, "REGULAR_USE": 30, "DEEP_ADOPTION": 25, "CHAMPION": 15}

# Get blocked customers
blocked = agent._adoption_tracker.get_blocked_customers()
# Returns: [{"customer_id": "cust_002", "blockers": ["integration_complexity", "team_resistance"]}]
```

## Method Signatures Reference

```python
# Customer Management
agent.add_customer(id: str, name: str, company: str, plan: str, mrr: float, **kwargs) -> Dict
agent.initialize() -> Dict
agent.shutdown() -> Dict

# Onboarding
agent.start_onboarding(customer_id: str) -> Dict
agent.complete_onboarding_task(customer_id: str, task_id: str, notes: str) -> Dict
agent.get_onboarding_progress(customer_id: str) -> Dict

# Health Scoring
agent.record_health_metric(customer_id: str, metric_type: str, value: float) -> Dict
agent.get_health_score(customer_id: str) -> Dict
agent.get_health_distribution() -> Dict

# Expansion
agent.identify_expansion(customer_id: str, type: ExpansionType, description: str, value: float) -> Dict
agent.get_expansion_pipeline() -> Dict

# QBR
agent.schedule_qbr(customer_id: str, quarter: str, date: datetime) -> Dict
agent.complete_qbr(qbr_id: str, metrics: Dict, action_items: List[Dict]) -> Dict
agent.get_upcoming_qbrs(days: int) -> List[Dict]

# Advocacy
agent.create_advocacy_entry(customer_id: str, type: AdvocacyType, description: str) -> Dict
agent.generate_referral_code(customer_id: str) -> Dict
agent.get_advocacy_stats() -> Dict

# Success Plans
agent.create_success_plan(customer_id: str, name: str, goals: List[Dict]) -> Dict
agent.activate_success_plan(plan_id: str) -> Dict
agent.get_success_plan_progress(plan_id: str) -> Dict

# Usage
agent.record_usage(customer_id: str, **metrics) -> Dict
agent.get_usage_report(customer_id: str) -> Dict

# Renewals
agent.create_renewal(customer_id: str, current_value: float, renewal_date: datetime) -> Dict
agent.get_upcoming_renewals(days: int) -> List[Dict]

# Risk Assessment
agent.assess_risk(customer_id: str, risk_type: str, factors: List[str]) -> Dict

# Milestones
agent.create_milestone(customer_id: str, type: MilestoneType, name: str, target_date: datetime) -> Dict
agent.get_milestone_progress(customer_id: str) -> Dict

# Value Realization
agent.record_value(customer_id: str, stage: ValueStage, realized: float, potential: float) -> Dict
agent.get_value_progress(customer_id: str) -> Dict

# CSM Workload
agent.assign_csm_task(csm_id: str, customer_id: str, task_type: str, priority: str) -> Dict
agent.get_csm_workload(csm_id: str) -> Dict

# Feedback
agent.record_feedback(customer_id: str, source: FeedbackSource, rating: float, comment: str) -> Dict
agent.get_feedback_summary(customer_id: str) -> Dict

# Adoption Journey
agent.record_adoption(customer_id: str, phase: AdoptionPhase, score: float) -> Dict
agent.get_adoption_phase(customer_id: str) -> Dict

# Reporting
agent.get_status() -> Dict
agent.get_full_report() -> Dict
```

## Data Models

### Customer
```python
@dataclass
class Customer:
    customer_id: str
    name: str = ""
    email: str = ""
    company: str = ""
    plan: str = "starter"
    mrr: float = 0.0
    arr: float = 0.0
    health_score: float = 50.0
    health_status: CustomerHealth = CustomerHealth.STABLE
    onboarding_stage: OnboardingStage = OnboardingStage.NOT_STARTED
    csm_assigned: str = ""
    contract_start: Optional[datetime] = None
    contract_end: Optional[datetime] = None
    renewal_date: Optional[datetime] = None
    segment: str = "standard"
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)
```

### RenewalRecord
```python
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

### AdoptionEntry
```python
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

### FeedbackRecord
```python
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
```

### ValueEntry
```python
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
```

### WorkloadEntry
```python
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

## Enums Reference

```python
class CustomerHealth(Enum):
    CRITICAL, POOR, AT_RISK, STABLE, HEALTHY, EXCELLENT

class OnboardingStage(Enum):
    NOT_STARTED, KICKOFF, SETUP, TRAINING, GO_LIVE, ADOPTION, COMPLETED

class ExpansionType(Enum):
    UPGRADE, CROSS_SELL, RENEWAL, ADD_ON, SEAT_EXPANSION, USAGE_BASED

class QBRStatus(Enum):
    SCHEDULED, IN_PROGRESS, COMPLETED, CANCELLED

class AdvocacyType(Enum):
    REFERRAL, CASE_STUDY, TESTIMONIAL, REVIEW, SPEAKING, COMMUNITY

class RiskLevel(Enum):
    NONE, LOW, MEDIUM, HIGH, CRITICAL

class SuccessPlanStatus(Enum):
    DRAFT, ACTIVE, ON_TRACK, AT_RISK, COMPLETED, ABANDONED

class InterventionType(Enum):
    CHECK_IN, TRAINING_SESSION, FEATURE_DEMO, ESCALATION,
    EXECUTIVE_SPONSOR, CUSTOM_SUCCESS_PLAN

class RenewalRisk(Enum):
    NONE, LOW, MEDIUM, HIGH, CRITICAL

class ValueStage(Enum):
    NOT_STARTED, INITIAL_ADOPTION, PARTIAL_VALUE,
    CORE_VALUE, FULL_VALUE, MAXIMUM_VALUE

class MilestoneType(Enum):
    ONBOARDING, SUCCESS_PLAN, PRODUCT, RELATIONSHIP, CONTRACT, ADVOCACY

class FeedbackSource(Enum):
    SURVEY, QBR, SUPPORT_TICKET, NPS, IN_PRODUCT,
    DIRECT_CONVERSATION, COMMUNITY

class AdoptionPhase(Enum):
    AWARENESS, EXPLORATION, FIRST_VALUE, REGULAR_USE,
    DEEP_ADOPTION, CHAMPION
```

## Checklists

### Onboarding Checklist
- [ ] Kickoff meeting scheduled
- [ ] Account configured
- [ ] Training sessions completed
- [ ] Key integrations connected
- [ ] Go-live milestone achieved
- [ ] Adoption metrics tracked
- [ ] Onboarding velocity reviewed
- [ ] Tasks reassigned as needed

### Health Review Checklist
- [ ] All metric categories updated
- [ ] Score calculated and verified
- [ ] Status classified correctly
- [ ] Trends analyzed (improving/declining/stable)
- [ ] Interventions planned for at-risk
- [ ] Top risk customers identified
- [ ] Health weights reviewed quarterly

### QBR Checklist
- [ ] Metrics prepared
- [ ] Attendees confirmed
- [ ] Agenda shared
- [ ] Action items documented
- [ ] Follow-ups scheduled
- [ ] Completion rate tracked
- [ ] Overdue QBRs flagged

### Renewal Checklist
- [ ] Renewal record created
- [ ] Risk score calculated
- [ ] At-risk renewals flagged
- [ ] Renewal summary reviewed
- [ ] Expansion opportunities identified
- [ ] 90-day warning triggered

### Adoption Journey Checklist
- [ ] Current phase recorded
- [ ] Adoption score calculated
- [ ] Blockers identified
- [ ] Key actions tracked
- [ ] Distribution reviewed
- [ ] Blocked customers prioritized

### Feedback Checklist
- [ ] Feedback collected from all sources
- [ ] Sentiment classified
- [ ] NPS calculated
- [ ] Negative feedback flagged for follow-up
- [ ] Trends analyzed
- [ ] Follow-ups scheduled within 7 days

### Value Realization Checklist
- [ ] Value stage recorded
- [ ] Realized vs potential tracked
- [ ] Realization rate calculated
- [ ] Summary reviewed
- [ ] Stagnant customers identified
- [ ] QBR progress shared

## Troubleshooting

### Health Score Returns 50.0
**Cause**: No metrics recorded for the customer.
**Fix**: Call `record_health_metric()` for each dimension before calculating.

### Onboarding Shows 0% Progress
**Cause**: No tasks created or all tasks already completed.
**Fix**: Call `start_onboarding()` first, or check if onboarding was already completed.

### Adoption Score Returns 0.0
**Cause**: No usage data recorded.
**Fix**: Call `record_usage()` with logins, active_users, and features_used.

### Renewal Risk Always NONE
**Cause**: Risk score not updated after creating renewal.
**Fix**: Call `_renewal_tracker.update_risk_score()` with appropriate risk factors.

### Feedback Sentiment Always Neutral
**Cause**: Ratings not in the expected range (0-10).
**Fix**: Ensure ratings are 0-10 scale. >= 7 is positive, <= 4 is negative.

### CSM Workload Shows 0 Minutes
**Cause**: No tasks assigned to the CSM.
**Fix**: Call `assign_csm_task()` to create workload entries.

### Value Realization Rate 0%
**Cause**: No value entries recorded or potential_value is 0.
**Fix**: Call `record_value()` with non-zero potential_value.

### Milestone Progress Shows 0% Achieved
**Cause**: Milestones created but not marked achieved.
**Fix**: Call `_milestone_tracker.achieve_milestone()` when milestones are reached.

### NPS Score Always 0
**Cause**: No NPS feedback entries recorded.
**Fix**: Record feedback with `FeedbackSource.NPS` source.

### Top Risk Customers Returns Empty
**Cause**: No health metrics recorded for any customers.
**Fix**: Record metrics for customers first, then query top risk.

### Win Rate Returns 0%
**Cause**: No closed opportunities (won or lost).
**Fix**: Close some opportunities with `close_opportunity()` first.

### Adoption Distribution All Zero
**Cause**: No adoption entries recorded.
**Fix**: Call `record_adoption()` for customers to populate distribution.

### CSM Balanced Assignment Returns Empty
**Cause**: No workload entries assigned to any CSM.
**Fix**: Assign tasks with `assign_csm_task()` first.

### Upcoming Renewals Returns Empty
**Cause**: No renewals with renewal_date in the future.
**Fix**: Create renewals with future `renewal_date` parameter.

### QBR Completion Rate Shows 0%
**Cause**: No QBRs completed or cancelled.
**Fix**: Complete QBRs with `complete_qbr()`.

## Error Handling

The agent uses a hierarchy of exceptions for error handling:

```
CustomerSuccessError (base)
├── OnboardingError
├── HealthScoreError
├── QBRError
├── RenewalError
├── RiskAssessmentError
├── WorkloadError
├── FeedbackError
├── AdoptionError
└── ValueRealizationError
```

All public methods are wrapped in try/except blocks. Errors are logged with context including the customer ID and operation being attempted. The base `CustomerSuccessError` exception can be used for catch-all error handling, while specific exceptions allow targeted recovery.

### Error Handling Strategy

- All public methods return Dict with status information
- Errors are logged using Python's logging module
- Specific exceptions for each subsystem
- Graceful degradation on subsystem failures
- Thread-safe error recording

## Thread Safety

The agent uses a per-manager locking strategy:

- Each of the 14 subsystems owns its own `threading.Lock()`
- Lock scope is limited to internal data structures
- No cross-manager locking required
- Copy-on-read pattern for safe data retrieval
- Atomic updates within lock scope

This design prevents deadlocks and allows parallel operations across independent subsystems.

## Performance Characteristics

| Operation | Complexity | Typical Latency |
|-----------|-----------|----------------|
| Health Score Calc | O(n) where n = metrics | < 50ms |
| Onboarding Progress | O(t) where t = tasks | < 100ms |
| Expansion Pipeline | O(o) where o = opportunities | < 200ms |
| Usage Adoption | O(1) | < 100ms |
| Renewal Summary | O(r) where r = renewals | < 150ms |
| Risk Assessment | O(a) where a = assessments | < 100ms |
| Milestone Progress | O(m) where m = milestones | < 100ms |
| Value Summary | O(v) where v = value entries | < 150ms |
| CSM Workload | O(w) where w = workload entries | < 100ms |
| Feedback Sentiment | O(f) where f = feedback entries | < 100ms |
| Adoption Distribution | O(j) where j = journey entries | < 100ms |
| Full Report | O(sum of all) | < 500ms |

All operations are O(n) in the size of their respective data structures. The in-memory storage model ensures fast lookups via dictionary-based registries.

## Integration Patterns

### With CRM Systems
```python
# Sync customer data from CRM
crm_data = fetch_from_crm("cust_001")
agent.add_customer(
    customer_id=crm_data["id"],
    name=crm_data["name"],
    company=crm_data["company"],
    plan=crm_data["plan"],
    mrr=crm_data["mrr"]
)

# Sync health metrics
for metric in crm_data["health_metrics"]:
    agent.record_health_metric("cust_001", metric["type"], metric["value"])
```

### With Support Systems
```python
# Import support ticket data
tickets = fetch_support_tickets("cust_001")
ticket_score = calculate_ticket_health(tickets)
agent.record_health_metric("cust_001", "support_tickets", ticket_score)
```

### With Product Analytics
```python
# Import product usage data
usage = fetch_product_usage("cust_001")
agent.record_usage(
    "cust_001",
    logins_30d=usage["logins"],
    active_users=usage["active_users"],
    features_used=usage["features_used"],
    total_features=usage["total_features"]
)

# Update adoption phase based on usage
if usage["adoption_score"] > 85:
    agent.record_adoption("cust_001", AdoptionPhase.CHAMPION, usage["adoption_score"])
elif usage["adoption_score"] > 70:
    agent.record_adoption("cust_001", AdoptionPhase.DEEP_ADOPTION, usage["adoption_score"])
```

### With NPS Survey Tools
```python
# Import NPS responses
nps_responses = fetch_nps_responses()
for response in nps_responses:
    agent.record_feedback(
        response["customer_id"],
        FeedbackSource.NPS,
        response["score"],
        response.get("comment", "")
    )

# Calculate NPS
nps = agent._feedback_manager.get_nps_score()
print(f"NPS Score: {nps['nps_score']}")
```

## Deployment Considerations

### In-Memory Storage
The agent stores all data in memory. For production use, consider:
- Regular checkpointing to persistent storage
- Backup and recovery procedures
- Memory usage monitoring for large customer bases

### Concurrency
The agent supports concurrent access via per-manager locking. For high-throughput scenarios:
- Monitor lock contention
- Consider sharding by customer segment
- Use connection pooling for external integrations

### Scalability
For large-scale deployments:
- Partition customers across agent instances
- Use message queues for async operations
- Implement caching layers for frequently accessed data

## Version History

### v3.0.0 (Current)
- Added renewal tracking and risk management
- Added customer milestone tracking
- Added value realization measurement
- Added CSM workload management
- Added customer feedback collection and NPS
- Added adoption journey tracking
- Expanded health scoring with trend analysis
- Expanded onboarding with velocity reports
- Expanded expansion management with win-rate analytics
- Added comprehensive error handling
- Added thread-safe operations

### v2.0.0
- Added health scoring with weighted metrics
- Added expansion revenue tracking
- Added QBR management
- Added advocacy programs
- Added success plans
- Added usage tracking

### v1.0.0
- Initial release with onboarding workflows
