# CertificationPrep Agent Architecture

## 1. Overview

The CertificationPrep Agent is a multi-layered, modular Python system designed to
assist learners in preparing for technical certifications through structured study
plans, exam simulations, progress tracking and strategic guidance. This document
describes the high-level architecture, all component boundaries, data flows, design
rationale, error handling, performance characteristics, testing strategy, security
posture, deployment options, maintenance procedures, known limitations and future
enhancements.

The agent is built around five pillars: **planning**, **practice**, **progress**,
**resources** and **strategy**. Each pillar is backed by a service-layer collaborator
with a single responsibility, keeping the system easy to extend and maintain.

### 1.1 Design Goals

The architecture addresses the following core goals:

- **Determinism**: Given the same inputs, the agent produces identical outputs,
  enabling reproducible test fixtures and CI/CD integration.
- **Zero external dependencies**: The agent relies solely on the Python standard
  library, making it lightweight and portable.
- **Testability**: Pure functions and single-responsibility classes mean each
  component can be unit-tested in isolation.
- **Extensibility**: New templates, resources and certification routes can be
  registered at runtime without modifying core logic.
- **Clarity**: Public API surface is intentionally small and well-typed,
  minimising the learning curve for new contributors.
- **Observability**: Status, progress and readiness scores are easy to query
  and monitor in production environments.
- **Graceful Degradation**: Missing or invalid inputs result in sensible defaults
  or descriptive errors rather than hard crashes.

### 1.2 Architectural Layers

The system is organised into five distinct layers:

1. **Consumer Layer**: CLI, web frameworks, notebooks, automation pipelines.
2. **API Layer**: `CertificationPrepAgent` with validation, clamping and orchestration.
3. **Service Layer**: Independent collaborating components (plan generator, question bank, etc.).
4. **Foundation Layer**: Models, configuration, utilities.
5. **Persistence Layer**: JSON filesystem helpers for durable state.

```
┌──────────────────────────────────────────────────────────────────────┐
│                         Consumer Layer                               │
│          (CLI, Web APIs, Notebooks, CI Pipelines, etc.)             │
└──────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────┐
│                  CertificationPrepAgent (API Layer)                  │
│      • Parameter clamping                                            │
│      • Input validation                                               │
│      • Service delegation                                             │
│      • Async wrappers                                                 │
│      • Model-to-dict serialisation                                    │
└──────────────────────────────────────────────────────────────────────┘
                                    │
                        ┌───────────┴───────────┐
                        ▼                       ▼
          ┌──────────────────────┐  ┌──────────────────────┐
          │   Service Layer       │  │   Coordination Layer  │
          │   (Specialised)       │  │   (Orchestration)     │
          └──────────────────────┘  └──────────────────────┘
                        │                       │
          ┌─────────────┼───────────┐           │
          │             │           │           │
          ▼             ▼           ▼           ▼
   [StudyPlan    [Resource    [Progress  [Analytics
    Generator]   Curator]     Tracker]   Engine]
          │             │           │           │
          │             │           │           │
   [Question    [Schedule    [MockExam   [ExamStrategy
    Bank]       Optimizer]   Simulator]   Advisor]
          │             │                       │
          │             │                       │
          │             ▼                       │
          │     [StudyNoteGenerator]            │
          │             │                       │
          │             │                       │
          └─────────────┼───────────────────────┘
                        ▼
          ┌──────────────────────┐
          │     Model Layer       │
          │  (@dataclass models   │
          │   with to_dict())     │
          └──────────────────────┘
                        │
                        ▼
          ┌──────────────────────┐
          │  Persistence Layer    │
          │  (JSON filesystem)    │
          └──────────────────────┘
```

## 2. System Architecture Diagram

```
                         ┌──────────────────────────────┐
                         │  CertificationPrep Agent      │
                         │  (Public API Layer)           │
                         └──────────┬───────────────────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           │                        │                        │
           ▼                        ▼                        ▼
┌───────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐
│ StudyPlanGenerator │ │ QuestionBank          │ │ ResourceCurator      │
│ ─────────────────  │ │ ────────────────────  │ │ ────────────────────  │
│ • parse_timeline() │ │ • generate()          │ │ • recommend()        │
│ • build_plan()     │ │ • templates[]         │ │ • add_resource()     │
│ • resolve_domains()│ │ • _pick_templates()   │ │ • RESOURCE_DB[]      │
│ • schedule         │ │ • _fill_template()    │ │                      │
│ • milestones       │ │ • _make_options()     │ │                      │
└─────────┬──────────┘ └───────────┬──────────┘ └──────────┬───────────┘
           │                        │                        │
           ▼                        ▼                        ▼
┌───────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐
│ ProgressTracker   │ │ MockExamSimulator    │ │ ExamStrategyAdvisor  │
│ ─────────────────  │ │ ────────────────────  │ │ ────────────────────  │
│ • update()        │ │ • run()               │ │ • strategy_for()     │
│ • get()           │ │ • _scoring            │ │ • _time_bands         │
│ • _compute_pct()  │ │ • _topic_breakdown    │ │                      │
└─────────┬──────────┘ └───────────┬──────────┘ └──────────┬───────────┘
           │                        │                        │
           ▼                        ▼                        ▼
┌────────────────────────────────────────────────────────────────┐
│                      AnalyticsEngine                            │
│                      ─────────────────                          │
│          • summary_for()  • rank_resources()                   │
└────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                         ┌──────────────────────────────┐
                         │  Model Layer                 │
                         │  StudyPlan / PracticeQ / etc │
                         └──────────────────────────────┘
                                    │
                                    ▼
                         ┌──────────────────────────────┐
                         │  Persistence Layer           │
                         │  (JSON files)                │
                         └──────────────────────────────┘
```

## 3. Design Principles

### 3.1 Single Responsibility

Each service class handles exactly one domain concern. This makes the codebase
easy to unit-test, easy to reason about and easy to extend when users request
new functionality.

### 3.2 Data-Aware but Agnostic

Models are defined as `@dataclass` structures with clear field semantics. The
agents themselves never speak directly to a database or external API; they
operate on in-memory dataclasses. Persistence is an opt-in concern pushed to
the JSON helper methods.

### 3.3 Typed Contracts

All public methods use Python type hints and explicit return shapes. This allows
consumers to know exactly what dictionary keys to expect and enables static
analysis with `mypy`.

### 3.4 Graceful Degradation

When optional inputs are missing (no timeline, no topic override, no seed), the
agent uses sensible defaults defined in the `Config` object. Invalid subjects,
out-of-bounds counts and negative values are clamped to safe ranges to prevent
cascading errors.

