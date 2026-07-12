"""
workforce_planning.py — Workforce planning platform: headcount forecasting,
skills inventory, succession pipeline, and capacity planning.

Provides data models and engines for strategic workforce planning.
"""

from __future__ import annotations

import math
import statistics
import uuid
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Optional


# ─── Enums ────────────────────────────────────────────────────────────────────

class SkillProficiency(Enum):
    NOVICE = 1
    BEGINNER = 2
    INTERMEDIATE = 3
    ADVANCED = 4
    EXPERT = 5


class ScenarioType(Enum):
    BEST_CASE = "best_case"
    BASE_CASE = "base_case"
    WORST_CASE = "worst_case"
    CUSTOM = "custom"


class CriticalityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ReadinessLevel(Enum):
    NOT_READY = "not_ready"
    READY_1_2_YEARS = "ready_in_1_2_years"
    READY_NEXT_ROLE = "ready_for_next_role"
    READY_NOW = "ready_now"


class UtilizationStatus(Enum):
    UNDER_UTILIZED = "under_utilized"
    OPTIMAL = "optimal"
    HIGH = "high"
    OVER_UTILIZED = "over_utilized"
    BURNOUT_RISK = "burnout_risk"


class ProjectPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class DemandCategory(Enum):
    DEVELOPMENT = "development"
    MAINTENANCE = "maintenance"
    STRATEGIC = "strategic"
    OPERATIONAL = "operational"


# ─── Data Classes ─────────────────────────────────────────────────────────────

@dataclass
class GrowthAssumptions:
    """Assumptions for headcount growth modeling."""
    annual_growth_rate: float
    annual_attrition_rate: float
    internal_mobility_rate: float
    cost_per_hire: float
    avg_salary: float

    @property
    def net_growth_rate(self) -> float:
        return self.annual_growth_rate - self.annual_attrition_rate + self.internal_mobility_rate


@dataclass
class BudgetImpact:
    """Budget impact of headcount changes."""
    new_hire_cost: float
    attrition_cost: float
    total_budget_required: float
    cost_per_employee: float


@dataclass
class Scenario:
    """A planning scenario."""
    scenario_type: ScenarioType
    growth_rate_modifier: float
    attrition_rate_modifier: float
    description: str


@dataclass
class HeadcountProjection:
    """Headcount projection for a single period."""
    month: int
    year: int
    starting_count: int
    new_hires: int
    departures: int
    internal_moves: int
    ending_count: int

    @property
    def net_change(self) -> int:
        return self.ending_count - self.starting_count

    @property
    def change_pct(self) -> float:
        if self.starting_count == 0:
            return 0.0
        return round(self.net_change / self.starting_count, 4)


@dataclass
class HeadcountPlan:
    """Complete headcount planning document."""
    plan_id: str
    department: str
    current_count: int
    projections: list[HeadcountProjection]
    assumptions: GrowthAssumptions
    scenarios: list[Scenario]
    created_at: date = field(default_factory=date.today)

    @property
    def final_count(self) -> int:
        return self.projections[-1].ending_count if self.projections else self.current_count

    @property
    def total_net_change(self) -> int:
        return self.final_count - self.current_count

    @property
    def total_new_hires(self) -> int:
        return sum(p.new_hires for p in self.projections)

    @property
    def total_departures(self) -> int:
        return sum(p.departures for p in self.projections)


@dataclass
class SkillAsset:
    """A skill in the organizational inventory."""
    skill_name: str
    category: str
    proficiency_level: SkillProficiency
    certified_count: int
    proficient_count: int
    total_holders: int
    demand_forecast: float

    @property
    def supply_ratio(self) -> float:
        if self.demand_forecast == 0:
            return 1.0
        return self.proficient_count / self.demand_forecast

    @property
    def surplus_deficit(self) -> int:
        return self.proficient_count - int(self.demand_forecast)


