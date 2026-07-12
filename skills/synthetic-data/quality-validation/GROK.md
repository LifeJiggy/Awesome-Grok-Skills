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
