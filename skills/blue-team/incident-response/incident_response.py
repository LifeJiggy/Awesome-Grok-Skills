"""
Incident Response Module
Incident lifecycle management, containment, evidence collection, chain of custody, and recovery.
"""

from __future__ import annotations

import hashlib
import logging
import secrets
from collections import defaultdict
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
    CONTAINMENT = "containment"
    ERADICATION = "eradication"
    RECOVERY = "recovery"
    POST_INCIDENT = "post_incident"


class IncidentCategory(Enum):
    MALWARE = "malware"
    PHISHING = "phishing"
    DATA_BREACH = "data_breach"
    RANSOMWARE = "ransomware"
    INSIDER_THREAT = "insider_threat"
    DDOS = "ddos"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    UNKNOWN = "unknown"


class ContainmentAction(Enum):
    ISOLATE_NETWORK = "isolate_network"
    DISABLE_ACCOUNT = "disable_account"
    BLOCK_IOC = "block_iocs"
    QUARANTINE_ENDPOINT = "quarantine_endpoint"
    DNS_SINKHOLE = "dns_sinkhole"
    SHUTDOWN_SYSTEM = "shutdown_system"


class ContainmentStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


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
    initial_indicators: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    assigned_to: str = ""
    iocs: List[Dict[str, str]] = field(default_factory=list)
    timeline: List[Dict[str, str]] = field(default_factory=list)
    resolution: str = ""

    @property
    def age_hours(self) -> float:
        return (datetime.now(timezone.utc) - self.created_at).total_seconds() / 3600

    def add_timeline_entry(self, action: str, actor: str, details: str = "") -> None:
        self.timeline.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "actor": actor,
            "details": details,
        })
        self.updated_at = datetime.now(timezone.utc)


@dataclass
class ContainmentActionRecord:
    """Record of a containment action."""
    action_id: str
    action: ContainmentAction
    target: str
    status: ContainmentStatus = ContainmentStatus.PENDING
    executed_by: str = ""
    executed_at: Optional[datetime] = None
    notes: str = ""


@dataclass
class EvidenceItem:
    """Collected evidence item."""
    evidence_id: str
    item_type: str
    source_system: str
    sha256: str
    file_size: int = 0
    collected_by: str = ""
    collected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    description: str = ""
    volatile: bool = False


@dataclass
class CustodyEntry:
    """Chain of custody entry."""
    evidence_id: str
    from_person: str
    to_person: str
    action: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    reason: str = ""
    hash_verified: bool = True


@dataclass
class RecoveryStep:
    """Recovery plan step."""
    step_id: int
    description: str
    status: str = "pending"
    assigned_to: str = ""
    estimated_hours: float = 1.0
    dependencies: List[int] = field(default_factory=list)


@dataclass
class RecoveryPlan:
    """Incident recovery plan."""
    incident_id: str
    steps: List[RecoveryStep] = field(default_factory=list)
    estimated_hours: float = 0.0
    approved_by: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class NotificationRecord:
    """Communication notification record."""
    notification_id: str
    recipients: List[str]
    subject: str
    message: str
    classification: str = "internal"
    sent_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    sent_by: str = ""


