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
