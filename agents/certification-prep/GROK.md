# Certification Prep Agent

## Overview

The **Certification Prep Agent** is a comprehensive Python-based autonomous
assistant designed to help learners prepare for technical certifications through
structured study plans, realistic practice tests, adaptive progress tracking,
curated resource recommendations and tailored exam-day strategies. It is built
as an in-process library that exposes a synchronous API with async wrappers,
making it suitable for CLI tools, web frameworks, notebooks and automation pipelines.

The agent is designed around principles of testability, extensibility and
separation of concerns. Rather than being a monolithic object, it is composed of
  specialised service-layer collaborators — plan generators, question banks,
resource curators, progress trackers, analytics engines, schedule optimisers,
mock exam simulators, study note generators, strategy advisors, competency
assessors, session managers and notification services — each with
a single, well-defined responsibility.

Because the agent holds no external state by default, it is safe to embed in
serverless functions, containerised microservices or long-running desktop
applications. Persistence is opt-in, via JSON file helpers or by the integrating
application storing returned dictionaries.

### Philosophy

The agent follows a **configurable-by-default** philosophy. All behaviour that
might vary between environments is controlled by the `Config` dataclass. No
magic constants are buried in business logic; every threshold and default is
named and documented.

The agent is **deterministic-by-design** when a seed is provided, making it
suitable for reproducible test fixtures and CI/CD pipelines.

The agent is **dependency-free**, relying only on the Python standard library.
This minimises supply-chain risk and simplifies deployment in restricted environments.

## Directory Layout

```
certification-prep/
├── agent.py              # Public API and all service-layer classes
├── GROK.md               # Agent instructions and detailed usage guide
├── ARCHITECTURE.md       # System architecture, data flows and design decisions
└── README.md             # End-user documentation and quick-start guide
```

## Agent Identity

| Field | Value |
|-------|-------|
| Name | `CertificationPrepAgent` |
| Version | 1.0.0 |
| Primary Domain | Education / Technology Certification Preparation |
| Execution Model | Synchronous with async wrappers |
| State Model | In-memory lists and dictionaries (persistence helpers available) |
| Thread Safety | Not thread-safe by default; create one instance per thread |
| Python Compatibility | 3.10, 3.11, 3.12 |
| License | MIT (or project license) |

## Agent Protocols

When operating as an autonomous agent within a larger system, the following
protocols should be followed:

### 1. Input Validation Protocol
- Always validate `plan_id` via `ValidationUtils.validate_plan_id()` before
  passing to internal methods.
- Validate timeline strings before persistence or plan generation.
- Clamp numeric inputs to documented ranges to prevent downstream errors.
- Never forward raw user input to `subprocess` or `exec` without sanitisation.

### 2. State Management Protocol
- Treat `_plans`, `_records` and `_sessions` as mutable state.
- Persist state explicitly via `save_plans_to_path()` or `export_full_backup()`.
- Assume in-memory state is lost on process exit unless persisted.
- Do not mutate `Plan` dataclass instances directly after creation; use
  dedicated update methods for progress tracking.

### 3. Error Reporting Protocol
- Raise `ValueError` for user-input errors with a human-readable message.
- Raise `KeyError` for missing state when caller expects a hard failure.
- Return `None` or error dictionaries for soft failures where appropriate.
- Log unexpected exceptions at `ERROR` level with full traceback.

### 4. Responsiveness Protocol
- Use async wrappers (`async_generate_practice_test`, `async_recommend_resources`,
  `async_track_progress`) for I/O-bound or long-running operations in web servers.
- Return immediately for simple read operations (`get_status`, `get_plans`).
- Emit structured dictionaries, not custom objects, for interoperability.

### 5. Extension Protocol
- Register new resources via `_resource_curator.add_resource()`.
- Register new question templates via `_template_engine.register_templates()`.
- Register new certification routes via `_route_manager.register_route()`.
- Do not fork core files; use hooks provided by `Config` and runtime registration.

### 6. Notification Protocol
- Notifications are silent unless `enable_notifications=True` in `Config`.
- SMTP credentials are never serialised or logged.
- Failed notifications are recorded with error details; processing continues.

