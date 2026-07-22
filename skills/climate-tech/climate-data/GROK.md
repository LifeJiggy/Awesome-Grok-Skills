---
name: "climate-data"
category: "climate-tech"
version: "2.0.0"
tags: ["climate-tech", "climate-data", "CMIP6", "temperature", "precipitation"]
---

# Climate Data

## Overview

The Climate Data module provides tools for processing, analyzing, and visualizing climate datasets including CMIP6 projections, ERA5 reanalysis, and satellite observations. It covers temperature anomaly analysis, precipitation pattern detection, extreme weather event identification, climate model intercomparison, and downscaling methodologies.

This skill is essential for climate scientists, meteorologists, environmental consultants, and researchers working with climate projections and observational data.

## Core Capabilities

- **Temperature Analysis**: Anomaly calculation, trend detection, heat index computation, growing degree days
- **Precipitation Analysis**: Rainfall intensity classification, drought indices (SPI, PDSI), flood risk assessment
- **Extreme Events**: Heat wave detection, cold spells, extreme precipitation, tropical cyclone tracking
- **Climate Projections**: CMIP6 scenario analysis, model ensemble statistics, uncertainty quantification
- **Downscaling**: Statistical downscaling, bias correction, delta method, quantile mapping
- **Sea Level**: Coastal flood risk, tidal analysis, storm surge estimation
- **Cryosphere**: Snow cover analysis, glacier mass balance, permafrost monitoring
- **Climate Indices**: ENSO, NAO, PDO, AMO teleconnection analysis

## Usage Examples

```python
from climate_data import (
    TemperatureAnalyzer,
    PrecipitationAnalyzer,
    ExtremeEventDetector,
    CMIP6Processor,
    Downscaler,
)

# --- Temperature Analysis ---
temp = TemperatureAnalyzer()
anomaly = temp.calculate_anomaly(
    observed=[14.5, 14.7, 14.8, 15.0, 15.1],
    baseline=[14.0, 14.0, 14.0, 14.0, 14.0],
)
print(f"Temperature anomaly: {anomaly.mean_anomaly:.2f} deg C")
print(f"Trend: {anomaly.trend_per_decade:.2f} deg C/decade")

# --- Precipitation ---
precip = PrecipitationAnalyzer()
spi = precip.calculate_spi(
    precipitation=[50, 45, 30, 20, 15, 10, 8, 5],
    scale_months=3,
)
print(f"SPI: {spi:.2f}")

# --- Extreme Events ---
detector = ExtremeEventDetector()
heatwaves = detector.detect_heatwaves(
    temperatures=[32, 33, 35, 36, 34, 33, 31],
    threshold=32,
    min_duration=3,
)
print(f"Heat waves: {len(heatwaves)}")
for hw in heatwaves:
    print(f"  {hw.start_date} to {hw.end_date}: max {hw.max_temp:.1f} deg C")

# --- CMIP6 Projections ---
cmip = CMIP6Processor()
projection = cmip.analyze_scenario(
    model="EC-Earth3",
    scenario="ssp245",
    variable="tas",
    region={"lat_min": 30, "lat_max": 45, "lon_min": -10, "lon_max": 10},
)
print(f"Mean warming: {projection.mean_anomaly:.2f} deg C")
print(f"Uncertainty range: {projection.ci_lower:.2f} to {projection.ci_upper:.2f}")

# --- Downscaling ---
downscaler = Downscaler(method="quantile_mapping")
local = downscaler.downscale(
    coarse_data=[14.5, 14.7, 15.0],
    reference_data=[14.2, 14.4, 14.8],
    target_resolution_km=1,
)
print(f"Downscaled values: {local}")
```

## Best Practices

- Use bias-corrected CMIP6 data for impact assessments — raw model output has systematic biases
- Apply appropriate statistical tests for trend detection (Mann-Kendall, linear regression)
- Account for autocorrelation in climate time series when calculating significance
- Use ensemble medians for projections; report inter-model spread as uncertainty
- Apply delta method downscaling for local-scale impact studies
- Use SPI for drought monitoring — it's standardized and comparable across regions
- Consider non-stationarity in extreme event analysis under climate change
- Validate downscaling methods against historical observations before applying to projections
- Report both mean and extreme changes — means can mask amplified extremes
- Use appropriate baselines (1991-2020 or 1981-2010) for anomaly calculations

## Related Modules

- **environmental-modeling**: Climate-driven ecosystem modeling
- **carbon-tracking**: Emissions data for climate projections
- **renewable-energy**: Climate data for energy system planning
- **emission-reduction**: Climate scenarios for mitigation pathways

## Advanced Configuration

### CMIP6 Data Access Configuration

```yaml
cmip6:
  catalog:
    source: "esgf-node.llnl.gov"
    mirror: "esgf-data.llnl.gov"
    protocol: "https"
  variables:
    - name: "tas"
      long_name: "Near-Surface Air Temperature"
      unit: "K"
    - name: "pr"
      long_name: "Precipitation"
      unit: "kg m-2 s-1"
    - name: "rsds"
      long_name: "Surface Downwelling Shortwave Radiation"
      unit: "W m-2"
  scenarios:
    - "ssp126"
    - "ssp245"
    - "ssp370"
    - "ssp585"
  models:
    - "EC-Earth3"
    - "MPI-ESM1-2-HR"
    - "UKESM1-0-LL"
```

### ERA5 Reanalysis Configuration

```yaml
era5:
  dataset: "era5_land"
  variables:
    - "2m_temperature"
    - "total_precipitation"
    - "10m_u_component_of_wind"
    - "10m_v_component_of_wind"
    - "surface_solar_radiation_downwards"
  temporal_resolution: "hourly"
  spatial_resolution: "0.1degree"
```

### Downscaling Configuration

```yaml
downscaling:
  methods:
    - name: "quantile_mapping"
      bias_correction: true
      distribution: "gamma"
    - name: "delta_method"
      reference_period: "1995-2014"
    - name: "statistical_downscaling"
      predictor_fields: ["slp", "z500", "u700"]
  output_resolution_km: 1
```

## Architecture Patterns

### Climate Data Processing Pipeline

```
Data Acquisition:
├── CMIP6 (projections)
├── ERA5 (reanalysis)
├── Observations (stations, satellites)
├── Reanalysis (MERRA-2, JRA-55)
└── Remote sensing (MODIS, Landsat)

Preprocessing:
├── Format conversion (GRIB → NetCDF)
├── Variable selection
├── Spatial subsetting
├── Temporal subsetting
├── Coordinate regridding
└── Unit conversion

Quality Control:
├── Range checks
├── Gap detection
├── Outlier identification
├── Cross-validation
├── Metadata verification
└── Consistency checks

Bias Correction:
├── Delta method
├── Quantile mapping
├── Linear scaling
├── Power transformation
└── Variogram mapping

Analysis:
├── Trend detection
├── Anomaly calculation
├── Extreme event analysis
├── Variability assessment
├── Teleconnection analysis
└── Climate indices

Output:
├── Derived variables
├── Maps and visualizations
├── Time series
├── Statistics
├── Uncertainty estimates
└── Export formats
```

### Extreme Event Detection Architecture

```
Detection Methods:
├── Threshold-based
│   ├── Fixed threshold (absolute)
│   ├── Percentile threshold (relative)
│   └── Station-specific threshold
├── Duration-based
│   ├── Minimum consecutive days
│   ├── Maximum consecutive days
│   └── Spell length analysis
├── Composite indices
│   ├── Heat wave duration index
│   ├── Consecutive dry days
│   └── Standardized precipitation index
└── Statistical
    ├── Peaks over threshold (POT)
    ├── Block maxima (GEV)
    └── Return period estimation
```

## Integration Guide

### xarray + Dask Integration

```python
import xarray as xr
import dask.distributed

# Start Dask cluster
client = dask.distributed.Client(n_workers=4, memory_limit="16GB")

# Load CMIP6 data
ds = xr.open_mfdataset(
    "/data/cmip6/tas/*.nc",
    parallel=True,
    chunks={"time": 365, "lat": 100, "lon": 100},
)

# Calculate anomaly
climatology = ds.tas.sel(time=slice("1991", "2020")).mean(dim="time")
anomaly = ds.tas - climatology

# Compute with Dask
result = anomaly.mean(dim=["lat", "lon"]).compute()
print(f"Global mean anomaly: {result.values}")
```

### CMIP6 ESGF Access

```python
from climate_data import ESGFClient

esgf = ESGFClient(
    node="esgf-node.llnl.gov",
    project="CMIP6",
)

# Search for data
results = esgf.search(
    experiment_id="ssp245",
    variable="tas",
    source_id="EC-Earth3",
    member_id="r1i1p1f1",
)
print(f"Files found: {len(results)}")

# Download
esgf.download(results, output_dir="/data/cmip6/")
```

### ERA5 CDS API

```python
from climate_data import CDSClient

cds = CDSClient(
    key="${CDS_API_KEY}",
    url="https://cds.climate.copernicus.eu/api/v2",
)

# Download ERA5 data
cds.retrieve(
    dataset="reanalysis-era5-land",
    variables=["2m_temperature"],
    area=[90, -180, -90, 180],
    dates=("2024-01-01", "2024-12-31"),
    output="/data/era5/temperature_2024.nc",
)
```

## Performance Optimization

### Data Processing Speed

| Technique | Description | Impact |
|-----------|-------------|--------|
| Chunking | Process in spatial tiles | Memory efficient |
| Parallel I/O | Multi-file reading | 2-4x faster |
| Dask parallelism | Distributed computing | Nx workers |
| Compression | NetCDF4/HDF5 compression | 2-5x smaller |
| Caching | Reuse computed results | 10x for iterations |

### Memory Optimization

```python
from climate_data import MemoryOptimizer

optimizer = MemoryOptimizer()
ds_optimized = optimizer.optimize(
    dataset=large_ds,
    techniques=[
        "chunking",
        "dtype_reduction",  # float64 → float32
        "compression",
        "memory_mapping",
    ],
)
print(f"Original size: {optimizer.original_gb:.1f} GB")
print(f"Optimized size: {optimizer.optimized_gb:.1f} GB")
```

### Parallel Processing

```python
from climate_data import ParallelProcessor

processor = ParallelProcessor(
    n_workers=8,
    memory_per_worker="4GB",
)

# Process multiple models in parallel
results = processor.process_models(
    models=["EC-Earth3", "MPI-ESM1-2-HR", "UKESM1-0-LL"],
    variable="tas",
    scenario="ssp245",
    function="calculate_anomaly",
)
print(f"Processed {len(results)} models")
```

## Security Considerations

### Data Security

| Control | Description | Implementation |
|---------|-------------|----------------|
| Access Control | Restrict data access | API keys, OAuth |
| Data Encryption | Protect data at rest | AES-256 |
| Audit Logging | Track data access | Logging infrastructure |
| Data Provenance | Track data lineage | Metadata catalogs |
| Backup | Regular backups | 3-2-1 rule |

### Data Integrity

```
Integrity Controls:
├── Checksum verification
├── Version control for code
├── Reproducible workflows
├── Peer review of methods
├── Documentation of assumptions
└── Data quality flags
```

### Sensitive Data

```
Climate Data Sensitivity:
├── Location of weather stations
├── Infrastructure vulnerability data
├── Agricultural production data
├── Water resource availability
└── Military installation locations
```

## Troubleshooting Guide

### Common Data Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Missing Files | Gaps in time series | Use alternate node, check access |
| Format Issues | Cannot read GRIB/NetCDF | Update libraries, check version |
| Coordinate Mismatch | Spatial misalignment | Regrid to common grid |
| Unit Errors | Incorrect values | Check unit conversion |
| Memory Overflow | Out of memory error | Chunk data, reduce resolution |

### Data Access Issues

```
Issue: ESGF connection fails
1. Check node availability
2. Verify credentials
3. Try alternate mirror
4. Check firewall settings
5. Use bulk download

Issue: ERA5 download slow
1. Use CDS API instead of web
2. Download in smaller chunks
3. Use parallel downloads
4. Check network bandwidth
```

### Processing Errors

```python
from climate_data import DataDebugger

debugger = DataDebugger()
diagnostics = debugger.diagnose(
    dataset_path="/data/cmip6/tas/*.nc",
    check_coordinates=True,
    check_units=True,
    check_completeness=True,
    check_consistency=True,
)
for issue in diagnostics.issues:
    print(f"[{issue.severity}] {issue.message}")
```

## API Reference

### TemperatureAnalyzer

```python
class TemperatureAnalyzer:
    def calculate_anomaly(
        observed: list[float],
        baseline: list[float],
    ) -> TemperatureAnomaly:
        """Calculate temperature anomaly."""
    
    def detect_trend(
        time_series: list[float],
        method: str = "mann_kendall",
    ) -> TrendResult:
        """Detect temperature trend."""
    
    def calculate_heat_index(
        temperature: float,
        humidity: float,
    ) -> float:
        """Calculate heat index."""
```

### PrecipitationAnalyzer

```python
class PrecipitationAnalyzer:
    def calculate_spi(
        precipitation: list[float],
        scale_months: int = 3,
    ) -> float:
        """Calculate Standardized Precipitation Index."""
    
    def classify_drought(
        spi_values: list[float],
    ) -> DroughtClassification:
        """Classify drought severity from SPI."""
    
    def calculate_extreme_indices(
        precipitation: list[float],
    ) -> ExtremeIndices:
        """Calculate extreme precipitation indices."""
```

### CMIP6Processor

```python
class CMIP6Processor:
    def analyze_scenario(
        model: str,
        scenario: str,
        variable: str,
        region: dict,
    ) -> ScenarioAnalysis:
        """Analyze CMIP6 scenario projection."""
    
    def ensemble_statistics(
        models: list[str],
        scenario: str,
        variable: str,
    ) -> EnsembleStats:
        """Calculate ensemble statistics."""
```

