---
name: "quality-validation"
category: "synthetic-data"
version: "1.0.0"
tags: ["synthetic-data", "quality", "validation", "metrics", "statistics", "utility"]
---

# Synthetic Data Quality Validation Toolkit

## Overview

The `quality-validation` module provides a rigorous framework for evaluating the fidelity, utility, and privacy-utility tradeoff of synthetic datasets. Generating synthetic data is only half the battle; ensuring it is "good enough" for its intended purpose—whether that's training a model, sharing with third parties, or testing a system—requires comprehensive validation. This module implements a suite of statistical tests, machine learning utility metrics, and privacy-attack simulations to provide a multi-dimensional view of data quality.

A central concept in this module is the "Fidelity vs. Utility vs. Privacy" triangle. High-fidelity data (statistically similar to the original) might compromise privacy if it's too accurate. High-utility data (good for training models) might not be representative of the real world. This toolkit helps practitioners navigate these trade-offs by providing a unified `ValidationReport` that aggregates results from diverse tests, including Kolmogorov-Smirnov (KS) tests for distributional similarity, Wasserstein distance for measuring the "work" needed to transform one distribution into another, and Pearson/Spearman correlation preservation checks.

The module also includes a `SyntheticDataDetector` component, which attempts to distinguish between real and synthetic records using a binary classifier. If a detector can easily tell them apart, the synthetic data is likely failing to capture the complex, non-linear relationships present in the real data. By iterating on generative model parameters and re-running these validation checks, users can converge on a synthetic dataset that meets their specific quality requirements.

The module is designed to be generator-agnostic: it works with data produced by CTGAN, Gaussian Copulas, VAEs, or any other generative method. This allows organizations to benchmark different generators against the same validation suite and select the one that best meets their requirements.

## Core Capabilities

*   **Distribution Fidelity Metrics**: Calculate per-column similarity using KS tests, Wasserstein-1 distance, and Jensen-Shannon (JS) divergence.
*   **Correlation Preservation**: Compare the Pearson and Spearman correlation matrices of real and synthetic data to ensure relationships between variables are maintained.
*   **ML Utility Evaluation**: Train a "Shadow Model" (e.g., XGBoost or Random Forest) on both real and synthetic data and compare its performance on a held-out real test set.
*   **Synthetic Data Detection**: Train a binary classifier to distinguish real from synthetic records; a lower AUC indicates higher fidelity.
*   **Privacy-Utility Tradeoff Analysis**: Visualize how varying privacy budgets ($\epsilon$) in the generation process affects both data utility and privacy-attack resistance.
*   **Outlier Handling Analysis**: Compare the distribution and count of outliers (using IQR or Z-score) between real and synthetic datasets.
*   **Benchmarking Framework**: Run a standardized suite of tests across multiple synthetic data generation methods (e.g., CTGAN vs. Gaussian Copula) and rank them.
*   **Automated Reporting**: Generate a comprehensive HTML or PDF report summarizing all validation metrics and visualizations.
*   **Temporal Consistency Checks**: For time-series data, validate that autocorrelation structure, seasonal patterns, and trend components are preserved.
*   **Categorical Fidelity**: Evaluate whether the frequency distribution of categorical columns matches using chi-squared tests and total variation distance.
*   **Edge Case Coverage**: Assess whether rare but important values (e.g., extreme outliers, minority class samples) are represented in the synthetic data.
*   **Drift Detection**: Compare the distribution shift between real and synthetic data using Population Stability Index (PSI) and Kolmogorov-Smirnov statistics over time.

## Quality Metric Taxonomy

### Statistical Fidelity Metrics

| Metric | What It Measures | Good Threshold | Interpretation |
|--------|-----------------|----------------|----------------|
| **KS Test (p-value)** | Per-column distribution similarity | p > 0.05 | Cannot reject null hypothesis that distributions are the same |
| **Wasserstein-1 Distance** | "Earth mover's distance" between distributions | Close to 0 | Less "work" to transform one distribution into the other |
| **Jensen-Shannon Divergence** | Symmetric divergence between distributions | < 0.01 | Distributions are nearly identical |
| **Total Variation Distance** | Maximum difference in probability mass | < 0.05 | Probability mass functions are close |
| **Chi-Squared Test** | Categorical frequency distribution similarity | p > 0.05 | Cannot reject null hypothesis for categorical distributions |
| **PSI (Population Stability Index)** | Distribution shift between real and synthetic | < 0.1 | Minimal shift; 0.1-0.25 is moderate; > 0.25 is significant |

