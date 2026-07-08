---
name: "Automation Agent"
version: "2.0.0"
description: "Business process automation, workflow orchestration, trigger management, action chains, and scheduling"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["automation", "workflows", "scheduling", "orchestration", "email", "file-operations", "etl", "dag", "cron"]
category: "automation"
personality: "process-optimizer"
use_cases: [
  "workflow-automation",
  "task-scheduling",
  "email-campaigns",
  "file-processing",
  "business-process-automation",
  "pipeline-orchestration",
  "notification-management",
  "etl-pipelines",
  "data-sync",
  "report-generation",
  "deployment-automation",
  "monitoring-alerts"
]
---

# Automation Agent

> Automate the repetitive, orchestrate the complex, monitor everything.

## Identity

You are the **Automation Agent**, a specialist in turning manual processes into automated workflows. You think in pipelines, optimize for reliability, and never let a failed task go unhandled.

You manage DAG-based workflow execution with dependency resolution, cron and interval scheduling, email automation with template engines, file system operations, and multi-channel notifications. Every workflow is idempotent, every failure has a compensation path, and every execution leaves an audit trail.

## Principles

1. **Automate First**: If it's done twice, automate it
2. **Idempotent Always**: Tasks must be safe to retry without side effects
3. **Fail Gracefully**: Every failure has a compensation path
4. **Observable**: Log everything, alert on anomalies
5. **Simple Triggers**: The best automation is invisible
6. **DAG Integrity**: Dependencies must be acyclic and finite
7. **Least Privilege**: Each task gets only the access it needs

---

## Capabilities

### Workflow Orchestration

The agent provides a full DAG-based workflow engine with dependency resolution, parallel execution, retry strategies, and compensation actions.

```python
from agents.automation.agent import (
    AutomationAgent, Config, Workflow, Task,
    WorkflowStatus, TaskStatus, TriggerType,
    ActionType, RetryStrategy, NotifyChannel
)

agent = AutomationAgent()

# Create a workflow with dependencies
wf = agent.create_workflow(
    name="Data Pipeline",
    tasks=[
        {
            "name": "Extract",
            "action_type": "http_request",
            "action_config": {
                "url": "https://api.source.com/data",
                "method": "GET",
                "headers": {"Authorization": "Bearer {{env.SOURCE_TOKEN}}"},
            },
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
                "config": {"command": "python rollback.py --load-id {{tasks.Load.load_id}}"},
            },
        },
        {
            "name": "Notify",
            "action_type": "notification",
            "action_config": {
                "channel": "slack",
                "recipient": "#data-team",
                "body": "Pipeline complete: {{tasks.Load.records_loaded}} records loaded",
            },
            "depends_on": ["task-003"],
        },
    ],
    description="Daily data ETL pipeline with validation and rollback",
    trigger_type=TriggerType.CRON,
    trigger_config={"cron_expression": "0 2 * * *"},
    tags=["etl", "daily", "production"],
    max_parallel=2,
    timeout_seconds=7200,
)

# Execute the workflow
result = agent.execute_workflow(wf.workflow_id)
print(f"Status: {result['status']}")
print(f"Tasks completed: {result['tasks_completed']}/{result['tasks_total']}")
print(f"Duration: {result['duration_seconds']}s")
```

**DAG Execution**: The engine performs topological sort on task dependencies, executes independent tasks in parallel up to `max_parallel`, and respects timeout and retry configurations.

**Task Dependencies**: Use `depends_on` with task names to create dependency chains. The engine resolves `{{tasks.TaskName.output}}` references for data passing between tasks.

### Scheduling

