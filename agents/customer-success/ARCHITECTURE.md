# Customer Success Agent Architecture

## Overview

The Customer Success Agent is a comprehensive customer success management platform covering onboarding workflows, health scoring, expansion revenue, QBR processes, advocacy programs, success plans, usage tracking, renewal management, risk assessment, milestone tracking, value realization, workload management, feedback collection, and adoption journey tracking. This document describes the complete system architecture, data flows, design patterns, thread safety model, and performance targets.

The agent is designed as an orchestrator pattern with 14 independent subsystems, each managing its own data and locking strategy. The orchestrator coordinates cross-subsystem operations while maintaining clean separation of concerns.

## System Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                        CustomerSuccessAgent (Orchestrator)                        │
│                                                                                  │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                           Core Subsystems                                  │  │
│  │                                                                            │  │
│  │  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────────┐       │  │
│  │  │  Onboarding  │  │  Health          │  │  Expansion           │       │  │
│  │  │  Manager     │  │  Scorer          │  │  Manager             │       │  │
│  │  └──────┬───────┘  └────────┬─────────┘  └──────────┬───────────┘       │  │
│  │         │                   │                        │                    │  │
│  │  ┌──────┴───────┐  ┌───────┴────────┐  ┌───────────┴──────────┐       │  │
│  │  │  Milestone   │  │  Weighted      │  │  Opportunity         │       │  │
│  │  │  Tracking    │  │  Scoring       │  │  Pipeline            │       │  │
│  │  └──────────────┘  └────────────────┘  └──────────────────────┘       │  │
│  │                                                                            │  │
│  │  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────────┐       │  │
│  │  │  QBR         │  │  Advocacy        │  │  Success Plan        │       │  │
│  │  │  Manager     │  │  Manager         │  │  Manager             │       │  │
│  │  └──────┬───────┘  └────────┬─────────┘  └──────────┬───────────┘       │  │
│  │         │                   │                        │                    │  │
│  │  ┌──────┴───────┐  ┌───────┴────────┐  ┌───────────┴──────────┐       │  │
│  │  │  Scheduling  │  │  Referral       │  │  Goal & Milestone    │       │  │
│  │  │  & Execution │  │  Codes          │  │  Tracking            │       │  │
│  │  └──────────────┘  └────────────────┘  └──────────────────────┘       │  │
│  │                                                                            │  │
│  │  ┌──────────────┐  ┌──────────────────────────────────────────────┐     │  │
│  │  │  Usage       │  │  Intervention Engine                          │     │  │
│  │  │  Tracker     │  │  Check-in, Training, Demo, Escalation        │     │  │
│  │  └──────────────┘  └──────────────────────────────────────────────┘     │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                  │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                        Extension Subsystems                                │  │
│  │                                                                            │  │
│  │  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────────┐       │  │
│  │  │  Renewal     │  │  Risk            │  │  Milestone           │       │  │
│  │  │  Tracker     │  │  Assessment      │  │  Tracker             │       │  │
│  │  └──────────────┘  └──────────────────┘  └──────────────────────┘       │  │
│  │                                                                            │  │
│  │  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────────┐       │  │
│  │  │  Value       │  │  CSM Workload    │  │  Feedback            │       │  │
│  │  │  Realization │  │  Manager         │  │  Manager             │       │  │
│  │  └──────────────┘  └──────────────────┘  └──────────────────────┘       │  │
│  │                                                                            │  │
│  │  ┌──────────────────────────────────────────────────────────────┐        │  │
│  │  │  Adoption Journey Tracker                                    │        │  │
│  │  │  Phase → Score → Blockers → Recommendations                 │        │  │
│  │  └──────────────────────────────────────────────────────────────┘        │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Component Deep Dives

### 1. Onboarding Manager

Manages the complete customer onboarding lifecycle from kickoff through full adoption with velocity tracking and task reassignment.

