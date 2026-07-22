---
name: caching
category: devops
version: 1.0.0
tags: [devops, caching, redis, memcached, cdn]
---

# Caching

## Overview

The Caching module provides a comprehensive toolkit for implementing multi-layer caching strategies across distributed systems. It supports in-memory caching (LRU, LFU, TTL-based), distributed caching (Redis, Memcached), CDN edge caching, and application-level caching with cache invalidation patterns. The module abstracts cache backend differences behind a unified API, enabling consistent caching behavior across development, staging, and production environments.

Caching is critical for system performance Ã¢â‚¬â€ a well-designed cache reduces database load by 90%+ and improves response times from seconds to milliseconds. This module implements the most common and battle-tested caching patterns: cache-aside, read-through, write-through, write-behind, and cache warming. Each pattern includes automatic cache invalidation strategies, stale-while-revalidate support, and cache stampede prevention.

The module provides cache analytics including hit rate monitoring, memory usage tracking, eviction rate analysis, and cache warming recommendations. Integration with monitoring systems (Prometheus, Datadog) enables real-time cache performance visibility. The module also supports cache coherency in distributed systems through pub/sub invalidation and consistent hashing.

## Core Capabilities

- Multi-layer caching with L1 (in-memory), L2 (distributed), and L3 (CDN) support
- Redis and Memcached backend support with connection pooling
- Cache patterns: cache-aside, read-through, write-through, write-behind
- TTL management with jitter to prevent cache stampede
- Cache invalidation via pub/sub for distributed consistency
- Cache warming and preloading strategies
- Hit rate monitoring and memory usage analytics
- Consistent hashing for distributed cache key distribution

## Usage Examples

### In-Memory LRU Cache

```python
from caching import MemoryCache

cache = MemoryCache(max_size=10000, ttl_seconds=300)

# Basic operations
cache.set("user:123", {"name": "Alice", "role": "admin"}, ttl=600)
user = cache.get("user:123")
print(f"User: {user}")

# Cache-aside pattern
def get_user(user_id):
    cached = cache.get(f"user:{user_id}")
    if cached:
        return cached
    user = db.users.find(user_id)
    cache.set(f"user:{user_id}", user, ttl=300)
    return user
```

### Redis Distributed Cache

```python
from caching import RedisCache

redis = RedisCache(
    host="redis-cluster.example.com",
    port=6379,
    password="secret",
    db=0,
    max_connections=50,
    socket_timeout=5,
    retry_on_timeout=True,
)

# Set with TTL
redis.set("session:abc123", session_data, ttl=3600)

# Get with fallback
data = redis.get("cache:key") or compute_expensive_result()
redis.set("cache:key", data, ttl=600)

# Pub/sub invalidation
redis.publish("cache:invalidate", {"pattern": "user:*"})
```

### Cache-Aside Pattern

```python
from caching import CacheAside, CacheKey

class ProductService:
    def __init__(self, cache, db):
        self.cache = CacheAside(cache, default_ttl=300)
        self.db = db

    def get_product(self, product_id):
        return self.cache.get_or_set(
            key=CacheKey("product", product_id),
            fetch_fn=lambda: self.db.products.find(product_id),
            ttl=300,
        )

    def update_product(self, product_id, data):
        self.db.products.update(product_id, data)
        self.cache.invalidate(CacheKey("product", product_id))
```

### Write-Behind Pattern

```python
from caching import WriteBehindCache

wb = WriteBehindCache(
    cache=redis,
    flush_interval_s=5,
    max_buffer_size=1000,
)

# Writes are buffered and flushed asynchronously
wb.write("analytics:pageview", pageview_event)
wb.write("analytics:pageview", another_event)

# Force flush
wb.flush()
```

### Cache Warming

```python
from caching import CacheWarmer

warmer = CacheWarmer(cache=redis)
warmer.add_warming_task("product_catalog", lambda: db.products.find_all(), ttl=3600)
warmer.add_warming_task("user_sessions", lambda: db.sessions.active(), ttl=600)
warmer.start_warming()
```

## Advanced Configuration

### Redis Cluster Configuration

```python
from caching import RedisCluster

cluster = RedisCluster(
    nodes=[
        {"host": "redis-1", "port": 6379},
        {"host": "redis-2", "port": 6379},
        {"host": "redis-3", "port": 6379},
    ],
    read_from_replicas=True,
    max_connections_per_node=20,
    health_check_interval=30,
    retry_on_cluster_down=True,
)
```

### Consistent Hashing

```python
from caching import ConsistentHashRing

ring = ConsistentHashRing(virtual_nodes=150)
ring.add_node("cache-1", weight=1.0)
ring.add_node("cache-2", weight=1.5)
ring.add_node("cache-3", weight=1.0)

node = ring.get_node("user:123")
print(f"Key routes to: {node}")
```

## Architecture Patterns

### Multi-Layer Cache Architecture

```
Application
    Ã¢â€â€š
    Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š L1: In-MemoryÃ¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ LRU/LFU, <1ms access
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
    Ã¢â€â€š MISS
    Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š L2: Redis    Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Distributed, <5ms access
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
    Ã¢â€â€š MISS
    Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š L3: Database Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Source of truth
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
```

### Cache Invalidation Patterns

```
Write Ã¢â€ â€™ Invalidate Cache Ã¢â€ â€™ Next Read Populates
Write Ã¢â€ â€™ Update Cache (write-through)
Write Ã¢â€ â€™ Buffer Writes (write-behind) Ã¢â€ â€™ Async Flush
```

## Integration Guide

### Prometheus Metrics

```python
from caching import PrometheusCacheMetrics

metrics = PrometheusCacheMetrics(cache=redis)
metrics.expose_port(9090)
# Metrics: cache_hits_total, cache_misses_total, cache_size_bytes, cache_evictions_total
```

### Django Integration

```python
from caching import DjangoCacheBackend

CACHES = {
    "default": DjangoCacheBackend(
        backend="redis",
        location="redis://localhost:6379/0",
        timeout=300,
        key_prefix="myapp",
    )
}
```

## Performance Optimization

| Strategy | Benefit |
|----------|---------|
| Local L1 cache | Sub-millisecond reads for hot keys |
| Stale-while-revalidate | Serve stale data while refreshing |
| Cache stampede prevention | Lock-based refresh for hot keys |
| Compression | 50%+ memory savings for large values |
| Pipeline operations | Batch Redis commands for throughput |

## Security Considerations

- **TLS for Redis connections**: Encrypt data in transit
- **ACL for Redis**: Restrict key access per application
- **No sensitive data in cache**: Encrypt PII before caching
- **Cache poisoning prevention**: Validate cached data on read
- **TTL enforcement**: Prevent indefinite cache retention

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Low hit rate | TTL too short or keys too specific | Increase TTL, use key patterns |
| Cache stampede | Hot key expiration | Use lock-based refresh |
| High memory usage | Large values or no eviction | Enable eviction, compress values |
| Redis connection errors | Pool exhaustion | Increase max_connections |
| Stale data after update | Missing invalidation | Add cache invalidation on write |

## API Reference

### MemoryCache

```python
class MemoryCache:
    def __init__(self, max_size: int, ttl_seconds: int)
    def get(self, key: str) -> any
    def set(self, key: str, value: any, ttl: int = None) -> None
    def delete(self, key: str) -> None
    def exists(self, key: str) -> bool
    def clear(self) -> None
    def stats(self) -> CacheStats
```

### RedisCache

```python
class RedisCache:
    def __init__(self, host: str, port: int, password: str, db: int, max_connections: int)
    def get(self, key: str) -> any
    def set(self, key: str, value: any, ttl: int = None) -> None
    def delete(self, key: str) -> None
    def publish(self, channel: str, message: dict) -> None
    def pipeline(self) -> RedisPipeline
```

## Data Models

```python
from dataclasses import dataclass

@dataclass
class CacheStats:
    hits: int
    misses: int
    hit_rate: float
    memory_used_bytes: int
    evictions: int

@dataclass
class CacheKey:
    prefix: str
    identifier: str
    version: int = 1

    def __str__(self):
        return f"{self.prefix}:v{self.version}:{self.identifier}"
```

## Deployment Guide

### Installation

```bash
pip install caching
# With Redis support
pip install caching[redis]
```

### Redis Setup

```bash
# Docker
docker run -d -p 6379:6379 redis:7-alpine

# Production cluster
redis-cli --cluster create node1:6379 node2:6379 node3:6379
```

## Monitoring & Observability

```python
from caching import MetricsCollector

collector = MetricsCollector()
collector.gauge("cache.hit_rate", stats.hit_rate)
collector.counter("cache.operations.total", count, tags={"operation": op})
collector.gauge("cache.memory_used_bytes", stats.memory_used_bytes)
collector.counter("cache.evictions.total", count)
```

## Testing Strategy

```python
import pytest
from caching import MemoryCache

def test_cache_hit():
    cache = MemoryCache(max_size=100, ttl_seconds=60)
    cache.set("key", "value")
    assert cache.get("key") == "value"

def test_cache_expiry():
    cache = MemoryCache(max_size=100, ttl_seconds=0)
    cache.set("key", "value")
    import time; time.sleep(0.01)
    assert cache.get("key") is None
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added Redis Cluster | Configure cluster nodes |
| 2.0.0 | New invalidation API | Update cache operations |

## Glossary

| Term | Definition |
|------|-----------|
| **LRU** | Least Recently Used Ã¢â‚¬â€ eviction policy |
| **Cache-Aside** | App manages cache reads/writes explicitly |
| **Write-Behind** | Buffer writes, flush asynchronously |
| **Stampede** | Thundering herd on cache miss |
| **TTL** | Time-To-Live Ã¢â‚¬â€ cache entry expiration |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with LRU/LFU memory cache
- Redis and Memcached backends
- Cache-aside, read-through, write-through patterns
- Pub/sub cache invalidation

## Contributing Guidelines

```bash
git clone https://github.com/example/caching.git
pip install -e ".[dev]"
pytest tests/
```

## Advanced Caching Strategies

### Cache Stampede Prevention

Cache stampede (thundering herd) occurs when many requests simultaneously attempt to rebuild a cached value after expiration. This module provides three strategies to prevent stampede:

```python
from caching import StampedePrevention

# Strategy 1: Lock-based refresh
stampede = StampedePrevention(strategy="lock", lock_timeout_s=5)
data = stampede.get_or_refresh(
    key="expensive:query",
    fetch_fn=lambda: db.run_expensive_query(),
    ttl=300,
)

# Strategy 2: Probabilistic early expiration
stampede = StampedePrevention(strategy="probabilistic", beta=1.0)
data = stampede.get_or_refresh(
    key="expensive:query",
    fetch_fn=lambda: db.run_expensive_query(),
    ttl=300,
)

# Strategy 3: Stale-while-revalidate
stampede = StampedePrevention(strategy="swr", stale_ttl=60)
data = stampede.get_or_refresh(
    key="expensive:query",
    fetch_fn=lambda: db.run_expensive_query(),
    ttl=300,
)
```

| Strategy | Mechanism | Best For |
|----------|-----------|----------|
| Lock-based | Distributed lock prevents concurrent rebuilds | Low-concurrency hot keys |
| Probabilistic | Random early refresh before TTL expires | High-concurrency hot keys |
| SWR | Serve stale data while async refresh | User-facing latency-sensitive |

### Cache Warming Patterns

Cache warming pre-populates cache before traffic arrives, eliminating cold-start latency.

```python
from caching import CacheWarmer, WarmingStrategy

warmer = CacheWarmer(cache=redis)

# Pattern 1: Scheduled warming
warmer.schedule(
    name="product_catalog",
    fetch_fn=lambda: db.products.find_all_active(),
    ttl=3600,
    cron="0 */6 * * *",  # Every 6 hours
    strategy=WarmingStrategy.PRELOAD,
)

# Pattern 2: Predictive warming based on usage patterns
warmer.predictive(
    name="user_sessions",
    fetch_fn=lambda user_id: db.sessions.get(user_id),
    ttl=600,
    lookback_days=30,
    peak_hours=[9, 10, 11, 14, 15],
)

# Pattern 3: Tiered warming
warmer.tiered(
    name="search_results",
    tiers=[
        {"priority": 1, "fetch_fn": lambda: db.top_searches(), "ttl": 300},
        {"priority": 2, "fetch_fn": lambda: db.recent_searches(), "ttl": 600},
        {"priority": 3, "fetch_fn": lambda: db.all_searches(), "ttl": 1800},
    ],
)
```

### Multi-Region Cache Replication

```python
from caching import MultiRegionCache

cache = MultiRegionCache(
    regions={
        "us-east-1": {"host": "redis-us.example.com", "port": 6379},
        "eu-west-1": {"host": "redis-eu.example.com", "port": 6379},
        "ap-south-1": {"host": "redis-ap.example.com", "port": 6379},
    },
    replication_mode="async",
    conflict_resolution="last_write_wins",
    local_ttl_seconds=30,
)

# Write replicates to all regions asynchronously
cache.set("config:feature_flags", flags, ttl=3600)

# Read from local region first, fallback to nearest
config = cache.get("config:feature_flags")
```

### Cache Eviction Policies

```python
from caching import MemoryCache, EvictionPolicy

# LRU (default) Ã¢â‚¬â€ evicts least recently accessed
cache_lru = MemoryCache(max_size=10000, eviction=EvictionPolicy.LRU)

# LFU Ã¢â‚¬â€ evicts least frequently accessed
cache_lfu = MemoryCache(max_size=10000, eviction=EvictionPolicy.LFU)

# FIFO Ã¢â‚¬â€ evicts oldest entries
cache_fifo = MemoryCache(max_size=10000, eviction=EvictionPolicy.FIFO)

# Random Ã¢â‚¬â€ random eviction
cache_random = MemoryCache(max_size=10000, eviction=EvictionPolicy.RANDOM)

# ARC Ã¢â‚¬â€ adaptive replacement cache
cache_arc = MemoryCache(max_size=10000, eviction=EvictionPolicy.ARC)
```

| Policy | Hit Rate | Memory Efficiency | Use Case |
|--------|----------|-------------------|----------|
| LRU | High | Medium | General purpose |
| LFU | Highest | Medium | Stable access patterns |
| FIFO | Low | High | Time-limited data |
| ARC | Highest | High | Mixed workloads |

### Cache Compression

```python
from caching import CompressedRedisCache, CompressionAlgorithm

cache = CompressedRedisCache(
    host="redis.example.com",
    port=6379,
    compression=CompressionAlgorithm.ZSTD,
    compression_threshold_bytes=1024,  # Only compress values > 1KB
    compression_level=3,
)

# Values > 1KB are automatically compressed
cache.set("large:json", large_json_data, ttl=3600)

# Check compression stats
stats = cache.compression_stats()
print(f"Compressed: {stats.compressed_count}")
print(f"Ratio: {stats.compression_ratio:.2f}")
print(f"Bytes saved: {stats.bytes_saved}")
```

### Cache warming benchmark results

| Cache Layer | Access Time | Throughput | Memory Overhead |
|-------------|-------------|------------|-----------------|
| L1 In-Memory | 0.01ms | 1M ops/s | 50 bytes/entry |
| L2 Redis | 0.5ms | 100K ops/s | 100 bytes/entry |
| L3 CDN | 5ms | 50K req/s | N/A (edge) |
| L4 Database | 10ms | 5K queries/s | N/A |

### Redis Sentinel High Availability

```python
from caching import RedisSentinel

sentinel = RedisSentinel(
    sentinels=[
        ("sentinel-1", 26379),
        ("sentinel-2", 26379),
        ("sentinel-3", 26379),
    ],
    service_name="mymaster",
    password="secret",
    socket_timeout=5,
)

# Automatic failover
master = sentinel.master_for()
slave = sentinel.slave_for(read_only=True)

master.set("key", "value")
data = slave.get("key")
```

### Cache Invalidation via Message Queue

```python
from caching import MQCacheInvalidation

invalidator = MQCacheInvalidation(
    mq_backend="rabbitmq",
    exchange="cache-invalidation",
    queue="cache-workers",
)

# Publisher invalidates cache
invalidator.invalidate(
    pattern="user:{user_id}:*",
    context={"user_id": 123, "reason": "profile_update"},
)

# Consumers listen for invalidations
@invalidator.on_invalidate
def handle_invalidation(message):
    cache.delete_pattern(message.pattern)
    log.info(f"Invalidated: {message.pattern}")
```

### Performance Benchmarks

```python
from caching import BenchmarkSuite

bench = BenchmarkSuite(cache=redis)

# Run standard benchmark
results = bench.run(
    operations=["get", "set", "delete", "pipeline"],
    key_count=100000,
    value_sizes=["1KB", "10KB", "100KB"],
    duration_s=60,
)

# Output:
# get:    125,000 ops/s, p99=0.8ms
# set:    98,000 ops/s,  p99=1.2ms
# delete: 110,000 ops/s, p99=0.9ms
# pipeline(100): 850,000 ops/s, p99=2.1ms
```

### Cache Analytics Dashboard

```python
from caching import CacheAnalytics

analytics = CacheAnalytics(cache=redis)

# Real-time metrics
metrics = analytics.get_metrics(window_minutes=5)
print(f"Hit rate: {metrics.hit_rate:.2%}")
print(f"Miss rate: {metrics.miss_rate:.2%}")
print(f"Avg latency: {metrics.avg_latency_ms:.2f}ms")
print(f"Memory usage: {metrics.memory_used_mb:.1f}MB")
print(f"Evictions/min: {metrics.evictions_per_minute:.0f}")

# Top keys by access count
top_keys = analytics.top_keys(limit=10, window_minutes=60)
for key in top_keys:
    print(f"  {key.name}: {key.access_count} hits, {key.avg_latency_ms:.2f}ms")

# Cache efficiency report
report = analytics.efficiency_report()
print(f"TTL optimization: {report.ttl_recommendation}")
print(f"Key size optimization: {report.key_recommendation}")
print(f"Value compression: {report.compression_recommendation}")
```

### Circuit Breaker for Cache

```python
from caching import CircuitBreakerCache

cache = CircuitBreakerCache(
    redis=redis,
    failure_threshold=5,
    recovery_timeout_s=30,
    half_open_max_requests=3,
)

# Automatically falls back to direct DB on Redis failure
try:
    data = cache.get("key")
except CacheUnavailable:
    # Circuit is open Ã¢â‚¬â€ Redis is down
    data = db.get("key")
    cache.set("key", data, ttl=60)  # Cache to local fallback
```

### Cache warming benchmark results

| Cache Layer | Access Time | Throughput | Memory Overhead |
|-------------|-------------|------------|-----------------|
| L1 In-Memory | 0.01ms | 1M ops/s | 50 bytes/entry |
| L2 Redis | 0.5ms | 100K ops/s | 100 bytes/entry |
| L3 CDN | 5ms | 50K req/s | N/A (edge) |
| L4 Database | 10ms | 5K queries/s | N/A |

### Redis Sentinel High Availability

```python
from caching import RedisSentinel

sentinel = RedisSentinel(
    sentinels=[
        ("sentinel-1", 26379),
        ("sentinel-2", 26379),
        ("sentinel-3", 26379),
    ],
    service_name="mymaster",
    password="secret",
    socket_timeout=5,
)

# Automatic failover
master = sentinel.master_for()
slave = sentinel.slave_for(read_only=True)

master.set("key", "value")
data = slave.get("key")
```

### Cache Invalidation via Message Queue

```python
from caching import MQCacheInvalidation

invalidator = MQCacheInvalidation(
    mq_backend="rabbitmq",
    exchange="cache-invalidation",
    queue="cache-workers",
)

# Publisher invalidates cache
invalidator.invalidate(
    pattern="user:{user_id}:*",
    context={"user_id": 123, "reason": "profile_update"},
)

# Consumers listen for invalidations
@invalidator.on_invalidate
def handle_invalidation(message):
    cache.delete_pattern(message.pattern)
    log.info(f"Invalidated: {message.pattern}")
```

### Performance Benchmarks

```python
from caching import BenchmarkSuite

bench = BenchmarkSuite(cache=redis)

# Run standard benchmark
results = bench.run(
    operations=["get", "set", "delete", "pipeline"],
    key_count=100000,
    value_sizes=["1KB", "10KB", "100KB"],
    duration_s=60,
)

# Output:
# get:    125,000 ops/s, p99=0.8ms
# set:    98,000 ops/s,  p99=1.2ms
# delete: 110,000 ops/s, p99=0.9ms
# pipeline(100): 850,000 ops/s, p99=2.1ms
```

### Cache Analytics Dashboard

```python
from caching import CacheAnalytics

analytics = CacheAnalytics(cache=redis)

# Real-time metrics
metrics = analytics.get_metrics(window_minutes=5)
print(f"Hit rate: {metrics.hit_rate:.2%}")
print(f"Miss rate: {metrics.miss_rate:.2%}")
print(f"Avg latency: {metrics.avg_latency_ms:.2f}ms")
print(f"Memory usage: {metrics.memory_used_mb:.1f}MB")
print(f"Evictions/min: {metrics.evictions_per_minute:.0f}")

# Top keys by access count
top_keys = analytics.top_keys(limit=10, window_minutes=60)
for key in top_keys:
    print(f"  {key.name}: {key.access_count} hits, {key.avg_latency_ms:.2f}ms")

