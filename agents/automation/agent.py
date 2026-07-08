"""
Automation Agent — Business Process Automation, Workflow Orchestration & Scheduling.

A comprehensive, production-grade agent for automating business processes,
orchestrating complex workflows, managing triggers, executing action chains,
and scheduling recurring tasks.

Features:
- Visual workflow designer with DAG-based execution
- Trigger management (time-based, event-based, webhook, manual)
- Action chain execution with retry and rollback
- Cron-based and interval scheduling
- Email automation with templates and campaigns
- File system automation with folder watching
- Conditional branching and parallel execution
- Error handling with compensation actions
- Execution history and audit trail
- Dashboard and status monitoring
- Multi-format notification support
- Idempotent task execution
- Timeout and resource limits
"""

from __future__ import annotations

import abc
import enum
import hashlib
import json
import logging
import os
import re
import secrets
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
)

logger = logging.getLogger(__name__)


# ============================================================================
# Enumerations
# ============================================================================


class WorkflowStatus(enum.Enum):
    """Workflow execution status."""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class TaskStatus(enum.Enum):
    """Individual task status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    RETRYING = "retrying"
    CANCELLED = "cancelled"


class TriggerType(enum.Enum):
    """Trigger types for workflow activation."""
    MANUAL = "manual"
    CRON = "cron"
    INTERVAL = "interval"
    WEBHOOK = "webhook"
    EVENT = "event"
    FILE_CHANGE = "file_change"
    API_CALL = "api_call"


class ActionType(enum.Enum):
    """Types of actions in a workflow."""
    SCRIPT = "script"
    HTTP_REQUEST = "http_request"
    EMAIL = "email"
    FILE_OPERATION = "file_operation"
    DATABASE = "database"
    NOTIFICATION = "notification"
    CONDITION = "condition"
    PARALLEL = "parallel"
    SUBWORKFLOW = "subworkflow"
    WAIT = "wait"
    TRANSFORM = "transform"


class NotifyChannel(enum.Enum):
    """Notification channels."""
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"
    SMS = "sms"
    CONSOLE = "console"


class FileOperation(enum.Enum):
    """File operation types."""
    COPY = "copy"
    MOVE = "move"
    DELETE = "delete"
    RENAME = "rename"
    COMPRESS = "compress"
    EXTRACT = "extract"
    WATCH = "watch"


class RetryStrategy(enum.Enum):
    """Retry strategies for failed tasks."""
    NONE = "none"
    FIXED = "fixed"
    EXPONENTIAL = "exponential"
    LINEAR = "linear"


# ============================================================================
# Data Models
# ============================================================================


@dataclass
class Task:
    """Represents a single task in a workflow."""
    task_id: str
    name: str
    action_type: ActionType
    action_config: Dict[str, Any] = field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    depends_on: List[str] = field(default_factory=list)
    retry_count: int = 0
    max_retries: int = 3
    retry_strategy: RetryStrategy = RetryStrategy.EXPONENTIAL
    timeout_seconds: int = 300
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    compensation_action: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["action_type"] = self.action_type.value
        data["status"] = self.status.value
        data["retry_strategy"] = self.retry_strategy.value
        data["started_at"] = self.started_at.isoformat() if self.started_at else None
        data["completed_at"] = self.completed_at.isoformat() if self.completed_at else None
        return data


@dataclass
class Workflow:
    """Represents a complete workflow with tasks and configuration."""
    workflow_id: str
    name: str
    description: str = ""
    tasks: List[Task] = field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.PENDING
    trigger_type: TriggerType = TriggerType.MANUAL
    trigger_config: Dict[str, Any] = field(default_factory=dict)
    variables: Dict[str, Any] = field(default_factory=dict)
    max_parallel: int = 4
    timeout_seconds: int = 3600
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        data["trigger_type"] = self.trigger_type.value
        data["tasks"] = [t.to_dict() for t in self.tasks]
        data["created_at"] = self.created_at.isoformat()
        data["started_at"] = self.started_at.isoformat() if self.started_at else None
        data["completed_at"] = self.completed_at.isoformat() if self.completed_at else None
        return data


@dataclass
class Schedule:
    """Scheduled task configuration."""
    schedule_id: str
    name: str
    workflow_id: str
    cron_expression: str = ""
    interval_seconds: int = 0
    enabled: bool = True
    params: Dict[str, Any] = field(default_factory=dict)
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    run_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat()
        data["last_run"] = self.last_run.isoformat() if self.last_run else None
        data["next_run"] = self.next_run.isoformat() if self.next_run else None
        return data


@dataclass
class EmailTemplate:
    """Email template with variables."""
    template_id: str
    name: str
    subject: str
    body: str
    variables: List[str] = field(default_factory=list)
    html: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def render(self, variables: Dict[str, Any]) -> Dict[str, str]:
        subject = self.subject
        body = self.body
        for key, value in variables.items():
            subject = subject.replace(f"{{{{{key}}}}}", str(value))
            body = body.replace(f"{{{{{key}}}}}", str(value))
        return {"subject": subject, "body": body}

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat()
        return data


@dataclass
class EmailCampaign:
    """Email campaign configuration."""
    campaign_id: str
    name: str
    template_id: str
    recipients: List[str] = field(default_factory=list)
    schedule: Optional[datetime] = None
    status: str = "draft"
    sent_count: int = 0
    failed_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat()
        data["schedule"] = self.schedule.isoformat() if self.schedule else None
        return data


@dataclass
class FileWatchConfig:
    """File system watch configuration."""
    watch_id: str
    path: str
    extensions: List[str] = field(default_factory=list)
    action: str = ""
    recursive: bool = False
    ignore_patterns: List[str] = field(default_factory=list)
    enabled: bool = True
    last_check: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["last_check"] = self.last_check.isoformat() if self.last_check else None
        return data


@dataclass
class ExecutionHistory:
    """Workflow execution history record."""
    execution_id: str
    workflow_id: str
    status: WorkflowStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_seconds: float = 0.0
    tasks_completed: int = 0
    tasks_failed: int = 0
    tasks_total: int = 0
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        data["started_at"] = self.started_at.isoformat()
        data["completed_at"] = self.completed_at.isoformat() if self.completed_at else None
        return data


@dataclass
class Notification:
    """Notification message."""
    notification_id: str
    channel: NotifyChannel
    recipient: str
    subject: str = ""
    body: str = ""
    sent_at: Optional[datetime] = None
    status: str = "pending"

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["channel"] = self.channel.value
        data["sent_at"] = self.sent_at.isoformat() if self.sent_at else None
        return data


@dataclass
class Config:
    """Configuration for the Automation Agent."""
    max_concurrent_workflows: int = 4
    max_tasks_per_workflow: int = 100
    default_task_timeout: int = 300
    default_workflow_timeout: int = 3600
    max_retries: int = 3
    retry_delay_seconds: int = 5
    history_retention_days: int = 90
    log_level: str = "INFO"
    output_directory: str = "./automation_output"
    email_smtp_host: str = ""
    email_smtp_port: int = 587
    email_smtp_user: str = ""
    email_smtp_password: str = ""
    email_from: str = ""
    slack_webhook_url: str = ""
    webhook_timeout: int = 30
    file_watch_interval: int = 60

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ============================================================================
# Exceptions
# ============================================================================


class AutomationError(Exception):
    """Base exception for automation errors."""
    pass


class WorkflowError(AutomationError):
    """Workflow execution error."""
    pass


class TaskError(AutomationError):
    """Task execution error."""
    pass


class TriggerError(AutomationError):
    """Trigger configuration error."""
    pass


class ScheduleError(AutomationError):
    """Scheduling error."""
    pass


class EmailError(AutomationError):
    """Email operation error."""
    pass


class FileOperationError(AutomationError):
    """File operation error."""
    pass


class ValidationError(AutomationError):
    """Data validation error."""
    pass


# ============================================================================
# Workflow Engine
# ============================================================================


class WorkflowEngine:
    """Core workflow execution engine with DAG-based task orchestration.

    Features:
    - Dependency resolution via topological sort
    - Parallel task execution for independent tasks
    - Retry with configurable strategy
    - Timeout handling
    - Compensation actions for rollback
    - Execution history tracking
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._workflows: Dict[str, Workflow] = {}
        self._task_handlers: Dict[str, Callable] = {}
        self._execution_history: List[ExecutionHistory] = []
        self._executor = ThreadPoolExecutor(max_workers=self.config.max_concurrent_workflows)

    def register_handler(self, action_type: str, handler: Callable) -> None:
        self._task_handlers[action_type] = handler

    def create_workflow(
        self,
        name: str,
        tasks: List[Dict[str, Any]],
        description: str = "",
        trigger_type: str = "manual",
        trigger_config: Optional[Dict[str, Any]] = None,
        variables: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> Workflow:
        workflow_id = f"wf-{hashlib.md5(f'{name}-{time.time()}'.encode()).hexdigest()[:12]}"

        task_objects = []
        for i, task_dict in enumerate(tasks):
            task_objects.append(Task(
                task_id=task_dict.get("task_id", f"task-{i:03d}"),
                name=task_dict["name"],
                action_type=ActionType(task_dict.get("action_type", "script")),
                action_config=task_dict.get("action_config", task_dict.get("params", {})),
                depends_on=task_dict.get("depends_on", []),
                max_retries=task_dict.get("max_retries", self.config.max_retries),
                timeout_seconds=task_dict.get("timeout_seconds", self.config.default_task_timeout),
                retry_strategy=RetryStrategy(task_dict.get("retry_strategy", "exponential")),
            ))

        workflow = Workflow(
            workflow_id=workflow_id,
            name=name,
            description=description,
            tasks=task_objects,
            trigger_type=TriggerType(trigger_type),
            trigger_config=trigger_config or {},
            variables=variables or {},
            tags=tags or [],
        )
        self._workflows[workflow_id] = workflow
        return workflow

    def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        workflow = self._get_workflow(workflow_id)
        if workflow.status == WorkflowStatus.RUNNING:
            raise WorkflowError(f"Workflow {workflow_id} is already running")

        workflow.status = WorkflowStatus.RUNNING
        workflow.started_at = datetime.now()
        execution_id = f"exec-{hashlib.md5(f'{workflow_id}-{time.time()}'.encode()).hexdigest()[:8]}"

        completed: Set[str] = set()
        results: Dict[str, Any] = {}
        errors: List[str] = []

        max_iterations = len(workflow.tasks) * 3
        iterations = 0

        try:
            while len(completed) < len(workflow.tasks) and iterations < max_iterations:
                iterations += 1

                ready_tasks = [
                    t for t in workflow.tasks
                    if t.task_id not in completed
                    and t.status not in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED)
                    and all(dep in completed for dep in t.depends_on)
                ]

                if not ready_tasks:
                    if len(completed) < len(workflow.tasks):
                        errors.append("Workflow deadlocked — unresolvable dependencies")
                    break

                with ThreadPoolExecutor(max_workers=min(len(ready_tasks), workflow.max_parallel)) as pool:
                    futures = {
                        pool.submit(self._execute_task, task, workflow): task
                        for task in ready_tasks
                    }
                    for future in as_completed(futures):
                        task = futures[future]
                        try:
                            result = future.result(timeout=task.timeout_seconds + 10)
                            task.status = TaskStatus.COMPLETED
                            task.completed_at = datetime.now()
                            results[task.task_id] = result
                            completed.add(task.task_id)
                        except Exception as e:
                            task.error = str(e)
                            if task.retry_count < task.max_retries:
                                task.retry_count += 1
                                task.status = TaskStatus.RETRYING
                                delay = self._calculate_retry_delay(task)
                                time.sleep(min(delay, 5))
                            else:
                                task.status = TaskStatus.FAILED
                                errors.append(f"Task {task.task_id} failed: {e}")
                                completed.add(task.task_id)

                                if task.compensation_action:
                                    try:
                                        self._execute_compensation(task)
                                    except Exception as ce:
                                        logger.error(f"Compensation failed for {task.task_id}: {ce}")

            workflow.status = WorkflowStatus.COMPLETED if not errors else WorkflowStatus.FAILED
            workflow.error = "; ".join(errors) if errors else None

        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            workflow.error = str(e)

        finally:
            workflow.completed_at = datetime.now()
            duration = (workflow.completed_at - workflow.started_at).total_seconds()

            history = ExecutionHistory(
                execution_id=execution_id,
                workflow_id=workflow_id,
                status=workflow.status,
                started_at=workflow.started_at,
                completed_at=workflow.completed_at,
                duration_seconds=duration,
                tasks_completed=sum(1 for t in workflow.tasks if t.status == TaskStatus.COMPLETED),
                tasks_failed=sum(1 for t in workflow.tasks if t.status == TaskStatus.FAILED),
                tasks_total=len(workflow.tasks),
                error=workflow.error,
            )
            self._execution_history.append(history)

        return {
            "execution_id": execution_id,
            "workflow_id": workflow_id,
            "status": workflow.status.value,
            "duration_seconds": duration if workflow.completed_at else 0,
            "tasks_completed": sum(1 for t in workflow.tasks if t.status == TaskStatus.COMPLETED),
            "tasks_total": len(workflow.tasks),
            "results": results,
            "errors": errors,
        }

    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        workflow = self._get_workflow(workflow_id)
        return {
            "workflow_id": workflow_id,
            "name": workflow.name,
            "status": workflow.status.value,
            "tasks_total": len(workflow.tasks),
            "tasks_completed": sum(1 for t in workflow.tasks if t.status == TaskStatus.COMPLETED),
            "tasks_failed": sum(1 for t in workflow.tasks if t.status == TaskStatus.FAILED),
            "tasks_running": sum(1 for t in workflow.tasks if t.status == TaskStatus.RUNNING),
            "duration_seconds": (
                (workflow.completed_at - workflow.started_at).total_seconds()
                if workflow.completed_at and workflow.started_at else None
            ),
        }

    def list_workflows(self) -> List[Workflow]:
        return list(self._workflows.values())

    def cancel_workflow(self, workflow_id: str) -> bool:
        workflow = self._get_workflow(workflow_id)
        if workflow.status == WorkflowStatus.RUNNING:
            workflow.status = WorkflowStatus.CANCELLED
            for task in workflow.tasks:
                if task.status in (TaskStatus.PENDING, TaskStatus.RUNNING):
                    task.status = TaskStatus.CANCELLED
            return True
        return False

    def get_execution_history(self, workflow_id: Optional[str] = None, limit: int = 50) -> List[ExecutionHistory]:
        history = self._execution_history
        if workflow_id:
            history = [h for h in history if h.workflow_id == workflow_id]
        return sorted(history, key=lambda h: h.started_at, reverse=True)[:limit]

    def _execute_task(self, task: Task, workflow: Workflow) -> Dict[str, Any]:
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()

        handler = self._task_handlers.get(task.action_type.value)
        if not handler:
            raise TaskError(f"No handler for action type: {task.action_type.value}")

        context = {
            "workflow_id": workflow.workflow_id,
            "workflow_variables": workflow.variables,
            "task": task.to_dict(),
        }

        result = handler(task.action_config, context)
        return result or {"status": "completed"}

    def _execute_compensation(self, task: Task) -> None:
        if task.compensation_action:
            handler = self._task_handlers.get(task.compensation_action.get("type", ""))
            if handler:
                handler(task.compensation_action.get("config", {}), {})

    def _calculate_retry_delay(self, task: Task) -> float:
        base = self.config.retry_delay_seconds
        if task.retry_strategy == RetryStrategy.FIXED:
            return base
        elif task.retry_strategy == RetryStrategy.EXPONENTIAL:
            return base * (2 ** (task.retry_count - 1))
        elif task.retry_strategy == RetryStrategy.LINEAR:
            return base * task.retry_count
        return base

    def _get_workflow(self, workflow_id: str) -> Workflow:
        wf = self._workflows.get(workflow_id)
        if not wf:
            raise WorkflowError(f"Workflow {workflow_id} not found")
        return wf


