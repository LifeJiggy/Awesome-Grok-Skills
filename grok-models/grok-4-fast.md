---
name: "Grok 4 Fast"
model_id: "grok-4-fast"
provider: "xAI"
context_window: 1000000
release_date: "2025-07-01"
pricing:
  input_per_million_tokens: 1.50
  output_per_million_tokens: 7.50
  currency: "USD"
  notes: "50% cost reduction vs Grok 4 standard"
tags:
  - speed-optimized
  - low-latency
  - high-throughput
  - cost-effective
  - general-purpose
version: "4.0.0-fast"
status: "stable"
last_updated: "2025-07-01"
---

# Grok 4 Fast

## Overview

Grok 4 Fast is the speed-optimized variant of the Grok 4 family, designed for applications where latency and throughput are critical. It maintains the full 1,000,000 token context window of Grok 4 while delivering responses at significantly higher speed and lower cost.

Grok 4 Fast uses the same base architecture as Grok 4 but with optimized inference — making it ideal for real-time applications, high-volume API workloads, and interactive experiences where users expect near-instant responses.

## Key Features

- **Low Latency**: Optimized for fast time-to-first-token (TTFT) and high throughput.
- **1M Token Context**: Same context window as the full Grok 4 model.
- **50% Cost Reduction**: Half the price of Grok 4 standard for both input and output.
- **Native Tool Use**: Full tool-calling support at faster execution speeds.
- **Streaming Optimized**: Enhanced SSE performance for real-time display.

## Technical Specifications

| Specification | Value |
|---|---|
| Model ID | `grok-4-fast` |
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
| TTFT (P50) | ~200ms |
| TTFT (P99) | ~800ms |
| Throughput | ~150 tokens/sec |

## Benchmark Performance

| Benchmark | Grok 4 Fast | Grok 4 | GPT-4o-mini | Claude 3.5 Haiku |
|---|---|---|---|---|
| MMLU (5-shot) | 85.1% | 88.4% | 82.0% | 84.0% |
| HumanEval | 81.2% | 86.7% | 87.0% | 88.1% |
| MATH (competition) | 72.3% | 78.5% | 70.2% | 68.5% |
| GPQA | 52.1% | 59.8% | 48.0% | 50.2% |
| ARC-Challenge | 94.8% | 96.2% | 93.5% | 94.1% |
| HellaSwag | 93.9% | 95.1% | 93.0% | 93.5% |
| IF Eval | 84.2% | 87.3% | 83.0% | 84.5% |
| Tool Use (BFCL) | 87.5% | 91.2% | 84.0% | 85.2% |
| Latency (relative) | 1.0x | 2.5x | 0.8x | 0.7x |

## API Configuration

### Basic Request

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_XAI_API_KEY",
    base_url="https://api.x.ai/v1"
)

response = client.chat.completions.create(
    model="grok-4-fast",
    messages=[
        {"role": "user", "content": "What is the capital of France?"}
    ],
    temperature=0.3,
    max_tokens=512
)

print(response.choices[0].message.content)
```

### High-Throughput Batch Processing

```python
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key="YOUR_XAI_API_KEY",
    base_url="https://api.x.ai/v1"
)

async def classify_text(text: str) -> str:
    response = await client.chat.completions.create(
        model="grok-4-fast",
        messages=[
            {"role": "system", "content": "Classify the sentiment as positive, negative, or neutral."},
            {"role": "user", "content": text}
        ],
        temperature=0.0,
        max_tokens=20
    )
    return response.choices[0].message.content

async def batch_classify(texts: list[str]) -> list[str]:
    tasks = [classify_text(text) for text in texts]
    return await asyncio.gather(*tasks)

