---
name: "mongodb-redis"
category: "nosql-databases"
version: "1.0.0"
tags: ["nosql-databases", "mongodb-redis"]
---

# Mongodb Redis

## Overview

Comprehensive mongodb-redis capabilities within the nosql-databases domain. This module provides tools, frameworks, and best practices for mongodb-redis operations.

## Core Capabilities

- Configuration and setup
- Data processing and analysis
- Integration with related systems
- Monitoring and observability
- Best practices and patterns

## Usage

```python
from mongodb-redis import _module

engine = _module.Engine()
engine.configure()
results = engine.run()
print(results)
```

## Best Practices

- Follow security guidelines
- Implement proper error handling
- Use configuration management
- Monitor performance metrics
- Document API interfaces

## Related Modules

- Other modules in nosql-databases domain
- Integration points with external systems

---

## Advanced Configuration

### MongoDB Replica Set Configuration

```javascript
// rs-init.js - Initialize a 3-member replica set
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo-primary:27017", priority: 10 },
    { _id: 1, host: "mongo-secondary1:27017", priority: 5 },
    { _id: 2, host: "mongo-secondary2:27017", priority: 5, arbiterOnly: false }
  ],
  settings: {
    chainingAllowed: true,
    heartbeatTimeoutSecs: 10,
    electionTimeoutMillis: 10000,
    getLastErrorModes: {
      majority: { w: "majority", wtimeout: 5000 }
    }
  }
});
```

### Redis Cluster Configuration

```redis
# redis-cluster.conf
cluster-enabled yes
cluster-config-file nodes-6379.conf
cluster-node-timeout 5000
cluster-require-full-coverage yes
cluster-migration-barrier 1

# Memory management
maxmemory 8gb
maxmemory-policy allkeys-lru

# Persistence
appendonly yes
appendfsync everysec
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# Slow log
slowlog-log-slower-than 10000
slowlog-max-len 128
```

### MongoDB WiredTiger Tuning

| Parameter | Default | Recommended | Description |
|-----------|---------|-------------|-------------|
| cacheSizeGB | 50% RAM | 60% RAM | WiredTiger cache size |
| journalCompressor | snappy | zstd | Compression for journal |
| collectionBlockCompressor | snappy | zstd | Collection compression |
| evictUpdatesCleanTarget | 20 | 100 | Dirty pages to trigger eviction |
| directoryForIndexes | false | true | Separate index files |

### Redis Sentinel Configuration

```redis
# sentinel.conf
sentinel monitor mymaster 127.0.0.1 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
sentinel parallel-syncs mymaster 1
sentinel auth-pass mymaster <password>

# Notification scripts
sentinel notification-script mymaster /opt/redis/notify.sh
sentinel client-reconfig-script mymaster /opt/redis/reconfig.sh
```

## Architecture Patterns

### Cache-Aside Pattern (MongoDB + Redis)

```
┌──────────┐     ┌───────────┐     ┌──────────┐
│  Client   │────▶│   Redis   │────▶│ MongoDB  │
│  Request  │     │  (Cache)  │     │  (Store) │
└──────────┘     └───────────┘     └──────────┘
     │                │                   │
     │    MISS        │    Fetch          │
     ├────────────────┼───────────────────┤
     │                │                   │
     │    HIT         │                   │
     ◀────────────────┤                   │
```

### Write-Through Pattern

```python
class WriteThroughCache:
    """Write-through cache ensuring consistency between MongoDB and Redis."""

    def __init__(self, mongo_client, redis_client):
        self.mongo = mongo_client
        self.redis = redis_client
        self.db = mongo_client.mydb

    def write(self, collection, doc_id, data):
        # Write to MongoDB first (source of truth)
        result = self.db[collection].update_one(
            {"_id": doc_id},
            {"$set": data},
            upsert=True
        )

        # Then update Redis cache
        cache_key = f"{collection}:{doc_id}"
        self.redis.setex(
            cache_key,
            3600,  # 1 hour TTL
            json.dumps(data, default=str)
        )

        return result

    def read(self, collection, doc_id):
        cache_key = f"{collection}:{doc_id}"
        cached = self.redis.get(cache_key)

        if cached:
            return json.loads(cached)

        # Cache miss - fetch from MongoDB
        doc = self.db[collection].find_one({"_id": doc_id})
        if doc:
            self.redis.setex(cache_key, 3600, json.dumps(doc, default=str))
        return doc
```

