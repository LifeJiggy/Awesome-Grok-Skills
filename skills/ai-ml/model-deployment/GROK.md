---
name: "model-deployment"
category: "ai-ml"
version: "2.0.0"
tags: ["ai-ml", "model-deployment", "mlops", "serving", "inference", "monitoring", "a-b-testing"]
---

# Model Deployment

## Overview

End-to-end MLOps platform for deploying, serving, monitoring, and managing machine learning models in production. This model covers model packaging (ONNX, TorchScript, SavedModel), inference serving (REST, gRPC, batch), A/B testing, canary deployments, shadow mode, model versioning, drift detection, performance monitoring, and automated rollback. Supports GPU and CPU inference with dynamic batching, model compression for edge deployment, and integration with Kubernetes, Docker, and cloud ML platforms.

## Core Capabilities

- **Model Packaging**: Convert models to ONNX, TorchScript, SavedModel, or TensorRT formats with optimization passes
- **Inference Serving**: REST API, gRPC, and batch inference endpoints with dynamic batching and auto-scaling
- **A/B Testing**: Traffic splitting between model versions with statistical significance testing
- **Canary Deployment**: Gradual rollout with automated rollback on metric degradation
- **Shadow Mode**: Run new models alongside production without affecting users, comparing outputs
- **Model Registry**: Versioned model storage with lineage tracking, metadata, and artifact management
- **Drift Detection**: Data drift, concept drift, and prediction drift monitoring with automated alerts
- **Performance Monitoring**: Latency percentiles, throughput, error rates, and resource utilization tracking

## Usage

```python
from model_deployment import (
    ModelServer, DeploymentConfig, ABTest, DriftDetector, ModelRegistry
)

# Register a model
registry = ModelRegistry()
model_version = registry.register(
    model_path="model_v2.onnx",
    model_name="fraud-detector",
    version="2.0.0",
    metrics={"auc": 0.985, "f1": 0.94},
    tags={"team": "ml-ops", "framework": "onnx"},
)
print(f"Registered: {model_version.model_name}:{model_version.version}")

# Deploy with canary
config = DeploymentConfig(
    model_name="fraud-detector",
    version="2.0.0",
    replicas=3,
    cpu_limit="2.0",
    memory_limit="4Gi",
    gpu_count=1,
    max_batch_size=32,
    timeout_ms=100,
    canary_percentage=10,
    auto_rollback=True,
)

server = ModelServer(config)
endpoint = server.deploy()
print(f"Deployed at: {endpoint.url}")
print(f"Health: {endpoint.health_status}")

# Monitor
drift = DriftDetector(baseline="train_distribution.json")
alerts = drift.check(prediction_stream=endpoint.prediction_log)
for alert in alerts:
    print(f"DRIFT: {alert.description}")
```

```python
# A/B test
ab_test = ABTest(
    name="fraud-v2-test",
    model_a="fraud-detector:1.0.0",
    model_b="fraud-detector:2.0.0",
    traffic_split=0.5,
    min_samples=1000,
    significance_level=0.05,
    primary_metric="auc",
)
ab_result = ab_test.evaluate()
print(f"Winner: {ab_result.winner}")
print(f"Improvement: {ab_result.improvement_pct:.2f}%")
print(f"p-value: {ab_result.p_value:.4f}")
print(f"Statistically significant: {ab_result.is_significant}")
```

## Best Practices

- Always validate model format compatibility before deploying — test inference locally first
- Use canary deployments (5-10% traffic) for at least 24 hours before full rollout
- Implement automated rollback triggered by latency spikes or accuracy drops
- Monitor input data distributions — data drift causes silent model degradation
- Use shadow mode for high-stakes models (fraud, medical) before production traffic
- Version every model artifact, preprocessing pipeline, and configuration together
- Set SLAs for inference latency (p99 < 100ms) and alert when violated
- Keep a rollback window of at least 3 model versions for quick recovery
- Log all predictions with input features for debugging and retraining data collection
- Use ONNX Runtime for cross-framework serving consistency

