---
name: "space-data"
category: "space-tech"
version: "1.0.0"
tags: ["space-tech", "space-data", "space-weather", "earth-observation"]
---

# Space Data Processing Toolkit

## Overview

The Space Data module provides a comprehensive computational framework for processing, analyzing, and fusing the diverse data streams that characterize the modern space domain. It covers space weather data processing (solar wind, geomagnetic indices, radiation belt flux), Earth observation data pipelines (optical and SAR imagery, atmospheric sounding), on-board data compression, remote sensing image analysis, space debris cataloguing, satellite telemetry analysis, ephemeris processing, and space situational awareness (SSA) data fusion. The module is designed for data engineers and analysts who need to transform raw space-domain data into actionable intelligence.

The space weather subsystem processes real-time and archival data from NOAA SWPC, including Kp, Dst, F10.7, solar wind speed/density/IMF, and proton/electron flux. It models radiation dose rates for spacecraft components, predicts geomagnetically induced currents (GIC), and provides space weather impact assessments for mission operations. The Earth observation pipeline handles both optical (multispectral, hyperspectral) and SAR data, with support for atmospheric correction, orthorectification, change detection, and feature extraction.

The debris cataloguing subsystem processes TLE (Two-Line Element) data, computes orbital evolution under J2 and drag, performs conjunction screening, and maintains a statistical debris environment model (ORDEM-like). The telemetry analysis module decompresses and parses satellite housekeeping data, performs anomaly detection via statistical process control, and generates trend reports. The SSA data fusion engine correlates data from multiple sensors (radar, optical, RF) to maintain a unified space object catalog with track association and orbit improvement.

## Core Capabilities

- **Space Weather Processing**: Real-time Kp/Dst/F10.7 index computation, solar wind parameter parsing, radiation belt flux modeling, geomagnetic storm classification (G-scale), and radiation dose estimation for spacecraft electronics
- **Earth Observation Pipelines**: Optical and SAR data ingestion, atmospheric correction (6S model), radiometric calibration, geometric orthorectification, image mosaicking, and time-series change detection
- **On-Board Data Compression**: Lossless (CCSDS 121.0-B-2 BZIP, CCSDS 123.0-B-2 predictive) and lossy (wavelet, JPEG2000) compression modeling; compression ratio estimation for various data types
- **Remote Sensing Image Analysis**: NDVI computation, spectral index analysis, supervised/unsupervised classification, edge detection, texture analysis, and anomaly detection in EO imagery
- **Space Debris Cataloguing**: TLE parsing and propagation, orbital collision probability computation, debris flux estimation (ORDEM), reentry prediction, and fragmentation event tracking
- **Satellite Telemetry Analysis**: TM packet parsing, housekeeping parameter extraction, limit checking, trend analysis, anomaly detection via CUSUM and EWMA control charts
- **Ephemeris Processing**: SPICE kernel management, state interpolation, coordinate frame transformations (ECI/ECEF/SEZ), and conjunction data message (CDM) parsing
- **SSA Data Fusion**: Multi-sensor track association, Bayesian orbit estimation, sensor bias calibration, track-to-track correlation, and unified catalog maintenance

## Usage Examples

### Space Weather Data Processing

```python
from space_data import SpaceWeatherProcessor, SolarWindData

swp = SpaceWeatherProcessor()

# Process solar wind measurement
solar_wind = SolarWindData(
    speed_kms=450.0,
    density_pcc=5.0,
    imf_bt_nt=5.0,
    imf_bz_nt=-8.0,
    temperature_k=100000.0,
)

storm = swp.classify_storm(solar_wind, kp_index=6.0)
print(f"Storm classification: {storm.severity.name}")
print(f"Estimated Dst:        {storm.estimated_dst_nt:.0f} nT")
print(f"Radiation dose rate:  {storm.radiation_dose_rate_mrad_hr:.2f} mrad/hr")
print(f"Mission impact:       {storm.mission_impact_level}")
print(f"Recommendations:")
for rec in storm.recommendations:
    print(f"  - {rec}")

# Radiation dose estimation
dose = swp.estimate_radiation_dose(
    energy_mev=50.0,
    shielding_mm_al=3.0,
    duration_hours=24.0,
)
print(f"\nRadiation dose (24h): {dose:.4f} mrad")
```

### Earth Observation Data Pipeline

```python
from space_data import EOPipeline, SensorConfig

sensor = SensorConfig(
    sensor_type="optical",
    bands=4,
    resolution_m=10.0,
    snr_db=45.0,
    swath_width_km=290.0,
)

pipeline = EOPipeline(sensor=sensor)
result = pipeline.process(
    raw_data_path="/data/scene_001.raw",
    output_format="GeoTIFF",
    atmospheric_correction=True,
    orthorectify=True,
)
print(f"Output:            {result.output_path}")
print(f"Cloud cover:       {result.cloud_cover_pct:.1f}%")
print(f"Processing time:   {result.processing_time_s:.1f} s")
print(f"Bands processed:   {result.bands_processed}")
print(f"Pixel count:       {result.pixel_count:,}")

# NDVI computation
red_band = [0.08, 0.12, 0.15, 0.10, 0.05]
nir_band = [0.25, 0.35, 0.40, 0.30, 0.18]
ndvi = pipeline.compute_ndvi(red_band, nir_band)
print(f"\nNDVI values: {[f'{v:.3f}' for v in ndvi]}")
```

