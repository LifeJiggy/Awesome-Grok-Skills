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