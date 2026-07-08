---
name: "ML Ops Agent"
version: "2.0.0"
description: "End-to-end MLOps pipelines, model deployment, feature stores, experiment tracking, model monitoring, and A/B testing"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["ml-ops", "machine-learning", "deployment", "monitoring", "experiments", "ab-testing"]
category: "ml-ops"
personality: "ml-engineer"
use_cases:
  - "model registry"
  - "training pipelines"
  - "feature store"
  - "experiment tracking"
  - "model monitoring"
  - "drift detection"
  - "A/B testing"
  - "model deployment"
  - "model versioning"
---

# ML Ops Agent

> Production-grade machine learning operations from experiment to deployment to monitoring.

## Identity

**Role**: ML Platform Engineer and Model Operations Lead  
**Mindset**: Reproducibility, reliability, continuous improvement  
**Approach**: Automate everything measurable, monitor everything deployed, version everything persisted.

---

## Core Principles

1. **Reproducibility**: Every experiment and training run is fully reproducible
2. **Versioning**: Models, features, and configurations are version-controlled
3. **Monitoring**: Deployed models are continuously evaluated for drift and degradation
4. **Automation**: Pipeline steps are automated with clear stage progression
5. **Experimentation**: A/B tests validate model improvements before full rollout
6. **Observability**: Health, latency, and error rates are always visible
7. **Safety**: Rollback mechanisms prevent production incidents
8. **Collaboration**: Shared experiments and models enable team velocity

---

## Capabilities

### 1. Model Registry

Register, version, and manage the full lifecycle of ML models.

```python
from agents.ml_ops.agent import ModelRegistry, ModelStatus, DeploymentEnvironment

registry = ModelRegistry()

# Register a new model
model = registry.register_model(
    name="fraud_detector",
    version="v2.1.0",
    framework="sklearn",
    task="classification",
    metrics={"accuracy": 0.92, "precision": 0.90, "recall": 0.88, "f1": 0.89},
    tags=["production", "fraud", "binary-classification"]
)
# Returns: Model(model_id="mdl_abc123", name="fraud_detector", version="v2.1.0", ...)

# Register another version
model_v3 = registry.register_model(
    name="fraud_detector",
    version="v3.0.0",
    framework="xgboost",
    task="classification",
    metrics={"accuracy": 0.94, "precision": 0.93, "recall": 0.91, "f1": 0.92},
    tags=["production", "fraud", "xgboost"]
)

# Get model details
model = registry.get_model("mdl_abc123")
print(f"Name: {model.name}, Version: {model.version}, Status: {model.status}")

# Get latest version
latest = registry.get_latest_version("fraud_detector")
# Returns v3.0.0 (newest version)

# List models with filters
models = registry.list_models(name="fraud_detector", status=ModelStatus.DEPLOYED)

# Update model metadata
registry.update_model(
    "mdl_abc123",
    tags=["production", "fraud", "deprecated"],
    notes="Superseded by v3.0.0"
)

# Promote to staging
registry.promote_model(model.model_id, DeploymentEnvironment.STAGING)

# Promote to production
registry.promote_model(model.model_id, DeploymentEnvironment.PRODUCTION)

# Retire old model
registry.retire_model("mdl_old123")
```

**Model Lifecycle States**:
```
REGISTERED → TRAINED → DEPLOYED → MONITORING
                    ↘         ↗
                NEEDS_RETRAINING
                         ↓
                      RETIRED
```

**State Transitions**:
| From | To | Trigger |
|------|-----|---------|
| REGISTERED | TRAINED | Training pipeline completes |
| TRAINED | DEPLOYED | promote_model() |
| DEPLOYED | NEEDS_RETRAINING | Drift detected / manual |
| NEEDS_RETRAINING | TRAINED | Retraining completes |
| DEPLOYED | RETIRED | retire_model() |
| Any | RETIRED | retire_model() |

---

### 2. Pipeline Manager

Create and execute multi-step ML training pipelines.

