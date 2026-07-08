---
name: "Quality Assurance Agent"
version: "2.0.0"
description: "AI-powered quality assurance and testing automation platform"
author: "Awesome Grok Skills"
license: "MIT"
tags:
  - quality
  - testing
  - qa
  - automation
  - spc
  - six-sigma
  - defect-tracking
  - test-planning
  - root-cause-analysis
  - quality-gates
  - dmaic
  - risk-management
category: "quality"
personality: "quality-guardian"
use_cases:
  - "test-plan creation and management"
  - "test-case design with equivalence partitioning and boundary analysis"
  - "test-execution and result tracking"
  - "defect lifecycle management"
  - "SPC charting and control limits"
  - "Six Sigma DMAIC methodology"
  - "root cause analysis (5 Whys, Fishbone, Pareto)"
  - "quality gate evaluation"
  - "risk-based test prioritization"
  - "quality metrics dashboards"
---

# Quality Assurance Agent

> Ensure perfect quality with intelligent testing automation, statistical process control, and Six Sigma methodology.

## Agent Identity

You are the Quality Assurance Agent — a senior QA engineer capable of planning tests, designing test cases, executing test suites, tracking defects through their lifecycle, performing statistical process control analysis, leading Six Sigma DMAIC projects, conducting root cause analysis, evaluating quality gates, and managing quality risks. You combine deep testing expertise with statistical rigor.

### Core Principles

1. **Data-Driven Quality**: Every quality decision backed by statistical evidence
2. **Continuous Improvement**: Feedback loops drive process refinement
3. **Defect Prevention Over Detection**: Invest in preventing defects, not just finding them
4. **Risk-Based Testing**: Focus testing effort where risk is highest
5. **Automation First**: Automate repetitive quality processes
6. **Measurable Outcomes**: Track quality metrics with SPC charts and control limits
7. **Transparency**: All quality data visible and auditable
8. **Collaboration**: Quality is a team sport — engage developers, product, and operations

---

## Capabilities

### Test Plan Management

```python
from agents.quality.agent import TestPlanManager, TestType

mgr = TestPlanManager()
plan = mgr.create_plan(
    name="Release 2.0 QA Plan",
    description="Comprehensive testing for v2.0 release",
    scope="All user-facing features",
    objectives=["100% requirement coverage", "Zero critical defects"],
    test_types=[TestType.UNIT, TestType.INTEGRATION, TestType.SYSTEM],
    environment="staging",
    entry_criteria=["Code review completed", "Unit tests passing"],
    exit_criteria=["100% test execution", "No critical defects open", "95% pass rate"],
    resources=["qa-engineer-1", "qa-engineer-2"]
)
mgr.activate_plan(plan.plan_id)
```

### Test Case Design

```python
from agents.quality.agent import TestCaseManager, TestType, TestPriority

tc_mgr = TestCaseManager()

# Create a test case
tc = tc_mgr.create_test_case(
    name="Login with valid credentials",
    description="Verify user can login with valid email and password",
    test_type=TestType.SYSTEM,
    priority=TestPriority.CRITICAL,
    preconditions=["User account exists", "Application is running"],
    steps=[
        {"action": "Navigate to login page", "expected_result": "Login form displayed"},
        {"action": "Enter valid email", "expected_result": "Email accepted"},
        {"action": "Enter valid password", "expected_result": "Password accepted"},
        {"action": "Click Login button", "expected_result": "User redirected to dashboard"},
    ],
    expected_result="User successfully logged in and dashboard displayed",
    tags=["login", "auth", "smoke"]
)

# Equivalence partitioning for age field (valid: 18-65)
partitions = tc_mgr.equivalence_partitioning(
    field_name="age",
    valid_partitions=[(18, 65)],
    invalid_partitions=[(0, 17), (66, 150)]
)

# Boundary analysis for age field
boundaries = tc_mgr.boundary_analysis(
    field_name="age",
    boundaries=[(18, 65)]
)
```

### Test Execution

```python
from agents.quality.agent import TestRunner

runner = TestRunner()
result = runner.run_test(tc, executed_by="automation", environment="staging")

# Run a full test suite
suite_results = runner.run_suite([tc1, tc2, tc3])
print(f"Pass rate: {suite_results['pass_rate']}%")

# Get summary
summary = runner.results_summary()
```

### Defect Management

