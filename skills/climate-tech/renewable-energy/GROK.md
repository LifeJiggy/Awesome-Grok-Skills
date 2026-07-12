---
name: "renewable-energy"
category: "climate-tech"
version: "2.0.0"
tags: ["climate-tech", "renewable-energy", "solar", "wind", "energy-storage"]
---

# Renewable Energy

## Overview

The Renewable Energy module provides comprehensive tools for planning, optimizing, and analyzing renewable energy systems including solar, wind, hydropower, and energy storage. It covers resource assessment, system sizing, economic analysis, grid integration, and performance monitoring. The module supports energy transition modeling, microgrid design, and renewable energy certificate tracking.

This skill is essential for energy engineers, project developers, sustainability consultants, and policymakers planning clean energy transitions.

## Core Capabilities

- **Solar Energy**: PV system sizing, solar resource assessment, panel orientation optimization, and performance ratio calculation
- **Wind Energy**: Wind resource analysis, turbine selection, capacity factor estimation, and wake effect modeling
- **Energy Storage**: Battery sizing, state-of-charge modeling, cycle life analysis, and storage economics
- **Hydropower**: Run-of-river and storage hydropower assessment, flow duration analysis, and turbine selection
- **Grid Integration**: Curtailment analysis, grid stability assessment, and interconnection capacity studies
- **Economic Analysis**: LCOE calculation, payback period, IRR, and sensitivity analysis
- **Microgrid Design**: Islanding capability, load balancing, and hybrid system optimization
- **Energy Certificates**: REC tracking, Guarantees of Origin, and carbon-free energy claims

## Usage Examples

```python
from renewable_energy import (
    SolarPlanner,
    WindPlanner,
    StorageOptimizer,
    EconomicAnalyzer,
    MicrogridDesigner,
)

# --- Solar System Sizing ---
solar = SolarPlanner(
    location={"lat": 35.0, "lon": -118.0},
    system_capacity_kw=100,
)
resource = solar.assess_resource()
print(f"Solar irradiance: {resource.ghi_kwh_m2:.1f} kWh/m^2/yr")
print(f"Peak sun hours: {resource.peak_sun_hours:.1f}")

performance = solar.estimate_performance()
print(f"Annual generation: {performance.annual_kwh:,.0f} kWh")
print(f"Performance ratio: {performance.performance_ratio:.1%}")
print(f"Capacity factor: {performance.capacity_factor:.1%}")

# --- Wind Energy ---
wind = WindPlanner(
    hub_height_m=80,
    turbine_rating_kw=3000,
)
wind_resource = wind.assess_resource(
    wind_speed_ms=7.5,
    weibull_k=2.0,
)
print(f"Wind power density: {wind_resource.power_density_w_m2:.1f} W/m^2")
print(f"Capacity factor: {wind_resource.capacity_factor:.1%}")

generation = wind.estimate_generation()
print(f"Annual generation: {generation.annual_mwh:,.0f} MWh")

# --- Energy Storage ---
storage = StorageOptimizer(
    technology="li_ion",
    capacity_kwh=500,
    power_kw=250,
)
cycle = storage.simulate_cycle(
    charge_rate=0.5,
    discharge_rate=0.8,
    depth_of_discharge=0.8,
)
print(f"Cycle efficiency: {cycle.efficiency:.1%}")
print(f"Cycle life: {cycle.cycle_life:,} cycles")

economics = storage.calculate_economics(
    electricity_price=0.12,
    demand_charge=15.0,
)
print(f"Simple payback: {economics.payback_years:.1f} years")

# --- LCOE Calculation ---
analyzer = EconomicAnalyzer()
lcoe = analyzer.calculate_lcoe(
    capex=200000,
    annual_opex=3000,
    annual_generation_kwh=150000,
    lifetime_years=25,
    discount_rate=0.06,
)
print(f"LCOE: ${lcoe:.3f}/kWh")

# --- Microgrid Design ---
microgrid = MicrogridDesigner()
system = microgrid.optimize(
    load_kw=500,
    solar_capacity_kw=800,
    storage_kwh=1000,
    grid_connection=True,
)
print(f"Renewable fraction: {system.renewable_fraction:.1%}")
print(f"Annual cost: ${system.annual_cost:,.0f}")
```

## Best Practices

- Use TMY (Typical Meteorological Year) data for solar resource assessment
- Apply appropriate wind shear models for hub height extrapolation
- Size battery storage based on load profile analysis, not just peak demand
- Include degradation rates (0.5%/yr for solar, 2%/yr for Li-ion) in lifetime analyses
- Consider curtailment losses for systems >100kW connected to constrained grids
- Use real load profiles (15-min intervals) for storage optimization — averages mislead
- Apply appropriate discount rates (6-10%) for project economics
- Include all balance-of-system costs in LCOE: inverters, wiring, permits, interconnection
- Monitor actual vs predicted performance — underperformance indicates maintenance needs
- Document all assumptions and data sources for energy yield assessments

## Related Modules

- **carbon-tracking**: Emissions avoided by renewable energy
- **climate-data**: Solar and wind resource data
- **environmental-modeling**: Environmental impact of energy projects
- **emission-reduction**: Energy transition pathways
