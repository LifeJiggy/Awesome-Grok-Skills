"""
Quantum Kernel Methods Module
Part of the quantum-ml skill domain

Provides quantum feature map construction, kernel matrix estimation,
quantum SVM training, and kernel alignment evaluation.
"""

from __future__ import annotations

import warnings
import math
import json
import hashlib
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from functools import lru_cache

import numpy as np

logger = logging.getLogger(__name__)


class FeatureMapType(Enum):
    """Supported quantum feature map architectures."""
    PAULI_Z = auto()            # Simple single-qubit RZ encoding
    PAULI_Z_Z = auto()          # ZZFeatureMap: alternating RZ and ZZ entangling
    PAULI_XZ = auto()           # XZFeatureMap: alternating RX and ZZ
    AMPLITUDE = auto()          # Amplitude encoding feature map
    IQP = auto()                # Instantaneous Quantum Polynomial
    QAOA = auto()               # QAOA-inspired encoding
    CUSTOM = auto()

    def __repr__(self) -> str:
        return f"FeatureMapType.{self.name}"


class EstimatorType(Enum):
    """Kernel estimation methods."""
    SWAP_TEST = auto()          # SWAP test overlap estimation
    STATE_PREPARATION = auto()  # Direct state overlap via inner product
    FIDELITY = auto()           # Quantum state fidelity estimation
    HISTOGRAM = auto()          # Measurement histogram overlap
    SIMULATED = auto()          # Simulated (exact) kernel computation

    def __repr__(self) -> str:
        return f"EstimatorType.{self.name}"


class KernelStatus(Enum):
    """Status of kernel computation or training."""
    IDLE = auto()
    COMPUTING = auto()
    READY = auto()
    ERROR = auto()
    CACHED = auto()

    def __repr__(self) -> str:
        return f"KernelStatus.{self.name}"


class SVMKernel(Enum):
    """SVM kernel types for comparison."""
    QUANTUM = auto()
    RBF = auto()
    POLYNOMIAL = auto()
    LAPLACIAN = auto()
    LINEAR = auto()
    SIGMOID = auto()

    def __repr__(self) -> str:
        return f"SVMKernel.{self.name}"


@dataclass
class FeatureMapConfig:
    """Configuration for a quantum feature map.

    Attributes:
        n_qubits: Number of qubits in the feature map circuit.
        feature_map_type: Architecture of the feature map.
        depth: Number of encoding layers.
        entanglement: Entanglement strategy — 'linear', 'full', 'circular', 'none'.
        data_reuploading: Whether to re-encode data in each layer.
        rotation_gates: Gates used for data encoding per qubit.
    """
    n_qubits: int = 4
    feature_map_type: FeatureMapType = FeatureMapType.PAULI_Z_Z
    depth: int = 2
    entanglement: str = "full"
    data_reuploading: bool = True
    rotation_gates: List[str] = field(default_factory=lambda: ["RZ"])

    def __post_init__(self) -> None:
        if self.n_qubits < 1:
            raise ValueError("n_qubits must be >= 1.")
        if self.depth < 1:
            raise ValueError("depth must be >= 1.")

    def validate(self) -> List[str]:
        errors = []
        if self.n_qubits > 30:
            errors.append("n_qubits > 30 is impractical for exact simulation.")
        if self.entanglement not in ("linear", "full", "circular", "none"):
            errors.append(f"Unknown entanglement strategy: {self.entanglement}")
        return errors


