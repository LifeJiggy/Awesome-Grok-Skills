---
name: "Grok 4"
model_id: "grok-4"
provider: "xAI"
context_window: 1000000
release_date: "2025-07-01"
pricing:
  input_per_million_tokens: 3.00
  output_per_million_tokens: 15.00
  currency: "USD"
  notes: "Volume discounts available for enterprise customers"
tags:
  - flagship
  - general-purpose
  - native-tool-use
  - multimodal
  - long-context
  - recommended
version: "4.0.0"
status: "stable"
last_updated: "2025-07-01"
---

# Grok 4

## Overview

Grok 4 is xAI's flagship large language model, representing the culmination of advances in reasoning, tool use, and long-context understanding. With a native 1,000,000 token context window and built-in tool-calling capabilities, Grok 4 is designed to be the default choice for a wide range of tasks — from complex multi-step reasoning to real-time data analysis and code generation.

Grok 4 replaces Grok 3 as the recommended general-purpose model. It delivers stronger performance across all benchmarks while maintaining the same API contract, making migration straightforward for existing users.

## Key Features

- **1M Token Context Window**: Process entire codebases, lengthy documents, or multi-hour conversations without truncation.
- **Native Tool Use**: First-class support for function calling, structured outputs, and multi-tool orchestration.
- **Multimodal Input**: Accept text, images, and documents as input. Generate text output.
- **Real-Time Data Access**: Integrated web search and information retrieval via xAI's data pipeline.
- **Extended Thinking**: Optional chain-of-thought reasoning for complex problem-solving tasks.
- **Streaming Support**: Server-sent events (SSE) for real-time output delivery.

## Technical Specifications

| Specification | Value |
|---|---|
| Model ID | `grok-4` |
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

## Benchmark Performance

| Benchmark | Grok 4 | Grok 3 | GPT-4o | Claude 3.5 Sonnet |
|---|---|---|---|---|
| MMLU (5-shot) | 88.4% | 85.2% | 88.7% | 88.7% |
| HumanEval | 86.7% | 78.3% | 90.2% | 92.0% |
| MATH (competition) | 78.5% | 71.2% | 76.6% | 71.1% |
| GPQA | 59.8% | 52.1% | 53.6% | 65.0% |
| ARC-Challenge | 96.2% | 94.8% | 96.3% | 96.7% |
| HellaSwag | 95.1% | 93.6% | 95.3% | 95.4% |
| IF Eval | 87.3% | 83.1% | 87.5% | 88.0% |
| Tool Use (BFCL) | 91.2% | 82.5% | 88.3% | 89.1% |

> Note: Benchmarks are approximate and reflect performance at launch. Results may vary based on prompting strategy and evaluation methodology.

## API Configuration

### Basic Request

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_XAI_API_KEY",
    base_url="https://api.x.ai/v1"
)

response = client.chat.completions.create(
    model="grok-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing in simple terms."}
    ],
    temperature=0.7,
    max_tokens=1024
)

print(response.choices[0].message.content)
```

### With Tool Use

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, e.g. 'San Francisco, CA'"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="grok-4",
    messages=[{"role": "user", "content": "What's the weather in Austin?"}],
    tools=tools,
    tool_choice="auto"
)
```

### Using cURL

```bash
curl https://api.x.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d '{
    "model": "grok-4",
    "messages": [
      {"role": "user", "content": "Summarize the latest research on fusion energy."}
    ],
    "max_tokens": 2048,
    "temperature": 0.5
  }'
```

### With System Prompt and Images

```python
response = client.chat.completions.create(
    model="grok-4",
    messages=[
        {"role": "system", "content": "You are a data analyst. Analyze charts and provide insights."},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What trends do you see in this chart?"},
                {
                    "type": "image_url",
                    "image_url": {"url": "https://example.com/chart.png"}
                }
            ]
        }
    ]
)
```

### Extended Thinking

```python
response = client.chat.completions.create(
    model="grok-4",
    messages=[
        {"role": "user", "content": "Solve this step by step: If a train travels 120 miles in 2 hours, then 180 miles in 3 hours, what is its average speed for the entire journey?"}
    ],
    reasoning_effort="high"
)
```

## Pricing

