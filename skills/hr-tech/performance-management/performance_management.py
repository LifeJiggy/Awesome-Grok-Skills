"""
performance_management.py — Performance management system: OKR tracking,
360 reviews, goal setting, and succession planning.

Provides data models and engines for structured performance management.
"""

from __future__ import annotations

import statistics
import uuid
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum, IntEnum
from typing import Optional


# ─── Enums ────────────────────────────────────────────────────────────────────

class ObjectiveHealth(Enum):
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    OFF_TRACK = "off_track"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class MetricType(Enum):
    QUANTITATIVE = "quantitative"
    BINARY = "binary"
    MILESTONE = "milestone"
    CUSTOM = "custom"


class ReviewType(Enum):
    ANNUAL = "annual"
    SEMI_ANNUAL = "semi_annual"
    QUARTERLY = "quarterly"
    PERFORMANCE_360 = "performance_360"
    PROBATION = "probation"
    PROJECT_BASED = "project_based"


class ReadinessLevel(Enum):
    NOT_READY = "not_ready"
    READY_1_2_YEARS = "ready_in_1_2_years"
    READY_NEXT_ROLE = "ready_for_next_role"
    READY_NOW = "ready_now"
    OVERQUALIFIED = "overqualified"


class RaterType(Enum):
    MANAGER = "manager"
    PEER = "peer"
    DIRECT_REPORT = "direct_report"
    SELF = "self"
    EXTERNAL = "external"


class CompetencyCategory(Enum):
    TECHNICAL = "technical"
    LEADERSHIP = "leadership"
    COMMUNICATION = "communication"
    COLLABORATION = "collaboration"
    INNOVATION = "innovation"
    EXECUTION = "execution"
    CULTURE = "culture"


class CalibrationStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ESCALATED = "escalated"


class PerformanceRating(Enum):
    EXCEPTIONAL = 5
    EXCEEDS = 4
    MEETS = 3
    DEVELOPING = 2
    UNSATISFACTORY = 1


# ─── Data Classes ─────────────────────────────────────────────────────────────

@dataclass
class KeyResult:
    """A measurable key result within an objective."""
    kr_id: str
    description: str
    metric_type: MetricType
    target_value: float
    current_value: float
    start_value: float = 0.0
    unit: str = ""
    confidence: float = 0.80

    @property
    def progress(self) -> float:
        if self.target_value == self.start_value:
            return 1.0
        raw = (self.current_value - self.start_value) / (self.target_value - self.start_value)
        return min(1.0, max(0.0, raw))

    @property
    def health(self) -> ObjectiveHealth:
        p = self.progress
        if p >= 0.7:
            return ObjectiveHealth.ON_TRACK
        elif p >= 0.4:
            return ObjectiveHealth.AT_RISK
        return ObjectiveHealth.OFF_TRACK


@dataclass
class Objective:
    """An objective with key results."""
    objective_id: str
    owner_id: str
    owner_name: str
    description: str
    key_results: list[KeyResult]
    alignment_parent: Optional[str] = None
    alignment_children: list[str] = field(default_factory=list)
    quarter: str = "Q1-2026"
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def score(self) -> float:
        if not self.key_results:
            return 0.0
        return statistics.mean([kr.progress for kr in self.key_results])

    @property
    def health(self) -> ObjectiveHealth:
        s = self.score
        if s >= 0.7:
            return ObjectiveHealth.ON_TRACK
        elif s >= 0.4:
            return ObjectiveHealth.AT_RISK
        return ObjectiveHealth.OFF_TRACK

    @property
    def completed_krs(self) -> int:
        return sum(1 for kr in self.key_results if kr.progress >= 1.0)

    @property
    def total_krs(self) -> int:
        return len(self.key_results)


@dataclass
class Competency:
    """A competency in the framework."""
    competency_id: str
    name: str
    category: CompetencyCategory
    description: str
    weight: float = 1.0


