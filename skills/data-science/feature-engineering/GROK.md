---
name: "Feature Engineering"
version: "2.0.0"
description: "Comprehensive feature engineering toolkit with automated feature construction, encoding, scaling, selection, interaction detection, and pipeline orchestration for machine learning workflows"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["data-science", "feature-engineering", "preprocessing", "pipelines", "selection", "encoding"]
category: "data-science"
personality: "feature-engineer"
use_cases: ["feature construction", "data preprocessing", "feature selection", "pipeline automation", "dimensionality reduction"]
---

# Feature Engineering

> Production-grade feature engineering toolkit providing automated feature construction, encoding, scaling, selection, interaction detection, and pipeline orchestration for building high-quality ML inputs.

## Overview

The Feature Engineering module provides a unified, composable pipeline for transforming raw data into ML-ready features. It handles missing value imputation (mean, median, KNN, MICE), categorical encoding (one-hot, target, ordinal, frequency), numerical transformations (log, Box-Cox, Yeo-Johnson, power), feature scaling (standard, minmax, robust, quantile), automated feature construction (polynomial, interaction, lag, rolling), feature selection (filter, wrapper, embedded, stability), and dimensionality reduction (PCA, UMAP, autoencoders). Every transformer exposes fit/transform/fit_transform interfaces with serialization support for production deployment.

## Core Capabilities

### 1. Missing Value Imputation
- Statistical: mean, median, mode, constant, forward-fill, backward-fill
- Model-based: KNN imputation, iterative (MICE) imputation
- Indicator flags: create missingness indicator columns
- Missing pattern analysis: MCAR/MAR/MNAR diagnostics

### 2. Categorical Encoding
- One-hot encoding with automatic cardinality management
- Target encoding with regularization and cross-fitting
- Ordinal encoding with customizable ordering
- Frequency/count encoding
- Binary encoding for high-cardinality features
- Leave-one-out encoding for rare categories

### 3. Numerical Transformations
- Log, square root, Box-Cox, Yeo-Johnson power transforms
- Quantile normalization to Gaussian
- Polynomial feature generation (degree 2-5)
- Binning: equal-width, equal-frequency, custom thresholds
- Date/time decomposition: year, month, day, day-of-week, hour, is_weekend, cyclical encoding

### 4. Feature Scaling
- StandardScaler (zero mean, unit variance)
- MinMaxScaler (bounded range)
- RobustScaler (median/IQR, outlier-resistant)
- QuantileScaler (uniform or Gaussian output)
- MaxAbsScaler (sparse-compatible)

### 5. Feature Selection and Importance
- Filter methods: correlation, mutual information, chi-squared, variance threshold
- Wrapper methods: recursive feature elimination (RFE), forward/backward selection
- Embedded methods: L1 regularization, tree importance, permutation importance
- Stability selection: bootstrap-based consistent feature identification
- Dimensionality reduction: PCA, incremental PCA, UMAP

### 6. Automated Feature Construction
- Polynomial and interaction features
- Lag features for time series
- Rolling window statistics (mean, std, min, max, skew)
- Expanding window aggregates
- Text-derived features (length, word count, special char ratio)
- Aggregation features (group-by + aggregate)

## Usage Examples

### Complete Preprocessing Pipeline

```python
from feature_engineering import FeaturePipeline, PipelineStep

pipeline = FeaturePipeline(name="customer_churn_pipeline")

# Step 1: Imputation
pipeline.add_step(PipelineStep(
    name="impute",
    transformer="iterative_imputer",
    params={"max_iter": 10, "random_state": 42, "initial_strategy": "mean"},
    columns=["age", "income", "tenure_months"],
))

# Step 2: Encoding
pipeline.add_step(PipelineStep(
    name="encode_categoricals",
    transformer="target_encoder",
    params={"smoothing": 10, "min_samples_leaf": 5, "cross_folds": 5},
    columns=["plan_type", "region", "acquisition_channel"],
))

# Step 3: Scaling
pipeline.add_step(PipelineStep(
    name="scale_numerics",
    transformer="robust_scaler",
    params={"quantile_range": (25, 75)},
    columns=["age", "income", "tenure_months", "monthly_charges"],
))

# Step 4: Feature construction
pipeline.add_step(PipelineStep(
    name="construct_features",
    transformer="polynomial_features",
    params={"degree": 2, "interaction_only": True, "include_bias": False},
    columns=["age", "income", "monthly_charges"],
))

# Step 5: Feature selection
pipeline.add_step(PipelineStep(
    name="select_features",
    transformer="mutual_information_selector",
    params={"k": 20, "discrete_features": "auto"},
))

# Fit and transform
X_train_transformed = pipeline.fit_transform(X_train, y=y_train)
X_test_transformed = pipeline.transform(X_test)

# Inspect pipeline
print(pipeline.summary())
print(f"Features before: {X_train.shape[1]}, after: {X_train_transformed.shape[1]}")
```

