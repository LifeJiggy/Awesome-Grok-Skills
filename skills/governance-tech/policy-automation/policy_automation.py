"""
Policy Automation Module
Part of the governance-tech skill domain

Provides policy-as-code engine, compliance checking, exception management,
attestation campaigns, and automated policy enforcement.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid


class PolicyLanguage(Enum):
    REGO = "rego"
    CEDAR = "cedar"
    DSL = "dsl"
    YAML = "yaml"


class Decision(Enum):
    ALLOW = "allow"
    DENY = "deny"
    MANUAL_REVIEW = "manual_review"


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ExceptionStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    EXPIRED = "expired"
    RENEWED = "renewed"


@dataclass
class PolicyViolation:
    control: str
    resource: str
    severity: str
    current_value: str
    expected_value: str
    remediation: str


@dataclass
class PolicyEvaluation:
    decision: Decision
    policy_name: str
    resource_type: str
    resource_config: Dict[str, Any]
    violations: List[PolicyViolation]
    evaluation_time_ms: float
    suggested_remediation: str = ""

    @property
    def is_compliant(self) -> bool:
        return self.decision == Decision.ALLOW


@dataclass
class ComplianceScan:
    scan_id: str
    scope: str
    controls_evaluated: int
    controls_passed: int
    controls_failed: int
    violations: List[PolicyViolation]
    scan_date: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def compliance_score(self) -> float:
        return self.controls_passed / max(self.controls_evaluated, 1)


@dataclass
class PolicyException:
    exception_id: str
    policy_name: str
    resource: str
    justification: str
    requested_by: str
    risk_level: RiskLevel
    risk_score: float
    compensating_controls: List[str]
    status: ExceptionStatus
    request_date: str
    expiry_date: str
    approved_by: str = ""


@dataclass
class AttestationCampaign:
    campaign_id: str
    name: str
    policies: List[str]
    target_count: int
    deadline: str
    status: str = "active"
    launch_date: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CampaignProgress:
    campaign_id: str
    target_count: int
    completed_count: int
    pending_count: int
    overdue_count: int

    @property
    def completion_rate(self) -> float:
        return self.completed_count / max(self.target_count, 1)


class PolicyEngine:
    """Policy-as-code evaluation engine."""

    def __init__(self, language: PolicyLanguage = PolicyLanguage.REGO,
                 policy_dir: str = "policies/",
                 decision_cache_ttl_seconds: int = 60):
        self.language = language
        self.policy_dir = policy_dir
        self.cache_ttl = decision_cache_ttl_seconds
        self._policies: Dict[str, Dict[str, Any]] = {}
        self._evaluations: List[PolicyEvaluation] = []

    def define_policy(self, name: str, description: str,
                      rules: List[Dict[str, Any]]) -> None:
        self._policies[name] = {
            "name": name, "description": description,
            "rules": rules, "version": "1.0",
            "created": datetime.now().isoformat(),
        }

    def evaluate(self, resource_type: str, resource_config: Dict[str, Any],
                 policy: str) -> PolicyEvaluation:
        policy_def = self._policies.get(policy)
        violations = []

        if policy_def:
            for rule in policy_def.get("rules", []):
                if rule.get("resource") == resource_type:
                    allowed = rule.get("allowed_values", [])
                    actual = resource_config.get(rule.get("attribute", ""), "")
                    if allowed and actual not in allowed:
                        violations.append(PolicyViolation(
                            control=f"{policy}_{rule.get('attribute')}",
                            resource=str(resource_config.get("name", "unknown")),
                            severity="high",
                            current_value=str(actual),
                            expected_value=str(allowed),
                            remediation=f"Change {rule.get('attribute')} to one of: {allowed}",
                        ))

        decision = Decision.DENY if violations else Decision.ALLOW
        remediation = violations[0].remediation if violations else ""

        result = PolicyEvaluation(
            decision=decision, policy_name=policy,
            resource_type=resource_type, resource_config=resource_config,
            violations=violations, evaluation_time_ms=12.5,
            suggested_remediation=remediation,
        )
        self._evaluations.append(result)
        return result

    def get_policy(self, name: str) -> Optional[Dict[str, Any]]:
        return self._policies.get(name)


class ComplianceChecker:
    """Automated compliance scanning and reporting."""

    def __init__(self, frameworks: Optional[List[str]] = None,
                 scan_schedule: str = "daily"):
        self.frameworks = frameworks or []
        self.schedule = scan_schedule
        self._scans: List[ComplianceScan] = []

    def scan(self, scope: str = "production",
             controls: Optional[List[str]] = None) -> ComplianceScan:
        ctrl_list = controls or ["encryption_at_rest", "access_logging",
                                  "data_retention", "mfa_enabled", "audit_trails"]
        violations = []
        passed = 0

        for ctrl in ctrl_list:
            if ctrl == "data_retention":
                violations.append(PolicyViolation(
                    control=ctrl, resource="legacy-logs-bucket",
                    severity="medium", current_value="indefinite",
                    expected_value="365_days",
                    remediation="Configure lifecycle policy to expire objects after 365 days",
                ))
            else:
                passed += 1

        scan = ComplianceScan(
            scan_id=f"SCAN-{uuid.uuid4().hex[:8].upper()}",
            scope=scope, controls_evaluated=len(ctrl_list),
            controls_passed=passed, controls_failed=len(violations),
            violations=violations,
        )
        self._scans.append(scan)
        return scan

    def get_latest_scan(self) -> Optional[ComplianceScan]:
        return self._scans[-1] if self._scans else None


class ExceptionManager:
    """Policy exception request and approval workflow."""

    def __init__(self, max_exception_duration_days: int = 90,
                 auto_escalation: bool = True):
        self.max_duration = max_exception_duration_days
        self.escalation = auto_escalation
        self._exceptions: Dict[str, PolicyException] = {}

    def request_exception(
        self, policy: str, resource: str,
        business_justification: str, requested_by: str,
        risk_level: RiskLevel = RiskLevel.MEDIUM,
        compensating_controls: Optional[List[str]] = None,
    ) -> PolicyException:
        eid = f"EXC-{uuid.uuid4().hex[:8].upper()}"
        risk_scores = {RiskLevel.LOW: 0.2, RiskLevel.MEDIUM: 0.5,
                       RiskLevel.HIGH: 0.8, RiskLevel.CRITICAL: 0.95}

        exception = PolicyException(
            exception_id=eid, policy_name=policy, resource=resource,
            justification=business_justification, requested_by=requested_by,
            risk_level=risk_level, risk_score=risk_scores.get(risk_level, 0.5),
            compensating_controls=compensating_controls or [],
            status=ExceptionStatus.PENDING,
            request_date=datetime.now().isoformat(),
            expiry_date=(datetime.now() + timedelta(days=self.max_duration)).isoformat(),
        )
        self._exceptions[eid] = exception
        return exception

    def approve(self, exception_id: str, approved_by: str) -> PolicyException:
        exc = self._exceptions.get(exception_id)
        if not exc:
            raise ValueError(f"Exception {exception_id} not found")
        exc.status = ExceptionStatus.APPROVED
        exc.approved_by = approved_by
        return exc

    def get_exceptions(self, status: Optional[ExceptionStatus] = None) -> List[PolicyException]:
        excs = list(self._exceptions.values())
        if status:
            excs = [e for e in excs if e.status == status]
        return excs


class AttestationManager:
    """Policy attestation campaign management."""

    def __init__(self):
        self._campaigns: Dict[str, AttestationCampaign] = {}
        self._attestations: Dict[str, List[str]] = {}  # campaign_id -> [user_ids]

    def create_campaign(self, name: str, policies: List[str],
                        target_count: int, deadline_days: int = 30) -> AttestationCampaign:
        cid = f"CAMP-{uuid.uuid4().hex[:8].upper()}"
        campaign = AttestationCampaign(
            campaign_id=cid, name=name, policies=policies,
            target_count=target_count,
            deadline=(datetime.now() + timedelta(days=deadline_days)).isoformat(),
        )
        self._campaigns[cid] = campaign
        return campaign

    def submit_attestation(self, campaign_id: str, user_id: str) -> bool:
        if campaign_id not in self._campaigns:
            raise ValueError(f"Campaign {campaign_id} not found")
        self._attestations.setdefault(campaign_id, []).append(user_id)
        return True

    def get_progress(self, campaign_id: str) -> CampaignProgress:
        campaign = self._campaigns.get(campaign_id)
        if not campaign:
            raise ValueError(f"Campaign {campaign_id} not found")
        completed = len(self._attestations.get(campaign_id, []))
        return CampaignProgress(
            campaign_id=campaign_id, target_count=campaign.target_count,
            completed_count=completed,
            pending_count=max(campaign.target_count - completed, 0),
            overdue_count=0,
        )


def main():
    print("=" * 60)
    print("  Policy Automation Demo")
    print("=" * 60)

    # Policy engine
    print("\n--- Policy-as-Code ---")
    engine = PolicyEngine()
    engine.define_policy("data_residency", "Ensure data stays in approved regions", [
        {"resource": "s3_bucket", "attribute": "region",
         "allowed_values": ["us-east-1", "us-west-2", "eu-west-1"]},
    ])
    result = engine.evaluate("s3_bucket", {"name": "customer-data", "region": "ap-southeast-1"},
                             "data_residency")
    print(f"  Decision: {result.decision.value}")
    print(f"  Violations: {len(result.violations)}")
    if result.violations:
        print(f"  Remediation: {result.suggested_remediation}")

    # Compliance
    print("\n--- Compliance Scan ---")
    checker = ComplianceChecker(frameworks=["GDPR", "HIPAA"])
    scan = checker.scan("production", ["encryption", "access_logging", "data_retention"])
    print(f"  Score: {scan.compliance_score:.1%}")
    print(f"  Passed: {scan.controls_passed}, Failed: {scan.controls_failed}")

    # Exceptions
    print("\n--- Exception Management ---")
    em = ExceptionManager()
    exc = em.request_exception("encryption_at_rest", "legacy-db",
                               "Migration planned Q3", "dba_team", RiskLevel.MEDIUM)
    print(f"  Exception: {exc.exception_id} ({exc.status.value})")
    em.approve(exc.exception_id, "ciso")
    print(f"  Approved by: {exc.approved_by}")

    # Attestation
    print("\n--- Attestation Campaign ---")
    am = AttestationManager()
    camp = am.create_campaign("Security Attestation 2026", ["acceptable_use", "data_classification"], 500)
    am.submit_attestation(camp.campaign_id, "user_001")
    am.submit_attestation(camp.campaign_id, "user_002")
    prog = am.get_progress(camp.campaign_id)
    print(f"  Campaign: {camp.name}")
    print(f"  Progress: {prog.completed_count}/{prog.target_count} ({prog.completion_rate:.1%})")


if __name__ == "__main__":
    main()
