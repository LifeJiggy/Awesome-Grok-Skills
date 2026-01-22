# NoSQL

## Overview

NoSQL databases provide flexible data models for applications that require scalability, schema flexibility, or specialized query patterns. This skill covers document, key-value, wide-column, and graph databases with their respective use cases and design patterns. NoSQL databases address limitations of traditional relational databases for specific workload requirements.

## Core Capabilities

Document databases like MongoDB store data in flexible JSON-like documents with nested structures. Key-value stores like Redis provide simple, high-performance lookups. Wide-column stores like Cassandra handle massive scale with tunable consistency. Graph databases like Neo4j model and query complex relationships efficiently.

Time-series databases like InfluxDB optimize for temporal data with automatic data retention. Schema flexibility enables rapid iteration without migration overhead. Horizontal scaling distributes data across clusters for capacity growth. Specialized query languages optimize for specific data models and access patterns.

## Usage Examples

```python
from nosql import NoSQL

nosql = NoSQL()

doc_db = nosql.create_document_database(
    name="app-database",
    db_type="mongodb",
    config={"version": "7.0", "storage_engine": "wiredTiger"}
)

doc_db.create_collection(
    collection_name="users",
    schema=nosql.create_document_schema(
        fields={
            "user_id": nosql.create_field_schema("user_id", "string"),
            "name": nosql.create_field_schema("name", "string"),
            "email": nosql.create_field_schema("email", "string"),
            "created_at": nosql.create_field_schema("created_at", "date"),
            "preferences": nosql.create_field_schema("preferences", "object")
        },
        required=["user_id", "name", "email"]
    )
)

doc_db.create_collection(
    collection_name="products",
    schema=nosql.create_document_schema(
        fields={
            "product_id": nosql.create_field_schema("product_id", "string"),
            "name": nosql.create_field_schema("name", "string"),
            "category": nosql.create_field_schema("category", "string"),
            "price": nosql.create_field_schema("price", "number"),
            "inventory": nosql.create_field_schema("inventory", "int"),
            "tags": nosql.create_field_schema("tags", ["string"]),
            "location": nosql.create_field_schema("location", "object")
        },
        required=["product_id", "name", "price"]
    )
)

nosql.create_text_index(
    db_name="app-database",
    collection_name="products",
    fields=["name", "description"],
    weights={"name": 10, "description": 5}
)

nosql.create_2dsphere_index(
    db_name="app-database",
    collection_name="products",
    field="location.geo"
)

nosql.configure_sharding(
    db_name="app-database",
    shard_key="product_category",
    shard_type="hashed"
)

nosql.configure_replication(
    db_name="app-database",
    replication_factor=3,
    write_concern="majority"
)

kv_store = nosql.create_key_value_store(
    name="session-store",
    provider="redis",
    config={"cluster": True, "persistence": "rdb"}
)

wide_column = nosql.create_wide_column_store(
    name="analytics-db",
    provider="cassandra",
    config={"version": "4.0"}
)

wide_column.create_keyspace(
    keyspace_name="analytics",
    replication={"class": "NetworkTopologyStrategy", "replication_factor": 3}
)

wide_column.create_column_family(
    keyspace_name="analytics",
    cf_name="user_events",
    columns=[
        {"name": "event_id", "type": "uuid"},
        {"name": "event_type", "type": "text"},
        {"name": "timestamp", "type": "timestamp"},
        {"name": "user_id", "type": "uuid"},
        {"name": "properties", "type": "map<text, text>"}
    ]
)

graph_db = nosql.create_graph_database(
    name="social-graph",
    provider="neo4j",
    config={"version": "5.0", "ha": True}
)

graph_db.create_node_label(
    label_name="User",
    properties=["user_id", "name", "email"]
)

graph_db.create_node_label(
    label_name="Product",
    properties=["product_id", "name", "category"]
)

graph_db.create_relationship_type(
    rel_type="PURCHASED",
    properties=["order_id", "timestamp", "amount"]
)

graph_db.create_relationship_type(
    rel_type="VIEWED",
    properties=["timestamp", "duration"]
)

query = nosql.create_graph_query(
    query_type="recommendation",
    cypher="""
    MATCH (u:User {user_id: $user_id})-[:PURCHASED]->(p:Product)<-[:PURCHASED]-(similar:User)-[:PURCHASED]->(recommended:Product)
    WHERE recommended.product_id <> p.product_id
    RETURN recommended, COUNT(*) as score
    ORDER BY score DESC
    LIMIT 10
    """
)

ts_db = nosql.create_time_series_database(
    name="metrics-db",
    provider="influxdb",
    config={"version": "2.7"}
)

ts_db.create_measurement(
    measurement_name="cpu_metrics",
    tags=["host", "region", "datacenter"],
    fields=["usage_user", "usage_system", "usage_idle"]
)

ts_db.create_measurement(
    measurement_name="request_metrics",
    tags=["endpoint", "method", "status_code"],
    fields=["latency_ms", "count"]
)

ts_db.create_retention_policy(
    policy_name="metrics_policy",
    duration="7d",
    replication=1
)

data_model = nosql.create_data_model(
    model_type="document",
    schema={
        "users": nosql.create_document_schema({}),
        "products": nosql.create_document_schema({}),
        "orders": nosql.create_document_schema({})
    }
)

data_model["access_patterns"] = [
    nosql.create_access_pattern(
        pattern_name="user_profile",
        query_type="find_one",
        fields=["user_id"],
        frequency="high"
    ),
    nosql.create_access_pattern(
        pattern_name="product_search",
        query_type="text_search",
        fields=["name", "description"],
        frequency="high"
    ),
    nosql.create_access_pattern(
        pattern_name="order_history",
        query_type="find_many",
        fields=["user_id", "created_at"],
        frequency="medium"
    )
]

nosql.create_consistency_config(
    db_name="app-database",
    consistency_level="majority",
    read_preference="primary"
)

nosql.create_backup_config(
    db_name="app-database",
    provider="cloud",
    schedule={"frequency": "daily", "time": "02:00", "timezone": "UTC"}
)
```

## Best Practices

Choose the right database type based on data model and access patterns. Design schemas around queries rather than normalizing data. Use appropriate indexing strategies for common access patterns. Implement proper data lifecycle management with TTL and archiving.

Configure consistency levels based on consistency requirements. Use sharding for horizontal scaling when needed. Monitor query performance and optimize indexes. Plan capacity for data growth and retention requirements. Implement backup and disaster recovery procedures.

## Related Skills

- MongoDB (document database)
- Redis (key-value store)
- Database Administration (general DBA)
- Data Modeling (schema design)

## Use Cases

Content management systems use document databases for flexible content structures. Real-time analytics use time-series databases for metrics and events. Social networks use graph databases for relationship-intensive queries. Gaming leaderboards use key-value stores for fast reads and writes. IoT platforms use wide-column stores for high-volume sensor data.
