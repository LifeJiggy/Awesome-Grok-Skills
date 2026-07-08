
"""
Agile Coach Agent - Team Guidance, Methodology Coaching & Maturity Assessment.

A comprehensive, production-ready agent for agile coaching, sprint facilitation,
team maturity assessment, and continuous improvement guidance.

Features:
- Multi-methodology support (Scrum, Kanban, XP, LeSS, SAFe, hybrid)
- Sprint planning assistance with capacity-based forecasting
- Retrospective facilitation (multiple formats)
- Team maturity assessment framework
- Velocity tracking and forecasting
- Technical debt management
- Definition of Done enforcement
- Continuous improvement recommendations
- Metrics dashboard (lead time, cycle time, throughput)
- Batch team assessments
- Multi-format reporting
- Integration with Jira, GitHub, Azure DevOps
"""

from __future__ import annotations

import abc
import asyncio
import csv
import enum
import hashlib
import json
import logging
import math
import random
import re
import statistics
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Union,
    Callable,
    Type,
)

logger = logging.getLogger(__name__)


# ============================================================================
# Enumerations
# ============================================================================


class CeremonyType(enum.Enum):
    """Agile ceremony types."""

    SPRINT_PLANNING = "sprint_planning"
    DAILY_STANDUP = "daily_standup"
    SPRINT_REVIEW = "sprint_review"
    RETROSPECTIVE = "retrospective"
    BACKLOG_REFINEMENT = "backlog_refinement"
    PI_PLANNING = "pi_planning"
    SCRUM_OF_SCRUMS = "scrum_of_scrums"


class Methodology(enum.Enum):
    """Agile methodologies."""

    SCRUM = "scrum"
    KANBAN = "kanban"
    XP = "xp"
    HYBRID = "hybrid"
    LESS = "less"
    SAFE = "safe"
    CRYSTAL = "crystal"
    FDD = "fdd"


class MaturityLevel(enum.Enum):
    """Agile maturity levels."""

    LEVEL_1_INITIAL = 1
    LEVEL_2_MANAGED = 2
    LEVEL_3_DEFINED = 3
    LEVEL_4_MEASURED = 4
    LEVEL_5_OPTIMIZING = 5


class RetrospectiveFormat(enum.Enum):
    """Retrospective formats."""

    START_STOP_CONTINUE = "start_stop_continue"
    MAD_SAD_GLAD = "mad_sad_glad"
    SAILBOAT = "sailboat"
        _4_LS  # Liked, Learned, Lacked, Longed For
    TIMELINE = "timeline"
    FISHBONE = "fishbone"
    SPEEDBOAT = "speedboat"
    KUDOS = "kudos"
    DAKI = "daki"  # Drop, Add, Keep, Improve
    WENT_WELL = "went_well"


class ImpedimentSeverity(enum.Enum):
    """Impediment severity levels."""

    BLOCKER = "blocker"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ArtifactType(enum.Enum):
    """Agile artifact types."""

    PRODUCT_BACKLOG = "product_backlog"
    SPRINT_BACKLOG = "sprint_backlog"
    INCREMENT = "increment"
    ROADMAP = "roadmap"
    VISION = "vision"
    BURNUP_CHART = "burnup_chart"
    BURNDOWN_CHART = "burndown_chart"
    CFD = "cumulative_flow_diagram"


class TeamRole(enum.Enum):
    """Team member roles."""

    PRODUCT_OWNER = "product_owner"
    SCRUM_MASTER = "scrum_master"
    DEVELOPER = "developer"
    DESIGNER = "designer"
    QA = "qa"
    DEVOPS = "devops"
    STAKEHOLDER = "stakeholder"


class MetricType(enum.Enum):
    """Agile metric types."""

    VELOCITY = "velocity"
    THROUGHPUT = "throughput"
    LEAD_TIME = "lead_time"
    CYCLE_TIME = "cycle_time"
    WIP = "wip"
    SPRINT_BURNUP = "sprint_burnup"
    SPRINT_BURNDOWN = "sprint_burndown"
    CUMULATIVE_FLOW = "cumulative_flow"
    ESCAPED_DEFECTS = "escaped_defects"
    TEAM_HAPPINESS = "team_happiness"


class ImprovementType(enum.Enum):
    """Types of improvements."""

    PROCESS = "process"
    TECHNICAL = "technical"
    COMMUNICATION = "communication"
    TOOLING = "tooling"
    CULTURE = "culture"
    SKILLS = "skills"
    ARCHITECTURE = "architecture"
    TESTING = "testing"


# ============================================================================
# Data Models
# ============================================================================


@dataclass
class VelocityRecord:
    """Single sprint velocity measurement."""

    sprint_id: str
    team_id: str
    committed_points: int
    completed_points: int
    planned_velocity: int
    actual_velocity: int
    start_date: datetime
    end_date: datetime
    capacity_hours: float
    available_hours: float
    interruptions_hours: float
    context_switches: int
    points_by_type: Dict[str, int] = field(default_factory=dict)
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["start_date"] = self.start_date.isoformat()
        data["end_date"] = self.end_date.isoformat()
        return data


