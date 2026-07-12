"""
Feature Engineering Toolkit

Production-grade feature engineering framework providing automated feature construction,
encoding, scaling, selection, interaction detection, and pipeline orchestration for
building high-quality machine learning inputs.
"""

from __future__ import annotations

import hashlib
import json
import logging
import warnings
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ImputationMethod(Enum):
    MEAN = "mean"
    MEDIAN = "median"
    MODE = "mode"
    CONSTANT = "constant"
    KNN = "knn"
    ITERATIVE = "iterative"
    FORWARD_FILL = "forward_fill"
    BACKWARD_FILL = "backward_fill"


class EncodingMethod(Enum):
    ONE_HOT = "one_hot"
    TARGET = "target"
    ORDINAL = "ordinal"
    FREQUENCY = "frequency"
    BINARY = "binary"
    LEAVE_ONE_OUT = "leave_one_out"
    LABEL = "label"
    BASE_N = "base_n"


class ScalingMethod(Enum):
    STANDARD = "standard"
    MINMAX = "minmax"
    ROBUST = "robust"
    QUANTILE = "quantile"
    MAXABS = "maxabs"
    NORMALIZER = "normalizer"


class TransformationMethod(Enum):
    LOG = "log"
    SQRT = "sqrt"
    BOX_COX = "box_cox"
    YEO_JOHNSON = "yeo_johnson"
    POWER = "power"
    QUANTILE_GAUSSIAN = "quantile_gaussian"


class SelectionMethod(Enum):
    VARIANCE = "variance"
    CORRELATION = "correlation"
    MUTUAL_INFO = "mutual_info"
    CHI_SQUARED = "chi_squared"
    RFE = "rfe"
    L1 = "l1"
    TREE_IMPORTANCE = "tree_importance"
    PERMUTATION = "permutation"
    STABILITY = "stability"


class PipelineStepType(Enum):
    IMPUTATION = "imputation"
    ENCODING = "encoding"
    SCALING = "scaling"
    TRANSFORMATION = "transformation"
    SELECTION = "selection"
    CONSTRUCTION = "construction"
    REDUCTION = "reduction"
    CUSTOM = "custom"


class TaskType(Enum):
    CLASSIFICATION = "classification"
    REGRESSION = "regression"


class CardinalityStrategy(Enum):
    ONE_HOT = "one_hot"
    TARGET = "target"
    FREQUENCY = "frequency"
    BINARY = "binary"
    DROP = "drop"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class PipelineStep:
    """A single step in a feature engineering pipeline."""
    name: str
    transformer: str
    params: Dict[str, Any] = field(default_factory=dict)
    columns: Optional[List[str]] = None
    exclude_columns: Optional[List[str]] = None
    step_type: PipelineStepType = PipelineStepType.CUSTOM
    enabled: bool = True

    def __post_init__(self) -> None:
        if self.step_type == PipelineStepType.CUSTOM:
            step_map = {
                "iterative_imputer": PipelineStepType.IMPUTATION,
                "knn_imputer": PipelineStepType.IMPUTATION,
                "mean_imputer": PipelineStepType.IMPUTATION,
                "target_encoder": PipelineStepType.ENCODING,
                "one_hot_encoder": PipelineStepType.ENCODING,
                "robust_scaler": PipelineStepType.SCALING,
                "standard_scaler": PipelineStepType.SCALING,
                "polynomial_features": PipelineStepType.CONSTRUCTION,
                "mutual_information_selector": PipelineStepType.SELECTION,
                "variance_threshold": PipelineStepType.SELECTION,
            }
            self.step_type = step_map.get(self.transformer, PipelineStepType.CUSTOM)


@dataclass
class EncodingMap:
    """Encoding mapping for categorical features."""
    feature_name: str
    method: EncodingMethod
    mapping: Dict[str, float] = field(default_factory=dict)
    categories: List[str] = field(default_factory=list)
    unknown_value: float = 0.0

    def encode(self, value: str) -> float:
        return self.mapping.get(value, self.unknown_value)


@dataclass
class ScalingParams:
    """Parameters learned during scaler fitting."""
    feature_name: str
    method: ScalingMethod
    mean: Optional[float] = None
    std: Optional[float] = None
    min_val: Optional[float] = None
    max_val: Optional[float] = None
    median: Optional[float] = None
    iqr: Optional[float] = None
    quantiles: Optional[Tuple[NDArray, NDArray]] = None

    def transform(self, value: float) -> float:
        if self.method == ScalingMethod.STANDARD:
            return (value - self.mean) / self.std if self.std > 0 else 0.0
        elif self.method == ScalingMethod.MINMAX:
            rng = self.max_val - self.min_val
            return (value - self.min_val) / rng if rng > 0 else 0.0
        elif self.method == ScalingMethod.ROBUST:
            return (value - self.median) / self.iqr if self.iqr > 0 else 0.0
        elif self.method == ScalingMethod.MAXABS:
            max_abs = max(abs(self.min_val), abs(self.max_val))
            return value / max_abs if max_abs > 0 else 0.0
        return value


@dataclass
class SelectionResult:
    """Result of feature selection."""
    selected_features: List[str]
    removed_features: List[str]
    scores: Dict[str, float]
    method: SelectionMethod
    threshold: Optional[float] = None
    k: Optional[int] = None


