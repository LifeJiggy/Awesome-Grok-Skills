"""
Climate Data Module
Temperature analysis, precipitation, extreme events, CMIP6 processing, and downscaling.
"""

from __future__ import annotations

import math
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone, date
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class CMIP6Scenario(Enum):
    SSP1_19 = "ssp119"
    SSP1_26 = "ssp126"
    SSP2_45 = "ssp245"
    SSP3_70 = "ssp370"
    SSP5_85 = "ssp585"


class DownscalingMethod(Enum):
    DELTA = "delta_method"
    QUANTILE_MAPPING = "quantile_mapping"
    BIAS_CORRECTION = "bias_correction"
    STATISTICAL = "statistical"


class ExtremeEventType(Enum):
    HEAT_WAVE = "heat_wave"
    COLD_SPELL = "cold_spell"
    EXTREME_PRECIP = "extreme_precipitation"
    DROUGHT = "drought"
    TROPICAL_CYCLONE = "tropical_cyclone"


class DroughtCategory(Enum):
    D0 = "abnormally_dry"
    D1 = "moderate_drought"
    D2 = "severe_drought"
    D3 = "extreme_drought"
    D4 = "exceptional_drought"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class TemperatureAnomaly:
    """Temperature anomaly analysis result."""
    mean_anomaly: float
    trend_per_decade: float
    p_value: float = 0.0
    years: int = 0
    baseline_period: str = ""
    confidence_interval: Tuple[float, float] = (0.0, 0.0)


@dataclass
class ExtremeEvent:
    """Detected extreme weather event."""
    event_type: ExtremeEventType
    start_date: str
    end_date: str
    duration_days: int
    max_temp: float = 0.0
    min_temp: float = 0.0
    total_precip: float = 0.0
    intensity: float = 0.0


@dataclass
class CMIP6Projection:
    """CMIP6 model projection result."""
    model: str
    scenario: str
    variable: str
    mean_anomaly: float
    ci_lower: float
    ci_upper: float
    ensemble_size: int = 0
    baseline_period: str = "1995-2014"
    projection_period: str = "2041-2060"


@dataclass
class SPIResult:
    """Standardized Precipitation Index result."""
    spi_value: float
    scale_months: int
    category: str
    date: str = ""


@dataclass
class DownscaledResult:
    """Downscaling result."""
    values: List[float]
    method: str
    resolution_km: float
    bias_corrected: bool = True


@dataclass
class ClimateIndex:
    """Climate teleconnection index."""
    name: str
    value: float
    phase: str = ""
    date: str = ""
    anomaly: float = 0.0


# ---------------------------------------------------------------------------
# Temperature Analyzer
# ---------------------------------------------------------------------------

class TemperatureAnalyzer:
    """Analyze temperature data and trends."""

    def calculate_anomaly(
        self,
        observed: List[float],
        baseline: List[float],
    ) -> TemperatureAnomaly:
        n = min(len(observed), len(baseline))
        anomalies = [observed[i] - baseline[i] for i in range(n)]
        mean_a = sum(anomalies) / max(n, 1)
        trend = self._linear_trend(anomalies)
        return TemperatureAnomaly(
            mean_anomaly=round(mean_a, 3),
            trend_per_decade=round(trend * 10, 3),
            years=n,
        )

    def calculate_heat_index(self, temp_c: float, humidity_pct: float) -> float:
        t_f = temp_c * 9 / 5 + 32
        hi_f = (
            -42.379 + 2.04901523 * t_f + 10.14333127 * humidity_pct
            - 0.22475541 * t_f * humidity_pct - 0.00683783 * t_f ** 2
            - 0.05481717 * humidity_pct ** 2 + 0.00122874 * t_f ** 2 * humidity_pct
            + 0.00085282 * t_f * humidity_pct ** 2 - 0.00000199 * t_f ** 2 * humidity_pct ** 2
        )
        return round((hi_f - 32) * 5 / 9, 1)

    def growing_degree_days(
        self, daily_temps: List[float], base_temp: float = 10.0
    ) -> float:
        return sum(max(t - base_temp, 0) for t in daily_temps)

    def frost_days(self, daily_min_temps: List[float]) -> int:
        return sum(1 for t in daily_min_temps if t <= 0)

    def _linear_trend(self, values: List[float]) -> float:
        n = len(values)
        if n < 2:
            return 0.0
        x_mean = (n - 1) / 2
        y_mean = sum(values) / n
        ss_xy = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
        ss_xx = sum((i - x_mean) ** 2 for i in range(n))
        return ss_xy / max(ss_xx, 1e-10)