### Correlation Preservation Metrics

| Metric | What It Measures | Good Threshold |
|--------|-----------------|----------------|
| **Pearson Correlation Delta** | Mean absolute difference in Pearson r matrices | < 0.1 |
| **Spearman Correlation Delta** | Mean absolute difference in Spearman rho matrices | < 0.1 |
| **Mutual Information Delta** | Difference in pairwise mutual information | < 0.05 |
| **Copula Dependency Preservation** | Rank correlation structure similarity | High agreement |

### ML Utility Metrics

| Metric | What It Measures | Good Threshold |
|--------|-----------------|----------------|
| **Utility Ratio** | synthetic_AUC / real_AUC | > 0.85 |
| **Accuracy Delta** | |synthetic_acc - real_acc| | < 5% |
| **F1 Delta** | |synthetic_f1 - real_f1| | < 5% |
| **Shadow Model AUC** | Ability to distinguish real vs. synthetic | Close to 0.5 (random) |
| **Feature Importance Correlation** | Agreement of feature importances between models | > 0.9 |

## Usage Examples

### 1. Basic Fidelity Check

```python
import pandas as pd
from quality_validation import FidelityEvaluator

# Load real and synthetic data
real_data = pd.read_csv("real_data.csv")
synthetic_data = pd.read_csv("synthetic_data.csv")

# Initialize evaluator
evaluator = FidelityEvaluator()

# Run per-column KS tests
ks_results = evaluator.ks_test(real_data, synthetic_data)

print("Kolmogorov-Smirnov Test Results (p-values):")
for col, p_val in ks_results.items():
    status = "PASS" if p_val > 0.05 else "FAIL"
    print(f"  {col}: {p_val:.4f} [{status}]")
```

### 2. ML Utility Evaluation

```python
from quality_validation import UtilityEvaluator

# Define the prediction task
target_column = "is_fraud"

# Initialize utility evaluator
util_eval = UtilityEvaluator(target=target_column, model_type="xgboost")

# Compare model performance
report = util_eval.compare(
    real_train=pd.read_csv("real_train.csv"),
    synthetic_train=pd.read_csv("synthetic_train.csv"),
    real_test=pd.read_csv("real_test.csv")
)

print(f"Model AUC on Real Data: {report['real_auc']:.4f}")
print(f"Model AUC on Synthetic Data: {report['synthetic_auc']:.4f}")
print(f"Utility Ratio: {report['utility_ratio']:.4f}")
```

### 3. Generating a Full Validation Report

```python
from quality_validation import ValidationSuite

# Run a full suite of tests
suite = ValidationSuite(
    real_data=real_data,
    synthetic_data=synthetic_data,
    metadata={"task": "customer_churn_prediction", "privacy_budget": 0.8}
)

# Generate the report
report_path = suite.generate_report(output_format="html")
print(f"Full validation report saved to: {report_path}")
```

### 4. Benchmarking Multiple Generators

```python
from quality_validation import BenchmarkSuite

# Compare multiple synthetic datasets against the same real data
benchmark = BenchmarkSuite(real_data=real_data)

benchmark.add_synthetic("CTGAN", pd.read_csv("synthetic_ctgan.csv"))
benchmark.add_synthetic("GaussianCopula", pd.read_csv("synthetic_gc.csv"))
benchmark.add_synthetic("TVAE", pd.read_csv("synthetic_tvae.csv"))

# Run all metrics and rank generators
results = benchmark.rank_by(metric="utility_ratio")
for rank, (name, score) in enumerate(results.items(), 1):
    print(f"  #{rank}: {name} (utility_ratio={score:.4f})")
```

### 5. Privacy-Utility Tradeoff Visualization

```python
from quality_validation import PrivacyUtilityAnalyzer

analyzer = PrivacyUtilityAnalyzer()

# Evaluate synthetic data generated with different privacy budgets
epsilon_values = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
results = []

for eps in epsilon_values:
    synthetic = generate_with_epsilon(epsilon=eps)
    metrics = analyzer.evaluate(
        real_data=real_data,
        synthetic_data=synthetic,
        quasi_identifiers=["age", "zip_code", "gender"]
    )
    results.append({"epsilon": eps, **metrics})

# Plot the tradeoff curve
analyzer.plot_tradeoff(results, output_path="privacy_utility_curve.png")
```

### 6. Temporal Consistency Validation

