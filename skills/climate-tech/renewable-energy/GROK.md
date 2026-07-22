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
- Use real load profiles (15-min intervals) for storage optimization â€” averages mislead
- Apply appropriate discount rates (6-10%) for project economics
- Include all balance-of-system costs in LCOE: inverters, wiring, permits, interconnection
- Monitor actual vs predicted performance â€” underperformance indicates maintenance needs
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
â”œâ”€â”€ Solar Resource
â”‚   â”œâ”€â”€ GHI, DNI, DHI measurements
â”‚   â”œâ”€â”€ TMY (Typical Meteorological Year)
â”‚   â”œâ”€â”€ Satellite-derived estimates
â”‚   â””â”€â”€ Ground station validation
â”œâ”€â”€ Wind Resource
â”‚   â”œâ”€â”€ Wind speed profiles
â”‚   â”œâ”€â”€ Weibull distribution
â”‚   â”œâ”€â”€ Turbulence intensity
â”‚   â””â”€â”€ Wind direction distribution
â”œâ”€â”€ Hydro Resource
â”‚   â”œâ”€â”€ Flow duration curves
â”‚   â”œâ”€â”€ Head measurements
â”‚   â””â”€â”€ Seasonal patterns
â””â”€â”€ Geothermal Resource
    â”œâ”€â”€ Temperature profiles
    â””â”€â”€ Flow rates

System Design:
â”œâ”€â”€ Sizing
â”‚   â”œâ”€â”€ Load analysis
â”‚   â”œâ”€â”€ Resource matching
â”‚   â”œâ”€â”€ Technology selection
â”‚   â””â”€â”€ Component sizing
â”œâ”€â”€ Layout
â”‚   â”œâ”€â”€ Panel/turbine spacing
â”‚   â”œâ”€â”€ Wake effects (wind)
â”‚   â”œâ”€â”€ Shading analysis
â”‚   â””â”€â”€ Access roads
â”œâ”€â”€ Electrical
â”‚   â”œâ”€â”€ Inverter sizing
â”‚   â”œâ”€â”€ Cable sizing
â”‚   â”œâ”€â”€ Transformer selection
â”‚   â””â”€â”€ Grid connection
â””â”€â”€ Structural
    â”œâ”€â”€ Foundation design
    â”œâ”€â”€ Mounting systems
    â””â”€â”€ Wind/snow loading

Performance Modeling:
â”œâ”€â”€ Energy Production
â”‚   â”œâ”€â”€ Hourly simulation
â”‚   â”œâ”€â”€ Loss factors
â”‚   â”œâ”€â”€ Degradation
â”‚   â””â”€â”€ Availability
â”œâ”€â”€ Financial Analysis
â”‚   â”œâ”€â”€ LCOE calculation
â”‚   â”œâ”€â”€ Cash flow analysis
â”‚   â”œâ”€â”€ Sensitivity analysis
â”‚   â””â”€â”€ Risk assessment
â””â”€â”€ Grid Integration
    â”œâ”€â”€ Curtailment analysis
    â”œâ”€â”€ Ramp rate limiting
    â”œâ”€â”€ Frequency response
    â””â”€â”€ Voltage regulation
