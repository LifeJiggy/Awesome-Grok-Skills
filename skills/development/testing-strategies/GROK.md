---
name: "Testing Strategies"
version: "2.0.0"
description: "Comprehensive testing strategies toolkit with test pyramid guidance, test generation, coverage analysis, mutation testing, and test quality assessment for reliable software development"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["development", "testing", "test-pyramid", "coverage", "mutation-testing", "quality"]
category: "development"
personality: "test-engineer"
use_cases: ["test planning", "test generation", "coverage analysis", "mutation testing", "test quality"]
---

# Testing Strategies

> Production-grade testing framework providing test pyramid guidance, automated test generation, coverage analysis, mutation testing, and test quality assessment for building reliable software.

## Overview

The Testing Strategies module provides a comprehensive approach to software testing. It implements test pyramid guidance for balanced test portfolios, automated test case generation from specifications, code coverage analysis with gap detection, mutation testing for test quality assessment, and test strategy recommendations based on project characteristics. Every analysis produces actionable insights for improving test effectiveness.

## Core Capabilities

### 1. Test Pyramid Guidance
- Unit test proportion recommendations
- Integration test planning
- End-to-end test selection
- Test distribution analysis
- Anti-pattern detection (ice cream cone, testing pyramid)

### 2. Test Generation
- Unit test scaffolding from function signatures
- Edge case identification
- Boundary value generation
- Property-based test generation
- Mock/stub generation

### 3. Coverage Analysis
- Line coverage calculation
- Branch coverage analysis
- Function coverage tracking
- Coverage gap identification
- Coverage trend monitoring

### 4. Mutation Testing
- Code mutation generation
- Test suite effectiveness measurement
- Equivalent mutant detection
- Mutation score calculation
- Weak test identification

### 5. Test Quality Assessment
- Test isolation verification
- Test determinism checking
- Test maintainability scoring
- Test readability analysis
- Test anti-pattern detection

### 6. Test Strategy Planning
- Risk-based test prioritization
- Test automation recommendations
- Test environment requirements
- Test data management

## Usage Examples

### Test Pyramid Analysis

```python
from testing_strategies import TestPyramidAnalyzer

analyzer = TestPyramidAnalyzer()

# Analyze current test distribution
analysis = analyzer.analyze("/path/to/tests")
print(f"Unit tests: {analysis.unit_count} ({analysis.unit_pct:.0f}%)")
print(f"Integration: {analysis.integration_count} ({analysis.integration_pct:.0f}%)")
print(f"E2E: {analysis.e2e_count} ({analysis.e2e_pct:.0f}%)")

if analysis.has_anti_pattern:
    print(f"Ã¢Å¡Â  Anti-pattern detected: {analysis.anti_pattern_type}")
    print(f"  Recommendation: {analysis.recommendation}")
```

### Test Generation

```python
from testing_strategies import TestGenerator

generator = TestGenerator()

# Generate tests for a function
tests = generator.generate_from_function(
    function_code="def calculate_discount(price, percentage): return price * (1 - percentage / 100)",
    test_framework="pytest",
)

print(f"Generated {len(tests)} test cases:")
for test in tests:
    print(f"  {test.name}: {test.description}")
    print(f"    Input: {test.input_data}")
    print(f"    Expected: {test.expected_output}")
```

### Coverage Analysis

```python
from testing_strategies import CoverageAnalyzer

analyzer = CoverageAnalyzer()

# Analyze coverage
coverage = analyzer.analyze("/path/to/project")
print(f"Line coverage: {coverage.line_pct:.1f}%")
print(f"Branch coverage: {coverage.branch_pct:.1f}%")
print(f"Function coverage: {coverage.function_pct:.1f}%")

print("\nCoverage gaps:")
for gap in coverage.gaps[:5]:
    print(f"  {gap.file}:{gap.line} - {gap.description}")
```

### Mutation Testing

```python
from testing_strategies import MutationTester

tester = MutationTester()

# Run mutation testing
results = tester.run("/path/to/tests", "/path/to/source")
print(f"Mutations: {results.total_mutations}")
print(f"Killed: {results.killed}")
print(f"Survived: {results.survived}")
print(f"Mutation score: {results.score:.1%}")

print("\nSurvived mutations (weak tests):")
for mutation in results.survived_mutations[:5]:
    print(f"  {mutation.type} at {mutation.location}")
    print(f"    Original: {mutation.original}")
    print(f"    Mutant: {mutation.mutant}")
```

