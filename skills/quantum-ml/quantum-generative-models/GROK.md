---
name: "quantum-generative-models"
category: "quantum-ml"
version: "1.1.0"
tags: ["quantum-ml", "quantum-generative-models", "QGAN", "QVAE", "QCBM", "generative", "sampling", "density-estimation"]
---

# Quantum Generative Models

## Overview

Quantum Generative Models leverage quantum circuits to learn and sample from probability distributions that are difficult to represent classically. This module covers three primary architectures: Quantum Generative Adversarial Networks (QGANs) where a quantum generator competes with a discriminator, Quantum Circuit Born Machines (QCBMs) that learn a Born distribution via KL divergence minimization, and Quantum Variational Autoencoders (QVAEs) that compress data into a latent quantum state. Quantum generative models are particularly promising for sampling from molecular distributions, simulating quantum many-body systems, generating combinatorial optimization solutions, and producing synthetic data with complex correlations.

The exponential state space of n qubits allows representing distributions over 2^n outcomes with only n qubits, offering potential quantum advantage in generative modeling. A quantum circuit with n qubits naturally produces probability distributions over computational basis states, where the Born rule determines the probability of each outcome. By parameterizing the circuit, these distributions become trainable, allowing the quantum model to learn complex target distributions that may be intractable for classical generative models.

Quantum generative models excel in domains where the target distribution has quantum structure (e.g., molecular energy distributions), where sampling efficiency matters (e.g., Monte Carlo integration), and where the exponential state space provides a natural advantage over classical representations. The module supports both simulation-based training and execution on real quantum hardware, with built-in tools for distribution evaluation, mode collapse detection, and conditional generation.

## Core Capabilities

- **QGAN training**: Train quantum generators against classical or quantum discriminators with configurable loss functions (vanilla, Wasserstein, least-squares). Supports adversarial training with gradient penalty and spectral normalization.
- **Born machine sampling**: Train a parameterized quantum circuit to match a target probability distribution via KL divergence, JS divergence, or maximum mean discrepancy (MMD). Maximum likelihood training for exact distribution matching.
- **Quantum VAE**: Build encoder-decoder quantum circuits for dimensionality reduction and generative sampling from a learned latent space. Supports reparameterization tricks for gradient estimation.
- **Distribution metrics**: Evaluate generated distributions against targets using KL divergence, JS divergence, fidelity, total variation distance, Wasserstein distance, and maximum mean discrepancy.
- **Mode collapse detection**: Monitor diversity of generated samples to detect and mitigate mode collapse in adversarial training. Tracks effective mode count and coverage metrics.
- **Conditional generation**: Extend any generative model to support conditional sampling on specified input labels or features. Enables class-conditional and attribute-conditional generation.
- **Circuit Born Machine (CBM)**: Maximum likelihood training of quantum circuits to produce desired output distributions. Supports gradient-based and gradient-free optimization.
- **Sample quality assessment**: FID-like scores, precision-recall curves, and statistical tests for evaluating generated sample quality against reference datasets.

## Usage Examples

### Training a Quantum GAN

```python
from quantum_generative_models import (
    QuantumGAN,
    QGANConfig,
    GeneratorType,
    DiscriminatorType,
)

config = QGANConfig(
    n_qubits_generator=4,
    n_qubits_discriminator=4,
    n_layers_generator=3,
    n_layers_discriminator=2,
    generator_type=GeneratorType.VARIATIONAL,
    discriminator_type=DiscriminatorType.CLASSICAL_MLP,
    loss_type="wasserstein",
    learning_rate_g=0.001,
    learning_rate_d=0.002,
    batch_size=32,
    n_epochs=200,
    gradient_penalty=10.0,
)

qgan = QuantumGAN(config)
history = qgan.fit(X_real=target_data)
print(f"Final G loss: {history['g_loss'][-1]:.4f}")
print(f"Final D loss: {history['d_loss'][-1]:.4f}")
print(f"Wasserstein distance: {history['wasserstein'][-1]:.4f}")
```

### Quantum Circuit Born Machine

