---
name: Data Architecture Agent
version: 3.0.0
description: "Expert data architect that designs scalable data systems, models data across domains, builds integration pipelines, manages MDM, enforces governance, and ensures data quality"
author: MiMoCode
tags:
  - data-architecture
  - data-modeling
  - data-integration
  - master-data-management
  - data-governance
  - data-quality
  - data-lineage
  - schema-registry
  - data-partitioning
  - data-masking
  - cost-tracking
  - data-migration
category: agents
difficulty: advanced
time_estimate: "10-14 hours"
dependencies:
  - python
  - data-modeling
  - database-design
personality: "data-architect"
use_cases:
  - "Design relational, document, graph, and columnar data models"
  - "Build ETL, ELT, CDC, and streaming integration pipelines"
  - "Implement master data management with golden record creation"
  - "Create data catalogs with full-text metadata search"
  - "Monitor data quality with configurable rules and dashboards"
  - "Track table-level and column-level data lineage"
  - "Enforce governance policies with audit logging and compliance"
  - "Register and evolve schemas with compatibility checking"
  - "Partition data across hash, range, and time-interval strategies"
  - "Mask PII with hash, tokenize, partial, and full-redact strategies"
  - "Model dependencies between data assets with topological sort"
  - "Manage data retention with automated lifecycle actions"
  - "Track infrastructure costs with budget management"
  - "Plan and execute data migrations between systems"
---

# Data Architecture Agent

## Agent Identity

You are an expert data architect agent. You design and implement scalable, compliant, and maintainable data systems. You think in terms of data domains, pipelines, quality dimensions, and governance frameworks. You always consider the full lifecycle of data from ingestion through archival.

### Core Principles

1. **Domain-Driven Design** - Organize data around business domains, not applications
2. **Data as a Product** - Treat every dataset with ownership, SLAs, and quality guarantees
3. **Governance by Default** - Every data asset has classification, access control, and retention
4. **Quality First** - Validate data at ingestion, transformation, and serving layers
5. **Lineage Always** - Track every column from source to destination
6. **Cost Awareness** - Optimize storage, compute, and transfer costs continuously
7. **Evolution Safe** - Schema changes must be backward-compatible by default

## Capabilities

### 1. Data Modeling

Design conceptual, logical, and physical data models across multiple storage types.

```python
from agents.data_architecture.agent import (
    DataArchitectureAgent, Config, ModelType, DataType,
    StorageType, DataDomain, DataField
)

agent = DataArchitectureAgent(Config())
agent.initialize()

# Create a logical model
agent.create_model(
    model_id="model_ecommerce",
    name="E-commerce Domain",
    model_type=ModelType.LOGICAL,
    description="Core e-commerce data model",
    owner="data_platform_team",
    tags=["ecommerce", "production"]
)

# Create a table with PII-flagged fields
fields = [
    DataField("f1", "customer_id", DataType.UUID,
              nullable=False, primary_key=True),
    DataField("f2", "full_name", DataType.STRING,
              max_length=255, pii_flag=True, classification="pii"),
    DataField("f3", "email", DataType.STRING,
              max_length=255, pii_flag=True, classification="pii"),
    DataField("f4", "lifetime_value", DataType.DECIMAL,
              precision=12, scale=2),
    DataField("f5", "created_at", DataType.TIMESTAMP),
]

agent.create_table(
    table_id="tbl_customers",
    name="customers",
    fields=fields,
    storage_type=StorageType.RELATIONAL_DB,
    domain=DataDomain.CUSTOMER,
    owner="data_platform_team"
)
```

### 2. Integration Pipelines

Build and monitor data integration pipelines across multiple patterns.

```python
from agents.data_architecture.agent import IntegrationPattern

# Create an ETL pipeline
agent.create_pipeline(
    pipeline_id="pipe_orders_etl",
    name="Orders ETL",
    source="transactional_db",
    destination="analytics_warehouse",
    pattern=IntegrationPattern.ETL,
    schedule="0 2 * * *"
)

# Create a CDC pipeline
agent.create_pipeline(
    pipeline_id="pipe_customers_cdc",
    name="Customers CDC",
    source="customer_db",
    destination="customer_cache",
    pattern=IntegrationPattern.CDC
)

# Run and monitor
result = agent.run_pipeline("pipe_orders_etl")
# {"pipeline_id": "pipe_orders_etl", "status": "success",
#  "records_processed": 45230, "duration_seconds": 127.3,
#  "bytes_transferred": 23456789}

# Get P95 latency metrics
stats = agent.get_pipeline_stats()
# {"pipe_orders_etl": {"total_runs": 30, "success_rate": 0.9667,
#   "p95_duration": 180.5, "throughput_records_per_sec": 312.4}}
```

### 3. Master Data Management

Create golden records, match duplicates, and merge with survivorship rules.

```python
# Create MDM records
r1 = agent.create_mdm_record("customer", {
    "name": "Acme Corp", "email": "info@acme.com", "domain": "acme.com"
}, source_id="crm_system")

r2 = agent.create_mdm_record("customer", {
    "name": "Acme Corporation", "email": "info@acme.com", "domain": "acme.com"
}, source_id="erp_system")

# Merge with highest-quality strategy
merged = agent.merge_mdm_records(
    r1["record_id"], r2["record_id"], strategy="highest_quality"
)
# {"merged_id": "xxx", "sources": ["crm_system", "erp_system"],
#  "strategy": "highest_quality"}
```

### 4. Data Quality Management

Define quality rules and monitor compliance with dashboards and trend analysis.

```python
from agents.data_architecture.agent import QualityRuleType

# Create quality rules
agent.create_quality_rule(
    rule_id="qr_email_not_null",
    name="Email Not Null",
    rule_type=QualityRuleType.NOT_NULL,
    table_id="tbl_customers",
    threshold=100.0,
    severity="critical"
)

agent.create_quality_rule(
    rule_id="qr_email_format",
    name="Email Format",
    rule_type=QualityRuleType.PATTERN_MATCH,
    table_id="tbl_customers",
    field_id="email",
    threshold=99.5,
    severity="warning"
)

# Run all checks
results = agent.run_quality_checks()
# {"total": 2, "passed": 1, "failed": 1}

# Get dashboard
dashboard = agent.get_quality_dashboard()
# {"total_rules": 2, "passing": 1, "failing": 1,
#  "pass_rate": 0.5, "by_type": {"NOT_NULL": {"passing": 1, "failing": 0}}}
```

### 5. Data Lineage

Track data flow at both table and column level.

```python
from agents.data_architecture.agent import LineageNodeType

# Add table-level lineage nodes
agent.add_lineage_node("src_orders", "Source: Orders DB", LineageNodeType.SOURCE)
agent.add_lineage_node("tfm_clean", "Transform: Clean & Dedup", LineageNodeType.TRANSFORMATION)
agent.add_lineage_node("tfm_agg", "Transform: Aggregate", LineageNodeType.AGGREGATION)
agent.add_lineage_node("dim_orders", "Dim: Orders", LineageNodeType.DESTINATION)

# Connect them
agent.add_lineage_edge("src_orders", "tfm_clean")
agent.add_lineage_edge("tfm_clean", "tfm_agg")
agent.add_lineage_edge("tfm_agg", "dim_orders")

# Impact analysis
impact = agent.get_lineage_impact("tfm_clean")
# {"node_id": "tfm_clean", "upstream_count": 1, "downstream_count": 2,
#  "upstream_nodes": ["src_orders"], "downstream_nodes": ["tfm_agg", "dim_orders"]}

# Column-level lineage
agent.add_column_lineage(
    "cl_001", "orders_db", "order_total",
    "dim_orders", "revenue",
    transformation="SUM(order_total) GROUP BY date"
)

upstream = agent._column_lineage.get_column_upstream("dim_orders", "revenue")
```

### 6. Schema Registry

Register schemas, check compatibility, and evolve safely.

```python
# Register initial schema
agent.register_schema("tbl_customers", {
    "fields": {"customer_id": "UUID", "name": "STRING", "email": "STRING"}
}, created_by="data_engineer")

# Check if adding a column is compatible
compat = agent.check_schema_compatibility("tbl_customers", {
    "fields": {"customer_id": "UUID", "name": "STRING",
               "email": "STRING", "phone": "STRING"}
})
# {"compatible": true, "added_fields": ["phone"],
#  "removed_fields": [], "modified_fields": []}

# Check if removing a column breaks compatibility
compat = agent.check_schema_compatibility("tbl_customers", {
    "fields": {"customer_id": "UUID", "email": "STRING"}
})
# {"compatible": false, "added_fields": [],
#  "removed_fields": ["name"], "modified_fields": []}
```

### 7. Data Partitioning

Partition tables using hash, range, or time-interval strategies.

```python
from agents.data_architecture.agent import PartitionStrategy

# Hash-based partitioning
agent.create_partition(
    config_id="part_customers",
    table_id="tbl_customers",
    strategy=PartitionStrategy.HASH,
    partition_count=16
)

# Time-interval partitioning
agent.create_partition(
    config_id="part_orders",
    table_id="tbl_orders",
    strategy=PartitionStrategy.TIME_INTERVAL,
    partition_count=30
)

# Compute which partition a key maps to
agent._partitioner.compute_partition("part_customers", "customer_123")
```

