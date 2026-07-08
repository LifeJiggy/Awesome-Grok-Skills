"""
HR Agent — Human Resources management, recruitment, performance reviews,
compensation analysis, employee engagement, compliance, and training.

Comprehensive implementation featuring:
- Employee record management and lifecycle tracking
- Recruitment pipeline and applicant tracking with funnel analytics
- Performance review management with goal tracking and 360-degree feedback
- Compensation analysis, benchmarking, and pay equity audits
- Employee engagement surveys and analytics dashboards
- Compliance tracking (labor law, certifications, policies, GDPR/CCPA)
- Training and development program management with LMS integration
- Time-off and leave management with policy enforcement
- Organizational structure and headcount planning
- Attrition analysis and retention modeling
- Onboarding workflow automation
- Offboarding and knowledge transfer tracking
- Benefits administration and enrollment
- HRIS integration patterns and data synchronization
"""

from __future__ import annotations

import hashlib
import json
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
    FURLOUGHED = "furloughed"
    SABBATICAL = "sabbatical"


class EmploymentType(Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    INTERN = "intern"
    FREELANCE = "freelance"
    SEASONAL = "seasonal"


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
    RESEARCH = "research"
    QUALITY = "quality"
    PROCUREMENT = "procurement"
    FACILITIES = "facilities"


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
    MONTHLY = "monthly"


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
    TECHNICAL_INTERVIEW = "technical_interVIEW"
    ON_SITE = "on_site"
    FINAL_INTERVIEW = "final_interview"
    OFFER = "offer"
    HIRED = "hired"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
    WAITLISTED = "waitlisted"


class LeaveType(Enum):
    VACATION = "vacation"
    SICK = "sick"
    PERSONAL = "personal"
    MATERNITY = "maternity"
    PATERNITY = "paternity"
    BEREAVEMENT = "bereavement"
    UNPAID = "unpaid"
    JURY_DUTY = "jury_duty"
    MILITARY = "military"
    Voting = "voting"
    BIRTHDAY = "birthday"
    SABBATICAL = "sabbatical"


class LeaveStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class SurveyQuestionType(Enum):
    LIKERT_5 = "likert_5"
    LIKERT_7 = "likert_7"
    YES_NO = "yes_no"
    MULTIPLE_CHOICE = "multiple_choice"
    OPEN_ENDED = "open_ended"
    RATING = "rating"
    NPS = "nps"


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
    OVERDUE = "overdue"


class TrainingStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    EXPIRED = "expired"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class GoalStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    OVERDUE = "overdue"
    ON_HOLD = "on_hold"


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
    SIGN_ON_BONUS = "sign_on_bonus"
    RETENTION_BONUS = "retention_bonus"


class OnboardingStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"


class OffboardingStatus(Enum):
    NOT_STARTED = "not_started"
    EXIT_INTERVIEW = "exit_interview"
    EQUIPMENT_RETURN = "equipment_return"
    ACCESS_REVOKED = "access_revoked"
    KNOWLEDGE_TRANSFER = "knowledge_transfer"
    FINAL_PAYROLL = "final_payroll"
    COMPLETED = "completed"


class BenefitType(Enum):
    HEALTH_INSURANCE = "health_insurance"
    DENTAL = "dental"
    VISION = "vision"
    LIFE_INSURANCE = "life_insurance"
    DISABILITY = "disability"
    RETIREMENT_401K = "retirement_401k"
    HSA = "hsa"
    FSA = "fsa"
    PTO = "pto"
    TUITION_REIMBURSEMENT = "tuition_reimbursement"
    WELLNESS = "wellness"
    TRANSPORTATION = "transportation"


class HeadcountStatus(Enum):
    PLANNED = "planned"
    APPROVED = "approved"
    HIRING = "hiring"
    FILLED = "filled"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"


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
    remote_work_eligible: bool = False
    office_days_per_week: int = 5
    employee满意的rating: float = 0.0
    performance_score: float = 0.0
    engagement_score: float = 0.0
    risk_of_attrition: float = 0.0
    promotion_readiness: float = 0.0
    salary_competitiveness_ratio: float = 1.0

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

    @property
    def daily_salary(self) -> float:
        return self.annual_salary / 260

    @property
    def hourly_rate(self) -> float:
        return self.annual_salary / 2080

    @property
    def benefits_cost_annual(self) -> float:
        return self.annual_salary * 0.30

    @property
    def total_compensation(self) -> float:
        return self.annual_salary + self.benefits_cost_annual

    def years_since_last_review(self) -> Optional[float]:
        if not self.last_review_date:
            return None
        return (datetime.utcnow() - self.last_review_date).days / 365.25

    def years_of_service_at(self, date: datetime) -> float:
        return (date - self.hire_date).days / 365.25

    def is_eligible_for_review(self, min_months: int = 6) -> bool:
        if not self.last_review_date:
            months = self.tenure_months
            return months >= min_months
        months = (datetime.utcnow() - self.last_review_date).days / 30.44
        return months >= min_months

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
            "total_compensation": self.total_compensation,
            "performance_score": self.performance_score,
            "engagement_score": self.engagement_score,
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
    source: str = ""
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
    referral_employee_id: Optional[str] = None
    location_preference: str = ""
    remote_work_ok: bool = False
    availability_date: Optional[datetime] = None
    offer_amount: float = 0.0
    offer_date: Optional[datetime] = None
    offer_expiry: Optional[datetime] = None
    background_check_status: str = "pending"
    reference_check_status: str = "pending"

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

    @property
    def is_offer_pending(self) -> bool:
        if not self.offer_date or not self.offer_expiry:
            return False
        return self.stage == CandidateStage.OFFER and datetime.utcnow() < self.offer_expiry

    def days_until_offer_expiry(self) -> Optional[int]:
        if not self.offer_expiry:
            return None
        return (self.offer_expiry - datetime.utcnow()).days


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
    self_assessment_score: Optional[float] = None
    peer_feedback_score: Optional[float] = None
    manager_feedback_score: Optional[float] = None
    upward_feedback_score: Optional[float] = None
    calibration_notes: str = ""

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

    @property
    def weighted_360_score(self) -> Optional[float]:
        scores = []
        weights = []
        if self.self_assessment_score is not None:
            scores.append(self.self_assessment_score)
            weights.append(0.15)
        if self.peer_feedback_score is not None:
            scores.append(self.peer_feedback_score)
            weights.append(0.25)
        if self.manager_feedback_score is not None:
            scores.append(self.manager_feedback_score)
            weights.append(0.40)
        if self.upward_feedback_score is not None:
            scores.append(self.upward_feedback_score)
            weights.append(0.20)
        if not scores:
            return None
        total_weight = sum(weights)
        weighted_sum = sum(s * w for s, w in zip(scores, weights))
        return weighted_sum / total_weight if total_weight > 0 else None


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
    aligns_with: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    parent_goal_id: Optional[str] = None
    category: str = "performance"
    weight: float = 1.0
    measurable_unit: str = ""
    target_value: float = 0.0
    current_value: float = 0.0
    milestones: List[Dict[str, Any]] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)
    notes: List[Dict[str, str]] = field(default_factory=list)

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

    @property
    def progress_based_on_value(self) -> Optional[float]:
        if self.target_value <= 0:
            return None
        return min(100.0, (self.current_value / self.target_value) * 100)

    @property
    def is_child_goal(self) -> bool:
        return self.parent_goal_id is not None


