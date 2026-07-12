---
name: "Time Series Analysis"
version: "2.0.0"
description: "Comprehensive time series analysis framework with decomposition, forecasting, anomaly detection, change point detection, spectral analysis, and state-space models for temporal data science"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["data-science", "time-series", "forecasting", "decomposition", "anomaly-detection", "state-space"]
category: "data-science"
personality: "time-series-analyst"
use_cases: ["forecasting", "trend analysis", "anomaly detection", "seasonality decomposition", "change point detection"]
---

# Time Series Analysis

> Production-grade time series framework providing decomposition, forecasting, anomaly detection, change point detection, spectral analysis, and state-space modeling for rigorous temporal data analysis.

## Overview

The Time Series Analysis module provides a complete toolkit for analyzing and forecasting temporal data. It implements classical decomposition (additive, multiplicative, STL), ARIMA/SARIMA family models, exponential smoothing (Holt-Winters), state-space models (Kalman filter, structural time series), change point detection (CUSUM, Bayesian, PELT), spectral analysis (FFT, periodogram, wavelets), and anomaly detection (Isolation Forest, seasonal ESD). Every analysis returns structured results with confidence intervals, diagnostics, and model comparison metrics.

## Core Capabilities

### 1. Time Series Decomposition
- Classical additive and multiplicative decomposition
- STL (Seasonal and Trend decomposition using Loess)
- MSTL for multiple seasonal patterns
- Trend extraction via HP filter, Baxter-King, and Butterworth
- Seasonal strength and trend strength metrics

### 2. Forecasting Models
- ARIMA with automatic order selection (auto-ARIMA)
- SARIMA for seasonal time series
- Exponential Smoothing (Simple, Holt, Holt-Winters)
- ETS (Error, Trend, Seasonality) state-space models
- Prophet-style decomposition (trend + seasonality + holidays)
- Model comparison via AIC, BIC, RMSE, MAE, MAPE

### 3. Anomaly Detection
- Statistical: Z-score, Modified Z-score, Grubbs' test
- Seasonal: Seasonal ESD (S-ESD), Twitter anomaly detection
- Model-based: ARIMA residuals, Kalman filter innovations
- Isolation Forest for multivariate time series
- Threshold-based with adaptive bounds

### 4. Change Point Detection
- CUSUM (Cumulative Sum Control)
- Bayesian Online Change Point Detection
- PELT (Pruned Exact Linear Time)
- Binary Segmentation
- Sliding window tests (Mann-Whitney, Kolmogorov-Smirnov)

### 5. Spectral and Frequency Analysis
- Fast Fourier Transform (FFT)
- Power spectral density estimation
- Periodogram and smoothed periodogram
- Wavelet transform (continuous and discrete)
- Autocorrelation (ACF) and Partial Autocorrelation (PACF)

### 6. State-Space Models
- Kalman filter for linear Gaussian systems
- Structural time series (local level, local trend, seasonal)
- Unobserved components model
- Particle filter for non-linear systems
- State smoothing and parameter estimation

## Usage Examples

### Time Series Decomposition

```python
from time_series import TimeSeriesDecomposer, DecompositionMethod

decomposer = TimeSeriesDecomposer()

# STL decomposition
result = decomposer.stl_decompose(
    data=sales_series,
    period=7,  # weekly seasonality
    seasonal_window=7,
    robust=True,
)

print(f"Trend strength:   {result.trend_strength:.3f}")
print(f"Seasonal strength: {result.seasonal_strength:.3f}")
print(f"Residual std:     {result.residual_std:.4f}")

# Multiple seasonalities (MSTL)
mstl_result = decomposer.mstl_decompose(
    data=hourly_energy,
    periods=[24, 168],  # daily + weekly
    seasonal_windows=[7, 14],
)
print(f"Seasonal periods: {mstl_result.periods}")
print(f"Remainder variance: {mstl_result.remainder_variance:.4f}")
```

### ARIMA Forecasting

```python
from time_series import ARIMAForecaster, ForecastHorizon

forecaster = ARIMAForecaster()

# Auto-ARIMA with order selection
model = forecaster.auto_arima(
    data=train_series,
    seasonal=True,
    m=12,  # monthly seasonality
    max_p=5, max_q=5, max_P=2, max_Q=2,
    information_criterion="aic",
    stepwise=True,
    trace=True,
)

# Generate forecasts
forecast = model.forecast(
    steps=24,
    alpha=0.05,
    return_conf_int=True,
)

print(f"Forecast values: {forecast.values[:6]}")
print(f"95% CI: {forecast.conf_int[:3]}")
print(f"AIC: {model.aic:.2f}")
print(f"BIC: {model.bic:.2f}")
print(f"Ljung-Box p-value: {model.ljung_box_pvalue:.4f}")

# Model diagnostics
diagnostics = model.diagnostics()
print(f"Residual normality: {diagnostics.shapiro_pvalue:.4f}")
print(f"Residual ACF: {diagnostics.acf_max_lag10:.4f}")
```