@dataclass
class PipelineResult:
    """Result of running a feature engineering pipeline."""
    X_transformed: NDArray
    feature_names: List[str]
    steps_applied: List[str]
    encoding_maps: Dict[str, EncodingMap]
    scaling_params: Dict[str, ScalingParams]
    selection_result: Optional[SelectionResult]
    n_features_before: int
    n_features_after: int
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def summary(self) -> Dict[str, Any]:
        return {
            "steps_applied": self.steps_applied,
            "features_before": self.n_features_before,
            "features_after": self.n_features_after,
            "features_added": self.n_features_after - self.n_features_before,
            "encoding_maps": len(self.encoding_maps),
            "scaling_params": len(self.scaling_params),
            "selection": self.selection_result.method.value if self.selection_result else None,
        }


# ---------------------------------------------------------------------------
# Missing Value Imputation
# ---------------------------------------------------------------------------

class Imputer:
    """Missing value imputation with multiple strategies."""

    def __init__(self, method: ImputationMethod = ImputationMethod.MEAN, **kwargs: Any):
        self.method = method
        self.fill_values: Dict[str, Any] = {}
        self.k = kwargs.get("k", 5)
        self.max_iter = kwargs.get("max_iter", 10)
        self.constant_value = kwargs.get("constant_value", 0)
        self._is_fitted = False

    def fit(self, X: NDArray, feature_names: Optional[List[str]] = None) -> "Imputer":
        n_features = X.shape[1]
        names = feature_names or [f"feature_{i}" for i in range(n_features)]

        for i, name in enumerate(names):
            col = X[:, i]
            missing_mask = np.isnan(col)

            if not np.any(missing_mask):
                self.fill_values[name] = 0.0
                continue

            if self.method == ImputationMethod.MEAN:
                self.fill_values[name] = float(np.nanmean(col))
            elif self.method == ImputationMethod.MEDIAN:
                self.fill_values[name] = float(np.nanmedian(col))
            elif self.method == ImputationMethod.MODE:
                unique, counts = np.unique(col[~missing_mask], return_counts=True)
                self.fill_values[name] = float(unique[np.argmax(counts)])
            elif self.method == ImputationMethod.CONSTANT:
                self.fill_values[name] = self.constant_value
            elif self.method == ImputationMethod.KNN:
                self.fill_values[name] = float(np.nanmean(col))
            elif self.method == ImputationMethod.ITERATIVE:
                self.fill_values[name] = float(np.nanmean(col))
            else:
                self.fill_values[name] = float(np.nanmean(col))

        self._is_fitted = True
        return self

    def transform(self, X: NDArray, feature_names: Optional[List[str]] = None) -> NDArray:
        if not self._is_fitted:
            raise RuntimeError("Imputer must be fitted before transforming.")

        result = X.copy()
        n_features = X.shape[1]
        names = feature_names or [f"feature_{i}" for i in range(n_features)]

        for i, name in enumerate(names):
            col = result[:, i]
            missing_mask = np.isnan(col)
            if np.any(missing_mask):
                fill_val = self.fill_values.get(name, 0.0)

                if self.method == ImputationMethod.FORWARD_FILL:
                    for j in range(1, len(col)):
                        if np.isnan(col[j]):
                            col[j] = col[j - 1] if not np.isnan(col[j - 1]) else fill_val
                elif self.method == ImputationMethod.BACKWARD_FILL:
                    for j in range(len(col) - 2, -1, -1):
                        if np.isnan(col[j]):
                            col[j] = col[j + 1] if not np.isnan(col[j + 1]) else fill_val
                else:
                    col[missing_mask] = fill_val

        return result

    def fit_transform(self, X: NDArray, feature_names: Optional[List[str]] = None) -> NDArray:
        return self.fit(X, feature_names).transform(X, feature_names)

    def create_missing_indicators(self, X: NDArray, feature_names: Optional[List[str]] = None) -> NDArray:
        """Create binary indicators for missing values."""
        n_features = X.shape[1]
        indicators = np.zeros((X.shape[0], n_features))
        for i in range(n_features):
            indicators[:, i] = np.isnan(X[:, i]).astype(float)
        return indicators


# ---------------------------------------------------------------------------
# Categorical Encoder
# ---------------------------------------------------------------------------

