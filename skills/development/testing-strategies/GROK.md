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
    print(f"⚠ Anti-pattern detected: {analysis.anti_pattern_type}")
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
- Don't chase 100% coverage — focus on critical paths
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