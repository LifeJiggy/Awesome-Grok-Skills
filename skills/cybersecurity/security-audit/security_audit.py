"""
Security Audit Module
Audit planning, control assessment, compliance mapping, and risk evaluation.
"""

from __future__ import annotations

import logging
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ControlStatus(Enum):
    PASS = "pass"
    FAIL = "fail"
    PARTIAL = "partial"
    NOT_APPLICABLE = "not_applicable"
    NOT_TESTED = "not_tested"


class RiskLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class AuditPlan:
    """Audit plan."""
    audit_id: str
    title: str
    scope: List[str]
    frameworks: List[str]
    duration_days: int
    team_size: int
    total_controls: int = 0
    start_date: str = ""
    status: str = "planning"


@dataclass
class ControlResult:
    """Control assessment result."""
    control_id: str
    status: ControlStatus
    score: int = 0
    evidence: str = ""
    findings: List[str] = field(default_factory=list)
    assessor: str = ""
    assessed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ComplianceMapping:
    """Compliance mapping result."""
    source: str
    target: str
    mapped_count: int = 0
    total_count: int = 0
    gaps: List[str] = field(default_factory=list)
    coverage_pct: float = 0.0


@dataclass
class RiskAssessment:
    """Risk assessment result."""
    title: str
    risk_level: RiskLevel
    score: float
    likelihood: str = ""
    impact: str = ""
    treatment: str = ""
    owner: str = ""


@dataclass
class AuditReportData:
    """Audit report data."""
    title: str = ""
    overall_score: float = 0.0
    total_controls: int = 0
    passed: int = 0
    failed: int = 0
    partial: int = 0
    critical_risks: int = 0
    executive_summary: str = ""
    recommendations: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Audit Planner
# ---------------------------------------------------------------------------

class AuditPlanner:
    """Plan and manage security audits."""

    FRAMEWORK_CONTROLS = {
        "ISO 27001": 114,
        "SOC 2": 64,
        "NIST CSF": 108,
        "PCI DSS": 300,
        "HIPAA": 42,
    }

    def create_plan(
        self,
        title: str,
        scope: Optional[List[str]] = None,
        frameworks: Optional[List[str]] = None,
        duration_days: int = 30,
        team_size: int = 4,
    ) -> AuditPlan:
        frameworks = frameworks or ["ISO 27001"]
        total = sum(self.FRAMEWORK_CONTROLS.get(f, 50) for f in frameworks)
        return AuditPlan(
            audit_id=f"AUD-{secrets.token_hex(4).upper()}",
            title=title,
            scope=scope or ["IT infrastructure"],
            frameworks=frameworks,
            duration_days=duration_days,
            team_size=team_size,
            total_controls=total,
            start_date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        )


# ---------------------------------------------------------------------------
# Control Assessor
# ---------------------------------------------------------------------------

class ControlAssessor:
    """Assess security controls."""

    def assess_controls(
        self,
        control_ids: List[str],
        evidence: Optional[List[Dict[str, Any]]] = None,
    ) -> List[ControlResult]:
        results: List[ControlResult] = []
        evidence_map = {e["control"]: e for e in (evidence or [])}
        for cid in control_ids:
            ev = evidence_map.get(cid, {})
            status_str = ev.get("status", "not_tested")
            try:
                status = ControlStatus(status_str)
            except ValueError:
                status = ControlStatus.NOT_TESTED
            score = 100 if status == ControlStatus.PASS else (50 if status == ControlStatus.PARTIAL else 0)
            results.append(ControlResult(
                control_id=cid,
                status=status,
                score=score,
                evidence=ev.get("evidence", ""),
            ))
        return results

    def calculate_compliance_score(self, results: List[ControlResult]) -> float:
        if not results:
            return 0.0
        total = len(results)
        passed = sum(1 for r in results if r.status == ControlStatus.PASS)
        partial = sum(1 for r in results if r.status == ControlStatus.PARTIAL)
        return (passed + partial * 0.5) / total * 100


# ---------------------------------------------------------------------------
# Compliance Mapper
# ---------------------------------------------------------------------------

class ComplianceMapper:
    """Map controls between frameworks."""

    def map_controls(
        self,
        source: str = "internal_controls",
        target_framework: str = "SOC 2",
    ) -> ComplianceMapping:
        total = self.FRAMEWORK_CONTROLS.get(target_framework, 64)
        mapped = int(total * 0.85)
        gaps = [f"Control gap in domain {i}" for i in range(total - mapped)]
        return ComplianceMapping(
            source=source,
            target=target_framework,
            mapped_count=mapped,
            total_count=total,
            gaps=gaps,
            coverage_pct=mapped / max(total, 1) * 100,
        )

    FRAMEWORK_CONTROLS = {"SOC 2": 64, "ISO 27001": 114, "NIST CSF": 108, "PCI DSS": 300}


