"""
HR Agent — Human Resources management, recruitment, performance reviews,
compensation analysis, employee engagement, compliance, and training.

This module provides comprehensive HR tools including:
- Employee record management and lifecycle tracking
- Recruitment pipeline and applicant tracking
- Performance review management with goal tracking
- Compensation analysis and benchmarking
- Employee engagement surveys and analytics
- Compliance tracking (labor law, certifications, policies)
- Training and development program management
- Time-off and leave management
- Organizational structure and headcount planning
- Attrition analysis and retention modeling
"""

from __future__ import annotations

import logging
import math
import statistics
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

class EmploymentStatus(Enum):
    ACTIVE = "active"
    ON_LEAVE = "on_leave"
    TERMINATED = "terminated"
    RESIGNED = "resigned"
    RETIRED = "retired"
    PROBATIONARY = "probationary"
    CONTRACT = "contract"
    INTERN = "intern"


class EmploymentType(Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    INTERN = "intern"
    FREELANCE = "freelance"


class Department(Enum):
    ENGINEERING = "engineering"
    PRODUCT = "product"
    DESIGN = "design"
    MARKETING = "marketing"
    SALES = "sales"
    CUSTOMER_SUCCESS = "customer_success"
    HR = "hr"
    FINANCE = "finance"
    LEGAL = "legal"
    OPERATIONS = "operations"
    IT = "it"
    SECURITY = "security"
    DATA = "data"
    EXECUTIVE = "executive"


class JobLevel(Enum):
    INTERN = "intern"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    PRINCIPAL = "principal"
    DIRECTOR = "director"
    VP = "vp"
    C_LEVEL = "c_level"


class ReviewCycle(Enum):
    QUARTERLY = "quarterly"
    SEMI_ANNUAL = "semi_annual"
    ANNUAL = "annual"
    PROBATIONARY = "probationary"
    PROJECT_BASED = "project_based"


class ReviewRating(IntEnum):
    NEEDS_IMPROVEMENT = 1
    BELOW_EXPECTATIONS = 2
    MEETS_EXPECTATIONS = 3
    EXCEEDS_EXPECTATIONS = 4
    OUTSTANDING = 5


class CandidateStage(Enum):
    APPLIED = "applied"
    SCREENING = "screening"
    PHONE_INTERVIEW = "phone_interview"
    TECHNICAL_INTERVIEW = "technical_interview"
    ON_SITE = "on_site"
    FINAL_INTERVIEW = "final_interview"
    OFFER = "offer"
    HIRED = "hired"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class LeaveType(Enum):
    VACATION = "vacation"
    SICK = "sick"
    PERSONAL = "personal"
    MATERNITY = "maternity"
    PATERNITY = "paternity"
    BEREAVEMENT = "bereavement"
    UNPAID = "unpaid"
    Jury_DUTY = "jury_duty"
    MILITARY = "military"


class LeaveStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    CANCELLED = "cancelled"


class SurveyQuestionType(Enum):
    LIKERT_5 = "likert_5"
    LIKERT_7 = "likert_7"
    YES_NO = "yes_no"
    MULTIPLE_CHOICE = "multiple_choice"
    OPEN_ENDED = "open_ended"
    RATING = "rating"


class EngagementLevel(Enum):
    VERY_DISENGAGED = 1
    DISENGAGED = 2
    NEUTRAL = 3
    ENGAGED = 4
    VERY_ENGAGED = 5


class ComplianceStatus(Enum):
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PENDING_REVIEW = "pending_review"
    EXEMPT = "exempt"
    EXPIRED = "expired"


class TrainingStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    EXPIRED = "expired"
    OVERDUE = "overdue"


class GoalStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    OVERDUE = "overdue"


class PayFrequency(Enum):
    WEEKLY = "weekly"
    BI_WEEKLY = "bi_weekly"
    SEMI_MONTHLY = "semi_monthly"
    MONTHLY = "monthly"
    ANNUALLY = "annually"


class CompensationType(Enum):
    SALARY = "salary"
    HOURLY = "hourly"
    COMMISSION = "commission"
    BONUS = "bonus"
    EQUITY = "equity"
    STIPEND = "stipend"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class Employee:
    """Employee record."""
    employee_id: str
    first_name: str
    last_name: str
    email: str
    department: Department
    job_title: str
    job_level: JobLevel = JobLevel.MID
    employment_status: EmploymentStatus = EmploymentStatus.ACTIVE
    employment_type: EmploymentType = EmploymentType.FULL_TIME
    hire_date: datetime = field(default_factory=datetime.utcnow)
    termination_date: Optional[datetime] = None
    manager_id: Optional[str] = None
    location: str = ""
    salary: float = 0.0
    pay_frequency: PayFrequency = PayFrequency.BI_WEEKLY
    probation_end_date: Optional[datetime] = None
    last_review_date: Optional[datetime] = None
    next_review_date: Optional[datetime] = None
    skills: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    emergency_contact: Dict[str, str] = field(default_factory=dict)
    address: str = ""
    phone: str = ""
    date_of_birth: Optional[datetime] = None
    gender: str = ""
    ethnicity: str = ""

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def tenure_years(self) -> float:
        end = self.termination_date or datetime.utcnow()
        return (end - self.hire_date).days / 365.25

    @property
    def tenure_months(self) -> float:
        end = self.termination_date or datetime.utcnow()
        return (end - self.hire_date).days / 30.44

    @property
    def is_active(self) -> bool:
        return self.employment_status == EmploymentStatus.ACTIVE

    @property
    def is_on_probation(self) -> bool:
        if not self.probation_end_date:
            return False
        return datetime.utcnow() < self.probation_end_date

    @property
    def annual_salary(self) -> float:
        multipliers = {
            PayFrequency.WEEKLY: 52,
            PayFrequency.BI_WEEKLY: 26,
            PayFrequency.SEMI_MONTHLY: 24,
            PayFrequency.MONTHLY: 12,
            PayFrequency.ANNUALLY: 1,
        }
        return self.salary * multipliers.get(self.pay_frequency, 26)

    @property
    def monthly_salary(self) -> float:
        return self.annual_salary / 12

    def years_since_last_review(self) -> Optional[float]:
        if not self.last_review_date:
            return None
        return (datetime.utcnow() - self.last_review_date).days / 365.25

    def to_dict(self) -> Dict[str, Any]:
        return {
            "employee_id": self.employee_id,
            "name": self.full_name,
            "email": self.email,
            "department": self.department.value,
            "job_title": self.job_title,
            "job_level": self.job_level.value,
            "status": self.employment_status.value,
            "hire_date": self.hire_date.isoformat(),
            "tenure_years": round(self.tenure_years, 1),
            "annual_salary": self.annual_salary,
        }


@dataclass
class Candidate:
    """Job candidate record."""
    candidate_id: str
    first_name: str
    last_name: str
    email: str
    phone: str = ""
    position_applied: str = ""
    stage: CandidateStage = CandidateStage.APPLIED
    source: str = ""  # referral, linkedin, job_board, career_site
    resume_url: str = ""
    applied_date: datetime = field(default_factory=datetime.utcnow)
    last_updated: datetime = field(default_factory=datetime.utcnow)
    salary_expectation: float = 0.0
    current_salary: float = 0.0
    years_experience: float = 0.0
    skills: List[str] = field(default_factory=list)
    notes: List[Dict[str, str]] = field(default_factory=list)
    interview_scores: Dict[str, float] = field(default_factory=dict)
    rejection_reason: str = ""
    recruiter: str = ""
    hiring_manager: str = ""

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def days_in_pipeline(self) -> int:
        return (datetime.utcnow() - self.applied_date).days

    @property
    def average_score(self) -> float:
        if not self.interview_scores:
            return 0.0
        return statistics.mean(self.interview_scores.values())

    @property
    def is_active(self) -> bool:
        return self.stage not in (CandidateStage.REJECTED, CandidateStage.WITHDRAWN, CandidateStage.HIRED)


@dataclass
class PerformanceReview:
    """Performance review record."""
    review_id: str
    employee_id: str
    reviewer_id: str
    review_cycle: ReviewCycle = ReviewCycle.ANNUAL
    review_date: datetime = field(default_factory=datetime.utcnow)
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    overall_rating: Optional[ReviewRating] = None
    competency_ratings: Dict[str, ReviewRating] = field(default_factory=dict)
    goals_met: int = 0
    goals_total: int = 0
    strengths: List[str] = field(default_factory=list)
    improvements: List[str] = field(default_factory=list)
    comments: str = ""
    employee_comments: str = ""
    development_plan: str = ""
    compensation_change: float = 0.0
    promotion_recommended: bool = False

    @property
    def goal_completion_pct(self) -> float:
        if self.goals_total == 0:
            return 0.0
        return self.goals_met / self.goals_total

    @property
    def avg_competency_rating(self) -> float:
        if not self.competency_ratings:
            return 0.0
        return statistics.mean(self.competency_ratings.values())


@dataclass
class Goal:
    """Employee goal/objective."""
    goal_id: str
    employee_id: str
    title: str
    description: str
    status: GoalStatus = GoalStatus.NOT_STARTED
    priority: str = "medium"
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    completion_pct: float = 0.0
    key_results: List[Dict[str, Any]] = field(default_factory=list)
    aligns_with: str = ""  # company OKR reference
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_overdue(self) -> bool:
        if not self.due_date:
            return False
        return datetime.utcnow() > self.due_date and self.status != GoalStatus.COMPLETED

    @property
    def days_until_due(self) -> Optional[int]:
        if not self.due_date:
            return None
        return (self.due_date - datetime.utcnow()).days


@dataclass
class CompensationRecord:
    """Compensation history entry."""
    record_id: str
    employee_id: str
    effective_date: datetime = field(default_factory=datetime.utcnow)
    compensation_type: CompensationType = CompensationType.SALARY
    amount: float = 0.0
    pay_frequency: PayFrequency = PayFrequency.ANNUALLY
    reason: str = ""  # hire, raise, promotion, adjustment
    approved_by: str = ""

    @property
    def annual_amount(self) -> float:
        multipliers = {
            PayFrequency.WEEKLY: 52,
            PayFrequency.BI_WEEKLY: 26,
            PayFrequency.SEMI_MONTHLY: 24,
            PayFrequency.MONTHLY: 12,
            PayFrequency.ANNUALLY: 1,
        }
        return self.amount * multipliers.get(self.pay_frequency, 1)


@dataclass
class LeaveRequest:
    """Time-off request."""
    request_id: str
    employee_id: str
    leave_type: LeaveType
    start_date: datetime = field(default_factory=datetime.utcnow)
    end_date: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(days=1))
    status: LeaveStatus = LeaveStatus.PENDING
    reason: str = ""
    approved_by: Optional[str] = None
    approved_date: Optional[datetime] = None

    @property
    def total_days(self) -> int:
        return max((self.end_date - self.start_date).days, 1)

    @property
    def is_pending(self) -> bool:
        return self.status == LeaveStatus.PENDING

    @property
    def is_approved(self) -> bool:
        return self.status == LeaveStatus.APPROVED