```python
from quality_validation import TemporalValidator

# Validate that time-series patterns are preserved
temporal_validator = TemporalValidator()

# Compare autocorrelation functions
acf_results = temporal_validator.check_autocorrelation(
    real_ts=real_time_series,
    synthetic_ts=synthetic_time_series,
    max_lag=50
)

# Compare seasonal decomposition
seasonal_results = temporal_validator.check_seasonality(
    real_ts=real_time_series,
    synthetic_ts=synthetic_time_series,
    period=12
)

print(f"ACF Preservation Score: {acf_results['score']:.4f}")
print(f"Seasonal Pattern Similarity: {seasonal_results['score']:.4f}")
```

## Best Practices

1.  **Use a Held-Out Test Set**: Never evaluate synthetic data quality on the same data used to train the generative model. Always use a separate, real test set.
2.  **Look Beyond Averages**: A synthetic dataset might have the correct mean and variance for "age" but completely miss the bimodal distribution. Use distribution plots (histograms/KDE) alongside summary statistics.
3.  **Prioritize Task-Relevant Metrics**: If the goal is training a classifier, ML Utility is the most important metric. If the goal is data sharing for BI, distribution fidelity is key.
4.  **Monitor Correlation Matrices**: Ensuring that the correlation between "income" and "spending" is preserved is often more important than preserving the exact distribution of each individually.
5.  **Check for Overfitting**: If the Synthetic Data Detector AUC is very low (near 0.5), it's a good sign. If it's very high (near 1.0), the generator may be "memorizing" the real data, which is a privacy risk.
6.  **Iterate and Re-evaluate**: Data quality is an iterative process. After adjusting generation parameters (e.g., adding more epochs or changing the epsilon), always re-run the validation suite.
7. **Validate Before Release**: Never ship synthetic data without running the full validation suite. A single failed KS test on a critical column can invalidate the entire dataset.
8. **Automate in CI/CD**: Integrate validation into your data pipeline so that every generated dataset is automatically evaluated before being published to consumers.
9. **Track Metrics Over Time**: Store validation results in a time-series database to detect drift in generator quality as source data evolves.
10. **Domain-Specific Thresholds**: Generic thresholds (e.g., KS p > 0.05) may be too loose or too strict for specific domains. Work with domain experts to calibrate thresholds.

## Common Validation Pitfalls

| Pitfall | Impact | Mitigation |
|---------|--------|------------|
| Evaluating on training data | Inflated fidelity scores | Always use a held-out real test set |
| Ignoring correlation structure | High individual column fidelity but broken relationships | Always check correlation matrices |
| Relying only on ML utility | Good model performance but unrealistic distributions | Combine statistical and utility metrics |
| Not checking for mode collapse | Missing rare but important values | Check minimum row count per category |
| Over-trusting KS test | Failing on trivially different columns | Use multiple metrics in combination |

## Related Modules

*   [data-generation](../data-generation/GROK.md): The source of the synthetic data being evaluated.
*   [privacy-preservation](../privacy-preservation/GROK.md): Tools to improve privacy, which will impact the metrics in this module.
*   [augmentation](../augmentation/GROK.md): Techniques that produce augmented data to be validated.
*   [domain-specific](../domain-specific/GROK.md): Domain-specific validation rules (e.g., ensuring medical codes are valid).

---

## Advanced Configuration

The `quality-validation` module supports detailed configuration of every validation metric through YAML files or programmatic APIs.

### Configuration File Format

```yaml
# validation_config.yaml
validation:
  default_metrics:
    - "ks_test"
    - "wasserstein"
    - "correlation_preservation"
    - "ml_utility"

ks_test:
  significance_level: 0.05
  alternative: "two-sided"
  method: "auto"  # "auto", "exact", "approx"

wasserstein:
  normalize: true
  max_samples: 10000

correlation:
  methods: ["pearson", "spearman"]
  threshold: 0.1

ml_utility:
  model_type: "xgboost"
  test_size: 0.2
  cross_validation: 5
  metrics: ["auc", "accuracy", "f1"]

detector:
  model_type: "random_forest"
  n_estimators: 100
  threshold: 0.5

report:
  format: "html"
  include_visualizations: true
  output_path: "./reports/"
```

### Programmatic Configuration