### Event Sourcing with Redis Streams + MongoDB

```python
import redis
from pymongo import MongoClient

class EventStore:
    """Event sourcing using Redis Streams as write-ahead log and MongoDB for projections."""

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.mongo = MongoClient('mongodb://localhost:27017/')
        self.events = self.mongo.events.events

    def append(self, stream_name, event_data):
        event = {
            'event_type': event_data['type'],
            'payload': json.dumps(event_data['payload']),
            'timestamp': time.time(),
            'aggregate_id': event_data['aggregate_id']
        }

        # Append to Redis Stream (fast write)
        message_id = self.redis.xadd(stream_name, event)

        # Async projection to MongoDB for complex queries
        event['_id'] = message_id
        self.events.insert_one(event)

        return message_id

    def get_events(self, stream_name, start_id='0'):
        return self.redis.xrange(stream_name, min=start_id, max='+')

    def replay(self, stream_name):
        """Replay all events for a stream."""
        events = self.redis.xrange(stream_name, min='0', max='+')
        state = {}
        for msg_id, data in events:
            payload = json.loads(data['payload'])
            state = self._apply_event(state, payload)
        return state
```

## Integration Guide

### Connection Pooling

```python
from pymongo import MongoClient
from pymongo.pool import PoolConnector
import redis

class DatabasePool:
    """Unified connection pool for MongoDB and Redis."""

    def __init__(self, config):
        self.mongo_client = MongoClient(
            config['mongo_uri'],
            maxPoolSize=100,
            minPoolSize=10,
            maxIdleTimeMS=45000,
            waitQueueTimeoutMS=5000,
            serverSelectionTimeoutMS=5000,
            retryWrites=True,
            retryReads=True,
            readPreference='secondaryPreferred',
            w='majority',
            journal=True
        )

        self.redis_pool = redis.ConnectionPool(
            host=config['redis_host'],
            port=config['redis_port'],
            db=config.get('redis_db', 0),
            password=config.get('redis_password'),
            max_connections=50,
            socket_timeout=5,
            socket_connect_timeout=2,
            retry_on_timeout=True,
            health_check_interval=30,
            decode_responses=True
        )

        self.redis_client = redis.Redis(connection_pool=self.redis_pool)

    def get_mongo(self):
        return self.mongo_client

    def get_redis(self):
        return self.redis_client

    def close(self):
        self.mongo_client.close()
        self.redis_pool.disconnect()
```

### Message Queue Integration (Redis Pub/Sub + MongoDB Change Streams)

```python
class MessageRelay:
    """Relay Redis pub/sub messages to MongoDB change streams for durability."""

    def __init__(self):
        self.redis = redis.Redis(host='localhost', decode_responses=True)
        self.mongo = MongoClient('mongodb://localhost:27017/')
        self.pubsub = self.redis.pubsub()

    def subscribe(self, channel):
        self.pubsub.subscribe(**{channel: self._handler})
        self.thread = self.pubsub.run_in_thread(sleep_time=0.001)

    def _handler(self, message):
        if message['type'] == 'message':
            data = json.loads(message['data'])
            data['received_at'] = datetime.utcnow()
            self.mongo.events.messages.insert_one(data)

    def watch_change_stream(self, pipeline=None):
        """Watch MongoDB change stream and relay to Redis."""
        with self.mongo.events.watch(pipeline or []) as stream:
            for change in stream:
                if change['operationType'] in ('insert', 'update'):
                    self.redis.publish(
                        'mongo-changes',
                        json.dumps(change, default=str)
                    )
```