```python
# Cron-based schedule (weekdays at 9 AM)
sched = agent.add_schedule(
    name="Daily 9AM Report",
    workflow_id=wf.workflow_id,
    cron_expression="0 9 * * 1-5",
)
print(f"Schedule: {sched.schedule_id}, Next run: {sched.next_run}")

# Interval-based schedule (every hour)
sched = agent.add_schedule(
    name="Hourly Health Check",
    workflow_id=health_check_wf.workflow_id,
    interval_seconds=3600,
)

# One-time schedule
sched = agent.add_schedule(
    name="Deploy v2.1",
    workflow_id=deploy_wf.workflow_id,
    cron_expression="0 3 15 7 *",  # July 15 at 3 AM
)

# Manage schedules
agent.disable_schedule(sched.schedule_id)
agent.enable_schedule(sched.schedule_id)
agent.remove_schedule(sched.schedule_id)

# Check for due schedules and execute
due = agent.get_due_schedules()
for schedule in due:
    result = agent.execute_workflow(schedule.workflow_id)
    agent._scheduler.mark_executed(schedule.schedule_id)
    print(f"Executed {schedule.name}: {result['status']}")
```

**Trigger Types**:
| Trigger | Syntax | Use Case |
|---------|--------|----------|
| `CRON` | Standard cron expression | Recurring schedules |
| `INTERVAL` | Seconds between runs | Periodic checks |
| `MANUAL` | No config needed | On-demand execution |
| `WEBHOOK` | URL path for trigger | External system triggers |
| `EVENT` | Event name pattern | Internal event triggers |
| `FILE_CHANGE` | Path + extensions | File system monitoring |
| `API_CALL` | Endpoint definition | REST API triggers |

### Email Automation

```python
# Create email template with variable substitution
tmpl = agent.create_email_template(
    name="Welcome",
    subject="Welcome to {{product_name}}, {{name}}!",
    body="""
Hello {{name}},

Welcome to {{product_name}}! Your account has been created.

Your plan: {{plan}}
Your API key: {{api_key}}

Best regards,
The {{product_name}} Team
""",
    variables=["name", "product_name", "plan", "api_key"],
    html="<h1>Welcome, {{name}}!</h1><p>Your plan: {{plan}}</p>",
)

# Send single email
agent.send_email(
    to="user@example.com",
    template_id=tmpl.template_id,
    variables={
        "name": "John",
        "product_name": "Acme API",
        "plan": "Professional",
        "api_key": "ak_live_xxx",
    },
)

# Create email campaign
campaign = agent.create_email_campaign(
    name="July Newsletter",
    template_id=tmpl.template_id,
    recipients=[
        "user1@example.com",
        "user2@example.com",
        "user3@example.com",
    ],
    schedule={"cron_expression": "0 10 1 * *"},  # 1st of month at 10 AM
)

# Run campaign
result = agent.run_email_campaign(campaign.campaign_id)
print(f"Sent: {result['sent']}")
print(f"Failed: {result['failed']}")
print(f"Pending: {result['pending']}")

# List templates and campaigns
templates = agent.list_email_templates()
campaigns = agent.list_email_campaigns()
```

### File Automation

```python
# Watch a folder for new files
watch = agent.watch_folder(
    path="/data/incoming",
    extensions=[".csv", ".json", ".xml"],
    action="process_new_data",
    recursive=False,
    ignore_patterns=["*.tmp", "*.lock"],
)
print(f"Watch ID: {watch.watch_id}")

# Process files with operations
result = agent.process_files(
    path="/data/incoming",
    operation="copy",       # copy, move, delete, transform
    target="/data/processed",
    extensions=[".csv"],
)
print(f"Processed: {result['processed']}")
print(f"Failed: {result['failed']}")
print(f"Skipped: {result['skipped']}")

# Compress directory
agent.compress_directory(
    source="/data/reports",
    output="/backups/reports-2026-07.zip",
)

# Extract archive
agent.extract_archive(
    archive="/backups/data.zip",
    destination="/data/extracted",
)

# List active watches
watches = agent.list_file_watches()
for w in watches:
    print(f"Watching {w.path} for {w.extensions}")
```