### Space Debris Analysis

```python
from space_data import DebrisCatalog, DebrisObject
from datetime import datetime

catalog = DebrisCatalog()

# Manually add debris objects
obj1 = DebrisObject(
    catalog_number=25544, name="ISS",
    epoch=datetime.now(),
    sma_km=6780.0, eccentricity=0.0006, inclination_deg=51.6,
    raan_deg=45.0, arg_perigee_deg=0.0, mean_anomaly_deg=120.0,
    cross_section_m2=4000.0, mass_kg=420000.0,
)
obj2 = DebrisObject(
    catalog_number=99999, name="DEBRIS-A",
    epoch=datetime.now(),
    sma_km=6790.0, eccentricity=0.005, inclination_deg=51.8,
    raan_deg=46.0, arg_perigee_deg=10.0, mean_anomaly_deg=200.0,
    cross_section_m2=5.0, mass_kg=5.0,
)
catalog.add_object(obj1)
catalog.add_object(obj2)

print(f"Catalog size: {catalog.object_count}")
print(f"Object orbital regime: {obj1.orbital_regime.value}")
print(f"Orbital period: {obj1.orbital_period_minutes:.1f} min")

# Conjunction screening
conjunctions = catalog.screen_conjunctions(
    target_sma=6780.0,
    target_inc_deg=51.6,
    time_window_days=7.0,
    distance_threshold_km=10.0,
)
print(f"\nConjunctions found: {len(conjunctions)}")
for c in conjunctions:
    print(f"  Object {c.secondary_catalog_number}: "
          f"miss={c.miss_distance_km:.3f} km, "
          f"PoC={c.probability_of_collision:.2e}")
```

### Satellite Telemetry Anomaly Detection

```python
from space_data import TelemetryAnalyzer, TelemetryParameter

analyzer = TelemetryAnalyzer()

params = [
    TelemetryParameter("battery_voltage_v", 28.2, unit="V", limits=(26.0, 30.0)),
    TelemetryParameter("solar_array_current_a", 4.5, unit="A", limits=(0.0, 8.0)),
    TelemetryParameter("cpu_temp_c", 35.0, unit="°C", limits=(-10.0, 60.0)),
    TelemetryParameter("reaction_wheel_rpm", 3200.0, unit="rpm", limits=(0, 6000)),
]

# Ingest history for trending
for _ in range(20):
    import random
    analyzer.ingest([
        TelemetryParameter("battery_voltage_v", 28.0 + random.gauss(0, 0.1), unit="V"),
        TelemetryParameter("cpu_temp_c", 35.0 + random.gauss(0, 1.0), unit="°C"),
    ])

anomalies = analyzer.detect_anomalies(params, method="cusum")
for a in anomalies:
    print(f"ANOMALY: {a.parameter_name} = {a.value} {a.unit} "
          f"({a.deviation_sigma:.1f}σ from mean)")
    print(f"  Severity: {a.severity}")

# Trend analysis
trend = analyzer.compute_trend("battery_voltage_v")
if trend is not None:
    print(f"\nBattery voltage trend: {trend:+.4f} V/sample")
```

### Ephemeris Processing

```python
from space_data import EphemerisProcessor, EphemerisState, CoordinateFrame
from datetime import datetime, timedelta

eph = EphemerisProcessor()

# Add ephemeris states
t0 = datetime.now()
eph.add_state(EphemerisState(
    epoch=t0,
    position_eci_m=(6871000.0, 0.0, 0.0),
    velocity_eci_mps=(0.0, 7500.0, 0.0),
    frame=CoordinateFrame.ECI,
))
eph.add_state(EphemerisState(
    epoch=t0 + timedelta(minutes=45),
    position_eci_m=(0.0, 6871000.0, 500000.0),
    velocity_eci_mps=(-7500.0, 0.0, 100.0),
    frame=CoordinateFrame.ECI,
))

# Interpolate at intermediate time
target = t0 + timedelta(minutes=20)
interp = eph.interpolate(target)
if interp:
    print(f"Interpolated radius: {interp.radius_m / 1000:.1f} km")
    print(f"Interpolated speed:  {interp.speed_mps:.1f} m/s")

# Propagate forward
propagated = eph.propagate_keplerian(eph._states[0], delta_s=3600.0)
print(f"Propagated radius:   {propagated.radius_m / 1000:.1f} km")

# Frame transformation
ecef = eph.eci_to_ecef(propagated, gmst_rad=0.5)
print(f"ECEF position:       ({ecef[0]/1000:.1f}, {ecef[1]/1000:.1f}, {ecef[2]/1000:.1f}) km")
```

