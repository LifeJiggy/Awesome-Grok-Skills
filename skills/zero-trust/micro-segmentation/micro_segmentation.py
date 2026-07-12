"""
Network Micro-Segmentation Module

Policy-as-code network segmentation, SDN controls, workload isolation,
container network policies, east-west traffic inspection, and dynamic
segmentation rules for zero trust environments.
"""

from __future__ import annotations

import fnmatch
import hashlib
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Optional


class SegmentClassification(Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"
    PCI_DSS_SCOPE = "pci_dss_scope"
    HIPAA_SCOPE = "hipaa_scope"


class PolicyAction(Enum):
    ALLOW = "allow"
    DENY = "deny"
    LOG = "log"
    RATE_LIMIT = "rate_limit"


class EnforcementMode(Enum):
    ENFORCING = "enforcing"
    AUDIT = "audit"
    DRY_RUN = "dry_run"


class TrafficDirection(Enum):
    INGRESS = "ingress"
    EGRESS = "egress"
    BIDIRECTIONAL = "bidirectional"


@dataclass
class Port:
    number: int
    protocol: str = "tcp"

    def __str__(self) -> str:
        return f"{self.number}/{self.protocol}"

    def matches(self, other: tuple[int, str]) -> bool:
        return self.number == other[0] and self.protocol == other[1]


@dataclass
class NetworkPolicy:
    name: str
    source_selectors: dict[str, str] = field(default_factory=dict)
    destination_selectors: dict[str, str] = field(default_factory=dict)
    ports: list[tuple[int, str]] = field(default_factory=list)
    action: PolicyAction = PolicyAction.DENY
    direction: TrafficDirection = TrafficDirection.INGRESS
    priority: int = 1000
    conditions: dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    created_at: float = field(default_factory=time.time)
    policy_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])

    def matches_workload(
        self, workload_labels: dict[str, str], direction: str = "source"
    ) -> bool:
        selectors = (
            self.source_selectors if direction == "source" else self.destination_selectors
        )
        if not selectors:
            return True
        for key, pattern in selectors.items():
            if key not in workload_labels:
                return False
            if not fnmatch.fnmatch(workload_labels[key], pattern):
                return False
        return True

    def matches_port(self, port: int, protocol: str = "tcp") -> bool:
        if not self.ports:
            return True
        return any(p[0] == port and p[1] == protocol for p in self.ports)


@dataclass
class Segment:
    segment_id: str
    description: str
    classification: SegmentClassification
    workload_selectors: dict[str, str] = field(default_factory=dict)
    ingress_rules: list[NetworkPolicy] = field(default_factory=list)
    egress_rules: list[NetworkPolicy] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    tags: list[str] = field(default_factory=list)

    def contains_workload(self, labels: dict[str, str]) -> bool:
        for key, pattern in self.workload_selectors.items():
            if key not in labels:
                return False
            if not fnmatch.fnmatch(labels[key], pattern):
                return False
        return True


@dataclass
class CrossSegmentPolicy:
    policy_id: str
    source_segment: str
    target_segment: str
    allowed_ports: list[tuple[int, str]] = field(default_factory=list)
    conditions: dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    created_at: float = field(default_factory=time.time)


@dataclass
class SimulationResult:
    allowed: bool
    matched_rules: list[str]
    conflicts: list[str]
    warnings: list[str]
    simulated_at: float = field(default_factory=time.time)


@dataclass
class DeployResult:
    success: bool
    rules_applied: int
    segments_deployed: list[str]
    errors: list[str]
    deployed_at: float = field(default_factory=time.time)


@dataclass
class TrafficEvent:
    event_id: str
    timestamp: float
    source_workload: dict[str, str]
    destination_workload: dict[str, str]
    source_ip: str
    destination_ip: str
    port: int
    protocol: str
    action: PolicyAction
    matched_policy: str | None = None
    bytes_transferred: int = 0


@dataclass
class AnomalyDetection:
    anomaly_id: str
    segment_id: str
    anomaly_type: str
    severity: str
    description: str
    source_workload: dict[str, str] = field(default_factory=dict)
    detected_at: float = field(default_factory=time.time)
    resolved: bool = False


