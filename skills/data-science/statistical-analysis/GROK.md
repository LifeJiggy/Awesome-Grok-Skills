---
name: "Statistical Analysis"
version: "2.0.0"
description: "Comprehensive statistical analysis toolkit with hypothesis testing, regression modeling, non-parametric methods, Bayesian statistics, and effect size estimation for rigorous empirical research"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["data-science", "statistics", "hypothesis-testing", "regression", "bayesian", "non-parametric"]
category: "data-science"
personality: "statistician"
use_cases: ["hypothesis testing", "regression analysis", "A/B testing", "survival analysis", "meta-analysis"]
---

# Statistical Analysis

> Rigorous statistical toolkit providing frequentist and Bayesian hypothesis testing, generalized linear models, non-parametric methods, survival analysis, and effect size computation for reproducible empirical research.

## Overview

The Statistical Analysis module provides a complete statistical toolkit for data scientists and researchers who need rigorous, reproducible statistical methods. It covers the full spectrum from descriptive statistics through advanced inference, including parametric and non-parametric tests, multiple regression techniques (linear, logistic, Poisson, Cox proportional hazards), Bayesian estimation, bootstrap resampling, and comprehensive effect size reporting. Every test returns structured results with test statistics, p-values, confidence intervals, power analysis, and practical recommendations.

## Core Capabilities

### 1. Hypothesis Testing Framework
- Parametric tests: t-tests (one-sample, two-sample, paired), F-test, ANOVA (one-way, two-way, repeated measures)
- Non-parametric tests: Mann-Whitney U, Wilcoxon signed-rank, Kruskal-Wallis, Friedman, permutation tests
- Multiple comparison correction: Bonferroni, Holm, Benjamini-Hochberg FDR, Tukey HSD
- Power analysis: a priori, post hoc, sensitivity, and sample size calculations
- Effect size computation: Cohen's d, Hedges' g, eta-squared, omega-squared, Glass's delta

### 2. Regression Modeling
- Linear regression with OLS, Ridge, Lasso, and Elastic Net regularization
- Generalized Linear Models: logistic, Poisson, gamma, inverse Gaussian
- Ordinal and multinomial regression
- Quantile regression for distributional analysis
- Robust regression (M-estimation, Theil-Sen) for outlier resilience

### 3. Bayesian Statistics
- Bayesian estimation with conjugate and MCMC methods
- Bayesian hypothesis testing via Bayes factors
- Bayesian credible intervals and posterior summaries
- Prior sensitivity analysis
- Bayesian model averaging

### 4. Survival Analysis
- Kaplan-Meier survival estimation
- Cox proportional hazards regression
- Log-rank and Wilcoxon tests for group comparisons
- Hazard ratio estimation with confidence intervals
- Cox-Snell and Martingale residuals for model diagnostics

### 5. Resampling and Robust Methods
- Bootstrap confidence intervals (percentile, BCa, studentized)
- Permutation tests for arbitrary test statistics
- jackknife bias estimation
- Cross-validated regression coefficients
- Wild bootstrap for heteroscedastic data

## Usage Examples

### Hypothesis Testing with Effect Sizes

```python
from statistical_analysis import HypothesisTesting, EffectSize

ht = HypothesisTesting()

# Two-sample t-test with comprehensive output
result = ht.t_test_ind(
    group1=treatment_outcomes,
    group2=control_outcomes,
    alternative="two-sided",
    equal_var=False,  # Welch's t-test
    effect_size=EffectSize.COHENS_D,
    power_analysis=True
)

print(f"t-statistic: {result.statistic:.4f}")
print(f"p-value:     {result.p_value:.6f}")
print(f"Cohen's d:   {result.effect_size:.4f} ({result.effect_size_interpretation})")
print(f"95% CI:      [{result.ci_lower:.4f}, {result.ci_upper:.4f}]")
print(f"Power:       {result.power:.4f}")
print(f"Decision:    {result.significant(alpha=0.05)}")

# Multiple comparison correction
results_batch = ht.batch_test([group_a, group_b, group_c], control)
corrected = ht.multiple_comparison_correction(results_batch, method="benjamini_hochberg")
for r in corrected:
    print(f"  {r.name}: p={r.adjusted_p:.4f} {'*' if r.significant else ''}")
```

### Generalized Linear Model