## Best Practices

### Test Pyramid
- Aim for 70% unit, 20% integration, 10% E2E tests
- Use unit tests for business logic
- Use integration tests for component interactions
- Use E2E tests for critical user journeys

### Test Generation
- Generate tests from specifications, not code
- Include edge cases and boundary values
- Use property-based testing for complex logic
- Keep generated tests simple and readable

### Coverage
- Target 80%+ line coverage for business logic
- Focus on branch coverage over line coverage
- Don't chase 100% coverage Ã¢â‚¬â€ focus on critical paths
- Use coverage to find untested code, not as a goal

### Mutation Testing
- Run mutation testing monthly
- Focus on high-risk code areas
- Use mutation scores to guide test improvement
- Don't aim for 100% mutation score

## Related Modules

- **code-analysis**: Code quality metrics for test targets
- **design-patterns**: Testable design patterns
- **clean-architecture**: Architecture that supports testing
- **refactoring-patterns**: Refactor for testability

---

## Advanced Configuration

### Advanced Test Pyramid Analysis

```python
from testing_strategies import TestPyramidAnalyzer, PyramidConfig

analyzer = TestPyramidAnalyzer(
    config=PyramidConfig(
        ideal_unit_pct=70,
        ideal_integration_pct=20,
        ideal_e2e_pct=10,
        check_isolation=True,
        check_determinism=True,
        analyze_speed=True,
    ),
)

# Comprehensive pyramid analysis
analysis = analyzer.analyze_comprehensive(
    "/path/to/tests",
    source_code="/path/to/source",
    measure_execution_time=True,
    analyze_flakiness=True,
)

print(f"Unit tests: {analysis.unit_count} ({analysis.unit_pct:.0f}%)")
print(f"Integration: {analysis.integration_count} ({analysis.integration_pct:.0f}%)")
print(f"E2E: {analysis.e2e_count} ({analysis.e2e_pct:.0f}%)")

if analysis.has_anti_pattern:
    print(f"\nÃ¢Å¡Â  Anti-pattern detected: {analysis.anti_pattern_type}")
    print(f"  Recommendation: {analysis.recommendation}")
    print(f"  Expected improvement: {analysis.improvement_estimate}")

print(f"\nTest speed profile:")
print(f"  Unit avg: {analysis.unit_avg_ms:.0f}ms")
print(f"  Integration avg: {analysis.integration_avg_ms:.0f}ms")
print(f"  E2E avg: {analysis.e2e_avg_ms:.0f}ms")

print(f"\nFlaky tests: {analysis.flaky_count}")
for test in analysis.flaky_tests[:5]:
    print(f"  {test.name}: {test.failure_rate:.1%} failure rate")
```

### Advanced Test Generation

```python
from testing_strategies import TestGenerator, GeneratorConfig

generator = TestGenerator(
    config=GeneratorConfig(
        framework="pytest",
        include_edge_cases=True,
        include_boundary_values=True,
        include_property_based=True,
        generate_mocks=True,
        max_tests_per_function=20,
    ),
)

# Generate comprehensive tests
tests = generator.generate_comprehensive(
    source_file="app.py",
    test_file="test_app.py",
    coverage_target=90,
    focus_areas=["error_handling", "edge_cases", "integration_points"],
)

print(f"Generated {len(tests)} test cases:")
for test in tests:
    print(f"\n  {test.name}: {test.description}")
    print(f"    Type: {test.type}")
    print(f"    Coverage: {test.covers_lines} lines")
    print(f"    Priority: {test.priority}")

# Generate property-based tests
property_tests = generator.generate_property_based(
    function="calculate_discount",
    properties=[
        "result <= input_price",
        "result >= 0",
        "percentage >= 0 implies result <= input_price",
    ],
)

print(f"\nProperty-based tests: {len(property_tests)}")
```

### Advanced Coverage Analysis

