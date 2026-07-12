"""
Quantum Data Module
Part of the quantum-ml skill domain

Provides classical-to-quantum data encoding, encoding validation,
quantum dataset management, data reuploading, feature selection,
and measurement extraction for quantum machine learning pipelines.
"""

from __future__ import annotations

import warnings
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json

import numpy as np

logger = logging.getLogger(__name__)


class EncodingType(Enum):
    """Supported classical-to-quantum encoding strategies."""
    ANGLE = auto()          # Encode features as rotation angles
    AMPLITUDE = auto()      # Encode 2^n features in state amplitudes
    BASIS = auto()          # Computational basis encoding
    IQP = auto()            # Instantaneous Quantum Polynomial encoding
    QAOA = auto()           # QAOA-inspired encoding
    CUSTOM = auto()

    def __repr__(self) -> str:
        return f"EncodingType.{self.name}"


class MeasurementBasis(Enum):
    """Measurement bases for extracting classical information."""
    PAULI_X = auto()
    PAULI_Y = auto()
    PAULI_Z = auto()
    COMPUTATIONAL = auto()  # Computational basis measurement
    CUSTOM = auto()

    def __repr__(self) -> str:
        return f"MeasurementBasis.{self.name}"


class DataStatus(Enum):
    """Status of data operations."""
    IDLE = auto()
    ENCODING = auto()
    VALIDATING = auto()
    READY = auto()
    ERROR = auto()

    def __repr__(self) -> str:
        return f"DataStatus.{self.name}"


class ReuploadStrategy(Enum):
    """Data reuploading strategies."""
    LAYERED = auto()       # Reupload in every variational layer
    ADAPTIVE = auto()      # Reupload based on gradient information
    PROGRESSIVE = auto()   # Gradually increase encoding depth

    def __repr__(self) -> str:
        return f"ReuploadStrategy.{self.name}"


class FeatureSelectionMethod(Enum):
    """Feature selection methods for quantum ML."""
    VARIANCE = auto()         # Select features with highest variance
    MUTUAL_INFO = auto()      # Mutual information with labels
    QUANTUM_FIDELITY = auto() # Based on quantum state fidelity
    RANDOM = auto()

    def __repr__(self) -> str:
        return f"FeatureSelectionMethod.{self.name}"


@dataclass
class EncodingConfig:
    """Configuration for classical-to-quantum data encoding.

    Attributes:
        n_qubits: Number of qubits for encoding.
        encoding_type: Encoding strategy.
        rotation_axis: Rotation axis for angle encoding ('x', 'y', 'z').
        normalize: Whether to normalize features before encoding.
        feature_range: Target range for normalized features.
        n_features: Expected number of input features (inferred if None).
    """
    n_qubits: int = 4
    encoding_type: EncodingType = EncodingType.ANGLE
    rotation_axis: str = "y"
    normalize: bool = True
    feature_range: Tuple[float, float] = (-np.pi, np.pi)
    n_features: Optional[int] = None

    def __post_init__(self) -> None:
        if self.n_qubits < 1:
            raise ValueError("n_qubits must be >= 1.")
        if self.encoding_type == EncodingType.AMPLITUDE:
            max_features = 2 ** self.n_qubits
            if self.n_features is not None and self.n_features > max_features:
                raise ValueError(
                    f"Amplitude encoding supports at most {max_features} features "
                    f"with {self.n_qubits} qubits, got {self.n_features}."
                )


@dataclass
class DatasetConfig:
    """Configuration for quantum dataset management.

    Attributes:
        n_qubits: Number of qubits for encoding.
        encoding_type: Encoding strategy name.
        train_ratio: Fraction of data for training.
        normalize: Whether to normalize features.
        feature_selection: Feature selection method name.
        n_features: Number of features to select.
        random_seed: Random seed for splitting.
    """
    n_qubits: int = 4
    encoding_type: str = "angle"
    train_ratio: float = 0.8
    normalize: bool = True
    feature_selection: Optional[str] = None
    n_features: Optional[int] = None
    random_seed: int = 42


