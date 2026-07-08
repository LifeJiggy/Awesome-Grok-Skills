# ML Ops Agent

End-to-end MLOps pipelines, model deployment, feature stores, experiment tracking, model monitoring, and A/B testing.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

The ML Ops Agent provides a complete machine learning operations platform covering the full lifecycle from feature engineering through model deployment and production monitoring. It enables teams to train, version, deploy, monitor, and iterate on ML models with reproducibility and reliability.

### Key Capabilities

| Capability | Description |
|-----------|-------------|
| Model Registry | Version and manage model lifecycle |
| Pipeline Manager | Orchestrate multi-step training workflows |
| Feature Store | Serve and compute features for ML |
| Experiment Tracker | Log and compare training runs |
| Model Monitor | Detect drift and evaluate health |
| A/B Testing | Run controlled model experiments |
| Deployment Manager | Deploy endpoints with scaling |

---

## Features

### Model Registry
- Semantic versioning with version history
- Status tracking through lifecycle stages
- Promotion across environments (local, staging, canary, production)
- Retirement and archival

### Pipeline Management
- Configurable multi-step pipelines
- 8 stage types covering the full ML workflow
- Execution tracking with duration and metrics
- Run history with parameter logging

### Feature Store
- Feature registration with metadata
- Real-time value ingestion and lookup
- Aggregated feature computation (mean, min, max, count)
- Entity-level feature serving

### Experiment Tracking
- Experiment creation with tags
- Run logging with parameters and metrics
- Automated best-run comparison
- Cross-metric optimization

### Model Monitoring
- Prediction logging with latency tracking
- Statistical drift detection (mean shift, variance change)
- Performance degradation alerts
- Health status dashboard

### A/B Testing
- Multi-variant test configuration
- Traffic percentage allocation
- Incremental metric recording
- Winner determination with confidence scoring

### Deployment
- Multi-environment deployment (local, staging, canary, production)
- Replica scaling
- Rollback to previous model versions
- Resource configuration

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│              MLOpsAgent (Facade)                 │
├─────────────────────────────────────────────────┤
│  ModelRegistry    │  PipelineManager            │
│  FeatureStore     │  ExperimentTracker          │
│  ModelMonitor     │  ABTestManager              │
│  DeploymentManager                            │
└─────────────────────────────────────────────────┘
```

---

## Quick Start

### Installation

```bash
pip install awesome-grok-skills
```

### Minimal Example

```python
from agents.ml_ops.agent import MLOpsAgent, DeploymentEnvironment

agent = MLOpsAgent()

# Train and deploy in one call
result = agent.train_and_deploy(
    model_name="classifier",
    version="v1.0.0",
    framework="sklearn",
    task="classification",
    environment=DeploymentEnvironment.STAGING
)

print(f"Model: {result['model_id']}")
print(f"Accuracy: {result['metrics']['accuracy']}")
```

---

## Usage

### Running the Agent

```bash
python agents/ml-ops/agent.py
```

### Programmatic Access

```python
from agents.ml_ops.agent import MLOpsAgent

agent = MLOpsAgent()

# Each component can be used independently
model = agent.registry.register_model("my_model", "v1", "pytorch", "regression")
pipeline = agent.pipelines.create_pipeline("my_pipeline", "my_model", [...])
feature = agent.features.register_feature("age", "int", "users")
exp = agent.experiments.create_experiment("my_experiment")
```

---

## API Reference

### MLOpsAgent

| Method | Description |
|--------|-------------|
| `train_and_deploy(name, version, framework, task, env)` | Full train-and-deploy workflow |

### ModelRegistry

| Method | Description |
|--------|-------------|
| `register_model(name, version, framework, task)` | Register new model |
| `get_model(model_id)` | Retrieve model |
| `update_model(model_id, **kwargs)` | Update model fields |
| `list_models(name, status)` | List models with filters |
| `get_latest_version(name)` | Get latest version |
| `promote_model(model_id, env)` | Promote to environment |
| `retire_model(model_id)` | Mark as retired |

### PipelineManager

| Method | Description |
|--------|-------------|
| `create_pipeline(name, model_name, steps)` | Create pipeline |
| `execute_pipeline(pipeline_id, params)` | Run pipeline |
| `get_run(run_id)` | Get run details |
| `list_pipelines()` | List all pipelines |
| `list_runs(pipeline_id)` | List runs for pipeline |

### FeatureStore

| Method | Description |
|--------|-------------|
| `register_feature(name, dtype, source)` | Register feature |
| `ingest_value(feature, entity, value)` | Add feature value |
| `get_latest_value(feature, entity)` | Get latest value |
| `compute_features(feature, entities)` | Compute aggregations |
| `list_features()` | List all features |
| `get_feature_stats()` | Feature statistics |

### ExperimentTracker

| Method | Description |
|--------|-------------|
| `create_experiment(name, desc, tags)` | Create experiment |
| `log_run(experiment_id, model, params, metrics)` | Log run |
| `compare_runs(experiment_id)` | Compare all runs |
| `list_experiments()` | List experiments |

### ModelMonitor

| Method | Description |
|--------|-------------|
| `set_baseline(model_id, metrics)` | Set baseline metrics |
| `log_prediction(model_id, pred, actual, latency)` | Log prediction |
| `check_health(model_id)` | Health check |
| `detect_drift(model_id, reference, current)` | Detect drift |
| `evaluate_performance(model_id)` | Evaluate against baseline |
| `get_alerts(model_id)` | Get drift alerts |

### ABTestManager

| Method | Description |
|--------|-------------|
| `create_test(name, variants)` | Create A/B test |
| `start_test(test_id)` | Start test |
| `record_outcome(test_id, variant, metrics, size)` | Record outcome |
| `evaluate_test(test_id)` | Evaluate and determine winner |
| `complete_test(test_id)` | Mark test complete |

### DeploymentManager

| Method | Description |
|--------|-------------|
| `deploy(model_id, env, replicas)` | Deploy model |
| `scale(deployment_id, replicas)` | Scale replicas |
| `rollback(deployment_id, prev_model)` | Rollback model |
| `list_deployments(env)` | List deployments |

---

## Examples

### Full Training Pipeline

```python
agent = MLOpsAgent()

# Create and execute pipeline
pipeline = agent.pipelines.create_pipeline("fraud_pipeline", "fraud_detector", [
    {"name": "load", "stage": "data_ingestion", "config": {"source": "s3://bucket/data"}},
    {"name": "clean", "stage": "preprocessing"},
    {"name": "features", "stage": "feature_engineering"},
    {"name": "train", "stage": "training", "config": {"algo": "xgboost"}},
    {"name": "eval", "stage": "evaluation"},
])

run = agent.pipelines.execute_pipeline(pipeline.pipeline_id)
print(f"Completed in {run.duration_seconds:.1f}s with accuracy {run.metrics['accuracy']}")
```

### Experiment Comparison

```python
exp = agent.experiments.create_experiment("lr_tuning", tags=["logistic-regression"])

for lr in [0.001, 0.01, 0.1, 1.0]:
    agent.experiments.log_run(exp.experiment_id, "model", {"lr": lr}, {"accuracy": 0.9 + lr * 0.01})

comparison = agent.experiments.compare_runs(exp.experiment_id)
print(f"Best: {comparison['best_per_metric']}")
```

### Production Monitoring

```python
agent.monitor.set_baseline("model_prod", {"accuracy": 0.92})

# Simulate predictions
for i in range(100):
    agent.monitor.log_prediction("model_prod", prediction=i % 2, actual=i % 2, latency_ms=45 + i % 10)

health = agent.monitor.check_health("model_prod")
drift = agent.monitor.detect_drift("model_prod", [0.92]*100, [0.87]*100)
perf = agent.monitor.evaluate_performance("model_prod")

print(f"Health: {health['status']}, Drift: {drift.severity.value}, Retrain: {perf['needs_retraining']}")
```

### A/B Test Workflow

```python
test = agent.ab_tests.create_test("model_v2_test", [
    {"variant_id": "control", "model_id": "model_v1", "traffic_percentage": 50},
    {"variant_id": "treatment", "model_id": "model_v2", "traffic_percentage": 50},
])
agent.ab_tests.start_test(test.test_id)

# Record outcomes
agent.ab_tests.record_outcome(test.test_id, "control", {"accuracy": 0.88}, 5000)
agent.ab_tests.record_outcome(test.test_id, "treatment", {"accuracy": 0.93}, 5000)

result = agent.ab_tests.evaluate_test(test.test_id)
print(f"Winner: {result['winning_variant']} (+{result['uplift_percent']}%)")
agent.ab_tests.complete_test(test.test_id)
```

---

## Configuration

### Pipeline Stages

| Stage | Purpose | Typical Duration |
|-------|---------|-----------------|
| DATA_INGESTION | Load data | 1-10 min |
| PREPROCESSING | Clean/transform | 5-30 min |
| FEATURE_ENGINEERING | Create features | 10-60 min |
| TRAINING | Fit model | 10-300 min |
| EVALUATION | Measure metrics | 1-5 min |
| REGISTRATION | Catalog model | <1 min |
| DEPLOYMENT | Serve endpoint | 1-5 min |
| MONITORING | Track health | Continuous |

### Deployment Environments

| Environment | Purpose | Typical Replicas |
|------------|---------|-----------------|
| LOCAL | Development | 1 |
| STAGING | Pre-production testing | 2-3 |
| CANARY | Gradual rollout | 2-5 |
| PRODUCTION | Full deployment | 3-10 |

### Drift Thresholds

| Score | Severity | Recommended Action |
|-------|----------|-------------------|
| > 0.5 | HIGH | Immediate retraining |
| 0.3-0.5 | MEDIUM | Schedule retraining within 1 week |
| < 0.3 | LOW | Continue monitoring |

---

## Best Practices

### Model Registry
- Use semantic versioning (v1.0.0)
- Always register models before deployment
- Tag models with purpose and status
- Retire old versions to reduce confusion

### Pipelines
- Define all stages explicitly
- Use descriptive step names
- Log parameters for reproducibility
- Set appropriate timeout values

### Feature Store
- Register features with clear descriptions
- Use consistent entity ID formats
- Monitor feature freshness with TTL
- Document data sources

### Experiments
- One experiment per tuning objective
- Log all relevant parameters
- Include baseline comparisons
- Document findings in tags

### Monitoring
- Set baselines at deployment time
- Log both predictions and actuals
- Monitor latency alongside accuracy
- Review drift alerts within 24 hours

### A/B Testing
- Ensure statistically significant sample sizes
- Run tests for sufficient duration
- Test one variable at a time
- Document test hypotheses

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

---

## License

MIT License - see [LICENSE](../../LICENSE) for details.