@dataclass
class Retrospective:
    """Retrospective meeting record."""

    id: str
    team_id: str
    sprint_id: str
    format: RetrospectiveFormat
    feedback_items: List[Dict[str, Any]] = field(default_factory=list)
    action_items: List[Dict[str, Any]] = field(default_factory=list)
    votes: Dict[str, int] = field(default_factory=dict)
    sentiment_score: float = 0.0
    facilitator: str = ""
    duration_minutes: int = 60
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["format"] = self.format.value
        data["created_at"] = self.created_at.isoformat()
        return data


@dataclass
class Impediment:
    """Team impediment or blocker."""

    id: str
    team_id: str
    description: str
    severity: ImpedimentSeverity
    reported_by: str
    assigned_to: str = ""
    status: str = "open"
    resolution: str = ""
    dependencies: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["severity"] = self.severity.value
        data["created_at"] = self.created_at.isoformat()
        data["resolved_at"] = self.resolved_at.isoformat() if self.resolved_at else None
        return data


@dataclass
class TeamMember:
    """Team member profile."""

    id: str
    name: str
    email: str
    role: TeamRole
    team_id: str
    skills: List[str] = field(default_factory=list)
    capacity_points_per_sprint: int = 20
    available_hours_per_day: float = 6.0
    timezone: str = "UTC"
    joined_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["role"] = self.role.value
        data["joined_at"] = self.joined_at.isoformat()
        return data


@dataclass
class Team:
    """Agile team profile."""

    id: str
    name: str
    methodology: Methodology
    maturity_level: MaturityLevel
    members: List[TeamMember] = field(default_factory=list)
    sprint_duration_days: int = 14
    velocity_history: List[VelocityRecord] = field(default_factory=list)
    impediments: List[Impediment] = field(default_factory=list)
    retrospectives: List[Retrospective] = field(default_factory=list)
    wip_limit: int = 5
    definition_of_done: List[str] = field(default_factory=list)
    working_agreement: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    archived_at: Optional[datetime] = None

    def average_velocity(self, last_n: int = 3) -> float:
        if not self.velocity_history:
            return 0.0
        recent = self.velocity_history[-last_n:]
        return statistics.mean([r.actual_velocity for r in recent])

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["methodology"] = self.methodology.value
        data["maturity_level"] = self.maturity_level.value
        data["members"] = [m.to_dict() for m in self.members]
        data["velocity_history"] = [v.to_dict() for v in self.velocity_history]
        data["impediments"] = [i.to_dict() for i in self.impediments]
        data["retrospectives"] = [r.to_dict() for r in self.retrospectives]
        data["created_at"] = self.created_at.isoformat()
        data["archived_at"] = self.archived_at.isoformat() if self.archived_at else None
        return data


@dataclass
class Sprint:
    """Sprint definition and state."""

    id: str
    team_id: str
    name: str
    goal: str
    start_date: datetime
    end_date: datetime
    status: str  # planned, active, completed, cancelled
    committed_points: int = 0
    completed_points: int = 0
    carryover_points: int = 0
    scope_changes: int = 0
    impediments_count: int = 0
    retro_action_items: int = 0
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["start_date"] = self.start_date.isoformat()
        data["end_date"] = self.end_date.isoformat()
        data["created_at"] = self.created_at.isoformat()
        return data


@dataclass
class Improvement:
    """Tracked improvement initiative."""

    id: str
    team_id: str
    type: ImprovementType
    title: str
    description: str
    status: str  # proposed, in_progress, completed, abandoned
    priority: str  # high, medium, low
    effort_estimate: str = ""
    impact_estimate: str = ""
    assigned_to: str = ""
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    retro_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["type"] = self.type.value
        data["created_at"] = self.created_at.isoformat()
        data["due_date"] = self.due_date.isoformat() if self.due_date else None
        data["completed_at"] = self.completed_at.isoformat() if self.completed_at else None
        return data


@dataclass
class MetricSnapshot:
    """Point-in-time metric measurement."""

    id: str
    team_id: str
    metric_type: MetricType
    value: float
    unit: str
    recorded_at: datetime
    context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["metric_type"] = self.metric_type.value
        data["recorded_at"] = self.recorded_at.isoformat()
        return data


@dataclass
class MaturityAssessment:
    """Agile maturity assessment result."""

    id: str
    team_id: str
    assessor: str
    assessment_date: datetime
    overall_score: float
    level: MaturityLevel
    dimension_scores: Dict[str, float] = field(default_factory=dict)
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    raw_responses: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["level"] = self.level.value
        data["assessment_date"] = self.assessment_date.isoformat()
        return data


