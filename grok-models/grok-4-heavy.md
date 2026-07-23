---
name: "Grok 4 Heavy"
model_id: "grok-4-heavy"
provider: "xAI"
context_window: 1000000
release_date: "2025-07-01"
pricing:
  input_per_million_tokens: 12.00
  output_per_million_tokens: 60.00
  currency: "USD"
  notes: "Premium pricing for maximum capability tier"
tags:
  - maximum-capability
  - deep-reasoning
  - complex-tasks
  - research
  - advanced-math
  - competitive-programming
version: "4.0.0-heavy"
status: "stable"
last_updated: "2025-07-01"
---

# Grok 4 Heavy

## Overview

Grok 4 Heavy is xAI's most capable model, designed for tasks that demand maximum reasoning depth, accuracy, and sophistication. It extends Grok 4 with enhanced chain-of-thought reasoning, deeper mathematical capabilities, and superior performance on the most challenging benchmarks.

Grok 4 Heavy is recommended for research-grade tasks, competitive programming, complex mathematical proofs, advanced scientific analysis, and any scenario where the quality of the output justifies the premium pricing.

## Key Features

- **Maximum Reasoning Depth**: Enhanced multi-step reasoning with longer chain-of-thought capabilities.
- **Superior Math & Science**: Best-in-class performance on competition-level mathematics and scientific reasoning.
- **Advanced Code Generation**: Excels at complex algorithms, system design, and multi-file codebases.
- **1M Token Context**: Full context window with improved long-range dependency handling.
- **Native Tool Use**: Sophisticated tool orchestration for complex multi-tool workflows.
- **Extended Thinking (Enhanced)**: Longer, deeper reasoning traces with higher accuracy.

## Technical Specifications

| Specification | Value |
|---|---|
| Model ID | `grok-4-heavy` |
| Provider | xAI |
| Context Window | 1,000,000 tokens |
| Max Output Tokens | 32,768 tokens |
| Input Modalities | Text, Images, Documents |
| Output Modalities | Text |
| Training Cutoff | Early 2025 |
| Native Tool Use | Yes |
| Structured Output | Yes (JSON Schema) |
| Streaming | Yes (SSE) |
| System Prompt | Supported |
| Temperature Range | 0.0 – 2.0 |
| Top-P Range | 0.0 – 1.0 |
| API Compatibility | OpenAI-compatible |
| Extended Thinking | Enhanced (longer traces) |
| Reasoning Budget | Up to 16K reasoning tokens |

## Benchmark Performance

| Benchmark | Grok 4 Heavy | Grok 4 | GPT-4o | Claude 3.5 Sonnet | o1-preview |
|---|---|---|---|---|---|
| MMLU (5-shot) | 91.2% | 88.4% | 88.7% | 88.7% | 91.8% |
| HumanEval | 93.5% | 86.7% | 90.2% | 92.0% | 92.4% |
| MATH (competition) | 88.7% | 78.5% | 76.6% | 71.1% | 85.5% |
| GPQA (Diamond) | 72.3% | 59.8% | 53.6% | 65.0% | 73.3% |
| ARC-Challenge | 97.8% | 96.2% | 96.3% | 96.7% | 97.2% |
| HellaSwag | 96.1% | 95.1% | 95.3% | 95.4% | 95.8% |
| IF Eval | 91.5% | 87.3% | 87.5% | 88.0% | 92.0% |
| Tool Use (BFCL) | 94.8% | 91.2% | 88.3% | 89.1% | 90.5% |
| SWE-bench Verified | 52.1% | 38.2% | 33.2% | 49.0% | 48.9% |
| AIME 2024 | 85.0% | 68.3% | 56.1% | 52.0% | 82.3% |

## API Configuration

### Basic Request

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_XAI_API_KEY",
    base_url="https://api.x.ai/v1"
)

response = client.chat.completions.create(
    model="grok-4-heavy",
    messages=[
        {"role": "system", "content": "You are an expert mathematician and scientist."},
        {"role": "user", "content": "Prove that the square root of 2 is irrational using proof by contradiction."}
    ],
    temperature=0.3,
    max_tokens=4096
)

print(response.choices[0].message.content)
```

### Extended Thinking for Complex Problems

```python
response = client.chat.completions.create(
    model="grok-4-heavy",
    messages=[
        {
            "role": "user",
            "content": """Design a distributed caching system that:
            1. Supports consistent hashing with virtual nodes
            2. Handles node failures with automatic rebalancing
            3. Maintains cache coherence across nodes
            4. Provides bounded memory usage with LRU eviction
            
            Provide a detailed architectural overview and implementation in Python."""
        }
    ],
    reasoning_effort="high",
    max_tokens=8192
)
```

### Multi-Tool Orchestration

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "run_python",
            "description": "Execute Python code and return output",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Python code to execute"}
                },
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_papers",
            "description": "Search academic papers on arXiv",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "max_results": {"type": "integer"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_database",
            "description": "Execute SQL query against analytics database",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql": {"type": "string"},
                    "database": {"type": "string"}
                },
                "required": ["sql"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="grok-4-heavy",
    messages=[{
        "role": "user",
        "content": "Analyze the relationship between paper publications in AI safety and funding trends. Search for recent papers, pull the funding data from our database, and create a visualization showing the correlation."
    }],
    tools=tools,
    tool_choice="auto"
)
```

