---
name: "quantum-kernel-methods"
category: "quantum-ml"
version: "1.1.0"
tags: ["quantum-ml", "quantum-kernel-methods", "kernel", "SVM", "feature-map", "QSVM", "kernel-alignment", "quantum-advantage"]
---

# Quantum Kernel Methods

## Overview

Quantum Kernel Methods exploit the exponentially large Hilbert space of quantum systems to construct kernel functions that are intractable to compute classically. A quantum kernel maps classical data into a quantum feature space via a parameterized circuit, estimates inner products between quantum states, and uses these as kernel entries in classical algorithms like Support Vector Machines (SVMs). Quantum kernels can provably outperform classical kernels on specific distributions (e.g., those with hidden parity structure).

The key insight is that quantum circuits can implicitly compute inner products in exponentially large feature spaces. For n qubits, the Hilbert space has dimension 2^n, and a quantum feature map can access this entire space. The kernel value K(x_i, x_j) = |<φ(x_i)|φ(x_j)>|^2 measures the overlap between quantum states prepared from classical inputs x_i and x_j. Computing this classically requires exponential resources, but a quantum computer can estimate it efficiently using techniques like the SWAP test or direct state preparation.

This module provides tools for constructing quantum feature maps, estimating kernel matrices, training Quantum SVMs, and evaluating quantum advantage on classification tasks. Quantum kernels are particularly powerful for datasets with non-trivial geometric structure in high-dimensional spaces, and they integrate seamlessly with classical kernel methods through the kernel trick.

## Core Capabilities

- **Feature map construction**: Build parameterized quantum circuits that embed classical data into quantum Hilbert spaces with configurable depth, entanglement, and gate sets. Supports ZZFeatureMap, PauliFeatureMap, and custom architectures.
- **Kernel matrix estimation**: Compute Gram matrices from quantum circuits via state preparation and overlap measurement using SWAP test, direct fidelity estimation, or classical simulation.
- **Quantum SVM training**: Train kernel-based classifiers (SVM, kernel ridge regression) with precomputed quantum kernel matrices. Supports binary and multi-class classification.
- **Kernel alignment**: Measure and optimize the alignment between quantum kernels and target labels to select optimal feature maps. Alignment score quantifies how well the kernel captures task-relevant structure.
- **Quantum advantage testing**: Benchmark quantum kernels against classical counterparts (RBF, polynomial, Laplacian) on problem distributions. Includes statistical significance testing.
- **Kernel caching**: Cache quantum kernel matrices to avoid redundant circuit execution during hyperparameter search. Supports disk-based caching with LRU eviction.
- **Multiple kernel learning**: Combine multiple quantum kernels with classical ones using weighted sums or tensor products for improved generalization.
- **Kernel visualization**: Plot kernel matrices, eigenvalue spectra, and decision boundaries to diagnose kernel quality and data separability.

## Usage Examples

### Building a Quantum Feature Map

```python
from quantum_kernel_methods import (
    QuantumFeatureMap,
    FeatureMapType,
    FeatureMapConfig,
)

config = FeatureMapConfig(
    n_qubits=4,
    feature_map_type=FeatureMapType.PAULI_Z_Z,
    depth=2,
    entanglement="full",
    data_reuploading=True,
)

fm = QuantumFeatureMap(config)
print(f"Feature map circuit depth: {fm.circuit_depth}")
print(f"Number of parameters: {fm.n_parameters}")
print(f"Gate count: {fm.gate_count}")
print(f"Circuit:\n{fm.draw()}")
```

### Computing a Quantum Kernel Matrix

