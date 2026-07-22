---
name: nosql
category: database
version: 1.0.0
tags: [database, nosql]
---

# Nosql

## Overview
Comprehensive nosql within database domain.

## Usage
```python
from nosql import NoSQLEngine
engine = NoSQLEngine()
```

## Advanced Configuration

### MongoDB Configuration

```python
from nosql import MongoDBConfig, ConnectionPool

# Advanced MongoDB configuration
mongo_config = MongoDBConfig(
    connection_string="mongodb://user:password@localhost:27017",
    database="myapp",
    replica_set="rs0",
    read_preference="secondaryPreferred",
    write_concern={"w": "majority", "wtimeout": 5000, "j": True},
    read_concern={"level": "majority"},
    connection_pool=ConnectionPool(
        min_pool_size=5,
        max_pool_size=50,
        max_idle_time_ms=30000,
        wait_queue_timeout_ms=5000,
    ),
    tls={
        "enabled": True,
        "ca_file": "/path/to/ca.pem",
        "cert_file": "/path/to/client.pem",
        "key_file": "/path/to/client-key.pem",
    },
    retry_writes=True,
    retry_reads=True,
)

engine = NoSQLEngine(mongo_config=mongo_config)
```

### Cassandra Configuration

```python
from nosql import CassandraConfig, ClusterConfig

# Advanced Cassandra configuration
cassandra_config = CassandraConfig(
    cluster=ClusterConfig(
        contact_points=["cassandra1", "cassandra2", "cassandra3"],
        port=9042,
        keyspace="myapp",
        protocol_version=4,
        load_balancing_policy="DCAwareRoundRobinPolicy",
        consistency_level="QUORUM",
        serial_consistency_level="LOCAL_SERIAL",
    ),
    connection={
        "idle_timeout": 60,
        "heartbeat_interval": 30,
        "max_schema_agreement_wait": 10,
    },
    retry_policy={
        "retry_on_timeout": True,
        "max_retries": 3,
    },
)

engine = NoSQLEngine(cassandra_config=cassandra_config)
```

### Redis Configuration

```python
from nosql import RedisConfig, SentinelConfig

# Advanced Redis configuration
redis_config = RedisConfig(
    host="localhost",
    port=6379,
    db=0,
    password="your_password",
    ssl=True,
    ssl_certfile="/path/to/client.crt",
    ssl_keyfile="/path/to/client.key",
    ssl_ca_certs="/path/to/ca.crt",
    connection_pool={
        "max_connections": 50,
        "retry_on_timeout": True,
        "socket_timeout": 5,
        "socket_connect_timeout": 5,
        "health_check_interval": 30,
    },
    sentinel=SentinelConfig(
        sentinels=[("sentinel1", 26379), ("sentinel2", 26379)],
        service_name="mymaster",
        socket_timeout=0.1,
    ),
)

engine = NoSQLEngine(redis_config=redis_config)
```

### DynamoDB Configuration

```python
from nosql import DynamoDBConfig, TableConfig

# Advanced DynamoDB configuration
dynamodb_config = DynamoDBConfig(
    region="us-east-1",
    endpoint="http://localhost:8000",  # For local development
    tables=[
        TableConfig(
            name="Users",
            key_schema=[
                {"AttributeName": "user_id", "KeyType": "HASH"},
            ],
            attribute_definitions=[
                {"AttributeName": "user_id", "AttributeType": "S"},
                {"AttributeName": "email", "AttributeType": "S"},
            ],
            global_secondary_indexes=[
                {
                    "IndexName": "email-index",
                    "KeySchema": [{"AttributeName": "email", "KeyType": "HASH"}],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
                }
            ],
            provisioned_throughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
        ),
    ],
)

engine = NoSQLEngine(dynamodb_config=dynamodb_config)
```

## Architecture Patterns

### Data Access Layer Pattern

