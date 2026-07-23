---
name: Grok-3
model_id: grok-3
provider: xAI
context_window: 131072
max_output: 32768
release_date: 2024-12-13
pricing:
  input: $3.00 / 1M tokens
  output: $15.00 / 1M tokens
  notes: "Frontier reasoning model with extended output"
tags:
  - frontier
  - reasoning
  - multimodal
  - vision
  - extended-output
  - highest-capability
deprecated: false
status: current
---

# Grok-3

## Overview

Grok-3 represents xAI's most capable language model to date, released in December 2024 as a significant leap forward in AI reasoning capabilities. This frontier model combines advanced chain-of-thought reasoning, native multimodal understanding, and an unprecedented 32K token output capacity. Grok-3 achieves state-of-the-art performance on numerous benchmarks while maintaining the distinctive Grok personality and real-time knowledge access.

The architecture introduces several innovations including enhanced attention mechanisms, improved reasoning chains, and a refined mixture-of-experts system that maximizes both performance and efficiency. Grok-3 excels at complex problem-solving, scientific reasoning, code generation, and creative tasks that require deep understanding and extended output.

Grok-3 is positioned as xAI's premium offering, competing with and often surpassing the most advanced models from OpenAI, Anthropic, and Google. Its combination of reasoning depth, context length, output capacity, and real-time knowledge makes it the ideal choice for applications requiring the highest level of AI capability.

## Key Features

- **Frontier Reasoning**: State-of-the-art chain-of-thought and logical reasoning
- **Extended Output**: 32K token maximum output for comprehensive responses
- **Native Multimodal**: Advanced text and image understanding
- **Massive Context**: 131K token context window
- **Real-Time Access**: Enhanced integration with X platform and web data
- **Scientific Reasoning**: Exceptional performance on scientific and mathematical tasks
- **Code Mastery**: Best-in-class code generation and debugging
- **Extended Thinking**: Visible reasoning process for transparency
- **Personality**: Maintains engaging conversational style

## Technical Specifications

| Specification | Value |
|---------------|-------|
| Model Type | Mixture of Experts (MoE) - Frontier |
| Total Parameters | ~1 trillion |
| Active Parameters | ~270 billion (per inference) |
| Context Window | 131,072 tokens |
| Max Output Tokens | 32,768 tokens |
| Modalities | Text, Image |
| Architecture | Next-gen Transformer with Advanced MoE |
| Training Data | Web, X platform, Books, Code, Scientific papers, Images |
| License | Proprietary (API access) |
| Precision | BF16, FP8, INT4 supported |
| GPU Memory Required | 1.5-3 TB |
| Inference Framework | xAI proprietary |
| Knowledge Cutoff | Late 2024 |
| API Endpoint | api.x.ai/v1 |
| Vision Encoder | Advanced multimodal encoder |
| Reasoning Mode | Extended thinking with visible chains |

## Benchmark Performance

### Standard Benchmarks

| Benchmark | Grok-3 | Grok-2 | GPT-4o | Claude 3.5 Sonnet |
|-----------|--------|--------|--------|-------------------|
| MMLU (5-shot) | 92.7% | 87.5% | 88.7% | 88.7% |
| HumanEval (pass@1) | 94.2% | 88.4% | 90.2% | 92.0% |
| GSM8K (8-shot) | 96.8% | 92.1% | 95.8% | 96.4% |
| MATH (4-shot) | 82.4% | 68.2% | 76.6% | 71.1% |
| ARC-Challenge | 97.3% | 94.1% | 96.4% | 96.7% |
| HellaSwag | 97.1% | 95.8% | 95.3% | 95.4% |
| TriviaQA | 92.4% | 88.7% | 89.2% | 88.9% |
| WinoGrande | 93.8% | 89.3% | 87.5% | 89.0% |

### Reasoning Benchmarks

