"""
AI-ML Agent
Machine learning operations and model management

Comprehensive implementation featuring:
- Model registry and lifecycle management
- Training pipeline orchestration
- Inference engine with observability
- Drift detection and anomaly monitoring
- Hyperparameter tuning
- Batch operations
- Multi-format reporting
- Plugin/integration hooks
"""

from __future__ import annotations

import hashlib
import itertools
import logging
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

logger = logging.getLogger(__name__)


class ModelStatus(str, Enum):
    TRAINING = "training"
    DEPLOYED = "deployed"
    DEPRECATED = "deprecated"
    FAILED = "failed"


class Framework(str, Enum):
    TENSORFLOW = "tensorflow"
    PYTORCH = "pytorch"
    SKLEARN = "sklearn"
    XGBOOST = "xgboost"
    CUSTOM = "custom"


@dataclass
class Model:
    model_id: str
    name: str
    version: str
    status: ModelStatus
    metrics: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    deployed_at: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PredictionRecord:
    prediction_id: str
    model_id: str
    input_data: Dict[str, Any]
    output: Dict[str, Any]
    latency: float
    timestamp: float = field(default_factory=time.time)
    ground_truth: Optional[Dict[str, Any]] = None


@dataclass
class TrainingArtifact:
    step_name: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    duration: float = 0.0


@dataclass
class DriftReport:
    model_id: str
    drift_detected: bool
    drift_score: float
    threshold: float
    affected_features: List[str] = field(default_factory=list)
    recommendation: Optional[str] = None
    timestamp: float = field(default_factory=time.time)


@dataclass
class AnomalyResult:
    metric: str
    value: float
    is_anomaly: bool
    severity: str
    threshold_upper: Optional[float] = None
    threshold_lower: Optional[float] = None
    baseline_mean: Optional[float] = None
    baseline_std: Optional[float] = None
    z_score: Optional[float] = None
    recommendation: Optional[str] = None


@dataclass
class TrainingConfig:
    validation_split: float = 0.2
    cross_validation_folds: int = 5
    early_stopping_rounds: Optional[int] = None
    hyperparameter_trials: int = 50
    random_seed: int = 42
    max_parallel_jobs: int = 4


class ModelManager:
    """Manage ML models lifecycle: registration, versioning, deployment, comparison."""

    def __init__(self, max_versions: int = 10) -> None:
        self.models: Dict[str, Model] = {}
        self.model_registry: Dict[str, List[Model]] = {}
        self.max_versions = max_versions
        self._hooks: List[Callable[[str], None]] = []

    def register_model(
        self,
        name: str,
        version: str,
        model_path: str,
        metrics: Optional[Dict[str, Any]] = None,
        framework: Framework = Framework.CUSTOM,
        tags: Optional[Dict[str, str]] = None,
    ) -> str:
        """Register a new model in the registry."""
        model_id = hashlib.md5(f"{name}:{version}:{model_path}:{time.time_ns()}".encode()).hexdigest()[:12]

        metadata = {
            "path": model_path,
            "framework": framework.value,
            "tags": tags or {},
        }

        self.models[model_id] = Model(
            model_id=model_id,
            name=name,
            version=version,
            status=ModelStatus.TRAINING,
            metrics=metrics or {},
            metadata=metadata,
        )

        self.model_registry.setdefault(name, []).append(self.models[model_id])
        self._enforce_version_limit(name)
        self._run_hooks(model_id)

        logger.info("Registered model %s (%s v%s)", model_id, name, version)
        return model_id

    def deploy_model(self, model_id: str) -> bool:
        """Deploy a registered model to production."""
        model = self._get_model(model_id)
        if model is None:
            logger.warning("Model %s not found during deploy", model_id)
            return False

        if model.status == ModelStatus.FAILED:
            logger.warning("Model %s has failed status; cannot deploy", model_id)
            return False

        model.status = ModelStatus.DEPLOYED
        model.deployed_at = time.time()
        self._run_hooks(model_id)
        logger.info("Deployed model %s", model_id)
        return True

    def deprecate_model(self, model_id: str) -> bool:
        """Mark a model as deprecated."""
        model = self._get_model(model_id)
        if model is None:
            return False
        model.status = ModelStatus.DEPRECATED
        self._run_hooks(model_id)
        logger.info("Deprecated model %s", model_id)
        return True

    def get_model(self, model_id: str) -> Optional[Model]:
        """Get a model by id."""
        return self._get_model(model_id)

    def get_model_metrics(self, model_id: str) -> Dict[str, Any]:
        """Get model performance metrics."""
        model = self._get_model(model_id)
        return model.metrics if model else {}

    def compare_models(
        self,
        model_ids: Iterable[str],
        metric: str = "accuracy",
        higher_is_better: bool = True,
    ) -> Dict[str, Any]:
        """Compare model performance across the given ids."""
        comparison: Dict[str, Any] = {}
        for mid in model_ids:
            model = self._get_model(mid)
            if model is None:
                comparison[mid] = None
                continue

            value = model.metrics.get(metric)
            comparison[mid] = {
                "name": model.name,
                "version": model.version,
                "status": model.status.value,
                metric: value,
            }

        ranked = sorted(
            (k for k, v in comparison.items() if v is not None),
            key=lambda k: comparison[k].get(metric, float("-inf") if higher_is_better else float("inf")),
            reverse=higher_is_better,
        )
        return {
            "metric": metric,
            "higher_is_better": higher_is_better,
            "results": comparison,
            "ranking": ranked,
            "best": ranked[0] if ranked else None,
        }

    def list_models(self, name: Optional[str] = None, status: Optional[ModelStatus] = None) -> List[Model]:
        """List models, optionally filtered."""
        results = list(self.models.values())
        if name:
            results = [m for m in results if m.name == name]
        if status:
            results = [m for m in results if m.status == status]
        return results

    def add_deploy_hook(self, hook: Callable[[str], None]) -> None:
        """Add hook called after model deployment or deprecation."""
        self._hooks.append(hook)

    def _get_model(self, model_id: str) -> Optional[Model]:
        return self.models.get(model_id)

    def _enforce_version_limit(self, name: str) -> None:
        versions = self.model_registry.get(name, [])
        versions.sort(key=lambda m: m.created_at, reverse=True)
        for old in versions[self.max_versions:]:
            old.status = ModelStatus.DEPRECATED

    def _run_hooks(self, model_id: str) -> None:
        for hook in self._hooks:
            try:
                hook(model_id)
            except Exception as exc:
                logger.error("Deploy hook failed: %s", exc)