@dataclass
class CompensationRecord:
    """Compensation history entry."""
    record_id: str
    employee_id: str
    effective_date: datetime = field(default_factory=datetime.utcnow)
    compensation_type: CompensationType = CompensationType.SALARY
    amount: float = 0.0
    pay_frequency: PayFrequency = PayFrequency.ANNUALLY
    reason: str = ""
    approved_by: str = ""
    notes: str = ""

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
    notes: str = ""
    medical_certificate_url: Optional[str] = None
    coverage_plan: str = ""
    emergency_contact_notified: bool = False

    @property
    def total_days(self) -> int:
        return max((self.end_date - self.start_date).days, 1)

    @property
    def is_pending(self) -> bool:
        return self.status == LeaveStatus.PENDING

    @property
    def is_approved(self) -> bool:
        return self.status == LeaveStatus.APPROVED

    @property
    def is_currently_active(self) -> bool:
        now = datetime.utcnow()
        return self.status == LeaveStatus.APPROVED and self.start_date <= now <= self.end_date


@dataclass
class LeaveBalance:
    """Employee leave balance."""
    employee_id: str
    year: int
    balances: Dict[str, float] = field(default_factory=dict)
    used: Dict[str, float] = field(default_factory=dict)
    pending: Dict[str, float] = field(default_factory=dict)

    def remaining(self, leave_type: str) -> float:
        return self.balances.get(leave_type, 0) - self.used.get(leave_type, 0)

    def total_remaining(self) -> float:
        return sum(self.remaining(lt) for lt in self.balances)

    def utilization_rate(self, leave_type: str) -> float:
        total = self.balances.get(leave_type, 0)
        used = self.used.get(leave_type, 0)
        return used / total if total > 0 else 0.0

    def usage_by_type(self) -> Dict[str, Dict[str, float]]:
        result = {}
        for lt in self.balances:
            result[lt] = {
                "balance": self.balances[lt],
                "used": self.used.get(lt, 0),
                "remaining": self.remaining(lt),
                "utilization": self.utilization_rate(lt),
            }
        return result


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
    target_participants: int = 0
    description: str = ""
    reminder_sent: bool = False

    @property
    def response_rate(self) -> float:
        if self.target_participants == 0:
            return 0.0
        return len(self.responses) / self.target_participants

    @property
    def avg_score(self) -> float:
        all_scores = []
        for resp in self.responses:
            for q_id, answer in resp.get("answers", {}).items():
                if isinstance(answer, (int, float)):
                    all_scores.append(answer)
        return statistics.mean(all_scores) if all_scores else 0.0

    @property
    def nps_score(self) -> Optional[float]:
        scores = []
        for resp in self.responses:
            for q_id, answer in resp.get("answers", {}).items():
                if isinstance(answer, (int, float)) and 0 <= answer <= 10:
                    scores.append(answer)
        if not scores:
            return None
        promoters = sum(1 for s in scores if s >= 9)
        detractors = sum(1 for s in scores if s <= 6)
        return (promoters - detractors) / len(scores) * 100

    @property
    def question_averages(self) -> Dict[str, float]:
        q_totals: Dict[str, List[float]] = defaultdict(list)
        for resp in self.responses:
            for q_id, answer in resp.get("answers", {}).items():
                if isinstance(answer, (int, float)):
                    q_totals[q_id].append(answer)
        return {q: statistics.mean(vals) for q, vals in q_totals.items()}


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
    assigned_by: str = ""
    category: str = "general"
    auto_renew: bool = False
    renewal_lead_days: int = 30

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

    @property
    def needs_renewal(self) -> bool:
        if not self.expiration_date or not self.auto_renew:
            return False
        days_left = self.days_until_expiry
        return days_left is not None and days_left <= self.renewal_lead_days

    @property
    def is_overdue(self) -> bool:
        if not self.due_date:
            return False
        return datetime.utcnow() > self.due_date and self.status not in (ComplianceStatus.COMPLIANT, ComplianceStatus.EXEMPT)


@dataclass
class TrainingRecord:
    """Training/completion record."""
    record_id: str
    employee_id: str
    training_name: str
    training_type: str = ""
    status: TrainingStatus = TrainingStatus.NOT_STARTED
    assigned_date: datetime = field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    score: Optional[float] = None
    provider: str = ""
    duration_hours: float = 0.0
    certificate_url: str = ""
    max_score: float = 100.0
    passing_score: float = 70.0
    attempts: int = 0
    max_attempts: int = 3
    version: str = "1.0"
    required: bool = True

    @property
    def is_overdue(self) -> bool:
        if not self.due_date:
            return False
        return datetime.utcnow() > self.due_date and self.status != TrainingStatus.COMPLETED

    @property
    def is_completed(self) -> bool:
        return self.status == TrainingStatus.COMPLETED

    @property
    def passed(self) -> bool:
        if self.score is None:
            return False
        return self.score >= self.passing_score

    @property
    def days_until_due(self) -> Optional[int]:
        if not self.due_date:
            return None
        return (self.due_date - datetime.utcnow()).days

    @property
    def completion_duration_days(self) -> Optional[int]:
        if not self.completed_date:
            return None
        return (self.completed_date - self.assigned_date).days


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
    cost_center: str = ""
    location: str = ""
    is_vacant: bool = False

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
    status: HeadcountStatus = HeadcountStatus.PLANNED
    justification: str = ""
    requisition_id: Optional[str] = None
    hiring_manager: str = ""
    approved_by: str = ""
    filled_count: int = 0

    @property
    def total_budget(self) -> float:
        return self.count * self.budget_per_position

    @property
    def remaining_count(self) -> int:
        return self.count - self.filled_count

    @property
    def fill_rate(self) -> float:
        return self.filled_count / self.count if self.count > 0 else 0.0


@dataclass
class ExitInterview:
    """Exit interview record."""
    interview_id: str
    employee_id: str
    exit_date: datetime = field(default_factory=datetime.utcnow)
    reason_for_leaving: str = ""
    overall_satisfaction: int = 0
    manager_rating: int = 0
    culture_rating: int = 0
    compensation_satisfaction: int = 0
    growth_opportunities: int = 0
    work_life_balance: int = 0
    would_recommend: bool = False
    would_return: bool = False
    improvement_suggestions: str = ""
    comments: str = ""
    interviewer: str = ""
    voluntary: bool = True
    counter_offer_made: bool = False
    counter_offer_accepted: bool = False
    rehire_eligible: bool = True
    knowledge_transfer_complete: bool = False


@dataclass
class RecruitmentMetrics:
    """Recruitment funnel metrics."""
    total_applicants: int = 0
    screened: int = 0
    interviewed: int = 0
    offered: int = 0
    hired: int = 0
    avg_time_to_fill_days: float = 0.0
    avg_time_to_hire_days: float = 0.0
    avg_cost_per_hire: float = 0.0
    source_breakdown: Dict[str, int] = field(default_factory=dict)
    diversity_metrics: Dict[str, float] = field(default_factory=dict)
    offer_acceptance_rate: float = 0.0
    quality_of_hire_score: float = 0.0
    recruitment_funnel_conversion: Dict[str, float] = field(default_factory=dict)


@dataclass
class OnboardingTask:
    """A single onboarding task."""
    task_id: str
    title: str
    description: str
    assigned_to: str
    due_days: int
    completed: bool = False
    completed_date: Optional[datetime] = None
    category: str = "general"

    @property
    def is_overdue(self) -> bool:
        return not self.completed and datetime.utcnow() > self.due_date_as_datetime

    @property
    def due_date_as_datetime(self) -> datetime:
        return datetime.utcnow() + timedelta(days=self.due_days)