### 3.5 Separation of Concerns

The system is organised into four distinct layers:

1. **Consumer Layer**: CLI, web frameworks, notebooks.
2. **API Layer**: `CertificationPrepAgent` with validation, clamping and orchestration.
3. **Service Layer**: Independent collaborating components (plan generator, question bank, etc.).
4. **Foundation Layer**: Models, configuration, utilities.

### 3.6 Explicit over Implicit

The agent avoids magic behaviour. All weights, thresholds, defaults and mappings
are defined as named constants or configurable fields, not buried in inline literals.

### 3.7 Fail-Fast Validation

Invalid inputs are rejected early with descriptive error messages. This prevents
wasted computation and helps consumers debug integration issues quickly.

### 3.8 Dependency Inversion

High-level modules (the `CertificationPrepAgent`) do not depend on low-level
module implementations. Both depend on abstractions (shared `Config` and
dataclass interfaces). New service components can be injected without changing
the API layer.

### 3.9 Open/Closed Principle

The system is open for extension (new templates, resources, routes) but closed
for modification (core logic remains stable). Registry patterns and `add_`
methods enable extension without touching existing code.

## 4. Component Deep-Dive

### 4.1 Public API Layer (`CertificationPrepAgent`)

The `CertificationPrepAgent` is the central coordinator. Its responsibilities
include:

- Parameter validation and clamping before delegating to services.
- Transforming model objects into plain serialisable dictionaries.
- Orchestrating cross-service workflows (plan creation, note export, backup).
- Providing async wrappers for CPU-bound operations.
- Managing lifecycle and dependencies of all service components.

It holds a reference to each service object (injected via the constructor) and
a `_plans` list that stores `StudyPlan` instances created during the lifetime of
the agent.

### 4.2 Configuration Layer (`Config`)

The `Config` dataclass defines runtime behaviour:

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `default_domain` | `Optional[CertificationDomain]` | `None` | Preferred certification family when none supplied. |
| `default_difficulty` | `DifficultyLevel` | `INTERMEDIATE` | Baseline difficulty for generated content. |
| `study_hours_per_week` | `int` | `10` | Budget used by `ScheduleOptimizer`. |
| `retention_days` | `int` | `90` | Placeholder for future TTL / expiry logic. |
| `storage_path` | `str` | `<agent_dir>/certification_prep_data` | JSON persistence root. |
| `verbose` | `bool` | `False` | Log verbosity when wired to a logger. |
| `enable_notifications` | `bool` | `False` | Enable email/SMTP notifications. |
| `smtp_host` | `Optional[str]` | `None` | SMTP server hostname. |
| `smtp_port` | `int` | `587` | SMTP server port. |
| `session_tracking` | `bool` | `True` | Track study sessions. |
| `competency_assessment` | `bool` | `True` | Enable adaptive competency assessment. |

The `_created_at` field records when the configuration was instantiated, useful
for cache invalidation and audit trails.

### 4.3 Study Plans (`StudyPlanGenerator`)

The generator translates a certification code and human-readable timeline into a
`StudyPlan` object.

**Timeline parsing**: accepts strings like `"3-months"`, `"12-weeks"`, `"1-year"`.
Regex: `^(\d+)\s*-(month|week|year)s?$`. Multipliers: week=1, month=4, year=52.
Maximum supported timeline: 10 years (520 weeks).

**Domain resolution**: creates weighted `ExamDomain` entries that define
the topic distribution across the study timeline.

**Schedule generation**: distributes topics across weeks according to domain
weights. Each entry is formatted: `"Week {N}: {topic}"`.

**Milestone generation**: creates checkpoints at 25%, 50%, near-end and exam-week.

**Metadata**: includes timeline source, domain weights and estimated session count.

### 4.4 Practice Tests (`QuestionBank`)

The `QuestionBank` generates realistic exam questions using templates.

**Templates**: organised under domain keys (`"cloud"`, `"data"`, `"security"`,
`"development"`, `"devops"`, `"networking"`, `"default"`).
Each template is a format string with placeholders (`{feature}`, `{concept}`,
`{provider}`).

**Placeholder substitution**: glossary maps placeholder names to topic-appropriate
values, e.g. `{provider}` maps to `"AWS"` for cloud topics.

**Option generation**: five distractors are created; 3–5 are selected at random.
The correct answer is indicated by `correct_index`.

**Reproducibility**: a `seed` parameter ensures deterministic output, ideal for
CI pipelines.

**Tagging strategy**: questions are tagged with topic, difficulty and domain
for downstream filtering and analytics.

**History tracking**: `_question_history` logs all generated question IDs for
auditing and deduplication.

### 4.5 Resources (`ResourceCurator`)

The `ResourceCurator` maintains an in-memory catalogue keyed by certification
identifier. Each entry has type, name, estimated hours and optional metadata.

**Type classification**: `course`, `book`, `lab`, `practice_test`, `documentation`,
`video`, `podcast`, `workshop`.

**Recommendation logic**: filters by `min_priority`, returns up to `max_resources`.
Optional `resource_types` filter allows further narrowing.

**Dynamic registration**: `add_resource()` allows runtime injection without
modifying hard-coded data.

**Catalogue discovery**: `get_catalogue()` returns a summary of available resources
by certification.

### 4.6 Progress Tracking (`ProgressTracker`)

Stores the latest progress snapshot per plan ID.

**Completion formula**:

```
completion_percentage = (topics_completed / max(topics_total, 1)) * 60.0
                      + (practice_accuracy * 40.0)
```

Topic completion contributes 60%; practice accuracy contributes 40%. This
weighting ensures that both breadth and depth are rewarded.

**Confidence estimation**: derived from completion percentage scaled by
practice accuracy.

**Weak domain detection**: identifies areas where performance falls below
configurable thresholds.

**Clamping guarantees**:
- `topics_completed >= 0`
- `topics_total >= 1`
- `practice_accuracy ∈ [0.0, 1.0]`
- `hours_studied >= 0.0`
- `current_streak >= 0`

### 4.7 Analytics (`AnalyticsEngine`)

Enriches raw progress metrics:

- **Estimated hours remaining**: proportional to topics remaining, using average
  hours per topic.
- **Learning velocity**: topics per hour and hours per streak day.
- **Recent activities**: from tracker history.
- **Resource ranking**: defaults to ranking by `(6 - priority) + (hours / 10) + (rating / 2)`.
  Caller-supplied `rating_fn` supported.

### 4.8 Scheduling (`ScheduleOptimizer`)

Maps weekly plan entries onto a concrete day-of-week calendar.

