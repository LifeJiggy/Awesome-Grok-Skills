---
name: "Grok 4.3 Beta"
model_id: "grok-4-3-beta"
provider: "xAI"
context_window: 1000000
release_date: "2026-01-15"
pricing:
  input_per_million_tokens: 4.00
  output_per_million_tokens: 20.00
  currency: "USD"
  notes: "Beta pricing — subject to change at GA"
tags:
  - beta
  - experimental
  - next-generation
  - agentic
  - multi-turn-tool-use
  - advanced-reasoning
version: "4.3.0-beta"
status: "beta"
last_updated: "2026-01-15"
---

# Grok 4.3 Beta

## Overview

Grok 4.3 Beta is a pre-release preview of xAI's next-generation model, featuring advanced agentic capabilities, multi-turn tool orchestration, and improved reasoning over the Grok 4.1 family. As a beta release, it provides early access to features that will define the next stable generation.

**Important**: This is a beta model. API behavior, pricing, and features may change without notice before general availability. Do not use in production without evaluating stability requirements.

## Key Features

- **Agentic Tool Use**: Multi-step, autonomous tool chains with planning and self-correction.
- **Multi-Turn Tool Orchestration**: Maintain context across tool calls for complex workflows.
- **Improved Reasoning**: Better performance on tasks requiring sustained multi-step logic.
- **Parallel Tool Execution**: Native support for concurrent tool calls.
- **Self-Correction**: Can detect and fix its own errors in tool outputs.
- **Structured Reasoning Output**: Step-by-step reasoning traces alongside final answers.

## Technical Specifications

| Specification | Value |
|---|---|
| Model ID | `grok-4-3-beta` |
| Provider | xAI |
| Context Window | 1,000,000 tokens |
| Max Output Tokens | 65,536 tokens |
| Input Modalities | Text, Images, Documents |
| Output Modalities | Text |
| Training Cutoff | Late 2025 |
| Native Tool Use | Yes (agentic, multi-turn) |
| Parallel Tool Calls | Yes (native) |
| Structured Output | Yes (JSON Schema) |
| Streaming | Yes (SSE) |
| System Prompt | Supported |
| Temperature Range | 0.0 – 2.0 |
| Top-P Range | 0.0 – 1.0 |
| API Compatibility | OpenAI-compatible (beta) |
| Beta Status | Active — features may change |

## Benchmark Performance

> Note: Beta benchmarks are preliminary and may change before GA.

| Benchmark | Grok 4.3 Beta | Grok 4.1 | Grok 4 Heavy | Claude 3.5 Sonnet | GPT-4o |
|---|---|---|---|---|---|
| MMLU (5-shot) | 91.5% | 89.8% | 91.2% | 88.7% | 88.7% |
| HumanEval | 94.2% | 90.1% | 93.5% | 92.0% | 90.2% |
| MATH (competition) | 85.1% | 82.3% | 88.7% | 71.1% | 76.6% |
| GPQA (Diamond) | 68.7% | 64.2% | 72.3% | 65.0% | 53.6% |
| SWE-bench Verified | 55.8% | 45.3% | 52.1% | 49.0% | 33.2% |
| Tool Use (BFCL) | 95.3% | 93.2% | 94.8% | 89.1% | 88.3% |
| Agentic Tasks (SWE-bench Lite) | 48.2% | 38.1% | 42.5% | 40.3% | 28.7% |
| Multi-Turn Tool (custom) | 89.7% | 82.1% | 85.3% | 78.5% | 75.2% |
| Self-Correction Rate | 73.5% | N/A | N/A | N/A | N/A |

## API Configuration

### Beta Access

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_XAI_API_KEY",
    base_url="https://api.x.ai/v1"
)

# Note: Beta model — include beta flag if required
response = client.chat.completions.create(
    model="grok-4-3-beta",
    messages=[
        {"role": "user", "content": "Hello, this is a beta model test."}
    ]
)
```

### Agentic Tool Chain

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "num_results": {"type": "integer", "default": 5}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_terminal",
            "description": "Execute a terminal command",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string"},
                    "working_dir": {"type": "string"}
                },
                "required": ["command"]
            }
        }
    }
]

# Grok 4.3 Beta can plan and execute multi-step tool chains autonomously
response = client.chat.completions.create(
    model="grok-4-3-beta",
    messages=[{
        "role": "user",
        "content": """
        Clone the repository at https://github.com/example/app,
        analyze its architecture, identify security issues,
        fix the top 3 critical findings, and commit the changes.
        """
    }],
    tools=tools,
    tool_choice="auto"
)
```

### Parallel Tool Execution

