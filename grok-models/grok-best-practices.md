---
name: Grok Best Practices
category: reference
version: "1.0"
tags:
  - grok
  - xai
  - best-practices
  - prompt-engineering
  - optimization
  - performance
  - cost
  - context-management
description: Best practices for using Grok models — prompt engineering, context management, cost optimization, performance tuning, and production patterns.
---

# Grok Best Practices

## Overview

This guide distills actionable best practices for working with Grok models across all use cases. Whether you're building a simple chatbot, an enterprise AI platform, or a specialized code tool, these patterns will help you get the most out of Grok's capabilities while minimizing costs and maximizing reliability.

## Prompt Engineering

### System Prompt Design

The system prompt is your most powerful tool for controlling model behavior. Invest time in crafting it well.

```python
# Structure of an effective system prompt
SYSTEM_PROMPT = """
## Role Definition
You are [SPECIFIC ROLE] with expertise in [DOMAIN].

## Capabilities
- [Capability 1]
- [Capability 2]

## Behavioral Rules
1. [Rule 1 — be specific and actionable]
2. [Rule 2]
3. [Rule 3]

## Output Format
[Exact format requirements]

## Constraints
- [What NOT to do]
- [Edge cases]
- [Safety guidelines]
"""
```

**Key principles:**

1. **Be specific about the role**: "You are a senior Python developer specializing in data engineering" is better than "You are a helpful assistant."
2. **State rules positively**: "Always include type hints" is better than "Don't forget type hints."
3. **Show, don't tell**: Include examples of desired output format.
4. **Prioritize rules**: Put the most important rules first — the model pays more attention to early instructions.

### User Prompt Patterns

#### The RACE Framework

Structure complex prompts using RACE:

```
R — Role context (who is asking and why)
A — Action (what specifically to do)
C — Constraints (rules and limitations)
E — Examples (sample input/output)
```

```python
# Using RACE
prompt = """
[Role] I'm a senior engineer reviewing a pull request for a production API.

[Action] Review this code diff and identify:
- Security vulnerabilities
- Performance issues
- Code style violations
- Potential bugs

[Constraints]
- Focus on high-severity issues only
- Be specific about line numbers
- No style nitpicks unless they cause bugs
- Output as JSON array of issues

[Example]
Input: `def get_user(id): return db.query(f"SELECT * FROM users WHERE id={id}")`
Output: [{"severity": "critical", "type": "sql_injection", "line": 1, "description": "String interpolation in SQL query allows injection attack. Use parameterized query."}]
"""
```

#### Chain-of-Thought Prompting

For complex reasoning tasks, explicitly request step-by-step thinking:

```python
prompt = """
Analyze this system architecture for potential failure points.

Think through this systematically:
1. Identify each component
2. Map dependencies between components
3. For each component, identify failure modes
4. Assess impact and likelihood
5. Recommend mitigations

Show your reasoning at each step.
"""
```

#### Few-Shot Examples

When you need consistent output format or behavior, include examples:

```python
prompt = """
Classify each customer message as: complaint, question, praise, or request.

Examples:
Message: "Your product broke after one day!" → complaint
Message: "How do I reset my password?" → question
Message: "Amazing service, thank you!" → praise
Message: "Can you expedite my order?" → request

Now classify:
Message: "{customer_message}" →
"""
```

### Prompt Templates

Create reusable prompt templates with variable slots:

```python
class PromptTemplates:
    CODE_REVIEW = """Review this {language} code for:
    - Bugs and logic errors
    - Security vulnerabilities
    - Performance issues
    - Maintainability concerns
    
    Code:
    ```{language}
    {code}
    ```
    
    Output as JSON array with keys: severity, type, line, description, suggestion
    """

    DATA_EXTRACTION = """Extract {data_type} information from this text:
    
    {text}
    
    Output as JSON with these fields: {fields}
    """

    ANALYSIS = """Analyze the following {topic}:
    
    {content}
    
    Provide:
    1. Key findings
    2. Implications
    3. Recommendations
    
    Be specific and actionable.
    """

    @classmethod
    def format(cls, template_name: str, **kwargs) -> str:
        template = getattr(cls, template_name)
        return template.format(**kwargs)
```

## Context Management

### Context Window Optimization

Grok models have large context windows, but bigger isn't always better. Optimize what you send:

```python
# BAD: Dumping entire files
def bad_prompt(file_content: str, question: str) -> str:
    return f"Here is the entire file:\n{file_content}\n\nQuestion: {question}"

# GOOD: Focused, relevant context
def good_prompt(relevant_code: str, question: str) -> str:
    return f"""Relevant code section:
```python
{relevant_code}
```

Question: {question}

Provide a concise answer referencing specific line numbers."""
```

### Conversation Management

```python
class ConversationManager:
    """Manage conversation context efficiently."""

    def __init__(self, max_tokens: int = 200000):
        self.messages = []
        self.max_tokens = max_tokens

    def add_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})
        self._prune_if_needed()

    def _estimate_tokens(self) -> int:
        """Rough token estimate (4 chars per token average)."""
        return sum(len(m["content"]) // 4 for m in self.messages)

    def _prune_if_needed(self) -> None:
        """Compress older messages when approaching context limit."""
        if self._estimate_tokens() > self.max_tokens * 0.8:
            # Keep system prompt + last 4 messages
            if len(self.messages) > 5:
                old_messages = self.messages[1:-4]
                recent = self.messages[-4:]
                summary = self._summarize(old_messages)
                self.messages = [self.messages[0]] + [
                    {"role": "system", "content": f"Conversation context: {summary}"}
                ] + recent

    def _summarize(self, messages: list) -> str:
        """Summarize older messages."""
        combined = "\n".join(f"{m['role']}: {m['content'][:200]}" for m in messages)
        # Use the model itself to summarize
        response = client.chat.completions.create(
            model="grok-4-5-fast",
            messages=[
                {"role": "system", "content": "Summarize this conversation in 200 words, preserving key facts and decisions."},
                {"role": "user", "content": combined}
            ],
            max_tokens=512,
        )
        return response.choices[0].message.content
```

### Context Loading Patterns

```python
# Progressive context loading: start minimal, add as needed
class ProgressiveLoader:
    def __init__(self, base_context: str = ""):
        self.base_context = base_context
        self.loaded = {"base"}

    def load(self, layer: str, content: str) -> None:
        if layer not in self.loaded:
            self.base_context += f"\n\n## {layer}\n{content}"
            self.loaded.add(layer)

    def get_context(self, layers: list[str]) -> str:
        """Get context with specified layers loaded."""
        parts = [self.base_context]
        for layer in layers:
            if layer in self.loaded:
                parts.append(f"## {layer}\n{self.loaded[layer]}")
        return "\n\n".join(parts)

# Usage
loader = ProgressiveLoader(base_context="Project: MyApp")
loader.load("architecture", read_file("docs/architecture.md"))
loader.load("api_spec", read_file("docs/api.yaml"))
loader.load("recent_changes", get_recent_commits())

# Only load what's needed
if task_type == "api_work":
    context = loader.get_context(["architecture", "api_spec"])
elif task_type == "bug_fix":
    context = loader.get_context(["architecture", "recent_changes"])
```

## Cost Optimization

### Model Selection Strategy

Use the right model for the right task:

```python
def select_model(task: str, complexity: str, latency_requirement: str = "normal") -> str:
    """Select the optimal Grok model for a given task."""
    
    # Simple tasks → Fast model
    if complexity == "simple" or latency_requirement == "critical":
        if task == "code":
            return "grok-code-fast-1"
        return "grok-4-5-fast"
    
    # Complex reasoning → Thinking model
    if task == "reasoning" or complexity == "complex":
        return "grok-4-5-thinking"
    
    # Code tasks → Code-specialized
    if task == "code":
        return "grok-code-fast-1"
    
    # Default
    return "grok-4-5"
```

### Token Usage Tracking

```python
from dataclasses import dataclass, field
from datetime import datetime, timedelta

@dataclass
class TokenUsage:
    total_input: int = 0
    total_output: int = 0
    total_cost: float = 0.0
    by_model: dict = field(default_factory=dict)

    COST_PER_1K = {
        "grok-4-5": {"input": 0.005, "output": 0.015},
        "grok-4-5-fast": {"input": 0.002, "output": 0.008},
        "grok-4-5-thinking": {"input": 0.01, "output": 0.03},
        "grok-code-fast-1": {"input": 0.003, "output": 0.01},
    }

    def record(self, model: str, input_tokens: int, output_tokens: int):
        self.total_input += input_tokens
        self.total_output += output_tokens

        costs = self.COST_PER_1K.get(model, {"input": 0.01, "output": 0.03})
        cost = (input_tokens / 1000 * costs["input"]) + (output_tokens / 1000 * costs["output"])
        self.total_cost += cost

        if model not in self.by_model:
            self.by_model[model] = {"input": 0, "output": 0, "cost": 0.0}
        self.by_model[model]["input"] += input_tokens
        self.by_model[model]["output"] += output_tokens
        self.by_model[model]["cost"] += cost

    def report(self) -> str:
        lines = [
            f"Token Usage Report",
            f"{'='*40}",
            f"Total Input:  {self.total_input:,} tokens",
            f"Total Output: {self.total_output:,} tokens",
            f"Total Cost:   ${self.total_cost:.4f}",
            f"",
            f"By Model:"
        ]
        for model, stats in self.by_model.items():
            lines.append(f"  {model}: {stats['input']:,} in / {stats['output']:,} out / ${stats['cost']:.4f}")
        return "\n".join(lines)
```

