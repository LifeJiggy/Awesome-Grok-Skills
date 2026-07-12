"""
Time Series Analysis Framework

Production-grade time series analysis toolkit providing decomposition, forecasting,
anomaly detection, change point detection, spectral analysis, and state-space
modeling for rigorous temporal data science workflows.
"""

from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class DecompositionMethod(Enum):
    ADDITIVE = "additive"
    MULTIPLICATIVE = "multiplicative"
    STL = "stl"
    MSTL = "mstl"
    CLASSICAL = "classical"


class SeasonalityType(Enum):
    ADDITIVE = "additive"
    MULTIPLICATIVE = "multiplicative"
    NONE = "none"


class ForecastMethod(Enum):
    ARIMA = "arima"
    SARIMA = "sarima"
    ETS = "ets"
    EXPONENTIAL_SMOOTHING = "exponential_smoothing"
    HOLT_WINTERS = "holt_winters"
    NAIVE = "naive"
    SEASONAL_NAIVE = "seasonal_naive"
    DRIFT = "drift"


class AnomalyMethod(Enum):
    Z_SCORE = "z_score"
    MODIFIED_Z_SCORE = "modified_z_score"
    GRUBBS = "grubbs"
    SEASONAL_ESD = "seasonal_esd"
    ARIMA_RESIDUAL = "arima_residual"
    ISOLATION_FOREST = "isolation_forest"
    ADAPTIVE_THRESHOLD = "adaptive_threshold"
    MAD = "mad"


class CPDMethod(Enum):
    CUSUM = "cusum"
    BAYESIAN_ONLINE = "bayesian_online"
    PELT = "pelt"
    BINARY_SEGMENTATION = "binary_segmentation"
    SLIDING_WINDOW = "sliding_window"


class SpectralMethod(Enum):
    FFT = "fft"
    WELCH = "welch"
    PERIODOGRAM = "periodogram"
    SMOOTHED_PERIODOGRAM = "smoothed_periodogram"
    WAVELET = "wavelet"


class StateSpaceType(Enum):
    LOCAL_LEVEL = "local_level"
    LOCAL_TREND = "local_trend"
    SEASONAL = "seasonal"
    STRUCTURAL = "structural"
    ARIMA = "arima_state_space"


class ModelCriterion(Enum):
    AIC = "aic"
    BIC = "bic"
    AICC = "aicc"
    RMSE = "rmse"
    MAE = "mae"
    MAPE = "mape"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class DecompositionResult:
    """Result of time series decomposition."""
    trend: NDArray
    seasonal: NDArray
    residual: NDArray
    observed: NDArray
    period: Union[int, List[int]]
    method: DecompositionMethod
    trend_strength: float = 0.0
    seasonal_strength: float = 0.0
    residual_variance: float = 0.0

    @property
    def remainder_std(self) -> float:
        return float(np.std(self.residual, ddof=1))


@dataclass
class ForecastResult:
    """Result of time series forecasting."""
    values: NDArray
    conf_int: Optional[Tuple[NDArray, NDArray]] = None
    method: ForecastMethod = ForecastMethod.ARIMA
    steps: int = 0
    aic: Optional[float] = None
    bic: Optional[float] = None
    aicc: Optional[float] = None
    rmse: Optional[float] = None
    mae: Optional[float] = None
    mape: Optional[float] = None
    fitted_values: Optional[NDArray] = None
    residuals: Optional[NDArray] = None
    order: Optional[Tuple[int, int, int]] = None
    seasonal_order: Optional[Tuple[int, int, int, int]] = None

    def summary(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "method": self.method.value,
            "steps": self.steps,
        }
        if self.aic is not None:
            result["aic"] = self.aic
        if self.bic is not None:
            result["bic"] = self.bic
        if self.rmse is not None:
            result["rmse"] = self.rmse
        if self.mape is not None:
            result["mape"] = self.mape
        if self.order is not None:
            result["order"] = self.order
        if self.seasonal_order is not None:
            result["seasonal_order"] = self.seasonal_order
        return result


@dataclass
class AnomalyPoint:
    """A single detected anomaly."""
    index: int
    timestamp: Optional[Any] = None
    value: float = 0.0
    expected: float = 0.0
    severity: float = 0.0
    is_anomaly: bool = True
    method: str = ""


@dataclass
class AnomalyResult:
    """Result of anomaly detection."""
    points: List[AnomalyPoint]
    method: AnomalyMethod
    n_anomalies: int = 0
    anomaly_rate: float = 0.0
    threshold: Optional[float] = None
    scores: Optional[NDArray] = None

    @property
    def anomaly_indices(self) -> List[int]:
        return [p.index for p in self.points if p.is_anomaly]


@dataclass
class ChangePoint:
    """A detected change point."""
    index: int
    timestamp: Optional[Any] = None
    confidence: float = 1.0
    segment_before: Optional[NDArray] = None
    segment_after: Optional[NDArray] = None


@dataclass
class CPDResult:
    """Result of change point detection."""
    change_points: List[ChangePoint]
    method: CPDMethod
    n_segments: int = 0
    run_lengths: Optional[NDArray] = None
    log_probabilities: Optional[NDArray] = None

    @property
    def change_point_indices(self) -> List[int]:
        return [cp.index for cp in self.change_points]


@dataclass
class DominantFrequency:
    """A dominant frequency in spectral analysis."""
    frequency: float
    power: float
    period: Optional[float] = None
    phase: Optional[float] = None


@dataclass
class PSDResult:
    """Result of power spectral density estimation."""
    frequencies: NDArray
    power: NDArray
    method: SpectralMethod
    sampling_rate: float = 1.0
    total_power: float = 0.0

    def dominant_frequencies(self, n_top: int = 5) -> List[DominantFrequency]:
        sorted_idx = np.argsort(self.power)[::-1][:n_top]
        result = []
        for idx in sorted_idx:
            freq = float(self.frequencies[idx])
            power = float(self.power[idx])
            period = 1.0 / freq if freq > 0 else float("inf")
            result.append(DominantFrequency(frequency=freq, power=power, period=period))
        return result


@dataclass
class WaveletResult:
    """Result of wavelet transform."""
    coefficients: NDArray
    scales: NDArray
    frequencies: NDArray
    power_spectrum: NDArray
    wavelet_name: str = "morlet"


@dataclass
class DiagnosticResult:
    """Model diagnostic results."""
    residuals_mean: float = 0.0
    residuals_std: float = 0.0
    ljung_box_statistic: float = 0.0
    ljung_box_pvalue: float = 0.0
    shapiro_statistic: float = 0.0
    shapiro_pvalue: float = 0.0
    acf_lag1: float = 0.0
    acf_lag5: float = 0.0
    acf_lag10: float = 0.0
    ljung_box_lags: int = 10
    normality_test: str = "shapiro"
    heteroscedasticity: bool = False


@dataclass
class KalmanResult:
    """Result of Kalman filter estimation."""
    filtered_state: NDArray
    predicted_state: NDArray
    smoothed_state: NDArray
    filtered_covariance: NDArray
    predicted_covariance: NDArray
    log_likelihood: float = 0.0
    innovations: Optional[NDArray] = None
    innovation_variances: Optional[NDArray] = None