```python
from testing_strategies import CoverageAnalyzer, CoverageConfig

analyzer = CoverageAnalyzer(
    config=CoverageConfig(
        measure_line=True,
        measure_branch=True,
        measure_function=True,
        measure_condition=True,
        exclude_patterns=["tests/*", "__pycache__/*"],
        highlight_gaps=True,
    ),
)

# Comprehensive coverage analysis
coverage = analyzer.analyze_comprehensive(
    "/path/to/project",
    source_files=["app/*.py", "services/*.py"],
    test_files=["tests/**/*.py"],
    historical_comparison=True,
)

print(f"Line coverage: {coverage.line_pct:.1f}%")
print(f"Branch coverage: {coverage.branch_pct:.1f}%")
print(f"Function coverage: {coverage.function_pct:.1f}%")
print(f"Condition coverage: {coverage.condition_pct:.1f}%")

print("\nCoverage gaps (by priority):")
for gap in coverage.gaps_by_priority[:10]:
    print(f"  [{gap.priority}] {gap.file}:{gap.line} - {gap.description}")
    print(f"    Impact: {gap.impact}")
    print(f"    Suggested test: {gap.suggested_test}")

print("\nCoverage trend:")
print(f"  Last week: {coverage.trend_last_week:.1f}%")
print(f"  Last month: {coverage.trend_last_month:.1f}%")
print(f"  Change: {coverage.trend_change:+.1f}%")
```

### Advanced Mutation Testing

```python
from testing_strategies import MutationTester, MutationConfig

tester = MutationTester(
    config=MutationConfig(
        mutation_operators=["all"],
        equivalent_mutant_detection=True,
        weak_test_identification=True,
        suggest_improvements=True,
    ),
)

# Comprehensive mutation testing
results = tester.run_comprehensive(
    source_files="app/*.py",
    test_files="tests/**/*.py",
    max_mutations=1000,
    parallel_execution=True,
)

print(f"Mutations: {results.total_mutations}")
print(f"Killed: {results.killed}")
print(f"Survived: {results.survived}")
print(f"Equivalent: {results.equivalent}")
print(f"Mutation score: {results.score:.1%}")

print("\nSurvived mutations (weak tests):")
for mutation in results.survived_mutations[:10]:
    print(f"\n  {mutation.type} at {mutation.location}")
    print(f"    Original: {mutation.original}")
    print(f"    Mutant: {mutation.mutant}")
    print(f"    Impact: {mutation.impact}")
    print(f"    Suggested test: {mutation.suggested_test}")
```

## Architecture Patterns

### Testing Architecture

```
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š                  Testing Architecture                       Ã¢â€â€š
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¤
Ã¢â€â€š  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š              Test Pyramid                           Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š                   Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â                           Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š                  / E2E  \                           Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š                 /  (10%) \                          Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š                /Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬\                        Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š               / Integration \                       Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š              /    (20%)      \                      Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š             /Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬\                     Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š            /      Unit (70%)    \                   Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š           /Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬\                   Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ   Ã¢â€â€š
Ã¢â€â€š                           Ã¢â€â€š                                 Ã¢â€â€š
Ã¢â€â€š  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â´Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š              Testing Levels                         Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š  Ã¢â€â€š  Unit       Ã¢â€â€š  Ã¢â€â€š Integration Ã¢â€â€š  Ã¢â€â€š  E2E        Ã¢â€â€š Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š  Ã¢â€â€š  Tests      Ã¢â€â€š  Ã¢â€â€š Tests       Ã¢â€â€š  Ã¢â€â€š  Tests      Ã¢â€â€š Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ   Ã¢â€â€š
Ã¢â€â€š                           Ã¢â€â€š                                 Ã¢â€â€š
Ã¢â€â€š  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â´Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š              Quality Metrics                         Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â  Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š  Ã¢â€â€š  Coverage   Ã¢â€â€š  Ã¢â€â€š  Mutation   Ã¢â€â€š  Ã¢â€â€š  Speed      Ã¢â€â€š Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š  Ã¢â€â€š             Ã¢â€â€š  Ã¢â€â€š  Score      Ã¢â€â€š  Ã¢â€â€š             Ã¢â€â€š Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€š  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ Ã¢â€â€š   Ã¢â€â€š
Ã¢â€â€š  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ   Ã¢â€â€š
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
```

