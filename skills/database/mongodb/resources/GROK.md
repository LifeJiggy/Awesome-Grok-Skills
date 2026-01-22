# MongoDB

## Overview

MongoDB is a leading NoSQL database that stores data in flexible, JSON-like documents with dynamic schemas. This skill covers MongoDB deployment, data modeling, query optimization, and operational management. MongoDB's document model suits modern application development with evolving requirements and semi-structured data patterns.

## Core Capabilities

Document data model supports nested structures, arrays, and varied document shapes within collections. Sharding enables horizontal scaling across clusters for large datasets and high throughput. Replica sets provide high availability with automatic failover and data redundancy. Aggregation framework supports complex data transformations with a pipeline approach.

Index types including single field, compound, text, 2dsphere, and hashed address various query patterns. Atlas managed service provides cloud deployment with automated operations. Change streams enable real-time data synchronization and event-driven architectures. Time-series collections optimize storage and queries for temporal data.

## Usage Examples

```python
from mongodb import MongoDB

mongo = MongoDB()

mongo.create_cluster(
    name="production-cluster",
    cluster_type="sharded_cluster",
    mongo_version="7.0"
)

mongo.add_replica_set_member(0, "mongo1:27017", priority=2)
mongo.add_replica_set_member(1, "mongo2:27017", priority=1)
mongo.add_replica_set_member(2, "mongo3:27017", priority=1, arbiter=True)

mongo.add_shard("shard01", "rs-replica1")

mongo.configure_config_server("config-rs")

mongo.configure_mongos()

mongo.create_database("myapp")

mongo.create_collection(
    "myapp",
    "users",
    options={"capped": False, "size": None}
)

mongo.create_index(
    "myapp",
    "users",
    keys=[{"field": "email", "direction": "asc"}],
    index_type="single",
    options={"unique": True}
)

mongo.create_compound_index(
    "myapp",
    "orders",
    keys=[
        {"field": "customer_id", "direction": "asc"},
        {"field": "order_date", "direction": -1}
    ]
)

mongo.create_text_index(
    "myapp",
    "products",
    fields=[
        {"field": "name", "weight": 10},
        {"field": "description", "weight": 5}
    ],
    default_language="english"
)

mongo.create_2dsphere_index(
    "myapp",
    "stores",
    "location"
)

user = mongo.create_user(
    username="app_user",
    password="secure_password",
    roles=[{"role": "readWrite", "db": "myapp"}]
)

mongo.create_view(
    "myapp",
    "active_users_view",
    source_collection="users",
    pipeline=[{"$match": {"status": "active"}}]
)

change_stream = mongo.configure_change_stream(
    "myapp",
    "orders",
    pipeline=[{"$match": {"operationType": "insert"}}]
)

aggregation = mongo.create_aggregation_pipeline([
    {"$match": {"status": "completed"}},
    {"$group": {"_id": "$customer_id", "total": {"$sum": "$amount"}}},
    {"$sort": {"total": -1}}
])

atlas_cluster = mongo.create_atlas_cluster(
    name="my-atlas-cluster",
    provider="AWS",
    instance_size="M40",
    region="us-east-1",
    backup_enabled=True
)

mongo.configure_performance_advisor("my-atlas-cluster")
```

## Best Practices

Design schemas around application query patterns rather than normalizing data. Use embedded documents for one-to-many relationships accessed together. Consider document size limits and normalize when documents become too large. Index common query predicates and sort fields.

Use proper sharding keys to ensure even data distribution and efficient queries. Implement proper authentication and authorization for production deployments. Monitor cluster health, connection pool usage, and query performance. Plan capacity for growth and implement proper backup and disaster recovery.

## Related Skills

- NoSQL (document database concepts)
- Database Administration (general DBA skills)
- Database Administration (PostgreSQL)
- Data Engineering (data pipeline development)

## Use Cases

Content management systems use MongoDB for flexible document storage of articles and media. Real-time analytics leverage change streams for streaming data pipelines. Mobile backends benefit from MongoDB's flexible schema for evolving data models. IoT platforms store time-series sensor data with efficient queries. Gaming applications use MongoDB for player profiles and game state.