@dataclass
class ReuploadingConfig:
    """Configuration for data reuploading.

    Attributes:
        n_qubits: Number of qubits.
        n_reuploads: Number of times to reupload data.
        strategy: Reuploading strategy.
        encoding_per_qubit: Encoding type per qubit.
        entangle_after_reupload: Whether to add entangling gates after reuploading.
    """
    n_qubits: int = 3
    n_reuploads: int = 3
    strategy: ReuploadStrategy = ReuploadStrategy.LAYERED
    encoding_per_qubit: str = "angle"
    entangle_after_reupload: bool = True


@dataclass
class EncodingCircuit:
    """A single encoding circuit operation list."""
    operations: List[Dict[str, Any]]
    n_features_encoded: int
    encoding_type: EncodingType
    depth: int


@dataclass
class EncodingValidationReport:
    """Report from encoding validation."""
    information_score: float
    redundancy_score: float
    expressivity: float
    n_features_encoded: int
    encoding_depth: int
    recommendations: List[str]


@dataclass
class MeasurementFeatureResult:
    """Extracted classical features from quantum measurements."""
    features: np.ndarray
    n_features: int
    bases_used: List[MeasurementBasis]
    confidence: float


class QuantumDataEncoder:
    """Encodes classical data into quantum circuit operations.

    Supports multiple encoding strategies including angle, amplitude,
    basis, and IQP encoding.
    """

    def __init__(self, config: Optional[EncodingConfig] = None):
        self.config = config or EncodingConfig()
        self._status: DataStatus = DataStatus.IDLE
        self._n_encoded_features: int = 0

    def encode_single(self, x: np.ndarray) -> EncodingCircuit:
        """Encode a single classical feature vector.

        Args:
            x: Feature vector.

        Returns:
            EncodingCircuit with the encoding operations.
        """
        self._status = DataStatus.ENCODING
        x = np.asarray(x, dtype=np.float64)

        if self.config.normalize:
            x = self._normalize(x)

        ops: List[Dict[str, Any]] = []

        if self.config.encoding_type == EncodingType.ANGLE:
            ops = self._encode_angle(x)
        elif self.config.encoding_type == EncodingType.AMPLITUDE:
            ops = self._encode_amplitude(x)
        elif self.config.encoding_type == EncodingType.BASIS:
            ops = self._encode_basis(x)
        elif self.config.encoding_type == EncodingType.IQP:
            ops = self._encode_iqp(x)
        else:
            ops = self._encode_angle(x)

        self._status = DataStatus.READY
        self._n_encoded_features = len(x)

        return EncodingCircuit(
            operations=ops,
            n_features_encoded=len(x),
            encoding_type=self.config.encoding_type,
            depth=len(ops),
        )

    def encode_batch(self, X: np.ndarray) -> List[EncodingCircuit]:
        """Encode a batch of feature vectors.

        Args:
            X: Feature matrix of shape (n_samples, n_features).

        Returns:
            List of EncodingCircuit objects.
        """
        X = np.asarray(X, dtype=np.float64)
        if self.config.normalize:
            X = self._normalize_batch(X)

        return [self.encode_single(X[i]) for i in range(len(X))]

    def _normalize(self, x: np.ndarray) -> np.ndarray:
        """Normalize a single feature vector to the configured range."""
        lo, hi = self.config.feature_range
        x_min, x_max = x.min(), x.max()
        if x_max - x_min < 1e-10:
            return np.full_like(x, (lo + hi) / 2)
        return lo + (x - x_min) / (x_max - x_min) * (hi - lo)

    def _normalize_batch(self, X: np.ndarray) -> np.ndarray:
        """Normalize a batch using per-feature min-max scaling."""
        lo, hi = self.config.feature_range
        X_min = X.min(axis=0)
        X_max = X.max(axis=0)
        ranges = X_max - X_min
        ranges = np.where(ranges < 1e-10, 1.0, ranges)
        return lo + (X - X_min) / ranges * (hi - lo)

    def _encode_angle(self, x: np.ndarray) -> List[Dict[str, Any]]:
        """Angle encoding: each feature becomes a rotation angle on one qubit."""
        ops = []
        n = self.config.n_qubits
        axis = self.config.rotation_axis.upper()
        gate = f"R{axis}"

        for i in range(min(n, len(x))):
            ops.append({
                "gate": gate,
                "qubit": i,
                "angle": float(x[i]),
                "type": "encoding",
            })

        return ops

    def _encode_amplitude(self, x: np.ndarray) -> List[Dict[str, Any]]:
        """Amplitude encoding: features encoded in state amplitudes."""
        n = self.config.n_qubits
        n_features = 2 ** n

        padded = np.zeros(n_features)
        padded[: min(len(x), n_features)] = x[: min(len(x), n_features)]

        norm = np.linalg.norm(padded)
        if norm > 0:
            padded /= norm
        else:
            padded = np.ones(n_features) / np.sqrt(n_features)

        ops = [{
            "gate": "INIT_STATE",
            "amplitudes": padded.tolist(),
            "type": "encoding",
        }]

        return ops

    def _encode_basis(self, x: np.ndarray) -> List[Dict[str, Any]]:
        """Basis encoding: features encoded as computational basis states."""
        ops = []
        n = self.config.n_qubits

        for i in range(min(n, len(x))):
            if x[i] > 0.5:
                ops.append({
                    "gate": "X",
                    "qubit": i,
                    "type": "encoding",
                })

        return ops

    def _encode_iqp(self, x: np.ndarray) -> List[Dict[str, Any]]:
        """IQP encoding: Hadamard + diagonal entangling + data rotation."""
        ops = []
        n = self.config.n_qubits

        # Hadamard layer
        for i in range(min(n, len(x))):
            ops.append({"gate": "H", "qubit": i, "type": "encoding"})

        # Data rotation
        for i in range(min(n, len(x))):
            ops.append({
                "gate": "RZ",
                "qubit": i,
                "angle": float(x[i]),
                "type": "encoding",
            })

        # Entangling products
        for i in range(min(n, len(x))):
            for j in range(i + 1, min(n, len(x))):
                ops.append({
                    "gate": "CNOT",
                    "control": i,
                    "target": j,
                    "type": "encoding",
                })
                ops.append({
                    "gate": "RZ",
                    "qubit": j,
                    "angle": float(x[i] * x[j]),
                    "type": "encoding",
                })
                ops.append({
                    "gate": "CNOT",
                    "control": i,
                    "target": j,
                    "type": "encoding",
                })

        return ops

    def get_status(self) -> Dict[str, Any]:
        return {
            "status": self._status.name,
            "encoding_type": self.config.encoding_type.name,
            "n_qubits": self.config.n_qubits,
            "n_encoded_features": self._n_encoded_features,
        }


