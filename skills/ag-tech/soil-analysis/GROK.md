---
name: "soil-analysis"
category: "ag-tech"
version: "2.0.0"
tags: ["agriculture", "soil-analysis", "nutrients", "ph", "cec", "soil-testing", "laboratory"]
---

# Soil Analysis

## Overview

Comprehensive soil analysis and interpretation toolkit for agricultural soil testing, nutrient management planning, and soil health assessment. This module processes laboratory soil test results (Mehlich-3, Bray-1, DTPA extraction methods), calculates nutrient recommendations using university extension algorithms, evaluates soil health indicators (organic matter, microbial activity, aggregate stability), and generates field-level nutrient management plans. Supports integration with NRCS soil survey data, soil health card programs, and conservation practice planning.

## Core Capabilities

- **Soil Test Interpretation**: Analyzes results from standard laboratory methods (Mehlich-3, Bray-1, Ammonium Acetate, DTPA) with crop-specific sufficiency ranges
- **Nutrient Recommendation Engine**: Calculates N, P, K, S, lime, and micronutrient recommendations using land-grant university algorithms (MITSCH, PSIAC, or custom)
- **Soil Health Assessment**: Evaluates biological, chemical, and physical soil health indicators with scoring against regional benchmarks
- **pH Management**: Calculates lime requirements, acidifier rates, and buffer pH adjustments for target pH zones
- **Organic Matter Analysis**: Tracks organic matter trends, carbon sequestration potential, and decomposition rates
- **Cation Exchange Capacity**: Interprets CEC for nutrient-holding capacity, soil texture inference, and base saturation calculations
- **Satellite Soil Survey Integration**: Imports USDA NRCS Web Soil Survey data for field characterization
- **Multi-Field Comparison**: Compares soil test results across fields, years, and management zones

## Usage

```python
from soil_analysis import (
    SoilTestLab, NutrientRecommendation, SoilHealthIndex, pHManager
)

# Load laboratory results
lab = SoilTestLab.from_file("soil_test_results.csv")
print(f"Loaded {len(lab.samples)} soil samples")

for sample in lab.samples[:3]:
    print(f"\n  Sample {sample.sample_id}:")
    print(f"    pH: {sample.ph:.1f} (buffer: {sample.buffer_ph:.1f})")
    print(f"    P: {sample.phosphorus_ppm:.1f} ppm ({sample.p_status})")
    print(f"    K: {sample.potassium_ppm:.1f} ppm ({sample.k_status})")
    print(f"    OM: {sample.organic_matter_pct:.1f}% ({sample.om_status})")
    print(f"    CEC: {sample.cec:.1f} meq/100g")

# Calculate nutrient recommendations
recommender = NutrientRecommendation(crop="corn", target_yield=180)
for sample in lab.samples[:5]:
    rec = recommender.calculate(sample)
    print(f"\n  {sample.sample_id} Recommendations:")
    print(f"    N: {rec.nitrogen_lb_ac:.0f} lb/ac")
    print(f"    P2O5: {rec.phosphorus_lb_ac:.0f} lb/ac")
    print(f"    K2O: {rec.potassium_lb_ac:.0f} lb/ac")
    print(f"    Lime: {rec.lime_tons_ac:.2f} tons/ac")

# Soil health assessment
health = SoilHealthIndex()
score = health.evaluate(
    organic_matter_pct=3.5,
    ph=6.5,
    cec=18.0,
    microbial_activity=0.75,
    aggregate_stability=65.0,
    infiltration_rate=1.5,
)
print(f"\nSoil Health Score: {score.total_score:.0f}/100")
print(f"  Chemical: {score.chemical_score:.0f}/100")
print(f"  Physical: {score.physical_score:.0f}/100")
print(f"  Biological: {score.biological_score:.0f}/100")
```

```python
# pH management
ph_mgr = pHManager()
current_ph = 5.8
target_ph = 6.5
buffer_ph = 6.8
soil_type = "silt_loam"

lime_rate = ph_mgr.calculate_lime(current_ph, target_ph, buffer_ph, soil_type)
print(f"\nLime needed: {lime_rate.tons_per_acre:.2f} tons/ac")
print(f"  Product: {lime_rate.product}")
print(f"  Effective calcium carbonate equivalent: {lime_rate.ecce:.0f}%")
```