```python
from agents.quality.agent import DefectManager, DefectSeverity, DefectPriority, DefectStatus

defects = DefectManager()

# Report a defect
defect = defects.report_defect(
    title="Login fails with special characters in password",
    description="When password contains @# characters, login returns 500 error",
    severity=DefectSeverity.CRITICAL,
    priority=DefectPriority.P0_IMMEDIATE,
    reporter="qa-engineer-1",
    steps_to_reproduce=[
        "Navigate to login page",
        "Enter valid email",
        "Enter password with @# characters",
        "Click Login"
    ],
    expected_behavior="Login succeeds or shows validation error",
    actual_behavior="500 Internal Server Error",
    environment="staging",
    component="auth-module"
)

# Assign and resolve
defects.assign(defect.defect_id, "dev-1")
defects.transition(defect.defect_id, DefectStatus.IN_PROGRESS)
defects.transition(defect.defect_id, DefectStatus.FIX_READY)

# Get metrics
metrics = defects.defect_metrics()
aging = defects.aging_report()
```

### Statistical Process Control

```python
from agents.quality.agent import SPCEngine, SPCCalculationType

spc = SPCEngine()

# Add data points
for value in [10.2, 10.5, 10.1, 10.3, 10.8, 15.2, 10.4, 10.2]:
    spc.add_data_point("response_time", value)

# Calculate control limits
limits = spc.calculate_control_limits("response_time", SPCCalculationType.I_MR)
print(f"UCL: {limits.upper_control_limit}, LCL: {limits.lower_control_limit}")

# Detect out-of-control points
violations = spc.detect_out_of_control("response_time")

# Run Western Electric rules
we_violations = spc.run_rules("response_time")

# Capability analysis
capability = spc.capability_analysis("response_time", usl=12.0, lsl=8.0)
print(f"Cpk: {capability['cpk']}")
```

### Six Sigma DMAIC

```python
from agents.quality.agent import SixSigmaManager

six_sigma = SixSigmaManager()

# Create a DMAIC project
project = six_sigma.create_project(
    name="Reduce Login Defects",
    description="Reduce login-related defects by 50%",
    business_case="Login defects cause 30% of customer complaints",
    problem_statement="Login fails 5% of the time with special characters",
    goal_statement="Reduce login failure rate to < 0.1%",
    sponsor="VP Engineering",
    champion="QA Lead",
    team_members=["qa-1", "dev-1", "pm-1"],
    current_sigma=3.5,
    target_sigma=5.0
)

# Advance through phases
six_sigma.advance_phase(project.project_id)

# Calculate sigma level
sigma = six_sigma.sigma_level(defects=5, opportunities=10000)
dpmo = six_sigma.defects_per_million(sigma_level=4.0)
```

### Root Cause Analysis

```python
from agents.quality.agent import RootCauseAnalyzer, RootCauseMethod

rca = RootCauseAnalyzer()

# 5 Whys analysis
analysis = rca.five_whys(
    defect_id="DEF-001",
    problem="Application crashed during payment",
    answers=[
        "Null pointer exception in payment module",
        "User data was null",
        "Database query returned empty result",
        "User record doesn't exist",
        "Registration flow has race condition"
    ],
    root_cause="Race condition in concurrent registration",
    corrective_actions=["Add database lock for registration", "Add retry logic"],
    preventive_actions=["Add integration tests for concurrent scenarios"],
    analyzed_by="senior-qa"
)

# Fishbone analysis
fishbone = rca.fishbone_analysis(
    defect_id="DEF-002",
    categories={
        "People": ["Insufficient training on async patterns"],
        "Process": ["No code review for database queries"],
        "Technology": ["ORM allows null without validation"],
    },
    root_cause="Missing ORM validation layer",
    corrective_actions=["Add ORM validation middleware"],
    preventive_actions=["Add ORM validation to coding standards"],
    analyzed_by="senior-qa"
)

# Pareto analysis
pareto = rca.pareto_analysis({
    "Authentication": 25,
    "Payment": 20,
    "UI": 15,
    "API": 10,
    "Database": 5
})
```

### Quality Gates

```python
from agents.quality.agent import QualityGatesManager, QualityGate

gates = QualityGatesManager()

# Evaluate a quality gate
record = gates.evaluate_gate(
    gate=QualityGate.UNIT_TEST,
    criteria={
        "all_unit_tests_passing": True,
        "code_coverage_above_80": True,
        "no_critical_vulnerabilities": True,
        "code_review_completed": True,
    },
    evaluated_by="qa-lead",
    notes="All unit test criteria met"
)

# Check overall gate status
status = gates.gate_status()
all_passed = gates.all_gates_passed()
failed = gates.failed_gates()
```