```python
from nosql import DataAccessLayer, Repository

class UserRepository(Repository):
    def __init__(self, db):
        self.collection = db.users
    
    def find_by_id(self, user_id):
        return self.collection.find_one({"_id": user_id})
    
    def find_by_email(self, email):
        return self.collection.find_one({"email": email})
    
    def create(self, user_data):
        return self.collection.insert_one(user_data)
    
    def update(self, user_id, update_data):
        return self.collection.update_one(
            {"_id": user_id},
            {"$set": update_data}
        )
    
    def delete(self, user_id):
        return self.collection.delete_one({"_id": user_id})
    
    def find_all(self, filter_query=None, limit=100):
        return list(self.collection.find(filter_query).limit(limit))

# Usage
dal = DataAccessLayer(mongo_config)
user_repo = UserRepository(dal.db)
user = user_repo.find_by_id("user123")
```

### CQRS Pattern

```python
from nosql import CQRSHandler, Command, Query

class CreateUserCommand(Command):
    def __init__(self, user_data):
        self.user_data = user_data

class GetUserQuery(Query):
    def __init__(self, user_id):
        self.user_id = user_id

class UserCQRSHandler(CQRSHandler):
    def __init__(self, write_db, read_db):
        self.write_db = write_db
        self.read_db = read_db
    
    def handle_command(self, command):
        if isinstance(command, CreateUserCommand):
            result = self.write_db.users.insert_one(command.user_data)
            # Publish event for read model update
            self.publish_event("user_created", {"user_id": str(result.inserted_id)})
            return result
    
    def handle_query(self, query):
        if isinstance(query, GetUserQuery):
            return self.read_db.users.find_one({"_id": query.user_id})

# Usage
handler = UserCQRSHandler(write_db=mongo_write, read_db=mongo_read)
handler.handle_command(CreateUserCommand({"name": "John", "email": "john@example.com"}))
user = handler.handle_query(GetUserQuery("user123"))
```

### Event Sourcing Pattern

```python
from nosql import EventStore, Event, AggregateRoot

class UserAggregate(AggregateRoot):
    def __init__(self, user_id):
        self.user_id = user_id
        self.name = None
        self.email = None
        self.events = []
    
    def create(self, name, email):
        self.apply_event(Event(
            type="UserCreated",
            data={"user_id": self.user_id, "name": name, "email": email}
        ))
    
    def change_email(self, new_email):
        self.apply_event(Event(
            type="EmailChanged",
            data={"user_id": self.user_id, "new_email": new_email}
        ))
    
    def apply_event(self, event):
        if event.type == "UserCreated":
            self.name = event.data["name"]
            self.email = event.data["email"]
        elif event.type == "EmailChanged":
            self.email = event.data["new_email"]
        self.events.append(event)

class EventStore:
    def __init__(self, db):
        self.events_collection = db.events
    
    def save_events(self, aggregate_id, events):
        for event in events:
            self.events_collection.insert_one({
                "aggregate_id": aggregate_id,
                "type": event.type,
                "data": event.data,
                "timestamp": event.timestamp,
            })
    
    def get_events(self, aggregate_id):
        return list(self.events_collection.find({"aggregate_id": aggregate_id}))
```

## Integration Guide

### SQLAlchemy Integration

```python
from nosql import SQLAlchemyNoSQLAdapter

adapter = SQLAlchemyNoSQLAdapter()

# Use NoSQL with SQLAlchemy-style queries
session = adapter.create_session(mongo_config)
users = session.query("users").filter({"age": {"$gte": 18}}).limit(10).all()
```

### PyMongo Integration

```python
from nosql import PyMongoAdapter

adapter = PyMongoAdapter()

# Direct PyMongo integration
client = adapter.create_client(mongo_config)
db = client.myapp
collection = db.users

# Insert document
collection.insert_one({"name": "John", "email": "john@example.com"})

# Find documents
users = collection.find({"age": {"$gte": 18}})
```

## Performance Optimization

### Connection Pool Optimization

```python
from nosql import ConnectionPoolOptimizer

optimizer = ConnectionPoolOptimizer(
    min_connections=5,
    max_connections=50,
    idle_timeout=30000,
    max_lifetime=1800000,
)

# Optimize connection pool
optimizer.optimize(mongo_config)
print(f"Optimal pool size: {optimizer.optimal_size}")
```

### Query Optimization

