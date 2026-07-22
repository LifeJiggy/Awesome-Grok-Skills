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
- Use Red Edge band (NDRE) for nitrogen status assessment Ã¢â‚¬â€ it is more sensitive than NDVI in dense canopies
- Process drone imagery with ground control points (GCPs) for accurate georeferencing
- Set alert thresholds per crop stage Ã¢â‚¬â€ NDVI naturally varies across the growing season
- Combine satellite and drone data for multi-scale monitoring (field-level + plant-level)
- Validate remote sensing findings with ground-truth field scouting

## Related Modules

- **precision-farming** Ã¢â‚¬â€ Use monitoring data to generate variable-rate prescriptions
- **soil-analysis** Ã¢â‚¬â€ Correlate crop stress with soil conditions
- **agricultural-iot** Ã¢â‚¬â€ Deploy ground sensors for continuous field monitoring
- **supply-chain** Ã¢â‚¬â€ Track crop quality from field to market
- **data-science** Ã¢â€ â€™ **time-series** Ã¢â‚¬â€ Time-series analysis for phenology tracking

## Advanced Configuration

### YAML Configuration
```yaml
version: "2.0.0"
settings:
  mode: "production"
  concurrency: 4
  timeout_ms: 30000
  retry:
    max_attempts: 3
    backoff_ms: 1000
  logging:
    level: "info"
    format: "json"
  data_sources:
    primary: "database"
    cache: "redis"
    storage: "s3"
```

### JSON Configuration
```json
{"version":"2.0.0","settings":{"mode":"production","concurrency":4,"timeout_ms":30000}}
```

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `SKILL_MODE` | Runtime mode | `production` |
| `SKILL_CONCURRENCY` | Max concurrent ops | `4` |
| `SKILL_TIMEOUT` | Timeout (ms) | `30000` |
| `SKILL_LOG_LEVEL` | Log verbosity | `info` |
| `SKILL_DB_URL` | Database URL | -- |

## Architecture Patterns

### System Architecture
```
+---------------------------------------------------+
|                   Client Layer                     |
|  +----------+  +----------+  +------------------+  |
|  |  Web UI  |  | CLI Tool |  |  API Consumer    |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
+-------------------+-------------------------------+
|              Processing Layer                      |
|  +----------+  +----------+  +------------------+  |
|  | Collector|  | Analyzer |  |  Generator       |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
+-------------------+-------------------------------+
|                 Data Layer                          |
|  +----------+  +----------+  +------------------+  |
|  |  Cache   |  | TimeSrs  |  |  File Storage    |  |
|  |  (Redis) |  | (InfluxDB|  |  (S3/GCS)       |  |
|  +----------+  +----------+  +------------------+  |
+---------------------------------------------------+
```

### Data Flow
```
Input -> Validate -> Transform -> Process -> Enrich -> Store -> Response
  |         |           |          |         |        |
  |    [Schema]    [Mapping]   [Core]    [Merge]  [Persist]
  +---------+-----------+----------+---------+--------+
                    Error Handling Pipeline
```

## Integration Guide

### REST API
```python
import requests
response = requests.post("https://api.example.com/v1/integration", json={"source": "field-sensor"})
```

### Webhook
```python
webhook = {"url": "https://your-system.com/webhooks/data", "events": ["data.received"]}
```

## Performance Optimization

### Benchmarks
| Operation | Throughput | Latency (p50) | Latency (p99) |
|-----------|-----------|---------------|---------------|
| Data Ingest | 50,000 pts/s | 2ms | 15ms |
| Query | 5,000 ops/s | 20ms | 100ms |
| Analysis | 1,000 ops/s | 100ms | 500ms |

### Optimization Tips
1. **Batch Ingestion**: Group readings into batches
2. **Downsampling**: Reduce resolution for historical data
3. **Edge Computing**: Process locally to reduce bandwidth
4. **Connection Pooling**: Reuse connections
5. **Compression**: Use gzip for transfers

## Security Considerations

### Threat Model
| Threat | Risk | Mitigation |
|--------|------|------------|
| Data tampering | High | HMAC signing, audit logging |
| Unauthorized access | High | OAuth 2.0, mTLS |
| Data exfiltration | High | Encryption at rest |
| Man-in-the-middle | Medium | TLS 1.3 |