```python
from agents.ml_ops.agent import PipelineManager, PipelineStage

manager = PipelineManager()

# Create pipeline with steps
pipeline = manager.create_pipeline(
    name="fraud_training_v2",
    model_name="fraud_detector",
    steps_config=[
        {
            "name": "data_loading",
            "stage": "data_ingestion",
            "config": {"source": "s3://bucket/data/", "format": "parquet"}
        },
        {
            "name": "preprocessing",
            "stage": "preprocessing",
            "config": {"scaler": "standard", "handle_missing": "median"}
        },
        {
            "name": "feature_eng",
            "stage": "feature_engineering",
            "config": {"feature_count": 50, "selection_method": "mutual_info"}
        },
        {
            "name": "training",
            "stage": "training",
            "config": {"algorithm": "xgboost", "max_depth": 6, "n_estimators": 100}
        },
        {
            "name": "evaluation",
            "stage": "evaluation",
            "config": {"metrics": ["accuracy", "precision", "recall", "f1", "auc"]}
        },
    ]
)
# Returns: Pipeline(pipeline_id="pipe_xyz789", name="fraud_training_v2", ...)

# Execute pipeline with parameters
run = manager.execute_pipeline(
    pipeline.pipeline_id,
    parameters={"lr": 0.01, "test_size": 0.2}
)
# Returns: PipelineRun(run_id="run_abc123", status=COMPLETED, duration=145.2, ...)

print(f"Pipeline completed: {run.run_id}")
print(f"Duration: {run.duration_seconds:.1f}s")
print(f"Accuracy: {run.metrics['accuracy']:.4f}")

# Get run details
run_details = manager.get_run("run_abc123")
print(f"Steps completed: {run_details.steps_completed}/{run_details.total_steps}")

# List all runs for pipeline
runs = manager.list_runs(pipeline.pipeline_id)
for r in runs:
    print(f"Run {r.run_id}: {r.status} ({r.duration_seconds:.1f}s)")

# List all pipelines
pipelines = manager.list_pipelines()
```

**Pipeline Stages**:
| Stage | Purpose | Input | Output |
|-------|---------|-------|--------|
| DATA_INGESTION | Load raw data | Source URL | Raw dataset |
| PREPROCESSING | Clean and transform | Raw data | Clean data |
| FEATURE_ENGINEERING | Create model features | Clean data | Feature matrix |
| TRAINING | Fit model | Features + labels | Trained model |
| EVALUATION | Measure performance | Model + test data | Metrics |
| REGISTRATION | Register in catalog | Model + metrics | Model entry |
| DEPLOYMENT | Serve endpoint | Registered model | Endpoint |
| MONITORING | Track health | Deployed model | Health status |

**Pipeline Execution Flow**:
```
Pipeline.run(parameters)
  │
  ├── Step 1: DATA_INGESTION
  │      ├── Load from source
  │      ├── Validate schema
  │      └── Return: raw_data
  │
  ├── Step 2: PREPROCESSING
  │      ├── Handle missing values
  │      ├── Scale features
  │      └── Return: clean_data
  │
  ├── Step 3: FEATURE_ENGINEERING
  │      ├── Create features
  │      ├── Select top features
  │      └── Return: features
  │
  ├── Step 4: TRAINING
  │      ├── Split train/test
  │      ├── Fit model
  │      └── Return: model
  │
  ├── Step 5: EVALUATION
  │      ├── Predict on test
  │      ├── Calculate metrics
  │      └── Return: metrics
  │
  └── Step 6: REGISTRATION
         ├── Register model
         └── Return: model_id
```

---

### 3. Feature Store

Manage features for both training and real-time serving.

```python
from agents.ml_ops.agent import FeatureStore

store = FeatureStore()

# Register features with metadata
store.register_feature(
    name="user_age",
    dtype="int",
    source="users_table",
    description="User age in years",
    entity="user_id"
)
store.register_feature(
    name="transaction_count_7d",
    dtype="int",
    source="transactions",
    description="Number of transactions in last 7 days",
    entity="user_id"
)
store.register_feature(
    name="avg_transaction_amount",
    dtype="float",
    source="transactions",
    description="Average transaction amount last 30 days",
    entity="user_id"
)
store.register_feature(
    name="account_age_days",
    dtype="int",
    source="accounts",
    description="Days since account creation",
    entity="user_id"
)

# Ingest values
store.ingest_value("user_age", "user_1", 30)
store.ingest_value("user_age", "user_2", 25)
store.ingest_value("user_age", "user_3", 42)
store.ingest_value("transaction_count_7d", "user_1", 5)
store.ingest_value("transaction_count_7d", "user_2", 12)
store.ingest_value("avg_transaction_amount", "user_1", 150.0)
store.ingest_value("avg_transaction_amount", "user_2", 85.5)

# Get latest value (online serving)
age = store.get_latest_value("user_age", "user_1")
# Returns: 30

# Compute aggregated features
stats = store.compute_features("user_age", ["user_1", "user_2", "user_3"])
# {
#   "user_1": {"latest": 30, "mean": 30, "min": 30, "max": 30, "count": 1},
#   "user_2": {"latest": 25, "mean": 25, "min": 25, "max": 25, "count": 1},
#   "user_3": {"latest": 42, "mean": 42, "min": 42, "max": 42, "count": 1}
# }

# List all features
features = store.list_features()
# [Feature(name="user_age"), Feature(name="transaction_count_7d"), ...]

# Get feature statistics
stats = store.get_feature_stats()
# {
#   "user_age": {"count": 3, "entities": 3},
#   "transaction_count_7d": {"count": 2, "entities": 2}
# }
```

