---
name: "Code Analysis"
version: "2.0.0"
description: "Comprehensive code analysis toolkit with static analysis, code quality metrics, complexity analysis, dependency analysis, and technical debt assessment for software development"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["development", "code-analysis", "static-analysis", "quality", "complexity", "dependencies"]
category: "development"
personality: "code-analyst"
use_cases: ["static analysis", "code quality", "complexity analysis", "dependency analysis", "technical debt"]
---

# Code Analysis

> Production-grade code analysis framework providing static analysis, code quality metrics, complexity analysis, dependency analysis, and technical debt assessment for maintaining high-quality software.

## Overview

The Code Analysis module provides tools for evaluating code quality, identifying issues, and tracking technical debt. It implements static code analysis with customizable rules, cyclomatic and cognitive complexity measurement, dependency graph analysis, code duplication detection, and technical debt estimation. Every analysis produces actionable reports with prioritized recommendations.

## Core Capabilities

### 1. Static Analysis
- Custom rule definition and checking
- Dead code detection
- Unused import/variable detection
- Type safety verification
- Security vulnerability scanning

### 2. Code Quality Metrics
- Lines of code (LOC), comments, blank lines
- Maintainability index calculation
- Code-to-comment ratio
- Average function length
- File size distribution

### 3. Complexity Analysis
- Cyclomatic complexity per function
- Cognitive complexity measurement
- Nesting depth analysis
- Coupling metrics (CBO, RFC)
- Cohesion metrics (LCOM)

### 4. Dependency Analysis
- Import graph construction
- Circular dependency detection
- Dependency depth measurement
- External dependency auditing
- Version conflict detection

### 5. Duplication Detection
- Exact code duplication
- Near-miss duplication
- Semantic duplication
- Copy-paste pattern detection

### 6. Technical Debt
- Debt estimation in time/money
- Debt prioritization
- Trend tracking
- ROI calculation for debt paydown

## Usage Examples

### Static Analysis

```python
from code_analysis import StaticAnalyzer, Rule

analyzer = StaticAnalyzer()

# Add custom rules
analyzer.add_rule(Rule(
    name="no_print_statements",
    pattern=r"\bprint\s*\(",
    severity="warning",
    message="Avoid print statements in production code",
))

# Analyze a file
results = analyzer.analyze_file("app.py")
print(f"Issues found: {len(results.issues)}")
for issue in results.issues:
    print(f"  Line {issue.line}: [{issue.severity}] {issue.message}")
```

### Code Quality Metrics

```python
from code_analysis import QualityMetrics

metrics = QualityMetrics()

# Calculate metrics for a project
report = metrics.analyze_project("/path/to/project")
print(f"Total LOC: {report.total_loc:,}")
print(f"Functions: {report.total_functions}")
print(f"Classes: {report.total_classes}")
print(f"Average function length: {report.avg_function_length:.1f} lines")
print(f"Maintainability index: {report.maintainability_index:.1f}/100")
```

### Complexity Analysis

```python
from code_analysis import ComplexityAnalyzer

analyzer = ComplexityAnalyzer()

# Analyze function complexity
result = analyzer.analyze_function(complex_function)
print(f"Cyclomatic complexity: {result.cyclomatic}")
print(f"Cognitive complexity: {result.cognitive}")
print(f"Nesting depth: {result.max_nesting}")

if result.cyclomatic > 10:
    print("⚠ High complexity — consider refactoring")
```

### Dependency Analysis

```python
from code_analysis import DependencyAnalyzer

analyzer = DependencyAnalyzer()

# Analyze dependencies
deps = analyzer.analyze("/path/to/project")
print(f"Direct dependencies: {len(deps.direct)}")
print(f"Transitive dependencies: {len(deps.transitive)}")

# Check for circular dependencies
cycles = deps.find_cycles()
if cycles:
    print(f"Circular dependencies: {len(cycles)}")
    for cycle in cycles:
        print(f"  {' → '.join(cycle)}")
```

## Best Practices

### Static Analysis
- Integrate static analysis into CI/CD pipeline
- Configure rules based on project conventions
- Use auto-fix capabilities where available
- Review and update rules regularly

### Code Quality
- Set minimum maintainability index threshold
- Track metrics over time for trends
- Use metrics to guide refactoring priorities
- Share metrics with the team

### Complexity
- Keep cyclomatic complexity below 10 per function
- Refactor functions with high cognitive complexity
- Use early returns to reduce nesting
- Break complex functions into smaller ones

### Dependencies
- Audit dependencies regularly for vulnerabilities
- Minimize transitive dependency count
- Pin dependency versions for reproducibility
- Remove unused dependencies

