"""
Drift Detection Module
Infrastructure configuration drift detection and remediation
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple
import uuid

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class DriftType(Enum):
    CONFIGURATION = "configuration"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    COST = "cost"
    PERMISSIONS = "permissions"
    NETWORK = "network"


class DriftSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DriftStatus(Enum):
    DETECTED = "detected"
    ACKNOWLEDGED = "acknowledged"
    REMEDIATING = "remediating"
    REMEDIATED = "remediated"
    ACCEPTED = "accepted"
    EXPIRED = "expired"


class RemediationAction(Enum):
    TERRAFORM_APPLY = "terraform_apply"
    CLOUDFORMATION_UPDATE = "cloudformation_update"
    MANUAL_REVIEW = "manual_review"
    AUTO_REVERT = "auto_revert"
    NOTIFY_ONLY = "notify_only"


class CheckType(Enum):
    TERRAFORM = "terraform"
    CLOUDFORMATION = "cloudformation"
    PULUMI = "pulumi"
    CUSTOM = "custom"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class DriftCheckConfig:
    """Configuration for drift detection checks."""
    terraform_workspaces: List[str] = field(default_factory=list)
    state_backends: Dict[str, str] = field(default_factory=dict)
    cloudformation_stacks: List[str] = field(default_factory=list)
    check_interval_minutes: int = 30
    enable_auto_remediation: bool = False
    severity_threshold: DriftSeverity = DriftSeverity.LOW

    def get_workspaces(self) -> List[str]:
        return self.terraform_workspaces


@dataclass
class ResourceChange:
    """A single resource change detected."""
    attribute: str = ""
    expected: Any = None
    actual: Any = None
    change_type: str = "update"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "attribute": self.attribute,
            "expected": str(self.expected),
            "actual": str(self.actual),
            "type": self.change_type,
        }


@dataclass
class DriftedResource:
    """A resource that has drifted from desired state."""
    resource_address: str = ""
    resource_type: str = ""
    resource_name: str = ""
    drift_type: DriftType = DriftType.CONFIGURATION
    severity: DriftSeverity = DriftSeverity.LOW
    changes: List[ResourceChange] = field(default_factory=list)
    detected_at: datetime = field(default_factory=datetime.utcnow)
    workspace: str = ""
    module: str = ""

    @property
    def change_count(self) -> int:
        return len(self.changes)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "address": self.resource_address,
            "type": self.resource_type,
            "name": self.resource_name,
            "drift_type": self.drift_type.value,
            "severity": self.severity.value,
            "changes": [c.to_dict() for c in self.changes],
            "detected_at": self.detected_at.isoformat(),
        }


@dataclass
class DriftCheckResult:
    """Result of a drift detection check."""
    check_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    workspace: str = ""
    check_type: CheckType = CheckType.TERRAFORM
    timestamp: datetime = field(default_factory=datetime.utcnow)
    resources_checked: int = 0
    resources_in_sync: int = 0
    drifted_count: int = 0
    drifted_resources: List[DriftedResource] = field(default_factory=list)
    duration_seconds: float = 0.0
    errors: List[str] = field(default_factory=list)

    @property
    def in_sync_count(self) -> int:
        return self.resources_in_sync

    @property
    def has_drift(self) -> bool:
        return self.drifted_count > 0

    @property
    def drift_percentage(self) -> float:
        if self.resources_checked == 0:
            return 0.0
        return (self.drifted_count / self.resources_checked) * 100


@dataclass
class DriftEvent:
    """A drift event requiring attention."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    drift: DriftedResource = field(default_factory=DriftedResource)
    status: DriftStatus = DriftStatus.DETECTED
    assigned_to: Optional[str] = None
    remediation_action: Optional[RemediationAction] = None
    notes: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None

    @property
    def age_minutes(self) -> float:
        return (datetime.utcnow() - self.created_at).total_seconds() / 60