### 8. Data Masking

Protect PII with configurable masking strategies.

```python
from agents.data_architecture.agent import MaskingType

# Partial masking for names
agent.create_masking_rule(
    rule_id="mask_name",
    name="Mask Customer Name",
    table_id="tbl_customers",
    field_id="full_name",
    masking_type=MaskingType.PARTIAL
)

# Hash masking for emails
agent.create_masking_rule(
    rule_id="mask_email",
    name="Mask Email",
    table_id="tbl_customers",
    field_id="email",
    masking_type=MaskingType.HASH,
    salt="my_secret_salt"
)

# Apply masking
masked = agent.mask_data("tbl_customers", {
    "full_name": "John Doe",
    "email": "john@example.com"
})
# {"full_name": "Jo***oe", "email": "a1b2c3d4e5f6a7b8"}
```

### 9. Governance and Compliance

Define policies, log audit events, and run compliance checks.

```python
from agents.data_architecture.agent import GovernancePolicy

# Create policies
agent.create_governance_policy(
    rule_id="gov_classification",
    name="Data Classification Policy",
    policy_type=GovernancePolicy.DATA_CLASSIFICATION,
    enforcement_level="mandatory"
)

agent.create_governance_policy(
    rule_id="gov_access",
    name="Access Control Policy",
    policy_type=GovernancePolicy.ACCESS_CONTROL,
    enforcement_level="enforced"
)

# Log audit events
agent.log_audit("read", "table", "tbl_customers", "analyst_001",
                details="Quarterly revenue report access")

# Run compliance check
compliance = agent._governance.run_compliance_check("gov_classification")
# {"passed": true, "details": "Compliance check passed"}
```

### 10. Dependency Graph

Model relationships between data assets and analyze critical paths.

```python
from agents.data_architecture.agent import DependencyType

# Add dependency nodes
agent.add_dependency_node("dep_orders", "table", "tbl_orders", "Orders",
                          DependencyType.TABLE_DEPENDS_ON)
agent.add_dependency_node("dep_pipe", "pipeline", "pipe_orders", "Orders ETL",
                          DependencyType.PIPELINE_FEEDS)
agent.add_dependency_node("dep_rule", "quality_rule", "qr_orders", "Orders Quality",
                          DependencyType.QUALITY_RULE_CHECKS)

# Connect dependencies
agent.add_dependency_edge("dep_pipe", "dep_orders")
agent.add_dependency_edge("dep_rule", "dep_orders")

# Topological sort for execution order
order = agent.get_dependency_order()
# ["dep_pipe", "dep_rule", "dep_orders"]
```

### 11. Cost Tracking

Monitor infrastructure costs and manage budgets.

```python
from agents.data_architecture.agent import CostCategory

# Record costs
agent.record_cost(CostCategory.COMPUTE, 150.00, "Daily Spark cluster")
agent.record_cost(CostCategory.STORAGE, 75.50, "S3 storage")
agent.record_cost(CostCategory.NETWORK, 23.30, "Data transfer")

# Get cost report
report = agent.get_cost_report()
# {"total_cost": 248.80, "total_entries": 3,
#  "by_category": {"COMPUTE": 150.0, "STORAGE": 75.5, "NETWORK": 23.3}}

# Set budgets
agent._cost_tracker.set_budget(CostCategory.COMPUTE, 5000.00)
status = agent._cost_tracker.get_budget_status()
```

### 12. Data Migration Planning

Plan and track migrations between source and target systems.

```python
from agents.data_architecture.agent import MigrationStatus

# Create migration plan
agent.create_migration_plan(
    plan_id="mig_cloud",
    name="Migrate to Cloud Warehouse",
    source="on_prem_db",
    target="snowflake",
    tables=["tbl_customers", "tbl_orders", "tbl_products"],
    estimated_hours=48.0,
    owner="data_engineering_team"
)

# Start migration
agent._migration_planner.start_migration("mig_cloud")

# Complete migration
agent._migration_planner.complete_migration("mig_cloud", rows_migrated=5000000)

# Get stats
stats = agent.get_migration_stats()
# {"total_plans": 1, "by_status": {"COMPLETED": 1},
#  "total_rows_migrated": 5000000}
```

## Method Signatures

### DataArchitectureAgent

| Method | Parameters | Returns |
|--------|-----------|---------|
| `initialize()` | - | `Dict[str, Any]` |
| `shutdown()` | - | `Dict[str, Any]` |
| `create_model()` | model_id, name, model_type, description, owner, tags | `Dict[str, Any]` |
| `create_table()` | table_id, name, fields, storage_type, domain, owner | `Dict[str, Any]` |
| `add_field()` | table_id, field_id, name, data_type, nullable, primary_key, pii_flag | `Dict[str, Any]` |
| `create_pipeline()` | pipeline_id, name, source, destination, pattern, schedule | `Dict[str, Any]` |
| `run_pipeline()` | pipeline_id | `Dict[str, Any]` |
| `create_mdm_record()` | entity_type, attributes, source_id | `Dict[str, Any]` |
| `merge_mdm_records()` | record_id_1, record_id_2, strategy | `Dict[str, Any]` |
| `add_metadata()` | entity_type, entity_id, key, value | `Dict[str, Any]` |
| `search_catalog()` | query, entity_type | `List[Dict]` |
| `create_quality_rule()` | rule_id, name, rule_type, table_id, threshold, severity | `Dict[str, Any]` |
| `run_quality_checks()` | - | `Dict[str, Any]` |
| `get_quality_dashboard()` | - | `Dict[str, Any]` |
| `add_lineage_node()` | node_id, name, node_type | `Dict[str, Any]` |
| `add_lineage_edge()` | source, target, edge_type | `Dict[str, Any]` |
| `get_lineage_impact()` | node_id | `Dict[str, Any]` |
| `create_governance_policy()` | rule_id, name, policy_type, enforcement_level | `Dict[str, Any]` |
| `log_audit()` | event_type, entity_type, entity_id, user, details | `Dict[str, Any]` |
| `register_schema()` | table_id, schema, created_by | `Dict[str, Any]` |
| `check_schema_compatibility()` | table_id, schema | `Dict[str, Any]` |
| `create_partition()` | config_id, table_id, strategy, partition_count | `Dict[str, Any]` |
| `create_masking_rule()` | rule_id, name, table_id, field_id, masking_type | `Dict[str, Any]` |
| `mask_data()` | table_id, record | `Dict[str, Any]` |
| `add_dependency_node()` | node_id, entity_type, entity_id, name, dependency_type | `Dict[str, Any]` |
| `add_dependency_edge()` | source, target | `Dict[str, Any]` |
| `get_dependency_order()` | - | `List[str]` |
| `create_retention_rule()` | rule_id, table_id, action, retention_days | `Dict[str, Any]` |
| `record_cost()` | category, amount, description | `Dict[str, Any]` |
| `get_cost_report()` | - | `Dict[str, Any]` |
| `create_migration_plan()` | plan_id, name, source, target, tables, estimated_hours | `Dict[str, Any]` |
| `add_column_lineage()` | lineage_id, source_table, source_column, target_table, target_column, transformation | `Dict[str, Any]` |
| `get_status()` | - | `Dict[str, Any]` |
| `get_full_report()` | - | `Dict[str, Any]` |

## Data Models

### DataField

| Field | Type | Description |
|-------|------|-------------|
| `field_id` | `str` | Unique identifier |
| `name` | `str` | Column name |
| `data_type` | `DataType` | Data type enum |
| `nullable` | `bool` | Allow null values |
| `primary_key` | `bool` | Primary key flag |
| `foreign_key` | `Optional[str]` | Foreign key reference |
| `pii_flag` | `bool` | PII indicator |
| `classification` | `str` | Data classification level |
| `masking_type` | `Optional[MaskingType]` | Masking strategy |
| `max_length` | `Optional[int]` | Max string length |
| `precision` | `Optional[int]` | Decimal precision |
| `scale` | `Optional[int]` | Decimal scale |

### DataTable

| Field | Type | Description |
|-------|------|-------------|
| `table_id` | `str` | Unique identifier |
| `name` | `str` | Table name |
| `schema_name` | `str` | Schema/database name |
| `fields` | `List[DataField]` | Column definitions |
| `storage_type` | `StorageType` | Storage backend |
| `domain` | `DataDomain` | Business domain |
| `owner` | `str` | Data owner |
| `partition_config` | `Optional[PartitionConfig]` | Partitioning setup |
| `retention_days` | `Optional[int]` | Data retention period |

### QualityRule

| Field | Type | Description |
|-------|------|-------------|
| `rule_id` | `str` | Unique identifier |
| `name` | `str` | Human-readable name |
| `rule_type` | `QualityRuleType` | Quality dimension |
| `table_id` | `str` | Target table |
| `field_id` | `Optional[str]` | Target column |
| `threshold` | `float` | Minimum pass threshold |
| `severity` | `str` | critical/warning/info |
| `owner` | `str` | Rule owner |

## Checklists

### New Data Model

- [ ] Define conceptual model with business entities
- [ ] Create logical model with attributes and relationships
- [ ] Design physical model with storage-specific types
- [ ] Identify PII fields and set masking rules
- [ ] Create quality rules for key fields
- [ ] Register schema in schema registry
- [ ] Set up lineage tracking
- [ ] Define retention policies
- [ ] Assign data owner and classification

### New Pipeline

- [ ] Choose integration pattern (ETL, ELT, CDC, streaming)
- [ ] Define source and destination
- [ ] Configure schedule and retry policy
- [ ] Set up quality checks on output
- [ ] Add lineage nodes and edges
- [ ] Configure alerting on failure
- [ ] Set up cost tracking
- [ ] Document in data catalog

### Schema Evolution

- [ ] Check backward compatibility
- [ ] Check forward compatibility
- [ ] Document breaking changes
- [ ] Update affected lineage
- [ ] Notify downstream consumers
- [ ] Register new schema version
- [ ] Update data catalog metadata

### Data Masking

- [ ] Identify all PII fields
- [ ] Choose appropriate masking strategy per field
- [ ] Configure salt for hash masking
- [ ] Test masking output format
- [ ] Verify masking rules cover all PII
- [ ] Document masking rules in catalog
- [ ] Set up compliance checks

## Troubleshooting

### Problem: Schema compatibility check fails after adding column

**Cause:** Removing or renaming fields breaks backward compatibility.

**Solution:** Add columns instead of removing. Use `SchemaEvolution.ADD_COLUMN` and register the new schema. For breaking changes, create a migration plan with rollback.

### Problem: Pipeline metrics show 0% success rate

**Cause:** Pipeline may be paused or not properly initialized.

**Solution:** Check `pipeline.is_active` status. Resume paused pipelines with `IntegrationManager.resume_pipeline()`. Verify source/destination connectivity.

### Problem: MDM merge produces unexpected golden record

**Cause:** Merge strategy may not match business requirements.

**Solution:** Use `strategy="highest_quality"` for quality-first merges. Set survivorship rules per entity/field for fine-grained control. Review `quality_score` on source records.

### Problem: Column lineage trace returns incomplete path

**Cause:** Missing intermediate lineage entries.

**Solution:** Ensure every transformation step has a lineage node and edges. Use `ColumnLineageTracker.add_column_lineage()` for each column mapping.

### Problem: Cost tracking shows zero totals

**Cause:** No cost entries have been recorded yet.

**Solution:** Use `CostTracker.record_cost()` to log costs. Set budgets with `set_budget()` for threshold monitoring.

### Problem: Dependency graph has cycles

**Cause:** Circular dependencies between data assets.

**Solution:** Run `DependencyGraphBuilder.topological_sort()`. If the result is shorter than the total node count, there are cycles. Break cycles by redesigning data flow or removing redundant dependencies.

### Problem: Quality checks always pass

**Cause:** Thresholds may be too low or check simulation returns high values.

**Solution:** Review `QUALITY_THRESHOLDS` defaults. Set explicit thresholds on rules. In production, connect to real data sources instead of simulated checks.

## FAQ

**Q: Does this generate real DDL?**
A: It provides design specs and schema snapshots. Extend with DDL generation for target databases (PostgreSQL, Snowflake, BigQuery).

**Q: Can I import existing models?**
A: Extend `SchemaRegistry.register_schema()` to accept JSON/YAML/DBML imports. Use `DataCatalog.add_metadata()` for cataloging existing assets.

**Q: How does column-level lineage differ from table-level?**
A: Table-level tracks which tables flow into which. Column-level tracks which specific columns map through transformations, enabling impact analysis at the field level.

**Q: Can I customize masking strategies?**
A: Yes. Extend `DataMaskingEngine.mask_value()` with new `MaskingType` cases. The engine supports pluggable strategies.

**Q: How do I connect to real data sources?**
A: Extend `IntegrationManager` with concrete connectors (JDBC, REST, Kafka). The current implementation provides the orchestration framework.

**Q: Is this thread-safe?**
A: Yes. All managers use `threading.Lock()` for concurrent access. The agent orchestrator delegates to manager-level locks.

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md).

## License

MIT License - see [LICENSE](../../LICENSE).

---

*Data Architecture Agent v3.0.0 - Part of the Awesome Grok Skills collection.*

*Last updated: 2026-07-06*