## Related Modules

- **refactoring-patterns**: Code refactoring techniques
- **design-patterns**: Design pattern detection and suggestion
- **clean-architecture**: Architecture quality assessment
- **testing-strategies**: Test coverage and quality analysis

---

## Advanced Configuration

### Advanced Static Analysis

```python
from code_analysis import StaticAnalyzer, Rule, RuleConfig

analyzer = StaticAnalyzer(
    config=RuleConfig(
        enabled_rules=["all"],
        disabled_rules=["print_statements"],
        custom_rules_path="./rules",
        severity_threshold="warning",
        auto_fix=True,
    ),
)

# Add custom rules
analyzer.add_rule(Rule(
    name="no_print_statements",
    pattern=r"\bprint\s*\(",
    severity="warning",
    message="Avoid print statements in production code",
    fix_suggestion="Use logging instead of print",
))

analyzer.add_rule(Rule(
    name="no_raw_sql",
    pattern=r"execute\s*\(\s*[\"']SELECT",
    severity="error",
    message="Raw SQL queries detected",
    fix_suggestion="Use parameterized queries or ORM",
))

# Analyze with custom configuration
results = analyzer.analyze_project(
    "/path/to/project",
    include_patterns=["*.py"],
    exclude_patterns=["tests/*", "venv/*"],
    max_file_size_mb=1,
)

print(f"Total issues: {results.total_issues}")
print(f"Errors: {results.error_count}")
print(f"Warnings: {results.warning_count}")
print(f"Info: {results.info_count}")
```

### Advanced Complexity Analysis

```python
from code_analysis import ComplexityAnalyzer, ComplexityConfig

analyzer = ComplexityAnalyzer(
    config=ComplexityConfig(
        calculate_cyclomatic=True,
        calculate_cognitive=True,
        calculate_halstead=True,
        calculate_maintainability=True,
        threshold_cyclomatic=10,
        threshold_cognitive=15,
        threshold_nesting=4,
    ),
)

# Analyze project complexity
report = analyzer.analyze_project("/path/to/project")
print(f"Average cyclomatic complexity: {report.avg_cyclomatic:.1f}")
print(f"Average cognitive complexity: {report.avg_cognitive:.1f}")
print(f"Functions above threshold: {report.above_threshold_count}")

print("\nMost complex functions:")
for func in report.most_complex[:10]:
    print(f"  {func.name} ({func.file}:{func.line})")
    print(f"    Cyclomatic: {func.cyclomatic}")
    print(f"    Cognitive: {func.cognitive}")
    print(f"    Lines: {func.lines}")
```

### Advanced Dependency Analysis

```python
from code_analysis import DependencyAnalyzer, DependencyConfig

analyzer = DependencyAnalyzer(
    config=DependencyConfig(
        analyze_internal=True,
        analyze_external=True,
        check_versions=True,
        check_vulnerabilities=True,
        max_depth=10,
    ),
)

# Comprehensive dependency analysis
deps = analyzer.analyze_comprehensive("/path/to/project")
print(f"Direct dependencies: {len(deps.direct)}")
print(f"Transitive dependencies: {len(deps.transitive)}")
print(f"Total dependencies: {deps.total_count}")

# Check for circular dependencies
cycles = deps.find_cycles()
if cycles:
    print(f"\nCircular dependencies: {len(cycles)}")
    for cycle in cycles:
        print(f"  {' → '.join(cycle)}")

# Check for vulnerabilities
if deps.vulnerabilities:
    print(f"\nVulnerable dependencies: {len(deps.vulnerabilities)}")
    for vuln in deps.vulnerabilities:
        print(f"  {vuln.package}: {vuln.description}")
        print(f"    Severity: {vuln.severity}")
        print(f"    Fix: {vuln.fix_version}")
```

## Architecture Patterns

### Code Analysis Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                Code Analysis Architecture                   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Collection Layer                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Source Code │  │  AST        │  │  Metrics    │ │   │
│  │  │  Parsing     │  │  Generation │  │  Collection │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Analysis Layer                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Static     │  │  Complexity │  │  Dependency  │ │   │
│  │  │  Analysis   │  │  Analysis   │  │  Analysis    │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Reporting Layer                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Issue      │  │  Metrics    │  │  Trend      │ │   │
│  │  │  Reports    │  │  Dashboard  │  │  Analysis   │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Integration Guide

### CI/CD Integration

