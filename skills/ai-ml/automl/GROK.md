---
name: "automl"
category: "ai-ml"
version: "2.0.0"
tags: ["ai-ml", "automl", "hyperparameter-tuning", "model-selection", "pipeline-optimization"]
---

# AutoML

## Overview

Automated Machine Learning (AutoML) platform for end-to-end model development including automated data preprocessing, feature engineering, model selection, hyperparameter optimization, and ensemble construction. This module supports tabular, time-series, and image classification tasks with search strategies including random search, Bayesian optimization, population-based training, and evolutionary algorithms. Integrates with scikit-learn, XGBoost, LightGBM, and PyTorch for model training with automatic experiment tracking and reproducibility.

## Core Capabilities

- **Automated Preprocessing**: Handles missing values, categorical encoding, outlier detection, feature scaling, and data type inference automatically
- **Feature Engineering**: Automated feature generation including polynomial features, interaction terms, target encoding, and embedding extraction
- **Model Selection**: Evaluates 20+ model families (linear, tree-based, neural networks, SVM) with automatic algorithm recommendation
- **Hyperparameter Optimization**: Bayesian optimization (TPE, GP), random search, and successive halving for efficient search
- **Ensemble Construction**: Stacking, blending, and weighted averaging of top models for improved performance
- **Experiment Tracking**: Automatic logging of all experiments with metrics, hyperparameters, and model artifacts
- **AutoCV**: Automated computer vision pipeline for image classification with architecture search and augmentation
- **Multi-Objective**: Optimize for accuracy, latency, memory, and interpretability simultaneously

## Usage

```python
from automl import AutoMLEngine, SearchStrategy, TaskType

# Tabular classification
engine = AutoMLEngine(
    task=TaskType.BINARY_CLASSIFICATION,
    time_budget=3600,  # 1 hour
    strategy=SearchStrategy.BAYESIAN,
    metric="roc_auc",
    n_cross_validation=5,
    ensemble_size=10,
)

# Run AutoML
result = engine.fit("train.csv", target_column="is_fraud")
print(f"Best model: {result.best_model_name}")
print(f"Best score: {result.best_score:.4f}")
print(f"Training time: {result.training_time_s:.0f}s")
print(f"Models evaluated: {result.models_evaluated}")

# Predict
predictions = engine.predict("test.csv")
print(f"Predictions shape: {predictions.shape}")
engine.save_model("best_model.pkl")
```

```python
# Feature importance
importance = engine.feature_importance()
for feat, score in importance[:10]:
    print(f"  {feat}: {score:.4f}")

# AutoML report
report = engine.generate_report()
report.export_html("automl_report.html")
report.export_json("automl_results.json")
```

## Best Practices

- Set a reasonable time budget — more time generally finds better models, but with diminishing returns
- Use cross-validation (k=5) to get reliable performance estimates during search
- Enable early stopping for neural network candidates to avoid wasting time on poor architectures
- Check feature importance after AutoML to understand what drives predictions
- Use ensemble of top-5 models rather than just the single best — ensembles are typically 1-3% better
- For imbalanced datasets, use class weighting or SMOTE rather than relying on default accuracy
- Export the full pipeline (preprocessing + model) to avoid train/serve skew
- Run AutoML on a held-out validation set to get an unbiased estimate before final model selection
- Document the AutoML search space and constraints for reproducibility
- Consider inference latency constraints when selecting from the Pareto front of models

## Related Modules

- **neural-architecture-search** — NAS for automated neural network architecture discovery
- **model-optimization** — Compress and optimize AutoML-discovered models
- **model-deployment** — Deploy AutoML pipelines to production
- **data-science** → **feature-engineering** — Manual feature engineering for domain-specific problems
- **data-science** → **statistical-analysis** — Statistical methods that complement AutoML

## Advanced Configuration

### YAML Configuration
```yaml
version: "2.0.0"
settings:
  mode: "production"
  concurrency: 4
  timeout_ms: 30000
  compute:
    gpus: 4
    distributed: true
    backend: "nccl"
```

### JSON Configuration
```json
{"version":"2.0.0","settings":{"mode":"production","compute":{"gpus":4,"distributed":true}}}
```

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `SKILL_MODE` | Runtime mode | `production` |
| `SKILL_GPUS` | Number of GPUs | `1` |
| `SKILL_TIMEOUT` | Timeout (ms) | `30000` |
| `CUDA_VISIBLE_DEVICES` | GPU device IDs | `all` |
| `SKILL_MODEL_PATH` | Model storage path | `/models` |

## Architecture Patterns

### System Architecture
```
+---------------------------------------------------+
|                   Client Layer                     |
|  +----------+  +----------+  +------------------+  |
|  |  Web UI  |  | CLI Tool |  |  Python SDK      |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
+-------------------+-------------------------------+
|              Compute Layer                         |
|  +----------+  +----------+  +------------------+  |
|  |  GPU     |  | Training |  |  Inference       |  |
|  |  Manager |  | Scheduler|  |  Engine          |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
+-------------------+-------------------------------+
|          Orchestration Layer                       |
|  +----------+  +----------+  +------------------+  |
|  | Job      |  | Resource |  |  Experiment      |  |
|  | Queue    |  | Pool     |  |  Tracker         |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
+-------------------+-------------------------------+
|                 Data Layer                          |
|  +----------+  +----------+  +------------------+  |
|  |  Model   |  | Dataset  |  |  Artifact        |  |
|  |  Store   |  | Store    |  |  Registry        |  |
|  +----------+  +----------+  +------------------+  |
+---------------------------------------------------+
```

### Training Pipeline
```
Data -> Preprocess -> Augment -> Batch -> Train -> Evaluate -> Deploy
  |         |           |        |       |         |
  |    [Normalize]  [Transform] [Loader] [Loop]  [Metrics]
  +---------+-----------+--------+-------+---------+
                   Experiment Tracking
```

## Integration Guide

### ML Platforms
```python
import mlflow
mlflow.set_experiment("skill-experiment")
with mlflow.start_run():
    mlflow.log_params(config)
    result = skill.process(input_data)
    mlflow.log_metrics(result.metrics)
```

### Kubeflow Pipeline
```python
from kfp import dsl

@dsl.pipeline(name="skill-pipeline")
def skill_pipeline():
    preprocess = dsl.ContainerOp(name="preprocess", image="skill-preprocess:latest")
    train = dsl.ContainerOp(name="train", image="skill-train:latest")
    deploy = dsl.ContainerOp(name="deploy", image="skill-deploy:latest")
    train.after(preprocess)
    deploy.after(train)
```

## Performance Optimization

### Benchmarks
| Operation | Throughput | Latency (p50) | Latency (p99) |
|-----------|-----------|---------------|---------------|
| Training (batch) | 1000 samples/s | 10ms/batch | 50ms/batch |
| Inference (GPU) | 10,000 inf/s | 0.1ms | 1ms |
| Inference (CPU) | 1,000 inf/s | 1ms | 10ms |

### Optimization Tips
1. **Mixed Precision**: FP16/BF16 for 2x speedup
2. **Gradient Accumulation**: Simulate large batches
3. **Data Loading**: Multiple workers with pinned memory
4. **Model Compilation**: torch.compile() for inference
5. **Dynamic Batching**: Variable-size inputs

## Security Considerations

### Threat Model
| Threat | Risk | Mitigation |
|--------|------|------------|
| Model poisoning | High | Data validation, provenance |
| Adversarial inputs | High | Input sanitization |
| Model theft | High | Access controls, watermarking |
| Data leakage | High | Differential privacy |

### Security Checklist
- [ ] Training data validated
- [ ] Model artifacts signed
- [ ] Inference endpoints authenticated
- [ ] Differential privacy applied
- [ ] Dependencies scanned

## Troubleshooting Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| CUDA out of memory | Batch too large | Reduce batch, gradient accumulation |
| Training divergence | LR too high | Lower LR, warmup schedule |
| Low accuracy | Underfitting | Larger model, train longer |
| Overfitting | Insufficient reg | Dropout, augmentation |
| Slow inference | No optimization | Quantization, TensorRT |

## API Reference

### `init(config: Config) -> Instance`
Initialize with configuration.

### `train(data: Dataset, config: TrainConfig) -> TrainResult`
Train model on dataset.

### `predict(input: Input) -> Prediction`
Run inference.

### `evaluate(model: str, dataset: Dataset) -> EvalResult`
Evaluate model performance.

## Data Models

### Model Schema
```json
{"type":"object","properties":{"model_id":{"type":"string"},"version":{"type":"string"},"framework":{"type":"string","enum":["pytorch","tensorflow","onnx"]},"metrics":{"type":"object"}}}
```

## Deployment Guide

### Docker
```dockerfile
FROM nvidia/cuda:12.2-runtime-ubuntu22.04
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1
CMD ["python", "-m", "uvicorn", "main:app"]
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: skill-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: skill
  template:
    spec:
      containers:
      - name: skill
        image: skill:2.0.0
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
            nvidia.com/gpu: 1
          limits:
            memory: "4Gi"
            cpu: "2000m"
            nvidia.com/gpu: 1
```

## Monitoring & Observability

| Metric | Type | Description | Alert Threshold |
|--------|------|-------------|-----------------|
| `training_loss` | Gauge | Training loss | Divergence |
| `inference_latency_ms` | Histogram | Inference latency | p99 > 100ms |
| `gpu_utilization` | Gauge | GPU usage | < 50% |
| `gpu_memory_used` | Gauge | GPU memory | > 90% |

## Testing Strategy

```python
def test_train():
    result = skill.train(train_data, config)
    assert result.accuracy > 0.8

def test_predict():
    prediction = skill.predict(test_input)
    assert prediction.confidence > 0.5
```

## Versioning & Migration

- Major version for breaking changes
- 6-month deprecation notice

### Changelog
- **[2.0.0]** -- New architecture
- **[1.5.0]** -- Performance improvements
- **[1.0.0]** -- Initial release

## Glossary

| Term | Definition |
|------|------------|
| **Epoch** | One pass through training data |
| **Batch** | Group of samples processed together |
| **LR** | Learning rate |
| **Quantization** | Reducing model precision |
| **Distillation** | Training smaller from larger model |
| **Pruning** | Removing redundant weights |
| **ONNX** | Open Neural Network Exchange |

## Changelog

### [2.0.0] -- 2024-12-01
- Major release with new architecture

### [1.5.0] -- 2024-06-15
- Performance improvements

### [1.0.0] -- 2024-01-01
- Initial stable release

## Contributing Guidelines

```bash
git clone https://github.com/example/skill.git
cd skill
pip install -e ".[dev]"
pytest
```

## License

MIT License -- Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Advanced Search Strategies

### Bayesian Optimization Deep Dive

| Surrogate Model | Strengths | Weaknesses |
|-----------------|-----------|------------|
| Gaussian Process | Uncertainty quantification | Scales poorly |
| Tree-Parzen Estimator | Fast, scalable | Less accurate uncertainty |
| Random Forest | Robust, fast | Less smooth |
| Neural Network | Flexible | Requires tuning |

### Successive Halving

```python
from automl import SuccessiveHalving

sh = SuccessiveHalving(
    n_configs=256,
    min_budget=1,
    max_budget=81,
    reduction_factor=4,
    resource_type="epochs",
)

# Progressively eliminates poor configs
winner = sh.search(objective_function)
```

### Hyperband Algorithm

| Budget | Configs | Survival Rate | Cumulative |
|--------|---------|---------------|------------|
| 1 | 256 | 25% | 64 |
| 4 | 64 | 33% | 21 |
| 16 | 21 | 33% | 7 |
| 64 | 7 | 50% | 3 |
| 256 | 3 | 100% | 1 |

## Feature Engineering Deep Dive

### Automated Feature Generation

| Feature Type | Examples | Use Case |
|--------------|----------|----------|
| Polynomial | x^2, x*y | Non-linear relationships |
| Interaction | x*y, x/z | Feature interactions |
| Aggregation | mean, std, max | Time series |
| Lag | x(t-1), x(t-2) | Temporal patterns |
| Target Encoding | mean(target) | Categorical variables |

### Feature Selection Methods

| Method | Speed | Accuracy | Interpretability |
|--------|-------|----------|------------------|
| Filter (MI) | Fast | Medium | High |
| Wrapper (RFE) | Slow | High | Medium |
| Embedded (L1) | Medium | High | Medium |
| Boruta | Medium | High | Medium |

## Model Selection Matrix

### Algorithm Comparison

| Algorithm | Speed | Accuracy | Memory | Interpretability |
|-----------|-------|----------|--------|------------------|
| Logistic Regression | Fast | Medium | Low | High |
| Random Forest | Medium | High | Medium | Medium |
| XGBoost | Medium | Very High | Medium | Low |
| LightGBM | Fast | Very High | Low | Low |
| CatBoost | Medium | Very High | Medium | Low |
| Neural Network | Slow | High | High | Low |
| SVM | Slow | High | Medium | Low |

