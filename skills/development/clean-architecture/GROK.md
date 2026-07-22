---
name: "Clean Architecture"
version: "2.0.0"
description: "Comprehensive clean architecture toolkit with layer analysis, dependency direction verification, boundary detection, SOLID principles assessment, and architectural fitness functions for maintainable software"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["development", "clean-architecture", "SOLID", "boundaries", "layer-analysis", "fitness-functions"]
category: "development"
personality: "architect"
use_cases: ["layer analysis", "dependency verification", "boundary detection", "SOLID assessment", "architecture fitness"]
---

# Clean Architecture

> Production-grade clean architecture framework providing layer analysis, dependency direction verification, boundary detection, SOLID principles assessment, and architectural fitness functions for building maintainable software systems.

## Overview

The Clean Architecture module provides tools for enforcing architectural boundaries and principles. It implements layer detection and analysis, dependency direction verification (dependencies must point inward), business logic boundary detection, SOLID principles assessment, architectural fitness function execution, and violation reporting with remediation guidance. Every analysis ensures the codebase maintains proper separation of concerns.

## Core Capabilities

### 1. Layer Analysis
- Detect architectural layers (presentation, business, data, infrastructure)
- Verify layer ordering and dependencies
- Identify layer violations
- Measure layer cohesion
- Track layer complexity

### 2. Dependency Direction
- Verify dependencies point toward business logic
- Detect circular dependencies
- Identify inward dependency violations
- Map dependency graphs
- Calculate dependency metrics

### 3. Boundary Detection
- Identify use cases and entities
- Detect interface/implementation boundaries
- Map service boundaries
- Verify dependency inversion
- Identify anti-corruption layers

### 4. SOLID Assessment
- Single Responsibility evaluation
- Open/Closed principle verification
- Liskov Substitution checking
- Interface Segregation analysis
- Dependency Inversion verification

### 5. Fitness Functions
- Automated architecture tests
- Boundary violation detection
- Dependency constraint enforcement
- Complexity thresholds
- Coverage requirements

### 6. Architecture Documentation
- Component diagram generation
- Dependency documentation
- Architecture decision records
- Context maps
- Interface documentation

## Usage Examples

### Layer Analysis

```python
from clean_architecture import LayerAnalyzer

analyzer = LayerAnalyzer()

# Analyze project layers
analysis = analyzer.analyze("/path/to/project")
print("Layers detected:")
for layer in analysis.layers:
    print(f"  {layer.name}: {layer.components} components")
    print(f"    Dependencies: {layer.dependencies}")
    print(f"    Violations: {layer.violations}")

print(f"\nLayer violations: {analysis.total_violations}")
```

### Dependency Direction

```python
from clean_architecture import DependencyAnalyzer

analyzer = DependencyAnalyzer()

# Check dependency directions
result = analyzer.check_dependencies("/path/to/project")
print(f"Valid dependencies: {result.valid_count}")
print(f"Invalid dependencies: {result.invalid_count}")

for violation in result.violations:
    print(f"  VIOLATION: {violation.source} → {violation.target}")
    print(f"    Rule: {violation.rule}")
    print(f"    Fix: {violation.suggestion}")
```

### SOLID Assessment

```python
from clean_architecture import SOLIDAssessor

assessor = SOLIDAssessor()

# Assess SOLID compliance
results = assessor.assess("app.py")
print("SOLID Assessment:")
for principle, score in results.items():
    status = "✓" if score > 0.7 else "✗"
    print(f"  {status} {principle}: {score:.0%}")
```

### Fitness Functions

```python
from clean_architecture import FitnessFunctionRunner

runner = FitnessFunctionRunner()

# Run architecture fitness functions
results = runner.run("/path/to/project")
print(f"Fitness functions: {results.total}")
print(f"Passed: {results.passed}")
print(f"Failed: {results.failed}")

for result in results.details:
    status = "PASS" if result.passed else "FAIL"
    print(f"  [{status}] {result.name}: {result.description}")
```

## Best Practices

### Layer Architecture
- Business logic should not depend on infrastructure
- Use dependency inversion at layer boundaries
- Keep layers thin and focused
- Document layer responsibilities