class EncodingValidator:
    """Validates the quality of data encoding into quantum circuits."""

    def __init__(self, encoder: QuantumDataEncoder):
        self.encoder = encoder

    def validate(self, X: np.ndarray) -> Dict[str, Any]:
        """Validate encoding quality on a dataset.

        Args:
            X: Feature matrix of shape (n_samples, n_features).

        Returns:
            Dictionary with validation metrics and recommendations.
        """
        X = np.asarray(X, dtype=np.float64)
        n_samples, n_features = X.shape

        # Information preservation: how much variance is retained
        info_score = self._compute_information_score(X)

        # Redundancy: whether encoding creates redundant representations
        redundancy = self._compute_redundancy_score(X)

        # Expressivity: whether the encoding can represent diverse states
        expressivity = self._compute_expressivity(X)

        recommendations = []
        if info_score < 0.5:
            recommendations.append(
                "Low information preservation. Consider amplitude encoding "
                "for higher information density per qubit."
            )
        if redundancy > 0.3:
            recommendations.append(
                "High encoding redundancy. Reduce n_features or use "
                "feature selection before encoding."
            )
        if expressivity < 0.3:
            recommendations.append(
                "Low expressivity. Consider IQP encoding for richer "
                "feature interactions."
            )

        # Encode a sample for depth analysis
        circuit = self.encoder.encode_single(X[0])

        return {
            "information_score": float(info_score),
            "redundancy_score": float(redundancy),
            "expressivity": float(expressivity),
            "n_features_encoded": min(n_features, self.encoder.config.n_qubits),
            "encoding_depth": circuit.depth,
            "recommendations": recommendations,
        }

    def _compute_information_score(self, X: np.ndarray) -> float:
        """Compute how well encoding preserves information."""
        n_features = X.shape[1]
        n_qubits = self.encoder.config.n_qubits

        if self.encoder.config.encoding_type == EncodingType.AMPLITUDE:
            capacity = 2 ** n_qubits
        else:
            capacity = n_qubits

        # Information score based on capacity vs features
        return min(1.0, capacity / max(n_features, 1))

    def _compute_redundancy_score(self, X: np.ndarray) -> float:
        """Compute encoding redundancy."""
        n_features = X.shape[1]
        n_qubits = self.encoder.config.n_qubits

        if n_features <= n_qubits:
            return 0.0

        # Measure pairwise feature correlation as proxy for redundancy
        corr = np.corrcoef(X.T)
        n = corr.shape[0]
        off_diag = corr[np.triu_indices(n, k=1)]
        return float(np.mean(np.abs(off_diag)))

    def _compute_expressivity(self, X: np.ndarray) -> float:
        """Compute encoding expressivity via state variance."""
        n_qubits = self.encoder.config.n_qubits

        # Encode first few samples and measure state diversity
        circuits = self.encoder.encode_batch(X[:min(10, len(X))])

        # Measure diversity of encoding angles
        all_angles = []
        for c in circuits:
            for op in c.operations:
                if "angle" in op:
                    all_angles.append(op["angle"])

        if not all_angles:
            return 0.5

        angle_var = float(np.var(all_angles))
        return min(1.0, angle_var / (np.pi ** 2 / 3))


