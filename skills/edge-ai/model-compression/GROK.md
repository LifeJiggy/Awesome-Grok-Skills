---
name: "Model Compression"
version: "2.0.0"
description: "Comprehensive model compression toolkit with quantization, pruning, knowledge distillation, low-rank factorization, and neural architecture search for efficient ML models"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["edge-ai", "model-compression", "quantization", "pruning", "distillation", "efficiency"]
category: "edge-ai"
personality: "compression-engineer"
use_cases: ["quantization", "pruning", "knowledge distillation", "low-rank factorization", "efficiency optimization"]
---

# Model Compression

> Production-grade model compression framework providing quantization, pruning, knowledge distillation, low-rank factorization, and architecture optimization for building efficient ML models.

## Overview

The Model Compression module provides tools for reducing model size and computational cost while maintaining accuracy. It implements post-training and quantization-aware training, structured and unstructured pruning, knowledge distillation from teacher to student models, low-rank factorization for weight matrices, and neural architecture search for efficient architectures. Every compression technique includes accuracy validation and performance benchmarking.

## Core Capabilities

### 1. Quantization
- Post-training quantization (PTQ)
- Quantization-aware training (QAT)
- Mixed-precision quantization
- Per-channel and per-tensor quantization
- Calibration dataset management

### 2. Pruning
- Unstructured pruning (magnitude-based)
- Structured pruning (channel/filter)
- Gradual pruning schedules
- Lottery ticket hypothesis support
- Sparsity-aware training

### 3. Knowledge Distillation
- Teacher-student training
- Feature-level distillation
- Attention transfer
- Knowledge distillation loss functions
- Multi-teacher distillation

### 4. Low-Rank Factorization
- SVD decomposition of weight matrices
- Tucker decomposition
- CP decomposition
- Tensor-train decomposition
- Rank selection optimization

### 5. Architecture Optimization
- Neural Architecture Search (NAS)
- EfficientNet-style compound scaling
- Depthwise separable convolutions
- MobileNet architectures
- ShuffleNet optimizations

### 6. Compression Analysis
- Size reduction measurement
- Speedup benchmarking
- Accuracy impact analysis
- FLOPs reduction calculation
- Memory footprint comparison

## Usage Examples

### Quantization

```python
from model_compression import Quantizer, QuantizationConfig

quantizer = Quantizer()

# Post-training quantization
config = QuantizationConfig(
    method="int8",
    calibration_samples=100,
    per_channel=True,
)

result = quantizer.quantize(model, config)
print(f"Size: {result.original_mb:.1f} → {result.compressed_mb:.1f} MB")
print(f"Accuracy: {result.original_accuracy:.2%} → {result.compressed_accuracy:.2%}")
print(f"Speedup: {result.speedup:.1f}x")
```

### Pruning

```python
from model_compression import Pruner, PruningSchedule

pruner = Pruner()

# Structured pruning
result = pruner.prune(
    model=model,
    sparsity=0.5,
    schedule=PruningSchedule.GRADUAL,
    structure="channel",
)

print(f"Parameters: {result.original_params:,} → {result.pruned_params:,}")
print(f"Sparsity: {result.actual_sparsity:.0%}")
print(f"Accuracy: {result.accuracy_after:.2%}")
```

### Knowledge Distillation

```python
from model_compression import Distiller, DistillationConfig

distiller = Distiller()

# Distill knowledge
student = distiller.distill(
    teacher=teacher_model,
    student=student_model,
    config=DistillationConfig(
        temperature=4.0,
        alpha=0.7,
        epochs=50,
    ),
)

print(f"Teacher accuracy: {teacher_accuracy:.2%}")
print(f"Student accuracy: {student_accuracy:.2%}")
print(f"Size reduction: {size_reduction:.1f}x")
```

### Low-Rank Factorization

```python
from model_compression import LowRankFactorizer

factorizer = LowRankFactorizer()

# Factorize layers
result = factorizer.factorize(
    model=model,
    target_layers=["fc1", "fc2"],
    rank_ratio=0.5,
)

print(f"Original parameters: {result.original_params:,}")
print(f"Factorized parameters: {result.factorized_params:,}")
print(f"Compression ratio: {result.compression_ratio:.1f}x")
```

## Best Practices

### Quantization
- Use calibration data representative of deployment data
- Start with PTQ before attempting QAT
- Check per-channel quantization for better accuracy
- Validate on edge device, not just simulation

### Pruning
- Use gradual pruning for better accuracy retention
- Prefer structured pruning for hardware efficiency
- Train sparse models, don't just prune trained ones
- Monitor accuracy during pruning

### Knowledge Distillation
- Choose teacher carefully (larger isn't always better)
- Tune temperature parameter for task
- Use multiple loss components (logits, features, attention)
- Train student for sufficient epochs

### Low-Rank Factorization
- Analyze layer sensitivity before factorizing
- Use different rank ratios per layer
- Fine-tune after factorization
- Check actual speedup on target hardware

## Related Modules

- **on-device-ml**: Deploy compressed models to devices
- **edge-inference**: Optimize inference of compressed models
- **tinyml**: Ultra-aggressive compression for microcontrollers
- **model-optimization**: General model optimization techniques