```python
from quality_validation import ValidationConfig, ValidationSuite

config = ValidationConfig(
    metrics=["ks_test", "wasserstein", "correlation_preservation", "ml_utility"],
    ks_significance=0.05,
    wasserstein_normalize=True,
    correlation_methods=["pearson", "spearman"],
    ml_model_type="xgboost",
    ml_cv_folds=5,
    report_format="html",
    output_path="./reports/"
)

suite = ValidationSuite(config=config)
```

### Environment-Specific Overrides

```bash
# Override validation settings via environment
export VALIDATION_METRICS="ks_test,wasserstein,ml_utility"
export VALIDATION_KS_SIGNIFICANCE=0.01
export VALIDATION_ML_MODEL="random_forest"
export VALIDATION_REPORT_FORMAT="pdf"
export VALIDATION_OUTPUT_PATH="/var/reports/"
```

### Dynamic Configuration Updates

```python
from quality_validation import DynamicConfigManager

config_manager = DynamicConfigManager(config_path="validation_config.yaml")

# Register callbacks for configuration changes
@config_manager.on_change("ml_utility.model_type")
def update_model(new_value):
    print(f"ML model updated to {new_value}")
    suite.update_config(ml_model_type=new_value)

# Hot-reload configuration
config_manager.reload()
```

---

## Architecture Patterns

### Strategy Pattern for Metrics

The module uses a strategy pattern where each metric is implemented as a separate strategy class.

```python
from quality_validation import MetricStrategy, ValidationSuite

class CustomMetricStrategy(MetricStrategy):
    def __init__(self, config):
        self.config = config

    def compute(self, real_data, synthetic_data):
        # Custom metric computation
        return {"score": 0.85, "details": {}}

# Register custom metric
ValidationSuite.register_metric("custom_metric", CustomMetricStrategy)

# Use in validation
suite = ValidationSuite(
    real_data=real_data,
    synthetic_data=synthetic_data,
    metrics=["ks_test", "custom_metric"]
)
```

### Composite Pattern for Reports

```python
from quality_validation import ReportComposite, ReportSection

# Build a composite report
report = ReportComposite()
report.add(ReportSection("Statistical Fidelity", ks_results))
report.add(ReportSection("Correlation Preservation", corr_results))
report.add(ReportSection("ML Utility", ml_results))

# Generate output
report.generate(format="html", output_path="validation_report.html")
```

### Observer Pattern for Progress

```python
from quality_validation import ValidationSuite, ValidationObserver

class ValidationProgressMonitor(ValidationObserver):
    def on_metric_start(self, metric_name):
        print(f"Starting {metric_name}...")

    def on_metric_complete(self, metric_name, result):
        print(f"Completed {metric_name}: {result['score']:.4f}")

    def on_validation_complete(self, report):
        print(f"Validation complete: {report['overall_score']:.4f}")

suite = ValidationSuite(
    real_data=real_data,
    synthetic_data=synthetic_data
)
suite.add_observer(ValidationProgressMonitor())
suite.run()
```

### Plugin Architecture

```python
from quality_validation import PluginRegistry

@PluginRegistry.register("custom_validator")
class CustomValidator:
    def __init__(self, config):
        self.config = config

    def validate(self, real_data, synthetic_data):
        # Custom validation logic
        return {"passed": True, "score": 0.9, "details": {}}
```

---

## Integration Guide

### Integration with Data Generation

```python
from data_generation import TabularGenerator
from quality_validation import ValidationSuite

# Generate synthetic data
generator = TabularGenerator(model_type="ctgan")
generator.fit(real_data)
synthetic_data = generator.generate(n_samples=10000)

# Validate immediately
suite = ValidationSuite(
    real_data=real_data,
    synthetic_data=synthetic_data
)
report = suite.generate_report()

# Check if quality is acceptable
if report["overall_score"] < 0.8:
    print("Quality below threshold, retraining...")
    generator.fit(real_data, epochs=500)
```

### Integration with Privacy Preservation

```python
from privacy_preservation import Anonymizer
from quality_validation import PrivacyUtilityAnalyzer

# Anonymize data
anonymizer = Anonymizer(method="k-anonymity", k=5)
anonymized = anonymizer.fit_transform(raw_data)

# Analyze privacy-utility tradeoff
analyzer = PrivacyUtilityAnalyzer()
metrics = analyzer.evaluate(
    real_data=raw_data,
    synthetic_data=anonymized,
    quasi_identifiers=["age", "zip"]
)

print(f"Utility retention: {metrics['utility_ratio']:.2%}")
print(f"Privacy risk: {metrics['reidentification_risk']:.2%}")
```

