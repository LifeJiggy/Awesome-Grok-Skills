---
name: "precision-farming"
category: "ag-tech"
version: "2.0.0"
tags: ["agriculture", "precision-farming", "variable-rate", "gps", "yield-mapping", "site-specific"]
---

# Precision Farming

## Overview

Comprehensive precision agriculture toolkit for site-specific crop management using GPS guidance, variable-rate technology (VRT), yield mapping, and geospatial data analysis. This module integrates soil sampling data, satellite imagery, drone photogrammetry, and IoT sensor networks to generate prescription maps for variable-rate application of seeds, fertilizers, and pesticides. Supports multi-layer GIS analysis, zone management, economic optimization, and compliance reporting for USDA conservation programs.

## Core Capabilities

- **Variable-Rate Prescription Maps**: Generate seed rate, fertilizer (N/P/K), and pesticide application maps from soil data, yield history, and satellite imagery
- **Yield Map Processing**: Import, clean, and analyze yield monitor data from John Deere, Case IH, AGCO, and CLAAS equipment
- **GPS Guidance Line Management**: Generate A-B lines, heading lines, pivot guidance, and curved paths for auto-steer systems
- **Multi-Layer GIS Analysis**: Overlay soil type, elevation, drainage, EC maps, and organic matter data for management zone delineation
- **Economic Optimization**: Calculate ROI per management zone considering input costs, expected yield, and commodity prices
- **Zone Management**: Create variable-rate management zones using k-means clustering, soil electrical conductivity, or historical yield data
- **Prescription File Export**: Generate shapefiles, ISO-XML, and proprietary formats (John Deere Operations Center, Climate FieldView)
- **Compliance Reporting**: Generate field-level reports for NRCS EQIP, CSP, and conservation practice documentation

## Usage

```python
from precision_farming import (
    PrescriptionEngine, YieldMapper, ZoneManager, SoilDataProvider
)

# Load soil sample data
soil = SoilDataProvider.from_csv("soil_samples_2024.csv")
print(f"Loaded {len(soil.samples)} soil samples")
print(f"N range: {soil.n_range[0]:.0f}-{soil.n_range[1]:.0f} ppm")
print(f"P range: {soil.p_range[0]:.0f}-{soil.p_range[1]:.0f} ppm")
print(f"pH range: {soil.ph_range[0]:.1f}-{soil.ph_range[1]:.1f}")

# Create management zones
zone_mgr = ZoneManager(soil_data=soil)
zones = zone_mgr.create_zones(
    num_zones=5,
    method="kmeans",
    features=["nitrogen", "phosphorus", "ph", "organic_matter", "cec"],
)
print(f"Created {len(zones)} management zones")
for zone in zones:
    print(f"  Zone {zone.id}: {zone.area_acres:.1f} acres, N={zone.avg_n:.0f}ppm, pH={zone.avg_ph:.1f}")

# Generate variable-rate nitrogen prescription
engine = PrescriptionEngine(soil_data=soil, zones=zones)
prescription = engine.generate_prescription(
    crop="corn",
    nutrient="nitrogen",
    target_yield_bu_ac=180,
    base_rate_lb_ac=120,
    price_per_ton=450.00,
    cost_per_lb_n=0.55,
)
print(f"\nPrescription generated: {prescription.total_area_acres:.1f} acres")
print(f"Average rate: {prescription.avg_rate:.1f} lb/ac")
print(f"Estimated cost: ${prescription.total_cost:.2f}")
print(f"Projected revenue: ${prescription.projected_revenue:.2f}")
```

```python
# Yield map analysis
mapper = YieldMapper()
yield_data = mapper.import_yield_file("yield_2024.csv")
stats = mapper.compute_statistics(yield_data)
print(f"Field average: {stats.mean:.1f} bu/ac")
print(f"Std deviation: {stats.std_dev:.1f} bu/ac")
print(f"Coefficient of variation: {stats.cv:.1%}")

# Export prescription
prescription.export_shapefile("prescription_n_2024.shp")
prescription.export_iso_xml("prescription_n_2024.xml")
prescription.export_jdoc("prescription_n_2024.jdoc")  # John Deere format
```

## Best Practices

- Collect soil samples on a consistent grid (2.5-acre or 5-acre) or zone-based pattern each year
- Calibrate yield monitors annually using known weights from certified scales
- Use at least 3-5 years of yield data for reliable management zone delineation
- Apply the 4R nutrient stewardship: Right source, Right rate, Right time, Right place
- Validate prescription maps against actual soil test results before application
- Document all field operations for USDA compliance and crop insurance purposes
- Use RTK GPS (sub-inch accuracy) for guidance lines in controlled traffic farming
- Consider drainage patterns and topography when creating management zones
- Account for field heterogeneity in economic models — not all zones justify VRT investment
- Store all geospatial data in standardized formats (GeoJSON, Shapefile) for equipment interoperability