```
┌─────────────────────────────────────────────────────────┐
│              OnboardingManager                            │
│                                                          │
│  Onboarding Stages:                                     │
│  NOT_STARTED → KICKOFF → SETUP → TRAINING →             │
│  GO_LIVE → ADOPTION → COMPLETED                         │
│                                                          │
│  Milestones & Timelines:                                │
│  ┌──────────┬─────────────────────┬──────────┐         │
│  │ Day      │ Milestone           │ Stage    │         │
│  ├──────────┼─────────────────────┼──────────┤         │
│  │ 0        │ Kickoff Meeting     │ KICKOFF  │         │
│  │ 3        │ Account Setup       │ SETUP    │         │
│  │ 14       │ Training Complete   │ TRAINING │         │
│  │ 30       │ Go Live             │ GO_LIVE  │         │
│  │ 60       │ Full Adoption       │ ADOPTION │         │
│  │ 90       │ Onboarding Complete │ DONE     │         │
│  └──────────┴─────────────────────┴──────────┘         │
│                                                          │
│  Task Tracking:                                         │
│  {customer_id: [OnboardingTask, ...]}               │
│  Each task: id, stage, name, due, completed, notes  │
│                                                          │
│  Progress Calculation:                                  │
│  progress = completed_tasks / total_tasks × 100     │
│                                                          │
│  Velocity Tracking:                                     │
│  avg_days = mean(delta_between_milestones)          │
│  total_days = sum(all_deltas)                       │
│                                                          │
│  Thread Safety:                                        │
│  All operations protected by threading.Lock()           │
│  Copy-on-read for task lists                           │
└─────────────────────────────────────────────────────────┘
```

**Internal Data Structures:**

```
_tasks: Dict[str, List[OnboardingTask]]
  Key: customer_id
  Value: List of all tasks for that customer
  Each task tracks: task_id, stage, name, description, assignee, due_date, completed, notes

_milestones: Dict[str, Dict[OnboardingStage, datetime]]
  Key: customer_id
  Value: Mapping of stage → completion timestamp
  Used for velocity calculation and progress tracking
```

**Progress Algorithm:**

```
1. Retrieve all tasks for customer_id
2. Count completed tasks
3. Find first incomplete task → current_stage
4. If all complete → current_stage = COMPLETED
5. progress_percent = completed / total × 100
6. Return: current_stage, progress_percent, milestones_reached, days_since_start
```

**Velocity Calculation:**

```
1. Get all milestone timestamps for customer
2. Sort chronologically
3. Calculate deltas between consecutive milestones
4. avg_days_per_stage = mean(deltas)
5. total_days = sum(deltas)
6. Return velocity metrics for reporting
```

### 2. Health Scorer

Calculates customer health scores using weighted metrics across multiple dimensions with trend analysis.

```
┌─────────────────────────────────────────────────────────┐
│                HealthScorer                              │
│                                                          │
│  Health Score Weights:                                  │
│  ┌─────────────────────┬──────────┐                    │
│  │ Metric              │ Weight   │                    │
│  ├─────────────────────┼──────────┤                    │
│  │ product_usage       │ 30%      │                    │
│  │ engagement          │ 20%      │                    │
│  │ support_tickets     │ 15%      │                    │
│  │ nps_score           │ 15%      │                    │
│  │ payment_health      │ 10%      │                    │
│  │ relationship        │ 10%      │                    │
│  └─────────────────────┴──────────┘                    │
│                                                          │
│  Score Calculation:                                     │
│  score = Σ(metric_value × weight) / Σ(weights)     │
│                                                          │
│  Health Status Thresholds:                              │
│  ┌────────────┬─────────────┐                          │
│  │ Status     │ Score Range │                          │
│  ├────────────┼─────────────┤                          │
│  │ CRITICAL   │ 0-20        │                          │
│  │ POOR       │ 20-40       │                          │
│  │ AT_RISK    │ 40-55       │                          │
│  │ STABLE     │ 55-70       │                          │
│  │ HEALTHY    │ 70-85       │                          │
│  │ EXCELLENT  │ 85-100      │                          │
│  └────────────┴─────────────┘                          │
│                                                          │
│  Trend Analysis:                                        │
│  - Track metric history per customer (deque, maxlen=100)│
│  - Compare first-half vs second-half averages       │
│  - Classify: improving (>+2), declining (<-2), stable │
│                                                          │
│  Weight Customization:                                 │
│  set_weight(metric_type, weight)                       │
│  Allows per-organization weight tuning                 │
└─────────────────────────────────────────────────────────┘
```

**Score Calculation Details:**

```
Input: customer_id
Process:
  1. Retrieve all metrics for customer_id
  2. If no metrics → return 50.0 (default)
  3. Calculate total_weight = sum(m.weight for m in metrics)
  4. If total_weight == 0 → return 50.0
  5. weighted_sum = sum(m.value * m.weight for m in metrics)
  6. score = weighted_sum / total_weight
  7. Clamp to [0, 100]
  8. Cache in _scores dict
  9. Return score
```