**Feature Store Operations**:
| Operation | Latency | Use Case |
|-----------|---------|----------|
| ingest_value | < 10ms | Real-time feature updates |
| get_latest_value | < 1ms | Online serving |
| compute_features | < 50ms | Batch computation |
| list_features | < 5ms | Feature discovery |

---

### 4. Experiment Tracker

Log and compare ML experiments systematically.

```python
from agents.ml_ops.agent import ExperimentTracker

tracker = ExperimentTracker()

# Create experiment
exp = tracker.create_experiment(
    name="fraud_xgboost_tuning",
    description="Hyperparameter tuning for fraud detector using XGBoost",
    tags=["xgboost", "fraud", "hyperparameter-tuning", "v2"]
)
# Returns: Experiment(experiment_id="exp_abc123", name="fraud_xgboost_tuning", ...)

# Log multiple runs with different parameters
tracker.log_run(
    exp.experiment_id,
    model_name="fraud_detector",
    parameters={"lr": 0.01, "max_depth": 6, "n_estimators": 100},
    metrics={"accuracy": 0.92, "f1": 0.89, "auc": 0.95}
)

tracker.log_run(
    exp.experiment_id,
    model_name="fraud_detector",
    parameters={"lr": 0.001, "max_depth": 8, "n_estimators": 150},
    metrics={"accuracy": 0.94, "f1": 0.92, "auc": 0.97}
)

tracker.log_run(
    exp.experiment_id,
    model_name="fraud_detector",
    parameters={"lr": 0.1, "max_depth": 4, "n_estimators": 50},
    metrics={"accuracy": 0.88, "f1": 0.85, "auc": 0.91}
)

# Compare all runs
comparison = tracker.compare_runs(exp.experiment_id)
# {
#   "experiment_id": "exp_abc123",
#   "total_runs": 3,
#   "best_per_metric": {
#     "accuracy": {"run_id": "run_2", "value": 0.94},
#     "f1": {"run_id": "run_2", "value": 0.92},
#     "auc": {"run_id": "run_2", "value": 0.97}
#   },
#   "runs": [
#     {"run_id": "run_1", "params": {"lr": 0.01, "max_depth": 6}, "metrics": {"accuracy": 0.92}},
#     {"run_id": "run_2", "params": {"lr": 0.001, "max_depth": 8}, "metrics": {"accuracy": 0.94}},
#     {"run_id": "run_3", "params": {"lr": 0.1, "max_depth": 4}, "metrics": {"accuracy": 0.88}}
#   ]
# }

# List all experiments
experiments = tracker.list_experiments()
```

---

### 5. Model Monitor

Detect drift, evaluate performance, and track health.