@dataclass
class CompetencyRating:
    """Rating for a single competency."""
    competency_id: str
    score: float
    evidence: str = ""

    def __post_init__(self) -> None:
        if not 1.0 <= self.score <= 5.0:
            raise ValueError(f"Score must be 1-5, got {self.score}")


@dataclass
class Feedback:
    """A single 360 feedback submission."""
    feedback_id: str
    reviewer_id: str
    reviewer_type: RaterType
    reviewee_id: str
    competency_ratings: list[CompetencyRating]
    strengths: list[str]
    improvements: list[str]
    open_ended: str = ""
    submitted_at: datetime = field(default_factory=datetime.now)


@dataclass
class AggregatedRating:
    """Aggregated 360 feedback for a reviewee."""
    reviewee_id: str
    competency_scores: dict[str, float]
    overall_score: float
    strengths_themes: list[str]
    improvement_themes: list[str]
    narrative_summary: str
    rater_count: int


@dataclass
class ReviewParticipant:
    """Participant in a review cycle."""
    employee_id: str
    employee_name: str
    manager_id: str
    department: str
    reviews_received: list[Feedback]
    self_assessment: Optional[Feedback] = None

    @property
    def avg_competency_score(self) -> float:
        all_scores: list[float] = []
        for fb in self.reviews_received:
            all_scores.extend([cr.score for cr in fb.competency_ratings])
        return statistics.mean(all_scores) if all_scores else 0.0


@dataclass
class ReviewCycle:
    """A complete review cycle."""
    cycle_id: str
    review_type: ReviewType
    name: str
    start_date: date
    end_date: date
    participants: list[ReviewParticipant]
    competencies: list[Competency]
    calibration_status: CalibrationStatus = CalibrationStatus.NOT_STARTED

    @property
    def completion_rate(self) -> float:
        if not self.participants:
            return 0.0
        completed = sum(
            1 for p in self.participants if len(p.reviews_received) >= 3
        )
        return completed / len(self.participants)

    @property
    def avg_score(self) -> float:
        scores = [p.avg_competency_score for p in self.participants if p.reviews_received]
        return statistics.mean(scores) if scores else 0.0


@dataclass
class CapabilityGap:
    """Gap between current and required capability."""
    competency_id: str
    competency_name: str
    current_level: float
    required_level: float
    gap_size: float
    priority: str

    def __post_init__(self) -> None:
        self.gap_size = round(self.required_level - self.current_level, 2)
        if self.gap_size > 1.5:
            self.priority = "critical"
        elif self.gap_size > 0.8:
            self.priority = "high"
        elif self.gap_size > 0.3:
            self.priority = "medium"
        else:
            self.priority = "low"


@dataclass
class DevelopmentAction:
    """A specific development action."""
    action_id: str
    description: str
    action_type: str
    target_date: date
    status: str = "not_started"


@dataclass
class DevelopmentPlan:
    """Development plan for a succession candidate."""
    plan_id: str
    candidate_id: str
    target_role: str
    actions: list[DevelopmentAction]
    estimated_readiness_date: date
    progress_pct: float = 0.0


@dataclass
class SuccessionCandidate:
    """A candidate in the succession pipeline."""
    candidate_id: str
    candidate_name: str
    current_role: str
    target_role: str
    readiness_level: ReadinessLevel
    performance_score: float
    potential_score: float
    aspiration_alignment: float
    capability_gaps: list[CapabilityGap]
    development_plan: Optional[DevelopmentPlan]
    flight_risk: float = 0.0

    @property
    def composite_readiness(self) -> float:
        base = (self.performance_score * 0.3 +
                self.potential_score * 0.3 +
                self.aspiration_alignment * 0.2)
        penalty = self.flight_risk * 0.2
        return round(min(1.0, base - penalty), 4)


@dataclass
class SuccessionPlan:
    """Succession plan for a critical role."""
    plan_id: str
    role_title: str
    role_owner_id: str
    candidates: list[SuccessionCandidate]
    coverage_ratio: float
    created_at: date = field(default_factory=date.today)

    @property
    def ready_now_count(self) -> int:
        return sum(1 for c in self.candidates if c.readiness_level == ReadinessLevel.READY_NOW)

    @property
    def health(self) -> str:
        if self.ready_now_count >= 2:
            return "strong"
        elif self.ready_now_count == 1:
            return "adequate"
        return "at_risk"


