"""
Incident Response Module
Incident lifecycle, containment, evidence collection, recovery, and reporting.
"""

from __future__ import annotations

import hashlib
import logging
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class IncidentSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class IncidentPhase(Enum):
    DETECTION = "detection"
    ANALYSIS = "analysis"
    CONTAINMENT = "containment"
    ERADICATION = "eradication"
    RECOVERY = "recovery"
    LESSONS_LEARNED = "lessons_learned"


class IncidentCategory(Enum):
    RANSOMWARE = "ransomware"
    MALWARE = "malware"
    PHISHING = "phishing"
    DATA_BREACH = "data_breach"
    DDOS = "ddos"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    INSIDER_THREAT = "insider_threat"
    UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class Incident:
    """Security incident."""
    incident_id: str
    title: str
    severity: IncidentSeverity
    category: IncidentCategory
    current_phase: IncidentPhase = IncidentPhase.DETECTION
    affected_systems: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    assigned_to: str = ""
    timeline: List[Dict[str, str]] = field(default_factory=list)
    resolution: str = ""

    @property
    def age_hours(self) -> float:
        return (datetime.now(timezone.utc) - self.created_at).total_seconds() / 3600


@dataclass
class ContainmentStep:
    """Containment plan step."""
    step_id: int
    action: str
    description: str
    priority: str = "high"
    status: str = "pending"
    assigned_to: str = ""


@dataclass
class ContainmentPlan:
    """Containment plan."""
    incident_id: str
    steps: List[ContainmentStep] = field(default_factory=list)
    short_term: List[str] = field(default_factory=list)
    long_term: List[str] = field(default_factory=list)


@dataclass
class EvidenceItem:
    """Collected evidence."""
    evidence_id: str
    evidence_type: str
    source_system: str
    sha256: str
    collected_by: str = ""
    collected_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    description: str = ""
    chain_of_custody: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class RecoveryStep:
    """Recovery plan step."""
    step_id: int
    action: str
    description: str
    estimated_hours: float = 1.0
    status: str = "pending"
    dependencies: List[int] = field(default_factory=list)


@dataclass
class RecoveryPlan:
    """Recovery plan."""
    incident_id: str
    steps: List[RecoveryStep] = field(default_factory=list)
    estimated_total_hours: float = 0.0


@dataclass
class IRReport:
    """Incident response report."""
    title: str
    incident_id: str
    executive_summary: str
    timeline: List[Dict[str, str]] = field(default_factory=list)
    findings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    root_cause: str = ""
    lessons_learned: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Incident Manager
# ---------------------------------------------------------------------------

class IncidentManager:
    """Manage incident lifecycle."""

    def __init__(self):
        self._incidents: Dict[str, Incident] = {}

    def create_incident(
        self,
        title: str,
        severity: str,
        category: str = "unknown",
        affected_systems: Optional[List[str]] = None,
    ) -> Incident:
        incident = Incident(
            incident_id=f"INC-{secrets.token_hex(4).upper()}",
            title=title,
            severity=IncidentSeverity(severity),
            category=IncidentCategory(category),
            affected_systems=affected_systems or [],
        )
        incident.timeline.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": "incident_created",
            "details": title,
        })
        self._incidents[incident.incident_id] = incident
        return incident

    def transition_phase(self, incident_id: str, phase: str) -> Optional[Incident]:
        incident = self._incidents.get(incident_id)
        if incident:
            incident.current_phase = IncidentPhase(phase)
            incident.timeline.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "action": "phase_transition",
                "details": phase,
            })
        return incident

    def get_incident(self, incident_id: str) -> Optional[Incident]:
        return self._incidents.get(incident_id)

    def get_timeline(self, incident_id: str) -> List[Dict[str, str]]:
        incident = self._incidents.get(incident_id)
        return incident.timeline if incident else []

    def get_open_incidents(self) -> List[Incident]:
        return [
            i for i in self._incidents.values()
            if i.current_phase != IncidentPhase.LESSONS_LEARNED
        ]


# ---------------------------------------------------------------------------
# Containment Planner
# ---------------------------------------------------------------------------

class ContainmentPlanner:
    """Plan containment actions."""

    def create_plan(
        self,
        incident_id: str,
        short_term: Optional[List[str]] = None,
        long_term: Optional[List[str]] = None,
    ) -> ContainmentPlan:
        steps: List[ContainmentStep] = []
        for i, action in enumerate(short_term or [], 1):
            steps.append(ContainmentStep(
                step_id=i, action=action,
                description=f"Short-term: {action}",
                priority="critical",
            ))
        for i, action in enumerate(long_term or [], len(steps) + 1):
            steps.append(ContainmentStep(
                step_id=i, action=action,
                description=f"Long-term: {action}",
                priority="high",
            ))
        return ContainmentPlan(
            incident_id=incident_id,
            steps=steps,
            short_term=short_term or [],
            long_term=long_term or [],
        )


