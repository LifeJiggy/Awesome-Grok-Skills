# HR Agent

> Comprehensive human resources management platform for employee lifecycle, recruitment, performance reviews, compensation analysis, engagement, compliance, and training.

---

## Overview

The HR Agent covers the full employee lifecycle:

- **Employee Management**: Records, demographics, tenure, organizational placement
- **Recruitment Pipeline**: Applicant tracking, stage management, funnel metrics
- **Performance Reviews**: Goal tracking, competency ratings, review cycles
- **Compensation**: Salary analysis, benchmarking, pay equity
- **Engagement**: Survey creation, response analysis, department scoring
- **Leave Management**: Request workflows, balance tracking, policy enforcement
- **Compliance**: Requirement tracking, expiration alerts, audit reporting
- **Training**: Program management, assignment, completion tracking
- **Org Charts**: Hierarchical structure, team trees, depth calculation

---

## Quick Start

```python
from agents.hr.agent import EmployeeManager, Department, JobLevel

mgr = EmployeeManager()
emp = mgr.hire_employee(
    first_name="Alice", last_name="Johnson", email="alice@co.com",
    department=Department.ENGINEERING, job_title="Engineer", salary=100000
)
print(f"Hired: {emp.full_name}")
```

### Run the Agent

```bash
python agents/hr/agent.py
```

---

## Usage

See [GROK.md](GROK.md) for detailed API documentation and examples.

---

## API Reference

| Class | Description |
|-------|-------------|
| `EmployeeManager` | Employee lifecycle management |
| `RecruitmentPipeline` | Applicant tracking |
| `PerformanceManager` | Reviews and goals |
| `CompensationAnalyzer` | Salary analysis |
| `EngagementAnalyzer` | Survey analytics |
| `LeaveManager` | Time-off management |
| `ComplianceTracker` | Compliance tracking |
| `TrainingManager` | Training programs |
| `OrgChartManager` | Org structure |

---

## Files

- `agent.py` — Full implementation
- `ARCHITECTURE.md` — System architecture
- `GROK.md` — Agent identity and patterns
- `README.md` — This file

---

*Manage people with data, not just intuition.*
