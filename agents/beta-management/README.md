# Beta Management Agent

A production-grade system for orchestrating software beta programs -- from user recruitment through release coordination.

---

## Table of Contents

- [Overview](#overview)
- [Capability Matrix](#capability-matrix)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
  - [1. Create and Run a Beta Program](#1-create-and-run-a-beta-program)
  - [2. Feature Flag Management](#2-feature-flag-management)
  - [3. Feedback Collection and Analysis](#3-feedback-collection-and-analysis)
  - [4. A/B Testing](#4-ab-testing)
  - [5. Staged Rollout](#5-staged-rollout)
  - [6. Bug Tracking](#6-bug-tracking)
  - [7. Release Coordination](#7-release-coordination)
  - [8. Full Program Lifecycle](#8-full-program-lifecycle)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [End-to-End Walkthrough](#end-to-end-walkthrough)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Beta Management Agent manages the complete lifecycle of software beta programs. It coordinates user recruitment, onboarding, feature flagging, feedback collection, A/B testing, rollout management, and release coordination.

### Key Capabilities

| Capability | Description | Key Methods |
|------------|-------------|-------------|
| Program Lifecycle | Create, manage, and close beta programs | `create_beta_program()`, `create_closure_report()` |
| User Recruitment | Target, recruit, and onboard beta users | `recruit_beta_users()`, `onboard_users()` |
| Feature Flags | Configure and evaluate feature flags | `configure_feature_flags()`, `evaluate_flag()` |
| Feedback Collection | Gather feedback across multiple channels | `collect_feedback()`, `analyze_feedback()` |
| A/B Testing | Design and analyze controlled experiments | `run_ab_test()`, `analyze_ab_results()` |
| Rollout Management | Execute staged rollouts with rollback | `create_rollout_plan()`, `execute_rollout()` |
| Bug Tracking | Track and triage beta bug reports | `manage_bug_reports()` |
| Metrics Dashboard | Track and visualize beta metrics | `create_beta_metric_dashboard()` |
| Sentiment Analysis | Analyze user sentiment trends | `perform_sentiment_analysis()` |
| Retention Analysis | Track user retention cohorts | `analyze_retention()` |
| Release Readiness | Generate checklists and quality gates | `generate_release_checklist()` |
| Risk Assessment | Identify and mitigate program risks | `assess_risk()` |
| Data Export | Export all beta program data | `export_beta_data()` |
| Communication | Manage beta user communications | `manage_beta_communication()` |
| Usability Testing | Conduct and record usability sessions | `conduct_usability_sessions()` |
| User Segmentation | Create and manage user segments | `create_user_segments()` |

---

## Architecture

```
+---------------------------------------------------------------------+
|                   Beta Management Agent                              |
+---------------------------------------------------------------------+
|                                                                      |
|  +------------+  +------------+  +------------+  +------------+    |
|  |  Program    |  |   User     |  |  Feature   |  |  Feedback  |    |
|  |  Manager    |  | Recruiter  |  | Flag Engine|  |  Collector |    |
|  +------+-----+  +------+-----+  +------+-----+  +------+-----+    |
|         |                |                |                |         |
|         +----------------+----------------+----------------+         |
|                          |                |                           |
|                          v                v                           |
|  +--------------------------------------------------------------+   |
|  |                  Orchestration Layer                          |   |
|  +------------------------------+-------------------------------+   |
|                              |                                       |
|         +--------------------+--------------------+                 |
|         v                    v                    v                 |
|  +------------+  +------------+  +------------+                    |
|  |  Rollout   |  |   A/B Test |  |    Bug     |                    |
|  | Controller |  | Framework  |  |  Tracker   |                    |
|  +------+-----+  +------+-----+  +------+-----+                    |
|         |                |                |                          |
|         +----------------+----------------+                         |
|                          v                                           |
|  +--------------------------------------------------------------+   |
|  |              Analytics & Reporting                            |   |
|  +------------------------------+-------------------------------+   |
|                              |                                       |
|         +--------------------+--------------------+                 |
|         v                    v                    v                 |
|  +------------+  +------------+  +------------+                    |
|  |  Metrics   |  | Sentiment  |  |  Release   |                    |
|  | Dashboard  |  |  Analysis  |  |Coordinator |                    |
|  +------------+  +------------+  +------------+                    |
|                                                                      |
+---------------------------------------------------------------------+
```

---

## Installation

### From Source

```bash
git clone https://github.com/your-org/beta-management-agent.git
cd beta-management-agent
pip install -e .
```

### Requirements

```
Python >= 3.10
```

No external dependencies required -- the agent uses only the Python standard library.

### Verify Installation

```bash
python -c "from agent import BetaManagementAgent; print('Beta Management Agent loaded successfully')"
```

---

## Quick Start

```python
from agent import (
    BetaManagementAgent,
    BetaPhase,
    FeatureFlagType,
    FeedbackChannel,
    SeverityLevel,
    SentimentLevel,
    RolloutStrategy,
)

# Initialize the agent
agent = BetaManagementAgent()

# Create a beta program
program = agent.create_beta_program(
    name="My Feature Beta",
    description="Testing the new dashboard",
    target_users=100,
    rollout_strategy=RolloutStrategy.CANARY,
)

# Recruit users
users = agent.recruit_beta_users(
    program.program_id,
    emails=["user1@example.com", "user2@example.com"],
)

# Configure feature flag
flag = agent.configure_feature_flags(
    feature_name="new-dashboard",
    flag_type=FeatureFlagType.GRADUAL_ROLLOUT,
    enabled=True,
    percentage=25.0,
)

# Collect feedback
agent.collect_feedback(
    user_id=users[0].user_id,
    program_id=program.program_id,
    channel=FeedbackChannel.IN_APP,
    title="Dashboard looks great!",
    body="Love the new layout",
    sentiment=SentimentLevel.POSITIVE,
)

# Generate report
report = agent.generate_beta_report(program.program_id)
print(f"NPS: {report['metrics']['nps']}")
```

---

## Usage Examples

### 1. Create and Run a Beta Program

Complete program lifecycle from creation through active beta.

```python
from agent import BetaManagementAgent, ProgramStatus, RolloutStrategy

agent = BetaManagementAgent()

# Create program
program = agent.create_beta_program(
    name="Q3 Analytics Redesign",
    description="Beta test for the completely rebuilt analytics dashboard",
    target_users=200,
    rollout_strategy=RolloutStrategy.RING_BASED,
    features=["analytics-v2", "real-time-charts", "export-pro"],
    metadata={"team": "data-visualization", "quarter": "Q3-2026"},
)

# Recruit with segment targeting
power_users = agent.recruit_beta_users(
    program.program_id,
    emails=[f"power-{i}@example.com" for i in range(50)],
    user_type=BetaUserType.EXTERNAL_POWER,
    segments=["data-analyst", "power-user"],
)

standard_users = agent.recruit_beta_users(
    program.program_id,
    emails=[f"standard-{i}@example.com" for i in range(150)],
    user_type=BetaUserType.EXTERNAL_STANDARD,
    segments=["general-user"],
)

# Onboard all users
results = agent.onboard_users(program.program_id)
onboarded_count = sum(1 for v in results.values() if v)
print(f"Onboarded: {onboarded_count}/{len(results)}")

# Track progress
print(f"Program: {program.name}")
print(f"Phase: {program.phase.value}")
print(f"Enrollment: {program.enrollment_rate():.1%}")
```

### 2. Feature Flag Management

Configure different flag types for different use cases.

```python
from agent import BetaManagementAgent, FeatureFlagType, ReleaseStage

agent = BetaManagementAgent()

# Simple on/off flag
dark_mode = agent.configure_feature_flags(
    feature_name="dark-mode",
    flag_type=FeatureFlagType.BOOLEAN,
    enabled=True,
    release_stage=ReleaseStage.BETA,
    owner="design-team",
)

# Percentage-based rollout
new_search = agent.configure_feature_flags(
    feature_name="new-search-algorithm",
    flag_type=FeatureFlagType.PERCENTAGE,
    enabled=True,
    percentage=10.0,  # Start with 10%
    release_stage=ReleaseStage.ALPHA,
    owner="search-team",
)

# Segment-based targeting
advanced_analytics = agent.configure_feature_flags(
    feature_name="advanced-analytics",
    flag_type=FeatureFlagType.USER_SEGMENT,
    enabled=True,
    target_segments=["enterprise", "power_users"],
    release_stage=ReleaseStage.BETA,
    owner="analytics-team",
)

# Kill switch (emergency disable)
risky_feature = agent.configure_feature_flags(
    feature_name="new-export-engine",
    flag_type=FeatureFlagType.KILL_SWITCH,
    enabled=True,
    kill_switch=False,  # Set True to immediately disable
    release_stage=ReleaseStage.BETA,
    owner="platform-team",
)

# Evaluate flags for a specific user
user = agent.users[list(agent.users.keys())[0]]
is_enabled = agent.evaluate_flag(dark_mode.flag_id, user.user_id)
print(f"Dark mode enabled for {user.display_name}: {is_enabled}")
```

### 3. Feedback Collection and Analysis

Multi-channel feedback with automated analysis.

```python
from agent import (
    BetaManagementAgent,
    FeedbackChannel,
    SeverityLevel,
    SentimentLevel,
)

agent = BetaManagementAgent()
program = agent.create_beta_program(name="Feedback Demo", target_users=50)
users = agent.recruit_beta_users(program.program_id, emails=["test@example.com"])

# Collect feedback across channels
agent.collect_feedback(
    user_id=users[0].user_id,
    program_id=program.program_id,
    channel=FeedbackChannel.IN_APP,
    title="Export feature is amazing",
    body="The new PDF export saves me hours every week",
    severity=SeverityLevel.LOW,
    sentiment=SentimentLevel.VERY_POSITIVE,
    category="features",
    tags=["export", "productivity"],
)

agent.collect_feedback(
    user_id=users[0].user_id,
    program_id=program.program_id,
    channel=FeedbackChannel.SUPPORT_TICKET,
    title="Charts crash on large datasets",
    body="Loading 50K rows causes browser to freeze",
    severity=SeverityLevel.CRITICAL,
    sentiment=SentimentLevel.VERY_NEGATIVE,
    category="performance",
    steps_to_reproduce="1. Open analytics 2. Load 50K row dataset 3. Browser freezes",
    expected="Dashboard loads within 5 seconds",
    actual="Browser becomes unresponsive",
)

# Analyze feedback
analysis = agent.analyze_feedback(program.program_id)
print(f"Total feedback: {analysis['total']}")
print(f"Actionable items: {analysis['actionable']}")
print(f"Severity distribution: {analysis['severity_distribution']}")
print(f"Average sentiment: {analysis['average_sentiment']:.3f}")
print(f"Sentiment trend: {analysis['sentiment_trend']}")
```

### 4. A/B Testing

Design and analyze controlled experiments.

```python
from agent import BetaManagementAgent

agent = BetaManagementAgent()
program = agent.create_beta_program(name="A/B Test Demo", target_users=500)

# Create A/B test
test = agent.run_ab_test(
    name="Dashboard Grid vs List Layout",
    hypothesis="Grid layout increases task completion rate by 15%",
    primary_metric="task_completion_rate",
    secondary_metrics=["time_on_task", "user_satisfaction", "error_rate"],
    sample_size=2000,
    duration_days=14,
    confidence_level=0.95,
)

print(f"Test started: {test.name}")
print(f"Status: {test.status}")

# Analyze results
results = agent.analyze_ab_results(test.test_id)
print(f"\nResults:")
print(f"  Control mean: {results['control_mean']:.4f}")
print(f"  Treatment mean: {results['treatment_mean']:.4f}")
print(f"  Absolute difference: {results['absolute_difference']:.4f}")
print(f"  Relative lift: {results['relative_difference_pct']:.1f}%")
print(f"  P-value: {results['p_value']:.4f}")
print(f"  Significant: {results['is_significant']}")
print(f"  Recommendation: {results['recommendation']}")
```

### 5. Staged Rollout

Execute canary releases with health monitoring.

```python
from agent import BetaManagementAgent, RolloutStrategy

agent = BetaManagementAgent()

# Create canary rollout plan
plan = agent.create_rollout_plan(
    feature_name="dashboard-v2",
    strategy=RolloutStrategy.CANARY,
    stages=[
        {"percentage": 1, "description": "Internal dogfooding", "duration_days": 2},
        {"percentage": 5, "description": "Early adopters", "duration_days": 3},
        {"percentage": 25, "description": "Power users", "duration_days": 5},
        {"percentage": 50, "description": "Partial GA", "duration_days": 3},
        {"percentage": 100, "description": "Full rollout", "duration_days": 0},
    ],
    rollback_threshold=0.03,
    monitoring_metrics=["error_rate", "latency_p99", "user_satisfaction"],
)

# Execute stages
for _ in range(3):
    result = agent.execute_rollout(plan.plan_id)
    print(f"Stage {result['executed_stage']}: {result['new_percentage']}%")

# Monitor health
monitoring = agent.monitor_rollout(plan.plan_id)
print(f"\nHealth Check:")
print(f"  Current: {monitoring['current_percentage']}%")
print(f"  Error rate: {monitoring['average_error_rate']:.4f}")
print(f"  Recommendation: {monitoring['recommendation']}")
```

### 6. Bug Tracking

Track and manage bugs from beta users.

```python
from agent import BetaManagementAgent, BugPriority

agent = BetaManagementAgent()
program = agent.create_beta_program(name="Bug Tracking Demo", target_users=50)
users = agent.recruit_beta_users(program.program_id, emails=["tester@example.com"])

# Create bug reports with different priorities
priorities_and_titles = [
    (BugPriority.P0_BLOCKER, "App crashes on login"),
    (BugPriority.P1_CRITICAL, "Data loss on save"),
    (BugPriority.P2_MAJOR, "Chart labels overlapping"),
    (BugPriority.P3_MINOR, "Tooltip text misaligned"),
    (BugPriority.P4_TRIVIAL, "Typo in help text"),
]

for priority, title in priorities_and_titles:
    agent.manage_bug_reports(
        program.program_id,
        action="create",
        reporter_id=users[0].user_id,
        priority=priority,
        title=title,
        description=f"Detailed description of: {title}",
        steps=["Step 1", "Step 2", "Step 3"],
        expected="Expected behavior",
        actual="Actual behavior",
    )

# Get summary
summary = agent.manage_bug_reports(program.program_id, action="summary")
print(f"Total bugs: {summary['total']}")
print(f"By priority: {summary['by_priority']}")
print(f"Blockers: {summary['blockers']}")
```

### 7. Release Coordination

Generate checklists and assess release readiness.

```python
from agent import BetaManagementAgent, ReleaseStage

agent = BetaManagementAgent()
program = agent.create_beta_program(name="Release Demo", target_users=100)

# Generate release checklist
checklist = agent.generate_release_checklist(
    feature_name="dashboard-v2",
    release_stage=ReleaseStage.GENERAL_AVAILABILITY,
)

print(f"Release Checklist for: {checklist.feature_name}")
print(f"Total items: {len(checklist.items)}")
for item in checklist.items:
    print(f"  [ ] {item['item']} ({item['category']})")

# Risk assessment
risks = agent.assess_risk(program.program_id)
print(f"\nRisk Assessment:")
for risk in risks:
    print(f"  [{risk.severity.value}] {risk.title}")
    print(f"    Score: {risk.risk_score():.2f}")
    print(f"    Mitigation: {risk.mitigation}")
```

### 8. Full Program Lifecycle

Complete end-to-end beta program from start to finish.

```python
from agent import (
    BetaManagementAgent,
    BetaPhase,
    FeatureFlagType,
    FeedbackChannel,
    SeverityLevel,
    SentimentLevel,
    RolloutStrategy,
    BugPriority,
    MetricCategory,
    ReleaseStage,
)

agent = BetaManagementAgent()

# Phase 1: Create and recruit
program = agent.create_beta_program(
    name="Full Lifecycle Demo",
    description="Complete beta program demonstration",
    target_users=100,
    rollout_strategy=RolloutStrategy.CANARY,
    features=["feature-x"],
)

users = agent.recruit_beta_users(
    program.program_id,
    emails=[f"user-{i}@example.com" for i in range(80)],
)

# Phase 2: Onboard
agent.onboard_users(program.program_id)

# Phase 3: Configure flags
agent.configure_feature_flags(
    feature_name="feature-x",
    flag_type=FeatureFlagType.GRADUAL_ROLLOUT,
    enabled=True,
    percentage=25.0,
)

# Phase 4: Collect feedback and metrics
for user in users[:20]:
    agent.collect_feedback(
        user_id=user.user_id,
        program_id=program.program_id,
        channel=FeedbackChannel.IN_APP,
        title="Feature X feedback",
        body="This feature is really useful for my workflow",
        severity=SeverityLevel.LOW,
        sentiment=SentimentLevel.POSITIVE,
    )

for _ in range(50):
    agent.record_metric(
        program_id=program.program_id,
        category=MetricCategory.ENGAGEMENT,
        name="session_duration",
        value=300.0,
        unit="seconds",
    )

# Phase 5: Track bugs
agent.manage_bug_reports(
    program.program_id,
    action="create",
    reporter_id=users[0].user_id,
    priority=BugPriority.P2_MAJOR,
    title="Minor rendering issue",
    description="Some edge cases in chart rendering",
)

# Phase 6: Run A/B test
test = agent.run_ab_test(
    name="Feature X Variant Test",
    hypothesis="Variant B increases engagement",
    primary_metric="engagement_score",
)
agent.analyze_ab_results(test.test_id)

# Phase 7: Rollout
plan = agent.create_rollout_plan(
    feature_name="feature-x",
    strategy=RolloutStrategy.CANARY,
)
agent.execute_rollout(plan.plan_id)

# Phase 8: Generate reports
dashboard = agent.create_beta_metric_dashboard(program.program_id)
sentiment = agent.perform_sentiment_analysis(program.program_id)
closure = agent.create_closure_report(program.program_id)

print(f"\n=== Program Complete ===")
print(f"Users: {dashboard['total_users']}")
print(f"NPS: {dashboard.get('nps_score', 'N/A')}")
print(f"Sentiment: {sentiment.overall_sentiment().value}")
print(f"Findings: {len(closure.key_findings)}")
print(f"Recommendations: {len(closure.recommendations)}")
```

---

## API Reference

### BetaManagementAgent

#### Constructor

```python
BetaManagementAgent(store: Optional[DataStore] = None)
```

Creates a new agent instance. Optionally accepts a custom data store implementation.

#### Program Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `create_beta_program(...)` | `BetaProgram` | Create a new beta program |
| `recruit_beta_users(...)` | `List[BetaUser]` | Recruit users into a program |
| `onboard_users(...)` | `Dict[str, bool]` | Onboard users with a flow |
| `generate_beta_report(...)` | `Dict[str, Any]` | Generate comprehensive report |
| `create_closure_report(...)` | `BetaClosureReport` | Generate closure report |
| `export_beta_data(...)` | `Dict[str, Any]` | Export all program data |

#### Feature Flag Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `configure_feature_flags(...)` | `FeatureFlag` | Configure a feature flag |
| `evaluate_flag(...)` | `bool` | Evaluate flag for a user |

#### Feedback Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `collect_feedback(...)` | `FeedbackItem` | Collect user feedback |
| `analyze_feedback(...)` | `Dict[str, Any]` | Analyze feedback metrics |
| `perform_sentiment_analysis(...)` | `SentimentAnalysis` | Analyze sentiment trends |

#### Rollout Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `create_rollout_plan(...)` | `RolloutPlan` | Create a rollout plan |
| `execute_rollout(...)` | `Dict[str, Any]` | Execute next rollout stage |
| `monitor_rollout(...)` | `Dict[str, Any]` | Monitor rollout health |

#### A/B Testing Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `run_ab_test(...)` | `ABTest` | Start an A/B test |
| `analyze_ab_results(...)` | `Dict[str, Any]` | Analyze test results |

#### Analytics Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `create_beta_metric_dashboard(...)` | `Dict[str, Any]` | Generate dashboard |
| `record_metric(...)` | `BetaMetric` | Record a metric data point |
| `analyze_retention(...)` | `RetentionCohort` | Analyze retention cohorts |

#### Bug Management Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `manage_bug_reports(...)` | `Any` | Create/list/resolve/summarize bugs |

#### Communication Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `manage_beta_communication(...)` | `BetaAnnouncement` | Send announcements |
| `design_survey(...)` | `SurveyTemplate` | Create a survey |

#### Planning Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `create_user_segments(...)` | `List[UserSegment]` | Create user segments |
| `create_iteration_plan(...)` | `IterationPlan` | Create iteration plan |
| `assess_risk(...)` | `List[RiskAssessment]` | Assess program risks |
| `generate_release_checklist(...)` | `ReleaseChecklist` | Generate release checklist |
| `conduct_usability_sessions(...)` | `List[UsabilitySession]` | Conduct usability tests |

---

## Configuration

### Custom Data Store

Implement the `DataStore` protocol for persistent storage:

```python
from agent import BetaManagementAgent, DataStore

class PostgresStore:
    def __init__(self, connection_string: str):
        self.conn = psycopg2.connect(connection_string)

    def save(self, key: str, value: Any) -> None:
        # Implement PostgreSQL storage
        pass

    def load(self, key: str) -> Optional[Any]:
        # Implement PostgreSQL retrieval
        pass

    def delete(self, key: str) -> None:
        # Implement PostgreSQL deletion
        pass

    def list_keys(self, prefix: str = "") -> List[str]:
        # Implement key listing
        pass

agent = BetaManagementAgent(store=PostgresStore("postgresql://localhost/beta"))
```

### Logging Configuration

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Verbose logging for development
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("beta-agent.log"),
        logging.StreamHandler(),
    ],
)
```

---

## End-to-End Walkthrough

This walkthrough demonstrates a complete beta program from creation to closure.

### Step 1: Create the Program

```python
from agent import BetaManagementAgent, RolloutStrategy, FeatureFlagType

agent = BetaManagementAgent()

program = agent.create_beta_program(
    name="Smart Notifications Beta",
    description="AI-powered notification prioritization and digest",
    target_users=300,
    rollout_strategy=RolloutStrategy.CANARY,
    features=["smart-notifications", "notification-digest", "priority-scoring"],
)
print(f"Created program: {program.program_id}")
```

### Step 2: Recruit Participants

```python
# Power users get early access
power = agent.recruit_beta_users(
    program.program_id,
    emails=[f"power-{i}@company.com" for i in range(50)],
    user_type=BetaUserType.EXTERNAL_POWER,
    segments=["notification-heavy", "power-user"],
)

# Standard users for broader feedback
standard = agent.recruit_beta_users(
    program.program_id,
    emails=[f"user-{i}@company.com" for i in range(250)],
    user_type=BetaUserType.EXTERNAL_STANDARD,
    segments=["general-user"],
)

print(f"Recruited {len(power)} power users and {len(standard)} standard users")
```

### Step 3: Onboard Users

```python
from agent import OnboardingFlow, BetaUserType

flow = OnboardingFlow(
    name="Smart Notifications Onboarding",
    steps=[
        {"title": "Welcome to Smart Notifications", "type": "info"},
        {"title": "How AI Prioritization Works", "type": "interactive"},
        {"title": "Customize Your Preferences", "type": "configuration"},
        {"title": "Try Your First Digest", "type": "guided"},
    ],
    target_user_type=BetaUserType.EXTERNAL_STANDARD,
    estimated_minutes=12,
)

results = agent.onboard_users(program.program_id, flow=flow)
print(f"Onboarding complete: {sum(results.values())}/{len(results)} users")
```

### Step 4: Configure Feature Flags

```python
agent.configure_feature_flags(
    feature_name="smart-notifications",
    flag_type=FeatureFlagType.GRADUAL_ROLLOUT,
    enabled=True,
    percentage=25.0,
    release_stage=FeatureFlagType.GRADUAL_ROLLOUT,
    owner="notifications-team",
)

agent.configure_feature_flags(
    feature_name="notification-digest",
    flag_type=FeatureFlagType.USER_SEGMENT,
    enabled=True,
    target_segments=["power-user"],
    release_stage=ReleaseStage.ALPHA,
    owner="notifications-team",
)
```

### Step 5: Collect Feedback During Beta

```python
from agent import FeedbackChannel, SeverityLevel, SentimentLevel

for user in power[:30]:
    agent.collect_feedback(
        user_id=user.user_id,
        program_id=program.program_id,
        channel=FeedbackChannel.IN_APP,
        title="Prioritization is spot-on",
        body="The AI correctly prioritizes urgent notifications",
        severity=SeverityLevel.LOW,
        sentiment=SentimentLevel.POSITIVE,
        category="prioritization",
    )

for user in standard[:50]:
    agent.collect_feedback(
        user_id=user.user_id,
        program_id=program.program_id,
        channel=FeedbackChannel.SURVEY,
        title="Digest timing could be better",
        body="I prefer receiving digests in the morning, not evening",
        severity=SeverityLevel.MEDIUM,
        sentiment=SentimentLevel.NEUTRAL,
        category="timing",
    )
```

### Step 6: Track Metrics and Bugs

```python
from agent import MetricCategory, BugPriority

# Record engagement metrics
for _ in range(100):
    agent.record_metric(
        program_id=program.program_id,
        category=MetricCategory.ENGAGEMENT,
        name="notification_open_rate",
        value=0.72,
        unit="ratio",
    )

# Track bugs
agent.manage_bug_reports(
    program.program_id,
    action="create",
    reporter_id=power[0].user_id,
    priority=BugPriority.P1_CRITICAL,
    title="Digest not sending for some users",
    description="15% of users report not receiving daily digest",
    steps=["1. Enable digest", "2. Wait 24 hours", "3. No digest received"],
    expected="Daily digest email received",
    actual="No email received",
)
```

### Step 7: Analyze Results

```python
# Feedback analysis
analysis = agent.analyze_feedback(program.program_id)
print(f"Feedback: {analysis['total']} items, {analysis['actionable']} actionable")

# Sentiment
sentiment = agent.perform_sentiment_analysis(program.program_id)
print(f"Sentiment: {sentiment.overall_sentiment().value}")

# Retention
retention = agent.analyze_retention(program.program_id)
print(f"D30 retention: {retention.retention_at_day(30):.1%}")

# Dashboard
dashboard = agent.create_beta_metric_dashboard(program.program_id)
print(f"NPS: {dashboard.get('nps_score', 'N/A')}")
```

### Step 8: Plan Iterations and Release

```python
# Iteration plan
iteration = agent.create_iteration_plan(program.program_id)
print(f"Iteration items: {len(iteration.items)}")

# Release checklist
checklist = agent.generate_release_checklist(
    feature_name="smart-notifications",
    release_stage=ReleaseStage.GENERAL_AVAILABILITY,
)
print(f"Release ready: {checklist.is_ready()}")

# Closure report
closure = agent.create_closure_report(program.program_id)
print(f"Key findings: {closure.key_findings}")
print(f"Recommendations: {closure.recommendations}")
```

---

## Best Practices

### Program Design

- **Define success criteria upfront**: Know what "success" looks like before launching
- **Set realistic timelines**: Beta programs typically run 2-8 weeks
- **Diversify your participant pool**: Include power users, standard users, and edge cases
- **Plan feedback touchpoints**: Don't wait for users to come to you

### Feature Flag Management

- **Use descriptive flag names**: `dashboard-grid-layout` not `flag-1`
- **Set owner on every flag**: Know who to contact about each flag
- **Use kill switches for risky features**: Always have an emergency off switch
- **Clean up retired flags**: Remove flags after GA to reduce technical debt

### Feedback Collection

- **Mix quantitative and NPS scores with qualitative open-text feedback**
- **Close the feedback loop**: Tell users what you did with their input
- **Prioritize by severity and frequency**: One critical bug beats ten cosmetic requests
- **Use multiple channels**: Different users prefer different feedback mechanisms

### Rollout Strategy

- **Start small**: Canary releases catch issues before they affect many users
- **Define rollback thresholds**: Know when to pull the plug before you need to
- **Monitor continuously**: Don't just check at stage transitions
- **Document rollback procedures**: When things go wrong at 2 AM, you need clear steps

### A/B Testing

- **Calculate sample size before starting**: Underpowered tests waste time
- **Test one thing at a time**: Confounded results are useless
- **Wait for full duration**: Don't peek and stop early based on p-hacking
- **Consider practical significance**: A 0.1% lift may not be worth shipping

---

## Troubleshooting

### Q: Users aren't enrolling in the beta

**Check enrollment rate:**
```python
program = agent.programs[program_id]
print(f"Enrolled: {program.enrolled_users}/{program.target_users}")
print(f"Rate: {program.enrollment_rate():.1%}")
```

**Solutions:**
- Expand recruitment channels
- Clarify the value proposition in invitations
- Simplify the signup process
- Consider offering incentives

### Q: Feedback volume is too low

**Check feedback metrics:**
```python
analysis = agent.analyze_feedback(program_id)
print(f"Total: {analysis['total']}")
print(f"By channel: {analysis['channel_distribution']}")
```

**Solutions:**
- Add in-app feedback prompts
- Send survey reminders
- Conduct user interviews for deeper insights
- Make feedback submission frictionless

### Q: A/B test isn't reaching significance

**Check test parameters:**
```python
results = agent.analyze_ab_results(test_id)
print(f"Sample size needed vs actual")
print(f"Effect size: {results['relative_difference_pct']:.1f}%")
print(f"P-value: {results['p_value']:.4f}")
```

**Solutions:**
- Increase sample size by expanding the test population
- Run the test longer
- Test a more impactful variant
- Consider whether the metric is the right one

### Q: Rollback was triggered

**Investigate the cause:**
```python
monitoring = agent.monitor_rollout(plan_id)
print(f"Error rate: {monitoring['average_error_rate']}")
print(f"Threshold: {monitoring['rollback_threshold']}")
```

**Solutions:**
- Review recent code changes
- Check infrastructure metrics
- Fix the root cause
- Re-run canary from stage 1

### Q: Negative sentiment from beta users

**Analyze sentiment:**
```python
sentiment = agent.perform_sentiment_analysis(program_id)
print(f"Top negative themes: {sentiment.top_negative_themes}")
```

**Solutions:**
- Address the top negative themes directly
- Increase communication frequency
- Conduct follow-up interviews
- Consider feature rollback if sentiment is severely negative

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Write tests for your changes
4. Ensure all tests pass (`pytest`)
5. Submit a pull request

### Development Setup

```bash
# Clone and install
git clone https://github.com/your-org/beta-management-agent.git
cd beta-management-agent
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run type checking
mypy agent.py

# Run linting
ruff check agent.py
```

---

## License

MIT License

Copyright (c) 2026 MiMoCode

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
