---
name: "Data Engineering Agent"
version: "2.0.0"
description: "Enterprise-grade data engineering agent for ETL/ELT pipelines, data warehousing, streaming architectures, data quality management, orchestration, and infrastructure as code."
author: "Awesome Grok Skills"
license: "MIT"
tags:
  - data-engineering
  - etl
  - elt
  - data-pipelines
  - data-quality
  - data-warehousing
  - streaming
  - kafka
  - schema-registry
  - data-catalog
  - lineage
  - infrastructure-as-code
  - terraform
  - orchestration
  - monitoring
category: "data-engineering"
personality: "data-engineer"
use_cases:
  - etl-pipeline-management
  - elt-pipeline-management
  - data-quality-assessment
  - data-warehousing
  - streaming-architecture
  - schema-management
  - data-catalog
  - data-lineage-tracking
  - infrastructure-as-code
  - pipeline-orchestration
  - monitoring-and-alerting
---

# Data Engineering Agent

> Enterprise data engineering with pipeline precision — from raw ingestion to curated analytics.

## Agent Identity

**Name:** Data Engineering Agent
**Role:** Senior Data Engineer and Pipeline Architect
**Expertise:** ETL/ELT design, data warehouse modeling, streaming systems, data quality, infrastructure automation
**Communication Style:** Technical, precise, methodical — prioritizes correctness and reliability

### Personality Traits

- **Reliable**: Every pipeline run is logged, tracked, and recoverable
- **Defensive**: Quality checks at every boundary; assume data will be malformed
- **Scalable**: Solutions designed for 10x current volume from day one
- **Observable**: If it can't be measured, it can't be improved
- **Automated**: Manual processes are bugs waiting to happen

---

## Core Principles

### 1. Schema-First Development

Always define data contracts before writing processing logic.

```python
# Define the schema first
schema = SchemaDefinition(
    name="user_events",
    columns=[
        ColumnDefinition(name="event_id", data_type="string", primary_key=True),
        ColumnDefinition(name="user_id", data_type="string", nullable=False),
        ColumnDefinition(name="event_type", data_type="string"),
        ColumnDefinition(name="timestamp", data_type="timestamp"),
        ColumnDefinition(name="payload", data_type="json"),
    ],
    partition_keys=["event_date"],
    compatibility=SchemaEvolutionStrategy.ADD_COLUMNS,
)

# Register before processing
agent.schema_registry.register_schema(schema)
```

### 2. Quality Gates at Every Boundary

Data must pass quality checks at ingestion, transformation, and loading.

```python
# Add checks at ingestion
agent.quality_manager.add_check("raw_events", QualityCheck(
    name="event_id_not_null",
    column="event_id",
    rule="NOT NULL",
    severity=Severity.CRITICAL,
))

# Add checks after transformation
agent.quality_manager.add_check("clean_events", QualityCheck(
    name="user_id_unique",
    column="user_id",
    rule="UNIQUE",
    severity=Severity.HIGH,
))
```

### 3. Idempotent Operations

Pipeline runs must be safe to retry without creating duplicates or data corruption.

### 4. Lineage by Default

Every data transformation automatically records lineage. No silent data movement.

### 5. Infrastructure as Code

All infrastructure is declarative, version-controlled, and reproducible.

---

## Capabilities

### 1. Pipeline Management

Create, execute, and monitor data pipelines with full lifecycle management.

```python
from agent import DataEngineeringAgent, PipelineType

agent = DataEngineeringAgent()

# Create an ETL pipeline
pipeline = agent.create_full_pipeline(
    name="daily_sales_etl",
    source={
        "type": "postgres",
        "connection": "prod_db",
        "query": "SELECT * FROM orders WHERE date >= CURRENT_DATE - 1",
    },
    transforms=[
        {"type": "filter", "column": "status", "op": "ne", "value": "cancelled"},
        {"type": "aggregate", "group_keys": ["product_id"], "aggregations": {"amount": "sum", "quantity": "sum"}},
        {"type": "rename", "renames": {"amount": "total_revenue", "quantity": "total_units"}},
    ],
    sink={"type": "bigquery", "table": "analytics.daily_sales", "write_mode": "overwrite"},
    pipeline_type=PipelineType.ETL,
)

# Execute the pipeline
run = agent.pipeline_manager.execute_pipeline(pipeline.pipeline_id)
print(f"Run ID: {run.run_id}")
print(f"Status: {run.status.value}")
print(f"Records loaded: {run.records_loaded}")
```

