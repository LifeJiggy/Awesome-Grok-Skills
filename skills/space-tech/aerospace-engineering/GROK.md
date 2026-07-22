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

## Advanced Configuration

### Reference Frame Configuration
```python
from aerospace_engineering import ReferenceFrameConfig

config = ReferenceFrameConfig(
    primary_frame="ECI",
    secondary_frame="ECEF",
    precession_model="IAU2000",
    nutation_model="IAU2000",
    earth_rotation_model="IERS2010",
)
```

### Numerical Integrator Settings
```python
from aerospace_engineering import IntegratorConfig

integrator_config = IntegratorConfig(
    method="Dormand-Prince",
    order=5,
    step_size=10.0,  # seconds
    tolerance=1e-12,
    max_steps=100000,
    adaptive_step=True,
)
```

### Atmospheric Model Configuration
```python
from aerospace_engineering import AtmosphericConfig

atmo_config = AtmosphericConfig(
    model="NRLMSISE-00",
    solar_flux_f107=150.0,
    geomagnetic_index=30,
    date="2028-09-01T12:00:00Z",
    latitude=28.5,
    longitude=-80.6,
)
```

## Architecture Patterns

### Plugin System
The module uses a plugin architecture for extensibility:
```python
from aerospace_engineering import PluginManager

pm = PluginManager()
pm.register("custom_propulsion", CustomPropulsionPlugin())
pm.register("custom_gravity", CustomGravityPlugin())
```

### Observer Pattern for Live Trajectory Updates
```python
from aerospace_engineering import TrajectoryObserver

class MyObserver(TrajectoryObserver):
    def on_update(self, state):
        print(f"Position: {state.position}")
        print(f"Velocity: {state.velocity}")

observer = MyObserver()
trajectory.add_observer(observer)
```

### Factory Pattern for Vehicle Definitions
```python
from aerospace_engineering import VehicleFactory

factory = VehicleFactory()
vehicle = factory.create("falcon_heavy")
vehicle.configure_mission("mars_transfer")
```

## Integration Guide

### NumPy/SciPy Backend
```python
from aerospace_engineering import NumericalBackend

backend = NumericalBackend(
    use_numpy=True,
    use_scipy=True,
    parallel=False,
    precision="double",
)
```

### MATLAB Integration
```python
from aerospace_engineering import MATLABBridge

bridge = MATLABBridge()
bridge.connect()
result = bridge.run_matlab_function("ode45", args=[...])
bridge.disconnect()
```

### API Server Integration
```python
from aerospace_engineering import APIClient

client = APIClient(base_url="https://api.aerospace-engineering.io/v1")
result = client.compute_trajectory(mission_params)
```

## Performance Optimization

### Parallel Computation
```python
from aerospace_engineering import ParallelConfig

config = ParallelConfig(
    enabled=True,
    workers=8,
    chunk_size=1000,
    use_gpu=False,
)
```

### Caching Strategy
```python
from aerospace_engineering import CacheManager

cache = CacheManager(
    strategy="lru",
    max_size=1000,
    ttl=3600,
)
```

### Memory Management
```python
from aerospace_engineering import MemoryOptimizer

optimizer = MemoryOptimizer(
    max_memory_mb=4096,
    swap_threshold=0.8,
    gc_interval=100,
)
```

## Security Considerations

### Data Encryption
```python
from aerospace_engineering import SecurityConfig

security = SecurityConfig(
    encrypt_data=True,
    key_management="aws_kms",
    audit_logging=True,
)
```

### Access Control
```python
from aerospace_engineering import AccessControl

acl = AccessControl()
acl.add_role("mission_planner", permissions=["read", "execute"])
acl.add_role("analyst", permissions=["read"])
```

## Troubleshooting Guide

### Common Issues

1. **NaN Results**: Check orbital element validity and reference frame consistency
2. **Integration Errors**: Reduce step size or switch to implicit method
3. **Memory Overflow**: Enable memory optimization or use chunked processing
4. **Performance Issues**: Enable parallel computation or caching

### Debug Mode
```python
from aerospace_engineering import enable_debug

enable_debug(
    log_level="DEBUG",
    verbose_output=True,
    save_intermediate=True,
)
```

## API Reference

### Core Classes
- `OrbitalMechanics` - Core orbital mechanics calculations
- `PropulsionSystem` - Propulsion system modeling
- `ThermalProtectionSystem` - Thermal protection analysis
- `LaunchVehicleAnalysis` - Launch vehicle analysis
- `LambertSolver` - Lambert problem solver

### Core Functions
- `hohmann_transfer()` - Compute Hohmann transfer
- `bi_elliptic_transfer()` - Compute bi-elliptic transfer
- `lambert_solve()` - Solve Lambert problem
- `propagate_orbit()` - Propagate orbit forward/backward
- `compute_delta_v()` - Compute delta-v requirements

## Data Models

### Orbital State
```python
class OrbitalState:
    position: np.ndarray  # [x, y, z] in meters
    velocity: np.ndarray  # [vx, vy, vz] in m/s
    timestamp: float      # Julian date
    frame: str            # Reference frame identifier
```

### Mission Plan
```python
class MissionPlan:
    name: str
    objectives: List[str]
    timeline: List[MissionEvent]
    constraints: MissionConstraints
    resources: MissionResources
```

### Vehicle Configuration
```python
class VehicleConfig:
    name: str
    dry_mass: float
    propellant_mass: float
    thrust: float
    isp: float
    dimensions: VehicleDimensions
```

## Deployment Guide

### Container Deployment
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "aerospace_engineering.server"]
```

### Kubernetes Configuration
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aerospace-engineering
spec:
  replicas: 3
  selector:
    matchLabels:
      app: aerospace-engineering
```

## Monitoring & Observability

### Metrics Collection
```python
from aerospace_engineering import MetricsCollector

collector = MetricsCollector(
    backend="prometheus",
    endpoint="/metrics",
    labels={"service": "aerospace-engineering"},
)
```

### Logging Configuration
```python
from aerospace_engineering import Logger

logger = Logger(
    level="INFO",
    format="json",
    output="stdout",
)
```

## Testing Strategy

### Unit Tests
```python
import unittest
from aerospace_engineering import OrbitalMechanics

class TestOrbitalMechanics(unittest.TestCase):
    def test_hohmann_transfer(self):
        orbital = OrbitalMechanics(central_body="earth")
        result = orbital.hohmann_transfer(6_571_000, 42_164_000)
        self.assertGreater(result['dv_total'], 0)
```

### Integration Tests
```python
def test_full_mission_workflow():
    # Test complete mission planning workflow
    pass
```

## Versioning & Migration

### Version History
- v1.0.0 - Initial release
- v1.1.0 - Added gravity assist trajectories
- v1.2.0 - Performance optimizations

### Migration Guide
```python
# v1.0 to v1.1 migration
from aerospace_engineering import migrate_v1_to_v1_1
migrate_v1_to_v1_1(config_file="old_config.yaml")
```

## Glossary

- **Delta-v**: Change in velocity required for orbital maneuvers
- **Specific Impulse (Isp)**: Measure of propulsion efficiency
- **Lambert Problem**: Finding orbit connecting two points in given time
- **Hohmann Transfer**: Minimum energy two-impulse transfer between circular orbits
- **J2 Perturbation**: Earth's oblateness effect on orbits

## Changelog

### v1.2.0 (2028-09-01)
- Added parallel computation support
- Improved memory management
- Fixed integration accuracy issues

### v1.1.0 (2028-06-15)
- Added gravity assist trajectory design
- Enhanced atmospheric models
- New API server integration

### v1.0.0 (2028-03-01)
- Initial release with core functionality

## Contributing Guidelines

