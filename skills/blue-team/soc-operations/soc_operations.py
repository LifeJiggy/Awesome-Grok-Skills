"""
SOC Operations Module
Triage workflows, escalation management, playbooks, shift handover, and KPI tracking.
"""

from __future__ import annotations

import logging
import secrets
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Priority(Enum):
    P1 = "P1_critical"
    P2 = "P2_high"
    P3 = "P3_medium"
    P4 = "P4_low"
    P5 = "P5_informational"


class TicketStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING = "waiting_on_third_party"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TriageAction(Enum):
    BLOCK_IP = "block_ip"
    INVESTIGATE = "investigate"
    ESCALATE = "escalate"
    DISMISS = "dismiss"
    AUTO_ENRICH = "auto_enrich"
    ESCALATE_T3 = "escalate_tier3"


class ShiftType(Enum):
    DAY = "day"
    EVENING = "evening"
    NIGHT = "night"
    ON_CALL = "on_call"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class TriageDecision:
    """Triage decision result."""
    action: TriageAction
    playbook: str
    escalate: bool
    priority: Priority
    reason: str
    auto_contain: bool = False
    estimated_time_minutes: int = 30


@dataclass
class SecurityTicket:
    """Security incident ticket."""
    ticket_id: str
    title: str
    severity: Priority
    status: TicketStatus
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    assigned_to: str = ""
    alert_ids: List[str] = field(default_factory=list)
    notes: List[Dict[str, str]] = field(default_factory=list)
    resolution: str = ""
    sla_deadline: Optional[datetime] = None
    resolved_at: Optional[datetime] = None

    @property
    def age_hours(self) -> float:
        return (datetime.now(timezone.utc) - self.created_at).total_seconds() / 3600

    @property
    def sla_breached(self) -> bool:
        if self.sla_deadline is None:
            return False
        return datetime.now(timezone.utc) > self.sla_deadline and self.status not in (TicketStatus.RESOLVED, TicketStatus.CLOSED)


@dataclass
class PlaybookStep:
    """Single step in a playbook."""
    step_id: int
    description: str
    action: str
    tool: str = ""
    evidence_type: str = ""
    estimated_time: int = 5
    completed: bool = False
    notes: str = ""


@dataclass
class PlaybookResult:
    """Playbook execution result."""
    playbook_name: str
    steps_completed: int
    total_steps: int
    evidence: List[Dict[str, str]] = field(default_factory=list)
    findings: List[str] = field(default_factory=list)
    duration_minutes: float = 0.0
    success: bool = True


@dataclass
class ShiftHandoverReport:
    """Shift handover report."""
    outgoing_shift: str
    incoming_shift: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    open_items: int = 0
    critical_alerts: int = 0
    ongoing_investigations: List[str] = field(default_factory=list)
    notable_events: List[str] = field(default_factory=list)
    equipment_issues: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class DetectionRecord:
    """Detection event record."""
    alert_id: str
    detect_time_seconds: float = 0.0
    respond_time_seconds: float = 0.0
    analyst: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    false_positive: bool = False
    mitre_technique: str = ""


@dataclass
class KPIMetrics:
    """SOC KPI metrics."""
    mttd_minutes: float = 0.0
    mttr_minutes: float = 0.0
    alerts_handled: int = 0
    false_positive_rate: float = 0.0
    sla_compliance: float = 0.0
    tickets_resolved: int = 0
    avg_triage_time: float = 0.0
    analyst_utilization: float = 0.0


# ---------------------------------------------------------------------------
# Triage Engine
# ---------------------------------------------------------------------------