@dataclass
class KernelConfig:
    """Configuration for a quantum kernel.

    Attributes:
        n_qubits: Number of qubits for the feature map.
        feature_map: Feature map name or type string.
        feature_map_depth: Depth of the feature map circuit.
        estimator: Kernel estimation method.
        regularization: Tikhonov regularization for kernel matrix inversion.
        shots: Number of measurement shots; None for analytic mode.
        cache_dir: Directory for caching kernel matrices.
    """
    n_qubits: int = 4
    feature_map: str = "zzfeaturemap"
    feature_map_depth: int = 2
    estimator: EstimatorType = EstimatorType.SIMULATED
    regularization: float = 0.01
    shots: Optional[int] = None
    cache_dir: Optional[str] = None

    def __post_init__(self) -> None:
        if self.n_qubits < 1:
            raise ValueError("n_qubits must be >= 1.")
        if self.feature_map_depth < 1:
            raise ValueError("feature_map_depth must be >= 1.")
        if self.regularization < 0:
            raise ValueError("regularization must be >= 0.")

    def validate(self) -> List[str]:
        errors = []
        if self.n_qubits > 30:
            errors.append("n_qubits > 30 may be impractical.")
        if self.shots is not None and self.shots < 1:
            errors.append("shots must be >= 1 or None.")
        return errors


@dataclass
class KernelResult:
    """Result of a kernel computation."""
    kernel_matrix: np.ndarray
    n_samples: int
    computation_time: float
    is_positive_semidefinite: bool
    condition_number: float
    min_eigenvalue: float
    cached: bool = False


@dataclass
class SVMResult:
    """Result of SVM training with a quantum kernel."""
    accuracy: float
    train_accuracy: float
    n_support_vectors: int
    support_vector_indices: List[int]
    dual_coefficients: np.ndarray
    training_time: float
    kernel_type: str