### Integration with ML Pipelines

```python
from sklearn.pipeline import Pipeline
from quality_validation import ValidationCallback

# Add validation as a pipeline step
validation_callback = ValidationCallback(
    real_data=real_data,
    metrics=["ml_utility"],
    threshold=0.85
)

pipeline = Pipeline([
    ("generate", TabularGenerator(model_type="ctgan")),
    ("validate", validation_callback),
    ("train", RandomForestClassifier())
])

# Validation runs automatically after generation
pipeline.fit(X_train, y_train)
```

### Integration with CI/CD

```yaml
# .github/workflows/validate.yml
name: Validate Synthetic Data
on:
  push:
    paths:
      - 'synthetic_data/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Validation
        run: |
          python -m quality_validation.cli \
            --real-data data/real.csv \
            --synthetic-data data/synthetic.csv \
            --config validation_config.yaml \
            --output reports/validation.json
      - name: Check Quality Threshold
        run: |
          python -c "
          import json
          report = json.load(open('reports/validation.json'))
          assert report['overall_score'] >= 0.8, 'Quality below threshold'
          "
```

---

## Performance Optimization

### Parallel Metric Computation

```python
from quality_validation import ParallelValidator

# Compute metrics in parallel
parallel_validator = ParallelValidator(
    n_workers=8,
    metrics=["ks_test", "wasserstein", "correlation_preservation"]
)

results = parallel_validator.validate(
    real_data=real_data,
    synthetic_data=synthetic_data
)
```

### Sampling Strategies

```python
from quality_validation import SamplingValidator

# Use sampling for large datasets
sampling_validator = SamplingValidator(
    max_samples=10000,
    sampling_method="stratified",
    random_seed=42
)

results = sampling_validator.validate(
    real_data=large_real_data,
    synthetic_data=large_synthetic_data
)
```

### Caching Results

```python
from quality_validation import CacheConfig, ValidationSuite

cache_config = CacheConfig(
    enabled=True,
    cache_dir="/tmp/validation_cache",
    max_size_gb=5,
    ttl_hours=24
)

suite = ValidationSuite(
    real_data=real_data,
    synthetic_data=synthetic_data,
    cache_config=cache_config
)

# Repeated validations use cached results
report = suite.generate_report()  # Computes and caches
report = suite.generate_report()  # Uses cache
```

### GPU Acceleration

```python
from quality_validation import GPUValidator

gpu_validator = GPUValidator(
    device="cuda:0",
    metrics=["ks_test", "wasserstein"]
)

results = gpu_validator.validate(
    real_data=real_data,
    synthetic_data=synthetic_data
)
```

---

## Security Considerations

### Data Integrity

```python
from quality_validation import IntegrityVerifier

verifier = IntegrityVerifier(
    algorithm="sha256",
    store_path="/var/lib/validation_hashes"
)

# Store hash before validation
original_hash = verifier.store_hash(real_data, identifier="real_data_v1")

# Verify integrity after validation
is_valid = verifier.verify_hash(
    real_data,
    identifier="real_data_v1",
    original_hash=original_hash
)
```

### Access Control

```python
from quality_validation import AccessControl

acl = AccessControl()
acl.add_policy(
    resource="validation_reports",
    allowed_roles=["data_scientist", "analyst"],
    conditions={
        "max_reports_per_day": 10,
        "require_approval": False
    }
)

# Check access before validation
if acl.authorize(user="data_scientist_1", resource="validation_reports"):
    report = suite.generate_report()
```

### Audit Logging

```python
from quality_validation import AuditLogger

audit_logger = AuditLogger(
    log_path="/var/log/validation_audit/",
    log_format="json",
    capture_inputs_hash=True,
    retention_days=365
)

suite = ValidationSuite(
    real_data=real_data,
    synthetic_data=synthetic_data,
    audit_logger=audit_logger
)
```

### Secure Report Storage

```python
from quality_validation import SecureReportStorage

storage = SecureReportStorage(
    encryption_key="path/to/key.pem",
    storage_path="/var/lib/reports/"
)

# Store report securely
storage.store(report, identifier="validation_2024_01")

# Retrieve with integrity check
report = storage.retrieve("validation_2024_01")
```

---

## Troubleshooting Guide

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `KS test failed` | Distributions significantly different | Check generation parameters, increase epochs |
| `Correlation preserved poorly` | Relationships between variables lost | Use metadata-aware generation |
| `ML utility low` | Synthetic data not useful for training | Try different generation model, increase data quality |
| `Memory exhausted` | Dataset too large for validation | Use sampling or parallel validation |
| `Report generation failed` | Invalid configuration | Check report format and output path |

### Debug Mode

```python
from quality_validation import ValidationSuite, DebugConfig

debug_config = DebugConfig(
    verbose=True,
    log_level="DEBUG",
    save_intermediate=True,
    intermediate_path="/tmp/debug/",
    profile_operations=True
)

suite = ValidationSuite(
    real_data=real_data,
    synthetic_data=synthetic_data,
    debug_config=debug_config
)
```

### Validation Diagnostics

```python
from quality_validation import DiagnosticTools

# Run diagnostic checks
diagnostics = DiagnosticTools.run(
    real_data=real_data,
    synthetic_data=synthetic_data,
    checks=["data_quality", "metric_consistency", "report_integrity"]
)

for check in diagnostics:
    if not check.passed:
        print(f"FAILED: {check.name} - {check.message}")
        print(f"  Recommendation: {check.suggestion}")
```

### Performance Profiling

```python
from quality_validation import Profiler

profiler = Profiler()

with profiler:
    report = suite.generate_report()

profiler.print_report()
# Output includes:
# - Per-metric timing
# - Memory usage
# - Throughput statistics
```

---

## API Reference

### ValidationSuite

```python
class ValidationSuite:
    """Run a comprehensive validation suite on synthetic data."""

    def __init__(
        self,
        real_data: pd.DataFrame,
        synthetic_data: pd.DataFrame,
        metrics: list[str] = None,
        config: ValidationConfig = None,
        metadata: dict = None
    ):
        """Initialize the validation suite.

        Args:
            real_data: Real dataset
            synthetic_data: Synthetic dataset
            metrics: List of metrics to compute
            config: ValidationConfig object
            metadata: Optional metadata
        """
        pass

    def run(self) -> dict:
        """Run all configured metrics.

        Returns:
            Dict with metric results
        """
        pass

    def generate_report(
        self,
        output_format: str = "html",
        output_path: str = None
    ) -> str:
        """Generate a validation report.

        Args:
            output_format: "html", "pdf", "json"
            output_path: Optional output path

        Returns:
            Path to generated report
        """
        pass

    def get_metric(self, metric_name: str) -> dict:
        """Get result for a specific metric.

        Args:
            metric_name: Name of the metric

        Returns:
            Metric result dict
        """
        pass
```

### FidelityEvaluator

```python
class FidelityEvaluator:
    """Evaluate distributional fidelity of synthetic data."""

    def __init__(
        self,
        metrics: list[str] = None,
        significance_level: float = 0.05
    ):
        """Initialize fidelity evaluator.

        Args:
            metrics: List of fidelity metrics
            significance_level: Significance level for statistical tests
        """
        pass

    def ks_test(
        self,
        real_data: pd.DataFrame,
        synthetic_data: pd.DataFrame
    ) -> dict:
        """Run Kolmogorov-Smirnov tests.

        Args:
            real_data: Real dataset
            synthetic_data: Synthetic dataset

        Returns:
            Dict mapping column names to p-values
        """
        pass

    def wasserstein_distance(
        self,
        real_data: pd.DataFrame,
        synthetic_data: pd.DataFrame
    ) -> dict:
        """Compute Wasserstein distances.

        Args:
            real_data: Real dataset
            synthetic_data: Synthetic dataset

        Returns:
            Dict mapping column names to distances
        """
        pass
```

### UtilityEvaluator

```python
class UtilityEvaluator:
    """Evaluate ML utility of synthetic data."""

    def __init__(
        self,
        target: str,
        model_type: str = "xgboost",
        test_size: float = 0.2,
        cv_folds: int = 5
    ):
        """Initialize utility evaluator.

        Args:
            target: Target column name
            model_type: ML model type
            test_size: Test set proportion
            cv_folds: Cross-validation folds
        """
        pass

    def compare(
        self,
        real_train: pd.DataFrame,
        synthetic_train: pd.DataFrame,
        real_test: pd.DataFrame
    ) -> dict:
        """Compare model performance on real vs synthetic data.

        Args:
            real_train: Real training data
            synthetic_train: Synthetic training data
            real_test: Real test data

        Returns:
            Dict with comparison metrics
        """
        pass
```

---

## Data Models

### ValidationConfig Schema

