---
name: "neural-architecture-search"
category: "ai-ml"
version: "2.0.0"
tags: ["ai-ml", "neural-architecture-search", "automl", "hyperparameters", "model-search", "darts"]
---

# Neural Architecture Search

## Overview

Automated Neural Architecture Search (NAS) framework for discovering optimal deep learning model architectures. This module implements multiple search strategies including differentiable architecture search (DARTS), evolutionary algorithms, reinforcement learning-based search, and Bayesian optimization over architecture hyperparameters. Supports search spaces for convolutional networks, transformers, and hybrid architectures with multi-objective optimization for accuracy, latency, parameter count, and FLOPs. Integrates with PyTorch and TensorFlow for architecture evaluation and provides searchable cell-based and macro-level architecture definitions.

## Core Capabilities

- **DARTS Search**: Differentiable Architecture Search with continuous relaxation for efficient gradient-based architecture optimization
- **Evolutionary NAS**: Population-based architecture search with mutation, crossover, and tournament selection
- **Bayesian Optimization**: Gaussian process-based search over discrete architecture hyperparameters
- **Multi-Objective Optimization**: Pareto-optimal search balancing accuracy, latency, parameters, and energy consumption
- **Search Space Definition**: Configurable cell-based, hierarchical, and macro-level architecture search spaces
- **Weight Sharing**: One-shot NAS with supernet training and architecture evaluation without retraining
- **Hardware-Aware NAS**: Architecture search conditioned on target deployment hardware constraints
- **Transfer Learning**: Warm-start architecture search from previously discovered architectures

## Usage

```python
from neural_architecture_search import (
    NASConfig, SearchSpace, DARTSSearch, EvolutionaryNAS, SearchStrategy
)

# Define search space
search_space = SearchSpace(
    operations=["conv_3x3", "conv_5x5", "depthwise_conv", "max_pool", "avg_pool", "skip_connect", "none"],
    nodes_per_cell=4,
    num_cells=8,
    cell_types=["reduction", "normal"],
)

# Configure DARTS search
config = NASConfig(
    strategy=SearchStrategy.DARTS,
    search_space=search_space,
    epochs=50,
    batch_size=64,
    learning_rate=0.025,
    weight_decay=3e-4,
    target_accuracy=0.95,
    max_parameters=5_000_000,
    max_latency_ms=10.0,
    dataset="cifar10",
    gpus=4,
)

# Run search
searcher = DARTSSearch(config)
result = searcher.search()
print(f"Best architecture: {result.architecture_id}")
print(f"Accuracy: {result.accuracy:.4f}")
print(f"Parameters: {result.parameter_count:,}")
print(f"Latency: {result.latency_ms:.1f}ms")
print(f"Architecture: {result.genotype}")
```

```python
# Evolutionary search
evo_search = EvolutionaryNAS(config)
result = evo_search.search(
    population_size=50,
    generations=100,
    mutation_rate=0.3,
    crossover_rate=0.5,
    tournament_size=5,
)
print(f"Best: {result.accuracy:.4f} ({result.parameter_count:,} params)")
for arch in result.pareto_front:
    print(f"  {arch.accuracy:.4f} | {arch.parameter_count:,} params | {arch.latency_ms:.1f}ms")
```

## Best Practices

- Start with DARTS for quick results, then refine with evolutionary search for better Pareto fronts
- Use weight sharing (one-shot NAS) to reduce search cost from GPU-months to GPU-hours
- Always evaluate final architectures with full training from scratch — supernet rankings can be inaccurate
- Set hardware constraints early in the search to avoid discovering impractical architectures
- Use progressive search space pruning to focus compute on promising architecture families
- Monitor the search for collapse to skip connections — DARTS is known for this failure mode
- Cache architecture evaluations to avoid redundant training runs during evolutionary search
- Report results on standard benchmarks (ImageNet, CIFAR-10) for comparability with literature
- Consider latency on target hardware, not just FLOPs — memory bandwidth is often the bottleneck
- Use multi-objective optimization when deployment constraints matter (edge, mobile, cloud)

## Related Modules

- **model-optimization** — Prune, quantize, and distill discovered architectures
- **model-deployment** — Deploy NAS-discovered architectures to production
- **automl** — Broader AutoML pipeline that includes NAS as a component
- **federated-learning** — Federated NAS for privacy-preserving architecture search
- **ai-ml** → **neural-architecture-search** — Complementary architecture design tools

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

## Advanced Search Strategies

### DARTS Variants

| Variant | Description | Key Innovation |
|---------|-------------|----------------|
| DARTS | Original differentiable search | Continuous relaxation |
| P-DARTS | Progressive depth search | Gradual depth increase |
| SDARTS | Stochastic DARTS | Probability-based selection |
| GDAS | Gumbel-DARTS | Gumbel-Softmax sampling |
| ProxylessNAS | Direct hardware-aware | Target-specific latency |

### Evolutionary Algorithms