@dataclass
class Config:
    """Configuration for the Agile Coach Agent."""

    default_methodology: str = "scrum"
    default_sprint_duration_days: int = 14
    ceremonies_per_sprint: int = 5
    target_maturity_level: int = 4
    velocity_trend_window: int = 5
    min_velocity: int = 5
    max_velocity: int = 100
    wip_limit_default: int = 5
    enable_retrospectives: bool = True
    enable_velocity_tracking: bool = True
    enable_maturity_assessment: bool = True
    enable_impediment_tracking: bool = True
    enable_technical_debt_tracking: bool = False
    enable_cfd: bool = False
    report_formats: List[str] = field(default_factory=lambda: ["html", "json", "csv"])
    output_directory: str = "./agile_reports"
    history_enabled: bool = True
    history_file: str = "agile_coach_history.json"
    retention_days: int = 365
    cache_enabled: bool = True
    cache_ttl_hours: int = 24
    integrations: Dict[str, Dict[str, str]] = field(default_factory=dict)
    notification_channels: List[str] = field(default_factory=lambda: ["email"])
    concurrency: int = 4

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ============================================================================
# Exceptions
# ============================================================================


class AgileCoachError(Exception):
    """Base exception for agile coach errors."""
    pass


class TeamError(AgileCoachError):
    """Team management error."""
    pass


class SprintError(AgileCoachError):
    """Sprint management error."""
    pass


class AssessmentError(AgileCoachError):
    """Maturity assessment error."""
    pass


class CeremonyError(AgileCoachError):
    """Ceremony facilitation error."""
    pass


class ConfigurationError(AgileCoachError):
    """Configuration validation error."""
    pass


# ============================================================================
# Maturity Assessor
# ============================================================================