## Core Capabilities

### 1. Study Plan Generation
- Accepts human-readable timelines like `"3-months"`, `"12-weeks"`, `"1-year"`.
- Resolves certification domains with weighted topic distributions.
- Creates a structured `StudyPlan` with a schedule of weekly activities.
- Generates milestone checkpoints for ongoing motivation.
- Supports topic focus and difficulty overrides.
- Includes metadata with session estimates and domain weight breakdowns.

### 2. Practice Test Creation
- Generates configurable sets of exam-style questions.
- Template-based approach ensures consistency and predictability.
- Supports seeded randomness for reproducible test fixtures.
- Returns rich metadata per question: topic, domain, difficulty, explanation, tags.
- Supports multi-domain templates (cloud, data, security, development, devops, networking).

### 3. Progress Tracking
- Tracks topic completion, practice accuracy, hours studied and streaks.
- Computes a weighted completion percentage combining coverage and quality.
- Stores metrics keyed to a plan identifier for easy retrieval.
- Provides history snapshots for trend analysis.
- Computes confidence scores and identifies weak domains.

### 4. Resource Curation
- Returns ranked learning resources from an in-memory catalogue.
- Supports dynamic registration of new resources at runtime.
- Classifies resources by type: course, book, lab, practice test, documentation.
- Filters by priority and maximum results.
- Supports type-specific filtering for targeted recommendations.

### 5. Mock Exam Simulation
- Simulates timed exam sittings with configurable question counts.
- Randomises question order for realism.
- Provides automatic scoring with per-domain performance breakdowns.
- Applies a 70 % pass threshold.
- Maintains exam history for review and trend analysis.

### 6. Exam Strategy Guidance
- Time-adaptive strategy recommendations based on days remaining.
- Balances content depth (foundations) against exam pressure (mocks, rest).
- Suggests daily study hours and resting periods.
- Maps to four distinct cognitive bands.
- Includes readiness score and action prioritisation.

### 7. Schedule Optimisation
- Generates conflict-aware weekly study schedules.
- Respects unavailable days and preferred study windows.
- Enforces per-session duration and weekly hour budgets.
- Distributes content evenly to prevent burnout.
- Limits sessions per day to respect cognitive load.

### 8. Study Note Generation
- Compiles Markdown study notes from questions, resources and domain summaries.
- Optional persistence to disk in a format designed for offline revision.
- Expands explanations and contextualises them within broader domains.
- Includes resource metadata (hours, priority) in production notes.

### 9. Competency Assessment
- Evaluates user performance across exam domains.
- Identifies strong and weak knowledge areas.
- Suggests difficulty adjustments based on recent accuracy.
- Generates recommended focus topics for targeted improvement.

### 10. Session Tracking
- Starts and ends timed study sessions.
- Tracks topics covered and questions answered per session.
- Supports concurrent plan tracking.
- Enables session history review and duration analysis.

### 11. Notification Service
- SMTP-based email delivery for milestone reminders.
- Silently disables when configuration is absent.
- Maintains notification history with delivery status.
- Supports custom recipient configuration.

### 12. Certification Route Management
- Maintains detailed certification metadata.
- Includes exam format, duration, passing score and prerequisites.
- Supports dynamic route registration.
- Enables discovery via `list_certification_routes()`.

### 13. JSON Serialisation and Persistence
- Full support for exporting plans, progress metrics and resources to JSON.
- Round-trip serialisation without external dependencies.
- File-system helpers for loading and saving plans.
- Comprehensive full backup export preserving all agent state.

### 14. Async Execution
- Provides `async_generate_practice_test()` and `async_recommend_resources()`
  wrappers that offload CPU-bound work to thread pool executors.
- Integrates naturally with FastAPI, Sanic or any `asyncio`-based framework.
- All async wrappers use `loop.run_in_executor()` for non-blocking behaviour.

### 15. Learning Analytics
- Computes learning velocity (topics per hour, hours per streak day).
- Estimates hours remaining based on historical rate.
- Identifies weak domains for targeted review.
- Produces comprehensive readiness scores.

