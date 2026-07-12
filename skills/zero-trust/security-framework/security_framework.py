"""
Zero Trust Security Framework Module

Implements NIST SP 800-207 aligned zero trust architecture with trust engines,
policy decision points, policy enforcement points, and security posture assessment.
"""

from __future__ import annotations

import hashlib
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Optional


class ResourceType(Enum):
    API_ENDPOINT = auto()
    DATABASE = auto()
    FILE_SHARE = auto()
    WEB_APPLICATION = auto()
    MICROSERVICE = auto()
    NETWORK_SEGMENT = auto()


class TrustAlgorithm(Enum):
    WEIGHTED_SUM = "weighted_sum"
    MINIMUM_THRESHOLD = "minimum_threshold"
    WEIGHTED_AVERAGE = "weighted_average"
    MANDATORY_SIGNALS = "mandatory_signals"


class AccessDecision(Enum):
    ALLOW = "allow"
    DENY = "deny"
    STEP_UP = "step_up"
    CONDITIONAL = "conditional"


class EnforcementMode(Enum):
    STRICT = "strict"
    PERMISSIVE = "permissive"
    MONITOR_ONLY = "monitor_only"


class MaturityLevel(Enum):
    INITIAL = 1
    DEVELOPING = 2
    DEFINED = 3
    MANAGED = 4
    OPTIMIZING = 5


@dataclass
class TrustSignal:
    signal_type: str
    value: str
    weight: float = 1.0
    confidence: float = 1.0
    timestamp: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def effective_weight(self) -> float:
        return self.weight * self.confidence

    def is_stale(self, max_age_seconds: float = 300.0) -> bool:
        return (time.time() - self.timestamp) > max_age_seconds


@dataclass
class PolicyRule:
    rule_id: str
    subject_pattern: str
    resource_pattern: str
    action: str
    conditions: dict[str, Any] = field(default_factory=dict)
    effect: AccessDecision = AccessDecision.DENY
    priority: int = 0
    enabled: bool = True


@dataclass
class AccessDecisionResult:
    granted: bool
    decision: AccessDecision
    trust_score: float
    matched_rules: list[str]
    reason: str
    evaluated_at: float = field(default_factory=time.time)
    request_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MicroPerimeter:
    perimeter_id: str
    resources: list[str]
    enforcement_mode: EnforcementMode
    default_action: AccessDecision = AccessDecision.DENY
    required_trust_level: float = 0.7
    exceptions: list[dict[str, Any]] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)


@dataclass
class PostureGap:
    gap_id: str
    category: str
    severity: str
    description: str
    current_state: str
    target_state: str
    remediation: str
    nist_reference: str = ""


@dataclass
class PostureAssessment:
    assessment_id: str
    scope: str
    framework: str
    maturity_level: MaturityLevel
    score: float
    gaps: list[PostureGap]
    recommendations: list[str]
    assessed_at: float = field(default_factory=time.time)


