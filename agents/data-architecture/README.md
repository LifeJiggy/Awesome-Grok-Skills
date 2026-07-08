# Data Architecture Agent

> Comprehensive data architecture design and management platform covering data modeling, integration pipelines, master data management, data catalog, quality monitoring, lineage tracking, governance, schema registry, partitioning, masking, dependency analysis, retention management, cost tracking, migration planning, and column-level lineage.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](../../LICENSE)
[![Version](https://img.shields.io/badge/version-3.0.0-orange.svg)](CHANGELOG.md)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Data Modeling](#data-modeling)
  - [Integration Pipelines](#integration-pipelines)
  - [Master Data Management](#master-data-management)
  - [Data Catalog](#data-catalog)
  - [Data Quality](#data-quality)
  - [Data Lineage](#data-lineage)
  - [Schema Registry](#schema-registry)
  - [Data Partitioning](#data-partitioning)
  - [Data Masking](#data-masking)
  - [Governance](#governance)
  - [Dependency Graph](#dependency-graph)
  - [Data Retention](#data-retention)
  - [Cost Tracking](#cost-tracking)
  - [Data Migration](#data-migration)
  - [Column Lineage](#column-lineage)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Data Types](#data-types)
- [Enums Reference](#enums-reference)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Data Architecture Agent is a comprehensive, thread-safe Python framework for designing, implementing, and managing enterprise data systems. It provides 14 interconnected subsystems that cover the full data lifecycle from ingestion through archival.

### What It Does

- **Design** relational, document, graph, and columnar data models
- **Build** ETL, ELT, CDC, streaming, and batch integration pipelines
- **Manage** master data with golden record creation, matching, and merging
- **Catalog** data assets with full-text metadata search and auto-discovery
- **Monitor** data quality with configurable rules, dashboards, and trend analysis
- **Track** table-level and column-level data lineage with impact analysis
- **Enforce** governance policies with audit logging and compliance checking
- **Register** schemas with version control and compatibility checking
- **Partition** data across hash, range, time-interval, and list strategies
- **Mask** PII with hash, tokenize, partial, and full-redact strategies
- **Model** dependencies between data assets with topological sort
- **Manage** data retention with automated lifecycle actions
- **Track** infrastructure costs with budget management
- **Plan** data migrations between source and target systems

### Key Design Principles

1. **Domain-Driven** - Organize data around business domains, not applications
2. **Thread-Safe** - All managers use locks for concurrent access
3. **Zero Dependencies** - Pure Python, no external packages required
4. **Extensible** - Pluggable strategies for masking, partitioning, and integration
5. **Observable** - Built-in metrics, dashboards, and audit logging

---

## Features

| Category | Feature | Description |
|----------|---------|-------------|
| **Modeling** | Multi-type models | Conceptual, logical, physical, semantic |
| **Modeling** | PII detection | Auto-flag fields with masking types |
| **Modeling** | Table cloning | Deep-copy tables with new IDs |
| **Pipelines** | 8 patterns | ETL, ELT, CDC, API, file, streaming, event, batch |
| **Pipelines** | Lifecycle mgmt | Pause, resume, delete with state tracking |
| **Pipelines** | P95 metrics | Latency percentiles and throughput |
| **MDM** | 4 merge strategies | r1_priority, r2_priority, latest_wins, highest_quality |
| **MDM** | Fuzzy matching | Jaccard similarity-based duplicate detection |
| **MDM** | Survivorship rules | Per-entity, per-field value transforms |
| **Catalog** | Full-text search | Inverted index with AND semantics |
| **Catalog** | Auto-discovery | Scan tables for missing metadata |
| **Quality** | 9 rule types | NOT_NULL, UNIQUE, RANGE, PATTERN, REFERENTIAL, etc. |
| **Quality** | Score history | Trend analysis over time |
| **Quality** | Severity levels | critical, warning, info |
| **Lineage** | Table + column | Both table-level and column-level tracking |
| **Lineage** | Impact analysis | Full upstream/downstream dependency mapping |
| **Lineage** | Shortest path | BFS pathfinding between nodes |
| **Schema** | Version control | Full version history per table |
| **Schema** | Compatibility | Backward/forward compatibility checking |
| **Schema** | Evolution | Safe schema changes with breaking-change flags |
| **Partitioning** | 6 strategies | HASH, RANGE, TIME_INTERVAL, LIST, GEO, DIRECTORY |
| **Masking** | 8 types | FULL_REDACT, PARTIAL, HASH, TOKENIZE, SHUFFLE, etc. |
| **Governance** | 3 enforcement | advisory, mandatory, enforced |
| **Governance** | Compliance | Per-policy compliance checking |
| **Dependencies** | Topological sort | DAG ordering for execution |
| **Dependencies** | Critical path | Longest path through dependency graph |
| **Retention** | 6 actions | DELETE, ARCHIVE, COMPRESS, COLD, KEEP, ANONYMIZE |
| **Costs** | 8 categories | COMPUTE, STORAGE, NETWORK, QUERY, etc. |
| **Costs** | Budget mgmt | Per-category budgets with utilization tracking |
| **Migration** | State machine | PLANNED -> IN_PROGRESS -> COMPLETED/FAILED/ROLLED_BACK |
| **Column Lineage** | Dual index | Upstream and downstream column tracing |
| **Column Lineage** | Full path | Multi-hop transformation tracing |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   DataArchitectureAgent (Orchestrator)                  │
│                                                                         │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐              │
│  │  Model    │ │ Integration│ │    MDM    │ │  Catalog  │              │
│  │  Manager  │ │  Manager   │ │  Manager  │ │           │              │
│  └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘              │
│        │              │              │              │                    │
│  ┌─────┴─────┐ ┌─────┴─────┐ ┌─────┴─────┐ ┌─────┴─────┐              │
│  │  Quality  │ │  Lineage  │ │ Governance│ │  Schema   │              │
│  │  Manager  │ │  (T+C)    │ │  Manager  │ │  Registry │              │
│  └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘              │
│        │              │              │              │                    │
│  ┌─────┴─────┐ ┌─────┴─────┐ ┌─────┴─────┐ ┌─────┴─────┐              │
│  │ Partitioner│ │  Masking  │ │Dependency │ │ Retention │              │
│  │           │ │  Engine   │ │  Graph    │ │  Manager  │              │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘              │
│                                                                         │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐                             │
│  │   Cost    │ │ Migration │ │ Column    │                             │
│  │  Tracker  │ │  Planner  │ │ Lineage   │                             │
│  └───────────┘ └───────────┘ └───────────┘                             │
└─────────────────────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed component diagrams, data flows, design patterns, and thread safety analysis.

---

## Quick Start

```python
from agents.data_architecture.agent import (
    DataArchitectureAgent, Config, ModelType, DataType,
    StorageType, DataDomain, DataField, IntegrationPattern
)

# Initialize the agent
agent = DataArchitectureAgent(Config())
agent.initialize()

# Create a data model
agent.create_model("model_001", "E-commerce", ModelType.LOGICAL)

# Add a table with PII fields
fields = [
    DataField("f1", "id", DataType.UUID, nullable=False, primary_key=True),
    DataField("f2", "name", DataType.STRING, pii_flag=True),
    DataField("f3", "email", DataType.STRING, pii_flag=True),
]
agent.create_table("tbl_customers", "customers", fields, domain=DataDomain.CUSTOMER)

# Create a pipeline
agent.create_pipeline("pipe_001", "ETL", "source_db", "warehouse",
                      IntegrationPattern.ETL)

# Run pipeline and check quality
agent.run_pipeline("pipe_001")
agent.create_quality_rule("qr_001", "Not Null", QualityRuleType.NOT_NULL,
                          "tbl_customers", 100.0)
results = agent.run_quality_checks()

# Get full report
report = agent.get_full_report()
print(report)
```

---

## Installation

```bash
git clone https://github.com/LifeJiggy/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills
```

No external dependencies required. Pure Python 3.8+.

---

## Usage

### Data Modeling

```python
from agents.data_architecture.agent import (
    DataArchitectureAgent, Config, ModelType, DataType,
    StorageType, DataDomain, DataField
)

agent = DataArchitectureAgent(Config())
agent.initialize()

# Create models
agent.create_model("model_001", "Customer Domain", ModelType.LOGICAL,
                   description="Core customer data model")

# Create tables
fields = [
    DataField("f1", "customer_id", DataType.UUID, nullable=False, primary_key=True),
    DataField("f2", "full_name", DataType.STRING, max_length=255),
    DataField("f3", "email", DataType.STRING, max_length=255),
    DataField("f4", "created_at", DataType.TIMESTAMP),
    DataField("f5", "lifetime_value", DataType.DECIMAL, precision=12, scale=2),
]

agent.create_table("tbl_customers", "customers", fields,
                   storage_type=StorageType.RELATIONAL_DB,
                   domain=DataDomain.CUSTOMER)

# Clone tables
cloned = agent._model_manager.clone_table("tbl_customers", "tbl_customers_v2",
                                           "customers_v2")

# Search tables
results = agent._model_manager.search_tables("customer")

# Get PII fields
pii_fields = agent._model_manager.get_pii_fields()

# Get model summary
summary = agent.get_model_summary()
```

### Integration Pipelines

```python
from agents.data_architecture.agent import IntegrationPattern

# Create pipelines
agent.create_pipeline("pipe_001", "ETL Customers", "source_db", "data_warehouse",
                      IntegrationPattern.ETL, schedule="0 2 * * *")

agent.create_pipeline("pipe_002", "CDC Events", "event_db", "cache",
                      IntegrationPattern.CDC)

# Run pipelines
result = agent.run_pipeline("pipe_001")
# {"status": "success", "records_processed": 45230, ...}

# Pause/resume
agent._integration_manager.pause_pipeline("pipe_001")
agent._integration_manager.resume_pipeline("pipe_001")

# Get metrics (including P95)
stats = agent.get_pipeline_stats()

# Get alerts
alerts = agent._integration_manager.get_alerts()
```

### Master Data Management

```python
# Create records
r1 = agent.create_mdm_record("customer", {
    "name": "Acme Corp", "email": "info@acme.com"
}, source_id="crm")

r2 = agent.create_mdm_record("customer", {
    "name": "Acme Corporation", "email": "info@acme.com"
}, source_id="erp")

# Merge records
merged = agent.merge_mdm_records(r1["record_id"], r2["record_id"],
                                 strategy="highest_quality")

# Fuzzy matching
fuzzy = agent._mdm_manager.fuzzy_match("customer", "name", threshold=0.5)

# Find duplicates
dupes = agent._mdm_manager.get_duplicates("customer", "email")

# Survivorship rules
agent._mdm_manager.set_survivorship_rule("customer", "name", "uppercase")
agent._mdm_manager.apply_survivorship(r1["record_id"])

# Stats
stats = agent.get_mdm_stats()
```

### Data Catalog

```python
# Add metadata
agent.add_metadata("table", "tbl_customers", "description", "Core customer data")
agent.add_metadata("table", "tbl_customers", "owner", "data_team")
agent.add_metadata("field", "email", "pii", True)

# Search
results = agent.search_catalog("customer")
results = agent.search_catalog("email", entity_type="field")

# Auto-discover
discovered = agent._catalog.auto_discover()

# Get entity metadata
meta = agent._catalog.get_entity_metadata("table", "tbl_customers")

# Stats
stats = agent.get_catalog_stats()
```

### Data Quality

```python
from agents.data_architecture.agent import QualityRuleType

# Create rules
agent.create_quality_rule("qr_001", "Email Not Null", QualityRuleType.NOT_NULL,
                          "tbl_customers", threshold=100.0, severity="critical")

agent.create_quality_rule("qr_002", "Email Format", QualityRuleType.PATTERN_MATCH,
                          "tbl_customers", field_id="email", threshold=99.5)

# Run checks
results = agent.run_quality_checks()
# {"total": 2, "passed": 1, "failed": 1}

# Dashboard
dashboard = agent.get_quality_dashboard()

# Score history
history = agent._quality_manager.get_score_history(limit=30)

# Filter by severity
critical = agent._quality_manager.get_rules_by_severity("critical")
```

### Data Lineage

```python
from agents.data_architecture.agent import LineageNodeType

# Add table-level lineage
agent.add_lineage_node("src_orders", "Source: Orders", LineageNodeType.SOURCE)
agent.add_lineage_node("tfm_clean", "Clean", LineageNodeType.TRANSFORMATION)
agent.add_lineage_node("dim_orders", "Dim: Orders", LineageNodeType.DESTINATION)

agent.add_lineage_edge("src_orders", "tfm_clean")
agent.add_lineage_edge("tfm_clean", "dim_orders")

# Impact analysis
impact = agent.get_lineage_impact("tfm_clean")

# Shortest path
path = agent._lineage.get_shortest_path("src_orders", "dim_orders")

# Stats
stats = agent.get_lineage_stats()
```

### Schema Registry

```python
# Register schemas
agent.register_schema("tbl_customers", {
    "fields": {"id": "UUID", "name": "STRING", "email": "STRING"}
}, created_by="engineer")

# Check compatibility
compat = agent.check_schema_compatibility("tbl_customers", {
    "fields": {"id": "UUID", "name": "STRING", "email": "STRING", "phone": "STRING"}
})
# {"compatible": true, "added_fields": ["phone"]}

# Schema diff
diff = agent._schema_registry.get_schema_diff("tbl_customers", 1, 2)

# Version history
versions = agent._schema_registry.get_all_versions("tbl_customers")
```

### Data Partitioning

```python
from agents.data_architecture.agent import PartitionStrategy

# Hash partitioning
agent.create_partition("part_001", "tbl_customers", PartitionStrategy.HASH, 16)

# Time-interval partitioning
agent.create_partition("part_002", "tbl_orders", PartitionStrategy.TIME_INTERVAL, 30)

# Initialize partitions
agent._partitioner.init_partitions("part_001")

# Compute partition
idx = agent._partitioner.compute_partition("part_001", "customer_123")

# Stats
stats = agent._partitioner.get_partition_stats("tbl_customers")
```

### Data Masking

```python
from agents.data_architecture.agent import MaskingType

# Create masking rules
agent.create_masking_rule("mask_001", "Mask Name", "tbl_customers",
                          "f2", MaskingType.PARTIAL)

agent.create_masking_rule("mask_002", "Hash Email", "tbl_customers",
                          "f3", MaskingType.HASH, salt="secret")

# Apply masking
masked = agent.mask_data("tbl_customers", {
    "full_name": "John Doe", "email": "john@example.com"
})
# {"full_name": "Jo***oe", "email": "a1b2c3d4e5f6a7b8"}

# Stats
stats = agent.get_masking_stats()
```

### Governance

```python
from agents.data_architecture.agent import GovernancePolicy

# Create policies
agent.create_governance_policy("gov_001", "Data Classification",
                               GovernancePolicy.DATA_CLASSIFICATION,
                               enforcement_level="mandatory")

# Log audit events
agent.log_audit("read", "table", "tbl_customers", "analyst_001",
                details="Revenue report")

# Compliance checks
result = agent._governance.run_compliance_check("gov_001")

# Audit log with filters
log = agent._governance.get_audit_log(user="analyst_001", limit=50)

# Stats
stats = agent.get_governance_summary()
```

### Dependency Graph

```python
from agents.data_architecture.agent import DependencyType

# Add nodes
agent.add_dependency_node("dep_001", "table", "t1", "Orders",
                          DependencyType.TABLE_DEPENDS_ON)
agent.add_dependency_node("dep_002", "pipeline", "p1", "ETL",
                          DependencyType.PIPELINE_FEEDS)

# Add edges
agent.add_dependency_edge("dep_002", "dep_001")

# Topological sort
order = agent.get_dependency_order()

# Critical path
critical = agent._dependency_graph.get_critical_path()

# Stats
stats = agent.get_dependency_stats()
```

### Data Retention

```python
from agents.data_architecture.agent import RetentionAction

# Create retention rules
agent.create_retention_rule("ret_001", "tbl_customers",
                            RetentionAction.ARCHIVE, retention_days=730)

# Execute retention
result = agent._retention_manager.execute_retention("ret_001")

# Get due rules
due = agent._retention_manager.get_due_rules()

# Stats
stats = agent.get_retention_stats()
```

### Cost Tracking

```python
from agents.data_architecture.agent import CostCategory

# Record costs
agent.record_cost(CostCategory.COMPUTE, 150.00, "Daily Spark cluster")
agent.record_cost(CostCategory.STORAGE, 75.50, "S3 storage")

# Set budgets
agent._cost_tracker.set_budget(CostCategory.COMPUTE, 5000.00)

# Reports
report = agent.get_cost_report()
budget_status = agent._cost_tracker.get_budget_status()

# Cost by resource
by_resource = agent._cost_tracker.get_cost_by_resource()
```

### Data Migration

```python
from agents.data_architecture.agent import MigrationStatus

# Create plan
agent.create_migration_plan("mig_001", "Cloud Migration",
                            "on_prem_db", "snowflake",
                            ["tbl_customers", "tbl_orders"],
                            estimated_hours=48.0)

# Lifecycle
agent._migration_planner.start_migration("mig_001")
agent._migration_planner.complete_migration("mig_001", rows_migrated=5000000)

# Stats
stats = agent.get_migration_stats()
```

### Column Lineage

```python
# Add column-level lineage
agent.add_column_lineage("cl_001", "orders_db", "order_total",
                         "dim_orders", "revenue",
                         transformation="SUM() GROUP BY date")

# Trace upstream
upstream = agent._column_lineage.get_column_upstream("dim_orders", "revenue")

# Trace downstream
downstream = agent._column_lineage.get_column_downstream("orders_db", "order_total")

# Full path trace
path = agent._column_lineage.trace_full_path("orders_db", "order_total")

# Stats
stats = agent.get_column_lineage_stats()
```

---

## API Reference

### DataArchitectureAgent

| Method | Returns | Description |
|--------|---------|-------------|
| `initialize()` | `Dict` | Initialize agent with config |
| `shutdown()` | `Dict` | Shutdown agent |
| `create_model(...)` | `Dict` | Create data model |
| `create_table(...)` | `Dict` | Create data table |
| `add_field(...)` | `Dict` | Add field to table |
| `create_pipeline(...)` | `Dict` | Create integration pipeline |
| `run_pipeline(id)` | `Dict` | Execute pipeline |
| `create_mdm_record(...)` | `Dict` | Create MDM golden record |
| `merge_mdm_records(...)` | `Dict` | Merge two MDM records |
| `add_metadata(...)` | `Dict` | Add catalog metadata |
| `search_catalog(query)` | `List` | Search catalog |
| `create_quality_rule(...)` | `Dict` | Create quality rule |
| `run_quality_checks()` | `Dict` | Execute all quality checks |
| `get_quality_dashboard()` | `Dict` | Get quality dashboard |
| `add_lineage_node(...)` | `Dict` | Add lineage node |
| `add_lineage_edge(...)` | `Dict` | Add lineage edge |
| `get_lineage_impact(id)` | `Dict` | Get impact analysis |
| `create_governance_policy(...)` | `Dict` | Create governance policy |
| `log_audit(...)` | `Dict` | Log audit event |
| `register_schema(...)` | `Dict` | Register schema version |
| `check_schema_compatibility(...)` | `Dict` | Check schema compatibility |
| `create_partition(...)` | `Dict` | Create partition config |
| `create_masking_rule(...)` | `Dict` | Create masking rule |
| `mask_data(table, record)` | `Dict` | Apply masking rules |
| `add_dependency_node(...)` | `Dict` | Add dependency node |
| `add_dependency_edge(...)` | `Dict` | Add dependency edge |
| `get_dependency_order()` | `List` | Topological sort |
| `create_retention_rule(...)` | `Dict` | Create retention rule |
| `record_cost(...)` | `Dict` | Record cost entry |
| `get_cost_report()` | `Dict` | Get cost report |
| `create_migration_plan(...)` | `Dict` | Create migration plan |
| `add_column_lineage(...)` | `Dict` | Add column lineage |
| `get_status()` | `Dict` | Get agent status |
| `get_full_report()` | `Dict` | Get comprehensive report |

### DataModelManager

| Method | Description |
|--------|-------------|
| `create_model(...)` | Create data model |
| `update_model(...)` | Update model fields |
| `delete_model(id)` | Delete model |
| `create_table(...)` | Create table |
| `add_field(table_id, field)` | Add field to table |
| `remove_field(table_id, field_id)` | Remove field |
| `get_tables_by_domain(domain)` | Filter by domain |
| `get_tables_by_storage(type)` | Filter by storage |
| `search_tables(query)` | Search tables |
| `clone_table(source_id, new_id, name)` | Clone table |
| `get_pii_fields()` | Get all PII fields |
| `get_model_summary()` | Summary statistics |

### IntegrationManager

| Method | Description |
|--------|-------------|
| `create_pipeline(...)` | Create pipeline |
| `run_pipeline(id)` | Execute pipeline |
| `pause_pipeline(id)` | Pause pipeline |
| `resume_pipeline(id)` | Resume pipeline |
| `delete_pipeline(id)` | Delete pipeline |
| `get_pipelines_by_pattern(pattern)` | Filter by pattern |
| `get_active_pipelines()` | Get active pipelines |
| `get_pipeline_stats(id)` | Get P95 metrics |
| `get_alerts(limit)` | Get failure alerts |

---

## Configuration

```python
from agents.data_architecture.agent import Config, StorageType

config = Config(
    default_storage=StorageType.RELATIONAL_DB,
    quality_check_interval="daily",
    lineage_depth=20,
    enable_cdc=True,
    enable_column_lineage=True,
    enable_cost_tracking=True,
    enable_partitioning=True,
    enable_masking=True,
    enable_retention=True,
    enable_schema_registry=True,
    enable_dependency_graph=True,
    enable_migration_planner=True,
)

agent = DataArchitectureAgent(config)
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `default_storage` | `StorageType` | `RELATIONAL_DB` | Default storage backend |
| `quality_check_interval` | `str` | `"daily"` | Quality check frequency |
| `lineage_depth` | `int` | `20` | Max lineage traversal depth |
| `enable_cdc` | `bool` | `True` | Enable CDC pipelines |
| `enable_column_lineage` | `bool` | `True` | Enable column-level lineage |
| `enable_cost_tracking` | `bool` | `True` | Enable cost tracking |
| `enable_partitioning` | `bool` | `True` | Enable data partitioning |
| `enable_masking` | `bool` | `True` | Enable data masking |
| `enable_retention` | `bool` | `True` | Enable retention management |
| `enable_schema_registry` | `bool` | `True` | Enable schema registry |
| `enable_dependency_graph` | `bool` | `True` | Enable dependency graph |
| `enable_migration_planner` | `bool` | `True` | Enable migration planning |

---

## Data Types

| Type | Size (bytes) | Description |
|------|-------------|-------------|
| `STRING` | 256 | Variable-length text |
| `INTEGER` | 4 | 32-bit integer |
| `FLOAT` | 8 | 64-bit float |
| `BOOLEAN` | 1 | True/False |
| `DATE` | 4 | Date only |
| `DATETIME` | 8 | Date + Time |
| `TIMESTAMP` | 8 | UTC timestamp |
| `BINARY` | 1024 | Binary data |
| `JSON` | 4096 | Semi-structured |
| `ARRAY` | 1024 | Array type |
| `MAP` | 2048 | Key-value map |
| `DECIMAL` | 16 | Exact numeric |
| `UUID` | 16 | Universally unique |
| `ENUM` | 4 | Enumeration |
| `TEXT` | 65536 | Long text |
| `BLOB` | 1048576 | Binary large object |

---

## Enums Reference

### ModelType
`CONCEPTUAL`, `LOGICAL`, `PHYSICAL`, `SEMANTIC`

### DataType
`STRING`, `INTEGER`, `FLOAT`, `BOOLEAN`, `DATE`, `DATETIME`, `TIMESTAMP`, `BINARY`, `JSON`, `ARRAY`, `MAP`, `DECIMAL`, `UUID`, `ENUM`, `TEXT`, `BLOB`

### IntegrationPattern
`ETL`, `ELT`, `CDC`, `API_SYNC`, `FILE_TRANSFER`, `STREAMING`, `EVENT_DRIVEN`, `BATCH`

### StorageType
`RELATIONAL_DB`, `DOCUMENT_DB`, `KEY_VALUE_STORE`, `COLUMN_FAMILY`, `GRAPH_DB`, `TIME_SERIES`, `OBJECT_STORAGE`, `DATA_LAKE`, `DATA_WAREHOUSE`, `CACHE`

### DataDomain
`CUSTOMER`, `PRODUCT`, `ORDER`, `FINANCE`, `INVENTORY`, `ANALYTICS`, `MARKETING`, `HR`, `SUPPLY_CHAIN`, `CUSTOM`

### QualityRuleType
`NOT_NULL`, `UNIQUE`, `RANGE_CHECK`, `PATTERN_MATCH`, `REFERENTIAL_INTEGRITY`, `FRESHNESS`, `COMPLETENESS`, `CONSISTENCY`, `ACCURACY`, `CUSTOM`

### GovernancePolicy
`DATA_CLASSIFICATION`, `ACCESS_CONTROL`, `RETENTION`, `ENCRYPTION`, `MASKING`, `AUDIT_LOGGING`, `COMPLIANCE`, `QUALITY_STANDARD`

### SchemaEvolution
`ADD_COLUMN`, `DROP_COLUMN`, `RENAME_COLUMN`, `CHANGE_TYPE`, `ADD_TABLE`, `DROP_TABLE`, `ADD_INDEX`, `DROP_INDEX`

### LineageNodeType
`SOURCE`, `TRANSFORMATION`, `DESTINATION`, `QUALITY_CHECK`, `AGGREGATION`, `FILTER`, `JOIN`, `LOOKUP`

### PartitionStrategy
`NONE`, `HASH`, `RANGE`, `LIST`, `TIME_INTERVAL`, `GEOGRAPHIC`, `DIRECTORY`

### MaskingType
`FULL_REDACT`, `PARTIAL`, `HASH`, `TOKENIZE`, `SHUFFLE`, `DATE_SHIFT`, `NULL_OUT`, `FORMAT_PRESERVING`

### RetentionAction
`DELETE`, `ARCHIVE`, `COMPRESS`, `MOVE_TO_COLD`, `KEEP_FOREVER`, `ANONYMIZE`

### MigrationStatus
`PLANNED`, `IN_PROGRESS`, `COMPLETED`, `FAILED`, `ROLLED_BACK`, `PAUSED`

### CostCategory
`COMPUTE`, `STORAGE`, `NETWORK`, `QUERY`, `BACKUP`, `LICENSE`, `TRANSFORMATION`, `MONITORING`

### DependencyType
`TABLE_DEPENDS_ON`, `PIPELINE_FEEDS`, `QUALITY_RULE_CHECKS`, `GOVERNANCE_POLICY_APPLIES`, `SCHEMA_OWNED_BY`, `DOMAIN_CONTAINS`

---

## Best Practices

### Data Modeling

- Always define primary keys with `nullable=False`
- Flag PII fields with `pii_flag=True` and appropriate `classification`
- Set `max_length` for STRING fields to prevent unbounded growth
- Use DECIMAL for financial data, never FLOAT
- Set `retention_days` on tables that contain time-sensitive data

### Integration Pipelines

- Use CDC for real-time sync, ETL for batch transformations
- Set `retry_count` and `timeout_seconds` for resilience
- Enable `alert_on_failure` for critical pipelines
- Monitor P95 latency, not just average
- Track `bytes_transferred` for cost attribution

### Data Quality

- Start with NOT_NULL and UNIQUE rules on primary keys
- Use REFERENTIAL_INTEGRITY for foreign key validation
- Set severity levels: critical for production, warning for staging
- Review `score_history` trends weekly
- Run `run_all_checks()` on schedule, not on-demand

### Governance

- Set `enforcement_level="mandatory"` for compliance-critical policies
- Log every data access with `log_audit()`
- Run compliance checks per-policy, not just globally
- Keep audit log rotation at 10000 entries max

### Schema Evolution

- Always add columns, never remove (backward compatible)
- Use `check_schema_compatibility()` before applying changes
- Set `breaking_change=True` for any removal or rename
- Register every schema version in the registry

### Performance

- Use partitioning for tables with >1M rows
- Hash partitioning for均匀 distribution
- Time-interval partitioning for time-series data
- Monitor cost by resource to identify hotspots

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Schema compatibility fails | Removing/renaming fields | Add columns instead; use migration for breaking changes |
| Pipeline shows 0% success | Pipeline paused or not initialized | Check `is_active` status; resume with `resume_pipeline()` |
| MDM merge unexpected | Wrong merge strategy | Use `strategy="highest_quality"`; set survivorship rules |
| Column lineage incomplete | Missing intermediate entries | Add lineage nodes for every transformation step |
| Cost totals are zero | No cost entries recorded | Use `record_cost()` to log costs |
| Dependency graph has cycles | Circular dependencies | Run `topological_sort()` to detect; break cycles |
| Quality checks always pass | Thresholds too low | Set explicit thresholds; connect to real data sources |
| Partition index out of range | Partition count mismatch | Run `init_partitions()` after creating config |
| Masking returns original value | No rule for field | Create masking rule for the specific table/field |
| Migration stuck IN_PROGRESS | No completion signal | Call `complete_migration()` or `fail_migration()` |

---

## Files

| File | Lines | Description |
|------|-------|-------------|
| `agent.py` | ~900 | Main implementation with all subsystems |
| `GROK.md` | ~900 | Agent identity, capabilities, API reference |
| `ARCHITECTURE.md` | ~900 | System architecture, diagrams, patterns |
| `README.md` | ~900 | This file - usage guide and documentation |

---

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md).

---

## License

MIT License - see [LICENSE](../../LICENSE).

---

*Data Architecture Agent v3.0.0 - Part of the Awesome Grok Skills collection.*

*Last updated: 2026-07-06*