```yaml
# .github/workflows/code-analysis.yml
name: Code Analysis

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install code-analysis
      
      - name: Run static analysis
        run: code-analysis static --config .code-analysis.yml
      
      - name: Run complexity analysis
        run: code-analysis complexity --threshold 10
      
      - name: Run dependency audit
        run: code-analysis dependencies --check-vulnerabilities
```

## Performance Optimization

### Analysis Performance

| Technique | Speed | Accuracy | Use Case |
|-----------|-------|----------|----------|
| Regex patterns | Fast | Medium | Quick checks |
| AST analysis | Medium | High | Structural analysis |
| Type inference | Slow | High | Type safety |
| Data flow | Slow | High | Security analysis |

## Security Considerations

### Security Scanning

```python
from code_analysis import SecurityScanner

scanner = SecurityScanner()

# Scan for security vulnerabilities
results = scanner.scan_project("/path/to/project")
print(f"Security issues: {results.total_issues}")
print(f"Critical: {results.critical_count}")
print(f"High: {results.high_count}")
print(f"Medium: {results.medium_count}")

for issue in results.issues[:10]:
    print(f"\n  [{issue.severity}] {issue.title}")
    print(f"    {issue.description}")
    print(f"    Location: {issue.file}:{issue.line}")
    print(f"    Fix: {issue.fix_suggestion}")
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| False positives | Incorrect warnings | Tune rules, add exceptions |
| Slow analysis | Long analysis time | Exclude large files, use caching |
| Missing symbols | Incomplete analysis | Ensure proper imports |
| Memory issues | OOM during analysis | Analyze in batches |

## API Reference

### StaticAnalyzer

```python
class StaticAnalyzer:
    def __init__(self, config: RuleConfig = None)
    def add_rule(self, rule: Rule)
    def analyze_file(self, file_path: str) -> AnalysisResult
    def analyze_project(self, project_path: str, **kwargs) -> ProjectResult
    def get_rules(self) -> list[Rule]
    def export_results(self, results: AnalysisResult, format: str = "json")
```

### ComplexityAnalyzer

```python
class ComplexityAnalyzer:
    def __init__(self, config: ComplexityConfig = None)
    def analyze_function(self, function_code: str) -> ComplexityResult
    def analyze_file(self, file_path: str) -> FileComplexityResult
    def analyze_project(self, project_path: str) -> ProjectComplexityResult
    def get_most_complex(self, n: int = 10) -> list[ComplexFunction]
```

### DependencyAnalyzer

```python
class DependencyAnalyzer:
    def __init__(self, config: DependencyConfig = None)
    def analyze(self, project_path: str) -> DependencyGraph
    def analyze_comprehensive(self, project_path: str) -> ComprehensiveResult
    def find_cycles(self) -> list[list[str]]
    def check_vulnerabilities(self) -> list[Vulnerability]
    def get_dependency_tree(self) -> DependencyTree
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum
from datetime import datetime

class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class Issue:
    rule: str
    severity: Severity
    message: str
    file: str
    line: int
    column: int
    fix_suggestion: Optional[str]

@dataclass
class ComplexityResult:
    cyclomatic: int
    cognitive: int
    halstead_volume: float
    maintainability_index: float
    lines: int
    nesting_depth: int

@dataclass
class DependencyGraph:
    direct: Dict[str, str]
    transitive: Dict[str, str]
    cycles: List[List[str]]
    vulnerabilities: List['Vulnerability']
```

## Deployment Guide

### Installation

```bash
pip install code-analysis

# With all extras
pip install code-analysis[all]
```

## Monitoring & Observability

### Metrics Collection

```python
from code_analysis import MetricsCollector

collector = MetricsCollector()

# Collect analysis metrics
collector.counter("analysis.files.analyzed", count)
collector.histogram("analysis.duration.seconds", duration)
collector.gauge("analysis.issues.total", count, tags={"severity": severity})
collector.gauge("analysis.complexity.average", avg)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from code_analysis import StaticAnalyzer

@pytest.fixture
def analyzer():
    return StaticAnalyzer()

def test_analyze_file(analyzer):
    result = analyzer.analyze_file("test.py")
    assert result is not None