**Trend Analysis Algorithm:**

```
Input: customer_id, days (default 30)
Process:
  1. Get all history entries within time window
  2. If < 2 data points → "insufficient_data"
  3. Split history into first_half and second_half
  4. Calculate mean of each half
  5. change = second_mean - first_mean
  6. Classify:
     change > 2  → "improving"
     change < -2 → "declining"
     else        → "stable"
  7. Return: trend, change value
```

### 3. Expansion Manager

Identifies and tracks expansion revenue opportunities across upgrade, cross-sell, and renewal types with win-rate analytics.

```
┌─────────────────────────────────────────────────────────┐
│               ExpansionManager                           │
│                                                          │
│  Expansion Types:                                       │
│  - UPGRADE: plan tier increase                      │
│  - CROSS_SELL: additional products                  │
│  - RENEWAL: contract renewal                        │
│  - ADD_ON: feature add-ons                          │
│  - SEAT_EXPANSION: more users                       │
│  - USAGE_BASED: overage charges                     │
│                                                          │
│  Pipeline:                                              │
│  ┌──────────────┬──────────────┬──────────────┐       │
│  │ Identified   │ In Progress  │ Closed Won   │       │
│  │ (prob × val) │              │ (actual)     │       │
│  └──────────────┴──────────────┴──────────────┘       │
│                                                          │
│  Pipeline Value:                                        │
│  Σ(estimated_value × probability) for open opps    │
│                                                          │
│  Win Rate:                                              │
│  closed_won / (closed_won + closed_lost) × 100     │
│                                                          │
│  Avg Deal Size:                                         │
│  Σ(closed_value) / count(won)                     │
│                                                          │
│  Status Lifecycle:                                     │
│  identified → in_progress → closed_won | closed_lost   │
└─────────────────────────────────────────────────────────┘
```

### 4. QBR Manager

Manages Quarterly Business Reviews including scheduling, execution, follow-up, and completion rate analytics.

```
┌─────────────────────────────────────────────────────────┐
│                QBRManager                                │
│                                                          │
│  QBR Lifecycle:                                         │
│  SCHEDULED → IN_PROGRESS → COMPLETED                │
│                    ↓                                 │
│                CANCELLED                             │
│                                                          │
│  QBR Components:                                    │
│  ┌──────────────────────────────────────────────┐    │
│  │ - Scheduled date & attendees                  │    │
│  │ - Metrics reviewed (health, usage, revenue)  │    │
│  │ - Action items with owners                    │    │
│  │ - Notes and follow-ups                        │    │
│  └──────────────────────────────────────────────┘    │
│                                                          │
│  Queries:                                           │
│  - Upcoming QBRs (next N days)                      │
│  - Customer QBR history                             │
│  - QBR completion rate                              │
│  - Overdue QBRs                                     │
│                                                          │
│  Completion Rate:                                     │
│  completed / (completed + cancelled) × 100          │
└─────────────────────────────────────────────────────────┘
```

### 5. Advocacy Manager

Manages customer advocacy programs including referrals, case studies, testimonials, and reviews with top-advocate ranking.

```
┌─────────────────────────────────────────────────────────┐
│               AdvocacyManager                            │
│                                                          │
│  Advocacy Types:                                    │
│  - REFERRAL: customer referrals                     │
│  - CASE_STUDY: published case studies               │
│  - TESTIMONIAL: customer quotes                     │
│  - REVIEW: public reviews                           │
│  - SPEAKING: event speaking                         │
│  - COMMUNITY: community participation               │
│                                                          │
│  Referral Code Generation:                          │
│  Format: REF_{customer_id}_{random}                 │
│  Unique per customer, trackable                     │
│                                                          │
│  Stats Tracking:                                    │
│  - Total entries per type                           │
│  - Completion rate                                  │
│  - Value generated                                  │
│  - Top advocates by value                           │
│                                                          │
│  Top Advocate Ranking:                              │
│  Sort by total value generated across all entries    │
│  Return top N advocates with counts and values       │
└─────────────────────────────────────────────────────────┘
```

### 6. Success Plan Manager

Creates and tracks success plans with goals, milestones, completion rates, and at-risk detection.