class TriageEngine:
    """Automated alert triage with decision trees."""

    SEVERITY_MAP = {
        "critical": Priority.P1,
        "high": Priority.P2,
        "medium": Priority.P3,
        "low": Priority.P4,
        "informational": Priority.P5,
    }

    PLAYBOOK_MAP = {
        "ssh_brute_force": "brute_force_response",
        "malware_detected": "malware_containment",
        "phishing": "phishing_response",
        "data_exfiltration": "data_exfil_response",
        "privilege_escalation": "priv_esc_response",
        "lateral_movement": "lateral_movement_response",
    }

    HIGH_RISK_GEOS = {"RU", "CN", "KP", "IR", "SY"}

    def triage_alert(
        self,
        alert_type: str,
        severity: str,
        source_ip: str = "",
        context: Optional[Dict[str, Any]] = None,
    ) -> TriageDecision:
        context = context or {}
        priority = self.SEVERITY_MAP.get(severity, Priority.P3)
        action = TriageAction.INVESTIGATE
        escalate = False
        auto_contain = False
        reason = "Standard investigation"

        geo = context.get("geo", "")
        attempts = context.get("attempts", 0)

        if severity == "critical":
            action = TriageAction.ESCALATE
            escalate = True
            reason = "Critical alert requires immediate escalation"
        elif attempts > 50:
            action = TriageAction.BLOCK_IP
            auto_contain = True
            reason = f"High attempt count ({attempts}) - auto-blocking"
        elif geo in self.HIGH_RISK_GEOS:
            action = TriageAction.ESCALATE
            escalate = True
            reason = f"High-risk geography: {geo}"

        playbook = self.PLAYBOOK_MAP.get(alert_type, "generic_response")
        sla_minutes = {
            Priority.P1: 15, Priority.P2: 60,
            Priority.P3: 240, Priority.P4: 480, Priority.P5: 1440,
        }

        return TriageDecision(
            action=action,
            playbook=playbook,
            escalate=escalate,
            priority=priority,
            reason=reason,
            auto_contain=auto_contain,
            estimated_time_minutes=sla_minutes.get(priority, 240),
        )

    def classify_alert(self, message: str) -> str:
        lower = message.lower()
        if "brute" in lower or "failed password" in lower:
            return "ssh_brute_force"
        elif "malware" in lower or "trojan" in lower:
            return "malware_detected"
        elif "phish" in lower:
            return "phishing"
        elif "exfil" in lower or "data transfer" in lower:
            return "data_exfiltration"
        return "generic"


# ---------------------------------------------------------------------------
# Escalation Manager
# ---------------------------------------------------------------------------

