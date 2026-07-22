---
name: "Refactoring Patterns"
version: "2.0.0"
description: "Comprehensive refactoring patterns toolkit with code smell detection, transformation catalog, automated refactoring, safe change verification, and refactoring guidance for improving code quality"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["development", "refactoring", "code-smells", "transformations", "clean-code", "quality"]
category: "development"
personality: "refactoring-expert"
use_cases: ["code smell detection", "refactoring guidance", "automated transformations", "safe refactoring", "code improvement"]
---

# Refactoring Patterns

> Production-grade refactoring framework providing code smell detection, transformation catalog, automated refactoring, safe change verification, and step-by-step guidance for improving code structure without changing behavior.

## Overview

The Refactoring Patterns module provides a systematic approach to code improvement. It implements code smell detection with severity assessment, a catalog of refactoring transformations with before/after examples, automated refactoring with test verification, safe change sequencing, and refactoring impact analysis. Every transformation includes safety checks, rollback capability, and verification steps.

## Core Capabilities

### 1. Code Smell Detection
- Long Method detection
- Large Class/God Object identification
- Feature Envy recognition
- Data Clumps detection
- Primitive Obsession identification
- Switch Statement detection
- Parallel Inheritance detection

### 2. Refactoring Catalog
- Extract Method/Function
- Inline Method
- Move Method/Field
- Replace Temp with Query
- Introduce Explaining Variable
- Split Temporary Variable
- Replace Method with Method Object
- Decompose Conditional

### 3. Automated Refactoring
- AST-based code transformation
- Test-guided refactoring
- Incremental refactoring steps
- Rollback on test failure
- Refactoring verification

### 4. Safe Change Sequencing
- Dependency-aware ordering
- Risk assessment per change
- Checkpoint creation
- Incremental verification
- Conflict detection

### 5. Impact Analysis
- Code coverage impact
- Risk assessment
- Effort estimation
- Benefit prediction
- Priority scoring

## Usage Examples

### Code Smell Detection

```python
from refactoring_patterns import SmellDetector

detector = SmellDetector()

# Analyze code for smells
smells = detector.detect_file("app.py")
print(f"Smells found: {len(smells)}")
for smell in smells:
    print(f"  [{smell.severity}] {smell.name}: {smell.description}")
    print(f"    Location: {smell.file}:{smell.line}")
    print(f"    Suggestion: {smell.refactoring_suggestion}")
```

### Refactoring Guidance

```python
from refactoring_patterns import RefactoringGuide

guide = RefactoringGuide()

# Get refactoring steps for a code smell
steps = guide.get_steps(smell)
for i, step in enumerate(steps, 1):
    print(f"Step {i}: {step.description}")
    print(f"  Code: {step.code_before}")
    print(f"  → {step.code_after}")
    print(f"  Verify: {step.verification}")
```

### Automated Refactoring

```python
from refactoring_patterns import AutoRefactor

refactor = AutoRefactor()

# Apply refactoring
result = refactor.apply(
    file_path="app.py",
    transformation="extract_method",
    start_line=42,
    end_line=58,
    method_name="process_data",
)

print(f"Refactoring applied: {result.success}")
print(f"Lines changed: {result.lines_changed}")
print(f"Tests passed: {result.tests_passed}")
```

### Refactoring Planning

```python
from refactoring_patterns import RefactoringPlanner

planner = RefactoringPlanner()

# Create refactoring plan
plan = planner.create_plan(codebase="/path/to/project")
print(f"Total refactorings: {len(plan.steps)}")
print(f"Estimated effort: {plan.estimated_hours:.1f} hours")
print(f"Risk level: {plan.risk_level}")

for step in plan.steps[:5]:
    print(f"  [{step.priority}] {step.name}: {step.description}")
```

## Best Practices

### Code Smells
- Address smells incrementally, not all at once
- Focus on high-impact smells first (Long Method, Large Class)
- Use tests to verify behavior preservation
- Document refactoring decisions

