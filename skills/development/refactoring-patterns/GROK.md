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