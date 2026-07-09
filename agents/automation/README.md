# Automation Agent

> Business process automation, workflow orchestration, scheduling, and task management.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Quick Start](#quick-start)
5. [Installation](#installation)
6. [Usage](#usage)
7. [API Reference](#api-reference)
8. [Data Models](#data-models)
9. [Examples](#examples)
10. [Configuration](#configuration)
11. [Best Practices](#best-practices)
12. [Security](#security)
13. [Scalability](#scalability)
14. [Design Patterns](#design-patterns)
15. [Troubleshooting](#troubleshooting)
16. [License](#license)

---

## Overview

The Automation Agent provides end-to-end business process automation with a DAG-based workflow engine, cron/interval scheduling, email automation, file system operations, and notification management. Every workflow is idempotent, every failure has a compensation path, and every execution leaves an audit trail.

### What It Does

- **Workflow Orchestration**: DAG-based task execution with dependencies and parallel runs
- **Scheduling**: Cron expressions and interval-based triggers
- **Retry & Rollback**: Configurable retry strategies with compensation actions
- **Email Automation**: Templates with variable substitution and bulk campaigns
- **File Operations**: Watch, copy, move, delete, compress, extract
- **Notifications**: Multi-channel alerts (email, Slack, webhook, SMS, console)
- **Execution History**: Full audit trail with duration and status tracking
- **Variable Templating**: Pass data between tasks with `{{tasks.TaskName.output}}` syntax

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                       Automation Agent                              │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Workflow   │  │  Scheduler   │  │    Email     │             │
│  │   Engine     │  │   Manager    │  │   Manager    │             │
│  │              │  │              │  │              │             │
│  │ • DAG        │  │ • Cron       │  │ • Templates  │             │
│  │ • Parallel   │  │ • Interval   │  │ • Campaigns  │             │
│  │ • Retry      │  │ • Recurring  │  │ • Bulk Send  │             │
│  │ • Compensate │  │ • One-shot   │  │ • Variables  │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │    File      │  │ Notification │  │   Execution  │             │
│  │  Operations  │  │   Manager    │  │   History    │             │
│  │              │  │              │  │              │             │
│  │ • Watch      │  │ • Email      │  │ • Audit Log  │             │
│  │ • Copy/Move  │  │ • Slack      │  │ • Duration   │             │
│  │ • Compress   │  │ • Webhook    │  │ • Status     │             │
│  │ • Extract    │  │ • SMS        │  │ • Variables  │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Schedule   │────▶│   Workflow  │────▶│    Task     │
│  Trigger    │     │   Engine    │     │  Execution  │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          │                          │
              ┌─────▼──────┐          ┌───────▼───────┐          ┌───────▼──────┐
              │   Email    │          │    File       │          │  Notification│
              │   Send     │          │   Operation   │          │   Dispatch   │
              └────────────┘          └───────────────┘          └──────────────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │  Execution  │
                                        │   History   │
                                        └─────────────┘
```

### DAG Execution Model

```
        ┌───────┐
        │ Start │
        └───┬───┘
            │
    ┌───────┴───────┐
    │               │
┌───▼───┐       ┌───▼───┐
│Task A │       │Task B │    ← Parallel execution
└───┬───┘       └───┬───┘
    │               │
    └───────┬───────┘
            │
        ┌───▼───┐
        │Task C │    ← Waits for A and B
        └───┬───┘
            │
        ┌───▼───┐
        │ End   │
        └───────┘
```

---

## Features

| Feature | Description |
|---------|-------------|
| DAG Execution | Topological sort for dependency resolution |
| Parallel Tasks | Independent tasks run concurrently (configurable max) |
| Retry Strategies | Fixed, linear, exponential backoff |
| Compensation | Rollback actions for failed tasks |
| Cron Scheduling | Standard cron expression support |
| Interval Scheduling | Fixed-interval triggers (seconds) |
| Email Templates | Variable substitution with HTML support |
| Bulk Campaigns | Send to multiple recipients with tracking |
| File Watching | Monitor folders for new files |
| File Operations | Copy, move, delete, transform, compress, extract |
| Multi-Channel | Email, Slack, webhook, SMS, console |
| Audit Trail | Full execution history with duration |
| Variable Templating | `{{tasks.TaskName.output}}` data passing |

---

## Quick Start

```python
from agents.automation.agent import AutomationAgent

agent = AutomationAgent()

# Create a workflow
wf = agent.create_workflow("Daily Report", [
    {"name": "Fetch Data", "action_type": "http_request", "action_config": {"url": "https://api.example.com/data"}},
    {"name": "Generate Report", "action_type": "script", "action_config": {"command": "python report.py"}, "depends_on": ["task-000"]},
    {"name": "Send Email", "action_type": "email", "action_config": {"to": "team@example.com"}, "depends_on": ["task-001"]},
])

# Execute
result = agent.execute_workflow(wf.workflow_id)
print(f"Status: {result['status']}")
```

### Run the Agent

```bash
python agents/automation/agent.py --status
python agents/automation/agent.py --workflow "Test" '[{"name":"Step1","action_type":"script","action_config":{"command":"echo hello"}}]'
```

---

## Installation

```bash
git clone https://github.com/LifeJiggy/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills
```

### Optional Dependencies

```bash
pip install schedule croniter python-dotenv requests
```

---

## Usage

### Workflow with Dependencies

```python
agent = AutomationAgent()

wf = agent.create_workflow(
    name="ETL Pipeline",
    tasks=[
        {
            "name": "Extract",
            "action_type": "http_request",
            "action_config": {"url": "https://source.com/data", "method": "GET"},
        },
        {
            "name": "Validate",
            "action_type": "script",
            "action_config": {"command": "python validate.py --input {{tasks.Extract.output}}"},
            "depends_on": ["task-000"],
            "timeout_seconds": 120,
        },
        {
            "name": "Transform",
            "action_type": "script",
            "action_config": {"command": "python transform.py --input {{tasks.Validate.output}}"},
            "depends_on": ["task-001"],
            "timeout_seconds": 300,
        },
        {
            "name": "Load",
            "action_type": "script",
            "action_config": {"command": "python load.py --input {{tasks.Transform.output}}"},
            "depends_on": ["task-002"],
            "timeout_seconds": 600,
            "max_retries": 3,
            "retry_strategy": "exponential",
            "compensation_action": {
                "type": "script",
                "config": {"command": "python rollback.py"},
            },
        },
        {
            "name": "Notify",
            "action_type": "notification",
            "action_config": {"channel": "slack", "recipient": "#data", "body": "ETL complete"},
            "depends_on": ["task-003"],
        },
    ],
    description="Complete ETL pipeline with validation and rollback",
    tags=["etl", "production"],
)

result = agent.execute_workflow(wf.workflow_id)
print(f"Status: {result['status']}, Duration: {result['duration_seconds']}s")
```

### Scheduling

```python
# Daily at 9 AM (weekdays only)
sched = agent.add_schedule(
    "Morning Report",
    wf.workflow_id,
    cron_expression="0 9 * * 1-5",
)

# Every hour
sched = agent.add_schedule(
    "Hourly Check",
    health_check_wf.workflow_id,
    interval_seconds=3600,
)

# Check what's due
due = agent.get_due_schedules()
for s in due:
    result = agent.execute_workflow(s.workflow_id)
    agent._scheduler.mark_executed(s.schedule_id)
    print(f"Executed {s.name}: {result['status']}")
```

### Email Campaigns

```python
# Create template
tmpl = agent.create_email_template(
    name="Monthly Update",
    subject="Monthly Update - {{month}}",
    body="Hi {{name}},\n\nHere's your monthly update for {{month}}.\n\nBest,\nThe Team",
    variables=["name", "month"],
)

# Send to one person
agent.send_email("john@example.com", tmpl.template_id, {"name": "John", "month": "July"})

# Bulk campaign
campaign = agent.create_email_campaign(
    name="July Newsletter",
    template_id=tmpl.template_id,
    recipients=["user1@example.com", "user2@example.com", "user3@example.com"],
)
result = agent.run_email_campaign(campaign.campaign_id)
print(f"Sent: {result['sent']}, Failed: {result['failed']}")
```

### File Operations

```python
# Watch a folder
watch = agent.watch_folder(
    path="/data/incoming",
    extensions=[".csv", ".json"],
    action="process_new_data",
    recursive=False,
)

# Copy CSV files
result = agent.process_files("/data/incoming", "copy", target="/data/processed", extensions=[".csv"])
print(f"Processed: {result['processed']}, Failed: {result['failed']}")

# Compress reports
agent.compress_directory("/reports", "/backups/reports.zip")

# Extract archives
agent.extract_archive("/backups/data.zip", "/data/extracted")
```

### Notifications

```python
# Multi-channel notifications
agent.send_notification("slack", "#ops-alerts", "Deployment Complete", "v2.1 deployed")
agent.send_notification("email", "team@example.com", "Alert", "High CPU usage detected")
agent.send_notification("webhook", "https://hooks.example.com", "Alert", '{"level":"warning"}')

# View history
notifications = agent.list_notifications(limit=10)
for n in notifications:
    print(f"[{n.channel}] {n.subject} → {n.status}")
```

---

## API Reference

### Core Methods

| Method | Description |
|--------|-------------|
| `create_workflow(name, tasks, ...)` | Create workflow with tasks |
| `execute_workflow(workflow_id)` | Execute a workflow |
| `get_workflow_status(workflow_id)` | Get execution status |
| `list_workflows()` | List all workflows |
| `cancel_workflow(workflow_id)` | Cancel running workflow |
| `get_execution_history(workflow_id)` | Get execution history |

### Scheduling

| Method | Description |
|--------|-------------|
| `add_schedule(name, workflow_id, ...)` | Create schedule |
| `remove_schedule(schedule_id)` | Remove schedule |
| `enable_schedule(schedule_id)` | Enable schedule |
| `disable_schedule(schedule_id)` | Disable schedule |
| `list_schedules()` | List all schedules |
| `get_due_schedules()` | Get schedules ready to run |

### Email

| Method | Description |
|--------|-------------|
| `create_email_template(name, subject, body)` | Create template |
| `send_email(to, template_id, variables)` | Send email |
| `create_email_campaign(name, template_id, recipients)` | Create campaign |
| `run_email_campaign(campaign_id)` | Execute campaign |
| `list_email_templates()` | List templates |
| `list_email_campaigns()` | List campaigns |

### File Operations

| Method | Description |
|--------|-------------|
| `watch_folder(path, extensions, action)` | Set up folder watch |
| `process_files(path, operation, target)` | Process files |
| `compress_directory(source, output)` | Create ZIP archive |
| `extract_archive(archive, destination)` | Extract archive |
| `list_file_watches()` | List active watches |

### Notifications

| Method | Description |
|--------|-------------|
| `send_notification(channel, recipient, subject, body)` | Send notification |
| `list_notifications(limit)` | List notification history |

---

## Data Models

### Workflow

```python
@dataclass
class Workflow:
    workflow_id: str              # Unique identifier
    name: str                     # Human-readable name
    description: str              # Workflow description
    tasks: List[Task]             # Ordered task list
    variables: Dict[str, Any]     # Workflow-level variables
    tags: List[str]               # Classification tags
    created_at: datetime          # Creation timestamp
    updated_at: datetime          # Last modification
    status: WorkflowStatus        # DRAFT, ACTIVE, COMPLETED, FAILED
```

### Task

```python
@dataclass
class Task:
    task_id: str                  # Unique identifier
    name: str                     # Human-readable name
    action_type: str              # "script", "http_request", "email", "notification", "file"
    action_config: Dict           # Action-specific configuration
    depends_on: List[str]         # List of task IDs this depends on
    timeout_seconds: int          # Execution timeout
    max_retries: int              # Maximum retry attempts
    retry_strategy: str           # "fixed", "linear", "exponential"
    compensation_action: Optional[Dict]  # Rollback action
    status: TaskStatus            # PENDING, RUNNING, COMPLETED, FAILED, SKIPPED
    output: Optional[str]         # Task output (set after execution)
    error: Optional[str]          # Error message (if failed)
```

### Schedule

```python
@dataclass
class Schedule:
    schedule_id: str              # Unique identifier
    name: str                     # Human-readable name
    workflow_id: str              # Associated workflow
    cron_expression: Optional[str]  # Cron schedule
    interval_seconds: Optional[int]  # Interval schedule
    enabled: bool                 # Whether active
    next_run: datetime            # Next scheduled execution
    last_run: Optional[datetime]  # Last execution time
    created_at: datetime          # Creation timestamp
```

---

## Examples

### Parallel Execution

```python
# Tasks without dependencies run in parallel
wf = agent.create_workflow("Parallel Tasks", [
    {"name": "Task A", "action_type": "script", "action_config": {"command": "echo A"}},
    {"name": "Task B", "action_type": "script", "action_config": {"command": "echo B"}},
    {"name": "Task C", "action_type": "script", "action_config": {"command": "echo C"}},
    {
        "name": "Summary",
        "action_type": "script",
        "action_config": {"command": "echo Done"},
        "depends_on": ["task-000", "task-001", "task-002"],
    },
])
# A, B, C run in parallel; Summary waits for all three
```

### Retry with Exponential Backoff

```python
wf = agent.create_workflow("Retry Example", [
    {
        "name": "Flaky API Call",
        "action_type": "http_request",
        "action_config": {"url": "https://unstable-api.com/data"},
        "max_retries": 5,
        "retry_strategy": "exponential",
        "timeout_seconds": 60,
    },
])
```

### Conditional Workflow with Variables

```python
wf = agent.create_workflow("Data Sync", [
    {
        "name": "Check Source",
        "action_type": "http_request",
        "action_config": {"url": "https://source.com/status"},
    },
    {
        "name": "Sync Data",
        "action_type": "script",
        "action_config": {"command": "python sync.py --since {{tasks.CheckSource.last_modified}}"},
        "depends_on": ["task-000"],
    },
], variables={"source_url": "https://source.com"})
```

### Multi-Channel Notification

```python
# Alert operations team via multiple channels
for channel, recipient in [
    ("slack", "#ops-alerts"),
    ("email", "ops@example.com"),
    ("webhook", "https://pagerduty.example.com"),
]:
    agent.send_notification(channel, recipient, "Service Down", "API returning 503")
```

---

## Configuration

```python
from agents.automation.agent import Config

config = Config(
    max_concurrent_workflows=8,
    default_task_timeout=600,
    default_workflow_timeout=7200,
    max_retries=5,
    retry_delay_seconds=10,
    history_retention_days=180,
    email_smtp_host="smtp.example.com",
    email_smtp_port=587,
    email_from="automation@example.com",
    slack_webhook_url="https://hooks.slack.com/...",
    webhook_timeout_seconds=30,
    file_watch_interval_seconds=10,
    max_parallel_tasks=4,
    enable_compensation=True,
    log_level="INFO",
)

agent = AutomationAgent(config=config)
```

---

## Best Practices

1. **Keep Tasks Small**: Each task should do one thing well
2. **Idempotent Tasks**: Design tasks to be safely retryable without side effects
3. **Set Timeouts**: Always set reasonable timeouts on tasks
4. **Use Compensation**: Add rollback actions for critical operations (database writes, deployments)
5. **Monitor Execution**: Check `get_execution_history()` regularly
6. **Test Workflows**: Run with `max_parallel=1` for debugging
7. **Clean Up History**: Set appropriate `history_retention_days`
8. **Name Descriptively**: Workflow and task names should describe what they do
9. **Use Variables**: Pass configuration via `variables` dict, not hardcoded values
10. **Verify Cron Expressions**: Use crontab.guru to validate before deploying
11. **Prefer UTC**: Use UTC for all schedules to avoid timezone confusion
12. **Alert on Failure**: Always configure failure notifications

---

## Security

### Credential Management

- SMTP credentials via environment variables, not config files
- Webhook URLs stored encrypted
- No secrets in workflow definitions
- Audit log of all credential access

### Execution Safety

```python
# Sandboxed execution
config = Config(
    enable_compensation=True,      # Always have rollback path
    default_task_timeout=600,      # Prevent runaway tasks
    max_parallel_tasks=4,          # Resource limits
    log_level="INFO",              # Audit trail
)
```

### Input Validation

- Task configurations validated before execution
- File paths sanitized against traversal
- Webhook URLs validated against SSRF
- Email recipients validated against injection

---

## Scalability

### Performance Targets

| Operation | Latency | Throughput |
|-----------|---------|------------|
| Workflow creation | < 100ms | 1,000/sec |
| Task execution | Varies | 4 parallel tasks |
| Schedule check | < 50ms | 10,000/sec |
| Email send | < 1s | 100/sec |
| Notification dispatch | < 500ms | 500/sec |

### Scaling Strategies

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Single    │────▶│  Worker     │────▶│  Distributed│
│   Node      │     │  Pool       │     │  Cluster    │
└─────────────┘     └─────────────┘     └─────────────┘
      │                    │                    │
      ▼                    ▼                    ▼
  < 100 workflows   100-1K workflows   1K+ workflows
  4 parallel tasks  16 parallel tasks  64+ parallel tasks
```

### Resource Management

```python
config = Config(
    max_concurrent_workflows=8,     # Limit concurrent workflows
    max_parallel_tasks=4,           # Limit parallel tasks
    default_task_timeout=600,       # Prevent resource exhaustion
    history_retention_days=180,     # Clean up old data
)
```

---

## Design Patterns

### DAG Pattern — Workflow Execution

```python
# Topological sort ensures correct execution order
def execute_dag(tasks):
    sorted_tasks = topological_sort(tasks)
    for task in sorted_tasks:
        if all_dependencies_met(task):
            execute_task(task)
```

### Strategy Pattern — Retry Logic

```python
class RetryStrategy:
    def wait_time(self, attempt: int) -> float:
        raise NotImplementedError

class ExponentialBackoff(RetryStrategy):
    def wait_time(self, attempt):
        return min(2 ** attempt * base_delay, max_delay)

class LinearBackoff(RetryStrategy):
    def wait_time(self, attempt):
        return attempt * base_delay
```

### Observer Pattern — Notifications

```python
class NotificationObserver:
    def on_workflow_complete(self, workflow):
        pass

class SlackObserver(NotificationObserver):
    def on_workflow_complete(self, workflow):
        send_slack(f"Workflow {workflow.name} completed")
```

### Command Pattern — Task Actions

```python
class TaskAction:
    def execute(self, config):
        raise NotImplementedError

class ScriptAction(TaskAction):
    def execute(self, config):
        return subprocess.run(config["command"], shell=True)

class HttpRequestAction(TaskAction):
    def execute(self, config):
        return requests.get(config["url"])
```

---

## Troubleshooting

| Problem | Cause | Resolution |
|---------|-------|------------|
| Workflow deadlocked | Circular dependency | Check `depends_on` for cycles in DAG |
| Task timeout | Task too slow or hung | Increase `timeout_seconds`; check task logic |
| Schedule not firing | Disabled or future `next_run` | Check `enabled` flag and `next_run` time |
| Email not sent | Template not found | Verify `template_id` exists in templates |
| File operation failed | Path doesn't exist | Verify path with `Path.exists()` before operation |
| Retry exhausted | Task fundamentally broken | Fix the handler logic; don't just increase retry count |
| Compensation failed | Compensation action errors | Test compensation actions independently first |
| Workflow variable undefined | Missing variable in config | Define all variables in `variables` dict |
| Notification channel invalid | Channel not configured | Check channel config (SMTP, webhook URL, etc.) |
| DAG too deep | Excessive nesting | Flatten workflow; split into sub-workflows |

---

## Additional Examples

### Example: Database Backup Workflow

```python
wf = agent.create_workflow("Database Backup", [
    {
        "name": "Create Snapshot",
        "action_type": "script",
        "action_config": {"command": "pg_dump -Fc mydb > /backups/mydb.dump"},
        "timeout_seconds": 600,
    },
    {
        "name": "Upload to S3",
        "action_type": "http_request",
        "action_config": {
            "url": "https://s3.amazonaws.com/my-backups",
            "method": "PUT",
            "body": "{{tasks.CreateSnapshot.output}}"
        },
        "depends_on": ["task-000"],
        "max_retries": 3,
        "retry_strategy": "exponential",
    },
    {
        "name": "Verify Upload",
        "action_type": "script",
        "action_config": {"command": "aws s3 ls s3://my-backups/mydb.dump"},
        "depends_on": ["task-001"],
    },
    {
        "name": "Notify Team",
        "action_type": "notification",
        "action_config": {
            "channel": "slack",
            "recipient": "#ops",
            "body": "Database backup completed successfully"
        },
        "depends_on": ["task-002"],
    },
], tags=["backup", "database", "scheduled"])

# Schedule daily at 2 AM
agent.add_schedule("Daily Backup", wf.workflow_id, cron_expression="0 2 * * *")
```

### Example: File Processing Pipeline

```python
wf = agent.create_workflow("CSV Processing", [
    {
        "name": "Watch Incoming",
        "action_type": "file_watch",
        "action_config": {
            "path": "/data/incoming",
            "extensions": [".csv"],
            "action": "process"
        },
    },
    {
        "name": "Validate Data",
        "action_type": "script",
        "action_config": {"command": "python validate.py --input {{tasks.WatchIncoming.file_path}}"},
        "depends_on": ["task-000"],
        "timeout_seconds": 300,
    },
    {
        "name": "Transform",
        "action_type": "script",
        "action_config": {"command": "python transform.py --input {{tasks.ValidateData.output}}"},
        "depends_on": ["task-001"],
        "timeout_seconds": 600,
    },
    {
        "name": "Load to Database",
        "action_type": "script",
        "action_config": {"command": "python load.py --input {{tasks.Transform.output}}"},
        "depends_on": ["task-002"],
        "max_retries": 3,
        "retry_strategy": "exponential",
        "compensation_action": {
            "type": "script",
            "config": {"command": "python rollback.py"}
        },
    },
    {
        "name": "Archive Processed",
        "action_type": "file_operation",
        "action_config": {
            "operation": "move",
            "source": "{{tasks.WatchIncoming.file_path}}",
            "target": "/data/processed/"
        },
        "depends_on": ["task-003"],
    },
], tags=["etl", "csv", "automated"])
```

### Example: Multi-Stage Deployment

```python
wf = agent.create_workflow("Deploy to Production", [
    {
        "name": "Run Tests",
        "action_type": "script",
        "action_config": {"command": "pytest tests/ -v"},
        "timeout_seconds": 600,
    },
    {
        "name": "Build Docker Image",
        "action_type": "script",
        "action_config": {"command": "docker build -t myapp:${VERSION} ."},
        "depends_on": ["task-000"],
        "timeout_seconds": 300,
    },
    {
        "name": "Push to Registry",
        "action_type": "script",
        "action_config": {"command": "docker push myapp:${VERSION}"},
        "depends_on": ["task-001"],
        "max_retries": 2,
    },
    {
        "name": "Update Staging",
        "action_type": "script",
        "action_config": {"command": "kubectl set image deployment/myapp myapp=myapp:${VERSION}"},
        "depends_on": ["task-002"],
    },
    {
        "name": "Run Smoke Tests",
        "action_type": "http_request",
        "action_config": {"url": "https://staging.example.com/health"},
        "depends_on": ["task-003"],
        "timeout_seconds": 60,
    },
    {
        "name": "Deploy to Production",
        "action_type": "script",
        "action_config": {"command": "kubectl set image deployment/myapp myapp=myapp:${VERSION} -n production"},
        "depends_on": ["task-004"],
        "compensation_action": {
            "type": "script",
            "config": {"command": "kubectl rollout undo deployment/myapp -n production"}
        },
    },
    {
        "name": "Notify Deployment",
        "action_type": "notification",
        "action_config": {
            "channel": "slack",
            "recipient": "#deployments",
            "body": "Production deployment complete: ${VERSION}"
        },
        "depends_on": ["task-005"],
    },
], tags=["deployment", "production", "multi-stage"])
```

### Example: Monitoring and Alerting Workflow

```python
wf = agent.create_workflow("Health Check Pipeline", [
    {
        "name": "Check API Health",
        "action_type": "http_request",
        "action_config": {"url": "https://api.example.com/health"},
        "timeout_seconds": 30,
    },
    {
        "name": "Check Database",
        "action_type": "script",
        "action_config": {"command": "pg_isready -h db.example.com"},
        "timeout_seconds": 10,
    },
    {
        "name": "Check Cache",
        "action_type": "script",
        "action_config": {"command": "redis-cli -h cache.example.com ping"},
        "timeout_seconds": 10,
    },
    {
        "name": "Aggregate Results",
        "action_type": "script",
        "action_config": {"command": "python check_results.py"},
        "depends_on": ["task-000", "task-001", "task-002"],
    },
    {
        "name": "Alert if Down",
        "action_type": "notification",
        "action_config": {
            "channel": "pagerduty",
            "recipient": "oncall",
            "body": "Service health check failed"
        },
        "depends_on": ["task-003"],
    },
], tags=["monitoring", "health-check", "scheduled"])

# Run every 5 minutes
agent.add_schedule("Health Check", wf.workflow_id, interval_seconds=300)
```

## Files

- `agent.py` — Full implementation with workflow engine, scheduler, email, file ops
- `ARCHITECTURE.md` — System architecture with ASCII diagrams
- `GROK.md` — Agent identity, capabilities, and usage patterns
- `README.md` — This file

---

## License

MIT License — see [LICENSE](../../LICENSE).

---

*Automation Agent v2.0 — Part of the Awesome Grok Skills collection.*
