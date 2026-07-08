# Data Engineering Agent — System Architecture

## Table of Contents

1. [Overview](#overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Component Deep Dives](#component-deep-dives)
4. [Data Flow](#data-flow)
5. [Design Patterns](#design-patterns)
6. [Tech Stack](#tech-stack)
7. [Security Architecture](#security-architecture)
8. [Scalability Patterns](#scalability-patterns)
9. [Deployment Topology](#deployment-topology)
10. [Data Lineage Architecture](#data-lineage-architecture)
11. [Streaming Architecture](#streaming-architecture)
12. [Monitoring & Observability](#monitoring--observability)
13. [Data Quality Framework](#data-quality-framework)
14. [Schema Management](#schema-management)
15. [Infrastructure as Code Patterns](#infrastructure-as-code-patterns)
16. [Performance Engineering](#performance-engineering)
17. [Disaster Recovery](#disaster-recovery)
18. [Appendix](#appendix)

---

## Overview

The Data Engineering Agent is a modular, composable system designed for enterprise-scale data pipeline orchestration, ETL/ELT processing, data warehousing, streaming, quality management, and infrastructure as code. It follows a layered architecture with clear separation of concerns, enabling independent scaling and evolution of each component.

### Core Design Principles

- **Modularity**: Each component is self-contained with a well-defined interface
- **Composability**: Components can be combined in arbitrary configurations
- **Observability**: Every operation is logged, metricated, and traceable
- **Idempotency**: Pipeline runs are safe to retry without side effects
- **Schema-first**: All data contracts are defined and validated before processing
- **Infrastructure as Code**: All infrastructure is declarative, version-controlled, and reproducible
- **Defense in Depth**: Quality checks at every data boundary
- **Zero-Trust Networking**: All inter-component communication is authenticated

### System Boundaries

```
┌─────────────────────────────────────────────────────────────────────┐
│                        External Systems                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐│
│  │  RDBMS  │  │  Cloud  │  │   API   │  │  Files  │  │ Message ││
│  │ Sources │  │ Storage │  │ Sources │  │  (CSV)  │  │  Queues ││
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘│
│       │            │            │            │            │      │
├───────┴────────────┴────────────┴────────────┴────────────┴──────┤
│                    DataEngineeringAgent                            │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    Ingestion Layer                           │ │
│  │  • Source adapters  • Schema validation  • Format detection │ │
│  └───────────────────────────┬─────────────────────────────────┘ │
│                              │                                     │
│  ┌───────────────────────────┴─────────────────────────────────┐ │
│  │                    Processing Layer                          │ │
│  │  • Transform engine  • Quality checks  • Lineage tracking   │ │
│  └───────────────────────────┬─────────────────────────────────┘ │
│                              │                                     │
│  ┌───────────────────────────┴─────────────────────────────────┐ │
│  │                    Storage Layer                             │ │
│  │  • Warehouse tables  • Schema registry  • Data catalog      │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DataEngineeringAgent (Orchestrator)                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Pipeline    │  │    Data      │  │     ETL      │  │   Warehouse  │  │
│  │   Manager     │  │   Quality    │  │ Orchestrator │  │   Manager    │  │
│  │              │  │   Manager    │  │              │  │              │  │
│  │ • Create     │  │ • Checks     │  │ • Schedule   │  │ • Tables     │  │
│  │ • Execute    │  │ • Profile    │  │ • DAG        │  │ • Partitions │  │
│  │ • Monitor    │  │ • Score      │  │ • Retry      │  │ • Optimize   │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                 │                 │           │
│  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐  │
│  │   Lineage    │  │  Streaming   │  │   Schema     │  │     Data     │  │
│  │   Tracker    │  │   Manager    │  │  Registry    │  │   Catalog    │  │
│  │              │  │              │  │              │  │              │  │
│  │ • DAG        │  │ • Topics     │  │ • Versions   │  │ • Search     │  │
│  │ • Impact     │  │ • Produce    │  │ • Compatible │  │ • Tags       │  │
│  │ • Visualize  │  │ • Consume    │  │ • Validate   │  │ • Owners     │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                 │                 │           │
│  ┌──────┴───────┐  ┌──────┴───────────────────────────────────┴───────┐  │
│  │    IaC       │  │              Monitoring & Alerting                │  │
│  │   Manager    │  │                                                   │  │
│  │              │  │  • Metrics Collection   • Alert Rules             │  │
│  │ • Terraform  │  │  • Health Checks        • Notification            │  │
│  │ • CFN/Pulumi │  │  • SLA Monitoring       • Dashboard              │  │
│  └──────────────┘  └───────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Interaction Summary

| Component | Role | Input | Output |
|-----------|------|-------|--------|
| PipelineManager | Lifecycle management | Config + Data | PipelineRun |
| DataQualityManager | Quality enforcement | Data + Rules | QualityResult |
| ETLOrchestrator | Job scheduling | DAG definition | Execution plan |
| DataWarehouseManager | Table management | Schema + Layer | Table metadata |
| DataLineageTracker | Lineage graph | Node + Edge | Graph traversal |
| StreamingManager | Event processing | Messages | Consumed data |
| SchemaRegistry | Schema contracts | Definitions | Compatibility |
| DataCatalog | Metadata search | Entries | Search results |
| InfrastructureAsCodeManager | Infra templates | Resources | Generated code |
| MonitoringManager | Observability | Metrics | Alerts |

---

## Component Deep Dives

### 1. PipelineManager

The PipelineManager is the central orchestrator for data pipelines. It manages the full lifecycle from creation through execution and monitoring.

```
┌─────────────────────────────────────────────────────┐
│                   PipelineManager                     │
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │ Pipeline  │───>│ Execute  │───>│  Monitor  │      │
│  │  Config   │    │  Engine  │    │  Health   │      │
│  └──────────┘    └──────────┘    └──────────┘      │
│       │              │                │              │
│  ┌────┴────┐   ┌─────┴─────┐   ┌─────┴─────┐      │
│  │ Validate│   │ Transform │   │   Alert   │      │
│  │  Rules  │   │   Chain   │   │  Manager  │      │
│  └─────────┘   └───────────┘   └───────────┘      │
│                                                       │
│  Execution Flow:                                      │
│  Extract ──> Transform ──> Load ──> Validate         │
│     │            │            │          │            │
│  Source        Transform    Target    Quality         │
│  Adapter       Registry     Adapter   Checks         │
└─────────────────────────────────────────────────────┘
```

**Key Responsibilities:**
- Pipeline CRUD operations with thread-safe state management
- Three-phase execution: Extract → Transform → Load
- Built-in retry logic with configurable backoff
- Pipeline run history tracking with full metrics
- Health calculation across all managed pipelines

**Thread Safety:**
The PipelineManager uses a `threading.Lock` to protect pipeline state mutations. All `_pipelines` dict operations are guarded, enabling safe concurrent access from multiple orchestrator threads.

**Execution Model:**
Each `execute_pipeline()` call runs synchronously within the calling thread. For production use, wrap in a `ThreadPoolExecutor` or submit to an external workflow engine.

### 2. DataQualityManager

Implements a rule-based quality assessment engine with profiling capabilities.

```
┌─────────────────────────────────────────────────────┐
│               DataQualityManager                      │
├─────────────────────────────────────────────────────┤
│                                                       │
│  Input Data ──> ┌─────────────┐ ──> Quality Report  │
│                 │  Rule Engine │                      │
│                 │              │                      │
│  ┌──────────┐  │  NOT NULL    │  ┌──────────────┐  │
│  │ Profiler │  │  UNIQUE      │  │    Score      │  │
│  │          │  │  RANGE       │  │  Calculator   │  │
│  │ Schema   │  │  REGEX       │  │              │  │
│  │ Stats    │  │  Custom      │  │  Weighted by │  │
│  │ Anomaly  │  │              │  │  Severity    │  │
│  └──────────┘  └─────────────┘  └──────────────┘  │
│                                                       │
│  Quality Dimensions:                                  │
│  ├── Completeness  (null %)                          │
│  ├── Accuracy      (valid values)                    │
│  ├── Consistency   (cross-column rules)              │
│  ├── Timeliness    (freshness SLA)                   │
│  └── Uniqueness    (duplicate detection)             │
└─────────────────────────────────────────────────────┘
```

**Rule Types:**

| Rule | Syntax | Example | Validates |
|------|--------|---------|-----------|
| NOT NULL | `NOT NULL` | `rule="NOT NULL"` | No null values |
| UNIQUE | `UNIQUE` | `rule="UNIQUE"` | No duplicate values |
| RANGE | `RANGE lo,hi` | `rule="RANGE 0,120"` | Values within bounds |
| REGEX | `REGEX pattern` | `rule="REGEX ^[a-z]+$"` | Pattern match |

**Scoring Algorithm:**

The quality score is a severity-weighted calculation:

```
score = 100 - (failed_weight / total_weight × 100)

Weights: INFO=1, LOW=2, MEDIUM=5, HIGH=10, CRITICAL=25
```

A CRITICAL failure reduces the score more than a LOW failure.

### 3. ETLOrchestrator

Manages job scheduling with dependency resolution via topological sort.

```
┌─────────────────────────────────────────────────────┐
│                 ETLOrchestrator                        │
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │ Job      │    │   DAG    │    │ Execution│      │
│  │ Registry │───>│ Resolver │───>│  Engine   │      │
│  └──────────┘    └──────────┘    └──────────┘      │
│                       │                               │
│              ┌────────┴────────┐                     │
│              │  Topological    │                     │
│              │  Sort           │                     │
│              └─────────────────┘                     │
│                                                       │
│  DAG Example:                                         │
│  extract_users ──┐                                    │
│                  ├──> join_data ──> load_warehouse   │
│  extract_orders ─┘           │                       │
│                              └──> update_dashboard   │
└─────────────────────────────────────────────────────┘
```

**Dependency Resolution:**

The `_topo_sort` method performs a depth-first topological sort, ensuring each job runs only after all its dependencies complete. The algorithm handles:
- Diamond dependencies (A→B, A→C, B→D, C→D)
- Circular dependency detection (via visited set)
- Root job identification (jobs with no dependencies)

### 4. DataWarehouseManager

Manages warehouse objects across medallion architecture layers.

```
┌─────────────────────────────────────────────────────────────┐
│                    DataWarehouseManager                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌──────┐ │
│  │  RAW   │─>│STAGING │─>│CURATED │─>│ANALYTICS│─>│ MART │ │
│  │        │  │        │  │        │  │         │  │      │ │
│  │Ingested│  │Cleaned │  │Business│  │ Query   │  │ Agg  │ │
│  │ data   │  │& typed │  │  rules │  │ optimized│ │ views│ │
│  └────────┘  └────────┘  └────────┘  └─────────┘  └──────┘ │
│                                                               │
│  Features:                                                    │
│  • DDL generation from schema definitions                    │
│  • Storage format selection (Parquet/ORC/Delta/Iceberg)      │
│  • Partition management                                       │
│  • Table optimization (compaction, statistics)                │
│  • Cross-layer lineage tracking                               │
└─────────────────────────────────────────────────────────────┘
```

**Medallion Architecture:**

| Layer | Purpose | Data Quality | Consumers |
|-------|---------|-------------|-----------|
| RAW | Landing zone, immutable | Raw format, no validation | Ingestion systems |
| STAGING | Cleaned, typed | Basic validation applied | Transformation jobs |
| CURATED | Business rules applied | Full quality checks | Analytics teams |
| ANALYTICS | Query-optimized | High quality, aggregated | BI dashboards, reports |
| MART | Domain-specific views | Curated for self-service | Business users |

### 5. DataLineageTracker

A graph-based lineage tracking system supporting upstream and downstream traversal.

```
┌─────────────────────────────────────────────────────┐
│               DataLineageTracker                      │
├─────────────────────────────────────────────────────┤
│                                                       │
│  source_orders ──────┐                               │
│       │              │                               │
│       v              v                               │
│  source_customers  source_products                   │
│       │              │                               │
│       v              v                               │
│       └────> clean_and_join <─────┘                 │
│                    │                                  │
│              ┌─────┴─────┐                           │
│              v           v                           │
│        analytics    ml_training                      │
│        _dashboard   _data                            │
│              │           │                           │
│              v           v                           │
│        weekly_      feature_                         │
│        reports      store                            │
│                                                       │
│  Operations:                                          │
│  • get_upstream(node)   — trace data sources         │
│  • get_downstream(node) — trace data consumers       │
│  • impact_analysis(node) — assess change impact      │
│  • visualize()          — ASCII graph rendering      │
└─────────────────────────────────────────────────────┘
```

**Graph Traversal:**

Both `get_upstream` and `get_downstream` use BFS with a configurable `max_depth` parameter to prevent infinite traversal in cyclic graphs (though the system enforces DAG properties at registration time).

### 6. StreamingManager

Manages Kafka-style topics, producers, consumers, and message buffers.

```
┌─────────────────────────────────────────────────────┐
│                StreamingManager                       │
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │  Topics  │───>│ Produce  │───>│ Consume  │      │
│  │ Registry │    │          │    │          │      │
│  └──────────┘    └──────────┘    └──────────┘      │
│       │              │                │              │
│  ┌────┴────┐   ┌─────┴─────┐   ┌─────┴─────┐      │
│  │Partition│   │  Buffer   │   │ Consumer  │      │
│  │ Routing │   │  Manager  │   │  Groups   │      │
│  └─────────┘   └───────────┘   └───────────┘      │
│                                                       │
│  Partitioning: hash(key) % num_partitions            │
│  Delivery: at-least-once (default)                   │
└─────────────────────────────────────────────────────┘
```

### 7. SchemaRegistry

Manages schema definitions, versioning, and compatibility.

```
┌─────────────────────────────────────────────────────┐
│                SchemaRegistry                         │
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │ Register │───>│ Version  │───>│Compatibi-│      │
│  │ Schema   │    │ Manager  │    │lity Check│      │
│  └──────────┘    └──────────┘    └──────────┘      │
│                                                       │
│  Strategies:                                          │
│  ├── FAIL: reject any incompatible change            │
│  ├── IGNORE: allow any change                        │
│  ├── ADD_COLUMNS: allow new columns only             │
│  └── TYPE_PROMOTION: allow compatible type changes   │
└─────────────────────────────────────────────────────┘
```

### 8. DataCatalog

Metadata catalog for data discovery and governance.

```
┌─────────────────────────────────────────────────────┐
│                  DataCatalog                           │
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │  Search  │───>│  Index   │───>│  Filter  │      │
│  │  Engine  │    │  Manager │    │  Engine   │      │
│  └──────────┘    └──────────┘    └──────────┘      │
│       │              │                │              │
│  ┌────┴────┐   ┌─────┴─────┐   ┌─────┴─────┐      │
│  │  Full   │   │   Tag     │   │  Owner    │      │
│  │  Text   │   │   Index   │   │  Index    │      │
│  └─────────┘   └───────────┘   └───────────┘      │
└─────────────────────────────────────────────────────┘
```

### 9. InfrastructureAsCodeManager

Generates and manages infrastructure templates.

```
┌─────────────────────────────────────────────────────┐
│             InfrastructureAsCodeManager               │
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │ Resource │───>│ Template │───>│ Deploy   │      │
│  │  Define  │    │ Generator│    │ Manager  │      │
│  └──────────┘    └──────────┘    └──────────┘      │
│                       │                               │
│              ┌────────┼────────┐                     │
│              v        v        v                     │
│         Terraform  CFN     Pulumi                    │
│         (HCL)    (JSON)   (YAML)                     │
└─────────────────────────────────────────────────────┘
```

### 10. MonitoringManager

Metrics collection, alert evaluation, and notification.

```
┌─────────────────────────────────────────────────────┐
│               MonitoringManager                       │
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │  Metric  │───>│  Alert   │───>│ Notify   │      │
│  │ Recorder │    │Evaluator │    │          │      │
│  └──────────┘    └──────────┘    └──────────┘      │
│       │              │                │              │
│  ┌────┴────┐   ┌─────┴─────┐   ┌─────┴─────┐      │
│  │ History │   │  Rules    │   │  Slack    │      │
│  │  Store  │   │  Engine   │   │  Email    │      │
│  └─────────┘   └───────────┘   │  PagerDuty│      │
│                                 └───────────┘      │
└─────────────────────────────────────────────────────┘
```

---

## Data Flow

### Batch Processing Flow

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  Source   │──>│ Extract  │──>│Transform │──>│  Quality  │──>│   Load   │
│  Systems  │   │          │   │          │   │  Checks   │   │          │
│           │   │ • JDBC    │   │ • Filter │   │           │   │ • Write  │
│ • RDBMS   │   │ • File    │   │ • Join   │   │ • Profile │   │ • Upsert │
│ • Files   │   │ • API     │   │ • Agg    │   │ • Score   │   │ • Append │
│ • APIs    │   │ • Stream  │   │ • Rename │   │ • Alert   │   │ • Replace│
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
                                    │                │              │
                                    v                v              v
                               ┌──────────────────────────────────────┐
                               │        Lineage Graph Updated         │
                               └──────────────────────────────────────┘
```

### Streaming Processing Flow

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ Event     │──>│ Produce  │──>│  Topic   │──>│ Consume  │
│ Sources   │   │          │   │ (Kafka)  │   │          │
│           │   │ • JSON   │   │          │   │ • Group  │
│ • Apps    │   │ • Avro   │   │ • Partit.│   │ • Offset │
│ • IoT     │   │ • Proto  │   │ • Schema │   │ • Commit │
│ • Logs    │   │          │   │ • Retain │   │          │
└──────────┘   └──────────┘   └──────────┘   └─────┬────┘
                                                     │
                              ┌──────────────────────┘
                              v
                        ┌──────────┐   ┌──────────┐
                        │ Process  │──>│   Sink   │
                        │          │   │          │
                        │ • Window │   │ • Table  │
                        │ • Join   │   │ • Topic  │
                        │ • Filter │   │ • File   │
                        └──────────┘   └──────────┘
```

### End-to-End Data Journey

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  Source  │──>│ Ingest  │──>│ Process │──>│Validate │──>│  Store  │
│          │   │         │   │         │   │         │   │         │
│ Raw data │   │ Extract │   │ Transform│  │ Quality │   │ Warehouse│
│          │   │ Validate│   │ Enrich  │   │ Profile │   │ Data Lake│
│          │   │ Schema  │   │ Aggregate│  │ Score   │   │ Catalog  │
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
     │              │              │              │              │
     v              v              v              v              v
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│Lineage  │   │Lineage  │   │Lineage  │   │Lineage  │   │Lineage  │
│ Node    │   │ Edge    │   │ Edge    │   │ Edge    │   │ Node    │
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
```

---

## Design Patterns

### Mediator Pattern

The `DataEngineeringAgent` acts as a mediator, coordinating interactions between all components without tight coupling.

```
┌─────────────────────────────────────────┐
│         Mediator (Agent)                │
│                                         │
│  create_full_pipeline():                │
│    1. PipelineManager.create()          │
│    2. LineageTracker.register()         │
│    3. DataCatalog.add_entry()           │
│    4. SchemaRegistry.register()         │
│                                         │
│  run_quality_assessment():              │
│    1. QualityManager.run_checks()       │
│    2. MonitoringManager.record_metric() │
│    3. AlertManager.evaluate()           │
└─────────────────────────────────────────┘
```

### Observer Pattern

The MonitoringManager implements the Observer pattern for alert evaluation. Metric recording triggers alert rule evaluation automatically.

```python
# Conceptual flow
monitoring.record_metric("pipeline.duration", 3600)
    → _evaluate_alerts("pipeline.duration", 3600)
        → for rule in alert_rules:
            if rule.metric == "pipeline.duration":
                if value > rule.threshold:
                    fire_alert(rule)
```

### Factory Pattern

The `generate_template` method in `InfrastructureAsCodeManager` uses the Factory pattern to produce different template formats from the same resource definition.

```
IaCResource ──> InfrastructureAsCodeManager
                    │
                    ├──> _gen_terraform()    → HCL string
                    ├──> _gen_cloudformation() → JSON template
                    └──> _gen_pulumi()        → YAML template
```

### Strategy Pattern

Transformations use the Strategy pattern. Each `TransformBase` subclass implements the same `execute()` interface with different algorithms.

```
TransformBase (abstract)
    │
    ├── FilterTransform.execute()      — row-level filtering
    ├── AggregateTransform.execute()   — group-by aggregation
    ├── JoinTransform.execute()        — dataset joining
    └── RenameTransform.execute()      — column renaming
```

### Builder Pattern

Pipeline configuration is built incrementally through the `PipelineConfig` dataclass, allowing flexible construction with sensible defaults.

### Chain of Responsibility

The quality check evaluation chains multiple rules, each processing the data and passing results to the scoring engine.

### Repository Pattern

The `SchemaRegistry`, `DataCatalog`, and `PipelineManager` all implement the Repository pattern, providing CRUD operations over in-memory stores with search and filtering capabilities.

### Template Method Pattern

The `execute_pipeline` method defines the skeleton of the extraction-transformation-load process, while `_extract`, `_transform`, and `_load` are override points.

---

## Tech Stack

### Core Runtime

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python 3.10+ | Core implementation |
| Type System | Dataclasses + Enum | Structured data contracts |
| Concurrency | ThreadPoolExecutor | Parallel pipeline execution |
| Serialization | JSON | Configuration and API communication |
| Logging | Python logging | Structured observability |
| Threading | threading.Lock | Thread-safe state management |

### Data Processing

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Batch Processing | Apache Spark / Dask | Large-scale ETL |
| Stream Processing | Apache Kafka / Flink | Real-time event processing |
| File Formats | Parquet, ORC, Avro | Columnar storage |
| Table Formats | Delta Lake, Iceberg, Hudi | ACID transactions on data lakes |

### Storage

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Data Warehouse | Snowflake, BigQuery, Redshift | Analytical queries |
| Data Lake | S3, GCS, ADLS | Raw and processed data storage |
| Metadata Store | Hive Metastore, Unity Catalog | Schema and table metadata |
| Schema Registry | Confluent Schema Registry | Avro/Protobuf schema management |

### Orchestration

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Workflow Engine | Airflow, Dagster, Prefect | DAG-based scheduling |
| Monitoring | Prometheus, Grafana | Metrics and dashboards |
| Alerting | PagerDuty, Slack, Email | Incident notification |

### Infrastructure

| Component | Technology | Purpose |
|-----------|-----------|---------|
| IaC | Terraform, CloudFormation, Pulumi | Infrastructure provisioning |
| Containers | Docker, Kubernetes | Deployment and scaling |
| CI/CD | GitHub Actions, GitLab CI | Automated deployment |

---

## Security Architecture

### Authentication & Authorization

```
┌─────────────────────────────────────────────────────┐
│                  Security Layers                      │
├─────────────────────────────────────────────────────┤
│                                                       │
│  Layer 1: Authentication                              │
│  ├── Service-to-service: mTLS / JWT tokens           │
│  ├── User access: OAuth 2.0 / SAML                   │
│  └── API keys for programmatic access                │
│                                                       │
│  Layer 2: Authorization                               │
│  ├── Role-Based Access Control (RBAC)                │
│  ├── Pipeline-level permissions                      │
│  ├── Dataset-level access control                    │
│  └── Column-level masking for PII                    │
│                                                       │
│  Layer 3: Data Protection                             │
│  ├── Encryption at rest (AES-256)                    │
│  ├── Encryption in transit (TLS 1.3)                 │
│  ├── Secrets management (Vault, AWS Secrets Manager) │
│  ├── PII detection and masking                       │
│  └── Audit logging for compliance                    │
│                                                       │
│  Layer 4: Network Security                            │
│  ├── VPC isolation for data processing               │
│  ├── Private endpoints for storage                   │
│  ├── WAF for API endpoints                           │
│  └── Network policies in Kubernetes                  │
└─────────────────────────────────────────────────────┘
```

### Secrets Management

```yaml
secrets:
  database:
    type: credential
    rotation: 30d
    storage: vault
  api_keys:
    type: token
    rotation: 90d
    storage: aws_secrets_manager
  encryption_keys:
    type: symmetric
    rotation: 365d
    storage: kms
```

### Data Classification

| Classification | Examples | Controls |
|---------------|----------|----------|
| Public | Product catalog | Standard access |
| Internal | Business metrics | RBAC required |
| Confidential | Customer PII | Column masking, audit |
| Restricted | Financial data | MFA, encryption, audit |

### Compliance Mapping

| Regulation | Relevant Controls |
|-----------|-------------------|
| GDPR | PII masking, right-to-deletion, audit logs |
| HIPAA | Encryption, access controls, audit trail |
| SOC 2 | Encryption, access management, monitoring |
| PCI DSS | Tokenization, encryption, network segmentation |

---

## Scalability Patterns

### Horizontal Scaling

```
┌──────────────────────────────────────────────────────────┐
│                    Horizontal Scaling                      │
├──────────────────────────────────────────────────────────┤
│                                                            │
│  Single Node:                                             │
│  ┌──────────┐                                             │
│  │ Pipeline │ ──> 100 records/sec                        │
│  │ Manager  │                                             │
│  └──────────┘                                             │
│                                                            │
│  Distributed:                                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                 │
│  │ Pipeline │ │ Pipeline │ │ Pipeline │ ──> 10K rec/sec │
│  │ Manager 1│ │ Manager 2│ │ Manager 3│                 │
│  └──────────┘ └──────────┘ └──────────┘                 │
│       │              │              │                     │
│  ┌────┴────┐   ┌─────┴────┐   ┌────┴────┐              │
│  │ Worker  │   │ Worker   │   │ Worker  │              │
│  │ Pool 1  │   │ Pool 2   │   │ Pool 3  │              │
│  └─────────┘   └──────────┘   └─────────┘              │
└──────────────────────────────────────────────────────────┘
```

### Vertical Scaling

- **Thread pools** for concurrent pipeline execution within a single node
- **Connection pooling** for database and API connections
- **Memory-mapped I/O** for large file processing
- **Batch processing** to amortize overhead across records

### Caching Strategy

```
┌─────────────────────────────────────────┐
│           Multi-Level Cache              │
├─────────────────────────────────────────┤
│                                         │
│  L1: In-Memory (per-component)          │
│  ├── Schema cache                       │
│  ├── Quality check results              │
│  └── Catalog metadata                   │
│                                         │
│  L2: Distributed (shared)               │
│  ├── Pipeline run history               │
│  ├── Lineage graph                      │
│  └── Monitoring metrics                 │
│                                         │
│  L3: Persistent (disk)                  │
│  ├── Checkpoint data                    │
│  ├── Audit logs                         │
│  └── Historical metrics                 │
└─────────────────────────────────────────┘
```

### Throughput Optimization

| Technique | Use Case | Impact |
|-----------|----------|--------|
| Parallel transforms | CPU-bound transforms | 2-4x throughput |
| Batch inserts | Loading to warehouse | 10x load speed |
| Partition pruning | Large table queries | 5-100x query speed |
| Columnar storage | Analytics queries | 3-10x compression |
| Materialized views | Repeated aggregations | 10-100x query speed |

---

## Deployment Topology

### Single-Node Development

```
┌─────────────────────────────────────────┐
│          Development Machine             │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │   DataEngineeringAgent          │   │
│  │   (all components in-process)   │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌──────────┐  ┌──────────────────┐   │
│  │ SQLite   │  │ Local filesystem │   │
│  │ (meta)   │  │ (data lake)      │   │
│  └──────────┘  └──────────────────┘   │
└─────────────────────────────────────────┘
```

### Production (Kubernetes)

```
┌───────────────────────────────────────────────────────────────┐
│                        Kubernetes Cluster                       │
├───────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                    Ingress / API Gateway                 │  │
│  └─────────────────────────┬───────────────────────────────┘  │
│                             │                                   │
│  ┌──────────┐ ┌──────────┐ │ ┌──────────┐ ┌──────────┐      │
│  │ Pipeline │ │ Quality  │ │ │ ETL      │ │ Warehouse│      │
│  │ Manager  │ │ Manager  │ │ │ Orch     │ │ Manager  │      │
│  │ (3 pods) │ │ (2 pods) │ │ │ (3 pods) │ │ (2 pods) │      │
│  └──────────┘ └──────────┘ │ └──────────┘ └──────────┘      │
│                             │                                   │
│  ┌──────────────────────────┴──────────────────────────────┐  │
│  │              Service Mesh (Istio)                        │  │
│  └──────────────────────────┬──────────────────────────────┘  │
│                             │                                   │
│  ┌──────────┐ ┌──────────┐ │ ┌──────────┐ ┌──────────┐      │
│  │ Lineage  │ │Streaming │ │ │ Schema   │ │ Catalog  │      │
│  │ Tracker  │ │ Manager  │ │ │ Registry │ │ Service  │      │
│  └──────────┘ └──────────┘ │ └──────────┘ └──────────┘      │
│                             │                                   │
│  ┌──────────────────────────┴──────────────────────────────┐  │
│  │        Persistent Storage (PV/PVC)                       │  │
│  │  • Metadata DB (PostgreSQL)                              │  │
│  │  • Object Storage (S3/GCS)                               │  │
│  │  • Schema Registry (Confluent)                           │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└───────────────────────────────────────────────────────────────┘
```

---

## Data Lineage Architecture

### Graph Model

```
┌─────────────────────────────────────────────────────┐
│                Lineage Graph Model                    │
├─────────────────────────────────────────────────────┤
│                                                       │
│  Nodes:                                              │
│  ┌─────────────────────────────────────────────┐    │
│  │  node_id: unique identifier                 │    │
│  │  name: human-readable name                  │    │
│  │  node_type: table | view | pipeline |       │    │
│  │            dashboard | dataset               │    │
│  │  metadata: custom key-value pairs           │    │
│  │  owner: responsible team/person              │    │
│  └─────────────────────────────────────────────┘    │
│                                                       │
│  Edges:                                              │
│  ┌─────────────────────────────────────────────┐    │
│  │  upstream_id ──> downstream_id              │    │
│  │  relationship: direct | derived | lookup     │    │
│  └─────────────────────────────────────────────┘    │
│                                                       │
│  Algorithms:                                         │
│  ├── BFS/DFS traversal (upstream/downstream)        │
│  ├── Impact analysis (what breaks if X changes)     │
│  ├── Critical path identification                    │
│  └── Circular dependency detection                   │
└─────────────────────────────────────────────────────┘
```

### Lineage Levels

| Level | Scope | Example |
|-------|-------|---------|
| Column-level | Individual columns | `users.email` → `analytics.email_masked` |
| Table-level | Entire tables | `raw.orders` → `mart.daily_sales` |
| Pipeline-level | ETL jobs | `extract_orders` → `load_warehouse` |
| System-level | Cross-system | `Salesforce` → `Snowflake` → `Tableau` |

---

## Streaming Architecture

### Event-Driven Pipeline

```
┌─────────────────────────────────────────────────────────┐
│                 Streaming Architecture                   │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Producers            Topics              Consumers      │
│  ┌─────────┐    ┌──────────────────┐    ┌─────────┐    │
│  │ App 1   │───>│                  │───>│Analytics│    │
│  └─────────┘    │  events.raw      │    └─────────┘    │
│  ┌─────────┐    │                  │    ┌─────────┐    │
│  │ App 2   │───>│  Partitions: 6   │───>│ ML      │    │
│  └─────────┘    │  Replication: 3  │    └─────────┘    │
│  ┌─────────┐    │  Retention: 168h │    ┌─────────┐    │
│  │ IoT     │───>│                  │───>│ Alerting│    │
│  └─────────┘    └──────────────────┘    └─────────┘    │
│                         │                               │
│                  ┌──────┴──────┐                        │
│                  │   Schema    │                        │
│                  │   Registry  │                        │
│                  └─────────────┘                        │
│                                                           │
│  Processing Modes:                                       │
│  ├── Exactly-once: transactional producers/consumers   │
│  ├── At-least-once: idempotent processing               │
│  └── Best-effort: low-latency, potential loss           │
└─────────────────────────────────────────────────────────┘
```

---

## Monitoring & Observability

### Metrics Collection

```
┌─────────────────────────────────────────────────────┐
│             Observability Stack                       │
├─────────────────────────────────────────────────────┤
│                                                       │
│  Metrics:                                            │
│  ├── Pipeline metrics (run count, duration, errors)  │
│  ├── Quality metrics (score, check pass rate)        │
│  ├── System metrics (CPU, memory, disk I/O)          │
│  ├── Throughput (records/sec, bytes/sec)             │
│  └── Latency (p50, p95, p99)                        │
│                                                       │
│  Logging:                                            │
│  ├── Structured JSON logs                            │
│  ├── Correlation IDs for traceability                │
│  ├── Log levels: DEBUG, INFO, WARNING, ERROR         │
│  └── Centralized log aggregation                     │
│                                                       │
│  Alerting:                                           │
│  ├── Threshold-based (metric > value)                │
│  ├── Rate-based (error rate increase)                │
│  ├── Anomaly detection (statistical)                 │
│  └── Multi-channel (email, Slack, PagerDuty)         │
│                                                       │
│  Dashboard:                                          │
│  ├── Pipeline health overview                        │
│  ├── Data quality trends                             │
│  ├── SLA compliance                                  │
│  ├── Cost tracking                                   │
│  └── Capacity planning                               │
└─────────────────────────────────────────────────────┘
```

### SLA Framework

| Metric | Target | Alert Threshold |
|--------|--------|----------------|
| Pipeline uptime | 99.9% | < 99.5% |
| Pipeline latency (p95) | < 30 min | > 45 min |
| Data quality score | > 95 | < 90 |
| Data freshness | < 1 hour | > 2 hours |
| Schema compatibility | 100% | Any breaking change |

---

## Data Quality Framework

### Quality Dimensions

```
┌─────────────────────────────────────────────────────┐
│              Quality Dimensions                       │
├─────────────────────────────────────────────────────┤
│                                                       │
│  Completeness ─────── % of non-null values           │
│       │                                               │
│  Accuracy ──────────── % of valid domain values      │
│       │                                               │
│  Consistency ───────── Agreement across sources      │
│       │                                               │
│  Timeliness ────────── Data freshness vs SLA         │
│       │                                               │
│  Uniqueness ────────── No unintended duplicates      │
│       │                                               │
│  Validity ──────────── Conformance to format rules   │
└─────────────────────────────────────────────────────┘
```

### Quality Gate Flow

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│ Ingest  │──>│ Quality │──>│ Transform│──>│ Quality │
│         │   │ Gate 1  │   │         │   │ Gate 2  │
│ Raw data│   │         │   │ Clean + │   │         │
│         │   │ • Nulls │   │ Enrich  │   │ • Rules │
│         │   │ • Types │   │         │   │ • Score │
│         │   │ • Vol.  │   │         │   │ • Alert │
└─────────┘   └─────────┘   └─────────┘   └─────────┘
                    │                           │
              FAIL → stop              FAIL → alert, continue
```

---

## Schema Management

### Schema Versioning

```
┌─────────────────────────────────────────────────────┐
│              Schema Evolution                         │
├─────────────────────────────────────────────────────┤
│                                                       │
│  v1: users (id, email, name)                        │
│      │                                               │
│      v  compatible (ADD_COLUMNS)                     │
│  v2: users (id, email, name, phone)                 │
│      │                                               │
│      v  compatible (ADD_COLUMNS)                     │
│  v3: users (id, email, name, phone, created_at)     │
│      │                                               │
│      x  incompatible (TYPE_PROMOTION or FAIL)        │
│  v3': users (id: string, email, name, phone,        │
│              created_at)                             │
│      type change id: int → string                    │
└─────────────────────────────────────────────────────┘
```

---

## Infrastructure as Code Patterns

### Resource Definition → Template → Deployment

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   Define     │──>│   Generate   │──>│   Deploy     │
│   Resource   │   │   Template   │   │              │
│              │   │              │   │              │
│ • name       │   │ • Terraform  │   │ • plan       │
│ • type       │   │ • CloudForm. │   │ • apply      │
│ • config     │   │ • Pulumi     │   │ • verify     │
│ • depends_on │   │ • CDK        │   │ • rollback   │
└──────────────┘   └──────────────┘   └──────────────┘
```

---

## Appendix: Component Interaction Matrix

| | Pipeline | Quality | ETL | Warehouse | Lineage | Streaming | Schema | Catalog | IaC | Monitor |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Pipeline** | - | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ❌ | ✅ |
| **Quality** | ✅ | - | ⚠️ | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ |
| **ETL** | ✅ | ⚠️ | - | ✅ | ✅ | ⚠️ | ✅ | ⚠️ | ❌ | ✅ |
| **Warehouse** | ✅ | ✅ | ✅ | - | ✅ | ❌ | ✅ | ✅ | ✅ | ⚠️ |
| **Lineage** | ✅ | ❌ | ✅ | ✅ | - | ⚠️ | ⚠️ | ✅ | ❌ | ❌ |
| **Streaming** | ⚠️ | ❌ | ⚠️ | ❌ | ⚠️ | - | ✅ | ⚠️ | ❌ | ✅ |
| **Schema** | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | - | ✅ | ❌ | ❌ |
| **Catalog** | ✅ | ✅ | ⚠️ | ✅ | ✅ | ⚠️ | ✅ | - | ❌ | ❌ |
| **IaC** | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | - | ✅ |
| **Monitor** | ✅ | ✅ | ✅ | ⚠️ | ❌ | ✅ | ❌ | ❌ | ✅ | - |

Legend: ✅ = strong coupling, ⚠️ = weak coupling, ❌ = no coupling