### Dependency Direction
- Dependencies should point inward toward business logic
- Use interfaces at boundaries
- Avoid circular dependencies
- Apply dependency inversion principle

### SOLID Principles
- Apply SOLID principles pragmatically
- Refactor violations incrementally
- Use automated checks in CI/CD
- Document architectural decisions

### Fitness Functions
- Define fitness functions for critical boundaries
- Run fitness functions in CI/CD
- Fail builds on fitness function violations
- Review fitness functions regularly

## Related Modules

- **design-patterns**: Design patterns for clean architecture
- **refactoring-patterns**: Refactor to achieve clean architecture
- **code-analysis**: Code quality metrics for architecture
- **testing-strategies**: Test architecture boundaries

---

## Advanced Configuration

### Advanced Layer Analysis

```python
from clean_architecture import LayerAnalyzer, LayerConfig

analyzer = LayerAnalyzer(
    config=LayerConfig(
        detect_layers=True,
        verify_dependencies=True,
        measure_cohesion=True,
        measure_coupling=True,
        generate_diagrams=True,
    ),
)

# Comprehensive layer analysis
analysis = analyzer.analyze_comprehensive(
    "/path/to/project",
    layer_definitions={
        "presentation": ["ui/*", "controllers/*"],
        "business": ["domain/*", "services/*"],
        "data": ["repositories/*", "models/*"],
        "infrastructure": ["database/*", "external/*"],
    },
)

print("Layers detected:")
for layer in analysis.layers:
    print(f"\n  {layer.name}:")
    print(f"    Components: {layer.component_count}")
    print(f"    Cohesion: {layer.cohesion_score:.2f}")
    print(f"    Coupling: {layer.coupling_score:.2f}")
    print(f"    Violations: {layer.violation_count}")

print(f"\nOverall architecture score: {analysis.architecture_score:.1f}/100")
```

### Advanced Dependency Direction

```python
from clean_architecture import DependencyAnalyzer, DependencyConfig

analyzer = DependencyAnalyzer(
    config=DependencyConfig(
        verify_direction=True,
        detect_cycles=True,
        measure_stability=True,
        calculate_abstractness=True,
        generate_report=True,
    ),
)

# Check dependency directions
result = analyzer.check_comprehensive(
    "/path/to/project",
    rules=[
        {"from": "presentation", "to": "business", "allowed": True},
        {"from": "business", "to": "data", "allowed": True},
        {"from": "data", "to": "business", "allowed": False},
        {"from": "infrastructure", "to": "business", "allowed": True},
    ],
)

print(f"Valid dependencies: {result.valid_count}")
print(f"Invalid dependencies: {result.invalid_count}")
print(f"Stability score: {result.stability_score:.2f}")
print(f"Abstractness score: {result.abstractness_score:.2f}")

for violation in result.violations:
    print(f"\n  VIOLATION: {violation.source} → {violation.target}")
    print(f"    Rule: {violation.rule}")
    print(f"    Impact: {violation.impact}")
    print(f"    Fix: {violation.suggestion}")
```

### Advanced SOLID Assessment

```python
from clean_architecture import SOLIDAssessor, SOLIDConfig

assessor = SOLIDAssessor(
    config=SOLIDConfig(
        detailed_analysis=True,
        suggest_improvements=True,
        estimate_effort=True,
        generate_report=True,
    ),
)

# Comprehensive SOLID assessment
results = assessor.assess_comprehensive(
    "/path/to/project",
    focus_areas=["single_responsibility", "dependency_inversion"],
)

print("SOLID Assessment:")
for principle, score in results.principles.items():
    status = "✓" if score > 0.7 else "✗"
    print(f"  {status} {principle}: {score:.0%}")
    if score < 0.7:
        print(f"    Issues: {results.issues[principle]}")
        print(f"    Fix: {results.suggestions[principle]}")

print(f"\nOverall SOLID score: {results.overall_score:.0%}")
```

### Advanced Fitness Functions