@dataclass
class LeaveBalance:
    """Employee leave balance."""
    employee_id: str
    year: int
    balances: Dict[str, float] = field(default_factory=dict)
    used: Dict[str, float] = field(default_factory=dict)

    def remaining(self, leave_type: str) -> float:
        return self.balances.get(leave_type, 0) - self.used.get(leave_type, 0)

    def total_remaining(self) -> float:
        return sum(self.remaining(lt) for lt in self.balances)


@dataclass
class EngagementSurvey:
    """Employee engagement survey."""
    survey_id: str
    title: str
    questions: List[Dict[str, Any]] = field(default_factory=list)
    responses: List[Dict[str, Any]] = field(default_factory=list)
    created_date: datetime = field(default_factory=datetime.utcnow)
    closed_date: Optional[datetime] = None
    anonymous: bool = True

    @property
    def response_rate(self) -> float:
        if not self.questions:
            return 0.0
        return len(self.responses) / max(len(self.questions), 1)

    @property
    def avg_score(self) -> float:
        all_scores = []
        for resp in self.responses:
            for q_id, answer in resp.get("answers", {}).items():
                if isinstance(answer, (int, float)):
                    all_scores.append(answer)
        return statistics.mean(all_scores) if all_scores else 0.0


@dataclass
class ComplianceItem:
    """Compliance tracking item."""
    item_id: str
    employee_id: str
    requirement: str
    status: ComplianceStatus = ComplianceStatus.PENDING_REVIEW
    due_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    evidence_url: str = ""
    notes: str = ""

    @property
    def is_expired(self) -> bool:
        if not self.expiration_date:
            return False
        return datetime.utcnow() > self.expiration_date

    @property
    def days_until_expiry(self) -> Optional[int]:
        if not self.expiration_date:
            return None
        return (self.expiration_date - datetime.utcnow()).days


