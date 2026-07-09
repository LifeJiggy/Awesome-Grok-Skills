# Full-Stack Planner Agent

> Comprehensive project planning platform for tech stack selection, architecture design, sprint management, resource allocation, risk assessment, and delivery tracking.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Usage](#usage)
  - [Tech Stack Evaluation](#tech-stack-evaluation)
  - [Sprint Planning](#sprint-planning)
  - [Resource Allocation](#resource-allocation)
  - [Risk Management](#risk-management)
  - [Cost Estimation](#cost-estimation)
  - [Architecture Design](#architecture-design)
  - [Technical Debt](#technical-debt)
  - [Performance Benchmarks](#performance-benchmarks)
  - [Project Roadmap](#project-roadmap)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Full-Stack Planner Agent provides a complete toolkit for managing software development projects from inception to delivery. It covers every aspect of technical project management:

- **Tech Stack Evaluation**: Multi-criteria comparison of frameworks, databases, and tools
- **Sprint Planning**: Scrum-based iteration management with velocity tracking
- **Resource Allocation**: Team capacity planning and workload optimization
- **Risk Management**: Quantitative risk assessment and mitigation tracking
- **Cost Estimation**: Labor, infrastructure, and third-party cost modeling
- **Architecture Design**: ADR management and component documentation
- **Technical Debt**: Tracking and prioritization of technical shortcuts
- **Performance Benchmarks**: SLA targets and measurement tracking
- **Project Roadmap**: Timeline and milestone management

Built with zero external dependencies — pure Python standard library.

### Key Benefits

- **Zero Dependencies**: Pure Python stdlib, no external packages required
- **Modular Design**: Use only the components you need
- **Type-Safe**: Full type hints on all public methods
- **Extensible**: Easy to add custom estimation strategies, risk models
- **Auditable**: Complete trail of all decisions and changes
- **Agile-Native**: Built for Scrum, Kanban, and hybrid methodologies

### Use Cases

| Use Case | Description |
|----------|-------------|
| Tech Stack Selection | Compare frameworks, databases, tools |
| Sprint Planning | Create sprints, assign tasks, track velocity |
| Resource Allocation | Manage team capacity, balance workloads |
| Risk Management | Identify, assess, and mitigate risks |
| Cost Estimation | Budget planning and tracking |
| Architecture Design | Document decisions and components |
| Technical Debt | Track and prioritize technical shortcuts |
| Performance Tracking | Monitor SLA targets and metrics |

---

## Features

| Category | Capabilities |
|----------|-------------|
| Tech Stack | Multi-criteria evaluation, category ranking, pairwise comparison |
| Sprints | Creation, planning, burndown, velocity tracking, completion |
| Resources | Capacity calculation, workload balancing, skill-based matching |
| Risk | Probability × impact scoring, mitigation suggestions, tolerance thresholds |
| Cost | Labor/infra/third-party estimation, contingency, budget reports |
| Architecture | ADR management, component documentation, ASCII diagrams |
| Debt | Interest modeling, severity classification, prioritized backlog |
| Benchmarks | Target/actual comparison, deviation tracking, status reporting |
| Roadmap | Milestones, dependencies, critical path, timeline generation |

### Detailed Feature List

**Tech Stack Evaluation**
- Register multiple technology candidates
- Evaluate by category (frontend, backend, database, etc.)
- Compare two options side-by-side
- Get full stack recommendations

**Sprint Planning**
- Create sprints with configurable duration
- Add tasks with story points and estimates
- Plan sprint based on team capacity
- Track progress and completion
- Generate burndown data
- Predict future sprint completion

**Resource Allocation**
- Add team members with skills and capacity
- Calculate team capacity
- Find best-fit member for tasks
- Rebalance workloads automatically

**Risk Management**
- Add risks with probability and impact
- Classify risks by severity
- Get mitigation suggestions
- Track risk register and summary

**Cost Estimation**
- Add estimates per work stream
- Calculate budget reports
- Estimate from task lists
- Include contingency

**Architecture Design**
- Document components and data stores
- Create Architecture Decision Records (ADRs)
- Generate ASCII diagrams
- Generate architecture documentation

**Technical Debt**
- Track debt items with interest rates
- Prioritize by interest × fix hours
- Get summary statistics

**Performance Benchmarks**
- Define SLA targets
- Track actual performance
- Report status (met/not met)

---

## Quick Start

```python
from agents.full_stack_planner.agent import (
    SprintPlanner, Task, Priority, ProjectConfig,
    ResourceAllocator, TeamMember, TeamRole,
    RiskManager, Risk,
)

# Create sprint planner
config = ProjectConfig(project_name="My App", team_name="Alpha")
planner = SprintPlanner(config)

# Create sprint
sprint = planner.create_sprint("S1", "Sprint 1", start_date, end_date, "Core features")

# Add tasks
planner.add_task(Task("T1", "Auth API", "JWT auth", Priority.HIGH, story_points=8, estimated_hours=16))
planner.add_task(Task("T2", "Dashboard", "React UI", Priority.MEDIUM, story_points=13, estimated_hours=30))

# Plan sprint
plan = planner.plan_sprint("S1", ["T1", "T2"], team_capacity_hours=160)
print(f"Planned: {plan['tasks_planned']} tasks, {plan['total_points']} points")
```

### Run the Agent

```bash
python agents/full_stack_planner/agent.py
```

---

## Architecture

### Component Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      FULL-STACK PLANNER AGENT                             │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    PROJECT LIFECYCLE                              │   │
│  │  Discover → Plan → Design → Develop → Monitor → Deliver         │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐           │
│  │  Tech Stack│ │  Sprint    │ │  Resource  │ │  Risk      │           │
│  │  Evaluator │ │  Planner   │ │  Allocator │ │  Manager   │           │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘           │
│                                                                          │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐           │
│  │  Cost      │ │  Arch      │ │  Tech Debt │ │  Perf      │           │
│  │  Estimator │ │  Designer  │ │  Tracker   │ │  Benchmarks│           │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘           │
└──────────────────────────────────────────────────────────────────────────┘
```

### Project Lifecycle

```
  Software Project Lifecycle:
  ══════════════════════════

  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │ Discovery│ ─► │ Planning │ ─► │ Design   │ ─► │ Develop  │
  │          │    │          │    │          │    │          │
  └──────────┘    └──────────┘    └──────────┘    └──────────┘
       │               │               │               │
       ▼               ▼               ▼               ▼
  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │  Tech    │    │  Cost    │    │  Arch    │    │  Sprint  │
  │  Eval    │    │  Estimate│    │  Design  │    │  Execute │
  └──────────┘    └──────────┘    └──────────┘    └──────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design.

---

## Usage

### Tech Stack Evaluation

```python
from agents.full_stack_planner.agent import TechStackEvaluator, TechStack, TechCategory

evaluator = TechStackEvaluator()

# Register candidates
evaluator.register_tech(TechStack("React", TechCategory.FRONTEND, "18.2",
    community_score=9.5, performance_score=8.0, learning_curve=7.0, ecosystem_score=9.0))
evaluator.register_tech(TechStack("Vue", TechCategory.FRONTEND, "3.3",
    community_score=8.0, performance_score=7.5, learning_curve=8.5, ecosystem_score=7.5))

# Rank by category
rankings = evaluator.evaluate_category(TechCategory.FRONTEND)
# [("React", 8.35), ("Vue", 7.65)]

# Compare two options
comp = evaluator.compare("React", "Vue")

# Get full recommendation
recs = evaluator.recommend_stack({"categories": [TechCategory.FRONTEND, TechCategory.BACKEND]})
```

### Sprint Planning

```python
from agents.full_stack_planner.agent import SprintPlanner, Task, Priority, TaskStatus

planner = SprintPlanner(ProjectConfig(project_name="MyApp"))

# Create sprint
sprint = planner.create_sprint("S1", "Sprint 1", start_date, end_date, "Core API")

# Add tasks
planner.add_task(Task("T1", "Auth API", "JWT", Priority.HIGH, story_points=8, estimated_hours=16))
planner.add_task(Task("T2", "Products", "CRUD", Priority.HIGH, story_points=5, estimated_hours=10))

# Plan
plan = planner.plan_sprint("S1", ["T1", "T2"], team_capacity_hours=160)

# Track progress
planner.update_task_status("T1", TaskStatus.DONE, actual_hours=14)

# Complete sprint
result = planner.complete_sprint("S1")

# Burndown data
burndown = planner.generate_burndown("S1")

# Predict future sprints
prediction = planner.predict_completion(remaining_points=50)
```

### Resource Allocation

```python
from agents.full_stack_planner.agent import ResourceAllocator, TeamMember, TeamRole

allocator = ResourceAllocator()

allocator.add_member(TeamMember("Alice", TeamRole.TECH_LEAD, ["python", "react"], 150, 40, 0.3, 1.2))
allocator.add_member(TeamMember("Bob", TeamRole.DEVELOPER, ["python", "react"], 100, 40, 0.5, 1.0))
allocator.add_member(TeamMember("Carol", TeamRole.DEVELOPER, ["python", "sql"], 100, 40, 0.2, 1.0))

# Team capacity
capacity = allocator.get_team_capacity()
print(f"Remaining: {capacity['total_remaining_hours']}h, Utilization: {capacity['utilization_pct']:.0f}%")

# Find best fit for a task
best = allocator.find_best_fit(["python", "react"], hours_needed=20)

# Rebalance workload
suggestions = allocator.rebalance_workload()
```

### Risk Management

```python
from agents.full_stack_planner.agent import RiskManager, Risk

risk_mgr = RiskManager(risk_tolerance="medium")

risk_mgr.add_risk(Risk("R1", "Key developer leaves", probability=0.3, impact=8, mitigation="Cross-train"))
risk_mgr.add_risk(Risk("R2", "Scope creep", probability=0.7, impact=6, mitigation="Change control"))
risk_mgr.add_risk(Risk("R3", "Performance issues", probability=0.5, impact=7, mitigation="Load testing"))

# Risk register
register = risk_mgr.get_risk_register()

# Summary
summary = risk_mgr.get_risk_summary()
print(f"Critical: {summary['critical_count']}, Above tolerance: {summary['above_tolerance']}")

# Mitigation suggestions
suggestions = risk_mgr.suggest_mitigations("R1")
```

### Cost Estimation

```python
from agents.full_stack_planner.agent import CostEstimator, CostEstimate

estimator = CostEstimator(default_hourly_rate=100)

estimator.add_estimate(CostEstimate("Backend", "API dev", 200, 120, 0.2, 500, 200))
estimator.add_estimate(CostEstimate("Frontend", "UI dev", 150, 100, 0.2, 0, 100))
estimator.add_estimate(CostEstimate("DevOps", "Infrastructure", 80, 150, 0.15, 2000, 300))

budget = estimator.generate_budget_report()
print(f"Grand total: ${budget['grand_total']:,.0f}")

# Quick estimate from tasks
quick = estimator.estimate_from_tasks(tasks, hourly_rate=100)
```

### Architecture Design

```python
from agents.full_stack_planner.agent import ArchitectureDesigner, ArchitectureStyle, ArchitectureDecision

arch = ArchitectureDesigner(ArchitectureStyle.MODULAR_MONOLITH)

arch.add_component("API Gateway", "Request routing", "FastAPI", ["Routing", "Auth"])
arch.add_component("User Service", "User management", "Python", ["Registration", "Auth"])
arch.add_data_store("PostgreSQL", "PostgreSQL", "Primary data store")
arch.add_integration("REST API", "Frontend", "API Gateway", "HTTPS", "Primary API")

arch.create_adr(ArchitectureDecision(
    adr_id="ADR-001", title="Use Modular Monolith", status="accepted",
    context="Small team", decision="Start modular, extract later",
    consequences=["Simpler deployment"]
))

print(arch.ascii_diagram())
doc = arch.generate_architecture_doc()
```

### Technical Debt

```python
from agents.full_stack_planner.agent import TechDebtTracker, TechnicalDebt, RiskLevel

tracker = TechDebtTracker()
tracker.add_debt(TechnicalDebt("D1", "Legacy auth", RiskLevel.HIGH, "auth", 20, 5))
tracker.add_debt(TechnicalDebt("D2", "Missing tests", RiskLevel.MEDIUM, "testing", 40, 3))

prioritized = tracker.prioritize()  # Highest interest first
summary = tracker.summary()
```

### Performance Benchmarks

```python
from agents.full_stack_planner.agent import PerformanceBenchmarks, PerformanceBenchmark

perf = PerformanceBenchmarks()
perf.add_benchmark(PerformanceBenchmark("API Response Time", target_value=200, unit="ms"))
perf.add_benchmark(PerformanceBenchmark("Uptime", target_value=99.9, unit="%"))

perf.update_actual("API Response Time", 180)
perf.update_actual("Uptime", 99.95)

status = perf.status_report()
# {"total": 2, "met": 2, "not_met": 0, "details": {...}}
```

### Project Roadmap

```python
from agents.full_stack_planner.agent import ProjectRoadmap, ProjectConfig

config = ProjectConfig(project_name="MyApp", start_date=datetime(2025, 1, 1))
roadmap = ProjectRoadmap(config)

roadmap.add_milestone("MVP", datetime(2025, 6, 1), ["Core API", "Basic UI"])
roadmap.add_milestone("Beta", datetime(2025, 9, 1), ["Full features", "Testing"])
roadmap.add_milestone("GA", datetime(2025, 12, 1), ["Production ready"])

timeline = roadmap.generate_timeline()
```

---

## API Reference

### Core Classes

| Class | Description |
|-------|-------------|
| `TechStackEvaluator` | Technology comparison and recommendation |
| `SprintPlanner` | Sprint lifecycle management |
| `ResourceAllocator` | Team capacity and workload optimization |
| `RiskManager` | Risk assessment and mitigation tracking |
| `CostEstimator` | Project cost modeling |
| `ArchitectureDesigner` | ADR and component documentation |
| `TechDebtTracker` | Technical debt management |
| `PerformanceBenchmarks` | SLA target tracking |
| `ProjectRoadmap` | Timeline and milestone management |

### Data Classes

| Class | Description |
|-------|-------------|
| `TechStack` | Technology evaluation entry |
| `Task` | Work item with story points and status |
| `Epic` | Large feature spanning multiple sprints |
| `Sprint` | Scrum sprint container |
| `TeamMember` | Team member with skills and capacity |
| `Risk` | Risk item with probability and impact |
| `ArchitectureDecision` | Architecture Decision Record |
| `CostEstimate` | Cost estimation entry |
| `TechnicalDebt` | Technical debt item |
| `PerformanceBenchmark` | Performance target |
| `ProjectConfig` | Project-level configuration |

### Enums

| Enum | Values |
|------|--------|
| `ProjectPhase` | DISCOVERY, PLANNING, DESIGN, DEVELOPMENT, TESTING, DEPLOYMENT, MAINTENANCE |
| `Priority` | CRITICAL(0), HIGH(1), MEDIUM(2), LOW(3), BACKLOG(4) |
| `TaskStatus` | TODO, IN_PROGRESS, IN_REVIEW, BLOCKED, DONE, CANCELLED |
| `RiskLevel` | CRITICAL, HIGH, MEDIUM, LOW, NEGLIGIBLE |
| `TechCategory` | FRONTEND, BACKEND, DATABASE, INFRASTRUCTURE, DEVOPS, TESTING, MONITORING, SECURITY |
| `ArchitectureStyle` | MONOLITH, MICROSERVICES, SERVERLESS, EVENT_DRIVEN, MODULAR_MONOLITH, CQRS, LAYERED, HEXAGONAL |
| `TeamRole` | PROJECT_MANAGER, TECH_LEAD, SENIOR_DEVELOPER, DEVELOPER, JUNIOR_DEVELOPER, DEVOPS_ENGINEER, QA_ENGINEER, UI_UX_DESIGNER |

---

## Examples

### Complete Project Kickoff

```python
from agents.full_stack_planner.agent import *

# 1. Configuration
config = ProjectConfig(
    project_name="E-Commerce Platform",
    team_name="Commerce Team",
    methodology="scrum",
    sprint_duration_days=14,
    budget=200_000,
    start_date=datetime(2025, 1, 6),
    target_launch=datetime(2025, 7, 1),
)

# 2. Tech Stack Selection
evaluator = TechStackEvaluator()
evaluator.register_tech(TechStack("React", TechCategory.FRONTEND, community_score=9.5, performance_score=8.0, learning_curve=7.0, ecosystem_score=9.0))
evaluator.register_tech(TechStack("FastAPI", TechCategory.BACKEND, community_score=7.5, performance_score=9.0, learning_curve=7.0, ecosystem_score=7.0))
evaluator.register_tech(TechStack("PostgreSQL", TechCategory.DATABASE, community_score=9.0, performance_score=8.5, learning_curve=6.0, ecosystem_score=9.0))

recs = evaluator.recommend_stack({"categories": [TechCategory.FRONTEND, TechCategory.BACKEND, TechCategory.DATABASE]})

# 3. Cost Estimation
estimator = CostEstimator()
estimator.add_estimate(CostEstimate("Backend", "API development", 400, 120, 0.2, 500, 200))
estimator.add_estimate(CostEstimate("Frontend", "UI development", 300, 100, 0.2, 0, 100))
estimator.add_estimate(CostEstimate("DevOps", "Infrastructure setup", 100, 150, 0.15, 2000, 300))
budget = estimator.generate_budget_report()

# 4. Risk Assessment
risk_mgr = RiskManager(risk_tolerance="medium")
risk_mgr.add_risk(Risk("R1", "Key developer leaves", 0.3, 8, mitigation="Cross-train"))
risk_mgr.add_risk(Risk("R2", "Scope creep", 0.7, 6, mitigation="Strict change control"))

# 5. Architecture
arch = ArchitectureDesigner(ArchitectureStyle.MODULAR_MONOLITH)
arch.add_component("API Gateway", "Request routing", "FastAPI", ["Routing", "Auth"])
arch.add_data_store("PostgreSQL", "PostgreSQL", "Primary data store")

# 6. Team Setup
allocator = ResourceAllocator()
allocator.add_member(TeamMember("Alice", TeamRole.TECH_LEAD, ["python", "react"], 150, 40, 0, 1.2))
allocator.add_member(TeamMember("Bob", TeamRole.DEVELOPER, ["python", "react"], 100, 40, 0, 1.0))
capacity = allocator.get_team_capacity()

# 7. Sprint Planning
planner = SprintPlanner(config)
sprint = planner.create_sprint("S1", "Sprint 1", datetime(2025, 1, 6), datetime(2025, 1, 19), "Core API")
```

---

## Configuration

### Project Config

```python
config = ProjectConfig(
    project_name="My Project",
    team_name="My Team",
    methodology="scrum",           # or "kanban", "waterfall"
    sprint_duration_days=14,       # 7, 14, or 21
    working_hours_per_day=8.0,
    working_days_per_week=5,
    risk_tolerance="medium",       # "low", "medium", "high"
    budget=100_000,
    architecture_style=ArchitectureStyle.MODULAR_MONOLITH,
)
```

### Cost Estimator

```python
estimator = CostEstimator(default_hourly_rate=100.0)
# Adjust hourly rates per role
# Set contingency percentage per estimate
```

### Risk Manager

```python
risk_mgr = RiskManager(risk_tolerance="medium")
# "low": threshold=3 (stricter)
# "medium": threshold=5 (balanced)
# "high": threshold=7 (lenient)
```

---

## Best Practices

1. **Start with architecture decisions** — ADRs before code
2. **Use story points for velocity**, hours for capacity planning
3. **Track technical debt** — it compounds like financial debt
4. **Review risks weekly** — probability and impact change over time
5. **Update benchmarks** — performance targets should evolve
6. **Rebalance workloads** — overloaded members produce bugs
7. **Document trade-offs** — every decision has consequences
8. **Estimate with the team** — don't estimate in isolation
9. **Review sprint velocity** — use 3-sprint rolling average
10. **Maintain the roadmap** — adjust milestones as reality changes

### Agile Best Practices

- Keep sprints time-boxed
- Conduct daily standups
- Hold sprint retrospectives
- Groom backlog regularly
- Use definition of done

### Architecture Best Practices

- Document all significant decisions
- Use ADRs for traceability
- Review architecture quarterly
- Avoid premature optimization
- Design for change

---

## Troubleshooting

| Issue | Solution |
|-------|---------|
| Velocity inconsistent | Use 3-sprint rolling average, review estimation accuracy |
| Low resource utilization | Check skill mismatches, review task dependencies |
| Risk scores seem wrong | Validate probability with team, reassess impact |
| Budget overrun | Compare actual vs estimated, review scope changes |
| Architecture drift | Create ADRs for all decisions, review quarterly |
| Debt backlog growing | Prioritize by interest rate, allocate sprint capacity |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Get detailed sprint info
sprint = planner.get_sprint("S1")
print(f"Tasks: {len(sprint.tasks)}")
print(f"Velocity: {sprint.velocity}")
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Update documentation
6. Submit a pull request

### Code Standards
- Full type hints on all public methods
- Docstrings for all classes and public methods
- Zero external dependencies (stdlib only)
- Follow existing naming conventions
- Write tests for new functionality
- Update documentation for API changes

---

## License

MIT License. See [LICENSE](../../LICENSE) for details.

---

## Files

- `agent.py` — Full implementation with all planning modules
- `ARCHITECTURE.md` — Detailed system architecture
- `GROK.md` — Agent identity and usage patterns
- `README.md` — This file
- `workflow.yaml` — Workflow configuration

---

*Plan smart, build right, deliver on time.*