### 2. Data Quality Management

Profile datasets, run quality checks, and compute quality scores.

```python
from agent import QualityCheck, Severity

# Add quality checks
agent.quality_manager.add_check("customer_data", QualityCheck(
    name="email_format",
    column="email",
    rule="REGEX ^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$",
    severity=Severity.HIGH,
))

agent.quality_manager.add_check("customer_data", QualityCheck(
    name="age_range",
    column="age",
    rule="RANGE 0,120",
    severity=Severity.MEDIUM,
))

# Run checks on data
data = [
    {"email": "alice@example.com", "age": 30, "name": "Alice"},
    {"email": "bob@test.com", "age": 25, "name": "Bob"},
    {"email": "invalid", "age": 200, "name": "Charlie"},
]

results = agent.quality_manager.run_checks("customer_data", data)
score = agent.quality_manager.compute_quality_score(results)
print(f"Quality Score: {score}/100")

# Profile the dataset
profile = agent.quality_manager.profile_dataset(data)
for col, stats in profile["columns"].items():
    print(f"  {col}: {stats['type']}, nulls={stats['null_pct']}%")
```

### 3. ETL Orchestration

Schedule jobs with dependency resolution and DAG visualization.

```python
# Register jobs with dependencies
extract = agent.etl_orchestrator.register_job(
    job_name="extract_orders",
    schedule="0 2 * * *",
    timeout=3600,
)

transform = agent.etl_orchestrator.register_job(
    job_name="transform_orders",
    schedule="0 3 * * *",
    dependencies=[extract["job_id"]],
)

load = agent.etl_orchestrator.register_job(
    job_name="load_warehouse",
    schedule="0 4 * * *",
    dependencies=[transform["job_id"]],
)

# Execute with dependency resolution
result = agent.etl_orchestrator.execute_job(load["job_id"])
print(f"Steps completed: {len(result['steps'])}")

# Visualize the DAG
print(agent.etl_orchestrator.get_dag_visualization())
```

### 4. Data Warehouse Management

Manage warehouse tables, partitions, and storage optimization.

```python
from agent import WarehouseLayer, StorageFormat, SchemaDefinition, ColumnDefinition

# Create a schema
schema = SchemaDefinition(
    name="fact_orders",
    columns=[
        ColumnDefinition(name="order_id", data_type="VARCHAR(36)", primary_key=True),
        ColumnDefinition(name="customer_id", data_type="VARCHAR(36)", nullable=False),
        ColumnDefinition(name="order_date", data_type="DATE"),
        ColumnDefinition(name="amount", data_type="DECIMAL(10,2)"),
        ColumnDefinition(name="status", data_type="VARCHAR(20)"),
    ],
    partition_keys=["order_date"],
)

# Create table in curated layer
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

# Optimize table
agent.warehouse_manager.optimize_table(table["table_id"])
```

### 5. Data Lineage Tracking

Track upstream sources and downstream consumers for any data asset.

```python
from agent import LineageNode

# Register lineage nodes
source = LineageNode(
    node_id="raw_orders", name="raw.orders",
    node_type="table", metadata={"source": "postgres"},
)
clean = LineageNode(
    node_id="clean_orders", name="clean.orders",
    node_type="table", metadata={"transform": "cleaning"},
)
mart = LineageNode(
    node_id="mart_daily_sales", name="mart.daily_sales",
    node_type="table", metadata={"transform": "aggregation"},
)

agent.lineage_tracker.register_node(source)
agent.lineage_tracker.register_node(clean)
agent.lineage_tracker.register_node(mart)
agent.lineage_tracker.add_edge("raw_orders", "clean_orders")
agent.lineage_tracker.add_edge("clean_orders", "mart_daily_sales")

# Trace upstream
upstream = agent.lineage_tracker.get_upstream("mart_daily_sales")
print(f"Upstream sources: {[n.name for n in upstream]}")

# Impact analysis
impact = agent.lineage_tracker.get_impact_analysis("raw_orders")
print(f"Affected nodes: {impact['affected_nodes']}")
```

### 6. Streaming Management

