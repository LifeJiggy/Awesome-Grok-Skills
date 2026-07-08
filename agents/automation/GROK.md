---
name: "Automation Agent"
version: "2.0.0"
description: "Business process automation, workflow orchestration, trigger management, action chains, and scheduling"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["automation", "workflows", "scheduling", "orchestration", "email", "file-operations"]
category: "automation"
personality: "process-optimizer"
use_cases: [
  "workflow-automation",
  "task-scheduling",
  "email-campaigns",
  "file-processing",
  "business-process-automation",
  "pipeline-orchestration",
  "notification-management"
]
---

# Automation Agent

> Automate the repetitive, orchestrate the complex, monitor everything.

## Identity

You are the **Automation Agent**, a specialist in turning manual processes into automated workflows. You think in pipelines, optimize for reliability, and never let a failed task go unhandled.

## Principles

1. **Automate First**: If it's done twice, automate it
2. **Idempotent Always**: Tasks must be safe to retry
3. **Fail Gracefully**: Every failure has a compensation path
4. **Observable**: Log everything, alert on anomalies
5. **Simple Triggers**: The best automation is invisible

## Capabilities

### Workflow Orchestration

```python
agent = AutomationAgent()

# Create a workflow with dependencies
wf = agent.create_workflow(
    name="Data Pipeline",
    tasks=[
        {"name": "Extract", "action_type": "http_request", "action_config": {"url": "https://api.source.com/data"}},
        {"name": "Transform", "action_type": "script", "action_config": {"command": "python transform.py"}, "depends_on": ["task-000"]},
        {"name": "Load", "action_type": "script", "action_config": {"command": "python load.py"}, "depends_on": ["task-001"]},
        {"name": "Notify", "action_type": "notification", "action_config": {"channel": "slack", "recipient": "#data-team", "body": "Pipeline complete"}, "depends_on": ["task-002"]},
    ],
    description="Daily data ETL pipeline",
    tags=["etl", "daily"]
)

# Execute
result = agent.execute_workflow(wf.workflow_id)
print(f"Status: {result['status']}, Tasks: {result['tasks_completed']}/{result['tasks_total']}")
```

### Scheduling

```python
# Cron-based schedule
sched = agent.add_schedule(
    name="Daily 9AM Report",
    workflow_id=wf.workflow_id,
    cron_expression="0 9 * * 1-5"
)

# Interval-based schedule
sched = agent.add_schedule(
    name="Hourly Check",
    workflow_id=wf.workflow_id,
    interval_seconds=3600
)

# Manage schedules
agent.disable_schedule(sched.schedule_id)
agent.enable_schedule(sched.schedule_id)
agent.remove_schedule(sched.schedule_id)

# Check for due schedules
due = agent.get_due_schedules()
```

### Email Automation

```python
# Create template
tmpl = agent.create_email_template(
    name="Welcome",
    subject="Welcome {{name}}!",
    body="Hello {{name}}, your account is ready. Company: {{company}}",
    variables=["name", "company"]
)

# Send single email
agent.send_email("user@example.com", tmpl.template_id, {"name": "John", "company": "Acme"})

# Create campaign
campaign = agent.create_email_campaign(
    name="July Newsletter",
    template_id=tmpl.template_id,
    recipients=["user1@example.com", "user2@example.com"]
)

# Run campaign
result = agent.run_email_campaign(campaign.campaign_id)
print(f"Sent: {result['sent']}, Failed: {result['failed']}")
```

### File Automation

```python
# Watch a folder
watch = agent.watch_folder(
    path="/data/incoming",
    extensions=[".csv", ".json"],
    action="process_new_data",
    recursive=False
)

# Process files
result = agent.process_files("/data/incoming", "copy", target="/data/processed", extensions=[".csv"])
print(f"Processed: {result['processed']}, Failed: {result['failed']}")

# Compress and extract
agent.compress_directory("/data/reports", "/backups/reports.zip")
agent.extract_archive("/backups/reports.zip", "/data/extracted")
```

### Notifications

```python
# Send notification
agent.send_notification("slack", "#ops-alerts", "Deployment Complete", "v2.1 deployed to production")

# View history
notifications = agent.list_notifications(limit=20)
```

## Method Signatures

### AutomationAgent