class WorkloadRegistry:
    def __init__(self) -> None:
        self._workloads: dict[str, dict[str, Any]] = {}

    def register(
        self,
        workload_id: str,
        labels: dict[str, str],
        ip_address: str,
        namespace: str = "default",
    ) -> None:
        self._workloads[workload_id] = {
            "labels": labels,
            "ip_address": ip_address,
            "namespace": namespace,
            "registered_at": time.time(),
        }

    def deregister(self, workload_id: str) -> bool:
        return self._workloads.pop(workload_id, None) is not None

    def find_by_labels(self, selector: dict[str, str]) -> list[str]:
        matches = []
        for wl_id, wl_data in self._workloads.items():
            all_match = True
            for key, pattern in selector.items():
                wl_labels = wl_data["labels"]
                if key not in wl_labels or not fnmatch.fnmatch(wl_labels[key], pattern):
                    all_match = False
                    break
            if all_match:
                matches.append(wl_id)
        return matches

    def get_workload(self, workload_id: str) -> dict[str, Any] | None:
        return self._workloads.get(workload_id)

    def get_all(self) -> dict[str, dict[str, Any]]:
        return dict(self._workloads)


class TrafficInspector:
    def __init__(self) -> None:
        self._events: list[TrafficEvent] = []
        self._baselines: dict[str, dict[str, float]] = {}
        self._anomalies: list[AnomalyDetection] = []

    def record_event(self, event: TrafficEvent) -> None:
        self._events.append(event)
        self._update_baseline(event)
        self._check_anomaly(event)

    def _update_baseline(self, event: TrafficEvent) -> None:
        key = f"{event.source_workload}:{event.destination_workload}:{event.port}"
        if key not in self._baselines:
            self._baselines[key] = {"count": 0, "bytes": 0, "last_seen": 0}
        self._baselines[key]["count"] += 1
        self._baselines[key]["bytes"] += event.bytes_transferred
        self._baselines[key]["last_seen"] = event.timestamp

    def _check_anomaly(self, event: TrafficEvent) -> None:
        key = f"{event.source_workload}:{event.destination_workload}:{event.port}"
        baseline = self._baselines.get(key, {})
        if baseline.get("count", 0) > 1000:
            anomaly = AnomalyDetection(
                anomaly_id=uuid.uuid4().hex[:12],
                segment_id="unknown",
                anomaly_type="high_volume",
                severity="medium",
                description=f"Unusual traffic volume detected: {baseline['count']} requests",
                source_workload=event.source_workload,
                detected_at=time.time(),
            )
            self._anomalies.append(anomaly)

    def get_events(
        self,
        source: str | None = None,
        destination: str | None = None,
        limit: int = 100,
    ) -> list[TrafficEvent]:
        events = self._events
        return events[-limit:]

    def get_anomalies(
        self, segment_id: str | None = None, unresolved_only: bool = True
    ) -> list[AnomalyDetection]:
        anomalies = self._anomalies
        if segment_id:
            anomalies = [a for a in anomalies if a.segment_id == segment_id]
        if unresolved_only:
            anomalies = [a for a in anomalies if not a.resolved]
        return anomalies


