---
name: "renewable-energy"
category: "sustainability"
version: "1.0.0"
tags: ["sustainability", "renewable-energy", "solar", "wind", "battery", "grid"]
---

# Renewable Energy

## Overview

Renewable Energy encompasses the technologies, algorithms, and market mechanisms for generating, storing, trading, and managing electricity from clean sources — primarily solar photovoltaics, wind turbines, and battery energy storage systems (BESS). This module provides a comprehensive computational toolkit for solar irradiance forecasting, wind power prediction, battery storage optimization, grid balancing, energy trading, microgrid management, and Renewable Energy Certificate (REC) tracking. As the global energy transition accelerates, the ability to predict renewable generation, optimize storage dispatch, and participate in energy markets becomes essential for both utilities and distributed energy resource operators.

The physics of renewable energy differ fundamentally from conventional generation: solar output depends on irradiance, temperature, and panel degradation; wind output depends on the cubic relationship between wind speed and power (with cut-in, rated, and cut-out thresholds); and battery storage involves complex electrochemistry with state-of-charge-dependent efficiency, degradation curves, and thermal management. This module models these physical realities to provide accurate predictions and optimal dispatch strategies. It includes numerical weather prediction (NWP) integration for day-ahead forecasting, real-time adjustment using measurement nowcasting, and machine learning-enhanced prediction models that learn from historical forecast errors.

The economic layer covers energy market participation: day-ahead and intraday market bidding strategies, battery arbitrage optimization (buy low, sell high), demand response program enrollment, and virtual power plant (VPP) aggregation. For behind-the-meter and islanded applications, the microgrid management component handles local optimization with constraints on import/export limits, voltage regulation, and black-start capability. The module also tracks Renewable Energy Certificates (RECs), Guarantees of Origin (GOs), and carbon-free energy (CFE) matching for corporate procurement and regulatory compliance.

## Core Capabilities

- **Solar Irradiance Forecasting**: Day-ahead and hour-ahead solar generation prediction using NWP data, satellite imagery processing, and PV system modeling (plane-of-array irradiance, temperature coefficients, inverter clipping).
- **Wind Power Prediction**: Turbine-level and farm-level wind power forecasting using wind speed/direction profiles, wake effects, air density corrections, and power curve modeling.
- **Battery Storage Optimization**: State-of-charge management, charge/discharge scheduling, degradation-aware dispatch, arbitrage optimization, and frequency regulation participation.
- **Grid Balancing Algorithms**: Real-time supply-demand balancing, frequency response modeling, voltage regulation, and congestion management for grid operators and aggregators.
- **Energy Trading Platform**: Day-ahead and intraday market bidding, PPA (Power Purchase Agreement) management, settlement calculation, and market price forecasting.
- **Microgrid Management**: Islanded and grid-connected operation modes, local optimization with DER (Distributed Energy Resource) coordination, and black-start sequencing.
- **REC/GO Tracking**: Renewable Energy Certificate issuance, transfer, retirement, and compliance matching for voluntary and regulatory markets.
- **Demand Response Optimization**: Load shifting, peak shaving, and ancillary service enrollment for behind-the-meter resources.

## Architecture

The module is structured around three operational layers:

1. **Forecast Layer**: SolarForecaster and WindForecaster consume weather data (NWP, satellite, historical) and produce generation predictions with uncertainty bounds. These forecasts drive all downstream optimization.
2. **Optimization Layer**: BatteryOptimizer, MicrogridManager, and EnergyTrader use forecasts plus market signals to generate optimal dispatch schedules. The optimization respects physical constraints (ramp rates, SOC limits, grid interconnection capacity) and economic objectives (revenue maximization, cost minimization, carbon reduction).
3. **Settlement Layer**: RECTracker and EnergyTrader's settlement functions track certificate flows, calculate market settlements, and reconcile physical generation with commercial positions.

## Usage Examples