## Related Modules

- **model-optimization** — Optimize models for production inference performance
- **neural-architecture-search** — Discover efficient architectures for deployment
- **automl** — Automated model development feeding into deployment pipeline
- **api** → **api-monitoring** — API-level monitoring complementing model monitoring
- **api-gateway** → **load-balancing** — Load balancing for model serving endpoints

## Advanced Configuration

### YAML Configuration
```yaml
version: "2.0.0"
settings:
  mode: "production"
  concurrency: 4
  timeout_ms: 30000
  compute:
    gpus: 4
    distributed: true
    backend: "nccl"
```

### JSON Configuration
```json
{"version":"2.0.0","settings":{"mode":"production","compute":{"gpus":4,"distributed":true}}}
```

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `SKILL_MODE` | Runtime mode | `production` |
| `SKILL_GPUS` | Number of GPUs | `1` |
| `SKILL_TIMEOUT` | Timeout (ms) | `30000` |
| `CUDA_VISIBLE_DEVICES` | GPU device IDs | `all` |
| `SKILL_MODEL_PATH` | Model storage path | `/models` |

## Architecture Patterns

### System Architecture
```
+---------------------------------------------------+
|                   Client Layer                     |
|  +----------+  +----------+  +------------------+  |
|  |  Web UI  |  | CLI Tool |  |  Python SDK      |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
+-------------------+-------------------------------+
|              Compute Layer                         |
|  +----------+  +----------+  +------------------+  |
|  |  GPU     |  | Training |  |  Inference       |  |
|  |  Manager |  | Scheduler|  |  Engine          |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
+-------------------+-------------------------------+
|          Orchestration Layer                       |
|  +----------+  +----------+  +------------------+  |
|  | Job      |  | Resource |  |  Experiment      |  |
|  | Queue    |  | Pool     |  |  Tracker         |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
+-------------------+-------------------------------+
|                 Data Layer                          |
|  +----------+  +----------+  +------------------+  |
|  |  Model   |  | Dataset  |  |  Artifact        |  |
|  |  Store   |  | Store    |  |  Registry        |  |
|  +----------+  +----------+  +------------------+  |
+---------------------------------------------------+
```

### Training Pipeline
```
Data -> Preprocess -> Augment -> Batch -> Train -> Evaluate -> Deploy
  |         |           |        |       |         |
  |    [Normalize]  [Transform] [Loader] [Loop]  [Metrics]
  +---------+-----------+--------+-------+---------+
                   Experiment Tracking
```

## Integration Guide

### ML Platforms
```python
import mlflow
mlflow.set_experiment("skill-experiment")
with mlflow.start_run():
    mlflow.log_params(config)
    result = skill.process(input_data)
    mlflow.log_metrics(result.metrics)
```

### Kubeflow Pipeline
```python
from kfp import dsl

@dsl.pipeline(name="skill-pipeline")
def skill_pipeline():
    preprocess = dsl.ContainerOp(name="preprocess", image="skill-preprocess:latest")
    train = dsl.ContainerOp(name="train", image="skill-train:latest")
    deploy = dsl.ContainerOp(name="deploy", image="skill-deploy:latest")
    train.after(preprocess)
    deploy.after(train)
```

## Performance Optimization

### Benchmarks
| Operation | Throughput | Latency (p50) | Latency (p99) |
|-----------|-----------|---------------|---------------|
| Training (batch) | 1000 samples/s | 10ms/batch | 50ms/batch |
| Inference (GPU) | 10,000 inf/s | 0.1ms | 1ms |
| Inference (CPU) | 1,000 inf/s | 1ms | 10ms |

### Optimization Tips
1. **Mixed Precision**: FP16/BF16 for 2x speedup
2. **Gradient Accumulation**: Simulate large batches
3. **Data Loading**: Multiple workers with pinned memory
4. **Model Compilation**: torch.compile() for inference
5. **Dynamic Batching**: Variable-size inputs