**Algorithm**:
1. Validate and deduplicate `available_days`.
2. Iterate schedule entries in plan order.
3. Compute candidate day: `(week_number - 1) % len(available_days)`.
4. Skip days exceeding `max_sessions_per_day`.
5. If no available days remain, fall back to first available day.
6. Track cumulative hours respecting `week_capacity`.
7. Reset `day_session_count` at each new week boundary.
8. Support `session_length_hours` per entry.

### 4.9 Mock Exams (`MockExamSimulator`)

Simulates an exam with realism:

- Draws between 20 and 45 questions (randomised).
- Shuffles question order unless suppressed.
- Auto-scores answers and computes per-domain breakdowns.
- 70 % threshold for passing.
- Score rounded to 4 decimal places.
- Maintains internal exam history for review and trend analysis.

### 4.10 Notes (`StudyNoteGenerator`)

Generate Markdown in three sections:

1. **Key Concepts**: unique domains from the question set.
2. **Recommended Resources**: type + name with hyperlinks and estimated hours.
3. **Practice Questions Summary**: up to 10 questions with options and explanations
   inside `> quote` blocks.

Supports optional persistence to disk.

### 4.11 Strategy (`ExamStrategyAdvisor`)

Time-adaptive advice:

| Band | Days | Focus |
|------|------|-------|
| A | > 60 | Foundation building |
| B | 14 – 60 | Intensive practice |
| C | 1 – 13 | Exam readiness |
| D | <= 0 | Past exam |

Daily recommended hours scale linearly to `study_hours_per_week / 7`.
Additional metadata includes rest days before exam and exam readiness status.

### 4.12 Competency Assessment (`CompetencyAssessor`)

Evaluates user performance across domains:

- Computes per-domain accuracy from question results.
- Identifies strong and weak areas based on configurable thresholds.
- Suggests difficulty adjustments based on recent accuracy performance.
- Generates recommended focus topics for targeted improvement.

**Difficulty mapping**:
- Accuracy >= 85%: suggest next higher difficulty level.
- Accuracy <= 40%: suggest next lower difficulty level.
- Otherwise: maintain current difficulty.

### 4.13 Session Tracking (`SessionManager`)

Manages study sessions:

- Starts and ends timed sessions with automatic duration computation.
- Tracks topics covered and questions answered per session.
- Supports concurrent plan tracking with one active session per plan.
- Enables session history review and duration analysis.
- Enforces single active session per plan to prevent state conflicts.

### 4.14 Notifications (`NotificationService`)

Optional notification infrastructure:

- SMTP-based email delivery.
- Milestone reminder templates.
- Silent failure with logging when disabled or misconfigured.
- Full notification history for audit and troubleshooting.

### 4.15 Template Engine (`TemplateEngine`)

Advanced template processing:

- Supports custom question template registration by domain.
- Enables runtime extension without modifying core question bank.
- Provides flexible placeholder substitution.
- Allows discovery of available domains.

### 4.16 Route Management (`CertificationRouteManager`)

Maintains certification route metadata:

- Exam format, duration, passing score and registration fee.
- Domain weights and topic definitions.
- Prerequisites and recommended experience.
- Validity periods for re-certification.
- Registration of new routes at runtime.

### 4.17 Validation Utils (`ValidationUtils`)

Centralised validation utilities:

- `validate_plan_id()`: Ensures non-empty, alphanumeric ID.
- `validate_timeline()`: Parses and validates timeline strings.
- `validate_count()`: Clamps to min/max bounds.
- `validate_accuracy()`: Clamps to [0.0, 1.0].
- `validate_non_negative()`: Ensures non-negative numeric values.

## 5. Data Models Reference

All models are `@dataclass` with `to_dict()` serialisers.

### 5.1 `StudyPlan`
- `plan_id: str` — unique identifier
- `certification: str` — certification code
- `timeline_weeks: int` — parsed timeline
- `topic: str` — original topic
- `difficulty: DifficultyLevel` — effective difficulty
- `weekly_hours: float` — hours per week
- `total_hours: float` — aggregate hours
- `domains: List[str]` — domain names
- `schedule: List[str]` — weekly activity strings
- `milestones: List[str]` — checkpoint strings
- `created_at: str` / `updated_at: str` — timestamps
- `metadata: Dict[str, Any]` — extended attributes

### 5.2 `PracticeQuestion`
- `question_id: str` — topic-q001 format
- `topic: str` — source topic
- `domain: str` — mapped domain
- `difficulty: DifficultyLevel` — question difficulty
- `text: str` — rendered question
- `options: List[str]` — answer choices
- `correct_index: int` — zero-based correct answer
- `explanation: str` — rationale text
- `tags: List[str]` — metadata labels
- `created_at: str` — generation timestamp

### 5.3 `ResourceRecommendation`
- `resource_id: str` — unique id
- `resource_type: str` — classification
- `name: str` — display name
- `url: Optional[str]` — link
- `description: str` — free-text
- `estimated_hours: float` — effort estimate
- `priority: int` — ranking value
- `tags: List[str]` — classification labels
- `rating: float` — user rating
- `review_count: int` — number of reviews

### 5.4 `ProgressMetric`
- `plan_id: str` — associated plan
- `certification: str` — target cert
- `completion_percentage: float` — weighted score ∈ [0, 100]
- `topics_completed: int` — finished topics
- `topics_total: int` — total topics
- `practice_questions_answered: int` — answered count
- `practice_accuracy: float` — correct ratio ∈ [0.0, 1.0]
- `hours_studied: float` — total logged time
- `current_streak: int` — consecutive study days
- `last_activity: str` — ISO timestamp
- `confidence_score: float` — estimated exam readiness
- `weak_domains: List[str]` — areas needing improvement

### 5.5 `ExamDomain`, `CertificationRoute`, `EnrollmentRecord`
Supporting models for domain definitions, route metadata and user enrolment
state respectively.

### 5.6 Supporting Models

- `StudySession`: Tracks individual study sessions with timing and performance.
- `NotificationRecord`: Logs sent notifications with delivery status.
- `CompetencyAssessment`: Evaluates domain-specific competency scores.

## 6. Data Flow Diagrams

### 6.1 Plan Creation

```
User: create_study_plan("aws-saa", "3-months")
  └─► API Layer validates & clamps inputs
      └─► ValidationUtils.validate_timeline() → 12 weeks
          └─► StudyPlanGenerator.build_plan()
              ├─► _resolve_domains() → 4 ExamDomain entries
              ├─► _generate_schedule()    → 12 week entries
              ├─► _generate_milestones()  → 4 milestones
              └─► StudyPlan model constructed
                  └─► Stored in agent._plans list
                      └─► to_dict() returned to caller
```