### Refactoring
- Always have tests before refactoring
- Refactor in small, verifiable steps
- Use version control for every change
- Run tests after each refactoring step

### Safety
- Create checkpoints before major changes
- Verify test coverage before refactoring
- Use automated tools when possible
- Review changes with team members

### Planning
- Prioritize refactorings by impact and risk
- Estimate effort realistically
- Schedule refactoring in dedicated sprints
- Track refactoring metrics over time

## Related Modules

- **code-analysis**: Identify code quality issues to refactor
- **design-patterns**: Apply design patterns during refactoring
- **clean-architecture**: Architectural refactoring guidance
- **testing-strategies**: Ensure test coverage for safe refactoring

---

## Advanced Configuration

### Advanced Code Smell Detection

```python
from refactoring_patterns import SmellDetector, SmellConfig

detector = SmellDetector(
    config=SmellConfig(
        enabled_smells=["all"],
        severity_threshold="medium",
        min_lines=10,
        min_complexity=5,
        check_naming=True,
        check_duplication=True,
    ),
)

# Detect smells in project
smells = detector.detect_project(
    "/path/to/project",
    include_patterns=["*.py"],
    exclude_patterns=["tests/*", "migrations/*"],
)

print(f"Total smells: {len(smells)}")
print(f"By severity:")
for severity in ["critical", "high", "medium", "low"]:
    count = len([s for s in smells if s.severity == severity])
    print(f"  {severity}: {count}")

print("\nBy type:")
smell_types = {}
for smell in smells:
    smell_types[smell.type] = smell_types.get(smell.type, 0) + 1
for smell_type, count in sorted(smell_types.items(), key=lambda x: -x[1]):
    print(f"  {smell_type}: {count}")
```

### Advanced Refactoring Automation

```python
from refactoring_patterns import AutoRefactor, RefactorConfig

refactor = AutoRefactor(
    config=RefactorConfig(
        dry_run=True,
        verify_tests=True,
        create_checkpoint=True,
        parallel_execution=True,
        max_workers=4,
    ),
)

# Apply multiple refactorings
result = refactor.apply_batch(
    refactorings=[
        {"type": "extract_method", "file": "app.py", "start": 42, "end": 58, "name": "process_data"},
        {"type": "rename_variable", "file": "app.py", "old_name": "x", "new_name": "user_count"},
        {"type": "inline_method", "file": "utils.py", "method": "helper"},
    ],
    verify_after_each=True,
)

print(f"Refactorings applied: {result.applied}")
print(f"Refactorings skipped: {result.skipped}")
print(f"Tests passed: {result.tests_passed}")
```

### Advanced Refactoring Planning

```python
from refactoring_patterns import RefactoringPlanner, PlanConfig

planner = RefactoringPlanner(
    config=PlanConfig(
        prioritize_by="impact",
        estimate_effort=True,
        assess_risk=True,
        group_related=True,
        create_roadmap=True,
    ),
)

# Create comprehensive refactoring plan
plan = planner.create_plan(
    codebase="/path/to/project",
    goals=["reduce_complexity", "improve_testability", "reduce_duplication"],
    constraints={"max_hours_per_sprint": 20, "risk_tolerance": "medium"},
)

print(f"Total refactorings: {len(plan.steps)}")
print(f"Estimated effort: {plan.estimated_hours:.1f} hours")
print(f"Risk level: {plan.risk_level}")

print("\nRoadmap:")
for phase in plan.phases:
    print(f"\n  Phase: {phase.name}")
    print(f"  Duration: {phase.duration_hours:.1f} hours")
    for step in phase.steps:
        print(f"    [{step.priority}] {step.name}: {step.description}")
```

## Architecture Patterns