class TrustEngine:
    def __init__(
        self,
        algorithm: TrustAlgorithm = TrustAlgorithm.WEIGHTED_SUM,
        default_threshold: float = 0.7,
    ):
        self.algorithm = algorithm
        self.default_threshold = default_threshold
        self.signal_validators: dict[str, Callable[[TrustSignal], bool]] = {}
        self._score_cache: dict[str, tuple[float, float]] = {}

    def register_signal_validator(
        self, signal_type: str, validator: Callable[[TrustSignal], bool]
    ) -> None:
        self.signal_validators[signal_type] = validator

    def compute_trust_score(
        self,
        signals: list[TrustSignal],
        context: dict[str, Any] | None = None,
    ) -> float:
        valid_signals = []
        for signal in signals:
            if signal.is_stale(max_age_seconds=300):
                continue
            validator = self.signal_validators.get(signal.signal_type)
            if validator and not validator(signal):
                continue
            valid_signals.append(signal)

        if not valid_signals:
            return 0.0

        if self.algorithm == TrustAlgorithm.WEIGHTED_SUM:
            return self._weighted_sum(valid_signals)
        elif self.algorithm == TrustAlgorithm.MINIMUM_THRESHOLD:
            return self._minimum_signal(valid_signals)
        elif self.algorithm == TrustAlgorithm.WEIGHTED_AVERAGE:
            return self._weighted_average(valid_signals)
        elif self.algorithm == TrustAlgorithm.MANDATORY_SIGNALS:
            return self._mandatory_check(valid_signals, context or {})
        return 0.0

    def _weighted_sum(self, signals: list[TrustSignal]) -> float:
        total_weight = sum(s.effective_weight for s in signals)
        if total_weight == 0:
            return 0.0
        weighted_value = sum(
            self._normalize_signal(s) * s.effective_weight for s in signals
        )
        return min(weighted_value / total_weight, 1.0)

    def _minimum_signal(self, signals: list[TrustSignal]) -> float:
        if not signals:
            return 0.0
        return min(self._normalize_signal(s) for s in signals)

    def _weighted_average(self, signals: list[TrustSignal]) -> float:
        if not signals:
            return 0.0
        normalized = [self._normalize_signal(s) for s in signals]
        return sum(normalized) / len(normalized)

    def _mandatory_check(
        self, signals: list[TrustSignal], context: dict[str, Any]
    ) -> float:
        mandatory = context.get("mandatory_signal_types", set())
        present_types = {s.signal_type for s in signals}
        if mandatory and not mandatory.issubset(present_types):
            return 0.0
        return self._weighted_average(signals)

    def _normalize_signal(self, signal: TrustSignal) -> float:
        positive_values = {
            "verified", "compliant", "normal", "trusted",
            "strong", "valid", "approved", "healthy",
        }
        negative_values = {
            "failed", "non_compliant", "anomalous", "untrusted",
            "weak", "invalid", "revoked", "unhealthy",
        }
        value_lower = signal.value.lower()
        if value_lower in positive_values:
            return 0.9
        elif value_lower in negative_values:
            return 0.1
        elif value_lower == "unknown":
            return 0.3
        return 0.5

    def invalidate_cache(self, subject: str) -> None:
        self._score_cache.pop(subject, None)


class PolicyStore:
    def __init__(self) -> None:
        self._rules: dict[str, PolicyRule] = {}
        self._perimeters: dict[str, MicroPerimeter] = {}
        self._decision_log: list[AccessDecisionResult] = []

    def add_rule(self, rule: PolicyRule) -> None:
        self._rules[rule.rule_id] = rule

    def remove_rule(self, rule_id: str) -> bool:
        return self._rules.pop(rule_id, None) is not None

    def get_rules_for_resource(self, resource: str) -> list[PolicyRule]:
        import fnmatch
        return [
            r for r in self._rules.values()
            if r.enabled and fnmatch.fnmatch(resource, r.resource_pattern)
        ]

    def add_perimeter(self, perimeter: MicroPerimeter) -> None:
        self._perimeters[perimeter.perimeter_id] = perimeter

    def log_decision(self, decision: AccessDecisionResult) -> None:
        self._decision_log.append(decision)

    def get_decision_history(
        self, subject: str | None = None, limit: int = 100
    ) -> list[AccessDecisionResult]:
        results = self._decision_log
        if subject:
            results = [d for d in results if subject in d.metadata.get("subject", "")]
        return results[-limit:]