```
┌─────────────────────────────────────────────────────────┐
│            SuccessPlanManager                            │
│                                                          │
│  Plan Structure:                                    │
│  ┌──────────────────────────────────────────────┐    │
│  │ Success Plan                                  │    │
│  │ ├── Goals: [{objective, target, metric}]      │    │
│  │ ├── Milestones: [{name, due, completed}]     │    │
│  │ ├── Status: DRAFT|ACTIVE|ON_TRACK|AT_RISK    │    │
│  │ ├── Owner: CSM name                          │    │
│  │ └── Target Date                               │    │
│  └──────────────────────────────────────────────┘    │
│                                                          │
│  Completion Rate:                                   │
│  rate = completed_milestones / total_milestones     │
│                                                          │
│  At-Risk Detection:                                  │
│  Plans with < 50% completion flagged                  │
│                                                          │
│  Dynamic Goal/Milestone Addition:                     │
│  add_goal(plan_id, objective, target)                │
│  add_milestone(plan_id, name, target_date)          │
└─────────────────────────────────────────────────────────┘
```

### 7. Usage Tracker

Tracks product usage metrics and calculates adoption scores with trend analysis.

```
┌─────────────────────────────────────────────────────────┐
│                UsageTracker                              │
│                                                          │
│  Usage Metrics:                                     │
│  - logins_30d: monthly login count                  │
│  - active_users: users actively using product       │
│  - features_used / total_features: adoption ratio   │
│  - avg_session_minutes: engagement depth            │
│  - tasks_completed: feature utilization             │
│  - integrations_active: ecosystem depth             │
│  - api_calls: technical adoption                    │
│                                                          │
│  Adoption Score:                                    │
│  avg(min(100, metric_normalized)) across dimensions │
│                                                          │
│  Feature Adoption:                                  │
│  features_used / total_features × 100               │
│                                                          │
│  Trend Analysis:                                     │
│  Compare earliest vs most recent snapshot            │
│  Classify: growing (>+10%), declining (<-10%), stable │
│                                                          │
│  Snapshot History:                                   │
│  deque(maxlen=50) per customer                      │
│  Enables trend comparison over time                  │
└─────────────────────────────────────────────────────────┘
```

### 8. Renewal Tracker

Manages the full renewal lifecycle including risk scoring and at-risk identification.

```
┌─────────────────────────────────────────────────────────┐
│               RenewalTracker                             │
│                                                          │
│  Renewal Risk Levels:                              │
│  ┌────────────┬─────────────┐                          │
│  │ Level      │ Risk Range  │                          │
│  ├────────────┼─────────────┤                          │
│  │ NONE       │ 0.0 - 0.1   │                          │
│  │ LOW        │ 0.1 - 0.3   │                          │
│  │ MEDIUM     │ 0.3 - 0.5   │                          │
│  │ HIGH       │ 0.5 - 0.75  │                          │
│  │ CRITICAL   │ 0.75 - 1.0  │                          │
│  └────────────┴─────────────┘                          │
│                                                          │
│  Summary Metrics:                                  │
│  - total_renewals: count of all records             │
│  - total_value: Σ(current_value)                    │
│  - at_risk_value: Σ(value where HIGH|CRITICAL)      │
│  - upcoming: filtered by renewal_date ≤ cutoff      │
│                                                          │
│  Risk Score Update:                                 │
│  update_risk_score(renewal_id, score)               │
│  Auto-classifies into risk level                    │
└─────────────────────────────────────────────────────────┘
```

### 9. Risk Assessment

Evaluates customer risk factors and maintains mitigation action plans.

```
┌─────────────────────────────────────────────────────────┐
│              RiskAssessment                              │
│                                                          │
│  Risk Levels:                                      │
│  NONE → LOW → MEDIUM → HIGH → CRITICAL              │
│                                                          │
│  Assessment Entry:                                 │
│  ┌──────────────────────────────────────────────┐    │
│  │ - assessment_id (UUID)                         │    │
│  │ - customer_id                                  │    │
│  │ - risk_type: category of risk                  │    │
│  │ - risk_level: severity classification         │    │
│  │ - risk_score: 0.0 - 1.0 normalized            │    │
│  │ - factors: list of contributing factors        │    │
│  │ - mitigation_actions: planned mitigations      │    │
│  │ - reviewed: boolean flag                       │    │
│  └──────────────────────────────────────────────┘    │
│                                                          │
│  High-Risk View:                                    │
│  Grouped by customer_id, showing risk_count and types  │
│                                                          │
│  Summary:                                            │
│  Total assessments + count by risk level              │
└─────────────────────────────────────────────────────────┘
```

### 10. Customer Milestone Tracker

Tracks customer milestones across onboarding, success plans, product usage, relationships, contracts, and advocacy.