```python
from neural_architecture_search import EvolutionaryConfig, GeneticOperators

config = EvolutionaryConfig(
    population_size=100,
    generations=200,
    tournament_size=5,
    elite_count=10,
    operators=GeneticOperators(
        mutation_rate=0.15,
        crossover_rate=0.7,
        swap_nodes=3,
        add_skip_probability=0.1,
        remove_layer_probability=0.05,
    ),
)
```

### Bayesian Optimization Search

```python
from neural_architecture_search import BayesianSearch, AcquisitionFunction

search = BayesianSearch(
    search_space=space,
    n_initial_points=20,
    acquisition_function=AcquisitionFunction.EI,
    n_iterations=150,
    surrogate_model="gp",
)
result = search.optimize(objective_function)
```

## Search Space Design

### Cell-Based Search Space

| Component | Options | Default |
|-----------|---------|---------|
| Operations | conv3x3, conv5x5, depthwise, maxpool, avgpool, skip | All |
| Nodes per cell | 2, 4, 6 | 4 |
| Cell count | 6, 8, 12 | 8 |
| Reduction freq | Every 2, 3, 4 cells | Every 3 |

### Macro-Level Search

| Dimension | Range | Impact |
|-----------|-------|--------|
| Depth | 8-32 layers | Model capacity |
| Width | 16-256 channels | Feature richness |
| Skip connections | 0-50% | Gradient flow |
| Attention heads | 1-16 | Context modeling |

## Evaluation Metrics

### Accuracy Metrics
- **Top-1 Accuracy**: Standard classification metric
- **Top-5 Accuracy**: For ImageNet-scale problems
- **F1 Score**: For imbalanced datasets

### Efficiency Metrics
- **FLOPs**: Floating-point operations
- **Parameters**: Model size in bytes
- **Latency**: Inference time on target hardware
- **Energy**: Power consumption (Joules per inference)

### Pareto Front Visualization

```python
import matplotlib.pyplot as plt

def plot_pareto(results):
    accs = [r.accuracy for r in results]
    params = [r.parameter_count for r in results]
    latencies = [r.latency_ms for r in results]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].scatter(params, accs, c='blue', alpha=0.6)
    axes[0].set_xlabel('Parameters')
    axes[0].set_ylabel('Accuracy')

    axes[1].scatter(latencies, accs, c='green', alpha=0.6)
    axes[1].set_xlabel('Latency (ms)')
    axes[1].set_ylabel('Accuracy')

    axes[2].scatter(params, latencies, c='red', alpha=0.6)
    axes[2].set_xlabel('Parameters')
    axes[2].set_ylabel('Latency (ms)')

    plt.tight_layout()
    plt.savefig('pareto_front.png')
```

## Hardware-Aware NAS

### Target Platforms

| Platform | Constraints | Typical Latency Target |
|----------|-------------|----------------------|
| Mobile (ARM) | < 50MB, < 10ms | 5-10ms |
| Edge (NPU) | < 10MB, < 5ms | 1-5ms |
| Cloud GPU | < 500MB, < 1ms | 0.1-1ms |
| Embedded | < 1MB, < 20ms | 10-20ms |

### Latency Lookup Table

```python
from neural_architecture_search import LatencyPredictor

predictor = LatencyPredictor(
    platform="mobile_arm",
    calibration_data="latency_measurements.json",
)

# Predict latency without running on device
latency = predictor.predict(
    operation="conv_3x3",
    input_channels=64,
    output_channels=128,
    resolution=224,
)
print(f"Predicted latency: {latency:.2f}ms")
```

## Distributed Search

### Multi-GPU Configuration

```yaml
distributed_search:
  strategy: "darts"
  num_gpus: 8
  sync_interval: 1
  gradient_compression: "topk"
  topk_ratio: 0.01
  communication_backend: "nccl"
```

### Serverless Search

```python
from neural_architecture_search import ServerlessSearch

search = ServerlessSearch(
    max_workers=100,
    cost_budget=500.0,  # dollars
    cloud_provider="aws",
    instance_type="p3.2xlarge",
)
result = search.run(config)
```

## Experiment Tracking

### MLflow Integration

```python
import mlflow
from neural_architecture_search import NASWithTracking

nas = NASWithTracking(
    config=config,
    experiment_name="nas-search-001",
    tracking_uri="http://mlflow-server:5000",
)

result = nas.search()
mlflow.log_artifact("best_architecture.json")
```

### Weights & Biases

```python
import wandb

wandb.init(project="nas-search", config=config)
wandb.log({
    "accuracy": result.accuracy,
    "params": result.parameter_count,
    "latency": result.latency_ms,
    "architecture": result.genotype,
})
```

## Advanced Techniques

### Zero-Cost NAS

| Method | Description | Speed |
|--------|-------------|-------|
| SynFlow | Path-norm pruning | 100x faster |
| NASWOT | Network density | 50x faster |
| GradNorm | Gradient magnitude | 30x faster |
| Jacobian Cov | Feature diversity | 20x faster |