class PolicyCompiler:
    @staticmethod
    def compile_to_iptables(segment: Segment) -> list[str]:
        rules = []
        for rule in segment.ingress_rules:
            for port_tuple in rule.ports:
                for wl_id in [f"src_{k}_{v}" for k, v in rule.source_selectors.items()]:
                    rule_str = (
                        f"-A INPUT -s {wl_id} -p tcp --dport {port_tuple[0]} "
                        f"-j {'ACCEPT' if rule.action == PolicyAction.ALLOW else 'DROP'}"
                    )
                    rules.append(rule_str)
        for rule in segment.egress_rules:
            for port_tuple in rule.ports:
                rule_str = (
                    f"-A OUTPUT -p tcp --dport {port_tuple[0]} "
                    f"-j {'ACCEPT' if rule.action == PolicyAction.ALLOW else 'DROP'}"
                )
                rules.append(rule_str)
        rules.append(f"-A INPUT -j {'ACCEPT' if False else 'DROP'}")
        return rules

    @staticmethod
    def compile_to_kubernetes_policy(segment: Segment) -> dict[str, Any]:
        ingress = []
        for rule in segment.ingress_rules:
            pod_selector = {
                "matchLabels": {k: v for k, v in rule.source_selectors.items()}
            }
            ports = [{"port": p[0], "protocol": p[1].upper()} for p in rule.ports]
            ingress.append({
                "from": [{"podSelector": pod_selector}],
                "ports": ports,
            })

        egress = []
        for rule in segment.egress_rules:
            pod_selector = {
                "matchLabels": {k: v for k, v in rule.destination_selectors.items()}
            }
            ports = [{"port": p[0], "protocol": p[1].upper()} for p in rule.ports]
            egress.append({
                "to": [{"podSelector": pod_selector}],
                "ports": ports,
            })

        return {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {"name": f"policy-{segment.segment_id}"},
            "spec": {
                "podSelector": {"matchLabels": segment.workload_selectors},
                "policyTypes": ["Ingress", "Egress"],
                "ingress": ingress,
                "egress": egress,
            },
        }


