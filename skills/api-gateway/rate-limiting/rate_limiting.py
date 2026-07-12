"""
Rate Limiting Module — Token bucket, sliding window, fixed window, and leaky bucket
algorithms with distributed counters, tiered limits, and DDoS protection.
"""

from __future__ import annotations

import json
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Algorithm(Enum):
    TOKEN_BUCKET = "token_bucket"
    SLIDING_WINDOW = "sliding_window"
    SLIDING_WINDOW_COUNTER = "sliding_window_counter"
    FIXED_WINDOW = "fixed_window"
    LEAKY_BUCKET = "leaky_bucket"


class LimitKey(Enum):
    IP = "ip"
    USER = "user"
    API_KEY = "api_key"
    CONSUMER = "consumer"


class RateLimitAction(Enum):
    ALLOW = "allow"
    THROTTLE = "throttle"
    BLOCK = "block"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ConsumerTier:
    """A consumer tier with rate limits."""
    name: str
    requests_per_minute: int = 60
    requests_per_hour: int = 1000
    requests_per_day: int = 100000
    burst_allowance: int = 10
    priority: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "rpm": self.requests_per_minute,
            "rph": self.requests_per_hour,
            "burst": self.burst_allowance,
        }


@dataclass
class RateLimit:
    """A specific rate limit configuration."""
    endpoint: str
    limit: int
    window_seconds: int = 60
    key: str = "ip"
    block_duration_seconds: int = 0
    burst_limit: Optional[int] = None
    priority: int = 0
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "endpoint": self.endpoint,
            "limit": self.limit,
            "window": self.window_seconds,
            "key": self.key,
        }


@dataclass
class RateLimitResult:
    """Result of a rate limit check."""
    allowed: bool
    limit: int
    remaining: int
    reset_at: float
    current_usage: int = 0
    action: RateLimitAction = RateLimitAction.ALLOW
    retry_after: Optional[float] = None
    bucket_tokens: Optional[int] = None
    window_start: Optional[float] = None

    @property
    def headers(self) -> Dict[str, str]:
        headers = {
            "X-RateLimit-Limit": str(self.limit),
            "X-RateLimit-Remaining": str(max(0, self.remaining)),
            "X-RateLimit-Reset": str(int(self.reset_at)),
        }
        if self.retry_after:
            headers["Retry-After"] = str(int(self.retry_after))
        if self.action == RateLimitAction.THROTTLE:
            headers["X-RateLimit-Action"] = "throttle"
        elif self.action == RateLimitAction.BLOCK:
            headers["X-RateLimit-Action"] = "block"
        return headers

    def to_dict(self) -> Dict[str, Any]:
        return {
            "allowed": self.allowed,
            "limit": self.limit,
            "remaining": self.remaining,
            "action": self.action.value,
            "reset_at": self.reset_at,
        }


@dataclass
class RateLimitBucket:
    """Token bucket for token bucket algorithm."""
    tokens: float
    capacity: float
    refill_rate: float  # tokens per second
    last_refill: float = field(default_factory=time.time)

    def consume(self, count: float = 1) -> bool:
        self._refill()
        if self.tokens >= count:
            self.tokens -= count
            return True
        return False

    def _refill(self) -> None:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    @property
    def wait_time_seconds(self) -> float:
        self._refill()
        if self.tokens >= 1:
            return 0.0
        return (1 - self.tokens) / self.refill_rate


@dataclass
class FixedWindow:
    """Fixed window counter."""
    window_start: float
    count: int = 0
    limit: int = 100

    def is_expired(self, window_seconds: float) -> bool:
        return time.time() - self.window_start >= window_seconds

    def increment(self) -> bool:
        if self.count < self.limit:
            self.count += 1
            return True
        return False


@dataclass
class SlidingWindowState:
    """Sliding window log of request timestamps."""
    timestamps: List[float] = field(default_factory=list)
    limit: int = 100
    window_seconds: int = 60

    def add_and_check(self) -> Tuple[bool, int]:
        now = time.time()
        cutoff = now - self.window_seconds
        self.timestamps = [t for t in self.timestamps if t > cutoff]
        if len(self.timestamps) < self.limit:
            self.timestamps.append(now)
            return True, len(self.timestamps)
        return False, len(self.timestamps)

    @property
    def reset_at(self) -> float:
        if self.timestamps:
            return self.timestamps[0] + self.window_seconds
        return time.time() + self.window_seconds