@dataclass
class GoalTemplate:
    """Reusable goal template."""
    template_id: str
    title: str
    description: str
    category: str
    level: int
    suggested_krs: list[str]
    suggested_stretch: float = 1.3


@dataclass
class CalibrationAdjustment:
    """A calibration adjustment to a performance rating."""
    employee_id: str
    original_rating: float
    adjusted_rating: float
    adjustment: float
    rationale: str
    adjusted_by: str


# ─── Engines ──────────────────────────────────────────────────────────────────

class OKREngine:
    """OKR tracking, scoring, and alignment engine."""

    def __init__(self) -> None:
        self._objectives: dict[str, Objective] = {}

    def create_objective(self, objective: Objective) -> Objective:
        self._objectives[objective.objective_id] = objective
        return objective

    def score_kr(self, kr: KeyResult) -> float:
        return kr.progress

    def score_objective(self, obj: Objective) -> float:
        return obj.score

    def update_kr(self, kr_id: str, new_value: float) -> Optional[KeyResult]:
        for obj in self._objectives.values():
            for kr in obj.key_results:
                if kr.kr_id == kr_id:
                    kr.current_value = new_value
                    return kr
        return None

    def alignment_score(self, parent_id: str, child_ids: list[str]) -> float:
        parent = self._objectives.get(parent_id)
        if not parent:
            return 0.0
        children = [self._objectives[cid] for cid in child_ids if cid in self._objectives]
        if not children:
            return 0.0
        child_scores = [c.score for c in children]
        return statistics.mean(child_scores)

    def health_report(self, owner_id: Optional[str] = None) -> dict[str, dict]:
        report: dict[str, dict] = {}
        for oid, obj in self._objectives.items():
            if owner_id and obj.owner_id != owner_id:
                continue
            report[oid] = {
                "description": obj.description,
                "score": obj.score,
                "health": obj.health.value,
                "kr_progress": {kr.kr_id: kr.progress for kr in obj.key_results},
                "completed": obj.completed_krs,
                "total": obj.total_krs,
            }
        return report

    def generate_stretch_targets(self, obj: Objective, multiplier: float = 1.3) -> list[KeyResult]:
        stretch_krs: list[KeyResult] = []
        for kr in obj.key_results:
            stretch_krs.append(KeyResult(
                kr_id=f"{kr.kr_id}-stretch",
                description=f"[STRETCH] {kr.description}",
                metric_type=kr.metric_type,
                target_value=round(kr.target_value * multiplier, 2),
                current_value=kr.current_value,
                start_value=kr.start_value,
                unit=kr.unit,
            ))
        return stretch_krs


