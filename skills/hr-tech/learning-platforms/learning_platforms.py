"""
learning_platforms.py — Learning platform system: LMS, adaptive learning,
skill gap analysis, and compliance training management.

Provides data models and engines for enterprise learning and development.
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

class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class CourseCategory(Enum):
    TECHNICAL = "technical"
    SOFT_SKILLS = "soft_skills"
    COMPLIANCE = "compliance"
    LEADERSHIP = "leadership"
    ONBOARDING = "onboarding"
    SAFETY = "safety"
    DIVERSITY = "diversity"


class ContentType(Enum):
    VIDEO = "video"
    ARTICLE = "article"
    INTERACTIVE = "interactive"
    QUIZ = "quiz"
    LAB = "lab"
    WORKSHOP = "workshop"


class EnrollmentStatus(Enum):
    NOT_ENROLLED = "not_enrolled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DROPPED = "dropped"
    EXPIRED = "expired"


class ComplianceStatus(Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    OVERDUE = "overdue"
    EXEMPT = "exempt"
    PENDING = "pending"


class MasteryLevel(Enum):
    NOVICE = "novice"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class AssessmentResult(Enum):
    CORRECT = "correct"
    INCORRECT = "incorrect"
    PARTIAL = "partial"


# ─── Data Classes ─────────────────────────────────────────────────────────────

@dataclass
class SkillEntry:
    """A skill in a learner's inventory."""
    skill_name: str
    level: MasteryLevel
    verified: bool = False
    last_assessed: Optional[date] = None
    confidence: float = 0.5


@dataclass
class Module:
    """A single learning module within a course."""
    module_id: str
    title: str
    content_type: ContentType
    estimated_minutes: int
    difficulty: DifficultyLevel
    skill_tags: list[str]
    order: int = 0

    @property
    def estimated_hours(self) -> float:
        return round(self.estimated_minutes / 60, 2)


@dataclass
class Course:
    """A complete course with modules."""
    course_id: str
    title: str
    description: str
    category: CourseCategory
    modules: list[Module]
    prerequisites: list[str]
    difficulty: DifficultyLevel
    compliance_tags: list[str]
    created_at: date = field(default_factory=date.today)

    @property
    def total_hours(self) -> float:
        return round(sum(m.estimated_minutes for m in self.modules) / 60, 2)

    @property
    def module_count(self) -> int:
        return len(self.modules)

    def get_module(self, module_id: str) -> Optional[Module]:
        for m in self.modules:
            if m.module_id == module_id:
                return m
        return None


@dataclass
class ModuleProgress:
    """Progress on a single module."""
    module_id: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    time_spent_minutes: float = 0.0
    score: Optional[float] = None
    attempts: int = 0

    @property
    def is_complete(self) -> bool:
        return self.completed_at is not None


@dataclass
class Enrollment:
    """A learner's enrollment in a course."""
    enrollment_id: str
    learner_id: str
    course_id: str
    enrolled_at: datetime
    status: EnrollmentStatus
    module_progress: list[ModuleProgress] = field(default_factory=list)
    target_completion: Optional[date] = None

    @property
    def completion_pct(self) -> float:
        if not self.module_progress:
            return 0.0
        completed = sum(1 for mp in self.module_progress if mp.is_complete)
        return completed / len(self.module_progress)

    @property
    def is_overdue(self) -> bool:
        if not self.target_completion:
            return False
        return date.today() > self.target_completion and self.status != EnrollmentStatus.COMPLETED


@dataclass
class ComplianceRequirement:
    """A compliance training requirement."""
    requirement_id: str
    regulation: str
    description: str
    course_id: str
    validity_months: int
    roles: list[str]
    frequency_months: int = 12


@dataclass
class ComplianceRecord:
    """A learner's compliance record for a requirement."""
    record_id: str
    learner_id: str
    requirement_id: str
    status: ComplianceStatus
    due_date: date
    completion_date: Optional[date] = None
    certificate_id: Optional[str] = None

    @property
    def is_overdue(self) -> bool:
        return self.status == ComplianceStatus.OVERDUE or (
            self.status == ComplianceStatus.PENDING and date.today() > self.due_date
        )