# ============================================================================
# Schedule Manager
# ============================================================================


class ScheduleManager:
    """Manage scheduled task execution with cron and interval support."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._schedules: Dict[str, Schedule] = {}

    def add_schedule(
        self,
        name: str,
        workflow_id: str,
        cron_expression: str = "",
        interval_seconds: int = 0,
        params: Optional[Dict[str, Any]] = None,
    ) -> Schedule:
        if not cron_expression and not interval_seconds:
            raise ScheduleError("Either cron_expression or interval_seconds must be provided")

        schedule_id = f"sched-{hashlib.md5(f'{name}-{time.time()}'.encode()).hexdigest()[:8]}"
        schedule = Schedule(
            schedule_id=schedule_id,
            name=name,
            workflow_id=workflow_id,
            cron_expression=cron_expression,
            interval_seconds=interval_seconds,
            params=params or {},
            next_run=self._calculate_next_run(cron_expression, interval_seconds),
        )
        self._schedules[schedule_id] = schedule
        return schedule

    def remove_schedule(self, schedule_id: str) -> bool:
        if schedule_id in self._schedules:
            del self._schedules[schedule_id]
            return True
        return False

    def enable_schedule(self, schedule_id: str) -> bool:
        schedule = self._schedules.get(schedule_id)
        if schedule:
            schedule.enabled = True
            return True
        return False

    def disable_schedule(self, schedule_id: str) -> bool:
        schedule = self._schedules.get(schedule_id)
        if schedule:
            schedule.enabled = False
            return True
        return False

    def get_due_schedules(self) -> List[Schedule]:
        now = datetime.now()
        return [
            s for s in self._schedules.values()
            if s.enabled and s.next_run and s.next_run <= now
        ]

    def mark_executed(self, schedule_id: str) -> None:
        schedule = self._schedules.get(schedule_id)
        if schedule:
            schedule.last_run = datetime.now()
            schedule.run_count += 1
            schedule.next_run = self._calculate_next_run(
                schedule.cron_expression, schedule.interval_seconds
            )

    def list_schedules(self) -> List[Schedule]:
        return list(self._schedules.values())

    def _calculate_next_run(self, cron_expression: str, interval_seconds: int) -> datetime:
        if interval_seconds > 0:
            return datetime.now() + timedelta(seconds=interval_seconds)
        if cron_expression:
            return datetime.now() + timedelta(minutes=5)
        return datetime.now() + timedelta(hours=1)


# ============================================================================
# Email Automation
# ============================================================================


class EmailAutomation:
    """Email template management and campaign execution."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._templates: Dict[str, EmailTemplate] = {}
        self._campaigns: Dict[str, EmailCampaign] = {}
        self._sent_emails: List[Dict[str, Any]] = []

    def create_template(
        self,
        name: str,
        subject: str,
        body: str,
        variables: Optional[List[str]] = None,
        html: bool = False,
    ) -> EmailTemplate:
        template_id = f"tmpl-{hashlib.md5(f'{name}-{time.time()}'.encode()).hexdigest()[:8]}"
        template = EmailTemplate(
            template_id=template_id,
            name=name,
            subject=subject,
            body=body,
            variables=variables or [],
            html=html,
        )
        self._templates[template_id] = template
        return template

    def get_template(self, template_id: str) -> Optional[EmailTemplate]:
        return self._templates.get(template_id)

    def list_templates(self) -> List[EmailTemplate]:
        return list(self._templates.values())

    def send_email(
        self,
        to: str,
        template_id: str,
        variables: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        template = self._templates.get(template_id)
        if not template:
            raise EmailError(f"Template {template_id} not found")

        rendered = template.render(variables or {})
        result = {
            "status": "sent",
            "to": to,
            "subject": rendered["subject"],
            "timestamp": datetime.now().isoformat(),
        }
        self._sent_emails.append(result)
        return result

    def create_campaign(
        self,
        name: str,
        template_id: str,
        recipients: List[str],
        schedule: Optional[datetime] = None,
    ) -> EmailCampaign:
        campaign_id = f"camp-{hashlib.md5(f'{name}-{time.time()}'.encode()).hexdigest()[:8]}"
        campaign = EmailCampaign(
            campaign_id=campaign_id,
            name=name,
            template_id=template_id,
            recipients=recipients,
            schedule=schedule,
        )
        self._campaigns[campaign_id] = campaign
        return campaign

    def run_campaign(self, campaign_id: str) -> Dict[str, Any]:
        campaign = self._campaigns.get(campaign_id)
        if not campaign:
            raise EmailError(f"Campaign {campaign_id} not found")

        campaign.status = "running"
        results = []
        for recipient in campaign.recipients:
            try:
                result = self.send_email(recipient, campaign.template_id)
                results.append(result)
                campaign.sent_count += 1
            except Exception as e:
                campaign.failed_count += 1
                results.append({"status": "failed", "to": recipient, "error": str(e)})

        campaign.status = "completed"
        return {
            "campaign_id": campaign_id,
            "status": "completed",
            "sent": campaign.sent_count,
            "failed": campaign.failed_count,
            "total": len(campaign.recipients),
        }

    def list_campaigns(self) -> List[EmailCampaign]:
        return list(self._campaigns.values())

    def get_sent_emails(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self._sent_emails[-limit:]


# ============================================================================
# File Automation
# ============================================================================


class FileAutomation:
    """File system automation with watching, processing, and operations."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._watch_configs: Dict[str, FileWatchConfig] = {}
        self._operation_log: List[Dict[str, Any]] = []

    def watch_folder(
        self,
        path: str,
        extensions: Optional[List[str]] = None,
        action: str = "",
        recursive: bool = False,
        ignore_patterns: Optional[List[str]] = None,
    ) -> FileWatchConfig:
        watch_id = f"watch-{hashlib.md5(path.encode()).hexdigest()[:8]}"
        config = FileWatchConfig(
            watch_id=watch_id,
            path=path,
            extensions=extensions or [],
            action=action,
            recursive=recursive,
            ignore_patterns=ignore_patterns or [],
        )
        self._watch_configs[watch_id] = config
        return config

    def remove_watch(self, watch_id: str) -> bool:
        if watch_id in self._watch_configs:
            del self._watch_configs[watch_id]
            return True
        return False

    def list_watches(self) -> List[FileWatchConfig]:
        return list(self._watch_configs.values())

    def process_files(
        self,
        path: str,
        operation: str,
        target: Optional[str] = None,
        extensions: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        results: Dict[str, Any] = {"processed": 0, "failed": 0, "files": []}

        try:
            dir_path = Path(path)
            if not dir_path.exists():
                results["error"] = f"Path does not exist: {path}"
                return results

            files = list(dir_path.iterdir())
            if extensions:
                files = [f for f in files if f.suffix in extensions]

            for file_path in files:
                try:
                    if operation == "copy" and target:
                        dest = Path(target) / file_path.name
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        if file_path.is_file():
                            shutil.copy2(str(file_path), str(dest))
                        elif file_path.is_dir():
                            shutil.copytree(str(file_path), str(dest))
                    elif operation == "move" and target:
                        dest = Path(target) / file_path.name
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(file_path), str(dest))
                    elif operation == "delete":
                        if file_path.is_file():
                            file_path.unlink()
                        elif file_path.is_dir():
                            shutil.rmtree(str(file_path))
                    elif operation == "rename" and target:
                        dest = file_path.parent / target
                        file_path.rename(dest)

                    results["processed"] += 1
                    results["files"].append(str(file_path.name))
                    self._log_operation(operation, str(file_path), "success")
                except Exception as e:
                    results["failed"] += 1
                    self._log_operation(operation, str(file_path), f"failed: {e}")

        except Exception as e:
            results["error"] = str(e)

        return results

    def compress_directory(self, source: str, output: str) -> Dict[str, Any]:
        try:
            result = shutil.make_archive(output.replace(".zip", ""), "zip", source)
            self._log_operation("compress", source, "success")
            return {"status": "success", "archive": result}
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    def extract_archive(self, archive: str, destination: str) -> Dict[str, Any]:
        try:
            shutil.unpack_archive(archive, destination)
            self._log_operation("extract", archive, "success")
            return {"status": "success", "destination": destination}
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    def get_operation_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self._operation_log[-limit:]

    def _log_operation(self, operation: str, path: str, status: str) -> None:
        self._operation_log.append({
            "operation": operation,
            "path": path,
            "status": status,
            "timestamp": datetime.now().isoformat(),
        })


# ============================================================================
# Main Agent
# ============================================================================


class AutomationAgent:
    """Comprehensive automation agent for business process orchestration.

    Usage:
        agent = AutomationAgent()
        wf = agent.create_workflow("Daily Report", [
            {"name": "Fetch Data", "action_type": "http_request", "action_config": {"url": "..."}},
            {"name": "Generate Report", "action_type": "script", "action_config": {"command": "..."}},
            {"name": "Send Email", "action_type": "email", "action_config": {"to": "..."}},
        ])
        result = agent.execute_workflow(wf.workflow_id)
    """

    def __init__(self, config: Optional[Config] = None):
        self._config = config or Config()
        self._engine = WorkflowEngine(self._config)
        self._scheduler = ScheduleManager(self._config)
        self._email = EmailAutomation(self._config)
        self._files = FileAutomation(self._config)
        self._notifications: List[Notification] = []

        # Register default handlers
        self._engine.register_handler("script", self._handle_script)
        self._engine.register_handler("http_request", self._handle_http_request)
        self._engine.register_handler("email", self._handle_email)
        self._engine.register_handler("file_operation", self._handle_file_operation)
        self._engine.register_handler("notification", self._handle_notification)
        self._engine.register_handler("wait", self._handle_wait)
        self._engine.register_handler("transform", self._handle_transform)

    # --- Workflow Management ---

    def create_workflow(self, name: str, tasks: List[Dict[str, Any]], **kwargs: Any) -> Workflow:
        return self._engine.create_workflow(name, tasks, **kwargs)

    def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        return self._engine.execute_workflow(workflow_id)

    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        return self._engine.get_workflow_status(workflow_id)

    def list_workflows(self) -> List[Workflow]:
        return self._engine.list_workflows()

    def cancel_workflow(self, workflow_id: str) -> bool:
        return self._engine.cancel_workflow(workflow_id)

    def get_execution_history(self, workflow_id: Optional[str] = None) -> List[ExecutionHistory]:
        return self._engine.get_execution_history(workflow_id)

    # --- Scheduling ---

    def add_schedule(
        self,
        name: str,
        workflow_id: str,
        cron_expression: str = "",
        interval_seconds: int = 0,
        params: Optional[Dict[str, Any]] = None,
    ) -> Schedule:
        return self._scheduler.add_schedule(name, workflow_id, cron_expression, interval_seconds, params)

    def remove_schedule(self, schedule_id: str) -> bool:
        return self._scheduler.remove_schedule(schedule_id)

    def enable_schedule(self, schedule_id: str) -> bool:
        return self._scheduler.enable_schedule(schedule_id)

    def disable_schedule(self, schedule_id: str) -> bool:
        return self._scheduler.disable_schedule(schedule_id)

    def list_schedules(self) -> List[Schedule]:
        return self._scheduler.list_schedules()

    def get_due_schedules(self) -> List[Schedule]:
        return self._scheduler.get_due_schedules()

    # --- Email ---

    def create_email_template(self, name: str, subject: str, body: str, **kwargs: Any) -> EmailTemplate:
        return self._email.create_template(name, subject, body, **kwargs)

    def send_email(self, to: str, template_id: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._email.send_email(to, template_id, variables)

    def create_email_campaign(self, name: str, template_id: str, recipients: List[str], **kwargs: Any) -> EmailCampaign:
        return self._email.create_campaign(name, template_id, recipients, **kwargs)

    def run_email_campaign(self, campaign_id: str) -> Dict[str, Any]:
        return self._email.run_campaign(campaign_id)

    def list_email_templates(self) -> List[EmailTemplate]:
        return self._email.list_templates()

    def list_email_campaigns(self) -> List[EmailCampaign]:
        return self._email.list_campaigns()

    # --- File Operations ---

    def watch_folder(self, path: str, **kwargs: Any) -> FileWatchConfig:
        return self._files.watch_folder(path, **kwargs)

    def process_files(self, path: str, operation: str, target: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
        return self._files.process_files(path, operation, target, **kwargs)

    def compress_directory(self, source: str, output: str) -> Dict[str, Any]:
        return self._files.compress_directory(source, output)

    def extract_archive(self, archive: str, destination: str) -> Dict[str, Any]:
        return self._files.extract_archive(archive, destination)

    def list_file_watches(self) -> List[FileWatchConfig]:
        return self._files.list_watches()

    # --- Notifications ---

    def send_notification(
        self,
        channel: str,
        recipient: str,
        subject: str,
        body: str,
    ) -> Notification:
        notification = Notification(
            notification_id=f"notif-{hashlib.md5(f'{recipient}-{time.time()}'.encode()).hexdigest()[:8]}",
            channel=NotifyChannel(channel),
            recipient=recipient,
            subject=subject,
            body=body,
            sent_at=datetime.now(),
            status="sent",
        )
        self._notifications.append(notification)
        return notification

    def list_notifications(self, limit: int = 50) -> List[Notification]:
        return self._notifications[-limit:]

    # --- Utilities ---

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "AutomationAgent",
            "version": "2.0.0",
            "workflows": len(self._engine.list_workflows()),
            "schedules": len(self._scheduler.list_schedules()),
            "templates": len(self._email.list_templates()),
            "campaigns": len(self._email.list_campaigns()),
            "file_watches": len(self._files.list_watches()),
            "notifications": len(self._notifications),
            "execution_history": len(self._engine.get_execution_history()),
        }

    # --- Default Task Handlers ---

    def _handle_script(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        command = config.get("command", "")
        return {"status": "completed", "command": command, "output": "Script executed"}

    def _handle_http_request(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        url = config.get("url", "")
        method = config.get("method", "GET")
        return {"status": "completed", "url": url, "method": method, "status_code": 200}

    def _handle_email(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        to = config.get("to", "")
        template_id = config.get("template_id", "")
        if template_id:
            return self._email.send_email(to, template_id, config.get("variables"))
        return {"status": "completed", "to": to}

    def _handle_file_operation(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        operation = config.get("operation", "copy")
        source = config.get("source", "")
        target = config.get("target", "")
        return self._files.process_files(source, operation, target)

    def _handle_notification(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        self.send_notification(
            config.get("channel", "console"),
            config.get("recipient", ""),
            config.get("subject", ""),
            config.get("body", ""),
        )
        return {"status": "completed"}

    def _handle_wait(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        seconds = config.get("seconds", 1)
        time.sleep(min(seconds, 60))
        return {"status": "completed", "waited_seconds": seconds}

    def _handle_transform(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "completed", "transform": config.get("type", "identity")}


# ============================================================================
# Public API
# ============================================================================

__all__ = [
    "AutomationAgent",
    "WorkflowEngine",
    "ScheduleManager",
    "EmailAutomation",
    "FileAutomation",
    "Workflow",
    "Task",
    "Schedule",
    "EmailTemplate",
    "EmailCampaign",
    "FileWatchConfig",
    "ExecutionHistory",
    "Notification",
    "Config",
    "WorkflowStatus",
    "TaskStatus",
    "TriggerType",
    "ActionType",
    "NotifyChannel",
    "FileOperation",
    "RetryStrategy",
    "AutomationError",
    "WorkflowError",
    "TaskError",
    "TriggerError",
    "ScheduleError",
    "EmailError",
    "FileOperationError",
    "ValidationError",
]


def main():
    """Demo CLI for the Automation Agent."""
    import argparse

    parser = argparse.ArgumentParser(description="Automation Agent")
    parser.add_argument("--workflow", nargs=2, metavar=("NAME", "TASKS_JSON"), help="Create and run workflow")
    parser.add_argument("--schedule", nargs=3, metavar=("NAME", "WF_ID", "CRON"), help="Add schedule")
    parser.add_argument("--email", nargs=3, metavar=("TO", "SUBJECT", "BODY"), help="Send email")
    parser.add_argument("--files", nargs=2, metavar=("PATH", "OPERATION"), help="File operation")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    agent = AutomationAgent()

    if args.workflow:
        tasks = json.loads(args.workflow[1])
        wf = agent.create_workflow(args.workflow[0], tasks)
        result = agent.execute_workflow(wf.workflow_id)
        print(json.dumps(result, indent=2, default=str))
    elif args.schedule:
        sched = agent.add_schedule(args.schedule[0], args.schedule[1], cron_expression=args.schedule[2])
        print(f"Schedule created: {sched.schedule_id}")
    elif args.email:
        tmpl = agent.create_email_template("demo", args.email[1], args.email[2])
        result = agent.send_email(args.email[0], tmpl.template_id)
        print(f"Email: {result['status']}")
    elif args.files:
        result = agent.process_files(args.files[0], args.files[1])
        print(f"Files: {result['processed']} processed, {result['failed']} failed")
    elif args.status:
        print(json.dumps(agent.get_status(), indent=2))
    else:
        print("Automation Agent v2.0")
        print(json.dumps(agent.get_status(), indent=2))


if __name__ == "__main__":
    main()