```python
from nosql import QueryOptimizer

optimizer = QueryOptimizer()

# Analyze query performance
analysis = optimizer.analyze_query(
    collection="users",
    query={"email": "john@example.com"},
    explain_output=True,
)

print(f"Execution time: {analysis.execution_time_ms:.2f}ms")
print(f"Documents examined: {analysis.docs_examined}")
print(f"Index used: {analysis.index_used}")
print(f"Recommendations: {analysis.recommendations}")
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Connection Pool Exhaustion

**Symptom**: Too many connections error

**Solution**:
```python
# Increase pool size
config.connection_pool["max_connections"] = 100

# Add connection pooling
from nosql import ConnectionPoolManager
pool = ConnectionPoolManager(config, max_connections=50)
```

#### 2. Slow Queries

**Symptom**: Query performance degrades

**Solution**:
```python
# Add indexes
collection.create_index([("email", 1)], unique=True)

# Analyze query
from nosql import QueryAnalyzer
analyzer = QueryAnalyzer()
analyzer.analyze(collection, {"email": "test@example.com"})
```

#### 3. Replica Set Issues

**Symptom**: Replication lag or failover problems

**Solution**:
```python
# Check replica status
status = client.admin.command("replSetGetStatus")
print(f"Primary: {status['myState']}")
print(f"Syncing to: {status['syncingTo']}")

# Configure read preference
from pymongo import ReadPreference
collection = db.users.with_options(
    read_preference=ReadPreference.SECONDARY_PREFERRED
)
```

## API Reference

### Core Classes

#### `NoSQLEngine`
```python
class NoSQLEngine:
    def __init__(self, mongo_config: Optional[MongoDBConfig] = None, cassandra_config: Optional[CassandraConfig] = None, redis_config: Optional[RedisConfig] = None) -> None: ...
    def connect(self) -> None: ...
    def disconnect(self) -> None: ...
    def get_collection(self, name: str) -> Collection: ...
    def execute_query(self, query: str) -> Result: ...
```

## Data Models

### Document Schema

```json
{
  "_id": "user123",
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "metadata": {
    "login_count": 15,
    "last_login": "2024-01-15T09:00:00Z"
  }
}
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY nosql/ /app/nosql/
WORKDIR /app

ENV MONGODB_URI=mongodb://localhost:27017
ENV REDIS_URL=redis://localhost:6379

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from nosql import health_check; health_check()"

CMD ["python", "-m", "nosql.server"]
```

## Monitoring & Observability

### Metrics Collection

```python
from nosql import MetricsCollector

collector = MetricsCollector(backend="prometheus")

collector.register_metric("nosql_connections_active", type="gauge")
collector.register_metric("nosql_query_duration", type="histogram")
collector.register_metric("nosql_operations_total", type="counter")

collector.set("nosql_connections_active", active_connections)
collector.observe("nosql_query_duration", query_time_ms)
collector.inc("nosql_operations_total")
```

## Testing Strategy

### Unit Tests

```python
import pytest
from nosql import NoSQLEngine, MongoDBConfig

class TestNoSQL:
    def setup_method(self):
        self.config = MongoDBConfig(connection_string="mongodb://localhost:27017", database="test")
        self.engine = NoSQLEngine(mongo_config=self.config)
    
    def test_insert_document(self):
        collection = self.engine.get_collection("test")
        result = collection.insert_one({"name": "test"})
        assert result.inserted_id is not None
    
    def test_find_document(self):
        collection = self.engine.get_collection("test")
        collection.insert_one({"name": "test"})
        doc = collection.find_one({"name": "test"})
        assert doc is not None
```

## Versioning & Migration

### Changelog

#### v2.0.0 (2024-01-15)
- **Breaking**: New config API
- **Added**: Cassandra support
- **Added**: DynamoDB support
- **Improved**: 2x faster queries
- **Fixed**: Connection pool leaks

## Glossary

| Term | Definition |
|------|------------|
| **Document Store** | Database storing JSON-like documents |
| **Key-Value Store** | Database storing key-value pairs |
| **Column Family** | Database organizing data in columns |
| **CAP Theorem** | Consistency, Availability, Partition tolerance tradeoff |
| ** eventual Consistency** | Model where all replicas converge |

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/nosql.git
cd nosql
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT License

Copyright (c) 2024 NoSQL Contributors

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

---

*Last updated: 2024-01-15*
*Version: 2.0.0*

## Advanced Patterns

### Data Pipeline Pattern

```python
from nosql import DataPipeline, PipelineStage