@dataclass
class SkillGap:
    """Gap between skill supply and demand."""
    skill_name: str
    current_supply: int
    forecasted_demand: float
    gap: float
    time_to_close_months: int
    severity: str

    def __post_init__(self) -> None:
        self.gap = round(self.current_supply - self.forecasted_demand, 1)
        if self.gap < -5:
            self.severity = "critical"
        elif self.gap < -2:
            self.severity = "high"
        elif self.gap < 0:
            self.severity = "medium"
        else:
            self.severity = "surplus"


@dataclass
class SupplyDemandReport:
    """Skills supply vs demand analysis."""
    report_date: date
    total_skills: int
    surplus_skills: int
    deficit_skills: int
    critical_gaps: list[SkillGap]
    overall_health: float


@dataclass
class SkillsInventory:
    """Complete organizational skills inventory."""
    inventory_id: str
    organization_id: str
    skills: list[SkillAsset]
    last_updated: datetime = field(default_factory=datetime.now)

    def find_gap(self, skill_name: str) -> Optional[SkillGap]:
        for skill in self.skills:
            if skill.skill_name.lower() == skill_name.lower():
                if skill.surplus_deficit < 0:
                    return SkillGap(
                        skill_name=skill.skill_name,
                        current_supply=skill.proficient_count,
                        forecasted_demand=skill.demand_forecast,
                        gap=0.0,
                        time_to_close_months=6,
                        severity="medium",
                    )
        return None

    def critical_deficits(self, threshold: float = -2.0) -> list[SkillAsset]:
        return [s for s in self.skills if s.surplus_deficit < threshold]


@dataclass
class Successor:
    """A successor candidate for a critical role."""
    employee_id: str
    employee_name: str
    current_role: str
    readiness_level: ReadinessLevel
    readiness_score: float
    potential_score: float
    time_to_ready_months: int
    development_actions: list[str]


@dataclass
class CriticalRole:
    """A role identified as critical to business operations."""
    role_id: str
    role_title: str
    department: str
    incumbent_id: str
    incumbent_name: str
    criticality: CriticalityLevel
    business_impact_score: float
    replacement_difficulty: float
    vacancy_risk: float
    successors: list[Successor]

    @property
    def has_ready_successor(self) -> bool:
        return any(s.readiness_level == ReadinessLevel.READY_NOW for s in self.successors)

    @property
    def pipeline_depth(self) -> int:
        return len(self.successors)

    @property
    def risk_score(self) -> float:
        successor_risk = 0.0 if self.has_ready_successor else 0.4
        return round(
            self.vacancy_risk * 0.3 +
            self.replacement_difficulty * 0.3 +
            successor_risk * 0.4,
            4,
        )


@dataclass
class CoverageGap:
    """A gap in succession coverage."""
    role_id: str
    role_title: str
    gap_type: str
    severity: str
    recommendation: str


@dataclass
class SuccessionPipeline:
    """Complete succession planning pipeline."""
    pipeline_id: str
    critical_roles: list[CriticalRole]
    created_at: date = field(default_factory=date.today)

    @property
    def coverage_ratio(self) -> float:
        if not self.critical_roles:
            return 1.0
        covered = sum(1 for r in self.critical_roles if r.has_ready_successor)
        return covered / len(self.critical_roles)

    @property
    def health_score(self) -> float:
        if not self.critical_roles:
            return 1.0
        scores = [1.0 - r.risk_score for r in self.critical_roles]
        return round(statistics.mean(scores), 4)


@dataclass
class TeamMember:
    """A team member for capacity planning."""
    employee_id: str
    name: str
    role: str
    skills: list[str]
    available_hours_per_week: float
    allocated_hours: float = 0.0

    @property
    def utilization(self) -> float:
        if self.available_hours_per_week == 0:
            return 0.0
        return round(self.allocated_hours / self.available_hours_per_week, 4)

    @property
    def available_capacity(self) -> float:
        return self.available_hours_per_week - self.allocated_hours

    @property
    def status(self) -> UtilizationStatus:
        u = self.utilization
        if u < 0.5:
            return UtilizationStatus.UNDER_UTILIZED
        elif u <= 0.8:
            return UtilizationStatus.OPTIMAL
        elif u <= 0.9:
            return UtilizationStatus.HIGH
        elif u <= 1.0:
            return UtilizationStatus.OVER_UTILIZED
        return UtilizationStatus.BURNOUT_RISK


