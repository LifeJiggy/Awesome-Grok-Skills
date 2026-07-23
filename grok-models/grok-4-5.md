---
name: Grok 4.5
category: foundation-model
version: "4.5"
tags:
  - grok
  - xai
  - foundation
  - multimodal
  - reasoning
  - next-generation
  - agentic
description: Grok 4.5 — next-generation foundation model from xAI with advanced reasoning, multimodal understanding, and agentic capabilities.
---

# Grok 4.5

## Overview

Grok 4.5 represents the next evolution in xAI's foundation model family, pushing the boundaries of what large language models can achieve across reasoning, multimodal understanding, code generation, and agentic workflows. Building on the strengths of Grok 3 and its predecessors, Grok 4.5 introduces architectural innovations that deliver substantial improvements in complex reasoning, long-context understanding, and real-world task execution.

Grok 4.5 is designed as a general-purpose model that excels across the full spectrum of AI tasks — from creative writing and analysis to technical problem-solving and autonomous multi-step workflows. It maintains the distinctive "Grok personality" — direct, witty, and unafraid to challenge assumptions — while delivering enterprise-grade reliability.

## Technical Specifications

### Architecture Overview

| Attribute | Detail |
|---|---|
| **Model Family** | Grok (xAI) |
| **Version** | 4.5 |
| **Architecture** | Advanced transformer with mixture-of-experts |
| **Context Window** | 256K tokens (standard), 1M tokens (extended) |
| **Max Output** | 32,768 tokens |
| **Training Data Cutoff** | Early 2026 |
| **Modalities** | Text, Vision, Audio (input); Text (output) |
| **Knowledge Base** | Real-time access to X/Twitter, web search |
| **Reasoning** | Extended chain-of-thought with structured output |

### Capability Matrix

| Capability | Rating | Notes |
|---|---|---|
| **General Reasoning** | Exceptional | Multi-step logical chains, causal inference |
| **Mathematical Reasoning** | Exceptional | Formal proofs, symbolic manipulation |
| **Code Generation** | Exceptional | Full-stack, multi-file, architecture design |
| **Creative Writing** | Excellent | Style adaptation, long-form narrative |
| **Analysis & Synthesis** | Exceptional | Complex document analysis, data interpretation |
| **Vision Understanding** | Excellent | Charts, diagrams, documents, photographs |
| **Multilingual** | Excellent | 50+ languages with strong translation |
| **Agentic Workflows** | Exceptional | Tool use, planning, self-correction |
| **Real-time Knowledge** | Excellent | X/Twitter integration, web access |
| **Instruction Following** | Exceptional | Complex multi-constraint adherence |

### Benchmark Performance

```
Benchmark                Grok 4.5    Grok 3    GPT-4o    Claude 3.5
──────────────────────────────────────────────────────────────────────
MMLU (5-shot)            94.2%       89.7%     88.7%     88.7%
GPQA (Diamond)           72.8%       61.3%     56.1%     65.0%
HumanEval (pass@1)       96.4%       91.2%     90.2%     92.0%
MATH (competition)       91.3%       78.5%     76.6%     78.3%
MGSM (multilingual)      93.1%       86.2%     90.5%     91.6%
IFEval (instructions)    92.7%       85.4%     87.5%     89.3%
SWE-bench (verified)     72.5%       49.6%     38.4%     49.0%
TAU-bench (agentic)      78.3%       58.2%     55.0%     63.5%
LongContext (Needle)     99.8%       97.2%     98.5%     99.1%
```

## Model Variants

### Grok 4.5 (Standard)

The default variant balancing capability and speed. Suitable for most production workloads.

```
Context: 256K tokens
Latency: ~200ms first token
Throughput: ~60-80 tok/s
Best for: General-purpose applications, chat, analysis
```

### Grok 4.5 Fast

Optimized for latency-critical applications with slightly reduced capability ceiling.

```
Context: 128K tokens
Latency: ~100ms first token
Throughput: ~100-150 tok/s
Best for: Real-time chat, IDE integration, streaming
```

### Grok 4.5 Thinking

Extended reasoning mode that performs visible chain-of-thought before answering.

```
Context: 256K tokens
Latency: ~5-30s (thinking time varies)
Output: Reasoning trace + final answer
Best for: Complex analysis, mathematical proofs, strategic planning
```

## Configuration

### API Setup

