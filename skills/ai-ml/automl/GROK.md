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
