---
name: Grok-3 Mini
model_id: grok-3-mini
provider: xAI
context_window: 131072
max_output: 32768
release_date: 2024-12-13
pricing:
  input: $0.50 / 1M tokens
  output: $2.00 / 1M tokens
  notes: "Lightweight tier with excellent value"
tags:
  - lightweight
  - cost-efficient
  - fast
  - text-generation
  - high-volume
deprecated: false
status: current
---

# Grok-3 Mini

## Overview

Grok-3 Mini is xAI's lightweight, cost-efficient model that delivers impressive performance at a fraction of the cost of larger models. Released alongside Grok-3 in December 2024, Grok-3 Mini maintains the same 131K token context window while offering significantly faster inference and lower costs. It's the ideal choice for high-volume applications, prototyping, and tasks that don't require the full power of the flagship Grok-3 model.

The model achieves remarkable performance on standard benchmarks while being optimized for speed and efficiency. Grok-3 Mini retains the core characteristics of the Grok family—real-time knowledge access, honest responses, and conversational ability—while being practical for production deployments at scale.

Grok-3 Mini is particularly well-suited for applications requiring quick responses, batch processing, and cost-sensitive deployments. Its combination of performance, speed, and affordability makes it a compelling choice for developers and businesses alike.

## Key Features

- **Cost-Efficient**: 83-87% cheaper than Grok-3
- **Fast Inference**: Optimized for low-latency responses
- **Large Context**: Same 131K token context as Grok-3
- **Real-Time Access**: Integration with X platform data
- **Production-Ready**: Optimized for high-volume deployments
- **API Compatible**: Drop-in replacement for Grok-3 in most cases
- **Text Generation**: Excellent for conversational and analytical tasks
- **Batch Processing**: Ideal for bulk content processing
- **No Vision**: Text-only model (use Grok-3 for image analysis)

## Technical Specifications

| Specification | Value |
|---------------|-------|
| Model Type | Mixture of Experts (MoE) - Optimized |
| Total Parameters | ~200 billion |
| Active Parameters | ~55 billion (per inference) |
| Context Window | 131,072 tokens |
| Max Output Tokens | 32,768 tokens |
| Modalities | Text only |
| Architecture | Optimized Transformer with MoE |
| Training Data | Web, X platform, Books, Code |
| License | Proprietary (API access) |
| Precision | BF16, INT8, INT4 supported |
| GPU Memory Required | 300-600 GB |
| Inference Framework | xAI proprietary, vLLM |
| Knowledge Cutoff | Late 2024 |
| API Endpoint | api.x.ai/v1 |
| Typical Latency | 150-400ms (first token) |

## Benchmark Performance

### Standard Benchmarks

| Benchmark | Grok-3 Mini | Grok-3 | GPT-4o Mini |
|-----------|-------------|--------|-------------|
| MMLU (5-shot) | 85.2% | 92.7% | 82.0% |
| HumanEval (pass@1) | 86.4% | 94.2% | 87.2% |
| GSM8K (8-shot) | 89.7% | 96.8% | 93.2% |
| MATH (4-shot) | 62.8% | 82.4% | 70.2% |
| ARC-Challenge | 93.1% | 97.3% | 93.7% |
| HellaSwag | 94.8% | 97.1% | 94.8% |
| TriviaQA | 88.2% | 92.4% | 85.4% |
| WinoGrande | 89.7% | 93.8% | 87.1% |

### Speed Benchmarks

| Metric | Grok-3 Mini | Grok-3 | Improvement |
|--------|-------------|--------|-------------|
| Time to First Token | 150-400ms | 500-1000ms | 2-3x faster |
| Tokens per Second | 100-160 | 50-80 | 2x faster |
| Throughput (tokens/min) | 6000-9600 | 3000-4800 | 2x higher |
| Latency (P95) | 600ms | 2000ms | 3x lower |

### Cost-Performance Analysis

| Metric | Grok-3 Mini | Grok-3 | Value |
|--------|-------------|--------|-------|
| Cost per 1M tokens (avg) | $1.25 | $9.00 | 7x cheaper |
| Performance (MMLU) | 85.2% | 92.7% | 92% of Grok-3 |
| Cost per Performance Point | $0.015 | $0.097 | 6.5x better value |

### Code Generation

| Benchmark | Grok-3 Mini | Grok-3 | Notes |
|-----------|-------------|--------|-------|
| HumanEval | 86.4% | 94.2% | Strong code generation |
| HumanEval+ | 80.1% | 90.1% | Good debugging |
| MBPP | 82.7% | 92.3% | Solid algorithmic skills |
| Simple Scripts | 97% | 99% | Excellent for basic tasks |
| Complex Systems | 75% | 90% | Use Grok-3 for complex code |