```python
from renewable_energy import SolarForecaster, WindForecaster, BatteryOptimizer

# Solar generation forecast
solar = SolarForecaster(
    system_capacity_kw=500,
    tilt_degrees=30,
    azimuth_degrees=180,
    latitude=37.77,
    longitude=-122.42
)
forecast = solar.forecast_next_24h(temperature_c=25.0)
for hour in forecast:
    print(f"  {hour.time.strftime('%H:%M')}: {hour.power_kw:.1f} kW "
          f"({hour.capacity_factor:.0%} CF)")

# Wind power prediction
wind = WindForecaster(
    turbine_rated_power_kw=3000,
    hub_height_m=100,
    rotor_diameter_m=112
)
wind_forecast = wind.predict(
    wind_speed_ms=8.5,
    wind_direction_deg=225,
    air_density_kg_m3=1.225,
    turbulence_intensity=0.12
)
print(f"Predicted output: {wind_forecast.power_kw:.0f} kW "
      f"({wind_forecast.capacity_factor:.0%} CF)")

# Battery storage optimization
battery = BatteryOptimizer(
    capacity_kwh=1000,
    max_charge_kw=250,
    max_discharge_kw=250,
    round_trip_efficiency=0.92,
    degradation_per_cycle=0.0002
)
schedule = battery.optimize_for_arbitrage(
    prices=[45, 42, 38, 35, 33, 30, 28, 32, 48, 65, 85, 95,
            110, 120, 95, 75, 60, 55, 70, 85, 100, 90, 70, 50],
    current_soc=0.5
)
profit = sum(s.revenue_usd for s in schedule)
print(f"Arbitrage profit: ${profit:.2f} over 24 hours")
```

```python
from renewable_energy import MicrogridManager, RECTracker, EnergyTrader

# Microgrid management
microgrid = MicrogridManager(name="Campus Microgrid")
microgrid.add_solar(capacity_kw=200)
microgrid.add_battery(capacity_kwh=500, max_power_kw=125)
microgrid.add_load(typical_kw=180, critical_kw=50)

dispatch = microgrid.optimize_dispatch(
    solar_forecast_kw=150,
    grid_price_cents=12.0,
    mode="grid_connected"
)
print(f"Solar: {dispatch.solar_used_kw:.0f} kW, Battery: {dispatch.battery_action}")
print(f"Grid import: {dispatch.grid_import_kw:.0f} kW")

# REC tracking
recs = RECTracker()
recs.issue(certificates=100, source="solar", vintage=2025, region="US-CA")
retirement = recs.retire(certificates=50, reason="Scope 2 compliance")
print(f"Retired {retirement['retired']} RECs. Remaining: {recs.balance()}")

# Energy trading
trader = EnergyTrader(market="PJM")
bids = trader.generate_day_ahead_bids(
    generation_forecast_kwh=[100, 120, 80, 60, 90, 150, 200, 180,
                              160, 140, 130, 120, 110, 105, 100, 95,
                              90, 110, 150, 200, 220, 180, 140, 100],
    price_forecast_cents=[3.5, 3.2, 3.0, 2.8, 3.1, 4.5, 6.0, 5.5,
                          5.0, 4.8, 4.5, 4.2, 4.0, 3.8, 3.5, 3.3,
                          3.2, 4.0, 6.5, 8.0, 9.5, 7.0, 5.0, 3.8]
)
print(f"Total bid volume: {sum(b.quantity_kwh for b in bids):,} kWh")
```

## Configuration

```python
config = {
    "solar": {
        "system_capacity_kw": 500,
        "tilt_degrees": 30,
        "azimuth_degrees": 180,
        "dc_ac_ratio": 1.2,
        "module_efficiency": 0.20,
        "temp_coefficient": -0.004,
        "soiling_loss_percent": 3.0
    },
    "wind": {
        "turbine_rated_power_kw": 3000,
        "hub_height_m": 100,
        "rotor_diameter_m": 112,
        "cut_in_ms": 3.5,
        "rated_ms": 12.0,
        "cut_out_ms": 25.0,
        "wake_model": "jensen"
    },
    "battery": {
        "capacity_kwh": 1000,
        "max_charge_kw": 250,
        "max_discharge_kw": 250,
        "round_trip_efficiency": 0.92,
        "degradation_per_cycle": 0.0002,
        "min_soc": 0.10,
        "max_soc": 0.95,
        "replacement_cost_per_kwh": 350
    },
    "market": {
        "market_operator": "PJM",
        "bid_lead_time_hours": 12,
        "imbalance_penalty_cents": 5.0,
        "min_price_cents": 2.0
    }
}
```

