# Data Science Agent

## Overview

The **Data Science Agent** provides comprehensive statistical analysis and data exploration capabilities. This agent enables exploratory data analysis, statistical testing, regression modeling, and advanced analytics for data-driven decision making.

## Core Capabilities

### 1. Data Profiling
Understand your dataset:
- **Structure Analysis**: Rows, columns, data types
- **Quality Assessment**: Missing values, duplicates
- **Distribution Analysis**: Statistical summaries
- **Data Validation**: Type checking, constraints

### 2. Descriptive Statistics
Calculate comprehensive statistics:
- **Central Tendency**: Mean, median, mode
- **Dispersion**: Variance, std deviation, range
- **Shape**: Skewness, kurtosis
- **Percentiles**: Quartiles, custom percentiles

### 3. Hypothesis Testing
Validate hypotheses statistically:
- **T-Tests**: Compare means
- **Chi-Square**: Test independence
- **ANOVA**: Compare multiple groups
- **Non-Parametric Tests**: Distribution-free tests

### 4. Correlation Analysis
Understand variable relationships:
- **Pearson Correlation**: Linear relationships
- **Spearman Correlation**: Rank correlations
- **Correlation Matrix**: Multi-variable analysis
- **Visualization Support**: Heatmaps, scatter plots

### 5. Regression Analysis
Model relationships:
- **Linear Regression**: Simple linear models
- **Multiple Regression**: Multi-predictor models
- **Residual Analysis**: Model diagnostics
- **Model Metrics**: R-squared, RMSE, MAE

### 6. Time Series Analysis
Analyze temporal patterns:
- **Trend Analysis**: Identify trends
- **Seasonality Detection**: Periodic patterns
- **Decomposition**: Trend, seasonal, residual
- **Forecasting**: Predict future values

### 7. Cluster Analysis
Discover natural groupings:
- **K-Means Clustering**: Partition-based clustering
- **Hierarchical Clustering**: Dendrogram building
- **Cluster Validation**: Silhouette scores
- **Cluster Profiling**: Characterize clusters

### 8. Feature Engineering
Create predictive features:
- **Feature Creation**: Polynomial, interaction terms
- **Feature Transformation**: Log, scaling, binning
- **Feature Selection**: Importance ranking
- **Dimensionality Reduction**: PCA, t-SNE

## Usage Examples

### Basic Statistics

```python
from data_science import DataScienceAnalyzer

ds = DataScienceAnalyzer()
stats = ds.descriptive_statistics([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(f"Mean: {stats['mean']}")
print(f"Std Dev: {stats['std_dev']}")
print(f"Percentiles: {stats['percentiles']}")
```

### Hypothesis Testing

```python
result = ds.hypothesis_testing(
    StatisticalTest.T_TEST,
    data1=[1, 2, 3, 4, 5],
    data2=[6, 7, 8, 9, 10]
)
print(f"P-value: {result['p_value']}")
print(f"Significant: {result['significant']}")
```

### Regression Analysis

```python
x = [1, 2, 3, 4, 5]
y = [2, 4, 5, 4, 5]
regression = ds.regression_analysis(x, y)
print(f"R-squared: {regression['r_squared']:.4f}")
print(f"Equation: {regression['equation']}")
```

### Clustering

```python
data = [[1, 2], [3, 4], [5, 6], [1.5, 2.5], [3.5, 4.5]]
clusters = ds.cluster_analysis(data, n_clusters=2)
print(f"Clusters: {len(clusters['clusters'])}")
print(f"Silhouette: {clusters['silhouette_score']:.4f}")
```

## Statistical Methods

### Descriptive Statistics

| Metric | Description | Use Case |
|--------|-------------|----------|
| Mean | Average value | Central tendency |
| Median | Middle value | Robust to outliers |
| Mode | Most frequent | Categorical data |
| Std Dev | Spread of data | Variability |
| IQR | Middle 50% | Robust spread |

### Hypothesis Tests

| Test | Purpose | Assumptions |
|------|---------|-------------|
| T-Test | Compare two means | Normal distribution |
| ANOVA | Compare 3+ means | Normal, equal variance |
| Chi-Square | Test independence | Categorical data |
| Mann-Whitney | Non-parametric comparison | Non-normal data |

### Correlation Measures

| Measure | Range | Interpretation |
|---------|-------|----------------|
| Pearson | -1 to 1 | Linear relationship |
| Spearman | -1 to 1 | Monotonic relationship |
| Kendall | -1 to 1 | Ordinal association |

## Data Science Workflow

```
┌─────────────────────────────────────────────────────────┐
│              Data Science Pipeline                       │
├─────────────────────────────────────────────────────────┤
│  1. Problem Definition → 2. Data Collection             │
│         │                          │                    │
│  6. Deployment ← 5. Evaluation ← 4. Modeling            │
│         │                          │                    │
│  7. Monitoring ←─── 3. EDA & Preprocessing              │
└─────────────────────────────────────────────────────────┘
```

## Machine Learning Integration

### Supervised Learning
- **Regression**: Continuous target variables
- **Classification**: Categorical targets
- **Evaluation**: Accuracy, precision, recall, F1

### Unsupervised Learning
- **Clustering**: Group similar data points
- **Dimensionality Reduction**: Feature compression
- **Anomaly Detection**: Outlier identification

### Model Evaluation
- **Cross-Validation**: Robust performance estimates
- **Hyperparameter Tuning**: Optimize model performance
- **Model Selection**: Choose best algorithm

## Tools and Libraries

### Python Libraries
- **NumPy**: Numerical computing
- **Pandas**: Data manipulation
- **SciPy**: Statistical functions
- **Scikit-learn**: Machine learning
- **Statsmodels**: Statistical modeling

### Visualization
- **Matplotlib**: Basic plotting
- **Seaborn**: Statistical graphics
- **Plotly**: Interactive visualizations
- **Bokeh**: Web-based plots

## Use Cases

### 1. Business Analytics
- Customer segmentation
- Sales forecasting
- Churn prediction
- A/B testing analysis

### 2. Scientific Research
- Experimental data analysis
- Hypothesis testing
- Publication-quality figures
- Reproducible research

### 3. Financial Analysis
- Risk assessment
- Portfolio optimization
- Fraud detection
- Market analysis

### 4. Healthcare
- Clinical trial analysis
- Patient outcomes
- Epidemiological studies
- Medical imaging

## Best Practices

1. **Understand the Problem**: Define objectives clearly
2. **Explore Data**: Visualize distributions first
3. **Preprocess Properly**: Handle missing values
4. **Validate Results**: Use cross-validation
5. **Communicate Findings**: Clear visualizations
6. **Document Everything**: Reproducible workflows

## Related Skills

- [Machine Learning Operations](../ml-ops/model-deployment/README.md) - ML deployment
- [Analytics](../analytics/data-analysis/README.md) - Data analysis
- [Data Engineering](../data-engineering/data-pipelines/README.md) - Data pipelines

---

**File Path**: `skills/data-science/statistical-analysis/resources/data_science.py`