class MaturityAssessor:
    """Assesses agile maturity across multiple dimensions.

    Based on industry-standard agile maturity models (Scrum Alliance, Agile
    Practice Guide, etc.).

    Dimensions assessed:
    - Technical practices (CI/CD, TDD, refactoring)
    - Team collaboration (communication, decision-making)
    - Delivery (lead time, predictability, quality)
    - Continuous improvement (retrospectives, feedback loops)
    - Customer collaboration (backlog quality, stakeholder engagement)
    - Tooling and automation
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._dimension_questions: Dict[str, List[Dict[str, Any]]] = self._build_questionnaire()

    def _build_questionnaire(self) -> Dict[str, List[Dict[str, Any]]]:
        return {
            "technical_practices": [
                {"id": "tp1", "question": "Team practices continuous integration?", "weight": 1.0},
                {"id": "tp2", "question": "Automated test coverage > 70%?", "weight": 1.0},
                {"id": "tp3", "question": "Code reviews are mandatory?", "weight": 1.0},
                {"id": "tp4", "question": "Refactoring is part of the workflow?", "weight": 1.0},
                {"id": "tp5", "question": "Pair programming is practiced?", "weight": 0.8},
            ],
            "team_collaboration": [
                {"id": "tc1", "question": "Cross-functional team (all skills needed)?", "weight": 1.0},
                {"id": "tc2", "question": "Team self-organizes work?", "weight": 1.0},
                {"id": "tc3", "question": "Daily standup is effective and <= 15min?", "weight": 0.8},
                {"id": "tc4", "question": "Team has T-shaped skills?", "weight": 0.9},
                {"id": "tc5", "question": "Psychological safety is present?", "weight": 1.0},
            ],
            "delivery": [
                {"id": "d1", "question": "CI/CD pipeline deploys to production daily?", "weight": 1.0},
                {"id": "d2", "question": "Lead time < 1 week for features?", "weight": 0.9},
                {"id": "d3", "question": "Velocity is predictable (CV < 20%)?", "weight": 0.8},
                {"id": "d4", "question": "Production incidents are rare (< 1 per sprint)?", "weight": 0.9},
                {"id": "d5", "question": "Feature toggles used for safe releases?", "weight": 0.7},
            ],
            "continuous_improvement": [
                {"id": "ci1", "question": "Retrospectives held every sprint?", "weight": 1.0},
                {"id": "ci2", "question": "Retro action items are tracked and completed?", "weight": 0.9},
                {"id": "ci3", "question": "Team experiments with improvements?", "weight": 0.8},
                {"id": "ci4", "question": "Feedback loops from production are analyzed?", "weight": 0.9},
                {"id": "ci5", "question": "Blameless post-mortems for incidents?", "weight": 0.8},
            ],
            "customer_collaboration": [
                {"id": "cc1", "question": "Product owner is available to team?", "weight": 1.0},
                {"id": "cc2", "question": "Backlog is refined regularly (>= weekly)?", "weight": 0.9},
                {"id": "cc3", "question": "User stories have clear acceptance criteria?", "weight": 0.9},
                {"id": "cc4", "question": "Stakeholders attend reviews?", "weight": 0.8},
                {"id": "cc5", "question": "Real users give feedback regularly?", "weight": 0.8},
            ],
            "tooling_automation": [
                {"id": "ta1", "question": "Issue tracking integrated with code repo?", "weight": 0.8},
                {"id": "ta2", "question": "Automated deployment pipeline?", "weight": 1.0},
                {"id": "ta3", "question": "Monitoring and alerting in place?", "weight": 0.8},
                {"id": "ta4", "question": "Chatops used for routine tasks?", "weight": 0.6},
                {"id": "ta5", "question": "Documentation auto-generated from code?", "weight": 0.5},
            ],
        }

    def assess(
        self,
        team: Team,
        responses: Dict[str, int],
        assessor: str = "AgileCoachAgent",
    ) -> MaturityAssessment:
        dimension_scores = {}
        all_recommendations = []
        all_strengths = []
        all_weaknesses = []

        for dimension, questions in self._dimension_questions.items():
            dimension_score = 0.0
            total_weight = 0.0
            dimension_recommendations = []

            for q in questions:
                response = responses.get(q["id"], 0)
                weighted_score = response * q["weight"]
                dimension_score += weighted_score
                total_weight += q["weight"]

                if response <= 2:
                    dimension_recommendations.append(
                        f"Improve: {q['question']}"
                    )
                elif response >= 4:
                    all_strengths.append(f"{dimension}: {q['question']}")

            normalized_score = (
                (dimension_score / total_weight) * 5.0
                if total_weight > 0
                else 0.0
            )
            dimension_scores[dimension] = normalized_score
            all_recommendations.extend(dimension_recommendations[:2])

            if normalized_score < 2.5:
                all_weaknesses.append(f"{dimension}: score {normalized_score:.1f}/5.0")

        overall_score = (
            sum(dimension_scores.values()) / len(dimension_scores)
            if dimension_scores
            else 0.0
        )
        overall_level = self._score_to_level(overall_score)

        return MaturityAssessment(
            id=self._generate_assessment_id(),
            team_id=team.id,
            assessor=assessor,
            assessment_date=datetime.now(),
            overall_score=overall_score,
            level=overall_level,
            dimension_scores=dimension_scores,
            strengths=all_strengths[:5],
            weaknesses=all_weaknesses[:5],
            recommendations=all_recommendations[:5],
            raw_responses=responses,
        )

    def _score_to_level(self, score: float) -> MaturityLevel:
        if score >= 4.5:
            return MaturityLevel.LEVEL_5_OPTIMIZING
        elif score >= 3.5:
            return MaturityLevel.LEVEL_4_MEASURED
        elif score >= 2.5:
            return MaturityLevel.LEVEL_3_DEFINED
        elif score >= 1.5:
            return MaturityLevel.LEVEL_2_MANAGED
        else:
            return MaturityLevel.LEVEL_1_INITIAL

    def get_questionnaire(self) -> Dict[str, List[Dict[str, Any]]]:
        return self._dimension_questions

    def _generate_assessment_id(self) -> str:
        raw = f"assessment-{datetime.now().isoformat()}"
        return hashlib.md5(raw.encode()).hexdigest()[:12]


# ============================================================================
# Sprint Planner
# ============================================================================


class SprintPlanner:
    """Plans and forecasts sprints based on historical velocity and capacity.

    Features:
    - Capacity-based commitment planning
    - Buffer factor for interruptions
    - Story point vs hour estimation conversion
    - Dependency mapping
    - Risk assessment
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()

    def plan(
        self,
        team: Team,
        backlog: List[Dict[str, Any]],
        buffer_factor: float = 0.8,
    ) -> Dict[str, Any]:
        avg_velocity = team.average_velocity(self.config.velocity_trend_window)
        if avg_velocity < self.config.min_velocity:
            avg_velocity = self.config.min_velocity

        # Adjust for team capacity
        available_capacity = self._calculate_capacity(team)
        max_points = int(avg_velocity * buffer_factor * (available_capacity / 100))

        selected = []
        total_points = 0
        for item in sorted(backlog, key=lambda x: x.get("priority", 0), reverse=True):
            points = item.get("story_points", 0)
            if total_points + points <= max_points:
                selected.append(item)
                total_points += points

        return {
            "team_id": team.id,
            "recommended_commitment": max_points,
            "selected_items": selected,
            "selected_points": total_points,
            "available_capacity_hours": available_capacity,
            "avg_velocity": avg_velocity,
            "buffer_factor": buffer_factor,
            "backlog_items_available": len(backlog),
            "backlog_items_selected": len(selected),
            "risk_level": self._assess_risk(team, selected),
        }

    def _calculate_capacity(self, team: Team) -> float:
        sprint_days = team.sprint_duration_days
        total_hours = 0.0
        for member in team.members:
            if member.is_active:
                total_hours += member.available_hours_per_day * sprint_days
        return total_hours

    def _assess_risk(self, team: Team, selected: List[Dict[str, Any]]) -> str:
        if not team.velocity_history:
            return "high"
        velocities = [r.actual_velocity for r in team.velocity_history]
        cv = (statistics.stdev(velocities) / statistics.mean(velocities)) if velocities else 1.0
        if cv < 0.2:
            return "low"
        elif cv < 0.5:
            return "medium"
        return "high"


# ============================================================================
# Retrospective Facilitator
# ============================================================================


