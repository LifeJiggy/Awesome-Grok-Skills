"""
Policy Engine for Zero Trust

ABAC/RBAC access control, OPA/Rego compatible policy authoring, policy
simulation, version control, compliance mapping, conflict resolution,
and comprehensive audit logging.
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Optional


class PolicyEffect(Enum):
    PERMIT = "permit"
    DENY = "deny"
    NOT_APPLICABLE = "not_applicable"
    INDETERMINATE = "indeterminate"


class ConflictResolution(Enum):
    MOST_SPECIFIC = "most_specific"
    MOST_RESTRICTIVE = "most_restrictive"
    HIGHEST_PRIORITY = "highest_priority"
    FIRST_MATCH = "first_match"


class Operator(Enum):
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    GTE = "gte"
    LTE = "lte"
    GT = "gt"
    LT = "lt"
    IN = "in"
    NOT_IN = "not_in"
    IN_RANGE = "in_range"
    CONTAINS = "contains"
    MATCHES = "matches"


@dataclass
class Attribute:
    principal: str
    attributes: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        return self.attributes.get(key, default)


@dataclass
class Condition:
    attribute: str
    operator: Operator
    value: Any
    negate: bool = False

    def evaluate(self, context: dict[str, Any]) -> bool:
        actual = self._resolve_attribute(self.attribute, context)
        result = self._apply_operator(actual, self.operator, self.value)
        return not result if self.negate else result

    def _resolve_attribute(self, path: str, context: dict[str, Any]) -> Any:
        parts = path.split(".")
        current = context
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return None
        return current

    def _apply_operator(self, actual: Any, op: Operator, expected: Any) -> bool:
        if actual is None:
            return op == Operator.NOT_EQUALS

        if op == Operator.EQUALS:
            return actual == expected
        elif op == Operator.NOT_EQUALS:
            return actual != expected
        elif op == Operator.GTE:
            return float(actual) >= float(expected)
        elif op == Operator.LTE:
            return float(actual) <= float(expected)
        elif op == Operator.GT:
            return float(actual) > float(expected)
        elif op == Operator.LT:
            return float(actual) < float(expected)
        elif op == Operator.IN:
            return actual in expected
        elif op == Operator.NOT_IN:
            return actual not in expected
        elif op == Operator.IN_RANGE:
            if isinstance(expected, str) and "-" in expected:
                parts = expected.split("-")
                return parts[0] <= str(actual) <= parts[1]
            return False
        elif op == Operator.CONTAINS:
            return str(expected) in str(actual)
        elif op == Operator.MATCHES:
            return fnmatch.fnmatch(str(actual), str(expected))
        return False


@dataclass
class Obligation:
    obligation_type: str
    detail: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass
class Policy:
    policy_id: str
    description: str
    effect: PolicyEffect
    target: dict[str, Any] = field(default_factory=dict)
    conditions: list[Condition] = field(default_factory=list)
    obligations: list[Obligation] = field(default_factory=list)
    priority: int = 1000
    enabled: bool = True
    version: int = 1
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    tags: list[str] = field(default_factory=list)
    compliance_refs: list[str] = field(default_factory=list)

    @property
    def specificity_score(self) -> int:
        return len(self.target) + len(self.conditions)

    def matches_target(
        self,
        subject_attrs: dict[str, Any],
        resource_attrs: dict[str, Any],
        action: str,
    ) -> bool:
        for key, pattern in self.target.items():
            if key.startswith("subject."):
                attr_key = key[len("subject."):]
                actual = subject_attrs.get(attr_key)
                if actual is None:
                    return False
                if isinstance(pattern, str) and ("*" in pattern or "?" in pattern):
                    if not fnmatch.fnmatch(str(actual), pattern):
                        return False
                elif actual != pattern:
                    return False
            elif key.startswith("resource."):
                attr_key = key[len("resource."):]
                actual = resource_attrs.get(attr_key)
                if actual is None:
                    return False
                if isinstance(pattern, str) and ("*" in pattern or "?" in pattern):
                    if not fnmatch.fnmatch(str(actual), pattern):
                        return False
                elif actual != pattern:
                    return False
            elif key == "action":
                if pattern != "*" and action != pattern:
                    return False
        return True


@dataclass
class EvaluationResult:
    decision: PolicyEffect
    matched_policies: list[str]
    obligations: list[Obligation]
    evaluation_trace: list[dict[str, Any]]
    evaluated_at: float = field(default_factory=time.time)
    request_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    cached: bool = False


@dataclass
class SimulationResult:
    would_allow: bool
    blocking_policies: list[str]
    allowing_policies: list[str]
    evaluation_details: list[dict[str, Any]]
    simulated_at: float = field(default_factory=time.time)


@dataclass
class ConflictInfo:
    conflict_id: str
    policy_a_id: str
    policy_b_id: str
    conflict_type: str
    description: str
    resolution: str


@dataclass
class PolicyDiff:
    policy_id: str
    old_version: int
    new_version: int
    changes: list[dict[str, Any]]
    changed_by: str = "system"
    changed_at: float = field(default_factory=time.time)
    change_description: str = ""


@dataclass
class ComplianceReport:
    report_id: str
    framework: str
    total_policies: int
    mapped_policies: int
    coverage_percentage: float
    compliance_mappings: list[dict[str, Any]]
    gaps: list[str]
    generated_at: float = field(default_factory=time.time)


class PolicyVersionControl:
    def __init__(self) -> None:
        self._versions: dict[str, list[dict[str, Any]]] = {}
        self._diffs: list[PolicyDiff] = []

    def save_version(self, policy: Policy) -> int:
        if policy.policy_id not in self._versions:
            self._versions[policy.policy_id] = []

        version_data = {
            "version": policy.version,
            "policy_id": policy.policy_id,
            "description": policy.description,
            "effect": policy.effect.value,
            "target": dict(policy.target),
            "conditions": [
                {"attr": c.attribute, "op": c.operator.value, "val": c.value}
                for c in policy.conditions
            ],
            "priority": policy.priority,
            "enabled": policy.enabled,
            "saved_at": time.time(),
        }
        self._versions[policy.policy_id].append(version_data)
        return policy.version

    def get_versions(self, policy_id: str) -> list[dict[str, Any]]:
        return self._versions.get(policy_id, [])

    def create_diff(
        self,
        policy_id: str,
        old_version: int,
        new_version: int,
        changed_by: str = "system",
        description: str = "",
    ) -> PolicyDiff | None:
        versions = self._versions.get(policy_id, [])
        old_data = None
        new_data = None

        for v in versions:
            if v["version"] == old_version:
                old_data = v
            if v["version"] == new_version:
                new_data = v

        if not old_data or not new_data:
            return None

        changes = []
        for key in set(list(old_data.keys()) + list(new_data.keys())):
            if key in ("version", "policy_id", "saved_at"):
                continue
            old_val = old_data.get(key)
            new_val = new_data.get(key)
            if old_val != new_val:
                changes.append({
                    "field": key,
                    "old": old_val,
                    "new": new_val,
                })

        diff = PolicyDiff(
            policy_id=policy_id,
            old_version=old_version,
            new_version=new_version,
            changes=changes,
            changed_by=changed_by,
            change_description=description,
        )
        self._diffs.append(diff)
        return diff

    def get_diffs(
        self, policy_id: str | None = None, limit: int = 20
    ) -> list[PolicyDiff]:
        diffs = self._diffs
        if policy_id:
            diffs = [d for d in diffs if d.policy_id == policy_id]
        return diffs[-limit:]

    def rollback(self, policy_id: str, target_version: int) -> dict[str, Any] | None:
        versions = self._versions.get(policy_id, [])
        for v in versions:
            if v["version"] == target_version:
                return dict(v)
        return None


class ComplianceMapper:
    FRAMEWORKS = {
        "NIST_800_53": {
            "AC-2": "Account Management",
            "AC-3": "Access Enforcement",
            "AC-6": "Least Privilege",
            "AC-7": "Unsuccessful Login Attempts",
            "IA-2": "Identification and Authentication",
        },
        "GDPR": {
            "Art.5": "Principles of Processing",
            "Art.25": "Data Protection by Design",
            "Art.32": "Security of Processing",
            "Art.33": "Breach Notification",
        },
        "HIPAA": {
            "164.312_a": "Access Control",
            "164.312_d": "Authentication",
            "164.312_e": "Transmission Security",
        },
        "PCI_DSS": {
            "Req.7": "Restrict Access by Business Need-to-Know",
            "Req.8": "Identify Users and Authenticate Access",
            "Req.10": "Track and Monitor Access",
        },
    }

    def map_policy_to_compliance(
        self, policy: Policy, framework: str
    ) -> list[dict[str, Any]]:
        mappings = []
        fw_controls = self.FRAMEWORKS.get(framework, {})

        for ref in policy.compliance_refs:
            if ref in fw_controls:
                mappings.append({
                    "policy_id": policy.policy_id,
                    "framework": framework,
                    "control": ref,
                    "control_name": fw_controls[ref],
                    "mapping_type": "satisfies",
                })

        if not policy.compliance_refs:
            effect_lower = policy.effect.value.lower()
            if effect_lower == "deny" and "AC-3" in fw_controls:
                mappings.append({
                    "policy_id": policy.policy_id,
                    "framework": framework,
                    "control": "AC-3",
                    "control_name": fw_controls["AC-3"],
                    "mapping_type": "supports",
                })

        return mappings

    def generate_report(
        self,
        policies: list[Policy],
        framework: str,
    ) -> ComplianceReport:
        all_mappings = []
        mapped_policy_ids: set[str] = set()

        for policy in policies:
            mappings = self.map_policy_to_compliance(policy, framework)
            all_mappings.extend(mappings)
            if mappings:
                mapped_policy_ids.add(policy.policy_id)

        fw_controls = self.FRAMEWORKS.get(framework, {})
        mapped_controls = {m["control"] for m in all_mappings}
        gaps = [
            f"{ctrl}: {name}"
            for ctrl, name in fw_controls.items()
            if ctrl not in mapped_controls
        ]

        total = len(policies)
        mapped = len(mapped_policy_ids)
        coverage = (mapped / total * 100) if total > 0 else 0.0

        return ComplianceReport(
            report_id=uuid.uuid4().hex[:12],
            framework=framework,
            total_policies=total,
            mapped_policies=mapped,
            coverage_percentage=coverage,
            compliance_mappings=all_mappings,
            gaps=gaps,
        )


class ConflictDetector:
    def __init__(self, resolution_strategy: ConflictResolution = ConflictResolution.MOST_SPECIFIC):
        self.resolution_strategy = resolution_strategy

    def detect_conflicts(self, policies: list[Policy]) -> list[ConflictInfo]:
        conflicts: list[ConflictInfo] = []

        for i, p1 in enumerate(policies):
            for p2 in policies[i + 1:]:
                if not p1.enabled or not p2.enabled:
                    continue

                if self._targets_overlap(p1, p2):
                    if p1.effect != p2.effect:
                        conflict_type = "effect_conflict"
                        resolution = self._resolve(p1, p2)
                        conflicts.append(ConflictInfo(
                            conflict_id=uuid.uuid4().hex[:8],
                            policy_a_id=p1.policy_id,
                            policy_b_id=p2.policy_id,
                            conflict_type=conflict_type,
                            description=(
                                f"Conflicting effects: {p1.effect.value} vs {p2.effect.value}"
                            ),
                            resolution=resolution,
                        ))

        return conflicts

    def detect_shadowed(self, policies: list[Policy]) -> list[ConflictInfo]:
        shadowed: list[ConflictInfo] = []
        enabled = [p for p in policies if p.enabled]

        for i, p1 in enumerate(enabled):
            for p2 in enabled[i + 1:]:
                if self._is_shadowed(p1, p2):
                    shadowed.append(ConflictInfo(
                        conflict_id=uuid.uuid4().hex[:8],
                        policy_a_id=p1.policy_id,
                        policy_b_id=p2.policy_id,
                        conflict_type="shadowed_rule",
                        description=(
                            f"Policy {p2.policy_id} is shadowed by {p1.policy_id}"
                        ),
                        resolution="higher_priority_policy_takes_precedence",
                    ))

        return shadowed

    def _targets_overlap(self, p1: Policy, p2: Policy) -> bool:
        for key in set(list(p1.target.keys()) + list(p2.target.keys())):
            v1 = p1.target.get(key, "*")
            v2 = p2.target.get(key, "*")
            if v1 != "*" and v2 != "*" and v1 != v2:
                return False
        return True

    def _is_shadowed(self, broader: Policy, narrower: Policy) -> bool:
        if broader.priority <= narrower.priority:
            return False
        if broader.effect != narrower.effect:
            return False
        for key, val in broader.target.items():
            if key not in narrower.target:
                return False
            nv = narrower.target[key]
            if val == "*" or val == nv:
                continue
            return False
        return True

    def _resolve(self, p1: Policy, p2: Policy) -> str:
        if self.resolution_strategy == ConflictResolution.MOST_SPECIFIC:
            return (
                p1.policy_id
                if p1.specificity_score >= p2.specificity_score
                else p2.policy_id
            )
        elif self.resolution_strategy == ConflictResolution.MOST_RESTRICTIVE:
            return p1.policy_id if p1.effect == PolicyEffect.DENY else p2.policy_id
        elif self.resolution_strategy == ConflictResolution.HIGHEST_PRIORITY:
            return p1.policy_id if p1.priority >= p2.priority else p2.policy_id
        else:
            return p1.policy_id


class AuditLogger:
    def __init__(self) -> None:
        self._entries: list[dict[str, Any]] = []

    def log_evaluation(
        self,
        request_id: str,
        subject: str,
        resource: str,
        action: str,
        decision: PolicyEffect,
        matched_policies: list[str],
        trace: list[dict[str, Any]],
    ) -> None:
        self._entries.append({
            "request_id": request_id,
            "timestamp": time.time(),
            "subject": subject,
            "resource": resource,
            "action": action,
            "decision": decision.value,
            "matched_policies": matched_policies,
            "trace": trace,
        })

    def log_policy_change(
        self,
        policy_id: str,
        change_type: str,
        details: dict[str, Any],
    ) -> None:
        self._entries.append({
            "event_type": "policy_change",
            "timestamp": time.time(),
            "policy_id": policy_id,
            "change_type": change_type,
            "details": details,
        })

    def get_entries(
        self,
        subject: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        entries = self._entries
        if subject:
            entries = [e for e in entries if e.get("subject") == subject]
        return entries[-limit:]

    def get_entries_for_policy(self, policy_id: str) -> list[dict[str, Any]]:
        return [
            e for e in self._entries
            if e.get("policy_id") == policy_id
            or policy_id in e.get("matched_policies", [])
        ]


class PolicyEngine:
    def __init__(
        self,
        engine_id: str = "pdp-default",
        default_effect: str = "deny",
        audit_logging: bool = True,
        conflict_resolution: str = "most_specific",
    ):
        self.engine_id = engine_id
        self.default_effect = PolicyEffect(default_effect)
        self.audit_logging = audit_logging
        self._policies: dict[str, Policy] = {}
        self._version_control = PolicyVersionControl()
        self._compliance_mapper = ComplianceMapper()
        self._conflict_detector = ConflictDetector(
            ConflictResolution(conflict_resolution)
        )
        self._audit = AuditLogger()
        self._evaluation_cache: dict[str, EvaluationResult] = {}

    def create_policy(
        self,
        policy_id: str,
        description: str,
        effect: str = "permit",
        target: dict[str, Any] | None = None,
        conditions: list[dict[str, Any]] | None = None,
        obligations: list[dict[str, Any]] | None = None,
        priority: int = 1000,
        tags: list[str] | None = None,
        compliance_refs: list[str] | None = None,
    ) -> Policy:
        parsed_conditions = []
        for c in (conditions or []):
            parsed_conditions.append(Condition(
                attribute=c["attribute"],
                operator=Operator(c["operator"]),
                value=c["value"],
            ))

        parsed_obligations = []
        for o in (obligations or []):
            parsed_obligations.append(Obligation(
                obligation_type=o["type"],
                detail=o.get("detail", ""),
                parameters=o.get("parameters", {}),
            ))

        policy = Policy(
            policy_id=policy_id,
            description=description,
            effect=PolicyEffect(effect),
            target=target or {},
            conditions=parsed_conditions,
            obligations=parsed_obligations,
            priority=priority,
            tags=tags or [],
            compliance_refs=compliance_refs or [],
        )

        self._policies[policy_id] = policy
        self._version_control.save_version(policy)

        if self.audit_logging:
            self._audit.log_policy_change(
                policy_id, "created", {"effect": effect, "description": description}
            )

        return policy

    def update_policy(
        self,
        policy_id: str,
        **kwargs: Any,
    ) -> Policy | None:
        policy = self._policies.get(policy_id)
        if not policy:
            return None

        old_version = policy.version

        if "effect" in kwargs:
            policy.effect = PolicyEffect(kwargs["effect"])
        if "target" in kwargs:
            policy.target = kwargs["target"]
        if "priority" in kwargs:
            policy.priority = kwargs["priority"]
        if "enabled" in kwargs:
            policy.enabled = kwargs["enabled"]
        if "description" in kwargs:
            policy.description = kwargs["description"]

        policy.version += 1
        policy.updated_at = time.time()

        self._version_control.save_version(policy)
        self._version_control.create_diff(
            policy_id, old_version, policy.version,
            description=kwargs.get("change_description", "policy updated"),
        )

        if self.audit_logging:
            self._audit.log_policy_change(
                policy_id, "updated",
                {"old_version": old_version, "new_version": policy.version},
            )

        return policy

    def delete_policy(self, policy_id: str) -> bool:
        if policy_id in self._policies:
            del self._policies[policy_id]
            if self.audit_logging:
                self._audit.log_policy_change(policy_id, "deleted", {})
            return True
        return False

    def evaluate(
        self,
        subject: Attribute,
        resource: Attribute,
        action: str,
        environment: dict[str, Any] | None = None,
    ) -> EvaluationResult:
        env = environment or {}
        full_context = {
            "subject": subject.attributes,
            "resource": resource.attributes,
            "action": action,
            "environment": env,
        }

        matched_policies: list[str] = []
        all_obligations: list[Obligation] = []
        trace: list[dict[str, Any]] = []

        applicable = []
        for policy in self._policies.values():
            if not policy.enabled:
                continue
            if policy.matches_target(subject.attributes, resource.attributes, action):
                applicable.append(policy)
                trace.append({
                    "policy_id": policy.policy_id,
                    "target_match": True,
                    "effect": policy.effect.value,
                })

        applicable.sort(key=lambda p: (p.specificity_score, p.priority), reverse=True)

        for policy in applicable:
            conditions_met = True
            for condition in policy.conditions:
                ctx_flat = {
                    **subject.attributes,
                    **resource.attributes,
                    **env,
                }
                if not condition.evaluate(ctx_flat):
                    conditions_met = False
                    trace.append({
                        "policy_id": policy.policy_id,
                        "condition_failed": condition.attribute,
                    })
                    break

            if conditions_met:
                matched_policies.append(policy.policy_id)
                all_obligations.extend(policy.obligations)

                if self._conflict_detector.resolution_strategy == ConflictResolution.FIRST_MATCH:
                    break

        if matched_policies:
            final_effect = self._resolve_final_effect(matched_policies)
        else:
            final_effect = self.default_effect

        result = EvaluationResult(
            decision=final_effect,
            matched_policies=matched_policies,
            obligations=all_obligations,
            evaluation_trace=trace,
        )

        if self.audit_logging:
            self._audit.log_evaluation(
                result.request_id,
                subject.principal,
                resource.principal,
                action,
                final_effect,
                matched_policies,
                trace,
            )

        return result

    def simulate(
        self,
        subject_attributes: dict[str, Any],
        resource_attributes: dict[str, Any],
        action: str,
        environment: dict[str, Any] | None = None,
    ) -> SimulationResult:
        subject = Attribute(principal="simulated", attributes=subject_attributes)
        resource = Attribute(principal="simulated", attributes=resource_attributes)

        result = self.evaluate(subject, resource, action, environment)

        allowing = []
        blocking = []
        for pid in result.matched_policies:
            policy = self._policies.get(pid)
            if policy:
                if policy.effect == PolicyEffect.PERMIT:
                    allowing.append(pid)
                else:
                    blocking.append(pid)

        return SimulationResult(
            would_allow=result.decision == PolicyEffect.PERMIT,
            blocking_policies=blocking,
            allowing_policies=allowing,
            evaluation_details=result.evaluation_trace,
        )

    def detect_conflicts(self) -> list[ConflictInfo]:
        return self._conflict_detector.detect_conflicts(list(self._policies.values()))

    def detect_shadowed_rules(self) -> list[ConflictInfo]:
        return self._conflict_detector.detect_shadowed(list(self._policies.values()))

    def generate_compliance_report(self, framework: str) -> ComplianceReport:
        return self._compliance_mapper.generate_report(
            list(self._policies.values()), framework
        )

    def get_audit_log(
        self, subject: str | None = None, limit: int = 50
    ) -> list[dict[str, Any]]:
        return self._audit.get_entries(subject, limit)

    def get_policy_versions(self, policy_id: str) -> list[dict[str, Any]]:
        return self._version_control.get_versions(policy_id)

    def get_policy_diffs(self, policy_id: str | None = None) -> list[PolicyDiff]:
        return self._version_control.get_diffs(policy_id)

    def rollback_policy(
        self, policy_id: str, target_version: int
    ) -> dict[str, Any] | None:
        return self._version_control.rollback(policy_id, target_version)

    def list_policies(self, enabled_only: bool = False) -> list[Policy]:
        policies = list(self._policies.values())
        if enabled_only:
            policies = [p for p in policies if p.enabled]
        return policies

    def get_policy(self, policy_id: str) -> Policy | None:
        return self._policies.get(policy_id)

    def _resolve_final_effect(self, matched_ids: list[str]) -> PolicyEffect:
        deny_found = False
        for pid in matched_ids:
            policy = self._policies.get(pid)
            if policy and policy.effect == PolicyEffect.DENY:
                deny_found = True
                break

        if deny_found and self._conflict_detector.resolution_strategy == ConflictResolution.MOST_RESTRICTIVE:
            return PolicyEffect.DENY

        for pid in matched_ids:
            policy = self._policies.get(pid)
            if policy and policy.effect == PolicyEffect.PERMIT:
                return PolicyEffect.PERMIT

        return PolicyEffect.DENY


def main() -> None:
    print("=" * 60)
    print("Policy Engine Module — Demo")
    print("=" * 60)

    engine = PolicyEngine(
        engine_id="authz-pdp-001",
        default_effect="deny",
        audit_logging=True,
        conflict_resolution="most_specific",
    )

    engine.create_policy(
        policy_id="permit-finance-read-payments",
        description="Allow finance analysts to read payment records",
        effect="permit",
        target={
            "subject.role": "finance_analyst",
            "resource.type": "payment_record",
            "action": "read",
        },
        conditions=[
            {"attribute": "environment.time_of_day", "operator": "in_range", "value": "08:00-18:00"},
            {"attribute": "device.trust_score", "operator": "gte", "value": 0.7},
        ],
        obligations=[
            {"type": "audit_log", "detail": "finance_payment_access"},
        ],
        priority=1000,
        compliance_refs=["Req.7", "AC-3"],
    )

    engine.create_policy(
        policy_id="deny-after-hours-access",
        description="Deny all access outside business hours",
        effect="deny",
        target={"action": "*"},
        conditions=[
            {"attribute": "environment.time_of_day", "operator": "in_range", "value": "00:00-08:00"},
        ],
        priority=500,
        compliance_refs=["AC-3"],
    )

    engine.create_policy(
        policy_id="permit-admin-full-access",
        description="Allow admins full access",
        effect="permit",
        target={"subject.role": "admin", "action": "*"},
        priority=2000,
    )

    print(f"\nPolicies created: {len(engine.list_policies())}")

    result = engine.evaluate(
        subject=Attribute(
            principal="user:alice@corp.com",
            attributes={"role": "finance_analyst", "department": "finance"},
        ),
        resource=Attribute(
            principal="resource:payment-001",
            attributes={"type": "payment_record", "classification": "confidential"},
        ),
        action="read",
        environment={"time_of_day": "10:30", "device_trust_score": 0.85},
    )

    print(f"\nEvaluation (finance analyst, read, business hours):")
    print(f"  Decision: {result.decision.value}")
    print(f"  Matched policies: {result.matched_policies}")
    print(f"  Obligations: {[o.obligation_type for o in result.obligations]}")

    sim = engine.simulate(
        subject_attributes={"role": "finance_analyst"},
        resource_attributes={"type": "payment_record"},
        action="read",
        environment={"time_of_day": "22:00"},
    )
    print(f"\nSimulation (after-hours):")
    print(f"  Would allow: {sim.would_allow}")
    print(f"  Blocking: {sim.blocking_policies}")

    conflicts = engine.detect_conflicts()
    print(f"\nConflicts detected: {len(conflicts)}")
    for c in conflicts:
        print(f"  {c.policy_a_id} vs {c.policy_b_id}: {c.description}")

    compliance = engine.generate_compliance_report("PCI_DSS")
    print(f"\nCompliance Report ({compliance.framework}):")
    print(f"  Total policies: {compliance.total_policies}")
    print(f"  Coverage: {compliance.coverage_percentage:.1f}%")
    print(f"  Gaps: {compliance.gaps}")

    engine.update_policy(
        "permit-finance-read-payments",
        priority=1500,
        change_description="Elevate priority for compliance audit",
    )
    diffs = engine.get_policy_diffs("permit-finance-read-payments")
    print(f"\nPolicy Diffs ({len(diffs)}):")
    for d in diffs:
        print(f"  v{d.old_version} -> v{d.new_version}: {d.change_description}")

    audit_log = engine.get_audit_log(limit=5)
    print(f"\nAudit Log ({len(audit_log)} entries):")
    for entry in audit_log:
        print(f"  [{entry.get('event_type', 'evaluation')}] {entry.get('decision', entry.get('change_type', ''))}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