### Refactoring Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                Refactoring Architecture                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Detection Layer                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Smell      │  │  Pattern    │  │  Complexity  │ │   │
│  │  │  Detection  │  │  Detection  │  │  Analysis    │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Planning Layer                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Priority   │  │  Effort     │  │  Risk       │ │   │
│  │  │  Ranking    │  │  Estimation │  │  Assessment  │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Execution Layer                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Code       │  │  Test       │  │  Verify     │ │   │
│  │  │  Transform  │  │  Execution  │  │  Results    │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Integration Guide

### CI/CD Integration

```yaml
# .github/workflows/refactoring.yml
name: Refactoring Analysis

on:
  pull_request:
    branches: [main]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Detect code smells
        run: refactoring-patterns detect --severity medium
      
      - name: Generate refactoring plan
        run: refactoring-patterns plan --output plan.json
      
      - name: Apply safe refactorings
        run: refactoring-patterns apply --auto --verify-tests
```

## Performance Optimization

### Refactoring Performance

| Technique | Speed | Safety | Use Case |
|-----------|-------|--------|----------|
| AST transformation | Fast | High | Code structure changes |
| Regex replacement | Fast | Medium | Simple renames |
| Manual refactoring | Slow | High | Complex changes |
| Batch refactoring | Medium | High | Multiple changes |

## Security Considerations

### Safe Refactoring

```python
from refactoring_patterns import SafetyChecker

checker = SafetyChecker()

# Check refactoring safety
safety = checker.check_refactoring(
    file="app.py",
    transformation="extract_method",
    start_line=42,
    end_line=58,
)

print(f"Safe to refactor: {safety.is_safe}")
print(f"Test coverage: {safety.test_coverage:.1%}")
print(f"Risk level: {safety.risk_level}")

if not safety.is_safe:
    print(f"Reasons:")
    for reason in safety.reasons:
        print(f"  - {reason}")
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Refactoring breaks tests | Test failures | Check test coverage, verify behavior |
| Merge conflicts | Conflicts after refactoring | Refactor in smaller steps |
| Performance regression | Slower code | Profile before/after |
| Lost functionality | Missing features | Verify with integration tests |

## API Reference

### SmellDetector

```python
class SmellDetector:
    def __init__(self, config: SmellConfig = None)
    def detect_file(self, file_path: str) -> list[CodeSmell]
    def detect_project(self, project_path: str, **kwargs) -> list[CodeSmell]
    def get_smell_types(self) -> list[str]
    def get_severity_counts(self, smells: list[CodeSmell]) -> dict[str, int]
```

### AutoRefactor

```python
class AutoRefactor:
    def __init__(self, config: RefactorConfig = None)
    def apply(self, **kwargs) -> RefactorResult
    def apply_batch(self, refactorings: list[dict], **kwargs) -> BatchResult
    def preview(self, **kwargs) -> PreviewResult
    def rollback(self, checkpoint_id: str) -> RollbackResult
```

### RefactoringPlanner

```python
class RefactoringPlanner:
    def __init__(self, config: PlanConfig = None)
    def create_plan(self, codebase: str, **kwargs) -> RefactoringPlan
    def estimate_effort(self, plan: RefactoringPlan) -> float
    def assess_risk(self, plan: RefactoringPlan) -> str
    def optimize_plan(self, plan: RefactoringPlan) -> RefactoringPlan
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum

class SmellType(Enum):
    LONG_METHOD = "long_method"
    LARGE_CLASS = "large_class"
    FEATURE_ENVY = "feature_envy"
    DATA_CLUMPS = "data_clumps"
    PRIMITIVE_OBSESSION = "primitive_obsession"
    SWITCH_STATEMENT = "switch_statement"
    DUPLICATED_CODE = "duplicated_code"

@dataclass
class CodeSmell:
    type: SmellType
    severity: str
    description: str
    file: str
    line: int
    refactoring_suggestion: str
    effort_estimate: float

@dataclass
class RefactoringStep:
    name: str
    description: str
    type: str
    file: str
    start_line: int
    end_line: int
    priority: str
    risk_level: str
    effort_hours: float
