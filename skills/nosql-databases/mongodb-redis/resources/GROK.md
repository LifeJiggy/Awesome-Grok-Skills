# NoSQL Database Agent

## Overview

The **NoSQL Database Agent** provides comprehensive management for document, key-value, column-family, and graph databases including MongoDB, Redis, Cassandra, and Elasticsearch. This agent enables flexible data modeling and scalable data operations.

## Core Capabilities

### 1. MongoDB Operations
Document database management:
- **CRUD Operations**: Create, read, update, delete
- **Aggregation Pipeline**: Data transformation
- **Index Management**: Performance optimization
- **Schema Validation**: Data quality enforcement
- **Sharding**: Horizontal scaling

### 2. Redis Operations
Key-value store management:
- **String Operations**: Basic key-value
- **Hash Operations**: Field-value pairs
- **List Operations**: Ordered collections
- **Set Operations**: Unique collections
- **Pub/Sub**: Message publishing
- **Cluster Management**: Distributed Redis

### 3. Cassandra Operations
Column-family database management:
- **CQL Queries**: Cassandra Query Language
- **Data Modeling**: Denormalized schemas
- **Replication Setup**: Multi-datacenter
- **Compaction Strategies**: Storage optimization
- **Tuning**: Performance configuration

### 4. Elasticsearch Operations
Search and analytics:
- **Index Management**: Index creation, mapping
- **Query DSL**: Search queries
- **Aggregations**: Analytics pipelines
- **Index Lifecycle**: Hot-warm-cold architecture
- **Cross-Cluster Search**: Multi-cluster queries

## Usage Examples

### MongoDB

```python
from nosql import MongoDBManager

mongo = MongoDBManager()
mongo.connect("mongodb://localhost:27017")
mongo.create_database('myapp', 'mongodb')
mongo.insert_document('users', {'name': 'John', 'age': 30})
docs = mongo.find_documents('users', {'age': {'$gt': 25}}, limit=10)
result = mongo.aggregate('orders', [
    {'$match': {'status': 'completed'}},
    {'$group': {'_id': '$product', 'total': {'$sum': '$quantity'}}}
])
```

### Redis

```python
from nosql import RedisManager

redis = RedisManager()
redis.connect('localhost', 6379)
redis.set_key('user:1', {'name': 'John'}, expiration_seconds=3600)
value = redis.get_key('user:1')
hash_ops = redis.hash_operations()
pub_result = redis.publish_subscribe('notifications', 'New message!')
```

### Elasticsearch

```python
from nosql import ElasticsearchManager

es = ElasticsearchManager()
es.connect(['localhost:9200'])
es.create_index('products', {'properties': {'name': {'type': 'text'}}})
es.index_document('products', {'name': 'Laptop', 'price': 999}, doc_id='p1')
results = es.search('products', {'query': {'match': {'name': 'laptop'}}})
```

## Data Models

### Document Model (MongoDB)
```json
{
  "_id": "123",
  "name": "John Doe",
  "email": "john@example.com",
  "addresses": [
    {"type": "home", "city": "NYC"},
    {"type": "work", "city": "LA"}
  ],
  "orders": [
    {"product": "Laptop", "price": 999}
  ]
}
```

### Key-Value Model (Redis)
```
user:12345 → {name: "John", email: "john@example.com"}
session:abc → {last_activity: "2024-01-01"}
```

### Column Model (Cassandra)
```cql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    name TEXT,
    email TEXT,
    created_at TIMESTAMP
);
```

### Document Index (Elasticsearch)
```json
{
  "index": "products",
  "mappings": {
    "properties": {
      "name": {"type": "text"},
      "price": {"type": "float"},
      "category": {"type": "keyword"}
    }
  }
}
```

## Use Cases

### MongoDB
- Content management systems
- User profiles and preferences
- Product catalogs
- Mobile backends
- Real-time analytics

### Redis
- Session storage
- Caching layer
- Rate limiting
- Leaderboards
- Message queues

### Cassandra
- Time-series data
- IoT sensor data
- Messaging systems
- Fraud detection
- Write-heavy workloads

### Elasticsearch
- Full-text search
- Log aggregation
- Application monitoring
- Business analytics
- Security analytics

## Performance Optimization

### MongoDB
- **Indexing**: Compound indexes, covered queries
- **Query Optimization**: Explain plans, $hint
- **Sharding**: Shard key selection
- **Aggregation**: Pipeline optimization

### Redis
- **Memory Optimization**: Data type selection
- **Clustering**: Hash slots, rebalancing
- **Persistence**: RDB/AOF tuning
- **Pipeline**: Batch operations

### Cassandra
- **Data Modeling**: Denormalization, duplicate data
- **Compaction**: Size-tiered, level-tiered
- **Consistency**: Read/write consistency levels
- **Batch Statements**: Counter batching

### Elasticsearch
- **Index Optimization**: Shards, replicas
- **Query Optimization**: Filter context, pagination
- **Aggregations**: Fielddata, doc values
- **ILM Policies**: Index lifecycle

## Scaling Strategies

### Vertical Scaling
- Increase memory
- Add CPU cores
- Fast storage (SSD)
- Network bandwidth

### Horizontal Scaling
- Sharding (MongoDB, Elasticsearch)
- Clustering (Redis, Cassandra)
- Read replicas
- Data partitioning

## Data Consistency

### Consistency Models

| Database | Consistency | Options |
|----------|-------------|---------|
| MongoDB | Eventual | Strong, causal, eventual |
| Redis | Strong | N/A (single-threaded) |
| Cassandra | Eventual | ONE, QUORUM, ALL |
| Elasticsearch | Eventual | Strong with primary |

### Trade-offs
- **Strong Consistency**: Slower writes, immediate reads
- **Eventual Consistency**: Faster writes, potential stale reads

## Security

### Authentication
- **MongoDB**: SCRAM, X.509 certificates
- **Redis**: Password, ACL
- **Cassandra**: Password, Kerberos
- **Elasticsearch**: Basic auth, LDAP, SAML

### Authorization
- **Role-Based Access Control**: Define roles
- **Field-Level Security**: Restrict access
- **Network Security**: Firewall rules, TLS

## Related Skills

- [Database Administration](../database-admin/db-management/README.md) - DBA tasks
- [Data Engineering](../data-engineering/data-pipelines/README.md) - Pipelines
- [Observability](../observability/monitoring/README.md) - Monitoring

---

**File Path**: `skills/nosql-databases/mongodb-redis/resources/nosql.py`