### Development Setup
```bash
git clone https://github.com/aerospace-engineering/aerospace-engineering.git
cd aerospace-engineering
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Code Style
- Follow PEP 8 for Python code
- Use type hints for all functions
- Write docstrings for public APIs

### Pull Request Process
1. Fork the repository
2. Create feature branch
3. Write tests
4. Update documentation
5. Submit pull request

## License

MIT License

Copyright (c) 2028 Aerospace Engineering Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Additional Reference Data

###常用 Orbital Parameters Reference

| Parameter | LEO (400 km) | MEO (20,200 km) | GEO (35,786 km) | Lunar Transfer |
|-----------|--------------|-----------------|-----------------|----------------|
| Semi-major axis (km) | 6,771 | 26,571 | 42,164 | 200,000+ |
| Orbital period (min) | 92.4 | 718 | 1,436 | Variable |
| Velocity (km/s) | 7.67 | 3.89 | 3.07 | 10.8+ |
| Delta-v from LEO (m/s) | 0 | 1,400 | 1,500 | 3,100+ |

### Engine Performance Comparison

| Engine | Thrust (kN) | Isp (vac) | Propellant | Application |
|--------|-------------|-----------|------------|-------------|
| RS-25 | 2,278 | 452 s | LOX/LH2 | SLS Core Stage |
| Merlin 1D | 845 | 311 s | LOX/RP-1 | Falcon 9 First Stage |
| Raptor | 2,300 | 380 s | LOX/CH4 | Starship |
| RL10 | 110 | 465 s | LOX/LH2 | Upper Stages |
| Hall Thruster | 0.001-0.01 | 1,500-3,000 s | Xenon | Station Keeping |

### Common Mission Delta-v Budgets

```python
# Reference delta-v budgets for common mission profiles
MISSION_BUDGETS = {
    "ISS_resupply_LEO": {
        "launch_to_LEO": 9400,      # m/s from surface
        "LEO_phasing": 50,          # m/s to match ISS
        "LEO_rendezvous": 100,      # m/s final approach
        "deorbit": 100,             # m/s
        "total_from_LEO": 250,      # m/s from LEO parking
    },
    "GEO_insertion": {
        "LEO_to_GTO": 2500,         # m/s
        "GTO_to_circularize": 1500, # m/s at apogee
        "inclination_correction": 1500,  # m/s for 28.5 to 0 deg
        "total_from_LEO": 5500,     # m/s
    },
    "mars_transfer": {
        "LEO_to_HCO": 3200,         # m/s to hyperbolic orbit
        "Mars_capture": 1400,       # m/s to Mars orbit
        "Mars_landing": 1400,       # m/s (EDL)
        "Mars_to_Earth": 5700,      # m/s total return
        "total_mission": 11700,     # m/s
    },
}
```

### Atmospheric Entry Corridor Limits

The entry corridor defines the acceptable range of entry flight-path angles for atmospheric capture. Too steep an angle leads to excessive heating and g-loads; too shallow an angle results in skip-out.

```python
# Entry corridor analysis for various vehicles
entry_corridors = {
    "capsule_steep_limit_deg": -7.5,   # Maximum steep entry angle
    "capsule_shallow_limit_deg": -1.5,  # Minimum shallow angle
    "capsule_nominal_deg": -5.5,        # Nominal entry angle
    "shuttle_steep_limit_deg": -6.0,
    "shuttle_shallow_limit_deg": -1.0,
    "shuttle_nominal_deg": -4.0,
}
```

### Propellant Properties Reference

| Property | LOX | LH2 | RP-1 | CH4 | N2H4 | MMH |
|----------|-----|-----|------|-----|------|-----|
| Density (kg/m3) | 1,141 | 70.8 | 810 | 422 | 1,008 | 875 |
| Boiling Point (K) | 90 | 20 | 373 | 112 | 387 | 360 |
| Freeze Point (K) | 54 | 14 | 216 | 91 | 275 | 220 |

### Structural Load Factors Summary

```python
# Typical structural load factors by flight phase
load_factors = {
    "max_q_phase": {
        "axial_load_factor_g": 2.5,
        "lateral_load_factor_g": 1.5,
        "bending_moment_kNm": 5000,
    },
    "stage_separation": {
        "axial_load_factor_g": 1.2,
        "lateral_load_factor_g": 0.8,
    },
    "reentry": {
        "axial_load_factor_g": 4.0,
        "lateral_load_factor_g": 0.5,
        "peak_heating_rate_w_cm2": 200,
    },
}
```