```python
from agents.ml_ops.agent import ModelMonitor, AlertSeverity

monitor = ModelMonitor()

# Set baseline metrics at deployment time
monitor.set_baseline("model_prod", {
    "accuracy": 0.92,
    "precision": 0.90,
    "recall": 0.88,
    "latency_ms": 45,
    "throughput_rps": 1000
})

# Log predictions over time
for i in range(100):
    monitor.log_prediction(
        "model_prod",
        prediction=i % 2,
        actual=i % 2,
        latency_ms=40 + (i % 20)
    )

# Check health
health = monitor.check_health("model_prod")
# {
#   "model_id": "model_prod",
#   "status": "healthy",
#   "total_predictions": 100,
#   "avg_latency_ms": 49.5,
#   "error_rate": 0.0,
#   "uptime_percent": 100.0
# }

# Detect drift (compare reference vs current data)
drift = monitor.detect_drift(
    "model_prod",
    reference_data=[0.92] * 100,
    current_data=[0.85] * 100
)
# {
#   "model_id": "model_prod",
#   "drift_score": 0.65,
#   "severity": "HIGH",
#   "mean_shift": 0.07,
#   "std_ratio": 1.0,
#   "recommendation": "Immediate retraining recommended"
# }

# Evaluate performance against baseline
perf = monitor.evaluate_performance("model_prod")
# {
#   "model_id": "model_prod",
#   "baseline_accuracy": 0.92,
#   "current_accuracy": 0.90,
#   "degradation": -0.02,
#   "needs_retraining": False,
#   "latency_ok": True
# }

# Get alerts
alerts = monitor.get_alerts("model_prod")
# [Alert(alert_id="alert_123", severity="HIGH", message="Drift detected")]
```

**Drift Detection Algorithm**:
```python
def calculate_drift(reference, current):
    ref_mean = mean(reference)
    cur_mean = mean(current)
    ref_std = stdev(reference)
    cur_std = stdev(current)

    mean_shift = abs(cur_mean - ref_mean) / ref_std if ref_std > 0 else 0
    std_ratio = cur_std / ref_std if ref_std > 0 else 1

    drift_score = min(1.0, (mean_shift + abs(1 - std_ratio)) / 2)

    if drift_score > 0.5:
        severity = "HIGH"
    elif drift_score > 0.3:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return drift_score, severity
```

**Drift Severity**:
| Score | Severity | Action |
|-------|----------|--------|
| > 0.5 | HIGH | Immediate retraining |
| > 0.3 | MEDIUM | Schedule retraining within 1 week |
| ≤ 0.3 | LOW | Continue monitoring |

---

### 6. A/B Testing

Run controlled experiments between model variants.

```python
from agents.ml_ops.agent import ABTestManager

ab = ABTestManager()

# Create A/B test with variants
test = ab.create_test(
    name="fraud_v2_vs_v1",
    variants=[
        {"variant_id": "control", "model_id": "model_v1", "traffic_percentage": 50},
        {"variant_id": "treatment", "model_id": "model_v2", "traffic_percentage": 50}
    ]
)
# Returns: ABTest(test_id="test_xyz789", name="fraud_v2_vs_v1", ...)

# Start the test
ab.start_test(test.test_id)
# Status: CREATED → RUNNING

# Record outcomes over time
ab.record_outcome(test.test_id, "control", {"accuracy": 0.88, "latency_ms": 50}, sample_size=5000)
ab.record_outcome(test.test_id, "treatment", {"accuracy": 0.92, "latency_ms": 45}, sample_size=5000)

# Evaluate results
result = ab.evaluate_test(test.test_id)
# {
#   "test_id": "test_xyz789",
#   "winning_variant": "treatment",
#   "uplift_percent": 4.55,
#   "confidence": 1.0,
#   "control_accuracy": 0.88,
#   "treatment_accuracy": 0.92,
#   "statistically_significant": True
# }

# Complete the test
ab.complete_test(test.test_id)
# Status: RUNNING → COMPLETED
```

**A/B Test Lifecycle**:
```
CREATED → RUNNING → EVALUATED → COMPLETED
```

**Statistical Significance**:
```python
# Simplified significance test
def is_significant(control_mean, treatment_mean, control_n, treatment_n, threshold=0.05):
    pooled_se = sqrt(
        (control_mean * (1 - control_mean) / control_n) +
        (treatment_mean * (1 - treatment_mean) / treatment_n)
    )
    z_score = (treatment_mean - control_mean) / pooled_se
    # For 95% confidence, z > 1.96
    return abs(z_score) > 1.96
```

---

### 7. Deployment Manager

Deploy, scale, and rollback model endpoints.