```python
import numpy as np
from quantum_kernel_methods import QuantumKernel, KernelConfig

config = KernelConfig(
    n_qubits=4,
    feature_map="zzfeaturemap",
    feature_map_depth=2,
    estimator="swap_test",
    shots=1024,
)

kernel = QuantumKernel(config)
X_train = np.random.randn(50, 4)  # 50 samples, 4 features
K = kernel.compute_kernel_matrix(X_train)
print(f"Kernel matrix shape: {K.shape}")
print(f"Kernel diagonal (self-similarities): {np.diag(K)[:5]}")
print(f"Kernel matrix is PSD: {kernel.is_psd(K)}")
print(f"Condition number: {np.linalg.cond(K):.2f}")
```

### Training a Quantum SVM Classifier

```python
from quantum_kernel_methods import QuantumSVM, KernelConfig

config = KernelConfig(
    n_qubits=4,
    feature_map="zzfeaturemap",
    feature_map_depth=3,
    regularization=0.1,
)

qsvm = QuantumSVM(config)
qsvm.fit(X_train, y_train, precomputed_kernel=True)

accuracy = qsvm.score(X_test, y_test)
print(f"QSVM accuracy: {accuracy:.3f}")

# Get decision function for confidence estimation
decisions = qsvm.decision_function(X_test)
print(f"Decision values range: [{decisions.min():.3f}, {decisions.max():.3f}]")

# Cross-validation
cv_scores = qsvm.cross_validate(X, y, k=5)
print(f"CV accuracy: {cv_scores.mean():.3f} +/- {cv_scores.std():.3f}")
```

### Kernel Alignment Score

```python
from quantum_kernel_methods import QuantumKernel, alignment_score

# Compute kernel matrix
kernel = QuantumKernel(config)
K = kernel.compute_kernel_matrix(X_train)

# Alignment with target labels (higher is better)
alignment = alignment_score(K, y_train)
print(f"Kernel-target alignment: {alignment:.4f}")
# alignment > 0.5 suggests the kernel captures task-relevant structure

# Compare alignment across feature map depths
for depth in [1, 2, 3, 4]:
    cfg = KernelConfig(n_qubits=4, feature_map="zzfeaturemap", feature_map_depth=depth)
    k = QuantumKernel(cfg)
    K_mat = k.compute_kernel_matrix(X_train)
    a = alignment_score(K_mat, y_train)
    print(f"Depth {depth}: alignment = {a:.4f}")
```

### Benchmarking Quantum vs Classical Kernels

```python
from quantum_kernel_methods import QuantumKernel, ClassicalKernel, benchmark_kernels

quantum_config = KernelConfig(n_qubits=4, feature_map="zzfeaturemap", depth=2)
classical_configs = {
    "rbf": {"gamma": 0.1},
    "poly": {"degree": 3},
    "laplacian": {"gamma": 0.05},
}

results = benchmark_kernels(
    X_train, y_train, X_test, y_test,
    quantum_config=quantum_config,
    classical_configs=classical_configs,
    n_trials=5,
)

for name, metrics in results.items():
    print(f"{name}: accuracy={metrics['accuracy']:.3f}, "
          f"train_time={metrics['train_time']:.2f}s, "
          f"std={metrics['std']:.4f}")
```

### Caching Kernel Matrices

