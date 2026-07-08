# Quality Assurance Agent

> AI-powered quality assurance and testing automation platform with SPC, Six Sigma DMAIC, and root cause analysis.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

The Quality Assurance Agent is a comprehensive QA platform that provides test planning, test case design, test execution, defect tracking, Statistical Process Control (SPC), Six Sigma DMAIC methodology, root cause analysis, quality gates, and risk management. It is designed for QA teams, development organizations, and anyone focused on software quality improvement.

### Design Principles

- **Data-Driven**: Every quality decision backed by statistical evidence
- **Automation First**: Automate repetitive quality processes
- **Risk-Based**: Focus testing effort where risk is highest
- **Measurable**: Track quality metrics with SPC charts and control limits
- **Continuous Improvement**: Feedback loops drive process refinement

---

## Features

| Feature | Description |
|---------|-------------|
| **Test Plan Management** | Create, activate, and complete test plans with entry/exit criteria |
| **Test Case Design** | Equivalence partitioning, boundary analysis, priority-based design |
| **Test Execution** | Run individual tests or full suites with result tracking |
| **Defect Tracking** | Full lifecycle management with severity/priority classification |
| **SPC Analysis** | Control limits, Western Electric rules, capability analysis |
| **Six Sigma DMAIC** | Project management with phase checklists and sigma level calculation |
| **Root Cause Analysis** | 5 Whys, Fishbone, Pareto analysis methods |
| **Quality Gates** | Gate evaluation with pass/fail criteria tracking |
| **Risk Management** | Risk assessment with probability × impact scoring |
| **Quality Metrics** | Track, aggregate, and scorecard quality metrics with threshold alerting |

---

## Quick Start

### Installation

```bash
# No external dependencies required
python agents/quality/agent.py
```

### Basic Usage

```python
from agents.quality.agent import QualityAgent

# Initialize the agent
agent = QualityAgent()

# Run the agent
result = agent.run()
print(result)
```

### First Test Plan

```python
from agents.quality.agent import TestPlanManager, TestType

mgr = TestPlanManager()
plan = mgr.create_plan(
    name="My First Test Plan",
    description="Testing the new login feature",
    scope="Login module",
    objectives=["Verify login with valid/invalid credentials"],
    test_types=[TestType.SYSTEM, TestType.SMOKE],
    environment="staging"
)
mgr.activate_plan(plan.plan_id)
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Quality Agent (Orchestrator)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐  │
│  │ TestPlanManager   │  │ TestCaseManager   │  │  TestRunner   │  │
│  └──────────────────┘  └──────────────────┘  └───────────────┘  │
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐  │
│  │  DefectManager    │  │    SPCEngine      │  │  SixSigma     │  │
│  └──────────────────┘  └──────────────────┘  └───────────────┘  │
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐  │
│  │ RootCauseAnalyzer │  │QualityGates      │  │ RiskManager   │  │
│  └──────────────────┘  └──────────────────┘  └───────────────┘  │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │              QualityMetricsEngine                          │   │
│  └───────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full system architecture.

---

## Usage

### Test Planning

```python
from agents.quality.agent import TestPlanManager, TestType

mgr = TestPlanManager()
plan = mgr.create_plan(
    name="Release 3.0 QA",
    description="Full regression for v3.0",
    scope="All modules",
    objectives=["Zero critical defects", "95% pass rate"],
    test_types=[TestType.UNIT, TestType.INTEGRATION, TestType.SYSTEM],
    entry_criteria=["Code complete", "Build deployed"],
    exit_criteria=["All tests pass", "No P0 defects"]
)
```

### Test Case Design

```python
from agents.quality.agent import TestCaseManager, TestType, TestPriority

tc_mgr = TestCaseManager()

# Create test case
tc = tc_mgr.create_test_case(
    name="Age validation",
    description="Test age field accepts valid ages",
    test_type=TestType.UNIT,
    priority=TestPriority.HIGH,
    preconditions=["Form is loaded"],
    steps=[{"action": "Enter age 25", "expected_result": "Age accepted"}],
    expected_result="Form submits successfully"
)

# Generate boundary tests
boundaries = tc_mgr.boundary_analysis("age", [(18, 65)])
# Returns: 17 (below_min), 18 (at_min), 19 (above_min), 64, 65, 66
```

### Defect Management

```python
from agents.quality.agent import DefectManager, DefectSeverity, DefectPriority

