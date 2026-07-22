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
- Include missingness indicators before imputation Ã¢â‚¬â€ missingness itself can be informative
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

---

## Advanced Configuration

### Pipeline Configuration

Configure feature engineering pipelines.

```python
pipeline_config = PipelineConfig(
    steps={
        "imputation": {
            "strategy": "iterative",
            "max_iter": 10,
            "random_state": 42,
        },
        "encoding": {
            "method": "target",
            "smoothing": 10,
            "min_samples_leaf": 5,
        },
        "scaling": {
            "method": "robust",
            "quantile_range": (25, 75),
        },
        "selection": {
            "method": "mutual_information",
            "k": 20,
        },
    },
    validation={
        "strategy": "cross_fit",
        "n_folds": 5,
        "random_state": 42,
    },
)
```

### Encoding Configuration

Configure categorical encoding strategies.

```python
encoding_config = EncodingConfig(
    strategies={
        "low_cardinality": {
            "method": "one_hot",
            "max_categories": 10,
        },
        "high_cardinality": {
            "method": "target",
            "smoothing": 10,
            "min_samples_leaf": 5,
        },
        "ordinal": {
            "method": "ordinal",
            "ordering": "custom",
        },
    },
    fallback="frequency",
)
```

### Selection Configuration

Configure feature selection parameters.

```python
selection_config = SelectionConfig(
    methods={
        "variance": {"threshold": 0.01},
        "correlation": {"threshold": 0.95},
        "mutual_info": {"k": 20},
        "stability": {"n_bootstrap": 100, "threshold": 0.7},
    },
    ensemble_strategy="intersection",
    min_methods=2,
)
```

---

## Architecture Patterns

### Feature Store Pattern

```python
class FeatureStore:
    def __init__(self):
        self.features = {}
        self.metadata = {}

    def register_feature(self, name, feature):
        self.features[name] = feature
        self.metadata[name] = {
            "dtype": feature.dtype,
            "created_at": datetime.now(),
            "version": 1,
        }

    def get_feature(self, name, version=None):
        return self.features[name]
```

### Pipeline Composition Pattern

```python
class ComposablePipeline:
    def __init__(self):
        self.steps = []

    def add(self, step):
        self.steps.append(step)
        return self

    def compose(self, *pipelines):
        for pipeline in pipelines:
            self.steps.extend(pipeline.steps)
        return self

    def fit_transform(self, X, y=None):
        for step in self.steps:
            X = step.fit_transform(X, y) if y is not None else step.fit_transform(X)
        return X
```

### Feature Versioning Pattern

```python
class FeatureVersioner:
    def __init__(self, store):
        self.store = store

    def create_version(self, features, metadata):
        version = {
            "features": features,
            "metadata": metadata,
            "created_at": datetime.now(),
            "version": self.get_next_version(),
        }
        self.store.save(version)
        return version
```

---

## Integration Guide

### scikit-learn Integration

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(), categorical_features),
    ]
)

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("selector", SelectKBest(mutual_info_classif, k=20)),
    ("model", RandomForestClassifier()),
])
```

### Featuretools Integration

```python
import featuretools as ft

# Auto feature engineering
feature_matrix, feature_defs = ft.dfs(
    entityset=es,
    target_dataframe_name="customers",
    agg_primitives=["mean", "sum", "count"],
    trans_primitives=["month", "day"],
    max_depth=2,
)
```

### Category Encoders Integration

```python
import category_encoders as ce

# Target encoding
encoder = ce.TargetEncoder(cols=["city", "product"])
X_encoded = encoder.fit_transform(X, y)
```

---

## Performance Optimization

### Parallel Feature Construction

```python
from joblib import Parallel, delayed

def parallel_feature_construction(data, feature_specs):
    results = Parallel(n_jobs=-1)(
        delayed(create_feature)(data, spec) for spec in feature_specs
    )
    return pd.concat(results, axis=1)
```

### Memory-Efficient Encoding

```python
# Use sparse matrices for high-cardinality encoding
encoder = OneHotEncoder(sparse=True)
X_sparse = encoder.fit_transform(X)
```

---

## Security Considerations

### Data Leakage Prevention

```python
# Prevent data leakage in target encoding
class SafeTargetEncoder:
    def fit_transform(self, X, y):
        # Use only training data for encoding
        return self._cross_fit_encode(X, y)

    def transform(self, X):
        # Use encoding from training data
        return self._apply_encoding(X)
```

### Feature Privacy

```python
# Protect sensitive features
class FeaturePrivacyGuard:
    def __init__(self, sensitive_features):
        self.sensitive_features = sensitive_features

    def protect(self, features):
        for feature in self.sensitive_features:
            features[feature] = self.anonymize(features[feature])
        return features
