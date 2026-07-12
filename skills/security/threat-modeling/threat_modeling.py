"""
Threat Modeling Framework
=========================

Implements STRIDE analysis, DREAD risk scoring, attack tree construction,
and attack surface quantification for systematic threat identification
and risk assessment.
"""

from __future__ import annotations

import math
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class STRIDECategory(Enum):
    SPOOFING = "spoofing"
    TAMPERING = "tampering"
    REPUDIATION = "repudiation"
    INFORMATION_DISCLOSURE = "information_disclosure"
    DENIAL_OF_SERVICE = "denial_of_service"
    ELEVATION_OF_PRIVILEGE = "elevation_of_privilege"


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ComponentType(Enum):
    PROCESS = "process"
    DATASTORE = "datastore"
    EXTERNAL_ENTITY = "external_entity"
    DATA_FLOW = "data_flow"


class MitigationStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    IMPLEMENTED = "implemented"
    VERIFIED = "verified"
    ACCEPTED = "accepted"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class SystemComponent:
    """A component in the system being modeled."""
    name: str
    type: ComponentType | str = ComponentType.PROCESS
    trust_level: str = "untrusted"
    description: str = ""
    data_classification: str = "internal"
    internet_facing: bool = False

    def __post_init__(self) -> None:
        if isinstance(self.type, str):
            self.type = ComponentType(self.type)


@dataclass
class TrustBoundary:
    """A boundary across which trust level changes."""
    name: str
    components: list[str] = field(default_factory=list)
    description: str = ""

    @property
    def component_count(self) -> int:
        return len(self.components)


@dataclass
class Threat:
    """A single identified threat."""
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    category: STRIDECategory = STRIDECategory.SPOOFING
    description: str = ""
    component: str = ""
    boundary_crossed: Optional[str] = None
    severity: RiskLevel = RiskLevel.MEDIUM
    affected_assets: list[str] = field(default_factory=list)
    mitigation: str = ""
    mitigation_status: MitigationStatus = MitigationStatus.NOT_STARTED


@dataclass
class STRIDEResult:
    """Result of a STRIDE analysis for a single component."""
    component: str
    threats: list[Threat] = field(default_factory=list)
    categories_found: list[STRIDECategory] = field(default_factory=list)

    @property
    def threat_count(self) -> int:
        return len(self.threats)


@dataclass
class DREADScore:
    """DREAD risk score for a threat."""
    threat_name: str
    damage: int = 0
    reproducibility: int = 0
    exploitability: int = 0
    affected_users: int = 0
    discoverability: int = 0

    @property
    def average(self) -> float:
        scores = [self.damage, self.reproducibility, self.exploitability,
                  self.affected_users, self.discoverability]
        return sum(scores) / len(scores) if scores else 0.0

    @property
    def risk_level(self) -> RiskLevel:
        avg = self.average
        if avg >= 8:
            return RiskLevel.CRITICAL
        elif avg >= 6:
            return RiskLevel.HIGH
        elif avg >= 4:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW


@dataclass
class AttackNode:
    """A node in an attack tree."""
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    method: str = ""
    cost: str = "unknown"
    success_probability: float = 0.0
    children: list[AttackNode] = field(default_factory=list)
    is_and_node: bool = False  # AND vs OR decomposition

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    @property
    def depth(self) -> int:
        if self.is_leaf:
            return 0
        return 1 + max(c.depth for c in self.children)


@dataclass
class GoalNode(AttackNode):
    """Root goal of an attack tree."""
    goal: str = ""
    attacker: str = "External"


@dataclass
class AttackPath:
    """A single path through an attack tree."""
    nodes: list[str] = field(default_factory=list)
    total_cost: float = 0.0
    probability: float = 1.0

    @property
    def risk_score(self) -> float:
        return self.total_cost * self.probability


@dataclass
class AttackSurfaceReport:
    """Quantified attack surface."""
    total_components: int = 0
    internet_facing: int = 0
    trust_boundaries: int = 0
    data_stores: int = 0
    external_integrations: int = 0
    authentication_points: int = 0
    risk_score: float = 0.0


# ---------------------------------------------------------------------------
# STRIDE Analyzer
# ---------------------------------------------------------------------------

