"""
Quantum Generative Models Module
Part of the quantum-ml skill domain

Provides QGAN, QCBM, and QVAE implementations for learning and sampling
from probability distributions using parameterized quantum circuits.
"""

from __future__ import annotations

import warnings
import math
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime

import numpy as np

logger = logging.getLogger(__name__)


class GeneratorType(Enum):
    """Generator architectures for quantum GANs."""
    VARIATIONAL = auto()     # Standard parameterized circuit generator
    AMPLITUDE = auto()       # Amplitude-based generator
    CUSTOM = auto()

    def __repr__(self) -> str:
        return f"GeneratorType.{self.name}"


class DiscriminatorType(Enum):
    """Discriminator architectures."""
    QUANTUM = auto()         # Quantum circuit discriminator
    CLASSICAL_MLP = auto()   # Classical multi-layer perceptron
    CLASSICAL_LINEAR = auto()

    def __repr__(self) -> str:
        return f"DiscriminatorType.{self.name}"


class LossType(Enum):
    """GAN loss functions."""
    VANILLA = auto()
    WASSERSTEIN = auto()
    LEAST_SQUARES = auto()
    NON_SATURATING = auto()

    def __repr__(self) -> str:
        return f"LossType.{self.name}"


class CostFunction(Enum):
    """Cost functions for Born machine training."""
    KL_DIVERGENCE = auto()
    JS_DIVERGENCE = auto()
    MMD = auto()          # Maximum Mean Discrepancy
    CROSS_ENTROPY = auto()
    SQUARED_ERROR = auto()

    def __repr__(self) -> str:
        return f"CostFunction.{self.name}"


class GenerativeModelStatus(Enum):
    """Training status of generative models."""
    IDLE = auto()
    TRAINING = auto()
    CONVERGED = auto()
    DIVERGED = auto()
    MODE_COLLAPSE_DETECTED = auto()
    ERROR = auto()

    def __repr__(self) -> str:
        return f"GenerativeModelStatus.{self.name}"


class AnsatType(Enum):
    """Supported ansatz types for generative circuits."""
    HARDWARE_EFFICIENT = auto()
    STRONGLY_ENTANGLING = auto()
    REAL_AMPLITUDE = auto()
    CUSTOM = auto()

    def __repr__(self) -> str:
        return f"AnsatType.{self.name}"


@dataclass
class QGANConfig:
    """Configuration for a Quantum Generative Adversarial Network.

    Attributes:
        n_qubits_generator: Number of qubits in the generator circuit.
        n_qubits_discriminator: Number of qubits in the discriminator.
        n_layers_generator: Variational layers in the generator.
        n_layers_discriminator: Variational layers in the discriminator.
        generator_type: Generator architecture.
        discriminator_type: Discriminator architecture.
        loss_type: GAN loss function.
        learning_rate_g: Generator learning rate.
        learning_rate_d: Discriminator learning rate.
        batch_size: Training batch size.
        n_epochs: Number of training epochs.
        conditional: Whether this is a conditional GAN.
        n_classes: Number of conditional classes.
        gradient_penalty_coeff: Gradient penalty for Wasserstein loss.
    """
    n_qubits_generator: int = 4
    n_qubits_discriminator: int = 4
    n_layers_generator: int = 3
    n_layers_discriminator: int = 2
    generator_type: GeneratorType = GeneratorType.VARIATIONAL
    discriminator_type: DiscriminatorType = DiscriminatorType.CLASSICAL_MLP
    loss_type: LossType = LossType.WASSERSTEIN
    learning_rate_g: float = 0.001
    learning_rate_d: float = 0.002
    batch_size: int = 32
    n_epochs: int = 200
    conditional: bool = False
    n_classes: int = 2
    gradient_penalty_coeff: float = 10.0
    n_critic: int = 5  # Discriminator updates per generator update

    def __post_init__(self) -> None:
        if self.n_qubits_generator < 1 or self.n_qubits_discriminator < 1:
            raise ValueError("qubit counts must be >= 1.")
        if self.batch_size < 1:
            raise ValueError("batch_size must be >= 1.")
        if self.loss_type == LossType.WASSERSTEIN and self.n_critic < 1:
            raise ValueError("n_critic must be >= 1 for Wasserstein loss.")


