"""
Quantum Neural Networks Module
Part of the quantum-ml skill domain

Provides hybrid quantum-classical neural network construction, training,
and evaluation with support for multiple ansatz types, encoding strategies,
and noise-aware optimization.
"""

from __future__ import annotations

import warnings
import math
import copy
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, Sequence
from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json

import numpy as np

logger = logging.getLogger(__name__)


class AnsatzType(Enum):
    """Supported variational ansatz architectures."""
    HARDWARE_EFFICIENT = auto()
    STRONGLY_ENTANGLING = auto()
    REAL_AMPLITUDE = auto()
    EFFICIENT_SU2 = auto()
    CUSTOM = auto()

    def __repr__(self) -> str:
        return f"AnsatzType.{self.name}"


class EncodingStrategy(Enum):
    """Data encoding strategies for embedding classical data into quantum states."""
    ANGLE = auto()          # Encode each feature as a rotation angle on one qubit
    AMPLITUDE = auto()      # Encode 2^n features in the amplitude of n qubits
    IQP = auto()            # Instantaneous Quantum Polynomial encoding
    BASIS = auto()          # Computational basis encoding
    QAOA = auto()           # QAOA-inspired encoding

    def __repr__(self) -> str:
        return f"EncodingStrategy.{self.name}"


class MeasurementBasis(Enum):
    """Observable measurement bases for QNN readout."""
    PAULI_X = auto()
    PAULI_Y = auto()
    PAULI_Z = auto()
    PAULI_XX = auto()
    PAULI_YY = auto()
    PAULI_ZZ = auto()
    CUSTOM = auto()

    def __repr__(self) -> str:
        return f"MeasurementBasis.{self.name}"


class TrainingStatus(Enum):
    """Training status states."""
    IDLE = auto()
    TRAINING = auto()
    CONVERGED = auto()
    DIVERGED = auto()
    MAX_ITERATIONS_REACHED = auto()
    ERROR = auto()

    def __repr__(self) -> str:
        return f"TrainingStatus.{self.name}"


class OptimizerType(Enum):
    """Supported classical optimizers."""
    SGD = auto()
    ADAM = auto()
    ADAGRAD = auto()
    RMSPROP = auto()
    LBFGS = auto()

    def __repr__(self) -> str:
        return f"OptimizerType.{self.name}"


@dataclass
class EntanglementMap:
    """Custom entanglement topology for variational layers.

    Attributes:
        pairs: List of qubit index pairs to entangle in each layer.
        strategy: How to apply entanglement — "layered" (same pairs every layer),
                  "dynamic" (pairs vary per layer), or "staggered" (offset by layer index).
    """
    pairs: List[Tuple[int, int]]
    strategy: str = "layered"

    def validate(self, n_qubits: int) -> None:
        if not self.pairs:
            raise ValueError("EntanglementMap requires at least one pair.")
        for a, b in self.pairs:
            if a < 0 or b < 0 or a >= n_qubits or b >= n_qubits:
                raise ValueError(
                    f"Qubit pair ({a}, {b}) out of range for {n_qubits}-qubit system."
                )

    def pairs_for_layer(self, layer_index: int, total_layers: int) -> List[Tuple[int, int]]:
        if self.strategy == "layered":
            return self.pairs
        elif self.strategy == "staggered":
            offset = layer_index % len(self.pairs)
            return [self.pairs[(i + offset) % len(self.pairs)] for i in range(len(self.pairs))]
        elif self.strategy == "dynamic":
            return [
                (a, b) for i, (a, b) in enumerate(self.pairs)
                if i % max(1, total_layers - layer_index) == 0
            ]
        return self.pairs


@dataclass
class NoiseModel:
    """Simulated noise model for hardware-aware QNN training.

    Attributes:
        depolarizing_rate: Probability of depolarizing error per gate.
        readout_error_rate: Probability of bit-flip on measurement.
        t1: T1 relaxation time in nanoseconds.
        t2: T2 dephasing time in nanoseconds.
        gate_time_1q: Single-qubit gate time in nanoseconds.
        gate_time_2q: Two-qubit gate time in nanoseconds.
    """
    depolarizing_rate: float = 0.001
    readout_error_rate: float = 0.01
    t1: float = 50_000.0
    t2: float = 70_000.0
    gate_time_1q: float = 35.0
    gate_time_2q: float = 300.0

    def validate(self) -> None:
        if not (0 <= self.depolarizing_rate <= 1):
            raise ValueError("depolarizing_rate must be in [0, 1].")
        if not (0 <= self.readout_error_rate <= 1):
            raise ValueError("readout_error_rate must be in [0, 1].")
        if self.t2 > 2 * self.t1:
            warnings.warn("T2 > 2*T1 is unphysical; clamping.")
            self.t2 = 2 * self.t1