@dataclass
class MonitoringSchedule:
    """Schedule for continuous monitoring."""
    interval_minutes: int = 15
    environments: List[str] = field(default_factory=list)
    check_types: List[str] = field(default_factory=list)
    quiet_hours_start: int = 2
    quiet_hours_end: int = 6

    def is_quiet_hours(self) -> bool:
        current_hour = datetime.utcnow().hour
        return self.quiet_hours_start <= current_hour < self.quiet_hours_end


@dataclass
class MonitorStatus:
    """Status of the drift monitor."""
    state: str = "running"
    last_check: Optional[datetime] = None
    next_scheduled: Optional[datetime] = None
    total_drift_events: int = 0
    active_drift_events: int = 0
    uptime_minutes: float = 0.0


@dataclass
class RemediationPolicy:
    """Policy for automatic remediation."""
    name: str = ""
    trigger: str = ""
    action: RemediationAction = RemediationAction.NOTIFY_ONLY
    auto_approve: bool = False
    approvers: List[str] = field(default_factory=list)
    notification_required: bool = True
    max_auto_remediations_per_hour: int = 5

    def matches_drift(self, drift: DriftedResource) -> bool:
        return self.trigger in (drift.drift_type.value, "any")


@dataclass
class RemediationResult:
    """Result of a remediation action."""
    remediation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    drift_event_id: str = ""
    action: RemediationAction = RemediationAction.NOTIFY_ONLY
    status: str = "pending"
    auto_approved: bool = False
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    output: str = ""
    errors: List[str] = field(default_factory=list)


@dataclass
class ComplianceReport:
    """Compliance and drift status report."""
    report_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    period_start: datetime = field(default_factory=datetime.utcnow)
    period_end: datetime = field(default_factory=datetime.utcnow)
    environments: List[str] = field(default_factory=list)
    total_checks: int = 0
    drift_events: int = 0
    remediated_count: int = 0
    accepted_count: int = 0
    pending_count: int = 0
    compliance_rate: float = 100.0
    drift_by_type: Dict[str, int] = field(default_factory=dict)
    drift_by_severity: Dict[str, int] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Drift Detector
# ---------------------------------------------------------------------------

class DriftDetector:
    """Main drift detection engine."""

    def __init__(self, config: Optional[DriftCheckConfig] = None) -> None:
        self.config = config or DriftCheckConfig()
        self._check_history: List[DriftCheckResult] = []
        self._drift_events: List[DriftEvent] = []

    def check_terraform_drift(self, workspace: str = "default") -> DriftCheckResult:
        result = DriftCheckResult(
            workspace=workspace,
            check_type=CheckType.TERRAFORM,
        )

        # Simulate drift detection
        result.resources_checked = 50
        result.resources_in_sync = 46
        result.drifted_count = 4
        result.duration_seconds = 8.5

        # Simulate drifted resources
        drifts = [
            DriftedResource(
                resource_address=f"aws_security_group.web",
                resource_type="aws_security_group",
                resource_name="web",
                drift_type=DriftType.SECURITY,
                severity=DriftSeverity.HIGH,
                changes=[
                    ResourceChange(attribute="ingress", expected="80,443", actual="80,443,22"),
                ],
                workspace=workspace,
            ),
            DriftedResource(
                resource_address=f"aws_instance.app",
                resource_type="aws_instance",
                resource_name="app",
                drift_type=DriftType.CONFIGURATION,
                severity=DriftSeverity.LOW,
                changes=[
                    ResourceChange(attribute="instance_type", expected="t3.medium", actual="t3.large"),
                ],
                workspace=workspace,
            ),
            DriftedResource(
                resource_address=f"aws_s3_bucket.data",
                resource_type="aws_s3_bucket",
                resource_name="data",
                drift_type=DriftType.COMPLIANCE,
                severity=DriftSeverity.MEDIUM,
                changes=[
                    ResourceChange(attribute="acl", expected="private", actual="public-read"),
                ],
                workspace=workspace,
            ),
        ]

        result.drifted_resources = drifts
        self._check_history.append(result)
        return result

    def check_cloudformation_drift(self, stack_name: str) -> DriftCheckResult:
        result = DriftCheckResult(
            workspace=stack_name,
            check_type=CheckType.CLOUDFORMATION,
        )
        result.resources_checked = 25
        result.resources_in_sync = 24
        result.drifted_count = 1
        return result

    def get_check_history(self, workspace: Optional[str] = None) -> List[DriftCheckResult]:
        if workspace:
            return [c for c in self._check_history if c.workspace == workspace]
        return self._check_history

    def get_drift_events(self, status: Optional[DriftStatus] = None) -> List[DriftEvent]:
        if status:
            return [e for e in self._drift_events if e.status == status]
        return self._drift_events

    def get_summary(self) -> Dict[str, Any]:
        total_checks = len(self._check_history)
        checks_with_drift = sum(1 for c in self._check_history if c.has_drift)
        return {
            "total_checks": total_checks,
            "checks_with_drift": checks_with_drift,
            "drift_rate": (checks_with_drift / total_checks * 100) if total_checks > 0 else 0.0,
            "drift_events": len(self._drift_events),
        }