```python
from quantum_generative_models import QuantumCBM, CBMConfig
import numpy as np

# Target distribution: a specific probability vector
target_dist = np.array([0.1, 0.2, 0.05, 0.15, 0.0, 0.25, 0.15, 0.1])
target_dist /= target_dist.sum()

config = CBMConfig(
    n_qubits=3,
    n_layers=4,
    ansatz="hardware_efficient",
    cost="kl_divergence",
    optimizer="adam",
    learning_rate=0.02,
)

cbm = QuantumCBM(config)
cbm.fit(target_dist, max_iter=300)

# Sample from the learned distribution
samples = cbm.sample(n_samples=1000)
learned_dist = cbm.get_distribution()
print(f"KL divergence: {cbm.kl_divergence(target_dist):.4f}")
print(f"JS divergence: {cbm.js_divergence(target_dist):.4f}")
print(f"Fidelity: {cbm.fidelity(target_dist):.4f}")
```

### Quantum Variational Autoencoder

```python
from quantum_generative_models import QuantumVAE, VAEConfig

config = VAEConfig(
    n_qubits_encoder=4,
    n_qubits_decoder=4,
    n_latent_qubits=2,
    n_encoder_layers=3,
    n_decoder_layers=3,
    learning_rate=0.001,
    beta=1.0,  # KL weight in VAE loss
)

qvae = QuantumVAE(config)
history = qvae.fit(X_train, epochs=100)

# Encode and decode
encoded = qvae.encode(X_test)
decoded = qvae.decode(encoded)
reconstruction_loss = qvae.reconstruction_error(X_test)
print(f"Reconstruction MSE: {reconstruction_loss:.4f}")

# Sample from latent space
new_samples = qvae.sample(n_samples=50)
print(f"Generated {len(new_samples)} samples from latent space")
```

### Evaluating Generated Distributions

```python
from quantum_generative_models import (
    DistributionMetrics,
    compare_distributions,
)

metrics = DistributionMetrics()

# KL Divergence
kl = metrics.kl_divergence(target_dist, generated_dist)
print(f"KL divergence: {kl:.4f}")

# Jensen-Shannon Divergence
js = metrics.js_divergence(target_dist, generated_dist)
print(f"JS divergence: {js:.4f}")

# Total variation distance
tv = metrics.total_variation(target_dist, generated_dist)
print(f"Total variation: {tv:.4f}")

# Fidelity (Bhattacharyya coefficient)
fid = metrics.fidelity(target_dist, generated_dist)
print(f"Fidelity: {fid:.4f}")

# Statistical tests
chi2, p_value = metrics.chi_squared_test(target_dist, generated_dist)
print(f"Chi-squared: {chi2:.4f}, p-value: {p_value:.4f}")
```

### Conditional Generation

```python
from quantum_generative_models import QuantumGAN, QGANConfig

config = QGANConfig(
    n_qubits_generator=4,
    n_qubits_discriminator=4,
    conditional=True,
    n_classes=3,
)

qgan = QuantumGAN(config)

# Generate samples conditioned on class 2
conditional_samples = qgan.generate(
    n_samples=100,
    condition=2,
)

# Train with conditional labels
qgan.fit(X_real=X_train, labels=y_train)

# Evaluate per-class generation quality
for cls in range(3):
    cls_samples = qgan.generate(n_samples=50, condition=cls)
    quality = qgan.evaluate_class(cls_samples, X_train[y_train == cls])
    print(f"Class {cls}: quality = {quality:.4f}")
```

### Monitoring Mode Collapse

```python
from quantum_generative_models import QuantumGAN, ModeCollapseDetector

config = QGANConfig(n_qubits_generator=4, n_layers_generator=3)
qgan = QuantumGAN(config)

detector = ModeCollapseDetector(
    n_bins=20,
    diversity_threshold=0.5,
    callback=lambda epoch, metrics: print(
        f"Epoch {epoch}: mode_coverage={metrics['mode_coverage']:.2f}, "
        f"effective_modes={metrics['effective_modes']:.1f}"
    ),
)

qgan.fit(X_real=target_data, monitor=detector)

# Post-training analysis
report = detector.get_report()
print(f"Total epochs: {report['total_epochs']}")
print(f"Final effective modes: {report['final_effective_modes']:.1f}")
print(f"Mode collapse detected: {report['collapse_detected']}")
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                Quantum Generative Model Architecture             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  QGAN:                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │  Latent  │───>│ Quantum  │───>│Measure   │───>│  Fake/   │ │
│  │  Vector z│    │Generator │    │          │    │  Real    │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│                                        │              │         │
│                                   Samples         Discriminator │
│                                        │              │         │
│                                   ┌────┴────┐   ┌────┴────┐   │
│                                   │  Target  │   │  Loss   │   │
│                                   │   Data   │   │Computation│  │
│                                   └─────────┘   └─────────┘   │
│                                                                  │
│  QCBM:                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │ Parameters│───>│ Quantum  │───>│Measure   │───>│ Loss     │ │
│  │  θ        │    │ Circuit  │    │          │    │(KL/MMD)  │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│       ↑                                       │                 │
│       └───────────── Gradient ────────────────┘                 │
│                                                                  │
│  QVAE:                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │  Input x │───>│ Encoder  │───>│ Latent z │───>│ Decoder  │ │
│  │          │    │(quantum) │    │ (quantum)│    │(quantum) │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│       ↑                                       │                 │
│       └───────── Reconstruction ──────────────┘                 │
└─────────────────────────────────────────────────────────────────┘
```

Each generative architecture uses quantum circuits differently: QGANs use quantum generators with classical discriminators, QCBMs directly optimize circuits to match target distributions, and QVAEs use quantum encoder-decoder pairs with latent quantum states.

## Best Practices

1. **Use Wasserstein loss for stability**: Standard GAN loss is notoriously unstable. Wasserstein loss (WGAN) provides smoother gradients and more stable training. Use gradient penalty for additional stability.

2. **Start with simple distributions**: Validate the QCBM on known distributions (uniform, Gaussian, bimodal) before attempting complex multimodal targets. This ensures the circuit architecture has sufficient expressivity.

3. **Monitor mode collapse actively**: Track the number of "effective modes" (exponentiated by entropy of the empirical distribution) during training. If it drops below the target's mode count, the generator is collapsing.

4. **Balance generator and discriminator capacity**: The discriminator should be slightly more powerful than the generator. For quantum GANs, use deeper discriminator circuits or classical MLP discriminators for better training stability.

5. **Use gradient penalty for WGAN**: Add a gradient penalty term to the Wasserstein loss to enforce the Lipschitz constraint without weight clipping, which can distort the learned distribution.

6. **KL divergence can diverge**: When the generated distribution has zero probability where the target has nonzero probability, KL divergence is infinite. Use JS divergence or add a small epsilon floor to probabilities for numerical stability.

7. **Validate Born machine outputs analytically**: For small systems (n_qubits <= 6), compute the full output distribution and compare directly. For larger systems, use statistical tests on sampled data.

8. **Consider noise-aware training**: Quantum hardware introduces sampling noise that can mimic mode collapse. Distinguish between genuine mode collapse and noise-induced variance by comparing against noiseless simulation baselines.

9. **Use curriculum learning**: Start training with simpler target distributions and gradually increase complexity. This helps the quantum circuit learn stable representations before tackling hard distributions.

10. **Log distribution metrics frequently**: Save generated distributions at regular intervals during training. This enables post-hoc analysis of training dynamics and early stopping based on distribution quality.

## Performance Considerations

- **Sampling cost**: Each sample requires one circuit execution and measurement. For n_shots samples, the cost is O(n_shots) circuit executions. Use batch execution to amortize overhead.
- **KL divergence estimation**: Estimating KL divergence from samples requires O(1/epsilon^2) samples for accuracy epsilon. Use importance sampling or density estimation for better sample efficiency.
- **Mode collapse recovery**: Once mode collapse occurs, recovery is difficult. Use techniques like unrolled GANs, minibatch discrimination, or spectral normalization to prevent it.
- **Circuit depth impact**: Deeper generator circuits are more expressive but harder to train. Start with 2-3 layers and increase only when the model underfits.
- **Hardware noise effects**: On real hardware, sampling noise can dominate for small systems. Use error mitigation or increase shot counts for reliable distribution estimation.
- **Classical simulation threshold**: For n <= 20 qubits, classical simulation of the full distribution is feasible. Use this for validation before scaling to quantum hardware.

## Security Considerations

- **Synthetic data risks**: Generated samples may inadvertently memorize and reproduce sensitive training data. Apply differential privacy or membership inference tests to quantify privacy leakage.
- **Adversarial manipulation**: Quantum GANs can be manipulated through adversarial perturbations of the latent space. Test robustness against latent vector perturbations.
- **Model extraction**: An adversary querying the generative model could reconstruct the learned distribution. Implement query rate limits and output perturbation.
- **Distribution inversion**: The learned distribution may reveal information about the training data. Use privacy-preserving training for sensitive datasets.
- **Reproducibility**: Quantum measurements are probabilistic. Use fixed seeds and sufficient samples for reproducible generation in regulated domains.

## Related Modules

- `quantum-neural-networks` — Hybrid quantum-classical models share ansatz construction patterns with quantum generators
- `variational-circuits` — Parameterized circuit primitives used in all generative model architectures
- `quantum-kernel-methods` — Kernel-based methods for evaluating distribution similarity
- `quantum-data` — Data encoding and quantum dataset management for training generative models

## References

- Dallaire-Demers, P.-L., & Killoran, N. (2018). Quantum generative adversarial networks. Physical Review A, 98(1), 012324.
- Zoufal, C., et al. (2019). Quantum GANs for financial risk modeling. arXiv:1911.00031.
- Liu, J., & Wang, L. (2018). Quantum circuit Born machine. arXiv:1804.04168.
- Li, J., et al. (2021). Quantum variational autoencoder. Quantum Science and Technology, 6(4), 045021.
- Kerenidis, I., & Landman, J. (2021). Quantum generative models for small molecule drug discovery. arXiv:2101.03438.
- PennyLane quantum GANs: https://pennylane.ai/qml/demos_quantum_gans.html
- Qiskit quantum generative models: https://qiskit.org/ecosystem/machine-learning/

## Advanced Configuration

### QGAN Advanced Training Configuration

```python
from quantum_generative_models import QuantumGAN, QGANConfig, TrainingConfig

config = QGANConfig(
    n_qubits_generator=4,
    n_qubits_discriminator=4,
    n_layers_generator=4,
    n_layers_discriminator=3,
    generator_type="variational",
    discriminator_type="classical_mlp",
    loss_type="wasserstein",
)

training_config = TrainingConfig(
    optimizer_g="adam",
    optimizer_d="adam",
    learning_rate_g=0.0002,
    learning_rate_d=0.0002,
    beta1=0.5,
    beta2=0.999,
    n_epochs=500,
    batch_size=64,
    gradient_penalty=10.0,
    n_critic=5,  # Train discriminator 5 times per generator step
    label_smoothing=0.1,
    spectral_normalization=True,
)

qgan = QuantumGAN(config)
history = qgan.fit(X_real=target_data, training_config=training_config)
```

### QCBM Advanced Configuration

```python
from quantum_generative_models import QuantumCBM, CBMConfig

config = CBMConfig(
    n_qubits=6,
    n_layers=5,
    ansatz="hardware_efficient",
    cost="kl_divergence",
    optimizer="adam",
    learning_rate=0.01,
    batch_size=128,
    gradient_clipping=1.0,
    early_stopping_patience=20,
    lr_scheduler="cosine_annealing",
)

cbm = QuantumCBM(config)
cbm.fit(target_dist, max_iter=500)
```

### QVAE Advanced Configuration

```python
from quantum_generative_models import QuantumVAE, VAEConfig

config = VAEConfig(
    n_qubits_encoder=6,
    n_qubits_decoder=6,
    n_latent_qubits=3,
    n_encoder_layers=4,
    n_decoder_layers=4,
    learning_rate=0.001,
    beta=0.5,  # KL weight
    beta_schedule="warmup",
    beta_warmup_epochs=10,
    reconstruction_loss="mse",
    latent_regularization="kl",
)

qvae = QuantumVAE(config)
history = qvae.fit(X_train, epochs=200)
```

### Distribution Metrics Configuration

```python
from quantum_generative_models import DistributionMetrics, MetricConfig

metrics_config = MetricConfig(
    metrics=["kl", "js", "tv", "fid", "mmd"],
    n_bootstrap=1000,
    confidence_level=0.95,
    bins=50,
    kernel="rbf",
    kernel_bandwidth=0.1,
)

metrics = DistributionMetrics(metrics_config)

# Comprehensive evaluation
report = metrics.evaluate(target_dist, generated_dist)
print(f"KL divergence: {report.kl:.4f} (CI: [{report.kl_ci_lower:.4f}, {report.kl_ci_upper:.4f}])")
print(f"JS divergence: {report.js:.4f}")
print(f"Total variation: {report.tv:.4f}")
print(f"Fidelity: {report.fid:.4f}")
print(f"MMD: {report.mmd:.4f}")
```

## Architecture Patterns

### GAN Training Pipeline Pattern

```python
from quantum_generative_models import GANPipeline, PipelineStage

pipeline = GANPipeline(stages=[
    PipelineStage(
        name="data_preprocessing",
        type="classical",
        processor=lambda x: normalize_data(x),
    ),
    PipelineStage(
        name="generator",
        type="quantum",
        processor=lambda z: generate_samples(z),
    ),
    PipelineStage(
        name="discriminator",
        type="hybrid",
        processor=lambda x: discriminate(x),
    ),
    PipelineStage(
        name="loss_computation",
        type="classical",
        processor=lambda x: compute_wasserstein_loss(x),
    ),
    PipelineStage(
        name="parameter_update",
        type="classical",
        processor=lambda x: update_parameters(x),
    ),
])

result = pipeline.train(X_real=target_data, n_epochs=200)
```

### Distribution Matching Pattern

```python
from quantum_generative_models import DistributionMatcher, MatchingStrategy

matcher = DistributionMatcher(
    strategy=MatchingStrategy.MULTI_SCALE,
    scales=[0.1, 0.5, 1.0],
    metrics=["kl", "js", "mmd"],
)

# Multi-scale distribution matching
result = matcher.match(
    target=target_dist,
    generator=cbm,
    max_iterations=300,
)

print(f"Final KL: {result.kl_divergence:.4f}")
print(f"Final JS: {result.js_divergence:.4f}")
print(f"Convergence epoch: {result.convergence_epoch}")
```

### Conditional Generation Pattern

```python
from quantum_generative_models import ConditionalGenerator, ConditionType

generator = ConditionalGenerator(
    model=qgan,
    condition_type=ConditionType.CLASS_LABEL,
    n_classes=3,
    conditioning_method="label_embedding",
    embedding_dim=4,
)

# Generate class-conditional samples
for cls in range(3):
    samples = generator.generate(
        n_samples=100,
        condition=cls,
        temperature=0.8,
    )
    print(f"Class {cls}: {len(samples)} samples generated")
```

## Integration Guide

### Scikit-learn Integration

```python
from quantum_generative_models import QuantumCBM, CBMConfig
from sklearn.base import BaseEstimator, GeneratorMixin

class QuantumGenerator(BaseEstimator, GeneratorMixin):
    def __init__(self, config):
        self.config = config
        self.cbm = QuantumCBM(config)
    
    def fit(self, X, y=None):
        dist = self._compute_distribution(X)
        self.cbm.fit(dist)
        return self
    
    def sample(self, n_samples=100):
        return self.cbm.sample(n_samples)
    
    def _compute_distribution(self, X):
        # Convert data to distribution
        hist, _ = np.histogram(X, bins=2**self.config.n_qubits, density=True)
        return hist / hist.sum()

# Use as sklearn generator
gen = QuantumGenerator(CBMConfig(n_qubits=4))
gen.fit(X_train)
samples = gen.sample(100)
```

### PyTorch Integration

```python
import torch
from quantum_generative_models import QuantumVAE, VAEConfig

class QuantumVAELayer(torch.nn.Module):
    def __init__(self, config):
        super().__init__()
        self.qvae = QuantumVAE(config)
    
    def forward(self, x):
        encoded = self.qvae.encode(x.numpy())
        decoded = self.qvae.decode(encoded)
        return torch.tensor(decoded, dtype=torch.float32)
    
    def loss(self, x, recon):
        return self.qvae.compute_loss(x.numpy(), recon.numpy())

# Build hybrid model
vae_layer = QuantumVAELayer(VAEConfig(n_qubits_encoder=4, n_qubits_decoder=4, n_latent_qubits=2))
```

## Performance Optimization

### Batch Sampling Optimization

```python
from quantum_generative_models import BatchSampler

sampler = BatchSampler(
    batch_size=100,
    n_workers=4,
    prefetch_factor=2,
)

# Parallel sampling
samples = sampler.sample(
    model=cbm,
    n_samples=1000,
    strategy="parallel_circuits",
)
print(f"Sampled {len(samples)} in {sampler.elapsed_time:.1f}s")
print(f"Throughput: {sampler.samples_per_second:.1f} samples/s")
```

### Distribution Caching