@dataclass
class TrainingRecord:
    """Training/completion record."""
    record_id: str
    employee_id: str
    training_name: str
    training_type: str = ""  # compliance, skill, onboarding, safety
    status: TrainingStatus = TrainingStatus.NOT_STARTED
    assigned_date: datetime = field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    score: Optional[float] = None
    provider: str = ""
    duration_hours: float = 0.0
    certificate_url: str = ""

    @property
    def is_overdue(self) -> bool:
        if not self.due_date:
            return False
        return datetime.utcnow() > self.due_date and self.status != TrainingStatus.COMPLETED

    @property
    def is_completed(self) -> bool:
        return self.status == TrainingStatus.COMPLETED


@dataclass
class OrgChart:
    """Organizational structure entry."""
    employee_id: str
    name: str
    title: str
    department: Department
    level: JobLevel
    manager_id: Optional[str] = None
    direct_reports: List[str] = field(default_factory=list)

    @property
    def is_manager(self) -> bool:
        return len(self.direct_reports) > 0

    @property
    def team_size(self) -> int:
        return len(self.direct_reports)


@dataclass
class HeadcountPlan:
    """Headcount planning entry."""
    position: str
    department: Department
    count: int = 1
    budget_per_position: float = 0.0
    priority: str = "medium"
    target_date: Optional[datetime] = None
    status: str = "planned"  # planned, approved, hiring, filled

    @property
    def total_budget(self) -> float:
        return self.count * self.budget_per_position


@dataclass
class ExitInterview:
    """Exit interview record."""
    interview_id: str
    employee_id: str
    exit_date: datetime = field(default_factory=datetime.utcnow)
    reason_for_leaving: str = ""
    overall_satisfaction: int = 0  # 1-5
    manager_rating: int = 0  # 1-5
    culture_rating: int = 0  # 1-5
    compensation_satisfaction: int = 0  # 1-5
    would_recommend: bool = False
    improvement_suggestions: str = ""
    comments: str = ""


@dataclass
class RecruitmentMetrics:
    """Recruitment funnel metrics."""
    total_applicants: int = 0
    screened: int = 0
    interviewed: int = 0
    offered: int = 0
    hired: int = 0
    avg_time_to_fill_days: float = 0.0
    avg_cost_per_hire: float = 0.0
    source_breakdown: Dict[str, int] = field(default_factory=dict)
    diversity_metrics: Dict[str, float] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Employee Manager
# ---------------------------------------------------------------------------