class QuantumFeatureMap:
    """Quantum feature map for embedding classical data into quantum states.

    This class constructs parameterized quantum circuits that map classical
    feature vectors to quantum states in a high-dimensional Hilbert space.
    """

    def __init__(self, config: Optional[FeatureMapConfig] = None):
        self.config = config or FeatureMapConfig()
        errors = self.config.validate()
        if errors:
            raise ValueError(f"Invalid feature map config: {'; '.join(errors)}")

        self._n_parameters = self._compute_n_parameters()
        self._parameters: Optional[np.ndarray] = None

    def _compute_n_parameters(self) -> int:
        """Compute total number of trainable parameters in the feature map."""
        n = self.config.n_qubits
        d = self.config.depth
        n_rot = len(self.config.rotation_gates)

        if self.config.feature_map_type == FeatureMapType.PAULI_Z:
            return n * d
        elif self.config.feature_map_type == FeatureMapType.PAULI_Z_Z:
            # RZ layers + ZZ entangling parameters
            entangling_params = self._count_entangling_params()
            return n * d + entangling_params * d
        elif self.config.feature_map_type == FeatureMapType.PAULI_XZ:
            return n * 2 * d + self._count_entangling_params() * d
        elif self.config.feature_map_type == FeatureMapType.IQP:
            return n + n * (n - 1) // 2
        return n * n_rot * d

    def _count_entangling_params(self) -> int:
        """Count entangling gate parameters per layer."""
        n = self.config.n_qubits
        if self.config.entanglement == "linear":
            return n - 1
        elif self.config.entanglement == "circular":
            return n
        elif self.config.entanglement == "full":
            return n * (n - 1) // 2
        return 0

    def initialize_parameters(self, seed: Optional[int] = None) -> np.ndarray:
        """Initialize feature map parameters.

        Args:
            seed: Random seed for reproducibility.

        Returns:
            Parameter array of shape (n_parameters,).
        """
        rng = np.random.default_rng(seed)
        self._parameters = rng.uniform(-np.pi, np.pi, size=self._n_parameters)
        return self._parameters.copy()

    def encode(self, x: np.ndarray, parameters: Optional[np.ndarray] = None) -> List[Dict[str, Any]]:
        """Encode a classical feature vector into quantum circuit operations.

        Args:
            x: Feature vector of shape (n_features,). n_features <= n_qubits.
            parameters: Optional feature map parameters.

        Returns:
            List of gate operation dictionaries.
        """
        params = parameters if parameters is not None else self._parameters
        if params is None:
            self.initialize_parameters()
            params = self._parameters

        ops = []
        n = self.config.n_qubits
        d = self.config.depth
        offset = 0

        for layer in range(d):
            # Encoding block
            if self.config.feature_map_type == FeatureMapType.PAULI_Z:
                for q in range(min(n, len(x))):
                    ops.append({"gate": "RZ", "qubit": q, "angle": float(x[q])})
                offset += n

            elif self.config.feature_map_type == FeatureMapType.PAULI_Z_Z:
                # RZ(data) layer
                for q in range(min(n, len(x))):
                    ops.append({"gate": "RZ", "qubit": q, "angle": float(x[q])})

                # ZZ entangling layer
                pairs = self._get_entangling_pairs()
                for ctrl, tgt in pairs:
                    if ctrl < len(x) and tgt < len(x):
                        ops.append({
                            "gate": "ZZ",
                            "qubits": [ctrl, tgt],
                            "angle": float(x[ctrl] * x[tgt]),
                        })

                # Additional parameterized rotations if not data reuploading
                if not self.config.data_reuploading:
                    for q in range(n):
                        ops.append({
                            "gate": "RZ",
                            "qubit": q,
                            "angle": float(params[offset + q]) if offset + q < len(params) else 0.0,
                        })
                    offset += n

            elif self.config.feature_map_type == FeatureMapType.IQP:
                # Hadamard layer
                for q in range(min(n, len(x))):
                    ops.append({"gate": "H", "qubit": q})

                # Data encoding
                for q in range(min(n, len(x))):
                    ops.append({"gate": "RZ", "qubit": q, "angle": float(x[q])})

                # Entangling + product encoding
                for i in range(min(n, len(x))):
                    for j in range(i + 1, min(n, len(x))):
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
                        ops.append({
                            "gate": "CNOT",
                            "control": i,
                            "target": j,
                        })

            # Amplitude encoding (special case)
            elif self.config.feature_map_type == FeatureMapType.AMPLITUDE:
                n_features = 2 ** n
                padded = np.zeros(n_features)
                padded[: min(len(x), n_features)] = x[: min(len(x), n_features)]
                norm = np.linalg.norm(padded)
                if norm > 0:
                    padded /= norm
                ops.append({"gate": "INIT_STATE", "amplitudes": padded.tolist()})

        return ops

    def _get_entangling_pairs(self) -> List[Tuple[int, int]]:
        """Get qubit pairs for entanglement based on the configured strategy."""
        n = self.config.n_qubits
        if self.config.entanglement == "linear":
            return [(i, i + 1) for i in range(n - 1)]
        elif self.config.entanglement == "circular":
            return [(i, (i + 1) % n) for i in range(n)]
        elif self.config.entanglement == "full":
            return [(i, j) for i in range(n) for j in range(i + 1, n)]
        return []

    @property
    def circuit_depth(self) -> int:
        """Estimated circuit depth of the feature map."""
        n = self.config.n_qubits
        if self.config.feature_map_type in (FeatureMapType.PAULI_Z, FeatureMapType.AMPLITUDE):
            return self.config.depth
        elif self.config.feature_map_type in (FeatureMapType.PAULI_Z_Z, FeatureMapType.PAULI_XZ):
            return self.config.depth * 3  # encoding + entangling + possible extra
        return self.config.depth * 2

    @property
    def n_parameters(self) -> int:
        return self._n_parameters


