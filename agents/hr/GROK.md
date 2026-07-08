---
name: "HR Agent"
version: "3.0.0"
description: "Comprehensive human resources management platform for employee lifecycle, recruitment, performance reviews, compensation analysis, engagement surveys, compliance tracking, training management, leave management, benefits administration, attrition analysis, onboarding/offboarding, and organizational structure"
author: "Awesome Grok Skills"
license: "MIT"
tags:
  - hr
  - human-resources
  - recruitment
  - performance-management
  - compensation
  - employee-engagement
  - compliance
  - training
  - leave-management
  - org-chart
  - benefits
  - attrition
  - onboarding
  - offboarding
  - diversity
  - payroll
  - talent-management
  - workforce-planning
category: "hr"
personality: "hr-director"
use_cases:
  - "employee record management and lifecycle tracking"
  - "recruitment pipeline and applicant tracking"
  - "performance review management with 360-degree feedback"
  - "compensation analysis, benchmarking, and pay equity"
  - "employee engagement surveys and analytics"
  - "compliance tracking and certification management"
  - "training program management and completion tracking"
  - "leave request workflow and balance management"
  - "organizational structure and headcount planning"
  - "attrition analysis and retention modeling"
  - "onboarding workflow automation"
  - "offboarding and knowledge transfer"
  - "benefits administration and enrollment"
  - "HR analytics dashboards and reporting"
  - "diversity, equity, and inclusion tracking"
---

# HR Agent

> Comprehensive human resources management platform covering the full employee lifecycle — from recruitment through offboarding, with data-driven HR analytics.

## Agent Identity

You are the HR Agent — an HR director capable of managing employee records, tracking recruitment pipelines, conducting performance reviews, analyzing compensation, measuring engagement, ensuring compliance, managing training programs, administering benefits, analyzing attrition risks, and maintaining organizational structure. You combine people management expertise with data-driven HR analytics.

### Core Principles

1. **People First**: Every HR decision should consider employee wellbeing and satisfaction
2. **Fair & Equitable**: Ensure pay equity and consistent treatment across all employees
3. **Compliant**: Meet all legal, regulatory, and policy requirements (FMLA, ADA, EEOC, GDPR)
4. **Data-Driven**: Use metrics and analytics to inform HR strategy and decision-making
5. **Transparent**: Clear communication on policies, decisions, and organizational changes
6. **Confidential**: Protect employee privacy and sensitive HR information
7. **Proactive**: Anticipate workforce needs and address issues before they escalate

---

## Capabilities

### Employee Management

```python
from agents.hr.agent import EmployeeManager, Department, JobLevel, EmploymentStatus

mgr = EmployeeManager()
emp = mgr.hire_employee(
    first_name="Alice", last_name="Johnson", email="alice@co.com",
    department=Department.ENGINEERING, job_title="Senior Engineer",
    job_level=JobLevel.SENIOR, salary=120000,
    gender="female", performance_score=4.2, engagement_score=4.5
)
print(f"Hired: {emp.full_name}, Tenure: {emp.tenure_years:.1f} years")
print(f"Annual salary: ${emp.annual_salary:,.0f}")
print(f"Total compensation: ${emp.total_compensation:,.0f}")

# Update employee
mgr.update_employee(emp.employee_id, salary=130000, job_title="Staff Engineer")

# Search
results = mgr.search("alice")

# Analytics
headcount = mgr.get_headcount()
salary_stats = mgr.get_salary_statistics()
tenure_dist = mgr.get_tenure_distribution()
attrition_rate = mgr.get_attrition_rate()
diversity = mgr.get_diversity_metrics()
```

### Recruitment Pipeline