| Benchmark | Grok-3 | Grok-2 | GPT-4o | Claude 3.5 Sonnet |
|-----------|--------|--------|--------|-------------------|
| GPQA (Diamond) | 78.2% | 56.8% | 56.1% | 65.0% |
| ARC-AGI | 42.3% | 28.1% | 32.4% | 38.7% |
| MMMU (Val) | 71.4% | 56.8% | 69.1% | 68.3% |
| MATH-500 | 96.4% | 82.1% | 88.2% | 85.7% |
| AIME 2024 | 68.7% | 42.3% | 51.2% | 58.4% |
| Olympiad-level | 72.1% | 48.6% | 54.8% | 62.3% |

### Code Generation Benchmarks

| Benchmark | Grok-3 | Grok-2 | GPT-4o |
|-----------|--------|--------|--------|
| HumanEval | 94.2% | 88.4% | 90.2% |
| HumanEval+ | 90.1% | 82.1% | 84.5% |
| MBPP | 92.3% | 85.7% | 87.2% |
| MBPP+ | 87.8% | 79.3% | 81.8% |
| CodeContests | 65.4% | 48.6% | 52.1% |
| SWE-bench | 48.7% | 32.4% | 38.2% |
| LiveCodeBench | 71.2% | 52.8% | 58.4% |

### Scientific Reasoning

| Benchmark | Grok-3 | Grok-2 | GPT-4o |
|-----------|--------|--------|--------|
| GPQA Diamond | 78.2% | 56.8% | 56.1% |
| SciQ | 94.6% | 88.2% | 91.3% |
| ARC-Challenge | 97.3% | 94.1% | 96.4% |
| AI2 Reasoning | 95.8% | 89.4% | 92.1% |
| Scientific Papers QA | 88.4% | 76.2% | 82.7% |

## API Configuration

### Basic API Usage

```python
import requests
import json
from typing import List, Dict, Optional, Generator

class Grok3Client:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.x.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def chat(self, messages: List[Dict], 
             temperature: float = 0.7,
             max_tokens: int = 8192,
             thinking: bool = False) -> Dict:
        """Send chat completion request."""
        payload = {
            "model": "grok-3",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        if thinking:
            payload["thinking"] = {"type": "enabled", "budget_tokens": 4096}
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            json=payload
        )
        return response.json()
    
    def extended_thinking(self, messages: List[Dict], 
                         budget_tokens: int = 8192) -> Dict:
        """Use extended thinking for complex reasoning."""
        payload = {
            "model": "grok-3",
            "messages": messages,
            "thinking": {
                "type": "enabled",
                "budget_tokens": budget_tokens
            },
            "max_tokens": 16384
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            json=payload
        )
        return response.json()
    
    def chat_stream(self, messages: List[Dict], 
                   max_tokens: int = 4096) -> Generator[str, None, None]:
        """Stream chat responses."""
        payload = {
            "model": "grok-3",
            "messages": messages,
            "stream": True,
            "max_tokens": max_tokens
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            json=payload,
            stream=True
        )
        
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: ') and line != 'data: [DONE]':
                    data = json.loads(line[6:])
                    if data['choices'][0]['delta'].get('content'):
                        yield data['choices'][0]['delta']['content']

# Usage
client = Grok3Client("your-api-key")

# Basic chat
response = client.chat([
    {"role": "user", "content": "Explain quantum entanglement."}
])
print(response["choices"][0]["message"]["content"])

# Extended thinking for complex problems
response = client.extended_thinking([
    {"role": "user", "content": "Solve this step by step: ..."}
], budget_tokens=4096)
print(response["choices"][0]["message"]["content"])
```

### Extended Thinking Mode