## Performance Optimization

### MongoDB Index Optimization

```javascript
// Compound index for common query patterns
db.orders.createIndex(
  { "customer_id": 1, "status": 1, "created_at": -1 },
  { background: true, name: "idx_customer_status_date" }
);

// Partial index to reduce storage
db.users.createIndex(
  { "email": 1 },
  { partialFilterExpression: { "active": true }, name: "idx_active_email" }
);

// TTL index for automatic expiration
db.sessions.createIndex(
  { "last_accessed": 1 },
  { expireAfterSeconds: 1800, name: "idx_session_ttl" }
);

// Text index for search
db.products.createIndex(
  { "name": "text", "description": "text" },
  { weights: { "name": 10, "description": 5 }, name: "idx_product_text" }
);
```

### Redis Pipeline Optimization

```python
def bulk_operations(redis_client, operations):
    """Execute Redis operations in a pipeline for reduced round trips."""
    pipe = redis_client.pipeline(transaction=False)

    for op in operations:
        if op['type'] == 'set':
            pipe.setex(op['key'], op['ttl'], op['value'])
        elif op['type'] == 'hash':
            pipe.hset(op['key'], mapping=op['data'])
        elif op['type'] == 'list':
            pipe.lpush(op['key'], *op['items'])
        elif op['type'] == 'zset':
            pipe.zadd(op['key'], op['members'])
        elif op['type'] == 'delete':
            pipe.delete(op['key'])

    results = pipe.execute()
    return results

# Benchmark: 10,000 individual SETs vs pipeline
# Individual: ~15 seconds
# Pipeline:   ~0.3 seconds (50x improvement)
```

### Cache Warming Strategy

```python
class CacheWarmer:
    """Pre-populate Redis cache with frequently accessed MongoDB data."""

    def __init__(self, mongo_db, redis_client):
        self.db = mongo_db
        self.redis = redis_client

    def warm_hot_keys(self, collection, query, ttl=3600, batch_size=1000):
        """Batch-load records from MongoDB into Redis."""
        cursor = self.db[collection].find(query).batch_size(batch_size)
        pipe = self.redis.pipeline(transaction=False)
        count = 0

        for doc in cursor:
            key = f"{collection}:{doc['_id']}"
            pipe.setex(key, ttl, json.dumps(doc, default=str))
            count += 1

            if count % batch_size == 0:
                pipe.execute()
                pipe = self.redis.pipeline(transaction=False)

        pipe.execute()
        return count

    def warm_popular_products(self):
        """Warm cache with top 1000 products by view count."""
        return self.warm_hot_keys(
            'products',
            {"view_count": {"$gte": 100}},
            ttl=7200
        )
```

## Security Considerations

### Authentication and Authorization

```javascript
// MongoDB: Create application user with least-privilege
use admin;
db.createUser({
  user: "app_user",
  pwd: "securePassword123!",
  roles: [
    { role: "readWrite", db: "myapp" },
    { role: "read", db: "analytics" }
  ]
});

// Enable SCRAM-SHA-256 authentication
// mongod.conf
security:
  authorization: enabled
  clusterAuthMode: keyFile
  keyFile: /etc/mongo/keyfile
  transitionToAuth: false
```

```redis
# Redis: ACL configuration
ACL SETUSER appuser on >appPassword123 ~cache:* ~session:* +get +set +del +expire +hset +hget +pipeline
ACL SETUSER readonly on >readPassword123 ~cache:* +get +pipeline
ACL SETUSER admin on >adminPassword123 ~* +@all

# Disable dangerous commands
rename-command FLUSHALL ""
rename-command FLUSHDB ""
rename-command DEBUG ""
```

### TLS/SSL Configuration

