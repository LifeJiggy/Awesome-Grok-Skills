# Data Architecture Agent Architecture

## Overview

The Data Architecture Agent is a comprehensive data architecture design and management platform covering data modeling, integration pipelines, master data management, data catalog, quality monitoring, lineage tracking, governance, schema registry, partitioning, masking, dependency analysis, retention management, cost tracking, migration planning, and column-level lineage. This document details the complete system architecture with ASCII diagrams, component deep dives, data flows, design patterns, thread safety, performance targets, and configuration.

## System Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                        DataArchitectureAgent (Orchestrator)                           │
│                                                                                      │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐│
│  │                             Core Subsystems                                      ││
│  │                                                                                  ││
│  │  ┌────────────────┐  ┌──────────────────┐  ┌────────────────────────────┐       ││
│  │  │  Data Model    │  │  Integration     │  │  MDM                       │       ││
│  │  │  Manager       │  │  Manager         │  │  Manager                   │       ││
│  │  └───────┬────────┘  └────────┬─────────┘  └────────────┬───────────────┘       ││
│  │          │                    │                          │                       ││
│  │  ┌───────┴────────┐  ┌───────┴─────────┐  ┌────────────┴───────────────┐       ││
│  │  │  Tables &      │  │  Pipeline       │  │  Record Matching &         │       ││
│  │  │  Fields        │  │  Orchestration  │  │  Merging                   │       ││
│  │  └────────────────┘  └─────────────────┘  └────────────────────────────┘       ││
│  │                                                                                  ││
│  │  ┌────────────────┐  ┌──────────────────┐  ┌────────────────────────────┐       ││
│  │  │  Data Catalog  │  │  Data Quality    │  │  Data Lineage              │       ││
│  │  │                │  │  Manager         │  │  (Table + Column Level)    │       ││
│  │  └───────┬────────┘  └────────┬─────────┘  └────────────┬───────────────┘       ││
│  │          │                    │                          │                       ││
│  │  ┌───────┴────────┐  ┌───────┴─────────┐  ┌────────────┴───────────────┐       ││
│  │  │  Metadata      │  │  Quality Rules  │  │  Impact Analysis           │       ││
│  │  │  Search Index  │  │  & Checks       │  │  & Dependencies            │       ││
│  │  └────────────────┘  └─────────────────┘  └────────────────────────────┘       ││
│  │                                                                                  ││
│  │  ┌────────────────┐  ┌──────────────────┐  ┌────────────────────────────┐       ││
│  │  │  Governance    │  │  Schema          │  │  Data Partitioner          │       ││
│  │  │  Manager       │  │  Registry        │  │                            │       ││
│  │  └────────────────┘  └──────────────────┘  └────────────────────────────┘       ││
│  │                                                                                  ││
│  │  ┌────────────────┐  ┌──────────────────┐  ┌────────────────────────────┐       ││
│  │  │  Masking       │  │  Dependency      │  │  Retention Manager         │       ││
│  │  │  Engine        │  │  Graph Builder   │  │                            │       ││
│  │  └────────────────┘  └──────────────────┘  └────────────────────────────┘       ││
│  │                                                                                  ││
│  │  ┌────────────────┐  ┌──────────────────┐  ┌────────────────────────────┐       ││
│  │  │  Cost          │  │  Migration       │  │  Column Lineage            │       ││
│  │  │  Tracker       │  │  Planner         │  │  Tracker                   │       ││
│  │  └────────────────┘  └──────────────────┘  └────────────────────────────┘       ││
│  └──────────────────────────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────────────────────────┘
```

## Component Deep Dives

### 1. Data Model Manager

Manages conceptual, logical, and physical data models with tables, fields, schema evolution, PII detection, and table cloning.

```
┌─────────────────────────────────────────────────────────┐
│              DataModelManager                            │
│                                                          │
│  Model Hierarchy:                                       │
│  Model                                                   │
│  ├── Table 1                                            │
│  │   ├── Field 1 (PK, UUID, NOT NULL, PII: true)      │
│  │   ├── Field 2 (STRING, max_length=255, MASKING)     │
│  │   ├── Field 3 (DATETIME)                             │
│  │   └── Partition Config (HASH, 8 partitions)         │
│  ├── Table 2                                            │
│  │   └── Fields...                                      │
│  └── Relationships                                      │
│                                                          │
│  Model Types:                                           │
│  - CONCEPTUAL: high-level entities                      │
│  - LOGICAL: detailed with attributes                    │
│  - PHYSICAL: storage-specific implementation            │
│  - SEMANTIC: business-meaningful views                  │
│                                                          │
│  Schema Evolution Tracking:                             │
│  - ADD_COLUMN, DROP_COLUMN, RENAME_COLUMN               │
│  - CHANGE_TYPE, ADD_TABLE, DROP_TABLE                   │
│  - Each change recorded with rollback SQL & breaking    │
│    change flag                                          │
│                                                          │
│  Operations:                                            │
│  - create_model, update_model, delete_model             │
│  - create_table, add_field, remove_field                │
│  - search_tables, get_tables_by_domain/storage          │
│  - clone_table, calculate_table_size                    │
│  - get_pii_fields, get_model_summary                    │
└─────────────────────────────────────────────────────────┘
```

**Data Type Reference:**

| Type | Size (bytes) | Description |
|------|-------------|-------------|
| STRING | 256 | Variable-length text |
| INTEGER | 4 | 32-bit integer |
| FLOAT | 8 | 64-bit float |
| BOOLEAN | 1 | True/False |
| DATE | 4 | Date only |
| DATETIME | 8 | Date + Time |
| TIMESTAMP | 8 | UTC timestamp |
| UUID | 16 | Universally unique |
| DECIMAL | 16 | Exact numeric |
| JSON | 4096 | Semi-structured |
| TEXT | 65536 | Long text |
| BLOB | 1048576 | Binary data |

### 2. Integration Manager

Manages data integration pipelines across ETL, ELT, CDC, streaming, and batch patterns with pipeline lifecycle, alerts, and P95 metrics.

```
┌─────────────────────────────────────────────────────────┐
│           IntegrationManager                             │
│                                                          │
│  Integration Patterns:                                  │
│  ┌──────────────────────────────────────────────┐       │
│  │ ETL: Extract -> Transform -> Load              │       │
│  │ ELT: Extract -> Load -> Transform              │       │
│  │ CDC: Change Data Capture (real-time)           │       │
│  │ API_SYNC: REST/GraphQL synchronization         │       │
│  │ STREAMING: Kafka/Pulsar real-time              │       │
│  │ BATCH: Scheduled bulk transfers                │       │
│  │ FILE_TRANSFER: SFTP/CSV processing             │       │
│  │ EVENT_DRIVEN: Event-based triggers             │       │
│  └──────────────────────────────────────────────┘       │
│                                                          │
│  Pipeline Lifecycle:                                    │
│  created -> active -> paused -> active                   │
│         \-> failed -> active                            │
│                                                          │
│  Metrics:                                               │
│  - total_runs, success_rate, p95_duration               │
│  - avg_duration, total_records, total_bytes             │
│  - throughput_records_per_sec                           │
│  - error_count, last_status                             │
│                                                          │
│  Alerts:                                                │
│  - On failure notification                              │
│  - Configurable alert_on_failure flag                   │
│  - Alert history with clear/alerts endpoint             │
└─────────────────────────────────────────────────────────┘
```

### 3. MDM Manager

Master Data Management for creating golden records, matching, merging with survivorship rules, and fuzzy matching.

```
┌─────────────────────────────────────────────────────────┐
│              MDMManager                                  │
│                                                          │
│  Record Structure:                                      │
│  ┌──────────────────────────────────────────────┐       │
│  │ MasterDataRecord                              │       │
│  │ ├── record_id (unique)                        │       │
│  │ ├── golden_id (G_{type}_{id})                 │       │
│  │ ├── entity_type (customer, product, etc.)     │       │
│  │ ├── source_ids (list of source references)    │       │
│  │ ├── attributes (key-value pairs)              │       │
│  │ ├── confidence_score (0.0 - 1.0)             │       │
│  │ ├── quality_score (0.0 - 1.0)                │       │
│  │ └── last_merged timestamp                     │       │
│  └──────────────────────────────────────────────┘       │
│                                                          │
│  Merge Strategies:                                      │
│  - r1_priority: record 1 wins on conflict               │
│  - r2_priority: record 2 wins on conflict               │
│  - latest_wins: most recently merged wins                │
│  - highest_quality: highest quality_score wins           │
│                                                          │
│  Survivorship Rules:                                    │
│  - Per-entity, per-field rules                          │
│  - Uppercase, trim, custom transforms                   │
│                                                          │
│  Matching:                                              │
│  - Exact match on specified fields                      │
│  - Fuzzy match with Jaccard similarity                  │
│  - Duplicate detection by field value                   │
└─────────────────────────────────────────────────────────┘
```

### 4. Data Catalog

Metadata management with full-text search, entity discovery, auto-discovery, and search index.

```
┌─────────────────────────────────────────────────────────┐
│              DataCatalog                                 │
│                                                          │
│  Metadata Storage:                                      │
│  {entity_type}_{entity_id}_{key}: value                 │
│                                                          │
│  Search Index:                                          │
│  token -> set of matching entry_ids                     │
│                                                          │
│  Search Process:                                        │
│  1. Tokenize query                                      │
│  2. Intersect matching sets (AND semantics)             │
│  3. Filter by entity_type if specified                  │
│  4. Return up to max_results                            │
│                                                          │
│  Auto-Discovery:                                        │
│  - Scans tables for missing schema metadata             │
│  - Creates metadata entries automatically               │
│                                                          │
│  CRUD:                                                  │
│  - add_metadata, update_metadata, delete_metadata       │
│  - search, get_entity_metadata, get_all_metadata        │
└─────────────────────────────────────────────────────────┘
```

### 5. Data Quality Manager

Configurable quality rules with automated checking, dashboards, score history, and severity-based filtering.

```
┌─────────────────────────────────────────────────────────┐
│          DataQualityManager                              │
│                                                          │
│  Rule Types:                                            │
│  ┌──────────────────┬──────────────┐                    │
│  │ Rule Type        │ Default Thresh│                    │
│  ├──────────────────┼──────────────┤                    │
│  │ NOT_NULL         │ 100%         │                    │
│  │ UNIQUE           │ 100%         │                    │
│  │ RANGE_CHECK      │ 99%          │                    │
│  │ PATTERN_MATCH    │ 99.5%        │                    │
│  │ REFERENTIAL_INT  │ 100%         │                    │
│  │ FRESHNESS        │ 99%          │                    │
│  │ COMPLETENESS     │ 95%          │                    │
│  │ CONSISTENCY      │ 98%          │                    │
│  │ ACCURACY         │ 99%          │                    │
│  └──────────────────┴──────────────┘                    │
│                                                          │
│  Severity Levels:                                       │
│  - critical: immediate attention                        │
│  - warning: investigate soon                            │
│  - info: informational                                  │
│                                                          │
│  Dashboard:                                             │
│  total_rules | passing | failing | not_checked          │
│  pass_rate = passing / total                            │
│  by_type: {rule_type: {passing, failing}}               │
│                                                          │
│  Score History:                                         │
│  [{timestamp, total, passing, score}]                   │
│  Enables trend analysis over time                       │
│                                                          │
│  Check Results:                                         │
│  [{rule_id, passed, actual, threshold,                  │
│    duration_ms, records_scanned, violations_found}]     │
└─────────────────────────────────────────────────────────┘
```

### 6. Data Lineage (Table + Column Level)

Tracks data flow from source to destination through transformations at both table and column level.

```
┌─────────────────────────────────────────────────────────┐
│              DataLineage                                 │
│                                                          │
│  Node Types:                                            │
│  - SOURCE: original data source                         │
│  - TRANSFORMATION: data processing step                 │
│  - DESTINATION: target table/view                       │
│  - QUALITY_CHECK: data validation step                  │
│  - AGGREGATION: summarization                           │
│  - FILTER: row selection                                │
│  - JOIN: table combination                              │
│  - LOOKUP: reference data enrichment                    │
│                                                          │
│  Graph Structure:                                       │
│  Nodes: {id: LineageNode}                               │
│  Edges: [{source, target, type, weight}]                │
│                                                          │
│  Operations:                                            │
│  - add_node, remove_node                                │
│  - add_edge, remove_edge                                │
│  - get_upstream, get_downstream (BFS, depth-limited)    │
│  - get_impact_analysis (full upstream/downstream)       │
│  - get_shortest_path (BFS pathfinding)                  │
│  - get_nodes_by_type, get_lineage_stats                 │
│                                                          │
│  Column Lineage:                                        │
│  - Per-column upstream/downstream tracing               │
│  - Full path trace with transformations                 │
│  - Source/target column indexing                        │
└─────────────────────────────────────────────────────────┘
```

### 7. Governance Manager

Policies, audit logging, compliance tracking, and enforcement levels.

```
┌─────────────────────────────────────────────────────────┐
│           GovernanceManager                              │
│                                                          │
│  Policy Types:                                          │
│  - DATA_CLASSIFICATION: sensitivity levels              │
│  - ACCESS_CONTROL: who can access what                  │
│  - RETENTION: data lifecycle policies                   │
│  - ENCRYPTION: encryption requirements                  │
│  - MASKING: PII/anonymization rules                     │
│  - AUDIT_LOGGING: access/change tracking                │
│  - COMPLIANCE: regulatory requirements                  │
│  - QUALITY_STANDARD: minimum quality levels             │
│                                                          │
│  Enforcement Levels:                                    │
│  - advisory: guidelines, no blocking                    │
│  - mandatory: must comply                               │
│  - enforced: actively blocks non-compliance             │
│                                                          │
│  Audit Log:                                             │
│  [{event_id, event_type, entity, user, ip_address,      │
│    timestamp}]                                          │
│  Max 10000 entries with automatic rotation              │
│                                                          │
│  Compliance:                                            │
│  - Per-policy compliance checks                         │
│  - Compliance rate calculation                          │
│  - Compliance history tracking                          │
└─────────────────────────────────────────────────────────┘
```

### 8. Schema Registry

Version-controlled schema management with compatibility checks and evolution tracking.

```
┌─────────────────────────────────────────────────────────┐
│              SchemaRegistry                              │
│                                                          │
│  Version Management:                                    │
│  table_id -> [SchemaVersion v1, v2, v3, ...]           │
│                                                          │
│  Compatibility Check:                                   │
│  1. Compare new schema fields to latest version         │
│  2. Detect added, removed, modified fields              │
│  3. Backward-compatible = no removals, no changes       │
│  4. Returns detailed diff                               │
│                                                          │
│  Schema Evolution:                                      │
│  - Supports ADD_COLUMN, DROP_COLUMN, RENAME_COLUMN      │
│  - CHANGE_TYPE for field type changes                   │
│  - Auto-creates breaking_change flag                    │
│  - Records SchemaChange with rollback info              │
│                                                          │
│  Schema Diff:                                           │
│  - Compare any two versions                             │
│  - Shows added, removed, common fields                  │
└─────────────────────────────────────────────────────────┘
```

### 9. Data Partitioner

Configurable data partitioning with hash, range, time-interval, and list strategies.

```
┌─────────────────────────────────────────────────────────┐
│              DataPartitioner                             │
│                                                          │
│  Partition Strategies:                                  │
│  - HASH: hash(key) % partition_count                    │
│  - RANGE: key % partition_count                         │
│  - TIME_INTERVAL: time() // 86400 % count               │
│  - LIST: lookup table mapping                           │
│  - GEOGRAPHIC: region-based                             │
│  - DIRECTORY: file-system based                         │
│                                                          │
│  Partition Config:                                      │
│  {table_id, strategy, column, count, interval}          │
│                                                          │
│  Partition State:                                       │
│  - Per-partition row count and size                     │
│  - Compression status                                   │
│  - Location tracking                                    │
│                                                          │
│  Stats:                                                 │
│  - Total rows, total size                               │
│  - Average rows/size per partition                      │
└─────────────────────────────────────────────────────────┘
```

### 10. Data Masking Engine

PII protection through configurable masking rules with multiple strategies.

```
┌─────────────────────────────────────────────────────────┐
│              DataMaskingEngine                           │
│                                                          │
│  Masking Types:                                         │
│  - FULL_REDACT: replace entire value with ***           │
│  - PARTIAL: keep first 2, last 2 chars                  │
│  - HASH: SHA-256 hash with optional salt                │
│  - TOKENIZE: deterministic token replacement            │
│  - SHUFFLE: random character reorder                    │
│  - DATE_SHIFT: random date offset                       │
│  - NULL_OUT: replace with None                          │
│  - FORMAT_PRESERVING: maintain structure                │
│                                                          │
│  Rule Structure:                                        │
│  {table_id, field_id, masking_type, pattern, salt}      │
│                                                          │
│  Application:                                           │
│  - Apply rules per-table to records                     │
│  - Tracking of all masking applications                 │
│  - Stats by masking type                                │
└─────────────────────────────────────────────────────────┘
```

### 11. Dependency Graph Builder

Models relationships between data assets with topological sorting and critical path analysis.

```
┌─────────────────────────────────────────────────────────┐
│          DependencyGraphBuilder                          │
│                                                          │
│  Node Types:                                            │
│  - TABLE_DEPENDS_ON                                     │
│  - PIPELINE_FEEDS                                       │
│  - QUALITY_RULE_CHECKS                                  │
│  - GOVERNANCE_POLICY_APPLIES                            │
│  - SCHEMA_OWNED_BY                                      │
│  - DOMAIN_CONTAINS                                      │
│                                                          │
│  Graph Representation:                                  │
│  - Forward adjacency: source -> {targets}               │
│  - Reverse adjacency: target -> {sources}               │
│  - Bidirectional traversal                              │
│                                                          │
│  Operations:                                            │
│  - add_node, add_dependency, remove_dependency          │
│  - get_dependents, get_dependencies                     │
│  - topological_sort (DAG ordering)                      │
│  - get_critical_path (longest path through DAG)         │
└─────────────────────────────────────────────────────────┘
```

### 12. Data Retention Manager

Automated data lifecycle management with configurable actions and scheduling.

```
┌─────────────────────────────────────────────────────────┐
│          DataRetentionManager                            │
│                                                          │
│  Retention Actions:                                     │
│  - DELETE: permanent removal                            │
│  - ARCHIVE: move to archive storage                     │
│  - COMPRESS: reduce storage footprint                   │
│  - MOVE_TO_COLD: move to cold storage                   │
│  - KEEP_FOREVER: exempt from retention                  │
│  - ANONYMIZE: strip PII but keep data                   │
│                                                          │
│  Rule Structure:                                        │
│  {table_id, action, retention_days, criteria,           │
│   next_scheduled, last_executed}                        │
│                                                          │
│  Scheduling:                                            │
│  - Automatic next_scheduled calculation                 │
│  - get_due_rules for execution                          │
│  - Execution log with affected row counts               │
└─────────────────────────────────────────────────────────┘
```

### 13. Cost Tracker

Tracks infrastructure and operational costs with budget management.

```
┌─────────────────────────────────────────────────────────┐
│              CostTracker                                 │
│                                                          │
│  Cost Categories:                                       │
│  - COMPUTE: processing costs                            │
│  - STORAGE: data storage costs                          │
│  - NETWORK: data transfer costs                         │
│  - QUERY: query execution costs                         │
│  - BACKUP: backup and recovery costs                    │
│  - LICENSE: software license costs                      │
│  - TRANSFORMATION: ETL/ELT costs                        │
│  - MONITORING: observability costs                      │
│                                                          │
│  Budget Management:                                     │
│  - Per-category budget setting                          │
│  - Utilization tracking                                 │
│  - Remaining budget calculation                         │
│                                                          │
│  Reporting:                                             │
│  - Total cost, cost by category                         │
│  - Cost by resource                                     │
│  - Budget status with utilization %                     │
└─────────────────────────────────────────────────────────┘
```

### 14. Data Migration Planner

Plans and tracks data migrations between systems.

```
┌─────────────────────────────────────────────────────────┐
│          DataMigrationPlanner                            │
│                                                          │
│  Migration States:                                      │
│  PLANNED -> IN_PROGRESS -> COMPLETED                    │
│            \-> FAILED -> ROLLED_BACK                    │
│            \-> PAUSED -> IN_PROGRESS                    │
│                                                          │
│  Plan Structure:                                        │
│  {source_system, target_system, tables,                 │
│   estimated_duration, actual_duration,                  │
│   rows_migrated, rows_total, errors}                    │
│                                                          │
│  Operations:                                            │
│  - create_plan, start_migration                         │
│  - complete_migration, fail_migration                   │
│  - rollback_migration                                   │
│  - get_plans_by_status, get_migration_stats             │
└─────────────────────────────────────────────────────────┘
```

### 15. Column Lineage Tracker

Tracks column-level data flow between tables with transformation details.

```
┌─────────────────────────────────────────────────────────┐
│          ColumnLineageTracker                            │
│                                                          │
│  Lineage Structure:                                     │
│  {source_table, source_column,                          │
│   target_table, target_column, transformation}          │
│                                                          │
│  Indexing:                                              │
│  - By target column: table.column -> [lineage_ids]      │
│  - By source column: table.column -> [lineage_ids]      │
│                                                          │
│  Operations:                                            │
│  - add_column_lineage                                   │
│  - get_column_upstream (what feeds this column)         │
│  - get_column_downstream (what this feeds)              │
│  - trace_full_path (multi-hop column tracing)           │
│  - delete_lineage                                       │
│                                                          │
│  Stats:                                                 │
│  - unique source/target columns                         │
│  - avg transformations per target                       │
└─────────────────────────────────────────────────────────┘
```

## Data Flow Diagrams

### Data Modeling Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Design  │────>│  Create      │────>│  Add Fields  │
│  Model   │     │  Tables      │     │  & Types     │
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
                   ┌──────────────┐     ┌────v───────┐
                   │  Track       │<────│  Record    │
                   │  Changes     │     │  Schema    │
                   └──────────────┘     └────────────┘
```

### Integration Pipeline Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Define  │────>│  Configure   │────>│  Schedule    │
│  Pipeline│     │  Source/Dest │     │  & Execute   │
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
                   ┌──────────────┐     ┌────v───────┐
                   │  Monitor     │<────│  Run       │
                   │  Metrics     │     │  Pipeline  │
                   └──────┬───────┘     └────────────┘
                          │
                   ┌──────v───────┐
                   │  Alert on    │
                   │  Failures    │
                   └──────────────┘
```

### Quality Check Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Define  │────>│  Execute     │────>│  Record      │
│  Rules   │     │  Checks      │     │  Results     │
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
                   ┌──────────────┐     ┌────v───────┐
                   │  Alert on    │<────│  Update     │
                   │  Failures    │     │  Dashboard  │
                   └──────────────┘     └────────────┘
```

### Schema Evolution Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Current │────>│  Check       │────>│  Apply       │
│  Schema  │     │  Compat.     │     │  Change      │
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
                   ┌──────────────┐     ┌────v───────┐
                   │  Register    │<────│  Record     │
                   │  New Version │     │  Change     │
                   └──────────────┘     └────────────┘
```

### Column Lineage Tracing Flow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Target      │────>│  Look Up     │────>│  Follow      │
│  Column      │     │  Lineage     │     │  Transforms  │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                 │
                   ┌──────────────┐     ┌────────v──────┐
                   │  Return      │<────│  Trace        │
                   │  Full Path   │     │  Upstream     │
                   └──────────────┘     └───────────────┘
```

