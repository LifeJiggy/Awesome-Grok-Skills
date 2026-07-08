# HR Agent

> Comprehensive human resources management platform for employee lifecycle, recruitment, performance reviews, compensation analysis, engagement, compliance, training, benefits, attrition analysis, onboarding/offboarding, and organizational structure.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Files](#files)
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
```

### Run the Agent

```bash
python agents/hr/agent.py
```

---

## Usage

See [GROK.md](GROK.md) for detailed API documentation, code examples, and method signatures.

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