### 16. Template Engine
- Supports custom question template registration.
- Enables domain-specific template collections.
- Provides flexible placeholder substitution.
- Allows runtime extension without modifying core question bank.

---

## Configuration

The agent is configured via the `Config` class.

### Config Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `default_domain` | `Optional[CertificationDomain]` | `None` | Preferred certification family when none specified. |
| `default_difficulty` | `DifficultyLevel` | `INTERMEDIATE` | Baseline question and plan difficulty. |
| `study_hours_per_week` | `int` | `10` | Weekly study hour budget used by schedule optimiser. |
| `retention_days` | `int` | `90` | Not yet consumed; reserved for future TTL logic. |
| `storage_path` | `str` | `"<agent_dir>/certification_prep_data"` | Base path for JSON persistence. |
| `verbose` | `bool` | `False` | Enable verbose runtime output. |
| `enable_notifications` | `bool` | `False` | Enable email/SMTP notifications. |
| `smtp_host` | `Optional[str]` | `None` | SMTP server hostname. |
| `smtp_port` | `int` | `587` | SMTP server port. |
| `smtp_user` | `Optional[str]` | `None` | SMTP authentication username. |
| `smtp_password` | `Optional[str]` | `None` | SMTP authentication password. |
| `notification_email` | `Optional[str]` | `None` | Default notification recipient. |
| `session_tracking` | `bool` | `True` | Enable study session tracking. |
| `competency_assessment` | `bool` | `True` | Enable adaptive competency assessment. |

### Configuration Examples

#### Basic
```python
agent = CertificationPrepAgent()
```

#### Advanced
```python
agent = CertificationPrepAgent(
    config=Config(
        default_difficulty=DifficultyLevel.ADVANCED,
        study_hours_per_week=15,
        retention_days=120,
        storage_path="./my_cert_prep_data",
        verbose=True,
        enable_notifications=True,
        smtp_host="smtp.example.com",
        smtp_port=587,
        smtp_user="notifier@example.com",
        smtp_password_env_var="SMTP_PASSWORD",
        notification_email="learner@example.com",
        session_tracking=True,
        competency_assessment=True,
    )
)
```

#### Enum-based Domain Constraint
```python
agent = CertificationPrepAgent(
    config=Config(
        default_domain=CertificationDomain.CLOUD,
        study_hours_per_week=12,
    )
)
```

#### Environment-based Configuration
```python
import os

config = Config(
    study_hours_per_week=int(os.getenv("CERT_PREP_HOURS_PER_WEEK", "10")),
    storage_path=os.getenv("CERT_PREP_STORAGE_PATH", "./data"),
    verbose=os.getenv("CERT_PREP_VERBOSE", "false").lower() == "true",
    enable_notifications=os.getenv("CERT_PREP_NOTIFICATIONS", "false").lower() == "true",
    smtp_host=os.getenv("CERT_PREP_SMTP_HOST"),
    smtp_port=int(os.getenv("CERT_PREP_SMTP_PORT", "587")),
    notification_email=os.getenv("CERT_PREP_RECIPIENT"),
)
agent = CertificationPrepAgent(config=config)
```

---

## Domain Taxonomy

Built-in domain keyword mappings help the agent generate relevant content for
popular certification categories:

| Domain Keyword | Mapped Domain | Example Certs |
|----------------|---------------|---------------|
| `aws` | Cloud | AWS Certified Solutions Architect |
| `gcp` | Cloud | Google Cloud Professional Data Engineer |
| `azure` | Cloud | Azure Solutions Architect Expert |
| `python` | Development | Python Institute PCAP / PCPP |
| `data` | Data | Any data-centric certification |
| `sec` | Security | CompTIA Security+, CISSP |
| `network` | Networking | CCNA, CCNP, CCIE |
| `docker` | DevOps | Docker Certified Associate |
| `k8s` | DevOps | Certified Kubernetes Administrator |
| `terraform` | DevOps | HashiCorp Certified Terraform Associate |

To add a new domain, extend `QuestionBank.QUESTION_TEMPLATES` and
`QuestionBank._guess_domain()`.

## Resource Type Taxonomy