class ReviewEngine:
    """360-degree review aggregation and calibration engine."""

    RATER_WEIGHTS: dict[RaterType, float] = {
        RaterType.MANAGER: 0.35,
        RaterType.PEER: 0.25,
        RaterType.DIRECT_REPORT: 0.25,
        RaterType.SELF: 0.15,
    }

    def __init__(self, min_raters: int = 3) -> None:
        self.min_raters = min_raters

    def aggregate_reviews(
        self, reviewee_id: str, reviews: list[Feedback]
    ) -> AggregatedRating:
        if not reviews:
            return AggregatedRating(
                reviewee_id=reviewee_id, competency_scores={},
                overall_score=0.0, strengths_themes=[], improvement_themes=[],
                narrative_summary="No reviews submitted", rater_count=0,
            )

        weighted_scores: dict[str, list[float]] = {}
        for review in reviews:
            weight = self.RATER_WEIGHTS.get(review.reviewer_type, 0.2)
            for cr in review.competency_ratings:
                weighted_scores.setdefault(cr.competency_id, []).append(cr.score * weight)

        competency_avgs: dict[str, float] = {}
        for cid, scores in weighted_scores.items():
            total_weight = sum(
                self.RATER_WEIGHTS.get(r.reviewer_type, 0.2)
                for r in reviews if any(cr.competency_id == cid for cr in r.competency_ratings)
            )
            competency_avgs[cid] = round(sum(scores) / total_weight if total_weight > 0 else 0, 3)

        overall = statistics.mean(competency_avgs.values()) if competency_avgs else 0.0

        all_strengths = [s for r in reviews for s in r.strengths]
        all_improvements = [i for r in reviews for i in r.improvements]

        strength_freq: dict[str, int] = {}
        for s in all_strengths:
            strength_freq[s.lower()] = strength_freq.get(s.lower(), 0) + 1
        improvement_freq: dict[str, int] = {}
        for i in all_improvements:
            improvement_freq[i.lower()] = improvement_freq.get(i.lower(), 0) + 1

        top_strengths = sorted(strength_freq, key=strength_freq.get, reverse=True)[:5]
        top_improvements = sorted(improvement_freq, key=improvement_freq.get, reverse=True)[:5]

        return AggregatedRating(
            reviewee_id=reviewee_id,
            competency_scores=competency_avgs,
            overall_score=round(overall, 3),
            strengths_themes=top_strengths,
            improvement_themes=top_improvements,
            narrative_summary=self._generate_narrative(overall, top_strengths, top_improvements),
            rater_count=len(reviews),
        )

    def _generate_narrative(
        self, overall: float, strengths: list[str], improvements: list[str]
    ) -> str:
        if overall >= 4.0:
            level = "exceptional"
        elif overall >= 3.0:
            level = "solid"
        elif overall >= 2.0:
            level = "developing"
        else:
            level = "needs improvement"
        strength_text = ", ".join(strengths[:3]) if strengths else "none identified"
        return f"Overall {level} performance ({overall:.2f}/5.0). Key strengths: {strength_text}."

    def calibration_normalize(
        self,
        participants: list[ReviewParticipant],
        target_mean: float = 3.5,
        max_adjustment: float = 0.15,
    ) -> list[CalibrationAdjustment]:
        if not participants:
            return []
        current_mean = statistics.mean(
            [p.avg_competency_score for p in participants if p.reviews_received]
        )
        adjustments: list[CalibrationAdjustment] = []
        for p in participants:
            if not p.reviews_received:
                continue
            raw = p.avg_competency_score
            shift = (target_mean - current_mean)
            shift = max(-max_adjustment, min(max_adjustment, shift))
            adjusted = round(raw + shift, 3)
            adjustments.append(CalibrationAdjustment(
                employee_id=p.employee_id,
                original_rating=round(raw, 3),
                adjusted_rating=adjusted,
                adjustment=round(shift, 4),
                rationale=f"Normalization shift from {raw:.2f} to {adjusted:.2f} (mean target {target_mean})",
                adjusted_by="system",
            ))
        return adjustments