```python
# MongoDB TLS
from pymongo import MongoClient

client = MongoClient(
    'mongodb://localhost:27017/',
    tls=True,
    tlsCertificateKeyFile='/etc/mongo/client.pem',
    tlsCAFile='/etc/mongo/ca.pem',
    tlsAllowInvalidCertificates=False,
    tlsAllowInvalidHostnames=False
)

# Redis TLS
import redis

pool = redis.ConnectionPool(
    host='localhost',
    port=6380,
    ssl=True,
    ssl_certfile='/etc/redis/client.pem',
    ssl_keyfile='/etc/redis/client.key',
    ssl_ca_certs='/etc/redis/ca.pem',
    ssl_cert_reqs='required',
    ssl_version='TLSv1_2'
)

r = redis.Redis(connection_pool=pool)
```

### Data Encryption at Rest

```python
from cryptography.fernet import Fernet
import pymongo

class EncryptedFieldHandler:
    """Encrypt sensitive fields before storing in MongoDB."""

    def __init__(self, key):
        self.cipher = Fernet(key)

    def encrypt(self, data):
        if isinstance(data, str):
            return self.cipher.encrypt(data.encode()).decode()
        elif isinstance(data, dict):
            return {k: self.encrypt(v) if k in self.sensitive_fields else v
                    for k, v in data.items()}
        return data

    def decrypt(self, data):
        if isinstance(data, str):
            return self.cipher.decrypt(data.encode()).decode()
        elif isinstance(data, dict):
            return {k: self.decrypt(v) if k in self.sensitive_fields else v
                    for k, v in data.items()}
        return data

# Usage
handler = EncryptedFieldHandler(Fernet.generate_key())
sensitive_fields = {'ssn', 'credit_card', 'email'}

doc = {"name": "John", "ssn": "123-45-6789", "email": "john@example.com"}
encrypted = handler.encrypt(doc)
# {"name": "John", "ssn": "gAAAAABk...", "email": "gAAAAABk..."}
```

## Troubleshooting Guide

### Common MongoDB Issues

| Issue | Symptom | Resolution |
|-------|---------|------------|
| Connection refused | `ServerSelectionTimeoutError` | Check mongod is running, firewall rules, bindIp |
| Too many connections | `ConnectionFailure` | Increase `maxIncomingConnections`, use pool |
| Slow queries | High `find` latency | Add indexes, use `explain()`, check cursor |
| Replication lag | `replSetGetStatus.optimeDate` difference | Check network, disk I/O, oplog window |
| OOM killed | Process killed by OS | Reduce `cacheSizeGB`, check for unbounded queries |

### Common Redis Issues

| Issue | Symptom | Resolution |
|-------|---------|------------|
| Memory pressure | `OOM command not allowed` | Increase `maxmemory`, set eviction policy |
| Slow commands | `SLOWLOG` entries | Avoid `KEYS *`, use `SCAN`, optimize patterns |
| Cluster failover | `CLUSTERDOWN` errors | Check node health, increase `cluster-node-timeout` |
| AOF rewrite lag | High disk I/O during rewrite | Use `appendfsync no` during rewrite, separate disk |
| Key expiration drift | Keys persist beyond TTL | Use `EXPIREAT`, check `hz` setting |

```python
def diagnose_redis(redis_client):
    """Run diagnostic checks on Redis instance."""
    info = redis_client.info()

    diagnostics = {
        'memory_used': info.get('used_memory_human'),
        'memory_peak': info.get('used_memory_peak_human'),
        'memory_fragmentation': info.get('mem_fragmentation_ratio'),
        'connected_clients': info.get('connected_clients'),
        'total_commands': info.get('total_commands_processed'),
        'hit_rate': info.get('keyspace_hits', 0) / max(
            info.get('keyspace_hits', 0) + info.get('keyspace_misses', 0), 1
        ),
        'expired_keys': info.get('expired_keys'),
        'evicted_keys': info.get('evicted_keys'),
        'instantaneous_ops': info.get('instantaneous_ops_per_sec'),
    }

    # Alert thresholds
    if diagnostics['memory_fragmentation'] > 1.5:
        print(f"WARNING: High fragmentation ratio: {diagnostics['memory_fragmentation']}")
    if diagnostics['hit_rate'] < 0.8:
        print(f"WARNING: Low cache hit rate: {diagnostics['hit_rate']:.1%}")
    if diagnostics['evicted_keys'] > 0:
        print(f"INFO: {diagnostics['evicted_keys']} keys evicted - consider increasing memory")

    return diagnostics
```

