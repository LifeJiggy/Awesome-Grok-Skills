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
