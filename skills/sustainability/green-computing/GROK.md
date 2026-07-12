---
name: "green-computing"
category: "sustainability"
version: "1.0.0"
tags: ["sustainability", "green-computing", "energy-efficiency", "carbon-aware"]
---

# Green Computing

## Overview

Green Computing encompasses the practice of designing, manufacturing, using, and disposing of computing devices and systems in a way that minimizes environmental impact. This module provides a comprehensive framework for energy-efficient algorithm design, carbon-aware workload scheduling, server power management through Dynamic Voltage and Frequency Scaling (DVFS), and real-time monitoring of the environmental footprint of computational workloads. By integrating with carbon intensity APIs from electricity grids worldwide, applications can dynamically shift compute-intensive tasks to periods and locations where renewable energy supply is at its peak.

The discipline sits at the intersection of computer science, environmental engineering, and energy policy. As data centers consume roughly 1-2% of global electricity and that share continues to rise with AI and cloud computing adoption, the need for software-level interventions has become critical. Green computing goes beyond simply turning off monitors — it involves restructuring algorithmic complexity, rethinking distributed systems architectures, implementing intelligent workload migration across geographic regions, and building observability stacks that track grams of CO2 per query, per transaction, or per training epoch.

This module equips engineers with tools to measure, reduce, and report the carbon footprint of their software systems. It includes carbon intensity data fetching, DVFS controller abstractions, workload schedulers that factor in grid carbon signals, green software metrics collection (SCI — Software Carbon Intensity), and power measurement interfaces for bare-metal and virtualized environments. The module is designed to be composable: each component can be used independently or orchestrated together for end-to-end carbon-aware computing.

## Core Capabilities

- **Carbon Intensity API Integration**: Fetch real-time and forecasted grid carbon intensity data from electricityMap, WattTime, Electricity Maps API, and regional ISO/RTO feeds to inform scheduling decisions.
- **DVFS Optimization**: Control CPU voltage and frequency scaling to match computational demand, reducing power consumption during low-utilization periods without violating latency SLAs.
- **Carbon-Aware Workload Scheduling**: Delay, defer, or migrate batch jobs and non-interactive workloads to time windows and regions where grid carbon intensity is lowest.
- **Software Carbon Intensity (SCI) Measurement**: Implement the SCI specification (gCO2eq per unit of functional unit) to benchmark and compare the carbon cost of software operations.
- **Server Power Modeling**: Estimate and track server power consumption using hardware performance counters, CPU utilization metrics, and empirical power models.
- **Workload Migration Engine**: Orchestrate live migration of virtual machines and containers across data centers to follow renewable energy availability signals.
- **Green Metrics Dashboard**: Collect, aggregate, and visualize energy consumption, carbon emissions, PUE-adjusted emissions, and renewable energy fraction over time.
- **Power Capping and Budgeting**: Enforce per-workload or per-cluster power budgets using hardware power caps (RAPL, IPMI) to stay within renewable energy budgets.

## Architecture

The module follows a layered architecture with clear separation of concerns:

1. **Data Layer**: Carbon intensity APIs, hardware power sensors (RAPL, IPMI, power meters), and historical telemetry databases provide the raw signals.
2. **Model Layer**: Power models, carbon intensity forecasts, and workload characterization engines transform raw data into actionable predictions.
3. **Decision Layer**: The scheduler, DVFS controller, and migration engine use model outputs to make optimization decisions.
4. **Action Layer**: APIs to cloud providers, hypervisors, and OS-level power management execute the decisions.
5. **Observability Layer**: The green metrics dashboard tracks outcomes, measures savings, and feeds back into model calibration.

Each layer communicates through well-defined interfaces, allowing you to swap implementations (e.g., replace WattTime with Electricity Maps) without changing downstream components.

## Usage Examples

```python
from green_computing import CarbonIntensityClient, WorkloadScheduler, DVFSController

# Fetch current carbon intensity for a region
client = CarbonIntensityClient()
intensity = client.get_current_intensity(region="DE")
print(f"Germany grid: {intensity.gCO2_per_kWh:.1f} gCO2eq/kWh")
print(f"Renewable fraction: {intensity.renewable_percent:.1f}%")

# Schedule a workload during low-carbon windows
scheduler = WorkloadScheduler(region="US-CAL-CISO")
optimal_window = scheduler.find_low_carbon_window(
    task_duration_hours=4,
    max_delay_hours=12
)
print(f"Best start: {optimal_window.start}")
print(f"Expected intensity: {optimal_window.avg_gCO2_per_kWh:.1f}")

# Optimize CPU DVFS for a background batch job
dvfs = DVFSController(cpu_id=0)
dvfs.set_governor("powersave")
dvfs.set_frequency_mhz(1200)  # Downclock for non-urgent work
power_before = dvfs.estimate_power_watts()
dvfs.set_frequency_mhz(2400)  # Upclock for urgent work
power_after = dvfs.estimate_power_watts()
print(f"Power savings at 1200MHz: {power_before - power_after:.1f}W")
```

