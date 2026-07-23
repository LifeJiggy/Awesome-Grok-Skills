---
name: Grok-1.5
model_id: grok-1.5
provider: xAI
context_window: 16384
max_output: 8192
release_date: 2024-03-26
pricing:
  input: $0.50 / 1M tokens
  output: $1.50 / 1M tokens
  notes: "Available via xAI API"
tags:
  - api
  - reasoning
  - improved
  - text-generation
  - extended-context
deprecated: false
status: current
---

# Grok-1.5

## Overview

Grok-1.5 represents a significant evolution in xAI's language model lineup, released in March 2024 as the successor to the original Grok-1. This iteration delivers substantial improvements across multiple dimensions: doubled context window, enhanced reasoning capabilities, improved code generation, and stronger performance on mathematical tasks. Grok-1.5 bridges the gap between the foundational Grok-1 and the more advanced Grok-2, offering a balanced combination of performance and accessibility.

The model builds upon Grok-1's Mixture of Experts architecture while introducing refined training techniques that improve both accuracy and efficiency. Grok-1.5 maintains the core philosophy of truth-seeking and minimal filtering while adding more sophisticated safety measures where necessary. The extended 16K context window enables the model to handle longer documents and more complex multi-turn conversations, addressing one of the primary limitations of its predecessor.

Grok-1.5 is available both through the xAI API and as an open-weight model for self-hosting, providing flexibility for different deployment scenarios and use cases.

## Key Features

- **Extended Context Window**: 16,384 tokens, double the capacity of Grok-1
- **Enhanced Reasoning**: Improved logical reasoning and problem-solving capabilities
- **Better Code Generation**: Significant improvements in coding tasks and debugging
- **Mathematical Proficiency**: Stronger performance on mathematical reasoning
- **Improved Efficiency**: Better performance-per-parameter ratio
- **API Access**: Available via xAI's API with competitive pricing
- **Open Weights**: Model weights available for self-hosting
- **Real-Time Knowledge**: Continued integration with X platform data
- **Multi-Turn Excellence**: Improved conversation coherence and context retention

## Technical Specifications

| Specification | Value |
|---------------|-------|
| Model Type | Mixture of Experts (MoE) |
| Total Parameters | 314 billion |
| Active Parameters | ~86 billion (per inference) |
| Context Window | 16,384 tokens |
| Max Output Tokens | 8,192 tokens |
| Architecture | Enhanced Transformer with MoE |
| Training Data | Expanded web + X platform corpus |
| License | Apache 2.0 (open weights) / API Terms |
| Precision | BF16, INT8, INT4 supported |
| GPU Memory Required | 320-640 GB (depending on quantization) |
| Inference Framework | JAX, PyTorch, vLLM, TGI |
| Knowledge Cutoff | Early 2024 |
| API Endpoint | api.x.ai/v1 |

## Benchmark Performance

### Standard Benchmarks

| Benchmark | Grok-1.5 | Grok-1 | GPT-4 Turbo |
|-----------|----------|--------|-------------|
| MMLU (5-shot) | 81.2% | 73.0% | 86.4% |
| HumanEval (pass@1) | 74.1% | 63.2% | 67.0% |
| GSM8K (8-shot) | 78.5% | 62.9% | 92.0% |
| MATH (4-shot) | 38.7% | 23.9% | 42.5% |
| ARC-Challenge | 82.3% | 68.7% | 96.3% |
| HellaSwag | 89.7% | 85.0% | 95.3% |
| TriviaQA | 81.4% | 75.2% | 82.1% |
| WinoGrande | 84.2% | 79.8% | 87.5% |

### Code Generation Benchmarks

| Benchmark | Grok-1.5 | Improvement over Grok-1 |
|-----------|----------|------------------------|
| HumanEval | 74.1% | +10.9% |
| HumanEval+ | 68.3% | +12.1% |
| MBPP | 72.8% | +15.4% |
| MBPP+ | 67.2% | +14.8% |
| CodeContests | 31.2% | +8.7% |

### Mathematical Benchmarks

| Benchmark | Grok-1.5 | Improvement over Grok-1 |
|-----------|----------|------------------------|
| GSM8K | 78.5% | +15.6% |
| MATH | 38.7% | +14.8% |
| Minerva Math | 45.2% | +11.3% |
| AQuA-RAT | 62.8% | +9.4% |
| SVAMP | 79.1% | +12.7% |

### Reasoning Tasks

| Task | Grok-1.5 Performance | Notes |
|------|---------------------|-------|
| Logical Deduction | Strong | Improved chain-of-thought |
| Causal Reasoning | Above Average | Better multi-step analysis |
| Analogical Reasoning | Strong | Enhanced pattern recognition |
| Spatial Reasoning | Moderate | Room for improvement |
| Temporal Reasoning | Above Average | Better time-related queries |

## API Configuration

### Basic API Usage

