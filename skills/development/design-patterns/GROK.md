---
name: "Design Patterns"
version: "2.0.0"
description: "Comprehensive design patterns toolkit with pattern detection, implementation guidance, anti-pattern identification, pattern selection, and pattern documentation for software architecture"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["development", "design-patterns", "architecture", "anti-patterns", "best-practices"]
category: "development"
personality: "design-pattern-expert"
use_cases: ["pattern detection", "implementation guidance", "anti-pattern identification", "pattern selection", "architecture design"]
---

# Design Patterns

> Production-grade design patterns framework providing pattern detection, implementation guidance, anti-pattern identification, pattern selection recommendations, and architecture documentation for building maintainable software.

## Overview

The Design Patterns module provides a comprehensive catalog of software design patterns with detection, implementation, and guidance. It implements pattern detection from code structure, anti-pattern identification, pattern selection based on requirements, implementation templates with examples, and pattern documentation generation. Every pattern includes use cases, trade-offs, and related patterns.

## Core Capabilities

### 1. Creational Patterns
- Singleton: Ensure single instance
- Factory Method: Create objects without specifying class
- Abstract Factory: Create families of related objects
- Builder: Construct complex objects step by step
- Prototype: Clone existing objects

### 2. Structural Patterns
- Adapter: Convert interface to another interface
- Bridge: Separate abstraction from implementation
- Composite: Compose objects into tree structures
- Decorator: Add responsibilities dynamically
- Facade: Simplify complex subsystems
- Proxy: Control access to another object

### 3. Behavioral Patterns
- Observer: Define subscription mechanism
- Strategy: Define family of algorithms
- Command: Encapsulate requests as objects
- State: Alter behavior when internal state changes
- Template Method: Define algorithm skeleton
- Iterator: Sequential access without exposing representation

### 4. Anti-Pattern Detection
- God Object detection
- Spaghetti Code identification
- Golden Hammer recognition
- Lava Flow detection
- Premature Optimization identification

### 5. Pattern Selection
- Requirement-based pattern recommendation
- Trade-off analysis
- Complexity assessment
- Implementation effort estimation

## Usage Examples

### Pattern Detection

```python
from design_patterns import PatternDetector

detector = PatternDetector()

# Analyze code for patterns
patterns = detector.detect_file("app.py")
print(f"Patterns detected: {len(patterns)}")
for pattern in patterns:
    print(f"  {pattern.name} ({pattern.category})")
    print(f"    Location: {pattern.file}:{pattern.line}")
    print(f"    Confidence: {pattern.confidence:.0%}")
```

### Pattern Implementation

```python
from design_patterns import PatternImpl, PatternType

# Generate pattern implementation
impl = PatternImpl.generate(
    pattern=PatternType.OBSERVER,
    language="python",
    subject_class="OrderService",
    observer_class="EmailNotifier",
)

print("Implementation:")
print(impl.code)
print("\nUsage:")
print(impl.usage_example)
```

### Anti-Pattern Detection

```python
from design_patterns import AntiPatternDetector

detector = AntiPatternDetector()

# Detect anti-patterns
anti_patterns = detector.detect("app.py")
print(f"Anti-patterns found: {len(anti_patterns)}")
for ap in anti_patterns:
    print(f"  {ap.name}: {ap.description}")
    print(f"    Impact: {ap.impact}")
    print(f"    Fix: {ap.refactoring_suggestion}")
```

### Pattern Selection

```python
from design_patterns import PatternSelector

selector = PatternSelector()

# Get pattern recommendations
recommendations = selector.recommend(
    requirements=["need to notify multiple components", "decouple sender and receiver"],
    context={"language": "python", "complexity": "medium"},
)

print("Recommended patterns:")
for rec in recommendations:
    print(f"  {rec.name}: {rec.reason}")
    print(f"    Trade-offs: {rec.trade_offs}")
```

## Best Practices

### Pattern Selection
- Don't use patterns for the sake of using patterns
- Choose patterns that solve actual problems
- Consider team familiarity and maintenance burden
- Document pattern usage in the codebase

### Implementation
- Follow the pattern's intent, not just its structure
- Keep implementations simple and focused
- Use language features where available (e.g., Python decorators for Decorator pattern)
- Test pattern implementations thoroughly

### Anti-Patterns
- Detect anti-patterns early in development
- Refactor anti-patterns incrementally
- Use code reviews to catch anti-patterns
- Document known anti-patterns and their fixes

### Documentation
- Document which patterns are used and why
- Include pattern diagrams in architecture docs
- Reference pattern sources (GoF book, etc.)
- Train team on common patterns

## Related Modules

- **refactoring-patterns**: Refactor code to use patterns
- **clean-architecture**: Architectural pattern guidance
- **code-analysis**: Detect pattern violations
- **testing-strategies**: Test pattern implementations