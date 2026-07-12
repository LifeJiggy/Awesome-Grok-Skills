---
name: "climate-data"
category: "climate-tech"
version: "2.0.0"
tags: ["climate-tech", "climate-data", "CMIP6", "temperature", "precipitation"]
---

# Climate Data

## Overview

The Climate Data module provides tools for processing, analyzing, and visualizing climate datasets including CMIP6 projections, ERA5 reanalysis, and satellite observations. It covers temperature anomaly analysis, precipitation pattern detection, extreme weather event identification, climate model intercomparison, and downscaling methodologies.

This skill is essential for climate scientists, meteorologists, environmental consultants, and researchers working with climate projections and observational data.

## Core Capabilities

- **Temperature Analysis**: Anomaly calculation, trend detection, heat index computation, growing degree days
- **Precipitation Analysis**: Rainfall intensity classification, drought indices (SPI, PDSI), flood risk assessment
- **Extreme Events**: Heat wave detection, cold spells, extreme precipitation, tropical cyclone tracking
- **Climate Projections**: CMIP6 scenario analysis, model ensemble statistics, uncertainty quantification
- **Downscaling**: Statistical downscaling, bias correction, delta method, quantile mapping
- **Sea Level**: Coastal flood risk, tidal analysis, storm surge estimation
- **Cryosphere**: Snow cover analysis, glacier mass balance, permafrost monitoring
- **Climate Indices**: ENSO, NAO, PDO, AMO teleconnection analysis

## Usage Examples

```python
from climate_data import (
    TemperatureAnalyzer,
    PrecipitationAnalyzer,
    ExtremeEventDetector,
    CMIP6Processor,
    Downscaler,
)

# --- Temperature Analysis ---
temp = TemperatureAnalyzer()
anomaly = temp.calculate_anomaly(
    observed=[14.5, 14.7, 14.8, 15.0, 15.1],
    baseline=[14.0, 14.0, 14.0, 14.0, 14.0],
)
print(f"Temperature anomaly: {anomaly.mean_anomaly:.2f} deg C")
print(f"Trend: {anomaly.trend_per_decade:.2f} deg C/decade")

# --- Precipitation ---
precip = PrecipitationAnalyzer()
spi = precip.calculate_spi(
    precipitation=[50, 45, 30, 20, 15, 10, 8, 5],
    scale_months=3,
)
print(f"SPI: {spi:.2f}")

# --- Extreme Events ---
detector = ExtremeEventDetector()
heatwaves = detector.detect_heatwaves(
    temperatures=[32, 33, 35, 36, 34, 33, 31],
    threshold=32,
    min_duration=3,
)
print(f"Heat waves: {len(heatwaves)}")
for hw in heatwaves:
    print(f"  {hw.start_date} to {hw.end_date}: max {hw.max_temp:.1f} deg C")

# --- CMIP6 Projections ---
cmip = CMIP6Processor()
projection = cmip.analyze_scenario(
    model="EC-Earth3",
    scenario="ssp245",
    variable="tas",
    region={"lat_min": 30, "lat_max": 45, "lon_min": -10, "lon_max": 10},
)
print(f"Mean warming: {projection.mean_anomaly:.2f} deg C")
print(f"Uncertainty range: {projection.ci_lower:.2f} to {projection.ci_upper:.2f}")

# --- Downscaling ---
downscaler = Downscaler(method="quantile_mapping")
local = downscaler.downscale(
    coarse_data=[14.5, 14.7, 15.0],
    reference_data=[14.2, 14.4, 14.8],
    target_resolution_km=1,
)
print(f"Downscaled values: {local}")
```

## Best Practices

- Use bias-corrected CMIP6 data for impact assessments — raw model output has systematic biases
- Apply appropriate statistical tests for trend detection (Mann-Kendall, linear regression)
- Account for autocorrelation in climate time series when calculating significance
- Use ensemble medians for projections; report inter-model spread as uncertainty
- Apply delta method downscaling for local-scale impact studies
- Use SPI for drought monitoring — it's standardized and comparable across regions
- Consider non-stationarity in extreme event analysis under climate change
- Validate downscaling methods against historical observations before applying to projections
- Report both mean and extreme changes — means can mask amplified extremes
- Use appropriate baselines (1991-2020 or 1981-2010) for anomaly calculations

## Related Modules

- **environmental-modeling**: Climate-driven ecosystem modeling
- **carbon-tracking**: Emissions data for climate projections
- **renewable-energy**: Climate data for energy system planning
- **emission-reduction**: Climate scenarios for mitigation pathways