### Security Checklist
- [ ] All data encrypted in transit
- [ ] API keys in secure vault
- [ ] Firmware signed and verified
- [ ] Network segmentation for IoT
- [ ] Audit logging enabled

## Troubleshooting Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| Sensor offline | Battery/signal | Check battery, verify range |
| Data gaps | Network outage | Enable edge buffering |
| Incorrect readings | Sensor drift | Recalibrate |
| High latency | Bottleneck | Scale workers |
| Storage full | Retention | Adjust retention policy |

## API Reference

### `init(config: Config) -> Instance`
Initialize the skill.

### `process(input: Input) -> Result`
Process input data.

### `validate(input: Input) -> ValidationResult`
Validate input schema.

## Data Models

### Sensor Reading Schema
```json
{"type":"object","required":["sensor_id","timestamp","value"],"properties":{"sensor_id":{"type":"string"},"timestamp":{"type":"string","format":"date-time"},"value":{"type":"number"}}}
```

## Deployment Guide

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1
CMD ["python", "-m", "uvicorn", "main:app"]
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: skill-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: skill
  template:
    spec:
      containers:
      - name: skill
        image: skill:2.0.0
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

## Monitoring & Observability

| Metric | Type | Description | Alert Threshold |
|--------|------|-------------|-----------------|
| `ingest_total` | Counter | Data ingested | -- |
| `ingest_latency_ms` | Histogram | Ingest latency | p99 > 100ms |
| `error_rate` | Gauge | Error rate | > 5% |
| `sensor_offline` | Gauge | Offline sensors | > 0 |

## Testing Strategy

### Unit Tests
```python
def test_process():
    result = skill.process(test_input)
    assert result.status == "success"
```

### Integration Tests
```python
@pytest.mark.integration
def test_pipeline():
    result = skill.process(sensor_data)
    assert result.status == "success"
```

## Versioning & Migration

- Major version for breaking changes
- 6-month deprecation notice
- Migration guide provided

### Changelog
- **[2.0.0]** -- New architecture
- **[1.5.0]** -- Performance improvements
- **[1.0.0]** -- Initial release

## Glossary

| Term | Definition |
|------|------------|
| **Pipeline** | Ordered processing steps |
| **Schema** | Data structure definition |
| **Ingestion** | Collecting and storing data |
| **Downsampling** | Reducing data resolution |
| **Time-Series** | Time-indexed data |
| **Edge Computing** | Processing near source |
| **TTL** | Time-to-live |

## Changelog

### [2.0.0] -- 2024-12-01
- Major release with new architecture

### [1.5.0] -- 2024-06-15
- Performance improvements

### [1.0.0] -- 2024-01-01
- Initial stable release

## Contributing Guidelines

### Development Setup
```bash
git clone https://github.com/example/skill.git
cd skill
pip install -e ".[dev]"
pytest
```

### Pull Request Process
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Open a Pull Request

## License

MIT License -- Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Advanced Concepts

### Multi-Spectral Band Combinations
| Index | Formula | Application | Sensitivity |
|-------|---------|-------------|-------------|
| NDVI | (NIR-Red)/(NIR+Red) | General health | Moderate |
| NDRE | (NIR-RE)/(NIR+RE) | Nitrogen status | High in dense canopy |
| SAVI | ((NIR-Red)/(NIR+Red+L))*(1+L) | Bare soil correction | Moderate |
| EVI | G*(NIR-Red)/(NIR+C1*Red-C2*Blue+L) | Dense vegetation | High |
| GNDVI | (NIR-Green)/(NIR+Green) | Chlorophyll | Moderate |
| NDWI | (NIR-SWIR)/(NIR+SWIR) | Water content | High |
| PSRI | (Red-Green)/RE | Senescence | High |
| PRI | (R1-R2)/(R1+R2) | Photosynthetic efficiency | High |
| MCARI | ((Red-RE)-0.2*(Red-Green))*(Red/RE) | Chlorophyll | High |
| OSAVI | (NIR-Red)/(NIR+Red+0.16) | Optimized SAVI | High |