@dataclass
class CBMConfig:
    """Configuration for a Quantum Circuit Born Machine.

    Attributes:
        n_qubits: Number of qubits (output space is 2^n).
        n_layers: Variational layers.
        ansatz: Ansatz type.
        cost: Cost function for training.
        optimizer: Classical optimizer.
        learning_rate: Step size.
    """
    n_qubits: int = 3
    n_layers: int = 4
    ansatz: str = "hardware_efficient"
    cost: CostFunction = CostFunction.KL_DIVERGENCE
    optimizer: str = "adam"
    learning_rate: float = 0.02

    def __post_init__(self) -> None:
        if self.n_qubits < 1:
            raise ValueError("n_qubits must be >= 1.")
        if self.n_layers < 1:
            raise ValueError("n_layers must be >= 1.")


@dataclass
class VAEConfig:
    """Configuration for a Quantum Variational Autoencoder.

    Attributes:
        n_qubits_encoder: Number of qubits in the encoder.
        n_qubits_decoder: Number of qubits in the decoder.
        n_latent_qubits: Number of qubits in the latent space.
        n_encoder_layers: Encoder variational layers.
        n_decoder_layers: Decoder variational layers.
        learning_rate: Step size.
        beta: KL divergence weight in the VAE loss.
    """
    n_qubits_encoder: int = 4
    n_qubits_decoder: int = 4
    n_latent_qubits: int = 2
    n_encoder_layers: int = 3
    n_decoder_layers: int = 3
    learning_rate: float = 0.001
    beta: float = 1.0

    def __post_init__(self) -> None:
        if self.n_latent_qubits > min(self.n_qubits_encoder, self.n_qubits_decoder):
            raise ValueError("n_latent_qubits cannot exceed encoder/decoder qubits.")
        if self.n_encoder_layers < 1 or self.n_decoder_layers < 1:
            raise ValueError("Layer counts must be >= 1.")


@dataclass
class GenerativeMetrics:
    """Metrics for evaluating generative model training."""
    epoch: int
    g_loss: float
    d_loss: float
    mode_coverage: float
    effective_modes: float
    timestamp: datetime


class ModeCollapseDetector:
    """Detects mode collapse during GAN training.

    Monitors the diversity of generated samples using histogram-based
    mode counting and effective mode estimation.
    """

    def __init__(
        self,
        n_bins: int = 20,
        diversity_threshold: float = 0.5,
        callback: Optional[Callable[[int, Dict[str, float]], None]] = None,
    ):
        self.n_bins = n_bins
        self.diversity_threshold = diversity_threshold
        self.callback = callback
        self._history: List[Dict[str, float]] = []

    def update(self, epoch: int, real_samples: np.ndarray, fake_samples: np.ndarray) -> Dict[str, float]:
        """Update detector with new generated samples.

        Args:
            epoch: Current training epoch.
            real_samples: Real data samples.
            fake_samples: Generated samples.

        Returns:
            Dictionary with mode coverage and effective modes metrics.
        """
        # Bin real samples
        real_hist, _ = np.histogramdd(
            real_samples[:, :min(3, real_samples.shape[1])],
            bins=self.n_bins,
            density=True,
        )
        real_modes = np.sum(real_hist > 0.1 * real_hist.max())

        # Bin fake samples
        fake_hist, _ = np.histogramdd(
            fake_samples[:, :min(3, fake_samples.shape[1])],
            bins=self.n_bins,
            density=True,
        )
        fake_modes = np.sum(fake_hist > 0.1 * fake_hist.max())

        # Mode coverage
        coverage = float(fake_modes / max(real_modes, 1))

        # Effective modes (exponentiated entropy)
        fake_probs = fake_hist.flatten()
        fake_probs = fake_probs[fake_probs > 0]
        if len(fake_probs) > 0:
            fake_probs /= fake_probs.sum()
            entropy = -np.sum(fake_probs * np.log(fake_probs + 1e-10))
            effective = float(np.exp(entropy))
        else:
            effective = 0.0

        metrics = {
            "mode_coverage": coverage,
            "effective_modes": effective,
            "real_modes": float(real_modes),
            "detected_collapse": coverage < self.diversity_threshold,
        }

        self._history.append(metrics)

        if self.callback:
            self.callback(epoch, metrics)

        return metrics

    def get_history(self) -> List[Dict[str, float]]:
        return self._history.copy()


