# Automation Agent

> Business process automation, workflow orchestration, scheduling, and task management.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Quick Start](#quick-start)
4. [Installation](#installation)
5. [Usage](#usage)
6. [API Reference](#api-reference)
7. [Examples](#examples)
8. [Configuration](#configuration)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)
11. [License](#license)

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