## API Configuration

### Basic API Usage

```python
import requests
import json
from typing import List, Dict, Optional

class Grok3MiniClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.x.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def chat(self, messages: List[Dict], 
             temperature: float = 0.7,
             max_tokens: int = 4096) -> Dict:
        """Send chat completion request."""
        payload = {
            "model": "grok-3-mini",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            json=payload
        )
        return response.json()
    
    def fast_chat(self, prompt: str, 
                  temperature: float = 0.3) -> str:
        """Quick single-turn chat for fast responses."""
        messages = [{"role": "user", "content": prompt}]
        response = self.chat(messages, temperature=temperature, max_tokens=1024)
        return response["choices"][0]["message"]["content"]

# Usage
client = Grok3MiniClient("your-api-key")

# Fast single-turn response
response = client.fast_chat("What is Python?")
print(response)

# Multi-turn conversation
response = client.chat([
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain REST APIs."}
])
print(response["choices"][0]["message"]["content"])
```

### Streaming Responses

```python
def stream_chat(client: Grok3MiniClient, messages: List[Dict]):
    """Stream responses for real-time output."""
    payload = {
        "model": "grok-3-mini",
        "messages": messages,
        "stream": True
    }
    
    response = requests.post(
        f"{client.base_url}/chat/completions",
        headers=client.headers,
        json=payload,
        stream=True
    )
    
    full_response = []
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: ') and line != 'data: [DONE]':
                data = json.loads(line[6:])
                if data['choices'][0]['delta'].get('content'):
                    content = data['choices'][0]['delta']['content']
                    print(content, end='', flush=True)
                    full_response.append(content)
    print()
    return ''.join(full_response)

# Usage
response = stream_chat(client, [
    {"role": "user", "content": "Write a short poem about coding."}
])
```

### Batch Processing

```python
import asyncio
import aiohttp
from typing import List, Dict

class Grok3MiniBatch:
    def __init__(self, api_key: str, max_concurrent: int = 20):
        self.api_key = api_key
        self.base_url = "https://api.x.ai/v1"
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_single(self, session: aiohttp.ClientSession, 
                            messages: List[Dict]) -> Dict:
        async with self.semaphore:
            payload = {
                "model": "grok-3-mini",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1024
            }
            
            async with session.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=payload
            ) as response:
                return await response.json()
    
    async def process_batch(self, batch: List[List[Dict]]) -> List[Dict]:
        async with aiohttp.ClientSession() as session:
            tasks = [self.process_single(session, msgs) for msgs in batch]
            return await asyncio.gather(*tasks)

# Usage
async def main():
    batch_processor = Grok3MiniBatch("your-api-key", max_concurrent=20)
    
    batch = [
        [{"role": "user", "content": f"Summarize topic {i}"}]
        for i in range(100)
    ]
    
    results = await batch_processor.process_batch(batch)
    print(f"Processed {len(results)} requests")

asyncio.run(main())
```

### Function Calling

```python
def grok_mini_with_tools(client: Grok3MiniClient, prompt: str):
    """Use function calling with Grok-3 Mini."""
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "Perform mathematical calculations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "Math expression to evaluate"
                        }
                    },
                    "required": ["expression"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search",
                "description": "Search for information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"}
                    },
                    "required": ["query"]
                }
            }
        }
    ]
    
    messages = [{"role": "user", "content": prompt}]
    response = client.chat(messages, tools=tools)
    return response

# Usage
response = grok_mini_with_tools(
    client,
    "What's 15% of 2847? Also search for current exchange rates."
)
```

## Pricing

### API Pricing (xAI)

| Model | Input Tokens | Output Tokens | Per 1M Tokens |
|-------|-------------|---------------|---------------|
| Grok-3 Mini | Input | - | $0.50 |
| Grok-3 Mini | Output | - | $2.00 |
| Grok-3 Mini | Batch Input | - | $0.25 |
| Grok-3 Mini | Batch Output | - | $1.00 |

### Cost Comparison

| Provider | Model | Input/1M | Output/1M | Notes |
|----------|-------|----------|-----------|-------|
| xAI | Grok-3 Mini | $0.50 | $2.00 | Best value |
| OpenAI | GPT-4o Mini | $0.15 | $0.60 | Cheapest |
| OpenAI | GPT-3.5 Turbo | $0.50 | $1.50 | Higher output cost |
| Anthropic | Claude 3 Haiku | $0.25 | $1.25 | Higher output cost |
| Google | Gemini 1.5 Flash | $0.075 | $0.30 | Cheapest |

### Cost Scenarios

