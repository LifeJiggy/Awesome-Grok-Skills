---
name: "green-it"
category: "sustainability"
version: "1.0.0"
tags: ["sustainability", "green-it", "data-center", "e-waste", "it-infra"]
---

# Green IT

## Overview

Green IT refers to the environmentally sustainable design, manufacture, use, and disposal of information technology systems and infrastructure. This module provides a comprehensive toolkit for conducting IT infrastructure sustainability audits, optimizing Data Center Power Usage Effectiveness (PUE), tracking electronic waste (e-waste) through the full equipment lifecycle, managing hardware refresh cycles, and ensuring compliance with Energy Star and EPEAT standards. As organizations increasingly depend on digital infrastructure, the environmental impact of IT operations — from the energy consumed by servers to the rare earth minerals embedded in networking equipment — demands systematic measurement and reduction strategies.

The module covers the complete IT sustainability lifecycle: procurement (evaluating environmental credentials of hardware vendors and products), operation (optimizing power, cooling, and resource utilization in data centers and offices), and end-of-life (tracking equipment through refurbishment, recycling, and responsible disposal channels). It includes tools for computing IT carbon footprints per department, per user, or per workload, enabling granular accountability and targeted reduction efforts. The PUE optimization component models airflow, cooling efficiency, and equipment placement to identify waste reduction opportunities without compromising reliability.

Green IT is not merely an environmental initiative — it directly impacts operational costs. Energy typically represents 30-40% of a data center's total operating expense, and efficient procurement and lifecycle management can yield 15-30% cost reductions while simultaneously reducing environmental impact. This module bridges the gap between sustainability goals and operational efficiency by providing actionable metrics, audit frameworks, and optimization algorithms that translate environmental targets into engineering decisions.

## Core Capabilities

- **PUE Optimization**: Model and optimize Power Usage Effectiveness through airflow analysis, hot/cold aisle containment assessment, cooling system tuning, and free cooling opportunity identification.
- **E-Waste Tracking**: Full-chain tracking of IT equipment from procurement through deployment, decommissioning, refurbishment, recycling, and certified disposal with chain-of-custody documentation.
- **Hardware Lifecycle Management**: Track asset age, warranty status, depreciation, refresh scheduling, and end-of-life planning with environmental impact scoring for replacement decisions.
- **IT Carbon Footprint Reporting**: Calculate departmental, per-user, and per-workload carbon footprints incorporating Scope 2 (electricity) and partial Scope 3 (embodied carbon, supply chain) emissions.
- **Green Procurement Scoring**: Evaluate hardware and software vendors against EPEAT, Energy Star, TCO Certified, and custom environmental procurement criteria.
- **Energy Star Compliance Monitoring**: Track fleet compliance with Energy Star specifications, identify non-compliant assets, and generate upgrade recommendations.
- **Virtualization Efficiency Analysis**: Measure and optimize the ratio of virtual to physical resources, identify consolidation opportunities, and quantify energy savings from virtualization.
- **Cooling System Audit**: Assess data center cooling infrastructure including CRAC/CRAH units, chiller efficiency, liquid cooling potential, and waste heat recovery opportunities.

## Architecture

The module is organized around four operational domains:

1. **Audit Domain**: DataCenterAuditor captures power measurements, calculates PUE, and generates optimization recommendations. It maintains a time-series of measurements for trend analysis and anomaly detection.
2. **Asset Domain**: EWasteTracker manages the lifecycle of every IT asset from procurement to disposition. Each asset carries metadata including weight, hazardous materials, expected lifespan, and disposal history.
3. **Reporting Domain**: CarbonFootprintCalculator aggregates energy, embodied carbon, and supply chain data into structured reports with Scope 1/2/3 breakdowns. GreenProcurementScorer evaluates products against standardized environmental criteria.
4. **Optimization Domain**: PUEOptimizer and virtualization analyzers identify specific improvement opportunities and quantify their impact in both environmental and financial terms.

## Usage Examples