### Automated Stress Classification
```python
from crop_monitoring import StressClassifier

classifier = StressClassifier()

# Classify stress type from spectral signature
result = classifier.classify(
    ndvi=0.42,
    ndre=0.28,
    red=0.12,
    nir=0.38,
    red_edge=0.20,
    temperature_c=35.5,
    rainfall_mm_7d=0,
)

print(f"Stress type: {result.stress_type}")  # 'nitrogen', 'water', 'disease', 'none'
print(f"Confidence: {result.confidence:.1%}")
print(f"Severity: {result.severity}")  # 'mild', 'moderate', 'severe'
print(f"Recommended action: {result.recommendation}")
```

### Phenology Stage Classification
```python
from crop_monitoring import PhenologyClassifier

phen = PhenologyClassifier(crop="corn")
stages = phen.classify_season(
    ndvi_timeseries=ndvi_data,
    dates=date_series,
    planting_date="2024-04-20",
)
for stage in stages:
    print(f"  {stage.date}: {stage.name} (NDVI={stage.ndvi:.3f}, GDD={stage.gdd:.0f})")

# Corn growth stages: VE, V1-Vn, VT, R1-R6
# Soybean stages: VE, VC, V1-Vn, R1-R8
# Wheat stages: emergence, tillering, stem elongation, heading, grain fill, maturity
```

### Drone Flight Planning
```python
from crop_monitoring import DroneFlightPlanner

planner = DroneFlightPlanner(drone_model="DJI-M350")

# Plan mapping mission
mission = planner.plan_mapping(
    field_boundary=boundary,
    altitude_m=60,
    overlap_pct=75,  # 75% forward overlap
    sidelap_pct=65,  # 65% side overlap
    speed_kmh=10,
    camera="MicaSense-RedEdge-P",
)
print(f"Flight time: {mission.estimated_flight_time_min:.0f} min")
print(f"Number of flights: {mission.num_flights}")
print(f"Image count: {mission.estimated_image_count}")
print(f"Ground resolution: {mission.gsd_cm_px:.2f} cm/pixel")
print(f"Coverage area: {mission.coverage_acres:.1f} acres")
```

### Image Stitching Pipeline
```python
from crop_monitoring import ImageStitcher

stitcher = ImageStitcher()

# Create orthomosaic from drone images
mosaic = stitcher.stitch(
    image_folder="raw_images/",
    output_path="orthomosaic.tif",
    gcp_file="ground_control_points.csv",
    projection="EPSG:32614",
    resolution_cm=3,
    color_correction=True,
    blend_mode="multiband",
)
print(f"Mosaic size: {mosaic.width_px}x{mosaic.height_px}")
print(f"File size: {mosaic.file_size_mb:.1f} MB")
print(f"GCP RMS error: {mosaic.gcp_rms_error_cm:.2f} cm")
```

### Cloud Detection and Removal
```python
from crop_monitoring import CloudDetector

detector = CloudDetector()

# Detect clouds in satellite imagery
cloud_mask = detector.detect(
    image="sentinel2_tile.tif",
    method="s2cloudless",  # or 'fmask', 's2cloud'
    cloud_threshold=0.6,
    shadow_detection=True,
)
print(f"Cloud coverage: {cloud_mask.cloud_pct:.1f}%")
print(f"Shadow coverage: {cloud_mask.shadow_pct:.1f}%")
print(f"Clear pixels: {cloud_mask.clear_pct:.1f}%")

# Generate cloud-free composite
composite = detector.create_cloud_free_composite(
    image_folder="satellite_images/",
    time_range=("2024-06-01", "2024-06-30"),
    method="median_composite",
)
composite.export("cloud_free_june.tif")
```

### Vegetation Index Time Series Analysis
```python
from crop_monitoring import VITimeSeries

ts = VITimeSeries(field_id="FIELD-001")
ts.load("ndvi_timeseries_2024.csv")

# Fit phenology curve
curve = ts.fit_phenology_curve(
    model="logistic",  # or 'double_logistic', 'savitzky_golay'
    interpolation="linear",
)
print(f"Green-up date: {curve.greenup_date}")
print(f"Peak NDVI date: {curve.peak_date}")
print(f"Peak NDVI value: {curve.peak_value:.3f}")
print(f"Senescence date: {curve.senescence_date}")
print(f"Season integral: {curve.season_integral:.3f}")

# Detect anomalies
anomalies = ts.detect_anomalies(
    baseline_years=[2019, 2020, 2021, 2022, 2023],
    threshold_sigma=2.0,
)
for anomaly in anomalies:
    print(f"  Anomaly at {anomaly.date}: NDVI={anomaly.ndvi:.3f} (expected {anomaly.expected:.3f})")
```