@dataclass
class OnboardingPlan:
    """Employee onboarding plan."""
    plan_id: str
    employee_id: str
    start_date: datetime
    status: OnboardingStatus = OnboardingStatus.NOT_STARTED
    tasks: List[OnboardingTask] = field(default_factory=list)
    buddy_id: Optional[str] = None
    mentor_id: Optional[str] = None
    notes: str = ""

    @property
    def completion_pct(self) -> float:
        if not self.tasks:
            return 0.0
        completed = sum(1 for t in self.tasks if t.completed)
        return completed / len(self.tasks)

    @property
    def days_since_start(self) -> int:
        return (datetime.utcnow() - self.start_date).days

    @property
    def is_30_day_checkin_due(self) -> bool:
        return self.days_since_start >= 30

    @property
    def is_90_day_checkin_due(self) -> bool:
        return self.days_since_start >= 90


@dataclass
class OffboardingPlan:
    """Employee offboarding plan."""
    plan_id: str
    employee_id: str
    last_day: datetime
    status: OffboardingStatus = OffboardingStatus.NOT_STARTED
    reason: str = ""
    tasks: List[OnboardingTask] = field(default_factory=list)
    exit_interview: Optional[ExitInterview] = None
    final_pay_date: Optional[datetime] = None
    benefits_end_date: Optional[datetime] = None
    notes: str = ""

    @property
    def days_until_last_day(self) -> int:
        return max((self.last_day - datetime.utcnow()).days, 0)

    @property
    def completion_pct(self) -> float:
        if not self.tasks:
            return 0.0
        completed = sum(1 for t in self.tasks if t.completed)
        return completed / len(self.tasks)


@dataclass
class BenefitEnrollment:
    """Benefit enrollment record."""
    enrollment_id: str
    employee_id: str
    benefit_type: BenefitType
    plan_name: str
    coverage_start: datetime
    coverage_end: Optional[datetime] = None
    employee_contribution: float = 0.0
    employer_contribution: float = 0.0
    dependents: List[str] = field(default_factory=list)
    status: str = "active"

    @property
    def total_monthly_cost(self) -> float:
        return self.employee_contribution + self.employer_contribution


@dataclass
class AttritionRisk:
    """Employee attrition risk assessment."""
    employee_id: str
    risk_score: float
    risk_factors: List[str] = field(default_factory=list)
    retention_actions: List[str] = field(default_factory=list)
    assessed_date: datetime = field(default_factory=datetime.utcnow)
    confidence: float = 0.0

    @property
    def risk_level(self) -> str:
        if self.risk_score >= 0.7:
            return "critical"
        if self.risk_score >= 0.5:
            return "high"
        if self.risk_score >= 0.3:
            return "medium"
        return "low"


@dataclass
class HRConfig:
    """Configuration for the HR agent."""
    probation_days: int = 90
    review_cycle_months: int = 12
    default_vacation_days: int = 15
    default_sick_days: int = 10
    default_personal_days: int = 5
    max_carryover_days: int = 5
    salary_benchmark_percentile: int = 50
    engagement_survey_frequency_months: int = 6
    compliance_renewal_lead_days: int = 30
    training_overdue_warning_days: int = 7
    attrition_risk_threshold: float = 0.5
    attrition_lookback_days: int = 365
    attrition_weights: Dict[str, float] = field(default_factory=lambda: {
        "tenure": 0.15,
        "engagement": 0.20,
        "performance": 0.20,
        "compensation": 0.15,
        "manager_relationship": 0.10,
        "growth_opportunity": 0.10,
        "work_life_balance": 0.10,
    })


# ---------------------------------------------------------------------------
# Employee Manager
# ---------------------------------------------------------------------------