```python
class Grok3Reasoning:
    def __init__(self, api_key: str):
        self.client = Grok3Client(api_key)
    
    def solve_with_reasoning(self, problem: str, 
                            show_thinking: bool = False) -> Dict:
        """Solve complex problems with visible reasoning."""
        
        messages = [
            {
                "role": "system",
                "content": """You are an expert problem solver. 
                Think through problems step by step, showing your reasoning.
                Be thorough and precise."""
            },
            {
                "role": "user",
                "content": problem
            }
        ]
        
        response = self.client.extended_thinking(
            messages,
            budget_tokens=8192
        )
        
        result = {
            "thinking": response["choices"][0]["message"].get("thinking", ""),
            "answer": response["choices"][0]["message"]["content"],
            "usage": response.get("usage", {})
        }
        
        if show_thinking:
            print("=== THINKING PROCESS ===")
            print(result["thinking"])
            print("\n=== FINAL ANSWER ===")
        
        return result

# Usage
reasoning = Grok3Reasoning("your-api-key")

result = reasoning.solve_with_reasoning("""
A ball is thrown vertically upward with initial velocity 20 m/s from a 
height of 1.5 meters. Assuming g = 9.8 m/s², find:
1. Maximum height reached
2. Time to reach maximum height
3. Time when ball hits the ground
4. Velocity just before impact

Show all work step by step.
""", show_thinking=True)

print(result["answer"])
```

### Vision with Extended Reasoning

```python
import base64
from pathlib import Path

class Grok3Vision:
    def __init__(self, api_key: str):
        self.client = Grok3Client(api_key)
    
    def analyze_complex_image(self, image_path: str, 
                             question: str,
                             use_thinking: bool = True) -> str:
        """Analyze images with extended reasoning."""
        
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        ext = Path(image_path).suffix.lower()
        media_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp"
        }
        media_type = media_types.get(ext, "image/jpeg")
        
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{media_type};base64,{image_data}"
                        }
                    },
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            }
        ]
        
        if use_thinking:
            response = self.client.extended_thinking(messages, budget_tokens=4096)
        else:
            response = self.client.chat(messages, max_tokens=4096)
        
        return response["choices"][0]["message"]["content"]

# Usage
vision = Grok3Vision("your-api-key")

# Analyze a scientific diagram
result = vision.analyze_complex_image(
    "circuit_diagram.png",
    """Analyze this circuit diagram:
    1. Identify all components
    2. Explain the circuit topology
    3. Calculate the expected output voltage
    4. Identify potential issues or improvements"""
)
print(result)
```

### Structured Output with Reasoning

```python
from pydantic import BaseModel
from typing import List, Optional
import json

class AnalysisResult(BaseModel):
    reasoning_steps: List[str]
    conclusion: str
    confidence: float
    supporting_evidence: List[str]
    potential_counterarguments: List[str]
    recommendations: List[str]

def structured_analysis_with_reasoning(client: Grok3Client, 
                                      analysis_request: str) -> AnalysisResult:
    """Perform structured analysis with visible reasoning."""
    
    system_prompt = """You are an expert analyst. Analyze the request and provide 
    structured output with your reasoning process visible.
    
    Return JSON with:
    - reasoning_steps: List of your reasoning steps
    - conclusion: Your main conclusion
    - confidence: 0-1 confidence level
    - supporting_evidence: Evidence supporting your conclusion
    - potential_counterarguments: Possible objections
    - recommendations: Action items based on your analysis"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": analysis_request}
    ]
    
    response = client.extended_thinking(messages, budget_tokens=4096)
    
    content = response["choices"][0]["message"]["content"]
    return AnalysisResult.parse_raw(content)

# Usage
analysis = structured_analysis_with_reasoning(
    client,
    """Analyze the potential impact of AI on healthcare in the next 5 years.
    Consider both positive and negative outcomes."""
)

print(f"Confidence: {analysis.confidence}")
print(f"Conclusion: {analysis.conclusion}")
```

## Pricing

### API Pricing (xAI)

