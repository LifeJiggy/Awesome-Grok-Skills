---
name: grok-model-comparison
category: reference
version: "1.0.0"
tags:
  - grok
  - models
  - comparison
  - benchmarks
  - pricing
last_updated: 2026-07-23
author: Awesome Grok Skills Contributors
license: MIT
---

# Grok Model Comparison: Complete Reference Guide

## Overview

This document provides a comprehensive side-by-side comparison of all available
Grok models from xAI. Use this guide to select the optimal model for your use case
based on performance, cost, context window, and specialized capabilities.

---

## Table of Contents

1. [Model Family Overview](#model-family-overview)
2. [Detailed Specifications](#detailed-specifications)
3. [Benchmark Comparisons](#benchmark-comparisons)
4. [Pricing Comparison](#pricing-comparison)
5. [Use Case Recommendations](#use-case-recommendations)
6. [Model Selection Guide](#model-selection-guide)
7. [Performance Characteristics](#performance-characteristics)
8. [Migration Guide](#migration-guide)
9. [Troubleshooting](#troubleshooting)

---

## Model Family Overview

### Grok Model Generations

| Generation | Models | Release | Focus |
|------------|--------|---------|-------|
| **Grok-1** | grok-1 | Nov 2023 | Initial release |
| **Grok-1.5** | grok-1-5 | Feb 2024 | Improved reasoning |
| **Grok-2** | grok-2, grok-2-mini | Aug 2024 | Enhanced performance |
| **Grok-3** | grok-3, grok-3-mini, grok-3-fast | Dec 2024 | Speed + quality balance |
| **Grok-4** | grok-4, grok-4-fast, grok-4-heavy | Jun 2025 | Advanced reasoning |
| **Grok-4.1** | grok-4-1, grok-4-1-fast | Nov 2025 | Enterprise grade |
| **Grok-4.5** | grok-4-5 | Feb 2026 | Latest flagship |

### Model Tiers

| Tier | Models | Primary Use |
|------|--------|-------------|
| **Flagship** | grok-4-5, grok-4-heavy | Complex reasoning, research |
| **Production** | grok-4-1, grok-4 | Enterprise, balanced quality |
| **Fast** | grok-4-1-fast, grok-4-fast, grok-3-fast | Low-latency applications |
| **Mini** | grok-3-mini, grok-2-mini | Cost-sensitive, simple tasks |
| **Legacy** | grok-1, grok-1-5, grok-2 | Maintained, not recommended |

---

## Detailed Specifications

### Current Models (2026)

| Model | Context Window | Max Output | Knowledge Cutoff | Multimodal | Reasoning |
|-------|---------------|------------|------------------|------------|-----------|
| **grok-4-5** | 128,000 | 32,768 | Feb 2026 | Yes | Advanced |
| **grok-4-1** | 32,768 | 16,384 | Nov 2025 | Yes | Advanced |
| **grok-4-1-fast** | 32,768 | 16,384 | Nov 2025 | Yes | Standard |
| **grok-4** | 32,768 | 16,384 | Jun 2025 | Yes | Advanced |
| **grok-4-fast** | 32,768 | 16,384 | Jun 2025 | Yes | Standard |
| **grok-4-heavy** | 32,768 | 16,384 | Jun 2025 | Yes | Extended |
| **grok-3** | 131,072 | 16,384 | Dec 2024 | Yes | Standard |
| **grok-3-fast** | 131,072 | 16,384 | Dec 2024 | Yes | Standard |
| **grok-3-mini** | 131,072 | 16,384 | Dec 2024 | No | Basic |
| **grok-2** | 131,072 | 8,192 | Aug 2024 | Yes | Standard |
| **grok-2-mini** | 131,072 | 8,192 | Aug 2024 | No | Basic |
| **grok-1-5** | 131,072 | 8,192 | Feb 2024 | No | Standard |
| **grok-1** | 131,072 | 4,096 | Nov 2023 | No | Basic |

### Extended Context Models

| Model | Context | Extended Context | Best For |
|-------|---------|------------------|----------|
| grok-3 | 131,072 | 1M (beta) | Long document analysis |
| grok-3-fast | 131,072 | 1M (beta) | Fast processing of long texts |
| grok-4-5 | 128,000 | N/A | Balanced context needs |

### Specialized Models

| Model | Specialization | Advantage |
|-------|---------------|-----------|
| **grok-3-mini** | Fast inference | 50% lower cost, 2x speed |
| **grok-4-heavy** | Extended reasoning | Multi-step problem solving |
| **grok-3-fast** | Low latency | <500ms first token |

---

## Benchmark Comparisons

### MMLU (Massive Multitask Language Understanding)

| Model | Score | Percentile |
|-------|-------|------------|
| grok-4-5 | 92.1 | 99th |
| grok-4-heavy | 89.7 | 97th |
| grok-4-1 | 88.4 | 95th |
| grok-4 | 87.2 | 93rd |
| grok-3 | 85.1 | 90th |
| grok-3-mini | 79.8 | 82nd |
| grok-2 | 78.5 | 80th |
| grok-2-mini | 72.1 | 68th |
| grok-1-5 | 73.4 | 71st |
| grok-1 | 64.2 | 52nd |

### HumanEval (Code Generation)

| Model | Pass@1 | Pass@10 |
|-------|--------|---------|
| grok-4-5 | 94.3 | 98.2 |
| grok-4-heavy | 91.7 | 96.5 |
| grok-4-1 | 89.2 | 95.1 |
| grok-4 | 87.8 | 93.7 |
| grok-3 | 85.6 | 92.4 |
| grok-3-mini | 76.3 | 86.2 |
| grok-2 | 72.1 | 83.5 |

### GSM8K (Grade School Math)

| Model | Accuracy |
|-------|----------|
| grok-4-5 | 97.2% |
| grok-4-heavy | 95.8% |
| grok-4-1 | 94.1% |
| grok-4 | 92.7% |
| grok-3 | 91.3% |
| grok-3-mini | 84.6% |
| grok-2 | 81.2% |

### MATH (Competition Mathematics)

| Model | Level 5 | Overall |
|-------|---------|---------|
| grok-4-5 | 78.4 | 86.2 |
| grok-4-heavy | 72.1 | 81.5 |
| grok-4-1 | 68.3 | 78.9 |
| grok-4 | 64.7 | 75.2 |
| grok-3 | 58.2 | 70.1 |
| grok-3-mini | 42.5 | 56.8 |

### GPQA (Graduate-Level Q&A)

| Model | Score |
|-------|-------|
| grok-4-5 | 68.4 |
| grok-4-heavy | 62.1 |
| grok-4-1 | 58.7 |
| grok-4 | 55.2 |
| grok-3 | 49.8 |
| grok-3-mini | 38.2 |

### Speed Benchmarks

| Model | First Token (ms) | Tokens/sec | Throughput |
|-------|------------------|------------|------------|
| grok-4-1-fast | <200 | 150+ | High |
| grok-4-fast | <250 | 120+ | High |
| grok-3-fast | <300 | 180+ | Highest |
| grok-3 | ~500 | 80+ | Medium |
| grok-4 | ~600 | 60+ | Medium |
| grok-4-1 | ~700 | 55+ | Medium |
| grok-4-5 | ~800 | 45+ | Lower |
| grok-4-heavy | ~1000 | 35+ | Lower |

---

## Pricing Comparison

### API Pricing (per 1M tokens)

| Model | Input | Output | Effective Cost |
|-------|-------|--------|----------------|
| **grok-4-5** | $15.00 | $45.00 | Premium |
| **grok-4-heavy** | $12.00 | $36.00 | Premium |
| **grok-4-1** | $5.00 | $15.00 | High |
| **grok-4-1-fast** | $5.00 | $15.00 | High |
| **grok-4** | $3.00 | $10.00 | Medium |
| **grok-4-fast** | $3.00 | $10.00 | Medium |
| **grok-3** | $2.00 | $6.00 | Standard |
| **grok-3-fast** | $2.00 | $6.00 | Standard |
| **grok-3-mini** | $0.30 | $0.50 | Budget |
| **grok-2** | $2.00 | $8.00 | Legacy |
| **grok-2-mini** | $0.20 | $0.40 | Budget |
| **grok-1-5** | $0.50 | $1.50 | Budget |
| **grok-1** | $0.50 | $1.50 | Budget |

### Cost Efficiency Analysis

| Use Case | Recommended | Cost per 1K Queries* |
|----------|-------------|---------------------|
| Simple Q&A | grok-3-mini | ~$0.15 |
| Code generation | grok-3 | ~$2.40 |
| Complex analysis | grok-4 | ~$5.20 |
| Research synthesis | grok-4-5 | ~$18.00 |
| Real-time chat | grok-3-fast | ~$2.40 |
| Enterprise ops | grok-4-1 | ~8.00 |

*Assumes 500 tokens input, 500 tokens output per query.

### Free Tier Limits

| Feature | Free | Tier 1 ($5) | Tier 2 ($25) | Tier 3 ($100) |
|---------|------|-------------|--------------|---------------|
| Rate Limit | 1 RPM | 10 RPM | 50 RPM | 200 RPM |
| Daily Tokens | 100K | 1M | 10M | 100M |
| Models | grok-3-mini | All | All | All |

---

## Use Case Recommendations

### By Industry

| Industry | Primary Model | Backup | Rationale |
|----------|---------------|--------|-----------|
| **Technology** | grok-3 | grok-3-fast | Balanced speed/quality |
| **Healthcare** | grok-4-5 | grok-4 | Accuracy critical |
| **Finance** | grok-4-1 | grok-4 | Reliability + reasoning |
| **Education** | grok-3 | grok-3-mini | Cost-effective |
| **Legal** | grok-4-5 | grok-4-1 | Precision required |
| **Creative** | grok-3-fast | grok-3 | Speed for iteration |
| **Research** | grok-4-5 | grok-4-heavy | Deep reasoning |
| **Enterprise** | grok-4-1 | grok-4 | SLA compliance |

### By Task Complexity

| Complexity | Model | Justification |
|------------|-------|---------------|
| Trivial (classification, extraction) | grok-3-mini | Lowest cost |
| Simple (Q&A, summarization) | grok-3 | Good balance |
| Moderate (analysis, generation) | grok-4 | Enhanced reasoning |
| Complex (research, multi-step) | grok-4-5 | Maximum capability |
| Critical (safety, compliance) | grok-4-1 + validation | Reliability focus |

### By Latency Requirement

| Latency | Model | P95 First Token |
|---------|-------|-----------------|
| <100ms | Not available | N/A |
| <300ms | grok-3-fast | 280ms |
| <500ms | grok-4-fast | 420ms |
| <1s | grok-3 | 750ms |
| <2s | grok-4 | 1.2s |
| Any | grok-4-5 | 2.5s |

### By Budget

| Budget Level | Strategy | Models |
|--------------|----------|--------|
| **Minimal** (<$100/mo) | grok-3-mini only | grok-3-mini |
| **Conservative** ($100-500/mo) | Mix mini + fast | grok-3-mini, grok-3-fast |
| **Standard** ($500-2000/mo) | Standard tier | grok-3, grok-4 |
| **Premium** ($2000+/mo) | Full access | All models |

---

## Model Selection Guide

### Decision Flowchart

```
START
  |
  v
[Need best quality?] --Yes--> [Budget available?] --Yes--> grok-4-5
  |                              |
  No                             No
  |                              v
  v                          grok-4-1
[Need speed?] --Yes--> [Simple task?] --Yes--> grok-3-fast
  |                        |
  No                       No
  |                        v
  v                    grok-4-1-fast
[Complex task?] --Yes--> grok-4
  |
  No
  |
  v
[Cost sensitive?] --Yes--> grok-3-mini
  |
  No
  |
  v
grok-3 (default)
```

### Quick Selection Matrix

| Requirement | Selection |
|-------------|-----------|
| "Cheapest possible" | grok-3-mini |
| "Fast and good" | grok-3-fast |
| "Best for code" | grok-4-1 |
| "Best for math" | grok-4-5 |
| "Best for writing" | grok-3 |
| "Best for analysis" | grok-4-5 |
| "Production ready" | grok-4-1 |
| "Research grade" | grok-4-5 |

### Fallback Strategy

```python
MODEL_FALLBACK_CHAIN = {
    "primary": "grok-4-5",
    "fallback_1": "grok-4-1",
    "fallback_2": "grok-4",
    "fallback_3": "grok-3",
    "emergency": "grok-3-mini"
}

def get_model_with_fallback(primary_model):
    """Select model with automatic fallback."""
    fallback_chain = {
        "grok-4-5": ["grok-4-1", "grok-4", "grok-3"],
        "grok-4-1": ["grok-4", "grok-3", "grok-3-mini"],
        "grok-4": ["grok-3", "grok-3-mini"],
        "grok-3": ["grok-3-mini", "grok-3-fast"],
    }
    return fallback_chain.get(primary_model, ["grok-3-mini"])
```

---

## Performance Characteristics

### Reasoning Depth

| Model | Chain of Thought | Multi-step | Verification |
|-------|-----------------|------------|--------------|
| grok-4-5 | Excellent | 10+ steps | Self-correcting |
| grok-4-heavy | Excellent | 8+ steps | Self-correcting |
| grok-4-1 | Very Good | 6+ steps | Good |
| grok-4 | Good | 5+ steps | Good |
| grok-3 | Good | 4+ steps | Basic |
| grok-3-mini | Basic | 2+ steps | None |

### Multimodal Capabilities

| Model | Text | Vision | Audio | Code |
|-------|------|--------|-------|------|
| grok-4-5 | Yes | Yes | Yes | Yes |
| grok-4-1 | Yes | Yes | Yes | Yes |
| grok-4 | Yes | Yes | Yes | Yes |
| grok-3 | Yes | Yes | Beta | Yes |
| grok-3-mini | Yes | No | No | Yes |
| grok-2 | Yes | Yes | No | Yes |

### Context Window Utilization

| Model | Effective Context | Optimal Range |
|-------|-------------------|---------------|
| grok-4-5 | 128K | 8K–64K tokens |
| grok-4-1 | 32K | 4K–16K tokens |
| grok-3 | 131K | 8K–64K tokens |
| grok-3-mini | 131K | 2K–32K tokens |

**Note:** Performance degrades outside optimal range. For best results, keep
input within the recommended optimal range.

### Consistency Metrics

| Model | Temperature Stability | Output Consistency |
|-------|----------------------|-------------------|
| grok-4-1 | Excellent | 95%+ |
| grok-4 | Very Good | 92%+ |
| grok-3 | Good | 88%+ |
| grok-3-fast | Good | 85%+ |
| grok-3-mini | Variable | 80%+ |

---

## Migration Guide

### Upgrading from Legacy Models

#### From grok-1 → grok-3

```python
# Before (grok-1)
response = client.chat.completions.create(
    model="grok-1",
    messages=[...],
    max_tokens=4096
)

# After (grok-3)
response = client.chat.completions.create(
    model="grok-3",
    messages=[...],
    max_tokens=16384,
    temperature=0.7  # More natural responses
)
```

#### From grok-2 → grok-4

```python
# Before (grok-2)
response = client.chat.completions.create(
    model="grok-2",
    messages=[...]
)

# After (grok-4) - Enhanced reasoning
response = client.chat.completions.create(
    model="grok-4",
    messages=[...],
    temperature=0.3  # More precise
)
```

### Cost Migration Analysis

| Migration Path | Cost Change | Quality Change |
|----------------|-------------|----------------|
| grok-1 → grok-3 | +150% | +40% quality |
| grok-2 → grok-4 | +50% | +25% quality |
| grok-3 → grok-4-1 | +125% | +15% quality |
| grok-4 → grok-4-5 | +400% | +10% quality |

### API Changes

```python
# v1 to v2 migration checklist
MIGRATION_CHECKLIST = [
    "Update model names (grok-1 → grok-3)",
    "Adjust max_tokens (new models support 16K+)",
    "Update temperature ranges (0.0–2.0 → 0.0–2.0)",
    "Add system message support",
    "Enable streaming for better UX",
    "Update error handling for new error codes",
    "Test with new rate limits"
]
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Model not found" | Deprecated model | Use grok-3+ |
| Slow responses | Large context | Reduce input or use fast variant |
| Inconsistent output | High temperature | Lower to 0.1–0.5 |
| Token limit error | Exceeds max | Chunk input or increase limit |
| Quality degradation | Wrong model tier | Upgrade to appropriate tier |

### Model-Specific Issues

#### grok-3-mini
- **Issue:** Less accurate for complex reasoning
- **Solution:** Use grok-3 or grok-4 for complex tasks

#### grok-3-fast
- **Issue:** Slightly lower quality vs grok-3
- **Solution:** Accept trade-off or use grok-3

#### grok-4-5
- **Issue:** Higher latency, higher cost
- **Solution:** Reserve for high-value tasks only

### Performance Debugging

```python
def debug_model_performance(response):
    """Debug model response quality."""
    metrics = {
        "model": response.model,
        "finish_reason": response.choices[0].finish_reason,
        "tokens_used": response.usage.total_tokens,
        "response_time": response.response_time,
    }
    
    if response.choices[0].finish_reason == "length":
        print("Warning: Response truncated. Increase max_tokens.")
    
    if metrics["response_time"] > 5000:
        print("Warning: Slow response. Consider faster model.")
    
    return metrics
```

---

## Quick Reference Card

### Model Selection Quick Reference

| Priority | Model | When to Use |
|----------|-------|-------------|
| **Quality** | grok-4-5 | Research, critical analysis |
| **Balance** | grok-4-1 | Production, enterprise |
| **Speed** | grok-3-fast | Real-time, chat |
| **Cost** | grok-3-mini | High volume, simple tasks |
| **Code** | grok-4-1 | Development, debugging |
| **Reasoning** | grok-4-heavy | Multi-step problems |

### API Endpoint

```
Base URL: https://api.x.ai/v1
Auth: Bearer $XAI_API_KEY
Content-Type: application/json
```

### Response Format

```json
{
  "id": "chatcmpl-xxx",
  "model": "grok-3",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "..."
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 500,
    "total_tokens": 600
  }
}
```

---

## References

- xAI API Documentation: https://docs.x.ai
- Model Pricing: https://docs.x.ai/pricing
- Rate Limits: https://docs.x.ai/rate-limits
- Benchmarks: https://docs.x.ai/benchmarks

---

*Last updated: 2026-07-23 | Version 1.0.0*