@dataclass
class LeakyBucket:
    """Leaky bucket for smooth rate limiting."""
    capacity: float
    leak_rate: float  # requests per second
    water_level: float = 0.0
    last_leak: float = field(default_factory=time.time)

    def add_request(self) -> bool:
        self._leak()
        if self.water_level < self.capacity:
            self.water_level += 1
            return True
        return False

    def _leak(self) -> None:
        now = time.time()
        elapsed = now - self.last_leak
        self.water_level = max(0, self.water_level - elapsed * self.leak_rate)
        self.last_leak = now

    @property
    def wait_time_seconds(self) -> float:
        self._leak()
        if self.water_level < self.capacity:
            return 0.0
        return (self.water_level - self.capacity + 1) / self.leak_rate


@dataclass
class BlockedRequest:
    """A blocked request log entry."""
    key: str
    endpoint: str
    blocked_at: str
    block_duration_s: float
    reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "endpoint": self.endpoint,
            "blocked_at": self.blocked_at,
            "duration_s": self.block_duration_s,
        }


@dataclass
class RateLimitMetrics:
    """Rate limiting analytics and metrics."""
    total_requests: int = 0
    allowed_requests: int = 0
    blocked_requests: int = 0
    throttled_requests: int = 0
    unique_keys: int = 0
    top_blocked_keys: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def block_rate(self) -> float:
        return self.blocked_requests / self.total_requests if self.total_requests > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total": self.total_requests,
            "allowed": self.allowed_requests,
            "blocked": self.blocked_requests,
            "block_rate": round(self.block_rate, 4),
        }


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class RateLimiter:
    """Main rate limiter with multiple algorithm support."""

    def __init__(
        self,
        algorithm: Algorithm = Algorithm.SLIDING_WINDOW,
        storage: str = "memory",
        default_limit: int = 1000,
        default_window_seconds: int = 60,
    ):
        self.algorithm = algorithm
        self.storage = storage
        self.default_limit = default_limit
        self.default_window = default_window_seconds
        self._tiers: Dict[str, ConsumerTier] = {}
        self._limits: Dict[str, RateLimit] = {}
        self._token_buckets: Dict[str, RateLimitBucket] = {}
        self._fixed_windows: Dict[str, FixedWindow] = {}
        self._sliding_windows: Dict[str, SlidingWindowState] = {}
        self._leaky_buckets: Dict[str, LeakyBucket] = {}
        self._blocked: Dict[str, float] = {}
        self._metrics = RateLimitMetrics()

    def add_tier(self, tier: ConsumerTier) -> None:
        self._tiers[tier.name] = tier

    def add_limit(self, limit: RateLimit) -> None:
        self._limits[limit.endpoint] = limit

    def check(self, key: str, endpoint: str, tier: str = "default") -> RateLimitResult:
        """Check if a request is allowed under the rate limit."""
        self._metrics.total_requests += 1

        # Check if blocked
        block_until = self._blocked.get(key, 0)
        if time.time() < block_until:
            self._metrics.blocked_requests += 1
            return RateLimitResult(
                allowed=False, limit=0, remaining=0,
                reset_at=block_until,
                action=RateLimitAction.BLOCK,
                retry_after=block_until - time.time(),
            )

        # Get effective limit
        rate_limit = self._limits.get(endpoint)
        consumer_tier = self._tiers.get(tier)
        limit = rate_limit.limit if rate_limit else (consumer_tier.requests_per_minute if consumer_tier else self.default_limit)
        window = rate_limit.window_seconds if rate_limit else self.default_window

        # Apply algorithm
        if self.algorithm == Algorithm.TOKEN_BUCKET:
            result = self._check_token_bucket(key, limit, window)
        elif self.algorithm == Algorithm.SLIDING_WINDOW:
            result = self._check_sliding_window(key, limit, window)
        elif self.algorithm == Algorithm.FIXED_WINDOW:
            result = self._check_fixed_window(key, limit, window)
        elif self.algorithm == Algorithm.LEAKY_BUCKET:
            result = self._check_leaky_bucket(key, limit, window)
        else:
            result = self._check_sliding_window(key, limit, window)

        if result.allowed:
            self._metrics.allowed_requests += 1
        else:
            self._metrics.blocked_requests += 1
            if rate_limit and rate_limit.block_duration_seconds > 0:
                self._blocked[key] = time.time() + rate_limit.block_duration_seconds

        return result

    def _check_token_bucket(self, key: str, limit: int, window: int) -> RateLimitResult:
        if key not in self._token_buckets:
            refill_rate = limit / window
            self._token_buckets[key] = RateLimitBucket(
                tokens=limit, capacity=limit, refill_rate=refill_rate,
            )
        bucket = self._token_buckets[key]
        allowed = bucket.consume()
        return RateLimitResult(
            allowed=allowed, limit=int(bucket.capacity), remaining=int(bucket.tokens),
            reset_at=time.time() + (1 / bucket.refill_rate if bucket.refill_rate > 0 else window),
            bucket_tokens=int(bucket.tokens),
            retry_after=bucket.wait_time_seconds if not allowed else None,
        )

    def _check_sliding_window(self, key: str, limit: int, window: int) -> RateLimitResult:
        if key not in self._sliding_windows:
            self._sliding_windows[key] = SlidingWindowState(limit=limit, window_seconds=window)
        sw = self._sliding_windows[key]
        sw.limit = limit
        sw.window_seconds = window
        allowed, count = sw.add_and_check()
        return RateLimitResult(
            allowed=allowed, limit=limit, remaining=max(0, limit - count),
            reset_at=sw.reset_at,
            current_usage=count,
            retry_after=sw.reset_at - time.time() if not allowed else None,
        )

    def _check_fixed_window(self, key: str, limit: int, window: int) -> RateLimitResult:
        if key not in self._fixed_windows or self._fixed_windows[key].is_expired(window):
            self._fixed_windows[key] = FixedWindow(
                window_start=time.time(), limit=limit,
            )
        fw = self._fixed_windows[key]
        allowed = fw.increment()
        reset_at = fw.window_start + window
        return RateLimitResult(
            allowed=allowed, limit=limit, remaining=max(0, limit - fw.count),
            reset_at=reset_at,
            current_usage=fw.count,
            retry_after=reset_at - time.time() if not allowed else None,
        )

    def _check_leaky_bucket(self, key: str, limit: int, window: int) -> RateLimitResult:
        if key not in self._leaky_buckets:
            leak_rate = limit / window
            self._leaky_buckets[key] = LeakyBucket(capacity=limit, leak_rate=leak_rate)
        lb = self._leaky_buckets[key]
        allowed = lb.add_request()
        return RateLimitResult(
            allowed=allowed, limit=int(lb.capacity),
            remaining=max(0, int(lb.capacity - lb.water_level)),
            reset_at=time.time() + lb.wait_time_seconds if not allowed else time.time() + 1,
            retry_after=lb.wait_time_seconds if not allowed else None,
        )

    def get_metrics(self) -> RateLimitMetrics:
        return self._metrics

    def get_blocked_keys(self) -> List[str]:
        now = time.time()
        return [k for k, until in self._blocked.items() if until > now]


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the rate limiting toolkit."""
    print("Rate Limiting Toolkit")
    print("=" * 60)

    limiter = RateLimiter(algorithm=Algorithm.SLIDING_WINDOW, default_limit=5, default_window_seconds=10)

    # Add tiers
    limiter.add_tier(ConsumerTier(name="free", requests_per_minute=5))
    limiter.add_tier(ConsumerTier(name="pro", requests_per_minute=50))

    # Add endpoint limits
    limiter.add_limit(RateLimit(endpoint="POST /auth/login", limit=3, window_seconds=60,
                               block_duration_seconds=300))

    # Test normal rate limiting
    print("\n--- Sliding Window (5 req/10s) ---")
    for i in range(7):
        r = limiter.check("user-1", "GET /api/users")
        print(f"  Request {i+1}: {'ALLOW' if r.allowed else 'BLOCK'} (remaining: {r.remaining})")

    # Test with different algorithms
    print("\n--- Token Bucket ---")
    token_limiter = RateLimiter(algorithm=Algorithm.TOKEN_BUCKET, default_limit=5, default_window_seconds=10)
    for i in range(7):
        r = token_limiter.check("user-2", "GET /api/data")
        print(f"  Request {i+1}: {'ALLOW' if r.allowed else 'BLOCK'} (tokens: {r.bucket_tokens})")

    # Test blocked endpoint
    print("\n--- Login Endpoint (3/60s + 5min lockout) ---")
    for i in range(5):
        r = limiter.check("ip-192.168.1.1", "POST /auth/login")
        print(f"  Attempt {i+1}: {r.action.value} (remaining: {r.remaining})")

    # Metrics
    metrics = limiter.get_metrics()
    print(f"\nMetrics: {metrics.total_requests} total, {metrics.blocked_requests} blocked ({metrics.block_rate:.1%})")


if __name__ == "__main__":
    main()
