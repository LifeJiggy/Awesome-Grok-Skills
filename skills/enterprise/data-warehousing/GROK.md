---
name: "Data Warehousing"
version: "2.0.0"
description: "Comprehensive data warehousing toolkit with schema design, ETL management, data quality, performance optimization, and governance for enterprise data platforms"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["enterprise", "data-warehousing", "ETL", "data-quality", "performance", "governance"]
category: "enterprise"
personality: "data-warehouse-engineer"
use_cases: ["schema design", "ETL management", "data quality", "performance optimization", "data governance"]
---

# Data Warehousing

> Production-grade data warehousing framework providing schema design, ETL management, data quality, performance optimization, and data governance for enterprise data platforms.

## Overview

The Data Warehousing module provides tools for building and operating enterprise data warehouses. It implements dimensional schema design, ETL pipeline management, data quality monitoring, query performance optimization, and comprehensive data governance. Every component includes monitoring, alerting, and audit capabilities.

## Core Capabilities

### 1. Schema Design
- Star schema modeling
- Snowflake schema modeling
- Slowly changing dimensions (SCD)
- Surrogate key management
- Schema documentation

### 2. ETL Management
- Extract from diverse sources
- Transform with business rules
- Load strategies (full, incremental)
- Error handling and recovery
- Lineage tracking

### 3. Data Quality
- Quality rule definition
- Automated quality checks
- Data profiling
- Anomaly detection
- Quality dashboards

### 4. Performance Optimization
- Query optimization
- Index management
- Partition strategies
- Materialized views
- Statistics management

### 5. Data Governance
- Data catalog management
- Access control
- Audit logging
- Compliance reporting
- Retention policies

### 6. Monitoring
- ETL job monitoring
- Query performance tracking
- Storage utilization
- Data freshness monitoring
- Alert management

## Usage Examples

### Schema Design

```python
from data_warehousing import SchemaDesigner, DimensionType

designer = SchemaDesigner()

# Design star schema
schema = designer.design_star_schema(
    name="sales_warehouse",
    fact_table="fact_sales",
    measures=["revenue", "quantity", "discount"],
    dimensions={
        "date": {"type": DimensionType.DATE, "scd_type": 2},
        "product": {"type": DimensionType.STANDARD, "scd_type": 1},
        "customer": {"type": DimensionType.STANDARD, "scd_type": 2},
        "store": {"type": DimensionType.STANDARD, "scd_type": 1},
    },
)

print(f"Schema: {schema.name}")
print(f"Fact measures: {schema.measures}")
print(f"Dimensions: {len(schema.dimensions)}")
```

### ETL Pipeline

```python
from data_warehousing import DataPipeline, LoadStrategy

pipeline = DataPipeline(name="daily_sales_etl")

# Configure pipeline
pipeline.extract(source="source_db", query="SELECT * FROM sales")
pipeline.transform([
    {"type": "clean", "rules": ["remove_duplicates"]},
    {"type": "enrich", "lookup": "product_dim"},
    {"type": "aggregate", "group_by": ["date", "product_id"]},
])
pipeline.load(target="data_warehouse", table="fact_sales", strategy=LoadStrategy.INCREMENTAL)

# Execute
result = pipeline.execute()
print(f"Records: {result.records_processed}")
print(f"Duration: {result.duration_seconds:.1f}s")
```

### Data Quality

```python
from data_warehousing import DataQualityEngine, QualityRule

engine = DataQualityEngine()

# Define rules
rules = [
    QualityRule("not_null", "revenue", "Revenue must not be null"),
    QualityRule("range", "quantity", "Quantity must be positive", min_val=0),
    QualityRule("unique", "order_id", "Order ID must be unique"),
]

# Run checks
results = engine.check(table="fact_sales", rules=rules)
for r in results:
    status = "PASS" if r.passed else "FAIL"
    print(f"  [{status}] {r.rule_name}: {r.message}")
```

### Performance Optimization

```python
from data_warehousing import PerformanceOptimizer

optimizer = PerformanceOptimizer()

# Optimize query
optimized = optimizer.optimize_query(
    query="SELECT * FROM fact_sales WHERE date > '2024-01-01'",
    warehouse="sales_warehouse",
)

print(f"Original time: {optimized.original_ms:.0f}ms")
print(f"Optimized time: {optimized.optimized_ms:.0f}ms")
print(f"Improvement: {optimized.improvement_pct:.0f}%")
```