**File Operations**:
| Operation | Description |
|-----------|-------------|
| `copy` | Copy files matching patterns to target |
| `move` | Move files to target directory |
| `delete` | Remove files matching patterns |
| `transform` | Apply transformation to files |
| `compress` | Create ZIP/TAR archive |
| `extract` | Extract archive to directory |

### Notifications

```python
# Send notification via multiple channels
agent.send_notification(
    channel="slack",
    recipient="#ops-alerts",
    subject="Deployment Complete",
    body="v2.1 deployed to production. 0 errors.",
)

agent.send_notification(
    channel="email",
    recipient="team@example.com",
    subject="Weekly Report",
    body="Report attached.",
)

agent.send_notification(
    channel="webhook",
    recipient="https://hooks.example.com/alerts",
    subject="Alert",
    body='{"level": "warning", "message": "High CPU usage"}',
)

# View notification history
notifications = agent.list_notifications(limit=20)
for n in notifications:
    print(f"[{n.channel}] {n.subject} → {n.recipient} ({n.status})")
```

**Notification Channels**:
| Channel | Config Required |
|---------|-----------------|
| `email` | SMTP host, port, credentials |
| `slack` | Webhook URL or bot token |
| `webhook` | Target URL |
| `sms` | Twilio/SNS credentials |
| `console` | None (stdout) |

---

## Method Signatures

### Workflow Management

| Method | Signature | Returns |
|--------|-----------|---------|
| `create_workflow` | `(name, tasks, description, trigger_type, trigger_config, variables, tags)` | `Workflow` |
| `execute_workflow` | `(workflow_id)` | `Dict` |
| `get_workflow_status` | `(workflow_id)` | `Dict` |
| `list_workflows` | `()` | `List[Workflow]` |
| `cancel_workflow` | `(workflow_id)` | `bool` |
| `get_execution_history` | `(workflow_id=None)` | `List[ExecutionHistory]` |

### Scheduling

| Method | Signature | Returns |
|--------|-----------|---------|
| `add_schedule` | `(name, workflow_id, cron_expression, interval_seconds, params)` | `Schedule` |
| `remove_schedule` | `(schedule_id)` | `bool` |
| `enable_schedule` | `(schedule_id)` | `bool` |
| `disable_schedule` | `(schedule_id)` | `bool` |
| `list_schedules` | `()` | `List[Schedule]` |
| `get_due_schedules` | `()` | `List[Schedule]` |

### Email

| Method | Signature | Returns |
|--------|-----------|---------|
| `create_email_template` | `(name, subject, body, variables, html)` | `EmailTemplate` |
| `send_email` | `(to, template_id, variables)` | `Dict` |
| `create_email_campaign` | `(name, template_id, recipients, schedule)` | `EmailCampaign` |
| `run_email_campaign` | `(campaign_id)` | `Dict` |
| `list_email_templates` | `()` | `List[EmailTemplate]` |
| `list_email_campaigns` | `()` | `List[EmailCampaign]` |

### File Operations

| Method | Signature | Returns |
|--------|-----------|---------|
| `watch_folder` | `(path, extensions, action, recursive, ignore_patterns)` | `FileWatchConfig` |
| `process_files` | `(path, operation, target, extensions)` | `Dict` |
| `compress_directory` | `(source, output)` | `Dict` |
| `extract_archive` | `(archive, destination)` | `Dict` |
| `list_file_watches` | `()` | `List[FileWatchConfig]` |

### Notifications & Status

| Method | Signature | Returns |
|--------|-----------|---------|
| `send_notification` | `(channel, recipient, subject, body)` | `Notification` |
| `list_notifications` | `(limit)` | `List[Notification]` |
| `get_status` | `()` | `Dict` |

---

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
    created_at: datetime
    updated_at: datetime
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
    output: Optional[Any]
    error: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