```javascript
// Node.js / TypeScript
import Grok from 'grok-sdk';

const client = new Grok({
  apiKey: process.env.XAI_API_KEY,
  baseUrl: 'https://api.x.ai/v1',
});

// Standard completion
const response = await client.chat.completions.create({
  model: 'grok-4-5',
  messages: [
    { role: 'system', content: 'You are a helpful assistant with access to real-time information.' },
    { role: 'user', content: 'What are the latest developments in quantum computing?' }
  ],
  temperature: 0.7,
  max_tokens: 4096,
});

// With extended thinking
const thinkingResponse = await client.chat.completions.create({
  model: 'grok-4-5-thinking',
  messages: [
    { role: 'system', content: 'Think step by step before answering.' },
    { role: 'user', content: 'Prove that the square root of 2 is irrational.' }
  ],
  temperature: 0.3,
  max_tokens: 8192,
});
```

```python
# Python
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["XAI_API_KEY"],
    base_url="https://api.x.ai/v1",
)

# Standard usage
response = client.chat.completions.create(
    model="grok-4-5",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum entanglement in simple terms."}
    ],
    temperature=0.7,
    max_tokens=4096,
)

# Structured output
import json

response = client.chat.completions.create(
    model="grok-4-5",
    messages=[
        {"role": "system", "content": "Output analysis as JSON with keys: summary, key_points, confidence, recommendations."},
        {"role": "user", "content": f"Analyze this data:\n{data_json}"}
    ],
    response_format={"type": "json_object"},
    temperature=0.2,
)
analysis = json.loads(response.choices[0].message.content)
```

### Environment Configuration

```bash
# Required
export XAI_API_KEY="xai-your-api-key-here"

# Optional: override defaults
export GROK_MODEL="grok-4-5"
export GROK_BASE_URL="https://api.x.ai/v1"
export GROK_MAX_TOKENS="4096"
export GROK_TEMPERATURE="0.7"

# Enterprise: custom endpoint
export GROK_BASE_URL="https://your-enterprise-endpoint.x.ai/v1"
```

## Usage Patterns

### Pattern 1: Advanced Reasoning with Structured Output

```python
def advanced_analysis(data: dict, question: str) -> dict:
    """Perform complex analysis with structured reasoning."""
    response = client.chat.completions.create(
        model="grok-4-5-thinking",
        messages=[
            {"role": "system", "content": """You are an expert analyst.
            Think step by step.
            Structure your response as JSON:
            {
                "reasoning": ["step 1", "step 2", ...],
                "conclusion": "final answer",
                "confidence": 0.0-1.0,
                "alternatives": ["alternative 1", ...],
                "caveats": ["caveat 1", ...]
            }"""},
            {"role": "user", "content": f"Data: {json.dumps(data)}\n\nQuestion: {question}"}
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
        max_tokens=8192,
    )
    return json.loads(response.choices[0].message.content)
```

### Pattern 2: Multi-Modal Document Analysis

```python
import base64

def analyze_document(image_path: str, question: str) -> str:
    """Analyze an image or document using vision capabilities."""
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="grok-4-5",
        messages=[
            {"role": "system", "content": "Analyze documents, charts, and images with precision. Reference specific elements by location."},
            {"role": "user", "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
            ]}
        ],
        temperature=0.2,
        max_tokens=4096,
    )
    return response.choices[0].message.content
```

### Pattern 3: Agentic Workflow

```python
import json
from typing import Callable

class GrokAgent:
    """Agentic workflow using Grok 4.5 with tool use."""

    def __init__(self, tools: dict[str, Callable]):
        self.tools = tools
        self.conversation = []

    def system_prompt(self) -> str:
        tool_descriptions = "\n".join([
            f"- {name}: {fn.__doc__ or 'No description'}"
            for name, fn in self.tools.items()
        ])
        return f"""You are an autonomous agent with access to these tools:
{tool_descriptions}

To use a tool, respond with a JSON block:
```tool_call
{{"tool": "<tool_name>", "args": {{...}}}}
```

Think step by step. Use tools when needed. When you have the final answer, state it clearly."""

    def run(self, task: str, max_steps: int = 10) -> str:
        """Execute a task through multi-step reasoning and tool use."""
        self.conversation = [
            {"role": "system", "content": self.system_prompt()},
            {"role": "user", "content": task}
        ]

        for step in range(max_steps):
            response = client.chat.completions.create(
                model="grok-4-5",
                messages=self.conversation,
                temperature=0.3,
                max_tokens=2048,
            )

            assistant_msg = response.choices[0].message.content
            self.conversation.append({"role": "assistant", "content": assistant_msg})

            # Check for tool calls
            tool_call = extract_tool_call(assistant_msg)
            if tool_call is None:
                return assistant_msg  # Final answer

            # Execute tool
            tool_name = tool_call["tool"]
            tool_args = tool_call["args"]

            if tool_name not in self.tools:
                result = f"Error: Unknown tool '{tool_name}'"
            else:
                try:
                    result = str(self.tools[tool_name](**tool_args))
                except Exception as e:
                    result = f"Error: {e}"

            self.conversation.append({
                "role": "user",
                "content": f"Tool result for {tool_name}:\n{result}"
            })

        return "Maximum steps reached without final answer."
```