```

## Deployment Guide

### Installation

```bash
pip install refactoring-patterns
```

## Monitoring & Observability

### Metrics Collection

```python
from refactoring_patterns import MetricsCollector

collector = MetricsCollector()

# Collect refactoring metrics
collector.counter("refactoring.applied.total", count, tags={"type": refactor_type})
collector.histogram("refactoring.duration.seconds", duration)
collector.gauge("refactoring.smells.total", count)
collector.gauge("refactoring.code_quality.score", score)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from refactoring_patterns import SmellDetector, AutoRefactor

@pytest.fixture
def detector():
    return SmellDetector()

def test_detect_smells(detector):
    smells = detector.detect_file("test.py")
    assert isinstance(smells, list)
```

## Versioning & Migration

### Version Compatibility

| Component | Minimum Version | Recommended |
|-----------|-----------------|-------------|
| Python | 3.8 | 3.11+ |

## Glossary

| Term | Definition |
|------|------------|
| **Code Smell** | Surface indication of deeper problem |
| **Refactoring** | Restructuring code without changing behavior |
| **Technical Debt** | Cost of shortcuts |
| **Cyclomatic Complexity** | Number of independent paths |
| **Coupling** | Degree of interdependence |

## Changelog

### Version 3.0.0 (2024-01-15)
- Added automated refactoring
- New refactoring planner
- Improved smell detection
- Added safety checks

## Contributing Guidelines

```bash
git clone https://github.com/awesome-grok/refactoring-patterns.git
cd refactoring-patterns
pip install -e ".[dev]"
pytest
```

## Domain-Specific Refactoring

### API Endpoint Refactoring

```python
from refactoring_patterns import APIRefactor

refactor = APIRefactor()

# Refactor monolithic API endpoint
result = refactor.split_endpoint(
    file="routes.py",
    function="handle_request",
    split_by="http_method",
)

print(f"Original: 1 function → {result.new_functions} functions")
for func in result.new_functions:
    print(f"  {func.name}: {func.method} {func.path}")
    print(f"    Lines: {func.line_count}")
    print(f"    Tests added: {func.tests_added}")
```

### Database Layer Refactoring

```python
from refactoring_patterns import DatabaseRefactor

refactor = DatabaseRefactor()

# Extract repository pattern
result = refactor.extract_repository(
    file="models.py",
    classes=["User", "Order", "Product"],
    target_dir="repositories/",
)

print(f"Repositories created: {len(result.repositories)}")
for repo in result.repositories:
    print(f"  {repo.name}: {repo.methods_count} methods")
    print(f"    Query methods: {repo.query_methods}")
    print(f"    CRUD methods: {repo.crud_methods}")

# Refactor raw SQL to ORM
orm_result = refactor.convert_to_orm(
    files=["queries.py"],
    orm="sqlalchemy",
)

print(f"\nSQL queries converted: {orm_result.queries_converted}")
print(f"Manual review needed: {orm_result.manual_review_count}")
```

### Event Handler Refactoring

```python
from refactoring_patterns import EventHandlerRefactor

refactor = EventHandlerRefactor()

# Refactor callback hell to async/await
result = refactor.modernize_callbacks(
    file="handlers.py",
    target_style="async_await",
)

print(f"Functions modernized: {result.functions_count}")
print(f"Callback depth reduced: {result.avg_depth_before:.1f} → {result.avg_depth_after:.1f}")

# Extract event dispatcher
dispatcher_result = refactor.extract_dispatcher(
    file="handlers.py",
    output="dispatcher.py",
)

print(f"Events extracted: {dispatcher_result.event_count}")
print(f"Handler methods: {dispatcher_result.handler_count}")
```

## Refactoring for Performance

### Hot Path Optimization

```python
from refactoring_patterns import PerformanceRefactor

refactor = PerformanceRefactor()

# Identify and optimize hot paths
hotspots = refactor.find_hotspots(
    profiler_data="profile_results.prof",
    threshold_ms=100,
)