class RetrospectiveFacilitator:
    """Facilitates retrospective meetings with multiple formats.

    Supports:
    - Start/Stop/Continue
    - Mad/Sad/Glad
    - Sailboat (Wind/Anchor/Island/Rocks)
    - 4 Ls (Liked, Learned, Lacked, Longed For)
    - Timeline (project journey mapping)
    - Fishbone (root cause analysis)
    - DAKI (Drop, Add, Keep, Improve)
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()

    def create_template(self, fmt: RetrospectiveFormat) -> Dict[str, Any]:
        templates = {
            RetrospectiveFormat.START_STOP_CONTINUE: {
                "columns": ["Start", "Stop", "Continue"],
                "prompts": [
                    "What should we start doing?",
                    "What should we stop doing?",
                    "What should we continue doing?",
                ],
            },
            RetrospectiveFormat.MAD_SAD_GLAD: {
                "columns": ["Mad", "Sad", "Glad"],
                "prompts": [
                    "What made you mad?",
                    "What made you sad?",
                    "What made you glad?",
                ],
            },
            RetrospectiveFormat.SAILBOAT: {
                "columns": ["Wind", "Anchor", "Island", "Rocks"],
                "prompts": [
                    "What is pushing us forward? (Wind)",
                    "What is slowing us down? (Anchor)",
                    "What is our destination? (Island)",
                    "What are the risks? (Rocks)",
                ],
            },
            RetrospectiveFormat._4_LS: {
                "columns": ["Liked", "Learned", "Lacked", "Longed For"],
                "prompts": [
                    "What did you like?",
                    "What did you learn?",
                    "What was lacking?",
                    "What did you long for?",
                ],
            },
            RetrospectiveFormat.DAKI: {
                "columns": ["Drop", "Add", "Keep", "Improve"],
                "prompts": [
                    "What should we drop?",
                    "What should we add?",
                    "What should we keep?",
                    "What should we improve?",
                ],
            },
        }
        return templates.get(fmt, {})

    def analyze_feedback(
        self,
        feedback_items: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        themes: Dict[str, List[str]] = {}
        for item in feedback_items:
            category = item.get("category", "uncategorized")
            text = item.get("text", "")
            themes.setdefault(category, []).append(text)

        summary = {}
        for category, items in themes.items():
            summary[category] = {
                "count": len(items),
                "items": items,
                "voting_score": sum(item.get("votes", 0) for item in items),
            }

        return {
            "total_items": len(feedback_items),
            "categories": len(summary),
            "themes": summary,
            "top_voted": sorted(
                feedback_items,
                key=lambda x: x.get("votes", 0),
                reverse=True,
            )[:5],
        }

    def generate_action_items(
        self,
        feedback_items: List[Dict[str, Any]],
        max_items: int = 3,
    ) -> List[Dict[str, Any]]:
        prioritized = sorted(
            [i for i in feedback_items if i.get("votes", 0) > 0],
            key=lambda x: x.get("votes", 0),
            reverse=True,
        )[:max_items]

        action_items = []
        for idx, item in enumerate(prioritized, 1):
            action_items.append({
                "id": f"action-{idx}",
                "title": item.get("text", "")[:50],
                "description": item.get("text", ""),
                "votes": item.get("votes", 0),
                "category": item.get("category", ""),
                "status": "planned",
                "assigned_to": "",
            })

        return action_items

    def generate_retro_prompts(self, team: Team, past_retro: Optional[Retrospective] = None) -> List[str]:
        prompts = [
            "What went well this sprint?",
            "What could have gone better?",
            "What should we change next sprint?",
        ]

        if past_retro:
            prev_actions = [a["title"] for a in past_retro.action_items]
            if prev_actions:
                prompts.append(f"Follow-up: Did we complete '{prev_actions[0]}'?")
                prompts.append("What is still pending from last retrospective?")

        if team.maturity_level.value >= 3:
            prompts.append("How can we improve our Definition of Done?")
            prompts.append("What technical debt did we incur, and how do we address it?")

        return prompts


# ============================================================================
# Reporting Engine
# ============================================================================


class ReportingEngine:
    """Generates agile coaching reports."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()

    def generate(
        self,
        teams: List[Team],
        fmt: str = "html",
        output_path: Optional[str] = None,
    ) -> str:
        if fmt == "html":
            content = self._generate_html(teams)
        elif fmt == "json":
            content = self._generate_json(teams)
        elif fmt == "csv":
            content = self._generate_csv(teams)
        else:
            raise ReportingError(f"Unsupported format: {fmt}")

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)

        return content

    def _generate_html(self, teams: List[Team]) -> str:
        rows = ""
        for t in teams:
            avg_vel = t.average_velocity()
            rows += f"""
            <tr>
              <td>{t.id}</td>
              <td>{t.name}</td>
              <td>{t.methodology.value}</td>
              <td>{t.maturity_level.value}</td>
              <td>{len(t.members)}</td>
              <td>{avg_vel:.1f}</td>
              <td>{len(t.impediments)}</td>
              <td>{len(t.retrospectives)}</td>
            </tr>
            """

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Agile Team Report</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    th {{ background: #f5f5f5; }}
    .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin: 20px 0; }}
    .metric {{ padding: 15px; background: #f9f9f9; border-radius: 5px; }}
    .metric h3 {{ margin: 0; font-size: 1.5em; }}
  </style>
</head>
<body>
  <h1>Agile Team Report</h1>
  <div class="summary">
    <div class="metric"><h3>{len(teams)}</h3><p>Teams</p></div>
    <div class="metric"><h3>{sum(len(t.members) for t in teams)}</h3><p>Members</p></div>
    <div class="metric"><h3>{sum(len(t.impediments) for t in teams)}</h3><p>Open Impediments</p></div>
    <div class="metric"><h3>{sum(1 for t in teams if t.maturity_level.value >= 4)}</h3><p>High Maturity</p></div>
  </div>
  <h2>Team Details</h2>
  <table>
    <thead>
      <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Methodology</th>
        <th>Maturity</th>
        <th>Members</th>
        <th>Avg Velocity</th>
        <th>Open Impediments</th>
        <th>Retros</th>
      </tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
</body>
</html>"""

    def _generate_json(self, teams: List[Team]) -> str:
        data = {
            "generated_at": datetime.now().isoformat(),
            "teams": [t.to_dict() for t in teams],
            "summary": {
                "total_teams": len(teams),
                "total_members": sum(len(t.members) for t in teams),
                "avg_velocity": statistics.mean(
                    [t.average_velocity() for t in teams if t.velocity_history]
                ) or 0,
                "avg_maturity": statistics.mean([t.maturity_level.value for t in teams]),
            },
        }
        return json.dumps(data, indent=2, default=str)

    def _generate_csv(self, teams: List[Team]) -> str:
        output = []
        writer = csv.DictWriter(
            output,
            fieldnames=[
                "id", "name", "methodology", "maturity_level",
                "members", "avg_velocity", "impediments", "retros",
            ],
        )
        writer.writeheader()
        for t in teams:
            row = {
                "id": t.id,
                "name": t.name,
                "methodology": t.methodology.value,
                "maturity_level": t.maturity_level.value,
                "members": len(t.members),
                "avg_velocity": f"{t.average_velocity():.1f}",
                "impediments": len(t.impediments),
                "retros": len(t.retrospectives),
            }
            output.append(writer.writerow(row))
        return "\n".join(output)


# ============================================================================
# Main Agent
# ============================================================================


class AgileCoachAgent:
    """Agent for agile coaching and continuous improvement.

    Usage:
        agent = AgileCoachAgent()
        team = agent.create_team("Alpha", Methodology.SCRUM)
        agent.add_team_member(team.id, "Alice", TeamRole.DEVELOPER)
        retro = agent.facilitate_retrospective(team.id, RetrospectiveFormat.START_STOP_CONTINUE)
        assessment = agent.assess_maturity(team.id)
    """

    def __init__(self, config: Optional[Config] = None):
        self._config = config or Config()
        self._teams: List[Team] = []
        self._team_count = 0
        self._last_report: Optional[str] = None
        self._maturity_assessor = MaturityAssessor(self._config)
        self._sprint_planner = SprintPlanner(self._config)
        self._retro_facilitator = RetrospectiveFacilitator(self._config)
        self._reporting_engine = ReportingEngine(self._config)
        self._history: List[Dict[str, Any]] = []

    # -------------------------------------------------------------------------
    # Team Management
    # -------------------------------------------------------------------------

    def create_team(
        self,
        name: str,
        methodology: str = "scrum",
        sprint_duration_days: int = 14,
    ) -> Team:
        self._team_count += 1
        team = Team(
            id=f"team-{self._team_count:03d}-{int(time.time())}",
            name=name,
            methodology=Methodology(methodology),
            maturity_level=MaturityLevel.LEVEL_1_INITIAL,
            sprint_duration_days=sprint_duration_days,
        )
        self._teams.append(team)
        self._history.append({
            "action": "create_team",
            "team_id": team.id,
            "timestamp": datetime.now().isoformat(),
        })
        return team

    def add_team_member(
        self,
        team_id: str,
        name: str,
        role: str,
        email: str = "",
        skills: Optional[List[str]] = None,
    ) -> TeamMember:
        team = self._get_team(team_id)
        if not team:
            raise TeamError(f"Team {team_id} not found.")

        member = TeamMember(
            id=f"member-{len(team.members) + 1:03d}-{int(time.time())}",
            name=name,
            email=email,
            role=TeamRole(role),
            team_id=team_id,
            skills=skills or [],
        )
        team.members.append(member)
        return member

    def get_team(self, team_id: str) -> Optional[Team]:
        return self._get_team(team_id)

    def list_teams(
        self,
        methodology: Optional[str] = None,
        maturity_level: Optional[int] = None,
    ) -> List[Team]:
        result = self._teams
        if methodology:
            result = [t for t in result if t.methodology.value == methodology]
        if maturity_level:
            result = [t for t in result if t.maturity_level.value >= maturity_level]
        return result

    # -------------------------------------------------------------------------
    # Ceremonies
    # -------------------------------------------------------------------------

    def facilitate_retrospective(
        self,
        team_id: str,
        fmt: str = "start_stop_continue",
        feedback_items: Optional[List[Dict[str, Any]]] = None,
        facilitator: str = "AgileCoachAgent",
        duration_minutes: int = 60,
    ) -> Retrospective:
        team = self._get_team(team_id)
        if not team:
            raise TeamError(f"Team {team_id} not found.")

        fmt_enum = RetrospectiveFormat(fmt)
        past_retro = team.retrospectives[-1] if team.retrospectives else None

        retro = Retrospective(
            id=self._generate_retro_id(),
            team_id=team_id,
            sprint_id="",
            format=fmt_enum,
            feedback_items=feedback_items or [],
            facilitator=facilitator,
            duration_minutes=duration_minutes,
        )

        retro.action_items = self._retro_facilitator.generate_action_items(
            retro.feedback_items
        )

        team.retrospectives.append(retro)
        return retro

    def get_retro_template(self, fmt: str) -> Dict[str, Any]:
        return self._retro_facilitator.create_template(RetrospectiveFormat(fmt))

    def assist_sprint_planning(
        self,
        team_id: str,
        backlog: List[Dict[str, Any]],
        buffer_factor: float = 0.8,
    ) -> Dict[str, Any]:
        team = self._get_team(team_id)
        if not team:
            raise TeamError(f"Team {team_id} not found.")
        return self._sprint_planner.plan(team, backlog, buffer_factor)

    def estimate_effort(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        estimates = []
        for item in items:
            points = item.get("story_points", self._default_estimate(item))
            estimates.append({
                "id": item.get("id", ""),
                "title": item.get("title", ""),
                "estimated_points": points,
                "estimated_hours": points * 4,
            })

        return {
            "items": estimates,
            "total_points": sum(e["estimated_points"] for e in estimates),
            "total_hours": sum(e["estimated_hours"] for e in estimates),
        }

    def _default_estimate(self, item: Dict[str, Any]) -> int:
        complexity = item.get("complexity", 3)
        uncertainty = item.get("uncertainty", 0.5)
        team_size = item.get("team_size", 3)
        base = complexity * 3
        uncertainty_factor = 1 + uncertainty
        team_factor = 1 + (team_size - 3) * 0.1
        return max(1, int(base * uncertainty_factor / team_factor))

    # -------------------------------------------------------------------------
    # Maturity Assessment
    # -------------------------------------------------------------------------

    def assess_maturity(
        self,
        team_id: str,
        responses: Dict[str, int],
        assessor: str = "AgileCoachAgent",
    ) -> MaturityAssessment:
        team = self._get_team(team_id)
        if not team:
            raise TeamError(f"Team {team_id} not found.")
        assessment = self._maturity_assessor.assess(team, responses, assessor)
        team.maturity_level = assessment.level
        return assessment

    def get_assessment_questionnaire(self) -> Dict[str, List[Dict[str, Any]]]:
        return self._maturity_assessor.get_questionnaire()

    # -------------------------------------------------------------------------
    # Improvements
    # -------------------------------------------------------------------------

    def create_improvement(
        self,
        team_id: str,
        improvement_type: str,
        title: str,
        description: str,
        priority: str = "medium",
    ) -> Improvement:
        team = self._get_team(team_id)
        if not team:
            raise TeamError(f"Team {team_id} not found.")
        improvement = Improvement(
            id=self._generate_improvement_id(),
            team_id=team_id,
            type=ImprovementType(improvement_type),
            title=title,
            description=description,
            priority=priority,
        )
        return improvement

    def suggest_improvements(self, team_id: str) -> List[str]:
        team = self._get_team(team_id)
        if not team:
            raise TeamError(f"Team {team_id} not found.")
        improvements = []

        if not team.definition_of_done:
            improvements.append("Define a clear Definition of Done for the team.")

        if team.maturity_level.value < 3:
            improvements.append("Implement regular retrospectives and track action items.")

        avg_vel = team.average_velocity()
        if avg_vel < self.config.min_velocity:
            improvements.append(
                f"Increase velocity by reducing interruptions and focusing on committed work."
            )

        if not team.working_agreement:
            improvements.append("Create a team working agreement to set expectations.")

        if len([i for i in team.impediments if i.status == "open"]) > 3:
            improvements.append("Prioritize and resolve open impediments to improve flow.")

        return improvements

    # -------------------------------------------------------------------------
    # Status & Reporting
    # -------------------------------------------------------------------------

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "AgileCoachAgent",
            "teams": len(self._teams),
            "methodologies": list({t.methodology.value for t in self._teams}),
            "maturity_distribution": {
                lvl.name.replace("_", " ").title(): sum(
                    1 for t in self._teams if t.maturity_level == lvl
                )
                for lvl in MaturityLevel
            },
            "total_impediments": sum(len(t.impediments) for t in self._teams),
            "open_impediments": sum(
                sum(1 for i in t.impediments if i.status == "open")
                for t in self._teams
            ),
        }

    def generate_report(
        self,
        team_ids: Optional[List[str]] = None,
        fmt: str = "html",
        output_path: Optional[str] = None,
    ) -> str:
        teams = (
            [self._get_team(tid) for tid in team_ids]
            if team_ids
            else self._teams
        )
        teams = [t for t in teams if t is not None]
        self._last_report = self._reporting_engine.generate(
            teams, fmt=fmt, output_path=output_path
        )
        return self._last_report

    def get_history(self) -> List[Dict[str, Any]]:
        return self._history[-100:]

    def clear_history(self) -> None:
        self._history = []

    # -------------------------------------------------------------------------
    # Integration Hooks
    # -------------------------------------------------------------------------

    def to_jira_format(self, team_id: str) -> Dict[str, Any]:
        team = self._get_team(team_id)
        if not team:
            return {}
        return {
            "team": team.name,
            "methodology": team.methodology.value,
            "maturity": team.maturity_level.value,
            "velocity": team.average_velocity(),
            "wip_limit": team.wip_limit,
            "impediments": [i.to_dict() for i in team.impediments if i.status == "open"],
        }

    def to_github_format(self, team_id: str) -> Dict[str, Any]:
        team = self._get_team(team_id)
        if not team:
            return {}
        return {
            "team": team.name,
            "sprint_duration_days": team.sprint_duration_days,
            "average_velocity": team.average_velocity(),
            "members": len(team.members),
            "working_agreement": team.working_agreement,
            "definition_of_done": team.definition_of_done,
        }

    # -------------------------------------------------------------------------
    # Utility Methods
    # -------------------------------------------------------------------------

    def _get_team(self, team_id: str) -> Optional[Team]:
        for t in self._teams:
            if t.id == team_id:
                return t
        return None

    def _generate_retro_id(self) -> str:
        raw = f"retro-{datetime.now().isoformat()}"
        return hashlib.md5(raw.encode()).hexdigest()[:12]

    def _generate_improvement_id(self) -> str:
        raw = f"improvement-{datetime.now().isoformat()}"
        return hashlib.md5(raw.encode()).hexdigest()[:12]


# ============================================================================
# Public API
# ============================================================================

__all__ = [
    "AgileCoachAgent",
    "Team",
    "TeamMember",
    "Sprint",
    "VelocityRecord",
    "Retrospective",
    "RetrospectiveFormat",
    "Impediment",
    "Improvement",
    "MetricSnapshot",
    "MaturityAssessment",
    "Config",
    "Methodology",
    "MaturityLevel",
    "CeremonyType",
    "ImpedimentSeverity",
    "ArtifactType",
    "TeamRole",
    "MetricType",
    "ImprovementType",
    "MaturityAssessor",
    "SprintPlanner",
    "RetrospectiveFacilitator",
    "ReportingEngine",
    "AgileCoachError",
    "TeamError",
    "SprintError",
    "AssessmentError",
    "CeremonyError",
    "ConfigurationError",
]


def main():
    """Demo CLI for the Agile Coach Agent."""
    import argparse

    parser = argparse.ArgumentParser(description="Agile Coach Agent")
    parser.add_argument("--create-team", help="Create a new team with name")
    parser.add_argument("--add-member", nargs=2, metavar=("TEAM_ID", "NAME"), help="Add team member")
    parser.add_argument("--retro", help="Facilitate retrospective for team ID")
    parser.add_argument("--assess", help="Assess maturity for team ID")
    parser.add_argument("--improvements", help="Suggest improvements for team ID")
    parser.add_argument("--report", action="store_true", help="Generate team report")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    agent = AgileCoachAgent()

    if args.create_team:
        team = agent.create_team(args.create_team, methodology="scrum")
        print(f"Created team: {team.id} ({team.name})")
    elif args.add_member:
        member = agent.add_team_member(args.add_member[0], args.add_member[1], "developer")
        print(f"Added member: {member.id} ({member.name})")
    elif args.retro:
        retro = agent.facilitate_retrospective(args.retro, fmt="start_stop_continue")
        print(f"Retro ID: {retro.id}")
        print(f"Action items: {[a['title'] for a in retro.action_items]}")
    elif args.assess:
        responses = {f"q{i}": random.randint(1, 5) for i in range(1, 31)}
        assessment = agent.assess_maturity(args.assess, responses)
        print(f"Maturity Level: {assessment.level.name}")
        print(f"Overall Score: {assessment.overall_score:.1f}/5.0")
        print(f"Strengths: {assessment.strengths[:3]}")
        print(f"Recommendations: {assessment.recommendations[:3]}")
    elif args.improvements:
        suggestions = agent.suggest_improvements(args.improvements)
        print(f"Improvements for team {args.improvements}:")
        for s in suggestions:
            print(f"  - {s}")
    elif args.report:
        report = agent.generate_report(fmt="markdown")
        print(report)
    else:
        print("Agile Coach Agent Demo")
        print(agent.get_status())


if __name__ == "__main__":
    main()
