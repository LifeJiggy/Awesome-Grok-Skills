---
name: "rate-limiting"
category: "api-gateway"
version: "2.0.0"
tags: ["rate-limiting", "throttling", "token-bucket", "sliding-window", "ddos", "backpressure"]
---

# Rate Limiting

## Overview

Distributed rate limiting platform for API gateways implementing multiple algorithms (token bucket, sliding window, fixed window, leaky bucket), per-user/per-endpoint/per-IP limiting, distributed counter synchronization via Redis, graceful degradation under load, and DDoS protection. Supports both API-level and consumer-level rate limits with burst allowances, priority queues, and automatic retry-after headers.

## Core Capabilities

- **Multiple Algorithms**: Token bucket, sliding window log, sliding window counter, fixed window, and leaky bucket
- **Granular Limits**: Per-IP, per-user, per-API-key, per-endpoint, per-method, and global rate limits
- **Distributed Counters**: Redis-backed distributed rate limit counters with atomic operations
- **Burst Handling**: Configurable burst allowances for short traffic spikes
- **Priority Queues**: Tiered rate limits (free/pro/enterprise) with priority-based request handling
- **Graceful Degradation**: Load shedding and backpressure when approaching limits
- **Retry-After Headers**: RFC 7231 compliant retry-after and rate limit headers
- **Analytics**: Real-time rate limit metrics, blocked request tracking, and abuse detection

## Usage

```python
from rate_limiting import (
    RateLimiter, Algorithm, RateLimit, ConsumerTier, SlidingWindow
)

# Configure rate limiter
limiter = RateLimiter(
    algorithm=Algorithm.SLIDING_WINDOW,
    storage="redis://localhost:6379",
    default_limit=1000,
    default_window_seconds=60,
)

# Add tiered limits
limiter.add_tier(ConsumerTier(
    name="free",
    requests_per_minute=60,
    requests_per_hour=1000,
    burst_allowance=10,
))
limiter.add_tier(ConsumerTier(
    name="pro",
    requests_per_minute=600,
    requests_per_hour=10000,
    burst_allowance=50,
))
limiter.add_tier(ConsumerTier(
    name="enterprise",
    requests_per_minute=6000,
    requests_per_hour=100000,
    burst_allowance=200,
))

# Add endpoint-specific limits
limiter.add_limit(RateLimit(
    endpoint="POST /api/auth/login",
    limit=5,
    window_seconds=60,
    key="ip",
    block_duration_seconds=900,  # 15 min lockout
))
limiter.add_limit(RateLimit(
    endpoint="GET /api/search",
    limit=30,
    window_seconds=60,
    key="user",
))

# Check rate limit
result = limiter.check(
    key="user-123",
    endpoint="GET /api/users",
    tier="pro",
)
print(f"Allowed: {result.allowed}")
print(f"Remaining: {result.remaining}/{result.limit}")
print(f"Reset: {result.reset_at}")
print(f"Headers: {result.headers}")
```

## Best Practices

- Apply rate limits at the gateway level to reject excessive requests before they reach services
- Use sliding window algorithms for smoother rate limiting without boundary spikes
- Set per-endpoint limits based on the resource cost of each endpoint
- Implement progressive rate limiting: warn → throttle → block
- Use token bucket for bursty traffic patterns where short bursts are acceptable
- Always return Retry-After headers so clients can implement proper backoff
- Monitor blocked requests to detect abuse patterns and adjust limits
- Implement circuit breakers alongside rate limits for defense in depth
- Use different keys (IP, user, API key) for different rate limiting dimensions
- Test rate limiting under realistic load to verify distributed counter accuracy

## Related Modules

- **api-management** — Gateway-level rate limiting integration
- **authentication** — Rate limiting tied to authenticated consumers
- **load-balancing** — Distribute rate-limited traffic across backends
- **api-security** — DDoS protection and abuse prevention
- **api-monitoring** — Rate limit metrics and alerting