## Security Considerations

### Threat Model
| Threat | Risk | Mitigation |
|--------|------|------------|
| Model poisoning | High | Data validation, provenance |
| Adversarial inputs | High | Input sanitization |
| Model theft | High | Access controls, watermarking |
| Data leakage | High | Differential privacy |

### Security Checklist
- [ ] Training data validated
- [ ] Model artifacts signed
- [ ] Inference endpoints authenticated
- [ ] Differential privacy applied
- [ ] Dependencies scanned

## Troubleshooting Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| CUDA out of memory | Batch too large | Reduce batch, gradient accumulation |
| Training divergence | LR too high | Lower LR, warmup schedule |
| Low accuracy | Underfitting | Larger model, train longer |
| Overfitting | Insufficient reg | Dropout, augmentation |
| Slow inference | No optimization | Quantization, TensorRT |

## API Reference

### `init(config: Config) -> Instance`
Initialize with configuration.

### `train(data: Dataset, config: TrainConfig) -> TrainResult`
Train model on dataset.

### `predict(input: Input) -> Prediction`
Run inference.

### `evaluate(model: str, dataset: Dataset) -> EvalResult`
Evaluate model performance.

## Data Models

### Model Schema
```json
{"type":"object","properties":{"model_id":{"type":"string"},"version":{"type":"string"},"framework":{"type":"string","enum":["pytorch","tensorflow","onnx"]},"metrics":{"type":"object"}}}
```

## Deployment Guide

### Docker
```dockerfile
FROM nvidia/cuda:12.2-runtime-ubuntu22.04
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1
CMD ["python", "-m", "uvicorn", "main:app"]
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: skill-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: skill
  template:
    spec:
      containers:
      - name: skill
        image: skill:2.0.0
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
            nvidia.com/gpu: 1
          limits:
            memory: "4Gi"
            cpu: "2000m"
            nvidia.com/gpu: 1
```

## Monitoring & Observability

| Metric | Type | Description | Alert Threshold |
|--------|------|-------------|-----------------|
| `training_loss` | Gauge | Training loss | Divergence |
| `inference_latency_ms` | Histogram | Inference latency | p99 > 100ms |
| `gpu_utilization` | Gauge | GPU usage | < 50% |
| `gpu_memory_used` | Gauge | GPU memory | > 90% |

## Testing Strategy

```python
def test_train():
    result = skill.train(train_data, config)
    assert result.accuracy > 0.8

def test_predict():
    prediction = skill.predict(test_input)
    assert prediction.confidence > 0.5
```

## Versioning & Migration

- Major version for breaking changes
- 6-month deprecation notice

### Changelog
- **[2.0.0]** -- New architecture
- **[1.5.0]** -- Performance improvements
- **[1.0.0]** -- Initial release

## Glossary

| Term | Definition |
|------|------------|
| **Epoch** | One pass through training data |
| **Batch** | Group of samples processed together |
| **LR** | Learning rate |
| **Quantization** | Reducing model precision |
| **Distillation** | Training smaller from larger model |
| **Pruning** | Removing redundant weights |
| **ONNX** | Open Neural Network Exchange |

## Changelog

### [2.0.0] -- 2024-12-01
- Major release with new architecture

### [1.5.0] -- 2024-06-15
- Performance improvements

### [1.0.0] -- 2024-01-01
- Initial stable release

## Contributing Guidelines

```bash
git clone https://github.com/example/skill.git
cd skill
pip install -e ".[dev]"
pytest
```

## License

MIT License -- Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Advanced Deployment Strategies

### Canary Deployment Configuration

```python
from model_deployment import CanaryDeployment

canary = CanaryDeployment(
    model_name="fraud-detector",
    version="2.0.0",
    canary_percentage=5,
    step_size=5,
    step_interval_minutes=30,
    max_steps=20,
    rollback_threshold=0.02,
    metrics=["latency_p99", "error_rate", "accuracy"],
)

result = canary.deploy()
print(f"Status: {result.status}")
print(f"Current step: {result.current_step}/{result.max_steps}")
```