# ---------------------------------------------------------------------------
# Drift Monitor
# ---------------------------------------------------------------------------

class DriftMonitor:
    """Continuous drift monitoring."""

    def __init__(
        self,
        schedule: Optional[MonitoringSchedule] = None,
        notifications: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.schedule = schedule or MonitoringSchedule()
        self.notifications = notifications or {}
        self._status = MonitorStatus()
        self._drift_detector = DriftDetector()
        self._events: List[DriftEvent] = []

    def start(self) -> None:
        self._status.state = "running"
        self._status.last_check = datetime.utcnow()
        logger.info("Drift monitor started")

    def stop(self) -> None:
        self._status.state = "stopped"
        logger.info("Drift monitor stopped")

    def run_check(self) -> List[DriftCheckResult]:
        results = []
        for env in self.schedule.environments:
            result = self._drift_detector.check_terraform_drift(workspace=env)
            results.append(result)
            if result.has_drift:
                for drift in result.drifted_resources:
                    event = DriftEvent(drift=drift)
                    self._events.append(event)
                    self._status.total_drift_events += 1
                    self._status.active_drift_events += 1
        self._status.last_check = datetime.utcnow()
        return results

    def get_status(self) -> MonitorStatus:
        return self._status


# ---------------------------------------------------------------------------
# Remediation Engine
# ---------------------------------------------------------------------------

class RemediationEngine:
    """Handles drift remediation based on policies."""

    def __init__(self, policies: Optional[List[RemediationPolicy]] = None) -> None:
        self.policies = policies or []
        self._remediation_history: List[RemediationResult] = []

    def find_policy(self, drift: DriftedResource) -> Optional[RemediationPolicy]:
        for policy in self.policies:
            if policy.matches_drift(drift):
                return policy
        return None

    def remediate(self, drift_event: DriftEvent) -> RemediationResult:
        policy = self.find_policy(drift_event.drift)
        if policy is None:
            return RemediationResult(
                drift_event_id=drift_event.event_id,
                action=RemediationAction.NOTIFY_ONLY,
                status="skipped",
                output="No matching policy found",
            )

        result = RemediationResult(
            drift_event_id=drift_event.event_id,
            action=policy.action,
        )

        if policy.auto_approve:
            result.auto_approved = True
            result.status = "executing"
            # Simulate remediation execution
            result.status = "completed"
            result.output = f"Auto-remediation executed: {policy.action.value}"
        else:
            result.status = "pending_approval"

        result.completed_at = datetime.utcnow()
        self._remediation_history.append(result)
        return result

    def get_history(self) -> List[RemediationResult]:
        return self._remediation_history


# ---------------------------------------------------------------------------
# Compliance Reporter
# ---------------------------------------------------------------------------

class ComplianceReporter:
    """Generates compliance and drift reports."""

    def generate_report(
        self,
        time_range_days: int = 30,
        environments: Optional[List[str]] = None,
    ) -> ComplianceReport:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=time_range_days)

        report = ComplianceReport(
            period_start=start_date,
            period_end=end_date,
            environments=environments or [],
            total_checks=100,
            drift_events=12,
            remediated_count=10,
            accepted_count=1,
            pending_count=1,
            drift_by_type={
                "security": 3,
                "configuration": 5,
                "compliance": 4,
            },
            drift_by_severity={
                "critical": 1,
                "high": 3,
                "medium": 5,
                "low": 3,
            },
        )

        # Calculate compliance rate
        non_compliant = report.drift_events - report.remediated_count - report.accepted_count
        report.compliance_rate = max(0, (1 - non_compliant / max(report.total_checks, 1)) * 100)

        # Add recommendations
        if report.drift_by_type.get("security", 0) > 0:
            report.recommendations.append("Review security-related drift events immediately")
        if report.drift_by_severity.get("critical", 0) > 0:
            report.recommendations.append("Address critical severity drifts as highest priority")

        return report


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the Drift Detection module."""
    print("=" * 60)
    print("  Drift Detection Module — Demo")
    print("=" * 60)

    # Drift detection
    detector = DriftDetector(
        config=DriftCheckConfig(
            terraform_workspaces=["production", "staging"],
            check_interval_minutes=30,
        )
    )

    result = detector.check_terraform_drift(workspace="production")
    print(f"\n[+] Drift Check Results:")
    print(f"    Resources Checked: {result.resources_checked}")
    print(f"    In Sync: {result.in_sync_count}")
    print(f"    Drifted: {result.drifted_count}")
    print(f"    Drift %: {result.drift_percentage:.1f}%")

    for drift in result.drifted_resources:
        print(f"\n    Drift: {drift.resource_address}")
        print(f"      Type: {drift.drift_type.value}, Severity: {drift.severity.value}")
        for change in drift.changes:
            print(f"      Change: {change.attribute}: {change.expected} -> {change.actual}")

    # Monitor
    monitor = DriftMonitor(
        schedule=MonitoringSchedule(environments=["production"], interval_minutes=15),
    )
    monitor.start()
    status = monitor.get_status()
    print(f"\n[+] Monitor Status: {status.state}")

    # Remediation
    remediation_engine = RemediationEngine(
        policies=[
            RemediationPolicy(name="auto-revert-security", trigger="security", action=RemediationAction.AUTO_REVERT, auto_approve=True),
            RemediationPolicy(name="manual-review", trigger="configuration", action=RemediationAction.MANUAL_REVIEW),
        ]
    )

    if result.drifted_resources:
        event = DriftEvent(drift=result.drifted_resources[0])
        remediation = remediation_engine.remediate(event)
        print(f"\n[+] Remediation:")
        print(f"    Action: {remediation.action.value}")
        print(f"    Status: {remediation.status}")
        print(f"    Auto-approved: {remediation.auto_approved}")

    # Compliance report
    reporter = ComplianceReporter()
    report = reporter.generate_report(time_range_days=30, environments=["production"])
    print(f"\n[+] Compliance Report:")
    print(f"    Period: {report.period_start.strftime('%Y-%m-%d')} to {report.period_end.strftime('%Y-%m-%d')}")
    print(f"    Total Checks: {report.total_checks}")
    print(f"    Drift Events: {report.drift_events}")
    print(f"    Compliance Rate: {report.compliance_rate:.1f}%")
    print(f"    Recommendations: {len(report.recommendations)}")

    # Summary
    summary = detector.get_summary()
    print(f"\n[+] Detection Summary: {summary}")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