```

### Energy Storage Architecture

```
Battery System:
â”œâ”€â”€ Cell Level
â”‚   â”œâ”€â”€ Chemistry (NMC, LFP, NCA)
â”‚   â”œâ”€â”€ Capacity (Ah)
â”‚   â”œâ”€â”€ Voltage (V)
â”‚   â””â”€â”€ Cycle life
â”œâ”€â”€ Module Level
â”‚   â”œâ”€â”€ Series/parallel config
â”‚   â”œâ”€â”€ BMS (Battery Management System)
â”‚   â”œâ”€â”€ Thermal management
â”‚   â””â”€â”€ Safety systems
â”œâ”€â”€ System Level
â”‚   â”œâ”€â”€ Power conversion (PCS)
â”‚   â”œâ”€â”€ Control system
â”‚   â”œâ”€â”€ Grid interface
â”‚   â””â”€â”€ Monitoring
â””â”€â”€ Application
    â”œâ”€â”€ Energy arbitrage
    â”œâ”€â”€ Frequency regulation
    â”œâ”€â”€ Peak shaving
    â”œâ”€â”€ Renewable firming
    â””â”€â”€ Backup power
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
â”œâ”€â”€ Anti-islanding protection
â”œâ”€â”€ Voltage/frequency protection
â”œâ”€â”€ Communication security
â”œâ”€â”€ Access control
â””â”€â”€ Monitoring and logging
```

### Data Security

```
Sensitive Data:
â”œâ”€â”€ Resource data (proprietary)
â”œâ”€â”€ Financial data (project economics)
â”œâ”€â”€ Grid data (system information)
â”œâ”€â”€ Customer data (load profiles)
â””â”€â”€ Operational data (performance)
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
   â”œâ”€â”€ Resource assessment
   â”œâ”€â”€ Site evaluation
   â”œâ”€â”€ Technology selection
   â”œâ”€â”€ Preliminary design
   â””â”€â”€ Economic analysis

2. Detailed Design
   â”œâ”€â”€ Engineering design
   â”œâ”€â”€ Equipment specification
   â”œâ”€â”€ Grid connection study
   â”œâ”€â”€ Environmental assessment
   â””â”€â”€ Permitting

3. Construction
   â”œâ”€â”€ Procurement
   â”œâ”€â”€ Civil works
   â”œâ”€â”€ Electrical installation
   â”œâ”€â”€ Commissioning
   â””â”€â”€ Grid connection

4. Operations
   â”œâ”€â”€ Performance monitoring
   â”œâ”€â”€ Maintenance scheduling
   â”œâ”€â”€ Grid compliance
   â”œâ”€â”€ Financial reporting
   â””â”€â”€ Asset management
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
â”œâ”€â”€ Real-time generation
â”œâ”€â”€ Performance ratio trend
â”œâ”€â”€ Capacity factor by month
â”œâ”€â”€ Availability statistics
â”œâ”€â”€ Revenue and savings
â”œâ”€â”€ Environmental benefits
â””â”€â”€ Maintenance alerts
```

## Testing Strategy

### Model Validation

```
1. Unit Tests
   â”œâ”€â”€ Resource calculations
   â”œâ”€â”€ Performance modeling
   â”œâ”€â”€ Financial calculations
   â””â”€â”€ Grid integration

2. Integration Tests
   â”œâ”€â”€ End-to-end simulation
   â”œâ”€â”€ Multi-technology systems
   â”œâ”€â”€ Storage optimization
   â””â”€â”€ Microgrid operation

3. Validation Tests
    actual project data
   â”œâ”€â”€ Industry benchmarks
   â”œâ”€â”€ Sensitivity analysis
   â””â”€â”€ Uncertainty quantification
```

## Versioning & Migration

### Model Versioning

```
v3.0: Major updates
â”œâ”€â”€ New technology models
â”œâ”€â”€ Updated cost data
â”œâ”€â”€ New optimization methods
â””â”€â”€ Grid compliance updates

v2.x: Feature additions
â”œâ”€â”€ New resource data sources
â”œâ”€â”€ Storage optimization
â”œâ”€â”€ Microgrid support
â””â”€â”€ Financial analysis

v2.0.x: Bug fixes
â”œâ”€â”€ Calculation corrections
â”œâ”€â”€ Data format fixes
â””â”€â”€ Documentation updates
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


## Additional Resources

### Related Technologies

This module integrates with industry-standard tools and frameworks. Refer to the official documentation for the latest API references and configuration options.

### Community and Support

- Open source contributions welcome
- Issue tracking via GitHub Issues
- Documentation updated with each release
- Community forums for discussion and support

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-01 | Initial release |
| 1.1.0 | 2026-03-15 | Enhanced configuration options |
| 1.2.0 | 2026-06-01 | Performance improvements |
| 2.0.0 | 2026-07-01 | Major architecture update |

### License

MIT License - Copyright (c) 2026 Awesome Grok Skills
