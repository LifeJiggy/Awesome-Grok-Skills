# Automation Agent — Architecture

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Component Deep Dives](#component-deep-dives)
- [Data Flow](#data-flow)
- [Data Models](#data-models)
- [Design Patterns](#design-patterns)
- [Tech Stack](#tech-stack)
- [Security Architecture](#security-architecture)
- [Scalability](#scalability)
- [Deployment](#deployment)

---

## Overview

The Automation Agent provides end-to-end business process automation including workflow orchestration, scheduling, email automation, file system operations, and notification management. It implements a DAG-based workflow engine with parallel execution, retry, and compensation support.

### Core Capabilities

```
┌─────────────────────────────────────────────────────────────────────┐
│                       Automation Agent                               │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │  Workflow    │  │  Schedule    │  │    Email     │             │
│  │   Engine     │  │   Manager    │  │  Automation  │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │    File      │  │ Notification │  │   Action     │             │
│  │  Automation  │  │   Engine     │  │   Chain      │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
```

### Architecture Principles

1. **DAG-Based Execution**: Workflows modeled as directed acyclic graphs
2. **Idempotent Tasks**: Safe to retry without side effects
3. **Compensation Support**: Rollback actions for failed tasks
4. **Parallel Execution**: Independent tasks run concurrently
5. **Observable**: Full execution history and audit trail

---

## System Architecture

### High-Level Architecture

```
                         ┌─────────────────────┐
                         │   Automation Agent  │
                         └──────────┬──────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         │                          │                          │
   ┌─────▼──────┐          ┌───────▼───────┐          ┌───────▼──────┐
   │  Workflow  │          │  Schedule     │          │    Email     │
   │   Engine   │          │   Manager     │          │  Automation  │
   │            │          │               │          │              │
   │ • DAG exec │          │ • Cron        │          │ • Templates  │
   │ • Parallel │          │ • Interval    │          │ • Campaigns  │
   │ • Retry    │          │ • Due check   │          │ • Send       │
   │ • Rollback │          │ • History     │          │ • Track      │
   └─────┬──────┘          └───────┬───────┘          └───────┬──────┘
         │                          │                          │
         └──────────────────────────┼──────────────────────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         │                          │                          │
   ┌─────▼──────┐          ┌───────▼───────┐          ┌───────▼──────┐
   │    File    │          │ Notification  │          │   History    │
   │ Automation │          │    Engine     │          │   Tracker    │
   │            │          │               │          │              │
   │ • Watch    │          │ • Email       │          │ • Executions │
   │ • Process  │          │ • Slack       │          │ • Audit      │
   │ • Compress │          │ • Webhook     │          │ • Metrics    │
   │ • Extract  │          │ • SMS         │          │ • Reports    │
   └────────────┘          └───────────────┘          └──────────────┘
```

---

## Component Deep Dives

### 1. Workflow Engine

```
┌─────────────────────────────────────────────────────────────────────┐
│                       Workflow Engine                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  DAG Construction                                            │   │
│  │                                                              │   │
│  │  Task A ──▶ Task B ──▶ Task D                               │   │
│  │    │                   ▲                                     │   │
│  │    └──▶ Task C ────────┘                                     │   │
│  │                                                              │   │
│  │  • Topological sort determines execution order               │   │
│  │  • Independent tasks run in parallel                         │   │
│  │  • Deadlock detection for circular dependencies              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Task Execution Lifecycle                                    │   │
│  │                                                              │   │
│  │  PENDING ──▶ RUNNING ──▶ COMPLETED                          │   │
│  │                │                                             │   │
│  │                ├──▶ FAILED ──▶ RETRYING ──▶ RUNNING         │   │
│  │                │         │                                   │   │
│  │                │         └──▶ (max retries) ──▶ FAILED      │   │
│  │                │                       │                     │   │
│  │                │                       ▼                     │   │
│  │                │              Compensation Action            │   │
│  │                │                                             │   │
│  │                └──▶ SKIPPED (dependency failed)              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Retry Strategies                                            │   │
│  │                                                              │   │
│  │  Fixed:        delay = base                                 │   │
│  │  Linear:       delay = base × attempt                       │   │
│  │  Exponential:  delay = base × 2^attempt                     │   │
│  │                                                              │   │
│  │  Default: 5s base, exponential backoff                       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2. Schedule Manager

```
┌─────────────────────────────────────────────────────────────────────┐
│                       Schedule Manager                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Schedule Types                                              │   │
│  │                                                              │   │
│  │  Cron Expression:                                            │   │
│  │    "0 9 * * 1-5"  → Weekdays at 9:00 AM                     │   │
│  │    "0 0 1 * *"    → First of every month                    │   │
│  │    "*/15 * * * *" → Every 15 minutes                        │   │
│  │                                                              │   │
│  │  Interval:                                                   │   │
│  │    3600  → Every hour                                        │   │
│  │    86400 → Daily                                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Schedule Lifecycle                                          │   │
│  │                                                              │   │
│  │  Create ──▶ Enabled ──▶ Running ──▶ Completed                │   │
│  │    │                       │                                 │   │
│  │    │                       ▼                                 │   │
│  │    │                  Disabled                               │   │
│  │    │                                                         │   │
│  │    └──▶ Removed                                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Due Schedule Detection:                                            │
│  get_due_schedules() ──▶ next_run <= now ──▶ execute               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3. Email Automation

```
┌─────────────────────────────────────────────────────────────────────┐
│                       Email Automation                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Template System                                              │   │
│  │                                                              │   │
│  │  Subject: "Welcome {{name}}!"                                │   │
│  │  Body: "Hello {{name}}, your account is ready."              │   │
│  │                                                              │   │
│  │  Variables: {{name}}, {{email}}, {{company}}                 │   │
│  │                                                              │   │
│  │  render({"name": "John"}) →                                 │   │
│  │    Subject: "Welcome John!"                                  │   │
│  │    Body: "Hello John, your account is ready."                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Campaign Lifecycle                                          │   │
│  │                                                              │   │
│  │  Draft ──▶ Running ──▶ Completed                             │   │
│  │                                                              │   │
│  │  • Bulk send to recipients list                              │   │
│  │  • Track sent/failed counts                                  │   │
│  │  • Schedule for future delivery                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 4. File Automation

```
┌─────────────────────────────────────────────────────────────────────┐
│                       File Automation                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Operations                                                  │   │
│  │                                                              │   │
│  │  • Copy — duplicate files/directories                        │   │
│  │  • Move — relocate files/directories                         │   │
│  │  • Delete — remove files/directories                         │   │
│  │  • Rename — rename files                                     │   │
│  │  • Compress — create ZIP archives                            │   │
│  │  • Extract — unpack archives                                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Folder Watching                                             │   │
│  │                                                              │   │
│  │  Watch: /data/incoming                                       │   │
│  │  Extensions: [".csv", ".json"]                               │   │
│  │  Action: process_new_data                                    │   │
│  │  Recursive: false                                            │   │
│  │                                                              │   │
│  │  Interval: 60 seconds                                       │   │
│  │  Last check: 2026-07-06T10:30:00                            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### End-to-End Automation Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Automation Flow                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. Define Workflow                                                 │
│     create_workflow() ──▶ Workflow with Tasks                       │
│                                                                     │
│  2. Configure Schedule (optional)                                   │
│     add_schedule() ──▶ Cron/Interval trigger                       │
│                                                                     │
│  3. Execute                                                         │
│     execute_workflow() ──▶ DAG resolution ──▶ Parallel execution   │
│                                                                     │
│  4. Monitor                                                         │
│     get_workflow_status() ──▶ Progress tracking                    │
│                                                                     │
│  5. Complete                                                        │
│     ExecutionHistory ──▶ Results + Duration + Status               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Task Execution Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Task Execution Flow                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Task Ready                                                         │
│       │                                                             │
│       ▼                                                             │
│  Resolve Handler ──▶ Execute ──▶ Success?                          │
│       │                  │           │                              │
│       │                  │           ├── Yes ──▶ COMPLETED          │
│       │                  │           │                              │
│       │                  │           └── No ──▶ Retry?             │
│       │                  │                       │                  │
│       │                  │                       ├── Yes ──▶ Wait ──▶ Execute │
│       │                  │                       │                  │
│       │                  │                       └── No ──▶ FAILED  │
│       │                  │                                │         │
│       │                  │                                ▼         │
│       │                  │                    Compensation Action   │
│       │                  │                                         │
│       └──▶ No Handler ──▶ TaskError                               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Models

### Entity Relationship

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Entity Relationships                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Workflow ───────────┬──── Task[]                                   │
│       │               │                                              │
│       │               └──── depends_on (Task IDs)                   │
│       │                                                              │
│       ├── Schedule (optional)                                       │
│       │                                                              │
│       └──── ExecutionHistory[]                                       │
│                                                                     │
│  Task ───────────────┬──── ActionType                               │
│       │               │                                              │
│       │               ├── action_config (Dict)                       │
│       │               │                                              │
│       │               └── compensation_action (optional)             │
│                                                                     │
│  Schedule ───────────┬──── Workflow reference                        │
│       │               │                                              │
│       │               └──── Cron/Interval config                     │
│                                                                     │
│  EmailTemplate ──────┬──── EmailCampaign reference                   │
│                      │                                               │
│                      └──── Variables list                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Design Patterns

### 1. DAG Pattern — Workflow Execution

```python
# Topological sort for execution order
ready_tasks = [
    t for t in workflow.tasks
    if all(dep in completed for dep in t.depends_on)
]
```

### 2. Strategy Pattern — Retry

```python
class RetryStrategy(Enum):
    FIXED = "fixed"          # delay = base
    EXPONENTIAL = "exponential"  # delay = base * 2^attempt
    LINEAR = "linear"        # delay = base * attempt
```

### 3. Observer Pattern — File Watching

```python
class FileWatchConfig:
    path: str
    extensions: List[str]
    action: str  # Handler to invoke on change
```

### 4. Template Method — Email

```python
class EmailTemplate:
    def render(self, variables: Dict) -> Dict[str, str]:
        # Template method: replace {{var}} with values
        ...
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Language | Python 3.10+ | Core runtime |
| Concurrency | `concurrent.futures` | Parallel task execution |
| Data Models | `dataclasses` | Typed data containers |
| Scheduling | Custom cron parser | Time-based triggers |
| File Ops | `shutil`, `pathlib` | File system operations |
| Hashing | `hashlib` | ID generation |
| Logging | `logging` | Observability |

---

## Security Architecture

### Considerations

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Security Layers                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Layer 1: Input Validation                                          │
│  • Validate task configurations                                     │
│  • Sanitize file paths (prevent traversal)                          │
│  • Validate email addresses                                         │
│                                                                     │
│  Layer 2: Execution Limits                                          │
│  • Task timeout enforcement                                         │
│  • Maximum retry limits                                             │
│  • Workflow timeout                                                 │
│  • Max concurrent workflows                                         │
│                                                                     │
│  Layer 3: File System Safety                                        │
│  • Restricted to configured directories                             │
│  • No symlink following by default                                  │
│  • Backup before destructive operations                             │
│                                                                     │
│  Layer 4: Audit                                                     │
│  • Full execution history                                           │
│  • File operation logging                                           │
│  • Email send tracking                                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Scalability

### Performance Characteristics

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Workflow creation | O(t) | t = number of tasks |
| DAG resolution | O(t + e) | e = dependencies |
| Task execution | O(1) per task | Parallel execution |
| Schedule check | O(s) | s = number of schedules |
| History query | O(h) | h = history entries |

### Scaling Strategies

1. **Current**: In-memory, single process — suitable for <100 workflows
2. **Database-Backed**: Persist workflows and history in PostgreSQL
3. **Distributed**: Use Celery/RQ for distributed task execution
4. **Event-Driven**: Replace polling with event bus for schedule triggers
5. **Kubernetes**: Deploy as pods with horizontal scaling

---

## Deployment

### Docker Deployment

```yaml
version: '3.8'
services:
  automation-agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SMTP_HOST=${SMTP_HOST}
      - SLACK_WEBHOOK=${SLACK_WEBHOOK}
    volumes:
      - ./data:/app/data
      - ./output:/app/output
```

---

*Automation Agent Architecture v2.0 — Part of the Awesome Grok Skills collection.*