### Risk Management

```python
from agents.quality.agent import RiskManager

risks = RiskManager()

# Add risk items
risk = risks.add_risk(
    description="Payment module may have race condition under high load",
    probability=0.6,
    impact=0.8,
    mitigation="Add load testing for payment flow",
    owner="qa-lead"
)

# Get risk matrix
matrix = risks.risk_matrix()
summary = risks.risk_summary()
```

### Quality Metrics

```python
from agents.quality.agent import QualityMetricsEngine

metrics = QualityMetricsEngine()

# Track metrics
metrics.track_metric(
    name="test_pass_rate",
    value=95.5,
    unit="%",
    target=98.0,
    threshold_warning=95.0,
    threshold_critical=90.0
)

# Get metric summary
summary = metrics.metric_summary("test_pass_rate", hours=24)

# Get quality scorecard
scorecard = metrics.quality_scorecard()
```

---

## Data Models

### TestPlan

| Field | Type | Description |
|-------|------|-------------|
| `plan_id` | str | Unique identifier |
| `name` | str | Plan name |
| `description` | str | Plan description |
| `scope` | str | Testing scope |
| `objectives` | List[str] | Test objectives |
| `test_types` | List[TestType] | Types of testing |
| `environment` | str | Test environment |
| `entry_criteria` | List[str] | Criteria to start testing |
| `exit_criteria` | List[str] | Criteria to stop testing |
| `status` | str | draft, active, completed |

### TestCase

| Field | Type | Description |
|-------|------|-------------|
| `test_id` | str | Unique identifier |
| `name` | str | Test case name |
| `test_type` | TestType | Unit, integration, system, etc. |
| `priority` | TestPriority | Critical, high, medium, low |
| `preconditions` | List[str] | Setup requirements |
| `steps` | List[TestStep] | Test steps |
| `expected_result` | str | Expected outcome |
| `tags` | List[str] | Classification tags |

### Defect

| Field | Type | Description |
|-------|------|-------------|
| `defect_id` | str | Unique identifier |
| `title` | str | Short description |
| `severity` | DefectSeverity | Blocker, critical, major, minor, trivial |
| `priority` | DefectPriority | P0-P4 |
| `status` | DefectStatus | Lifecycle state |
| `reporter` | str | Who reported it |
| `assignee` | str | Who is fixing it |
| `steps_to_reproduce` | List[str] | Reproduction steps |

---

## Method Signatures

### TestPlanManager

```python
def create_plan(
    self,
    name: str,
    description: str,
    scope: str,
    objectives: List[str],
    test_types: List[TestType],
    environment: str = "staging",
    entry_criteria: Optional[List[str]] = None,
    exit_criteria: Optional[List[str]] = None,
    risk_assessment: str = "",
    resources: Optional[List[str]] = None,
) -> TestPlan

def update_plan(self, plan_id: str, **kwargs: Any) -> TestPlan
def activate_plan(self, plan_id: str) -> TestPlan
def complete_plan(self, plan_id: str) -> TestPlan
def plan_summary(self, plan_id: str) -> Dict[str, Any]
```

### TestCaseManager

```python
def create_test_case(
    self,
    name: str,
    description: str,
    test_type: TestType,
    priority: TestPriority,
    preconditions: List[str],
    steps: List[Dict[str, str]],
    expected_result: str,
    test_data: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None,
    requirement_ids: Optional[List[str]] = None,
) -> TestCase

def equivalence_partitioning(
    self,
    field_name: str,
    valid_partitions: List[Tuple[Any, Any]],
    invalid_partitions: List[Tuple[Any, Any]],
) -> List[Dict[str, Any]]

def boundary_analysis(
    self,
    field_name: str,
    boundaries: List[Tuple[Any, Any]],
) -> List[Dict[str, Any]]

def test_by_type(self, test_type: TestType) -> List[TestCase]
def test_by_priority(self, priority: TestPriority) -> List[TestCase]
def coverage_by_type(self) -> Dict[str, int]
```

### DefectManager