@dataclass
class MasteryEstimate:
    """Bayesian knowledge tracing estimate for a concept."""
    concept: str
    mastery_probability: float
    last_update: datetime
    observations: int
    slip_rate: float = 0.1
    guess_rate: float = 0.2

    @property
    def mastery_level(self) -> MasteryLevel:
        p = self.mastery_probability
        if p >= 0.90:
            return MasteryLevel.EXPERT
        elif p >= 0.75:
            return MasteryLevel.ADVANCED
        elif p >= 0.50:
            return MasteryLevel.INTERMEDIATE
        elif p >= 0.25:
            return MasteryLevel.BEGINNER
        return MasteryLevel.NOVICE

    def update(self, correct: bool) -> None:
        """Update mastery using Bayesian Knowledge Tracing."""
        if correct:
            self.mastery_probability = (
                self.mastery_probability * (1.0 - self.slip_rate)
            ) / (
                self.mastery_probability * (1.0 - self.slip_rate) +
                (1.0 - self.mastery_probability) * self.guess_rate
            )
        else:
            self.mastery_probability = (
                self.mastery_probability * self.slip_rate
            ) / (
                self.mastery_probability * self.slip_rate +
                (1.0 - self.mastery_probability) * (1.0 - self.guess_rate)
            )
        self.mastery_probability = max(0.01, min(0.99, self.mastery_probability))
        self.observations += 1
        self.last_update = datetime.now()


@dataclass
class RecommendedModule:
    """A module recommended by the adaptive engine."""
    module: Module
    priority_score: float
    rationale: str
    estimated_time_minutes: int


@dataclass
class LearningPath:
    """A personalized learning path for a learner."""
    path_id: str
    learner_id: str
    modules: list[RecommendedModule]
    rationale: str
    estimated_completion: date
    priority_score: float

    @property
    def total_hours(self) -> float:
        return round(sum(rm.estimated_time_minutes for rm in self.modules) / 60, 2)


@dataclass
class SkillGap:
    """A gap between current and required skill level."""
    skill_name: str
    current_level: MasteryLevel
    required_level: MasteryLevel
    gap_severity: float
    business_impact: str
    recommended_courses: list[str]

    def __post_init__(self) -> None:
        levels = list(MasteryLevel)
        curr_idx = levels.index(self.current_level)
        req_idx = levels.index(self.required_level)
        self.gap_severity = max(0.0, (req_idx - curr_idx) / len(levels))


@dataclass
class Learner:
    """A learner profile."""
    learner_id: str
    name: str
    role: str
    department: str
    level: int
    skill_inventory: list[SkillEntry]
    enrollments: list[Enrollment]
    completions: list[str]
    compliance_records: list[ComplianceRecord]

    @property
    def active_enrollments(self) -> int:
        return sum(1 for e in self.enrollments if e.status == EnrollmentStatus.IN_PROGRESS)

    @property
    def total_courses_completed(self) -> int:
        return len(self.completions)

    def skill_level(self, skill_name: str) -> MasteryLevel:
        for s in self.skill_inventory:
            if s.skill_name.lower() == skill_name.lower():
                return s.level
        return MasteryLevel.NOVICE


@dataclass
class ComplianceReport:
    """Compliance status report for a learner or department."""
    report_date: date
    total_requirements: int
    compliant: int
    non_compliant: int
    overdue: list[ComplianceRecord]
    compliance_rate: float

    def __post_init__(self) -> None:
        if self.total_requirements > 0:
            self.compliance_rate = round(self.compliant / self.total_requirements, 4)


@dataclass
class LearningROI:
    """Return on investment metrics for learning programs."""
    program_name: str
    total_cost: float
    total_learners: int
    completion_rate: float
    avg_skill_improvement: float
    estimated_productivity_gain: float

    @property
    def cost_per_learner(self) -> float:
        return round(self.total_cost / max(1, self.total_learners), 2)

    @property
    def roi_ratio(self) -> float:
        if self.total_cost == 0:
            return 0.0
        return round(self.estimated_productivity_gain / self.total_cost, 2)


