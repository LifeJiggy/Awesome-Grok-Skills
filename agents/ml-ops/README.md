# ML Ops Agent

End-to-end MLOps pipelines, model deployment, feature stores, experiment tracking, model monitoring, and A/B testing.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Contributing](#contributing)
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

### System Requirements

- Python 3.10 or higher
- 1 GB RAM minimum
- 500 MB disk space
- Network access for remote serving (optional)

---

## Features

### Model Registry
- Semantic versioning with version history
- Status tracking through lifecycle stages (registered, trained, deployed, needs_retraining, retired)
- Promotion across environments (local, staging, canary, production)
- Retirement and archival
- Model metadata and framework tracking

### Pipeline Management
- Configurable multi-step pipelines
- 8 stage types covering the full ML workflow
- Execution tracking with duration and metrics
- Run history with parameter logging
- Parallel step execution where dependencies allow

### Feature Store
- Feature registration with metadata
- Real-time value ingestion and lookup
- Aggregated feature computation (mean, min, max, count)
- Entity-level feature serving
- Online store (< 1ms latency) and offline store (batch)

### Experiment Tracking
- Experiment creation with tags
- Run logging with parameters and metrics
- Automated best-run comparison
- Cross-metric optimization
- Experiment history and versioning

### Model Monitoring
- Prediction logging with latency tracking
- Statistical drift detection (mean shift, variance change)
- Performance degradation alerts
- Health status dashboard
- Configurable drift thresholds

### A/B Testing
- Multi-variant test configuration
- Traffic percentage allocation
- Incremental metric recording
- Winner determination with confidence scoring
- Statistical significance evaluation

### Deployment
- Multi-environment deployment (local, staging, canary, production)
- Replica scaling
- Rollback to previous model versions
- Resource configuration
- Health check verification

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│              MLOpsAgent (Facade)                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │ ModelRegistry  │  │PipelineManager │  │ FeatureStore   │    │
│  │                │  │                │  │                │    │
│  │ Versioning     │  │ Orchestrate    │  │ Online/Offline │    │
│  │ Promotion      │  │ Step Execution │  │ Serving        │    │
│  │ Lifecycle      │  │ Run History    │  │ Aggregation    │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │ExperimentTrackr│  │ ModelMonitor   │  │ ABTestManager  │    │
│  │                │  │                │  │                │    │
│  │ Runs           │  │ Drift          │  │ Variants       │    │
│  │ Comparison     │  │ Performance    │  │ Traffic Split  │    │
│  │ Best Model     │  │ Alerts         │  │ Evaluation     │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
│                                                                  │
│  ┌────────────────┐                                             │
│  │DeploymentMgr   │                                             │
│  │                │                                             │
│  │ Endpoints      │                                             │
│  │ Scaling        │                                             │
│  │ Rollback       │                                             │
│  └────────────────┘                                             │
└─────────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

```
ML Workflow Request
     │
     ▼
MLOpsAgent (facade)
     │
     ├──→ ModelRegistry.register_model()
     │         │
     │         ▼
     │    Model (REGISTERED)
     │
     ├──→ PipelineManager.create_pipeline()
     │         │
     │         ▼
     │    Pipeline
     │
     ├──→ PipelineManager.execute_pipeline()
     │         │
     │         ├──→ Data Ingestion
     │         ├──→ Feature Engineering
     │         ├──→ Training
     │         ├──→ Evaluation
     │         └──→ Registration
     │
     ├──→ ModelRegistry.promote_model()
     │         │
     │         ▼
     │    Model (DEPLOYED)
     │
     ├──→ DeploymentManager.deploy()
     │         │
     │         ▼
     │    Endpoint (active)
     │
     ├──→ ModelMonitor.set_baseline()
     │         │
     │         ▼
     │    Baseline metrics set
     │
     ├──→ ABTestManager.create_test()
     │         │
     │         ▼
     │    A/B Test (RUNNING)
     │
     └──→ ModelMonitor.check_health()
               │
               ▼
          Health Status
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

### 60-Second Setup

```python
from agents.ml_ops.agent import MLOpsAgent, DeploymentEnvironment

agent = MLOpsAgent()

# Register and deploy
model = agent.registry.register_model("my_model", "v1.0.0", "pytorch", "regression")
agent.deployment.deploy(model.model_id, DeploymentEnvironment.LOCAL, replicas=1)

# Check health
health = agent.monitor.check_health(model.model_id)
print(f"Status: {health['status']}")
```

---

## Installation

### From PyPI

```bash
pip install awesome-grok-skills
```

### From Source

```bash
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e .
```

### Development Install

```bash
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e ".[dev]"
pytest  # Run tests
```

### Requirements

```
Python >= 3.10
No external dependencies (stdlib only)
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

### Component Independence

```python
from agents.ml_ops.agent import ModelRegistry, FeatureStore

# Use components directly without the facade
registry = ModelRegistry()
features = FeatureStore()

model = registry.register_model("direct_model", "v1", "sklearn", "classification")
features.register_feature("age", "int", "users")
```

### CLI Usage

```bash
# List all models
python agents/ml-ops/agent.py --list-models

# Execute pipeline
python agents/ml-ops/agent.py --execute-pipeline pipeline_123

# Check model health
python agents/ml-ops/agent.py --health model_abc
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
    agent.experiments.log_run(
        exp.experiment_id,
        "model",
        {"lr": lr},
        {"accuracy": 0.9 + lr * 0.01, "loss": 0.2 - lr * 0.01}
    )

comparison = agent.experiments.compare_runs(exp.experiment_id)
print(f"Best accuracy: {comparison['best_per_metric']['accuracy']}")
```

### Production Monitoring

```python
agent.monitor.set_baseline("model_prod", {"accuracy": 0.92, "latency_ms": 50})

# Simulate predictions
for i in range(100):
    agent.monitor.log_prediction(
        "model_prod",
        prediction=i % 2,
        actual=i % 2,
        latency_ms=45 + i % 10
    )

health = agent.monitor.check_health("model_prod")
drift = agent.monitor.detect_drift("model_prod", [0.92]*100, [0.87]*100)
perf = agent.monitor.evaluate_performance("model_prod")

print(f"Health: {health['status']}")
print(f"Drift: {drift.severity.value}")
print(f"Retrain: {perf['needs_retraining']}")
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

### Feature Store Operations

```python
# Register features
agent.features.register_feature("age", "int", "users")
agent.features.register_feature("income", "float", "users")
agent.features.register_feature("purchase_count", "int", "users")

# Ingest values
agent.features.ingest_value("age", "user_1", 35)
agent.features.ingest_value("income", "user_1", 75000.0)
agent.features.ingest_value("purchase_count", "user_1", 12)

# Retrieve
age = agent.features.get_latest_value("age", "user_1")
print(f"Age: {age}")

# Compute aggregations
stats = agent.features.compute_features("purchase_count", ["user_1", "user_2", "user_3"])
print(f"Stats: {stats}")
```

### Deployment with Rollback

```python
# Deploy v1
agent.deployment.deploy("model_v1", DeploymentEnvironment.STAGING, replicas=2)

#发现问题, rollback
agent.deployment.rollback("deployment_abc", "model_v1")

# Check deployments
deployments = agent.deployment.list_deployments(DeploymentEnvironment.STAGING)
for d in deployments:
    print(f"{d.model_id}: {d.status} ({d.replicas} replicas)")
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

### Model States

| State | Description |
|-------|-------------|
| REGISTERED | Model registered but not trained |
| TRAINED | Model trained and ready |
| DEPLOYED | Model serving in environment |
| NEEDS_RETRAINING | Model requires retraining |
| RETIRED | Model no longer in use |

---

## Best Practices

### Model Registry
- Use semantic versioning (v1.0.0)
- Always register models before deployment
- Tag models with purpose and status
- Retire old versions to reduce confusion
- Document model assumptions and limitations

### Pipelines
- Define all stages explicitly
- Use descriptive step names
- Log parameters for reproducibility
- Set appropriate timeout values
- Validate data before each step
- Handle failures gracefully

### Feature Store
- Register features with clear descriptions
- Use consistent entity ID formats
- Monitor feature freshness with TTL
- Document data sources
- Validate feature values before ingestion
- Use offline store for batch training

### Experiments
- One experiment per tuning objective
- Log all relevant parameters
- Include baseline comparisons
- Document findings in tags
- Use consistent metric naming
- Track experiment lineage

### Monitoring
- Set baselines at deployment time
- Log both predictions and actuals
- Monitor latency alongside accuracy
- Review drift alerts within 24 hours
- Set up automated retraining triggers
- Track model version in predictions

### A/B Testing
- Ensure statistically significant sample sizes
- Run tests for sufficient duration
- Test one variable at a time
- Document test hypotheses
- Monitor for novelty effects
- Use confidence intervals

### Deployment
- Use blue-green deployments for zero downtime
- Implement health checks before traffic routing
- Set up automatic rollback on failure
- Monitor deployment metrics
- Use canary releases for validation
- Document deployment procedures

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

### Common Error Messages

| Error | Meaning | Fix |
|-------|---------|-----|
| `ModelNotFoundError` | Model ID doesn't exist | Verify model_id |
| `PipelineError` | Pipeline execution failed | Check step configuration |
| `DeploymentError` | Deployment failed | Check resources and config |
| `FeatureStoreError` | Feature operation failed | Verify feature registration |
| `ExperimentNotFoundError` | Experiment ID doesn't exist | Verify experiment_id |

---

## FAQ

### Q: Can I use components independently?
A: Yes, each component (ModelRegistry, FeatureStore, etc.) can be used standalone without the MLOpsAgent facade.

### Q: What frameworks are supported?
A: Any Python ML framework (sklearn, pytorch, tensorflow, xgboost, etc.). The agent is framework-agnostic.

### Q: How many pipeline steps can I have?
A: No hard limit, but we recommend 5-8 steps for maintainability.

### Q: Can I run pipelines in parallel?
A: Sequential execution is default. Parallel execution is supported when steps have no dependencies.

### Q: How do I handle large datasets?
A: Use the offline feature store for batch processing and the online store for real-time serving.

### Q: Can I customize drift detection?
A: The drift algorithm is built-in, but you can set custom thresholds and baseline metrics.

---

## Contributing

We welcome contributions! Please see our [Contributing Guide](../../CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e ".[dev]"
pre-commit install
```

### Running Tests

```bash
pytest tests/ml_ops/
pytest --cov=agents.ml_ops
```

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for public methods
- Add tests for new functionality

---

## License

MIT License - see [LICENSE](../../LICENSE) for details.

---

## Support

- Documentation: [docs.example.com](https://docs.example.com)
- Issues: [GitHub Issues](https://github.com/awesome-grok-skills/awesome-grok-skills/issues)
- Discussions: [GitHub Discussions](https://github.com/awesome-grok-skills/awesome-grok-skills/discussions)