| Type | Description | Typical Sources |
|------|-------------|-----------------|
| `course` | Structured video or text-based learning | Udemy, Coursera, edX |
| `book` | Reference-style printed or digital material | O'Reilly, McGraw-Hill, Manning |
| `lab` | Interactive hands-on environments | AWS Skill Builder, Cloud Shell |
| `practice_test` | Simulated exam sittings | Official exam portals, third-party vendors |
| `documentation` | Official API or product documentation | Vendor websites |
| `video` | Recorded lectures and walkthroughs | YouTube, official training |
| `podcast` | Audio content for on-the-go learning | Vendor podcasts, community shows |
| `workshop` | Instructor-led sessions | Conferences, corporate training |

## Progress Calculation

Completion percentage is a weighted composite intended to reward both
breadth and depth:

```
completion_percentage = (topics_completed / max(topics_total, 1)) * 60.0
                      + (practice_accuracy * 40.0)
```

Confidence score is derived from completion percentage:

```
confidence_score = min(1.0, completion_percentage / 100.0)
```

Implementation guarantees:
- `topics_total` is clamped to `>= 1` to prevent division by zero.
- `practice_accuracy` is clamped to `[0.0, 1.0]`.
- Non-negative counting fields are clamped to `>= 0`.
- Negative hours are rejected and clamped to zero.

## Mock Exam Scoring

Exams are scored against a 70 % pass threshold:

| Score Range | Status |
|-------------|--------|
| 0.00 – 0.69 | Fail |
| 0.70 – 1.00 | Pass |

A topic breakdown dictionary is returned for per-domain review.

## Exam Strategy Matrix

| Days Remaining | Focus | Actions |
|----------------|-------|---------|
| > 60 | Foundation Building | Official guide review, foundational courses, lab environment |
| 14 – 60 | Intensive Practice | Daily exams, weak-domain review, time management drills |
| 1 – 13 | Exam Readiness | Single timed mock, summaries, rest, logistics |
| <= 0 | Post Exam | Performance review, re-certification planning |

Daily recommended hours scale linearly from 0 at 0 days remaining up to
`study_hours_per_week / 7` for long timelines.

## Schedule Optimisation Rules

1. Plan entries are processed in order.
2. Each entry is assigned to a day chosen from `preferred_days`.
3. If the chosen day is contained in `unavailable`, the first available
   preferred day is chosen instead.
4. Weekly hour usage accumulates; when it exceeds the configured budget, the
   next week calendar bound resets the counter.
5. Each session defaults to `session_length_hours` (1.5 hours).
6. Daily session count is limited by `max_sessions_per_day` (default 2).

## Usage Patterns

### Basic Workflow

```python
from agents.certification-prep.agent import CertificationPrepAgent

agent = CertificationPrepAgent()

# 1. Create a plan
plan = agent.create_study_plan("aws-saa", "3-months")
plan_id = plan["plan_id"]
print("Plan created:", plan_id)

# 2. Generate questions
questions = agent.generate_practice_test("aws-saa", count=10)
for q in questions[:3]:
    print(f"{q['question_id']}: {q['text']}")

# 3. Track progress
status = agent.track_progress(
    plan_id=plan_id,
    topics_completed=4,
    topics_total=10,
    practice_questions_answered=30,
    practice_accuracy=0.72,
    hours_studied=15.0,
    current_streak=4,
)
print(f"Progress: {status['completion_percentage']}%")

# 4. Curate resources
resources = agent.recommend_resources("aws-saa", max_resources=5)
print("Top resource:", resources[0]["name"])

# 5. Optimise schedule
schedule = agent.optimize_schedule(
    plan_id,
    unavailable=["Sunday"],
    session_length_hours=1.5,
)
print("Next session:", schedule[0])

# 6. Run mock exam
exam = agent.run_mock_exam("aws-saa", count=20, time_limit_minutes=60)
print("Pass:", exam["pass"], "Score:", exam["score"])

# 7. Get exam strategy
strategy = agent.exam_strategy("aws-saa", days_remaining=21)
print("Strategy:", strategy["focus"])

# 8. Export study notes
notes = agent.export_study_notes("aws-saa", output_path="./notes.md")

# 9. Persist plans
agent.save_plans_to_path("./plans.json")
```

