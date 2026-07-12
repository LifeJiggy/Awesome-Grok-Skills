---
name: "efficient-code"
category: "core"
version: "2.0.0"
tags: ["core", "efficient-code", "optimization", "performance", "best-practices"]
---

# Efficient Code

## Overview

The Efficient Code module provides comprehensive guidance for writing clean, performant, and maintainable code across programming languages. It covers algorithm selection, data structure optimization, memory management, concurrency patterns, and code quality metrics. The module emphasizes practical optimization techniques with measurable impact.

This skill is essential for software engineers seeking to write code that is both correct and performant, and for tech leads establishing coding standards for their teams.

## Core Capabilities

- **Algorithm Selection**: Choosing optimal algorithms based on time/space complexity and input characteristics
- **Data Structure Optimization**: Selecting and implementing data structures for specific access patterns
- **Memory Management**: Object pooling, lazy evaluation, flyweight patterns, and memory-efficient data representations
- **Concurrency**: Thread-safe patterns, async/await optimization, lock-free data structures, and parallel processing
- **Code Quality**: Cyclomatic complexity, function length guidelines, naming conventions, and DRY principle application
- **Profiling**: Identifying bottlenecks, flame graph analysis, and systematic optimization approaches
- **Language-Specific**: Python, JavaScript, Go, Rust, and Java optimization idioms

## Usage Examples

```python
from efficient_code import (
    ComplexityAnalyzer,
    DataStructureSelector,
    MemoryOptimizer,
    ConcurrencyHelper,
    CodeQualityChecker,
)

# --- Complexity Analysis ---
analyzer = ComplexityAnalyzer()
analysis = analyzer.analyze_function(
    code="for i in range(n): for j in range(n): pass",
    input_sizes=[100, 1000, 10000],
)
print(f"Time complexity: {analysis.time_complexity}")
print(f"Space complexity: {analysis.space_complexity}")

# --- Data Structure Selection ---
selector = DataStructureSelector()
recommendation = selector.recommend(
    operations=["insert", "lookup", "delete"],
    access_pattern="random",
    size_estimate=100000,
    ordering_required=False,
)
print(f"Recommended: {recommendation.structure}")
print(f"Reason: {recommendation.reasoning}")

# --- Memory Optimization ---
optimizer = MemoryOptimizer()
suggestions = optimizer.analyze(
    code_sample="large_list = [dict() for _ in range(1000000)]",
    language="python",
)
for suggestion in suggestions:
    print(f"  {suggestion}")

# --- Concurrency ---
helper = ConcurrencyHelper()
pattern = helper.recommend_pattern(
    task_type="io_bound",
    parallelism_needed=True,
    shared_state=True,
)
print(f"Pattern: {pattern.name}")
print(f"Implementation: {pattern.implementation}")

# --- Code Quality ---
checker = CodeQualityChecker()
issues = checker.check("def f(x): return x+1 if x>0 else None")
for issue in issues:
    print(f"  [{issue.severity}] {issue.message}")
```

## Best Practices

- Profile before optimizing — premature optimization is the root of all evil
- Choose the right algorithm first, then optimize the implementation
- Use appropriate data structures: hash maps for lookups, arrays for sequential access
- Minimize object allocation in hot paths — use object pools where appropriate
- Prefer iteration over recursion for deep call stacks
- Use lazy evaluation to defer expensive computations until needed
- Apply the principle of least astonishment in API design
- Keep functions small and focused — single responsibility principle
- Write self-documenting code with clear naming — comments should explain WHY, not WHAT
- Measure everything — use benchmarks to validate optimization claims

## Related Modules

- **performance-tuning**: Runtime performance profiling and optimization
- **code-golf**: Minimal code solutions for educational purposes
- **algorithmic-art**: Creative algorithm implementations
- **meme-code-hybrids**: Fun and educational code patterns
