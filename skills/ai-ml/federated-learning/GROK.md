---
name: "federated-learning"
category: "ai-ml"
version: "2.0.0"
tags: ["ai-ml", "federated-learning", "privacy", "distributed", "differential-privacy", "secure-aggregation"]
---

# Federated Learning

## Overview

Privacy-preserving federated learning framework for training machine learning models across decentralized data sources without sharing raw data. This module implements FedAvg, FedProx, Scaffold, and personalized federated learning algorithms with built-in differential privacy, secure aggregation, communication compression, and heterogeneous device management. Supports cross-silo (enterprise) and cross-device (mobile/IoT) federated learning topologies with Byzantine-robust aggregation and non-IID data handling.

## Core Capabilities

- **Federated Averaging (FedAvg)**: Standard federated averaging with configurable local epochs and learning rate schedules
- **FedProx**: Proximal term regularization for handling heterogeneous data distributions across clients
- **SCAFFOLD**: Variance-reduced federated learning with client control variates
- **Differential Privacy**: (ÃŽÂµ, ÃŽÂ´)-differential privacy with per-round and cumulative privacy accounting
- **Secure Aggregation**: Cryptographic secure aggregation preventing server from seeing individual client updates
- **Communication Compression**: Gradient compression via top-k sparsification, quantization, and error feedback
- **Byzantine Robustness**: Robust aggregation rules (Krum, trimmed mean, median) for hostile client detection
- **Personalization**: Per-client model personalization via meta-learning, local fine-tuning, and mixture-of-experts

## Usage

```python
from federated_learning import (
    FederatedServer, FederatedClient, FedAlgorithm, PrivacyBudget
)

# Configure federated learning server
server = FederatedServer(
    algorithm=FedAlgorithm.FEDAVG,
    global_model="resnet50",
    num_rounds=100,
    clients_per_round=10,
    min_clients=5,
    rounds_before_exit=10,
)

# Configure privacy
server.configure_privacy(
    epsilon=8.0,
    delta=1e-5,
    max_grad_norm=1.0,
    noise_multiplier=1.1,
)

# Add clients
for i in range(50):
    server.add_client(
        client_id=f"client_{i}",
        data_samples=1000 + i * 100,
        compute_power="medium",
        connection_type="wifi",
    )

# Run federated training
result = server.train()
print(f"Global accuracy: {result.final_accuracy:.4f}")
print(f"Communication rounds: {result.total_rounds}")
print(f"Privacy spent: ÃŽÂµ={result.privacy_spent.epsilon:.2f}, ÃŽÂ´={result.privacy_spent.delta:.2e}")
print(f"Total communication: {result.total_communication_mb:.1f} MB")
```

```python
# Federated client
client = FederatedClient(
    client_id="client_0",
    local_data="data/client_0/",
    local_epochs=5,
    learning_rate=0.01,
    batch_size=32,
)
client.train_local(global_model)
update = client.get_update()
print(f"Local accuracy: {update.local_accuracy:.4f}")
print(f"Update size: {update.update_size_mb:.2f} MB")
```

## Best Practices

- Use FedProx or SCAFFOLD when data is non-IID across clients Ã¢â‚¬â€ FedAvg struggles with heterogeneous data
- Set differential privacy budget (ÃŽÂµ) before training starts Ã¢â‚¬â€ privacy loss is cumulative across rounds
- Use secure aggregation when client updates could reveal sensitive information about local data
- Compress gradients for cross-device FL where bandwidth is limited (top-k sparsification works well)
- Monitor for Byzantine clients using Krum or trimmed mean aggregation in open federation settings
- Start with 10-20% of clients per round to balance communication cost and convergence speed
- Use learning rate warmup for the first 5-10 rounds to stabilize early training
- Implement early stopping based on validation accuracy on a small shared held-out dataset
- Log per-client metrics to detect free-riders and stragglers in the federation
- Use FedBN (federated batch normalization) when local batch statistics vary significantly across clients

## Related Modules