### 6.2 Practice Test Generation

```
User: generate_practice_test("aws-saa", count=15, seed=42)
  └─► API Layer clamps count to [5, 50]
      └─► QuestionBank.generate()
          ├─► _pick_templates("aws-saa") → cloud templates
          ├─► Loop 15 times
          │   ├─► _fill_template()  → rendered question
          │   ├─► _make_options()   → 3-5 distractors
          │   ├─► _guess_domain()   → "Cloud"
          │   ├─► _default_explanation() → rationale text
          │   └─► Build PracticeQuestion
          └─► Log to _question_history
              └─► to_dict() each and return
```

### 6.3 Progress Tracking

```
User: track_progress(plan_id, topics_completed=4, ...)
  └─► API Layer validates plan_id, clamps numerics
      └─► ValidationUtils.validate_accuracy(practice_accuracy)
          └─► ProgressTracker.update()
              ├─► _compute_completion() → weighted percentage
              ├─► _estimate_confidence() → confidence score
              ├─► _identify_weak_domains() → weak areas
              └─► ProgressMetric stored in _records[plan_id]
                  └─► Log to _history_log
                      └─► to_dict() returned
```

### 6.4 Analytics

```
User: get_progress(plan_id)
  └─► ProgressTracker.get(plan_id) → ProgressMetric?
      ├─► If None → return {"status": "not_found"}
      └─► AnalyticsEngine.summary_for(plan_id)
          ├─► Fetch metric from tracker
          ├─► Compute remaining topics / hours
          ├─► Compute hours_per_topic
          ├─► Fetch learning velocity
          └─► Return enriched dictionary
```

### 6.5 Mock Exam

```
User: run_mock_exam("aws-saa", count=20, time_limit_minutes=60)
  └─► QuestionBank.generate() → 20 questions
      └─► MockExamSimulator.run()
          ├─► Shuffle pool (if enabled)
          ├─► Draw 20-45 questions
          ├─► Simulate random answers for each
          ├─► Score & accumulate per-domain stats
          ├─► Compute overall score
          ├─► Determine pass/fail (70% threshold)
          └─► Return {score, pass, breakdown, ...}
              └─► Append to _exam_history
```

### 6.6 Resource Curation

```
User: recommend_resources("aws-saa", max_resources=5, resource_types=["course", "book"])
  └─► ResourceCurator.recommend()
      ├─► Lookup RESOURCE_DATABASE["aws-saa"] or fallback to "default"
      ├─► Filter by min_priority
      ├─► Filter by resource_types (if specified)
      └─► Convert to ResourceRecommendation list
          └─► to_dict() each and return
```

### 6.7 Session Tracking

```
User: start_study_session(plan_id, topics=["EC2", "S3"])
  └─► ValidationUtils.validate_plan_id(plan_id)
      └─► SessionManager.start_session()
          ├─► Check no active session for plan
          ├─► Generate session_id
          └─► Create StudySession, return to_dict()

User: end_study_session(plan_id, questions_answered=15, correct_answers=12)
  └─► SessionManager.end_session()
      ├─► Lookup active session_id
      ├─► Compute duration from ISO timestamps
      ├─► Record questions and correct answers
      └─► Return completed session dict
```

### 6.8 Notifications

```
User: send_milestone_reminder(recipient, "aws-saa", "Week 4 check")
  └─► NotificationService.send_milestone_reminder()
      ├─► Check enable_notifications and smtp_host
      ├─► Build MIMEText message
      ├─► Connect to SMTP server
      ├─► Authenticate and send
      └─► Record NotificationRecord in _sent history
```

### 6.9 Competency Assessment

```
User: assess_competency(q_list, user_answers)
  └─► Convert dict questions to PracticeQuestion objects
      └─► CompetencyAssessor.assess_from_questions()
          ├─► Group by domain
          ├─► Compute per-domain accuracy
          ├─► Sort weak domains
          └─► Return CompetencyAssessment
              └─► to_dict()
```

### 6.10 Full Backup Export

```
User: export_full_backup("./backup.json")
  └─► Serialise:
      ├─► agent._plans → list of StudyPlan dicts
      ├─► progress_tracker._records → dict of ProgressMetric dicts
      ├─► session_manager._sessions → list of StudySession dicts
      ├─► mock_simulator.get_history() → list of exam result dicts
      ├─► notification_service.get_sent_history() → list of notification dicts
      └─► Write to JSON file with exported_at timestamp
```

## 7. Extended Configuration Reference

### 7.1 Default Settings

```python
Config(
    default_domain=None,
    default_difficulty=DifficultyLevel.INTERMEDIATE,
    study_hours_per_week=10,
    retention_days=90,
    storage_path="./certification_prep_data",
    verbose=False,
    enable_notifications=False,
    smtp_host=None,
    smtp_port=587,
    smtp_user=None,
    smtp_password=None,
    notification_email=None,
    session_tracking=True,
    competency_assessment=True,
)
```

### 7.2 Example YAML Configuration

```yaml
# certification_prep_config.yaml
agent: certification-prep
default_domain: cloud
default_difficulty: intermediate
study_hours_per_week: 12
retention_days: 90
storage_path: ./certification_prep_data
verbose: false
question_defaults:
  min_questions: 5
  max_questions: 50
  default_count: 10
exam_defaults:
  min_questions: 20
  max_questions: 45
  pass_threshold: 0.70
  time_limit_minutes: 60
notifications:
  enabled: false
  smtp_host: smtp.example.com
  smtp_port: 587
  recipient: learner@example.com
  smtp_user: notifier@example.com
session_tracking: true
competency_assessment: true
```

### 7.3 Environment Variable Overrides

| Variable | Purpose | Fallback |
|----------|---------|----------|
| `CERT_PREP_HOURS_PER_WEEK` | Override study hours | `10` |
| `CERT_PREP_STORAGE_PATH` | Override persistence dir | `./certification_prep_data` |
| `CERT_PREP_VERBOSE` | Enable verbose logging | `false` |
| `CERT_PREP_SMTP_HOST` | SMTP hostname | — |
| `CERT_PREP_SMTP_PORT` | SMTP port | `587` |
| `CERT_PREP_SMTP_USER` | SMTP username | — |
| `CERT_PREP_SMTP_PASSWORD` | SMTP password | — |
| `CERT_PREP_RECIPIENT` | Notification recipient | — |
| `CERT_PREP_NOTIFICATIONS` | Enable notifications | `false` |

### 7.4 Configuration Loading Pattern