print(f"Hot spots found: {len(hotspots)}")
for spot in hotspots:
    print(f"  {spot.function}: {spot.avg_time_ms:.1f}ms ({spot.call_count} calls)")
    print(f"    Optimization: {spot.suggestion}")
    print(f"    Estimated improvement: {spot.estimated_speedup:.1f}x")

# Apply optimizations
result = refactor.optimize(
    hotspots=hotspots[:5],
    strategies=["caching", "batching", "lazy_loading"],
)

print(f"\nOptimizations applied: {result.applied}")
print(f"Total speedup: {result.total_speedup:.1f}x")
```

### Memory Optimization

```python
from refactoring_patterns import MemoryRefactor

refactor = MemoryRefactor()

# Find memory leaks
leaks = refactor.find_leaks(
    heap_snapshot="heap.heapsnapshot",
    threshold_mb=10,
)

print(f"Memory leaks found: {len(leaks)}")
for leak in leaks:
    print(f"  {leak.location}: {leak.size_mb:.1f}MB retained")
    print(f"    Root: {leak.root_path}")
    print(f"    Fix: {leak.suggestion}")

# Optimize data structures
result = refactor.optimize_data_structures(
    file="data_processor.py",
    strategies=["generators", "slots", "compact_dicts"],
)

print(f"\nMemory reduction: {result.before_mb:.1f}MB → {result.after_mb:.1f}MB")
print(f"Savings: {result.savings_percent:.1f}%")
```

### Concurrency Optimization

```python
from refactoring_patterns import ConcurrencyRefactor

refactor = ConcurrencyRefactor()

# Add async support to synchronous code
result = refactor.add_async(
    file="http_client.py",
    functions=["fetch_data", "process_response", "send_request"],
)

print(f"Functions made async: {len(result.converted)}")
for func in result.converted:
    print(f"  {func.name}: {func.style}")

# Add connection pooling
pool_result = refactor.add_connection_pool(
    file="database.py",
    pool_size=10,
    max_overflow=20,
)

print(f"\nConnection pooling added: {pool_result.applied}")
print(f"Pool size: {pool_result.pool_size}")
```

## Refactoring for Testability

### Dependency Injection Refactoring

```python
from refactoring_patterns import TestabilityRefactor

refactor = TestabilityRefactor()

# Extract hard-coded dependencies
result = refactor.extract_dependencies(
    file="service.py",
    class_name="PaymentService",
)

print(f"Dependencies extracted: {len(result.dependencies)}")
for dep in result.dependencies:
    print(f"  {dep.name}: {dep.type}")
    print(f"    Constructor injection: {dep.use_constructor}")
    print(f"    Interface created: {dep.interface_created}")

# Add test doubles
test_result = refactor.add_test_doubles(
    file="service.py",
    output_dir="tests/mocks/",
    doubles=["mocks", "stubs", "fakes"],
)

print(f"\nTest doubles created: {len(test_result.doubles)}")
for double in test_result.doubles:
    print(f"  {double.name}: {double.type}")
```

### Making Code Testable

```python
from refactoring_patterns import TestabilityRefactor

refactor = TestabilityRefactor()

# Refactor global state
result = refactor.remove_global_state(
    file="app.py",
    globals=["database_connection", "config", "logger"],
)

print(f"Globals removed: {len(result.removed)}")
for global_var in result.removed:
    print(f"  {global_var.name}: {global_var.replacement}")

# Add test hooks
hook_result = refactor.add_test_hooks(
    file="service.py",
    hooks=["reset_state", "mock_time", "capture_logs"],
)

print(f"\nTest hooks added: {len(hook_result.hooks)}")
for hook in hook_result.hooks:
    print(f"  {hook.name}: {hook.description}")
```

## Large-Scale Refactoring

### Codebase Migration

```python
from refactoring_patterns import MigrationRefactor

refactor = MigrationRefactor()

# Plan migration
plan = refactor.plan_migration(
    source_framework="django",
    target_framework="fastapi",
    codebase_path="project/",
)

