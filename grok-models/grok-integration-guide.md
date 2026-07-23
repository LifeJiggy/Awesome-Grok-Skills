---
name: grok-integration-guide
category: guide
version: "1.0.0"
tags:
  - grok
  - api
  - integration
  - sdk
  - streaming
  - python
last_updated: 2026-07-23
author: Awesome Grok Skills Contributors
license: MIT
---

# Grok API Integration Guide: Patterns and Best Practices

## Overview

This guide covers practical integration patterns for the xAI Grok API. Learn
authentication, request/response handling, streaming, error management, rate
limiting, and SDK usage with working code examples in Python and curl.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Authentication](#authentication)
3. [Basic Request Pattern](#basic-request-pattern)
4. [Streaming Responses](#streaming-responses)
5. [Chat Completions](#chat-completions)
6. [Vision and Multimodal](#vision-and-multimodal)
7. [Error Handling](#error-handling)
8. [Rate Limiting](#rate-limiting)
9. [SDK Usage](#sdk-usage)
10. [Advanced Patterns](#advanced-patterns)
11. [Best Practices](#best-practices)
12. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites

1. xAI API account: https://console.x.ai
2. API key from console
3. Python 3.8+ or curl

### Minimal Working Example

```python
import requests

response = requests.post(
    "https://api.x.ai/v1/chat/completions",
    headers={
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    },
    json={
        "model": "grok-3",
        "messages": [
            {"role": "user", "content": "Hello, Grok!"}
        ]
    }
)

print(response.json()["choices"][0]["message"]["content"])
```

### curl Quick Start

```bash
curl -s https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-3",
    "messages": [
      {"role": "user", "content": "Hello, Grok!"}
    ]
  }'
```

---

## Authentication

### API Key Management

```python
import os
from pathlib import Path

class GrokAuth:
    """Secure API key management."""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or self._load_from_env()
        if not self.api_key:
            raise ValueError(
                "API key required. Set XAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
    
    def _load_from_env(self):
        """Load API key from environment."""
        return os.environ.get("XAI_API_KEY")
    
    def _load_from_file(self, filepath="~/.xai_api_key"):
        """Load API key from file."""
        path = Path(filepath).expanduser()
        if path.exists():
            return path.read_text().strip()
        return None
    
    def get_headers(self):
        """Return authorization headers."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
```

### Environment Variables

```bash
# Linux/macOS
export XAI_API_KEY="your-api-key-here"

# Windows PowerShell
$env:XAI_API_KEY="your-api-key-here"

# Windows CMD
set XAI_API_KEY=your-api-key-here
```

### Secure Storage

```python
# .env file (add to .gitignore)
XAI_API_KEY=your-api-key-here

# Load with python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ.get("XAI_API_KEY")
```

**Security Best Practices:**
- Never hardcode API keys in source code
- Use environment variables or secret managers
- Rotate keys regularly
- Use different keys for development/production
- Monitor API usage for anomalies

---

## Basic Request Pattern

### Request Structure

```python
import requests
from typing import Optional, Dict, Any

def grok_request(
    model: str,
    messages: list,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    stream: bool = False,
    **kwargs
) -> Dict[str, Any]:
    """
    Make a Grok API request.
    
    Args:
        model: Model identifier (e.g., "grok-3")
        messages: List of message dicts
        temperature: Sampling temperature (0.0-2.0)
        max_tokens: Maximum completion tokens
        stream: Enable streaming response
        **kwargs: Additional parameters
    
    Returns:
        API response dict
    """
    api_key = os.environ.get("XAI_API_KEY")
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        **kwargs
    }
    
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens
    
    if stream:
        payload["stream"] = True
    
    response = requests.post(
        "https://api.x.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=30
    )
    
    response.raise_for_status()
    return response.json()
```

### Response Structure

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1699876543,
  "model": "grok-3",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you today?"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 9,
    "total_tokens": 21
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique completion ID |
| `object` | string | Always "chat.completion" |
| `created` | int | Unix timestamp |
| `model` | string | Model used |
| `choices` | array | Completion options |
| `choices[].message` | object | Assistant message |
| `choices[].finish_reason` | string | "stop", "length", or "content_filter" |
| `usage` | object | Token counts |

---

## Streaming Responses

### Streaming Implementation

```python
import requests
import json

def stream_grok_response(model, messages, temperature=0.7):
    """
    Stream a Grok API response.
    
    Yields chunks as they arrive.
    """
    api_key = os.environ.get("XAI_API_KEY")
    
    response = requests.post(
        "https://api.x.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": True
        },
        stream=True,
        timeout=60
    )
    
    response.raise_for_status()
    
    for line in response.iter_lines():
        if line:
            line = line.decode("utf-8")
            
            # Skip SSE prefix
            if line.startswith("data: "):
                line = line[6:]
            
            # Check for stream end
            if line.strip() == "[DONE]":
                break
            
            try:
                chunk = json.loads(line)
                if "choices" in chunk and len(chunk["choices"]) > 0:
                    delta = chunk["choices"][0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        yield content
            except json.JSONDecodeError:
                continue
```

### Streaming with Display

```python
import sys

def print_streaming_response(model, messages):
    """Print response as it streams."""
    print("Response: ", end="", flush=True)
    
    for chunk in stream_grok_response(model, messages):
        print(chunk, end="", flush=True)
    
    print()  # Newline after completion

# Usage
print_streaming_response(
    "grok-3",
    [{"role": "user", "content": "Write a haiku about coding"}]
)
```

### curl Streaming

```bash
curl -s https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-3",
    "messages": [{"role": "user", "content": "Hello"}],
    "stream": true
  }' | while read line; do
    echo "$line" | grep -o '"content":"[^"]*"' | cut -d'"' -f4
done
```

---

## Chat Completions

### System Messages

```python
def chat_with_system(system_prompt, user_message, model="grok-3"):
    """Chat with system-level instructions."""
    return grok_request(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

# Example: Code reviewer
response = chat_with_system(
    system_prompt="You are an expert Python developer. Review code for bugs and improvements.",
    user_message="def add(a,b): return a+b"
)
```

### Multi-turn Conversations

```python
class GrokChat:
    """Manage multi-turn conversations."""
    
    def __init__(self, model="grok-3", system_prompt=None):
        self.model = model
        self.messages = []
        
        if system_prompt:
            self.messages.append({
                "role": "system",
                "content": system_prompt
            })
    
    def add_user_message(self, content):
        """Add a user message."""
        self.messages.append({
            "role": "user",
            "content": content
        })
    
    def add_assistant_message(self, content):
        """Add an assistant message."""
        self.messages.append({
            "role": "assistant",
            "content": content
        })
    
    def send(self, user_message):
        """Send message and get response."""
        self.add_user_message(user_message)
        
        response = grok_request(
            model=self.model,
            messages=self.messages
        )
        
        assistant_content = response["choices"][0]["message"]["content"]
        self.add_assistant_message(assistant_content)
        
        return assistant_content

# Usage
chat = GrokChat(
    model="grok-3",
    system_prompt="You are a helpful cooking assistant."
)

print(chat.send("What's a good pasta recipe?"))
print(chat.send("Can I substitute gluten-free pasta?"))
```

### Message Roles

| Role | Description | Usage |
|------|-------------|-------|
| `system` | Instructions for behavior | Set once at start |
| `user` | User input | Each user turn |
| `assistant` | Model responses | Model's replies |
| `function` | Function call results | After function calls |
| `tool` | Tool call results | After tool use |

### Content Types

```python
# Text content
{"role": "user", "content": "Hello"}

# Image content (multimodal)
{
    "role": "user",
    "content": [
        {"type": "text", "text": "What's in this image?"},
        {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
    ]
}

# Function call
{
    "role": "assistant",
    "content": None,
    "function_call": {
        "name": "get_weather",
        "arguments": "{\"location\": \"San Francisco\"}"
    }
}
```

---

## Vision and Multimodal

### Image Analysis

```python
import base64
from pathlib import Path

def analyze_image(image_path, question, model="grok-3"):
    """Analyze an image with a question."""
    
    # Read and encode image
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    
    # Determine MIME type
    suffix = Path(image_path).suffix.lower()
    mime_map = {".jpg": "jpeg", ".jpeg": "jpeg", ".png": "png", ".gif": "gif", ".webp": "webp"}
    mime_type = f"image/{mime_map.get(suffix, 'jpeg')}"
    
    response = grok_request(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{image_data}"
                        }
                    }
                ]
            }
        ]
    )
    
    return response["choices"][0]["message"]["content"]

# Usage
result = analyze_image(
    "screenshot.png",
    "Describe the UI layout and identify any issues"
)
```

### Multiple Images

```python
def compare_images(image_paths, question):
    """Compare multiple images."""
    content = [{"type": "text", "text": question}]
    
    for path in image_paths:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{data}"}
        })
    
    return grok_request(
        model="grok-3",
        messages=[{"role": "user", "content": content}]
    )
```

---

## Error Handling

### Error Response Format

```json
{
  "error": {
    "message": "Invalid API key",
    "type": "authentication_error",
    "code": "invalid_api_key"
  }
}
```

### Common Error Codes

| Code | Type | Cause | Solution |
|------|------|-------|----------|
| `invalid_api_key` | authentication_error | Bad/missing key | Check API key |
| `model_not_found` | invalid_request_error | Wrong model name | Use valid model |
| `context_length_exceeded` | invalid_request_error | Input too long | Reduce input size |
| `rate_limit_exceeded` | rate_limit_error | Too many requests | Implement backoff |
| `server_error` | server_error | xAI issue | Retry with backoff |

### Error Handling Implementation

```python
import time
from typing import Optional

class GrokError(Exception):
    """Base Grok API error."""
    def __init__(self, message, error_type=None, code=None):
        super().__init__(message)
        self.error_type = error_type
        self.code = code

class RateLimitError(GrokError):
    """Rate limit exceeded."""
    pass

class AuthenticationError(GrokError):
    """Authentication failed."""
    pass

class ContextLengthError(GrokError):
    """Input exceeds context window."""
    pass

def handle_grok_error(response):
    """Parse and raise appropriate error."""
    if response.status_code == 200:
        return response.json()
    
    try:
        error_data = response.json().get("error", {})
    except:
        error_data = {"message": response.text}
    
    error_type = error_data.get("type", "unknown")
    message = error_data.get("message", "Unknown error")
    code = error_data.get("code")
    
    error_map = {
        "authentication_error": AuthenticationError,
        "rate_limit_error": RateLimitError,
        "invalid_request_error": GrokError,
        "server_error": GrokError,
    }
    
    ErrorClass = error_map.get(error_type, GrokError)
    raise ErrorClass(message, error_type=error_type, code=code)

def grok_request_with_retry(
    model: str,
    messages: list,
    max_retries: int = 3,
    base_delay: float = 1.0
):
    """Make request with exponential backoff retry."""
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.environ.get('XAI_API_KEY')}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": messages
                },
                timeout=30
            )
            
            return handle_grok_error(response)
            
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            
            delay = base_delay * (2 ** attempt)
            print(f"Rate limited. Retrying in {delay}s...")
            time.sleep(delay)
            
        except AuthenticationError:
            raise  # Don't retry auth errors
        
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            delay = base_delay * (2 ** attempt)
            print(f"Error: {e}. Retrying in {delay}s...")
            time.sleep(delay)
```

---

## Rate Limiting

### Current Limits

| Tier | Requests/min | Tokens/min | Daily Limit |
|------|--------------|------------|-------------|
| Free | 1 | 10,000 | 100,000 |
| Tier 1 ($5) | 10 | 100,000 | 1,000,000 |
| Tier 2 ($25) | 50 | 500,000 | 10,000,000 |
| Tier 3 ($100) | 200 | 2,000,000 | 100,000,000 |

### Client-Side Rate Limiting

```python
import time
from collections import deque

class RateLimiter:
    """Token bucket rate limiter."""
    
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = deque()
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded."""
        now = time.time()
        
        # Remove old requests outside window
        while self.requests and self.requests[0] < now - self.window_seconds:
            self.requests.popleft()
        
        # If at limit, wait
        if len(self.requests) >= self.max_requests:
            sleep_time = self.requests[0] + self.window_seconds - now
            if sleep_time > 0:
                print(f"Rate limit reached. Waiting {sleep_time:.1f}s...")
                time.sleep(sleep_time)
        
        self.requests.append(time.time())

# Usage
limiter = RateLimiter(max_requests=10, window_seconds=60)

def rate_limited_request(model, messages):
    """Make rate-limited request."""
    limiter.wait_if_needed()
    return grok_request(model, messages)
```

### Streaming Rate Limit Handling

```python
def stream_with_rate_limit(model, messages):
    """Handle rate limits during streaming."""
    max_retries = 3
    base_delay = 1.0
    
    for attempt in range(max_retries):
        try:
            return list(stream_grok_response(model, messages))
        
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            
            delay = base_delay * (2 ** attempt)
            print(f"Rate limited. Waiting {delay}s...")
            time.sleep(delay)
```

---

## SDK Usage

### Official Python SDK

```bash
pip install xai-sdk
```

```python
from xai import XAI

client = XAI(api_key="your-api-key")

# Basic completion
response = client.chat.completions.create(
    model="grok-3",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

### Async SDK Usage

```python
import asyncio
from xai import AsyncXAI

async def main():
    client = AsyncXAI(api_key="your-api-key")
    
    response = await client.chat.completions.create(
        model="grok-3",
        messages=[
            {"role": "user", "content": "Hello!"}
        ]
    )
    
    print(response.choices[0].message.content)

asyncio.run(main())
```

### SDK Streaming

```python
from xai import XAI

client = XAI(api_key="your-api-key")

# Stream completion
stream = client.chat.completions.create(
    model="grok-3",
    messages=[
        {"role": "user", "content": "Tell me a story"}
    ],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### SDK with Tools/Functions

```python
from xai import XAI

client = XAI(api_key="your-api-key")

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
                        "description": "City name"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="grok-3",
    messages=[
        {"role": "user", "content": "What's the weather in San Francisco?"}
    ],
    tools=tools,
    tool_choice="auto"
)

# Handle tool call
tool_call = response.choices[0].message.tool_calls[0]
print(f"Function: {tool_call.function.name}")
print(f"Arguments: {tool_call.function.arguments}")
```

---

## Advanced Patterns

### Conversation with Memory

```python
class GrokMemory:
    """Conversation with summarization for memory."""
    
    def __init__(self, model="grok-3", max_history=20):
        self.model = model
        self.max_history = max_history
        self.messages = []
        self.summary = None
    
    def add_message(self, role, content):
        """Add message and summarize if too long."""
        self.messages.append({"role": role, "content": content})
        
        if len(self.messages) > self.max_history:
            self._summarize()
    
    def _summarize(self):
        """Summarize old messages."""
        old_messages = self.messages[:10]
        self.messages = self.messages[10:]
        
        summary_response = grok_request(
            self.model,
            [
                {"role": "system", "content": "Summarize this conversation:"},
                *old_messages
            ]
        )
        
        new_summary = summary_response["choices"][0]["message"]["content"]
        
        if self.summary:
            self.summary = f"{self.summary}\n\n{new_summary}"
        else:
            self.summary = new_summary
        
        self.messages.insert(0, {
            "role": "system",
            "content": f"Conversation summary:\n{self.summary}"
        })
    
    def send(self, user_message):
        """Send message with memory."""
        self.add_message("user", user_message)
        
        response = grok_request(self.model, self.messages)
        assistant_content = response["choices"][0]["message"]["content"]
        
        self.add_message("assistant", assistant_content)
        
        return assistant_content
```

### Parallel Requests

```python
import concurrent.futures
from typing import List

def parallel_grok_requests(
    requests_data: List[dict],
    max_workers: int = 5
) -> List[dict]:
    """Make multiple parallel API requests."""
    
    def make_request(data):
        return grok_request(
            model=data.get("model", "grok-3"),
            messages=data["messages"]
        )
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(make_request, req) for req in requests_data]
        results = []
        
        for future in concurrent.futures.as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                results.append({"error": str(e)})
    
    return results
```

### Response Caching

```python
import hashlib
import json
from functools import lru_cache

class GrokCache:
    """Cache API responses."""
    
    def __init__(self, cache_dir=".grok_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def _get_cache_key(self, model, messages, **kwargs):
        """Generate cache key from request."""
        data = json.dumps({"model": model, "messages": messages, **kwargs})
        return hashlib.sha256(data.encode()).hexdigest()
    
    def get(self, model, messages, **kwargs):
        """Get cached response if exists."""
        key = self._get_cache_key(model, messages, **kwargs)
        cache_file = self.cache_dir / f"{key}.json"
        
        if cache_file.exists():
            return json.loads(cache_file.read_text())
        
        return None
    
    def set(self, model, messages, response, **kwargs):
        """Cache a response."""
        key = self._get_cache_key(model, messages, **kwargs)
        cache_file = self.cache_dir / f"{key}.json"
        cache_file.write_text(json.dumps(response))

# Usage
cache = GrokCache()

def cached_grok_request(model, messages, **kwargs):
    """Request with caching."""
    cached = cache.get(model, messages, **kwargs)
    if cached:
        return cached
    
    response = grok_request(model, messages, **kwargs)
    cache.set(model, messages, response, **kwargs)
    
    return response
```

---

## Best Practices

### 1. Input Optimization

```python
def optimize_messages(messages, max_context=120000):
    """Optimize message context to fit within limits."""
    total_tokens = sum(len(m["content"]) // 4 for m in messages)
    
    if total_tokens > max_context:
        # Keep system message and recent messages
        system_msgs = [m for m in messages if m["role"] == "system"]
        other_msgs = [m for m in messages if m["role"] != "system"]
        
        # Keep most recent messages
        kept_tokens = 0
        kept_messages = []
        
        for msg in reversed(other_msgs):
            msg_tokens = len(msg["content"]) // 4
            if kept_tokens + msg_tokens > max_context * 0.8:
                break
            kept_messages.insert(0, msg)
            kept_tokens += msg_tokens
        
        return system_msgs + kept_messages
    
    return messages
```

### 2. Output Validation

```python
def validate_response(response, required_fields=None):
    """Validate API response structure."""
    if "choices" not in response:
        raise ValueError("No choices in response")
    
    if len(response["choices"]) == 0:
        raise ValueError("Empty choices array")
    
    choice = response["choices"][0]
    
    if "message" not in choice:
        raise ValueError("No message in choice")
    
    if required_fields:
        for field in required_fields:
            if field not in response:
                raise ValueError(f"Missing field: {field}")
    
    return True
```

### 3. Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("grok")

def log_request(model, messages, response=None, error=None):
    """Log API request/response."""
    log_data = {
        "model": model,
        "message_count": len(messages),
        "timestamp": time.time()
    }
    
    if response:
        log_data["tokens"] = response.get("usage", {}).get("total_tokens")
        log_data["finish_reason"] = response["choices"][0].get("finish_reason")
        logger.info(f"Request completed: {log_data}")
    
    if error:
        log_data["error"] = str(error)
        logger.error(f"Request failed: {log_data}")
```

### 4. Graceful Degradation

```python
def grok_with_fallback(messages, preferred_model="grok-4-5"):
    """Try preferred model, fallback to cheaper options."""
    fallback_chain = ["grok-4-5", "grok-4-1", "grok-4", "grok-3", "grok-3-mini"]
    
    start_idx = fallback_chain.index(preferred_model) if preferred_model in fallback_chain else 0
    
    for model in fallback_chain[start_idx:]:
        try:
            return grok_request(model, messages)
        except RateLimitError:
            continue
        except Exception as e:
            logger.warning(f"Model {model} failed: {e}")
            continue
    
    raise Exception("All models failed")
```

---

## Troubleshooting

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| 401 Unauthorized | Authentication error | Check API key |
| 429 Too Many Requests | Rate limit error | Implement backoff |
| Context too long | 400 error | Reduce input size |
| Slow response | Timeouts | Use faster model |
| Empty response | No content | Check message format |

### Debug Mode

```python
def debug_grok_request(model, messages, verbose=True):
    """Debug API request with detailed logging."""
    
    if verbose:
        print(f"Model: {model}")
        print(f"Messages: {len(messages)}")
        print(f"Total chars: {sum(len(m['content']) for m in messages)}")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.environ.get('XAI_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": messages
            },
            timeout=30
        )
        
        elapsed = time.time() - start_time
        
        if verbose:
            print(f"Status: {response.status_code}")
            print(f"Time: {elapsed:.2f}s")
            print(f"Headers: {dict(response.headers)}")
        
        if response.status_code != 200:
            print(f"Error: {response.text}")
            return None
        
        return response.json()
        
    except Exception as e:
        print(f"Exception: {e}")
        return None
```

### Performance Monitoring

```python
class GrokMetrics:
    """Track API performance metrics."""
    
    def __init__(self):
        self.requests = []
    
    def record(self, model, tokens, latency, success):
        """Record a request metric."""
        self.requests.append({
            "model": model,
            "tokens": tokens,
            "latency": latency,
            "success": success,
            "timestamp": time.time()
        })
    
    def summary(self):
        """Get metrics summary."""
        if not self.requests:
            return {}
        
        successful = [r for r in self.requests if r["success"]]
        failed = [r for r in self.requests if not r["success"]]
        
        return {
            "total_requests": len(self.requests),
            "successful": len(successful),
            "failed": len(failed),
            "avg_latency": sum(r["latency"] for r in successful) / len(successful) if successful else 0,
            "total_tokens": sum(r["tokens"] for r in successful)
        }
```

---

## References

- xAI API Docs: https://docs.x.ai
- Python SDK: https://pypi.org/project/xai-sdk/
- Rate Limits: https://docs.x.ai/rate-limits
- Error Codes: https://docs.x.ai/errors

---

*Last updated: 2026-07-23 | Version 1.0.0*