```python
# Grok 4.3 Beta can issue multiple tool calls in parallel
# when tasks are independent
response = client.chat.completions.create(
    model="grok-4-3-beta",
    messages=[{
        "role": "user",
        "content": "Compare the README files in three repos: repo-a, repo-b, and repo-c"
    }],
    tools=tools,
    tool_choice="auto"
)

# The model may return multiple tool_calls in a single message:
# message.tool_calls = [
#     ToolCall(function="read_file", arguments={"path": "repo-a/README.md"}),
#     ToolCall(function="read_file", arguments={"path": "repo-b/README.md"}),
#     ToolCall(function="read_file", arguments={"path": "repo-c/README.md"})
# ]
```

### Structured Reasoning Output

```python
response = client.chat.completions.create(
    model="grok-4-3-beta",
    messages=[{
        "role": "user",
        "content": "Design a microservices architecture for a real-time collaborative document editor."
    }],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "architecture_design",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "reasoning_trace": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Step-by-step reasoning process"
                    },
                    "services": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "purpose": {"type": "string"},
                                "api_endpoints": {"type": "array", "items": {"type": "string"}},
                                "data_store": {"type": "string"}
                            },
                            "required": ["name", "purpose", "api_endpoints"]
                        }
                    },
                    "data_flow": {"type": "string"},
                    "trade_offs": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["reasoning_trace", "services", "data_flow", "trade_offs"]
            }
        }
    }
)
```

## Pricing

| Tier | Input | Output | Notes |
|---|---|---|---|
| Beta Access | $4.00/M tokens | $20.00/M tokens | Subject to change |
| Enterprise Beta | Custom | Custom | Early access program |
| Free Beta | Limited | Limited | Developer program |

**Cost Comparison:**

| Model | Input | Output | Status |
|---|---|---|---|
| Grok 4.3 Beta | $4.00 | $20.00 | Beta |
| Grok 4.1 | $3.50 | $17.50 | Stable |
| Grok 4 | $3.00 | $15.00 | Stable |
| Grok 4 Fast | $1.50 | $7.50 | Stable |

**Pricing Warning**: Beta pricing is introductory and may increase at GA. Budget accordingly.

## Best Use Cases

1. **AI Agents**: Autonomous multi-step task execution with planning and self-correction.
2. **Codebase Migration**: Clone, analyze, refactor, and test entire repositories.
3. **Complex Research**: Multi-source information gathering with synthesis and reporting.
4. **DevOps Automation**: Automated CI/CD pipeline setup, debugging, and optimization.
5. **Data Pipeline Orchestration**: Multi-step ETL with error handling and recovery.
6. **Prototyping**: Rapid prototyping of complex systems with tool-assisted development.

## Limitations and Considerations

- **Beta Instability**: API behavior may change without notice. Not recommended for production.
- **Higher Cost**: Premium beta pricing above stable models.
- **Rate Limits**: Beta access may have lower rate limits than stable models.
- **No SLA**: Beta models do not come with uptime guarantees.
- **Feature Changes**: Multi-turn tool use, parallel calls, and self-correction may change before GA.
- **Max Output**: 65,536 output tokens (increased from 32,768 in stable models).
- **Bug Reports**: Expect occasional failures, especially with complex tool chains. Report issues via the xAI developer portal.

## Migration Guide

### From Grok 4.1 (Experimental Upgrade)

```python
# Before (stable)
response = client.chat.completions.create(
    model="grok-4-1",
    messages=[...],
    tools=tools
)

# After (beta — for agentic workflows)
response = client.chat.completions.create(
    model="grok-4-3-beta",
    messages=[...],
    tools=tools
)
```

**When to try Grok 4.3 Beta:**
- You need autonomous multi-step tool execution
- Parallel tool calls would improve your workflow
- Self-correction would reduce error handling code
- You're building AI agent architectures

**When to stay on Grok 4.1:**
- Production stability is required
- Your current tool use patterns work well
- Cost predictability is important

### Beta to GA Migration Plan

When Grok 4.3 reaches general availability:

1. **Test Stability**: Run your beta workloads against the GA model
2. **Compare Pricing**: GA pricing may differ from beta
3. **Update Model ID**: May change from `grok-4-3-beta` to `grok-4-3`
4. **Remove Beta Flags**: Remove any beta-specific headers or flags
5. **Monitor**: Watch for behavior changes in edge cases

## Changelog

| Version | Date | Changes |
|---|---|---|
| 4.3.0-beta | 2026-01-15 | Initial beta release |

## See Also

- [Grok 4.1](grok-4-1.md) — Current stable flagship
- [Grok 4.20 Beta](grok-4-20-beta.md) — Experimental variant
- [Grok 4 Heavy](grok-4-heavy.md) — Maximum capability stable model
