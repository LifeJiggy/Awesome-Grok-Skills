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

## Advanced Configuration

### Solar Resource Configuration

```yaml
solar_resource:
  data_source: "nsrdb"
  api_key: "${NSRDB_API_KEY}"
  dataset: "psm3"
  year: 2023
  timezone: "UTC"
  attributes:
    - "ghi"
    - "dni"
    - "dhi"
    - "solar_zenith"
    - "solar_azimuth"
```

### Wind Resource Configuration

```yaml
wind_resource:
  data_source: "global_wind_atlas"
  resolution: "1km"
  heights: [50, 80, 100, 150, 200]
  weibull_fitting: true
  wind_shear_model: "log_power_law"
  air_density_correction: true
```

### Battery Storage Configuration

```yaml
battery:
  technology: "li_ion_nmc"
  degradation_model: "calendar_cycling"
  temperature_dependence: true
  round_trip_efficiency: 0.92
  calendar_life_years: 15
  cycle_life_depth:
    - depth: 0.8
      cycles: 5000
    - depth: 0.5
      cycles: 10000
    - depth: 0.3
      cycles: 15000
```

### Microgrid Configuration

```yaml
microgrid:
  components:
    - type: "solar_pv"
      capacity_kw: 800
      cost_per_kw: 1200
    - type: "battery"
      capacity_kwh: 1000
      power_kw: 500
    - type: "diesel_generator"
      capacity_kw: 500
      fuel_cost_per_liter: 1.2
  optimization:
    objective: "minimize_cost"
    constraint: "reliability_99.9"
    time_step_minutes: 15
```

## Architecture Patterns

### Renewable Energy System Architecture

```
Resource Assessment:
├── Solar Resource
│   ├── GHI, DNI, DHI measurements
│   ├── TMY (Typical Meteorological Year)
│   ├── Satellite-derived estimates
│   └── Ground station validation
├── Wind Resource
│   ├── Wind speed profiles
│   ├── Weibull distribution
│   ├── Turbulence intensity
│   └── Wind direction distribution
├── Hydro Resource
│   ├── Flow duration curves
│   ├── Head measurements
│   └── Seasonal patterns
└── Geothermal Resource
    ├── Temperature profiles
    └── Flow rates

System Design:
├── Sizing
│   ├── Load analysis
│   ├── Resource matching
│   ├── Technology selection
│   └── Component sizing
├── Layout
│   ├── Panel/turbine spacing
│   ├── Wake effects (wind)
│   ├── Shading analysis
│   └── Access roads
├── Electrical
│   ├── Inverter sizing
│   ├── Cable sizing
│   ├── Transformer selection
│   └── Grid connection
└── Structural
    ├── Foundation design
    ├── Mounting systems
    └── Wind/snow loading

Performance Modeling:
├── Energy Production
│   ├── Hourly simulation
│   ├── Loss factors
│   ├── Degradation
│   └── Availability
├── Financial Analysis
│   ├── LCOE calculation
│   ├── Cash flow analysis
│   ├── Sensitivity analysis
│   └── Risk assessment
└── Grid Integration
    ├── Curtailment analysis
    ├── Ramp rate limiting
    ├── Frequency response
    └── Voltage regulation
```

### Energy Storage Architecture

```
Battery System:
├── Cell Level
│   ├── Chemistry (NMC, LFP, NCA)
│   ├── Capacity (Ah)
│   ├── Voltage (V)
│   └── Cycle life
├── Module Level
│   ├── Series/parallel config
│   ├── BMS (Battery Management System)
│   ├── Thermal management
│   └── Safety systems
├── System Level
│   ├── Power conversion (PCS)
│   ├── Control system
│   ├── Grid interface
│   └── Monitoring
└── Application
    ├── Energy arbitrage
    ├── Frequency regulation
    ├── Peak shaving
    ├── Renewable firming
    └── Backup power
```

## Integration Guide

### NSRDB Solar Data API

```python
from renewable_energy import NSRDBClient

nsrdb = NSRDBClient(
    api_key="${NSRDB_API_KEY}",
    dataset="psm3",
)

# Get solar resource data
data = nsrdb.get_solar_resource(
    lat=35.0,
    lon=-118.0,
    year=2023,
    attributes=["ghi", "dni", "dhi"],
)
print(f"Annual GHI: {data.annual_ghi:.1f} kWh/m2")
print(f"Peak sun hours: {data.peak_sun_hours:.1f}")
```

### Global Wind Atlas API

```python
from renewable_energy import WindAtlasClient

gwa = WindAtlasClient()

# Get wind resource data
wind_data = gwa.get_wind_resource(
    lat=55.0,
    lon=-3.0,
    heights=[80, 100, 150],
)
print(f"Wind speed at 100m: {wind_data.wind_speed_100m:.1f} m/s")
print(f"Weibull A: {wind_data.weibull_a:.2f}")
print(f"Weibull k: {wind_data.weibull_k:.2f}")
```

### SAM Integration

```python
from renewable_energy import SAMIntegration

sam = SAMIntegration()

# Solar PV simulation
solar_result = sam.simulate_solar(
    location={"lat": 35.0, "lon": -118.0},
    system_capacity_kw=100,
    tilt=30,
    azimuth=180,
    array_type="fixed",
)
print(f"Annual generation: {solar_result.annual_kwh:,.0f} kWh")
print(f"Capacity factor: {solar_result.capacity_factor:.1%}")

# Wind simulation
wind_result = sam.simulate_wind(
    wind_resource=wind_data,
    turbine_model="NREL_5MW",
    hub_height=80,
    rotor_diameter=126,
)
print(f"Annual generation: {wind_result.annual_mwh:,.0f} MWh")
print(f"Capacity factor: {wind_result.capacity_factor:.1%}")
```

## Performance Optimization

### Simulation Speed

| Technique | Description | Impact |
|-----------|-------------|--------|
| Parallel simulation | Multi-year parallel runs | Nx speedup |
| Caching | Reuse resource data | 2-5x for iterations |
| Surrogate models | ML approximation | 100-1000x faster |
| Reduced order | Simplified physics | 10-50x faster |
| GPU acceleration | CUDA-enabled models | 10-50x for ML |

### Optimization Speed

```python
from renewable_energy import OptimizationOptimizer

optimizer = OptimizationOptimizer()
result = optimizer.optimize(
    components=["solar", "wind", "storage"],
    load_profile=load_data,
    techniques=[
        "parallel_evaluation",
        "warm_start",
        "surrogate_assisted",
    ],
)
print(f"Original time: {result.original_hours:.1f}h")
print(f"Optimized time: {result.optimized_hours:.1f}h")
```

### Data Processing Speed

```python
from renewable_energy import DataProcessor

processor = DataProcessor()
processed = processor.process(
    data_sources=["solar", "wind", "load"],
    resolution="15min",
    techniques=[
        "chunking",
        "parallel_io",
        "compression",
    ],
)
print(f"Processing time: {processed.time_seconds:.1f}s")
```

## Security Considerations

### System Security

| Control | Description | Implementation |
|---------|-------------|----------------|
| Access Control | Restrict system access | Role-based access |
| SCADA Security | Protect control systems | Network segmentation |
| Data Integrity | Ensure data accuracy | Validation checks |
| Physical Security | Protect equipment | Fencing, cameras |
| Cyber Security | Protect digital systems | Firewalls, monitoring |

### Grid Connection Security

```
Grid Interconnection:
├── Anti-islanding protection
├── Voltage/frequency protection
├── Communication security
├── Access control
└── Monitoring and logging
```

### Data Security

```
Sensitive Data:
├── Resource data (proprietary)
├── Financial data (project economics)
├── Grid data (system information)
├── Customer data (load profiles)
└── Operational data (performance)
```

## Troubleshooting Guide

### Common Modeling Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Data Gaps | Missing resource data | Use satellite data, interpolation |
| Wake Effects | Lower than expected output | Apply wake model correction |
| Shading Loss | Reduced morning/evening output | Analyze shading patterns |
| Inverter Clipping | Flat-topped generation curve | Upsize inverter |
| Temperature Derating | Summer output reduction | Apply temperature coefficients |

### Resource Data Issues

```
Issue: GHI data seems low
1. Check data source and year
2. Verify coordinates
3. Compare with nearby stations
4. Check for sensor issues
5. Use satellite-derived data

Issue: Wind data doesn't match expected
1. Check measurement height
2. Verify terrain effects
3. Compare with nearby masts
4. Check for obstacles
5. Use mesoscale model data
```

### Simulation Debugging

```python
from renewable_energy import SimulationDebugger

debugger = SimulationDebugger()
diagnostics = debugger.diagnose(
    simulation_type="solar_pv",
    results=solar_result,
    check_inputs=True,
    check_losses=True,
    check_weather=True,
)
for issue in diagnostics.issues:
    print(f"[{issue.severity}] {issue.message}")
    print(f"  Fix: {issue.suggestion}")
```

## API Reference

### SolarPlanner

```python
class SolarPlanner:
    def __init__(
        location: dict,
        system_capacity_kw: float,
    ): ...
    
    def assess_resource(self) -> SolarResource:
        """Assess solar resource at location."""
    
    def estimate_performance(
        tilt: float = None,
        azimuth: float = 180,
        losses: dict = None,
    ) -> SolarPerformance:
        """Estimate system performance."""

class SolarResource:
    ghi_kwh_m2: float
    dni_kwh_m2: float
    dhi_kwh_m2: float
    peak_sun_hours: float
    clearness_index: float
    temperature_avg: float
```

### WindPlanner

```python
class WindPlanner:
    def __init__(
        hub_height_m: float,
        turbine_rating_kw: float,
    ): ...
    
    def assess_resource(
        wind_speed_ms: float,
        weibull_k: float = 2.0,
    ) -> WindResource:
        """Assess wind resource."""
    
    def estimate_generation(
        capacity_factor: float,
    ) -> WindGeneration:
        """Estimate annual generation."""

class WindResource:
    power_density_w_m2: float
    capacity_factor: float
    turbulence_intensity: float
    wind_shear_exponent: float
```

### StorageOptimizer

```python
class StorageOptimizer:
    def __init__(
        technology: str,
        capacity_kwh: float,
        power_kw: float,
    ): ...
    
    def simulate_cycle(
        charge_rate: float,
        discharge_rate: float,
        depth_of_discharge: float,
    ) -> CycleResult:
        """Simulate battery cycle."""
    
    def calculate_economics(
        electricity_price: float,
        demand_charge: float,
    ) -> StorageEconomics:
        """Calculate storage economics."""

class CycleResult:
    efficiency: float
    cycle_life: int
    energy_throughput: float
    degradation_per_cycle: float
```

## Data Models

### SolarResource

```
SolarResource:
  latitude: float
  longitude: float
  elevation_m: float
  ghi_kwh_m2: float
  dni_kwh_m2: float
  dhi_kwh_m2: float
  peak_sun_hours: float
  clearness_index: float
  temperature_avg: float
  monthly_ghi: list[float]
```

### WindResource

```
WindResource:
  latitude: float
  longitude: float
  elevation_m: float
  wind_speed_ms: float
  wind_direction_deg: float
  turbulence_intensity: float
  weibull_a: float
  weibull_k: float
  power_density_w_m2: float
  monthly_wind_speed: list[float]
```

### EnergySystemDesign

```
EnergySystemDesign:
  components: list[SystemComponent]
  annual_generation_kwh: float
  annual_load_kwh: float
  renewable_fraction: float
  annual_cost: float
  lcoe: float
  payback_years: float
```