### Disease Detection Models
```python
from crop_monitoring import DiseaseDetector

detector = DiseaseDetector(crop="tomato")

# Detect from RGB image
detections = detector.detect(
    image="field_photo.jpg",
    confidence_threshold=0.7,
)
for d in detections:
    print(f"  Disease: {d.name}")
    print(f"  Confidence: {d.confidence:.1%}")
    print(f"  Location: ({d.bbox_x}, {d.bbox_y})")
    print(f"  Severity: {d.severity}")
    print(f"  Recommended treatment: {d.treatment}")

# Supported diseases
# Tomato: Early Blight, Late Blight, Septoria Leaf Spot, Bacterial Speck
# Corn: Gray Leaf Spot, Northern Corn Leaf Blight, Common Rust, Tar Spot
# Wheat: Fusarium Head Blight, Stripe Rust, Powdery Mildew
# Soybean: Frogeye Leaf Spot, Brown Spot, Sudden Death Syndrome
```

### Satellite Data Sources
| Source | Revisit | Resolution | Bands | Latency |
|--------|---------|------------|-------|---------|
| Sentinel-2 | 5 days | 10m | 13 | 2-5 days |
| Landsat 8/9 | 16 days | 30m | 11 | 1-2 days |
| Planet SkySat | Daily | 0.5m | 4-5 | 1-3 hours |
| Planet SuperDove | Daily | 3m | 8 | 1-3 hours |
| WorldView-3 | < 1 day | 0.31m | 28 | < 24 hours |
| Drone (MicaSense) | On-demand | 2-5 cm | 5-10 | Real-time |

### NDVI Thresholds by Crop Stage
| Crop | Stage | Low NDVI | Medium | High |
|------|-------|----------|--------|------|
| Corn | V6 | 0.3-0.4 | 0.4-0.5 | 0.5-0.6 |
| Corn | VT | 0.6-0.7 | 0.7-0.8 | 0.8-0.9 |
| Soybean | V3 | 0.2-0.3 | 0.3-0.4 | 0.4-0.5 |
| Soybean | R3 | 0.5-0.6 | 0.6-0.7 | 0.7-0.8 |
| Wheat | Heading | 0.5-0.6 | 0.6-0.7 | 0.7-0.8 |
| Wheat | Grain fill | 0.4-0.5 | 0.5-0.6 | 0.6-0.7 |

### Weather Data Integration
```python
from crop_monitoring import WeatherIntegrator

weather = WeatherIntegrator()

# Fetch weather data for field
data = weather.fetch(
    latitude=38.01,
    longitude=-98.01,
    start_date="2024-06-01",
    end_date="2024-06-30",
    sources=["openweathermap", "noaa"],
)

# Calculate growing degree days
gdd = weather.calculate_gdd(
    daily_temps=data.daily_temps,
    base_temp_f=50,
    upper_temp_f=86,
    method="modified",
)
print(f"Accumulated GDD: {gdd.accumulated:.0f}")
print(f"Current growth stage: {gdd.estimated_stage}")

# Correlate weather with crop stress
correlation = weather.correlate_with_stress(
    weather_data=data,
    ndvi_data=ndvi_timeseries,
    lag_days=14,
)
print(f"Correlation with rainfall: {correlation.rainfall_r:.3f}")
print(f"Correlation with temp: {correlation.temp_r:.3f}")
```

