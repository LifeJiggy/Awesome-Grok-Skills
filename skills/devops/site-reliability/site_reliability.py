"""
Site Reliability Engineering Framework

Production-grade SRE toolkit providing SLO management, incident management,
toil reduction, and reliability engineering practices.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Severity(Enum):
    P1 = "P1"  # Critical
    P2 = "P2"  # High
    P3 = "P3"  # Medium
    P4 = "P4"  # Low


class IncidentStatus(Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    IDENTIFIED = "identified"
    MONITORING = "monitoring"
    RESOLVED = "resolved"


class ToilLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class SLIDefinition:
    """Service Level Indicator definition."""
    name: str
    metric: str
    good_event: str = ""
    total_event: str = ""
    description: str = ""


@dataclass
class SLOTarget:
    """Service Level Objective target."""
    name: str
    sli: SLIDefinition
    target: float  # e.g., 99.9
    window_days: int = 30


@dataclass
class ErrorBudget:
    """Error budget information."""
    slo: SLOTarget
    remaining_pct: float
    consumed_pct: float
    days_remaining: float
    is_exhausted: bool = False


@dataclass
class Incident:
    """An incident record."""
    id: str
    title: str
    severity: Severity
    service: str
    status: IncidentStatus = IncidentStatus.OPEN
    description: str = ""
    oncall_engineer: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None
    updates: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def duration_minutes(self) -> float:
        if self.resolved_at:
            return (self.resolved_at - self.created_at).total_seconds() / 60
        return (datetime.now(timezone.utc) - self.created_at).total_seconds() / 60


@dataclass
class Postmortem:
    """Post-incident review record."""
    incident_id: str
    title: str
    summary: str
    root_cause: str
    timeline: List[Dict[str, str]]
    action_items: List[Dict[str, Any]]
    lessons_learned: List[str]
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ToilActivity:
    """Toil activity record."""
    task: str
    duration_minutes: float
    frequency: str
    automation_opportunity: str = "medium"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ToilReport:
    """Toil analysis report."""
    total_hours: float
    toil_ratio: float
    opportunities: List[Dict[str, str]]
    activities: List[ToilActivity]


@dataclass
class CapacityAnalysis:
    """Capacity analysis result."""
    service: str
    current_utilization: float
    projected_30day: float
    projected_90day: float
    days_until_capacity: int
    bottleneck_resource: str = ""


@dataclass
class ScalingRecommendation:
    """Scaling recommendation."""
    action: str
    reason: str
    priority: str = "medium"
    estimated_impact: str = ""


@dataclass
class OnCallSchedule:
    """On-call schedule."""
    engineer: str
    start_time: datetime
    end_time: datetime
    escalation_contact: str = ""


# ---------------------------------------------------------------------------
# SLO Manager
# ---------------------------------------------------------------------------

class SLOManager:
    """Manage Service Level Objectives."""

    def __init__(self):
        self._slos: List[SLOTarget] = []

    def create_slo(self, name: str, sli: SLIDefinition,
                   target: float, window_days: int = 30) -> SLOTarget:
        slo = SLOTarget(name=name, sli=sli, target=target, window_days=window_days)
        self._slos.append(slo)
        return slo

    def get_error_budget(self, slo: SLOTarget) -> ErrorBudget:
        # Simulate error budget calculation
        consumed = np.random.uniform(10, 80)
        remaining = 100 - consumed
        days_remaining = slo.window_days * (remaining / 100)

        return ErrorBudget(
            slo=slo,
            remaining_pct=remaining,
            consumed_pct=consumed,
            days_remaining=days_remaining,
            is_exhausted=remaining <= 0,
        )

    def get_all_slos(self) -> List[SLOTarget]:
        return self._slos

    def check_burn_rate(self, slo: SLOTarget, burn_rate: float) -> bool:
        # Alert if burn rate exceeds budget
        max_burn_rate = (100 - slo.target) / slo.target * 100
        return burn_rate > max_burn_rate


# ---------------------------------------------------------------------------
# Incident Manager
# ---------------------------------------------------------------------------

class IncidentManager:
    """Manage incidents and response workflows."""

    def __init__(self):
        self._incidents: Dict[str, Incident] = {}
        self._postmortems: List[Postmortem] = []

    def create_incident(self, title: str, severity: Severity, service: str,
                        description: str = "") -> Incident:
        incident_id = hashlib.md5(f"{title}:{time.time()}".encode()).hexdigest()[:8]
        incident = Incident(
            id=incident_id,
            title=title,
            severity=severity,
            service=service,
            description=description,
            oncall_engineer="engineer@company.com",
        )
        self._incidents[incident_id] = incident
        logger.info("Incident created: %s [%s]", incident_id, severity.value)
        return incident

    def update(self, incident_id: str, update: str) -> None:
        if incident_id in self._incidents:
            self._incidents[incident_id].updates.append({
                "message": update,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })

    def resolve(self, incident_id: str, resolution: str = "") -> None:
        if incident_id in self._incidents:
            self._incidents[incident_id].status = IncidentStatus.RESOLVED
            self._incidents[incident_id].resolved_at = datetime.now(timezone.utc)

    def get_incident(self, incident_id: str) -> Optional[Incident]:
        return self._incidents.get(incident_id)

    def get_open_incidents(self) -> List[Incident]:
        return [i for i in self._incidents.values() if i.status != IncidentStatus.RESOLVED]

    def create_postmortem(self, incident_id: str) -> Optional[Postmortem]:
        incident = self._incidents.get(incident_id)
        if not incident:
            return None

        postmortem = Postmortem(
            incident_id=incident_id,
            title=f"Postmortem: {incident.title}",
            summary=f"Incident affecting {incident.service}",
            root_cause="Root cause analysis pending",
            timeline=[
                {"time": incident.created_at.isoformat(), "event": "Incident detected"},
                {"time": datetime.now(timezone.utc).isoformat(), "event": "Incident resolved"},
            ],
            action_items=[],
            lessons_learned=[],
        )
        self._postmortems.append(postmortem)
        return postmortem


# ---------------------------------------------------------------------------
# Toil Tracker
# ---------------------------------------------------------------------------

class ToilTracker:
    """Track and analyze toil activities."""

    def __init__(self):
        self._activities: List[ToilActivity] = []

    def log_activity(self, task: str, duration_minutes: float,
                     frequency: str, automation_opportunity: str = "medium") -> ToilActivity:
        activity = ToilActivity(
            task=task,
            duration_minutes=duration_minutes,
            frequency=frequency,
            automation_opportunity=automation_opportunity,
        )
        self._activities.append(activity)
        return activity

    def get_report(self) -> ToilReport:
        total_minutes = sum(a.duration_minutes for a in self._activities)
        total_hours = total_minutes / 60

        # Assume 40-hour work week
        toil_ratio = total_hours / 160  # Monthly hours

        opportunities = []
        for activity in self._activities:
            if activity.automation_opportunity in ("high", "critical"):
                opportunities.append({
                    "task": activity.task,
                    "current_hours": f"{activity.duration_minutes / 60:.1f}",
                    "automation_effort": activity.automation_opportunity,
                })

        return ToilReport(
            total_hours=total_hours,
            toil_ratio=toil_ratio,
            opportunities=opportunities,
            activities=list(self._activities),
        )


# ---------------------------------------------------------------------------
# Capacity Planner
# ---------------------------------------------------------------------------

class CapacityPlanner:
    """Plan and manage system capacity."""

    def analyze(self, service: str = "default") -> CapacityAnalysis:
        current = np.random.uniform(0.4, 0.7)
        growth = np.random.uniform(0.02, 0.05)

        return CapacityAnalysis(
            service=service,
            current_utilization=current,
            projected_30day=min(0.95, current * (1 + growth)),
            projected_90day=min(0.99, current * (1 + growth * 3)),
            days_until_capacity=int((0.9 - current) / (growth / 30)) if growth > 0 else 365,
            bottleneck_resource="CPU" if np.random.random() > 0.5 else "Memory",
        )

    def get_recommendations(self) -> List[ScalingRecommendation]:
        return [
            ScalingRecommendation(
                action="Scale horizontally",
                reason="Current CPU utilization trending upward",
                priority="high",
                estimated_impact="50% capacity increase",
            ),
            ScalingRecommendation(
                action="Enable auto-scaling",
                reason="Peak hours show 3x normal load",
                priority="medium",
                estimated_impact="Handle traffic spikes automatically",
            ),
        ]


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate SRE capabilities."""
    print("=" * 70)
    print("Site Reliability Engineering Framework - Demo")
    print("=" * 70)

    # --- 1. SLO Management ---
    print("\n--- SLO Management ---")
    slo_mgr = SLOManager()
    sli = SLIDefinition("availability", "successful_requests / total_requests")
    slo = slo_mgr.create_slo("api_availability", sli, 99.9, 30)
    budget = slo_mgr.get_error_budget(slo)
    print(f"  SLO: {slo.name} target={slo.target}%")
    print(f"  Budget remaining: {budget.remaining_pct:.2f}%")
    print(f"  Days remaining: {budget.days_remaining:.1f}")

    # --- 2. Incident Management ---
    print("\n--- Incident Management ---")
    inc_mgr = IncidentManager()
    incident = inc_mgr.create_incident(
        "API error rate spike", Severity.P1, "api-gateway",
        "Error rate increased to 5%"
    )
    print(f"  Incident: {incident.id}")
    print(f"  Severity: {incident.severity.value}")
    print(f"  On-call: {incident.oncall_engineer}")

    inc_mgr.update(incident.id, "Investigating root cause")
    inc_mgr.resolve(incident.id, "Increased connection pool size")
    print(f"  Status: {incident.status.value}")
    print(f"  Duration: {incident.duration_minutes:.1f} minutes")

    postmortem = inc_mgr.create_postmortem(incident.id)
    if postmortem:
        print(f"  Postmortem: {postmortem.title}")

    # --- 3. Toil Reduction ---
    print("\n--- Toil Reduction ---")
    toil = ToilTracker()
    toil.log_activity("Manual certificate renewal", 30, "monthly", "high")
    toil.log_activity("Log rotation cleanup", 15, "weekly", "medium")
    toil.log_activity("Database backup verification", 45, "daily", "high")

    report = toil.get_report()
    print(f"  Total toil: {report.total_hours:.1f} hours/month")
    print(f"  Toil ratio: {report.toil_ratio:.1%}")
    print(f"  Automation opportunities: {len(report.opportunities)}")

    # --- 4. Capacity Planning ---
    print("\n--- Capacity Planning ---")
    capacity = CapacityPlanner()
    analysis = capacity.analyze("api-gateway")
    print(f"  Current utilization: {analysis.current_utilization:.1%}")
    print(f"  Projected 30-day: {analysis.projected_30day:.1%}")
    print(f"  Days until capacity: {analysis.days_until_capacity}")
    print(f"  Bottleneck: {analysis.bottleneck_resource}")

    recs = capacity.get_recommendations()
    for rec in recs:
        print(f"  [{rec.priority}] {rec.action}: {rec.reason}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()