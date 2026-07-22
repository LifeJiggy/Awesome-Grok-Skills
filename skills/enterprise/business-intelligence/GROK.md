---
name: "Business Intelligence"
version: "2.0.0"
description: "Comprehensive business intelligence toolkit with data warehousing, ETL pipelines, OLAP analysis, dashboard creation, and reporting for enterprise analytics"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["enterprise", "business-intelligence", "ETL", "OLAP", "dashboards", "reporting"]
category: "enterprise"
personality: "bi-engineer"
use_cases: ["data warehousing", "ETL pipelines", "OLAP analysis", "dashboards", "enterprise reporting"]
---

# Business Intelligence

> Production-grade business intelligence framework providing data warehousing, ETL pipelines, OLAP analysis, dashboard creation, and comprehensive reporting for enterprise analytics.

## Overview

The Business Intelligence module provides tools for transforming raw data into actionable business insights. It implements data warehouse design and management, ETL/ELT pipeline orchestration, OLAP cube operations, interactive dashboard creation, and enterprise reporting. Every analysis includes data quality checks, lineage tracking, and audit logging.

## Core Capabilities

### 1. Data Warehousing
- Star and snowflake schema design
- Dimensional modeling
- Slowly changing dimensions (SCD)
- Data quality management
- Metadata management

### 2. ETL/ELT Pipelines
- Extract from multiple sources
- Transform with business rules
- Load into target systems
- Incremental loading
- Data lineage tracking

### 3. OLAP Analysis
- Cube creation and management
- Drill-down and roll-up operations
- Slice and dice operations
- Pivot table analysis
- What-if analysis

### 4. Dashboard Creation
- Interactive visualizations
- Real-time data binding
- Cross-filtering and drill-through
- Mobile-responsive design
- Embedding support

### 5. Reporting
- Pixel-perfect report design
- Scheduled report generation
- Distribution management
- Parameterized reports
- Export to multiple formats

### 6. Data Governance
- Data catalog management
- Data quality rules
- Access control
- Audit logging
- Compliance reporting

## Usage Examples

### Data Warehouse Design

```python
from business_intelligence import DataWarehouse, SchemaType

warehouse = DataWarehouse()

# Design star schema
schema = warehouse.create_schema(
    name="sales_warehouse",
    schema_type=SchemaType.STAR,
    fact_table="fact_sales",
    dimension_tables=["dim_date", "dim_product", "dim_customer", "dim_store"],
)

print(f"Schema: {schema.name}")
print(f"Fact table: {schema.fact_table}")
print(f"Dimensions: {len(schema.dimension_tables)}")
```

### ETL Pipeline

```python
from business_intelligence import ETLPipeline, DataSource

pipeline = ETLPipeline(name="sales_etl")

# Define pipeline steps
pipeline.add_extract(DataSource(type="database", connection="source_db"))
pipeline.add_transform({"type": "clean", "rules": ["remove_nulls", "standardize_dates"]})
pipeline.add_transform({"type": "aggregate", "group_by": ["product_id", "date"]})
pipeline.add_load(target="data_warehouse", table="fact_sales")

# Run pipeline
result = pipeline.run()
print(f"Records processed: {result.records_processed}")
print(f"Duration: {result.duration_seconds:.1f}s")
print(f"Errors: {result.errors}")
```

### OLAP Analysis

```python
from business_intelligence import OLAPCube, AnalysisType

cube = OLAPCube(name="sales_cube")

# Perform analysis
result = cube.analyze(
    analysis_type=AnalysisType.DRILL_DOWN,
    dimensions=["date", "product_category"],
    measures=["revenue", "quantity"],
    filters={"region": "North America"},
)

print(f"Results: {len(result.data_points)} data points")
print(f"Total revenue: ${result.totals['revenue']:,.2f}")
```

### Dashboard

```python
from business_intelligence import Dashboard, Widget

dashboard = Dashboard(title="Sales Dashboard")

# Add widgets
dashboard.add_widget(Widget(
    type="line_chart",
    title="Revenue Trend",
    data_source="sales_cube",
    dimensions=["date"],
    measures=["revenue"],
))

dashboard.add_widget(Widget(
    type="kpi_card",
    title="Total Revenue",
    data_source="sales_cube",
    measure="revenue",
    format="$#,##0",
))

print(f"Dashboard: {dashboard.title}")
print(f"Widgets: {len(dashboard.widgets)}")
```

## Best Practices

### Data Warehousing
- Use star schema for simplicity
- Implement SCD Type 2 for historical tracking
- Define clear grain for fact tables
- Document all business rules

### ETL
- Implement data quality checks at each stage
- Use incremental loading for large datasets
- Track data lineage for compliance
- Handle errors gracefully

### OLAP
- Pre-aggregate common queries
- Use appropriate grain levels
- Implement caching for performance
- Monitor cube size and performance

### Dashboards
- Focus on key metrics (KPIs)
- Enable drill-down for details
- Design for mobile viewing
- Update data in real-time

## Related Modules

- **data-warehousing**: Data warehouse management
- **crm-systems**: Customer data integration
- **erp-systems**: ERP data integration
- **workflow-automation**: BI workflow automation

---

## Advanced Configuration

### ETL Pipeline Settings

```python
from business_intelligence import ETLConfig

etl_config = ETLConfig(
    # Source Configuration
    sources={
        "database": {
            "type": "postgresql",
            "batch_size": 10000,
            "parallelism": 4,
        },
        "api": {
            "type": "rest",
            "rate_limit": 100,
            "timeout_s": 30,
        },
    },
    
    # Transformation
    transformation={
        "engine": "spark",  # spark, dask, pandas
        "memory_limit_gb": 8,
        "checkpoint_interval": 1000,
    },
    
    # Loading
    loading={
        "target": "redshift",
        "batch_size": 50000,
        "parallel_load": True,
        "upsert": True,
    },
)
```

### Dashboard Configuration

```python
from business_intelligence import DashboardConfig

dashboard_config = DashboardConfig(
    # Refresh Settings
    refresh={
        "auto_refresh": True,
        "interval_seconds": 300,
        "on_demand": True,
    },
    
    # Caching
    caching={
        "enabled": True,
        "ttl_seconds": 600,
        "cache_backend": "redis",
    },
    
    # Security
    security={
        "row_level_security": True,
        "column_masking": True,
        "audit_logging": True,
    },
)
```

## Architecture Patterns

### BI Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Data Sources                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Database │  │ API      │  │ Files    │         │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘         │
└───────┼──────────────┼──────────────┼───────────────┘
        │              │              │
        ▼              ▼              ▼
┌─────────────────────────────────────────────────────┐
│                    ETL Layer                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Extract  │──│Transform │──│ Load     │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│              Data Warehouse                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Staging  │──│ DIM      │──│ FACT     │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│               Presentation Layer                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │Dashboards│  │ Reports  │  │ Analytics│         │
│  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────────────────────────────────────┘
```

### OLAP Cube Design

```python
from business_intelligence import OLAPCube

cube = OLAPCube()

# Define cube schema
cube.define(
    name="sales_cube",
    facts=[
        {"name": "amount", "type": "decimal", "aggregation": "sum"},
        {"name": "quantity", "type": "integer", "aggregation": "sum"},
    ],
    dimensions=[
        {"name": "time", "hierarchy": ["year", "quarter", "month", "day"]},
        {"name": "product", "hierarchy": ["category", "subcategory", "product"]},
        {"name": "geography", "hierarchy": ["country", "state", "city"]},
    ],
)

# Build cube
cube.build(source="sales_data")
print(f"Cube built: {cube.cell_count} cells")
```

## Integration Guide

### Data Source Integration

```python
from business_intelligence import DataSourceManager

dsm = DataSourceManager()

# Connect to source
dsm.connect(
    name="sales_db",
    type="postgresql",
    connection_string="postgresql://user:pass@host:5432/sales",
)

# Extract data
data = dsm.extract(
    source="sales_db",
    query="SELECT * FROM sales WHERE date >= '2024-01-01'",
    incremental=True,
    last_extract="2024-01-15",
)
```

### Reporting Integration

```python
from business_intelligence import ReportManager

reports = ReportManager()

# Generate report
report = reports.generate(
    template="monthly_sales",
    parameters={
        "start_date": "2024-01-01",
        "end_date": "2024-01-31",
        "region": "North America",
    },
    format="pdf",
)

# Distribute report
reports.distribute(
    report_id=report.id,
    recipients=["cfo@company.com", "sales-team@company.com"],
    schedule="monthly",
)
```

## Performance Optimization

### Query Optimization

```python
from business_intelligence import QueryOptimizer

optimizer = QueryOptimizer()

# Optimize query
optimized = optimizer.optimize(
    query="SELECT product, SUM(amount) FROM sales GROUP BY product",
    strategies=[
        "materialized_views",
        "partition_pruning",
        "columnar_storage",
    ],
)

print(f"Original time: {optimized.original_ms:.0f}ms")
print(f"Optimized time: {optimized.optimized_ms:.0f}ms")
print(f"Improvement: {optimized.improvement:.1%}")
```

### ETL Optimization

```python
from business_intelligence import ETLOptimizer

etl_opt = ETLOptimizer()

# Optimize ETL pipeline
result = etl_opt.optimize(
    pipeline="sales_etl",
    strategies=[
        "parallel_extraction",
        "incremental_loading",
        "compression",
    ],
)

print(f"Original duration: {result.original_minutes:.1f}min")
print(f"Optimized duration: {result.optimized_minutes:.1f}min")
print(f"Resource savings: {result.resource_savings:.1%}")
```

## Security Considerations

### Data Security

```python
from business_intelligence import BISecurity

security = BISecurity()

# Implement row-level security
security.enable_row_security(
    table="sales",
    rules=[
        {"role": "sales_rep", "filter": "region = current_user_region()"},
        {"role": "manager", "filter": "true"},
    ],
)

# Column masking
security.mask_column(
    table="customers",
    column="email",
    mask_type="partial",
)
```

### Audit Logging

```python
from business_intelligence import AuditLogger

audit = AuditLogger()

# Log data access
audit.log(
    user="analyst@company.com",
    action="query",
    object="sales_cube",
    query="SELECT * FROM sales WHERE region='EMEA'",
    rows_accessed=1500,
)
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Slow ETL | Large data volume | Use incremental loading, parallelize |
| Dashboard lag | Uncached queries | Enable caching, optimize queries |
| Data staleness | Refresh issues | Check ETL schedule, fix failures |
| Access denied | Permission issues | Review RLS policies |
| Memory errors | Large datasets | Use sampling, optimize transformations |

### Debug Mode

```python
from business_intelligence import enable_debug

enable_debug(
    components=["etl", "olap", "dashboard"],
    log_level="DEBUG",
)

# Debug ETL pipeline
debug_session = debug.trace_pipeline("sales_etl")
print(f"Debug report: {debug_session.report_url}")
```

## API Reference

### REST Endpoints

```
GET    /api/v1/bi/dashboards                List dashboards
GET    /api/v1/bi/dashboards/{id}           Get dashboard
POST   /api/v1/bi/dashboards/{id}/refresh   Refresh dashboard
GET    /api/v1/bi/reports                   List reports
POST   /api/v1/bi/reports/generate          Generate report
GET    /api/v1/bi/etl/pipelines             List ETL pipelines
POST   /api/v1/bi/etl/pipelines/{id}/run    Run ETL pipeline
GET    /api/v1/bi/olap/cubes                List OLAP cubes
```

### Data Models

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from uuid import UUID

@dataclass
class Dashboard:
    dashboard_id: UUID
    name: str
    widgets: List["Widget"]
    refresh_interval_s: int
    last_refreshed: datetime
    owner: str

@dataclass
class Widget:
    widget_id: UUID
    type: str  # chart, table, kpi
    query: str
    visualization: dict
    position: dict

@dataclass
class ETLJob:
    job_id: UUID
    name: str
    source: str
    target: str
    status: str
    last_run: datetime
    next_run: datetime
    duration_minutes: float
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bi-platform
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bi-platform
  template:
    spec:
      containers:
      - name: bi-api
        image: bi-platform:latest
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        env:
        - name: WAREHOUSE_URL
          valueFrom:
            secretKeyRef:
              name: bi-secrets
              key: warehouse-url
```

## Monitoring & Observability

### Key Metrics

```python
from business_intelligence import Metrics

metrics = Metrics()

# Track ETL performance
metrics.histogram("etl.duration_minutes", duration, tags={"pipeline": "sales"})
metrics.counter("etl.rows_processed", tags={"pipeline": "sales"})

# Track dashboard usage
metrics.counter("dashboard.views", tags={"dashboard": "sales_overview"})
metrics.histogram("dashboard.load_time_ms", load_time)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from business_intelligence import ETLProcessor

@pytest.fixture
def processor():
    return ETLProcessor(test_mode=True)

def test_extract(processor):
    data = processor.extract(
        source="test_db",
        query="SELECT * FROM test_table",
    )
    assert len(data) > 0
```

## Versioning & Migration

### Version History

- **2.0.0**: Added real-time dashboards, advanced OLAP, ML-powered insights
- **1.5.0**: Added ETL optimization, report scheduling
- **1.0.0**: Initial release with basic BI capabilities

## Glossary

| Term | Definition |
|------|------------|
| **ETL** | Extract, Transform, Load |
| **OLAP** | Online Analytical Processing |
| **KPI** | Key Performance Indicator |
| **Data Warehouse** | Central repository for analytical data |
| **Cube** | Multidimensional data structure |
| **Dashboard** | Visual representation of KPIs |

## Changelog

### Version 2.0.0
- Real-time dashboard updates
- Advanced OLAP operations
- ML-powered insights
- Enhanced security features

### Version 1.5.0
- ETL pipeline optimization
- Report scheduling and distribution
- Performance improvements

### Version 1.0.0
- Initial release
- Basic dashboards and reports
- Simple ETL pipelines

## Contributing Guidelines

1. Test with realistic data volumes
2. Validate data accuracy
3. Benchmark query performance
4. Document data lineage

## Data Governance Deep Dive

### Data Catalog Management

```python
from business_intelligence import DataCatalog

catalog = DataCatalog()

# Register dataset
catalog.register(
    dataset_id="sales_data_q1",
    name="Q1 2024 Sales Data",
    description="Aggregated sales data for Q1 2024",
    owner="analytics-team",
    sensitivity="confidential",
    lineage={
        "source": "sales_db",
        "transformations": ["aggregation", "deduplication"],
        "destination": "data_warehouse",
    },
    quality_score=0.95,
)

# Search catalog
results = catalog.search(query="sales data", filters={"sensitivity": "confidential"})
print(f"Found {len(results)} datasets")
```

### Data Quality Monitoring

```python
from business_intelligence import DataQualityEngine

dq_engine = DataQualityEngine()

# Define quality rules
rules = dq_engine.define_rules(
    table="fact_sales",
    rules=[
        {"column": "revenue", "rule": "not_null", "threshold": 0.99},
        {"column": "revenue", "rule": "positive", "threshold": 0.99},
        {"column": "product_id", "rule": "foreign_key", "references": "dim_product"},
        {"column": "date", "rule": "not_future"},
    ],
)

# Run quality checks
results = dq_engine.check(table="fact_sales")
print(f"Quality Score: {results.quality_score:.1%}")
print(f"Rules Passed: {results.passed}/{results.total}")
```

## Self-Service Analytics

### Ad-Hoc Query Builder

```python
from business_intelligence import QueryBuilder

builder = QueryBuilder()

# Build ad-hoc query
query = builder.build(
    description="Show me total sales by region for Q1 2024",
    data_source="sales_cube",
    auto_generate_sql=True,
)

print(f"Generated Query:")
print(f"  SQL: {query.sql}")
print(f"  Dimensions: {query.dimensions}")
print(f"  Measures: {query.measures}")
print(f"  Filters: {query.filters}")
```

### Dashboard Sharing

```python
from business_intelligence import DashboardSharing

sharing = DashboardSharing()

# Share dashboard
share = sharing.share(
    dashboard_id="sales-overview",
    recipients=["team@company.com"],
    permissions="view",
    expiry_days=30,
)

print(f"Dashboard Shared:")
print(f"  Share URL: {share.url}")
print(f"  Expiry: {share.expiry_date}")
print(f"  Permissions: {share.permissions}")
```

## Advanced Analytics Patterns

### Cohort Analysis

```python
from business_intelligence import CohortAnalyzer

analyzer = CohortAnalyzer()

# Perform cohort analysis
cohorts = analyzer.analyze(
    metric="customer_retention",
    cohort_period="monthly",
    time_periods=12,
)

print(f"Cohort Analysis:")
for cohort in cohorts[:3]:
    print(f"\n{cohort.name}:")
    for period, value in cohort.retention_curve.items():
        print(f"  Month {period}: {value:.1%}")
```

### What-If Analysis

```python
from business_intelligence import WhatIfAnalyzer

analyzer = WhatIfAnalyzer()

# Run what-if scenarios
scenarios = analyzer.run(
    base_scenario="current_quarter",
    what_if_changes=[
        {"variable": "marketing_spend", "change": "+20%"},
        {"variable": "pricing", "change": "-5%"},
        {"variable": "headcount", "change": "+10%"},
    ],
)

for scenario in scenarios:
    print(f"\nScenario: {scenario.name}")
    print(f"  Revenue Impact: {scenario.revenue_impact:+.1%}")
    print(f"  Profit Impact: {scenario.profit_impact:+.1%}")
    print(f"  Risk Level: {scenario.risk_level}")
```

### Trend Analysis

```python
from business_intelligence import TrendAnalyzer

analyzer = TrendAnalyzer()

# Analyze trends
trends = analyzer.analyze(
    metric="revenue",
    time_range="24_months",
    granularity="monthly",
    decomposition=True,
)

print(f"Trend Analysis:")
print(f"  Trend Direction: {trends.direction}")
print(f"  Trend Strength: {trends.strength:.2f}")
print(f"  Seasonality: {trends.seasonality_pattern}")
print(f"  Forecast (3 months): {trends.forecast_next_3_months}")
```

## Data Lineage and Impact Analysis

### Data Lineage Tracking

```python
from business_intelligence import LineageTracker

tracker = LineageTracker()

# Track data lineage
lineage = tracker.trace(
    target_table="fact_sales",
    direction="upstream",
    depth=5,
)

print(f"Data Lineage for fact_sales:")
for source in lineage.sources:
    print(f"  Source: {source.table}.{source.column}")
    print(f"    Transformation: {source.transformation}")
    print(f"    Last Updated: {source.last_updated}")
```

### Impact Analysis

```python
from business_intelligence import ImpactAnalyzer

analyzer = ImpactAnalyzer()

# Analyze impact of schema change
impact = analyzer.analyze(
    change_type="column_addition",
    table="dim_product",
    column="new_attribute",
    column_type="VARCHAR(100)",
)

print(f"Impact Analysis:")
print(f"  Affected Dashboards: {impact.dashboard_count}")
print(f"  Affected Reports: {impact.report_count}")
print(f"  Affected ETL Jobs: {impact.etl_job_count}")
print(f"  Risk Level: {impact.risk_level}")
```

## Report Scheduling and Distribution

### Automated Report Generation

```python
from business_intelligence import ReportScheduler

scheduler = ReportScheduler()

# Schedule report
schedule = scheduler.schedule(
    report_id="monthly_sales",
    frequency="monthly",
    recipients=["cfo@company.com", "sales-team@company.com"],
    format="pdf",
    delivery_time="09:00",
)

print(f"Report Scheduled:")
print(f"  Report: {schedule.report_name}")
print(f"  Frequency: {schedule.frequency}")
print(f"  Next Run: {schedule.next_run}")
print(f"  Recipients: {len(schedule.recipients)}")
```

## License

MIT License - Copyright (c) 2024 Awesome Grok Skills