| Tier | Input | Output | Notes |
|---|---|---|---|
| Standard | $3.00/M tokens | $15.00/M tokens | Pay-as-you-go |
| Enterprise | Custom | Custom | Volume discounts, SLA |
| Free Tier | $0.00 | $0.00 | Limited requests/day |

**Cost Estimation Examples:**

| Task | Est. Input Tokens | Est. Output Tokens | Est. Cost |
|---|---|---|---|
| Short Q&A | 200 | 300 | $0.001 |
| Code generation (moderate) | 2,000 | 1,000 | $0.021 |
| Document analysis (10K words) | 15,000 | 2,000 | $0.075 |
| Large codebase refactoring | 100,000 | 10,000 | $0.450 |
| Full novel analysis (500K tokens) | 500,000 | 5,000 | $1.575 |

## Best Use Cases

1. **General-Purpose Assistant**: Default choice for chat, Q&A, and conversational AI applications.
2. **Code Generation & Review**: Strong performance on HumanEval and practical coding tasks. Ideal for IDE integrations, code review bots, and automated refactoring.
3. **Document Analysis**: 1M context window enables processing entire legal documents, research papers, or codebases in a single pass.
4. **Data Analysis**: Combine chart/image understanding with reasoning for business intelligence workflows.
5. **Multi-Step Reasoning**: Extended thinking mode handles complex math, logic, and planning tasks.
6. **Tool-Orchestrated Workflows**: Native tool use makes it excellent for agent architectures that need to call APIs, search the web, or interact with external systems.
7. **Content Generation**: Marketing copy, technical documentation, creative writing with controllable tone.

## Limitations and Considerations

- **Output Length**: Maximum 32,768 output tokens. For very long outputs, consider chunking or iterative generation.
- **Image Understanding**: Supports image input but cannot generate images. Use a dedicated image generation model for that.
- **Real-Time Data**: While Grok 4 can access web data via tools, the base model has a training cutoff. Always verify time-sensitive information.
- **Cost at Scale**: The $3/$15 pricing tier can add up for high-volume applications. Consider batch processing or caching strategies.
- **Rate Limits**: Standard tier has per-minute and per-day request limits. Enterprise tier offers higher throughput.
- **Hallucinations**: Like all LLMs, Grok 4 can produce plausible-sounding but incorrect information. Always validate critical outputs.
- **Structured Output**: JSON Schema mode is supported but may occasionally produce schema violations on complex nested structures.

## Migration Guide

### From Grok 3

```python
# Before (Grok 3)
response = client.chat.completions.create(
    model="grok-3",
    messages=[...]
)

# After (Grok 4) — just change the model name
response = client.chat.completions.create(
    model="grok-4",
    messages=[...]
)
```

**Key changes:**
- Model ID changes from `grok-3` to `grok-4`
- Context window increases from 128K to 1M tokens
- Tool use is now native (no beta flag needed)
- Extended thinking uses `reasoning_effort` parameter instead of separate endpoint

### From GPT-4o

```python
# Before (OpenAI)
client = OpenAI(api_key="sk-...")
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[...]
)

# After (Grok 4) — change base_url and model
client = OpenAI(
    api_key="YOUR_XAI_API_KEY",
    base_url="https://api.x.ai/v1"
)
response = client.chat.completions.create(
    model="grok-4",
    messages=[...]
)
```

### From Claude 3.5 Sonnet

```python
# Before (Anthropic)
import anthropic
client = anthropic.Anthropic(api_key="sk-ant-...")
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[...]
)

# After (Grok 4 via OpenAI-compatible API)
from openai import OpenAI
client = OpenAI(
    api_key="YOUR_XAI_API_KEY",
    base_url="https://api.x.ai/v1"
)
response = client.chat.completions.create(
    model="grok-4",
    messages=[...]
)
```

## Changelog

| Version | Date | Changes |
|---|---|---|
| 4.0.0 | 2025-07-01 | Initial release of Grok 4 |

## See Also

- [Grok 4 Fast](grok-4-fast.md) — Speed-optimized variant
- [Grok 4 Heavy](grok-4-heavy.md) — Maximum capability variant
- [Grok 4.1](grok-4-1.md) — Enhanced variant
- [API Reference](https://docs.x.ai/api)