```python
from quantum_kernel_methods import QuantumKernel, KernelCache

cache = KernelCache(cache_dir="./kernel_cache")
kernel = QuantumKernel(config, cache=cache)

# First call computes and caches
K1 = kernel.compute_kernel_matrix(X_train, cache_key="train_50")

# Second call retrieves from cache
K2 = kernel.compute_kernel_matrix(X_train, cache_key="train_50")
assert np.allclose(K1, K2)
print(f"Cache hit: {cache.hit_rate:.1%}")
print(f"Cache size: {cache.size_bytes / 1024:.1f} KB")

# Evict old entries
cache.evict(max_age_hours=24)
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   Quantum Kernel Pipeline                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  Classical    │───>│   Quantum    │───>│   Kernel     │      │
│  │  Data Input   │    │ Feature Map  │    │  Estimator   │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                    │                    │              │
│    Feature vectors     |φ(x)> states      K(i,j) = |<φ(xi)|   │
│    Normalization       Hilbert space       φ(xj)>|^2           │
│                                                          │       │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Classical   │<───│   Kernel     │<───│  Quantum     │      │
│  │   SVM/Classifier│  │  Matrix      │    │  Circuit     │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                    │                                   │
│    Decision boundary    Gram matrix                             │
│    Support vectors      Positive semi-definite                  │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Kernel Evaluation Methods                    │    │
│  │  ┌─────────┐  ┌──────────┐  ┌───────────────────┐     │    │
│  │  │SWAP Test│  │ Fidelity │  │ Classical Sim     │     │    │
│  │  │ (hardware)│ │ (direct) │  │ (small systems)   │     │    │
│  │  └─────────┘  └──────────┘  └───────────────────┘     │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

The quantum kernel pipeline transforms classical data into quantum states, computes pairwise overlaps to form a Gram matrix, and feeds this matrix into classical kernel methods. The feature map design determines what structures the kernel can capture.

## Best Practices

1. **Match feature map depth to data complexity**: Shallow feature maps (depth 1-2) work for simple datasets. Increase depth only when the kernel alignment score is low, as deeper circuits risk noise-induced degradation on real hardware.

2. **Use data reuploading for expressivity**: Re-encoding input data in each layer (data reuploading) significantly increases the feature map's expressivity without adding more qubits. This is critical for capturing nonlinear decision boundaries.

3. **Normalize kernel matrices**: Always normalize kernel matrices so that K[i,i] = 1. Unnormalized kernels can cause numerical instability in SVM training and misleading alignment scores.

4. **Check kernel matrix properties**: Verify the kernel matrix is positive semi-definite (PSD) and symmetric. Non-PSD matrices from noisy hardware require eigenvalue clipping before SVM training.

5. **Precompute when possible**: Quantum kernel matrix computation is expensive (O(n^2) circuit executions). Precompute and cache the full kernel matrix once, then reuse for hyperparameter search over SVM parameters.

6. **Start with ZZFeatureMap**: The ZZFeatureMap (alternating RZ and ZZ entangling layers) is the most commonly validated quantum feature map. Use it as the default before experimenting with custom maps.

7. **Use the kernel alignment score**: Before committing to expensive quantum SVM training, compute the kernel alignment score. Values above 0.5 indicate the kernel is useful for the task; values below 0.3 suggest trying a different feature map.

8. **Combine quantum and classical kernels**: If a single quantum kernel underperforms, try multiple kernel learning — combine quantum kernels with classical RBF or polynomial kernels via weighted sums. This often yields better results than either alone.

9. **Monitor kernel eigenvalue spectrum**: The eigenvalue spectrum of the kernel matrix reveals its effective dimensionality. Rapidly decaying eigenvalues suggest the kernel is over-parameterized for the dataset.

10. **Validate on small systems first**: Before scaling to many qubits, validate the feature map on small systems (3-4 qubits) where exact classical simulation is feasible. This confirms the kernel captures expected structure.

## Performance Considerations

- **Kernel matrix cost**: Computing K for n samples requires O(n^2) quantum circuit evaluations. For n=1000, this means 1,000,000 circuit executions — precomputation is essential.
- **SWAP test overhead**: The SWAP test requires ancilla qubits and doubles the circuit width. For small systems, classical simulation of the kernel may be faster.
- **Feature map depth**: Each additional depth layer adds O(n) gates (n = qubits). On hardware with limited coherence, keep total depth under 100 gates.
- **Classical simulation threshold**: For n <= 20 qubits, classical simulation of the kernel matrix is feasible. Beyond this, quantum hardware execution is necessary.
- **Cache efficiency**: Disk-based kernel caching reduces redundant computation during hyperparameter search. For datasets with repeated feature maps, cache hit rates can exceed 90%.
- **Batch kernel evaluation**: Group kernel computations by shared circuit structure to maximize quantum hardware utilization and minimize calibration overhead.

## Security Considerations

- **Kernel extraction attacks**: An adversary with query access to a quantum kernel service could attempt to reconstruct the feature map or kernel function. Implement differential privacy or query rate limits.
- **Data leakage in kernel matrices**: The Gram matrix K contains information about all training samples. Ensure K is not exposed in API responses or logs that could leak sensitive data.
- **Model inversion**: Quantum kernel classifiers may be vulnerable to model inversion attacks that reconstruct training data from decision boundaries. Apply privacy-preserving techniques for sensitive applications.
- **Hardware trust**: When executing on cloud quantum hardware, the provider may observe circuit structures. Use blind quantum computing protocols for proprietary feature maps.
- **Reproducibility**: Quantum kernel estimation is stochastic. Use sufficient shots and fixed seeds for reproducible results in regulated domains.

## Related Modules

- `quantum-neural-networks` — Alternative QML approach using variational circuits directly for classification instead of kernel methods
- `variational-circuits` — Low-level parameterized circuit primitives used to construct quantum feature maps
- `quantum-generative-models` — Generative models that share kernel estimation techniques for density modeling
- `quantum-data` — Data encoding utilities and quantum dataset preparation for kernel evaluation

## References

- Havlíček, V., et al. (2019). Supervised learning with quantum-enhanced feature spaces. Nature, 567(7747), 209-212.
- Schuld, M., & Killoran, N. (2019). Quantum machine learning in feature Hilbert spaces. Physical Review Letters, 122(4), 040504.
- Liu, Y., et al. (2021). Quantum kernel methods for machine learning. arXiv:2101.11011.
- Huang, H.-Y., et al. (2021). Power of data in quantum machine learning. Nature Communications, 12(1), 2631.
- Jerbi, S., et al. (2021). Quantum kernel methods: A survey. arXiv:2104.10066.
- Qiskit QSVM tutorial: https://qiskit.org/ecosystem/machine-learning/
- PennyLane kernel module: https://pennylane.ai/qml/glossary/quantum_kernel/

## Advanced Configuration

### Feature Map Parameter Tuning

```python
from quantum_kernel_methods import FeatureMapConfig, TuningStrategy