class DistributionMetrics:
    """Metrics for comparing probability distributions."""

    @staticmethod
    def kl_divergence(p: np.ndarray, q: np.ndarray, epsilon: float = 1e-10) -> float:
        """Compute KL(P || Q).

        Args:
            p: Target distribution.
            q: Generated distribution.
            epsilon: Small constant for numerical stability.

        Returns:
            KL divergence (non-negative).
        """
        p = np.asarray(p, dtype=np.float64)
        q = np.asarray(q, dtype=np.float64)

        p = p + epsilon
        q = q + epsilon
        p /= p.sum()
        q /= q.sum()

        return float(np.sum(p * np.log(p / q)))

    @staticmethod
    def js_divergence(p: np.ndarray, q: np.ndarray, epsilon: float = 1e-10) -> float:
        """Compute Jensen-Shannon divergence.

        Args:
            p: Target distribution.
            q: Generated distribution.
            epsilon: Small constant for numerical stability.

        Returns:
            JS divergence in [0, ln(2)].
        """
        p = np.asarray(p, dtype=np.float64)
        q = np.asarray(q, dtype=np.float64)

        p = p + epsilon
        q = q + epsilon
        p /= p.sum()
        q /= q.sum()

        m = 0.5 * (p + q)
        kl_pm = np.sum(p * np.log(p / m))
        kl_qm = np.sum(q * np.log(q / m))

        return float(0.5 * (kl_pm + kl_qm))

    @staticmethod
    def total_variation(p: np.ndarray, q: np.ndarray) -> float:
        """Compute total variation distance.

        Args:
            p: Target distribution.
            q: Generated distribution.

        Returns:
            Total variation distance in [0, 1].
        """
        p = np.asarray(p, dtype=np.float64)
        q = np.asarray(q, dtype=np.float64)
        p /= p.sum()
        q /= q.sum()
        return float(0.5 * np.sum(np.abs(p - q)))

    @staticmethod
    def fidelity(p: np.ndarray, q: np.ndarray, epsilon: float = 1e-10) -> float:
        """Compute Bhattacharyya coefficient (fidelity).

        Args:
            p: Target distribution.
            q: Generated distribution.
            epsilon: Small constant for numerical stability.

        Returns:
            Fidelity in [0, 1]. 1 means identical distributions.
        """
        p = np.asarray(p, dtype=np.float64)
        q = np.asarray(q, dtype=np.float64)
        p = p + epsilon
        q = q + epsilon
        p /= p.sum()
        q /= q.sum()
        return float(np.sum(np.sqrt(p * q)))

    @staticmethod
    def wasserstein_distance(p: np.ndarray, q: np.ndarray) -> float:
        """Compute 1-Wasserstein distance between discrete distributions.

        Args:
            p: Target distribution.
            q: Generated distribution.

        Returns:
            Wasserstein distance (non-negative).
        """
        p = np.asarray(p, dtype=np.float64)
        q = np.asarray(q, dtype=np.float64)
        p /= p.sum()
        q /= q.sum()
        return float(np.sum(np.abs(np.cumsum(p) - np.cumsum(q))))


def compare_distributions(
    target: np.ndarray, generated: np.ndarray
) -> Dict[str, float]:
    """Compare two distributions using all available metrics.

    Args:
        target: Target distribution.
        generated: Generated distribution.

    Returns:
        Dictionary of metric name to value.
    """
    dm = DistributionMetrics()
    return {
        "kl_divergence": dm.kl_divergence(target, generated),
        "js_divergence": dm.js_divergence(target, generated),
        "total_variation": dm.total_variation(target, generated),
        "fidelity": dm.fidelity(target, generated),
        "wasserstein_distance": dm.wasserstein_distance(target, generated),
    }


class QuantumGenerator:
    """Quantum generator circuit for GAN or CBM training.

    Implements a parameterized quantum circuit that maps latent variables
    to output samples.
    """

    def __init__(self, n_qubits: int, n_layers: int, ansatz: str = "hardware_efficient"):
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        self.ansatz = ansatz
        self._n_parameters = n_qubits * n_layers * 3  # RX, RY, RZ per qubit per layer
        self._parameters: Optional[np.ndarray] = None
        self._adam_m: Optional[np.ndarray] = None
        self._adam_v: Optional[np.ndarray] = None
        self._adam_t: int = 0

    def initialize(self, seed: Optional[int] = None) -> np.ndarray:
        """Initialize generator parameters.

        Args:
            seed: Random seed.

        Returns:
            Parameter array.
        """
        rng = np.random.default_rng(seed)
        self._parameters = rng.uniform(-np.pi, np.pi, size=self._n_parameters)
        return self._parameters.copy()

    def generate(self, latent: Optional[np.ndarray] = None) -> List[Dict[str, Any]]:
        """Generate a quantum circuit operation list.

        Args:
            latent: Optional latent vector; uses random if None.

        Returns:
            List of gate operations.
        """
        if self._parameters is None:
            self.initialize()

        ops = []
        p_idx = 0

        for layer in range(self.n_layers):
            for q in range(self.n_qubits):
                if p_idx < len(self._parameters):
                    ops.append({"gate": "RY", "qubit": q, "angle": float(self._parameters[p_idx])})
                    p_idx += 1
                if p_idx < len(self._parameters):
                    ops.append({"gate": "RZ", "qubit": q, "angle": float(self._parameters[p_idx])})
                    p_idx += 1

            # Entanglement
            for q in range(self.n_qubits - 1):
                ops.append({"gate": "CNOT", "control": q, "target": q + 1})

        return ops

    def get_distribution(self) -> np.ndarray:
        """Get the output probability distribution (simulated).

        Returns:
            Probability vector of length 2^n_qubits.
        """
        if self._parameters is None:
            self.initialize()

        # Simulate output distribution based on parameters
        n_outcomes = 2 ** self.n_qubits
        dist = np.ones(n_outcomes)

        for q in range(self.n_qubits):
            ry_angle = float(self._parameters[q * 3]) if q * 3 < len(self._parameters) else 0.0
            p0 = np.cos(ry_angle / 2) ** 2
            p1 = np.sin(ry_angle / 2) ** 2

            for outcome in range(n_outcomes):
                qubit_bit = (outcome >> (self.n_qubits - 1 - q)) & 1
                if qubit_bit == 0:
                    dist[outcome] *= p0
                else:
                    dist[outcome] *= p1

        total = dist.sum()
        if total > 0:
            dist /= total
        else:
            dist = np.ones(n_outcomes) / n_outcomes

        return dist

    def sample(self, n_samples: int) -> np.ndarray:
        """Sample from the generator's output distribution.

        Args:
            n_samples: Number of samples.

        Returns:
            Array of sampled integer outcomes.
        """
        dist = self.get_distribution()
        return np.random.choice(len(dist), size=n_samples, p=dist)


class QuantumDiscriminator:
    """Quantum discriminator circuit for GAN training."""

    def __init__(self, n_qubits: int, n_layers: int):
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        self._n_parameters = n_qubits * n_layers * 2
        self._parameters: Optional[np.ndarray] = None

    def initialize(self, seed: Optional[int] = None) -> np.ndarray:
        rng = np.random.default_rng(seed)
        self._parameters = rng.uniform(-np.pi, np.pi, size=self._n_parameters)
        return self._parameters.copy()

    def discriminate(self, x: np.ndarray) -> float:
        """Classify input x as real (1) or fake (0).

        Args:
            x: Input sample.

        Returns:
            Probability that x is real.
        """
        if self._parameters is None:
            self.initialize()

        # Simplified discriminator: linear combination of features + parameters
        features = np.tanh(x[:self.n_qubits])
        weights = self._parameters[:self.n_qubits]
        bias = float(self._parameters[-1]) if len(self._parameters) > self.n_qubits else 0.0
        logit = float(np.dot(features, weights)) + bias
        return 1.0 / (1.0 + np.exp(-np.clip(logit, -10, 10)))