```python
from green_it import DataCenterAuditor, PUEOptimizer, EWasteTracker

# Audit a data center's PUE
auditor = DataCenterAuditor(name="DC-East")
auditor.record_measurement(
    total_power_kw=500.0,
    it_equipment_power_kw=320.0,
    cooling_power_kw=120.0,
    lighting_power_kw=10.0,
    other_power_kw=50.0
)
pue_result = auditor.calculate_pue()
print(f"PUE: {pue_result.pue:.2f}")  # Target: <1.2 for efficient
print(f"Wasted energy: {pue_result.wasted_power_kw:.1f} kW")
print(f"Annual excess cost: ${pue_result.annual_excess_cost_usd:,.0f}")

# Track e-waste through the full lifecycle
tracker = EWasteTracker()
device = tracker.register_device(
    asset_tag="SRV-2024-001",
    device_type="server",
    manufacturer="Dell",
    model="PowerEdge R750",
    purchase_date="2024-01-15",
    weight_kg=28.5,
    hazardous_materials=["lead_solder", "brominated_flame_retardant"]
)
tracker.update_status(device.asset_tag, "decommissioned", reason="refresh_cycle")
tracker.schedule_disposition(
    device.asset_tag,
    method="certified_recycler",
    recycler="Dell Reconnect",
    expected_recovery_percent=92.0
)
```

```python
from green_it import CarbonFootprintCalculator, GreenProcurementScorer

# Calculate IT department carbon footprint
calc = CarbonFootprintCalculator()
calc.add_energy_source(
    name="DC-East electricity",
    annual_kwh=4_380_000,
    grid_carbon_intensity=350.0,
    pue=1.35
)
calc.add_equipment_embodied(
    category="servers",
    count=120,
    embodied_carbon_kg=850.0,
    expected_lifespan_years=5,
    current_age_years=2.5
)
calc.add_scope3(
    category="cloud_services",
    annual_cost_usd=250_000,
    emission_factor_kg_per_usd=0.12
)
footprint = calc.compute()
print(f"Scope 2 (electricity): {footprint.scope2_kgCO2:,.0f} kg CO2eq")
print(f"Embodied (amortized): {footprint.embodied_kgCO2:,.0f} kg CO2eq")
print(f"Scope 3 (supply chain): {footprint.scope3_kgCO2:,.0f} kg CO2eq")
print(f"Total: {footprint.total_kgCO2:,.0f} kg CO2eq")

# Score hardware for green procurement
scorer = GreenProcurementScorer()
scores = scorer.score_products([
    {"name": "Dell PowerEdge R760", "epeat": "gold", "energy_star": True,
     "recycled_content": 35, "packaging_recyclable": True},
    {"name": "HPE ProLiant DL380", "epeat": "silver", "energy_star": True,
     "recycled_content": 20, "packaging_recyclable": True},
])
for s in scores:
    print(f"  {s['name']}: {s['total_score']:.1f}/100 ({s['rating']})")
```

```python
from green_it import DataCenterAuditor

# Trend analysis over multiple measurements
auditor = DataCenterAuditor(name="DC-West", climate_zone="cold")
import random
for _ in range(10):
    auditor.record_measurement(
        total_power_kw=480 + random.uniform(-20, 20),
        it_equipment_power_kw=310 + random.uniform(-10, 10),
        cooling_power_kw=100 + random.uniform(-5, 5),
        lighting_power_kw=8,
        other_power_kw=45
    )

trend = auditor.trend_analysis()
print(f"PUE trend: {trend['trend']}")
print(f"Change: {trend['change_percent']:.1f}%")

# Zombie server estimate
zombies = auditor.zombie_server_estimate(total_servers=500)
print(f"Estimated zombies: {zombies['estimated_zombies']}")
print(f"Annual waste: ${zombies['annual_waste_usd']:,.0f}")
```

## Configuration

The module supports configuration through constructor parameters for data center profiles, procurement criteria, and reporting thresholds:

```python
config = {
    "data_center": {
        "climate_zone": "temperate",  # cold, temperate, warm, tropical
        "target_pue": 1.25,
        "electricity_rate_usd_per_kwh": 0.10,
        "carbon_intensity_g_per_kwh": 350.0
    },
    "e_waste": {
        "default_recycler": "Dell Reconnect",
        "require_certified_recycler": True,
        "hazardous_materials_list": ["lead_solder", "brominated_flame_retardant", "mercury"]
    },
    "procurement": {
        "minimum_epeat": "silver",
        "require_energy_star": True,
        "minimum_recycled_content_percent": 20,
        "scoring_weights": {"epeat": 35, "energy_star": 20, "recycled_content": 25, "packaging": 10}
    }
}
```

## Use Cases

- **Data Center Consolidation Planning**: Use PUE measurements and zombie server detection to model the environmental and cost impact of consolidating multiple data centers into fewer, more efficient facilities.
- **IT Asset Refresh Optimization**: Model the crossover point where keeping an old server costs more in electricity than buying a new efficient one, factoring in embodied carbon of the new hardware.
- **Green Procurement RFP Evaluation**: Score vendor proposals against EPEAT, Energy Star, and custom criteria to select the most environmentally responsible hardware for large-scale deployments.
- **E-Waste Compliance Reporting**: Generate jurisdiction-specific e-waste compliance reports (WEEE Directive, state e-waste laws) with full chain-of-custody documentation for auditors.
- **Departmental Carbon Accountability**: Calculate per-department, per-team, or per-user IT carbon footprints to drive accountability and inform internal carbon pricing mechanisms.
- **Data Center Cooling Audit**: Identify hotspots, recirculation zones, and bypass airflow paths using temperature sensor data to reduce cooling energy by 15-30% without capital investment.

## Best Practices

- **Set PUE Targets by Climate Zone**: A PUE of 1.2 is excellent in a cold climate with free cooling, but may be unrealistic in tropical regions. Benchmark against climate-appropriate targets using ASHRAE guidelines.
- **Refresh Hardware Strategically**: Don't replace hardware solely on age. A 3-year-old efficient server often has a lower lifetime carbon footprint than a brand-new one when embodied carbon is factored in. Model the crossover point.
- **Require EPEAT Gold for Procurement**: Make EPEAT Gold (or equivalent) a mandatory procurement criterion for all IT equipment. This eliminates the worst environmental performers without requiring custom evaluation.
- **Track E-Waste with Chain of Custody**: Never use uncertified recyclers. Require documented chain of custody from decommissioning through final disposition, including downstream recycler certifications (R2, e-Stewards).
- **Virtualize Before Buying**: Consolidate workloads through virtualization before purchasing new hardware. A 3:1 consolidation ratio is typically achievable and delays embodied carbon emissions.
- **Monitor PUE Continuously**: Monthly manual PUE measurements miss seasonal variation and operational drift. Deploy real-time PUE monitoring with automated alerting when PUE exceeds thresholds.
- **Factor in Water Usage (WUE)**: Water Usage Effectiveness is the next frontier after PUE. Cooling towers consume significant water, and water scarcity makes WUE as important as PUE in many regions.
- **Decommission Zombies**: Idle servers ("zombies") consume 30-60% of active power while doing no useful work. Automated discovery and decommissioning of zombie infrastructure is the lowest-hanging fruit in green IT.

## Key Metrics & Formulas

| Metric | Formula | Description |
|--------|---------|-------------|
| **PUE** | `Total_facility_power / IT_equipment_power` | Power Usage Effectiveness: 1.0 = perfect, typical = 1.2-2.0 |
| **WUE** | `Water_used_liters / IT_equipment_kWh` | Water Usage Effectiveness for cooling-intensive facilities |
| **EPEAT Score** | Weighted sum of 8 categories | Environmental performance rating: Bronze/Silver/Gold |
| **IT Carbon Footprint** | `Scope2 + Embodied + Scope3` | Total carbon footprint of IT operations |
| **Recycling Rate** | `Recycled_weight / Total_e-waste_weight` | Percentage of e-waste diverted from landfill |
| **Zombie Server Cost** | `Count × Idle_power × Hours × Rate` | Annual cost of idle, unused servers |
| **Hardware Crossover Age** | Model iterative comparison | Age at which old hardware's running cost exceeds new hardware's total cost |