```python
import os

def load_config_from_env() -> Config:
    return Config(
        study_hours_per_week=int(os.getenv("CERT_PREP_HOURS_PER_WEEK", "10")),
        storage_path=os.getenv("CERT_PREP_STORAGE_PATH"),
        verbose=os.getenv("CERT_PREP_VERBOSE", "false").lower() == "true",
        enable_notifications=os.getenv("CERT_PREP_NOTIFICATIONS", "false").lower() == "true",
        smtp_host=os.getenv("CERT_PREP_SMTP_HOST"),
        smtp_port=int(os.getenv("CERT_PREP_SMTP_PORT", "587")),
        notification_email=os.getenv("CERT_PREP_RECIPIENT"),
    )
```

### 7.5 Configuration Immutability Considerations

The `Config` object is mutable by default. For thread-safe or multi-instance
scenarios, consider creating a frozen dataclass wrapper:

```python
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class FrozenConfig:
    study_hours_per_week: int = 10
    default_difficulty: str = "intermediate"
    # ... other fields

config = FrozenConfig()
agent = CertificationPrepAgent(config=config)
```

## 8. Error Handling Strategy

### 8.1 Error Categories

| Category | Examples | Strategy |
|----------|----------|----------|
| User Input Errors | Invalid timeline string, empty plan_id | Raise `ValueError` with clear message |
| Validation Errors | Out-of-range accuracy, negative hours | Clamp or raise with descriptive message |
| Missing State | Plan not found in active list | Return `None` or raise `KeyError` depending on caller expectation |
| File System | Missing persistence file, unwritable directory | Raise `FileNotFoundError` / `OSError` |
| Type Mismatch | Non-existent difficulty level passed | Validate and raise `ValueError` |
| Logic Errors | Negative topics, accuracy > 1.0 | Clamp with validation utilities |
| Runtime Errors | SMTP failure, disk full | Log and fail gracefully |
| Concurrent Access | Session already active | Raise `RuntimeError` |

### 8.2 Detailed Error Matrix

| Scenario | Detection Point | Exception | Consumer Action |
|----------|-----------------|-----------|-----------------|
| Invalid timeline `"foobar"` | `_parse_timeline()` regex | `ValueError: Unable to parse timeline string: 'foobar'` | Use `<number>-<unit>` format |
| Invalid timeline value (e.g. `0-weeks`) | `validate_timeline()` | `ValueError: Timeline value must be a positive integer` | Use positive integer |
| Timeline > 10 years | `validate_timeline()` | `ValueError: Timeline exceeds maximum of 10 years (520 weeks)` | Reduce timeline |
| Plan ID `""` passed | `validate_plan_id()` check | `ValueError: plan_id must be a non-empty string` | Provide valid plan ID |
| Plan ID with special chars | `validate_plan_id()` regex | `ValueError: plan_id must contain only alphanumeric, underscore or hyphen characters` | Sanitise plan ID |
| Plan ID not in store | `get_plan()` scan | Returns `None` (soft) or `KeyError` (hard) | Verify with `get_plans()` first |
| File missing on load | `Path.is_file()` | `FileNotFoundError` | Confirm file path |
| JSON parse error | `json.loads()` | `json.JSONDecodeError` | Validate JSON format |
| File not a JSON array | Type check on load | `ValueError: Expected a JSON array of plan objects` | Fix file contents |
| Negative topics completed | Clamping in API layer | None (clamped to 0) | No action needed |
| Accuracy > 1.0 | `validate_accuracy()` | None (clamped to 1.0) | No action needed |
| Accuracy not numeric | `validate_accuracy()` | `TypeError: accuracy must be a float` | Pass valid float |
| Question count > 50 | `validate_count()` | `ValueError: count must be between 5 and 50` | Adjust count |
| Count not integer | `validate_count()` | `TypeError: count must be an integer` | Pass integer |
| Notes missing | Directory issue | `OSError` / `PermissionError` | Ensure parent dirs writable |
| Exam always fails | Random + tight limit |— (soft, informational) | Increase count or parameterise |
| Session already active | `start_session()` check | `RuntimeError: Session already active for plan {plan_id}` | End previous session first |
| SMTP connection failure | `smtplib.SMTP()` | `smtplib.SMTPException` | Verify SMTP credentials/host |
| Unknown certification route | `get_route()` lookup | Returns `None` | Use `list_certification_routes()` |
| Import resource file missing | `Path.is_file()` | `FileNotFoundError` | Verify file path |
| Import data not a list | Type check | `ValueError: Expected a JSON array of resource objects` | Fix JSON format |

### 8.3 Error Response Patterns

- **User errors**: Clear, friendly message strings.
- **Programmer errors**: Explicit exceptions with type annotations.
- **Recoverable errors**: Fallback values, no exception.
- **Async wrappers**: Propagate errors to executor future; caller handles.
- **Logged errors**: All unexpected exceptions logged at `ERROR` level before propagation.

### 8.4 Logging Strategy

When `verbose=True` or `logging.basicConfig(level=logging.INFO)` is set:

- **INFO level**: Agent initialisation, plan creation, milestone events, session lifecycle.
- **DEBUG level**: Template selection, resource lookup, session details, timing.
- **WARNING level**: Clamping of out-of-range inputs, deprecated parameters.
- **ERROR level**: File I/O failures, SMTP errors, malformed inputs, unhandled exceptions.

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
```

## 9. Performance Characteristics

### 9.1 Complexity Analysis

| Operation | Time Complexity | Notes |
|-----------|---------------|-------|
| `create_study_plan()` | O(D × W) | D = domains, W = timeline weeks |
| `generate_practice_test()` | O(N) | N = question count |
| `batch_generate_questions()` | O(T × N) | T = topics, N = count per topic |
| `track_progress()` | O(1) | Dictionary insertion in ProgressTracker |
| `recommend_resources()` | O(R) | R = resources for cert |
| `optimize_schedule()` | O(E) | E = schedule entries |
| `run_mock_exam()` | O(Q) | Q = exam questions |
| `export_study_notes()` | O(Q + R) | Q = questions, R = resources |
| `export_full_backup()` | O(P + S + H + N) | P = plans, S = sessions, H = history, N = notifications |
| `assess_competency()` | O(Q) | Q = question count |

### 9.2 Space Complexity

| Structure | Space |
|-----------|-------|
| `StudyPlan` | O(W + M) — W schedule entries, M milestones |
| `List[PracticeQuestion]` | O(N) — N questions |
| `ProgressTracker._records` | O(P) — P unique plan IDs |
| `ResourceCurator.RESOURCE_DATABASE` | O(R) — R total resource entries |
| `MockExamSimulator._exam_history` | O(E) — E simulated exams |
| `SessionManager._sessions` | O(S) — S recorded sessions |
| `QuestionBank._question_history` | O(Q) — Q total questions generated |

### 9.3 Benchmark Results (approximate, no I/O)

| Scenario | Approximate Time |
|----------|-----------------|
| Single plan generation | < 1 ms |
| 100-question batch | ~5 ms |
| Progress update | < 1 ms |
| Schedule optimisation (12 weeks) | ~2 ms |
| Mock exam (40 questions) | < 1 ms |
| Study notes generation | ~3 ms |
| Full backup export | ~1 ms |
| Analytics summary | < 1 ms |
| Competency assessment (20 questions) | < 1 ms |
| Route lookup | < 0.1 ms |
| Batch questions (10 topics × 10 qty) | ~40 ms |
| JSON persistence (100 plans) | ~5 ms |
| Async practice test (10 questions) | ~2 ms overhead |

## 10. Testing Strategy

### 10.1 Unit Test Coverage

| Test Suite | Coverage Target | Key Tests |
|-----------|-----------------|-----------|
| `test_config.py` | 100 % | Instantiation, defaults, serialisation, edge values |
| `test_models.py` | 100 % | Field types, `to_dict()` round-trip, defaults |
| `test_validation_utils.py` | 100 % | All validation methods, edge cases, error messages |
| `test_study_plan_generator.py` | 95 % | Timeline parsing, domain resolution, milestones, metadata |
| `test_question_bank.py` | 95 % | Template selection, option generation, seeding, history |
| `test_resource_curator.py` | 90 % | Recommendation filtering, dynamic addition, catalogue |
| `test_progress_tracker.py` | 95 % | Completion formula, clamping, confidence, weak domains |
| `test_analytics_engine.py` | 90 % | Summary enrichment, ranking, velocity |
| `test_schedule_optimizer.py` | 90 % | Day selection, unavailable handling, per-day limits |
| `test_mock_exam_simulator.py` | 90 % | Scoring, pass threshold, topic breakdown, history |
| `test_study_note_generator.py` | 85 % | Markdown structure, file persistence |
| `test_exam_strategy_advisor.py` | 95 % | Time bands, action generation, readiness |
| `test_competency_assessor.py` | 90 % | Domain scoring, difficulty suggestion |
| `test_session_manager.py` | 90 % | Session lifecycle, tracking, history |
| `test_route_manager.py` | 90 % | Route lookup, registration, all_routes |
| `test_notification_service.py` | 85 % | Email sending (mocked), history |
| `test_template_engine.py` | 90 % | Registration, rendering, placeholder substitution |
| `test_api_integration.py` | 95 % | End-to-end workflow chains |

### 10.2 Integration Test Scenarios

1. **End-to-end pipeline**: plan → questions → progress → analytics.
2. **Async wrappers**: event-loop compatibility and executor offloading.
3. **JSON round-trip**: `save_plans_to_path()` then `load_plans_from_path()`.
4. **CLI invocation**: `argparse` flag parsing and demo execution.
5. **Competency flow**: questions + user answers → assessment → difficulty suggestion.
6. **Session tracking flow**: start → end → history review.
7. **Backup export**: comprehensive state preservation and restoration.
8. **Resource import**: loading external resource definitions.
9. **Template registration**: custom template integration.
10. **Notification flow**: milestone reminder generation and dispatch.

### 10.3 CI/CD Pipeline

```yaml
# .github/workflows/test.yml (example)
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.10, 3.11, 3.12]

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Lint
        run: ruff check agent.py --select E,F,W --max-line-length 120

      - name: Type check
        run: mypy agent.py --strict --ignore-missing-imports

      - name: Unit tests
        run: pytest tests/ -v --tb=short --cov=agent --cov-report=term-missing

      - name: Integration tests
        run: pytest tests/test_api_integration.py -v --tb=short
```

### 10.4 Test Data Generation

```python
import random

def generate_test_plan(agent, cert: str = "test-cert", weeks: int = 4) -> Dict[str, Any]:
    return agent.create_study_plan(cert, f"{weeks}-weeks")

def generate_test_questions(agent, topic: str, count: int = 10, seed: int = 12345) -> List[Dict]:
    random.seed(seed)
    return agent.generate_practice_test(topic, count=count, seed=seed)

def generate_full_test_scenario(agent, cert: str = "aws-saa", weeks: int = 4):
    plan = generate_test_plan(agent, cert, weeks)
    pid = plan["plan_id"]
    questions = generate_test_questions(agent, cert, count=20)
    agent.track_progress(
        pid, topics_completed=2, topics_total=weeks*3,
        practice_accuracy=0.7, hours_studied=5.0, current_streak=2
    )
    return plan, questions
```

## 11. Security Architecture

### 11.1 Authentication

Not built-in. Consumers must enforce authentication at the application boundary
(e.g. API gateway, reverse proxy, OAuth in a web framework).

### 11.2 Authorization

No RBAC within the agent. All plans and metrics are global within a process.
Multi-tenant isolation requires a wrapper that partitions state by user ID.

### 11.3 Data Protection

- No secrets stored in state.
- JSON files should be permission-restricted (chmod 600 recommended).
- Inputs validated via regex and clamped via `max()` / `min()`.
- SMTP passwords passed in `Config` are never logged or serialised in JSON exports.
- Notification bodies are not persisted to disk by default.
- No PII is collected or stored unless explicitly provided by the user.

### 11.4 Audit Recommendations

1. Enable verbose logging only in development.
2. Log plan creation with timestamps.
3. Rotate externally provided API keys.
4. Review JSON backup files for sensitive data before sharing.
5. Use environment variables for SMTP credentials, not hard-coded values.
6. Restrict filesystem access to designated data directories.

### 11.5 Threat Model

| Threat | Mitigation |
|--------|-----------|
| Path traversal | `Path` objects with `write_text()` restrict to intended paths |
| Injection via timeline | Regex validation rejects malformed input |
| Resource exhaustion | Count clamping, week limits, memory bounds |
| Information leakage | Verbose mode off by default; no PII in logs |
| Dependency confusion | Zero external dependencies reduces supply-chain risk |
| Config injection | Env vars validated before use; secrets not in JSON payloads |
| Session fixation | Unique session IDs with timestamp seeding |
| Replay attacks | Session validation with existing active session checks |
| Data tampering | JSON backups are plain text; use transport encryption for sharing |

## 12. Deployment Options

### 12.1 CLI

```
python agents/certification-prep/agent.py demo
python agents/certification-prep/agent.py plan --certification aws-saa --timeline 3-months
python agents/certification-prep/agent.py route --certification ccna
```

### 12.2 Library

```python
from agents.certification-prep.agent import CertificationPrepAgent, Config