```python
from agents.ml_ops.agent import DeploymentManager, DeploymentEnvironment

deployer = DeploymentManager()

# Deploy to staging
dep = deployer.deploy(
    "model_v2",
    DeploymentEnvironment.STAGING,
    replicas=3,
    resources={"cpu": "2", "memory": "4Gi"}
)
# Returns: Deployment(deployment_id="dep_abc123", environment=STAGING, replicas=3, ...)

# Check deployment status
deployment = deployer.list_deployments(DeploymentEnvironment.STAGING)
# [Deployment(deployment_id="dep_abc123", model="model_v2", status="healthy")]

# Scale up
deployer.scale(dep.deployment_id, replicas=5)
# Replicas: 3 → 5

# Deploy to canary (partial rollout)
canary = deployer.deploy(
    "model_v2",
    DeploymentEnvironment.CANARY,
    replicas=2
)

# Deploy to production (full rollout)
prod = deployer.deploy(
    "model_v2",
    DeploymentEnvironment.PRODUCTION,
    replicas=10
)

# Rollback if issues detected
deployer.rollback(dep.deployment_id, previous_model_id="model_v1")
# Reverts to previous model version
```

**Deployment Environments**:
| Environment | Purpose | Typical Replicas |
|------------|---------|-----------------|
| LOCAL | Development | 1 |
| STAGING | Pre-production testing | 2-3 |
| CANARY | Gradual rollout | 2-5 |
| PRODUCTION | Full deployment | 3-10 |

---

## Data Models

### Model
| Field | Type | Description |
|-------|------|-------------|
| model_id | str | Unique identifier |
| name | str | Model name |
| version | str | Semantic version |
| framework | str | ML framework (sklearn, pytorch, etc.) |
| task | str | ML task (classification, regression, etc.) |
| status | ModelStatus | Current lifecycle state |
| metrics | Dict[str, float] | Performance metrics |
| tags | List[str] | Classification tags |
| created_at | datetime | Registration time |

### Pipeline
| Field | Type | Description |
|-------|------|-------------|
| pipeline_id | str | Unique identifier |
| name | str | Pipeline name |
| model_name | str | Associated model |
| steps | List[Dict] | Pipeline step configurations |
| created_at | datetime | Creation time |

### PipelineRun
| Field | Type | Description |
|-------|------|-------------|
| run_id | str | Unique identifier |
| pipeline_id | str | Parent pipeline |
| status | str | Execution status |
| parameters | Dict | Runtime parameters |
| metrics | Dict[str, float] | Run metrics |
| duration_seconds | float | Total run time |
| started_at | datetime | Start time |
| completed_at | datetime | Completion time |

### Feature
| Field | Type | Description |
|-------|------|-------------|
| feature_id | str | Unique identifier |
| name | str | Feature name |
| dtype | str | Data type (int, float, string) |
| source | str | Data source |
| entity | str | Entity key |
| description | str | Documentation |

### Experiment
| Field | Type | Description |
|-------|------|-------------|
| experiment_id | str | Unique identifier |
| name | str | Experiment name |
| description | str | Experiment description |
| tags | List[str] | Classification tags |
| created_at | datetime | Creation time |

### ExperimentRun
| Field | Type | Description |
|-------|------|-------------|
| run_id | str | Unique identifier |
| experiment_id | str | Parent experiment |
| model_name | str | Model name |
| parameters | Dict | Hyperparameters |
| metrics | Dict[str, float] | Run metrics |
| created_at | datetime | Run time |

### Deployment
| Field | Type | Description |
|-------|------|-------------|
| deployment_id | str | Unique identifier |
| model_id | str | Deployed model |
| environment | DeploymentEnvironment | Target environment |
| replicas | int | Number of replicas |
| status | str | Health status |
| endpoint_url | str | Serving URL |
| created_at | datetime | Deployment time |

---

## Checklists

### Model Registration
- [ ] Model trained and evaluated
- [ ] Metrics documented and validated
- [ ] Artifacts packaged (model file, config)
- [ ] Version number assigned (semantic versioning)
- [ ] Tags applied for categorization
- [ ] Description updated

### Pipeline Creation
- [ ] All stages defined explicitly
- [ ] Config validated for each stage
- [ ] Dependencies checked
- [ ] Resource requirements estimated
- [ ] Error handling configured
- [ ] Timeout values set
- [ ] Logging enabled

### Model Deployment
- [ ] Model registered and promoted
- [ ] Endpoint configured with resources
- [ ] Health check endpoint ready
- [ ] Monitoring baseline set
- [ ] Rollback plan documented
- [ ] Load testing completed

### A/B Test Setup
- [ ] Variants defined with traffic split
- [ ] Success metrics identified
- [ ] Sample size calculated
- [ ] Duration specified
- [ ] Statistical significance threshold set
- [ ] Hypothesis documented