## Related Modules

- [green-computing](../green-computing/GROK.md) — Energy-efficient algorithms and carbon-aware workload scheduling. Works at the software layer, while green-it addresses the infrastructure layer.
- [carbon-tracking](../carbon-tracking/GROK.md) — Scope 1/2/3 emissions calculation and carbon accounting. Green-IT feeds electricity and embodied carbon data into carbon-tracking's reporting framework.
- [renewable-energy](../renewable-energy/GROK.md) — Renewable energy procurement, REC tracking, and grid integration. Enables green-IT to account for renewable energy in Scope 2 market-based calculations.
- [circular-economy](../circular-economy/GROK.md) — Material flow analysis and product lifecycle tracking. Extends green-IT's e-waste tracking with broader material circularity analysis.

---

## Advanced Configuration

The Green IT module supports advanced configuration through environment variables, configuration files, and programmatic API for fine-tuning data center audits, e-waste tracking, and procurement scoring.

```python
from green_it import AdvancedConfig

config = AdvancedConfig(
    # Data center audit precision
    power_measurement_interval_seconds=60,
    pue_calculation_window_hours=24,
    temperature_sensor_resolution_celsius=0.1,
    airflow_model="cfd_simplified",  # cfd_full, cfd_simplified, empirical

    # E-waste tracking granularity
    track_hazardous_materials=True,
    chain_of_custody_required=True,
    recycler_certification_min="r2",  # r2, e_stewards, iso14001
    asset_depreciation_method="straight_line",  # straight_line, declining_balance

    # Procurement scoring weights
    procurement_weights={
        "epeat": 0.35,
        "energy_star": 0.20,
        "recycled_content": 0.25,
        "packaging": 0.10,
        "repairability": 0.10
    },

    # Carbon footprint boundaries
    scope2_methodology="market_based",  # location_based, market_based
    include_embodied_carbon=True,
    embodied_carbon_amortization_years=5,

    # Alerting thresholds
    pue_alert_threshold=1.5,
    temperature_hotspot_delta_c=10,
    zombie_server_idle_days=90,
    eol_warning_months=6
)
```

### Configuration File Format

```yaml
# green_it_config.yaml
data_center:
  name: "DC-East-Primary"
  climate_zone: "temperate"
  target_pue: 1.25
  measurement:
    interval_seconds: 60
    sensors:
      - type: "power_meter"
        protocol: "snmp"
        endpoint: "10.0.1.100"
      - type: "temperature"
        protocol: "modbus"
        endpoint: "10.0.1.101"

e_waste:
  tracking:
    require_chain_of_custody: true
    certified_recyclers:
      - name: "Dell Reconnect"
        certification: "r2"
      - name: "Apple Trade In"
        certification: "iso14001"
  lifecycle:
    default_lifespan_years: 5
    refresh_trigger_utilization: 0.85

procurement:
  minimum_epeat: "silver"
  require_energy_star: true
  scoring:
    weights:
      epeat: 35
      energy_star: 20
      recycled_content: 25
      packaging: 10
      repairability: 10
```

## Architecture Patterns

### Sensor Aggregation Pattern

Multiple power and temperature sensors feed into a unified data model:

```python
from green_it import SensorAggregator, SensorConfig

aggregator = SensorAggregator()

# Register heterogeneous sensors
aggregator.register(SensorConfig(
    name="main_power",
    type="power",
    protocol="snmp",
    endpoint="10.0.1.100",
    poll_interval_seconds=60
))

aggregator.register(SensorConfig(
    name="rack_temps",
    type="temperature",
    protocol="modbus",
    endpoint="10.0.1.101",
    poll_interval_seconds=30,
    channels=48  # 48U rack
))

# Unified measurement
measurement = aggregator.read_all()
print(f"Total power: {measurement.total_power_kw:.1f} kW")
print(f"Max rack temp: {measurement.max_temperature_c:.1f} C")
```