# Auto-tune feature map parameters
config = FeatureMapConfig(
    n_qubits=4,
    feature_map_type="zzfeaturemap",
    depth=2,
    entanglement="full",
    data_reuploading=True,
    tuning=TuningStrategy.GRID_SEARCH,
    param_ranges={
        "rotation_scale": [0.5, 1.0, 1.5, 2.0],
        "entanglement_strength": [0.1, 0.5, 1.0],
        "reupload_layers": [1, 2, 3],
    },
)

fm = QuantumFeatureMap(config)
fm.tune(X_train, y_train, metric="alignment")
print(f"Best parameters: {fm.best_params}")
print(f"Best alignment: {fm.best_score:.4f}")
```

### Advanced Kernel Configuration

```python
from quantum_kernel_methods import KernelConfig, KernelMethod

config = KernelConfig(
    n_qubits=6,
    feature_map="zzfeaturemap",
    feature_map_depth=3,
    estimator="swap_test",
    shots=4096,
    regularization=0.01,
    kernel_method=KernelMethod.GRAM_MATRIX,
    psd_correction="eigenvalue_clipping",
    eigenvalue_threshold=1e-6,
)

kernel = QuantumKernel(config)
K = kernel.compute_kernel_matrix(X_train)
print(f"Kernel condition number: {np.linalg.cond(K):.2f}")
print(f"PSD eigenvalues: {np.sum(np.linalg.eigvalsh(K) > 0)}/{len(K)}")
```

### Multiple Kernel Learning Configuration

```python
from quantum_kernel_methods import MultipleKernelLearning, KernelCombination

