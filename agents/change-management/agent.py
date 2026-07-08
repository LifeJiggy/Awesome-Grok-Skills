"""
Change Management Agent - Organizational Change and Transformation.

Provides comprehensive change management capabilities including stakeholder analysis,
ADKAR modeling, transition planning, resistance management, communication strategy,
and organizational readiness assessment. Built for enterprise-scale transformations
with full lifecycle support from initiation through institutionalization.
"""

from __future__ import annotations

import logging
import uuid
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple, Set
from collections import defaultdict
import hashlib

logger = logging.getLogger(__name__)


# =============================================================================
# Enumerations
# =============================================================================

class ChangeType(Enum):
    """Types of organizational change."""
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"
    STRUCTURAL = "structural"
    CULTURAL = "cultural"
    TECHNOLOGICAL = "technological"
    PROCESS = "process"
    COMPLIANCE = "compliance"
    RESTRUCTURING = "restructuring"
    MERGER_ACQUISITION = "merger_acquisition"
    DIGITAL_TRANSFORMATION = "digital_transformation"


class ChangePhase(Enum):
    """Phases of the ADKAR change model."""
    AWARENESS = "awareness"
    DESIRE = "desire"
    KNOWLEDGE = "knowledge"
    ABILITY = "ability"
    REINFORCEMENT = "reinforcement"


class ChangeStatus(Enum):
    """Current status of a change initiative."""
    DRAFT = "draft"
    PLANNING = "planning"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class StakeholderImpact(Enum):
    """Level of impact a change has on a stakeholder."""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ResistanceLevel(Enum):
    """Levels of resistance to change."""
    CHAMPION = "champion"
    SUPPORTER = "supporter"
    NEUTRAL = "neutral"
    CRITIC = "critic"
    SABOTEUR = "saboteur"


class CommunicationChannel(Enum):
    """Available communication channels."""
    EMAIL = "email"
    TOWN_HALL = "town_hall"
    ONE_ON_ONE = "one_on_one"
    TEAM_MEETING = "team_meeting"
    INTRANET = "intranet"
    VIDEO = "video"
    WORKSHOP = "workshop"
    NEWSLETTER = "newsletter"
    SLACK = "slack"
    SURVEY = "survey"
    REPORT = "report"
    EXECUTIVE_BRIEF = "executive_brief"


class UrgencyLevel(Enum):
    """Urgency classification for change initiatives."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ReadinessLevel(Enum):
    """Organizational readiness assessment levels."""
    NOT_READY = "not_ready"
    PARTIALLY_READY = "partially_ready"
    READY = "ready"
    HIGHLY_READY = "highly_ready"


class TrainingFormat(Enum):
    """Training delivery formats."""
    IN_PERSON = "in_person"
    VIRTUAL_LIVE = "virtual_live"
    SELF_PACED = "self_paced"
    BLENDED = "blended"
    ON_THE_JOB = "on_the_job"
    MENTORING = "mentoring"
    SIMULATION = "simulation"
    WORKSHOP = "workshop"


class RiskSeverity(Enum):
    """Risk severity levels."""
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MilestoneStatus(Enum):
    """Status of a project milestone."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELAYED = "delayed"
    CANCELLED = "cancelled"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class Stakeholder:
    """Represents a stakeholder in a change initiative."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    role: str = ""
    department: str = ""
    title: str = ""
    impact_level: StakeholderImpact = StakeholderImpact.MEDIUM
    resistance_level: ResistanceLevel = ResistanceLevel.NEUTRAL
    influence_score: float = 0.5
    engagement_score: float = 0.5
    adkar_scores: Dict[str, float] = field(default_factory=dict)
    interests: List[str] = field(default_factory=list)
    concerns: List[str] = field(default_factory=list)
    communication_preferences: List[CommunicationChannel] = field(default_factory=list)
    notes: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "department": self.department,
            "title": self.title,
            "impact_level": self.impact_level.value,
            "resistance_level": self.resistance_level.value,
            "influence_score": self.influence_score,
            "engagement_score": self.engagement_score,
            "adkar_scores": self.adkar_scores,
            "interests": self.interests,
            "concerns": self.concerns,
            "communication_preferences": [c.value for c in self.communication_preferences],
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class CommunicationMessage:
    """A single communication item in a communication plan."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    message: str = ""
    channel: CommunicationChannel = CommunicationChannel.EMAIL
    target_audience: List[str] = field(default_factory=list)
    sender: str = ""
    scheduled_date: Optional[datetime] = None
    sent: bool = False
    feedback_expected: bool = False
    priority: int = 3
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "message": self.message,
            "channel": self.channel.value,
            "target_audience": self.target_audience,
            "sender": self.sender,
            "scheduled_date": self.scheduled_date.isoformat() if self.scheduled_date else None,
            "sent": self.sent,
            "feedback_expected": self.feedback_expected,
            "priority": self.priority,
            "tags": self.tags,
        }


@dataclass
class TrainingModule:
    """A training module for change readiness."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    description: str = ""
    training_format: TrainingFormat = TrainingFormat.BLENDED
    duration_hours: float = 1.0
    objectives: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    target_audience: List[str] = field(default_factory=list)
    adkar_phase: ChangePhase = ChangePhase.KNOWLEDGE
    max_participants: int = 30
    materials: List[str] = field(default_factory=list)
    assessment_criteria: List[str] = field(default_factory=list)
    trainer: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "training_format": self.training_format.value,
            "duration_hours": self.duration_hours,
            "objectives": self.objectives,
            "prerequisites": self.prerequisites,
            "target_audience": self.target_audience,
            "adkar_phase": self.adkar_phase.value,
            "max_participants": self.max_participants,
            "materials": self.materials,
            "assessment_criteria": self.assessment_criteria,
            "trainer": self.trainer,
        }


@dataclass
class RiskItem:
    """A risk identified during change planning."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    description: str = ""
    severity: RiskSeverity = RiskSeverity.MEDIUM
    probability: float = 0.5
    impact: float = 0.5
    risk_score: float = 0.25
    mitigation_strategy: str = ""
    contingency_plan: str = ""
    owner: str = ""
    status: str = "open"
    identified_date: datetime = field(default_factory=datetime.utcnow)
    target_resolution: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "severity": self.severity.value,
            "probability": self.probability,
            "impact": self.impact,
            "risk_score": self.risk_score,
            "mitigation_strategy": self.mitigation_strategy,
            "contingency_plan": self.contingency_plan,
            "owner": self.owner,
            "status": self.status,
            "identified_date": self.identified_date.isoformat(),
            "target_resolution": self.target_resolution.isoformat() if self.target_resolution else None,
            "tags": self.tags,
        }