### Async Usage

```python
import asyncio

async def prepare():
    agent = CertificationPrepAgent()
    questions = await agent.async_generate_practice_test("gcp-data", count=20)
    resources = await agent.async_recommend_resources("gcp-data", max_resources=5)
    progress = await agent.async_track_progress(
        plan_id="plan-1",
        topics_completed=5,
        topics_total=10,
        practice_questions_answered=20,
        practice_accuracy=0.7,
        hours_studied=10.0,
        current_streak=3,
    )
    return questions, resources, progress

questions, resources, progress = asyncio.run(prepare())
```

### Deterministic Test Fixtures

```python
agent = CertificationPrepAgent(
    config=Config(default_difficulty=DifficultyLevel.INTERMEDIATE)
)

# Same seed always produces identical questions
q1 = agent.generate_practice_test("aws-saa", count=5, seed=42)
q2 = agent.generate_practice_test("aws-saa", count=5, seed=42)
assert q1 == q2
```

### Analytics-Driven Review

```python
plan = agent.create_study_plan("ccna", "12-weeks")
plan_id = plan["plan_id"]

agent.track_progress(
    plan_id,
    topics_completed=3,
    topics_total=10,
    practice_questions_answered=30,
    practice_accuracy=0.68,
    hours_studied=9.0,
    current_streak=2,
)

summary = agent.get_progress(plan_id)
print("Hours remaining:", summary["estimated_hours_remaining"])
print("Topics remaining:", summary["topics_remaining"])

velocity = agent.get_learning_velocity(plan_id)
print("Topics per hour:", velocity["topics_per_hour"])

readiness = agent.calculate_readiness(plan_id)
print("Readiness score:", readiness["readiness_score"])
```

### Dynamic Resource Registration

```python
agent = CertificationPrepAgent()
agent._resource_curator.add_resource(
    certification="my-custom-cert",
    resource_type="course",
    name="Custom Certification Bootcamp",
    url="https://example.com/bootcamp",
    estimated_hours=30.0,
    description="Intensive preparation for my-custom-cert.",
    priority=1,
)
resources = agent.recommend_resources("my-custom-cert", max_resources=5)
```

### Difficulty Override

```python
questions_easy = agent.generate_practice_test(
    "aws-saa", count=10, difficulty=DifficultyLevel.BEGINNER
)
questions_hard = agent.generate_practice_test(
    "aws-saa", count=10, difficulty=DifficultyLevel.EXPERT
)
```

### Competency Assessment

```python
agent = CertificationPrepAgent()
plan = agent.create_study_plan("aws-saa", "3-months")
plan_id = plan["plan_id"]

questions = agent.generate_practice_test("aws-saa", count=20)
user_answers = {q["question_id"]: random.randint(0, 3) for q in questions}

assessment = agent.assess_competency(questions, user_answers)
print("Strong areas:", assessment["strong_areas"])
print("Weak areas:", assessment["weak_areas"])
print("Suggested focus:", assessment["recommended_focus"])

# Get adaptive difficulty suggestion
suggested = agent.suggest_difficulty(
    recent_accuracy=assessment["overall_score"],
    current_difficulty=DifficultyLevel.INTERMEDIATE,
)
print("Consider difficulty:", suggested)
```

### Session Tracking

```python
agent = CertificationPrepAgent()
plan = agent.create_study_plan("aws-saa", "3-months")
plan_id = plan["plan_id"]

# Start a study session
session = agent.start_study_session(plan_id, topics=["storage", "EC2"])
print("Session started:", session["session_id"])

# ... study activity ...

# End the session
ended = agent.end_study_session(
    plan_id,
    questions_answered=15,
    correct_answers=12,
)
print("Session duration:", ended["duration_minutes"], "minutes")

# Review all sessions
all_sessions = agent.get_sessions(plan_id)
for s in all_sessions:
    print(f"{s['started_at']}: {s['duration_minutes']}m, "
          f"score {s['correct_answers']}/{s['questions_answered']}")
```