### Pattern 4: Long-Context Analysis

```python
def analyze_long_document(document: str, questions: list[str]) -> list[dict]:
    """Analyze a very long document against multiple questions."""
    # Grok 4.5 supports 256K+ context, so we can process large documents
    results = []

    # Batch questions for efficiency
    batched_prompt = f"""Analyze the following document and answer each question.

Document:
{document}

Questions:
{chr(10).join(f'{i+1}. {q}' for i, q in enumerate(questions))}

Provide answers as JSON array: [{{"question": "...", "answer": "...", "confidence": 0.0-1.0, "page_references": [...]}}]"""

    response = client.chat.completions.create(
        model="grok-4-5",
        messages=[
            {"role": "system", "content": "Analyze the full document carefully. Reference specific sections in your answers."},
            {"role": "user", "content": batched_prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
        max_tokens=8192,
    )

    return json.loads(response.choices[0].message.content)
```

### Pattern 5: Real-Time Knowledge Integration

```python
def get_current_analysis(topic: str) -> str:
    """Leverage Grok 4.5's real-time knowledge for current events analysis."""
    response = client.chat.completions.create(
        model="grok-4-5",
        messages=[
            {"role": "system", "content": """You have access to real-time information from X/Twitter and the web.
            Use this to provide current, up-to-date analysis.
            Cite specific sources when possible.
            Distinguish between confirmed information and speculation."""},
            {"role": "user", "content": f"Provide a current analysis of: {topic}"}
        ],
        temperature=0.5,
        max_tokens=4096,
    )
    return response.choices[0].message.content
```

## Advanced Configuration

### System Prompt Architecture

```python
# Tiered system prompt for complex applications
SYSTEM_PROMPT = """
## Identity
You are [ROLE], an expert in [DOMAIN] with [EXPERIENCE].

## Capabilities
- Access to real-time information via X/Twitter and web search
- Vision understanding for image analysis
- Extended reasoning for complex problems
- Tool use for autonomous workflows

## Behavioral Rules
1. Always verify facts before stating them
2. When uncertain, express confidence level
3. Reference specific sources when citing information
4. If asked about recent events, use real-time knowledge
5. For complex analysis, show your reasoning step by step

## Output Format
[Specific format requirements for the application]

## Safety Guidelines
[Application-specific safety constraints]
"""
```

### Response Format Control

```python
# JSON mode for structured output
response = client.chat.completions.create(
    model="grok-4-5",
    messages=[...],
    response_format={"type": "json_object"},
)

# Streaming for real-time display
async def stream_response(messages):
    stream = await client.chat.completions.create(
        model="grok-4-5",
        messages=messages,
        stream=True,
    )
    async for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# Function calling / tool use
response = client.chat.completions.create(
    model="grok-4-5",
    messages=[...],
    tools=[
        {
            "type": "function",
            "function": {
                "name": "search_web",
                "description": "Search the web for current information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"}
                    },
                    "required": ["query"]
                }
            }
        }
    ],
    tool_choice="auto",
)
```

## Cost Optimization

### Token Usage Breakdown

| Operation | Cost Factor | Optimization |
|---|---|---|
| Input tokens | Proportional to context length | Trim context aggressively |
| Output tokens | Proportional to response length | Use max_tokens limits |
| Thinking tokens | Separate from output | Use thinking mode sparingly |
| Image tokens | ~85 tokens per tile | Resize images before sending |

### Cost-Reduction Strategies

```python
# 1. Cache system prompts (they're reusable)
CACHED_SYSTEM_PROMPT = "You are a helpful assistant."  # Reuse across calls

# 2. Use appropriate model variant
# Fast for simple queries, Standard for complex, Thinking for reasoning
def select_model(query_complexity: str) -> str:
    if query_complexity == "simple":
        return "grok-4-5-fast"
    elif query_complexity == "complex":
        return "grok-4-5-thinking"
    return "grok-4-5"

# 3. Compress long contexts
def summarize_context(full_text: str) -> str:
    """Use the model to summarize before analysis."""
    response = client.chat.completions.create(
        model="grok-4-5-fast",
        messages=[
            {"role": "system", "content": "Summarize the following text in 500 words, preserving all key facts and numbers."},
            {"role": "user", "content": full_text}
        ],
        max_tokens=1024,
    )
    return response.choices[0].message.content

# 4. Batch related queries
def batch_queries(queries: list[str]) -> str:
    """Combine multiple questions into a single API call."""
    combined = "\n".join(f"Q{i+1}: {q}" for i, q in enumerate(queries))
    prompt = f"""Answer each question concisely:
{combined}

Format each answer on a separate line starting with the question number."""
    # ...
```