## Use Cases

- **Solar Farm Investment Analysis**: Model expected generation, revenue from energy market bidding, and battery storage value-add to evaluate the financial viability of new solar farm investments.
- **Corporate PPA Optimization**: Optimize Power Purchase Agreement structures by analyzing hourly generation profiles against load shapes to maximize renewable energy matching and minimize cost.
- **Microgrid Islanding Preparation**: Pre-compute optimal dispatch schedules for islanded operation scenarios, ensuring critical loads can be served by solar + battery during grid outages.
- **Battery Arbitrage Revenue Maximization**: Use day-ahead and intraday price forecasts to optimize battery charge/discharge cycles for maximum arbitrage revenue while respecting degradation constraints.
- **Virtual Power Plant Aggregation**: Aggregate distributed solar, battery, and flexible load resources into a virtual power plant that participates in wholesale energy and ancillary service markets.
- **REC Compliance Matching**: Automatically match renewable energy certificates against electricity consumption by region, vintage, and source type to demonstrate compliance with renewable portfolio standards.

## Best Practices

- **Calibrate Solar Models with Site Data**: Generic PV models have 10-15% error. Install a pyranometer and reference cell for at least one year to calibrate the site-specific model, reducing forecast error to 3-5%.
- **Use Ensemble Forecasts**: No single forecasting model is best in all weather conditions. Combine NWP-based, satellite-based, and persistence models with weighted averaging or stacking for 15-20% error reduction.
- **Model Battery Degradation**: Every charge-discharge cycle degrades lithium-ion batteries. Dispatch optimization that ignores degradation overestimates revenue by 20-40%. Include cycle-counting and capacity fade models in your objective function.
- **Reserve for Ancillary Services**: Batteries earn more from frequency regulation than from energy arbitrage in many markets. Reserve 20-30% of capacity for high-value ancillary services rather than committing everything to energy markets.
- **Account for Curtailment**: Solar and wind farms are often curtailed when grid congestion occurs. Your generation forecast must include expected curtailment hours, not just theoretical output, for accurate market bidding.
- **Monitor Inverter Clipping**: Solar systems with DC:AC ratios > 1.2 lose energy to inverter clipping during peak irradiance. Model the clipping loss explicitly rather than using nameplate capacity × capacity factor.
- **Track REC Vintage Separately**: RECs from different vintages have different market values and regulatory eligibility. Mixing vintages in your portfolio without tracking leads to compliance issues and value loss.
- **Consider Wake Effects in Wind Farms**: Wake losses in wind farms can reduce farm-level output by 10-20% below turbine-level sums. Use wake models (Jensen, Gaussian) for accurate farm-level forecasting.

## Key Metrics & Formulas

| Metric | Formula | Description |
|--------|---------|-------------|
| **Capacity Factor** | `Actual_output / (Rated_power × hours)` | Fraction of theoretical maximum output achieved |
| **Solar POA Irradiance** | `GHI × cos(tilt) × orientation_factor` | Plane-of-array irradiance on tilted panels |
| **Wind Power Curve** | `P = P_rated × ((v - v_in) / (v_rated - v_in))³` | Cubic relationship between wind speed and power |
| **Battery Round-Trip Efficiency** | `Energy_out / Energy_in` | Fraction of energy recovered after charge+discharge |
| **Arbitrage Revenue** | `Σ(Discharge × Price_high) - Σ(Charge × Price_low)` | Revenue from buying low, selling high |
| **Wake Loss** | `1 - (2/(1 + spacing/D))² × factor` | Jensen wake model for wind farm losses |
| **REC Coverage** | `RECs_retired / Total_consumption_MWh` | Percentage of consumption matched by RECs |