class TrainingPipeline:
    """Configurable training pipeline with step orchestration and hyperparameter tuning."""

    def __init__(self, config: Optional[TrainingConfig] = None) -> None:
        self.steps: List[Tuple[str, Callable[[Any], Any]]] = []
        self.artifacts: Dict[str, TrainingArtifact] = {}
        self.config = config or TrainingConfig()

    def add_step(self, step_name: str, function: Callable[[Any], Any]) -> None:
        """Add a training step."""
        if not step_name:
            raise ValueError("step_name must be non-empty")
        self.steps.append((step_name, function))

    def run(self, data_path: str) -> Dict[str, Any]:
        """Run all configured training steps against data_path."""
        results: Dict[str, Any] = {}
        start = time.time()
        for step_name, step_func in self.steps:
            step_start = time.time()
            try:
                result = step_func(data_path)
                self.artifacts[step_name] = TrainingArtifact(
                    step_name=step_name,
                    status="success",
                    result=result,
                    duration=time.time() - step_start,
                )
                results[step_name] = result
            except Exception as exc:
                self.artifacts[step_name] = TrainingArtifact(
                    step_name=step_name,
                    status="failed",
                    error=str(exc),
                    duration=time.time() - step_start,
                )
                logger.exception("Training step %s failed", step_name)
                raise
        return results

    def hyperparameter_tuning(
        self,
        param_grid: Dict[str, Any],
        objective: str = "accuracy",
    ) -> Dict[str, Any]:
        """Search parameter combinations and return the best result."""
        best_params: Dict[str, Any] = {}
        best_score = float("-inf")
        history: List[Dict[str, Any]] = []

        for params in self._generate_param_combinations(param_grid):
            try:
                score = self._evaluate_params(params, objective)
            except Exception as exc:
                logger.debug("Parameter evaluation failed: %s", exc)
                score = float("-inf")

            history.append({"params": params, "score": score})
            if score > best_score:
                best_score = score
                best_params = dict(params)

        return {
            "best_params": best_params,
            "best_score": best_score,
            "trials": len(history),
            "history": history[-50:],
        }

    def clear_steps(self) -> None:
        """Remove all training steps."""
        self.steps.clear()

    def _generate_param_combinations(self, param_grid: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
        keys = list(param_grid.keys())
        values = [
            param_grid[k] if isinstance(param_grid[k], list) else [param_grid[k]] for k in keys
        ]
        for combo in itertools.product(*values):
            yield dict(zip(keys, combo))

    def _evaluate_params(self, params: Dict[str, Any], objective: str) -> float:
        # Placeholder: replace with actual cross-validation logic.
        base = 0.5
        if objective in {"accuracy", "f1", "precision", "recall"}:
            return base + (hash(str(params)) % 100) / 500.0
        if objective in {"mse", "mae"}:
            return base + (hash(str(params)) % 100) / 1000.0
        raise ValueError(f"Unsupported objective: {objective}")


class InferenceEngine:
    """Serve predictions with optional logging and batching."""

    def __init__(self) -> None:
        self.model: Any = None
        self.model_id: Optional[str] = None

    def load_model(self, model_id: str, model_lookup: Optional[Dict[str, Any]] = None) -> None:
        """Load a model artifact for serving."""
        self.model_id = model_id
        self.model = (model_lookup or {}).get(model_id)
        logger.info("Loaded model %s", model_id)

    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single prediction."""
        if self.model is None:
            raise RuntimeError("Model not loaded")

        start = time.time()
        # Placeholder payload; replace with actual model inference.
        output = self.model.predict(input_data) if hasattr(self.model, "predict") else {"label": "unknown"}
        latency = time.time() - start
        return {
            "prediction_id": str(uuid.uuid4()),
            "model_id": self.model_id,
            "input": input_data,
            "output": output,
            "latency": latency,
            "timestamp": time.time(),
        }

    def batch_predict(self, inputs: List[Dict[str, Any]], batch_size: int = 32) -> List[Dict[str, Any]]:
        """Run predictions in batches."""
        results: List[Dict[str, Any]] = []
        for i in range(0, len(inputs), batch_size):
            batch = inputs[i : i + batch_size]
            for item in batch:
                results.append(self.predict(item))
        return results


class Aiobservability:
    """Log predictions and detect data drift or performance degradation."""

    def __init__(self, retention_days: int = 30) -> None:
        self.predictions: List[PredictionRecord] = []
        self.drift_reports: List[DriftReport] = []
        self.retention_days = retention_days
        self._thresholds: Dict[str, Tuple[Optional[float], Optional[float]]] = {}
        self._baselines: Dict[str, Dict[str, Any]] = {}

    def log_prediction(
        self,
        model_id: str,
        input_data: Dict[str, Any],
        output: Dict[str, Any],
        latency: float,
        *,
        ground_truth: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log a single prediction."""
        record = PredictionRecord(
            prediction_id=str(uuid.uuid4()),
            model_id=model_id,
            input_data=input_data,
            output=output,
            latency=latency,
            ground_truth=ground_truth,
        )
        self.predictions.append(record)
        self._enforce_retention()
        logger.debug("Logged prediction for %s", model_id)

    def log_predictions_bulk(self, records: Iterable[PredictionRecord]) -> None:
        """Log multiple prediction records."""
        self.predictions.extend(records)
        self._enforce_retention()

    def detect_drift(
        self,
        model_id: str,
        reference_data: List[Dict[str, Any]],
        current_data: List[Dict[str, Any]],
        threshold: float = 0.1,
    ) -> DriftReport:
        """Detect data drift between reference and current datasets."""
        ref_stats = self._compute_stats(reference_data)
        curr_stats = self._compute_stats(current_data)
        drift_score = self._compute_drift_score(ref_stats, curr_stats)
        affected = [k for k, v in drift_score.get("per_feature", {}).items() if v > threshold]

        report = DriftReport(
            model_id=model_id,
            drift_detected=drift_score["total"] > threshold,
            drift_score=drift_score["total"],
            threshold=threshold,
            affected_features=affected,
            recommendation="Consider retraining with recent data" if affected else None,
        )
        self.drift_reports.append(report)
        logger.info("Drift report for %s: detected=%s score=%.4f", model_id, report.drift_detected, report.drift_score)
        return report

    def get_predictions(self, model_id: Optional[str] = None, limit: int = 1000) -> List[PredictionRecord]:
        """Get recent prediction records."""
        records = self.predictions if model_id is None else [r for r in self.predictions if r.model_id == model_id]
        return records[-limit:]

    def set_drift_threshold(self, threshold: float) -> None:
        self._thresholds["drift"] = (threshold, None)

    def _enforce_retention(self) -> None:
        cutoff = time.time() - (self.retention_days * 86400)
        self.predictions = [r for r in self.predictions if r.timestamp >= cutoff]
        self.drift_reports = [r for r in self.drift_reports if r.timestamp >= cutoff]

    @staticmethod
    def _compute_stats(data: List[Dict[str, Any]]) -> Dict[str, Any]:
        numeric_fields: Dict[str, List[float]] = {}
        for row in data:
            for key, value in row.items():
                if isinstance(value, (int, float)):
                    numeric_fields.setdefault(key, []).append(float(value))

        summary: Dict[str, Any] = {}
        for field, values in numeric_fields.items():
            if not values:
                continue
            values_sorted = sorted(values)
            n = len(values_sorted)
            mean = sum(values_sorted) / n
            variance = sum((v - mean) ** 2 for v in values_sorted) / n
            std = variance ** 0.5
            summary[field] = {
                "mean": mean,
                "std": std,
                "n": n,
                "min": values_sorted[0],
                "max": values_sorted[-1],
            }
        return summary

    def _compute_drift_score(
        self,
        ref_stats: Dict[str, Any],
        curr_stats: Dict[str, Any],
    ) -> Dict[str, Any]:
        per_feature: Dict[str, float] = {}
        for feature in ref_stats.keys() & curr_stats.keys():
            ref = ref_stats[feature]
            curr = curr_stats[feature]
            z_ref = abs(ref.get("mean", 0)) / (ref.get("std", 0) + 1e-9)
            z_curr = abs(curr.get("mean", 0)) / (curr.get("std", 0) + 1e-9)
            per_feature[feature] = abs(z_curr - z_ref)

        total = sum(per_feature.values()) / (len(per_feature) + 1e-9)
        return {"total": total, "per_feature": per_feature}


class AnomalyDetector:
    """Static-threshold and baseline-based anomaly detection."""

    def __init__(self) -> None:
        self.thresholds: Dict[str, Dict[str, Optional[float]]] = {}
        self.baselines: Dict[str, Dict[str, Any]] = {}

    def set_threshold(self, metric: str, upper: float, lower: float = 0) -> None:
        if upper < lower:
            raise ValueError("upper threshold must be >= lower threshold")
        self.thresholds[metric] = {"upper": upper, "lower": lower}

    def set_baseline(
        self,
        metric: str,
        mean: float,
        std: float,
        samples: int = 30,
        z_threshold: float = 3.0,
    ) -> None:
        if std < 0:
            raise ValueError("std must be non-negative")
        self.baselines[metric] = {
            "mean": mean,
            "std": std,
            "samples": samples,
            "z_threshold": z_threshold,
        }

    def check_anomaly(
        self,
        metric: str,
        value: float,
        *,
        recommendation: Optional[str] = None,
    ) -> AnomalyResult:
        """Check a metric value against configured thresholds or baseline."""
        if metric in self.thresholds:
            thresh = self.thresholds[metric]
            upper = thresh.get("upper")
            lower = thresh.get("lower")
            is_anomaly = (upper is not None and value > upper) or (lower is not None and value < lower)
            severity = "critical" if is_anomaly else "normal"
            return AnomalyResult(
                metric=metric,
                value=value,
                is_anomaly=is_anomaly,
                severity=severity,
                threshold_upper=upper,
                threshold_lower=lower,
                recommendation=recommendation or ("Review immediate action" if is_anomaly else None),
            )

        if metric in self.baselines:
            baseline = self.baselines[metric]
            mean = baseline.get("mean", 0)
            std = baseline.get("std", 0)
            z_threshold = baseline.get("z_threshold", 3.0)
            z_score = abs(value - mean) / (std + 1e-9) if std else 0.0
            is_anomaly = z_score > z_threshold
            severity = "critical" if z_score > z_threshold * 1.5 else "warning" if is_anomaly else "normal"
            return AnomalyResult(
                metric=metric,
                value=value,
                is_anomaly=is_anomaly,
                severity=severity,
                baseline_mean=mean,
                baseline_std=std,
                z_score=z_score,
                recommendation=recommendation or ("Value deviates from baseline" if is_anomaly else None),
            )

        return AnomalyResult(
            metric=metric,
            value=value,
            is_anomaly=False,
            severity="unknown",
            recommendation="No threshold or baseline configured",
        )

    def remove_metric(self, metric: str) -> None:
        self.thresholds.pop(metric, None)
        self.baselines.pop(metric, None)


class ReportingEngine:
    """Simple reporting engine that serializes model state and artifacts."""

    def __init__(self, output_directory: str = "./ai_ml_reports") -> None:
        self.output_directory = output_directory
        self._reports: Dict[str, Dict[str, Any]] = {}

    def generate_model_report(self, manager: ModelManager, model_id: str) -> Dict[str, Any]:
        model = manager.get_model(model_id)
        if model is None:
            raise ValueError(f"Model {model_id} not found")
        report = {
            "model_id": model.model_id,
            "name": model.name,
            "version": model.version,
            "status": model.status.value,
            "metrics": model.metrics,
            "created_at": model.created_at,
            "deployed_at": model.deployed_at,
            "metadata": model.metadata,
        }
        self._reports[model_id] = report
        return report

    def export_report(self, report: Dict[str, Any], fmt: str = "json", path: Optional[str] = None) -> str:
        if fmt == "json":
            payload = json_dumps(report)
            target = path or f"{self.output_directory}/{report['model_id']}.json"
            with open(target, "w", encoding="utf-8") as f:
                f.write(payload)
            return target
        if fmt == "csv":
            rows = [report]
            target = path or f"{self.output_directory}/{report['model_id']}.csv"
            with open(target, "w", encoding="utf-8") as f:
                f.write(",".join(report.keys()) + "\n")
                f.write(",".join(str(v) for v in report.values()) + "\n")
            return target
        raise ValueError(f"Unsupported report format: {fmt}")


def json_dumps(payload: Dict[str, Any]) -> str:
    import json

    return json.dumps(payload, indent=2, default=str)


class AiMlAgent:
    """High-level orchestrator for ML operations."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.manager = ModelManager(max_versions=self.config.get("max_model_versions", 10))
        self.pipeline = TrainingPipeline(config=TrainingConfig(
            hyperparameter_trials=self.config.get("hyperparameter_trials", 50),
            max_parallel_jobs=self.config.get("max_parallel_jobs", 4),
        ))
        self.inference = InferenceEngine()
        self.observability = Aiobservability(
            retention_days=self.config.get("prediction_log_retention_days", 30),
        )
        self.anomaly = AnomalyDetector()
        self.reporter = ReportingEngine(
            output_directory=self.config.get("output_directory", "./ai_ml_reports"),
        )
        self._plugins: List[Callable[[], None]] = []

    def register_model(
        self,
        name: str,
        version: str,
        model_path: str,
        metrics: Optional[Dict[str, Any]] = None,
        framework: str = "custom",
    ) -> str:
        return self.manager.register_model(
            name=name,
            version=version,
            model_path=model_path,
            metrics=metrics or {},
            framework=Framework(framework),
        )

    def train(self, data_path: str, steps: Optional[List[Tuple[str, Callable]]] = None) -> Dict[str, Any]:
        if steps:
            self.pipeline.clear_steps()
            for step_name, step_func in steps:
                self.pipeline.add_step(step_name, step_func)
        return self.pipeline.run(data_path)

    def deploy(self, model_id: str) -> bool:
        return self.manager.deploy_model(model_id)

    def predict(self, model_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.inference.load_model(model_id)
        result = self.inference.predict(input_data)
        self.observability.log_prediction(
            model_id=model_id,
            input_data=input_data,
            output=result["output"],
            latency=result["latency"],
        )
        return result

    def batch_predict(self, model_id: str, inputs: List[Dict[str, Any]], batch_size: int = 32) -> List[Dict[str, Any]]:
        self.inference.load_model(model_id)
        results = self.inference.batch_predict(inputs, batch_size=batch_size)
        self.observability.log_predictions_bulk(
            [
                PredictionRecord(
                    prediction_id=r["prediction_id"],
                    model_id=r["model_id"],
                    input_data=r["input"],
                    output=r["output"],
                    latency=r["latency"],
                )
                for r in results
            ]
        )
        return results

    def detect_drift(
        self,
        model_id: str,
        reference_data: List[Dict[str, Any]],
        current_data: List[Dict[str, Any]],
        threshold: float = 0.1,
    ) -> DriftReport:
        return self.observability.detect_drift(model_id, reference_data, current_data, threshold=threshold)

    def tune(self, param_grid: Dict[str, Any], objective: str = "accuracy") -> Dict[str, Any]:
        return self.pipeline.hyperparameter_tuning(param_grid, objective=objective)

    def get_status(self) -> Dict[str, Any]:
        return {
            "models": len(self.manager.models),
            "deployed": len(self.manager.list_models(status=ModelStatus.DEPLOYED)),
            "training": len(self.manager.list_models(status=ModelStatus.TRAINING)),
            "predictions_logged": len(self.observability.predictions),
            "drift_reports": len(self.observability.drift_reports),
            "pipeline_steps": len(self.pipeline.steps),
        }

    def add_plugin(self, plugin: Callable[[], None]) -> None:
        self._plugins.append(plugin)

    def run_plugins(self) -> None:
        for plugin in self._plugins:
            try:
                plugin()
            except Exception as exc:
                logger.error("Plugin failed: %s", exc)