agent = CertificationPrepAgent(config=Config(study_hours_per_week=15))
```

### 12.3 Web (FastAPI)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.certification-prep.agent import CertificationPrepAgent, Config

app = FastAPI()
agent = CertificationPrepAgent(config=Config(study_hours_per_week=12))

class PlanRequest(BaseModel):
    certification: str
    timeline: str
    topic: str | None = None

@app.post("/plan")
def post_plan(req: PlanRequest):
    try:
        return agent.create_study_plan(req.certification, req.timeline, req.topic)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.get("/progress/{plan_id}")
def get_progress(plan_id: str):
    result = agent.get_progress(plan_id)
    if result.get("status") == "not_found":
        raise HTTPException(status_code=404, detail="Plan not found")
    return result

@app.post("/mock-exam/{topic}")
def run_mock(topic: str, count: int = 20):
    return agent.run_mock_exam(topic, count=count)
```

### 12.4 Flask

```python
from flask import Flask, jsonify, request
from agents.certification-prep.agent import CertificationPrepAgent, Config

app = Flask(__name__)
agent = CertificationPrepAgent(config=Config(study_hours_per_week=14))

@app.route("/plan", methods=["POST"])
def create_plan():
    data = request.get_json()
    try:
        return jsonify(agent.create_study_plan(data["certification"], data["timeline"]))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

@app.route("/plans", methods=["GET"])
def list_plans():
    return jsonify(agent.get_plans())
```

### 12.5 Container (Docker)

```dockerfile
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -e .
VOLUME ["/app/data"]
ENTRYPOINT ["python", "agents/certification-prep/agent.py", "demo"]
```

### 12.6 Serverless (AWS Lambda)

```python
def lambda_handler(event, context):
    from agents.certification-prep.agent import CertificationPrepAgent, Config

    agent = CertificationPrepAgent(config=Config(
        study_hours_per_week=event.get("hours", 10)
    ))
    cert = event.get("certification", "aws-saa")
    timeline = event.get("timeline", "3-months")

    plan = agent.create_study_plan(cert, timeline)
    questions = agent.generate_practice_test(cert, count=10)

    return {
        "statusCode": 200,
        "body": {"plan": plan, "questions": questions},
    }
```

### 12.7 Google Cloud Function

```python
def certification_prep(request):
    request_json = request.get_json(silent=True)
    from agents.certification-prep.agent import CertificationPrepAgent
    agent = CertificationPrepAgent()
    cert = request_json.get("certification", "gcp-data") if request_json else "gcp-data"
    return agent.create_study_plan(cert, "3-months")
```

### 12.8 Poetry Package

```toml
# pyproject.toml
[project]
name = "certification-prep-agent"
version = "1.0.0"
requires-python = ">=3.10"
dependencies = []

[project.scripts]
cert-prep = "agents.certification-prep.agent:main"
```

## 13. Operational Runbook

### 13.1 Health Checks

```python
status = agent.get_status()
assert status["ready"] is True
assert len(status["components"]) > 0
assert status["plans"] >= 0
```

### 13.2 Routine Operations

| Task | Action |
|------|--------|
| Check health | `agent.get_status()` |
| List plans | `agent.get_plans()` |
| Persist plans | `agent.save_plans_to_path("backup.json")` |
| Restore plans | `agent.load_plans_from_path("backup.json")` |
| Export plan JSON | `agent.to_json(plan_id)` |
| Full backup | `agent.export_full_backup("full_backup.json")` |
| Run demo | `python agent.py demo` |
| Show agent status | `python agent.py status` |
| Create plan via CLI | `python agent.py plan --certification aws-saa --timeline 3-months` |
| Show certification route | `python agent.py route --certification ccna` |
| Suggest difficulty | `python agent.py suggest-difficulty --current intermediate --accuracy 0.72` |

### 13.3 Backup and Restore

```python
# Full backup
agent.export_full_backup("./full_backup.json")

# Partial restore (load only plans)
agent2 = CertificationPrepAgent()
agent2.load_plans_from_path("./plans.json")

# Restore progress only
for pid, metric in backup["progress"].items():
    agent2._progress_tracker._records[pid] = metric
```

### 13.4 Monitoring

Recommended metrics to expose:

- Number of active plans.
- Average completion percentage across all plans.
- Count of notifications sent.
- Exam pass rate distribution.
- Most viewed certification routes.
- Average session duration.
- Current study streak distribution.

### 13.5 Maintenance Procedures

| Task | Frequency | Procedure |
|------|-----------|-----------|
| Review logs | Weekly | Check ERROR and WARNING entries |
| Validate backups | Monthly | Load and re-save all backups |
| Update resource catalogues | Monthly | Review and add new resources |
| Audit session data | Monthly | Verify session count and durations |
| Review competency thresholds | Quarterly | Adjust weak domain thresholds if needed |
| Check Python compatibility | Quarterly | Test with new Python releases |
| Security patch review | As needed | Monitor standard library CVEs |

### 13.6 Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ValueError: Unable to parse timeline string` | Timeline wrong | Use `"3-months"` |
| Plan not found | Wrong plan_id | Verify via `get_plans()` |
| Zero questions | Count out of bounds | Set 5 ≤ count ≤ 50 |
| Notes missing | Directory issue | Ensure parent dirs writable |
| Exam always fails | Random + tight limit | Increase count/limit |
| `FileNotFoundError` on load | Path incorrect | Verify absolute/relative path |
| `RuntimeError` on session start | Session already active | End previous session or check active sessions |
| SMTP delivery failure | Host/credentials invalid | Verify SMTP settings and TLS access |
| `KeyError` when retrieving plan | plan_id not found | Check plan was created and not deleted |
| JSON decode error | Malformed file | Validate JSON with a linter |
| Import error on `agent.py` | Missing `__init__.py` | Ensure package has `__init__.py` |
| Slow response times | Large plan count | Consider pagination or lazy loading |

## 14. Known Limitations

- Template-based questions; no LLM-backed open-ended generation.
- Static resource catalogue unless dynamically extended.
- Volatile in-memory state; explicit JSON persistence only.
- No built-in authentication or multi-tenancy.
- `CertificationDomain` enum defined but not used for production routing.
- No built-in scheduling calendar integration (e.g. iCal, Google Calendar).
- Study notes generation currently limited to first 10 questions for detail.
- Notification system requires manual SMTP configuration.
- No WebSocket or realtime event streaming.
- No persisted exam history beyond current process lifetime.