### Anomaly Detection

```python
from time_series import AnomalyDetector, AnomalyMethod

detector = AnomalyDetector()

# Seasonal ESD (Twitter algorithm)
anomalies = detector.seasonal_esd(
    data=metrics_series,
    period=24,  # hourly data with daily seasonality
    k=10,  # max anomalies to detect
    alpha=0.05,
)

print(f"Detected {len(anomalies.points)} anomalies")
for a in anomalies.points[:5]:
    print(f"  {a.timestamp}: value={a.value:.2f}, expected={a.expected:.2f}, "
          f"severity={a.severity:.3f}")

# Adaptive threshold detection
threshold_result = detector.adaptive_threshold(
    data=metrics_series,
    window_size=48,
    n_sigma=3.0,
    method="mad",
)
print(f"Threshold violations: {threshold_result.n_violations}")
print(f"Anomaly rate: {threshold_result.anomaly_rate:.4f}")
```

### Change Point Detection

```python
from time_series import ChangePointDetector, CPDMethod

cpd = ChangePointDetector()

# Bayesian Online Change Point Detection
bocpd_result = cpd.bayesian_online(
    data=system_metrics,
    hazard_rate=1/200,  # expected changepoint every 200 points
    observation_likelihood="student_t",
)

print(f"Change points: {bocpd_result.change_points}")
print(f"Run lengths: {bocpd_result.current_run_length}")

# PELT
pelt_result = cpd.pelt(
    data=system_metrics,
    cost_function="rbf",
    penalty="auto",
)
print(f"PELT change points: {pelt_result.change_points}")
print(f"Segments: {pelt_result.n_segments}")
```

### Spectral Analysis

```python
from time_series import SpectralAnalyzer

analyzer = SpectralAnalyzer()

# Power Spectral Density
psd = analyzer.power_spectral_density(
    data=sensor_signal,
    fs=1000,  # sampling frequency Hz
    method="welch",
    nperseg=256,
)

# Find dominant frequencies
dominant = analyzer.find_dominant_frequencies(psd, n_top=5)
for freq, power in dominant:
    print(f"  Frequency: {freq:.2f} Hz, Power: {power:.4f}")

# Wavelet transform
wavelet = analyzer.continuous_wavelet_transform(
    data=sensor_signal,
    scales=np.arange(1, 128),
    wavelet="morlet",
)
print(f"Wavelet coefficients shape: {wavelet.coefficients.shape}")
print(f"Scale with max energy: {wavelet.scales[np.argmax(np.abs(wavelet.coefficients).max(axis=1))]}")
```

## Best Practices

### Decomposition
- Use STL for robust decomposition with missing values; classical for clean data
- Check seasonal strength > 0.6 before including seasonal component in models
- For multiple seasonalities (e.g., hourly data with daily + weekly patterns), use MSTL
- Examine residuals for remaining patterns — they should be white noise

### Forecasting
- Always split data chronologically (never randomly) for train/test
- Use auto-ARIMA for initial order selection, then refine based on domain knowledge
- Compare multiple models (ARIMA vs ETS vs Prophet) using cross-validation RMSE
- Report prediction intervals, not just point forecasts — uncertainty matters

### Anomaly Detection
- Seasonal ESD works best when seasonality is strong and stable
- For irregular patterns, use model-based detection (ARIMA residuals)
- Validate anomalies manually — automated detection always has false positives
- Use adaptive thresholds when the baseline shifts over time

### Change Point Detection
- Set hazard rate based on expected frequency of changes in your domain
- Use PELT for offline detection with known data; BOCPD for streaming
- Validate detected change points against known events (deployments, incidents)
- Consider lag — change points may be detected with a delay in real-time systems

## Related Modules

- **statistical-analysis**: Foundational statistical tests for time series assumptions
- **feature-engineering**: Lag features, rolling statistics, and date decomposition
- **advanced-analytics**: Bayesian methods for state-space models
- **data-visualization**: Time series plotting with trend and seasonality overlays