## Best Practices

- Take soil samples at consistent depths (0-8" for standard, 0-24" for deep sampling) and times of year
- Use 15-20 cores per sample zone, composited and mixed thoroughly before sending to lab
- Choose the appropriate extraction method for your region (Mehlich-3 is standard in the Eastern US)
- Interpret P and K levels relative to crop-specific critical levels, not just absolute values
- Apply lime 6-12 months before the crop needs the pH adjustment — lime reacts slowly
- Monitor organic matter trends annually — a 0.1% change over 5 years indicates a significant trend
- Use CEC to calibrate fertilizer rates — high-CEC soils need more nutrients to change test levels
- Consider soil texture when interpreting results — sandy soils have naturally low CEC and OM
- Track soil test results over time to evaluate the effectiveness of management practices
- Combine laboratory results with field observations for a complete soil health picture

## Related Modules

- **precision-farming** — Apply soil analysis results to variable-rate prescriptions
- **crop-monitoring** — Correlate soil conditions with crop health indicators
- **agricultural-iot** — Deploy soil sensors for continuous monitoring
- **supply-chain** — Track soil amendments from purchase to application
- **data-science** → **statistical-analysis** — Statistical methods for soil data analysis

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

### Nutrient Interaction Matrix
| Nutrient | N | P | K | S | Ca | Mg | Fe | Mn | Zn | Cu | B |
|----------|---|---|---|---|----|----|----|----|----|----|----|
| **N** | - | + | + | + | - | - | + | + | + | + | + |
| **P** | + | - | + | + | - | - | - | - | - | - | - |
| **K** | + | + | - | - | - | - | - | - | - | - | - |
| **S** | + | + | - | - | - | - | - | - | - | - | - |
| **Ca** | - | - | - | - | - | + | - | - | - | - | - |
| **Mg** | - | - | - | - | + | - | - | - | - | - | - |
| **Fe** | + | - | - | - | - | - | - | + | + | + | - |
| **Mn** | + | - | - | - | - | - | + | - | + | + | - |
| **Zn** | + | - | - | - | - | - | + | + | - | + | - |
| **Cu** | + | - | - | - | - | - | + | + | + | - | - |
| **B** | + | - | - | - | - | - | - | - | - | - | - |

Legend: + = synergistic, - = antagonistic, blank = no significant interaction

### Soil Texture Classification
```python
from soil_analysis import SoilTextureClassifier

classifier = SoilTextureClassifier()

# Classify soil texture from particle size analysis
texture = classifier.classify(
    sand_pct=40,
    silt_pct=45,
    clay_pct=15,
)
print(f"Soil texture: {texture.name}")  # 'Sandy Clay Loam'
print(f"USDA triangle position: ({texture.sand_pct}, {texture.silt_pct}, {texture.clay_pct})")
print(f"Drainage class: {texture.drainage_class}")
print(f"Water holding capacity: {texture.whc_class}")
print(f"CEC range: {texture.cec_range}")
```

### Lime Requirement Calculation
```python
from soil_analysis import LimeCalculator

calc = LimeCalculator()

# Multiple lime requirement methods
results = {
    "adams_evans": calc.adams_evans(
        buffer_ph=6.8,
        target_ph=6.5,
        soil_texture="silt_loam",
    ),
    "sikora": calc.sikora(
        buffer_ph=6.8,
        target_ph=6.5,
        cec=18.0,
    ),
    "mekaru": calc.mekaru(
        buffer_ph=6.8,
        target_ph=6.5,
        organic_matter_pct=3.5,
    ),
}

for method, result in results.items():
    print(f"{method}: {result.lime_tons_ac:.2f} tons/ac (ECCE={result.ecce:.0f}%)")
```

