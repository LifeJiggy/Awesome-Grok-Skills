---
name: grok-api-reference
category: reference
version: "1.0.0"
tags:
  - grok
  - api
  - reference
  - endpoints
  - documentation
last_updated: 2026-07-23
author: Awesome Grok Skills Contributors
license: MIT
---

# Grok API Reference: Complete Endpoint Documentation

## Overview

This document provides a comprehensive reference for the xAI Grok API. All endpoints,
parameters, response formats, error codes, authentication details, and versioning
information are covered with examples.

**Base URL:** `https://api.x.ai/v1`

**Authentication:** Bearer token via `Authorization` header

---

## Table of Contents

1. [API Overview](#api-overview)
2. [Authentication](#authentication)
3. [Chat Completions](#chat-completions)
4. [Models](#models)
5. [Embeddings](#embeddings)
6. [Images](#images)
7. [Audio](#audio)
8. [Files](#files)
9. [Error Reference](#error-reference)
10. [Rate Limits](#rate-limits)
11. [Versioning](#versioning)
12. [Webhooks](#webhooks)

---

## API Overview

### Request Format

All requests use JSON with the following headers:

```
Authorization: Bearer $XAI_API_KEY
Content-Type: application/json
```

### Response Format

All responses return JSON. Successful responses include the requested data.
Errors return an error object with details.

### HTTP Methods

| Method | Usage |
|--------|-------|
| `GET` | Retrieve resources |
| `POST` | Create resources |
| `PUT` | Update resources |
| `DELETE` | Delete resources |

### Request Limits

| Limit | Value |
|-------|-------|
| Max request size | 10 MB |
| Max URL length | 2,048 characters |
| Timeout | 30 seconds (default) |
| Max retries | 3 (recommended) |

---

## Authentication

### API Key Authentication

All API requests require authentication via Bearer token:

```bash
curl -s https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "grok-3", "messages": [{"role": "user", "content": "Hello"}]}'
```

### Key Types

| Type | Prefix | Usage |
|------|--------|-------|
| Production | `xai-` | Live applications |
| Development | `xai-dev-` | Testing only |
| Restricted | `xai-r-` | Limited endpoints |

### Key Management

```python
import os

# Load API key
api_key = os.environ.get("XAI_API_KEY")

# Validate key format
if not api_key or not api_key.startswith("xai-"):
    raise ValueError("Invalid API key format")
```

### Scopes

| Scope | Access |
|-------|--------|
| `read` | GET requests only |
| `write` | GET + POST requests |
| `admin` | Full access |

---

## Chat Completions

### Create Chat Completion

**Endpoint:** `POST /v1/chat/completions`

Creates a model response for the given conversation.

#### Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model` | string | Yes | - | Model ID to use |
| `messages` | array | Yes | - | Conversation messages |
| `temperature` | number | No | 1.0 | Sampling temperature (0.0-2.0) |
| `top_p` | number | No | 1.0 | Nucleus sampling parameter |
| `max_tokens` | integer | No | null | Max completion tokens |
| `stream` | boolean | No | false | Enable streaming |
| `stop` | string/array | No | null | Stop sequences |
| `presence_penalty` | number | No | 0.0 | Presence penalty (-2.0 to 2.0) |
| `frequency_penalty` | number | No | 0.0 | Frequency penalty (-2.0 to 2.0) |
| `logit_bias` | object | No | null | Token bias adjustments |
| `user` | string | No | null | End-user identifier |
| `tools` | array | No | null | Available tools |
| `tool_choice` | string/object | No | "auto" | Tool selection strategy |
| `response_format` | object | No | null | Output format specification |

#### Messages Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `role` | string | Yes | "system", "user", "assistant", "function", "tool" |
| `content` | string/array | Yes | Message content |
| `name` | string | No | Participant name |
| `function_call` | object | No | Function call details |
| `tool_calls` | array | No | Tool calls |
| `tool_call_id` | string | No | Tool call identifier |

#### Request Example (curl)

```bash
curl -s https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-3",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "What is the capital of France?"
      }
    ],
    "temperature": 0.7,
    "max_tokens": 1024,
    "stream": false
  }'
```

#### Request Example (Python)

```python
import requests
import os

response = requests.post(
    "https://api.x.ai/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.environ.get('XAI_API_KEY')}",
        "Content-Type": "application/json"
    },
    json={
        "model": "grok-3",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }
)

print(response.json())
```

#### Response Format

```json
{
  "id": "chatcmpl-abc123def456",
  "object": "chat.completion",
  "created": 1699876543,
  "model": "grok-3",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "The capital of France is Paris."
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 10,
    "total_tokens": 35
  },
  "system_fingerprint": "fp_abc123"
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique completion identifier |
| `object` | string | Always "chat.completion" |
| `created` | integer | Unix timestamp of creation |
| `model` | string | Model used for completion |
| `choices` | array | Completion choices |
| `choices[].index` | integer | Choice index (0-based) |
| `choices[].message` | object | Generated message |
| `choices[].finish_reason` | string | "stop", "length", "tool_calls", "content_filter" |
| `usage` | object | Token usage statistics |
| `usage.prompt_tokens` | integer | Tokens in prompt |
| `usage.completion_tokens` | integer | Tokens in completion |
| `usage.total_tokens` | integer | Total tokens used |

---

## Models

### List Models

**Endpoint:** `GET /v1/models`

Returns all available models.

#### Response Example

```json
{
  "object": "list",
  "data": [
    {
      "id": "grok-4-5",
      "object": "model",
      "created": 1706745600,
      "owned_by": "xai",
      "permission": [],
      "root": "grok-4-5",
      "parent": null
    },
    {
      "id": "grok-4-1",
      "object": "model",
      "created": 1700000000,
      "owned_by": "xai",
      "permission": [],
      "root": "grok-4-1",
      "parent": null
    }
  ]
}
```

### Retrieve Model

**Endpoint:** `GET /v1/models/{model_id}`

Returns details for a specific model.

#### Path Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | string | Model identifier |

#### Response Example

```json
{
  "id": "grok-3",
  "object": "model",
  "created": 1699000000,
  "owned_by": "xai",
  "permission": [
    {
      "id": "modelperm-abc123",
      "object": "model_permission",
      "created": 1699000000,
      "allow_create_engine": false,
      "allow_sampling": true,
      "allow_logprobs": true,
      "allow_search_indices": false,
      "allow_view": true,
      "allow_fine_tuning": false,
      "organization": "*",
      "group": null,
      "is_blocking": false
    }
  ],
  "root": "grok-3",
  "parent": null
}
```

### Delete Model

**Endpoint:** `DELETE /v1/models/{model_id}`

Deletes a fine-tuned model.

```bash
curl -s -X DELETE https://api.x.ai/v1/models/ft:grok-3:org:custom:id \
  -H "Authorization: Bearer $XAI_API_KEY"
```

---

## Embeddings

### Create Embedding

**Endpoint:** `POST /v1/embeddings`

Creates an embedding vector for input text.

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | Embedding model ID |
| `input` | string/array | Yes | Text to embed |
| `encoding_format` | string | No | "float" (default) or "base64" |
| `dimensions` | integer | No | Output dimensions |

#### Request Example

```bash
curl -s https://api.x.ai/v1/embeddings \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-embedding-v1",
    "input": "The quick brown fox jumps over the lazy dog"
  }'
```

#### Response Example

```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [0.0023064255, -0.009327292, 0.015795325, ...],
      "index": 0
    }
  ],
  "model": "grok-embedding-v1",
  "usage": {
    "prompt_tokens": 8,
    "total_tokens": 8
  }
}
```

#### Batch Embeddings

```python
import requests

response = requests.post(
    "https://api.x.ai/v1/embeddings",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    json={
        "model": "grok-embedding-v1",
        "input": [
            "First text to embed",
            "Second text to embed",
            "Third text to embed"
        ]
    }
)

embeddings = [item["embedding"] for item in response.json()["data"]]
```

---

## Images

### Create Image

**Endpoint:** `POST /v1/images/generations`

Generates an image from a text prompt.

#### Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `model` | string | No | "grok-image-v1" | Image model |
| `prompt` | string | Yes | - | Text description |
| `n` | integer | No | 1 | Number of images (1-4) |
| `size` | string | No | "1024x1024" | Image dimensions |
| `quality` | string | No | "standard" | "standard" or "hd" |
| `response_format` | string | No | "url" | "url" or "b64_json" |

#### Supported Sizes

| Size | Aspect Ratio |
|------|--------------|
| `1024x1024` | 1:1 (Square) |
| `1024x1792` | 9:16 (Portrait) |
| `1792x1024` | 16:9 (Landscape) |
| `512x512` | 1:1 (Small) |

#### Request Example

```bash
curl -s https://api.x.ai/v1/images/generations \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-image-v1",
    "prompt": "A futuristic city skyline at sunset, cyberpunk style",
    "n": 1,
    "size": "1024x1024",
    "quality": "hd"
  }'
```

#### Response Example

```json
{
  "created": 1699876543,
  "data": [
    {
      "url": "https://api.x.ai/v1/images/img-abc123.png",
      "revised_prompt": "A futuristic city skyline at sunset...",
      "b64_json": null
    }
  ]
}
```

### Edit Image

**Endpoint:** `POST /v1/images/edits`

Edits an image with a text prompt (requires image upload).

```bash
curl -s https://api.x.ai/v1/images/edits \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -F "image=@original.png" \
  -F "prompt=Add a rainbow in the sky" \
  -F "n=1" \
  -F "size=1024x1024"
```

### Create Image Variation

**Endpoint:** `POST /v1/images/variations`

Creates variations of an image.

```bash
curl -s https://api.x.ai/v1/images/variations \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -F "image=@original.png" \
  -F "n=3" \
  -F "size=1024x1024"
```

---

## Audio

### Create Transcription

**Endpoint:** `POST /v1/audio/transcriptions`

Transcribes audio to text.

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | file | Yes | Audio file (mp3, mp4, wav, etc.) |
| `model` | string | Yes | "grok-audio-v1" |
| `language` | string | No | ISO 639-1 language code |
| `prompt` | string | No | Transcript hint |
| `response_format` | string | No | "json", "text", "verbose_json", "srt", "vtt" |

#### Request Example

```bash
curl -s https://api.x.ai/v1/audio/transcriptions \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -F "file=@audio.mp3" \
  -F "model=grok-audio-v1" \
  -F "language=en" \
  -F "response_format=text"
```

#### Response Example

```json
{
  "text": "The transcription of the audio file..."
}
```

### Create Translation

**Endpoint:** `POST /v1/audio/translations`

Translates audio to English text.

```bash
curl -s https://api.x.ai/v1/audio/translations \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -F "file=@spanish_audio.mp3" \
  -F "model=grok-audio-v1"
```

### Create Speech

**Endpoint:** `POST /v1/audio/speech`

Converts text to speech audio.

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | "grok-tts-v1" |
| `input` | string | Yes | Text to speak |
| `voice` | string | Yes | "alloy", "echo", "fable", "onyx", "nova", "shimmer" |
| `response_format` | string | No | "mp3", "opus", "aac", "flac" |
| `speed` | number | No | 0.25 to 4.0 (default 1.0) |

```bash
curl -s https://api.x.ai/v1/audio/speech \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-tts-v1",
    "input": "Hello, welcome to xAI!",
    "voice": "nova",
    "response_format": "mp3"
  }' \
  --output speech.mp3
```

---

## Files

### Upload File

**Endpoint:** `POST /v1/files`

Uploads a file for use with the API.

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | file | Yes | File to upload |
| `purpose` | string | Yes | "fine-tune", "assistants", "batch" |

#### Supported File Types

| Type | Extensions | Max Size |
|------|------------|----------|
| Text | .jsonl, .txt, .csv, .tsv | 512 MB |
| Code | .py, .js, .ts, etc. | 50 MB |
| Documents | .pdf, .docx | 100 MB |
| Images | .png, .jpg, .gif, .webp | 20 MB |

```bash
curl -s https://api.x.ai/v1/files \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -F "file=@training_data.jsonl" \
  -F "purpose=fine-tune"
```

#### Response Example

```json
{
  "id": "file-abc123def456",
  "object": "file",
  "bytes": 123456,
  "created_at": 1699876543,
  "filename": "training_data.jsonl",
  "purpose": "fine-tune",
  "status": "processed",
  "status_details": null
}
```

### List Files

**Endpoint:** `GET /v1/files`

```bash
curl -s https://api.x.ai/v1/files \
  -H "Authorization: Bearer $XAI_API_KEY"
```

### Retrieve File

**Endpoint:** `GET /v1/files/{file_id}`

```bash
curl -s https://api.x.ai/v1/files/file-abc123def456 \
  -H "Authorization: Bearer $XAI_API_KEY"
```

### Delete File

**Endpoint:** `DELETE /v1/files/{file_id}`

```bash
curl -s -X DELETE https://api.x.ai/v1/files/file-abc123def456 \
  -H "Authorization: Bearer $XAI_API_KEY"
```

### Download File

**Endpoint:** `GET /v1/files/{file_id}/content`

```bash
curl -s https://api.x.ai/v1/files/file-abc123def456/content \
  -H "Authorization: Bearer $XAI_API_KEY" \
  --output downloaded_file.jsonl
```

---

## Error Reference

### Error Response Format

```json
{
  "error": {
    "message": "Invalid API key provided",
    "type": "authentication_error",
    "code": "invalid_api_key",
    "param": null
  }
}
```

### Error Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `message` | string | Human-readable error message |
| `type` | string | Error category |
| `code` | string | Specific error code |
| `param` | string/null | Parameter that caused the error |

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid API key |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 408 | Request Timeout |
| 409 | Conflict - Resource conflict |
| 413 | Payload Too Large |
| 422 | Unprocessable Entity |
| 429 | Too Many Requests - Rate limited |
| 500 | Internal Server Error |
| 502 | Bad Gateway |
| 503 | Service Unavailable |
| 504 | Gateway Timeout |

### Error Types and Codes

#### Authentication Errors

| Code | Message | Solution |
|------|---------|----------|
| `invalid_api_key` | Invalid API key provided | Check API key |
| `api_key_expired` | API key has expired | Generate new key |
| `api_key_deactivated` | API key has been deactivated | Contact support |

#### Rate Limit Errors

| Code | Message | Solution |
|------|---------|----------|
| `rate_limit_exceeded` | Rate limit exceeded | Wait and retry |
| `tokens_per_minute_exceeded` | TPM limit exceeded | Reduce request rate |
| `requests_per_minute_exceeded` | RPM limit exceeded | Reduce request rate |

#### Request Errors

| Code | Message | Solution |
|------|---------|----------|
| `invalid_request` | Invalid request format | Check request body |
| `model_not_found` | Model does not exist | Use valid model ID |
| `context_length_exceeded` | Input exceeds context window | Reduce input size |
| `invalid_temperature` | Temperature out of range | Use 0.0-2.0 |
| `invalid_max_tokens` | Max tokens out of range | Use valid range |
| `invalid_stop_sequence` | Invalid stop sequence | Check stop parameter |
| `invalid_tool_choice` | Invalid tool choice | Check tool_choice parameter |

#### Content Errors

| Code | Message | Solution |
|------|---------|----------|
| `content_filtered` | Content was filtered | Modify input |
| `invalid_content` | Invalid content format | Check content |
| `harmful_content` | Potentially harmful content | Review input |

#### Server Errors

| Code | Message | Solution |
|------|---------|----------|
| `server_error` | Internal server error | Retry with backoff |
| `model_overloaded` | Model is currently overloaded | Wait and retry |
| `maintenance` | System under maintenance | Wait and retry |

### Error Handling Examples

#### Python

```python
import requests

class GrokAPIError(Exception):
    def __init__(self, status_code, error_type, message, code):
        self.status_code = status_code
        self.error_type = error_type
        self.message = message
        self.code = code
        super().__init__(f"{error_type}: {message}")

def handle_error(response):
    """Parse error response."""
    try:
        error_data = response.json().get("error", {})
    except:
        error_data = {
            "message": response.text,
            "type": "unknown",
            "code": "unknown"
        }
    
    raise GrokAPIError(
        status_code=response.status_code,
        error_type=error_data.get("type", "unknown"),
        message=error_data.get("message", "Unknown error"),
        code=error_data.get("code", "unknown")
    )
```

#### JavaScript

```javascript
class GrokAPIError extends Error {
    constructor(statusCode, errorType, message, code) {
        super(`${errorType}: ${message}`);
        this.statusCode = statusCode;
        this.errorType = errorType;
        this.code = code;
    }
}

async function handleResponse(response) {
    if (!response.ok) {
        const error = await response.json();
        throw new GrokAPIError(
            response.status,
            error.error?.type || 'unknown',
            error.error?.message || 'Unknown error',
            error.error?.code || 'unknown'
        );
    }
    return response.json();
}
```

---

## Rate Limits

### Default Limits

| Tier | RPM | TPM | Daily Tokens |
|------|-----|-----|--------------|
| Free | 1 | 10,000 | 100,000 |
| Tier 1 | 10 | 100,000 | 1,000,000 |
| Tier 2 | 50 | 500,000 | 10,000,000 |
| Tier 3 | 200 | 2,000,000 | 100,000,000 |
| Enterprise | Custom | Custom | Custom |

### Model-Specific Limits

| Model | RPM | TPM | Notes |
|-------|-----|-----|-------|
| grok-4-5 | 20 | 50,000 | Premium model |
| grok-4-1 | 50 | 200,000 | Standard |
| grok-4 | 50 | 200,000 | Standard |
| grok-3 | 100 | 500,000 | High throughput |
| grok-3-fast | 100 | 500,000 | High throughput |
| grok-3-mini | 200 | 1,000,000 | Highest throughput |

### Rate Limit Headers

| Header | Description |
|--------|-------------|
| `x-ratelimit-limit-requests` | RPM limit |
| `x-ratelimit-remaining-requests` | Remaining RPM |
| `x-ratelimit-reset-requests` | Time until RPM reset |
| `x-ratelimit-limit-tokens` | TPM limit |
| `x-ratelimit-remaining-tokens` | Remaining TPM |
| `x-ratelimit-reset-tokens` | Time until TPM reset |

### Rate Limit Response

```json
{
  "error": {
    "message": "Rate limit exceeded",
    "type": "rate_limit_error",
    "code": "rate_limit_exceeded"
  }
}
```

### Handling Rate Limits

```python
import time
from functools import wraps

def retry_on_rate_limit(max_retries=3, base_delay=1.0):
    """Decorator for rate limit retry."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except GrokAPIError as e:
                    if e.code != "rate_limit_exceeded":
                        raise
                    if attempt == max_retries - 1:
                        raise
                    
                    delay = base_delay * (2 ** attempt)
                    print(f"Rate limited. Retrying in {delay}s...")
                    time.sleep(delay)
            return wrapper
        return decorator
```

---

## Versioning

### API Versions

| Version | Status | Base URL |
|---------|--------|----------|
| v1 | Current, stable | `https://api.x.ai/v1` |
| v0 | Deprecated | N/A |

### Version Selection

Use the URL path to specify version:

```
https://api.x.ai/v1/chat/completions
```

### Breaking Changes Policy

- New versions released for breaking changes
- Previous versions supported for 12 months after deprecation
- Deprecation notices sent 6 months in advance
- Non-breaking additions made within current version

### Model Versioning

| Model | API Version | Status |
|-------|-------------|--------|
| grok-4-5 | v1 | Current |
| grok-4-1 | v1 | Current |
| grok-4 | v1 | Current |
| grok-3 | v1 | Current |
| grok-2 | v1 | Legacy |
| grok-1 | v1 | Deprecated |

### Migration Guide

```python
# v1 request (current)
response = requests.post(
    "https://api.x.ai/v1/chat/completions",
    headers=headers,
    json=payload
)
```

---

## Webhooks

### Webhook Events

| Event | Description |
|-------|-------------|
| `completion.completed` | Async completion finished |
| `file.processed` | File processing complete |
| `fine_tune.completed` | Fine-tuning job complete |
| `fine_tune.failed` | Fine-tuning job failed |

### Webhook Registration

**Endpoint:** `POST /v1/webhooks`

```bash
curl -s https://api.x.ai/v1/webhooks \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-server.com/webhook",
    "events": ["completion.completed", "file.processed"],
    "secret": "your-webhook-secret"
  }'
```

### Webhook Payload

```json
{
  "id": "evt_abc123",
  "object": "event",
  "type": "completion.completed",
  "created": 1699876543,
  "data": {
    "object": {
      "id": "chatcmpl-abc123",
      "status": "completed"
    }
  }
}
```

### Webhook Verification

```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    """Verify webhook signature."""
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected, signature)
```

### Webhook Response

Your endpoint should return:
- 200 OK for successful processing
- 4xx for invalid payloads
- 5xx will trigger retry (3 attempts)

---

## Quick Reference

### All Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/chat/completions` | POST | Create chat completion |
| `/v1/models` | GET | List models |
| `/v1/models/{model_id}` | GET | Retrieve model |
| `/v1/models/{model_id}` | DELETE | Delete model |
| `/v1/embeddings` | POST | Create embedding |
| `/v1/images/generations` | POST | Generate image |
| `/v1/images/edits` | POST | Edit image |
| `/v1/images/variations` | POST | Create variations |
| `/v1/audio/transcriptions` | POST | Transcribe audio |
| `/v1/audio/translations` | POST | Translate audio |
| `/v1/audio/speech` | POST | Text to speech |
| `/v1/files` | POST | Upload file |
| `/v1/files` | GET | List files |
| `/v1/files/{file_id}` | GET | Retrieve file |
| `/v1/files/{file_id}` | DELETE | Delete file |
| `/v1/files/{file_id}/content` | GET | Download file |
| `/v1/webhooks` | POST | Register webhook |
| `/v1/webhooks` | GET | List webhooks |
| `/v1/webhooks/{webhook_id}` | DELETE | Delete webhook |

### Supported Models

| Model | Type | Max Context |
|-------|------|-------------|
| grok-4-5 | Chat, Vision | 128K |
| grok-4-1 | Chat, Vision | 32K |
| grok-4-1-fast | Chat, Vision | 32K |
| grok-4 | Chat, Vision | 32K |
| grok-4-fast | Chat, Vision | 32K |
| grok-4-heavy | Chat, Vision | 32K |
| grok-3 | Chat, Vision | 131K |
| grok-3-fast | Chat, Vision | 131K |
| grok-3-mini | Chat | 131K |
| grok-embedding-v1 | Embedding | N/A |
| grok-image-v1 | Image | N/A |
| grok-audio-v1 | Audio | N/A |
| grok-tts-v1 | TTS | N/A |

---

## References

- Full API Documentation: https://docs.x.ai
- OpenAPI Spec: https://docs.x.ai/openapi
- Status Page: https://status.x.ai
- Support: https://support.x.ai

---

*Last updated: 2026-07-23 | Version 1.0.0*