| Model | Input Tokens | Output Tokens | Per 1M Tokens |
|-------|-------------|---------------|---------------|
| Grok-3 | Input | - | $3.00 |
| Grok-3 | Output | - | $15.00 |
| Grok-3 | Batch Input | - | $1.50 |
| Grok-3 | Batch Output | - | $7.50 |
| Grok-3 | Thinking Tokens | - | $3.00 (same as input) |

### Cost Comparison

| Provider | Model | Input/1M | Output/1M | Capabilities |
|----------|-------|----------|-----------|--------------|
| xAI | Grok-3 | $3.00 | $15.00 | Frontier reasoning |
| OpenAI | o1 | $15.00 | $60.00 | Reasoning model |
| OpenAI | GPT-4o | $2.50 | $10.00 | Multimodal |
| Anthropic | Claude 3.5 Sonnet | $3.00 | $15.00 | Strong reasoning |
| Google | Gemini 1.5 Pro | $1.25 | $5.00 | Long context |

### Extended Output Cost Analysis

```python
def estimate_extended_output_cost(input_tokens: int, 
                                  output_tokens: int,
                                  thinking_tokens: int = 0,
                                  model: str = "grok-3") -> dict:
    """Estimate cost for extended output requests."""
    
    # Pricing per million tokens
    rates = {
        "input": 3.00,
        "output": 15.00,
        "thinking": 3.00
    }
    
    input_cost = (input_tokens / 1_000_000) * rates["input"]
    output_cost = (output_tokens / 1_000_000) * rates["output"]
    thinking_cost = (thinking_tokens / 1_000_000) * rates["thinking"]
    
    total = input_cost + output_cost + thinking_cost
    
    return {
        "input_cost": f"${input_cost:.6f}",
        "output_cost": f"${output_cost:.6f}",
        "thinking_cost": f"${thinking_cost:.6f}",
        "total_cost": f"${total:.6f}",
        "cost_per_1k_output": f"${(rates['output'] * 1000) / 1_000_000:.6f}"
    }

# Example: 10K input, 8K output, 4K thinking
cost = estimate_extended_output_cost(10000, 8000, 4000)
print(f"Total cost: ${cost['total_cost']}")
```

### Self-Hosting Costs (Theoretical)

| Configuration | Hardware | Est. Hourly Cost | Monthly (24/7) |
|--------------|----------|------------------|----------------|
| Minimum | 32x H100 80GB | ~$160 | ~$115,200 |
| Recommended | 64x H100 80GB | ~$320 | ~$230,400 |
| High Performance | 128x H100 80GB | ~$640 | ~$460,800 |

## Best Use Cases

### 1. Complex Scientific Research

```python
def scientific_analysis(client: Grok3Client, research_question: str):
    """Perform deep scientific analysis."""
    
    messages = [
        {
            "role": "system",
            "content": """You are a world-class research scientist.
            Analyze problems with extreme rigor, citing relevant principles
            and considering multiple perspectives."""
        },
        {
            "role": "user",
            "content": f"""Analyze this research question thoroughly:
            
            {research_question}
            
            Include:
            1. Current state of knowledge
            2. Theoretical framework
            3. Proposed mechanisms
            4. Experimental predictions
            5. Potential applications"""
        }
    ]
    
    response = client.extended_thinking(messages, budget_tokens=16384)
    return response["choices"][0]["message"]["content"]

# Complex scientific reasoning
result = scientific_analysis(client, """
What are the potential mechanisms by which quantum effects 
could influence biological processes like photosynthesis 
and bird navigation? Provide a theoretical framework 
and experimental predictions.
""")
```

**Why Grok-3**: Frontier reasoning capabilities for complex scientific questions.

### 2. Advanced Code Architecture

