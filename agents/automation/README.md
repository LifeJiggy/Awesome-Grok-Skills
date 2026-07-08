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

The Automation Agent provides end-to-end business process automation with a DAG-based workflow engine, cron/interval scheduling, email automation, file system operations, and notification management.

### What It Does

- **Workflow Orchestration**: DAG-based task execution with dependencies and parallel runs
- **Scheduling**: Cron expressions and interval-based triggers
- **Retry & Rollback**: Configurable retry strategies with compensation actions
- **Email Automation**: Templates with variable substitution and bulk campaigns
- **File Operations**: Watch, copy, move, delete, compress, extract
- **Notifications**: Multi-channel alerts (email, Slack, webhook, SMS, console)
- **Execution History**: Full audit trail with duration and status tracking

---

## Features

| Feature | Description |
|---------|-------------|
| DAG Execution | Topological sort for dependency resolution |
| Parallel Tasks | Independent tasks run concurrently |
| Retry Strategies | Fixed, linear, exponential backoff |
| Compensation | Rollback actions for failed tasks |
| Cron Scheduling | Standard cron expression support |
| Email Templates | Variable substitution and campaigns |
| File Watching | Monitor folders for changes |
| Multi-Channel | Email, Slack, webhook, SMS, console |
| Audit Trail | Full execution history |

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

---

## Usage

### Workflow with Dependencies

```python
agent = AutomationAgent()

wf = agent.create_workflow(
    name="ETL Pipeline",
    tasks=[
        {"name": "Extract", "action_type": "http_request", "action_config": {"url": "https://source.com/data"}},
        {"name": "Validate", "action_type": "script", "action_config": {"command": "python validate.py"}, "depends_on": ["task-000"]},
        {"name": "Transform", "action_type": "script", "action_config": {"command": "python transform.py"}, "depends_on": ["task-001"]},
        {"name": "Load", "action_type": "script", "action_config": {"command": "python load.py"}, "depends_on": ["task-002"]},
        {"name": "Notify", "action_type": "notification", "action_config": {"channel": "slack", "recipient": "#data", "body": "Done"}, "depends_on": ["task-003"]},
    ],
    description="Complete ETL pipeline",
    tags=["etl", "production"]
)

result = agent.execute_workflow(wf.workflow_id)
```

### Scheduling

```python
# Daily at 9 AM
sched = agent.add_schedule("Morning Report", wf.workflow_id, cron_expression="0 9 * * *")

# Every hour
sched = agent.add_schedule("Hourly Check", wf.workflow_id, interval_seconds=3600)

# Check what's due
due = agent.get_due_schedules()
for s in due:
    agent.execute_workflow(s.workflow_id)
    agent._scheduler.mark_executed(s.schedule_id)
```

### Email Campaigns

```python
# Create template
tmpl = agent.create_email_template(
    name="Monthly Update",
    subject="Monthly Update - {{month}}",
    body="Hi {{name}},\n\nHere's your monthly update for {{month}}.\n\nBest,\nThe Team"
)

# Send to one person
agent.send_email("john@example.com", tmpl.template_id, {"name": "John", "month": "July"})

# Bulk campaign
campaign = agent.create_email_campaign(
    name="July Newsletter",
    template_id=tmpl.template_id,
    recipients=["user1@example.com", "user2@example.com", "user3@example.com"]
)
result = agent.run_email_campaign(campaign.campaign_id)
```

### File Operations

```python
# Copy CSV files
result = agent.process_files("/data/incoming", "copy", target="/data/processed", extensions=[".csv"])

# Compress reports
agent.compress_directory("/reports", "/backups/reports.zip")

# Extract archives
agent.extract_archive("/backups/data.zip", "/data/extracted")
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

---

## Examples

### Parallel Execution

```python
# Tasks without dependencies run in parallel
wf = agent.create_workflow("Parallel Tasks", [
    {"name": "Task A", "action_type": "script", "action_config": {"command": "echo A"}},
    {"name": "Task B", "action_type": "script", "action_config": {"command": "echo B"}},
    {"name": "Task C", "action_type": "script", "action_config": {"command": "echo C"}},
    {"name": "Summary", "action_type": "script", "action_config": {"command": "echo Done"}, "depends_on": ["task-000", "task-001", "task-002"]},
])
# A, B, C run in parallel; Summary waits for all three
```

### Retry with Backoff

```python
wf = agent.create_workflow("Retry Example", [
    {
        "name": "Flaky API Call",
        "action_type": "http_request",
        "action_config": {"url": "https://unstable-api.com/data"},
        "max_retries": 5,
        "retry_strategy": "exponential",
        "timeout_seconds": 60
    },
])
```

---

## Configuration

```python
from agent import Config

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
)

agent = AutomationAgent(config=config)
```

---

## Best Practices

1. **Keep Tasks Small**: Each task should do one thing well
2. **Idempotent Tasks**: Design tasks to be safely retryable
3. **Set Timeouts**: Always set reasonable timeouts on tasks
4. **Use Compensation**: Add rollback actions for critical operations
5. **Monitor Execution**: Check `get_execution_history()` regularly
6. **Test Workflows**: Run with `max_parallel=1` for debugging
7. **Clean Up History**: Set appropriate `history_retention_days`

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Workflow deadlocked | Circular dependency | Check `depends_on` for cycles |
| Task timeout | Task too slow | Increase `timeout_seconds` |
| Schedule not firing | Disabled or future `next_run` | Check `enabled` and `next_run` |
| Email not sent | Template not found | Verify `template_id` exists |
| File operation failed | Path doesn't exist | Verify path before operation |
| Retry exhausted | Task fundamentally broken | Fix the handler logic |

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