### Cost Reduction Strategies

```python
# Strategy 1: Cache identical requests
from functools import lru_cache

@lru_cache(maxsize=500)
def cached_completion(prompt_hash: str, model: str, temperature: float) -> str:
    """Cache completions for repeated identical prompts."""
    # This function body is only called on cache miss
    ...

# Strategy 2: Compress before analyzing
def analyze_with_compression(long_text: str, question: str) -> str:
    """Summarize long text before asking questions about it."""
    # Step 1: Compress (cheaper model)
    summary = client.chat.completions.create(
        model="grok-4-5-fast",
        messages=[
            {"role": "system", "content": "Summarize in 500 words, preserving key data and facts."},
            {"role": "user", "content": long_text}
        ],
        max_tokens=1024,
    ).choices[0].message.content

    # Step 2: Analyze summary (standard model)
    return client.chat.completions.create(
        model="grok-4-5",
        messages=[
            {"role": "user", "content": f"Based on this summary:\n{summary}\n\nQuestion: {question}"}
        ],
        max_tokens=2048,
    ).choices[0].message.content

# Strategy 3: Batch related questions
def batch_questions(questions: list[str], context: str) -> list[str]:
    """Combine multiple questions into one API call."""
    combined = "\n".join(f"Q{i+1}: {q}" for i, q in enumerate(questions))
    prompt = f"""Context:\n{context}\n\nAnswer each question concisely:\n{combined}"""

    response = client.chat.completions.create(
        model="grok-4-5",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
    )

    # Parse individual answers
    return parse_numbered_answers(response.choices[0].message.content)

# Strategy 4: Use structured output to reduce retries
def get_structured_response(prompt: str, schema: dict) -> dict:
    """Use JSON mode to get parseable output on first try."""
    response = client.chat.completions.create(
        model="grok-4-5",
        messages=[
            {"role": "system", "content": f"Output valid JSON matching this schema:\n{json.dumps(schema)}"},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    return json.loads(response.choices[0].message.content)
```

## Performance Tuning

### Latency Optimization

```python
# 1. Use streaming for perceived performance
async def streaming_chat(messages):
    stream = await client.chat.completions.create(
        model="grok-4-5",
        messages=messages,
        stream=True,
    )
    async for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# 2. Parallel independent requests
async def parallel_analysis(items: list) -> list:
    tasks = [analyze_single(item) for item in items]
    return await asyncio.gather(*tasks)

# 3. Use the Fast variant when possible
FAST_MODEL_TASKS = {
    "quick_qa",
    "summarization",
    "classification",
    "simple_extraction",
    "translation",
    "code_completion",
}

def select_for_speed(task_type: str) -> str:
    return "grok-4-5-fast" if task_type in FAST_MODEL_TASKS else "grok-4-5"
```

### Throughput Optimization

```python
# Connection pooling
import httpx

transport = httpx.AsyncHTTPTransport(
    limits=httpx.Limits(
        max_connections=20,
        max_keepalive_connections=10,
        keepalive_expiry=30,
    )
)

client = AsyncOpenAI(
    api_key=os.environ["XAI_API_KEY"],
    base_url="https://api.x.ai/v1",
    http_client=httpx.AsyncClient(transport=transport),
)

# Request queuing with rate limiting
import asyncio
from collections import deque

class RequestQueue:
    def __init__(self, max_per_second: int = 10):
        self.max_per_second = max_per_second
        self.queue = deque()
        self.semaphore = asyncio.Semaphore(max_per_second)

    async def process(self, request_fn):
        async with self.semaphore:
            result = await request_fn()
            await asyncio.sleep(1.0 / self.max_per_second)
            return result
```

### Error Handling and Retry Logic