```
┌─────────────────────────────────────────────────────────┐
│         CustomerMilestoneTracker                         │
│                                                          │
│  Milestone Types:                                   │
│  - ONBOARDING: onboarding-specific milestones        │
│  - SUCCESS_PLAN: goals from success plans            │
│  - PRODUCT: product usage milestones                 │
│  - RELATIONSHIP: relationship building               │
│  - CONTRACT: contract-related events                 │
│  - ADVOCACY: advocacy participation                  │
│                                                          │
│  Progress Metrics:                                   │
│  ┌──────────────────────────────────────────────┐    │
│  │ - total: count of all milestones              │    │
│  │ - achieved: count of completed milestones     │    │
│  │ - overdue: milestones past target_date        │    │
│  │ - completion_rate: achieved / total × 100     │    │
│  └──────────────────────────────────────────────┘    │
│                                                          │
│  Upcoming Milestones:                                 │
│  Filter by target_date ≤ now + days, not achieved     │
└─────────────────────────────────────────────────────────┘
```

### 11. Value Realization

Measures how much value customers have realized vs their potential, tracking the progression through value stages.

```
┌─────────────────────────────────────────────────────────┐
│              ValueRealization                            │
│                                                          │
│  Value Stages:                                     │
│  NOT_STARTED → INITIAL_ADOPTION → PARTIAL_VALUE →   │
│  CORE_VALUE → FULL_VALUE → MAXIMUM_VALUE            │
│                                                          │
│  Value Entry:                                      │
│  - value_stage: current progression stage          │
│  - realized_value: actual value delivered           │
│  - potential_value: maximum possible value          │
│  - metrics: supporting data points                  │
│                                                          │
│  Realization Rate:                                 │
│  rate = realized_value / potential_value × 100     │
│                                                          │
│  Summary:                                            │
│  - total_realized: Σ(realized) across customers    │
│  - total_potential: Σ(potential) across customers  │
│  - overall_rate: total_realized / total_potential   │
│                                                          │
│  Per-Customer History:                               │
│  Multiple entries per customer tracking progression   │
│  Latest entry represents current state               │
└─────────────────────────────────────────────────────────┘
```

### 12. CSM Workload Manager

Balances workload across customer success managers and provides assignment recommendations.

```
┌─────────────────────────────────────────────────────────┐
│             CSMWorkloadManager                           │
│                                                          │
│  Workload Entry:                                    │
│  - csm_id: assigned CSM                             │
│  - customer_id: target customer                      │
│  - task_type: category of work                       │
│  - priority: low|normal|high|urgent                 │
│  - estimated_minutes: time estimate                  │
│  - status: pending|completed                        │
│                                                          │
│  Per-CSM Metrics:                                   │
│  ┌──────────────────────────────────────────────┐    │
│  │ - pending_tasks: count of incomplete work     │    │
│  │ - total_estimated_minutes: workload total     │    │
│  │ - customers_served: distinct customer count   │    │
│  └──────────────────────────────────────────────┘    │
│                                                          │
│  Balanced Assignment:                                │
│  Recommends CSM with lowest estimated_minutes        │
│  Ensures no single CSM is overloaded                 │
└─────────────────────────────────────────────────────────┘
```

### 13. Customer Feedback Manager

Collects and analyzes customer feedback across multiple channels with sentiment analysis and NPS calculation.

```
┌─────────────────────────────────────────────────────────┐
│          CustomerFeedbackManager                        │
│                                                          │
│  Feedback Sources:                                 │
│  - SURVEY: structured surveys                       │
│  - QBR: feedback from QBRs                          │
│  - SUPPORT_TICKET: support interactions              │
│  - NPS: Net Promoter Score surveys                  │
│  - IN_PRODUCT: in-app feedback                      │
│  - DIRECT_CONVERSATION: verbal feedback              │
│  - COMMUNITY: community forum feedback              │
│                                                          │
│  Sentiment Classification:                          │
│  ┌──────────────────────────────────────────────┐    │
│  │ rating ≥ 7  →  positive                       │    │
│  │ 4 < rating < 7  →  neutral                    │    │
│  │ rating ≤ 4  →  negative                       │    │
│  │ rating ≤ 3  →  follow_up_needed = True        │    │
│  └──────────────────────────────────────────────┘    │
│                                                          │
│  NPS Calculation:                                   │
│  NPS = (promoters - detractors) / total × 100      │
│  promoters: rating ≥ 9 | detractors: rating ≤ 6    │
│                                                          │
│  Follow-Up Tracking:                                │
│  Negative feedback auto-flagged for follow-up       │
│  Configurable follow-up window                      │
└─────────────────────────────────────────────────────────┘
```

