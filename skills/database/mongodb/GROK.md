---
name: "MongoDB Operations"
version: "2.0.0"
description: "Comprehensive MongoDB administration toolkit with document modeling, aggregation pipelines, replica set management, sharding, change streams, and performance optimization for production MongoDB deployments"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["database", "mongodb", "nosql", "document-modeling", "aggregation", "sharding"]
category: "database"
personality: "mongodb-specialist"
use_cases: ["document modeling", "aggregation pipelines", "replica set management", "sharding", "change streams"]
---

# MongoDB Operations

> Production-grade MongoDB administration framework providing document modeling, aggregation pipelines, replica set management, sharding strategies, change streams, and performance optimization for reliable MongoDB deployments.

## Overview

The MongoDB Operations module provides a comprehensive toolkit for managing MongoDB in production environments. It implements document schema design with validation rules, aggregation pipeline construction with optimization, replica set monitoring and failover management, sharding strategy selection and balancer configuration, change stream processing for real-time data pipelines, and performance analysis with index optimization. Every operation includes retry logic, connection pooling, and structured logging.

## Core Capabilities

### 1. Document Modeling and Schema Design
- Schema validation with JSON Schema
- Reference vs embedding strategy guidance
- Polymorphic pattern implementation
- Attribute pattern for variable fields
- Bucket pattern for time-series data
- Schema versioning and migration

### 2. Aggregation Pipeline Builder
- Pipeline stage construction with type safety
- Pipeline optimization and explain analysis
- $lookup (join) optimization
- $graphLookup for hierarchical data
- $facet for multi-pipeline analysis
- $unionWith for cross-collection aggregation

### 3. Replica Set Management
- Health monitoring and election tracking
- Oplog analysis and lag monitoring
- Read preference configuration
- Write concern management
- Automatic failover handling
- Arbiter management

### 4. Sharding Strategy
- Hashed sharding for even distribution
- Range sharding for range queries
- Zone sharding for data locality
- Shard key selection guidance
- Balancer configuration and monitoring
- Chunk migration tracking

### 5. Change Streams
- Real-time change event processing
- Pipeline filtering for relevant changes
- Resume token management for reliability
- Full document lookup on updates
- Error recovery and reconnection

### 6. Performance Optimization
- Index usage analysis and recommendations
- Query plan analysis (explain)
- Slow query detection and profiling
- Connection pool monitoring
- Storage engine metrics
- WiredTiger cache analysis

## Usage Examples

### Document Schema Validation

```python
from mongodb import SchemaBuilder, Validator

schema = SchemaBuilder(collection="users")

schema.add_validation(
    validator=Validator({
        "bsonType": "object",
        "required": ["email", "name", "created_at"],
        "properties": {
            "email": {"bsonType": "string", "pattern": "^.+@.+$"},
            "name": {"bsonType": "string", "minLength": 1, "maxLength": 100},
            "age": {"bsonType": "int", "minimum": 0, "maximum": 150},
            "roles": {
                "bsonType": "array",
                "items": {"bsonType": "string", "enum": ["admin", "user", "viewer"]},
            },
            "created_at": {"bsonType": "date"},
        },
    }),
    level="strict",  # strict | moderate | off
)

schema.create()
```

### Aggregation Pipeline

```python
from mongodb import AggregationPipeline, Stage

pipeline = AggregationPipeline(collection="orders")

pipeline.add_stage(Stage.MATCH({
    "status": "completed",
    "created_at": {"$gte": "2024-01-01"},
}))

pipeline.add_stage(Stage.UNWIND("$items"))

pipeline.add_stage(Stage.GROUP(
    _id={"product": "$items.product_id", "month": {"$month": "$created_at"}},
    total_quantity={"$sum": "$items.quantity"},
    total_revenue={"$sum": {"$multiply": ["$items.price", "$items.quantity"]}},
    avg_order_value={"$avg": "$total"},
))

pipeline.add_stage(Stage.SORT({"total_revenue": -1}))

pipeline.add_stage(Stage.LIMIT(20))

# Execute and analyze
results = pipeline.execute()
explain = pipeline.explain()
print(f"Pipeline stages: {explain.stages}")
print(f"Execution time: {explain.execution_time_ms:.1f}ms")
print(f"Documents examined: {explain.total_docs_examined}")
```

### Change Stream Processing

```python
from mongodb import ChangeStream, OperationType

stream = ChangeStream(
    collection="inventory",
    pipeline=[
        {"$match": {"operationType": {"$in": ["insert", "update"]}}},
        {"$match": {"fullDocument.quantity": {"$lt": 10}}},
    ],
)

# Process changes with automatic resume
for change in stream.listen(resume_token=None):
    print(f"Low stock alert: {change.full_document}")
    print(f"  Product: {change.full_document['product_id']}")
    print(f"  Quantity: {change.full_document['quantity']}")
    print(f"  Operation: {change.operation_type}")

    # Save resume token for reliability
    stream.save_resume_token(change.resume_token)
```

### Shard Management

```python
from mongodb import ShardManager, ShardingStrategy

shard_mgr = ShardManager()

# Enable sharding with hashed key
shard_mgr.enable_sharding(
    database="ecommerce",
    collection="orders",
    strategy=ShardingStrategy.HASHED,
    shard_key="customer_id",
)

# Configure zones for data locality
shard_mgr.add_zone_tag(
    shard="shard-us-east-1",
    zone="us-east",
    min_value={"region": "US"},
    max_value={"region": "USZZ"},
)

# Monitor balancer
status = shard_mgr.balancer_status()
print(f"Balancer active: {status.active}")
print(f"Currently balancing: {status.currently_balancing}")
print(f"Chunks migrated today: {status.chunks_migrated_today}")
```

### Index Optimization

```python
from mongodb import IndexAnalyzer, QueryProfiler

analyzer = IndexAnalyzer(collection="orders")

# Analyze index usage
usage = analyzer.index_usage_stats()
for idx in usage:
    print(f"  {idx.name}: {idx.accesses_ops} ops, {idx.size_mb:.1f} MB")

# Get recommendations
recommendations = analyzer.recommendations()
for rec in recommendations:
    print(f"  Recommendation: {rec.description}")
    print(f"    Impact: {rec.estimated_impact}")

# Profile slow queries
profiler = QueryProfiler(database="ecommerce", threshold_ms=100)
slow_queries = profiler.get_slow_queries(limit=5)
for q in slow_queries:
    print(f"  {q.duration_ms:.0f}ms: {q.command}")
```

## Best Practices

### Document Design
- Embed when data is accessed together; reference when data is independent
- Keep document size under 16MB; use GridFS for large files
- Use the bucket pattern for time-series data to avoid unbounded array growth
- Design schemas for your query patterns, not your data structure

### Aggregation
- Place $match and $sort before $lookup to reduce documents processed
- Use $project early to limit fields passed to subsequent stages
- Create indexes that support your aggregation pipeline's first $match stage
- Use $facet sparingly — it runs multiple pipelines on the same data

### Sharding
- Choose shard keys with high cardinality and low frequency
- Avoid monotonically increasing shard keys (like ObjectId) for write-heavy workloads
- Monitor chunk distribution — uneven chunks indicate poor shard key choice
- Use zone sharding for multi-region deployments

### Performance
- Use covered queries (index-only scans) whenever possible
- Limit result sets with .limit() — never fetch unbounded results
- Monitor the WiredTiger cache — evictions indicate memory pressure
- Enable the profiler only in development or for targeted troubleshooting

## Related Modules

- **database-administration**: Cross-database administration and connection pooling
- **query-optimization**: Query performance analysis applicable to MongoDB
- **data-modeling**: Schema design patterns and entity relationships
- **replication**: MongoDB replica set and high availability configuration