class EmployeeManager:
    """Employee record management and lifecycle tracking."""

    def __init__(self) -> None:
        self.employees: Dict[str, Employee] = {}
        self._emp_counter = 0

    def hire_employee(self, **kwargs: Any) -> Employee:
        self._emp_counter += 1
        emp_id = kwargs.pop("employee_id", f"EMP-{self._emp_counter:05d}")
        emp = Employee(employee_id=emp_id, **kwargs)
        self.employees[emp_id] = emp
        logger.info("Employee hired: %s (%s)", emp.full_name, emp_id)
        return emp

    def terminate_employee(self, employee_id: str, reason: str = "") -> bool:
        if employee_id not in self.employees:
            return False
        emp = self.employees[employee_id]
        emp.employment_status = EmploymentStatus.TERMINATED
        emp.termination_date = datetime.utcnow()
        logger.info("Employee terminated: %s (%s)", emp.full_name, reason)
        return True

    def get_employee(self, employee_id: str) -> Optional[Employee]:
        return self.employees.get(employee_id)

    def get_by_department(self, department: Department) -> List[Employee]:
        return [e for e in self.employees.values() if e.department == department and e.is_active]

    def get_by_manager(self, manager_id: str) -> List[Employee]:
        return [e for e in self.employees.values() if e.manager_id == manager_id and e.is_active]

    def get_headcount(self) -> Dict[str, int]:
        counts: Dict[str, int] = defaultdict(int)
        for emp in self.employees.values():
            if emp.is_active:
                counts[emp.department.value] += 1
        return dict(counts)

    def get_tenure_distribution(self) -> Dict[str, int]:
        brackets = {"< 1 year": 0, "1-3 years": 0, "3-5 years": 0, "5-10 years": 0, "10+ years": 0}
        for emp in self.employees.values():
            if not emp.is_active:
                continue
            t = emp.tenure_years
            if t < 1:
                brackets["< 1 year"] += 1
            elif t < 3:
                brackets["1-3 years"] += 1
            elif t < 5:
                brackets["3-5 years"] += 1
            elif t < 10:
                brackets["5-10 years"] += 1
            else:
                brackets["10+ years"] += 1
        return brackets

    def search(self, query: str) -> List[Employee]:
        q = query.lower()
        return [
            e for e in self.employees.values()
            if q in e.full_name.lower() or q in e.email.lower() or q in e.job_title.lower()
        ]


# ---------------------------------------------------------------------------
# Recruitment Pipeline
# ---------------------------------------------------------------------------

class RecruitmentPipeline:
    """Applicant tracking and recruitment pipeline management."""

    def __init__(self) -> None:
        self.candidates: Dict[str, Candidate] = {}
        self.job_openings: Dict[str, Dict[str, Any]] = {}
        self._cand_counter = 0

    def create_opening(
        self, position: str, department: Department, description: str = "",
        salary_range: Tuple[float, float] = (0, 0)
    ) -> str:
        opening_id = f"JOB-{len(self.job_openings) + 1:04d}"
        self.job_openings[opening_id] = {
            "position": position,
            "department": department.value,
            "description": description,
            "salary_range": salary_range,
            "status": "open",
            "created": datetime.utcnow(),
        }
        return opening_id

    def add_candidate(self, **kwargs: Any) -> Candidate:
        self._cand_counter += 1
        cand_id = kwargs.pop("candidate_id", f"CAND-{self._cand_counter:05d}")
        cand = Candidate(candidate_id=cand_id, **kwargs)
        self.candidates[cand_id] = cand
        logger.info("Candidate added: %s (%s)", cand.full_name, cand_id)
        return cand

    def advance_stage(self, candidate_id: str, stage: CandidateStage, notes: str = "") -> bool:
        if candidate_id not in self.candidates:
            return False
        self.candidates[candidate_id].stage = stage
        self.candidates[candidate_id].last_updated = datetime.utcnow()
        if notes:
            self.candidates[candidate_id].notes.append({
                "date": datetime.utcnow().isoformat(),
                "note": notes,
                "stage": stage.value,
            })
        return True

    def reject_candidate(self, candidate_id: str, reason: str = "") -> bool:
        if candidate_id not in self.candidates:
            return False
        self.candidates[candidate_id].stage = CandidateStage.REJECTED
        self.candidates[candidate_id].rejection_reason = reason
        return True

    def get_pipeline(self, position: Optional[str] = None) -> Dict[str, List[Candidate]]:
        pipeline: Dict[str, List[Candidate]] = defaultdict(list)
        for cand in self.candidates.values():
            if position and cand.position_applied != position:
                continue
            if cand.is_active:
                pipeline[cand.stage.value].append(cand)
        return dict(pipeline)

    def get_metrics(self) -> RecruitmentMetrics:
        active = [c for c in self.candidates.values() if c.is_active]
        hired = [c for c in self.candidates.values() if c.stage == CandidateStage.HIRED]
        source_counts = defaultdict(int)
        for c in self.candidates.values():
            source_counts[c.source] += 1
        avg_days = statistics.mean([c.days_in_pipeline for c in hired]) if hired else 0
        return RecruitmentMetrics(
            total_applicants=len(self.candidates),
            screened=sum(1 for c in active if c.stage != CandidateStage.APPLIED),
            interviewed=sum(1 for c in active if c.stage in (
                CandidateStage.PHONE_INTERVIEW, CandidateStage.TECHNICAL_INTERVIEW,
                CandidateStage.ON_SITE, CandidateStage.FINAL_INTERVIEW)),
            offered=sum(1 for c in active if c.stage == CandidateStage.OFFER),
            hired=len(hired),
            avg_time_to_fill_days=avg_days,
            source_breakdown=dict(source_counts),
        )