## Deployment Guide

### Renewable Energy Project Setup

```
1. Feasibility Study
   ├── Resource assessment
   ├── Site evaluation
   ├── Technology selection
   ├── Preliminary design
   └── Economic analysis

2. Detailed Design
   ├── Engineering design
   ├── Equipment specification
   ├── Grid connection study
   ├── Environmental assessment
   └── Permitting

3. Construction
   ├── Procurement
   ├── Civil works
   ├── Electrical installation
   ├── Commissioning
   └── Grid connection

4. Operations
   ├── Performance monitoring
   ├── Maintenance scheduling
   ├── Grid compliance
   ├── Financial reporting
   └── Asset management
```

### Software Environment

```bash
# Install renewable energy tools
conda install -c conda-forge pvlib windpowerlib
pip install nrel-pySAM

# Configure API keys
export NSRDB_API_KEY="your_key"
export WIND_ATLAS_API_KEY="your_key"
```

## Monitoring & Observability

### Performance Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Performance Ratio | >80% | Actual vs expected output |
| Availability | >98% | System uptime |
| Capacity Factor | Varies | Actual vs rated capacity |
| Degradation | <0.5%/yr | Annual output decline |
| LCOE | <$50/MWh | Levelized cost |

### Monitoring Dashboard

```
Renewable Energy Dashboard:
├── Real-time generation
├── Performance ratio trend
├── Capacity factor by month
├── Availability statistics
├── Revenue and savings
├── Environmental benefits
└── Maintenance alerts
```

## Testing Strategy

### Model Validation

```
1. Unit Tests
   ├── Resource calculations
   ├── Performance modeling
   ├── Financial calculations
   └── Grid integration

2. Integration Tests
   ├── End-to-end simulation
   ├── Multi-technology systems
   ├── Storage optimization
   └── Microgrid operation

3. Validation Tests
    actual project data
   ├── Industry benchmarks
   ├── Sensitivity analysis
   └── Uncertainty quantification
```

## Versioning & Migration

### Model Versioning

```
v3.0: Major updates
├── New technology models
├── Updated cost data
├── New optimization methods
└── Grid compliance updates

v2.x: Feature additions
├── New resource data sources
├── Storage optimization
├── Microgrid support
└── Financial analysis

v2.0.x: Bug fixes
├── Calculation corrections
├── Data format fixes
└── Documentation updates
```

## Glossary

| Term | Definition |
|------|-----------|
| Capacity Factor | Actual output / (rated capacity x hours) |
| GHI | Global Horizontal Irradiance |
| LCOE | Levelized Cost of Energy |
| Performance Ratio | Actual output / expected output |
| TMY | Typical Meteorological Year |
| Weibull | Statistical distribution for wind speed |
| DNI | Direct Normal Irradiance |
| Curtailment | Reducing output below available capacity |
| Round-trip Efficiency | Energy out / Energy in for storage |
| Wake Effect | Wind speed reduction behind turbine |

## Changelog

### 2.0.0 (2024-12-01)
- Added microgrid design optimization
- Added energy storage economics
- Improved solar resource assessment
- Added wind wake modeling

### 1.2.0 (2024-08-15)
- Added LCOE calculation
- Added wind resource assessment
- Improved performance modeling

### 1.1.0 (2024-05-20)
- Added solar PV system sizing
- Added energy storage sizing
- Improved financial analysis

### 1.0.0 (2024-02-01)
- Initial release with basic solar sizing
- Simple resource assessment
- Basic economic analysis

## Contributing Guidelines

### Adding New Technologies

1. Define technology specification
2. Implement simulation model
3. Add validation cases
4. Document parameters and outputs
5. Submit PR with validation results

### Code Quality

- Type hints on all functions
- Unit tests for calculations
- Integration tests with real data
- Documentation for new technologies

## License

MIT License

Copyright (c) 2024 Renewable Energy Contributors

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