class QuantumKernel:
    """Quantum kernel matrix computation and evaluation.

    Computes the Gram matrix K[i,j] = |<psi(x_i)|psi(x_j)>|^2 where
    |psi(x)> is the quantum state produced by encoding x through the
    feature map circuit.
    """

    def __init__(
        self,
        config: Optional[KernelConfig] = None,
        cache_dir: Optional[str] = None,
    ):
        self.config = config or KernelConfig()
        errors = self.config.validate()
        if errors:
            raise ValueError(f"Invalid kernel config: {'; '.join(errors)}")

        self.feature_map = QuantumFeatureMap(FeatureMapConfig(
            n_qubits=self.config.n_qubits,
            depth=self.config.feature_map_depth,
        ))

        self._kernel_cache: Dict[str, np.ndarray] = {}
        self._cache_dir = Path(cache_dir or self.config.cache_dir or ".kernel_cache")
        self._status: KernelStatus = KernelStatus.IDLE
        self._last_result: Optional[KernelResult] = None

        if self._cache_dir:
            self._cache_dir.mkdir(parents=True, exist_ok=True)

    def _cache_key(self, X: np.ndarray) -> str:
        """Generate a cache key from the data matrix."""
        data_bytes = X.tobytes()
        return hashlib.sha256(data_bytes).hexdigest()[:16]

    def _get_cached(self, key: str) -> Optional[np.ndarray]:
        """Retrieve a cached kernel matrix."""
        if key in self._kernel_cache:
            return self._kernel_cache[key]
        cache_file = self._cache_dir / f"{key}.npy"
        if cache_file.exists():
            matrix = np.load(cache_file)
            self._kernel_cache[key] = matrix
            return matrix
        return None

    def _store_cached(self, key: str, matrix: np.ndarray) -> None:
        """Store a kernel matrix in cache."""
        self._kernel_cache[key] = matrix
        cache_file = self._cache_dir / f"{key}.npy"
        np.save(cache_file, matrix)

    def compute_kernel_matrix(
        self, X: np.ndarray, X2: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """Compute the kernel matrix between datasets.

        Args:
            X: First dataset of shape (n_samples, n_features).
            X2: Optional second dataset for cross-kernel. If None, computes K(X, X).

        Returns:
            Kernel matrix of shape (n_samples, n_samples) or (n, m) if X2 given.
        """
        self._status = KernelStatus.COMPUTING
        start_time = datetime.now()

        X = np.asarray(X, dtype=np.float64)
        if X2 is not None:
            X2 = np.asarray(X2, dtype=np.float64)

        # Check cache
        cache_key = self._cache_key(X)
        if X2 is None and cache_key in self._kernel_cache:
            self._status = KernelStatus.CACHED
            logger.info("Kernel matrix retrieved from cache (key=%s)", cache_key)
            return self._kernel_cache[cache_key]

        n = len(X)
        m = n if X2 is None else len(X2)
        K = np.zeros((n, m))

        for i in range(n):
            j_start = i if X2 is None else 0
            for j in range(j_start, m):
                xi = X[i]
                xj = X[j] if X2 is None else X2[j]
                k_val = self._compute_kernel_entry(xi, xj)
                K[i, j] = k_val
                if X2 is None and i != j:
                    K[j, i] = k_val

        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info("Kernel matrix computed: %dx%d in %.3fs", n, m, elapsed)

        # Cache the result
        if X2 is None:
            self._store_cached(cache_key, K)

        # Validate PSD property
        eigenvalues = np.linalg.eigvalsh(K)
        is_psd = bool(np.all(eigenvalues >= -1e-10))
        cond_number = float(eigenvalues[-1] / max(eigenvalues[0], 1e-15))

        self._last_result = KernelResult(
            kernel_matrix=K,
            n_samples=n,
            computation_time=elapsed,
            is_positive_semidefinite=is_psd,
            condition_number=cond_number,
            min_eigenvalue=float(eigenvalues[0]),
        )

        if not is_psd:
            warnings.warn(
                f"Kernel matrix is not PSD (min eigenvalue: {eigenvalues[0]:.6e}). "
                "Consider applying regularization or eigenvalue clipping."
            )

        self._status = KernelStatus.READY
        return K

    def _compute_kernel_entry(self, x1: np.ndarray, x2: np.ndarray) -> float:
        """Compute a single kernel entry K(x1, x2) = |<psi(x1)|psi(x2)>|^2.

        Uses simulated state vector overlap for the kernel entry.
        """
        # Simulate feature map overlap using a simplified model
        # that captures the essential structure of quantum kernel computation
        ops1 = self.feature_map.encode(x1)
        ops2 = self.feature_map.encode(x2)

        # Compute kernel value via simulated overlap
        # For ZZ feature maps: product of cos terms for each qubit pair
        k_val = 1.0
        n = self.config.n_qubits

        for q in range(min(n, len(x1), len(x2))):
            diff = x1[q] - x2[q]
            k_val *= np.cos(diff / 2) ** 2

        # Add entangling contributions
        if self.config.feature_map_depth > 1:
            for d in range(1, self.config.feature_map_depth):
                for q in range(min(n - 1, len(x1) - 1, len(x2) - 1)):
                    product_diff = (x1[q] * x1[q + 1]) - (x2[q] * x2[q + 1])
                    k_val *= np.cos(product_diff / 2) ** (2 * d)

        return max(0.0, min(1.0, k_val))

    def normalize_kernel(self, K: np.ndarray) -> np.ndarray:
        """Normalize kernel matrix so that diagonal entries equal 1.

        Args:
            K: Kernel matrix of shape (n, n).

        Returns:
            Normalized kernel matrix.
        """
        diag = np.sqrt(np.diag(K))
        diag = np.where(diag > 0, diag, 1.0)
        return K / np.outer(diag, diag)

    def clip_eigenvalues(self, K: np.ndarray, epsilon: float = 1e-6) -> np.ndarray:
        """Clip negative eigenvalues to enforce positive semi-definiteness.

        Args:
            K: Kernel matrix of shape (n, n).
            epsilon: Minimum eigenvalue after clipping.

        Returns:
            PSD kernel matrix.
        """
        eigenvalues, eigenvectors = np.linalg.eigh(K)
        eigenvalues = np.maximum(eigenvalues, epsilon)
        return eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T

    def get_status(self) -> Dict[str, Any]:
        """Return current kernel status."""
        return {
            "status": self._status.name,
            "n_qubits": self.config.n_qubits,
            "feature_map": self.config.feature_map,
            "cache_size": len(self._kernel_cache),
            "last_result": {
                "n_samples": self._last_result.n_samples,
                "is_psd": self._last_result.is_positive_semidefinite,
                "condition_number": self._last_result.condition_number,
            } if self._last_result else None,
        }


class QuantumSVM:
    """Quantum Support Vector Machine classifier.

    Trains an SVM using a precomputed quantum kernel matrix.
    """

    def __init__(self, config: Optional[KernelConfig] = None):
        self.config = config or KernelConfig()
        self.kernel = QuantumKernel(self.config)
        self._support_vectors: Optional[np.ndarray] = None
        self._support_labels: Optional[np.ndarray] = None
        self._dual_coefs: Optional[np.ndarray] = None
        self._bias: float = 0.0
        self._X_train: Optional[np.ndarray] = None
        self._kernel_matrix_train: Optional[np.ndarray] = None

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        precomputed_kernel: bool = True,
    ) -> "QuantumSVM":
        """Train the quantum SVM.

        Args:
            X: Training features of shape (n_samples, n_features).
            y: Training labels of shape (n_samples,) with values in {-1, +1} or {0, 1}.
            precomputed_kernel: Whether to use precomputed kernel matrix.

        Returns:
            Self for chaining.
        """
        start_time = datetime.now()

        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y)

        # Map labels to {-1, +1}
        unique_labels = np.unique(y)
        if set(unique_labels) == {0, 1}:
            y_svm = 2 * y - 1
        else:
            y_svm = y.copy()

        self._X_train = X

        # Compute kernel matrix
        logger.info("Computing quantum kernel matrix for %d samples...", len(X))
        K = self.kernel.compute_kernel_matrix(X)

        # Normalize and regularize
        K = self.kernel.normalize_kernel(K)
        K = K + self.config.regularization * np.eye(len(K))

        self._kernel_matrix_train = K

        # Simplified SMO-like solver (for demonstration)
        n = len(y_svm)
        alpha = np.zeros(n)
        self._bias = 0.0

        # Simple gradient-based dual optimization
        for _ in range(100):
            margins = (alpha * y_svm) @ K + self._bias
            violations = y_svm * margins < 1
            grad = 1 - violations * y_svm * margins
            alpha += 0.01 * grad
            alpha = np.maximum(alpha, 0)

            # Update bias
            sv_mask = alpha > 1e-6
            if np.any(sv_mask):
                self._bias = np.mean(
                    y_svm[sv_mask] - (alpha * y_svm) @ K[:, sv_mask]
                )

        self._dual_coefs = alpha * y_svm
        self._support_labels = y_svm
        self._support_vectors = X[alpha > 1e-6]

        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info("Quantum SVM trained in %.3fs", elapsed)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict class labels for new samples.

        Args:
            X: Test features of shape (n_samples, n_features).

        Returns:
            Predicted labels in the same format as training labels.
        """
        if self._X_train is None or self._dual_coefs is None:
            raise RuntimeError("SVM not trained. Call fit() first.")

        X = np.asarray(X, dtype=np.float64)

        # Compute cross-kernel matrix
        K_cross = np.zeros((len(X), len(self._X_train)))
        for i in range(len(X)):
            for j in range(len(self._X_train)):
                K_cross[i, j] = self.kernel._compute_kernel_entry(X[i], self._X_train[j])

        # Decision function
        decision = K_cross @ self._dual_coefs + self._bias

        # Map back to original label format
        predictions = np.where(decision >= 0, 1, -1)
        if self._support_labels is not None and set(np.unique(self._support_labels)) == {-1, 1}:
            # Check if original labels were 0/1
            unique_orig = np.unique(self._support_labels)
            if not np.all(np.isin(unique_orig, [-1, 1])):
                predictions = (predictions + 1) // 2

        return predictions

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Compute classification accuracy.

        Args:
            X: Test features of shape (n_samples, n_features).
            y: True labels of shape (n_samples,).

        Returns:
            Accuracy in [0, 1].
        """
        preds = self.predict(X)
        return float(np.mean(preds == y))

    def get_status(self) -> Dict[str, Any]:
        """Return current SVM status."""
        return {
            "kernel_status": self.kernel.get_status(),
            "n_support_vectors": len(self._support_vectors) if self._support_vectors is not None else 0,
            "bias": self._bias,
        }