@dataclass
class Project:
    """A project requiring staffing."""
    project_id: str
    name: str
    priority: ProjectPriority
    required_skills: list[str]
    estimated_hours: float
    deadline: date
    category: DemandCategory
    min_team_size: int = 1


@dataclass
class Allocation:
    """Staffing allocation for a project."""
    project_id: str
    employee_id: str
    hours_allocated: float
    skill_match_score: float
    start_date: date
    end_date: date


@dataclass
class TeamCapacity:
    """Capacity summary for a team."""
    team_id: str
    team_name: str
    members: list[TeamMember]
    utilization_target: float = 0.80

    @property
    def total_capacity(self) -> float:
        return sum(m.available_hours_per_week for m in self.members)

    @property
    def total_allocated(self) -> float:
        return sum(m.allocated_hours for m in self.members)

    @property
    def team_utilization(self) -> float:
        if self.total_capacity == 0:
            return 0.0
        return round(self.total_allocated / self.total_capacity, 4)

    @property
    def available_capacity(self) -> float:
        return self.total_capacity - self.total_allocated

    @property
    def bottleneck_risk(self) -> str:
        u = self.team_utilization
        if u > 0.90:
            return "high"
        elif u > 0.80:
            return "medium"
        return "low"


@dataclass
class DemandForecast:
    """Demand forecast for a planning period."""
    forecast_id: str
    period_months: int
    projects: list[Project]
    total_hours_required: float
    peak_month: int
    skill_demands: dict[str, float]


@dataclass
class CapacityReport:
    """Capacity planning report."""
    report_date: date
    teams: list[TeamCapacity]
    demand_forecast: DemandForecast
    bottlenecks: list[str]
    recommendations: list[str]
    overall_utilization: float


# ─── Engines ──────────────────────────────────────────────────────────────────