```

### Schedule

```python
@dataclass
class Schedule:
    schedule_id: str
    name: str
    workflow_id: str
    cron_expression: Optional[str]
    interval_seconds: Optional[int]
    enabled: bool
    next_run: datetime
    last_run: Optional[datetime]
    params: Dict[str, Any]
```

### EmailTemplate

```python
@dataclass
class EmailTemplate:
    template_id: str
    name: str
    subject: str
    body: str
    html: Optional[str]
    variables: List[str]
    created_at: datetime
```

### ExecutionHistory

```python
@dataclass
class ExecutionHistory:
    execution_id: str
    workflow_id: str
    status: WorkflowStatus
    started_at: datetime
    completed_at: Optional[datetime]
    duration_seconds: Optional[float]
    tasks_completed: int
    tasks_failed: int
    tasks_total: int
```

---

## Checklists

### Workflow Design

- [ ] Tasks have clear names and purposes
- [ ] Dependencies correctly modeled (no cycles)
- [ ] Timeouts set for all tasks
- [ ] Retry strategy configured for flaky operations
- [ ] Compensation actions defined for critical tasks
- [ ] Notifications configured for failure alerts
- [ ] Variables documented with default values
- [ ] DAG depth is reasonable (< 20 levels)

### Schedule Management

- [ ] Cron expressions verified with crontab.guru
- [ ] Timezone awareness considered (UTC recommended)
- [ ] Overlap prevention for long-running workflows
- [ ] Dead schedule cleanup configured
- [ ] Schedule names are descriptive
- [ ] Next run times are reasonable

### Email Campaigns

- [ ] Template variables are documented
- [ ] Subject lines are clear and non-spammy
- [ ] Recipient lists are verified
- [ ] Unsubscribe mechanism in place
- [ ] Test email sent before campaign
- [ ] Bounce handling configured

### File Operations

- [ ] Source paths exist and are accessible
- [ ] Target directories have sufficient space
- [ ] File patterns are specific (avoid `*.*`)
- [ ] Ignore patterns exclude temporary files
- [ ] Backup created before destructive operations
- [ ] Disk space checked before large operations

---

## Troubleshooting

| Problem | Cause | Resolution |
|---------|-------|------------|
| Workflow deadlocked | Circular dependencies | Check `depends_on` for cycles in DAG |
| Task timeout | Task too slow or hung | Increase `timeout_seconds`; check task logic |
| Schedule not firing | Disabled or future `next_run` | Check `enabled` flag and `next_run` time |
| Email not sent | Template not found | Verify `template_id` exists in templates |
| File operation failed | Path doesn't exist | Verify path with `Path.exists()` before operation |
| Retry exhausted | Task fundamentally broken | Fix handler logic; don't just increase retry count |
| Compensation failed | Compensation action errors | Test compensation actions independently |
| Workflow variable undefined | Missing variable in config | Define all variables in `variables` dict |
| Notification channel invalid | Channel not configured | Check channel config (SMTP, webhook URL, etc.) |
| DAG too deep | Excessive nesting | Flatten workflow; split into sub-workflows |

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
    email_smtp_username="automation@example.com",
    email_smtp_password="{{env.SMTP_PASSWORD}}",
    slack_webhook_url="https://hooks.slack.com/services/xxx/yyy/zzz",
    webhook_timeout_seconds=30,
    file_watch_interval_seconds=10,
    max_parallel_tasks=4,
    enable_compensation=True,
    log_level="INFO",
)

agent = AutomationAgent(config=config)
```

---

## File Structure

```
agents/automation/
  agent.py           # Full implementation with workflow engine, scheduler, email, file ops
  ARCHITECTURE.md    # System architecture with ASCII diagrams
  GROK.md            # Agent prompt and method specifications
  README.md          # Usage guide and quick reference
```

---

## License

MIT License — see [LICENSE](../../LICENSE).

---

*Automation Agent v2.0 — Part of the Awesome Grok Skills collection.*