## Related Modules

- [green-computing](../green-computing/GROK.md) — Carbon-aware workload scheduling aligned with renewable availability. Schedules compute workloads to coincide with peak renewable generation.
- [carbon-tracking](../carbon-tracking/GROK.md) — Scope 2 emissions accounting for renewable procurement. Uses REC and PPA data for market-based emissions calculations.
- [green-it](../green-it/GROK.md) — Data center renewable energy integration. Addresses the infrastructure side of renewable energy adoption in IT operations.
- [circular-economy](../circular-economy/GROK.md) — End-of-life management for solar panels, wind blades, and batteries. Handles the circularity challenges unique to renewable energy equipment.

---

## Advanced Configuration

The renewable energy module supports advanced configuration for forecasting accuracy, battery management, and market participation. These options are available through the `AdvancedConfig` class or via environment variables.

```python
from renewable_energy import AdvancedConfig

config = AdvancedConfig(
    # Solar forecasting
    solar_forecast_model="ensemble",  # nwp, satellite, ml, ensemble
    solar_horizon_hours=48,
    solar_update_interval_minutes=15,
    solar_temperature_coefficient=-0.004,
    solar_soiling_model="linear",  # linear, exponential, none

    # Wind forecasting
    wind_forecast_model="physical",  # physical, statistical, ml, ensemble
    wind_wake_model="jensen",  # jensen, gaussian, flow_model
    wind_turbine_data_source="manufacturer",  # manufacturer, measured, iec
    wind_air_density_correction=True,

    # Battery management
    battery_degradation_model="cycling",  # cycling, calendar, combined
    battery_thermal_model="lumped",  # lumped, spatial, electrochemical
    battery_soh_initial=1.0,
    battery_replacement_cost_per_kwh=350,
    battery_max_cycles=6000,

    # Market participation
    market_operator="PJM",
    bid_lead_time_hours=12,
    imbalance_penalty_cents=5.0,
    reserve_margin_percent=10,

    # Microgrid
    microgrid_import_limit_kw=500,
    microgrid_export_limit_kw=200,
    microgrid_frequency_setpoint_hz=60.0,
    microgrid_voltage_setpoint_v=480
)
```

### Weather Data Source Configuration

```python
from renewable_energy import WeatherConfig

weather_config = WeatherConfig(
    primary_source="open_meteo",  # open_meteo, nwp, satellite
    fallback_sources=["windy", "noaa_gfs"],

    # NWP configuration
    nwp_model="gfs",  # gfs, ecmwf, hrrr, nam
    nwp_resolution_km=25,
    nwp_update_interval_hours=6,

    # Satellite configuration
    satellite_source="goes",  # goes, msg, himawari
    satellite_resolution_km=2,
    satellite_update_interval_minutes=10,

    # Site-specific data
    pyranometer_enabled=True,
    anemometer_enabled=True,
    temperature_sensor_enabled=True
)
```

## Architecture Patterns

### Ensemble Forecasting

Combine multiple forecast models for improved accuracy:

```python
from renewable_energy import EnsembleSolarForecaster

ensemble = EnsembleSolarForecaster(
    models={
        "nwp": {"weight": 0.4, "model": "gfs"},
        "satellite": {"weight": 0.3, "model": "goes"},
        "persistence": {"weight": 0.15},
        "ml": {"weight": 0.15, "model": "lstm"}
    },
    rebalance_interval_hours=6
)

forecast = ensemble.forecast_next_24h()
print(f"Ensemble forecast: {forecast.total_kwh:.1f} kWh")
print(f"Uncertainty: +/- {forecast.uncertainty_percent:.1f}%")
```

### Battery Dispatch Optimization