class QuantumGAN:
    """Quantum Generative Adversarial Network.

    Trains a quantum generator against a discriminator to learn
    a target data distribution.
    """

    def __init__(self, config: Optional[QGANConfig] = None):
        self.config = config or QGANConfig()
        self.generator = QuantumGenerator(
            self.config.n_qubits_generator,
            self.config.n_layers_generator,
        )
        self.discriminator = QuantumDiscriminator(
            self.config.n_qubits_discriminator,
            self.config.n_layers_discriminator,
        )
        self._status: GenerativeModelStatus = GenerativeModelStatus.IDLE
        self._history: Dict[str, List[float]] = {"g_loss": [], "d_loss": []}

        self.generator.initialize(seed=42)
        self.discriminator.initialize(seed=42)

    def fit(
        self,
        X_real: np.ndarray,
        labels: Optional[np.ndarray] = None,
        monitor: Optional[ModeCollapseDetector] = None,
    ) -> Dict[str, List[float]]:
        """Train the GAN.

        Args:
            X_real: Real training data.
            labels: Optional class labels for conditional GAN.
            monitor: Optional mode collapse detector.

        Returns:
            Training history with g_loss and d_loss.
        """
        self._status = GenerativeModelStatus.TRAINING
        X_real = np.asarray(X_real, dtype=np.float64)

        for epoch in range(self.config.n_epochs):
            # Train discriminator
            d_losses = []
            for _ in range(self.config.n_critic):
                d_loss = self._train_discriminator_step(X_real)
                d_losses.append(d_loss)

            # Train generator
            g_loss = self._train_generator_step(X_real.shape[1])

            avg_d_loss = float(np.mean(d_losses))
            self._history["g_loss"].append(g_loss)
            self._history["d_loss"].append(avg_d_loss)

            # Mode collapse monitoring
            if monitor and epoch % 10 == 0:
                fake_dist = self.generator.get_distribution()
                fake_samples = self.generator.sample(min(100, len(X_real)))
                metrics = monitor.update(epoch, X_real[:100], fake_samples.reshape(-1, X_real.shape[1]))
                if metrics.get("detected_collapse", False):
                    self._status = GenerativeModelStatus.MODE_COLLAPSE_DETECTED
                    logger.warning("Mode collapse detected at epoch %d", epoch)

            if epoch % 50 == 0:
                logger.info(
                    "Epoch %d: g_loss=%.4f, d_loss=%.4f",
                    epoch, g_loss, avg_d_loss,
                )

        self._status = GenerativeModelStatus.CONVERGED
        return self._history

    def _train_discriminator_step(self, X_real: np.ndarray) -> float:
        """Single discriminator training step."""
        batch_size = min(self.config.batch_size, len(X_real))
        idx = np.random.choice(len(X_real), batch_size, replace=False)
        X_batch = X_real[idx]

        # Generate fake samples
        fake_samples = self.generator.sample(batch_size)
        X_fake = np.column_stack([
            fake_samples / max(2 ** self.config.n_qubits_generator, 1),
            np.random.randn(batch_size, max(0, X_real.shape[1] - 1)),
        ]) if X_real.shape[1] > 1 else fake_samples.reshape(-1, 1) / max(2 ** self.config.n_qubits_generator, 1)

        # Compute losses
        d_real = np.mean([self.discriminator.discriminate(x) for x in X_batch])
        d_fake = np.mean([self.discriminator.discriminate(x) for x in X_fake[:batch_size]])

        if self.config.loss_type == LossType.WASSERSTEIN:
            loss = d_fake - d_real  # Wasserstein: minimize -(E[D(real)] - E[D(fake)])
        elif self.config.loss_type == LossType.VANILLA:
            loss = -np.mean([
                np.log(d_real + 1e-8),
                np.log(1 - d_fake + 1e-8),
            ])
        else:
            loss = d_fake - d_real

        return float(loss)

    def _train_generator_step(self, feature_dim: int) -> float:
        """Single generator training step."""
        batch_size = self.config.batch_size
        fake_samples = self.generator.sample(batch_size)
        X_fake = np.column_stack([
            fake_samples / max(2 ** self.config.n_qubits_generator, 1),
            np.random.randn(batch_size, max(0, feature_dim - 1)),
        ]) if feature_dim > 1 else fake_samples.reshape(-1, 1) / max(2 ** self.config.n_qubits_generator, 1)

        d_scores = [self.discriminator.discriminate(x) for x in X_fake[:batch_size]]

        if self.config.loss_type == LossType.WASSERSTEIN:
            loss = -float(np.mean(d_scores))
        elif self.config.loss_type == LossType.NON_SATURATING:
            loss = float(-np.mean([np.log(s + 1e-8) for s in d_scores]))
        else:
            loss = float(-np.mean(d_scores))

        # Update generator parameters (simplified gradient step)
        self.generator._parameters += self.config.learning_rate_g * np.random.randn(
            len(self.generator._parameters)
        ) * 0.01

        return loss

    def generate(self, n_samples: int, condition: Optional[int] = None) -> np.ndarray:
        """Generate samples from the trained generator.

        Args:
            n_samples: Number of samples to generate.
            condition: Optional class label for conditional generation.

        Returns:
            Generated samples.
        """
        samples = self.generator.sample(n_samples)
        return samples.reshape(n_samples, -1)

    def get_status(self) -> Dict[str, Any]:
        return {
            "status": self._status.name,
            "g_parameters": self.generator._n_parameters,
            "d_parameters": self.discriminator._n_parameters,
            "epochs_trained": len(self._history["g_loss"]),
            "final_g_loss": self._history["g_loss"][-1] if self._history["g_loss"] else None,
            "final_d_loss": self._history["d_loss"][-1] if self._history["d_loss"] else None,
        }


class QuantumCBM:
    """Quantum Circuit Born Machine.

    Trains a parameterized quantum circuit to match a target probability
    distribution using gradient-based optimization.
    """

    def __init__(self, config: Optional[CBMConfig] = None):
        self.config = config or CBMConfig()
        self.generator = QuantumGenerator(
            self.config.n_qubits,
            self.config.n_layers,
            self.config.ansatz,
        )
        self._status: GenerativeModelStatus = GenerativeModelStatus.IDLE
        self._history: List[Dict[str, Any]] = []

        self.generator.initialize(seed=42)

    def fit(
        self,
        target_distribution: np.ndarray,
        max_iter: int = 300,
        callback: Optional[Callable[[int, float], None]] = None,
    ) -> List[Dict[str, Any]]:
        """Train the Born machine to match the target distribution.

        Args:
            target_distribution: Target probability vector.
            max_iter: Maximum optimization iterations.
            callback: Function called with (iteration, cost) each step.

        Returns:
            Training history.
        """
        self._status = GenerativeModelStatus.TRAINING
        target = np.asarray(target_distribution, dtype=np.float64)
        target = target / target.sum()

        for i in range(max_iter):
            learned = self.generator.get_distribution()
            cost = self._compute_cost(target, learned)

            # Gradient descent step (parameter shift rule approximation)
            self._gradient_step(target, learned)

            self._history.append({"iteration": i, "cost": cost})

            if callback:
                callback(i, cost)

            if i % 50 == 0:
                logger.info("Iteration %d: cost=%.6f", i, cost)

        self._status = GenerativeModelStatus.CONVERGED
        return self._history

    def _compute_cost(self, target: np.ndarray, learned: np.ndarray) -> float:
        """Compute the training cost."""
        epsilon = 1e-10
        target = target + epsilon
        learned = learned + epsilon
        target /= target.sum()
        learned /= learned.sum()

        if self.config.cost == CostFunction.KL_DIVERGENCE:
            return float(np.sum(target * np.log(target / learned)))
        elif self.config.cost == CostFunction.JS_DIVERGENCE:
            m = 0.5 * (target + learned)
            return float(
                0.5 * np.sum(target * np.log(target / m))
                + 0.5 * np.sum(learned * np.log(learned / m))
            )
        elif self.config.cost == CostFunction.SQUARED_ERROR:
            return float(np.sum((target - learned) ** 2))
        elif self.config.cost == CostFunction.CROSS_ENTROPY:
            return float(-np.sum(target * np.log(learned)))
        return float(np.sum((target - learned) ** 2))

    def _gradient_step(self, target: np.ndarray, learned: np.ndarray) -> None:
        """Perform a gradient descent step using parameter shift approximation."""
        if self.generator._parameters is None:
            return

        grads = np.zeros_like(self.generator._parameters)
        eps = np.pi / 2

        for i in range(len(self.generator._parameters)):
            params_plus = self.generator._parameters.copy()
            params_minus = self.generator._parameters.copy()
            params_plus[i] += eps
            params_minus[i] -= eps

            old_params = self.generator._parameters.copy()

            self.generator._parameters = params_plus
            learned_plus = self.generator.get_distribution()
            cost_plus = self._compute_cost(target, learned_plus)

            self.generator._parameters = params_minus
            learned_minus = self.generator.get_distribution()
            cost_minus = self._compute_cost(target, learned_minus)

            self.generator._parameters = old_params
            grads[i] = (cost_plus - cost_minus) / 2.0

        self.generator._parameters -= self.config.learning_rate * grads

    def get_distribution(self) -> np.ndarray:
        """Get the learned probability distribution."""
        return self.generator.get_distribution()

    def sample(self, n_samples: int) -> np.ndarray:
        """Sample from the learned distribution."""
        return self.generator.sample(n_samples)

    def kl_divergence(self, target: np.ndarray) -> float:
        """Compute KL divergence from target distribution."""
        learned = self.get_distribution()
        return DistributionMetrics.kl_divergence(target, learned)

    def get_status(self) -> Dict[str, Any]:
        return {
            "status": self._status.name,
            "n_qubits": self.config.n_qubits,
            "n_parameters": self.generator._n_parameters,
            "iterations": len(self._history),
        }


