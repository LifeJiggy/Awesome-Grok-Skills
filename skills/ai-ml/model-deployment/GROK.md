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