@dataclass
class Milestone:
    """A milestone in the change timeline."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    description: str = ""
    target_date: datetime = field(default_factory=datetime.utcnow)
    actual_date: Optional[datetime] = None
    status: MilestoneStatus = MilestoneStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    deliverables: List[str] = field(default_factory=list)
    owner: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "target_date": self.target_date.isoformat(),
            "actual_date": self.actual_date.isoformat() if self.actual_date else None,
            "status": self.status.value,
            "dependencies": self.dependencies,
            "deliverables": self.deliverables,
            "owner": self.owner,
        }


@dataclass
class ChangePlan:
    """A complete change management plan."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    initiative_name: str = ""
    change_type: ChangeType = ChangeType.OPERATIONAL
    status: ChangeStatus = ChangeStatus.DRAFT
    urgency: UrgencyLevel = UrgencyLevel.MEDIUM
    description: str = ""
    business_case: str = ""
    objectives: List[str] = field(default_factory=list)
    scope: str = ""
    out_of_scope: List[str] = field(default_factory=list)
    stakeholders: List[Stakeholder] = field(default_factory=list)
    phases: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    adkar_readiness: Dict[str, float] = field(default_factory=dict)
    communication_plan: List[CommunicationMessage] = field(default_factory=list)
    training_modules: List[TrainingModule] = field(default_factory=list)
    risks: List[RiskItem] = field(default_factory=list)
    milestones: List[Milestone] = field(default_factory=list)
    budget: float = 0.0
    timeline_weeks: int = 26
    success_criteria: List[str] = field(default_factory=list)
    created_by: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    approved_by: str = ""
    approved_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "initiative_name": self.initiative_name,
            "change_type": self.change_type.value,
            "status": self.status.value,
            "urgency": self.urgency.value,
            "description": self.description,
            "business_case": self.business_case,
            "objectives": self.objectives,
            "scope": self.scope,
            "out_of_scope": self.out_of_scope,
            "stakeholders": [s.to_dict() for s in self.stakeholders],
            "phases": self.phases,
            "adkar_readiness": self.adkar_readiness,
            "communication_plan": [c.to_dict() for c in self.communication_plan],
            "training_modules": [t.to_dict() for t in self.training_modules],
            "risks": [r.to_dict() for r in self.risks],
            "milestones": [m.to_dict() for m in self.milestones],
            "budget": self.budget,
            "timeline_weeks": self.timeline_weeks,
            "success_criteria": self.success_criteria,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "approved_by": self.approved_by,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
        }


# =============================================================================
# ADKAR Model
# =============================================================================