```python
from quantum_generative_models import DistributionCache

cache = DistributionCache(
    cache_dir="./dist_cache",
    max_size_mb=512,
    ttl_hours=24,
)

# Cache-aware generation
cached_dist = cache.get_or_compute(
    key="target_distribution",
    compute_fn=lambda: compute_target_distribution(X_train),
)
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Mode Collapse in QGAN

**Symptom**: Generator produces only a few modes

**Solution**:
```python
# Use Wasserstein loss with gradient penalty
config.loss_type = "wasserstein"
config.gradient_penalty = 10.0

# Add minibatch discrimination
config.discriminator_features.append("minibatch")

# Use unrolled GAN
config.unroll_steps = 5
```

#### 2. KL Divergence Infinity

**Symptom**: KL divergence explodes to infinity

**Solution**:
```python
# Use JS divergence instead
config.cost = "js_divergence"

# Or add epsilon floor
config.epsilon = 1e-10
```

#### 3. Training Instability

**Symptom**: Loss oscillates without converging

**Solution**:
```python
# Reduce learning rates
config.learning_rate_g = 0.0002
config.learning_rate_d = 0.0002

# Use spectral normalization
config.spectral_normalization = True

# Add label smoothing
config.label_smoothing = 0.1
```

#### 4. Poor Sample Quality

**Symptom**: Generated samples don't match target distribution

**Solution**:
```python
# Increase circuit depth
config.n_layers_generator = 5

# Use more qubits
config.n_qubits_generator = 6

# Train longer
config.n_epochs = 500
```

## API Reference

### Core Classes

#### `QuantumGAN`
```python
class QuantumGAN:
    def __init__(self, config: QGANConfig) -> None: ...
    def fit(self, X_real: np.ndarray, **kwargs) -> TrainingHistory: ...
    def generate(self, n_samples: int = 100, **kwargs) -> np.ndarray: ...
    def evaluate(self, X_real: np.ndarray) -> EvaluationResult: ...
```

#### `QuantumCBM`
```python
class QuantumCBM:
    def __init__(self, config: CBMConfig) -> None: ...
    def fit(self, target_dist: np.ndarray, max_iter: int = 300) -> TrainingHistory: ...
    def sample(self, n_samples: int = 100) -> np.ndarray: ...
    def get_distribution(self) -> np.ndarray: ...
    def kl_divergence(self, target: np.ndarray) -> float: ...
    def js_divergence(self, target: np.ndarray) -> float: ...
    def fidelity(self, target: np.ndarray) -> float: ...
```

## Data Models

### GAN Configuration Schema

```json
{
  "name": "qgan_v1",
  "generator": {
    "n_qubits": 4,
    "n_layers": 3,
    "ansatz": "hardware_efficient"
  },
  "discriminator": {
    "type": "classical_mlp",
    "hidden_layers": [64, 32],
    "activation": "relu"
  },
  "training": {
    "loss": "wasserstein",
    "optimizer": "adam",
    "learning_rate": 0.0002,
    "epochs": 200,
    "batch_size": 32
  }
}
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY quantum_generative_models/ /app/quantum_generative_models/
WORKDIR /app

ENV QGM_BACKEND=default.qubit
ENV QGM_SHOTS=1024

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from quantum_generative_models import health_check; health_check()"

CMD ["python", "-m", "quantum_generative_models.server"]
```

## Monitoring & Observability

### Metrics Collection

```python
from quantum_generative_models import MetricsCollector

collector = MetricsCollector(backend="prometheus")

collector.register_metric("qgm_generator_loss", type="gauge")
collector.register_metric("qgm_discriminator_loss", type="gauge")
collector.register_metric("qgm_wasserstein_distance", type="gauge")
collector.register_metric("qgm_mode_coverage", type="gauge")

collector.set("qgm_generator_loss", g_loss)
collector.set("qgm_discriminator_loss", d_loss)
collector.set("qgm_wasserstein_distance", w_distance)
collector.set("qgm_mode_coverage", mode_coverage)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from quantum_generative_models import QuantumCBM, CBMConfig

class TestQCBM:
    def setup_method(self):
        self.config = CBMConfig(n_qubits=3, n_layers=2)
        self.cbm = QuantumCBM(self.config)
    
    def test_sample_shape(self):
        target = np.ones(8) / 8
        self.cbm.fit(target, max_iter=10)
        samples = self.cbm.sample(100)
        assert samples.shape == (100,)
    
    def test_kl_divergence(self):
        target = np.array([0.1, 0.2, 0.05, 0.15, 0.0, 0.25, 0.15, 0.1])
        target /= target.sum()
        self.cbm.fit(target, max_iter=50)
        kl = self.cbm.kl_divergence(target)
        assert kl >= 0