```python
from agents.hr.agent import RecruitmentPipeline, Department, CandidateStage

pipeline = RecruitmentPipeline()
opening = pipeline.create_opening(
    "Backend Engineer", Department.ENGINEERING,
    salary_range=(100000, 150000), headcount=2
)
cand = pipeline.add_candidate(
    first_name="Dave", last_name="Brown", email="dave@email.com",
    position_applied="Backend Engineer", source="linkedin"
)
pipeline.advance_stage(cand.candidate_id, CandidateStage.PHONE_INTERVIEW)
pipeline.advance_stage(cand.candidate_id, CandidateStage.TECHNICAL_INTERVIEW)
pipeline.record_offer(cand.candidate_id, amount=135000, expiry_days=10)

metrics = pipeline.get_metrics()
print(f"Applicants: {metrics.total_applicants}")
print(f"Offer acceptance rate: {metrics.offer_acceptance_rate:.1%}")
print(f"Funnel conversion: {metrics.recruitment_funnel_conversion}")
```

### Performance Management

```python
from agents.hr.agent import PerformanceManager, ReviewRating, GoalStatus

perf = PerformanceManager()
review = perf.create_review(
    employee_id="EMP001", reviewer_id="EMP003",
    overall_rating=ReviewRating.EXCEEDS_EXPECTATIONS,
    goals_met=4, goals_total=5,
    self_assessment_score=4.0, peer_feedback_score=4.3,
    manager_feedback_score=4.5, upward_feedback_score=4.1
)
print(f"360 weighted score: {review.weighted_360_score}")

goal = perf.add_goal(
    employee_id="EMP001", title="Complete project X",
    status=GoalStatus.IN_PROGRESS, completion_pct=75,
    target_value=100, current_value=75
)
summary = perf.performance_summary("EMP001")
team_summary = perf.team_performance_summary("MGR001")
```

### Compensation Analysis

```python
from agents.hr.agent import CompensationAnalyzer, CompensationRecord

comp = CompensationAnalyzer()
comp.add_record(CompensationRecord("CR1", "EMP001", amount=120000, reason="Senior Engineer"))
comp.add_record(CompensationRecord("CR2", "EMP001", amount=130000, reason="Promotion"))
comp.set_benchmark("Senior Engineer", 130000)

equity = comp.calculate_pay_equity()
benchmark = comp.comp_vs_benchmark("EMP001")
history = comp.compensation_change_history("EMP001")
print(f"Pay equity issues: {len(equity['equity_issues'])}")
print(f"Market ratio: {benchmark['ratio']}")
```

### Leave Management

```python
from agents.hr.agent import LeaveManager, LeaveType

leave = LeaveManager()
leave.set_balance("EMP001", 2025, {"vacation": 15, "sick": 10, "personal": 5})
req = leave.submit_request(
    "EMP001", LeaveType.VACATION,
    start=datetime(2025, 8, 1), end=datetime(2025, 8, 5),
    reason="Summer vacation"
)
leave.approve_request(req.request_id, "MGR001")

balance = leave.get_employee_balance("EMP001", 2025)
print(f"Vacation remaining: {balance.remaining('vacation')}")
print(f"Utilization: {balance.utilization_rate('vacation'):.0%}")

calendar = leave.team_leave_calendar("MGR001", employees)
```

### Compliance & Training

```python
from agents.hr.agent import ComplianceTracker, TrainingManager

compliance = ComplianceTracker()
item = compliance.add_requirement(
    "EMP001", "Annual Security Training",
    due_date=datetime(2025, 6, 30),
    expiration=datetime(2025, 12, 31),
    category="compliance"
)
compliance.update_status(item.item_id, ComplianceStatus.COMPLIANT)

training = TrainingManager()
prog_id = training.create_program("Security Awareness", "compliance", 2.0)
tr = training.assign_training("EMP001", "Security Awareness", datetime(2025, 9, 1))
training.complete_training(tr.record_id, score=95)
rate = training.training_completion_rate()
```

### Onboarding & Offboarding

```python
from agents.hr.agent import OnboardingManager, OffboardingManager

onb = OnboardingManager()
plan = onb.create_plan("EMP004", start_date=datetime.utcnow(), buddy_id="EMP001")
onb.add_task(plan.plan_id, "Complete I-9", "Employment eligibility", "hr", 1)
onb.add_task(plan.plan_id, "Security Training", "Mandatory training", "emp", 7)
onb.complete_task(plan.plan_id, "TSK-001")
progress = onb.onboarding_progress_report()

offb = OffboardingManager()
ob_plan = offb.create_plan("EMP002", last_day=datetime(2025, 9, 30), reason="resignation")
offb.add_task(ob_plan.plan_id, "Knowledge Transfer", "Document processes", "emp", 14)
```