# ---------------------------------------------------------------------------
# Performance Manager
# ---------------------------------------------------------------------------

class PerformanceManager:
    """Performance review and goal management."""

    def __init__(self) -> None:
        self.reviews: Dict[str, PerformanceReview] = {}
        self.goals: Dict[str, Goal] = {}
        self._review_counter = 0
        self._goal_counter = 0

    def create_review(self, **kwargs: Any) -> PerformanceReview:
        self._review_counter += 1
        review_id = kwargs.pop("review_id", f"REV-{self._review_counter:05d}")
        review = PerformanceReview(review_id=review_id, **kwargs)
        self.reviews[review_id] = review
        return review

    def add_goal(self, **kwargs: Any) -> Goal:
        self._goal_counter += 1
        goal_id = kwargs.pop("goal_id", f"GOAL-{self._goal_counter:05d}")
        goal = Goal(goal_id=goal_id, **kwargs)
        self.goals[goal_id] = goal
        return goal

    def update_goal_progress(self, goal_id: str, completion_pct: float, status: Optional[GoalStatus] = None) -> bool:
        if goal_id not in self.goals:
            return False
        goal = self.goals[goal_id]
        goal.completion_pct = min(completion_pct, 100.0)
        if status:
            goal.status = status
        elif completion_pct >= 100:
            goal.status = GoalStatus.COMPLETED
        return True

    def get_employee_reviews(self, employee_id: str) -> List[PerformanceReview]:
        return sorted(
            [r for r in self.reviews.values() if r.employee_id == employee_id],
            key=lambda r: r.review_date, reverse=True
        )

    def get_employee_goals(self, employee_id: str) -> List[Goal]:
        return [g for g in self.goals.values() if g.employee_id == employee_id]

    def get_latest_review(self, employee_id: str) -> Optional[PerformanceReview]:
        reviews = self.get_employee_reviews(employee_id)
        return reviews[0] if reviews else None

    def performance_summary(self, employee_id: str) -> Dict[str, Any]:
        reviews = self.get_employee_reviews(employee_id)
        goals = self.get_employee_goals(employee_id)
        latest = reviews[0] if reviews else None
        avg_rating = statistics.mean([r.overall_rating for r in reviews if r.overall_rating]) if reviews else 0
        completed_goals = sum(1 for g in goals if g.status == GoalStatus.COMPLETED)
        return {
            "employee_id": employee_id,
            "total_reviews": len(reviews),
            "avg_rating": avg_rating,
            "latest_rating": latest.overall_rating.value if latest and latest.overall_rating else None,
            "total_goals": len(goals),
            "completed_goals": completed_goals,
            "goal_completion_rate": completed_goals / len(goals) if goals else 0,
            "promotion_recommended": latest.promotion_recommended if latest else False,
        }


# ---------------------------------------------------------------------------
# Compensation Analyzer
# ---------------------------------------------------------------------------

class CompensationAnalyzer:
    """Compensation analysis, benchmarking, and equity analysis."""

    def __init__(self) -> None:
        self.comp_records: Dict[str, List[CompensationRecord]] = defaultdict(list)
        self.benchmarks: Dict[str, Dict[str, float]] = {}

    def add_record(self, record: CompensationRecord) -> None:
        self.comp_records[record.employee_id].append(record)

    def set_benchmark(self, job_title: str, market_rate: float, percentile: int = 50) -> None:
        self.benchmarks[job_title] = {"market_rate": market_rate, "percentile": percentile}

    def get_current_comp(self, employee_id: str) -> Optional[CompensationRecord]:
        records = self.comp_records.get(employee_id, [])
        if not records:
            return None
        return sorted(records, key=lambda r: r.effective_date, reverse=True)[0]

    def get_comp_history(self, employee_id: str) -> List[CompensationRecord]:
        return sorted(self.comp_records.get(employee_id, []), key=lambda r: r.effective_date)

    def calculate_pay_equity(self) -> Dict[str, Any]:
        by_title: Dict[str, List[float]] = defaultdict(list)
        for emp_id, records in self.comp_records.items():
            current = sorted(records, key=lambda r: r.effective_date, reverse=True)
            if current:
                by_title[current[0].reason].append(current[0].annual_amount)

        equity_issues = []
        for title, salaries in by_title.items():
            if len(salaries) >= 2:
                median = statistics.median(salaries)
                for s in salaries:
                    if abs(s - median) / median > 0.15:
                        equity_issues.append({"title": title, "salary": s, "median": median})

        return {
            "titles_analyzed": len(by_title),
            "equity_issues": equity_issues,
        }

    def comp_vs_benchmark(self, employee_id: str) -> Dict[str, Any]:
        current = self.get_current_comp(employee_id)
        if not current:
            return {"error": "No compensation record"}
        benchmark = self.benchmarks.get(current.reason, {})
        if not benchmark:
            return {"error": "No benchmark data"}
        ratio = current.annual_amount / benchmark["market_rate"] if benchmark["market_rate"] > 0 else 0
        return {
            "employee_id": employee_id,
            "current_salary": current.annual_amount,
            "market_rate": benchmark["market_rate"],
            "ratio": ratio,
            "above_market": ratio > 1.0,
        }