# Mapping from component type to applicable STRIDE categories
STRIDE_APPlicability: dict[str, list[STRIDECategory]] = {
    "process": [
        STRIDECategory.SPOOFING,
        STRIDECategory.TAMPERING,
        STRIDECategory.REPUDIATION,
        STRIDECategory.DENIAL_OF_SERVICE,
        STRIDECategory.ELEVATION_OF_PRIVILEGE,
    ],
    "datastore": [
        STRIDECategory.TAMPERING,
        STRIDECategory.INFORMATION_DISCLOSURE,
        STRIDECategory.DENIAL_OF_SERVICE,
    ],
    "external_entity": [
        STRIDECategory.SPOOFING,
        STRIDECategory.TAMPERING,
    ],
    "data_flow": [
        STRIDECategory.TAMPERING,
        STRIDECategory.INFORMATION_DISCLOSURE,
        STRIDECategory.DENIAL_OF_SERVICE,
    ],
}

STRIDE_QUESTIONS: dict[STRIDECategory, str] = {
    STRIDECategory.SPOOFING: "Can an attacker impersonate this component or user?",
    STRIDECategory.TAMPERING: "Can an attacker modify data in transit or at rest?",
    STRIDECategory.REPUDIATION: "Can a user deny performing an action?",
    STRIDECategory.INFORMATION_DISCLOSURE: "Can an attacker access sensitive data?",
    STRIDECategory.DENIAL_OF_SERVICE: "Can an attacker make this component unavailable?",
    STRIDECategory.ELEVATION_OF_PRIVILEGE: "Can an attacker gain unauthorized access?",
}


class STRIDEAnalyzer:
    """Perform STRIDE threat analysis on a system model."""

    def __init__(self, components: list[SystemComponent],
                 boundaries: list[TrustBoundary]) -> None:
        self.components = {c.name: c for c in components}
        self.boundaries = boundaries

    def analyze(self) -> list[Threat]:
        """Run full STRIDE analysis across all components."""
        threats: list[Threat] = []
        for comp in self.components.values():
            comp_threats = self._analyze_component(comp)
            threats.extend(comp_threats)
        return threats

    def _analyze_component(self, component: SystemComponent) -> list[Threat]:
        threats: list[Threat] = []
        type_key = component.type.value if isinstance(component.type, ComponentType) else component.type
        categories = STRIDE_APPlicability.get(type_key, [])

        for category in categories:
            threat = Threat(
                category=category,
                description=STRIDE_QUESTIONS[category],
                component=component.name,
                severity=self._assess_severity(category, component),
            )
            # Find crossing boundaries
            for boundary in self.boundaries:
                if component.name in boundary.components:
                    threat.boundary_crossed = boundary.name
                    break
            threats.append(threat)

        return threats

    def _assess_severity(self, category: STRIDECategory,
                         component: SystemComponent) -> RiskLevel:
        """Simple severity heuristic based on component properties."""
        base = RiskLevel.MEDIUM
        if component.internet_facing:
            base = RiskLevel.HIGH
        if component.data_classification == "sensitive":
            base = RiskLevel.HIGH
        if category == STRIDECategory.ELEVATION_OF_PRIVILEGE:
            base = RiskLevel.HIGH
        return base

    def get_surface_report(self) -> AttackSurfaceReport:
        """Quantify the attack surface."""
        report = AttackSurfaceReport()
        for comp in self.components.values():
            report.total_components += 1
            if comp.internet_facing:
                report.internet_facing += 1
            if comp.type == ComponentType.DATASTORE:
                report.data_stores += 1
            if comp.trust_level == "untrusted":
                report.external_integrations += 1
        report.trust_boundaries = len(self.boundaries)
        report.risk_score = (
            report.internet_facing * 3
            + report.data_stores * 2
            + report.external_integrations * 1.5
            + report.trust_boundaries * 1
        )
        return report


# ---------------------------------------------------------------------------
# Attack Tree
# ---------------------------------------------------------------------------

_COST_MAP = {"low": 1.0, "medium": 5.0, "high": 10.0}