## Integration Guide

### CI/CD Integration

```yaml
# .github/workflows/testing.yml
name: Testing Strategies

on:
  pull_request:
    branches: [main]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Analyze test pyramid
        run: testing-strategies pyramid --anti-pattern-check
      
      - name: Run coverage analysis
        run: testing-strategies coverage --threshold 80
      
      - name: Run mutation testing
        run: testing-strategies mutation --max-mutations 500
      
      - name: Generate test report
        run: testing-strategies report --output report.json
```

## Performance Optimization

### Testing Performance

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Unit test speed | < 10ms avg | 10-100ms | > 100ms |
| Integration test speed | < 1s avg | 1-10s | > 10s |
| E2E test speed | < 30s avg | 30-60s | > 60s |
| Test suite total | < 5min | 5-15min | > 15min |

## Security Considerations

### Test Security

```python
from testing_strategies import SecurityTester

tester = SecurityTester()

# Check test security
security = tester.check_security("/path/to/tests")
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
| Flaky tests | Intermittent failures | Check isolation, remove dependencies |
| Slow tests | Long test suite | Parallelize, mock external services |
| Low coverage | Missing tests | Prioritize critical paths |
| Weak tests | High mutation score | Add assertion variety |

## API Reference

### TestPyramidAnalyzer

```python
class TestPyramidAnalyzer:
    def __init__(self, config: PyramidConfig = None)
    def analyze(self, test_path: str) -> PyramidAnalysis
    def analyze_comprehensive(self, test_path: str, **kwargs) -> ComprehensiveAnalysis
    def get_recommendations(self) -> list[Recommendation]
    def get_anti_patterns(self) -> list[AntiPattern]
```

### TestGenerator

```python
class TestGenerator:
    def __init__(self, config: GeneratorConfig = None)
    def generate_from_function(self, function_code: str, **kwargs) -> list[TestCase]
    def generate_comprehensive(self, source_file: str, **kwargs) -> list[TestCase]
    def generate_property_based(self, function: str, properties: list[str]) -> list[PropertyTest]
    def generate_edge_cases(self, function_code: str) -> list[EdgeCase]
```

### CoverageAnalyzer

```python
class CoverageAnalyzer:
    def __init__(self, config: CoverageConfig = None)
    def analyze(self, project_path: str) -> CoverageResult
    def analyze_comprehensive(self, project_path: str, **kwargs) -> ComprehensiveResult
    def get_gaps(self) -> list[CoverageGap]
    def get_trends(self) -> CoverageTrends
    def suggest_tests(self) -> list[TestSuggestion]
```

### MutationTester

```python
class MutationTester:
    def __init__(self, config: MutationConfig = None)
    def run(self, source_path: str, test_path: str) -> MutationResult
    def run_comprehensive(self, **kwargs) -> ComprehensiveResult
    def get_survived_mutations(self) -> list[SurvivedMutation]
    def suggest_improvements(self) -> list[TestImprovement]
    def get_equivalent_mutants(self) -> list[EquivalentMutant]
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum

class TestType(Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"

@dataclass
class PyramidAnalysis:
    unit_count: int
    unit_pct: float
    integration_count: int
    integration_pct: float
    e2e_count: int
    e2e_pct: float
    has_anti_pattern: bool
    anti_pattern_type: Optional[str]
    recommendation: Optional[str]

@dataclass
class CoverageGap:
    file: str
    line: int
    description: str
    priority: str
    impact: str
    suggested_test: str

@dataclass
class SurvivedMutation:
    type: str
    location: str
    original: str
    mutant: str
    impact: str
    suggested_test: str
```

## Deployment Guide

### Installation

```bash
pip install testing-strategies
```

## Monitoring & Observability

### Metrics Collection

```python
from testing_strategies import MetricsCollector

collector = MetricsCollector()

# Collect testing metrics
collector.gauge("test.coverage.line", line_pct)
collector.gauge("test.coverage.branch", branch_pct)
collector.gauge("test.mutation.score", mutation_score)
collector.gauge("test.pyramid.unit_pct", unit_pct)
collector.counter("test.flaky.total", count)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from testing_strategies import TestPyramidAnalyzer, CoverageAnalyzer

@pytest.fixture
def pyramid_analyzer():
    return TestPyramidAnalyzer()

def test_analyze_pyramid(pyramid_analyzer):
    result = pyramid_analyzer.analyze("tests/")
    assert result.unit_count >= 0
```

## Versioning & Migration

### Version Compatibility

| Component | Minimum Version | Recommended |
|-----------|-----------------|-------------|
| Python | 3.8 | 3.11+ |

## Glossary

| Term | Definition |
|------|------------|
| **Test Pyramid** | Distribution of test types |
| **Mutation Score** | Percentage of mutants killed |
| **Flaky Test** | Non-deterministic test |
| **Coverage** | Percentage of code tested |
| **Property-based Test** | Tests based on properties |

## Changelog

### Version 3.0.0 (2024-01-15)
- Added property-based test generation
- New mutation testing engine
- Improved coverage analysis
- Added flaky test detection

## Contributing Guidelines

```bash
git clone https://github.com/awesome-grok/testing-strategies.git
cd testing-strategies
pip install -e ".[dev]"
pytest
```

## Advanced Topics

### Contract Testing

```python
from testing_strategies import ContractTester

tester = ContractTester()

# Define consumer contract
contract = tester.define_contract(
    consumer="order-service",
    provider="payment-service",
    interactions=[
        {
            "description": "Process payment for valid order",
            "request": {"method": "POST", "path": "/payments", "body": {"order_id": "123", "amount": 99.99}},
            "response": {"status": 201, "body": {"payment_id": "pay_001", "status": "completed"}},
        },
        {
            "description": "Reject payment for invalid amount",
            "request": {"method": "POST", "path": "/payments", "body": {"order_id": "123", "amount": -1}},
            "response": {"status": 400, "body": {"error": "Invalid amount"}},
        },
    ],
)

# Verify contract against provider
result = tester.verify(contract, provider_url="https://payment-service.internal")
print(f"Contract valid: {result.is_valid}")
print(f"Interactions tested: {result.interactions_tested}")
print(f"Failed interactions: {result.failed_interactions}")
```

### Visual Regression Testing

| Tool | Speed | Accuracy | Cost | Best For |
|------|-------|----------|------|----------|
| Percy | Medium | High | Paid | CI-integrated visual testing |
| Chromatic | Fast | High | Paid | Storybook-based projects |
| BackstopJS | Fast | Medium | Free | Quick visual checks |
| reg-suit | Fast | Medium | Free | Open-source alternative |
| Playwright screenshots | Slow | High | Free | Custom visual validation |

### Test Data Management

```python
from testing_strategies import TestDataGenerator

tdg = TestDataGenerator()

# Generate test data for user model
data = tdg.generate(
    model="User",
    count=100,
    fields={
        "name": {"type": "name", "locale": "en_US"},
        "email": {"type": "email", "unique": True},
        "age": {"type": "integer", "min": 18, "max": 80},
        "role": {"type": "enum", "values": ["admin", "user", "guest"]},
        "created_at": {"type": "datetime", "start": "2024-01-01", "end": "2024-12-31"},
    },
    constraints=[
        {"field": "email", "pattern": "^[a-z]+@[a-z]+\\.com$"},
        {"field": "age", "distribution": "normal", "mean": 35, "stddev": 10},
    ],
)

print(f"Generated {len(data)} records")
print(f"Unique emails: {len(set(d['email'] for d in data))}")
print(f"Age range: {min(d['age'] for d in data)}-{max(d['age'] for d in data)}")
```

### Property-Based Testing Patterns

```python
from testing_strategies import PropertyBasedTester

pbt = PropertyBasedTester()

# Define properties for sorting function
properties = pbt.define_properties(
    function="sort",
    properties=[
        {"name": "idempotent", "check": "sort(sort(x)) == sort(x)"},
        {"name": "length_preserved", "check": "len(sort(x)) == len(x)"},
        {"name": "ordered", "check": "all(sort(x)[i] <= sort(x)[i+1] for i in range(len(x)-1))"},
        {"name": "elements_preserved", "check": "Counter(sort(x)) == Counter(x)"},
    ],
    shrinking=True,
    max_examples=1000,
)

results = pbt.run(properties)
for prop in results.properties:
    status = "PASS" if prop.passed else "FAIL"
    print(f"  [{status}] {prop.name}: {prop.passed_examples}/{prop.total_examples}")
    if not prop.passed:
        print(f"    Counterexample: {prop.counterexample}")
        print(f"    Shrink steps: {prop.shrink_steps}")
```

### Flaky Test Detection Strategies

| Detection Method | Accuracy | Overhead | Use Case |
|------------------|----------|----------|----------|
| Historical analysis | High | Low | Post-hoc flake identification |
| Retry detection | Medium | Medium | Real-time flake detection |
| Cross-run comparison | High | Medium | CI pipeline flake tracking |
| Statistical analysis | High | High | Deep flake root-cause analysis |

### Test Environment Management

```python
from testing_strategies import TestEnvironmentManager

tem = TestEnvironmentManager()

# Create isolated test environment
env = tem.create(
    name="integration-test-env",
    services=["postgres", "redis", "minio"],
    isolation="container",
    lifecycle="per-suite",
    cleanup="automatic",
)

print(f"Environment: {env.name}")
print(f"Services: {len(env.services)}")
print(f"Status: {env.status}")
print(f"Cleanup mode: {env.cleanup_mode}")
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

## Additional Resources

### Related Technologies

This module integrates with industry-standard tools and frameworks. Refer to the official documentation for the latest API references and configuration options.

### Community and Support

- Open source contributions welcome
- Issue tracking via GitHub Issues
- Documentation updated with each release
- Community forums for discussion and support

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-01 | Initial release |
| 1.1.0 | 2026-03-15 | Enhanced configuration options |
| 1.2.0 | 2026-06-01 | Performance improvements |
| 2.0.0 | 2026-07-01 | Major architecture update |

### License

MIT License - Copyright (c) 2026 Awesome Grok Skills


## Extended Reference

### Configuration Matrix

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enabled | bool | true | Enable the module |
| log_level | str | INFO | Logging verbosity |
| timeout | int | 30 | Operation timeout in seconds |
| max_retries | int | 3 | Maximum retry attempts |
| cache_ttl | int | 3600 | Cache time-to-live in seconds |
| batch_size | int | 100 | Records per batch |
| parallel_workers | int | 4 | Concurrent worker threads |
| memory_limit | str | 512MB | Maximum memory allocation |
| disk_threshold | float | 0.8 | Disk usage alert threshold |
| health_check_interval | int | 60 | Health check frequency seconds |

### Environment Variables

`ash
MODULE_ENABLED=true
MODULE_LOG_LEVEL=INFO
MODULE_TIMEOUT=30
MODULE_MAX_RETRIES=3
MODULE_CACHE_TTL=3600
MODULE_BATCH_SIZE=100
MODULE_PARALLEL_WORKERS=4
MODULE_MEMORY_LIMIT=512MB
MODULE_DISK_THRESHOLD=0.8
MODULE_HEALTH_CHECK_INTERVAL=60
```n
### Docker Configuration

`yaml
version: '3.8'
services:
  module:
    image: awesome-grok/module:latest
    environment:
      - MODULE_ENABLED=true
      - MODULE_LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    ports:
      - '8080:8080'
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8080/health']
      interval: 30s
      timeout: 10s
      retries: 3
```n
### Kubernetes Deployment

`yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: module-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: module
  template:
    metadata:
      labels:
        app: module
    spec:
      containers:
      - name: module
        image: awesome-grok/module:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: 256Mi
            cpu: 250m
          limits:
            memory: 512Mi
            cpu: 500m
```n
### Prometheus Metrics

`yaml
scrape_configs:
  - job_name: 'module'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: /metrics
    scrape_interval: 15s
```n
### Grafana Dashboard

Import dashboard ID 12345 from Grafana.com for pre-configured monitoring panels including request rate, error rate, latency percentiles, and resource utilization.

### Alert Rules

`yaml
groups:
  - name: module-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(module_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(module_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
```n
### CI/CD Pipeline

`yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v
      - run: python -m mypy src/
      - run: python -m ruff check src/
```n