### Audit Report Pipeline

```python
from green_it import AuditPipeline, AuditReport

pipeline = AuditPipeline(data_center="DC-East")
pipeline.add_stage("power_measurement", interval="1h")
pipeline.add_stage("pue_calculation", method="time_weighted")
pipeline.add_stage("hotspot_detection", threshold_c=35)
pipeline.add_stage("recommendation_generation")

report = pipeline.execute()
report.export_pdf("dc-east-audit-2025Q1.pdf")
```

### Event-Driven Asset Lifecycle

```python
from green_it import AssetEventBus, EWasteTracker

bus = AssetEventBus()
tracker = EWasteTracker()

@bus.on("asset_decommissioned")
def handle_decommission(event):
    tracker.schedule_disposition(
        asset_tag=event.asset_tag,
        method="certified_recycler",
        recycler="Dell Reconnect"
    )
    print(f"Decommissioned {event.asset_tag}: {event.reason}")

@bus.on("warranty_expiring")
def handle_warranty(event):
    print(f"Warranty expiring for {event.asset_tag} in {event.days_remaining} days")
```

## Integration Guide

### DCIM Integration

```python
from green_it import DCIMConnector

# Connect to Nlyte DCIM
connector = DCIMConnector(
    platform="nlyte",
    api_url="https://dcim.internal/api/v2",
    credentials_file="/etc/green-it/dcim-credentials.json"
)

# Import asset inventory
assets = connector.sync_assets()
print(f"Synced {len(assets)} assets from DCIM")

# Export audit results
connector.push_audit_results(
    data_center="DC-East",
    audit_results=audit_report
)
```

### Cloud Provider Integration

```python
from green_it import CloudProviderConnector

# AWS integration for cloud sustainability
aws = CloudProviderConnector(provider="aws")
aws.configure(
    regions=["us-east-1", "us-west-2"],
    include_embodied=True,
    pue_estimate=1.2
)

# GCP integration
gcp = CloudProviderConnector(provider="gcp")
gcp.configure(
    regions=["us-central1", "europe-west1"],
    carbon_aware=True
)
```

## Performance Optimization

### Batch Asset Processing

For large asset inventories, batch processing reduces API calls and improves throughput:

```python
from green_it import BatchAssetProcessor

processor = BatchAssetProcessor(
    batch_size=100,
    parallel_workers=4,
    retry_count=3
)

# Process 10,000 assets efficiently
results = processor.process(
    assets=large_asset_list,
    operation="update_lifecycle_status"
)
print(f"Processed: {results.success_count}")
print(f"Failed: {results.failure_count}")
print(f"Time: {results.elapsed_seconds:.1f}s")
```

### Cached PUE Calculations

PUE calculations can be cached to avoid recomputation:

```python
from green_it import CachedPUECalculator

calculator = CachedPUECalculator(
    cache_backend="redis",
    cache_ttl_seconds=3600,
    recalculate_on_anomaly=True
)

# First call computes and caches
pue = calculator.compute(
    total_power_kw=500,
    it_power_kw=320
)

# Second call uses cache (near-instant)
pue_cached = calculator.compute(
    total_power_kw=500,
    it_power_kw=320
)
```

## Security Considerations

### Credential Management

```python
from green_it import SecureDCIMConnector

connector = SecureDCIMConnector(
    platform="nlyte",
    secret_backend="aws_secrets_manager",
    secret_name="dcim/api-credentials",
    rotate_days=90
)
```

### Data Privacy

Asset tracking data may contain sensitive information. Apply data classification:

```python
from green_it import AssetDataClassifier

classifier = AssetDataClassifier()
classifier.classify("asset_tag", "public")
classifier.classify("location_floor", "internal")
classifier.classify("assigned_user", "confidential")

# Redacted export
export = classifier.export(
    assets=asset_list,
    classification_max="internal"
)
```

## Troubleshooting Guide