print(f"Migration plan:")
print(f"  Estimated effort: {plan.estimated_hours:.0f} hours")
print(f"  Phases: {len(plan.phases)}")
for phase in plan.phases:
    print(f"    Phase: {phase.name} ({phase.estimated_hours:.0f}h)")
    print(f"    Steps: {len(phase.steps)}")

# Execute phase
result = refactor.execute_phase(
    plan=plan,
    phase_index=0,
    dry_run=True,
)

print(f"\nPhase execution:")
print(f"  Files modified: {result.files_modified}")
print(f"  Lines changed: {result.lines_changed}")
print(f"  Tests passing: {result.tests_passing}")
```

### Monolith to Microservices

```python
from refactoring_patterns import MicroserviceRefactor

refactor = MicroserviceRefactor()

# Analyze service boundaries
boundaries = refactor.analyze_boundaries(
    monolith_path="monolith/",
    strategy="domain_driven_design",
)

print(f"Proposed services: {len(boundaries)}")
for boundary in boundaries:
    print(f"  {boundary.name}:")
    print(f"    Domain: {boundary.domain}")
    print(f"    Tables: {len(boundary.tables)}")
    print(f"    Endpoints: {len(boundary.endpoints)}")
    print(f"    Dependencies: {boundary.dependencies}")

# Extract service
result = refactor.extract_service(
    monolith_path="monolith/",
    service_boundary=boundaries[0],
    output_path="services/user-service/",
)

print(f"\nService extracted:")
print(f"  Files created: {result.files_created}")
print(f"  API endpoints: {result.endpoints}")
print(f"  Database tables: {result.tables}")
print(f"  Tests: {result.test_count}")
```

## Case Studies

### Real-World Refactoring: E-Commerce Checkout

```python
from refactoring_patterns import CaseStudy

study = CaseStudy("ecommerce-checkout")

# Analyze the codebase
analysis = study.analyze("checkout/")
print(f"Original state:")
print(f"  LOC: {analysis.total_loc:,}")
print(f"  Cyclomatic complexity: {analysis.avg_complexity:.1f}")
print(f"  Test coverage: {analysis.test_coverage:.1%}")
print(f"  Code smells: {analysis.smell_count}")

# Execute refactoring plan
plan = study.create_plan()
result = study.execute_plan(plan, verify_tests=True)

print(f"\nAfter refactoring:")
print(f"  LOC: {result.total_loc:,} ({result.loc_change:+,})")
print(f"  Complexity: {result.avg_complexity:.1f} ({result.complexity_change:+.1f})")
print(f"  Coverage: {result.test_coverage:.1%} ({result.coverage_change:+.1%})")
print(f"  Smells: {result.smell_count} ({result.smell_change:+})")
print(f"  Performance: {result.performance_change:+.1f}%")
```

### Case Study: Legacy Python 2 to 3 Migration

```python
from refactoring_patterns import MigrationCase

case = MigrationCase("python2-to-3")

# Analyze Python 2 codebase
analysis = case.analyze("legacy_project/")
print(f"Python 2 patterns found:")
for pattern, count in analysis.py2_patterns.items():
    print(f"  {pattern}: {count}")

# Create migration plan
plan = case.create_migration_plan()
print(f"\nMigration plan:")
print(f"  Total steps: {len(plan.steps)}")
print(f"  Estimated hours: {plan.estimated_hours:.0f}")
print(f"  Risk level: {plan.risk_level}")

# Execute migration
result = case.execute_migration(plan)
print(f"\nMigration result:")
print(f"  Files converted: {result.files_converted}")
print(f"  Patterns fixed: {result.patterns_fixed}")
print(f"  Tests passing: {result.tests_passing}")
print(f"  Compatibility score: {result.compatibility_score:.1%}")
```

## Contributing Guidelines

```bash
git clone https://github.com/awesome-grok/refactoring-patterns.git
cd refactoring-patterns
pip install -e ".[dev]"
pytest
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills