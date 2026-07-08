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

---

## Capabilities

### 1. Model Registry

Register, version, and manage the full lifecycle of ML models.

```python
from agents.ml_ops.agent import ModelRegistry, ModelStatus

registry = ModelRegistry()

# Register a model
model = registry.register_model(
    name="fraud_detector",
    version="v2.1.0",
    framework="sklearn",
    task="classification",
    metrics={"accuracy": 0.92, "precision": 0.90, "recall": 0.88},
    tags=["production", "fraud"]
)

# Get latest version
latest = registry.get_latest_version("fraud_detector")

# Promote to production
deployment = registry.promote_model(model.model_id, DeploymentEnvironment.PRODUCTION)

# Retire old model
registry.retire_model(old_model_id)
```

**Model Lifecycle**:
```
REGISTERED → TRAINED → DEPLOYED → MONITORING
                               ↕
                        NEEDS_RETRAINING
                               ↓
                            RETIRED
```

---

### 2. Pipeline Manager

Create and execute multi-step ML training pipelines.

```python
from agents.ml_ops.agent import PipelineManager, PipelineStage

manager = PipelineManager()

# Create pipeline
pipeline = manager.create_pipeline(
    name="fraud_training_v2",
    model_name="fraud_detector",
    steps_config=[
        {"name": "data_loading", "stage": "data_ingestion", "config": {"source": "s3://data/"}},
        {"name": "preprocessing", "stage": "preprocessing", "config": {"scaler": "standard"}},
        {"name": "feature_eng", "stage": "feature_engineering", "config": {"features": 50}},
        {"name": "training", "stage": "training", "config": {"algorithm": "xgboost"}},
        {"name": "evaluation", "stage": "evaluation", "config": {"metrics": ["accuracy", "f1"]}},
    ]
)

# Execute
run = manager.execute_pipeline(pipeline.pipeline_id, parameters={"lr": 0.01})
print(f"Pipeline completed: {run.run_id}, accuracy: {run.metrics['accuracy']}")
```

**Pipeline Stages**:
| Stage | Purpose |
|-------|---------|
| DATA_INGESTION | Load raw data |
| PREPROCESSING | Clean and transform |
| FEATURE_ENGINEERING | Create model features |
| TRAINING | Fit model |
| EVALUATION | Measure performance |
| REGISTRATION | Register in catalog |
| DEPLOYMENT | Serve endpoint |
| MONITORING | Track health |

---

### 3. Feature Store

Manage features for both training and real-time serving.

```python
from agents.ml_ops.agent import FeatureStore

store = FeatureStore()

# Register feature
store.register_feature("user_age", "int", "users_table", "User age in years")
store.register_feature("transaction_count_7d", "int", "transactions", "Transactions in last 7 days")

# Ingest values
store.ingest_value("user_age", "user_1", 30)
store.ingest_value("user_age", "user_2", 25)

# Get latest value
latest = store.get_latest_value("user_age", "user_1")

# Compute aggregated features
stats = store.compute_features("user_age", ["user_1", "user_2"])
# {'user_1': {'latest': 30, 'mean': 30}, 'user_2': {'latest': 25, 'mean': 25}}
```

---

### 4. Experiment Tracker

Log and compare ML experiments systematically.

```python
from agents.ml_ops.agent import ExperimentTracker

tracker = ExperimentTracker()

# Create experiment
exp = tracker.create_experiment(
    name="fraud_xgboost_tuning",
    description="Hyperparameter tuning for fraud detector",
    tags=["xgboost", "fraud", "v2"]
)

# Log runs
tracker.log_run(exp.experiment_id, "fraud_detector", {"lr": 0.01, "depth": 6}, {"accuracy": 0.92})
tracker.log_run(exp.experiment_id, "fraud_detector", {"lr": 0.001, "depth": 8}, {"accuracy": 0.94})
tracker.log_run(exp.experiment_id, "fraud_detector", {"lr": 0.1, "depth": 4}, {"accuracy": 0.88})

# Compare
comparison = tracker.compare_runs(exp.experiment_id)
# {'best_per_metric': {'accuracy': {'best_run': 'run_abc', 'best_value': 0.94}}}
```

---

### 5. Model Monitor

Detect drift, evaluate performance, and track health.

```python
from agents.ml_ops.agent import ModelMonitor

monitor = ModelMonitor()

# Set baseline
monitor.set_baseline("model_1", {"accuracy": 0.92, "latency_ms": 45})

# Log predictions
monitor.log_prediction("model_1", prediction=1, actual=1, latency_ms=42)
monitor.log_prediction("model_1", prediction=0, actual=1, latency_ms=38)

# Check health
health = monitor.check_health("model_1")
# {'status': 'healthy', 'avg_latency_ms': 40.0, 'error_rate': 0.5}

# Detect drift
drift = monitor.detect_drift("model_1", reference_data=[0.92]*100, current_data=[0.85]*100)
# {'drift_score': 0.65, 'severity': 'high'}

# Evaluate performance
perf = monitor.evaluate_performance("model_1")
# {'degradation': -0.02, 'needs_retraining': False}
```