| Issue | Possible Cause | Resolution |
|-------|---------------|------------|
| PUE calculation returns 1.0 | IT power reading equals total power | Check power meter wiring and sensor calibration |
| E-waste chain of custody broken | Recycler not reporting disposition | Contact recycler, require R2 certification documentation |
| Zombie servers detected | Workloads migrated but servers not decommissioned | Verify no running processes, schedule decommission |
| Green procurement scores inconsistent | Missing vendor data fields | Request EPEAT/Energy Star documentation from vendor |
| Temperature hotspot not detected | Sensor density too low | Add temperature sensors to high-density racks |

```python
# Diagnostic script
from green_it import DiagnosticRunner

diag = DiagnosticRunner(data_center="DC-East")
results = diag.run_all()
for check in results:
    status = "PASS" if check.passed else "FAIL"
    print(f"[{status}] {check.name}: {check.message}")
```

## API Reference

### DataCenterAuditor

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `record_measurement(...)` | power values: float | `None` | Record a power measurement |
| `calculate_pue()` | - | `PUEResult` | Calculate PUE from measurements |
| `trend_analysis()` | - | `TrendResult` | Analyze PUE trend over time |
| `zombie_server_estimate(total_servers)` | count: int | `ZombieEstimate` | Estimate idle server count |

### EWasteTracker

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `register_device(...)` | device details | `Asset` | Register a new IT asset |
| `update_status(tag, status)` | tag: str, status: str | `None` | Update asset lifecycle status |
| `schedule_disposition(...)` | disposition details | `Disposition` | Schedule disposal method |
| `get_lifecycle_report(tag)` | tag: str | `LifecycleReport` | Full lifecycle history |

### GreenProcurementScorer

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `score_products(products)` | list: List[dict] | `List[Score]` | Score products against criteria |
| `update_weights(weights)` | weights: dict | `None` | Adjust scoring weights |
| `add_custom_criterion(...)` | criterion details | `None` | Add custom procurement criterion |

## Data Models

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class PUEResult:
    pue: float
    total_power_kw: float
    it_power_kw: float
    wasted_power_kw: float
    annual_excess_cost_usd: float
    timestamp: datetime

@dataclass
class Asset:
    asset_tag: str
    device_type: str
    manufacturer: str
    model: str
    purchase_date: str
    weight_kg: float
    hazardous_materials: List[str]
    status: str
    lifecycle_events: List[dict]

@dataclass
class Disposition:
    asset_tag: str
    method: str
    recycler: str
    expected_recovery_percent: float
    scheduled_date: str
    chain_of_custody: List[dict]

@dataclass
class ProcurementScore:
    name: str
    total_score: float
    rating: str
    epeat_score: float
    energy_star: bool
    recycled_content: float
    details: dict
```

## Deployment Guide

### On-Premises Deployment

```bash
# Install dependencies
pip install green-it[all]

# Configure data center profile
cp config.example.yaml /etc/green-it/config.yaml
vim /etc/green-it/config.yaml

# Initialize database
green-it init-db --config /etc/green-it/config.yaml

# Start the audit service
green-it serve --config /etc/green-it/config.yaml --port 8080
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

RUN pip install green-it[all]

COPY config.yaml /etc/green-it/config.yaml

HEALTHCHECK --interval=30s --timeout=5s \
  CMD green-it health-check

ENTRYPOINT ["green-it"]
CMD ["serve", "--config", "/etc/green-it/config.yaml"]
```

## Monitoring & Observability

### Metrics Collection

```python
from green_it import MetricsCollector

collector = MetricsCollector()

# Register custom metrics
collector.register_gauge("pue_current", "Current PUE value")
collector.register_counter("assets_decommissioned_total", "Total assets decommissioned")
collector.register_histogram("audit_duration_seconds", "Audit execution time")

# Update metrics
collector.set("pue_current", 1.35)
collector.inc("assets_decommissioned_total")
```

### Alerting

```python
from green_it import AlertManager

alerts = AlertManager()

@alerts.on("pue_exceeded")
def handle_pue_alert(event):
    print(f"PUE alert: {event.current_pue} exceeds threshold {event.threshold}")
    # Send notification to operations team