# ---------------------------------------------------------------------------
# Engagement Analyzer
# ---------------------------------------------------------------------------

class EngagementAnalyzer:
    """Employee engagement survey and analytics."""

    def __init__(self) -> None:
        self.surveys: Dict[str, EngagementSurvey] = {}
        self._survey_counter = 0

    def create_survey(self, title: str, questions: List[Dict[str, Any]]) -> EngagementSurvey:
        self._survey_counter += 1
        survey = EngagementSurvey(
            survey_id=f"SRV-{self._survey_counter:04d}",
            title=title,
            questions=questions,
        )
        self.surveys[survey.survey_id] = survey
        return survey

    def submit_response(self, survey_id: str, employee_id: str, answers: Dict[str, Any]) -> bool:
        if survey_id not in self.surveys:
            return False
        self.surveys[survey_id].responses.append({
            "employee_id": employee_id,
            "answers": answers,
            "submitted_at": datetime.utcnow(),
        })
        return True

    def get_survey_results(self, survey_id: str) -> Dict[str, Any]:
        if survey_id not in self.surveys:
            return {}
        survey = self.surveys[survey_id]
        return {
            "survey_id": survey_id,
            "title": survey.title,
            "responses": len(survey.responses),
            "avg_score": survey.avg_score,
            "questions": len(survey.questions),
        }

    def analyze_department_engagement(
        self, survey_id: str, employees: Dict[str, Employee]
    ) -> Dict[str, float]:
        if survey_id not in self.surveys:
            return {}
        survey = self.surveys[survey_id]
        dept_scores: Dict[str, List[float]] = defaultdict(list)
        for resp in survey.responses:
            emp_id = resp.get("employee_id")
            if emp_id in employees:
                dept = employees[emp_id].department.value
                scores = [v for v in resp.get("answers", {}).values() if isinstance(v, (int, float))]
                if scores:
                    dept_scores[dept].append(statistics.mean(scores))
        return {dept: statistics.mean(scores) for dept, scores in dept_scores.items()}


# ---------------------------------------------------------------------------
# Leave Manager
# ---------------------------------------------------------------------------

class LeaveManager:
    """Time-off request and balance management."""

    def __init__(self, default_policies: Optional[Dict[str, float]] = None) -> None:
        self.requests: Dict[str, LeaveRequest] = {}
        self.balances: Dict[str, LeaveBalance] = {}
        self.policies = default_policies or {
            "vacation": 15, "sick": 10, "personal": 5,
        }
        self._req_counter = 0

    def set_balance(self, employee_id: str, year: int, balances: Dict[str, float]) -> None:
        key = f"{employee_id}-{year}"
        self.balances[key] = LeaveBalance(employee_id=employee_id, year=year, balances=balances)

    def submit_request(self, employee_id: str, leave_type: LeaveType, start: datetime, end: datetime, reason: str = "") -> LeaveRequest:
        self._req_counter += 1
        req = LeaveRequest(
            request_id=f"LR-{self._req_counter:05d}",
            employee_id=employee_id,
            leave_type=leave_type,
            start_date=start,
            end_date=end,
            reason=reason,
        )
        self.requests[req.request_id] = req
        return req

    def approve_request(self, request_id: str, approver: str) -> bool:
        if request_id not in self.requests:
            return False
        req = self.requests[request_id]
        req.status = LeaveStatus.APPROVED
        req.approved_by = approver
        req.approved_date = datetime.utcnow()
        key = f"{req.employee_id}-{req.start_date.year}"
        if key in self.balances:
            self.balances[key].used[req.leave_type.value] = (
                self.balances[key].used.get(req.leave_type.value, 0) + req.total_days
            )
        return True

    def deny_request(self, request_id: str) -> bool:
        if request_id not in self.requests:
            return False
        self.requests[request_id].status = LeaveStatus.DENIED
        return True

    def get_pending_requests(self) -> List[LeaveRequest]:
        return [r for r in self.requests.values() if r.is_pending]

    def get_employee_balance(self, employee_id: str, year: int) -> Optional[LeaveBalance]:
        return self.balances.get(f"{employee_id}-{year}")

    def get_leave_summary(self) -> Dict[str, Any]:
        by_type = defaultdict(int)
        for req in self.requests.values():
            if req.is_approved:
                by_type[req.leave_type.value] += req.total_days
        return {
            "total_requests": len(self.requests),
            "pending": sum(1 for r in self.requests.values() if r.is_pending),
            "approved_days": dict(by_type),
        }


# ---------------------------------------------------------------------------
# Compliance Tracker
# ---------------------------------------------------------------------------