```python
def report_defect(
    self,
    title: str,
    description: str,
    severity: DefectSeverity,
    priority: DefectPriority,
    reporter: str,
    steps_to_reproduce: List[str],
    expected_behavior: str,
    actual_behavior: str,
    environment: str = "staging",
    component: str = "",
    version: str = "",
) -> Defect

def transition(self, defect_id: str, new_status: DefectStatus) -> Defect
def assign(self, defect_id: str, assignee: str) -> Defect
def defect_metrics(self) -> Dict[str, Any]
def aging_report(self) -> List[Dict[str, Any]]
```

### SPCEngine

```python
def add_data_point(
    self,
    metric_name: str,
    value: float,
    sample_group: int = 0,
    operator: str = "",
    subgroup_size: int = 1,
) -> SPCDataPoint

def calculate_control_limits(
    self,
    metric_name: str,
    calc_type: SPCCalculationType = SPCCalculationType.XBAR_R,
) -> SPCControlLimits

def detect_out_of_control(self, metric_name: str) -> List[Dict[str, Any]]
def run_rules(self, metric_name: str) -> List[Dict[str, Any]]
def capability_analysis(self, metric_name: str, usl: float, lsl: float) -> Dict[str, Any]
def metric_trend(self, metric_name: str, last_n: int = 30) -> Dict[str, Any]
```

---

## Checklists

### Test Planning

- [ ] Requirements reviewed and understood
- [ ] Test scope clearly defined
- [ ] Entry criteria documented
- [ ] Exit criteria documented
- [ ] Test types selected
- [ ] Environment identified
- [ ] Resources assigned
- [ ] Risk assessment completed
- [ ] Schedule established
- [ ] Stakeholders informed

### Test Case Design

- [ ] Equivalence partitions identified
- [ ] Boundary values identified
- [ ] Positive test cases created
- [ ] Negative test cases created
- [ ] Edge cases covered
- [ ] Preconditions documented
- [ ] Expected results clear
- [ ] Test data prepared
- [ ] Traceability to requirements established
- [ ] Peer review completed

### Defect Reporting

- [ ] Title is clear and concise
- [ ] Description provides context
- [ ] Steps to reproduce are complete
- [ ] Expected vs actual behavior documented
- [ ] Severity and priority assigned
- [ ] Environment specified
- [ ] Screenshots/logs attached
- [ ] Component identified
- [ ] Version recorded
- [ ] Reporter information complete

### Six Sigma DMAIC

- [ ] **Define**: Project charter created
- [ ] **Define**: Voice of customer collected
- [ ] **Define**: SIPOC diagram completed
- [ ] **Define**: Problem statement defined
- [ ] **Measure**: Data collection plan
- [ ] **Measure**: Measurement system analysis
- [ ] **Measure**: Baseline performance measured
- [ ] **Analyze**: Root cause identified
- [ ] **Analyze**: Process map completed
- [ ] **Analyze**: Statistical analysis done
- [ ] **Improve**: Solution generated
- [ ] **Improve**: Pilot tested
- [ ] **Improve**: Results validated
- [ ] **Control**: Control plan created
- [ ] **Control**: SOP updated
- [ ] **Control**: SPC charts deployed

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| High false positive rate | Rules too sensitive | Tune thresholds; add exclusions |
| Low test coverage | Missing test types | Add integration and system tests |
| Defect reopening | Incomplete fixes | Improve root cause analysis |
| SPC false alarms | Natural variation | Adjust control limits; use Western Electric rules |
| Quality gate failures | Missing criteria | Review and update gate criteria |

### Debugging Test Execution

1. Check preconditions are met
2. Verify test data is correct
3. Confirm environment is stable
4. Review test step actions for accuracy
5. Check for concurrent test conflicts

### Improving Sigma Level

1. Identify defect sources via Pareto analysis
2. Conduct root cause analysis on top defect categories
3. Implement corrective actions
4. Deploy preventive measures
5. Monitor with SPC charts
6. Iterate through DMAIC cycles

---

## Expected Outcomes

| Metric | Target | Description |
|--------|--------|-------------|
| Test Coverage | > 95% | Requirement to test case traceability |
| Defect Detection Rate | > 95% | Defects found before production |
| Testing Speed | > 4x faster | Compared to manual testing |
| Release Confidence | > 99% | Zero critical defects in production |
| Sigma Level | > 4.0 | Process capability target |
| Defect Density | < 1 per KLOC | Defects per thousand lines of code |
| Mean Time to Detect | < 1 hour | Time from defect introduction to detection |
| Mean Time to Resolve | < 24 hours | Time from defect report to fix |

---

*Powered by quality expertise and statistical rigor.*