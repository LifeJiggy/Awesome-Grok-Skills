# Quality Agent — System Architecture

> Comprehensive architecture for the Quality Assurance Agent — test planning, defect tracking, SPC, Six Sigma DMAIC, and quality metrics.

---

## Table of Contents

1. [Overview](#overview)
2. [Design Principles](#design-principles)
3. [System Components](#system-components)
4. [Data Flow](#data-flow)
5. [Component Deep Dives](#component-deep-dives)
6. [Data Models](#data-models)
7. [Design Patterns](#design-patterns)
8. [Configuration](#configuration)
9. [Performance](#performance)
10. [Security](#security)
11. [Scalability](#scalability)
12. [Extension Points](#extension-points)
13. [Monitoring & Observability](#monitoring--observability)
14. [Testing the Agent](#testing-the-agent)
15. [Troubleshooting](#troubleshooting)
16. [Best Practices](#best-practices)
17. [Glossary](#glossary)
18. [Appendix: Design Decisions](#appendix-design-decisions)

---

## Overview

The Quality Agent is a comprehensive quality assurance platform integrating test management, defect lifecycle tracking, Statistical Process Control (SPC), Six Sigma DMAIC methodology, root cause analysis, quality gates, and risk management into a unified system.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         QUALITY ECOSYSTEM                               │
│                                                                         │
│   Requirements ──▶ Test Plan ──▶ Test Cases ──▶ Execution ──▶ Results  │
│                                                                         │
│   Results ──▶ Defects ──▶ Root Cause ──▶ Corrective Actions            │
│                                                                         │
│   Results ──▶ SPC Charts ──▶ Control Limits ──▶ Process Improvements   │
│                                                                         │
│   All Data ──▶ Metrics Engine ──▶ Dashboards ──▶ Stakeholders          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Benefits

| Benefit | Description |
|---------|-------------|
| **Statistical Rigor** | All quality decisions backed by SPC and statistical evidence |
| **Automated Gates** | Quality gates enforce standards at every phase transition |
| **Root Cause Depth** | Multiple RCA methods (5 Whys, Fishbone, Pareto) for different scenarios |
| **Continuous Improvement** | DMAIC projects drive measurable process improvements |
| **Risk-Based Focus** | Testing effort concentrated where risk is highest |

---

## Design Principles

1. **Data-Driven Quality**: Every quality decision backed by statistical evidence.
2. **Continuous Improvement**: Feedback loops drive process refinement.
3. **Defect Prevention Over Detection**: Invest in preventing defects, not just finding them.
4. **Risk-Based Testing**: Focus testing effort where risk is highest.
5. **Automation First**: Automate repetitive quality processes.
6. **Measurable Outcomes**: Track quality metrics with SPC charts and control limits.

```
Design Principles in Practice:
═══════════════════════════════

  "Data-Driven"          "Prevention"           "Risk-Based"
       │                      │                      │
       ▼                      ▼                      ▼
  ┌─────────┐          ┌──────────┐          ┌──────────┐
  │   SPC   │          │  DMAIC   │          │  Risk    │
  │ Charts  │          │ Projects │          │  Matrix  │
  └────┬────┘          └────┬─────┘          └────┬─────┘
       │                    │                     │
       └────────────────────┼─────────────────────┘
                            ▼
                   ┌────────────────┐
                   │ Quality Gates  │
                   │  (Enforce at   │
                   │   each phase)  │
                   └────────────────┘
```

---

## System Components

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          Quality Agent (Orchestrator)                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────────┐  │
│  │ TestPlanManager   │  │ TestCaseManager   │  │       TestRunner             │  │
│  │                   │  │                   │  │                              │  │
│  │ • Create plans    │  │ • Create cases    │  │ • Execute tests              │  │
│  │ • Entry/exit      │  │ • Equivalence     │  │ • Run suites                 │  │
│  │   criteria        │  │   partitioning    │  │ • Record results             │  │
│  │ • Activate/       │  │ • Boundary        │  │ • Track pass/fail            │  │
│  │   complete        │  │   analysis        │  │ • Summary statistics         │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────────────────┘  │
│                                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────────┐  │
│  │  DefectManager    │  │    SPCEngine      │  │    SixSigmaManager          │  │
│  │                   │  │                   │  │                              │  │
│  │ • Report defects  │  │ • Control limits  │  │ • DMAIC projects            │  │
│  │ • Status FSM      │  │ • Out of control  │  │ • Sigma level calc          │  │
│  │ • Assign/track    │  │ • Western Electric│  │ • DPMO conversion           │  │
│  │ • Aging report    │  │ • Capability (Cp, │  │ • Phase management           │  │
│  │ • Metrics         │  │   Cpk) analysis   │  │ • DMAIC checklists          │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────────────────┘  │
│                                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────────┐  │
│  │RootCauseAnalyzer  │  │QualityGatesManager│ │     RiskManager              │  │
│  │                   │  │                   │  │                              │  │
│  │ • 5 Whys          │  │ • Gate evaluation │  │ • Risk assessment            │  │
│  │ • Fishbone        │  │ • Pass/fail       │  │ • Risk matrix                │  │
│  │ • Pareto          │  │ • All-gates check │  │ • Mitigation tracking        │  │
│  │ • Summary         │  │ • Failed gates    │  │ • Score computation          │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────────────────┘  │
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐   │
│  │                      QualityMetricsEngine                                │   │
│  │  • Track metrics  • Summary  • Scorecard  • Threshold alerts            │   │
│  └──────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

```
                    ┌──────────────────────────┐
                    │    Requirements Input     │
                    │    Code Changes           │
                    │    Production Data        │
                    └────────────┬─────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
    ┌─────────▼─────────┐ ┌─────▼──────┐ ┌────────▼────────┐
    │  TestPlanManager   │ │TestCaseMgr │ │  RiskManager     │
    │  (Define scope →   │ │(Generate → │ │  (Assess →       │
    │   Entry/exit →     │ │  Boundary →│ │   Score →        │
    │   Activate)        │ │  ECP)      │ │   Mitigate)      │
    └─────────┬─────────┘ └─────┬──────┘ └────────┬────────┘
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │       TestRunner          │
                    │  (Execute → Record →      │
                    │   Summarize)              │
                    └────────────┬─────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
    ┌─────────▼─────────┐ ┌─────▼──────┐ ┌────────▼────────┐
    │  DefectManager     │ │  SPCEngine  │ │QualityGates     │
    │  (Report →         │ │ (Collect → │ │(Evaluate →      │
    │   Triage →         │ │  Limits →  │ │ Pass/Fail →     │
    │   Resolve)         │ │  Detect →  │ │ Record)         │
    │                    │ │  Analyze)  │ │                 │
    └─────────┬─────────┘ └─────┬──────┘ └────────┬────────┘
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
    ┌─────────▼─────────┐ ┌─────▼──────┐          │
    │RootCauseAnalyzer   │ │SixSigma    │          │
    │ (5 Whys / Fishbone │ │Manager     │          │
    │  → Corrective →    │ │(DMAIC →    │          │
    │  Preventive)       │ │ Sigma →    │          │
    │                    │ │ Improve)   │          │
    └─────────┬─────────┘ └─────┬──────┘          │
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │  QualityMetricsEngine     │
                    │  (Aggregate → Scorecard → │
                    │   Alert → Dashboard)      │
                    └──────────────────────────┘
```

### Defect Lifecycle State Machine

```
NEW ──→ CONFIRMED ──→ ASSIGNED ──→ IN_PROGRESS ──→ FIX_READY
 │          │                                        │
 │          ├──→ DEFERRED ──→ ASSIGNED               │
 │          │                                        │
 │          └──→ DUPLICATE (terminal)                │
 │                                                   ▼
 └──→ WONT_FIX (terminal)                    VERIFIED ──→ CLOSED
                                                   │
                                                   └──→ REOPENED ──→ IN_PROGRESS
```

### Test Execution Flow

```
TEST_PLAN ──→ TEST_CASES ──→ EXECUTION ──→ RESULTS ──→ REPORT
                                         │
                                         ├──→ PASSED ──→ Next test
                                         ├──→ FAILED ──→ Defect report
                                         ├──→ SKIPPED ──→ Log reason
                                         └──→ BLOCKED ──→ Risk flag
```

---

## Component Deep Dives

### TestPlanManager

Manages comprehensive test plans with entry/exit criteria.

**Plan Lifecycle:**
```
DRAFT ──→ ACTIVE ──→ COMPLETED
```

**Entry Criteria Examples:**
- Code review completed
- Unit tests passing
- Build deployed to test environment

**Exit Criteria Examples:**
- 100% test execution
- No critical defects open
- 95% pass rate

```python
# Method signatures
class TestPlanManager:
    def create_plan(self, name, description, scope, objectives,
                    test_types, environment, entry_criteria=None,
                    exit_criteria=None) -> TestPlan
    def activate_plan(self, plan_id) -> TestPlan
    def complete_plan(self, plan_id) -> TestPlan
    def get_plan(self, plan_id) -> Optional[TestPlan]
    def list_plans(self, status=None) -> List[TestPlan]
    def get_plan_summary(self, plan_id) -> Dict
```

### TestCaseManager

Creates test cases with support for test design techniques.

**Equivalence Partitioning:**
```
Input: Age field (valid: 18-65)
Partitions:
  Valid: [18, 65]  → test with 40
  Invalid: [< 18]  → test with 10
  Invalid: [> 65]  → test with 70
```

**Boundary Analysis:**
```
Boundaries: 18, 65
Test values: 17, 18, 19, 64, 65, 66
```

### DefectManager

Full defect lifecycle with severity/priority classification.

**Severity Definitions:**
| Severity | Definition |
|----------|-----------|
| Blocker | System down, no workaround |
| Critical | Major feature broken, no workaround |
| Major | Feature broken with workaround |
| Minor | Cosmetic or minor issue |
| Trivial | Enhancement or typo |

**Valid State Transitions:**
```
NEW → CONFIRMED, WONT_FIX, DUPLICATE
CONFIRMED → ASSIGNED, DEFERRED, WONT_FIX
ASSIGNED → IN_PROGRESS, DEFERRED
IN_PROGRESS → FIX_READY, ASSIGNED
FIX_READY → VERIFIED
VERIFIED → CLOSED, REOPENED
REOPENED → IN_PROGRESS
```

### SPCEngine

Statistical Process Control for quality monitoring.

**Control Limits Formula:**
```
UCL = mean + 3σ
CL  = mean
LCL = mean - 3σ

For I-MR charts:
UCL = mean + 2.66 × MR̄
LCL = mean - 2.66 × MR̄
```

**Western Electric Rules:**
1. One point beyond 3σ
2. Two of three consecutive points beyond 2σ (same side)
3. Four of five consecutive points beyond 1σ (same side)
4. Eight consecutive points on same side of center line

**Capability Indices:**
```
Cp  = (USL - LSL) / 6σ
Cpu = (USL - mean) / 3σ
Cpl = (mean - LSL) / 3σ
Cpk = min(Cpu, Cpl)
```

**Interpretation Guide:**
```
Cpk Rating    Interpretation    Action
─────────────────────────────────────────
≥ 1.67        Excellent         Monitor
1.33 - 1.67   Capable           Accept
1.0 - 1.33    Marginally Capable  Improve
< 1.0         Incapable         Stop & Fix
```

### SixSigmaManager

DMAIC project management with sigma level calculations.

**Sigma Level to DPMO:**
```
1σ → 691,462 DPMO
2σ →  22,750 DPMO
3σ →   1,350 DPMO
4σ →      32 DPMO
5σ →       0.57 DPMO
6σ →       0.0034 DPMO
```

**DMAIC Phase Checklist:**
```
DEFINE:
  [x] Problem statement
  [x] Project charter
  [x] Stakeholder analysis
  [x] SIPOC diagram

MEASURE:
  [x] Data collection plan
  [x] Measurement system analysis
  [x] Process capability baseline
  [x] Voice of Customer

ANALYZE:
  [x] Root cause analysis
  [x] Hypothesis testing
  [x] Regression analysis
  [x] Process mapping

IMPROVE:
  [x] Solution generation
  [x] Pilot implementation
  [x] Cost-benefit analysis
  [x] Risk assessment

CONTROL:
  [x] Control plan
  [x] SPC monitoring
  [x] Documentation
  [x] Training plan
```

### RootCauseAnalyzer

Multiple analysis methods for defect root cause identification.

**5 Whys Example:**
```
Problem: Application crashed
Why 1: Null pointer exception in payment module
Why 2: User data was null
Why 3: Database query returned empty result
Why 4: User record doesn't exist
Why 5: Registration flow has race condition
Root Cause: Race condition in concurrent registration
```

**Fishbone Categories:**
- People: Training, skills, communication
- Process: Procedures, workflows, standards
- Technology: Tools, infrastructure, code
- Materials: Data, inputs, specifications
- Environment: Network, hardware, load
- Management: Resources, priorities, oversight

**Pareto Principle:**
```
80% of defects come from 20% of causes
Vital Few: Categories causing ≤80% of defects
Trivial Many: Remaining categories
```

### QualityGatesManager

Evaluates quality gates at phase transitions.

**Gate Sequence:**
```
REQUIREMENTS → DESIGN → CODE_REVIEW → UNIT_TEST → INTEGRATION_TEST
→ SYSTEM_TEST → UAT → PERFORMANCE → SECURITY → RELEASE
```

### RiskManager

Assesses and mitigates quality risks using probability × impact scoring.

**Risk Matrix:**
```
Impact ↑
  5  │ M  H  H  C  C
  4  │ L  M  H  H  C
  3  │ L  M  M  H  H
  2  │ L  L  M  M  H
  1  │ L  L  L  M  M
     └────────────────→
       1  2  3  4  5  Probability
```

### QualityMetricsEngine

Tracks and analyzes quality metrics with threshold-based alerting.

---

## Data Models

### Core Entities

```
┌─────────────────────┐     ┌─────────────────────┐
│     TestPlan        │     │     TestCase        │
│                     │     │                     │
│ • plan_id           │     │ • test_id           │
│ • name              │     │ • plan_id           │
│ • status            │     │ • name              │
│ • entry_criteria    │     │ • test_type         │
│ • exit_criteria     │     │ • priority          │
│ • test_types        │     │ • steps             │
│ • scope             │     │ • expected_result   │
│ • objectives        │     │ • preconditions     │
└─────────────────────┘     └─────────────────────┘

┌─────────────────────┐     ┌─────────────────────┐
│     Defect          │     │     TestResult      │
│                     │     │                     │
│ • defect_id         │     │ • result_id         │
│ • title             │     │ • test_id           │
│ • severity          │     │ • status            │
│ • priority          │     │ • duration_ms       │
│ • status            │     │ • executed_at       │
│ • reporter          │     │ • error_message     │
│ • assignee          │     │ • notes             │
│ • steps_to_reproduce│     └─────────────────────┘
│ • history           │
└─────────────────────┘     ┌─────────────────────┐
                            │     QualityMetric   │
┌─────────────────────┐     │                     │
│     SPCDataPoint    │     │ • metric_id         │
│                     │     │ • name              │
│ • metric_name       │     │ • value             │
│ • value             │     │ • unit              │
│ • timestamp         │     │ • recorded_at       │
│ • subgroup          │     │ • thresholds        │
│ • source            │     │ • tags              │
└─────────────────────┘     └─────────────────────┘
```

---

## Design Patterns

| Pattern | Usage | Component |
|---------|-------|-----------|
| **State** | Defect lifecycle FSM | DefectManager |
| **Strategy** | Multiple SPC calculation types | SPCEngine |
| **Template Method** | DMAIC phase checklists | SixSigmaManager |
| **Chain of Responsibility** | Quality gate evaluations | QualityGatesManager |
| **Observer** | Threshold alerting | QualityMetricsEngine |
| **Factory** | Test case generation from templates | TestCaseManager |
| **Composite** | Test suites containing test cases | TestRunner |
| **Facade** | Unified quality interface | QualityAgent |

---

## Configuration

```python
QualityConfig(
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

## Performance

| Metric | Target | Notes |
|--------|--------|-------|
| Test case creation | < 2ms | Dict insertion |
| Test execution | < 10ms | Depends on step count |
| Defect reporting | < 2ms | Dict insertion |
| SPC control limits | < 5ms | For 1000 data points |
| Capability analysis | < 10ms | For 1000 data points |
| Pareto analysis | < 5ms | Sort + accumulate |
| Quality gate eval | < 2ms | Boolean check |
| Risk matrix | < 5ms | Categorize risks |
| Full status | < 20ms | All components |

---

## Security

- **Input Validation**: All public methods validate inputs.
- **No External Calls**: All computation is local.
- **Audit Trail**: Defect and test result history maintained.
- **Access Control**: Method-level for sensitive operations.
- **Data Integrity**: Immutable result records.

---

## Scalability

| Dimension | Strategy |
|-----------|----------|
| Test cases | Indexed by type, priority, tags |
| Test results | Time-bucketed; summary statistics |
| Defects | Indexed by severity, status, component |
| SPC data | Time-series with rolling windows |
| DMAIC projects | Independent lifecycle |
| Quality gates | Sequential evaluation with caching |

---

## Extension Points

1. **Custom SPC Charts**: Add EWMA, CUSUM, or other chart types.
2. **Test Automation Hooks**: Integrate with pytest, selenium, etc.
3. **Defect Integrations**: Jira, GitHub Issues, Linear connectors.
4. **Custom Root Cause Methods**: Add fault tree, failure mode analysis.
5. **Quality Dashboard Plugins**: Custom visualizations and reports.

---

## Monitoring & Observability

| Signal | Method |
|--------|--------|
| Test pass rate | `test_runner.results_summary()["pass_rate"]` |
| Defect density | `defects.defect_metrics()["defect_density"]` |
| SPC violations | `spc.detect_out_of_control(metric)` |
| Quality gate status | `gates.gate_status()` |
| Risk exposure | `risks.risk_summary()["avg_score"]` |
| Six Sigma level | `six_sigma.sigma_level(defects, opportunities)` |
| RCA completion | `rca.analysis_summary()["total_analyses"]` |

---

## Testing the Agent

```python
# Unit test example for SPC
def test_control_limits():
    spc = SPCEngine()
    for v in [10.0, 10.2, 9.8, 10.1, 10.3]:
        spc.add_data_point("metric1", v)
    limits = spc.calculate_control_limits("metric1", SPCCalculationType.I_MR)
    assert limits.upper_control_limit > limits.center_line
    assert limits.lower_control_limit < limits.center_line

# Integration test for defect lifecycle
def test_defect_lifecycle():
    dm = DefectManager()
    defect = dm.report_defect(title="Bug", severity=DefectSeverity.MAJOR,
                               priority=DefectPriority.P2_HIGH, reporter="qa-1")
    dm.confirm_defect(defect.defect_id)
    dm.assign_defect(defect.defect_id, "dev-1")
    dm.start_fix(def defect.defect_id)
    dm.mark_fix_ready(defect.defect_id)
    dm.verify_fix(defect.defect_id)
    assert defect.status == DefectStatus.CLOSED
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| SPC shows no violations | Limits not calculated | Calculate limits before detection |
| Defect transition fails | Invalid state transition | Check valid transition table |
| Quality gate always passes | Criteria too lenient | Review and tighten criteria |
| Sigma level returns 0 | Zero defects/opportunities | Ensure both values > 0 |
| Pareto chart incomplete | Few categories | Add more root cause categories |
| Test suite blocked | Missing prerequisites | Verify entry criteria met |
| Metrics show stale data | No recent recordings | Ensure metrics are being tracked |

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

## Glossary

| Term | Definition |
|------|-----------|
| SPC | Statistical Process Control |
| DMAIC | Define, Measure, Analyze, Improve, Control |
| DPMO | Defects Per Million Opportunities |
| Cp | Process capability index (potential) |
| Cpk | Process capability index (actual) |
| USL | Upper Specification Limit |
| LSL | Lower Specification Limit |
| UCL | Upper Control Limit |
| LCL | Lower Control Limit |
| MR | Moving Range |
| FMEA | Failure Mode and Effects Analysis |
| RCA | Root Cause Analysis |
| ECP | Equivalence Class Partitioning |

---

## Appendix: Design Decisions

| Decision | Rationale |
|----------|-----------|
| Defect FSM with reopen | Real-world defects often reopen after verification |
| Welch's t-test for SPC | More robust for unequal subgroup sizes |
| 3σ default control limits | Industry standard for SPC charts |
| Pareto 80/20 threshold | Well-established quality management principle |
| In-memory storage | Simplicity; persistence layer optional |
| Multiple RCA methods | Different defects suit different analysis techniques |
| Quality gate strictness | Configurable to balance speed vs. quality |
