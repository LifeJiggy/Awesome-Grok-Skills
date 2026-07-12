---
name: "On-Device ML"
version: "2.0.0"
description: "Comprehensive on-device machine learning toolkit with model optimization, inference engines, hardware acceleration, and edge deployment for mobile and IoT ML applications"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["edge-ai", "on-device", "mobile-ml", "inference", "optimization", "deployment"]
category: "edge-ai"
personality: "edge-ml-engineer"
use_cases: ["model optimization", "inference engines", "hardware acceleration", "edge deployment", "mobile ML"]
---

# On-Device ML

> Production-grade on-device machine learning framework providing model optimization, inference engine management, hardware acceleration, and edge deployment for running ML models on mobile and IoT devices.

## Overview

The On-Device ML module provides tools for deploying machine learning models to edge devices. It implements model optimization for constrained environments, inference engine management across platforms (TensorFlow Lite, Core ML, ONNX Runtime), hardware acceleration (GPU, NPU, DSP), and comprehensive deployment pipelines. Every deployment includes performance profiling, accuracy validation, and monitoring.

## Core Capabilities

### 1. Model Optimization
- Quantization (INT8, FP16, dynamic)
- Pruning and sparsification
- Knowledge distillation
- Model compression
- Operator fusion

### 2. Inference Engines
- TensorFlow Lite integration
- Core ML support
- ONNX Runtime
- NCNN for Android
- MNN for cross-platform

### 3. Hardware Acceleration
- GPU delegate (OpenGL, Metal, Vulkan)
- NNAPI for Android
- Core ML Neural Engine
- Qualcomm Hexagon DSP
- Intel VPU support

### 4. Edge Deployment
- Model packaging and distribution
- OTA model updates
- A/B testing for models
- Rollback capabilities
- Version management

### 5. Performance Profiling
- Latency measurement
- Memory usage tracking
- Power consumption analysis
- Thermal impact assessment
- Benchmark comparisons

### 6. Accuracy Validation
- On-device accuracy testing
- Drift detection
- A/B accuracy comparison
- Regression testing
- User feedback integration

## Usage Examples

### Model Optimization

```python
from on_device_ml import ModelOptimizer, QuantizationType

optimizer = ModelOptimizer()

# Quantize model
quantized = optimizer.quantize(
    model_path="model.tflite",
    quantization=QuantizationType.INT8,
    calibration_data=calibration_dataset,
)

print(f"Original size: {quantized.original_size_mb:.1f} MB")
print(f"Quantized size: {quantized.quantized_size_mb:.1f} MB")
print(f"Compression ratio: {quantized.compression_ratio:.1f}x")
print(f"Accuracy drop: {quantized.accuracy_drop:.2f}%")
```

### Inference Engine

```python
from on_device_ml import InferenceEngine, Platform

engine = InferenceEngine(platform=Platform.ANDROID)

# Load and run model
engine.load_model("model.tflite")
result = engine.predict(input_data)

print(f"Inference time: {result.latency_ms:.1f}ms")
print(f"Output: {result.predictions}")
print(f"Confidence: {result.confidence:.2%}")
```

### Hardware Acceleration

```python
from on_device_ml import HardwareAccelerator, DelegateType

accelerator = HardwareAccelerator()

# Configure acceleration
config = accelerator.configure(
    delegate=DelegateType.GPU,
    fallback_to_cpu=True,
    precision=Precision.FP16,
)

print(f"Delegate: {config.active_delegate}")
print(f"GPU available: {config.gpu_available}")
print(f"Acceleration factor: {config.speedup_factor:.1f}x")
```

### Edge Deployment

```python
from on_device_ml import EdgeDeployer

deployer = EdgeDeployer()

# Deploy model to devices
deployment = deployer.deploy(
    model_path="model_optimized.tflite",
    target_devices=["android", "ios"],
    rollout_percentage=10,
    monitoring=True,
)

print(f"Deployment: {deployment.id}")
print(f"Target: {deployment.target_devices}")
print(f"Rollout: {deployment.rollout_percentage}%")
```

## Best Practices

### Model Optimization
- Start with post-training quantization before QAT
- Profile accuracy impact of each optimization
- Use mixed precision for sensitive layers
- Validate optimizations on representative data

### Inference
- Choose the right engine for your platform
- Benchmark multiple engines before deciding
- Use hardware delegates when available
- Implement fallback to CPU

### Hardware Acceleration
- Check hardware support before enabling
- Profile power consumption on mobile
- Handle thermal throttling gracefully
- Test on target hardware, not just simulators

### Deployment
- Use A/B testing for model updates
- Implement monitoring and alerting
- Support rollback for failed deployments
- Track model performance in production

## Related Modules

- **model-compression**: Advanced model compression techniques
- **edge-inference**: Inference optimization strategies
- **tinyml**: Ultra-low-power ML deployment
- **federated-edge**: Federated learning at the edge