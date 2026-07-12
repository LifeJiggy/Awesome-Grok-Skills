---
name: "satellite-systems"
category: "space-tech"
version: "1.0.0"
tags: ["space-tech", "satellite-systems", "constellation", "adcs", "orbit-determination"]
---

# Satellite Systems Toolkit

## Overview

The Satellite Systems module provides comprehensive tools for satellite constellation management, orbit determination, attitude control systems (ADCS), power and thermal subsystem modeling, communication link budget analysis, and space debris tracking. Designed for satellite operations engineers, constellation architects, and mission planners, this toolkit covers the full satellite lifecycle from initial orbit design through end-of-life deorbit planning.

Constellation management includes Walker delta constellation synthesis, coverage analysis with ground-track repeat patterns, inter-satellite link geometry, and phasing optimization. Orbit determination supports both ground-based tracking (range, range-rate, angle measurements) and onboard GPS-based methods with Kalman filtering. ADCS modeling covers reaction wheel sizing, magnetic torquer control laws, star tracker accuracy budgets, and full 3-degree-of-freedom attitude dynamics simulation.

The module implements realistic subsystem power budgets (solar array generation, battery cycling, eclipse modeling), thermal control analysis (passive radiator sizing, heater power requirements), and communication link budgets accounting for free-space path loss, atmospheric absorption, polarization mismatch, pointing losses, and rain fade. Deorbit planning includes compliance checks against the 25-year deorbit guideline and active deorbit mechanism sizing (drag sails, electrodynamic tethers, propulsion-based disposal).

## Core Capabilities

- **Constellation Management**: Walker delta/star constellation synthesis, ground-track analysis, coverage optimization, inter-satellite link geometry, phasing strategies
- **Orbit Determination**: Batch least-squares and sequential Kalman filter OD from range/range-rate/angles, onboard GPS orbit determination, state transition matrix computation
- **Attitude Control Systems**: Reaction wheel pyramid sizing, magnetic torquer moment computation, star tracker/IMU accuracy budgets, PD controller tuning, detumbling algorithms
- **Power Subsystem**: Solar array power generation (eclipse modeling, sun angle, degradation), battery state-of-charge cycling, depth-of-discharge management, power budget reconciliation
- **Thermal Control**: Passive radiator sizing, Multi-Layer Insulation (MLI) analysis, heater power budgets, thermal equilibrium with orbital heat flux variations
- **Communication Link Budgets**: Full link budget chain from transmitter to receiver, free-space path loss, atmospheric and rain attenuation, G/T and C/N0 computation
- **Deorbit Planning**: 25-year compliance analysis, collision probability estimation, drag sail sizing, electrodynamic tether deorbit times, controlled disposal orbit selection
- **Space Debris Tracking**: TLE parsing and propagation, conjunction assessment, miss distance computation, probability of collision calculation

## Usage Examples

### Walker Constellation Design

```python
from satellite_systems import ConstellationManager
import numpy as np

constellation = ConstellationManager()

walker = constellation.walker_delta(
    total_satellites=66,
    orbital_planes=6,
    inclination_deg=53.0,
    altitude_km=550,
    phasing_offset=1,
)

print(f"Constellation:       {walker['total_sats']} sats")
print(f"Planes:              {walker['num_planes']}, Sats/plane: {walker['sats_per_plane']}")
print(f"RAAN spacing:        {walker['raan_spacing_deg']:.1f}°")
print(f"True anomaly spacing: {walker['ta_spacing_deg']:.1f}°")
print(f"Orbital period:      {walker['period_hours']:.2f} hours")

# Coverage analysis
coverage = constellation.analyze_coverage(
    walker_result=walker,
    grid_resolution_deg=2.0,
    simulation_days=1,
)
print(f"\nCoverage Analysis:")
print(f"  Average visibility:  {coverage['avg_visibility']:.2f} satellites")
print(f"  Max gap (minutes):   {coverage['max_gap_minutes']:.1f}")
print(f"  Coverage (%):        {coverage['coverage_pct']:.1f}%")

# Inter-satellite link geometry
isl = constellation.compute_isl_geometry(walker_result=walker)
print(f"\nISL Geometry:")
print(f"  Max link distance:   {isl['max_distance_km']:.0f} km")
print(f"  Min link distance:   {isl['min_distance_km']:.0f} km")
print(f"  Mean elevation:      {isl['mean_elevation_deg']:.1f}°")
```

### Orbit Determination from Tracking

```python
from satellite_systems import OrbitDetermination
import numpy as np

od = OrbitDetermination(body="earth")

# Simulated observations: (time_s, range_m, range_rate_mps)
observations = [
    (0.0,    6_900_000, -120.5),
    (600.0,  6_850_000,  -85.2),
    (1200.0, 6_920_000,   45.3),
    (1800.0, 7_100_000,  110.8),
    (2400.0, 6_950_000,   78.4),
    (3000.0, 6_800_000,  -30.1),
    (3600.0, 6_980_000,   92.6),
]

result = od.batch_least_squares(
    observations=observations,
    initial_guess=np.array([7_000_000, 0, 0, 0, 7_500, 0]),
)

print(f"\nOrbit Determination Result:")
print(f"  Position:      {np.linalg.norm(result['position']):.0f} m")
print(f"  Velocity:      {np.linalg.norm(result['velocity']):.0f} m/s")
print(f"  Semi-major axis: {result['sma_km']:.1f} km")
print(f"  Eccentricity:  {result['eccentricity']:.6f}")
print(f"  Inclination:   {result['inclination_deg']:.3f}°")
print(f"  Residual RMS:  {result['residual_rms']:.2f} m")
print(f"  Iterations:    {result['iterations']}")

# Covariance analysis
cov = od.compute_covariance(observations, result['state_vector'])
print(f"\nPosition 3σ uncertainty: {cov['position_3sigma_m']:.1f} m")
print(f"Velocity 3σ uncertainty: {cov['velocity_3sigma_mps']:.2f} m/s")
```

