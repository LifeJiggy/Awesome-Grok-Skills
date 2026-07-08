# Data Engineering Agent

Enterprise-grade data engineering agent for ETL/ELT pipelines, data warehousing, streaming architectures, data quality management, orchestration, and infrastructure as code.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Creating Pipelines](#creating-pipelines)
  - [Running Quality Checks](#running-quality-checks)
  - [Orchestrating Jobs](#orchestrating-jobs)
  - [Managing Warehouse Tables](#managing-warehouse-tables)
  - [Tracking Data Lineage](#tracking-data-lineage)
  - [Streaming Events](#streaming-events)
  - [Schema Management](#schema-management)
  - [Data Catalog](#data-catalog)
  - [Infrastructure as Code](#infrastructure-as-code)
  - [Monitoring & Alerting](#monitoring--alerting)
- [API Reference](#api-reference)
  - [DataEngineeringAgent](#dataengineeringagent)
  - [PipelineManager](#pipelinemanager)
  - [DataQualityManager](#dataqualitymanager)
  - [ETLOrchestrator](#etlorchestrator)
  - [DataWarehouseManager](#datawarehousemanager)
  - [DataLineageTracker](#datalineagetracker)
  - [StreamingManager](#streamingmanager)
  - [SchemaRegistry](#schemaregistry)
  - [DataCatalog](#datacatalog)
  - [InfrastructureAsCodeManager](#infrastructureascodemanager)
  - [MonitoringManager](#monitoringmanager)
- [Examples](#examples)
- [Configuration](#configuration)
- [Data Models](#data-models)
  - [Enums](#enums)
  - [Dataclasses](#dataclasses)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Data Engineering Agent is a comprehensive, modular Python framework for building and managing enterprise data pipelines. It provides first-class support for:

- **ETL/ELT Pipelines** — Full lifecycle management with extract, transform, and load phases
- **Data Quality** — Rule-based quality checks, dataset profiling, and scoring
- **Orchestration** — DAG-based job scheduling with dependency resolution
- **Data Warehousing** — Table management across medallion architecture layers
- **Data Lineage** — Graph-based lineage tracking with impact analysis
- **Streaming** — Topic management, produce/consume with partition awareness
- **Schema Registry** — Versioned schema management with compatibility checks
- **Data Catalog** — Metadata search, tagging, and discovery
- **Infrastructure as Code** — Terraform and CloudFormation template generation
- **Monitoring** — Metrics collection, alert rules, and health dashboards

### Why This Agent?

| Problem | Solution |
|---------|----------|
| Scattered pipeline logic | Centralized `PipelineManager` with full lifecycle |
| Silent data quality issues | `DataQualityManager` with configurable rule engine |
| Manual dependency management | `ETLOrchestrator` with topological sort |
| Schema drift | `SchemaRegistry` with compatibility checks |
| Unknown data consumers | `DataLineageTracker` with impact analysis |
| Infrastructure drift | `InfrastructureAsCodeManager` with declarative templates |
| Invisible data assets | `DataCatalog` with search, tags, and ownership |
| Silent failures | `MonitoringManager` with alert rules and metrics |

### Design Philosophy

- **Schema-first**: Define data contracts before writing processing logic
- **Quality gates**: Validation at every data boundary
- **Idempotent operations**: Safe to retry without side effects
- **Observable by default**: Every operation is logged and metricated
- **Modular composition**: Use only the components you need

---

## Features

### Pipeline Management

- Create pipelines with source, transforms, and sink configurations
- Execute pipelines with automatic stage tracking (Extract → Transform → Load)
- Built-in retry logic with configurable timeout
- Pipeline run history with full metrics (duration, records processed, failures)
- Health calculation across all managed pipelines
- Thread-safe pipeline state management via `threading.Lock`

### Data Quality Engine

- Rule-based checks: NOT NULL, UNIQUE, RANGE, REGEX
- Weighted quality scoring based on severity levels (INFO through CRITICAL)
- Dataset profiling with column-level statistics (type detection, null counts, min/max/mean, distinct count)
- Quality level classification: Excellent, Good, Fair, Poor, Critical
- Configurable severity per check rule

### ETL Orchestration

- Job registration with cron-based scheduling
- Dependency resolution via topological sort
- ASCII DAG visualization for job relationships
- Execution recording with per-step timing and status
- Aggregate monitoring across all registered jobs

### Data Warehouse

- Table management across medallion layers (Raw → Staging → Curated → Analytics → Mart)
- Support for Parquet, ORC, Avro, Delta, and Iceberg formats
- DDL generation from schema definitions
- Table optimization (compaction, statistics refresh, metadata cleanup)
- Storage usage statistics across layers

### Data Lineage

- DAG-based lineage graph with upstream/downstream traversal
- Impact analysis for change management ("what breaks if I modify this?")
- Configurable traversal depth to prevent infinite loops
- ASCII graph visualization
- Node metadata and ownership tracking

### Streaming

- Topic creation with partition and replication configuration
- Produce and consume with partition-aware routing (`hash(key) % partitions`)
- Consumer group management
- Buffer-based message storage with offset tracking
- Topic-level statistics (buffer size, partition count, retention)

### Schema Registry

- Multi-version schema registration with auto-incrementing version numbers
- Compatibility checking (ADD_COLUMNS, TYPE_PROMOTION, FAIL, IGNORE strategies)
- Schema listing with version history and column counts
- Column-level validation against existing schema

### Data Catalog

- Add entries with type, description, owner, and tags
- Full-text search across name, description, and tags
- Filter by entry type, tag, or owner
- Catalog statistics (entries by type, unique tags, unique owners)

### Infrastructure as Code

- Define resources with type, config, and dependencies
- Generate Terraform (HCL) templates from resource definitions
- Generate CloudFormation (JSON) templates from resource definitions
- Deployment planning and execution with step tracking

### Monitoring

- Metric recording with timestamp history
- Alert rule evaluation on every metric record (gt, lt, eq operators)
- Multi-channel alert delivery (Slack, Email, PagerDuty)
- Active alert tracking with recent alert history
- Monitoring summary dashboard

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DataEngineeringAgent                          │
├─────────────────────────────────────────────────────────────────┤
│  PipelineManager │ DataQualityManager │ ETLOrchestrator         │
│  DataWarehouseManager │ DataLineageTracker │ StreamingManager   │
│  SchemaRegistry │ DataCatalog │ InfrastructureAsCodeManager     │
│  MonitoringManager                                              │
└─────────────────────────────────────────────────────────────────┘
```

The agent follows a mediator pattern where `DataEngineeringAgent` coordinates all components. Each component is independently usable but provides enhanced functionality when composed through the agent.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the complete system architecture with detailed diagrams, design patterns, security architecture, scalability patterns, and deployment topologies.

---

## Quick Start

### Minimal Example

```python
from agent import DataEngineeringAgent, PipelineType

agent = DataEngineeringAgent()

pipeline = agent.create_full_pipeline(
    name="hello_world",
    source={"type": "csv", "path": "/data/input.csv"},
    transforms=[
        {"type": "filter", "column": "status", "op": "eq", "value": "active"},
    ],
    sink={"type": "csv", "path": "/data/output.csv"},
    pipeline_type=PipelineType.ETL,
)

run = agent.pipeline_manager.execute_pipeline(pipeline.pipeline_id)
print(f"Pipeline completed: {run.status.value}")
print(f"Records processed: {run.records_loaded}")
```

### Quality Check Example

```python
from agent import DataEngineeringAgent, QualityCheck, Severity

agent = DataEngineeringAgent()

agent.quality_manager.add_check("users", QualityCheck(
    name="email_valid", column="email", rule="REGEX ^.+@.+\\..+$", severity=Severity.HIGH
))

data = [
    {"email": "alice@example.com", "age": 30},
    {"email": "invalid-email", "age": 25},
]
results = agent.quality_manager.run_checks("users", data)
score = agent.quality_manager.compute_quality_score(results)
print(f"Quality: {score}/100")
```

### Run Directly

```bash
python agents/data-engineering/agent.py
```

This runs a demo that exercises all major components including pipeline creation, execution, quality assessment, streaming, and system status reporting.

---

## Installation

### Requirements

- Python 3.10+
- No external dependencies (uses only Python standard library)

### Setup

```bash
# Clone the repository
git clone https://github.com/example/awesome-grok-skills.git
cd awesome-grok-skills

# Run the agent demo
python agents/data-engineering/agent.py
```

### Integration

Import individual components or the full agent:

```python
# Full agent (recommended)
from agent import DataEngineeringAgent

# Individual components
from agent import PipelineManager, DataQualityManager, ETLOrchestrator
from agent import DataWarehouseManager, DataLineageTracker, StreamingManager
from agent import SchemaRegistry, DataCatalog, InfrastructureAsCodeManager, MonitoringManager

# Data models
from agent import (
    PipelineConfig, PipelineRun, QualityCheck, QualityResult,
    SchemaDefinition, ColumnDefinition, LineageNode, StreamingTopic,
    CatalogEntry, IaCResource, AlertRule,
)

# Enums
from agent import (
    PipelineStatus, PipelineType, DataQualityLevel, Severity,
    StorageFormat, WarehouseLayer, StreamingMode, IaCTemplateType,
    SchemaEvolutionStrategy, CatalogEntryType,
)
```

---

## Usage

### Creating Pipelines

```python
from agent import DataEngineeringAgent, PipelineType

agent = DataEngineeringAgent()

# Create an ETL pipeline with transforms
pipeline = agent.create_full_pipeline(
    name="user_analytics_etl",
    source={
        "type": "postgres",
        "connection": "prod_db",
        "query": "SELECT * FROM users WHERE active = true",
    },
    transforms=[
        {"type": "filter", "column": "age", "op": "gte", "value": 18},
        {"type": "rename", "renames": {"user_id": "id"}},
        {"type": "aggregate", "group_keys": ["status"], "aggregations": {"amount": "sum"}},
    ],
    sink={"type": "bigquery", "table": "analytics.adult_users"},
    pipeline_type=PipelineType.ETL,
)

# Execute and inspect
run = agent.pipeline_manager.execute_pipeline(pipeline.pipeline_id)
print(f"Status: {run.status.value}")
print(f"Extracted: {run.records_extracted}")
print(f"Transformed: {run.records_transformed}")
print(f"Loaded: {run.records_loaded}")
```

### Running Quality Checks

```python
from agent import QualityCheck, Severity

# Add quality checks for a dataset
agent.quality_manager.add_check("orders", QualityCheck(
    name="order_id_not_null", column="order_id", rule="NOT NULL", severity=Severity.CRITICAL
))
agent.quality_manager.add_check("orders", QualityCheck(
    name="amount_range", column="amount", rule="RANGE 0,1000000", severity=Severity.HIGH
))
agent.quality_manager.add_check("orders", Column="email", rule="REGEX ^.+@.+$", severity=Severity.MEDIUM)

# Run checks
results = agent.quality_manager.run_checks("orders", orders_data)
score = agent.quality_manager.compute_quality_score(results)
print(f"Quality: {score}/100")

# Profile the dataset
profile = agent.quality_manager.profile_dataset(orders_data)
for col, stats in profile["columns"].items():
    print(f"  {col}: type={stats['type']}, nulls={stats['null_pct']}%, distinct={stats['distinct_count']}")
```

### Orchestrating Jobs

```python
# Register jobs with dependencies
extract = agent.etl_orchestrator.register_job("extract_orders", "0 2 * * *", timeout=3600)
transform = agent.etl_orchestrator.register_job("transform_orders", "0 3 * * *", dependencies=[extract["job_id"]])
load = agent.etl_orchestrator.register_job("load_warehouse", "0 4 * * *", dependencies=[transform["job_id"]])

# Execute with dependency resolution
result = agent.etl_orchestrator.execute_job(load["job_id"])
print(f"Steps completed: {len(result['steps'])}")

# Visualize the DAG
print(agent.etl_orchestrator.get_dag_visualization())
```

### Managing Warehouse Tables

```python
from agent import WarehouseLayer, StorageFormat, SchemaDefinition, ColumnDefinition

# Define a schema
schema = SchemaDefinition(name="fact_orders", columns=[
    ColumnDefinition(name="order_id", data_type="VARCHAR(36)", primary_key=True),
    ColumnDefinition(name="customer_id", data_type="VARCHAR(36)", nullable=False),
    ColumnDefinition(name="order_date", data_type="DATE"),
    ColumnDefinition(name="amount", data_type="DECIMAL(10,2)"),
], partition_keys=["order_date"])

# Create table
table = agent.warehouse_manager.create_table(
    name="analytics.fact_orders",
    layer=WarehouseLayer.CURATED,
    schema=schema,
    partition_keys=["order_date"],
    storage_format=StorageFormat.PARQUET,
)

# Generate DDL
ddl = agent.warehouse_manager.generate_ddl(table["table_id"])
print(ddl)

# Optimize
agent.warehouse_manager.optimize_table(table["table_id"])
```

### Tracking Data Lineage

```python
from agent import LineageNode

# Register lineage nodes
agent.lineage_tracker.register_node(LineageNode(
    node_id="raw_orders", name="raw.orders", node_type="table"
))
agent.lineage_tracker.register_node(LineageNode(
    node_id="clean_orders", name="clean.orders", node_type="table"
))
agent.lineage_tracker.register_node(LineageNode(
    node_id="mart_sales", name="mart.daily_sales", node_type="table"
))

# Connect them
agent.lineage_tracker.add_edge("raw_orders", "clean_orders")
agent.lineage_tracker.add_edge("clean_orders", "mart_sales")

# Trace upstream
upstream = agent.lineage_tracker.get_upstream("mart_sales")
print(f"Upstream: {[n.name for n in upstream]}")

# Impact analysis
impact = agent.lineage_tracker.get_impact_analysis("raw_orders")
print(f"Would affect {impact['affected_nodes']} downstream nodes")
```

### Streaming Events

```python
# Create a topic
topic = agent.streaming_manager.create_topic("user_events", partitions=6)

# Produce messages
agent.streaming_manager.produce(topic.topic_id, "evt_1", {"type": "click", "page": "/home"})
agent.streaming_manager.produce(topic.topic_id, "evt_2", {"type": "view", "page": "/about"})

# Consume messages
messages = agent.streaming_manager.consume(topic.topic_id, "analytics_consumer", max_messages=10)
for msg in messages:
    print(f"Key: {msg['key']}, Partition: {msg['partition']}, Value: {msg['value']}")
```

### Schema Management

```python
from agent import SchemaDefinition, ColumnDefinition, SchemaEvolutionStrategy

# Register v1
v1 = SchemaDefinition(name="user_profile", version=1, columns=[
    ColumnDefinition(name="user_id", data_type="string", primary_key=True),
    ColumnDefinition(name="email", data_type="string"),
], compatibility=SchemaEvolutionStrategy.ADD_COLUMNS)
agent.schema_registry.register_schema(v1)

# Register v2 (compatible — adds new column)
v2 = SchemaDefinition(name="user_profile", version=2, columns=[
    ColumnDefinition(name="user_id", data_type="string", primary_key=True),
    ColumnDefinition(name="email", data_type="string"),
    ColumnDefinition(name="phone", data_type="string"),
], compatibility=SchemaEvolutionStrategy.ADD_COLUMNS)
result = agent.schema_registry.check_compatibility("user_profile", v2)
print(f"Compatible: {result['compatible']}")
```

### Data Catalog

```python
from agent import CatalogEntry, CatalogEntryType

# Add entries
agent.data_catalog.add_entry(CatalogEntry(
    name="daily_sales", entry_type=CatalogEntryType.TABLE,
    description="Aggregated daily sales by product",
    owner="analytics_team", tags=["sales", "daily", "curated"],
))

# Search
results = agent.data_catalog.search("sales")
print(f"Found {len(results)} entries")

# Filter by tag
by_tag = agent.data_catalog.get_entries_by_tag("sales")
print(f"Tagged 'sales': {len(by_tag)}")
```

### Infrastructure as Code

```python
from agent import IaCTemplateType

# Define a resource
s3 = agent.iac_manager.define_resource(
    name="data_lake_raw", resource_type="aws_s3_bucket",
    template_type=IaCTemplateType.TERRAFORM,
    config={"bucket": "company-data-lake-raw", "versioning": True},
)

# Generate template
tf = agent.iac_manager.generate_template(s3.resource_id)
print(tf)

# Plan and deploy
plan = agent.iac_manager.plan_deployment()
print(f"Resources to add: {plan['resources_to_add']}")
```

### Monitoring & Alerting

```python
from agent import AlertRule, Severity

# Add alert rule
agent.monitoring.add_alert_rule(AlertRule(
    name="high_pipeline_duration", metric="pipeline.duration_minutes",
    threshold=60, operator="gt", severity=Severity.HIGH, channels=["slack"],
))

# Record metrics (triggers alert evaluation)
agent.monitoring.record_metric("pipeline.duration_minutes", 75)

# Check alerts
alerts = agent.monitoring.get_active_alerts()
print(f"Active alerts: {len(alerts)}")
```

---

## API Reference

### DataEngineeringAgent

Top-level orchestrator composing all components.

| Method | Return | Description |
|--------|--------|-------------|
| `create_full_pipeline(name, source, transforms, sink, pipeline_type)` | `PipelineConfig` | Create pipeline with lineage + catalog registration |
| `run_quality_assessment(dataset, data)` | `Dict` | Run quality checks and return score |
| `get_system_status()` | `Dict` | Aggregate status of all components |
| `shutdown()` | `None` | Gracefully stop all components |

### PipelineManager

| Method | Return | Description |
|--------|--------|-------------|
| `create_pipeline(name, source, transforms, sink, ...)` | `PipelineConfig` | Create a new pipeline |
| `execute_pipeline(pipeline_id)` | `PipelineRun` | Execute and track a pipeline run |
| `get_pipeline(pipeline_id)` | `Optional[PipelineConfig]` | Get pipeline by ID |
| `list_pipelines(pipeline_type, tags)` | `List[PipelineConfig]` | List pipelines with filters |
| `delete_pipeline(pipeline_id)` | `bool` | Delete a pipeline |
| `get_pipeline_runs(pipeline_id)` | `List[PipelineRun]` | Get execution history |
| `get_pipeline_health()` | `Dict[str, Any]` | Get aggregate health metrics |

### DataQualityManager

| Method | Return | Description |
|--------|--------|-------------|
| `add_check(dataset, check)` | `QualityCheck` | Register a quality check |
| `remove_check(dataset, check_id)` | `bool` | Remove a quality check |
| `run_checks(dataset, data)` | `List[QualityResult]` | Run all checks on data |
| `profile_dataset(data)` | `Dict[str, Any]` | Profile dataset statistics |
| `compute_quality_score(results)` | `float` | Compute weighted score (0-100) |
| `get_quality_summary(dataset)` | `Dict[str, Any]` | Get quality status summary |

### ETLOrchestrator

| Method | Return | Description |
|--------|--------|-------------|
| `register_job(job_name, schedule, ...)` | `Dict` | Register an ETL job |
| `resolve_dependencies(job_id)` | `List[str]` | Topological sort of dependencies |
| `execute_job(job_id)` | `Dict` | Execute job and dependencies |
| `get_dag_visualization()` | `str` | ASCII DAG representation |
| `monitor_jobs()` | `Dict[str, Any]` | Aggregate monitoring stats |

### DataWarehouseManager

| Method | Return | Description |
|--------|--------|-------------|
| `create_table(name, layer, schema, ...)` | `Dict` | Create a warehouse table |
| `drop_table(table_id)` | `bool` | Drop a table |
| `list_tables(layer)` | `List[Dict]` | List tables with optional layer filter |
| `get_storage_stats()` | `Dict[str, Any]` | Storage usage statistics |
| `optimize_table(table_id)` | `Dict` | Run table optimization |
| `generate_ddl(table_id)` | `str` | Generate SQL DDL |

### DataLineageTracker

| Method | Return | Description |
|--------|--------|-------------|
| `register_node(node)` | `LineageNode` | Register a lineage node |
| `add_edge(upstream_id, downstream_id)` | `bool` | Add a lineage edge |
| `get_upstream(node_id, max_depth)` | `List[LineageNode]` | Trace upstream sources |
| `get_downstream(node_id, max_depth)` | `List[LineageNode]` | Trace downstream consumers |
| `get_impact_analysis(node_id)` | `Dict` | Assess change impact |
| `visualize()` | `str` | ASCII graph visualization |

### StreamingManager

| Method | Return | Description |
|--------|--------|-------------|
| `create_topic(name, partitions, ...)` | `StreamingTopic` | Create a streaming topic |
| `produce(topic_id, key, value)` | `bool` | Produce a message |
| `consume(topic_id, consumer_id, max_messages)` | `List[Dict]` | Consume messages |
| `register_consumer(topic_id, consumer_group)` | `Dict` | Register a consumer |
| `get_topic_stats()` | `Dict[str, Any]` | Topic statistics |

### SchemaRegistry

| Method | Return | Description |
|--------|--------|-------------|
| `register_schema(schema)` | `SchemaDefinition` | Register a schema version |
| `get_schema(name, version)` | `Optional[SchemaDefinition]` | Get schema by name/version |
| `list_schemas()` | `List[Dict]` | List all schemas |
| `check_compatibility(name, new_schema)` | `Dict` | Check compatibility |

### DataCatalog

| Method | Return | Description |
|--------|--------|-------------|
| `add_entry(entry)` | `CatalogEntry` | Add a catalog entry |
| `get_entry(entry_id)` | `Optional[CatalogEntry]` | Get entry by ID |
| `search(query, entry_type)` | `List[CatalogEntry]` | Search catalog |
| `get_entries_by_tag(tag)` | `List[CatalogEntry]` | Filter by tag |
| `get_entries_by_owner(owner)` | `List[CatalogEntry]` | Filter by owner |
| `get_catalog_stats()` | `Dict[str, Any]` | Catalog statistics |

### InfrastructureAsCodeManager

| Method | Return | Description |
|--------|--------|-------------|
| `define_resource(name, type, template_type, config)` | `IaCResource` | Define an infrastructure resource |
| `generate_template(resource_id)` | `str` | Generate IaC template |
| `plan_deployment(resource_ids)` | `Dict` | Plan resource deployment |
| `deploy(resource_ids)` | `Dict` | Execute deployment |

### MonitoringManager

| Method | Return | Description |
|--------|--------|-------------|
| `add_alert_rule(rule)` | `AlertRule` | Add an alert rule |
| `record_metric(metric_name, value)` | `None` | Record a metric value |
| `get_metric_history(metric_name, limit)` | `List[Dict]` | Get metric history |
| `get_active_alerts()` | `List[Dict]` | Get recently fired alerts |
| `get_monitoring_summary()` | `Dict[str, Any]` | Monitoring summary |

---

## Examples

### End-to-End Pipeline with Quality Gates

```python
from agent import (
    DataEngineeringAgent, PipelineType, QualityCheck, Severity,
    SchemaDefinition, ColumnDefinition, WarehouseLayer, StorageFormat,
    LineageNode, CatalogEntry, CatalogEntryType, AlertRule,
)

agent = DataEngineeringAgent()

# 1. Define schema
schema = SchemaDefinition(name="events", columns=[
    ColumnDefinition(name="event_id", data_type="string", primary_key=True),
    ColumnDefinition(name="user_id", data_type="string"),
    ColumnDefinition(name="event_type", data_type="string"),
    ColumnDefinition(name="timestamp", data_type="timestamp"),
])
agent.schema_registry.register_schema(schema)

# 2. Create warehouse table
table = agent.warehouse_manager.create_table(
    name="analytics.events",
    layer=WarehouseLayer.CURATED,
    schema=schema,
    storage_format=StorageFormat.PARQUET,
)

# 3. Add quality checks
agent.quality_manager.add_check("events", QualityCheck(
    name="event_id_unique", column="event_id", rule="UNIQUE", severity=Severity.CRITICAL
))

# 4. Create pipeline
pipeline = agent.create_full_pipeline(
    name="events_pipeline",
    source={"type": "kafka", "topic": "raw_events"},
    transforms=[
        {"type": "filter", "column": "event_type", "op": "in", "value": ["click", "view"]},
    ],
    sink={"type": "warehouse", "table": "analytics.events"},
)

# 5. Execute
run = agent.pipeline_manager.execute_pipeline(pipeline.pipeline_id)
print(f"Status: {run.status.value}, Records: {run.records_loaded}")
```

### Streaming Pipeline with Consumer Groups

```python
topic = agent.streaming_manager.create_topic("clicks", partitions=12, replication_factor=3)

# Register consumers
agent.streaming_manager.register_consumer(topic.topic_id, "analytics_group")
agent.streaming_manager.register_consumer(topic.topic_id, "ml_group")

# Produce events
for event in click_events:
    agent.streaming_manager.produce(topic.topic_id, event["session_id"], event)

# Consume
analytics_msgs = agent.streaming_manager.consume(topic.topic_id, "cons_1", 100)
ml_msgs = agent.streaming_manager.consume(topic.topic_id, "cons_2", 100)
```

### Schema Evolution with Compatibility Check

```python
v1 = SchemaDefinition(name="users", columns=[
    ColumnDefinition(name="id", data_type="string"),
    ColumnDefinition(name="email", data_type="string"),
])
agent.schema_registry.register_schema(v1)

# Evolve schema
v2 = SchemaDefinition(name="users", columns=[
    ColumnDefinition(name="id", data_type="string"),
    ColumnDefinition(name="email", data_type="string"),
    ColumnDefinition(name="phone", data_type="string"),
])
compat = agent.schema_registry.check_compatibility("users", v2)
if compat["compatible"]:
    agent.schema_registry.register_schema(v2)
    print("Schema v2 registered")
else:
    print(f"Incompatible: {compat['issues']}")
```

---

## Configuration

### Pipeline Configuration

```yaml
pipeline:
  name: "daily_sales_etl"
  type: "etl"
  schedule: "0 2 * * *"
  retry_count: 3
  timeout_seconds: 3600
  source:
    type: "postgres"
    connection: "prod_db"
    query: "SELECT * FROM orders"
  transforms:
    - type: "filter"
      column: "status"
      op: "ne"
      value: "cancelled"
  sink:
    type: "bigquery"
    table: "analytics.daily_sales"
```

### Quality Check Configuration

```yaml
quality:
  dataset: "orders"
  checks:
    - name: "order_id_not_null"
      column: "order_id"
      rule: "NOT NULL"
      severity: "critical"
    - name: "amount_range"
      column: "amount"
      rule: "RANGE 0,1000000"
      severity: "high"
    - name: "email_format"
      column: "email"
      rule: "REGEX ^.+@.+\\..+$"
      severity: "medium"
```

### Alert Configuration

```yaml
monitoring:
  alerts:
    - name: "pipeline_failure"
      metric: "pipeline.runs_failed"
      threshold: 1
      operator: "gt"
      severity: "critical"
      channels: ["slack", "pagerduty"]
    - name: "quality_degradation"
      metric: "quality.score"
      threshold: 90
      operator: "lt"
      severity: "high"
      channels: ["slack", "email"]
```

### Warehouse Configuration

```yaml
warehouse:
  default_layer: "curated"
  default_format: "parquet"
  partition_strategy: "date"
  optimization:
    compact_threshold_mb: 256
    statistics_refresh: "daily"
```

---

## Data Models

### Enums

| Enum | Values | Description |
|------|--------|-------------|
| `PipelineStatus` | CREATED, PENDING, RUNNING, PAUSED, SUCCESS, FAILED, CANCELLED, RETRYING | Pipeline execution state |
| `DataQualityLevel` | EXCELLENT, GOOD, FAIR, POOR, CRITICAL | Quality assessment level |
| `Severity` | INFO, LOW, MEDIUM, HIGH, CRITICAL | Issue severity |
| `PipelineType` | ETL, ELT, STREAMING, BATCH, HYBRID, LAMBDA, KAPPA | Pipeline pattern |
| `WarehouseLayer` | RAW, STAGING, CURATED, ANALYTICS, MART, ARCHIVE | Medallion layer |
| `StorageFormat` | PARQUET, ORC, AVRO, CSV, JSON, DELTA, ICEBERG | File format |
| `StreamingMode` | EXACTLY_ONCE, AT_LEAST_ONCE, BEST_EFFORT | Delivery guarantee |
| `SchemaEvolutionStrategy` | FAIL, IGNORE, ADD_COLUMNS, TYPE_PROMOTION | Schema change handling |
| `CatalogEntryType` | TABLE, VIEW, DASHBOARD, PIPELINE, DATASET, TOPIC | Catalog asset type |
| `IaCTemplateType` | TERRAFORM, CLOUDFORMATION, PULUMI, CDK, ANSIBLE | IaC format |

### Dataclasses

| Class | Key Fields | Description |
|-------|-----------|-------------|
| `PipelineConfig` | pipeline_id, name, pipeline_type, source, transforms, sink, schedule | Pipeline definition |
| `PipelineRun` | run_id, pipeline_id, status, started_at, records_* | Execution record |
| `QualityCheck` | check_id, name, column, rule, severity | Quality rule definition |
| `QualityResult` | check_id, passed, records_checked, records_failed | Check result |
| `SchemaDefinition` | schema_id, name, version, columns, compatibility | Schema contract |
| `ColumnDefinition` | name, data_type, nullable, primary_key | Column specification |
| `LineageNode` | node_id, name, node_type, upstream, downstream | Lineage vertex |
| `StreamingTopic` | topic_id, name, partitions, replication_factor | Topic configuration |
| `CatalogEntry` | entry_id, name, entry_type, owner, tags | Catalog asset |
| `IaCResource` | resource_id, name, resource_type, template_type, config | Infrastructure resource |
| `AlertRule` | alert_id, name, metric, threshold, operator, channels | Alert definition |

---

## Best Practices

### Pipeline Design

1. **Idempotent writes** — Use overwrite or upsert modes so retries don't create duplicates
2. **Schema-first** — Define and register schemas before building pipelines
3. **Quality gates** — Add checks at both ingestion and load boundaries
4. **Lineage tracking** — Register lineage nodes for every pipeline and table
5. **Timeout configuration** — Set reasonable timeouts based on data volume
6. **Retry with backoff** — Configure retry_count for transient failures

### Data Quality

1. **Severity-appropriate rules** — CRITICAL for primary keys, HIGH for business fields, MEDIUM for nullable columns
2. **Profile regularly** — Run profiling on every dataset to catch anomalies early
3. **Score thresholds** — Set minimum quality scores as pipeline gates (e.g., >= 90 to proceed)
4. **Alert on degradation** — Monitor quality score trends, not just absolute values

### Schema Management

1. **Version everything** — Every schema change gets a new version
2. **Compatibility strategies** — Use ADD_COLUMNS for additive changes, FAIL for breaking changes
3. **Document changes** — Add descriptions to columns and schemas

### Infrastructure

1. **Everything in IaC** — No manual infrastructure changes
2. **Plan before deploy** — Always run plan_deployment() before deploy()
3. **Tag resources** — Use consistent tagging for cost allocation and ownership

### Monitoring

1. **Record metrics for everything** — Pipeline duration, quality scores, record counts
2. **Alert on symptoms, not causes** — Alert on "pipeline failed" not "disk full"
3. **Multi-channel alerts** — Critical alerts go to Slack AND PagerDuty
4. **Review alert history** — Tune thresholds based on false positive rates

---

## Troubleshooting

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| Pipeline FAILED | Source connection error | Check source config and network access |
| Quality score = 0 | All checks failing | Review data format and check rules |
| Schema incompatible | Type change on existing column | Use TYPE_PROMOTION strategy or rename column |
| No messages consumed | Consumer not registered | Register consumer with `register_consumer()` |
| Deployment fails | Missing dependencies | Run `plan_deployment()` to identify gaps |
| Alert not firing | Wrong metric name | Verify metric name matches `record_metric()` calls |
| Pipeline timeout | Data volume too large | Increase `timeout_seconds` or optimize transforms |
| DAG cycle error | Circular dependencies | Review job dependency graph, break cycle |

### Debug Mode

Enable debug logging for detailed output:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Health Check

```python
status = agent.get_system_status()
for component, metrics in status["components"].items():
    print(f"{component}: {metrics}")
```

### Pipeline Debugging

```python
# Check pipeline runs
runs = agent.pipeline_manager.get_pipeline_runs(pipeline_id)
for run in runs:
    print(f"Run {run.run_id}: {run.status.value}")
    for stage in run.stages:
        print(f"  {stage['name']}: {stage['status']} ({stage['records']} records)")
```

### Quality Debugging

```python
# Get quality summary
summary = agent.quality_manager.get_quality_summary("my_dataset")
print(f"Score: {summary['score']}, Level: {summary['level']}")
print(f"Passed: {summary['passed']}, Failed: {summary['failed']}")
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/example/awesome-grok-skills.git
cd awesome-grok-skills
python agents/data-engineering/agent.py
```

### Code Style

- Type hints on all public methods
- Dataclasses for structured data
- Enums for fixed sets of values
- Logging via `logging` module
- Docstrings for public APIs
- Thread safety for shared state

### Testing

```bash
python agents/data-engineering/agent.py
```

The `__main__` block runs a comprehensive demo that exercises all components.

---

## License

MIT License

Copyright (c) 2026 Awesome Grok Skills

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