```python
@dataclass
class ValidationConfig:
    """Configuration for validation suite."""

    metrics: list[str] = field(default_factory=lambda: [
        "ks_test", "wasserstein", "correlation_preservation", "ml_utility"
    ])
    ks_significance: float = 0.05
    wasserstein_normalize: bool = True
    correlation_methods: list[str] = field(default_factory=lambda: ["pearson", "spearman"])
    correlation_threshold: float = 0.1
    ml_model_type: str = "xgboost"
    ml_cv_folds: int = 5
    ml_test_size: float = 0.2
    report_format: str = "html"
    output_path: str = "./reports/"
    random_seed: int = None
```

### ValidationReport Schema

```python
@dataclass
class ValidationReport:
    """Comprehensive validation report."""

    report_id: str
    timestamp: datetime
    real_data_hash: str
    synthetic_data_hash: str
    overall_score: float
    metrics: dict[str, dict]
    recommendations: list[str]
    metadata: dict
```

### MetricResult Schema

```python
@dataclass
class MetricResult:
    """Result of a single metric computation."""

    metric_name: str
    score: float
    details: dict
    passed: bool
    threshold: float
    computation_time: float
```

---

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY config/ /app/config/

WORKDIR /app

EXPOSE 8083

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s \
    CMD curl -f http://localhost:8083/health || exit 1

