---
name: redis
category: database
version: 1.0.0
tags: [database, redis]
---

# Redis

## Overview
Comprehensive redis within database domain.

## Usage
```python
from redis import Redis
r = Redis()
```

## Advanced Configuration

### Connection Configuration

```python
from redis import RedisConfig, SentinelConfig, ClusterConfig

# Advanced Redis configuration
config = RedisConfig(
    host="localhost",
    port=6379,
    db=0,
    password="your_password",
    username="default",
    ssl=True,
    ssl_certfile="/path/to/client.crt",
    ssl_keyfile="/path/to/client.key",
    ssl_ca_certs="/path/to/ca.crt",
    ssl_cert_reqs="required",
    socket_timeout=5,
    socket_connect_timeout=5,
    socket_keepalive=True,
    socket_keepalive_options={
        1: 60,  # TCP_KEEPIDLE
        2: 10,  # TCP_KEEPINTVL
        3: 5,   # TCP_KEEPCNT
    },
    retry_on_timeout=True,
    health_check_interval=30,
    client_name="myapp",
    encoding="utf-8",
    encoding_errors="strict",
    decode_responses=True,
    max_connections=50,
    connection_pool_kwargs={
        "max_connections": 50,
        "retry_on_timeout": True,
    },
)

r = Redis(config=config)
```

### Sentinel Configuration

```python
from redis import SentinelConfig

# High availability with Sentinel
sentinel_config = SentinelConfig(
    sentinels=[
        ("sentinel1.example.com", 26379),
        ("sentinel2.example.com", 26379),
        ("sentinel3.example.com", 26379),
    ],
    service_name="mymaster",
    password="sentinel_password",
    socket_timeout=0.1,
    socket_connect_timeout=0.1,
    retry_on_timeout=True,
    health_check_interval=30,
)

r = Redis(sentinel=sentinel_config)
master = r.master_for("mymaster", socket_timeout=0.1)
slave = r.slave_for("mymaster", socket_timeout=0.1)
```

### Cluster Configuration

```python
from redis import ClusterConfig

# Redis Cluster configuration
cluster_config = ClusterConfig(
    startup_nodes=[
        {"host": "redis-node1.example.com", "port": 6379},
        {"host": "redis-node2.example.com", "port": 6379},
        {"host": "redis-node3.example.com", "port": 6379},
    ],
    max_connections=50,
    retry_on_timeout=True,
    health_check_interval=30,
    skip_full_coverage_check=True,
    read_from_replicas=True,
)

r = Redis(cluster=cluster_config)
```

### Pipeline Configuration

```python
from redis import PipelineConfig

# Advanced pipeline configuration
pipeline_config = PipelineConfig(
    transaction=True,
    shard_hint=None,
    max_commands=100,
)

# Use pipeline for batch operations
pipe = r.pipeline(transaction=True)
for i in range(1000):
    pipe.set(f"key:{i}", f"value:{i}")
pipe.execute()
```

## Architecture Patterns

### Cache-Aside Pattern

```python
from redis import CacheAside

cache = CacheAside(
    redis_client=r,
    default_ttl=300,  # 5 minutes
    key_prefix="cache:",
    serializer="json",
    compressor="lz4",
)

@cache.memoize(ttl=600)
def get_user(user_id):
    # Database query
    return db.query("SELECT * FROM users WHERE id = $1", user_id)

# Usage
user = get_user(123)  # Cache miss, fetches from DB
user = get_user(123)  # Cache hit, returns from Redis
```

### Write-Through Pattern

```python
from redis import WriteThrough

write_through = WriteThrough(
    redis_client=r,
    db_client=db,
    key_prefix="user:",
    ttl=300,
)

def save_user(user_data):
    # Write to Redis and DB simultaneously
    write_through.write(
        key=user_data["id"],
        value=user_data,
        db_operation=lambda data: db.insert("users", data),
    )

def get_user(user_id):
    # Read from Redis, fallback to DB
    return write_through.read(
        key=user_id,
        db_operation=lambda: db.query("SELECT * FROM users WHERE id = $1", user_id),
    )
```

### Rate Limiting Pattern

```python
from redis import RateLimiter

limiter = RateLimiter(
    redis_client=r,
    max_requests=100,
    window_seconds=60,
    key_prefix="ratelimit:",
)

def api_endpoint(request):
    client_ip = request.remote_addr
    
    if not limiter.is_allowed(client_ip):
        return {"error": "Rate limit exceeded"}, 429
    
    # Process request
    return {"success": True}
```

### Session Store Pattern