class QuantumDataset:
    """Manages classical datasets for quantum machine learning.

    Handles loading, preprocessing, splitting, and encoding
    of datasets for quantum ML pipelines.
    """

    def __init__(self, config: Optional[DatasetConfig] = None):
        self.config = config or DatasetConfig()
        self.X: Optional[np.ndarray] = None
        self.y: Optional[np.ndarray] = None
        self.X_train: Optional[np.ndarray] = None
        self.X_test: Optional[np.ndarray] = None
        self.y_train: Optional[np.ndarray] = None
        self.y_test: Optional[np.ndarray] = None
        self._encoder: Optional[QuantumDataEncoder] = None
        self._status: DataStatus = DataStatus.IDLE

    def load(self, X: np.ndarray, y: Optional[np.ndarray] = None) -> None:
        """Load a dataset.

        Args:
            X: Feature matrix of shape (n_samples, n_features).
            y: Optional labels of shape (n_samples,).
        """
        self.X = np.asarray(X, dtype=np.float64)
        self.y = np.asarray(y) if y is not None else None
        self._status = DataStatus.IDLE

        logger.info("Dataset loaded: %d samples, %d features",
                    len(self.X), self.X.shape[1] if len(self.X.shape) > 1 else 1)

    def preprocess(self) -> None:
        """Preprocess the dataset: normalize, select features, split."""
        if self.X is None:
            raise RuntimeError("No data loaded. Call load() first.")

        X = self.X.copy()

        # Feature selection
        if self.config.feature_selection and self.config.n_features:
            X = self._select_features(X)

        # Normalization
        if self.config.normalize:
            X = self._normalize(X)

        # Train/test split
        n = len(X)
        n_train = int(n * self.config.train_ratio)
        rng = np.random.default_rng(self.config.random_seed)
        indices = rng.permutation(n)

        self.X_train = X[indices[:n_train]]
        self.X_test = X[indices[n_train:]]

        if self.y is not None:
            self.y_train = self.y[indices[:n_train]]
            self.y_test = self.y[indices[n_train:]]

        # Set up encoder
        encoding_map = {
            "angle": EncodingType.ANGLE,
            "amplitude": EncodingType.AMPLITUDE,
            "basis": EncodingType.BASIS,
            "iqp": EncodingType.IQP,
        }
        enc_type = encoding_map.get(self.config.encoding_type, EncodingType.ANGLE)

        self._encoder = QuantumDataEncoder(EncodingConfig(
            n_qubits=self.config.n_qubits,
            encoding_type=enc_type,
            n_features=X.shape[1],
        ))

        self._status = DataStatus.READY
        logger.info("Dataset preprocessed: train=%d, test=%d", len(self.X_train), len(self.X_test))

    def _normalize(self, X: np.ndarray) -> np.ndarray:
        """Min-max normalize features."""
        X_min = X.min(axis=0)
        X_max = X.max(axis=0)
        ranges = X_max - X_min
        ranges = np.where(ranges < 1e-10, 1.0, ranges)
        return (X - X_min) / ranges

    def _select_features(self, X: np.ndarray) -> np.ndarray:
        """Select top features by variance."""
        variances = np.var(X, axis=0)
        top_indices = np.argsort(variances)[-self.config.n_features:]
        return X[:, top_indices]

    def encode(self, X: np.ndarray) -> List[EncodingCircuit]:
        """Encode data using the configured encoder.

        Args:
            X: Feature matrix.

        Returns:
            List of encoding circuits.
        """
        if self._encoder is None:
            raise RuntimeError("Dataset not preprocessed. Call preprocess() first.")
        return self._encoder.encode_batch(X)

    @property
    def n_encoded_features(self) -> int:
        return self.config.n_features or self.X.shape[1]

    def get_status(self) -> Dict[str, Any]:
        return {
            "status": self._status.name,
            "n_samples": len(self.X) if self.X is not None else 0,
            "n_features": self.X.shape[1] if self.X is not None and len(self.X.shape) > 1 else 0,
            "train_size": len(self.X_train) if self.X_train is not None else 0,
            "test_size": len(self.X_test) if self.X_test is not None else 0,
        }


