---
name: "model-optimization"
category: "ai-ml"
version: "2.0.0"
tags: ["ai-ml", "model-optimization", "pruning", "quantization", "distillation", "compression", "inference"]
---

# Model Optimization

## Overview

Comprehensive model optimization toolkit for reducing inference latency, memory footprint, and energy consumption of deep learning models. This module implements pruning (unstructured, structured, movement-based), quantization (post-training, quantization-aware training, INT8/INT4), knowledge distillation, neural architecture optimization, and graph-level optimizations. Supports PyTorch, TensorFlow, and ONNX Runtime with hardware-specific optimization passes for CPU, GPU, and edge/TPU deployment targets.

## Core Capabilities

- **Pruning**: Unstructured (magnitude-based), structured (channel/filter), and movement pruning with gradual sparsity schedules
- **Quantization**: Post-training dynamic/static quantization, QAT (quantization-aware training), INT8, INT4, and mixed-precision quantization
- **Knowledge Distillation**: Teacher-student framework with soft-label, feature-map, and attention-transfer distillation
- **Graph Optimization**: Operator fusion, constant folding, dead code elimination, and layout optimization
- **Sparsity**: N:M structured sparsity for hardware acceleration (2:4 on NVIDIA Ampere+)
- **Model Profiling**: Detailed layer-by-layer profiling with FLOPs, parameters, memory, and latency breakdown
- **Hardware Targeting**: Optimization presets for mobile (ARM), edge (NPU), cloud GPU, and server CPU
- **Compression Ratio Control**: Target specific compression ratios with automatic strategy selection

## Usage

```python
from model_optimization import (
    Pruner, Quantizer, Distiller, ModelProfiler, OptimizationTarget
)

# Profile original model
profiler = ModelProfiler()
profile = profiler.profile("model.onnx")
print(f"Parameters: {profile.parameter_count:,}")
print(f"FLOPs: {profile.flops:.2e}")
print(f"Memory: {profile.memory_mb:.1f} MB")
print(f"Latency (CPU): {profile.latency_ms:.1f} ms")

# Structured pruning
pruner = Pruner(sparsity=0.5, method="structured")
pruned = pruner.prune("model.onnx")
pruned_profile = profiler.profile(pruned)
print(f"\nAfter pruning:")
print(f"  Parameters: {pruned_profile.parameter_count:,} ({pruned.compression_ratio:.1f}x)")
print(f"  FLOPs: {pruned_profile.flops:.2e}")
print(f"  Accuracy drop: {pruned.accuracy_delta:.2%}")

# INT8 quantization
quantizer = Quantizer(precision="int8", method="post_training_static")
quantized = quantizer.quantize(pruned, calibration_dataset="calibration_data.bin")
quant_profile = profiler.profile(quantized)
print(f"\nAfter quantization:")
print(f"  Model size: {quant_profile.memory_mb:.1f} MB ({quantized.size_ratio:.1f}x smaller)")
print(f"  Latency: {quant_profile.latency_ms:.1f} ms ({quantized.speedup:.1f}x faster)")
```

```python
# Knowledge distillation
from model_optimization import DistillationConfig

distiller = Distiller(
    config=DistillationConfig(
        teacher_model="teacher_large.onnx",
        student_model="student_small.onnx",
        temperature=4.0,
        alpha=0.7,  # soft-label weight
        beta=0.3,   # feature-map weight
        epochs=50,
        learning_rate=1e-4,
    )
)
distilled = distiller.distill()
print(f"Student accuracy: {distilled.accuracy:.4f} (teacher: {distilled.teacher_accuracy:.4f})")
print(f"Compression: {distilled.compression_ratio:.1f}x, Speedup: {distilled.speedup:.1f}x")
```

## Best Practices

- Profile before optimizing — know your bottleneck (compute, memory, or bandwidth)
- Apply pruning before quantization — sparse models quantize more effectively
- Use calibration datasets representative of real inference data for PTQ accuracy
- Start with 50% sparsity and increase gradually — aggressive pruning needs fine-tuning
- Knowledge distillation works best when teacher is 3-10x larger than student
- Use mixed-precision quantization (FP16 for activations, INT8 for weights) for best accuracy/latency tradeoff
- Validate optimized models on a held-out test set — never trust training-set metrics alone
- Benchmark on target hardware — GPU speedups don't predict CPU/edge speedups
- Use N:M sparsity (2:4) for guaranteed hardware acceleration on modern GPUs
- Combine techniques: prune → distill → quantize for maximum compression

## Related Modules

- **neural-architecture-search** — Discover efficient architectures before optimization
- **model-deployment** — Deploy optimized models to production serving infrastructure
- **automl** — Automated pipeline selecting optimal optimization strategies
- **federated-learning** — Optimize models for federated learning communication efficiency
- **edge-ai** → **tinyml** — Extreme compression for microcontroller deployment