## Related Modules

- **crop-monitoring** — Real-time crop health monitoring via satellite and drone imagery
- **soil-analysis** — Detailed soil composition analysis and interpretation
- **agricultural-iot** — IoT sensor network deployment for field-level data collection
- **supply-chain** — Farm-to-market supply chain tracking and logistics
- **data-science** → **statistical-analysis** — Statistical methods for yield data analysis

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

### Multi-Year Yield Trend Analysis
```python
from precision_farming import YieldTrendAnalyzer

analyzer = YieldTrendAnalyzer(field_id="FIELD-001")
trend = analyzer.analyze(
    years=["2019", "2020", "2021", "2022", "2023", "2024"],
    metric="yield_bu_ac",
)
print(f"5-year average: {trend.avg_yield:.1f} bu/ac")
print(f"Trend direction: {trend.direction}")  # 'improving', 'declining', 'stable'
print(f"Year-over-year change: {trend.yoy_change_pct:.1f}%")
print(f"Std deviation: {trend.std_dev:.1f} bu/ac")
print(f"Coefficient of variation: {trend.cv:.1%}")

# Identify problem zones
zones = analyzer.identify_declining_zones(threshold=-0.05)
for zone in zones:
    print(f"  Zone {zone.id}: {zone.trend_pct:.1f}% avg annual decline")
```

### Variable-Rate Seeding Optimization
```python
from precision_farming import SeedingOptimizer

optimizer = SeedingOptimizer(crop="corn")
seeding_map = optimizer.generate_map(
    soil_data=soil,
    yield_history=yield_data,
    target_population=34000,  # seeds per acre
    hybrid="DKC64-69",
    seed_cost_per_unit=3.50,
    expected_price=4.50,
)
print(f"Seeding map: {seeding_map.variable_rate_range[0]}-{seeding_map.variable_rate_range[1]} seeds/ac")
print(f"Optimal seed cost: ${seeding_map.total_cost:.2f}")
print(f"Projected revenue: ${seeding_map.projected_revenue:.2f}")
print(f"ROI improvement: {seeding_map.roi_improvement_pct:.1f}%")
```

### Prescription Map Visualization
```python
from precision_farming import PrescriptionVisualizer

viz = PrescriptionVisualizer(prescription)
viz.plot_rate_map(
    title="Variable-Rate Nitrogen Prescription 2024",
    color_scheme="RdYlGn",
    show_boundaries=True,
    show_elevation=True,
    output_path="prescription_map.png",
)
viz.plot_comparison(
    yield_map_2023,
    prescription,
    title="Yield vs Prescription Overlay",
    output_path="comparison.png",
)
```

### Soil Sampling Strategies
```python
from precision_farming import SamplingStrategy

strategy = SamplingStrategy(field_id="FIELD-001")

# Grid sampling
grid = strategy.grid_sampling(
    grid_spacing_ft=300,  # 300-foot grid
    depth_in=8,
    num_cores_per_point=15,
)
print(f"Grid sample points: {grid.num_points}")
print(f"Recommended lab tests: {grid.tests_recommended}")

# Zone-based sampling
zone_samples = strategy.zone_sampling(
    zones=zones,
    cores_per_zone=20,
    depth_in=8,
)
print(f"Zone sample points: {zone_samples.num_points}")
```

### GPS Guidance Line Management
```python
from precision_farming import GuidanceLines

guidance = GuidanceLines(field_id="FIELD-001")

# A-B lines
ab_line = guidance.create_ab_line(
    point_a=(38.0100, -98.0100),
    point_b=(38.0100, -98.0200),
    heading_degrees=270.0,
    implement_width_ft=90,
    overlap_ft=0,
)

# Curved path for irregular fields
curved = guidance.create_curved_path(
    boundary=field_boundary,
    implement_width_ft=90,
    curve_smoothing=0.8,
)

# Export to John Deere Operations Center
guidance.export_jdoc([ab_line, curved], filename="guidance_lines_2024.jdoc")
```