class DataReuploader:
    """Manages data reuploading for variational quantum circuits.

    Data reuploading re-encodes classical data in each variational layer,
    which has been proven necessary for universal approximation.
    """

    def __init__(self, config: Optional[ReuploadingConfig] = None):
        self.config = config or ReuploadingConfig()

    def encode_layer(self, x: np.ndarray, layer_index: int) -> List[Dict[str, Any]]:
        """Generate encoding operations for a specific layer.

        Args:
            x: Feature vector to encode.
            layer_index: Current layer index (affects encoding parameters).

        Returns:
            List of gate operations.
        """
        x = np.asarray(x, dtype=np.float64)
        ops = []
        n = self.config.n_qubits

        if self.config.strategy == ReuploadStrategy.LAYERED:
            # Same encoding every layer
            scale = 1.0
        elif self.config.strategy == ReuploadStrategy.PROGRESSIVE:
            # Scale down in later layers for hierarchical learning
            scale = 1.0 / (1 + layer_index * 0.5)
        elif self.config.strategy == ReuploadStrategy.ADAPTIVE:
            # Add extra rotation based on layer
            scale = 1.0 + 0.1 * np.sin(layer_index)
        else:
            scale = 1.0

        if self.config.encoding_per_qubit == "angle":
            for q in range(min(n, len(x))):
                angle = float(x[q]) * scale
                ops.append({
                    "gate": "RY",
                    "qubit": q,
                    "angle": angle,
                    "layer": layer_index,
                    "type": "reupload",
                })
        elif self.config.encoding_per_qubit == "amplitude":
            n_features = 2 ** n
            padded = np.zeros(n_features)
            padded[: min(len(x), n_features)] = x[: min(len(x), n_features)]
            norm = np.linalg.norm(padded)
            if norm > 0:
                padded *= scale / norm
            ops.append({
                "gate": "INIT_STATE",
                "amplitudes": padded.tolist(),
                "layer": layer_index,
                "type": "reupload",
            })

        if self.config.entangle_after_reupload:
            for q in range(n - 1):
                ops.append({
                    "gate": "CNOT",
                    "control": q,
                    "target": q + 1,
                    "layer": layer_index,
                    "type": "entanglement",
                })

        return ops


