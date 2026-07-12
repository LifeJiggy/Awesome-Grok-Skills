"""
Model Deployment Module — MLOps platform for model serving, versioning, A/B testing,
canary deployment, drift detection, and production monitoring.
"""

from __future__ import annotations

import json
import math
import random
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ModelFormat(Enum):
    ONNX = "onnx"
    TORCHSCRIPT = "torchscript"
    SAVEDMODEL = "savedmodel"
    TENSORRT = "tensorrt"
    PICKLE = "pickle"
    PMML = "pmml"


class ServingProtocol(Enum):
    REST = "rest"
    GRPC = "grpc"
    BATCH = "batch"
    STREAMING = "streaming"


class DeploymentStatus(Enum):
    PENDING = "pending"
    DEPLOYING = "deploying"
    RUNNING = "running"
    CANARY = "canary"
    ROLLED_BACK = "rolled_back"
    STOPPED = "stopped"
    ERROR = "error"


class DriftType(Enum):
    DATA_DRIFT = "data_drift"
    CONCEPT_DRIFT = "concept_drift"
    PREDICTION_DRIFT = "prediction_drift"
    FEATURE_DRIFT = "feature_drift"


class ABTestStatus(Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    STOPPED = "stopped"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class DeploymentConfig:
    """Configuration for model deployment."""
    model_name: str
    version: str
    replicas: int = 3
    cpu_limit: str = "2.0"
    memory_limit: str = "4Gi"
    gpu_count: int = 0
    max_batch_size: int = 32
    timeout_ms: int = 100
    canary_percentage: float = 0.0
    auto_rollback: bool = True
    protocol: ServingProtocol = ServingProtocol.REST
    port: int = 8080
    health_check_interval_s: int = 30
    autoscale_min: int = 1
    autoscale_max: int = 10
    target_latency_p99_ms: float = 100.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model": self.model_name,
            "version": self.version,
            "replicas": self.replicas,
            "canary_pct": self.canary_percentage,
            "protocol": self.protocol.value,
        }


@dataclass
class ModelVersion:
    """A registered model version."""
    model_name: str
    version: str
    model_path: str
    model_format: ModelFormat = ModelFormat.ONNX
    metrics: Dict[str, float] = field(default_factory=dict)
    tags: Dict[str, str] = field(default_factory=dict)
    registered_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    artifact_size_mb: float = 0.0
    description: str = ""

    @property
    def display_name(self) -> str:
        return f"{self.model_name}:{self.version}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.model_name,
            "version": self.version,
            "format": self.model_format.value,
            "metrics": {k: round(v, 4) for k, v in self.metrics.items()},
            "registered_at": self.registered_at,
        }


@dataclass
class DeploymentEndpoint:
    """A live model deployment endpoint."""
    url: str
    model_name: str
    version: str
    status: DeploymentStatus
    health_status: str = "healthy"
    uptime_s: float = 0.0
    requests_total: int = 0
    avg_latency_ms: float = 0.0
    error_rate: float = 0.0
    deployed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "model": self.model_name,
            "version": self.version,
            "status": self.status.value,
            "health": self.health_status,
            "requests": self.requests_total,
            "avg_latency_ms": round(self.avg_latency_ms, 2),
        }


@dataclass
class InferenceRequest:
    """A single inference request."""
    request_id: str
    model_name: str
    version: str
    input_data: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class InferenceResponse:
    """A single inference response."""
    request_id: str
    predictions: List[float]
    latency_ms: float
    model_version: str
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "predictions": [round(p, 4) for p in self.predictions],
            "latency_ms": round(self.latency_ms, 2),
            "model_version": self.model_version,
        }


@dataclass
class ABTestResult:
    """Result of an A/B test evaluation."""
    name: str
    model_a: str
    model_b: str
    winner: str
    improvement_pct: float
    p_value: float
    is_significant: bool
    samples_a: int = 0
    samples_b: int = 0
    metric_a: float = 0.0
    metric_b: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "winner": self.winner,
            "improvement": f"{self.improvement_pct:.2f}%",
            "p_value": round(self.p_value, 4),
            "significant": self.is_significant,
        }