class EscalationManager:
    """Manage ticket creation and escalation."""

    SLA_HOURS = {
        Priority.P1: 4,
        Priority.P2: 8,
        Priority.P3: 24,
        Priority.P4: 72,
        Priority.P5: 168,
    }

    def __init__(self):
        self._tickets: Dict[str, SecurityTicket] = {}
        self._escalation_hooks: List[Callable[[SecurityTicket], None]] = []

    def create_ticket(
        self,
        title: str,
        severity: str,
        analyst: str = "",
        alert_ids: Optional[List[str]] = None,
    ) -> SecurityTicket:
        priority = TriageEngine.SEVERITY_MAP.get(severity, Priority.P3)
        sla_hours = self.SLA_HOURS.get(priority, 24)
        ticket = SecurityTicket(
            ticket_id=f"TKT-{secrets.token_hex(4).upper()}",
            title=title,
            severity=priority,
            status=TicketStatus.OPEN,
            assigned_to=analyst,
            alert_ids=alert_ids or [],
            sla_deadline=datetime.now(timezone.utc) + timedelta(hours=sla_hours),
        )
        self._tickets[ticket.ticket_id] = ticket
        return ticket

    def assign(self, ticket_id: str, analyst: str) -> Optional[SecurityTicket]:
        ticket = self._tickets.get(ticket_id)
        if ticket:
            ticket.assigned_to = analyst
            ticket.status = TicketStatus.IN_PROGRESS
        return ticket

    def escalate_ticket(self, ticket_id: str, reason: str = "") -> Optional[SecurityTicket]:
        ticket = self._tickets.get(ticket_id)
        if ticket:
            ticket.status = TicketStatus.ESCALATED
            ticket.notes.append({
                "action": "escalated",
                "reason": reason,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            for hook in self._escalation_hooks:
                hook(ticket)
        return ticket

    def add_escalation_hook(self, hook: Callable[[SecurityTicket], None]) -> None:
        self._escalation_hooks.append(hook)

    def get_breached_tickets(self) -> List[SecurityTicket]:
        return [t for t in self._tickets.values() if t.sla_breached]

    def get_tickets(
        self, status: Optional[TicketStatus] = None, analyst: str = ""
    ) -> List[SecurityTicket]:
        tickets = list(self._tickets.values())
        if status:
            tickets = [t for t in tickets if t.status == status]
        if analyst:
            tickets = [t for t in tickets if t.assigned_to == analyst]
        return tickets


# ---------------------------------------------------------------------------
# Playbook Runner
# ---------------------------------------------------------------------------

class PlaybookRunner:
    """Execute incident response playbooks."""

    DEFAULT_PLAYBOOKS = {
        "brute_force_response": [
            PlaybookStep(1, "Verify alert is not false positive", "check_logs"),
            PlaybookStep(2, "Identify source IP and geolocation", "geoip_lookup"),
            PlaybookStep(3, "Check for successful logins from source", "log_analysis"),
            PlaybookStep(4, "Block source IP at firewall", "firewall_block"),
            PlaybookStep(5, "Check for lateral movement", "network_analysis"),
            PlaybookStep(6, "Notify account owner", "notification"),
            PlaybookStep(7, "Document findings and close", "documentation"),
        ],
        "malware_containment": [
            PlaybookStep(1, "Isolate affected endpoint", "endpoint_isolation"),
            PlaybookStep(2, "Collect malware sample", "sample_collection"),
            PlaybookStep(3, "Run full AV scan", "av_scan"),
            PlaybookStep(4, "Check for C2 communication", "network_analysis"),
            PlaybookStep(5, "Block IOCs across network", "ioc_blocking"),
            PlaybookStep(6, "Restore from clean backup", "backup_restore"),
        ],
    }

    def __init__(self):
        self._playbooks = dict(self.DEFAULT_PLAYBOOKS)

    def load_playbook(self, name: str) -> List[PlaybookStep]:
        return list(self._playbooks.get(name, []))

    def execute(
        self,
        steps: List[PlaybookStep],
        context: Optional[Dict[str, Any]] = None,
    ) -> PlaybookResult:
        completed = 0
        evidence: List[Dict[str, str]] = []
        findings: List[str] = []

        for step in steps:
            step.completed = True
            completed += 1
            evidence.append({
                "step": str(step.step_id),
                "action": step.action,
                "result": "completed",
            })
            findings.append(f"Step {step.step_id}: {step.description} - OK")

        return PlaybookResult(
            playbook_name="executed",
            steps_completed=completed,
            total_steps=len(steps),
            evidence=evidence,
            findings=findings,
            duration_minutes=len(steps) * 5,
            success=True,
        )

    def register_playbook(self, name: str, steps: List[PlaybookStep]) -> None:
        self._playbooks[name] = steps


# ---------------------------------------------------------------------------
# Shift Handover
# ---------------------------------------------------------------------------

class ShiftHandover:
    """Generate shift handover reports."""

    def generate(
        self,
        outgoing_shift: str,
        incoming_shift: str,
        open_tickets: Optional[List[SecurityTicket]] = None,
        ongoing_investigations: Optional[List[str]] = None,
        notable_events: Optional[List[str]] = None,
    ) -> ShiftHandoverReport:
        open_tickets = open_tickets or []
        critical = sum(1 for t in open_tickets if t.severity == Priority.P1)
        return ShiftHandoverReport(
            outgoing_shift=outgoing_shift,
            incoming_shift=incoming_shift,
            open_items=len(open_tickets),
            critical_alerts=critical,
            ongoing_investigations=ongoing_investigations or [],
            notable_events=notable_events or [],
        )


# ---------------------------------------------------------------------------
# KPI Tracker
# ---------------------------------------------------------------------------

class KPITracker:
    """Track SOC KPI metrics."""

    def __init__(self):
        self._records: List[DetectionRecord] = []

    def record_detection(
        self,
        alert_id: str,
        detect_time: float,
        respond_time: float,
        analyst: str = "",
        false_positive: bool = False,
    ) -> None:
        self._records.append(DetectionRecord(
            alert_id=alert_id,
            detect_time_seconds=detect_time,
            respond_time_seconds=respond_time,
            analyst=analyst,
            false_positive=false_positive,
        ))

    def get_metrics(self, period: str = "daily") -> KPIMetrics:
        if not self._records:
            return KPIMetrics()
        mttd = sum(r.detect_time_seconds for r in self._records) / len(self._records) / 60
        mttr = sum(r.respond_time_seconds for r in self._records) / len(self._records) / 60
        fp_rate = sum(1 for r in self._records if r.false_positive) / len(self._records)
        return KPIMetrics(
            mttd_minutes=round(mttd, 1),
            mttr_minutes=round(mttr, 1),
            alerts_handled=len(self._records),
            false_positive_rate=round(fp_rate, 3),
        )

    def analyst_performance(self) -> Dict[str, Dict[str, float]]:
        by_analyst: Dict[str, List[DetectionRecord]] = defaultdict(list)
        for r in self._records:
            by_analyst[r.analyst or "unknown"].append(r)
        perf: Dict[str, Dict[str, float]] = {}
        for analyst, records in by_analyst.items():
            perf[analyst] = {
                "alerts": len(records),
                "avg_detect_time": sum(r.detect_time_seconds for r in records) / max(len(records), 1) / 60,
                "fp_rate": sum(1 for r in records if r.false_positive) / max(len(records), 1),
            }
        return perf


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  SOC Operations Demo")
    print("=" * 60)

    print("\n[1] Alert Triage")
    triage = TriageEngine()
    decision = triage.triage_alert(
        alert_type="ssh_brute_force",
        severity="high",
        source_ip="192.168.1.100",
        context={"attempts": 15, "geo": "RU"},
    )
    print(f"  Action: {decision.action.value}")
    print(f"  Priority: {decision.priority.value}")
    print(f"  Playbook: {decision.playbook}")
    print(f"  Escalate: {decision.escalate}")

    print("\n[2] Ticket Management")
    esc_mgr = EscalationManager()
    ticket = esc_mgr.create_ticket(
        title="SSH Brute Force", severity="high", analyst="analyst1"
    )
    print(f"  Ticket: {ticket.ticket_id}")
    print(f"  SLA: {ticket.sla_deadline}")
    esc_mgr.escalate_ticket(ticket.ticket_id, "High risk geo")

    print("\n[3] Playbook Execution")
    runner = PlaybookRunner()
    steps = runner.load_playbook("brute_force_response")
    result = runner.execute(steps, {"source_ip": "192.168.1.100"})
    print(f"  Steps: {result.steps_completed}/{result.total_steps}")
    print(f"  Evidence: {len(result.evidence)} items")

    print("\n[4] Shift Handover")
    handover = ShiftHandover()
    report = handover.generate("day", "night", [ticket], ["APT tracking"])
    print(f"  Open items: {report.open_items}")
    print(f"  Critical: {report.critical_alerts}")

    print("\n[5] KPI Tracking")
    kpi = KPITracker()
    kpi.record_detection("a1", 120, 300, "analyst1")
    kpi.record_detection("a2", 60, 180, "analyst2", false_positive=True)
    metrics = kpi.get_metrics()
    print(f"  MTTD: {metrics.mttd_minutes} min")
    print(f"  MTTR: {metrics.mttr_minutes} min")
    print(f"  FP rate: {metrics.false_positive_rate:.1%}")

    print("\n" + "=" * 60)
    print("  SOC operations demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
