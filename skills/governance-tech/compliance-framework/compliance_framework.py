"""
Compliance Framework Management System

Implements framework selection, control mapping, maturity assessment,
gap analysis, and continuous monitoring for ISO 27001, SOC 2, NIST CSF, and COBIT.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional
from uuid import uuid4


# ─── Enums ───────────────────────────────────────────────────────────────────

class FrameworkType(Enum):
    ISO27001 = "iso27001"
    SOC2 = "soc2"
    NIST_CSF = "nist_csf"
    COBIT = "cobit"


class MaturityLevel(Enum):
    INITIAL = 1
    DEVELOPING = 2
    DEFINED = 3
    MANAGED = 4
    OPTIMIZING = 5


class GapSeverity(Enum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    OBSERVATION = "observation"


class ControlStatus(Enum):
    NOT_IMPLEMENTED = "not_implemented"
    PARTIALLY_IMPLEMENTED = "partially_implemented"
    IMPLEMENTED = "implemented"
    EFFECTIVE = "effective"
    EXCEPTION = "exception"


class MonitoringFrequency(Enum):
    REAL_TIME = "real_time"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"


# ─── Data Classes ────────────────────────────────────────────────────────────

@dataclass
class Control:
    """Represents a single compliance control."""
    control_id: str
    framework: FrameworkType
    domain: str
    title: str
    description: str
    status: ControlStatus = ControlStatus.NOT_IMPLEMENTED
    owner: Optional[str] = None
    operator: Optional[str] = None
    evidence_refs: list[str] = field(default_factory=list)
    mapped_controls: dict[str, str] = field(default_factory=dict)
    last_assessed: Optional[datetime] = None
    next_assessment: Optional[datetime] = None
    monitoring_frequency: MonitoringFrequency = MonitoringFrequency.QUARTERLY
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_effective(self) -> bool:
        return self.status == ControlStatus.EFFECTIVE

    @property
    def needs_attention(self) -> bool:
        return self.status in (
            ControlStatus.NOT_IMPLEMENTED,
            ControlStatus.PARTIALLY_IMPLEMENTED,
            ControlStatus.EXCEPTION,
        )

    def assess(self, status: ControlStatus, evidence: list[str] | None = None) -> None:
        self.status = status
        self.last_assessed = datetime.utcnow()
        if evidence:
            self.evidence_refs.extend(evidence)
        self.next_assessment = self._calculate_next_assessment()

    def _calculate_next_assessment(self) -> datetime:
        frequency_days = {
            MonitoringFrequency.REAL_TIME: 1,
            MonitoringFrequency.DAILY: 1,
            MonitoringFrequency.WEEKLY: 7,
            MonitoringFrequency.MONTHLY: 30,
            MonitoringFrequency.QUARTERLY: 90,
            MonitoringFrequency.ANNUALLY: 365,
        }
        days = frequency_days.get(self.monitoring_frequency, 90)
        return datetime.utcnow() + timedelta(days=days)


@dataclass
class ControlMapping:
    """Maps controls across different frameworks."""
    source_control: str
    source_framework: FrameworkType
    target_control: str
    target_framework: FrameworkType
    mapping_type: str = "equivalent"  # equivalent, partial, supplementary
    confidence: float = 1.0
    notes: str = ""


@dataclass
class MaturityAssessment:
    """Result of a maturity assessment for a domain."""
    domain: str
    level: MaturityLevel
    score: float  # 0.0 to 5.0
    findings: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    assessed_by: str = ""
    assessed_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Gap:
    """Identified gap between current and target state."""
    gap_id: str = field(default_factory=lambda: str(uuid4())[:8])
    control_id: str = ""
    framework: FrameworkType = FrameworkType.ISO27001
    severity: GapSeverity = GapSeverity.MINOR
    description: str = ""
    current_state: str = ""
    target_state: str = ""
    remediation: str = ""
    effort_estimate: str = ""
    risk_score: float = 0.0
    owner: str = ""
    due_date: Optional[datetime] = None

    @property
    def is_overdue(self) -> bool:
        if self.due_date is None:
            return False
        return datetime.utcnow() > self.due_date


@dataclass
class ComplianceReport:
    """Aggregated compliance posture report."""
    report_id: str = field(default_factory=lambda: str(uuid4())[:8])
    generated_at: datetime = field(default_factory=datetime.utcnow)
    framework: FrameworkType = FrameworkType.ISO27001
    total_controls: int = 0
    effective_controls: int = 0
    gaps_by_severity: dict[str, int] = field(default_factory=dict)
    maturity_scores: dict[str, float] = field(default_factory=dict)
    compliance_percentage: float = 0.0
    critical_findings: list[str] = field(default_factory=list)

    @property
    def overall_posture(self) -> str:
        if self.compliance_percentage >= 90:
            return "STRONG"
        elif self.compliance_percentage >= 70:
            return "ADEQUATE"
        elif self.compliance_percentage >= 50:
            return "NEEDS_IMPROVEMENT"
        return "WEAK"


# ─── Core Classes ────────────────────────────────────────────────────────────

class FrameworkRegistry:
    """Registry of framework controls and their mappings."""

    def __init__(self) -> None:
        self.controls: dict[str, Control] = {}
        self.mappings: list[ControlMapping] = []

    def register_control(self, control: Control) -> None:
        self.controls[control.control_id] = control

    def add_mapping(self, mapping: ControlMapping) -> None:
        self.mappings.append(mapping)

    def get_controls_by_framework(self, framework: FrameworkType) -> list[Control]:
        return [c for c in self.controls.values() if c.framework == framework]

    def get_controls_by_domain(self, domain: str) -> list[Control]:
        return [c for c in self.controls.values() if c.domain == domain]

    def get_mapped_controls(self, control_id: str) -> list[ControlMapping]:
        return [m for m in self.mappings if m.source_control == control_id or m.target_control == control_id]

    def get_coverage(self, framework: FrameworkType) -> float:
        controls = self.get_controls_by_framework(framework)
        if not controls:
            return 0.0
        effective = sum(1 for c in controls if c.is_effective)
        return effective / len(controls) * 100


class MaturityAssessor:
    """Conducts maturity assessments across organizational domains."""

    MATURITY_DIMENSIONS = [
        "policy_governance",
        "people_culture",
        "process_operations",
        "technology_tools",
        "metrics_reporting",
    ]

    def __init__(self, registry: FrameworkRegistry) -> None:
        self.registry = registry
        self.assessments: list[MaturityAssessment] = []

    def assess_domain(self, domain: str, scores: dict[str, float],
                      assessor: str = "") -> MaturityAssessment:
        valid_scores = [s for s in scores.values() if 0.0 <= s <= 5.0]
        if not valid_scores:
            avg_score = 0.0
        else:
            avg_score = sum(valid_scores) / len(valid_scores)

        level = self._score_to_level(avg_score)
        findings = self._generate_findings(scores)
        recommendations = self._generate_recommendations(scores, level)

        assessment = MaturityAssessment(
            domain=domain,
            level=level,
            score=avg_score,
            findings=findings,
            recommendations=recommendations,
            assessed_by=assessor,
        )
        self.assessments.append(assessment)
        return assessment

    def _score_to_level(self, score: float) -> MaturityLevel:
        if score >= 4.5:
            return MaturityLevel.OPTIMIZING
        elif score >= 3.5:
            return MaturityLevel.MANAGED
        elif score >= 2.5:
            return MaturityLevel.DEFINED
        elif score >= 1.5:
            return MaturityLevel.DEVELOPING
        return MaturityLevel.INITIAL

    def _generate_findings(self, scores: dict[str, float]) -> list[str]:
        findings = []
        for dim, score in scores.items():
            if score < 2.0:
                findings.append(f"{dim}: Critical maturity gap (score {score})")
            elif score < 3.0:
                findings.append(f"{dim}: Below target maturity (score {score})")
        return findings

    def _generate_recommendations(self, scores: dict[str, float],
                                   level: MaturityLevel) -> list[str]:
        recs = []
        weak_dims = sorted(scores.items(), key=lambda x: x[1])[:2]
        for dim, score in weak_dims:
            if score < 3.0:
                recs.append(f"Invest in {dim.replace('_', ' ')} to reach defined maturity")
        if level.value < MaturityLevel.DEFINED.value:
            recs.append("Prioritize documentation and standardization across all domains")
        return recs

    def get_assessment_history(self, domain: str) -> list[MaturityAssessment]:
        return [a for a in self.assessments if a.domain == domain]


class GapAnalyzer:
    """Performs gap analysis between current and target compliance state."""

    def __init__(self, registry: FrameworkRegistry) -> None:
        self.registry = registry
        self.gaps: list[Gap] = []

    def analyze(self, framework: FrameworkType,
                target_maturity: MaturityLevel = MaturityLevel.MANAGED) -> list[Gap]:
        controls = self.registry.get_controls_by_framework(framework)
        new_gaps = []

        for control in controls:
            if control.needs_attention:
                gap = self._create_gap(control, target_maturity)
                new_gaps.append(gap)
                self.gaps.append(gaps)

        return new_gaps

    def _create_gap(self, control: Control,
                    target_maturity: MaturityLevel) -> Gap:
        severity = self._determine_severity(control)
        remediation = self._suggest_remediation(control, severity)
        risk_score = self._calculate_risk_score(severity, control)

        return Gap(
            control_id=control.control_id,
            framework=control.framework,
            severity=severity,
            description=f"Control {control.control_id}: {control.title} is {control.status.value}",
            current_state=control.status.value,
            target_state="effective",
            remediation=remediation,
            risk_score=risk_score,
            owner=control.owner or "unassigned",
        )

    def _determine_severity(self, control: Control) -> GapSeverity:
        if control.status == ControlStatus.NOT_IMPLEMENTED:
            return GapSeverity.CRITICAL
        elif control.status == ControlStatus.PARTIALLY_IMPLEMENTED:
            return GapSeverity.MAJOR
        elif control.status == ControlStatus.EXCEPTION:
            return GapSeverity.MAJOR
        return GapSeverity.MINOR

    def _suggest_remediation(self, control: Control, severity: GapSeverity) -> str:
        if severity == GapSeverity.CRITICAL:
            return f"Implement control {control.control_id} immediately - no control exists"
        elif severity == GapSeverity.MAJOR:
            return f"Complete implementation of control {control.control_id}"
        return f"Strengthen existing control {control.control_id}"

    def _calculate_risk_score(self, severity: GapSeverity, control: Control) -> float:
        severity_scores = {
            GapSeverity.CRITICAL: 4.0,
            GapSeverity.MAJOR: 3.0,
            GapSeverity.MINOR: 2.0,
            GapSeverity.OBSERVATION: 1.0,
        }
        base = severity_scores.get(severity, 1.0)
        if control.monitoring_frequency in (MonitoringFrequency.REAL_TIME, MonitoringFrequency.DAILY):
            base *= 1.2
        return min(base, 5.0)

    def prioritize_gaps(self) -> list[Gap]:
        return sorted(self.gaps, key=lambda g: g.risk_score, reverse=True)

    def get_gaps_by_severity(self, severity: GapSeverity) -> list[Gap]:
        return [g for g in self.gaps if g.severity == severity]

    def get_overdue_gaps(self) -> list[Gap]:
        return [g for g in self.gaps if g.is_overdue]


class ComplianceMonitor:
    """Continuous monitoring of compliance posture."""

    def __init__(self, registry: FrameworkRegistry) -> None:
        self.registry = registry
        self.alerts: list[dict[str, Any]] = []

    def check_control_freshness(self) -> list[dict[str, Any]]:
        stale = []
        now = datetime.utcnow()
        for control in self.registry.controls.values():
            if control.next_assessment and control.next_assessment < now:
                alert = {
                    "control_id": control.control_id,
                    "framework": control.framework.value,
                    "overdue_days": (now - control.next_assessment).days,
                    "severity": "high" if control.needs_attention else "medium",
                }
                stale.append(alert)
                self.alerts.append(alert)
        return stale

    def generate_posture_report(self, framework: FrameworkType) -> ComplianceReport:
        controls = self.registry.get_controls_by_framework(framework)
        total = len(controls)
        effective = sum(1 for c in controls if c.is_effective)

        gaps_by_severity: dict[str, int] = {}
        for c in controls:
            if c.needs_attention:
                sev = self._control_to_gap_severity(c)
                gaps_by_severity[sev.value] = gaps_by_severity.get(sev.value, 0) + 1

        compliance_pct = (effective / total * 100) if total > 0 else 0.0

        return ComplianceReport(
            framework=framework,
            total_controls=total,
            effective_controls=effective,
            gaps_by_severity=gaps_by_severity,
            compliance_percentage=round(compliance_pct, 1),
            critical_findings=[
                f"{sev}: {count} controls" for sev, count in gaps_by_severity.items()
                if sev in ("critical", "major")
            ],
        )

    def _control_to_gap_severity(self, control: Control) -> GapSeverity:
        if control.status == ControlStatus.NOT_IMPLEMENTED:
            return GapSeverity.CRITICAL
        elif control.status in (ControlStatus.PARTIALLY_IMPLEMENTED, ControlStatus.EXCEPTION):
            return GapSeverity.MAJOR
        return GapSeverity.MINOR


class FrameworkSelector:
    """Helps select the most appropriate compliance framework."""

    FRAMEWORK_SCORES: dict[FrameworkType, dict[str, float]] = {
        FrameworkType.ISO27001: {
            "international": 5.0,
            "certification": 5.0,
            "us_focus": 2.0,
            "saas_service": 3.0,
            "it_governance": 3.0,
        },
        FrameworkType.SOC2: {
            "international": 3.0,
            "certification": 3.0,
            "us_focus": 5.0,
            "saas_service": 5.0,
            "it_governance": 2.0,
        },
        FrameworkType.NIST_CSF: {
            "international": 2.0,
            "certification": 2.0,
            "us_focus": 5.0,
            "saas_service": 3.0,
            "it_governance": 3.0,
        },
        FrameworkType.COBIT: {
            "international": 3.0,
            "certification": 1.0,
            "us_focus": 3.0,
            "saas_service": 2.0,
            "it_governance": 5.0,
        },
    }

    def evaluate(self, requirements: dict[str, bool]) -> list[tuple[FrameworkType, float]]:
        scores = []
        for framework, profile in self.FRAMEWORK_SCORES.items():
            total = 0.0
            count = 0
            for req, needed in requirements.items():
                if needed and req in profile:
                    total += profile[req]
                    count += 1
            avg = total / count if count > 0 else 0.0
            scores.append((framework, round(avg, 2)))
        return sorted(scores, key=lambda x: x[1], reverse=True)

    def recommend(self, requirements: dict[str, bool]) -> FrameworkType:
        ranked = self.evaluate(requirements)
        return ranked[0][0] if ranked else FrameworkType.NIST_CSF


# ─── Demo ────────────────────────────────────────────────────────────────────

def main() -> None:
    """Demonstrate compliance framework management system."""
    print("=" * 70)
    print("COMPLIANCE FRAMEWORK MANAGEMENT SYSTEM")
    print("=" * 70)

    # 1. Framework Selection
    print("\n[1] Framework Selection")
    print("-" * 40)
    selector = FrameworkSelector()
    requirements = {
        "international": True,
        "certification": True,
        "us_focus": False,
        "saas_service": True,
        "it_governance": False,
    }
    ranked = selector.evaluate(requirements)
    for fw, score in ranked:
        print(f"  {fw.value:12s} -> score {score}")
    recommended = selector.recommend(requirements)
    print(f"  Recommended: {recommended.value}")

    # 2. Register Controls
    print("\n[2] Registering Controls")
    print("-" * 40)
    registry = FrameworkRegistry()

    sample_controls = [
        ("A.9.1.1", FrameworkType.ISO27001, "access_control",
         "Access Control Policy", "Establish access control policy"),
        ("CC6.1", FrameworkType.SOC2, "access_control",
         "Logical Access Security", "Logical access controls implemented"),
        ("PR.AC-1", FrameworkType.NIST_CSF, "access_control",
         "Identity Management", "Identity and credentials managed"),
        ("DSS05.01", FrameworkType.COBIT, "access_control",
         "Manage Security", "IT security management established"),
        ("A.16.1.1", FrameworkType.ISO27001, "incident_response",
         "IR Plan", "Incident response plan established"),
        ("CC7.1", FrameworkType.SOC2, "incident_response",
         "Incident Detection", "Detection of security incidents"),
        ("RS.RP-1", FrameworkType.NIST_CSF, "incident_response",
         "Response Plan", "Response plan executed"),
    ]

    for cid, fw, domain, title, desc in sample_controls:
        ctrl = Control(
            control_id=cid, framework=fw, domain=domain,
            title=title, description=desc,
            status=ControlStatus.EFFECTIVE if cid.startswith(("A.9", "CC6")) else ControlStatus.PARTIALLY_IMPLEMENTED,
        )
        registry.register_control(ctrl)
    print(f"  Registered {len(registry.controls)} controls across {len(FrameworkType)} frameworks")

    # 3. Control Mapping
    print("\n[3] Control Mappings")
    print("-" * 40)
    mappings = [
        ControlMapping("A.9.1.1", FrameworkType.ISO27001, "CC6.1", FrameworkType.SOC2),
        ControlMapping("A.9.1.1", FrameworkType.ISO27001, "PR.AC-1", FrameworkType.NIST_CSF),
        ControlMapping("CC6.1", FrameworkType.SOC2, "PR.AC-1", FrameworkType.NIST_CSF),
    ]
    for m in mappings:
        registry.add_mapping(m)
        print(f"  {m.source_framework.value}:{m.source_control} <-> "
              f"{m.target_framework.value}:{m.target_control}")

    # 4. Maturity Assessment
    print("\n[4] Maturity Assessment")
    print("-" * 40)
    assessor = MaturityAssessor(registry)
    assessment = assessor.assess_domain(
        "access_control",
        {"policy_governance": 3.5, "people_culture": 2.0,
         "process_operations": 3.0, "technology_tools": 4.0,
         "metrics_reporting": 2.5},
        assessor="Jane Smith",
    )
    print(f"  Domain: {assessment.domain}")
    print(f"  Level: {assessment.level.name} (score {assessment.score:.1f})")
    for f in assessment.findings:
        print(f"    Finding: {f}")
    for r in assessment.recommendations:
        print(f"    Recommend: {r}")

    # 5. Gap Analysis
    print("\n[5] Gap Analysis")
    print("-" * 40)
    gap_analyzer = GapAnalyzer(registry)
    gaps = gap_analyzer.analyze(FrameworkType.ISO27001)
    prioritized = gap_analyzer.prioritize_gaps()
    for g in prioritized[:3]:
        print(f"  [{g.severity.value.upper():12s}] {g.control_id}: {g.description}")
        print(f"    Risk: {g.risk_score:.1f} | Remediation: {g.remediation}")

    # 6. Continuous Monitoring
    print("\n[6] Continuous Monitoring")
    print("-" * 40)
    monitor = ComplianceMonitor(registry)
    stale = monitor.check_control_freshness()
    print(f"  Stale controls: {len(stale)}")
    for s in stale[:2]:
        print(f"    {s['control_id']} ({s['framework']}) - {s['overdue_days']}d overdue")

    # 7. Posture Report
    print("\n[7] Compliance Posture Report")
    print("-" * 40)
    for fw in FrameworkType:
        report = monitor.generate_posture_report(fw)
        print(f"  {fw.value:12s} | {report.effective_controls}/{report.total_controls} effective "
              f"| {report.compliance_percentage}% | Posture: {report.overall_posture}")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