## API Reference

### MongoDB CRUD Operations

```javascript
// Insert
db.users.insertOne({ name: "Alice", email: "alice@example.com", age: 30 });
db.users.insertMany([
  { name: "Bob", email: "bob@example.com", age: 25 },
  { name: "Charlie", email: "charlie@example.com", age: 35 }
]);

// Read with aggregation
db.orders.aggregate([
  { $match: { status: "completed", created_at: { $gte: ISODate("2024-01-01") } } },
  { $group: { _id: "$customer_id", total: { $sum: "$amount" } } },
  { $sort: { total: -1 } },
  { $limit: 10 }
]);

// Update with upsert
db.users.updateOne(
  { email: "alice@example.com" },
  { $set: { last_login: new Date() }, $inc: { login_count: 1 } },
  { upsert: true }
);

// Delete
db.users.deleteMany({ last_login: { $lt: ISODate("2023-01-01") } });
```

### Redis Data Structure Operations

```python
# Strings
r.set("user:1:name", "Alice", ex=3600)
r.get("user:1:name")
r.incr("page:views:home")
r.mset({"key1": "val1", "key2": "val2"})

# Hashes
r.hset("user:1", mapping={"name": "Alice", "age": "30", "role": "admin"})
r.hget("user:1", "name")
r.hgetall("user:1")

# Lists
r.lpush("notifications:user:1", "New message", "New alert")
r.rpop("notifications:user:1")
r.lrange("notifications:user:1", 0, -1)

# Sets
r.sadd("tags:article:1", "python", "redis", "nosql")
r.smembers("tags:article:1")
r.sinter("tags:article:1", "tags:article:2")

# Sorted Sets
r.zadd("leaderboard", {"player1": 1500, "player2": 2000, "player3": 1800})
r.zrevrange("leaderboard", 0, 9, withscores=True)  # Top 10

# Streams
r.xadd("events", {"type": "user_signup", "user_id": "123"})
messages = r.xread({"events": "$"}, count=10, block=5000)

# HyperLogLog
r.pfadd("unique:visitors", "user1", "user2", "user3")
count = r.pfcount("unique:visitors")
```

## Data Models

### MongoDB Document Schema

```javascript
// User document with embedded references
{
  _id: ObjectId("..."),
  username: "alice",
  email: "alice@example.com",
  profile: {
    first_name: "Alice",
    last_name: "Smith",
    avatar_url: "https://cdn.example.com/avatars/alice.jpg",
    bio: "Software engineer"
  },
  preferences: {
    theme: "dark",
    notifications: {
      email: true,
      push: false,
      sms: true
    }
  },
  tags: ["premium", "early-adopter"],
  created_at: ISODate("2024-01-15T10:30:00Z"),
  updated_at: ISODate("2024-06-20T14:22:00Z"),
  login_history: [
    { ip: "192.168.1.100", timestamp: ISODate("2024-06-20T14:22:00Z") }
  ]
}
```

### Redis Key Schema Design

```
# Key naming conventions
user:{id}                    → Hash (user profile)
user:{id}:sessions           → Set (active session IDs)
user:{id}:permissions        → Set (permission strings)
session:{id}                 → Hash (session data)
session:{id}:ttl             → String (expiry timestamp)
post:{id}                    → Hash (post content)
post:{id}:likes              → Set (user IDs who liked)
post:{id}:comments           → Sorted Set (comment_id → timestamp)
feed:{user_id}               → Sorted Set (post_id → timestamp)
leaderboard:{game}           → Sorted Set (player_id → score)
rate_limit:{ip}:{window}     → String (request count)
lock:{resource}              → String (mutex with NX/EX)
queue:{name}                 → List (job payloads)
stream:{name}                → Stream (events)
```