defects = DefectManager()
defect = defects.report_defect(
    title="Payment timeout on slow network",
    description="Payment API times out after 30s on 3G connection",
    severity=DefectSeverity.MAJOR,
    priority=DefectPriority.P2_HIGH,
    reporter="qa-1",
    steps_to_reproduce=["Connect to 3G", "Initiate payment", "Wait 30s"],
    expected_behavior="Payment completes or shows retry option",
    actual_behavior="Timeout error with no retry"
)
```

### SPC Analysis

```python
from agents.quality.agent import SPCEngine, SPCCalculationType

spc = SPCEngine()
for value in [10.2, 10.5, 10.1, 10.3, 15.2, 10.4]:
    spc.add_data_point("response_time", value)

limits = spc.calculate_control_limits("response_time", SPCCalculationType.I_MR)
violations = spc.detect_out_of_control("response_time")
capability = spc.capability_analysis("response_time", usl=12.0, lsl=8.0)
```

### Six Sigma DMAIC

```python
from agents.quality.agent import SixSigmaManager

ss = SixSigmaManager()
project = ss.create_project(
    name="Reduce Defect Rate",
    description="Cut defects by 50%",
    business_case="High defect rate impacts customer satisfaction",
    problem_statement="5% defect rate in production",
    goal_statement="Reduce to 2.5% within 6 months",
    sponsor="VP Eng",
    champion="QA Lead",
    team_members=["qa-1", "dev-1"],
    current_sigma=3.5,
    target_sigma=4.5
)
sigma = ss.sigma_level(defects=100, opportunities=10000)
```

---

## API Reference

| Class | Description |
|-------|-------------|
| `TestPlanManager` | Create, manage, and track test plans |
| `TestCaseManager` | Design test cases with partitioning and boundary analysis |
| `TestRunner` | Execute tests and record results |
| `DefectManager` | Defect lifecycle management with FSM |
| `SPCEngine` | Statistical Process Control with control limits and rules |
| `SixSigmaManager` | DMAIC project management and sigma calculations |
| `RootCauseAnalyzer` | 5 Whys, Fishbone, and Pareto analysis |
| `QualityGatesManager` | Quality gate evaluation and tracking |
| `RiskManager` | Risk assessment and mitigation tracking |
| `QualityMetricsEngine` | Metric tracking, aggregation, and scorecards |
| `QualityAgent` | Orchestrator that ties all components together |

### Enums

| Enum | Values |
|------|--------|
| `TestStatus` | PASSED, FAILED, SKIPPED, BLOCKED, ERROR, NOT_RUN |
| `TestType` | UNIT, INTEGRATION, SYSTEM, ACCEPTANCE, PERFORMANCE, SECURITY, USABILITY, REGRESSION, SMOKE, SANITY |
| `TestPriority` | CRITICAL(1), HIGH(2), MEDIUM(3), LOW(4) |
| `DefectSeverity` | BLOCKER, CRITICAL, MAJOR, MINOR, TRIVIAL |
| `DefectPriority` | P0_IMMEDIATE, P1_URGENT, P2_HIGH, P3_MEDIUM, P4_LOW |
| `DefectStatus` | NEW, CONFIRMED, ASSIGNED, IN_PROGRESS, FIX_READY, VERIFIED, CLOSED, REOPENED, DEFERRED, DUPLICATE, WONT_FIX |
| `SPCCalculationType` | XBAR_R, XBAR_S, P_CHART, NP_CHART, C_CHART, U_CHART, I_MR |
| `DMAICPhase` | DEFINE, MEASURE, ANALYZE, IMPROVE, CONTROL |
| `RootCauseMethod` | FIVE_WHYS, FISHBONE, PARETO, FAULT_TREE, FAILURE_MODE |
| `QualityGate` | REQUIREMENTS, DESIGN, CODE_REVIEW, UNIT_TEST, INTEGRATION_TEST, SYSTEM_TEST, UAT, PERFORMANCE, SECURITY, RELEASE |

---

## Examples

### Complete QA Workflow

```python
from agents.quality.agent import QualityAgent, TestType, TestPriority, DefectSeverity, DefectPriority

# Initialize
agent = QualityAgent()

# 1. Create test plan
plan = agent.test_plans.create_plan(
    name="Sprint 42 QA",
    description="QA for sprint 42 features",
    scope="New payment module",
    objectives=["Full coverage of payment flows"],
    test_types=[TestType.UNIT, TestType.INTEGRATION, TestType.SYSTEM]
)