```python
import asyncio
from typing import TypeVar, Callable

T = TypeVar("T")

async def with_retry(
    fn: Callable[..., T],
    max_retries: int = 3,
    base_delay: float = 1.0,
    backoff_factor: float = 2.0,
    retryable_errors: tuple = (429, 500, 502, 503),
) -> T:
    """Execute with exponential backoff retry."""
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            return await fn()
        except Exception as e:
            last_error = e
            status = getattr(e, 'status', None)

            if status not in retryable_errors:
                raise  # Non-retryable error

            if attempt < max_retries:
                delay = base_delay * (backoff_factor ** attempt)
                # Respect Retry-After header for 429
                if status == 429:
                    retry_after = getattr(e, 'headers', {}).get('Retry-After')
                    if retry_after:
                        delay = max(delay, float(retry_after))

                await asyncio.sleep(delay)

    raise last_error
```

## Production Patterns

### Logging and Observability

```python
import logging
import time
from contextlib import contextmanager

logger = logging.getLogger("grok")

@contextmanager
def log_grok_request(operation: str, model: str, **kwargs):
    """Log Grok API requests with timing and metadata."""
    start = time.time()
    request_id = f"grok-{int(start * 1000)}"

    logger.info(f"[{request_id}] Starting {operation} with {model}", extra={
        "request_id": request_id,
        "operation": operation,
        "model": model,
        **kwargs,
    })

    try:
        yield request_id
        elapsed = time.time() - start
        logger.info(f"[{request_id}] Completed in {elapsed:.2f}s")
    except Exception as e:
        elapsed = time.time() - start
        logger.error(f"[{request_id}] Failed after {elapsed:.2f}s: {e}")
        raise
```

### Graceful Degradation

```python
async def robust_completion(messages: list, task: str) -> str:
    """Attempt completion with fallback strategies."""
    strategies = [
        # Strategy 1: Full model
        {"model": "grok-4-5", "max_tokens": 4096, "temperature": 0.7},
        # Strategy 2: Reduced context
        {"model": "grok-4-5", "max_tokens": 2048, "temperature": 0.5},
        # Strategy 3: Fast model
        {"model": "grok-4-5-fast", "max_tokens": 1024, "temperature": 0.3},
        # Strategy 4: Minimal fallback
        {"model": "grok-4-5-fast", "max_tokens": 512, "temperature": 0.1},
    ]

    last_error = None
    for strategy in strategies:
        try:
            response = await client.chat.completions.create(
                messages=messages,
                **strategy,
            )
            return response.choices[0].message.content
        except Exception as e:
            last_error = e
            logger.warning(f"Strategy failed: {strategy['model']} - {e}")
            continue

    raise RuntimeError(f"All strategies failed. Last error: {last_error}")
```

### Testing Grok Integrations

```python
import pytest
from unittest.mock import AsyncMock, patch

# Mock the Grok client for tests
@pytest.fixture
def mock_grok():
    with patch('openai.OpenAI') as mock:
        client = mock.return_value
        client.chat.completions.create = AsyncMock()
        yield client

# Test prompt construction
def test_prompt_construction():
    prompt = build_review_prompt(code="print('hello')", language="python")
    assert "python" in prompt.lower()
    assert "print('hello')" in prompt
    assert "review" in prompt.lower()

# Test error handling
@pytest.mark.asyncio
async def test_retry_on_rate_limit(mock_grok):
    mock_grok.chat.completions.create.side_effect = [
        Exception(status=429),
        Exception(status=429),
        AsyncMock(choices=[AsyncMock(message=AsyncMock(content="Success"))]),
    ]

    result = await with_retry(lambda: mock_grok.chat.completions.create(), max_retries=3)
    assert result.choices[0].message.content == "Success"

# Test context management
def test_context_pruning():
    manager = ConversationManager(max_tokens=1000)
    for i in range(100):
        manager.add_message("user", f"Message {i} " * 100)
    assert manager._estimate_tokens() < 1000
```

## Common Pitfalls and Solutions

### Pitfall 1: Not Using System Prompts

**Problem**: Leaving behavior to chance with user messages only.

**Solution**: Always set a system prompt, even for simple use cases:

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant. Be concise and accurate."},
    {"role": "user", "content": question}
]
```

### Pitfall 2: Ignoring Temperature

**Problem**: Using default temperature (1.0) for factual tasks.

**Solution**: Match temperature to task requirements:

| Task | Temperature | Why |
|---|---|---|
| Code generation | 0.0 - 0.2 | Deterministic, reproducible |
| Data extraction | 0.0 - 0.1 | Exact accuracy needed |
| Factual Q&A | 0.1 - 0.3 | Minimize hallucination |
| Creative writing | 0.7 - 1.0 | Maximize variety |
| Brainstorming | 0.8 - 1.0 | Generate diverse ideas |

### Pitfall 3: Not Validating Output

**Problem**: Trusting model output without validation, especially for structured data.

**Solution**: Always validate structured output:

```python
from pydantic import BaseModel, ValidationError