texts = ["Great product!", "Terrible experience", "It was okay"]
results = asyncio.run(batch_classify(texts))
print(results)
```

### Streaming for Real-Time UI

```python
stream = client.chat.completions.create(
    model="grok-4-fast",
    messages=[{"role": "user", "content": "Tell me a short joke about programming."}],
    stream=True,
    max_tokens=200
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Tool Use at Speed

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search for products by keyword",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "category": {"type": "string"},
                    "max_price": {"type": "number"}
                },
                "required": ["query"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="grok-4-fast",
    messages=[{"role": "user", "content": "Find wireless headphones under $100"}],
    tools=tools,
    tool_choice="auto"
)
```

## Pricing

| Tier | Input | Output | Notes |
|---|---|---|---|
| Standard | $1.50/M tokens | $7.50/M tokens | 50% less than Grok 4 |
| Enterprise | Custom | Custom | Volume discounts |
| Free Tier | $0.00 | $0.00 | Limited requests/day |

**Cost Comparison (per 1M tokens processed):**

| Model | Input Cost | Output Cost | Total (typical mix) |
|---|---|---|---|
| Grok 4 Fast | $1.50 | $7.50 | $3.00 |
| Grok 4 | $3.00 | $15.00 | $6.00 |
| GPT-4o-mini | $0.15 | $0.60 | $0.24 |
| Claude 3.5 Haiku | $0.80 | $4.00 | $1.60 |

**Cost Estimation Examples:**

| Task | Est. Input Tokens | Est. Output Tokens | Est. Cost |
|---|---|---|---|
| Short Q&A | 200 | 300 | $0.0003 |
| Sentiment classification | 100 | 10 | $0.0002 |
| Chatbot response | 500 | 500 | $0.0015 |
| Document summarization | 10,000 | 1,000 | $0.023 |

## Best Use Cases

1. **Real-Time Chatbots**: Low latency makes it ideal for customer-facing conversational interfaces.
2. **High-Volume Classification**: Cost-effective for large-scale text classification, moderation, and tagging pipelines.
3. **Autocomplete & Suggestions**: Fast enough for inline code completion, search suggestions, and autocomplete features.
4. **Content Moderation**: Quick evaluation of user-generated content at scale.
5. **API Middleware**: Lightweight processing in request/response pipelines where speed matters.
6. **Interactive IDE Plugins**: Code completion and inline suggestions that need sub-second response times.
7. **A/B Testing**: Run experiments with lower cost per request to gather statistically significant results faster.

## Limitations and Considerations

- **Lower Accuracy Than Grok 4**: Trades some accuracy for speed. Not recommended for tasks requiring maximum reasoning depth.
- **No Extended Thinking**: The fast variant does not support `reasoning_effort` for chain-of-thought reasoning.
- **Same Output Length Limit**: 32,768 output tokens, same as Grok 4.
- **Rate Limits May Differ**: Fast models may have separate rate limit tiers — check your account dashboard.
- **Not Ideal for Complex Reasoning**: For multi-step math, logical proofs, or nuanced analysis, use Grok 4 or Grok 4 Heavy.

## Migration Guide

### From Grok 3 Mini / Grok 3 Fast

```python
# Before
response = client.chat.completions.create(
    model="grok-3-mini",  # or "grok-3-fast"
    messages=[...]
)

# After
response = client.chat.completions.create(
    model="grok-4-fast",
    messages=[...]
)
```

### From GPT-4o-mini

```python
# Before
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...]
)

# After — change base_url and model
client = OpenAI(
    api_key="YOUR_XAI_API_KEY",
    base_url="https://api.x.ai/v1"
)
response = client.chat.completions.create(
    model="grok-4-fast",
    messages=[...]
)
```

### Cost Optimization Strategy

For most applications, consider a tiered approach:
1. Use **Grok 4 Fast** for simple, high-volume tasks (classification, Q&A, moderation).
2. Route complex tasks to **Grok 4** or **Grok 4 Heavy** only when needed.
3. This tiered approach can reduce costs by 60-80% while maintaining quality where it matters.

## Changelog

| Version | Date | Changes |
|---|---|---|
| 4.0.0-fast | 2025-07-01 | Initial release of Grok 4 Fast |

## See Also

- [Grok 4](grok-4.md) — Full-capability flagship model
- [Grok 4 Heavy](grok-4-heavy.md) — Maximum capability variant
- [Grok 4.1 Fast](grok-4-1-fast.md) — Enhanced fast variant
