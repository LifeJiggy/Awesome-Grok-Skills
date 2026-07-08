# Development Agent — System Architecture

## Table of Contents

1. [Overview](#overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Component Deep Dives](#component-deep-dives)
4. [Data Flow Diagrams](#data-flow-diagrams)
5. [Design Patterns](#design-patterns)
6. [Tech Stack](#tech-stack)
7. [Security Architecture](#security-architecture)
8. [Scalability Patterns](#scalability-patterns)
9. [Testing Architecture](#testing-architecture)
10. [CI/CD Pipeline Architecture](#cicd-pipeline-architecture)
11. [Monitoring & Observability](#monitoring--observability)
12. [Deployment Topology](#deployment-topology)
13. [Configuration Reference](#configuration-reference)
14. [Error Handling Patterns](#error-handling-patterns)

---

## Overview

The Development Agent is a comprehensive software development analysis and generation
system built around a modular architecture. Each concern — static analysis, refactoring,
security scanning, testing, documentation, CI/CD, and performance optimization — is
encapsulated in a dedicated engine with well-defined interfaces. A unified Dashboard
orchestrates all engines and exposes a single entry point for consumers.

### Design Principles

| Principle | Description |
|-----------|-------------|
| **Single Responsibility** | Each engine handles one concern exclusively |
| **Open/Closed** | New analysis engines can be added without modifying existing code |
| **Dependency Inversion** | High-level orchestration depends on abstract engine interfaces |
| **Composition over Inheritance** | The Dashboard composes engines rather than inheriting from them |
| **Fail-Safe Defaults** | Every component returns meaningful defaults on error |

### Module Map

```
agents/development/
├── agent.py           # All engines, data models, and the Dashboard
├── ARCHITECTURE.md    # This document — system design and rationale
├── GROK.md            # Agent identity, capabilities, and usage guides
└── README.md          # Quick start, API reference, examples
```

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        CONSUMER LAYER                                │
│   CLI  │  API Gateway  │  Web UI  │  CI/CD Webhook  │  SDK Client  │
└────────┬──────────┬──────────┬──────────┬──────────────┬────────────┘
         │          │          │          │              │
         ▼          ▼          ▼          ▼              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT DASHBOARD                              │
│                                                                      │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌──────────────────┐  │
│  │   Static   │ │ Refactoring│ │  Security  │ │   Performance    │  │
│  │  Analysis  │ │   Engine   │ │  Scanner   │ │    Optimizer     │  │
│  │  Engine    │ │            │ │            │ │                  │  │
│  └────────────┘ └────────────┘ └────────────┘ └──────────────────┘  │
│                                                                      │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌──────────────────┐  │
│  │  Testing   │ │   Code     │ │   CI/CD    │ │   Documentation  │  │
│  │ Strategies │ │  Quality   │ │  Pipeline  │ │   Generator      │  │
│  │            │ │  Manager   │ │            │ │                  │  │
│  └────────────┘ └────────────┘ └────────────┘ └──────────────────┘  │
│                                                                      │
│  ┌────────────┐ ┌────────────┐                                      │
│  │ Dependency │ │   Code     │                                      │
│  │  Analyzer  │ │ Generation │                                      │
│  │            │ │  Engine    │                                      │
│  └────────────┘ └────────────┘                                      │
└──────────────────────────────────────────────────────────────────────┘
         │          │          │          │              │
         ▼          ▼          ▼          ▼              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      SUPPORT LAYER                                   │
│  Logging  │  Metrics  │  Caching  │  Event Bus  │  Configuration    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Component Deep Dives

### 1. Static Analysis Engine

The StaticAnalysisEngine performs pattern-based code analysis using regex patterns
for security vulnerabilities, code smells, and quality issues.

```
┌─────────────────────────────────────────────────┐
│              Static Analysis Engine               │
│                                                   │
│  ┌─────────────┐   ┌──────────────────────────┐  │
│  │   Pattern   │──▶│  Issue Classification    │  │
│  │   Matcher   │   │  (Type + Severity)       │  │
│  └─────────────┘   └──────────┬───────────────┘  │
│                               │                   │
│  ┌─────────────┐   ┌──────────▼───────────────┐  │
│  │  Metric     │──▶│  CodeIssue Generation    │  │
│  │  Calculator │   │  (with suggestions)      │  │
│  └─────────────┘   └──────────────────────────┘  │
│                                                   │
│  Metrics:                                         │
│  ├── Cyclomatic Complexity (McCabe)               │
│  ├── Halstead Volume                              │
│  ├── Maintainability Index                        │
│  ├── Lines of Code / Comments / Blanks            │
│  └── Function / Class / Import Counts             │
└─────────────────────────────────────────────────┘
```

**Key algorithms:**

- **Cyclomatic Complexity**: Counts decision points (`if`, `elif`, `for`, `while`, `except`, `and`, `or`) plus a base of 1. This gives a lower bound on the number of independent execution paths.

- **Halstead Volume**: Computes vocabulary (unique operators + unique operands) and derives volume as `V = n * log2(n)`. Higher volume indicates greater complexity.

- **Maintainability Index**: A composite of LOC, complexity, function count, and comment ratio mapped to a 0-100 scale. Scores below 60 flag code for attention.

### 2. Refactoring Engine

Identifies refactoring opportunities across multiple dimensions:

```
┌───────────────────────────────────────────────────────┐
│                 Refactoring Engine                      │
│                                                         │
│  Detectors:                                             │
│  ├── Long Method (>50 lines)                            │
│  ├── Too Many Parameters (>5)                           │
│  ├── Deep Nesting (>4 levels)                           │
│  ├── Global Variable Usage                              │
│  ├── Missing Main Guard                                 │
│  └── Naming Quality (15+ patterns)                      │
│                                                         │
│  Output: RefactoringSuggestion[]                        │
│  ├── file_path, line_number                             │
│  ├── original_code, suggested_code                      │
│  ├── reason, effort (low/medium/high)                   │
│  ├── refactoring_type (enum)                            │
│  ├── risk_level, estimated_time_minutes                 │
│  └── dependencies                                       │
└───────────────────────────────────────────────────────┘
```

### 3. Security Scanner

Comprehensive OWASP-aligned vulnerability detection:

```
┌───────────────────────────────────────────────────────────┐
│                    Security Scanner                         │
│                                                             │
│  Vulnerability Patterns:                                    │
│  ├── SQL Injection (f-string in queries)        CWE-89     │
│  ├── XSS (innerHTML, document.write)            CWE-79     │
│  ├── Path Traversal (os.path.join + request)    CWE-22     │
│  ├── SSL Bypass (verify=False)                   CWE-295    │
│  ├── Insecure Deserialization (yaml.load)        CWE-502    │
│  ├── Overly Permissive CORS (allow_origins=*)    CWE-942    │
│  └── Weak RNG (random module for security)       CWE-330    │
│                                                             │
│  Risk Scoring:                                              │
│  ├── Critical = 10.0 pts                                   │
│  ├── High     =  7.5 pts                                   │
│  ├── Medium   =  5.0 pts                                   │
│  ├── Low      =  2.5 pts                                   │
│  └── Info     =  1.0 pts                                   │
│                                                             │
│  Risk Level: CRITICAL(≥50) HIGH(≥30) MEDIUM(≥15) LOW(≥5)  │
└───────────────────────────────────────────────────────────┘
```

### 4. Code Quality Manager

Enforces quality standards and runs quality gates:

```
┌─────────────────────────────────────────────────────┐
│               Code Quality Manager                    │
│                                                       │
│  Standards (configurable):                            │
│  ├── Max function length:        30 lines             │
│  ├── Max class length:          300 lines             │
│  ├── Max cyclomatic complexity:  10                   │
│  ├── Min test coverage:         80%                   │
│  ├── Max line length:          120 chars              │
│  ├── Min docstring coverage:   70%                    │
│  ├── Max nesting depth:          4 levels             │
│  └── Max params per function:    5                    │
│                                                       │
│  Quality Gate Flow:                                   │
│  ┌──────┐  ┌──────────┐  ┌────────────┐             │
│  │ CHECK├─▶│  PASS/    ├─▶│   RESULT   │             │
│  │      │  │  FAIL     │  │  GATE      │             │
│  └──────┘  └──────────┘  └────────────┘             │
│                                                       │
│  Technical Debt Estimation:                           │
│  ├── Critical issues: 4.0 hours each                  │
│  ├── High issues:     2.0 hours each                  │
│  ├── Medium issues:   0.5 hours each                  │
│  ├── Low issues:      0.25 hours each                 │
│  └── Info issues:     0.1 hours each                  │
└─────────────────────────────────────────────────────┘
```

### 5. Testing Strategies Engine

```
┌─────────────────────────────────────────────────────────┐
│                Testing Strategies                         │
│                                                           │
│  Test Plan Generation:                                   │
│  ├── Scan for classes → instantiation + method tests      │
│  ├── Scan for functions → happy path + edge + error       │
│  └── Suggest test types (unit, integration, e2e)          │
│                                                           │
│  Coverage Calculation:                                   │
│  └── coverage = tested_lines / total_lines × 100          │
│                                                           │
│  Test Quality Assessment:                                │
│  ├── Assertion density    (assertions per test)           │
│  ├── Setup utilization    (fixtures/setUp usage)          │
│  ├── Mocking adoption     (dependency isolation)          │
│  └── Quality Score (0-100 composite)                     │
└─────────────────────────────────────────────────────────┘
```

### 6. Documentation Generator

```
┌────────────────────────────────────────────────────────┐
│              Documentation Generator                     │
│                                                          │
│  Outputs:                                                │
│  ├── API Reference docs (classes, functions, signatures) │
│  ├── Changelog entries (version, date, categories)       │
│  ├── README templates (installation, usage, config)      │
│  ├── Type stub files (.pyi)                              │
│  └── Internal documentation tree (DocumentationNode)     │
│                                                          │
│  Source: AST-style regex extraction from source code     │
│  Target: Markdown, .pyi, YAML                            │
└────────────────────────────────────────────────────────┘
```

### 7. CI/CD Pipeline Manager

```
┌──────────────────────────────────────────────────────────┐
│                  CI/CD Pipeline Manager                    │
│                                                            │
│  Default Pipeline Stages:                                 │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────────┐                │
│  │ LINT ├▶│BUILD ├▶│ TEST ├▶│SECURITY  │                │
│  │ 5min │ │15min │ │20min │ │SCAN 10m  │                │
│  └──────┘ └──────┘ └──────┘ └────┬─────┘                │
│                                   │                       │
│  ┌───────────────┐ ┌───────────┐ ┌▼─────────┐           │
│  │   MONITOR     │◀│DEPLOY PROD│◀│DEPLOY    │           │
│  │   10min       │ │  20min    │ │STAGING   │           │
│  └───────────────┘ └───────────┘ │  15min   │           │
│                                   └──────────┘           │
│  Outputs:                                                 │
│  ├── PipelineConfig (stages, triggers, env vars)          │
│  ├── GitHub Actions YAML                                  │
│  └── Simulated execution results                          │
└──────────────────────────────────────────────────────────┘
```

### 8. Performance Optimizer

```
┌──────────────────────────────────────────────────────────┐
│                 Performance Optimizer                      │
│                                                            │
│  Anti-Pattern Detection:                                  │
│  ├── Triple-nested loops (O(n^3))                         │
│  ├── String concatenation in loops                        │
│  ├── Global variable access patterns                      │
│  ├── Repeated function calls (≥3x same call)              │
│  ├── range(len()) instead of enumerate()                  │
│  └── Append-in-loop (list comprehension candidate)        │
│                                                            │
│  Profiling:                                                │
│  ├── Per-function avg time                                 │
│  ├── Call count tracking                                   │
│  └── Threshold-based pass/fail                             │
│                                                            │
│  Optimization Potential: HIGH(≥9) MEDIUM(≥4) LOW          │
└──────────────────────────────────────────────────────────┘
```

### 9. Code Review Assistant

```
┌──────────────────────────────────────────────────────────┐
│                Code Review Assistant                        │
│                                                            │
│  Diff Analysis:                                            │
│  ├── TODO/FIXME markers          → INFO                   │
│  ├── Hardcoded passwords         → CRITICAL               │
│  ├── Bare/broad exceptions       → MEDIUM                 │
│  ├── Debug print statements      → LOW                    │
│  ├── Lines exceeding 120 chars   → INFO                   │
│  ├── eval()/exec() usage         → HIGH                   │
│  └── Old-style string formatting → INFO                   │
│                                                            │
│  Review Summary:                                           │
│  ├── Total comments, unresolved count                      │
│  ├── Breakdown by severity and category                    │
│  └── Approval recommendation (approve / request_changes)   │
└──────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### Complete Analysis Flow

```
                         ┌─────────────────┐
                         │  Source Code /   │
                         │  Project Path    │
                         └────────┬────────┘
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │   Development Dashboard   │
                    │   (Orchestrator)           │
                    └──────────┬───────────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
  │ Static         │  │ Security       │  │ Performance    │
  │ Analysis       │  │ Scanner        │  │ Optimizer      │
  │ Engine         │  │                │  │                │
  └───────┬────────┘  └───────┬────────┘  └───────┬────────┘
          │                   │                   │
          ▼                   ▼                   ▼
  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
  │ CodeIssue[]    │  │ SecurityVuln[] │  │ PerfMetric[]   │
  └───────┬────────┘  └───────┬────────┘  └───────┬────────┘
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
                              ▼
                    ┌──────────────────────┐
                    │   Unified Results    │
                    │   (JSON / Dict)      │
                    └──────────────────────┘
```

### Code Generation Flow

```
  ┌──────────────────┐
  │ Generation       │
  │ Request          │
  │ (type + params)  │
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐     ┌───────────────┐
  │ CodeGeneration   │────▶│   Template    │
  │ Engine           │     │   Library     │
  └────────┬─────────┘     └───────────────┘
           │
           ├── class  → generate_class()
           ├── api    → generate_api_endpoint()
           ├── test   → generate_unit_test()
           ├── docs   → generate_api_docs()
           ├── readme → generate_readme_template()
           ├── pipeline → generate_github_actions_config()
           └── changelog → generate_changelog()
```

### Security Scanning Flow

```
  ┌──────────────────┐
  │  Source Code      │
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────────────────────────┐
  │  Security Scanner                     │
  │                                        │
  │  For each VULNERABILITY_PATTERN:       │
  │  ┌────────────────────────────────┐   │
  │  │ Regex match against each line  │   │
  │  │ Assign CWE ID                  │   │
  │  │ Create SecurityVulnerability   │   │
  │  └────────────────────────────────┘   │
  │                                        │
  │  Aggregate → calculate_risk_score()    │
  └───────────────┬──────────────────────┘
                  │
                  ▼
  ┌──────────────────────────────────────┐
  │  Risk Assessment                      │
  │  ├── Total risk score                 │
  │  ├── Risk level (CRITICAL→INFO)       │
  │  ├── Breakdown by category            │
  │  └── Breakdown by severity            │
  └──────────────────────────────────────┘
```

---

## Design Patterns

### Strategy Pattern — Analysis Engines

Each analysis engine implements the `AnalysisEngine` abstract base class. The
Dashboard can swap engines independently:

```python
class AnalysisEngine(ABC):
    @abstractmethod
    def analyze(self, source_code: str, file_path: str) -> Dict[str, Any]: ...

    @abstractmethod
    def get_engine_name(self) -> str: ...
```

Engines conforming to this interface: `StaticAnalysisEngine`, `CodeRefactoringEngine`.
Others (Security, Performance, Testing) follow the same pattern without inheriting
the ABC, enabling independent evolution.

### Composite Pattern — Documentation Tree

The `DocumentationNode` dataclass forms a tree structure where nodes reference
children by ID. This supports nested documentation structures:

```
DocumentationNode
├── node_id
├── title
├── content
├── children[] → [DocumentationNode, ...]
└── parent_id
```

### Builder Pattern — Pipeline Configuration

`CICDPipeline.generate_pipeline_config()` acts as a builder, assembling a
`PipelineConfig` from project type and framework inputs, then registering it:

```python
config = pipeline.generate_pipeline_config("python", "fastapi")
pipeline.create_pipeline(config)
pipeline.simulate_pipeline_run(config.pipeline_id)
```

### Facade Pattern — Development Dashboard

The `DevelopmentDashboard` acts as a facade, providing a simplified interface
to the complex subsystem of 10+ engines. Consumers interact with:

```python
dashboard = DevelopmentDashboard()
results = dashboard.analyze_code(source_code, file_path)
generated = dashboard.generate_code("class", parameters)
```

### Observer Pattern — Quality Gates

Quality gate checks emit results that downstream processes can consume.
Each check in the gate produces a pass/fail record:

```
QualityGateResult
├── gate_name
├── status (PASSED / FAILED / WARNING)
├── checks[] → [{name, status, actual, threshold}, ...]
├── summary
└── timestamp
```

---

## Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Language** | Python 3.10+ | Type hints, dataclasses, pattern matching |
| **Type System** | typing + dataclasses | Runtime-checkable data contracts |
| **Testing** | pytest / unittest | Industry standard, rich ecosystem |
| **Linting** | flake8 / ruff / mypy | Style enforcement and type checking |
| **CI/CD** | GitHub Actions | Native GitHub integration |
| **Security** | Custom regex + CWE mapping | Lightweight, no external dependencies |
| **Documentation** | Markdown + auto-generation | Human-readable, version-controllable |
| **Logging** | Python logging module | Structured, leveled, configurable |
| **Regex Engine** | Python re | Built-in, no external dependency |
| **Math** | Python math | Halstead volume, maintainability index |

---

## Security Architecture

### Threat Model

```
┌──────────────────────────────────────────────────────────┐
│                    Threat Boundaries                       │
│                                                            │
│  External Threats:                                         │
│  ├── Malicious source code input (injection payloads)      │
│  ├── Path traversal via file_path parameters               │
│  ├── Resource exhaustion (huge files, deep recursion)      │
│  └── Supply chain attacks (dependency scanning)            │
│                                                            │
│  Internal Threats:                                         │
│  ├── Regex denial of service (ReDoS)                       │
│  ├── Memory exhaustion (unbounded issue collection)        │
│  └── Information leakage (verbose error messages)          │
│                                                            │
│  Mitigations:                                              │
│  ├── Input size limits on source code analysis             │
│  ├── Timeout enforcement on all engine operations          │
│  ├── Sanitized file paths (no directory traversal)         │
│  ├── Capped collection sizes (max issues per file)         │
│  └── Structured logging without sensitive data exposure    │
└──────────────────────────────────────────────────────────┘
```

### Security Controls

| Control | Implementation | Layer |
|---------|---------------|-------|
| Input validation | File path sanitization, size limits | Dashboard |
| Regex safety | Avoid backtracking-heavy patterns | Engines |
| Error handling | Try/except with structured logging | All |
| Dependency scanning | CVE database matching | DependencyAnalyzer |
| Secret detection | Pattern-based hardcoded secret scanning | StaticAnalysis |
| OWASP alignment | CWE IDs mapped to findings | SecurityScanner |

---

## Scalability Patterns

### Vertical Scaling

```
Single-Process Architecture:
┌──────────────────────────────────────┐
│           Dashboard                   │
│  ┌──────┐ ┌──────┐ ┌──────┐        │
│  │Engine│ │Engine│ │Engine│  ...    │
│  └──────┘ └──────┘ └──────┘        │
│                                       │
│  Processing: Sequential per file     │
│  Memory: Linear with file count      │
│  Suitable for: <1000 files           │
└──────────────────────────────────────┘
```

### Horizontal Scaling

```
Distributed Architecture:
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Worker 1 │  │ Worker 2 │  │ Worker 3 │
│ (Engine  │  │ (Engine  │  │ (Engine  │
│  subset) │  │  subset) │  │  subset) │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │              │              │
     ▼              ▼              ▼
┌──────────────────────────────────────┐
│         Result Aggregator             │
│  (Merge issues, metrics, vulns)      │
└──────────────────────────────────────┘
```

### Caching Strategy

```
┌────────────────────────────────────────────────────────┐
│                   Caching Layers                         │
│                                                          │
│  L1 — In-Engine Cache:                                  │
│  ├── Pattern compilation cache                          │
│  └── Metrics computation cache (per file hash)          │
│                                                          │
│  L2 — Dashboard Cache:                                  │
│  ├── File analysis results (content hash → results)     │
│  └── Project-level aggregated metrics                   │
│                                                          │
│  Invalidation:                                           │
│  ├── File modification timestamp change                  │
│  └── Explicit cache.clear() on config change             │
└────────────────────────────────────────────────────────┘
```

---

## Testing Architecture

### Test Pyramid

```
                    ┌─────────┐
                    │  E2E    │  5%
                    │  Tests  │
                   ┌┴─────────┴┐
                   │Integration │  15%
                   │   Tests    │
                  ┌┴───────────┴┐
                  │    Unit      │  80%
                  │    Tests     │
                  └─────────────┘
```

### Test Categories

| Category | Scope | Framework | Purpose |
|----------|-------|-----------|---------|
| Unit | Single method/class | pytest | Correctness of individual units |
| Integration | Engine interactions | pytest | Cross-engine data flow |
| Regression | Previously fixed bugs | pytest | Ensure bugs stay fixed |
| Performance | Timing thresholds | pytest-benchmark | Catch regressions |
| Security | Vulnerability detection | custom | Verify scanner accuracy |

---

## CI/CD Pipeline Architecture

### Pipeline Stages

```
┌──────────────────────────────────────────────────────────────┐
│                   CI/CD Pipeline                               │
│                                                                │
│  Trigger: push / pull_request / schedule / manual              │
│                                                                │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────────┐      │
│  │  LINT  ├──▶│ BUILD  ├──▶│  TEST  ├──▶│  SECURITY  │      │
│  │ ruff   │   │  pip   │   │ pytest │   │   scan     │      │
│  │ mypy   │   │  build │   │ cov    │   │   custom   │      │
│  └────────┘   └────────┘   └────────┘   └─────┬──────┘      │
│                                                 │              │
│  ┌──────────────┐   ┌────────┐   ┌─────────┐   │              │
│  │   MONITOR    │◀──│DEPLOY  │◀──│ DEPLOY  │◀──┘              │
│  │   alerts     │   │ PROD   │   │ STAGING │                  │
│  └──────────────┘   └────────┘   └─────────┘                  │
└──────────────────────────────────────────────────────────────┘
```

### Quality Gates Between Stages

```
LINT ──pass──▶ BUILD ──pass──▶ TEST ──pass──▶ SECURITY SCAN
  │ fail          │ fail          │ fail            │ fail
  ▼               ▼               ▼                ▼
BLOCKED        BLOCKED         BLOCKED           BLOCKED
(annotated)   (annotated)     (annotated)      (annotated)
```

---

## Monitoring & Observability

### Metrics Collected

| Metric | Type | Purpose |
|--------|------|---------|
| `analysis.files_processed` | Counter | Throughput tracking |
| `analysis.issues_found` | Histogram | Issue distribution |
| `analysis.duration_ms` | Timer | Performance monitoring |
| `security.vulnerabilities` | Counter | Security posture |
| `quality.gate_result` | Gauge | Quality trends |
| `cicd.pipeline_duration` | Timer | Pipeline health |

### Logging Levels

```
DEBUG   → Pattern match details, metric calculations
INFO    → Analysis start/end, issue counts, gate results
WARNING → Unrecognized patterns, degraded functionality
ERROR   → Analysis failures, invalid input, timeout
CRITICAL→ System-level failures (should not occur)
```

---

## Deployment Topology

### Standalone Mode

```
┌─────────────────────────┐
│  Development Agent       │
│  (Single Process)       │
│                          │
│  Dashboard + All Engines │
│  In-memory State         │
│  CLI / Script Interface  │
└─────────────────────────┘
```

### Service Mode

```
┌──────────────────────────────────────────────────┐
│  API Gateway / Load Balancer                       │
└─────────────────┬────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌────────┐  ┌────────┐  ┌────────┐
│Agent   │  │Agent   │  │Agent   │
│Replica │  │Replica │  │Replica │
│  1     │  │  2     │  │  3     │
└────────┘  └────────┘  └────────┘
    │             │             │
    └─────────────┼─────────────┘
                  │
        ┌─────────▼─────────┐
        │  Shared Cache /   │
        │  Result Store     │
        └───────────────────┘
```

---

## Configuration Reference

### Engine Configuration

Each engine accepts configuration via constructor parameters or class attributes.
Override defaults before instantiation:

```python
# Customize quality standards
from agents.development.agent import CodeQualityManager
manager = CodeQualityManager()
manager.standards["max_complexity"] = {"value": 15, "unit": " McCabe"}

# Add custom security patterns
from agents.development.agent import StaticAnalysisEngine, IssueType, IssueSeverity
engine = StaticAnalysisEngine()
engine.SECURITY_PATTERNS.append((
    r'my_custom_pattern', IssueType.SECURITY, IssueSeverity.HIGH,
    "Custom vulnerability", "Custom remediation"
))
```

### Pipeline Configuration

```python
from agents.development.agent import CICDPipeline, PipelineConfig, CICDStage
pipeline = CICDPipeline()
config = PipelineConfig(
    pipeline_id="custom-pipeline",
    name="Custom Pipeline",
    stages=[CICDStage.LINT, CICDStage.TEST, CICDStage.DEPLOY_PRODUCTION],
    triggers=["push", "schedule"],
    environment_variables={"PYTHON_VERSION": "3.12"},
    timeout_minutes=30,
)
pipeline.create_pipeline(config)
```

---

## Error Handling Patterns

### Engine-Level Error Handling

Each engine wraps its analysis in try/except blocks and returns partial results
on failure rather than raising exceptions:

```python
try:
    issues = engine.scan_for_issues(source_code, file_path)
except Exception as e:
    logger.error("Analysis failed for %s: %s", file_path, e)
    issues = []  # Graceful degradation
```

### Dashboard Orchestration

The Dashboard calls each engine independently, so a failure in one engine
does not prevent others from completing:

```python
results = {}
for name, engine in engines.items():
    try:
        results[name] = engine.analyze(source_code, file_path)
    except Exception as e:
        logger.error("Engine %s failed: %s", name, e)
        results[name] = {"error": str(e)}
```

### Pipeline Failure Handling

Pipeline stages use pass/fail status with optional retry logic. Failed stages
block subsequent stages and emit detailed failure reports.

---

## Extension Points

The architecture supports extension through:

1. **New Analysis Engines** — Implement `AnalysisEngine` interface and register with Dashboard
2. **Custom Patterns** — Add tuples to `SECURITY_PATTERNS` or `QUALITY_PATTERNS`
3. **New Generation Templates** — Extend `CodeGenerationEngine` with new `generate_*` methods
4. **Pipeline Stages** — Add entries to `CICDPipeline.DEFAULT_STAGES`
5. **Architecture Patterns** — Register new patterns in `ArchitecturePatterns.PATTERN_DESCRIPTIONS`
6. **Quality Standards** — Override `CodeQualityManager.standards` dict

---

## Appendix: Data Model Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                  Data Model Relationships                     │
│                                                               │
│  DevelopmentDashboard                                         │
│  ├── composes → StaticAnalysisEngine                          │
│  │               └── produces → CodeIssue[]                   │
│  ├── composes → CodeRefactoringEngine                         │
│  │               └── produces → RefactoringSuggestion[]       │
│  ├── composes → SecurityScanner                               │
│  │               └── produces → SecurityVulnerability[]       │
│  ├── composes → PerformanceOptimizer                          │
│  │               └── produces → PerformanceMetric[]           │
│  ├── composes → TestingStrategies                             │
│  │               └── produces → TestResult[]                  │
│  ├── composes → CodeQualityManager                            │
│  │               └── produces → QualityGateResult             │
│  ├── composes → DocumentationGenerator                        │
│  │               └── produces → DocumentationNode[], str      │
│  ├── composes → CICDPipeline                                  │
│  │               └── produces → PipelineConfig, Dict results  │
│  ├── composes → CodeGenerationEngine                          │
│  │               └── produces → str (generated code)          │
│  ├── composes → DependencyAnalyzer                            │
│  │               └── produces → DependencyInfo[], score       │
│  ├── composes → CodeReviewAssistant                           │
│  │               └── produces → CodeReviewComment[]           │
│  └── composes → ArchitecturePatterns                          │
│                  └── produces → recommendation[], detected    │
└─────────────────────────────────────────────────────────────┘
```

---

*Architecture version: 2.0.0 — Last updated: 2026-07-06*