```python
def calculate_monthly_cost(daily_requests: int, 
                          avg_input_tokens: int = 500,
                          avg_output_tokens: int = 300,
                          batch_percentage: float = 0.0):
    """Calculate monthly cost based on usage patterns."""
    
    # Standard pricing
    input_rate = 0.50 / 1_000_000
    output_rate = 2.00 / 1_000_000
    
    # Batch pricing (50% discount)
    batch_input_rate = 0.25 / 1_000_000
    batch_output_rate = 1.00 / 1_000_000
    
    monthly_requests = daily_requests * 30
    standard_requests = int(monthly_requests * (1 - batch_percentage))
    batch_requests = int(monthly_requests * batch_percentage)
    
    # Standard costs
    standard_input = standard_requests * avg_input_tokens * input_rate
    standard_output = standard_requests * avg_output_tokens * output_rate
    
    # Batch costs
    batch_input = batch_requests * avg_input_tokens * batch_input_rate
    batch_output = batch_requests * avg_output_tokens * batch_output_rate
    
    total = standard_input + standard_output + batch_input + batch_output
    
    return {
        "monthly_requests": monthly_requests,
        "standard_requests": standard_requests,
        "batch_requests": batch_requests,
        "standard_cost": f"${standard_input + standard_output:.2f}",
        "batch_cost": f"${batch_input + batch_output:.2f}",
        "total_monthly": f"${total:.2f}",
        "cost_per_request": f"${total / monthly_requests:.6f}"
    }

# Examples
print("Low volume (100 req/day):")
print(calculate_monthly_cost(100))
print("\nMedium volume (1000 req/day):")
print(calculate_monthly_cost(1000, batch_percentage=0.5))
print("\nHigh volume (10000 req/day):")
print(calculate_monthly_cost(10000, batch_percentage=0.7))
```

### Break-Even Analysis

| Daily Requests | Grok-3 Mini Cost | Grok-3 Cost | Savings |
|---------------|------------------|-------------|---------|
| 100 | $7.50 | $90.00 | $82.50 (92%) |
| 1,000 | $75.00 | $900.00 | $825.00 (92%) |
| 10,000 | $750.00 | $9,000.00 | $8,250.00 (92%) |
| 100,000 | $7,500.00 | $90,000.00 | $82,500.00 (92%) |

## Best Use Cases

### 1. High-Volume Chat Applications

```python
class ChatApplication:
    def __init__(self, api_key: str):
        self.client = Grok3MiniClient(api_key)
    
    def handle_message(self, user_message: str, 
                      conversation_history: list) -> str:
        """Handle chat messages efficiently."""
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            *conversation_history[-10:],  # Keep last 10 messages
            {"role": "user", "content": user_message}
        ]
        
        response = self.client.chat(
            messages,
            temperature=0.7,
            max_tokens=1024  # Reasonable limit for chat
        )
        return response["choices"][0]["message"]["content"]

# Cost-effective for millions of messages
```

**Why Grok-3 Mini**: Low cost per request makes it ideal for high-volume applications.

### 2. Content Classification and Tagging

```python
def classify_content_batch(client: Grok3MiniClient, 
                          content_batch: list) -> list:
    """Classify large batches of content efficiently."""
    
    classifications = []
    for content in content_batch:
        response = client.fast_chat(
            f"""Classify this content into one of these categories:
            [Technology, Business, Science, Entertainment, Sports, Politics]
            
            Content: {content}
            
            Return ONLY the category name."""
        )
        classifications.append(response.strip())
    
    return classifications

# Process thousands of articles efficiently
```

**Why Grok-3 Mini**: Fast inference and low cost for bulk processing.

### 3. Rapid Prototyping

```python
def prototype_feature(api_key: str, feature_description: str):
    """Quickly prototype a new feature using Grok-3 Mini."""
    
    client = Grok3MiniClient(api_key)
    
    # Generate code quickly
    response = client.fast_chat(
        f"""Write Python code for this feature:
        {feature_description}
        
        Include error handling and basic tests."""
    )
    
    return response

# Fast iteration at low cost
```

**Why Grok-3 Mini**: Quick responses and low cost enable rapid experimentation.

### 4. Customer Support Automation

```python
class SupportBot:
    def __init__(self, api_key: str, knowledge_base: str):
        self.client = Grok3MiniClient(api_key)
        self.knowledge_base = knowledge_base
    
    def answer_question(self, question: str) -> str:
        """Answer customer questions quickly."""
        
        response = self.client.fast_chat(
            f"""Answer this customer question using the knowledge base.
            
            Knowledge Base:
            {self.knowledge_base}
            
            Question: {question}
            
            Be helpful and concise."""
        )
        return response

# Cost-effective for thousands of daily support tickets
```