pipeline = DataPipeline(stages=[
    PipelineStage(
        name="ingestion",
        type="source",
        source="kafka",
        config={"topic": "events"},
    ),
    PipelineStage(
        name="transformation",
        type="transform",
        processor=lambda x: transform_event(x),
    ),
    PipelineStage(
        name="validation",
        type="validate",
        schema=event_schema,
    ),
    PipelineStage(
        name="storage",
        type="sink",
        sink="redis",
        config={"prefix": "events:"},
    ),
])

# Execute pipeline
pipeline.execute()
```

### Data Partitioning

```python
from nosql import PartitionManager

partition_manager = PartitionManager(
    strategy="hash",
    num_partitions=16,
    key_extractor=lambda doc: doc["user_id"],
)

# Partition data
for doc in documents:
    partition = partition_manager.get_partition(doc)
    print(f"Document {doc['id']} goes to partition {partition}")
```

### Data Sharding

```python
from nosql import ShardManager

shard_manager = ShardManager(
    shards=[
        {"host": "shard1", "port": 27017},
        {"host": "shard2", "port": 27017},
        {"host": "shard3", "port": 27017},
    ],
    shard_key="user_id",
    balancing_strategy="range",
)

# Route queries to shards
shard = shard_manager.get_shard(user_id=123)
result = shard.query("SELECT * FROM users WHERE id = 123")
```

### Data Replication

```python
from nosql import ReplicationManager

replication = ReplicationManager(
    primary=r,
    replicas=[r1, r2],
    sync_mode="async",
    heartbeat_interval=10,
)

# Check replication status
status = replication.get_status()
print(f"Primary lag: {status.primary_lag_ms}ms")
print(f"Replicas: {status.replica_count}")
print(f"Healthy: {status.is_healthy}")
```

### Data Archival

```python
from nosql import ArchivalManager

archival = ArchivalManager(
    redis_client=r,
    archive_storage="s3",
    archive_bucket="my-archive",
    archive_prefix="redis/",
    retention_days=30,
    compression=True,
)

# Archive old data
archived = archival.archive(
    pattern="session:*",
    older_than_days=30,
)
print(f"Archived {archived} keys")

# Restore archived data
archived_data = archival.restore(
    archive_id="archive-2024-01-15",
    keys=["session:123", "session:456"],
)
```

## Advanced Patterns

### Caching Strategies

```python
from nosql import CacheManager, CacheStrategy

cache = CacheManager(
    strategy=CacheStrategy.WRITE_THROUGH,
    ttl=300,
    max_size=10000,
    eviction_policy="lru",
)

@cache.cache(ttl=600)
def get_user(user_id):
    return db.users.find_one({"_id": user_id})

# Cache invalidation
cache.invalidate("user:123")
cache.invalidate_pattern("user:*")
```

### Data Serialization

```python
from nosql import Serializer, Compressor

serializer = Serializer(
    format="json",
    compression="lz4",
    encryption=None,
)

# Serialize document
data = {"name": "John", "age": 30}
serialized = serializer.serialize(data)
print(f"Serialized size: {len(serialized)} bytes")

# Deserialize
deserialized = serializer.deserialize(serialized)
assert deserialized == data
```

### Connection Monitoring

```python
from nosql import ConnectionMonitor

monitor = ConnectionMonitor(
    redis_client=r,
    check_interval=30,
    alert_threshold=0.8,
)

# Monitor connections
monitor.start()
alerts = monitor.get_alerts()
for alert in alerts:
    print(f"Alert: {alert.message}")
    print(f"Severity: {alert.severity}")
```

### Batch Operations

```python
from nosql import BatchProcessor

processor = BatchProcessor(
    redis_client=r,
    batch_size=1000,
    parallel_workers=4,
)

# Batch operations
data = {f"key:{i}": f"value:{i}" for i in range(10000)}
processor.batch_set(data)