```python
from green_computing import SCICalculator, PowerModel

# Calculate Software Carbon Intensity
calc = SCICalculator(
    energy_measurements=[0.005, 0.004, 0.006, 0.003],  # kWh per request batch
    carbon_intensity=250.0,  # gCO2eq/kWh grid average
    embodied_carbon_g=1200.0,  # Embodied carbon of server
    expected_lifespan_hours=43800.0  # 5-year lifespan
)
sci_score = calc.compute(
    functional_unit="per-request",
    total_requests=100000
)
print(f"SCI: {sci_score.gCO2eq_per_request:.6f} gCO2eq/request")

# Model server power consumption
model = PowerModel(
    idle_power_watts=85,
    max_power_watts=350,
    cpu_tdp=170,
    memory_watts=24,
    storage_watts=12
)
for utilization in [0.1, 0.3, 0.5, 0.7, 1.0]:
    power = model.estimate(cpu_utilization=utilization, memory_utilization=0.4)
    print(f"CPU {utilization*100:.0f}%: {power:.1f}W")
```

```python
from green_computing import GreenMetricsDashboard
from datetime import datetime, timezone, timedelta

# Track carbon metrics over time
dashboard = GreenMetricsDashboard()
now = datetime.now(timezone.utc)

# Record hourly measurements for a week
for i in range(168):  # 7 days
    dashboard.record(
        timestamp=now + timedelta(hours=i),
        energy_kwh=0.5 + (i % 24) * 0.02,  # Varies by hour
        carbon_g=150 + (i % 24) * 5,
        pue=1.15 + (i % 7) * 0.01
    )

summary = dashboard.summary()
print(f"Total energy: {summary['total_energy_kwh']:.1f} kWh")
print(f"Total carbon: {summary['total_carbon_g']:.0f} g CO2")
print(f"Avg carbon intensity: {summary['avg_carbon_per_kwh']:.1f} gCO2eq/kWh")
print(f"Avg PUE: {summary['avg_pue']:.2f}")
```

## Configuration

The module supports configuration through constructor parameters or a configuration dictionary:

```python
config = {
    "carbon_api": {
        "provider": "electricitymaps",  # or "watttime"
        "api_key": "your-api-key",
        "cache_ttl_seconds": 300,
        "fallback_intensity": 400.0  # gCO2eq/kWh when API is unavailable
    },
    "dvfs": {
        "default_governor": "schedutil",
        "min_freq_mhz": 800,
        "max_freq_mhz": 4500,
        "power_model": "linear"  # or "polynomial"
    },
    "scheduler": {
        "max_delay_hours": 24,
        "min_carbon_savings_percent": 10,
        "reschedule_interval_minutes": 15
    },
    "power_model": {
        "idle_power_watts": 85,
        "max_power_watts": 350,
        "pue": 1.2,
        "electricity_rate_usd_per_kwh": 0.10
    }
}
```

## Use Cases

- **AI/ML Training Job Scheduling**: Defer large model training runs (LLMs, computer vision) to off-peak hours when grid carbon intensity is lowest. A typical 1000-GPU training job consuming 500kW for 48 hours can save 2-5 tonnes of CO2 by shifting 6 hours to a low-carbon window.
- **CI/CD Pipeline Carbon Budgeting**: Set carbon budgets for continuous integration pipelines. When a build exceeds its carbon budget, automatically defer non-critical test suites to lower-carbon periods or reduce parallelism.
- **Cloud Region Selection**: When deploying new services, compare carbon intensity across cloud provider regions and select the one with the highest renewable energy fraction, not just the lowest latency.
- **Data Lake Compaction**: Schedule periodic data compaction and garbage collection jobs during nighttime hours when wind generation peaks and carbon intensity drops below 100 gCO2eq/kWh in most grids.
- **Video Transcoding Optimization**: Batch video transcoding jobs are ideal carbon-aware candidates — they are delay-tolerant, embarrassingly parallel, and compute-intensive. Schedule transcoding queues to follow solar generation curves.
- **Carbon-Aware API Rate Limiting**: Implement dynamic rate limiting that throttles non-essential API traffic during high-carbon periods and relaxes limits during low-carbon windows, reducing the carbon cost of traffic spikes.

