"""
Compliance Framework
====================

Provides multi-framework control mapping, gap analysis, evidence collection,
control testing, and compliance reporting for SOC 2, ISO 27001, PCI DSS,
HIPAA, and NIST 800-53.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Framework(Enum):
    SOC2 = "SOC 2"
    ISO27001 = "ISO 27001"
    PCI_DSS = "PCI DSS"
    HIPAA = "HIPAA"
    GDPR = "GDPR"
    NIST_800_53 = "NIST 800-53"
    CIS = "CIS Benchmarks"


class ControlStatus(Enum):
    NOT_IMPLEMENTED = "not_implemented"
    PARTIALLY_IMPLEMENTED = "partially_implemented"
    IMPLEMENTED = "implemented"
    EFFECTIVE = "effective"
    NON_COMPLIANT = "non_compliant"


class EvidenceType(Enum):
    POLICY = "policy"
    PROCEDURE = "procedure"
    CONFIGURATION = "configuration"
    SCAN_REPORT = "scan_report"
    ACCESS_REVIEW = "access_review"
    AUDIT_LOG = "audit_log"
    SCREENSHOT = "screenshot"
    TEST_RESULT = "test_result"
    ATTESTATION = "attestation"


class TestResult(Enum):
    PASS = "pass"
    FAIL = "fail"
    PARTIAL = "partial"
    NOT_TESTED = "not_tested"


class GapPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Control:
    """A single security control."""
    control_id: str = ""
    title: str = ""
    description: str = ""
    implementation: str = ""
    framework_mappings: dict[Framework, list[str]] = field(default_factory=dict)
    evidence_sources: list[str] = field(default_factory=list)
    owner: str = ""
    review_frequency: str = "quarterly"
    status: ControlStatus = ControlStatus.NOT_IMPLEMENTED
    last_reviewed: str = ""
    next_review: str = ""
    notes: str = ""

    @property
    def frameworks(self) -> list[Framework]:
        return list(self.framework_mappings.keys())

    @property
    def control_ids_by_framework(self) -> dict[str, str]:
        result: dict[str, str] = {}
        for fw, ids in self.framework_mappings.items():
            result[fw.value] = ", ".join(ids)
        return result


@dataclass
class FrameworkRequirement:
    """A single requirement from a compliance framework."""
    framework: Framework = Framework.SOC2
    control_id: str = ""
    title: str = ""
    description: str = ""
    category: str = ""


@dataclass
class FrameworkCoverage:
    """Coverage metrics for a framework."""
    framework: Framework = Framework.SOC2
    total: int = 0
    implemented: int = 0
    partial: int = 0
    missing: int = 0

    @property
    def percentage(self) -> float:
        return (self.implemented / self.total * 100) if self.total > 0 else 0.0

    @property
    def overall_status(self) -> str:
        if self.percentage >= 95:
            return "audit-ready"
        elif self.percentage >= 80:
            return "mostly-compliant"
        elif self.percentage >= 50:
            return "partial"
        return "significant-gaps"


@dataclass
class GapAnalysisResult:
    """Result of a gap analysis."""
    target: Framework = Framework.SOC2
    implemented: int = 0
    partial: int = 0
    missing: int = 0
    total_requirements: int = 0
    missing_controls: list[GapItem] = field(default_factory=list)
    partial_controls: list[GapItem] = field(default_factory=list)

    @property
    def coverage_percentage(self) -> float:
        return ((self.implemented + self.partial * 0.5)
                / self.total_requirements * 100) if self.total_requirements > 0 else 0.0


@dataclass
class GapItem:
    """A single gap identified in analysis."""
    control_id: str = ""
    title: str = ""
    framework_requirement: str = ""
    priority: GapPriority = GapPriority.MEDIUM
    recommendation: str = ""


@dataclass
class EvidenceItem:
    """A single evidence artifact."""
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    evidence_type: EvidenceType = EvidenceType.CONFIGURATION
    system: str = ""
    description: str = ""
    collection_date: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    reviewer: str = ""
    file_path: str = ""
    hash_sha256: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditBundle:
    """Bundled evidence for an auditor."""
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    framework: Framework = Framework.SOC2
    period: str = ""
    auditor: str = ""
    evidence_items: list[EvidenceItem] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    path: str = ""
    size_mb: float = 0.0


@dataclass
class ComplianceStatus:
    """Overall compliance status for a framework."""
    framework: Framework = Framework.SOC2
    overall_posture: str = "unknown"
    implemented: int = 0
    total: int = 0
    last_audit_date: str = ""
    next_review_date: str = ""
    open_gaps: int = 0
    avg_evidence_age_days: float = 0.0
    coverage: Optional[FrameworkCoverage] = None


@dataclass
class ControlTest:
    """A control test result."""
    control_id: str = ""
    test_date: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    result: TestResult = TestResult.NOT_TESTED
    tester: str = ""
    findings: list[str] = field(default_factory=list)
    evidence_ids: list[str] = field(default_factory=list)


@dataclass
class PolicyDocument:
    """A managed policy document."""
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    title: str = ""
    version: str = "1.0"
    content_hash: str = ""
    last_reviewed: str = ""
    next_review: str = ""
    owner: str = ""
    status: str = "active"
    acknowledgments: list[str] = field(default_factory=list)
    mapped_controls: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Control Registry
# ---------------------------------------------------------------------------

class ControlRegistry:
    """Central registry of security controls with multi-framework mappings."""

    def __init__(self) -> None:
        self._controls: dict[str, Control] = {}

    def register_control(self, **kwargs: Any) -> Control:
        """Register a new control."""
        control = Control(**kwargs)
        self._controls[control.control_id] = control
        return control

    def get_control(self, control_id: str) -> Optional[Control]:
        return self._controls.get(control_id)

    def get_all_controls(self) -> list[Control]:
        return list(self._controls.values())

    def get_controls_for_framework(self, framework: Framework) -> list[Control]:
        return [
            c for c in self._controls.values()
            if framework in c.framework_mappings
        ]

    def get_framework_coverage(self, framework: Framework) -> FrameworkCoverage:
        """Calculate coverage for a specific framework."""
        relevant = self.get_controls_for_framework(framework)
        total = sum(
            len(c.framework_mappings.get(framework, []))
            for c in relevant
        )
        implemented = sum(
            1 for c in relevant
            if c.status in (ControlStatus.IMPLEMENTED, ControlStatus.EFFECTIVE)
        )
        partial = sum(
            1 for c in relevant
            if c.status == ControlStatus.PARTIALLY_IMPLEMENTED
        )
        missing = sum(
            1 for c in relevant
            if c.status in (ControlStatus.NOT_IMPLEMENTED,
                            ControlStatus.NON_COMPLIANT)
        )
        return FrameworkCoverage(
            framework=framework,
            total=total or len(relevant),
            implemented=implemented,
            partial=partial,
            missing=missing,
        )

    def get_frameworks_summary(self) -> dict[str, FrameworkCoverage]:
        """Get coverage for all frameworks."""
        summary: dict[str, FrameworkCoverage] = {}
        for fw in Framework:
            coverage = self.get_framework_coverage(fw)
            if coverage.total > 0:
                summary[fw.value] = coverage
        return summary


# ---------------------------------------------------------------------------
# Gap Analyzer
# ---------------------------------------------------------------------------

class GapAnalyzer:
    """Perform gap analysis against compliance frameworks."""

    def __init__(self, registry: ControlRegistry) -> None:
        self.registry = registry

    def analyze(self, target: Framework,
                requirements: list[FrameworkRequirement] | None = None
                ) -> GapAnalysisResult:
        """Run gap analysis against a target framework."""
        controls = self.registry.get_controls_for_framework(target)
        coverage = self.registry.get_framework_coverage(target)

        result = GapAnalysisResult(
            target=target,
            implemented=coverage.implemented,
            partial=coverage.partial,
            missing=coverage.missing,
            total_requirements=coverage.total,
        )

        # Identify missing controls
        for control in controls:
            fw_ids = control.framework_mappings.get(target, [])
            for cid in fw_ids:
                if control.status == ControlStatus.NOT_IMPLEMENTED:
                    result.missing_controls.append(GapItem(
                        control_id=cid,
                        title=control.title,
                        framework_requirement=f"{target.value} {cid}",
                        priority=GapPriority.HIGH,
                        recommendation=f"Implement: {control.description}",
                    ))
                elif control.status == ControlStatus.PARTIALLY_IMPLEMENTED:
                    result.partial_controls.append(GapItem(
                        control_id=cid,
                        title=control.title,
                        framework_requirement=f"{target.value} {cid}",
                        priority=GapPriority.MEDIUM,
                        recommendation=f"Complete implementation: {control.description}",
                    ))

        return result


# ---------------------------------------------------------------------------
# Evidence Collector
# ---------------------------------------------------------------------------

class EvidenceCollector:
    """Collect and manage audit evidence artifacts."""

    def __init__(self, storage_path: str = "./evidence") -> None:
        self.storage_path = storage_path
        self._evidence: list[EvidenceItem] = []

    def collect_access_review(self, system: str, review_date: str,
                              reviewer: str = "",
                              findings: str = "") -> EvidenceItem:
        """Record an access review as evidence."""
        item = EvidenceItem(
            evidence_type=EvidenceType.ACCESS_REVIEW,
            system=system,
            description=f"Access review: {findings}",
            collection_date=review_date,
            reviewer=reviewer,
        )
        self._evidence.append(item)
        return item

    def collect_configuration_export(self, system: str,
                                     config_path: str = "",
                                     compliance_check: str = "") -> EvidenceItem:
        """Record a configuration export as evidence."""
        item = EvidenceItem(
            evidence_type=EvidenceType.CONFIGURATION,
            system=system,
            description=f"Configuration export: {compliance_check}",
            file_path=config_path,
        )
        self._evidence.append(item)
        return item

    def collect_scan_report(self, scanner: str, target: str,
                            report_path: str = "",
                            summary: str = "") -> EvidenceItem:
        """Record a scan report as evidence."""
        item = EvidenceItem(
            evidence_type=EvidenceType.SCAN_REPORT,
            system=scanner,
            description=f"Scan of {target}: {summary}",
            file_path=report_path,
        )
        self._evidence.append(item)
        return item

    def collect_policy(self, title: str, version: str = "1.0",
                       owner: str = "") -> EvidenceItem:
        """Record a policy document as evidence."""
        item = EvidenceItem(
            evidence_type=EvidenceType.POLICY,
            system="policy",
            description=f"Policy: {title} v{version}",
            reviewer=owner,
        )
        self._evidence.append(item)
        return item

    def collect_audit_log(self, system: str, log_path: str = "",
                          description: str = "") -> EvidenceItem:
        """Record audit log as evidence."""
        item = EvidenceItem(
            evidence_type=EvidenceType.AUDIT_LOG,
            system=system,
            description=description or f"Audit log from {system}",
            file_path=log_path,
        )
        self._evidence.append(item)
        return item

    def get_all_evidence(self) -> list[EvidenceItem]:
        return list(self._evidence)

    def create_audit_bundle(self, framework: Framework, period: str,
                            auditor: str = "",
                            evidence_items: list[EvidenceItem] | None = None
                            ) -> AuditBundle:
        """Bundle evidence for auditor delivery."""
        items = evidence_items or self._evidence
        return AuditBundle(
            framework=framework,
            period=period,
            auditor=auditor,
            evidence_items=items,
            path=f"{self.storage_path}/{framework.value}/{period}",
            size_mb=len(items) * 0.05,  # Estimate
        )


# ---------------------------------------------------------------------------
# Control Tester
# ---------------------------------------------------------------------------

class ControlTester:
    """Schedule and execute control tests."""

    def __init__(self, registry: ControlRegistry) -> None:
        self.registry = registry
        self._tests: list[ControlTest] = []

    def test_control(self, control_id: str, result: TestResult,
                     tester: str = "", findings: list[str] | None = None
                     ) -> ControlTest:
        """Record a control test result."""
        test = ControlTest(
            control_id=control_id,
            result=result,
            tester=tester,
            findings=findings or [],
        )
        self._tests.append(test)

        # Update control status based on test result
        control = self.registry.get_control(control_id)
        if control:
            if result == TestResult.PASS:
                control.status = ControlStatus.EFFECTIVE
            elif result == TestResult.FAIL:
                control.status = ControlStatus.NON_COMPLIANT
            control.last_reviewed = test.test_date

        return test

    def get_all_tests(self) -> list[ControlTest]:
        return list(self._tests)

    def get_failing_tests(self) -> list[ControlTest]:
        return [t for t in self._tests if t.result == TestResult.FAIL]

    def get_compliance_rate(self) -> float:
        if not self._tests:
            return 0.0
        passing = sum(1 for t in self._tests if t.result == TestResult.PASS)
        return passing / len(self._tests)


# ---------------------------------------------------------------------------
# Compliance Dashboard
# ---------------------------------------------------------------------------

class ComplianceDashboard:
    """Generate compliance posture reports and dashboards."""

    def __init__(self, registry: ControlRegistry,
                 evidence_collector: EvidenceCollector | None = None) -> None:
        self.registry = registry
        self.evidence = evidence_collector

    def get_status(self, framework: Framework) -> ComplianceStatus:
        """Get compliance status for a framework."""
        coverage = self.registry.get_framework_coverage(framework)
        controls = self.registry.get_controls_for_framework(framework)

        # Calculate evidence age
        evidence_age = 0.0
        if self.evidence:
            all_evidence = self.evidence.get_all_evidence()
            if all_evidence:
                ages = []
                for e in all_evidence:
                    try:
                        collected = datetime.fromisoformat(e.collection_date)
                        age = (datetime.utcnow() - collected).days
                        ages.append(age)
                    except (ValueError, TypeError):
                        pass
                evidence_age = sum(ages) / len(ages) if ages else 0.0

        open_gaps = sum(
            1 for c in controls
            if c.status in (ControlStatus.NOT_IMPLEMENTED,
                            ControlStatus.PARTIALLY_IMPLEMENTED,
                            ControlStatus.NON_COMPLIANT)
        )

        return ComplianceStatus(
            framework=framework,
            overall_posture=coverage.overall_status,
            implemented=coverage.implemented,
            total=coverage.total,
            open_gaps=open_gaps,
            avg_evidence_age_days=evidence_age,
            coverage=coverage,
        )

    def generate_executive_summary(self) -> dict[str, Any]:
        """Generate an executive summary across all frameworks."""
        frameworks_status: dict[str, Any] = {}
        for fw in Framework:
            status = self.get_status(fw)
            if status.total > 0:
                frameworks_status[fw.value] = {
                    "posture": status.overall_posture,
                    "coverage": f"{status.implemented}/{status.total}",
                    "open_gaps": status.open_gaps,
                }
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "frameworks": frameworks_status,
            "total_controls": len(self.registry.get_all_controls()),
        }


# ---------------------------------------------------------------------------
# Policy Manager
# ---------------------------------------------------------------------------

class PolicyManager:
    """Manage security policy documents."""

    def __init__(self) -> None:
        self._policies: dict[str, PolicyDocument] = {}

    def create_policy(self, title: str, version: str = "1.0",
                      owner: str = "",
                      mapped_controls: list[str] | None = None) -> PolicyDocument:
        """Create a new policy document."""
        policy = PolicyDocument(
            title=title, version=version, owner=owner,
            mapped_controls=mapped_controls or [],
            last_reviewed=datetime.utcnow().isoformat(),
            next_review=(datetime.utcnow() + timedelta(days=365)).isoformat(),
        )
        self._policies[policy.id] = policy
        return policy

    def get_policy(self, policy_id: str) -> Optional[PolicyDocument]:
        return self._policies.get(policy_id)

    def get_all_policies(self) -> list[PolicyDocument]:
        return list(self._policies.values())

    def get_expiring_policies(self, within_days: int = 30) -> list[PolicyDocument]:
        """Get policies that need review within N days."""
        cutoff = datetime.utcnow() + timedelta(days=within_days)
        return [
            p for p in self._policies.values()
            if p.next_review
            and datetime.fromisoformat(p.next_review) <= cutoff
        ]

    def record_acknowledgment(self, policy_id: str, user: str) -> None:
        """Record that a user acknowledged a policy."""
        policy = self._policies.get(policy_id)
        if policy and user not in policy.acknowledgments:
            policy.acknowledgments.append(user)

    def get_acknowledgment_rate(self, policy_id: str,
                                total_users: int) -> float:
        """Calculate acknowledgment rate for a policy."""
        policy = self._policies.get(policy_id)
        if not policy or total_users == 0:
            return 0.0
        return len(policy.acknowledgments) / total_users


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the compliance framework."""
    print("=" * 60)
    print("  Compliance Framework Demo")
    print("=" * 60)

    # --- Control Registry ---
    print("\n--- Control Registry ---")
    registry = ControlRegistry()

    registry.register_control(
        control_id="SC-001", title="SSH Key Rotation",
        description="All SSH keys rotated every 90 days",
        implementation="Automated via Ansible",
        framework_mappings={
            Framework.SOC2: ["CC6.1", "CC6.3"],
            Framework.ISO27001: ["A.9.4.2", "A.9.4.3"],
            Framework.PCI_DSS: ["2.2", "8.2.4"],
            Framework.NIST_800_53: ["IA-5(1)"],
        },
        evidence_sources=["ansible_logs", "vault_audit"],
        owner="platform-team",
        status=ControlStatus.IMPLEMENTED,
    )
    registry.register_control(
        control_id="SC-002", title="Access Review",
        description="Quarterly access reviews for all systems",
        implementation="Manual review with Jira tracking",
        framework_mappings={
            Framework.SOC2: ["CC6.1"],
            Framework.ISO27001: ["A.9.2.5"],
            Framework.PCI_DSS: ["7.2.1"],
        },
        evidence_sources=["jira_tickets", "access_exports"],
        owner="security-team",
        status=ControlStatus.IMPLEMENTED,
    )
    registry.register_control(
        control_id="SC-003", title="Incident Response Plan",
        description="Documented IR plan with annual testing",
        implementation="Draft stage — not yet implemented",
        framework_mappings={
            Framework.SOC2: ["CC7.3"],
            Framework.ISO27001: ["A.16.1"],
        },
        owner="ciso",
        status=ControlStatus.NOT_IMPLEMENTED,
    )

    print(f"  Controls registered: {len(registry.get_all_controls())}")

    # --- Framework Coverage ---
    print("\n--- Framework Coverage ---")
    for fw in [Framework.SOC2, Framework.ISO27001, Framework.PCI_DSS]:
        coverage = registry.get_framework_coverage(fw)
        print(f"  {fw.value:12s}: {coverage.percentage:.0f}% "
              f"({coverage.implemented}/{coverage.total}) "
              f"[{coverage.overall_status}]")

    # --- Gap Analysis ---
    print("\n--- Gap Analysis (PCI DSS) ---")
    analyzer = GapAnalyzer(registry)
    gap_report = analyzer.analyze(target=Framework.PCI_DSS)
    print(f"  Implemented: {gap_report.implemented}")
    print(f"  Partial:     {gap_report.partial}")
    print(f"  Missing:     {gap_report.missing}")
    print(f"  Coverage:    {gap_report.coverage_percentage:.0f}%")
    for gap in gap_report.missing_controls:
        print(f"  GAP: {gap.control_id} - {gap.title} "
              f"({gap.priority.value})")

    # --- Evidence Collection ---
    print("\n--- Evidence Collection ---")
    collector = EvidenceCollector(storage_path="./evidence/2024-Q1")
    e1 = collector.collect_access_review(
        system="AWS IAM", review_date="2024-01-15",
        reviewer="security-team", findings="No excessive permissions"
    )
    e2 = collector.collect_configuration_export(
        system="nginx", compliance_check="TLS 1.2+ enforced"
    )
    e3 = collector.collect_scan_report(
        scanner="trivy", target="web-prod-01",
        summary="0 critical, 2 high, 15 medium"
    )
    e4 = collector.collect_audit_log(
        system="cloudtrail", description="CloudTrail audit logs"
    )

    print(f"  Evidence items: {len(collector.get_all_evidence())}")

    bundle = collector.create_audit_bundle(
        framework=Framework.SOC2, period="2024-Q1", auditor="Deloitte"
    )
    print(f"  Audit bundle: {bundle.path} ({bundle.size_mb:.1f} MB)")

    # --- Control Testing ---
    print("\n--- Control Testing ---")
    tester = ControlTester(registry)
    tester.test_control("SC-001", TestResult.PASS, tester="auditor")
    tester.test_control("SC-002", TestResult.PASS, tester="auditor")
    tester.test_control("SC-003", TestResult.FAIL, tester="auditor",
                         findings=["Not implemented", "No IR plan documented"])

    print(f"  Tests run:     {len(tester.get_all_tests())}")
    print(f"  Compliance:    {tester.get_compliance_rate():.0%}")
    print(f"  Failing tests: {len(tester.get_failing_tests())}")

    # --- Dashboard ---
    print("\n--- Compliance Dashboard ---")
    dashboard = ComplianceDashboard(registry, collector)
    for fw in [Framework.SOC2, Framework.ISO27001, Framework.PCI_DSS]:
        status = dashboard.get_status(fw)
        print(f"\n  {fw.value}:")
        print(f"    Posture:      {status.overall_posture}")
        print(f"    Controls:     {status.implemented}/{status.total}")
        print(f"    Open gaps:    {status.open_gaps}")
        print(f"    Evidence age: {status.avg_evidence_age_days:.0f} days")

    # --- Executive Summary ---
    summary = dashboard.generate_executive_summary()
    print(f"\n  Executive Summary:")
    print(f"    Total controls: {summary['total_controls']}")
    for fw_name, fw_data in summary["frameworks"].items():
        print(f"    {fw_name}: {fw_data['posture']} "
              f"({fw_data['coverage']})")

    # --- Policy Management ---
    print("\n--- Policy Management ---")
    pm = PolicyManager()
    p1 = pm.create_policy("Acceptable Use Policy", "2.0",
                           owner="hr", mapped_controls=["SC-002"])
    p2 = pm.create_policy("Incident Response Policy", "1.0",
                           owner="ciso", mapped_controls=["SC-003"])

    pm.record_acknowledgment(p1.id, "alice")
    pm.record_acknowledgment(p1.id, "bob")
    pm.record_acknowledgment(p1.id, "charlie")

    print(f"  Policies: {len(pm.get_all_policies())}")
    print(f"  AUP ack rate: {pm.get_acknowledgment_rate(p1.id, 10):.0%}")

    print("\n" + "=" * 60)
    print("  Demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