class ExtractionResult(BaseModel):
    name: str
    email: str
    confidence: float

def extract_with_validation(text: str) -> ExtractionResult:
    response = client.chat.completions.create(
        model="grok-4-5",
        messages=[
            {"role": "system", "content": "Extract name, email, and confidence as JSON."},
            {"role": "user", "content": text}
        ],
        response_format={"type": "json_object"},
    )

    data = json.loads(response.choices[0].message.content)

    try:
        return ExtractionResult(**data)
    except ValidationError as e:
        # Retry with explicit schema
        return retry_extraction(text, e.errors())
```

### Pitfall 4: Synchronous Calls in Async Applications

**Problem**: Blocking the event loop with synchronous API calls.

**Solution**: Use the async client:

```python
# BAD
from openai import OpenAI
client = OpenAI(api_key=key, base_url=url)
response = client.chat.completions.create(...)  # Blocks

# GOOD
from openai import AsyncOpenAI
client = AsyncOpenAI(api_key=key, base_url=url)
response = await client.chat.completions.create(...)  # Non-blocking
```

### Pitfall 5: No Rate Limiting

**Problem**: Hitting API rate limits and getting 429 errors.

**Solution**: Implement client-side rate limiting:

```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.timestamps = deque()

    async def acquire(self):
        now = time.time()
        while self.timestamps and self.timestamps[0] < now - self.window_seconds:
            self.timestamps.popleft()

        if len(self.timestamps) >= self.max_requests:
            sleep_time = self.timestamps[0] + self.window_seconds - now
            await asyncio.sleep(max(0, sleep_time))

        self.timestamps.append(time.time())
```

## Security Best Practices

### Input Sanitization

```python
import re

def sanitize_for_prompt(user_input: str) -> str:
    """Sanitize user input to prevent prompt injection."""
    # Remove common injection patterns
    patterns = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"you\s+are\s+now",
        r"system\s*:\s*",
        r"<\|im_start\|>",
        r"<\|im_end\|>",
    ]

    sanitized = user_input
    for pattern in patterns:
        sanitized = re.sub(pattern, "[REDACTED]", sanitized, flags=re.IGNORECASE)

    return sanitized

# Use in your API
@app.post("/chat")
async def chat(user_message: str):
    safe_message = sanitize_for_prompt(user_message)
    # Process with safe_message
```

### API Key Management

```python
# NEVER commit API keys to source control
# NEVER log API keys
# NEVER include API keys in error messages

import os
from pathlib import Path

def load_api_key() -> str:
    """Load API key from secure sources."""
    # 1. Environment variable (preferred)
    key = os.environ.get("XAI_API_KEY")
    if key:
        return key

    # 2. Secret file (Docker secrets, Kubernetes secrets)
    secret_path = Path("/run/secrets/xai_api_key")
    if secret_path.exists():
        return secret_path.read_text().strip()

    raise ValueError("XAI_API_KEY not found in environment or secrets")
```

## Checklist: Before Going to Production

- [ ] System prompt is well-defined and tested
- [ ] Error handling covers rate limits, timeouts, and API errors
- [ ] Rate limiting is implemented client-side
- [ ] API keys are stored securely (env vars, secrets manager)
- [ ] Model selection is appropriate for each use case
- [ ] Temperature and sampling parameters are tuned per task
- [ ] Output validation is implemented for structured responses
- [ ] Logging captures request/response metadata (no secrets)
- [ ] Monitoring tracks latency, error rates, and token usage
- [ ] Cost alerts are configured
- [ ] Graceful degradation is implemented
- [ ] Tests cover both happy path and error scenarios
- [ ] Input sanitization prevents prompt injection
- [ ] Context management prevents unbounded growth
- [ ] Streaming is used for user-facing real-time responses

## Related Documentation

- [Grok 4.5](./grok-4-5.md) — Model specification
- [Grok Code Fast 1](./grok-code-fast-1.md) — Code model
- [Vision Capabilities](./grok-vision.md) — Multimodal reference
- [Build Configuration](./grok-build.md) — Deployment guide