```python
import requests
import json

# xAI API Configuration
API_KEY = "your-xai-api-key"
BASE_URL = "https://api.x.ai/v1"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Chat completion request
def grok_chat(messages, model="grok-1.5", temperature=0.7):
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 4096
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json=payload
    )
    return response.json()

# Example usage
messages = [
    {"role": "system", "content": "You are a helpful coding assistant."},
    {"role": "user", "content": "Write a Python function to find prime numbers."}
]

response = grok_chat(messages)
print(response["choices"][0]["message"]["content"])
```

### Streaming Responses

```python
import requests
import json

def grok_stream(messages, model="grok-1.5"):
    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "temperature": 0.7
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json=payload,
        stream=True
    )
    
    for line in response.iter_lines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data: '):
                data = json.loads(line[6:])
                if data['choices'][0]['delta'].get('content'):
                    print(data['choices'][0]['delta']['content'], end='')
    print()

# Usage
messages = [{"role": "user", "content": "Explain quantum computing."}]
grok_stream(messages)
```

### Function Calling

```python
import json

def grok_with_tools(messages, tools=None):
    payload = {
        "model": "grok-1.5",
        "messages": messages,
        "tools": tools or [
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
        ],
        "tool_choice": "auto"
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers=headers,
        json=payload
    )
    return response.json()

# Example
messages = [{"role": "user", "content": "What's the weather in San Francisco?"}]
response = grok_with_tools(messages)
```

### Self-Hosted Deployment

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model with quantization for efficiency
model_name = "xAI/grok-1.5"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    load_in_8bit=True  # Enable 8-bit quantization
)

def generate_response(prompt, max_tokens=2048):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Example
response = generate_response("Explain the difference between TCP and UDP.")
print(response)
```

## Pricing

### API Pricing (xAI)

| Model | Input Tokens | Output Tokens | Per 1M Tokens |
|-------|-------------|---------------|---------------|
| Grok-1.5 | Input | - | $0.50 |
| Grok-1.5 | Output | - | $1.50 |
| Grok-1.5 | Batch Input | - | $0.25 |
| Grok-1.5 | Batch Output | - | $0.75 |

### Cost Comparison

| Provider | Model | Input/1M | Output/1M | Context |
|----------|-------|----------|-----------|---------|
| xAI | Grok-1.5 | $0.50 | $1.50 | 16K |
| OpenAI | GPT-4 Turbo | $10.00 | $30.00 | 128K |
| OpenAI | GPT-4 | $30.00 | $60.00 | 8K |
| Anthropic | Claude 3 Haiku | $0.25 | $1.25 | 200K |
| Google | Gemini 1.5 Pro | $1.25 | $5.00 | 1M |

### Self-Hosting Costs

| Configuration | Hardware | Est. Hourly Cost | Monthly (24/7) |
|--------------|----------|------------------|----------------|
| Minimum | 4x A100 80GB | ~$12 | ~$8,640 |
| Recommended | 8x A100 80GB | ~$24 | ~$17,280 |
| High Performance | 8x H100 80GB | ~$40 | ~$28,800 |

### Cost Optimization Tips

1. **Use Batch API**: 50% discount for non-urgent requests
2. **Implement Caching**: Cache common responses to reduce API calls
3. **Optimize Prompts**: Shorter, more focused prompts reduce input tokens
4. **Use Streaming**: For better user experience and token efficiency

## Best Use Cases

### 1. Complex Document Analysis

```python
# Analyze long documents with extended context
document = """[Long document content - up to 16K tokens]"""

messages = [
    {"role": "system", "content": "Analyze the provided document thoroughly."},
    {"role": "user", "content": f"Summarize the key points and provide recommendations:\n\n{document}"}
]

response = grok_chat(messages)
```

**Why Grok-1.5**: Extended context window handles full documents without chunking.

### 2. Code Generation and Debugging

```python
# Complex code generation with context
messages = [
    {"role": "system", "content": "You are an expert Python developer."},
    {"role": "user", "content": """
    Write a complete REST API with:
    - User authentication (JWT)
    - CRUD operations for products
    - Database integration (PostgreSQL)
    - Unit tests
    - Docker configuration
    """}
]

response = grok_chat(messages)
```

**Why Grok-1.5**: Improved code generation and ability to maintain context across large codebases.

### 3. Mathematical Problem Solving

```python
# Advanced mathematical reasoning
messages = [
    {"role": "user", "content": """
    Solve this step by step:
    A company has 100 employees. 60% work in engineering, 
    25% in marketing, and the rest in HR. If 10% of engineers 
    are promoted and 5% of marketers are promoted, what is 
    the total percentage of employees promoted?
    """}
]

response = grok_chat(messages)
```

**Why Grok-1.5**: Enhanced mathematical reasoning with clear step-by-step explanations.

### 4. Research and Analysis

```python
# Multi-source research synthesis
messages = [
    {"role": "user", "content": """
    Based on current information, analyze the following topics:
    1. Latest developments in renewable energy
    2. Impact of AI on healthcare
    3. Cryptocurrency market trends
    
    Provide citations and evidence-based conclusions.
    """}
]