mkl = MultipleKernelLearning(
    kernels=[
        {"type": "quantum", "config": quantum_config_1},
        {"type": "quantum", "config": quantum_config_2},
        {"type": "classical", "kernel": "rbf", "gamma": 0.1},
        {"type": "classical", "kernel": "poly", "degree": 3},
    ],
    combination=KernelCombination.WEIGHTED_SUM,
    optimization="alignment",
)

mkl.fit(X_train, y_train)
print(f"Kernel weights: {mkl.weights}")
print(f"Combined alignment: {mkl.alignment_score:.4f}")
```

### Advanced SVM Configuration

```python
from quantum_kernel_methods import QuantumSVM, SVMConfig

svm_config = SVMConfig(
    kernel="precomputed",
    C=1.0,
    gamma="scale",
    class_weight="balanced",
    probability=True,
    decision_function_shape="ovr",
    cache_size=1000,
    max_iter=10000,
)

qsvm = QuantumSVM(config=svm_config)
qsvm.fit(X_train, y_train, precomputed_kernel=True)

# Get probability estimates
probabilities = qsvm.predict_proba(X_test)
print(f"Probability estimates shape: {probabilities.shape}")
print(f"Prediction confidence: {probabilities.max(axis=1).mean():.3f}")
```

## Architecture Patterns

### Kernel Pipeline Pattern

```python
from quantum_kernel_methods import KernelPipeline, PipelineStage

pipeline = KernelPipeline(stages=[
    PipelineStage(
        name="data_preprocessing",
        type="classical",
        processor=lambda x: StandardScaler().fit_transform(x),
    ),
    PipelineStage(
        name="feature_selection",
        type="classical",
        processor=lambda x: SelectKBest(k=4).fit_transform(x, y),
    ),
    PipelineStage(
        name="quantum_encoding",
        type="quantum",
        processor=lambda x: encode_amplitude(x),
    ),
    PipelineStage(
        name="kernel_computation",
        type="quantum",
        processor=lambda x: compute_swap_test(x),
    ),
    PipelineStage(
        name="svm_training",
        type="classical",
        processor=lambda x: train_svm(x),
    ),
])

result = pipeline.execute(X_train, y_train)
```

### Kernel Cache Strategy Pattern

```python
from quantum_kernel_methods import KernelCache, CacheStrategy

# Multi-level caching
cache = KernelCache(
    strategy=CacheStrategy.MULTI_LEVEL,
    memory_limit_mb=512,
    disk_path="/fast_ssd/kernel_cache",
    ttl_hours=24,
    eviction_policy="lru",
)

kernel = QuantumKernel(config, cache=cache)

# Cache-aware computation
K = kernel.compute_kernel_matrix(
    X_train,
    cache_key="train_100_features",
    force_recompute=False,
)

# Cache statistics
stats = cache.get_stats()
print(f"Hit rate: {stats.hit_rate:.2%}")
print(f"Memory usage: {stats.memory_usage_mb:.1f} MB")
print(f"Disk usage: {stats.disk_usage_mb:.1f} MB")
```

### Kernel Evaluation Strategy Pattern

```python
from quantum_kernel_methods import KernelEvaluator, EvaluationStrategy

evaluator = KernelEvaluator(
    strategy=EvaluationStrategy.CROSS_VALIDATION,
    n_folds=5,
    metrics=["accuracy", "f1", "auc"],
    confidence_level=0.95,
)

# Evaluate kernel quality
results = evaluator.evaluate(
    kernel=kernel,
    X=X_train,
    y=y_train,
)

print(f"Mean accuracy: {results.mean_accuracy:.3f} +/- {results.std_accuracy:.3f}")
print(f"Mean F1: {results.mean_f1:.3f} +/- {results.std_f1:.3f}")
print(f"95% CI for accuracy: [{results.ci_lower:.3f}, {results.ci_upper:.3f}]")
```

## Integration Guide

### Scikit-learn Integration

```python
from quantum_kernel_methods import QuantumKernel, QuantumSVM
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# QKSVM as sklearn estimator
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('qsvm', QuantumSVM(config)),
])