```python
from renewable_energy import BatteryDispatchOptimizer

optimizer = BatteryDispatchOptimizer(
    capacity_kwh=1000,
    max_charge_kw=250,
    max_discharge_kw=250,
    degradation_cost_per_kwh=0.05
)

# Optimize for multiple objectives
schedule = optimizer.optimize(
    prices=hourly_prices,
    solar_forecast=hourly_solar,
    load_forecast=hourly_load,
    objectives=["maximize_revenue", "minimize_degradation"],
    constraints={"min_soc": 0.1, "max_soc": 0.95}
)
```

### Virtual Power Plant Aggregation

```python
from renewable_energy import VirtualPowerPlant

vpp = VirtualPowerPlant(name="Regional VPP")

# Add distributed resources
vpp.add_resource(type="solar", capacity_kw=500, location="Site A")
vpp.add_resource(type="battery", capacity_kwh=200, max_power_kw=50, location="Site B")
vpp.add_resource(type="flexible_load", max_shift_kw=100, location="Site C")

# Optimize VPP dispatch
dispatch = vpp.optimize_dispatch(
    market_price_forecast=hourly_prices,
    grid_services_needed=["frequency_regulation", "peak_shaving"]
)
print(f"VPP output: {dispatch.total_output_kw:.0f} kW")
print(f"Revenue: ${dispatch.total_revenue_usd:.2f}")
```

## Integration Guide

### OpenEI / OpenWeather Integration

```python
from renewable_energy import OpenMeteoClient, OpenEIClient

# OpenMeteo weather data
meteo = OpenMeteoClient()
forecast = meteo.get_forecast(
    latitude=37.77,
    longitude=-122.42,
    hourly=["solar_radiation", "wind_speed", "temperature"]
)

# OpenEI utility rate data
openei = OpenEIClient()
rates = openei.get_rates(
    utility="PG&E",
    sector="commercial",
    state="CA"
)
```

### ISO/RTO Market Integration

```python
from renewable_energy import ISOConnector

# PJM market connector
pjm = ISOConnector(market="PJM")
pjm.configure(
    account_id="your-account",
    api_key="your-key",
    node="WESTJ_1_NI"
)

# Get day-ahead prices
prices = pjm.get_day_ahead_prices(date="2025-01-15")

# Submit bids
bid = pjm.submit_bid(
    quantity_mwh=100,
    price_per_mwh=45.00,
    bid_type="supply"
)
```

### REC Registry Integration

```python
from renewable_energy import MRETSConnector, NARConnector

# M-RETS (Midwest Renewable Energy Tracking System)
mrets = MRETSConnector(account_id="your-account")
mrets.issue_certificate(
    generator_id="SOLAR-001",
    mwh=100,
    vintage=2025,
    fuel_type="solar"
)

# NAR (National Accounts Registry)
nar = NARConnector()
nar.retire_certificate(
    certificate_id="REC-2025-12345",
    retirement_reason="Scope 2 compliance",
    retired_by="Acme Corp"
)
```

## Performance Optimization

### Forecast Caching

```python
from renewable_energy import ForecastCache

cache = ForecastCache(
    backend="redis",
    redis_url="redis://localhost:6379",
    solar_ttl_seconds=900,  # 15 minutes
    wind_ttl_seconds=600    # 10 minutes
)

# Cached solar forecast
solar = SolarForecaster(cache=cache)
forecast = solar.forecast_next_24h()  # Uses cache if available
```

### Battery Optimization Solver

```python
from renewable_energy import BatterySolver

solver = BatterySolver(
    solver="gurobi",  # gurobi, cplex, coin-or, scip
    time_limit_seconds=30,
    mip_gap=0.01
)

# Solve large-scale battery scheduling problem
schedule = solver.optimize(
    battery_capacity_kwh=5000,
    horizon_hours=168,  # 1 week
    prices=weekly_prices,
    solar_forecast=weekly_solar
)
```

## Security Considerations

### Market Communication Security

```python
from renewable_energy import SecureMarketConnector

connector = SecureMarketConnector(
    market="PJM",
    tls_cert="/certs/client.pem",
    tls_key="/certs/client.key",
    ca_cert="/certs/ca.pem",
    api_key_vault="aws_secrets_manager"
)
```

### Microgrid Control Security