### Notification Configuration

```python
config = Config(
    enable_notifications=True,
    smtp_host="smtp.gmail.com",
    smtp_port=587,
    smtp_user="your-email@gmail.com",
    smtp_password_env_var="SMTP_PASSWORD",
    notification_email="recipient@example.com",
)
agent = CertificationPrepAgent(config=config)

agent.send_milestone_reminder(
    recipient="learner@example.com",
    certification="aws-saa",
    milestone="Week 4: Initial knowledge check",
)
```

### Certification Route Discovery

```python
agent = CertificationPrepAgent()

# List all available routes
routes = agent.list_certification_routes()
for route in routes:
    print(f"{route['certification_id']}: {route['display_name']}")

# Get details for a specific route
aws_route = agent.get_certification_route("aws-saa")
print("Exam duration:", aws_route["exam_duration_minutes"], "minutes")
print("Passing score:", f"{aws_route['passing_score']:.0%}")
print("Domains:")
for domain in aws_route["domains"]:
    print(f"  {domain['name']} ({domain['weight']:.0%})")
```

### Combined Batch Workflow

```python
agent = CertificationPrepAgent()
plan = agent.create_study_plan("ccna", "12-weeks")
pid = plan["plan_id"]

resources = agent.recommend_resources("ccna", max_resources=7)
agent.export_study_notes("ccna", output_path="./ccna_notes.md")
exam = agent.run_mock_exam("ccna", count=25, time_limit_minutes=90)
strategy = agent.exam_strategy("ccna", days_remaining=30)
agent.save_plans_to_path("./ccna_progress.json")

print(f"Exam passed: {exam['pass']} with score {exam['score']:.2%}")
print(f"Strategy focus: {strategy['focus']}")
print(f"Readiness: {agent.calculate_readiness(pid)['readiness_score']:.0%}")
```

---

## CLI Reference

The agent exposes a full command-line interface:

```bash
# Show agent status
python agents/certification-prep/agent.py status

# Run interactive demo
python agents/certification-prep/agent.py demo

# Create plan and questions
python agents/certification-prep/agent.py plan \
  --certification aws-saa \
  --timeline 3-months \
  --questions 20 \
  --verbose

# Show certification route details
python agents/certification-prep/agent.py route --certification ccna

# Suggest difficulty adjustment
python agents/certification-prep/agent.py suggest-difficulty \
  --current intermediate \
  --accuracy 0.72
```

### CLI Flags and Commands

| Command | Description | Arguments |
|---------|-------------|-----------|
| `demo` | Run interactive demo | `[--verbose]` |
| `plan` | Create a study plan | `--certification`, `--timeline`, `[--questions]`, `[--verbose]` |
| `status` | Show agent status | `[--verbose]` |
| `route` | Show certification route | `--certification` |
| `suggest-difficulty` | Suggest difficulty | `--current`, `--accuracy` |

| Flag | Description | Default |
|------|-------------|---------|
| `--verbose` | Enable verbose logging | `False` |
| `--certification` | Certification identifier | `None` |
| `--timeline` | Study timeline | `"3-months"` |
| `--questions` | Number of practice questions | `5` |
| `--current` | Current difficulty level | — |
| `--accuracy` | Recent accuracy (0.0-1.0) | — |

---

## Persistence Guide

Plans can be saved and loaded as JSON arrays. This enables session recovery in
automated environments (CI pipelines, batch training jobs, etc.).

### Save Plans

```python
agent.save_plans_to_path("./backup.json")
```

### Load Plans

```python
agent2 = CertificationPrepAgent()
agent2.load_plans_from_path("./backup.json")
assert len(agent2.get_plans()) == len(agent.get_plans())
```

### Full Backup

```python
agent.export_full_backup("./full_backup.json")
```

### JSON Payload Shape