class AttackTree:
    """Attack tree analysis for adversary goal modeling."""

    def __init__(self, root: GoalNode) -> None:
        self.root = root

    def cheapest_path(self) -> AttackPath:
        """Find the cheapest attack path to the root goal."""
        paths = self._enumerate_paths(self.root)
        if not paths:
            return AttackPath()
        return min(paths, key=lambda p: p.total_cost)

    def highest_risk_path(self) -> AttackPath:
        """Find the path with the highest risk score."""
        paths = self._enumerate_paths(self.root)
        if not paths:
            return AttackPath()
        return max(paths, key=lambda p: p.risk_score)

    def _enumerate_paths(self, node: AttackNode) -> list[AttackPath]:
        """Recursively enumerate all leaf-to-root paths."""
        if node.is_leaf:
            cost = _COST_MAP.get(node.cost, 5.0)
            prob = node.success_probability if node.success_probability > 0 else 0.5
            return [AttackPath(
                nodes=[node.method],
                total_cost=cost,
                probability=prob,
            )]

        child_paths: list[AttackPath] = []
        for child in node.children:
            child_paths.extend(self._enumerate_paths(child))

        # Aggregate: for AND nodes, combine probabilities; for OR, pick best
        result: list[AttackPath] = []
        for cp in child_paths:
            path = AttackPath(
                nodes=[node.goal or node.method] + cp.nodes,
                total_cost=cp.total_cost,
                probability=cp.probability,
            )
            result.append(path)
        return result

    def stats(self) -> dict[str, Any]:
        """Get summary statistics for the attack tree."""
        paths = self._enumerate_paths(self.root)
        costs = [p.total_cost for p in paths]
        probs = [p.probability for p in paths]
        return {
            "total_paths": len(paths),
            "min_cost": min(costs) if costs else 0,
            "max_cost": max(costs) if costs else 0,
            "avg_cost": sum(costs) / len(costs) if costs else 0,
            "max_depth": self.root.depth,
            "avg_probability": sum(probs) / len(probs) if probs else 0,
        }


# ---------------------------------------------------------------------------
# DREAD Scorer
# ---------------------------------------------------------------------------

class DREADScorer:
    """Score threats using the DREAD risk model."""

    @staticmethod
    def score(threat_name: str, factors: dict[str, int]) -> DREADScore:
        """Score a threat. Factors: damage, reproducibility, exploitability,
        affected_users, discoverability (each 1-10)."""
        return DREADScore(
            threat_name=threat_name,
            damage=max(1, min(10, factors.get("damage", 5))),
            reproducibility=max(1, min(10, factors.get("reproducibility", 5))),
            exploitability=max(1, min(10, factors.get("exploitability", 5))),
            affected_users=max(1, min(10, factors.get("affected_users", 5))),
            discoverability=max(1, min(10, factors.get("discoverability", 5))),
        )

    @staticmethod
    def prioritize(scores: list[DREADScore]) -> list[DREADScore]:
        """Sort threats by DREAD score descending."""
        return sorted(scores, key=lambda s: s.average, reverse=True)


# ---------------------------------------------------------------------------
# Mitigation Tracker
# ---------------------------------------------------------------------------

@dataclass
class MitigationAction:
    """A single mitigation action for a threat."""
    threat_id: str
    action: str
    status: MitigationStatus = MitigationStatus.NOT_STARTED
    owner: str = ""
    due_date: str = ""
    notes: str = ""