```

## Versioning & Migration

### Changelog

#### v2.0.0 (2024-01-15)
- **Breaking**: New config API for all generative models
- **Added**: Conditional generation support
- **Added**: Multi-scale distribution matching
- **Improved**: 2x faster training
- **Fixed**: Mode collapse detection

## Glossary

| Term | Definition |
|------|------------|
| **Born Machine** | Quantum circuit that produces Born distribution |
| **KL Divergence** | Measure of distribution similarity |
| **Mode Collapse** | Generator produces limited diversity |
| **QCBM** | Quantum Circuit Born Machine |
| **QGAN** | Quantum Generative Adversarial Network |
| **QVAE** | Quantum Variational Autoencoder |
| **Wasserstein Distance** | Earth-mover distance between distributions |

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/quantum-generative.git
cd quantum-generative
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT License

Copyright (c) 2024 Quantum Generative Models Contributors

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

### Generator Architecture Patterns

```python
from quantum_generative_models import GeneratorArchitecture, ArchStrategy

arch = GeneratorArchitecture(
    strategy=ArchStrategy.HARDWARE_EFFICIENT,
    n_qubits=4,
    n_layers=3,
    entanglement="circular",
    rotation_gates=["RX", "RY", "RZ"],
    entangling_gate="CZ",
)

# Build generator
generator = arch.build()
print(f"Generator depth: {generator.circuit_depth}")
print(f"Parameters: {generator.n_parameters}")
print(f"Expressivity: {generator.expressivity:.4f}")
```

### Discriminator Design Patterns

```python
from quantum_generative_models import DiscriminatorDesign, DiscStrategy

disc_design = DiscriminatorDesign(
    strategy=DiscStrategy.CLASSICAL_MLP,
    hidden_layers=[64, 32, 16],
    activation="relu",
    dropout=0.2,
    spectral_normalization=True,
)

# Build discriminator
discriminator = disc_design.build()
print(f"Discriminator layers: {discriminator.num_layers}")
print(f"Parameters: {discriminator.n_parameters}")
```

### Training Stability Patterns

```python
from quantum_generative_models import TrainingStability, StabilityStrategy

stability = TrainingStability(
    strategy=StabilityStrategy.WASSERSTEIN_LOSS,
    gradient_penalty=10.0,
    label_smoothing=0.1,
    spectral_normalization=True,
    EMA_decay=0.999,
)

# Apply stability techniques
stabilized_model = stability.apply(gan_model)
print(f"Training stability score: {stability.stability_score:.4f}")
```

### Distribution Matching Patterns

```python
from quantum_generative_models import DistributionMatcher, MatchStrategy

matcher = DistributionMatcher(
    strategy=MatchStrategy.MULTI_SCALE,
    scales=[0.1, 0.5, 1.0],
    metrics=["kl", "js", "mmd"],
)

# Match distributions
result = matcher.match(
    target=target_dist,
    generator=cbm,
    max_iterations=300,
)

print(f"Final KL: {result.kl_divergence:.4f}")
print(f"Final JS: {result.js_divergence:.4f}")
print(f"Convergence epoch: {result.convergence_epoch}")
```

### Sample Quality Assessment Patterns

```python
from quantum_generative_models import SampleQualityAssessor, QualityStrategy

assessor = SampleQualityAssessor(
    strategy=QualityStrategy.FID_SCORE,
    reference_samples=reference_data,
    inception_model="inception_v3",
    num_samples=1000,
)

# Assess quality
quality = assessor.assess(generated_samples)
print(f"FID score: {quality.fid_score:.4f}")
print(f"Precision: {quality.precision:.4f}")
print(f"Recall: {quality.recall:.4f}")
print(f"Diversity: {quality.diversity:.4f}")
```

### Conditional Generation Patterns

```python
from quantum_generative_models import ConditionalGenerator, ConditionStrategy

cond_gen = ConditionalGenerator(
    strategy=ConditionStrategy.LABEL_EMBEDDING,
    n_classes=3,
    embedding_dim=4,
)

# Generate conditional samples
for cls in range(3):
    samples = cond_gen.generate(
        n_samples=100,
        condition=cls,
        temperature=0.8,
    )
    print(f"Class {cls}: {len(samples)} samples generated")
```