class PostureAssessor:
    NIST_800_207_CRITERIA = [
        ("identity", "MFA enforced", "multi-factor authentication required for all users"),
        ("device", "Device health check", "device posture validated before access"),
        ("network", "Micro-segmentation", "network segmented with least-privilege policies"),
        ("application", "Application isolation", "applications run in isolated containers"),
        ("data", "Data classification", "sensitive data classified and encrypted at rest"),
        ("visibility", "Centralized logging", "all access decisions logged and auditable"),
        ("automation", "Automated response", "automated threat response and remediation"),
    ]

    def assess(
        self, scope: str, framework: str = "NIST_800_207"
    ) -> PostureAssessment:
        gaps: list[PostureGap] = []
        score = 1.0

        for category, title, description in self.NIST_800_207_CRITERIA:
            gap = PostureGap(
                gap_id=f"GAP-{uuid.uuid4().hex[:8]}",
                category=category,
                severity="high",
                description=f"{title}: {description}",
                current_state="not_implemented",
                target_state="fully_implemented",
                remediation=f"Implement {category} controls per NIST 800-207 guidance",
                nist_reference=f"NIST SP 800-207 §{category.upper()}",
            )
            gaps.append(gap)
            score -= 0.12

        maturity = MaturityLevel.DEVELOPING
        if score > 0.8:
            maturity = MaturityLevel.MANAGED
        elif score > 0.6:
            maturity = MaturityLevel.DEFINED

        recommendations = [
            "Prioritize identity verification as the foundation of zero trust",
            "Implement device health attestation before granting network access",
            "Deploy micro-segmentation around high-value assets first",
        ]

        return PostureAssessment(
            assessment_id=uuid.uuid4().hex[:12],
            scope=scope,
            framework=framework,
            maturity_level=maturity,
            score=max(score, 0.0),
            gaps=gaps,
            recommendations=recommendations,
        )


class ZeroTrustEngine:
    def __init__(
        self,
        policy_store: str = "in_memory",
        trust_algorithm: str = "weighted_sum",
        default_deny: bool = True,
    ):
        self.trust_engine = TrustEngine(
            algorithm=TrustAlgorithm(trust_algorithm),
            default_threshold=0.7,
        )
        self.policy_store = PolicyStore()
        self.assessor = PostureAssessor()
        self.default_deny = default_deny
        self._resources: dict[str, dict[str, Any]] = {}

    def register_resource(
        self,
        resource_id: str,
        resource_type: ResourceType,
        classification: str = "internal",
        owner_team: str = "platform",
        required_trust_level: float = 0.7,
    ) -> dict[str, Any]:
        resource = {
            "resource_id": resource_id,
            "resource_type": resource_type,
            "classification": classification,
            "owner_team": owner_team,
            "required_trust_level": required_trust_level,
            "registered_at": time.time(),
        }
        self._resources[resource_id] = resource
        return resource

    def evaluate_access(
        self,
        subject: str,
        resource: str,
        action: str,
        context_signals: list[TrustSignal] | None = None,
    ) -> AccessDecisionResult:
        signals = context_signals or []
        trust_score = self.trust_engine.compute_trust_score(signals)

        resource_config = self._resources.get(resource, {})
        required_level = resource_config.get("required_trust_level", 0.7)

        matched_rules: list[str] = []
        effective_decision = AccessDecision.DENY if self.default_deny else AccessDecision.ALLOW

        rules = self.policy_store.get_rules_for_resource(resource)
        for rule in sorted(rules, key=lambda r: r.priority, reverse=True):
            if self._subject_matches(subject, rule.subject_pattern):
                if action == rule.action or rule.action == "*":
                    matched_rules.append(rule.rule_id)
                    effective_decision = rule.effect
                    break

        granted = trust_score >= required_level and effective_decision == AccessDecision.ALLOW

        if not granted and trust_score >= (required_level * 0.8):
            effective_decision = AccessDecision.STEP_UP
            granted = False

        result = AccessDecisionResult(
            granted=granted,
            decision=effective_decision,
            trust_score=trust_score,
            matched_rules=matched_rules,
            reason=f"Trust score {trust_score:.2f} vs required {required_level:.2f}",
            metadata={"subject": subject, "resource": resource, "action": action},
        )

        self.policy_store.log_decision(result)
        return result

    def _subject_matches(self, subject: str, pattern: str) -> bool:
        import fnmatch
        return fnmatch.fnmatch(subject, pattern)

    def define_micro_perimeter(
        self,
        perimeter_id: str,
        resources: list[str],
        enforcement_mode: str = "strict",
        default_action: str = "deny",
        exceptions: list[dict[str, Any]] | None = None,
    ) -> MicroPerimeter:
        perimeter = MicroPerimeter(
            perimeter_id=perimeter_id,
            resources=resources,
            enforcement_mode=EnforcementMode(enforcement_mode),
            default_action=AccessDecision(default_action),
            exceptions=exceptions or [],
        )
        self.policy_store.add_perimeter(perimeter)
        return perimeter

    def assess_posture(
        self,
        scope: str,
        framework: str = "NIST_800_207",
        include_recommendations: bool = True,
    ) -> PostureAssessment:
        return self.assessor.assess(scope, framework)

    def add_policy_rule(
        self,
        rule_id: str,
        subject_pattern: str,
        resource_pattern: str,
        action: str,
        effect: str = "allow",
        priority: int = 0,
    ) -> PolicyRule:
        rule = PolicyRule(
            rule_id=rule_id,
            subject_pattern=subject_pattern,
            resource_pattern=resource_pattern,
            action=action,
            effect=AccessDecision(effect),
            priority=priority,
        )
        self.policy_store.add_rule(rule)
        return rule

    def get_audit_log(
        self, subject: str | None = None, limit: int = 50
    ) -> list[AccessDecisionResult]:
        return self.policy_store.get_decision_history(subject, limit)