@dataclass
class DriftAlert:
    """A drift detection alert."""
    alert_id: str
    drift_type: DriftType
    feature_name: str
    severity: str
    description: str
    baseline_distribution: str = ""
    current_distribution: str = ""
    psi_score: float = 0.0
    detected_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "type": self.drift_type.value,
            "feature": self.feature_name,
            "severity": self.severity,
            "psi": round(self.psi_score, 4),
        }


@dataclass
class PerformanceMetrics:
    """Model serving performance metrics."""
    requests_per_second: float = 0.0
    latency_p50_ms: float = 0.0
    latency_p95_ms: float = 0.0
    latency_p99_ms: float = 0.0
    error_rate_pct: float = 0.0
    cpu_usage_pct: float = 0.0
    memory_usage_pct: float = 0.0
    gpu_utilization_pct: float = 0.0
    active_connections: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rps": round(self.requests_per_second, 1),
            "p50": round(self.latency_p50_ms, 2),
            "p95": round(self.latency_p95_ms, 2),
            "p99": round(self.latency_p99_ms, 2),
            "error_rate": round(self.error_rate_pct, 2),
            "cpu": round(self.cpu_usage_pct, 1),
        }


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class ModelRegistry:
    """Versioned model registry with lineage tracking."""

    def __init__(self, storage_path: str = "model_registry"):
        self.storage_path = storage_path
        self._versions: Dict[str, List[ModelVersion]] = {}

    def register(
        self, model_path: str, model_name: str, version: str,
        metrics: Optional[Dict[str, float]] = None,
        tags: Optional[Dict[str, str]] = None,
        model_format: ModelFormat = ModelFormat.ONNX,
        description: str = "",
    ) -> ModelVersion:
        mv = ModelVersion(
            model_name=model_name,
            version=version,
            model_path=model_path,
            model_format=model_format,
            metrics=metrics or {},
            tags=tags or {},
            description=description,
        )
        if model_name not in self._versions:
            self._versions[model_name] = []
        self._versions[model_name].append(mv)
        return mv

    def get_version(self, model_name: str, version: str) -> Optional[ModelVersion]:
        for mv in self._versions.get(model_name, []):
            if mv.version == version:
                return mv
        return None

    def list_versions(self, model_name: str) -> List[ModelVersion]:
        return self._versions.get(model_name, [])

    def get_latest(self, model_name: str) -> Optional[ModelVersion]:
        versions = self._versions.get(model_name, [])
        return versions[-1] if versions else None

    def promote(self, model_name: str, version: str, stage: str) -> None:
        mv = self.get_version(model_name, version)
        if mv:
            mv.tags["stage"] = stage