### Target Encoding with Cross-Fitting

```python
from feature_engineering import TargetEncoder

encoder = TargetEncoder(
    smoothing=10,
    min_samples_leaf=5,
    cross_folds=5,
    random_state=42,
)

# Fit on training data with target
X_encoded = encoder.fit_transform(X_train, y_train, categorical_columns=["city", "product"])

# Transform test data (uses global encoding from training)
X_test_encoded = encoder.transform(X_test, categorical_columns=["city", "product"])

# Inspect encoding maps
print(encoder.encoding_maps_)
print(encoder.feature_importances_)
```

### Automated Feature Construction

```python
from feature_engineering import FeatureConstructor

constructor = FeatureConstructor()

# Lag features for time series
lag_features = constructor.create_lag_features(
    data=df,
    column="sales",
    lags=[1, 7, 14, 28],
    group_column="store_id",
)

# Rolling window statistics
rolling_features = constructor.create_rolling_features(
    data=df,
    column="sales",
    windows=[7, 14, 30],
    functions=["mean", "std", "min", "max", "skew"],
    group_column="store_id",
)

# Interaction features
interaction_features = constructor.create_interactions(
    data=df,
    columns=["price", "quantity", "discount"],
    operations=["multiply", "divide", "add", "subtract"],
)

# Date decomposition
date_features = constructor.decompose_datetime(
    data=df,
    date_column="order_date",
    features=["year", "month", "day", "dayofweek", "hour", "is_weekend", "quarter"],
    cyclical=["month", "dayofweek", "hour"],
)

# Combine all
df_features = pd.concat([df, lag_features, rolling_features, interaction_features, date_features], axis=1)
```

### Feature Selection

```python
from feature_engineering import FeatureSelector, SelectionMethod

selector = FeatureSelector(random_state=42)

# Variance threshold
low_variance = selector.variance_threshold(X_train, threshold=0.01)
print(f"Removed {len(low_variance)} low-variance features")

# Correlation filter
uncorrelated = selector.correlation_filter(X_train, threshold=0.95)
print(f"Removed {len(uncorrelated)} highly correlated features")

# Mutual information
top_features = selector.mutual_information(
    X=X_train, y=y_train, k=20, task="classification"
)
print(f"Top features by MI: {top_features}")

# Stability selection
stable_features = selector.stability_selection(
    X=X_train, y=y_train,
    method="lasso",
    n_bootstrap=100,
    threshold=0.7,
    task="classification",
)
print(f"Stable features: {stable_features}")

# Combined pipeline
selected = selector.auto_select(
    X=X_train, y=y_train,
    methods=["variance", "correlation", "mutual_info", "stability"],
    k=15,
    task="classification",
)
```

## Best Practices

### Pipeline Design
- Always fit on training data only; never fit on test data to avoid data leakage
- Use cross-fitting for target encoding and other target-dependent transforms
- Include missingness indicators before imputation — missingness itself can be informative
- Serialize fitted pipelines for reproducible deployment

### Encoding Strategy
- One-hot for low-cardinality (< 10 categories); target encoding for high-cardinality
- Avoid ordinal encoding unless there is a true natural ordering
- Use frequency encoding when category frequency is the signal, not the label
- Always check for rare categories that may cause overfitting

### Feature Scaling
- Use RobustScaler when outliers are present; StandardScaler otherwise
- Tree-based models do not require scaling; linear models and neural networks do
- Fit scalers on training data and transform both train and test
- For sparse data, use MaxAbsScaler to preserve sparsity

### Feature Selection
- Start with filter methods to remove obviously irrelevant features
- Use embedded methods (L1, tree importance) for model-aware selection
- Stability selection guards against selecting features due to random chance
- Validate selected features on a hold-out set before finalizing

## Related Modules

- **statistical-analysis**: Statistical tests for feature significance
- **advanced-analytics**: Multivariate analysis for feature relationships
- **time-series**: Temporal feature construction and decomposition
- **model-optimization**: Hyperparameter tuning for feature engineering parameters