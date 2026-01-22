# Redis

## Overview

Redis is an in-memory data structure store used as a database, cache, and message broker. This skill covers Redis deployment patterns, data structures, performance optimization, and high availability configurations. Redis provides exceptional performance by storing data in memory with optional durability, making it ideal for caching, session management, and real-time applications.

## Core Capabilities

Data structures including strings, hashes, lists, sets, sorted sets, and streams support diverse use cases. Pub/Sub enables real-time messaging patterns with channels and patterns. Lua scripting allows atomic multi-operation scripts on the server side. Geospatial indexes support location-based queries and radius searches.

Sentinel provides high availability with automatic failover for standalone and master-replica setups. Cluster mode enables horizontal sharding across multiple Redis instances. Redis Modules extend functionality with RedisJSON, RedisSearch, RedisGraph, and RedisBloom. Stream consumer groups support reliable message processing patterns.

## Usage Examples

```python
from redis import Redis

redis = Redis()

redis.create_cluster(
    name="production-redis",
    cluster_mode="cluster",
    redis_version="7.2"
)

redis.configure_sentinel(
    master_name="mymaster",
    quorum=2,
    down_after_milliseconds=30000
)

redis.add_sentinel_monitor(
    master_name="mymaster",
    host="redis-master",
    port=6379,
    quorum=2
)

redis.configure_cluster_mode(enable=True)

replication = redis.create_replication(
    master_host="redis-master",
    replica_of=None
)

data = redis.create_data_structure(
    key="user:1001",
    data_type="hash",
    value={"name": "John", "email": "john@example.com"},
    ttl=3600
)

stream = redis.create_stream(
    stream_name="orders",
    max_length=10000
)

consumer_group = redis.create_consumer_group(
    stream_name="orders",
    group_name="processors",
    consumer_name="worker-1"
)

sorted_set = redis.create_sorted_set(
    key="leaderboard",
    members_scores=[("player1", 1000), ("player2", 950), ("player3", 900)]
)

redis.configure_persistence(
    rdb_enabled=True,
    aof_enabled=True
)

security = redis.configure_security(
    requirepass="secure_password",
    acl_enabled=True
)

performance = redis.configure_performance(
    maxclients=10000,
    timeout=0,
    maxmemory="4gb",
    maxmemory_policy="allkeys-lru"
)

slow_log = redis.configure_slow_log(
    slowlog_log_slower_than=10000,
    slowlog_max_len=128
)

lua_script = redis.create_lua_script(
    script_name="increment_with_cap",
    script_body="local current = redis.call('GET', KEYS[1]) or 0 local max = tonumber(ARGV[1]) local new = math.min(tonumber(current) + 1, max) redis.call('SET', KEYS[1], new) return new"
)

geo_index = redis.create_geospatial_index(
    key="stores",
    members_locations=[("store1", -73.935242, 40.730610), ("store2", -74.0060, 40.7128)]
)

redis.create_bloom_filter(
    key="user_emails",
    error_rate=0.01,
    initial_capacity=10000
)

rate_limit = redis.configure_rate_limiting(
    key="api:/v1/users",
    max_requests=100,
    window_seconds=60
)

circuit_breaker = redis.create_circuit_breaker(
    key="payment_service",
    failure_threshold=5,
    reset_timeout=30
)

search_index = redis.create_search_index(
    index_name="products_idx",
    prefix="product:",
    schema=[
        {"field": "name", "type": "text", "weight": 1.0},
        {"field": "description", "type": "text", "weight": 0.5},
        {"field": "price", "type": "numeric"}
    ]
)
```

## Best Practices

Choose appropriate eviction policies based on access patterns and data importance. Use Redis Cluster for production deployments requiring horizontal scaling. Implement proper authentication and ACLs to secure production instances. Monitor memory usage, eviction counts, and latency metrics.

Use pipelines to batch multiple commands and reduce network round-trips. Implement proper connection pooling in client applications. Use Lua scripts for atomic multi-key operations. Configure persistence appropriately based on durability requirements. Plan capacity for growth with proper memory allocation and monitoring.

## Related Skills

- Caching (caching strategies)
- Database Administration (general DBA skills)
- Message Queues (messaging patterns)
- NoSQL (alternative database paradigms)

## Use Cases

Application caching reduces database load and improves response times for frequently accessed data. Session storage provides fast, scalable session management for web applications. Real-time leaderboards use sorted sets for instant ranking updates. Rate limiting protects APIs from abuse with sliding window counters. Message queues with streams enable reliable event processing. Geospatial queries power location-based features in applications.