## Common Pitfalls and Solutions

### Pitfall 1: Over-Reliance on Default Settings

**Problem**: Using default temperature (1.0) for factual tasks produces unreliable results.

**Solution**: Match temperature to task:
- Factual/analytical: 0.0 - 0.3
- Balanced: 0.5 - 0.7
- Creative: 0.7 - 1.0

### Pitfall 2: Ignoring the Thinking Model

**Problem**: Using the standard model for complex reasoning when the thinking variant would produce better results.

**Solution**: Route complex reasoning tasks to `grok-4-5-thinking`:
- Mathematical proofs
- Multi-step logical analysis
- Strategic planning
- Debugging complex systems

### Pitfall 3: Context Window Mismanagement

**Problem**: Sending too much context wastes tokens; too little loses important information.

**Solution**: Implement context management:
```python
def manage_context(messages: list, max_tokens: int = 200000) -> list:
    """Manage context window by summarizing older messages."""
    total_tokens = estimate_tokens(messages)
    if total_tokens > max_tokens:
        # Summarize older messages
        older = messages[1:-3]
        summary = summarize_messages(older)
        return [messages[0], {"role": "user", "content": f"Context summary:\n{summary}"}] + messages[-3:]
    return messages
```

### Pitfall 4: Not Leveraging Real-Time Knowledge

**Problem**: Asking about current events without prompting the model to use its real-time capabilities.

**Solution**: Explicitly request current information:
```python
# Instead of:
"What is the stock price of Tesla?"

# Use:
"What is the current stock price of Tesla? Please use your real-time knowledge and cite sources."
```

### Pitfall 5: Hallucination in Long Responses

**Problem**: Longer responses may include fabricated details.

**Solution**: 
- Request citations and verify them
- Use structured output to constrain responses
- Break complex questions into smaller parts
- Use `response_format` for JSON output to enforce structure

## Integration Patterns

### Multi-Agent System

```python
class MultiAgentOrchestrator:
    """Orchestrate multiple specialized Grok 4.5 agents."""

    def __init__(self):
        self.agents = {
            "researcher": Agent(role="Research specialist", model="grok-4-5"),
            "analyst": Agent(role="Data analyst", model="grok-4-5-thinking"),
            "writer": Agent(role="Technical writer", model="grok-4-5"),
            "reviewer": Agent(role="Quality reviewer", model="grok-4-5-thinking"),
        }

    async def execute_pipeline(self, task: str) -> str:
        """Execute a multi-agent pipeline."""
        # Phase 1: Research
        research = await self.agents["researcher"].run(
            f"Research the following topic thoroughly: {task}"
        )

        # Phase 2: Analysis
        analysis = await self.agents["analyst"].run(
            f"Analyze this research and identify key insights:\n{research}"
        )

        # Phase 3: Writing
        draft = await self.agents["writer"].run(
            f"Write a comprehensive report based on this analysis:\n{analysis}"
        )

        # Phase 4: Review
        review = await self.agents["reviewer"].run(
            f"Review this report for accuracy, completeness, and clarity:\n{draft}"
        )

        # Phase 5: Final revision
        final = await self.agents["writer"].run(
            f"Revise this report incorporating the review feedback:\n\nOriginal:\n{draft}\n\nReview:\n{review}"
        )

        return final
```

### Streaming Chat Application

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/chat")
async def chat(messages: list[dict]):
    """Streaming chat endpoint."""
    async def generate():
        stream = await client.chat.completions.create(
            model="grok-4-5",
            messages=messages,
            stream=True,
            temperature=0.7,
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

## Rate Limits and Quotas

| Tier | RPM | TPM | Daily Limit |
|---|---|---|---|
| Free | 5 | 25,000 | 250,000 |
| Standard | 60 | 500,000 | 10,000,000 |
| Premium | 300 | 2,000,000 | 100,000,000 |
| Enterprise | Custom | Custom | Custom |

## Security Considerations

1. **Prompt injection**: Validate and sanitize user inputs before passing to the model.
2. **Data privacy**: Be aware that API calls may be subject to data retention policies.
3. **Output validation**: Always validate generated code and structured output before use.
4. **Rate limiting**: Implement client-side rate limiting to avoid hitting API limits.
5. **Secrets management**: Never include API keys or secrets in prompts.

## Related Documentation

- [Grok Code Fast 1](./grok-code-fast-1.md) — Code-specialized variant
- [Vision Capabilities](./grok-vision.md) — Multimodal reference
- [Best Practices](./grok-best-practices.md) — Optimization guide
- [Build Configuration](./grok-build.md) — Deployment guide