```python
from clean_architecture import FitnessFunctionRunner, FitnessConfig

runner = FitnessFunctionRunner(
    config=FitnessConfig(
        fail_on_violation=True,
        generate_report=True,
        track_history=True,
        alert_on_regression=True,
    ),
)

# Run comprehensive fitness functions
results = runner.run_comprehensive(
    "/path/to/project",
    functions=[
        {"name": "no_circular_dependencies", "severity": "critical"},
        {"name": "layer_dependencies_point_inward", "severity": "high"},
        {"name": "business_logic_not_in_infrastructure", "severity": "high"},
        {"name": "interfaces_at_boundaries", "severity": "medium"},
        {"name": "max_coupling_threshold", "threshold": 0.3},
    ],
)

print(f"Fitness functions: {results.total}")
print(f"Passed: {results.passed}")
print(f"Failed: {results.failed}")
print(f"Score: {results.score:.1f}%")

for result in results.details:
    status = "PASS" if result.passed else "FAIL"
    print(f"\n  [{status}] {result.name}")
    print(f"    {result.description}")
    if not result.passed:
        print(f"    Violation: {result.violation}")
        print(f"    Fix: {result.suggestion}")
```

## Architecture Patterns

### Clean Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Clean Architecture                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Presentation Layer                     │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  UI         │  │  Controllers│  │  ViewModels  │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│                          ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Application Layer                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Use Cases  │  │  DTOs       │  │  Interfaces  │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│                          ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Domain Layer                           │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Entities   │  │  Value Obj  │  │  Domain Svc  │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│                          ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Infrastructure Layer                   │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Database   │  │  External   │  │  Frameworks │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Dependency Direction Rules

```
┌─────────────────────────────────────────────────────────────┐
│                  Dependency Direction Rules                 │
├─────────────────────────────────────────────────────────────┤
│  ✓ Presentation → Application (allowed)                    │
│  ✓ Application → Domain (allowed)                          │
│  ✓ Infrastructure → Domain (allowed via interfaces)        │
│  ✗ Domain → Application (VIOLATION)                        │
│  ✗ Domain → Infrastructure (VIOLATION)                     │
│  ✗ Application → Presentation (VIOLATION)                  │
└─────────────────────────────────────────────────────────────┘
```

## Integration Guide

### CI/CD Integration

```yaml
# .github/workflows/clean-architecture.yml
name: Clean Architecture Check

on:
  pull_request:
    branches: [main]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check layer dependencies
        run: clean-architecture check-layers
      
      - name: Verify dependency direction
        run: clean-architecture check-dependencies
      
      - name: Run fitness functions
        run: clean-architecture fitness --fail-on-violation
```

## Performance Optimization

### Architecture Analysis Performance

| Technique | Speed | Accuracy | Use Case |
|-----------|-------|----------|----------|
| Static analysis | Medium | High | Layer detection |
| Dependency parsing | Fast | High | Direction checking |
| Complexity metrics | Medium | High | Coupling analysis |
| Diagram generation | Slow | Medium | Visualization |

## Security Considerations

### Architecture Security

```python
from clean_architecture import SecurityAnalyzer

analyzer = SecurityAnalyzer()

# Check architecture security
security = analyzer.check_security("/path/to/project")
print(f"Security score: {security.score:.1f}/100")
print(f"Issues: {len(security.issues)}")

for issue in security.issues:
    print(f"  [{issue.severity}] {issue.description}")
    print(f"    Location: {issue.location}")
    print(f"    Fix: {issue.fix_suggestion}")
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Layer violations | Dependencies point outward | Apply dependency inversion |
| Circular dependencies | Cycles in dependency graph | Introduce interfaces |
| High coupling | Components tightly coupled | Extract interfaces |
| Low cohesion | Classes do too much | Split responsibilities |

## API Reference

### LayerAnalyzer

```python
class LayerAnalyzer:
    def __init__(self, config: LayerConfig = None)
    def analyze(self, project_path: str) -> LayerAnalysis
    def analyze_comprehensive(self, project_path: str, **kwargs) -> ComprehensiveAnalysis
    def get_layer_metrics(self) -> dict[str, float]
    def get_violations(self) -> list[LayerViolation]
```

### DependencyAnalyzer

```python
class DependencyAnalyzer:
    def __init__(self, config: DependencyConfig = None)
    def check_dependencies(self, project_path: str) -> DependencyResult
    def check_comprehensive(self, project_path: str, **kwargs) -> ComprehensiveResult
    def get_dependency_graph(self) -> DependencyGraph
    def calculate_metrics(self) -> DependencyMetrics