# Cache efficiency report
report = analytics.efficiency_report()
print(f"TTL optimization: {report.ttl_recommendation}")
print(f"Key size optimization: {report.key_recommendation}")
print(f"Value compression: {report.compression_recommendation}")
```

### Circuit Breaker for Cache

```python
from caching import CircuitBreakerCache

cache = CircuitBreakerCache(
    redis=redis,
    failure_threshold=5,
    recovery_timeout_s=30,
    half_open_max_requests=3,
)

# Automatically falls back to direct DB on Redis failure
try:
    data = cache.get("key")
except CacheUnavailable:
    # Circuit is open Ã¢â‚¬â€ Redis is down
    data = db.get("key")
    cache.set("key", data, ttl=60)  # Cache to local fallback
```

### Cache Key Naming Conventions

| Pattern | Example | Use Case |
|---------|---------|----------|
| `{service}:{entity}:{id}` | `api:user:123` | Single entity cache |
| `{service}:{entity}:{id}:{field}` | `api:user:123:profile` | Partial entity cache |
| `{service}:{collection}:{query_hash}` | `api:products:a1b2c3` | Query result cache |
| `{service}:lock:{key}` | `api:lock:user:123` | Distributed lock |
| `{service}:counter:{metric}` | `api:counter:pageviews` | Rate limiting |

### Memory-Mapped Cache for Large Datasets

```python
from caching import MMapCache

cache = MMapCache(
    file_path="/dev/shm/cache.bin",
    max_size_bytes=1024 * 1024 * 1024,  # 1GB
    page_size_bytes=4096,
)

# Near-zero latency for large read-heavy datasets
cache.set("dataset:full", full_dataset)
data = cache.get("dataset:full")
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills


## Additional Resources

### Related Technologies

This module integrates with industry-standard tools and frameworks. Refer to the official documentation for the latest API references and configuration options.

### Community and Support

- Open source contributions welcome
- Issue tracking via GitHub Issues
- Documentation updated with each release
- Community forums for discussion and support

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-01 | Initial release |
| 1.1.0 | 2026-03-15 | Enhanced configuration options |
| 1.2.0 | 2026-06-01 | Performance improvements |
| 2.0.0 | 2026-07-01 | Major architecture update |

### License

MIT License - Copyright (c) 2026 Awesome Grok Skills


## Extended Reference

### Configuration Matrix

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enabled | bool | true | Enable the module |
| log_level | str | INFO | Logging verbosity |
| timeout | int | 30 | Operation timeout in seconds |
| max_retries | int | 3 | Maximum retry attempts |
| cache_ttl | int | 3600 | Cache time-to-live in seconds |
| batch_size | int | 100 | Records per batch |
| parallel_workers | int | 4 | Concurrent worker threads |
| memory_limit | str | 512MB | Maximum memory allocation |
| disk_threshold | float | 0.8 | Disk usage alert threshold |
| health_check_interval | int | 60 | Health check frequency seconds |

### Environment Variables

`ash
MODULE_ENABLED=true
MODULE_LOG_LEVEL=INFO
MODULE_TIMEOUT=30
MODULE_MAX_RETRIES=3
MODULE_CACHE_TTL=3600
MODULE_BATCH_SIZE=100
MODULE_PARALLEL_WORKERS=4
MODULE_MEMORY_LIMIT=512MB
MODULE_DISK_THRESHOLD=0.8
MODULE_HEALTH_CHECK_INTERVAL=60
```n
### Docker Configuration

`yaml
version: '3.8'
services:
  module:
    image: awesome-grok/module:latest
    environment:
      - MODULE_ENABLED=true
      - MODULE_LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    ports:
      - '8080:8080'
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8080/health']
      interval: 30s
      timeout: 10s
      retries: 3
```n
### Kubernetes Deployment

`yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: module-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: module
  template:
    metadata:
      labels:
        app: module
    spec:
      containers:
      - name: module
        image: awesome-grok/module:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: 256Mi
            cpu: 250m
          limits:
            memory: 512Mi
            cpu: 500m
```n
### Prometheus Metrics

`yaml
scrape_configs:
  - job_name: 'module'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: /metrics
    scrape_interval: 15s
```n
### Grafana Dashboard

Import dashboard ID 12345 from Grafana.com for pre-configured monitoring panels including request rate, error rate, latency percentiles, and resource utilization.

### Alert Rules

`yaml
groups:
  - name: module-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(module_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(module_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
```n
### CI/CD Pipeline

`yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v
      - run: python -m mypy src/
      - run: python -m ruff check src/
```n
