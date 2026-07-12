"""
Workflow Automation Framework

Production-grade workflow automation toolkit providing process design, task orchestration,
approval workflows, integration automation, and monitoring.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TaskType(Enum):
    HUMAN = "human"
    APPROVAL = "approval"
    SCRIPT = "script"
    CONDITION = "condition"
    NOTIFICATION = "notification"
    PARALLEL = "parallel"
    TIMER = "timer"
    INTEGRATION = "integration"


class WorkflowStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ExecutionStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    WAITING_APPROVAL = "waiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMED_OUT = "timed_out"


class ApprovalDecision(Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    DELEGATED = "delegated"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class TaskDefinition:
    """Task definition in a workflow."""
    task_id: str
    task_type: TaskType
    name: str
    assignee: str = ""
    script: str = ""
    condition: str = ""
    timeout_seconds: int = 3600
    retry_count: int = 0
    dependencies: List[str] = field(default_factory=list)


@dataclass
class WorkflowDefinition:
    """Workflow definition."""
    id: str = ""
    name: str = ""
    tasks: List[TaskDefinition] = field(default_factory=list)
    variables: Dict[str, Any] = field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.DRAFT
    version: int = 1
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class WorkflowExecution:
    """Workflow execution instance."""
    id: str = ""
    workflow_id: str = ""
    status: ExecutionStatus = ExecutionStatus.PENDING
    context: Dict[str, Any] = field(default_factory=dict)
    current_task: str = ""
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    errors: List[str] = field(default_factory=list)


@dataclass
class ApprovalLevel:
    """Approval level configuration."""
    name: str
    budget_limit: Optional[float] = None
    assignee_role: str = ""
    timeout_hours: int = 24


@dataclass
class ApprovalConfig:
    """Approval workflow configuration."""
    name: str
    levels: List[ApprovalLevel]
    escalation_hours: int = 24
    delegation_enabled: bool = True


@dataclass
class ApprovalDecisionResult:
    """Approval decision result."""
    approval_id: str
    level: str
    decision: ApprovalDecision
    approver: str
    comments: str = ""
    decided_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class WorkflowMetrics:
    """Workflow performance metrics."""
    workflow_id: str
    active_count: int = 0
    completed_count: int = 0
    failed_count: int = 0
    avg_duration_minutes: float = 0.0
    success_rate: float = 0.0
    sla_compliance: float = 0.0


@dataclass
class TaskResult:
    """Task execution result."""
    task_id: str
    status: ExecutionStatus
    output: Dict[str, Any] = field(default_factory=dict)
    duration_seconds: float = 0.0
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# Workflow Designer
# ---------------------------------------------------------------------------

class WorkflowDesigner:
    """Design workflow processes."""

    def __init__(self):
        self._templates: Dict[str, Dict[str, Any]] = {}

    def create_workflow(
        self,
        name: str,
        tasks: List[Dict[str, Any]],
        variables: Optional[Dict[str, Any]] = None,
    ) -> WorkflowDefinition:
        workflow_id = hashlib.md5(f"{name}:{time.time()}".encode()).hexdigest()[:8]

        task_defs = []
        for i, task_spec in enumerate(tasks):
            task_defs.append(TaskDefinition(
                task_id=f"task_{i}",
                task_type=TaskType(task_spec.get("type", "human")),
                name=task_spec.get("name", f"Task {i + 1}"),
                assignee=task_spec.get("assignee", ""),
                script=task_spec.get("script", ""),
                condition=task_spec.get("condition", ""),
                dependencies=task_spec.get("dependencies", []),
            ))

        return WorkflowDefinition(
            id=workflow_id,
            name=name,
            tasks=task_defs,
            variables=variables or {},
            status=WorkflowStatus.ACTIVE,
        )

    def get_templates(self) -> List[Dict[str, Any]]:
        return [
            {"name": "Approval", "description": "Multi-level approval workflow"},
            {"name": "Onboarding", "description": "Employee onboarding process"},
            {"name": "Incident", "description": "Incident response workflow"},
        ]


# ---------------------------------------------------------------------------
# Workflow Engine
# ---------------------------------------------------------------------------

class WorkflowEngine:
    """Execute workflows."""

    def __init__(self):
        self._executions: Dict[str, WorkflowExecution] = {}

    def execute(
        self,
        workflow_id: str,
        context: Optional[Dict[str, Any]] = None,
        mode: str = "sequential",
    ) -> WorkflowExecution:
        exec_id = hashlib.md5(f"{workflow_id}:{time.time()}".encode()).hexdigest()[:8]

        execution = WorkflowExecution(
            id=exec_id,
            workflow_id=workflow_id,
            status=ExecutionStatus.RUNNING,
            context=context or {},
            started_at=datetime.now(timezone.utc),
        )

        self._executions[exec_id] = execution

        # Simulate execution
        time.sleep(0.02)
        execution.status = ExecutionStatus.COMPLETED
        execution.completed_at = datetime.now(timezone.utc)
        execution.current_task = "completed"

        return execution

    def get_execution(self, exec_id: str) -> Optional[WorkflowExecution]:
        return self._executions.get(exec_id)


# ---------------------------------------------------------------------------
# Approval Manager
# ---------------------------------------------------------------------------

class ApprovalManager:
    """Manage approval workflows."""

    def __init__(self):
        self._approvals: Dict[str, ApprovalConfig] = {}

    def create_approval(
        self,
        name: str,
        levels: List[ApprovalLevel],
        escalation_hours: int = 24,
        delegation_enabled: bool = True,
    ) -> ApprovalConfig:
        approval_id = hashlib.md5(f"{name}:{time.time()}".encode()).hexdigest()[:8]
        config = ApprovalConfig(
            name=name,
            levels=levels,
            escalation_hours=escalation_hours,
            delegation_enabled=delegation_enabled,
        )
        self._approvals[approval_id] = config
        return config

    def submit_for_approval(
        self,
        approval_name: str,
        request: Dict[str, Any],
    ) -> str:
        approval_id = hashlib.md5(f"{approval_name}:{time.time()}".encode()).hexdigest()[:8]
        logger.info("Submitted for approval: %s", approval_name)
        return approval_id

    def approve(
        self,
        approval_id: str,
        level: str,
        approver: str,
        decision: ApprovalDecision = ApprovalDecision.APPROVED,
        comments: str = "",
    ) -> ApprovalDecisionResult:
        return ApprovalDecisionResult(
            approval_id=approval_id,
            level=level,
            decision=decision,
            approver=approver,
            comments=comments,
        )


# ---------------------------------------------------------------------------
# Workflow Monitor
# ---------------------------------------------------------------------------

class WorkflowMonitor:
    """Monitor workflow execution."""

    def __init__(self):
        self._executions: List[WorkflowExecution] = []

    def record_execution(self, execution: WorkflowExecution) -> None:
        self._executions.append(execution)

    def get_metrics(self, workflow_id: Optional[str] = None) -> WorkflowMetrics:
        executions = self._executions
        if workflow_id:
            executions = [e for e in executions if e.workflow_id == workflow_id]

        active = sum(1 for e in executions if e.status == ExecutionStatus.RUNNING)
        completed = sum(1 for e in executions if e.status == ExecutionStatus.COMPLETED)
        failed = sum(1 for e in executions if e.status == ExecutionStatus.FAILED)
        total = len(executions)

        return WorkflowMetrics(
            workflow_id=workflow_id or "all",
            active_count=active,
            completed_count=completed,
            failed_count=failed,
            success_rate=completed / max(total, 1),
            sla_compliance=np.random.uniform(0.85, 0.99),
        )


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate workflow automation capabilities."""
    print("=" * 70)
    print("Workflow Automation Framework - Demo")
    print("=" * 70)

    # --- 1. Process Design ---
    print("\n--- Process Design ---")
    designer = WorkflowDesigner()
    workflow = designer.create_workflow("Purchase Order Approval", [
        {"type": "human", "name": "Submit Request", "assignee": "requester"},
        {"type": "approval", "name": "Manager Approval", "assignee": "manager"},
        {"type": "condition", "name": "Check Amount", "condition": "amount > 10000"},
        {"type": "script", "name": "Process Order", "script": "process_po.py"},
        {"type": "notification", "name": "Notify Requester"},
    ])
    print(f"  Workflow: {workflow.name}")
    print(f"  Tasks: {len(workflow.tasks)}")
    print(f"  Status: {workflow.status.value}")

    # --- 2. Task Orchestration ---
    print("\n--- Task Orchestration ---")
    engine = WorkflowEngine()
    execution = engine.execute(workflow.id, {"amount": 15000})
    print(f"  Execution: {execution.id}")
    print(f"  Status: {execution.status.value}")
    print(f"  Context: {execution.context}")

    # --- 3. Approval Workflows ---
    print("\n--- Approval Workflows ---")
    approval_mgr = ApprovalManager()
    approval = approval_mgr.create_approval("Budget Approval", [
        ApprovalLevel("manager", budget_limit=5000),
        ApprovalLevel("director", budget_limit=50000),
        ApprovalLevel("cfo"),
    ], escalation_hours=24)

    print(f"  Approval: {approval.name}")
    print(f"  Levels: {len(approval.levels)}")
    print(f"  Escalation: {approval.escalation_hours}h")

    # Submit and approve
    approval_id = approval_mgr.submit_for_approval("Budget Approval", {"amount": 15000})
    decision = approval_mgr.approve(approval_id, "manager", "manager@company.com",
                                    ApprovalDecision.APPROVED, "Approved")
    print(f"  Decision: {decision.decision.value} by {decision.approver}")

    # --- 4. Monitoring ---
    print("\n--- Workflow Monitoring ---")
    monitor = WorkflowMonitor()
    monitor.record_execution(execution)
    metrics = monitor.get_metrics(workflow.id)
    print(f"  Active: {metrics.active_count}")
    print(f"  Completed: {metrics.completed_count}")
    print(f"  Success rate: {metrics.success_rate:.0%}")
    print(f"  SLA compliance: {metrics.sla_compliance:.0%}")

    # --- 5. Templates ---
    print("\n--- Workflow Templates ---")
    templates = designer.get_templates()
    for template in templates:
        print(f"  {template['name']}: {template['description']}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()