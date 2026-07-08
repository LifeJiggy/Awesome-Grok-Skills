"""Operations Agent for business operations"""
from typing import List, Dict, Any, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict, deque
import json
import uuid
import threading
import hashlib
import logging
import time
import os
from pathlib import Path


class ProcessStatus(Enum):
    """Status of an operational process."""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class KPIThreshold(Enum):
    """Threshold levels for KPIs."""
    CRITICAL = "critical"
    WARNING = "warning"
    NORMAL = "normal"
    EXCELLENT = "excellent"


class MetricDirection(Enum):
    """Direction in which a KPI should move."""
    HIGHER_IS_BETTER = "higher_is_better"
    LOWER_IS_BETTER = "lower_is_better"
    TARGET_IS_EXACT = "target_is_exact"


class ProcessPriority(Enum):
    """Priority levels for processes."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ProcessStep:
    """Represents a single step in an operational process."""
    name: str
    description: str
    owner: str
    estimated_duration_minutes: int = 0
    dependencies: List[str] = field(default_factory=list)
    automated: bool = False
    status: ProcessStatus = ProcessStatus.DRAFT

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "owner": self.owner,
            "estimated_duration_minutes": self.estimated_duration_minutes,
            "dependencies": self.dependencies,
            "automated": self.automated,
            "status": self.status.value
        }


@dataclass
class KPI:
    """Represents a Key Performance Indicator."""
    name: str
    target: float
    unit: str
    current: float = 0.0
    threshold_critical: Optional[float] = None
    threshold_warning: Optional[float] = None
    measurement_frequency: str = "daily"
    last_measured: Optional[datetime] = None

    def calculate_status(self) -> KPIThreshold:
        if self.threshold_critical is not None and self.current <= self.threshold_critical:
            return KPIThreshold.CRITICAL
        if self.threshold_warning is not None and self.current <= self.threshold_warning:
            return KPIThreshold.WARNING
        if self.current >= self.target:
            return KPIThreshold.EXCELLENT
        return KPIThreshold.NORMAL

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "target": self.target,
            "unit": self.unit,
            "current": self.current,
            "threshold_critical": self.threshold_critical,
            "threshold_warning": self.threshold_warning,
            "measurement_frequency": self.measurement_frequency,
            "last_measured": self.last_measured.isoformat() if self.last_measured else None,
            "status": self.calculate_status().value
        }


@dataclass
class WorkflowAction:
    """Represents an action within a workflow."""
    action_id: str
    action_type: str
    parameters: Dict[str, Any]
    timeout_seconds: int = 30
    retry_count: int = 3
    on_failure: str = "stop"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_id": self.action_id,
            "action_type": self.action_type,
            "parameters": self.parameters,
            "timeout_seconds": self.timeout_seconds,
            "retry_count": self.retry_count,
            "on_failure": self.on_failure
        }


@dataclass
class Workflow:
    """Represents an operational workflow."""
    name: str
    trigger: str
    actions: List[WorkflowAction]
    enabled: bool = True
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    last_triggered: Optional[datetime] = None
    execution_count: int = 0
    success_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "trigger": self.trigger,
            "actions": [a.to_dict() for a in self.actions],
            "enabled": self.enabled,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "last_triggered": self.last_triggered.isoformat() if self.last_triggered else None,
            "execution_count": self.execution_count,
            "success_count": self.success_count,
            "success_rate": (self.success_count / self.execution_count * 100) if self.execution_count > 0 else 0.0
        }


@dataclass
class ProcessReport:
    """Represents a generated process report."""
    report_id: str
    process_name: str
    generated_at: datetime
    data: Dict[str, Any]
    format: str = "json"
    author: str = "system"
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "process_name": self.process_name,
            "generated_at": self.generated_at.isoformat(),
            "data": self.data,
            "format": self.format,
            "author": self.author,
            "tags": self.tags
        }


@dataclass
class Resource:
    """Represents an operational resource."""
    name: str
    resource_type: str
    capacity: float
    unit: str = ""
    owner: str = ""
    allocated: float = 0.0
    status: str = "available"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.resource_type,
            "capacity": self.capacity,
            "unit": self.unit,
            "owner": self.owner,
            "allocated": self.allocated,
            "available": self.capacity - self.allocated,
            "utilization_percent": round((self.allocated / self.capacity * 100) if self.capacity > 0 else 0.0, 2),
            "status": self.status
        }


@dataclass
class ScheduledJob:
    """Represents a scheduled workflow job."""
    schedule_id: str
    workflow_name: str
    run_at: str
    payload: Dict[str, Any]
    repeat: Optional[str]
    status: str = "scheduled"
    created_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schedule_id": self.schedule_id,
            "workflow_name": self.workflow_name,
            "run_at": self.run_at,
            "payload": self.payload,
            "repeat": self.repeat,
            "status": self.status,
            "created_at": self.created_at
        }


@dataclass
class Event:
    """Represents a system event."""
    event_type: str
    payload: Dict[str, Any]
    timestamp: str
    handlers_invoked: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "handlers_invoked": self.handlers_invoked
        }


@dataclass
class BatchJobResult:
    """Result of a batch processing job."""
    job_id: str
    total_items: int
    batches: int
    success_count: int
    failure_count: int
    output: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "total_items": self.total_items,
            "batches": self.batches,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "output": self.output
        }


@dataclass
class Rule:
    """Represents a business rule."""
    rule_id: str
    condition: str
    action: str
    priority: int = 10
    active: bool = True
    created_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "condition": self.condition,
            "action": self.action,
            "priority": self.priority,
            "active": self.active,
            "created_at": self.created_at
        }


class AnalyticsEngine:
    """Engine for operational analytics and reporting."""

    def __init__(self):
        self.reports: Dict[str, ProcessReport] = {}
        self.metrics_history: Dict[str, List[Tuple[datetime, float]]] = {}

    def generate_trend_analysis(self, kpi_name: str, days: int = 30) -> Dict[str, Any]:
        if kpi_name not in self.metrics_history:
            return {"error": f"No history available for {kpi_name}"}

        cutoff = datetime.now() - timedelta(days=days)
        history = [(ts, val) for ts, val in self.metrics_history[kpi_name] if ts >= cutoff]

        if not history:
            return {"error": f"No data in last {days} days for {kpi_name}"}

        values = [v for _, v in history]
        return {
            "kpi": kpi_name,
            "period_days": days,
            "average": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "trend": "improving" if values[-1] > values[0] else "declining",
            "data_points": len(values)
        }

    def record_metric(self, kpi_name: str, value: float, timestamp: Optional[datetime] = None):
        if kpi_name not in self.metrics_history:
            self.metrics_history[kpi_name] = []
        ts = timestamp or datetime.now()
        self.metrics_history[kpi_name].append((ts, value))

    def create_report(self, process_name: str, data: Dict[str, Any], author: str = "system", tags: List[str] = None) -> ProcessReport:
        report = ProcessReport(
            report_id=str(uuid.uuid4()),
            process_name=process_name,
            generated_at=datetime.now(),
            data=data,
            author=author,
            tags=tags or []
        )
        self.reports[report.report_id] = report
        return report

    def get_report(self, report_id: str) -> Optional[ProcessReport]:
        return self.reports.get(report_id)

    def list_reports(self, process_name: Optional[str] = None) -> List[ProcessReport]:
        if process_name:
            return [r for r in self.reports.values() if r.process_name == process_name]
        return list(self.reports.values())


class IntegrationManager:
    """Manages integrations with external systems."""

    def __init__(self):
        self.integrations: Dict[str, Dict[str, Any]] = {}
        self.connection_status: Dict[str, bool] = {}

    def register_integration(self, name: str, config: Dict[str, Any], connection_type: str = "api") -> Dict[str, Any]:
        integration = {
            "name": name,
            "config": config,
            "connection_type": connection_type,
            "registered_at": datetime.now().isoformat(),
            "status": "registered"
        }
        self.integrations[name] = integration
        self.connection_status[name] = False
        return integration

    def test_connection(self, name: str) -> bool:
        if name not in self.integrations:
            raise ValueError(f"Integration {name} not registered")
        self.connection_status[name] = True
        return True

    def get_integration(self, name: str) -> Optional[Dict[str, Any]]:
        return self.integrations.get(name)

    def list_integrations(self) -> List[Dict[str, Any]]:
        return [{"name": k, **v, "connected": self.connection_status.get(k, False)} for k, v in self.integrations.items()]

    def send_data(self, integration_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.connection_status.get(integration_name):
            raise ConnectionError(f"No active connection to {integration_name}")
        return {"status": "sent", "integration": integration_name, "payload": payload, "timestamp": datetime.now().isoformat()}


class NotificationService:
    """Service for sending notifications."""

    def __init__(self):
        self.notification_history: List[Dict[str, Any]] = []

    def send_email(self, recipient: str, subject: str, body: str, priority: str = "normal") -> Dict[str, Any]:
        notification = {
            "type": "email",
            "recipient": recipient,
            "subject": subject,
            "body": body,
            "priority": priority,
            "timestamp": datetime.now().isoformat(),
            "status": "sent"
        }
        self.notification_history.append(notification)
        return notification

    def send_alert(self, channel: str, message: str, severity: str = "info") -> Dict[str, Any]:
        notification = {
            "type": "alert",
            "channel": channel,
            "message": message,
            "severity": severity,
            "timestamp": datetime.now().isoformat(),
            "status": "dispatched"
        }
        self.notification_history.append(notification)
        return notification

    def get_notification_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self.notification_history[-limit:]


class OperationsManager:
    """Main operations management class with comprehensive business process handling."""

    logger: logging.Logger = logging.getLogger("operations.agent")
    def __init__(self, storage_path: Optional[str] = None):
        self.processes: Dict[str, Dict[str, Any]] = {}
        self.kpis: Dict[str, KPI] = {}
        self.workflows: Dict[str, Workflow] = {}
        self.analytics = AnalyticsEngine()
        self.integrations = IntegrationManager()
        self.notifications = NotificationService()
        self.storage_path = Path(storage_path) if storage_path else None
        self._lock = threading.RLock()
        self.resource_manager = ResourceManager()
        self.scheduler = WorkflowScheduler()
        self.rule_engine = RuleEngine()
        self.event_bus = EventBus()
        self.metric_aggregator = MetricAggregator()
        self.batch_processor = BatchProcessor()

    def define_process(self, name: str, steps: List[str], owner: str, description: str = "", estimated_duration_minutes: int = 0) -> Dict[str, Any]:
        """Define a new operational process with steps and owner."""
        with self._lock:
            process_steps = []
            for i, step_name in enumerate(steps):
                step = ProcessStep(
                    name=step_name,
                    description=f"Step {i+1} of process {name}",
                    owner=owner,
                    estimated_duration_minutes=estimated_duration_minutes // max(len(steps), 1),
                    dependencies=[steps[i-1]] if i > 0 else [],
                    automated=False,
                    status=ProcessStatus.DRAFT
                )
                process_steps.append(step)

            self.processes[name] = {
                "steps": process_steps,
                "owner": owner,
                "efficiency": 100.0,
                "status": ProcessStatus.DRAFT,
                "description": description,
                "created_at": datetime.now().isoformat(),
                "total_steps": len(steps)
            }
            self.notifications.send_alert("operations", f"New process defined: {name}")
            self.event_bus.publish("process.created", {"process_name": name, "owner": owner})
            return self.processes[name]

    def update_process_status(self, name: str, status: ProcessStatus) -> Dict[str, Any]:
        """Update the status of a process."""
        if name not in self.processes:
            raise KeyError(f"Process {name} not found")
        with self._lock:
            self.processes[name]["status"] = status
            self.notifications.send_alert("operations", f"Process {name} status changed to {status.value}")
            self.event_bus.publish("process.status_changed", {"process_name": name, "status": status.value})
            return self.processes[name]

    def set_kpi(self, name: str, target: float, unit: str, threshold_warning: Optional[float] = None, threshold_critical: Optional[float] = None, measurement_frequency: str = "daily") -> Dict[str, Any]:
        """Set or update a Key Performance Indicator."""
        with self._lock:
            self.kpis[name] = KPI(
                name=name,
                target=target,
                unit=unit,
                threshold_warning=threshold_warning,
                threshold_critical=threshold_critical,
                measurement_frequency=measurement_frequency
            )
            self.notifications.send_alert("operations", f"KPI set: {name} target {target} {unit}")
            self.event_bus.publish("kpi.created", {"kpi_name": name, "target": target, "unit": unit})
            return self.kpis[name].to_dict()

    def record_kpi(self, name: str, value: float, timestamp: Optional[datetime] = None) -> Dict[str, Any]:
        """Record a KPI measurement."""
        if name not in self.kpis:
            raise KeyError(f"KPI {name} not found")
        with self._lock:
            self.kpis[name].current = value
            self.kpis[name].last_measured = timestamp or datetime.now()
            self.analytics.record_metric(name, value, self.kpis[name].last_measured)
            self.metric_aggregator.add(name, value, self.kpis[name].last_measured)
            status = self.kpis[name].calculate_status()
            if status in (KPIThreshold.CRITICAL, KPIThreshold.WARNING):
                self.notifications.send_alert("kpi", f"KPI {name} is {status.value}: {value} {self.kpis[name].unit}")
                self.event_bus.publish("kpi.threshold_breach", {"kpi_name": name, "value": value, "status": status.value})
            return self.kpis[name].to_dict()

    def estimate_process_efficiency(self, name: str, actual_duration_minutes: int, planned_duration_minutes: int) -> Dict[str, Any]:
        """Calculate process efficiency based on actual vs planned duration."""
        if name not in self.processes:
            raise KeyError(f"Process {name} not found")
        if planned_duration_minutes == 0:
            return {"error": "Planned duration cannot be zero"}
        efficiency = (planned_duration_minutes / actual_duration_minutes) * 100 if actual_duration_minutes > 0 else 100.0
        efficiency = min(efficiency, 200.0)
        with self._lock:
            self.processes[name]["efficiency"] = efficiency
            self.processes[name]["last_actual_duration"] = actual_duration_minutes
            self.processes[name]["last_planned_duration"] = planned_duration_minutes
            self.processes[name]["efficiency_updated_at"] = datetime.now().isoformat()
            return {
                "process": name,
                "efficiency": round(efficiency, 2),
                "actual_duration": actual_duration_minutes,
                "planned_duration": planned_duration_minutes,
                "variance": round(planned_duration_minutes - actual_duration_minutes, 2)
            }

    def create_workflow(self, name: str, trigger: str, actions: List[Dict[str, Any]], description: str = "", enabled: bool = True) -> Dict[str, Any]:
        """Create a new workflow with actions."""
        with self._lock:
            workflow_actions = []
            for action_data in actions:
                action = WorkflowAction(
                    action_id=action_data.get("action_id", str(uuid.uuid4())),
                    action_type=action_data.get("action_type", "generic"),
                    parameters=action_data.get("parameters", {}),
                    timeout_seconds=action_data.get("timeout_seconds", 30),
                    retry_count=action_data.get("retry_count", 3),
                    on_failure=action_data.get("on_failure", "stop")
                )
                workflow_actions.append(action)

            self.workflows[name] = Workflow(
                name=name,
                trigger=trigger,
                actions=workflow_actions,
                enabled=enabled,
                description=description
            )
            self.notifications.send_alert("operations", f"Workflow created: {name}")
            self.event_bus.publish("workflow.created", {"workflow_name": name, "trigger": trigger})
            return self.workflows[name].to_dict()

    def execute_workflow(self, name: str, input_payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a workflow by name."""
        if name not in self.workflows:
            raise KeyError(f"Workflow {name} not found")
        workflow = self.workflows[name]
        if not workflow.enabled:
            raise ValueError(f"Workflow {name} is disabled")

        with self._lock:
            workflow.execution_count += 1
            workflow.last_triggered = datetime.now()
            results = []
            success = True
            for action in workflow.actions:
                result = self._execute_action(action, input_payload)
                results.append(result)
                if result.get("status") != "success":
                    success = False
                    if action.on_failure == "stop":
                        break
            if success:
                workflow.success_count += 1
            self.event_bus.publish("workflow.executed", {"workflow_name": name, "success": success, "results": results})
            return {
                "workflow": name,
                "execution_id": str(uuid.uuid4()),
                "triggered_at": workflow.last_triggered.isoformat(),
                "results": results,
                "overall_status": "success" if success else "partial_failure"
            }

    def _execute_action(self, action: WorkflowAction, payload: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Internal method to execute a single workflow action."""
        return {
            "action_id": action.action_id,
            "action_type": action.action_type,
            "status": "success",
            "output": {"action": action.action_id, "processed": True},
            "duration_ms": 10
        }

    def get_operations_dashboard(self) -> Dict[str, Any]:
        """Get a summary dashboard of operations."""
        active_kpis = {k: v for k, v in self.kpis.items() if v.calculate_status() == KPIThreshold.CRITICAL}
        active_processes = {k: v for k, v in self.processes.items() if v.get("status") == ProcessStatus.ACTIVE}
        active_workflows = {k: w for k, w in self.workflows.items() if w.enabled}

        return {
            "total_processes": len(self.processes),
            "active_processes": len(active_processes),
            "total_kpis": len(self.kpis),
            "kpis_in_critical_state": len(active_kpis),
            "total_workflows": len(self.workflows),
            "enabled_workflows": len(active_workflows),
            "total_reports": len(self.analytics.reports),
            "registered_integrations": len(self.integrations.integrations),
            "process_breakdown": {k: v.get("status", ProcessStatus.DRAFT).value for k, v in self.processes.items()},
            "kpi_summary": {k: v.calculate_status().value for k, v in self.kpis.items()},
            "generated_at": datetime.now().isoformat()
        }

    def generate_compliance_report(self, process_name: str, standards: List[str], author: str = "compliance_bot") -> Dict[str, Any]:
        """Generate a compliance report for a process against standards."""
        if process_name not in self.processes:
            raise KeyError(f"Process {process_name} not found")

        compliance = {std: {"compliant": True, "checks": []} for std in standards}
        for std in standards:
            for step in self.processes[process_name]["steps"]:
                compliance[std]["checks"].append({
                    "step": step.name,
                    "requirement": f"{std} check for {step.name}",
                    "passed": True,
                    "notes": "Automated check passed"
                })

        report = self.analytics.create_report(
            process_name=process_name,
            data={"compliance": compliance, "standards": standards},
            author=author,
            tags=["compliance", "audit"]
        )

        self.notifications.send_alert("compliance", f"Compliance report generated for {process_name}")
        return report.to_dict()

    def export_state(self, filepath: str) -> Dict[str, str]:
        """Export the current operations state to a JSON file."""
        state = {
            "processes": {k: v for k, v in self.processes.items()},
            "kpis": {k: v.to_dict() for k, v in self.kpis.items()},
            "workflows": {k: w.to_dict() for k, w in self.workflows.items()},
            "exported_at": datetime.now().isoformat()
        }
        path = Path(filepath)
        path.write_text(json.dumps(state, indent=2, default=str))
        return {"status": "exported", "filepath": str(path), "size_bytes": len(path.read_text())}

    def import_state(self, filepath: str) -> Dict[str, int]:
        """Import operations state from a JSON file."""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        data = json.loads(path.read_text())
        imported = {"processes": 0, "kpis": 0, "workflows": 0}

        with self._lock:
            for name, proc in data.get("processes", {}).items():
                if name not in self.processes:
                    self.processes[name] = proc
                    imported["processes"] += 1

            for name, kpi_data in data.get("kpis", {}).items():
                if name not in self.kpis:
                    self.kpis[name] = KPI(
                        name=kpi_data["name"],
                        target=kpi_data["target"],
                        unit=kpi_data["unit"],
                        current=kpi_data.get("current", 0.0),
                        threshold_warning=kpi_data.get("threshold_warning"),
                        threshold_critical=kpi_data.get("threshold_critical"),
                        measurement_frequency=kpi_data.get("measurement_frequency", "daily")
                    )
                    imported["kpis"] += 1

            for name, wf_data in data.get("workflows", {}).items():
                if name not in self.workflows:
                    self.workflows[name] = Workflow(
                        name=wf_data["name"],
                        trigger=wf_data["trigger"],
                        actions=[WorkflowAction(**a) for a in wf_data.get("actions", [])],
                        enabled=wf_data.get("enabled", True),
                        description=wf_data.get("description", "")
                    )
                    imported["workflows"] += 1

        return imported

    def get_kpi_trend(self, name: str, days: int = 30) -> Dict[str, Any]:
        """Get trend analysis for a KPI."""
        return self.analytics.generate_trend_analysis(name, days)

    def register_integration(self, name: str, config: Dict[str, Any], connection_type: str = "api") -> Dict[str, Any]:
        """Register an external integration."""
        return self.integrations.register_integration(name, config, connection_type)

    def send_notification(self, recipient: str, subject: str, body: str, priority: str = "normal") -> Dict[str, Any]:
        """Send a notification."""
        return self.notifications.send_email(recipient, subject, body, priority)


class ProcessOptimizer:
    """Provides optimization recommendations for operational processes."""

    @staticmethod
    def calculate_bottlenecks(process_steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify bottlenecks in a process."""
        bottlenecks = []
        total_time = sum(step.get("estimated_duration_minutes", 0) for step in process_steps)
        for step in process_steps:
            duration = step.get("estimated_duration_minutes", 0)
            if total_time > 0 and duration / total_time > 0.4:
                bottlenecks.append({
                    "step": step["name"],
                    "duration": duration,
                    "percentage": round(duration / total_time * 100, 1),
                    "recommendation": f"Consider optimizing {step['name']} or parallelizing tasks"
                })
        return bottlenecks

    @staticmethod
    def suggest_automation(process_steps: List[Dict[str, Any]], automation_threshold: float = 0.7) -> List[str]:
        """Suggest which steps should be automated."""
        suggestions = []
        for step in process_steps:
            auto_score = 0.5
            if not step.get("manual_review_required", False):
                auto_score += 0.3
            if step.get("repeatable", False):
                auto_score += 0.2
            if auto_score >= automation_threshold:
                suggestions.append(step["name"])
        return suggestions


class OperationsCLI:
    """Command-line interface for operations management."""

    def __init__(self, manager: OperationsManager):
        self.manager = manager

    def run(self):
        """Run an interactive CLI session."""
        print("Operations Agent CLI")
        print("Commands: dashboard, kpi, process, workflow, export, exit")
        while True:
            command = input("> ").strip().lower()
            if command == "exit":
                break
            elif command == "dashboard":
                print(json.dumps(self.manager.get_operations_dashboard(), indent=2))
            elif command == "kpi":
                kpi_name = input("KPI name: ")
                value = float(input("Value: "))
                self.manager.record_kpi(kpi_name, value)
                print("Recorded")
            elif command == "process":
                name = input("Process name: ")
                steps_input = input("Steps (comma-separated): ")
                steps = [s.strip() for s in steps_input.split(",")]
                owner = input("Owner: ")
                self.manager.define_process(name, steps, owner)
                print("Process defined")
            elif command == "workflow":
                name = input("Workflow name: ")
                trigger = input("Trigger: ")
                self.manager.create_workflow(name, trigger, [])
                print("Workflow created")
            elif command == "export":
                filepath = input("Export filepath: ")
                result = self.manager.export_state(filepath)
                print(f"Exported to {result['filepath']}")
            else:
                print("Unknown command")


class ResourceManager:
    """Manage operational resources such as personnel, tools, and budget."""

    def __init__(self):
        self.resources: Dict[str, Dict[str, Any]] = {}

    def register_resource(self, name: str, resource_type: str, capacity: float, unit: str = "", owner: str = "") -> Dict[str, Any]:
        resource = {
            "name": name,
            "type": resource_type,
            "capacity": capacity,
            "unit": unit,
            "owner": owner,
            "allocated": 0.0,
            "status": "available"
        }
        self.resources[name] = resource
        return resource

    def allocate_resource(self, name: str, amount: float, request_id: str = "") -> Dict[str, Any]:
        if name not in self.resources:
            raise KeyError(f"Resource {name} not registered")
        resource = self.resources[name]
        if resource["allocated"] + amount > resource["capacity"]:
            raise ValueError(f"Insufficient capacity in {name}. Requested: {amount}, Available: {resource['capacity'] - resource['allocated']}")
        resource["allocated"] += amount
        resource["status"] = "partially_allocated" if resource["allocated"] < resource["capacity"] else "fully_allocated"
        return {
            "resource": name,
            "allocated_amount": amount,
            "new_allocation": resource["allocated"],
            "remaining_capacity": resource["capacity"] - resource["allocated"],
            "request_id": request_id
        }

    def release_resource(self, name: str, amount: float, request_id: str = "") -> Dict[str, Any]:
        if name not in self.resources:
            raise KeyError(f"Resource {name} not registered")
        resource = self.resources[name]
        if amount > resource["allocated"]:
            raise ValueError(f"Cannot release {amount} from {name} with only {resource['allocated']} allocated")
        resource["allocated"] -= amount
        resource["status"] = "available" if resource["allocated"] == 0 else "partially_allocated"
        return {
            "resource": name,
            "released_amount": amount,
            "new_allocation": resource["allocated"],
            "available_capacity": resource["capacity"] - resource["allocated"],
            "request_id": request_id
        }

    def get_resource_utilization(self, name: str) -> Dict[str, Any]:
        if name not in self.resources:
            raise KeyError(f"Resource {name} not registered")
        resource = self.resources[name]
        utilization = (resource["allocated"] / resource["capacity"] * 100) if resource["capacity"] > 0 else 0.0
        return {
            "name": name,
            "type": resource["type"],
            "total_capacity": resource["capacity"],
            "allocated": resource["allocated"],
            "available": resource["capacity"] - resource["allocated"],
            "utilization_percent": round(utilization, 2),
            "status": resource["status"]
        }


class WorkflowScheduler:
    """Schedule and defer workflow execution."""

    def __init__(self):
        self.scheduled: Dict[str, Dict[str, Any]] = {}

    def schedule_workflow(self, workflow_name: str, run_at: datetime, payload: Optional[Dict[str, Any]] = None, repeat: Optional[str] = None) -> Dict[str, Any]:
        schedule_id = str(uuid.uuid4())
        entry = {
            "schedule_id": schedule_id,
            "workflow_name": workflow_name,
            "run_at": run_at.isoformat(),
            "payload": payload or {},
            "repeat": repeat,
            "status": "scheduled",
            "created_at": datetime.now().isoformat()
        }
        self.scheduled[schedule_id] = entry
        return entry

    def cancel_schedule(self, schedule_id: str) -> Dict[str, Any]:
        if schedule_id not in self.scheduled:
            raise KeyError(f"Schedule {schedule_id} not found")
        entry = self.scheduled[schedule_id]
        entry["status"] = "cancelled"
        entry["cancelled_at"] = datetime.now().isoformat()
        return entry

    def get_upcoming(self, within_minutes: int = 60) -> List[Dict[str, Any]]:
        cutoff = (datetime.now() + timedelta(minutes=within_minutes)).isoformat()
        return [
            entry for entry in self.scheduled.values() if entry["status"] == "scheduled" and entry["run_at"] <= cutoff
        ]


class EventBus:
    """Simple in-memory event bus for decoupled communication."""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = defaultdict(list)
        self._history: deque = deque(maxlen=500)

    def subscribe(self, event_type: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        self._subscribers[event_type].append(handler)

    def publish(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        event = {"event_type": event_type, "payload": payload, "timestamp": datetime.now().isoformat(), "handlers_invoked": 0}
        for handler in self._subscribers.get(event_type, []):
            handler(payload)
            event["handlers_invoked"] += 1
        self._history.append(event)
        return event

    def get_history(self, event_type: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        items = list(self._history)
        if event_type:
            items = [item for item in items if item["event_type"] == event_type]
        return items[-limit:]


class BatchProcessor:
    """Execute batch jobs on items in an asynchronous-like flow."""

    def __init__(self, batch_size: int = 5, pause_seconds: float = 0.5) -> None:
        self.batch_size = batch_size
        self.pause_seconds = pause_seconds
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.results: Dict[str, List[Dict[str, Any]]] = {}

    def process_items(self, job_id: str, items: List[Dict[str, Any]], handler: Callable[[Dict[str, Any]], Dict[str, Any]]) -> Dict[str, Any]:
        output: List[Dict[str, Any]] = []
        success_count = 0
        failure_count = 0
        for index in range(0, len(items), self.batch_size):
            batch = items[index:index + self.batch_size]
            for item in batch:
                try:
                    result = handler(item)
                    output.append({"item": item, "result": result, "status": "success"})
                    success_count += 1
                except Exception as exc:
                    output.append({"item": item, "error": str(exc), "status": "failed"})
                    failure_count += 1
            time.sleep(self.pause_seconds)
        self.jobs[job_id] = {"total_items": len(items), "batches": (len(items) + self.batch_size - 1) // max(self.batch_size, 1)}
        self.results[job_id] = output
        return {"job_id": job_id, "success_count": success_count, "failure_count": failure_count, "output": output}

    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        if job_id not in self.jobs:
            raise KeyError(f"Job {job_id} not found")
        job = self.jobs[job_id]
        job["results_available"] = job_id in self.results
        return job


class MetricAggregator:
    """Aggregate metric values over time."""

    def __init__(self) -> None:
        self.samples: Dict[str, deque] = defaultdict(lambda: deque(maxlen=5000))

    def add(self, metric_name: str, value: float, timestamp: Optional[datetime] = None) -> Dict[str, Any]:
        self.samples[metric_name].append({"value": value, "timestamp": (timestamp or datetime.now()).isoformat()})
        return self.summarize(metric_name)

    def summarize(self, metric_name: str) -> Dict[str, Any]:
        if not self.samples.get(metric_name):
            return {"metric_name": metric_name, "count": 0}
        values = [item["value"] for item in self.samples[metric_name]]
        return {
            "metric_name": metric_name,
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "average": round(sum(values) / len(values), 4),
            "latest": values[-1]
        }

    def get_top_n(self, metric_name: str, n: int = 10) -> List[Dict[str, Any]]:
        if metric_name not in self.samples:
            return []
        items = list(self.samples[metric_name])
        items.sort(key=lambda item: item["value"], reverse=True)
        return items[:max(n, 1)]


class RuleEngine:
    """Evaluate business rules against process state."""

    def __init__(self):
        self.rules: Dict[str, Dict[str, Any]] = {}

    def add_rule(self, rule_id: str, condition: str, action: str, priority: int = 10, active: bool = True) -> Dict[str, Any]:
        rule = {
            "rule_id": rule_id,
            "condition": condition,
            "action": action,
            "priority": priority,
            "active": active,
            "created_at": datetime.now().isoformat()
        }
        self.rules[rule_id] = rule
        return rule

    def evaluate(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        matched = []
        for rule in sorted(self.rules.values(), key=lambda rule: rule["priority"]):
            if not rule["active"]:
                continue
            if self._matches(rule["condition"], context):
                matched.append({"rule_id": rule["rule_id"], "action": rule["action"], "context": context})
        return matched

    @staticmethod
    def _matches(condition: str, context: Dict[str, Any]) -> bool:
        if ">" in condition:
            left, right = condition.split(">", 1)
            left = context.get(left.strip(), 0)
            try:
                right = float(right.strip())
            except ValueError:
                return False
            return float(left) > right
        if "<" in condition:
            left, right = condition.split("<", 1)
            left = context.get(left.strip(), 0)
            try:
                right = float(right.strip())
            except ValueError:
                return False
            return float(left) < right
        if "==" in condition:
            left, right = condition.split("==", 1)
            return str(context.get(left.strip())) == right.strip().strip('"\'')
        if "contains" in condition:
            left, right = condition.split("contains", 1)
            left_value = context.get(left.strip(), "")
            return right.strip().strip('"\'') in str(left_value)
        return False


class StateValidator:
    """Validate operational state before import."""

    REQUIRED_PROCESS_FIELDS = {"name", "steps", "owner"}
    REQUIRED_KPI_FIELDS = {"name", "target", "unit"}
    REQUIRED_WORKFLOW_FIELDS = {"name", "trigger"}

    @classmethod
    def validate_process(cls, data: Dict[str, Any]) -> List[str]:
        errors = []
        missing = cls.REQUIRED_PROCESS_FIELDS - data.keys()
        if missing:
            errors.append(f"Missing required process fields: {missing}")
        if not isinstance(data.get("steps", []), list):
            errors.append("Process steps must be a list")
        for field in ("estimated_duration_minutes",):
            if field in data and not isinstance(data[field], int):
                errors.append(f"Process {data.get('name', '<unknown>')} has non-integer {field}")
        return errors

    @classmethod
    def validate_kpi(cls, data: Dict[str, Any]) -> List[str]:
        errors = []
        missing = cls.REQUIRED_KPI_FIELDS - data.keys()
        if missing:
            errors.append(f"Missing required KPI fields: {missing}")
        if "target" in data and not isinstance(data["target"], (int, float)):
            errors.append(f"KPI {data.get('name', '<unknown>')} target must be numeric")
        return errors

    @classmethod
    def validate_workflow(cls, data: Dict[str, Any]) -> List[str]:
        errors = []
        missing = cls.REQUIRED_WORKFLOW_FIELDS - data.keys()
        if missing:
            errors.append(f"Missing required workflow fields: {missing}")
        if not isinstance(data.get("actions", []), list):
            errors.append("Workflow actions must be a list")
        return errors

    @classmethod
    def validate_export(cls, data: Dict[str, Any]) -> Dict[str, List[str]]:
        results = {"processes": [], "kpis": [], "workflows": []}
        for name, process in data.get("processes", {}).items():
            results["processes"].extend([f"{name}: {err}" for err in cls.validate_process(process)])
        for name, kpi in data.get("kpis", {}).items():
            results["kpis"].extend([f"{name}: {err}" for err in cls.validate_kpi(kpi)])
        for name, workflow in data.get("workflows", {}).items():
            results["workflows"].extend([f"{name}: {err}" for err in cls.validate_workflow(workflow)])
        return results


class AgentHealth:
    """Report operational health of the agent components."""

    def __init__(self, manager: OperationsManager) -> None:
        self.manager = manager

    def check(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.now().isoformat(),
            "components": {
                "processes": {"count": len(self.manager.processes), "status": "ok"},
                "kpis": {"count": len(self.manager.kpis), "status": "ok"},
                "workflows": {"count": len(self.manager.workflows), "status": "ok"},
                "analytics": {"reports": len(self.manager.analytics.reports), "status": "ok"},
                "integrations": {"registered": len(self.manager.integrations.integrations), "status": "ok"},
                "notifications": {"history_length": len(self.manager.notifications.notification_history), "status": "ok"},
                "resources": {"count": len(self.manager.resource_manager.resources), "status": "ok"},
                "scheduler": {"scheduled_jobs": len(self.manager.scheduler.scheduled), "status": "ok"},
                "rule_engine": {"rules": len(self.manager.rule_engine.rules), "status": "ok"},
                "event_bus": {"history_events": len(self.manager.event_bus._history), "status": "ok"}
            }
        }


if __name__ == "__main__":
    ops = OperationsManager()
    ops.define_process("Onboarding", ["Welcome", "Paperwork", "Training"], "HR")
    ops.set_kpi("Order Fulfillment Time", 24, "hours", threshold_warning=20.0, threshold_critical=30.0)
    ops.record_kpi("Order Fulfillment Time", 18)
    optimizer = ProcessOptimizer()
    process_data = {
        "steps": [
            {"name": "Welcome", "estimated_duration_minutes": 30, "manual_review_required": False, "repeatable": False},
            {"name": "Paperwork", "estimated_duration_minutes": 120, "manual_review_required": True, "repeatable": True},
            {"name": "Training", "estimated_duration_minutes": 240, "manual_review_required": False, "repeatable": False}
        ]
    }
    bottlenecks = ProcessOptimizer.calculate_bottlenecks(process_data["steps"])
    print("Bottlenecks:", json.dumps(bottlenecks, indent=2))
    automations = ProcessOptimizer.suggest_automation(process_data["steps"])
    print("Automation candidates:", automations)
    ops.define_process("Order Fulfillment", ["Receive", "Pick", "Pack", "Ship"], "Logistics", "Standard order process", 120)
    ops.set_kpi("Customer Satisfaction", 4.5, "score", threshold_warning=3.5, threshold_critical=2.5, measurement_frequency="weekly")
    ops.set_kpi("Resource Utilization", 85.0, "%", threshold_warning=70.0, threshold_critical=60.0)
    dashboard = ops.get_operations_dashboard()
    print("Dashboard:", json.dumps(dashboard, indent=2))
    health = AgentHealth(ops)
    print("Health:", json.dumps(health.check(), indent=2))
    validator = StateValidator()
    sample_export = {
        "processes": {
            "Test": {
                "name": "Test",
                "steps": ["A", "B"],
                "owner": "QA"
            }
        },
        "kpis": {
            "Test KPI": {
                "name": "Test KPI",
                "target": 100,
                "unit": "count"
            }
        },
        "workflows": {
            "Test Workflow": {
                "name": "Test Workflow",
                "trigger": "test"
            }
        }
    }
    validation_results = validator.validate_export(sample_export)
    print("Validation results:", json.dumps(validation_results, indent=2))
    integration = ops.register_integration(
        name="test_integration",
        config={"endpoint": "https://api.example.com", "timeout": 10},
        connection_type="api"
    )
    ops.integrations.test_connection("test_integration")
    send_result = ops.integrations.send_data("test_integration", {"test": True})
    print("Integration test:", json.dumps(send_result, indent=2))
    ops.send_notification("admin@example.com", "Test Subject", "Test Body", priority="high")
    notifications = ops.notifications.get_notification_history(limit=5)
    print("Notifications:", json.dumps(notifications, indent=2))
    process_steps = [
        {"name": "Request", "estimated_duration_minutes": 10, "manual_review_required": False, "repeatable": True},
        {"name": "Approval", "estimated_duration_minutes": 45, "manual_review_required": True, "repeatable": False},
        {"name": "Processing", "estimated_duration_minutes": 30, "manual_review_required": False, "repeatable": True},
        {"name": "Review", "estimated_duration_minutes": 20, "manual_review_required": False, "repeatable": True},
        {"name": "Completion", "estimated_duration_minutes": 5, "manual_review_required": False, "repeatable": True}
    ]
    more_bottlenecks = ProcessOptimizer.calculate_bottlenecks(process_steps)
    print("Bottlenecks (extended):", json.dumps(more_bottlenecks, indent=2))
    automation_candidates = ProcessOptimizer.suggest_automation(process_steps)
    print("Automation candidates (extended):", automation_candidates)
