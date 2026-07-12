---
name: "crop-monitoring"
category: "ag-tech"
version: "2.0.0"
tags: ["agriculture", "crop-monitoring", "satellite", "ndvi", "drone", "remote-sensing", "phenology"]
---

# Crop Monitoring

## Overview

Advanced crop health monitoring system using multi-spectral satellite imagery, drone-based photogrammetry, and ground sensor fusion. This module processes NDVI, NDRE, SAVI, and custom vegetation indices to detect crop stress, nutrient deficiencies, water stress, and disease outbreaks at sub-field resolution. Provides time-series phenology tracking, automated alert generation, crop stage classification, and yield forecasting based on vegetation index trends and weather data integration.

## Core Capabilities

- **Vegetation Index Calculation**: Computes NDVI, NDRE, SAVI, EVI, GNDVI, and custom indices from multi-spectral imagery (Red, Green, Blue, NIR, Red Edge bands)
- **Stress Detection**: Identifies drought stress, nutrient deficiency (N, P, K), waterlogging, and frost damage using spectral signatures
- **Disease Detection**: Detects fungal, bacterial, and viral infections using characteristic spectral patterns and temporal changes
- **Phenology Tracking**: Monitors crop growth stages (emergence, vegetative, reproductive, maturity) using time-series analysis
- **Drone Mosaic Generation**: Processes overlapping drone images into georeferenced orthomosaics with ground control points
- **Weather Integration**: Correlates crop health with precipitation, temperature, humidity, and evapotranspiration data
- **Alert System**: Generates automated alerts when vegetation indices fall below thresholds or anomalous patterns are detected
- **Yield Forecasting**: Estimates harvest yield using vegetation index trends and historical yield correlations

## Usage

```python
from crop_monitoring import (
    VegetationIndex, CropAlert, PhenologyTracker, DroneProcessor, WeatherIntegrator
)

# Calculate NDVI from multi-spectral bands
vi = VegetationIndex()
ndvi = vi.calculate_ndvi(red=0.08, nir=0.45)
print(f"NDVI: {ndvi:.3f}")  # Healthy crop: 0.6-0.9

ndre = vi.calculate_ndre(red_edge=0.15, nir=0.45)
print(f"NDRE: {ndre:.3f}")

# Analyze stress from drone imagery
from crop_monitoring import StressAnalyzer
analyzer = StressAnalyzer()
stress_map = analyzer.analyze_field(
    red_band="field_red.tif",
    nir_band="field_nir.tif",
    red_edge_band="field_re.tif",
)
print(f"Healthy: {stress_map.healthy_pct:.1f}%")
print(f"Stressed: {stress_map.stressed_pct:.1f}%")
print(f"Critical: {stress_map.critical_pct:.1f}%")
for alert in stress_map.alerts:
    print(f"  ALERT: {alert.description}")
```

```python
# Phenology tracking
tracker = PhenologyTracker(field_id="FIELD-001")
stages = tracker.track_season("2024")
for stage in stages:
    print(f"  {stage.date}: {stage.name} (NDVI={stage.ndvi:.3f})")

# Generate monitoring report
from crop_monitoring import MonitoringReport
report = MonitoringReport.generate(
    field_id="FIELD-001",
    start_date="2024-04-01",
    end_date="2024-09-30",
)
report.export_html("crop_report_2024.html")
report.export_json("crop_report_2024.json")
```

## Best Practices

- Acquire satellite imagery during cloud-free periods (less than 10% cloud cover)
- Use drones for high-resolution monitoring when satellite revisit intervals are insufficient
- Calibrate NDVI thresholds based on crop type, growth stage, and local conditions
- Integrate weather data to distinguish between disease stress and environmental stress
- Maintain a historical database of vegetation indices for anomaly detection baseline
- Use Red Edge band (NDRE) for nitrogen status assessment — it is more sensitive than NDVI in dense canopies
- Process drone imagery with ground control points (GCPs) for accurate georeferencing
- Set alert thresholds per crop stage — NDVI naturally varies across the growing season
- Combine satellite and drone data for multi-scale monitoring (field-level + plant-level)
- Validate remote sensing findings with ground-truth field scouting

## Related Modules

- **precision-farming** — Use monitoring data to generate variable-rate prescriptions
- **soil-analysis** — Correlate crop stress with soil conditions
- **agricultural-iot** — Deploy ground sensors for continuous field monitoring
- **supply-chain** — Track crop quality from field to market
- **data-science** → **time-series** — Time-series analysis for phenology tracking