# Hyperparameter search
from sklearn.model_selection import GridSearchCV
param_grid = {
    'qsvm__config__feature_map_depth': [1, 2, 3],
    'qsvm__config__regularization': [0.01, 0.1, 1.0],
}

search = GridSearchCV(pipeline, param_grid, cv=3)
search.fit(X_train, y_train)
print(f"Best params: {search.best_params_}")
```

### PyTorch Integration

```python
import torch
from quantum_kernel_methods import QuantumKernel, KernelConfig

class QuantumKernelLayer(torch.nn.Module):
    def __init__(self, config, X_support):
        super().__init__()
        self.kernel = QuantumKernel(config)
        self.X_support = torch.tensor(X_support, dtype=torch.float32)
    
    def forward(self, x):
        K = self.kernel.compute_kernel_matrix(x.numpy(), self.X_support.numpy())
        return torch.tensor(K, dtype=torch.float32)

# Build hybrid model
kernel_layer = QuantumKernelLayer(config, X_support)
model = torch.nn.Sequential(
    torch.nn.Linear(10, 4),
    kernel_layer,
    torch.nn.Linear(len(X_support), 1),
)
```

## Performance Optimization

### Kernel Matrix Optimization

```python
from quantum_kernel_methods import KernelOptimizer

optimizer = KernelOptimizer(
    strategy="batch_computation",
    batch_size=100,
    n_workers=4,
    use_gpu=True,
)

# Optimized kernel computation
K = optimizer.compute_kernel_matrix(
    kernel=kernel,
    X=X_large,
    parallel=True,
)
print(f"Computation time: {optimizer.elapsed_time:.1f}s")
print(f"Throughput: {optimizer.throughput:.1f} samples/s")
```

### Feature Map Optimization

```python
from quantum_kernel_methods import FeatureMapOptimizer

fm_optimizer = FeatureMapOptimizer(
    target_depth=50,
    optimization_level=3,
    coupling_map="ibmq_mumbai",
)

optimized_fm = fm_optimizer.optimize(feature_map)
print(f"Original depth: {feature_map.circuit_depth}")
print(f"Optimized depth: {optimized_fm.circuit_depth}")
print(f"Gate reduction: {(1 - optimized_fm.circuit_depth/feature_map.circuit_depth)*100:.1f}%")
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Kernel Matrix Not Positive Semi-Definite

**Symptom**: SVM training fails or gives poor results

**Solution**:
```python
from quantum_kernel_methods import correct_psd

# Correct non-PSD kernel matrix
K_corrected = correct_psd(K, method="eigenvalue_clipping", threshold=1e-6)
print(f"Corrected eigenvalues: {np.sum(np.linalg.eigvalsh(K_corrected) > 0)}/{len(K)}")
```

#### 2. Low Kernel Alignment Score

**Symptom**: Alignment score < 0.3, poor classification accuracy

**Solution**:
```python
# Try different feature map
config.feature_map_type = "pauli_z_z"
config.depth = 3
config.data_reuploading = True

# Or use multiple kernel learning
mkl = MultipleKernelLearning(kernels=[...])
```

#### 3. Kernel Computation Too Slow

**Symptom**: Kernel matrix computation takes too long

**Solution**:
```python
# Use batch computation
kernel.compute_kernel_matrix(X, batch_size=100, n_workers=4)

# Or use approximate kernel
config.estimator = "classical_simulation"  # For n <= 20 qubits
```

#### 4. SVM Overfitting

**Symptom**: High training accuracy, low test accuracy

**Solution**:
```python
config.regularization = 0.01  # Increase regularization
svm_config.C = 0.1  # Reduce C parameter

# Or use cross-validation for parameter selection
cv_scores = qsvm.cross_validate(X, y, k=5)
```

## API Reference

### Core Classes