# ---------------------------------------------------------------------------
# Risk Evaluator
# ---------------------------------------------------------------------------

class RiskEvaluator:
    """Evaluate and score risks."""

    LIKELIHOOD_MAP = {"low": 1, "medium": 3, "high": 5}
    IMPACT_MAP = {"low": 1, "medium": 3, "high": 5, "critical": 10}

    def evaluate(
        self, findings: List[Dict[str, Any]]
    ) -> List[RiskAssessment]:
        risks: List[RiskAssessment] = []
        for f in findings:
            likelihood = self.LIKELIHOOD_MAP.get(f.get("likelihood", "medium"), 3)
            impact = self.IMPACT_MAP.get(f.get("impact", "medium"), 3)
            score = likelihood * impact
            if score >= 20:
                level = RiskLevel.CRITICAL
            elif score >= 12:
                level = RiskLevel.HIGH
            elif score >= 6:
                level = RiskLevel.MEDIUM
            elif score >= 2:
                level = RiskLevel.LOW
            else:
                level = RiskLevel.INFORMATIONAL
            risks.append(RiskAssessment(
                title=f.get("title", "Unknown"),
                risk_level=level,
                score=score,
                likelihood=f.get("likelihood", "medium"),
                impact=f.get("impact", "medium"),
                treatment="mitigate" if score >= 6 else "accept",
            ))
        return sorted(risks, key=lambda r: r.score, reverse=True)


# ---------------------------------------------------------------------------
# Audit Report
# ---------------------------------------------------------------------------

class AuditReport:
    """Generate audit reports."""

    def generate(
        self,
        audit_plan: Optional[AuditPlan] = None,
        control_results: Optional[List[ControlResult]] = None,
        risk_assessment: Optional[List[RiskAssessment]] = None,
    ) -> AuditReportData:
        plan = audit_plan or AuditPlan("default", "", [], [], 0, 0)
        controls = control_results or []
        risks = risk_assessment or []
        passed = sum(1 for c in controls if c.status == ControlStatus.PASS)
        failed = sum(1 for c in controls if c.status == ControlStatus.FAIL)
        partial = sum(1 for c in controls if c.status == ControlStatus.PARTIAL)
        score = (passed + partial * 0.5) / max(len(controls), 1) * 100
        critical = sum(1 for r in risks if r.risk_level == RiskLevel.CRITICAL)
        return AuditReportData(
            title=f"Audit Report - {plan.title}",
            overall_score=round(score, 1),
            total_controls=len(controls),
            passed=passed,
            failed=failed,
            partial=partial,
            critical_risks=critical,
            executive_summary=f"Overall compliance: {score:.1f}%. {critical} critical risks identified.",
            recommendations=[
                "Address all critical risk findings immediately",
                "Implement MFA across all administrative access",
                "Establish continuous compliance monitoring",
            ],
        )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Security Audit Demo")
    print("=" * 60)

    print("\n[1] Audit Planning")
    planner = AuditPlanner()
    plan = planner.create_plan(
        "Annual Security Audit 2024",
        ["IT infrastructure", "applications"],
        ["ISO 27001", "SOC 2"],
        30, 4,
    )
    print(f"  ID: {plan.audit_id}")
    print(f"  Controls: {plan.total_controls}")

    print("\n[2] Control Assessment")
    assessor = ControlAssessor()
    results = assessor.assess_controls(
        ["A.8.1.1", "A.8.1.2", "A.9.1.1"],
        [{"control": "A.8.1.1", "status": "pass", "evidence": "Inventory maintained"},
         {"control": "A.8.1.2", "status": "fail", "evidence": "No media policy"}],
    )
    for r in results:
        print(f"  {r.control_id}: {r.status.value} ({r.score}/100)")
    score = assessor.calculate_compliance_score(results)
    print(f"  Compliance: {score:.1f}%")

    print("\n[3] Compliance Mapping")
    mapper = ComplianceMapper()
    mapping = mapper.map_controls("internal", "SOC 2")
    print(f"  Mapped: {mapping.mapped_count}/{mapping.total_count}")
    print(f"  Coverage: {mapping.coverage_pct:.1f}%")

    print("\n[4] Risk Evaluation")
    evaluator = RiskEvaluator()
    risks = evaluator.evaluate([
        {"title": "Missing MFA", "likelihood": "high", "impact": "high"},
        {"title": "Unencrypted data", "likelihood": "medium", "impact": "critical"},
    ])
    for r in risks:
        print(f"  [{r.risk_level.value}] {r.title}: score={r.score}")

    print("\n[5] Audit Report")
    report = AuditReport()
    data = report.generate(plan, results, risks)
    print(f"  Title: {data.title}")
    print(f"  Score: {data.overall_score}")
    print(f"  Critical risks: {data.critical_risks}")

    print("\n" + "=" * 60)
    print("  Security audit demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