### 14. Adoption Journey Tracker

Maps the customer adoption journey through defined phases with blocker identification.

```
┌─────────────────────────────────────────────────────────┐
│         AdoptionJourneyTracker                          │
│                                                          │
│  Adoption Phases:                                   │
│  ┌──────────────────────────────────────────────┐    │
│  │ AWARENESS (0-15%)                             │    │
│  │ → EXPLORATION (15-30%)                        │    │
│  │ → FIRST_VALUE (30-50%)                        │    │
│  │ → REGULAR_USE (50-70%)                        │    │
│  │ → DEEP_ADOPTION (70-85%)                      │    │
│  │ → CHAMPION (85-100%)                          │    │
│  └──────────────────────────────────────────────┘    │
│                                                          │
│  Journey Entry:                                     │
│  - phase: current adoption phase                    │
│  - adoption_score: 0-100 normalized                  │
│  - key_actions_completed: achievements list         │
│  - blockers: impediments to progress                │
│                                                          │
│  Distribution View:                                 │
│  Count of customers in each phase                    │
│                                                          │
│  Blocked Customers:                                 │
│  Customers with non-empty blockers list              │
│  Prioritized for intervention                       │
└─────────────────────────────────────────────────────────┘
```

## Data Flow Diagrams

### Customer Onboarding Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Start   │────▶│  Create      │────▶│  Track       │
│  Onboard │     │  Tasks       │     │  Progress    │
└──────────┘     └──────────────┘     └──────┬───────┘
                                              │
                    ┌──────────────┐     ┌────▼───────┐
                    │  Complete    │◀────│  Complete   │
│  Milestone │     │  Tasks       │     │  Tasks      │
└──────┬───────┘     └────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Mark Stage  │
                    │  Complete    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Velocity    │
                    │  Report      │
                    └──────────────┘
```

### Health Score Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Record  │────▶│  Apply       │────▶│  Calculate   │
│  Metrics │     │  Weights     │     │  Score       │
└──────────┘     └──────────────┘     └──────┬───────┘
                                              │
                    ┌──────────────┐     ┌────▼───────┐
                    │  Trigger     │◀────│  Classify   │
                    │  Intervention│     │  Health     │
                    └──────┬───────┘     └────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Trend       │
                    │  Analysis    │
                    └──────────────┘
```

### Expansion Pipeline Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│Identify  │────▶│  Qualify     │────▶│  Track       │
│Opp       │     │  Opportunity │     │  Pipeline    │
└──────────┘     └──────────────┘     └──────┬───────┘
                                              │
                    ┌──────────────┐     ┌────▼───────┐
                    │  Report      │◀────│  Close      │
                    │  Metrics     │     │  Deal       │
                    └──────────────┘     └────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Win Rate    │
                    │  Analytics   │
                    └──────────────┘
```

### Renewal Lifecycle Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Create  │────▶│  Calculate   │────▶│  Monitor     │
│  Renewal │     │  Risk Score  │     │  Status      │
└──────────┘     └──────────────┘     └──────┬───────┘
                                              │
                    ┌──────────────┐     ┌────▼───────┐
                    │  At-Risk     │◀────│  Risk       │
                    │  Actions     │     │  Level      │
                    └──────────────┘     └────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Renewal     │
                    │  Summary     │
                    └──────────────┘
```

### Adoption Journey Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Record  │────▶│  Determine   │────▶│  Track       │
│  Actions │     │  Phase       │     │  Progress    │
└──────────┘     └──────────────┘     └──────┬───────┘
                                              │
                    ┌──────────────┐     ┌────▼───────┐
                    │  Identify    │◀────│  Check      │
                    │  Blockers    │     │  Blockers   │
                    └──────────────┘     └────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Distribution│
                    │  Report      │
                    └──────────────┘
```

### Feedback Collection Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Record  │────▶│  Classify    │────▶│  Analyze     │
│  Rating  │     │  Sentiment   │     │  Trends      │
└──────────┘     └──────────────┘     └──────┬───────┘
                                              │
                    ┌──────────────┐     ┌────▼───────┐
                    │  Flag        │◀────│  Calculate   │
                    │  Follow-Up   │     │  NPS         │
                    └──────────────┘     └────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Negative    │
                    │  Feedback    │
                    │  Report      │
                    └──────────────┘
```