### Shadow Mode Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| Traffic % | Percentage to shadow | 10% |
| Log predictions | Store shadow outputs | True |
| Compare outputs | Diff with production | True |
| Latency threshold | Max acceptable overhead | 5ms |

### Blue-Green Deployment

```python
from model_deployment import BlueGreenDeployment

deployment = BlueGreenDeployment(
    model_name="recommendation-engine",
    blue_version="1.0.0",
    green_version="2.0.0",
    switch_after_minutes=60,
    auto_switch_if_healthy=True,
    health_check_interval=30,
)

deployment.switch()
```

## Inference Optimization

### Dynamic Batching Configuration

| Parameter | Description | Recommended |
|-----------|-------------|-------------|
| max_batch_size | Max samples per batch | 32-128 |
| max_latency_ms | Max wait for batching | 10-50ms |
| batch_timeout_ms | Timeout to force batch | 5-20ms |
| preferred_batch_size | Optimal batch size | 16-64 |

### Model Compilation

```python
from model_deployment import ModelCompiler

compiler = ModelCompiler(
    target="tensorrt",
    precision="fp16",
    workspace_size_gb=4,
    max_batch_size=64,
    optimization_level="maximum",
)

compiled = compiler.compile("model.onnx")
print(f"Speedup: {compiled.speedup:.1f}x")
print(f"Size reduction: {compiled.size_ratio:.1f}x")
```

## Serving Frameworks Comparison

| Framework | Latency | Throughput | GPU Support | Ease of Use |
|-----------|---------|------------|-------------|-------------|
| TorchServe | Low | High | Yes | Medium |
| TensorFlow Serving | Low | High | Yes | Medium |
| Triton | Very Low | Very High | Yes | Complex |
| ONNX Runtime | Low | High | Yes | Easy |
| BentoML | Medium | High | Yes | Easy |
| FastAPI | Medium | Medium | Manual | Easy |

## A/B Testing Deep Dive

### Statistical Significance

| Metric | Minimum Sample | Significance Level | Power |
|--------|----------------|--------------------|----|
| Conversion rate | 1000 per variant | 0.05 | 0.8 |
| Revenue per user | 500 per variant | 0.05 | 0.8 |
| Latency | 100 per variant | 0.01 | 0.9 |

### A/B Test Configuration

```python
from model_deployment import ABTestConfig

config = ABTestConfig(
    name="model-v2-test",
    model_a="model:1.0.0",
    model_b="model:2.0.0",
    traffic_split=0.5,
    min_samples=1000,
    max_duration_days=14,
    significance_level=0.05,
    power=0.8,
    primary_metric="conversion_rate",
    secondary_metrics=["revenue", "latency", "error_rate"],
)

test = ABTest(config)
result = test.run()
print(f"Winner: {result.winner}")
print(f"p-value: {result.p_value:.4f}")
print(f"Confidence interval: {result.ci_lower:.4f} - {result.ci_upper:.4f}")
```

## Drift Detection Deep Dive

### Drift Types

| Type | Description | Detection Method |
|------|-------------|------------------|
| Data Drift | Input distribution changes | KS test, PSI |
| Concept Drift | P-(Y\|X) changes | ADWIN, DDM |
| Prediction Drift | Output distribution changes | Chi-squared |
| Label Drift | Label distribution changes | KL divergence |

### Drift Detection Configuration

```python
from model_deployment import DriftDetectorConfig

config = DriftDetectorConfig(
    baseline_path="train_distribution.json",
    methods=["psi", "ks_test", "chi_squared"],
    psi_threshold=0.2,
    ks_p_value=0.05,
    window_size=1000,
    alert_cooldown_minutes=60,
)

detector = DriftDetector(config)
alerts = detector.monitor(prediction_stream)
```

## Model Registry

### Version Management