class SegmentationEngine:
    def __init__(
        self,
        provider: str = "kubernetes",
        default_action: str = "deny",
        inspection_enabled: bool = True,
    ):
        self.provider = provider
        self.default_action = default_action
        self.inspection_enabled = inspection_enabled
        self._segments: dict[str, Segment] = {}
        self._cross_segment_policies: dict[str, CrossSegmentPolicy] = {}
        self._workload_registry = WorkloadRegistry()
        self._inspector = TrafficInspector()
        self._compiler = PolicyCompiler()
        self._deployment_history: list[DeployResult] = []

    def create_segment(
        self,
        segment_id: str,
        description: str,
        classification: str = "internal",
        workload_selectors: dict[str, str] | None = None,
        ingress_rules: list[NetworkPolicy] | None = None,
        egress_rules: list[NetworkPolicy] | None = None,
        tags: list[str] | None = None,
    ) -> Segment:
        segment = Segment(
            segment_id=segment_id,
            description=description,
            classification=SegmentClassification(classification),
            workload_selectors=workload_selectors or {},
            ingress_rules=ingress_rules or [],
            egress_rules=egress_rules or [],
            tags=tags or [],
        )
        self._segments[segment_id] = segment
        return segment

    def delete_segment(self, segment_id: str) -> bool:
        return self._segments.pop(segment_id, None) is not None

    def create_cross_segment_policy(
        self,
        policy_id: str,
        source_segment: str,
        target_segment: str,
        allowed_ports: list[tuple[int, str]] | None = None,
        conditions: dict[str, Any] | None = None,
    ) -> CrossSegmentPolicy:
        policy = CrossSegmentPolicy(
            policy_id=policy_id,
            source_segment=source_segment,
            target_segment=target_segment,
            allowed_ports=allowed_ports or [],
            conditions=conditions or {},
        )
        self._cross_segment_policies[policy_id] = policy
        return policy

    def simulate(
        self,
        source_workload: dict[str, str],
        target_workload: dict[str, str],
        proposed_policies: list[str] | None = None,
        port: int = 443,
        protocol: str = "tcp",
    ) -> SimulationResult:
        matched_rules: list[str] = []
        conflicts: list[str] = []
        warnings: list[str] = []
        allowed = self.default_action == "allow"

        source_segment = self._find_segment_for_workload(source_workload)
        target_segment = self._find_segment_for_workload(target_workload)

        if source_segment and target_segment:
            if source_segment.segment_id == target_segment.segment_id:
                for rule in target_segment.ingress_rules:
                    if rule.matches_workload(source_workload, "source"):
                        if rule.matches_port(port, protocol):
                            matched_rules.append(rule.policy_id)
                            allowed = rule.action == PolicyAction.ALLOW
            else:
                policy_ids = proposed_policies or []
                for pid in policy_ids:
                    csp = self._cross_segment_policies.get(pid)
                    if csp:
                        if csp.source_segment == source_segment.segment_id:
                            if csp.target_segment == target_segment.segment_id:
                                matched_rules.append(csp.policy_id)
                                allowed = True
                            else:
                                conflicts.append(
                                    f"Policy {pid} targets wrong segment"
                                )

        if not matched_rules and self.default_action == "deny":
            warnings.append("No matching rules found; default deny applies")

        return SimulationResult(
            allowed=allowed,
            matched_rules=matched_rules,
            conflicts=conflicts,
            warnings=warnings,
        )

    def deploy(
        self,
        segment_ids: list[str],
        dry_run: bool = False,
        validate_compliance: bool = True,
    ) -> DeployResult:
        errors: list[str] = []
        rules_applied = 0

        for sid in segment_ids:
            segment = self._segments.get(sid)
            if not segment:
                errors.append(f"Segment {sid} not found")
                continue

            if validate_compliance:
                compliance_issues = self._validate_compliance(segment)
                errors.extend(compliance_issues)

            if not dry_run:
                rules_applied += len(segment.ingress_rules) + len(segment.egress_rules)

        result = DeployResult(
            success=len(errors) == 0,
            rules_applied=rules_applied,
            segments_deployed=[] if errors else segment_ids,
            errors=errors,
        )
        self._deployment_history.append(result)
        return result

    def get_segment(self, segment_id: str) -> Segment | None:
        return self._segments.get(segment_id)

    def list_segments(self) -> list[Segment]:
        return list(self._segments.values())

    def get_deployment_history(self, limit: int = 10) -> list[DeployResult]:
        return self._deployment_history[-limit:]

    def get_traffic_events(self, limit: int = 50) -> list[TrafficEvent]:
        return self._inspector.get_events(limit=limit)

    def get_anomalies(self, segment_id: str | None = None) -> list[AnomalyDetection]:
        return self._inspector.get_anomalies(segment_id=segment_id)

    def record_traffic_event(
        self,
        source_ip: str,
        destination_ip: str,
        port: int,
        protocol: str = "tcp",
        action: str = "allow",
        bytes_transferred: int = 0,
    ) -> TrafficEvent:
        event = TrafficEvent(
            event_id=uuid.uuid4().hex[:12],
            timestamp=time.time(),
            source_workload={"ip": source_ip},
            destination_workload={"ip": destination_ip},
            source_ip=source_ip,
            destination_ip=destination_ip,
            port=port,
            protocol=protocol,
            action=PolicyAction(action),
            bytes_transferred=bytes_transferred,
        )
        self._inspector.record_event(event)
        return event

    def compile_segment(self, segment_id: str) -> dict[str, Any]:
        segment = self._segments.get(segment_id)
        if not segment:
            return {"error": f"Segment {segment_id} not found"}

        if self.provider == "kubernetes":
            return self._compiler.compile_to_kubernetes_policy(segment)
        else:
            return {"iptables_rules": self._compiler.compile_to_iptables(segment)}

    def _find_segment_for_workload(
        self, workload_labels: dict[str, str]
    ) -> Segment | None:
        for segment in self._segments.values():
            if segment.contains_workload(workload_labels):
                return segment
        return None

    def _validate_compliance(self, segment: Segment) -> list[str]:
        issues = []
        if segment.classification in (
            SegmentClassification.PCI_DSS_SCOPE,
            SegmentClassification.HIPAA_SCOPE,
        ):
            if not segment.egress_rules:
                issues.append(
                    f"Segment {segment.segment_id}: restricted segment requires "
                    "explicit egress rules for compliance"
                )
            has_deny = any(
                r.action == PolicyAction.DENY for r in segment.egress_rules
            )
            if not has_deny:
                issues.append(
                    f"Segment {segment.segment_id}: restricted segment should "
                    "include explicit deny egress rules"
                )
        return issues