### Economic Optimization
```python
from precision_farming import EconomicOptimizer

econ = EconomicOptimizer()

# Optimize nitrogen rates based on economic return
result = econ.optimize_n_rate(
    field_data=field,
    n_cost_per_lb=0.55,
    corn_price_per_bu=4.50,
    yield_response_model="quadratic-plateau",
    risk_aversion=0.5,  # 0=profit-maximizing, 1=risk-averse
)
print(f"Economic optimal N rate: {result.optimal_n_lb_ac:.0f} lb/ac")
print(f"Marginal return: ${result.marginal_return_per_lb:.2f}/lb N")
print(f"Total profit: ${result.total_profit_per_acre:.2f}/ac")
print(f"90% confidence interval: {result.ci_low:.0f}-{result.ci_high:.0f} lb/ac")
```

### Drainage and Topography Analysis
```python
from precision_farming import TopographyAnalyzer

topo = TopographyAnalyzer(dem_resolution_ft=3)
analysis = topo.analyze_field(field_boundary)

print(f"Field elevation range: {analysis.min_elev:.1f}-{analysis.max_elev:.1f} ft")
print(f"Slope range: {analysis.min_slope:.1f}-{analysis.max_slope:.1f}%")
print(f"Average slope: {analysis.avg_slope:.1f}%")

# Generate drainage zones
drainage_zones = topo.classify_drainage(
    soil_texture="silt_loam",
    slope_thresholds=[1.0, 3.0, 5.0],
)
for zone in drainage_zones:
    print(f"  {zone.classification}: {zone.area_pct:.1f}% of field")

# Create surface wetness index
wetness = topo.compute_wetness_index()
wetness.export_tif("wetness_index.tif")
```

### Equipment Calibration
```python
from precision_farming import EquipmentCalibrator

calibrator = EquipmentCalibrator()

# Calibrate yield monitor
yield_cal = calibrator.calibrate_yield_monitor(
    monitor_readings=[180, 175, 185, 170],
    scale_weights=[18200, 17500, 18600, 16800],
    grain_bushel_weight=56,  # lb/bu for corn
)
print(f"Calibration R-squared: {yield_cal.r_squared:.4f}")
print(f"Mean bias: {yield_cal.mean_bias_pct:.1f}%")
print(f"Correction factor: {yield_cal.correction_factor:.4f}")

# Calibrate variable-rate controller
vr_cal = calibrator.calibrate_vr_controller(
    target_rates=[100, 120, 140, 160, 180],
    actual_rates=[98, 122, 138, 163, 178],
)
print(f"VR accuracy: {vr_cal.accuracy_pct:.1f}%")
print(f"CV across rates: {vr_cal.cv_pct:.1f}%")
```

### Data Export Formats
```python
from precision_farming import ExportManager

exporter = ExportManager(prescription)

# Shapefile export
exporter.to_shapefile("prescription.shp", crs="EPSG:4326")

# ISO-XML (ISO 11783)
exporter.to_iso_xml("prescription.xml", task_controller_version="3")

# John Deere Operations Center
exporter.to_jdoc("prescription.jdoc", field_id="FIELD-001")

# Climate FieldView
exporter.to_climate_fieldview("prescription.csv", format="fieldview")

# Ag Leader SMS
exporter.to_agleader_sms("prescription.ald", version="12")

# Generic GeoJSON
exporter.to_geojson("prescription.geojson")
```

### Zone Delineation Methods
| Method | Input Data | Best For | Resolution |
|--------|-----------|----------|------------|
| K-means clustering | Soil properties | General purpose | Medium |
| EC mapping | Electrical conductivity | Clay/texture zones | High |
| Yield history | 3-5 years yield data | Performance zones | High |
| NDVI clustering | Satellite imagery | Crop health zones | Medium |
| Manual delineation | Soil map + experience | Complex fields | Custom |
| Fuzzy c-means | Multi-source data | Gradual transitions | Medium |
| Principal component | Multi-variable | Variable reduction | Medium |

### Common GPS Coordinate Systems
| System | EPSG | Use Case |
|--------|------|----------|
| WGS 84 | 4326 | Global, GPS default |
| UTM Zone 14N | 32614 | Central US (TX to ND) |
| NAD83 State Plane | varies | US state-level precision |
| ETRS89 | 4258 | European applications |
| GDA2020 | 7842 | Australian applications |

### Yield Monitor Data Cleaning
```python
from precision_farming import YieldDataCleaner

cleaner = YieldDataCleaner()
clean_data = cleaner.clean(
    raw_data=yield_data,
    remove_zeros=True,
    remove_outliers=True,
    outlier_method="mad",  # median absolute deviation
    outlier_threshold=3.0,
    smooth=True,
    smoothing_window=5,
    correct_for_moisture=True,
    grain_flow_calibration=0.98,
    header_flow_calibration=1.02,
)
print(f"Raw points: {len(raw_data)}")
print(f"Cleaned points: {len(clean_data)}")
print(f"Points removed: {len(raw_data) - len(clean_data)} ({cleaner.removal_pct:.1f}%)")
```

