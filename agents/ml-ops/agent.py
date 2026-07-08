"""
ML Ops Agent
MLOps pipelines, model deployment, feature stores, experiment tracking, model monitoring, and A/B testing.
"""

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple
from uuid import uuid4

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────

class ModelStatus(Enum):
    REGISTERED = "registered"
    TRAINING = "training"
    TRAINED = "trained"
    VALIDATING = "validating"
    DEPLOYED = "deployed"
    MONITORING = "monitoring"
    NEEDS_RETRAINING = "needs_retraining"
    RETIRED = "retired"
    ARCHIVED = "archived"


class PipelineStage(Enum):
    DATA_INGESTION = "data_ingestion"
    PREPROCESSING = "preprocessing"
    FEATURE_ENGINEERING = "feature_engineering"
    TRAINING = "training"
    EVALUATION = "evaluation"
    REGISTRATION = "registration"
    DEPLOYMENT = "deployment"
    MONITORING = "monitoring"


class DriftType(Enum):
    DATA_DRIFT = "data_drift"
    CONCEPT_DRIFT = "concept_drift"
    PREDICTION_DRIFT = "prediction_drift"
    LABEL_DRIFT = "label_drift"


class ExperimentStatus(Enum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class DeploymentEnvironment(Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"
    CANARY = "canary"


class ABTestStatus(Enum):
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class MetricType(Enum):
    ACCURACY = "accuracy"
    PRECISION = "precision"
    RECALL = "recall"
    F1 = "f1"
    AUC = "auc"
    MSE = "mse"
    RMSE = "rmse"
    MAE = "mae"
    LATENCY = "latency"
    THROUGHPUT = "throughput"


class AlertSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


# ──────────────────────────────────────────────
# Data Classes
# ──────────────────────────────────────────────

@dataclass
class Model:
    model_id: str = field(default_factory=lambda: f"model_{str(uuid4())[:8]}")
    name: str = ""
    version: str = "1.0.0"
    framework: str = ""
    task: str = ""
    status: ModelStatus = ModelStatus.REGISTERED
    metrics: Dict[str, float] = field(default_factory=dict)
    artifacts: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class TrainingRun:
    run_id: str = field(default_factory=lambda: f"run_{str(uuid4())[:8]}")
    model_name: str = ""
    pipeline_id: str = ""
    status: str = "created"
    config: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, float] = field(default_factory=dict)
    parameters: Dict[str, Any] = field(default_factory=dict)
    artifacts: List[str] = field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: float = 0.0


@dataclass
class PipelineStep:
    step_id: str = field(default_factory=lambda: f"step_{str(uuid4())[:8]}")
    name: str = ""
    stage: PipelineStage = PipelineStage.DATA_INGESTION
    status: str = "pending"
    config: Dict[str, Any] = field(default_factory=dict)
    duration_seconds: float = 0.0
    error: Optional[str] = None


@dataclass
class Pipeline:
    pipeline_id: str = field(default_factory=lambda: f"pipe_{str(uuid4())[:8]}")
    name: str = ""
    steps: List[PipelineStep] = field(default_factory=list)
    status: str = "created"
    model_name: str = ""
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Feature:
    feature_id: str = field(default_factory=lambda: f"feat_{str(uuid4())[:8]}")
    name: str = ""
    dtype: str = "float"
    source: str = ""
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: Optional[datetime] = None


@dataclass
class Experiment:
    experiment_id: str = field(default_factory=lambda: f"exp_{str(uuid4())[:8]}")
    name: str = ""
    description: str = ""
    status: ExperimentStatus = ExperimentStatus.CREATED
    runs: List[TrainingRun] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ABVariant:
    variant_id: str = ""
    model_id: str = ""
    traffic_percentage: float = 0.0
    metrics: Dict[str, float] = field(default_factory=dict)
    sample_size: int = 0


@dataclass
class ABTest:
    test_id: str = field(default_factory=lambda: f"test_{str(uuid4())[:8]}")
    name: str = ""
    status: ABTestStatus = ABTestStatus.DRAFT
    variants: List[ABVariant] = field(default_factory=list)
    winning_variant: Optional[str] = None
    confidence: float = 0.0
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


@dataclass
class DeploymentRecord:
    deployment_id: str = field(default_factory=lambda: f"dep_{str(uuid4())[:8]}")
    model_id: str = ""
    environment: DeploymentEnvironment = DeploymentEnvironment.STAGING
    endpoint: str = ""
    replicas: int = 1
    status: str = "pending"
    resources: Dict[str, Any] = field(default_factory=dict)
    deployed_at: Optional[datetime] = None


@dataclass
class DriftAlert:
    alert_id: str = field(default_factory=lambda: f"alert_{str(uuid4())[:8]}")
    model_id: str = ""
    drift_type: DriftType = DriftType.DATA_DRIFT
    severity: AlertSeverity = AlertSeverity.MEDIUM
    affected_features: List[str] = field(default_factory=list)
    detection_score: float = 0.0
    message: str = ""
    detected_at: datetime = field(default_factory=datetime.now)


@dataclass
class FeatureValue:
    feature_name: str = ""
    entity_id: str = ""
    value: Any = None
    timestamp: datetime = field(default_factory=datetime.now)


# ──────────────────────────────────────────────
# Exceptions
# ──────────────────────────────────────────────

class MLOpsError(Exception):
    """Base MLOps error."""


class ModelNotFoundError(MLOpsError):
    """Model ID not found."""


class PipelineError(MLOpsError):
    """Pipeline execution error."""


class DeploymentError(MLOpsError):
    """Deployment failed."""


class FeatureStoreError(MLOpsError):
    """Feature store operation failed."""


# ──────────────────────────────────────────────
# Model Registry
# ──────────────────────────────────────────────

class ModelRegistry:
    """Register, version, and manage ML models."""

    def __init__(self) -> None:
        self._models: Dict[str, Model] = {}
        self._version_history: Dict[str, List[str]] = {}

    def register_model(
        self,
        name: str,
        version: str,
        framework: str,
        task: str,
        metrics: Optional[Dict[str, float]] = None,
        artifacts: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
    ) -> Model:
        model = Model(
            name=name,
            version=version,
            framework=framework,
            task=task,
            metrics=metrics or {},
            artifacts=artifacts or [],
            tags=tags or [],
        )
        self._models[model.model_id] = model
        self._version_history.setdefault(name, []).append(version)
        logger.info("Registered model %s v%s (%s)", name, version, model.model_id)
        return model

    def get_model(self, model_id: str) -> Model:
        if model_id not in self._models:
            raise ModelNotFoundError(f"Model {model_id} not found")
        return self._models[model_id]

    def update_model(self, model_id: str, **kwargs: Any) -> Model:
        model = self.get_model(model_id)
        for key, value in kwargs.items():
            if hasattr(model, key):
                setattr(model, key, value)
        model.updated_at = datetime.now()
        return model

    def list_models(self, name: Optional[str] = None, status: Optional[ModelStatus] = None) -> List[Model]:
        models = list(self._models.values())
        if name:
            models = [m for m in models if m.name == name]
        if status:
            models = [m for m in models if m.status == status]
        return models

    def get_latest_version(self, name: str) -> Optional[Model]:
        versions = self._version_history.get(name, [])
        if not versions:
            return None
        latest = versions[-1]
        for model in self._models.values():
            if model.name == name and model.version == latest:
                return model
        return None

    def promote_model(self, model_id: str, target_env: DeploymentEnvironment) -> DeploymentRecord:
        model = self.get_model(model_id)
        record = DeploymentRecord(
            model_id=model_id,
            environment=target_env,
            endpoint=f"https://api.example.com/v1/predict/{model.name}/{model.version}",
        )
        logger.info("Promoted model %s to %s", model_id, target_env.value)
        return record

    def retire_model(self, model_id: str) -> Model:
        return self.update_model(model_id, status=ModelStatus.RETIRED)


# ──────────────────────────────────────────────
# Pipeline Manager
# ──────────────────────────────────────────────

class PipelineManager:
    """Create and manage ML training pipelines."""

    def __init__(self) -> None:
        self._pipelines: Dict[str, Pipeline] = {}
        self._runs: Dict[str, TrainingRun] = {}

    def create_pipeline(
        self,
        name: str,
        model_name: str,
        steps_config: List[Dict[str, Any]],
    ) -> Pipeline:
        pipeline = Pipeline(name=name, model_name=model_name)
        for i, step_config in enumerate(steps_config):
            stage = PipelineStage(step_config.get("stage", "data_ingestion"))
            step = PipelineStep(
                name=step_config.get("name", f"step_{i}"),
                stage=stage,
                config=step_config.get("config", {}),
            )
            pipeline.steps.append(step)
        self._pipelines[pipeline.pipeline_id] = pipeline
        logger.info("Created pipeline %s with %d steps", pipeline.pipeline_id, len(pipeline.steps))
        return pipeline

    def execute_pipeline(self, pipeline_id: str, parameters: Optional[Dict[str, Any]] = None) -> TrainingRun:
        pipeline = self._get_pipeline(pipeline_id)
        run = TrainingRun(
            model_name=pipeline.model_name,
            pipeline_id=pipeline_id,
            config=parameters or {},
            started_at=datetime.now(),
            status="running",
        )
        pipeline.status = "running"
        for step in pipeline.steps:
            step.status = "completed"
            step.duration_seconds = 10.0
        run.status = "completed"
        run.completed_at = datetime.now()
        run.duration_seconds = (run.completed_at - run.started_at).total_seconds()
        run.metrics = {"loss": 0.15, "accuracy": 0.92}
        pipeline.status = "completed"
        self._runs[run.run_id] = run
        logger.info("Pipeline %s completed in %.1fs", pipeline_id, run.duration_seconds)
        return run

    def get_run(self, run_id: str) -> TrainingRun:
        if run_id not in self._runs:
            raise PipelineError(f"Run {run_id} not found")
        return self._runs[run_id]

    def list_pipelines(self) -> List[Pipeline]:
        return list(self._pipelines.values())

    def list_runs(self, pipeline_id: Optional[str] = None) -> List[TrainingRun]:
        runs = list(self._runs.values())
        if pipeline_id:
            runs = [r for r in runs if r.pipeline_id == pipeline_id]
        return runs

    def _get_pipeline(self, pipeline_id: str) -> Pipeline:
        if pipeline_id not in self._pipelines:
            raise PipelineError(f"Pipeline {pipeline_id} not found")
        return self._pipelines[pipeline_id]


# ──────────────────────────────────────────────
# Feature Store
# ──────────────────────────────────────────────

class FeatureStore:
    """Manage, serve, and compute features for ML models."""

    def __init__(self) -> None:
        self._features: Dict[str, Feature] = {}
        self._values: Dict[str, List[FeatureValue]] = {}

    def register_feature(
        self,
        name: str,
        dtype: str,
        source: str,
        description: str = "",
    ) -> Feature:
        feature = Feature(name=name, dtype=dtype, source=source, description=description)
        self._features[feature.feature_id] = feature
        logger.info("Registered feature %s (%s)", name, feature.feature_id)
        return feature

    def ingest_value(self, feature_name: str, entity_id: str, value: Any) -> FeatureValue:
        fv = FeatureValue(feature_name=feature_name, entity_id=entity_id, value=value)
        self._values.setdefault(feature_name, []).append(fv)
        return fv

    def get_latest_value(self, feature_name: str, entity_id: str) -> Optional[FeatureValue]:
        values = self._values.get(feature_name, [])
        for fv in reversed(values):
            if fv.entity_id == entity_id:
                return fv
        return None

    def get_feature_values(self, feature_name: str) -> List[FeatureValue]:
        return self._values.get(feature_name, [])

    def compute_features(self, feature_name: str, entity_ids: List[str]) -> Dict[str, Any]:
        results: Dict[str, Any] = {}
        values = self._values.get(feature_name, [])
        for eid in entity_ids:
            entity_vals = [fv.value for fv in values if fv.entity_id == eid and isinstance(fv.value, (int, float))]
            if entity_vals:
                results[eid] = {
                    "latest": entity_vals[-1],
                    "mean": sum(entity_vals) / len(entity_vals),
                    "min": min(entity_vals),
                    "max": max(entity_vals),
                    "count": len(entity_vals),
                }
        return results

    def list_features(self) -> List[Feature]:
        return list(self._features.values())

    def get_feature_stats(self) -> Dict[str, Any]:
        stats: Dict[str, Any] = {}
        for name, values in self._values.items():
            numeric = [v.value for v in values if isinstance(v.value, (int, float))]
            stats[name] = {
                "total_values": len(values),
                "unique_entities": len(set(v.entity_id for v in values)),
                "mean": sum(numeric) / len(numeric) if numeric else 0,
            }
        return stats


# ──────────────────────────────────────────────
# Experiment Tracker
# ──────────────────────────────────────────────

class ExperimentTracker:
    """Track ML experiments, runs, and compare results."""

    def __init__(self) -> None:
        self._experiments: Dict[str, Experiment] = {}

    def create_experiment(
        self, name: str, description: str = "", tags: Optional[List[str]] = None
    ) -> Experiment:
        exp = Experiment(name=name, description=description, tags=tags or [])
        self._experiments[exp.experiment_id] = exp
        logger.info("Created experiment %s (%s)", exp.experiment_id, name)
        return exp

    def log_run(
        self,
        experiment_id: str,
        model_name: str,
        parameters: Dict[str, Any],
        metrics: Dict[str, float],
        artifacts: Optional[List[str]] = None,
    ) -> TrainingRun:
        exp = self._get_experiment(experiment_id)
        run = TrainingRun(
            model_name=model_name,
            parameters=parameters,
            metrics=metrics,
            artifacts=artifacts or [],
            status="completed",
            started_at=datetime.now(),
            completed_at=datetime.now(),
        )
        exp.runs.append(run)
        return run

    def compare_runs(self, experiment_id: str) -> Dict[str, Any]:
        exp = self._get_experiment(experiment_id)
        if not exp.runs:
            return {"error": "No runs to compare"}
        comparison: Dict[str, Any] = {"total_runs": len(exp.runs), "runs": []}
        for run in exp.runs:
            comparison["runs"].append({
                "run_id": run.run_id,
                "parameters": run.parameters,
                "metrics": run.metrics,
            })
        all_metric_keys = set()
        for run in exp.runs:
            all_metric_keys.update(run.metrics.keys())
        best_per_metric: Dict[str, Dict[str, Any]] = {}
        for key in all_metric_keys:
            best_val = None
            best_run = None
            for run in exp.runs:
                if key in run.metrics:
                    if best_val is None or run.metrics[key] > best_val:
                        best_val = run.metrics[key]
                        best_run = run.run_id
            best_per_metric[key] = {"best_run": best_run, "best_value": best_val}
        comparison["best_per_metric"] = best_per_metric
        return comparison

    def get_experiment(self, experiment_id: str) -> Experiment:
        return self._get_experiment(experiment_id)

    def list_experiments(self) -> List[Experiment]:
        return list(self._experiments.values())

    def _get_experiment(self, experiment_id: str) -> Experiment:
        if experiment_id not in self._experiments:
            raise MLOpsError(f"Experiment {experiment_id} not found")
        return self._experiments[experiment_id]


# ──────────────────────────────────────────────
# Model Monitor
# ──────────────────────────────────────────────

class ModelMonitor:
    """Monitor deployed models for drift, performance, and health."""

    def __init__(self) -> None:
        self._predictions: Dict[str, List[Dict[str, Any]]] = {}
        self._alerts: List[DriftAlert] = []
        self._baseline_metrics: Dict[str, Dict[str, float]] = {}

    def set_baseline(self, model_id: str, metrics: Dict[str, float]) -> None:
        self._baseline_metrics[model_id] = metrics

    def log_prediction(
        self, model_id: str, prediction: Any, actual: Optional[Any] = None, latency_ms: float = 0.0
    ) -> None:
        self._predictions.setdefault(model_id, []).append({
            "prediction": prediction,
            "actual": actual,
            "latency_ms": latency_ms,
            "timestamp": datetime.now(),
        })

    def check_health(self, model_id: str) -> Dict[str, Any]:
        preds = self._predictions.get(model_id, [])
        if not preds:
            return {"status": "no_data", "model_id": model_id}
        latencies = [p["latency_ms"] for p in preds if p["latency_ms"] > 0]
        error_rate = sum(1 for p in preds if p["actual"] is not None and p["prediction"] != p["actual"]) / len(preds) if preds else 0
        return {
            "model_id": model_id,
            "status": "healthy",
            "total_predictions": len(preds),
            "avg_latency_ms": round(sum(latencies) / len(latencies), 2) if latencies else 0,
            "p99_latency_ms": round(sorted(latencies)[int(len(latencies) * 0.99)] if latencies else 0, 2),
            "error_rate": round(error_rate, 4),
        }

    def detect_drift(self, model_id: str, reference_data: List[float], current_data: List[float]) -> DriftAlert:
        ref_mean = sum(reference_data) / len(reference_data) if reference_data else 0
        cur_mean = sum(current_data) / len(current_data) if current_data else 0
        ref_std = self._std_dev(reference_data)
        cur_std = self._std_dev(current_data)
        mean_shift = abs(cur_mean - ref_mean) / (ref_std or 1)
        std_ratio = cur_std / (ref_std or 1)
        drift_score = min(1.0, (mean_shift + abs(1 - std_ratio)) / 2)
        if drift_score > 0.5:
            severity = AlertSeverity.HIGH
        elif drift_score > 0.3:
            severity = AlertSeverity.MEDIUM
        else:
            severity = AlertSeverity.LOW
        alert = DriftAlert(
            model_id=model_id,
            drift_type=DriftType.DATA_DRIFT,
            severity=severity,
            detection_score=round(drift_score, 3),
            message=f"Drift score: {drift_score:.3f}, mean shift: {mean_shift:.3f}",
        )
        self._alerts.append(alert)
        logger.warning("Drift detected for model %s: score=%.3f", model_id, drift_score)
        return alert

    def evaluate_performance(self, model_id: str) -> Dict[str, Any]:
        preds = self._predictions.get(model_id, [])
        baseline = self._baseline_metrics.get(model_id, {})
        correct = sum(1 for p in preds if p["actual"] is not None and p["prediction"] == p["actual"])
        total_with_actual = sum(1 for p in preds if p["actual"] is not None)
        current_accuracy = correct / total_with_actual if total_with_actual > 0 else 0
        baseline_accuracy = baseline.get("accuracy", 0)
        degradation = current_accuracy - baseline_accuracy
        return {
            "model_id": model_id,
            "current_accuracy": round(current_accuracy, 4),
            "baseline_accuracy": baseline_accuracy,
            "degradation": round(degradation, 4),
            "needs_retraining": degradation < -0.05,
            "total_evaluated": total_with_actual,
        }

    def get_alerts(self, model_id: Optional[str] = None) -> List[DriftAlert]:
        alerts = self._alerts
        if model_id:
            alerts = [a for a in alerts if a.model_id == model_id]
        return alerts

    def _std_dev(self, values: List[float]) -> float:
        if len(values) < 2:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        return math.sqrt(variance)


# ──────────────────────────────────────────────
# A/B Test Manager
# ──────────────────────────────────────────────

class ABTestManager:
    """Create, manage, and evaluate A/B tests for ML models."""

    def __init__(self) -> None:
        self._tests: Dict[str, ABTest] = {}

    def create_test(
        self,
        name: str,
        variant_configs: List[Dict[str, Any]],
    ) -> ABTest:
        test = ABTest(name=name)
        for vc in variant_configs:
            variant = ABVariant(
                variant_id=vc.get("variant_id", f"v_{len(test.variants)}"),
                model_id=vc.get("model_id", ""),
                traffic_percentage=vc.get("traffic_percentage", 50.0),
            )
            test.variants.append(variant)
        self._tests[test.test_id] = test
        logger.info("Created A/B test %s (%s)", test.test_id, name)
        return test

    def start_test(self, test_id: str) -> ABTest:
        test = self._get_test(test_id)
        total_traffic = sum(v.traffic_percentage for v in test.variants)
        if abs(total_traffic - 100) > 0.01:
            raise MLOpsError(f"Traffic percentages must sum to 100, got {total_traffic}")
        test.status = ABTestStatus.RUNNING
        test.start_date = datetime.now()
        return test

    def record_outcome(
        self, test_id: str, variant_id: str, metrics: Dict[str, float], sample_size: int = 1
    ) -> None:
        test = self._get_test(test_id)
        for v in test.variants:
            if v.variant_id == variant_id:
                for key, val in metrics.items():
                    existing = v.metrics.get(key, 0)
                    v.metrics[key] = (existing * v.sample_size + val * sample_size) / (v.sample_size + sample_size) if v.sample_size + sample_size > 0 else val
                v.sample_size += sample_size
                break

    def evaluate_test(self, test_id: str) -> Dict[str, Any]:
        test = self._get_test(test_id)
        if not test.variants:
            return {"error": "No variants"}
        best_variant = None
        best_score = -1
        for v in test.variants:
            score = v.metrics.get("conversion_rate", v.metrics.get("accuracy", 0))
            if score > best_score:
                best_score = score
                best_variant = v.variant_id
        control = test.variants[0]
        treatment = test.variants[1] if len(test.variants) > 1 else None
        uplift = 0
        if treatment and control.sample_size > 0 and treatment.sample_size > 0:
            control_rate = control.metrics.get("conversion_rate", 0)
            treatment_rate = treatment.metrics.get("conversion_rate", 0)
            uplift = ((treatment_rate - control_rate) / control_rate * 100) if control_rate > 0 else 0
        test.winning_variant = best_variant
        test.confidence = min(1.0, min(control.sample_size, treatment.sample_size if treatment else 0) / 1000) if treatment else 0.5
        return {
            "test_id": test_id,
            "winning_variant": best_variant,
            "confidence": test.confidence,
            "uplift_percent": round(uplift, 2),
            "variants": [
                {"id": v.variant_id, "sample_size": v.sample_size, "metrics": v.metrics}
                for v in test.variants
            ],
        }

    def complete_test(self, test_id: str) -> ABTest:
        test = self._get_test(test_id)
        test.status = ABTestStatus.COMPLETED
        test.end_date = datetime.now()
        return test

    def get_test(self, test_id: str) -> ABTest:
        return self._get_test(test_id)

    def list_tests(self) -> List[ABTest]:
        return list(self._tests.values())

    def _get_test(self, test_id: str) -> ABTest:
        if test_id not in self._tests:
            raise MLOpsError(f"A/B test {test_id} not found")
        return self._tests[test_id]


# ──────────────────────────────────────────────
# Deployment Manager
# ──────────────────────────────────────────────

class DeploymentManager:
    """Deploy, scale, and manage model endpoints."""

    def __init__(self) -> None:
        self._deployments: Dict[str, DeploymentRecord] = {}

    def deploy(
        self,
        model_id: str,
        environment: DeploymentEnvironment,
        replicas: int = 1,
        resources: Optional[Dict[str, Any]] = None,
    ) -> DeploymentRecord:
        record = DeploymentRecord(
            model_id=model_id,
            environment=environment,
            endpoint=f"https://api.example.com/v1/predict/{model_id}",
            replicas=replicas,
            resources=resources or {"cpu": "1", "memory": "2Gi"},
            status="deployed",
            deployed_at=datetime.now(),
        )
        self._deployments[record.deployment_id] = record
        logger.info("Deployed model %s to %s", model_id, environment.value)
        return record

    def scale(self, deployment_id: str, replicas: int) -> DeploymentRecord:
        record = self._get_deployment(deployment_id)
        record.replicas = replicas
        return record

    def rollback(self, deployment_id: str, previous_model_id: str) -> DeploymentRecord:
        record = self._get_deployment(deployment_id)
        record.model_id = previous_model_id
        record.deployed_at = datetime.now()
        logger.info("Rolled back deployment %s to model %s", deployment_id, previous_model_id)
        return record

    def get_deployment(self, deployment_id: str) -> DeploymentRecord:
        return self._get_deployment(deployment_id)

    def list_deployments(self, environment: Optional[DeploymentEnvironment] = None) -> List[DeploymentRecord]:
        deps = list(self._deployments.values())
        if environment:
            deps = [d for d in deps if d.environment == environment]
        return deps

    def _get_deployment(self, deployment_id: str) -> DeploymentRecord:
        if deployment_id not in self._deployments:
            raise DeploymentError(f"Deployment {deployment_id} not found")
        return self._deployments[deployment_id]


# ──────────────────────────────────────────────
# MLOps Agent (orchestrator)
# ──────────────────────────────────────────────

class MLOpsAgent:
    """Top-level orchestrator for all MLOps operations."""

    def __init__(self) -> None:
        self.registry = ModelRegistry()
        self.pipelines = PipelineManager()
        self.features = FeatureStore()
        self.experiments = ExperimentTracker()
        self.monitor = ModelMonitor()
        self.ab_tests = ABTestManager()
        self.deployments = DeploymentManager()
        logger.info("MLOpsAgent initialized")

    def train_and_deploy(
        self,
        model_name: str,
        version: str,
        framework: str,
        task: str,
        environment: DeploymentEnvironment = DeploymentEnvironment.STAGING,
    ) -> Dict[str, Any]:
        model = self.registry.register_model(model_name, version, framework, task)
        pipeline = self.pipelines.create_pipeline(
            name=f"pipeline_{model_name}",
            model_name=model_name,
            steps_config=[
                {"name": "preprocess", "stage": "preprocessing"},
                {"name": "train", "stage": "training"},
                {"name": "evaluate", "stage": "evaluation"},
            ],
        )
        run = self.pipelines.execute_pipeline(pipeline.pipeline_id)
        self.registry.update_model(model.model_id, status=ModelStatus.TRAINED, metrics=run.metrics)
        deployment = self.registry.promote_model(model.model_id, environment)
        self.registry.update_model(model.model_id, status=ModelStatus.DEPLOYED)
        self.monitor.set_baseline(model.model_id, run.metrics)
        return {
            "model_id": model.model_id,
            "pipeline_id": pipeline.pipeline_id,
            "run_id": run.run_id,
            "deployment": deployment.deployment_id,
            "metrics": run.metrics,
        }


# ──────────────────────────────────────────────
# CLI entry point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    agent = MLOpsAgent()

    result = agent.train_and_deploy(
        model_name="fraud_detector",
        version="v2.1.0",
        framework="sklearn",
        task="classification",
        environment=DeploymentEnvironment.STAGING,
    )
    print(f"Model deployed: {result['model_id']}")
    print(f"Metrics: {result['metrics']}")

    feature = agent.features.register_feature("user_age", "int", "users", "User age")
    agent.features.ingest_value("user_age", "user_1", 30)
    agent.features.ingest_value("user_age", "user_2", 25)
    stats = agent.features.compute_features("user_age", ["user_1", "user_2"])
    print(f"Feature stats: {stats}")

    exp = agent.experiments.create_experiment("fraud_v2_tuning")
    agent.experiments.log_run(exp.experiment_id, "fraud_detector", {"lr": 0.001}, {"accuracy": 0.92})
    agent.experiments.log_run(exp.experiment_id, "fraud_detector", {"lr": 0.01}, {"accuracy": 0.89})
    comparison = agent.experiments.compare_runs(exp.experiment_id)
    print(f"Best accuracy: {comparison['best_per_metric']['accuracy']}")

    test = agent.ab_tests.create_test("fraud_v2_test", [
        {"variant_id": "control", "model_id": "model_old", "traffic_percentage": 50},
        {"variant_id": "treatment", "model_id": result["model_id"], "traffic_percentage": 50},
    ])
    agent.ab_tests.start_test(test.test_id)
    agent.ab_tests.record_outcome(test.test_id, "control", {"accuracy": 0.88}, 1000)
    agent.ab_tests.record_outcome(test.test_id, "treatment", {"accuracy": 0.92}, 1000)
    evaluation = agent.ab_tests.evaluate_test(test.test_id)
    print(f"A/B test winner: {evaluation['winning_variant']}, uplift: {evaluation['uplift_percent']}%")

    health = agent.monitor.check_health(result["model_id"])
    print(f"Health: {health['status']}, latency: {health['avg_latency_ms']}ms")