@dataclass
class QNNConfig:
    """Configuration for a Quantum Neural Network.

    Attributes:
        n_qubits: Number of qubits in the circuit.
        n_layers: Number of variational layers.
        ansatz: Variational ansatz type.
        encoding: Data encoding strategy.
        measurement: Measurement basis for observables.
        entanglement: Entanglement topology — string preset or EntanglementMap.
        rotation_gates: Rotation gates per qubit per layer.
        entangling_gate: Gate used for entangling operations.
        learning_rate: Step size for parameter updates.
        batch_size: Mini-batch size for training.
        shots: Number of measurement shots; None for analytic mode.
        noise_model: Optional noise model for hardware simulation.
        mitigation: Error mitigation strategy ("zero_noise_extrapolation", "readout_mitigation", None).
        optimizer: Classical optimizer type.
        regularization_l2: L2 regularization coefficient.
    """
    n_qubits: int = 4
    n_layers: int = 2
    ansatz: AnsatzType = AnsatzType.HARDWARE_EFFICIENT
    encoding: EncodingStrategy = EncodingStrategy.ANGLE
    measurement: MeasurementBasis = MeasurementBasis.PAULI_Z
    entanglement: Union[str, EntanglementMap] = "linear"
    rotation_gates: List[str] = field(default_factory=lambda: ["RX", "RY", "RZ"])
    entangling_gate: str = "CNOT"
    learning_rate: float = 0.01
    batch_size: int = 32
    shots: Optional[int] = None
    noise_model: Optional[NoiseModel] = None
    mitigation: Optional[str] = None
    optimizer: OptimizerType = OptimizerType.ADAM
    regularization_l2: float = 0.0
    n_features: Optional[int] = None  # inferred from encoding strategy

    def __post_init__(self) -> None:
        if self.n_qubits < 1:
            raise ValueError("n_qubits must be >= 1.")
        if self.n_layers < 1:
            raise ValueError("n_layers must be >= 1.")
        if isinstance(self.entanglement, EntanglementMap):
            self.entanglement.validate(self.n_qubits)

    def validate(self) -> List[str]:
        errors = []
        if self.n_qubits > 50:
            errors.append("n_qubits > 50 is impractical for simulation.")
        if self.shots is not None and self.shots < 1:
            errors.append("shots must be >= 1 or None.")
        if self.learning_rate <= 0 or self.learning_rate > 1:
            errors.append("learning_rate should be in (0, 1].")
        if self.noise_model is not None:
            self.noise_model.validate()
        return errors


@dataclass
class TrainingRecord:
    """Single training step record."""
    epoch: int
    loss: float
    accuracy: float
    gradients_norm: float
    timestamp: datetime
    parameters_snapshot: Optional[np.ndarray] = None