class MitigationTracker:
    """Track mitigation actions for identified threats."""

    def __init__(self) -> None:
        self._actions: list[MitigationAction] = []

    def add_action(self, threat_id: str, action: str, owner: str = "",
                   due_date: str = "") -> MitigationAction:
        ma = MitigationAction(
            threat_id=threat_id, action=action,
            owner=owner, due_date=due_date
        )
        self._actions.append(ma)
        return ma

    def update_status(self, threat_id: str, action_index: int,
                      status: MitigationStatus) -> None:
        matches = [a for a in self._actions if a.threat_id == threat_id]
        if action_index < len(matches):
            matches[action_index].status = status

    def get_summary(self) -> dict[str, int]:
        summary: dict[str, int] = {}
        for status in MitigationStatus:
            summary[status.value] = sum(
                1 for a in self._actions if a.status == status
            )
        return summary

    def get_overdue(self, current_date: str = "") -> list[MitigationAction]:
        return [
            a for a in self._actions
            if a.status != MitigationStatus.VERIFIED
            and a.due_date
            and a.due_date < current_date
        ]


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the threat modeling framework."""
    print("=" * 60)
    print("  Threat Modeling Framework Demo")
    print("=" * 60)

    # --- STRIDE Analysis ---
    print("\n--- STRIDE Analysis ---")
    components = [
        SystemComponent("WebApp", type="process", trust_level="semi-trusted",
                        internet_facing=True, data_classification="sensitive"),
        SystemComponent("APIGateway", type="process", trust_level="trusted"),
        SystemComponent("Database", type="datastore", trust_level="internal",
                        data_classification="sensitive"),
        SystemComponent("UserBrowser", type="external_entity",
                        trust_level="untrusted"),
        SystemComponent("ThirdPartyAPI", type="external_entity",
                        trust_level="untrusted"),
    ]
    boundaries = [
        TrustBoundary("Internet", components=["UserBrowser", "WebApp"]),
        TrustBoundary("DMZ", components=["WebApp", "APIGateway"]),
        TrustBoundary("Internal", components=["APIGateway", "Database"]),
    ]

    analyzer = STRIDEAnalyzer(components, boundaries)
    threats = analyzer.analyze()

    print(f"  Components analyzed: {len(components)}")
    print(f"  Threats identified:  {len(threats)}")
    for t in threats[:6]:
        print(f"    [{t.category.value:30s}] {t.component}")
        print(f"      {t.description}")
        print(f"      Severity: {t.severity.value}")

    # --- Attack Surface ---
    surface = analyzer.get_surface_report()
    print(f"\n  Attack Surface Score: {surface.risk_score}")
    print(f"  Internet-facing:      {surface.internet_facing}")
    print(f"  Data stores:          {surface.data_stores}")
    print(f"  Trust boundaries:     {surface.trust_boundaries}")

    # --- Attack Tree ---
    print("\n--- Attack Tree ---")
    tree = AttackTree(root=GoalNode(
        goal="Exfiltrate customer PII",
        attacker="External",
        children=[
            AttackNode(method="SQL Injection", cost="low",
                       success_probability=0.6),
            AttackNode(method="Compromise admin creds", cost="medium",
                       success_probability=0.3,
                       children=[
                           AttackNode(method="Credential stuffing", cost="low"),
                           AttackNode(method="Phishing", cost="medium"),
                       ]),
            AttackNode(method="SSRF via webhook", cost="low",
                       success_probability=0.4),
        ]
    ))

    cheapest = tree.cheapest_path()
    highest_risk = tree.highest_risk_path()
    stats = tree.stats()

    print(f"  Total paths:     {stats['total_paths']}")
    print(f"  Max depth:       {stats['max_depth']}")
    print(f"  Cheapest path:   {' → '.join(cheapest.nodes)}")
    print(f"    Cost: {cheapest.total_cost}, Prob: {cheapest.probability:.1f}")
    print(f"  Highest risk:    {' → '.join(highest_risk.nodes)}")
    print(f"    Risk score: {highest_risk.risk_score:.1f}")

    # --- DREAD Scoring ---
    print("\n--- DREAD Scoring ---")
    scorer = DREADScorer()
    scores = [
        scorer.score("SQL Injection", {"damage": 10, "reproducibility": 8,
                     "exploitability": 7, "affected_users": 9,
                     "discoverability": 6}),
        scorer.score("XSS in profile", {"damage": 6, "reproducibility": 9,
                     "exploitability": 8, "affected_users": 7,
                     "discoverability": 7}),
        scorer.score("SSRF via webhook", {"damage": 8, "reproducibility": 6,
                     "exploitability": 5, "affected_users": 4,
                     "discoverability": 4}),
    ]
    prioritized = scorer.prioritize(scores)
    for s in prioritized:
        print(f"  {s.threat_name:25s}: DREAD={s.average:.1f} ({s.risk_level.value})")

    # --- Mitigation Tracker ---
    print("\n--- Mitigation Tracker ---")
    tracker = MitigationTracker()
    for t in threats[:3]:
        tracker.add_action(t.id, f"Mitigate {t.category.value}",
                           owner="security-team", due_date="2024-06-01")
    summary = tracker.get_summary()
    print(f"  Actions: {summary}")

    print("\n" + "=" * 60)
    print("  Demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