```

## Testing Strategy

```python
import pytest
from green_it import DataCenterAuditor, EWasteTracker

class TestDataCenterAuditor:
    def test_pue_calculation(self):
        auditor = DataCenterAuditor(name="test-dc")
        auditor.record_measurement(
            total_power_kw=500,
            it_equipment_power_kw=320,
            cooling_power_kw=120,
            lighting_power_kw=10,
            other_power_kw=50
        )
        result = auditor.calculate_pue()
        assert abs(result.pue - 1.5625) < 0.01

    def test_zombie_detection(self):
        auditor = DataCenterAuditor(name="test-dc")
        zombies = auditor.zombie_server_estimate(total_servers=500)
        assert zombies.estimated_zombies > 0
        assert zombies.annual_waste_usd > 0

class TestEWasteTracker:
    def test_asset_lifecycle(self):
        tracker = EWasteTracker()
        device = tracker.register_device(
            asset_tag="TEST-001",
            device_type="server",
            manufacturer="Dell",
            model="R750",
            purchase_date="2024-01-15",
            weight_kg=28.5,
            hazardous_materials=[]
        )
        tracker.update_status("TEST-001", "decommissioned")
        report = tracker.get_lifecycle_report("TEST-001")
        assert len(report.lifecycle_events) >= 2
```

## Versioning & Migration

### Semantic Versioning

- **MAJOR**: Breaking changes to API or configuration schema
- **MINOR**: New features, new DCIM integrations, new procurement criteria
- **PATCH**: Bug fixes, performance improvements

### Migration Guide

```python
# v1.x to v2.x migration
# Old API
auditor = DataCenterAuditor("DC-East", power_meter_ip="10.0.1.100")

# New API
from green_it import DataCenterAuditor, SensorConfig
auditor = DataCenterAuditor(
    name="DC-East",
    sensors=[SensorConfig(type="power", endpoint="10.0.1.100")]
)
```

## Glossary

| Term | Definition |
|------|-----------|
| **PUE** | Power Usage Effectiveness — ratio of total facility power to IT equipment power |
| **WUE** | Water Usage Effectiveness — liters of water per kWh of IT equipment |
| **EPEAT** | Electronic Product Environmental Assessment Tool — procurement standard |
| **Energy Star** | EPA program for energy-efficient products |
| **E-Waste** | Electronic waste — discarded electrical or electronic devices |
| **Zombie Server** | An idle server consuming power but doing no useful work |
| **CRAC** | Computer Room Air Conditioning — data center cooling unit |
| **CRAH** | Computer Room Air Handler — air-based cooling distribution unit |
| **Hot Aisle/Cold Aisle** | Containment design separating hot exhaust from cold intake air |
| **R2** | Responsible Recycling — e-waste recycler certification standard |

## Changelog

### v1.0.0 (2025-01-15)
- Initial release with PUE optimization
- E-waste tracking with chain of custody
- Green procurement scoring
- Carbon footprint calculator

### v1.1.0 (2025-02-01)
- Added DCIM integration
- Improved zombie server detection
- Added Water Usage Effectiveness (WUE) metrics

### v1.2.0 (2025-03-01)
- Added Kubernetes deployment support
- Improved audit report generation
- Added multi-data-center aggregation

## Contributing Guidelines

1. **Fork the repository** and create a feature branch from `main`
2. **Write tests** for all new functionality with >80% coverage
3. **Follow PEP 8** style guidelines with type hints
4. **Update documentation** for any API changes
5. **Add changelog entries** under `[Unreleased]` section
6. **Submit a pull request** with a clear description of changes

### Code Review Checklist

- [ ] Tests pass and coverage meets threshold
- [ ] No hardcoded credentials or API keys
- [ ] E-waste tracking includes chain of custody
- [ ] PUE calculations are auditable
- [ ] Procurement scoring criteria are documented

## License

This module is licensed under the Apache License, Version 2.0. See the LICENSE file for full terms.

Copyright 2025 Green IT Contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