```

## Versioning & Migration

### Version Compatibility

| Component | Minimum Version | Recommended |
|-----------|-----------------|-------------|
| Python | 3.8 | 3.11+ |

## Glossary

| Term | Definition |
|------|------------|
| **Cyclomatic Complexity** | Number of independent paths through code |
| **Cognitive Complexity** | How difficult code is to understand |
| **Maintainability Index** | Composite measure of maintainability |
| **Technical Debt** | Cost of shortcuts taken |
| **AST** | Abstract Syntax Tree |

## Changelog

### Version 3.0.0 (2024-01-15)
- Added security scanning
- New complexity metrics
- Improved dependency analysis
- Added auto-fix capabilities

## Contributing Guidelines

```bash
git clone https://github.com/awesome-grok/code-analysis.git
cd code-analysis
pip install -e ".[dev]"
pytest
```

## Cross-Language Analysis

### Multi-Language Support Matrix

| Language | Parser | AST Support | Complexity | Dependencies | Auto-Fix |
|----------|--------|-------------|------------|--------------|----------|
| Python | tree-sitter | Full | Cyclomatic/Cognitive | pip/poetry | Yes |
| JavaScript | tree-sitter | Full | Halstead/Cyclomatic | npm/yarn | Yes |
| TypeScript | tree-sitter | Full | All metrics | npm/yarn | Yes |
| Java | javaparser | Full | All metrics | maven/gradle | Yes |
| Go | go/ast | Full | Cyclomatic | go.mod | Limited |
| Rust | syn | Full | Cognitive | cargo | Limited |
| C/C++ | libclang | Partial | Cyclomatic | cmake/conan | No |

### Language-Specific Static Rules

```python
from code_analysis import LanguageConfig

# Configure per-language rules
configs = {
    "python": LanguageConfig(
        rules=["no-mutable-default-args", "no-bare-except", "type-hint-coverage"],
        complexity_threshold=8,
        max_function_length=50,
    ),
    "javascript": LanguageConfig(
        rules=["no-var", "prefer-const", "no-unused-vars", "eqeqeq"],
        complexity_threshold=10,
        max_function_length=40,
    ),
    "typescript": LanguageConfig(
        rules=["strict-null-checks", "no-any", "explicit-function-return-type"],
        complexity_threshold=10,
        max_function_length=40,
    ),
    "java": LanguageConfig(
        rules=["no-null-return", "immutable-collections", "record-classes"],
        complexity_threshold=10,
        max_function_length=50,
    ),
}

analyzer = StaticAnalyzer(language_configs=configs)
```

### Python-Specific Analysis

```python
from code_analysis import PythonAnalyzer

py_analyzer = PythonAnalyzer()

# Python-specific checks
results = py_analyzer.analyze("app.py")
print(f"Mutable default args: {results.mutable_defaults}")
print(f"Bare excepts: {results.bare_excepts}")
print(f"Missing type hints: {results.missing_type_hints}")
print(f"Unused imports: {results.unused_imports}")
print(f"Cyclomatic complexity: {results.cyclomatic_avg:.1f}")
print(f"Type hint coverage: {results.type_hint_coverage:.1%}")
```

### JavaScript/TypeScript Analysis

```python
from code_analysis import JavaScriptAnalyzer

js_analyzer = JavaScriptAnalyzer()

results = js_analyzer.analyze("src/")
print(f"any types: {results.any_count}")
print(f"Unused variables: {results.unused_vars}")
print(f"Console statements: {results.console_statements}")
print(f"Promise handling issues: {results.promise_issues}")
print(f"Module coupling: {results.coupling_score:.2f}")
```

## Advanced Metrics & Dashboards

### Composite Quality Score

```python
from code_analysis import QualityScoreCalculator

calculator = QualityScoreCalculator()

# Calculate composite score across dimensions
score = calculator.calculate("project/", weights={
    "maintainability": 0.25,
    "complexity": 0.20,
    "duplication": 0.15,
    "test_coverage": 0.20,
    "documentation": 0.10,
    "dependency_health": 0.10,
})

print(f"Overall quality: {score.overall:.1f}/100")
print(f"Maintainability: {score.maintainability:.1f}")
print(f"Complexity: {score.complexity:.1f}")
print(f"Duplication: {score.duplication:.1f}")
print(f"Test coverage: {score.test_coverage:.1f}")
print(f"Documentation: {score.documentation:.1f}")
print(f"Dependency health: {score.dependency_health:.1f}")

# Generate trend data
trends = calculator.get_trends("project/", period="6_months")
for trend in trends:
    print(f"  {trend.date}: {trend.score:.1f} ({trend.direction})")
```

### Dashboard Generation

```python
from code_analysis import DashboardGenerator

generator = DashboardGenerator()

# Generate HTML dashboard
dashboard = generator.generate(
    project_path="/path/to/project",
    output="quality-dashboard.html",
    metrics=["complexity", "coverage", "debt", "dependencies"],
    time_range="30_days",
)