response = grok_chat(messages)
```

**Why Grok-1.5**: Real-time knowledge access and improved reasoning capabilities.

### 5. Educational Content Creation

```python
# Create comprehensive educational materials
messages = [
    {"role": "system", "content": "Create educational content for computer science students."},
    {"role": "user", "content": """
    Create a comprehensive tutorial on data structures covering:
    - Arrays and Linked Lists
    - Trees and Graphs
    - Hash Tables
    - Sorting Algorithms
    Include code examples, visualizations descriptions, and practice problems.
    """}
]

response = grok_chat(messages)
```

**Why Grok-1.5**: Extended context allows comprehensive content creation in single responses.

## Limitations and Considerations

### Technical Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| 16K context | Still limited for very long documents | Use document summarization |
| MoE architecture | Higher memory than dense models | Use quantization |
| API rate limits | May affect high-volume applications | Implement queuing |
| No multimodal | Text-only interactions | Combine with vision APIs |
| Knowledge cutoff | May miss very recent events | Leverage real-time data |

### Performance Considerations

1. **Latency**: Self-hosted deployment may have higher latency than API
2. **Throughput**: Batch processing recommended for high-volume tasks
3. **Consistency**: Temperature settings significantly affect output variation
4. **Resource Usage**: Monitoring recommended for production deployments

### Ethical Considerations

1. **Content Safety**: Minimal filtering requires external safety measures
2. **Bias Awareness**: May reflect biases in training data
3. **Misinformation**: Real-time data doesn't guarantee accuracy
4. **Privacy**: Handle user data responsibly when using API

### Known Issues

1. **Hallucination**: May generate plausible but incorrect information
2. **Context Drift**: May lose focus in very long conversations
3. **Inconsistent Formatting**: Output format may vary between runs
4. **Token Efficiency**: Some prompts may use more tokens than expected

## Migration Guide

### From Grok-1 to Grok-1.5

```python
# Grok-1 (Old)
import requests

response = requests.post(
    "https://api.x.ai/v1/chat/completions",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "grok-1",
        "messages": messages,
        "max_tokens": 4096  # Limited output
    }
)

# Grok-1.5 (New)
response = requests.post(
    "https://api.x.ai/v1/chat/completions",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "grok-1.5",
        "messages": messages,
        "max_tokens": 8192  # Doubled output capacity
    }
)
```

**Key Changes**:
- Model identifier: `grok-1` → `grok-1.5`
- Context window: 8K → 16K tokens
- Max output: 4K → 8K tokens
- Improved accuracy across all benchmarks

### From OpenAI to Grok-1.5

```python
# OpenAI (Before)
import openai

openai.api_key = "your-openai-key"
response = openai.ChatCompletion.create(
    model="gpt-4-turbo-preview",
    messages=messages,
    max_tokens=4096
)

# Grok-1.5 (After)
import requests

XAI_API_KEY = "your-xai-key"
response = requests.post(
    "https://api.x.ai/v1/chat/completions",
    headers={"Authorization": f"Bearer {XAI_API_KEY}"},
    json={
        "model": "grok-1.5",
        "messages": messages,
        "max_tokens": 4096
    }
)
```

**Migration Considerations**:
- Different API endpoint structure
- Pricing comparison (typically lower cost)
- Similar message format
- Real-time knowledge advantage

### From Other Models to Grok-1.5

#### Migration Checklist

- [ ] Update API endpoint to `api.x.ai/v1`
- [ ] Update model identifier to `grok-1.5`
- [ ] Verify prompt format compatibility
- [ ] Test output quality on representative tasks
- [ ] Implement error handling for new API
- [ ] Update monitoring and logging
- [ ] Review pricing and cost projections
- [ ] Train team on new capabilities

#### Prompt Format Differences

```python
# Some models use different message structures
# Grok-1.5 uses OpenAI-compatible format

# System message (optional but recommended)
{"role": "system", "content": "You are a helpful assistant."}

# User message
{"role": "user", "content": "Your question here"}

# Assistant message (for multi-turn)
{"role": "assistant", "content": "Previous response"}

# Tool/Function results
{"role": "tool", "content": "Function output"}
```

### Performance Optimization

```python
# Optimize for Grok-1.5's strengths
optimized_config = {
    "model": "grok-1.5",
    "temperature": 0.7,  # Balanced creativity/accuracy
    "top_p": 0.9,        # Nucleus sampling
    "max_tokens": 4096,  # Adjust based on needs
    "stream": True,      # Better user experience
    "presence_penalty": 0.1,  # Reduce repetition
    "frequency_penalty": 0.1
}
```

## Additional Resources

- **API Documentation**: [docs.x.ai](https://docs.x.ai)
- **GitHub**: [xAI/grok-1.5](https://github.com/xai-org/grok-1.5)
- **Hugging Face**: [xAI/grok-1.5](https://huggingface.co/xai/grok-1.5)
- **Community Forum**: X platform developer community
- **Support**: support@x.ai

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.5.0 | 2024-03-26 | Initial release with 16K context |
| 1.5.1 | 2024-04-15 | Bug fixes and performance improvements |
| 1.5.2 | 2024-05-01 | Enhanced code generation capabilities |

---

*Last updated: July 2026*
*Maintained by: xAI*