```python
from redis import SessionStore

session_store = SessionStore(
    redis_client=r,
    key_prefix="session:",
    ttl=1800,  # 30 minutes
    serializer="json",
    secure=True,
    httponly=True,
    samesite="Lax",
)

# Create session
session_id = session_store.create({
    "user_id": 123,
    "ip": "192.168.1.1",
    "user_agent": "Mozilla/5.0",
})

# Get session
session = session_store.get(session_id)

# Update session
session_store.update(session_id, {"last_activity": datetime.now()})

# Delete session
session_store.delete(session_id)
```

## Integration Guide

### Django Integration

```python
from redis import DjangoRedisIntegration

# Configure Django cache
django_config = DjangoRedisIntegration(
    cache_servers={
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://localhost:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
            },
        }
    },
    session_backend={
        "ENGINE": "django_redis.backends.session.RedisSession",
        "LOCATION": "redis://localhost:6379/2",
    },
)

django_config.setup()
```

### Flask Integration

```python
from redis import FlaskRedisIntegration

# Configure Flask
flask_config = FlaskRedisIntegration(
    app=app,
    redis_url="redis://localhost:6379/0",
    cache_type="redis",
    session_type="redis",
)

flask_config.setup()
```

### FastAPI Integration

```python
from redis import FastAPIRedisIntegration

# Configure FastAPI
fastapi_config = FastAPIRedisIntegration(
    app=app,
    redis_url="redis://localhost:6379/0",
    cache_backend="redis",
    session_backend="redis",
)

fastapi_config.setup()
```

## Performance Optimization

### Pipeline Optimization

```python
from redis import PipelineOptimizer

optimizer = PipelineOptimizer(r)

# Batch operations
batch_data = {f"key:{i}": f"value:{i}" for i in range(10000)}

# Optimized batch set
optimizer.batch_set(batch_data, chunk_size=1000)
print(f"Batch set completed in {optimizer.elapsed_time:.2f}s")
```

### Memory Optimization

```python
from redis import MemoryOptimizer

optimizer = MemoryOptimizer(r)

# Analyze memory usage
analysis = optimizer.analyze_memory()
print(f"Total memory: {analysis.total_memory_mb:.2f} MB")
print(f"Used memory: {analysis.used_memory_mb:.2f} MB")
print(f"Memory fragmentation: {analysis.fragmentation_ratio:.2f}")

# Optimize memory
optimizer.optimize_keys(ttl_default=3600)
print(f"Optimized {optimizer.optimized_keys} keys")
```

### Query Optimization

```python
from redis import QueryOptimizer

optimizer = QueryOptimizer(r)

# Analyze slow commands
slow_commands = optimizer.find_slow_commands(
    threshold_ms=10,
    time_range_hours=24,
)

for cmd in slow_commands:
    print(f"Command: {cmd.command}")
    print(f"  Avg time: {cmd.avg_time_ms:.2f}ms")
    print(f"  Calls: {cmd.call_count}")
    print(f"  Recommendation: {cmd.recommendation}")
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Memory Issues

**Symptom**: Redis running out of memory

**Solution**:
```python
# Check memory usage
info = r.info("memory")
print(f"Used memory: {info['used_memory_human']}")
print(f"Max memory: {info.get('maxmemory_human', 'unlimited')}")

# Set max memory
r.config_set("maxmemory", "1gb")
r.config_set("maxmemory-policy", "allkeys-lru")

# Flush old keys
r.flushdb()
```

#### 2. Connection Issues

**Symptom**: Cannot connect to Redis

**Solution**:
```python
# Test connection
try:
    r.ping()
    print("Connected to Redis")
except ConnectionError as e:
    print(f"Connection failed: {e}")

# Check connection pool
pool = r.connection_pool
print(f"Connections in pool: {pool.connection_kwargs}")
```

#### 3. Slow Queries

**Symptom**: Redis commands taking too long

**Solution**:
```python
# Enable slow log
r.config_set("slowlog-log-slower-than", 10000)  # 10ms

# Get slow log
slow_log = r.slowlog_get(10)
for entry in slow_log:
    print(f"Command: {entry['command']}")
    print(f"Duration: {entry['duration']} microseconds")
```

## API Reference

### Core Classes

#### `Redis`
```python
class Redis:
    def __init__(self, config: Optional[RedisConfig] = None) -> None: ...
    def get(self, key: str) -> Optional[str]: ...
    def set(self, key: str, value: str, ex: Optional[int] = None) -> bool: ...
    def delete(self, *keys: str) -> int: ...
    def exists(self, *keys: str) -> int: ...
    def expire(self, key: str, time: int) -> bool: ...
    def keys(self, pattern: str = "*") -> List[str]: ...
    def hset(self, name: str, mapping: dict) -> int: ...
    def hget(self, name: str, key: str) -> Optional[str]: ...
    def lpush(self, name: str, *values: str) -> int: ...
    def rpush(self, name: str, *values: str) -> int: ...
    def lpop(self, name: str) -> Optional[str]: ...
    def lrange(self, name: str, start: int, end: int) -> List[str]: ...
    def sadd(self, name: str, *values: str) -> int: ...
    def smembers(self, name: str) -> Set[str]: ...
    def pipeline(self, transaction: bool = True) -> Pipeline: ...