```python
from statistical_analysis import GLM, Family, Link

glm = GLM(family=Family.POISSON(link=Link.LOG))

# Fit Poisson regression for count data
model = glm.fit(
    y=count_outcome,
    X=feature_matrix,
    feature_names=["age", "income", "treatment", "baseline_count"],
    offset=np.log(exposure_time),
    dispersion="pearson"
)

print(f"Coefficients:")
for name, coef, se, z, p in model.summary():
    stars = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
    print(f"  {name:20s}  coef={coef:+.4f}  se={se:.4f}  z={z:.3f}  p={p:.4f} {stars}")

print(f"Deviance: {model.deviance:.2f} (df={model.residual_df})")
print(f"AIC: {model.aic:.2f}, BIC: {model.bic:.2f}")
print(f"Pearson chi-sq / df: {model.dispersion_estimate:.3f}")
```

### Bootstrap Confidence Intervals

```python
from statistical_analysis import Bootstrap, ConfidenceLevel

boot = Bootstrap(n_resamples=10000, seed=42)

# BCa confidence interval for median
result = boot.confidence_interval(
    data=outcomes,
    statistic=np.median,
    level=ConfidenceLevel.BCA,
    alpha=0.05
)

print(f"Point estimate:  {result.point_estimate:.4f}")
print(f"BCa 95% CI:      [{result.ci_lower:.4f}, {result.ci_upper:.4f}]")
print(f"Bootstrap SE:    {result.std_error:.4f}")
print(f"Bias:            {result.bias:.4f}")
print(f"Acceleration:    {result.acceleration:.6f}")

# Bootstrap hypothesis test
test_result = boot.permutation_test(
    group1=treatment,
    group2=control,
    statistic=lambda g1, g2: np.mean(g1) - np.mean(g2),
    n_permutations=5000
)
print(f"Permutation p-value: {test_result.p_value:.4f}")
```

### Survival Analysis

```python
from statistical_analysis import SurvivalAnalysis

sa = SurvivalAnalysis()

# Kaplan-Meier estimation
km_result = sa.kaplan_meier(
    times=survival_times,
    events=event_indicator,
    groups=treatment_arm
)

print("Kaplan-Meier Estimates:")
for group, stats in km_result.group_summary().items():
    print(f"  {group}: median={stats.median_survival:.1f}, "
          f"surv_1yr={stats.survival_at(12):.3f}")

# Log-rank test
lr = sa.log_rank_test(km_result, group_a="treatment", group_b="control")
print(f"Log-rank chi-sq: {lr.chi_square:.3f}, p={lr.p_value:.4f}")

# Cox proportional hazards
cox = sa.cox_ph(
    times=survival_times,
    events=event_indicator,
    covariates=demographic_matrix,
    covariate_names=["age", "stage", "treatment"]
)
print(f"Hazard ratios:")
for name, hr, ci_lo, ci_hi, p in cox.summary():
    print(f"  {name}: HR={hr:.3f} [{ci_lo:.3f}, {ci_hi:.3f}] p={p:.4f}")
```

## Best Practices

### Hypothesis Testing
- Always check assumptions (normality, homoscedasticity, independence) before parametric tests
- Report effect sizes alongside p-values — p < 0.05 with d = 0.1 is practically meaningless
- Use Bonferroni or FDR correction when running more than 2-3 tests simultaneously
- Design studies with power >= 0.80; report achieved power post hoc

### Regression Analysis
- Examine residual plots (QQ, scale-location, leverage) before interpreting coefficients
- Use robust standard errors (HC3) when heteroscedasticity is detected
- Check VIF > 5 for multicollinearity; consider removing or combining correlated predictors
- Prefer AIC/BIC over p-values for model selection among nested and non-nested models

### Bayesian Analysis
- Conduct prior sensitivity analysis — vary priors and check if conclusions change
- Use weakly informative priors when domain knowledge is limited
- Report posterior distributions, not just point estimates
- Check R-hat < 1.05 and ESS > 400 for MCMC convergence

### Survival Analysis
- Check proportional hazards assumption via Schoenfeld residuals
- Use time-varying coefficients when PH assumption is violated
- Report median survival and restricted mean survival time (RMST) alongside hazard ratios
- Account for competing risks when applicable

## Related Modules

- **advanced-analytics**: Bayesian inference, Monte Carlo, causal inference, and multivariate methods
- **feature-engineering**: Data transformation for statistical modeling inputs
- **data-visualization**: Statistical graphics including regression diagnostics and survival curves
- **time-series**: Temporal data analysis with autocorrelation and state-space models