class ADKARModel:
    """
    ADKAR individual change model evaluator.

    Measures and tracks individual readiness across five dimensions:
    Awareness, Desire, Knowledge, Ability, Reinforcement.
    """

    PHASE_DESCRIPTIONS = {
        ChangePhase.AWARENESS: "Understanding why the change is needed",
        ChangePhase.DESIRE: "Motivation and willingness to support the change",
        ChangePhase.KNOWLEDGE: "Information and training on how to change",
        ChangePhase.ABILITY: "Demonstrated capability to implement the change",
        ChangePhase.REINFORCEMENT: "Sustaining the change and preventing regression",
    }

    THRESHOLD_READY = 0.7
    THRESHOLD_PARTIAL = 0.4

    def __init__(self) -> None:
        self._evaluations: Dict[str, Dict[str, float]] = {}
        self._phase_history: Dict[str, List[Dict[str, Any]]] = {}

    def evaluate_stakeholder(
        self, stakeholder_id: str, scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Evaluate a stakeholder's ADKAR readiness.

        Args:
            stakeholder_id: Unique identifier for the stakeholder.
            scores: Dictionary mapping phase names to scores (0.0-1.0).

        Returns:
            Evaluation results with bottlenecks and recommendations.
        """
        validated_scores: Dict[str, float] = {}
        bottlenecks: List[str] = []
        recommendations: List[str] = []

        for phase in ChangePhase:
            phase_key = phase.value
            raw_score = scores.get(phase_key, 0.5)
            clamped = max(0.0, min(1.0, raw_score))
            validated_scores[phase_key] = clamped

            if clamped < self.THRESHOLD_READY:
                bottlenecks.append(phase_key)
                recommendations.append(
                    self._generate_recommendation(phase, clamped, stakeholder_id)
                )

        readiness_level = self._assess_readiness(validated_scores)
        overall_score = sum(validated_scores.values()) / len(validated_scores)

        self._evaluations[stakeholder_id] = validated_scores
        self._record_history(stakeholder_id, validated_scores, readiness_level)

        return {
            "stakeholder_id": stakeholder_id,
            "scores": validated_scores,
            "overall_score": round(overall_score, 3),
            "readiness_level": readiness_level,
            "bottlenecks": bottlenecks,
            "recommendations": recommendations,
            "phase_descriptions": {
                p.value: self.PHASE_DESCRIPTIONS[p] for p in ChangePhase
            },
            "evaluated_at": datetime.utcnow().isoformat(),
        }

    def get_bottleneck(self, stakeholder_id: str) -> Optional[Dict[str, Any]]:
        """
        Identify the primary ADKAR bottleneck for a stakeholder.

        The bottleneck is the earliest phase where the score falls below threshold,
        since later phases cannot succeed without earlier ones being satisfied.
        """
        scores = self._evaluations.get(stakeholder_id)
        if not scores:
            return None

        for phase in ChangePhase:
            score = scores.get(phase.value, 0.0)
            if score < self.THRESHOLD_READY:
                return {
                    "phase": phase.value,
                    "score": score,
                    "description": self.PHASE_DESCRIPTIONS[phase],
                    "recommendation": self._generate_recommendation(
                        phase, score, stakeholder_id
                    ),
                }
        return None

    def compare_readiness(
        self, stakeholder_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Compare ADKAR readiness across multiple stakeholders.

        Returns a matrix of scores plus identifies the most and least ready.
        """
        if not stakeholder_ids:
            return {"error": "No stakeholder IDs provided", "comparisons": []}

        comparisons: List[Dict[str, Any]] = []
        phase_averages: Dict[str, List[float]] = defaultdict(list)

        for sid in stakeholder_ids:
            scores = self._evaluations.get(sid, {})
            overall = (
                sum(scores.values()) / len(scores) if scores else 0.0
            )
            comparisons.append(
                {
                    "stakeholder_id": sid,
                    "scores": scores,
                    "overall_score": round(overall, 3),
                    "bottleneck": self.get_bottleneck(sid),
                }
            )
            for phase_key, val in scores.items():
                phase_averages[phase_key].append(val)

        comparisons.sort(key=lambda c: c["overall_score"], reverse=True)

        avg_by_phase = {
            k: round(sum(v) / len(v), 3) if v else 0.0
            for k, v in phase_averages.items()
        }

        return {
            "stakeholder_count": len(stakeholder_ids),
            "comparisons": comparisons,
            "phase_averages": avg_by_phase,
            "most_ready": comparisons[0] if comparisons else None,
            "least_ready": comparisons[-1] if comparisons else None,
        }

    def overall_organizational_readiness(
        self, stakeholder_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Compute aggregate organizational readiness.

        If no stakeholder IDs provided, uses all evaluated stakeholders.
        """
        target_ids = stakeholder_ids or list(self._evaluations.keys())
        if not target_ids:
            return {
                "level": ReadinessLevel.NOT_READY.value,
                "score": 0.0,
                "stakeholder_count": 0,
            }

        all_scores: List[float] = []
        for sid in target_ids:
            scores = self._evaluations.get(sid, {})
            if scores:
                all_scores.append(
                    sum(scores.values()) / len(scores)
                )

        if not all_scores:
            return {
                "level": ReadinessLevel.NOT_READY.value,
                "score": 0.0,
                "stakeholder_count": len(target_ids),
            }

        avg_score = sum(all_scores) / len(all_scores)
        level = (
            ReadinessLevel.HIGHLY_READY
            if avg_score >= 0.85
            else ReadinessLevel.READY
            if avg_score >= 0.65
            else ReadinessLevel.PARTIALLY_READY
            if avg_score >= 0.4
            else ReadinessLevel.NOT_READY
        )

        return {
            "level": level.value,
            "score": round(avg_score, 3),
            "stakeholder_count": len(target_ids),
            "evaluated_at": datetime.utcnow().isoformat(),
        }

    def _assess_readiness(self, scores: Dict[str, float]) -> str:
        overall = sum(scores.values()) / len(scores) if scores else 0.0
        if overall >= 0.85:
            return ReadinessLevel.HIGHLY_READY.value
        if overall >= 0.65:
            return ReadinessLevel.READY.value
        if overall >= 0.4:
            return ReadinessLevel.PARTIALLY_READY.value
        return ReadinessLevel.NOT_READY.value

    def _generate_recommendation(
        self, phase: ChangePhase, score: float, stakeholder_id: str
    ) -> str:
        recommendations = {
            ChangePhase.AWARENESS: (
                "Increase awareness through executive communication, town halls, "
                "and clear articulation of the 'why' behind the change."
            ),
            ChangePhase.DESIRE: (
                "Build motivation through WIIFM messaging, peer champions, "
                "and addressing individual concerns directly."
            ),
            ChangePhase.KNOWLEDGE: (
                "Provide structured training, documentation, and access to "
                "subject matter experts to build necessary knowledge."
            ),
            ChangePhase.ABILITY: (
                "Enable practice through simulations, hands-on workshops, "
                "and gradual exposure with coaching support."
            ),
            ChangePhase.REINFORCEMENT: (
                "Sustain through recognition programs, success metrics tracking, "
                "and regular check-ins to prevent regression."
            ),
        }
        base = recommendations.get(phase, "No specific recommendation available.")
        severity = "critically " if score < 0.3 else ""
        return f"{severity}{base}"

    def _record_history(
        self, stakeholder_id: str, scores: Dict[str, float], level: str
    ) -> None:
        if stakeholder_id not in self._phase_history:
            self._phase_history[stakeholder_id] = []
        self._phase_history[stakeholder_id].append(
            {
                "scores": dict(scores),
                "level": level,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )


# =============================================================================
# Stakeholder Analysis Engine
# =============================================================================

class StakeholderAnalyzer:
    """
    Comprehensive stakeholder analysis for change initiatives.

    Maps stakeholders by influence, interest, impact, and resistance
    to develop targeted engagement strategies.
    """

    def __init__(self) -> None:
        self._stakeholders: Dict[str, Stakeholder] = {}

    def register_stakeholder(self, stakeholder: Stakeholder) -> str:
        """Register a stakeholder and return their ID."""
        self._stakeholders[stakeholder.id] = stakeholder
        logger.info(
            "Stakeholder registered: %s (%s)", stakeholder.name, stakeholder.id
        )
        return stakeholder.id

    def get_stakeholder(self, stakeholder_id: str) -> Optional[Stakeholder]:
        return self._stakeholders.get(stakeholder_id)

    def list_stakeholders(
        self,
        impact_filter: Optional[StakeholderImpact] = None,
        resistance_filter: Optional[ResistanceLevel] = None,
        department_filter: Optional[str] = None,
    ) -> List[Stakeholder]:
        """List stakeholders with optional filters."""
        results = list(self._stakeholders.values())
        if impact_filter:
            results = [s for s in results if s.impact_level == impact_filter]
        if resistance_filter:
            results = [s for s in results if s.resistance_level == resistance_filter]
        if department_filter:
            results = [
                s for s in results if s.department.lower() == department_filter.lower()
            ]
        return results

    def classify_by_influence_interest(self) -> Dict[str, List[Stakeholder]]:
        """
        Classify stakeholders into a power/interest grid.

        Returns stakeholders categorized into four quadrants:
        - high_influence_high_interest: Manage closely
        - high_influence_low_interest: Keep satisfied
        - low_influence_high_interest: Keep informed
        - low_influence_low_interest: Monitor
        """
        grid: Dict[str, List[Stakeholder]] = {
            "high_influence_high_interest": [],
            "high_influence_low_interest": [],
            "low_influence_high_interest": [],
            "low_influence_low_interest": [],
        }

        for s in self._stakeholders.values():
            high_influence = s.influence_score >= 0.5
            high_interest = s.engagement_score >= 0.5

            if high_influence and high_interest:
                grid["high_influence_high_interest"].append(s)
            elif high_influence and not high_interest:
                grid["high_influence_low_interest"].append(s)
            elif not high_influence and high_interest:
                grid["low_influence_high_interest"].append(s)
            else:
                grid["low_influence_low_interest"].append(s)

        return grid

    def identify_champions(self) -> List[Stakeholder]:
        """Identify potential change champions."""
        return [
            s
            for s in self._stakeholders.values()
            if s.resistance_level == ResistanceLevel.CHAMPION
            or (
                s.influence_score >= 0.7
                and s.engagement_score >= 0.7
                and s.resistance_level
                in (ResistanceLevel.CHAMPION, ResistanceLevel.SUPPORTER)
            )
        ]

    def identify_risks(self) -> List[Dict[str, Any]]:
        """
        Identify stakeholder-related risks.

        High-influence critics and saboteurs pose the greatest risk.
        """
        risks: List[Dict[str, Any]] = []

        for s in self._stakeholders.values():
            risk_score = s.influence_score * self._resistance_weight(s.resistance_level)
            if risk_score >= 0.3:
                risks.append(
                    {
                        "stakeholder_id": s.id,
                        "name": s.name,
                        "role": s.role,
                        "resistance_level": s.resistance_level.value,
                        "influence_score": s.influence_score,
                        "risk_score": round(risk_score, 3),
                        "concerns": s.concerns,
                        "recommended_action": self._recommend_action(s),
                    }
                )

        risks.sort(key=lambda r: r["risk_score"], reverse=True)
        return risks

    def engagement_strategy(self, stakeholder_id: str) -> Dict[str, Any]:
        """
        Generate a tailored engagement strategy for a stakeholder.

        Based on their influence, interest, resistance level, and concerns.
        """
        s = self._stakeholders.get(stakeholder_id)
        if not s:
            return {"error": f"Stakeholder {stakeholder_id} not found"}

        quadrant = self._get_quadrant(s)
        strategy_map = {
            "high_influence_high_interest": {
                "approach": "Manage Closely",
                "frequency": "Weekly",
                "methods": [
                    "One-on-one meetings",
                    "Involvement in decision-making",
                    "Co-creation workshops",
                    "Direct executive access",
                ],
                "messaging_focus": "Strategic vision, personal impact, co-ownership",
            },
            "high_influence_low_interest": {
                "approach": "Keep Satisfied",
                "frequency": "Bi-weekly",
                "methods": [
                    "Executive summaries",
                    "High-level progress reports",
                    "Selective inclusion in key meetings",
                ],
                "messaging_focus": "Business outcomes, ROI, risk mitigation",
            },
            "low_influence_high_interest": {
                "approach": "Keep Informed",
                "frequency": "Weekly",
                "methods": [
                    "Team briefings",
                    "Intranet updates",
                    "Q&A sessions",
                    "Peer networks",
                ],
                "messaging_focus": "Practical details, personal benefits, support available",
            },
            "low_influence_low_interest": {
                "approach": "Monitor",
                "frequency": "Monthly",
                "methods": [
                    "Newsletter updates",
                    "Town hall attendance",
                    "Self-service resources",
                ],
                "messaging_focus": "High-level updates, availability of information",
            },
        }

        base = strategy_map.get(quadrant, strategy_map["low_influence_low_interest"])

        return {
            "stakeholder_id": s.id,
            "name": s.name,
            "quadrant": quadrant,
            "strategy": base,
            "personalized_messaging": self._personalize_messaging(s),
            "communication_channels": [c.value for c in s.communication_preferences]
            if s.communication_preferences
            else ["email", "team_meeting"],
            "concerns_to_address": s.concerns,
            "escalation_triggers": self._escalation_triggers(s),
        }

    def _resistance_weight(self, level: ResistanceLevel) -> float:
        weights = {
            ResistanceLevel.CHAMPION: 0.0,
            ResistanceLevel.SUPPORTER: 0.1,
            ResistanceLevel.NEUTRAL: 0.3,
            ResistanceLevel.CRITIC: 0.7,
            ResistanceLevel.SABOTEUR: 1.0,
        }
        return weights.get(level, 0.5)

    def _recommend_action(self, stakeholder: Stakeholder) -> str:
        if stakeholder.resistance_level == ResistanceLevel.SABOTEUR:
            return "Immediate executive intervention; consider isolation from critical path"
        if stakeholder.resistance_level == ResistanceLevel.CRITIC:
            return "Active listening sessions; address concerns directly; assign a champion mentor"
        if stakeholder.resistance_level == ResistanceLevel.NEUTRAL:
            return "Increase engagement through WIIFM messaging and peer influence"
        return "Maintain current engagement; leverage as change advocate"

    def _get_quadrant(self, s: Stakeholder) -> str:
        hi = s.influence_score >= 0.5
        he = s.engagement_score >= 0.5
        if hi and he:
            return "high_influence_high_interest"
        if hi:
            return "high_influence_low_interest"
        if he:
            return "low_influence_high_interest"
        return "low_influence_low_interest"

    def _personalize_messaging(self, s: Stakeholder) -> str:
        if s.concerns:
            return f"Address primary concern: {s.concerns[0]}"
        if s.interests:
            return f"Leverage interest in: {s.interests[0]}"
        return "Standard engagement messaging"

    def _escalation_triggers(self, s: Stakeholder) -> List[str]:
        triggers = []
        if s.resistance_level in (ResistanceLevel.CRITIC, ResistanceLevel.SABOTEUR):
            triggers.append("Public opposition in meetings")
            triggers.append("Influence on other stakeholders")
        if s.influence_score >= 0.8:
            triggers.append("Withdrawal of support")
            triggers.append("Escalation to board level")
        return triggers

    def get_all_stakeholders(self) -> List[Dict[str, Any]]:
        return [s.to_dict() for s in self._stakeholders.values()]


# =============================================================================
# Resistance Management
# =============================================================================

class ResistanceManager:
    """
    Manages and mitigates resistance to organizational change.

    Provides strategies for each resistance level, tracks resistance patterns,
    and recommends targeted interventions.
    """

    INTERVENTION_STRATEGIES = {
        ResistanceLevel.CHAMPION: {
            "actions": [
                "Formally recognize and publicize their support",
                "Involve in leadership communication",
                "Empower as peer mentors",
                "Provide exclusive briefings and early access",
            ],
            "risk": "Champion fatigue if over-burdened",
            "monitoring_frequency": "monthly",
        },
        ResistanceLevel.SUPPORTER: {
            "actions": [
                "Keep engaged through regular updates",
                "Solicit feedback to maintain ownership feeling",
                "Connect with champions for momentum",
            ],
            "risk": "May drift to neutral if not engaged",
            "monitoring_frequency": "bi-weekly",
        },
        ResistanceLevel.NEUTRAL: {
            "actions": [
                "Present clear WIIFM (What's In It For Me)",
                "Use peer pressure from supporters",
                "Provide low-risk opportunities to engage",
                "Address unspoken concerns proactively",
            ],
            "risk": "May align with critics if unaddressed",
            "monitoring_frequency": "weekly",
        },
        ResistanceLevel.CRITIC: {
            "actions": [
                "Schedule one-on-one listening sessions",
                "Acknowledge their concerns as valid",
                "Involve them in solution design where appropriate",
                "Provide evidence and data to counter misinformation",
                "Assign a respected champion as a liaison",
            ],
            "risk": "May sway neutral stakeholders",
            "monitoring_frequency": "twice weekly",
        },
        ResistanceLevel.SABOTEUR: {
            "actions": [
                "Escalate to executive sponsor immediately",
                "Document all opposition behaviors",
                "Consider removing from critical path",
                "Address underlying personal fears",
                "Establish clear consequences for active sabotage",
                "Explore if a different role would be better post-change",
            ],
            "risk": "Active undermining of change initiative",
            "monitoring_frequency": "daily",
        },
    }

    def __init__(self) -> None:
        self._resistance_log: List[Dict[str, Any]] = []
        self._interventions: List[Dict[str, Any]] = []

    def assess_resistance(
        self, stakeholder: Stakeholder
    ) -> Dict[str, Any]:
        """
        Assess the resistance profile of a stakeholder.

        Returns the resistance level, recommended interventions, and monitoring plan.
        """
        strategy = self.INTERVENTION_STRATEGIES.get(
            stakeholder.resistance_level,
            self.INTERVENTION_STRATEGIES[ResistanceLevel.NEUTRAL],
        )

        assessment = {
            "stakeholder_id": stakeholder.id,
            "name": stakeholder.name,
            "resistance_level": stakeholder.resistance_level.value,
            "influence_score": stakeholder.influence_score,
            "concerns": stakeholder.concerns,
            "recommended_actions": strategy["actions"],
            "risk": strategy["risk"],
            "monitoring_frequency": strategy["monitoring_frequency"],
            "priority": self._calculate_priority(stakeholder),
        }

        self._resistance_log.append(
            {
                "assessment": assessment,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

        return assessment

    def create_intervention_plan(
        self, stakeholder: Stakeholder, custom_actions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a detailed intervention plan for a resistant stakeholder.
        """
        strategy = self.INTERVENTION_STRATEGIES.get(
            stakeholder.resistance_level,
            self.INTERVENTION_STRATEGIES[ResistanceLevel.NEUTRAL],
        )

        actions = custom_actions or strategy["actions"]
        plan = {
            "id": str(uuid.uuid4())[:8],
            "stakeholder_id": stakeholder.id,
            "stakeholder_name": stakeholder.name,
            "resistance_level": stakeholder.resistance_level.value,
            "actions": [],
            "timeline_days": self._timeline_for_level(stakeholder.resistance_level),
            "escalation_path": self._escalation_path(stakeholder),
            "success_metrics": self._success_metrics(stakeholder),
            "created_at": datetime.utcnow().isoformat(),
        }

        for i, action in enumerate(actions):
            plan["actions"].append(
                {
                    "step": i + 1,
                    "action": action,
                    "status": "pending",
                    "target_date": (
                        datetime.utcnow() + timedelta(days=(i + 1) * 3)
                    ).isoformat(),
                    "notes": "",
                }
            )

        self._interventions.append(plan)
        return plan

    def track_resistance_trend(
        self, stakeholder_id: str
    ) -> Dict[str, Any]:
        """
        Track how a stakeholder's resistance level changes over time.
        """
        entries = [
            e
            for e in self._resistance_log
            if e["assessment"]["stakeholder_id"] == stakeholder_id
        ]

        if not entries:
            return {
                "stakeholder_id": stakeholder_id,
                "trend": "no_data",
                "entries": [],
            }

        levels = [e["assessment"]["resistance_level"] for e in entries]
        level_values = {
            "champion": 1, "supporter": 2, "neutral": 3, "critic": 4, "saboteur": 5
        }
        numeric = [level_values.get(l, 3) for l in levels]

        trend = "stable"
        if len(numeric) >= 2:
            diff = numeric[-1] - numeric[0]
            if diff < -1:
                trend = "improving"
            elif diff > 1:
                trend = "worsening"

        return {
            "stakeholder_id": stakeholder_id,
            "current_level": levels[-1] if levels else "unknown",
            "trend": trend,
            "assessment_count": len(entries),
            "first_assessed": entries[0]["timestamp"] if entries else None,
            "last_assessed": entries[-1]["timestamp"] if entries else None,
        }

    def resistance_summary(self) -> Dict[str, Any]:
        """Provide an overview of all resistance in the initiative."""
        if not self._resistance_log:
            return {"total_assessments": 0, "by_level": {}, "high_priority_count": 0}

        by_level: Dict[str, int] = defaultdict(int)
        high_priority = 0

        for entry in self._resistance_log:
            level = entry["assessment"]["resistance_level"]
            by_level[level] += 1
            if entry["assessment"]["priority"] == "high":
                high_priority += 1

        return {
            "total_assessments": len(self._resistance_log),
            "by_level": dict(by_level),
            "high_priority_count": high_priority,
            "active_interventions": len(self._interventions),
        }

    def _calculate_priority(self, stakeholder: Stakeholder) -> str:
        score = stakeholder.influence_score * self._resistance_weight_val(
            stakeholder.resistance_level
        )
        if score >= 0.6:
            return "high"
        if score >= 0.3:
            return "medium"
        return "low"

    def _resistance_weight_val(self, level: ResistanceLevel) -> float:
        return {
            ResistanceLevel.CHAMPION: 0.0,
            ResistanceLevel.SUPPORTER: 0.1,
            ResistanceLevel.NEUTRAL: 0.3,
            ResistanceLevel.CRITIC: 0.7,
            ResistanceLevel.SABOTEUR: 1.0,
        }.get(level, 0.5)

    def _timeline_for_level(self, level: ResistanceLevel) -> int:
        return {
            ResistanceLevel.CHAMPION: 90,
            ResistanceLevel.SUPPORTER: 60,
            ResistanceLevel.NEUTRAL: 30,
            ResistanceLevel.CRITIC: 21,
            ResistanceLevel.SABOTEUR: 14,
        }.get(level, 30)

    def _escalation_path(self, stakeholder: Stakeholder) -> List[str]:
        path = ["Direct manager", "Change sponsor"]
        if stakeholder.influence_score >= 0.8:
            path.append("Executive leadership")
        if stakeholder.resistance_level == ResistanceLevel.SABOTEUR:
            path.append("HR leadership")
        return path

    def _success_metrics(self, stakeholder: Stakeholder) -> List[str]:
        return [
            "Shift to lower resistance level within 30 days",
            "Active participation in at least one change activity",
            "Positive verbal acknowledgment of change benefits",
            "Reduction in negative influence on peers",
        ]


# =============================================================================
# Communication Planner
# =============================================================================

class CommunicationPlanner:
    """
    Develops and manages communication plans for change initiatives.

    Creates targeted messaging for different stakeholder groups,
    schedules communications, and tracks effectiveness.
    """

    def __init__(self) -> None:
        self._plans: Dict[str, List[CommunicationMessage]] = {}
        self._templates: Dict[str, str] = {
            "announcement": (
                "We are pleased to announce {initiative_name}. "
                "{description} This change will {impact_summary}. "
                "We are committed to supporting everyone through this transition."
            ),
            "progress_update": (
                "Update on {initiative_name}: We have {progress_summary}. "
                "Next steps include {next_steps}. "
                "If you have questions, please {contact_info}."
            ),
            "training_announcement": (
                "Training for {initiative_name} is now available. "
                "Format: {format}. Duration: {duration}. "
                "Please register by {deadline}."
            ),
            "feedback_request": (
                "We value your input on {initiative_name}. "
                "Please share your thoughts via {method}. "
                "Your feedback helps us improve the transition process."
            ),
            "milestone_celebration": (
                "We are excited to announce that {milestone_name} has been achieved! "
                "This marks {significance}. Thank you to everyone who contributed."
            ),
        }

    def create_communication_plan(
        self,
        plan_id: str,
        initiative_name: str,
        stakeholder_groups: List[str],
        timeline_weeks: int,
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive communication plan.

        Creates a structured schedule of communications across
        different channels and stakeholder groups.
        """
        communications: List[CommunicationMessage] = []
        week_num = 0

        # Pre-change communications
        for group in stakeholder_groups:
            communications.append(
                CommunicationMessage(
                    title=f"Initial Announcement - {group}",
                    message=self._templates["announcement"].format(
                        initiative_name=initiative_name,
                        description="This initiative aims to improve our operations.",
                        impact_summary="benefit your daily work and our organization",
                    ),
                    channel=CommunicationChannel.EMAIL,
                    target_audience=[group],
                    sender="Executive Sponsor",
                    scheduled_date=datetime.utcnow() + timedelta(weeks=week_num),
                    priority=1,
                    tags=["announcement", "pre-change"],
                )
            )

        week_num += 1

        # Regular updates
        update_frequency = max(1, timeline_weeks // 8)
        while week_num < timeline_weeks:
            for group in stakeholder_groups:
                communications.append(
                    CommunicationMessage(
                        title=f"Progress Update Week {week_num} - {group}",
                        message=self._templates["progress_update"].format(
                            initiative_name=initiative_name,
                            progress_summary="completed several key milestones",
                            next_steps="continue implementation and gather feedback",
                            contact_info="reach out to your team lead or the change team",
                        ),
                        channel=CommunicationChannel.EMAIL,
                        target_audience=[group],
                        sender="Change Manager",
                        scheduled_date=datetime.utcnow() + timedelta(weeks=week_num),
                        feedback_expected=True,
                        priority=3,
                        tags=["update", "progress"],
                    )
                )
            week_num += update_frequency

        # Post-change reinforcement
        communications.append(
            CommunicationMessage(
                title=f"Change Complete - {initiative_name}",
                message=f"The {initiative_name} transition is now complete.",
                channel=CommunicationChannel.TOWN_HALL,
                target_audience=stakeholder_groups,
                sender="Executive Sponsor",
                scheduled_date=datetime.utcnow() + timedelta(weeks=timeline_weeks),
                priority=1,
                tags=["completion", "celebration"],
            )
        )

        self._plans[plan_id] = communications

        return {
            "plan_id": plan_id,
            "initiative_name": initiative_name,
            "total_communications": len(communications),
            "by_channel": self._count_by_channel(communications),
            "by_audience": self._count_by_audience(communications),
            "communication_schedule": [c.to_dict() for c in communications],
        }

    def add_communication(
        self, plan_id: str, message: CommunicationMessage
    ) -> str:
        if plan_id not in self._plans:
            self._plans[plan_id] = []
        self._plans[plan_id].append(message)
        return message.id

    def get_plan(self, plan_id: str) -> List[Dict[str, Any]]:
        messages = self._plans.get(plan_id, [])
        return [m.to_dict() for m in messages]

    def generate_message(
        self, template_key: str, **kwargs: str
    ) -> str:
        """Generate a message from a template with variable substitution."""
        template = self._templates.get(template_key, "")
        try:
            return template.format(**kwargs)
        except KeyError as e:
            return f"Template error: missing variable {e}"

    def register_template(self, key: str, template: str) -> None:
        self._templates[key] = template

    def _count_by_channel(
        self, messages: List[CommunicationMessage]
    ) -> Dict[str, int]:
        counts: Dict[str, int] = defaultdict(int)
        for m in messages:
            counts[m.channel.value] += 1
        return dict(counts)

    def _count_by_audience(
        self, messages: List[CommunicationMessage]
    ) -> Dict[str, int]:
        counts: Dict[str, int] = defaultdict(int)
        for m in messages:
            for audience in m.target_audience:
                counts[audience] += 1
        return dict(counts)


# =============================================================================
# Training Developer
# =============================================================================

class TrainingDeveloper:
    """
    Develops and manages training programs for change readiness.

    Creates training modules aligned with ADKAR phases,
    tracks completion, and assesses effectiveness.
    """

    def __init__(self) -> None:
        self._modules: Dict[str, TrainingModule] = {}
        self._enrollments: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._completions: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    def create_training_program(
        self,
        initiative_id: str,
        initiative_name: str,
        target_groups: List[str],
    ) -> Dict[str, Any]:
        """
        Create a complete training program for a change initiative.

        Auto-generates modules for each ADKAR phase based on
        the target audience and change type.
        """
        modules: List[TrainingModule] = []

        # Phase 1: Awareness training
        awareness = TrainingModule(
            title=f"{initiative_name} - Why We're Changing",
            description="Understanding the business case and urgency for change",
            training_format=TrainingFormat.TOWN_HALL,
            duration_hours=1.0,
            objectives=[
                "Understand the business drivers behind the change",
                "Articulate the vision and expected outcomes",
                "Recognize the risks of not changing",
            ],
            target_audience=target_groups,
            adkar_phase=ChangePhase.AWARENESS,
            max_participants=100,
        )
        modules.append(awareness)

        # Phase 2: Desire building
        desire = TrainingModule(
            title=f"{initiative_name} - What's In It For You",
            description="Building motivation and personal connection to the change",
            training_format=TrainingFormat.WORKSHOP,
            duration_hours=2.0,
            objectives=[
                "Identify personal benefits of the change",
                "Address individual concerns and fears",
                "Build commitment to participate",
            ],
            target_audience=target_groups,
            adkar_phase=ChangePhase.DESIRE,
            max_participants=25,
        )
        modules.append(desire)

        # Phase 3: Knowledge transfer
        knowledge = TrainingModule(
            title=f"{initiative_name} - New Skills and Processes",
            description="Hands-on training on new tools, processes, and procedures",
            training_format=TrainingFormat.BLENDED,
            duration_hours=8.0,
            objectives=[
                "Master new tools and systems",
                "Understand revised processes and workflows",
                "Practice with realistic scenarios",
            ],
            target_audience=target_groups,
            adkar_phase=ChangePhase.KNOWLEDGE,
            max_participants=15,
            prerequisites=["Completion of Awareness and Desire modules"],
        )
        modules.append(knowledge)

        # Phase 4: Ability practice
        ability = TrainingModule(
            title=f"{initiative_name} - Practice and Application",
            description="Supervised practice in a safe environment",
            training_format=TrainingFormat.SIMULATION,
            duration_hours=4.0,
            objectives=[
                "Apply new skills in simulated scenarios",
                "Receive coaching feedback",
                "Build confidence for go-live",
            ],
            target_audience=target_groups,
            adkar_phase=ChangePhase.ABILITY,
            max_participants=10,
            prerequisites=["Completion of Knowledge module"],
        )
        modules.append(ability)

        # Phase 5: Reinforcement
        reinforcement = TrainingModule(
            title=f"{initiative_name} - Sustaining the Change",
            description="Ongoing support and refresher training",
            training_format=TrainingFormat.ON_THE_JOB,
            duration_hours=2.0,
            objectives=[
                "Reinforce correct behaviors",
                "Address regression quickly",
                "Share best practices and lessons learned",
            ],
            target_audience=target_groups,
            adkar_phase=ChangePhase.REINFORCEMENT,
            max_participants=20,
        )
        modules.append(reinforcement)

        for module in modules:
            self._modules[module.id] = module

        total_hours = sum(m.duration_hours for m in modules)
        return {
            "initiative_id": initiative_id,
            "program_name": f"{initiative_name} Training Program",
            "modules": [m.to_dict() for m in modules],
            "total_modules": len(modules),
            "total_hours": total_hours,
            "target_groups": target_groups,
            "created_at": datetime.utcnow().isoformat(),
        }

    def enroll_participant(
        self, module_id: str, participant_id: str, participant_name: str
    ) -> Dict[str, Any]:
        module = self._modules.get(module_id)
        if not module:
            return {"error": f"Module {module_id} not found"}

        enrolled = self._enrollments[module_id]
        if len(enrolled) >= module.max_participants:
            return {"error": "Module is at maximum capacity"}

        enrollment = {
            "participant_id": participant_id,
            "participant_name": participant_name,
            "enrolled_at": datetime.utcnow().isoformat(),
            "status": "enrolled",
        }
        enrolled.append(enrollment)

        return {
            "module_id": module_id,
            "module_title": module.title,
            "participant": participant_name,
            "enrolled_count": len(enrolled),
            "max_participants": module.max_participants,
        }

    def record_completion(
        self,
        module_id: str,
        participant_id: str,
        score: float,
        feedback: str = "",
    ) -> Dict[str, Any]:
        """Record that a participant completed a training module."""
        completion = {
            "module_id": module_id,
            "participant_id": participant_id,
            "score": max(0.0, min(1.0, score)),
            "feedback": feedback,
            "completed_at": datetime.utcnow().isoformat(),
        }
        self._completions[module_id].append(completion)

        return {
            "module_id": module_id,
            "participant_id": participant_id,
            "score": completion["score"],
            "passed": completion["score"] >= 0.7,
            "total_completions": len(self._completions[module_id]),
        }

    def get_program_stats(self) -> Dict[str, Any]:
        """Get overall training program statistics."""
        total_modules = len(self._modules)
        total_enrollments = sum(
            len(enrollments) for enrollments in self._enrollments.values()
        )
        total_completions = sum(
            len(completions) for completions in self._completions.values()
        )
        avg_score = 0.0
        all_scores = []
        for completions in self._completions.values():
            for c in completions:
                all_scores.append(c["score"])
        if all_scores:
            avg_score = sum(all_scores) / len(all_scores)

        return {
            "total_modules": total_modules,
            "total_enrollments": total_enrollments,
            "total_completions": total_completions,
            "completion_rate": (
                round(total_completions / total_enrollments, 3)
                if total_enrollments > 0
                else 0.0
            ),
            "average_score": round(avg_score, 3),
        }


# =============================================================================
# Readiness Assessor
# =============================================================================

class ReadinessAssessor:
    """
    Assesses organizational readiness for change across multiple dimensions.

    Evaluates culture, capability, capacity, and commitment to determine
    overall readiness and identify areas needing preparation.
    """

    DIMENSIONS = {
        "leadership_commitment": "Leaders actively champion and resource the change",
        "employee_engagement": "Staff are informed, consulted, and involved",
        "organizational_culture": "Culture supports innovation and adaptation",
        "technical_capability": "Systems and skills exist or can be built",
        "resource_availability": "Budget, people, and time are allocated",
        "change_history": "Organization has successful change track record",
        "communication_infrastructure": "Channels exist for two-way communication",
        "training_capacity": "Ability to develop and deliver training",
    }

    def __init__(self) -> None:
        self._assessments: Dict[str, Dict[str, float]] = {}
        self._history: List[Dict[str, Any]] = []

    def assess(
        self, organization_id: str, scores: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Assess organizational readiness for change.

        If scores are not provided, prompts for dimensional assessment.
        """
        if scores is None:
            scores = {dim: 0.5 for dim in self.DIMENSIONS}

        validated: Dict[str, float] = {}
        for dim in self.DIMENSIONS:
            raw = scores.get(dim, 0.5)
            validated[dim] = max(0.0, min(1.0, raw))

        overall = sum(validated.values()) / len(validated)
        level = self._readiness_level(overall)
        gaps = self._identify_gaps(validated)
        strengths = self._identify_strengths(validated)

        self._assessments[organization_id] = validated
        self._history.append(
            {
                "organization_id": organization_id,
                "scores": validated,
                "overall": overall,
                "level": level,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

        return {
            "organization_id": organization_id,
            "scores": validated,
            "overall_score": round(overall, 3),
            "readiness_level": level,
            "dimension_descriptions": self.DIMENSIONS,
            "strengths": strengths,
            "gaps": gaps,
            "recommendations": self._generate_recommendations(gaps),
        }

    def compare_assessments(self, organization_id: str) -> Dict[str, Any]:
        """Compare readiness assessments over time."""
        history = [
            h for h in self._history if h["organization_id"] == organization_id
        ]
        if len(history) < 2:
            return {"trend": "insufficient_data", "data_points": len(history)}

        first = history[0]["overall"]
        last = history[-1]["overall"]
        change = last - first

        return {
            "organization_id": organization_id,
            "data_points": len(history),
            "first_score": round(first, 3),
            "latest_score": round(last, 3),
            "change": round(change, 3),
            "trend": "improving" if change > 0.05 else "declining" if change < -0.05 else "stable",
        }

    def _readiness_level(self, score: float) -> str:
        if score >= 0.8:
            return ReadinessLevel.HIGHLY_READY.value
        if score >= 0.6:
            return ReadinessLevel.READY.value
        if score >= 0.4:
            return ReadinessLevel.PARTIALLY_READY.value
        return ReadinessLevel.NOT_READY.value

    def _identify_gaps(self, scores: Dict[str, float]) -> List[Dict[str, Any]]:
        gaps = []
        for dim, score in scores.items():
            if score < 0.5:
                gaps.append({
                    "dimension": dim,
                    "description": self.DIMENSIONS[dim],
                    "score": score,
                    "severity": "critical" if score < 0.3 else "significant",
                })
        gaps.sort(key=lambda g: g["score"])
        return gaps

    def _identify_strengths(self, scores: Dict[str, float]) -> List[Dict[str, Any]]:
        strengths = []
        for dim, score in scores.items():
            if score >= 0.7:
                strengths.append({
                    "dimension": dim,
                    "description": self.DIMENSIONS[dim],
                    "score": score,
                })
        strengths.sort(key=lambda s: s["score"], reverse=True)
        return strengths

    def _generate_recommendations(self, gaps: List[Dict[str, Any]]) -> List[str]:
        recs = []
        dim_recs = {
            "leadership_commitment": "Secure visible executive sponsorship with named champions",
            "employee_engagement": "Launch inclusive consultation process before implementation",
            "organizational_culture": "Consider a cultural assessment and pilot change first",
            "technical_capability": "Conduct a technical readiness audit and training needs analysis",
            "resource_availability": "Develop a detailed business case to secure budget and headcount",
            "change_history": "Share lessons learned from past changes; start with a small pilot",
            "communication_infrastructure": "Establish dedicated communication channels and cadence",
            "training_capacity": "Partner with L&D or external providers to build training capacity",
        }
        for gap in gaps:
            rec = dim_recs.get(gap["dimension"], "Address this gap before proceeding")
            recs.append(f"[{gap['dimension']}] {rec}")
        return recs


# =============================================================================
# Main Change Management Agent
# =============================================================================

class ChangeManagementAgent:
    """
    Primary orchestrator for organizational change management.

    Coordinates stakeholder analysis, ADKAR evaluation, communication planning,
    training development, resistance management, and readiness assessment
    into a unified change management workflow.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self._config = config or {}
        self._plans: Dict[str, ChangePlan] = {}
        self._adkar = ADKARModel()
        self._stakeholders = StakeholderAnalyzer()
        self._resistance = ResistanceManager()
        self._communication = CommunicationPlanner()
        self._training = TrainingDeveloper()
        self._readiness = ReadinessAssessor()
        self._created_at = datetime.utcnow()

        logger.info("ChangeManagementAgent initialized")

    def create_change_plan(
        self,
        initiative_name: str,
        change_type: str = "operational",
        description: str = "",
        objectives: Optional[List[str]] = None,
        timeline_weeks: int = 26,
        budget: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Create a comprehensive change management plan.

        Establishes the foundation for managing an organizational change
        initiative including scope, objectives, and initial structure.
        """
        ct = ChangeType(change_type) if change_type in [e.value for e in ChangeType] else ChangeType.OPERATIONAL

        plan = ChangePlan(
            initiative_name=initiative_name,
            change_type=ct,
            status=ChangeStatus.PLANNING,
            description=description,
            objectives=objectives or [],
            timeline_weeks=timeline_weeks,
            budget=budget,
            created_by=self._config.get("user", "system"),
        )

        plan.phases = self._create_phase_plan(plan)
        plan.milestones = self._create_initial_milestones(plan)

        self._plans[plan.id] = plan
        logger.info("Change plan created: %s (%s)", initiative_name, plan.id)

        return {
            "plan_id": plan.id,
            "initiative_name": initiative_name,
            "change_type": ct.value,
            "status": plan.status.value,
            "phases": plan.phases,
            "milestones": [m.to_dict() for m in plan.milestones],
            "timeline_weeks": timeline_weeks,
        }

    def add_stakeholder(
        self,
        plan_id: str,
        name: str,
        role: str,
        department: str = "",
        impact_level: str = "medium",
        resistance_level: str = "neutral",
        influence_score: float = 0.5,
        engagement_score: float = 0.5,
        concerns: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Add a stakeholder to a change plan."""
        plan = self._plans.get(plan_id)
        if not plan:
            return {"error": f"Plan {plan_id} not found"}

        il = StakeholderImpact(impact_level) if impact_level in [e.value for e in StakeholderImpact] else StakeholderImpact.MEDIUM
        rl = ResistanceLevel(resistance_level) if resistance_level in [e.value for e in ResistanceLevel] else ResistanceLevel.NEUTRAL

        stakeholder = Stakeholder(
            name=name,
            role=role,
            department=department,
            impact_level=il,
            resistance_level=rl,
            influence_score=max(0.0, min(1.0, influence_score)),
            engagement_score=max(0.0, min(1.0, engagement_score)),
            concerns=concerns or [],
        )

        plan.stakeholders.append(stakeholder)
        self._stakeholders.register_stakeholder(stakeholder)

        # Auto-assess resistance
        resistance_assessment = self._resistance.assess_resistance(stakeholder)

        return {
            "stakeholder_id": stakeholder.id,
            "name": name,
            "plan_id": plan_id,
            "resistance_assessment": resistance_assessment,
            "engagement_strategy": self._stakeholders.engagement_strategy(stakeholder.id),
        }

    def evaluate_adkar(
        self, plan_id: str, stakeholder_id: str, scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """Evaluate a stakeholder's ADKAR readiness."""
        return self._adkar.evaluate_stakeholder(stakeholder_id, scores)

    def develop_communication_plan(
        self, plan_id: str
    ) -> Dict[str, Any]:
        """Develop a communication plan for the change initiative."""
        plan = self._plans.get(plan_id)
        if not plan:
            return {"error": f"Plan {plan_id} not found"}

        groups = list(set(
            s.department or "all_employees" for s in plan.stakeholders
        ))
        if not groups:
            groups = ["all_employees"]

        return self._communication.create_communication_plan(
            plan_id=plan_id,
            initiative_name=plan.initiative_name,
            stakeholder_groups=groups,
            timeline_weeks=plan.timeline_weeks,
        )

    def develop_training_program(
        self, plan_id: str
    ) -> Dict[str, Any]:
        """Develop a training program for the change initiative."""
        plan = self._plans.get(plan_id)
        if not plan:
            return {"error": f"Plan {plan_id} not found"}

        groups = list(set(s.department or "all" for s in plan.stakeholders))
        if not groups:
            groups = ["all"]

        return self._training.create_training_program(
            initiative_id=plan_id,
            initiative_name=plan.initiative_name,
            target_groups=groups,
        )

    def assess_readiness(
        self, plan_id: str, scores: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """Assess organizational readiness for the change."""
        return self._readiness.assess(plan_id, scores)

    def get_resistance_summary(self) -> Dict[str, Any]:
        """Get an overview of resistance across all plans."""
        return self._resistance.resistance_summary()

    def get_plan_status(self, plan_id: str) -> Dict[str, Any]:
        """Get comprehensive status of a change plan."""
        plan = self._plans.get(plan_id)
        if not plan:
            return {"error": f"Plan {plan_id} not found"}

        return {
            "plan_id": plan.id,
            "initiative_name": plan.initiative_name,
            "status": plan.status.value,
            "change_type": plan.change_type.value,
            "stakeholder_count": len(plan.stakeholders),
            "milestone_count": len(plan.milestones),
            "risk_count": len(plan.risks),
            "timeline_weeks": plan.timeline_weeks,
            "created_at": plan.created_at.isoformat(),
        }

    def list_plans(self) -> List[Dict[str, Any]]:
        """List all change plans."""
        return [self.get_plan_status(pid) for pid in self._plans]

    def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            "agent": "ChangeManagementAgent",
            "version": "2.0.0",
            "active_plans": len(self._plans),
            "total_stakeholders": len(self._stakeholders._stakeholders),
            "total_communications": sum(
                len(msgs) for msgs in self._communication._plans.values()
            ),
            "uptime": str(datetime.utcnow() - self._created_at),
        }

    def _create_phase_plan(self, plan: ChangePlan) -> Dict[str, Dict[str, Any]]:
        weeks = plan.timeline_weeks
        return {
            "preparation": {
                "name": "Preparation & Planning",
                "start_week": 0,
                "end_week": max(1, weeks // 6),
                "activities": [
                    "Stakeholder identification and analysis",
                    "ADKAR readiness assessment",
                    "Communication plan development",
                    "Training program design",
                ],
            },
            "awareness": {
                "name": "Building Awareness",
                "start_week": max(1, weeks // 6),
                "end_week": max(2, weeks // 3),
                "activities": [
                    "Executive communication campaign",
                    "Town halls and team briefings",
                    "FAQ and resource development",
                ],
            },
            "design": {
                "name": "Solution Design & Training",
                "start_week": max(2, weeks // 3),
                "end_week": max(4, weeks * 2 // 3),
                "activities": [
                    "Detailed solution design",
                    "Training material development",
                    "Pilot program execution",
                ],
            },
            "implementation": {
                "name": "Implementation",
                "start_week": max(4, weeks * 2 // 3),
                "end_week": max(6, weeks - 2),
                "activities": [
                    "Phased rollout",
                    "Training delivery",
                    "Change adoption support",
                    "Issue resolution",
                ],
            },
            "reinforcement": {
                "name": "Reinforcement & Sustainment",
                "start_week": max(6, weeks - 2),
                "end_week": weeks,
                "activities": [
                    "Success metrics measurement",
                    "Reinforcement activities",
                    "Lessons learned documentation",
                    "Transition to BAU",
                ],
            },
        }

    def _create_initial_milestones(self, plan: ChangePlan) -> List[Milestone]:
        base = plan.created_at
        weeks = plan.timeline_weeks
        return [
            Milestone(
                title="Stakeholder Analysis Complete",
                description="All stakeholders identified and analyzed",
                target_date=base + timedelta(weeks=max(1, weeks // 6)),
                owner="Change Manager",
            ),
            Milestone(
                title="Communication Plan Approved",
                description="Communication strategy reviewed and approved by sponsor",
                target_date=base + timedelta(weeks=max(2, weeks // 4)),
                owner="Change Manager",
            ),
            Milestone(
                title="Training Program Ready",
                description="All training materials developed and reviewed",
                target_date=base + timedelta(weeks=max(4, weeks // 3)),
                owner="Training Lead",
            ),
            Milestone(
                title="Pilot Complete",
                description="Pilot group has completed the change and provided feedback",
                target_date=base + timedelta(weeks=max(6, weeks // 2)),
                owner="Pilot Lead",
            ),
            Milestone(
                title="Full Rollout Complete",
                description="Change implemented across all target groups",
                target_date=base + timedelta(weeks=max(8, weeks * 3 // 4)),
                owner="Change Manager",
            ),
            Milestone(
                title="Change Institutionalized",
                description="Change fully embedded in organizational processes",
                target_date=base + timedelta(weeks=weeks),
                owner="Executive Sponsor",
            ),
        ]


# =============================================================================
# Entry Point
# =============================================================================

def main() -> None:
    """Demonstrate the Change Management Agent capabilities."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    print("=" * 70)
    print("  Change Management Agent v2.0 - Demonstration")
    print("=" * 70)

    agent = ChangeManagementAgent({"user": "demo_user"})

    # Create a change plan
    print("\n--- Creating Change Plan ---")
    result = agent.create_change_plan(
        initiative_name="Cloud Migration Initiative",
        change_type="technological",
        description="Migrating on-premise infrastructure to AWS cloud",
        objectives=[
            "Reduce infrastructure costs by 30%",
            "Improve system reliability to 99.9% uptime",
            "Enable auto-scaling for peak demand",
        ],
        timeline_weeks=30,
        budget=500000.0,
    )
    plan_id = result["plan_id"]
    print(f"Plan created: {plan_id}")
    print(f"Status: {result['status']}")
    print(f"Milestones: {len(result['milestones'])}")

    # Add stakeholders
    print("\n--- Adding Stakeholders ---")
    stakeholders_data = [
        {"name": "Sarah Chen", "role": "CTO", "department": "Engineering",
         "impact_level": "critical", "resistance_level": "champion",
         "influence_score": 0.9, "engagement_score": 0.95},
        {"name": "Mike Johnson", "role": "VP Operations", "department": "Operations",
         "impact_level": "high", "resistance_level": "critic",
         "influence_score": 0.8, "engagement_score": 0.3,
         "concerns": ["downtime during migration", "staff retraining costs"]},
        {"name": "Lisa Park", "role": "Security Lead", "department": "Security",
         "impact_level": "high", "resistance_level": "neutral",
         "influence_score": 0.7, "engagement_score": 0.5,
         "concerns": ["data sovereignty", "compliance requirements"]},
        {"name": "Tom Wilson", "role": "Dev Team Lead", "department": "Engineering",
         "impact_level": "medium", "resistance_level": "supporter",
         "influence_score": 0.5, "engagement_score": 0.7},
        {"name": "Amy Davis", "role": "CFO", "department": "Finance",
         "impact_level": "high", "resistance_level": "neutral",
         "influence_score": 0.85, "engagement_score": 0.4,
         "concerns": ["budget overruns", "ROI timeline"]},
    ]

    for sd in stakeholders_data:
        res = agent.add_stakeholder(plan_id=plan_id, **sd)
        print(f"  Added: {sd['name']} ({sd['role']}) - Resistance: {sd['resistance_level']}")

    # ADKAR evaluation
    print("\n--- ADKAR Evaluation ---")
    adkar_result = agent.evaluate_adkar(
        plan_id, "stakeholder_id",
        {"awareness": 0.8, "desire": 0.6, "knowledge": 0.4, "ability": 0.3, "reinforcement": 0.5}
    )
    print(f"Overall readiness: {adkar_result['overall_score']}")
    print(f"Bottlenecks: {adkar_result['bottlenecks']}")

    # Communication plan
    print("\n--- Communication Plan ---")
    comm_result = agent.develop_communication_plan(plan_id)
    print(f"Total communications: {comm_result['total_communications']}")
    print(f"By channel: {comm_result['by_channel']}")

    # Training program
    print("\n--- Training Program ---")
    training_result = agent.develop_training_program(plan_id)
    print(f"Modules: {training_result['total_modules']}")
    print(f"Total hours: {training_result['total_hours']}")

    # Readiness assessment
    print("\n--- Readiness Assessment ---")
    readiness = agent.assess_readiness(plan_id, {
        "leadership_commitment": 0.8,
        "employee_engagement": 0.6,
        "organizational_culture": 0.5,
        "technical_capability": 0.7,
        "resource_availability": 0.6,
        "change_history": 0.4,
        "communication_infrastructure": 0.7,
        "training_capacity": 0.5,
    })
    print(f"Overall readiness: {readiness['overall_score']} ({readiness['readiness_level']})")
    print(f"Gaps: {len(readiness['gaps'])}")
    print(f"Strengths: {len(readiness['strengths'])}")

    # Resistance summary
    print("\n--- Resistance Summary ---")
    resistance = agent.get_resistance_summary()
    print(f"Total assessments: {resistance['total_assessments']}")
    print(f"By level: {resistance['by_level']}")
    print(f"High priority: {resistance['high_priority_count']}")

    # Agent status
    print("\n--- Agent Status ---")
    status = agent.get_status()
    for k, v in status.items():
        print(f"  {k}: {v}")

    print("\n" + "=" * 70)
    print("  Demonstration Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()