### Structured Output for Complex Schemas

```python
response = client.chat.completions.create(
    model="grok-4-heavy",
    messages=[{
        "role": "user",
        "content": "Analyze this codebase and provide a structured security audit report."
    }],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "security_audit",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "summary": {"type": "string"},
                    "risk_level": {"type": "string", "enum": ["critical", "high", "medium", "low", "info"]},
                    "findings": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "severity": {"type": "string"},
                                "description": {"type": "string"},
                                "remediation": {"type": "string"},
                                "cwe_id": {"type": "string"}
                            },
                            "required": ["title", "severity", "description", "remediation"]
                        }
                    }
                },
                "required": ["summary", "risk_level", "findings"]
            }
        }
    }
)
```

## Pricing

| Tier | Input | Output | Notes |
|---|---|---|---|
| Standard | $12.00/M tokens | $60.00/M tokens | Premium tier |
| Enterprise | Custom | Custom | Volume discounts, priority queue |
| Free Tier | Not available | Not available | — |

**Cost Comparison (per 1M tokens processed):**

| Model | Input Cost | Output Cost | Cost Ratio vs Grok 4 |
|---|---|---|---|
| Grok 4 Heavy | $12.00 | $60.00 | 4x |
| Grok 4 | $3.00 | $15.00 | 1x (baseline) |
| Grok 4 Fast | $1.50 | $7.50 | 0.5x |
| o1-preview | $15.00 | $60.00 | 5x |

**Cost Estimation Examples:**

| Task | Est. Input Tokens | Est. Output Tokens | Est. Cost |
|---|---|---|---|
| Complex math proof | 500 | 2,000 | $0.126 |
| Architecture design | 2,000 | 4,000 | $0.264 |
| Code review (large PR) | 50,000 | 5,000 | $0.900 |
| Research analysis | 100,000 | 10,000 | $1.800 |

## Best Use Cases

1. **Competitive Programming**: AIME-level math problems, algorithmic challenges, and competitive coding.
2. **Scientific Research**: Complex hypothesis testing, literature synthesis, and experimental design.
3. **System Architecture**: Designing distributed systems, database architectures, and infrastructure.
4. **Advanced Code Generation**: Multi-file refactoring, complex algorithm implementation, and codebase migration.
5. **Security Auditing**: Deep vulnerability analysis with actionable remediation guidance.
6. **Academic Paper Analysis**: Synthesizing findings across large research corpora.
7. **Financial Modeling**: Complex quantitative analysis and risk assessment.
8. **Legal Document Analysis**: Nuanced interpretation of complex legal texts.

## Limitations and Considerations

- **High Cost**: At $12/$60 per million tokens, this model is 4x the price of Grok 4. Use only when the task justifies the premium.
- **Slower Response Times**: Deeper reasoning means longer processing. Expect 2-5x the latency of Grok 4 Fast.
- **Same Output Limit**: 32,768 output tokens. Very long outputs may still require chunking.
- **Overkill for Simple Tasks**: Don't use Grok 4 Heavy for classification, simple Q&A, or straightforward content generation.
- **Extended Thinking Tokens Count**: Reasoning tokens consume the output budget. Plan accordingly for very complex prompts.
- **Rate Limits**: Premium tier may have different rate limit configurations.

## Migration Guide

### From Grok 4 (Upgrade Path)

```python
# When tasks demand maximum quality
response = client.chat.completions.create(
    model="grok-4-heavy",  # was "grok-4"
    messages=[...],
    reasoning_effort="high"  # leverage enhanced reasoning
)
```

**When to upgrade from Grok 4 to Grok 4 Heavy:**
- Benchmark performance is insufficient for your task
- Complex multi-step reasoning is critical
- Mathematical or scientific accuracy is paramount
- Code generation needs to handle complex architectures

### From o1-preview

```python
# Before (OpenAI)
response = client.chat.completions.create(
    model="o1-preview",
    messages=[...]
)

# After (Grok 4 Heavy)
client = OpenAI(
    api_key="YOUR_XAI_API_KEY",
    base_url="https://api.x.ai/v1"
)
response = client.chat.completions.create(
    model="grok-4-heavy",
    messages=[...],
    reasoning_effort="high"
)
```

### Cost Optimization: When to Use What

| Task Complexity | Recommended Model | Why |
|---|---|---|
| Simple Q&A, classification | Grok 4 Fast | Cheapest, fast enough |
| General chat, code generation | Grok 4 | Best balance |
| Complex reasoning, math, research | Grok 4 Heavy | Maximum accuracy |
| A/B testing, prototyping | Grok 4 Fast | Low cost per experiment |

## Changelog

| Version | Date | Changes |
|---|---|---|
| 4.0.0-heavy | 2025-07-01 | Initial release of Grok 4 Heavy |

## See Also

- [Grok 4](grok-4.md) — Standard capability model
- [Grok 4 Fast](grok-4-fast.md) — Speed-optimized variant
- [Grok 4.1](grok-4-1.md) — Enhanced variant