### Base Saturation Analysis
```python
from soil_analysis import BaseSaturation

bs = BaseSaturation()

# Calculate base saturation from cation data
saturation = bs.calculate(
    calcium_ppm=1200,
    magnesium_ppm=180,
    potassium_ppm=150,
    sodium_ppm=25,
    cec=18.0,
)
print(f"Ca saturation: {saturation.ca_pct:.1f}% (ideal: 60-80%)")
print(f"Mg saturation: {saturation.mg_pct:.1f}% (ideal: 10-30%)")
print(f"K saturation: {saturation.k_pct:.1f}% (ideal: 2-5%)")
print(f"Na saturation: {saturation.na_pct:.1f}% (ideal: <2%)")
print(f"CEC saturation: {saturation.total_base_pct:.1f}%")
print(f"pH-buffer capacity: {saturation.buffer_capacity}")
```

### Soil Organic Carbon Dynamics
```python
from soil_analysis import OrganicCarbonModel

model = OrganicCarbonModel()

# Model carbon sequestration under different practices
scenarios = {
    "conventional_till": model.simulate(
        initial_om_pct=2.5,
        practices=["conventional_tillage", "no_cover_crop"],
        years=10,
    ),
    "no_till_cover": model.simulate(
        initial_om_pct=2.5,
        practices=["no_tillage", "cover_crops", "compost"],
        years=10,
    ),
}

for name, result in scenarios.items():
    print(f"\n{name}:")
    print(f"  Final OM: {result.final_om_pct:.2f}%")
    print(f"  Change: {result.om_change_pct:+.2f}%")
    print(f"  C sequestered: {result.carbon_sequestered_tons_ac:.2f} tons/ac")
```

### Mehlich-3 vs Bray-1 Comparison
| Nutrient | Mehlich-3 | Bray-1 | Use Case |
|----------|-----------|--------|----------|
| P | Universal | Acid soils only | Mehlich-3 preferred in most regions |
| K | Same | Same | Both equivalent |
| Ca | Yes | No | Mehlich-3 only |
| Mg | Yes | No | Mehlich-3 only |
| Zn | Yes | No | Mehlich-3 only |
| Fe | Yes | No | Mehlich-3 only |
| Mn | Yes | No | Mehlich-3 only |
| Cu | Yes | No | Mehlich-3 only |
| B | No | No | Hot water extraction |

### Soil Health Indicators
| Indicator | Measurement | Score Range | Importance |
|-----------|-------------|-------------|------------|
| Organic Matter (%) | Loss on ignition | 0-100 | High |
| Microbial Biomass | PLFA analysis | 0-100 | High |
| Aggregate Stability | Wet sieve | 0-100 | High |
| Infiltration Rate | Double ring infiltrometer | 0-100 | Medium |
| Water Stable Aggregates | Wet sieve | 0-100 | High |
| Respiration | CO2 burst | 0-100 | High |
| Active Carbon | POXC | 0-100 | Medium |
| Bulk Density | Core method | 0-100 | Medium |
| Compaction | Penetrometer | 0-100 | Medium |
| Earthworm Count | Hand sorting | 0-100 | Low |

### CEC Interpretation
```python
from soil_analysis import CECInterpreter

interp = CECInterpreter()

# Interpret CEC values
result = interp.interpret(
    cec=18.0,
    soil_texture="silt_loam",
    region="midwest_us",
)
print(f"CEC class: {result.cec_class}")  # 'high', 'medium', 'low'
print(f"Nutrient holding capacity: {result.holding_capacity}")
print(f"Fertilizer efficiency: {result.fertilizer_efficiency}")
print(f"Lime reactivity: {result.lime_reactivity}")
print(f"Recommended sampling frequency: {result.sampling_frequency}")
```