- **model-optimization** Ã¢â‚¬â€ Compress federated updates for efficient communication
- **model-deployment** Ã¢â‚¬â€ Deploy federated models to edge devices
- **ai-ml** Ã¢â€ â€™ **neural-architecture-search** Ã¢â‚¬â€ Federated NAS for privacy-preserving architecture search
- **api-security** Ã¢â‚¬â€ Secure communication channels for federated coordination
- **zero-trust** Ã¢â€ â€™ **security-framework** Ã¢â‚¬â€ Zero-trust principles for federated infrastructure

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

## Advanced Federated Algorithms

### FedProx Deep Dive

| Parameter | Description | Typical Value |
|-----------|-------------|---------------|
| mu | Proximal coefficient | 0.01 - 1.0 |
| Local LR | Client learning rate | 0.01 - 0.1 |
| Local Epochs | Steps per round | 1 - 20 |
| Batch Size | Client batch size | 32 - 128 |

### SCAFFOLD Algorithm

```python
from federated_learning import SCAFFOLD, ControlVariates

server = SCAFFOLD(
    global_model="resnet50",
    num_rounds=100,
    clients_per_round=10,
    variance_reduction=True,
    control_variate_momentum=0.9,
)

# Server tracks global control variate
server.init_control_variates()

# Training with variance reduction
result = server.train()
print(f"Convergence speedup: {result.convergence_speedup:.1f}x vs FedAvg")
```

### FedNova (Normalized Averaging)

| Feature | FedAvg | FedNova |
|---------|--------|---------|
| Local steps | Fixed | Variable |
| Averaging | Weighted by data | Normalized by steps |
| Heterogeneity | Poor | Good |
| Convergence | Slower | Faster |

## Differential Privacy Deep Dive

### Privacy Accounting Methods

| Method | Tightness | Speed | Memory |
|--------|-----------|-------|--------|
| Basic composition | Loose | Fast | Low |
| Advanced composition | Better | Fast | Low |
| RDP accountant | Tight | Medium | Medium |
| zCDP | Tight | Fast | Low |

### Privacy Budget Configuration

```python
from federated_learning import PrivacyBudget, PrivacyAccountant

budget = PrivacyBudget(
    epsilon=8.0,
    delta=1e-5,
    accounting_method="rdp",
    rdp_orders=[1 + x / 10.0 for x in range(1, 100)],
)

accountant = PrivacyAccountant(budget)
for round in range(num_rounds):
    accountant.accumulate(
        noise_multiplier=1.1,
        sample_rate=0.1,
        steps=local_epochs,
    )
    print(f"Round {round}: epsilon={accountant.epsilon:.2f}")
```

### Per-Round Privacy Loss

| Round | Noise Multiplier | Sample Rate | Delta Epsilon |
|-------|------------------|-------------|---------------|
| 1 | 1.1 | 0.1 | 0.42 |
| 5 | 1.1 | 0.1 | 0.38 |
| 10 | 1.1 | 0.1 | 0.35 |
| 50 | 1.1 | 0.1 | 0.28 |
| 100 | 1.1 | 0.1 | 0.22 |

## Secure Aggregation

### Cryptographic Protocols

| Protocol | Overhead | Security | Communication |
|----------|----------|----------|---------------|
| Secret Sharing | 2-3x | Perfect | 2x |
| Homomorphic | 10-100x | Computational | 1x |
| Trusted Execution | 1.2x | Hardware | 1x |
| Hybrid | 3-5x | Mixed | 2x |

### Secure Aggregation Setup

```python
from federated_learning import SecureAggregation

secagg = SecureAggregation(
    protocol="secret_sharing",
    threshold=0.5,  # Minimum clients needed
    timeout_seconds=300,
    retry_count=3,
)

server = FederatedServer(
    secure_aggregation=secagg,
    min_clients=10,
    clients_per_round=20,
)
```

## Communication Compression

### Gradient Compression Methods

| Method | Compression | Accuracy Impact | Bandwidth |
|--------|-------------|-----------------|-----------|
| Top-K | k/100% | Low | K% of original |
| Random-K | k/100% | Medium | K% of original |
| Quantization | 32x (INT1) | Low | 1/32 of original |
| Error Feedback | Maintains | None | Combined with others |

### Compression Configuration