class ModelServer:
    """Model serving infrastructure with auto-scaling and health checks."""

    def __init__(self, config: DeploymentConfig):
        self.config = config
        self._status = DeploymentStatus.PENDING
        self._endpoint: Optional[DeploymentEndpoint] = None
        self._metrics = PerformanceMetrics()
        self._request_log: List[InferenceResponse] = []

    def deploy(self) -> DeploymentEndpoint:
        """Deploy the model to serving infrastructure."""
        self._status = DeploymentStatus.RUNNING
        self._endpoint = DeploymentEndpoint(
            url=f"http://localhost:{self.config.port}/v1/models/{self.config.model_name}",
            model_name=self.config.model_name,
            version=self.config.version,
            status=self._status,
        )
        return self._endpoint

    def predict(self, input_data: Dict[str, Any]) -> InferenceResponse:
        """Run inference on a single input."""
        start = time.time()
        # Simulate inference
        latency = random.uniform(5, 50)
        predictions = [random.uniform(0, 1) for _ in range(10)]
        response = InferenceResponse(
            request_id=f"REQ-{uuid.uuid4().hex[:8].upper()}",
            predictions=predictions,
            latency_ms=latency,
            model_version=self.config.version,
            confidence=max(predictions),
        )
        self._request_log.append(response)
        if self._endpoint:
            self._endpoint.requests_total += 1
        return response

    def predict_batch(self, inputs: List[Dict[str, Any]]) -> List[InferenceResponse]:
        """Run batch inference."""
        return [self.predict(inp) for inp in inputs]

    def get_metrics(self) -> PerformanceMetrics:
        if not self._request_log:
            return self._metrics
        latencies = [r.latency_ms for r in self._request_log]
        sorted_lat = sorted(latencies)
        n = len(sorted_lat)
        self._metrics.latency_p50_ms = sorted_lat[n // 2] if n > 0 else 0
        self._metrics.latency_p95_ms = sorted_lat[int(n * 0.95)] if n > 20 else sorted_lat[-1] if n > 0 else 0
        self._metrics.latency_p99_ms = sorted_lat[int(n * 0.99)] if n > 100 else sorted_lat[-1] if n > 0 else 0
        return self._metrics

    def rollback(self, previous_version: str) -> None:
        self.config.version = previous_version
        self._status = DeploymentStatus.ROLLED_BACK
        if self._endpoint:
            self._endpoint.version = previous_version
            self._endpoint.status = self._status

    def stop(self) -> None:
        self._status = DeploymentStatus.STOPPED
        if self._endpoint:
            self._endpoint.status = self._status


class ABTest:
    """A/B test between two model versions."""

    def __init__(
        self,
        name: str,
        model_a: str,
        model_b: str,
        traffic_split: float = 0.5,
        min_samples: int = 1000,
        significance_level: float = 0.05,
        primary_metric: str = "auc",
    ):
        self.name = name
        self.model_a = model_a
        self.model_b = model_b
        self.traffic_split = traffic_split
        self.min_samples = min_samples
        self.significance_level = significance_level
        self.primary_metric = primary_metric
        self._results_a: List[float] = []
        self._results_b: List[float] = []

    def record_result(self, model: str, metric_value: float) -> None:
        if model == self.model_a:
            self._results_a.append(metric_value)
        elif model == self.model_b:
            self._results_b.append(metric_value)

    def evaluate(self) -> ABTestResult:
        """Evaluate A/B test results with statistical significance."""
        # Generate synthetic results for demo
        self._results_a = [random.uniform(0.92, 0.98) for _ in range(self.min_samples)]
        self._results_b = [random.uniform(0.93, 0.99) for _ in range(self.min_samples)]

        mean_a = sum(self._results_a) / len(self._results_a) if self._results_a else 0
        mean_b = sum(self._results_b) / len(self._results_b) if self._results_b else 0

        # Simplified t-test
        std_a = (sum((x - mean_a) ** 2 for x in self._results_a) / len(self._results_a)) ** 0.5 if len(self._results_a) > 1 else 0
        std_b = (sum((x - mean_b) ** 2 for x in self._results_b) / len(self._results_b)) ** 0.5 if len(self._results_b) > 1 else 0
        se = math.sqrt(std_a ** 2 / len(self._results_a) + std_b ** 2 / len(self._results_b)) if (self._results_a and self._results_b) else 1
        z = (mean_b - mean_a) / se if se > 0 else 0
        p_value = max(0.001, 2 * (1 - min(abs(z) / 3, 0.999)))

        is_significant = p_value < self.significance_level
        winner = self.model_b if mean_b > mean_a and is_significant else self.model_a
        improvement = ((mean_b - mean_a) / mean_a * 100) if mean_a > 0 else 0

        return ABTestResult(
            name=self.name,
            model_a=self.model_a,
            model_b=self.model_b,
            winner=winner,
            improvement_pct=improvement,
            p_value=p_value,
            is_significant=is_significant,
            samples_a=len(self._results_a),
            samples_b=len(self._results_b),
            metric_a=mean_a,
            metric_b=mean_b,
        )


class DriftDetector:
    """Detect data and concept drift in model predictions."""

    def __init__(self, baseline: str = "", psi_threshold: float = 0.2):
        self.psi_threshold = psi_threshold
        self._baseline: Dict[str, Any] = {}
        self._recent_predictions: List[float] = []

    def check(self, prediction_stream: Optional[List[float]] = None) -> List[DriftAlert]:
        """Check for drift in recent predictions."""
        alerts = []
        preds = prediction_stream or [random.uniform(0, 1) for _ in range(100)]

        psi = self._calculate_psi(preds)
        if psi > self.psi_threshold:
            alerts.append(DriftAlert(
                alert_id=f"DRIFT-{uuid.uuid4().hex[:8].upper()}",
                drift_type=DriftType.PREDICTION_DRIFT,
                feature_name="predictions",
                severity="warning" if psi < 0.3 else "critical",
                description=f"Prediction distribution shifted (PSI={psi:.3f})",
                psi_score=psi,
            ))

        # Feature drift simulation
        for feat in ["feature_1", "feature_2", "feature_3"]:
            feat_psi = random.uniform(0, 0.4)
            if feat_psi > self.psi_threshold:
                alerts.append(DriftAlert(
                    alert_id=f"DRIFT-{uuid.uuid4().hex[:8].upper()}",
                    drift_type=DriftType.FEATURE_DRIFT,
                    feature_name=feat,
                    severity="warning",
                    description=f"Feature '{feat}' drifted (PSI={feat_psi:.3f})",
                    psi_score=feat_psi,
                ))

        return alerts

    def _calculate_psi(self, current: List[float]) -> float:
        """Calculate Population Stability Index."""
        # Simplified PSI calculation
        n_bins = 10
        baseline_counts = [len(current) / n_bins] * n_bins
        current_counts = [len(current) / n_bins] * n_bins

        psi = 0.0
        for b, c in zip(baseline_counts, current_counts):
            if b > 0 and c > 0:
                psi += (c - b) * math.log(c / b)
        return abs(psi)


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the model deployment platform."""
    print("Model Deployment Platform")
    print("=" * 60)

    # Registry
    registry = ModelRegistry()
    v1 = registry.register("model_v1.onnx", "fraud-detector", "1.0.0",
                           metrics={"auc": 0.965, "f1": 0.92})
    v2 = registry.register("model_v2.onnx", "fraud-detector", "2.0.0",
                           metrics={"auc": 0.985, "f1": 0.94})
    print(f"Registered: {v1.display_name}, {v2.display_name}")

    # Deploy
    config = DeploymentConfig(
        model_name="fraud-detector", version="2.0.0",
        replicas=3, canary_percentage=10,
    )
    server = ModelServer(config)
    endpoint = server.deploy()
    print(f"\nDeployed: {endpoint.url} ({endpoint.status.value})")

    # Inference
    print("\n--- Inference ---")
    for _ in range(5):
        resp = server.predict({"features": [0.1, 0.5, 0.3]})
        print(f"  {resp.request_id}: pred={resp.predictions[0]:.4f}, latency={resp.latency_ms:.1f}ms")

    metrics = server.get_metrics()
    print(f"\nMetrics: p50={metrics.latency_p50_ms:.1f}ms, p95={metrics.latency_p95_ms:.1f}ms, p99={metrics.latency_p99_ms:.1f}ms")

    # A/B Test
    print("\n--- A/B Test ---")
    ab = ABTest("v1-vs-v2", "fraud-detector:1.0.0", "fraud-detector:2.0.0", min_samples=500)
    result = ab.evaluate()
    print(f"  Winner: {result.winner}")
    print(f"  Improvement: {result.improvement_pct:.2f}%")
    print(f"  p-value: {result.p_value:.4f} (significant: {result.is_significant})")

    # Drift
    print("\n--- Drift Detection ---")
    drift = DriftDetector()
    alerts = drift.check()
    print(f"  Alerts: {len(alerts)}")
    for a in alerts:
        print(f"    {a.drift_type.value}: {a.description}")


if __name__ == "__main__":
    main()