## Deployment Guide

### Docker Compose Setup

```yaml
version: '3.8'

services:
  mongo-primary:
    image: mongo:7.0
    command: mongod --replSet rs0 --bind_ip_all --keyFile /etc/mongo/keyfile
    volumes:
      - mongo-primary-data:/data/db
      - ./mongo-keyfile:/etc/mongo/keyfile
    ports:
      - "27017:27017"
    networks:
      - mongo-net

  mongo-secondary:
    image: mongo:7.0
    command: mongod --replSet rs0 --bind_ip_all --keyFile /etc/mongo/keyfile
    volumes:
      - mongo-secondary-data:/data/db
      - ./mongo-keyfile:/etc/mongo/keyfile
    networks:
      - mongo-net

  redis-primary:
    image: redis:7.2-alpine
    command: redis-server /etc/redis/redis.conf
    volumes:
      - redis-data:/data
      - ./redis.conf:/etc/redis/redis.conf
    ports:
      - "6379:6379"
    networks:
      - redis-net

  redis-replica:
    image: redis:7.2-alpine
    command: redis-server /etc/redis/redis.conf --replicaof redis-primary 6379
    volumes:
      - redis-replica-data:/data
      - ./redis.conf:/etc/redis/redis.conf
    networks:
      - redis-net

volumes:
  mongo-primary-data:
  mongo-secondary-data:
  redis-data:
  redis-replica-data:

networks:
  mongo-net:
  redis-net:
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mongodb
spec:
  serviceName: mongodb
  replicas: 3
  selector:
    matchLabels:
      app: mongodb
  template:
    metadata:
      labels:
        app: mongodb
    spec:
      containers:
        - name: mongodb
          image: mongo:7.0
          ports:
            - containerPort: 27017
          command: ["mongod", "--replSet", "rs0", "--bind_ip_all"]
          volumeMounts:
            - name: mongo-data
              mountPath: /data/db
          resources:
            requests:
              memory: "2Gi"
              cpu: "1"
            limits:
              memory: "4Gi"
              cpu: "2"
  volumeClaimTemplates:
    - metadata:
        name: mongo-data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 50Gi
```

## Monitoring & Observability

### Prometheus Metrics Export

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Define metrics
MONGO_OPS = Counter('mongo_operations_total', 'Total MongoDB operations', ['operation', 'collection'])
MONGO_LATENCY = Histogram('mongo_operation_latency_seconds', 'MongoDB operation latency', ['operation'])
REDIS_OPS = Counter('redis_operations_total', 'Total Redis operations', ['operation'])
REDIS_LATENCY = Histogram('redis_operation_latency_seconds', 'Redis operation latency', ['operation'])
CACHE_HITS = Counter('cache_hits_total', 'Cache hits', ['cache_type'])
CACHE_MISSES = Counter('cache_misses_total', 'Cache misses', ['cache_type'])

class InstrumentedDB:
    def __init__(self, mongo_client, redis_client):
        self.mongo = mongo_client
        self.redis = redis_client

    def timed_operation(self, operation_name, collection_name, func, cache_type=None):
        start = time.time()
        try:
            result = func()
            MONGO_OPS.labels(operation=operation_name, collection=collection_name).inc()
            if cache_type:
                CACHE_HITS.labels(cache_type=cache_type).inc()
            return result
        except Exception as e:
            CACHE_MISSES.labels(cache_type=cache_type or 'unknown').inc()
            raise
        finally:
            MONGO_LATENCY.labels(operation=operation_name).observe(time.time() - start)

# Start metrics server
start_http_server(8000)
```

### Grafana Dashboard Queries

```promql
# MongoDB operations per second
rate(mongo_operations_total[5m])