### Soil Test Result Ranges
| Nutrient | Very Low | Low | Medium | High | Very High |
|----------|----------|-----|--------|------|-----------|
| P (Mehlich-3, ppm) | < 15 | 15-30 | 30-60 | 60-100 | > 100 |
| K (ppm) | < 100 | 100-175 | 175-250 | 250-350 | > 350 |
| S (ppm) | < 6 | 6-12 | 12-20 | 20-30 | > 30 |
| Zn (DTPA, ppm) | < 0.5 | 0.5-1.0 | 1.0-2.0 | 2.0-4.0 | > 4.0 |
| Mn (DTPA, ppm) | < 1.0 | 1.0-2.0 | 2.0-5.0 | 5.0-20 | > 20 |
| Fe (DTPA, ppm) | < 2.0 | 2.0-4.5 | 4.5-10 | 10-25 | > 25 |
| Cu (DTPA, ppm) | < 0.1 | 0.1-0.2 | 0.2-0.5 | 0.5-1.0 | > 1.0 |
| B (hot water, ppm) | < 0.3 | 0.3-0.6 | 0.6-1.0 | 1.0-2.0 | > 2.0 |

### Micronutrient Deficiency Symptoms
```python
from soil_analysis import DeficiencyDiagnosis

diag = DeficiencyDiagnosis()

# Diagnose deficiency from visual symptoms
result = diag.diagnose(
    crop="corn",
    symptoms=["interveinal chlorosis", "yellowing between veins"],
    affected_leaves="lower",
    growth_stage="V8",
)
print(f"Likely deficiency: {result.nutrient}")  # 'magnesium'
print(f"Confidence: {result.confidence:.1%}")
print(f"Confirmatory test: {result.confirmatory_test}")
print(f"Recommended treatment: {result.treatment}")
print(f"Application method: {result.application_method}")
```

### Nutrient Removal Rates
| Crop | Yield | N | P2O5 | K2O | S | Ca | Mg |
|------|-------|---|------|-----|---|----|----|
| Corn | 200 bu/ac | 164 lb | 72 lb | 50 lb | 24 lb | 14 lb | 16 lb |
| Soybean | 50 bu/ac | 180 lb | 40 lb | 76 lb | 24 lb | 30 lb | 20 lb |
| Wheat | 80 bu/ac | 88 lb | 38 lb | 26 lb | 12 lb | 8 lb | 8 lb |
| Cotton | 1000 lb lint | 100 lb | 36 lb | 44 lb | 12 lb | 10 lb | 12 lb |
| Alfalfa | 6 tons | 336 lb | 54 lb | 276 lb | 36 lb | 240 lb | 36 lb |

### Soil Sampling Best Practices
```python
from soil_analysis import SamplingProtocol

protocol = SamplingProtocol()

# Generate sampling plan
plan = protocol.create_plan(
    field_id="FIELD-001",
    field_acres=160,
    method="zone",
    management_zones=zones,
    depth_in=8,
    cores_per_zone=20,
)
print(f"Total sample points: {plan.num_points}")
print(f"Total cores to pull: {plan.total_cores}")
print(f"Lab analysis cost: ${plan.estimated_cost:.2f}")
print(f"Recommended lab tests: {plan.tests_recommended}")

# Generate field map with sample points
plan.export_map("sampling_plan_2024.png")
plan.export_csv("sampling_points_2024.csv")
```

### Water Quality Assessment
```python
from soil_analysis import WaterQuality

wq = WaterQuality()

# Analyze irrigation water quality
result = wq.analyze(
    ph=7.2,
    ec_dsm=1.5,
    sodium_ppm=50,
    calcium_ppm=40,
    magnesium_ppm=15,
    bicarbonate_ppm=150,
    chloride_ppm=30,
    sulfate_ppm=50,
)
print(f"SAR: {result.sar:.2f} (ideal < 6)")
print(f"EC class: {result.ec_class}")  # 'low', 'medium', 'high', 'very_high'
print(f"Suitability: {result.suitability}")  # 'good', 'marginal', 'poor'
print(f"Potential issues: {result.issues}")
print(f"Management recommendations: {result.recommendations}")
```