## 15. Future Work

- LLM-backed prompt pipeline for dynamic question generation.
- Vector-backed related-question retrieval (e.g., FAISS, Chroma).
- SQLite / PostgreSQL pluggable persistence.
- Collaborative multi-user plans with conflict resolution.
- Email, Slack, Teams notification adapters.
- Interactive timeline visualisation.
- Adaptive pacing based on learning velocity.
- iCal / Google Calendar schedule export.
- Dark-mode Markdown themes for study notes.
- Recommendation engine powered by collaborative filtering.
- Integration with flashcard tools (Anki, Quizlet export).
- Multi-modal content (audio summary, video link injection).
- Offline-first mobile companion app.
- Web dashboard for study analytics.

## 16. Glossary

| Term | Definition |
|------|-----------|
| **Plan ID** | Unique string identifier for a study plan instance. |
| **Domain** | A weighted exam area. |
| **Milestone** | Key checkpoint date inside a study plan. |
| **Practice Accuracy** | Ratio of correct to answered questions ∈ [0.0, 1.0]. |
| **Session Length** | Single contiguous study block duration in hours. |
| **Streak** | Consecutive days of study activity. |
| **Confidence Score** | Value in [0.0, 1.0] indicating estimated exam readiness. |
| **Readiness Score** | Composite metric combining completion, accuracy and streak. |
| **Competency Assessment** | Evaluation of domain-specific knowledge gaps. |
| **Learning Velocity** | Topics per hour and hours per week metrics. |
| **Topic Weights** | Proportional allocation of study time across domains. |
| **Seed** | Random initialiser for deterministic question generation. |
| **Persistence** | JSON-based storage for plan and progress durability. |
| **Resource Type** | Classification of learning material (course, book, lab, etc.). |
| **Template** | Format string with placeholders for question generation. |
| **Route** | Certification route metadata including domains and scoring details. |

## 17. Appendix: Code to Diagram Mapping

| Component | File Location | Line Approx. |
|-----------|---------------|---------------|
| `Config` | `agent.py` | 52 |
| `ValidationUtils` | `agent.py` | 130 |
| `StudyPlan` | `agent.py` | 194 |
| `PracticeQuestion` | `agent.py` | 220 |
| `ResourceRecommendation` | `agent.py` | 240 |
| `ProgressMetric` | `agent.py` | 255 |
| `ExamDomain` | `agent.py` | 272 |
| `CertificationRoute` | `agent.py` | 280 |
| `EnrollmentRecord` | `agent.py` | 301 |
| `StudySession` | `agent.py` | 313 |
| `NotificationRecord` | `agent.py` | 325 |
| `CompetencyAssessment` | `agent.py` | 334 |
| `StudyPlanGenerator` | `agent.py` | 401 |
| `QuestionBank` | `agent.py` | 517 |
| `ResourceCurator` | `agent.py` | 672 |
| `ProgressTracker` | `agent.py` | 801 |
| `AnalyticsEngine` | `agent.py` | 860 |
| `ScheduleOptimizer` | `agent.py` | 904 |
| `MockExamSimulator` | `agent.py` | 1000 |
| `StudyNoteGenerator` | `agent.py` | 1057 |
| `ExamStrategyAdvisor` | `agent.py` | 1102 |
| `CompetencyAssessor` | `agent.py` | 1150 |
| `SessionManager` | `agent.py` | 1198 |
| `NotificationService` | `agent.py` | 1237 |
| `TemplateEngine` | `agent.py` | 1278 |
| `CertificationRouteManager` | `agent.py` | 1292 |
| `CertificationPrepAgent` | `agent.py` | 1321 |
| `main()` CLI | `agent.py` | 1626 |

## 18. Appendix: Directory Structure

```
certification-prep/
├── agent.py              # Public API and all service-layer classes
├── GROK.md               # Agent instructions and detailed usage guide
├── ARCHITECTURE.md       # System architecture, data flows and design decisions
└── README.md             # End-user documentation and quick-start guide

tests/                    # Unit and integration tests
├── test_config.py
├── test_models.py
├── test_validation_utils.py
├── test_study_plan_generator.py
├── test_question_bank.py
├── test_resource_curator.py
├── test_progress_tracker.py
├── test_analytics_engine.py
├── test_schedule_optimizer.py
├── test_mock_exam_simulator.py
├── test_study_note_generator.py
├── test_exam_strategy_advisor.py
├── test_competency_assessor.py
├── test_session_manager.py
├── test_route_manager.py
├── test_notification_service.py
├── test_template_engine.py
└── test_api_integration.py

data/                     # Persistence directory
├── plans.json
├── progress.json
└── backup.json

scripts/                  # Operational scripts
├── benchmark.py
├── import_resources.py
└── validate_backup.py
```

## 19. Appendix: Design Decision Records

### ADR-001: Single-File Architecture
**Decision**: All classes live in a single `agent.py` file.
**Rationale**: Maximises discoverability and reduces import complexity for
library consumers. Trade-off: file size grows, mitigated by clear section markers.

### ADR-002: In-Memory State with Opt-In JSON
**Decision**: No database dependency; in-memory state with JSON persistence helpers.
**Rationale**: Zero-dependency goal; JSON is human-readable and portable.
Trade-off: State is volatile, requires explicit persistence.

### ADR-003: Template-Based Questions
**Decision**: Questions generated from format strings, not LLM calls.
**Rationale**: Deterministic output, zero API costs, offline-capable.
Trade-off: Question variety limited to template author imagination.

### ADR-004: Sync API with Async Wrappers
**Decision**: Core methods are synchronous; async versions use `loop.run_in_executor()`.
**Rationale**: CPU-bound work benefits from thread offloading in event loops.
Trade-off: Slight overhead from thread pool switching.

### ADR-005: ValidationUtils as Static Class
**Decision**: Validation helpers grouped in a static utility class.
**Rationale**: Pure functions with no state; easy to test and reuse.
Trade-off: Less OOP-friendly than instance methods.

## 20. Appendix: Version History

### 1.0.0 (2026-06-04)
- Initial modular release with `CertificationPrepAgent` and seventeen service
  components.
- Template-based question generation with seed support.
- Progress tracking with weighted completion formula.
- Resource curation with dynamic registration.
- JSON serialisation, async wrappers and extensive CLI subcommands.
- Competency assessment, session tracking and notification service.
- Certification route management and template engine.
- Comprehensive documentation across `GROK.md`, `README.md` and
  `ARCHITECTURE.md`.