```python
def architecture_design(client: Grok3Client, requirements: str):
    """Design complex software architecture."""
    
    messages = [
        {
            "role": "system",
            "content": """You are a principal software architect.
            Design systems that are scalable, maintainable, and elegant.
            Consider trade-offs and provide detailed implementation guidance."""
        },
        {
            "role": "user",
            "content": f"""Design a complete architecture for:
            
            {requirements}
            
            Include:
            1. High-level architecture diagram (text description)
            2. Component breakdown
            3. Data flow
            4. Scalability considerations
            5. Security measures
            6. Implementation phases
            7. Code examples for critical components"""
        }
    ]
    
    response = client.extended_thinking(messages, budget_tokens=16384)
    return response["choices"][0]["message"]["content"]

# Complex system design
result = architecture_design(client, """
A real-time collaborative document editing platform
like Google Docs, supporting:
- 100K concurrent users
- Offline editing with sync
- Real-time presence indicators
- Version history
- End-to-end encryption
- Plugin system
""")
```

**Why Grok-3**: Extended output and deep reasoning for complex architectural decisions.

### 3. Mathematical Problem Solving

```python
def solve_complex_math(client: Grok3Client, problem: str):
    """Solve advanced mathematical problems."""
    
    messages = [
        {
            "role": "system",
            "content": """You are an expert mathematician.
            Solve problems with rigorous proof techniques.
            Show all steps and justify each one."""
        },
        {
            "role": "user",
            "content": f"""Solve this problem rigorously:
            
            {problem}
            
            Provide:
            1. Problem interpretation
            2. Strategy selection
            3. Step-by-step solution
            4. Verification
            5. Generalization (if applicable)"""
        }
    ]
    
    response = client.extended_thinking(messages, budget_tokens=8192)
    return response["choices"][0]["message"]["content"]

# Complex mathematical proof
result = solve_complex_math(client, """
Prove that for any prime p > 3, p² ≡ 1 (mod 24).
Then generalize this result.
""")
```

**Why Grok-3**: Best-in-class mathematical reasoning and proof generation.

### 4. Legal and Contract Analysis

```python
def legal_analysis(client: Grok3Client, document: str, 
                   analysis_type: str = "comprehensive"):
    """Analyze legal documents with deep reasoning."""
    
    messages = [
        {
            "role": "system",
            "content": """You are an expert legal analyst.
            Analyze documents thoroughly, identifying key terms,
            potential issues, and implications."""
        },
        {
            "role": "user",
            "content": f"""Perform a {analysis_type} analysis of this legal document:
            
            {document}
            
            Include:
            1. Key terms and definitions
            2. Obligations and rights
            3. Potential risks
            4. Ambiguities
            5. Comparison with standard practices
            6. Recommendations"""
        }
    ]
    
    response = client.extended_thinking(messages, budget_tokens=16384)
    return response["choices"][0]["message"]["content"]
```

**Why Grok-3**: Extended context and output for comprehensive document analysis.

### 5. Multi-Modal Research Synthesis

```python
def multi_modal_research(client: Grok3Client, 
                        images: list, 
                        text_documents: list,
                        research_question: str):
    """Synthesize information from multiple modalities."""
    
    content = []
    
    # Add text documents
    for i, doc in enumerate(text_documents):
        content.append({
            "type": "text",
            "text": f"Document {i+1}:\n{doc}\n\n"
        })
    
    # Add images
    import base64
    for img_path in images:
        with open(img_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode('utf-8')
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}
        })
    
    # Add research question
    content.append({
        "type": "text",
        "text": f"\n\nResearch Question: {research_question}\n\n"
        "Synthesize insights from all provided materials."
    })
    
    messages = [{"role": "user", "content": content}]
    
    response = client.extended_thinking(messages, budget_tokens=16384)
    return response["choices"][0]["message"]["content"]
```

**Why Grok-3**: Advanced multimodal understanding with deep synthesis capabilities.

## Limitations and Considerations

### Technical Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| 131K context | Large but not unlimited | Summarize extremely long content |
| 32K output | Very large but may still truncate | Split very long outputs |
| High cost | Premium pricing | Use Grok-2-mini for simpler tasks |
| Vision processing | Added latency for complex images | Optimize image sizes |
| Rate limits | May affect high-volume applications | Implement queuing |