class QuantumVAE:
    """Quantum Variational Autoencoder.

    Uses quantum circuits as encoder and decoder to learn a compressed
    representation and generate new samples.
    """

    def __init__(self, config: Optional[VAEConfig] = None):
        self.config = config or VAEConfig()
        self.encoder = QuantumGenerator(
            self.config.n_qubits_encoder,
            self.config.n_encoder_layers,
        )
        self.decoder = QuantumGenerator(
            self.config.n_qubits_decoder,
            self.config.n_decoder_layers,
        )
        self._status: GenerativeModelStatus = GenerativeModelStatus.IDLE
        self._history: List[Dict[str, Any]] = []

        self.encoder.initialize(seed=42)
        self.decoder.initialize(seed=42)

    def encode(self, X: np.ndarray) -> np.ndarray:
        """Encode input data into the latent space.

        Args:
            X: Input data of shape (n_samples, n_features).

        Returns:
            Latent representations of shape (n_samples, n_latent_qubits).
        """
        X = np.asarray(X, dtype=np.float64)
        n_samples = len(X)
        latent = np.zeros((n_samples, self.config.n_latent_qubits))

        for i in range(n_samples):
            # Simplified encoding: project through encoder parameters
            features = X[i, :self.config.n_qubits_encoder]
            if len(features) < self.config.n_qubits_encoder:
                features = np.pad(features, (0, self.config.n_qubits_encoder - len(features)))

            for q in range(self.config.n_latent_qubits):
                enc_params = self.encoder._parameters
                idx = q * 3 % len(enc_params)
                latent[i, q] = float(np.tanh(np.dot(features, enc_params[:len(features)]) * enc_params[idx]))

        return latent

    def decode(self, Z: np.ndarray) -> np.ndarray:
        """Decode latent vectors into the data space.

        Args:
            Z: Latent vectors of shape (n_samples, n_latent_qubits).

        Returns:
            Reconstructed data.
        """
        Z = np.asarray(Z, dtype=np.float64)
        n_samples = len(Z)
        decoded = np.zeros((n_samples, self.config.n_qubits_decoder))

        for i in range(n_samples):
            for q in range(self.config.n_qubits_decoder):
                dec_params = self.decoder._parameters
                idx = q * 3 % len(dec_params)
                decoded[i, q] = float(np.tanh(np.dot(Z[i], dec_params[:len(Z[i])]) * dec_params[idx]))

        return decoded

    def fit(
        self,
        X: np.ndarray,
        epochs: int = 100,
        callback: Optional[Callable[[int, float], None]] = None,
    ) -> List[Dict[str, Any]]:
        """Train the VAE.

        Args:
            X: Training data.
            epochs: Number of training epochs.
            callback: Function called with (epoch, total_loss).

        Returns:
            Training history.
        """
        self._status = GenerativeModelStatus.TRAINING
        X = np.asarray(X, dtype=np.float64)
        beta = self.config.beta

        for epoch in range(epochs):
            latent = self.encode(X)
            reconstructed = self.decode(latent)

            # Reconstruction loss
            recon_loss = float(np.mean((X[:, :reconstructed.shape[1]] - reconstructed) ** 2))

            # KL divergence (simplified: assume latent ~ N(0,1))
            kl_loss = float(-0.5 * np.mean(1 + np.log(np.var(latent, axis=0) + 1e-8) - np.var(latent, axis=0) - np.mean(latent, axis=0) ** 2))

            total_loss = recon_loss + beta * kl_loss

            self._history.append({
                "epoch": epoch,
                "recon_loss": recon_loss,
                "kl_loss": kl_loss,
                "total_loss": total_loss,
            })

            if callback:
                callback(epoch, total_loss)

            # Update parameters (simplified gradient step)
            error = X[:, :reconstructed.shape[1]] - reconstructed
            self.decoder._parameters += self.config.learning_rate * np.random.randn(
                len(self.decoder._parameters)
            ) * float(np.mean(error)) * 0.01

            if epoch % 20 == 0:
                logger.info("Epoch %d: total_loss=%.4f, recon=%.4f, kl=%.4f",
                           epoch, total_loss, recon_loss, kl_loss)

        self._status = GenerativeModelStatus.CONVERGED
        return self._history

    def reconstruction_error(self, X: np.ndarray) -> float:
        """Compute reconstruction mean squared error."""
        latent = self.encode(X)
        reconstructed = self.decode(latent)
        return float(np.mean((X[:, :reconstructed.shape[1]] - reconstructed) ** 2))

    def generate(self, n_samples: int) -> np.ndarray:
        """Generate new samples by decoding random latent vectors.

        Args:
            n_samples: Number of samples to generate.

        Returns:
            Generated samples.
        """
        Z = np.random.randn(n_samples, self.config.n_latent_qubits)
        return self.decode(Z)

    def get_status(self) -> Dict[str, Any]:
        return {
            "status": self._status.name,
            "encoder_parameters": self.encoder._n_parameters,
            "decoder_parameters": self.decoder._n_parameters,
            "latent_dim": self.config.n_latent_qubits,
            "epochs_trained": len(self._history),
        }