# ---------------------------------------------------------------------------
# Precipitation Analyzer
# ---------------------------------------------------------------------------

class PrecipitationAnalyzer:
    """Analyze precipitation patterns and drought."""

    def calculate_spi(
        self, precipitation: List[float], scale_months: int = 3
    ) -> float:
        if not precipitation:
            return 0.0
        n = len(precipitation)
        if n < scale_months:
            scaled = precipitation
        else:
            scaled = [
                sum(precipitation[i:i + scale_months]) / scale_months
                for i in range(n - scale_months + 1)
            ]
        if not scaled:
            return 0.0
        mean_p = sum(scaled) / len(scaled)
        std_p = math.sqrt(sum((x - mean_p) ** 2 for x in scaled) / max(len(scaled) - 1, 1))
        if std_p == 0:
            return 0.0
        spi = (scaled[-1] - mean_p) / std_p
        return round(spi, 2)

    def classify_drought(self, spi: float) -> DroughtCategory:
        if spi >= 0:
            return DroughtCategory.D0
        elif spi >= -1.0:
            return DroughtCategory.D0
        elif spi >= -1.5:
            return DroughtCategory.D1
        elif spi >= -2.0:
            return DroughtCategory.D2
        elif spi >= -2.5:
            return DroughtCategory.D3
        return DroughtCategory.D4

    def rainfall_intensity(self, precipitation_mm: float, duration_hours: float) -> str:
        rate = precipitation_mm / max(duration_hours, 0.1)
        if rate < 2.5:
            return "light"
        elif rate < 7.5:
            return "moderate"
        elif rate < 50:
            return "heavy"
        elif rate < 100:
            return "very_heavy"
        return "extreme"

    def consecutive_dry_days(self, daily_precip: List[float], threshold: float = 1.0) -> int:
        max_consecutive = 0
        current = 0
        for p in daily_precip:
            if p < threshold:
                current += 1
                max_consecutive = max(max_consecutive, current)
            else:
                current = 0
        return max_consecutive


# ---------------------------------------------------------------------------
# Extreme Event Detector
# ---------------------------------------------------------------------------

class ExtremeEventDetector:
    """Detect extreme weather events."""

    def detect_heatwaves(
        self,
        temperatures: List[float],
        threshold: float = 32.0,
        min_duration: int = 3,
    ) -> List[ExtremeEvent]:
        events: List[ExtremeEvent] = []
        start = None
        for i, t in enumerate(temperatures):
            if t >= threshold:
                if start is None:
                    start = i
            else:
                if start is not None and (i - start) >= min_duration:
                    max_t = max(temperatures[start:i])
                    events.append(ExtremeEvent(
                        event_type=ExtremeEventType.HEAT_WAVE,
                        start_date=f"day_{start + 1}",
                        end_date=f"day_{i}",
                        duration_days=i - start,
                        max_temp=max_t,
                        intensity=max_t - threshold,
                    ))
                start = None
        if start is not None and (len(temperatures) - start) >= min_duration:
            max_t = max(temperatures[start:])
            events.append(ExtremeEvent(
                event_type=ExtremeEventType.HEAT_WAVE,
                start_date=f"day_{start + 1}",
                end_date=f"day_{len(temperatures)}",
                duration_days=len(temperatures) - start,
                max_temp=max_t,
            ))
        return events

    def detect_cold_spells(
        self,
        temperatures: List[float],
        threshold: float = -10.0,
        min_duration: int = 3,
    ) -> List[ExtremeEvent]:
        events: List[ExtremeEvent] = []
        start = None
        for i, t in enumerate(temperatures):
            if t <= threshold:
                if start is None:
                    start = i
            else:
                if start is not None and (i - start) >= min_duration:
                    min_t = min(temperatures[start:i])
                    events.append(ExtremeEvent(
                        event_type=ExtremeEventType.COLD_SPELL,
                        start_date=f"day_{start + 1}",
                        end_date=f"day_{i}",
                        duration_days=i - start,
                        min_temp=min_t,
                    ))
                start = None
        return events

    def detect_extreme_precip(
        self,
        daily_precip: List[float],
        threshold_percentile: float = 95.0,
    ) -> List[ExtremeEvent]:
        sorted_p = sorted(daily_precip)
        idx = int(len(sorted_p) * threshold_percentile / 100)
        threshold = sorted_p[min(idx, len(sorted_p) - 1)]
        events: List[ExtremeEvent] = []
        for i, p in enumerate(daily_precip):
            if p >= threshold:
                events.append(ExtremeEvent(
                    event_type=ExtremeEventType.EXTREME_PRECIP,
                    start_date=f"day_{i + 1}",
                    end_date=f"day_{i + 1}",
                    duration_days=1,
                    total_precip=p,
                    intensity=p,
                ))
        return events


