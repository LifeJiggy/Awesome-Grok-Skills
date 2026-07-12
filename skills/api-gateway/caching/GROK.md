---
name: "caching"
category: "api-gateway"
version: "2.0.0"
tags: ["caching", "cdn", "redis", "cache-invalidation", "response-cache", "ttl", "edge-cache"]
---

# Gateway Caching

## Overview

Gateway-level response caching platform for reducing upstream load and improving API response times. This module implements in-memory, Redis-backed, and CDN edge caching with configurable TTLs, cache key strategies, ETag-based conditional requests, cache invalidation (manual, TTL, event-driven), and cache warming. Supports per-endpoint cache policies, vary headers, cache-busting, and stale-while-revalidate patterns.

## Core Capabilities

- **Multi-Layer Caching**: In-memory (L1), Redis (L2), and CDN edge (L3) caching hierarchy
- **Cache Key Strategies**: URL-based, header-based, query-param-based, and custom cache key functions
- **Conditional Requests**: ETag and Last-Modified headers for 304 Not Modified responses
- **Cache Invalidation**: TTL-based, manual purge, event-driven, and pattern-based invalidation
- **Stale-While-Revalidate**: Serve stale responses while refreshing in background
- **Vary Headers**: Cache different variants based on Accept, Accept-Language, or custom headers
- **Cache Warming**: Pre-populate cache for critical endpoints on startup or schedule
- **Metrics**: Cache hit rate, miss rate, size, eviction count, and per-endpoint statistics

## Usage

```python
from caching import (
    CacheManager, CacheLayer, CachePolicy, CacheKey, ETagHandler
)

# Initialize cache manager
cache = CacheManager(
    l1_size_mb=256,
    l2_redis_url="redis://localhost:6379",
    default_ttl_seconds=300,
)

# Configure per-endpoint policies
cache.add_policy(CachePolicy(
    endpoint="GET /api/products",
    ttl_seconds=600,
    vary_headers=["Accept-Language"],
    cache_key=CacheKey(
        include_path=True,
        include_query=True,
        include_headers=["Authorization"],
        exclude_query_params=["timestamp"],
    ),
    stale_while_revalidate_s=60,
    stale_if_error_s=3600,
))

cache.add_policy(CachePolicy(
    endpoint="GET /api/config",
    ttl_seconds=3600,
    vary_headers=[],
    tags=["config"],
))

# Check cache
result = cache.get(
    key="GET /api/products?category=electronics",
    headers={"Accept-Language": "en"},
)
if result.hit:
    print(f"Cache HIT: {result.data}")
    print(f"Age: {result.age_seconds}s, TTL: {result.ttl_seconds}s")
else:
    # Fetch from upstream and cache
    data = fetch_from_upstream()
    cache.set(key=result.key, value=data, ttl=300, tags=["products"])

# ETag handling
etag_handler = ETagHandler()
etag = etag_handler.generate(data)
if etag_handler.check_match(request_headers, etag):
    return Response(status=304)

# Cache invalidation
cache.invalidate_pattern("/api/products/*")
cache.invalidate_tag("products")

# Metrics
metrics = cache.get_metrics()
print(f"Hit rate: {metrics['hit_rate']:.1%}")
print(f"Total hits: {metrics['hits']}, misses: {metrics['misses']}")
print(f"Memory used: {metrics['l1_size_mb']:.1f} MB")
```

## Best Practices

- Cache at the gateway level to reduce load on all backend services
- Use appropriate TTLs: short (1-5 min) for dynamic data, long (1hr+) for static
- Implement cache warming for critical endpoints to avoid cold-start misses
- Use ETag-based conditional requests to reduce bandwidth and improve freshness
- Implement stale-while-revalidate for high-traffic endpoints to serve stale data during refresh
- Use cache tags for efficient bulk invalidation when related data changes
- Monitor cache hit rates per endpoint — below 50% suggests misconfigured policies
- Set appropriate cache size limits to prevent memory exhaustion
- Use Vary headers correctly to cache personalized responses without over-caching
- Test cache behavior under load to verify eviction and refresh patterns

## Related Modules

- **api-management** — Gateway-level caching plugin configuration
- **load-balancing** — Cache-aware load balancing decisions
- **rate-limiting** — Cached rate limit counters for performance
- **api-monitoring** — Cache metrics and hit rate monitoring
- **api** → **api-design** — Cache-friendly API design patterns