```

### SOLIDAssessor

```python
class SOLIDAssessor:
    def __init__(self, config: SOLIDConfig = None)
    def assess(self, file_path: str) -> dict[str, float]
    def assess_comprehensive(self, project_path: str, **kwargs) -> ComprehensiveResult
    def get_principle_details(self, principle: str) -> PrincipleDetails
    def suggest_improvements(self) -> list[Improvement]
```

### FitnessFunctionRunner

```python
class FitnessFunctionRunner:
    def __init__(self, config: FitnessConfig = None)
    def run(self, project_path: str) -> FitnessResult
    def run_comprehensive(self, project_path: str, **kwargs) -> ComprehensiveResult
    def get_history(self) -> list[FitnessHistory]
    def get_trends(self) -> FitnessTrends
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum

class LayerType(Enum):
    PRESENTATION = "presentation"
    APPLICATION = "application"
    DOMAIN = "domain"
    INFRASTRUCTURE = "infrastructure"

@dataclass
class Layer:
    name: str
    type: LayerType
    component_count: int
    cohesion_score: float
    coupling_score: float
    violation_count: int
    dependencies: List[str]

@dataclass
class DependencyViolation:
    source: str
    target: str
    rule: str
    impact: str
    suggestion: str

@dataclass
class SOLIDResult:
    principles: Dict[str, float]
    overall_score: float
    issues: Dict[str, List[str]]
    suggestions: Dict[str, str]
```

## Deployment Guide

### Installation

```bash
pip install clean-architecture
```

## Monitoring & Observability

### Metrics Collection

```python
from clean_architecture import MetricsCollector

collector = MetricsCollector()

# Collect architecture metrics
collector.gauge("architecture.layer.cohesion", score, tags=["layer": layer])
collector.gauge("architecture.layer.coupling", score, tags=["layer": layer])
collector.counter("architecture.violations.total", count, tags=["type": violation_type])
collector.gauge("architecture.solid.score", score)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from clean_architecture import LayerAnalyzer, DependencyAnalyzer

@pytest.fixture
def analyzer():
    return LayerAnalyzer()

def test_analyze_layers(analyzer):
    result = analyzer.analyze("test_project")
    assert result.layers is not None
```

## Versioning & Migration

### Version Compatibility

| Component | Minimum Version | Recommended |
|-----------|-----------------|-------------|
| Python | 3.8 | 3.11+ |

## Glossary

| Term | Definition |
|------|------------|
| **SOLID** | Single responsibility, Open-closed, Liskov, Interface, Dependency |
| **Dependency Inversion** | High-level modules don't depend on low-level |
| **Cohesion** | Degree to which elements belong together |
| **Coupling** | Degree of interdependence between modules |
| **Fitness Function** | Architectural constraint as automated test |

## Changelog

### Version 3.0.0 (2024-01-15)
- Added comprehensive SOLID assessment
- New fitness function runner
- Improved dependency analysis
- Added diagram generation

## Contributing Guidelines

```bash
git clone https://github.com/awesome-grok/clean-architecture.git
cd clean-architecture
pip install -e ".[dev]"
pytest
```

## Advanced Topics

### Hexagonal Architecture (Ports and Adapters)

```python
from clean_architecture import HexagonalAnalyzer

analyzer = HexagonalAnalyzer()

# Analyze hexagonal architecture compliance
result = analyzer.analyze("/path/to/project")
print(f"Ports detected: {len(result.ports)}")
print(f"Adapters detected: {len(result.adapters)}")
print(f"Core completeness: {result.core_completeness:.0%}")

for port in result.ports:
    print(f"\n  Port: {port.name}")
    print(f"    Type: {port.type}")  # primary or secondary
    print(f"    Implementations: {len(port.adapters)}")
    print(f"    Inverted: {port.dependency_inverted}")
```

### Domain-Driven Design Patterns

```python
from clean_architecture import DDDAnalyzer

ddd = DDDAnalyzer()

# Analyze DDD patterns in codebase
result = ddd.analyze("/path/to/project")
print(f"Bounded contexts: {len(result.bounded_contexts)}")
print(f"Aggregates: {len(result.aggregates)}")
print(f"Value objects: {len(result.value_objects)}")
print(f"Domain events: {len(result.domain_events)}")