```python
from federated_learning import GradientCompression

compression = GradientCompression(
    method="topk",
    k_ratio=0.01,  # Keep top 1% of gradients
    error_feedback=True,
    warmup_rounds=5,
    quantization_bits=8,
)

# Apply to client updates
client = FederatedClient(
    gradient_compression=compression,
    upload_bandwidth_mbps=10,
    download_bandwidth_mbps=50,
)
```

## Byzantine Robustness

### Robust Aggregation Rules

| Rule | Fault Tolerance | Complexity | Overhead |
|------|-----------------|------------|----------|
| Krum | f < (n-2)/2 | O(n^2 * d) | Low |
| Trimmed Mean | f < n/4 | O(n * d) | Low |
| Median | f < n/2 | O(n * d) | Low |
| Bulyan | f < n/4 | O(n^2 * d) | Medium |

### Byzantine Client Detection

```python
from federated_learning import ByzantineDetector

detector = ByzantineDetector(
    method="krum",
    num_byzantine=5,
    distance_metric="cosine",
    threshold_percentile=90,
)

# Detect malicious clients
suspicious = detector.detect(client_updates)
for client_id, score in suspicious:
    print(f"Client {client_id}: anomaly score {score:.4f}")
```

## Personalization Methods

### Personalization Strategies

| Method | Communication | Personalization | Complexity |
|--------|---------------|-----------------|------------|
| Per-Client Fine-tuning | Low | High | Low |
| Meta-Learning (MAML) | Medium | High | High |
| Mixture-of-Experts | High | Medium | Medium |
| Clustered FL | Medium | Medium | Medium |
| FedBN | Low | Medium | Low |

### Personalization Configuration

```python
from federated_learning import PersonalizationConfig

personalization = PersonalizationConfig(
    strategy="maml",
    inner_lr=0.01,
    inner_steps=5,
    meta_lr=0.001,
    personalization_layers=["layer3", "layer4", "fc"],
    mixture_experts=4,
)

server = FederatedServer(
    global_model="resnet50",
    personalization=personalization,
)
```

## Non-IID Data Handling

### Data Distribution Strategies

| Type | Description | Challenge |
|------|-------------|-----------|
| IID | Balanced, random | None |
| Pathological | Some classes missing | Severe |
| Quantity Skew | Unequal samples | Medium |
| Label Distribution | Unequal label ratios | High |
| Feature Shift | Different distributions | High |

### Non-IID Mitigation

```python
from federated_learning import NonIIDHandler

handler = NonIIDHandler(
    strategy="fedprox",
    mu=0.1,
    adaptive_lr=True,
    lr_scaling="linear",
    batch_norm_correction=True,
)

# Monitor non-IIDÃ§Â¨â€¹Ã¥ÂºÂ¦
divergence = handler.measure_divergence(clients_data)
print(f"Mean JS divergence: {divergence.mean:.4f}")
print(f"Max JS divergence: {divergence.max:.4f}")
```

## Cross-Device vs Cross-Silo

### Comparison Table

| Aspect | Cross-Device | Cross-Silo |
|--------|--------------|------------|
| Client count | 10K - 10M | 10 - 1000 |
| Reliability | Low | High |
| Bandwidth | Limited | Abundant |
| Compute | Heterogeneous | Homogeneous |
| Drop rate | 30-50% | 0-5% |
| Privacy need | High | Medium |

### Cross-Device Configuration

```python
from federated_learning import CrossDeviceConfig

config = CrossDeviceConfig(
    clients_per_round=100,
    min_completion_rate=0.6,
    timeout_seconds=300,
    client_sampling="poisson",
    selection_rate=0.01,
    speed_normalization=True,
)
```

## Federated Learning Metrics

### Convergence Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Communication rounds | Steps to convergence | < 200 |
| Total communication | MB transferred | < 1000 MB |
| Client participation | Average % per round | > 10% |
| Privacy budget used | Cumulative epsilon | < 10 |

### Monitoring Dashboard

```python
from federated_learning import FLDashboard

dashboard = FLDashboard(
    metrics=[
        "global_accuracy", "local_accuracy", "communication_cost",
        "privacy_spent", "client_participation", "convergence_rate",
    ],
    export_format="html",
)

dashboard.log_round(round_metrics)
report = dashboard.generate_report()
```

