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
