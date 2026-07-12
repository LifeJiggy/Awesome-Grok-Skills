---
name: "code-golf"
category: "core"
version: "2.0.0"
tags: ["core", "code-golf", "minimal-code", "one-liners", "tricks"]
---

# Code Golf

## Overview

The Code Golf module provides techniques, tricks, and solutions for solving programming challenges with the minimum number of characters. It covers language-specific golfing tricks, common patterns, and optimization techniques for competitive code golf on platforms like Code Golf Stack Exchange.

This skill is useful for recreational programmers, competitive code golfers, and anyone looking to understand language features at a deeper level.

## Core Capabilities

- **Language Tricks**: Python, JavaScript, Ruby, GolfScript, and other golf-friendly language tricks
- **Common Patterns**: Minimum implementations for common algorithms and data manipulation
- **String Manipulation**: Shortest ways to transform, parse, and generate strings
- **Math Shortcuts**: Mathematical tricks that reduce character count
- **IO Optimization**: Minimal input/output patterns for competitive golf
- **Recursion Tricks**: Short recursive solutions using lambda and Y-combinators
- **Built-in Abuse**: Leveraging language built-ins in creative ways

## Usage Examples

```python
from code_golf import (
    GolfSolver,
    LanguageTricks,
    CharCounter,
)

# --- Solve Challenges ---
solver = GolfSolver()
solution = solver.solve(
    challenge="fizzbuzz",
    language="python",
    n=100,
)
print(f"Challenge: {solution.challenge}")
print(f"Solution: {solution.code}")
print(f"Characters: {solution.char_count}")

# --- Language Tricks ---
tricks = LanguageTricks()
lang_tricks = tricks.get_tricks("python")
for trick in lang_tricks[:5]:
    print(f"  {trick.name}: {trick.description}")
    print(f"    Code: {trick.example}")

# --- Count Characters ---
counter = CharCounter()
count = counter.count(solution.code)
print(f"Character count: {count}")
```

## Best Practices

- Learn the language's golf-specific quirks (Python's `[::-1]`, JS's `!0`/`!1`)
- Use single-letter variable names — they're shorter
- Exploit operator precedence to avoid parentheses
- Use list comprehensions and generator expressions creatively
- Abuse short-circuit evaluation (`and`/`or`) for conditionals
- Use `lambda` for anonymous functions in one-liners
- Combine multiple operations in single expressions using chained methods
- Use regex for complex string transformations in fewer characters
- Study top golf solutions on Code Golf SE for new tricks
- Remember: readability doesn't matter in code golf!

## Related Modules

- **meme-code-hybrids**: Fun code challenges with humor
- **efficient-code**: The serious side of code optimization
- **algorithmic-art**: Algorithmic art and creative coding
- **performance-tuning**: Performance optimization (the practical kind)