#### `QuantumKernel`
```python
class QuantumKernel:
    def __init__(self, config: KernelConfig) -> None: ...
    def compute_kernel_matrix(self, X: np.ndarray, Y: Optional[np.ndarray] = None) -> np.ndarray: ...
    def is_psd(self, K: np.ndarray) -> bool: ...
    def alignment_score(self, K: np.ndarray, y: np.ndarray) -> float: ...
```

#### `QuantumSVM`
```python
class QuantumSVM:
    def __init__(self, config: KernelConfig) -> None: ...
    def fit(self, X: np.ndarray, y: np.ndarray, precomputed_kernel: bool = False) -> None: ...
    def predict(self, X: np.ndarray) -> np.ndarray: ...
    def score(self, X: np.ndarray, y: np.ndarray) -> float: ...
    def decision_function(self, X: np.ndarray) -> np.ndarray: ...
    def cross_validate(self, X: np.ndarray, y: np.ndarray, k: int = 5) -> CVResult: ...
```

## Data Models

### Kernel Configuration Schema

```json
{
  "name": "quantum_kernel_v1",
  "n_qubits": 4,
  "feature_map": {
    "type": "zzfeaturemap",
    "depth": 2,
    "entanglement": "full",
    "data_reuploading": true
  },
  "estimation": {
    "method": "swap_test",
    "shots": 1024
  },
  "svm": {
    "kernel": "precomputed",
    "C": 1.0,
    "regularization": 0.1
  }
}
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY quantum_kernel_methods/ /app/quantum_kernel_methods/
WORKDIR /app

ENV KERNEL_BACKEND=default.qubit
ENV KERNEL_SHOTS=1024

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from quantum_kernel_methods import health_check; health_check()"

CMD ["python", "-m", "quantum_kernel_methods.server"]
```

## Monitoring & Observability

### Metrics Collection

```python
from quantum_kernel_methods import MetricsCollector

collector = MetricsCollector(backend="prometheus")

collector.register_metric("kernel_computation_time", type="histogram")
collector.register_metric("kernel_condition_number", type="gauge")
collector.register_metric("svm_accuracy", type="gauge")

collector.observe("kernel_computation_time", computation_ms)
collector.set("kernel_condition_number", np.linalg.cond(K))
collector.set("svm_accuracy", accuracy)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from quantum_kernel_methods import QuantumKernel, KernelConfig

class TestQuantumKernel:
    def setup_method(self):
        self.config = KernelConfig(n_qubits=4, feature_map="zzfeaturemap")
        self.kernel = QuantumKernel(self.config)
    
    def test_kernel_matrix_shape(self):
        X = np.random.randn(20, 4)
        K = self.kernel.compute_kernel_matrix(X)
        assert K.shape == (20, 20)
    
    def test_kernel_matrix_symmetric(self):
        X = np.random.randn(20, 4)
        K = self.kernel.compute_kernel_matrix(X)
        assert np.allclose(K, K.T)
    
    def test_kernel_diagonal_positive(self):
        X = np.random.randn(20, 4)
        K = self.kernel.compute_kernel_matrix(X)
        assert np.all(np.diag(K) >= 0)
```

## Versioning & Migration

### Changelog

#### v2.0.0 (2024-01-15)
- **Breaking**: New `KernelConfig` API
- **Added**: Multiple kernel learning support
- **Added**: Kernel alignment scoring
- **Improved**: 3x faster kernel computation
- **Fixed**: PSD correction for noisy hardware

#### v1.1.0 (2023-09-01)
- **Added**: ZZFeatureMap support
- **Added**: Kernel caching
- **Improved**: SVM training stability

## Glossary

| Term | Definition |
|------|------------|
| **Feature Map** | Quantum circuit that embeds classical data into Hilbert space |
| **Gram Matrix** | Matrix of pairwise kernel evaluations |
| **Kernel Alignment** | Measure of kernel-target compatibility |
| **PSD** | Positive Semi-Definite; required for valid kernels |
| **QSVM** | Quantum Support Vector Machine |
| **SWAP Test** | Quantum circuit for state overlap estimation |

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/quantum-kernels.git
cd quantum-kernels
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT License

