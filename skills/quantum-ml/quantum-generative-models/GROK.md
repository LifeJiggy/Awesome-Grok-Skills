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