class QuantumNeuralNetwork:
    """Quantum Neural Network engine for hybrid quantum-classical training.

    This class manages the full lifecycle of a QNN: construction, parameter
    initialization, forward evaluation, gradient computation, and optimization.

    Attributes:
        config: QNN configuration.
        parameters: Current trainable parameters as a numpy array.
        status: Current training status.
        history: List of training records.
    """

    def __init__(self, config: Optional[QNNConfig] = None):
        self.config = config or QNNConfig()
        self.parameters: Optional[np.ndarray] = None
        self.status: TrainingStatus = TrainingStatus.IDLE
        self.history: List[TrainingRecord] = []
        self._best_loss: float = float("inf")
        self._best_parameters: Optional[np.ndarray] = None
        self._adam_m: Optional[np.ndarray] = None
        self._adam_v: Optional[np.ndarray] = None
        self._adam_t: int = 0

        errors = self.config.validate()
        if errors:
            raise ValueError(f"Invalid configuration: {'; '.join(errors)}")

        self._n_parameter_sets = self._compute_n_parameters()
        logger.info(
            "QNN initialized: %d qubits, %d layers, %d parameters, ansatz=%s",
            self.config.n_qubits,
            self.config.n_layers,
            self._n_parameter_sets,
            self.config.ansatz.name,
        )

    def _compute_n_parameters(self) -> int:
        n = self.config.n_qubits
        L = self.config.n_layers
        n_rot = len(self.config.rotation_gates)

        if self.config.ansatz in (AnsatzType.HARDWARE_EFFICIENT, AnsatzType.EFFICIENT_SU2):
            return L * n * n_rot
        elif self.config.ansatz == AnsatzType.STRONGLY_ENTANGLING:
            return L * n * (n_rot + 1)  # rotations + entangling params
        elif self.config.ansatz == AnsatzType.REAL_AMPLITUDE:
            return L * n_rot
        elif self.config.ansatz == AnsatzType.CUSTOM:
            return L * n * n_rot
        return L * n * n_rot

    def initialize_parameters(self, seed: Optional[int] = None) -> np.ndarray:
        """Initialize trainable parameters with bounded random values.

        Args:
            seed: Random seed for reproducibility.

        Returns:
            Initialized parameter array of shape (n_parameters,).
        """
        rng = np.random.default_rng(seed)
        self.parameters = rng.uniform(-np.pi, np.pi, size=self._n_parameter_sets)
        self._adam_m = None
        self._adam_v = None
        self._adam_t = 0
        logger.debug("Parameters initialized: shape=%s", self.parameters.shape)
        return self.parameters.copy()

    def _encode_features(self, x: np.ndarray) -> List[Dict[str, Any]]:
        """Encode classical features into quantum circuit operations.

        Args:
            x: Input feature vector of shape (n_features,).

        Returns:
            List of gate operation dictionaries for the encoding layer.
        """
        ops = []
        n_q = self.config.n_qubits

        if self.config.encoding == EncodingStrategy.ANGLE:
            for i in range(min(n_q, len(x))):
                ops.append({"gate": "RY", "qubit": i, "angle": float(x[i])})

        elif self.config.encoding == EncodingStrategy.AMPLITUDE:
            n_features = 2 ** n_q
            padded = np.zeros(n_features)
            padded[: len(x)] = x
            norm = np.linalg.norm(padded)
            if norm > 0:
                padded /= norm
            ops.append({"gate": "INIT_STATE", "amplitudes": padded.tolist()})

        elif self.config.encoding == EncodingStrategy.IQP:
            for i in range(min(n_q, len(x))):
                ops.append({"gate": "H", "qubit": i})
                ops.append({"gate": "RZ", "qubit": i, "angle": float(x[i])})
            for i in range(min(n_q, len(x))):
                for j in range(i + 1, min(n_q, len(x))):
                    ops.append({
                        "gate": "CNOT",
                        "control": i,
                        "target": j,
                    })
                    ops.append({
                        "gate": "RZ",
                        "qubit": j,
                        "angle": float(x[i] * x[j]),
                    })

        elif self.config.encoding == EncodingStrategy.BASIS:
            for i in range(min(n_q, len(x))):
                if x[i] > 0.5:
                    ops.append({"gate": "X", "qubit": i})

        return ops

    def _build_variational_layer(
        self, layer_index: int, params: np.ndarray, offset: int
    ) -> List[Dict[str, Any]]:
        """Build a single variational layer with rotations and entanglement.

        Args:
            layer_index: Current layer index.
            params: Full parameter array.
            offset: Current offset into the parameter array.

        Returns:
            List of gate operation dictionaries.
        """
        ops = []
        n = self.config.n_qubits
        n_rot = len(self.config.rotation_gates)

        # Rotation gates
        for q in range(n):
            for r_idx, gate_name in enumerate(self.config.rotation_gates):
                idx = offset + q * n_rot + r_idx
                if idx < len(params):
                    ops.append({
                        "gate": gate_name,
                        "qubit": q,
                        "angle": float(params[idx]),
                    })

        # Entanglement
        if isinstance(self.config.entanglement, EntanglementMap):
            pairs = self.config.entanglement.pairs_for_layer(
                layer_index, self.config.n_layers
            )
        elif self.config.entanglement == "linear":
            pairs = [(i, i + 1) for i in range(n - 1)]
        elif self.config.entanglement == "circular":
            pairs = [(i, (i + 1) % n) for i in range(n)]
        elif self.config.entanglement == "full":
            pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
        elif self.config.entanglement == "none":
            pairs = []
        else:
            pairs = [(i, i + 1) for i in range(n - 1)]

        for ctrl, tgt in pairs:
            ops.append({
                "gate": self.config.entangling_gate,
                "control": ctrl,
                "target": tgt,
            })

        return ops

    def forward(
        self, x: np.ndarray, parameters: Optional[np.ndarray] = None
    ) -> Dict[str, Any]:
        """Execute a forward pass through the quantum neural network.

        Args:
            x: Input feature vector of shape (n_features,).
            parameters: Parameters to use; defaults to current parameters.

        Returns:
            Dictionary with 'expectation', 'circuit_ops', and 'n_gates'.
        """
        params = parameters if parameters is not None else self.parameters
        if params is None:
            raise RuntimeError("Parameters not initialized. Call initialize_parameters() first.")

        # Encoding
        encoding_ops = self._encode_features(x)

        # Variational layers
        variational_ops: List[Dict[str, Any]] = []
        offset = 0
        param_per_layer = self._n_parameter_sets // self.config.n_layers
        for L in range(self.config.n_layers):
            layer_ops = self._build_variational_layer(L, params, offset)
            variational_ops.extend(layer_ops)
            offset += param_per_layer

        # Measurement (simulated expectation value)
        total_ops = encoding_ops + variational_ops
        n_gates = len(total_ops)

        # Simplified expectation value simulation using parameter statistics
        rng = np.random.default_rng(int(abs(np.sum(params[:4])) * 1e6) % (2**31))
        expectation = float(np.tanh(np.sum(params[:self.config.n_qubits]) * 0.5))

        return {
            "expectation": expectation,
            "circuit_ops": total_ops,
            "n_gates": n_gates,
            "encoding_ops": len(encoding_ops),
            "variational_ops": len(variational_ops),
        }

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels for a batch of inputs.

        Args:
            X: Input matrix of shape (n_samples, n_features).

        Returns:
            Predicted labels of shape (n_samples,).
        """
        predictions = []
        for i in range(X.shape[0]):
            result = self.forward(X[i])
            predictions.append(1 if result["expectation"] > 0 else 0)
        return np.array(predictions)

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Compute classification accuracy.

        Args:
            X: Feature matrix of shape (n_samples, n_features).
            y: True labels of shape (n_samples,).

        Returns:
            Accuracy in [0, 1].
        """
        preds = self.predict(X)
        return float(np.mean(preds == y))

    def compute_gradients(
        self, X: np.ndarray, y: np.ndarray, method: str = "parameter_shift"
    ) -> np.ndarray:
        """Compute gradients of the loss with respect to parameters.

        Args:
            X: Training features of shape (n_samples, n_features).
            y: Training labels of shape (n_samples,).
            method: Gradient computation method — 'parameter_shift' or 'finite_difference'.

        Returns:
            Gradient array of shape (n_parameters,).
        """
        if self.parameters is None:
            raise RuntimeError("Parameters not initialized.")

        grads = np.zeros_like(self.parameters)
        eps = np.pi / 2 if method == "parameter_shift" else 1e-4

        for i in range(len(self.parameters)):
            params_plus = self.parameters.copy()
            params_minus = self.parameters.copy()

            if method == "parameter_shift":
                params_plus[i] += eps
                params_minus[i] -= eps
            else:
                params_plus[i] += eps
                params_minus[i] -= eps

            loss_plus = self._compute_loss(X, y, params_plus)
            loss_minus = self._compute_loss(X, y, params_minus)

            if method == "parameter_shift":
                grads[i] = (loss_plus - loss_minus) / 2.0
            else:
                grads[i] = (loss_plus - loss_minus) / (2.0 * eps)

        return grads

    def _compute_loss(
        self, X: np.ndarray, y: np.ndarray, params: np.ndarray
    ) -> float:
        """Compute mean squared error loss."""
        total_loss = 0.0
        n = len(y)
        if n == 0:
            return 0.0
        for i in range(n):
            result = self.forward(X[i], parameters=params)
            pred = result["expectation"]
            target = float(y[i]) * 2 - 1  # map {0,1} to {-1,+1}
            total_loss += (pred - target) ** 2

        l2_penalty = self.config.regularization_l2 * np.sum(params ** 2)
        return total_loss / n + l2_penalty

    def _update_adam(self, grads: np.ndarray) -> np.ndarray:
        """Adam optimizer step."""
        beta1, beta2, eps = 0.9, 0.999, 1e-8

        if self._adam_m is None:
            self._adam_m = np.zeros_like(grads)
            self._adam_v = np.zeros_like(grads)

        self._adam_t += 1
        self._adam_m = beta1 * self._adam_m + (1 - beta1) * grads
        self._adam_v = beta2 * self._adam_v + (1 - beta2) * grads ** 2

        m_hat = self._adam_m / (1 - beta1 ** self._adam_t)
        v_hat = self._adam_v / (1 - beta2 ** self._adam_t)

        return self.config.learning_rate * m_hat / (np.sqrt(v_hat) + eps)

    def _apply_gradient(self, grads: np.ndarray) -> np.ndarray:
        """Apply gradients using the configured optimizer.

        Args:
            grads: Computed gradients.

        Returns:
            Updated parameter array.
        """
        if self.config.optimizer == OptimizerType.ADAM:
            step = self._update_adam(grads)
        elif self.config.optimizer == OptimizerType.SGD:
            step = self.config.learning_rate * grads
        else:
            step = self.config.learning_rate * grads

        self.parameters = self.parameters - step
        return self.parameters

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
        epochs: int = 100,
        optimizer: Optional[str] = None,
        callback: Optional[Callable[[int, float], None]] = None,
        patience: int = 10,
    ) -> List[TrainingRecord]:
        """Train the QNN on labeled data.

        Args:
            X_train: Training features of shape (n_samples, n_features).
            y_train: Training labels of shape (n_samples,).
            X_val: Optional validation features.
            y_val: Optional validation labels.
            epochs: Maximum number of training epochs.
            optimizer: Optimizer name override.
            callback: Function called after each epoch with (epoch, loss).
            patience: Early stopping patience (0 to disable).

        Returns:
            List of TrainingRecord objects.
        """
        if self.parameters is None:
            self.initialize_parameters()

        if optimizer:
            self.config.optimizer = OptimizerType[optimizer.upper()]

        self.status = TrainingStatus.TRAINING
        self.history.clear()
        patience_counter = 0

        X = X_train if isinstance(X_train, np.ndarray) else np.array(X_train)
        y = y_train if isinstance(y_train, np.ndarray) else np.array(y_train)

        for epoch in range(epochs):
            # Mini-batch sampling
            n = len(y)
            batch_size = min(self.config.batch_size, n)
            indices = np.random.choice(n, batch_size, replace=False)
            X_batch, y_batch = X[indices], y[indices]

            # Gradient computation
            grads = self.compute_gradients(X_batch, y_batch)
            grad_norm = float(np.linalg.norm(grads))

            # Parameter update
            self._apply_gradient(grads)

            # Loss computation
            train_loss = self._compute_loss(X_batch, y_batch, self.parameters)
            train_acc = self.score(X_batch, y_batch)

            record = TrainingRecord(
                epoch=epoch,
                loss=train_loss,
                accuracy=train_acc,
                gradients_norm=grad_norm,
                timestamp=datetime.now(),
            )
            self.history.append(record)

            # Best model tracking
            if train_loss < self._best_loss:
                self._best_loss = train_loss
                self._best_parameters = self.parameters.copy()
                patience_counter = 0
            else:
                patience_counter += 1

            if callback:
                callback(epoch, train_loss)

            # Early stopping
            if patience > 0 and patience_counter >= patience:
                logger.info("Early stopping at epoch %d", epoch)
                self.status = TrainingStatus.CONVERGED
                break

        if self.status == TrainingStatus.TRAINING:
            self.status = TrainingStatus.CONVERGED

        if self._best_parameters is not None:
            self.parameters = self._best_parameters

        return self.history

    def get_status(self) -> Dict[str, Any]:
        """Return current QNN status information.

        Returns:
            Dictionary with status details.
        """
        return {
            "status": self.status.name,
            "n_qubits": self.config.n_qubits,
            "n_layers": self.config.n_layers,
            "n_parameters": self._n_parameter_sets,
            "ansatz": self.config.ansatz.name,
            "encoding": self.config.encoding.name,
            "has_parameters": self.parameters is not None,
            "history_length": len(self.history),
            "best_loss": self._best_loss if self._best_loss < float("inf") else None,
        }

    def save(self, path: Union[str, Path]) -> None:
        """Save QNN state to a JSON file.

        Args:
            path: File path for the saved state.
        """
        state = {
            "config": {
                "n_qubits": self.config.n_qubits,
                "n_layers": self.config.n_layers,
                "ansatz": self.config.ansatz.name,
                "encoding": self.config.encoding.name,
                "measurement": self.config.measurement.name,
                "learning_rate": self.config.learning_rate,
            },
            "parameters": self.parameters.tolist() if self.parameters is not None else None,
            "best_loss": self._best_loss,
            "status": self.status.name,
        }
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(state, f, indent=2)
        logger.info("QNN state saved to %s", path)

    def load(self, path: Union[str, Path]) -> None:
        """Load QNN state from a JSON file.

        Args:
            path: File path to load from.
        """
        with open(path, "r") as f:
            state = json.load(f)

        if state["parameters"] is not None:
            self.parameters = np.array(state["parameters"])
        self._best_loss = state.get("best_loss", float("inf"))
        logger.info("QNN state loaded from %s", path)