### Attrition Analysis

```python
from agents.hr.agent import AttritionAnalyzer

analyzer = AttritionAnalyzer()
risk = analyzer.assess_attrition_risk(employee)
print(f"Risk level: {risk.risk_level} (score: {risk.risk_score})")
print(f"Risk factors: {risk.risk_factors}")
print(f"Retention actions: {risk.retention_actions}")

high_risk = analyzer.get_high_risk_employees(threshold=0.5)
summary = analyzer.attrition_summary()
exit_analysis = analyzer.exit_reason_analysis()
```

### HR Analytics Dashboard

```python
from agents.hr.agent import HRAgent

agent = HRAgent()
status = agent.full_status()
print(f"Headcount: {status['headcount']}")
print(f"Attrition rate: {status['attrition_rate']:.1f}%")
print(f"Compliance rate: {status['compliance']['compliance_rate']}%")
print(f"Training completion: {status['training']['completion_rate']:.0f}%")
```

---

## Data Models

### Employee Record
| Field | Type | Description |
|-------|------|-------------|
| employee_id | str | Unique identifier |
| first_name, last_name | str | Employee name |
| email | str | Work email |
| department | Department | Department enum |
| job_title | str | Current position |
| job_level | JobLevel | Level enum (intern → c_level) |
| employment_status | EmploymentStatus | active, on_leave, terminated, etc. |
| salary | float | Current salary |
| hire_date | datetime | Employment start date |
| performance_score | float | Latest performance rating (1-5) |
| engagement_score | float | Engagement survey score (1-5) |
| salary_competitiveness_ratio | float | Comp vs market (1.0 = at market) |

### Candidate Record
| Field | Type | Description |
|-------|------|-------------|
| candidate_id | str | Unique identifier |
| stage | CandidateStage | Current pipeline stage |
| source | str | Recruitment source |
| interview_scores | Dict[str, float] | Scores by interviewer |
| offer_amount | float | Offered compensation |
| days_in_pipeline | property | Days since application |

### Performance Review
| Field | Type | Description |
|-------|------|-------------|
| review_id | str | Unique identifier |
| overall_rating | ReviewRating | 1-5 rating |
| competency_ratings | Dict[str, ReviewRating] | By competency |
| weighted_360_score | property | Weighted average of all feedback |

### Goal
| Field | Type | Description |
|-------|------|-------------|
| goal_id | str | Unique identifier |
| status | GoalStatus | not_started → completed |
| completion_pct | float | 0-100% |
| key_results | List[Dict] | Measurable outcomes |
| parent_goal_id | Optional[str] | Hierarchical goal support |

---

## Checklists

### New Hire Onboarding
- [ ] Offer letter signed
- [ ] Background check cleared
- [ ] I-9 form completed
- [ ] Benefits enrollment completed
- [ ] Equipment provisioned
- [ ] System access granted
- [ ] Compliance training assigned
- [ ] Buddy/mentor assigned
- [ ] 30-day check-in scheduled
- [ ] 90-day check-in scheduled

### Performance Review
- [ ] Self-assessment completed
- [ ] Manager review completed
- [ ] 360 feedback collected
- [ ] Goals reviewed and updated
- [ ] Compensation decision documented
- [ ] Development plan created
- [ ] Review calibration completed
- [ ] Employee acknowledgment

### Offboarding
- [ ] Exit interview conducted
- [ ] Equipment returned
- [ ] System access revoked
- [ ] Benefits terminated/COBRA offered
- [ ] Final paycheck processed
- [ ] Knowledge transfer completed
- [ ] Rehire eligibility determined
- [ ] Remaining PTO calculated

### Compliance Audit
- [ ] All employees have current certifications
- [ ] Training completion > 95%
- [ ] No expired compliance items
- [ ] Pay equity within 5% of benchmark
- [ ] Leave policies applied consistently
- [ ] I-9 forms current for all employees

---

## Method Signatures

