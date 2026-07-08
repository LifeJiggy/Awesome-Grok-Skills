# Quality Agent Architecture

> Comprehensive architecture for the Quality Assurance Agent — test planning, defect tracking, SPC, Six Sigma DMAIC, and quality metrics.

---

## Table of Contents

1. [Overview](#overview)
2. [System Components](#system-components)
3. [Data Flow](#data-flow)
4. [Key Components](#key-components)
5. [Component Details](#component-details)
6. [Design Patterns](#design-patterns)
7. [Tech Stack](#tech-stack)
8. [Configuration](#configuration)
9. [Performance](#performance)
10. [Security](#security)
11. [Scalability](#scalability)
12. [Extension Points](#extension-points)
13. [Monitoring & Observability](#monitoring--observability)
14. [Glossary](#glossary)
15. [Appendix: Design Decisions](#appendix-design-decisions)

---

## Overview

The Quality Agent is a comprehensive quality assurance platform integrating test management, defect lifecycle tracking, Statistical Process Control (SPC), Six Sigma DMAIC methodology, root cause analysis, quality gates, and risk management into a unified system.

### Design Principles

- **Data-Driven Quality**: Every quality decision backed by statistical evidence.
- **Continuous Improvement**: Feedback loops drive process refinement.
- **Defect Prevention Over Detection**: Invest in preventing defects, not just finding them.
- **Risk-Based Testing**: Focus testing effort where risk is highest.
- **Automation First**: Automate repetitive quality processes.
- **Measurable Outcomes**: Track quality metrics with SPC charts and control limits.

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

## Key Components

### 1. TestPlanManager

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

### 2. TestCaseManager

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

### 3. TestRunner

Executes test cases and records results with timing.

### 4. DefectManager

Full defect lifecycle with severity/priority classification.

**Severity Definitions:**
- Blocker: System down, no workaround
- Critical: Major feature broken, no workaround
- Major: Feature broken with workaround
- Minor: Cosmetic or minor issue
- Trivial: Enhancement or typo

### 5. SPCEngine

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

### 6. SixSigmaManager

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

**Sigma Level Calculation:**
```
σ = 0.8406 + 0.2948 × ln(1,000,000 / DPMO)
```

### 7. RootCauseAnalyzer

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

### 8. QualityGatesManager

Evaluates quality gates at phase transitions.

**Gate Sequence:**
```
REQUIREMENTS → DESIGN → CODE_REVIEW → UNIT_TEST → INTEGRATION_TEST
→ SYSTEM_TEST → UAT → PERFORMANCE → SECURITY → RELEASE
```

### 9. RiskManager

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

### 10. QualityMetricsEngine

Tracks and analyzes quality metrics with threshold-based alerting.

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

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| Data Structures | dataclasses, Enum, Dict, List |
| Statistics | statistics, math (normal CDF) |
| Date/Time | datetime, timedelta |
| ID Generation | uuid4 |
| Logging | Python logging module |
| Optional | pytest, SQLite |

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
