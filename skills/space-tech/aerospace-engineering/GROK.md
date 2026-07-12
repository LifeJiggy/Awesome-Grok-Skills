---
name: "aerospace-engineering"
category: "space-tech"
version: "1.0.0"
tags: ["space-tech", "aerospace-engineering", "orbital-mechanics", "propulsion", "trajectory-optimization"]
---

# Aerospace Engineering Toolkit

## Overview

The Aerospace Engineering module provides comprehensive computational tools for orbital mechanics, propulsion system modeling, structural analysis, thermal protection systems, and trajectory optimization. Built on classical astrodynamics equations and modern numerical methods, this toolkit enables rapid prototyping of launch vehicle design, mission delta-v budgeting, and aerodynamic analysis for atmospheric entry vehicles. All calculations follow standard aerospace reference frames (ECI, ECEF, LVLH) and support both SI and Imperial unit systems.

The module implements patched-conic approximations, Lambert solvers, Hohmann and bi-elliptic transfer algorithms, and high-fidelity numerical propagators using Cowell's method. Propulsion modeling covers chemical (bipropellant, solid), electric (ion, Hall-effect), and experimental (VASIMR, nuclear thermal) systems with realistic specific impulse curves and mass flow rate calculations. Structural analysis includes buckling criteria, vibration mode estimation, and load factor computation under launch, cruise, and re-entry flight regimes.

Designed for mission architects, flight dynamics engineers, and aerospace researchers, this toolkit bridges the gap between high-level mission design tools (like GMAT or STK) and first-principles Python implementations. Every function returns intermediate computation results for verification and integrates seamlessly with NumPy/SciPy numerical backends.

## Core Capabilities

- **Orbital Mechanics**: Keplerian orbit propagation, orbital element conversions (Keplerian ↔ Cartesian), relative motion (Hill-Clohessy-Wiltshire), and Lagrange point computation
- **Delta-v Budgeting**: Full mission delta-v accounting including gravity losses, drag losses, steering losses, and plane-change costs
- **Propulsion Modeling**: Chemical, electric, and advanced propulsion system performance modeling with throttle profiles and duty cycles
- **Trajectory Optimization**: Hohmann transfers, bi-elliptic transfers, low-thrust spiral trajectories, and gravity-assist trajectory design
- **Aerodynamic Analysis**: Hypersonic drag coefficient estimation, heating rate calculations, and ballistic coefficient computation for re-entry vehicles
- **Structural Analysis**: Launch vehicle load factor computation, buckling margin analysis, and vibration frequency estimation
- **Thermal Protection**: Heat shield sizing, ablation modeling, and thermal equilibrium calculations for atmospheric entry
- **Flight Dynamics**: Six-degree-of-freedom simulation, attitude dynamics, and guidance-law implementation (gravity turn, pitch-over)

## Usage Examples

### Hohmann Transfer Computation

```python
from aerospace_engineering import OrbitalMechanics
import numpy as np

orbital = OrbitalMechanics(central_body="earth")

leo_radius = 6_571_000   # 200 km altitude LEO (meters)
geo_radius = 42_164_000  # GEO radius (meters)

hohmann = orbital.hohmann_transfer(leo_radius, geo_radius)

print(f"Transfer burn 1:       {hohmann['dv1']:.3f} m/s")
print(f"Transfer burn 2:       {hohmann['dv2']:.3f} m/s")
print(f"Total delta-v:         {hohmann['dv_total']:.3f} m/s")
print(f"Transfer time:         {hohmann['transfer_time_hours']:.1f} hours")
print(f"Phase angle at TIG:    {hohmann['phase_angle_deg']:.2f} degrees")
```

### Propulsion System Performance

```python
from aerospace_engineering import PropulsionSystem

engine = PropulsionSystem(
    name="RS-25",
    thrust_vacuum=2_278_000,   # Newtons
    thrust_sl=1_860_000,
    isp_vacuum=452,            # seconds
    isp_sl=366,
    propellant_mass=352_700,   # kg (SSME)
    oxidizer_fuel_ratio=6.0,
)

print(f"Mass flow rate:        {engine.mass_flow_rate:.2f} kg/s")
print(f"Exhaust velocity (vac): {engine.exhaust_velocity_vac:.1f} m/s")
print(f"Delta-v capacity:      {engine.delta_v_capacity():.1f} m/s")
print(f"TWR (sea level):       {engine.twr(5_400_000):.2f}")

# Throttle profile analysis
throttle_curve = engine.throttle_profile(
    throttle_range=(0.65, 1.0),
    steps=10,
)
for point in throttle_curve:
    print(f"  Throttle {point['throttle_pct']:.0f}%: "
          f"thrust={point['thrust_n']:.0f} N, "
          f"isp={point['isp_s']:.1f} s")
```

### Re-entry Heating Analysis

```python
from aerospace_engineering import ThermalProtectionSystem, ReentryVehicle

vehicle = ReentryVehicle(
    mass=8_000,               # kg
    reference_area=12.5,       # m^2
    nose_radius=0.5,           # meters (blunt body)
    ballistic_coefficient=None,  # auto-computed
)

tp = ThermalProtectionSystem(vehicle)
heating = tp.stagnation_point_heating(
    velocity=7_800,            # m/s at entry interface
    atmosphere_density=0.001,  # kg/m^3
    nose_radius=0.5,
)
print(f"Peak heat flux:    {heating['heat_flux']:.2f} W/cm^2")
print(f"Total heat load:   {heating['total_heat_load']:.2f} J/cm^2")
print(f"Heat shield mass:  {heating['shield_mass_kg']:.1f} kg")

# Ablation depth estimation
ablation = tp.ablation_model(
    heat_flux_w_cm2=heating['heat_flux'],
    exposure_time_s=heating['heating_duration_s'],
    material="PICA-X",
)
print(f"Ablation depth:    {ablation['depth_mm']:.2f} mm")
```

### Launch Vehicle Load Factors

```python
from aerospace_engineering import LaunchVehicleAnalysis

lv = LaunchVehicleAnalysis(
    dry_mass=25_000,
    propellant_mass=220_000,
    thrust_sea_level=7_600_000,
    reference_area=11.3,
    drag_coefficient=0.3,
)

profile = lv.ascent_profile(
    initial_altitude=0,
    target_altitude=200_000,
    pitch_over_altitude=1_000,
    max_q_altitude=11_000,
)
for point in profile:
    print(f"  Alt={point['altitude']/1000:.1f}km  "
          f"q={point['dynamic_pressure']/1000:.1f}kPa  "
          f"n={point['load_factor']:.2f}g  "
          f"drag={point['drag_loss']:.1f}m/s")

# Vehicle mass budget summary
budget = lv.mass_budget-summary()
print(f"\nDry mass:      {budget['dry_mass_kg']:.0f} kg")
print(f"Propellant:    {budget['propellant_kg']:.0f} kg")
print(f"Payload:       {budget['payload_kg']:.0f} kg")
print(f"Mass fraction: {budget['mass_fraction']:.3f}")
```

### Lambert Problem Solver

```python
from aerospace_engineering import LambertSolver
import numpy as np

solver = LambertSolver(central_body="earth")

r1 = np.array([6_571_000, 0, 0])         # LEO position (m)
r2 = np.array([0, 42_164_000, 0])         # GEO position (m)
tof_s = 5.25 * 3600                        # 5.25 hours transfer time

result = solver.solve(r1, r2, tof_s, direction="prograde")
print(f"v1: {result['v1']} m/s")
print(f"v2: {result['v2']} m/s")
print(f"Delta-v1: {np.linalg.norm(result['v1'] - np.array([0, 7800, 0])):.1f} m/s")
```

### Gravity Assist Trajectory Design