class HeadcountForecaster:
    """Headcount forecasting with scenario planning."""

    def __init__(self, horizon_months: int = 24) -> None:
        self.horizon_months = horizon_months

    def project(
        self,
        current_count: int,
        assumptions: GrowthAssumptions,
        months: Optional[int] = None,
    ) -> list[HeadcountProjection]:
        horizon = months or self.horizon_months
        projections: list[HeadcountProjection] = []
        count = current_count

        for m in range(1, horizon + 1):
            monthly_growth = assumptions.annual_growth_rate / 12
            monthly_attrition = assumptions.annual_attrition_rate / 12
            monthly_mobility = assumptions.internal_mobility_rate / 12

            new_hires = max(0, round(count * monthly_growth))
            departures = max(0, round(count * monthly_attrition))
            moves = round(count * monthly_mobility)

            ending = count + new_hires - departures
            year = date.today().year + ((date.today().month + m - 1) // 12)
            month_num = ((date.today().month + m - 1) % 12) + 1

            projections.append(HeadcountProjection(
                month=month_num, year=year,
                starting_count=count, new_hires=new_hires,
                departures=departures, internal_moves=moves,
                ending_count=ending,
            ))
            count = ending

        return projections

    def plan_with_scenarios(
        self,
        department: str,
        current_count: int,
        base_assumptions: GrowthAssumptions,
        scenarios: list[Scenario],
    ) -> dict[str, HeadcountPlan]:
        plans: dict[str, HeadcountPlan] = {}
        for scenario in scenarios:
            modified = GrowthAssumptions(
                annual_growth_rate=base_assumptions.annual_growth_rate * (1 + scenario.growth_rate_modifier),
                annual_attrition_rate=base_assumptions.annual_attrition_rate * (1 + scenario.attrition_rate_modifier),
                internal_mobility_rate=base_assumptions.internal_mobility_rate,
                cost_per_hire=base_assumptions.cost_per_hire,
                avg_salary=base_assumptions.avg_salary,
            )
            projections = self.project(current_count, modified)
            plans[scenario.scenario_type.value] = HeadcountPlan(
                plan_id=str(uuid.uuid4())[:8],
                department=department,
                current_count=current_count,
                projections=projections,
                assumptions=modified,
                scenarios=[scenario],
            )
        return plans

    def budget_impact(
        self, plan: HeadcountPlan, cost_per_hire: Optional[float] = None
    ) -> BudgetImpact:
        cph = cost_per_hire or plan.assumptions.cost_per_hire
        new_hire_cost = plan.total_new_hires * cph
        attrition_cost = plan.total_departures * cph * 0.5
        salary_cost = plan.final_count * plan.assumptions.avg_salary
        return BudgetImpact(
            new_hire_cost=round(new_hire_cost, 2),
            attrition_cost=round(attrition_cost, 2),
            total_budget_required=round(salary_cost + new_hire_cost + attrition_cost, 2),
            cost_per_employee=round((salary_cost + new_hire_cost) / max(1, plan.final_count), 2),
        )


class SkillsInventoryManager:
    """Skills inventory management and gap analysis."""

    def __init__(self) -> None:
        self._inventory: Optional[SkillsInventory] = None

    def register_inventory(self, inventory: SkillsInventory) -> None:
        self._inventory = inventory

    def supply_demand_analysis(self) -> SupplyDemandReport:
        if not self._inventory:
            return SupplyDemandReport(
                report_date=date.today(), total_skills=0,
                surplus_skills=0, deficit_skills=0,
                critical_gaps=[], overall_health=0.0,
            )

        surplus = sum(1 for s in self._inventory.skills if s.surplus_deficit > 0)
        deficit = sum(1 for s in self._inventory.skills if s.surplus_deficit < 0)
        critical = [
            SkillGap(
                skill_name=s.skill_name,
                current_supply=s.proficient_count,
                forecasted_demand=s.demand_forecast,
                gap=0.0,
                time_to_close_months=6,
                severity="",
            )
            for s in self._inventory.critical_deficits(threshold=-3)
        ]
        total = len(self._inventory.skills)
        health = surplus / total if total > 0 else 0.0

        return SupplyDemandReport(
            report_date=date.today(),
            total_skills=total,
            surplus_skills=surplus,
            deficit_skills=deficit,
            critical_gaps=critical,
            overall_health=round(health, 4),
        )

    def forecast_gaps(self, months_ahead: int = 12) -> list[SkillGap]:
        if not self._inventory:
            return []
        gaps: list[SkillGap] = []
        for skill in self._inventory.skills:
            projected_demand = skill.demand_forecast * (1 + 0.1 * months_ahead / 12)
            gap_size = skill.proficient_count - projected_demand
            if gap_size < 0:
                gaps.append(SkillGap(
                    skill_name=skill.skill_name,
                    current_supply=skill.proficient_count,
                    forecasted_demand=round(projected_demand, 1),
                    gap=round(gap_size, 1),
                    time_to_close_months=max(3, int(abs(gap_size) * 3)),
                    severity="",
                ))
        return sorted(gaps, key=lambda g: g.gap)


class SuccessionPlanner:
    """Succession pipeline planning and risk assessment."""

    def __init__(self, readiness_threshold: float = 0.70) -> None:
        self.readiness_threshold = readiness_threshold

    def assess_pipeline_health(self, pipeline: SuccessionPipeline) -> dict[str, object]:
        return {
            "total_critical_roles": len(pipeline.critical_roles),
            "covered_roles": sum(1 for r in pipeline.critical_roles if r.has_ready_successor),
            "coverage_ratio": pipeline.coverage_ratio,
            "health_score": pipeline.health_score,
            "at_risk_roles": [
                r.role_title for r in pipeline.critical_roles
                if r.risk_score > 0.6
            ],
        }

    def identify_coverage_gaps(self, pipeline: SuccessionPipeline) -> list[CoverageGap]:
        gaps: list[CoverageGap] = []
        for role in pipeline.critical_roles:
            if not role.has_ready_successor:
                gaps.append(CoverageGap(
                    role_id=role.role_id,
                    role_title=role.role_title,
                    gap_type="no_ready_successor",
                    severity=role.criticality.value,
                    recommendation=f"Accelerate development for {role.pipeline_depth} pipeline candidates",
                ))
            if role.pipeline_depth < 2:
                gaps.append(CoverageGap(
                    role_id=role.role_id,
                    role_title=role.role_title,
                    gap_type="thin_pipeline",
                    severity="medium",
                    recommendation="Recruit external candidates or expand internal talent pool",
                ))
        return gaps

    def development_timeline(self, role: CriticalRole) -> dict[str, object]:
        timelines: list[dict] = []
        for s in role.successors:
            timelines.append({
                "candidate": s.employee_name,
                "current_readiness": s.readiness_level.value,
                "score": s.readiness_score,
                "months_to_ready": s.time_to_ready_months,
                "actions": s.development_actions,
            })
        return {
            "role": role.role_title,
            "criticality": role.criticality.value,
            "successors": timelines,
            "earliest_ready": min(
                (s.time_to_ready_months for s in role.successors), default=999
            ),
        }


class CapacityPlanner:
    """Team capacity planning and project allocation engine."""

    def __init__(self, utilization_target: float = 0.80, burnout_threshold: float = 0.90) -> None:
        self.utilization_target = utilization_target
        self.burnout_threshold = burnout_threshold

    def analyze_team(self, team: TeamCapacity) -> dict[str, object]:
        utilization = team.team_utilization
        statuses = [m.status.value for m in team.members]
        over_allocated = [m.name for m in team.members if m.status in (
            UtilizationStatus.OVER_UTILIZED, UtilizationStatus.BURNOUT_RISK
        )]
        under_allocated = [m.name for m in team.members if m.status == UtilizationStatus.UNDER_UTILIZED]

        return {
            "team": team.team_name,
            "members": len(team.members),
            "total_capacity": team.total_capacity,
            "allocated": team.total_allocated,
            "utilization": utilization,
            "target": self.utilization_target,
            "on_track": abs(utilization - self.utilization_target) <= 0.10,
            "over_allocated": over_allocated,
            "under_allocated": under_allocated,
            "bottleneck_risk": team.bottleneck_risk,
        }

    def optimize_allocation(
        self, projects: list[Project], team: TeamCapacity
    ) -> list[Allocation]:
        allocations: list[Allocation] = []
        available = {m.employee_id: m.available_capacity for m in team.members}
        sorted_projects = sorted(projects, key=lambda p: p.priority.value, reverse=True)

        for project in sorted_projects:
            best_member = None
            best_score = -1.0
            for member in team.members:
                if available.get(member.employee_id, 0) <= 0:
                    continue
                skill_match = len(
                    set(project.required_skills) & set(member.skills)
                ) / max(1, len(project.required_skills))
                capacity_score = min(1.0, available[member.employee_id] / max(1, project.estimated_hours))
                score = skill_match * 0.6 + capacity_score * 0.4
                if score > best_score:
                    best_score = score
                    best_member = member

            if best_member:
                alloc_hours = min(project.estimated_hours, available[best_member.employee_id])
                allocations.append(Allocation(
                    project_id=project.project_id,
                    employee_id=best_member.employee_id,
                    hours_allocated=alloc_hours,
                    skill_match_score=round(best_score, 3),
                    start_date=date.today(),
                    end_date=project.deadline,
                ))
                available[best_member.employee_id] -= alloc_hours

        return allocations

    def demand_forecast(
        self, projects: list[Project], horizon_months: int = 6
    ) -> DemandForecast:
        total_hours = sum(p.estimated_hours for p in projects)
        skill_demands: dict[str, float] = {}
        for p in projects:
            for skill in p.required_skills:
                skill_demands[skill] = skill_demands.get(skill, 0) + p.estimated_hours / len(p.required_skills)

        peak_month = 1
        monthly_hours = [total_hours / horizon_months] * horizon_months

        return DemandForecast(
            forecast_id=str(uuid.uuid4())[:8],
            period_months=horizon_months,
            projects=projects,
            total_hours_required=total_hours,
            peak_month=peak_month,
            skill_demands=skill_demands,
        )

    def generate_report(
        self,
        teams: list[TeamCapacity],
        demand: DemandForecast,
    ) -> CapacityReport:
        bottlenecks: list[str] = []
        recommendations: list[str] = []

        total_utilizations = []
        for team in teams:
            analysis = self.analyze_team(team)
            total_utilizations.append(analysis["utilization"])
            if analysis["bottleneck_risk"] == "high":
                bottlenecks.append(team.team_name)
                recommendations.append(
                    f"Team '{team.team_name}' at {analysis['utilization']:.0%} — "
                    "consider hiring or redistributing workload"
                )

        overall = statistics.mean(total_utilizations) if total_utilizations else 0.0

        for skill, hours in sorted(demand.skill_demands.items(), key=lambda x: -x[1])[:5]:
            recommendations.append(f"High demand for '{skill}': {hours:.0f}h projected")

        return CapacityReport(
            report_date=date.today(),
            teams=teams,
            demand_forecast=demand,
            bottlenecks=bottlenecks,
            recommendations=recommendations,
            overall_utilization=round(overall, 4),
        )


# ─── Main Demo ────────────────────────────────────────────────────────────────

def main() -> None:
    """Demonstrate the workforce planning platform end-to-end."""
    print("=" * 72)
    print("  WORKFORCE PLANNING PLATFORM DEMO")
    print("=" * 72)

    # 1. Headcount Forecasting
    print("\n[1] HEADCOUNT FORECASTING")
    print("-" * 40)
    forecaster = HeadcountForecaster(horizon_months=12)
    assumptions = GrowthAssumptions(
        annual_growth_rate=0.20, annual_attrition_rate=0.15,
        internal_mobility_rate=0.05, cost_per_hire=8000,
        avg_salary=120000,
    )
    scenarios = [
        Scenario(ScenarioType.BEST_CASE, 0.2, -0.2, "Aggressive growth, low attrition"),
        Scenario(ScenarioType.BASE_CASE, 0.0, 0.0, "Standard projections"),
        Scenario(ScenarioType.WORST_CASE, -0.3, 0.3, "Conservative growth, high attrition"),
    ]

    plans = forecaster.plan_with_scenarios("Engineering", 50, assumptions, scenarios)
    for scenario_name, plan in plans.items():
        print(f"\n  Scenario: {scenario_name.upper()}")
        print(f"    Start: {plan.current_count} -> End: {plan.final_count} "
              f"(net {plan.total_net_change:+d})")
        print(f"    New hires: {plan.total_new_hires}, Departures: {plan.total_departures}")
        budget = forecaster.budget_impact(plan)
        print(f"    Budget: ${budget.total_budget_required:,.0f} "
              f"(${budget.cost_per_employee:,.0f}/employee)")

    base_plan = plans["base_case"]
    print(f"\n  Base Case Monthly Projections:")
    for p in base_plan.projections[:6]:
        print(f"    {p.year}-{p.month:02d}: {p.starting_count} -> {p.ending_count} "
              f"(+{p.new_hires}h, -{p.departures}d)")

    # 2. Skills Inventory
    print("\n[2] SKILLS INVENTORY & GAP ANALYSIS")
    print("-" * 40)
    inventory_manager = SkillsInventoryManager()
    inventory = SkillsInventory(
        inventory_id="SI-001", organization_id="ORG-001",
        skills=[
            SkillAsset("Python", "programming", SkillProficiency.ADVANCED, 15, 25, 30, 20.0),
            SkillAsset("Machine Learning", "ai", SkillProficiency.INTERMEDIATE, 5, 8, 12, 18.0),
            SkillAsset("Kubernetes", "devops", SkillProficiency.BEGINNER, 3, 6, 10, 15.0),
            SkillAsset("React", "frontend", SkillProficiency.ADVANCED, 12, 20, 22, 12.0),
            SkillAsset("SQL", "data", SkillProficiency.EXPERT, 18, 28, 32, 16.0),
        ],
    )
    inventory_manager.register_inventory(inventory)

    report = inventory_manager.supply_demand_analysis()
    print(f"  Total Skills:    {report.total_skills}")
    print(f"  Surplus:         {report.surplus_skills}")
    print(f"  Deficit:         {report.deficit_skills}")
    print(f"  Health:          {report.overall_health:.0%}")
    print(f"  Critical Gaps:   {len(report.critical_gaps)}")

    print(f"\n  Skill Supply vs Demand:")
    for skill in inventory.skills:
        status = "SURPLUS" if skill.surplus_deficit > 0 else "DEFICIT"
        print(f"    {skill.skill_name:20s} supply={skill.proficient_count:3d} "
              f"demand={skill.demand_forecast:5.1f} gap={skill.surplus_deficit:+3d} [{status}]")

    future_gaps = inventory_manager.forecast_gaps(months_ahead=12)
    print(f"\n  12-Month Gap Forecast: {len(future_gaps)} gaps")
    for gap in future_gaps[:3]:
        print(f"    {gap.skill_name:20s} gap={gap.gap:+.1f} "
              f"(close in {gap.time_to_close_months} months)")

    # 3. Succession Planning
    print("\n[3] SUCCESSION PIPELINE")
    print("-" * 40)
    planner = SuccessionPlanner(readiness_threshold=0.70)
    pipeline = SuccessionPipeline(
        pipeline_id="SP-001",
        critical_roles=[
            CriticalRole(
                role_id="R1", role_title="VP Engineering", department="Engineering",
                incumbent_id="E007", incumbent_name="George Brown",
                criticality=CriticalityLevel.CRITICAL,
                business_impact_score=0.95, replacement_difficulty=0.8,
                vacancy_risk=0.3,
                successors=[
                    Successor("E001", "Alice Chen", "Senior Engineer",
                              ReadinessLevel.READY_NEXT_ROLE, 0.72, 0.85, 12,
                              ["Leadership training", "Mentorship program"]),
                    Successor("E004", "Diana Johnson", "Product Manager",
                              ReadinessLevel.READY_1_2_YEARS, 0.55, 0.70, 24,
                              ["Technical depth", "Engineering management"]),
                ],
            ),
            CriticalRole(
                role_id="R2", role_title="Head of Sales", department="Sales",
                incumbent_id="E002", incumbent_name="Bob Williams",
                criticality=CriticalityLevel.HIGH,
                business_impact_score=0.85, replacement_difficulty=0.6,
                vacancy_risk=0.25,
                successors=[
                    Successor("E003", "Carlos Rivera", "Sales Rep",
                              ReadinessLevel.READY_NOW, 0.82, 0.75, 0,
                              ["Sales leadership course"]),
                ],
            ),
        ],
    )

    health = planner.assess_pipeline_health(pipeline)
    print(f"  Pipeline Health: {health['health_score']:.2%}")
    print(f"  Coverage:        {health['coverage_ratio']:.0%}")
    print(f"  Critical Roles:  {health['total_critical_roles']}")
    print(f"  At Risk:         {health['at_risk_roles']}")

    gaps = planner.identify_coverage_gaps(pipeline)
    print(f"\n  Coverage Gaps: {len(gaps)}")
    for gap in gaps:
        print(f"    [{gap.severity}] {gap.role_title}: {gap.gap_type}")
        print(f"      Recommendation: {gap.recommendation}")

    for role in pipeline.critical_roles:
        timeline = planner.development_timeline(role)
        print(f"\n  Development Timeline: {role.role_title}")
        print(f"    Earliest ready: {timeline['earliest_ready']} months")
        for s in timeline["successors"]:
            print(f"    - {s['candidate']}: {s['current_readiness']} "
                  f"({s['months_to_ready']} months, score={s['score']:.2f})")

    # 4. Capacity Planning
    print("\n[4] CAPACITY PLANNING")
    print("-" * 40)
    capacity_planner = CapacityPlanner(utilization_target=0.80, burnout_threshold=0.90)

    team = TeamCapacity(
        team_id="T1", team_name="Platform Team",
        members=[
            TeamMember("E001", "Alice Chen", "Senior Engineer", ["python", "kubernetes"], 40, 35),
            TeamMember("E003", "Carlos Rivera", "Engineer", ["python", "sql"], 40, 28),
            TeamMember("E006", "Fiona Park", "Senior Designer", ["react", "design"], 40, 32),
            TeamMember("E008", "Hana Tanaka", "Analyst", ["sql", "python"], 40, 20),
        ],
    )

    analysis = capacity_planner.analyze_team(team)
    print(f"  Team:            {analysis['team']}")
    print(f"  Members:         {analysis['members']}")
    print(f"  Utilization:     {analysis['utilization']:.0%} (target: {analysis['target']:.0%})")
    print(f"  On Track:        {analysis['on_track']}")
    print(f"  Over-allocated:  {analysis['over_allocated']}")
    print(f"  Under-allocated: {analysis['under_allocated']}")
    print(f"  Bottleneck Risk: {analysis['bottleneck_risk']}")

    projects = [
        Project("P1", "API Refactor", ProjectPriority.HIGH, ["python", "kubernetes"], 80, date(2026, 9, 30), DemandCategory.DEVELOPMENT),
        Project("P2", "Dashboard Redesign", ProjectPriority.MEDIUM, ["react", "design"], 60, date(2026, 10, 15), DemandCategory.STRATEGIC),
        Project("P3", "Data Pipeline", ProjectPriority.CRITICAL, ["python", "sql"], 100, date(2026, 8, 31), DemandCategory.OPERATIONAL),
    ]

    allocations = capacity_planner.optimize_allocation(projects, team)
    print(f"\n  Optimal Allocations:")
    for alloc in allocations:
        print(f"    {alloc.project_id} -> {alloc.employee_id}: {alloc.hours_allocated:.0f}h "
              f"(match={alloc.skill_match_score:.2f})")

    demand = capacity_planner.demand_forecast(projects, horizon_months=6)
    print(f"\n  Demand Forecast:")
    print(f"    Total hours:  {demand.total_hours_required:.0f}")
    print(f"    Peak month:   {demand.peak_month}")
    print(f"    Skill demands:")
    for skill, hours in sorted(demand.skill_demands.items(), key=lambda x: -x[1]):
        print(f"      {skill:20s} {hours:.0f}h")

    cap_report = capacity_planner.generate_report([team], demand)
    print(f"\n  Capacity Report:")
    print(f"    Overall utilization: {cap_report.overall_utilization:.0%}")
    print(f"    Bottlenecks: {cap_report.bottlenecks}")
    print(f"    Recommendations:")
    for rec in cap_report.recommendations:
        print(f"      - {rec}")

    print("\n" + "=" * 72)
    print("  WORKFORCE PLANNING COMPLETE")
    print("=" * 72)


if __name__ == "__main__":
    main()