## Design Patterns

### 1. Pipeline Pattern
Expansion opportunities flow through identified → qualified → closed stages. Each stage transforms the opportunity data and may change its status.

### 2. State Machine
Onboarding stages and QBR status follow defined state transitions with guards preventing invalid transitions.

### 3. Weighted Scoring
Health scores use configurable weights for different metric categories, allowing customization per organization.

### 4. Registry Pattern
All entities (customers, plans, QBRs, renewals, assessments) use dictionary-based registries for O(1) lookup.

### 5. Template Method
Onboarding follows a template: kickoff → setup → training → go-live → adoption. The stages are predefined but execution is customer-specific.

### 6. Observer Pattern
Health score changes can trigger interventions. Adoption phase changes can trigger outreach.

### 7. Strategy Pattern
Health scoring weights and adoption phase thresholds are configurable, allowing different strategies per segment.

### 8. Composite Pattern
Success plans contain goals and milestones that are composed into a unified tracking structure.

### 9. Snapshot Pattern
Usage tracker maintains historical snapshots (deque with maxlen) for trend analysis without external storage.

### 10. Fan-Out Pattern
CSM workload manager fans out task assignments and aggregates results for balanced distribution.

## Thread Safety Model

```
┌─────────────────────────────────────────────────────────┐
│                  Thread Safety Model                     │
│                                                          │
│  Per-Manager Lock Strategy:                         │
│  ┌──────────────────────────────────────────────┐    │
│  │ Each manager owns a threading.Lock()           │    │
│  │ Lock scope: internal data structures only      │    │
│  │ No cross-manager locking required              │    │
│  └──────────────────────────────────────────────┘    │
│                                                          │
│  Lock Acquisition Order:                            │
│  1. Individual manager locks (no nesting)           │
│  2. Orchestrator lock only for _customers dict     │
│  3. No circular dependency possible                │
│                                                          │
│  Safe Patterns:                                     │
│  - with self._lock: for all dict reads/writes     │
│  - Copy-on-read: list(self._data.values())        │
│  - Atomic updates within lock scope                │
│                                                          │
│  Avoided:                                           │
│  - Nested lock acquisition                         │
│  - Lock held across I/O                             │
│  - Lock held during logger calls                   │
│                                                          │
│  Concurrency Ceiling:                               │
│  - Max parallel operations: 14 (one per manager)   │
│  - Expected contention: minimal (independent data) │
│                                                          │
│  Thread Safety Guarantees:                           │
│  - All dict operations atomic within lock           │
│  - No stale reads (copy-on-read pattern)           │
│  - No deadlocks (flat lock hierarchy)              │
└─────────────────────────────────────────────────────────┘
```

## Performance Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| Health Score Calc | < 50ms | Weighted sum over 6 metrics |
| Onboarding Progress | < 100ms | Task list scan + milestone check |
| Expansion Pipeline | < 200ms | Sum over all opportunities |
| Usage Adoption Score | < 100ms | Multi-dimension average |
| Renewal Summary | < 150ms | Sum + filter over records |
| Risk Assessment | < 100ms | Group + count operations |
| Milestone Progress | < 100ms | Filter + count |
| Value Summary | < 150ms | Sum over all customer entries |
| CSM Workload | < 100ms | Filter + sum per CSM |
| Feedback Sentiment | < 100ms | Count + average |
| Adoption Distribution | < 100ms | Count by phase |
| Full Report | < 500ms | Aggregation of all subsystems |
| Health Trend | < 80ms | History scan + split mean |
| Win Rate | < 100ms | Filter + count |
| Top Risk Customers | < 200ms | Score all + sort |
| NPS Score | < 100ms | Filter + count + calculate |

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

intervention_types:
  - CHECK_IN
  - TRAINING_SESSION
  - FEATURE_DEMO
  - ESCALATION
  - EXECUTIVE_SPONSOR
  - CUSTOM_SUCCESS_PLAN