```python
from aerospace_engineering import GravityAssistDesigner
import numpy as np

designer = GravityAssistDesigner(central_body="sun")

# Earth-Venus-Mars gravity assist trajectory
trajectory = designer.multi_gravity_assist(
    bodies=["earth", "venus", "mars"],
    departure_date="2028-09-01",
    arrival_date="2030-06-15",
    departure_c3_km2_s2=15.0,
    max_flyby_altitude_km=500,
)

print(f"Total delta-v:      {trajectory['total_dv_km_s']:.3f} km/s")
print(f"Flight time:        {trajectory['flight_days']:.0f} days")
print(f"Flyby altitudes:    {trajectory['flyby_altitudes_km']}")
print(f"Gravity assist dv:  {trajectory['assist_dv_km_s']:.3f} km/s")
for leg in trajectory['legs']:
    print(f"  {leg['from']}-{leg['to']}: {leg['tof_days']:.0f}d, "
          f"C3={leg['c3_km2_s2']:.1f} km²/s²")
```

### Orbital Element Conversions

```python
from aerospace_engineering import OrbitalMechanics
import numpy as np

orbital = OrbitalMechanics(central_body="earth")

# Convert Keplerian to Cartesian
cartesian = orbital.keplerian_to_cartesian(
    sma_km=6771,
    ecc=0.001,
    inc_deg=51.6,
    raan_deg=0.0,
    argp_deg=0.0,
    ta_deg=90.0,
)
print(f"Position (ECI): {cartesian['position_m']} m")
print(f"Velocity (ECI): {cartesian['velocity_mps']} m/s")

# Convert back to verify
keplerian = orbital.cartesian_to_keplerian(
    cartesian['position_m'],
    cartesian['velocity_mps'],
)
print(f"\nVerification:")
print(f"  SMA:  {keplerian['sma_km']:.1f} km")
print(f"  ECC:  {keplerian['eccentricity']:.6f}")
print(f"  INC:  {keplerian['inclination_deg']:.3f}°")
print(f"  RAAN: {keplerian['raan_deg']:.3f}°")
print(f"  TA:   {keplerian['true_anomaly_deg']:.3f}°")

# Relative motion (Hill-Clohessy-Wiltshire)
relative = orbital.hill_clohessy_wiltshire(
    chief_sma_km=6771,
    deputy_offset_m=np.array([100, 50, 25]),
    chief_velocity_mps=7670,
)
print(f"\nDeputy position (LVLH): {relative['position_lvlh_m']}")
print(f"Deputy velocity (LVLH): {relative['velocity_lvlh_mps']}")
```

## Best Practices

1. **Always verify orbital element validity** — check semi-major axis > 0, eccentricity in [0, 1) for bound orbits, and inclination in [0, π]. Invalid elements silently produce NaN in downstream calculations.
2. **Account for J2 perturbations early** — for LEO missions, J2-induced nodal regression can exceed 5°/day. Include J2 in any propagation lasting more than a few orbits.
3. **Use consistent reference frames** — ECI for orbit propagation, LVLH for relative motion, and ECEF for ground-track calculations. Mixing frames without proper rotation matrices is the #1 source of trajectory errors.
4. **Validate delta-v budgets against known mission data** — compare your Hohmann calculations against published mission delta-v (e.g., ISS resupply ~300 m/s LEO-to-LEO, GEO insertion ~1500 m/s from GTO).
5. **Apply safety margins on structural loads** — use 1.25× ultimate load factor and 1.1× on predicted heating rates. Spacecraft structures are designed to these margins per NASA-STD-5001.
6. **Check atmospheric model validity** — the exponential atmosphere model breaks down above ~100 km; use NRLMSISE-00 or similar for thermosphere/exosphere calculations.
7. **Numerical integrator selection matters** — use Dormand-Prince (RK45) for short arcs, Gauss-Jackson for long-duration orbit propagation, and Symplectic integrators for energy-conserving Kepler problems.
8. **Unit consistency is critical** — the module expects SI units (meters, kilograms, seconds). Always convert from common aerospace units (nautical miles, slugs, lbf) before calling functions.

## Related Modules

- [satellite-systems](../satellite-systems/GROK.md) — Orbit determination, ADCS, constellation management
- [mission-planning](../mission-planning/GROK.md) — Timeline scheduling, launch window calculation, contingency planning
- [ground-stations](../ground-stations/GROK.md) — Antenna tracking, signal processing, Doppler compensation
- [space-data](../space-data/GROK.md) — Ephemeris processing, space weather, telemetry analysis