| Feature | Description |
|---------|-------------|
| Lineage tracking | Full model history |
| Artifact storage | Models, configs, data |
| Stage management | Staging, production, archived |
| Metadata search | Query by metrics, tags |

### Registry Configuration

```python
from model_deployment import ModelRegistry

registry = ModelRegistry(
    storage_backend="s3",
    bucket="ml-models",
    prefix="registry/",
)

# Register model
version = registry.register(
    model_path="model_v2.onnx",
    model_name="fraud-detector",
    version="2.0.0",
    metrics={"auc": 0.985},
    tags={"team": "ml-ops", "framework": "onnx"},
    stage="staging",
)

# Promote to production
registry.promote(
    model_name="fraud-detector",
    version="2.0.0",
    stage="production",
    approval="auto",
)
```

## Performance Monitoring

### Latency Monitoring

| Percentile | Description | Alert Threshold |
|------------|-------------|-----------------|
| p50 | Median latency | > 20ms |
| p95 | Tail latency | > 50ms |
| p99 | Extreme tail | > 100ms |
| p99.9 | Outliers | > 500ms |

### Throughput Monitoring

```python
from model_deployment import ThroughputMonitor

monitor = ThroughputMonitor(
    window_seconds=60,
    alert_threshold_rps=100,
    normal_range_rps=(200, 1000),
)

metrics = monitor.get_metrics()
print(f"Current RPS: {metrics.current_rps}")
print(f"Average RPS: {metrics.avg_rps}")
print(f"Peak RPS: {metrics.peak_rps}")
```

## Container Optimization

### Docker Multi-Stage Build

```dockerfile
FROM python:3.10-slim as builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM nvidia/cuda:12.2-runtime-ubuntu22.04
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "main:app"]
```

### Kubernetes Scaling

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: model-server-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: model-server
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: inference_queue_size
      target:
        type: AverageValue
        averageValue: 10
```

## GPU Utilization

### GPU Monitoring

| Metric | Description | Target |
|--------|-------------|--------|
| GPU Utilization | Compute usage | > 80% |
| GPU Memory | Memory usage | < 90% |
| SM Occupancy | Streaming multiprocessor | > 75% |
| Memory Bandwidth | Transfer rate | > 70% of peak |

### Multi-GPU Serving

```python
from model_deployment import MultiGPUServer

server = MultiGPUServer(
    model_path="model.onnx",
    gpus=[0, 1, 2, 3],
    distribution="round_robin",
    max_batch_size=64,
    per_gpu_memory_limit_gb=8,
)

endpoint = server.deploy()
```

## Common Deployment Patterns

### Pattern: Online Inference

```
Request -> Load Balancer -> Inference Server -> Response
              |
              +-> Model A (70%)
              +-> Model B (30%)
```

### Pattern: Batch Inference

```
Data Lake -> Scheduler -> Batch Processor -> Result Store
                |
                +-> Model A (daily)
                +-> Model B (hourly)
```

### Pattern: Streaming Inference

```
Kafka -> Stream Processor -> Inference Engine -> Kafka
              |
              +-> Model A (real-time)
              +-> Model B (near-real-time)
```

## Deployment Decision Tree

```
Start
  |
  +-- Latency requirement < 10ms?
  |     +-- Yes -> GPU serving with TensorRT
  |     +-- No -> Continue
  |
  +-- Throughput > 1000 RPS?
  |     +-- Yes -> Horizontal scaling + load balancing
  |     +-- No -> Continue
  |
  +-- Batch processing acceptable?
  |     +-- Yes -> Batch inference pipeline
  |     +-- No -> Continue
  |
  +-- Edge deployment?
        +-- Yes -> ONNX Runtime / TFLite
        +-- No -> Cloud serving (Triton/TorchServe)
```

## Future Directions

- **Serverless inference**: Scale to zero, pay per request
- **Federated inference**: Inference across distributed nodes
- **Adaptive models**: Dynamic model complexity based on load
- **Green inference**: Carbon-aware inference scheduling
