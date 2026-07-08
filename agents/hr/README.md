# HR Agent

> Comprehensive human resources management platform for employee lifecycle, recruitment, performance reviews, compensation analysis, engagement, compliance, training, benefits, attrition analysis, onboarding/offboarding, and organizational structure.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Employee Management](#employee-management)
  - [Recruitment Pipeline](#recruitment-pipeline)
  - [Performance Management](#performance-management)
  - [Compensation Analytics](#compensation-analytics)
  - [Engagement Surveys](#engagement-surveys)
  - [Leave Management](#leave-management)
  - [Compliance Tracking](#compliance-tracking)
  - [Training Management](#training-management)
  - [Benefits Administration](#benefits-administration)
  - [Attrition Analysis](#attrition-analysis)
  - [Onboarding/Offboarding](#onboardingoffboarding)
  - [Org Charts](#org-charts)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The HR Agent covers the full employee lifecycle with 13 integrated components:

- **Employee Management**: Records, demographics, tenure, organizational placement, salary analytics
- **Recruitment Pipeline**: Applicant tracking, stage management, funnel metrics, offer lifecycle
- **Performance Reviews**: Goal tracking, competency ratings, 360-degree feedback, team summaries
- **Compensation**: Salary analysis, benchmarking, pay equity audits, change history
- **Engagement**: Survey creation, response analysis, NPS scoring, department breakdowns
- **Leave Management**: Request workflows, balance tracking, policy enforcement, team calendars
- **Compliance**: Requirement tracking, expiration alerts, renewal management, audit reporting
- **Training**: Program management, assignment, completion tracking, score recording
- **Org Charts**: Hierarchical structure, team trees, span of control analysis
- **Onboarding**: New hire workflows, task management, progress tracking, check-in scheduling
- **Offboarding**: Departure workflows, knowledge transfer, exit interviews
- **Benefits**: Enrollment management, dependent tracking, cost analysis
- **Attrition Analysis**: Risk scoring, factor analysis, retention actions, exit analytics

---

## Features

### Employee Lifecycle Management
- Hire, update, terminate, and search employees
- Track employment status, type, and level
- Monitor tenure, salary, and performance metrics
- Headcount analytics by department, level, and type

### Recruitment Pipeline
- Create job openings with salary ranges
- Track candidates through 10 pipeline stages
- Record offers with expiry dates
- Funnel conversion analytics and time-per-stage metrics

### Performance Management
- Create reviews with 1-5 ratings and competency scores
- 360-degree feedback with weighted scoring
- Goal tracking with hierarchical objectives (OKR alignment)
- Team performance summaries for managers

### Compensation Analytics
- Salary history and change tracking
- Market benchmarking and competitiveness ratios
- Pay equity audits across job titles
- Total compensation calculations (salary + benefits)

### Engagement Surveys
- Create surveys with multiple question types (Likert, NPS, yes/no)
- Submit anonymous or attributed responses
- Calculate NPS scores and question-level averages
- Department-level engagement analysis

### Leave Management
- Submit, approve, deny, and cancel leave requests
- Track balances by leave type (vacation, sick, personal, etc.)
- View team leave calendars
- Utilization rate analysis

### Compliance Tracking
- Track compliance items by category and employee
- Monitor expiration dates and renewal needs
- Generate compliance reports with status breakdowns
- Overdue item identification

### Training Management
- Create training programs with duration and provider
- Assign training with due dates and required/optional flags
- Record completion and scores
- Required training completion rate tracking

### Benefits Administration
- Enroll employees in benefit plans
- Track employer and employee contributions
- Manage dependent coverage
- Benefits cost summary by type

### Attrition Analysis
- Multi-factor risk scoring (tenure, engagement, performance, compensation, etc.)
- Retention action recommendations
- Exit interview recording and analysis
- Attrition trend reporting

### Onboarding/Offboarding
- Create structured onboarding plans with tasks
- Track completion progress
- Assign buddy and mentor
- Offboarding workflows with knowledge transfer

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              HRAgent (Orchestrator)                             │
├─────────────────┬─────────────────┬─────────────────┬─────────────────────────┤
│   Employee      │   Recruitment   │   Performance   │   Compensation          │
│   Manager       │   Pipeline      │   Manager       │   Analyzer              │
├─────────────────┼─────────────────┼─────────────────┼─────────────────────────┤
│ Hire/Terminate  │ Openings        │ Reviews         │ Salary History          │
│ Search          │ Candidates      │ Goals           │ Pay Equity              │
│ Demographics    │ Offers          │ 360 Feedback    │ Benchmarking            │
├─────────────────┼─────────────────┼─────────────────┼─────────────────────────┤
│   Engagement    │   Leave         │   Compliance    │   Training              │
│   Analyzer      │   Manager       │   Tracker       │   Manager               │
├─────────────────┼─────────────────┼─────────────────┼─────────────────────────┤
│ Surveys         │ Requests        │ Requirements    │ Programs                │
│ NPS             │ Balances        │ Expirations     │ Assignments             │
│ Analysis        │ Calendar        │ Audits          │ Scores                  │
├─────────────────┼─────────────────┼─────────────────┼─────────────────────────┤
│   Org Chart     │   Onboarding    │   Offboarding   │   Benefits              │
│   Manager       │   Manager       │   Manager       │   Manager               │
├─────────────────┼─────────────────┼─────────────────┼─────────────────────────┤
│ Hierarchy       │ Plans           │ Plans           │ Enrollment              │
│ Teams           │ Tasks           │ Tasks           │ Dependents              │
│ Span of Control │ Progress        │ Knowledge Xfer  │ Costs                   │
├─────────────────┴─────────────────┴─────────────────┴─────────────────────────┤
│                          AttritionAnalyzer                                    │
├───────────────────────────────────────────────────────────────────────────────┤
│ Risk Scoring │ Factor Analysis │ Retention Actions │ Exit Analytics          │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

```python
from agents.hr.agent import HRAgent, Department, JobLevel

# Initialize the agent
agent = HRAgent()

# Hire an employee
emp = agent.employees.hire_employee(
    first_name="Alice", last_name="Johnson", email="alice@co.com",
    department=Department.ENGINEERING, job_title="Senior Engineer",
    job_level=JobLevel.SENIOR, salary=120000
)

# Get full status dashboard
status = agent.full_status()
print(f"Headcount: {status['headcount']}")
print(f"Departments: {status['by_department']}")
print(f"Avg Tenure: {status['avg_tenure_months']:.1f} months")
```

### Run the Agent

```bash
python agents/hr/agent.py
```

---

## Installation

### Requirements

- Python 3.10+
- No external dependencies (standard library only)

### Setup

```bash
# Clone the repository
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills

# Install in development mode
pip install -e .
```

---

## Usage

### Employee Management

```python
from agents.hr.agent import HRAgent, Department, JobLevel, EmploymentStatus

agent = HRAgent()

# Hire employee
emp = agent.employees.hire_employee(
    first_name="Bob", last_name="Smith",
    email="bob@co.com",
    department=Department.ENGINEERING,
    job_title="Software Engineer",
    job_level=JobLevel.MID,
    salary=95000
)

# Update employee
agent.employees.update_employee(
    emp.employee_id,
    job_title="Senior Software Engineer",
    job_level=JobLevel.SENIOR,
    salary=110000
)

# Terminate employee
agent.employees.terminate_employee(
    emp.employee_id,
    reason="Position eliminated",
    last_day="2025-03-31"
)

# Search employees
results = agent.employees.search("engineer")
# [Employee(...), Employee(...), ...]

# Get headcount
headcount = agent.employees.get_headcount()
# {"total": 150, "by_department": {...}, "by_level": {...}}
```

### Recruitment Pipeline

```python
# Create job opening
opening = agent.recruitment.create_opening(
    title="Senior Product Manager",
    department=Department.PRODUCT,
    salary_min=130000,
    salary_max=160000,
    description="Lead product strategy for enterprise features"
)

# Add candidate
candidate = agent.recruitment.add_candidate(
    opening_id=opening.opening_id,
    name="Jane Doe",
    email="jane@email.com",
    resume_url="https://example.com/resume.pdf"
)

# Advance through stages
agent.recruitment.advance_stage(candidate.candidate_id, "phone_screen")
agent.recruitment.advance_stage(candidate.candidate_id, "technical")
agent.recruitment.advance_stage(candidate.candidate_id, "onsite")
agent.recruitment.advance_stage(candidate.candidate_id, "offer")

# Record offer
agent.recruitment.record_offer(
    candidate_id=candidate.candidate_id,
    salary=145000,
    start_date="2025-04-01",
    expiry_date="2025-02-15"
)

# Get funnel metrics
funnel = agent.recruitment.get_funnel_metrics()
# {"apply": 120, "phone_screen": 45, "technical": 25, "onsite": 12, "offer": 5, "hired": 3}
```

### Performance Management

```python
# Create review
review = agent.performance.create_review(
    employee_id="EMP001",
    reviewer_id="MGR001",
    overall_rating=ReviewRating.EXCEEDS_EXPECTATIONS,
    self_assessment_score=4.0,
    peer_feedback_score=4.3,
    manager_feedback_score=4.5
)

# Add goals (OKR alignment)
goal = agent.performance.add_goal(
    employee_id="EMP001",
    title="Launch feature X",
    description="Ship new analytics dashboard",
    status=GoalStatus.IN_PROGRESS,
    completion_pct=60,
    parent_goal_id="OBJ-001"  # Link to company objective
)

# Get performance summary
summary = agent.performance.performance_summary("EMP001")
# {
#   "employee_id": "EMP001",
#   "avg_rating": 4.2,
#   "reviews": 3,
#   "goals": {"total": 5, "completed": 2, "in_progress": 3},
#   "trend": "improving"
# }

# Team summary
team = agent.performance.team_summary("MGR001")
# {"team_size": 8, "avg_rating": 3.9, "top_performer": "EMP003", ...}
```

### Compensation Analytics

```python
from agents.hr.agent import CompensationAnalyzer

comp = CompensationAnalyzer()

# Add salary record
comp.add_record(
    employee_id="EMP001",
    salary=95000,
    effective_date="2024-01-01",
    reason="Annual adjustment"
)

# Update salary
comp.add_record(
    employee_id="EMP001",
    salary=105000,
    effective_date="2025-01-01",
    reason="Promotion"
)

# Pay equity audit
equity = comp.calculate_pay_equity("Software Engineer")
# {
#   "job_title": "Software Engineer",
#   "employee_count": 25,
#   "avg_salary": 105000,
#   "median_salary": 102000,
#   "min_salary": 85000,
#   "max_salary": 130000,
#   "std_deviation": 12500,
#   "equity_ratio": 0.82
# }

# Benchmark comparison
benchmark = comp.comp_vs_benchmark("Software Engineer", 105000)
# {
#   "job_title": "Software Engineer",
#   "salary": 105000,
#   "market_p50": 110000,
#   "ratio": 0.95,
#   "position": "slightly_below"
# }
```

### Engagement Surveys

```python
from agents.hr.agent import EngagementAnalyzer, QuestionType

engagement = EngagementAnalyzer()

# Create survey
survey = engagement.create_survey(
    name="Q1 2025 Engagement Survey",
    questions=[
        {"text": "I feel valued at work", "type": QuestionType.LIKERT},
        {"text": "How likely to recommend us?", "type": QuestionType.NPS},
        {"text": "Do you have the tools to succeed?", "type": QuestionType.YES_NO}
    ]
)

# Submit responses
engagement.submit_response(
    survey_id=survey.survey_id,
    employee_id="EMP001",
    responses=[{"question_idx": 0, "value": 5}, {"question_idx": 1, "value": 9}]
)

# Analyze
analysis = engagement.analyze_survey(survey.survey_id)
# {
#   "response_rate": 0.85,
#   "nps_score": 42,
#   "question_averages": [4.2, 8.1, 0.88],
#   "by_department": {...}
# }

# Department analysis
dept = engagement.analyze_department_engagement("engineering")
# {"avg_score": 4.1, "nps": 38, "response_rate": 0.92}
```

### Leave Management

```python
from agents.hr.agent import LeaveManager, LeaveType

leave = LeaveManager()

# Set balance
leave.set_balance("EMP001", LeaveType.VACATION, 15)
leave.set_balance("EMP001", LeaveType.SICK, 10)

# Submit request
request = leave.submit_request(
    employee_id="EMP001",
    leave_type=LeaveType.VACATION,
    start_date="2025-06-01",
    end_date="2025-06-05",
    reason="Family vacation"
)

# Approve
leave.approve_request(request.request_id, approved_by="MGR001")

# Get balance
balance = leave.get_employee_balance("EMP001", LeaveType.VACATION)
# {"remaining": 10, "used": 5, "total": 15}

# Team calendar
calendar = leave.get_team_leave_calendar("2025-06")
# [{"employee": "EMP001", "dates": ["2025-06-01", ...], "type": "vacation"}]
```

### Compliance Tracking

```python
from agents.hr.agent import ComplianceTracker

compliance = ComplianceTracker()

# Add requirement
compliance.add_requirement(
    name="Annual Security Training",
    category="training",
    renewal_months=12,
    applicable_to="all"
)

# Update status
compliance.update_status(
    employee_id="EMP001",
    requirement_name="Annual Security Training",
    status="completed",
    completion_date="2025-01-15"
)

# Compliance report
report = compliance.compliance_report()
# {
#   "total_employees": 150,
#   "compliant": 135,
#   "non_compliant": 10,
#   "pending": 5,
#   "compliance_rate": 0.90,
#   "expiring_soon": [...]
# }
```

### Training Management

```python
from agents.hr.agent import TrainingManager

training = TrainingManager()

# Create program
program = training.create_program(
    name="Security Awareness",
    description="Annual security training",
    duration_hours=4,
    provider="Internal"
)

# Assign training
assignment = training.assign_training(
    employee_id="EMP001",
    program_id=program.program_id,
    due_date="2025-03-31",
    required=True
)

# Record completion
training.record_completion(
    assignment_id=assignment.assignment_id,
    score=92,
    completed_date="2025-03-15"
)

# Completion rate
rate = training.training_completion_rate("Security Awareness")
# {"assigned": 150, "completed": 135, "rate": 0.90}
```

### Attrition Analysis

```python
from agents.hr.agent import AttritionAnalyzer

attrition = AttritionAnalyzer()

# Assess risk
risk = attrition.assess_attrition_risk(employee)
# {
#   "employee_id": "EMP001",
#   "risk_score": 0.72,
#   "risk_level": "high",
#   "factors": {
#     "tenure": 0.2,
#     "engagement": 0.3,
#     "performance": 0.1,
#     "compensation": 0.12
#   },
#   "retention_actions": [
#     "Schedule retention conversation",
#     "Review compensation competitiveness",
#     "Discuss career growth path"
#   ]
# }

# High-risk employees
high_risk = attrition.get_high_risk_employees(threshold=0.5)
# [Employee(...), Employee(...), ...]

# Exit analysis
analysis = attrition.exit_reason_analysis()
# {"compensation": 35, "career_growth": 28, "management": 15, "other": 22}
```

---

## API Reference

| Class | Description | Key Methods |
|-------|-------------|-------------|
| `EmployeeManager` | Employee lifecycle management | `hire_employee()`, `terminate_employee()`, `search()` |
| `RecruitmentPipeline` | Applicant tracking | `create_opening()`, `add_candidate()`, `advance_stage()` |
| `PerformanceManager` | Reviews and goals | `create_review()`, `add_goal()`, `performance_summary()` |
| `CompensationAnalyzer` | Salary analysis | `add_record()`, `calculate_pay_equity()`, `comp_vs_benchmark()` |
| `EngagementAnalyzer` | Survey analytics | `create_survey()`, `submit_response()`, `analyze_department_engagement()` |
| `LeaveManager` | Time-off management | `submit_request()`, `approve_request()`, `get_employee_balance()` |
| `ComplianceTracker` | Compliance tracking | `add_requirement()`, `update_status()`, `compliance_report()` |
| `TrainingManager` | Training programs | `create_program()`, `assign_training()`, `training_completion_rate()` |
| `OrgChartManager` | Org structure | `add_employee()`, `get_team_tree()`, `get_span_of_control()` |
| `OnboardingManager` | New hire workflows | `create_plan()`, `add_task()`, `onboarding_progress_report()` |
| `OffboardingManager` | Departure workflows | `create_plan()`, `add_task()`, `offboarding_summary()` |
| `BenefitsManager` | Benefits enrollment | `enroll()`, `get_employee_benefits()`, `benefits_summary_by_type()` |
| `AttritionAnalyzer` | Risk analysis | `assess_attrition_risk()`, `get_high_risk_employees()`, `exit_reason_analysis()` |
| `HRAgent` | Orchestrator | `full_status()`, `run()` |

---

## Configuration

```python
from agents.hr.agent import HRConfig

config = HRConfig(
    probation_days=90,                    # Default probation period
    review_cycle_months=12,               # Review cycle frequency
    default_vacation_days=15,             # Annual vacation allowance
    default_sick_days=10,                 # Annual sick days
    compliance_renewal_lead_days=30,      # Days before expiry to renew
    attrition_risk_threshold=0.5,         # High-risk threshold
    salary_benchmark_percentile=50,       # Market percentile target
)
agent = HRAgent(config=config)
```

---

## Examples

### Hire and Onboard Employee
```python
agent = HRAgent()
emp = agent.employees.hire_employee(
    first_name="Bob", last_name="Smith", email="bob@co.com",
    department=Department.ENGINEERING, job_title="Developer",
    salary=95000
)
plan = agent.onboarding.create_plan(emp.employee_id, datetime.utcnow())
agent.onboarding.add_task(plan.plan_id, "Setup workstation", "Configure dev environment", "it", 1)
agent.onboarding.add_task(plan.plan_id, "Security training", "Complete mandatory training", "emp", 7)
```

### Performance Review Cycle
```python
review = agent.performance.create_review(
    employee_id="EMP001", reviewer_id="MGR001",
    overall_rating=ReviewRating.EXCEEDS_EXPECTATIONS,
    self_assessment_score=4.0, peer_feedback_score=4.3,
    manager_feedback_score=4.5
)
goal = agent.performance.add_goal(
    employee_id="EMP001", title="Launch feature X",
    status=GoalStatus.IN_PROGRESS, completion_pct=60
)
summary = agent.performance.performance_summary("EMP001")
```

### Attrition Risk Assessment
```python
risk = agent.attrition.assess_attrition_risk(employee)
if risk.risk_score >= 0.5:
    print(f"HIGH RISK: {employee.full_name}")
    for action in risk.retention_actions:
        print(f"  → {action}")
```

---

## Best Practices

1. **Set employee scores early** — performance and engagement scores drive attrition risk analysis
2. **Use hierarchical goals** with `parent_goal_id` for OKR alignment
3. **Track compensation changes** via `CompensationRecord` for audit compliance
4. **Configure leave balances annually** and handle cancellations properly
5. **Set compliance renewal alerts** with adequate lead time
6. **Complete onboarding within 90 days** for best retention outcomes
7. **Review attrition risks quarterly** and update retention actions
8. **Use the orchestrator** (`HRAgent`) for cross-component analytics

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Employee not found | Verify `employee_id` exists in `employees.employees` |
| Leave balance missing | Call `set_balance()` before submitting requests |
| Training score not recorded | Ensure `score` parameter is numeric |
| Attrition risk inaccurate | Set `engagement_score` and `performance_score` on employee |
| Compliance items not expiring | Set `expiration_date` on the compliance item |
| Onboarding tasks not tracked | Use valid `plan_id` from `create_plan()` |

---

## Files

- `agent.py` — Full implementation with all 13 components
- `ARCHITECTURE.md` — System architecture and design patterns
- `GROK.md` — Agent identity, capabilities, and API documentation
- `README.md` — This file

---

## License

MIT License — See [LICENSE](../LICENSE) for details.

---

*Manage people with data, not just intuition. Build great workplaces through transparency and fairness.*
