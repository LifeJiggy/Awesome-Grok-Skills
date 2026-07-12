"""
Gateway Caching Module — Multi-layer caching, ETag handling, cache invalidation,
cache warming, stale-while-revalidate, and cache metrics for API gateways.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class CacheLayer(Enum):
    L1_MEMORY = "l1_memory"
    L2_REDIS = "l2_redis"
    L3_CDN = "l3_cdn"


class EvictionPolicy(Enum):
    LRU = "lru"
    LFU = "lfu"
    FIFO = "fifo"
    TTL = "ttl"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class CacheKey:
    """Cache key configuration."""
    include_path: bool = True
    include_query: bool = True
    include_headers: List[str] = field(default_factory=list)
    exclude_query_params: List[str] = field(default_factory=list)
    prefix: str = ""
    custom_function: Optional[str] = None

    def generate(self, method: str, path: str, query_params: Optional[Dict[str, str]] = None,
                 headers: Optional[Dict[str, str]] = None) -> str:
        parts = [method.upper(), path] if self.include_path else [method.upper()]
        if self.include_query and query_params:
            filtered = {k: v for k, v in query_params.items() if k not in self.exclude_query_params}
            parts.append(json.dumps(filtered, sort_keys=True))
        if self.include_headers and headers:
            header_parts = {h: headers.get(h, "") for h in self.include_headers}
            parts.append(json.dumps(header_parts, sort_keys=True))
        key = ":".join(parts)
        if self.prefix:
            key = f"{self.prefix}:{key}"
        return hashlib.sha256(key.encode()).hexdigest()[:32]


@dataclass
class CachePolicy:
    """Caching policy for an endpoint."""
    endpoint: str
    ttl_seconds: int = 300
    cache_key: CacheKey = field(default_factory=CacheKey)
    vary_headers: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    stale_while_revalidate_s: int = 0
    stale_if_error_s: int = 0
    bypass_cache: bool = False
    cache_request_body: bool = False
    max_cache_size_bytes: int = 1_000_000

    def to_dict(self) -> Dict[str, Any]:
        return {
            "endpoint": self.endpoint,
            "ttl": self.ttl_seconds,
            "vary_headers": self.vary_headers,
            "tags": self.tags,
        }


@dataclass
class CacheEntry:
    """A single cache entry."""
    key: str
    value: Any
    created_at: float = field(default_factory=time.time)
    ttl_seconds: int = 300
    tags: List[str] = field(default_factory=list)
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)
    etag: str = ""
    content_type: str = "application/json"

    @property
    def age_seconds(self) -> float:
        return time.time() - self.created_at

    @property
    def remaining_ttl(self) -> float:
        return max(0, self.ttl_seconds - self.age_seconds)

    @property
    def is_expired(self) -> bool:
        return self.age_seconds > self.ttl_seconds

    @property
    def is_stale_while_revalidatable(self) -> bool:
        return self.is_expired and self.remaining_ttl > -60

    def touch(self) -> None:
        self.last_accessed = time.time()
        self.access_count += 1


@dataclass
class CacheResult:
    """Result of a cache lookup."""
    hit: bool
    key: str
    data: Any = None
    age_seconds: float = 0
    ttl_seconds: float = 0
    layer: CacheLayer = CacheLayer.L1_MEMORY
    etag: str = ""
    from_stale: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hit": self.hit,
            "key": self.key,
            "age": round(self.age_seconds, 1),
            "ttl": round(self.ttl_seconds, 1),
            "layer": self.layer.value,
        }


@dataclass
class CacheMetrics:
    """Cache performance metrics."""
    hits: int = 0
    misses: int = 0
    l1_hits: int = 0
    l2_hits: int = 0
    l3_hits: int = 0
    evictions: int = 0
    invalidations: int = 0
    total_entries: int = 0
    total_size_bytes: int = 0
    avg_entry_size_bytes: float = 0
    per_endpoint: Dict[str, Dict[str, int]] = field(default_factory=dict)

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(self.hit_rate, 4),
            "l1_hits": self.l1_hits,
            "l2_hits": self.l2_hits,
            "total_entries": self.total_entries,
            "total_size_mb": round(self.total_size_bytes / (1024 * 1024), 2),
        }


@dataclass
class ETagResult:
    """ETag generation and validation result."""
    etag: str
    matches: bool = False
    last_modified: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"etag": self.etag, "matches": self.matches}


@dataclass
class CacheWarmingTask:
    """A cache warming task."""
    task_id: str
    endpoint: str
    cache_key: str
    schedule: str = ""  # cron expression
    warm_function: str = ""
    enabled: bool = True
    last_warmed: Optional[str] = None
    warm_count: int = 0


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class ETagHandler:
    """Generate and validate ETags for conditional requests."""

    def generate(self, data: Any) -> str:
        content = json.dumps(data, sort_keys=True) if isinstance(data, dict) else str(data)
        return f'"{hashlib.md5(content.encode()).hexdigest()}"'

    def check_match(self, request_headers: Dict[str, str], current_etag: str) -> bool:
        if_none_match = request_headers.get("If-None-Match", "")
        if if_none_match:
            if if_none_match == "*" or if_none_match == current_etag:
                return True
            # Handle list of ETags
            etags = [e.strip() for e in if_none_match.split(",")]
            return current_etag in etags
        return False

    def check_modified(self, request_headers: Dict[str, str], last_modified: str) -> bool:
        if_modified_since = request_headers.get("If-Modified-Since", "")
        if if_modified_since and last_modified:
            return last_modified > if_modified_since
        return False


class InMemoryCache:
    """L1 in-memory cache with LRU eviction."""

    def __init__(self, max_size_mb: int = 256, max_entries: int = 10000):
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.max_entries = max_entries
        self._entries: Dict[str, CacheEntry] = {}
        self._size_bytes: int = 0

    def get(self, key: str) -> Optional[CacheEntry]:
        entry = self._entries.get(key)
        if entry and not entry.is_expired:
            entry.touch()
            return entry
        if entry and entry.is_expired:
            self._remove(key)
        return None

    def set(self, key: str, value: Any, ttl: int = 300, tags: Optional[List[str]] = None) -> None:
        entry_size = len(json.dumps(value).encode()) if isinstance(value, (dict, list)) else len(str(value).encode())

        # Evict if necessary
        while (self._size_bytes + entry_size > self.max_size_bytes or
               len(self._entries) >= self.max_entries):
            if not self._entries:
                break
            self._evict_lru()

        if key in self._entries:
            self._size_bytes -= self._estimate_size(self._entries[key])

        entry = CacheEntry(key=key, value=value, ttl_seconds=ttl, tags=tags or [])
        self._entries[key] = entry
        self._size_bytes += entry_size

    def invalidate(self, key: str) -> bool:
        if key in self._entries:
            self._remove(key)
            return True
        return False

    def invalidate_pattern(self, pattern: str) -> int:
        prefix = pattern.replace("*", "")
        keys_to_remove = [k for k in self._entries if k.startswith(prefix)]
        for key in keys_to_remove:
            self._remove(key)
        return len(keys_to_remove)

    def invalidate_tag(self, tag: str) -> int:
        keys_to_remove = [k for k, v in self._entries.items() if tag in v.tags]
        for key in keys_to_remove:
            self._remove(key)
        return len(keys_to_remove)

    def clear(self) -> None:
        self._entries.clear()
        self._size_bytes = 0

    def _evict_lru(self) -> None:
        if not self._entries:
            return
        lru_key = min(self._entries, key=lambda k: self._entries[k].last_accessed)
        self._remove(lru_key)

    def _remove(self, key: str) -> None:
        if key in self._entries:
            self._size_bytes -= self._estimate_size(self._entries[key])
            del self._entries[key]

    def _estimate_size(self, entry: CacheEntry) -> int:
        return len(json.dumps(entry.value).encode()) if isinstance(entry.value, (dict, list)) else len(str(entry.value).encode())

    @property
    def size_bytes(self) -> int:
        return self._size_bytes

    @property
    def entry_count(self) -> int:
        return len(self._entries)


class CacheManager:
    """Multi-layer cache manager with policies and warming."""

    def __init__(self, l1_size_mb: int = 256, l2_redis_url: Optional[str] = None,
                 default_ttl_seconds: int = 300):
        self.default_ttl = default_ttl_seconds
        self._l1 = InMemoryCache(max_size_mb=l1_size_mb)
        self._policies: Dict[str, CachePolicy] = {}
        self._metrics = CacheMetrics()
        self._etag_handler = ETagHandler()
        self._warming_tasks: List[CacheWarmingTask] = []

    def add_policy(self, policy: CachePolicy) -> None:
        self._policies[policy.endpoint] = policy

    def get(self, key: str, headers: Optional[Dict[str, str]] = None) -> CacheResult:
        # Try L1
        entry = self._l1.get(key)
        if entry:
            self._metrics.hits += 1
            self._metrics.l1_hits += 1
            return CacheResult(
                hit=True, key=key, data=entry.value,
                age_seconds=entry.age_seconds, ttl_seconds=entry.remaining_ttl,
                layer=CacheLayer.L1_MEMORY, etag=entry.etag,
            )

        # L1 miss
        self._metrics.misses += 1
        return CacheResult(hit=False, key=key)

    def set(self, key: str, value: Any, ttl: Optional[int] = None,
            tags: Optional[List[str]] = None, endpoint: str = "") -> None:
        policy = self._policies.get(endpoint)
        effective_ttl = ttl or (policy.ttl_seconds if policy else self.default_ttl)
        effective_tags = tags or (policy.tags if policy else [])

        etag = self._etag_handler.generate(value)
        entry = CacheEntry(key=key, value=value, ttl_seconds=effective_ttl,
                          tags=effective_tags, etag=etag)
        self._l1.set(key, value, ttl=effective_ttl, tags=effective_tags)
        self._metrics.total_entries = self._l1.entry_count
        self._metrics.total_size_bytes = self._l1.size_bytes

    def invalidate(self, key: str) -> bool:
        self._metrics.invalidations += 1
        return self._l1.invalidate(key)

    def invalidate_pattern(self, pattern: str) -> int:
        count = self._l1.invalidate_pattern(pattern)
        self._metrics.invalidations += count
        return count

    def invalidate_tag(self, tag: str) -> int:
        count = self._l1.invalidate_tag(tag)
        self._metrics.invalidations += count
        return count

    def generate_cache_key(self, method: str, path: str, query_params: Optional[Dict[str, str]] = None,
                          headers: Optional[Dict[str, str]] = None, endpoint: str = "") -> str:
        policy = self._policies.get(endpoint)
        cache_key = policy.cache_key if policy else CacheKey()
        return cache_key.generate(method, path, query_params, headers)

    def get_etag(self, data: Any) -> str:
        return self._etag_handler.generate(data)

    def check_etag_match(self, headers: Dict[str, str], etag: str) -> bool:
        return self._etag_handler.check_match(headers, etag)

    def add_warming_task(self, endpoint: str, cache_key: str, schedule: str = "") -> CacheWarmingTask:
        task = CacheWarmingTask(
            task_id=f"WARM-{uuid.uuid4().hex[:8].upper()}",
            endpoint=endpoint, cache_key=cache_key, schedule=schedule,
        )
        self._warming_tasks.append(task)
        return task

    def warm_cache(self, key: str, value: Any, ttl: int = 300, tags: Optional[List[str]] = None) -> None:
        self.set(key, value, ttl=ttl, tags=tags)
        for task in self._warming_tasks:
            if task.cache_key == key:
                task.last_warmed = datetime.now(timezone.utc).isoformat()
                task.warm_count += 1

    def get_metrics(self) -> Dict[str, Any]:
        return self._metrics.to_dict()

    def get_entry_count(self) -> int:
        return self._l1.entry_count

    def clear(self) -> None:
        self._l1.clear()
        self._metrics = CacheMetrics()


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the gateway caching toolkit."""
    print("Gateway Caching Toolkit")
    print("=" * 60)

    cache = CacheManager(l1_size_mb=64, default_ttl_seconds=60)

    # Add policies
    cache.add_policy(CachePolicy(
        endpoint="GET /api/products", ttl_seconds=300,
        vary_headers=["Accept-Language"],
        tags=["products"],
    ))
    cache.add_policy(CachePolicy(
        endpoint="GET /api/config", ttl_seconds=3600, tags=["config"],
    ))

    # Cache entries
    print("\n--- Cache Operations ---")
    cache.set("GET:/api/products", {"products": ["A", "B", "C"]}, ttl=300, tags=["products"])
    cache.set("GET:/api/config", {"theme": "dark", "lang": "en"}, ttl=3600, tags=["config"])

    # Lookup
    result = cache.get("GET:/api/products")
    print(f"Products: hit={result.hit}, age={result.age_seconds:.1f}s, ttl={result.ttl_seconds:.1f}s")

    result2 = cache.get("GET:/api/missing")
    print(f"Missing: hit={result2.hit}")

    # ETag
    etag = cache.get_etag({"data": "test"})
    print(f"\nETag: {etag}")
    match = cache.check_etag_match({"If-None-Match": etag}, etag)
    print(f"ETag match: {match}")

    # Invalidation
    cache.invalidate_tag("products")
    result3 = cache.get("GET:/api/products")
    print(f"After invalidation: hit={result3.hit}")

    # Metrics
    metrics = cache.get_metrics()
    print(f"\nMetrics: {json.dumps(metrics, indent=2)}")

    # Warming
    task = cache.add_warming_task("GET /api/products", "warm-key")
    cache.warm_cache("warm-key", {"warmed": True}, ttl=600)
    print(f"\nWarming task: {task.warm_count} times warmed")


if __name__ == "__main__":
    main()