```python
from renewable_energy import SecureMicrogridController

controller = SecureMicrogridController(
    scada_endpoint="https://scada.internal:443",
    auth_method="mutual_tls",
    command_signing=True,
    audit_logging=True
)
```

## Troubleshooting Guide

| Issue | Possible Cause | Resolution |
|-------|---------------|------------|
| Solar forecast too high | Soiling or shading not modeled | Calibrate with site measurements |
| Wind forecast inaccurate | Wake effects underestimated | Use Gaussian wake model, add SCADA data |
| Battery degradation faster than expected | Aggressive cycling or temperature | Review dispatch schedule, check thermal management |
| REC retirement failed | Certificate already retired | Check certificate status before retirement |
| Market bid rejected | Price outside allowed range | Verify market rules, check bid constraints |

```python
# Diagnostic script
from renewable_energy import DiagnosticRunner

diag = DiagnosticRunner(site="Solar Farm Alpha")
results = diag.run_all()
for check in results:
    status = "PASS" if check.passed else "FAIL"
    print(f"[{status}] {check.name}: {check.message}")
```

## API Reference

### SolarForecaster

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `forecast_next_24h(temp_c)` | temperature: float | `List[HourForecast]` | 24-hour solar forecast |
| `forecast_next_7d()` | - | `List[DayForecast]` | 7-day solar forecast |
| `calibrate(measurements)` | measurements: List[float] | `None` | Calibrate with site data |

### BatteryOptimizer

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `optimize_for_arbitrage(prices, soc)` | prices: List[float], soc: float | `List[Dispatch]` | Optimize for price arbitrage |
| `optimize_for_self_consumption(solar, load)` | solar: List[float], load: List[float] | `List[Dispatch]` | Maximize self-consumption |
| `get_degradation()` | - | `DegradationReport` | Current battery health status |

### MicrogridManager

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `optimize_dispatch(solar, price, mode)` | parameters | `DispatchSchedule` | Optimize microgrid dispatch |
| `simulate_island(critical_loads)` | loads: List[float] | `IslandResult` | Simulate islanded operation |
| `get_black_start_sequence()` | - | `List[Command]` | Black start procedure |

## Data Models

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class SolarForecast:
    time: datetime
    power_kw: float
    capacity_factor: float
    irradiance_w_m2: float
    temperature_c: float
    confidence: float

@dataclass
class WindForecast:
    time: datetime
    power_kw: float
    capacity_factor: float
    wind_speed_ms: float
    wind_direction_deg: float
    air_density_kg_m3: float

@dataclass
class BatteryState:
    soc: float
    soh: float
    temperature_c: float
    charge_power_kw: float
    discharge_power_kw: float
    cycles_count: int
    remaining_capacity_kwh: float

@dataclass
class DispatchSchedule:
    timestamps: List[datetime]
    solar_kwh: List[float]
    battery_kwh: List[float]
    grid_import_kwh: List[float]
    grid_export_kwh: List[float]
    total_revenue_usd: float
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

RUN pip install renewable-energy[all]

COPY config.yaml /etc/renewable-energy/config.yaml

HEALTHCHECK --interval=30s --timeout=5s \
  CMD python -c "from renewable_energy import health_check; health_check()"

