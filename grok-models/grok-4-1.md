---
name: "Grok 4.1"
model_id: "grok-4-1"
provider: "xAI"
context_window: 1000000
release_date: "2025-10-15"
pricing:
  input_per_million_tokens: 3.50
  output_per_million_tokens: 17.50
  currency: "USD"
  notes: "Incremental improvement over Grok 4 at slightly higher price"
tags:
  - enhanced
  - general-purpose
  - improved-reasoning
  - better-instruction-following
  - long-context
  - recommended
version: "4.1.0"
status: "stable"
last_updated: "2025-10-15"
---

# Grok 4.1

## Overview

Grok 4.1 is an enhanced iteration of the Grok 4 family, delivering meaningful improvements in instruction following, reasoning accuracy, and code quality over the original Grok 4. It maintains the same 1,000,000 token context window and API compatibility while offering better performance across a wider range of tasks.

Grok 4.1 is recommended as the new default model for production workloads that benefit from improved accuracy and consistency.

## Key Features

- **Improved Instruction Following**: More precise adherence to complex, multi-part instructions.
- **Better Code Quality**: Cleaner, more idiomatic code generation with fewer bugs.
- **Enhanced Reasoning**: Stronger performance on multi-step logical reasoning tasks.
- **Reduced Hallucination**: Lower rates of fabricated information, especially for factual queries.
- **1M Token Context**: Same context window with improved long-range coherence.
- **Native Tool Use**: Enhanced tool orchestration with better multi-step tool workflows.
- **JSON Mode Improvements**: More reliable structured output generation.

## Technical Specifications

| Specification | Value |
|---|---|
| Model ID | `grok-4-1` |
| Provider | xAI |
| Context Window | 1,000,000 tokens |
| Max Output Tokens | 32,768 tokens |
| Input Modalities | Text, Images, Documents |
| Output Modalities | Text |
| Training Cutoff | Late 2025 |
| Native Tool Use | Yes (enhanced) |
| Structured Output | Yes (JSON Schema, improved) |
| Streaming | Yes (SSE) |
| System Prompt | Supported |
| Temperature Range | 0.0 – 2.0 |
| Top-P Range | 0.0 – 1.0 |
| API Compatibility | OpenAI-compatible |
| Instruction Following | Enhanced |
| Hallucination Rate | Reduced (~30% improvement) |

## Benchmark Performance

| Benchmark | Grok 4.1 | Grok 4 | Grok 4 Heavy | GPT-4o | Claude 3.5 Sonnet |
|---|---|---|---|---|---|
| MMLU (5-shot) | 89.8% | 88.4% | 91.2% | 88.7% | 88.7% |
| HumanEval | 90.1% | 86.7% | 93.5% | 90.2% | 92.0% |
| MATH (competition) | 82.3% | 78.5% | 88.7% | 76.6% | 71.1% |
| GPQA (Diamond) | 64.2% | 59.8% | 72.3% | 53.6% | 65.0% |
| ARC-Challenge | 96.8% | 96.2% | 97.8% | 96.3% | 96.7% |
| HellaSwag | 95.5% | 95.1% | 96.1% | 95.3% | 95.4% |
| IF Eval | 90.1% | 87.3% | 91.5% | 87.5% | 88.0% |
| Tool Use (BFCL) | 93.2% | 91.2% | 94.8% | 88.3% | 89.1% |
| SWE-bench Verified | 45.3% | 38.2% | 52.1% | 33.2% | 49.0% |
| Arena-Hard | 82.1% | 78.5% | 87.3% | 79.2% | 80.5% |

## API Configuration

### Basic Request

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_XAI_API_KEY",
    base_url="https://api.x.ai/v1"
)

response = client.chat.completions.create(
    model="grok-4-1",
    messages=[
        {"role": "system", "content": "You are a senior software engineer. Write clean, well-tested code."},
        {"role": "user", "content": "Implement a thread-safe LRU cache in Python with TTL support."}
    ],
    temperature=0.2,
    max_tokens=4096
)

print(response.choices[0].message.content)
```

### Complex Multi-Part Instructions

```python
response = client.chat.completions.create(
    model="grok-4-1",
    messages=[{
        "role": "user",
        "content": """
        Perform the following tasks in order:
        1. Analyze this Python codebase for security vulnerabilities
        2. For each vulnerability found, provide:
           - A severity rating (Critical/High/Medium/Low)
           - The specific file and line number
           - A code fix with before/after comparison
           - A CWE identifier
        3. Generate a summary report in markdown format
        4. Create a prioritized remediation plan
        5. Estimate the development effort for each fix
        
        Start your response with a table of contents.
        """
    }],
    temperature=0.1,
    max_tokens=8192
)
```

### Reliable JSON Output

```python
response = client.chat.completions.create(
    model="grok-4-1",
    messages=[{
        "role": "user",
        "content": "Generate a REST API design for a blog platform with users, posts, and comments."
    }],
    response_format={"type": "json_object"},
    temperature=0.3
)

