# Edge ML

Specialized skill for deploying and running machine learning models on edge devices. Covers model optimization, quantization, edge deployment strategies, federated learning, and inference management for resource-constrained environments.

## Core Capabilities

### Model Optimization
- Post-training quantization (INT8, FP16)
- Pruning and sparsity
- Knowledge distillation
- Architecture search for edge
- Mixed-precision optimization

### Edge Deployment
- TensorRT optimization for NVIDIA
- TFLite conversion and deployment
- Core ML for Apple devices
- Edge TPU compilation
- ONNX Runtime edge

### Inference Management
- Model versioning and rollbacks
- A/B testing at the edge
- Adaptive inference based on load
- Model caching and prefetching
- Batch inference optimization

### Federated Learning
- On-device model training
- Secure aggregation
- Differential privacy
- Client selection strategies
- Convergence monitoring

### Hardware Acceleration
- GPU-accelerated inference
- NPU and TPU integration
- CPU-optimized operators
- Memory-efficient execution
- Power-aware inference

## Usage Examples

### Edge ML Manager Setup
```python
from edge_ml import (
    EdgeMLManager, EdgeModel, ModelType, DeploymentTarget
)

edge = EdgeMLManager("factory-edge-01")

models = edge.get_model_list()
for m in models:
    print(f"{m['name']}: {m['latency_ms']:.1f}ms, {m['accuracy']:.1%}")

status = edge.get_edge_status()
print(f"Models: {status['models_deployed']}, Nodes: {status['nodes']['total_nodes']}")
```

### Running Inference
```python
result = edge.run_inference(
    model_id="object-detector",
    input_data={"image": "frame_001.jpg"},
    target_node="node-camera-1"
)
print(f"Inference time: {result['inference_time_ms']:.2f}ms")
print(f"Model: {result['model_name']}")
```

### Model Optimization
```python
quantization = edge.quantize_model("object-detector", precision="int8")
print(f"Size: {quantization['original_size_mb']:.1f} -> {quantization['quantized_size_mb']:.1f} MB")
print(f"Speedup: {quantization['speedup']:.2f}x")

pruning = edge.prune_model("object-detector", sparsity=0.3)
print(f"Parameters: {pruning['original_parameters']} -> {pruning['pruned_parameters']}")
```

### Model Deployment
```python
new_model = EdgeModel(
    model_id="custom-classifier",
    name="Custom CNN",
    model_type=ModelType.CNN,
    input_shape=[1, 224, 224, 3],
    output_shape=[1, 10],
    parameters=2500000,
    accuracy=0.925,
    latency_ms=8.0,
    memory_mb=10.0
)

deploy_result = edge.deploy_model(new_model, "node-gateway-1")
print(f"Deployed: {deploy_result['version']}")
```

### Benchmarking
```python
benchmark = edge.benchmark_model("pose-estimator", "node-gateway-1")
print(f"Throughput: {benchmark['throughput_fps']:.1f} FPS")
print(f"Power: {benchmark['power_watts']:.2f}W")
```

### Node Management
```python
node_status = edge.get_node_status()
for node_id, info in node_status["nodes"].items():
    print(f"{node_id}: {info['device_type']}, {info['memory_available']:.1f}GB RAM")
```

### Federated Learning
```python
fed_result = edge.federated_learning_round(
    model_id="object-detector",
    client_nodes=["node-camera-1", "node-camera-2"]
)
print(f"Round {fed_result['round']}: {fed_result['total_samples']} samples")
print(f"Aggregated update: {fed_result['aggregated_update']:.4f}")
```

### On-Device Training
```python
from edge_ml import OnDeviceTraining

trainer = OnDeviceTraining()
train_result = trainer.incremental_train(
    model_id="object-detector",
    new_data={"images": 500},
    epochs=5
)
print(f"Accuracy: {train_result['accuracy_before']:.2%} -> {train_result['accuracy_after']:.2%}")
```

## Best Practices

1. **Quantization**: Start with INT8 quantization for 4x size reduction
2. **Memory Management**: Implement model swapping for memory constraints
3. **Power Efficiency**: Use lower precision for battery-powered devices
4. **Latency Budget**: Profile to meet real-time requirements
5. **Updates**: Implement atomic model updates with rollback
6. **Privacy**: Use federated learning for sensitive data
7. **Testing**: Test on actual edge hardware, not just simulators
8. **Monitoring**: Track model drift and performance degradation

## Related Skills

- [Machine Learning](ai-ml/ml): ML fundamentals
- [Model Optimization](ai-ml/optimization): Optimization techniques
- [IoT](iot/embedded-systems): Edge device integration
- [Computer Vision](computer-vision): CV model deployment

## Use Cases

- Real-time object detection in surveillance
- Predictive maintenance on factory equipment
- Voice keyword detection on smart speakers
- Anomaly detection in industrial sensors
- Autonomous robot navigation
- Medical device inference
- Agricultural crop analysis
- Wildlife monitoring and conservation