## Data Models

### ClimateProjection

```
ClimateProjection:
  model: str
  scenario: str
  variable: str
  region: dict
  time_range: tuple
  mean_anomaly: float
  trend_per_decade: float
  uncertainty_range: tuple
  data_file: str
```

### ExtremeEvent

```
ExtremeEvent:
  event_type: str          # heatwave, coldspell, flood, drought
  start_date: datetime
  end_date: datetime
  duration_days: int
  severity: str            # moderate, extreme, exceptional
  magnitude: float
  affected_area_km2: float
  return_period: float
```

### DownscaledData

```
DownscaledData:
  method: str
  input_resolution_deg: float
  output_resolution_km: float
  bias_correction: str
  validation_metric: float
  output_file: str
```

## Deployment Guide

### Climate Data Environment Setup

```
1. Hardware
   ├── CPU: 8+ cores
   ├── RAM: 32+ GB
   ├── Storage: 2TB+ NVMe
   └── Network: High bandwidth for data download

2. Software
   ├── Python 3.10+
   ├── Conda/Mamba
   ├── xarray, dask, netCDF4
   ├── GDAL/OGR
   └── CDO, NCO (command line)

3. Data
   ├── CMIP6 local mirror
   ├── ERA5 archive
   ├── Station data
   └── Topographic data

4. Configuration
   ├── Data paths
   ├── Dask cluster settings
   ├── Output directories
   └── Logging configuration
```

### Data Pipeline

```bash
# Install climate tools
conda install -c conda-forge xarray dask netCDF4 cdo nco

# Configure data paths
export CMIP6_DATA="/data/cmip6"
export ERA5_DATA="/data/era5"
export OUTPUT_DIR="/output/climate"

# Start Dask cluster
dask scheduler --port 8786 &
dask worker tcp://localhost:8786 --nworkers 4 &
```

## Monitoring & Observability

### Data Quality Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Completeness | >99% | Data availability |
| Accuracy | <0.5C | Temperature error |
| Timeliness | <24h | Data latency |
| Consistency | >95% | Cross-source agreement |
| Coverage | >90% | Spatial coverage |

### Monitoring Dashboard

```
Climate Data Dashboard:
├── Data availability status
├── Processing pipeline status
├── Data quality scores
├── Storage utilization
├── Download progress
├── Error and warning logs
└── Performance metrics
```

## Testing Strategy

### Data Testing

```
1. Unit Tests
   ├── Coordinate handling
   ├── Unit conversion
   ├── Statistical calculations
   └── File I/O operations

2. Integration Tests
   ├── Pipeline end-to-end
   ├── Multi-source processing
   ├── Downscaling validation
   └── Output verification

3. Validation Tests
    against observations
   ├── Cross-model comparison
   ├── Historical reanalysis
   └── Extreme event validation
```

## Versioning & Migration

### Data Versioning

```
v3.0: New data sources
├── CMIP6 update
├── ERA5 extension
├── New observation datasets
└── Updated emission scenarios

v2.x: Processing updates
├── New algorithms
├── Improved bias correction
├── Higher resolution
└── Additional variables

v2.0.x: Bug fixes
├── Calculation corrections
├── Format fixes
└── Documentation updates
```

## Glossary

| Term | Definition |
|------|-----------|
| CMIP6 | Coupled Model Intercomparison Project Phase 6 |
| ERA5 | ECMWF Reanalysis v5 |
| GWP | Global Warming Potential |
| NCEP | National Centers for Environmental Prediction |
| SPI | Standardized Precipitation Index |
| SSP | Shared Socioeconomic Pathway |
| Teleconnection | Large-scale climate pattern linking distant regions |
| TWAP | Time-Weighted Average Price |
| Downscaling | Converting coarse to fine resolution data |
| Bias Correction | Adjusting model output to match observations |

## Changelog

### 2.0.0 (2024-12-01)
- Added CMIP6 full support
- Added ERA5 reanalysis integration
- Added downscaled data support
- Improved extreme event detection

### 1.2.0 (2024-08-15)
- Added climate indices (ENSO, NAO)
- Added bias correction methods
- Improved visualization

### 1.1.0 (2024-05-20)
- Added temperature analysis
- Added precipitation analysis
- Improved trend detection

### 1.0.0 (2024-02-01)
- Initial release with basic data processing
- Simple temperature analysis
- Basic visualization

## Contributing Guidelines

### Adding New Data Sources

1. Document data source access
2. Implement data loader
3. Add quality control checks
4. Include validation against reference
5. Submit PR with documentation

### Code Quality

- Type hints on all functions
- Unit tests for calculations
- Integration tests with real data
- Documentation for new sources

## License

MIT License

Copyright (c) 2024 Climate Data Contributors

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