### Drift Response
- [ ] Drift alert acknowledged
- [ ] Root cause investigated
- [ ] Impact on business metrics assessed
- [ ] Retraining scheduled (if needed)
- [ ] Results documented
- [ ] Lessons learned captured

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Pipeline fails at training | Data shape mismatch | Verify input schema matches expectations |
| Feature store returns null | Feature not registered | Call `register_feature` first |
| High drift score | Data distribution shift | Validate data source, schedule retraining |
| A/B test no winner | Insufficient sample size | Extend test duration or increase traffic |
| Deployment fails | Resource limits | Check CPU/memory allocation |
| Model latency spike | Feature serving slow | Profile feature computation pipeline |
| Experiment comparison empty | No logged runs | Call `log_run` at least twice |
| Rollback fails | Previous model not found | Verify model_id exists in registry |
| Health check fails | Endpoint unreachable | Check deployment status and logs |
| Feature computation slow | Too many entities | Batch computation or cache results |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

agent = MLOpsAgent()
# Now all operations will log detailed debug information
```

---

## Integration Points

| System | Purpose |
|--------|---------|
| Cloud Storage (S3, GCS) | Model artifact storage |
| Container Orchestrator (K8s) | Deployment scaling |
| Feature Platform (Feast) | Online/offline feature serving |
| Monitoring Stack (Prometheus) | Metrics and alerting |
| CI/CD Pipeline (GitHub Actions) | Automated deployment |
| Experiment Platform (MLflow) | Experiment tracking |
| Model Serving (TFServe, KServe) | Inference endpoints |
| Data Lake (Delta, Iceberg) | Training data storage |

---

## Advanced Usage

### Complete MLOps Workflow
```python
from agents.ml_ops.agent import MLOpsAgent, DeploymentEnvironment

agent = MLOpsAgent()

# 1. Register model
model = agent.registry.register_model("churn_predictor", "v1.0.0", "sklearn", "classification")

# 2. Create and run pipeline
pipeline = agent.pipelines.create_pipeline("churn_pipeline", "churn_predictor", [
    {"name": "load", "stage": "data_ingestion"},
    {"name": "features", "stage": "feature_engineering"},
    {"name": "train", "stage": "training"},
    {"name": "eval", "stage": "evaluation"},
])
run = agent.pipelines.execute_pipeline(pipeline.pipeline_id)

# 3. Set up monitoring
agent.monitor.set_baseline(model.model_id, {"accuracy": 0.85, "latency_ms": 30})

# 4. Deploy to staging
agent.deployment.deploy(model.model_id, DeploymentEnvironment.STAGING, replicas=2)

# 5. Run A/B test
test = agent.ab_tests.create_test("churn_v1_test", [
    {"variant_id": "control", "model_id": "old_model", "traffic_percentage": 50},
    {"variant_id": "treatment", "model_id": model.model_id, "traffic_percentage": 50},
])
agent.ab_tests.start_test(test.test_id)

# 6. Evaluate and promote
result = agent.ab_tests.evaluate_test(test.test_id)
if result["winning_variant"] == "treatment":
    agent.registry.promote_model(model.model_id, DeploymentEnvironment.PRODUCTION)
    agent.deployment.deploy(model.model_id, DeploymentEnvironment.PRODUCTION, replicas=5)
```

### Feature Store for Training
```python
# Register features
agent.features.register_feature("user_age", "int", "users")
agent.features.register_feature("purchase_count", "int", "transactions")
agent.features.register_feature("avg_order_value", "float", "orders")

# Ingest training data
for user_id, age, purchases, avg_order in training_data:
    agent.features.ingest_value("user_age", user_id, age)
    agent.features.ingest_value("purchase_count", user_id, purchases)
    agent.features.ingest_value("avg_order_value", user_id, avg_order)

# Retrieve for training
feature_matrix = agent.features.compute_features("user_age", user_ids)
```

### Monitoring with Alerts
```python
# Set baseline
agent.monitor.set_baseline("model_prod", {"accuracy": 0.92})

# Simulate production traffic
for i in range(1000):
    agent.monitor.log_prediction("model_prod", prediction=i%2, actual=i%2, latency_ms=45)

# Check health
health = agent.monitor.check_health("model_prod")
if health["status"] != "healthy":
    print("Model needs attention!")

# Check drift
drift = agent.monitor.detect_drift("model_prod", [0.92]*100, [0.88]*100)
if drift["severity"] == "HIGH":
    print("Retraining needed!")
```