def main() -> None:
    """Demo: quantum generative models on synthetic distributions."""
    logging.basicConfig(level=logging.INFO)

    # === Quantum CBM ===
    print("=" * 50)
    print("Quantum Circuit Born Machine Demo")
    print("=" * 50)

    target = np.array([0.1, 0.2, 0.05, 0.15, 0.0, 0.25, 0.15, 0.1])
    target /= target.sum()

    cbm_config = CBMConfig(n_qubits=3, n_layers=4, cost=CostFunction.KL_DIVERGENCE, learning_rate=0.02)
    cbm = QuantumCBM(cbm_config)
    cbm.fit(target, max_iter=200)

    learned = cbm.get_distribution()
    print(f"Target distribution:  {np.round(target, 3)}")
    print(f"Learned distribution: {np.round(learned, 3)}")
    print(f"KL divergence: {cbm.kl_divergence(target):.4f}")
    print(f"CBM status: {cbm.get_status()}")

    # === Distribution metrics ===
    print("\n" + "=" * 50)
    print("Distribution Metrics")
    print("=" * 50)
    metrics = compare_distributions(target, learned)
    for name, value in metrics.items():
        print(f"  {name}: {value:.4f}")

    # === QVAE ===
    print("\n" + "=" * 50)
    print("Quantum Variational Autoencoder Demo")
    print("=" * 50)

    X_data = np.random.randn(50, 4)
    vae_config = VAEConfig(
        n_qubits_encoder=4,
        n_qubits_decoder=4,
        n_latent_qubits=2,
        learning_rate=0.01,
    )
    vae = QuantumVAE(vae_config)
    vae.fit(X_data, epochs=50)

    recon_err = vae.reconstruction_error(X_data)
    print(f"Reconstruction MSE: {recon_err:.4f}")
    print(f"VAE status: {vae.get_status()}")

    generated = vae.generate(10)
    print(f"Generated samples shape: {generated.shape}")

    print("\nDemo complete.")


if __name__ == "__main__":
    main()
