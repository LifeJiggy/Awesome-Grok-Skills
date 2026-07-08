"""
Data Science Agent — Statistical Analysis, ML Model Development,
Feature Engineering, Experiment Design, Visualization, and Reproducibility.
Zero external dependencies. Full type hints and dataclass models.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import os
import random
import statistics
import time
import uuid
from copy import deepcopy
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

logger = logging.getLogger("data_science_agent")
logger.setLevel(logging.DEBUG)
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s %(name)s — %(message)s", datefmt="%Y-%m-%dT%H:%M:%S"))
logger.addHandler(_handler)
# ── Enums ──────────────────────────────────────────────────────────────
class DataType(Enum):
    NUMERICAL = "numerical"; CATEGORICAL = "categorical"; TEMPORAL = "temporal"
    TEXT = "text"; BINARY = "binary"
class TaskType(Enum):
    CLASSIFICATION = "classification"; REGRESSION = "regression"
    CLUSTERING = "clustering"; DIMENSIONALITY_REDUCTION = "dimensionality_reduction"
    TIME_SERIES = "time_series"
class ImputationStrategy(Enum):
    MEAN = "mean"; MEDIAN = "median"; MODE = "mode"; CONSTANT = "constant"
    DROP = "drop"; FORWARD_FILL = "ffill"; BACKWARD_FILL = "bfill"; KNN = "knn"
class NormalizationMethod(Enum):
    MINMAX = "minmax"; ZSCORE = "zscore"; ROBUST = "robust"
    MAXABS = "maxabs"; L1 = "l1"; L2 = "l2"
class EncodingMethod(Enum):
    ONEHOT = "onehot"; LABEL = "label"; ORDINAL = "ordinal"
    TARGET = "target"; FREQUENCY = "frequency"; BINARY = "binary"
class SplitStrategy(Enum):
    RANDOM = "random"; STRATIFIED = "stratified"; TEMPORAL = "temporal"
    KFOLD = "kfold"; STRATIFIED_KFOLD = "stratified_kfold"
class ExperimentStatus(Enum):
    DRAFT = "draft"; RUNNING = "running"; COMPLETED = "completed"
    FAILED = "failed"; CANCELLED = "cancelled"
class VisType(Enum):
    HISTOGRAM = "histogram"; SCATTER = "scatter"; BAR = "bar"; LINE = "line"
    BOX = "box"; HEATMAP = "heatmap"; PAIR = "pair"; VIOLIN = "violin"
# ── Dataclasses ────────────────────────────────────────────────────────

@dataclass
class DataProfile:
    column_name: str; data_type: DataType; count: int
    missing_values: int; unique_values: int
    statistics: Dict[str, Any] = field(default_factory=dict)
    quality_score: float = 0.0

@dataclass
class FeatureImportance:
    feature_name: str; importance_score: float; rank: int; method: str

@dataclass
class ModelResult:
    model_name: str; task_type: TaskType; metrics: Dict[str, float]
    parameters: Dict[str, Any]; feature_importances: List[FeatureImportance]
    training_time_seconds: float; model_hash: str; fitted: bool = False

@dataclass
class ExperimentConfig:
    experiment_id: str; name: str; description: str; task_type: TaskType
    target_column: str; feature_columns: List[str]
    hyperparameters: Dict[str, Any]; split_strategy: SplitStrategy
    test_size: float = 0.2; random_state: int = 42
    created_at: str = ""; status: ExperimentStatus = ExperimentStatus.DRAFT

@dataclass
class ExperimentResult:
    experiment_id: str; model_result: ModelResult
    predictions: List[Any]; actuals: List[Any]
    cross_val_scores: List[float]
    confusion_matrix: Optional[List[List[int]]] = None
    completed_at: str = ""

@dataclass
class VisualizationSpec:
    vis_type: VisType; title: str; x_column: str
    y_column: Optional[str] = None; hue_column: Optional[str] = None
    bins: int = 30; figsize: Tuple[int, int] = (10, 6)
    output_path: Optional[str] = None

@dataclass
class PipelineStep:
    step_id: str; name: str; function_name: str
    parameters: Dict[str, Any]
    depends_on: List[str] = field(default_factory=list)
@dataclass
class ReproducibilityRecord:
    record_id: str; pipeline_hash: str; data_hash: str
    random_seeds: Dict[str, int]; environment: Dict[str, str]; timestamp: str
# ── StatisticalAnalyzer ───────────────────────────────────────────────
class StatisticalAnalyzer:
    """Comprehensive statistical analysis toolkit."""
    def __init__(self) -> None:
        self._cache: Dict[str, Any] = {}
    def describe(self, values: Sequence[float]) -> Dict[str, float]:
        if not values:
            raise ValueError("Cannot describe an empty sequence")
        s = sorted(values); n = len(s)
        mean = sum(s) / n
        var = sum((v - mean) ** 2 for v in s) / n
        std = math.sqrt(var)
        return {
            "count": n, "mean": mean, "median": self.median(s), "std": std,
            "variance": var, "min": s[0], "max": s[-1], "range": s[-1] - s[0],
            "q1": self.percentile(s, 25), "q3": self.percentile(s, 75),
            "iqr": self.percentile(s, 75) - self.percentile(s, 25),
            "skewness": self._skewness(s, mean, std),
            "kurtosis": self._kurtosis(s, mean, std),
            "sem": std / math.sqrt(n),
            "cv": (std / mean) if mean != 0 else float("inf"),
        }
    @staticmethod
    def median(sv: List[float]) -> float:
        n = len(sv); m = n // 2
        return (sv[m - 1] + sv[m]) / 2 if n % 2 == 0 else sv[m]
    @staticmethod
    def percentile(sv: List[float], p: float) -> float:
        if not sv:
            raise ValueError("Empty list")
        k = (p / 100) * (len(sv) - 1); f = math.floor(k); c = math.ceil(k)
        return sv[int(k)] if f == c else sv[f] * (c - k) + sv[c] * (k - f)
    @staticmethod
    def _skewness(vals: List[float], mean: float, std: float) -> float:
        n = len(vals)
        if std == 0 or n < 3:
            return 0.0
        return sum((v - mean) ** 3 for v in vals) / n / (std ** 3)
    @staticmethod
    def _kurtosis(vals: List[float], mean: float, std: float) -> float:
        n = len(vals)
        if std == 0 or n < 4:
            return 0.0
        return sum((v - mean) ** 4 for v in vals) / n / (std ** 4) - 3.0
    def t_test(self, sample_a: Sequence[float], sample_b: Sequence[float],
               alpha: float = 0.05) -> Dict[str, Any]:
        a, b = list(sample_a), list(sample_b)
        if len(a) < 2 or len(b) < 2:
            raise ValueError("Each sample needs >= 2 observations")
        ma, mb = sum(a) / len(a), sum(b) / len(b)
        va = sum((x - ma) ** 2 for x in a) / (len(a) - 1)
        vb = sum((x - mb) ** 2 for x in b) / (len(b) - 1)
        se = math.sqrt(va / len(a) + vb / len(b))
        if se == 0:
            return {"t_statistic": 0.0, "p_value": 1.0, "significant": False}
        t = (ma - mb) / se; df = len(a) + len(b) - 2
        p = self._approx_t_p(abs(t), df)
        return {"t_statistic": t, "p_value": p, "significant": p < alpha,
                "mean_a": ma, "mean_b": mb, "degrees_of_freedom": df}
    @staticmethod
    def _approx_t_p(t: float, df: int) -> float:
        x = df / (df + t * t)
        if x >= 1.0:
            return 1.0
        a, b = df / 2.0, 0.5
        bv = math.gamma(a) * math.gamma(b) / math.gamma(a + b)
        return min(max(((1.0 - x) ** a) / (a * bv) if a * bv else 1.0, 0.0), 1.0)
    def chi_square_test(self, observed: List[int], expected: List[int],
                        alpha: float = 0.05) -> Dict[str, Any]:
        if len(observed) != len(expected):
            raise ValueError("Observed and expected must have same length")
        if any(e == 0 for e in expected):
            raise ValueError("Expected frequencies must not be zero")
        chi2 = sum((o - e) ** 2 / e for o, e in zip(observed, expected))
        df = len(observed) - 1; p = self._chi2_p(chi2, df)
        return {"chi2": chi2, "df": df, "p_value": p, "significant": p < alpha}
    @staticmethod
    def _chi2_p(chi2: float, df: int) -> float:
        if chi2 <= 0:
            return 1.0
        k, x = df / 2.0, chi2 / 2.0
        if x == 0:
            return 1.0
        term = math.exp(-x + k * math.log(x) - math.lgamma(k))
        total = term / x
        for i in range(1, max(int(k) + 10, 30)):
            term *= x / (k + i); total += term / x
            if term < 1e-12:
                break
        return min(total, 1.0)
    def correlation_matrix(self, data: List[Dict[str, float]],
                           columns: Optional[List[str]] = None) -> Dict[str, Dict[str, float]]:
        if not data:
            raise ValueError("Empty data")
        cols = columns or [k for k, v in data[0].items() if isinstance(v, (int, float))]
        return {c1: {c2: self._pearson(
            [float(r.get(c1, 0)) for r in data],
            [float(r.get(c2, 0)) for r in data]
        ) for c2 in cols} for c1 in cols}
    @staticmethod
    def _pearson(x: List[float], y: List[float]) -> float:
        n = len(x)
        if n == 0:
            return 0.0
        mx, my = sum(x) / n, sum(y) / n
        num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
        dx = math.sqrt(sum((xi - mx) ** 2 for xi in x))
        dy = math.sqrt(sum((yi - my) ** 2 for yi in y))
        return num / (dx * dy) if dx and dy else 0.0
    def detect_outliers(self, values: Sequence[float], method: str = "iqr",
                        threshold: float = 1.5) -> List[int]:
        vals = list(values)
        if method == "iqr":
            s = sorted(vals); q1 = self.percentile(s, 25); q3 = self.percentile(s, 75)
            iqr = q3 - q1; lo, hi = q1 - threshold * iqr, q3 + threshold * iqr
            return [i for i, v in enumerate(vals) if v < lo or v > hi]
        elif method == "zscore":
            mu = sum(vals) / len(vals)
            std = math.sqrt(sum((v - mu) ** 2 for v in vals) / len(vals))
            return [] if std == 0 else [i for i, v in enumerate(vals) if abs((v - mu) / std) > threshold]
        raise ValueError(f"Unknown outlier method: {method}")
    def normality_test(self, values: Sequence[float], alpha: float = 0.05) -> Dict[str, Any]:
        vals = list(values); n = len(vals)
        if n < 3:
            raise ValueError("Need at least 3 observations")
        mean = sum(vals) / n
        std = math.sqrt(sum((v - mean) ** 2 for v in vals) / n)
        if std == 0:
            return {"normal": False, "reason": "zero variance"}
        s = sorted(vals)
        w_num = sum((s[-1 - i] - s[i]) ** 2 for i in range(n // 2))
        w_den = sum((v - mean) ** 2 for v in s)
        w = w_num / w_den if w_den != 0 else 0
        return {"w_statistic": w, "normal": w > (0.7 + 0.05 * math.log(n)), "n": n}
# ── MLModelBuilder ────────────────────────────────────────────────────
class MLModelBuilder:
    """Train, evaluate, and compare ML models without external dependencies."""
    def __init__(self, task_type: TaskType = TaskType.CLASSIFICATION) -> None:
        self.task_type = task_type
        self._models: Dict[str, Any] = {}
        self._best: Optional[ModelResult] = None
    class _DecisionStump:
        def __init__(self) -> None:
            self.feature_idx: int = 0; self.threshold: float = 0.0
            self.left_value: Any = 0; self.right_value: Any = 0
        def fit(self, X: List[List[float]], y: List[float]) -> None:
            best_gini = float("inf")
            for f in range(len(X[0]) if X else 0):
                for t in sorted(set(row[f] for row in X)):
                    ly = [y[i] for i in range(len(y)) if X[i][f] <= t]
                    ry = [y[i] for i in range(len(y)) if X[i][f] > t]
                    if not ly or not ry:
                        continue
                    gini = (self._gini(ly) * len(ly) + self._gini(ry) * len(ry)) / len(y)
                    if gini < best_gini:
                        best_gini = gini; self.feature_idx = f; self.threshold = t
                        self.left_value = statistics.mode(ly); self.right_value = statistics.mode(ry)
        def predict(self, x: List[float]) -> Any:
            return self.left_value if x[self.feature_idx] <= self.threshold else self.right_value

        @staticmethod
        def _gini(labels: List[float]) -> float:
            if not labels:
                return 0.0
            counts: Dict[float, int] = {}
            for l in labels:
                counts[l] = counts.get(l, 0) + 1
            n = len(labels)
            return 1.0 - sum((c / n) ** 2 for c in counts.values())
    class _SimpleLinearModel:
        def __init__(self) -> None:
            self.coefficients: List[float] = []; self.intercept: float = 0.0
        def fit(self, X: List[List[float]], y: List[float]) -> None:
            n, p = len(X), len(X[0]) if X else 0
            if n == 0:
                return
            XtX = [[0.0] * p for _ in range(p)]
            Xty = [0.0] * p
            for i in range(n):
                for j in range(p):
                    Xty[j] += X[i][j] * y[i]
                    for k in range(p):
                        XtX[j][k] += X[i][j] * X[i][k]
            for j in range(p):
                XtX[j][j] += 1e-4  # ridge
            self.coefficients = MLModelBuilder._SimpleLinearModel._solve(XtX, Xty)
            ym = sum(y) / n; xm = [sum(X[i][j] for i in range(n)) / n for j in range(p)]
            self.intercept = ym - sum(self.coefficients[j] * xm[j] for j in range(p))
        def predict(self, X: List[List[float]]) -> List[float]:
            return [self.intercept + sum(self.coefficients[j] * row[j] for j in range(len(row))) for row in X]
        @staticmethod
        def _solve(A: List[List[float]], b: List[float]) -> List[float]:
            n = len(b)
            M = [row[:] + [b[i]] for i, row in enumerate(A)]
            for col in range(n):
                mr = max(range(col, n), key=lambda r: abs(M[r][col]))
                M[col], M[mr] = M[mr], M[col]
                if abs(M[col][col]) < 1e-12:
                    continue
                for row in range(col + 1, n):
                    f = M[row][col] / M[col][col]
                    for j in range(col, n + 1):
                        M[row][j] -= f * M[col][j]
            x = [0.0] * n
            for i in range(n - 1, -1, -1):
                x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
            return x
    def train(self, X: List[List[float]], y: List[float], model_type: str = "stump",
              **kwargs: Any) -> ModelResult:
        start = time.time()
        if model_type == "stump":
            model = self._DecisionStump(); model.fit(X, y)
        elif model_type == "linear":
            model = self._SimpleLinearModel(); model.fit(X, y)
        else:
            raise ValueError(f"Unsupported model_type: {model_type}")
        mid = f"{model_type}_{uuid.uuid4().hex[:8]}"
        self._models[mid] = model; elapsed = time.time() - start
        preds = model.predict(X)
        if self.task_type == TaskType.CLASSIFICATION:
            metrics = {"accuracy": sum(1 for p, a in zip(preds, y) if p == a) / len(y) if y else 0}
        else:
            mse = sum((p - a) ** 2 for p, a in zip(preds, y)) / len(y) if y else 0
            my = sum(y) / len(y) if y else 0
            sst = sum((a - my) ** 2 for a in y) if y else 1
            metrics = {"mse": mse, "rmse": math.sqrt(mse), "r2": 1 - mse * len(y) / sst if sst else 0}
        result = ModelResult(model_name=mid, task_type=self.task_type, metrics=metrics,
                             parameters={"model_type": model_type, **kwargs},
                             feature_importances=[], training_time_seconds=elapsed,
                             model_hash=hashlib.md5(str(time.time()).encode()).hexdigest()[:12], fitted=True)
        self._best = result
        logger.info("Trained %s — metrics: %s", mid, metrics)
        return result
    def predict(self, model_id: str, X: List[List[float]]) -> List[Any]:
        model = self._models.get(model_id)
        if model is None:
            raise KeyError(f"Model {model_id} not found")
        return model.predict(X)
    def cross_validate(self, X: List[List[float]], y: List[float], k: int = 5,
                       model_type: str = "stump") -> Dict[str, Any]:
        n = len(X); fs = max(1, n // k); scores: List[float] = []
        for i in range(k):
            s, e = i * fs, min(i * fs + fs, n)
            Xt, yt = X[s:e], y[s:e]; Xr, yr = X[:s] + X[e:], y[:s] + y[e:]
            if not Xr:
                continue
            m = self._DecisionStump() if self.task_type == TaskType.CLASSIFICATION else self._SimpleLinearModel()
            m.fit(Xr, yr); preds = m.predict(Xt)
            if self.task_type == TaskType.CLASSIFICATION:
                scores.append(sum(1 for p, a in zip(preds, yt) if p == a) / len(yt))
            else:
                scores.append(math.sqrt(sum((p - a) ** 2 for p, a in zip(preds, yt)) / len(yt)))
        return {"mean_score": sum(scores) / len(scores) if scores else 0,
                "std_score": statistics.stdev(scores) if len(scores) > 1 else 0,
                "fold_scores": scores, "k": k}
# ── FeatureEngineer ───────────────────────────────────────────────────
class FeatureEngineer:
    """Feature creation, selection, and transformation."""
    def __init__(self) -> None:
        self._definitions: Dict[str, Dict[str, Any]] = {}
    def create_features(self, data: List[Dict[str, Any]],
                        specs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        result: List[Dict[str, Any]] = []
        for row in data:
            nr = dict(row)
            for spec in specs:
                name, op = spec["name"], spec["transformation"]
                try:
                    if op == "polynomial":
                        nr[name] = float(nr.get(spec["column"], 0)) ** spec.get("degree", 2)
                    elif op == "log":
                        v = float(nr.get(spec["column"], 0))
                        nr[name] = math.log(v) if v > 0 else 0.0
                    elif op == "sqrt":
                        nr[name] = math.sqrt(abs(float(nr.get(spec["column"], 0))))
                    elif op == "ratio":
                        d = float(nr.get(spec["column2"], 1))
                        nr[name] = float(nr.get(spec["column1"], 0)) / d if d else 0.0
                    elif op == "difference":
                        nr[name] = float(nr.get(spec["column1"], 0)) - float(nr.get(spec["column2"], 0))
                    elif op == "interaction":
                        nr[name] = float(nr.get(spec["column1"], 0)) * float(nr.get(spec["column2"], 0))
                    elif op == "absolute":
                        nr[name] = abs(float(nr.get(spec["column"], 0)))
                    elif op == "binning":
                        nr[name] = int(float(nr.get(spec["column"], 0)) * spec.get("bins", 5))
                    elif op == "date_parts":
                        dt = datetime.strptime(str(nr.get(spec["column"], "")), "%Y-%m-%d")
                        for attr in ("year", "month", "day", "weekday", "quarter"):
                            nr[f"{name}_{attr}"] = getattr(dt, attr) if attr != "quarter" else (dt.month - 1) // 3 + 1
                            if attr == "weekday":
                                nr[f"{name}_{attr}"] = dt.weekday()
                except (KeyError, ValueError, TypeError):
                    nr[name] = 0
            result.append(nr)
        return result
    def select_features(self, data: List[Dict[str, Any]], target_col: str,
                        method: str = "correlation", threshold: float = 0.1) -> List[str]:
        if not data:
            return []
        candidates = [c for c in data[0].keys() if c != target_col and isinstance(data[0].get(c), (int, float))]
        scores: Dict[str, float] = {}
        if method == "correlation":
            tv = [float(r.get(target_col, 0)) for r in data]
            for c in candidates:
                scores[c] = abs(self._pearson(tv, [float(r.get(c, 0)) for r in data]))
        elif method == "variance":
            for c in candidates:
                v = [float(r.get(c, 0)) for r in data]
                mu = sum(v) / len(v); scores[c] = sum((x - mu) ** 2 for x in v) / len(v)
        elif method == "mutual_information":
            tv = [float(r.get(target_col, 0)) for r in data]
            for c in candidates:
                scores[c] = self._mutual_info(tv, [float(r.get(c, 0)) for r in data])
        return [col for col, sc in sorted(scores.items(), key=lambda x: -x[1]) if sc >= threshold]
    @staticmethod
    def _pearson(x: List[float], y: List[float]) -> float:
        n = len(x)
        if n == 0:
            return 0.0
        mx, my = sum(x) / n, sum(y) / n
        num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
        dx = math.sqrt(sum((xi - mx) ** 2 for xi in x))
        dy = math.sqrt(sum((yi - my) ** 2 for yi in y))
        return num / (dx * dy) if dx and dy else 0.0

    @staticmethod
    def _mutual_info(x: List[float], y: List[float], bins: int = 10) -> float:
        n = len(x)
        if n == 0:
            return 0.0
        xr, yr = max(x) - min(x) or 1, max(y) - min(y) or 1
        joint = [[0] * bins for _ in range(bins)]
        for xi, yi in zip(x, y):
            bx = min(int((xi - min(x)) / xr * (bins - 1)), bins - 1)
            by = min(int((yi - min(y)) / yr * (bins - 1)), bins - 1)
            joint[bx][by] += 1
        mi = 0.0
        for i in range(bins):
            for j in range(bins):
                pxy = joint[i][j] / n
                if pxy == 0:
                    continue
                px = sum(joint[i][k] for k in range(bins)) / n
                py = sum(joint[k][j] for k in range(bins)) / n
                if px > 0 and py > 0:
                    mi += pxy * math.log(pxy / (px * py))
        return mi
    def polynomial_features(self, data: List[Dict[str, Any]], columns: List[str],
                            degree: int = 2) -> List[Dict[str, Any]]:
        result: List[Dict[str, Any]] = []
        for row in data:
            nr = dict(row)
            for col in columns:
                v = float(nr.get(col, 0))
                for d in range(2, degree + 1):
                    nr[f"{col}_pow{d}"] = v ** d
            for i, c1 in enumerate(columns):
                for c2 in columns[i + 1:]:
                    nr[f"{c1}_x_{c2}"] = float(nr.get(c1, 0)) * float(nr.get(c2, 0))
            result.append(nr)
        return result
# ── DataPreprocessor ──────────────────────────────────────────────────
class DataPreprocessor:
    """Data cleaning, imputation, encoding, and normalization."""
    def __init__(self) -> None:
        self._encoders: Dict[str, Dict[str, int]] = {}
        self._scaler_params: Dict[str, Dict[str, float]] = {}
    def handle_missing(self, data: List[Dict[str, Any]],
                       strategy: ImputationStrategy = ImputationStrategy.MEAN,
                       columns: Optional[List[str]] = None,
                       fill_value: Any = 0) -> List[Dict[str, Any]]:
        if not data:
            return data
        result = deepcopy(data); cols = columns or list(data[0].keys())
        for col in cols:
            vals = [r.get(col) for r in result if r.get(col) is not None]
            if strategy == ImputationStrategy.DROP:
                result = [r for r in result if r.get(col) is not None]
            elif strategy == ImputationStrategy.MEAN:
                nv = [float(v) for v in vals if isinstance(v, (int, float))]
                fill = sum(nv) / len(nv) if nv else fill_value
                for r in result:
                    if r.get(col) is None:
                        r[col] = fill
            elif strategy == ImputationStrategy.MEDIAN:
                nv = sorted([float(v) for v in vals if isinstance(v, (int, float))])
                fill = nv[len(nv) // 2] if nv else fill_value
                for r in result:
                    if r.get(col) is None:
                        r[col] = fill
            elif strategy == ImputationStrategy.MODE:
                counts: Dict[Any, int] = {}
                for v in vals:
                    counts[v] = counts.get(v, 0) + 1
                fill = max(counts, key=counts.get) if counts else fill_value
                for r in result:
                    if r.get(col) is None:
                        r[col] = fill
            elif strategy == ImputationStrategy.CONSTANT:
                for r in result:
                    if r.get(col) is None:
                        r[col] = fill_value
            elif strategy == ImputationStrategy.FORWARD_FILL:
                last = fill_value
                for r in result:
                    if r.get(col) is not None:
                        last = r[col]
                    else:
                        r[col] = last
            elif strategy == ImputationStrategy.BACKWARD_FILL:
                last = fill_value
                for r in reversed(result):
                    if r.get(col) is not None:
                        last = r[col]
                    else:
                        r[col] = last
        logger.info("Imputed missing values (strategy=%s)", strategy.value)
        return result
    def normalize(self, data: List[Dict[str, Any]], columns: List[str],
                  method: NormalizationMethod = NormalizationMethod.ZSCORE) -> List[Dict[str, Any]]:
        if not data:
            return data
        result = deepcopy(data)
        for col in columns:
            vals = [float(r[col]) for r in result if r.get(col) is not None]
            if not vals:
                continue
            if method == NormalizationMethod.MINMAX:
                lo, hi = min(vals), max(vals); rng = hi - lo or 1
                for r in result:
                    if r.get(col) is not None:
                        r[col] = (float(r[col]) - lo) / rng
            elif method == NormalizationMethod.ZSCORE:
                mu = sum(vals) / len(vals)
                std = math.sqrt(sum((v - mu) ** 2 for v in vals) / len(vals)) or 1
                for r in result:
                    if r.get(col) is not None:
                        r[col] = (float(r[col]) - mu) / std
                self._scaler_params[col] = {"mean": mu, "std": std}
            elif method == NormalizationMethod.ROBUST:
                s = sorted(vals); med = s[len(s) // 2]
                q1, q3 = s[len(s) // 4], s[3 * len(s) // 4]
                iqr = q3 - q1 or 1
                for r in result:
                    if r.get(col) is not None:
                        r[col] = (float(r[col]) - med) / iqr
        return result
    def encode(self, data: List[Dict[str, Any]], columns: List[str],
               method: EncodingMethod = EncodingMethod.LABEL
               ) -> Tuple[List[Dict[str, Any]], Dict[str, Dict[str, int]]]:
        if not data:
            return data, {}
        result = deepcopy(data); mappings: Dict[str, Dict[str, int]] = {}
        for col in columns:
            uv = sorted(set(str(r.get(col, "")) for r in result))
            mapping = {v: i for i, v in enumerate(uv)}; mappings[col] = mapping
            if method == EncodingMethod.LABEL:
                for r in result:
                    r[col] = mapping.get(str(r.get(col, "")), -1)
            elif method == EncodingMethod.FREQUENCY:
                freq: Dict[str, int] = {}
                for r in result:
                    k = str(r.get(col, "")); freq[k] = freq.get(k, 0) + 1
                for r in result:
                    r[col] = freq.get(str(r.get(col, "")), 0) / len(result)
            elif method == EncodingMethod.ONEHOT:
                for val in uv:
                    for r in result:
                        r[f"{col}_{val}"] = 1 if str(r.get(col, "")) == val else 0
                for r in result:
                    r.pop(col, None)
        return result, mappings
    def remove_duplicates(self, data: List[Dict[str, Any]],
                          key_columns: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        seen: set = set(); result: List[Dict[str, Any]] = []
        for row in data:
            ident = tuple(row.get(c) for c in key_columns) if key_columns else tuple(sorted(row.items()))
            if ident not in seen:
                seen.add(ident); result.append(row)
        return result
    def split_data(self, X: List[List[float]], y: List[float], test_size: float = 0.2,
                   strategy: SplitStrategy = SplitStrategy.RANDOM,
                   random_state: int = 42) -> Tuple[List[List[float]], List[List[float]], List[float], List[float]]:
        n = len(X); indices = list(range(n))
        rng = random.Random(random_state); rng.shuffle(indices)
        si = int(n * (1 - test_size)); ti = indices[:si]; tei = indices[si:]
        return [X[i] for i in ti], [X[i] for i in tei], [y[i] for i in ti], [y[i] for i in tei]
# ── HyperparameterTuner ───────────────────────────────────────────────
class HyperparameterTuner:
    """Grid search and random search for hyperparameter optimisation."""
    def __init__(self, builder: MLModelBuilder) -> None:
        self._builder = builder
    def grid_search(self, X: List[List[float]], y: List[float],
                    param_grid: Dict[str, List[Any]],
                    X_val: Optional[List[List[float]]] = None,
                    y_val: Optional[List[float]] = None) -> Dict[str, Any]:
        keys = list(param_grid.keys()); values = list(param_grid.values())
        combos = self._product(values)
        best_score, best_params = -float("inf"), {}; results: List[Dict[str, Any]] = []
        for combo in combos:
            params = dict(zip(keys, combo)); mt = params.pop("model_type", "stump")
            try:
                r = self._builder.train(X, y, model_type=mt, **params)
                if X_val and y_val:
                    preds = self._builder.predict(r.model_name, X_val)
                    score = (sum(1 for p, a in zip(preds, y_val) if p == a) / len(y_val)
                             if self._builder.task_type == TaskType.CLASSIFICATION
                             else -sum((p - a) ** 2 for p, a in zip(preds, y_val)) / len(y_val))
                else:
                    score = list(r.metrics.values())[0] if r.metrics else 0
                results.append({"params": params, "score": score})
                if score > best_score:
                    best_score, best_params = score, params
            except Exception as exc:
                logger.warning("Grid search combo failed: %s", exc)
        return {"best_params": best_params, "best_score": best_score, "all_results": results}
    def random_search(self, X: List[List[float]], y: List[float],
                      param_distributions: Dict[str, List[Any]], n_iter: int = 10,
                      random_state: int = 42) -> Dict[str, Any]:
        rng = random.Random(random_state); best_score, best_params = -float("inf"), {}
        results: List[Dict[str, Any]] = []
        for _ in range(n_iter):
            params = {k: rng.choice(v) for k, v in param_distributions.items()}
            mt = params.pop("model_type", "stump")
            try:
                r = self._builder.train(X, y, model_type=mt, **params)
                score = list(r.metrics.values())[0] if r.metrics else 0
                results.append({"params": params, "score": score})
                if score > best_score:
                    best_score, best_params = score, params
            except Exception as exc:
                logger.warning("Random search iteration failed: %s", exc)
        return {"best_params": best_params, "best_score": best_score, "all_results": results}
    @staticmethod
    def _product(lists: List[List[Any]]) -> List[List[Any]]:
        result: List[List[Any]] = [[]]
        for l in lists:
            result = [r + [item] for r in result for item in l]
        return result
# ── ModelEvaluator ────────────────────────────────────────────────────
class ModelEvaluator:
    """Compute classification and regression metrics."""
    def classification_metrics(self, actual: List[Any], predicted: List[Any]) -> Dict[str, Any]:
        classes = sorted(set(actual) | set(predicted))
        cm = [[0] * len(classes) for _ in range(len(classes))]
        idx = {c: i for i, c in enumerate(classes)}
        for a, p in zip(actual, predicted):
            cm[idx[a]][idx[p]] += 1
        total = len(actual)
        accuracy = sum(cm[i][i] for i in range(len(classes))) / total if total else 0
        per_class: Dict[str, Dict[str, float]] = {}
        for i, cls in enumerate(classes):
            tp = cm[i][i]; fp = sum(cm[j][i] for j in range(len(classes))) - tp; fn = sum(cm[i]) - tp
            pr = tp / (tp + fp) if (tp + fp) else 0; rc = tp / (tp + fn) if (tp + fn) else 0
            f1 = 2 * pr * rc / (pr + rc) if (pr + rc) else 0
            per_class[str(cls)] = {"precision": pr, "recall": rc, "f1": f1}
        mp = sum(v["precision"] for v in per_class.values()) / len(classes)
        mr = sum(v["recall"] for v in per_class.values()) / len(classes)
        mf1 = sum(v["f1"] for v in per_class.values()) / len(classes)
        return {"accuracy": accuracy, "macro_precision": mp, "macro_recall": mr,
                "macro_f1": mf1, "per_class": per_class, "confusion_matrix": cm, "classes": classes}
    def regression_metrics(self, actual: List[float], predicted: List[float]) -> Dict[str, float]:
        n = len(actual)
        if n == 0:
            return {}
        mse = sum((a - p) ** 2 for a, p in zip(actual, predicted)) / n
        mae = sum(abs(a - p) for a, p in zip(actual, predicted)) / n
        ma = sum(actual) / n; sst = sum((a - ma) ** 2 for a in actual)
        ssr = sum((a - p) ** 2 for a, p in zip(actual, predicted))
        r2 = 1 - ssr / sst if sst else 0
        nz = [a for a in actual if a != 0]
        mape = sum(abs((a - p) / a) for a, p in zip(actual, predicted) if a != 0) / len(nz) * 100 if nz else float("inf")
        return {"mse": mse, "rmse": math.sqrt(mse), "mae": mae, "r2": r2, "mape": mape}
    def compare_models(self, results: List[ModelResult]) -> List[Dict[str, Any]]:
        ranked = [{"model_name": r.model_name,
                    "primary_metric": list(r.metrics.values())[0] if r.metrics else 0,
                    "all_metrics": r.metrics} for r in results]
        return sorted(ranked, key=lambda x: x["primary_metric"], reverse=True)
# ── ExperimentDesigner ────────────────────────────────────────────────
class ExperimentDesigner:
    """Design, track, and persist data-science experiments."""
    def __init__(self, storage_dir: str = ".experiments") -> None:
        self._storage = Path(storage_dir); self._storage.mkdir(parents=True, exist_ok=True)
        self._experiments: Dict[str, ExperimentConfig] = {}
        self._results: Dict[str, ExperimentResult] = {}
    def create_experiment(self, name: str, description: str, task_type: TaskType,
                          target_column: str, feature_columns: List[str],
                          hyperparameters: Optional[Dict[str, Any]] = None,
                          split_strategy: SplitStrategy = SplitStrategy.RANDOM,
                          test_size: float = 0.2, random_state: int = 42) -> ExperimentConfig:
        eid = f"exp_{uuid.uuid4().hex[:12]}"
        config = ExperimentConfig(experiment_id=eid, name=name, description=description,
                                  task_type=task_type, target_column=target_column,
                                  feature_columns=feature_columns,
                                  hyperparameters=hyperparameters or {},
                                  split_strategy=split_strategy, test_size=test_size,
                                  random_state=random_state,
                                  created_at=datetime.now(timezone.utc).isoformat())
        self._experiments[eid] = config
        (self._storage / f"{eid}_config.json").write_text(json.dumps(asdict(config), indent=2, default=str))
        logger.info("Created experiment %s: %s", eid, name)
        return config
    def record_result(self, result: ExperimentResult) -> None:
        self._results[result.experiment_id] = result
        data = {"experiment_id": result.experiment_id, "model_name": result.model_result.model_name,
                "metrics": result.model_result.metrics, "cross_val_scores": result.cross_val_scores,
                "completed_at": result.completed_at}
        (self._storage / f"{result.experiment_id}_result.json").write_text(json.dumps(data, indent=2, default=str))
    def list_experiments(self) -> List[ExperimentConfig]:
        return list(self._experiments.values())
    def get_experiment(self, experiment_id: str) -> Optional[ExperimentConfig]:
        return self._experiments.get(experiment_id)
    def compare_experiments(self, experiment_ids: List[str]) -> List[Dict[str, Any]]:
        comps = []
        for eid in experiment_ids:
            exp, res = self._experiments.get(eid), self._results.get(eid)
            if exp and res:
                comps.append({"experiment_id": eid, "name": exp.name, "task_type": exp.task_type.value,
                              "primary_metric": list(res.model_result.metrics.values())[0] if res.model_result.metrics else None,
                              "cv_mean": sum(res.cross_val_scores) / len(res.cross_val_scores) if res.cross_val_scores else None})
        return sorted(comps, key=lambda x: x.get("primary_metric") or 0, reverse=True)
# ── DataVisualizer ────────────────────────────────────────────────────
class DataVisualizer:
    """Declarative visualization specification builder with ASCII rendering."""
    def __init__(self) -> None:
        self._specs: List[VisualizationSpec] = []
    def histogram(self, data: List[Dict[str, Any]], column: str, bins: int = 30,
                  title: str = "") -> VisualizationSpec:
        spec = VisualizationSpec(vis_type=VisType.HISTOGRAM, title=title or f"Distribution of {column}",
                                 x_column=column, bins=bins)
        self._specs.append(spec); return spec
    def scatter(self, data: List[Dict[str, Any]], x_col: str, y_col: str,
                hue: Optional[str] = None, title: str = "") -> VisualizationSpec:
        spec = VisualizationSpec(vis_type=VisType.SCATTER, title=title or f"{y_col} vs {x_col}",
                                 x_column=x_col, y_column=y_col, hue_column=hue)
        self._specs.append(spec); return spec
    def correlation_heatmap(self, matrix: Dict[str, Dict[str, float]],
                            title: str = "Correlation Matrix") -> VisualizationSpec:
        spec = VisualizationSpec(vis_type=VisType.HEATMAP, title=title, x_column="", y_column="")
        self._specs.append(spec); return spec
    def boxplot(self, data: List[Dict[str, Any]], column: str,
                group_by: Optional[str] = None, title: str = "") -> VisualizationSpec:
        spec = VisualizationSpec(vis_type=VisType.BOX, title=title or f"Box Plot of {column}",
                                 x_column=column, hue_column=group_by)
        self._specs.append(spec); return spec
    def render_ascii(self, spec: VisualizationSpec, data: List[Dict[str, Any]]) -> str:
        if spec.vis_type == VisType.HISTOGRAM:
            return self._ascii_histogram(data, spec.x_column, spec.bins)
        elif spec.vis_type == VisType.SCATTER:
            return self._ascii_scatter(data, spec.x_column, spec.y_column or "")
        elif spec.vis_type == VisType.BAR:
            return self._ascii_bar(data, spec.x_column)
        return f"[{spec.vis_type.value} visualization: {spec.title}]"

    @staticmethod
    def _ascii_histogram(data: List[Dict[str, Any]], column: str, bins: int) -> str:
        vals = [float(r.get(column, 0)) for r in data if r.get(column) is not None]
        if not vals:
            return f"No data for {column}"
        lo, hi = min(vals), max(vals); bw = (hi - lo) / bins if bins else 1
        counts = [0] * bins
        for v in vals:
            counts[min(int((v - lo) / bw), bins - 1)] += 1
        mc = max(counts) or 1; lines = [f"Histogram: {column} ({len(vals)} values, {bins} bins)", ""]
        for i, c in enumerate(counts):
            lines.append(f"{lo + i * bw:>8.1f} |{'█' * int(c / mc * 40)} ({c})")
        return "\n".join(lines)
    @staticmethod
    def _ascii_scatter(data: List[Dict[str, Any]], x_col: str, y_col: str) -> str:
        pts = [(float(r.get(x_col, 0)), float(r.get(y_col, 0))) for r in data if r.get(x_col) is not None and r.get(y_col) is not None]
        if not pts:
            return f"No data for {x_col} vs {y_col}"
        xv, yv = [p[0] for p in pts], [p[1] for p in pts]
        xlo, xhi, ylo, yhi = min(xv), max(xv), min(yv), max(yv)
        w, h = 50, 20; grid = [[" "] * w for _ in range(h)]
        for x, y in pts:
            c = int((x - xlo) / (xhi - xlo) * (w - 1)) if xhi != xlo else w // 2
            r = h - 1 - int((y - ylo) / (yhi - ylo) * (h - 1)) if yhi != ylo else h // 2
            grid[max(0, min(h - 1, r))][max(0, min(w - 1, c))] = "●"
        return "\n".join([f"Scatter: {y_col} vs {x_col} ({len(pts)} points)", ""] + ["".join(row) for row in grid])
    @staticmethod
    def _ascii_bar(data: List[Dict[str, Any]], column: str) -> str:
        counts: Dict[str, int] = {}
        for r in data:
            v = str(r.get(column, "N/A")); counts[v] = counts.get(v, 0) + 1
        top = sorted(counts.items(), key=lambda x: -x[1])[:15]
        if not top:
            return f"No data for {column}"
        mc = top[0][1]; lines = [f"Bar Chart: {column}", ""]
        for val, cnt in top:
            lines.append(f"{val[:20]:>20} |{'█' * int(cnt / mc * 40)} ({cnt})")
        return "\n".join(lines)
# ── ReproducibilityManager ───────────────────────────────────────────
class ReproducibilityManager:
    """Ensure experiments are fully reproducible."""
    def __init__(self, base_dir: str = ".reproducibility") -> None:
        self._base = Path(base_dir); self._base.mkdir(parents=True, exist_ok=True)
        self._records: List[ReproducibilityRecord] = []
    def snapshot(self, data: List[Dict[str, Any]], pipeline_steps: List[PipelineStep],
                 seeds: Optional[Dict[str, int]] = None) -> ReproducibilityRecord:
        dh = hashlib.sha256(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()[:16]
        ph = hashlib.sha256(json.dumps([asdict(s) for s in pipeline_steps], sort_keys=True, default=str).encode()).hexdigest()[:16]
        env = {"python_version": f"{__import__('sys').version_info.major}.{__import__('sys').version_info.minor}",
               "platform": __import__("sys").platform, "timestamp": datetime.now(timezone.utc).isoformat()}
        record = ReproducibilityRecord(record_id=f"rep_{uuid.uuid4().hex[:10]}", pipeline_hash=ph, data_hash=dh,
                                       random_seeds=seeds or {"python": 42}, environment=env, timestamp=env["timestamp"])
        self._records.append(record)
        (self._base / f"{record.record_id}.json").write_text(json.dumps(asdict(record), indent=2))
        logger.info("Snapshot %s created", record.record_id)
        return record
    def verify(self, record_id: str, data: List[Dict[str, Any]],
               pipeline_steps: List[PipelineStep]) -> bool:
        record = next((r for r in self._records if r.record_id == record_id), None)
        if record is None:
            path = self._base / f"{record_id}.json"
            if path.exists():
                record = ReproducibilityRecord(**json.loads(path.read_text()))
        if record is None:
            return False
        dh = hashlib.sha256(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()[:16]
        ph = hashlib.sha256(json.dumps([asdict(s) for s in pipeline_steps], sort_keys=True, default=str).encode()).hexdigest()[:16]
        ok = dh == record.data_hash and ph == record.pipeline_hash
        logger.info("Verification %s: %s", record_id, "PASS" if ok else "FAIL")
        return ok
    def get_environment(self) -> Dict[str, str]:
        return {"python_version": f"{__import__('sys').version_info.major}.{__import__('sys').version_info.minor}.{__import__('sys').version_info.micro}",
                "platform": __import__("sys").platform, "pid": str(os.getpid())}
# ── DataPipeline ──────────────────────────────────────────────────────
class DataPipeline:
    """Orchestrate a sequence of reproducible data-processing steps."""
    def __init__(self) -> None:
        self._steps: List[PipelineStep] = []
        self._step_functions: Dict[str, Callable[..., Any]] = {}
    def register(self, name: str, fn: Callable[..., Any]) -> None:
        self._step_functions[name] = fn
    def add_step(self, name: str, function_name: str, parameters: Optional[Dict[str, Any]] = None,
                 depends_on: Optional[List[str]] = None) -> PipelineStep:
        step = PipelineStep(step_id=f"step_{len(self._steps)}", name=name, function_name=function_name,
                            parameters=parameters or {}, depends_on=depends_on or [])
        self._steps.append(step); return step
    def run(self, data: Any, **global_context: Any) -> Any:
        result = data
        for step in self._steps:
            fn = self._step_functions.get(step.function_name)
            if fn is None:
                raise KeyError(f"No function registered for '{step.function_name}'")
            logger.info("Running step %s: %s", step.step_id, step.name)
            result = fn(result, **step.parameters, **global_context)
        logger.info("Pipeline complete — %d steps", len(self._steps))
        return result
    def get_steps(self) -> List[PipelineStep]:
        return list(self._steps)
    def to_dict(self) -> List[Dict[str, Any]]:
        return [asdict(s) for s in self._steps]
# ── Main ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logger.info("=== Data Science Agent Demo ===")
    sample_data = [
        {"age": 25, "income": 50000, "city": "NYC", "date": "2024-01-15"},
        {"age": 30, "income": 60000, "city": "LA", "date": "2024-01-16"},
        {"age": None, "income": 55000, "city": "NYC", "date": "2024-01-17"},
        {"age": 35, "income": 70000, "city": "CHI", "date": "2024-01-18"},
        {"age": 28, "income": None, "city": "LA", "date": "2024-01-19"},
    ]
    sa = StatisticalAnalyzer()
    desc = sa.describe([25.0, 30.0, 35.0, 28.0])
    logger.info("Descriptive stats: %s", {k: round(v, 3) for k, v in desc.items()})
    dp = DataPreprocessor()
    cleaned = dp.handle_missing(sample_data, strategy=ImputationStrategy.MEAN, columns=["age", "income"])
    encoded, mappings = dp.encode(cleaned, ["city"], method=EncodingMethod.LABEL)
    logger.info("City encoding: %s", mappings.get("city"))
    fe = FeatureEngineer()
    features = fe.create_features(encoded, [
        {"name": "income_log", "transformation": "log", "column": "income"},
        {"name": "age_income_ratio", "transformation": "ratio", "column1": "income", "column2": "age"},
    ])
    logger.info("Feature columns: %s", list(features[0].keys()))
    builder = MLModelBuilder(task_type=TaskType.REGRESSION)
    X = [[float(r.get("age", 0)), float(r.get("income", 0)), float(r.get("city", 0))] for r in features]
    y = [float(r.get("income", 0)) for r in features]
    result = builder.train(X, y, model_type="linear")
    logger.info("Model %s — metrics: %s", result.model_name, result.metrics)
    ed = ExperimentDesigner()
    exp = ed.create_experiment(name="income-prediction", description="Predict income from age and city",
                               task_type=TaskType.REGRESSION, target_column="income", feature_columns=["age", "city"])
    logger.info("Experiment %s created", exp.experiment_id)
    logger.info("=== Demo complete ===")