Copyright (c) 2024 Quantum Kernel Methods Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

*Last updated: 2024-01-15*
*Version: 2.0.0*

## Advanced Patterns

### Feature Map Design Patterns

```python
from quantum_kernel_methods import FeatureMapDesigner, DesignStrategy

designer = FeatureMapDesigner(
    strategy=DesignStrategy.DATA_ADAPTIVE,
    depth=3,
    entanglement="full",
    data_reuploading=True,
)

# Design feature map
feature_map = designer.design(X_train, y_train)
print(f"Feature map depth: {feature_map.circuit_depth}")
print(f"Number of parameters: {feature_map.n_parameters}")
print(f"Expressivity score: {feature_map.expressivity:.4f}")
```

### Kernel Optimization Patterns

```python
from quantum_kernel_methods import KernelOptimizer, OptimizationStrategy

optimizer = KernelOptimizer(
    strategy=OptimizationStrategy.ALIGNMENT_MAXIMIZATION,
    learning_rate=0.01,
    max_iterations=100,
    convergence_threshold=1e-6,
)

# Optimize kernel parameters
optimized_kernel = optimizer.optimize(
    kernel=quantum_kernel,
    X=X_train,
    y=y_train,
)

print(f"Original alignment: {kernel.alignment_score:.4f}")
print(f"Optimized alignment: {optimized_kernel.alignment_score:.4f}")
```

### Multiple Kernel Learning Patterns

```python
from quantum_kernel_methods import MultipleKernelLearner, MKLStrategy

mkl = MultipleKernelLearner(
    strategy=MKLStrategy.WEIGHTED_SUM,
    kernels=[
        {"type": "quantum", "config": kernel_config_1},
        {"type": "quantum", "config": kernel_config_2},
        {"type": "classical", "kernel": "rbf", "gamma": 0.1},
        {"type": "classical", "kernel": "poly", "degree": 3},
    ],
    optimization="alignment",
)

# Learn kernel combination
mkl.fit(X_train, y_train)
print(f"Kernel weights: {mkl.weights}")
print(f"Combined alignment: {mkl.alignment_score:.4f}")
```

### Kernel Evaluation Patterns

```python
from quantum_kernel_methods import KernelEvaluator, EvaluationStrategy

evaluator = KernelEvaluator(
    strategy=EvaluationStrategy.CROSS_VALIDATION,
    n_folds=5,
    metrics=["accuracy", "f1", "auc"],
    confidence_level=0.95,
)

# Evaluate kernel quality
results = evaluator.evaluate(
    kernel=kernel,
    X=X_train,
    y=y_train,
)

print(f"Mean accuracy: {results.mean_accuracy:.3f} +/- {results.std_accuracy:.3f}")
print(f"Mean F1: {results.mean_f1:.3f} +/- {results.std_f1:.3f}")
print(f"95% CI for accuracy: [{results.ci_lower:.3f}, {results.ci_upper:.3f}]")
```

### Quantum Advantage Testing Patterns

```python
from quantum_kernel_methods import QuantumAdvantageTester, AdvantageStrategy

advantage_tester = QuantumAdvantageTester(
    strategy=AdvantageStrategy.STATISTICAL_SIGNIFICANCE,
    n_trials=100,
    significance_level=0.05,
    test_distributions=["hidden_parity", "clustered_data"],
)

# Test quantum advantage
results = advantage_tester.test(
    quantum_kernel=quantum_kernel,
    classical_kernels=["rbf", "poly", "linear"],
    X=X_train,
    y=y_train,
)

print(f"Quantum advantage: {results.advantage_detected}")
print(f"p-value: {results.p_value:.4f}")
print(f"Effect size: {results.effect_size:.4f}")
```
