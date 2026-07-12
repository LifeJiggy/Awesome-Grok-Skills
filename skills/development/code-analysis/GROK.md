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