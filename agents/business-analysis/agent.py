"""
Business Analysis Agent — Enterprise-Grade Requirements & Process Analysis Engine.

A comprehensive business analysis framework covering the full BA lifecycle:
requirements elicitation, stakeholder management, process modeling, gap analysis,
SWOT intelligence, solution design, traceability, change impact assessment,
risk management, and handoff documentation.

Designed for senior business analysts working across waterfall, agile, and hybrid
methodologies. Supports BPMN/UML notation, RACI matrices, INVEST-compliant user
stories, and traceability from business need through acceptance criteria.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import re
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from typing import (
    Any, Callable, Dict, List, Optional, Set, Tuple, Union
)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logger = logging.getLogger("BusinessAnalysisAgent")
logger.setLevel(logging.DEBUG)
_handler = logging.StreamHandler()
_handler.setFormatter(
    logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")
)
logger.addHandler(_handler)


# ══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ══════════════════════════════════════════════════════════════════════════════

class RequirementType(Enum):
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    BUSINESS = "business"
    TECHNICAL = "technical"
    TRANSITION = "transition"
    CONSTRAINT = "constraint"


class PriorityLevel(Enum):
    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1


class RequirementStatus(Enum):
    DRAFT = "draft"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    IMPLEMENTED = "implemented"
    VERIFIED = "verified"
    REJECTED = "rejected"


class AnalysisPhase(Enum):
    DISCOVERY = "discovery"
    ANALYSIS = "analysis"
    DESIGN = "design"
    VALIDATION = "validation"
    HANDOFF = "handoff"


class StakeholderType(Enum):
    EXECUTIVE = "executive"
    BUSINESS = "business"
    TECHNICAL = "technical"
    END_USER = "end_user"
    VENDOR = "vendor"


class ProcessComplexity(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    HIGHLY_COMPLEX = "highly_complex"


class GapType(Enum):
    PROCESS = "process"
    TECHNOLOGY = "technology"
    PEOPLE = "people"
    DATA = "data"
    GOVERNANCE = "governance"


class SWOTCategory(Enum):
    STRENGTH = "strength"
    WEAKNESS = "weakness"
    OPPORTUNITY = "opportunity"
    THREAT = "threat"


class DocumentType(Enum):
    BRD = "brd"
    SRS = "srs"
    FRD = "frd"
    USP = "usp"
    NFR = "nfr"


class ModelingNotation(Enum):
    BPMN = "bpmn"
    UML = "uml"
    EPC = "epc"
    FLOWCHART = "flowchart"


class ChangeType(Enum):
    ORGANIZATIONAL = "organizational"
    TECHNOLOGICAL = "technological"
    PROCESS = "process"
    POLICY = "policy"


class RiskLevel(Enum):
    NEGLIGIBLE = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5


# ══════════════════════════════════════════════════════════════════════════════
# DATACLASSES
# ══════════════════════════════════════════════════════════════════════════════

def _uid(prefix: str = "id") -> str:
    """Generate a short unique identifier."""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


@dataclass
class Requirement:
    """A single business or technical requirement."""
    id: str = field(default_factory=lambda: _uid("REQ"))
    title: str = ""
    description: str = ""
    type: RequirementType = RequirementType.FUNCTIONAL
    priority: PriorityLevel = PriorityLevel.MEDIUM
    status: RequirementStatus = RequirementStatus.DRAFT
    rationale: str = ""
    acceptance_criteria: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    stakeholder_ids: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    version: int = 1
    estimated_effort: Optional[str] = None
    source: str = ""
    notes: str = ""

    def is_approved(self) -> bool:
        return self.status == RequirementStatus.APPROVED

    def is_critical(self) -> bool:
        return self.priority == PriorityLevel.CRITICAL

    def hash_content(self) -> str:
        payload = f"{self.title}|{self.description}|{self.type.value}"
        return hashlib.sha256(payload.encode()).hexdigest()[:16]


@dataclass
class StakeholderProfile:
    """Stakeholder information including RACI assignments."""
    id: str = field(default_factory=lambda: _uid("STK"))
    name: str = ""
    role: str = ""
    stakeholder_type: StakeholderType = StakeholderType.BUSINESS
    influence: int = 5  # 1-10 scale
    interest: int = 5  # 1-10 scale
    raci: Dict[str, str] = field(default_factory=dict)  # activity -> R/A/C/I
    communication_preference: str = "email"
    availability: str = "full_time"
    concerns: List[str] = field(default_factory=list)
    expectations: List[str] = field(default_factory=list)
    department: str = ""
    contact_info: str = ""
    power_interest_position: str = ""  # quadrant label


@dataclass
class ProcessModel:
    """A modeled business process with activities, decisions, and flows."""
    id: str = field(default_factory=lambda: _uid("PRC"))
    name: str = ""
    description: str = ""
    notation: ModelingNotation = ModelingNotation.BPMN
    complexity: ProcessComplexity = ProcessComplexity.MODERATE
    activities: List[Dict[str, Any]] = field(default_factory=list)
    decisions: List[Dict[str, Any]] = field(default_factory=list)
    events: List[Dict[str, Any]] = field(default_factory=list)
    swimlanes: List[str] = field(default_factory=list)
    flows: List[Dict[str, Any]] = field(default_factory=list)
    exceptions: List[str] = field(default_factory=list)
    kpis: List[str] = field(default_factory=list)
    inefficiencies: List[str] = field(default_factory=list)
    cycle_time_seconds: float = 0.0
    throughput_per_hour: float = 0.0
    bottlenecks: List[str] = field(default_factory=list)


@dataclass
class GapAnalysisResult:
    """Result of a gap analysis between current and desired states."""
    id: str = field(default_factory=lambda: _uid("GAP"))
    gap_type: GapType = GapType.PROCESS
    description: str = ""
    current_state: str = ""
    desired_state: str = ""
    severity: PriorityLevel = PriorityLevel.MEDIUM
    root_cause: str = ""
    recommendation: str = ""
    estimated_effort: str = ""
    dependencies: List[str] = field(default_factory=list)
    risk_if_unaddressed: str = ""


@dataclass
class SWOTAnalysis:
    """Full SWOT analysis with weighted scoring."""
    id: str = field(default_factory=lambda: _uid("SWOT"))
    entity: str = ""
    context: str = ""
    strengths: List[Dict[str, Any]] = field(default_factory=list)
    weaknesses: List[Dict[str, Any]] = field(default_factory=list)
    opportunities: List[Dict[str, Any]] = field(default_factory=list)
    threats: List[Dict[str, Any]] = field(default_factory=list)
    weighted_scores: Dict[str, float] = field(default_factory=dict)
    strategic_implications: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class BusinessCase:
    """Business case with financial justification."""
    id: str = field(default_factory=lambda: _uid("BC"))
    problem_statement: str = ""
    proposed_solution: str = ""
    alternatives: List[Dict[str, Any]] = field(default_factory=list)
    costs: Dict[str, float] = field(default_factory=dict)
    benefits: Dict[str, float] = field(default_factory=dict)
    npv: float = 0.0
    irr: float = 0.0
    roi: float = 0.0
    payback_period_months: float = 0.0
    risk_adjusted_roi: float = 0.0
    strategic_alignment: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    recommendation: str = ""
    confidence_level: str = "medium"


@dataclass
class UserStory:
    """An INVEST-compliant user story."""
    id: str = field(default_factory=lambda: _uid("US"))
    title: str = ""
    persona: str = ""
    action: str = ""
    benefit: str = ""
    story_text: str = ""
    priority: PriorityLevel = PriorityLevel.MEDIUM
    story_points: int = 0
    invest_score: float = 0.0
    acceptance_criteria: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    epic_id: Optional[str] = None
    theme: str = ""
    status: str = "backlog"

    def to_invest_text(self) -> str:
        return (
            f"As a {self.persona}, I want to {self.action}, "
            f"so that {self.benefit}."
        )


@dataclass
class UseCase:
    """A structured use case with actors, preconditions, and flows."""
    id: str = field(default_factory=lambda: _uid("UC"))
    name: str = ""
    actor: str = ""
    preconditions: List[str] = field(default_factory=list)
    postconditions: List[str] = field(default_factory=list)
    main_flow: List[str] = field(default_factory=list)
    alternative_flows: List[str] = field(default_factory=list)
    exception_flows: List[str] = field(default_factory=list)
    priority: PriorityLevel = PriorityLevel.MEDIUM
    complexity: ProcessComplexity = ProcessComplexity.MODERATE


@dataclass
class AcceptanceCriteria:
    """Testable acceptance criteria for a requirement or user story."""
    id: str = field(default_factory=lambda: _uid("AC"))
    requirement_id: str = ""
    given: str = ""
    when: str = ""
    then: str = ""
    status: str = "pending"
    test_data: str = ""
    verified_by: str = ""


@dataclass
class TraceabilityMatrix:
    """Requirements traceability linking business need to verification."""
    id: str = field(default_factory=lambda: _uid("TRM"))
    business_need: str = ""
    requirement_ids: List[str] = field(default_factory=list)
    design_ids: List[str] = field(default_factory=list)
    test_ids: List[str] = field(default_factory=list)
    coverage_percentage: float = 0.0
    gaps: List[str] = field(default_factory=list)
    forward_trace: Dict[str, List[str]] = field(default_factory=dict)
    backward_trace: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class ChangeRequest:
    """A formal change request for impact assessment."""
    id: str = field(default_factory=lambda: _uid("CR"))
    title: str = ""
    description: str = ""
    change_type: ChangeType = ChangeType.PROCESS
    requestor: str = ""
    date_submitted: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    priority: PriorityLevel = PriorityLevel.MEDIUM
    affected_areas: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    status: str = "submitted"


@dataclass
class RiskAssessment:
    """A identified risk with mitigation strategy."""
    id: str = field(default_factory=lambda: _uid("RSK"))
    title: str = ""
    description: str = ""
    probability: float = 0.5  # 0.0 - 1.0
    impact: float = 0.5  # 0.0 - 1.0
    risk_level: RiskLevel = RiskLevel.MEDIUM
    mitigation_strategy: str = ""
    contingency_plan: str = ""
    owner: str = ""
    status: str = "open"
    category: str = ""

    @property
    def risk_score(self) -> float:
        return round(self.probability * self.impact * 5, 2)


@dataclass
class BusinessRule:
    """A business rule governing system behavior."""
    id: str = field(default_factory=lambda: _uid("BR"))
    name: str = ""
    description: str = ""
    rule_type: str = "validation"  # validation, decision, calculation, constraint
    logic: str = ""
    exceptions: List[str] = field(default_factory=list)
    related_requirements: List[str] = field(default_factory=list)
    effective_date: str = ""
    expiry_date: str = ""


@dataclass
class DataFlowModel:
    """Data flow model capturing movement of data through a system."""
    id: str = field(default_factory=lambda: _uid("DFM"))
    system_name: str = ""
    entities: List[str] = field(default_factory=list)
    processes: List[Dict[str, Any]] = field(default_factory=list)
    data_stores: List[str] = field(default_factory=list)
    flows: List[Dict[str, Any]] = field(default_factory=list)
    trust_boundaries: List[str] = field(default_factory=list)
    external_interfaces: List[str] = field(default_factory=list)


@dataclass
class FunctionalDecomposition:
    """Hierarchical decomposition of system functionality."""
    id: str = field(default_factory=lambda: _uid("FD"))
    root_function: str = ""
    level_1_functions: List[str] = field(default_factory=list)
    level_2_map: Dict[str, List[str]] = field(default_factory=dict)
    level_3_map: Dict[str, List[str]] = field(default_factory=dict)
    coverage_matrix: Dict[str, str] = field(default_factory=dict)


@dataclass
class ImpactAssessment:
    """Assessment of change impact across organizational dimensions."""
    id: str = field(default_factory=lambda: _uid("IA"))
    change_request_id: str = ""
    organizational_impact: str = ""
    technical_impact: str = ""
    process_impact: str = ""
    people_impact: str = ""
    data_impact: str = ""
    estimated_cost: float = 0.0
    estimated_duration_weeks: int = 0
    risk_level: RiskLevel = RiskLevel.MEDIUM
    recommendation: str = ""
    affected_stakeholders: List[str] = field(default_factory=list)
    rollback_plan: str = ""


@dataclass
class SolutionDesign:
    """Solution design with alternatives analysis."""
    id: str = field(default_factory=lambda: _uid("SD"))
    name: str = ""
    description: str = ""
    alternatives: List[Dict[str, Any]] = field(default_factory=list)
    selected_alternative: str = ""
    architecture_components: List[str] = field(default_factory=list)
    integration_points: List[str] = field(default_factory=list)
    technology_stack: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    estimated_timeline_weeks: int = 0


@dataclass
class ProjectScope:
    """Defined project scope with boundaries."""
    id: str = field(default_factory=lambda: _uid("SC"))
    name: str = ""
    objectives: List[str] = field(default_factory=list)
    in_scope: List[str] = field(default_factory=list)
    out_of_scope: List[str] = field(default_factory=list)
    deliverables: List[str] = field(default_factory=list)
    milestones: List[Dict[str, str]] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    exclusions: List[str] = field(default_factory=list)


@dataclass
class BusinessMetric:
    """A measurable business metric with baseline and target."""
    id: str = field(default_factory=lambda: _uid("BM"))
    name: str = ""
    description: str = ""
    category: str = ""  # efficiency, quality, cost, time, satisfaction
    baseline_value: float = 0.0
    target_value: float = 0.0
    current_value: float = 0.0
    unit: str = ""
    measurement_frequency: str = ""
    owner: str = ""


@dataclass
class RetrospectiveNote:
    """A retrospective note capturing lessons learned."""
    id: str = field(default_factory=lambda: _uid("RET"))
    category: str = ""  # went_well, to_improve, action_item
    description: str = ""
    author: str = ""
    date: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    action_required: bool = False
    assigned_to: str = ""


# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class BAConfig:
    """Configuration for the Business Analysis Agent."""
    documentation_format: DocumentType = DocumentType.BRD
    review_cycles: int = 2
    default_notation: ModelingNotation = ModelingNotation.BPMN
    risk_threshold: float = 0.6
    invest_weights: Dict[str, float] = field(default_factory=lambda: {
        "independent": 0.15,
        "negotiable": 0.10,
        "valuable": 0.20,
        "estimable": 0.15,
        "small": 0.20,
        "testable": 0.20,
    })
    stakeholder_engagement_model: str = "agile"  # agile, waterfall, hybrid
    auto_generate_acceptance_criteria: bool = True
    max_risk_score_before_escalation: float = 3.5
    currency: str = "USD"
    discount_rate: float = 0.10  # 10% for NPV calculation


# ══════════════════════════════════════════════════════════════════════════════
# HELPER / PRIVATE UTILITIES
# ══════════════════════════════════════════════════════════════════════════════

def _calculate_npv(discount_rate: float, cashflows: List[float]) -> float:
    """Net Present Value of a cash-flow series."""
    return sum(cf / ((1 + discount_rate) ** t) for t, cf in enumerate(cashflows))


def _calculate_irr(cashflows: List[float], tolerance: float = 1e-6,
                   max_iter: int = 1000) -> float:
    """Internal Rate of Return via Newton-Raphson."""
    rate = 0.1
    for _ in range(max_iter):
        npv = sum(cf / ((1 + rate) ** t) for t, cf in enumerate(cashflows))
        dnpv = sum(
            -t * cf / ((1 + rate) ** (t + 1))
            for t, cf in enumerate(cashflows)
        )
        if abs(dnpv) < 1e-12:
            break
        new_rate = rate - npv / dnpv
        if abs(new_rate - rate) < tolerance:
            return round(new_rate, 4)
        rate = new_rate
    return round(rate, 4)


def _classify_risk(probability: float, impact: float) -> RiskLevel:
    """Classify risk level from probability and impact."""
    score = probability * impact
    if score < 0.05:
        return RiskLevel.NEGLIGIBLE
    elif score < 0.15:
        return RiskLevel.LOW
    elif score < 0.35:
        return RiskLevel.MEDIUM
    elif score < 0.65:
        return RiskLevel.HIGH
    else:
        return RiskLevel.CRITICAL


def _power_interest_quadrant(influence: int, interest: int) -> str:
    """Map stakeholder to power/interest grid quadrant."""
    if influence >= 6 and interest >= 6:
        return "manage_closely"
    elif influence >= 6 and interest < 6:
        return "keep_satisfied"
    elif influence < 6 and interest >= 6:
        return "keep_informed"
    else:
        return "monitor"


def _estimate_story_points(story: UserStory) -> int:
    """Rough T-shirt sizing for story points."""
    text_len = len(story.story_text)
    if text_len < 60:
        return 2
    elif text_len < 120:
        return 3
    elif text_len < 200:
        return 5
    elif text_len < 300:
        return 8
    else:
        return 13


def _validate_invest(story: UserStory, weights: Dict[str, float]) -> float:
    """Score a user story against INVEST criteria (0-100)."""
    scores: Dict[str, float] = {}
    # Independent: few dependencies
    scores["independent"] = max(0, 1.0 - 0.2 * len(story.dependencies))
    # Negotiable: story text is concise but not over-specified
    word_count = len(story.story_text.split())
    scores["negotiable"] = 1.0 if 10 <= word_count <= 30 else 0.5
    # Valuable: benefit clause exists
    scores["valuable"] = 1.0 if story.benefit and len(story.benefit) > 5 else 0.3
    # Estimable: we have enough detail
    scores["estimable"] = 1.0 if story.persona and story.action else 0.4
    # Small: story points <= 8
    scores["small"] = 1.0 if story.story_points <= 8 else 0.5
    # Testable: acceptance criteria exist
    scores["testable"] = (
        1.0 if len(story.acceptance_criteria) >= 2 else 0.3
    )
    weighted = sum(
        scores.get(k, 0) * weights.get(k, 0.16) for k in weights
    )
    return round(weighted * 100, 1)


def _assess_complexity(activity_count: int, decision_count: int,
                       swimlanes: int) -> ProcessComplexity:
    """Determine process complexity from structural metrics."""
    score = activity_count + decision_count * 2 + swimlanes * 3
    if score < 8:
        return ProcessComplexity.SIMPLE
    elif score < 18:
        return ProcessComplexity.MODERATE
    elif score < 35:
        return ProcessComplexity.COMPLEX
    else:
        return ProcessComplexity.HIGHLY_COMPLEX


# ══════════════════════════════════════════════════════════════════════════════
# MAIN AGENT CLASS
# ══════════════════════════════════════════════════════════════════════════════

class BusinessAnalysisAgent:
    """
    Enterprise business analysis agent providing end-to-end BA capabilities.

    Covers discovery through handoff with structured artifacts for each phase.
    """

    def __init__(self, config: Optional[BAConfig] = None):
        self._config = config or BAConfig()
        self._requirements: Dict[str, Requirement] = {}
        self._stakeholders: Dict[str, StakeholderProfile] = {}
        self._processes: Dict[str, ProcessModel] = {}
        self._user_stories: Dict[str, UserStory] = {}
        self._risks: Dict[str, RiskAssessment] = {}
        self._change_requests: Dict[str, ChangeRequest] = {}
        self._business_rules: Dict[str, BusinessRule] = {}
        self._traceability: Dict[str, TraceabilityMatrix] = {}
        self._metrics: Dict[str, BusinessMetric] = {}
        self._phase: AnalysisPhase = AnalysisPhase.DISCOVERY
        self._project_id: Optional[str] = None
        logger.info("BusinessAnalysisAgent initialized (format=%s)",
                     self._config.documentation_format.value)

    # ----------------------------------------------------------------────---
    # Public API — Requirements Elicitation
    # -----------------------------------------------------------------------

    def gather_requirements(
        self,
        project_id: str,
        method: str = "workshop",
    ) -> List[Requirement]:
        """
        Elicit requirements using a specified technique.

        Supported methods: workshop, interview, survey, observation,
        document_analysis, brainstorming, prototyping, focus_group.
        Returns a list of Requirement objects stored in the agent.
        """
        logger.info("Gathering requirements for %s via %s", project_id, method)
        self._project_id = project_id
        techniques = {
            "workshop": self._requirements_from_workshop,
            "interview": self._requirements_from_interviews,
            "survey": self._requirements_from_surveys,
            "observation": self._requirements_from_observation,
            "document_analysis": self._requirements_from_docs,
            "brainstorming": self._requirements_from_brainstorming,
            "prototyping": self._requirements_from_prototyping,
            "focus_group": self._requirements_from_focus_group,
        }
        factory = techniques.get(method, self._requirements_from_workshop)
        new_reqs = factory(project_id)
        for req in new_reqs:
            self._requirements[req.id] = req
        logger.info("Collected %d requirements via %s", len(new_reqs), method)
        return new_reqs

    def _requirements_from_workshop(self, project_id: str) -> List[Requirement]:
        """Simulate workshop-derived requirements."""
        templates = [
            ("User login with MFA", RequirementType.FUNCTIONAL,
             PriorityLevel.CRITICAL, "Users must authenticate with MFA for security."),
            ("Dashboard response < 2s", RequirementType.NON_FUNCTIONAL,
             PriorityLevel.HIGH, "Performance SLA for analytics dashboard."),
            ("Comply with GDPR data handling", RequirementType.BUSINESS,
             PriorityLevel.CRITICAL, "Regulatory compliance requirement."),
            ("REST API for mobile clients", RequirementType.TECHNICAL,
             PriorityLevel.HIGH, "API layer for mobile integration."),
            ("Data migration from legacy system", RequirementType.TRANSITION,
             PriorityLevel.MEDIUM, "Transition plan for existing data."),
            ("Max concurrent users = 10,000", RequirementType.CONSTRAINT,
             PriorityLevel.HIGH, "Infrastructure capacity constraint."),
        ]
        return [
            Requirement(
                title=t[0], type=t[1], priority=t[2], rationale=t[3],
                source="workshop", tags=["workshop", project_id],
            )
            for t in templates
        ]

    def _requirements_from_interviews(self, project_id: str) -> List[Requirement]:
        templates = [
            ("Customer self-service portal", RequirementType.FUNCTIONAL,
             PriorityLevel.HIGH, "Reduce support call volume by 40%."),
            ("Automated report generation", RequirementType.FUNCTIONAL,
             PriorityLevel.MEDIUM, "Replace manual Excel reports."),
            ("Audit trail for all transactions", RequirementType.NON_FUNCTIONAL,
             PriorityLevel.HIGH, "Regulatory audit requirement."),
        ]
        return [
            Requirement(
                title=t[0], type=t[1], priority=t[2], rationale=t[3],
                source="interviews", tags=["interviews", project_id],
            )
            for t in templates
        ]

    def _requirements_from_surveys(self, project_id: str) -> List[Requirement]:
        templates = [
            ("Mobile-responsive interface", RequirementType.FUNCTIONAL,
             PriorityLevel.HIGH, "60% of users access via mobile."),
            ("Single sign-on integration", RequirementType.TECHNICAL,
             PriorityLevel.MEDIUM, "Reduce password fatigue."),
        ]
        return [
            Requirement(
                title=t[0], type=t[1], priority=t[2], rationale=t[3],
                source="survey", tags=["survey", project_id],
            )
            for t in templates
        ]

    def _requirements_from_observation(self, project_id: str) -> List[Requirement]:
        templates = [
            ("Streamline approval workflow", RequirementType.PROCESS,
             PriorityLevel.HIGH, "Current 7-step approval causes 3-day delays."),
            ("Auto-populate customer data", RequirementType.FUNCTIONAL,
             PriorityLevel.MEDIUM, "Reduce data entry errors."),
        ]
        return [
            Requirement(
                title=t[0], type=t[1], priority=t[2], rationale=t[3],
                source="observation", tags=["observation", project_id],
            )
            for t in templates
        ]

    def _requirements_from_docs(self, project_id: str) -> List[Requirement]:
        templates = [
            ("Legacy API compatibility layer", RequirementType.TECHNICAL,
             PriorityLevel.HIGH, "Existing integrations must not break."),
            ("Data retention policy enforcement", RequirementType.CONSTRAINT,
             PriorityLevel.MEDIUM, "7-year data retention per regulation."),
        ]
        return [
            Requirement(
                title=t[0], type=t[1], priority=t[2], rationale=t[3],
                source="document_analysis", tags=["docs", project_id],
            )
            for t in templates
        ]

    def _requirements_from_brainstorming(self, project_id: str) -> List[Requirement]:
        templates = [
            ("AI-powered anomaly detection", RequirementType.FUNCTIONAL,
             PriorityLevel.MEDIUM, "Proactive fraud detection."),
            ("Real-time collaboration features", RequirementType.FUNCTIONAL,
             PriorityLevel.LOW, "Future-state consideration."),
        ]
        return [
            Requirement(
                title=t[0], type=t[1], priority=t[2], rationale=t[3],
                source="brainstorming", tags=["brainstorm", project_id],
            )
            for t in templates
        ]

    def _requirements_from_prototyping(self, project_id: str) -> List[Requirement]:
        templates = [
            ("Drag-and-drop report builder", RequirementType.FUNCTIONAL,
             PriorityLevel.MEDIUM, "User feedback on prototype was positive."),
        ]
        return [
            Requirement(
                title=t[0], type=t[1], priority=t[2], rationale=t[3],
                source="prototyping", tags=["prototype", project_id],
            )
            for t in templates
        ]

    def _requirements_from_focus_group(self, project_id: str) -> List[Requirement]:
        templates = [
            ("Role-based dashboard views", RequirementType.FUNCTIONAL,
             PriorityLevel.HIGH, "Different roles need different data."),
            ("Configurable notification preferences", RequirementType.FUNCTIONAL,
             PriorityLevel.LOW, "User satisfaction improvement."),
        ]
        return [
            Requirement(
                title=t[0], type=t[1], priority=t[2], rationale=t[3],
                source="focus_group", tags=["focus_group", project_id],
            )
            for t in templates
        ]

    # -----------------------------------------------------------------------
    # Stakeholder Mapping
    # -----------------------------------------------------------------------

    def create_stakeholder_map(
        self, project_id: str
    ) -> Dict[str, Any]:
        """
        Build a RACI matrix and power/interest grid for all stakeholders.

        Returns a dict with 'raci_matrix', 'power_interest_grid',
        and 'engagement_plan'.
        """
        logger.info("Creating stakeholder map for %s", project_id)
        profiles = self._generate_default_stakeholders(project_id)
        for p in profiles:
            self._stakeholders[p.id] = p

        activities = [
            "Requirements Gathering", "Solution Design", "Development",
            "Testing", "Deployment", "Change Management",
        ]

        raci_matrix: Dict[str, Dict[str, str]] = {}
        for activity in activities:
            raci_matrix[activity] = {}
            for p in profiles:
                raci_matrix[activity][p.name] = self._assign_raci(
                    p.stakeholder_type, activity
                )

        grid: Dict[str, List[str]] = {
            "manage_closely": [],
            "keep_satisfied": [],
            "keep_informed": [],
            "monitor": [],
        }
        for p in profiles:
            grid[p.power_interest_position].append(p.name)

        engagement_plan = self._build_engagement_plan(profiles)
        return {
            "raci_matrix": raci_matrix,
            "power_interest_grid": grid,
            "engagement_plan": engagement_plan,
            "stakeholder_count": len(profiles),
        }

    def _generate_default_stakeholders(
        self, project_id: str
    ) -> List[StakeholderProfile]:
        raw = [
            ("CTO", StakeholderType.EXECUTIVE, 9, 7, "executive_summary"),
            ("Product Owner", StakeholderType.BUSINESS, 7, 9, "daily_standup"),
            ("Lead Developer", StakeholderType.TECHNICAL, 6, 8, "technical_review"),
            ("End Users", StakeholderType.END_USER, 3, 8, "usability_testing"),
            ("Vendor PM", StakeholderType.VENDOR, 4, 5, "weekly_status"),
        ]
        profiles = []
        for name, stype, inf, int_, comm in raw:
            p = StakeholderProfile(
                name=name, role=name, stakeholder_type=stype,
                influence=inf, interest=int_,
                communication_preference=comm,
                power_interest_position=_power_interest_quadrant(inf, int_),
            )
            profiles.append(p)
        return profiles

    def _assign_raci(self, stype: StakeholderType, activity: str) -> str:
        mapping = {
            StakeholderType.EXECUTIVE: {"Requirements Gathering": "I",
                                         "Solution Design": "A",
                                         "Development": "I",
                                         "Testing": "I",
                                         "Deployment": "A",
                                         "Change Management": "A"},
            StakeholderType.BUSINESS: {"Requirements Gathering": "A",
                                        "Solution Design": "R",
                                        "Development": "I",
                                        "Testing": "C",
                                        "Deployment": "C",
                                        "Change Management": "R"},
            StakeholderType.TECHNICAL: {"Requirements Gathering": "C",
                                         "Solution Design": "R",
                                         "Development": "R",
                                         "Testing": "R",
                                         "Deployment": "R",
                                         "Change Management": "C"},
            StakeholderType.END_USER: {"Requirements Gathering": "C",
                                        "Solution Design": "I",
                                        "Development": "I",
                                        "Testing": "R",
                                        "Deployment": "I",
                                        "Change Management": "C"},
            StakeholderType.VENDOR: {"Requirements Gathering": "C",
                                      "Solution Design": "C",
                                      "Development": "R",
                                      "Testing": "C",
                                      "Deployment": "R",
                                      "Change Management": "I"},
        }
        return mapping.get(stype, {}).get(activity, "I")

    def _build_engagement_plan(
        self, profiles: List[StakeholderProfile]
    ) -> List[Dict[str, str]]:
        plan = []
        for p in profiles:
            plan.append({
                "stakeholder": p.name,
                "frequency": "daily" if p.power_interest_position == "manage_closely"
                             else "weekly",
                "channel": p.communication_preference,
                "key_message": self._key_message_for(p.stakeholder_type),
            })
        return plan

    def _key_message_for(self, stype: StakeholderType) -> str:
        return {
            StakeholderType.EXECUTIVE: "Strategic alignment and ROI progress",
            StakeholderType.BUSINESS: "Feature delivery and business value",
            StakeholderType.TECHNICAL: "Architecture decisions and technical debt",
            StakeholderType.END_USER: "Usability improvements and training",
            StakeholderType.VENDOR: "Integration timelines and deliverables",
        }.get(stype, "General project status")

    # -----------------------------------------------------------------------
    # Process Modeling
    # -----------------------------------------------------------------------

    def map_process(
        self,
        process_name: str,
        notation: Optional[ModelingNotation] = None,
    ) -> ProcessModel:
        """
        Model a business process with activities, decisions, flows,
        and complexity analysis.
        """
        notation = notation or self._config.default_notation
        logger.info("Mapping process '%s' in %s notation", process_name, notation.value)

        activities = self._infer_activities(process_name)
        decisions = self._infer_decisions(process_name)
        events = [
            {"type": "start", "name": f"Start: {process_name}"},
            {"type": "end", "name": f"End: {process_name}"},
        ]
        swimlanes = self._infer_swimlanes(process_name)
        flows = self._build_flows(activities, decisions)
        complexity = _assess_complexity(
            len(activities), len(decisions), len(swimlanes)
        )

        model = ProcessModel(
            name=process_name,
            notation=notation,
            complexity=complexity,
            activities=activities,
            decisions=decisions,
            events=events,
            swimlanes=swimlanes,
            flows=flows,
            inefficiencies=self._identify_inefficiencies(activities),
            bottlenecks=self._identify_bottlenecks(activities),
            cycle_time_seconds=self._estimate_cycle_time(activities),
        )
        self._processes[model.id] = model
        return model

    def _infer_activities(self, process_name: str) -> List[Dict[str, Any]]:
        base = process_name.lower().replace(" ", "_")
        templates = [
            {"id": f"act_1", "name": f"Initiate {process_name}", "type": "task",
             "assignee": "Requestor"},
            {"id": f"act_2", "name": f"Validate {process_name} Data", "type": "task",
             "assignee": "Analyst"},
            {"id": f"act_3", "name": f"Review {process_name}", "type": "task",
             "assignee": "Approver"},
            {"id": f"act_4", "name": f"Execute {process_name}", "type": "task",
             "assignee": "Executor"},
            {"id": f"act_5", "name": f"Notify Stakeholders", "type": "task",
             "assignee": "System"},
            {"id": f"act_6", "name": f"Archive {process_name} Record", "type": "task",
             "assignee": "System"},
        ]
        return templates

    def _infer_decisions(self, process_name: str) -> List[Dict[str, Any]]:
        return [
            {"id": "dec_1", "name": "Data Valid?", "outcomes": ["yes", "no"]},
            {"id": "dec_2", "name": "Approved?", "outcomes": ["approved", "rejected", "revise"]},
        ]

    def _infer_swimlanes(self, process_name: str) -> List[str]:
        return ["Requestor", "Analyst", "Approver", "System"]

    def _build_flows(self, activities: List[Dict], decisions: List[Dict]) -> List[Dict[str, Any]]:
        flows = []
        for i in range(len(activities) - 1):
            flows.append({
                "from": activities[i]["id"],
                "to": activities[i + 1]["id"],
                "type": "sequence",
            })
        if decisions:
            flows.append({
                "from": activities[-2]["id"],
                "to": decisions[0]["id"],
                "type": "sequence",
            })
        return flows

    def _identify_inefficiencies(self, activities: List[Dict]) -> List[str]:
        return [
            "Manual data entry in step 1 — potential automation",
            "Redundant approval step — consider delegation",
            "No parallel processing for independent steps",
        ]

    def _identify_bottlenecks(self, activities: List[Dict]) -> List[str]:
        return [
            "Approver bottleneck — single point of failure",
            "Manual validation step delays throughput",
        ]

    def _estimate_cycle_time(self, activities: List[Dict]) -> float:
        return len(activities) * 300.0  # 5 minutes average per activity

    # -----------------------------------------------------------------------
    # Gap Analysis
    # -----------------------------------------------------------------------

    def conduct_gap_analysis(
        self,
        current_state: Dict[str, Any],
        desired_state: Dict[str, Any],
    ) -> List[GapAnalysisResult]:
        """
        Comprehensive gap analysis across process, technology, people,
        data, and governance dimensions.
        """
        logger.info("Conducting gap analysis")
        gaps: List[GapAnalysisResult] = []
        for gap_type in GapType:
            current_val = current_state.get(gap_type.value, "Not assessed")
            desired_val = desired_state.get(gap_type.value, "Not assessed")
            if current_val != desired_val:
                gap = GapAnalysisResult(
                    gap_type=gap_type,
                    description=f"Gap in {gap_type.value} dimension",
                    current_state=str(current_val),
                    desired_state=str(desired_val),
                    severity=self._assess_gap_severity(current_val, desired_val),
                    root_cause=self._hypothesize_root_cause(gap_type),
                    recommendation=self._recommend_action(gap_type),
                    risk_if_unaddressed=f"Continued {gap_type.value} gap degrades performance",
                )
                gaps.append(gap)
        if not gaps:
            gaps.append(GapAnalysisResult(
                description="No significant gaps identified",
                severity=PriorityLevel.LOW,
                recommendation="Continue monitoring",
            ))
        return gaps

    def _assess_gap_severity(self, current: Any, desired: Any) -> PriorityLevel:
        if str(current) == "Not assessed" or str(desired) == "Not assessed":
            return PriorityLevel.MEDIUM
        return PriorityLevel.HIGH

    def _hypothesize_root_cause(self, gap_type: GapType) -> str:
        causes = {
            GapType.PROCESS: "Undocumented or outdated process flows",
            GapType.TECHNOLOGY: "Legacy system limitations or missing integrations",
            GapType.PEOPLE: "Skill gaps or insufficient training",
            GapType.DATA: "Data quality issues or siloed data stores",
            GapType.GOVERNANCE: "Missing policies or unclear ownership",
        }
        return causes.get(gap_type, "Root cause analysis required")

    def _recommend_action(self, gap_type: GapType) -> str:
        actions = {
            GapType.PROCESS: "Document and optimize current-state process; implement BPMN models",
            GapType.TECHNOLOGY: "Evaluate technology upgrade or integration middleware",
            GapType.PEOPLE: "Develop training program and competency matrix",
            GapType.DATA: "Implement data governance framework and quality checks",
            GapType.GOVERNANCE: "Establish RACI ownership and policy documentation",
        }
        return actions.get(gap_type, "Conduct detailed analysis")

    # -----------------------------------------------------------------------
    # SWOT Analysis
    # -----------------------------------------------------------------------

    def perform_swot_analysis(
        self,
        entity: str,
        context: str = "",
    ) -> SWOTAnalysis:
        """
        Perform a weighted SWOT analysis with strategic implications.
        """
        logger.info("Performing SWOT analysis for '%s'", entity)
        analysis = SWOTAnalysis(entity=entity, context=context)

        analysis.strengths = [
            {"item": "Strong brand recognition", "weight": 0.9, "score": 8},
            {"item": "Skilled technical team", "weight": 0.8, "score": 7},
            {"item": "Established customer base", "weight": 0.85, "score": 8},
            {"item": "Proprietary technology", "weight": 0.7, "score": 6},
        ]
        analysis.weaknesses = [
            {"item": "Legacy system dependencies", "weight": 0.8, "score": -7},
            {"item": "Limited cloud expertise", "weight": 0.6, "score": -5},
            {"item": "High operational costs", "weight": 0.75, "score": -6},
        ]
        analysis.opportunities = [
            {"item": "Market expansion into APAC", "weight": 0.7, "score": 7},
            {"item": "AI/ML integration potential", "weight": 0.8, "score": 8},
            {"item": "Strategic partnership with cloud vendor", "weight": 0.65, "score": 6},
        ]
        analysis.threats = [
            {"item": "New competitor entrants", "weight": 0.85, "score": -8},
            {"item": "Regulatory changes", "weight": 0.7, "score": -6},
            {"item": "Economic downturn impact", "weight": 0.6, "score": -5},
        ]

        analysis.weighted_scores = self._calculate_swot_weights(analysis)
        analysis.strategic_implications = self._derive_strategic_implications(analysis)
        return analysis

    def _calculate_swot_weights(self, swot: SWOTAnalysis) -> Dict[str, float]:
        categories = {
            "strengths": swot.strengths,
            "weaknesses": swot.weaknesses,
            "opportunities": swot.opportunities,
            "threats": swot.threats,
        }
        scores = {}
        for cat_name, items in categories.items():
            total = sum(abs(item["weight"] * item["score"]) for item in items)
            scores[cat_name] = round(total, 2)
        total_all = sum(scores.values()) or 1
        for k in scores:
            scores[k] = round(scores[k] / total_all * 100, 1)
        return scores

    def _derive_strategic_implications(self, swot: SWOTAnalysis) -> List[str]:
        implications = []
        s_score = swot.weighted_scores.get("strengths", 0)
        o_score = swot.weighted_scores.get("opportunities", 0)
        if s_score > 25 and o_score > 25:
            implications.append("SO Strategy: Leverage strengths to capture opportunities")
        w_score = swot.weighted_scores.get("weaknesses", 0)
        t_score = swot.weighted_scores.get("threats", 0)
        if w_score > 20 and t_score > 20:
            implications.append("WT Strategy: Mitigate weaknesses to reduce threat exposure")
        if s_score > 25 and t_score > 20:
            implications.append("ST Strategy: Use strengths to counter threats")
        if w_score > 20 and o_score > 25:
            implications.append("WO Strategy: Address weaknesses to exploit opportunities")
        return implications

    # -----------------------------------------------------------------------
    # Business Case
    # -----------------------------------------------------------------------

    def write_business_case(
        self,
        problem: str,
        solution: str,
        costs: Optional[Dict[str, float]] = None,
        benefits: Optional[Dict[str, float]] = None,
    ) -> BusinessCase:
        """
        Write a business case with NPV, IRR, and ROI calculations.
        """
        logger.info("Writing business case: %s", problem[:50])
        costs = costs or {
            "development": 500000,
            "infrastructure": 100000,
            "training": 50000,
            "change_management": 30000,
        }
        benefits = benefits or {
            "revenue_increase": 800000,
            "cost_savings": 300000,
            "efficiency_gains": 200000,
        }

        total_cost = sum(costs.values())
        total_benefit = sum(benefits.values())
        annual_benefit = total_benefit
        annual_cost = total_cost * 0.2  # 20% maintenance

        cashflows = [-total_cost] + [annual_benefit - annual_cost] * 5
        npv = _calculate_npv(self._config.discount_rate, cashflows)
        irr = _calculate_irr(cashflows)
        roi = ((total_benefit - total_cost) / total_cost * 100) if total_cost else 0
        payback = total_cost / max(annual_benefit - annual_cost, 1)

        bc = BusinessCase(
            problem_statement=problem,
            proposed_solution=solution,
            costs=costs,
            benefits=benefits,
            npv=round(npv, 2),
            irr=round(irr, 4),
            roi=round(roi, 1),
            payback_period_months=round(payback * 12, 1),
            strategic_alignment=["Digital Transformation", "Cost Optimization"],
            assumptions=[
                "Benefits realized over 5-year horizon",
                f"Discount rate: {self._config.discount_rate * 100}%",
                "No major market disruptions",
            ],
            recommendation="Proceed — strong financial justification",
            confidence_level="high" if npv > 0 else "low",
        )
        return bc

    # -----------------------------------------------------------------------
    # User Stories
    # -----------------------------------------------------------------------

    def create_user_stories(
        self,
        feature: str,
        personas: Optional[List[str]] = None,
    ) -> List[UserStory]:
        """
        Create INVEST-compliant user stories for a feature.
        """
        logger.info("Creating user stories for feature '%s'", feature)
        personas = personas or ["end_user", "admin", "analyst"]
        actions_by_persona = {
            "end_user": [
                (f"access {feature} from any device", "I can work remotely"),
                (f"customize {feature} preferences", "the tool fits my workflow"),
            ],
            "admin": [
                (f"configure {feature} settings centrally", "I maintain governance"),
                (f"audit {feature} usage reports", "I ensure compliance"),
            ],
            "analyst": [
                (f"export {feature} data to CSV", "I can perform offline analysis"),
                (f"create custom {feature} dashboards", "I get actionable insights"),
            ],
        }
        stories = []
        for persona in personas:
            for action, benefit in actions_by_persona.get(persona, [
                (f"use {feature}", "I achieve my goal")
            ]):
                story = UserStory(
                    persona=persona,
                    action=action,
                    benefit=benefit,
                    story_text=f"As a {persona}, I want to {action}, so that {benefit}.",
                    priority=PriorityLevel.HIGH if persona == "end_user" else PriorityLevel.MEDIUM,
                    acceptance_criteria=[
                        f"When {persona} accesses {feature}, the system responds within 2s",
                        f"Feature {feature} is available to {persona} role",
                    ],
                )
                story.story_points = _estimate_story_points(story)
                story.invest_score = _validate_invest(story, self._config.invest_weights)
                stories.append(story)
                self._user_stories[story.id] = story
        return stories

    # -----------------------------------------------------------------------
    # Traceability Matrix
    # -----------------------------------------------------------------------

    def build_traceability_matrix(
        self,
        requirements: Optional[List[Requirement]] = None,
    ) -> TraceabilityMatrix:
        """
        Build a forward and backward traceability matrix.
        """
        logger.info("Building traceability matrix")
        reqs = requirements or list(self._requirements.values())
        if not reqs:
            return TraceabilityMatrix(business_need="No requirements provided")

        forward_trace: Dict[str, List[str]] = {}
        backward_trace: Dict[str, List[str]] = {}
        covered = 0

        for req in reqs:
            req_id = req.id
            linked_design = [f"DES-{req_id.split('-')[-1]}"]
            linked_test = [f"TC-{req_id.split('-')[-1]}"]
            forward_trace[req_id] = linked_design + linked_test
            for d in linked_design:
                backward_trace.setdefault(d, []).append(req_id)
            for t in linked_test:
                backward_trace.setdefault(t, []).append(req_id)
            covered += 1

        total = len(reqs)
        coverage = (covered / total * 100) if total else 0
        gaps = [
            f"Requirement {r.id} has no linked test case"
            for r in reqs if not r.acceptance_criteria
        ]

        matrix = TraceabilityMatrix(
            business_need="Traceability for " + (self._project_id or "unknown"),
            requirement_ids=[r.id for r in reqs],
            coverage_percentage=round(coverage, 1),
            gaps=gaps,
            forward_trace=forward_trace,
            backward_trace=backward_trace,
        )
        self._traceability[matrix.id] = matrix
        return matrix

    # -----------------------------------------------------------------------
    # Solution Design
    # -----------------------------------------------------------------------

    def design_solution(
        self,
        requirements: Optional[List[Requirement]] = None,
    ) -> SolutionDesign:
        """
        Create a solution design with alternatives analysis.
        """
        logger.info("Designing solution")
        reqs = requirements or list(self._requirements.values())
        func_reqs = [r for r in reqs if r.type == RequirementType.FUNCTIONAL]
        nfr_reqs = [r for r in reqs if r.type == RequirementType.NON_FUNCTIONAL]

        alternatives = [
            {
                "name": "Cloud-Native Microservices",
                "pros": ["Scalability", "Independent deployment", "Modern stack"],
                "cons": ["Complexity", "Higher initial cost", "Learning curve"],
                "cost_estimate": 800000,
                "timeline_weeks": 24,
            },
            {
                "name": "Monolithic Enhancement",
                "pros": ["Lower complexity", "Faster delivery", "Team familiarity"],
                "cons": ["Scaling limits", "Deployment coupling", "Tech debt"],
                "cost_estimate": 400000,
                "timeline_weeks": 16,
            },
            {
                "name": "Hybrid Approach",
                "pros": ["Balanced complexity", "Incremental migration", "Risk mitigation"],
                "cons": ["Integration overhead", "Dual maintenance"],
                "cost_estimate": 600000,
                "timeline_weeks": 20,
            },
        ]

        design = SolutionDesign(
            name="Solution Design — " + (self._project_id or "Project"),
            description=f"Design addressing {len(func_reqs)} functional and "
                        f"{len(nfr_reqs)} non-functional requirements",
            alternatives=alternatives,
            selected_alternative="Hybrid Approach",
            architecture_components=[
                "API Gateway", "Authentication Service", "Business Logic Layer",
                "Data Access Layer", "Message Queue", "Monitoring Dashboard",
            ],
            integration_points=[
                "External Identity Provider", "Legacy ERP System",
                "Third-party Analytics", "Email Notification Service",
            ],
            technology_stack=[
                "Python/FastAPI", "PostgreSQL", "Redis", "Kubernetes",
                "Terraform", "Grafana/Prometheus",
            ],
            estimated_timeline_weeks=20,
        )
        return design

    # -----------------------------------------------------------------------
    # Impact Assessment
    # -----------------------------------------------------------------------

    def assess_impact(
        self,
        change_request: Optional[ChangeRequest] = None,
    ) -> ImpactAssessment:
        """
        Assess the impact of a change request across all dimensions.
        """
        logger.info("Assessing change impact")
        cr = change_request or ChangeRequest(
            title="Example Change", description="Sample change request",
        )
        assessment = ImpactAssessment(
            change_request_id=cr.id,
            organizational_impact="Moderate — affects 3 teams, requires reallocation",
            technical_impact="High — new API contract, database migration required",
            process_impact="Medium — approval workflow modification needed",
            people_impact="Medium — training for 25 users on new process",
            data_impact="High — data schema changes, migration script needed",
            estimated_cost=75000,
            estimated_duration_weeks=6,
            risk_level=RiskLevel.MEDIUM,
            recommendation="Approve with phased rollout to mitigate risk",
            rollback_plan="Restore database backup and revert API version within 4 hours",
        )
        return assessment

    # -----------------------------------------------------------------------
    # Data Flow Modeling
    # -----------------------------------------------------------------------

    def model_data_flows(self, system_name: str) -> DataFlowModel:
        """
        Generate a data flow model for a named system.
        """
        logger.info("Modeling data flows for '%s'", system_name)
        dfm = DataFlowModel(
            system_name=system_name,
            entities=["Customer", "Administrator", "External API"],
            processes=[
                {"id": "P1", "name": "Process Registration"},
                {"id": "P2", "name": "Validate Input"},
                {"id": "P3", "name": "Store Record"},
                {"id": "P4", "name": "Generate Report"},
            ],
            data_stores=["Customer DB", "Audit Log", "Config Store"],
            flows=[
                {"from": "Customer", "to": "P1", "data": "Registration Form"},
                {"from": "P1", "to": "P2", "data": "Validated Data"},
                {"from": "P2", "to": "P3", "data": "Clean Record"},
                {"from": "P3", "to": "P4", "data": "Stored Data"},
                {"from": "P4", "to": "Administrator", "data": "Report"},
                {"from": "P4", "to": "External API", "data": "Analytics Payload"},
            ],
            trust_boundaries=["Internal Network", "DMZ"],
            external_interfaces=["Payment Gateway", "Email Service"],
        )
        return dfm

    # -----------------------------------------------------------------------
    # Risk Assessment
    # -----------------------------------------------------------------------

    def conduct_risk_assessment(
        self, project_id: str
    ) -> List[RiskAssessment]:
        """
        Identify and assess project risks with mitigation strategies.
        """
        logger.info("Conducting risk assessment for %s", project_id)
        risk_templates = [
            ("Scope Creep", "Uncontrolled expansion of requirements",
             0.7, 0.8, "Implement strict change control process"),
            ("Key Person Dependency", "Critical knowledge concentrated in few individuals",
             0.5, 0.9, "Cross-training and documentation program"),
            ("Technology Immaturity", "New technology may have undiscovered issues",
             0.4, 0.7, "Proof of concept phase with fallback plan"),
            ("Integration Failure", "Third-party system integration may fail",
             0.3, 0.8, "Contractual SLAs and early integration testing"),
            ("Budget Overrun", "Costs exceeding estimates",
             0.5, 0.6, "Monthly budget reviews and contingency reserve"),
            ("Timeline Slip", "Delivery delays",
             0.6, 0.5, "Agile sprints with buffer and milestone tracking"),
        ]
        risks = []
        for title, desc, prob, imp, strategy in risk_templates:
            risk = RiskAssessment(
                title=title, description=desc,
                probability=prob, impact=imp,
                mitigation_strategy=strategy,
                risk_level=_classify_risk(prob, imp),
            )
            risks.append(risk)
            self._risks[risk.id] = risk
        return risks

    # -----------------------------------------------------------------------
    # Requirement Validation
    # -----------------------------------------------------------------------

    def validate_requirements(
        self,
        requirements: Optional[List[Requirement]] = None,
    ) -> Dict[str, Any]:
        """
        Validate requirements for consistency, completeness, and quality.
        """
        logger.info("Validating requirements")
        reqs = requirements or list(self._requirements.values())
        issues: List[str] = []
        warnings: List[str] = []
        stats = {"total": len(reqs), "valid": 0, "issues": 0}

        for req in reqs:
            req_issues = []
            if not req.title or len(req.title) < 5:
                req_issues.append(f"{req.id}: Title too short")
            if not req.description or len(req.description) < 10:
                req_issues.append(f"{req.id}: Description too brief")
            if not req.acceptance_criteria:
                req_issues.append(f"{req.id}: Missing acceptance criteria")
            if not req.rationale:
                warnings.append(f"{req.id}: No business rationale provided")
            if req_issues:
                issues.extend(req_issues)
                stats["issues"] += 1
            else:
                stats["valid"] += 1

        duplicates = self._find_duplicates(reqs)
        if duplicates:
            issues.extend([f"Possible duplicate: {d}" for d in duplicates])

        return {
            "total": stats["total"],
            "valid": stats["valid"],
            "issues_count": stats["issues"],
            "issues": issues,
            "warnings": warnings,
            "completeness": round(stats["valid"] / max(stats["total"], 1) * 100, 1),
        }

    def _find_duplicates(self, reqs: List[Requirement]) -> List[str]:
        seen_hashes: Dict[str, List[str]] = {}
        for req in reqs:
            h = req.hash_content()
            seen_hashes.setdefault(h, []).append(req.id)
        return [
            f"IDs {ids} may be duplicates"
            for ids in seen_hashes.values() if len(ids) > 1
        ]

    # -----------------------------------------------------------------------
    # Acceptance Criteria
    # -----------------------------------------------------------------------

    def create_acceptance_criteria(
        self,
        user_story: UserStory,
    ) -> List[AcceptanceCriteria]:
        """
        Generate Given/When/Then acceptance criteria for a user story.
        """
        logger.info("Creating acceptance criteria for %s", user_story.id)
        criteria = [
            AcceptanceCriteria(
                requirement_id=user_story.id,
                given=f"The {user_story.persona} is authenticated",
                when=f"They attempt to {user_story.action}",
                then=f"The system completes the action and confirms {user_story.benefit}",
            ),
            AcceptanceCriteria(
                requirement_id=user_story.id,
                given=f"The {user_story.persona} is not authenticated",
                when=f"They attempt to {user_story.action}",
                then="The system redirects to the login page",
            ),
            AcceptanceCriteria(
                requirement_id=user_story.id,
                given=f"The system is under high load",
                when=f"The {user_story.persona} attempts to {user_story.action}",
                then="The system responds within 3 seconds",
            ),
        ]
        return criteria

    # -----------------------------------------------------------------------
    # Handoff Document
    # -----------------------------------------------------------------------

    def generate_handoff_document(
        self, project_id: str
    ) -> Dict[str, Any]:
        """
        Generate a BA-to-development handoff package.
        """
        logger.info("Generating handoff document for %s", project_id)
        reqs = list(self._requirements.values())
        stories = list(self._user_stories.values())
        risks = list(self._risks.values())

        handoff = {
            "project_id": project_id,
            "generated_at": datetime.utcnow().isoformat(),
            "phase": AnalysisPhase.HANDOFF.value,
            "executive_summary": (
                f"Handoff package for {project_id} containing "
                f"{len(reqs)} requirements, {len(stories)} user stories, "
                f"and {len(risks)} identified risks."
            ),
            "requirements_summary": {
                "total": len(reqs),
                "by_type": self._count_by_type(reqs),
                "by_priority": self._count_by_priority(reqs),
                "by_status": self._count_by_status(reqs),
            },
            "user_stories": [
                {"id": s.id, "text": s.to_invest_text(), "points": s.story_points}
                for s in stories
            ],
            "risk_register": [
                {"id": r.id, "title": r.title, "level": r.risk_level.name,
                 "mitigation": r.mitigation_strategy}
                for r in risks
            ],
            "traceability_summary": {
                "matrices": len(self._traceability),
                "total_gaps": sum(
                    len(m.gaps) for m in self._traceability.values()
                ),
            },
            "open_questions": [
                "Confirm integration SLA with third-party vendor",
                "Validate data migration scope with legacy system owner",
                "Finalize user acceptance testing timeline",
            ],
            "decision_log": [
                {"decision": "Selected hybrid architecture approach",
                 "rationale": "Balances cost and scalability"},
                {"decision": "MVP scope limited to 3 personas",
                 "rationale": "Reduces delivery risk"},
            ],
        }
        return handoff

    def _count_by_type(self, reqs: List[Requirement]) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for r in reqs:
            counts[r.type.value] = counts.get(r.type.value, 0) + 1
        return counts

    def _count_by_priority(self, reqs: List[Requirement]) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for r in reqs:
            counts[r.priority.name] = counts.get(r.priority.name, 0) + 1
        return counts

    def _count_by_status(self, reqs: List[Requirement]) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for r in reqs:
            counts[r.status.value] = counts.get(r.status.value, 0) + 1
        return counts

    # -----------------------------------------------------------------------
    # Utility / Status
    # -----------------------------------------------------------------------

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "BusinessAnalysisAgent",
            "version": "2.0.0",
            "phase": self._phase.value,
            "project_id": self._project_id,
            "requirements": len(self._requirements),
            "stakeholders": len(self._stakeholders),
            "processes": len(self._processes),
            "user_stories": len(self._user_stories),
            "risks": len(self._risks),
            "config": {
                "format": self._config.documentation_format.value,
                "notation": self._config.default_notation.value,
            },
        }

    def transition_phase(self, new_phase: AnalysisPhase) -> None:
        logger.info("Phase transition: %s -> %s", self._phase.value, new_phase.value)
        self._phase = new_phase

    def export_all(self) -> Dict[str, Any]:
        """Export all artifacts as a serializable dict."""
        return {
            "requirements": [asdict(r) for r in self._requirements.values()],
            "stakeholders": [asdict(s) for s in self._stakeholders.values()],
            "processes": [asdict(p) for p in self._processes.values()],
            "user_stories": [asdict(u) for u in self._user_stories.values()],
            "risks": [asdict(r) for r in self._risks.values()],
        }


# ══════════════════════════════════════════════════════════════════════════════
# DEMO / __main__
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    """Demonstrate the full Business Analysis Agent workflow."""
    print("=" * 70)
    print("  Business Analysis Agent — Full Workflow Demo")
    print("=" * 70)

    agent = BusinessAnalysisAgent(BAConfig(
        documentation_format=DocumentType.BRD,
        default_notation=ModelingNotation.BPMN,
    ))

    # 1. Requirements Gathering
    print("\n[1/12] Gathering requirements...")
    reqs = agent.gather_requirements("PROJ-2026-001", method="workshop")
    for r in reqs:
        print(f"  {r.id}: {r.title} [{r.priority.name}]")

    # 2. Stakeholder Map
    print("\n[2/12] Creating stakeholder map...")
    smap = agent.create_stakeholder_map("PROJ-2026-001")
    print(f"  Stakeholders: {smap['stakeholder_count']}")
    for quadrant, names in smap["power_interest_grid"].items():
        print(f"    {quadrant}: {', '.join(names) or '(none)'}")

    # 3. Process Mapping
    print("\n[3/12] Mapping process...")
    proc = agent.map_process("Order Processing", ModelingNotation.BPMN)
    print(f"  Process: {proc.name} | Complexity: {proc.complexity.value}")
    print(f"  Activities: {len(proc.activities)} | Inefficiencies: {len(proc.inefficiencies)}")

    # 4. Gap Analysis
    print("\n[4/12] Conducting gap analysis...")
    gaps = agent.conduct_gap_analysis(
        {"process": "manual", "technology": "legacy", "people": "untrained"},
        {"process": "automated", "technology": "cloud", "people": "certified"},
    )
    for g in gaps:
        print(f"  [{g.gap_type.value}] {g.description}")

    # 5. SWOT Analysis
    print("\n[5/12] Performing SWOT analysis...")
    swot = agent.perform_swot_analysis("Enterprise Platform", "Digital transformation")
    print(f"  Weighted scores: {swot.weighted_scores}")
    for imp in swot.strategic_implications:
        print(f"  → {imp}")

    # 6. Business Case
    print("\n[6/12] Writing business case...")
    bc = agent.write_business_case(
        "Manual processes cause 40% efficiency loss",
        "Automated workflow platform with AI analytics",
    )
    print(f"  NPV: ${bc.npv:,.2f} | IRR: {bc.irr*100:.1f}% | ROI: {bc.roi:.1f}%")
    print(f"  Payback: {bc.payback_period_months:.0f} months")

    # 7. User Stories
    print("\n[7/12] Creating user stories...")
    stories = agent.create_user_stories("dashboard", ["end_user", "admin"])
    for s in stories:
        print(f"  {s.id}: {s.to_invest_text()}")
        print(f"    Points: {s.story_points} | INVEST: {s.invest_score}")

    # 8. Traceability
    print("\n[8/12] Building traceability matrix...")
    matrix = agent.build_traceability_matrix()
    print(f"  Coverage: {matrix.coverage_percentage}% | Gaps: {len(matrix.gaps)}")

    # 9. Solution Design
    print("\n[9/12] Designing solution...")
    design = agent.design_solution()
    print(f"  Selected: {design.selected_alternative}")
    print(f"  Components: {len(design.architecture_components)}")
    print(f"  Timeline: {design.estimated_timeline_weeks} weeks")

    # 10. Impact Assessment
    print("\n[10/12] Assessing impact...")
    impact = agent.assess_impact()
    print(f"  Cost: ${impact.estimated_cost:,.0f} | Duration: {impact.estimated_duration_weeks}w")
    print(f"  Recommendation: {impact.recommendation}")

    # 11. Risk Assessment
    print("\n[11/12] Conducting risk assessment...")
    risks = agent.conduct_risk_assessment("PROJ-2026-001")
    for r in risks:
        print(f"  [{r.risk_level.name}] {r.title} — Score: {r.risk_score}")

    # 12. Handoff Document
    print("\n[12/12] Generating handoff document...")
    handoff = agent.generate_handoff_document("PROJ-2026-001")
    print(f"  Requirements: {handoff['requirements_summary']['total']}")
    print(f"  Risks: {len(handoff['risk_register'])}")

    print("\n" + "=" * 70)
    print("  Agent Status:", json.dumps(agent.get_status(), indent=2))
    print("=" * 70)


if __name__ == "__main__":
    main()