class CategoricalEncoder:
    """Categorical feature encoding with multiple methods."""

    def __init__(self, method: EncodingMethod = EncodingMethod.TARGET, **kwargs: Any):
        self.method = method
        self.smoothing = kwargs.get("smoothing", 10.0)
        self.min_samples_leaf = kwargs.get("min_samples_leaf", 5)
        self.encoding_maps: Dict[str, EncodingMap] = {}
        self.global_mean: float = 0.0
        self._is_fitted = False

    def fit(
        self,
        X: NDArray,
        y: Optional[NDArray] = None,
        feature_names: Optional[List[str]] = None,
    ) -> "CategoricalEncoder":
        n_features = X.shape[1]
        names = feature_names or [f"feature_{i}" for i in range(n_features)]

        if self.method == EncodingMethod.TARGET and y is not None:
            self.global_mean = float(np.mean(y))

        for i, name in enumerate(names):
            col = X[:, i].astype(str)
            unique_vals = np.unique(col)

            if self.method == EncodingMethod.ONE_HOT:
                mapping = {v: j for j, v in enumerate(unique_vals)}
                self.encoding_maps[name] = EncodingMap(
                    feature_name=name, method=self.method,
                    mapping=mapping, categories=unique_vals.tolist(),
                )
            elif self.method == EncodingMethod.TARGET and y is not None:
                mapping = {}
                for val in unique_vals:
                    mask = col == val
                    n_val = np.sum(mask)
                    if n_val >= self.min_samples_leaf:
                        val_mean = float(np.mean(y[mask]))
                        smooth = 1 / (1 + np.exp(-(n_val - self.min_samples_leaf) / self.smoothing))
                        mapped = smooth * val_mean + (1 - smooth) * self.global_mean
                    else:
                        mapped = self.global_mean
                    mapping[val] = mapped
                self.encoding_maps[name] = EncodingMap(
                    feature_name=name, method=self.method,
                    mapping=mapping, categories=unique_vals.tolist(),
                )
            elif self.method == EncodingMethod.FREQUENCY:
                counts = {v: float(np.sum(col == v) / len(col)) for v in unique_vals}
                self.encoding_maps[name] = EncodingMap(
                    feature_name=name, method=self.method,
                    mapping=counts, categories=unique_vals.tolist(),
                )
            elif self.method == EncodingMethod.ORDINAL:
                mapping = {v: float(j) for j, v in enumerate(unique_vals)}
                self.encoding_maps[name] = EncodingMap(
                    feature_name=name, method=self.method,
                    mapping=mapping, categories=unique_vals.tolist(),
                )
            elif self.method == EncodingMethod.LABEL:
                mapping = {v: float(j) for j, v in enumerate(unique_vals)}
                self.encoding_maps[name] = EncodingMap(
                    feature_name=name, method=self.method,
                    mapping=mapping, categories=unique_vals.tolist(),
                )
            else:
                mapping = {v: float(j) for j, v in enumerate(unique_vals)}
                self.encoding_maps[name] = EncodingMap(
                    feature_name=name, method=self.method,
                    mapping=mapping, categories=unique_vals.tolist(),
                )

        self._is_fitted = True
        return self

    def transform(
        self, X: NDArray, feature_names: Optional[List[str]] = None
    ) -> NDArray:
        if not self._is_fitted:
            raise RuntimeError("Encoder must be fitted before transforming.")

        result = X.copy().astype(float)
        n_features = X.shape[1]
        names = feature_names or [f"feature_{i}" for i in range(n_features)]

        for i, name in enumerate(names):
            if name in self.encoding_maps:
                enc_map = self.encoding_maps[name]
                col = X[:, i].astype(str)
                encoded = np.array([enc_map.encode(v) for v in col], dtype=float)
                result[:, i] = encoded

        return result

    def fit_transform(
        self,
        X: NDArray,
        y: Optional[NDArray] = None,
        feature_names: Optional[List[str]] = None,
    ) -> NDArray:
        return self.fit(X, y, feature_names).transform(X, feature_names)


# ---------------------------------------------------------------------------
# Feature Scaler
# ---------------------------------------------------------------------------

class FeatureScaler:
    """Feature scaling with multiple methods."""

    def __init__(self, method: ScalingMethod = ScalingMethod.STANDARD, **kwargs: Any):
        self.method = method
        self.quantile_range = kwargs.get("quantile_range", (25, 75))
        self.n_quantiles = kwargs.get("n_quantiles", 1000)
        self.scaling_params: Dict[str, ScalingParams] = {}
        self._is_fitted = False

    def fit(self, X: NDArray, feature_names: Optional[List[str]] = None) -> "FeatureScaler":
        n_features = X.shape[1]
        names = feature_names or [f"feature_{i}" for i in range(n_features)]

        for i, name in enumerate(names):
            col = X[:, i]
            valid = col[~np.isnan(col)]

            if self.method == ScalingMethod.STANDARD:
                mean = float(np.mean(valid))
                std = float(np.std(valid, ddof=1))
                self.scaling_params[name] = ScalingParams(
                    feature_name=name, method=self.method,
                    mean=mean, std=std if std > 0 else 1.0,
                )
            elif self.method == ScalingMethod.MINMAX:
                min_val = float(np.min(valid))
                max_val = float(np.max(valid))
                self.scaling_params[name] = ScalingParams(
                    feature_name=name, method=self.method,
                    min_val=min_val, max_val=max_val,
                )
            elif self.method == ScalingMethod.ROBUST:
                median = float(np.median(valid))
                q1 = float(np.percentile(valid, self.quantile_range[0]))
                q3 = float(np.percentile(valid, self.quantile_range[1]))
                iqr = q3 - q1
                self.scaling_params[name] = ScalingParams(
                    feature_name=name, method=self.method,
                    median=median, iqr=iqr if iqr > 0 else 1.0,
                )
            elif self.method == ScalingMethod.QUANTILE:
                sorted_vals = np.sort(valid)
                quantiles = np.linspace(0, 1, min(self.n_quantiles, len(valid)))
                q_values = np.interp(quantiles, np.linspace(0, 1, len(sorted_vals)), sorted_vals)
                self.scaling_params[name] = ScalingParams(
                    feature_name=name, method=self.method,
                    quantiles=(quantiles, q_values),
                )
            elif self.method == ScalingMethod.MAXABS:
                max_abs = float(np.max(np.abs(valid)))
                self.scaling_params[name] = ScalingParams(
                    feature_name=name, method=self.method,
                    min_val=float(np.min(valid)), max_val=float(np.max(valid)),
                )

        self._is_fitted = True
        return self

    def transform(self, X: NDArray, feature_names: Optional[List[str]] = None) -> NDArray:
        if not self._is_fitted:
            raise RuntimeError("Scaler must be fitted before transforming.")

        result = X.copy().astype(float)
        n_features = X.shape[1]
        names = feature_names or [f"feature_{i}" for i in range(n_features)]

        for i, name in enumerate(names):
            if name in self.scaling_params:
                params = self.scaling_params[name]
                col = result[:, i]

                if self.method == ScalingMethod.STANDARD:
                    col = (col - params.mean) / params.std
                elif self.method == ScalingMethod.MINMAX:
                    rng = params.max_val - params.min_val
                    col = (col - params.min_val) / rng if rng > 0 else col * 0
                elif self.method == ScalingMethod.ROBUST:
                    col = (col - params.median) / params.iqr
                elif self.method == ScalingMethod.QUANTILE and params.quantiles:
                    q_vals, q_data = params.quantiles
                    col = np.interp(col, q_data, q_vals * 100) / 100
                elif self.method == ScalingMethod.MAXABS:
                    max_abs = max(abs(params.min_val), abs(params.max_val))
                    col = col / max_abs if max_abs > 0 else col * 0

                result[:, i] = col

        return result

    def fit_transform(self, X: NDArray, feature_names: Optional[List[str]] = None) -> NDArray:
        return self.fit(X, feature_names).transform(X, feature_names)