ENTRYPOINT ["renewable-energy"]
CMD ["serve", "--config", "/etc/renewable-energy/config.yaml"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: renewable-energy-optimizer
spec:
  replicas: 2
  selector:
    matchLabels:
      app: renewable-energy
  template:
    spec:
      containers:
      - name: optimizer
        image: renewable-energy:1.0.0
        env:
        - name: WEATHER_API_KEY
          valueFrom:
            secretKeyRef:
              name: weather-keys
              key: open-meteo
```

## Monitoring & Observability

### Metrics Collection

```python
from renewable_energy import MetricsCollector

collector = MetricsCollector()

# Register custom metrics
collector.register_gauge("solar_output_kw", "Current solar output")
collector.register_gauge("battery_soc_percent", "Battery state of charge")
collector.register_counter("energy_traded_mwh", "Total energy traded")
collector.register_histogram("forecast_error_percent", "Forecast accuracy")
```

### Dashboard Integration

```python
from renewable_energy import DashboardExporter

dashboard = DashboardExporter(
    grafana_url="https://grafana.internal",
    datasource="renewable_energy"
)

# Push real-time data
dashboard.push_metrics({
    "solar_output_kw": 450,
    "battery_soc": 0.75,
    "grid_frequency_hz": 60.02
})
```

## Testing Strategy

```python
import pytest
from renewable_energy import SolarForecaster, BatteryOptimizer

class TestSolarForecaster:
    def test_forecast_accuracy(self):
        solar = SolarForecaster(capacity_kw=500)
        forecast = solar.forecast_next_24h(temperature_c=25.0)
        assert len(forecast) == 24
        assert all(f.power_kw >= 0 for f in forecast)
        assert all(f.capacity_factor <= 1.0 for f in forecast)

class TestBatteryOptimizer:
    def test_arbitrage_profit(self):
        battery = BatteryOptimizer(capacity_kwh=1000, max_charge_kw=250)
        prices = [45, 42, 38, 35, 33, 30, 28, 32, 48, 65, 85, 95]
        schedule = battery.optimize_for_arbitrage(prices=prices, current_soc=0.5)
        profit = sum(s.revenue_usd for s in schedule)
        assert profit > 0  # Should be profitable
```

## Versioning & Migration

### Semantic Versioning

- **MAJOR**: Breaking changes to API, forecast model changes
- **MINOR**: New market integrations, new battery models
- **PATCH**: Bug fixes, performance improvements

### Migration Guide

```python
# v1.x to v2.x migration
# Old API
solar = SolarForecaster(capacity=500, lat=37.77, lon=-122.42)

# New API
solar = SolarForecaster(
    capacity_kw=500,
    latitude=37.77,
    longitude=-122.42,
    tilt_degrees=30
)
```

## Glossary

| Term | Definition |
|------|-----------|
| **Capacity Factor** | Ratio of actual output to theoretical maximum output |
| **POA Irradiance** | Plane-of-array irradiance — solar radiation on tilted panel surface |
| **BESS** | Battery Energy Storage System |
| **SOC** | State of Charge — current energy level as percentage of capacity |
| **SOH** | State of Health — battery capacity relative to original capacity |
| **PPA** | Power Purchase Agreement — long-term contract for electricity purchase |
| **REC** | Renewable Energy Certificate — proof of renewable electricity generation |
| **GO** | Guarantee of Origin — European equivalent of REC |
| **VPP** | Virtual Power Plant — aggregation of distributed energy resources |
| **DER** | Distributed Energy Resource — small-scale energy generation or storage |
| **Ancillary Services** | Grid support services like frequency regulation and voltage support |
| **Curtailment** | Reduction of renewable output due to grid congestion or oversupply |

## Changelog

### v1.0.0 (2025-01-15)
- Initial release with solar and wind forecasting
- Battery storage optimization
- Basic market trading

### v1.1.0 (2025-02-01)
- Added microgrid management
- Improved forecast accuracy with ensemble models
- Added REC tracking

### v1.2.0 (2025-03-01)
- Added virtual power plant aggregation
- Performance improvements in battery optimization
- Added multi-market support

## Contributing Guidelines

1. **Fork the repository** and create a feature branch from `main`
2. **Write tests** for all new functionality with >80% coverage
3. **Follow PEP 8** style guidelines with type hints
4. **Update documentation** for any API changes
5. **Add changelog entries** under `[Unreleased]` section
6. **Submit a pull request** with a clear description of changes

### Code Review Checklist

- [ ] Tests pass and coverage meets threshold
- [ ] Forecast models are validated against historical data
- [ ] Battery degradation is modeled accurately
- [ ] Market integration follows ISO/RTO rules
- [ ] No hardcoded market data or prices

## License

This module is licensed under the Apache License, Version 2.0. See the LICENSE file for full terms.

Copyright 2025 Renewable Energy Contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