class EmployeeManager:
    """Employee record management and lifecycle tracking."""

    def __init__(self, config: Optional[HRConfig] = None) -> None:
        self.employees: Dict[str, Employee] = {}
        self._emp_counter = 0
        self.config = config or HRConfig()

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

    def update_employee(self, employee_id: str, **kwargs: Any) -> Optional[Employee]:
        if employee_id not in self.employees:
            return None
        emp = self.employees[employee_id]
        for key, value in kwargs.items():
            if hasattr(emp, key) and key not in ("employee_id", "hire_date"):
                setattr(emp, key, value)
        return emp

    def get_employee(self, employee_id: str) -> Optional[Employee]:
        return self.employees.get(employee_id)

    def get_by_department(self, department: Department) -> List[Employee]:
        return [e for e in self.employees.values() if e.department == department and e.is_active]

    def get_by_manager(self, manager_id: str) -> List[Employee]:
        return [e for e in self.employees.values() if e.manager_id == manager_id and e.is_active]

    def get_by_level(self, level: JobLevel) -> List[Employee]:
        return [e for e in self.employees.values() if e.job_level == level and e.is_active]

    def get_headcount(self) -> Dict[str, int]:
        counts: Dict[str, int] = defaultdict(int)
        for emp in self.employees.values():
            if emp.is_active:
                counts[emp.department.value] += 1
        return dict(counts)

    def get_headcount_by_level(self) -> Dict[str, int]:
        counts: Dict[str, int] = defaultdict(int)
        for emp in self.employees.values():
            if emp.is_active:
                counts[emp.job_level.value] += 1
        return dict(counts)

    def get_headcount_by_type(self) -> Dict[str, int]:
        counts: Dict[str, int] = defaultdict(int)
        for emp in self.employees.values():
            if emp.is_active:
                counts[emp.employment_type.value] += 1
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

    def get_salary_statistics(self) -> Dict[str, Any]:
        active = [e for e in self.employees.values() if e.is_active and e.salary > 0]
        if not active:
            return {"count": 0}
        salaries = [e.annual_salary for e in active]
        by_dept: Dict[str, List[float]] = defaultdict(list)
        for e in active:
            by_dept[e.department.value].append(e.annual_salary)
        dept_avgs = {d: statistics.mean(s) for d, s in by_dept.items()}
        return {
            "count": len(salaries),
            "mean": round(statistics.mean(salaries), 2),
            "median": round(statistics.median(salaries), 2),
            "min": round(min(salaries), 2),
            "max": round(max(salaries), 2),
            "stdev": round(statistics.stdev(salaries), 2) if len(salaries) > 1 else 0,
            "department_averages": dept_avgs,
            "total_payroll_annual": round(sum(salaries), 2),
        }

    def search(self, query: str) -> List[Employee]:
        q = query.lower()
        return [
            e for e in self.employees.values()
            if q in e.full_name.lower() or q in e.email.lower() or q in e.job_title.lower()
        ]

    def get_active_count(self) -> int:
        return sum(1 for e in self.employees.values() if e.is_active)

    def get_attrition_rate(self, lookback_days: int = 365) -> float:
        cutoff = datetime.utcnow() - timedelta(days=lookback_days)
        terminated = sum(
            1 for e in self.employees.values()
            if e.termination_date and e.termination_date >= cutoff
        )
        avg_headcount = self.get_active_count() + terminated / 2
        return (terminated / avg_headcount * 100) if avg_headcount > 0 else 0.0

    def get_diversity_metrics(self) -> Dict[str, Any]:
        active = [e for e in self.employees.values() if e.is_active]
        if not active:
            return {}
        gender_dist: Dict[str, int] = defaultdict(int)
        ethnicity_dist: Dict[str, int] = defaultdict(int)
        for e in active:
            gender_dist[e.gender or "unspecified"] += 1
            ethnicity_dist[e.ethnicity or "unspecified"] += 1
        total = len(active)
        return {
            "gender_distribution": {k: {"count": v, "pct": round(v / total * 100, 1)} for k, v in gender_dist.items()},
            "ethnicity_distribution": {k: {"count": v, "pct": round(v / total * 100, 1)} for k, v in ethnicity_dist.items()},
        }


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
        salary_range: Tuple[float, float] = (0, 0),
        headcount: int = 1,
        requisition_id: Optional[str] = None,
    ) -> str:
        opening_id = requisition_id or f"JOB-{len(self.job_openings) + 1:04d}"
        self.job_openings[opening_id] = {
            "position": position,
            "department": department.value,
            "description": description,
            "salary_range": salary_range,
            "status": "open",
            "created": datetime.utcnow(),
            "headcount": headcount,
            "filled": 0,
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

    def record_offer(self, candidate_id: str, amount: float, expiry_days: int = 7) -> bool:
        if candidate_id not in self.candidates:
            return False
        cand = self.candidates[candidate_id]
        cand.stage = CandidateStage.OFFER
        cand.offer_amount = amount
        cand.offer_date = datetime.utcnow()
        cand.offer_expiry = datetime.utcnow() + timedelta(days=expiry_days)
        return True

    def get_pipeline(self, position: Optional[str] = None) -> Dict[str, List[Candidate]]:
        pipeline: Dict[str, List[Candidate]] = defaultdict(list)
        for cand in self.candidates.values():
            if position and cand.position_applied != position:
                continue
            if cand.is_active:
                pipeline[cand.stage.value].append(cand)
        return dict(pipeline)

    def get_candidates_by_source(self) -> Dict[str, int]:
        counts: Dict[str, int] = defaultdict(int)
        for c in self.candidates.values():
            counts[c.source or "unknown"] += 1
        return dict(counts)

    def get_avg_days_per_stage(self) -> Dict[str, float]:
        stage_days: Dict[str, List[float]] = defaultdict(list)
        for c in self.candidates.values():
            if c.stage in (CandidateStage.REJECTED, CandidateStage.WITHDRAWN):
                continue
            stage_days[c.stage.value].append(c.days_in_pipeline)
        return {stage: round(statistics.mean(days), 1) for stage, days in stage_days.items()}

    def get_metrics(self) -> RecruitmentMetrics:
        active = [c for c in self.candidates.values() if c.is_active]
        hired = [c for c in self.candidates.values() if c.stage == CandidateStage.HIRED]
        offered = [c for c in self.candidates.values() if c.stage == CandidateStage.OFFER]
        source_counts = defaultdict(int)
        for c in self.candidates.values():
            source_counts[c.source] += 1
        avg_days = statistics.mean([c.days_in_pipeline for c in hired]) if hired else 0
        total = len(self.candidates)
        return RecruitmentMetrics(
            total_applicants=total,
            screened=sum(1 for c in active if c.stage != CandidateStage.APPLIED),
            interviewed=sum(1 for c in active if c.stage in (
                CandidateStage.PHONE_INTERVIEW, CandidateStage.TECHNICAL_INTERVIEW,
                CandidateStage.ON_SITE, CandidateStage.FINAL_INTERVIEW)),
            offered=sum(1 for c in active if c.stage == CandidateStage.OFFER),
            hired=len(hired),
            avg_time_to_fill_days=avg_days,
            source_breakdown=dict(source_counts),
            offer_acceptance_rate=len(hired) / max(len(hired) + len(offered), 1),
            recruitment_funnel_conversion={
                "applied_to_screened": sum(1 for c in self.candidates.values() if c.stage != CandidateStage.APPLIED) / max(total, 1),
                "screened_to_interviewed": sum(1 for c in active if c.stage in (CandidateStage.PHONE_INTERVIEW, CandidateStage.TECHNICAL_INTERVIEW, CandidateStage.ON_SITE, CandidateStage.FINAL_INTERVIEW)) / max(sum(1 for c in self.candidates.values() if c.stage != CandidateStage.APPLIED), 1),
                "interviewed_to_offered": sum(1 for c in active if c.stage == CandidateStage.OFFER) / max(sum(1 for c in active if c.stage in (CandidateStage.PHONE_INTERVIEW, CandidateStage.TECHNICAL_INTERVIEW, CandidateStage.ON_SITE, CandidateStage.FINAL_INTERVIEW)), 1),
                "offered_to_hired": len(hired) / max(len(hired) + len(offered), 1),
            },
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
        goal.updated_at = datetime.utcnow()
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

    def get_active_goals(self, employee_id: str) -> List[Goal]:
        return [g for g in self.goals.values() if g.employee_id == employee_id and g.status == GoalStatus.IN_PROGRESS]

    def get_overdue_goals(self) -> List[Goal]:
        return [g for g in self.goals.values() if g.is_overdue]

    def get_latest_review(self, employee_id: str) -> Optional[PerformanceReview]:
        reviews = self.get_employee_reviews(employee_id)
        return reviews[0] if reviews else None

    def performance_summary(self, employee_id: str) -> Dict[str, Any]:
        reviews = self.get_employee_reviews(employee_id)
        goals = self.get_employee_goals(employee_id)
        latest = reviews[0] if reviews else None
        ratings = [r.overall_rating for r in reviews if r.overall_rating]
        avg_rating = statistics.mean(ratings) if ratings else 0
        completed_goals = sum(1 for g in goals if g.status == GoalStatus.COMPLETED)
        return {
            "employee_id": employee_id,
            "total_reviews": len(reviews),
            "avg_rating": avg_rating,
            "latest_rating": latest.overall_rating.value if latest and latest.overall_rating else None,
            "total_goals": len(goals),
            "completed_goals": completed_goals,
            "active_goals": sum(1 for g in goals if g.status == GoalStatus.IN_PROGRESS),
            "overdue_goals": sum(1 for g in goals if g.is_overdue),
            "goal_completion_rate": completed_goals / len(goals) if goals else 0,
            "promotion_recommended": latest.promotion_recommended if latest else False,
            "360_score": latest.weighted_360_score if latest else None,
        }

    def team_performance_summary(self, manager_id: str) -> Dict[str, Any]:
        direct_reports = [g.employee_id for g in self.goals.values() if g.employee_id]
        summaries = [self.performance_summary(eid) for eid in set(direct_reports)]
        if not summaries:
            return {"team_size": 0}
        ratings = [s["avg_rating"] for s in summaries if s["avg_rating"] > 0]
        return {
            "manager_id": manager_id,
            "team_size": len(summaries),
            "avg_team_rating": round(statistics.mean(ratings), 2) if ratings else 0,
            "total_goals": sum(s["total_goals"] for s in summaries),
            "overall_goal_completion": round(statistics.mean([s["goal_completion_rate"] for s in summaries]), 2),
            "promotions_recommended": sum(1 for s in summaries if s["promotion_recommended"]),
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
            "total_employees_analyzed": sum(len(v) for v in by_title.values()),
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
            "ratio": round(ratio, 3),
            "above_market": ratio > 1.0,
            "percentile_position": self._estimate_percentile(ratio),
        }

    def compensation_change_history(self, employee_id: str) -> Dict[str, Any]:
        records = self.get_comp_history(employee_id)
        if len(records) < 2:
            return {"employee_id": employee_id, "changes": [], "avg_increase_pct": 0}
        changes = []
        for i in range(1, len(records)):
            prev = records[i - 1].annual_amount
            curr = records[i].annual_amount
            pct = ((curr - prev) / prev * 100) if prev > 0 else 0
            changes.append({
                "from": prev,
                "to": curr,
                "change": curr - prev,
                "pct_change": round(pct, 2),
                "reason": records[i].reason,
                "date": records[i].effective_date.isoformat(),
            })
        avg_increase = statistics.mean([c["pct_change"] for c in changes]) if changes else 0
        return {
            "employee_id": employee_id,
            "total_changes": len(changes),
            "changes": changes,
            "avg_increase_pct": round(avg_increase, 2),
        }

    def _estimate_percentile(self, ratio: float) -> int:
        if ratio >= 1.2:
            return 90
        if ratio >= 1.1:
            return 75
        if ratio >= 1.0:
            return 50
        if ratio >= 0.9:
            return 25
        return 10


# ---------------------------------------------------------------------------
# Engagement Analyzer
# ---------------------------------------------------------------------------

class EngagementAnalyzer:
    """Employee engagement survey and analytics."""

    def __init__(self) -> None:
        self.surveys: Dict[str, EngagementSurvey] = {}
        self._survey_counter = 0

    def create_survey(self, title: str, questions: List[Dict[str, Any]],
                      target_participants: int = 0) -> EngagementSurvey:
        self._survey_counter += 1
        survey = EngagementSurvey(
            survey_id=f"SRV-{self._survey_counter:04d}",
            title=title,
            questions=questions,
            target_participants=target_participants,
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
            "response_rate": round(survey.response_rate * 100, 1),
            "avg_score": round(survey.avg_score, 2),
            "nps_score": survey.nps_score,
            "questions": len(survey.questions),
            "question_averages": {k: round(v, 2) for k, v in survey.question_averages.items()},
        }

    def analyze_department_engagement(
        self, survey_id: str, employees: Dict[str, Employee]
    ) -> Dict[str, Dict[str, float]]:
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
        return {
            dept: {
                "avg_score": round(statistics.mean(scores), 2),
                "response_count": len(scores),
                "min": round(min(scores), 2),
                "max": round(max(scores), 2),
            }
            for dept, scores in dept_scores.items()
        }

    def engagement_trends(self) -> List[Dict[str, Any]]:
        return sorted([
            {
                "survey_id": s.survey_id,
                "title": s.title,
                "date": s.created_date.isoformat(),
                "responses": len(s.responses),
                "avg_score": round(s.avg_score, 2),
                "response_rate": round(s.response_rate * 100, 1),
            }
            for s in self.surveys.values()
        ], key=lambda x: x["date"], reverse=True)


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

    def cancel_request(self, request_id: str) -> bool:
        if request_id not in self.requests:
            return False
        req = self.requests[request_id]
        if req.status == LeaveStatus.APPROVED:
            key = f"{req.employee_id}-{req.start_date.year}"
            if key in self.balances:
                self.balances[key].used[req.leave_type.value] = max(
                    0, self.balances[key].used.get(req.leave_type.value, 0) - req.total_days
                )
        req.status = LeaveStatus.CANCELLED
        return True

    def get_pending_requests(self) -> List[LeaveRequest]:
        return [r for r in self.requests.values() if r.is_pending]

    def get_employee_requests(self, employee_id: str) -> List[LeaveRequest]:
        return sorted(
            [r for r in self.requests.values() if r.employee_id == employee_id],
            key=lambda r: r.start_date, reverse=True
        )

    def get_current_leave(self) -> List[LeaveRequest]:
        return [r for r in self.requests.values() if r.is_currently_active]

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
            "approved": sum(1 for r in self.requests.values() if r.is_approved),
            "denied": sum(1 for r in self.requests.values() if r.status == LeaveStatus.DENIED),
            "approved_days": dict(by_type),
        }

    def team_leave_calendar(self, manager_id: str, employees: Dict[str, Employee]) -> List[Dict[str, Any]]:
        team_ids = {e.employee_id for e in employees.values() if e.manager_id == manager_id and e.is_active}
        return [
            {
                "employee_id": r.employee_id,
                "employee_name": employees[r.employee_id].full_name if r.employee_id in employees else "Unknown",
                "leave_type": r.leave_type.value,
                "start_date": r.start_date.isoformat(),
                "end_date": r.end_date.isoformat(),
                "days": r.total_days,
                "status": r.status.value,
            }
            for r in self.requests.values()
            if r.employee_id in team_ids and r.is_approved
        ]


# ---------------------------------------------------------------------------
# Compliance Tracker
# ---------------------------------------------------------------------------

class ComplianceTracker:
    """Compliance requirement tracking and reporting."""

    def __init__(self) -> None:
        self.items: Dict[str, ComplianceItem] = {}
        self._item_counter = 0

    def add_requirement(self, employee_id: str, requirement: str, due_date: Optional[datetime] = None,
                        expiration: Optional[datetime] = None, category: str = "general") -> ComplianceItem:
        self._item_counter += 1
        item = ComplianceItem(
            item_id=f"COMP-{self._item_counter:05d}",
            employee_id=employee_id,
            requirement=requirement,
            due_date=due_date,
            expiration_date=expiration,
            category=category,
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

    def get_overdue(self) -> List[ComplianceItem]:
        return [i for i in self.items.values() if i.is_overdue]

    def get_needing_renewal(self) -> List[ComplianceItem]:
        return [i for i in self.items.values() if i.needs_renewal]

    def compliance_by_category(self) -> Dict[str, Dict[str, int]]:
        by_cat: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        for item in self.items.values():
            by_cat[item.category][item.status.value] += 1
        return {cat: dict(counts) for cat, counts in by_cat.items()}

    def compliance_report(self) -> Dict[str, Any]:
        by_status = defaultdict(int)
        for item in self.items.values():
            by_status[item.status.value] += 1
        return {
            "total": len(self.items),
            "by_status": dict(by_status),
            "expiring_soon": len(self.get_expiring(30)),
            "non_compliant": len(self.get_non_compliant()),
            "overdue": len(self.get_overdue()),
            "needs_renewal": len(self.get_needing_renewal()),
            "compliance_rate": round(
                by_status.get("compliant", 0) / max(len(self.items), 1) * 100, 1
            ),
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

    def create_program(self, name: str, training_type: str, duration_hours: float,
                       provider: str = "", required: bool = True) -> str:
        prog_id = f"TRP-{len(self.programs) + 1:04d}"
        self.programs[prog_id] = {
            "name": name,
            "type": training_type,
            "duration_hours": duration_hours,
            "provider": provider,
            "required": required,
        }
        return prog_id

    def assign_training(self, employee_id: str, training_name: str,
                        due_date: Optional[datetime] = None,
                        required: bool = True) -> TrainingRecord:
        self._rec_counter += 1
        record = TrainingRecord(
            record_id=f"TR-{self._rec_counter:05d}",
            employee_id=employee_id,
            training_name=training_name,
            due_date=due_date,
            required=required,
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

    def get_required_incomplete(self) -> List[TrainingRecord]:
        return [r for r in self.records.values() if r.required and not r.is_completed]

    def training_completion_rate(self) -> Dict[str, Any]:
        total = len(self.records)
        completed = sum(1 for r in self.records.values() if r.is_completed)
        overdue = len(self.get_overdue())
        required_total = sum(1 for r in self.records.values() if r.required)
        required_completed = sum(1 for r in self.records.values() if r.required and r.is_completed)
        scores = [r.score for r in self.records.values() if r.score is not None]
        return {
            "total_assigned": total,
            "completed": completed,
            "overdue": overdue,
            "completion_rate": round(completed / total * 100, 1) if total > 0 else 0,
            "required_completion_rate": round(required_completed / required_total * 100, 1) if required_total > 0 else 0,
            "avg_score": round(statistics.mean(scores), 1) if scores else None,
            "total_hours": round(sum(r.duration_hours for r in self.records.values() if r.is_completed), 1),
        }

    def employee_training_summary(self, employee_id: str) -> Dict[str, Any]:
        records = self.get_employee_training(employee_id)
        completed = [r for r in records if r.is_completed]
        scores = [r.score for r in completed if r.score is not None]
        return {
            "employee_id": employee_id,
            "total_assigned": len(records),
            "completed": len(completed),
            "in_progress": sum(1 for r in records if r.status == TrainingStatus.IN_PROGRESS),
            "overdue": sum(1 for r in records if r.is_overdue),
            "avg_score": round(statistics.mean(scores), 1) if scores else None,
            "total_hours_completed": round(sum(r.duration_hours for r in completed), 1),
        }


# ---------------------------------------------------------------------------
# Org Chart Manager
# ---------------------------------------------------------------------------

class OrgChartManager:
    """Organizational structure management."""

    def __init__(self) -> None:
        self.entries: Dict[str, OrgChart] = {}

    def add_employee(self, employee_id: str, name: str, title: str,
                     department: Department, level: JobLevel,
                     manager_id: Optional[str] = None) -> OrgChart:
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

    def get_span_of_control(self) -> Dict[str, int]:
        return {eid: len(e.direct_reports) for eid, e in self.entries.items() if e.direct_reports}

    def get_org_chart_flat(self) -> List[Dict[str, Any]]:
        return [
            {
                "employee_id": e.employee_id,
                "name": e.name,
                "title": e.title,
                "department": e.department.value,
                "level": e.level.value,
                "manager_id": e.manager_id,
                "direct_report_count": len(e.direct_reports),
            }
            for e in self.entries.values()
        ]


# ---------------------------------------------------------------------------
# Onboarding Manager
# ---------------------------------------------------------------------------

class OnboardingManager:
    """Employee onboarding workflow management."""

    def __init__(self) -> None:
        self.plans: Dict[str, OnboardingPlan] = {}
        self._plan_counter = 0

    def create_plan(self, employee_id: str, start_date: datetime,
                    buddy_id: Optional[str] = None,
                    mentor_id: Optional[str] = None) -> OnboardingPlan:
        self._plan_counter += 1
        plan = OnboardingPlan(
            plan_id=f"ONB-{self._plan_counter:04d}",
            employee_id=employee_id,
            start_date=start_date,
            buddy_id=buddy_id,
            mentor_id=mentor_id,
        )
        self.plans[plan.plan_id] = plan
        return plan

    def add_task(self, plan_id: str, title: str, description: str,
                 assigned_to: str, due_days: int,
                 category: str = "general") -> Optional[OnboardingTask]:
        if plan_id not in self.plans:
            return None
        task = OnboardingTask(
            task_id=f"TSK-{len(self.plans[plan_id].tasks) + 1:03d}",
            title=title,
            description=description,
            assigned_to=assigned_to,
            due_days=due_days,
            category=category,
        )
        self.plans[plan_id].tasks.append(task)
        return task

    def complete_task(self, plan_id: str, task_id: str) -> bool:
        if plan_id not in self.plans:
            return False
        plan = self.plans[plan_id]
        for task in plan.tasks:
            if task.task_id == task_id:
                task.completed = True
                task.completed_date = datetime.utcnow()
                if all(t.completed for t in plan.tasks):
                    plan.status = OnboardingStatus.COMPLETED
                return True
        return False

    def get_plan(self, plan_id: str) -> Optional[OnboardingPlan]:
        return self.plans.get(plan_id)

    def get_employee_plan(self, employee_id: str) -> Optional[OnboardingPlan]:
        for plan in self.plans.values():
            if plan.employee_id == employee_id:
                return plan
        return None

    def onboarding_progress_report(self) -> Dict[str, Any]:
        total = len(self.plans)
        completed = sum(1 for p in self.plans.values() if p.status == OnboardingStatus.COMPLETED)
        in_progress = sum(1 for p in self.plans.values() if p.status == OnboardingStatus.IN_PROGRESS)
        overdue = sum(1 for p in self.plans.values()
                      if p.status != OnboardingStatus.COMPLETED and p.days_since_start > 90)
        return {
            "total_plans": total,
            "completed": completed,
            "in_progress": in_progress,
            "overdue": overdue,
            "completion_rate": round(completed / total * 100, 1) if total > 0 else 0,
            "avg_completion_days": self._avg_completion_days(),
        }

    def _avg_completion_days(self) -> Optional[float]:
        completed = [p for p in self.plans.values() if p.status == OnboardingStatus.COMPLETED]
        if not completed:
            return None
        days = [p.days_since_start for p in completed]
        return round(statistics.mean(days), 1)


# ---------------------------------------------------------------------------
# Offboarding Manager
# ---------------------------------------------------------------------------

class OffboardingManager:
    """Employee offboarding workflow management."""

    def __init__(self) -> None:
        self.plans: Dict[str, OffboardingPlan] = {}
        self._plan_counter = 0

    def create_plan(self, employee_id: str, last_day: datetime,
                    reason: str = "") -> OffboardingPlan:
        self._plan_counter += 1
        plan = OffboardingPlan(
            plan_id=f"OBF-{self._plan_counter:04d}",
            employee_id=employee_id,
            last_day=last_day,
            reason=reason,
        )
        self.plans[plan.plan_id] = plan
        return plan

    def add_task(self, plan_id: str, title: str, description: str,
                 assigned_to: str, due_days: int) -> Optional[OnboardingTask]:
        if plan_id not in self.plans:
            return None
        task = OnboardingTask(
            task_id=f"TSK-{len(self.plans[plan_id].tasks) + 1:03d}",
            title=title,
            description=description,
            assigned_to=assigned_to,
            due_days=due_days,
        )
        self.plans[plan_id].tasks.append(task)
        return task

    def complete_task(self, plan_id: str, task_id: str) -> bool:
        if plan_id not in self.plans:
            return False
        plan = self.plans[plan_id]
        for task in plan.tasks:
            if task.task_id == task_id:
                task.completed = True
                task.completed_date = datetime.utcnow()
                return True
        return False

    def get_plan(self, plan_id: str) -> Optional[OffboardingPlan]:
        return self.plans.get(plan_id)

    def offboarding_summary(self) -> Dict[str, Any]:
        total = len(self.plans)
        completed = sum(1 for p in self.plans.values() if p.status == OffboardingStatus.COMPLETED)
        return {
            "total_offboardings": total,
            "completed": completed,
            "in_progress": total - completed,
        }


# ---------------------------------------------------------------------------
# Benefits Manager
# ---------------------------------------------------------------------------

class BenefitsManager:
    """Benefits administration and enrollment management."""

    def __init__(self) -> None:
        self.enrollments: Dict[str, BenefitEnrollment] = {}
        self._enroll_counter = 0

    def enroll(self, employee_id: str, benefit_type: BenefitType, plan_name: str,
               coverage_start: datetime, employee_contribution: float = 0,
               employer_contribution: float = 0,
               dependents: Optional[List[str]] = None) -> BenefitEnrollment:
        self._enroll_counter += 1
        enrollment = BenefitEnrollment(
            enrollment_id=f"BEN-{self._enroll_counter:05d}",
            employee_id=employee_id,
            benefit_type=benefit_type,
            plan_name=plan_name,
            coverage_start=coverage_start,
            employee_contribution=employee_contribution,
            employer_contribution=employer_contribution,
            dependents=dependents or [],
        )
        self.enrollments[enrollment.enrollment_id] = enrollment
        return enrollment

    def get_employee_benefits(self, employee_id: str) -> List[BenefitEnrollment]:
        return [e for e in self.enrollments.values() if e.employee_id == employee_id and e.status == "active"]

    def total_employer_cost(self) -> float:
        return sum(e.employer_contribution * 12 for e in self.enrollments.values() if e.status == "active")

    def benefits_summary_by_type(self) -> Dict[str, Dict[str, Any]]:
        by_type: Dict[str, Dict[str, Any]] = {}
        for benefit_type in BenefitType:
            enrollments = [e for e in self.enrollments.values() if e.benefit_type == benefit_type and e.status == "active"]
            if enrollments:
                by_type[benefit_type.value] = {
                    "enrolled_count": len(enrollments),
                    "total_employer_cost": round(sum(e.employer_contribution * 12 for e in enrollments), 2),
                    "total_employee_cost": round(sum(e.employee_contribution * 12 for e in enrollments), 2),
                }
        return by_type


# ---------------------------------------------------------------------------
# Attrition Analyzer
# ---------------------------------------------------------------------------

class AttritionAnalyzer:
    """Attrition risk analysis and retention modeling."""

    def __init__(self, config: Optional[HRConfig] = None) -> None:
        self.config = config or HRConfig()
        self.risk_assessments: Dict[str, AttritionRisk] = {}
        self.exit_interviews: Dict[str, ExitInterview] = {}

    def assess_attrition_risk(self, employee: Employee) -> AttritionRisk:
        risk_factors = []
        retention_actions = []
        risk_score = 0.0

        if employee.tenure_years < 1:
            risk_score += self.config.attrition_weights["tenure"] * 0.7
            risk_factors.append("Early tenure (< 1 year)")
        elif employee.tenure_years > 5:
            risk_score += self.config.attrition_weights["tenure"] * 0.3
            risk_factors.append("Long tenure may seek new challenges")

        if employee.engagement_score < 3.0:
            risk_score += self.config.attrition_weights["engagement"] * 0.8
            risk_factors.append("Low engagement score")
            retention_actions.append("Schedule engagement conversation")
        elif employee.engagement_score > 4.0:
            risk_score += self.config.attrition_weights["engagement"] * 0.1

        if employee.performance_score < 2.5:
            risk_score += self.config.attrition_weights["performance"] * 0.6
            risk_factors.append("Below expectations performance")
        elif employee.performance_score > 4.0:
            risk_score += self.config.attrition_weights["performance"] * 0.1
            retention_actions.append("High performer — discuss career path")

        if employee.salary_competitiveness_ratio < 0.9:
            risk_score += self.config.attrition_weights["compensation"] * 0.9
            risk_factors.append("Below market compensation")
            retention_actions.append("Review compensation against market")
        elif employee.salary_competitiveness_ratio > 1.1:
            risk_score += self.config.attrition_weights["compensation"] * 0.05

        if not employee.remote_work_eligible and employee.office_days_per_week >= 5:
            risk_score += self.config.attrition_weights["work_life_balance"] * 0.5
            risk_factors.append("No remote work flexibility")

        confidence = min(0.9, 0.5 + (len(risk_factors) * 0.05))

        if risk_score < 0.2:
            retention_actions.append("Continue monitoring")
        elif risk_score < 0.4:
            retention_actions.append("Schedule skip-level meeting")
        else:
            retention_actions.append("Immediate retention intervention")
            retention_actions.append("Compensation review")

        assessment = AttritionRisk(
            employee_id=employee.employee_id,
            risk_score=round(min(risk_score, 1.0), 3),
            risk_factors=risk_factors,
            retention_actions=retention_actions,
            confidence=round(confidence, 3),
        )
        self.risk_assessments[employee.employee_id] = assessment
        return assessment

    def get_high_risk_employees(self, threshold: float = 0.5) -> List[AttritionRisk]:
        return sorted(
            [r for r in self.risk_assessments.values() if r.risk_score >= threshold],
            key=lambda r: r.risk_score, reverse=True
        )

    def attrition_summary(self) -> Dict[str, Any]:
        assessments = list(self.risk_assessments.values())
        if not assessments:
            return {"total_assessed": 0}
        risk_levels = defaultdict(int)
        for a in assessments:
            risk_levels[a.risk_level] += 1
        return {
            "total_assessed": len(assessments),
            "avg_risk_score": round(statistics.mean(a.risk_score for a in assessments), 3),
            "risk_distribution": dict(risk_levels),
            "high_risk_count": sum(1 for a in assessments if a.risk_score >= 0.5),
            "critical_risk_count": sum(1 for a in assessments if a.risk_score >= 0.7),
        }

    def record_exit_interview(self, interview: ExitInterview) -> None:
        self.exit_interviews[interview.interview_id] = interview

    def exit_reason_analysis(self) -> Dict[str, Any]:
        interviews = list(self.exit_interviews.values())
        if not interviews:
            return {"total": 0}
        reasons = defaultdict(int)
        for i in interviews:
            reasons[i.reason_for_leaving or "not_specified"] += 1
        voluntary = sum(1 for i in interviews if i.voluntary)
        avg_satisfaction = statistics.mean(i.overall_satisfaction for i in interviews if i.overall_satisfaction > 0)
        return {
            "total_exits": len(interviews),
            "voluntary": voluntary,
            "involuntary": len(interviews) - voluntary,
            "reasons": dict(reasons),
            "avg_exit_satisfaction": round(avg_satisfaction, 2) if avg_satisfaction else 0,
            "would_return_pct": round(sum(1 for i in interviews if i.would_return) / len(interviews) * 100, 1),
            "rehire_eligible_pct": round(sum(1 for i in interviews if i.rehire_eligible) / len(interviews) * 100, 1),
        }


# ---------------------------------------------------------------------------
# HR Agent (Orchestrator)
# ---------------------------------------------------------------------------

class HRAgent:
    """Orchestrates all HR sub-components."""

    def __init__(self, config: Optional[HRConfig] = None) -> None:
        self.config = config or HRConfig()
        self.employees = EmployeeManager(self.config)
        self.recruitment = RecruitmentPipeline()
        self.performance = PerformanceManager()
        self.compensation = CompensationAnalyzer()
        self.engagement = EngagementAnalyzer()
        self.leave = LeaveManager()
        self.compliance = ComplianceTracker()
        self.training = TrainingManager()
        self.org_chart = OrgChartManager()
        self.onboarding = OnboardingManager()
        self.offboarding = OffboardingManager()
        self.benefits = BenefitsManager()
        self.attrition = AttritionAnalyzer(self.config)
        logger.info("HRAgent initialized")

    def full_status(self) -> Dict[str, Any]:
        return {
            "headcount": self.employees.get_active_count(),
            "headcount_by_department": self.employees.get_headcount(),
            "recruitment": self.recruitment.get_metrics().__dict__,
            "performance": {
                "total_reviews": len(self.performance.reviews),
                "total_goals": len(self.performance.goals),
                "overdue_goals": len(self.performance.get_overdue_goals()),
            },
            "compensation": self.compensation.calculate_pay_equity(),
            "engagement_surveys": len(self.engagement.surveys),
            "leave_summary": self.leave.get_leave_summary(),
            "compliance": self.compliance.compliance_report(),
            "training": self.training.training_completion_rate(),
            "attrition_rate": self.employees.get_attrition_rate(),
            "attrition_risk": self.attrition.attrition_summary(),
            "onboarding": self.onboarding.onboarding_progress_report(),
            "offboarding": self.offboarding.offboarding_summary(),
            "salary_stats": self.employees.get_salary_statistics(),
        }

    def run(self) -> Dict[str, Any]:
        logger.info("HRAgent run starting")
        status = self.full_status()
        logger.info("HRAgent run complete")
        return status


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------

def main() -> None:
    logging.basicConfig(level=logging.INFO)
    print("=" * 60)
    print("HR Agent — Comprehensive Demo")
    print("=" * 60)

    agent = HRAgent()

    emp1 = agent.employees.hire_employee(
        first_name="Alice", last_name="Johnson", email="alice@co.com",
        department=Department.ENGINEERING, job_title="Senior Engineer",
        job_level=JobLevel.SENIOR, salary=120000,
        gender="female", ethnicity="caucasian",
        performance_score=4.2, engagement_score=4.5,
        salary_competitiveness_ratio=1.05,
    )
    emp2 = agent.employees.hire_employee(
        first_name="Bob", last_name="Smith", email="bob@co.com",
        department=Department.ENGINEERING, job_title="Junior Engineer",
        job_level=JobLevel.JUNIOR, salary=80000, manager_id=emp1.employee_id,
        gender="male", ethnicity="asian", performance_score=3.5,
        engagement_score=3.8, salary_competitiveness_ratio=0.95,
    )
    emp3 = agent.employees.hire_employee(
        first_name="Carol", last_name="Williams", email="carol@co.com",
        department=Department.HR, job_title="HR Manager",
        job_level=JobLevel.LEAD, salary=110000,
        gender="female", ethnicity="african_american",
        performance_score=4.8, engagement_score=4.9,
    )

    print(f"\nHeadcount: {agent.employees.get_headcount()}")
    print(f"Tenure distribution: {agent.employees.get_tenure_distribution()}")
    print(f"Salary stats: {agent.employees.get_salary_statistics()}")

    opening = agent.recruitment.create_opening("Backend Engineer", Department.ENGINEERING)
    cand1 = agent.recruitment.add_candidate(first_name="Dave", last_name="Brown", email="dave@email.com", position_applied="Backend Engineer", source="linkedin")
    cand2 = agent.recruitment.add_candidate(first_name="Eve", last_name="Davis", email="eve@email.com", position_applied="Backend Engineer", source="referral")
    agent.recruitment.advance_stage(cand1.candidate_id, CandidateStage.PHONE_INTERVIEW, "Good phone screen")
    agent.recruitment.advance_stage(cand1.candidate_id, CandidateStage.TECHNICAL_INTERVIEW)
    agent.recruitment.record_offer(cand1.candidate_id, 130000)
    metrics = agent.recruitment.get_metrics()
    print(f"\nRecruitment: {metrics.total_applicants} applicants, {metrics.hired} hired")
    print(f"Funnel conversion: {metrics.recruitment_funnel_conversion}")

    review = agent.performance.create_review(
        employee_id=emp1.employee_id, reviewer_id=emp3.employee_id,
        overall_rating=ReviewRating.EXCEEDS_EXPECTATIONS, goals_met=4, goals_total=5,
        self_assessment_score=4.0, peer_feedback_score=4.3, manager_feedback_score=4.5,
    )
    goal = agent.performance.add_goal(employee_id=emp1.employee_id, title="Complete project X", status=GoalStatus.IN_PROGRESS, completion_pct=75)
    summary = agent.performance.performance_summary(emp1.employee_id)
    print(f"\nPerformance: avg rating={summary['avg_rating']}, goals={summary['completed_goals']}/{summary['total_goals']}")
    print(f"360 score: {summary['360_score']}")

    agent.compensation.add_record(CompensationRecord("CR1", emp1.employee_id, amount=120000, reason="Senior Engineer"))
    agent.compensation.add_record(CompensationRecord("CR2", emp2.employee_id, amount=80000, reason="Junior Engineer"))
    agent.compensation.set_benchmark("Senior Engineer", 130000)
    equity = agent.compensation.calculate_pay_equity()
    print(f"\nCompensation: {equity['titles_analyzed']} titles, {len(equity['equity_issues'])} equity issues")

    agent.leave.set_balance(emp1.employee_id, 2025, {"vacation": 15, "sick": 10, "personal": 5})
    req = agent.leave.submit_request(emp1.employee_id, LeaveType.VACATION, datetime(2025, 8, 1), datetime(2025, 8, 5), "Summer vacation")
    agent.leave.approve_request(req.request_id, emp3.employee_id)
    balance = agent.leave.get_employee_balance(emp1.employee_id, 2025)
    print(f"\nLeave: vacation remaining = {balance.remaining('vacation') if balance else 'N/A'}")

    agent.training.create_program("Security Awareness", "compliance", 2.0)
    tr = agent.training.assign_training(emp1.employee_id, "Security Awareness", datetime(2025, 9, 1))
    agent.training.complete_training(tr.record_id, score=95)
    rate = agent.training.training_completion_rate()
    print(f"\nTraining: {rate['completed']}/{rate['total_assigned']} completed ({rate['completion_rate']:.0f}%)")

    agent.compliance.add_requirement(emp1.employee_id, "Annual Security Training", expiration=datetime(2025, 12, 31))
    agent.compliance.add_requirement(emp2.employee_id, "Background Check")
    agent.compliance.update_status(list(agent.compliance.items.keys())[0], ComplianceStatus.COMPLIANT)
    report = agent.compliance.compliance_report()
    print(f"\nCompliance: {report['total']} items, {report['non_compliant']} non-compliant, {report['compliance_rate']}% compliance")

    agent.org_chart.add_employee(emp1.employee_id, emp1.full_name, "Senior Engineer", Department.ENGINEERING, JobLevel.SENIOR)
    agent.org_chart.add_employee(emp2.employee_id, emp2.full_name, "Junior Engineer", Department.ENGINEERING, JobLevel.JUNIOR, manager_id=emp1.employee_id)
    agent.org_chart.add_employee(emp3.employee_id, emp3.full_name, "HR Manager", Department.HR, JobLevel.LEAD)
    tree = agent.org_chart.get_team_tree(emp1.employee_id)
    print(f"\nOrg Chart: {tree['name']} manages {len(tree['reports'])} reports")

    risk = agent.attrition.assess_attrition_risk(emp2)
    print(f"\nAttrition Risk for {emp2.full_name}: {risk.risk_level} (score={risk.risk_score})")
    print(f"  Factors: {risk.risk_factors}")
    print(f"  Actions: {risk.retention_actions}")

    onb = agent.onboarding.create_plan(emp2.employee_id, datetime.utcnow())
    agent.onboarding.add_task(onb.plan_id, "Complete I-9", "Fill out employment eligibility", "hr", 1, "paperwork")
    agent.onboarding.add_task(onb.plan_id, "Security Training", "Complete mandatory security training", "emp", 7, "compliance")
    progress = agent.onboarding.onboarding_progress_report()
    print(f"\nOnboarding: {progress}")

    print(f"\nFull status: {json.dumps(agent.run(), indent=2, default=str)[:500]}...")

    print("\n" + "=" * 60)
    print("HR Agent demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