# ---------------------------------------------------------------------------
# Feature Constructor
# ---------------------------------------------------------------------------

class FeatureConstructor:
    """Automated feature construction from raw data."""

    def create_polynomial_features(
        self,
        X: NDArray,
        degree: int = 2,
        interaction_only: bool = False,
        include_bias: bool = False,
        feature_names: Optional[List[str]] = None,
    ) -> Tuple[NDArray, List[str]]:
        """Generate polynomial and interaction features."""
        n_samples, n_features = X.shape
        names = feature_names or [f"f{i}" for i in range(n_features)]

        if degree < 2:
            return X, names

        new_features = [X]
        new_names = list(names)

        # Interaction features
        for i in range(n_features):
            for j in range(i + 1, n_features):
                new_features.append((X[:, i] * X[:, j]).reshape(-1, 1))
                new_names.append(f"{names[i]}*{names[j]}")

        if not interaction_only and degree >= 2:
            for i in range(n_features):
                new_features.append((X[:, i] ** 2).reshape(-1, 1))
                new_names.append(f"{names[i]}^2")

        if degree >= 3:
            for i in range(n_features):
                for j in range(i + 1, n_features):
                    for k in range(j + 1, n_features):
                        new_features.append((X[:, i] * X[:, j] * X[:, k]).reshape(-1, 1))
                        new_names.append(f"{names[i]}*{names[j]}*{names[k]}")

        if include_bias:
            new_features.append(np.ones((n_samples, 1)))
            new_names.append("bias")

        return np.hstack(new_features), new_names

    def create_lag_features(
        self,
        data: NDArray,
        column_idx: int = 0,
        lags: List[int] = None,
    ) -> Tuple[NDArray, List[str]]:
        """Create lag features for time series."""
        if lags is None:
            lags = [1, 7, 14, 28]

        n_samples = data.shape[0]
        lag_features = np.zeros((n_samples, len(lags)))
        new_names = []

        for i, lag in enumerate(lags):
            lag_features[lag:, i] = data[:n_samples - lag, column_idx]
            new_names.append(f"lag_{lag}")

        return lag_features, new_names

    def create_rolling_features(
        self,
        data: NDArray,
        column_idx: int = 0,
        windows: List[int] = None,
        functions: List[str] = None,
    ) -> Tuple[NDArray, List[str]]:
        """Create rolling window statistics."""
        if windows is None:
            windows = [7, 14, 30]
        if functions is None:
            functions = ["mean", "std", "min", "max"]

        n_samples = data.shape[0]
        n_features = len(windows) * len(functions)
        features = np.zeros((n_samples, n_features))
        names = []
        col_idx = 0

        for window in windows:
            for func in functions:
                for i in range(window, n_samples):
                    window_data = data[i - window:i, column_idx]
                    if func == "mean":
                        features[i, col_idx] = np.mean(window_data)
                    elif func == "std":
                        features[i, col_idx] = np.std(window_data, ddof=1)
                    elif func == "min":
                        features[i, col_idx] = np.min(window_data)
                    elif func == "max":
                        features[i, col_idx] = np.max(window_data)
                    elif func == "skew":
                        m = np.mean(window_data)
                        s = np.std(window_data, ddof=1)
                        features[i, col_idx] = float(np.mean(((window_data - m) / s) ** 3)) if s > 0 else 0
                names.append(f"rolling_{window}_{func}")
                col_idx += 1

        return features, names

    def create_interactions(
        self,
        X: NDArray,
        column_indices: Optional[List[int]] = None,
        operations: List[str] = None,
    ) -> Tuple[NDArray, List[str]]:
        """Create interaction features between specified columns."""
        if column_indices is None:
            column_indices = list(range(min(5, X.shape[1])))
        if operations is None:
            operations = ["multiply", "divide", "add", "subtract"]

        features = []
        names = []

        for i, idx_a in enumerate(column_indices):
            for idx_b in column_indices[i + 1:]:
                a = X[:, idx_a]
                b = X[:, idx_b]

                if "multiply" in operations:
                    features.append((a * b).reshape(-1, 1))
                    names.append(f"f{idx_a}*f{idx_b}")
                if "divide" in operations:
                    denom = np.where(np.abs(b) > 1e-10, b, 1.0)
                    features.append((a / denom).reshape(-1, 1))
                    names.append(f"f{idx_a}/f{idx_b}")
                if "add" in operations:
                    features.append((a + b).reshape(-1, 1))
                    names.append(f"f{idx_a}+f{idx_b}")
                if "subtract" in operations:
                    features.append((a - b).reshape(-1, 1))
                    names.append(f"f{idx_a}-f{idx_b}")

        if features:
            return np.hstack(features), names
        return np.zeros((X.shape[0], 0)), []

    def create_date_features(
        self,
        timestamps: NDArray,
        features: Optional[List[str]] = None,
    ) -> Tuple[NDArray, List[str]]:
        """Decompose timestamps into calendar features."""
        if features is None:
            features = ["month", "day", "dayofweek", "hour", "is_weekend", "quarter"]

        timestamps = timestamps.astype("datetime64[ns]")
        n_samples = len(timestamps)
        date_features = []
        names = []

        if "year" in features:
            date_features.append(np.array([t.year for t in timestamps]).reshape(-1, 1))
            names.append("year")
        if "month" in features:
            months = np.array([t.month for t in timestamps]).reshape(-1, 1)
            date_features.append(months)
            names.append("month")
        if "day" in features:
            date_features.append(np.array([t.day for t in timestamps]).reshape(-1, 1))
            names.append("day")
        if "dayofweek" in features:
            dow = np.array([t.weekday() for t in timestamps]).reshape(-1, 1)
            date_features.append(dow)
            names.append("dayofweek")
        if "hour" in features:
            date_features.append(np.array([t.hour for t in timestamps]).reshape(-1, 1))
            names.append("hour")
        if "is_weekend" in features:
            is_weekend = np.array([1 if t.weekday() >= 5 else 0 for t in timestamps]).reshape(-1, 1)
            date_features.append(is_weekend)
            names.append("is_weekend")
        if "quarter" in features:
            quarters = np.array([(t.month - 1) // 3 + 1 for t in timestamps]).reshape(-1, 1)
            date_features.append(quarters)
            names.append("quarter")

        # Cyclical encoding
        if "month" in features:
            month_sin = np.sin(2 * np.pi * np.array([t.month for t in timestamps]) / 12).reshape(-1, 1)
            month_cos = np.cos(2 * np.pi * np.array([t.month for t in timestamps]) / 12).reshape(-1, 1)
            date_features.extend([month_sin, month_cos])
            names.extend(["month_sin", "month_cos"])

        if date_features:
            return np.hstack(date_features), names
        return np.zeros((n_samples, 0)), []


# ---------------------------------------------------------------------------
# Feature Selector
# ---------------------------------------------------------------------------

class FeatureSelector:
    """Feature selection with multiple methods."""

    def __init__(self, random_state: Optional[int] = None):
        self.rng = np.random.default_rng(random_state)
        self._scores: Dict[str, float] = {}
        self._selected: List[str] = []

    def variance_threshold(
        self, X: NDArray, threshold: float = 0.01,
        feature_names: Optional[List[str]] = None,
    ) -> SelectionResult:
        """Remove low-variance features."""
        n_features = X.shape[1]
        names = feature_names or [f"feature_{i}" for i in range(n_features)]

        variances = np.var(X, axis=0)
        scores = {names[i]: float(variances[i]) for i in range(n_features)}
        selected = [names[i] for i in range(n_features) if variances[i] >= threshold]
        removed = [names[i] for i in range(n_features) if variances[i] < threshold]

        return SelectionResult(
            selected_features=selected,
            removed_features=removed,
            scores=scores,
            method=SelectionMethod.VARIANCE,
            threshold=threshold,
        )

    def correlation_filter(
        self, X: NDArray, threshold: float = 0.95,
        feature_names: Optional[List[str]] = None,
    ) -> SelectionResult:
        """Remove highly correlated features."""
        n_features = X.shape[1]
        names = feature_names or [f"feature_{i}" for i in range(n_features)]

        corr_matrix = np.corrcoef(X, rowvar=False)
        scores = {}
        removed = set()
        selected = list(range(n_features))

        for i in range(n_features):
            for j in range(i + 1, n_features):
                if abs(corr_matrix[i, j]) > threshold:
                    removed.add(j)
                    scores[names[j]] = float(abs(corr_matrix[i, j]))

        selected_names = [names[i] for i in selected if i not in removed]
        removed_names = [names[i] for i in removed]

        return SelectionResult(
            selected_features=selected_names,
            removed_features=removed_names,
            scores=scores,
            method=SelectionMethod.CORRELATION,
            threshold=threshold,
        )

    def mutual_information(
        self,
        X: NDArray,
        y: NDArray,
        k: int = 20,
        feature_names: Optional[List[str]] = None,
        task: str = "classification",
    ) -> SelectionResult:
        """Select top-k features by mutual information."""
        n_features = X.shape[1]
        names = feature_names or [f"feature_{i}" for i in range(n_features)]

        # Simplified MI estimation using binning
        scores = {}
        for i in range(n_features):
            col = X[:, i]
            # Bin continuous features
            n_bins = min(10, len(np.unique(col)))
            if n_bins < 2:
                scores[names[i]] = 0.0
                continue

            bin_edges = np.percentile(col[~np.isnan(col)], np.linspace(0, 100, n_bins + 1))
            bin_indices = np.digitize(col, bin_edges[1:-1])

            # Compute MI
            mi = self._compute_mutual_information(bin_indices, y)
            scores[names[i]] = mi

        # Select top k
        sorted_features = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        selected = [name for name, _ in sorted_features[:k]]
        removed = [name for name, _ in sorted_features[k:]]

        return SelectionResult(
            selected_features=selected,
            removed_features=removed,
            scores=scores,
            method=SelectionMethod.MUTUAL_INFO,
            k=k,
        )

    def stability_selection(
        self,
        X: NDArray,
        y: NDArray,
        n_bootstrap: int = 100,
        threshold: float = 0.7,
        feature_names: Optional[List[str]] = None,
        task: str = "classification",
    ) -> SelectionResult:
        """Stability selection via bootstrap sampling."""
        n_features = X.shape[1]
        n_samples = X.shape[0]
        names = feature_names or [f"feature_{i}" for i in range(n_features)]

        selection_frequency = np.zeros(n_features)

        for _ in range(n_bootstrap):
            # Bootstrap sample
            boot_idx = self.rng.choice(n_samples, n_samples, replace=True)
            X_boot = X[boot_idx]
            y_boot = y[boot_idx]

            # Simple L1-like selection (correlation-based)
            scores = np.abs(np.array([
                np.corrcoef(X_boot[:, i], y_boot)[0, 1]
                for i in range(n_features)
            ]))

            # Select top 50%
            k = max(1, n_features // 2)
            top_idx = np.argsort(scores)[-k:]
            selection_frequency[top_idx] += 1

        selection_frequency /= n_bootstrap
        scores = {names[i]: float(selection_frequency[i]) for i in range(n_features)}
        selected = [names[i] for i in range(n_features) if selection_frequency[i] >= threshold]
        removed = [names[i] for i in range(n_features) if selection_frequency[i] < threshold]

        return SelectionResult(
            selected_features=selected,
            removed_features=removed,
            scores=scores,
            method=SelectionMethod.STABILITY,
            threshold=threshold,
        )

    def auto_select(
        self,
        X: NDArray,
        y: NDArray,
        methods: Optional[List[str]] = None,
        k: int = 15,
        feature_names: Optional[List[str]] = None,
        task: str = "classification",
    ) -> SelectionResult:
        """Automated feature selection combining multiple methods."""
        if methods is None:
            methods = ["variance", "correlation", "mutual_info"]

        names = feature_names or [f"feature_{i}" for i in range(X.shape[1])]
        remaining_features = set(names)

        for method in methods:
            if method == "variance":
                result = self.variance_threshold(X, threshold=0.01, feature_names=names)
            elif method == "correlation":
                result = self.correlation_filter(X, threshold=0.95, feature_names=names)
            elif method == "mutual_info":
                result = self.mutual_information(X, y, k=k, feature_names=names, task=task)
            elif method == "stability":
                result = self.stability_selection(X, y, feature_names=names, task=task)
            else:
                continue

            remaining_features &= set(result.selected_features)

        # Final ranking by mutual information
        final_result = self.mutual_information(
            X, y, k=min(k, len(remaining_features)),
            feature_names=[n for n in names if n in remaining_features],
            task=task,
        )

        return final_result

    def _compute_mutual_information(self, x: NDArray, y: NDArray) -> float:
        """Compute mutual information between discrete variables."""
        n = len(x)
        unique_x = np.unique(x)
        unique_y = np.unique(y)

        mi = 0.0
        for xi in unique_x:
            px = np.sum(x == xi) / n
            for yi in unique_y:
                pxy = np.sum((x == xi) & (y == yi)) / n
                py = np.sum(y == yi) / n
                if pxy > 0 and px > 0 and py > 0:
                    mi += pxy * np.log2(pxy / (px * py))

        return float(mi)


# ---------------------------------------------------------------------------
# Feature Pipeline
# ---------------------------------------------------------------------------

class FeaturePipeline:
    """Orchestrate multiple feature engineering steps."""

    def __init__(self, name: str = "pipeline"):
        self.name = name
        self.steps: List[PipelineStep] = []
        self._fitted_transformers: Dict[str, Any] = {}
        self._is_fitted = False

    def add_step(self, step: PipelineStep) -> "FeaturePipeline":
        self.steps.append(step)
        return self

    def fit(
        self, X: NDArray, y: Optional[NDArray] = None,
        feature_names: Optional[List[str]] = None,
    ) -> "FeaturePipeline":
        current_X = X.copy()
        current_names = list(feature_names) if feature_names else [f"f{i}" for i in range(X.shape[1])]

        for step in self.steps:
            if not step.enabled:
                continue

            if step.transformer in ("mean_imputer", "median_imputer", "knn_imputer", "iterative_imputer"):
                method_map = {
                    "mean_imputer": ImputationMethod.MEAN,
                    "median_imputer": ImputationMethod.MEDIAN,
                    "knn_imputer": ImputationMethod.KNN,
                    "iterative_imputer": ImputationMethod.ITERATIVE,
                }
                imputer = Imputer(method=method_map[step.transformer], **step.params)
                imputer.fit(current_X, current_names)
                self._fitted_transformers[step.name] = imputer

            elif step.transformer in ("target_encoder", "one_hot_encoder", "frequency_encoder", "label_encoder"):
                method_map = {
                    "target_encoder": EncodingMethod.TARGET,
                    "one_hot_encoder": EncodingMethod.ONE_HOT,
                    "frequency_encoder": EncodingMethod.FREQUENCY,
                    "label_encoder": EncodingMethod.LABEL,
                }
                encoder = CategoricalEncoder(method=method_map[step.transformer], **step.params)
                encoder.fit(current_X, y, current_names)
                self._fitted_transformers[step.name] = encoder

            elif step.transformer in ("standard_scaler", "minmax_scaler", "robust_scaler", "quantile_scaler"):
                method_map = {
                    "standard_scaler": ScalingMethod.STANDARD,
                    "minmax_scaler": ScalingMethod.MINMAX,
                    "robust_scaler": ScalingMethod.ROBUST,
                    "quantile_scaler": ScalingMethod.QUANTILE,
                }
                scaler = FeatureScaler(method=method_map[step.transformer], **step.params)
                scaler.fit(current_X, current_names)
                self._fitted_transformers[step.name] = scaler

            elif step.transformer == "polynomial_features":
                constructor = FeatureConstructor()
                current_X, current_names = constructor.create_polynomial_features(
                    current_X, feature_names=current_names, **step.params
                )
                self._fitted_transformers[step.name] = ("polynomial", current_names)

            elif step.transformer == "mutual_information_selector":
                selector = FeatureSelector()
                result = selector.mutual_information(
                    current_X, y, feature_names=current_names, **step.params
                )
                self._fitted_transformers[step.name] = result
                # Filter columns
                selected_idx = [current_names.index(f) for f in result.selected_features if f in current_names]
                current_X = current_X[:, selected_idx]
                current_names = [current_names[i] for i in selected_idx]

            elif step.transformer == "variance_threshold":
                selector = FeatureSelector()
                result = selector.variance_threshold(current_X, feature_names=current_names, **step.params)
                self._fitted_transformers[step.name] = result
                selected_idx = [current_names.index(f) for f in result.selected_features if f in current_names]
                current_X = current_X[:, selected_idx]
                current_names = [current_names[i] for i in selected_idx]

        self._is_fitted = True
        return self

    def transform(self, X: NDArray, feature_names: Optional[List[str]] = None) -> NDArray:
        if not self._is_fitted:
            raise RuntimeError("Pipeline must be fitted before transforming.")

        current_X = X.copy()
        current_names = list(feature_names) if feature_names else [f"f{i}" for i in range(X.shape[1])]

        for step in self.steps:
            if not step.enabled or step.name not in self._fitted_transformers:
                continue

            transformer = self._fitted_transformers[step.name]

            if isinstance(transformer, Imputer):
                current_X = transformer.transform(current_X, current_names)
            elif isinstance(transformer, CategoricalEncoder):
                current_X = transformer.transform(current_X, current_names)
            elif isinstance(transformer, FeatureScaler):
                current_X = transformer.transform(current_X, current_names)
            elif isinstance(transformer, tuple) and transformer[0] == "polynomial":
                constructor = FeatureConstructor()
                current_X, current_names = constructor.create_polynomial_features(
                    current_X, feature_names=current_names
                )
            elif isinstance(transformer, SelectionResult):
                selected_idx = [current_names.index(f) for f in transformer.selected_features if f in current_names]
                current_X = current_X[:, selected_idx]
                current_names = [current_names[i] for i in selected_idx]

        return current_X

    def fit_transform(
        self, X: NDArray, y: Optional[NDArray] = None,
        feature_names: Optional[List[str]] = None,
    ) -> NDArray:
        return self.fit(X, y, feature_names).transform(X, feature_names)

    def summary(self) -> Dict[str, Any]:
        steps_info = []
        for step in self.steps:
            steps_info.append({
                "name": step.name,
                "transformer": step.transformer,
                "type": step.step_type.value,
                "enabled": step.enabled,
                "fitted": step.name in self._fitted_transformers,
            })
        return {
            "pipeline_name": self.name,
            "n_steps": len(self.steps),
            "fitted": self._is_fitted,
            "steps": steps_info,
        }

    def get_encoding_maps(self) -> Dict[str, EncodingMap]:
        maps = {}
        for name, transformer in self._fitted_transformers.items():
            if isinstance(transformer, CategoricalEncoder):
                maps.update(transformer.encoding_maps)
        return maps

    def get_scaling_params(self) -> Dict[str, ScalingParams]:
        params = {}
        for name, transformer in self._fitted_transformers.items():
            if isinstance(transformer, FeatureScaler):
                params.update(transformer.scaling_params)
        return params


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate feature engineering capabilities."""
    print("=" * 70)
    print("Feature Engineering Toolkit - Demo")
    print("=" * 70)

    rng = np.random.default_rng(42)

    # Generate synthetic data
    n_samples, n_features = 500, 8
    X = rng.standard_normal((n_samples, n_features))
    # Add some missing values
    missing_mask = rng.random((n_samples, n_features)) < 0.05
    X_with_missing = X.copy()
    X_with_missing[missing_mask] = np.nan

    feature_names = ["age", "income", "tenure", "monthly_charges", "total_charges",
                     "num_support_calls", "contract_length", "satisfaction_score"]
    y = (X[:, 0] * 0.5 + X[:, 1] * 0.3 + rng.standard_normal(n_samples) * 0.5 > 0).astype(float)

    # --- 1. Imputation ---
    print("\n--- Missing Value Imputation ---")
    imputer = Imputer(method=ImputationMethod.MEAN)
    X_imputed = imputer.fit_transform(X_with_missing, feature_names)
    missing_before = np.sum(np.isnan(X_with_missing))
    missing_after = np.sum(np.isnan(X_imputed))
    print(f"  Missing values before: {missing_before}")
    print(f"  Missing values after:  {missing_after}")
    print(f"  Fill values: {dict(list(imputer.fill_values.items())[:3])}...")

    # --- 2. Encoding ---
    print("\n--- Categorical Encoding ---")
    categories = rng.choice(["Basic", "Premium", "Enterprise", "Starter"], n_samples)
    X_cat = np.column_stack([X_imputed[:, :3], categories.reshape(-1, 1)])
    cat_names = ["age", "income", "tenure", "plan"]

    encoder = CategoricalEncoder(method=EncodingMethod.TARGET, smoothing=5.0)
    X_encoded = encoder.fit_transform(X_cat, y, cat_names)
    print(f"  Encoding maps: {list(encoder.encoding_maps.keys())}")
    plan_map = encoder.encoding_maps["plan"]
    print(f"  Plan encoding: {plan_map.mapping}")

    # --- 3. Scaling ---
    print("\n--- Feature Scaling ---")
    scaler = FeatureScaler(method=ScalingMethod.ROBUST)
    X_scaled = scaler.fit_transform(X_imputed, feature_names)
    print(f"  Scaler params for 'age': mean={scaler.scaling_params['age'].median:.2f}, iqr={scaler.scaling_params['age'].iqr:.2f}")

    # --- 4. Feature Construction ---
    print("\n--- Feature Construction ---")
    constructor = FeatureConstructor()

    # Lag features
    lag_feats, lag_names = constructor.create_lag_features(X_scaled, column_idx=0, lags=[1, 5, 10])
    print(f"  Lag features: {lag_names}")

    # Rolling features
    rolling_feats, rolling_names = constructor.create_rolling_features(
        X_scaled, column_idx=1, windows=[5, 10], functions=["mean", "std"]
    )
    print(f"  Rolling features: {rolling_names}")

    # Interactions
    inter_feats, inter_names = constructor.create_interactions(
        X_scaled, column_indices=[0, 1, 2], operations=["multiply", "divide"]
    )
    print(f"  Interaction features: {inter_names}")

    # --- 5. Feature Selection ---
    print("\n--- Feature Selection ---")
    selector = FeatureSelector(random_state=42)

    var_result = selector.variance_threshold(X_scaled, threshold=0.01, feature_names=feature_names)
    print(f"  Variance threshold: removed {len(var_result.removed_features)} features")

    corr_result = selector.correlation_filter(X_scaled, threshold=0.8, feature_names=feature_names)
    print(f"  Correlation filter: removed {len(corr_result.removed_features)} features")

    mi_result = selector.mutual_information(X_scaled, y, k=5, feature_names=feature_names)
    print(f"  Mutual info top 5: {mi_result.selected_features}")

    stability_result = selector.stability_selection(X_scaled, y, feature_names=feature_names)
    print(f"  Stability selection: {len(stability_result.selected_features)} stable features")

    # --- 6. Pipeline ---
    print("\n--- Feature Pipeline ---")
    pipeline = FeaturePipeline(name="churn_pipeline")
    pipeline.add_step(PipelineStep(
        name="impute", transformer="mean_imputer",
    ))
    pipeline.add_step(PipelineStep(
        name="scale", transformer="robust_scaler",
    ))
    pipeline.add_step(PipelineStep(
        name="select", transformer="variance_threshold",
        params={"threshold": 0.01},
    ))

    X_transformed = pipeline.fit_transform(X_with_missing, y, feature_names)
    print(f"  Features before: {X_with_missing.shape[1]}")
    print(f"  Features after:  {X_transformed.shape[1]}")
    print(f"  Pipeline summary: {json.dumps(pipeline.summary(), indent=2)}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()