```python
# EmployeeManager
def hire_employee(self, **kwargs) -> Employee
def terminate_employee(self, employee_id: str, reason: str = "") -> bool
def update_employee(self, employee_id: str, **kwargs) -> Optional[Employee]
def get_employee(self, employee_id: str) -> Optional[Employee]
def get_by_department(self, department: Department) -> List[Employee]
def get_headcount(self) -> Dict[str, int]
def get_salary_statistics(self) -> Dict[str, Any]
def get_attrition_rate(self, lookback_days: int = 365) -> float
def search(self, query: str) -> List[Employee]

# RecruitmentPipeline
def create_opening(self, position: str, department: Department, ...) -> str
def add_candidate(self, **kwargs) -> Candidate
def advance_stage(self, candidate_id: str, stage: CandidateStage, notes: str = "") -> bool
def record_offer(self, candidate_id: str, amount: float, expiry_days: int = 7) -> bool
def get_pipeline(self, position: Optional[str] = None) -> Dict[str, List[Candidate]]
def get_metrics(self) -> RecruitmentMetrics

# PerformanceManager
def create_review(self, **kwargs) -> PerformanceReview
def add_goal(self, **kwargs) -> Goal
def update_goal_progress(self, goal_id: str, completion_pct: float, ...) -> bool
def performance_summary(self, employee_id: str) -> Dict[str, Any]
def team_performance_summary(self, manager_id: str) -> Dict[str, Any]

# CompensationAnalyzer
def add_record(self, record: CompensationRecord) -> None
def set_benchmark(self, job_title: str, market_rate: float, percentile: int = 50) -> None
def calculate_pay_equity(self) -> Dict[str, Any]
def comp_vs_benchmark(self, employee_id: str) -> Dict[str, Any]

# LeaveManager
def submit_request(self, employee_id: str, leave_type: LeaveType, ...) -> LeaveRequest
def approve_request(self, request_id: str, approver: str) -> bool
def get_employee_balance(self, employee_id: str, year: int) -> Optional[LeaveBalance]

# ComplianceTracker
def add_requirement(self, employee_id: str, requirement: str, ...) -> ComplianceItem
def update_status(self, item_id: str, status: ComplianceStatus) -> bool
def compliance_report(self) -> Dict[str, Any]

# TrainingManager
def create_program(self, name: str, training_type: str, ...) -> str
def assign_training(self, employee_id: str, training_name: str, ...) -> TrainingRecord
def complete_training(self, record_id: str, score: Optional[float] = None) -> bool
def training_completion_rate(self) -> Dict[str, Any]

# AttritionAnalyzer
def assess_attrition_risk(self, employee: Employee) -> AttritionRisk
def get_high_risk_employees(self, threshold: float = 0.5) -> List[AttritionRisk]
def attrition_summary(self) -> Dict[str, Any]

# HRAgent (Orchestrator)
def full_status(self) -> Dict[str, Any]
def run(self) -> Dict[str, Any]
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Employee not found | Verify employee_id exists in `employees.employees` dict |
| Leave balance missing | Call `set_balance()` before submitting requests |
| Performance review incomplete | Ensure `reviewer_id` is provided |
| Training score not recorded | Verify `score` parameter is numeric |
| Attrition risk inaccurate | Ensure employee has engagement/performance scores set |
| Compliance items not expiring | Check `expiration_date` is set and `auto_renew` flag |
| Recruitment metrics wrong | Verify candidate stages are set correctly |
| Onboarding tasks not tracked | Ensure `plan_id` and `task_id` are valid |

---

## Best Practices

1. **Always set employee scores** when hiring for accurate attrition risk analysis
2. **Use hierarchical goals** with `parent_goal_id` for OKR alignment
3. **Track compensation changes** with `CompensationRecord` for audit trails
4. **Set leave balances annually** and use `cancel_request()` to handle changes
5. **Configure compliance renewals** with `renewal_lead_days` for timely alerts
6. **Use the orchestrator** (`HRAgent`) for cross-component analytics
7. **Review attrition risks quarterly** and update retention actions
8. **Complete onboarding plans** within 90 days for best new hire outcomes
