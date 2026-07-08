# Data Science Agent

A self-contained, zero-dependency data science framework covering the full lifecycle: data ingestion → profiling → preprocessing → feature engineering → model training → evaluation → experiment tracking → visualization → reproducibility management.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Statistical Analysis](#statistical-analysis)
  - [ML Model Development](#ml-model-development)
  - [Feature Engineering](#feature-engineering)
  - [Data Preprocessing](#data-preprocessing)
  - [Experiment Tracking](#experiment-tracking)
  - [Visualization](#visualization)
  - [Reproducibility](#reproducibility)
  - [Hyperparameter Tuning](#hyperparameter-tuning)
  - [Model Evaluation](#model-evaluation)
  - [Data Pipelines](#data-pipelines)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Data Science Agent provides production-grade data science capabilities implemented entirely in Python with zero external dependencies. Every statistical test, ML algorithm, and visualization is built from scratch for maximum portability, auditability, and educational value.

**Key Design Principles:**
- Zero external dependencies (no numpy, sklearn, pandas required)
- Full type hints and dataclass models
- Comprehensive error handling and logging
- Reproducibility by design (SHA-256 hashing, seed tracking, environment capture)
- Every operation is inspectable and reversible

---

## Features

| Feature | Description | Classes |
|---------|-------------|---------|
| Statistical Analysis | Descriptive stats, hypothesis testing, correlation, outlier detection, normality testing | `StatisticalAnalyzer` |
| ML Model Training | Decision stump (classification), OLS linear regression, cross-validation | `MLModelBuilder` |
| Feature Engineering | Polynomial, log, sqrt, ratio, interaction, date decomposition, binning, selection | `FeatureEngineer` |
| Data Preprocessing | Missing value imputation (7 strategies), normalization (6 methods), encoding (4 methods), deduplication, train/test splitting | `DataPreprocessor` |
| Hyperparameter Tuning | Grid search, random search | `HyperparameterTuner` |
| Model Evaluation | Classification metrics (accuracy, precision, recall, F1, confusion matrix), regression metrics (MSE, RMSE, MAE, R², MAPE) | `ModelEvaluator` |
| Experiment Tracking | Create, record, list, compare experiments with JSON persistence | `ExperimentDesigner` |
| Visualization | Histograms, scatter plots, bar charts, correlation heatmaps, ASCII rendering | `DataVisualizer` |
| Reproducibility | Data snapshots, pipeline hashing, environment capture, verification | `ReproducibilityManager` |
| Data Pipelines | Register steps, chain operations, run end-to-end with logging | `DataPipeline` |

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                  Data Science Agent                       │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Statistical  │  │     ML       │  │   Feature    │  │
│  │  Analyzer     │  │  Model Bldr  │  │  Engineer    │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                  │           │
│  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐  │
│  │  Preprocessor │  │  Evaluator   │  │  Tuner      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Experiment   │  │  Visualizer  │  │ Reproduci-   │  │
│  │  Designer     │  │              │  │ bility Mgr   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                          │
│              ┌──────────────────────────┐                │
│              │       DataPipeline       │                │
│              │  (orchestrates all)      │                │
│              └──────────────────────────┘                │
└──────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for full system design documentation.

---

## Quick Start

### Minimal Example (5 lines)

```python
from agent import StatisticalAnalyzer

sa = StatisticalAnalyzer()
result = sa.describe([10, 20, 30, 40, 50])
print(result)
# {'count': 5, 'mean': 30.0, 'median': 30.0, 'std': 14.142, ...}
```

### Full Pipeline Example

```python
from agent import (
    DataPreprocessor, ImputationStrategy,
    FeatureEngineer, MLModelBuilder, TaskType,
    ModelEvaluator, DataPipeline
)

# 1. Load and clean data
data = [
    {"age": 25, "income": 50000, "city": "NYC"},
    {"age": None, "income": 60000, "city": "LA"},
    {"age": 30, "income": 55000, "city": "NYC"},
]

dp = DataPreprocessor()
cleaned = dp.handle_missing(data, strategy=ImputationStrategy.MEAN, columns=["age"])

# 2. Encode categoricals
encoded, mappings = dp.encode(cleaned, columns=["city"])

# 3. Feature engineering
fe = FeatureEngineer()
features = fe.create_features(encoded, [
    {"name": "income_log", "transformation": "log", "column": "income"},
])

# 4. Train model
X = [[float(r.get("age", 0)), float(r.get("income", 0))] for r in features]
y = [float(r.get("income", 0)) for r in features]
builder = MLModelBuilder(task_type=TaskType.REGRESSION)
result = builder.train(X, y, model_type="linear")
print(f"R² = {result.metrics['r2']:.4f}")

# 5. Evaluate
evaluator = ModelEvaluator()
metrics = evaluator.regression_metrics(y, builder.predict(result.model_name, X))
print(metrics)
```

### Experiment Tracking Example

```python
from agent import ExperimentDesigner, TaskType

ed = ExperimentDesigner()

exp = ed.create_experiment(
    name="income-prediction-v1",
    description="Predict income from age and city",
    task_type=TaskType.REGRESSION,
    target_column="income",
    feature_columns=["age", "city"],
    hyperparameters={"model_type": "linear"}
)
print(f"Experiment created: {exp.experiment_id}")

# After running your model...
# ed.record_result(result)
# experiments = ed.list_experiments()
```

---

## Installation

No installation required — the agent is a single Python file with zero dependencies.

```bash
# Clone the repository
git clone <repo-url>
cd agents/data-science/

# Run the demo
python agent.py
```

### Optional Dependencies (for extended features)

```bash
pip install numpy scipy scikit-learn matplotlib seaborn
```

These are NOT required for the core agent. They extend functionality when available.

---

## Usage

### Statistical Analysis

```python
from agent import StatisticalAnalyzer

sa = StatisticalAnalyzer()

# Descriptive statistics
stats = sa.describe([25.0, 30.0, 35.0, 28.0, 42.0])
# → count, mean, median, std, variance, min, max, range,
#   q1, q3, iqr, skewness, kurtosis, sem, cv

# Two-sample t-test
t_result = sa.t_test(
    sample_a=[23.5, 25.1, 22.8, 24.9, 26.0],
    sample_b=[28.1, 30.2, 27.5, 29.8, 31.0],
    alpha=0.05
)
# → t_statistic, p_value, significant, mean_a, mean_b, degrees_of_freedom

# Correlation matrix
matrix = sa.correlation_matrix(data, columns=["x", "y", "z"])

# Outlier detection
outlier_indices = sa.detect_outliers(values, method="iqr", threshold=1.5)

# Normality test
normality = sa.normality_test(values, alpha=0.05)
```

### ML Model Development

```python
from agent import MLModelBuilder, TaskType

# Classification
builder = MLModelBuilder(task_type=TaskType.CLASSIFICATION)
result = builder.train(X_train, y_train, model_type="stump")
predictions = builder.predict(result.model_name, X_test)
cv = builder.cross_validate(X, y, k=5)

# Regression
reg_builder = MLModelBuilder(task_type=TaskType.REGRESSION)
result = reg_builder.train(X_train, y_train, model_type="linear")
predictions = reg_builder.predict(result.model_name, X_test)
```

### Feature Engineering

```python
from agent import FeatureEngineer

fe = FeatureEngineer()

# Create derived features
specs = [
    {"name": "revenue", "transformation": "interaction",
     "column1": "price", "column2": "quantity"},
    {"name": "price_log", "transformation": "log", "column": "price"},
    {"name": "date_parts", "transformation": "date_parts", "column": "date"},
]
enhanced = fe.create_features(data, specs)

# Select features by correlation
selected = fe.select_features(data, target_col="target", threshold=0.1)

# Generate polynomial features
poly = fe.polynomial_features(data, columns=["x", "y"], degree=3)
```

### Data Preprocessing

```python
from agent import DataPreprocessor, ImputationStrategy, NormalizationMethod, EncodingMethod

dp = DataPreprocessor()

# Impute missing values (7 strategies)
cleaned = dp.handle_missing(data, strategy=ImputationStrategy.MEAN)
cleaned = dp.handle_missing(data, strategy=ImputationStrategy.FORWARD_FILL)

# Normalize (6 methods)
normalized = dp.normalize(data, columns=["age", "income"], method=NormalizationMethod.ZSCORE)

# Encode categoricals (4 methods)
encoded, mappings = dp.encode(data, columns=["city"], method=EncodingMethod.LABEL)

# Remove duplicates
unique = dp.remove_duplicates(data, key_columns=["id"])

# Split data
X_train, X_test, y_train, y_test = dp.split_data(X, y, test_size=0.2)
```

### Experiment Tracking

```python
from agent import ExperimentDesigner, TaskType

ed = ExperimentDesigner(storage_dir=".experiments")

# Create, record, compare
exp = ed.create_experiment(name="test", description="...", task_type=TaskType.CLASSIFICATION, ...)
ed.record_result(result)
experiments = ed.list_experiments()
comparison = ed.compare_experiments([exp1_id, exp2_id])
```

### Visualization

```python
from agent import DataVisualizer

viz = DataVisualizer()

# Create specs and render ASCII
spec = viz.histogram(data, "score", bins=20)
ascii_chart = viz.render_ascii(spec, data)

# Scatter, bar, heatmap, boxplot
viz.scatter(data, x_col="age", y_col="income")
viz.boxplot(data, column="score", group_by="category")
```

### Reproducibility

```python
from agent import ReproducibilityManager, PipelineStep

rm = ReproducibilityManager()

# Snapshot and verify
record = rm.snapshot(data, pipeline_steps, seeds={"python": 42})
is_valid = rm.verify(record.record_id, data, pipeline_steps)
env = rm.get_environment()
```

### Hyperparameter Tuning

```python
from agent import HyperparameterTuner

tuner = HyperparameterTuner(builder)
grid = tuner.grid_search(X, y, param_grid={"model_type": ["stump", "linear"]})
random = tuner.random_search(X, y, param_distributions={"model_type": ["stump", "linear"]}, n_iter=10)
```

### Model Evaluation

```python
from agent import ModelEvaluator

evaluator = ModelEvaluator()
cls = evaluator.classification_metrics(actual, predicted)
reg = evaluator.regression_metrics(actual, predicted)
ranking = evaluator.compare_models([result1, result2])
```

### Data Pipelines

```python
from agent import DataPipeline

pipeline = DataPipeline()
pipeline.register("clean", clean_fn)
pipeline.register("train", train_fn)
pipeline.add_step("clean", "clean", {"strategy": "mean"})
pipeline.add_step("train", "train", {"model_type": "stump"})
result = pipeline.run(raw_data)
```

---

## API Reference

### StatisticalAnalyzer

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `describe()` | `values: Sequence[float]` | `Dict[str, float]` | Full descriptive statistics |
| `median()` | `sorted_values: List[float]` | `float` | Median of sorted list |
| `percentile()` | `sorted_values, p: float` | `float` | Linear-interpolation percentile |
| `t_test()` | `sample_a, sample_b, alpha` | `Dict[str, Any]` | Welch's two-sample t-test |
| `chi_square_test()` | `observed, expected, alpha` | `Dict[str, Any]` | Chi-squared goodness-of-fit |
| `correlation_matrix()` | `data, columns` | `Dict[str, Dict[str, float]]` | Pearson correlation matrix |
| `detect_outliers()` | `values, method, threshold` | `List[int]` | Outlier indices |
| `normality_test()` | `values, alpha` | `Dict[str, Any]` | Normality assessment |

### MLModelBuilder

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `train()` | `X, y, model_type, **kwargs` | `ModelResult` | Train a model |
| `predict()` | `model_id, X` | `List[Any]` | Run predictions |
| `cross_validate()` | `X, y, k, model_type` | `Dict[str, Any]` | k-fold cross-validation |

### FeatureEngineer

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `create_features()` | `data, specs` | `List[Dict]` | Derive new features |
| `select_features()` | `data, target_col, method, threshold` | `List[str]` | Feature selection |
| `polynomial_features()` | `data, columns, degree` | `List[Dict]` | Polynomial terms |

### DataPreprocessor

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `handle_missing()` | `data, strategy, columns, fill_value` | `List[Dict]` | Impute/drop missing |
| `normalize()` | `data, columns, method` | `List[Dict]` | Normalize features |
| `encode()` | `data, columns, method` | `Tuple[List, Dict]` | Encode categoricals |
| `remove_duplicates()` | `data, key_columns` | `List[Dict]` | Deduplicate rows |
| `split_data()` | `X, y, test_size, strategy, random_state` | `Tuple[4 lists]` | Train/test split |

### HyperparameterTuner

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `grid_search()` | `X, y, param_grid, X_val, y_val` | `Dict[str, Any]` | Exhaustive grid search |
| `random_search()` | `X, y, param_distributions, n_iter` | `Dict[str, Any]` | Random search |

### ModelEvaluator

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `classification_metrics()` | `actual, predicted` | `Dict[str, Any]` | Acc, precision, recall, F1, CM |
| `regression_metrics()` | `actual, predicted` | `Dict[str, float]` | MSE, RMSE, MAE, R², MAPE |
| `compare_models()` | `results: List[ModelResult]` | `List[Dict]` | Rank models by metric |

### ExperimentDesigner

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `create_experiment()` | `name, description, task_type, ...` | `ExperimentConfig` | Create experiment |
| `record_result()` | `result: ExperimentResult` | `None` | Store outcome |
| `list_experiments()` | — | `List[ExperimentConfig]` | List all experiments |
| `compare_experiments()` | `experiment_ids` | `List[Dict]` | Compare results |

### DataVisualizer

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `histogram()` | `data, column, bins, title` | `VisualizationSpec` | Histogram spec |
| `scatter()` | `data, x_col, y_col, hue` | `VisualizationSpec` | Scatter spec |
| `correlation_heatmap()` | `matrix, title` | `VisualizationSpec` | Heatmap spec |
| `boxplot()` | `data, column, group_by` | `VisualizationSpec` | Boxplot spec |
| `render_ascii()` | `spec, data` | `str` | ASCII chart |

### ReproducibilityManager

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `snapshot()` | `data, pipeline_steps, seeds` | `ReproducibilityRecord` | Create snapshot |
| `verify()` | `record_id, data, pipeline_steps` | `bool` | Verify match |
| `get_environment()` | — | `Dict[str, str]` | Current environment |

### DataPipeline

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `register()` | `name, fn` | `None` | Register step function |
| `add_step()` | `name, function_name, parameters, depends_on` | `PipelineStep` | Add pipeline step |
| `run()` | `data, **global_context` | `Any` | Execute pipeline |
| `to_dict()` | — | `List[Dict]` | Export pipeline def |

---

## Examples

### Example 1: Customer Churn Analysis

```python
from agent import (
    StatisticalAnalyzer, DataPreprocessor, FeatureEngineer,
    MLModelBuilder, TaskType, ModelEvaluator, ExperimentDesigner
)

# Profile the data
sa = StatisticalAnalyzer()
print(sa.describe([25.0, 30.0, 35.0, 28.0]))  # tenure stats

# Clean
dp = DataPreprocessor()
cleaned = dp.handle_missing(data, strategy=ImputationStrategy.MEAN)

# Engineer features
fe = FeatureEngineer()
features = fe.create_features(cleaned, [
    {"name": "charge_per_tenure", "transformation": "ratio",
     "column1": "monthly_charge", "column2": "tenure"},
])

# Train
builder = MLModelBuilder(task_type=TaskType.CLASSIFICATION)
X = [[float(r["tenure"]), float(r["monthly_charge"])] for r in features]
y = [float(r["churned"]) for r in features]
result = builder.train(X, y, model_type="stump")
print(f"Accuracy: {result.metrics['accuracy']:.2%}")

# Evaluate
evaluator = ModelEvaluator()
preds = builder.predict(result.model_name, X)
metrics = evaluator.classification_metrics(y, preds)
print(f"F1: {metrics['macro_f1']:.3f}")
```

### Example 2: Sales Forecasting

```python
from agent import StatisticalAnalyzer, FeatureEngineer

sa = StatisticalAnalyzer()
fe = FeatureEngineer()

# Analyze historical sales
stats = sa.describe(sales_values)
print(f"Mean daily sales: {stats['mean']:.0f}")
print(f"Std: {stats['std']:.0f}")

# Create time features
features = fe.create_features(sales_data, [
    {"name": "day_of_week", "transformation": "date_parts", "column": "date"},
    {"name": "sales_lag7", "transformation": "ratio", "column1": "sales", "column2": "sales_prev7"},
])

# Detect outliers (unusual sales days)
outliers = sa.detect_outliers(sales_values, method="zscore", threshold=2.5)
print(f"Unusual sales days: {len(outliers)}")
```

### Example 3: A/B Test Analysis

```python
from agent import StatisticalAnalyzer

sa = StatisticalAnalyzer()

# Control group vs treatment group
control = [12.5, 13.1, 11.8, 12.9, 13.5, 12.0, 12.8]
treatment = [14.2, 15.0, 13.8, 14.5, 15.2, 14.0, 14.8]

result = sa.t_test(control, treatment, alpha=0.05)
print(f"p-value: {result['p_value']:.4f}")
print(f"Significant: {result['significant']}")
print(f"Control mean: {result['mean_a']:.2f}")
print(f"Treatment mean: {result['mean_b']:.2f}")
```

---

## Data Models

### Enums

| Enum | Values | Usage |
|------|--------|-------|
| `DataType` | NUMERICAL, CATEGORICAL, TEMPORAL, TEXT, BINARY | Column type inference |
| `TaskType` | CLASSIFICATION, REGRESSION, CLUSTERING, DIMENSIONALITY_REDUCTION, TIME_SERIES | ML task selection |
| `ImputationStrategy` | MEAN, MEDIAN, MODE, CONSTANT, DROP, FORWARD_FILL, BACKWARD_FILL, KNN | Missing value handling |
| `NormalizationMethod` | MINMAX, ZSCORE, ROBUST, MAXABS, L1, L2 | Feature scaling |
| `EncodingMethod` | ONEHOT, LABEL, ORDINAL, TARGET, FREQUENCY, BINARY | Categorical encoding |
| `SplitStrategy` | RANDOM, STRATIFIED, TEMPORAL, KFOLD, STRATIFIED_KFOLD | Data splitting |
| `ExperimentStatus` | DRAFT, RUNNING, COMPLETED, FAILED, CANCELLED | Experiment lifecycle |
| `VisType` | HISTOGRAM, SCATTER, BAR, LINE, BOX, HEATMAP, PAIR, VIOLIN | Chart types |

### Dataclasses

| Dataclass | Key Fields | Description |
|-----------|-----------|-------------|
| `DataProfile` | column_name, data_type, count, missing_values, unique_values, statistics, quality_score | Column profiling result |
| `FeatureImportance` | feature_name, importance_score, rank, method | Feature ranking entry |
| `ModelResult` | model_name, task_type, metrics, parameters, feature_importances, training_time_seconds, model_hash, fitted | Trained model container |
| `ExperimentConfig` | experiment_id, name, description, task_type, target_column, feature_columns, hyperparameters, split_strategy, test_size, random_state, created_at, status | Experiment specification |
| `ExperimentResult` | experiment_id, model_result, predictions, actuals, cross_val_scores, confusion_matrix, completed_at | Experiment outcome |
| `VisualizationSpec` | vis_type, title, x_column, y_column, hue_column, bins, figsize, output_path | Chart specification |
| `PipelineStep` | step_id, name, function_name, parameters, depends_on | Pipeline unit |
| `ReproducibilityRecord` | record_id, pipeline_hash, data_hash, random_seeds, environment, timestamp | Reproducibility snapshot |

### Return Value Shapes

**StatisticalAnalyzer.describe() returns:**
```python
{
    "count": int,        # Number of observations
    "mean": float,       # Arithmetic mean
    "median": float,     # Median value
    "std": float,        # Standard deviation
    "variance": float,   # Variance
    "min": float,        # Minimum value
    "max": float,        # Maximum value
    "range": float,      # max - min
    "q1": float,         # 25th percentile
    "q3": float,         # 75th percentile
    "iqr": float,        # Interquartile range
    "skewness": float,   # Distribution skewness
    "kurtosis": float,   # Distribution kurtosis
    "sem": float,        # Standard error of mean
    "cv": float          # Coefficient of variation
}
```

**StatisticalAnalyzer.t_test() returns:**
```python
{
    "t_statistic": float,    # t-test statistic
    "p_value": float,        # Two-tailed p-value
    "significant": bool,     # p < alpha
    "mean_a": float,         # Sample A mean
    "mean_b": float,         # Sample B mean
    "degrees_of_freedom": int
}
```

**ModelEvaluator.classification_metrics() returns:**
```python
{
    "accuracy": float,
    "macro_precision": float,
    "macro_recall": float,
    "macro_f1": float,
    "per_class": {
        "class_name": {"precision": float, "recall": float, "f1": float}
    },
    "confusion_matrix": [[int]],
    "classes": [str]
}
```

**ModelEvaluator.regression_metrics() returns:**
```python
{
    "mse": float,    # Mean squared error
    "rmse": float,   # Root mean squared error
    "mae": float,    # Mean absolute error
    "r2": float,     # R-squared
    "mape": float    # Mean absolute percentage error
}
```

---

## Configuration

### Logging

```python
import logging

# Enable debug logging
logging.getLogger("data_science_agent").setLevel(logging.DEBUG)

# Silence logging
logging.getLogger("data_science_agent").setLevel(logging.WARNING)
```

### Experiment Storage

```python
# Default: .experiments/ directory
ed = ExperimentDesigner()

# Custom directory
ed = ExperimentDesigner(storage_dir="/path/to/experiments")
```

### Reproducibility Storage

```python
# Default: .reproducibility/ directory
rm = ReproducibilityManager()

# Custom directory
rm = ReproducibilityManager(base_dir="/path/to/snapshots")
```

### Random Seeds

```python
# All split/train operations accept random_state
dp.split_data(X, y, random_state=42)
tuner.random_search(X, y, param_distributions, random_state=42)
rm.snapshot(data, steps, seeds={"python": 42, "numpy": 42})
```

---

## Best Practices

### Data Analysis

1. **Always profile first** — Run `StatisticalAnalyzer.describe()` before any modeling
2. **Check for missing values** — Decide on strategy before proceeding
3. **Visualize distributions** — Histograms reveal skewness, multimodality
4. **Examine correlations** — High correlation (>0.8) between features = redundancy
5. **Test assumptions** — Normality, equal variance, independence

### Model Development

1. **Start simple** — Baseline model first, complexity only if needed
2. **Cross-validate** — Never trust a single train/test split
3. **Watch for overfitting** — Train accuracy >> test accuracy = problem
4. **Compare fairly** — Same split, same preprocessing for all models
5. **Report uncertainty** — Include std of CV scores in all reports

### Experiment Tracking

1. **Name experiments descriptively** — "churn-v2-imbalance-handling" not "test1"
2. **Record everything** — Hyperparameters, data hash, random seeds
3. **Compare systematically** — Use `compare_experiments()` to rank
4. **Document conclusions** — What worked, what didn't, what's next

### Reproducibility

1. **Set random seeds** — Every random operation should use a seed
2. **Snapshot before major changes** — `ReproducibilityManager.snapshot()`
3. **Verify after re-runs** — `verify()` confirms data+pipeline match
4. **Capture environment** — Python version, platform, dependencies

### Code Quality

1. **Use type hints** — All public methods are fully typed
2. **Handle edge cases** — Empty data, zero variance, division by zero
3. **Log meaningfully** — Operation name, row count, timing
4. **Fail fast** — Validate inputs before processing

---

## Common Workflows

### Workflow 1: Exploratory Data Analysis (EDA)

```python
from agent import StatisticalAnalyzer, DataPreprocessor, DataVisualizer

sa = StatisticalAnalyzer()
dp = DataPreprocessor()
viz = DataVisualizer()

# Step 1: Basic profiling
for col in numeric_columns:
    vals = [float(r[col]) for r in data if r.get(col) is not None]
    print(f"{col}: {sa.describe(vals)}")

# Step 2: Missing value analysis
cleaned = dp.handle_missing(data, strategy=ImputationStrategy.DROP)

# Step 3: Outlier detection
for col in numeric_columns:
    vals = [float(r[col]) for r in cleaned if r.get(col) is not None]
    outliers = sa.detect_outliers(vals, method="iqr")
    print(f"{col}: {len(outliers)} outliers")

# Step 4: Correlation analysis
matrix = sa.correlation_matrix(cleaned, columns=numeric_columns)
for col1 in matrix:
    for col2 in matrix[col1]:
        if col1 != col2 and abs(matrix[col1][col2]) > 0.7:
            print(f"High correlation: {col1} <-> {col2}: {matrix[col1][col2]:.3f}")

# Step 5: Visualize
for col in numeric_columns:
    spec = viz.histogram(cleaned, col)
    print(viz.render_ascii(spec, cleaned))
```

### Workflow 2: Model Selection

```python
from agent import (
    DataPreprocessor, MLModelBuilder, TaskType,
    HyperparameterTuner, ModelEvaluator
)

dp = DataPreprocessor()
X_train, X_test, y_train, y_test = dp.split_data(X, y, test_size=0.2)

# Train multiple models
builder = MLModelBuilder(task_type=TaskType.CLASSIFICATION)
models_to_try = ["stump", "linear"]
results = []

for mt in models_to_try:
    result = builder.train(X_train, y_train, model_type=mt)
    preds = builder.predict(result.model_name, X_test)
    evaluator = ModelEvaluator()
    metrics = evaluator.classification_metrics(y_test, preds)
    results.append(result)
    print(f"{mt}: accuracy={metrics['accuracy']:.3f}, f1={metrics['macro_f1']:.3f}")

# Rank
ranking = evaluator.compare_models(results)
print(f"Best model: {ranking[0]['model_name']}")

# Tune best model
tuner = HyperparameterTuner(builder)
tuned = tuner.grid_search(X_train, y_train, param_grid={"model_type": ["stump", "linear"]})
print(f"Best params after tuning: {tuned['best_params']}")
```

### Workflow 3: Reproducible Experiment

```python
from agent import (
    ExperimentDesigner, ReproducibilityManager, PipelineStep, TaskType
)

ed = ExperimentDesigner()
rm = ReproducibilityManager()

# Define pipeline
steps = [
    PipelineStep("s1", "clean", "handle_missing", {"strategy": "mean"}),
    PipelineStep("s2", "encode", "encode", {"columns": ["city"]}),
    PipelineStep("s3", "train", "train", {"model_type": "stump"}),
]

# Snapshot before run
record = rm.snapshot(data=data, pipeline_steps=steps, seeds={"python": 42})
print(f"Snapshot: {record.record_id}, data_hash={record.data_hash}")

# Run experiment
exp = ed.create_experiment(
    name="reproducible-test",
    description="Test reproducibility workflow",
    task_type=TaskType.CLASSIFICATION,
    target_column="target",
    feature_columns=["x1", "x2"],
)

# ... run your pipeline ...

# Verify reproducibility
is_valid = rm.verify(record.record_id, data=data, pipeline_steps=steps)
print(f"Reproducibility verified: {is_valid}")

# Compare with previous run
ed.compare_experiments([exp.experiment_id])
```

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `ValueError: Cannot describe an empty sequence` | Empty dataset | Check data loading, verify row count > 0 |
| Division by zero in normalization | Constant column (max == min) | Check for constant columns before normalizing |
| Model predicts single class | All labels identical or perfect separation | Check label distribution, try different model |
| High CV score variance | Small dataset or unstable model | Increase data, simplify model, increase k |
| `KeyError: No function registered` | Pipeline step references unknown function | Call `pipeline.register()` before adding step |
| Experiment files not found | Storage directory moved or deleted | Check `.experiments/` directory exists |
| Reproducibility verify fails | Data or pipeline changed since snapshot | Compare hashes to identify what changed |
| `IndexError` on split | Dataset too small for requested split ratio | Increase data or reduce `test_size` |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)
# All operations log detailed information
```

---

## Contributing

### Development Setup

```bash
git clone <repo-url>
cd agents/data-science/
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### Code Standards

- Python 3.10+ required
- All public methods must have type hints
- All public methods must have docstrings
- Error messages must be descriptive
- Logging at INFO level for major operations
- No external dependencies in core `agent.py`

### Testing

```bash
python agent.py  # Run built-in demo
python -m pytest tests/  # If tests exist
```

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Add type hints to all new code
4. Add docstrings to all public methods
5. Ensure `python agent.py` runs without errors
6. Submit PR with description of changes

---

## License

MIT License

```
MIT License

Copyright (c) 2024 MiMoCode

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