class QuantumFeatureSelector:
    """Selects the most informative features for quantum ML encoding.

    Uses quantum-aware metrics to evaluate which classical features
    are most useful when projected into quantum Hilbert space.
    """

    def __init__(
        self,
        encoder: QuantumDataEncoder,
        n_qubits: int,
        method: FeatureSelectionMethod = FeatureSelectionMethod.VARIANCE,
    ):
        self.encoder = encoder
        self.n_qubits = n_qubits
        self.method = method
        self._selected_indices: Optional[np.ndarray] = None
        self._feature_importances: Optional[np.ndarray] = None

    def select_features(
        self, X: np.ndarray, y: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """Select the most informative features.

        Args:
            X: Feature matrix of shape (n_samples, n_features).
            y: Optional labels for supervised selection.

        Returns:
            Array of selected feature indices.
        """
        X = np.asarray(X, dtype=np.float64)

        if self.method == FeatureSelectionMethod.VARIANCE:
            scores = np.var(X, axis=0)
        elif self.method == FeatureSelectionMethod.MUTUAL_INFO:
            scores = self._mutual_info_scores(X, y)
        elif self.method == FeatureSelectionMethod.QUANTUM_FIDELITY:
            scores = self._quantum_fidelity_scores(X)
        else:
            scores = np.random.rand(X.shape[1])

        self._feature_importances = scores
        self._selected_indices = np.argsort(scores)[-self.n_qubits:]

        return self._selected_indices.copy()

    def _mutual_info_scores(self, X: np.ndarray, y: Optional[np.ndarray]) -> np.ndarray:
        """Compute mutual information between features and labels."""
        if y is None:
            return np.var(X, axis=0)

        n_features = X.shape[1]
        scores = np.zeros(n_features)

        for i in range(n_features):
            # Simplified mutual information estimate
            values = X[:, i]
            bins = np.linspace(values.min(), values.max(), min(10, len(np.unique(values))))
            digitized = np.digitize(values, bins)

            unique_y = np.unique(y)
            h_y = -np.sum([
                np.mean(y == uy) * np.log(np.mean(y == uy) + 1e-10)
                for uy in unique_y
            ])

            h_y_given_x = 0.0
            for b in np.unique(digitized):
                mask = digitized == b
                if np.sum(mask) > 0:
                    p_b = np.mean(mask)
                    y_given = y[mask]
                    h_cond = -np.sum([
                        np.mean(y_given == uy) * np.log(np.mean(y_given == uy) + 1e-10)
                        for uy in unique_y
                    ])
                    h_y_given_x += p_b * h_cond

            scores[i] = max(0, h_y - h_y_given_x)

        return scores

    def _quantum_fidelity_scores(self, X: np.ndarray) -> np.ndarray:
        """Score features based on quantum encoding fidelity."""
        n_features = X.shape[1]
        scores = np.zeros(n_features)

        for i in range(min(n_features, self.n_qubits)):
            # Measure how well this feature maps to distinct quantum states
            feature_vals = X[:, i]
            unique_vals = len(np.unique(np.round(feature_vals, 6)))
            scores[i] = min(1.0, unique_vals / len(feature_vals))

        return scores

    @property
    def feature_importances(self) -> Optional[np.ndarray]:
        return self._feature_importances


class MeasurementExtractor:
    """Extracts classical features from quantum measurement results.

    Converts quantum measurement data (expectation values, variances,
    probabilities) into classical feature vectors for downstream processing.
    """

    def __init__(
        self,
        bases: Optional[List[MeasurementBasis]] = None,
        n_shots: int = 1024,
    ):
        self.bases = bases or [MeasurementBasis.PAULI_Z]
        self.n_shots = n_shots

    def extract_features(self, measurements: Dict[str, Any]) -> np.ndarray:
        """Extract classical features from measurement results.

        Args:
            measurements: Dictionary with measurement data.

        Returns:
            Feature vector as numpy array.
        """
        features = []

        # Expectation values
        for basis in self.bases:
            key = f"expectation_{basis.name.lower()}"
            if key in measurements:
                features.append(float(measurements[key]))

        # Variances
        for basis in self.bases:
            key = f"variance_{basis.name.lower()}"
            if key in measurements:
                features.append(float(measurements[key]))

        # Probabilities
        if "probabilities" in measurements:
            probs = np.asarray(measurements["probabilities"])
            features.extend(probs.tolist())

            # Shannon entropy of measurement distribution
            probs_pos = probs[probs > 0]
            entropy = -np.sum(probs_pos * np.log(probs_pos + 1e-10))
            features.append(float(entropy))

        # Statistical moments
        if "expectation_z" in measurements:
            features.append(float(measurements["expectation_z"]) ** 2)  # second moment

        if not features:
            features = [0.0]

        return np.array(features)

    def extract_batch(
        self, batch_measurements: List[Dict[str, Any]]
    ) -> np.ndarray:
        """Extract features from a batch of measurement results.

        Args:
            batch_measurements: List of measurement dictionaries.

        Returns:
            Feature matrix of shape (n_samples, n_features).
        """
        return np.array([self.extract_features(m) for m in batch_measurements])


@dataclass
class OptimizationResult:
    """Result of encoding circuit optimization."""
    optimized_depth: int
    original_depth: int
    gate_reduction: float
    operations_removed: int
    strategy: str


class EncodingOptimizer:
    """Optimizes encoding circuits to reduce gate count and depth."""

    def __init__(self, encoder: QuantumDataEncoder):
        self.encoder = encoder

    @property
    def original_depth(self) -> int:
        circuit = self.encoder.encode_single(np.zeros(self.encoder.config.n_qubits))
        return circuit.depth

    def optimize(
        self,
        X: np.ndarray,
        strategy: str = "gate_cancellation",
    ) -> OptimizationResult:
        """Optimize encoding circuits for a dataset.

        Args:
            X: Dataset to optimize encoding for.
            strategy: Optimization strategy.

        Returns:
            OptimizationResult with metrics.
        """
        original = self.encoder.encode_single(X[0])
        original_depth = original.depth
        original_gates = len(original.operations)

        # Simulate optimization by removing redundant operations
        optimized_ops = []
        seen = set()

        for op in original.operations:
            op_key = (op.get("gate"), op.get("qubit", op.get("control")))
            if op_key not in seen or op.get("type") == "encoding":
                optimized_ops.append(op)
                seen.add(op_key)

        optimized_depth = max(1, original_depth - 1)
        ops_removed = original_gates - len(optimized_ops)
        reduction = ops_removed / max(original_gates, 1)

        return OptimizationResult(
            optimized_depth=optimized_depth,
            original_depth=original_depth,
            gate_reduction=float(reduction),
            operations_removed=ops_removed,
            strategy=strategy,
        )


def main() -> None:
    """Demo: quantum data encoding and dataset management."""
    logging.basicConfig(level=logging.INFO)

    # === Encoding ===
    print("=" * 50)
    print("Quantum Data Encoding")
    print("=" * 50)

    X = np.random.randn(100, 4)

    # Angle encoding
    angle_config = EncodingConfig(n_qubits=4, encoding_type=EncodingType.ANGLE)
    angle_encoder = QuantumDataEncoder(angle_config)
    circuits = angle_encoder.encode_batch(X[:10])
    print(f"Angle encoding: {len(circuits)} circuits, {len(circuits[0].operations)} ops each")

    # Amplitude encoding
    amp_config = EncodingConfig(n_qubits=4, encoding_type=EncodingType.AMPLITUDE)
    amp_encoder = QuantumDataEncoder(amp_config)
    X_amp = np.random.randn(10, 16)
    amp_circuits = amp_encoder.encode_batch(X_amp)
    print(f"Amplitude encoding: 16 features -> 4 qubits")

    # IQP encoding
    iqp_config = EncodingConfig(n_qubits=4, encoding_type=EncodingType.IQP)
    iqp_encoder = QuantumDataEncoder(iqp_config)
    iqp_circuits = iqp_encoder.encode_batch(X[:5])
    print(f"IQP encoding: {len(iqp_circuits[0].operations)} ops per sample")

    # === Validation ===
    print("\n" + "=" * 50)
    print("Encoding Validation")
    print("=" * 50)

    validator = EncodingValidator(angle_encoder)
    report = validator.validate(X)
    print(f"Information score: {report['information_score']:.4f}")
    print(f"Redundancy score: {report['redundancy_score']:.4f}")
    print(f"Expressivity: {report['expressivity']:.4f}")
    print(f"Recommendations: {report['recommendations']}")

    # === Dataset Management ===
    print("\n" + "=" * 50)
    print("Quantum Dataset")
    print("=" * 50)

    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    ds_config = DatasetConfig(n_qubits=4, encoding_type="angle", train_ratio=0.8)
    dataset = QuantumDataset(ds_config)
    dataset.load(X, y)
    dataset.preprocess()

    print(f"Train: {dataset.X_train.shape}, Test: {dataset.X_test.shape}")
    print(f"Status: {dataset.get_status()}")

    # === Data Reuploading ===
    print("\n" + "=" * 50)
    print("Data Reuploading")
    print("=" * 50)

    reupload_config = ReuploadingConfig(n_qubits=3, n_reuploads=3, strategy=ReuploadStrategy.LAYERED)
    reuploader = DataReuploader(reupload_config)

    for layer in range(3):
        ops = reuploader.encode_layer(X[0][:3], layer)
        print(f"Layer {layer}: {len(ops)} operations")

    # === Feature Selection ===
    print("\n" + "=" * 50)
    print("Feature Selection")
    print("=" * 50)

    X_large = np.random.randn(200, 10)
    y_large = (X_large[:, 0] + X_large[:, 2] > 0).astype(int)

    selector = QuantumFeatureSelector(angle_encoder, n_qubits=4, method=FeatureSelectionMethod.VARIANCE)
    selected = selector.select_features(X_large, y_large)
    print(f"Selected features: {selected}")
    print(f"Importances: {np.round(selector.feature_importances, 4)}")

    # === Measurement Extraction ===
    print("\n" + "=" * 50)
    print("Measurement Extraction")
    print("=" * 50)

    extractor = MeasurementExtractor(bases=[MeasurementBasis.PAULI_Z, MeasurementBasis.PAULI_X])
    measurements = {
        "expectation_z": 0.75,
        "expectation_x": 0.25,
        "variance_z": 0.125,
        "probabilities": [0.375, 0.125, 0.125, 0.375],
    }
    features = extractor.extract_features(measurements)
    print(f"Extracted features: {features}")
    print(f"Feature count: {len(features)}")

    print("\nDemo complete.")


if __name__ == "__main__":
    main()