import json
api_design = json.loads(response.choices[0].message.content)
print(json.dumps(api_design, indent=2))
```

### Code Refactoring with Context

```python
response = client.chat.completions.create(
    model="grok-4-1",
    messages=[
        {"role": "system", "content": "You are a code refactoring expert. Preserve behavior while improving code quality."},
        {
            "role": "user",
            "content": f"""
            Refactor this code to be more maintainable and testable:
            
            ```python
            {large_code_block}
            ```
            
            Requirements:
            - Add type hints
            - Extract helper functions
            - Add docstrings
            - Maintain 100% backward compatibility
            - Suggest any additional improvements
            """
        }
    ],
    temperature=0.2,
    max_tokens=8192
)
```

## Pricing

| Tier | Input | Output | Notes |
|---|---|---|---|
| Standard | $3.50/M tokens | $17.50/M tokens | ~17% premium over Grok 4 |
| Enterprise | Custom | Custom | Volume discounts |
| Free Tier | Not available | Not available | — |

**Cost Comparison:**

| Model | Input | Output | Cost Index |
|---|---|---|---|
| Grok 4 Fast | $1.50 | $7.50 | 0.43x |
| Grok 4 | $3.00 | $15.00 | 0.86x |
| **Grok 4.1** | **$3.50** | **$17.50** | **1.0x (baseline)** |
| Grok 4 Heavy | $12.00 | $60.00 | 3.43x |

**Cost Estimation Examples:**

| Task | Est. Input Tokens | Est. Output Tokens | Est. Cost |
|---|---|---|---|
| Simple code generation | 2,000 | 1,500 | $0.033 |
| Security audit (medium codebase) | 50,000 | 5,000 | $0.263 |
| Documentation generation | 10,000 | 3,000 | $0.088 |
| Large refactoring task | 100,000 | 15,000 | $0.613 |

## Best Use Cases

1. **Production Workloads**: The improved accuracy and instruction following make it ideal for production deployments.
2. **Code Generation & Review**: Better code quality than Grok 4 with cleaner, more idiomatic output.
3. **Complex Instruction Following**: Multi-part tasks with specific formatting requirements.
4. **API Design & Documentation**: Structured output with reliable JSON generation.
5. **Security Auditing**: Reduced hallucination rates are critical for vulnerability detection.
6. **Data Pipeline Development**: Complex ETL logic with type safety and error handling.
7. **Customer Support Automation**: Better instruction following leads to more consistent responses.

## Limitations and Considerations

- **Higher Cost Than Grok 4**: The 17% price increase may not be justified for simple tasks.
- **Same Output Length**: 32,768 output tokens, same as other Grok 4 models.
- **No Extended Thinking**: Does not have the enhanced reasoning mode of Grok 4 Heavy.
- **Training Cutoff**: Late 2025 training data. Use web search for newer information.
- **Not the Absolute Best**: For tasks requiring maximum reasoning depth, Grok 4 Heavy still outperforms.

## Migration Guide

### From Grok 4 (Recommended Upgrade)

```python
# Before
response = client.chat.completions.create(
    model="grok-4",
    messages=[...]
)

# After — just change the model name
response = client.chat.completions.create(
    model="grok-4-1",
    messages=[...]
)
```

**Migration checklist:**
1. Update model ID from `grok-4` to `grok-4-1`
2. Test with your existing prompts — should work without changes
3. Monitor for improved accuracy in production metrics
4. Adjust temperature if needed (Grok 4.1 may be slightly more confident)

### From GPT-4o

```python
# Before (OpenAI)
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[...]
)

# After (Grok 4.1)
client = OpenAI(
    api_key="YOUR_XAI_API_KEY",
    base_url="https://api.x.ai/v1"
)
response = client.chat.completions.create(
    model="grok-4-1",
    messages=[...]
)
```

### Model Selection Decision Tree

```
Is this a simple, high-volume task?
├── Yes → Use Grok 4 Fast ($1.50/$7.50)
└── No → Does it need maximum reasoning depth?
    ├── Yes → Use Grok 4 Heavy ($12.00/$60.00)
    └── No → Does it need production-grade accuracy?
        ├── Yes → Use Grok 4.1 ($3.50/$17.50) ✓
        └── No → Use Grok 4 ($3.00/$15.00)
```

## Changelog

| Version | Date | Changes |
|---|---|---|
| 4.1.0 | 2025-10-15 | Initial release of Grok 4.1 |

## See Also

- [Grok 4](grok-4.md) — Original flagship model
- [Grok 4.1 Fast](grok-4-1-fast.md) — Speed-optimized Grok 4.1
- [Grok 4 Heavy](grok-4-heavy.md) — Maximum capability variant