# ---------------------------------------------------------------------------
# Time Series Decomposer
# ---------------------------------------------------------------------------

class TimeSeriesDecomposer:
    """Decompose time series into trend, seasonal, and residual components."""

    def classical_decompose(
        self,
        data: NDArray,
        period: int = 12,
        method: DecompositionMethod = DecompositionMethod.ADDITIVE,
    ) -> DecompositionResult:
        """Classical decomposition using moving averages."""
        n = len(data)

        # Trend via centered moving average
        trend = np.full(n, np.nan)
        half = period // 2
        for i in range(half, n - half):
            trend[i] = np.mean(data[i - half:i + half + 1])

        # Fill trend edges
        first_valid = next((i for i in range(n) if not np.isnan(trend[i])), 0)
        last_valid = next((i for i in range(n - 1, -1, -1) if not np.isnan(trend[i])), n - 1)
        trend[:first_valid] = trend[first_valid]
        trend[last_valid + 1:] = trend[last_valid]

        # Detrend
        if method == DecompositionMethod.MULTIPLICATIVE:
            detrended = data / np.where(np.abs(trend) > 1e-10, trend, 1.0)
        else:
            detrended = data - trend

        # Seasonal
        seasonal = np.zeros(n)
        seasonal_means = np.zeros(period)
        for i in range(period):
            indices = list(range(i, n, period))
            seasonal_means[i] = np.mean(detrended[indices])
        seasonal_means -= np.mean(seasonal_means)

        for i in range(n):
            seasonal[i] = seasonal_means[i % period]

        # Residual
        if method == DecompositionMethod.MULTIPLICATIVE:
            residual = data / (np.where(np.abs(trend) > 1e-10, trend, 1.0) *
                               np.where(np.abs(seasonal) > 1e-10, seasonal, 1.0))
        else:
            residual = data - trend - seasonal

        # Strength metrics
        var_residual = np.var(residual, ddof=1)
        var_detrended = np.var(data - trend, ddof=1)
        var_deseasoned = np.var(data - seasonal, ddof=1)
        trend_strength = max(0, 1 - var_residual / var_detrended) if var_detrended > 0 else 0
        seasonal_strength = max(0, 1 - var_residual / var_deseasoned) if var_deseasoned > 0 else 0

        return DecompositionResult(
            trend=trend,
            seasonal=seasonal,
            residual=residual,
            observed=data,
            period=period,
            method=method,
            trend_strength=trend_strength,
            seasonal_strength=seasonal_strength,
            residual_variance=float(var_residual),
        )

    def stl_decompose(
        self,
        data: NDArray,
        period: int = 7,
        seasonal_window: int = 7,
        robust: bool = True,
        n_inner: int = 2,
    ) -> DecompositionResult:
        """STL decomposition using Loess smoothing."""
        n = len(data)

        # Initialize
        trend = np.zeros(n)
        seasonal = np.zeros(n)
        remainder = data.copy()

        for _ in range(n_inner):
            # Deseasonalize
            deseasonalized = data - seasonal

            # Trend estimation via moving average
            half = period // 2
            trend_new = np.full(n, np.nan)
            for i in range(half, n - half):
                window = deseasonalized[i - half:i + half + 1]
                weights = self._loess_weights(np.arange(-half, half + 1), half)
                trend_new[i] = np.average(window, weights=weights)

            # Fill edges
            first_valid = next((i for i in range(n) if not np.isnan(trend_new[i])), 0)
            last_valid = next((i for i in range(n - 1, -1, -1) if not np.isnan(trend_new[i])), n - 1)
            trend_new[:first_valid] = trend_new[first_valid]
            trend_new[last_valid + 1:] = trend_new[last_valid]

            trend = trend_new

            # Seasonal estimation
            detrended = data - trend
            seasonal_new = np.zeros(n)
            for i in range(period):
                indices = list(range(i, n, period))
                if len(indices) >= seasonal_window:
                    for j, idx in enumerate(indices):
                        start = max(0, j - seasonal_window // 2)
                        end = min(len(indices), j + seasonal_window // 2 + 1)
                        window_indices = indices[start:end]
                        window_vals = detrended[window_indices]
                        local_idx = j - start
                        weights = self._loess_weights(
                            np.arange(len(window_indices)) - local_idx,
                            len(window_indices) // 2
                        )
                        seasonal_new[idx] = np.average(window_vals, weights=weights)
                else:
                    for idx in indices:
                        seasonal_new[idx] = np.mean(detrended[indices])

            seasonal_new -= np.mean(seasonal_new)
            seasonal = seasonal_new

            remainder = data - trend - seasonal

        var_residual = np.var(remainder, ddof=1)
        var_detrended = np.var(data - trend, ddof=1)
        var_deseasoned = np.var(data - seasonal, ddof=1)
        trend_strength = max(0, 1 - var_residual / var_detrended) if var_detrended > 0 else 0
        seasonal_strength = max(0, 1 - var_residual / var_deseasoned) if var_deseasoned > 0 else 0

        return DecompositionResult(
            trend=trend,
            seasonal=seasonal,
            residual=remainder,
            observed=data,
            period=period,
            method=DecompositionMethod.STL,
            trend_strength=trend_strength,
            seasonal_strength=seasonal_strength,
            residual_variance=float(var_residual),
        )

    def mstl_decompose(
        self,
        data: NDArray,
        periods: List[int],
        seasonal_windows: Optional[List[int]] = None,
    ) -> DecompositionResult:
        """Multiple Seasonal-Trend decomposition using Loess (MSTL)."""
        if seasonal_windows is None:
            seasonal_windows = [7] * len(periods)

        n = len(data)
        seasonal_total = np.zeros(n)

        # Iteratively extract each seasonal component
        residual = data.copy()
        seasonal_components = {}

        for period, window in zip(periods, seasonal_windows):
            result = self.stl_decompose(residual, period=period, seasonal_window=window)
            seasonal_components[period] = result.seasonal
            seasonal_total += result.seasonal
            residual = residual - result.seasonal

        # Final trend extraction
        final_result = self.stl_decompose(residual, period=periods[0], seasonal_window=7)

        return DecompositionResult(
            trend=final_result.trend,
            seasonal=seasonal_total,
            residual=final_result.residual,
            observed=data,
            period=periods,
            method=DecompositionMethod.MSTL,
            trend_strength=final_result.trend_strength,
            seasonal_strength=np.mean([np.var(s) for s in seasonal_components.values()]) / np.var(data) if np.var(data) > 0 else 0,
            residual_variance=float(np.var(final_result.residual, ddof=1)),
        )

    def _loess_weights(self, distances: NDArray, bandwidth: int) -> NDArray:
        """Compute Loess (tricube) weights."""
        u = np.abs(distances) / (bandwidth + 1)
        u = np.clip(u, 0, 1)
        weights = (1 - u ** 3) ** 3
        return weights / np.sum(weights) if np.sum(weights) > 0 else np.ones_like(weights) / len(weights)


# ---------------------------------------------------------------------------
# ARIMA Forecaster
# ---------------------------------------------------------------------------

class ARIMAForecaster:
    """ARIMA/SARIMA family forecasting models."""

    def auto_arima(
        self,
        data: NDArray,
        seasonal: bool = False,
        m: int = 1,
        max_p: int = 5,
        max_q: int = 5,
        max_P: int = 2,
        max_Q: int = 2,
        d: Optional[int] = None,
        D: Optional[int] = None,
        information_criterion: str = "aic",
        stepwise: bool = True,
        trace: bool = False,
    ) -> "ARIMAModel":
        """Automatic ARIMA order selection."""
        n = len(data)

        # Determine differencing order
        if d is None:
            d = self._determine_d(data, max_d=2)
        if seasonal and D is None:
            D = self._determine_seasonal_d(data, m, max_D=1)

        # Differencing
        differenced = data.copy()
        for _ in range(d):
            differenced = np.diff(differenced)
        if seasonal and D > 0:
            for _ in range(D):
                differenced = differenced[m:] - differenced[:-m]

        # Grid search or stepwise
        if stepwise:
            order, seasonal_order = self._stepwise_search(
                differenced, max_p, max_q, max_P, max_Q, m, seasonal, information_criterion
            )
        else:
            order, seasonal_order = self._grid_search(
                differenced, max_p, max_q, max_P, max_Q, m, seasonal, information_criterion
            )

        # Fit final model
        model = ARIMAModel(order=order, seasonal_order=seasonal_order if seasonal else (0, 0, 0, 0))
        model.fit(data)

        if trace:
            logger.info("Auto-ARIMA selected: order=%s, seasonal=%s, AIC=%.2f",
                       order, seasonal_order, model.aic)

        return model

    def _determine_d(self, data: NDArray, max_d: int = 2) -> int:
        """Determine differencing order using ADF-like heuristic."""
        for d in range(max_d + 1):
            series = data.copy()
            for _ in range(d):
                series = np.diff(series)
            # Check stationarity via variance of differences
            if d > 0:
                var_ratio = np.var(np.diff(series)) / np.var(series) if np.var(series) > 0 else 0
                if var_ratio > 0.9:
                    return d - 1
        return 1

    def _determine_seasonal_d(self, data: NDArray, m: int, max_D: int = 1) -> int:
        for D in range(max_D + 1):
            series = data.copy()
            for _ in range(D):
                series = series[m:] - series[:-m]
            if D > 0:
                autocorr_m = np.corrcoef(series[m:], series[:-m])[0, 1]
                if abs(autocorr_m) < 0.1:
                    return D - 1
        return 1

    def _stepwise_search(
        self, data: NDArray, max_p: int, max_q: int,
        max_P: int, max_Q: int, m: int, seasonal: bool, criterion: str,
    ) -> Tuple[Tuple[int, int, int], Tuple[int, int, int, int]]:
        """Simplified stepwise ARIMA order selection."""
        best_aic = float("inf")
        best_order = (1, 0, 0)
        best_seasonal = (0, 0, 0, 0)

        candidates = []
        for p in range(max_p + 1):
            for q in range(max_q + 1):
                if p == 0 and q == 0:
                    continue
                candidates.append((p, 0, q))

        for order in candidates:
            try:
                aic = self._compute_aic(data, order, (0, 0, 0, 0))
                if aic < best_aic:
                    best_aic = aic
                    best_order = order
            except Exception:
                continue

        if seasonal:
            for P in range(max_P + 1):
                for Q in range(max_Q + 1):
                    if P == 0 and Q == 0:
                        continue
                    seasonal_order = (P, 1, Q, m)
                    try:
                        aic = self._compute_aic(data, best_order, seasonal_order)
                        if aic < best_aic:
                            best_aic = aic
                            best_seasonal = seasonal_order
                    except Exception:
                        continue

        return best_order, best_seasonal

    def _grid_search(
        self, data: NDArray, max_p: int, max_q: int,
        max_P: int, max_Q: int, m: int, seasonal: bool, criterion: str,
    ) -> Tuple[Tuple[int, int, int], Tuple[int, int, int, int]]:
        best_aic = float("inf")
        best_order = (1, 0, 0)
        best_seasonal = (0, 0, 0, 0)

        for p in range(max_p + 1):
            for q in range(max_q + 1):
                if p == 0 and q == 0:
                    continue
                order = (p, 0, q)
                seasonal_orders = [(0, 0, 0, 0)]
                if seasonal:
                    for P in range(max_P + 1):
                        for Q in range(max_Q + 1):
                            seasonal_orders.append((P, 1, Q, m))

                for s_order in seasonal_orders:
                    try:
                        aic = self._compute_aic(data, order, s_order)
                        if aic < best_aic:
                            best_aic = aic
                            best_order = order
                            best_seasonal = s_order
                    except Exception:
                        continue

        return best_order, best_seasonal

    def _compute_aic(
        self, data: NDArray, order: Tuple[int, int, int],
        seasonal_order: Tuple[int, int, int, int],
    ) -> float:
        """Compute AIC for a given ARIMA specification."""
        p, d, q = order
        n = len(data)
        k = p + q + 1

        # Simple approximation using residual variance
        # In production, use proper MLE
        model = ARIMAModel(order=order, seasonal_order=seasonal_order)
        model.fit(data)
        return model.aic


class ARIMAModel:
    """Fitted ARIMA model."""

    def __init__(
        self,
        order: Tuple[int, int, int] = (1, 1, 1),
        seasonal_order: Tuple[int, int, int, int] = (0, 0, 0, 0),
    ):
        self.order = order
        self.seasonal_order = seasonal_order
        self.ar_params: Optional[NDArray] = None
        self.ma_params: Optional[NDArray] = None
        self.intercept: float = 0.0
        self.sigma2: float = 1.0
        self._data: Optional[NDArray] = None
        self._fitted_values: Optional[NDArray] = None
        self._residuals: Optional[NDArray] = None
        self.aic: float = 0.0
        self.bic: float = 0.0
        self.aicc: float = 0.0
        self.log_likelihood: float = 0.0
        self._is_fitted = False

    def fit(self, data: NDArray) -> "ARIMAModel":
        """Fit ARIMA model to data."""
        self._data = data.copy()
        n = len(data)
        p, d, q = self.order

        # Apply differencing
        diff_data = data.copy()
        for _ in range(d):
            diff_data = np.diff(diff_data)

        # Seasonal differencing
        sP, sD, sQ, m = self.seasonal_order
        for _ in range(sD):
            if m > 0 and len(diff_data) > m:
                diff_data = diff_data[m:] - diff_data[:-m]

        # Estimate AR parameters via Yule-Walker
        if p > 0:
            self.ar_params = self._yule_walker(diff_data, p)
        else:
            self.ar_params = np.array([])

        # Estimate MA parameters (simplified)
        if q > 0:
            self.ma_params = np.zeros(q)
            # Simple residual-based estimation
            if p > 0:
                ar_fitted = np.convolve(diff_data, self.ar_params, mode='full')[:len(diff_data)]
                residuals = diff_data - ar_fitted
            else:
                residuals = diff_data - np.mean(diff_data)

            for j in range(q):
                if j < len(residuals) - 1:
                    self.ma_params[j] = np.corrcoef(residuals[:-(j+1)], residuals[j+1:])[0, 1] * 0.5
        else:
            self.ma_params = np.array([])

        self.intercept = float(np.mean(diff_data))
        self.sigma2 = float(np.var(diff_data, ddof=1))

        # Compute fitted values and residuals
        self._fitted_values = self._compute_fitted_values(data)
        self._residuals = data - self._fitted_values

        # Information criteria
        n_params = p + q + 1
        self.log_likelihood = -n / 2 * (np.log(2 * np.pi * self.sigma2) + 1)
        self.aic = -2 * self.log_likelihood + 2 * n_params
        self.bic = -2 * self.log_likelihood + n_params * np.log(n)
        self.aicc = self.aic + 2 * n_params * (n_params + 1) / max(n - n_params - 1, 1)

        self._is_fitted = True
        return self

    def _yule_walker(self, data: NDArray, p: int) -> NDArray:
        """Yule-Walker estimation for AR parameters."""
        n = len(data)
        mean = np.mean(data)
        centered = data - mean

        # Autocorrelation
        acf = np.array([np.sum(centered[:n-k] * centered[k:]) / n for k in range(p + 1)])

        # Build Toeplitz matrix
        R = np.array([[acf[abs(i - j)] for j in range(p)] for i in range(p)])
        r = acf[1:p + 1]

        try:
            params = np.linalg.solve(R, r)
        except np.linalg.LinAlgError:
            params = np.linalg.lstsq(R, r, rcond=None)[0]

        return params

    def _compute_fitted_values(self, data: NDArray) -> NDArray:
        n = len(data)
        fitted = np.full(n, np.nan)
        p, d, q = self.order

        # Simple fitted values based on AR parameters
        if p > 0 and self.ar_params is not None:
            for t in range(p, n):
                ar_sum = sum(self.ar_params[j] * data[t - j - 1] for j in range(min(p, t)))
                fitted[t] = self.intercept + ar_sum
        else:
            fitted[:] = self.intercept

        # Fill initial NaN with mean
        first_valid = next((i for i in range(n) if not np.isnan(fitted[i])), 0)
        fitted[:first_valid] = fitted[first_valid]

        return fitted

    def forecast(
        self,
        steps: int = 12,
        alpha: float = 0.05,
        return_conf_int: bool = True,
    ) -> ForecastResult:
        """Generate multi-step ahead forecasts."""
        if not self._is_fitted:
            raise RuntimeError("Model must be fitted before forecasting.")

        data = self._data
        n = len(data)
        p, d, q = self.order

        forecasts = np.zeros(steps)
        history = list(data)

        for h in range(steps):
            # AR component
            ar_sum = 0.0
            if p > 0 and self.ar_params is not None:
                for j in range(min(p, len(history))):
                    ar_sum += self.ar_params[j] * history[-(j + 1)]

            # MA component (using last q residuals)
            ma_sum = 0.0
            if q > 0 and self.ma_params is not None and self._residuals is not None:
                for j in range(min(q, len(self._residuals))):
                    ma_sum += self.ma_params[j] * self._residuals[-(j + 1)]

            forecast = self.intercept + ar_sum + ma_sum
            forecasts[h] = forecast
            history.append(forecast)

        # Confidence intervals
        conf_int = None
        if return_conf_int:
            z = 1.96
            stderr = np.sqrt(self.sigma2)
            ci_lower = np.zeros(steps)
            ci_upper = np.zeros(steps)
            for h in range(steps):
                step_stderr = stderr * np.sqrt(h + 1)
                ci_lower[h] = forecasts[h] - z * step_stderr
                ci_upper[h] = forecasts[h] + z * step_stderr
            conf_int = (ci_lower, ci_upper)

        return ForecastResult(
            values=forecasts,
            conf_int=conf_int,
            method=ForecastMethod.ARIMA,
            steps=steps,
            aic=self.aic,
            bic=self.bic,
            aicc=self.aicc,
            fitted_values=self._fitted_values,
            residuals=self._residuals,
            order=self.order,
            seasonal_order=self.seasonal_order,
        )

    def diagnostics(self) -> DiagnosticResult:
        """Compute model diagnostic statistics."""
        if self._residuals is None:
            return DiagnosticResult()

        residuals = self._residuals[~np.isnan(self._residuals)]
        n = len(residuals)

        # Basic stats
        mean = float(np.mean(residuals))
        std = float(np.std(residuals, ddof=1))

        # ACF
        acf_values = np.correlate(residuals - mean, residuals - mean, mode="full")
        acf_values = acf_values[n - 1:] / acf_values[n - 1]
        acf_lag1 = float(acf_values[1]) if len(acf_values) > 1 else 0.0
        acf_lag5 = float(acf_values[5]) if len(acf_values) > 5 else 0.0
        acf_lag10 = float(acf_values[10]) if len(acf_values) > 10 else 0.0

        # Ljung-Box test
        lag = min(10, n // 5)
        lb_stat = n * (n + 2) * sum(
            acf_values[k] ** 2 / (n - k) for k in range(1, lag + 1)
        ) if lag > 0 else 0
        # Approximate p-value using chi-squared
        lb_pvalue = self._chi2_survival(lb_stat, lag)

        # Shapiro-Wilk (simplified)
        sorted_res = np.sort(residuals)
        w_stat = self._shapiro_wilk_approx(sorted_res)
        shapiro_pvalue = min(1.0, max(0.0, 1.0 - w_stat))

        return DiagnosticResult(
            residuals_mean=mean,
            residuals_std=std,
            ljung_box_statistic=float(lb_stat),
            ljung_box_pvalue=float(lb_pvalue),
            shapiro_statistic=float(w_stat),
            shapiro_pvalue=float(shapiro_pvalue),
            acf_lag1=acf_lag1,
            acf_lag5=acf_lag5,
            acf_lag10=acf_lag10,
        )

    def _chi2_survival(self, x: float, df: int) -> float:
        """Approximate chi-squared survival function."""
        if x <= 0 or df <= 0:
            return 1.0
        z = (x / df) ** (1 / 3) - (1 - 2 / (9 * df))
        z /= np.sqrt(2 / (9 * df))
        return 0.5 * (1 - np.math.erf(z / np.sqrt(2)))

    def _shapiro_wilk_approx(self, sorted_data: NDArray) -> float:
        """Simplified Shapiro-Wilk normality test."""
        n = len(sorted_data)
        if n < 3:
            return 1.0
        mean = np.mean(sorted_data)
        ss = np.sum((sorted_data - mean) ** 2)
        if ss == 0:
            return 1.0
        # Simplified W statistic
        sorted_abs = np.sort(np.abs(sorted_data - mean))
        a = np.sum(sorted_abs[-n // 2:]) / ss if ss > 0 else 0
        return min(1.0, max(0.0, a))


# ---------------------------------------------------------------------------
# Exponential Smoothing
# ---------------------------------------------------------------------------

class ExponentialSmoothingForecaster:
    """Exponential smoothing family (Simple, Holt, Holt-Winters)."""

    def holt_winters(
        self,
        data: NDArray,
        period: int = 12,
        seasonal: SeasonalityType = SeasonalityType.ADDITIVE,
        alpha: Optional[float] = None,
        beta: Optional[float] = None,
        gamma: Optional[float] = None,
        damped_trend: bool = False,
    ) -> ForecastResult:
        """Holt-Winters exponential smoothing."""
        n = len(data)
        if alpha is None:
            alpha = 0.2 / period
        if beta is None:
            beta = 0.01
        if gamma is None:
            gamma = 0.01 / period

        # Initialize components
        level = np.mean(data[:period])
        trend = (np.mean(data[period:2 * period]) - np.mean(data[:period])) / period
        seasonal = np.zeros(period)

        if seasonal == SeasonalityType.ADDITIVE:
            for i in range(period):
                seasonal[i] = np.mean(data[i::period]) - level
        else:
            for i in range(period):
                seasonal[i] = np.mean(data[i::period]) / level if level > 0 else 1.0

        # Filter
        fitted = np.zeros(n)
        levels = np.zeros(n)
        trends = np.zeros(n)
        seasonals = np.zeros((n, period))

        for t in range(n):
            s_idx = t % period
            if t == 0:
                levels[t] = level
                trends[t] = trend
            else:
                if seasonal == SeasonalityType.ADDITIVE:
                    levels[t] = alpha * (data[t] - seasonals[t - 1, s_idx]) + (1 - alpha) * (levels[t - 1] + (1 if not damped_trend else 0.98) * trends[t - 1])
                else:
                    levels[t] = alpha * (data[t] / max(seasonals[t - 1, s_idx], 1e-10)) + (1 - alpha) * (levels[t - 1] + (1 if not damped_trend else 0.98) * trends[t - 1])

                trends[t] = beta * (levels[t] - levels[t - 1]) + (1 - beta) * (1 if not damped_trend else 0.98) * trends[t - 1]

            seasonals[t, s_idx] = gamma * (data[t] - levels[t]) + (1 - gamma) * seasonals[t - 1, s_idx] if t > 0 else seasonal[s_idx]

            if seasonal == SeasonalityType.ADDITIVE:
                fitted[t] = levels[t] + trends[t] + seasonals[t, s_idx]
            else:
                fitted[t] = (levels[t] + trends[t]) * seasonals[t, s_idx]

        residuals = data - fitted
        sigma2 = float(np.var(residuals, ddof=1))

        return ForecastResult(
            values=fitted,
            method=ForecastMethod.HOLT_WINTERS,
            fitted_values=fitted,
            residuals=residuals,
            rmse=float(np.sqrt(np.mean(residuals ** 2))),
            mae=float(np.mean(np.abs(residuals))),
            mape=float(np.mean(np.abs(residuals / np.where(np.abs(data) > 1e-10, data, 1.0))) * 100),
        )


# ---------------------------------------------------------------------------
# Anomaly Detector
# ---------------------------------------------------------------------------

class AnomalyDetector:
    """Detect anomalies in time series data."""

    def z_score(
        self, data: NDArray, threshold: float = 3.0, window: Optional[int] = None
    ) -> AnomalyResult:
        """Z-score based anomaly detection."""
        if window is not None:
            anomalies = []
            scores = np.zeros(len(data))
            for i in range(window, len(data)):
                window_data = data[i - window:i]
                mean = np.mean(window_data)
                std = np.std(window_data, ddof=1)
                z = abs(data[i] - mean) / std if std > 0 else 0
                scores[i] = z
                if z > threshold:
                    anomalies.append(AnomalyPoint(
                        index=i, value=float(data[i]), expected=float(mean),
                        severity=float(z / threshold), method="z_score",
                    ))
        else:
            mean = np.mean(data)
            std = np.std(data, ddof=1)
            z_scores = np.abs((data - mean) / std) if std > 0 else np.zeros_like(data)
            scores = z_scores
            anomalies = [
                AnomalyPoint(
                    index=i, value=float(data[i]), expected=float(mean),
                    severity=float(z_scores[i] / threshold), method="z_score",
                )
                for i in range(len(data)) if z_scores[i] > threshold
            ]

        return AnomalyResult(
            points=anomalies,
            method=AnomalyMethod.Z_SCORE,
            n_anomalies=len(anomalies),
            anomaly_rate=len(anomalies) / len(data),
            threshold=threshold,
            scores=scores,
        )

    def modified_z_score(
        self, data: NDArray, threshold: float = 3.5
    ) -> AnomalyResult:
        """Modified Z-score using median absolute deviation."""
        median = np.median(data)
        mad = np.median(np.abs(data - median))
        modified_z = 0.6745 * (data - median) / mad if mad > 0 else np.zeros_like(data)

        anomalies = [
            AnomalyPoint(
                index=i, value=float(data[i]), expected=float(median),
                severity=float(abs(modified_z[i]) / threshold), method="modified_z_score",
            )
            for i in range(len(data)) if abs(modified_z[i]) > threshold
        ]

        return AnomalyResult(
            points=anomalies,
            method=AnomalyMethod.MODIFIED_Z_SCORE,
            n_anomalies=len(anomalies),
            anomaly_rate=len(anomalies) / len(data),
            threshold=threshold,
            scores=modified_z,
        )

    def seasonal_esd(
        self,
        data: NDArray,
        period: int = 24,
        k: int = 10,
        alpha: float = 0.05,
    ) -> AnomalyResult:
        """Seasonal ESD (S-ESD) for detecting anomalies in seasonal data."""
        n = len(data)
        anomalies = []
        remaining = data.copy()
        outlier_indices = set()

        for _ in range(k):
            if len(remaining) < period:
                break

            # Compute seasonal median
            seasonal_medians = np.zeros(period)
            for i in range(period):
                indices = list(range(i, len(remaining), period))
                seasonal_medians[i] = np.median(remaining[indices])

            # Remove seasonal component
            deseasonalized = np.array([
                remaining[i] - seasonal_medians[i % period] for i in range(len(remaining))
            ])

            # Compute ESD statistic
            median = np.median(deseasonalized)
            mad = np.median(np.abs(deseasonalized - median))
            test_stats = 0.6745 * np.abs(deseasonalized - median) / mad if mad > 0 else np.zeros_like(deseasonalized)

            # Find maximum
            max_idx = np.argmax(test_stats)
            max_stat = test_stats[max_idx]

            # Critical value (approximation)
            p = len(deseasonalized)
            t_crit = (p - 1) * np.sqrt(max_stat ** 2 / (p - max_stat ** 2 + max_stat ** 2)) if max_stat ** 2 < p else p

            if max_stat > t_crit and max_idx not in outlier_indices:
                # Map back to original index
                original_idx = max_idx
                anomalies.append(AnomalyPoint(
                    index=original_idx,
                    value=float(data[original_idx]) if original_idx < n else 0.0,
                    expected=float(seasonal_medians[original_idx % period]),
                    severity=float(max_stat / t_crit) if t_crit > 0 else 0,
                    method="seasonal_esd",
                ))
                outlier_indices.add(max_idx)
                remaining = np.delete(remaining, max_idx)
            else:
                break

        return AnomalyResult(
            points=anomalies,
            method=AnomalyMethod.SEASONAL_ESD,
            n_anomalies=len(anomalies),
            anomaly_rate=len(anomalies) / n,
        )

    def adaptive_threshold(
        self,
        data: NDArray,
        window_size: int = 48,
        n_sigma: float = 3.0,
        method: str = "mad",
    ) -> AnomalyResult:
        """Adaptive threshold anomaly detection."""
        n = len(data)
        anomalies = []
        scores = np.zeros(n)

        for i in range(window_size, n):
            window = data[i - window_size:i]
            if method == "mad":
                median = np.median(window)
                mad = np.median(np.abs(window - median))
                score = 0.6745 * abs(data[i] - median) / mad if mad > 0 else 0
            else:
                mean = np.mean(window)
                std = np.std(window, ddof=1)
                score = abs(data[i] - mean) / std if std > 0 else 0

            scores[i] = score
            if score > n_sigma:
                anomalies.append(AnomalyPoint(
                    index=i, value=float(data[i]),
                    expected=float(np.median(window)),
                    severity=float(score / n_sigma),
                    method="adaptive_threshold",
                ))

        return AnomalyResult(
            points=anomalies,
            method=AnomalyMethod.ADAPTIVE_THRESHOLD,
            n_anomalies=len(anomalies),
            anomaly_rate=len(anomalies) / n,
            threshold=n_sigma,
            scores=scores,
        )


# ---------------------------------------------------------------------------
# Change Point Detector
# ---------------------------------------------------------------------------

class ChangePointDetector:
    """Detect change points in time series data."""

    def cusum(
        self,
        data: NDArray,
        threshold: float = 5.0,
        drift: float = 0.5,
    ) -> CPDResult:
        """CUSUM (Cumulative Sum Control) change point detection."""
        n = len(data)
        mean = np.mean(data)
        std = np.std(data, ddof=1)
        target = mean / std if std > 0 else 0

        s_pos = np.zeros(n)
        s_neg = np.zeros(n)
        change_points = []

        for i in range(1, n):
            normalized = (data[i] - mean) / std if std > 0 else 0
            s_pos[i] = max(0, s_pos[i - 1] + normalized - drift)
            s_neg[i] = max(0, s_neg[i - 1] - normalized - drift)

            if s_pos[i] > threshold or s_neg[i] > threshold:
                change_points.append(ChangePoint(
                    index=i, confidence=min(s_pos[i], s_neg[i]) / threshold,
                    method="cusum",
                ))
                s_pos[i] = 0
                s_neg[i] = 0

        return CPDResult(
            change_points=change_points,
            method=CPDMethod.CUSUM,
            n_segments=len(change_points) + 1,
        )

    def bayesian_online(
        self,
        data: NDArray,
        hazard_rate: float = 1 / 200,
        observation_likelihood: str = "student_t",
    ) -> CPDResult:
        """Bayesian Online Change Point Detection (Adams & MacKay 2007)."""
        n = len(data)
        run_lengths = np.zeros(n, dtype=int)
        log_probs = np.zeros(n)
        change_points = []

        # Run length distribution
        max_run = min(n, 500)
        log_R = np.zeros((n, max_run + 1))
        log_R[0, 0] = 0  # R_0 = 1

        for t in range(1, n):
            # Predictive probabilities for each run length
            predictive = np.zeros(max_run + 1)
            for r in range(min(t, max_run)):
                # Student-t predictive (simplified)
                window = data[t - r:t]
                mu = np.mean(window)
                var = np.var(window, ddof=1) if len(window) > 1 else 1.0
                nu = max(len(window) - 1, 1)
                scale = var * (1 + 1 / len(window))
                x = data[t]
                # Student-t PDF approximation
                z = (x - mu) / np.sqrt(scale) if scale > 0 else 0
                predictive[r] = -0.5 * (nu + 1) * np.log(1 + z ** 2 / nu)

            # Growth probabilities
            log_growth = log_R[t - 1, :max_run] + predictive[:max_run]

            # Change point probability
            H = hazard_rate
            log_cp = np.log(H) + self._log_sum_exp(log_R[t - 1, :max_run])

            # Update run length distribution
            log_R[t, 1:max_run + 1] = log_growth
            log_R[t, 0] = log_cp

            # Normalize
            max_log = np.max(log_R[t, :max_run + 1])
            log_R[t, :max_run + 1] -= max_log

            # Detect change point
            if log_R[t, 0] > np.max(log_R[t, 1:max_run + 1]):
                change_points.append(ChangePoint(
                    index=t,
                    confidence=float(np.exp(log_R[t, 0])),
                    method="bayesian_online",
                ))

            run_lengths[t] = np.argmax(log_R[t, :max_run + 1])
            log_probs[t] = max_log

        return CPDResult(
            change_points=change_points,
            method=CPDMethod.BAYESIAN_ONLINE,
            n_segments=len(change_points) + 1,
            run_lengths=run_lengths,
            log_probabilities=log_probs,
        )

    def pelt(
        self,
        data: NDArray,
        cost_function: str = "rbf",
        penalty: Union[str, float] = "auto",
    ) -> CPDResult:
        """PELT (Pruned Exact Linear Time) change point detection."""
        n = len(data)

        if isinstance(penalty, str) and penalty == "auto":
            penalty = 2 * np.log(n)

        # Cost function: RBF kernel cost
        def segment_cost(start: int, end: int) -> float:
            segment = data[start:end]
            if len(segment) < 2:
                return 0
            return float(np.var(segment, ddof=1) * len(segment))

        # Dynamic programming with pruning
        F = np.full(n + 1, np.inf)
        F[0] = -penalty
        cp_list = [[] for _ in range(n + 1)]

        for t in range(1, n + 1):
            candidates = list(range(max(0, t - 200), t))  # Limit search window
            costs = [F[s] + segment_cost(s, t) + penalty for s in candidates]
            best_idx = np.argmin(costs)
            F[t] = costs[best_idx]
            s = candidates[best_idx]
            cp_list[t] = cp_list[s] + [s] if s > 0 else []

        # Extract change points
        change_point_indices = [cp for cp in cp_list[n] if cp > 0]
        change_points = [ChangePoint(index=cp, method="pelt") for cp in change_point_indices]

        return CPDResult(
            change_points=change_points,
            method=CPDMethod.PELT,
            n_segments=len(change_point_indices) + 1,
        )

    def _log_sum_exp(self, log_values: NDArray) -> float:
        max_val = np.max(log_values)
        if np.isinf(max_val):
            return float("-inf")
        return float(max_val + np.log(np.sum(np.exp(log_values - max_val))))


# ---------------------------------------------------------------------------
# Spectral Analyzer
# ---------------------------------------------------------------------------

class SpectralAnalyzer:
    """Spectral and frequency domain analysis."""

    def power_spectral_density(
        self,
        data: NDArray,
        fs: float = 1.0,
        method: str = "welch",
        nperseg: int = 256,
    ) -> PSDResult:
        """Estimate power spectral density."""
        n = len(data)

        if method == "fft":
            fft_vals = np.fft.rfft(data - np.mean(data))
            power = np.abs(fft_vals) ** 2 / n
            frequencies = np.fft.rfftfreq(n, d=1 / fs)
        elif method == "welch":
            # Simplified Welch's method
            n_segments = max(1, n // nperseg)
            segment_size = n // n_segments
            power = np.zeros(nperseg // 2 + 1)
            for i in range(n_segments):
                segment = data[i * segment_size:(i + 1) * segment_size]
                if len(segment) < nperseg:
                    segment = np.pad(segment, (0, nperseg - len(segment)))
                fft_vals = np.fft.rfft(segment - np.mean(segment))
                power += np.abs(fft_vals) ** 2 / segment_size
            power /= n_segments
            frequencies = np.fft.rfftfreq(nperseg, d=1 / fs)
        else:  # periodogram
            fft_vals = np.fft.rfft(data - np.mean(data))
            power = np.abs(fft_vals) ** 2 / n
            frequencies = np.fft.rfftfreq(n, d=1 / fs)

        total_power = float(np.sum(power))

        return PSDResult(
            frequencies=frequencies[:len(power)],
            power=power,
            method=SpectralMethod(method),
            sampling_rate=fs,
            total_power=total_power,
        )

    def autocorrelation(
        self,
        data: NDArray,
        max_lag: Optional[int] = None,
        standardized: bool = True,
    ) -> Tuple[NDArray, NDArray]:
        """Compute autocorrelation function."""
        n = len(data)
        if max_lag is None:
            max_lag = min(n // 2, 50)

        mean = np.mean(data)
        var = np.var(data, ddof=1)
        centered = data - mean

        acf = np.zeros(max_lag + 1)
        for lag in range(max_lag + 1):
            if var > 0:
                acf[lag] = np.sum(centered[:n - lag] * centered[lag:]) / ((n - lag) * var)
            else:
                acf[lag] = 0

        lags = np.arange(max_lag + 1)
        return lags, acf

    def partial_autocorrelation(
        self,
        data: NDArray,
        max_lag: Optional[int] = None,
    ) -> Tuple[NDArray, NDArray]:
        """Compute partial autocorrelation function via Durbin-Levinson."""
        n = len(data)
        if max_lag is None:
            max_lag = min(n // 2, 30)

        _, acf = self.autocorrelation(data, max_lag)
        pacf = np.zeros(max_lag + 1)
        pacf[0] = 1.0

        if max_lag >= 1:
            pacf[1] = acf[1]

        phi = np.zeros((max_lag + 1, max_lag + 1))
        phi[1, 1] = acf[1]

        for k in range(2, max_lag + 1):
            num = acf[k] - sum(phi[k - 1, j] * acf[k - j] for j in range(1, k))
            den = 1 - sum(phi[k - 1, j] * acf[j] for j in range(1, k))

            if abs(den) > 1e-10:
                phi[k, k] = num / den
                pacf[k] = phi[k, k]

                for j in range(1, k):
                    phi[k, j] = phi[k - 1, j] - phi[k, k] * phi[k - 1, k - j]

        lags = np.arange(max_lag + 1)
        return lags, pacf

    def continuous_wavelet_transform(
        self,
        data: NDArray,
        scales: Optional[NDArray] = None,
        wavelet: str = "morlet",
    ) -> WaveletResult:
        """Continuous Wavelet Transform (CWT)."""
        n = len(data)
        if scales is None:
            scales = np.arange(1, min(128, n // 2))

        # Mother wavelet (Morlet approximation)
        if wavelet == "morlet":
            omega0 = 6.0
        else:
            omega0 = 5.0

        coefficients = np.zeros((len(scales), n))

        for i, scale in enumerate(scales):
            # Convolution with scaled wavelet
            wavelet_len = min(8 * scale, n)
            t = np.arange(-wavelet_len, wavelet_len) / scale

            if wavelet == "morlet":
                psi = np.pi ** (-0.25) * np.exp(1j * omega0 * t) * np.exp(-t ** 2 / 2)
            else:
                psi = np.pi ** (-0.25) * (1 - t ** 2) * np.exp(-t ** 2 / 2)

            # Pad signal
            padded = np.pad(data, (wavelet_len, wavelet_len), mode="edge")
            conv = np.convolve(padded, psi.real, mode="valid")[:n]
            coefficients[i, :] = np.abs(conv) / np.sqrt(scale)

        # Frequency mapping
        frequencies = omega0 / (2 * np.pi * scales)

        # Power spectrum
        power = coefficients ** 2

        return WaveletResult(
            coefficients=coefficients,
            scales=scales,
            frequencies=frequencies,
            power_spectrum=power,
            wavelet_name=wavelet,
        )


# ---------------------------------------------------------------------------
# Kalman Filter
# ---------------------------------------------------------------------------

class KalmanFilter:
    """Kalman filter for linear Gaussian state-space models."""

    def __init__(
        self,
        transition_matrix: Optional[NDArray] = None,
        observation_matrix: Optional[NDArray] = None,
        process_noise: Optional[NDArray] = None,
        observation_noise: Optional[NDArray] = None,
        initial_state: Optional[NDArray] = None,
        initial_covariance: Optional[NDArray] = None,
    ):
        self.F = transition_matrix  # State transition
        self.H = observation_matrix  # Observation model
        self.Q = process_noise  # Process noise covariance
        self.R = observation_noise  # Observation noise covariance
        self.x0 = initial_state  # Initial state mean
        self.P0 = initial_covariance  # Initial state covariance

    def filter(self, observations: NDArray) -> KalmanResult:
        """Run Kalman filter on observations."""
        n_obs = len(observations)
        dim_state = len(self.x0) if self.x0 is not None else 1
        dim_obs = 1

        # Initialize
        x = self.x0.copy() if self.x0 is not None else np.zeros(dim_state)
        P = self.P0.copy() if self.P0 is not None else np.eye(dim_state)

        filtered = np.zeros((n_obs, dim_state))
        predicted = np.zeros((n_obs, dim_state))
        innovations = np.zeros(n_obs)
        innovation_vars = np.zeros(n_obs)

        for t in range(n_obs):
            # Predict
            if self.F is not None:
                x_pred = self.F @ x
                P_pred = self.F @ P @ self.F.T + self.Q
            else:
                x_pred = x
                P_pred = P + self.Q

            predicted[t] = x_pred

            # Update
            if self.H is not None:
                y_pred = self.H @ x_pred
                innovation = observations[t] - y_pred
                S = self.H @ P_pred @ self.H.T + self.R
                K = P_pred @ self.H.T @ np.linalg.inv(S) if isinstance(S, np.ndarray) and S.ndim > 0 else P_pred @ self.H.T / (S if np.isscalar(S) else S[0, 0])

                x = x_pred + K * innovation
                P = (np.eye(dim_state) - K @ self.H) @ P_pred
            else:
                innovation = observations[t] - x_pred[0]
                S = P_pred[0, 0] + self.R[0, 0] if self.R is not None else P_pred[0, 0]
                K = P_pred[:, 0] / S

                x = x_pred + K * innovation
                P = P_pred - np.outer(K, K) * S

            filtered[t] = x
            innovations[t] = float(innovation)
            innovation_vars[t] = float(S) if np.isscalar(S) else float(S[0, 0])

        # Smoothed states (simplified: just use filtered)
        smoothed = filtered.copy()

        # Log likelihood
        log_lik = -0.5 * n_obs * np.log(2 * np.pi) - 0.5 * np.sum(
            np.log(innovation_vars + 1e-10) + innovations ** 2 / (innovation_vars + 1e-10)
        )

        return KalmanResult(
            filtered_state=filtered,
            predicted_state=predicted,
            smoothed_state=smoothed,
            filtered_covariance=P,
            predicted_covariance=P_pred if 'P_pred' in dir() else P,
            log_likelihood=float(log_lik),
            innovations=innovations,
            innovation_variances=innovation_vars,
        )


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate time series analysis capabilities."""
    print("=" * 70)
    print("Time Series Analysis Framework - Demo")
    print("=" * 70)

    rng = np.random.default_rng(42)
    n = 200

    # Generate synthetic time series with trend, seasonality, and anomalies
    t = np.arange(n, dtype=float)
    trend = 0.05 * t
    seasonal = 5 * np.sin(2 * np.pi * t / 24) + 2 * np.cos(2 * np.pi * t / 7)
    noise = rng.normal(0, 1, n)
    data = 50 + trend + seasonal + noise

    # Inject anomalies
    data[50] += 15
    data[100] -= 12
    data[150] += 18

    # --- 1. Decomposition ---
    print("\n--- Time Series Decomposition ---")
    decomposer = TimeSeriesDecomposer()
    result = decomposer.stl_decompose(data, period=24, seasonal_window=7)
    print(f"  Method:          STL")
    print(f"  Trend strength:  {result.trend_strength:.3f}")
    print(f"  Seasonal strength: {result.seasonal_strength:.3f}")
    print(f"  Residual std:    {result.remainder_std:.4f}")

    # --- 2. ARIMA Forecasting ---
    print("\n--- ARIMA Forecasting ---")
    forecaster = ARIMAForecaster()
    train = data[:160]
    test = data[160:]

    model = forecaster.auto_arima(train, seasonal=True, m=24, max_p=3, max_q=3)
    forecast = model.forecast(steps=40, alpha=0.05)
    print(f"  Order:           {model.order}")
    print(f"  Seasonal order:  {model.seasonal_order}")
    print(f"  AIC:             {model.aic:.2f}")
    print(f"  BIC:             {model.bic:.2f}")
    print(f"  Forecast[:5]:    {forecast.values[:5]}")
    if forecast.conf_int:
        print(f"  95% CI[0]:       [{forecast.conf_int[0][0]:.2f}, {forecast.conf_int[1][0]:.2f}]")

    # Model diagnostics
    diag = model.diagnostics()
    print(f"  Residual mean:   {diag.residuals_mean:.6f}")
    print(f"  Ljung-Box p:     {diag.ljung_box_pvalue:.4f}")

    # --- 3. Anomaly Detection ---
    print("\n--- Anomaly Detection ---")
    detector = AnomalyDetector()

    # Z-score
    z_result = detector.z_score(data, threshold=3.0, window=24)
    print(f"  Z-score anomalies: {z_result.n_anomalies} ({z_result.anomaly_rate:.2%})")
    for a in z_result.points[:3]:
        print(f"    idx={a.index}: value={a.value:.1f}, expected={a.expected:.1f}, severity={a.severity:.2f}")

    # Seasonal ESD
    sesd_result = detector.seasonal_esd(data, period=24, k=5)
    print(f"  S-ESD anomalies:   {sesd_result.n_anomalies}")
    for a in sesd_result.points[:3]:
        print(f"    idx={a.index}: value={a.value:.1f}, severity={a.severity:.2f}")

    # --- 4. Change Point Detection ---
    print("\n--- Change Point Detection ---")
    cpd = ChangePointDetector()

    # CUSUM
    cusum_result = cpd.cusum(data, threshold=5.0, drift=0.5)
    print(f"  CUSUM change points: {cusum_result.change_point_indices}")

    # PELT
    pelt_result = cpd.pelt(data, penalty="auto")
    print(f"  PELT change points:  {pelt_result.change_point_indices}")
    print(f"  PELT segments:       {pelt_result.n_segments}")

    # --- 5. Spectral Analysis ---
    print("\n--- Spectral Analysis ---")
    analyzer = SpectralAnalyzer()

    psd = analyzer.power_spectral_density(data, fs=1.0, method="welch", nperseg=64)
    dominant = psd.dominant_frequencies(n_top=3)
    print(f"  Top frequencies:")
    for freq in dominant:
        print(f"    {freq.frequency:.4f} Hz (period={freq.period:.1f}), power={freq.power:.2f}")

    lags, acf = analyzer.autocorrelation(data, max_lag=30)
    print(f"  ACF at lag 1:  {acf[1]:.4f}")
    print(f"  ACF at lag 24: {acf[24]:.4f}")

    lags, pacf = analyzer.partial_autocorrelation(data, max_lag=30)
    print(f"  PACF at lag 1:  {pacf[1]:.4f}")
    print(f"  PACF at lag 24: {pacf[24]:.4f}")

    # Wavelet
    wavelet = analyzer.continuous_wavelet_transform(
        data[:100], scales=np.arange(1, 32), wavelet="morlet"
    )
    max_scale_idx = np.argmax(np.abs(wavelet.coefficients).max(axis=1))
    print(f"  Wavelet max energy scale: {wavelet.scales[max_scale_idx]} "
          f"(freq={wavelet.frequencies[max_scale_idx]:.4f})")

    # --- 6. Kalman Filter ---
    print("\n--- Kalman Filter ---")
    # Simple local level model
    kf = KalmanFilter(
        transition_matrix=np.array([[1.0]]),
        observation_matrix=np.array([[1.0]]),
        process_noise=np.array([[0.1]]),
        observation_noise=np.array([[1.0]]),
        initial_state=np.array([data[0]]),
        initial_covariance=np.array([[1.0]]),
    )
    kalman_result = kf.filter(data)
    print(f"  Filtered state range: [{kalman_result.filtered_state.min():.2f}, {kalman_result.filtered_state.max():.2f}]")
    print(f"  Log-likelihood:       {kalman_result.log_likelihood:.2f}")
    print(f"  Innovation std:       {np.std(kalman_result.innovations):.4f}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()