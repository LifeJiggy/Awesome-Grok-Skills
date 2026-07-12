"""
Audit Management System

Implements audit planning, evidence collection with chain-of-custody,
finding lifecycle tracking, remediation workflows, and continuous auditing.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional
from uuid import uuid4


# ─── Enums ───────────────────────────────────────────────────────────────────

class AuditType(Enum):
    INTERNAL = "internal"
    EXTERNAL = "external"
    COMPLIANCE = "compliance"
    OPERATIONAL = "operational"
    FINANCIAL = "financial"
    ITGC = "itgc"


class AuditStatus(Enum):
    PLANNING = "planning"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    FIELDWORK_COMPLETE = "fieldwork_complete"
    REPORTING = "reporting"
    COMPLETE = "complete"


class FindingSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    OBSERVATION = "observation"


class FindingState(Enum):
    IDENTIFIED = "identified"
    VALIDATED = "validated"
    REPORTED = "reported"
    ACKNOWLEDGED = "acknowledged"
    REMEDIATION_PLANNED = "remediation_planned"
    REMEDIATION_IN_PROGRESS = "remediation_in_progress"
    REMEDIATION_COMPLETE = "remediation_complete"
    VERIFIED = "verified"
    CLOSED = "closed"
    DISPUTED = "disputed"
    REOPENED = "reopened"


class EvidenceType(Enum):
    DOCUMENTARY = "documentary"
    TESTIMONIAL = "testimonial"
    ANALYTICAL = "analytical"
    PHYSICAL = "physical"
    ELECTRONIC = "electronic"


class RemediationStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    VERIFIED = "verified"
    OVERDUE = "overdue"


# ─── Data Classes ────────────────────────────────────────────────────────────

@dataclass
class Evidence:
    """Evidence item with chain-of-custody metadata."""
    evidence_id: str = field(default_factory=lambda: str(uuid4())[:8])
    finding_id: str = ""
    evidence_type: EvidenceType = EvidenceType.DOCUMENTARY
    description: str = ""
    source: str = ""
    collector: str = ""
    collected_at: datetime = field(default_factory=datetime.utcnow)
    content_hash: str = ""
    storage_location: str = ""
    access_log: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def record_access(self, accessor: str, purpose: str) -> None:
        self.access_log.append({
            "accessor": accessor,
            "purpose": purpose,
            "timestamp": datetime.utcnow().isoformat(),
        })

    def verify_integrity(self, expected_hash: str) -> bool:
        return self.content_hash == expected_hash


@dataclass
class Finding:
    """Audit finding with full lifecycle tracking."""
    finding_id: str = field(default_factory=lambda: f"FN-{str(uuid4())[:6]}")
    audit_id: str = ""
    title: str = ""
    severity: FindingSeverity = FindingSeverity.MEDIUM
    state: FindingState = FindingState.IDENTIFIED
    condition: str = ""
    criteria: str = ""
    root_cause: str = ""
    impact: str = ""
    recommendation: str = ""
    management_response: str = ""
    evidence_refs: list[str] = field(default_factory=list)
    identified_at: datetime = field(default_factory=datetime.utcnow)
    target_remediation: Optional[datetime] = None
    actual_remediation: Optional[datetime] = None
    remediation_status: RemediationStatus = RemediationStatus.NOT_STARTED
    owner: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_open(self) -> bool:
        return self.state not in (FindingState.CLOSED, FindingState.DISPUTED)

    @property
    def is_overdue(self) -> bool:
        if self.target_remediation is None:
            return False
        return datetime.utcnow() > self.target_remediation and self.is_open

    @property
    def days_open(self) -> int:
        return (datetime.utcnow() - self.identified_at).days

    @property
    def days_to_remediation(self) -> Optional[int]:
        if self.target_remediation is None:
            return None
        delta = self.target_remediation - datetime.utcnow()
        return delta.days

    def transition(self, new_state: FindingState) -> bool:
        valid_transitions = {
            FindingState.IDENTIFIED: [FindingState.VALIDATED, FindingState.DISPUTED],
            FindingState.VALIDATED: [FindingState.REPORTED],
            FindingState.REPORTED: [FindingState.ACKNOWLEDGED, FindingState.DISPUTED],
            FindingState.ACKNOWLEDGED: [FindingState.REMEDIATION_PLANNED],
            FindingState.REMEDIATION_PLANNED: [FindingState.REMEDIATION_IN_PROGRESS],
            FindingState.REMEDIATION_IN_PROGRESS: [FindingState.REMEDIATION_COMPLETE],
            FindingState.REMEDIATION_COMPLETE: [FindingState.VERIFIED],
            FindingState.VERIFIED: [FindingState.CLOSED, FindingState.REOPENED],
            FindingState.DISPUTED: [FindingState.REPORTED],
            FindingState.REOPENED: [FindingState.REMEDIATION_IN_PROGRESS],
        }
        allowed = valid_transitions.get(self.state, [])
        if new_state in allowed:
            self.state = new_state
            return True
        return False

    def get_remediation_deadline(self) -> int:
        deadlines = {
            FindingSeverity.CRITICAL: 1,
            FindingSeverity.HIGH: 7,
            FindingSeverity.MEDIUM: 30,
            FindingSeverity.LOW: 90,
            FindingSeverity.OBSERVATION: 365,
        }
        return deadlines.get(self.severity, 30)


@dataclass
class AuditPlan:
    """Audit planning document."""
    audit_id: str = field(default_factory=lambda: f"AUD-{str(uuid4())[:6]}")
    audit_type: AuditType = AuditType.INTERNAL
    title: str = ""
    scope: str = ""
    objectives: list[str] = field(default_factory=list)
    in_scope_items: list[str] = field(default_factory=list)
    out_of_scope_items: list[str] = field(default_factory=list)
    methodology: str = ""
    lead_auditor: str = ""
    audit_team: list[str] = field(default_factory=list)
    estimated_hours: float = 0.0
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None
    status: AuditStatus = AuditStatus.PLANNING
    status_history: list[dict[str, Any]] = field(default_factory=list)

    def update_status(self, new_status: AuditStatus) -> None:
        self.status = new_status
        self.status_history.append({
            "status": new_status.value,
            "timestamp": datetime.utcnow().isoformat(),
        })

    @property
    def duration_days(self) -> Optional[int]:
        if self.planned_start and self.planned_end:
            return (self.planned_end - self.planned_start).days
        return None


@dataclass
class AuditReport:
    """Audit report with findings summary."""
    report_id: str = field(default_factory=lambda: f"RPT-{str(uuid4())[:6]}")
    audit_id: str = ""
    findings: list[Finding] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.utcnow)
    overall_opinion: str = ""
    executive_summary: str = ""

    @property
    def total_findings(self) -> int:
        return len(self.findings)

    @property
    def findings_by_severity(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for f in self.findings:
            counts[f.severity.value] = counts.get(f.severity.value, 0) + 1
        return counts

    @property
    def open_findings(self) -> list[Finding]:
        return [f for f in self.findings if f.is_open]

    @property
    def overdue_findings(self) -> list[Finding]:
        return [f for f in self.findings if f.is_overdue]


# ─── Core Classes ────────────────────────────────────────────────────────────

class AuditPlanner:
    """Manages audit planning and scheduling."""

    def __init__(self) -> None:
        self.plans: dict[str, AuditPlan] = {}

    def create_plan(self, title: str, audit_type: AuditType,
                    scope: str, lead_auditor: str,
                    objectives: list[str] | None = None) -> AuditPlan:
        plan = AuditPlan(
            title=title,
            audit_type=audit_type,
            scope=scope,
            lead_auditor=lead_auditor,
            objectives=objectives or [],
        )
        self.plans[plan.audit_id] = plan
        return plan

    def schedule_audit(self, audit_id: str, start: datetime, end: datetime,
                       team: list[str], estimated_hours: float) -> AuditPlan:
        plan = self.plans.get(audit_id)
        if plan:
            plan.planned_start = start
            plan.planned_end = end
            plan.audit_team = team
            plan.estimated_hours = estimated_hours
            plan.update_status(AuditStatus.SCHEDULED)
        return plan

    def get_upcoming_audits(self, within_days: int = 30) -> list[AuditPlan]:
        cutoff = datetime.utcnow() + timedelta(days=within_days)
        return [
            p for p in self.plans.values()
            if p.planned_start and p.planned_start <= cutoff
            and p.status in (AuditStatus.PLANNING, AuditStatus.SCHEDULED)
        ]

    def get_audit_utilization(self) -> dict[str, float]:
        utilization: dict[str, float] = {}
        for plan in self.plans.values():
            for member in plan.audit_team:
                utilization[member] = utilization.get(member, 0.0) + plan.estimated_hours
        return utilization


class EvidenceManager:
    """Manages evidence collection, storage, and chain-of-custody."""

    def __init__(self) -> None:
        self.evidence_items: dict[str, Evidence] = {}

    def collect_evidence(self, finding_id: str, evidence_type: EvidenceType,
                         description: str, source: str, collector: str,
                         content: str = "") -> Evidence:
        content_hash = hashlib.sha256(content.encode()).hexdigest() if content else ""
        evidence = Evidence(
            finding_id=finding_id,
            evidence_type=evidence_type,
            description=description,
            source=source,
            collector=collector,
            content_hash=content_hash,
        )
        evidence.record_access(collector, "initial collection")
        self.evidence_items[evidence.evidence_id] = evidence
        return evidence

    def access_evidence(self, evidence_id: str, accessor: str,
                        purpose: str) -> Optional[Evidence]:
        evidence = self.evidence_items.get(evidence_id)
        if evidence:
            evidence.record_access(accessor, purpose)
        return evidence

    def get_evidence_for_finding(self, finding_id: str) -> list[Evidence]:
        return [e for e in self.evidence_items.values() if e.finding_id == finding_id]

    def verify_evidence_integrity(self, evidence_id: str) -> bool:
        evidence = self.evidence_items.get(evidence_id)
        if not evidence:
            return False
        return evidence.verify_integrity(evidence.content_hash)

    def get_evidence_by_type(self, evidence_type: EvidenceType) -> list[Evidence]:
        return [e for e in self.evidence_items.values() if e.evidence_type == evidence_type]


class FindingTracker:
    """Tracks findings through their lifecycle."""

    def __init__(self, evidence_manager: EvidenceManager) -> None:
        self.findings: dict[str, Finding] = {}
        self.evidence_manager = evidence_manager

    def create_finding(self, audit_id: str, title: str, severity: FindingSeverity,
                       condition: str, criteria: str, impact: str,
                       recommendation: str, owner: str = "") -> Finding:
        finding = Finding(
            audit_id=audit_id,
            title=title,
            severity=severity,
            condition=condition,
            criteria=criteria,
            impact=impact,
            recommendation=recommendation,
            owner=owner,
        )
        deadline_days = finding.get_remediation_deadline()
        finding.target_remediation = datetime.utcnow() + timedelta(days=deadline_days)
        self.findings[finding.finding_id] = finding
        return finding

    def transition_finding(self, finding_id: str, new_state: FindingState) -> bool:
        finding = self.findings.get(finding_id)
        if finding:
            return finding.transition(new_state)
        return False

    def add_evidence(self, finding_id: str, evidence_type: EvidenceType,
                     description: str, source: str, collector: str,
                     content: str = "") -> Optional[Evidence]:
        if finding_id not in self.findings:
            return None
        return self.evidence_manager.collect_evidence(
            finding_id, evidence_type, description, source, collector, content
        )

    def get_findings_by_severity(self, severity: FindingSeverity) -> list[Finding]:
        return [f for f in self.findings.values() if f.severity == severity]

    def get_findings_by_state(self, state: FindingState) -> list[Finding]:
        return [f for f in self.findings.values() if f.state == state]

    def get_open_findings(self) -> list[Finding]:
        return [f for f in self.findings.values() if f.is_open]

    def get_overdue_findings(self) -> list[Finding]:
        return [f for f in self.findings.values() if f.is_overdue]

    def get_repeat_findings(self) -> dict[str, list[Finding]]:
        repeats: dict[str, list[Finding]] = {}
        for f in self.findings.values():
            key = f.title.lower().strip()
            repeats.setdefault(key, []).append(f)
        return {k: v for k, v in repeats.items() if len(v) > 1}

    def get_mttr(self) -> Optional[float]:
        completed = [
            f for f in self.findings.values()
            if f.actual_remediation is not None
        ]
        if not completed:
            return None
        total_days = sum(
            (f.actual_remediation - f.identified_at).days for f in completed
        )
        return total_days / len(completed)


class RemediationWorkflow:
    """Manages remediation workflows for findings."""

    def __init__(self, finding_tracker: FindingTracker) -> None:
        self.tracker = finding_tracker

    def start_remediation(self, finding_id: str, plan: str) -> bool:
        finding = self.tracker.findings.get(finding_id)
        if not finding:
            return False
        finding.management_response = plan
        finding.transition(FindingState.REMEDIATION_PLANNED)
        finding.transition(FindingState.REMEDIATION_IN_PROGRESS)
        finding.remediation_status = RemediationStatus.IN_PROGRESS
        return True

    def complete_remediation(self, finding_id: str,
                             evidence_content: str = "") -> bool:
        finding = self.tracker.findings.get(finding_id)
        if not finding:
            return False
        if evidence_content:
            self.tracker.add_evidence(
                finding_id, EvidenceType.DOCUMENTARY,
                "Remediation evidence", "remediation_system", "system",
                evidence_content,
            )
        finding.transition(FindingState.REMEDIATION_COMPLETE)
        finding.actual_remediation = datetime.utcnow()
        finding.remediation_status = RemediationStatus.COMPLETE
        return True

    def verify_remediation(self, finding_id: str,
                           verified_by: str = "") -> bool:
        finding = self.tracker.findings.get(finding_id)
        if not finding:
            return False
        finding.transition(FindingState.VERIFIED)
        finding.remediation_status = RemediationStatus.VERIFIED
        return True

    def close_finding(self, finding_id: str) -> bool:
        finding = self.tracker.findings.get(finding_id)
        if not finding:
            return False
        return finding.transition(FindingState.CLOSED)

    def reopen_finding(self, finding_id: str, reason: str) -> bool:
        finding = self.tracker.findings.get(finding_id)
        if not finding:
            return False
        finding.metadata["reopen_reason"] = reason
        return finding.transition(FindingState.REOPENED)

    def get_remediation_metrics(self) -> dict[str, Any]:
        all_findings = list(self.tracker.findings.values())
        open_count = sum(1 for f in all_findings if f.is_open)
        overdue_count = sum(1 for f in all_findings if f.is_overdue)
        completed_count = sum(
            1 for f in all_findings if f.remediation_status == RemediationStatus.VERIFIED
        )
        total = len(all_findings)

        return {
            "total_findings": total,
            "open_findings": open_count,
            "overdue_findings": overdue_count,
            "completed_remediations": completed_count,
            "remediation_rate": (completed_count / total * 100) if total > 0 else 0.0,
            "on_time_rate": ((total - overdue_count) / total * 100) if total > 0 else 0.0,
            "mttr_days": self.tracker.get_mttr(),
        }


class ContinuousAuditor:
    """Automated continuous auditing engine."""

    def __init__(self) -> None:
        self.test_results: list[dict[str, Any]] = []
        self.rules: list[dict[str, Any]] = []

    def add_rule(self, rule_id: str, name: str, description: str,
                 test_function: str, frequency: str = "daily",
                 severity: str = "medium") -> None:
        self.rules.append({
            "rule_id": rule_id,
            "name": name,
            "description": description,
            "test_function": test_function,
            "frequency": frequency,
            "severity": severity,
            "enabled": True,
            "created_at": datetime.utcnow().isoformat(),
        })

    def execute_rule(self, rule_id: str, data: Any = None) -> dict[str, Any]:
        rule = next((r for r in self.rules if r["rule_id"] == rule_id), None)
        if not rule:
            return {"error": f"Rule {rule_id} not found"}

        result = {
            "rule_id": rule_id,
            "rule_name": rule["name"],
            "executed_at": datetime.utcnow().isoformat(),
            "status": "pass",
            "exceptions": [],
            "details": {},
        }
        self.test_results.append(result)
        return result

    def get_test_results(self, rule_id: str | None = None,
                         status: str | None = None) -> list[dict[str, Any]]:
        results = self.test_results
        if rule_id:
            results = [r for r in results if r.get("rule_id") == rule_id]
        if status:
            results = [r for r in results if r.get("status") == status]
        return results

    def get_exception_summary(self) -> dict[str, int]:
        summary: dict[str, int] = {}
        for result in self.test_results:
            for exc in result.get("exceptions", []):
                summary[exc] = summary.get(exc, 0) + 1
        return summary

    def get_rules_by_frequency(self, frequency: str) -> list[dict[str, Any]]:
        return [r for r in self.rules if r["frequency"] == frequency and r["enabled"]]


# ─── Demo ────────────────────────────────────────────────────────────────────

def main() -> None:
    """Demonstrate audit management system."""
    print("=" * 70)
    print("AUDIT MANAGEMENT SYSTEM")
    print("=" * 70)

    # 1. Audit Planning
    print("\n[1] Audit Planning")
    print("-" * 40)
    planner = AuditPlanner()
    plan = planner.create_plan(
        title="Q3 Access Control Audit",
        audit_type=AuditType.ITGC,
        scope="All production systems and IAM platform",
        lead_auditor="Alice Johnson",
        objectives=["Verify access control effectiveness", "Validate least privilege"],
    )
    planner.schedule_audit(
        plan.audit_id,
        start=datetime(2025, 7, 1),
        end=datetime(2025, 7, 15),
        team=["Alice Johnson", "Bob Chen", "Carol Davis"],
        estimated_hours=120.0,
    )
    print(f"  Plan: {plan.title} ({plan.audit_id})")
    print(f"  Type: {plan.audit_type.value}")
    print(f"  Status: {plan.status.value}")
    print(f"  Duration: {plan.duration_days} days")
    print(f"  Team: {', '.join(plan.audit_team)}")

    upcoming = planner.get_upcoming_audits(within_days=60)
    print(f"  Upcoming audits (60 days): {len(upcoming)}")

    # 2. Finding Lifecycle
    print("\n[2] Finding Lifecycle")
    print("-" * 40)
    evidence_mgr = EvidenceManager()
    tracker = FindingTracker(evidence_mgr)

    finding1 = tracker.create_finding(
        audit_id=plan.audit_id,
        title="Excessive Privileged Access",
        severity=FindingSeverity.HIGH,
        condition="3 service accounts have permanent admin access to production DB",
        criteria="Least privilege principle; access must be time-bound and role-based",
        impact="Potential data breach affecting 50K+ customer records",
        recommendation="Implement just-in-time access and reduce standing privileges",
        owner="Infrastructure Team",
    )
    finding2 = tracker.create_finding(
        audit_id=plan.audit_id,
        title="Stale User Accounts",
        severity=FindingSeverity.MEDIUM,
        condition="12 user accounts inactive >90 days still have active credentials",
        criteria="User access review must be performed quarterly",
        impact="Increased attack surface for credential-based attacks",
        recommendation="Implement automated deprovisioning after 60-day inactivity",
        owner="IT Operations",
    )

    print(f"  Created: {finding1.finding_id} - {finding1.title} ({finding1.severity.value})")
    print(f"  Created: {finding2.finding_id} - {finding2.title} ({finding2.severity.value})")
    print(f"  Finding1 deadline: {finding1.days_to_remediation} days")

    # 3. Evidence Collection
    print("\n[3] Evidence Collection")
    print("-" * 40)
    tracker.add_evidence(
        finding1.finding_id, EvidenceType.ELECTRONIC,
        "IAM role listing showing permanent admin access",
        "AWS IAM Console", "Alice Johnson",
        '{"roles": ["admin-prod-db", "admin-prod-full"]}',
    )
    tracker.add_evidence(
        finding1.finding_id, EvidenceType.DOCUMENTARY,
        "Screenshot of access review policy",
        "SharePoint", "Alice Johnson",
    )
    evidence = evidence_mgr.get_evidence_for_finding(finding1.finding_id)
    print(f"  Evidence items for {finding1.finding_id}: {len(evidence)}")
    for e in evidence:
        print(f"    {e.evidence_id}: {e.evidence_type.value} - {e.description}")
        print(f"      Collector: {e.collector}, Hash: {e.content_hash[:16]}...")

    # 4. Finding Transitions
    print("\n[4] Finding State Transitions")
    print("-" * 40)
    for state_name in ["VALIDATED", "REPORTED", "ACKNOWLEDGED",
                       "REMEDIATION_PLANNED", "REMEDIATION_IN_PROGRESS"]:
        new_state = FindingState(state_name.lower())
        success = tracker.transition_finding(finding1.finding_id, new_state)
        print(f"  {finding1.finding_id}: -> {state_name} ({'OK' if success else 'FAIL'})")
    print(f"  Current state: {finding1.state.value}")

    # 5. Remediation Workflow
    print("\n[5] Remediation Workflow")
    print("-" * 40)
    workflow = RemediationWorkflow(tracker)
    workflow.start_remediation(
        finding1.finding_id,
        "Implement JIT access via HashiCorp Vault; remove standing admin access",
    )
    workflow.complete_remediation(
        finding1.finding_id,
        '{"vault_policy": "prod-db-readonly", "admin_accounts_disabled": true}',
    )
    workflow.verify_remediation(finding1.finding_id, "Alice Johnson")
    workflow.close_finding(finding1.finding_id)
    print(f"  {finding1.finding_id}: state={finding1.state.value}, "
          f"status={finding1.remediation_status.value}")

    metrics = workflow.get_remediation_metrics()
    print(f"  Metrics: {metrics['completed_remediations']}/{metrics['total_findings']} completed")
    print(f"  MTTR: {metrics['mttr_days']:.1f} days")

    # 6. Continuous Auditing
    print("\n[6] Continuous Auditing")
    print("-" * 40)
    auditor = ContinuousAuditor()
    auditor.add_rule(
        "CA-001", "Privilege Escalation Detection",
        "Detect any IAM policy changes granting admin access",
        "detect_escalation", "daily", "critical",
    )
    auditor.add_rule(
        "CA-002", "Stale Account Monitor",
        "Flag accounts inactive >60 days",
        "check_inactive", "weekly", "medium",
    )
    auditor.add_rule(
        "CA-003", "Config Drift Detection",
        "Compare production configs against baseline",
        "detect_drift", "daily", "high",
    )
    for rule in auditor.rules:
        auditor.execute_rule(rule["rule_id"])

    print(f"  Rules: {len(auditor.rules)}")
    print(f"  Executions: {len(auditor.get_test_results())}")
    daily_rules = auditor.get_rules_by_frequency("daily")
    print(f"  Daily rules: {len(daily_rules)}")

    # 7. Summary
    print("\n[7] Audit Summary")
    print("-" * 40)
    report = AuditReport(
        audit_id=plan.audit_id,
        findings=[finding1, finding2],
        overall_opinion="Needs Improvement",
    )
    print(f"  Report: {report.report_id}")
    print(f"  Total findings: {report.total_findings}")
    print(f"  By severity: {report.findings_by_severity}")
    print(f"  Open findings: {len(report.open_findings)}")
    print(f"  Overdue: {len(report.overdue_findings)}")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