def alignment_score(K: np.ndarray, y: np.ndarray) -> float:
    """Compute kernel-target alignment.

    Measures how well the kernel matrix correlates with the target labels.
    Higher values indicate better kernel quality for the classification task.

    Args:
        K: Kernel matrix of shape (n, n).
        y: Target labels of shape (n,) in {-1, +1}.

    Returns:
        Alignment score in [0, 1]. Values > 0.5 are generally good.
    """
    y = np.asarray(y)
    if set(np.unique(y)) == {0, 1}:
        y = 2 * y - 1

    n = len(y)
    # Target kernel: K_y[i,j] = y[i]*y[j]
    K_y = np.outer(y, y)

    # Frobenius inner product
    numerator = np.sum(K * K_y)
    denominator = np.sqrt(np.sum(K ** 2) * np.sum(K_y ** 2))

    if denominator == 0:
        return 0.0

    alignment = float(numerator / denominator)
    return alignment


def benchmark_kernels(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    quantum_config: Optional[KernelConfig] = None,
    classical_configs: Optional[Dict[str, Dict[str, Any]]] = None,
) -> Dict[str, Dict[str, Any]]:
    """Benchmark quantum vs classical kernels on classification tasks.

    Args:
        X_train: Training features.
        y_train: Training labels.
        X_test: Test features.
        y_test: Test labels.
        quantum_config: Configuration for the quantum kernel.
        classical_configs: Dictionary of classical kernel configurations.

    Returns:
        Dictionary mapping kernel name to metrics (accuracy, train_time).
    """
    results: Dict[str, Dict[str, Any]] = {}

    # Quantum kernel
    if quantum_config is not None:
        start = datetime.now()
        qsvm = QuantumSVM(quantum_config)
        qsvm.fit(X_train, y_train)
        acc = qsvm.score(X_test, y_test)
        elapsed = (datetime.now() - start).total_seconds()
        results["quantum"] = {
            "accuracy": acc,
            "train_time": elapsed,
            "type": "quantum",
        }

    # Classical kernels (simplified simulation)
    if classical_configs:
        from sklearn.svm import SVC

        for name, params in classical_configs.items():
            start = datetime.now()
            try:
                svm = SVC(kernel=name if name != "laplacian" else "rbf", **params)
                svm.fit(X_train, y_train)
                acc = svm.score(X_test, y_test)
            except Exception as e:
                logger.warning("Classical kernel %s failed: %s", name, e)
                acc = 0.0
            elapsed = (datetime.now() - start).total_seconds()
            results[name] = {
                "accuracy": acc,
                "train_time": elapsed,
                "type": "classical",
            }

    return results


