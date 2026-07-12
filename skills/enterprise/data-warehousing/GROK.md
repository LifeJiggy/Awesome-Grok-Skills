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