```

## Error Handling

```
┌─────────────────────────────────────────────────────────┐
│               Error Hierarchy                            │
│                                                          │
│  CustomerSuccessError (base)                         │
│  ├── OnboardingError                                │
│  │   └── Task not found, invalid stage transition   │
│  ├── HealthScoreError                               │
│  │   └── Invalid metric type, weight out of range   │
│  ├── QBRError                                       │
│  │   └── QBR not found, invalid status transition   │
│  ├── RenewalError                                   │
│  │   └── Renewal not found, risk score invalid      │
│  ├── RiskAssessmentError                            │
│  │   └── Assessment not found, risk level invalid   │
│  ├── WorkloadError                                  │
│  │   └── CSM not found, task not found              │
│  ├── FeedbackError                                  │
│  │   └── Rating out of range, source invalid        │
│  ├── AdoptionError                                  │
│  │   └── Phase not found, score out of range        │
│  └── ValueRealizationError                          │
│      └── Stage not found, values invalid            │
│                                                          │
│  Strategy:                                           │
│  - All public methods wrapped in try/except           │
│  - Errors logged with context                        │
│  - Base exceptions for catch-all                      │
│  - Specific exceptions for targeted handling          │
│  - Graceful degradation on subsystem failures         │
└─────────────────────────────────────────────────────────┘
```

## Data Storage Model

```
┌─────────────────────────────────────────────────────────┐
│                In-Memory Storage                         │
│                                                          │
│  CustomerSuccessAgent._customers:                   │
│  Dict[str, Customer]                                    │
│                                                          │
│  Per-Manager Storage:                                │
│  OnboardingManager._tasks:                          │
│    Dict[str, List[OnboardingTask]]                   │
│  OnboardingManager._milestones:                     │
│    Dict[str, Dict[OnboardingStage, datetime]]        │
│  HealthScorer._metrics:                             │
│    Dict[str, Dict[str, HealthMetric]]                │
│  HealthScorer._history:                             │
│    Dict[str, deque(maxlen=100)]                     │
│  HealthScorer._scores:                              │
│    Dict[str, float]                                  │
│  ExpansionManager._opportunities:                   │
│    Dict[str, ExpansionOpportunity]                  │
│  QBRManager._qbrs:                                  │
│    Dict[str, QBR]                                    │
│  AdvocacyManager._entries:                          │
│    Dict[str, AdvocacyEntry]                         │
│  AdvocacyManager._referral_codes:                   │
│    Dict[str, str]                                    │
│  SuccessPlanManager._plans:                         │
│    Dict[str, SuccessPlan]                           │
│  UsageTracker._usage:                               │
│    Dict[str, UsageMetrics]                          │
│  UsageTracker._history:                             │
│    Dict[str, deque(maxlen=50)]                      │
│  RenewalTracker._renewals:                          │
│    Dict[str, RenewalRecord]                         │
│  RiskAssessment._assessments:                       │
│    Dict[str, RiskAssessmentEntry]                   │
│  CustomerMilestoneTracker._milestones:              │
│    Dict[str, MilestoneRecord]                       │
│  ValueRealization._entries:                         │
│    Dict[str, List[ValueEntry]]                      │
│  CSMWorkloadManager._workload:                      │
│    Dict[str, List[WorkloadEntry]]                   │
│  CustomerFeedbackManager._feedback:                 │
│    Dict[str, List[FeedbackRecord]]                  │
│  AdoptionJourneyTracker._journeys:                  │
│    Dict[str, List[AdoptionEntry]]                   │
│  CustomerSuccessAgent._interventions:               │
│    Dict[str, List[Intervention]]                    │
└─────────────────────────────────────────────────────────┘
```

## Orchestrator Coordination

The `CustomerSuccessAgent` orchestrator class coordinates between subsystems:

```
┌─────────────────────────────────────────────────────────┐
│              Orchestrator Responsibilities               │
│                                                          │
│  1. Customer Registration:                            │
│     add_customer() → _customers dict                  │
│                                                          │
│  2. Cross-Subsystem Updates:                          │
│     record_health_metric() →                         │
│       HealthScorer.record_metric()                    │
│       HealthScorer.calculate_health_score()           │
│       Customer.health_score = score                   │
│       Customer.health_status = status                 │
│                                                          │
│  3. Unified Reporting:                                │
│     get_full_report() →                               │
│       Aggregates from all 14 subsystems               │
│       Returns comprehensive dashboard data            │
│                                                          │
│  4. Status Monitoring:                                │
│     get_status() →                                    │
│       Customer count                                  │
│       Active plans                                    │
│       Health distribution                             │
│       Upcoming renewals                               │
│       Pending feedback                                │
│                                                          │
│  5. Lifecycle Management:                             │
│     initialize() → set _running = True                │
│     shutdown() → set _running = False                 │
└─────────────────────────────────────────────────────────┘
```