```

## Data Models

### Redis Data Types

```python
# String
r.set("key", "value")
r.get("key")  # "value"

# Hash
r.hset("user:1", mapping={"name": "John", "email": "john@example.com"})
r.hget("user:1", "name")  # "John"

# List
r.lpush("queue", "task1", "task2")
r.rpop("queue")  # "task2"

# Set
r.sadd("tags", "python", "redis", "cache")
r.smembers("tags")  # {"python", "redis", "cache"}

# Sorted Set
r.zadd("leaderboard", {"player1": 100, "player2": 200})
r.zrevrange("leaderboard", 0, 9)  # Top 10 players
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM redis:7-alpine

COPY redis.conf /usr/local/etc/redis/redis.conf

EXPOSE 6379

CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
spec:
  serviceName: redis
  replicas: 3
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        volumeMounts:
        - name: data
          mountPath: /data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

## Monitoring & Observability

### Metrics Collection

```python
from redis import MetricsCollector

collector = MetricsCollector(backend="prometheus")

collector.register_metric("redis_connections_active", type="gauge")
collector.register_metric("redis_commands_total", type="counter")
collector.register_metric("redis_memory_used", type="gauge")
collector.register_metric("redis_hits_ratio", type="gauge")

collector.set("redis_connections_active", active_connections)
collector.inc("redis_commands_total")
collector.set("redis_memory_used", memory_used_bytes)
collector.set("redis_hits_ratio", hits / (hits + misses))
```

### Health Check

```python
from redis import HealthCheck

health = HealthCheck(r)

# Run health check
status = health.check()
print(f"Status: {status.status}")
print(f"Latency: {status.latency_ms:.2f}ms")
print(f"Memory: {status.memory_used_mb:.2f}MB")
print(f"Connections: {status.connections_active}")
```

## Testing Strategy

### Unit Tests

```python
import pytest
from redis import Redis, RedisConfig

class TestRedis:
    def setup_method(self):
        self.config = RedisConfig(host="localhost", port=6379, db=15)
        self.r = Redis(self.config)
    
    def test_set_get(self):
        self.r.set("test_key", "test_value")
        assert self.r.get("test_key") == "test_value"
    
    def test_hash_operations(self):
        self.r.hset("test_hash", mapping={"field1": "value1", "field2": "value2"})
        assert self.r.hget("test_hash", "field1") == "value1"
    
    def test_list_operations(self):
        self.r.lpush("test_list", "item1", "item2")
        assert self.r.llen("test_list") == 2
```

## Versioning & Migration

### Changelog

#### v2.0.0 (2024-01-15)
- **Breaking**: New config API
- **Added**: Cluster support
- **Added**: Sentinel support
- **Improved**: 2x faster operations
- **Fixed**: Connection pool leaks

## Glossary

| Term | Definition |
|------|------------|
| **Redis** | Remote Dictionary Server; in-memory data store |
| **Pipeline** | Batch multiple commands into single round-trip |
| **Pub/Sub** | Publish/subscribe messaging pattern |
| **Lua Scripting** | Execute Lua scripts atomically on server |
| **Cluster** | Distributed Redis deployment across multiple nodes |

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/redis.git
cd redis
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT License

Copyright (c) 2024 Redis Contributors

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

## Data Validation

### Command Validation

```python
from redis import CommandValidator

validator = CommandValidator()

# Validate command
validator.validate_command(command)
validator.validate_key(key)
validator.validate_value(value)
```

## Advanced Patterns

### Redlock Distributed Locking

```python
from redis import Redlock, LockConfig

lock_config = LockConfig(
    retry_count=3,
    retry_delay=200,
    ttl=10000,
)

redlock = Redlock(
    redis_clients=[r1, r2, r3],
    config=lock_config,
)

# Acquire lock
with redlock.lock("resource:123") as lock:
    # Critical section
    print("Lock acquired")
    # Do work
print("Lock released")
```

### Rate Limiting Algorithms

```python
from redis import SlidingWindowRateLimiter, TokenBucketRateLimiter

# Sliding window rate limiter
slimiter = SlidingWindowRateLimiter(
    redis_client=r,
    max_requests=100,
    window_seconds=60,
    key_prefix="ratelimit:",
)

# Token bucket rate limiter
tlimiter = TokenBucketRateLimiter(
    redis_client=r,
    capacity=100,
    refill_rate=10,  # tokens per second
    key_prefix="tokenbucket:",
)

def api_endpoint(request):
    client_id = request.headers.get("X-Client-ID")
    
    if not slimiter.is_allowed(client_id):
        return {"error": "Rate limit exceeded"}, 429
    
    # Process request
    return {"success": True}
```