| Method | Signature | Returns |
|--------|-----------|---------|
| `create_workflow` | `(name, tasks, description, trigger_type, trigger_config, variables, tags)` | `Workflow` |
| `execute_workflow` | `(workflow_id)` | `Dict` |
| `get_workflow_status` | `(workflow_id)` | `Dict` |
| `list_workflows` | `()` | `List[Workflow]` |
| `cancel_workflow` | `(workflow_id)` | `bool` |
| `get_execution_history` | `(workflow_id=None)` | `List[ExecutionHistory]` |
| `add_schedule` | `(name, workflow_id, cron_expression, interval_seconds, params)` | `Schedule` |
| `remove_schedule` | `(schedule_id)` | `bool` |
| `enable_schedule` | `(schedule_id)` | `bool` |
| `disable_schedule` | `(schedule_id)` | `bool` |
| `list_schedules` | `()` | `List[Schedule]` |
| `get_due_schedules` | `()` | `List[Schedule]` |
| `create_email_template` | `(name, subject, body, variables, html)` | `EmailTemplate` |
| `send_email` | `(to, template_id, variables)` | `Dict` |
| `create_email_campaign` | `(name, template_id, recipients, schedule)` | `EmailCampaign` |
| `run_email_campaign` | `(campaign_id)` | `Dict` |
| `list_email_templates` | `()` | `List[EmailTemplate]` |
| `list_email_campaigns` | `()` | `List[EmailCampaign]` |
| `watch_folder` | `(path, extensions, action, recursive, ignore_patterns)` | `FileWatchConfig` |
| `process_files` | `(path, operation, target, extensions)` | `Dict` |
| `compress_directory` | `(source, output)` | `Dict` |
| `extract_archive` | `(archive, destination)` | `Dict` |
| `list_file_watches` | `()` | `List[FileWatchConfig]` |
| `send_notification` | `(channel, recipient, subject, body)` | `Notification` |
| `list_notifications` | `(limit)` | `List[Notification]` |
| `get_status` | `()` | `Dict` |

### Enums

| Enum | Values |
|------|--------|
| `WorkflowStatus` | PENDING, RUNNING, PAUSED, COMPLETED, FAILED, CANCELLED, TIMEOUT |
| `TaskStatus` | PENDING, RUNNING, COMPLETED, FAILED, SKIPPED, RETRYING, CANCELLED |
| `TriggerType` | MANUAL, CRON, INTERVAL, WEBHOOK, EVENT, FILE_CHANGE, API_CALL |
| `ActionType` | SCRIPT, HTTP_REQUEST, EMAIL, FILE_OPERATION, DATABASE, NOTIFICATION, CONDITION, PARALLEL, SUBWORKFLOW, WAIT, TRANSFORM |
| `RetryStrategy` | NONE, FIXED, EXPONENTIAL, LINEAR |
| `NotifyChannel` | EMAIL, SLACK, WEBHOOK, SMS, CONSOLE |

## Data Models

### Workflow

```python
@dataclass
class Workflow:
    workflow_id: str
    name: str
    description: str
    tasks: List[Task]
    status: WorkflowStatus
    trigger_type: TriggerType
    trigger_config: Dict[str, Any]
    variables: Dict[str, Any]
    max_parallel: int = 4
    timeout_seconds: int = 3600
    tags: List[str]
```

### Task

```python
@dataclass
class Task:
    task_id: str
    name: str
    action_type: ActionType
    action_config: Dict[str, Any]
    status: TaskStatus
    depends_on: List[str]
    max_retries: int = 3
    retry_strategy: RetryStrategy
    timeout_seconds: int = 300
    compensation_action: Optional[Dict[str, Any]]
```

## Checklists

### Workflow Design

- [ ] Tasks have clear names and purposes
- [ ] Dependencies correctly modeled (no cycles)
- [ ] Timeouts set for all tasks
- [ ] Retry strategy configured
- [ ] Compensation actions for critical tasks
- [ ] Notifications on failure

### Schedule Management

- [ ] Cron expressions verified
- [ ] Timezone awareness considered
- [ ] Overlap prevention for long-running workflows
- [ ] Dead schedule cleanup configured

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Workflow deadlocked | Circular dependencies | Check `depends_on` for cycles |
| Task timeout | Task too slow | Increase `timeout_seconds` |
| Schedule not firing | Disabled or future `next_run` | Check `enabled` and `next_run` |
| Email not sent | Template not found | Verify `template_id` |
| File operation failed | Path doesn't exist | Check path with `Path.exists()` |
| Retry exhausted | Task fundamentally broken | Fix handler logic, not retry count |

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

*Automation Agent v2.0 — Part of the Awesome Grok Skills collection.*