**Drift Severity**:
| Score | Severity | Action |
|-------|----------|--------|
| > 0.5 | HIGH | Retrain immediately |
| > 0.3 | MEDIUM | Schedule retraining |
| ≤ 0.3 | LOW | Continue monitoring |

---

### 6. A/B Testing

Run controlled experiments between model variants.

```python
from agents.ml_ops.agent import ABTestManager

ab = ABTestManager()

# Create test
test = ab.create_test("fraud_v2_vs_v1", [
    {"variant_id": "control", "model_id": "model_v1", "traffic_percentage": 50},
    {"variant_id": "treatment", "model_id": "model_v2", "traffic_percentage": 50},
])

# Start
ab.start_test(test.test_id)

# Record outcomes
ab.record_outcome(test.test_id, "control", {"accuracy": 0.88, "latency_ms": 50}, sample_size=1000)
ab.record_outcome(test.test_id, "treatment", {"accuracy": 0.92, "latency_ms": 45}, sample_size=1000)

# Evaluate
result = ab.evaluate_test(test.test_id)
# {'winning_variant': 'treatment', 'uplift_percent': 4.55, 'confidence': 1.0}

# Complete
ab.complete_test(test.test_id)
```

---

### 7. Deployment Manager

Deploy, scale, and rollback model endpoints.

```python
from agents.ml_ops.agent import DeploymentManager, DeploymentEnvironment

deployer = DeploymentManager()

# Deploy to staging
dep = deployer.deploy("model_v2", DeploymentEnvironment.STAGING, replicas=3)

# Scale up
deployer.scale(dep.deployment_id, replicas=5)

# Rollback if needed
deployer.rollback(dep.deployment_id, previous_model_id="model_v1")
```

---

## Data Models

### Model
| Field | Type | Description |
|-------|------|-------------|
| model_id | str | Unique identifier |
| name | str | Model name |
| version | str | Semantic version |
| framework | str | ML framework |
| status | ModelStatus | Current lifecycle state |
| metrics | Dict[str, float] | Performance metrics |

### TrainingRun
| Field | Type | Description |
|-------|------|-------------|
| run_id | str | Unique identifier |
| model_name | str | Associated model |
| parameters | Dict | Hyperparameters |
| metrics | Dict[str, float] | Run metrics |
| duration_seconds | float | Run time |

### Feature
| Field | Type | Description |
|-------|------|-------------|
| feature_id | str | Unique identifier |
| name | str | Feature name |
| dtype | str | Data type |
| source | str | Data source |
| description | str | Documentation |

### DriftAlert
| Field | Type | Description |
|-------|------|-------------|
| alert_id | str | Unique identifier |
| model_id | str | Affected model |
| drift_type | DriftType | Type of drift |
| severity | AlertSeverity | Alert level |
| detection_score | float | 0.0-1.0 score |

---

## Checklists

### Model Registration
- [ ] Model trained and evaluated
- [ ] Metrics documented
- [ ] Artifacts packaged
- [ ] Version number assigned
- [ ] Tags applied

### Pipeline Creation
- [ ] All stages defined
- [ ] Config validated
- [ ] Dependencies checked
- [ ] Resource requirements estimated
- [ ] Error handling configured

### Model Deployment
- [ ] Model registered and promoted
- [ ] Endpoint configured
- [ ] Health check endpoint ready
- [ ] Monitoring enabled
- [ ] Rollback plan documented

### A/B Test Setup
- [ ] Variants defined with traffic split
- [ ] Success metrics identified
- [ ] Sample size calculated
- [ ] Duration specified
- [ ] Statistical significance threshold set

### Drift Response
- [ ] Drift alert acknowledged
- [ ] Root cause investigated
- [ ] Impact assessed
- [ ] Retraining scheduled (if needed)
- [ ] Results documented

---

## Troubleshooting

### Pipeline Fails at Training Stage
- Check data shape and types
- Verify feature store connectivity
- Review hyperparameter values
- Check resource availability

### High Drift Score Detected
- Validate incoming data quality
- Check for schema changes
- Review feature distribution shifts
- Consider retraining with recent data

### A/B Test Shows No Significant Difference
- Increase sample size
- Extend test duration
- Check for implementation issues
- Review metric selection

### Model Latency Increased
- Check deployment replica count
- Review feature serving latency
- Profile inference pipeline
- Consider model optimization

### Feature Store Returns Null
- Verify feature registration
- Check entity ID format
- Confirm data ingestion completed
- Review TTL settings

---

## Integration Points

| System | Purpose |
|--------|---------|
| Cloud Storage | Model artifact storage |
| Container Orchestrator | Deployment scaling |
| Feature Platform | Online/offline feature serving |
| Monitoring Stack | Metrics and alerting |
| CI/CD Pipeline | Automated deployment |
| Experiment Platform | A/B test orchestration |