### Prescription Validation Rules
```python
from precision_farming import PrescriptionValidator

validator = PrescriptionValidator()
issues = validator.validate(prescription)

for issue in issues:
    print(f"  [{issue.severity}] {issue.message}")
    print(f"    Location: ({issue.lat:.6f}, {issue.lon:.6f})")
    print(f"    Recommendation: {issue.recommendation}")

# Common validation checks:
# - Rate within equipment capability range
# - Rates are non-negative
# - Zones are contiguous
# - Boundary matches field boundary
# - CRS is correct
# - No gaps between application zones
# - Rate changes are within acceptable step size
```

### Soil Zone Classification Thresholds
| Property | Low | Medium | High | Very High |
|----------|-----|--------|------|-----------|
| Nitrogen (ppm) | < 10 | 10-25 | 25-50 | > 50 |
| Phosphorus (ppm) | < 15 | 15-30 | 30-60 | > 60 |
| Potassium (ppm) | < 100 | 100-175 | 175-250 | > 250 |
| pH | < 5.5 | 5.5-6.2 | 6.2-7.0 | > 7.0 |
| Organic Matter (%) | < 1.5 | 1.5-3.0 | 3.0-5.0 | > 5.0 |
| CEC (meq/100g) | < 5 | 5-15 | 15-25 | > 25 |

### Integration with External Platforms
```python
# Climate FieldView integration
from precision_farming import ClimateFieldView

cfv = ClimateFieldView(api_key="your-api-key")
cfv.upload_prescription(prescription, field_id="CFV-FIELD-001")
cfv.sync_yield_data(field_id="CFV-FIELD-001", year=2024)

# John Deere Operations Center
from precision_farming import JohnDeereOpsCenter

jd = JohnDeereOpsCenter(oauth_token="your-token")
jd.upload_field_boundary(field_boundary, org_id="ORG-001")
jd.upload_prescription(prescription, field_id="JD-FIELD-001")
jd.download_yield_data(field_id="JD-FIELD-001", year=2024)

# Ag Leader SMS
from precision_farming import AgLeaderSMS

sms = AgLeaderSMS(data_path="C:\\AgLeader\\SMS")
sms.import_prescription(prescription, field_name="North 160")
sms.export_yield_data(year=2024, format="agf")
```

### Multi-Season Planning
```python
from precision_farming import SeasonPlanner

planner = SeasonPlanner(field_id="FIELD-001")

# Generate crop rotation recommendation
rotation = planner.recommend_rotation(
    current_crop="corn",
    soil_data=soil,
    market_prices=prices,
    sustainability_score=True,
)
print(f"Recommended rotation: {rotation.sequence}")
print(f"Expected 5-year profit: ${rotation.projected_profit:.0f}/ac")
print(f"Sustainability score: {rotation.sustainability:.0f}/100")

# Generate season plan
plan = planner.create_season_plan(
    crop="corn",
    planting_window=("2025-04-15", "2025-05-15"),
    target_yield=200,
)
print(f"Pre-plant fertilizer: {plan.preplant_fertilizer}")
print(f"Side-dress timing: {plan.side_dress_date}")
print(f"Estimated harvest date: {plan.harvest_date}")
```

### Common Crop Parameters
| Crop | Target Pop (seeds/ac) | N Rate (lb/ac) | P2O5 (lb/ac) | K2O (lb/ac) |
|------|----------------------|-----------------|---------------|--------------|
| Corn | 32,000-36,000 | 150-200 | 60-90 | 80-120 |
| Soybeans | 130,000-150,000 | 0-20 | 40-80 | 60-100 |
| Wheat | 1.2-1.5 M | 80-120 | 40-60 | 40-60 |
| Cotton | 32,000-40,000 | 60-80 | 40-60 | 60-80 |
| Sorghum | 75,000-90,000 | 80-120 | 40-60 | 40-60 |

### RTK GPS Base Station Setup
```python
from precision_farming import RTKBaseStation

base = RTKBaseStation(
    location=(38.0100, -98.0100),
    antenna_height_m=2.0,
    correction_source="NTRIP",  # or 'radio', 'satellite'
    ntrip caster="rtk2go.com",
    ntrip_mountpoint="YOUR_CASTER",
)
base.start()
print(f"Base status: {base.status}")
print(f"Correction age: {base.correction_age_s:.1f}s")
print(f"Position accuracy: {base.accuracy_cm:.1f}cm")
```