print(f"Dashboard generated: {dashboard.output_path}")
print(f"Widgets: {len(dashboard.widgets)}")
print(f"Data points: {dashboard.data_points}")
```

### Technical Debt Quantification

```python
from code_analysis import DebtQuantifier

quantifier = DebtQuantifier()

# Quantify technical debt
debt = quantifier.analyze("project/")
print(f"Total debt hours: {debt.total_hours:.1f}")
print(f"Estimated cost: ${debt.estimated_cost:,.2f}")
print(f"Debt ratio: {debt.ratio:.1%}")

print("\nDebt by category:")
for category, amount in debt.by_category.items():
    print(f"  {category}: {amount:.1f} hours (${amount * 150:,.2f})")

print("\nDebt hotspots:")
for hotspot in debt.hotspots[:5]:
    print(f"  {hotspot.file}: {hotspot.hours:.1f} hours")
    print(f"    Smells: {hotspot.smell_count}")
    print(f"    Complexity: {hotspot.complexity}")
```

## Real-World Case Studies

### E-Commerce Platform Analysis

```python
from code_analysis import ProjectAnalyzer

analyzer = ProjectAnalyzer()

# Analyze large e-commerce codebase
report = analyzer.analyze("ecommerce-platform/")

print("=== E-Commerce Platform Analysis ===")
print(f"Total files: {report.total_files:,}")
print(f"Total LOC: {report.total_loc:,}")
print(f"Functions: {report.total_functions:,}")
print(f"Classes: {report.total_classes:,}")

print("\n=== Quality Metrics ===")
print(f"Maintainability index: {report.maintainability_index:.1f}/100")
print(f"Average complexity: {report.avg_complexity:.1f}")
print(f"Test coverage: {report.test_coverage:.1%}")
print(f"Documentation coverage: {report.doc_coverage:.1%}")

print("\n=== Top Issues ===")
for issue in report.critical_issues[:10]:
    print(f"  [{issue.severity}] {issue.file}:{issue.line}")
    print(f"    {issue.message}")

print("\n=== Recommendations ===")
for rec in report.recommendations[:5]:
    print(f"  [{rec.priority}] {rec.title}")
    print(f"    {rec.description}")
    print(f"    Estimated impact: {rec.impact_hours:.1f} hours")
```

### Microservice Analysis

```python
from code_analysis import MicroserviceAnalyzer

analyzer = MicroserviceAnalyzer()

# Analyze microservice architecture
architecture = analyzer.analyze("services/")

print("=== Service Dependencies ===")
for service, deps in architecture.dependencies.items():
    print(f"  {service} → {', '.join(deps)}")

print("\n=== Circular Dependencies ===")
cycles = architecture.find_cycles()
if cycles:
    for cycle in cycles:
        print(f"  {' → '.join(cycle)} → {cycle[0]}")

print("\n=== Service Metrics ===")
for service, metrics in architecture.service_metrics.items():
    print(f"  {service}:")
    print(f"    LOC: {metrics.loc:,}")
    print(f"    Complexity: {metrics.avg_complexity:.1f}")
    print(f"    Coupling: {metrics.coupling_score:.2f}")
    print(f"    Cohesion: {metrics.cohesion_score:.2f}")
```

## Migration & Upgrade Guide

### Upgrading from v2 to v3

```python
from code_analysis.migration import MigrationTool

migration = MigrationTool()

# Migrate configuration
result = migration.migrate_config(
    old_config=".code-analysis-v2.yml",
    new_config=".code-analysis-v3.yml",
)

print(f"Config migrated: {result.success}")
print(f"Changes: {len(result.changes)}")
for change in result.changes:
    print(f"  {change.description}")

# Migrate custom rules
rules_result = migration.migrate_rules(
    old_rules="./rules-v2/",
    new_rules="./rules-v3/",
)

print(f"Rules migrated: {rules_result.count}")
print(f"Deprecated: {rules_result.deprecated_count}")
print(f"New features available: {rules_result.new_features}")
```

### Configuration Migration Script

```python
from code_analysis.migration import ConfigMigrator

migrator = ConfigMigrator()

# Migrate project configuration
migrator.migrate(
    source=".",
    target_config=".code-analysis.yml",
    interactive=True,
    backup=True,
)

# Validate new configuration
validation = migrator.validate(".code-analysis.yml")
print(f"Configuration valid: {validation.is_valid}")
if validation.warnings:
    print(f"Warnings: {len(validation.warnings)}")
    for warning in validation.warnings:
        print(f"  {warning}")
```

## Contributing Guidelines

```bash
git clone https://github.com/awesome-grok/code-analysis.git
cd code-analysis
pip install -e ".[dev]"
pytest
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills