---
name: "ocean-data"
category: "ocean-tech"
version: "1.0.0"
tags: ["ocean-tech", "ocean-data"]
---

# Ocean Data

## Overview

Comprehensive ocean-data capabilities within the ocean-tech domain. This module provides tools, frameworks, and best practices for ocean-data operations.

## Core Capabilities

- Configuration and setup
- Data processing and analysis
- Integration with related systems
- Monitoring and observability
- Best practices and patterns

## Usage

```python
from ocean_data import _module

engine = _module.Engine()
engine.configure()
results = engine.run()
print(results)
```

## Best Practices

- Follow security guidelines
- Implement proper error handling
- Use configuration management
- Monitor performance metrics
- Document API interfaces

## Related Modules

- Other modules in ocean-tech domain
- Integration points with external systems

## Advanced Configuration

### Data Format Support

- **NetCDF4/HDF5**: Primary format for gridded ocean data. Supports chunking, compression, and CF-convention metadata.
- **GRIB2**: WMO standard for meteorological/oceanographic data. Used by ECMWF and NOAA models.
- **Zarr**: Cloud-optimized format for large-scale array storage. Ideal for S3/GCS backends.
- **Shapefile/GeoJSON**: Vector format for coastline, bathymetry, and region definitions.

### CF-Convention Compliance

```python
from ocean_data import CFCompliance

compliance = CFCompliance(
    check_coordinates=True,
    check_dimensions=True,
    check_units=True,
    check_standard_names=True,
    check_global_attributes=True
)

report = compliance.validate(dataset)
print(f"Compliance score: {report.score:.2f}")
print(f"Issues: {report.issues}")
```

### Data Discovery Configuration

```yaml
discovery:
  catalogs:
    - name: "NOAA ERDDAP"
      url: "https://coastwatch.pfeg.noaa.gov/erddap"
      type: "erddap"
    - name: "CMEMS"
      url: "https://marine.copernicus.eu"
      type: "cmems"
    - name: " local_archive"
      path: "/data/ocean"
      type: "filesystem"
  search:
    spatial_index: "rtree"
    temporal_index: "btree"
    text_search: "elasticsearch"
```

### Version Control for Data

```python
from ocean_data import DataVersioning

versioning = DataVersioning(
    storage="s3://ocean-data-versioned",
    metadata_store="postgresql://localhost/ocean_meta"
)

# Track data versions
version = versioning.commit(
    dataset="sst_daily",
    file="sst_2024.nc",
    metadata={"source": "satellite", "resolution": "1km"},
    tags=["operational", "daily"]
)
```

## Architecture Patterns

### Data Lake Architecture

```
┌─────────────────────────────────────────┐
│           Application Layer             │
│   (APIs, Notebooks, Visualization)      │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│          Query Layer                     │
│   (Presto, Trino, DuckDB)               │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│          Processing Layer               │
│   (Spark, Dask, Xarray)                 │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│          Storage Layer                  │
│   (S3, GCS, HDFS — Zarr/NetCDF)        │
└─────────────────────────────────────────┘
```

### Data Pipeline Architecture

```
Ingestion → Validation → Processing → Storage → Serving
    │           │            │          │         │
    ▼           ▼            ▼          ▼         ▼
  Format     QC Check    Transform   Partition   API
  Detection  CF Check    Aggregate   Compress    Export
```

### Spatial Data Organization

- **Zonal**: Divided by ocean basins (Atlantic, Pacific, Indian, Southern, Arctic).
- **Gridded**: Regular latitude/longitude grids (0.25°, 0.1°, 0.01°).
- **Profile**: Vertical sections along ship tracks or float trajectories.
- **Time Series**: Fixed locations (moorings, tide gauges).

### Data Quality Framework

```
Level 0 → Level 1 → Level 2 → Level 3 → Level 4
  Raw     Calibrated   QC'd     Gridded   Analyzed
```

## Integration Guide

### ERDDAP Integration