def main() -> None:
    print("=" * 60)
    print("Zero Trust Security Framework — Demo")
    print("=" * 60)

    engine = ZeroTrustEngine(
        trust_algorithm="weighted_sum",
        default_deny=True,
    )

    resource = engine.register_resource(
        resource_id="api-payments-001",
        resource_type=ResourceType.API_ENDPOINT,
        classification="confidential",
        owner_team="payments",
        required_trust_level=0.80,
    )
    print(f"\nRegistered resource: {resource['resource_id']}")

    engine.add_policy_rule(
        rule_id="allow-payments-read",
        subject_pattern="user:alice@corp.com",
        resource_pattern="api-payments-*",
        action="read",
        effect="allow",
        priority=10,
    )

    signals = [
        TrustSignal(signal_type="identity", value="verified", weight=0.30),
        TrustSignal(signal_type="device_health", value="compliant", weight=0.25),
        TrustSignal(signal_type="network_location", value="corporate", weight=0.20),
        TrustSignal(signal_type="behavior", value="normal", weight=0.25),
    ]

    decision = engine.evaluate_access(
        subject="user:alice@corp.com",
        resource="api-payments-001",
        action="read",
        context_signals=signals,
    )
    print(f"\nAccess Decision: {decision.decision.value}")
    print(f"  Granted: {decision.granted}")
    print(f"  Trust Score: {decision.trust_score:.2f}")
    print(f"  Reason: {decision.reason}")

    weak_signals = [
        TrustSignal(signal_type="identity", value="failed", weight=0.30),
        TrustSignal(signal_type="device_health", value="non_compliant", weight=0.25),
    ]

    decision2 = engine.evaluate_access(
        subject="user:bob@corp.com",
        resource="api-payments-001",
        action="write",
        context_signals=weak_signals,
    )
    print(f"\nWeak-signal Decision: {decision2.decision.value}")
    print(f"  Trust Score: {decision2.trust_score:.2f}")

    perimeter = engine.define_micro_perimeter(
        perimeter_id="payments-zone",
        resources=["api-payments-*", "db-payments-*"],
        enforcement_mode="strict",
        default_action="deny",
    )
    print(f"\nMicro-perimeter: {perimeter.perimeter_id}")
    print(f"  Resources: {perimeter.resources}")
    print(f"  Mode: {perimeter.enforcement_mode.value}")

    assessment = engine.assess_posture(scope="payments-zone")
    print(f"\nPosture Assessment: {assessment.assessment_id}")
    print(f"  Maturity: {assessment.maturity_level.name}")
    print(f"  Score: {assessment.score:.2f}")
    print(f"  Gaps found: {len(assessment.gaps)}")
    for gap in assessment.gaps[:3]:
        print(f"    [{gap.severity}] {gap.category}: {gap.description[:60]}")

    log = engine.get_audit_log(limit=5)
    print(f"\nAudit Log ({len(log)} entries):")
    for entry in log:
        print(f"  {entry.request_id}: {entry.decision.value} — {entry.reason}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