### Yield Map Interpolation
```python
from precision_farming import YieldInterpolator

interpolator = YieldInterpolator()

# Kriging interpolation
kriged = interpolator.kriging(
    yield_data,
    grid_spacing_m=10,
    variogram_model="spherical",
    search_radius_m=50,
)
kriged.export_tif("yield_kriged.tif")

# Inverse distance weighting
idw = interpolator.idw(
    yield_data,
    grid_spacing_m=10,
    power=2,
    search_points=12,
)
idw.export_tif("yield_idw.tif")
```

### Field Boundary Management
```python
from precision_farming import FieldBoundary

boundary = FieldBoundary.from_shapefile("field_boundary.shp")
print(f"Field area: {boundary.area_acres:.1f} acres")
print(f"Perimeter: {boundary.perimeter_ft:.0f} ft")
print(f"Compactness: {boundary.compactness_ratio:.3f}")

# Simplify boundary for equipment
simplified = boundary.simplify(tolerance_ft=10)
print(f"Original vertices: {boundary.num_vertices}")
print(f"Simplified vertices: {simplified.num_vertices}")

# Generate buffer zones
buffer = boundary.create_buffer(width_ft=30, side="inside")
buffer.export_shapefile("exclusion_zone.shp")
```

### Controlled Traffic Farming
```python
from precision_farming import ControlledTraffic

ctf = ControlledTraffic(field_id="FIELD-001")
trafficked_pct = ctf.calculate_trafficked_area(
    wheel_spacing_ft=120,  # 30-foot tramlines
    pass_width_ft=120,
    implement_width_ft=90,
)
print(f"Trafficked area: {trafficked_pct:.1f}% of field")
print(f"Potential yield gain from CTF: {ctf.estimated_yield_gain_pct:.1f}%")
```

### Nutrient Loss Risk Assessment
```python
from precision_farming import NutrientLossRisk

risk = NutrientLossRisk()
assessment = risk.assess(
    nitrogen_applied_lb_ac=180,
    soil_type="silt_loam",
    slope_pct=2.0,
    rainfall_30day_in=4.5,
    drainage_type="poorly_drained",
    cover_crop=False,
)
print(f"N loss risk: {assessment.risk_level}")  # 'low', 'medium', 'high'
print(f"Estimated N lost: {assessment.estimated_loss_lb_ac:.0f} lb/ac")
print(f"Recommendation: {assessment.recommendation}")
```

### Data Backup and Recovery
```python
from precision_farming import DataBackup

backup = DataBackup(base_path="D:\\precision_farm_data")

# Backup all field data
backup.backup_field(
    field_id="FIELD-001",
    include=["yield", "soil", "prescriptions", "imagery", "guidance"],
    destination="s3://farm-backups/2024/",
    compress=True,
)
print(f"Backup size: {backup.last_backup_size_gb:.2f} GB")

# Restore from backup
backup.restore_field(
    field_id="FIELD-001",
    source="s3://farm-backups/2024/",
    target_path="D:\\restored_data",
)
```

### Compliance Reporting
```python
from precision_farming import ComplianceReport

report = ComplianceReport(field_id="FIELD-001")

# NRCS EQIP reporting
eqip = report.generate_eqip_report(
    practice_code="590",  # Nutrient Management
    fiscal_year=2024,
    field_acres=160,
    nutrient_plan=nutrient_plan,
)
eqip.export_pdf("eqip_report_2024.pdf")

# Conservation practice documentation
conservation = report.generate_conservation_practices(
    practices=["cover_crops", "nutrient_management", "conservation_tillage"],
    year=2024,
)
conservation.export_pdf("conservation_report_2024.pdf")
```

---

## Return format (required)

Your FINAL assistant message — what the spawning agent will receive — MUST start with this header block:

  **Status**: success | partial | failed | blocked
  **Summary**: <one sentence describing what happened>

After the header, include the actual deliverable (whatever the task asked for in its prompt).

If applicable, also include below the deliverable:

  **Files touched**: <comma-separated paths or "(none)">
  **Findings worth promoting**: <bullet list of cross-task transferable facts; "(none)" if just routine work>

This format lets the spawning agent and the checkpoint writer extract your progress without parsing free-form prose. Do NOT precede the header with an introduction — your final message must start with "**Status**:".