### Task-Auto-Algorithm Matching

| Task | Recommended | Backup |
|------|-------------|--------|
| Binary Classification | XGBoost | LightGBM |
| Multi-Class | CatBoost | XGBoost |
| Regression | LightGBM | XGBoost |
| Time Series | Prophet | LSTM |
| Image | EfficientNet | ResNet |
| Text | BERT | RoBERTa |

## Hyperparameter Optimization

### Bayesian Optimization Configuration

```python
from automl import BayesianOptimizer

optimizer = BayesianOptimizer(
    n_initial_points=20,
    acquisition_function="ei",
    kappa=2.576,
    n_iterations=100,
    early_stop_rounds=20,
    parallel_evaluations=4,
)
```

### Hyperparameter Spaces

| Algorithm | Key Hyperparameters | Search Range |
|-----------|---------------------|--------------|
| XGBoost | max_depth, learning_rate, n_estimators | 3-10, 0.01-0.3, 100-1000 |
| LightGBM | num_leaves, learning_rate, feature_fraction | 20-150, 0.01-0.3, 0.5-1.0 |
| Neural Net | hidden_size, dropout, learning_rate | 64-512, 0.1-0.5, 1e-4-1e-2 |

## Ensemble Methods

### Stacking Configuration

```python
from automl import StackingEnsemble

ensemble = StackingEnsemble(
    base_models=[
        ("xgboost", {"max_depth": 6, "learning_rate": 0.1}),
        ("lightgbm", {"num_leaves": 31, "learning_rate": 0.1}),
        ("random_forest", {"n_estimators": 200}),
    ],
    meta_model="logistic_regression",
    cv_folds=5,
    use_features_in_secondary=True,
)
```

### Ensemble Performance Gains

| Method | Improvement | Complexity |
|--------|-------------|------------|
| Weighted Average | 0.5-1% | Low |
| Stacking | 1-3% | Medium |
| Blending | 0.5-2% | Low |
| Multi-layer Stacking | 2-4% | High |

## AutoML Pipelines

### Full Pipeline Configuration

```python
from automl import AutoMLPipeline

pipeline = AutoMLPipeline(
    preprocessing={
        "missing_strategy": "auto",
        "encoding": "onehot_target",
        "scaling": "standard",
        "outlier_detection": "isolation_forest",
    },
    feature_engineering={
        "polynomial_degree": 2,
        "interaction_features": True,
        "target_encoding": True,
        "feature_selection": "mutual_info",
        "k_best_features": 50,
    },
    model_selection={
        "algorithms": ["xgboost", "lightgbm", "random_forest"],
        "metric": "roc_auc",
        "time_budget": 3600,
    },
    ensemble={
        "method": "stacking",
        "top_k": 5,
    },
)
```

## Experiment Tracking

### MLflow Integration

```python
import mlflow
from automl import AutoMLWithTracking

automl = AutoMLWithTracking(
    task=TaskType.BINARY_CLASSIFICATION,
    tracking_uri="http://mlflow-server:5000",
    experiment_name="automl-experiment",
)

result = automl.fit("train.csv", target="label")
mlflow.log_artifact("best_model.pkl")
```

### Weights & Biases

```python
import wandb

wandb.init(project="automl-experiment")
wandb.log({
    "best_model": result.best_model_name,
    "best_score": result.best_score,
    "models_evaluated": result.models_evaluated,
    "training_time": result.training_time_s,
})
```

## AutoCV (Computer Vision)

### Image Classification Pipeline

| Stage | Options | Default |
|-------|---------|---------|
| Architecture | EfficientNet, ResNet, MobileNet | EfficientNet-B0 |
| Augmentation | RandomCrop, Flip, ColorJitter | Auto |
| Training | Adam, SGD with cosine schedule | Auto |
| Optimization | Pruning, Quantization | None |

### AutoCV Configuration

```python
from automl import AutoCV

autocv = AutoCV(
    task="image_classification",
    time_budget=7200,
    architectures=["efficientnet_b0", "resnet50", "mobilenet_v2"],
    input_size=(224, 224),
    augmentations="auto",
    early_stopping_patience=10,
)

result = autocv.fit("data/train/")
```

## Data Preprocessing

### Missing Value Strategies