class GoalTemplateEngine:
    """Goal template library and smart goal generation."""

    DEFAULT_TEMPLATES: list[GoalTemplate] = [
        GoalTemplate(
            template_id="GT001", title="Improve Technical Skills",
            description="Complete advanced training in core technical area",
            category="technical", level=3,
            suggested_krs=["Complete X certification", "Deliver Y project", "Mentor Z engineers"],
        ),
        GoalTemplate(
            template_id="GT002", title="Drive Business Growth",
            description="Contribute to revenue or growth targets",
            category="business", level=5,
            suggested_krs=["Achieve X revenue target", "Close Y strategic deals", "Launch Z initiative"],
        ),
        GoalTemplate(
            template_id="GT003", title="Build Team Capability",
            description="Develop team skills and improve team performance",
            category="leadership", level=4,
            suggested_krs=["Train X team members", "Improve team engagement by Y%", "Reduce attrition to Z%"],
        ),
    ]

    def __init__(self) -> None:
        self.templates = list(self.DEFAULT_TEMPLATES)

    def get_templates(self, category: Optional[str] = None, level: Optional[int] = None) -> list[GoalTemplate]:
        results = self.templates
        if category:
            results = [t for t in results if t.category == category]
        if level is not None:
            results = [t for t in results if t.level == level]
        return results

    def create_goal_from_template(
        self, template: GoalTemplate, owner_id: str, quarter: str
    ) -> Objective:
        key_results = [
            KeyResult(
                kr_id=str(uuid.uuid4())[:8],
                description=kr,
                metric_type=MetricType.MILESTONE,
                target_value=100.0,
                current_value=0.0,
                start_value=0.0,
            )
            for kr in template.suggested_krs
        ]
        return Objective(
            objective_id=str(uuid.uuid4())[:8],
            owner_id=owner_id,
            owner_name="",
            description=template.description,
            key_results=key_results,
            quarter=quarter,
        )

    def validate_smart(self, goal_text: str) -> dict[str, bool]:
        checks = {
            "specific": len(goal_text.split()) >= 5,
            "measurable": any(c.isdigit() for c in goal_text),
            "achievable": len(goal_text) <= 200,
            "relevant": True,
            "time_bound": any(
                kw in goal_text.lower()
                for kw in ["quarter", "month", "year", "q1", "q2", "q3", "q4", "by"]
            ),
        }
        return checks


class SuccessionEngine:
    """Succession planning and talent pipeline management."""

    def __init__(self, readiness_threshold: float = 0.70) -> None:
        self.readiness_threshold = readiness_threshold

    def assess_readiness(
        self, candidate: SuccessionCandidate
    ) -> ReadinessLevel:
        score = candidate.composite_readiness
        if score >= 0.85:
            return ReadinessLevel.READY_NOW
        elif score >= 0.65:
            return ReadinessLevel.READY_NEXT_ROLE
        elif score >= 0.45:
            return ReadinessLevel.READY_1_2_YEARS
        return ReadinessLevel.NOT_READY

    def identify_gaps(
        self, candidate: SuccessionCandidate, target_competencies: list[Competency]
    ) -> list[CapabilityGap]:
        gaps: list[CapabilityGap] = []
        for comp in target_competencies:
            current = candidate.performance_score
            required = 4.0
            gap = CapabilityGap(
                competency_id=comp.competency_id,
                competency_name=comp.name,
                current_level=current,
                required_level=required,
                gap_size=0.0,
                priority="",
            )
            if gap.gap_size > 0.3:
                gaps.append(gap)
        return sorted(gaps, key=lambda g: g.gap_size, reverse=True)

    def plan_coverage(self, succession_plans: list[SuccessionPlan]) -> dict[str, str]:
        coverage: dict[str, str] = {}
        for plan in succession_plans:
            coverage[plan.role_title] = plan.health
        return coverage

    def flight_risk_overlay(
        self,
        candidates: list[SuccessionCandidate],
        attrition_scores: dict[str, float],
    ) -> list[dict]:
        overlay: list[dict] = []
        for c in candidates:
            risk = attrition_scores.get(c.candidate_id, 0.0)
            c.flight_risk = risk
            overlay.append({
                "candidate": c.candidate_name,
                "target_role": c.target_role,
                "readiness": c.readiness_level.value,
                "flight_risk": f"{risk:.0%}",
                "composite": c.composite_readiness,
                "concern": "HIGH" if risk > 0.6 and c.readiness_level == ReadinessLevel.READY_NOW else "OK",
            })
        return overlay


# ─── Main Demo ────────────────────────────────────────────────────────────────