def main() -> None:
    """Demo: quantum kernel classification on a synthetic dataset."""
    logging.basicConfig(level=logging.INFO)

    # Generate a simple dataset
    np.random.seed(42)
    n = 60
    X_pos = np.random.randn(n // 2, 4) + 1.0
    X_neg = np.random.randn(n // 2, 4) - 1.0
    X_train = np.vstack([X_pos, X_neg])
    y_train = np.array([1] * (n // 2) + [0] * (n // 2))

    X_test_pos = np.random.randn(20, 4) + 1.0
    X_test_neg = np.random.randn(20, 4) - 1.0
    X_test = np.vstack([X_test_pos, X_test_neg])
    y_test = np.array([1] * 20 + [0] * 20)

    # Feature map
    print("=== Quantum Feature Map ===")
    fm_config = FeatureMapConfig(n_qubits=4, feature_map_type=FeatureMapType.PAULI_Z_Z, depth=2)
    fm = QuantumFeatureMap(fm_config)
    fm.initialize_parameters(seed=42)
    ops = fm.encode(X_train[0])
    print(f"Encoded {len(ops)} circuit operations for first sample")
    print(f"Feature map: {fm.n_parameters} parameters, depth ~{fm.circuit_depth}")

    # Kernel matrix
    print("\n=== Quantum Kernel Matrix ===")
    kernel_config = KernelConfig(n_qubits=4, feature_map="zzfeaturemap", feature_map_depth=2)
    kernel = QuantumKernel(kernel_config)
    K = kernel.compute_kernel_matrix(X_train[:20])  # Small subset for speed
    print(f"Kernel matrix shape: {K.shape}")
    print(f"Kernel diagonal mean: {np.mean(np.diag(K)):.4f}")
    print(f"Is PSD: {kernel._last_result.is_positive_semidefinite}")
    print(f"Condition number: {kernel._last_result.condition_number:.2f}")

    # Normalization
    K_norm = kernel.normalize_kernel(K)
    print(f"Normalized diagonal mean: {np.mean(np.diag(K_norm)):.4f}")

    # Kernel alignment
    align = alignment_score(K, y_train[:20])
    print(f"\nKernel-target alignment: {align:.4f}")

    # Quantum SVM
    print("\n=== Quantum SVM ===")
    qsvm_config = KernelConfig(n_qubits=4, feature_map_depth=2, regularization=0.1)
    qsvm = QuantumSVM(qsvm_config)
    qsvm.fit(X_train[:30], y_train[:30])
    accuracy = qsvm.score(X_test[:20], y_test[:20])
    print(f"QSVM test accuracy: {accuracy:.3f}")
    print(f"SVM status: {qsvm.get_status()}")

    print("\nKernel status:", kernel.get_status())
    print("\nDemo complete.")


if __name__ == "__main__":
    main()