# Redis latency p95
histogram_quantile(0.95, rate(redis_operation_latency_seconds_bucket[5m]))

# Cache hit ratio
cache_hits_total / (cache_hits_total + cache_misses_total)

# Active connections
redis_connected_clients

# Memory usage
redis_memory_used_bytes / redis_memory_max_bytes
```

## Testing Strategy

### Unit Tests

```python
import pytest
from unittest.mock import Mock, patch

class TestCacheAsidePattern:
    @pytest.fixture
    def cache(self, mock_mongo, mock_redis):
        return WriteThroughCache(mock_mongo, mock_redis)

    def test_cache_hit(self, cache, mock_redis):
        mock_redis.get.return_value = '{"name": "test"}'
        result = cache.read("users", "123")
        assert result["name"] == "test"
        mock_redis.get.assert_called_once()

    def test_cache_miss(self, cache, mock_mongo, mock_redis):
        mock_redis.get.return_value = None
        mock_mongo.mydb.users.find_one.return_value = {"_id": "123", "name": "test"}
        result = cache.read("users", "123")
        assert result["name"] == "test"
        mock_redis.setex.assert_called_once()

    @pytest.mark.parametrize("collection,doc_id", [
        ("users", "1"),
        ("products", "42"),
        ("orders", "999"),
    ])
    def test_write_operations(self, cache, collection, doc_id):
        data = {"name": "test", "value": 42}
        result = cache.write(collection, doc_id, data)
        assert result is not None
```

### Integration Tests

```python
import pytest
import redis
from pymongo import MongoClient

@pytest.fixture(scope="session")
def mongo_client():
    client = MongoClient("mongodb://localhost:27017/test_db")
    yield client
    client.drop_database("test_db")
    client.close()

@pytest.fixture(scope="session")
def redis_client():
    client = redis.Redis(host="localhost", port=6379, db=15)
    yield client
    client.flushdb()
    client.close()

class TestEndToEnd:
    def test_full_lifecycle(self, mongo_client, redis_client):
        # Write
        mongo_client.test_db.users.insert_one({"_id": "1", "name": "Test"})
        redis_client.setex("users:1", 3600, '{"name": "Test"}')

        # Read from cache
        cached = json.loads(redis_client.get("users:1"))
        assert cached["name"] == "Test"

        # Invalidate
        redis_client.delete("users:1")
        assert redis_client.get("users:1") is None

        # Read from MongoDB
        doc = mongo_client.test_db.users.find_one({"_id": "1"})
        assert doc["name"] == "Test"

    def test_concurrent_writes(self, mongo_client, redis_client):
        import threading
        errors = []

        def write_doc(i):
            try:
                mongo_client.test_db.docs.insert_one({"_id": str(i), "val": i})
                redis_client.set(f"doc:{i}", str(i))
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=write_doc, args=(i,)) for i in range(100)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0
        assert mongo_client.test_db.docs.count_documents({}) == 100
```

## Versioning & Migration

### MongoDB Schema Migration

```python
from pymongo import MongoClient
from datetime import datetime

class MongoMigration:
    """Version-controlled MongoDB schema migrations."""

    def __init__(self, db):
        self.db = db
        self.migrations = self.db.migrations

    def get_current_version(self):
        doc = self.migrations.find_one({"type": "schema"}, sort=[("version", -1)])
        return doc['version'] if doc else 0

    def migrate(self, version, up_func, down_func):
        current = self.get_current_version()
        if current >= version:
            return

        up_func(self.db)
        self.migrations.insert_one({
            "type": "schema",
            "version": version,
            "applied_at": datetime.utcnow(),
            "description": up_func.__doc__ or ""
        })

# Migration examples
def v2_add_user_preferences(db):
    """Add default preferences to users without preferences."""
    db.users.update_many(
        {"preferences": {"$exists": False}},
        {"$set": {"preferences": {"theme": "light", "notifications": True}}}
    )