| Strategy | Speed | Accuracy | Use Case |
|----------|-------|----------|----------|
| Mean/Median | Fast | Medium | Numeric, MCAR |
| Mode | Fast | Medium | Categorical |
| KNN Imputer | Slow | High | Small dataset |
| MICE | Slow | High | MAR data |
| Model-based | Slow | High | Complex patterns |

### Categorical Encoding

| Method | Cardinality | Memory | Accuracy |
|--------|-------------|--------|----------|
| One-Hot | Low (< 20) | High | High |
| Label | Any | Low | Medium |
| Target | High | Low | High |
| Binary | High | Medium | Medium |
| Embedding | Very High | Medium | High |

## AutoML Metrics

### Metric Selection Guide

| Metric | Use Case | Range |
|--------|----------|-------|
| ROC-AUC | Binary classification | 0-1 |
| F1 Score | Imbalanced classes | 0-1 |
| RMSE | Regression | 0 - inf |
| MAE | Regression (robust) | 0 - inf |
| Log Loss | Probability calibration | 0 - inf |
| Accuracy | Balanced classes | 0-1 |

### Cross-Validation Strategies

| Method | Folds | Speed | Reliability |
|--------|-------|-------|-------------|
| K-Fold | 5-10 | Medium | High |
| Stratified K-Fold | 5-10 | Medium | High |
| Leave-One-Out | N | Slow | High |
| Time Series Split | Varies | Fast | Medium |
| Nested CV | 5x5 | Slow | Very High |

## Common Pitfalls

| Issue | Symptom | Solution |
|-------|---------|----------|
| Overfitting search | High CV, low test | Use holdout set |
| Time budget too short | Poor model quality | Increase time |
| Wrong metric | Misleading results | Match metric to business goal |
| Data leakage | Unrealistic scores | Proper CV splits |
| Feature leakage | Artificially high scores | Remove ID columns |

## AutoML Decision Tree

```
Start
  |
  +-- Tabular data?
  |     +-- Yes -> Use XGBoost/LightGBM ensemble
  |     +-- No -> Continue
  |
  +-- Image data?
  |     +-- Yes -> Use AutoCV with EfficientNet
  |     +-- No -> Continue
  |
  +-- Text data?
  |     +-- Yes -> Use AutoNLP with BERT
  |     +-- No -> Continue
  |
  +-- Time series?
        +-- Yes -> Use AutoTS with Prophet
        +-- No -> General AutoML with mixed models
```

## Future Directions

- **Neural Architecture Search integration**: Combined hyperparameter + architecture search
- **Meta-learning**: Learn from previous AutoML runs
- **Auto-feature engineering**: Automated feature synthesis
- **Auto-interpretability**: Automated model explanation generation

## AutoML Benchmarks

### OpenML Results

| Dataset | Best Model | Score | Time (s) |
|---------|------------|-------|----------|
| adult | XGBoost | 0.928 | 120 |
| bank-marketing | LightGBM | 0.912 | 95 |
| credit-default | CatBoost | 0.887 | 150 |
| higgs | XGBoost | 0.845 | 300 |
| kick | RandomForest | 0.798 | 180 |

### AutoML vs Manual Tuning

| Aspect | AutoML | Manual Tuning |
|--------|--------|---------------|
| Time to solution | 1-2 hours | 1-2 weeks |
| Final performance | 95-99% of manual | 100% |
| Expertise required | Low | High |
| Reproducibility | High | Medium |
| Documentation | Automatic | Manual |

## AutoML Configuration Templates

### Quick Start Template

```python
from automl import AutoMLEngine, TaskType

engine = AutoMLEngine(
    task=TaskType.BINARY_CLASSIFICATION,
    time_budget=600,
    metric="roc_auc",
    ensemble_size=5,
    n_jobs=-1,
)

result = engine.fit("data.csv", target="label")
```

### Production Template

```python
from automl import AutoMLEngine, TaskType, ProductionConfig

engine = AutoMLEngine(
    task=TaskType.BINARY_CLASSIFICATION,
    time_budget=3600,
    strategy="bayesian",
    metric="roc_auc",
    ensemble_size=10,
    config=ProductionConfig(
        interpretability=True,
        fairness_check=True,
        latency_constraint_ms=50,
        model_size_constraint_mb=100,
    ),
)

result = engine.fit(
    train_data="train.csv",
    target="label",
    validation_data="val.csv",
    test_data="test.csv",
)
```