### One-Shot NAS

```python
from neural_architecture_search import OneShotNAS

# Train supernet once
supernet = OneShotNAS(search_space)
supernet.train(epochs=100)

# Sample and evaluate architectures
for _ in range(1000):
    arch = supernet.sample_architecture()
    accuracy = supernet.evaluate(arch, skip_training=True)
    results.append((arch, accuracy))

# Get best without retraining
best = max(results, key=lambda x: x[1])
```

### Differentiable NAS Extensions

```python
from neural_architecture_search import DARTSExtended

darts = DARTSExtended(
    search_space=space,
    alpha_decay=0.999,  # Architecture parameter decay
    regularization="l1",
    early_stop_rounds=20,
    gradient_clip=5.0,
)
```

## Common Pitfalls

| Issue | Symptom | Solution |
|-------|---------|----------|
| Collapse to skip | All ops become skip_connect | Add regularization, use GDAS |
| Overfitting search set | High search acc, low final | Use separate search/val sets |
| Slow convergence | Loss plateaus early | Increase LR, add warmup |
| Memory overflow | OOM during search | Reduce batch, use gradient checkpointing |
| Unfair comparison | Different training protocols | Standardize final training |

## Case Studies

### ImageNet MobileNAS

| Model | Top-1 Acc | Params | Latency (ms) |
|-------|-----------|--------|--------------|
| MobileNetV2 | 72.0% | 3.4M | 6.2 |
| NAS-discovered | 74.8% | 3.1M | 5.8 |
| EfficientNet-B0 | 77.1% | 5.3M | 7.1 |

### CIFAR-10 DARTS

| Search Method | Final Acc | Search Cost (GPU hrs) |
|---------------|-----------|----------------------|
| Random Search | 93.5% | 10 |
| DARTS | 97.0% | 24 |
| GDAS | 97.1% | 18 |
| Evolutionary | 97.3% | 200 |

## Future Directions

- **Hardware-software co-design**: Joint search for architectures and accelerators
- **Multi-task NAS**: Architectures optimized for multiple objectives
- **Transferable NAS**: Search once, deploy everywhere
- **Green NAS**: Carbon-aware architecture search scheduling

## Search Space Pruning

### Pruning Strategies

| Strategy | Speedup | Accuracy Impact | When to Use |
|----------|---------|-----------------|-------------|
| Low-fidelity | 10-100x | Medium | Initial exploration |
| Learning curve | 5-20x | Low | Mid-search |
| Performance prediction | 50-200x | Low | Large search spaces |
| Transfer learning | 10-50x | Low | Related tasks available |

### Progressive Search Space Pruning

```python
from neural_architecture_search import ProgressivePruning

pruner = ProgressivePruning(
    initial_space_size=10000,
    stages=[
        {"prune_ratio": 0.5, "fidelity": 5},
        {"prune_ratio": 0.3, "fidelity": 10},
        {"prune_ratio": 0.2, "fidelity": 20},
    ],
    metric="proxy_accuracy",
)

pruned_space = pruner.prune(search_space)
print(f"Reduced from {initial_size} to {len(pruned_space)} architectures")
```

## NAS Benchmarks

### Standard Benchmarks

| Dataset | Task | State-of-the-Art | Search Cost |
|---------|------|------------------|-------------|
| CIFAR-10 | Classification | 97.3% | 200 GPU-hrs |
| CIFAR-100 | Classification | 82.5% | 300 GPU-hrs |
| ImageNet | Classification | 82.0% top-1 | 2000 GPU-hrs |
| Penn Treebank | Language Modeling | 55.7 PPL | 50 GPU-hrs |
| WikiText-103 | Language Modeling | 28.0 PPL | 500 GPU-hrs |

### NAS-Bench-201

```python
from neural_architecture_search import NASBench201

bench = NASBench201()
# Query architecture performance without training
arch = bench.get_architecture(arch_id=42)
print(f"Accuracy: {arch.cifar10_accuracy:.4f}")
print(f"FLOPs: {arch.flops:.2e}")
print(f"Params: {arch.params:,}")
```

## NAS for Specific Domains

### Object Detection NAS

| Component | Search Space | Latency Budget |
|-----------|--------------|----------------|
| Backbone | EfficientNet variants | 5-20ms |
| Neck | FPN variants | 2-5ms |
| Head | RetinaNet variants | 3-10ms |

### Semantic Segmentation NAS

| Component | Search Space | Resolution |
|-----------|--------------|------------|
| Encoder | MobileNetV3 variants | 512x512 |
| Decoder | UNet variants | 512x512 |
| Head | DeepLabV3 variants | 512x512 |

### NLP NAS

| Component | Search Space | Vocabulary |
|-----------|--------------|------------|
| Embedding | Transformer variants | 30K |
| Encoder | BERT variants | 512 tokens |
| Pooler | Attention variants | 768 dim |