### ADCS Reaction Wheel Sizing

```python
from satellite_systems import AttitudeController
import numpy as np

adcs = AttitudeController()

wheels = adcs.size_reaction_wheels(
    desired_pointing_accuracy_deg=0.01,
    max_slew_rate_deg_per_sec=1.0,
    max_torque_nm=0.05,
    momentum_storage_required_nm_s=10.0,
    spacecraft_inertia_kgm2=np.diag([120, 100, 80]),
)

print(f"\nReaction Wheel Sizing:")
print(f"  Configuration:  {wheels['configuration']}")
print(f"  Wheel speed:     {wheels['max_speed_rpm']:.0f} RPM")
print(f"  Wheel mass:      {wheels['total_mass_kg']:.1f} kg")
print(f"  Power:           {wheels['power_watts']:.1f} W")

# Detumbling simulation
detumble = adcs.simulate_detumbling(
    initial_angular_velocity_rad_s=np.array([0.1, -0.05, 0.02]),
    inertia_kgm2=np.diag([120, 100, 80]),
    magnetic_field_t=np.array([2e-5, 0, -4e-5]),
    duration_s=300,
)
print(f"\nDetumbling:")
print(f"  Time to <1°/s:  {detumble['settling_time_s']:.0f} s")
print(f"  Final rate:      {detumble['final_rate_deg_s']:.3f}°/s")
print(f"  Magnetic torque: {detumble['max_torque_nm']:.4f} Nm")
```

### Communication Link Budget

```python
from satellite_systems import LinkBudget

link = LinkBudget(
    tx_power_watts=10.0,
    tx_gain_dbi=15.0,
    rx_gain_dbi=25.0,
    frequency_ghz=12.0,
    distance_km=36_000,
    tx_line_loss_db=0.5,
    rx_line_loss_db=0.3,
    pointing_loss_db=0.5,
)

budget = link.compute()
print(f"\nLink Budget (12 GHz GEO):")
print(f"  EIRP:              {budget['eirp_dbw']:.1f} dBW")
print(f"  Free-space loss:   {budget['fspl_db']:.1f} dB")
print(f"  Atmospheric loss:  {budget['atm_loss_db']:.2f} dB")
print(f"  C/N0:              {budget['cn0_db_hz']:.1f} dB-Hz")
print(f"  Link margin:       {budget['margin_db']:.1f} dB")
print(f"  Achievable rate:   {budget['max_data_rate_mbps']:.1f} Mbps")
```

### Power Budget

```python
from satellite_systems import PowerSubsystem

power = PowerSubsystem(
    solar_array_area_m2=2.5,
    solar_cell_efficiency=0.28,
    eclipse_fraction=0.35,
    average_power_consumption_w=50,
    battery_capacity_wh=200,
    degradation_factor=0.95,
)

budget = power.compute_budget()
print(f"\nPower Budget:")
print(f"  Solar generation (EOL): {budget['solar_generation_eol_w']:.1f} W")
print(f"  Average load:           {budget['average_load_w']:.1f} W")
print(f"  Peak load:              {budget['peak_load_w']:.1f} W")
print(f"  Battery DoD:            {budget['depth_of_discharge']:.1%}")
print(f"  Power margin:           {budget['margin_w']:.1f} W")
print(f"  Eclipse duration:       {budget['eclipse_minutes']:.1f} min")
print(f"  Battery cycles (LEO):   {budget['daily_cycles']:.1f} /day")
```

## Best Practices

1. **Validate Walker constellation phasing** — incorrect phasing offsets produce ground-track gaps. Verify that the phasing parameter F satisfies 0 ≤ F < P (number of planes) and produces the desired harmonic relationship between planes.
2. **Include atmospheric drag in LEO orbit propagation** — below 600 km, atmospheric drag dominates secular evolution. Use NRLMSISE-00 density model, not exponential, for accurate lifetime predictions.
3. **Size reaction wheels for worst-case disturbance torque** — include gravity gradient, solar radiation pressure, magnetic residual dipole, and aerodynamic torques. Apply 30% margin on momentum storage.
4. **Account for solar cell degradation** — end-of-life (EOL) efficiency is typically 70-80% of beginning-of-life (BOL) after 15 years in GEO. Apply radiation damage models based on orbital environment.
5. **Verify link budget against rain fade** — for Ka-band and above, rain attenuation exceeds 10 dB at 0.01% exceedance in tropical regions. Always include ITU-R P.618 rain fade models for service availability analysis.
6. **Check 25-year deorbit compliance early** — if your mission altitude exceeds ~600 km, the 25-year guideline may require active deorbit. Include this in the mass/power budget from Phase A.
7. **Use proper TLE propagation** — SGP4/SDP4 propagators have ~1 km accuracy for LEO TLEs. Don't use Keplerian propagation on TLE data; always feed through SGP4.
8. **Kalman filter initialization matters** — poor initial state estimates cause filter divergence. Use batch least-squares for initial OD, then hand off to sequential Kalman filter for tracking.

## Related Modules

- [aerospace-engineering](../aerospace-engineering/GROK.md) — Orbital mechanics, propulsion, trajectory optimization
- [mission-planning](../mission-planning/GROK.md) — Timeline scheduling, launch windows, contingency planning
- [ground-stations](../ground-stations/GROK.md) — Antenna tracking, signal processing, telemetry decoding
- [space-data](../space-data/GROK.md) — Ephemeris processing, telemetry analysis, space weather
