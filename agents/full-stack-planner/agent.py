"""
Full-Stack Planner Agent — Project planning, tech stack selection,
architecture decisions, sprint planning, resource allocation, and
technical roadmap management for full-stack software projects.

This module provides comprehensive planning tools including:
- Tech stack evaluation and selection matrices
- System architecture design and documentation
- Sprint planning with velocity tracking and burndown analysis
- Resource allocation and capacity planning
- Risk assessment and dependency management
- Technical debt tracking and remediation planning
- Cost estimation and budget management
- Performance benchmarking and SLA definition
"""

from __future__ import annotations

import logging
import math
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, IntEnum
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    NamedTuple,
    Optional,
    Protocol,
    Sequence,
    Set,
    Tuple,
    Union,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ProjectPhase(Enum):
    DISCOVERY = "discovery"
    PLANNING = "planning"
    DESIGN = "design"
    DEVELOPMENT = "development"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"
    RETIREMENT = "retirement"


class Priority(IntEnum):
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3
    BACKLOG = 4


class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    BLOCKED = "blocked"
    DONE = "done"
    CANCELLED = "cancelled"


class RiskLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NEGLIGIBLE = "negligible"


class TechCategory(Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    DATABASE = "database"
    INFRASTRUCTURE = "infrastructure"
    DEVOPS = "devops"
    TESTING = "testing"
    MONITORING = "monitoring"
    SECURITY = "security"
    MOBILE = "mobile"
    AI_ML = "ai_ml"


class ArchitectureStyle(Enum):
    MONOLITH = "monolith"
    MICROSERVICES = "microservices"
    SERVERLESS = "serverless"
    EVENT_DRIVEN = "event_driven"
    MODULAR_MONOLITH = "modular_monolith"
    CQRS = "cqrs"
    LAYERED = "layered"
    HEXAGONAL = "hexagonal"
    PIPELINE = "pipeline"


class TeamRole(Enum):
    PROJECT_MANAGER = "project_manager"
    TECH_LEAD = "tech_lead"
    SENIOR_DEVELOPER = "senior_developer"
    DEVELOPER = "developer"
    JUNIOR_DEVELOPER = "junior_developer"
    DEVOPS_ENGINEER = "devops_engineer"
    QA_ENGINEER = "qa_engineer"
    UI_UX_DESIGNER = "ui_ux_designer"
    DATA_ENGINEER = "data_engineer"
    SECURITY_ENGINEER = "security_engineer"
    SCRUM_MASTER = "scrum_master"


class SprintEvent(Enum):
    PLANNING = "planning"
    DAILY_STANDUP = "daily_standup"
    REVIEW = "review"
    RETROSPECTIVE = "retrospective"
    DEMO = "demo"
    BACKLOG_REFINEMENT = "backlog_refinement"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class TechStack:
    """Technology stack entry with evaluation criteria."""
    name: str
    category: TechCategory
    version: str = ""
    maturity: str = "stable"
    community_score: float = 0.0     # 0-10
    performance_score: float = 0.0   # 0-10
    learning_curve: float = 0.0      # 0-10 (10 = easy)
    ecosystem_score: float = 0.0     # 0-10
    cost: float = 0.0               # monthly cost estimate
    license: str = "mit"
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    use_cases: List[str] = field(default_factory=list)
    alternatives: List[str] = field(default_factory=list)

    @property
    def composite_score(self) -> float:
        weights = {"community": 0.2, "performance": 0.25, "learning": 0.15, "ecosystem": 0.25, "cost_inv": 0.15}
        cost_inv = max(0, 10 - self.cost / 100)
        return (
            weights["community"] * self.community_score
            + weights["performance"] * self.performance_score
            + weights["learning"] * self.learning_curve
            + weights["ecosystem"] * self.ecosystem_score
            + weights["cost_inv"] * cost_inv
        )


@dataclass
class Task:
    """Work item for sprint or project tracking."""
    task_id: str
    title: str
    description: str
    priority: Priority
    status: TaskStatus = TaskStatus.TODO
    story_points: int = 0
    assignee: Optional[str] = None
    epic: Optional[str] = None
    sprint_id: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_hours: float = 0.0
    actual_hours: float = 0.0
    acceptance_criteria: List[str] = field(default_factory=list)
    notes: str = ""

    @property
    def is_blocked(self) -> bool:
        return self.status == TaskStatus.BLOCKED

    @property
    def cycle_time_days(self) -> Optional[float]:
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds() / 86400
        return None

    @property
    def efficiency(self) -> float:
        if self.estimated_hours > 0:
            return self.estimated_hours / self.actual_hours if self.actual_hours > 0 else 0
        return 0.0


@dataclass
class Epic:
    """Large feature grouping that spans multiple sprints."""
    epic_id: str
    name: str
    description: str
    priority: Priority
    tasks: List[str] = field(default_factory=list)  # task IDs
    target_date: Optional[datetime] = None
    business_value: float = 0.0     # 0-10
    completion_pct: float = 0.0

    @property
    def total_tasks(self) -> int:
        return len(self.tasks)


@dataclass
class Sprint:
    """Scrum sprint container."""
    sprint_id: str
    name: str
    start_date: datetime
    end_date: datetime
    goal: str = ""
    tasks: List[str] = field(default_factory=list)
    velocity: int = 0
    completed_points: int = 0
    committed_points: int = 0
    team_capacity_hours: float = 0.0
    events: Dict[str, datetime] = field(default_factory=dict)

    @property
    def duration_days(self) -> int:
        return (self.end_date - self.start_date).days

    @property
    def completion_rate(self) -> float:
        if self.committed_points == 0:
            return 0.0
        return self.completed_points / self.committed_points

    @property
    def is_active(self) -> bool:
        now = datetime.utcnow()
        return self.start_date <= now <= self.end_date


@dataclass
class TeamMember:
    """Team member with skills and capacity."""
    name: str
    role: TeamRole
    skills: List[str] = field(default_factory=list)
    hourly_rate: float = 0.0
    available_hours_per_week: float = 40.0
    current_load_pct: float = 0.0
    productivity_factor: float = 1.0   # 0-1.5
    experience_years: float = 0.0
    seniority: str = "mid"

    @property
    def effective_hours_per_week(self) -> float:
        return self.available_hours_per_week * self.productivity_factor

    @property
    def remaining_capacity_hours(self) -> float:
        return self.effective_hours_per_week * (1 - self.current_load_pct)

    @property
    def weekly_cost(self) -> float:
        return self.hourly_rate * self.available_hours_per_week


@dataclass
class Risk:
    """Project risk item."""
    risk_id: str
    description: str
    probability: float        # 0-1
    impact: float             # 0-10
    level: RiskLevel = RiskLevel.LOW
    mitigation: str = ""
    owner: str = ""
    status: str = "open"
    identified_date: datetime = field(default_factory=datetime.utcnow)

    @property
    def risk_score(self) -> float:
        return self.probability * self.impact

    @property
    def expected_loss(self) -> float:
        return self.risk_score * 1000  # monetary estimate


@dataclass
class ArchitectureDecision:
    """Architecture Decision Record (ADR)."""
    adr_id: str
    title: str
    status: str  # proposed, accepted, deprecated, superseded
    context: str
    decision: str
    consequences: List[str] = field(default_factory=list)
    alternatives: List[Dict[str, str]] = field(default_factory=list)
    date: datetime = field(default_factory=datetime.utcnow)
    decision_makers: List[str] = field(default_factory=list)
    superseded_by: Optional[str] = None


@dataclass
class CostEstimate:
    """Cost estimation for a project or feature."""
    category: str
    description: str
    hours_estimate: float
    hourly_rate: float = 100.0
    contingency_pct: float = 0.20
    infrastructure_monthly: float = 0.0
    third_party_monthly: float = 0.0

    @property
    def labor_cost(self) -> float:
        return self.hours_estimate * self.hourly_rate

    @property
    def total_labor_with_contingency(self) -> float:
        return self.labor_cost * (1 + self.contingency_pct)

    @property
    def first_year_total(self) -> float:
        return self.total_labor_with_contingency + (self.infrastructure_monthly + self.third_party_monthly) * 12


@dataclass
class TechnicalDebt:
    """Technical debt item tracking."""
    debt_id: str
    description: str
    severity: RiskLevel
    area: str
    estimated_fix_hours: float
    interest_per_sprint: float  # additional hours per sprint if unfixed
    introduced_date: datetime = field(default_factory=datetime.utcnow)
    status: str = "open"
    linked_task: Optional[str] = None

    @property
    def total_cost_if_unfixed(self, sprints: int = 10) -> float:
        return self.estimated_fix_hours + self.interest_per_sprint * sprints


@dataclass
class PerformanceBenchmark:
    """Performance target and measurement."""
    metric_name: str
    target_value: float
    actual_value: Optional[float] = None
    unit: str = ""
    threshold_warning: float = 0.0
    threshold_critical: float = 0.0

    @property
    def meets_target(self) -> bool:
        if self.actual_value is None:
            return False
        return self.actual_value <= self.target_value

    @property
    def deviation_pct(self) -> Optional[float]:
        if self.actual_value is None or self.target_value == 0:
            return None
        return (self.actual_value - self.target_value) / self.target_value * 100


@dataclass
class ProjectConfig:
    """Project-level configuration."""
    project_name: str
    team_name: str
    methodology: str = "scrum"
    sprint_duration_days: int = 14
    default_story_points: List[int] = field(default_factory=lambda: [1, 2, 3, 5, 8, 13])
    working_hours_per_day: float = 8.0
    working_days_per_week: int = 5
    risk_tolerance: str = "medium"
    budget: float = 0.0
    start_date: Optional[datetime] = None
    target_launch: Optional[datetime] = None
    architecture_style: ArchitectureStyle = ArchitectureStyle.MODULAR_MONOLITH

    @property
    def weekly_capacity_hours(self) -> float:
        return self.working_hours_per_day * self.working_days_per_week


# ---------------------------------------------------------------------------
# Protocols
# ---------------------------------------------------------------------------

class Estimator(Protocol):
    """Protocol for estimation strategies."""
    def estimate(self, tasks: List[Task]) -> float: ...


class NotificationHandler(Protocol):
    """Protocol for notifications."""
    def send(self, message: str, recipients: List[str]) -> bool: ...


# ---------------------------------------------------------------------------
# Tech Stack Evaluator
# ---------------------------------------------------------------------------

class TechStackEvaluator:
    """
    Evaluates and compares technology options across multiple criteria
    to support informed stack selection decisions.
    """

    def __init__(self) -> None:
        self.stacks: Dict[str, TechStack] = {}
        self.evaluation_history: List[Dict[str, Any]] = []
        logger.info("TechStackEvaluator initialized")

    def register_tech(self, stack: TechStack) -> None:
        self.stacks[stack.name] = stack
        logger.info("Registered tech: %s (%s)", stack.name, stack.category.value)

    def evaluate_category(
        self, category: TechCategory, weights: Optional[Dict[str, float]] = None
    ) -> List[Tuple[str, float]]:
        candidates = [
            (name, s) for name, s in self.stacks.items() if s.category == category
        ]
        if not candidates:
            return []

        results = []
        for name, stack in candidates:
            score = stack.composite_score
            results.append((name, score))

        results.sort(key=lambda x: x[1], reverse=True)
        self.evaluation_history.append({
            "category": category.value,
            "results": results,
            "timestamp": datetime.utcnow(),
        })
        return results

    def compare(self, tech_a: str, tech_b: str) -> Dict[str, Any]:
        if tech_a not in self.stacks or tech_b not in self.stacks:
            return {"error": "Tech not found"}
        a, b = self.stacks[tech_a], self.stacks[tech_b]
        return {
            "tech_a": tech_a,
            "tech_b": tech_b,
            "composite_a": a.composite_score,
            "composite_b": b.composite_score,
            "winner": tech_a if a.composite_score >= b.composite_score else tech_b,
            "criteria": {
                "community": {"a": a.community_score, "b": b.community_score},
                "performance": {"a": a.performance_score, "b": b.performance_score},
                "learning_curve": {"a": a.learning_curve, "b": b.learning_curve},
                "ecosystem": {"a": a.ecosystem_score, "b": b.ecosystem_score},
            },
        }

    def recommend_stack(
        self, requirements: Dict[str, Any]
    ) -> Dict[TechCategory, Optional[Tuple[str, float]]]:
        recommendations: Dict[TechCategory, Optional[Tuple[str, float]]] = {}
        required_categories = requirements.get("categories", list(TechCategory))
        for cat in required_categories:
            ranked = self.evaluate_category(cat)
            recommendations[cat] = ranked[0] if ranked else None
        return recommendations

    def generate_report(self) -> Dict[str, Any]:
        categories: Dict[str, List[Tuple[str, float]]] = defaultdict(list)
        for name, stack in self.stacks.items():
            categories[stack.category.value].append((name, stack.composite_score))
        for cat in categories:
            categories[cat].sort(key=lambda x: x[1], reverse=True)
        return {
            "total_techs": len(self.stacks),
            "categories": dict(categories),
            "evaluations_performed": len(self.evaluation_history),
        }


# ---------------------------------------------------------------------------
# Sprint Planner
# ---------------------------------------------------------------------------

class SprintPlanner:
    """
    Manages sprint lifecycle: planning, execution tracking,
    burndown analysis, and velocity computation.
    """

    def __init__(self, config: Optional[ProjectConfig] = None) -> None:
        self.config = config or ProjectConfig(project_name="Default", team_name="Default")
        self.sprints: Dict[str, Sprint] = {}
        self.tasks: Dict[str, Task] = {}
        self.velocity_history: List[int] = []
        logger.info("SprintPlanner initialized for project: %s", self.config.project_name)

    def create_sprint(
        self,
        sprint_id: str,
        name: str,
        start_date: datetime,
        end_date: datetime,
        goal: str = "",
    ) -> Sprint:
        sprint = Sprint(
            sprint_id=sprint_id, name=name,
            start_date=start_date, end_date=end_date, goal=goal,
        )
        sprint.events = {
            "planning": start_date,
            "review": end_date - timedelta(days=1),
            "retrospective": end_date,
        }
        self.sprints[sprint_id] = sprint
        logger.info("Sprint created: %s (%s to %s)", name, start_date.date(), end_date.date())
        return sprint

    def add_task(self, task: Task) -> None:
        self.tasks[task.task_id] = task

    def plan_sprint(
        self,
        sprint_id: str,
        task_ids: List[str],
        team_capacity_hours: Optional[float] = None,
    ) -> Dict[str, Any]:
        if sprint_id not in self.sprints:
            return {"error": f"Sprint {sprint_id} not found"}

        sprint = self.sprints[sprint_id]
        sprint.tasks = task_ids
        total_points = 0
        total_hours = 0.0
        task_details = []

        for tid in task_ids:
            if tid in self.tasks:
                task = self.tasks[tid]
                task.sprint_id = sprint_id
                total_points += task.story_points
                total_hours += task.estimated_hours
                task_details.append({
                    "task_id": tid,
                    "title": task.title,
                    "points": task.story_points,
                    "hours": task.estimated_hours,
                    "priority": task.priority.name,
                })

        sprint.committed_points = total_points
        sprint.team_capacity_hours = team_capacity_hours or 0

        return {
            "sprint_id": sprint_id,
            "tasks_planned": len(task_ids),
            "total_points": total_points,
            "total_hours": total_hours,
            "capacity_utilization": total_hours / sprint.team_capacity_hours if sprint.team_capacity_hours > 0 else 0,
            "task_details": task_details,
            "avg_velocity": self._average_velocity(),
        }

    def update_task_status(
        self, task_id: str, status: TaskStatus, actual_hours: float = 0
    ) -> None:
        if task_id not in self.tasks:
            return
        task = self.tasks[task_id]
        task.status = status
        if status == TaskStatus.IN_PROGRESS and not task.started_at:
            task.started_at = datetime.utcnow()
        elif status == TaskStatus.DONE:
            task.completed_at = datetime.utcnow()
            task.actual_hours = actual_hours

    def complete_sprint(self, sprint_id: str) -> Dict[str, Any]:
        if sprint_id not in self.sprints:
            return {"error": "Sprint not found"}

        sprint = self.sprints[sprint_id]
        completed = 0
        incomplete = 0
        completed_points = 0

        for tid in sprint.tasks:
            if tid in self.tasks:
                task = self.tasks[tid]
                if task.status == TaskStatus.DONE:
                    completed += 1
                    completed_points += task.story_points
                else:
                    incomplete += 1

        sprint.completed_points = completed_points
        sprint.velocity = completed_points
        self.velocity_history.append(completed_points)

        return {
            "sprint_id": sprint_id,
            "completed_tasks": completed,
            "incomplete_tasks": incomplete,
            "velocity": completed_points,
            "completion_rate": sprint.completion_rate,
            "avg_velocity": self._average_velocity(),
        }

    def generate_burndown(self, sprint_id: str) -> List[Dict[str, Any]]:
        if sprint_id not in self.sprints:
            return []
        sprint = self.sprints[sprint_id]
        total_points = sprint.committed_points
        duration = sprint.duration_days
        ideal_burn = [total_points - (total_points / max(duration - 1, 1)) * i for i in range(duration)]

        actual_burn = [total_points]
        remaining = total_points
        for tid in sprint.tasks:
            if tid in self.tasks and self.tasks[tid].status == TaskStatus.DONE:
                remaining -= self.tasks[tid].story_points
        actual_burn.append(remaining)

        return [
            {"day": i, "ideal": ideal_burn[i], "actual": actual_burn[min(i, len(actual_burn) - 1)]}
            for i in range(duration)
        ]

    def _average_velocity(self) -> float:
        if not self.velocity_history:
            return 0.0
        return sum(self.velocity_history) / len(self.velocity_history)

    def predict_completion(self, remaining_points: int) -> Dict[str, Any]:
        avg_vel = self._average_velocity()
        if avg_vel == 0:
            return {"sprints_needed": None, "message": "No velocity data available"}
        sprints = math.ceil(remaining_points / avg_vel)
        return {
            "remaining_points": remaining_points,
            "average_velocity": avg_vel,
            "sprints_needed": sprints,
            "estimated_weeks": sprints * (self.config.sprint_duration_days / 7),
        }


# ---------------------------------------------------------------------------
# Resource Allocator
# ---------------------------------------------------------------------------

class ResourceAllocator:
    """
    Manages team capacity, workload distribution, and resource optimization.
    """

    def __init__(self) -> None:
        self.team: Dict[str, TeamMember] = {}
        self.allocations: Dict[str, Dict[str, float]] = {}  # task_id -> {member_name: hours}
        logger.info("ResourceAllocator initialized")

    def add_member(self, member: TeamMember) -> None:
        self.team[member.name] = member
        self.allocations[member.name] = {}

    def allocate(self, task_id: str, member_name: str, hours: float) -> Dict[str, Any]:
        if member_name not in self.team:
            return {"error": f"Member {member_name} not found"}
        member = self.team[member_name]
        if hours > member.remaining_capacity_hours:
            return {"error": "Exceeds capacity", "remaining": member.remaining_capacity_hours}
        self.allocations.setdefault(task_id, {})
        self.allocations[task_id][member_name] = hours
        member.current_load_pct += hours / member.available_hours_per_week
        return {"allocated": True, "task_id": task_id, "member": member_name, "hours": hours}

    def get_team_capacity(self) -> Dict[str, Any]:
        total_available = sum(m.available_hours_per_week for m in self.team.values())
        total_effective = sum(m.effective_hours_per_week for m in self.team.values())
        total_remaining = sum(m.remaining_capacity_hours for m in self.team.values())
        total_cost = sum(m.weekly_cost for m in self.team.values())
        return {
            "team_size": len(self.team),
            "total_available_hours": total_available,
            "total_effective_hours": total_effective,
            "total_remaining_hours": total_remaining,
            "utilization_pct": (total_available - total_remaining) / total_available * 100 if total_available > 0 else 0,
            "weekly_cost": total_cost,
            "members": {
                name: {
                    "role": m.role.value,
                    "load_pct": m.current_load_pct * 100,
                    "remaining_hrs": m.remaining_capacity_hours,
                }
                for name, m in self.team.items()
            },
        }

    def find_best_fit(self, required_skills: List[str], hours_needed: float) -> Optional[str]:
        candidates = []
        for name, member in self.team.items():
            if member.remaining_capacity_hours < hours_needed:
                continue
            skill_match = len(set(required_skills) & set(member.skills))
            candidates.append((name, skill_match, member.remaining_capacity_hours))
        if not candidates:
            return None
        candidates.sort(key=lambda x: (x[1], x[2]), reverse=True)
        return candidates[0][0]

    def rebalance_workload(self) -> List[Dict[str, Any]]:
        overloaded = [(n, m) for n, m in self.team.items() if m.current_load_pct > 0.9]
        underloaded = [(n, m) for n, m in self.team.items() if m.current_load_pct < 0.5]
        suggestions = []
        for o_name, o_member in overloaded:
            for u_name, u_member in underloaded:
                transferable = min(
                    o_member.current_load_pct * o_member.available_hours_per_week * 0.2,
                    u_member.remaining_capacity_hours,
                )
                if transferable > 1:
                    suggestions.append({
                        "from": o_name,
                        "to": u_name,
                        "transfer_hours": round(transferable, 1),
                    })
        return suggestions


# ---------------------------------------------------------------------------
# Risk Manager
# ---------------------------------------------------------------------------

class RiskManager:
    """
    Tracks, evaluates, and mitigates project risks.
    """

    def __init__(self, risk_tolerance: str = "medium") -> None:
        self.risks: Dict[str, Risk] = {}
        self.tolerance = risk_tolerance
        self.threshold = {"low": 3, "medium": 5, "high": 7}.get(risk_tolerance, 5)
        logger.info("RiskManager initialized (tolerance=%s)", risk_tolerance)

    def add_risk(self, risk: Risk) -> None:
        risk.level = self._classify_risk(risk.risk_score)
        self.risks[risk.risk_id] = risk
        logger.info("Risk added: %s (score=%.2f, level=%s)", risk.risk_id, risk.risk_score, risk.level.value)

    def _classify_risk(self, score: float) -> RiskLevel:
        if score >= 7:
            return RiskLevel.CRITICAL
        elif score >= 5:
            return RiskLevel.HIGH
        elif score >= 3:
            return RiskLevel.MEDIUM
        elif score >= 1:
            return RiskLevel.LOW
        return RiskLevel.NEGLIGIBLE

    def get_risk_register(self) -> List[Dict[str, Any]]:
        register = []
        for risk in sorted(self.risks.values(), key=lambda r: r.risk_score, reverse=True):
            register.append({
                "risk_id": risk.risk_id,
                "description": risk.description,
                "probability": risk.probability,
                "impact": risk.impact,
                "score": risk.risk_score,
                "level": risk.level.value,
                "mitigation": risk.mitigation,
                "status": risk.status,
            })
        return register

    def get_risk_summary(self) -> Dict[str, Any]:
        levels = defaultdict(int)
        for risk in self.risks.values():
            levels[risk.level.value] += 1
        total_expected_loss = sum(r.expected_loss for r in self.risks.values() if r.status == "open")
        critical_risks = [r for r in self.risks.values() if r.level == RiskLevel.CRITICAL and r.status == "open"]
        return {
            "total_risks": len(self.risks),
            "by_level": dict(levels),
            "total_expected_loss": total_expected_loss,
            "critical_count": len(critical_risks),
            "above_tolerance": sum(1 for r in self.risks.values() if r.risk_score >= self.threshold),
        }

    def suggest_mitigations(self, risk_id: str) -> List[str]:
        if risk_id not in self.risks:
            return []
        risk = self.risks[risk_id]
        suggestions = []
        if risk.probability > 0.7:
            suggestions.append("Reduce probability: add controls, testing, or process gates")
        if risk.impact > 7:
            suggestions.append("Reduce impact: add fallbacks, redundancy, or insurance")
        if risk.risk_score >= self.threshold:
            suggestions.append("Consider avoiding the activity entirely")
            suggestions.append("Transfer risk via contracts or insurance")
        suggestions.append("Monitor regularly and update risk assessment")
        return suggestions


# ---------------------------------------------------------------------------
# Cost Estimator
# ---------------------------------------------------------------------------

class CostEstimator:
    """
    Estimates project costs including labor, infrastructure, and third-party services.
    """

    def __init__(self, default_hourly_rate: float = 100.0) -> None:
        self.default_hourly_rate = default_hourly_rate
        self.estimates: List[CostEstimate] = []

    def add_estimate(self, estimate: CostEstimate) -> None:
        self.estimates.append(estimate)

    def total_labor_cost(self) -> float:
        return sum(e.total_labor_with_contingency for e in self.estimates)

    def total_infrastructure_cost(self) -> float:
        return sum(e.infrastructure_monthly * 12 for e in self.estimates)

    def total_third_party_cost(self) -> float:
        return sum(e.third_party_monthly * 12 for e in self.estimates)

    def grand_total(self) -> float:
        return self.total_labor_cost() + self.total_infrastructure_cost() + self.total_third_party_cost()

    def generate_budget_report(self) -> Dict[str, Any]:
        by_category: Dict[str, float] = defaultdict(float)
        for e in self.estimates:
            by_category[e.category] += e.total_labor_with_contingency
        return {
            "total_labor": self.total_labor_cost(),
            "total_infrastructure": self.total_infrastructure_cost(),
            "total_third_party": self.total_third_party_cost(),
            "grand_total": self.grand_total(),
            "by_category": dict(by_category),
            "contingency_total": sum(e.labor_cost * e.contingency_pct for e in self.estimates),
            "num_estimates": len(self.estimates),
        }

    def estimate_from_tasks(self, tasks: List[Task], hourly_rate: Optional[float] = None) -> Dict[str, Any]:
        rate = hourly_rate or self.default_hourly_rate
        total_hours = sum(t.estimated_hours for t in tasks)
        total_points = sum(t.story_points for t in tasks)
        cost = total_hours * rate * 1.2  # 20% contingency
        return {
            "total_tasks": len(tasks),
            "total_hours": total_hours,
            "total_points": total_points,
            "labor_cost": cost,
            "avg_hours_per_task": total_hours / len(tasks) if tasks else 0,
            "avg_points_per_task": total_points / len(tasks) if tasks else 0,
        }


# ---------------------------------------------------------------------------
# Architecture Designer
# ---------------------------------------------------------------------------

class ArchitectureDesigner:
    """
    Guides architecture decisions, maintains ADRs, and generates
    architecture documentation.
    """

    def __init__(self, style: ArchitectureStyle = ArchitectureStyle.MODULAR_MONOLITH) -> None:
        self.style = style
        self.adrs: Dict[str, ArchitectureDecision] = {}
        self.components: List[Dict[str, Any]] = []
        self.data_stores: List[Dict[str, Any]] = []
        self.integrations: List[Dict[str, Any]] = []
        logger.info("ArchitectureDesigner initialized (style=%s)", style.value)

    def create_adr(self, adr: ArchitectureDecision) -> None:
        self.adrs[adr.adr_id] = adr
        logger.info("ADR created: %s - %s", adr.adr_id, adr.title)

    def add_component(
        self, name: str, description: str, tech: str, responsibilities: List[str]
    ) -> None:
        self.components.append({
            "name": name,
            "description": description,
            "technology": tech,
            "responsibilities": responsibilities,
        })

    def add_data_store(
        self, name: str, technology: str, purpose: str, schema_version: str = "1.0"
    ) -> None:
        self.data_stores.append({
            "name": name,
            "technology": technology,
            "purpose": purpose,
            "schema_version": schema_version,
        })

    def add_integration(
        self, name: str, source: str, target: str, protocol: str, description: str
    ) -> None:
        self.integrations.append({
            "name": name,
            "source": source,
            "target": target,
            "protocol": protocol,
            "description": description,
        })

    def generate_architecture_doc(self) -> Dict[str, Any]:
        return {
            "style": self.style.value,
            "components": self.components,
            "data_stores": self.data_stores,
            "integrations": self.integrations,
            "adr_count": len(self.adrs),
            "adrs": [
                {"id": a.adr_id, "title": a.title, "status": a.status}
                for a in self.adrs.values()
            ],
        }

    def ascii_diagram(self) -> str:
        lines = [
            f"Architecture: {self.style.value.upper()}",
            "=" * 50,
        ]
        if self.components:
            lines.append("")
            lines.append("Components:")
            for c in self.components:
                lines.append(f"  [{c['name']}] ({c['technology']})")
                for r in c.get("responsibilities", [])[:3]:
                    lines.append(f"    - {r}")
        if self.data_stores:
            lines.append("")
            lines.append("Data Stores:")
            for ds in self.data_stores:
                lines.append(f"  ({ds['name']}) [{ds['technology']}] - {ds['purpose']}")
        if self.integrations:
            lines.append("")
            lines.append("Integrations:")
            for ig in self.integrations:
                lines.append(f"  {ig['source']} --[{ig['protocol']}]--> {ig['target']}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Technical Debt Tracker
# ---------------------------------------------------------------------------

class TechDebtTracker:
    """Tracks and prioritizes technical debt items."""

    def __init__(self) -> None:
        self.debts: Dict[str, TechnicalDebt] = {}

    def add_debt(self, debt: TechnicalDebt) -> None:
        self.debts[debt.debt_id] = debt

    def prioritize(self) -> List[TechnicalDebt]:
        return sorted(
            self.debts.values(),
            key=lambda d: (d.interest_per_sprint * 10 + d.estimated_fix_hours),
            reverse=True,
        )

    def summary(self) -> Dict[str, Any]:
        total_fix_hours = sum(d.estimated_fix_hours for d in self.debts.values())
        total_interest = sum(d.interest_per_sprint for d in self.debts.values())
        return {
            "total_items": len(self.debts),
            "total_fix_hours": total_fix_hours,
            "total_interest_per_sprint": total_interest,
            "by_severity": {
                level.value: sum(1 for d in self.debts.values() if d.severity == level)
                for level in RiskLevel
            },
        }


# ---------------------------------------------------------------------------
# Performance Benchmarking
# ---------------------------------------------------------------------------

class PerformanceBenchmarks:
    """Tracks performance targets and measurements."""

    def __init__(self) -> None:
        self.benchmarks: Dict[str, PerformanceBenchmark] = {}

    def add_benchmark(self, bm: PerformanceBenchmark) -> None:
        self.benchmarks[bm.metric_name] = bm

    def update_actual(self, metric_name: str, actual_value: float) -> None:
        if metric_name in self.benchmarks:
            self.benchmarks[metric_name].actual_value = actual_value

    def status_report(self) -> Dict[str, Any]:
        results = {}
        met = 0
        not_met = 0
        for name, bm in self.benchmarks.items():
            status = "met" if bm.meets_target else ("pending" if bm.actual_value is None else "not_met")
            if status == "met":
                met += 1
            elif status == "not_met":
                not_met += 1
            results[name] = {
                "target": bm.target_value,
                "actual": bm.actual_value,
                "unit": bm.unit,
                "status": status,
                "deviation_pct": bm.deviation_pct,
            }
        return {
            "total": len(self.benchmarks),
            "met": met,
            "not_met": not_met,
            "details": results,
        }


# ---------------------------------------------------------------------------
# Project Roadmap
# ---------------------------------------------------------------------------

class ProjectRoadmap:
    """
    Manages the overall project timeline, phases, milestones,
    and dependencies.
    """

    def __init__(self, config: ProjectConfig) -> None:
        self.config = config
        self.milestones: List[Dict[str, Any]] = []
        self.dependencies: List[Dict[str, str]] = []

    def add_milestone(
        self, name: str, target_date: datetime, deliverables: List[str]
    ) -> None:
        self.milestones.append({
            "name": name,
            "target_date": target_date,
            "deliverables": deliverables,
            "status": "pending",
        })

    def add_dependency(self, predecessor: str, successor: str) -> None:
        self.dependencies.append({"predecessor": predecessor, "successor": successor})

    def get_critical_path(self) -> List[str]:
        if not self.milestones:
            return []
        sorted_ms = sorted(self.milestones, key=lambda m: m["target_date"])
        return [m["name"] for m in sorted_ms]

    def generate_timeline(self) -> Dict[str, Any]:
        sorted_ms = sorted(self.milestones, key=lambda m: m["target_date"])
        if not sorted_ms:
            return {"milestones": [], "total_duration_days": 0}
        start = self.config.start_date or datetime.utcnow()
        end = sorted_ms[-1]["target_date"]
        return {
            "project_name": self.config.project_name,
            "start_date": start,
            "end_date": end,
            "total_duration_days": (end - start).days,
            "milestones": sorted_ms,
            "dependencies": self.dependencies,
        }


# ---------------------------------------------------------------------------
# Main demonstration
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("=" * 60)
    print("Full-Stack Planner Agent — Comprehensive Demo")
    print("=" * 60)

    # Tech Stack Evaluation
    evaluator = TechStackEvaluator()
    evaluator.register_tech(TechStack("React", TechCategory.FRONTEND, "18.2", "stable", 9.5, 8.0, 7.0, 9.0, 0, "mit", pros=["Huge ecosystem", "Virtual DOM"], cons=["Learning curve"], alternatives=["Vue", "Angular"]))
    evaluator.register_tech(TechStack("Vue", TechCategory.FRONTEND, "3.3", "stable", 8.0, 7.5, 8.5, 7.5, 0, "mit", pros=["Easy to learn", "Flexible"], cons=["Smaller ecosystem"], alternatives=["React", "Angular"]))
    evaluator.register_tech(TechStack("FastAPI", TechCategory.BACKEND, "0.100", "stable", 7.5, 9.0, 7.0, 7.0, 0, "mit", pros=["Async support", "Type hints"], cons=["Newer"], alternatives=["Django", "Flask"]))
    evaluator.register_tech(TechStack("PostgreSQL", TechCategory.DATABASE, "15", "stable", 9.0, 8.5, 6.0, 9.0, 50, "postgresql", pros=["Feature-rich", "Reliable"], cons=["Complex setup"], alternatives=["MySQL", "MongoDB"]))

    print("\n--- Tech Stack Evaluation ---")
    frontend = evaluator.evaluate_category(TechCategory.FRONTEND)
    print(f"Frontend ranking: {frontend}")
    backend = evaluator.evaluate_category(TechCategory.BACKEND)
    print(f"Backend ranking: {backend}")

    # Sprint Planning
    planner = SprintPlanner(ProjectConfig(project_name="E-Commerce Platform", team_name="Alpha"))
    sprint1 = planner.create_sprint("S1", "Sprint 1", datetime.utcnow(), datetime.utcnow() + timedelta(days=14), "Core API")

    tasks = [
        Task("T1", "User Auth API", "JWT auth", Priority.HIGH, story_points=8, estimated_hours=16),
        Task("T2", "Product CRUD", "REST endpoints", Priority.HIGH, story_points=5, estimated_hours=10),
        Task("T3", "Shopping Cart", "Session-based cart", Priority.MEDIUM, story_points=8, estimated_hours=20),
        Task("T4", "UI Dashboard", "React admin panel", Priority.MEDIUM, story_points=13, estimated_hours=30),
        Task("T5", "CI/CD Pipeline", "GitHub Actions", Priority.HIGH, story_points=5, estimated_hours=8),
    ]
    for t in tasks:
        planner.add_task(t)

    plan_result = planner.plan_sprint("S1", ["T1", "T2", "T5"], team_capacity_hours=160)
    print(f"\n--- Sprint Planning ---")
    print(f"Tasks planned: {plan_result['tasks_planned']}, Points: {plan_result['total_points']}")

    # Resource Allocation
    allocator = ResourceAllocator()
    allocator.add_member(TeamMember("Alice", TeamRole.TECH_LEAD, ["python", "react", "devops"], 150, 40, 0.3, 1.2))
    allocator.add_member(TeamMember("Bob", TeamRole.DEVELOPER, ["python", "react"], 100, 40, 0.5, 1.0))
    allocator.add_member(TeamMember("Carol", TeamRole.DEVELOPER, ["python", "sql"], 100, 40, 0.2, 1.0))
    capacity = allocator.get_team_capacity()
    print(f"\n--- Resource Allocation ---")
    print(f"Team size: {capacity['team_size']}, Remaining hours: {capacity['total_remaining_hours']}")

    # Risk Management
    risk_mgr = RiskManager(risk_tolerance="medium")
    risk_mgr.add_risk(Risk("R1", "Key developer leaves", 0.3, 8, mitigation="Cross-train team"))
    risk_mgr.add_risk(Risk("R2", "Scope creep", 0.7, 6, mitigation="Strict change control"))
    risk_mgr.add_risk(Risk("R3", "Performance bottleneck", 0.5, 7, mitigation="Early load testing"))
    summary = risk_mgr.get_risk_summary()
    print(f"\n--- Risk Management ---")
    print(f"Total risks: {summary['total_risks']}, Critical: {summary['critical_count']}")

    # Cost Estimation
    estimator = CostEstimator()
    estimator.add_estimate(CostEstimate("Backend", "API development", 200, 120, 0.2, 500, 200))
    estimator.add_estimate(CostEstimate("Frontend", "UI development", 150, 100, 0.2, 0, 100))
    estimator.add_estimate(CostEstimate("DevOps", "Infrastructure", 80, 150, 0.15, 2000, 300))
    budget = estimator.generate_budget_report()
    print(f"\n--- Cost Estimation ---")
    print(f"Grand total: ${budget['grand_total']:,.0f}")

    # Architecture
    arch = ArchitectureDesigner(ArchitectureStyle.MODULAR_MONOLITH)
    arch.add_component("API Gateway", "Request routing", "FastAPI", ["Routing", "Auth", "Rate limiting"])
    arch.add_component("User Service", "User management", "Python", ["Registration", "Profile", "Auth"])
    arch.add_component("Product Service", "Product catalog", "Python", ["CRUD", "Search", "Inventory"])
    arch.add_data_store("PostgreSQL", "PostgreSQL", "Primary data store")
    arch.add_data_store("Redis", "Redis", "Session cache")
    arch.add_integration("REST API", "Frontend", "API Gateway", "HTTPS", "Primary API")
    print(f"\n--- Architecture ---")
    print(arch.ascii_diagram())

    # Technical Debt
    debt_tracker = TechDebtTracker()
    debt_tracker.add_debt(TechnicalDebt("D1", "Legacy auth module", RiskLevel.HIGH, "auth", 20, 5))
    debt_tracker.add_debt(TechnicalDebt("D2", "Missing tests", RiskLevel.MEDIUM, "testing", 40, 3))
    debt_tracker.summary()
    print(f"\n--- Technical Debt ---")
    print(f"Items: {debt_tracker.summary()['total_items']}, Total fix hours: {debt_tracker.summary()['total_fix_hours']}")

    # Performance Benchmarks
    perf = PerformanceBenchmarks()
    perf.add_benchmark(PerformanceBenchmark("API Response Time", 200, 180, "ms", 300, 500))
    perf.add_benchmark(PerformanceBenchmark("Page Load Time", 2.0, 1.8, "s", 3.0, 5.0))
    perf.add_benchmark(PerformanceBenchmark("Uptime", 99.9, 99.95, "%", 99.5, 99.0))
    print(f"\n--- Performance Benchmarks ---")
    status = perf.status_report()
    print(f"Metrics: {status['total']}, Met: {status['met']}, Not met: {status['not_met']}")

    print("\n" + "=" * 60)
    print("Full-Stack Planner Agent demo complete.")
    print("=" * 60)