```python
from ocean_data import ERDDAPClient

erddap = ERDDAPClient(
    server_url="https://coastwatch.pfeg.noaa.gov/erddap"
)

# Search datasets
datasets = erddap.search(
    query="sea surface temperature",
    max_results=10
)

# Download data
data = erddap.get_data(
    dataset_id="jplMURSST41",
    variables="analysed_sst",
    constraints={
        "latitude": (30, 40),
        "longitude": (-130, -120),
        "time": ("2024-01-01", "2024-01-31")
    }
)
```

### OPeNDAP Integration

```python
from ocean_data import OPENDAPClient

opendap = OPENDAPClient(
    server_url="https://opendap.example.com"
)

# Lazy loading of large datasets
dataset = opendap.open_dataset("ocean_model_daily.nc")
subset = dataset.subset(
    latitude=slice(30, 40),
    longitude=slice(-130, -120),
    time=slice("2024-01-01", "2024-01-31")
)
```

### GDAL/OGR Integration

```python
from ocean_data import GDALWrapper

gdal = GDALWrapper()

# Read raster data
raster = gdal.read_raster("bathymetry.tif")

# Reproject to common coordinate system
projected = gdal.reproject(
    raster,
    target_crs="EPSG:4326",
    resampling="bilinear"
)

# Export to different format
gdal.export(projected, "bathymetry_reprojected.nc", format="netcdf")
```

## Performance Optimization

### Parallel Processing

```python
from ocean_data import ParallelProcessor

processor = ParallelProcessor(
    workers=8,
    chunk_size="auto",
    memory_limit="4GB"
)

# Process large dataset in parallel
results = processor.map(
    func=compute_derived_variable,
    datasets=dataset_chunks
)
```

### Caching Strategies

- **In-memory**: LRU cache for frequently accessed subsets.
- **Disk cache**: SSD-backed for medium-term caching.
- **Cloud cache**: CDN for public data products.
- **Query cache**: Cache common aggregation results.

### Storage Optimization

- **Zarr chunking**: Optimize chunk dimensions for access patterns.
- **Compression**: Use zstd for best speed/ratio, zlib for compatibility.
- **Consolidation**: Merge small files for improved read performance.

## Security Considerations

- **Data authentication**: Verify data integrity with checksums and digital signatures.
- **Access control**: Implement RBAC for data download and modification.
- **Encryption**: TLS 1.3 for transport, AES-256 for storage.
- **Audit logging**: Track all data access and modification events.
- **License compliance**: Respect data usage restrictions and attribution requirements.

## Troubleshooting Guide

### Common Issues

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| NetCDF read error | Missing dependencies | Install netcdf4, h5py |
| Memory error | Dataset too large | Use chunked reading, Dask |
| CF validation errors | Non-compliant metadata | Fix attributes per CF spec |
| Spatial query slow | No spatial index | Create spatial index on data |
| Download timeout | Server rate limiting | Implement retry with backoff |

## API Reference

### Core Classes

#### `OceanDataset`

```python
class OceanDataset:
    def __init__(self, path: str, format: str = "auto")
    def subset(self, **kwargs) -> OceanDataset
    def to_zarr(self, path: str, **kwargs) -> None
    def validate_cf(self) -> CFReport
    def compute_derived(self, variable: str, func: Callable) -> OceanDataset
```

#### `DataCatalog`

```python
class DataCatalog:
    def search(self, query: str, **filters) -> List[DatasetMetadata]
    def list_datasets(self, source: str) -> List[DatasetMetadata]
    def get_metadata(self, dataset_id: str) -> DatasetMetadata
```

## Data Models

### Dataset Metadata Schema

```sql
CREATE TABLE datasets (
    id UUID PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    source VARCHAR(128),
    format VARCHAR(32),
    variables JSONB NOT NULL,
    spatial_extent JSONB,
    temporal_extent JSONB,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_datasets_variables ON datasets USING GIN (variables);
CREATE INDEX idx_datasets_spatial ON datasets USING GIST (
    ST_MakeEnvelope(
        (spatial_extent->>'west')::float,
        (spatial_extent->>'south')::float,
        (spatial_extent->>'east')::float,
        (spatial_extent->>'north')::float,
        4326
    )
);
```

## Deployment Guide

### Docker Deployment

```yaml
version: '3.8'
services:
  ocean-data-api:
    image: ocean-data/api:latest
    ports:
      - "8080:8080"
    volumes:
      - /data/ocean:/data:ro
    environment:
      - DATABASE_URL=postgresql://localhost/ocean_data
  ocean-data-worker:
    image: ocean-data/worker:latest
    environment:
      - REDIS_URL=redis://localhost:6379
      - WORKER_CONCURRENCY=4
```

## Monitoring & Observability

### Self-Monitoring Metrics

- `ocean_data_ingestion_total` — datasets ingested.
- `ocean_data_queries_total` — data queries executed.
- `ocean_data_storage_bytes` — total storage usage.
- `ocean_data_processing_seconds` — processing duration.

## Testing Strategy

### Unit Testing

```python
def test_cf_validation():
    dataset = OceanDataset("test.nc")
    report = dataset.validate_cf()
    assert report.score >= 0.95

def test_spatial_subset():
    dataset = OceanDataset("global_sst.nc")
    subset = dataset.subset(
        latitude=(30, 40),
        longitude=(-130, -120)
    )
    assert subset.spatial_extent['south'] >= 30
```

## Versioning & Migration

- **v1.0.0**: Initial release with NetCDF support and basic querying.
- **v1.1.0**: Added ERDDAP and OPeNDAP integration.
- **v1.2.0**: Zarr support and cloud-optimized storage.

## Glossary

| Term | Definition |
|------|-----------|
| CF-Convention | Metadata standard for climate/forecast data |
| Zarr | Cloud-native chunked array storage format |
| ERDDAP | Environmental data server for ocean data |
| OPeNDAP | Protocol for remote access to scientific data |
| Bathymetry | Measurement of ocean depth |

## Changelog

### v1.2.0
- Added Zarr format support.
- Cloud-optimized storage backend.
- Performance optimization for large datasets.

### v1.1.0
- ERDDAP and OPeNDAP integration.
- CF-compliance validation tools.
- Enhanced spatial querying.

### v1.0.0
- Initial release with NetCDF support.
- Basic data discovery and download.

## Contributing Guidelines

1. Fork the repository and create a feature branch.
2. Write tests for all new functionality.
3. Follow the existing code style and naming conventions.
4. Update documentation for any API changes.
5. Add entries to the changelog for user-facing changes.
6. Submit a pull request with a clear description of changes.

### Zarr Store Configuration

```python
from ocean_data import ZarrStore

store = ZarrStore(
    path="s3://ocean-data-zarr",
    compressor="zstd",
    chunk_shape={"time": 365, "latitude": 180, "longitude": 360},
    consolidated_metadata=True,
    overwrite_encoded_chunks=True
)

# Write dataset to Zarr
dataset.to_zarr(store=store, mode="w", consolidated=True)

# Read subset from Zarr
subset = xr.open_zarr(store=store).sel(
    latitude=slice(30, 40),
    time=slice("2024-01-01", "2024-12-31")
)
```

### Data Lineage Tracking

```python
from ocean_data import LineageTracker

tracker = LineageTracker(
    storage="postgresql://localhost/ocean_lineage"
)

# Track data provenance
tracker.record(
    dataset_id="sst_daily_2024",
    source="satellite",
    processing_steps=["calibration", "cloud_masking", "interpolation"],
    parent_datasets=["sst_raw_2024", "cloud_mask_2024"],
    metadata={"algorithm": "optimal_interpolation", "resolution": "1km"}
)

# Query lineage
lineage = tracker.get_lineage(dataset_id="sst_daily_2024")
```

### Data Visualization

```python
from ocean_data import OceanVisualizer

viz = OceanVisualizer(
    projection="mercator",
    colormap="viridis",
    resolution="high"
)

# Create SST map
sst_map = viz.create_map(
    data=sst_dataset,
    variable="sea_surface_temperature",
    title="Sea Surface Temperature - January 2024",
    colorbar_units="degC",
    extent=(-180, 180, -60, 60)
)

sst_map.save("sst_jan_2024.png", dpi=300)

# Create vertical section plot
section = viz.create_section(
    data=profile_data,
    variables=["temperature", "salinity"],
    x_axis="distance",
    y_axis="depth",
    title="Temperature-Salinity Section"
)
```

### Data Quality Assessment

```python
from ocean_data import QualityAssessor

assessor = QualityAssessor(
    cf_standards=True,
    range_checks=True,
    gradient_checks=True,
    spike_checks=True
)

# Assess dataset quality
report = assessor.assess(dataset)

print(f"Overall quality score: {report.quality_score:.2f}")
print(f"Total records: {report.total_records}")
print(f"Pass: {report.pass_count}")
print(f"Flagged: {report.flagged_count}")
print(f"Failed: {report.failed_count}")
```

### Multi-Resolution Data Fusion

```python
from ocean_data import DataFusion

fusion = DataFusion(
    algorithm="optimal_interpolation",
    correlation_scale={"spatial": 100, "temporal": 24},  # km, hours
    noise_ratio=0.1
)

# Fuse satellite and in-situ data
fused = fusion.fuse(
    satellite_data=sst_satellite,
    insitu_data=buoy_observations,
    output_resolution={"spatial": "0.1deg", "temporal": "daily"}
)
```

### Climate Data Processing

```python
from ocean_data import ClimateProcessor

processor = ClimateProcessor(
    base_period="1991-2020",
    anomalies=True
)

# Calculate climate normals
normals = processor.calculate_normals(
    dataset=sst_monthly,
    variables=["sst"]
)

# Calculate anomalies
anomalies = processor.calculate_anomalies(
    data=sst_monthly,
    normals=normals
)

# Calculate trends
trends = processor.calculate_trends(
    data=anomalies,
    method="linear",
    confidence_level=0.95
)
```

### Data Discovery API

```python
from ocean_data import DataDiscoveryAPI

api = DataDiscoveryAPI(
    catalog_backends=["erddap", "opendap", "local"],
    search_engine="elasticsearch"
)

# Search for datasets
results = api.search(
    query="sea surface temperature",
    spatial_filter={"bbox": [-180, -90, 180, 90]},
    temporal_filter={"start": "2024-01-01", "end": "2024-12-31"},
    variable_filter=["sst", "temperature"],
    max_results=50
)

for dataset in results:
    print(f"{dataset.name}: {dataset.description}")
    print(f"  Source: {dataset.source}")
    print(f"  Variables: {dataset.variables}")
```

### Ocean Data API

```yaml
ocean_data_api:
  endpoints:
    - path: "/api/v1/datasets"
      method: "GET"
      description: "List available datasets"
    - path: "/api/v1/datasets/{id}/subset"
      method: "GET"
      description: "Subset a dataset"
    - path: "/api/v1/datasets/{id}/variables"
      method: "GET"
      description: "List dataset variables"
  authentication:
    type: "api_key"
    header: "X-API-Key"
  rate_limiting:
    requests_per_minute: 100
    burst: 20
```

## Advanced Topics

### Ocean Data Standardization and Interoperability

Ensuring data follows international standards for seamless integration across global ocean observation networks.

```python
from ocean_data import Standardizer, CFConvention, ACDDConvention

standardizer = Standardizer(
    conventions=[CFConvention(version="1.11"), ACDDConvention(version="1.3")],
    enforce_compliance=True
)

# Standardize a raw dataset
raw_dataset = xr.open_dataset("raw_ocean_profile.nc")
standardized = standardizer.standardize(
    raw_dataset,
    global_attributes={
        "title": "CTD Profile - Station 42",
        "institution": "Ocean Research Institute",
        "source": "CTD Rosette",
        "history": "Processed using OceanData v2.1"
    },
    variable_mapping={
        "temp": ("sea_water_temperature", {"standard_name": "sea_water_temperature", "units": "degC"}),
        "sal": ("sea_water_practical_salinity", {"standard_name": "sea_water_practical_salinity"}),
        "depth": ("depth", {"standard_name": "depth", "units": "m", "positive": "down"})
    }
)

# Validate compliance
report = standardizer.validate(standardized)
print(f"CF compliance: {report.cf_score:.1%}")
print(f"ACDD compliance: {report.acdd_score:.1%}")
for issue in report.issues:
    print(f"  Issue: {issue.severity} - {issue.message}")
```

### Time Series Gap Filling and Interpolation

Robust methods for handling missing data in ocean time series observations.

```python
from ocean_data import GapFiller, InterpolationMethod

filler = GapFiller(
    method=InterpolationMethod.OPTIMAL_INTERPOLATION,
    max_gap_duration="7D",
    confidence_threshold=0.7
)

# Define interpolation parameters
oi_config = {
    "correlation_length_scale": 50000,  # meters
    "temporal_correlation_scale": 86400,  # seconds
    "noise_to_signal_ratio": 0.1,
    "background_error_variance": 0.5
}

# Fill gaps in temperature time series
filled = filler.fill(
    timeseries=sst_timeseries,
    covariates=[{
        "name": "sst_l4",
        "weight": 0.6,
        "source": "modis_aqua"
    }, {
        "name": "sst_l3",
        "weight": 0.4,
        "source": "viirs"
    }],
    config=oi_config
)

print(f"Original coverage: {filled.original_completeness:.1%}")
print(f"Filled coverage: {filled.filled_completeness:.1%}")
print(f"Gaps filled: {filled.gaps_filled}")
print(f"Mean interpolation error: {filled.mean_error:.3f} degC")
```

### Multi-Resolution Data Aggregation

Combining observations at different spatial and temporal resolutions into unified analysis-ready products.

```python
from ocean_data import MultiResolutionAggregator, AggregationStrategy

aggregator = MultiResolutionAggregator(
    target_grid={
        "resolution": 0.1,  # degrees
        "bounds": (-60, 60, -180, 180)
    },
    temporal_resolution="daily"
)

# Register input datasets with varying resolutions
aggregator.add_source(
    name="modis_sst",
    resolution=0.04,  # ~4km
    temporal="daily",
    weight=0.5,
    uncertainty=0.3
)

aggregator.add_source(
    name="viirs_sst",
    resolution=0.02,  # ~2km
    temporal="daily",
    weight=0.3,
    uncertainty=0.25
)

aggregator.add_source(
    name="drifter_sst",
    resolution="point",
    temporal="6hourly",
    weight=0.2,
    uncertainty=0.15
)

# Produce multi-resolution fused product
product = aggregator.aggregate(
    variable="sea_surface_temperature",
    start_date="2024-01-01",
    end_date="2024-01-31"
)

print(f"Output grid: {product.shape}")
print(f"Sources integrated: {product.sources_used}")
print(f"Weighted mean uncertainty: {product.mean_uncertainty:.3f}")
```

### Ocean Data Quality Control Pipeline

Automated quality control following international standards (WOD, GTSPP) with customizable flags and thresholds.

```yaml
qc_pipeline:
  stage_1_range_checks:
    - variable: "sea_water_temperature"
      valid_range: [-2.5, 35.0]
      action: "flag"
    - variable: "sea_water_salinity"
      valid_range: [0, 42.0]
      action: "flag"
    - variable: "pressure"
      valid_range: [0, 11000]
      action: "flag"

  stage_2_gradient_checks:
    temperature:
      vertical_gradient: 0.5  # degC per dbar
      horizontal_gradient: 2.0  # degC per 100km
      temporal_gradient: 3.0  # degC per day
    salinity:
      vertical_gradient: 0.1  # PSU per dbar
      horizontal_gradient: 0.5  # PSU per 100km

  stage_3_climatological_checks:
    enabled: true
    reference_climatology: "WOD18"
    deviation_threshold: 3.0  # standard deviations
    seasonal_adjustment: true

  stage_4_spike_detection:
    method: "median_filter"
    window_size: 5
    threshold: 2.5  # deviations from local median

  stage_5_density_consistency:
    enabled: true
    max_density_inversion: 0.01  # kg/m3
    check_depth_range: [0, 500]

  output_flags:
    good: 1
    probably_good: 2
    probably_bad: 3
    bad: 4
    missing: 9
```

### Real-Time Data Ingestion Architecture

High-throughput ingestion pipeline for real-time ocean observation data streams.