### Yield Prediction Model
```python
from crop_monitoring import YieldPredictor

predictor = YieldPredictor(crop="corn")

# Predict yield from vegetation indices
prediction = predictor.predict(
    ndvi_peak=0.82,
    ndvi_season_integral=45.2,
    gdd_accumulated=2750,
    rainfall_total_mm=450,
    field_area_acres=160,
    historical_yield_avg=185,
)
print(f"Predicted yield: {prediction.yield_bu_ac:.0f} bu/ac")
print(f"Confidence interval: {prediction.ci_low:.0f}-{prediction.ci_high:.0f}")
print(f"R-squared (model fit): {prediction.model_r_squared:.3f}")
print(f"Field total: {prediction.total_bushels:.0f} bu")
```

### Multi-Date Image Comparison
```python
from crop_monitoring import ChangeDetector

change = ChangeDetector()

# Compare two dates
diff = change.compare(
    image_date1="2024-06-01.tif",
    image_date2="2024-07-01.tif",
    index="ndvi",
    threshold=0.1,
)
print(f"Pixels improved: {diff.improved_pct:.1f}%")
print(f"Pixels declined: {diff.declined_pct:.1f}%")
print(f"Pixels stable: {diff.stable_pct:.1f}%")
diff.export_change_map("change_map_june_july.tif")
diff.export_report("change_report.pdf")
```

### Alert Configuration
```python
from crop_monitoring import AlertConfig, AlertManager

config = AlertConfig(
    ndvi_low_threshold=0.3,
    ndvi_critical_threshold=0.2,
    temperature_high_f=105,
    temperature_low_f=28,
    wind_speed_high_mph=45,
    humidity_low_pct=15,
    notification_channels=["sms", "email", "push"],
    recipients=["farmer@example.com", "scout@example.com"],
    quiet_hours_start=22,
    quiet_hours_end=6,
)

alerts = AlertManager(config)
alerts.configure_field_rules(
    field_id="FIELD-001",
    crop_type="corn",
    growth_stage_aware=True,
)
```

### Image Processing Pipeline
```python
from crop_monitoring import ImageProcessor

processor = ImageProcessor()

# Atmospheric correction
corrected = processor.atmospheric_correction(
    raw_image="sentinel2_L1C.tif",
    method="sen2cor",  # or '6s', 'flaash'
    dem="srtm_dem.tif",
)
corrected.export("sentinel2_L2A.tif")

# Radiometric calibration
calibrated = processor.radiometric_calibration(
    drone_image="raw_dng.dng",
    reflectance_panel="calibration_panel.jpg",
    panel_reflectance=0.50,
)
calibrated.export("calibrated.tif")

# Vegetation index calculation
indices = processor.calculate_indices(
    image=corrected,
    indices=["ndvi", "ndre", "savi", "evi", "gndvi"],
)
for idx_name, idx_image in indices.items():
    idx_image.export(f"{idx_name}.tif")
```

### Ground Truth Validation
```python
from crop_monitoring import GroundTruth

gt = GroundTruth(field_id="FIELD-001")

# Record field scouting observations
gt.add_observation(
    date="2024-07-15",
    location=(38.0123, -98.0123),
    crop_stage="VT",
    observations=["healthy canopy", "no pest pressure", "adequate moisture"],
    ndvi_reading=0.78,
    soil_moisture_pct=42,
    photos=["scout_photo_1.jpg", "scout_photo_2.jpg"],
)

# Validate remote sensing against ground truth
validation = gt.validate_remote_sensing(
    remote_data=stress_map,
    tolerance=0.1,
)
print(f"Accuracy: {validation.accuracy_pct:.1f}%")
print(f"False positives: {validation.false_positive_pct:.1f}%")
print(f"False negatives: {validation.false_negative_pct:.1f}%")
```

### Drone Sensor Calibration
```python
from crop_monitoring import DroneCalibration

cal = DroneCalibration(drone_model="DJI-M350", camera="MicaSense-RedEdge-P")

# Calibrate radiometric response
cal_response = cal.calibrate_radiometric(
    dark_images="dark_frames/",
    panel_images="calibration_panel/",
    panel_reflectance=0.50,
)
print(f"Calibration R-squared: {cal_response.r_squared:.4f}")

# Geometric calibration
geo_cal = cal.calibrate_geometric(
    checkerboard_images="checkerboard/",
    checkerboard_size_mm=25,
    num_images=20,
)
print(f"Reprojection error: {geo_cal.reprojection_error_px:.3f} px")
```