@dataclass
class PostIncidentReport:
    """Post-incident report."""
    incident_id: str
    sections: List[Dict[str, str]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    root_cause: str = ""
    lessons_learned: List[str] = field(default_factory=list)
    control_gaps: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# Incident Manager
# ---------------------------------------------------------------------------

class IncidentManager:
    """Manage security incident lifecycle."""

    def __init__(self):
        self._incidents: Dict[str, Incident] = {}

    def create_incident(
        self,
        title: str,
        severity: str,
        category: str = "unknown",
        affected_systems: Optional[List[str]] = None,
        initial_indicators: Optional[List[str]] = None,
    ) -> Incident:
        incident = Incident(
            incident_id=f"INC-{secrets.token_hex(4).upper()}",
            title=title,
            severity=IncidentSeverity(severity),
            category=IncidentCategory(category),
            affected_systems=affected_systems or [],
            initial_indicators=initial_indicators or [],
        )
        incident.add_timeline_entry("incident_created", "system", title)
        self._incidents[incident.incident_id] = incident
        return incident

    def transition_phase(self, incident_id: str, phase: IncidentPhase) -> Optional[Incident]:
        incident = self._incidents.get(incident_id)
        if incident:
            old_phase = incident.current_phase
            incident.current_phase = phase
            incident.add_timeline_entry(
                "phase_transition", "system",
                f"{old_phase.value} -> {phase.value}",
            )
        return incident

    def add_ioc(self, incident_id: str, ioc_type: str, value: str) -> None:
        incident = self._incidents.get(incident_id)
        if incident:
            incident.iocs.append({"type": ioc_type, "value": value})

    def get_incident(self, incident_id: str) -> Optional[Incident]:
        return self._incidents.get(incident_id)

    def get_open_incidents(self) -> List[Incident]:
        return [
            i for i in self._incidents.values()
            if i.current_phase != IncidentPhase.POST_INCIDENT
        ]

    def generate_post_incident_report(self, incident_id: str) -> PostIncidentReport:
        incident = self._incidents.get(incident_id)
        if not incident:
            return PostIncidentReport(incident_id=incident_id)
        report = PostIncidentReport(incident_id=incident_id)
        report.sections = [
            {"title": "Executive Summary", "content": f"Incident: {incident.title}"},
            {"title": "Timeline", "content": f"{len(incident.timeline)} events recorded"},
            {"title": "Impact", "content": f"{len(incident.affected_systems)} systems affected"},
            {"title": "Response Actions", "content": f"{len(incident.timeline)} actions taken"},
            {"title": "Root Cause", "content": "Under investigation"},
            {"title": "Lessons Learned", "content": "To be determined in post-incident review"},
        ]
        report.recommendations = [
            "Review detection rules for this attack vector",
            "Update incident response playbook",
            "Conduct security awareness training",
            "Implement additional monitoring on affected systems",
        ]
        return report


# ---------------------------------------------------------------------------
# Containment Engine
# ---------------------------------------------------------------------------

class ContainmentEngine:
    """Execute containment actions."""

    def __init__(self):
        self._actions: List[ContainmentActionRecord] = []

    def execute_containment(
        self,
        incident_id: str,
        systems: List[str],
        actions: List[str],
    ) -> List[ContainmentActionRecord]:
        results: List[ContainmentActionRecord] = []
        for system in systems:
            for action_name in actions:
                try:
                    action_enum = ContainmentAction(action_name)
                except ValueError:
                    action_enum = ContainmentAction.BLOCK_IOC
                record = ContainmentActionRecord(
                    action_id=f"CONT-{secrets.token_hex(4).upper()}",
                    action=action_enum,
                    target=system,
                    status=ContainmentStatus.COMPLETED,
                    executed_at=datetime.now(timezone.utc),
                )
                self._actions.append(record)
                results.append(record)
        return results

    def get_actions_for_incident(self, incident_id: str) -> List[ContainmentActionRecord]:
        return self._actions


# ---------------------------------------------------------------------------
# Evidence Collector
# ---------------------------------------------------------------------------

class EvidenceCollector:
    """Collect forensic evidence."""

    def collect_volatile_data(
        self,
        system: str,
        items: Optional[List[str]] = None,
        collector: str = "system",
    ) -> List[EvidenceItem]:
        items = items or ["memory_dump", "running_processes"]
        evidence: List[EvidenceItem] = []
        for item_type in items:
            content = f"{system}:{item_type}:{datetime.now(timezone.utc).isoformat()}"
            sha = hashlib.sha256(content.encode()).hexdigest()
            ev = EvidenceItem(
                evidence_id=f"EVD-{secrets.token_hex(4).upper()}",
                item_type=item_type,
                source_system=system,
                sha256=sha,
                file_size=len(content),
                collected_by=collector,
                volatile=True,
                description=f"Volatile data: {item_type} from {system}",
            )
            evidence.append(ev)
        return evidence

    def collect_disk_image(
        self,
        system: str,
        target_partition: str = "/dev/sda1",
        collector: str = "system",
    ) -> EvidenceItem:
        content = f"{system}:{target_partition}:disk_image"
        sha = hashlib.sha256(content.encode()).hexdigest()
        return EvidenceItem(
            evidence_id=f"EVD-{secrets.token_hex(4).upper()}",
            item_type="disk_image",
            source_system=system,
            sha256=sha,
            file_size=500_000_000_000,
            collected_by=collector,
            description=f"Disk image of {target_partition} from {system}",
        )

    def collect_logs(
        self,
        system: str,
        log_paths: List[str],
        collector: str = "system",
    ) -> List[EvidenceItem]:
        evidence: List[EvidenceItem] = []
        for path in log_paths:
            content = f"{system}:{path}"
            sha = hashlib.sha256(content.encode()).hexdigest()
            evidence.append(EvidenceItem(
                evidence_id=f"EVD-{secrets.token_hex(4).upper()}",
                item_type="log_file",
                source_system=system,
                sha256=sha,
                collected_by=collector,
                description=f"Log file: {path}",
            ))
        return evidence


# ---------------------------------------------------------------------------
# Chain of Custody
# ---------------------------------------------------------------------------

class ChainOfCustody:
    """Manage evidence chain of custody."""

    def __init__(self):
        self._entries: Dict[str, List[CustodyEntry]] = defaultdict(list)
        self._evidence_info: Dict[str, Dict[str, str]] = {}

    def register_evidence(
        self,
        evidence_id: str,
        collector: str,
        description: str,
    ) -> None:
        self._evidence_info[evidence_id] = {
            "collector": collector,
            "description": description,
            "registered_at": datetime.now(timezone.utc).isoformat(),
        }
        self._entries[evidence_id].append(CustodyEntry(
            evidence_id=evidence_id,
            from_person="system",
            to_person=collector,
            action="collected",
            reason="Initial collection",
        ))

    def transfer(
        self,
        evidence_id: str,
        from_person: str,
        to_person: str,
        reason: str = "",
    ) -> CustodyEntry:
        entry = CustodyEntry(
            evidence_id=evidence_id,
            from_person=from_person,
            to_person=to_person,
            action="transferred",
            reason=reason,
        )
        self._entries[evidence_id].append(entry)
        return entry

    def get_custody_chain(self, evidence_id: str) -> List[CustodyEntry]:
        return self._entries.get(evidence_id, [])

    def verify_integrity(self, evidence_id: str, current_hash: str, original_hash: str) -> bool:
        return current_hash == original_hash


# ---------------------------------------------------------------------------
# Recovery Manager
# ---------------------------------------------------------------------------

class RecoveryManager:
    """Manage incident recovery."""

    def create_recovery_plan(
        self,
        incident_id: str,
        systems: List[str],
        steps: Optional[List[str]] = None,
    ) -> RecoveryPlan:
        steps = steps or ["restore_from_backup", "validate_integrity"]
        plan = RecoveryPlan(incident_id=incident_id)
        for i, step_desc in enumerate(steps, 1):
            plan.steps.append(RecoveryStep(
                step_id=i,
                description=f"{step_desc} for {', '.join(systems)}",
                estimated_hours=2.0,
            ))
        plan.estimated_hours = sum(s.estimated_hours for s in plan.steps)
        return plan

    def execute_step(
        self, plan: RecoveryPlan, step_id: int
    ) -> Optional[RecoveryStep]:
        for step in plan.steps:
            if step.step_id == step_id:
                step.status = "completed"
                return step
        return None


# ---------------------------------------------------------------------------
# Communication Manager
# ---------------------------------------------------------------------------

class CommunicationManager:
    """Manage incident communications."""

    def __init__(self):
        self._notifications: List[NotificationRecord] = []

    def send_notification(
        self,
        recipients: List[str],
        subject: str,
        message: str,
        classification: str = "internal",
        sender: str = "ir-team",
    ) -> NotificationRecord:
        record = NotificationRecord(
            notification_id=f"NOTIF-{secrets.token_hex(4).upper()}",
            recipients=recipients,
            subject=subject,
            message=message,
            classification=classification,
            sent_by=sender,
        )
        self._notifications.append(record)
        return record

    def generate_executive_briefing(self, incident: Incident) -> str:
        return (
            f"EXECUTIVE BRIEFING\n"
            f"Incident: {incident.incident_id}\n"
            f"Title: {incident.title}\n"
            f"Severity: {incident.severity.value}\n"
            f"Phase: {incident.current_phase.value}\n"
            f"Systems affected: {len(incident.affected_systems)}\n"
            f"Actions taken: {len(incident.timeline)}\n"
        )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Incident Response Demo")
    print("=" * 60)

    manager = IncidentManager()
    incident = manager.create_incident(
        title="Ransomware on finance workstation",
        severity="critical",
        category="ransomware",
        affected_systems=["FIN-WS-001", "FIN-SRV-001"],
    )
    print(f"\nIncident: {incident.incident_id}")
    print(f"Severity: {incident.severity.value}")

    print("\n[1] Containment")
    containment = ContainmentEngine()
    actions = containment.execute_containment(
        incident.incident_id, ["FIN-WS-001"], ["isolate_network", "disable_account"]
    )
    print(f"  Actions: {len(actions)}")

    print("\n[2] Evidence Collection")
    collector = EvidenceCollector()
    evidence = collector.collect_volatile_data("FIN-WS-001", ["memory_dump", "network_connections"])
    print(f"  Items: {len(evidence)}")
    print(f"  Hash: {evidence[0].sha256[:32]}...")

    print("\n[3] Chain of Custody")
    coc = ChainOfCustody()
    coc.register_evidence(evidence[0].evidence_id, "analyst1", "Memory dump")
    coc.transfer(evidence[0].evidence_id, "analyst1", "forensics_team", "Deep analysis")
    chain = coc.get_custody_chain(evidence[0].evidence_id)
    print(f"  Custody entries: {len(chain)}")

    print("\n[4] Recovery")
    recovery = RecoveryManager()
    plan = recovery.create_recovery_plan(incident.incident_id, ["FIN-WS-001"], ["restore_backup", "patch", "reset_creds"])
    print(f"  Steps: {len(plan.steps)}")
    print(f"  Est. hours: {plan.estimated_hours}")

    print("\n[5] Communication")
    comms = CommunicationManager()
    comms.send_notification(["ciso@co.com"], f"Incident {incident.incident_id}", "Ransomware detected")
    briefing = comms.generate_executive_briefing(incident)
    print(f"  Briefing:\n{briefing}")

    print("\n[6] Post-Incident Report")
    report = manager.generate_post_incident_report(incident.incident_id)
    print(f"  Sections: {len(report.sections)}")
    print(f"  Recommendations: {len(report.recommendations)}")

    print("\n" + "=" * 60)
    print("  Incident response demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