```python
from ocean_data import IngestionPipeline, StreamConfig

pipeline = IngestionPipeline(
    buffer_size=1_000_000,
    batch_size=10_000,
    parallel_workers=4
)

# Configure input streams
pipeline.add_stream(StreamConfig(
    name="gts_real_time",
    protocol="mqtt",
    broker="mqtt.oceanobs.org",
    topic="gts/observation/#",
    format="bufr",
    priority=1
))

pipeline.add_stream(StreamConfig(
    name="glider_telegram",
    protocol="ssh",
    host="glider fleet gateway",
    poll_interval=300,
    format="netcdf",
    priority=2
))

# Define processing stages
pipeline.add_stage("decode", handler="decode_bufr_or_netcdf")
pipeline.add_stage("qc", handler="realtime_qc", config={"strict": False})
pipeline.add_stage("transform", handler="cf_standardize")
pipeline.add_stage("store", handler="write_to_database")

# Monitor pipeline health
stats = pipeline.get_stats()
print(f"Messages processed: {stats.total_processed}")
print(f"Processing rate: {stats.messages_per_second:.1f} msg/s")
print(f"Error rate: {stats.error_rate:.3%}")
print(f"Latency p99: {stats.latency_p99_ms:.0f} ms")
```

### Ocean Data Web Services and APIs

Implementing OGC-compliant web services for ocean data distribution.

```yaml
web_services:
  wms:
    version: "1.3.0"
    supported_formats:
      - "image/png"
      - "image/jpeg"
      - "image/tiff"
    layers:
      - name: "sst"
        title: "Sea Surface Temperature"
        queryable: true
        time_extent: "2024-01-01/P1D"
      - name: "salinity"
        title: "Sea Surface Salinity"
        queryable: true
        time_extent: "2024-01-01/P1D"

  wcs:
    version: "2.0.1"
    coverage_type: "grid"
    supported_formats:
      - "application/netcdf"
      - "application/x-netcdf"
      - "text/csv"

  opendap:
    enabled: true
    max_concurrent_clients: 100
    cache_size: "10GB"

  stac:
    enabled: true
    catalog_title: "Ocean Observation Data Catalog"
    conformance_classes:
      - "STAC API - Core"
      - "STAC API - Features"
      - "STAC API - Filter"
```

## Performance Tuning

### Parallel Processing Configuration

```python
from ocean_data import ParallelProcessor

processor = ParallelProcessor(
    scheduler="distributed",
    n_workers=16,
    memory_per_worker="4GB",
    threads_per_worker=2
)

# Optimize chunk sizes for large NetCDF files
processor.optimize_chunks(
    dataset=large_dataset,
    target_chunk_size="100MB",
    dim_preferences={
        "time": 1,
        "lat": -1,
        "lon": -1,
        "depth": 1
    }
)
```

### Database Indexing Strategy

```sql
-- Create spatial index for fast geographic queries
CREATE INDEX idx_obs_location
ON observations USING GIST (ST_MakePoint(longitude, latitude));

-- Create temporal index for time-range queries
CREATE INDEX idx_obs_time
ON observations USING BRIN (timestamp)
WITH (pages_per_range = 32);

-- Composite index for common query patterns
CREATE INDEX idx_obs时空
ON observations (variable_id, timestamp)
WHERE quality_flag IN (1, 2);
```

## Security Considerations

### Data Access and Authentication

```yaml
authentication:
  method: "oauth2"
  providers:
    - name: "orcid"
      scopes: ["openid", "email", "profile"]
    - name: "institutional_saml"
      entity_id: "https://idp.oceanlab.edu"
  token_expiry: 3600
  refresh_enabled: true

authorization:
  model: "rbac"
  roles:
    - name: "public"
      access: ["metadata", "low_res_products"]
    - name: "researcher"
      access: ["metadata", "all_data", "download"]
      requires: ["verified_email", "institution"]
    - name: "data_provider"
      access: ["upload", "edit_own", "metadata"]
      requires: ["data_agreement"]
```

### Secure Data Transfer

```yaml
data_transfer:
  protocols:
    - name: "sftp"
      port: 22
      auth: "public_key"
      cipher: "aes256-ctr"
    - name: "https"
      port: 443
      tls_version: "1.3"
      client_cert_auth: true
  checksums:
    algorithm: "sha256"
    verify_on_transfer: true
  compression:
    enabled: true
    algorithm: "zstd"
    level: 3
```

## License

MIT License. See the root LICENSE file for full terms.