### SSA Data Fusion

```python
from space_data import SSADataFusion, SensorType, EphemerisState
from datetime import datetime

ssa = SSADataFusion()

# Register sensor biases
ssa.register_sensor_bias("RADAR-1", bias_rad=(0.001, -0.002, 0.0))
ssa.register_sensor_bias("OPTICAL-1", bias_rad=(-0.0005, 0.001, 0.0))

# Add known objects to catalog
state = EphemerisState(
    epoch=datetime.now(),
    position_eci_m=(6871000.0, 0.0, 0.0),
    velocity_eci_mps=(0.0, 7500.0, 0.0),
)
ssa.update_catalog(1001, state)

# Try to associate a new observation
assoc = ssa.associate_observation(
    sensor_id="RADAR-1",
    sensor_type=SensorType.RADAR,
    observation_time=datetime.now(),
    measured_position=(6871500.0, 100.0, 50.0),
    measurement_covariance=(100.0, 100.0, 100.0),
)
if assoc:
    print(f"Association: {'Matched' if assoc.is_associated else 'No match'}")
    print(f"  Catalog #:   {assoc.catalog_number}")
    print(f"  Mahalanobis: {assoc.mahalanobis_distance:.3f}")

print(f"\nCatalog size:    {ssa.catalog_size()}")
print(f"Association rate: {ssa.association_rate():.1%}")
```

### Data Compression Modeling

```python
from space_data import CompressionModeler, CompressionType

comp = CompressionModeler()

data_sizes = [1024 * 1024, 10 * 1024 * 1024, 100 * 1024 * 1024]
algorithms = [
    CompressionType.WAVELET,
    CompressionType.JPEG2000,
    CompressionType.LOSSLESS_CCSDS_123,
]

print("Compression Analysis:")
print(f"{'Algorithm':<25} {'Original':>10} {'Compressed':>10} {'Ratio':>8} {'Time':>8}")
print("-" * 65)
for size in data_sizes:
    for algo in algorithms:
        res = comp.estimate_ratio("imagery", algo, size)
        print(f"{algo.value:<25} {size/1024:>8.0f}KB "
              f"{res.compressed_size_bytes/1024:>8.0f}KB "
              f"{res.compression_ratio:>7.1f}:1 "
              f"{res.compression_time_ms:>7.1f}ms")
```

## Best Practices

1. **Always validate space weather input data for quality flags before using it in mission operations.** NOAA SWPC data can contain missing values, sensor dropouts, and calibration artifacts — blindly processing raw data produces incorrect Kp and Dst values that can trigger unnecessary mission responses.
2. **Earth observation atmospheric correction should use site-specific aerosol optical depth (AOD) data when available.** The default climatological AOD can introduce 5–10% reflectance errors that propagate into downstream products like NDVI and land cover classification.
3. **For space debris conjunction assessment, always use the latest TLE catalog (within 24 hours) and propagate with SGP4, not simple Keplerian models.** TLE elements already include mean-element corrections for drag and J2 — re-propagating with a different model introduces artificial errors.
4. **On-board data compression ratio estimation should be validated against actual flight data, not just synthetic test patterns.** Real spacecraft data (imagery, telemetry, science data) has different entropy characteristics than JPEG test images — using the wrong model can cause data storage shortfalls.
5. **Telemetry anomaly detection should use rolling-window baselines, not global statistics.** Spacecraft parameters drift slowly over the mission lifetime due to component aging — a 2-year-old battery voltage baseline will generate false anomaly flags for normal degradation.
6. **When fusing multi-sensor SSA data, always calibrate sensor biases before track association.** A 0.1° systematic bias in an optical sensor produces hundreds of kilometers of position error at GEO range — this overwhelms the track correlation logic if not removed.
7. **Ephemeris processing should use the latest leap second table and IAU precession/nutation model.** UTC-UT1 differences accumulate to seconds over decades, and using an outdated model introduces timing errors that affect conjunction assessment accuracy.
8. **SSA data fusion track association should use a Mahalanobis distance threshold of 3σ, not a simple position threshold.** The Mahalanobis distance accounts for the covariance of both tracks and provides a statistically principled association criterion that adapts to measurement quality.

## Related Modules

- [aerospace-engineering](../aerospace-engineering/GROK.md) — Propulsion, structural analysis, orbital mechanics
- [satellite-systems](../satellite-systems/GROK.md) — ADCS, constellation design, link budgets
- [mission-planning](../mission-planning/GROK.md) — Scheduling, launch windows, resource allocation
- [ground-stations](../ground-stations/GROK.md) — Antenna tracking, signal processing, telemetry