### Soil Temperature Modeling
```python
from soil_analysis import SoilTempModel

model = SoilTempModel()

# Predict soil temperature at depth
temp = model.predict(
    air_temp_f=85,
    day_of_year=180,
    latitude=38.0,
    soil_type="silt_loam",
    residue_cover=True,
    tillage="no-till",
)
print(f"Soil temp at 2\": {temp.depth_2_f:.0f}F")
print(f"Soil temp at 4\": {temp.depth_4_f:.0f}F")
print(f"Soil temp at 8\": {temp.depth_8_f:.0f}F")
print(f"Germination rate: {temp.germination_rate:.0f}%")
```

### Nutrient Banding vs Broadcast
```python
from soil_analysis import ApplicationMethod

method = ApplicationMethod()

# Compare application methods
comparison = method.compare(
    nutrient="P2O5",
    rate_lb_ac=60,
    soil_ph=6.5,
    crop="corn",
    soil_texture="silt_loam",
)
print(f"Broadcast: {comparison.broadcast.efficiency:.0f}% utilization")
print(f"Band (2x2): {comparison.banded_2x2.efficiency:.0f}% utilization")
print(f"Band (4x4): {comparison.banded_4x4.efficiency:.0f}% utilization")
print(f"Deep band: {comparison.deep_band.efficiency:.0f}% utilization")
print(f"Recommended: {comparison.recommended_method}")
```

### Soil Profile Analysis
```python
from soil_analysis import SoilProfile

profile = SoilProfile(field_id="FIELD-001")

# Analyze multi-depth sampling
results = profile.analyze_depths(
    depths=[
        {"label": "0-8in", "start_in": 0, "end_in": 8},
        {"label": "8-16in", "start_in": 8, "end_in": 16},
        {"label": "16-24in", "start_in": 16, "end_in": 24},
        {"label": "24-36in", "start_in": 24, "end_in": 36},
    ],
    data_file="deep_samples.csv",
)
for depth_result in results:
    print(f"\n  {depth_result.label}:")
    print(f"    pH: {depth_result.ph:.1f}")
    print(f"    P: {depth_result.phosphorus:.0f} ppm")
    print(f"    K: {depth_result.potassium:.0f} ppm")
    print(f"    OM: {depth_result.organic_matter:.1f}%")
```

### Compaction Assessment
```python
from soil_analysis import CompactionAnalyzer

analyzer = CompactionAnalyzer()

# Analyze penetrometer data
result = analyzer.analyze(
    penetrometer_readings=[
        {"depth_in": 0, "pressure_psi": 50},
        {"depth_in": 3, "pressure_psi": 120},
        {"depth_in": 6, "pressure_psi": 280},
        {"depth_in": 9, "pressure_psi": 350},
        {"depth_in": 12, "pressure_psi": 200},
        {"depth_in": 18, "pressure_psi": 150},
    ],
    soil_texture="silt_loam",
    moisture_status="field_capacity",
)
print(f"Compaction layer: {result.compaction_depth_in} inches")
print(f"Peak resistance: {result.peak_psi} PSI")
print(f"Severity: {result.severity}")  # 'none', 'mild', 'moderate', 'severe'
print(f"Recommendation: {result.recommendation}")
```

### Lab Submission Form Generator
```python
from soil_analysis import LabSubmissionForm

form = LabSubmissionForm()

# Generate submission form
form.add_samples(
    samples=lab_samples,
    lab="Midwest Laboratories",
    analysis_package="Comprehensive Soil Test",
    special_instructions="Include organic matter and CEC",
)
form.export_pdf("submission_form_2024.pdf")
form.export_csv("submission_data_2024.csv")

# Print barcode labels
form.print_labels(
    label_format="avery_5160",
    include_barcode=True,
)
```

### Trend Analysis Over Time
```python
from soil_analysis import TrendAnalyzer

trend = TrendAnalyzer(field_id="FIELD-001")

# Analyze nutrient trends
analysis = trend.analyze(
    metric="phosphorus_ppm",
    years=[2019, 2020, 2021, 2022, 2023, 2024],
    method="linear_regression",
)
print(f"5-year trend: {analysis.slope:+.1f} ppm/year")
print(f"Trend significance: {analysis.p_value:.4f}")
print(f"R-squared: {analysis.r_squared:.3f}")
print(f"Interpretation: {analysis.interpretation}")
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