def main() -> None:
    """Demonstrate the performance management system end-to-end."""
    print("=" * 72)
    print("  PERFORMANCE MANAGEMENT SYSTEM DEMO")
    print("=" * 72)

    # 1. OKR Tracking
    print("\n[1] OKR TRACKING & SCORING")
    print("-" * 40)
    engine = OKREngine()

    eng_obj = Objective(
        objective_id="OBJ-001", owner_id="E001", owner_name="Alice Chen",
        description="Deliver high-quality platform features on time",
        key_results=[
            KeyResult("KR1", "Reduce bug escape rate to <2%", MetricType.QUANTITATIVE, 2.0, 2.8, 5.0, "%"),
            KeyResult("KR2", "Achieve 95% sprint velocity consistency", MetricType.QUANTITATIVE, 95.0, 88.0, 70.0, "%"),
            KeyResult("KR3", "Complete 3 architectural RFCs", MetricType.MILESTONE, 3.0, 2.0, 0.0),
        ],
        quarter="Q3-2026",
    )
    engine.create_objective(eng_obj)

    sales_obj = Objective(
        objective_id="OBJ-002", owner_id="E002", owner_name="Bob Williams",
        description="Drive revenue growth through new market penetration",
        key_results=[
            KeyResult("KR1", "Close $2M in new ARR", MetricType.QUANTITATIVE, 2000000, 1400000, 0, "$"),
            KeyResult("KR2", "Generate 50 qualified leads per month", MetricType.QUANTITATIVE, 50, 42, 20),
            KeyResult("KR3", "Achieve 30% lead-to-close conversion", MetricType.QUANTITATIVE, 0.30, 0.25, 0.15),
        ],
        quarter="Q3-2026",
    )
    engine.create_objective(sales_obj)

    report = engine.health_report()
    for oid, info in report.items():
        print(f"\n  {info['description']}")
        print(f"    Score: {info['score']:.2%} [{info['health']}]")
        print(f"    KRs:   {info['completed']}/{info['total']} completed")
        for krid, prog in info['kr_progress'].items():
            print(f"      {krid}: {prog:.0%}")

    stretch = engine.generate_stretch_targets(eng_obj, multiplier=1.3)
    print(f"\n  Stretch targets for OBJ-001:")
    for skr in stretch:
        print(f"    - {skr.description}: target={skr.target_value}")

    # 2. 360-Degree Review
    print("\n[2] 360-DEGREE REVIEW")
    print("-" * 40)
    review_engine = ReviewEngine(min_raters=3)
    competencies = [
        Competency("C1", "Technical Excellence", CompetencyCategory.TECHNICAL, "Deep technical skill", 1.0),
        Competency("C2", "Leadership", CompetencyCategory.LEADERSHIP, "Leading teams", 1.0),
        Competency("C3", "Communication", CompetencyCategory.COMMUNICATION, "Clear communication", 1.0),
    ]

    reviews = [
        Feedback("F001", "mgr-001", RaterType.MANAGER, "E001",
                 [CompetencyRating("C1", 4.5), CompetencyRating("C2", 4.0), CompetencyRating("C3", 3.8)],
                 ["Strong technical skills", "Great mentor"], ["Could improve delegation"]),
        Feedback("F002", "peer-001", RaterType.PEER, "E001",
                 [CompetencyRating("C1", 4.2), CompetencyRating("C2", 3.5), CompetencyRating("C3", 4.0)],
                 ["Collaborative", "Knowledge sharing"], ["Sometimes too detailed"]),
        Feedback("F003", "report-001", RaterType.DIRECT_REPORT, "E001",
                 [CompetencyRating("C1", 4.0), CompetencyRating("C2", 4.3), CompetencyRating("C3", 4.1)],
                 ["Supportive manager", "Clear direction"], ["Needs more strategic vision"]),
        Feedback("F004", "self-001", RaterType.SELF, "E001",
                 [CompetencyRating("C1", 3.8), CompetencyRating("C2", 3.5), CompetencyRating("C3", 3.5)],
                 ["Technical depth", "Process oriented"], ["Public speaking", "Delegation"]),
    ]

    aggregated = review_engine.aggregate_reviews("E001", reviews)
    print(f"\n  Reviewee: E001")
    print(f"  Raters:   {aggregated.rater_count}")
    print(f"  Overall:  {aggregated.overall_score:.3f}/5.0")
    print(f"  Competency Scores:")
    for cid, score in aggregated.competency_scores.items():
        print(f"    {cid}: {score:.3f}")
    print(f"  Strengths:     {', '.join(aggregated.strengths_themes)}")
    print(f"  Improvements:  {', '.join(aggregated.improvement_themes)}")
    print(f"  Narrative: {aggregated.narrative_summary}")

    # Calibration
    participants = [
        ReviewParticipant("E001", "Alice Chen", "mgr-001", "Engineering", reviews),
        ReviewParticipant("E002", "Bob Williams", "mgr-002", "Sales", []),
    ]
    adjustments = review_engine.calibration_normalize(participants, target_mean=3.5)
    print(f"\n  Calibration Adjustments:")
    for adj in adjustments:
        print(f"    {adj.employee_id}: {adj.original_rating:.3f} -> {adj.adjusted_rating:.3f} "
              f"(shift={adj.adjustment:+.4f})")

    # 3. Goal Templates
    print("\n[3] GOAL TEMPLATES & SMART VALIDATION")
    print("-" * 40)
    template_engine = GoalTemplateEngine()
    templates = template_engine.get_templates(category="technical")
    for t in templates:
        print(f"  [{t.template_id}] {t.title}")
        print(f"    Category: {t.category}, Level: {t.level}")
        print(f"    Suggested KRs: {', '.join(t.suggested_krs)}")

    goal_text = "Reduce system downtime to below 0.1% by end of Q4 through infrastructure improvements"
    smart = template_engine.validate_smart(goal_text)
    print(f"\n  SMART Validation: '{goal_text[:60]}...'")
    for check, passed in smart.items():
        status = "PASS" if passed else "FAIL"
        print(f"    {check:12s}: [{status}]")

    # 4. Succession Planning
    print("\n[4] SUCCESSION PLANNING")
    print("-" * 40)
    succession_engine = SuccessionEngine(readiness_threshold=0.70)

    candidates = [
        SuccessionCandidate(
            candidate_id="E001", candidate_name="Alice Chen",
            current_role="Senior Engineer", target_role="Engineering Manager",
            readiness_level=ReadinessLevel.NOT_READY,
            performance_score=4.2, potential_score=4.0, aspiration_alignment=0.9,
            capability_gaps=[], development_plan=None,
        ),
        SuccessionCandidate(
            candidate_id="E004", candidate_name="Diana Johnson",
            current_role="Product Manager", target_role="VP Product",
            readiness_level=ReadinessLevel.NOT_READY,
            performance_score=4.0, potential_score=3.8, aspiration_alignment=0.85,
            capability_gaps=[], development_plan=None,
        ),
        SuccessionCandidate(
            candidate_id="E007", candidate_name="George Brown",
            current_role="VP Operations", target_role="COO",
            readiness_level=ReadinessLevel.NOT_READY,
            performance_score=4.5, potential_score=4.7, aspiration_alignment=0.95,
            capability_gaps=[], development_plan=None,
        ),
    ]

    for c in candidates:
        c.readiness_level = succession_engine.assess_readiness(c)
        print(f"\n  {c.candidate_name}")
        print(f"    Current:      {c.current_role}")
        print(f"    Target:       {c.target_role}")
        print(f"    Readiness:    {c.readiness_level.value}")
        print(f"    Composite:    {c.composite_readiness:.2%}")
        print(f"    Performance:  {c.performance_score:.1f}")
        print(f"    Potential:    {c.potential_score:.1f}")
        print(f"    Aspiration:   {c.aspiration_alignment:.0%}")

    plan = SuccessionPlan(
        plan_id="SP-001", role_title="Engineering Manager",
        role_owner_id="E999", candidates=candidates,
        coverage_ratio=0.5,
    )
    print(f"\n  Succession Plan: {plan.role_title}")
    print(f"    Ready Now:    {plan.ready_now_count}")
    print(f"    Health:       {plan.health}")
    print(f"    Coverage:     {plan.coverage_ratio:.0%}")

    print("\n" + "=" * 72)
    print("  PERFORMANCE MANAGEMENT COMPLETE")
    print("=" * 72)


if __name__ == "__main__":
    main()