**Why Grok-3 Mini**: Fast responses keep customers happy, low costs keep budgets happy.

### 5. Data Extraction and Processing

```python
def extract_data_batch(client: Grok3MiniClient, 
                      raw_data_batch: list) -> list:
    """Extract structured data from unstructured text."""
    
    results = []
    for raw_text in raw_data_batch:
        response = client.fast_chat(
            f"""Extract the following fields from this text and return as JSON:
            - name
            - date
            - amount
            - category
            
            Text: {raw_text}"""
        )
        results.append(response)
    
    return results

# Process thousands of documents efficiently
```

**Why Grok-3 Mini**: Cost-efficient for large-scale data processing.

## Limitations and Considerations

### Technical Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| No vision capabilities | Cannot analyze images | Use Grok-3 for image tasks |
| ~200B parameters | Less capable than Grok-3 | Use Grok-3 for complex reasoning |
| Text-only | No multimodal support | Combine with specialized models |
| Rate limits | May affect very high volume | Implement queuing |
| No extended thinking | Limited complex reasoning | Use Grok-3 for deep analysis |

### Performance Considerations

1. **Reasoning Depth**: May struggle with very complex multi-step problems
2. **Code Complexity**: Better for simple to moderate code, use Grok-3 for complex systems
3. **Nuance**: May miss subtle nuances in very complex analyses
4. **Consistency**: Output quality may vary more than larger models

### When NOT to Use Grok-3 Mini

- **Complex reasoning tasks**: Use Grok-3
- **Image analysis**: Use Grok-3
- **Critical applications**: Consider Grok-3 for highest accuracy
- **Deep analysis**: Use Grok-3 for thorough reasoning

### Cost vs Quality Trade-offs

| Task Type | Recommended Model | Reason |
|-----------|-------------------|--------|
| Simple Q&A | Grok-3 Mini | Cost-effective |
| Classification | Grok-3 Mini | Fast and cheap |
| Complex Analysis | Grok-3 | Better accuracy |
| Code Review | Grok-3 | Better understanding |
| Creative Writing | Grok-3 Mini or Grok-3 | Depends on quality needs |
| Research | Grok-3 | Better synthesis |

## Migration Guide

### From Grok-3 to Grok-3 Mini

```python
# Grok-3 (Before)
response = client.chat(
    messages,
    model="grok-3",
    temperature=0.7
)

# Grok-3 Mini (After) - Same interface, lower cost
response = client.chat(
    messages,
    model="grok-3-mini",
    temperature=0.7
)
```

**Key Changes**:
- Model identifier: `grok-3` → `grok-3-mini`
- Cost: ~83-87% reduction
- Speed: ~2-3x faster
- Quality: Slight reduction for complex tasks

### From GPT-3.5 Turbo to Grok-3 Mini

```python
# OpenAI (Before)
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
)

# Grok-3 Mini (After)
response = client.chat(messages, model="grok-3-mini")
```

**Migration Considerations**:
- Similar pricing structure
- Better context window (131K vs 16K)
- Real-time knowledge access
- Similar performance level

### From Grok-2-mini to Grok-3 Mini

```python
# Grok-2-mini (Before)
response = client.chat(
    messages,
    model="grok-2-mini",
    temperature=0.7
)

# Grok-3 Mini (After) - Better performance at similar cost
response = client.chat(
    messages,
    model="grok-3-mini",
    temperature=0.7
)
```

**Migration Considerations**:
- Model identifier: `grok-2-mini` → `grok-3-mini`
- Slightly higher cost but better performance
- Same context window
- Improved reasoning capabilities

### Migration Checklist

- [ ] Update model identifier to `grok-3-mini`
- [ ] Verify prompt format compatibility
- [ ] Test output quality on representative tasks
- [ ] Benchmark latency requirements
- [ ] Calculate cost savings
- [ ] Update monitoring and logging
- [ ] Train team on differences
- [ ] Set up fallback to Grok-3 if needed

## Additional Resources

- **API Documentation**: [docs.x.ai](https://docs.x.ai)
- **Model Card**: [xAI/grok-3-mini-card](https://x.ai/grok-3-mini-card)
- **Pricing Calculator**: [x.ai/pricing](https://x.ai/pricing)
- **Community**: X platform developer community
- **Support**: support@x.ai

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.0.0-mini | 2024-12-13 | Initial release |
| 3.0.1-mini | 2025-01-05 | Performance optimizations |
| 3.0.2-mini | 2025-01-20 | Reduced latency |

---

*Last updated: July 2026*
*Maintained by: xAI*