## Design Patterns

### 1. Registry Pattern
All entities (models, tables, pipelines, rules, schemas, partitions, masks, dependencies, retention, costs, migrations) use dictionary-based registries with unique IDs for O(1) lookup.

### 2. Graph Pattern
Data lineage uses directed graph with nodes and edges for upstream/downstream traversal. Dependency graph uses adjacency lists with reverse adjacency for bidirectional queries.

### 3. Observer Pattern
Quality checks and pipeline runs notify systems of failures through alerts. Governance compliance checks trigger audit events.

### 4. State Machine
Pipeline status follows defined state transitions: created -> active -> paused -> active. Migration plans follow: PLANNED -> IN_PROGRESS -> COMPLETED/FAILED/ROLLED_BACK.

### 5. Strategy Pattern
Integration patterns (ETL, ELT, CDC) implement different strategies. Partition strategies (HASH, RANGE, TIME_INTERVAL) provide different partitioning logic. Masking types (FULL_REDACT, HASH, TOKENIZE) implement different protection strategies.

### 6. Version Pattern
Schema registry maintains version history for each table. Each schema change creates a new version with compatibility checking against the previous version.

### 7. Index Pattern
Data catalog uses inverted index for search. Column lineage tracker maintains dual indexes (by-source, by-target) for efficient traversal.

## Thread Safety

All managers use `threading.Lock()` for thread-safe operations:

| Manager | Lock Scope |
|---------|-----------|
| DataModelManager | Models, tables, schema changes, version history |
| IntegrationManager | Pipelines, run history, alerts |
| MDMManager | Records, entity indices, match history, survivorship rules |
| DataCatalog | Metadata entries, search index, lineage entries |
| DataQualityManager | Rules, results, score history |
| DataLineage | Nodes, edges |
| GovernanceManager | Policies, audit log, compliance checks |
| SchemaRegistry | Version registry, compatibility cache |
| DataPartitioner | Configs, partitions |
| DataMaskingEngine | Rules, masking history |
| DependencyGraphBuilder | Nodes, adjacency lists |
| DataRetentionManager | Records, execution log |
| CostTracker | Entries, budgets |
| DataMigrationPlanner | Plans, step log |
| ColumnLineageTracker | Lineages, by-source index, by-target index |

**Lock acquisition order:** Always acquire locks in the same order across managers to prevent deadlocks. The agent orchestrator acquires locks implicitly through manager methods.

## Performance Targets

| Operation | Target | Current |
|-----------|--------|---------|
| Model Create | < 50ms | ~10ms |
| Table Create | < 30ms | ~8ms |
| Pipeline Run | < 1s | ~500ms |
| Quality Check | < 200ms | ~50ms |
| Lineage Query | < 300ms | ~80ms |
| Catalog Search | < 100ms | ~25ms |
| Schema Compatibility Check | < 100ms | ~15ms |
| Partition Compute | < 5ms | ~1ms |
| Masking Apply | < 50ms | ~10ms |
| Dependency Topo Sort | < 500ms | ~200ms |
| Column Lineage Trace | < 200ms | ~60ms |
| Cost Aggregation | < 100ms | ~30ms |
| Migration Plan Create | < 50ms | ~12ms |

## Configuration

```yaml
agent:
  default_storage: relational_db
  quality_check_interval: daily
  lineage_depth: 20
  enable_cdc: true
  enable_column_lineage: true
  enable_cost_tracking: true
  enable_partitioning: true
  enable_masking: true
  enable_retention: true
  enable_schema_registry: true
  enable_dependency_graph: true
  enable_migration_planner: true

thresholds:
  quality:
    NOT_NULL: 100.0
    UNIQUE: 100.0
    RANGE_CHECK: 99.0
    PATTERN_MATCH: 99.5
    REFERENTIAL_INTEGRITY: 100.0
    FRESHNESS: 99.0
    COMPLETENESS: 95.0
    CONSISTENCY: 98.0
    ACCURACY: 99.0

limits:
  max_lineage_depth: 20
  max_catalog_search_results: 100
  max_audit_log_entries: 10000
  default_partition_count: 16
```

## Module Dependencies

```
DataArchitectureAgent
    |
    ├── DataModelManager
    |       └── SchemaRegistry (reads tables from model_manager)
    |
    ├── IntegrationManager
    |       └── (standalone, uses pipeline registry)
    |
    ├── MDMManager
    |       └── (standalone, uses entity indices)
    |
    ├── DataCatalog
    |       └── (reads tables from model_manager for auto_discover)
    |
    ├── DataQualityManager
    |       └── (standalone, uses rule registry)
    |
    ├── DataLineage
    |       └── (standalone, uses node/edge graphs)
    |
    ├── GovernanceManager
    |       └── (standalone, uses policy registry + audit log)
    |
    ├── DataPartitioner
    |       └── (standalone, uses config + partition registry)
    |
    ├── DataMaskingEngine
    |       └── (standalone, uses rule registry)
    |
    ├── DependencyGraphBuilder
    |       └── (standalone, uses adjacency lists)
    |
    ├── DataRetentionManager
    |       └── (standalone, uses retention record registry)
    |
    ├── CostTracker
    |       └── (standalone, uses entry list + budgets)
    |
    ├── DataMigrationPlanner
    |       └── (standalone, uses plan registry)
    |
    └── ColumnLineageTracker
            └── (standalone, uses dual-index lineage registry)
```

## Error Hierarchy

```
DataArchitectureError (base)
    ├── ModelError
    ├── IntegrationError
    ├── QualityError
    ├── GovernanceError
    ├── SchemaError
    ├── SchemaRegistryError
    ├── PartitionError
    ├── MaskingError
    ├── DependencyError
    ├── RetentionError
    ├── CostTrackingError
    ├── MigrationError
    └── LineageError
```

Each subsystem raises its own typed exception for targeted error handling. The agent orchestrator catches `DataArchitectureError` for unified error management.