```json
[
  {
    "plan_id": "plan-aws-saa-1717500000",
    "certification": "aws-saa",
    "topic": "aws-saa",
    "timeline_weeks": 12,
    "difficulty": "intermediate",
    "weekly_hours": 10.0,
    "total_hours": 120.0,
    "domains": ["Core Concepts", "Implementation", ...],
    "schedule": ["Week 1: aws-saa-fundamentals", ...],
    "milestones": ["Week 3: Initial knowledge check", ...],
    "metadata": {
      "timeline_source": "3-months",
      "domain_weights": {"Core Concepts": 0.3, ...},
      "session_count_estimate": 60
    }
  }
]
```

---

## Serialisation

`to_json(plan_id)` returns a structured JSON string containing the plan,
latest progress and top resources. Useful for API responses or configuration
exports:

```python
import json
payload = json.loads(agent.to_json(plan_id))
print(json.dumps(payload, indent=2))
```

The JSON output includes:

- `plan`: Full study plan dictionary.
- `progress`: Latest progress metrics (or `null`).
- `resources`: Top 10 resources for the certification.
- `sessions`: All sessions associated with the plan.

---

## Integration Guide

The agent emits no external events by default, but integrates cleanly with
web frameworks.

### FastAPI

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
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timeline format")

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

### Flask

```python
from flask import Flask
from agents.certification-prep.agent import CertificationPrepAgent

app = Flask(__name__)
agent = CertificationPrepAgent()

@app.route("/plan/<cert>/<timeline>")
def plan(cert, timeline):
    try:
        return agent.create_study_plan(cert, timeline)
    except ValueError as exc:
        return {"error": str(exc)}, 400

@app.route("/status")
def status():
    return agent.get_status()
```

### Celery Task Queue

```python
from celery import Celery
celery_app = Celery("cert_prep")
agent = CertificationPrepAgent()

@celery_app.task
def generate_plan_task(certification: str, timeline: str, topic: str):
    return agent.create_study_plan(certification, timeline, topic)
```

### Jupyter Notebook Integration

```python
from IPython.display import display, Markdown

agent = CertificationPrepAgent()
plan = agent.create_study_plan("aws-saa", "3-months")
display(Markdown(f"**Plan ID**: {plan['plan_id']}"))
display(Markdown(f"**Milestones**: {len(plan['milestones'])}"))

questions = agent.generate_practice_test("aws-saa", count=10)
for q in questions:
    display(Markdown(f"**Q**: {q['text']}"))
    display(Markdown("\n".join(f"- {chr(65+i)}. {opt}"
                               for i, opt in enumerate(q["options"]))))
```

---

## Extensibility Checklist

- [ ] Add new templates to `QuestionBank.QUESTION_TEMPLATES` or via `TemplateEngine`.
- [ ] Register new resources in `ResourceCurator.RESOURCE_DATABASE` or via `add_resource()`.
- [ ] Update `CertificationDomain` if adding a new top-level domain.
- [ ] Register new certification routes via `CertificationRouteManager.register_route()`.
- [ ] Add unit tests for new behaviour in `tests/`.
- [ ] Update `ARCHITECTURE.md` with new component documentation.

### Suggested Test Layout

```
tests/
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
```

---

## Operational Notes

- **Agent state is volatile**: In-memory plans are lost on process exit. Use
  `save_plans_to_path()` or `export_full_backup()` for durability.
- **Verbose mode**: `--verbose` enables logging. In production, wire to a
  structured logger.
- **Single instance**: The agent is not thread-safe. Create one instance per
  thread or protect access with a lock.
- **Seeds**: Always set a seed in automated test environments for determinism.
- **SMTP Configuration**: Notifications require explicit SMTP configuration;
  they remain silent otherwise.
- **Session Tracking**: Session data is in-memory and not persisted automatically.
- **Resource Registration**: New resources take effect immediately for the
  lifetime of the agent instance; they are not persisted unless backed up.

---

## Troubleshooting