### Leaderboard Implementation

```python
from redis import Leaderboard

leaderboard = Leaderboard(redis_client=r, key="game:leaderboard")

# Update scores
leaderboard.update("player1", 1000)
leaderboard.update("player2", 1500)
leaderboard.update("player3", 1200)

# Get top players
top10 = leaderboard.top(10)
for rank, (player, score) in enumerate(top10, 1):
    print(f"#{rank}: {player} - {score}")

# Get player rank
rank = leaderboard.rank("player1")
print(f"Player1 rank: {rank}")
```

### Distributed Task Queue

```python
from redis import TaskQueue, Worker

queue = TaskQueue(redis_client=r, queue_name="tasks")

# Add tasks
queue.enqueue("process_image", image_id=123, priority="high")
queue.enqueue("send_email", to="user@example.com", subject="Hello")

# Worker
def worker():
    while True:
        task = queue.dequeue()
        if task:
            # Process task
            result = process_task(task)
            task.complete(result)

# Start worker
worker_thread = Worker(queue, worker_func=worker)
worker_thread.start()
```

### Pub/Sub with Patterns

```python
from redis import PatternPubSub

pubsub = PatternPubSub(redis_client=r)

# Subscribe to patterns
pubsub.psubscribe("user.*", lambda channel, message: print(f"User event: {message}"))
pubsub.psubscribe("order.*", lambda channel, message: print(f"Order event: {message}"))

# Publish events
pubsub.publish("user.created", {"user_id": 123})
pubsub.publish("order.placed", {"order_id": 456})
```

### Redis Streams

```python
from redis import RedisStream

stream = RedisStream(redis_client=r)

# Create stream
stream.create("events")

# Add events
stream.add("events", {"type": "user.created", "user_id": "123"})
stream.add("events", {"type": "order.placed", "order_id": "456"})

# Read events
events = stream.read("events", count=10)
for event in events:
    print(f"Event: {event}")

# Consumer group
stream.create_group("events", "processors")
stream.read_group("events", "processors", "consumer1", count=5)
```

### Redis Cluster Operations

```python
from redis import RedisCluster

cluster = RedisCluster(
    startup_nodes=[
        {"host": "node1", "port": 6379},
        {"host": "node2", "port": 6379},
        {"host": "node3", "port": 6379},
    ],
    decode_responses=True,
)

# Cluster operations
cluster.set("key1", "value1")
cluster.get("key1")

# Cluster info
info = cluster.cluster_info()
print(f"Cluster state: {info['cluster_state']}")
print(f"Known nodes: {info['cluster_known_nodes']}")
```

### Redis Sentinel Operations

```python
from redis import RedisSentinel

sentinel = RedisSentinel(
    sentinels=[
        ("sentinel1", 26379),
        ("sentinel2", 26379),
        ("sentinel3", 26379),
    ],
    socket_timeout=0.1,
)

# Get master
master = sentinel.master_for("mymaster", socket_timeout=0.1)
master.set("key", "value")

# Get slave
slave = sentinel.slave_for("mymaster", socket_timeout=0.1)
slave.get("key")

# Sentinel info
info = sentinel.sentinel_info()
print(f"Master: {info['master']}")
```

### Lua Scripting Advanced

```python
from redis import LuaScriptManager

manager = LuaScriptManager(redis_client=r)

# Define complex script
acquire_lock_script = """
local key = KEYS[1]
local value = ARGV[1]
local ttl = tonumber(ARGV[2])

if redis.call('SET', key, value, 'NX', 'EX', ttl) then
    return 1
else
    return 0
end
"""

# Register script
script_id = manager.register(acquire_lock_script)

# Execute script
result = manager.execute(script_id, keys=["lock:resource1"], args=["owner1", 30])
print(f"Lock acquired: {result == 1}")
```

### Redis Transactions

```python
from redis import TransactionManager

tx = TransactionManager(redis_client=r)

# Execute transaction
with tx.pipeline(transaction=True) as pipe:
    pipe.set("account:1:balance", "1000")
    pipe.set("account:2:balance", "500")
    pipe.incrby("account:1:balance", -100)
    pipe.incrby("account:2:balance", 100)
    results = pipe.execute()

print(f"Transaction completed: {all(results)}")
```

### Redis Module Integration

```python
from redis import ModuleManager

modules = ModuleManager(redis_client=r)

# Check loaded modules
loaded = modules.list_loaded()
print(f"Loaded modules: {loaded}")

# Load module
modules.load("redisearch")
modules.load("redisjson")

# Use module commands
r.ft_create("idx", "PREFIX", "1", "doc:", "SCHEMA", "title", "TEXT", "body", "TEXT")
r.json_set("doc:1", "$", {"title": "Hello", "body": "World"})
```