for ctx in result.bounded_contexts:
    print(f"\n  Context: {ctx.name}")
    print(f"    Aggregates: {len(ctx.aggregates)}")
    print(f"    Entities: {len(ctx.entities)}")
    print(f"    Ubiquitous language terms: {len(ctx.ubiquitous_language)}")
```

### Architecture Decision Records

| Field | Description | Example |
|-------|-------------|---------|
| Title | Short name for the decision | "Use event sourcing for order management" |
| Status | Proposed / Accepted / Deprecated / Superseded | Accepted |
| Context | Forces at play, constraints | High write volume, audit requirements |
| Decision | What was decided | Implement event sourcing pattern |
| Consequences | Positive and negative outcomes | Full audit trail, eventual consistency |
| Alternatives | Options considered | CQRS with snapshot, traditional CRUD |

### Ports and Adapters Mapping

```
┌─────────────────────────────────────────────────────────┐
│                   Core Domain                            │
│  ┌──────────────────┐  ┌──────────────────┐             │
│  │  Primary Ports   │  │  Secondary Ports │             │
│  │  (Use Cases)     │  │  (Interfaces)    │             │
│  │  ┌────────────┐  │  │  ┌────────────┐  │             │
│  │  │ OrderSvc   │  │  │  │ RepoPort   │  │             │
│  │  │ PaymentSvc │  │  │  │ NotifyPort │  │             │
│  │  └────────────┘  │  │  └────────────┘  │             │
│  └──────────────────┘  └──────────────────┘             │
│           ▲                    │                         │
│           │                    ▼                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │                  Adapters                         │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐       │   │
│  │  │ REST API │  │ DB Repo  │  │ Email    │       │   │
│  │  │ Adapter  │  │ Adapter  │  │ Adapter  │       │   │
│  │  └──────────┘  └──────────┘  └──────────┘       │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Anti-Corruption Layer Patterns

```python
from clean_architecture import ACLAnalyzer

acl = ACLAnalyzer()

# Analyze anti-corruption layers
result = acl.analyze("/path/to/project")
print(f"ACLs found: {len(result.layers)}")

for layer in result.layers:
    print(f"\n  ACL: {layer.name}")
    print(f"    Bounded context: {layer.context}")
    print(f"    External system: {layer.external_system}")
    print(f"    Translation quality: {layer.translation_score:.0%}")
    print(f"    Leaks detected: {layer.leak_count}")
```

### Event Sourcing Architecture Analysis

```python
from clean_architecture import EventSourcingAnalyzer

esa = EventSourcingAnalyzer()

# Analyze event sourcing implementation
result = esa.analyze("/path/to/project")
print(f"Event stores: {len(result.event_stores)}")
print(f"Event types: {len(result.event_types)}")
print(f"Projections: {len(result.projections)}")
print(f"Snapshot strategy: {result.snapshot_strategy}")

for store in result.event_stores:
    print(f"\n  Store: {store.name}")
    print(f"    Events: {store.event_count}")
    print(f"    Throughput: {store.throughput_per_sec:.0f} events/sec")
    print(f"    Retention: {store.retention_days} days")
```

### CQRS Pattern Assessment

| Component | Present | Score | Recommendation |
|-----------|---------|-------|----------------|
| Command handler separation | Yes | 90% | Maintain separation |
| Query model optimization | Partial | 60% | Add read models |
| Event store implementation | No | 0% | Consider adding |
| Projection management | Yes | 80% | Add monitoring |
| Version consistency | Yes | 85% | Add conflict detection |

### Fitness Function Catalog

| Function | Severity | Description |
|----------|----------|-------------|
| No circular dependencies | Critical | Dependencies must form DAG |
| Layer deps inward | High | Dependencies point toward domain |
| Interface segregation | Medium | Clients depend on specific interfaces |
| Max coupling | Medium | Coupling ratio below threshold |
| Min cohesion | Medium | Cohesion ratio above threshold |
| Acyclic dependencies | Critical | No cycles in dependency graph |
| Stable abstractions | Medium | Abstractness correlates with stability |

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills