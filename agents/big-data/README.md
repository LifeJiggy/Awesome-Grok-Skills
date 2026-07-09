# Big Data Agent

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/awesome-grok-skills/big-data-agent)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-yellow.svg)](https://www.python.org/)

A comprehensive distributed computing agent for large-scale data processing, including cluster management, pipeline orchestration, stream processing, batch processing, and data lake management.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Cluster Management](#cluster-management)
  - [Pipeline Orchestration](#pipeline-orchestration)
  - [Stream Processing](#stream-processing)
  - [Batch Processing](#batch-processing)
  - [Data Lake Management](#data-lake-management)
  - [Data Quality](#data-quality)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Big Data Agent is a modular, extensible platform designed for enterprise-scale data processing. It provides:

- **Cluster Management**: Create, scale, and monitor distributed computing clusters
- **Pipeline Orchestration**: Build and manage data ingestion and ETL workflows
- **Stream Processing**: Handle real-time data streams with exactly-once semantics
- **Batch Processing**: Execute large-scale data transformations
- **Data Lake Management**: Manage petabyte-scale data lakes with ACID transactions
- **Data Quality**: Monitor and enforce data quality across all datasets

### Why Use This Agent?

| Traditional Approach | Big Data Agent |
|---------------------|----------------|
| Manual cluster setup | Automated provisioning and scaling |
| Siloed processing | Unified batch + stream processing |
| No data quality | Built-in quality monitoring |
| Schema evolution issues | Schema registry with compatibility |
| High operational cost | Cost-aware resource management |

---

## Features

### Core Features

- **Cluster Management**: Multi-cloud, multi-framework cluster provisioning
- **Pipeline Orchestration**: Visual pipeline builder with scheduling
- **Stream Processing**: Flink-based exactly-once processing
- **Batch Processing**: Spark-optimized batch transformations
- **Data Lake**: Delta Lake / Iceberg / Hudi support

### Advanced Features

- **Auto-Scaling**: Dynamic cluster scaling based on workload
- **Schema Registry**: Versioned schemas with compatibility checks
- **Data Quality**: Automated quality checks and monitoring
- **Spark Optimization**: AI-powered job optimization suggestions
- **Cost Tracking**: Real-time cost monitoring and optimization

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Big Data Agent                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  │
│  │  Cluster   │  │ Pipeline  │  │  Stream   │  │  Batch    │  │
│  │  Manager   │  │ Manager   │  │ Processor │  │ Processor │  │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  │
│  │  Data Lake │  │  Quality  │  │  Schema   │  │  Spark    │  │
│  │  Manager   │  │  Manager  │  │  Registry │  │  Optimizer│  │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Component Overview

| Component | Purpose | Key Classes |
|-----------|---------|-------------|
| Cluster Manager | Cluster lifecycle management | `ClusterManager`, `ClusterConfig` |
| Pipeline Manager | Data pipeline orchestration | `PipelineManager`, `DataPipeline` |
| Stream Processor | Real-time stream processing | `StreamProcessor`, `StreamJob` |
| Batch Processor | Batch data transformation | `BatchProcessor`, `BatchJob` |
| Data Lake Manager | Data lake operations | `DataLakeManager`, `DataLake` |
| Quality Manager | Data quality monitoring | `DataQualityManager`, `DataQualityReport` |
| Spark Optimizer | Job performance optimization | `SparkOptimizer` |

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/awesome-grok-skills/agents.git
cd agents

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from agents.big_data.agent import BigDataAgent, ProcessingFramework

# Initialize the agent
agent = BigDataAgent()

# Create a cluster
cluster = agent.cluster_manager.create_cluster(
    name="My Cluster",
    framework=ProcessingFramework.SPARK,
    num_workers=5
)

# Create a pipeline
pipeline = agent.pipeline_manager.create_pipeline(
    name="My Pipeline",
    source="s3://raw/",
    destination="s3://processed/"
)

# Run the pipeline
result = agent.pipeline_manager.run_pipeline(pipeline.pipeline_id)
print(f"Processed {result['records_processed']} records")
```

### Run the Demo

```bash
python agents/big_data/agent.py
```

---

## Usage

### Cluster Management

Create and manage distributed computing clusters.

```python
# Create a cluster with auto-scaling
cluster = agent.cluster_manager.create_cluster(
    name="Production Cluster",
    framework=ProcessingFramework.SPARK,
    mode=ClusterMode.KUBERNETES,
    num_workers=20,
    worker_memory="16g",
    worker_cores=8,
    auto_scaling=True
)

# Scale based on workload
agent.cluster_manager.scale_cluster(cluster.cluster_id, target_workers=30)

# Get cluster status
status = agent.cluster_manager.get_cluster_status(cluster.cluster_id)
print(f"CPU: {status['resources']['cpu_used_percent']}%")
print(f"Cost: ${status['cost']['per_hour']}/hour")

# Stop cluster
agent.cluster_manager.stop_cluster(cluster.cluster_id)
```

**Supported Frameworks:**

| Framework | Use Case | Best For |
|-----------|----------|----------|
| Apache Spark | Batch + ML | Large-scale transformations |
| Apache Flink | Stream | Real-time processing |
| Dask | Parallel Python | Interactive analytics |
| Hadoop MapReduce | Legacy batch | Existing Hadoop ecosystems |

### Pipeline Orchestration

Build and manage data pipelines.

```python
# Create a pipeline
pipeline = agent.pipeline_manager.create_pipeline(
    name="Sales Ingestion",
    source="s3://raw/sales/",
    destination="s3://curated/sales/",
    format=StorageFormat.PARQUET,
    schedule="hourly"
)

# Execute the pipeline
run = agent.pipeline_manager.run_pipeline(pipeline.pipeline_id)
print(f"Records: {run['records_processed']}")
print(f"Duration: {run['execution_time_seconds']}s")

# Monitor pipeline
status = agent.pipeline_manager.get_pipeline_status(pipeline.pipeline_id)
print(f"Total processed: {status['total_processed']}")
```

**Pipeline Schedules:**

| Schedule | Description | Use Case |
|----------|-------------|----------|
| `real_time` | Continuous | Streaming data |
| `hourly` | Every hour | Near-real-time |
| `daily` | Once daily | Batch reporting |
| `weekly` | Weekly | Aggregations |
| `monthly` | Monthly | Financial data |

### Stream Processing

Handle real-time data streams.

```python
# Create a stream job
stream_job = agent.stream_processor.create_stream_job(
    name="Real-time Events",
    source_topic="raw-events",
    sink_topic="processed-events",
    framework=ProcessingFramework.FLINK,
    mode=StreamMode.EXACTLY_ONCE
)

# Monitor throughput
metrics = agent.stream_processor.get_stream_metrics(stream_job.job_id)
print(f"Throughput: {metrics['throughput_mps']} msg/s")
print(f"Lag: {metrics['consumer_lag']}")

# Create a topic
agent.stream_processor.create_topic(
    topic_name="user-actions",
    partitions=12,
    replication_factor=3
)
```

**Processing Modes:**

| Mode | Guarantees | Trade-offs |
|------|-----------|------------|
| AT_MOST_ONCE | No duplicates | May lose messages |
| AT_LEAST_ONCE | No loss | May have duplicates |
| EXACTLY_ONCE | Perfect | Higher latency |

### Batch Processing

Execute large-scale batch transformations.

```python
# Create a batch job
batch_job = agent.batch_processor.create_batch_job(
    name="Daily Aggregation",
    input_path="s3://data-lake/silver/transactions/",
    output_path="s3://data-lake/gold/daily-metrics/",
    framework=ProcessingFramework.SPARK
)

# Optimize the job
optimizations = agent.batch_processor.optimize_spark_job(
    batch_job.job_id,
    optimizations=["broadcast_join", "aqe"]
)
print(f"Expected improvement: {optimizations['estimated_improvement']}")

# Execute
result = agent.batch_processor.execute_job(batch_job.job_id)
print(f"Processed: {result['records_processed']}")
```

**Spark Optimizations:**

| Optimization | Description | Expected Speedup |
|-------------|-------------|------------------|
| Broadcast Join | Broadcast small tables | 2-5x |
| AQE | Adaptive query execution | 1.2-2x |
| Compression | Snappy/ZSTD compression | 1.5-3x |
| Caching | Cache hot data | 2-10x |

### Data Lake Management

Manage petabyte-scale data lakes.

```python
# Create a Delta Lake
lake = agent.data_lake_manager.create_data_lake(
    name="Enterprise Data Lake",
    storage_path="s3://enterprise-data-lake/",
    format=StorageFormat.DELTA,
    partition_strategy=PartitionStrategy.TIMESTAMP,
    compression=CompressionType.ZSTD
)

# Get lake status
status = agent.data_lake_manager.get_lake_status(lake.lake_id)
print(f"Size: {status['total_size_gb']} GB")
print(f"Files: {status['total_files']}")

# Compact files
compaction = agent.data_lake_manager.compact_data_lake(lake.lake_id)
print(f"Reduced files by {compaction['reduction_percent']}%")

# Schema management
schema = agent.data_lake_manager.create_schema(
    name="orders",
    fields=[
        {"name": "order_id", "type": "string"},
        {"name": "amount", "type": "decimal(10,2)"}
    ],
    compatibility="BACKWARD"
)
```

**Storage Formats:**

| Format | ACID | Time Travel | Best For |
|--------|------|-------------|----------|
| Delta Lake | Yes | Yes | Spark workloads |
| Iceberg | Yes | Yes | Multi-engine |
| Hudi | Yes | Yes | Incremental |
| Parquet | No | No | Columnar storage |

### Data Quality

Monitor and enforce data quality.

```python
# Create quality rules
agent.quality_manager.create_quality_rule(
    dataset="orders",
    rule_type="not_null",
    column="order_id",
    config={"severity": "critical"}
)

# Run quality check
report = agent.quality_manager.run_quality_check("orders", total_records=1000000)
print(f"Quality: {report.overall_quality.value}")
print(f"Completeness: {report.completeness_score}")

# Get trend
trend = agent.quality_manager.get_quality_trend("orders", days=30)
print(f"Average score: {trend['average_score']}")
```

**Quality Dimensions:**

| Dimension | Description | Metric |
|-----------|-------------|--------|
| Completeness | No missing values | % non-null |
| Accuracy | Correct values | % valid |
| Consistency | Consistent format | % consistent |
| Timeliness | Data freshness | Latency |

---

## API Reference

### BigDataAgent

```python
class BigDataAgent:
    """Main Big Data Agent."""
    
    cluster_manager: ClusterManager
    pipeline_manager: PipelineManager
    stream_processor: StreamProcessor
    batch_processor: BatchProcessor
    data_lake_manager: DataLakeManager
    quality_manager: DataQualityManager
    spark_optimizer: SparkOptimizer
    
    def get_status(self) -> Dict[str, Any]
```

### ClusterManager

```python
class ClusterManager:
    def create_cluster(
        name: str,
        framework: ProcessingFramework,
        mode: ClusterMode,
        num_workers: int,
        worker_memory: str = "8g",
        worker_cores: int = 4,
        auto_scaling: bool = False
    ) -> ClusterConfig
    
    def get_cluster_status(cluster_id: str) -> Dict[str, Any]
    def scale_cluster(cluster_id: str, target_workers: int) -> Dict[str, Any]
    def stop_cluster(cluster_id: str) -> Dict[str, Any]
    def get_all_clusters() -> List[Dict[str, Any]]
```

### PipelineManager

```python
class PipelineManager:
    def create_pipeline(
        name: str,
        source: str,
        destination: str,
        format: StorageFormat = StorageFormat.PARQUET,
        schedule: str = "hourly"
    ) -> DataPipeline
    
    def run_pipeline(pipeline_id: str) -> Dict[str, Any]
    def get_pipeline_status(pipeline_id: str) -> Dict[str, Any]
    def list_pipelines(status: Optional[str] = None) -> List[Dict[str, Any]]
```

### StreamProcessor

```python
class StreamProcessor:
    def create_stream_job(
        name: str,
        source_topic: str,
        sink_topic: str,
        framework: ProcessingFramework = ProcessingFramework.FLINK,
        mode: StreamMode = StreamMode.AT_LEAST_ONCE
    ) -> StreamJob
    
    def get_stream_metrics(job_id: str) -> Dict[str, Any]
    def create_topic(topic_name: str, partitions: int = 6) -> Dict[str, Any]
    def get_topic_metrics(topic_name: str) -> Dict[str, Any]
```

### BatchProcessor

```python
class BatchProcessor:
    def create_batch_job(
        name: str,
        input_path: str,
        output_path: str,
        framework: ProcessingFramework = ProcessingFramework.SPARK
    ) -> BatchJob
    
    def execute_job(job_id: str) -> Dict[str, Any]
    def optimize_spark_job(job_id: str, optimizations: List[str]) -> Dict[str, Any]
    def get_job_metrics() -> Dict[str, Any]
```

### DataLakeManager

```python
class DataLakeManager:
    def create_data_lake(
        name: str,
        storage_path: str,
        format: StorageFormat = StorageFormat.PARQUET,
        partition_strategy: PartitionStrategy = PartitionStrategy.TIMESTAMP,
        compression: CompressionType = CompressionType.SNAPPY
    ) -> DataLake
    
    def get_lake_status(lake_id: str) -> Dict[str, Any]
    def compact_data_lake(lake_id: str) -> Dict[str, Any]
    def create_schema(name: str, fields: List[Dict], compatibility: str) -> SchemaDefinition
    def validate_schema_compatibility(schema_id: str, new_fields: List[Dict]) -> Dict[str, Any]
```

---

## Examples

### Example 1: Real-time Analytics Pipeline

```python
from agents.big_data.agent import BigDataAgent, ProcessingFramework

agent = BigDataAgent()

# Create stream job for real-time events
stream_job = agent.stream_processor.create_stream_job(
    name="User Activity Stream",
    source_topic="user-events",
    sink_topic="user-analytics",
    framework=ProcessingFramework.FLINK
)

# Monitor in real-time
metrics = agent.stream_processor.get_stream_metrics(stream_job.job_id)
print(f"Processing {metrics['throughput_mps']} events/second")
```

### Example 2: Batch Data Lake Pipeline

```python
from agents.big_data.agent import BigDataAgent, StorageFormat

agent = BigDataAgent()

# Create data lake
lake = agent.data_lake_manager.create_data_lake(
    name="Sales Data Lake",
    storage_path="s3://sales-data-lake/",
    format=StorageFormat.DELTA
)

# Create batch job
batch_job = agent.batch_processor.create_batch_job(
    name="Monthly Aggregation",
    input_path="s3://sales-data-lake/silver/",
    output_path="s3://sales-data-lake/gold/"
)

# Execute
result = agent.batch_processor.execute_job(batch_job.job_id)
print(f"Aggregated {result['records_processed']} records")
```

### Example 3: Data Quality Monitoring

```python
from agents.big_data.agent import BigDataAgent

agent = BigDataAgent()

# Define quality rules
for col in ["order_id", "customer_id", "amount"]:
    agent.quality_manager.create_quality_rule(
        dataset="orders",
        rule_type="not_null",
        column=col,
        config={"severity": "critical"}
    )

# Run quality check
report = agent.quality_manager.run_quality_check("orders")
if report.overall_quality.value in ["poor", "critical"]:
    print(f"Quality alert: {report.overall_quality.value}")
```

---

## Configuration

### Environment Variables

```bash
# Cluster
SPARK_MASTER=k8s://https://kubernetes.default.svc
KAFKA_BROKERS=kafka:9092

# Storage
S3_BUCKET=my-data-lake
S3_REGION=us-east-1

# Monitoring
PROMETHEUS_URL=http://prometheus:9090
GRAFANA_URL=http://grafana:3000
```

### Configuration File

```yaml
# config.yaml
bigdata_agent:
  cluster:
    auto_scaling: true
    min_workers: 2
    max_workers: 50
    spot_instances: true
  
  pipeline:
    default_format: parquet
    compression: snappy
    max_concurrent: 10
  
  stream:
    checkpoint_interval: 60
    state_backend: rocksdb
    max_parallelism: 128
  
  data_lake:
    default_format: delta
    compaction_schedule: daily
    retention_days: 90
  
  quality:
    auto_check: true
    alert_threshold: 0.9
```

---

## Best Practices

### Cluster Management

1. **Right-Size Workers**: Match resources to workload characteristics
2. **Enable Auto-Scaling**: Let clusters adapt to demand
3. **Use Spot Instances**: Save 60-70% on batch workloads
4. **Monitor Costs**: Track and optimize cluster spend
5. **Plan Failures**: Use replication and fault-tolerant storage

### Pipeline Design

1. **Idempotent Operations**: Ensure safe re-runs
2. **Incremental Processing**: Process only new/changed data
3. **Schema Validation**: Validate at ingestion
4. **Dead Letter Queues**: Route failed records
5. **Monitoring**: Track health and SLAs

### Stream Processing

1. **Exactly-Once Semantics**: Use checkpointing
2. **State Management**: Use RocksDB for large state
3. **Backpressure**: Implement rate limiting
4. **Windowing**: Choose based on business needs
5. **Consumer Groups**: Monitor lag

### Data Lake

1. **Medallion Architecture**: Bronze → Silver → Gold
2. **Partitioning**: By high-cardinality columns
3. **File Sizing**: 128MB-256MB optimal
4. **Compaction**: Regular small file compaction
5. **Time Travel**: Leverage for debugging

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| OutOfMemoryError | Low executor memory | Increase memory or reduce partitions |
| Slow shuffle | Too many partitions | Adjust shuffle.partitions |
| Data skew | Uneven distribution | Use salting or broadcast join |
| Stream lag | Consumer bottleneck | Scale consumers |
| Pipeline failure | Source unavailable | Add retry logic |
| Schema error | Breaking change | Use compatibility checks |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

agent = BigDataAgent()
```

### Performance Tuning

```python
spark_config = {
    "spark.sql.adaptive.enabled": True,
    "spark.sql.shuffle.partitions": 200,
    "spark.sql.autoBroadcastJoinThreshold": "10MB"
}
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

### Development Setup

```bash
pip install -r requirements-dev.txt
pytest tests/
ruff check agents/big_data/
```

---

## License

MIT License - see [LICENSE](LICENSE)

---

## Support

- **Documentation**: [docs.example.com](https://docs.example.com)
- **Issues**: [GitHub Issues](https://github.com/awesome-grok-skills/agents/issues)

## Advanced Usage

### Custom Pipeline Components

```python
# Create custom transformation
class CustomTransformer(PipelineTransformer):
    def __init__(self, config):
        self.config = config
    
    def transform(self, data):
        # Custom transformation logic
        return data.filter(lambda x: x['value'] > self.config['threshold'])

# Register custom component
agent.pipeline_manager.register_transformer("custom_filter", CustomTransformer)
```

### Advanced Stream Processing

```python
# Complex event processing
def detect_fraud_pattern(events):
    """
    Detect fraudulent patterns using CEP
    """
    pattern = (events
        .key_by(lambda e: e['user_id'])
        .window(TumblingEventTimeWindows.of(Time.minutes(5)))
        .process(FraudPatternDetector()))

# Windowed aggregation
def windowed_aggregation(events):
    return (events
        .key_by(lambda e: e['product_id'])
        .window(SlidingEventTimeWindows.of(Time.minutes(10), Time.minutes(1)))
        .aggregate(AverageAggregator()))
```

### Data Lake Management

```python
# Advanced data lake operations
def optimize_data_lake(lake_id):
    """
    Optimize data lake for performance
    """
    # Compaction
    agent.data_lake_manager.compact_data_lake(
        lake_id=lake_id,
        target_file_size_mb=256,
        strategy="bin_packing"
    )
    
    # Z-ordering
    agent.data_lake_manager.optimize_z_ordering(
        lake_id=lake_id,
        columns=["date", "region", "product_id"]
    )
    
    # Statistics collection
    agent.data_lake_manager.collect_statistics(
        lake_id=lake_id,
        columns=["date", "amount", "quantity"]
    )
```

## Performance Tuning

### Cluster Optimization

```python
# Optimize cluster configuration
def optimize_cluster(cluster_id):
    """
    Optimize cluster for workload
    """
    # Analyze workload
    workload = agent.cluster_manager.analyze_workload(cluster_id)
    
    # Right-size workers
    recommendations = agent.cluster_manager.get_right_sizing_recommendations(
        cluster_id=cluster_id,
        workload_type=workload['type']
    )
    
    # Apply recommendations
    for rec in recommendations:
        if rec['action'] == 'resize':
            agent.cluster_manager.resize_worker(
                cluster_id=cluster_id,
                worker_type=rec['worker_type'],
                new_size=rec['recommended_size']
            )
```

### Pipeline Optimization

```python
# Optimize pipeline performance
def optimize_pipeline(pipeline_id):
    """
    Optimize pipeline for throughput
    """
    # Analyze bottlenecks
    analysis = agent.pipeline_manager.analyze_bottlenecks(pipeline_id)
    
    # Apply optimizations
    optimizations = []
    if analysis['serialization_bottleneck']:
        optimizations.append("use_kryo")
    if analysis['shuffle_bottleneck']:
        optimizations.append("broadcast_join")
    if analysis['skew_detected']:
        optimizations.append("salting")
    
    agent.pipeline_manager.optimize_pipeline(
        pipeline_id=pipeline_id,
        optimizations=optimizations
    )
```

### Query Optimization

```python
# Optimize SQL queries
def optimize_query(query):
    """
    Optimize query for performance
    """
    # Analyze query plan
    plan = agent.spark_optimizer.explain_query(query)
    
    # Get optimization suggestions
    suggestions = agent.spark_optimizer.get_optimization_suggestions(plan)
    
    # Apply optimizations
    optimized_query = query
    for suggestion in suggestions:
        if suggestion['type'] == 'broadcast_join':
            optimized_query = optimized_query.replace(
                f"JOIN {suggestion['table']}",
                f"BROADCAST JOIN {suggestion['table']}"
            )
    
    return optimized_query
```

## Security Considerations

### Data Encryption

```python
ENCRYPTION_CONFIG = {
    "at_rest": {
        "algorithm": "AES-256",
        "key_management": "AWS KMS",
        "rotation": "annual",
        "enforcement": "required"
    },
    "in_transit": {
        "protocol": "TLS 1.3",
        "certificate_validation": "strict",
        "mutual_tls": True
    },
    "data_masking": {
        "pii_detection": True,
        "masking_strategies": {
            "email": "partial",
            "phone": "hash",
            "ssn": "redact"
        }
    }
}
```

### Access Control

```python
ACCESS_CONTROL = {
    "authentication": {
        "methods": ["oauth2", "saml", "api_key"],
        "mfa_required": True,
        "session_timeout": "8h"
    },
    "authorization": {
        "model": "abac",
        "policies": [
            {
                "role": "data_engineer",
                "permissions": ["read", "write", "execute"],
                "resources": ["cluster:*", "pipeline:*"]
            },
            {
                "role": "data_analyst",
                "permissions": ["read"],
                "resources": ["data_lake:*"]
            }
        ]
    },
    "audit_logging": {
        "enabled": True,
        "events": ["login", "data_access", "schema_change", "pipeline_run"],
        "retention": "1 year",
        "storage": "s3://audit-logs"
    }
}
```

### Network Security

```python
NETWORK_CONFIG = {
    "vpc": {
        "cidr": "10.0.0.0/16",
        "subnets": {
            "private": ["10.0.1.0/24", "10.0.2.0/24"],
            "public": ["10.0.101.0/24", "10.0.102.0/24"]
        }
    },
    "security_groups": {
        "cluster": {
            "inbound": [
                {"port": 22, "source": "10.0.0.0/16", "description": "SSH"},
                {"port": 8080, "source": "10.0.0.0/16", "description": "Spark UI"}
            ],
            "outbound": [
                {"port": 443, "destination": "0.0.0.0/0", "description": "HTTPS"}
            ]
        }
    },
    "network_policies": {
        "kubernetes": {
            "default_deny": True,
            "allowed_namespaces": ["data-processing", "monitoring"]
        }
    }
}
```

## Integration Examples

### Kafka Integration

```python
# Advanced Kafka configuration
KAFKA_CONFIG = {
    "producers": {
        "acks": "all",
        "retries": 3,
        "batch_size": 16384,
        "linger_ms": 10,
        "compression": "snappy"
    },
    "consumers": {
        "group_id": "big-data-consumer",
        "auto_offset_reset": "earliest",
        "enable_auto_commit": False,
        "max_poll_records": 500
    },
    "topics": {
        "raw_events": {
            "partitions": 12,
            "replication_factor": 3,
            "retention_hours": 168,
            "cleanup_policy": "delete"
        }
    }
}
```

### Airflow Integration

```python
# Airflow DAG configuration
AIRFLOW_CONFIG = {
    "dag": {
        "dag_id": "big_data_pipeline",
        "schedule_interval": "@daily",
        "catchup": False,
        "max_active_runs": 1
    },
    "tasks": {
        "extract": {
            "operator": "PythonOperator",
            "python_callable": "extract_data"
        },
        "transform": {
            "operator": "SparkSubmitOperator",
            "application": "transform.py"
        },
        "load": {
            "operator": "S3ToRedshiftOperator",
            "schema": "analytics"
        }
    }
}
```

### Grafana Integration

```python
# Grafana dashboard configuration
GRAFANA_CONFIG = {
    "datasources": {
        "prometheus": {
            "type": "prometheus",
            "url": "http://prometheus:9090",
            "access": "proxy"
        },
        "influxdb": {
            "type": "influxdb",
            "url": "http://influxdb:8086",
            "database": "metrics"
        }
    },
    "dashboards": {
        "cluster_monitoring": {
            "title": "Cluster Monitoring",
            "panels": [
                {"type": "graph", "title": "CPU Usage", "metric": "cpu_usage"},
                {"type": "graph", "title": "Memory Usage", "metric": "memory_usage"},
                {"type": "stat", "title": "Active Jobs", "metric": "active_jobs"}
            ]
        }
    }
}
```

## Monitoring & Troubleshooting

### Health Checks

```python
# Comprehensive health check
def health_check():
    """
    Perform comprehensive health check
    """
    checks = {
        "cluster": agent.cluster_manager.health_check(),
        "pipelines": agent.pipeline_manager.health_check(),
        "streams": agent.stream_processor.health_check(),
        "data_lake": agent.data_lake_manager.health_check()
    }
    
    status = "healthy"
    for component, result in checks.items():
        if result['status'] != 'healthy':
            status = "unhealthy"
            print(f"{component}: {result['issues']}")
    
    return {"status": status, "components": checks}
```

### Performance Monitoring

```python
# Monitor performance metrics
def monitor_performance():
    """
    Monitor system performance
    """
    metrics = {
        "cluster": {
            "cpu_utilization": agent.cluster_manager.get_cpu_utilization(),
            "memory_utilization": agent.cluster_manager.get_memory_utilization(),
            "active_tasks": agent.cluster_manager.get_active_tasks()
        },
        "pipelines": {
            "throughput": agent.pipeline_manager.get_throughput(),
            "error_rate": agent.pipeline_manager.get_error_rate(),
            "latency": agent.pipeline_manager.get_latency()
        },
        "streams": {
            "consumer_lag": agent.stream_processor.get_consumer_lag(),
            "throughput": agent.stream_processor.get_throughput(),
            "checkpoint_status": agent.stream_processor.get_checkpoint_status()
        }
    }
    
    return metrics
```

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable detailed tracing
agent.enable_tracing(
    sample_rate=1.0,
    export_to="jaeger",
    tags={
        "environment": "development",
        "service": "big-data-agent"
    }
)
```

## Deployment Options

### Docker Compose

```yaml
version: '3.8'
services:
  spark-master:
    image: bitnami/spark:3.4
    environment:
      - SPARK_MODE=master
    ports:
      - "8080:8080"
      - "7077:7077"

  spark-worker:
    image: bitnami/spark:3.4
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
    depends_on:
      - spark-master

  kafka:
    image: confluentinc/cp-kafka:7.4.0
    environment:
      - KAFKA_BROKER_ID=1
      - KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
    ports:
      - "9092:9092"

  zookeeper:
    image: confluentinc/cp-zookeeper:7.4.0
    environment:
      - ZOOKEEPER_CLIENT_PORT=2181
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: spark-master
spec:
  serviceName: spark-master
  replicas: 1
  selector:
    matchLabels:
      app: spark-master
  template:
    metadata:
      labels:
        app: spark-master
    spec:
      containers:
        - name: spark-master
          image: bitnami/spark:3.4
          ports:
            - containerPort: 8080
            - containerPort: 7077
          resources:
            requests:
              memory: "2Gi"
              cpu: "1000m"
            limits:
              memory: "4Gi"
              cpu: "2000m"
```

### Terraform

```hcl
# EMR cluster
resource "aws_emr_cluster" "big_data" {
  name          = "big-data-cluster"
  release_label = "emr-6.10.0"
  applications  = ["Spark", "Hive", "Hadoop"]

  master_instance_group {
    instance_type  = "m5.xlarge"
    instance_count = 1
  }

  core_instance_group {
    instance_type  = "m5.2xlarge"
    instance_count = 3
  }

  ec2_attributes {
    subnet_id = aws_subnet.private.id
  }
}
```

## Contributing Guidelines

### Development Workflow

```bash
# 1. Fork and clone
git clone https://github.com/your-org/awesome-grok-skills.git

# 2. Create feature branch
git checkout -b feature/amazing-feature

# 3. Install development dependencies
pip install -r requirements-dev.txt

# 4. Run tests
pytest tests/ -v

# 5. Run linter
ruff check agents/big_data/

# 6. Run type checker
mypy agents/big_data/

# 7. Commit changes
git commit -m 'Add amazing feature'

# 8. Push to branch
git push origin feature/amazing-feature

# 9. Create Pull Request
```

### Code Standards

```python
# Code style
- Follow PEP 8
- Use type hints
- Write docstrings for all public functions
- Keep functions under 50 lines
- Maximum line length: 88 characters

# Testing
- Write unit tests for all new features
- Maintain >90% test coverage
- Use pytest fixtures
- Mock external dependencies

# Documentation
- Update README.md for new features
- Add API documentation
- Include usage examples
```