## Best Practices

### Schema Design
- Use surrogate keys for dimensions
- Implement SCD Type 2 for historical tracking
- Define clear grain for fact tables
- Document business rules

### ETL
- Implement idempotent loads
- Use incremental loading when possible
- Track data lineage
- Handle errors gracefully

### Data Quality
- Define quality rules at source
- Profile data regularly
- Monitor data freshness
- Set up quality dashboards

### Performance
- Partition large fact tables
- Create appropriate indexes
- Use materialized views for common queries
- Update statistics regularly

## Related Modules

- **business-intelligence**: BI tools and reporting
- **data-quality**: Advanced data quality management
- **metadata-management**: Metadata catalog
- **data-governance**: Data governance framework

---

## Advanced Configuration

### Schema Design Settings

```python
from data_warehousing import SchemaConfig

schema_config = SchemaConfig(
    # Dimensional Model
    dimensional={
        "naming_convention": "dim_",  # dim_, fact_
        "slowly_changing": "type2",  # type1, type2, type3
        " surrogate_key": True,
        "audit_columns": True,
    },
    
    # Partitioning
    partitioning={
        "strategy": "range",  # range, hash, list
        "partition_column": "date",
        "partition_interval": "monthly",
        "retention_partitions": 36,
    },
    
    # Clustering
    clustering={
        "enabled": True,
        "cluster_columns": ["date", "region"],
        "sort_columns": ["product_id"],
    },
)
```

### ETL Settings

```python
from data_warehousing import ETLConfig

etl_config = ETLConfig(
    # Extraction
    extraction={
        "method": "cdc",  # full, incremental, cdc
        "cdc_tool": "debezium",
        "batch_size": 10000,
    },
    
    # Transformation
    transformation={
        "engine": "spark",
        "cluster_size": "medium",
        "checkpoint_interval": 1000,
    },
    
    # Loading
    loading={
        "strategy": "upsert",  # insert, upsert, overwrite
        "batch_size": 50000,
        "parallel_load": True,
    },
)
```

## Architecture Patterns

### Data Warehouse Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Data Sources                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ OLTP     │  │ SaaS     │  │ Files    │         │
│  │ Systems  │  │ APIs     │  │ Logs     │         │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘         │
└───────┼──────────────┼──────────────┼───────────────┘
        │              │              │
        ▼              ▼              ▼
┌─────────────────────────────────────────────────────┐
│                   ETL Layer                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Extract  │──│Transform │──│ Load     │         │
│  │ (CDC)    │  │ (Spark)  │  │ (Bulk)   │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│               Data Warehouse                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Staging  │──│Integration│──│Presenta- │         │
│  │ Area     │  │ Layer    │  │tion Layer│         │
│  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│                Data Marts                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Sales    │  │ Marketing│  │ Finance  │         │
│  │ Mart     │  │ Mart     │  │ Mart     │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────────────────────────────────────┘
```

### Star Schema Design

```python
from data_warehousing import StarSchemaDesigner

designer = StarSchemaDesigner()

# Design star schema
schema = designer.design(
    fact_table="fact_sales",
    dimensions=[
        {"name": "dim_date", "grain": "day", "hierarchy": ["year", "quarter", "month", "day"]},
        {"name": "dim_product", "hierarchy": ["category", "subcategory", "product"]},
        {"name": "dim_customer", "hierarchy": ["segment", "region", "customer"]},
        {"name": "dim_store", "hierarchy": ["region", "state", "store"]},
    ],
    facts=[
        {"name": "sales_amount", "type": "decimal", "aggregation": "sum"},
        {"name": "quantity", "type": "integer", "aggregation": "sum"},
        {"name": "discount", "type": "decimal", "aggregation": "sum"},
    ],
)

print(f"Schema designed: {schema.tables} tables")
```

## Integration Guide

### Source System Integration

```python
from data_warehousing import SourceIntegrator

integrator = SourceIntegrator()

# Connect to source
integrator.connect(
    name="erp_system",
    type="oracle",
    connection="erp-host:1521/ERPDB",
)

# Configure CDC
integrator.configure_cdc(
    source="erp_system",
    tables=["orders", "customers", "products"],
    capture_changes=True,
)
```

### Data Quality Integration

```python
from data_warehousing import DataQualityIntegration

dq = DataQualityIntegration()

# Define quality rules
dq.define_rules(
    table="fact_sales",
    rules=[
        {"column": "sales_amount", "rule": "not_null"},
        {"column": "sales_amount", "rule": "positive"},
        {"column": "product_id", "rule": "foreign_key", "references": "dim_product"},
    ],
)

# Run quality checks
results = dq.check(table="fact_sales")
print(f"Pass rate: {results.pass_rate:.1%}")
print(f"Failed records: {results.failed_count}")
```

## Performance Optimization

### Query Performance

```python
from data_warehousing import QueryOptimizer

optimizer = QueryOptimizer()

# Optimize query performance
result = optimizer.optimize(
    warehouse="sales_warehouse",
    strategies=[
        "materialized_views",
        "partition_pruning",
        "columnar_compression",
        "query_result_cache",
    ],
)

print(f"Average query time: {result.avg_query_ms:.0f}ms")
print(f"Cache hit rate: {result.cache_hit_rate:.1%}")
```

### ETL Performance

```python
from data_warehousing import ETLOptimizer

etl_opt = ETLOptimizer()

# Optimize ETL pipeline
result = etl_opt.optimize(
    pipeline="sales_etl",
    strategies=[
        "parallel_extraction",
        "incremental_loading",
        "bulk_insert",
    ],
)

print(f"Original duration: {result.original_minutes:.1f}min")
print(f"Optimized duration: {result.optimized_minutes:.1f}min")
print(f"Resource savings: {result.resource_savings:.1%}")
```

## Security Considerations

### Data Security

```python
from data_warehousing import WarehouseSecurity

security = WarehouseSecurity()

# Encrypt data at rest
security.encrypt_at_rest(
    tables=["fact_sales", "dim_customer"],
    algorithm="aes-256",
    key_management="hsm",
)

# Column-level security
security.column_security(
    table="dim_customer",
    columns=["email", "phone", "address"],
    access_levels={
        "analyst": "masked",
        "manager": "full",
        "admin": "full",
    },
)
```

### Audit Logging

```python
from data_warehousing import AuditLogger

audit = AuditLogger()

# Log data access
audit.log(
    user="analyst@company.com",
    action="query",
    table="fact_sales",
    query="SELECT * FROM fact_sales WHERE date >= '2024-01-01'",
    rows_accessed=15000,
    timestamp=datetime.now(),
)
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Slow ETL | Large data volume | Use CDC, incremental loading |
| Query timeout | Missing indexes | Add indexes, partition tables |
| Data quality issues | Source problems | Add validation rules |
| Storage growth | No retention policy | Implement partition retention |
| Sync failures | API limits | Add retry logic, rate limiting |

### Debug Mode

```python
from data_warehousing import enable_debug

enable_debug(
    components=["etl", "schema", "quality"],
    log_level="DEBUG",
)

# Debug ETL pipeline
debug_session = debug.trace_pipeline("sales_etl")
print(f"Debug report: {debug_session.report_url}")
```

## API Reference

### REST Endpoints

```
GET    /api/v1/warehouse/schemas            List schemas
GET    /api/v1/warehouse/tables             List tables
GET    /api/v1/warehouse/tables/{name}      Get table info
POST   /api/v1/warehouse/etl/run            Run ETL job
GET    /api/v1/warehouse/etl/jobs           List ETL jobs
GET    /api/v1/warehouse/quality/checks     Run quality checks
GET    /api/v1/warehouse/lineage/{table}    Get table lineage
```

### Data Models

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from uuid import UUID

@dataclass
class Table:
    table_id: UUID
    name: str
    schema: str
    type: str  # fact, dimension, staging
    row_count: int
    size_gb: float
    last_updated: datetime

@dataclass
class ETLJob:
    job_id: UUID
    name: str
    source: str
    target: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime]
    rows_processed: int

@dataclass
class DataQualityResult:
    check_id: UUID
    table: str
    rule: str
    passed: bool
    failed_count: int
    total_count: int
    checked_at: datetime
```

## Deployment Guide

### Snowflake Deployment

```sql
-- Create warehouse
CREATE WAREHOUSE sales_wh
  WITH
    WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE;

-- Create database
CREATE DATABASE sales_dwh;

-- Create schema
CREATE SCHEMA sales_dwh.raw;
CREATE SCHEMA sales_dwh.integration;
CREATE SCHEMA sales_dwh.presentation;
```

## Monitoring & Observability

### Key Metrics

```python
from data_warehousing import Metrics

metrics = Metrics()

# Track ETL performance
metrics.histogram("etl.duration_minutes", duration, tags={"pipeline": "sales"})
metrics.counter("etl.rows_processed", tags={"pipeline": "sales"})

# Track query performance
metrics.histogram("warehouse.query_ms", query_time, tags={"table": "fact_sales"})
metrics.gauge("warehouse.storage_gb", storage, tags={"database": "sales_dwh"})
```

## Testing Strategy

### Unit Tests

```python
import pytest
from data_warehousing import ETLProcessor

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

- **2.0.0**: Added CDC support, advanced partitioning, data quality automation
- **1.5.0**: Added schema design tools, ETL optimization
- **1.0.0**: Initial release with basic warehousing

## Glossary

| Term | Definition |
|------|------------|
| **CDC** | Change Data Capture |
| **ETL** | Extract, Transform, Load |
| **Star Schema** | Dimensional modeling pattern |
| **Fact Table** | Transaction/measurement table |
| **Dimension Table** | Descriptive attribute table |
| **SCD** | Slowly Changing Dimension |

## Changelog

### Version 2.0.0
- CDC-based extraction
- Advanced partitioning strategies
- Data quality automation
- Enhanced security features

### Version 1.5.0
- Schema design tools
- ETL optimization
- Basic quality checks

### Version 1.0.0
- Initial release
- Basic warehousing
- Simple ETL

## Contributing Guidelines

1. Test with production-like data volumes
2. Validate schema designs
3. Benchmark query performance
4. Document data lineage

## Data Lineage Tracking

### Column-Level Lineage

```python
from data_warehousing import LineageTracker

tracker = LineageTracker()

# Track column lineage
lineage = tracker.get_column_lineage(
    table="fact_sales",
    column="revenue",
)

print(f"Column Lineage for fact_sales.revenue:")
for step in lineage.steps:
    print(f"  Source: {step.source_table}.{step.source_column}")
    print(f"  Transformation: {step.transformation}")
    print(f"  Confidence: {step.confidence:.1%}")
```

### Impact Analysis

```python
from data_warehousing import ImpactAnalyzer

analyzer = ImpactAnalyzer()

# Analyze impact of schema change
impact = analyzer.analyze_impact(
    change_type="column_rename",
    table="dim_product",
    column="old_name",
    new_column="new_name",
)

print(f"Impact Analysis:")
print(f"  Affected Tables: {len(impact.affected_tables)}")
print(f"  Affected ETL Jobs: {len(impact.affected_jobs)}")
print(f"  Affected Reports: {len(impact.affected_reports)}")
print(f"  Risk Level: {impact.risk_level}")
```

### Data Quality Rules Engine

```python
from data_warehousing import QualityEngine

dq_engine = QualityEngine()

# Define and run quality rules
rules = dq_engine.configure_rules(
    table="fact_sales",
    rules=[
        {"column": "revenue", "rule": "not_null", "severity": "critical"},
        {"column": "quantity", "rule": "positive", "severity": "warning"},
        {"column": "date", "rule": "not_future", "severity": "critical"},
        {"column": "product_id", "rule": "foreign_key", "references": "dim_product", "severity": "critical"},
    ],
)

results = dq_engine.run_rules("fact_sales")
print(f"Quality Score: {results.score:.1%}")
print(f"Critical Failures: {results.critical_failures}")
print(f"Warnings: {results.warnings}")
```

## Data Mart Management

### Data Mart Creation

```python
from data_warehousing import DataMartManager

mart_mgr = DataMartManager()

# Create departmental data mart
mart = mart_mgr.create(
    name="sales_mart",
    source_warehouse="enterprise_dwh",
    tables=[
        {"name": "fact_sales", "refresh": "daily"},
        {"name": "dim_customer", "refresh": "daily"},
        {"name": "dim_product", "refresh": "weekly"},
        {"name": "dim_date", "refresh": "monthly"},
    ],
    access_group="sales_analysts",
)

print(f"Data Mart Created:")
print(f"  Name: {mart.name}")
print(f"  Tables: {mart.table_count}")
print(f"  Size: {mart.size_gb:.1f} GB")
print(f"  Access Group: {mart.access_group}")
```

### Materialized View Management

```python
from data_warehousing import MaterializedViewManager

mv_mgr = MaterializedViewManager()

# Create materialized view
mv = mv_mgr.create(
    name="mv_daily_sales_summary",
    query="""
    SELECT 
        date_key,
        product_category,
        region,
        SUM(revenue) as total_revenue,
        SUM(quantity) as total_quantity,
        COUNT(DISTINCT customer_key) as unique_customers
    FROM fact_sales
    JOIN dim_product USING (product_key)
    JOIN dim_date USING (date_key)
    GROUP BY 1, 2, 3
    """,
    refresh_schedule="0 6 * * *",
    storage_bytes=52428800,
)

print(f"Materialized View: {mv.name}")
print(f"  Refresh: {mv.refresh_schedule}")
print(f"  Size: {mv.size_mb:.1f} MB")
print(f"  Last Refresh: {mv.last_refresh}")
```

## Slowly Changing Dimensions

### SCD Type 2 Implementation

```python
from data_warehousing import SCDManager

scd = SCDManager()

# Implement SCD Type 2 for customer dimension
result = scd.apply_scd_type2(
    target_table="dim_customer",
    source_table="stg_customers",
    natural_key="customer_id",
    tracked_columns=["name", "email", "segment", "region"],
    effective_date_column="valid_from",
    expiry_date_column="valid_to",
    current_flag_column="is_current",
)

print(f"SCD Type 2 Applied:")
print(f"  New Records: {result.new_count}")
print(f"  Updated Records: {result.updated_count}")
print(f"  Expired Records: {result.expired_count}")
print(f"  Unchanged Records: {result.unchanged_count}")
```

### SCD Type 1 Implementation

```python
from data_warehousing import SCDManager

scd = SCDManager()

# Implement SCD Type 1 (overwrite)
result = scd.apply_scd_type1(
    target_table="dim_product",
    source_table="stg_products",
    natural_key="product_id",
    update_columns=["price", "category", "status"],
)

print(f"SCD Type 1 Applied:")
print(f"  Updated: {result.updated_count}")
print(f"  Unchanged: {result.unchanged_count}")
```

## Data Warehouse Testing

### Data Quality Test Suite

```python
from data_warehousing import DataQualityTestSuite

suite = DataQualityTestSuite()

# Define test suite
suite.add_test(
    name="fact_sales_not_null",
    table="fact_sales",
    column="revenue",
    test_type="not_null",
    threshold=0.99,
)

suite.add_test(
    name="fact_sales_positive",
    table="fact_sales",
    column="revenue",
    test_type="greater_than",
    value=0,
    threshold=0.99,
)

suite.add_test(
    name="dim_product_foreign_key",
    table="fact_sales",
    column="product_key",
    test_type="foreign_key",
    references="dim_product(product_key)",
    threshold=1.0,
)

# Run tests
results = suite.run()
print(f"Test Results: {results.passed}/{results.total} passed")
print(f"Pass Rate: {results.pass_rate:.1%}")
```

## Partition Management

### Automated Partition Maintenance

```python
from data_warehousing import PartitionManager

pm = PartitionManager()

# Manage partitions for fact table
result = pm.manage(
    table="fact_sales",
    partition_column="date_key",
    strategy="range",
    partition_interval="monthly",
    retention_months=36,
    archive_after_months=12,
)

print(f"Partition Management:")
print(f"  Active Partitions: {result.active_count}")
print(f"  Archived: {result.archived_count}")
print(f"  Dropped: {result.dropped_count}")
print(f"  Storage Freed: {result.storage_freed_gb:.1f} GB")
```

## License

MIT License - Copyright (c) 2024 Awesome Grok Skills