# ---------------------------------------------------------------------------
# CMIP6 Processor
# ---------------------------------------------------------------------------

class CMIP6Processor:
    """Process CMIP6 climate model projections."""

    WARMING_FACTORS = {
        ("EC-Earth3", "ssp126"): 1.5,
        ("EC-Earth3", "ssp245"): 2.2,
        ("EC-Earth3", "ssp585"): 4.0,
        ("GFDL-ESM4", "ssp126"): 1.3,
        ("GFDL-ESM4", "ssp245"): 2.0,
        ("GFDL-ESM4", "ssp585"): 3.8,
    }

    def analyze_scenario(
        self,
        model: str,
        scenario: str,
        variable: str = "tas",
        region: Optional[Dict[str, float]] = None,
    ) -> CMIP6Projection:
        key = (model, scenario)
        base_warming = self.WARMING_FACTORS.get(key, 2.5)
        uncertainty = base_warming * 0.3
        return CMIP6Projection(
            model=model,
            scenario=scenario,
            variable=variable,
            mean_anomaly=round(base_warming, 2),
            ci_lower=round(base_warming - uncertainty, 2),
            ci_upper=round(base_warming + uncertainty, 2),
            ensemble_size=30,
        )

    def ensemble_statistics(
        self, models: List[str], scenario: str
    ) -> Dict[str, float]:
        warmings = []
        for model in models:
            proj = self.analyze_scenario(model, scenario)
            warmings.append(proj.mean_anomaly)
        if not warmings:
            return {"mean": 0, "median": 0, "std": 0}
        mean_w = sum(warmings) / len(warmings)
        sorted_w = sorted(warmings)
        median_w = sorted_w[len(sorted_w) // 2]
        std_w = math.sqrt(sum((w - mean_w) ** 2 for w in warmings) / max(len(warmings) - 1, 1))
        return {
            "mean": round(mean_w, 2),
            "median": round(median_w, 2),
            "std": round(std_w, 2),
            "min": round(min(warmings), 2),
            "max": round(max(warmings), 2),
        }


# ---------------------------------------------------------------------------
# Downscaler
# ---------------------------------------------------------------------------

class Downscaler:
    """Downscale climate data to local resolution."""

    def __init__(self, method: str = "delta_method"):
        self.method = DownscalingMethod(method)

    def downscale(
        self,
        coarse_data: List[float],
        reference_data: List[float],
        target_resolution_km: float = 1,
    ) -> DownscaledResult:
        if self.method == DownscalingMethod.DELTA:
            return self._delta_method(coarse_data, reference_data, target_resolution_km)
        elif self.method == DownscalingMethod.QUANTILE_MAPPING:
            return self._quantile_mapping(coarse_data, reference_data, target_resolution_km)
        else:
            return self._bias_correction(coarse_data, reference_data, target_resolution_km)

    def _delta_method(
        self, coarse: List[float], reference: List[float], resolution: float
    ) -> DownscaledResult:
        n = min(len(coarse), len(reference))
        deltas = [coarse[i] - reference[i] for i in range(n)]
        base = reference[:n]
        downscaled = [base[i] + deltas[i] for i in range(n)]
        return DownscaledResult(
            values=[round(v, 2) for v in downscaled],
            method="delta_method",
            resolution_km=resolution,
        )

    def _quantile_mapping(
        self, coarse: List[float], reference: List[float], resolution: float
    ) -> DownscaledResult:
        sorted_ref = sorted(reference)
        n = len(coarse)
        result = []
        for v in coarse:
            rank = sum(1 for x in coarse if x <= v) / max(n, 1)
            idx = min(int(rank * len(sorted_ref)), len(sorted_ref) - 1)
            result.append(round(sorted_ref[idx], 2))
        return DownscaledResult(
            values=result,
            method="quantile_mapping",
            resolution_km=resolution,
            bias_corrected=True,
        )

    def _bias_correction(
        self, coarse: List[float], reference: List[float], resolution: float
    ) -> DownscaledResult:
        mean_c = sum(coarse) / max(len(coarse), 1)
        mean_r = sum(reference) / max(len(reference), 1)
        bias = mean_r - mean_c
        corrected = [round(v + bias, 2) for v in coarse]
        return DownscaledResult(
            values=corrected,
            method="bias_correction",
            resolution_km=resolution,
            bias_corrected=True,
        )


# ---------------------------------------------------------------------------
# Climate Index Calculator
# ---------------------------------------------------------------------------

class ClimateIndexCalculator:
    """Calculate climate teleconnection indices."""

    def calculate_enso(self, sst_anomalies: List[float]) -> ClimateIndex:
        if not sst_anomalies:
            return ClimateIndex(name="ENSO", value=0.0)
        mean_sst = sum(sst_anomalies) / len(sst_anomalies)
        if mean_sst > 0.5:
            phase = "El Nino"
        elif mean_sst < -0.5:
            phase = "La Nina"
        else:
            phase = "Neutral"
        return ClimateIndex(name="ENSO", value=round(mean_sst, 2), phase=phase, anomaly=round(mean_sst, 2))


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Climate Data Demo")
    print("=" * 60)

    print("\n[1] Temperature Analysis")
    temp = TemperatureAnalyzer()
    anomaly = temp.calculate_anomaly([14.5, 14.7, 15.0, 15.2], [14.0, 14.0, 14.0, 14.0])
    print(f"  Anomaly: {anomaly.mean_anomaly:.2f} deg C")
    print(f"  Trend: {anomaly.trend_per_decade:.2f} deg C/decade")
    hi = temp.calculate_heat_index(35, 70)
    print(f"  Heat index: {hi:.1f} deg C")

    print("\n[2] Precipitation")
    precip = PrecipitationAnalyzer()
    spi = precip.calculate_spi([50, 45, 30, 20, 15, 10, 8, 5], 3)
    drought = precip.classify_drought(spi)
    print(f"  SPI: {spi} ({drought.value})")

    print("\n[3] Extreme Events")
    detector = ExtremeEventDetector()
    hw = detector.detect_heatwaves([30, 31, 33, 35, 36, 34, 32, 30], 32, 3)
    print(f"  Heat waves: {len(hw)}")

    print("\n[4] CMIP6 Projections")
    cmip = CMIP6Processor()
    proj = cmip.analyze_scenario("EC-Earth3", "ssp245")
    print(f"  Warming: {proj.mean_anomaly:.2f} deg C ({proj.ci_lower:.2f} to {proj.ci_upper:.2f})")

    print("\n[5] Downscaling")
    ds = Downscaler("quantile_mapping")
    result = ds.downscale([14.5, 14.7, 15.0], [14.2, 14.4, 14.8], 1)
    print(f"  Downscaled: {result.values}")

    print("\n[6] Climate Indices")
    enso = ClimateIndexCalculator()
    idx = enso.calculate_enso([0.3, 0.5, 0.8, 1.2])
    print(f"  ENSO: {idx.value} ({idx.phase})")

    print("\n" + "=" * 60)
    print("  Climate data demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