CMD ["python", "-m", "quality_validation.server", "--port", "8083"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: validation-service
  namespace: synthetic-data
spec:
  replicas: 2
  selector:
    matchLabels:
      app: validation
  template:
    metadata:
      labels:
        app: validation
    spec:
      containers:
      - name: validator
        image: synthetic-data/validation:latest
        ports:
        - containerPort: 8083
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        env:
        - name: VALIDATION_OUTPUT_PATH
          value: "/var/reports/"
```

### REST API Server

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from quality_validation import ValidationSuite

app = FastAPI(title="Validation API")

class ValidateRequest(BaseModel):
    real_data: list[dict]
    synthetic_data: list[dict]
    metrics: list[str] = ["ks_test", "wasserstein"]

@app.post("/validate")
async def validate_data(request: ValidateRequest):
    try:
        import pandas as pd
        real_df = pd.DataFrame(request.real_data)
        synth_df = pd.DataFrame(request.synthetic_data)

        suite = ValidationSuite(
            real_data=real_df,
            synthetic_data=synth_df,
            metrics=request.metrics
        )

        report = suite.generate_report(output_format="json")
        return {"report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

---

## Monitoring & Observability

### Metrics Collection

```python
from quality_validation import MetricsCollector

metrics = MetricsCollector(
    backend="prometheus",
    port=9093,
    metrics=[
        "validation_duration_seconds",
        "validations_completed_total",
        "overall_score",
        "metric_computation_time"
    ]
)

suite = ValidationSuite(
    real_data=real_data,
    synthetic_data=synthetic_data,
    metrics_collector=metrics
)
```

### Audit Logging

```python
from quality_validation import AuditLogger

audit_logger = AuditLogger(
    log_path="/var/log/validation_audit/",
    log_format="json",
    capture_inputs_hash=True,
    retention_days=365
)

suite = ValidationSuite(
    real_data=real_data,
    synthetic_data=synthetic_data,
    audit_logger=audit_logger
)
```

### Alerting Rules

```python
from quality_validation import AlertManager

alert_manager = AlertManager(
    rules=[
        {"metric": "overall_score", "threshold": 0.8, "severity": "warning", "operator": "lt"},
        {"metric": "validation_duration_seconds", "threshold": 300, "severity": "warning"},
        {"metric": "validations_completed_total", "threshold": 0, "severity": "critical"}
    ],
    notification_channels=["slack", "email"]
)
```

### Dashboard Integration

```python
from quality_validation import DashboardExporter

exporter = DashboardExporter(
    format="grafana",
    output_path="/var/lib/grafana/dashboards/validation.json"
)

exporter.generate_dashboard(
    metrics=["validation_throughput", "quality_scores", "metric_trends"],
    time_range="7d"
)
```

---

## Testing Strategy

### Unit Tests

```python
import pytest
import pandas as pd
import numpy as np
from quality_validation import FidelityEvaluator, UtilityEvaluator

@pytest.fixture
def sample_data():
    np.random.seed(42)
    real = pd.DataFrame({
        "age": np.random.randint(18, 80, 1000),
        "income": np.random.lognormal(10, 1, 1000),
        "target": np.random.choice([0, 1], 1000)
    })
    synthetic = pd.DataFrame({
        "age": np.random.randint(18, 80, 1000),
        "income": np.random.lognormal(10, 1, 1000),
        "target": np.random.choice([0, 1], 1000)
    })
    return real, synthetic

class TestFidelityEvaluator:
    def test_ks_test_returns_pvalues(self, sample_data):
        real, synthetic = sample_data
        evaluator = FidelityEvaluator()
        results = evaluator.ks_test(real, synthetic)
        assert "age" in results
        assert 0 <= results["age"] <= 1

    def test_wasserstein_returns_distances(self, sample_data):
        real, synthetic = sample_data
        evaluator = FidelityEvaluator()
        results = evaluator.wasserstein_distance(real, synthetic)
        assert "income" in results
        assert results["income"] >= 0

class TestUtilityEvaluator:
    def test_compare_returns_metrics(self, sample_data):
        real, synthetic = sample_data
        evaluator = UtilityEvaluator(target="target")
        results = evaluator.compare(
            real_train=real,
            synthetic_train=synthetic,
            real_test=real
        )
        assert "real_auc" in results
        assert "synthetic_auc" in results
        assert "utility_ratio" in results
```

### Integration Tests

```python
class TestValidationSuite:
    def test_full_validation(self, sample_data):
        real, synthetic = sample_data
        suite = ValidationSuite(
            real_data=real,
            synthetic_data=synthetic
        )
        report = suite.generate_report()
        assert report["overall_score"] > 0
        assert len(report["metrics"]) > 0
```

---

## Versioning & Migration

### Semantic Versioning

- **MAJOR**: Breaking API changes, incompatible report formats
- **MINOR**: New metrics, backward-compatible
- **PATCH**: Bug fixes, performance improvements

### Report Format Migration

```python
from quality_validation import ReportMigrator

migrator = ReportMigrator(
    source_version="1.2.0",
    target_version="2.0.0"
)

migrator.migrate_report(
    source="old_report.json",
    target="new_report.json",
    schema_mappings={
        "old_metric_name": "new_metric_name"
    }
)
```

### Configuration Migration

```python
from quality_validation import ConfigMigrator

config_migrator = ConfigMigrator()
config_migrator.migrate(
    source="old_validation_config.yaml",
    target="new_validation_config.yaml"
)
```

---

## Glossary

| Term | Definition |
|------|------------|
| **KS Test** | Kolmogorov-Smirnov test - nonparametric test for distribution equality |
| **Wasserstein Distance** | "Earth mover's distance" - measures the work needed to transform one distribution into another |
| **Jensen-Shannon Divergence** | Symmetric measure of similarity between two probability distributions |
| **Correlation Preservation** | Maintaining the statistical relationships between variables in synthetic data |
| **ML Utility** | How well machine learning models trained on synthetic data perform on real data |
| **Synthetic Data Detector** | A classifier that attempts to distinguish real from synthetic records |
| **Fidelity** | How closely synthetic data matches the statistical properties of real data |
| **Utility Ratio** | Ratio of model performance on synthetic data vs real data |
| **Population Stability Index** | Measures distribution shift between two datasets |
| **Shadow Model** | A model trained to detect whether data is real or synthetic |

---

## Changelog

### v1.0.0 (2024-01-15)
- Initial release with KS test, Wasserstein distance, correlation preservation
- ML utility evaluation with XGBoost
- Synthetic data detection
- HTML report generation

### v1.1.0 (2024-03-01)
- Added Jensen-Shannon divergence
- Temporal consistency validation for time series
- Benchmarking framework for multiple generators
- PDF report generation

### v1.2.0 (2024-05-15)
- Privacy-utility tradeoff analysis
- Edge case coverage metrics
- Drift detection with PSI
- REST API for validation-as-a-service

### v1.3.0 (2024-08-01)
- Kubernetes deployment templates
- Dashboard integration
- Enhanced audit logging
- Parallel metric computation

---

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/quality-validation.git
cd quality-validation
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/
ruff check src/
ruff format src/
```

### Code Style

- Follow PEP 8 for Python code
- Use type hints for all public functions
- Write docstrings for all public classes and methods
- Keep functions under 50 lines
- Use meaningful variable names

### Pull Request Process

1. Create a feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation if needed
5. Submit PR with clear description of changes

### Commit Message Format

```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

---

## License

Copyright (c) 2024 Synthetic Data Toolkit Contributors

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