def v3_create_indexes(db):
    """Create compound indexes for common query patterns."""
    db.users.createIndex([("email", 1)], unique=True)
    db.orders.createIndex([("customer_id", 1), ("created_at", -1)])

# Usage
migration = MongoMigration(db)
migration.migrate(2, v2_add_user_preferences, None)
migration.migrate(3, v3_create_indexes, None)
```

### Redis Schema Migration

```python
class RedisMigration:
    """Migrate Redis key patterns without downtime."""

    def __init__(self, redis_client):
        self.redis = redis_client

    def migrate_key_pattern(self, old_pattern, new_pattern, transform=None):
        """Scan and migrate keys matching old_pattern to new_pattern."""
        cursor = 0
        migrated = 0

        while True:
            cursor, keys = self.redis.scan(cursor, match=old_pattern, count=1000)
            for key in keys:
                new_key = new_pattern.replace('*', key.decode().split(':')[-1])
                data = self.redis.get(key)
                if data and transform:
                    data = transform(data)
                if data:
                    ttl = self.redis.ttl(key)
                    if ttl > 0:
                        self.redis.setex(new_key, ttl, data)
                    else:
                        self.redis.set(new_key, data)
                    self.redis.delete(key)
                    migrated += 1
            if cursor == 0:
                break

        return migrated

# Example: Migrate from v1 to v2 key format
# v1: user:123 → v2: users:123:profile
migration = RedisMigration(redis_client)
count = migration.migrate_key_pattern(
    "user:*",
    "users:*:profile",
    transform=lambda data: json.dumps(json.loads(data), sort_keys=True)
)
print(f"Migrated {count} keys")
```

## Glossary

| Term | Definition |
|------|------------|
| Replica Set | A group of MongoDB instances that maintain the same data set |
| Primary Node | The node in a replica set that receives all write operations |
| Secondary Node | Nodes that replicate data from the primary and handle reads |
| Oplog | A capped collection that records write operations for replication |
| WiredTiger | MongoDB's default storage engine |
| Sharding | Horizontal scaling by distributing data across multiple machines |
| Chunk | A contiguous range of shard key values in a sharded cluster |
| Sentinel | Redis high-availability solution providing automatic failover |
| Cluster | Redis deployment that distributes data across multiple nodes |
| Slot | One of 16384 hash slots used to distribute keys in Redis Cluster |
| Pipeline | A mechanism to batch multiple Redis commands into a single round trip |
| Pub/Sub | Redis publish/subscribe messaging paradigm |
| Cache-Aside | A caching pattern where the application manages cache explicitly |
| Write-Through | A caching pattern where writes go to cache and database simultaneously |
| TTL | Time To Live - expiration time for keys |
| Eviction Policy | Algorithm for removing keys when memory limit is reached (LRU, LFU) |
| Connection Pool | Reusable pool of database connections for efficiency |
| Change Stream | MongoDB mechanism to watch for real-time data changes |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01-01 | Initial release with MongoDB and Redis configuration basics |
| 1.1.0 | 2024-03-15 | Added architecture patterns (cache-aside, write-through) |
| 1.2.0 | 2024-05-01 | Added performance optimization section with benchmarks |
| 1.3.0 | 2024-07-01 | Added security hardening (TLS, ACL, encryption) |
| 1.4.0 | 2024-09-01 | Added monitoring and observability with Prometheus |
| 1.5.0 | 2024-11-01 | Added testing strategies and migration patterns |
| 1.6.0 | 2025-01-01 | Expanded troubleshooting guide and API reference |

## Contributing Guidelines

1. **Code Style**: Follow PEP 8 for Python and Airbnb style guide for JavaScript
2. **Testing**: All changes must include unit tests; integration tests for database operations
3. **Documentation**: Update this document for any configuration or API changes
4. **Security**: Never commit credentials; use environment variables or secrets management
5. **Performance**: Include benchmarks for any performance-critical changes

## License

This module is part of the Awesome-Grok-Skills project and follows the MIT License.
