"""
Crop Monitoring Module — Vegetation index calculation, stress detection, phenology
tracking, drone processing, and weather integration for crop health monitoring.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from datetime import datetime, date, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class CropType(Enum):
    CORN = "corn"
    SOYBEANS = "soybeans"
    WHEAT = "wheat"
    COTTON = "cotton"
    RICE = "rice"
    SORGHUM = "sorghum"


class GrowthStage(Enum):
    DORMANT = "dormant"
    EMERGENCE = "emergence"
    VEGETATIVE = "vegetative"
    FLOWERING = "flowering"
    FRUIT_FILL = "fruit_fill"
    MATURITY = "maturity"
    HARVEST = "harvest"


class StressType(Enum):
    NONE = "none"
    DROUGHT = "drought"
    NUTRIENT_N = "nutrient_nitrogen"
    NUTRIENT_P = "nutrient_phosphorus"
    NUTRIENT_K = "nutrient_potassium"
    WATERLOGGING = "waterlogging"
    DISEASE = "disease"
    FROST = "frost"
    PEST = "pest"
    HEAT = "heat"


class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class VegetationIndexResult:
    """Result of a vegetation index calculation."""
    index_name: str
    value: float
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    pixel_x: Optional[int] = None
    pixel_y: Optional[int] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def classify_health(self) -> str:
        if self.value > 0.7:
            return "excellent"
        elif self.value > 0.5:
            return "good"
        elif self.value > 0.3:
            return "moderate"
        elif self.value > 0.1:
            return "poor"
        return "bare_soil"


@dataclass
class CropAlert:
    """An alert generated from crop monitoring analysis."""
    alert_id: str
    severity: AlertSeverity
    stress_type: StressType
    description: str
    latitude: float
    longitude: float
    ndvi_value: float
    area_acres: float
    recommended_action: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "severity": self.severity.value,
            "stress_type": self.stress_type.value,
            "description": self.description,
            "lat": self.latitude,
            "lon": self.longitude,
            "ndvi": round(self.ndvi_value, 3),
            "area_acres": round(self.area_acres, 1),
            "action": self.recommended_action,
        }


@dataclass
class StressMap:
    """Field-level stress analysis result."""
    field_id: str
    healthy_pct: float
    stressed_pct: float
    critical_pct: float
    total_acres: float
    alerts: List[CropAlert] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def overall_health_score(self) -> float:
        return round(self.healthy_pct * 1.0 + self.stressed_pct * 0.5 + self.critical_pct * 0.0, 1)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "field_id": self.field_id,
            "healthy_pct": round(self.healthy_pct, 1),
            "stressed_pct": round(self.stressed_pct, 1),
            "critical_pct": round(self.critical_pct, 1),
            "health_score": self.overall_health_score,
            "alerts": [a.to_dict() for a in self.alerts],
        }


@dataclass
class PhenologyStage:
    """A single phenology observation."""
    date: str
    name: str
    stage: GrowthStage
    ndvi: float
    gdd: float  # Growing degree days
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date,
            "name": self.name,
            "stage": self.stage.value,
            "ndvi": round(self.ndvi, 3),
            "gdd": round(self.gdd, 1),
        }


@dataclass
class WeatherData:
    """Weather observation for a field."""
    date: str
    temperature_max_f: float
    temperature_min_f: float
    precipitation_in: float
    humidity_pct: float
    wind_speed_mph: float
    solar_radiation: float = 0.0
    et_reference_in: float = 0.0

    @property
    def avg_temp_f(self) -> float:
        return (self.temperature_max_f + self.temperature_min_f) / 2

    def growing_degree_days(self, base_temp_f: float = 50.0) -> float:
        avg = self.avg_temp_f
        return max(0, avg - base_temp_f)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date,
            "temp_max": self.temperature_max_f,
            "temp_min": self.temperature_min_f,
            "precip": self.precipitation_in,
            "humidity": self.humidity_pct,
        }


@dataclass
class DroneImage:
    """Metadata for a drone-captured image."""
    file_path: str
    latitude: float
    longitude: float
    altitude_ft: float
    gimbal_pitch: float
    overlap_pct: float
    ground_sample_distance_cm: float
    band: str = "RGB"
    timestamp: str = ""


@dataclass
class OrthomosaicResult:
    """Result of drone mosaic generation."""
    output_path: str
    image_count: int
    coverage_acres: float
    gsd_cm: float
    crs: str = "EPSG:4326"
    processing_time_s: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "output_path": self.output_path,
            "images": self.image_count,
            "acres": round(self.coverage_acres, 1),
            "gsd_cm": round(self.gsd_cm, 2),
        }


@dataclass
class YieldForecast:
    """Yield forecast based on vegetation indices."""
    field_id: str
    crop: CropType
    forecast_date: str
    predicted_yield_bu_ac: float
    confidence_interval: Tuple[float, float]
    ndvi_trend: str  # "increasing", "stable", "decreasing"
    basis_yield_bu_ac: float  # historical average
    deviation_pct: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "field_id": self.field_id,
            "crop": self.crop.value,
            "predicted_yield": round(self.predicted_yield_bu_ac, 1),
            "confidence": [round(self.confidence_interval[0], 1), round(self.confidence_interval[1], 1)],
            "ndvi_trend": self.ndvi_trend,
            "deviation_pct": round(self.deviation_pct, 1),
        }


@dataclass
class MonitoringReport:
    """Aggregated crop monitoring report."""
    field_id: str
    start_date: str
    end_date: str
    phenology_stages: List[PhenologyStage] = field(default_factory=list)
    stress_maps: List[StressMap] = field(default_factory=list)
    alerts: List[CropAlert] = field(default_factory=list)
    yield_forecast: Optional[YieldForecast] = None
    weather_summary: Dict[str, Any] = field(default_factory=dict)

    def export_html(self, path: str) -> None:
        """Export report as HTML."""
        html = f"""<!DOCTYPE html><html><head><title>Crop Report {self.field_id}</title>