class ComplianceTracker:
    """Compliance requirement tracking and reporting."""

    def __init__(self) -> None:
        self.items: Dict[str, ComplianceItem] = {}
        self._item_counter = 0

    def add_requirement(self, employee_id: str, requirement: str, due_date: Optional[datetime] = None, expiration: Optional[datetime] = None) -> ComplianceItem:
        self._item_counter += 1
        item = ComplianceItem(
            item_id=f"COMP-{self._item_counter:05d}",
            employee_id=employee_id,
            requirement=requirement,
            due_date=due_date,
            expiration_date=expiration,
        )
        self.items[item.item_id] = item
        return item

    def update_status(self, item_id: str, status: ComplianceStatus) -> bool:
        if item_id not in self.items:
            return False
        self.items[item_id].status = status
        if status == ComplianceStatus.COMPLIANT:
            self.items[item_id].completed_date = datetime.utcnow()
        return True

    def get_employee_compliance(self, employee_id: str) -> List[ComplianceItem]:
        return [i for i in self.items.values() if i.employee_id == employee_id]

    def get_expiring(self, days: int = 30) -> List[ComplianceItem]:
        cutoff = datetime.utcnow() + timedelta(days=days)
        return [
            i for i in self.items.values()
            if i.expiration_date and i.expiration_date <= cutoff and i.status != ComplianceStatus.COMPLIANT
        ]

    def get_non_compliant(self) -> List[ComplianceItem]:
        return [i for i in self.items.values() if i.status == ComplianceStatus.NON_COMPLIANT]

    def compliance_report(self) -> Dict[str, Any]:
        by_status = defaultdict(int)
        for item in self.items.values():
            by_status[item.status.value] += 1
        return {
            "total": len(self.items),
            "by_status": dict(by_status),
            "expiring_soon": len(self.get_expiring(30)),
            "non_compliant": len(self.get_non_compliant()),
        }


# ---------------------------------------------------------------------------
# Training Manager
# ---------------------------------------------------------------------------

class TrainingManager:
    """Training program management and tracking."""

    def __init__(self) -> None:
        self.records: Dict[str, TrainingRecord] = {}
        self.programs: Dict[str, Dict[str, Any]] = {}
        self._rec_counter = 0

    def create_program(self, name: str, training_type: str, duration_hours: float, provider: str = "") -> str:
        prog_id = f"TRP-{len(self.programs) + 1:04d}"
        self.programs[prog_id] = {
            "name": name,
            "type": training_type,
            "duration_hours": duration_hours,
            "provider": provider,
        }
        return prog_id

    def assign_training(self, employee_id: str, training_name: str, due_date: Optional[datetime] = None) -> TrainingRecord:
        self._rec_counter += 1
        record = TrainingRecord(
            record_id=f"TR-{self._rec_counter:05d}",
            employee_id=employee_id,
            training_name=training_name,
            due_date=due_date,
        )
        self.records[record.record_id] = record
        return record

    def complete_training(self, record_id: str, score: Optional[float] = None) -> bool:
        if record_id not in self.records:
            return False
        record = self.records[record_id]
        record.status = TrainingStatus.COMPLETED
        record.completed_date = datetime.utcnow()
        record.score = score
        return True

    def get_employee_training(self, employee_id: str) -> List[TrainingRecord]:
        return [r for r in self.records.values() if r.employee_id == employee_id]

    def get_overdue(self) -> List[TrainingRecord]:
        return [r for r in self.records.values() if r.is_overdue]

    def training_completion_rate(self) -> Dict[str, Any]:
        total = len(self.records)
        completed = sum(1 for r in self.records.values() if r.is_completed)
        overdue = len(self.get_overdue())
        return {
            "total_assigned": total,
            "completed": completed,
            "overdue": overdue,
            "completion_rate": completed / total if total > 0 else 0,
        }


# ---------------------------------------------------------------------------
# Org Chart Manager
# ---------------------------------------------------------------------------

class OrgChartManager:
    """Organizational structure management."""

    def __init__(self) -> None:
        self.entries: Dict[str, OrgChart] = {}

    def add_employee(self, employee_id: str, name: str, title: str, department: Department, level: JobLevel, manager_id: Optional[str] = None) -> OrgChart:
        entry = OrgChart(
            employee_id=employee_id, name=name, title=title,
            department=department, level=level, manager_id=manager_id,
        )
        self.entries[employee_id] = entry
        if manager_id and manager_id in self.entries:
            self.entries[manager_id].direct_reports.append(employee_id)
        return entry

    def get_direct_reports(self, employee_id: str) -> List[OrgChart]:
        if employee_id not in self.entries:
            return []
        return [self.entries[eid] for eid in self.entries[employee_id].direct_reports if eid in self.entries]

    def get_org_depth(self, employee_id: str) -> int:
        depth = 0
        current = employee_id
        while current in self.entries and self.entries[current].manager_id:
            depth += 1
            current = self.entries[current].manager_id
        return depth

    def get_team_tree(self, employee_id: str, depth: int = 0) -> Dict[str, Any]:
        if employee_id not in self.entries:
            return {}
        entry = self.entries[employee_id]
        return {
            "name": entry.name,
            "title": entry.title,
            "department": entry.department.value,
            "reports": [
                self.get_team_tree(report_id, depth + 1)
                for report_id in entry.direct_reports
            ],
        }