| Issue | Resolution |
|-------|-----------|
| `ValueError: Unable to parse timeline string` | Ensure format is `<integer>-<unit>` (e.g. `6-weeks`). |
| `ValueError: Timeline value must be positive` | Use a positive integer for the timeline value. |
| `ValueError: Timeline exceeds maximum of 10 years` | Reduce timeline to 520 weeks or less. |
| `KeyError` when retrieving plan | Confirm `plan_id` is correct and plan was not garbage collected. |
| Zero practice questions returned | Ensure `count` is between `5` and `50`. |
| Study notes file not created | Confirm output directory exists and is writable. |
| Mock exam fails frequently | Decrease `time_limit_minutes` or increase `count`. |
| JSON load error | Ensure the file contains a JSON array of plan objects. |
| `RuntimeError` on session start | End the active session for that plan first. |
| `TypeError` on accuracy | Pass a float value (0.0 to 1.0), not an integer. |
| Notification not sent | Verify `enable_notifications` and SMTP configuration. |
| `PermissionError` on file write | Check directory permissions and disk space. |
| `FileNotFoundError` on backup load | Verify the backup file path is correct. |

---

## Limitations and Constraints

1. **Template-based questions**: No LLM integration; open-ended scenarios
   require manual template authoring.
2. **Static resource catalogue**: Resources must be registered programmatically
   for dynamic content.
3. **In-memory state**: Persistence requires explicit JSON save/load helpers.
4. **No authentication**: Caller is trusted to enforce access control.
5. **Not thread-safe**: One agent instance per thread recommended.
6. **Limited question types**: Currently supports multiple-choice only.
7. **No built-in calendar sync**: Schedule output is plain dictionaries.
8. **SMTP-only notifications**: No webhook or push notification adapters built-in.
9. **No persisted exam history**: Exam results are tracked in-memory only.

---

## Agent Guidelines

When consuming this agent, follow these guidelines to maximise value:

1. **Validate inputs before calling the agent**: Sanitise user-provided
   certifications and timeline strings before passing them to the API.
2. **Persist plans regularly**: Use `save_plans_to_path()` to avoid losing
   study plan data.
3. **Leverage deterministic tests**: Use `seed` with `generate_practice_test()`
   in CI/CD pipelines to ensure reproducible output.
4. **Chain features**: Combine multiple capabilities (plan → questions →
   progress → notes) for a richer learning experience.
5. **Extend thoughtfully**: Prefer registering new resources and templates over
   forking the agent core.
6. **Handle errors explicitly**: Check for `KeyError`, `ValueError` and `None`
   returns in production code.
7. **Monitor readiness scores**: Use `calculate_readiness()` to drive
   personalised recommendations and adaptive pacing.
8. **Use async wrappers in web servers**: Prevent blocking the event loop
   during CPU-bound question generation.
9. **Sanitise exported data**: Review JSON backups before transmission to
   ensure no sensitive credentials are included.
10. **Version compatibility**: Test with Python 3.10+ and pin dependencies
    appropriately for production deployments.

---

## Contributing

Phases for extending the agent:

1. Add templates to `QuestionBank.QUESTION_TEMPLATES` under a new key.
2. Add resource entries to `ResourceCurator.RESOURCE_DATABASE`.
3. Update `CertificationDomain` with any new enumeration values.
4. Add unit tests in `tests/` matching the service-layer component patterns.
5. Update `ARCHITECTURE.md` with new component documentation.
6. Update this `GROK.md` with usage examples for new capabilities.

---

## Performance Tips

- For batch question generation, use `batch_generate_questions()` to amortise
  setup overhead.
- Set `session_tracking=False` in `Config` if session data is not needed.
- Set `competency_assessment=False` if adaptive adjustment is not required.
- Use `export_full_backup()` sparingly in high-throughput environments; it
  copies all in-memory state to a single JSON payload.
- In web deployments, create one `CertificationPrepAgent` instance and share
  it across requests only if requests are serialised (e.g. via a task queue).

---

## License

Internal use. Add your project's licence block here.

---

## Changelog

### 1.0.0 (2026-06-04)
- Initial modular release with `CertificationPrepAgent` and fifteen service
  components.
- Template-based question generation with seed support.
- Progress tracking with weighted completion formula.
- Resource curation with dynamic registration.
- JSON serialisation, async wrappers and argparse CLI.
- Competency assessment and session tracking.
- Certification route management.
- Notification service with SMTP support.
- Comprehensive documentation across `GROK.md`, `README.md` and
  `ARCHITECTURE.md`.
