# Architecture Review Agent

## Overview

Reviews software architecture, identifies issues, and recommends improvements.

## Capabilities

- **Architecture Assessment**: Evaluate system architecture quality
- **Pattern Analysis**: Identify architectural patterns and anti-patterns
- **Scalability Review**: Assess scalability and performance
- **Security Review**: Evaluate security architecture
- **Tech Debt Assessment**: Identify and prioritize technical debt

## Usage

```python
from agents.architecture-review.agent import ArchitectureReviewAgent

agent = ArchitectureReviewAgent()
report = agent.review_architecture(design_document="arch.pdf")
```