def main() -> None:
    print("=" * 60)
    print("Micro-Segmentation Module — Demo")
    print("=" * 60)

    engine = SegmentationEngine(
        provider="kubernetes",
        default_action="deny",
        inspection_enabled=True,
    )

    frontend_segment = engine.create_segment(
        segment_id="frontend",
        description="Frontend web application workloads",
        classification="internal",
        workload_selectors={"app": "web-*", "tier": "frontend"},
        ingress_rules=[
            NetworkPolicy(
                name="allow-external",
                source_selectors={"app": "*"},
                ports=[(443, "tcp")],
                action=PolicyAction.ALLOW,
            ),
        ],
        egress_rules=[
            NetworkPolicy(
                name="to-backend",
                destination_selectors={"app": "api-*", "tier": "backend"},
                ports=[(8443, "tcp")],
                action=PolicyAction.ALLOW,
            ),
        ],
    )

    backend_segment = engine.create_segment(
        segment_id="backend",
        description="Backend API workloads",
        classification="confidential",
        workload_selectors={"app": "api-*", "tier": "backend"},
        ingress_rules=[
            NetworkPolicy(
                name="from-frontend",
                source_selectors={"app": "web-*", "tier": "frontend"},
                ports=[(8443, "tcp")],
                action=PolicyAction.ALLOW,
            ),
        ],
        egress_rules=[
            NetworkPolicy(
                name="to-database",
                destination_selectors={"app": "db-*"},
                ports=[(5432, "tcp")],
                action=PolicyAction.ALLOW,
            ),
        ],
    )

    payments_segment = engine.create_segment(
        segment_id="payments",
        description="PCI DSS scoped payment processing",
        classification="pci_dss_scope",
        workload_selectors={"app": "payment-*", "compliance": "pci"},
        ingress_rules=[
            NetworkPolicy(
                name="allow-backend",
                source_selectors={"app": "api-*"},
                ports=[(443, "tcp")],
                action=PolicyAction.ALLOW,
            ),
        ],
        egress_rules=[
            NetworkPolicy(
                name="deny-all-egress",
                destination_selectors={"app": "*"},
                ports=[],
                action=PolicyAction.DENY,
            ),
        ],
    )

    print(f"\nSegments created:")
    for seg in engine.list_segments():
        print(f"  {seg.segment_id}: {seg.description} [{seg.classification.value}]")

    engine.create_cross_segment_policy(
        policy_id="frontend-to-backend",
        source_segment="frontend",
        target_segment="backend",
        allowed_ports=[(8443, "tcp")],
        conditions={"require_mutual_tls": True},
    )

    sim = engine.simulate(
        source_workload={"app": "web-frontend-1", "tier": "frontend"},
        target_workload={"app": "api-payments", "tier": "backend"},
        proposed_policies=["frontend-to-backend"],
        port=8443,
    )
    print(f"\nSimulation (frontend -> backend):")
    print(f"  Allowed: {sim.allowed}")
    print(f"  Matched rules: {sim.matched_rules}")
    print(f"  Conflicts: {sim.conflicts}")

    deploy = engine.deploy(
        segment_ids=["frontend", "backend", "payments"],
        dry_run=False,
        validate_compliance=True,
    )
    print(f"\nDeployment:")
    print(f"  Success: {deploy.success}")
    print(f"  Rules applied: {deploy.rules_applied}")
    print(f"  Segments: {deploy.segments_deployed}")
    if deploy.errors:
        print(f"  Errors: {deploy.errors}")

    for i in range(5):
        engine.record_traffic_event(
            source_ip=f"10.0.1.{10 + i}",
            destination_ip="10.0.2.20",
            port=443,
            bytes_transferred=1024 * (i + 1),
        )

    k8s_policy = engine.compile_segment("payments")
    print(f"\nKubernetes Policy for 'payments':")
    print(f"  Kind: {k8s_policy.get('kind', 'N/A')}")
    print(f"  Ingress rules: {len(k8s_policy.get('spec', {}).get('ingress', []))}")

    anomalies = engine.get_anomalies()
    print(f"\nAnomalies detected: {len(anomalies)}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