# 2. Create test cases
tc = agent.test_cases.create_test_case(
    name="Payment with valid card",
    test_type=TestType.SYSTEM,
    priority=TestPriority.CRITICAL,
    preconditions=["User logged in", "Item in cart"],
    steps=[
        {"action": "Click Checkout", "expected_result": "Payment form shown"},
        {"action": "Enter card details", "expected_result": "Card validated"},
        {"action": "Click Pay", "expected_result": "Payment processed"},
    ],
    expected_result="Order confirmed"
)

# 3. Execute tests
result = agent.test_runner.run_test(tc)

# 4. If failed, report defect
if result.status.value == "failed":
    defect = agent.defects.report_defect(
        title="Payment fails with valid card",
        severity=DefectSeverity.CRITICAL,
        priority=DefectPriority.P0_IMMEDIATE,
        reporter="qa-1",
        steps_to_reproduce=["Click Checkout", "Enter valid card", "Click Pay"],
        expected_behavior="Payment succeeds",
        actual_behavior="Payment API returns 500"
    )

# 5. Track quality metrics
agent.metrics.track_metric("test_pass_rate", 95.0, unit="%")

# 6. Get full status
status = agent.full_status()
```

### SPC Monitoring Dashboard

```python
from agents.quality.agent import SPCEngine, SPCCalculationType

spc = SPCEngine()

# Simulate production metrics
import random
random.seed(42)
for i in range(50):
    value = 10.0 + random.gauss(0, 0.5)
    spc.add_data_point("api_response_time", value)

# Calculate limits
limits = spc.calculate_control_limits("api_response_time", SPCCalculationType.I_MR)
print(f"Center Line: {limits.center_line}")
print(f"UCL: {limits.upper_control_limit}")
print(f"LCL: {limits.lower_control_limit}")

# Check for violations
violations = spc.detect_out_of_control("api_response_time")
print(f"Out-of-control points: {len(violations)}")

# Get trend
trend = spc.metric_trend("api_response_time", last_n=20)
print(f"Trend direction: {trend['trend_direction']}")
```

---

## Configuration

```python
from agents.quality.agent import QualityConfig

config = QualityConfig(
    default_test_environment="staging",
    defect_auto_assign=True,
    spc_default_subgroup_size=5,
    spc_warning_threshold_sigma=2.0,
    spc_critical_threshold_sigma=3.0,
    min_test_coverage_pct=80.0,
    max_defect_reopen_rate=5.0,
    quality_gate_strict=True,
    regression_suite_min_pass_rate=95.0,
)
```

| Setting | Default | Description |
|---------|---------|-------------|
| `default_test_environment` | "staging" | Default test environment |
| `defect_auto_assign` | True | Auto-assign defects on creation |
| `spc_default_subgroup_size` | 5 | Default SPC subgroup size |
| `spc_warning_threshold_sigma` | 2.0 | Warning threshold (sigma) |
| `spc_critical_threshold_sigma` | 3.0 | Critical threshold (sigma) |
| `min_test_coverage_pct` | 80.0 | Minimum test coverage target |
| `max_defect_reopen_rate` | 5.0 | Maximum acceptable reopen rate |
| `quality_gate_strict` | True | Strict quality gate evaluation |
| `regression_suite_min_pass_rate` | 95.0 | Minimum regression pass rate |

---

## Best Practices

### Test Planning
1. Always define clear entry and exit criteria
2. Include risk assessment in every test plan
3. Map test cases to requirements for traceability
4. Review and update test plans as scope changes

### Defect Management
1. Write clear, reproducible steps to reproduce
2. Classify severity and priority accurately
3. Track defect aging and address stale defects
4. Conduct root cause analysis on recurring defects

### SPC Monitoring
1. Collect data consistently over time
2. Use appropriate chart types for your data
3. Investigate all out-of-control signals
4. Update control limits as process improves

### Six Sigma DMAIC
1. Start with a clear problem statement
2. Collect baseline data before making changes
3. Validate improvements with statistical analysis
4. Sustain gains with control plans and SPC

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Test execution fails with import error | Ensure `agents/quality/` is in your Python path |
| SPC shows no violations | Verify control limits are calculated before detection |
| Defect transition fails | Check the valid transition table for the current state |
| Quality gate always passes | Review criteria — ensure they test real conditions |
| Sigma level returns 0 | Check that defects and opportunities are > 0 |

---

## Files

| File | Description |
|------|-------------|
| `agent.py` | Full implementation (all classes and logic) |
| `GROK.md` | Agent identity, capabilities, and code examples |
| `ARCHITECTURE.md` | System architecture with diagrams |
| `README.md` | This file — overview and quick start |

---

## License

MIT License — see [LICENSE](../../LICENSE) for details.

---

*Ensure quality, measure outcomes, improve continuously.*