## Best Practices

- **Measure Before Optimizing**: Instrument your application with energy and carbon measurement before attempting optimizations. You cannot improve what you cannot measure.
- **Use SCI as Your Baseline**: Adopt the Green Software Foundation's SCI specification as your primary metric. It provides a standardized, comparable measure across teams and organizations.
- **Carbon-Intensity-Aware Scheduling**: Always use real-time and forecasted carbon intensity data, not regional averages, for scheduling decisions. Average values mask significant diurnal and weather-driven variability.
- **Separate Interactive from Batch Workloads**: Interactive (latency-sensitive) workloads require different optimization strategies than batch workloads. Batch workloads are ideal candidates for carbon-aware deferral and migration.
- **Account for Embodied Carbon**: Software carbon accounting must include the embodied carbon of the hardware running it (manufacturing, transport, disposal). The SCI specification includes an `Embodied Carbon` term for this purpose.
- **Test Power Models Against Real Hardware**: Empirical power models (linear, polynomial) must be calibrated against actual hardware measurements using RAPL, IPMI, or power meters. Published TDP values are upper bounds, not operational averages.
- **Leverage DVFS Wisely**: DVFS scaling is most effective for compute-bound workloads with predictable utilization patterns. For I/O-bound workloads, memory and storage power dominate CPU power, limiting DVFS impact.
- **Monitor Grid Mix Continuously**: Grid carbon intensity can change within minutes as wind/solar generation fluctuates. For workloads longer than 15 minutes, re-check carbon intensity periodically during execution, not just at scheduling time.

## Key Metrics & Formulas

| Metric | Formula | Description |
|--------|---------|-------------|
| **SCI** | `(E × I + M) / R` | Software Carbon Intensity: Energy × Carbon Intensity + Embodied carbon, per Functional Unit |
| **Carbon Intensity** | `gCO2eq / kWh` | Grams of CO2 equivalent per kilowatt-hour of electricity consumed |
| **Power Savings** | `(P_max - P_actual) × hours` | Energy saved by running at reduced frequency vs. maximum |
| **Carbon Savings** | `Energy_saved × grid_intensity` | CO2 avoided by workload deferral to low-carbon periods |
| **DVFS Efficiency** | `P_actual / P_max` | Fraction of maximum power consumed at current frequency |
| **Renewable Match** | `Renewable_generation / Total_load` | Fraction of load served by renewable energy |
| **DVFS Power Ratio** | `P_actual / P_max_frequency` | Power consumption as fraction of max-frequency power |
| **SCI Embodied Term** | `Embodied_carbon × (time_in_service / lifespan)` | Amortized embodied carbon per measurement period |
| **Carbon-Aware Delay** | `Current_CI - Forecast_min_CI` | Carbon intensity difference between now and optimal window |

## Related Modules

- [green-it](../green-it/GROK.md) — IT infrastructure sustainability audits, data center PUE optimization, e-waste tracking, and hardware lifecycle management. Complements green computing by addressing the physical infrastructure layer.
- [carbon-tracking](../carbon-tracking/GROK.md) — Scope 1/2/3 emissions calculation, GHG Protocol compliance, and carbon credit management. Provides the accounting framework that green computing metrics feed into.
- [renewable-energy](../renewable-energy/GROK.md) — Solar/wind forecasting, battery storage optimization, and grid balancing. Supplies the renewable generation data that carbon-aware schedulers depend on.
- [circular-economy](../circular-economy/GROK.md) — Material flow analysis, product lifecycle tracking, and circular design scoring. Addresses the embodied carbon and end-of-life phases of computing hardware.

## Data Sources & APIs

The module integrates with the following external data providers for carbon intensity and energy data:

| Provider | Coverage | Data Type | Update Frequency |
|----------|----------|-----------|------------------|
| Electricity Maps | 200+ regions | Real-time + forecast | 5-minute |
| WattTime | US grid | Real-time marginal | 5-minute |
| EPA eGRID | US regions | Annual average | Annual |
| IEA | Global | Country-level | Annual |
| DEFRA | UK | Conversion factors | Annual |