## Advanced Federated Architectures

### Hierarchical Federated Learning

```
Level 1: Edge Devices (1000s)
    |
Level 2: Edge Servers (100s)
    |
Level 3: Cloud Server (1)
```

### Federated Transfer Learning

```python
from federated_learning import FederatedTransfer

transfer = FederatedTransfer(
    source_task="imagenet_classification",
    target_task="medical_imaging",
    adaptation_layers=["fc", "layer4"],
    num_rounds=50,
)
```

## Common Pitfalls

| Issue | Symptom | Solution |
|-------|---------|----------|
| Client drift | Accuracy oscillates | FedProx, SCAFFOLD |
| Privacy budget exhaustion | High epsilon | Reduce rounds, increase noise |
| Slow convergence | Many rounds needed | SCAFFOLD, adaptive LR |
| Communication bottleneck | Slow training | Gradient compression |
| Byzantine attack | Accuracy drop | Krum, trimmed mean |

## Future Directions

- **Federated Foundation Models**: Training large language models across organizations
- **Federated Reinforcement Learning**: Multi-agent RL with privacy
- **Cross-Platform FL**: Interoperable federated learning
- **Federated Unlearning**: Forgetting specific data contributions


## Additional Resources

### Related Technologies

This module integrates with industry-standard tools and frameworks. Refer to the official documentation for the latest API references and configuration options.

### Community and Support

- Open source contributions welcome
- Issue tracking via GitHub Issues
- Documentation updated with each release
- Community forums for discussion and support

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-01 | Initial release |
| 1.1.0 | 2026-03-15 | Enhanced configuration options |
| 1.2.0 | 2026-06-01 | Performance improvements |
| 2.0.0 | 2026-07-01 | Major architecture update |

### License

MIT License - Copyright (c) 2026 Awesome Grok Skills


## Extended Reference

### Configuration Matrix

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enabled | bool | true | Enable the module |
| log_level | str | INFO | Logging verbosity |
| timeout | int | 30 | Operation timeout in seconds |
| max_retries | int | 3 | Maximum retry attempts |
| cache_ttl | int | 3600 | Cache time-to-live in seconds |
| batch_size | int | 100 | Records per batch |
| parallel_workers | int | 4 | Concurrent worker threads |
| memory_limit | str | 512MB | Maximum memory allocation |
| disk_threshold | float | 0.8 | Disk usage alert threshold |
| health_check_interval | int | 60 | Health check frequency seconds |

### Environment Variables

`ash
MODULE_ENABLED=true
MODULE_LOG_LEVEL=INFO
MODULE_TIMEOUT=30
MODULE_MAX_RETRIES=3
MODULE_CACHE_TTL=3600
MODULE_BATCH_SIZE=100
MODULE_PARALLEL_WORKERS=4
MODULE_MEMORY_LIMIT=512MB
MODULE_DISK_THRESHOLD=0.8
MODULE_HEALTH_CHECK_INTERVAL=60
```n
### Docker Configuration

`yaml
version: '3.8'
services:
  module:
    image: awesome-grok/module:latest
    environment:
      - MODULE_ENABLED=true
      - MODULE_LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    ports:
      - '8080:8080'
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8080/health']
      interval: 30s
      timeout: 10s
      retries: 3
```n
### Kubernetes Deployment

`yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: module-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: module
  template:
    metadata:
      labels:
        app: module
    spec:
      containers:
      - name: module
        image: awesome-grok/module:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: 256Mi
            cpu: 250m
          limits:
            memory: 512Mi
            cpu: 500m
```n
### Prometheus Metrics

`yaml
scrape_configs:
  - job_name: 'module'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: /metrics
    scrape_interval: 15s
```n
### Grafana Dashboard

Import dashboard ID 12345 from Grafana.com for pre-configured monitoring panels including request rate, error rate, latency percentiles, and resource utilization.

### Alert Rules

`yaml
groups:
  - name: module-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(module_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(module_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
```n
### CI/CD Pipeline

`yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v
      - run: python -m mypy src/
      - run: python -m ruff check src/
```n