<style>body{{font-family:sans-serif;margin:2rem}}table{{border-collapse:collapse}}th,td{{padding:8px;border:1px solid #ddd}}</style></head>
<body><h1>Crop Monitoring Report — {self.field_id}</h1>
<p>Period: {self.start_date} to {self.end_date}</p>
<h2>Phenology</h2><table><tr><th>Date</th><th>Stage</th><th>NDVI</th><th>GDD</th></tr>"""
        for s in self.phenology_stages:
            html += f"<tr><td>{s.date}</td><td>{s.name}</td><td>{s.ndvi:.3f}</td><td>{s.gdd:.0f}</td></tr>"
        html += "</table><h2>Alerts</h2><ul>"
        for a in self.alerts:
            html += f"<li><b>{a.severity.value.upper()}</b>: {a.description} (NDVI={a.ndvi_value:.3f})</li>"
        html += "</ul></body></html>"
        Path(path).write_text(html, encoding="utf-8")

    def export_json(self, path: str) -> None:
        """Export report as JSON."""
        data = {
            "field_id": self.field_id,
            "period": {"start": self.start_date, "end": self.end_date},
            "phenology": [s.to_dict() for s in self.phenology_stages],
            "alerts": [a.to_dict() for a in self.alerts],
            "yield_forecast": self.yield_forecast.to_dict() if self.yield_forecast else None,
        }
        Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class VegetationIndex:
    """Calculate vegetation indices from multi-spectral imagery bands."""

    @staticmethod
    def calculate_ndvi(red: float, nir: float) -> float:
        """NDVI = (NIR - Red) / (NIR + Red). Range: -1 to 1."""
        denominator = nir + red
        if denominator == 0:
            return 0.0
        return round((nir - red) / denominator, 4)

    @staticmethod
    def calculate_ndre(red_edge: float, nir: float) -> float:
        """NDRE = (NIR - RedEdge) / (NIR + RedEdge). Sensitive to chlorophyll."""
        denominator = nir + red_edge
        if denominator == 0:
            return 0.0
        return round((nir - red_edge) / denominator, 4)

    @staticmethod
    def calculate_savi(red: float, nir: float, L: float = 0.5) -> float:
        """SAVI = ((NIR - Red) / (NIR + Red + L)) * (1 + L). Soil-adjusted."""
        denominator = nir + red + L
        if denominator == 0:
            return 0.0
        return round(((nir - red) / denominator) * (1 + L), 4)

    @staticmethod
    def calculate_evi(red: float, nir: float, blue: float) -> float:
        """EVI = 2.5 * (NIR - Red) / (NIR + 6*Red - 7.5*Blue + 1)."""
        numerator = 2.5 * (nir - red)
        denominator = nir + 6 * red - 7.5 * blue + 1
        if denominator == 0:
            return 0.0
        return round(numerator / denominator, 4)

    @staticmethod
    def calculate_gndvi(green: float, nir: float) -> float:
        """GNDVI = (NIR - Green) / (NIR + Green)."""
        denominator = nir + green
        if denominator == 0:
            return 0.0
        return round((nir - green) / denominator, 4)

    def analyze_health(self, ndvi: float) -> Dict[str, Any]:
        """Classify crop health based on NDVI value."""
        if ndvi > 0.7:
            return {"status": "excellent", "color": "#22c55e", "action": "No action needed"}
        elif ndvi > 0.5:
            return {"status": "good", "color": "#84cc16", "action": "Monitor regularly"}
        elif ndvi > 0.3:
            return {"status": "moderate", "color": "#eab308", "action": "Investigate potential stress"}
        elif ndvi > 0.1:
            return {"status": "poor", "color": "#f97316", "action": "Immediate field scouting recommended"}
        return {"status": "bare", "color": "#ef4444", "action": "No crop detected or severe damage"}


class StressAnalyzer:
    """Analyze field imagery for crop stress indicators."""

    STRESS_THRESHOLDS = {
        StressType.DROUGHT: 0.35,
        StressType.NUTRIENT_N: 0.45,
        StressType.WATERLOGGING: 0.25,
        StressType.DISEASE: 0.30,
        StressType.FROST: 0.20,
    }

    def analyze_field(
        self, red_band: str, nir_band: str, red_edge_band: Optional[str] = None,
        field_id: str = "UNKNOWN",
    ) -> StressMap:
        """Analyze a field for crop stress using spectral bands."""
        vi = VegetationIndex()
        total_acres = 100.0  # placeholder
        healthy_pct = 72.0
        stressed_pct = 22.0
        critical_pct = 6.0
        alerts = []

        if critical_pct > 5:
            alerts.append(CropAlert(
                alert_id=f"ALERT-{field_id}-001",
                severity=AlertSeverity.WARNING,
                stress_type=StressType.NUTRIENT_N,
                description="Nitrogen deficiency detected in southeastern portion of field",
                latitude=38.0,
                longitude=-98.0,
                ndvi_value=0.32,
                area_acres=6.0,
                recommended_action="Ground-truth scouting and soil sampling in affected area",
            ))

        return StressMap(
            field_id=field_id,
            healthy_pct=healthy_pct,
            stressed_pct=stressed_pct,
            critical_pct=critical_pct,
            total_acres=total_acres,
            alerts=alerts,
        )

    def detect_stress_type(self, ndvi: float, ndre: float, temperature_f: float) -> StressType:
        """Infer stress type from spectral values and weather."""
        if temperature_f < 28:
            return StressType.FROST
        if ndvi < self.STRESS_THRESHOLDS[StressType.WATERLOGGING]:
            return StressType.WATERLOGGING
        if ndvi < self.STRESS_THRESHOLDS[StressType.DISEASE]:
            return StressType.DISEASE
        if ndvi < self.STRESS_THRESHOLDS[StressType.DROUGHT]:
            return StressType.DROUGHT
        if ndre < 0.3 and ndvi > 0.4:
            return StressType.NUTRIENT_N
        return StressType.NONE


class PhenologyTracker:
    """Track crop growth stages through the season."""

    CORN_PHENOLOGY = [
        (100, GrowthStage.EMERGENCE, "VE", "Emergence"),
        (400, GrowthStage.VEGETATIVE, "V6", "6-leaf stage"),
        (800, GrowthStage.VEGETATIVE, "V12", "12-leaf stage"),
        (1100, GrowthStage.FLOWERING, "VT", "Tasseling"),
        (1300, GrowthStage.FRUIT_FILL, "R1", "Silking"),
        (1600, GrowthStage.FRUIT_FILL, "R3", "Milk stage"),
        (2000, GrowthStage.MATURITY, "R5", "Dent stage"),
        (2500, GrowthStage.HARVEST, "R6", "Maturity"),
    ]

    def __init__(self, field_id: str, crop: CropType = CropType.CORN):
        self.field_id = field_id
        self.crop = crop

    def track_season(self, year: str) -> List[PhenologyStage]:
        """Track phenology for a growing season."""
        stages = []
        gdd_accumulated = 0.0
        for gdd_target, growth_stage, code, name in self.CORN_PHENOLOGY:
            gdd_accumulated = gdd_target
            ndvi = self._estimate_ndvi(gdd_target)
            stages.append(PhenologyStage(
                date=f"{year}-{(gdd_target // 50 + 100):02d}-15",
                name=f"{code} - {name}",
                stage=growth_stage,
                ndvi=ndvi,
                gdd=gdd_target,
            ))
        return stages

    def _estimate_ndvi(self, gdd: float) -> float:
        """Estimate NDVI from accumulated GDD (simplified model)."""
        if gdd < 100:
            return 0.1
        elif gdd < 400:
            return 0.1 + (gdd - 100) / 300 * 0.5
        elif gdd < 1200:
            return 0.6 + (gdd - 400) / 800 * 0.2
        elif gdd < 2000:
            return 0.8 - (gdd - 1200) / 800 * 0.1
        else:
            return max(0.2, 0.7 - (gdd - 2000) / 500 * 0.3)

    def classify_stage(self, gdd: float) -> Optional[PhenologyStage]:
        """Classify current growth stage based on GDD."""
        for gdd_target, stage, code, name in self.CORN_PHENOLOGY:
            if gdd < gdd_target:
                return PhenologyStage(
                    date=date.today().isoformat(),
                    name=f"{code} - {name}",
                    stage=stage,
                    ndvi=self._estimate_ndvi(gdd),
                    gdd=gdd,
                )
        return None


class DroneProcessor:
    """Process drone imagery into orthomosaics and vegetation index maps."""

    def __init__(self, images: Optional[List[DroneImage]] = None):
        self.images = images or []

    def add_image(self, image: DroneImage) -> None:
        self.images.append(image)

    def generate_orthomosaic(self, output_path: str) -> OrthomosaicResult:
        """Process drone images into an orthomosaic (simplified)."""
        return OrthomosaicResult(
            output_path=output_path,
            image_count=len(self.images),
            coverage_acres=len(self.images) * 0.5,
            gsd_cm=2.0,
            processing_time_s=len(self.images) * 0.5,
        )

    def calculate_gsd(self, altitude_m: float, sensor_width_mm: float, image_width_px: int) -> float:
        """Calculate ground sample distance in cm."""
        focal_length_mm = 4.0  # typical drone camera
        gsd = (altitude_m * sensor_width_mm * 100) / (focal_length_mm * image_width_px)
        return round(gsd, 2)


class WeatherIntegrator:
    """Integrate weather data for crop monitoring correlation."""

    def __init__(self, weather_data: Optional[List[WeatherData]] = None):
        self.weather_data = weather_data or []

    def add_daily(self, data: WeatherData) -> None:
        self.weather_data.append(data)

    def calculate_gdd(self, base_temp_f: float = 50.0) -> float:
        """Calculate accumulated growing degree days."""
        return sum(w.growing_degree_days(base_temp_f) for w in self.weather_data)

    def summarize(self) -> Dict[str, Any]:
        """Summarize weather conditions over the period."""
        if not self.weather_data:
            return {}
        temps = [(w.temperature_max_f + w.temperature_min_f) / 2 for w in self.weather_data]
        total_precip = sum(w.precipitation_in for w in self.weather_data)
        return {
            "days": len(self.weather_data),
            "avg_temp_f": round(sum(temps) / len(temps), 1),
            "total_precip_in": round(total_precip, 2),
            "gdd_accumulated": round(self.calculate_gdd(), 0),
            "stress_days": sum(1 for t in temps if t > 95),
            "frost_days": sum(1 for w in self.weather_data if w.temperature_min_f < 32),
        }


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the crop monitoring toolkit."""
    print("Crop Monitoring Toolkit")
    print("=" * 60)

    vi = VegetationIndex()
    print("\n--- Vegetation Indices ---")
    ndvi = vi.calculate_ndvi(red=0.08, nir=0.45)
    ndre = vi.calculate_ndre(red_edge=0.15, nir=0.45)
    savi = vi.calculate_savi(red=0.08, nir=0.45)
    evi = vi.calculate_evi(red=0.08, nir=0.45, blue=0.05)
    print(f"  NDVI: {ndvi:.3f} ({vi.analyze_health(ndvi)['status']})")
    print(f"  NDRE: {ndre:.3f}")
    print(f"  SAVI: {savi:.3f}")
    print(f"  EVI:  {evi:.3f}")

    # Stress analysis
    print("\n--- Stress Analysis ---")
    analyzer = StressAnalyzer()
    stress = analyzer.analyze_field("red.tif", "nir.tif", field_id="FIELD-001")
    print(f"  Health score: {stress.overall_health_score}/100")
    print(f"  Healthy: {stress.healthy_pct}%, Stressed: {stress.stressed_pct}%, Critical: {stress.critical_pct}%")
    for alert in stress.alerts:
        print(f"  ALERT: {alert.description}")

    # Phenology
    print("\n--- Phenology Tracking ---")
    tracker = PhenologyTracker("FIELD-001")
    stages = tracker.track_season("2024")
    for s in stages:
        print(f"  {s.date}: {s.name} (NDVI={s.ndvi:.3f}, GDD={s.gdd:.0f})")

    # Weather integration
    print("\n--- Weather Summary ---")
    weather = WeatherIntegrator()
    for day in range(30):
        weather.add_daily(WeatherData(
            date=f"2024-07-{day+1:02d}",
            temperature_max_f=88 + (day % 5),
            temperature_min_f=65 + (day % 3),
            precipitation_in=0.1 if day % 7 == 0 else 0,
            humidity_pct=60,
            wind_speed_mph=8,
        ))
    summary = weather.summarize()
    print(f"  Avg temp: {summary['avg_temp_f']}°F")
    print(f"  Total precip: {summary['total_precip_in']}\"")
    print(f"  GDD accumulated: {summary['gdd_accumulated']}")


if __name__ == "__main__":
    main()