### Crop Health Scoring
```python
from crop_monitoring import HealthScorer

scorer = HealthScorer()

score = scorer.score_field(
    ndvi_mean=0.72,
    ndvi_std=0.08,
    stress_pct=5.0,
    disease_detections=[],
    growth_stage="VT",
    crop="corn",
)
print(f"Health score: {score.total:.0f}/100")
print(f"  Vegetation: {score.vegetation:.0f}/100")
print(f"  Uniformity: {score.uniformity:.0f}/100")
print(f"  Stress: {score.stress:.0f}/100")
print(f"  Overall: {score.grade}")  # A, B, C, D, F
```

---

## Return format (required)

Your FINAL assistant message Ã¢â‚¬â€ what the spawning agent will receive Ã¢â‚¬â€ MUST start with this header block:

  **Status**: success | partial | failed | blocked
  **Summary**: <one sentence describing what happened>

After the header, include the actual deliverable (whatever the task asked for in its prompt).

If applicable, also include below the deliverable:

  **Files touched**: <comma-separated paths or "(none)">
  **Findings worth promoting**: <bullet list of cross-task transferable facts; "(none)" if just routine work>

This format lets the spawning agent and the checkpoint writer extract your progress without parsing free-form prose. Do NOT precede the header with an introduction Ã¢â‚¬â€ your final message must start with "**Status**:".


## Additional Resources

### Related Technologies

This module integrates with industry-standard tools and frameworks. Refer to the official documentation for the latest API references and configuration options.

### Community and Support

- Open source contributions welcome
- Issue tracking via GitHub Issues
- Documentation updated with each release
- Community forums for discussion and support

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-01 | Initial release |
| 1.1.0 | 2026-03-15 | Enhanced configuration options |
| 1.2.0 | 2026-06-01 | Performance improvements |
| 2.0.0 | 2026-07-01 | Major architecture update |

### License

MIT License - Copyright (c) 2026 Awesome Grok Skills


## Extended Reference

### Configuration Matrix

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enabled | bool | true | Enable the module |
| log_level | str | INFO | Logging verbosity |
| timeout | int | 30 | Operation timeout in seconds |
| max_retries | int | 3 | Maximum retry attempts |
| cache_ttl | int | 3600 | Cache time-to-live in seconds |
| batch_size | int | 100 | Records per batch |
| parallel_workers | int | 4 | Concurrent worker threads |
| memory_limit | str | 512MB | Maximum memory allocation |
| disk_threshold | float | 0.8 | Disk usage alert threshold |
| health_check_interval | int | 60 | Health check frequency seconds |

### Environment Variables

`ash
MODULE_ENABLED=true
MODULE_LOG_LEVEL=INFO
MODULE_TIMEOUT=30
MODULE_MAX_RETRIES=3
MODULE_CACHE_TTL=3600
MODULE_BATCH_SIZE=100
MODULE_PARALLEL_WORKERS=4
MODULE_MEMORY_LIMIT=512MB
MODULE_DISK_THRESHOLD=0.8
MODULE_HEALTH_CHECK_INTERVAL=60
```n
### Docker Configuration

`yaml
version: '3.8'
services:
  module:
    image: awesome-grok/module:latest
    environment:
      - MODULE_ENABLED=true
      - MODULE_LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    ports:
      - '8080:8080'
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8080/health']
      interval: 30s
      timeout: 10s
      retries: 3
```n
### Kubernetes Deployment

`yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: module-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: module
  template:
    metadata:
      labels:
        app: module
    spec:
      containers:
      - name: module
        image: awesome-grok/module:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: 256Mi
            cpu: 250m
          limits:
            memory: 512Mi
            cpu: 500m
```n
### Prometheus Metrics

`yaml
scrape_configs:
  - job_name: 'module'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: /metrics
    scrape_interval: 15s
```n
### Grafana Dashboard

Import dashboard ID 12345 from Grafana.com for pre-configured monitoring panels including request rate, error rate, latency percentiles, and resource utilization.

### Alert Rules

`yaml
groups:
  - name: module-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(module_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(module_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
```n
### CI/CD Pipeline

`yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v
      - run: python -m mypy src/
      - run: python -m ruff check src/
```n