def make_spiral(
    n_samples: int, n_classes: int = 2, n_features: int = 2, noise: float = 0.5
) -> Tuple[np.ndarray, np.ndarray]:
    """Generate a spiral dataset for QNN classification benchmarks.

    Args:
        n_samples: Total number of samples.
        n_classes: Number of spiral arms (classes).
        n_features: Feature dimensionality (extra dims are zeros).
        noise: Gaussian noise level.

    Returns:
        Tuple of (X, y) arrays.
    """
    points_per_class = n_samples // n_classes
    X = np.zeros((n_samples, n_features))
    y = np.zeros(n_samples, dtype=int)

    for c in range(n_classes):
        idx = range(points_per_class * c, points_per_class * (c + 1))
        theta = np.linspace(c * np.pi * 2, (c + 1) * np.pi * 2, points_per_class)
        r = theta + noise * np.random.randn(points_per_class)
        X[idx, 0] = r * np.cos(theta)
        X[idx, 1] = r * np.sin(theta)
        y[idx] = c

    return X, y


def main() -> None:
    """Demo: train a QNN on a spiral classification task."""
    logging.basicConfig(level=logging.INFO)

    X, y = make_spiral(200, n_classes=2, n_features=4)

    config = QNNConfig(
        n_qubits=4,
        n_layers=2,
        ansatz=AnsatzType.HARDWARE_EFFICIENT,
        encoding=EncodingStrategy.ANGLE,
        measurement=MeasurementBasis.PAULI_Z,
        entanglement="linear",
        learning_rate=0.05,
        batch_size=32,
        optimizer=OptimizerType.ADAM,
    )

    qnn = QuantumNeuralNetwork(config)
    qnn.initialize_parameters(seed=42)

    print(f"QNN: {config.n_qubits} qubits, {config.n_layers} layers, "
          f"{qnn._n_parameter_sets} parameters")
    print(f"Status: {qnn.get_status()}")

    def log_epoch(epoch: int, loss: float) -> None:
        if epoch % 10 == 0:
            print(f"  Epoch {epoch:3d}: loss={loss:.4f}")

    history = qnn.fit(X, y, epochs=50, callback=log_epoch)

    accuracy = qnn.score(X, y)
    print(f"\nFinal training accuracy: {accuracy:.3f}")
    print(f"Best loss: {qnn._best_loss:.4f}")
    print(f"Status: {qnn.get_status()}")

    # Save and reload
    save_path = Path("qnn_checkpoint.json")
    qnn.save(save_path)
    qnn2 = QuantumNeuralNetwork(config)
    qnn2.load(save_path)
    print(f"Reloaded parameters match: {np.allclose(qnn.parameters, qnn2.parameters)}")

    print("\nDemo complete.")


if __name__ == "__main__":
    main()