# ---------------------------------------------------------------------------
# Evidence Collector
# ---------------------------------------------------------------------------

class EvidenceCollector:
    """Collect forensic evidence."""

    def collect(
        self,
        system: str,
        evidence_types: Optional[List[str]] = None,
        collector: str = "ir_team",
    ) -> List[EvidenceItem]:
        items: List[EvidenceItem] = []
        for ev_type in (evidence_types or ["memory_dump"]):
            content = f"{system}:{ev_type}:{datetime.now(timezone.utc).isoformat()}"
            sha = hashlib.sha256(content.encode()).hexdigest()
            items.append(EvidenceItem(
                evidence_id=f"EVD-{secrets.token_hex(4).upper()}",
                evidence_type=ev_type,
                source_system=system,
                sha256=sha,
                collected_by=collector,
                description=f"{ev_type} from {system}",
            ))
        return items


# ---------------------------------------------------------------------------
# Recovery Manager
# ---------------------------------------------------------------------------

class RecoveryManager:
    """Plan system recovery."""

    def create_plan(
        self,
        incident_id: str,
        steps: Optional[List[str]] = None,
    ) -> RecoveryPlan:
        recovery_steps: List[RecoveryStep] = []
        for i, action in enumerate(steps or ["restore_backup"], 1):
            recovery_steps.append(RecoveryStep(
                step_id=i,
                action=action,
                description=f"Recovery step: {action}",
                estimated_hours=2.0,
            ))
        total_hours = sum(s.estimated_hours for s in recovery_steps)
        return RecoveryPlan(
            incident_id=incident_id,
            steps=recovery_steps,
            estimated_total_hours=total_hours,
        )


# ---------------------------------------------------------------------------
# IR Report Generator
# ---------------------------------------------------------------------------

class IRReportGenerator:
    """Generate incident response reports."""

    def generate(
        self,
        incident: Optional[Incident] = None,
        timeline: Optional[List[Dict[str, str]]] = None,
        findings: Optional[List[str]] = None,
    ) -> IRReport:
        inc = incident or Incident("default", "Unknown", IncidentSeverity.LOW, IncidentCategory.UNKNOWN)
        return IRReport(
            title=f"Incident Report - {inc.incident_id}",
            incident_id=inc.incident_id,
            executive_summary=f"{inc.title} incident with {len(inc.affected_systems)} systems affected",
            timeline=timeline or inc.timeline,
            findings=findings or [],
            recommendations=[
                "Update detection rules to prevent recurrence",
                "Conduct security awareness training",
                "Implement additional monitoring on affected systems",
            ],
            root_cause="Under investigation",
            lessons_learned=[
                "Early detection reduced impact",
                "Playbook needs update for this attack type",
            ],
        )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Incident Response Demo")
    print("=" * 60)

    print("\n[1] Create Incident")
    manager = IncidentManager()
    incident = manager.create_incident(
        "Ransomware on finance workstation",
        "critical", "ransomware",
        ["FIN-WS-001", "FIN-SRV-001"],
    )
    print(f"  ID: {incident.incident_id}")
    print(f"  Severity: {incident.severity.value}")
    print(f"  Phase: {incident.current_phase.value}")

    print("\n[2] Containment Plan")
    containment = ContainmentPlanner()
    plan = containment.create_plan(
        incident.incident_id,
        short_term=["isolate_network", "disable_accounts"],
        long_term=["patch_vuln", "reset_creds"],
    )
    print(f"  Steps: {len(plan.steps)}")

    print("\n[3] Evidence Collection")
    evidence = EvidenceCollector()
    items = evidence.collect("FIN-WS-001", ["memory_dump", "disk_image"])
    for item in items:
        print(f"  {item.evidence_type}: {item.sha256[:16]}...")

    print("\n[4] Recovery Plan")
    recovery = RecoveryManager()
    rplan = recovery.create_plan(incident.incident_id, ["restore_backup", "validate", "monitor"])
    print(f"  Steps: {len(rplan.steps)}")
    print(f"  Est. hours: {rplan.estimated_total_hours}")

    print("\n[5] Phase Transition")
    manager.transition_phase(incident.incident_id, "containment")
    print(f"  Phase: {incident.current_phase.value}")
    print(f"  Timeline entries: {len(incident.timeline)}")

    print("\n[6] IR Report")
    reporter = IRReportGenerator()
    report = reporter.generate(incident, findings=["Malware contained", "Backups verified"])
    print(f"  Title: {report.title}")
    print(f"  Findings: {report.findings}")
    print(f"  Recommendations: {len(report.recommendations)}")

    print("\n" + "=" * 60)
    print("  Incident response demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