# ─── Engines ──────────────────────────────────────────────────────────────────

class AdaptiveLearningEngine:
    """Adaptive learning path engine with Bayesian knowledge tracing."""

    def __init__(
        self,
        mastery_threshold: float = 0.80,
        spaced_repetition_days: int = 7,
    ) -> None:
        self.mastery_threshold = mastery_threshold
        self.spaced_repetition_days = spaced_repetition_days
        self._mastery: dict[str, dict[str, MasteryEstimate]] = {}

    def assess_baseline(self, learner_id: str, skills: list[str]) -> dict[str, MasteryEstimate]:
        estimates: dict[str, MasteryEstimate] = {}
        for skill in skills:
            estimates[skill] = MasteryEstimate(
                concept=skill,
                mastery_probability=0.3,
                last_update=datetime.now(),
                observations=0,
            )
        self._mastery[learner_id] = estimates
        return estimates

    def update_mastery(self, learner_id: str, concept: str, correct: bool) -> MasteryEstimate:
        if learner_id not in self._mastery:
            self._mastery[learner_id] = {}
        if concept not in self._mastery[learner_id]:
            self._mastery[learner_id][concept] = MasteryEstimate(
                concept=concept, mastery_probability=0.3,
                last_update=datetime.now(), observations=0,
            )
        estimate = self._mastery[learner_id][concept]
        estimate.update(correct)
        return estimate

    def get_mastery(self, learner_id: str, concept: str) -> MasteryEstimate:
        if learner_id in self._mastery and concept in self._mastery[learner_id]:
            return self._mastery[learner_id][concept]
        return MasteryEstimate(
            concept=concept, mastery_probability=0.3,
            last_update=datetime.now(), observations=0,
        )

    def identify_gaps(self, learner_id: str, course: Course) -> list[Module]:
        gaps: list[Module] = []
        for module in course.modules:
            for tag in module.skill_tags:
                mastery = self.get_mastery(learner_id, tag)
                if mastery.mastery_probability < self.mastery_threshold:
                    gaps.append(module)
                    break
        return gaps

    def recommend_modules(
        self, learner_id: str, course: Course, max_modules: int = 5
    ) -> list[RecommendedModule]:
        gaps = self.identify_gaps(learner_id, course)
        recommendations: list[RecommendedModule] = []
        for module in sorted(gaps, key=lambda m: m.difficulty.value):
            avg_mastery = statistics.mean([
                self.get_mastery(learner_id, tag).mastery_probability
                for tag in module.skill_tags
            ]) if module.skill_tags else 0.3
            priority = 1.0 - avg_mastery
            recommendations.append(RecommendedModule(
                module=module,
                priority_score=round(priority, 3),
                rationale=f"Mastery at {avg_mastery:.0%} — below {self.mastery_threshold:.0%} threshold",
                estimated_time_minutes=module.estimated_minutes,
            ))
            if len(recommendations) >= max_modules:
                break
        return recommendations

    def spaced_repetition_schedule(
        self, learner_id: str, concepts: list[str]
    ) -> list[dict[str, object]]:
        schedule: list[dict[str, object]] = []
        for concept in concepts:
            mastery = self.get_mastery(learner_id, concept)
            if mastery.mastery_probability < 0.5:
                interval = max(1, self.spaced_repetition_days // 2)
            elif mastery.mastery_probability < 0.8:
                interval = self.spaced_repetition_days
            else:
                interval = self.spaced_repetition_days * 2
            schedule.append({
                "concept": concept,
                "mastery": mastery.mastery_probability,
                "next_review_days": interval,
                "mastery_level": mastery.mastery_level.value,
            })
        return schedule


class SkillGapAnalyzer:
    """Skill gap analysis and learning path generation."""

    ROLE_REQUIREMENTS: dict[str, dict[str, MasteryLevel]] = {
        "engineer": {
            "python": MasteryLevel.ADVANCED,
            "sql": MasteryLevel.INTERMEDIATE,
            "system_design": MasteryLevel.ADVANCED,
            "communication": MasteryLevel.INTERMEDIATE,
            "testing": MasteryLevel.ADVANCED,
        },
        "manager": {
            "leadership": MasteryLevel.ADVANCED,
            "communication": MasteryLevel.EXPERT,
            "project_management": MasteryLevel.ADVANCED,
            "budgeting": MasteryLevel.INTERMEDIATE,
            "conflict_resolution": MasteryLevel.ADVANCED,
        },
        "analyst": {
            "sql": MasteryLevel.ADVANCED,
            "statistics": MasteryLevel.ADVANCED,
            "visualization": MasteryLevel.INTERMEDIATE,
            "python": MasteryLevel.INTERMEDIATE,
            "communication": MasteryLevel.INTERMEDIATE,
        },
    }

    def __init__(self) -> None:
        self.course_catalog: dict[str, Course] = {}

    def register_course(self, course: Course) -> None:
        self.course_catalog[course.course_id] = course

    def analyze_gaps(
        self, learner: Learner, role_requirements: Optional[dict[str, MasteryLevel]] = None
    ) -> list[SkillGap]:
        reqs = role_requirements or self.ROLE_REQUIREMENTS.get(learner.role.lower(), {})
        gaps: list[SkillGap] = []
        for skill, required_level in reqs.items():
            current = learner.skill_level(skill)
            levels = list(MasteryLevel)
            if levels.index(current) < levels.index(required_level):
                recommended = self._find_courses_for_skill(skill, required_level)
                gaps.append(SkillGap(
                    skill_name=skill,
                    current_level=current,
                    required_level=required_level,
                    gap_severity=0.0,
                    business_impact=self._assess_impact(skill, learner.role),
                    recommended_courses=recommended,
                ))
        return sorted(gaps, key=lambda g: g.gap_severity, reverse=True)

    def _find_courses_for_skill(self, skill: str, level: MasteryLevel) -> list[str]:
        courses: list[str] = []
        for cid, course in self.course_catalog.items():
            for m in course.modules:
                if skill.lower() in [t.lower() for t in m.skill_tags]:
                    courses.append(cid)
                    break
        return courses

    def _assess_impact(self, skill: str, role: str) -> str:
        critical_skills = {"python", "sql", "leadership", "system_design"}
        if skill.lower() in critical_skills:
            return "high"
        return "medium"

    def generate_learning_path(
        self, learner: Learner, gaps: list[SkillGap], max_courses: int = 3
    ) -> LearningPath:
        recommended_modules: list[RecommendedModule] = []
        for gap in gaps:
            for cid in gap.recommended_courses[:1]:
                course = self.course_catalog.get(cid)
                if course:
                    for m in course.modules[:2]:
                        recommended_modules.append(RecommendedModule(
                            module=m,
                            priority_score=gap.gap_severity,
                            rationale=f"Close gap in {gap.skill_name}",
                            estimated_time_minutes=m.estimated_minutes,
                        ))
            if len(recommended_modules) >= max_courses * 3:
                break

        total_minutes = sum(rm.estimated_time_minutes for rm in recommended_modules)
        est_completion = date.today() + timedelta(days=max(7, total_minutes // 60))

        return LearningPath(
            path_id=str(uuid.uuid4())[:8],
            learner_id=learner.learner_id,
            modules=recommended_modules[:max_courses * 3],
            rationale=f"Address {len(gaps)} skill gaps for {learner.role} role",
            estimated_completion=est_completion,
            priority_score=statistics.mean([rm.priority_score for rm in recommended_modules]) if recommended_modules else 0.0,
        )


class ComplianceTracker:
    """Compliance training tracking and escalation engine."""

    def __init__(self, escalation_days: int = 7) -> None:
        self.escalation_days = escalation_days
        self._requirements: list[ComplianceRequirement] = []

    def register_requirement(self, req: ComplianceRequirement) -> None:
        self._requirements.append(req)

    def get_requirements_for_role(self, role: str) -> list[ComplianceRequirement]:
        return [r for r in self._requirements if role.lower() in [rl.lower() for rl in r.roles]]

    def check_compliance(self, learner: Learner) -> ComplianceReport:
        requirements = self.get_requirements_for_role(learner.role)
        overdue: list[ComplianceRecord] = []
        compliant_count = 0

        for req in requirements:
            record = self._find_record(learner, req.requirement_id)
            if record and record.status == ComplianceStatus.COMPLIANT:
                compliant_count += 1
            elif record and record.is_overdue:
                overdue.append(record)
            else:
                if record is None:
                    overdue.append(ComplianceRecord(
                        record_id=str(uuid.uuid4())[:8],
                        learner_id=learner.learner_id,
                        requirement_id=req.requirement_id,
                        status=ComplianceStatus.OVERDUE,
                        due_date=date.today(),
                    ))

        total = len(requirements)
        return ComplianceReport(
            report_date=date.today(),
            total_requirements=total,
            compliant=compliant_count,
            non_compliant=total - compliant_count,
            overdue=overdue,
            compliance_rate=0.0,
        )

    def _find_record(
        self, learner: Learner, requirement_id: str
    ) -> Optional[ComplianceRecord]:
        for record in learner.compliance_records:
            if record.requirement_id == requirement_id:
                return record
        return None

    def assign_training(
        self, learner: Learner, course_id: str, due_date: date
    ) -> Enrollment:
        return Enrollment(
            enrollment_id=str(uuid.uuid4())[:8],
            learner_id=learner.learner_id,
            course_id=course_id,
            enrolled_at=datetime.now(),
            status=EnrollmentStatus.IN_PROGRESS,
            target_completion=due_date,
        )

    def generate_audit_trail(
        self, learner: Learner
    ) -> list[dict[str, object]]:
        trail: list[dict[str, object]] = []
        for record in learner.compliance_records:
            trail.append({
                "record_id": record.record_id,
                "requirement_id": record.requirement_id,
                "status": record.status.value,
                "due_date": record.due_date.isoformat(),
                "completion_date": record.completion_date.isoformat() if record.completion_date else None,
                "certificate_id": record.certificate_id,
            })
        return trail


class CourseManager:
    """Course catalog and enrollment management."""

    def __init__(self) -> None:
        self.courses: dict[str, Course] = {}
        self.enrollments: dict[str, Enrollment] = {}

    def add_course(self, course: Course) -> None:
        self.courses[course.course_id] = course

    def get_course(self, course_id: str) -> Optional[Course]:
        return self.courses.get(course_id)

    def enroll(self, learner_id: str, course_id: str) -> Optional[Enrollment]:
        course = self.courses.get(course_id)
        if not course:
            return None
        for preq_id in course.prerequisites:
            if not self._has_completed(learner_id, preq_id):
                return None

        enrollment = Enrollment(
            enrollment_id=str(uuid.uuid4())[:8],
            learner_id=learner_id,
            course_id=course_id,
            enrolled_at=datetime.now(),
            status=EnrollmentStatus.IN_PROGRESS,
            module_progress=[
                ModuleProgress(module_id=m.module_id)
                for m in sorted(course.modules, key=lambda m: m.order)
            ],
        )
        self.enrollments[enrollment.enrollment_id] = enrollment
        return enrollment

    def _has_completed(self, learner_id: str, course_id: str) -> bool:
        for e in self.enrollments.values():
            if e.learner_id == learner_id and e.course_id == course_id:
                if e.status == EnrollmentStatus.COMPLETED:
                    return True
        return False

    def complete_module(self, enrollment_id: str, module_id: str, score: float) -> bool:
        enrollment = self.enrollments.get(enrollment_id)
        if not enrollment:
            return False
        for mp in enrollment.module_progress:
            if mp.module_id == module_id:
                mp.completed_at = datetime.now()
                mp.score = score
                mp.attempts += 1
                if all(m.is_complete for m in enrollment.module_progress):
                    enrollment.status = EnrollmentStatus.COMPLETED
                return True
        return False


# ─── Main Demo ────────────────────────────────────────────────────────────────

def main() -> None:
    """Demonstrate the learning platform system end-to-end."""
    print("=" * 72)
    print("  LEARNING PLATFORMS DEMO")
    print("=" * 72)

    # 1. Course Catalog & Enrollment
    print("\n[1] COURSE CATALOG & ENROLLMENT")
    print("-" * 40)
    course_manager = CourseManager()

    py_course = Course(
        course_id="CRS-001", title="Advanced Python",
        description="Master advanced Python patterns and performance",
        category=CourseCategory.TECHNICAL,
        modules=[
            Module("M1", "Decorators & Metaclasses", ContentType.VIDEO, 45, DifficultyLevel.ADVANCED, ["python"]),
            Module("M2", "Async Programming", ContentType.LAB, 60, DifficultyLevel.ADVANCED, ["python", "async"]),
            Module("M3", "Performance Optimization", ContentType.INTERACTIVE, 50, DifficultyLevel.EXPERT, ["python", "performance"]),
        ],
        prerequisites=[], difficulty=DifficultyLevel.ADVANCED,
        compliance_tags=[],
    )
    course_manager.add_course(py_course)

    compliance_course = Course(
        course_id="CRS-002", title="GDPR Awareness",
        description="Annual GDPR compliance training",
        category=CourseCategory.COMPLIANCE,
        modules=[
            Module("M1", "GDPR Principles", ContentType.VIDEO, 30, DifficultyLevel.BEGINNER, ["gdpr"]),
            Module("M2", "Data Subject Rights", ContentType.QUIZ, 20, DifficultyLevel.BEGINNER, ["gdpr"]),
        ],
        prerequisites=[], difficulty=DifficultyLevel.BEGINNER,
        compliance_tags=["GDPR", "privacy"],
    )
    course_manager.add_course(compliance_course)

    print(f"  Courses registered: {len(course_manager.courses)}")
    for cid, course in course_manager.courses.items():
        print(f"    [{cid}] {course.title} — {course.total_hours}h, {course.module_count} modules")

    learner = Learner(
        learner_id="L001", name="Alice Chen", role="engineer",
        department="Engineering", level=4,
        skill_inventory=[
            SkillEntry("python", MasteryLevel.INTERMEDIATE),
            SkillEntry("sql", MasteryLevel.BEGINNER),
        ],
        enrollments=[], completions=[], compliance_records=[],
    )

    enrollment = course_manager.enroll(learner.learner_id, "CRS-001")
    if enrollment:
        print(f"\n  Enrolled: {enrollment.enrollment_id}")
        print(f"  Modules:  {len(enrollment.module_progress)}")
        course_manager.complete_module(enrollment.enrollment_id, "M1", 0.92)
        print(f"  After M1 completion: {enrollment.completion_pct:.0%}")

    # 2. Adaptive Learning
    print("\n[2] ADAPTIVE LEARNING ENGINE")
    print("-" * 40)
    adaptive = AdaptiveLearningEngine(mastery_threshold=0.80)
    concepts = ["python", "sql", "system_design", "testing"]
    adaptive.assess_baseline(learner.learner_id, concepts)

    test_results = [
        ("python", True), ("python", True), ("python", False),
        ("sql", False), ("sql", True), ("system_design", True),
    ]
    for concept, correct in test_results:
        est = adaptive.update_mastery(learner.learner_id, concept, correct)
        print(f"  {concept:20s} -> mastery={est.mastery_probability:.2%} [{est.mastery_level.value}] "
              f"(obs={est.observations})")

    gaps = adaptive.identify_gaps(learner.learner_id, py_course)
    print(f"\n  Knowledge gaps in Advanced Python: {len(gaps)} modules")
    for g in gaps:
        print(f"    - {g.title} ({g.difficulty.value})")

    recommendations = adaptive.recommend_modules(learner.learner_id, py_course, max_modules=3)
    print(f"\n  Recommended next modules:")
    for rm in recommendations:
        print(f"    [{rm.module.module_id}] {rm.module.title}")
        print(f"      Priority: {rm.priority_score:.3f} | {rm.rationale}")
        print(f"      Est time: {rm.estimated_time_minutes} min")

    schedule = adaptive.spaced_repetition_schedule(learner.learner_id, concepts)
    print(f"\n  Spaced Repetition Schedule:")
    for item in schedule:
        print(f"    {item['concept']:20s} mastery={item['mastery']:.0%} "
              f"review in {item['next_review_days']}d [{item['mastery_level']}]")

    # 3. Skill Gap Analysis
    print("\n[3] SKILL GAP ANALYSIS")
    print("-" * 40)
    gap_analyzer = SkillGapAnalyzer()
    gap_analyzer.register_course(py_course)
    gap_analyzer.register_course(compliance_course)

    gaps = gap_analyzer.analyze_gaps(learner)
    print(f"  Skill Gaps for {learner.name} ({learner.role}):")
    for gap in gaps:
        print(f"    {gap.skill_name:20s} {gap.current_level.value:12s} -> {gap.required_level.value:12s} "
              f"(severity={gap.gap_severity:.2f}, impact={gap.business_impact})")
        print(f"      Recommended: {', '.join(gap.recommended_courses[:2])}")

    learning_path = gap_analyzer.generate_learning_path(learner, gaps)
    print(f"\n  Generated Learning Path: {learning_path.path_id}")
    print(f"    Modules: {len(learning_path.modules)}")
    print(f"    Est hours: {learning_path.total_hours}")
    print(f"    Target:    {learning_path.estimated_completion}")
    print(f"    Rationale: {learning_path.rationale}")

    # 4. Compliance Tracking
    print("\n[4] COMPLIANCE TRAINING")
    print("-" * 40)
    compliance = ComplianceTracker(escalation_days=7)
    compliance.register_requirement(ComplianceRequirement(
        requirement_id="CR-001", regulation="GDPR",
        description="Annual GDPR training", course_id="CRS-002",
        validity_months=12, roles=["engineer", "analyst", "manager"],
    ))
    compliance.register_requirement(ComplianceRequirement(
        requirement_id="CR-002", regulation="SECURITY",
        description="Security awareness training", course_id="CRS-003",
        validity_months=12, roles=["engineer"],
    ))

    comp_report = compliance.check_compliance(learner)
    print(f"  Compliance Report for {learner.name}:")
    print(f"    Requirements: {comp_report.total_requirements}")
    print(f"    Compliant:    {comp_report.compliant}")
    print(f"    Non-compliant: {comp_report.non_compliant}")
    print(f"    Overdue:      {len(comp_report.overdue)}")
    print(f"    Rate:         {comp_report.compliance_rate:.0%}")

    audit_trail = compliance.generate_audit_trail(learner)
    print(f"\n  Audit Trail Entries: {len(audit_trail)}")

    # 5. Learning ROI
    print("\n[5] LEARNING ROI METRICS")
    print("-" * 40)
    roi = LearningROI(
        program_name="Engineering Upskilling Q3",
        total_cost=50000.0,
        total_learners=45,
        completion_rate=0.82,
        avg_skill_improvement=0.35,
        estimated_productivity_gain=125000.0,
    )
    print(f"  Program:    {roi.program_name}")
    print(f"  Cost:       ${roi.total_cost:,.0f}")
    print(f"  Learners:   {roi.total_learners}")
    print(f"  Completion: {roi.completion_rate:.0%}")
    print(f"  Skill gain: {roi.avg_skill_improvement:.0%}")
    print(f"  Prod gain:  ${roi.estimated_productivity_gain:,.0f}")
    print(f"  Cost/learn: ${roi.cost_per_learner:,.0f}")
    print(f"  ROI:        {roi.roi_ratio:.1f}x")

    print("\n" + "=" * 72)
    print("  LEARNING PLATFORM DEMO COMPLETE")
    print("=" * 72)


if __name__ == "__main__":
    main()