# Batch with callbacks
processor.batch_with_callbacks(
    operations=[("set", f"key:{i}", f"value:{i}") for i in range(10000)],
    on_success=lambda op: print(f"Success: {op}"),
    on_failure=lambda op, err: print(f"Failed: {op}, Error: {err}"),
)
```

### Transaction Support

```python
from nosql import TransactionManager

tx_manager = TransactionManager(redis_client=r)

# Execute transaction
with tx_manager.transaction() as tx:
    tx.set("account:1:balance", "1000")
    tx.set("account:2:balance", "500")
    tx.incrby("account:1:balance", -100)
    tx.incrby("account:2:balance", 100)
    # Auto-commit on successful exit
```

### Pub/Sub Messaging

```python
from nosql import PubSubManager

pubsub = PubSubManager(redis_client=r)

# Publisher
def publish_event(channel, data):
    pubsub.publish(channel, data)

# Subscriber
def subscribe_to_events(channel, callback):
    pubsub.subscribe(channel, callback)

# Usage
subscribe_to_events("user.events", lambda msg: print(f"Received: {msg}"))
publish_event("user.events", {"type": "created", "user_id": 123})
```

### Lua Scripting

```python
from nosql import LuaScript

script = LuaScript(redis_client=r)

# Define Lua script
increase_with_limit = """
local key = KEYS[1]
local increment = tonumber(ARGV[1])
local limit = tonumber(ARGV[2])
local current = tonumber(redis.call('GET', key) or 0)
if current + increment <= limit then
    redis.call('INCRBY', key, increment)
    return current + increment
else
    return -1
end
"""

# Execute script
result = script.execute(increase_with_limit, keys=["counter"], args=[10, 100])
print(f"New value: {result}")
```

### Geospatial Operations

```python
from nosql import GeoSpatial

geo = GeoSpatial(redis_client=r)

# Add locations
geo.add("stores", "store1", longitude=-73.9857, latitude=40.7484)
geo.add("stores", "store2", longitude=-73.9851, latitude=40.7490)
geo.add("stores", "store3", longitude=-73.9847, latitude=40.7488)

# Find nearby stores
nearby = geo.nearby("stores", longitude=-73.9857, latitude=40.7484, radius=1000)
print(f"Nearby stores: {nearby}")

# Calculate distance
distance = geo.distance("stores", "store1", "store2")
print(f"Distance: {distance:.2f} meters")
```

### Stream Processing

```python
from nosql import StreamProcessor

processor = StreamProcessor(redis_client=r)

# Create stream
processor.create_stream("events")

# Add events
processor.add("events", {"type": "user.created", "user_id": 123})
processor.add("events", {"type": "order.placed", "order_id": 456})

# Read events
events = processor.read("events", count=10)
for event in events:
    print(f"Event: {event}")
```

### Time Series Operations

```python
from nosql import TimeSeries

ts = TimeSeries(redis_client=r)

# Add data points
ts.add("sensor:temperature", value=22.5, timestamp=1705312200)
ts.add("sensor:temperature", value=22.7, timestamp=1705312260)
ts.add("sensor:temperature", value=23.0, timestamp=1705312320)

# Query range
data = ts.range("sensor:temperature", from_ts=1705312200, to_ts=1705312400)
print(f"Data points: {len(data)}")

# Get last value
last = ts.get("sensor:temperature")
print(f"Last value: {last}")
```

### HyperLogLog Operations

```python
from nosql import HyperLogLog

hll = HyperLogLog(redis_client=r)

# Add unique items
hll.add("unique_visitors", "user1")
hll.add("unique_visitors", "user2")
hll.add("unique_visitors", "user1")  # Duplicate, won't affect count

# Get count
count = hll.count("unique_visitors")
print(f"Unique visitors: {count}")
```

### Bloom Filter Operations

```python
from nosql import BloomFilter

bf = BloomFilter(redis_client=r, key="email_bloom", error_rate=0.01, capacity=1000000)

# Add items
bf.add("user1@example.com")
bf.add("user2@example.com")

# Check existence
exists = bf.exists("user1@example.com")
print(f"Exists: {exists}")  # True

not_exists = bf.exists("user3@example.com")
print(f"Exists: {not_exists}")  # False (with 1% error rate)
```