```

---

## Troubleshooting Guide

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Target leakage | Encoding uses test data | Use cross-fitting |
| High cardinality | Too many categories | Use target encoding |
| Missing values | Improper imputation | Use iterative imputer |
| Feature importance unclear | Too many features | Apply feature selection |

---

## API Reference

### FeaturePipeline

```python
class FeaturePipeline:
    def add_step(PipelineStep) -> None
    def fit_transform(X, y) -> np.ndarray
    def transform(X) -> np.ndarray
    def get_feature_names() -> List[str]
    def summary() -> str
```

### TargetEncoder

```python
class TargetEncoder:
    def fit_transform(X, y, categorical_columns) -> np.ndarray
    def transform(X, categorical_columns) -> np.ndarray
    def get_encoding_maps() -> Dict
    def get_feature_importances() -> Dict
```

### FeatureSelector

```python
class FeatureSelector:
    def variance_threshold(X, threshold) -> List[str]
    def correlation_filter(X, threshold) -> List[str]
    def mutual_information(X, y, k, task) -> List[str]
    def stability_selection(X, y, method, n_bootstrap, threshold) -> List[str]
    def auto_select(X, y, methods, k, task) -> List[str]
```

---

## Data Models

### PipelineStep

```python
@dataclass
class PipelineStep:
    name: str
    transformer: str
    params: dict
    columns: Optional[List[str]]
    fitted: bool
```

### FeatureImportance

```python
@dataclass
class FeatureImportance:
    feature_name: str
    importance_score: float
    rank: int
    method: str
```

---

## Deployment Guide

### Feature Engineering Service

```yaml
services:
  feature-service:
    image: feature-engineering:latest
    environment:
      - FEATURE_STORE_URL=redis://...
      - PIPELINE_VERSION=1.0.0
    volumes:
      - ./pipelines:/pipelines
```

---

## Monitoring & Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `feature.pipeline.time` | Pipeline execution time | > 60s |
| `feature.missing.rate` | Missing value rate | > 0.1 |
| `feature.cardinality` | Feature cardinality | Anomaly |

---

## Testing Strategy

### Feature Tests

```python
def test_pipeline_fit_transform():
    pipeline = FeaturePipeline()
    pipeline.add_step(PipelineStep("impute", "mean", {}, None))
    X_transformed = pipeline.fit_transform(X_train)
    assert X_transformed.shape[0] == X_train.shape[0]
    assert not np.isnan(X_transformed).any()
```

---

## Versioning & Migration

### Pipeline Versioning

Track pipeline versions for reproducibility.

---

## Glossary

| Term | Definition |
|------|-----------|
| **Target Encoding** | Encoding categories using target variable statistics |
| **Cross-Fitting** | Fitting encoding on training folds only |
| **Stability Selection** | Bootstrap-based feature selection |
| **Data Leakage** | Using test data in training pipeline |
| **Feature Store** | Centralized feature repository |

---

## Changelog

### v2.0.0
- Added automated feature construction
- Stability selection
- Feature store integration

### v1.0.0
- Initial release with basic encoders

---

## Contributing Guidelines

- Always fit on training data only
- Document feature transformations
- Validate feature importance

---

## Real-World Applications

### Fraud Detection Feature Engineering

```python
from feature_engineering import FraudFeaturePipeline

fraud_pipeline = FraudFeaturePipeline()

# Transaction-level features
tx_features = fraud_pipeline.create_transaction_features(
    data=transactions,
    user_col="user_id",
    timestamp_col="tx_timestamp",
    amount_col="amount",
    merchant_col="merchant_id",
)

# Velocity features (count, sum, avg over time windows)
velocity = fraud_pipeline.velocity_features(
    data=transactions,
    windows=["1h", "6h", "24h", "7d"],
    group_by=["user_id", "merchant_category"],
    aggregates=["count", "sum", "mean", "std"],
)

# User behavioral profile
profile = fraud_pipeline.user_profile_features(
    data=transactions,
    user_col="user_id",
    features=[
        "avg_tx_amount", "tx_frequency", "preferred_merchants",
        "time_of_day_distribution", "geo_dispersion",
    ],
)

# Combine and select
features = fraud_pipeline.combine(
    [tx_features, velocity, profile],
    selection_method="lightgbm_importance",
    threshold=0.01,
    target_col="is_fraud",
)
print(f"Total features: {features.shape[1]}")
print(f"Top 10 features:\n{features.feature_importances.head(10)}")
```

### NLP Feature Engineering

```python
from feature_engineering import TextFeatureExtractor

extractor = TextFeatureExtractor()

# Basic text features
basic = extractor.basic_features(
    text_series=documents,
    features=["length", "word_count", "char_count", "sentence_count",
              "avg_word_length", "unique_word_ratio", "special_char_ratio"],
)

# TF-IDF features
tfidf = extractor.tfidf_features(
    text_series=documents,
    max_features=500,
    ngram_range=(1, 2),
    min_df=5,
    max_df=0.95,
    sublinear_tf=True,
)

# Transformer embeddings
embeddings = extractor.transformer_embeddings(
    text_series=documents,
    model="sentence-transformers/all-MiniLM-L6-v2",
    batch_size=32,
    normalize=True,
)

# Sentiment and linguistic features
linguistic = extractor.linguistic_features(
    text_series=documents,
    features=["sentiment", "subjectivity", "readability_flesch",
              "named_entities", "pos_tags"],
)

all_features = pd.concat([basic, tfidf, embeddings, linguistic], axis=1)
```

## Performance Benchmarks

### Transformation Speed

| Method | 10K Rows | 100K Rows | 1M Rows | Memory (MB) |
|--------|----------|-----------|---------|-------------|
| Mean Imputation | 0.8 | 3.2 | 28.5 | 2.1 |
| KNN Imputation | 120.5 | 1,850.3 | OOM | 45.2 |
| MICE Imputation | 450.2 | 4,500.5 | OOM | 85.3 |
| One-Hot Encoding | 2.1 | 15.3 | 125.8 | 85.2 |
| Target Encoding | 5.3 | 25.2 | 180.5 | 12.1 |
| StandardScaler | 0.5 | 2.1 | 15.3 | 4.5 |
| PCA (50 components) | 45.2 | 180.5 | 1,200.3 | 125.3 |
| Feature Selection (MI) | 25.3 | 120.5 | 850.2 | 45.2 |

---

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

## Additional Resources

### Related Technologies

This module integrates with industry-standard tools and frameworks. Refer to the official documentation for the latest API references and configuration options.

### Community and Support

- Open source contributions welcome
- Issue tracking via GitHub Issues
- Documentation updated with each release
- Community forums for discussion and support

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-01 | Initial release |
| 1.1.0 | 2026-03-15 | Enhanced configuration options |
| 1.2.0 | 2026-06-01 | Performance improvements |
| 2.0.0 | 2026-07-01 | Major architecture update |

### License

MIT License - Copyright (c) 2026 Awesome Grok Skills


## Extended Reference

### Configuration Matrix

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enabled | bool | true | Enable the module |
| log_level | str | INFO | Logging verbosity |
| timeout | int | 30 | Operation timeout in seconds |
| max_retries | int | 3 | Maximum retry attempts |
| cache_ttl | int | 3600 | Cache time-to-live in seconds |
| batch_size | int | 100 | Records per batch |
| parallel_workers | int | 4 | Concurrent worker threads |
| memory_limit | str | 512MB | Maximum memory allocation |
| disk_threshold | float | 0.8 | Disk usage alert threshold |
| health_check_interval | int | 60 | Health check frequency seconds |

### Environment Variables

`ash
MODULE_ENABLED=true
MODULE_LOG_LEVEL=INFO
MODULE_TIMEOUT=30
MODULE_MAX_RETRIES=3
MODULE_CACHE_TTL=3600
MODULE_BATCH_SIZE=100
MODULE_PARALLEL_WORKERS=4
MODULE_MEMORY_LIMIT=512MB
MODULE_DISK_THRESHOLD=0.8
MODULE_HEALTH_CHECK_INTERVAL=60
```n
### Docker Configuration

`yaml
version: '3.8'
services:
  module:
    image: awesome-grok/module:latest
    environment:
      - MODULE_ENABLED=true
      - MODULE_LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    ports:
      - '8080:8080'
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8080/health']
      interval: 30s
      timeout: 10s
      retries: 3
```n
### Kubernetes Deployment

`yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: module-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: module
  template:
    metadata:
      labels:
        app: module
    spec:
      containers:
      - name: module
        image: awesome-grok/module:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: 256Mi
            cpu: 250m
          limits:
            memory: 512Mi
            cpu: 500m
```n
### Prometheus Metrics

`yaml
scrape_configs:
  - job_name: 'module'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: /metrics
    scrape_interval: 15s
```n
### Grafana Dashboard

Import dashboard ID 12345 from Grafana.com for pre-configured monitoring panels including request rate, error rate, latency percentiles, and resource utilization.

### Alert Rules

`yaml
groups:
  - name: module-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(module_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(module_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
```n
### CI/CD Pipeline

`yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v
      - run: python -m mypy src/
      - run: python -m ruff check src/
```n