# ---------------------------------------------------------------------------
# Main demonstration
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("=" * 60)
    print("HR Agent — Comprehensive Demo")
    print("=" * 60)

    # Employee Management
    emp_mgr = EmployeeManager()
    emp1 = emp_mgr.hire_employee(first_name="Alice", last_name="Johnson", email="alice@co.com", department=Department.ENGINEERING, job_title="Senior Engineer", job_level=JobLevel.SENIOR, salary=120000)
    emp2 = emp_mgr.hire_employee(first_name="Bob", last_name="Smith", email="bob@co.com", department=Department.ENGINEERING, job_title="Junior Engineer", job_level=JobLevel.JUNIOR, salary=80000, manager_id=emp1.employee_id)
    emp3 = emp_mgr.hire_employee(first_name="Carol", last_name="Williams", email="carol@co.com", department=Department.HR, job_title="HR Manager", job_level=JobLevel.LEAD, salary=110000)

    print(f"\nHeadcount: {emp_mgr.get_headcount()}")
    print(f"Tenure distribution: {emp_mgr.get_tenure_distribution()}")

    # Recruitment
    pipeline = RecruitmentPipeline()
    opening = pipeline.create_opening("Backend Engineer", Department.ENGINEERING)
    cand1 = pipeline.add_candidate(first_name="Dave", last_name="Brown", email="dave@email.com", position_applied="Backend Engineer", source="linkedin")
    cand2 = pipeline.add_candidate(first_name="Eve", last_name="Davis", email="eve@email.com", position_applied="Backend Engineer", source="referral")
    pipeline.advance_stage(cand1.candidate_id, CandidateStage.PHONE_INTERVIEW, "Good phone screen")
    pipeline.advance_stage(cand1.candidate_id, CandidateStage.TECHNICAL_INTERVIEW)

    metrics = pipeline.get_metrics()
    print(f"\nRecruitment: {metrics.total_applicants} applicants, {metrics.hired} hired")

    # Performance
    perf_mgr = PerformanceManager()
    review = perf_mgr.create_review(employee_id=emp1.employee_id, reviewer_id=emp3.employee_id, overall_rating=ReviewRating.EXCEEDS_EXPECTATIONS, goals_met=4, goals_total=5)
    goal = perf_mgr.add_goal(employee_id=emp1.employee_id, title="Complete project X", status=GoalStatus.IN_PROGRESS, completion_pct=75)
    summary = perf_mgr.performance_summary(emp1.employee_id)
    print(f"\nPerformance: avg rating={summary['avg_rating']}, goals={summary['completed_goals']}/{summary['total_goals']}")

    # Compensation
    comp_analyzer = CompensationAnalyzer()
    comp_analyzer.add_record(CompensationRecord("CR1", emp1.employee_id, amount=120000, reason="Senior Engineer"))
    comp_analyzer.add_record(CompensationRecord("CR2", emp2.employee_id, amount=80000, reason="Junior Engineer"))
    comp_analyzer.set_benchmark("Senior Engineer", 130000)
    equity = comp_analyzer.calculate_pay_equity()
    print(f"\nCompensation: {equity['titles_analyzed']} titles, {len(equity['equity_issues'])} issues")

    # Leave
    leave_mgr = LeaveManager()
    leave_mgr.set_balance(emp1.employee_id, 2025, {"vacation": 15, "sick": 10, "personal": 5})
    req = leave_mgr.submit_request(emp1.employee_id, LeaveType.VACATION, datetime(2025, 8, 1), datetime(2025, 8, 5), "Summer vacation")
    leave_mgr.approve_request(req.request_id, emp3.employee_id)
    balance = leave_mgr.get_employee_balance(emp1.employee_id, 2025)
    print(f"\nLeave: vacation remaining = {balance.remaining('vacation') if balance else 'N/A'}")

    # Training
    training_mgr = TrainingManager()
    training_mgr.create_program("Security Awareness", "compliance", 2.0)
    tr = training_mgr.assign_training(emp1.employee_id, "Security Awareness", datetime(2025, 9, 1))
    training_mgr.complete_training(tr.record_id, score=95)
    rate = training_mgr.training_completion_rate()
    print(f"\nTraining: {rate['completed']}/{rate['total_assigned']} completed ({rate['completion_rate']:.0%})")

    # Compliance
    compliance = ComplianceTracker()
    compliance.add_requirement(emp1.employee_id, "Annual Security Training", expiration=datetime(2025, 12, 31))
    compliance.add_requirement(emp2.employee_id, "Background Check")
    compliance.update_status(compliance.items[list(compliance.items.keys())[0]].item_id, ComplianceStatus.COMPLIANT)
    report = compliance.compliance_report()
    print(f"\nCompliance: {report['total']} items, {report['non_compliant']} non-compliant")

    # Org Chart
    org = OrgChartManager()
    org.add_employee(emp1.employee_id, emp1.full_name, "Senior Engineer", Department.ENGINEERING, JobLevel.SENIOR)
    org.add_employee(emp2.employee_id, emp2.full_name, "Junior Engineer", Department.ENGINEERING, JobLevel.JUNIOR, manager_id=emp1.employee_id)
    org.add_employee(emp3.employee_id, emp3.full_name, "HR Manager", Department.HR, JobLevel.LEAD)
    tree = org.get_team_tree(emp1.employee_id)
    print(f"\nOrg Chart: {tree['name']} manages {len(tree['reports'])} reports")

    print("\n" + "=" * 60)
    print("HR Agent demo complete.")
    print("=" * 60)
