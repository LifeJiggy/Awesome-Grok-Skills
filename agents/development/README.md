# Development Agent

> Comprehensive software development analysis, generation, and quality assurance toolkit.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Static Analysis](#static-analysis)
  - [Security Scanning](#security-scanning)
  - [Refactoring](#refactoring)
  - [Code Generation](#code-generation)
  - [Testing Strategies](#testing-strategies)
  - [Code Quality](#code-quality)
  - [Documentation Generation](#documentation-generation)
  - [CI/CD Pipelines](#cicd-pipelines)
  - [Performance Optimization](#performance-optimization)
  - [Code Review](#code-review)
  - [Architecture Patterns](#architecture-patterns)
- [API Reference](#api-reference)
  - [DevelopmentDashboard](#developmentdashboard)
  - [StaticAnalysisEngine](#staticanalysisengine)
  - [SecurityScanner](#securityscanner)
  - [CodeRefactoringEngine](#coderefactoringengine)
  - [TestingStrategies](#testingstrategies)
  - [CodeQualityManager](#codequalitymanager)
  - [DocumentationGenerator](#documentationgenerator)
  - [CICDPipeline](#cicdpipeline)
  - [PerformanceOptimizer](#performanceoptimizer)
  - [CodeReviewAssistant](#codereviewassistant)
  - [ArchitecturePatterns](#architecturepatterns)
  - [DependencyAnalyzer](#dependencyanalyzer)
- [Data Models](#data-models)
  - [Enums](#enums)
  - [Dataclasses](#dataclasses)
- [Configuration](#configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Development Agent is a comprehensive software development analysis and generation
system designed for modern development workflows. It provides 12 interconnected engines
covering the full software development lifecycle:

- **Static Analysis** — Pattern-based code issue detection with CWE mapping
- **Security Scanning** — OWASP-aligned vulnerability detection with risk scoring
- **Refactoring** — Automated identification of code improvement opportunities
- **Code Generation** — Boilerplate, tests, documentation, and pipeline configs
- **Testing Strategies** — Test plan generation and quality assessment
- **Code Quality** — Configurable quality gates and technical debt estimation
- **Documentation** — API docs, changelogs, README templates, type stubs
- **CI/CD Pipelines** — Pipeline configuration and GitHub Actions generation
- **Performance** — Anti-pattern detection and profiling
- **Code Review** — Diff analysis with structured feedback
- **Architecture** — Pattern detection and recommendation
- **Dependencies** — Vulnerability and license analysis

### Key Differentiators

| Feature | Development Agent | Generic Linters |
|---------|-------------------|-----------------|
| Security + CWE mapping | Yes | Limited |
| Architecture pattern detection | Yes | No |
| CI/CD pipeline generation | Yes | No |
| Technical debt estimation | Yes | No |
| Risk scoring | Yes | No |
| Code generation | Yes | No |
| Documentation generation | Yes | No |
| 12 integrated engines | Yes | 1-2 |

---

## Features

### Static Analysis Engine
- 13 security patterns (hardcoded secrets, SQL injection, eval/exec, pickle, subprocess)
- 12 quality patterns (TODO/FIXME, bare except, print statements, pass blocks)
- Cyclomatic complexity (McCabe)
- Halstead volume estimation
- Maintainability index (0-100 scale)
- Detailed metrics (LOC, comments, functions, classes, imports, line lengths)

### Security Scanner
- 7 OWASP-aligned vulnerability categories
- CWE ID mapping for each finding
- Risk scoring (0-100 scale with severity levels)
- Category and severity breakdowns
- Concrete remediation steps

### Refactoring Engine
- Long method detection (>50 lines)
- Parameter count analysis (>5 parameters)
- Nesting depth analysis (>4 levels)
- Global variable detection
- 15+ naming quality patterns
- Main guard detection
- Effort and risk estimation per suggestion

### Code Generation
- Python classes with type hints, docstrings, repr, eq
- FastAPI-style API endpoints with auth support
- Unit tests (pytest and unittest frameworks)
- API reference documentation (Markdown)
- README templates
- GitHub Actions workflow YAML
- Changelog entries
- Type stub files (.pyi)

### Testing Strategies
- Test plan generation from source code
- Test quality assessment (assertion density, mocking, setup)
- Coverage calculation
- Test type recommendations

### Code Quality Manager
- 9 configurable quality standards
- Quality gate evaluation (pass/fail with check details)
- Technical debt estimation (hours by severity)
- Debt breakdown by issue type

### CI/CD Pipeline
- 8-stage default pipeline (lint → build → test → security → staging → integration → production → monitor)
- GitHub Actions YAML generation
- Pipeline simulation with timing
- Configurable triggers and environment variables

### Performance Optimizer
- Nested loop detection (O(n^3) and worse)
- String concatenation in loops
- Repeated computation detection
- range(len()) anti-pattern
- Append-in-loop optimization candidates
- Function profiling with threshold-based pass/fail

### Code Review Assistant
- Diff analysis with 7 issue types
- Structured review comments with severity
- Review summary with approval recommendation
- Category and severity breakdowns

### Architecture Patterns
- Pattern fit analysis based on project type, team size, scale
- 6 supported patterns (MVC, Microservices, Event-Driven, Clean, Hexagonal, Repository)
- Codebase pattern detection from source code
- Confidence scoring

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                      CONSUMER LAYER                               │
│   CLI  │  API Gateway  │  Web UI  │  CI/CD Webhook  │  SDK      │
└────────┬──────────┬──────────┬──────────┬──────────────┬────────┘
         │          │          │          │              │
         ▼          ▼          ▼          ▼              ▼
┌──────────────────────────────────────────────────────────────────┐
│                   DEVELOPMENT DASHBOARD                            │
│                                                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────────────┐   │
│  │  Static  │ │Refactoring│ │ Security │ │   Performance      │   │
│  │ Analysis │ │  Engine   │ │ Scanner  │ │    Optimizer       │   │
│  └──────────┘ └──────────┘ └──────────┘ └────────────────────┘   │
│                                                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────────────┐   │
│  │ Testing  │ │   Code   │ │  CI/CD   │ │   Documentation    │   │
│  │Strategies│ │ Quality  │ │ Pipeline │ │   Generator        │   │
│  └──────────┘ └──────────┘ └──────────┘ └────────────────────┘   │
│                                                                    │
│  ┌──────────┐ ┌──────────┐                                        │
│  │Dependency│ │   Code   │                                        │
│  │ Analyzer │ │Generation│                                        │
│  └──────────┘ └──────────┘                                        │
└──────────────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for the full system architecture.

---

## Quick Start

### Minimal Example

```python
from agents.development.agent import DevelopmentDashboard

dashboard = DevelopmentDashboard()

source = '''
password = "admin123"
def get_user(user_id):
    return eval(f"db.query({user_id})")
'''

results = dashboard.analyze_code(source, "auth.py")
print(f"Issues: {results['static_analysis']['issue_count']}")
print(f"Security vulns: {len(results['security'])}")
```

### Run the Agent Directly

```bash
python agents/development/agent.py
```

### Analyze a Project

```python
from agents.development.agent import DevelopmentDashboard
from pathlib import Path

dashboard = DevelopmentDashboard()

for py_file in Path("src").rglob("*.py"):
    source = py_file.read_text(encoding="utf-8")
    result = dashboard.analyze_code(source, str(py_file))
    issues = result["static_analysis"]["issue_count"]
    vulns = len(result["security"])
    if issues > 0 or vulns > 0:
        print(f"{py_file}: {issues} issues, {vulns} vulnerabilities")
```

---

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/awesome-grok-skills/development-agent.git
cd development-agent

# Install dependencies (none required — pure Python)
pip install -e .
```

### Requirements

- Python 3.10 or higher
- No external dependencies (uses only stdlib modules: `re`, `ast`, `math`, `logging`, `hashlib`, `json`, `time`, `collections`, `pathlib`, `datetime`, `abc`, `textwrap`, `keyword`)

---

## Usage

### Static Analysis

```python
from agents.development.agent import StaticAnalysisEngine

engine = StaticAnalysisEngine()

results = engine.analyze(source_code, "module.py")
print(f"Lines of code: {results['lines_of_code']}")
print(f"Issues found: {results['issue_count']}")
print(f"Cyclomatic complexity: {results['complexity']}")
print(f"Maintainability index: {results['maintainability_index']}")

for issue in results["issues"]:
    print(f"  [{issue['severity']}] {issue['message']} (line {issue['line']})")
```

### Security Scanning

```python
from agents.development.agent import SecurityScanner

scanner = SecurityScanner()
vulns = scanner.scan_source(source_code, "app.py")

risk = scanner.calculate_risk_score(vulns)
print(f"Risk level: {risk['risk_level']}")
print(f"Total score: {risk['total_risk_score']}")
print(f"Vulnerabilities: {risk['total_vulnerabilities']}")

for v in vulns:
    print(f"  [{v.severity.name}] {v.title} ({v.cwe_id})")
```

### Refactoring

```python
from agents.development.agent import CodeRefactoringEngine

engine = CodeRefactoringEngine()
suggestions = engine.analyze_for_refactoring(source_code, "module.py")

for s in suggestions:
    print(f"  [{s.effort}] {s.reason}")
    print(f"    Original: {s.original_code[:50]}...")
    print(f"    Suggested: {s.suggested_code[:50]}...")
```

### Code Generation

```python
from agents.development.agent import DevelopmentDashboard

dashboard = DevelopmentDashboard()

# Generate a Python class
class_code = dashboard.generate_code("class", {
    "name": "UserService",
    "attributes": ["user_id", "name", "email"],
    "methods": ["create", "update", "delete", "get_by_id"],
})
print(class_code)

# Generate unit tests
test_code = dashboard.generate_code("test", {
    "class_name": "UserService",
    "test_cases": [
        {"name": "create_user", "call": "service.create('Alice')", "assertion": "IsNotNone(result)"},
        {"name": "get_nonexistent", "call": "service.get_by_id(999)", "assertion": "IsNone(result)"},
    ],
})
print(test_code)
```

### Testing Strategies

```python
from agents.development.agent import TestingStrategies

tester = TestingStrategies()
plan = tester.generate_test_plan(source_code, "module.py")

print(f"Test cases planned: {plan['total_test_cases']}")
print(f"Coverage target: {plan['coverage_target']}%")

for tc in plan["test_cases"]:
    print(f"  {tc.get('function', tc.get('class', 'unknown'))}:")
    for case in tc.get("cases", []):
        print(f"    - {case['name']}")
```

### Code Quality

```python
from agents.development.agent import CodeQualityManager

manager = CodeQualityManager()

# Check against standards
gate = manager.evaluate_quality_gate({
    "avg_complexity": 8,
    "avg_maintainability": 72,
    "test_coverage": 85,
    "issues_by_severity": {"critical": 0, "high": 2},
})

print(f"Gate status: {gate.status.value}")
for check in gate.checks:
    print(f"  {check['name']}: {check['status']}")

# Estimate technical debt
debt = manager.calculate_technical_debt(issues)
print(f"Estimated debt: {debt['total_hours']} hours")
```

### Documentation Generation

```python
from agents.development.agent import DocumentationGenerator

doc_gen = DocumentationGenerator()

# Generate API docs
api_docs = doc_gen.generate_api_docs(source_code, "My API")

# Generate changelog
changelog = doc_gen.generate_changelog([
    {"category": "added", "description": "New feature X"},
    {"category": "fixed", "description": "Bug in module Y"},
], version="2.1.0")

# Generate README template
readme = doc_gen.generate_readme_template("MyProject", "An awesome project")
```

### CI/CD Pipelines

```python
from agents.development.agent import CICDPipeline

pipeline = CICDPipeline()

# Auto-generate pipeline
config = pipeline.generate_pipeline_config("python", "fastapi")
print(f"Pipeline: {config.name}")
print(f"Stages: {[s.value for s in config.stages]}")

# Simulate execution
results = pipeline.simulate_pipeline_run(config.pipeline_id)
print(f"Status: {results['overall_status']}")
print(f"Duration: {results['total_duration']}s")

# Generate GitHub Actions YAML
yaml = pipeline.generate_github_actions_config(config)
```

### Performance Optimization

```python
from agents.development.agent import PerformanceOptimizer

optimizer = PerformanceOptimizer()
perf = optimizer.analyze_performance(source_code, "compute.py")

print(f"Issues: {perf['issue_count']}")
print(f"Optimization potential: {perf['optimization_potential']}")

for issue in perf["performance_issues"]:
    print(f"  [{issue['severity']}] {issue['message']}")
```

### Code Review

```python
from agents.development.agent import CodeReviewAssistant

reviewer = CodeReviewAssistant()
comments = reviewer.review_diff(diff_content, "changes.py")

summary = reviewer.generate_review_summary(comments)
print(f"Recommendation: {summary['approval_recommendation']}")
print(f"Unresolved: {summary['unresolved_comments']}")

for comment in comments:
    print(f"  [{comment.severity.name}] Line {comment.line_number}: {comment.content}")
```

### Architecture Patterns

```python
from agents.development.agent import ArchitecturePatterns

arch = ArchitecturePatterns()

# Get recommendations
recs = arch.analyze_pattern_fit("web", 12, "high")
for r in recs:
    print(f"  {r['pattern'].value}: score={r['fit_score']} — {r['reason']}")

# Detect existing pattern
detected = arch.evaluate_codebase_pattern(source_code)
print(f"Detected: {detected['detected_pattern']} (confidence: {detected['confidence']})")
```

---

## API Reference

### DevelopmentDashboard

The main entry point orchestrating all analysis engines.

```python
class DevelopmentDashboard:
    def __init__(self) -> None
    def analyze_project(self, project_path: str) -> Dict[str, Any]
    def analyze_code(self, source_code: str, file_path: str = "analyzed.py") -> Dict[str, Any]
    def generate_code(self, request_type: str, parameters: Dict[str, Any]) -> str
```

**Parameters for `generate_code`:**

| request_type | Required Parameters | Optional Parameters |
|-------------|-------------------|-------------------|
| `"class"` | `name`, `attributes` | `methods`, `base_class`, `include_repr`, `include_eq` |
| `"api"` | `method`, `path`, `handler` | `request_model`, `response_model`, `auth_required` |
| `"test"` | `class_name`, `test_cases` | — |
| `"docs"` | `source_code` | `title` |
| `"readme"` | `project_name`, `description` | — |
| `"pipeline"` | `project_type`, `framework` | — |
| `"changelog"` | `changes` | `version` |

### StaticAnalysisEngine

```python
class StaticAnalysisEngine:
    def __init__(self) -> None
    def analyze(self, source_code: str, file_path: str = "") -> Dict[str, Any]
    def scan_for_issues(self, source_code: str, file_path: str = "") -> List[CodeIssue]
    def calculate_cyclomatic_complexity(self, source_code: str) -> int
    def calculate_halstead_volume(self, source_code: str) -> float
    def calculate_metrics(self, source_code: str) -> Dict[str, Any]
    def calculate_maintainability(self, metrics: Dict[str, Any], complexity: int) -> float
```

**Return values:**
- `analyze()` returns: `file`, `lines_of_code`, `total_lines`, `issues`, `issue_count`, `complexity`, `metrics`, `maintainability_index`, `timestamp`
- `calculate_metrics()` returns: `lines_of_code`, `total_lines`, `blank_lines`, `comment_lines`, `comment_ratio`, `function_count`, `class_count`, `import_count`, `average_line_length`, `max_line_length`, `long_lines_count`, `halstead_volume`

### SecurityScanner

```python
class SecurityScanner:
    def __init__(self) -> None
    def scan_source(self, source_code: str, file_path: str = "") -> List[SecurityVulnerability]
    def calculate_risk_score(self, vulns: List[SecurityVulnerability]) -> Dict[str, Any]
```

**Risk levels:** CRITICAL (≥50), HIGH (≥30), MEDIUM (≥15), LOW (≥5), INFO (<5)

### CodeRefactoringEngine

```python
class CodeRefactoringEngine:
    def __init__(self) -> None
    def analyze(self, source_code: str, file_path: str = "") -> Dict[str, Any]
    def analyze_for_refactoring(self, source_code: str, file_path: str = "") -> List[RefactoringSuggestion]
    def suggest_naming_improvements(self, source_code: str, file_path: str = "") -> List[RefactoringSuggestion]
```

### TestingStrategies

```python
class TestingStrategies:
    def __init__(self) -> None
    def generate_test_plan(self, source_code: str, file_path: str = "") -> Dict[str, Any]
    def calculate_test_coverage(self, tested_lines: Set[int], total_lines: int) -> float
    def assess_test_quality(self, test_code: str) -> Dict[str, Any]
```

### CodeQualityManager

```python
class CodeQualityManager:
    def __init__(self) -> None
    def evaluate_quality_gate(self, metrics: Dict[str, Any]) -> QualityGateResult
    def calculate_technical_debt(self, issues: List[CodeIssue]) -> Dict[str, Any]
```

### DocumentationGenerator

```python
class DocumentationGenerator:
    def __init__(self) -> None
    def generate_api_docs(self, source_code: str, title: str = "API Reference") -> str
    def generate_changelog(self, changes: List[Dict[str, str]], version: str = "1.0.0") -> str
    def generate_readme_template(self, project_name: str, description: str) -> str
    def generate_type_stubs(self, source_code: str) -> str
```

### CICDPipeline

```python
class CICDPipeline:
    def __init__(self) -> None
    def create_pipeline(self, config: PipelineConfig) -> PipelineConfig
    def generate_pipeline_config(self, project_type: str, framework: str) -> PipelineConfig
    def simulate_pipeline_run(self, pipeline_id: str) -> Dict[str, Any]
    def generate_github_actions_config(self, config: PipelineConfig) -> str
```

### PerformanceOptimizer

```python
class PerformanceOptimizer:
    def __init__(self) -> None
    def analyze_performance(self, source_code: str, file_path: str = "") -> Dict[str, Any]
    def profile_function(self, func_name: str, call_count: int, total_time_ms: float) -> PerformanceMetric
```

### CodeReviewAssistant

```python
class CodeReviewAssistant:
    def __init__(self) -> None
    def review_diff(self, diff_content: str, file_path: str = "") -> List[CodeReviewComment]
    def generate_review_summary(self, comments: List[CodeReviewComment]) -> Dict[str, Any]
```

### ArchitecturePatterns

```python
class ArchitecturePatterns:
    def __init__(self) -> None
    def analyze_pattern_fit(self, project_type: str, team_size: int, scale_requirements: str) -> List[Dict[str, Any]]
    def get_pattern_details(self, pattern: ArchitecturePattern) -> Dict[str, str]
    def evaluate_codebase_pattern(self, source_code: str) -> Dict[str, Any]
```

### DependencyAnalyzer

```python
class DependencyAnalyzer:
    def __init__(self) -> None
    def analyze_dependencies(self, package_file: str = "requirements.txt", lock_file: str = "") -> Dict[str, Any]
    def find_dependency_conflicts(self, dependencies: Dict[str, Any]) -> List[Dict[str, Any]]
    def compute_dependency_score(self, analysis: Dict[str, Any]) -> float
```

---

## Data Models

### Enums

| Enum | Values | Purpose |
|------|--------|---------|
| `IssueSeverity` | INFO, LOW, MEDIUM, HIGH, CRITICAL | Impact classification |
| `IssueType` | BUG, SECURITY, PERFORMANCE, CODE_QUALITY, STYLE, DOCUMENTATION, DESIGN, TESTING, MAINTENANCE | Issue category |
| `SecurityVulnCategory` | INJECTION, BROKEN_AUTH, XSS, SSRF, PATH_TRAVERSAL, etc. | OWASP category |
| `RefactoringType` | EXTRACT_METHOD, EXTRACT_CLASS, RENAME_VARIABLE, etc. | Transformation type |
| `TestType` | UNIT, INTEGRATION, FUNCTIONAL, PERFORMANCE, SECURITY, E2E, SMOKE, REGRESSION | Test category |
| `TestFramework` | PYTEST, UNITTEST, NOSE, ROBOT, JEST, MOCHA, JUNIT | Framework |
| `CICDStage` | LINT, BUILD, TEST, SECURITY_SCAN, DEPLOY_STAGING, etc. | Pipeline stage |
| `QualityGateStatus` | PASSED, FAILED, WARNING, SKIPPED | Gate result |
| `ArchitecturePattern` | MVC, MVVM, LAYERED, MICROSERVICES, EVENT_DRIVEN, etc. | Design pattern |
| `Language` | PYTHON, JAVASCRIPT, TYPESCRIPT, JAVA, GO, RUST, etc. | Programming language |

### Dataclasses

| Dataclass | Key Fields | Purpose |
|-----------|-----------|---------|
| `CodeIssue` | issue_id, file_path, line_number, issue_type, severity, message, suggestion | Code analysis finding |
| `SecurityVulnerability` | vuln_id, category, cwe_id, cvss_score, remediation | Security vulnerability |
| `RefactoringSuggestion` | refactoring_type, effort, risk_level, estimated_time_minutes | Refactoring recommendation |
| `TestResult` | test_name, test_type, status, duration_ms, coverage_percent | Test execution result |
| `PerformanceMetric` | metric_name, value, unit, threshold, status | Performance measurement |
| `QualityGateResult` | gate_name, status, checks, summary | Quality gate outcome |
| `PipelineConfig` | pipeline_id, stages, triggers, environment_variables | CI/CD configuration |
| `CodeReviewComment` | comment_id, category, severity, is_resolved | Review feedback |
| `DependencyInfo` | name, current_version, latest_version, license, is_vulnerable | Dependency metadata |
| `DocumentationNode` | node_id, title, content, children, parent_id | Documentation tree node |
| `ProjectMetrics` | total_files, languages, avg_complexity, test_coverage, technical_debt_hours | Project-level metrics |

---

## Configuration

### Quality Standards

The `CodeQualityManager` has configurable standards. Override defaults:

```python
from agents.development.agent import CodeQualityManager

manager = CodeQualityManager()

# Customize thresholds
manager.standards["max_complexity"] = {"value": 15, "unit": " McCabe"}
manager.standards["min_test_coverage"] = {"value": 70, "unit": "%"}
manager.standards["max_function_length"] = {"value": 50, "unit": "lines"}
```

### Security Patterns

Add custom security patterns to the `StaticAnalysisEngine`:

```python
from agents.development.agent import StaticAnalysisEngine, IssueType, IssueSeverity

engine = StaticAnalysisEngine()

# Add custom pattern
engine.SECURITY_PATTERNS.append((
    r'my_custom_vulnerable_pattern',
    IssueType.SECURITY,
    IssueSeverity.HIGH,
    "Custom vulnerability detected",
    "Apply custom remediation",
))
```

### Pipeline Configuration

Customize CI/CD pipeline defaults:

```python
from agents.development.agent import CICDPipeline, CICDStage, PipelineConfig

pipeline = CICDPipeline()

# Create custom pipeline
config = PipelineConfig(
    pipeline_id="my-pipeline",
    name="Custom Pipeline",
    stages=[CICDStage.LINT, CICDStage.TEST, CICDStage.DEPLOY_PRODUCTION],
    triggers=["push"],
    environment_variables={"PYTHON_VERSION": "3.12"},
    timeout_minutes=30,
)
pipeline.create_pipeline(config)
```

---

## Examples

### Example 1: Security Audit

```python
from agents.development.agent import SecurityScanner

scanner = SecurityScanner()

# Audit a web application
source = '''
import os
import yaml
import requests

password = "admin123"
db_password = os.getenv("DB_PASS", "default_pass")

config = yaml.load(open("config.yaml"), Loader=yaml.UnsafeLoader)
response = requests.get("https://api.internal", verify=False)
file_path = os.path.join("/uploads", request.args.get("file"))
result = eval(request.form.get("expression"))
'''

vulns = scanner.scan_source(source, "app.py")
risk = scanner.calculate_risk_score(vulns)

print(f"Security Audit Results:")
print(f"  Risk Level: {risk['risk_level']}")
print(f"  Total Score: {risk['total_risk_score']}")
print(f"  Vulnerabilities: {risk['total_vulnerabilities']}")
print()
for v in vulns:
    print(f"  [{v.severity.name}] {v.title}")
    print(f"    CWE: {v.cwe_id}")
    print(f"    Fix: {v.remediation}")
    print()
```

### Example 2: CI/CD Pipeline Setup

```python
from agents.development.agent import CICDPipeline

pipeline = CICDPipeline()

# Generate and run a pipeline for a Python/FastAPI project
config = pipeline.generate_pipeline_config("python", "fastapi")
yaml_content = pipeline.generate_github_actions_config(config)

print("Generated GitHub Actions workflow:")
print(yaml_content)
print()

# Simulate pipeline execution
results = pipeline.simulate_pipeline_run(config.pipeline_id)
print(f"Pipeline: {results['overall_status']}")
for stage in results["stages"]:
    print(f"  {stage['name']}: {stage['status']} ({stage['duration_seconds']}s)")
```

### Example 3: Comprehensive Project Analysis

```python
from agents.development.agent import DevelopmentDashboard
from pathlib import Path

dashboard = DevelopmentDashboard()
report = []

for py_file in Path("src").rglob("*.py"):
    source = py_file.read_text(encoding="utf-8")
    result = dashboard.analyze_code(source, str(py_file))

    issues = result["static_analysis"]["issue_count"]
    vulns = len(result["security"])
    perf = result["performance"]["issue_count"]
    refactor = result["refactoring"]["total_suggestions"]

    report.append({
        "file": str(py_file),
        "issues": issues,
        "vulnerabilities": vulns,
        "performance": perf,
        "refactoring": refactor,
    })

# Print summary
total_issues = sum(r["issues"] for r in report)
total_vulns = sum(r["vulnerabilities"] for r in report)
print(f"Analyzed {len(report)} files")
print(f"Total issues: {total_issues}")
print(f"Total vulnerabilities: {total_vulns}")

# Top files by issue count
top_files = sorted(report, key=lambda r: r["issues"], reverse=True)[:5]
print("\nTop 5 files by issues:")
for f in top_files:
    print(f"  {f['file']}: {f['issues']} issues, {f['vulnerabilities']} vulns")
```

---

## Best Practices

### 1. Run Analysis Early and Often

Integrate the Development Agent into your CI pipeline to catch issues before they reach production.

```yaml
# In your CI pipeline
- name: Code Analysis
  run: |
    python -c "
    from agents.development.agent import DevelopmentDashboard
    dashboard = DevelopmentDashboard()
    results = dashboard.analyze_code(open('${FILE}').read(), '${FILE}')
    issues = results['static_analysis']['issue_count']
    vulns = len(results['security'])
    if vulns > 0:
        raise SystemExit(f'Found {vulns} security vulnerabilities')
    "
```

### 2. Use Severity to Prioritize

Focus on CRITICAL and HIGH severity issues first. They represent the most significant risks:

```python
critical_issues = [i for i in issues if i["severity"] in ("CRITICAL", "HIGH")]
if critical_issues:
    print(f"Address {len(critical_issues)} critical/high issues first")
```

### 3. Combine Engines for Comprehensive Analysis

No single engine catches everything. Use the Dashboard for full coverage:

```python
results = dashboard.analyze_code(source, file_path)
# Combines: static analysis + security + performance + refactoring + testing + docs
```

### 4. Customize Standards for Your Team

One size doesn't fit all. Adjust quality thresholds to match your team's maturity:

```python
manager = CodeQualityManager()
# Start relaxed, tighten over time
manager.standards["min_test_coverage"] = {"value": 60, "unit": "%"}
```

### 5. Use Generated Code as Starting Points

Generated code (classes, tests, endpoints) is boilerplate — review and customize it:

```python
generated_class = dashboard.generate_code("class", params)
# Review and modify before using in production
```

---

## Troubleshooting

### "No issues found" when expecting some

- Verify the source code is non-empty
- Check that patterns are relevant to the language (current patterns are Python-focused)
- Ensure file_path is provided for accurate tracking

### High false positive rate

- Security patterns are intentionally broad — review manually
- Use `confidence` field to prioritize
- Add custom exclusion patterns for test directories

### Quality gate always fails

- Start with relaxed thresholds and tighten incrementally
- Check which specific checks are failing via `gate.checks`
- Address the failing metrics systematically

### Slow analysis on large files

- The agent uses regex-based analysis, which is O(n) per pattern
- For very large files (>10,000 lines), consider splitting
- Cache results for unchanged files

### Code generation produces incomplete output

- Verify all required parameters are provided
- Check `request_type` is one of: `class`, `api`, `test`, `docs`, `readme`, `pipeline`, `changelog`

---

## Contributing

### Development Setup

```bash
git clone https://github.com/awesome-grok-skills/development-agent.git
cd development-agent
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### Running Tests

```bash
python -m pytest tests/ -v
```

### Adding New Security Patterns

1. Define the regex pattern
2. Map to CWE ID and OWASP category
3. Assign severity based on exploitability
4. Add to `SecurityScanner.VULNERABILITY_PATTERNS`
5. Write tests to verify detection

### Adding New Refactoring Rules

1. Define the detection logic in `CodeRefactoringEngine`
2. Create `RefactoringSuggestion` with type, effort, risk
3. Add to the appropriate detector method
4. Write tests with both positive and negative cases

### Code Style

- Follow PEP 8
- Use type hints on all public methods
- Keep methods under 30 lines
- Document public APIs with docstrings
- Write tests for new features

---

## License

MIT License

Copyright (c) 2026 Awesome Grok Skills

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

*Documentation version: 2.0.0 — Last updated: 2026-07-06*
