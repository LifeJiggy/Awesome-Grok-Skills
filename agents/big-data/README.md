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