Create topics, produce and consume messages with partition management.

```python
# Create a topic
topic = agent.streaming_manager.create_topic(
    name="user_events",
    partitions=6,
    replication_factor=3,
    retention_hours=168,
)

# Produce messages
agent.streaming_manager.produce(topic.topic_id, "evt_1", {
    "event_type": "page_view",
    "user_id": "u_123",
    "page": "/home",
    "timestamp": "2026-01-15T10:30:00Z",
})

agent.streaming_manager.produce(topic.topic_id, "evt_2", {
    "event_type": "click",
    "user_id": "u_456",
    "element": "buy_button",
    "timestamp": "2026-01-15T10:31:00Z",
})

# Consume messages
messages = agent.streaming_manager.consume(
    topic.topic_id, "analytics_consumer", max_messages=10
)
for msg in messages:
    print(f"Key: {msg['key']}, Partition: {msg['partition']}")
```

### 7. Schema Registry

Register, version, and validate schema compatibility.

```python
from agent import SchemaDefinition, ColumnDefinition, SchemaEvolutionStrategy

# Register a schema
schema_v1 = SchemaDefinition(
    name="user_profile",
    version=1,
    columns=[
        ColumnDefinition(name="user_id", data_type="string", primary_key=True),
        ColumnDefinition(name="email", data_type="string"),
        ColumnDefinition(name="created_at", data_type="timestamp"),
    ],
    compatibility=SchemaEvolutionStrategy.ADD_COLUMNS,
)
agent.schema_registry.register_schema(schema_v1)

# Register v2 with new columns (compatible)
schema_v2 = SchemaDefinition(
    name="user_profile",
    version=2,
    columns=[
        ColumnDefinition(name="user_id", data_type="string", primary_key=True),
        ColumnDefinition(name="email", data_type="string"),
        ColumnDefinition(name="created_at", data_type="timestamp"),
        ColumnDefinition(name="phone", data_type="string"),  # new column
    ],
    compatibility=SchemaEvolutionStrategy.ADD_COLUMNS,
)
result = agent.schema_registry.check_compatibility("user_profile", schema_v2)
print(f"Compatible: {result['compatible']}")
```

### 8. Data Catalog

Search, tag, and manage metadata for all data assets.

```python
from agent import CatalogEntry, CatalogEntryType

# Add catalog entries
agent.data_catalog.add_entry(CatalogEntry(
    name="daily_sales",
    entry_type=CatalogEntryType.TABLE,
    description="Aggregated daily sales by product",
    owner="analytics_team",
    tags=["sales", "daily", "curated"],
    location="bigquery://analytics.mart_daily_sales",
))

agent.data_catalog.add_entry(CatalogEntry(
    name="sales_dashboard",
    entry_type=CatalogEntryType.DASHBOARD,
    description="Executive sales overview dashboard",
    owner="bi_team",
    tags=["sales", "dashboard", "executive"],
))

# Search the catalog
results = agent.data_catalog.search("sales")
print(f"Found {len(results)} entries for 'sales'")

# Filter by tag
sales_tables = agent.data_catalog.get_entries_by_tag("sales")
print(f"Tables tagged 'sales': {len(sales_tables)}")
```

### 9. Infrastructure as Code

Generate Terraform and CloudFormation templates for data infrastructure.

```python
from agent import IaCTemplateType

# Define a data lake resource
s3_bucket = agent.iac_manager.define_resource(
    name="data_lake_raw",
    resource_type="aws_s3_bucket",
    template_type=IaCTemplateType.TERRAFORM,
    config={
        "bucket": "company-data-lake-raw",
        "versioning": {"enabled": True},
        "server_side_encryption_configuration": {
            "rule": {"apply_server_side_encryption_by_default": {"sse_algorithm": "AES256"}}
        },
    },
)

# Generate Terraform template
tf = agent.iac_manager.generate_template(s3_bucket.resource_id)
print(tf)

# Plan deployment
plan = agent.iac_manager.plan_deployment()
print(f"Resources to add: {plan['resources_to_add']}")
```

### 10. Monitoring & Alerting

Set up metrics collection and alert rules.

```python
from agent import AlertRule, Severity

# Add alert rules
agent.monitoring.add_alert_rule(AlertRule(
    name="high_pipeline_duration",
    metric="pipeline.duration_minutes",
    threshold=60,
    operator="gt",
    severity=Severity.HIGH,
    channels=["slack", "email"],
))

agent.monitoring.add_alert_rule(AlertRule(
    name="low_quality_score",
    metric="quality.customer_data",
    threshold=90,
    operator="lt",
    severity=Severity.MEDIUM,
    channels=["slack"],
))

# Record metrics
agent.monitoring.record_metric("pipeline.duration_minutes", 45)
agent.monitoring.record_metric("pipeline.duration_minutes", 75)  # triggers alert

# Check fired alerts
alerts = agent.monitoring.get_active_alerts()
print(f"Active alerts: {len(alerts)}")
```

---

## Method Signatures

### PipelineManager

```python
def create_pipeline(
    self,
    name: str,
    source_config: Dict[str, Any],
    transforms: List[Dict[str, Any]],
    sink_config: Dict[str, Any],
    pipeline_type: PipelineType = PipelineType.ETL,
    schedule: str = "0 * * * *",
    tags: Optional[List[str]] = None,
) -> PipelineConfig:
    """Create a new data pipeline configuration."""

def execute_pipeline(self, pipeline_id: str) -> PipelineRun:
    """Execute a pipeline and return the run result."""

def get_pipeline(self, pipeline_id: str) -> Optional[PipelineConfig]:
    """Retrieve a pipeline configuration by ID."""

def list_pipelines(
    self,
    pipeline_type: Optional[PipelineType] = None,
    tags: Optional[List[str]] = None,
) -> List[PipelineConfig]:
    """List all pipelines, optionally filtered."""

def delete_pipeline(self, pipeline_id: str) -> bool:
    """Delete a pipeline by ID."""

def get_pipeline_runs(self, pipeline_id: str) -> List[PipelineRun]:
    """Get execution history for a pipeline."""

def get_pipeline_health(self) -> Dict[str, Any]:
    """Get aggregate health metrics across all pipelines."""
```

### DataQualityManager

```python
def add_check(self, dataset: str, check: QualityCheck) -> QualityCheck:
    """Register a quality check for a dataset."""

def remove_check(self, dataset: str, check_id: str) -> bool:
    """Remove a quality check."""

def run_checks(self, dataset: str, data: List[Dict[str, Any]]) -> List[QualityResult]:
    """Run all checks for a dataset against provided data."""

def profile_dataset(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Profile a dataset, returning column-level statistics."""

def compute_quality_score(self, results: List[QualityResult]) -> float:
    """Compute weighted quality score from check results (0-100)."""

def get_quality_summary(self, dataset: str) -> Dict[str, Any]:
    """Get summary of quality status for a dataset."""
```

### ETLOrchestrator

```python
def register_job(
    self,
    job_name: str,
    schedule: str,
    dependencies: Optional[List[str]] = None,
    timeout: int = 3600,
    retry_count: int = 3,
) -> Dict[str, Any]:
    """Register an ETL job with scheduling."""

def resolve_dependencies(self, job_id: str) -> List[str]:
    """Return topologically sorted execution order."""

def execute_job(self, job_id: str) -> Dict[str, Any]:
    """Execute a job and all its dependencies."""

def get_dag_visualization(self) -> str:
    """Return ASCII DAG visualization."""

def monitor_jobs(self) -> Dict[str, Any]:
    """Get aggregate job monitoring stats."""
```

### DataWarehouseManager

```python
def create_table(
    self,
    name: str,
    layer: WarehouseLayer,
    schema: SchemaDefinition,
    partition_keys: Optional[List[str]] = None,
    storage_format: StorageFormat = StorageFormat.PARQUET,
) -> Dict[str, Any]:
    """Create a warehouse table definition."""

def drop_table(self, table_id: str) -> bool:
    """Drop a table by ID."""

def list_tables(self, layer: Optional[WarehouseLayer] = None) -> List[Dict[str, Any]]:
    """List tables, optionally filtered by layer."""

def get_storage_stats(self) -> Dict[str, Any]:
    """Get storage usage statistics."""

def optimize_table(self, table_id: str) -> Dict[str, Any]:
    """Run optimization (compaction, statistics) on a table."""

def generate_ddl(self, table_id: str) -> str:
    """Generate SQL DDL for a table."""
```

### SchemaRegistry

```python
def register_schema(self, schema: SchemaDefinition) -> SchemaDefinition:
    """Register a new schema version."""

def get_schema(self, name: str, version: Optional[int] = None) -> Optional[SchemaDefinition]:
    """Get a schema by name and optional version."""

def list_schemas(self) -> List[Dict[str, Any]]:
    """List all registered schemas."""

def check_compatibility(
    self, name: str, new_schema: SchemaDefinition
) -> Dict[str, Any]:
    """Check if a new schema is compatible with the existing one."""
```

---

## Usage Patterns

### Pattern 1: Batch ETL Pipeline

Best for: Daily/hourly data processing from source to warehouse.

```python
agent = DataEngineeringAgent()

# Step 1: Define schema
schema = SchemaDefinition(name="orders", columns=[
    ColumnDefinition(name="order_id", data_type="string", primary_key=True),
    ColumnDefinition(name="amount", data_type="decimal"),
    ColumnDefinition(name="status", data_type="string"),
])
agent.schema_registry.register_schema(schema)

# Step 2: Create pipeline with quality gates
pipeline = agent.create_full_pipeline(
    name="orders_etl",
    source={"type": "postgres", "query": "SELECT * FROM orders"},
    transforms=[
        {"type": "filter", "column": "status", "op": "ne", "value": "cancelled"},
        {"type": "aggregate", "group_keys": ["status"], "aggregations": {"amount": "sum"}},
    ],
    sink={"type": "bigquery", "table": "analytics.order_summary"},
)

# Step 3: Execute and monitor
run = agent.pipeline_manager.execute_pipeline(pipeline.pipeline_id)
assert run.status == PipelineStatus.SUCCESS
```

### Pattern 2: Streaming Pipeline

Best for: Real-time event processing with low latency.

```python
# Create topic
topic = agent.streaming_manager.create_topic("events", partitions=6)

# Produce events
for event in event_stream:
    agent.streaming_manager.produce(topic.topic_id, event["key"], event["data"])

# Consume and process
while True:
    messages = agent.streaming_manager.consume(topic.topic_id, "processor", 100)
    for msg in messages:
        process_event(msg["value"])
```

### Pattern 3: Data Quality Gate

Best for: Pre-load validation before data enters the warehouse.

```python
# Define quality rules
checks = [
    QualityCheck(name="not_null_pk", column="id", rule="NOT NULL", severity=Severity.CRITICAL),
    QualityCheck(name="valid_email", column="email", rule="REGEX ^.+@.+\\..+$", severity=Severity.HIGH),
    QualityCheck(name="amount_range", column="amount", rule="RANGE 0,1000000", severity=Severity.MEDIUM),
]
for check in checks:
    agent.quality_manager.add_check("incoming_data", check)

# Run before loading
results = agent.quality_manager.run_checks("incoming_data", raw_data)
score = agent.quality_manager.compute_quality_score(results)
if score >= 90:
    load_to_warehouse(raw_data)
else:
    alert_data_team(score)
```

### Pattern 4: Schema Evolution

Best for: Safely evolving data contracts over time.

```python
# Register initial schema
v1 = SchemaDefinition(name="users", columns=[
    ColumnDefinition(name="id", data_type="string"),
    ColumnDefinition(name="email", data_type="string"),
])
agent.schema_registry.register_schema(v1)

# Evolve schema (add columns)
v2 = SchemaDefinition(name="users", columns=[
    ColumnDefinition(name="id", data_type="string"),
    ColumnDefinition(name="email", data_type="string"),
    ColumnDefinition(name="phone", data_type="string"),
    ColumnDefinition(name="created_at", data_type="timestamp"),
])
result = agent.schema_registry.check_compatibility("users", v2)
if result["compatible"]:
    agent.schema_registry.register_schema(v2)
```

---

## Data Models

### PipelineConfig

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| pipeline_id | str | auto-generated | Unique pipeline identifier |
| name | str | required | Human-readable pipeline name |
| pipeline_type | PipelineType | ETL | Pipeline architecture pattern |
| source | Dict | {} | Source configuration (type, connection, query) |
| transforms | List[Dict] | [] | Ordered list of transformation configs |
| sink | Dict | {} | Sink configuration (type, table, write_mode) |
| schedule | str | "0 * * * *" | Cron schedule expression |
| retry_count | int | 3 | Number of retry attempts on failure |
| timeout_seconds | int | 3600 | Maximum execution time in seconds |
| enabled | bool | True | Whether the pipeline is active |
| tags | List[str] | [] | Tags for organization and filtering |

### QualityCheck

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| check_id | str | auto-generated | Unique check identifier |
| name | str | required | Human-readable check name |
| column | str | required | Column to check |
| rule | str | required | Rule expression (NOT NULL, UNIQUE, RANGE, REGEX) |
| severity | Severity | MEDIUM | Issue severity level |
| enabled | bool | True | Whether the check is active |
| description | str | "" | Optional description |

### SchemaDefinition

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| schema_id | str | auto-generated | Unique schema identifier |
| name | str | required | Schema name |
| version | int | 1 | Schema version number |
| columns | List[ColumnDefinition] | [] | Column definitions |
| partition_keys | List[str] | [] | Partition key columns |
| compatibility | SchemaEvolutionStrategy | ADD_COLUMNS | Schema evolution strategy |
| description | str | "" | Optional description |

### CatalogEntry

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| entry_id | str | auto-generated | Unique entry identifier |
| name | str | required | Asset name |
| entry_type | CatalogEntryType | TABLE | Type of data asset |
| description | str | "" | Asset description |
| owner | str | "" | Responsible team/person |
| tags | List[str] | [] | Discovery tags |
| schema | SchemaDefinition | None | Associated schema |
| location | str | "" | Physical location URI |
| access_level | str | "internal" | Access classification |

---

## Checklists

### New Pipeline Checklist

- [ ] Schema defined and registered in Schema Registry
- [ ] Source connection tested and accessible
- [ ] Quality checks defined for source data
- [ ] Transformations documented with expected input/output
- [ ] Sink table/view created in target layer
- [ ] Quality checks defined for transformed data
- [ ] Lineage nodes registered for upstream and downstream
- [ ] Catalog entry added with description, owner, and tags
- [ ] Alert rules configured for pipeline failures
- [ ] Retry and timeout configured appropriately
- [ ] Test run completed successfully
- [ ] Documentation updated

### Data Quality Checklist

- [ ] NOT NULL checks on primary keys and required fields
- [ ] UNIQUE checks on identifiers
- [ ] RANGE checks on numeric fields
- [ ] REGEX checks on formatted strings (email, phone, etc.)
- [ ] Cross-column consistency rules
- [ ] Freshness checks (data is recent enough)
- [ ] Volume checks (row count within expected range)
- [ ] Alert thresholds set for quality score degradation

### Production Deployment Checklist

- [ ] All infrastructure defined in IaC (Terraform/CloudFormation)
- [ ] Secrets stored in vault, not in code
- [ ] Monitoring dashboards created
- [ ] Alert rules configured and tested
- [ ] Runbooks documented for common failures
- [ ] Rollback procedure tested
- [ ] Performance baseline established
- [ ] Capacity plan reviewed

---

## Troubleshooting

### Pipeline Failures

**Symptom:** Pipeline status is FAILED with error_message.

**Steps:**
1. Check `run.error_message` for the specific failure
2. Review `run.stages` to identify which phase failed
3. Check source connectivity and permissions
4. Verify schema compatibility with `schema_registry.check_compatibility()`
5. Review quality check results if the failure is in the load phase
6. Check monitoring alerts for related infrastructure issues

### Quality Score Drops

**Symptom:** Quality score falls below threshold.

**Steps:**
1. Run `quality_manager.profile_dataset()` to identify anomalies
2. Compare with previous profile results
3. Check for upstream schema changes via `lineage_tracker.get_upstream()`
4. Review recent pipeline runs for data volume anomalies
5. Inspect specific failing checks via `quality_manager.get_quality_summary()`

### Schema Compatibility Issues

**Symptom:** `check_compatibility()` returns `compatible: false`.

**Steps:**
1. Review the `issues` list in the compatibility result
2. Check the schema's `compatibility` strategy setting
3. If using `ADD_COLUMNS` strategy, ensure new columns are additive only
4. If using `TYPE_PROMOTION` strategy, ensure type changes are compatible (int→long, float→double)
5. Consider bumping schema version and re-registering

### Pipeline Performance

**Symptom:** Pipeline duration exceeds SLA.

**Steps:**
1. Check `pipeline_health.avg_duration_seconds` trend
2. Review data volume trends (are inputs growing?)
3. Check system metrics (CPU, memory, I/O) during execution
4. Consider partitioning strategy for large datasets
5. Review transform complexity — can any be simplified?
6. Consider increasing parallelism or scaling resources

### Streaming Backlog

**Symptom:** Consumer lag increasing.

**Steps:**
1. Check `streaming_manager.get_topic_stats()` for buffer sizes
2. Verify consumer group is active and healthy
3. Check consumer processing throughput
4. Consider increasing consumer instances or partitions
5. Review message format changes that may slow deserialization

---

## Examples

### End-to-End Pipeline with Quality Gates

```python
from agent import (
    DataEngineeringAgent, PipelineType, QualityCheck, Severity,
    SchemaDefinition, ColumnDefinition, WarehouseLayer, StorageFormat,
    LineageNode, CatalogEntry, CatalogEntryType, AlertRule,
)

# Initialize the agent
agent = DataEngineeringAgent()

# 1. Define and register schema
schema = SchemaDefinition(name="fact_orders", columns=[
    ColumnDefinition(name="order_id", data_type="VARCHAR(36)", primary_key=True),
    ColumnDefinition(name="customer_id", data_type="VARCHAR(36)"),
    ColumnDefinition(name="product_id", data_type="VARCHAR(36)"),
    ColumnDefinition(name="quantity", data_type="INT"),
    ColumnDefinition(name="unit_price", data_type="DECIMAL(10,2)"),
    ColumnDefinition(name="order_date", data_type="DATE"),
    ColumnDefinition(name="status", data_type="VARCHAR(20)"),
], partition_keys=["order_date"])
agent.schema_registry.register_schema(schema)

# 2. Create warehouse table
table = agent.warehouse_manager.create_table(
    name="analytics.fact_orders",
    layer=WarehouseLayer.CURATED,
    schema=schema,
    partition_keys=["order_date"],
    storage_format=StorageFormat.PARQUET,
)

# 3. Add quality checks
for check in [
    QualityCheck(name="order_id_nn", column="order_id", rule="NOT NULL", severity=Severity.CRITICAL),
    QualityCheck(name="quantity_range", column="quantity", rule="RANGE 1,10000", severity=Severity.HIGH),
    QualityCheck(name="price_range", column="unit_price", rule="RANGE 0.01,99999.99", severity=Severity.HIGH),
]:
    agent.quality_manager.add_check("fact_orders", check)

# 4. Create and execute pipeline
pipeline = agent.create_full_pipeline(
    name="orders_to_warehouse",
    source={"type": "postgres", "query": "SELECT * FROM orders"},
    transforms=[
        {"type": "filter", "column": "status", "op": "in", "value": ["completed", "shipped"]},
        {"type": "rename", "renames": {"total": "unit_price"}},
    ],
    sink={"type": "warehouse", "table": "analytics.fact_orders", "mode": "append"},
    pipeline_type=PipelineType.ETL,
)

run = agent.pipeline_manager.execute_pipeline(pipeline.pipeline_id)
print(f"Pipeline: {run.status.value}, Records: {run.records_loaded}")

# 5. Run quality checks
sample_data = [
    {"order_id": "o1", "customer_id": "c1", "product_id": "p1", "quantity": 5, "unit_price": 29.99, "order_date": "2026-01-15", "status": "completed"},
    {"order_id": "o2", "customer_id": "c2", "product_id": "p2", "quantity": 1, "unit_price": 99.99, "order_date": "2026-01-15", "status": "shipped"},
]
qa = agent.run_quality_assessment("fact_orders", sample_data)
print(f"Quality: {qa['score']}/100 ({qa['level']})")

# 6. Set up monitoring
agent.monitoring.add_alert_rule(AlertRule(
    name="orders_pipeline_failure",
    metric="pipeline.runs_failed",
    threshold=1, operator="gt",
    severity=Severity.CRITICAL,
    channels=["slack", "pagerduty"],
))

# 7. Get full system status
status = agent.get_system_status()
for component, metrics in status["components"].items():
    print(f"  {component}: {metrics}")
```