### Performance Considerations

1. **Extended Thinking Cost**: Thinking tokens add to cost
2. **Latency**: Complex reasoning may take longer
3. **Temperature Sensitivity**: Lower temperatures for deterministic tasks
4. **Context Utilization**: Full context may not always be optimal

### When to Use Grok-3 vs Alternatives

| Task | Recommended Model | Reason |
|------|-------------------|--------|
| Simple Q&A | Grok-2-mini | Cost-effective |
| Code generation | Grok-2 | Good balance |
| Complex reasoning | Grok-3 | Best performance |
| Mathematical proofs | Grok-3 | Frontier capabilities |
| Scientific research | Grok-3 | Deep analysis |
| Creative writing | Grok-2 or Grok-3 | Depends on quality needs |
| High-volume processing | Grok-2-mini | Cost and speed |

### Known Issues

1. **Hallucination**: May still generate plausible but incorrect information
2. **Overthinking**: Extended thinking may over-complicate simple problems
3. **Consistency**: Complex outputs may vary between runs
4. **Cost Management**: Easy to incur high costs with extended thinking

## Migration Guide

### From Grok-2 to Grok-3

```python
# Grok-2 (Before)
response = client.chat(
    messages,
    model="grok-2",
    max_tokens=16384
)

# Grok-3 (After) - Enhanced capabilities
response = client.chat(
    messages,
    model="grok-3",
    max_tokens=32768  # Double the output capacity
)

# New: Extended thinking for complex problems
response = client.extended_thinking(
    messages,
    budget_tokens=8192
)
```

**Key Changes**:
- Model identifier: `grok-2` → `grok-3`
- Output capacity: 16K → 32K tokens
- New: Extended thinking mode
- Improved: All benchmark scores significantly higher

### From OpenAI o1 to Grok-3

```python
# OpenAI o1 (Before)
response = openai.ChatCompletion.create(
    model="o1-preview",
    messages=messages
)

# Grok-3 (After)
response = client.extended_thinking(
    messages,
    budget_tokens=8192
)
```

**Migration Considerations**:
- Similar reasoning capabilities
- Grok-3 offers extended output
- Real-time knowledge access
- Different pricing structure

### From Claude 3.5 Sonnet to Grok-3

```python
# Anthropic (Before)
client = anthropic.Anthropic(api_key="...")
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=messages,
    max_tokens=8192
)

# Grok-3 (After)
response = client.extended_thinking(
    messages,
    budget_tokens=8192
)
```

**Migration Considerations**:
- Different API structure
- Extended thinking similar to Claude's extended thinking
- Higher output capacity
- Real-time data access advantage

### Migration Checklist

- [ ] Update model identifier to `grok-3`
- [ ] Implement extended thinking for complex tasks
- [ ] Adjust max_tokens for 32K output capacity
- [ ] Update cost projections
- [ ] Test with representative complex workloads
- [ ] Implement thinking token budget management
- [ ] Update monitoring for extended outputs
- [ ] Train team on extended thinking capabilities

## Additional Resources

- **API Documentation**: [docs.x.ai](https://docs.x.ai)
- **Model Card**: [xAI/grok-3-card](https://x.ai/grok-3-card)
- **Reasoning Guide**: [docs.x.ai/reasoning](https://docs.x.ai/reasoning)
- **GitHub**: [xAI/grok-3](https://github.com/xai-org/grok-3)
- **Community**: X platform developer community
- **Support**: support@x.ai

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.0.0 | 2024-12-13 | Initial release with extended thinking |
| 3.0.1 | 2025-01-05 | Reasoning improvements |
| 3.0.2 | 2025-01-20 | Extended output optimizations |

---

*Last updated: July 2026*
*Maintained by: xAI*